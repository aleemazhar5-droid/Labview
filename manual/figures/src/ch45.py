"""Figures for Chapter 45 - Data, Computing Hardware and Edge AI in Orbit.

Six figures run real machine-learning code with fixed random seeds on synthetic data: active learning and weak
labels (scikit-learn), domain randomisation for a sim-to-real gap, drift monitoring and retraining, bit-flip
injection into a numpy network, quantisation/pruning of that network, and federated averaging across a simulated
constellation.  The others are computed from physics or from the tables in the chapter.  Numbers quoted in the
chapter text are printed by each function.
"""
import os
import sys
import textwrap
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch  # noqa: F401
from matplotlib.lines import Line2D

FOOT = 6.0


def panel_tag(ax, s, x=-0.02, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, weight="bold", ha="right", va="bottom", color=INK)


def foot(fig, text, y=0.01, width=150):
    """Grey footnote at the bottom right, wrapped so that it never extends beyond the figure width."""
    fig.text(0.99, y, "\n".join(textwrap.wrap(text, width)), ha="right", va="bottom", fontsize=FOOT, color=GREY,
             multialignment="right", linespacing=1.25)


# ==============================================================================================
# Synthetic multispectral pixels (8 Sentinel-2-like bands) for six surface classes.
BANDS_UM = np.array([0.49, 0.56, 0.665, 0.705, 0.74, 0.842, 1.61, 2.19])
CLASSES = ["Water", "Vegetation", "Soil", "Urban", "Snow", "Cloud"]
SPECTRA = np.array([
    [0.070, 0.060, 0.040, 0.030, 0.020, 0.015, 0.008, 0.005],   # water
    [0.040, 0.080, 0.045, 0.120, 0.300, 0.380, 0.220, 0.110],   # vegetation
    [0.100, 0.140, 0.180, 0.200, 0.220, 0.250, 0.320, 0.280],   # soil
    [0.120, 0.130, 0.140, 0.150, 0.160, 0.180, 0.200, 0.180],   # urban
    [0.880, 0.860, 0.830, 0.800, 0.780, 0.740, 0.100, 0.060],   # snow
    [0.700, 0.700, 0.700, 0.700, 0.700, 0.690, 0.550, 0.400],   # thick cloud
])


def pixels(n, rng, probs=None, noise=0.025, gain=None, var=0.10):
    """Pixels = class spectrum x brightness, with spectral variability, thin-cloud contamination and noise.
    Cloud pixels are a mixture of cloud (45-100 %) over a random surface, so thin cloud overlaps clear classes."""
    probs = np.ones(6) / 6 if probs is None else np.asarray(probs)
    y = rng.choice(6, n, p=probs)
    X = SPECTRA[y].copy()
    X *= rng.uniform(0.8, 1.2, (n, 1))
    X *= 1 + rng.normal(0, var, (n, 8))
    clear = y != 5
    m = clear & (rng.random(n) < 0.35)
    f = rng.uniform(0, 0.55, m.sum())
    X[m] = (1 - f)[:, None] * X[m] + f[:, None] * SPECTRA[5]
    c = ~clear
    surf = SPECTRA[rng.integers(0, 5, c.sum())] * rng.uniform(0.8, 1.2, (c.sum(), 1))
    f = rng.uniform(0.45, 1.0, c.sum())
    X[c] = (1 - f)[:, None] * surf + f[:, None] * SPECTRA[5] * rng.uniform(0.85, 1.15, (c.sum(), 1))
    X += rng.normal(0, noise, (n, 8))
    if gain is not None:
        X = X * gain
    return X, y


# ----------------------------------------------------------------------------------------------
# A small numpy multilayer perceptron (8 -> 64 -> 64 -> 6, ReLU, softmax) trained with Adam.
def mlp_init(sizes, rng):
    return [[rng.normal(0, np.sqrt(2.0 / a), (a, b)), np.zeros(b)] for a, b in zip(sizes[:-1], sizes[1:])]


def mlp_logits(P, X, Ws=None):
    h = X
    Ws = [W for W, _ in P] if Ws is None else Ws
    for i, ((_, b), W) in enumerate(zip(P, Ws)):
        h = h @ W + b
        if i < len(P) - 1:
            h = np.maximum(h, 0)
    return h


def mlp_acc(P, X, y, Ws=None):
    with np.errstate(all="ignore"):
        z = mlp_logits(P, X, Ws)
    z = np.where(np.isfinite(z), z, 0.0)
    return float(np.mean(np.argmax(z, axis=1) == y))


def mlp_train(P, X, y, epochs, lr, seed, bs=128, wq=None, masks=None):
    """Adam on cross-entropy. wq: function W -> quantised W used in the forward pass (straight-through
    estimator for quantisation-aware training). masks: fixed pruning masks."""
    rng = np.random.default_rng(seed)
    m = [[np.zeros_like(W), np.zeros_like(b)] for W, b in P]
    v = [[np.zeros_like(W), np.zeros_like(b)] for W, b in P]
    t = 0
    n = len(X)
    for _ in range(epochs):
        idx = rng.permutation(n)
        for k in range(0, n, bs):
            j = idx[k:k + bs]
            hs = [X[j]]
            Ws = [(wq(W) if wq else W) * (masks[i] if masks else 1.0) for i, (W, _) in enumerate(P)]
            h = X[j]
            for i, ((_, b), W) in enumerate(zip(P, Ws)):
                h = h @ W + b
                if i < len(P) - 1:
                    h = np.maximum(h, 0)
                hs.append(h)
            z = hs[-1] - hs[-1].max(axis=1, keepdims=True)
            p = np.exp(z)
            p /= p.sum(axis=1, keepdims=True)
            p[np.arange(len(j)), y[j]] -= 1
            d = p / len(j)
            t += 1
            for i in range(len(P) - 1, -1, -1):
                gW = hs[i].T @ d
                gb = d.sum(axis=0)
                if i > 0:
                    d = (d @ Ws[i].T) * (hs[i] > 0)
                if masks:
                    gW = gW * masks[i]
                for q, g in enumerate((gW, gb)):
                    m[i][q] = 0.9 * m[i][q] + 0.1 * g
                    v[i][q] = 0.999 * v[i][q] + 0.001 * g * g
                    mh = m[i][q] / (1 - 0.9 ** t)
                    vh = v[i][q] / (1 - 0.999 ** t)
                    P[i][q] = P[i][q] - lr * mh / (np.sqrt(vh) + 1e-8)
    return P


_NET = {}


def trained_net():
    """Train (once) the reference network used by the bit-flip and compression figures."""
    if _NET:
        return _NET
    rng = np.random.default_rng(45)
    Xtr, ytr = pixels(20000, rng)
    Xte, yte = pixels(8000, rng)
    mu, sd = Xtr.mean(axis=0), Xtr.std(axis=0)
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    P = mlp_init([8, 64, 64, 6], np.random.default_rng(1))
    P = mlp_train(P, Xtr, ytr, epochs=40, lr=3e-3, seed=2)
    P = [[W.astype(np.float32), b.astype(np.float32)] for W, b in P]
    _NET.update(P=P, Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte, acc=mlp_acc(P, Xte, yte))
    nW = sum(W.size for W, _ in P)
    nb = sum(b.size for _, b in P)
    print(f"reference net: {nW} weights + {nb} biases = {nW + nb} parameters; float32 test acc {_NET['acc']:.4f}")
    return _NET


def quantise(W, bits, per_channel=False):
    qmax = 2 ** (bits - 1) - 1
    s = (np.abs(W).max(axis=0, keepdims=True) if per_channel else np.abs(W).max()) / qmax
    return np.clip(np.round(W / s), -qmax, qmax) * s


# ==============================================================================================
def bitflips():
    """Inject random bit flips into stored weights: float32 vs int8, unprotected and with ECC / TMR."""
    net = trained_net()
    P, Xte, yte = net["P"], net["Xte"][:2000], net["yte"][:2000]
    Ws32 = [W.copy() for W, _ in P]
    shapes = [W.shape for W in Ws32]
    sizes = [W.size for W in Ws32]
    flat32 = np.concatenate([W.ravel() for W in Ws32]).astype(np.float32)
    # int8 per-tensor symmetric quantisation of the same weights
    scales = [np.abs(W).max() / 127 for W in Ws32]
    q8 = np.concatenate([np.clip(np.round(W.ravel() / s), -127, 127) for W, s in zip(Ws32, scales)]).astype(np.int8)
    wmax = [np.abs(W).max() for W in Ws32]
    acc32 = mlp_acc(P, Xte, yte)
    acc8 = mlp_acc(P, Xte, yte, unflat(q8.astype(np.float32), shapes, sizes, scales))
    print(f"bitflips: clean acc float32 {acc32:.4f}, int8 {acc8:.4f}")

    def as_bits(fmt):
        return (flat32.view(np.uint32).copy(), 32) if fmt == "f32" else (q8.view(np.uint8).copy(), 8)

    def decode(words, fmt, check=False):
        if fmt == "f32":
            with np.errstate(all="ignore"):
                w = words.view(np.float32).astype(np.float64)
            Ws = unflat(w, shapes, sizes, None)
            if check:
                Ws = [np.where(np.isfinite(W) & (np.abs(W) <= 2 * mx), W, 0.0) for W, mx in zip(Ws, wmax)]
            return Ws
        return unflat(words.view(np.int8).astype(np.float64), shapes, sizes, scales)

    def flip(words, nbits, positions):
        pos = np.asarray(positions, dtype=np.int64)
        if pos.size == 0:
            return words
        widx, bidx = pos // nbits, (pos % nbits).astype(words.dtype)
        np.bitwise_xor.at(words, widx, words.dtype.type(1) << bidx)
        return words

    def run(fmt, prot, ber, rng):
        words, nb = as_bits(fmt)
        nbits = words.size * nb
        if prot == "none" or prot == "check":
            k = rng.poisson(ber * nbits)
            words = flip(words, nb, rng.integers(0, nbits, k))
        elif prot == "ecc":
            # SEC-DED Hamming code on 64-bit data words (72-bit codewords). Words with one flip are corrected;
            # words with two or more flips keep their data-bit errors (worst case: no reload, no scrubbing).
            nword = nbits // 64
            k = rng.poisson(ber * nword * 72)
            pos = rng.integers(0, nword * 72, k)
            w64, b72 = pos // 72, pos % 72
            uw, cnt = np.unique(w64, return_counts=True)
            bad = set(uw[cnt >= 2].tolist())
            keep = [w * 64 + b for w, b in zip(w64, b72) if w in bad and b < 64]
            words = flip(words, nb, keep)
        elif prot == "tmr":
            # three copies, bitwise majority vote: a bit is wrong only if flipped in two or three copies
            k = rng.poisson(ber * 3 * nbits)
            pos = rng.integers(0, 3 * nbits, k)
            copy, bit = pos // nbits, pos % nbits
            pairs = np.unique(np.stack([copy, bit]), axis=1)
            ub, cnt = np.unique(pairs[1], return_counts=True)
            words = flip(words, nb, ub[cnt >= 2])
        return mlp_acc(P, Xte, yte, decode(words, fmt, check=(prot == "check")))

    bers = np.logspace(-6, -1.5, 19)
    configs = [("f32", "none"), ("f32", "check"), ("i8", "none"), ("f32", "ecc"), ("i8", "ecc"), ("f32", "tmr")]
    res = {}
    rng = np.random.default_rng(7)
    ntr = 40
    for cfg in configs:
        arr = np.zeros((len(bers), ntr))
        for i, ber in enumerate(bers):
            for t in range(ntr):
                arr[i, t] = run(*cfg, ber, rng)
        res[cfg] = arr

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.25), sharey=True)
    style = {("f32", "none"): (RED, "float32, unprotected"), ("f32", "check"): (ORANGE, "float32 + range check"),
             ("i8", "none"): (BLUE, "int8, unprotected"), ("f32", "ecc"): (VIOLET, "float32 + SEC-DED ECC"),
             ("i8", "ecc"): (GREEN, "int8 + SEC-DED ECC"), ("f32", "tmr"): (NAVY, "float32 + TMR")}
    for ax, group in zip(axs, [configs[:3], configs[3:]]):
        if group[0] == ("f32", "ecc"):
            med = np.median(res[("f32", "none")], axis=1)
            ax.plot(bers, 100 * med, color=GREY, lw=1.0, ls="--", label="float32, unprotected (median)")
        for cfg in group:
            col, lab = style[cfg]
            arr = 100 * res[cfg]
            ax.fill_between(bers, np.percentile(arr, 10, axis=1), np.percentile(arr, 90, axis=1), color=col,
                            alpha=0.14, lw=0)
            ax.plot(bers, np.median(arr, axis=1), color=col, lw=1.7, label=lab)
        ax.set_xscale("log")
        ax.set_xlabel("Fraction of stored weight bits flipped")
        ax.set_ylim(0, 100)
        ax.legend(loc="lower left", fontsize=6.6, handlelength=1.6)
        sec = ax.secondary_xaxis("top", functions=(lambda b: b / 7.6e-7, lambda d: d * 7.6e-7))
        sec.set_xlabel("Days in LEO without scrubbing (SRAM rate)", fontsize=7)
        sec.tick_params(labelsize=7)
    axs[0].set_ylabel("Test accuracy (%)")
    axs[0].set_title("a   Unprotected memory", fontsize=8.6, loc="left", pad=22)
    axs[1].set_title("b   Error-correcting code and triple redundancy", fontsize=8.6, loc="left", pad=22)
    foot(fig, "Numpy network 8-64-64-6 (4 992 weights) trained on 20 000 synthetic 8-band pixels of six classes; "
         "2 000 test pixels; 40 random trials per point (line: median; band: 10th-90th percentile). Flips land "
         "uniformly on all stored weight bits (biases protected). Range check: weights non-finite or > 2x the "
         "largest original weight are set to zero. ECC: SEC-DED on 64-bit words, multi-bit words left "
         "uncorrected. Top axis: 7.6e-7 upsets per bit per day, measured in SRAM on LEO satellites.", width=170)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    save(fig, "ch45_bitflips")
    for cfg in configs:
        med = np.median(res[cfg], axis=1)
        p10 = np.percentile(res[cfg], 10, axis=1)
        idx = [np.argmin(np.abs(bers - b)) for b in (1e-5, 1e-4, 1e-3, 1e-2)]
        print("bitflips", cfg, "BER", [f"{bers[i]:.1e}" for i in idx], "median",
              [f"{100 * med[i]:.1f}" for i in idx], "p10", [f"{100 * p10[i]:.1f}" for i in idx])
    nb32 = flat32.size * 32
    print(f"bitflips: float32 weight bits {nb32}, int8 bits {q8.size * 8}; upsets/day at 7.6e-7: "
          f"{nb32 * 7.6e-7:.3f} (f32), {q8.size * 8 * 7.6e-7:.3f} (i8)")


def unflat(flat, shapes, sizes, scales):
    out, k = [], 0
    for i, (sh, sz) in enumerate(zip(shapes, sizes)):
        W = flat[k:k + sz].reshape(sh)
        out.append(W * scales[i] if scales is not None else W)
        k += sz
    return out


# ==============================================================================================
def compress():
    """Post-training quantisation, quantisation-aware training and magnitude pruning of the reference net."""
    net = trained_net()
    P, Xtr, ytr, Xte, yte = net["P"], net["Xtr"], net["ytr"], net["Xte"], net["yte"]
    P64 = [[W.astype(np.float64), b.astype(np.float64)] for W, b in P]
    base = mlp_acc(P64, Xte, yte)
    bits = [8, 6, 4, 3, 2]
    ptq, ptqc, qat = [], [], []
    for b in bits:
        ptq.append(mlp_acc(P64, Xte, yte, [quantise(W, b) for W, _ in P64]))
        ptqc.append(mlp_acc(P64, Xte, yte, [quantise(W, b, True) for W, _ in P64]))
        Pq = [[W.copy(), bb.copy()] for W, bb in P64]
        Pq = mlp_train(Pq, Xtr, ytr, epochs=12, lr=1e-3, seed=10 + b, wq=lambda W, b=b: quantise(W, b, True))
        qat.append(mlp_acc(Pq, Xte, yte, [quantise(W, b, True) for W, _ in Pq]))
    nW = sum(W.size for W, _ in P)
    nb = sum(b.size for _, b in P)
    nch = sum(W.shape[1] for W, _ in P)
    size_f32 = (nW + nb) * 4 / 1024
    sizes = [(nW * b / 8 + nb * 4 + nch * 4) / 1024 for b in bits]
    print(f"compress: float32 {100 * base:.2f} %, size {size_f32:.2f} kB")
    for b, a1, a2, a3, s in zip(bits, ptq, ptqc, qat, sizes):
        print(f"  {b} bit: PTQ per-tensor {100 * a1:.2f}  PTQ per-channel {100 * a2:.2f}  QAT {100 * a3:.2f}  "
              f"size {s:.2f} kB ({size_f32 / s:.1f}x smaller)")
    # magnitude pruning (global threshold on weights), with and without fine-tuning
    spars = [0, 0.5, 0.7, 0.8, 0.9, 0.95, 0.98]
    allw = np.concatenate([np.abs(W).ravel() for W, _ in P64])
    pr0, pr1 = [], []
    for s in spars:
        thr = np.quantile(allw, s) if s > 0 else -1
        masks = [(np.abs(W) > thr).astype(float) for W, _ in P64]
        pr0.append(mlp_acc(P64, Xte, yte, [W * mk for (W, _), mk in zip(P64, masks)]))
        Pp = [[W * mk, bb.copy()] for (W, bb), mk in zip(P64, masks)]
        if s > 0:
            Pp = mlp_train(Pp, Xtr, ytr, epochs=10, lr=1e-3, seed=30, masks=masks)
        pr1.append(mlp_acc(Pp, Xte, yte, [W * mk for (W, _), mk in zip(Pp, masks)]))
    for s, a0, a1 in zip(spars, pr0, pr1):
        print(f"  prune {s:.2f}: no fine-tune {100 * a0:.2f}  fine-tuned {100 * a1:.2f}")

    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.7), gridspec_kw=dict(width_ratios=[1.15, 0.9, 1.15]))
    ax = axs[0]
    xs = np.arange(len(bits) + 1)
    lab = ["32\n(float)"] + [str(b) for b in bits]
    ax.plot(xs, 100 * np.r_[base, ptq], "o-", color=RED, ms=4, label="PTQ, one scale per tensor")
    ax.plot(xs, 100 * np.r_[base, ptqc], "s-", color=ORANGE, ms=4, label="PTQ, one scale per neuron")
    ax.plot(xs, 100 * np.r_[base, qat], "D-", color=GREEN, ms=4, label="Quantisation-aware training")
    ax.set_xticks(xs)
    ax.set_xticklabels(lab, fontsize=7)
    ax.set_xlabel("Bits per weight")
    ax.set_ylabel("Test accuracy (%)")
    lo = min(100 * min(ptq), 100 * min(pr0))
    ax.set_ylim(max(0, lo - 5), 100)
    ax.legend(fontsize=6.3, loc="lower left")
    ax.set_title("a   Quantisation", fontsize=8.6, loc="left")
    ax = axs[1]
    vals = [size_f32] + sizes
    cols = [GREY] + [BLUE] * len(bits)
    ax.bar(np.arange(len(vals)), vals, color=cols, width=0.65)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.4, f"{v:.1f}", ha="center", fontsize=6.4)
    ax.set_xticks(np.arange(len(vals)))
    ax.set_xticklabels(["32"] + [str(b) for b in bits], fontsize=7)
    ax.set_xlabel("Bits per weight")
    ax.set_ylabel("Model size (kB)")
    ax.set_ylim(0, size_f32 * 1.18)
    ax.set_title("b   Memory", fontsize=8.6, loc="left")
    ax = axs[2]
    ax.plot(100 * np.array(spars), 100 * np.array(pr0), "o-", color=RED, ms=4, label="pruned, no retraining")
    ax.plot(100 * np.array(spars), 100 * np.array(pr1), "D-", color=GREEN, ms=4, label="pruned + fine-tuned")
    ax.set_xlabel("Weights removed (%)")
    ax.set_ylabel("Test accuracy (%)")
    ax.set_ylim(max(0, lo - 5), 100)
    ax.legend(fontsize=6.3, loc="lower left")
    ax.set_title("c   Magnitude pruning", fontsize=8.6, loc="left")
    foot(fig, "Same network and data as the bit-flip figure (5 126 parameters). Weights quantised symmetrically, "
         "biases and activations kept in 32-bit floating point. QAT: 12 epochs of fine-tuning with quantised "
         "weights in the forward pass (straight-through estimator). Pruning: global magnitude threshold, then "
         "10 epochs of fine-tuning with the mask fixed. Sizes include biases and one scale per neuron.", width=165)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    save(fig, "ch45_compress")



# ==============================================================================================
def labels():
    """(a) Active learning by margin sampling versus random sampling; (b) random versus systematic label noise."""
    from sklearn.ensemble import RandomForestClassifier
    rng = np.random.default_rng(11)
    Xpool, ypool = pixels(12000, rng)
    Xte, yte = pixels(5000, rng)
    step, nmax, reps = 30, 600, 4
    res = {"random": [], "margin": []}
    for r in range(reps):
        for strat in res:
            rr = np.random.default_rng(100 + r)
            lab = np.concatenate([rr.choice(np.where(ypool == c)[0], 5, replace=False) for c in range(6)])
            accs, ns = [], []
            while True:
                clf = RandomForestClassifier(50, random_state=r, n_jobs=1).fit(Xpool[lab], ypool[lab])
                accs.append(clf.score(Xte, yte))
                ns.append(len(lab))
                if len(lab) >= nmax:
                    break
                unl = np.setdiff1d(np.arange(len(Xpool)), lab)
                if strat == "random":
                    new = rr.choice(unl, step, replace=False)
                else:
                    sub = rr.choice(unl, 3000, replace=False)
                    ps = np.sort(clf.predict_proba(Xpool[sub]), axis=1)
                    new = sub[np.argsort(ps[:, -1] - ps[:, -2])[:step]]
                lab = np.concatenate([lab, new])
            res[strat].append(accs)
    ns = np.array(ns)
    full = RandomForestClassifier(100, random_state=0, n_jobs=1).fit(Xpool, ypool).score(Xte, yte)
    rnd, mar = np.array(res["random"]), np.array(res["margin"])
    print(f"labels: RF on all 12 000 pool labels {100 * full:.1f} %")
    for k in (0, 3, 6, 9, 13, 19):
        print(f"  n={ns[k]}: random {100 * rnd[:, k].mean():.1f}  margin {100 * mar[:, k].mean():.1f}")
    # random labels needed to match margin sampling at 210 labels
    target = mar[:, ns.tolist().index(210)].mean()
    above = np.where(rnd.mean(axis=0) >= target)[0]
    print("  margin@210 =", f"{100 * target:.1f}", "random reaches it at n =", ns[above[0]] if len(above) else ">600")
    # weak labels
    Xtr, ytr = pixels(4000, np.random.default_rng(12))
    noise = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    out = {k: np.zeros((len(noise), 2)) for k in ("random", "omission")}
    U, S = CLASSES.index("Urban"), CLASSES.index("Soil")
    for kind in out:
        for i, p in enumerate(noise):
            accs = []
            for r in range(3):
                rr = np.random.default_rng(200 + r)
                yn = ytr.copy()
                if kind == "random":
                    m = rr.random(len(yn)) < p
                    yn[m] = (yn[m] + rr.integers(1, 6, m.sum())) % 6
                else:
                    m = (ytr == U) & (rr.random(len(yn)) < p)
                    yn[m] = S
                clf = RandomForestClassifier(100, random_state=r, n_jobs=1, min_samples_leaf=3).fit(Xtr, yn)
                pr = clf.predict(Xte)
                accs.append([np.mean(pr == yte), np.mean(pr[yte == U] == U)])
            out[kind][i] = np.mean(accs, axis=0)
    for kind in out:
        print("  weak", kind, "acc", np.round(100 * out[kind][:, 0], 1), "urban recall",
              np.round(100 * out[kind][:, 1], 1))

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.9))
    ax = axs[0]
    for arr, col, lab in [(rnd, GREY, "random sampling"), (mar, BLUE, "active learning (margin sampling)")]:
        mu = 100 * arr.mean(axis=0)
        sd = 100 * arr.std(axis=0)
        ax.fill_between(ns, mu - sd, mu + sd, color=col, alpha=0.15, lw=0)
        ax.plot(ns, mu, color=col, lw=1.7, label=lab)
    ax.axhline(100 * full, color=GREEN, ls="--", lw=1.0)
    ax.text(nmax, 100 * full + 0.4, f"all 12 000 labels: {100 * full:.1f} %", ha="right", va="bottom", fontsize=6.4,
            color=GREEN)
    ax.set_xlabel("Labelled pixels")
    ax.set_ylabel("Test accuracy (%)")
    ax.set_xlim(0, nmax)
    ax.set_ylim(70, 96)
    ax.legend(loc="lower right", fontsize=6.6)
    ax.set_title("a   Choosing which pixels to label", fontsize=8.6, loc="left")
    ax = axs[1]
    for kind, col, lab in [("random", BLUE, "random label errors"), ("omission", ORANGE,
                                                                      "urban mislabelled as soil (map gap)")]:
        ax.plot(100 * noise, 100 * out[kind][:, 0], "o-", color=col, ms=3.5, lw=1.5, label=f"{lab}: accuracy")
        ax.plot(100 * noise, 100 * out[kind][:, 1], "s--", color=col, ms=3.5, lw=1.2,
                label=f"{lab}: urban recall")
    ax.set_xlabel("Training labels affected (%)")
    ax.set_ylabel("Score on clean test labels (%)")
    ax.set_ylim(0, 100)
    ax.legend(loc="lower left", fontsize=6.0)
    ax.set_title("b   Weak labels: random versus systematic errors", fontsize=8.6, loc="left")
    foot(fig, "Random forests on synthetic 8-band pixels of six classes (water, vegetation, soil, urban, snow, cloud). "
         "(a) Pool of 12 000 unlabelled pixels, 5 000 test pixels; start with 5 labels per class, add 30 per round; "
         "margin sampling labels the pixels whose two most likely classes are closest; mean and +/-1 s.d. of 4 runs. "
         "(b) 4 000 training pixels; 'random' replaces a label by another class at random; 'map gap' relabels urban "
         "pixels as soil, as when buildings are missing from a reference map; mean of 3 runs.", width=165)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.92, bottom=0.3, wspace=0.28)
    save(fig, "ch45_labels")


# ==============================================================================================
def _smooth_noise(rng, n, size, scale):
    from scipy.ndimage import gaussian_filter
    z = rng.normal(size=(n, size, size))
    return np.stack([gaussian_filter(a, scale) for a in z]) * scale


def render(theta, sun, rng, size=20, bg=None, noise=None, blur=None, gain=None):
    """Toy renderer: a T-shaped spacecraft (body, solar panel, offset antenna) seen from above.
    Panel and body brightness depend on the Sun direction relative to the spacecraft axis; a glint
    appears on the panel when the Sun is nearly aligned."""
    from scipy.ndimage import gaussian_filter
    n = len(theta)
    g = (np.arange(size * 2) + 0.5) / 2 - size / 2          # 2x supersampling
    yy, xx = np.meshgrid(g, g, indexing="ij")
    c, s = np.cos(theta)[:, None, None], np.sin(theta)[:, None, None]
    u = c * xx + s * yy
    v = -s * xx + c * yy
    body = (np.abs(u) < 3.0) & (np.abs(v) < 2.2)
    panel = (np.abs(u) < 8.0) & (np.abs(v - 3.7) < 1.0)
    ant = (np.abs(u - 2.0) < 0.8) & (v < -2.2) & (v > -5.5)
    rel = (sun - theta)[:, None, None]
    pb = 0.25 + 0.55 * np.clip(np.cos(rel), 0, None) + 0.6 * np.exp(-(np.angle(np.exp(1j * rel)) ** 2) / 0.03)
    bb = 0.35 + 0.45 * np.clip(np.cos(rel - np.pi / 2), 0, None)
    ab = 0.3 + 0.5 * np.clip(np.cos(rel + np.pi / 2), 0, None)
    img = np.where(panel, pb, 0.0) + np.where(body & ~panel, bb, 0.0) + np.where(ant & ~body & ~panel, ab, 0.0)
    img = img.reshape(n, size, 2, size, 2).mean(axis=(2, 4))
    obj = img > 0
    if bg is not None:
        img = np.where(img > 0.02, img, 0) + bg * (img <= 0.02) + bg * 0.15 * (img > 0.02)
    if blur is not None:
        img = np.stack([gaussian_filter(a, b) if b > 0.05 else a for a, b in zip(img, blur)])
    if gain is not None:
        img = img * gain[:, None, None]
    if noise is not None:
        img = img + rng.normal(size=img.shape) * noise[:, None, None]
    return img, obj


def earth_bg(rng, n, size, strength):
    """'Real' backgrounds: a bright Earth limb crossing the image with cloud texture."""
    ang = rng.uniform(0, 2 * np.pi, n)
    off = rng.uniform(-6, 6, n)
    g = np.arange(size) + 0.5 - size / 2
    yy, xx = np.meshgrid(g, g, indexing="ij")
    d = np.cos(ang)[:, None, None] * xx + np.sin(ang)[:, None, None] * yy - off[:, None, None]
    limb = 1 / (1 + np.exp(-d / 0.8))
    tex = 0.5 + 0.5 * np.tanh(_smooth_noise(rng, n, size, 1.5) * 3)
    return strength[:, None, None] * limb * (0.45 + 0.55 * tex)


def random_bg(rng, n, size):
    """Domain-randomisation backgrounds: random level, random linear gradient and random blobs."""
    g = np.arange(size) + 0.5 - size / 2
    yy, xx = np.meshgrid(g, g, indexing="ij")
    a = rng.uniform(0, 2 * np.pi, n)
    grad = (np.cos(a)[:, None, None] * xx + np.sin(a)[:, None, None] * yy) / size + 0.5
    lev = rng.uniform(0, 0.6, n)[:, None, None]
    blobs = np.clip(_smooth_noise(rng, n, size, 2.5) * 2.5, 0, None)
    return np.clip(lev * grad + rng.uniform(0, 0.4, n)[:, None, None] * blobs, 0, 1)


def make_set(kind, n, rng, sev=1.0):
    k = rng.integers(0, 8, n)
    theta = k * np.pi / 4 + rng.uniform(-0.2, 0.2, n)
    if kind == "synthetic":
        img, _ = render(theta, np.zeros(n), rng)
    elif kind == "randomised":
        img, _ = render(theta, rng.uniform(0, 2 * np.pi, n), rng, bg=random_bg(rng, n, 20),
                        noise=rng.uniform(0, 0.12, n), blur=rng.uniform(0, 1.3, n), gain=rng.uniform(0.6, 1.4, n))
    else:   # 'real': lighting, Earth background, blur, gain error and noise, all scaled by severity
        sun = rng.uniform(-np.pi, np.pi, n) * sev
        img, _ = render(theta, sun, rng, bg=earth_bg(rng, n, 20, np.full(n, 0.7 * sev)),
                        noise=np.full(n, 0.08 * sev), blur=np.full(n, 1.0 * sev),
                        gain=1 + 0.3 * sev * rng.choice([-1, 1], n))
    return img.reshape(n, -1), k, img


def simreal():
    """Sim-to-real gap: a numpy network trained on clean renders versus on domain-randomised renders."""
    rng = np.random.default_rng(21)
    Xa, ya, _ = make_set("synthetic", 8000, rng)
    Xb, yb, _ = make_set("randomised", 8000, rng)
    nets = {}
    for name, X, y in [("synthetic", Xa, ya), ("randomised", Xb, yb)]:
        P = mlp_init([400, 96, 8], np.random.default_rng(3))
        nets[name] = mlp_train(P, X, y, epochs=25, lr=1e-3, seed=4)
    sevs = np.linspace(0, 1, 9)
    acc = {k: [] for k in nets}
    for sv in sevs:
        Xr, yr, _ = make_set("real", 3000, np.random.default_rng(int(1000 * sv) + 5), sev=sv)
        for k in nets:
            acc[k].append(mlp_acc(nets[k], Xr, yr))
    Xv, yv, _ = make_set("synthetic", 3000, np.random.default_rng(6))
    print("simreal: on clean synthetic test", {k: round(100 * mlp_acc(nets[k], Xv, yv), 1) for k in nets})
    for k in nets:
        print("  real-domain accuracy vs severity", k, np.round(100 * np.array(acc[k]), 1))

    fig = plt.figure(figsize=(7.0, 3.1))
    gs = fig.add_gridspec(3, 7, width_ratios=[1, 1, 1, 1, 0.62, 2.6, 0.02], wspace=0.08, hspace=0.12,
                          left=0.115, right=0.985, top=0.9, bottom=0.3)
    rr = np.random.default_rng(8)
    rows = [("synthetic", "Synthetic\n(training A)"), ("randomised", "Randomised\n(training B)"),
            ("real", "'Real'\n(test, severity 1)")]
    for i, (kind, lab) in enumerate(rows):
        _, _, imgs = make_set(kind, 4, np.random.default_rng(30 + i), sev=1.0)
        for j in range(4):
            ax = fig.add_subplot(gs[i, j])
            ax.imshow(np.clip(imgs[j], 0, 1.2), cmap="gray", vmin=0, vmax=1.1)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
            for sp in ax.spines.values():
                sp.set_visible(True)
                sp.set_color("#B0B8C0")
            if j == 0:
                ax.set_ylabel(lab, fontsize=6.4, rotation=0, ha="right", va="center", labelpad=4)
    fig.text(0.28, 0.93, "a   Training and test images", fontsize=8.6, weight="bold", ha="center")
    ax = fig.add_subplot(gs[:, 5])
    ax.plot(sevs, 100 * np.array(acc["synthetic"]), "o-", color=RED, ms=3.5, label="A: trained on clean renders")
    ax.plot(sevs, 100 * np.array(acc["randomised"]), "D-", color=GREEN, ms=3.5,
            label="B: trained with domain randomisation")
    ax.set_xlabel("Severity of the domain shift", fontsize=7.8)
    ax.set_ylabel("Accuracy on 'real' images (%)", fontsize=7.8)
    ax.set_ylim(0, 105)
    ax.legend(loc="lower left", fontsize=6.6, frameon=True, facecolor="white", edgecolor="none", framealpha=1)
    ax.set_title("b   The sim-to-real gap", fontsize=8.6, loc="left")
    foot(fig, "Toy renderer: 20 x 20-pixel images of a T-shaped spacecraft in 8 orientation classes (45 deg apart, "
         "+/-11 deg jitter). Numpy network 400-96-8 trained on 8 000 images per set. A: Sun fixed, black sky, no "
         "noise. B: random Sun angle, random gradient and blob backgrounds, blur, gain and noise. 'Real' test images "
         "(3 000 per point): Sun angle spread, textured Earth-limb background, blur, gain error and noise all "
         "grow with severity (0 = identical to A).", width=160)
    save(fig, "ch45_simreal")


# ==============================================================================================
def psi(ref, cur, bins=10):
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    p = np.histogram(ref, edges)[0] / len(ref) + 1e-4
    q = np.histogram(cur, edges)[0] / len(cur) + 1e-4
    return float(np.sum((q - p) * np.log(q / p)))


def drift():
    """Monitoring a deployed classifier for drift: detector degradation and a processing change."""
    from sklearn.ensemble import RandomForestClassifier
    months = np.arange(0, 49)
    deg = np.array([0.006, 0.005, 0.004, 0.003, 0.002, 0.002, 0.001, 0.001])   # gain loss per month by band

    def gain(t):
        g = 1 - deg * t
        if t >= 33:                                 # ground-processing change: SWIR calibration +20 %
            g = g * np.r_[np.ones(6), 1.2, 1.2]
        return g

    rng = np.random.default_rng(31)
    X0, y0 = pixels(4000, rng)
    model0 = RandomForestClassifier(80, random_state=0, n_jobs=1).fit(X0, y0)
    thr = 0.1
    acc_static, acc_ret, psis, alarms = [], [], [], []
    model, ref = model0, X0
    for t in months:
        Xt, yt = pixels(3000, np.random.default_rng(500 + t), gain=gain(t))
        acc_static.append(model0.score(Xt, yt))
        acc_ret.append(model.score(Xt, yt))
        val = max(psi(ref[:, b], Xt[:, b]) for b in range(8))
        psis.append(val)
        if val > thr:
            alarms.append(t)
            Xn, yn = pixels(2000, np.random.default_rng(900 + t), gain=gain(t))   # newly labelled data
            model = RandomForestClassifier(80, random_state=t, n_jobs=1).fit(Xn, yn)
            ref = Xn
    acc_static, acc_ret = np.array(acc_static), np.array(acc_ret)
    print("drift: alarms at months", alarms)
    for t in (0, 12, 24, 30, 32, 33, 36, 48):
        print(f"  month {t}: static {100 * acc_static[t]:.1f}  with retraining {100 * acc_ret[t]:.1f}  "
              f"PSI {psis[t]:.3f}")

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.75))
    ax = axs[0]
    ax.plot(months, 100 * acc_static, color=RED, lw=1.6, label="model never retrained")
    ax.plot(months, 100 * acc_ret, color=GREEN, lw=1.6, label="retrained when drift alarm fires")
    for a in alarms:
        ax.axvline(a, color=GREEN, lw=0.6, ls=":")
    ax.axvline(33, color=GREY, lw=0.8, ls="--")
    ax.text(33.6, 66, "processing\nchange", fontsize=6.2, color=GREY, va="bottom")
    ax.set_xlabel("Months in orbit")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(50, 100)
    ax.legend(loc="lower left", fontsize=6.6)
    ax.set_title("a   Accuracy of a deployed classifier", fontsize=8.6, loc="left")
    ax = axs[1]
    ax.plot(months, psis, color=BLUE, lw=1.5)
    ax.axhline(thr, color=ORANGE, ls="--", lw=1.0)
    ax.text(48, thr * 1.08, f"alarm threshold PSI = {thr}", fontsize=6.4, color=ORANGE, ha="right")
    ax.plot(alarms, [psis[a] for a in alarms], "v", color=GREEN, ms=6, label="alarm: label new data, retrain")
    ax.set_xlabel("Months in orbit")
    ax.set_ylabel("Largest population stability index")
    ax.set_yscale("log")
    ax.legend(loc="lower right", fontsize=6.6)
    ax.set_title("b   Monitoring the input distribution", fontsize=8.6, loc="left")
    foot(fig, "Random forest (80 trees) trained on 4 000 synthetic 8-band pixels at launch; each month 3 000 new "
         "pixels are classified. The detector loses 0.1-0.6 % of its gain per month (fastest in the blue band); at "
         "month 33 a processing change raises the two short-wave infrared bands by 20 %. PSI: population "
         "stability index of each band against the training data (10 quantile bins); after an alarm the model is "
         "retrained on 2 000 newly labelled pixels, which become the new reference.", width=160)
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    save(fig, "ch45_drift")


# ==============================================================================================
def fedlearn():
    """(a) Federated learning across a constellation; (b) FedAvg versus local-only and centralised training."""
    K, nk, rounds = 10, 600, 40
    rng = np.random.default_rng(41)
    props = rng.dirichlet(np.full(6, 0.3), K)
    data = [pixels(nk, np.random.default_rng(60 + k), probs=props[k]) for k in range(K)]
    Xte, yte = pixels(6000, np.random.default_rng(99))
    Xall = np.concatenate([d[0] for d in data])
    mu, sd = Xall.mean(axis=0), Xall.std(axis=0)
    data = [((X - mu) / sd, y) for X, y in data]
    Xte = (Xte - mu) / sd
    Xc = np.concatenate([d[0] for d in data])
    yc = np.concatenate([d[1] for d in data])
    sizes = [8, 32, 6]
    Pc = mlp_train(mlp_init(sizes, np.random.default_rng(1)), Xc, yc, epochs=60, lr=3e-3, seed=2)
    central = mlp_acc(Pc, Xte, yte)
    local = [mlp_acc(mlp_train(mlp_init(sizes, np.random.default_rng(1)), X, y, epochs=60, lr=3e-3, seed=3),
                     Xte, yte) for X, y in data]
    G = mlp_init(sizes, np.random.default_rng(1))
    fed = []
    for r in range(rounds):
        news = []
        for k, (X, y) in enumerate(data):
            Pk = [[W.copy(), b.copy()] for W, b in G]
            news.append(mlp_train(Pk, X, y, epochs=2, lr=3e-3, seed=1000 * r + k))
        w = np.array([len(d[1]) for d in data], float)
        w /= w.sum()
        G = [[sum(wk * Pk[i][0] for wk, Pk in zip(w, news)), sum(wk * Pk[i][1] for wk, Pk in zip(w, news))]
             for i in range(len(G))]
        fed.append(mlp_acc(G, Xte, yte))
    nparam = sum(W.size + b.size for W, b in G)
    print(f"fedlearn: centralised {100 * central:.1f} %, local-only mean {100 * np.mean(local):.1f} % "
          f"(range {100 * min(local):.1f}-{100 * max(local):.1f}), FedAvg after 5/10/20/40 rounds "
          f"{100 * fed[4]:.1f}/{100 * fed[9]:.1f}/{100 * fed[19]:.1f}/{100 * fed[-1]:.1f} %; params {nparam}")
    print("  class proportions per satellite (rounded):", np.round(props, 2).tolist()[:3])

    fig = plt.figure(figsize=(7.0, 3.1))
    ax = fig.add_axes([0.0, 0.13, 0.54, 0.85])
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 44)
    ax.set_aspect("equal")
    ax.axis("off")
    pts = [(6, 26), (18, 31), (30, 33), (42, 31), (54, 26)]
    box(ax, 19, 9.5, 22, 6.5, text="Ground station or lead satellite:\naverage the updates", fs=6.0, fc="white",
        ec=NAVY, r=0.6, z=4)
    for i, (x, y) in enumerate(pts):
        satellite(ax, x, y, s=1.1)
        ax.text(x, y + 2.6, f"satellite {i + 1}", fontsize=5.9, ha="center", va="bottom", color=INK)
        ax.text(x, y - 2.8, "trains on\nits own images", fontsize=5.3, ha="center", va="top", color=GREY,
                linespacing=1.0)
        tx = 30 + (x - 30) * 0.32
        arrow(ax, (x + (30 - x) * 0.08, y - 6.6), (tx, 16.3), color=ORANGE, lw=0.9, ms=7, z=3)
    for x, y in (pts[0], pts[4]):
        arrow(ax, (30 + (x - 30) * 0.42, 14.0), (x, y - 7.2), color=VIOLET, lw=0.9, ms=7, ls="--",
              rad=0.25 if x > 30 else -0.25, z=3)
    ax.plot([4, 8], [3.0, 3.0], color=ORANGE, lw=1.2)
    ax.text(9, 3.0, "model updates (MB)", fontsize=6.1, color=ORANGE, va="center")
    ax.plot([33, 37], [3.0, 3.0], color=VIOLET, lw=1.2, ls="--")
    ax.text(38, 3.0, "new global model (MB)", fontsize=6.1, color=VIOLET, va="center")
    ax.text(30, 7.0, "Raw images (GB to TB per day) stay on board; only weights travel.", fontsize=6.3,
            ha="center", color=NAVY)
    ax.text(1, 43.5, "a   Federated learning", fontsize=8.6, weight="bold", va="top")
    ax2 = fig.add_axes([0.6, 0.27, 0.38, 0.62])
    ax2.plot(np.arange(1, rounds + 1), 100 * np.array(fed), "o-", color=BLUE, ms=3, lw=1.5, label="FedAvg")
    ax2.axhline(100 * central, color=GREEN, ls="--", lw=1.1, label="all data pooled on the ground")
    ax2.axhline(100 * np.mean(local), color=RED, ls=":", lw=1.3, label="each satellite alone (mean)")
    ax2.set_xlabel("Communication rounds")
    ax2.set_ylabel("Test accuracy (%)")
    ax2.set_ylim(0, 100)
    ax2.legend(loc="lower right", fontsize=6.4)
    ax2.set_title("b   Ten satellites, different regions", fontsize=8.6, loc="left")
    foot(fig, "(b) Numpy network 8-32-6 on synthetic 8-band pixels. Each of 10 satellites holds 600 pixels with "
         "its own class mix (Dirichlet, alpha = 0.3: one may see mostly ocean, another desert). Each round every "
         "satellite trains 2 epochs from the global model; updates are averaged by sample count. Test: 6 000 pixels "
         "with all classes equally likely.", width=150)
    save(fig, "ch45_fedlearn")



# ==============================================================================================
def volumes():
    """Data volumes: archives and AI training sets (a), daily flows (b). Values from the chapter's sources."""
    arch = [("NASA EOSDIS archive (Sep 2025)", 178_700, NAVY),
            ("NISAR products over 3 years (planned)", 140_000, SKY),
            ("Copernicus Data Space, online (end 2025)", 91_000, NAVY),
            ("Google Earth Engine catalogue (2026)", 90_000, NAVY),
            ("Rubin LSST raw images, 10 years (planned)", 60_000, SKY),
            ("Major TOM Core-S2L2A training set (2024)", 23, ORANGE),
            ("fMoW multispectral benchmark (2018)", 3.5, ORANGE),
            ("ESA-ADB telemetry benchmark (2024)", 0.00732, ORANGE)]
    flow = [("Copernicus downloads (2025 mean)", 129_900 / 365, NAVY),
            ("EOSDIS archive growth", 160, NAVY),
            ("NISAR data products", 85, NAVY),
            ("Rubin images (per night)", 20, NAVY),
            ("TBIRD laser, one 5-min pass", 4.8, VIOLET),
            ("NISAR radar downlink (required)", 26 / 8, VIOLET),
            ("Sentinel-2, one satellite", 1.5, VIOLET)]
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw=dict(wspace=1.15))

    def fmt(v):
        if v >= 1000:
            return f"{v / 1000:,.0f} PB".replace(",", " ")
        if v >= 1:
            return f"{v:,.1f} TB".replace(",", " ").replace(".0 TB", " TB")
        return f"{v * 1000:.1f} GB"
    for ax, items, xl, ttl in [(axs[0], arch, "Terabytes (log scale)", "a   Archives and AI-ready data sets"),
                               (axs[1], flow, "Terabytes per day (log scale)", "b   Daily flows")]:
        y = np.arange(len(items))[::-1]
        vals = [v for _, v, _ in items]
        ax.barh(y, vals, color=[c for _, _, c in items], height=0.62)
        ax.set_xscale("log")
        ax.set_yticks(y)
        ax.set_yticklabels([n for n, _, _ in items], fontsize=6.6)
        for yy, v in zip(y, vals):
            ax.text(v * 1.25, yy, fmt(v), va="center", fontsize=6.3, color=INK)
        ax.set_xlabel(xl, fontsize=7.6)
        ax.set_xlim(min(vals) / 3, max(vals) * 8)
        ax.grid(axis="y", visible=False)
        ax.set_title(ttl, fontsize=8.6, loc="left", x=-0.75 if ax is axs[1] else -0.95)
    foot(fig, "Sources: NASA Earthdata metrics (FY2025); Copernicus Data Space Ecosystem annual report (2025 data); "
         "Google Earth Engine; NASA/JPL NISAR; Rubin Observatory; Major TOM (ESA Phi-lab); fMoW; ESA-ADB (Kotowski "
         "et al. 2024); MIT Lincoln Laboratory TBIRD; Airbus (Sentinel-2). In (b) blue bars are ground-side flows, "
         "violet bars are what a single spacecraft sends down.", width=160)
    fig.subplots_adjust(left=0.27, right=0.97, top=0.9, bottom=0.29)
    save(fig, "ch45_volumes")


# ==============================================================================================
def pipeline():
    """Block diagram of an end-to-end MLOps pipeline from satellite to model to user, and back."""
    fig, ax = canvas(7.0, 4.15, xlim=(0, 100), ylim=(0, 59))
    cols = [21, 40.5, 60, 79.5]
    w, h = 16.5, 11.0
    rows = [43.0, 24.0, 5.0]
    # space segment column
    box(ax, 0.5, 5.0, 17.0, 49.0, fc="#EEF3F8", ec=NAVY, r=1.0)
    ax.text(9.0, 52.6, "SPACE SEGMENT", fontsize=6.8, weight="bold", color=NAVY, ha="center", va="top")
    sp = [(45.0, "Sensor"), (36.0, "Calibrate, tile,\ncompress"), (25.0, "Edge model:\nscreen clouds,\ndetect events"),
          (12.0, "Onboard store\nand scheduler")]
    for yy, t in sp:
        box(ax, 2.2, yy - 3.6, 13.6, 7.2, text=t, fs=6.0, fc="white", ec=BLUE, r=0.6)
    for (y1, _), (y2, _) in zip(sp[:-1], sp[1:]):
        arrow(ax, (9.0, y1 - 3.6), (9.0, y2 + 3.6), lw=0.8, ms=6)
    txt = {(0, 0): "Ground stations\n(X, Ka, optical)", (0, 1): "Level-0/1/2\nprocessing",
           (0, 2): "Archive and\ncatalogue (versioned)", (0, 3): "Labelling: experts,\ncrowd, weak labels,\nactive learning",
           (1, 3): "Training-data\nsnapshot\n(data version ID)", (1, 2): "Training on GPUs\nor TPUs, experiment\ntracking",
           (1, 1): "Model registry\n(versions, model\ncards)", (1, 0): "Validation gates:\naccuracy by region,\nrobustness, budgets",
           (2, 0): "Uplink package:\nshadow mode,\nthen active", (2, 1): "Ground inference\nservice",
           (2, 2): "Users: products,\nalerts, decisions", (2, 3): "Monitoring: drift,\naccuracy, feedback"}
    colr = {0: "#E8F1FA", 1: "#EEF7EE", 2: "#F6F0FA"}
    for (r, c), t in txt.items():
        box(ax, cols[c], rows[r], w, h, text=t, fs=6.0, fc=colr[r], ec=NAVY, r=0.7)
    ym = [y + h / 2 for y in rows]
    for c in range(3):
        arrow(ax, (cols[c] + w, ym[0]), (cols[c + 1], ym[0]), lw=0.9, ms=7)
        arrow(ax, (cols[c + 1], ym[1]), (cols[c] + w, ym[1]), lw=0.9, ms=7)
    arrow(ax, (cols[1] + w, ym[2]), (cols[2], ym[2]), lw=0.9, ms=7)
    arrow(ax, (cols[2] + w, ym[2]), (cols[3], ym[2]), lw=0.9, ms=7)
    arrow(ax, (cols[3] + w / 2, rows[0]), (cols[3] + w / 2, rows[1] + h), lw=0.9, ms=7)
    arrow(ax, (cols[0] + w / 2, rows[1]), (cols[0] + w / 2, rows[2] + h), lw=0.9, ms=7)
    arrow(ax, (cols[0] + w * 0.8, rows[1]), (cols[1] + w * 0.25, rows[2] + h), lw=0.9, ms=7)
    # downlink and uplink
    arrow(ax, (15.8, 45.0), (cols[0], ym[0]), lw=1.4, ms=8, color=ORANGE)
    ax.text(19.3, 41.6, "down-\nlink", fontsize=5.8, color=ORANGE, ha="center", weight="bold", linespacing=1.0)
    arrow(ax, (cols[0], ym[2]), (15.8, 25.0), lw=1.2, ms=8, color=VIOLET, ls="--")
    ax.text(19.4, 22.8, "up-\nlink", fontsize=5.8, color=VIOLET, ha="center", weight="bold", linespacing=1.0)
    # retraining loop on the right edge
    xr = cols[3] + w + 2.0
    ax.plot([cols[3] + w, xr, xr], [ym[2], ym[2], ym[0]], color=GREEN, lw=1.2, solid_capstyle="round", zorder=3)
    arrow(ax, (xr, ym[0]), (cols[3] + w, ym[0]), color=GREEN, lw=1.2, ms=8)
    ax.text(xr + 1.2, ym[1], "retrain when drift is found", fontsize=6.0, color=GREEN, ha="center", va="center",
            rotation=90)
    # data scale tags
    tags = [(cols[0] + w / 2, rows[0] + h + 1.6, "TB per day"), (cols[2] + w / 2, rows[0] + h + 1.6, "PB"),
            (cols[3] + w / 2, rows[0] + h + 1.6, "GB-TB of labels"), (cols[1] + w / 2, rows[1] - 1.6, "MB-GB"),
            (cols[3] + w / 2, rows[1] - 1.6, "GB-TB")]
    for x, y, t in tags:
        ax.text(x, y, t, fontsize=5.9, color=GREY, ha="center", va="center", style="italic")
    save(fig, "ch45_pipeline")


# ==============================================================================================
# Processor data (from the chapter's processor table): name, year in space or available, peak GOPS,
# power W (None = not published), class, kind of operation
PROCS = [
    ("RAD750", 2005, 0.4, 5.0, "hard", "cpu"),
    ("GR740 (4 x LEON4)", 2022, 1.7, 3.0, "hard", "cpu"),
    ("PIC64-HPSC (CPU)", 2025, 28.1, None, "hard", "cpu"),
    ("PIC64-HPSC (int8)", 2025, 2000, None, "hard", "ai"),
    ("Myriad 2 (Phi-sat-1)", 2020, 100, 1.0, "cots", "ai"),
    ("Myriad X", 2021, 1000, None, "cots", "ai"),
    ("T4 GPU (Spaceborne\nComputer-2)", 2021, 130_000, 70.0, "cots", "ai"),
    ("Versal AI Core XQR", 2023, 133_000, 130.0, "tol", "ai"),
    ("Jetson Orin NX", 2024, 50_000, 25.0, "cots", "ai"),
    ("H100 (Starcloud-1)", 2025, 1_979_000, 700.0, "cots", "ai"),
    ("Three-Body satellite", 2025, 744_000, None, "cots", "sat"),
    ("4 x TPU v6e (Suncatcher\nprototype)", 2026, 4 * 1_836_000, None, "cots", "sat"),
]
PCOL = {"hard": NAVY, "tol": VIOLET, "cots": ORANGE}
PLAB = {"hard": "radiation-hardened by design", "tol": "radiation-tolerant (space-grade FPGA/SoC)",
        "cots": "commercial part, tested and shielded"}


def procperf():
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.8), gridspec_kw=dict(width_ratios=[1.3, 1.0]))
    ax = axs[0]
    pos = {"RAD750": (2006.0, 0.4, "left"), "GR740 (4 x LEON4)": (2021.2, 1.7, "right"),
           "PIC64-HPSC (CPU)": (2024.2, 28, "right"), "PIC64-HPSC (int8)": (2024.2, 3200, "right"),
           "Myriad 2 (Phi-sat-1)": (2019.2, 100, "right"), "Myriad X": (2020.2, 1000, "right"),
           "T4 GPU (Spaceborne\nComputer-2)": (2020.2, 1.3e5, "right"), "Versal AI Core XQR": (2023.6, 1.33e5, "left"),
           "Jetson Orin NX": (2023.2, 3.2e4, "right"), "H100 (Starcloud-1)": (2024.2, 2.6e6, "right"),
           "Three-Body satellite": (2024.2, 5.6e5, "right"),
           "4 x TPU v6e (Suncatcher\nprototype)": (2025.2, 1.3e7, "right")}
    for name, yr, gops, pw, cls, kind in PROCS:
        mk = {"cpu": "s", "ai": "o", "sat": "*"}[kind]
        ax.scatter(yr, gops, s=46 if kind != "sat" else 110, marker=mk, color=PCOL[cls], zorder=4,
                   edgecolor="white", lw=0.6)
        tx, ty, ha = pos[name]
        ax.text(tx, ty, name.replace("Versal AI Core XQR", "Versal XQR"), fontsize=5.9, ha=ha, va="center",
                color=INK, linespacing=1.0)
    ax.set_yscale("log")
    ax.set_xlim(2003, 2028)
    ax.set_ylim(0.1, 6e7)
    ax.set_xlabel("Year first flown (or available)")
    ax.set_ylabel("Peak throughput (GOPS, log scale)")
    ax.set_title("a   Peak computing power in orbit", fontsize=8.6, loc="left")
    h = [Line2D([], [], marker="o", ls="", color=PCOL[k], label=PLAB[k], ms=5) for k in ("hard", "tol", "cots")]
    h += [Line2D([], [], marker="s", ls="", color=GREY, label="CPU (DMIPS / 1 000)", ms=5),
          Line2D([], [], marker="o", ls="", color=GREY, label="AI engine (int8 or fp16 ops)", ms=5),
          Line2D([], [], marker="*", ls="", color=GREY, label="whole satellite", ms=8)]
    fig.legend(handles=h, loc="upper center", ncol=3, fontsize=6.4, handletextpad=0.3, columnspacing=1.2,
               bbox_to_anchor=(0.5, 0.995))
    ax = axs[1]
    rows = [(n, g / p, c) for n, _, g, p, c, _ in PROCS if p]
    rows.sort(key=lambda r: r[1])
    y = np.arange(len(rows))
    ax.barh(y, [r[1] for r in rows], color=[PCOL[r[2]] for r in rows], height=0.6)
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels([r[0].replace("\n", " ").replace("T4 GPU (Spaceborne Computer-2)", "T4 (Spaceborne Comp.-2)")
                        for r in rows], fontsize=6.4)
    for yy, (n, e, c) in zip(y, rows):
        ax.text(e * 1.3, yy, f"{e:,.2f}".replace(",", " ") if e < 10 else f"{e:,.0f}".replace(",", " "),
                va="center", fontsize=6.2)
    ax.set_xlim(0.03, 4e4)
    ax.set_xlabel("Peak GOPS per watt (log scale)")
    ax.grid(axis="y", visible=False)
    ax.set_title("b   Efficiency", fontsize=8.6, loc="left")
    for n, g, p, c in [(n, g, p, c) for n, _, g, p, c, _ in PROCS if p]:
        print(f"procperf: {n.replace(chr(10), ' '):38s} {g:>12,.1f} GOPS {p:>6.0f} W  {g / p:>9.2f} GOPS/W")
    foot(fig, "Vendor peak figures from the processor table: CPUs in millions of Dhrystone instructions per second "
         "(DMIPS / 1 000); AI engines in int8 operations (Myriad 2: fp16), dense, without sparsity. H100: SXM "
         "version (700 W); the variant flown was not disclosed. Versal power: about 130 W when fully used "
         "(commercial part). Parts without published power are omitted from (b). Real applications reach "
         "10-50 % of peak.", width=165)
    fig.subplots_adjust(left=0.085, right=0.985, top=0.845, bottom=0.25, wspace=0.62)
    save(fig, "ch45_procperf")


# ==============================================================================================
def downlink():
    """Data generated by pushbroom imagers versus daily downlink capacity, and an onboard-processing budget."""
    vg = 7.0e3                       # ground-track speed, m/s
    gsd = np.logspace(np.log10(0.3), 2, 200)
    duty = 0.30
    day = 86400

    def per_day(g, npx, bands, bits=12, d=duty):
        return npx * (vg / g) * bands * bits * d * day / 8 / 1e12        # TB/day

    links = [("X-band, 0.5 Gbit/s x 40 min", 0.5e9 * 2400 / 8 / 1e12, GREEN),
             ("Ka-band, 3.5 Gbit/s x 40 min", 3.5e9 * 2400 / 8 / 1e12, BLUE),
             ("Optical, 100 Gbit/s x 20 min", 100e9 * 1200 / 8 / 1e12, VIOLET)]
    s2 = (29000 * (vg / 10) * 4 + 14500 * (vg / 20) * 6 + 4833 * (vg / 60) * 3) * 12 * duty * day / 8 / 1e12
    print(f"downlink: link capacities TB/day {[round(l[1], 3) for l in links]}; Sentinel-2-like raw {s2:.2f} TB/day "
          f"-> compression ratio to 1.5 TB/day {s2 / 1.5:.1f}")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.2, 1.0]))
    ax = axs[0]
    for npx, bands, col, lab in [(40000, 8, NAVY, "40 000 pixels across, 8 bands"),
                                 (12000, 4, ORANGE, "12 000 pixels across, 4 bands")]:
        ax.plot(gsd, per_day(gsd, npx, bands), color=col, lw=1.7, label=lab)
    for name, cap, col in links:
        ax.axhline(cap, color=col, ls="--", lw=1.0)
        ax.text(0.33, cap * 1.12, name, ha="left", va="bottom", fontsize=6.0, color=col)
    ax.plot(10, 1.5, "D", color=RED, ms=5)
    ax.annotate("Sentinel-2 (one satellite,\n1.5 TB/day compressed)", (10, 1.5), xytext=(-5, -7),
                textcoords="offset points", fontsize=6.0, color=RED, va="top", ha="right")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.3, 100)
    ax.set_ylim(0.01, 300)
    ax.set_xlabel("Ground sample distance (m)")
    ax.set_ylabel("Data per day (TB, uncompressed)")
    ax.legend(loc="lower left", fontsize=6.2)
    ax.set_title("a   Imagers outrun their links", fontsize=8.6, loc="left")
    # (b) budget for a 3 m, 4-band imager with 8 000 pixels across (24 km swath)
    from scipy import stats
    raw = per_day(3.0, 8000, 4)
    d = stats.beta(0.55, 0.45)
    discard = d.sf(0.7)
    steps = [("Raw", raw), ("Lossless\ncompres-\nsion 2:1", raw / 2),
             ("Drop\nscenes >70 %\ncloudy", raw / 2 * (1 - discard)),
             ("Send only\ndetections\n(1 % pixels)", raw / 2 * (1 - discard) * 0.01)]
    ax = axs[1]
    x = np.arange(len(steps))
    ax.bar(x, [v for _, v in steps], color=[GREY, BLUE, SKY, GREEN], width=0.62)
    for i, (_, v) in enumerate(steps):
        ax.text(i, v * 1.15, f"{v * 1000:,.0f} GB".replace(",", " ") if v < 1 else f"{v:.2f} TB", ha="center",
                fontsize=6.3)
    for name, cap, col in links[:2]:
        ax.axhline(cap, color=col, ls="--", lw=1.0)
        ax.text(3.42, cap * 0.88, name.split(",")[0] + " (40 min)", ha="right", va="top", fontsize=6.0, color=col)
    ax.set_yscale("log")
    ax.set_ylim(0.005, 10)
    ax.set_xticks(x)
    ax.set_xticklabels([n for n, _ in steps], fontsize=6.0, linespacing=1.0)
    ax.set_ylabel("Data per day (TB)")
    ax.grid(axis="x", visible=False)
    ax.set_title("b   3 m imager, 24 km swath", fontsize=8.6, loc="left")
    print(f"downlink(b): raw {raw:.2f} TB/day, compressed {raw / 2:.2f}, discard fraction {discard:.3f} -> "
          f"{raw / 2 * (1 - discard):.3f} TB, detections {raw / 2 * (1 - discard) * 0.01 * 1000:.1f} GB")
    foot(fig, "Pushbroom model: data rate = pixels across track x lines per second (ground speed 7.0 km/s / GSD) x "
         "bands x 12 bits, imaging 30 % of the time. Link capacity = rate x daily contact time (assumed). "
         "Sentinel-2 check: the same model with its 10/20/60 m bands gives about 4.4 TB/day before compression. "
         "(b) Scene cloud fractions follow a U-shaped beta distribution with a mean of 55 % (land); scenes more "
         "than 70 % cloudy are discarded.", width=165)
    fig.subplots_adjust(left=0.08, right=0.985, top=0.92, bottom=0.3, wspace=0.3)
    save(fig, "ch45_downlink")


# ==============================================================================================
def radiator():
    """Radiator area needed to reject compute heat, and areas of an orbital data centre versus power."""
    sig, eps = 5.670e-8, 0.9
    T = np.linspace(250, 400, 300)

    def area_per_kw(T, sides=2, qenv=0.0):
        return 1000 / (sides * (eps * sig * T ** 4 - qenv))
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.1))
    ax = axs[0]
    for sides, qenv, col, ls, lab in [(2, 0, GREEN, "-", "two-sided, deep-space view"),
                                      (2, 100, BLUE, "-", "two-sided, LEO (100 W/m² absorbed per side)"),
                                      (1, 100, ORANGE, "-", "one-sided, LEO")]:
        ax.plot(T, area_per_kw(T, sides, qenv), color=col, ls=ls, lw=1.7, label=lab)
    ax.plot(278, 475 / 70, "D", color=RED, ms=5)
    ax.annotate("ISS radiators:\n70 kW from 475 m²", (278, 475 / 70), xytext=(6, 8), textcoords="offset points",
                fontsize=6.1, color=RED, va="bottom")
    ax.axvline(300, color=GREY, lw=0.7, ls=":")
    ax.set_yscale("log")
    ax.set_xlabel("Radiator temperature (K)")
    ax.set_ylabel("Radiator area per kW (m², log)")
    ax.set_xlim(250, 400)
    ax.set_ylim(0.25, 20)
    ax.legend(loc="lower left", fontsize=6.0)
    ax.set_title("a   Area to reject 1 kW", fontsize=8.6, loc="left")
    for t in (300, 350):
        print(f"radiator: T={t} K: q=eps*sig*T^4={eps * sig * t ** 4:.1f} W/m2; m2/kW ideal 2-sided "
              f"{area_per_kw(t):.2f}, LEO 2-sided {area_per_kw(t, 2, 100):.2f}, 1-sided {area_per_kw(t, 1, 100):.2f}")
    ax = axs[1]
    P = np.logspace(0, 6, 100)                              # kW
    solar = P * 1000 / (1361 * 0.30 * 0.85)
    rad = P * area_per_kw(300, 2, 100)
    ax.plot(P, solar, color=GOLD, lw=1.8, label="solar array (30 % cells, 85 % packing)")
    ax.plot(P, rad, color=BLUE, lw=1.8, label="radiator at 300 K (two-sided, LEO)")
    for pk, lab in [(10, "10 kW\n(one 8-GPU\nserver)"), (1000, "1 MW"), (1e6, "1 GW")]:
        ax.axvline(pk, color=GREY, lw=0.6, ls=":")
        ax.text(pk * 1.15, 3e5 if pk < 1e6 else 3e5, lab, fontsize=6.0, color=GREY, va="top",
                ha="left" if pk < 1e6 else "right")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Computing power (kW)")
    ax.set_ylabel("Area (m²)")
    ax.set_xlim(1, 1e6)
    ax.set_ylim(1, 1e7)
    ax.legend(loc="lower right", fontsize=6.0)
    ax.set_title("b   Areas of an orbital data centre", fontsize=8.6, loc="left")
    for pk in (10, 1000, 1e6):
        print(f"radiator(b): {pk:g} kW: solar {pk * 1000 / (1361 * 0.30 * 0.85):,.0f} m2, radiator "
              f"{pk * area_per_kw(300, 2, 100):,.0f} m2")
    foot(fig, "Net rejection per side = emissivity (0.9) x Stefan-Boltzmann constant x T^4 minus absorbed "
         "environmental flux; fin efficiency, temperature drop from chip to radiator and design margin are ignored, "
         "which is why the real ISS radiators need about four times the ideal area. Solar array in continuous "
         "sunlight (dawn-dusk orbit), 1 361 W/m².", width=165)
    fig.subplots_adjust(left=0.085, right=0.985, top=0.92, bottom=0.29, wspace=0.3)
    save(fig, "ch45_radiator")


if __name__ == "__main__":
    fns = [volumes, labels, simreal, pipeline, drift, bitflips, procperf, compress, downlink, fedlearn, radiator]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
