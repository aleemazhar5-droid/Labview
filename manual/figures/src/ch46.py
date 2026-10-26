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
    fig, ax = canvas(7.0, 3.55, xlim=(0, 100), ylim=(0, 50))
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


def lc_scene(seed, n=160):
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
    fig = plt.figure(figsize=(7.0, 5.0))
    gs = fig.add_gridspec(3, 4, height_ratios=[1, 0.10, 1.0], hspace=0.30, wspace=0.12)
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

    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.55), gridspec_kw={"width_ratios": [1.15, 0.9, 1.15]})
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
    ax.text(DOY[clx[i]][-1] - 4, 0.02, "one maize field,\n60 % cloudy dates", fontsize=5.8, ha="right", va="bottom")
    ax.set_xlabel("Day of year", fontsize=7)
    ax.set_ylabel("NDVI", fontsize=7)
    ax.set_ylim(-0.02, 1.05)
    ax.tick_params(labelsize=6.5)
    ax.legend(fontsize=5.6, loc="upper right", handlelength=1.2, ncol=2, columnspacing=0.6)
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
    foot(fig, "Synthetic fields: double-logistic NDVI curves (grass: three mowing cuts) with ±7-day timing shifts, "
         "amplitude spread and noise; 49 dates every 5 days; clouds remove dates at random and 5 % of 'clear' dates "
         f"carry undetected thin cloud. Both models trained on 5 000 fields, tested on 3 000 per point. Attention "
         f"network: four heads, {n_par:,} weights, numpy.".replace(",", " "), width=165)
    fig.tight_layout(rect=(0, 0.1, 1, 1), w_pad=1.0)
    save(fig, "ch46_crops")


if __name__ == "__main__":
    fns = [pipeline, landcover, change, crops]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
