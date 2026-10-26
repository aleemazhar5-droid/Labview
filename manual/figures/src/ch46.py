"""Figures for Chapter 46 - AI for Earth Observation.

Most figures run real machine-learning or optimisation code with fixed random seeds on synthetic scenes built from
simple physical models: a random forest and a small numpy convolutional network for land cover, a learned change
detector, a numpy temporal-attention network for crop types, speckle filters (Lee, a least-squares linear filter and
a numpy network), CFAR versus a learned ship detector, Otsu thresholding versus a learned flood mapper, calibration
of the integrated-mass-enhancement method for methane plumes, Monte Carlo smart tasking under clouds, and domain shift
plus area estimation.  Numbers quoted in the chapter are printed by each function.
"""
import os
import sys
import textwrap
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch  # noqa: F401
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from scipy import ndimage as ndi

FOOT = 6.0


def panel_tag(ax, s, x=-0.02, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, weight="bold", ha="right", va="bottom", color=INK)


def foot(fig, text, y=0.01, width=150):
    fig.text(0.99, y, "\n".join(textwrap.wrap(text, width)), ha="right", va="bottom", fontsize=FOOT, color=GREY,
             multialignment="right", linespacing=1.25)


def img_axes(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color("#9AA5AF")
        s.set_linewidth(0.6)


# ==============================================================================================
# A small fully connected network written in numpy (ReLU hidden layers, softmax output, Adam).
class NumpyNet:
    def __init__(self, n_in, hidden, n_out, seed=0):
        rng = np.random.default_rng(seed)
        sizes = [n_in, *hidden, n_out]
        self.W = [rng.normal(0, np.sqrt(2.0 / sizes[i]), (sizes[i], sizes[i + 1])) for i in range(len(sizes) - 1)]
        self.b = [np.zeros(sizes[i + 1]) for i in range(len(sizes) - 1)]
        self.rng = rng

    def n_params(self):
        return int(sum(w.size + b.size for w, b in zip(self.W, self.b)))

    def forward(self, X):
        acts = [X]
        h = X
        for i, (w, b) in enumerate(zip(self.W, self.b)):
            z = h @ w + b
            h = np.maximum(z, 0) if i < len(self.W) - 1 else z
            acts.append(h)
        return acts

    def predict_proba(self, X, batch=20000):
        out = []
        for i in range(0, len(X), batch):
            z = self.forward(X[i:i + batch])[-1]
            z = z - z.max(1, keepdims=True)
            p = np.exp(z)
            out.append(p / p.sum(1, keepdims=True))
        return np.vstack(out)

    def predict_value(self, X, batch=20000):
        return np.vstack([self.forward(X[i:i + batch])[-1] for i in range(0, len(X), batch)])

    def fit(self, X, y, epochs=30, lr=2e-3, batch=256, wd=1e-4, regression=False, weights=None):
        m = [np.zeros_like(w) for w in self.W] + [np.zeros_like(b) for b in self.b]
        v = [np.zeros_like(w) for w in self.W] + [np.zeros_like(b) for b in self.b]
        t = 0
        n = len(X)
        for ep in range(epochs):
            perm = self.rng.permutation(n)
            for i in range(0, n, batch):
                idx = perm[i:i + batch]
                acts = self.forward(X[idx])
                z = acts[-1]
                if regression:
                    g = (z - y[idx]) / len(idx)
                else:
                    z = z - z.max(1, keepdims=True)
                    p = np.exp(z)
                    p /= p.sum(1, keepdims=True)
                    p[np.arange(len(idx)), y[idx]] -= 1
                    if weights is not None:
                        p *= weights[y[idx]][:, None]
                    g = p / len(idx)
                grads_w, grads_b = [], []
                for li in range(len(self.W) - 1, -1, -1):
                    grads_w.insert(0, acts[li].T @ g + wd * self.W[li])
                    grads_b.insert(0, g.sum(0))
                    if li > 0:
                        g = (g @ self.W[li].T) * (acts[li] > 0)
                t += 1
                params = self.W + self.b
                grads = grads_w + grads_b
                for k in range(len(params)):
                    m[k] = 0.9 * m[k] + 0.1 * grads[k]
                    v[k] = 0.999 * v[k] + 0.001 * grads[k] ** 2
                    mh = m[k] / (1 - 0.9 ** t)
                    vh = v[k] / (1 - 0.999 ** t)
                    params[k] -= lr * mh / (np.sqrt(vh) + 1e-8)
        return self


def patches(img, r, idx_rows, idx_cols):
    """Extract (2r+1)x(2r+1) patches of a (H, W, C) image (reflect padding) at the given pixels -> (n, k*k*C)."""
    pad = np.pad(img, ((r, r), (r, r), (0, 0)), mode="reflect")
    out = []
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out.append(pad[idx_rows + r + dy, idx_cols + r + dx, :])
    return np.concatenate(out, axis=1)


def f1_scores(y, p, k):
    cm = np.zeros((k, k), int)
    np.add.at(cm, (y, p), 1)
    prod = np.diag(cm) / np.maximum(cm.sum(1), 1)
    user = np.diag(cm) / np.maximum(cm.sum(0), 1)
    f1 = 2 * prod * user / np.maximum(prod + user, 1e-9)
    return cm, prod, user, f1


# ==============================================================================================
# 1. Pipeline block diagram
def pipeline():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 100), ylim=(3.5, 50))
    stages = [
        ("Sensor and\nsatellite", "Optical, radar,\nthermal,\nhyperspectral", NAVY, "TB per day"),
        ("On board", "Cloud screening,\ndetection,\ncompression", VIOLET, "GB–TB"),
        ("Ground\nprocessing", "Calibration,\ngeometry,\nanalysis-ready\ndata", BLUE, "PB archive"),
        ("Models", "Foundation\nencoder + head;\nor RF, U-Net,\ndetector", GREEN, "GPU hours"),
        ("Products", "Maps, alerts,\nobject lists,\nestimates with\nuncertainty", ORANGE, "MB–GB"),
        ("Users", "Agencies,\ninsurers, NGOs,\nfarmers,\nanalysts", RED, "kB alerts"),
    ]
    w, gap, x0, y0, h = 14.6, 2.2, 1.0, 20, 21
    xs = [x0 + i * (w + gap) for i in range(len(stages))]
    for x, (t, body, c, vol) in zip(xs, stages):
        title_box(ax, x, y0, w, h, t, body, hc=c, ec=c, fs=6.1, tfs=6.9)
        label(ax, x + w / 2, y0 + h + 1.6, vol, fs=6.1, color=c, weight="bold")
    for i in range(len(stages) - 1):
        arrow(ax, (xs[i] + w + 0.15, y0 + 7), (xs[i + 1] - 0.15, y0 + 7), color=NAVY, lw=1.1, ms=8)
    # look-ahead retasking (on board -> sensor), routed above the boxes
    yl = y0 + h + 4.6
    ax.plot([xs[1] + 4, xs[1] + 4, xs[0] + w - 3], [y0 + h, yl, yl], color=VIOLET, lw=0.9)
    arrow(ax, (xs[0] + w - 3, yl), (xs[0] + w - 3, y0 + h + 0.1), color=VIOLET, lw=0.9, ms=7)
    label(ax, xs[1] + 5.0, yl, "look-ahead retasking (dynamic targeting)", fs=6.0, color=VIOLET, ha="left")
    # labels feedback (users -> models)
    yg = 14.5
    ax.plot([xs[5] + w / 2, xs[5] + w / 2, xs[3] + w / 2], [y0, yg, yg], color=GREEN, lw=1.0)
    arrow(ax, (xs[3] + w / 2, yg), (xs[3] + w / 2, y0 - 0.1), color=GREEN, lw=1.0, ms=8)
    label(ax, (xs[3] + xs[4] + w) / 2 + 0.3, yg + 2.7, "labels, corrections,\nnew training data", fs=5.9, color=GREEN)
    # tip-and-cue (products -> sensor)
    yo = 7.5
    ax.plot([xs[4] + w / 2, xs[4] + w / 2, xs[0] + w / 2], [y0, yo, yo], color=ORANGE, lw=1.0, ls="--")
    arrow(ax, (xs[0] + w / 2, yo), (xs[0] + w / 2, y0 - 0.1), color=ORANGE, lw=1.0, ms=8)
    label(ax, (xs[0] + xs[4] + w) / 2, yo - 1.7,
          "tip-and-cue: a detection triggers new tasking of the same or another satellite", fs=6.0, color=ORANGE)
    # monitoring band
    box(ax, xs[1] + 1, 15.6, xs[3] - xs[1] - 4, 3.0, "drift monitoring · independent validation · model cards",
        fc="#F3F6F9", ec=GREY, fs=5.9, color=GREY, r=0.6, lw=0.6)
    fig.tight_layout()
    save(fig, "ch46_pipeline")


# ==============================================================================================
# 2. Land-cover classification of a synthetic multispectral scene
LC_NAMES = ["Water", "Forest", "Cropland", "Grassland", "Built-up", "Bare soil"]
LC_SHORT = ["Water", "Forest", "Crop", "Grass", "Built", "Bare"]
LC_COLS = ["#2F6DB5", "#1E6B3A", "#E3C04D", "#9BCB6B", "#C0392B", "#C9A27E"]
# Sentinel-2-like bands B2, B3, B4, B8, B11, B12 (reflectance)
SPEC = {
    "water": [0.050, 0.060, 0.040, 0.020, 0.010, 0.008],
    "forest": [0.025, 0.045, 0.025, 0.300, 0.140, 0.060],
    "crop": [0.040, 0.075, 0.050, 0.400, 0.200, 0.100],
    "grass": [0.045, 0.075, 0.065, 0.270, 0.240, 0.140],
    "roof": [0.140, 0.150, 0.160, 0.200, 0.240, 0.220],
    "asphalt": [0.070, 0.080, 0.090, 0.110, 0.130, 0.120],
    "bare": [0.110, 0.150, 0.200, 0.260, 0.340, 0.300],
}


def lc_scene(seed, n=160, shift=0.0):
    """shift > 0 moves the scene to a drier, hazier region: brighter, redder soils, less NIR from plants."""
    rng = np.random.default_rng(seed)
    fields = np.stack([ndi.gaussian_filter(rng.normal(size=(n, n)), 9, mode="wrap") for _ in range(6)])
    fields *= np.array([1.0, 1.15, 1.1, 0.95, 0.95, 0.85])[:, None, None]
    cls = fields.argmax(0)
    # parcels (Voronoi) give crops and grass a varying growth stage
    pts = rng.uniform(0, n, (90, 2))
    yy, xx = np.mgrid[0:n, 0:n]
    d = (yy[..., None] - pts[:, 0]) ** 2 + (xx[..., None] - pts[:, 1]) ** 2
    parcel = d.argmin(-1)
    stage = rng.uniform(0, 0.9, 90)[parcel]
    S = {k: np.array(v) for k, v in SPEC.items()}
    if shift:
        S["bare"] = S["bare"] * (1 + shift * np.array([0.1, 0.2, 0.35, 0.25, 0.2, 0.25]))
        for k in ("forest", "crop", "grass"):
            S[k] = S[k] * (1 - shift * np.array([0, 0, -0.15, 0.25, 0.0, -0.1]))
        S["water"] = S["water"] * (1 + 0.8 * shift)
    img = np.zeros((n, n, 6))
    img[cls == 0] = S["water"]
    m = cls == 1
    gap = rng.uniform(size=m.sum()) < 0.18                                       # canopy gaps
    img[m] = np.where(gap[:, None], S["grass"], S["forest"]) * rng.lognormal(0, 0.18, (m.sum(), 1))
    m = cls == 2
    img[m] = (1 - stage[m, None]) * S["crop"] + stage[m, None] * S["bare"]
    m = cls == 3
    img[m] = (1 - 0.7 * stage[m, None]) * S["grass"] + 0.7 * stage[m, None] * S["bare"]
    m = cls == 4
    u = rng.uniform(size=m.sum())
    img[m] = np.where(u[:, None] < 0.32, S["roof"], np.where(u[:, None] < 0.6, S["asphalt"],
                      np.where(u[:, None] < 0.85, S["grass"], S["forest"])))
    img[cls == 5] = S["bare"]
    # optics blur, illumination/moisture variation, noise
    img = ndi.gaussian_filter(img, (0.6, 0.6, 0))
    illum = 1 + 0.12 * ndi.gaussian_filter(rng.normal(size=(n, n)), 6) / 0.05
    img = img * np.clip(illum, 0.75, 1.25)[..., None] * rng.lognormal(0, 0.10, (n, n, 6))
    img += rng.normal(0, 0.010, img.shape)
    img += shift * np.array([0.03, 0.02, 0.012, 0.005, 0, 0])        # haze
    return np.clip(img, 0.001, 1), cls


def rgb(img, gain=3.2):
    return np.clip(img[..., [2, 1, 0]] * gain, 0, 1) ** 0.8


def pixel_feats(img):
    b, g, r, nir, s1, s2 = [img[..., i] for i in range(6)]
    ndvi = (nir - r) / (nir + r)
    ndbi = (s1 - nir) / (s1 + nir)
    mndwi = (g - s1) / (g + s1)
    return np.concatenate([img, ndvi[..., None], ndbi[..., None], mndwi[..., None]], axis=-1)


def landcover():
    from sklearn.ensemble import RandomForestClassifier
    n = 160
    img, cls = lc_scene(46)
    feats = pixel_feats(img)
    rng = np.random.default_rng(1)
    # training labels only from the western half; test on the eastern half (8-pixel buffer)
    tr_r, tr_c, tr_y = [], [], []
    for k in range(6):
        rr, cc = np.where((cls == k) & (np.arange(n)[None, :] < 72))
        sel = rng.choice(len(rr), min(400, len(rr)), replace=False)
        tr_r += list(rr[sel]); tr_c += list(cc[sel]); tr_y += [k] * len(sel)
    tr_r, tr_c, tr_y = map(np.array, (tr_r, tr_c, tr_y))
    te_r, te_c = np.where(np.arange(n)[None, :].repeat(n, 0) >= 80)
    te_y = cls[te_r, te_c]
    # random forest, per pixel
    rf = RandomForestClassifier(n_estimators=200, min_samples_leaf=2, random_state=0, n_jobs=2)
    rf.fit(feats[tr_r, tr_c], tr_y)
    all_r, all_c = np.mgrid[0:n, 0:n]
    all_r, all_c = all_r.ravel(), all_c.ravel()
    rf_map = rf.predict(feats[all_r, all_c]).reshape(n, n)
    # random forest on the same 5x5 patches the network sees (control)
    logimg = np.log(img)
    mu, sd = logimg.reshape(-1, 6).mean(0), logimg.reshape(-1, 6).std(0)
    z = (logimg - mu) / sd
    Xtr = patches(z, 2, tr_r, tr_c)
    rf2 = RandomForestClassifier(n_estimators=200, min_samples_leaf=2, random_state=0, n_jobs=2).fit(Xtr, tr_y)
    Xall = patches(z, 2, all_r, all_c)
    rfp_map = rf2.predict(Xall).reshape(n, n)
    # small CNN: one 5x5 convolution with 64 filters + ReLU + 1x1 output layer, evaluated pixel by pixel
    # augmentation: random flips/rotations of the training patches
    aug = []
    P = Xtr.reshape(-1, 5, 5, 6)
    for kk in range(4):
        aug.append(np.rot90(P, kk, axes=(1, 2)))
        aug.append(np.rot90(P[:, ::-1], kk, axes=(1, 2)))
    Xaug = np.concatenate([a.reshape(len(P), -1) for a in aug])
    yaug = np.tile(tr_y, 8)
    net = NumpyNet(Xtr.shape[1], (64,), 6, seed=3).fit(Xaug, yaug, epochs=25, lr=2e-3, batch=128, wd=3e-4)
    cnn_map = net.predict_proba(Xall).argmax(1).reshape(n, n)
    res = {}
    for name, mp in [("RF", rf_map), ("RF5", rfp_map), ("CNN", cnn_map)]:
        cm, prod, user, f1 = f1_scores(te_y, mp[te_r, te_c], 6)
        oa = np.trace(cm) / cm.sum()
        res[name] = (cm, prod, user, f1, oa)
        print(f"landcover {name}: OA={oa*100:.1f}%  F1=" + " ".join(f"{x:.2f}" for x in f1)
              + "  prod=" + " ".join(f"{x:.2f}" for x in prod) + "  user=" + " ".join(f"{x:.2f}" for x in user))
    print("landcover CNN params", net.n_params(), "train pixels", len(tr_y), "test pixels", len(te_y))

    cmap = ListedColormap(LC_COLS)
    fig = plt.figure(figsize=(7.0, 4.55))
    gs = fig.add_gridspec(3, 4, height_ratios=[1, 0.07, 1.0], hspace=0.26, wspace=0.12)
    axs = [fig.add_subplot(gs[0, i]) for i in range(4)]
    for ax, im, t in zip(axs, [rgb(img), cls, rf_map, cnn_map],
                         ["(a) True-colour image", "(b) Reference map", "(c) Random forest",
                          "(d) Small CNN"]):
        if im.ndim == 3:
            ax.imshow(im, interpolation="nearest")
        else:
            ax.imshow(im, cmap=cmap, vmin=-0.5, vmax=5.5, interpolation="nearest")
        img_axes(ax)
        ax.set_title(t, fontsize=7.6, loc="left")
        ax.axvline(75.5, color="white", lw=0.8, ls="--")
    axs[0].text(36, 152, "train", color="white", fontsize=6.3, ha="center", va="center")
    axs[0].text(118, 152, "test", color="white", fontsize=6.3, ha="center", va="center")
    for ax, (name, lab) in zip(axs[2:], [("RF", "RF"), ("CNN", "CNN")]):
        ax.text(156, 6, f"test OA {res[name][4]*100:.1f} %", color="white", fontsize=6.2, ha="right", va="top",
                bbox=dict(fc="black", ec="none", alpha=0.45, pad=1.2))
    # legend
    handles = [Rectangle((0, 0), 1, 1, fc=c) for c in LC_COLS]
    lax = fig.add_subplot(gs[1, :])
    lax.axis("off")
    lax.legend(handles, LC_NAMES, loc="center", ncol=6, fontsize=6.5, handlelength=1.0, columnspacing=1.4)
    # confusion matrix of CNN
    ax = fig.add_subplot(gs[2, 0:2])
    cm = res["CNN"][0].astype(float)
    cmn = cm / cm.sum(1, keepdims=True) * 100
    ax.imshow(cmn, cmap="Blues", vmin=0, vmax=100)
    for i in range(6):
        for j in range(6):
            ax.text(j, i, f"{cmn[i, j]:.0f}", ha="center", va="center", fontsize=6.2,
                    color="white" if cmn[i, j] > 55 else INK)
    ax.set_xticks(range(6))
    ax.set_xticklabels(LC_SHORT, fontsize=6.0)
    ax.set_yticks(range(6))
    ax.set_yticklabels(LC_NAMES, fontsize=6.2)
    ax.grid(False)
    ax.set_xlabel("Mapped class (CNN)", fontsize=7)
    ax.set_ylabel("Reference", fontsize=7)
    ax.set_title("(e) CNN confusion matrix, % of reference", fontsize=7.6, loc="left")
    # per-class F1
    ax = fig.add_subplot(gs[2, 2:])
    xx = np.arange(6)
    for off, name, col, lab in [(-0.27, "RF", ORANGE, "RF, pixel"), (0.0, "RF5", GOLD, "RF, 5 × 5 patch"),
                                (0.27, "CNN", BLUE, "CNN")]:
        ax.bar(xx + off, res[name][3], 0.26, color=col, label=f"{lab} {res[name][4]*100:.0f} %")
    ax.set_xticks(xx)
    ax.set_xticklabels(LC_SHORT, fontsize=6.2)
    ax.set_ylim(0, 1.3)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.tick_params(labelsize=6.5)
    ax.set_ylabel("F1 score (test half)", fontsize=7)
    ax.legend(fontsize=5.9, loc="upper center", ncol=3, handlelength=1.0, columnspacing=0.8, title="overall accuracy",
              title_fontsize=5.9)
    ax.set_title("(f) Per-class F1", fontsize=7.6, loc="left")
    foot(fig, "Synthetic 160 × 160-pixel scene, six Sentinel-2-like bands, with parcels at different growth stages, "
         "textured built-up areas, blur, illumination changes and noise. 400 labelled pixels per class from the "
         "western half train each model; all 12 800 pixels of the eastern half test it. CNN: one 5 × 5 × 64 "
         "convolution, ReLU, 1 × 1 output (10 054 weights), written in numpy.", width=170)
    fig.subplots_adjust(left=0.1, right=0.99, top=0.95, bottom=0.165)
    save(fig, "ch46_landcover")

# ==============================================================================================
# 3. Change detection: NDVI differencing versus a learned bi-temporal classifier
def cd_scene(seed, n=128):
    rng = np.random.default_rng(seed)
    S = {k: np.array(v) for k, v in SPEC.items()}
    f = np.stack([ndi.gaussian_filter(rng.normal(size=(n, n)), 10, mode="wrap") for _ in range(3)])
    f *= np.array([1.35, 1.0, 0.8])[:, None, None]
    land = f.argmax(0)                      # 0 forest, 1 cropland, 2 grassland
    pts = rng.uniform(0, n, (70, 2))
    yy, xx = np.mgrid[0:n, 0:n]
    parcel = ((yy[..., None] - pts[:, 0]) ** 2 + (xx[..., None] - pts[:, 1]) ** 2).argmin(-1)
    st1 = rng.uniform(0, 0.4, 70)
    harvested = rng.uniform(size=70) < 0.35
    st2 = np.where(harvested, rng.uniform(0.75, 0.95, 70), np.clip(st1 + rng.normal(0.1, 0.1, 70), 0, 0.6))
    def render(stage, grass_dry):
        img = np.zeros((n, n, 6))
        m = land == 0
        img[m] = S["forest"] * rng.lognormal(0, 0.10, (m.sum(), 1))
        m = land == 1
        img[m] = (1 - stage[parcel][m, None]) * S["crop"] + stage[parcel][m, None] * S["bare"]
        m = land == 2
        img[m] = (1 - grass_dry) * S["grass"] + grass_dry * S["bare"]
        return img
    before = render(st1, 0.1)
    after = render(st2, 0.35)               # harvests and seasonal drying of grass: changes, but not forest loss
    # true forest loss: irregular clearings inside forest
    change = np.zeros((n, n), bool)
    for _ in range(9):
        cy, cx = rng.uniform(8, n - 8, 2)
        ry, rx = rng.uniform(3, 9, 2)
        th = rng.uniform(0, np.pi)
        dy, dx = yy - cy, xx - cx
        u = (dx * np.cos(th) + dy * np.sin(th)) / rx
        v = (-dx * np.sin(th) + dy * np.cos(th)) / ry
        blob = (u ** 2 + v ** 2 + 0.35 * ndi.gaussian_filter(rng.normal(size=(n, n)), 2) / 0.1) < 1
        change |= blob & (land == 0)
    debris = rng.uniform(0.55, 0.9, change.sum())[:, None]
    after[change] = debris * S["bare"] + (1 - debris) * S["forest"]
    # nuisances in the after image: haze, cloud shadow, 1-pixel misregistration
    def ellipse(cy, cx, ry, rx):
        return ((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2
    hc = rng.uniform(20, n - 20, 2)
    haze = np.exp(-ellipse(hc[0], hc[1], 18, 26))
    after += haze[..., None] * np.array([0.07, 0.06, 0.05, 0.02, 0.008, 0.004])
    sc = rng.uniform(20, n - 20, 2)
    shadow = np.exp(-ellipse(sc[0], sc[1], 10, 16) ** 2)
    after *= (1 - 0.6 * shadow)[..., None]
    after = np.roll(after, 1, axis=1)
    change = np.roll(change, 1, axis=1)
    for im in (before, after):
        im *= rng.lognormal(0, 0.05, im.shape)
        im += rng.normal(0, 0.006, im.shape)
    return np.clip(before, 0.001, 1), np.clip(after, 0.001, 1), change, land


def ndvi(img):
    return (img[..., 3] - img[..., 2]) / (img[..., 3] + img[..., 2])


def nbr(img):
    return (img[..., 3] - img[..., 5]) / (img[..., 3] + img[..., 5])


def cd_feats(b, a):
    dn = ndvi(a) - ndvi(b)
    dnbr = nbr(a) - nbr(b)
    return np.concatenate([np.log(b), np.log(a), dn[..., None], dnbr[..., None], ndvi(b)[..., None],
                           ndi.uniform_filter(dn, 3)[..., None]], axis=-1)


def change():
    from sklearn.ensemble import RandomForestClassifier
    rng = np.random.default_rng(5)
    Xs, ys, dns = [], [], []
    for sd in (101, 102, 103, 104):
        b, a, ch, _ = cd_scene(sd)
        F = cd_feats(b, a).reshape(-1, 18 - 2)
        y = ch.ravel()
        pos = np.where(y)[0]
        neg = rng.choice(np.where(~y)[0], 6 * len(pos), replace=False)
        idx = np.concatenate([pos, neg])
        Xs.append(F[idx]); ys.append(y[idx])
        dns.append(((ndvi(a) - ndvi(b)).ravel(), y))
    rf = RandomForestClassifier(n_estimators=200, min_samples_leaf=3, random_state=0, n_jobs=2)
    rf.fit(np.vstack(Xs), np.concatenate(ys))
    # NDVI threshold tuned on the same training scenes to maximise F1
    dn_all = np.concatenate([d for d, _ in dns]); y_all = np.concatenate([y for _, y in dns])
    best = (0, None)
    for t in np.linspace(-0.8, -0.05, 76):
        p = dn_all < t
        tp = (p & y_all).sum(); fp = (p & ~y_all).sum(); fn = (~p & y_all).sum()
        f1 = 2 * tp / max(2 * tp + fp + fn, 1)
        if f1 > best[0]:
            best = (f1, t)
    thr = best[1]
    b, a, ch, land = cd_scene(46)
    dn = ndvi(a) - ndvi(b)
    p_nd = dn < thr
    prob = rf.predict_proba(cd_feats(b, a).reshape(-1, 16))[:, 1].reshape(ch.shape)
    p_ml = prob > 0.5
    scores = {}
    for name, p in [("NDVI", p_nd), ("RF", p_ml)]:
        tp = (p & ch).sum(); fp = (p & ~ch).sum(); fn = (~p & ch).sum()
        prec, rec = tp / max(tp + fp, 1), tp / max(tp + fn, 1)
        scores[name] = (prec, rec, 2 * prec * rec / (prec + rec))
        print(f"change {name}: thr={thr:.2f} precision={prec:.2f} recall={rec:.2f} F1={scores[name][2]:.2f} "
              f"FP px={fp} TP px={tp} FN px={fn} true change px={ch.sum()}")

    def fc(img):
        return np.clip(img[..., [3, 2, 1]] * np.array([2.2, 5.0, 5.0]), 0, 1) ** 0.9

    def outcome(p):
        base = fc(a).mean(-1, keepdims=True).repeat(3, -1) * 0.55 + 0.35
        out = base.copy()
        out[p & ch] = [0.12, 0.42, 0.75]
        out[p & ~ch] = [0.75, 0.15, 0.2]
        out[~p & ch] = [0.95, 0.62, 0.1]
        return out
    fig = plt.figure(figsize=(7.0, 2.5))
    gs = fig.add_gridspec(1, 5, width_ratios=[1, 1, 1, 1, 1.15], wspace=0.08)
    titles = ["(a) Before", "(b) After", "(c) NDVI difference", "(d) Learned (RF)"]
    iax = []
    for i, (im, t) in enumerate(zip([fc(b), fc(a), outcome(p_nd), outcome(p_ml)], titles)):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(im, interpolation="nearest")
        img_axes(ax)
        ax.set_title(t, fontsize=7.4, loc="left")
        iax.append(ax)
    ax = fig.add_subplot(gs[0, 4])
    xx = np.arange(3)
    ax.bar(xx - 0.19, scores["NDVI"], 0.36, color=GREY, label="NDVI difference")
    ax.bar(xx + 0.19, scores["RF"], 0.36, color=BLUE, label="Learned (RF)")
    for k in range(3):
        ax.text(k - 0.19, scores["NDVI"][k] + 0.02, f"{scores['NDVI'][k]:.2f}", ha="center", fontsize=5.8)
        ax.text(k + 0.19, scores["RF"][k] + 0.02, f"{scores['RF'][k]:.2f}", ha="center", fontsize=5.8)
    ax.set_xticks(xx)
    ax.set_xticklabels(["Precision", "Recall", "F1"], fontsize=6.4)
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.5, 1.0])
    ax.tick_params(labelsize=6.4)
    ax.set_title("(e) Scores on test scene", fontsize=7.4, loc="left")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.27)
    iax[0].apply_aspect()
    p0 = iax[0].get_position()
    pb = ax.get_position()
    ax.set_position([pb.x0 + 0.03, p0.y0, pb.width - 0.03, p0.height])
    cols = ([0.12, 0.42, 0.75], [0.75, 0.15, 0.2], [0.95, 0.62, 0.1], GREY, BLUE)
    handles = [Rectangle((0, 0), 1, 1, fc=c) for c in cols]
    fig.legend(handles, ["correct detection", "false alarm", "missed change", "NDVI difference", "learned (RF)"],
               loc="center", ncol=5, fontsize=6.2, bbox_to_anchor=(0.41, p0.y0 - 0.07), handlelength=1.0,
               columnspacing=1.5)
    foot(fig, "Synthetic 128 × 128-pixel scene (false colour: NIR, red, green). Forest clearings are the only true "
         "change; harvests, drying grass, haze, a cloud shadow and 1-pixel misregistration are not. The NDVI "
         f"threshold ({thr:.2f}) and the random forest (200 trees, 16 bi-temporal features) were both tuned on four "
         "other scenes.", width=150)
    save(fig, "ch46_change")

# ==============================================================================================
# 4. Crop types from Sentinel-2-like NDVI time series: random forest versus a numpy temporal-attention network
CROP_NAMES = ["Winter wheat", "Maize", "Soybean", "Sugar beet", "Grassland", "Sunflower"]
CROP_COLS = [GOLD, ORANGE, GREEN, VIOLET, SKY, RED]
DOY = np.arange(60, 305, 5).astype(float)          # 49 acquisition dates, every 5 days


def crop_series(rng, n, pc):
    """Return NDVI (n, T), clear mask (n, T) and labels for n fields; pc = probability a date is cloudy."""
    y = rng.integers(0, 6, n)
    T = len(DOY)
    par = {0: (0.18, 70, 182, 0.67, 9, 6), 1: (0.18, 162, 262, 0.68, 7, 8), 2: (0.18, 170, 252, 0.64, 6, 7),
           3: (0.18, 145, 288, 0.64, 11, 10), 5: (0.18, 158, 238, 0.60, 7, 6)}
    out = np.zeros((n, T))
    shift = rng.normal(0, 10, n)
    amp = rng.uniform(0.85, 1.1, n)
    base = rng.normal(0, 0.04, n)
    for k in (0, 1, 2, 3, 5):
        m = y == k
        b0, sos, eos, a0, r1, r2 = par[k]
        t = DOY[None, :] - shift[m, None]
        out[m] = b0 + base[m, None] + a0 * amp[m, None] * (1 / (1 + np.exp(-(t - sos) / r1))
                                                           - 1 / (1 + np.exp(-(t - eos) / r2)))
    m = y == 4
    cuts = np.array([140.0, 195.0, 255.0])[None, :] + rng.normal(0, 8, (m.sum(), 3))
    g = 0.72 + base[m, None] + 0.06 * np.sin((DOY[None, :] - 60) / 240 * np.pi)
    for c in range(3):
        dt = DOY[None, :] - cuts[:, [c]]
        g -= 0.32 * ((dt >= 0) & (dt < 30)) * (1 - dt / 30) * amp[m, None]
    out[m] = g
    out += rng.normal(0, 0.03, out.shape)
    clear = rng.uniform(size=(n, T)) > pc
    thin = (rng.uniform(size=(n, T)) < 0.08) & clear                   # undetected thin cloud
    out[thin] -= rng.uniform(0.15, 0.4, thin.sum())
    clear[:, 0] |= ~clear.any(1)
    return np.clip(out, -0.1, 1), clear, y


def interp_series(nd, clear):
    out = np.empty_like(nd)
    for i in range(len(nd)):
        m = clear[i]
        out[i] = np.interp(DOY, DOY[m], nd[i, m])
    return out


class TemporalAttention:
    """Embedding of (NDVI, day of year) -> tanh features; H learned queries attend over clear dates only."""
    def __init__(self, D=48, H=6, Dk=16, n_out=6, seed=0):
        rng = np.random.default_rng(seed)
        self.D, self.H, self.Dk = D, H, Dk
        freqs = 1.0 / (10.0 * (40.0 ** (np.arange(D // 2) / (D // 2))))
        self.P = np.concatenate([np.sin(DOY[:, None] * freqs), np.cos(DOY[:, None] * freqs)], 1)   # (T, D)
        self.p = {"We": rng.normal(0, 1.0, (1, D)), "be": np.zeros(D), "Wp": rng.normal(0, 0.5, (D, D)),
                  "Wk": rng.normal(0, 1 / np.sqrt(D), (D, Dk)), "q": rng.normal(0, 1.0, (H, Dk)),
                  "Wo": rng.normal(0, 1 / np.sqrt(H * D), (H * D, n_out)), "bo": np.zeros(n_out)}
        self.rng = rng

    def forward(self, x, mask):
        p = self.p
        u = x[..., None] * p["We"][0] + p["be"] + self.P @ p["Wp"]          # (B, T, D)
        h = np.tanh(u)
        k = h @ p["Wk"]                                                     # (B, T, Dk)
        s = np.einsum("btk,hk->bht", k, p["q"]) / np.sqrt(self.Dk)
        s = np.where(mask[:, None, :], s, -1e9)
        s -= s.max(-1, keepdims=True)
        a = np.exp(s) * mask[:, None, :]
        a /= a.sum(-1, keepdims=True)
        z = np.einsum("bht,btd->bhd", a, h)
        logits = z.reshape(len(x), -1) @ p["Wo"] + p["bo"]
        return logits, (x, mask, h, k, a, z)

    def predict(self, x, mask):
        return self.forward(x, mask)[0].argmax(1)

    def fit(self, x, mask, y, epochs=60, lr=3e-3, batch=128, wd=1e-4):
        p = self.p
        m = {k: np.zeros_like(v) for k, v in p.items()}
        v2 = {k: np.zeros_like(v) for k, v in p.items()}
        t = 0
        for ep in range(epochs):
            perm = self.rng.permutation(len(x))
            for i in range(0, len(x), batch):
                idx = perm[i:i + batch]
                B = len(idx)
                logits, (xb, mb, h, k, a, z) = self.forward(x[idx], mask[idx])
                pr = np.exp(logits - logits.max(1, keepdims=True))
                pr /= pr.sum(1, keepdims=True)
                pr[np.arange(B), y[idx]] -= 1
                dl = pr / B
                g = {"Wo": z.reshape(B, -1).T @ dl, "bo": dl.sum(0)}
                dz = (dl @ p["Wo"].T).reshape(B, self.H, self.D)
                da = np.einsum("bhd,btd->bht", dz, h)
                dh = np.einsum("bht,bhd->btd", a, dz)
                ds = a * (da - (a * da).sum(-1, keepdims=True)) / np.sqrt(self.Dk)
                g["q"] = np.einsum("bht,btk->hk", ds, k)
                dk = np.einsum("bht,hk->btk", ds, p["q"])
                g["Wk"] = np.einsum("btd,btk->dk", h, dk)
                dh += dk @ p["Wk"].T
                du = dh * (1 - h ** 2)
                g["We"] = np.einsum("bt,btd->d", xb, du)[None, :]
                g["be"] = du.sum((0, 1))
                g["Wp"] = self.P.T @ du.sum(0)
                t += 1
                for key in p:
                    gg = g[key] + (wd * p[key] if key in ("Wo", "Wk", "Wp") else 0)
                    m[key] = 0.9 * m[key] + 0.1 * gg
                    v2[key] = 0.999 * v2[key] + 0.001 * gg ** 2
                    p[key] -= lr * (m[key] / (1 - 0.9 ** t)) / (np.sqrt(v2[key] / (1 - 0.999 ** t)) + 1e-8)
        return self


def crops():
    from sklearn.ensemble import RandomForestClassifier
    rng = np.random.default_rng(46)
    ntr = 5000
    pcs_tr = rng.uniform(0.2, 0.8, ntr)
    nd_tr, cl_tr, y_tr = crop_series(rng, ntr, pcs_tr[:, None])
    rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=2, random_state=0, n_jobs=2)
    rf.fit(interp_series(nd_tr, cl_tr), y_tr)
    ta = TemporalAttention(seed=1).fit(nd_tr, cl_tr, y_tr, epochs=50, lr=3e-3)
    n_par = sum(v.size for v in ta.p.values())
    pcs = [0.2, 0.35, 0.5, 0.65, 0.8]
    acc_rf, acc_ta = [], []
    for pc in pcs:
        nd, cl, y = crop_series(np.random.default_rng(int(pc * 100)), 3000, pc)
        acc_rf.append((rf.predict(interp_series(nd, cl)) == y).mean())
        acc_ta.append((ta.predict(nd, cl) == y).mean())
    print("crops pc", pcs)
    print("crops RF-interp acc", [f"{a*100:.1f}" for a in acc_rf])
    print("crops attention acc", [f"{a*100:.1f}" for a in acc_ta], "params", n_par)
    # attention weights per class (clear-sky reference set, pc = 0.2)
    nd, cl, y = crop_series(np.random.default_rng(7), 3000, 0.2)
    _, (xb, mb, h, k, a, z) = ta.forward(nd, cl)
    # head with the most peaked attention on average
    ent = -(a * np.log(a + 1e-12)).sum(-1).mean((0))
    hsel = int(np.argmin(ent))

    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.8), gridspec_kw={"width_ratios": [1.15, 0.9, 1.15]})
    ax = axs[0]
    nd0, cl0, y0 = crop_series(np.random.default_rng(3), 400, 0.0)
    for kk in range(6):
        mm = y0 == kk
        mu = nd0[mm].mean(0)
        sd = nd0[mm].std(0)
        ax.fill_between(DOY, mu - sd, mu + sd, color=CROP_COLS[kk], alpha=0.18, lw=0)
        ax.plot(DOY, mu, color=CROP_COLS[kk], lw=1.4, label=CROP_NAMES[kk])
    ndx, clx, yx = crop_series(np.random.default_rng(11), 30, 0.6)
    i = int(np.where(yx == 1)[0][0])
    ax.plot(DOY[clx[i]], ndx[i, clx[i]], "o", ms=3.2, mfc="white", mec=INK, mew=0.8)
    ax.legend([Line2D([], [], ls="none", marker="o", ms=3.2, mfc="white", mec=INK, mew=0.8)],
              ["clear dates of one maize field (60 % cloudy)"], fontsize=5.8, loc="upper left", handlelength=1.0)
    ax.set_xlabel("Day of year", fontsize=7)
    ax.set_ylabel("NDVI", fontsize=7)
    ax.set_ylim(-0.02, 1.2)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.tick_params(labelsize=6.5)
    ax.set_title("(a) Crop calendars in NDVI", fontsize=7.6, loc="left")
    ax = axs[1]
    ax.plot([p * 100 for p in pcs], np.array(acc_rf) * 100, "o-", color=ORANGE, ms=3.5, label="RF, gap-filled")
    ax.plot([p * 100 for p in pcs], np.array(acc_ta) * 100, "s-", color=BLUE, ms=3.5, label="Temporal attention")
    ax.set_xlabel("Cloudy dates (%)", fontsize=7)
    ax.set_ylabel("Overall accuracy (%)", fontsize=7)
    ax.tick_params(labelsize=6.5)
    ax.legend(fontsize=5.9, loc="lower left", handlelength=1.4)
    ax.set_title("(b) Accuracy", fontsize=7.6, loc="left")
    ax = axs[2]
    for kk in range(6):
        mm = y == kk
        w = a[mm, hsel, :].mean(0)
        ax.plot(DOY, w, color=CROP_COLS[kk], lw=1.3)
    ax.set_xlabel("Day of year", fontsize=7)
    ax.set_ylabel("Mean attention weight", fontsize=7)
    ax.tick_params(labelsize=6.5)
    ax.set_title(f"(c) Where one attention head looks", fontsize=7.6, loc="left")
    handles = [Line2D([], [], color=c, lw=1.6) for c in CROP_COLS]
    fig.legend(handles, CROP_NAMES, loc="center", ncol=6, fontsize=6.3, bbox_to_anchor=(0.5, 0.2),
               handlelength=1.4, columnspacing=1.4)
    foot(fig, "Synthetic fields: double-logistic NDVI curves (grass: three mowing cuts) with ±10-day timing shifts, "
         "amplitude spread and noise; 49 dates every 5 days; clouds remove dates at random and 8 % of 'clear' dates "
         f"carry undetected thin cloud. Both models trained on 5 000 fields, tested on 3 000 per point. Attention "
         f"network: six heads, {n_par:,} weights, numpy.".replace(",", " "), width=165)
    fig.tight_layout(rect=(0, 0.24, 1, 1), w_pad=1.0)
    save(fig, "ch46_crops")

# ==============================================================================================
# 5. SAR speckle: Lee filter versus learned filters, with the equivalent number of looks (ENL)
def sar_reflectivity(seed, n=192):
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0, n, (34, 2))
    yy, xx = np.mgrid[0:n, 0:n]
    parcel = ((yy[..., None] - pts[:, 0]) ** 2 + (xx[..., None] - pts[:, 1]) ** 2).argmin(-1)
    db = rng.choice([-17.0, -14.0, -11.0, -8.0, -5.0], 34)[parcel]
    # a road (dark line) and a few bright point targets
    a, b0 = rng.uniform(-0.6, 0.6), rng.uniform(0.3 * n, 0.7 * n)
    road = np.abs(yy - (a * xx + b0)) < 1.3
    db[road] = -22.0
    for _ in range(10):
        cy, cx = rng.integers(5, n - 5, 2)
        db[cy:cy + 2, cx:cx + 2] = 8.0
    return 10 ** (db / 10)


def lee(I, w=7, looks=1):
    m = ndi.uniform_filter(I, w)
    v = ndi.uniform_filter(I * I, w) - m * m
    cu2 = 1.0 / looks
    ci2 = v / np.maximum(m * m, 1e-12)
    k = np.clip((1 - cu2 / np.maximum(ci2, 1e-12)) / (1 + cu2), 0, 1)
    return m + k * (I - m)


def despeckle():
    r = 4                                            # 9 x 9 patches
    Xl, yl = [], []
    rng = np.random.default_rng(0)
    for sd in (201, 202, 203):
        R = sar_reflectivity(sd)
        for rep in range(2):
            I = R * rng.exponential(1.0, R.shape)
            L = np.log(I)[..., None]
            rr, cc = rng.integers(0, R.shape[0], 20000), rng.integers(0, R.shape[1], 20000)
            P = patches(L, r, rr, cc)
            Xl.append(P); yl.append(np.log(R[rr, cc]))
    X = np.vstack(Xl); y = np.concatenate(yl)
    mu = X.mean(1, keepdims=True)
    # learned linear filter: least-squares 9x9 kernel on log intensity (+ bias)
    A = np.hstack([X, np.ones((len(X), 1))])
    wlin = np.linalg.lstsq(A, y, rcond=None)[0]
    # learned non-linear filter: numpy network on mean-removed patches (+ patch mean as an input)
    Xn = np.hstack([X - mu, mu])
    net = NumpyNet(Xn.shape[1], (128, 64), 1, seed=2).fit(Xn, (y - mu[:, 0])[:, None], epochs=18, lr=1.5e-3,
                                                          batch=256, wd=1e-5, regression=True)
    # test scene
    R = sar_reflectivity(46)
    I = R * np.random.default_rng(46).exponential(1.0, R.shape)
    n = R.shape[0]
    rr, cc = np.mgrid[0:n, 0:n]
    P = patches(np.log(I)[..., None], r, rr.ravel(), cc.ravel())
    pm = P.mean(1, keepdims=True)
    out = {
        "1 look": I,
        "Boxcar 7×7": ndi.uniform_filter(I, 7),
        "Lee 7×7": lee(I, 7),
        "Learned linear": np.exp(np.hstack([P, np.ones((len(P), 1))]) @ wlin).reshape(n, n),
        "Learned network": np.exp(net.predict_value(np.hstack([P - pm, pm]))[:, 0] + pm[:, 0]).reshape(n, n),
    }
    # homogeneous region: interior of the largest parcel (eroded), excluding points and road
    lab = np.round(10 * np.log10(R)).astype(int)
    best = None
    for v in np.unique(lab):
        comp, nc = ndi.label(lab == v)
        for c in range(1, nc + 1):
            m = ndi.binary_erosion(comp == c, iterations=6)
            if best is None or m.sum() > best.sum():
                best = m
    edge = ndi.binary_dilation(np.abs(ndi.laplace(lab.astype(float))) > 0, iterations=1)
    stats = {}
    for k, im in out.items():
        enl = im[best].mean() ** 2 / im[best].var()
        err = 10 * np.log10(np.maximum(im, 1e-6)) - 10 * np.log10(R)
        rmse = np.sqrt((err ** 2).mean())
        rmse_edge = np.sqrt((err[edge] ** 2).mean())
        stats[k] = (enl, rmse, rmse_edge)
        print(f"despeckle {k}: ENL={enl:.1f} RMSE={rmse:.2f} dB  RMSE near edges={rmse_edge:.2f} dB")
    print("despeckle homogeneous pixels", best.sum(), "net params", net.n_params(), "train patches", len(X))

    fig = plt.figure(figsize=(7.0, 3.95))
    gs = fig.add_gridspec(2, 4, height_ratios=[1, 0.78], hspace=0.36, wspace=0.1)
    show = [("(a) True reflectivity", R), ("(b) Single look", I), ("(c) Lee 7 × 7", out["Lee 7×7"]),
            ("(d) Learned network", out["Learned network"])]
    for i, (t, im) in enumerate(show):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(10 * np.log10(np.maximum(im, 1e-4)), cmap="gray", vmin=-24, vmax=2, interpolation="nearest")
        img_axes(ax)
        ax.set_title(t, fontsize=7.4, loc="left")
        if i == 1:
            ax.contour(best, levels=[0.5], colors=[GOLD], linewidths=0.7)
            ax.text(4, n - 6, "ENL region", color=GOLD, fontsize=5.8, va="bottom")
    names = list(out.keys())
    cols = [GREY, SKY, ORANGE, GREEN, BLUE]
    ax = fig.add_subplot(gs[1, 0:2])
    xx = np.arange(len(names))
    enl = [stats[k][0] for k in names]
    ax.bar(xx, enl, 0.6, color=cols)
    for k, v in enumerate(enl):
        ax.text(k, v * 1.08, f"{v:.0f}" if v >= 10 else f"{v:.1f}", ha="center", fontsize=6.0)
    ax.set_yscale("log")
    ax.set_ylim(0.5, 400)
    ax.set_xticks(xx)
    ax.set_xticklabels([s.replace(" ", "\n", 1) for s in names], fontsize=6.0)
    ax.tick_params(labelsize=6.3)
    ax.set_ylabel("ENL (higher = smoother)", fontsize=6.8)
    ax.set_title("(e) Equivalent number of looks", fontsize=7.4, loc="left")
    ax = fig.add_subplot(gs[1, 2:])
    w = 0.38
    ax.bar(xx - w / 2, [stats[k][1] for k in names], w, color=cols, alpha=0.95, label="all pixels")
    ax.bar(xx + w / 2, [stats[k][2] for k in names], w, color=cols, alpha=0.45, hatch="////", edgecolor="white",
           lw=0, label="near edges")
    ax.set_xticks(xx)
    ax.set_xticklabels([s.replace(" ", "\n", 1) for s in names], fontsize=6.0)
    ax.tick_params(labelsize=6.3)
    ax.set_ylabel("RMS error (dB)", fontsize=6.8)
    ax.legend(fontsize=6.0, loc="upper right", handlelength=1.4)
    ax.set_title("(f) Error against the truth", fontsize=7.4, loc="left")
    foot(fig, "Synthetic 192 × 192-pixel scene: 34 fields between −17 and −5 dB, a −22 dB road and ten +8 dB point "
         "targets, multiplied by single-look exponential speckle. Learned filters see 9 × 9 log-intensity patches "
         "and were trained on 120 000 patches from three other scenes; the network (two hidden layers, "
         f"{net.n_params():,} weights) is written in numpy.".replace(",", " "), width=165)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.95, bottom=0.2)
    save(fig, "ch46_despeckle")

# ==============================================================================================
# 6. Ship detection in K-distributed sea clutter: CA-CFAR versus a learned detector
CH = 24


def k_clutter(rng, n):
    """K-distributed intensity: correlated Gamma texture (shape 1.5, built from three squared smoothed Gaussian
    fields) times exponential speckle; mean 1."""
    tex = np.zeros((n, CH, CH))
    for _ in range(3):
        g = ndi.gaussian_filter(rng.normal(size=(n, CH, CH)), (0, 1.2, 1.2))
        g /= g.std(axis=(1, 2), keepdims=True)
        tex += g ** 2 / 3
    return tex * rng.exponential(1.0, (n, CH, CH))


def ship_chips(rng, n, kind):
    """kind 0: ship, 1: clutter only, 2: azimuth ambiguity ghost, 3: breaking-wave spikes."""
    X = k_clutter(rng, n)
    scr = np.zeros(n)
    yy, xx = np.mgrid[0:CH, 0:CH]
    for i in range(n):
        cy, cx = CH / 2 + rng.uniform(-2, 2, 2)
        if kind == 0:
            L = rng.uniform(2, 7)
            th = rng.uniform(0, np.pi)
            s_db = rng.uniform(3, 20)
            scr[i] = s_db
            u = (xx - cx) * np.cos(th) + (yy - cy) * np.sin(th)
            v = -(xx - cx) * np.sin(th) + (yy - cy) * np.cos(th)
            body = np.exp(-0.5 * ((np.maximum(np.abs(u) - L / 2, 0) / 0.6) ** 2 + (v / 0.6) ** 2))
            side = 0.05 * (np.exp(-0.5 * ((yy - cy) / 0.6) ** 2) * (np.abs(xx - cx) < 5)
                           + np.exp(-0.5 * ((xx - cx) / 0.6) ** 2) * (np.abs(yy - cy) < 5))
            T = 10 ** (s_db / 10) * (body + side) * rng.gamma(4, 0.25, (CH, CH))
            X[i] += T
        elif kind == 2:
            Lg = rng.uniform(7, 14)
            s_db = rng.uniform(2, 8)
            ghost = np.exp(-0.5 * (((xx - cx) / 0.9) ** 2 + (np.maximum(np.abs(yy - cy) - Lg / 2, 0) / 1.5) ** 2))
            X[i] += 10 ** (s_db / 10) * ghost * rng.exponential(1.0, (CH, CH))
        elif kind == 3:
            for _ in range(rng.integers(1, 4)):
                py, px = (np.array([cy, cx]) + rng.uniform(-4, 4, 2)).astype(int)
                X[i, py, px] += 10 ** (rng.uniform(9, 15) / 10)
    return X, scr


def cfar_stat(X):
    inner = np.zeros((CH, CH), bool)
    c = CH // 2
    inner[c - 5:c + 6, c - 5:c + 6] = True
    bg = X[:, ~inner].mean(1)
    sm = ndi.uniform_filter(X, (1, 2, 2))
    return sm[:, c - 4:c + 4, c - 4:c + 4].reshape(len(X), -1).max(1) / bg


def net_input(X):
    inner = np.zeros((CH, CH), bool)
    c = CH // 2
    inner[c - 5:c + 6, c - 5:c + 6] = True
    bg = X[:, ~inner].mean(1)
    return np.log(X / bg[:, None, None] + 0.05).reshape(len(X), -1) / 2.0


def roc(score, y):
    order = np.argsort(-score)
    ys = y[order]
    tp = np.cumsum(ys) / ys.sum()
    fp = np.cumsum(~ys) / (~ys).sum()
    return fp, tp


def ships():
    rng = np.random.default_rng(46)
    def dataset(npos, nneg):
        Xp, scr = ship_chips(rng, npos, 0)
        parts = [ship_chips(rng, int(nneg * f), k)[0] for k, f in ((1, 0.6), (2, 0.2), (3, 0.2))]
        Xn = np.concatenate(parts)
        kinds = np.concatenate([np.full(len(p), k) for p, k in zip(parts, (1, 2, 3))])
        X = np.concatenate([Xp, Xn])
        y = np.concatenate([np.ones(npos, bool), np.zeros(len(Xn), bool)])
        return X, y, np.concatenate([scr, np.full(len(Xn), np.nan)]), np.concatenate([np.zeros(npos), kinds])
    Xtr, ytr, _, _ = dataset(6000, 6000)
    # augmentation: flips and 90-degree rotations
    Xa = np.concatenate([np.rot90(Xtr, k, axes=(1, 2)) for k in range(4)]
                        + [np.rot90(Xtr[:, ::-1], k, axes=(1, 2)) for k in range(4)])
    ya = np.tile(ytr, 8).astype(int)
    net = NumpyNet(CH * CH, (64,), 2, seed=4).fit(net_input(Xa), ya, epochs=6, lr=1.5e-3, batch=256, wd=1e-4)
    Xte, yte, scr_te, kind_te = dataset(6000, 30000)
    s_cfar = cfar_stat(Xte)
    s_net = net.predict_proba(net_input(Xte))[:, 1]
    res = {}
    for name, sc in (("CFAR", s_cfar), ("Net", s_net)):
        fp, tp = roc(sc, yte)
        auc = np.trapezoid(tp, fp)
        out = {"fp": fp, "tp": tp, "auc": auc}
        for pfa in (1e-2, 1e-3):
            thr = np.quantile(sc[~yte], 1 - pfa)
            out[pfa] = (thr, (sc[yte] > thr).mean())
        # false-alarm breakdown at PFA 1e-2
        thr = out[1e-2][0]
        fa = sc[~yte] > thr
        kinds = kind_te[~yte]
        out["fa_kind"] = [(fa & (kinds == k)).sum() for k in (1, 2, 3)]
        res[name] = out
        print(f"ships {name}: AUC={auc:.3f}  PD@1e-2={out[1e-2][1]*100:.1f}%  PD@1e-3={out[1e-3][1]*100:.1f}%  "
              f"false alarms at 1e-2 by kind (clutter, ghost, spikes) = {out['fa_kind']}")
    print("ships net params", net.n_params())

    fig = plt.figure(figsize=(7.0, 2.55))
    gsl = fig.add_gridspec(2, 3, left=0.01, right=0.29, top=0.86, bottom=0.34, wspace=0.08, hspace=0.25)
    gsr = fig.add_gridspec(1, 2, left=0.37, right=0.99, top=0.88, bottom=0.34, wspace=0.32)
    rr = np.random.default_rng(9)
    ex = []
    for k, s_want in ((0, 6), (0, 11), (0, 16)):
        while True:
            Xc, sc = ship_chips(rr, 1, 0)
            if abs(sc[0] - s_want) < 0.8:
                break
        ex.append((Xc[0], f"ship {s_want} dB"))
    for k, lab in ((1, "spiky clutter"), (2, "ambiguity ghost"), (3, "wave spikes")):
        ex.append((ship_chips(rr, 1, k)[0][0], lab))
    cells = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    for (im, lab), (r0, c0) in zip(ex, cells):
        ax = fig.add_subplot(gsl[r0, c0])
        ax.imshow(10 * np.log10(im), cmap="gray", vmin=-8, vmax=18, interpolation="nearest")
        img_axes(ax)
        ax.text(0.5, -0.05, lab, transform=ax.transAxes, fontsize=5.6, ha="center", va="top")
    fig.text(0.01, 0.93, "(a) Example 24 × 24-pixel chips", fontsize=7.4, weight="bold", ha="left")
    ax = fig.add_subplot(gsr[0, 0])
    for name, col, lab in (("CFAR", ORANGE, "CA-CFAR"), ("Net", BLUE, "Learned (numpy net)")):
        ax.plot(np.maximum(res[name]["fp"], 1e-5), res[name]["tp"], color=col,
                label=f"{lab}, AUC {res[name]['auc']:.3f}")
    ax.set_xscale("log")
    ax.set_xlim(1e-4, 1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("False-alarm probability per chip", fontsize=6.8)
    ax.set_ylabel("Detection probability", fontsize=6.8)
    ax.tick_params(labelsize=6.3)
    ax.legend(fontsize=5.9, loc="upper left", handlelength=1.4)
    ax.set_title("(b) ROC curves", fontsize=7.4, loc="left")
    ax = fig.add_subplot(gsr[0, 1])
    bins = np.arange(3, 20.1, 1.7)
    mid = (bins[:-1] + bins[1:]) / 2
    for name, sc, col, lab in (("CFAR", s_cfar, ORANGE, "CA-CFAR"), ("Net", s_net, BLUE, "Learned")):
        thr = res[name][1e-2][0]
        pdv = [(sc[yte & (scr_te >= a) & (scr_te < b)] > thr).mean() for a, b in zip(bins[:-1], bins[1:])]
        ax.plot(mid, pdv, "o-", color=col, ms=3, label=lab)
    ax.set_xlabel("Ship signal-to-clutter ratio (dB)", fontsize=6.8)
    ax.set_ylabel("Detection probability", fontsize=6.8)
    ax.set_ylim(0, 1.02)
    ax.tick_params(labelsize=6.3)
    ax.legend(fontsize=5.9, loc="lower right", handlelength=1.4)
    ax.set_title("(c) At 1 % false alarms", fontsize=7.4, loc="left")
    foot(fig, "Synthetic Sentinel-1-like chips: K-distributed sea clutter (shape 1.5), ships 2–7 pixels long at 3–20 dB "
         "above the clutter, and look-alikes (azimuth ghosts, breaking-wave spikes). Training: 12 000 chips with "
         "flips and rotations; test: 6 000 ships and 30 000 negatives. CA-CFAR: brightest 2 × 2 mean over the "
         "background ring mean.", width=150)
    save(fig, "ch46_ships")

# ==============================================================================================
# 7. Flood mapping from Sentinel-1-like data: Otsu threshold, threshold + HAND mask, learned classifier
def flood_scene(seed, n=200):
    rng = np.random.default_rng(seed)
    hflood = rng.uniform(2.0, 5.0)
    yy, xx = np.mgrid[0:n, 0:n].astype(float)
    xr = n / 2 + 0.16 * n * np.sin(yy / (0.2 * n) + rng.uniform(0, 6)) + 0.05 * n * np.sin(yy / (0.07 * n))
    dist = np.abs(xx - xr)
    hills = ndi.gaussian_filter(rng.normal(size=(n, n)), 7)
    hills = np.maximum(hills / hills.std(), 0)
    hand = 0.09 * dist ** 1.15 + 7 * hills * (dist > 18)
    channel = dist < 2.5
    # land cover parcels
    pts = rng.uniform(0, n, (60, 2))
    parcel = ((yy[..., None] - pts[:, 0]) ** 2 + (xx[..., None] - pts[:, 1]) ** 2).argmin(-1)
    lc = rng.choice(4, 60, p=[0.6, 0.22, 0.1, 0.08])[parcel]       # 0 open, 1 forest, 2 urban, 3 smooth sand/tarmac
    # radar shadow on steep slopes facing away from the radar (radar looks from the left)
    gx = ndi.sobel(hand, axis=1) / 8
    shadow = (gx < -1.6) & (hand > 8)
    level = hflood + 0.8 * ndi.gaussian_filter(rng.normal(size=(n, n)), 15) / 0.03   # uneven water surface
    flood = (hand < level) & ~channel
    ponds = (ndi.gaussian_filter(rng.normal(size=(n, n)), 3) > 0.21) & (hand > 8) & ~flood   # rain-fed ponds
    flood |= ponds
    water = channel | flood
    VV = np.select([lc == 0, lc == 1, lc == 2, lc == 3], [-10.0, -7.0, 0.0, -17.0])
    VH = np.select([lc == 0, lc == 1, lc == 2, lc == 3], [-17.0, -12.5, -8.0, -25.0])
    VV = VV + rng.normal(0, 1.2, 60)[parcel]
    VH = VH + rng.normal(0, 1.2, 60)[parcel]
    pre_vv, pre_vh = VV.copy(), VH.copy()
    pre_vv[channel] = -21.0; pre_vh[channel] = -28.0
    post_vv, post_vh = pre_vv.copy(), pre_vh.copy()
    ow = water & ((lc == 0) | (lc == 3) | channel)
    post_vv[ow] = -21.0; post_vh[ow] = -28.0
    fv = flood & (lc == 1)
    post_vv[fv] = -4.5; post_vh[fv] = -12.0                           # flooded forest: some double bounce
    fu = flood & (lc == 2)
    post_vv[fu] = 2.5; post_vh[fu] = -6.5                             # flooded urban
    post_vv += 1.0 * (lc == 0) * (~water) * rng.normal(0, 1, 60)[parcel]   # soil moisture change after rain
    for a in (pre_vv, pre_vh, post_vv, post_vh):
        a[shadow] = -24.0 if a is pre_vv or a is post_vv else -29.0
    out = []
    for a in (pre_vv, pre_vh, post_vv, post_vh):
        lin = 10 ** (a / 10) * rng.gamma(4.4, 1 / 4.4, (n, n))          # GRD-like speckle, ~4.4 looks
        out.append(10 * np.log10(lin))
    hand_obs = np.maximum(hand + 1.5 * ndi.gaussian_filter(rng.normal(size=(n, n)), 4) / 0.07, 0)   # DEM errors
    return out, hand_obs, water, lc, shadow


def otsu(v, nb=256):
    h, e = np.histogram(v, nb)
    c = (e[:-1] + e[1:]) / 2
    w0 = np.cumsum(h); w1 = w0[-1] - w0
    m0 = np.cumsum(h * c) / np.maximum(w0, 1)
    m1 = (np.sum(h * c) - np.cumsum(h * c)) / np.maximum(w1, 1)
    return c[np.argmax(w0 * w1 * (m0 - m1) ** 2)]


def flood_feats(imgs, hand):
    pre_vv, pre_vh, post_vv, post_vh = [ndi.uniform_filter(a, 3) for a in imgs]
    f = [post_vv, post_vh, pre_vv, pre_vh, post_vv - pre_vv, post_vh - pre_vh, hand, imgs[2]]
    return np.stack(f, -1).reshape(-1, len(f))


def iou(p, t):
    return (p & t).sum() / max((p | t).sum(), 1)


def flood():
    from sklearn.ensemble import RandomForestClassifier
    Xs, ys = [], []
    rng = np.random.default_rng(1)
    for sd in (301, 302, 303):
        imgs, hand, water, lc, sh = flood_scene(sd)
        F = flood_feats(imgs, hand)
        idx = rng.choice(F.shape[0], 15000, replace=False)
        Xs.append(F[idx]); ys.append(water.ravel()[idx])
    rf = RandomForestClassifier(n_estimators=150, min_samples_leaf=3, random_state=0, n_jobs=2)
    rf.fit(np.vstack(Xs), np.concatenate(ys))
    imgs, hand, water, lc, shadow = flood_scene(46)
    vv = ndi.uniform_filter(imgs[2], 3)
    t = otsu(vv)
    p1 = vv < t
    p2 = p1 & (hand < 10)
    p3 = rf.predict(flood_feats(imgs, hand)).reshape(water.shape).astype(bool)
    res = {"Otsu": iou(p1, water), "Otsu + HAND": iou(p2, water), "Learned (RF)": iou(p3, water)}
    for k, v in res.items():
        print(f"flood {k}: IoU={v:.3f}")
    fl_veg = water & ((lc == 1) | (lc == 2)) & (imgs[2] > -12)
    print(f"flood Otsu thr={t:.1f} dB; flooded veg/urban px={fl_veg.sum()}, found by Otsu+HAND={((p2) & fl_veg).sum()},"
          f" by RF={(p3 & fl_veg).sum()}; shadow px={shadow.sum()}, Otsu FP in shadow={(p1 & shadow).sum()}, "
          f"after HAND={(p2 & shadow).sum()}; water px={water.sum()} of {water.size}")

    def outcome(p):
        base = np.clip((vv + 25) / 27, 0, 1)[..., None].repeat(3, -1) * 0.6 + 0.3
        o = base.copy()
        o[p & water] = [0.12, 0.42, 0.75]
        o[p & ~water] = [0.75, 0.15, 0.2]
        o[~p & water] = [0.95, 0.62, 0.1]
        return o
    fig = plt.figure(figsize=(7.0, 4.7))
    gs = fig.add_gridspec(2, 3, hspace=0.42, wspace=0.14)
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(imgs[2], cmap="gray", vmin=-26, vmax=4, interpolation="nearest")
    img_axes(ax)
    ax.set_title("(a) VV backscatter after the flood", fontsize=7.4, loc="left")
    ax = fig.add_subplot(gs[0, 1])
    bins = np.linspace(-30, 8, 77)
    ax.hist(vv[water], bins, color=BLUE, alpha=0.75, label="water (reference)")
    ax.hist(vv[~water & ~shadow], bins, color=GREY, alpha=0.6, label="dry land")
    ax.hist(vv[shadow], bins, color=VIOLET, alpha=0.8, label="radar shadow")
    ax.axvline(t, color=RED, lw=1.0, ls="--")
    ax.text(t - 0.6, ax.get_ylim()[1] * 0.97, f"Otsu\n{t:.1f} dB", color=RED, fontsize=6.0, va="top", ha="right")
    ax.set_xlabel("VV (dB, 3 × 3 mean)", fontsize=6.8)
    ax.set_ylabel("Pixels", fontsize=6.8)
    ax.tick_params(labelsize=6.2)
    ax.legend(fontsize=5.8, loc="upper right", handlelength=1.0)
    ax.set_title("(b) Histogram", fontsize=7.4, loc="left")
    ax = fig.add_subplot(gs[0, 2])
    ref = np.zeros(water.shape + (3,)) + 0.93
    ref[water] = [0.12, 0.42, 0.75]
    ref[water & ((lc == 1) | (lc == 2)) & ~(np.abs(imgs[2]) > 99)] = [0.12, 0.42, 0.75]
    ref[fl_veg] = [0.3, 0.7, 0.85]
    ref[shadow] = [0.6, 0.5, 0.75]
    ax.imshow(ref, interpolation="nearest")
    img_axes(ax)
    ax.set_title("(c) Reference water", fontsize=7.4, loc="left")
    ax.legend([Rectangle((0, 0), 1, 1, fc=c) for c in ([0.12, 0.42, 0.75], [0.3, 0.7, 0.85], [0.6, 0.5, 0.75])],
              ["open water", "flooded forest/urban", "radar shadow (dry)"], fontsize=5.6, loc="lower left",
              handlelength=0.9, framealpha=0.85, frameon=True)
    for i, (t_, p) in enumerate((("(d) Otsu + HAND < 10 m", p2), ("(e) Learned (random forest)", p3))):
        ax = fig.add_subplot(gs[1, i])
        ax.imshow(outcome(p), interpolation="nearest")
        img_axes(ax)
        ax.set_title(t_, fontsize=7.4, loc="left")
    ax.legend([Rectangle((0, 0), 1, 1, fc=c) for c in ([0.12, 0.42, 0.75], [0.75, 0.15, 0.2], [0.95, 0.62, 0.1])],
              ["correct", "false alarm", "missed"], fontsize=5.6, loc="lower left", handlelength=0.9,
              framealpha=0.85, frameon=True)
    ax = fig.add_subplot(gs[1, 2])
    names = list(res.keys())
    ax.bar(range(3), [res[k] for k in names], 0.55, color=[GREY, ORANGE, BLUE])
    for k, nm in enumerate(names):
        ax.text(k, res[nm] + 0.02, f"{res[nm]:.2f}", ha="center", fontsize=6.3)
    ax.set_xticks(range(3))
    ax.set_xticklabels(["Otsu", "Otsu +\nHAND", "Learned\n(RF)"], fontsize=6.4)
    ax.set_ylim(0, 1.05)
    ax.tick_params(labelsize=6.3)
    ax.set_ylabel("Water IoU", fontsize=6.8)
    ax.set_title("(f) Intersection over union", fontsize=7.4, loc="left")
    foot(fig, "Synthetic 200 × 200-pixel Sentinel-1-like scene (VV and VH, before and after, about 4.4 looks) over a "
         "valley; floodwater fills land up to 2–5 m above the river (HAND, uneven), plus a few ponds; the HAND map given to the models carries ±1.5 m DEM errors. Look-alikes: smooth sand or tarmac, "
         "radar shadow on hills; flooded forest and buildings appear bright. Random forest: 150 trees, 8 features, "
         "trained on three other scenes.", width=160)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.16)
    save(fig, "ch46_flood")

# ==============================================================================================
# 8. Methane plumes: integrated mass enhancement (IME) and a learned effective wind speed
PPB_TO_KGM2 = 1e-9 * (101325 / 9.81 / 0.02897) * 0.01604        # column mass per ppb of XCH4 (dry air, 1 atm)


def plume(rng, Q_kgh, U10, n=80, dx=30.0, noise_ppb=50.0):
    """Column enhancement (kg/m2) of a puffy Gaussian plume from a point source, with retrieval noise."""
    Up = U10 * rng.uniform(0.7, 1.4) + 0.5                       # transport wind in the plume layer
    th = rng.normal(0, 0.15)
    yy, xx = (np.mgrid[0:n, 0:n] + 0.5) * dx
    x0, y0 = 8 * dx, n / 2 * dx
    xr = (xx - x0) * np.cos(th) + (yy - y0) * np.sin(th)
    yr = -(xx - x0) * np.sin(th) + (yy - y0) * np.cos(th)
    sig = 0.25 * np.maximum(xr, 0) ** 0.9 + 15.0
    Q = Q_kgh / 3600.0
    om = np.where(xr > -dx, Q / (np.sqrt(2 * np.pi) * sig * Up) * np.exp(-yr ** 2 / (2 * sig ** 2)), 0)
    om *= np.exp(-np.maximum(-xr, 0) / dx)
    puff = np.exp(0.35 * ndi.gaussian_filter(rng.normal(size=(n, n)), 2.5) / 0.11)
    om *= puff / puff.mean()
    noise = rng.normal(0, noise_ppb, (n, n)) + 15 * ndi.gaussian_filter(rng.normal(size=(n, n)), 3) / 0.094
    return om + noise * PPB_TO_KGM2, om, Up, (x0, y0)


def ime_estimate(obs, dx=30.0):
    sm = ndi.gaussian_filter(obs, 1.0)
    sd = 1.4826 * np.median(np.abs(sm - np.median(sm)))            # robust noise level of the smoothed image
    thr = 2.0 * sd
    lab, nl = ndi.label(sm > thr)
    n = obs.shape[0]
    src = lab[n // 2 - 3:n // 2 + 4, 6:12]
    ids = np.unique(src[src > 0])
    if len(ids) == 0:
        return np.nan, np.nan, np.zeros_like(obs, bool)
    mask = np.isin(lab, ids)
    A = dx * dx
    ime = obs[mask].sum() * A
    L = np.sqrt(mask.sum() * A)
    return ime, L, mask


def methane():
    rng = np.random.default_rng(46)
    rows = []
    for i in range(500):
        Q = 10 ** rng.uniform(np.log10(300), np.log10(5000))
        U10 = rng.uniform(1.5, 8.0)
        obs, om, Up, _ = plume(rng, Q, U10)
        ime, L, mask = ime_estimate(obs)
        rows.append((Q, U10, ime, L))
    R = np.array(rows)
    ok = np.isfinite(R[:, 2]) & (R[:, 2] > 0)
    R = R[ok]
    tr, te = R[:300], R[300:]
    ueff = tr[:, 0] / 3600 * tr[:, 3] / tr[:, 2]
    A = np.vstack([tr[:, 1], np.ones(len(tr))]).T
    alpha, beta = np.linalg.lstsq(A, ueff, rcond=None)[0]
    q_exact = (alpha * te[:, 1] + beta) * te[:, 2] / te[:, 3] * 3600
    u_err = np.maximum(te[:, 1] + np.random.default_rng(1).normal(0, 1.0, len(te)), 0.5)
    q_werr = (alpha * u_err + beta) * te[:, 2] / te[:, 3] * 3600
    e1 = np.abs(q_exact / te[:, 0] - 1)
    e2 = np.abs(q_werr / te[:, 0] - 1)
    print(f"methane: fitted Ueff = {alpha:.2f} U10 + {beta:.2f} m/s  (n_train={len(tr)}, n_test={len(te)}, "
          f"detected {ok.sum()} of 500)")
    print(f"methane: median |error| exact wind {np.median(e1)*100:.0f}%  with 1 m/s wind error "
          f"{np.median(e2)*100:.0f}%; 90th pct {np.percentile(e1,90)*100:.0f}% / {np.percentile(e2,90)*100:.0f}%")
    # example plume
    rr = np.random.default_rng(7)
    obs, om, Up, (x0, y0) = plume(rr, 1500.0, 4.0)
    ime, L, mask = ime_estimate(obs)
    qhat = (alpha * 4.0 + beta) * ime / L * 3600
    print(f"methane example: Q=1500 kg/h U10=4 -> IME={ime:.1f} kg, L={L:.0f} m, mask px={mask.sum()}, "
          f"Q_est={qhat:.0f} kg/h")

    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.55), gridspec_kw={"width_ratios": [1.0, 1.05, 1.05]})
    ax = axs[0]
    im = ax.imshow(ndi.gaussian_filter(obs, 0.6) / PPB_TO_KGM2, cmap="magma", vmin=-80, vmax=400,
                   extent=(0, 2.4, 0, 2.4), origin="lower")
    ax.contour(np.linspace(0.015, 2.385, 80), np.linspace(0.015, 2.385, 80), mask, levels=[0.5], colors=[SKY],
               linewidths=0.8)
    ax.plot(x0 / 1000, y0 / 1000, "^", color="white", ms=4)
    ax.set_xlabel("km", fontsize=6.6)
    ax.tick_params(labelsize=6.2)
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.ax.tick_params(labelsize=5.8)
    cb.set_label("ΔXCH₄ (ppb)", fontsize=6.2)
    ax.set_title("(a) Plume and mask", fontsize=7.4, loc="left")
    ax.text(0.05, 2.3, f"true 1 500 kg/h\nestimate {qhat:,.0f} kg/h".replace(",", " "), color="white", fontsize=5.8,
            va="top")
    ax = axs[1]
    ax.plot(tr[:, 1], ueff, "o", ms=2.2, color=GREY, alpha=0.6, label="simulated plumes")
    uu = np.linspace(1, 8.5, 10)
    ax.plot(uu, alpha * uu + beta, color=RED, lw=1.4, label=f"fit: {alpha:.2f} U₁₀ + {beta:.2f}")
    ax.set_xlabel("Wind speed at 10 m, U₁₀ (m/s)", fontsize=6.6)
    ax.set_ylabel("Effective wind Q·L/IME (m/s)", fontsize=6.6)
    ax.tick_params(labelsize=6.2)
    ax.legend(fontsize=5.8, loc="upper left", handlelength=1.2)
    ax.set_title("(b) Learning the effective wind", fontsize=7.4, loc="left")
    ax = axs[2]
    ax.loglog(te[:, 0], q_werr, "o", ms=2.2, color=ORANGE, alpha=0.6,
              label=f"wind error 1 m/s (median {np.median(e2)*100:.0f} %)")
    ax.loglog(te[:, 0], q_exact, "o", ms=2.2, color=BLUE, alpha=0.7,
              label=f"exact wind (median {np.median(e1)*100:.0f} %)")
    ax.plot([200, 8000], [200, 8000], color=INK, lw=0.8, ls="--")
    ax.set_xlim(250, 6000)
    ax.set_ylim(150, 12000)
    from matplotlib.ticker import FixedLocator, NullFormatter, FixedFormatter
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_locator(FixedLocator([300, 1000, 3000, 10000]))
        axis.set_major_formatter(FixedFormatter(["300", "1 000", "3 000", "10 000"]))
        axis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("True emission (kg/h)", fontsize=6.6)
    ax.set_ylabel("Estimated emission (kg/h)", fontsize=6.6)
    ax.tick_params(labelsize=6.2)
    ax.legend(fontsize=5.6, loc="upper left", handlelength=1.0)
    ax.set_title("(c) IME estimates on test plumes", fontsize=7.4, loc="left")
    foot(fig, "Synthetic 30 m imagery (2.4 km × 2.4 km): puffy Gaussian plumes, 300–5 000 kg/h, winds 1.5–8 m/s, "
         "50 ppb pixel noise plus correlated surface artefacts. Mask: smoothed image above 2σ, connected to the source. "
         f"U_eff fitted on {len(tr)} plumes, tested on {len(te)}. Q = U_eff · IME / L, L = √(mask area).", width=160)
    fig.tight_layout(rect=(0, 0.09, 1, 1), w_pad=0.8)
    save(fig, "ch46_methane")

# ==============================================================================================
# 9. Clouds and smart tasking: Monte Carlo of a pass with 20 candidate targets and room for 6 images
def tasking():
    from scipy.stats import norm, beta as betad
    rng = np.random.default_rng(46)
    N, M, P = 20, 6, 4000
    kappa = 1.2
    means = np.sort(np.r_[np.linspace(0.1, 0.9, 17), 0.67])
    rho_track, rho_fc = 0.6, 0.7
    res = {k: [] for k in ("blind", "forecast", "lookahead", "share_raw", "share_scr", "saved", "lost")}
    for m in means:
        z = np.zeros((P, N))
        z[:, 0] = rng.normal(size=P)
        for j in range(1, N):
            z[:, j] = rho_track * z[:, j - 1] + np.sqrt(1 - rho_track ** 2) * rng.normal(size=P)
        c = betad.ppf(norm.cdf(z), m * kappa, (1 - m) * kappa)
        useful = c < 0.2
        blind = useful[:, :M].sum(1).mean()
        zf = rho_fc * z + np.sqrt(1 - rho_fc ** 2) * rng.normal(size=z.shape)
        zl = 0.97 * z + np.sqrt(1 - 0.97 ** 2) * rng.normal(size=z.shape)
        pick_f = np.argsort(zf, 1)[:, :M]
        pick_l = np.argsort(zl, 1)[:, :M]
        res["blind"].append(blind)
        res["forecast"].append(np.take_along_axis(useful, pick_f, 1).sum(1).mean())
        res["lookahead"].append(np.take_along_axis(useful, pick_l, 1).sum(1).mean())
        # onboard screening of blind images: keep if estimated cloud fraction < 0.5 (classifier error 0.08)
        ch = np.clip(c + rng.normal(0, 0.08, c.shape), 0, 1)
        keep = ch < 0.5
        res["share_raw"].append(useful.mean())
        res["share_scr"].append((useful & keep).sum() / max(keep.sum(), 1))
        res["saved"].append(1 - keep.mean())
        res["lost"].append((useful & ~keep).sum() / max(useful.sum(), 1))
    for k in res:
        res[k] = np.array(res[k])
    for mm in (0.3, 0.55, 0.67):
        i = int(np.argmin(np.abs(means - mm)))
        print(f"tasking m={means[i]:.2f}: useful of {M}: blind {res['blind'][i]:.2f}, forecast {res['forecast'][i]:.2f}, "
              f"look-ahead {res['lookahead'][i]:.2f}; useful share raw {res['share_raw'][i]*100:.0f}% -> screened "
              f"{res['share_scr'][i]*100:.0f}%, downlink saved {res['saved'][i]*100:.0f}%, clear lost "
              f"{res['lost'][i]*100:.1f}%")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.7))
    ax = axs[0]
    x = means * 100
    ax.plot(x, res["lookahead"], "-", color=GREEN, label="look-ahead on board (dynamic targeting)")
    ax.plot(x, res["forecast"], "-", color=BLUE, label="cloud-forecast tasking")
    ax.plot(x, res["blind"], "-", color=GREY, label="blind tasking")
    ax.axvline(67, color=GOLD, lw=0.8, ls=":")
    ax.text(66, 0.25, "global mean ≈ 67 %", fontsize=5.8, color=GOLD, va="bottom", ha="right")
    ax.set_xlabel("Mean cloud cover over the targets (%)", fontsize=6.8)
    ax.set_ylabel(f"Clear images per pass (of {M})", fontsize=6.8)
    ax.set_ylim(0, 8.6)
    ax.set_yticks(range(7))
    ax.tick_params(labelsize=6.3)
    ax.legend(fontsize=5.8, loc="upper right", handlelength=1.4)
    ax.set_title("(a) Choosing what to image", fontsize=7.4, loc="left")
    ax = axs[1]
    ax.plot(x, res["share_scr"] * 100, "-", color=VIOLET, label="useful share, with onboard screening")
    ax.plot(x, res["share_raw"] * 100, "-", color=GREY, label="useful share, no screening")
    ax.plot(x, res["saved"] * 100, "--", color=ORANGE, label="downlink saved by screening")
    ax.plot(x, res["lost"] * 100, ":", color=RED, label="clear images wrongly discarded")
    ax.set_xlabel("Mean cloud cover over the targets (%)", fontsize=6.8)
    ax.set_ylabel("Per cent", fontsize=6.8)
    ax.set_ylim(0, 150)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.tick_params(labelsize=6.3)
    ax.legend(fontsize=5.8, loc="upper left", handlelength=1.6, ncol=2, columnspacing=1.0)
    ax.set_title("(b) Screening what to send down", fontsize=7.4, loc="left")
    foot(fig, "Monte Carlo, 4 000 passes per point: 20 candidate targets per pass, room for 6 images; scene cloud "
         "fractions follow a U-shaped beta distribution, correlated along track (ρ = 0.6). An image is useful if "
         "under 20 % cloudy. Forecast skill: correlation 0.7 with the truth; look-ahead camera: 0.97. Screening "
         "keeps images estimated under 50 % cloudy (error 0.08).", width=165)
    fig.tight_layout(rect=(0, 0.1, 1, 1), w_pad=1.5)
    save(fig, "ch46_tasking")

# ==============================================================================================
# 10. Pitfalls: domain shift (sensor gain) and area estimation from a map with errors
def pitfalls():
    from sklearn.ensemble import RandomForestClassifier
    img_a, cls_a = lc_scene(46)
    rng = np.random.default_rng(2)
    n = cls_a.size
    idx = rng.choice(n, 6000, replace=False)
    Xa, ya = pixel_feats(img_a).reshape(-1, 9)[idx], cls_a.ravel()[idx]

    def rf():
        return RandomForestClassifier(150, min_samples_leaf=2, random_state=0, n_jobs=2)
    rf_a = rf().fit(Xa, ya)
    # augmentation: random band gains and offsets applied to the source-domain reflectances
    ra = img_a.reshape(-1, 6)[idx]
    aug = []
    for k in range(4):
        g = rng.uniform(0.9, 1.15, (len(ra), 6)) * rng.uniform(0.9, 1.1, (len(ra), 1))
        o = rng.uniform(0, 0.03, (len(ra), 1)) * np.array([1, 0.7, 0.4, 0.15, 0, 0])
        aug.append(np.clip(ra * g + o, 0.001, 1))
    Xaug = np.concatenate([Xa] + [pixel_feats(a_[:, None, :])[:, 0, :] for a_ in aug])
    rf_aug = rf().fit(Xaug, np.tile(ya, 5))
    shifts = np.linspace(0, 1.5, 7)
    acc = {"A": [], "aug": [], "few": []}
    for sh in shifts:
        img_b, cls_b = lc_scene(47, shift=sh)
        Fb = pixel_feats(img_b).reshape(-1, 9)
        yb = cls_b.ravel()
        rb = np.random.default_rng(3)
        few = np.concatenate([rb.choice(np.where(yb == k)[0], 40, replace=False) for k in range(6)])
        test = np.setdiff1d(rb.choice(len(yb), 12000, replace=False), few)
        rf_few = rf().fit(np.vstack([Xa, Fb[few]]), np.concatenate([ya, yb[few]]),
                          sample_weight=np.concatenate([np.ones(len(ya)), np.full(len(few), 10.0)]))
        acc["A"].append((rf_a.predict(Fb[test]) == yb[test]).mean())
        acc["aug"].append((rf_aug.predict(Fb[test]) == yb[test]).mean())
        acc["few"].append((rf_few.predict(Fb[test]) == yb[test]).mean())
    for k in acc:
        acc[k] = np.array(acc[k])
        print(f"pitfalls domain {k}: " + " ".join(f"{a*100:.1f}" for a in acc[k]))
    # area estimation (Olofsson et al. 2014): stratified sample of a loss / no-loss map
    N = 1_000_000
    true_loss = 30_000
    detected = int(0.65 * true_loss)                       # producer's accuracy 0.65
    false = 4_000
    map_loss = detected + false
    W1, W2 = map_loss / N, 1 - map_loss / N
    p1 = detected / map_loss                               # P(true loss | mapped loss) = user's accuracy
    p2 = (true_loss - detected) / (N - map_loss)           # P(true loss | mapped no loss) = omission rate
    print(f"pitfalls area: true loss {true_loss/1e4:.2f}% ; mapped {map_loss/1e4:.2f}% ; user's acc {p1:.3f} ; "
          f"omission share in no-loss stratum {p2*100:.2f}%")
    ns = np.array([100, 200, 400, 800, 1600, 3200])
    R = 400
    est_m, lo, hi, ci_m = [], [], [], []
    rs = np.random.default_rng(5)
    for nn in ns:
        n1 = n2 = nn // 2
        k1 = rs.binomial(n1, p1, R)
        k2 = rs.binomial(n2, p2, R)
        ph1, ph2 = k1 / n1, k2 / n2
        est = W1 * ph1 + W2 * ph2
        se = np.sqrt(W1 ** 2 * ph1 * (1 - ph1) / (n1 - 1) + W2 ** 2 * ph2 * (1 - ph2) / (n2 - 1))
        est_m.append(est.mean() * 100)
        lo.append(np.percentile(est, 2.5) * 100); hi.append(np.percentile(est, 97.5) * 100)
        ci_m.append((1.96 * se).mean() * 100)
        cover = (np.abs(est - true_loss / N) <= 1.96 * se).mean()
        print(f"pitfalls area n={nn}: mean est {est.mean()*100:.2f}%  95% range {lo[-1]:.2f}-{hi[-1]:.2f}%  "
              f"mean ±CI {ci_m[-1]:.2f}  coverage {cover*100:.0f}%")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.6))
    ax = axs[0]
    ax.plot(shifts, acc["A"] * 100, "o-", ms=3, color=ORANGE, label="trained on region A only")
    ax.plot(shifts, acc["aug"] * 100, "^-", ms=3, color=GREEN, label="A + spectral augmentation")
    ax.plot(shifts, acc["few"] * 100, "s-", ms=3, color=BLUE, label="A + 240 labels from region B")
    ax.set_xlabel("Shift of region B from A (0 = same climate)", fontsize=6.8)
    ax.set_ylabel("Accuracy on another scene (%)", fontsize=6.8)
    ax.tick_params(labelsize=6.3)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=5.9, loc="lower center", handlelength=1.4)
    ax.set_title("(a) Domain shift to a new region", fontsize=7.4, loc="left")
    ax = axs[1]
    ax.fill_between(ns, lo, hi, color=SKY, alpha=0.35, lw=0, label="95 % of repeated surveys")
    ax.plot(ns, est_m, "o-", ms=3, color=BLUE, label="stratified estimate (mean)")
    ax.axhline(true_loss / N * 100, color=INK, lw=1.0, ls="--", label="true loss area")
    ax.axhline(map_loss / N * 100, color=RED, lw=1.0, label="pixel count of the map")
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(v) for v in ns])
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlabel("Reference sample size (half in each map stratum)", fontsize=6.8)
    ax.set_ylabel("Forest loss (% of area)", fontsize=6.8)
    ax.set_ylim(1.0, 7.0)
    ax.tick_params(labelsize=6.3)
    ax.legend(fontsize=5.8, loc="upper right", handlelength=1.4)
    ax.set_title("(b) Area from a map with errors", fontsize=7.4, loc="left")
    foot(fig, "(a) Random forests trained on 6 000 pixels of a synthetic six-class scene (region A, as in the land-cover "
         "figure) and tested on 12 000 pixels of another scene whose soils, vegetation and haze shift towards a drier "
         "climate (shift 1: soils up to 35 % brighter, plant NIR 25 % lower, more haze). (b) A 10⁶-pixel map finds 65 % "
         "of 30 000 loss pixels and adds 4 000 false ones; 400 simulated surveys per sample size, estimator of "
         "Olofsson et al. (2014).", width=165)
    fig.tight_layout(rect=(0, 0.1, 1, 1), w_pad=1.5)
    save(fig, "ch46_pitfalls")


if __name__ == "__main__":
    fns = [pipeline, landcover, change, crops, despeckle, ships, flood, methane, tasking, pitfalls]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
