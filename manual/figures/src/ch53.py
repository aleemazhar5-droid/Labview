"""Figures for Chapter 53 - Trustworthy AI for Space: Assurance, Security, Governance and Outlook.

Computed figures use fixed random seeds and synthetic data; nothing here is flight data:
  * shift     - a small numpy neural network classifies synthetic 16 x 16 surface patches (plain, crater, boulder)
                rendered with Lambertian shading; accuracy under sensor noise and under Sun-direction shift
  * ood       - out-of-distribution detection with a Mahalanobis-distance monitor on the network's hidden features,
                compared with the maximum-softmax baseline (ROC curves)
  * ibp       - interval bound propagation (IBP) on a tiny ReLU network, compared with an exact mixed-integer
                verifier (scipy milp) and a gradient attack
  * fgsm      - fast-gradient-sign (FGSM) and iterated (PGD) attacks on the patch classifier; adversarial training
  * cagetrade - availability against residual hazard for a safety cage built from the OOD monitor
  * tests     - number of failure-free tests needed to demonstrate a failure probability (binomial statistics)
  * energy    - training energy and emissions from the 6ND compute rule with stated hardware assumptions
Diagrams: wshape (learning-assurance life cycle), cage (simplex / safety-cage architecture), gsn (assurance case),
roadmap (outlook to 2035 with confidence levels).
Numbers quoted in the chapter text are printed by each function.
"""
import os
import sys
import textwrap
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch  # noqa: F401
from matplotlib.lines import Line2D  # noqa: F401
from scipy import ndimage, stats  # noqa: F401

FOOT = 6.0
CLASSES = ["plain", "crater", "boulder"]


def panel_tag(ax, s, x=-0.02, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, weight="bold", ha="right", va="bottom", color=INK)


def foot(fig, text, y=0.01, width=150):
    fig.text(0.99, y, "\n".join(textwrap.wrap(text, width)), ha="right", va="bottom", fontsize=FOOT, color=GREY,
             multialignment="right", linespacing=1.25)


# ==============================================================================================
# Synthetic planetary surface patches, rendered from height maps with Lambertian shading
N = 16
_YY, _XX = np.mgrid[0:N, 0:N].astype(float)


def _height(kind, rng):
    """Height map (pixels) of one patch: plain, crater, boulder or (unseen) trough."""
    h = ndimage.gaussian_filter(rng.normal(0, 1.0, (N, N)), 1.6) * 0.9     # gentle rolling texture
    cx, cy = 7.5 + rng.uniform(-2, 2), 7.5 + rng.uniform(-2, 2)
    if kind == "crater":
        r = rng.uniform(3.0, 6.0)
        rho = np.hypot(_XX - cx, _YY - cy) / r
        bowl = np.where(rho < 1, -0.9 * r * (1 - rho ** 2), 0.0)
        rim = 0.25 * r * np.exp(-((rho - 1.0) / 0.25) ** 2)
        h = h + bowl + rim
    elif kind == "boulder":
        r = rng.uniform(2.0, 4.5)
        rho = np.hypot(_XX - cx, _YY - cy) / r
        h = h + 0.9 * r * np.exp(-1.5 * rho ** 2)
    elif kind == "trough":       # a linear rille: never seen in training
        th = rng.uniform(0, np.pi)
        d = (_XX - cx) * np.cos(th) + (_YY - cy) * np.sin(th)
        w = rng.uniform(1.5, 3.0)
        h = h - 2.2 * w * np.exp(-(d / w) ** 2)
    return h


def _shade(h, az_deg, el_deg, rng, noise=0.02):
    gy, gx = np.gradient(h)
    nrm = np.sqrt(gx ** 2 + gy ** 2 + 1.0)
    az, el = np.radians(az_deg), np.radians(el_deg)
    s = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    lam = (-gx * s[0] - gy * s[1] + s[2]) / nrm
    albedo = rng.uniform(0.35, 0.55)
    img = albedo * np.clip(lam, 0, None) / np.sin(el) * 0.9
    img = img * rng.uniform(0.9, 1.1)               # detector gain variation
    img = img + rng.normal(0, noise, img.shape)
    return np.clip(img, 0, 1)


def make_set(n, rng, az=(150, 210), el=(20, 45), noise=0.02, kinds=("plain", "crater", "boulder"), fault=False):
    """n images per kind. Training ODD: Sun from the west (azimuth 150-210 deg), elevation 20-45 deg."""
    X, y = [], []
    for k, kind in enumerate(kinds):
        for _ in range(n):
            h = _height(kind, rng)
            a = rng.uniform(*az) if isinstance(az, tuple) else az
            e = rng.uniform(*el)
            nz = rng.uniform(*noise) if isinstance(noise, tuple) else noise
            img = _shade(h, a, e, rng, nz)
            if fault:      # detector fault: a dead column, a bright column and hot pixels
                c1, c2 = rng.choice(N, 2, replace=False)
                img[:, c1] = 0.0
                img[:, c2] = np.clip(img[:, c2] + 0.5, 0, 1)
                hp = rng.integers(0, N, (6, 2))
                img[hp[:, 0], hp[:, 1]] = 1.0
            X.append(img.ravel())
            y.append(k)
    return np.array(X), np.array(y)


# ==============================================================================================
# Small numpy ReLU network with softmax output, trained with Adam
def net_init(sizes, rng):
    return [[rng.normal(0, np.sqrt(2.0 / a), (a, b)), np.zeros(b)] for a, b in zip(sizes[:-1], sizes[1:])]


def net_fwd(P, X):
    """Returns list of pre-activations zs and activations hs (hs[0] = X)."""
    hs, zs = [X], []
    for i, (W, b) in enumerate(P):
        z = hs[-1] @ W + b
        zs.append(z)
        hs.append(np.maximum(z, 0) if i < len(P) - 1 else z)
    return zs, hs


def softmax(z):
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def net_grads(P, X, y, need_input=False):
    zs, hs = net_fwd(P, X)
    p = softmax(hs[-1])
    n = len(y)
    d = p.copy()
    d[np.arange(n), y] -= 1
    d /= n
    grads = []
    for i in range(len(P) - 1, -1, -1):
        W, b = P[i]
        grads.append([hs[i].T @ d, d.sum(0)])
        d = d @ W.T
        if i > 0:
            d = d * (zs[i - 1] > 0)
    grads = grads[::-1]
    loss = -np.mean(np.log(p[np.arange(n), y] + 1e-12))
    return (grads, loss, d * n) if need_input else (grads, loss)


def input_grad(P, X, y):
    """Gradient of the per-sample cross-entropy loss with respect to the input."""
    return net_grads(P, X, y, need_input=True)[2]


def predict(P, X):
    return net_fwd(P, X)[1][-1].argmax(1)


def train(X, y, sizes, seed=0, epochs=30, bs=128, lr=2e-3, adv_eps=0.0, wd=1e-4):
    rng = np.random.default_rng(seed)
    P = net_init(sizes, rng)
    m = [[np.zeros_like(W), np.zeros_like(b)] for W, b in P]
    v = [[np.zeros_like(W), np.zeros_like(b)] for W, b in P]
    t = 0
    for ep in range(epochs):
        idx = rng.permutation(len(y))
        for s in range(0, len(y), bs):
            j = idx[s:s + bs]
            xb, yb = X[j], y[j]
            if adv_eps > 0:      # adversarial training: half clean, half FGSM examples
                g = input_grad(P, xb, yb)
                xa = np.clip(xb + adv_eps * np.sign(g), 0, 1)
                xb, yb = np.vstack([xb, xa]), np.concatenate([yb, yb])
            g, _ = net_grads(P, xb, yb)
            t += 1
            for i in range(len(P)):
                for k in range(2):
                    gr = g[i][k] + (wd * P[i][k] if k == 0 else 0)
                    m[i][k] = 0.9 * m[i][k] + 0.1 * gr
                    v[i][k] = 0.999 * v[i][k] + 0.001 * gr ** 2
                    mh = m[i][k] / (1 - 0.9 ** t)
                    vh = v[i][k] / (1 - 0.999 ** t)
                    P[i][k] = P[i][k] - lr * mh / (np.sqrt(vh) + 1e-8)
    return P


SIZES = [N * N, 64, 32, 3]


@lru_cache(maxsize=None)
def train_data():
    """9 000 training patches inside the design domain (Sun from the west, noise 0.02)."""
    return make_set(3000, np.random.default_rng(53), noise=0.02)


@lru_cache(maxsize=None)
def patch_model(kind="std"):
    """Train the patch classifier once per process. kind: std (plain training) or adv (FGSM adversarial training)."""
    X, y = train_data()
    return train(X, y, SIZES, seed=1, epochs=30, adv_eps=(0.03 if kind == "adv" else 0.0))


@lru_cache(maxsize=None)
def test_sets():
    rng = np.random.default_rng(530)
    out = {}
    out["id"] = make_set(600, rng)                                    # in the operational design domain
    out["sun"] = make_set(600, rng, az=(330, 390))                    # Sun from the east instead of the west
    out["fault"] = make_set(600, rng, fault=True)                     # detector fault
    Xt, _ = make_set(1800, rng, kinds=("trough",))                    # unseen terrain type
    out["trough"] = (Xt, np.full(len(Xt), -1))
    return out


# ==============================================================================================
def _acc(P, X, y):
    return float((predict(P, X) == y).mean())


def _show_patch(ax, img, title=None, color=INK):
    ax.imshow(img.reshape(N, N), cmap="gray", vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for sp_ in ax.spines.values():
        sp_.set_visible(True)
        sp_.set_color("#9AA5B1")
        sp_.set_linewidth(0.6)
    if title:
        ax.set_title(title, fontsize=6.2, weight="normal", color=color, pad=2)


def _blur(X, sd):
    return np.array([ndimage.gaussian_filter(x.reshape(N, N), sd).ravel() for x in X])


def shift():
    """Accuracy of the patch classifier under sensor noise and other shifts (stress test)."""
    P = patch_model("std")
    rng = np.random.default_rng(5301)
    X0, y0 = make_set(400, rng)
    cases = [("inside design domain", X0, y0)]
    for s_ in (0.1, 0.2, 0.3):
        X, y = make_set(400, rng, noise=s_)
        cases.append((f"noise {s_:.1f}", X, y))
    cases.append(("gain ×0.5 (ageing)", X0 * 0.5, y0))
    cases.append(("blur 1 pixel", _blur(X0, 1.0), y0))
    cases.append(("blur 2 pixels", _blur(X0, 2.0), y0))
    X, y = make_set(400, rng, el=(5, 12))
    cases.append(("low Sun 5–12°", X, y))
    X, y = make_set(400, rng, el=(60, 80))
    cases.append(("high Sun 60–80°", X, y))
    for o in (60, 90, 180):
        X, y = make_set(400, rng, az=(180 + o - 5, 180 + o + 5))
        cases.append((f"Sun azimuth +{o}°", X, y))
    accs = [(t, _acc(P, X, y)) for t, X, y in cases]
    print("shift: stress test")
    for t, a in accs:
        print(f"  {t:24s} {a*100:5.1f}")
    offs = np.arange(0, 181, 15)
    acc_a, swap = [], []
    for o in offs:
        X, y = make_set(400, rng, az=(180 + o - 5, 180 + o + 5))
        pr = predict(P, X)
        acc_a.append(float((pr == y).mean()))
        swap.append(float((pr[y == 1] == 2).mean()))
    print("shift: sun offset", offs)
    print("  acc", np.round(acc_a, 3))
    print("  crater->boulder", np.round(swap, 3))

    fig = plt.figure(figsize=(7.0, 2.95))
    gs = fig.add_gridspec(1, 3, width_ratios=[0.95, 1.25, 1], wspace=0.30, left=0.015, right=0.99, top=0.87,
                          bottom=0.25)
    # (a) example patches
    sub = gs[0].subgridspec(2, 3, wspace=0.08, hspace=0.36)
    hc = _height("crater", np.random.default_rng(7))
    hb = _height("boulder", np.random.default_rng(8))
    hp = _height("plain", np.random.default_rng(9))
    ex = [(hp, 180, 0.02, "plain"), (hc, 180, 0.02, "crater"), (hb, 180, 0.02, "boulder"),
          (hc, 0, 0.02, "crater,\nSun east"), (hb, 0, 0.02, "boulder,\nSun east"), (hc, 180, 0.2, "crater,\nnoise 0.2")]
    for k, (h, az, nz, t) in enumerate(ex):
        a = fig.add_subplot(sub[k // 3, k % 3])
        _show_patch(a, _shade(h, az, 32, np.random.default_rng(3), nz), t, color=(RED if k >= 3 else INK))
        if k == 0:
            panel_tag(a, "a", x=-0.05, y=1.12)
    fig.text(0.165, 0.215, "top: inside the design domain\n(Sun from the west); bottom: outside", fontsize=6.0,
             color=GREY, ha="center", va="top")
    # (b) stress test
    ax = fig.add_subplot(gs[1])
    labs = [t for t, _ in accs][::-1]
    vals = np.array([a for _, a in accs][::-1]) * 100
    cols = [GREEN if t.startswith("inside") else (RED if v < 80 else (ORANGE if v < 95 else BLUE))
            for t, v in zip(labs, vals)]
    ax.barh(range(len(vals)), vals, color=cols, height=0.72, zorder=2)
    for i, (v, t) in enumerate(zip(vals, labs)):
        if v > 55:
            ax.text(1.5, i, t, va="center", ha="left", fontsize=6.2, color="white", weight="bold", zorder=4)
            ax.text(v + 1, i, f"{v:.0f}", va="center", fontsize=6.2, color=INK, zorder=4)
        else:
            ax.text(v + 1, i, f"{v:.0f}   {t}", va="center", fontsize=6.2, color=INK, zorder=4)
    ax.set_yticks([])
    ax.axvline(100 / 3, color=GREY, lw=0.8, ls=":", zorder=0.5)
    ax.text(100 / 3, len(vals) - 0.2, "chance", fontsize=6.0, color=GREY, va="bottom", ha="center")
    ax.set_xlim(0, 108)
    ax.set_ylim(-0.6, len(vals) + 0.3)
    ax.set_xlabel("accuracy (%)")
    ax.grid(axis="y", visible=False)
    panel_tag(ax, "b", x=-0.02)
    # (c) Sun azimuth
    ax = fig.add_subplot(gs[2])
    ax.axvspan(0, 30, color=GREEN, alpha=0.12, lw=0)
    ax.text(15, 50, "design\ndomain", fontsize=6.0, color=GREEN, ha="center", va="center")
    ax.plot(offs, np.array(acc_a) * 100, "-o", ms=3, color=BLUE)
    ax.plot(offs, np.array(swap) * 100, "--", color=RED, lw=1.2)
    ax.text(178, 44, "accuracy", fontsize=6.6, color=BLUE, ha="right", va="bottom")
    ax.text(178, 86, "craters called\nboulders", fontsize=6.6, color=RED, ha="right", va="top")
    ax.axhline(100 / 3, color=GREY, lw=0.8, ls=":")
    ax.set_xlabel("Sun azimuth away from training (°)")
    ax.set_ylabel("per cent")
    ax.set_xticks([0, 30, 60, 90, 120, 150, 180])
    ax.set_ylim(0, 102)
    ax.set_xlim(0, 180)
    panel_tag(ax, "c")
    foot(fig, "Synthetic 16 × 16 patches rendered from height maps with Lambertian shading; network 256–64–32–3 "
         "(ReLU, numpy, Adam) trained on 9 000 patches with the Sun from the west (azimuth 150–210°, elevation "
         "20–45°) and noise 0.02. Each bar or point: 1 200 new test patches. Seeds fixed.", width=165)
    save(fig, "ch53_shift")


def features(P, X):
    """Both hidden layers (64 + 32 ReLU units)."""
    hs = net_fwd(P, X)[1]
    return np.hstack([hs[1], hs[2]])


@lru_cache(maxsize=None)
def monitor_scores():
    """Mahalanobis distance to the nearest class (class-conditional Gaussian model of the hidden features) and the
    max-softmax score for each test set."""
    P = patch_model("std")
    Xtr, ytr = train_data()
    F = features(P, Xtr)
    mus = [F[ytr == k].mean(0) for k in range(3)]
    Sis = [np.linalg.inv(np.cov(F[ytr == k].T) + 1e-3 * np.eye(F.shape[1])) for k in range(3)]
    out = {}
    for k, (X, y) in test_sets().items():
        f = features(P, X)
        d = np.stack([np.einsum("ij,jk,ik->i", f - m, Si, f - m) for m, Si in zip(mus, Sis)], 1).min(1)
        p = softmax(net_fwd(P, X)[1][-1])
        out[k] = dict(maha=d, soft=1 - p.max(1), pred=p.argmax(1), y=y)
    return out


def _roc(s_in, s_out):
    th = np.unique(np.concatenate([s_in, s_out]))[::-1]
    th = np.concatenate([[np.inf], th])
    fpr = np.array([(s_in >= t).mean() for t in th])
    tpr = np.array([(s_out >= t).mean() for t in th])
    auc = np.trapezoid(tpr, fpr)
    return fpr, tpr, auc


OODSETS = [("sun", "Sun from the east", RED), ("fault", "detector fault", ORANGE), ("trough", "unseen terrain", VIOLET)]


def ood():
    """Runtime monitor: Mahalanobis distance on hidden features vs max-softmax; ROC and safety-cage trade."""
    sc = monitor_scores()
    idd = sc["id"]
    print("ood: ID accuracy", (idd["pred"] == idd["y"]).mean())
    o = sc["sun"]
    w = o["pred"] != o["y"]
    print(f"  Sun from east: wrong answers with confidence > 0.9: {np.mean(1 - o['soft'][w] > 0.9)*100:.0f} %, "
          f"median confidence {np.median(1 - o['soft'][w]):.3f}")
    res = {}
    for k, name, _ in OODSETS:
        o = sc[k]
        r = {}
        for m in ("maha", "soft"):
            fpr, tpr, auc = _roc(idd[m], o[m])
            t95 = np.quantile(idd[m], 0.95)
            r[m] = (fpr, tpr, auc, float((o[m] > t95).mean()))
        res[k] = r
        acc = (o["pred"] == o["y"]).mean() if k != "trough" else 0.0
        print(f"  {name:20s} acc {acc:.3f}  AUC maha {r['maha'][2]:.3f} soft {r['soft'][2]:.3f}  "
              f"TPR@5%FPR maha {r['maha'][3]:.3f} soft {r['soft'][3]:.3f}")
    # ---- safety-cage trade on an operational stream: 90 % inside the domain, 10 % outside (equal thirds)
    w_in, w_out = 0.90, 0.10 / 3

    def trade(m, odd=False):
        qs = np.linspace(0.0, 1.0, 201)
        av, hz = [], []
        for q in qs:
            t = np.quantile(idd[m], q) if q < 1 else np.inf
            acts_in = idd[m] <= t
            a = w_in * acts_in.mean()
            h = w_in * (acts_in & (idd["pred"] != idd["y"])).mean()
            for k, _, _ in OODSETS:
                o = sc[k]
                acts = (o[m] <= t) & (not (odd and k == "sun"))
                wrong = np.ones_like(acts) if k == "trough" else (o["pred"] != o["y"])
                a += w_out * acts.mean()
                h += w_out * (acts & wrong).mean()
            av.append(a)
            hz.append(h)
        return qs, np.array(av), np.array(hz)

    trades = {m: trade(m) for m in ("maha", "soft")}
    trades["odd"] = trade("maha", odd=True)
    for m in ("maha", "soft", "odd"):
        qs, av, hz = trades[m]
        for q in (1.0, 0.99, 0.95, 0.90):
            j = np.argmin(abs(qs - q))
            print(f"  cage {m} accept {q:.2f} of in-domain: availability {av[j]*100:.1f} %, "
                  f"hazardous errors {hz[j]*100:.2f} %")

    fig = plt.figure(figsize=(7.0, 3.05))
    gs = fig.add_gridspec(1, 3, wspace=0.40, left=0.065, right=0.99, top=0.86, bottom=0.335)
    # (a) histograms of Mahalanobis distance
    ax = fig.add_subplot(gs[0])
    allv = np.concatenate([sc[k]["maha"] for k in ("id", "sun", "fault", "trough")])
    bins = np.logspace(np.log10(max(allv.min(), 1)), np.log10(allv.max()), 40)
    ax.hist(idd["maha"], bins=bins, color=GREEN, alpha=0.55, label="inside domain", density=True)
    for k, name, c in OODSETS:
        ax.hist(sc[k]["maha"], bins=bins, histtype="step", color=c, lw=1.2, label=name, density=True)
    t95 = np.quantile(idd["maha"], 0.95)
    ax.axvline(t95, color=INK, lw=0.9, ls="--")
    ax.text(t95 * 1.15, ax.get_ylim()[1] * 0.97, "threshold:\n95 % of in-domain\ninputs pass", fontsize=5.8,
            va="top", ha="left", color=INK)
    ax.set_xscale("log")
    ax.set_yticks([])
    ax.set_xlabel("Mahalanobis distance $d^2$", fontsize=7.5)
    ax.set_ylabel("share of inputs", fontsize=7.5)
    ax.legend(fontsize=5.8, loc="lower left", bbox_to_anchor=(-0.02, 1.0), ncol=2, handlelength=1.2,
              columnspacing=0.8)
    panel_tag(ax, "a", y=1.22)
    # (b) ROC
    ax = fig.add_subplot(gs[1])
    for k, name, c in OODSETS:
        fpr, tpr, auc, _ = res[k]["maha"]
        ax.plot(fpr, tpr, color=c, lw=1.4, label=f"{name} ({auc:.2f})")
        fpr, tpr, auc, _ = res[k]["soft"]
        ax.plot(fpr, tpr, color=c, lw=1.0, ls="--")
    ax.plot([0, 1], [0, 1], color=GREY, lw=0.7, ls=":")
    ax.set_xlabel("in-domain inputs flagged\n(false alarms)", fontsize=7.5)
    ax.set_ylabel("outside inputs flagged", fontsize=7.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.01)
    ax.legend(fontsize=5.8, loc="lower right", title="Mahalanobis (AUC)", title_fontsize=5.8, handlelength=1.4)
    ax.set_title("solid: Mahalanobis; dashed: softmax", fontsize=6.2, weight="normal", color=GREY, pad=3)
    panel_tag(ax, "b")
    # (c) cage trade
    ax = fig.add_subplot(gs[2])
    for m, c, lab in (("soft", ORANGE, "softmax"), ("maha", BLUE, "Mahalanobis"),
                      ("odd", GREEN, "Mahalanobis + Sun-angle check")):
        qs, av, hz = trades[m]
        ax.plot(av * 100, hz * 100, color=c, lw=1.4, label=lab)
        j = np.argmin(abs(qs - 0.95))
        ax.plot(av[j] * 100, hz[j] * 100, "o", color=c, ms=4)
    qs, av, hz = trades["maha"]
    ax.plot(av[-1] * 100, hz[-1] * 100, "s", color=RED, ms=5)
    ax.text(av[-1] * 100 - 1.5, hz[-1] * 100, "no cage", fontsize=6.0, color=RED, ha="right", va="center")
    ax.set_xlabel("availability: inputs\nhandled by ML (%)", fontsize=7.5)
    ax.set_ylabel("hazardous errors (% of inputs)", fontsize=7.5)
    ax.set_xlim(60, 101)
    ax.set_ylim(0, None)
    ax.legend(fontsize=5.8, loc="upper left", handlelength=1.4)
    panel_tag(ax, "c")
    foot(fig, "Same network and patches as the previous figure. Monitor: distance to the nearest class in the 96 hidden "
         "units, with class means and covariances from the training set. Each outside set: 1 800 patches. Stream in (c): 90 % "
         "inside the domain, 10 % outside (equal thirds); dots mark the threshold that passes 95 % of in-domain "
         "inputs; flagged inputs go to a safe fallback.", width=165)
    save(fig, "ch53_ood")


def fgsm_attack(P, X, y, eps):
    return np.clip(X + eps * np.sign(input_grad(P, X, y)), 0, 1)


def pgd_attack(P, X, y, eps, steps=10, rng=None):
    rng = rng or np.random.default_rng(0)
    Xa = np.clip(X + rng.uniform(-eps, eps, X.shape), 0, 1)
    a = eps / 4
    for _ in range(steps):
        Xa = Xa + a * np.sign(input_grad(P, Xa, y))
        Xa = np.clip(np.clip(Xa, X - eps, X + eps), 0, 1)
    return Xa


def fgsm():
    """Adversarial examples on the patch classifier: FGSM and PGD, random noise, adversarial training."""
    Ps, Pa = patch_model("std"), patch_model("adv")
    X, y = test_sets()["id"]
    rng = np.random.default_rng(77)
    eps = np.array([0.0, 0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1])
    curves = {k: [] for k in ("s_rand", "s_fgsm", "s_pgd", "a_fgsm", "a_pgd")}
    for e in eps:
        curves["s_rand"].append(_acc(Ps, np.clip(X + e * rng.choice([-1, 1], X.shape), 0, 1), y))
        curves["s_fgsm"].append(_acc(Ps, fgsm_attack(Ps, X, y, e), y))
        curves["s_pgd"].append(_acc(Ps, pgd_attack(Ps, X, y, e), y))
        curves["a_fgsm"].append(_acc(Pa, fgsm_attack(Pa, X, y, e), y))
        curves["a_pgd"].append(_acc(Pa, pgd_attack(Pa, X, y, e), y))
    print("fgsm: eps", eps, "(x255:", np.round(eps * 255, 1), ")")
    for k, v in curves.items():
        print(f"  {k:7s}", np.round(np.array(v) * 100, 1))
    # example: a crater turned into a boulder
    Xc, yc = X[y == 1], y[y == 1]
    e0 = 0.03
    Xadv = fgsm_attack(Ps, Xc, yc, e0)
    pa = softmax(net_fwd(Ps, Xadv)[1][-1])
    p0 = softmax(net_fwd(Ps, Xc)[1][-1])
    cand = np.where((pa.argmax(1) == 2) & (p0[:, 1] > 0.95))[0]
    j = cand[np.argmax(pa[cand, 2])]
    print(f"  example: clean p(crater)={p0[j,1]:.3f}; adversarial eps={e0} p(boulder)={pa[j,2]:.3f} "
          f"(of {len(Xc)} craters, {np.mean(pa.argmax(1) != 1)*100:.1f} % misclassified)")

    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.25], wspace=0.25, left=0.01, right=0.99, top=0.88,
                          bottom=0.29)
    sub = gs[0].subgridspec(1, 3, wspace=0.35)
    a1 = fig.add_subplot(sub[0])
    _show_patch(a1, Xc[j], f"crater\n{p0[j,1]*100:.0f} % sure")
    panel_tag(a1, "a", x=-0.05, y=1.25)
    a2 = fig.add_subplot(sub[1])
    d = (Xadv[j] - Xc[j]).reshape(N, N)
    a2.imshow(d, cmap="RdBu_r", vmin=-e0, vmax=e0, interpolation="nearest")
    a2.set_xticks([])
    a2.set_yticks([])
    a2.grid(False)
    a2.set_title(f"change, ±{e0:.2f}\n(±{e0*255:.0f} of 255 levels)", fontsize=6.2, weight="normal", pad=2)
    a3 = fig.add_subplot(sub[2])
    _show_patch(a3, Xadv[j], f"“boulder”\n{pa[j,2]*100:.1f} % sure", color=RED)
    b1, b2, b3 = a1.get_position(), a2.get_position(), a3.get_position()
    ym = (b1.y0 + b1.y1) / 2
    fig.text((b1.x1 + b2.x0) / 2, ym, "+", fontsize=12, ha="center", va="center", color=INK)
    fig.text((b2.x1 + b3.x0) / 2, ym, "=", fontsize=12, ha="center", va="center", color=INK)
    fig.text(0.21, 0.2, "the change is invisible to a person but\nflips the network's answer", fontsize=6.2,
             color=GREY, ha="center", va="top")
    ax = fig.add_subplot(gs[1])
    e255 = eps * 255
    ax.plot(e255, np.array(curves["s_rand"]) * 100, "-", color=GREY, lw=1.2, label="random noise, same size")
    ax.plot(e255, np.array(curves["s_fgsm"]) * 100, "-o", ms=3, color=ORANGE, label="FGSM (one step)")
    ax.plot(e255, np.array(curves["s_pgd"]) * 100, "-s", ms=3, color=RED, label="PGD (10 steps)")
    ax.plot(e255, np.array(curves["a_fgsm"]) * 100, "--o", ms=2.5, color=SKY, lw=1.0)
    ax.plot(e255, np.array(curves["a_pgd"]) * 100, "--s", ms=3, color=BLUE, label="adversarially trained: PGD\n(light: FGSM)")
    ax.plot([0.03 * 255] * 2, [40, 102], color=GREEN, lw=0.9, ls=":")
    ax.text(0.03 * 255 - 0.4, 68, "ε used in\nadversarial\ntraining", fontsize=6.0, color=GREEN, va="center",
            ha="right")
    ax.set_xlabel("perturbation size ε (grey levels of 255, per pixel)", fontsize=7.5)
    ax.set_ylabel("accuracy (%)", fontsize=7.5)
    ax.set_ylim(0, 102)
    ax.set_xlim(0, 25.5)
    ax.legend(fontsize=6.0, loc="lower left", handlelength=1.8, bbox_to_anchor=(0.0, 0.0))
    panel_tag(ax, "b")
    foot(fig, "Same network and patches as before (1 800 in-domain test patches). White-box attacks use the gradient "
         "of the loss with respect to the pixels; PGD = projected gradient descent, step ε/4, random start. The "
         "adversarially trained network saw FGSM examples with ε = 0.03 (about 8 grey levels) during training.",
         width=165)
    save(fig, "ch53_fgsm")


# ==============================================================================================
# Interval bound propagation and exact verification on a tiny ReLU network
def _site_data(n, rng):
    """Landing-site toy: x1 = slope / 20 deg, x2 = rock cover / 20 %; safe (1) if under a curved limit."""
    X = rng.uniform(0, 1, (n, 2))
    lim = 0.62 - 0.35 * X[:, 0] ** 2 + 0.10 * np.sin(6 * X[:, 0])
    y = (X[:, 1] < lim).astype(int)
    flip = rng.uniform(0, 1, n) < 0.03
    y[flip] = 1 - y[flip]
    return X, y


@lru_cache(maxsize=None)
def site_model():
    rng = np.random.default_rng(530)
    X, y = _site_data(1500, rng)
    P = train(X, y, [2, 16, 16, 2], seed=3, epochs=250, bs=64, lr=3e-3, wd=0.0)
    return P, X, y


def ibp_bounds(P, lo, hi):
    """Interval bound propagation: returns lower/upper bounds of every layer's pre-activation."""
    out = []
    for i, (W, b) in enumerate(P):
        c, r = (lo + hi) / 2, (hi - lo) / 2
        zc, zr = c @ W + b, r @ np.abs(W)
        zl, zu = zc - zr, zc + zr
        out.append((zl, zu))
        lo, hi = (np.maximum(zl, 0), np.maximum(zu, 0)) if i < len(P) - 1 else (zl, zu)
    return out


def ibp_margin(P, x, eps, cls):
    """Certified lower bound of logit[cls] - logit[other] over the L-infinity ball (difference layer folded in)."""
    W2, b2 = P[-1]
    d = np.zeros(2)
    d[cls], d[1 - cls] = 1, -1
    Pm = P[:-1] + [[W2 @ d[:, None], np.array([b2 @ d])]]
    zl, zu = ibp_bounds(Pm, np.clip(x - eps, 0, 1), np.clip(x + eps, 0, 1))[-1]
    return float(zl[0])


def ibp_radius(P, x, cls, hi=0.25):
    lo_, hi_ = 0.0, hi
    for _ in range(30):
        m = (lo_ + hi_) / 2
        if ibp_margin(P, x, m, cls) > 0:
            lo_ = m
        else:
            hi_ = m
    return lo_


def milp_radius(P, x, cls):
    """Exact L-infinity robustness radius by mixed-integer linear programming (big-M ReLU encoding)."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    (W1, b1), (W2, b2), (W3, b3) = P
    R = 0.25                                 # radii above R are reported as R (plots stop at 0.2)
    box_lo, box_hi = np.clip(x - R, 0, 1), np.clip(x + R, 0, 1)    # inputs stay physical
    (l1, u1), (l2, u2), _ = ibp_bounds(P, box_lo, box_hi)
    n1, n2 = W1.shape[1], W2.shape[1]
    # variable order: x'(2), eps(1), z1(n1), h1(n1), d1(n1), z2(n2), h2(n2), d2(n2)
    ix, ie = 0, 2
    iz1, ih1, id1 = 3, 3 + n1, 3 + 2 * n1
    iz2, ih2, id2 = 3 + 3 * n1, 3 + 3 * n1 + n2, 3 + 3 * n1 + 2 * n2
    nv = 3 + 3 * n1 + 3 * n2
    rows, lbs, ubs = [], [], []

    def add(coefs, lb, ub):
        r = np.zeros(nv)
        for j, v in coefs:
            r[j] += v
        rows.append(r)
        lbs.append(lb)
        ubs.append(ub)
    for k in range(2):                      # |x'_k - x_k| <= eps
        add([(ix + k, 1), (ie, -1)], -np.inf, x[k])
        add([(ix + k, 1), (ie, 1)], x[k], np.inf)
    for j in range(n1):                     # z1 = W1^T x' + b1
        add([(iz1 + j, 1)] + [(ix + k, -W1[k, j]) for k in range(2)], b1[j], b1[j])
    for (iz, ih, idd, l, u, n) in ((iz1, ih1, id1, l1, u1, n1), (iz2, ih2, id2, l2, u2, n2)):
        for j in range(n):
            add([(ih + j, 1), (iz + j, -1)], 0, np.inf)                       # h >= z
            add([(ih + j, 1), (iz + j, -1), (idd + j, -l[j])], -np.inf, -l[j])   # h <= z - l(1-d)
            add([(ih + j, 1), (idd + j, -u[j])], -np.inf, 0)                  # h <= u d
    for j in range(n2):                     # z2 = W2^T h1 + b2
        add([(iz2 + j, 1)] + [(ih1 + k, -W2[k, j]) for k in range(n1)], b2[j], b2[j])
    w = W3[:, cls] - W3[:, 1 - cls]
    add([(ih2 + k, w[k]) for k in range(n2)], -np.inf, -(b3[cls] - b3[1 - cls]))   # margin <= 0
    lb = np.full(nv, -np.inf)
    ub = np.full(nv, np.inf)
    lb[ix:ix + 2], ub[ix:ix + 2] = box_lo, box_hi
    lb[ie], ub[ie] = 0, R
    for (iz, ih, idd, l, u, n) in ((iz1, ih1, id1, l1, u1, n1), (iz2, ih2, id2, l2, u2, n2)):
        lb[iz:iz + n], ub[iz:iz + n] = l, u
        lb[ih:ih + n], ub[ih:ih + n] = 0, np.maximum(u, 0)
        lb[idd:idd + n], ub[idd:idd + n] = 0, 1
    integ = np.zeros(nv)
    integ[id1:id1 + n1] = 1
    integ[id2:id2 + n2] = 1
    cvec = np.zeros(nv)
    cvec[ie] = 1
    fd = os.dup(1)                           # silence the solver's C-level messages
    nul = os.open(os.devnull, os.O_WRONLY)
    sys.stdout.flush()
    os.dup2(nul, 1)
    try:
        res = milp(cvec, constraints=LinearConstraint(np.array(rows), lbs, ubs), integrality=integ,
                   bounds=Bounds(lb, ub))
    finally:
        sys.stdout.flush()
        os.dup2(fd, 1)
        os.close(nul)
        os.close(fd)
    return float(res.x[ie]) if res.success else R


def attack_radius(P, x, cls, hi=0.25):
    """Smallest eps at which a PGD attack (with restarts) finds a counter-example (upper bound)."""
    def broken(e):
        rng = np.random.default_rng(1)
        for st in range(3):
            xa = np.clip(x + rng.uniform(-e, e, 2), 0, 1)
            for _ in range(40):
                g = input_grad(P, xa[None, :], np.array([cls]))[0]
                xa = np.clip(np.clip(xa + e / 10 * np.sign(g), x - e, x + e), 0, 1)
            if predict(P, xa[None, :])[0] != cls:
                return True
        return False
    lo_, hi_ = 0.0, hi
    if not broken(hi):
        return hi
    for _ in range(12):
        m = (lo_ + hi_) / 2
        if broken(m):
            hi_ = m
        else:
            lo_ = m
    return hi_


def ibp():
    """Certified robustness radius: IBP (sound, incomplete) vs exact MILP vs attack."""
    P, Xtr, ytr = site_model()
    rng = np.random.default_rng(531)
    Xt, yt = _site_data(110, rng)
    pr = predict(P, Xt)
    ok = pr == yt
    print(f"ibp: train acc {(predict(P, Xtr) == ytr).mean():.3f}, test acc {ok.mean():.3f}")
    Xt, cls = Xt[ok], pr[ok]
    r_ibp = np.array([ibp_radius(P, x, c) for x, c in zip(Xt, cls)])
    r_ex = np.array([milp_radius(P, x, c) for x, c in zip(Xt, cls)])
    r_at = np.array([attack_radius(P, x, c) for x, c in zip(Xt, cls)])
    print(f"  points {len(Xt)}; median radius IBP {np.median(r_ibp):.4f}, exact {np.nanmedian(r_ex):.4f}, "
          f"attack {np.median(r_at):.4f}; mean ratio IBP/exact {np.nanmean(r_ibp / r_ex):.2f}")
    print(f"  IBP never exceeds exact: {np.all(r_ibp <= r_ex + 1e-6)}; attack >= exact: "
          f"{np.mean(r_at >= r_ex - 1e-3):.3f}")
    epsg = np.linspace(0, 0.2, 81)
    f_ibp = [(r_ibp >= e).mean() for e in epsg]
    f_ex = [(r_ex >= e).mean() for e in epsg]
    f_at = [(r_at >= e).mean() for e in epsg]
    for e in (0.02, 0.05, 0.1):
        print(f"  eps {e}: certified IBP {np.mean(r_ibp >= e):.3f}, exact {np.mean(r_ex >= e):.3f}, "
              f"not broken by attack {np.mean(r_at >= e):.3f}")

    fig = plt.figure(figsize=(7.0, 3.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.15], wspace=0.28, left=0.075, right=0.99, top=0.9, bottom=0.25)
    ax = fig.add_subplot(gs[0])
    g = np.linspace(0, 1, 300)
    GX, GY = np.meshgrid(g, g)
    Z = net_fwd(P, np.c_[GX.ravel(), GY.ravel()])[1][-1]
    Z = (Z[:, 1] - Z[:, 0]).reshape(GX.shape)
    ax.contourf(GX, GY, Z > 0, levels=[-0.5, 0.5, 1.5], colors=["#F6D9D9", "#DDEFE2"])
    ax.contour(GX, GY, Z, levels=[0], colors=INK, linewidths=0.9)
    sel = rng.choice(len(Xtr), 250, replace=False)
    ax.scatter(Xtr[sel, 0], Xtr[sel, 1], s=3, c=[GREEN if v else RED for v in ytr[sel]], lw=0, alpha=0.6)
    pen = np.where(r_ex < 0.23, 0.0, 9.0)        # show only boxes below the 0.25 search cap
    picks = [int(np.argmin(np.hypot(Xt[:, 0] - a, Xt[:, 1] - b) + pen)) for a, b in
             [(0.25, 0.25), (0.5, 0.75), (0.8, 0.15), (0.15, 0.85), (0.5, 0.42), (0.85, 0.55)]]
    for j in picks:
        x0, y0 = Xt[j]
        for r_, kw in ((r_ex[j], dict(fill=False, ec=NAVY, lw=0.9, ls="--", zorder=4)),
                       (r_ibp[j], dict(fc=BLUE, ec=BLUE, alpha=0.35, lw=0.8, zorder=5))):
            xa_, xb_ = max(x0 - r_, 0), min(x0 + r_, 1)
            ya_, yb_ = max(y0 - r_, 0), min(y0 + r_, 1)
            ax.add_patch(Rectangle((xa_, ya_), xb_ - xa_, yb_ - ya_, **kw))
        ax.plot(x0, y0, "o", ms=2.5, color=INK, zorder=6)
    ax.text(0.03, 0.03, "safe", fontsize=7, color=GREEN, weight="bold", zorder=7)
    ax.text(0.5, 0.97, "unsafe", fontsize=7, color=RED, weight="bold", ha="center", va="top", zorder=7)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticklabels(["0", "5", "10", "15", "20"])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_yticklabels(["0", "5", "10", "15", "20"])
    ax.set_xlabel("slope (°)", fontsize=7.5)
    ax.set_ylabel("rock cover (%)", fontsize=7.5)
    ax.grid(False)
    panel_tag(ax, "a")
    ax.legend(handles=[Rectangle((0, 0), 1, 1, fc=BLUE, alpha=0.35, ec=BLUE),
                       Rectangle((0, 0), 1, 1, fill=False, ec=NAVY, ls="--")],
              labels=["certified by IBP", "exact (MILP)"], fontsize=6.0, loc="lower left",
              bbox_to_anchor=(0.0, 1.0), ncol=2, handlelength=1.2)
    ax = fig.add_subplot(gs[1])
    ax.plot(epsg * 20, np.array(f_at) * 100, color=RED, lw=1.3, label="not broken by attack (upper bound)")
    ax.plot(epsg * 20, np.array(f_ex) * 100, color=NAVY, lw=1.6, ls="--", label="exact, MILP (complete)")
    ax.plot(epsg * 20, np.array(f_ibp) * 100, color=BLUE, lw=1.6, label="IBP certified (sound, incomplete)")
    ax.fill_between(epsg * 20, f_ibp_ := np.array(f_ibp) * 100, np.array(f_ex) * 100, color=BLUE, alpha=0.12, lw=0)
    ax.text(2.6, 38, "verification\ngap", fontsize=6.2, color=BLUE, ha="center")
    ax.set_xlabel("perturbation radius ε (in slope degrees; rock cover in %)", fontsize=7.5)
    ax.set_ylabel("test points proved robust (%)", fontsize=7.5)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 102)
    ax.legend(fontsize=6.0, loc="upper right", handlelength=1.8)
    panel_tag(ax, "b")
    foot(fig, "Synthetic landing-site data (1 500 training points, 3 % label noise); network 2–16–16–2 (ReLU, numpy). "
         f"{len(Xt)} correctly classified test points. Radii in the L∞ norm (a box). MILP: scipy milp with a big-M "
         "encoding of each ReLU; attack: projected gradient with 3 random starts.", width=160)
    save(fig, "ch53_ibp")


# ==============================================================================================
def tests():
    """Statistical testing: failure-free tests needed, and what a test campaign can claim."""
    from scipy import optimize
    p = np.logspace(-6, -1, 200)
    fig = plt.figure(figsize=(7.0, 2.95))
    gs = fig.add_gridspec(1, 2, wspace=0.3, left=0.08, right=0.99, top=0.9, bottom=0.29)
    ax = fig.add_subplot(gs[0])
    for C, c in ((0.90, SKY), (0.95, BLUE), (0.99, NAVY)):
        n = np.log(1 - C) / np.log1p(-p)
        ax.loglog(p, n, color=c, lw=1.5, label=f"{C*100:.0f} % confidence, no failures")
    n1 = [optimize.brentq(lambda n: stats.binom.cdf(1, int(n), q) - 0.05, 1 / q, 30 / q) for q in p[::10]]
    ax.loglog(p[::10], n1, "--", color=ORANGE, lw=1.3, label="95 %, one failure allowed")
    n95 = np.log(0.05) / np.log1p(-1e-4)
    n95_1 = optimize.brentq(lambda n: stats.binom.cdf(1, int(n), 1e-4) - 0.05, 1e4, 1e6)
    ax.plot(1e-4, n95, "o", color=RED, ms=4, zorder=5)
    ax.annotate(f"p = 10⁻⁴ at 95 %:\n{n95:,.0f} tests".replace(",", " "), (1e-4, n95), (2e-5, 150),
                fontsize=6.4, color=RED, ha="center", arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    ax.invert_xaxis()
    ax.set_xlabel("failure probability to demonstrate, p", fontsize=7.5)
    ax.set_ylabel("independent tests needed", fontsize=7.5)
    ax.legend(fontsize=5.9, loc="upper left", handlelength=1.6)
    ax.set_ylim(10, 1e8)
    panel_tag(ax, "a", x=-0.14)
    print(f"tests: p=1e-4 at 95 %: {n95:.0f} failure-free; with one failure {n95_1:.0f}; 3/p = {3/1e-4:.0f}")
    for C in (0.9, 0.99):
        print(f"  p=1e-4 at {C}: {np.log(1-C)/np.log1p(-1e-4):.0f}")
    print(f"  1e-9 per hour at 95 %: {3/1e-9:.3g} hours = {3/1e-9/8766:.3g} years")
    # (b) upper confidence bound after n tests
    ax = fig.add_subplot(gs[1])
    n = np.logspace(1, 6.5, 200)
    for k, c in ((0, BLUE), (1, ORANGE), (5, RED)):
        ub = stats.beta.ppf(0.95, k + 1, n - k)
        ax.loglog(n, ub, color=c, lw=1.5, label=f"{k} failure{'s' if k != 1 else ''} seen")
    ax.axhline(1e-4, color=GREY, lw=0.8, ls=":")
    ax.text(12, 1.25e-4, "target 10⁻⁴", fontsize=6.2, color=GREY, va="bottom")
    ax.set_xlabel("number of independent tests, n", fontsize=7.5)
    ax.set_ylabel("95 % upper bound on p", fontsize=7.5)
    ax.legend(fontsize=6.0, loc="lower left", handlelength=1.6)
    ax.set_ylim(1e-7, 1)
    panel_tag(ax, "b", x=-0.14)
    for k in (0, 1, 5):
        print(f"  n=10 000, {k} failures: 95 % upper bound {stats.beta.ppf(0.95, k + 1, 10000 - k):.2e}")
    foot(fig, "Binomial statistics, assuming independent tests drawn from the operational distribution. (a) Smallest n "
         "with P(at most k failures | n, p) ≤ 1 − confidence. (b) One-sided Clopper–Pearson 95 % upper bound. "
         "For no failures, n ≈ 3/p at 95 % (the 'rule of three').", width=160)
    save(fig, "ch53_tests")


ENERGY = dict(peak=989e12, mfu=0.40, board_kw=0.70, host=1.3, pue=1.2)


def energy():
    """Training energy and emissions from compute (6 N D) with stated hardware assumptions."""
    e = ENERGY
    j_per_flop_new = e["board_kw"] * 1e3 * e["host"] * e["pue"] / (e["peak"] * e["mfu"])
    ref_flop, ref_mwh, ref_t = 3.14e23, 1287.0, 552.0          # Patterson et al. 2021 (175-billion-parameter model)
    j_per_flop_2020 = ref_mwh * 3.6e9 / ref_flop
    print(f"energy: J/FLOP now {j_per_flop_new:.3g}, 2020 reference {j_per_flop_2020:.3g}, "
          f"ratio {j_per_flop_2020/j_per_flop_new:.1f}")
    Nn, Dd = 7e9, 2e12
    C = 6 * Nn * Dd
    gpu_h = C / (e["peak"] * e["mfu"]) / 3600
    kw_gpu = e["board_kw"] * e["host"] * e["pue"]
    mwh = gpu_h * kw_gpu / 1e3
    tot = mwh * 3
    grids = [("low-carbon grid\n(30 g/kWh)", 30), ("world average 2025\n(458 g/kWh)", 458),
             ("coal-heavy grid\n(800 g/kWh)", 800)]
    print(f"  example 7e9 params x 2e12 tokens: C = {C:.3g} FLOP; GPU-hours {gpu_h:,.0f}; per GPU all-in "
          f"{kw_gpu:.3f} kW; one run {mwh:.1f} MWh; with 3x experiments {tot:.0f} MWh; on 512 GPUs "
          f"{gpu_h/512:.0f} h = {gpu_h/512/24:.1f} days")
    for g, ci in grids:
        print(f"  {g.splitlines()[0]}: {tot*ci/1e3:.1f} t CO2")
    inf_mwh = 1e6 * 365 * 0.24 / 1e6
    print(f"  inference 1 M queries/day at 0.24 Wh: {inf_mwh:.1f} MWh/yr = {inf_mwh*458/1e3:.1f} t at 458 g")

    fig = plt.figure(figsize=(7.0, 3.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1], wspace=0.32, left=0.08, right=0.99, top=0.9, bottom=0.30)
    ax = fig.add_subplot(gs[0])
    Cg = np.logspace(19, 25, 50)
    ax.loglog(Cg, Cg * j_per_flop_2020 / 3.6e9, color=GREY, lw=1.4, label="2020 efficiency (from the reference)")
    ax.loglog(Cg, Cg * j_per_flop_new / 3.6e9, color=BLUE, lw=1.6, label="2024–26 accelerators (assumed)")
    ax.plot(ref_flop, ref_mwh, "o", color=INK, ms=4)
    ax.text(ref_flop * 0.6, ref_mwh * 1.6, "175-billion-parameter\nmodel, 2020: 1 287 MWh", fontsize=6.0, ha="right",
            va="bottom")
    ax.plot(C, mwh, "s", color=ORANGE, ms=5)
    ax.text(C * 1.6, mwh * 0.55, f"worked example:\n{mwh:.0f} MWh per run", fontsize=6.0, color=ORANGE, va="top")
    ax.set_xlabel("training compute (floating-point operations)", fontsize=7.5)
    ax.set_ylabel("electricity per training run (MWh)", fontsize=7.5)
    ax.set_xlim(1e19, 1e25)
    ax.legend(fontsize=6.0, loc="lower right", handlelength=1.6)
    panel_tag(ax, "a")
    ax = fig.add_subplot(gs[1])
    labs = ["low-carbon\n30 g/kWh", "world average\n458 g/kWh", "coal-heavy\n800 g/kWh", "inference,\none year*"]
    vals = [tot * ci / 1e3 for _, ci in grids] + [inf_mwh * 458 / 1e3]
    cols = [GREEN, BLUE, RED, VIOLET]
    ax.bar(range(4), vals, color=cols, width=0.62)
    for i, v in enumerate(vals):
        ax.text(i, v + 3, f"{v:.0f} t" if v >= 10 else f"{v:.1f} t", ha="center", fontsize=6.4)
    ax.set_xticks(range(4))
    ax.set_xticklabels(labs, fontsize=6.2)
    ax.set_ylabel("tonnes of CO₂", fontsize=7.5)
    ax.set_ylim(0, max(vals) * 1.15)
    ax.grid(axis="x", visible=False)
    ax.set_title(f"worked example: {tot:.0f} MWh including experiments", fontsize=6.6, weight="normal", pad=3)
    panel_tag(ax, "b")
    foot(fig, "Compute C = 6 N D (N parameters, D training tokens). Assumed: 989 TFLOP/s peak per accelerator, 40 % "
         "utilisation, 0.7 kW board power × 1.3 for host and network × 1.2 data-centre overhead (PUE). Reference: "
         "Patterson et al. (2021). *1 million queries a day at 0.24 Wh each (a median reported by one large provider "
         "in 2025), world-average grid.", width=165)
    save(fig, "ch53_energy")


# ==============================================================================================
# Diagrams
def wshape():
    """Learning-assurance life cycle: a W-shaped process (simplified, after the EASA concept papers)."""
    fig, ax = canvas(7.0, 3.55, xlim=(0, 100), ylim=(0, 51))
    NEW, OLD = ORANGE, NAVY
    W, H = 15.0, 7.6
    nodes = {
        "req": (1.0, 39.5, "Requirements\nand design domain", OLD),
        "data": (10.5, 26.5, "Data management:\ncollect, label, split", NEW),
        "learn": (20.0, 13.5, "Learning process:\nmodel, loss, settings", NEW),
        "train": (31.5, 1.0, "Training", NEW),
        "lver": (43.0, 13.5, "Learning\nverification", NEW),
        "impl": (54.5, 1.0, "Implementation\non flight computer", OLD),
        "iver": (66.0, 13.5, "Inference-model\nverification", OLD),
        "dver": (75.5, 26.5, "Data\nverification", NEW),
        "rver": (84.0, 39.5, "Requirements\nverification", OLD),
    }
    for k, (x, y, t, c) in nodes.items():
        box(ax, x, y, W, H, t, fc=("#FBE7D6" if c == NEW else LIGHT), ec=c, fs=6.2, lw=1.1)
    chain = ["req", "data", "learn", "train", "lver", "impl", "iver", "dver", "rver"]
    for a, b in zip(chain[:-1], chain[1:]):
        xa, ya = nodes[a][0] + W / 2, nodes[a][1]
        xb, yb = nodes[b][0] + W / 2, nodes[b][1] + H
        if nodes[b][1] < nodes[a][1]:
            arrow(ax, (xa, ya), (xb, yb), lw=1.0, ms=8)
        else:
            arrow(ax, (nodes[a][0] + W / 2, nodes[a][1] + H), (nodes[b][0] + W / 2, nodes[b][1]), lw=1.0, ms=8)
    # traceability links (dotted)
    for a, b in (("req", "rver"), ("data", "dver"), ("learn", "lver")):
        ya = nodes[a][1] + H / 2
        ax.plot([nodes[a][0] + W, nodes[b][0]], [ya, ya], color=GREY, lw=0.8, ls=":")
    ax.text(50, 44.6, "traceability: each verification step checks the matching step on the left", fontsize=6.2,
            color=GREY, ha="center", va="bottom")
    ax.text(50, 31.0, "is the data complete, correct and\nrepresentative of the design domain?", fontsize=6.0,
            color=GREY, ha="center", va="bottom")
    ax.text(50.5, 21.8, "does the trained model generalise:\naccuracy, robustness, stability?", fontsize=6.0,
            color=GREY, ha="center", va="bottom")
    # legend + operations feedback
    box(ax, 79.5, 7.5, 3.0, 2.2, fc="#FBE7D6", ec=NEW, lw=1.0)
    ax.text(83.5, 8.6, "new for machine learning", fontsize=6.2, va="center")
    box(ax, 79.5, 3.5, 3.0, 2.2, fc=LIGHT, ec=OLD, lw=1.0)
    ax.text(83.5, 4.6, "as for classical software", fontsize=6.2, va="center")
    ax.annotate("", xy=(1.5 + W / 2, 47.4), xytext=(84.0 + W / 2, 47.4),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0, connectionstyle="arc3,rad=0.0",
                                linestyle="--"))
    ax.plot([84.0 + W / 2, 84.0 + W / 2], [47.1, 47.4], color=BLUE, lw=1.0)
    ax.text(50, 48.1, "in operation: runtime monitoring, drift and incidents feed new data and a new pass through the W",
            fontsize=6.2, color=BLUE, ha="center", va="bottom")
    save(fig, "ch53_wshape")


def cage():
    """Simplex / safety-cage architecture for an onboard learned function."""
    fig, ax = canvas(7.0, 3.6, xlim=(0, 100), ylim=(0, 52))
    UNV, VER = ORANGE, GREEN
    title_box(ax, 0.5, 18, 15, 22, "Sensors", "camera, lidar,\nstar tracker\n\ncontext:\nSun angle, altitude,\nmode, time",
              fs=6.0, tfs=6.8)
    title_box(ax, 25, 33, 24, 13, "Learned function", "e.g. neural hazard detector\nhigh performance, hard to\nverify (category C)",
              fs=6.0, tfs=6.8, hc=UNV, ec=UNV, fc="#FBE7D6")
    title_box(ax, 25, 4, 24, 13, "Baseline function", "e.g. plane fit to lidar slope,\nor a pre-surveyed safe site\n(verified, category B)",
              fs=6.0, tfs=6.8, hc=VER, ec=VER, fc="#E3F2E8")
    title_box(ax, 25, 19.0, 24, 12, "Input monitor", "inside the design domain?\nSun angle, image quality,\nout-of-distribution score",
              fs=5.9, tfs=6.6, hc=VER, ec=VER, fc="#E3F2E8")
    title_box(ax, 55, 33, 18, 13, "Output monitor", "plausible? physics,\nconsistency over time,\nsafety envelope",
              fs=5.9, tfs=6.6, hc=VER, ec=VER, fc="#E3F2E8")
    title_box(ax, 57, 9.5, 16, 18.5, "Arbiter", "learned output\nonly if both\nmonitors pass;\nelse baseline",
              fs=5.9, tfs=6.6, hc=NAVY, ec=NAVY)
    title_box(ax, 80, 18, 19, 15, "Guidance and\ncontrol", "commands to\nengines,\nthrusters", fs=6.0, tfs=6.4)
    title_box(ax, 80, 38, 19, 10, "Logs to ground", "monitor trips, inputs,\nfor review and retraining",
              fs=5.8, tfs=6.4, hc=GREY, ec=GREY)
    # arrows
    arrow(ax, (15.5, 36), (25, 39.5), lw=1.0, ms=8)
    arrow(ax, (15.5, 29), (25, 25), lw=1.0, ms=8)
    arrow(ax, (15.5, 22), (25, 10.5), lw=1.0, ms=8)
    arrow(ax, (49, 39.5), (55, 39.5), lw=1.0, ms=8)
    arrow(ax, (64, 33), (64, 28), lw=1.0, ms=8)
    ax.text(65, 30.6, "output +\ncheck", fontsize=5.8, color=NAVY, va="center")
    arrow(ax, (49, 25), (57, 22), lw=1.0, ms=8)
    ax.text(49.6, 25.6, "pass/fail", fontsize=5.8, color=NAVY, va="bottom", ha="left")
    arrow(ax, (49, 10.5), (57, 14), lw=1.0, ms=8)
    ax.text(49.6, 10.0, "fallback", fontsize=5.8, color=NAVY, va="top", ha="left")
    arrow(ax, (73, 19.5), (80, 24), lw=1.2, ms=9)
    arrow(ax, (73, 41), (80, 42), lw=0.8, ms=7, color=GREY, ls="--")
    arrow(ax, (65, 9.5), (65, 2.5), lw=0.8, ms=7, color=RED)
    ax.text(67, 3.5, "both fail or disagree:\nsafe mode / abort", fontsize=5.9, color=RED, va="center")
    ax.text(37, 49.5, "untrusted, high-performance path", fontsize=6.2, color=UNV, ha="center", weight="bold")
    ax.text(37, 0.6, "trusted, verified path", fontsize=6.2, color=VER, ha="center", weight="bold")
    save(fig, "ch53_cage")


def gsn():
    """An assurance case in Goal Structuring Notation for an onboard learned hazard detector."""
    from matplotlib.patches import Ellipse
    fig, ax = canvas(7.0, 4.3, xlim=(0, 100), ylim=(0, 61.5))

    def goal(x, y, w, h, tag, text, fs=5.9):
        box(ax, x, y, w, h, fc=LIGHT, ec=NAVY, style="square", lw=1.0)
        ax.text(x + 0.8, y + h - 0.6, tag, fontsize=5.9, weight="bold", color=NAVY, va="top")
        ax.text(x + w / 2, y + h / 2 - 0.9, text, fontsize=fs, ha="center", va="center", linespacing=1.2)

    def soln(x, y, r, tag, text):
        ax.add_patch(Circle((x, y), r, fc="#E3F2E8", ec=GREEN, lw=1.0, zorder=2))
        ax.text(x, y + r - 1.4, tag, fontsize=5.8, weight="bold", color=GREEN, ha="center", va="top", zorder=3)
        ax.text(x, y - 0.9, text, fontsize=5.6, ha="center", va="center", linespacing=1.15, zorder=3)

    goal(31, 52, 38, 8.2, "G1", "The learned hazard detector does not make\nlanding less safe inside its design domain",
         fs=6.3)
    box(ax, 1, 52.5, 25, 7.2, fc="white", ec=GREY, r=2.5, lw=0.9)
    ax.text(2, 59, "C1  design domain", fontsize=5.9, weight="bold", color=GREY, va="top")
    ax.text(13.5, 54.9, "altitude 2 000–50 m; Sun elevation\n5–45°; polar terrain types", fontsize=5.7, ha="center",
            va="center")
    ax.add_patch(Ellipse((86, 56.1), 26, 8.6, fc="white", ec=VIOLET, lw=0.9))
    ax.text(86, 56.1, "A1  Sun direction and altitude\nare known from navigation", fontsize=5.7, ha="center",
            va="center")
    ax.text(97.5, 52.3, "A", fontsize=6.5, weight="bold", color=VIOLET)
    ax.plot([26, 31], [56, 56], color=GREY, lw=0.8)
    ax.plot([69, 73], [56, 56], color=VIOLET, lw=0.8)
    # strategy
    sx, sy, sw, sh = 27, 41.5, 46, 6.5
    ax.add_patch(Polygon([(sx + 2, sy + sh), (sx + sw + 2, sy + sh), (sx + sw - 2, sy), (sx - 2, sy)], closed=True,
                         fc="#F1ECF8", ec=VIOLET, lw=1.0))
    ax.text(sx + 3.0, sy + sh - 0.5, "S1", fontsize=5.9, weight="bold", color=VIOLET, va="top")
    ax.text(50, sy + sh / 2 - 0.4, "argue over each life-cycle step and the runtime protection", fontsize=6.1,
            ha="center", va="center")
    arrow(ax, (50, 52), (50, 48), lw=0.9, ms=7)
    goals = [("G2", "requirements\nand domain are\ncomplete"), ("G3", "data are\nrepresentative\nand correct"),
             ("G4", "model is accurate\nand robust in\nthe domain"), ("G5", "cage catches\noutside inputs;\narbiter verified"),
             ("G6", "flight code\nmatches the\nverified model"), ("G7", "operations\nmonitor and\ncorrect")]
    sols = [("Sn1", "hazard\nanalysis,\ndomain review"), ("Sn2", "datasheet,\ncoverage\nreport"),
            ("Sn3", "30 000-case\ntest; IBP\nproofs"), ("Sn4", "monitor ROC;\nfault\ninjection"),
            ("Sn5", "bit-exact\nHIL; radiation\ntests"), ("Sn6", "drift limits;\nupdate\nprocedure")]
    gw, gh = 14.6, 10.5
    for k, ((gt, gtx), (st, stx)) in enumerate(zip(goals, sols)):
        x = 1.5 + k * 16.4
        goal(x, 24.5, gw, gh, gt, gtx)
        ax.annotate("", xy=(x + gw / 2, 35.0), xytext=(50, 41.5),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=0.8, mutation_scale=7, shrinkA=0, shrinkB=0))
        soln(x + gw / 2, 11.0, 7.3, st, stx)
        arrow(ax, (x + gw / 2, 24.5), (x + gw / 2, 18.3), lw=0.8, ms=7, color=GREEN)
    # legend
    lx = 1
    for t, c, kind in (("goal (claim)", NAVY, "g"), ("strategy", VIOLET, "s"), ("evidence", GREEN, "e"),
                       ("context", GREY, "c"), ("assumption", VIOLET, "a")):
        if kind == "g":
            ax.add_patch(Rectangle((lx, 0.6), 3, 2, fc=LIGHT, ec=c, lw=0.8))
        elif kind == "s":
            ax.add_patch(Polygon([(lx + 0.5, 2.6), (lx + 3.5, 2.6), (lx + 2.5, 0.6), (lx - 0.5, 0.6)], fc="#F1ECF8",
                                 ec=c, lw=0.8))
        elif kind == "e":
            ax.add_patch(Circle((lx + 1.5, 1.6), 1.1, fc="#E3F2E8", ec=c, lw=0.8))
        elif kind == "c":
            box(ax, lx, 0.6, 3, 2, fc="white", ec=c, r=0.8, lw=0.8)
        else:
            ax.add_patch(Ellipse((lx + 1.5, 1.6), 3.4, 2.0, fc="white", ec=c, lw=0.8))
        ax.text(lx + 4.2, 1.6, t, fontsize=5.9, va="center")
        lx += 18
    save(fig, "ch53_gsn")


def roadmap():
    """Outlook to 2035: when capabilities may become routine, with confidence levels (projections)."""
    rows = [
        ("Learned weather and EO products in operations", 2024.0, 2028, "high", "ECMWF AIFS operational 2025 (Ch. 47)"),
        ("Foundation models for Earth and space data", 2024.5, 2029, "high", "open models since 2023 (Ch. 44)"),
        ("Onboard AI triage on new EO satellites", 2025.0, 2030, "medium", "flight demos since 2020 (Ch. 45–46)"),
        ("LLM assistants in mission operations", 2025.5, 2029, "medium", "pilots; human approval kept (Ch. 49)"),
        ("Certified ML in safety-related flight functions", 2026.5, 2032, "medium", "standards 2024–27; none yet"),
        ("Autonomous constellation traffic coordination", 2025.0, 2031, "medium", "single-operator autonomy (Ch. 48, 50)"),
        ("AI-assisted servicing and assembly", 2026.0, 2033, "low", "demos; learned perception (Ch. 40, 48)"),
        ("Human–AI teaming on the lunar surface", 2028.0, 2034, "low", "field tests now; crews from late 2020s"),
        ("Spacecraft largely designed by AI", 2026.5, 2035, "low", "generative parts flown (Ch. 52)"),
        ("Data centres in orbit at commercial scale", 2026.0, 2036, "low", "single-satellite demos (Ch. 45)"),
    ]
    conf = {"high": GREEN, "medium": GOLD, "low": RED}
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    y0 = len(rows)
    for k, (name, start, routine, c, note_) in enumerate(rows):
        y = y0 - k
        ax.plot([2026.8, 2035.4], [y, y], color="#E3E8EE", lw=7, solid_capstyle="butt", zorder=1)
        ax.add_patch(Rectangle((max(start, 2023.5), y - 0.22), min(routine, 2035.4) - max(start, 2023.5), 0.44,
                               fc=conf[c], alpha=0.30, ec="none", zorder=2))
        if routine <= 2035:
            ax.plot(routine, y, "D", color=conf[c], ms=5.5, zorder=3)
        else:
            ax.annotate("", xy=(2035.6, y), xytext=(2034.4, y),
                        arrowprops=dict(arrowstyle="-|>", color=conf[c], lw=1.2))
        ax.text(2023.4, y, name, ha="right", va="center", fontsize=6.4)
        ax.text(2027.0, y + 0.27, note_, fontsize=5.6, color=GREY, va="bottom", ha="left")
    ax.axvline(2026.8, color=INK, lw=0.9, ls="--")
    ax.text(2026.85, y0 + 0.75, "October 2026", fontsize=6.2, ha="left", va="bottom")
    ax.set_xlim(2023.5, 2036)
    ax.set_ylim(0.4, y0 + 1.2)
    ax.set_yticks([])
    ax.set_xticks(range(2024, 2036, 2))
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    hs = [Line2D([], [], marker="D", color=conf[c], lw=0, ms=5, label=f"{c} confidence") for c in ("high", "medium",
                                                                                                      "low")]
    hs.append(Rectangle((0, 0), 1, 1, fc=GREY, alpha=0.3, label="shaded: from first use to routine use"))
    ax.legend(handles=hs, fontsize=6.0, loc="upper left", bbox_to_anchor=(-0.62, -0.08), ncol=4, handlelength=1.4)
    fig.subplots_adjust(left=0.37, right=0.99, top=0.93, bottom=0.17)
    fig.text(0.99, 0.005, "Diamonds: the author's estimate of when each capability becomes routine; these are "
             "projections, not facts. Grey notes: status in October 2026.", ha="right", va="bottom", fontsize=FOOT,
             color=GREY)
    save(fig, "ch53_roadmap")


if __name__ == "__main__":
    fns = [shift, ood, fgsm, ibp, tests, energy, wshape, cage, gsn, roadmap]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
