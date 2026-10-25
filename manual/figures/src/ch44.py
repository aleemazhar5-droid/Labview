"""Figures for Chapter 44 - Deep Learning, Foundation Models and Generative AI.

Most figures run real (small) neural networks written directly in numpy on synthetic or open data with fixed
random seeds: optimiser comparison, a trained self-attention layer, a 2-D diffusion model, a neural surrogate of
atmospheric density, deep ensembles with conformal prediction and input-gradient saliency.  The numbers quoted in
the chapter text are printed by each function.
"""
import sys
import time
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch  # noqa: F401
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[2]
FOOT = 6.0


def panel_tag(ax, s, x=-0.02, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, weight="bold", ha="right", va="bottom", color=INK)


def ttl(ax, letter, text, fs=8.4):
    ax.set_title(f"$\\bf{{{letter}}}$  {text}", fontsize=fs, loc="left", weight="normal")


def foot(fig, text, y=0.01, width=140):
    fig.text(0.99, y, "\n".join(textwrap.wrap(text, width)), ha="right", va="bottom", fontsize=FOOT, color=GREY,
             multialignment="right", linespacing=1.25)


# ==============================================================================================
# A tiny numpy deep-learning toolkit: MLP forward/backward and Adam
# ==============================================================================================
def act(z, kind):
    if kind == "relu":
        return np.maximum(z, 0.0)
    if kind == "tanh":
        return np.tanh(z)
    if kind == "silu":
        return z / (1.0 + np.exp(-z))
    raise ValueError(kind)


def dact(z, kind):
    if kind == "relu":
        return (z > 0).astype(z.dtype)
    if kind == "tanh":
        return 1.0 - np.tanh(z) ** 2
    if kind == "silu":
        s = 1.0 / (1.0 + np.exp(-z))
        return s * (1.0 + z * (1.0 - s))
    raise ValueError(kind)


def mlp_init(sizes, rng, gain=None, kind="relu"):
    params = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        g = gain if gain is not None else (np.sqrt(2.0) if kind == "relu" else 1.0)
        params.append([rng.normal(0.0, g / np.sqrt(a), (a, b)), np.zeros(b)])
    return params


def mlp_forward(params, X, kind="relu"):
    hs, zs = [X], []
    h = X
    for i, (W, b) in enumerate(params):
        z = h @ W + b
        zs.append(z)
        h = act(z, kind) if i < len(params) - 1 else z
        hs.append(h)
    return h, (hs, zs)


def mlp_backward(params, cache, dout, kind="relu"):
    hs, zs = cache
    grads = [None] * len(params)
    d = dout
    for i in reversed(range(len(params))):
        W, _ = params[i]
        if i < len(params) - 1:
            d = d * dact(zs[i], kind)
        grads[i] = [hs[i].T @ d, d.sum(axis=0)]
        d = d @ W.T
    return grads, d


class Adam:
    def __init__(self, arrays, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8):
        self.a, self.lr, self.b1, self.b2, self.eps = arrays, lr, b1, b2, eps
        self.m = [np.zeros_like(x) for x in arrays]
        self.v = [np.zeros_like(x) for x in arrays]
        self.t = 0

    def step(self, grads, lr=None):
        self.t += 1
        lr = self.lr if lr is None else lr
        for x, g, m, v in zip(self.a, grads, self.m, self.v):
            m *= self.b1
            m += (1 - self.b1) * g
            v *= self.b2
            v += (1 - self.b2) * g * g
            mh = m / (1 - self.b1 ** self.t)
            vh = v / (1 - self.b2 ** self.t)
            x -= lr * mh / (np.sqrt(vh) + self.eps)


def flat(params):
    return [p for layer in params for p in layer]


# ==============================================================================================
# 1. Building blocks: activations, initialisation through depth, optimisers
# ==============================================================================================
def _reg_data(n, rng):
    X = rng.uniform(-2, 2, (n, 2))
    y = np.sin(2.0 * X[:, 0]) * np.cos(1.5 * X[:, 1]) + 0.3 * X[:, 0] + 0.1 * rng.normal(size=n)
    return X, y[:, None]


def _train_opt(opt, lr, Xtr, ytr, Xva, yva, epochs=40, bs=32, seed=0):
    rng = np.random.default_rng(seed)
    params = mlp_init([2, 64, 64, 1], rng, kind="relu")
    arrs = flat(params)
    vel = [np.zeros_like(a) for a in arrs]
    adam = Adam(arrs, lr=lr) if opt == "adam" else None
    hist = []
    n = len(Xtr)
    for ep in range(epochs + 1):
        out, _ = mlp_forward(params, Xva)
        hist.append(float(np.mean((out - yva) ** 2)))
        if ep == epochs:
            break
        idx = rng.permutation(n)
        for k in range(0, n, bs):
            b = idx[k:k + bs]
            out, cache = mlp_forward(params, Xtr[b])
            grads, _ = mlp_backward(params, cache, 2 * (out - ytr[b]) / len(b))
            g = flat(grads)
            if opt == "adam":
                adam.step(g)
            else:
                beta = 0.9 if opt == "momentum" else 0.0
                for a, gi, v in zip(arrs, g, vel):
                    v *= beta
                    v += gi
                    a -= lr * v
        if not np.isfinite(hist[-1]) or hist[-1] > 1e3:
            hist += [np.nan] * (epochs - ep)
            break
    return np.array(hist)


def blocks():
    np.seterr(over="ignore", invalid="ignore")
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.65), gridspec_kw=dict(width_ratios=[1, 1.05, 1.15]))
    # (a) activation functions
    ax = axs[0]
    x = np.linspace(-4, 4, 400)
    gelu = 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))
    ax.plot(x, 1 / (1 + np.exp(-x)), color=BLUE, label="sigmoid")
    ax.plot(x, np.tanh(x), color=GREEN, label="tanh")
    ax.plot(x, np.maximum(x, 0), color=ORANGE, label="ReLU", lw=2.0)
    ax.plot(x, gelu, color=VIOLET, ls="--", label="GELU")
    ax.set_ylim(-1.3, 3.2)
    ax.set_xlabel("input z")
    ax.set_ylabel("activation f(z)")
    ax.legend(loc="upper left", fontsize=6.6, handlelength=1.6)
    ttl(ax, "a", "Activation functions")
    # (b) signal propagation through a deep ReLU network for three initialisation scales
    ax = axs[1]
    rng = np.random.default_rng(1)
    width, depth = 256, 30
    X0 = rng.normal(size=(512, width))
    res = {}
    for gain, lab, col in [(1.0, r"$\sigma_w^2 = 1/n$ (too small)", BLUE), (np.sqrt(2), r"$\sigma_w^2 = 2/n$ (He)", GREEN),
                           (2.0, r"$\sigma_w^2 = 4/n$ (too large)", RED)]:
        h = X0.copy()
        stds = [h.std()]
        r = np.random.default_rng(2)
        for _ in range(depth):
            W = r.normal(0, gain / np.sqrt(width), (width, width))
            h = np.maximum(h @ W, 0)
            stds.append(h.std())
        res[lab] = stds
        ax.semilogy(range(depth + 1), stds, color=col, label=lab)
    # with layer normalisation (too-large weights, but each layer's output re-standardised)
    h = X0.copy()
    stds = [h.std()]
    r = np.random.default_rng(2)
    for _ in range(depth):
        W = r.normal(0, 2.0 / np.sqrt(width), (width, width))
        h = np.maximum(h @ W, 0)
        h = (h - h.mean(axis=1, keepdims=True)) / (h.std(axis=1, keepdims=True) + 1e-6)
        stds.append(h.std())
    ax.semilogy(range(depth + 1), stds, color=GREY, ls=":", lw=1.8, label="too large + layer norm")
    ax.set_xlabel("layer")
    ax.set_ylabel("std. dev. of activations")
    ax.set_ylim(1e-6, 1e6)
    ax.legend(fontsize=5.9, loc="lower left", handlelength=1.5)
    ttl(ax, "b", "Initialisation, 30 layers")
    for lab, s in res.items():
        print(f"blocks: {lab}: activation std after {depth} layers = {s[-1]:.3g}")
    # (c) optimisers on the same small regression network
    ax = axs[2]
    rng = np.random.default_rng(5)
    Xtr, ytr = _reg_data(2000, rng)
    Xva, yva = _reg_data(2000, rng)
    grids = {"sgd": [0.003, 0.01, 0.03, 0.1], "momentum": [0.001, 0.003, 0.01, 0.03], "adam": [3e-4, 1e-3, 3e-3, 1e-2]}
    labels = {"sgd": "SGD", "momentum": "SGD + momentum", "adam": "Adam"}
    cols = {"sgd": BLUE, "momentum": ORANGE, "adam": GREEN}
    noise_floor = 0.01
    for opt, lrs in grids.items():
        best = None
        for lr in lrs:
            h = _train_opt(opt, lr, Xtr, ytr, Xva, yva)
            score = np.nanmean(h[-5:]) if np.all(np.isfinite(h[-5:])) else np.inf
            if best is None or score < best[0]:
                best = (score, lr, h)
        score, lr, h = best
        e10 = h[10]
        print(f"blocks: {opt}: best lr {lr}, val MSE after 10 epochs {e10:.4f}, after 40 epochs {h[-1]:.4f}")
        ax.semilogy(range(len(h)), h, color=cols[opt], label=f"{labels[opt]} (η = {lr:g})")
    ax.axhline(noise_floor, color=GREY, lw=0.8, ls="--")
    ax.text(39.5, noise_floor * 1.12, "noise floor", fontsize=6.0, color=GREY, ha="right", va="bottom")
    ax.set_xlabel("epoch")
    ax.set_ylabel("validation mean squared error")
    ax.set_ylim(0.006, 0.6)
    ax.legend(fontsize=6.2, loc="upper right")
    ttl(ax, "c", "Optimisers, same network")
    foot(fig, "(b) 512 random inputs through 30 ReLU layers of width 256. (c) Network 2-64-64-1 (ReLU, He init.) "
              "trained on 2 000 noisy samples of a smooth 2-D function, mini-batches of 32; best of four learning "
              "rates per optimiser on 2 000 validation samples; one seed.", width=150)
    fig.tight_layout(rect=(0, 0.07, 1, 1), w_pad=1.2)
    save(fig, "ch44_blocks")


# ==============================================================================================
# 2. Scaling laws (published fit of Hoffmann et al. 2022)
# ==============================================================================================
E_, A_, B_, ALPHA, BETA = 1.69, 406.4, 410.7, 0.34, 0.28


def chin_loss(N, D):
    return E_ + A_ / N ** ALPHA + B_ / D ** BETA


def chin_opt(C):
    Ns = np.logspace(6, 14, 4000)
    L = chin_loss(Ns, C / (6 * Ns))
    k = np.argmin(L)
    return Ns[k], C / (6 * Ns[k]), L[k]


def scaling():
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.9))
    ax = axs[0]
    Ns = np.logspace(7, 12, 300)
    Ds = np.logspace(9, 14, 300)
    NN, DD = np.meshgrid(Ns, Ds)
    L = chin_loss(NN, DD)
    cs = ax.contourf(np.log10(NN), np.log10(DD), L, levels=np.arange(1.8, 4.01, 0.2), cmap="Blues_r", alpha=0.9)
    cl = ax.contour(np.log10(NN), np.log10(DD), L, levels=[2.0, 2.2, 2.6, 3.0], colors="white", linewidths=0.6)
    ax.clabel(cl, fmt="%.1f", fontsize=6.0)
    for C in [1e19, 1e21, 1e23, 1e25]:
        n = np.logspace(7, 12, 400)
        d = C / (6 * n)
        ok = (d > 1e9) & (d < 1e14)
        ax.plot(np.log10(n[ok]), np.log10(d[ok]), color=ORANGE, lw=0.9, ls="--")
        x0, y0 = np.log10(n[ok][0]), np.log10(d[ok][0])
        ax.text(x0 + 0.12, min(y0, 13.88) - 0.12, f"10$^{{{int(np.log10(C))}}}$ FLOP", fontsize=6.0, color="white",
                va="top", ha="left", bbox=dict(fc=ORANGE, ec="none", pad=0.8, alpha=0.9))
    Cs = np.logspace(18, 26, 40)
    opt = np.array([chin_opt(C) for C in Cs])
    ok = (opt[:, 1] < 1e14) & (opt[:, 0] < 1e12)
    ax.plot(np.log10(opt[ok, 0]), np.log10(opt[ok, 1]), color=RED, lw=2.0, label="compute-optimal")
    n20 = np.logspace(7, 12, 10)
    ax.plot(np.log10(n20), np.log10(20 * n20), color="white", lw=1.0, ls=":", label="20 tokens per parameter")
    ax.set_xlabel("parameters N (log$_{10}$)")
    ax.set_ylabel("training tokens D (log$_{10}$)")
    ax.set_xlim(7, 12)
    ax.set_ylim(9, 14)
    ax.grid(False)
    leg = ax.legend(fontsize=6.0, loc="lower right", frameon=True, facecolor=NAVY, edgecolor="none", labelcolor="white")
    cb = fig.colorbar(cs, ax=ax, pad=0.02, fraction=0.06)
    cb.set_label("predicted loss (nats/token)", fontsize=7)
    cb.ax.tick_params(labelsize=6.5)
    ttl(ax, "a", "Loss surface $L(N, D)$")
    ax = axs[1]
    Cs = np.logspace(17, 26, 200)
    for N, col in zip([1e8, 1e9, 1e10, 1e11], [SKY, BLUE, VIOLET, NAVY]):
        D = Cs / (6 * N)
        ok = D > 1e8
        ax.plot(Cs[ok], chin_loss(N, D[ok]), color=col, lw=1.3, label=f"N = 10$^{{{int(np.log10(N))}}}$")
    opt = np.array([chin_opt(C) for C in Cs])
    ax.plot(Cs, opt[:, 2], color=RED, lw=2.2, ls="--", label="compute-optimal")
    ax.axhline(E_, color=GREY, lw=0.8, ls=":")
    ax.text(1.2e17, E_ + 0.03, "irreducible loss E = 1.69", fontsize=6.0, color=GREY, va="bottom")
    ax.set_xscale("log")
    ax.set_ylim(1.6, 4.2)
    ax.set_xlabel("training compute C (FLOP)")
    ax.set_ylabel("predicted loss (nats/token)")
    ax.legend(fontsize=6.2, loc="upper right", ncol=1)
    ttl(ax, "b", "Fixed model size vs optimal allocation")
    for C in [1e20, 1e22, 1e24]:
        n, d, l = chin_opt(C)
        print(f"scaling: C={C:.0e}: N_opt={n:.3g}, D_opt={d:.3g}, D/N={d / n:.1f}, L={l:.3f}")
    # fixed 1e9 model at 1e22 vs optimal
    print(f"scaling: N=1e9 at C=1e22 -> L={chin_loss(1e9, 1e22 / 6e9):.3f}")
    print(f"scaling: exponents a={BETA / (ALPHA + BETA):.3f}, b={ALPHA / (ALPHA + BETA):.3f}")
    foot(fig, "Computed from the published fit L = E + A/N^α + B/D^β (E = 1.69, A = 406.4, B = 410.7, α = 0.34, "
              "β = 0.28; Hoffmann et al. 2022) for language models; training compute C ≈ 6ND floating-point "
              "operations (dashed lines in a: equal compute). Constants differ for other data types and architectures.", width=150)
    fig.tight_layout(rect=(0, 0.07, 1, 1), w_pad=1.5)
    save(fig, "ch44_scaling")


# ==============================================================================================
# 3. Convolution filters applied to a real Landsat image
# ==============================================================================================
def _conv(img, k):
    from scipy.signal import convolve2d
    return convolve2d(img, k[::-1, ::-1], mode="same", boundary="symm")


def convmaps():
    from PIL import Image
    im = Image.open(ROOT / "figures/photos/ch44_vegas.jpg").convert("RGB")
    im = im.crop((30, 590, 510, 1070))          # 2011 image, Las Vegas valley and mountains (480 x 480 px)
    rgb = np.asarray(im).astype(float) / 255.0
    g = rgb @ np.array([0.299, 0.587, 0.114])
    g = (g - g.mean()) / g.std()
    sob_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float)
    sob_y = sob_x.T
    lap = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float)
    yy, xx = np.mgrid[-4:5, -4:5].astype(float)
    th = np.deg2rad(45)
    xr = xx * np.cos(th) + yy * np.sin(th)
    gab = np.exp(-(xx ** 2 + yy ** 2) / (2 * 2.2 ** 2)) * np.cos(2 * np.pi * xr / 5.0)
    gab -= gab.mean()
    ex, ey = _conv(g, sob_x), _conv(g, sob_y)
    lp = _conv(g, lap)
    gb = _conv(g, gab)
    mag = np.sqrt(ex ** 2 + ey ** 2)
    from scipy.ndimage import uniform_filter
    energy = uniform_filter(np.abs(lp), 15)
    relu = np.maximum(ex, 0)
    pooled = relu[: relu.shape[0] // 4 * 4, : relu.shape[1] // 4 * 4].reshape(relu.shape[0] // 4, 4, -1, 4).max(axis=(1, 3))

    fig = plt.figure(figsize=(7.0, 3.9))
    gs = fig.add_gridspec(2, 4, hspace=0.32, wspace=0.12)
    panels = [
        (rgb, "Input (Landsat 5, false colour)", None),
        (ex, "Vertical edges (Sobel x)", "RdBu_r"),
        (ey, "Horizontal edges (Sobel y)", "RdBu_r"),
        (gb, "Diagonal texture (Gabor 45°)", "RdBu_r"),
        (lp, "Spots and lines (Laplacian)", "RdBu_r"),
        (energy, "Texture energy (|Laplacian|, 15 px)", "magma"),
        (pooled, "ReLU + 4×4 max-pool of (b)", "Greys_r"),
    ]
    tags = "abcdefg"
    for k, (arr, title, cmap) in enumerate(panels):
        ax = fig.add_subplot(gs[k // 4, k % 4])
        if cmap is None:
            ax.imshow(arr)
        elif cmap == "RdBu_r":
            v = np.percentile(np.abs(arr), 96)
            ax.imshow(arr, cmap=cmap, vmin=-v, vmax=v)
        else:
            ax.imshow(arr, cmap=cmap, vmin=0, vmax=np.percentile(arr, 99.5))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(True)
            s.set_color("#9AA5B1")
            s.set_linewidth(0.5)
        ttl(ax, tags[k], title, fs=6.6)
    # inset kernels on (b) and (d)
    ax = fig.add_subplot(gs[1, 3])
    L = np.arange(1, 13)
    rf_plain = 1 + 2 * L
    # VGG-like: 2x2 pooling after every second 3x3 conv
    rf_pool, rf, jump = [], 1, 1
    for l in L:
        rf += 2 * jump
        if l % 2 == 0:
            rf += jump
            jump *= 2
        rf_pool.append(rf)
    rf_dil = 2 ** (L + 1) - 1
    ax.plot(L, rf_plain, "o-", ms=2.2, color=BLUE, label="3×3 conv.")
    ax.plot(L, rf_pool, "s-", ms=2.2, color=ORANGE, label="+ pool every 2nd")
    ax.plot(L, rf_dil, "^-", ms=2.2, color=GREEN, label="dilated ×2")
    ax.set_yscale("log")
    ax.set_xticks([2, 4, 6, 8, 10, 12])
    ax.set_xlabel("layers", fontsize=6.4, labelpad=0)
    ax.set_ylabel("receptive field (px)", fontsize=6.4, labelpad=0)
    ax.tick_params(labelsize=5.9, pad=1)
    ax.legend(fontsize=5.5, loc="upper left", handlelength=1.2, borderaxespad=0.2)
    ttl(ax, "h", "Receptive field growth", fs=6.6)
    print(f"convmaps: input {g.shape}, pooled {pooled.shape}; RF after 12 layers plain {rf_plain[-1]}, "
          f"pooled {rf_pool[-1]}, dilated {rf_dil[-1]}")
    foot(fig, "Fixed (hand-designed) 3×3 and 9×9 kernels convolved with a 480 × 480-pixel crop (about 40 m per "
              "pixel) of a Landsat 5 image of Las Vegas, Nevada, 2 November 2011 (bands 7, 4, 2; NASA/USGS). "
              "Red and blue: positive and negative responses. A trained CNN learns similar filters in its first layer.",
         width=150)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.95, bottom=0.14)
    pos = ax.get_position()
    ax.set_position([pos.x0 + 0.035, pos.y0 + 0.02, pos.width - 0.04, pos.height - 0.02])
    save(fig, "ch44_convmaps")


# ==============================================================================================
# 4. CNN architectures: classifier with tensor shapes, residual block, U-Net
# ==============================================================================================
def _slab(ax, x, y, w, h, d, fc, ec=NAVY, lw=0.7, z=2):
    """Pseudo-3D feature-map block: front face w x h, depth offset d."""
    off = d * 0.45
    ax.add_patch(Polygon([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], closed=True, fc=fc, ec=ec, lw=lw,
                         zorder=z))
    ax.add_patch(Polygon([(x, y + h), (x + off, y + h + off * 0.8), (x + w + off, y + h + off * 0.8), (x + w, y + h)],
                         closed=True, fc=fc, ec=ec, lw=lw, zorder=z, alpha=0.75))
    ax.add_patch(Polygon([(x + w, y), (x + w + off, y + off * 0.8), (x + w + off, y + h + off * 0.8), (x + w, y + h)],
                         closed=True, fc=fc, ec=ec, lw=lw, zorder=z, alpha=0.55))


def cnnarch():
    fig, ax = canvas(7.0, 4.7, xlim=(0, 100), ylim=(0, 67))
    # --- top: small CNN classifier
    ax.text(1, 66.5, "A small CNN classifier (Example 44.1)", fontsize=8.2, weight="bold", color=NAVY, va="top")
    specs = [("256×256×4\ninput chip", 3.0, 0.8, 16, 2, "#D6E4F0"),
             ("256×256×32\nconv 3×3 + ReLU", 17.0, 1.8, 16, 4, "#9FC3E3"),
             ("128×128×64\npool, conv", 32.0, 2.6, 11, 6, "#6FA6D6"),
             ("64×64×128\npool, conv", 48.0, 3.4, 7.5, 8, "#3F84C2"),
             ("32×32×128\npool", 64.0, 3.4, 5, 8, "#2465A3")]
    yc = 51.0
    ends = []
    for txt, x, w, h, d, col in specs:
        _slab(ax, x, yc - h / 2, w, h, d, col)
        off = d * 0.45
        ends.append((x, x + w + off))
        ax.text(x + (w + off) / 2, 41.8, txt, fontsize=5.8, ha="center", va="top", color=INK, linespacing=1.15)
    for k in range(len(ends) - 1):
        arrow(ax, (ends[k][1] + 0.8, yc), (ends[k + 1][0] - 0.8, yc), lw=0.9, ms=7)
    box(ax, 75.5, yc - 4, 8.5, 8, text="global\naverage\npool → 128", fs=5.8, fc="white", ec=BLUE, r=0.6)
    arrow(ax, (ends[-1][1] + 0.8, yc), (75.3, yc), lw=0.9, ms=7)
    box(ax, 87.0, yc - 4, 9.0, 8, text="dense\n128 → 10\nsoftmax", fs=5.8, fc="white", ec=BLUE, r=0.6)
    arrow(ax, (84.2, yc), (86.8, yc), lw=0.9, ms=7)
    ax.text(91.5, 41.8, "class\nprobabilities", fontsize=5.8, ha="center", va="top", color=INK, linespacing=1.15)
    ax.text(50, 36.0, "Each convolution slides the same small kernel over every position (weight sharing); pooling "
                      "halves the resolution and widens the view.", fontsize=6.0, color=GREY, ha="center",
            style="italic")
    ax.plot([1, 99], [34.2, 34.2], color="#C9D3DD", lw=0.6)
    # --- bottom left: residual block
    ax.text(1, 32.8, "Residual block (ResNet)", fontsize=8.2, weight="bold", color=NAVY, va="top")
    bx, cxr = 4.0, 12.0
    ax.text(cxr, 28.6, "input x", fontsize=6.2, ha="center", va="center")
    box(ax, bx, 21.0, 16, 4.2, text="conv 3×3 → norm → ReLU", fs=5.9, fc="white", ec=BLUE, r=0.6)
    box(ax, bx, 13.5, 16, 4.2, text="conv 3×3 → norm", fs=5.9, fc="white", ec=BLUE, r=0.6)
    ax.add_patch(Circle((cxr, 8.6), 1.5, fc="white", ec=NAVY, lw=1.0, zorder=3))
    ax.text(cxr, 8.6, "+", fontsize=9, ha="center", va="center", zorder=4, color=NAVY)
    box(ax, bx + 2, 1.2, 12, 4.0, text="ReLU → output y", fs=5.9, fc="white", ec=BLUE, r=0.6)
    arrow(ax, (cxr, 27.6), (cxr, 25.4), lw=0.9, ms=7)
    arrow(ax, (cxr, 21.0), (cxr, 17.9), lw=0.9, ms=7)
    arrow(ax, (cxr, 13.5), (cxr, 10.2), lw=0.9, ms=7)
    arrow(ax, (cxr, 7.0), (cxr, 5.4), lw=0.9, ms=7)
    ax.plot([cxr, 25.0, 25.0], [27.0, 27.0, 8.6], color=ORANGE, lw=1.3, zorder=2)
    arrow(ax, (25.0, 8.6), (cxr + 1.6, 8.6), lw=1.3, ms=8, color=ORANGE)
    ax.text(25.8, 18.0, "identity\nshortcut", fontsize=5.9, color=ORANGE, ha="left", va="center")
    ax.text(cxr + 0.8, 11.8, "F(x)", fontsize=6.2, color=BLUE, ha="left", va="center")
    ax.text(cxr - 2.0, 8.6, "F(x) + x", fontsize=6.2, color=NAVY, ha="right", va="center")
    ax.plot([34.5, 34.5], [1, 32], color="#C9D3DD", lw=0.6)
    # --- bottom right: U-Net
    ax.text(37, 32.8, "U-Net for semantic segmentation", fontsize=8.2, weight="bold", color=NAVY, va="top")
    lv = [(40, 20.5, 2.0, 7.0), (47, 14.5, 2.8, 5.0), (54.5, 9.0, 3.6, 3.4), (62.8, 3.5, 4.4, 2.4)]
    up = [(71.5, 9.0, 3.6, 3.4), (79.5, 14.5, 2.8, 5.0), (86.5, 20.5, 2.0, 7.0)]
    for x0, y0b, w, h in lv:
        ax.add_patch(Rectangle((x0, y0b), w, h, fc="#6FA6D6", ec=NAVY, lw=0.7, zorder=2))
    for x0, y0b, w, h in up:
        ax.add_patch(Rectangle((x0, y0b), w, h, fc="#E8A86B", ec=NAVY, lw=0.7, zorder=2))
    for (xa, ya, wa, ha_), (xb, yb, wb, hb) in zip(lv[:-1], lv[1:]):
        arrow(ax, (xa + wa / 2, ya - 0.2), (xb - 0.2, yb + hb / 2), lw=0.8, ms=6, color=NAVY)
    path_up = [lv[-1]] + up
    for (xa, ya, wa, ha_), (xb, yb, wb, hb) in zip(path_up[:-1], path_up[1:]):
        arrow(ax, (xa + wa + 0.2, ya + ha_ / 2), (xb + wb / 2, yb - 0.2), lw=0.8, ms=6, color=ORANGE)
    for (xa, ya, wa, ha_), (xb, yb, wb, hb) in zip(lv[:-1], up[::-1]):
        arrow(ax, (xa + wa + 0.3, ya + ha_ / 2), (xb - 0.3, yb + hb / 2), lw=0.8, ms=6, color=GREEN, ls="--")
    ax.text(64.3, 28.6, "skip connections copy fine spatial detail", fontsize=5.9, color=GREEN, ha="center")
    ax.text(41, 19.6, "image", fontsize=5.9, ha="center", va="top")
    ax.text(94.7, 19.6, "class map\n(per pixel)", fontsize=5.9, ha="center", va="top")
    ax.text(47.5, 6.0, "encoder:\nconv + pool", fontsize=5.9, color=NAVY, ha="center", va="center")
    ax.text(82.5, 6.0, "decoder:\nup-sample + conv", fontsize=5.9, color=ORANGE, ha="center", va="center")
    cl = [LAND, EARTH, "#C8B88A"]
    for i in range(5):
        for j in range(5):
            ax.add_patch(Rectangle((91.5 + j * 1.3, 20.5 + i * 1.4), 1.3, 1.4,
                                   fc=cl[(i // 2 + (j > 2)) % 3], ec="white", lw=0.3, zorder=3))
    arrow(ax, (88.8, 24.0), (91.3, 24.0), lw=0.8, ms=6, color=ORANGE)
    save(fig, "ch44_cnnarch")


# ==============================================================================================
# 5. A self-attention layer trained in numpy on periodic "telemetry"
# ==============================================================================================
T_SEQ, PERIOD = 48, 16


def _att_batch(rng, B):
    t = np.arange(T_SEQ + 1)
    A = rng.uniform(0.5, 1.5, (B, 1))
    ph = rng.uniform(0, 2 * np.pi, (B, 1))
    c = rng.uniform(-1, 1, (B, 1))
    clean = c + A * np.sin(2 * np.pi * t / PERIOD + ph) + 0.35 * A * np.sin(4 * np.pi * t / PERIOD + 2 * ph)
    x = clean + 0.30 * rng.normal(size=clean.shape)
    return x[:, :-1], x[:, 1:]


class AttnModel:
    def __init__(self, rng, d=16):
        self.P = rng.normal(0, 0.3, (T_SEQ, d))
        self.we = rng.normal(0, 0.3, d)
        self.Wq = rng.normal(0, 1 / np.sqrt(d), (d, d))
        self.Wk = rng.normal(0, 1 / np.sqrt(d), (d, d))
        self.s = np.array([1.0])
        self.b = np.array([0.0])
        self.d = d
        self.mask = np.triu(np.ones((T_SEQ, T_SEQ), bool), 1)

    def arrays(self):
        return [self.P, self.we, self.Wq, self.Wk, self.s, self.b]

    def forward(self, X):
        E = self.P[None] + X[..., None] * self.we[None, None]
        Q = E @ self.Wq.T
        K = E @ self.Wk.T
        S = Q @ K.transpose(0, 2, 1) / np.sqrt(self.d)
        S = np.where(self.mask[None], -1e9, S)
        S -= S.max(axis=2, keepdims=True)
        Aw = np.exp(S)
        Aw /= Aw.sum(axis=2, keepdims=True)
        z = (Aw @ X[..., None])[..., 0]
        y = self.s[0] * z + self.b[0]
        return y, (E, Q, K, Aw, z)

    def grads(self, X, Y, cache, y, w):
        E, Q, K, Aw, z = cache
        dy = 2 * (y - Y) * w / w.sum()
        ds = np.sum(dy * z)
        db = np.sum(dy)
        dz = dy * self.s[0]
        dA = dz[..., None] * X[:, None, :]
        dS = Aw * (dA - np.sum(dA * Aw, axis=2, keepdims=True))
        dQ = dS @ K / np.sqrt(self.d)
        dK = dS.transpose(0, 2, 1) @ Q / np.sqrt(self.d)
        dWq = np.einsum("bti,btj->ij", dQ, E)
        dWk = np.einsum("bti,btj->ij", dK, E)
        dE = dQ @ self.Wq + dK @ self.Wk
        dP = dE.sum(axis=0)
        dwe = np.einsum("btd,bt->d", dE, X)
        return [dP, dwe, dWq, dWk, np.array([ds]), np.array([db])]


def attention():
    rng = np.random.default_rng(11)
    model = AttnModel(rng)
    opt = Adam(model.arrays(), lr=3e-3)
    w = np.ones(T_SEQ)
    t0 = time.time()
    losses = []
    for it in range(4000):
        X, Y = _att_batch(rng, 64)
        y, cache = model.forward(X)
        W = np.broadcast_to(w, X.shape)
        losses.append(np.mean((y - Y) ** 2))
        opt.step(model.grads(X, Y, cache, y, W), lr=3e-3 if it < 3000 else 1e-3)
    print(f"attention: trained in {time.time() - t0:.1f} s, final batch MSE {np.mean(losses[-100:]):.4f}")
    # test
    rt = np.random.default_rng(99)
    Xt, Yt = _att_batch(rt, 4000)
    yt, cache = model.forward(Xt)
    Aw = cache[3]
    sl = slice(32, T_SEQ)
    rmse_att = np.sqrt(np.mean((yt[:, sl] - Yt[:, sl]) ** 2))
    rmse_pers = np.sqrt(np.mean((Xt[:, sl] - Yt[:, sl]) ** 2))
    lag = np.arange(T_SEQ)
    ysea = Xt[:, 32 - 15:T_SEQ - 15]
    rmse_sea = np.sqrt(np.mean((ysea - Yt[:, sl]) ** 2))
    print(f"attention: test RMSE (positions 32-47): attention {rmse_att:.3f}, persistence {rmse_pers:.3f}, "
          f"same phase one period earlier {rmse_sea:.3f}; noise sd 0.30")
    Amean = Aw.mean(axis=0)
    # mean weight by lag for queries 32..47 (lag = i - j; predicted sample is i+1)
    lagw = np.zeros(T_SEQ)
    for i in range(32, T_SEQ):
        for j in range(i + 1):
            lagw[i - j] += Amean[i, j]
    lagw /= (T_SEQ - 32)
    top = np.argsort(lagw)[::-1][:4]
    print("attention: top lags (i-j) and weights:", [(int(k), round(float(lagw[k]), 3)) for k in top],
          f"; weight at lags 15+31+47: {lagw[15] + lagw[31] + lagw[47]:.2f}")

    fig = plt.figure(figsize=(7.0, 4.8))
    gs = fig.add_gridspec(2, 2, height_ratios=[0.8, 1.25], width_ratios=[1, 1.05], hspace=0.42, wspace=0.42)
    ax = fig.add_subplot(gs[0, :])
    k = 3
    tt = np.arange(T_SEQ)
    ax.axvspan(31.5, T_SEQ + 0.5, color=LIGHT, zorder=0)
    ax.plot(tt, Xt[k], "o-", ms=2.4, lw=0.9, color=GREY, label="noisy telemetry x$_t$")
    ax.plot(tt + 1, yt[k], "-", lw=1.6, color=ORANGE, label="attention prediction of x$_{t+1}$")
    ax.text(40, 0.97, "scored positions", fontsize=6.2, color=NAVY, ha="center", va="top",
            transform=ax.get_xaxis_transform())
    ax.set_xlabel("time step t (period = 16 steps)", labelpad=1)
    ax.set_ylabel("value")
    ax.legend(fontsize=6.2, loc="upper left", ncol=2)
    ax.set_xlim(-1, T_SEQ + 1)
    ax.set_ylim(Xt[k].min() - 0.3, Xt[k].max() + 1.2)
    ttl(ax, "a", "One test sequence")
    ax = fig.add_subplot(gs[1, 0])
    im = ax.imshow(Amean, cmap="Blues", vmin=0, vmax=0.3, origin="upper")
    ax.set_xlabel("key position j (attended to)")
    ax.set_ylabel("query position i (predicts x$_{i+1}$)")
    ax.grid(False)
    ax.text(34, 7, "future positions\nmasked (causal)", fontsize=6.0, color=GREY, ha="center")
    ax.annotate("one period back\n(i − j = 15)", xy=(21, 36), xytext=(31, 21), fontsize=6.0, color=ORANGE,
                ha="center", arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7))
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, extend="max")
    cb.set_label("mean attention weight", fontsize=6.6)
    cb.ax.tick_params(labelsize=6.2)
    ttl(ax, "b", "Learned attention matrix")
    ax = fig.add_subplot(gs[1, 1])
    ax.bar(lag, lagw, color=[ORANGE if k in (15, 31, 47) else SKY for k in lag], width=0.8)
    ax.set_xlabel("look-back i − j (steps)")
    ax.set_ylabel("mean weight, queries 32–47")
    ax.set_xlim(-1, T_SEQ)
    ttl(ax, "c", "Where the trained head looks")
    foot(fig, "Single causal self-attention head (16-dimensional learned position embeddings plus a value "
              "embedding; queries and keys learned, values = raw samples) trained with Adam for 4 000 steps on random "
              "noisy two-harmonic signals (noise s.d. 0.30). The model was told nothing about the period.", width=150)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.16)
    save(fig, "ch44_attention")
    return rmse_att, rmse_pers, rmse_sea


def attcost():
    """Worked-example numbers: transformer layer cost vs sequence length (printed only)."""
    d = 768
    for n in [196, 1024, 4096, 16384]:
        lin = 24 * n * d ** 2
        att = 4 * n ** 2 * d
        mem = n ** 2 * 12 * 2 / 1e6
        print(f"attcost: n={n}: linear {lin / 1e9:.1f} GFLOP, attention {att / 1e9:.1f} GFLOP, "
              f"share {att / (att + lin) * 100:.0f} %, scores 12 heads 16-bit {mem:.0f} MB/layer")


# ==============================================================================================
# 6. Icosahedral multi-mesh (GraphCast-style) and message passing
# ==============================================================================================
def _icosphere(levels):
    p = (1 + 5 ** 0.5) / 2
    V = np.array([[-1, p, 0], [1, p, 0], [-1, -p, 0], [1, -p, 0], [0, -1, p], [0, 1, p], [0, -1, -p], [0, 1, -p],
                  [p, 0, -1], [p, 0, 1], [-p, 0, -1], [-p, 0, 1]], float)
    V /= np.linalg.norm(V, axis=1)[:, None]
    F = [[0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11], [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6],
         [7, 1, 8], [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9], [4, 9, 5], [2, 4, 11], [6, 2, 10],
         [8, 6, 7], [9, 8, 1]]
    verts = [tuple(v) for v in V]
    out = []
    faces = F
    for lev in range(levels + 1):
        edges = set()
        for a, b, c in faces:
            for u, v in ((a, b), (b, c), (c, a)):
                edges.add((min(u, v), max(u, v)))
        out.append((np.array(verts), np.array(sorted(edges)), len(faces)))
        if lev == levels:
            break
        cache = {}

        def mid(u, v):
            key = (min(u, v), max(u, v))
            if key not in cache:
                m = (np.array(verts[u]) + np.array(verts[v])) / 2
                m /= np.linalg.norm(m)
                verts.append(tuple(m))
                cache[key] = len(verts) - 1
            return cache[key]
        nf = []
        for a, b, c in faces:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            nf += [[a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]]
        faces = nf
    return out


def _ortho(V, lat0=25, lon0=20):
    la, lo = np.deg2rad(lat0), np.deg2rad(lon0)
    R1 = np.array([[np.cos(lo), np.sin(lo), 0], [-np.sin(lo), np.cos(lo), 0], [0, 0, 1]])
    R2 = np.array([[np.cos(la), 0, np.sin(la)], [0, 1, 0], [-np.sin(la), 0, np.cos(la)]])
    W = V @ R1.T @ R2.T
    return W[:, 1], W[:, 2], W[:, 0]       # x, y on screen, depth


def mesh():
    lv = _icosphere(6)
    R = 6371.0
    print("mesh: level, nodes, faces, edges, mean edge km")
    stats = []
    tot_edges = 0
    for r, (V, E, nf) in enumerate(lv):
        ang = np.arccos(np.clip(np.sum(V[E[:, 0]] * V[E[:, 1]], axis=1), -1, 1))
        tot_edges += len(E)
        stats.append((r, len(V), nf, len(E), ang.mean() * R))
        print(f"mesh: {r} {len(V)} {nf} {len(E)} {ang.mean() * R:.0f}")
    print(f"mesh: multimesh undirected edges {tot_edges}, directed {2 * tot_edges}")
    fig = plt.figure(figsize=(7.0, 3.0))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.1], wspace=0.15)
    cols = [RED, ORANGE, BLUE, GREY]
    for p, (levels, title) in enumerate([((0, 1, 2), "Multi-mesh: levels 0–2 overlaid"),
                                         ((4,), "Level 4: 2 562 nodes")]):
        ax = fig.add_subplot(gs[0, p])
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(Circle((0, 0), 1, fc="#EEF4FA", ec="#9AB", lw=0.8, zorder=0))
        for li in sorted(levels, reverse=True):
            V, E, _ = lv[li]
            x, y, z = _ortho(V)
            vis = (z[E[:, 0]] > -0.05) & (z[E[:, 1]] > -0.05)
            col = cols[min(li, 2)] if len(levels) > 1 else BLUE
            lw = {0: 1.6, 1: 1.1, 2: 0.6}.get(li, 0.35)
            for a, b in E[vis]:
                # draw great-circle arc
                tt = np.linspace(0, 1, 12)[:, None]
                arc = V[a] * (1 - tt) + V[b] * tt
                arc /= np.linalg.norm(arc, axis=1)[:, None]
                ax_, ay_, az_ = _ortho(arc)
                ax.plot(ax_, ay_, color=col, lw=lw, zorder=2 + (3 - min(li, 3)))
            if len(levels) == 1:
                vv = z > 0
                ax.plot(x[vv], y[vv], ".", ms=1.2, color=NAVY, zorder=5)
        if len(levels) > 1:
            for li, lab in zip((0, 1, 2), ("level 0: 12 nodes", "level 1: 42", "level 2: 162")):
                ax.plot([], [], color=cols[li], lw={0: 1.6, 1: 1.1, 2: 0.6}[li], label=lab)
            ax.legend(fontsize=6.0, loc="lower center", bbox_to_anchor=(0.5, -0.17), ncol=3, handlelength=1.2,
                      columnspacing=0.8)
        ax.set_xlim(-1.08, 1.08)
        ax.set_ylim(-1.08, 1.08)
        ax.set_title(title, fontsize=8.0)
        panel_tag(ax, "ab"[p], x=0.02, y=1.0)
    # (c) message passing schematic
    ax = fig.add_subplot(gs[0, 2])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    cx, cy = 5.0, 5.6
    nb = [(2.0, 8.3), (8.0, 8.3), (9.0, 4.6), (6.6, 3.0), (1.6, 4.0)]
    for k, (x, y) in enumerate(nb):
        ax.plot([x, cx], [y, cy], color=GREY, lw=0.9, zorder=1)
        arrow(ax, (x + (cx - x) * 0.18, y + (cy - y) * 0.18), (x + (cx - x) * 0.72, y + (cy - y) * 0.72), lw=1.0, ms=7,
              color=ORANGE)
        ax.add_patch(Circle((x, y), 0.55, fc=SKY, ec=NAVY, lw=0.8, zorder=3))
        ax.text(x, y, f"$h_{k + 1}$", fontsize=6.4, ha="center", va="center", zorder=4)
    ax.add_patch(Circle((cx, cy), 0.75, fc=BLUE, ec=NAVY, lw=1.0, zorder=3))
    ax.text(cx, cy, "$h_i$", fontsize=7.4, ha="center", va="center", color="white", zorder=4)
    ax.text(5.0, 9.9, "Message passing at node i", fontsize=8.0, weight="bold", ha="center", va="top", color=INK)
    ax.text(5.0, 0.75, r"$m_{ij} = \phi(h_i, h_j, e_{ij})$" + "\n" + r"$h_i \leftarrow \psi\left(h_i, \sum_{j} m_{ij}\right)$",
            fontsize=7.0, ha="center", va="center", color=NAVY, linespacing=1.5)
    ax.text(7.6, 6.9, "messages", fontsize=6.0, color=ORANGE, ha="left")
    panel_tag(ax, "c", x=0.02, y=1.0)
    foot(fig, f"Computed: a regular icosahedron refined by splitting each triangle into four; level 6 has "
              f"{stats[6][1]:,} nodes ({stats[6][2]:,} faces, mean edge {stats[6][4]:.0f} km) — the finest level of "
              f"GraphCast's mesh. Level-0 edges are about {stats[0][4]:,.0f} km long, so a few message-passing steps "
              f"on the multi-mesh carry information across the globe.".replace(",", " "), width=150)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.92, bottom=0.17)
    save(fig, "ch44_mesh")


# ==============================================================================================
# 7. A 2-D diffusion model (DDPM) trained in numpy
# ==============================================================================================
N_MODES, R_RING, S_MODE = 8, 2.0, 0.12


def _ring_data(rng, n):
    k = rng.integers(0, N_MODES, n)
    ang = 2 * np.pi * k / N_MODES
    return np.c_[R_RING * np.cos(ang), R_RING * np.sin(ang)] + S_MODE * rng.normal(size=(n, 2))


def _temb(t, T, dim=16):
    half = dim // 2
    fr = np.exp(-np.log(1000.0) * np.arange(half) / half)
    a = (t[:, None] / T) * 1000.0 * fr[None] / 10.0
    return np.c_[np.sin(a), np.cos(a)]


def diffusion():
    rng = np.random.default_rng(7)
    T = 100
    betas = np.linspace(1e-4, 0.12, T)
    alphas = 1 - betas
    abar = np.cumprod(alphas)
    print(f"diffusion: alpha-bar_T = {abar[-1]:.2e}")
    params = mlp_init([2 + 16, 128, 128, 128, 2], rng, kind="silu", gain=1.0)
    opt = Adam(flat(params), lr=2e-3)
    t0 = time.time()
    losses = []
    steps = 9000
    for it in range(steps):
        x0 = _ring_data(rng, 512)
        t = rng.integers(0, T, 512)
        eps = rng.normal(size=x0.shape)
        xt = np.sqrt(abar[t])[:, None] * x0 + np.sqrt(1 - abar[t])[:, None] * eps
        inp = np.c_[xt, _temb(t.astype(float), T)]
        out, cache = mlp_forward(params, inp, "silu")
        losses.append(np.mean((out - eps) ** 2))
        g, _ = mlp_backward(params, cache, 2 * (out - eps) / out.size, "silu")
        lr = 2e-3 if it < 6000 else 5e-4
        opt.step(flat(g), lr=lr)
    print(f"diffusion: trained {steps} steps in {time.time() - t0:.1f} s; final loss {np.mean(losses[-200:]):.3f}")
    # sampling
    rs = np.random.default_rng(123)
    n = 4000
    x = rs.normal(size=(n, 2))
    snaps = {T: x.copy()}
    for t in range(T - 1, -1, -1):
        tt = np.full(n, t, float)
        epsp, _ = mlp_forward(params, np.c_[x, _temb(tt, T)], "silu")
        mean = (x - betas[t] / np.sqrt(1 - abar[t]) * epsp) / np.sqrt(alphas[t])
        if t > 0:
            sig = np.sqrt(betas[t] * (1 - abar[t - 1]) / (1 - abar[t]))
            x = mean + sig * rs.normal(size=x.shape)
        else:
            x = mean
        if t in (60, 30, 10, 0):
            snaps[t] = x.copy()
    # quality: distance to nearest mode centre
    cen = np.c_[R_RING * np.cos(2 * np.pi * np.arange(N_MODES) / N_MODES),
                R_RING * np.sin(2 * np.pi * np.arange(N_MODES) / N_MODES)]
    dist = np.linalg.norm(x[:, None] - cen[None], axis=2)
    near = dist.min(axis=1)
    lab = dist.argmin(axis=1)
    within = np.mean(near < 3 * S_MODE)
    counts = np.bincount(lab[near < 3 * S_MODE], minlength=N_MODES)
    ref = _ring_data(np.random.default_rng(5), n)
    dref = np.linalg.norm(ref[:, None] - cen[None], axis=2).min(axis=1)
    print(f"diffusion: samples within 3 sigma of a mode: {within * 100:.1f} % (training data {np.mean(dref < 3 * S_MODE) * 100:.1f} %);"
          f" per-mode share min {counts.min() / counts.sum() * 100:.1f} %, max {counts.max() / counts.sum() * 100:.1f} %")
    fig, axs = plt.subplots(1, 6, figsize=(7.0, 2.25), gridspec_kw=dict(width_ratios=[1, 1, 1, 1, 1, 1.25]))
    show = [("Training data", ref, GREY), ("t = 100: pure noise", snaps[T], NAVY), ("t = 60", snaps[60], NAVY),
            ("t = 30", snaps[30], NAVY), ("t = 0: samples", snaps[0], ORANGE)]
    for k, (title, pts, col) in enumerate(show):
        ax = axs[k]
        ax.scatter(pts[:1500, 0], pts[:1500, 1], s=0.6, color=col, alpha=0.5, lw=0)
        ax.set_xlim(-3.3, 3.3)
        ax.set_ylim(-3.3, 3.3)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=7.0, weight="normal")
        panel_tag(ax, "abcde"[k], x=0.02, y=1.0)
    for k in range(1, 4):
        axs[k].annotate("", xy=(1.13, 0.5), xytext=(1.0, 0.5), xycoords="axes fraction",
                        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.9))
    ax = axs[5]
    sm = np.convolve(losses, np.ones(100) / 100, mode="valid")
    ax.plot(np.arange(len(sm)) + 100, sm, color=BLUE, lw=1.0)
    ax.set_xlabel("training step", fontsize=6.6, labelpad=1)
    ax.set_ylabel("noise-prediction MSE", fontsize=6.6, labelpad=1)
    ax.tick_params(labelsize=6.0)
    ax.set_ylim(0.25, 0.75)
    ax.set_xticks([0, 4000, 8000])
    ax.set_title("Training loss", fontsize=7.0, weight="normal")
    panel_tag(ax, "f", x=-0.05, y=1.0)
    foot(fig, f"Numpy DDPM: noise predictor 18-128-128-128-2 (SiLU), sinusoidal time embedding, T = 100 steps, "
              f"linear β from 10⁻⁴ to 0.12, {steps:,} Adam steps on a ring of eight Gaussians. "
              f"{within * 100:.0f} % of 4 000 generated samples lie within 3σ of a mode; every mode is "
              f"populated ({counts.min() / counts.sum() * 100:.0f}–{counts.max() / counts.sum() * 100:.0f} % each)."
         .replace(",", " "), width=150)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.87, bottom=0.31, wspace=0.22)
    pos = axs[5].get_position()
    axs[5].set_position([pos.x0 + 0.04, pos.y0 + 0.06, pos.width - 0.04, pos.height - 0.06])
    save(fig, "ch44_diffusion")


# ==============================================================================================
# 8. Foundation-model pipeline (block diagram)
# ==============================================================================================
def fmpipeline():
    fig, ax = canvas(7.0, 3.9, xlim=(0, 100), ylim=(0, 56))
    # column headers
    heads = [(10.5, "1  Unlabelled data"), (35.5, "2  Self-supervised\npre-training"),
             (59.5, "3  Foundation model"), (85, "4  Adapt with few labels")]
    for x, t in heads:
        ax.text(x, 55, t, fontsize=7.6, weight="bold", color=NAVY, ha="center", va="top", linespacing=1.1)
    data = ["Optical time series\n(Landsat, Sentinel-2)", "Radar (Sentinel-1)", "Reanalysis\n(ERA5, MERRA-2)",
            "Solar images (SDO)", "Text, code, manuals"]
    ys = [43.5, 36.0, 28.5, 21.0, 13.5]
    for t, y in zip(data, ys):
        box(ax, 1, y - 3, 19, 6.2, text=t, fs=5.9, fc="white", ec=BLUE, r=0.6)
    ax.text(10.5, 8.6, "terabytes to petabytes,\nno labels needed", fontsize=5.8, color=GREY, ha="center", va="top",
            style="italic")
    # pre-training box
    title_box(ax, 25, 15, 21, 32, "Pretext task", "", fs=5.9)
    ax.text(35.5, 39.5, "mask 75 % of patches,\nreconstruct them", fontsize=5.9, ha="center", va="center")
    ax.text(35.5, 31.5, "or: match two views of\nthe same place (contrastive)", fontsize=5.9, ha="center",
            va="center")
    ax.text(35.5, 23.5, "or: predict the next\nstep / next token", fontsize=5.9, ha="center", va="center")
    ax.text(35.5, 17.6, "10⁴–10⁵ GPU-hours", fontsize=5.9, ha="center", va="center", color=ORANGE, weight="bold")
    for y in ys:
        arrow(ax, (20.2, y + 0.1), (24.8, 31), lw=0.6, ms=5, color=GREY)
    arrow(ax, (46.2, 31), (50.5, 31), lw=1.1, ms=8)
    # foundation model: encoder stack
    box(ax, 51, 19, 17, 24, fc="#DCE8F4", ec=NAVY, r=0.8)
    for k in range(5):
        box(ax, 53, 21.5 + k * 4.0, 13, 2.8, text="transformer block" if k else "patch embedding", fs=5.6,
            fc="white", ec=BLUE, r=0.4)
    ax.text(59.5, 16.6, "encoder weights\n(10⁸–10⁹ parameters)", fontsize=5.8, ha="center", va="top", color=NAVY)
    ax.text(59.5, 46.0, "embeddings: a vector\nper pixel, patch or day", fontsize=5.8, ha="center", va="bottom",
            color=VIOLET)
    # adaptation options
    opts = [("Frozen embeddings +\nsmall classifier (probe)", 43.5, GREEN),
            ("Low-rank adapters (LoRA):\ntrain ~1 % of weights", 33.5, BLUE),
            ("Full fine-tuning:\nall weights + task head", 23.5, VIOLET)]
    for t, y, c in opts:
        box(ax, 72, y - 3.5, 26, 7.2, text=t, fs=5.9, fc="white", ec=c, r=0.6, lw=1.1)
        arrow(ax, (68.2, 31), (71.8, y), lw=0.8, ms=6, color=c)
    ax.text(85, 15.6, "tasks: flood and burn-scar maps,\ncrop types, flare forecasts,\ndocument search",
            fontsize=5.8, ha="center", va="center", color=INK)
    ax.text(85, 8.8, "10–10 000 labelled examples", fontsize=5.9, ha="center", va="center", color=ORANGE,
            weight="bold")
    # feedback
    ax.annotate("", xy=(35.5, 12.8), xytext=(85, 5.6),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.9, connectionstyle="arc3,rad=-0.12",
                                mutation_scale=8, linestyle="--"))
    ax.text(57, 3.2, "evaluate against a task-specific baseline (e.g. U-Net); new data and errors feed the next "
                     "version", fontsize=5.8, color=GREY, ha="center", style="italic")
    save(fig, "ch44_fmpipeline")


# ==============================================================================================
# 9. Neural surrogate of atmospheric density (US Standard Atmosphere 1976 + exponential segments)
# ==============================================================================================
US76 = [(0.0, 288.15, -6.5, 101325.0), (11.0, 216.65, 0.0, 22632.06), (20.0, 216.65, 1.0, 5474.889),
        (32.0, 228.65, 2.8, 868.0187), (47.0, 270.65, 0.0, 110.9063), (51.0, 270.65, -2.8, 66.93887),
        (71.0, 214.65, -2.0, 3.956420)]
EXPO = [(80, 1.905e-5, 5.799), (90, 3.396e-6, 5.382), (100, 5.297e-7, 5.877), (110, 9.661e-8, 7.263),
        (120, 2.438e-8, 9.473), (130, 8.484e-9, 12.636), (140, 3.845e-9, 16.149), (150, 2.070e-9, 22.523),
        (180, 5.464e-10, 29.740), (200, 2.789e-10, 37.105), (250, 7.248e-11, 45.546), (300, 2.418e-11, 53.628),
        (350, 9.518e-12, 53.298), (400, 3.725e-12, 58.515), (450, 1.585e-12, 60.828), (500, 6.967e-13, 63.822),
        (600, 1.454e-13, 71.835), (700, 3.614e-14, 88.667), (800, 1.170e-14, 124.64), (900, 5.245e-15, 181.05),
        (1000, 3.019e-15, 268.00)]


def density_model(h_km):
    """US Standard Atmosphere 1976 (0-86 km, closed form per layer) and exponential segments above 86 km."""
    h = np.atleast_1d(np.asarray(h_km, float))
    rho = np.empty_like(h)
    low = h <= 86.0
    if low.any():
        r0, g0, M, Rg = 6356.766, 9.80665, 0.0289644, 8.31432
        Hp = r0 * h[low] / (r0 + h[low])
        bases = np.array([b[0] for b in US76])
        k = np.clip(np.searchsorted(bases, Hp, side="right") - 1, 0, len(US76) - 1)
        Hb = bases[k]
        Tb = np.array([b[1] for b in US76])[k]
        Lb = np.array([b[2] for b in US76])[k] / 1000.0
        Pb = np.array([b[3] for b in US76])[k]
        T = Tb + Lb * (Hp - Hb) * 1000.0
        with np.errstate(divide="ignore", invalid="ignore"):
            P_iso = Pb * np.exp(-g0 * M * (Hp - Hb) * 1000.0 / (Rg * Tb))
            P_grad = Pb * (Tb / T) ** (g0 * M / (Rg * np.where(Lb == 0, 1, Lb)))
        P = np.where(Lb == 0, P_iso, P_grad)
        rho[low] = P * M / (Rg * T)
    hi = ~low
    if hi.any():
        hb = np.array([e[0] for e in EXPO], float)
        k = np.clip(np.searchsorted(hb, h[hi], side="right") - 1, 0, len(EXPO) - 1)
        r0 = np.array([e[1] for e in EXPO])[k]
        H = np.array([e[2] for e in EXPO])[k]
        rho[hi] = r0 * np.exp(-(h[hi] - hb[k]) / H)
    return rho


def surrogate():
    h_tr = np.linspace(0, 600, 601)
    y_tr = np.log10(density_model(h_tr))
    hn = lambda h: (h - 300.0) / 300.0                            # noqa: E731
    ym, ys = y_tr.mean(), y_tr.std()
    # pure neural surrogate
    rng = np.random.default_rng(4)
    params = mlp_init([1, 32, 32, 1], rng, kind="tanh")
    opt = Adam(flat(params), lr=3e-3)
    X = hn(h_tr)[:, None]
    Y = ((y_tr - ym) / ys)[:, None]
    t0 = time.time()
    for it in range(12000):
        out, cache = mlp_forward(params, X, "tanh")
        g, _ = mlp_backward(params, cache, 2 * (out - Y) / len(Y), "tanh")
        opt.step(flat(g), lr=3e-3 if it < 8000 else 5e-4)
    # hybrid: physics baseline (log-linear fit to the top 100 km of the training range = constant scale height)
    # plus a neural correction
    sel = h_tr >= 500
    cf = np.polyfit(h_tr[sel], y_tr[sel], 1)
    base = lambda h: np.polyval(cf, h)                            # noqa: E731
    rs = y_tr - base(h_tr)
    rm, rsd = rs.mean(), rs.std()
    rng2 = np.random.default_rng(4)
    p2 = mlp_init([1, 32, 32, 1], rng2, kind="tanh")
    opt2 = Adam(flat(p2), lr=3e-3)
    Y2 = ((rs - rm) / rsd)[:, None]
    for it in range(12000):
        out, cache = mlp_forward(p2, X, "tanh")
        g, _ = mlp_backward(p2, cache, 2 * (out - Y2) / len(Y2), "tanh")
        opt2.step(flat(g), lr=3e-3 if it < 8000 else 5e-4)
    print(f"surrogate: trained two networks in {time.time() - t0:.1f} s; baseline scale height "
          f"{-1 / (cf[0] * np.log(10)):.1f} km")
    h = np.linspace(0, 1000, 2001)
    truth = np.log10(density_model(h))
    nn = mlp_forward(params, hn(h)[:, None], "tanh")[0][:, 0] * ys + ym
    hy = base(h) + mlp_forward(p2, hn(h)[:, None], "tanh")[0][:, 0] * rsd + rm
    err_nn = (10 ** (nn - truth) - 1) * 100
    err_hy = (10 ** (hy - truth) - 1) * 100
    tr = h <= 600
    for lab, e in [("NN", err_nn), ("hybrid", err_hy)]:
        print(f"surrogate: {lab}: training range median |err| {np.median(np.abs(e[tr])):.2f} %, "
              f"max {np.max(np.abs(e[tr])):.1f} %; at 800 km {e[np.argmin(abs(h - 800))]:.0f} %, "
              f"at 1000 km {e[-1]:.0f} %")
    # speed (one million altitudes, vectorised)
    hq = np.random.default_rng(0).uniform(0, 600, 1_000_000)
    tp, tn = [], []
    for _ in range(3):
        t0 = time.perf_counter()
        density_model(hq)
        tp.append(time.perf_counter() - t0)
        t0 = time.perf_counter()
        10 ** (mlp_forward(params, hn(hq)[:, None], "tanh")[0][:, 0] * ys + ym)
        tn.append(time.perf_counter() - t0)
    tp, tn = min(tp), min(tn)
    print(f"surrogate: 1e6 evaluations: physics model {tp * 1e3:.0f} ms, neural surrogate {tn * 1e3:.0f} ms")

    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.85), gridspec_kw=dict(width_ratios=[1.25, 1.25, 0.8]))
    ax = axs[0]
    ax.axhspan(600, 1000, color="#FBEDE3", zorder=0)
    ax.plot(truth, h, color=INK, lw=2.2, label="physics model")
    ax.plot(nn, h, color=RED, lw=1.3, ls="--", label="neural surrogate")
    ax.plot(hy, h, color=GREEN, lw=1.3, ls="-.", label="hybrid (physics + NN)")
    ax.text(-14.6, 940, "extrapolation", fontsize=6.4, color=ORANGE, ha="left", va="center")
    ax.text(-14.6, 560, "training range\n0–600 km", fontsize=6.4, color=NAVY, ha="left", va="center")
    ax.set_xlabel("log$_{10}$ density (kg/m³)")
    ax.set_ylabel("altitude (km)")
    ax.set_ylim(0, 1000)
    ax.set_xlim(-15, 1)
    ax.legend(fontsize=6.2, loc="upper right")
    ax.set_title("Density profile", fontsize=8.4)
    panel_tag(ax, "a")
    ax = axs[1]
    ax.axhspan(600, 1000, color="#FBEDE3", zorder=0)
    ax.plot(np.abs(err_nn) + 1e-3, h, color=RED, lw=1.2, ls="--", label="neural surrogate")
    ax.plot(np.abs(err_hy) + 1e-3, h, color=GREEN, lw=1.2, ls="-.", label="hybrid")
    ax.set_xscale("log")
    ax.set_xlim(1e-2, 1e5)
    ax.set_ylim(0, 1000)
    ax.set_xlabel("density error (%)")
    ax.set_ylabel("altitude (km)")
    ax.legend(fontsize=6.2, loc="lower right")
    ax.set_title("Error vs physics model", fontsize=8.4)
    panel_tag(ax, "b")
    ax = axs[2]
    bars = ax.bar([0, 1], [tp * 1e3, tn * 1e3], color=[INK, RED], width=0.6)
    for b, v in zip(bars, [tp * 1e3, tn * 1e3]):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.03, f"{v:.0f} ms", ha="center", va="bottom", fontsize=6.6)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["physics\nmodel", "neural\nsurrogate"], fontsize=6.8)
    ax.set_ylabel("time for 10⁶ evaluations (ms)")
    ax.set_ylim(0, max(tp, tn) * 1e3 * 1.25)
    ax.set_title("Speed (this case)", fontsize=8.4)
    panel_tag(ax, "c")
    foot(fig, "Physics model: US Standard Atmosphere 1976 below 86 km and exponential segments (Vallado) to 1 000 km. "
              "Surrogates: numpy MLP 1-32-32-1 (tanh), 12 000 Adam steps on 601 altitudes, 0–600 km; hybrid = "
              "constant-scale-height fit to 500–600 km plus a learned correction. Timings: one CPU core, vectorised.",
         width=150)
    fig.tight_layout(rect=(0, 0.08, 1, 1), w_pad=1.0)
    save(fig, "ch44_surrogate")


# ==============================================================================================
# 10. Uncertainty: deep ensemble and split conformal prediction
# ==============================================================================================
def _uq_f(x):
    return np.sin(1.3 * x) + 0.25 * x


def _uq_sigma(x):
    return 0.08 + 0.06 * x


def _uq_data(rng, n, lo=0.0, hi=7.0):
    x = rng.uniform(lo, hi, n)
    return x, _uq_f(x) + _uq_sigma(x) * rng.normal(size=n)


def uq():
    rng = np.random.default_rng(21)
    xtr, ytr = _uq_data(rng, 600)
    xcal, ycal = _uq_data(rng, 400)
    xte, yte = _uq_data(rng, 4000)
    xood, yood = _uq_data(rng, 2000, 7.0, 10.0)
    xs = lambda x: ((x - 3.5) / 2.0)[:, None]                         # noqa: E731
    members = []
    t0 = time.time()
    for m in range(5):
        r = np.random.default_rng(100 + m)
        p = mlp_init([1, 64, 64, 2], r, kind="tanh")
        opt = Adam(flat(p), lr=3e-3)
        X, Y = xs(xtr), ytr[:, None]
        for it in range(6000):
            out, cache = mlp_forward(p, X, "tanh")
            mu, s = out[:, :1], out[:, 1:]
            var = np.log1p(np.exp(s)) + 1e-4
            dmu = (mu - Y) / var
            dvar = 0.5 / var - 0.5 * (mu - Y) ** 2 / var ** 2
            ds = dvar / (1 + np.exp(-s))
            warm = it < 1500
            if warm:
                dmu, ds = 2 * (mu - Y), 0 * ds
            g, _ = mlp_backward(p, cache, np.c_[dmu, ds] / len(Y), "tanh")
            opt.step(flat(g), lr=3e-3 if it < 4500 else 1e-3)
        members.append(p)
    print(f"uq: trained 5 members in {time.time() - t0:.1f} s")

    def predict(x):
        mus, vars_ = [], []
        for p in members:
            out, _ = mlp_forward(p, xs(x), "tanh")
            mus.append(out[:, 0])
            vars_.append(np.log1p(np.exp(out[:, 1])) + 1e-4)
        mus, vars_ = np.array(mus), np.array(vars_)
        mu = mus.mean(0)
        epi = mus.var(0)
        ale = vars_.mean(0)
        return mu, epi, ale

    z90 = 1.6449
    mu_c, epi_c, ale_c = predict(xcal)
    # split conformal on normalised residuals
    sc = np.abs(ycal - mu_c) / np.sqrt(epi_c + ale_c)
    ncal = len(sc)
    q = np.quantile(sc, np.ceil((ncal + 1) * 0.9) / ncal, method="higher")
    # plain split conformal (absolute residuals)
    qa = np.quantile(np.abs(ycal - mu_c), np.ceil((ncal + 1) * 0.9) / ncal, method="higher")
    res = {}
    for name, (x, y) in {"in": (xte, yte), "ood": (xood, yood)}.items():
        mu, epi, ale = predict(x)
        sd = np.sqrt(epi + ale)
        res[name] = dict(
            epi_only=np.mean(np.abs(y - mu) <= z90 * np.sqrt(epi)),
            ens=np.mean(np.abs(y - mu) <= z90 * sd),
            conf_abs=np.mean(np.abs(y - mu) <= qa),
            conf_norm=np.mean(np.abs(y - mu) <= q * sd),
            width_ens=np.mean(2 * z90 * sd), width_abs=2 * qa, width_norm=np.mean(2 * q * sd))
        print(f"uq: {name}: coverage at 90 % nominal: ensemble spread only {res[name]['epi_only'] * 100:.1f} %, "
              f"ensemble total {res[name]['ens'] * 100:.1f} %, conformal (abs) {res[name]['conf_abs'] * 100:.1f} %, "
              f"conformal (normalised) {res[name]['conf_norm'] * 100:.1f} %; mean widths ens {res[name]['width_ens']:.2f},"
              f" abs {res[name]['width_abs']:.2f}, norm {res[name]['width_norm']:.2f}")
    xg = np.linspace(0, 10, 500)
    mu, epi, ale = predict(xg)
    sd = np.sqrt(epi + ale)
    print(f"uq: epistemic sd at x=3.5: {np.sqrt(epi[np.argmin(abs(xg - 3.5))]):.3f}, at x=9.5: "
          f"{np.sqrt(epi[np.argmin(abs(xg - 9.5))]):.3f}; q_norm = {q:.3f}")

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.9), gridspec_kw=dict(width_ratios=[1.6, 1]))
    ax = axs[0]
    ax.axvspan(7, 10, color="#FBEDE3", zorder=0)
    ax.scatter(xtr, ytr, s=2, color=GREY, alpha=0.6, lw=0, label="training data")
    ax.scatter(xood[:300], yood[:300], s=2, color=RED, alpha=0.6, lw=0, label="new data outside range")
    ax.fill_between(xg, mu - q * sd, mu + q * sd, color=SKY, alpha=0.35, lw=0, label="90 % conformal band")
    ax.fill_between(xg, mu - z90 * np.sqrt(epi), mu + z90 * np.sqrt(epi), color=VIOLET, alpha=0.45, lw=0,
                    label="ensemble spread only (±1.645σ)")
    ax.plot(xg, _uq_f(xg), color=INK, lw=0.9, ls=":", label="true mean")
    ax.plot(xg, mu, color=NAVY, lw=1.3, label="ensemble mean")
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.2, 4.8)
    ax.set_xlabel("input x (e.g. a driver such as solar-wind speed, scaled)")
    ax.set_ylabel("target y")
    ax.legend(fontsize=5.9, loc="upper left", ncol=2, handlelength=1.4, columnspacing=0.8)
    ax.text(8.5, -0.9, "outside training\nrange", fontsize=6.2, color=ORANGE, ha="center")
    ax.set_title("Deep ensemble with conformal intervals", fontsize=8.4)
    panel_tag(ax, "a")
    ax = axs[1]
    names = ["ensemble\nspread only", "ensemble\n(total var.)", "conformal\n(absolute)", "conformal\n(normalised)"]
    keys = ["epi_only", "ens", "conf_abs", "conf_norm"]
    xx = np.arange(4)
    ax.bar(xx - 0.19, [res["in"][k] * 100 for k in keys], width=0.36, color=BLUE, label="in range")
    ax.bar(xx + 0.19, [res["ood"][k] * 100 for k in keys], width=0.36, color=RED, label="outside range")
    ax.axhline(90, color=INK, lw=0.9, ls="--")
    ax.text(3.6, 91, "target 90 %", fontsize=6.0, ha="right", va="bottom")
    ax.set_xticks(xx)
    ax.set_xticklabels(names, fontsize=6.0)
    ax.set_ylabel("measured coverage (%)")
    ax.set_ylim(0, 105)
    ax.legend(fontsize=6.2, loc="lower right")
    ax.set_title("Coverage check", fontsize=8.4)
    panel_tag(ax, "b")
    foot(fig, "Synthetic regression y = sin(1.3x) + 0.25x with noise s.d. rising from 0.08 to 0.50. Five numpy MLPs "
              "(1-64-64-2, tanh) trained on 600 points with the Gaussian negative log-likelihood; conformal quantiles "
              "from 400 calibration points; coverage measured on 4 000 in-range and 2 000 out-of-range test points.",
         width=150)
    fig.tight_layout(rect=(0, 0.08, 1, 1), w_pad=1.2)
    save(fig, "ch44_uq")


# ==============================================================================================
# 11. Explainability: input-gradient saliency reveals a shortcut ("Clever Hans")
# ==============================================================================================
IMG = 24


def _chips(rng, n, cue_prob):
    """Synthetic 24x24 radar-like chips: sea clutter; class 1 has a ship (bright elongated blob).
    A bright 'quay' strip along the left edge appears with probability cue_prob in ship chips and
    1 - cue_prob in empty chips (cue_prob = 0.5 means no correlation)."""
    X = rng.gamma(2.0, 0.5, (n, IMG, IMG))
    y = rng.integers(0, 2, n)
    yy, xx = np.mgrid[0:IMG, 0:IMG]
    pos = []
    for i in range(n):
        if y[i] == 1:
            cx, cy = rng.uniform(7, 19), rng.uniform(5, 19)
            th = rng.uniform(0, np.pi)
            u = (xx - cx) * np.cos(th) + (yy - cy) * np.sin(th)
            v = -(xx - cx) * np.sin(th) + (yy - cy) * np.cos(th)
            X[i] += 1.4 * np.exp(-(u / 2.6) ** 2 - (v / 0.9) ** 2)
            pos.append((cx, cy))
        else:
            pos.append((np.nan, np.nan))
        cue = rng.random() < (cue_prob if y[i] == 1 else 1 - cue_prob)
        if cue:
            X[i, :, :2] += 1.6
    return X.reshape(n, -1), y, np.array(pos)


def _train_clf(X, y, seed, epochs=60):
    rng = np.random.default_rng(seed)
    params = mlp_init([IMG * IMG, 64, 1], rng, kind="relu")
    opt = Adam(flat(params), lr=1e-3)
    mu, sd = X.mean(), X.std()
    for ep in range(epochs):
        idx = rng.permutation(len(X))
        for k in range(0, len(X), 128):
            b = idx[k:k + 128]
            out, cache = mlp_forward(params, (X[b] - mu) / sd)
            p = 1 / (1 + np.exp(-out[:, 0]))
            g, _ = mlp_backward(params, cache, ((p - y[b]) / len(b))[:, None])
            opt.step(flat(g))
    return params, mu, sd


def _predict(params, mu, sd, X):
    out, _ = mlp_forward(params, (X - mu) / sd)
    return 1 / (1 + np.exp(-out[:, 0]))


def _saliency(params, mu, sd, X):
    out, cache = mlp_forward(params, (X - mu) / sd)
    _, dx = mlp_backward(params, cache, np.ones_like(out))
    return dx / sd


def xai():
    rng = np.random.default_rng(31)
    Xb, yb, _ = _chips(rng, 6000, 0.95)        # biased training set: quay strip co-occurs with ships
    Xc, yc, _ = _chips(rng, 6000, 0.5)         # clean training set
    Xt, yt, pt = _chips(np.random.default_rng(77), 4000, 0.5)    # test: cue uncorrelated
    Xtb, ytb, _ = _chips(np.random.default_rng(78), 4000, 0.95)  # test drawn like the biased training set
    t0 = time.time()
    mb = _train_clf(Xb, yb, 1)
    mc = _train_clf(Xc, yc, 1)
    print(f"xai: trained two classifiers in {time.time() - t0:.1f} s")
    acc = {}
    for name, m in [("shortcut", mb), ("clean", mc)]:
        a_same = np.mean((_predict(*m, Xtb) > 0.5) == ytb)
        a_new = np.mean((_predict(*m, Xt) > 0.5) == yt)
        acc[name] = (a_same, a_new)
        print(f"xai: {name} model: accuracy on biased-like test {a_same * 100:.1f} %, on uncorrelated test "
              f"{a_new * 100:.1f} %")
    # mean |saliency| maps over ship test chips
    ship = yt == 1
    sb = np.abs(_saliency(*mb, Xt[ship])).mean(0).reshape(IMG, IMG)
    scl = np.abs(_saliency(*mc, Xt[ship])).mean(0).reshape(IMG, IMG)
    frac_b = sb[:, :2].sum() / sb.sum()
    frac_c = scl[:, :2].sum() / scl.sum()
    print(f"xai: share of saliency in the 2-pixel quay strip (8.3 % of pixels): shortcut {frac_b * 100:.0f} %, "
          f"clean {frac_c * 100:.0f} %")
    # one example: ship without quay strip
    cand = np.where((yt == 1) & (Xt.reshape(-1, IMG, IMG)[:, :, :2].mean(axis=(1, 2)) < 1.3))[0]
    pb = _predict(*mb, Xt[cand])
    k = cand[np.argmin(pb)]
    ex = Xt[k].reshape(IMG, IMG)
    s1 = np.abs(_saliency(*mb, Xt[k:k + 1])).reshape(IMG, IMG)
    s2 = np.abs(_saliency(*mc, Xt[k:k + 1])).reshape(IMG, IMG)
    p1, p2 = _predict(*mb, Xt[k:k + 1])[0], _predict(*mc, Xt[k:k + 1])[0]
    print(f"xai: example chip: P(ship) shortcut {p1:.2f}, clean {p2:.2f}")
    # an example training chip with quay
    Xd, ydd, _ = _chips(np.random.default_rng(5), 40, 0.95)
    kq = np.where(ydd == 1)[0][0]
    ke = np.where(ydd == 0)[0][0]

    fig = plt.figure(figsize=(7.0, 2.75))
    gs = fig.add_gridspec(2, 5, width_ratios=[1, 1, 1, 1, 1.55], hspace=0.45, wspace=0.12)
    imgs = [(gs[0, 0], Xd[kq].reshape(IMG, IMG), "train: ship + quay", "gray"),
            (gs[1, 0], Xd[ke].reshape(IMG, IMG), "train: sea only", "gray"),
            (gs[0, 1], sb, "shortcut model:\nmean saliency", "inferno"),
            (gs[1, 1], scl, "clean model:\nmean saliency", "inferno"),
            (gs[0, 2], ex, f"test ship, no quay", "gray"),
            (gs[0, 3], s1, f"shortcut: P(ship) = {p1:.2f}", "inferno"),
            (gs[1, 3], s2, f"clean: P(ship) = {p2:.2f}", "inferno")]
    for k_, (g, arr, title, cmap) in enumerate(imgs):
        ax = fig.add_subplot(g)
        ax.imshow(arr, cmap=cmap, vmin=0 if cmap == "inferno" else 0, vmax=np.percentile(arr, 99.5))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_title(title, fontsize=6.2, weight="normal", pad=2, linespacing=1.05)
    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    ax.text(0.5, 0.5, "saliency = |∂P/∂pixel|\n(input gradient)", fontsize=6.0, ha="center", va="center",
            color=GREY, transform=ax.transAxes)
    ax = fig.add_subplot(gs[:, 4])
    xx = np.arange(2)
    ax.bar(xx - 0.19, [acc["shortcut"][0] * 100, acc["clean"][0] * 100], width=0.36, color=SKY,
           label="test like training data")
    ax.bar(xx + 0.19, [acc["shortcut"][1] * 100, acc["clean"][1] * 100], width=0.36, color=ORANGE,
           label="test with quay uncorrelated")
    for i, key in enumerate(["shortcut", "clean"]):
        for j, v in enumerate(acc[key]):
            ax.text(i + (j - 0.5) * 0.38, v * 100 + 1, f"{v * 100:.0f}", fontsize=6.0, ha="center", va="bottom")
    ax.set_xticks(xx)
    ax.set_xticklabels(["trained on\nbiased data", "trained on\nclean data"], fontsize=6.4)
    ax.set_ylim(40, 108)
    ax.set_ylabel("accuracy (%)", fontsize=7)
    ax.tick_params(labelsize=6.4)
    ax.legend(fontsize=5.8, loc="upper center", ncol=1)
    ax.set_title("Accuracy", fontsize=7.6)
    foot(fig, "Synthetic 24 × 24-pixel radar-like chips (gamma sea clutter; ships = bright elongated blobs). In the biased "
              "training set a bright quay strip on the left edge accompanies 95 % of ships. Numpy MLP 576-64-1 (ReLU), "
              "60 Adam epochs on 6 000 chips; saliency averaged over ship chips of the uncorrelated test set.",
         width=150)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.88, bottom=0.17)
    save(fig, "ch44_xai")


if __name__ == "__main__":
    fns = [blocks, scaling, convmaps, cnnarch, attention, attcost, mesh, diffusion, fmpipeline, surrogate, uq, xai]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
