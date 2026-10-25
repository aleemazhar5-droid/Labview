"""Figures for Chapter 43 - AI Foundations: Machine Learning for Space Engineers.

Most figures run real (small) machine-learning or optimisation code on synthetic data with fixed random
seeds: gradient descent, a multilayer perceptron written in numpy, scikit-learn classifiers, k-means/PCA
and spatial cross-validation.  Numbers quoted in the chapter text are printed by each function.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch  # noqa: F401
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap

FOOT = 6.0

# ----------------------------------------------------------------------------------------------
# Synthetic "cloud vs clear" two-band reflectance data (visible 0.65 um, short-wave infrared 1.6 um)
# Each surface or cloud type is a 2-D Gaussian.  Snow is bright in the visible but dark at 1.6 um,
# water clouds are bright in both, thin clouds overlap bright soil -> irreducible error.
# name, label (1 = cloud), weight, mean (vis, swir), sd (vis, swir), correlation
COMPONENTS = [
    ("Water", 0, 0.15, (0.05, 0.02), (0.020, 0.012), 0.3),
    ("Vegetation", 0, 0.17, (0.06, 0.22), (0.020, 0.045), 0.2),
    ("Soil", 0, 0.13, (0.24, 0.36), (0.050, 0.060), 0.6),
    ("Snow", 0, 0.08, (0.78, 0.12), (0.080, 0.050), 0.2),
    ("Bright desert", 0, 0.05, (0.40, 0.50), (0.060, 0.060), 0.6),
    ("Thick cloud", 1, 0.22, (0.72, 0.50), (0.100, 0.070), 0.6),
    ("Thin cloud", 1, 0.12, (0.30, 0.25), (0.080, 0.070), 0.6),
    ("Ice cloud", 1, 0.08, (0.55, 0.24), (0.090, 0.060), 0.4),
]
LABEL_NOISE = 0.10      # one label in ten is wrong (hand-drawn masks near cloud edges)


def _cov(sd, rho):
    return np.array([[sd[0] ** 2, rho * sd[0] * sd[1]], [rho * sd[0] * sd[1], sd[1] ** 2]])


def cloud_data(n, seed, noise=LABEL_NOISE, return_comp=False):
    rng = np.random.default_rng(seed)
    w = np.array([c[2] for c in COMPONENTS])
    w = w / w.sum()
    comp = rng.choice(len(COMPONENTS), size=n, p=w)
    X = np.zeros((n, 2))
    for k, (_, _, _, mu, sd, rho) in enumerate(COMPONENTS):
        idx = comp == k
        X[idx] = rng.multivariate_normal(mu, _cov(sd, rho), size=idx.sum())
    X = np.clip(X, 0.0, 1.1)
    y_true = np.array([COMPONENTS[k][1] for k in comp])
    flip = rng.random(n) < noise
    y = np.where(flip, 1 - y_true, y_true)
    if return_comp:
        return X, y, y_true, comp
    return X, y


def bayes_posterior(X):
    """Exact P(cloud | x) under the generating mixture (before label noise; clipping ignored)."""
    num = np.zeros(len(X))
    den = np.zeros(len(X))
    w = np.array([c[2] for c in COMPONENTS])
    w = w / w.sum()
    for k, (_, lab, _, mu, sd, rho) in enumerate(COMPONENTS):
        C = _cov(sd, rho)
        Ci = np.linalg.inv(C)
        d = X - np.array(mu)
        pdf = np.exp(-0.5 * np.einsum("ij,jk,ik->i", d, Ci, d)) / (2 * np.pi * np.sqrt(np.linalg.det(C)))
        den += w[k] * pdf
        if lab == 1:
            num += w[k] * pdf
    return num / np.maximum(den, 1e-300)


def bayes_error(noise=LABEL_NOISE, n=400000, seed=99):
    X, y, yt = cloud_data(n, seed, noise=0.0, return_comp=False)[0], None, None
    p = bayes_posterior(X)
    clean = np.mean(np.minimum(p, 1 - p))
    return noise + (1 - 2 * noise) * clean, clean


# ----------------------------------------------------------------------------------------------
# A small multilayer perceptron written directly in numpy (ReLU hidden layers, sigmoid output,
# binary cross-entropy loss, backpropagation, Adam optimiser).
class NumpyMLP:
    def __init__(self, sizes, seed=0):
        rng = np.random.default_rng(seed)
        self.W = [rng.normal(0, np.sqrt(2.0 / sizes[i]), (sizes[i], sizes[i + 1])) for i in range(len(sizes) - 1)]
        self.b = [np.zeros(sizes[i + 1]) for i in range(len(sizes) - 1)]
        self.m = [np.zeros_like(p) for p in self.W + self.b]
        self.v = [np.zeros_like(p) for p in self.W + self.b]
        self.t = 0

    def forward(self, X):
        acts = [X]
        h = X
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = h @ W + b
            h = np.maximum(z, 0.0) if i < len(self.W) - 1 else z
            acts.append(h)
        return acts

    def logits(self, X):
        return self.forward(X)[-1][:, 0]

    def proba(self, X):
        return 1.0 / (1.0 + np.exp(-self.logits(X)))

    @staticmethod
    def bce(z, y):
        # numerically stable binary cross-entropy with logits
        return np.mean(np.maximum(z, 0) - z * y + np.log1p(np.exp(-np.abs(z))))

    def loss(self, X, y):
        return self.bce(self.logits(X), y)

    def step(self, X, y, lr=0.01, l2=0.0, b1=0.9, b2=0.999, eps=1e-8):
        acts = self.forward(X)
        z = acts[-1][:, 0]
        p = 1.0 / (1.0 + np.exp(-z))
        d = ((p - y) / len(y))[:, None]                  # dLoss/dz for each sample
        gW, gb = [None] * len(self.W), [None] * len(self.W)
        for i in range(len(self.W) - 1, -1, -1):        # backpropagation, layer by layer
            gW[i] = acts[i].T @ d + l2 * self.W[i]
            gb[i] = d.sum(axis=0)
            if i > 0:
                d = (d @ self.W[i].T) * (acts[i] > 0)
        self.t += 1
        params = self.W + self.b
        grads = gW + gb
        for k, (p_, g) in enumerate(zip(params, grads)):
            self.m[k] = b1 * self.m[k] + (1 - b1) * g
            self.v[k] = b2 * self.v[k] + (1 - b2) * g * g
            mh = self.m[k] / (1 - b1 ** self.t)
            vh = self.v[k] / (1 - b2 ** self.t)
            p_ -= lr * mh / (np.sqrt(vh) + eps)

    def copy_params(self):
        return [w.copy() for w in self.W], [b.copy() for b in self.b]

    def set_params(self, params):
        self.W = [w.copy() for w in params[0]]
        self.b = [b.copy() for b in params[1]]


def standardise(Xtr, *others):
    mu, sd = Xtr.mean(axis=0), Xtr.std(axis=0)
    return [(Xtr - mu) / sd] + [(o - mu) / sd for o in others], (mu, sd)


def panel_tag(ax, s, x=-0.02, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, weight="bold", ha="right", va="bottom", color=INK)



def foot(fig, text, y=0.01, width=135):
    """Grey footnote at the bottom right, wrapped so that it never extends beyond the figure width."""
    import textwrap
    fig.text(0.99, y, "\n".join(textwrap.wrap(text, width)), ha="right", va="bottom", fontsize=FOOT, color=GREY,
             multialignment="right", linespacing=1.25)


CLEAR_C, CLOUD_C = "#C98B2B", "#2F6DB0"


# ==============================================================================================
def gdpaths():
    """Gradient descent and SGD on the least-squares loss of a two-coefficient linear model."""
    rng = np.random.default_rng(4)
    n = 200
    r = 0.9                                                   # correlation of the two predictors
    Z = rng.multivariate_normal([0, 0], [[1, r], [r, 1]], size=n)
    Z = (Z - Z.mean(0)) / Z.std(0)
    w_true = np.array([1.0, 0.5])
    y = Z @ w_true + rng.normal(0, 0.3, n)
    y = y - y.mean()
    H = Z.T @ Z / n
    w_star = np.linalg.solve(H, Z.T @ y / n)

    def L(w):
        res = Z @ w - y
        return 0.5 * np.mean(res ** 2)

    Lstar = L(w_star)
    lam, ev = np.linalg.eigh(H)                                 # columns of ev: slow, fast directions
    print("gdpaths: Hessian eigenvalues", lam, "condition", lam[1] / lam[0], "max stable lr", 2 / lam[1],
          "optimal lr", 2 / (lam[0] + lam[1]))
    w0 = w_star - 2.3 * ev[:, 0] * np.sign(ev[0, 0]) - 0.45 * ev[:, 1] * np.sign(ev[0, 1])
    print("  start", w0, "minimum", w_star, "L* =", Lstar)
    runs = [(0.1, "η = 0.1: crawls", SKY, 0), (0.6, "η = 0.6: steady", GREEN, 0),
            (1.0, "η = 1.0: zig-zags, fastest", ORANGE, 1), (1.08, "η = 1.08: diverges", RED, 1)]
    iters = 60
    fig = plt.figure(figsize=(7.0, 2.75))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.15], wspace=0.28)
    axs = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
    bx = fig.add_subplot(gs[2])
    g1, g2 = np.meshgrid(np.linspace(-2.0, 3.0, 300), np.linspace(-1.6, 3.2, 300))
    W = np.stack([g1.ravel(), g2.ravel()], 1)
    res = W @ Z.T - y[None, :]
    LL = 0.5 * np.mean(res ** 2, axis=1).reshape(g1.shape)
    lev = Lstar + np.array([0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1.1, 1.6, 2.2])
    for k, ax in enumerate(axs):
        ax.contour(g1, g2, LL, levels=lev, colors="#9DB3C8", linewidths=0.6)
        ax.plot(*w_star, marker="*", color=INK, ms=8, zorder=6)
        ax.plot(*w0, "s", color=INK, ms=3.8, zorder=6)
        ax.text(w0[0] - 0.1, w0[1] + 0.2, "start", fontsize=6.6, ha="right")
        ax.text(w_star[0] + 0.25, w_star[1] - 0.45, "minimum", fontsize=6.6)
        ax.set_xlim(-2.0, 3.0)
        ax.set_ylim(-1.6, 3.2)
        ax.set_aspect("equal")
        ax.set_xlabel("Coefficient $w_1$")
        ax.grid(False)
    axs[0].set_ylabel("Coefficient $w_2$")
    axs[0].set_title("Small steps and SGD", fontsize=8.6)
    axs[1].set_title("Large steps", fontsize=8.6)
    for lr, lab, col, k in runs:
        w = w0.copy()
        path = [w.copy()]
        losses = [L(w) - Lstar]
        for _ in range(iters):
            g = Z.T @ (Z @ w - y) / n
            w = w - lr * g
            path.append(w.copy())
            losses.append(L(w) - Lstar)
        path = np.array(path)
        show = path[:9] if lr > 1.0 else path[:40]
        axs[k].plot(show[:, 0], show[:, 1], "-o", color=col, ms=1.8, lw=0.9, zorder=4)
        tag_xy = {0.1: (-1.9, -0.45), 0.6: (-1.9, -0.95), 1.0: (1.25, 1.6), 1.08: (0.55, 2.65)}[lr]
        axs[k].annotate(f"η = {lr:g}", show[-1] if lr != 1.08 else show[5], xytext=tag_xy, fontsize=6.4, color=col,
                        weight="bold", arrowprops=dict(arrowstyle="-", color=col, lw=0.5))
        bx.semilogy(np.arange(iters + 1), np.maximum(losses, 1e-12), color=col, lw=1.4, label=lab)
        print(f"  lr={lr}: excess loss after 10 it {losses[10]:.3g}, after 60 it {losses[-1]:.3g}")
    # stochastic gradient descent, mini-batches of 10, eta = 0.3
    w = w0.copy()
    path = [w.copy()]
    sl = [L(w) - Lstar]
    rng2 = np.random.default_rng(11)
    for it in range(iters):
        idx = rng2.choice(n, 10, replace=False)
        g = Z[idx].T @ (Z[idx] @ w - y[idx]) / 10
        w = w - 0.3 * g
        path.append(w.copy())
        sl.append(L(w) - Lstar)
    path = np.array(path)
    axs[0].plot(path[:, 0], path[:, 1], "-", color=VIOLET, lw=0.8, zorder=3)
    axs[0].annotate("SGD", path[-1], xytext=(1.6, 1.6), fontsize=6.4, color=VIOLET, weight="bold",
                    arrowprops=dict(arrowstyle="-", color=VIOLET, lw=0.5))
    bx.semilogy(np.arange(iters + 1), sl, color=VIOLET, lw=1.0, label="SGD, batches of 10, η = 0.3")
    print(f"  SGD excess loss after 60 it {sl[-1]:.3g}")
    bx.set_xlabel("Iteration")
    bx.set_ylabel("Loss above minimum")
    bx.set_ylim(1e-9, 1e3)
    bx.set_title("Convergence", fontsize=8.6)
    bx.legend(fontsize=6.2, loc="lower left", handlelength=1.3, borderaxespad=0.2)
    panel_tag(axs[0], "a")
    panel_tag(axs[1], "b")
    panel_tag(bx, "c")
    foot(fig, "Least squares on 200 synthetic samples, predictor correlation 0.9. Hessian eigenvalues 0.083 and 1.92: stable only for η < 1.04.", y=0.01)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.235)
    save(fig, "ch43_gdpaths")


# ==============================================================================================
def _train_mlp(Xtr, ytr, Xva, yva, sizes, epochs, lr, seed, l2=0.0, record=True):
    net = NumpyMLP(sizes, seed=seed)
    tr, va = [], []
    best = (np.inf, 0, net.copy_params())
    for ep in range(epochs):
        net.step(Xtr, ytr, lr=lr, l2=l2)
        if record:
            lt, lv = net.loss(Xtr, ytr), net.loss(Xva, yva)
            tr.append(lt)
            va.append(lv)
            if lv < best[0]:
                best = (lv, ep + 1, net.copy_params())
    return net, np.array(tr), np.array(va), best


def mlpoverfit():
    """Numpy MLP on a small, noisily labelled training set: overfitting and early stopping."""
    Xtr, ytr = cloud_data(100, seed=1)
    Xva, yva = cloud_data(2000, seed=2)
    Xte, yte, yte_true, _ = cloud_data(20000, seed=3, return_comp=True)
    (Ztr, Zva, Zte), (mu, sd) = standardise(Xtr, Xva, Xte)
    epochs = 3000
    net, tr, va, best = _train_mlp(Ztr, ytr, Zva, yva, [2, 64, 64, 1], epochs, 0.01, seed=5)
    final = net.copy_params()
    acc_final = np.mean((net.proba(Zte) > 0.5) == yte)
    net.set_params(best[2])
    acc_best = np.mean((net.proba(Zte) > 0.5) == yte)
    print(f"mlpoverfit: best val loss {best[0]:.3f} at epoch {best[1]}; final train {tr[-1]:.3f} val {va[-1]:.3f}")
    print(f"  test accuracy early-stopped {acc_best:.3f}, final {acc_final:.3f}; train acc final ",
          np.mean((NumpyMLP_from(final, Ztr) > 0.5) == ytr))
    be, bclean = bayes_error()
    print(f"  Bayes error {be:.3f} (clean {bclean:.3f}) -> best possible accuracy {1 - be:.3f}")

    fig = plt.figure(figsize=(7.0, 2.75))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 1, 1], wspace=0.32)
    ax = fig.add_subplot(gs[0])
    ep = np.arange(1, epochs + 1)
    ax.semilogx(ep, tr, color=BLUE, lw=1.4, label="Training loss")
    ax.semilogx(ep, va, color=ORANGE, lw=1.4, label="Validation loss")
    ax.axvline(best[1], color=GREY, lw=0.8, ls="--")
    ax.plot(best[1], best[0], "o", color=ORANGE, ms=4)
    ax.text(best[1] * 0.85, 0.03, f"early stop\n(epoch {best[1]})", fontsize=6.6, color=INK, va="bottom", ha="right")
    ax.text(epochs * 0.95, 0.97, f"validation loss\nreaches {va[-1]:.1f}", fontsize=6.6, color=ORANGE, ha="right",
            va="top")
    ax.set_xlabel("Epoch (full passes over the data)")
    ax.set_ylabel("Cross-entropy loss")
    ax.set_ylim(0, 1.0)
    ax.set_xlim(1, epochs)
    ax.text(70, 0.66, "validation", fontsize=7, color=ORANGE, weight="bold", ha="center")
    ax.text(8, 0.32, "training", fontsize=7, color=BLUE, weight="bold", ha="center")
    ax.set_title("Loss curves", fontsize=9)
    panel_tag(ax, "a")

    gx, gy = np.meshgrid(np.linspace(0, 1.05, 260), np.linspace(0, 0.75, 220))
    G = (np.stack([gx.ravel(), gy.ravel()], 1) - mu) / sd
    for j, (params, title, acc) in enumerate([(best[2], f"Early-stopped: {acc_best * 100:.1f} %", acc_best),
                                              (final, f"After 3 000 epochs: {acc_final * 100:.1f} %",
                                               acc_final)]):
        bx = fig.add_subplot(gs[j + 1])
        net.set_params(params)
        P = net.proba(G).reshape(gx.shape)
        bx.contourf(gx, gy, P, levels=[0, 0.5, 1], colors=["#F6E7CF", "#D6E6F5"], alpha=1.0)
        bx.contour(gx, gy, P, levels=[0.5], colors=INK, linewidths=0.8)
        bx.scatter(Xtr[ytr == 0, 0], Xtr[ytr == 0, 1], s=7, color=CLEAR_C, edgecolor="white", lw=0.3,
                   label="labelled clear")
        bx.scatter(Xtr[ytr == 1, 0], Xtr[ytr == 1, 1], s=7, color=CLOUD_C, edgecolor="white", lw=0.3,
                   label="labelled cloud")
        bx.set_xlim(0, 1.05)
        bx.set_ylim(0, 0.75)
        bx.set_xlabel("Visible reflectance (0.65 µm)")
        if j == 0:
            bx.set_ylabel("SWIR reflectance (1.6 µm)")
        bx.set_title(title, fontsize=8.2)
        bx.grid(False)
        panel_tag(bx, "bc"[j])
        if j == 0:
            bx.legend(loc="upper left", fontsize=6.2, handletextpad=0.2, borderaxespad=0.2, markerscale=1.3)
    foot(fig, "Numpy network 2–64–64–1 (ReLU, Adam, step 0.01) trained on 100 synthetic pixels with 10 % wrong labels; test set 20 000 pixels.", y=0.01)
    fig.subplots_adjust(left=0.075, right=0.99, top=0.9, bottom=0.25)
    save(fig, "ch43_mlpoverfit")


def NumpyMLP_from(params, X):
    net = NumpyMLP([2, 64, 64, 1])
    net.set_params(params)
    return net.proba(X)


# ==============================================================================================
def boundaries():
    """Logistic regression, random forest and numpy MLP on the same cloud/clear data."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    Xtr, ytr = cloud_data(2000, seed=11)
    Xva, yva = cloud_data(1000, seed=12)
    Xte, yte, yte_true, comp = cloud_data(20000, seed=13, return_comp=True)
    (Ztr, Zva, Zte), (mu, sd) = standardise(Xtr, Xva, Xte)
    lr = LogisticRegression().fit(Ztr, ytr)
    rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0, n_jobs=-1).fit(Ztr, ytr)
    net, tr, va, best = _train_mlp(Ztr, ytr, Zva, yva, [2, 32, 32, 1], 1500, 0.01, seed=7)
    net.set_params(best[2])
    print("boundaries: MLP early stop epoch", best[1])
    models = [("Logistic regression", lambda Z: lr.predict_proba(Z)[:, 1]),
              ("Random forest (300 trees)", lambda Z: rf.predict_proba(Z)[:, 1]),
              ("Neural network (numpy MLP)", net.proba)]
    be, bclean = bayes_error()
    snow = comp == 3
    gx, gy = np.meshgrid(np.linspace(0, 1.05, 300), np.linspace(0, 0.75, 240))
    G = (np.stack([gx.ravel(), gy.ravel()], 1) - mu) / sd
    pb = bayes_posterior(np.stack([gx.ravel(), gy.ravel()], 1)).reshape(gx.shape)
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.65), sharey=True)
    rng = np.random.default_rng(0)
    show = rng.choice(len(Xtr), 700, replace=False)
    for ax, (name, f) in zip(axs, models):
        p_te = f(Zte)
        acc = np.mean((p_te > 0.5) == yte)
        acc_true = np.mean((p_te > 0.5) == yte_true)
        snow_fa = np.mean(p_te[snow] > 0.5)
        print(f"  {name}: test acc (noisy labels) {acc:.3f}, vs true labels {acc_true:.3f}, snow flagged as cloud {snow_fa:.3f}")
        P = f(G).reshape(gx.shape)
        ax.contourf(gx, gy, P, levels=[0, 0.5, 1], colors=["#F6E7CF", "#D6E6F5"])
        ax.contour(gx, gy, P, levels=[0.5], colors=INK, linewidths=0.9)
        ax.contour(gx, gy, pb, levels=[0.5], colors=RED, linewidths=0.8, linestyles="--")
        s0 = show[ytr[show] == 0]
        s1 = show[ytr[show] == 1]
        ax.scatter(Xtr[s0, 0], Xtr[s0, 1], s=3, color=CLEAR_C, lw=0, alpha=0.8)
        ax.scatter(Xtr[s1, 0], Xtr[s1, 1], s=3, color=CLOUD_C, lw=0, alpha=0.8)
        ax.set_title(f"{name}\ntest accuracy {acc * 100:.1f} %", fontsize=8.0)
        ax.set_xlim(0, 1.05)
        ax.set_ylim(0, 0.75)
        ax.set_xlabel("Visible reflectance (0.65 µm)")
        ax.grid(False)
    axs[0].set_ylabel("SWIR reflectance (1.6 µm)")
    for txt, xy in [("water", (0.06, 0.04)), ("vegetation", (0.09, 0.2)), ("soil", (0.22, 0.43)),
                    ("snow", (0.83, 0.05)), ("thick cloud", (0.80, 0.63))]:
        axs[0].text(*xy, txt, fontsize=6.3, color=INK, ha="center",
                    bbox=dict(fc="white", ec="none", alpha=0.7, pad=0.6))
    handles = [Line2D([], [], color=INK, lw=0.9, label="model boundary (p = 0.5)"),
               Line2D([], [], color=RED, lw=0.8, ls="--", label="ideal (Bayes) boundary"),
               Line2D([], [], marker="o", ls="", color=CLEAR_C, ms=3, label="clear"),
               Line2D([], [], marker="o", ls="", color=CLOUD_C, ms=3, label="cloud")]
    fig.legend(handles=handles, loc="lower left", ncol=4, fontsize=6.6, bbox_to_anchor=(0.06, 0.0),
               handlelength=1.6, columnspacing=1.2)
    foot(fig, f"2 000 training pixels from eight surface and cloud types, 10 % of labels wrong; test 20 000 pixels; best possible {100 * (1 - be):.1f} %.", y=0.075)
    fig.subplots_adjust(left=0.075, right=0.99, top=0.85, bottom=0.30, wspace=0.08)
    save(fig, "ch43_boundaries")


# ==============================================================================================
def fire_data(n, seed, prev=0.01):
    """Synthetic rare-event task: 'fire' pixels (prevalence 1 %) against background and fire-like confusers."""
    rng = np.random.default_rng(seed)
    y = (rng.random(n) < prev).astype(int)
    X = np.zeros((n, 2))
    neg = np.where(y == 0)[0]
    pos = np.where(y == 1)[0]
    conf = rng.random(len(neg)) < 0.05                     # 5 % of clear pixels are hot or glinting
    X[neg[~conf]] = rng.normal([0, 0], [1, 1], size=((~conf).sum(), 2))
    X[neg[conf]] = rng.normal([2.5, 0.8], [1.0, 1.0], size=(conf.sum(), 2))
    X[pos] = rng.normal([2.8, 2.3], [1.2, 1.2], size=(len(pos), 2))
    return X, y


def rocpr():
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score, average_precision_score
    Xtr, ytr = fire_data(200000, 1)
    Xte, yte = fire_data(200000, 2)
    m = LogisticRegression().fit(Xtr, ytr)
    p = m.predict_proba(Xte)[:, 1]
    auc = roc_auc_score(yte, p)
    ap = average_precision_score(yte, p)
    print(f"rocpr: test positives {yte.sum()} of {len(yte)}; ROC AUC {auc:.3f}; average precision {ap:.3f}")
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.6))
    ax, bx, cx = axs
    fpr, tpr, thr = roc_curve(yte, p)
    ax.semilogx(np.maximum(fpr, 1e-5), tpr, color=BLUE, lw=1.5, label=f"classifier (AUC {auc:.3f})")
    ff = np.logspace(-5, 0, 50)
    ax.semilogx(ff, ff, color=GREY, lw=0.8, ls="--", label="random guess")
    # operating point at threshold 0.5
    pr = p > 0.5
    tp = np.sum(pr & (yte == 1)); fp = np.sum(pr & (yte == 0)); fn = np.sum(~pr & (yte == 1)); tn = np.sum(~pr & (yte == 0))
    rec5, fpr5, prec5, acc5 = tp / (tp + fn), fp / (fp + tn), tp / (tp + fp), (tp + tn) / len(yte)
    print(f"  threshold 0.5: recall {rec5:.3f}, false-alarm rate {fpr5:.4f}, precision {prec5:.3f}, accuracy {acc5:.4f};"
          f" all-clear accuracy {1 - yte.mean():.4f}; TP {tp} FP {fp} FN {fn}")
    ax.plot(fpr5, rec5, "o", color=ORANGE, ms=4.5, zorder=5)
    ax.annotate(f"threshold 0.5:\nrecall {rec5 * 100:.0f} %,\nfalse alarms {fpr5 * 100:.2f} %", (fpr5, rec5),
                xytext=(2e-2, 0.12), fontsize=6.3, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))
    ax.set_xlabel("False-alarm rate (log scale)")
    ax.set_ylabel("Recall (true-positive rate)")
    ax.set_title("ROC curve", fontsize=8.6)
    ax.legend(loc="upper left", fontsize=6.0)
    ax.set_xlim(1e-4, 1); ax.set_ylim(0, 1.0)
    # precision-recall at three prevalences (negatives subsampled from the same test set)
    rng = np.random.default_rng(5)
    posi = np.where(yte == 1)[0]
    negi = np.where(yte == 0)[0]
    for prev, col in [(0.5, GREEN), (0.1, VIOLET), (0.01, BLUE)]:
        nneg = int(round(len(posi) * (1 - prev) / prev))
        sel = np.concatenate([posi, rng.choice(negi, min(nneg, len(negi)), replace=False)])
        pr_, rc_, _ = precision_recall_curve(yte[sel], p[sel])
        a = average_precision_score(yte[sel], p[sel])
        a2 = roc_auc_score(yte[sel], p[sel])
        print(f"  prevalence {prev}: AP {a:.3f}, ROC AUC {a2:.3f}")
        bx.plot(rc_, pr_, color=col, lw=1.4, label=f"prevalence {prev * 100:g} % (AP {a:.2f})")
    bx.axhline(0.01, color=BLUE, lw=0.7, ls=":")
    bx.text(0.02, 0.035, "no-skill level at 1 %", fontsize=6.0, color=BLUE)
    bx.plot(rec5, prec5, "o", color=ORANGE, ms=4.5, zorder=5)
    bx.set_xlabel("Recall")
    bx.set_ylabel("Precision")
    bx.set_title("Precision–recall curves", fontsize=8.6)
    bx.set_xlim(0, 1); bx.set_ylim(0, 1.02)
    bx.legend(loc="lower left", fontsize=5.9, bbox_to_anchor=(0.0, 0.08), handlelength=1.2)
    # metrics versus threshold at 1 % prevalence
    ts = np.linspace(0.05, 0.95, 91)
    A, P, R, F = [], [], [], []
    for t in ts:
        pr = p > t
        tp = np.sum(pr & (yte == 1)); fp = np.sum(pr & (yte == 0)); fn = np.sum(~pr & (yte == 1))
        A.append(np.mean(pr == yte)); R.append(tp / (tp + fn)); P.append(tp / max(tp + fp, 1))
        F.append(2 * P[-1] * R[-1] / max(P[-1] + R[-1], 1e-9))
    F = np.array(F)
    cx.plot(ts, A, color=INK, lw=1.4)
    cx.plot(ts, P, color=GREEN, lw=1.2)
    cx.plot(ts, R, color=ORANGE, lw=1.2)
    cx.plot(ts, F, color=VIOLET, lw=1.2, ls="--")
    cx.text(0.1, 0.94, f"accuracy ≥ {100 * min(A):.1f} % everywhere;\n'never fire' scores "
            f"{100 * (1 - yte.mean()):.1f} %", fontsize=6.1, color=INK, ha="left", va="top")
    print(f"  min accuracy over thresholds 0.05-0.95: {min(A):.4f}")
    cx.text(0.66, 0.60, "precision", fontsize=6.5, color=GREEN, weight="bold")
    cx.text(0.62, 0.15, "recall", fontsize=6.5, color=ORANGE, weight="bold")
    cx.text(0.42, 0.555, "F1", fontsize=6.5, color=VIOLET, weight="bold")
    kb = int(np.argmax(F))
    print(f"  best F1 {F[kb]:.3f} at threshold {ts[kb]:.2f} (precision {P[kb]:.3f}, recall {R[kb]:.3f}, accuracy {A[kb]:.4f})")
    cx.plot(ts[kb], F[kb], "o", color=VIOLET, ms=4)
    cx.set_xlabel("Decision threshold on p(fire)")
    cx.set_ylabel("Score")
    cx.set_ylim(0, 1.02)
    cx.set_title("Scores versus threshold", fontsize=8.6)
    cx.annotate(f"best F1 = {F[kb]:.2f}", (ts[kb], F[kb]), xytext=(0.30, 0.30), fontsize=6.3, color=VIOLET,
                arrowprops=dict(arrowstyle="-", color=VIOLET, lw=0.5))
    for a_, t_ in zip(axs, "abc"):
        panel_tag(a_, t_)
    foot(fig, "Logistic regression on two synthetic thermal features; 200 000 test pixels: 1 % fires, 5 % of clear pixels fire-like.", y=0.01)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.25, wspace=0.32)
    save(fig, "ch43_rocpr")


# ==============================================================================================
def learning():
    """(a) bias-variance: tree depth; (b) learning curves: test error versus training-set size."""
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import cross_val_score
    be, _ = bayes_error()
    X, y = cloud_data(1000, seed=21)
    Xte, yte = cloud_data(20000, seed=22)
    depths = np.arange(1, 21)
    tr_err, cv_err, te_err = [], [], []
    for d in depths:
        t = DecisionTreeClassifier(max_depth=d, random_state=0).fit(X, y)
        tr_err.append(1 - t.score(X, y))
        cv_err.append(1 - cross_val_score(DecisionTreeClassifier(max_depth=d, random_state=0), X, y, cv=5).mean())
        te_err.append(1 - t.score(Xte, yte))
    kbest = int(np.argmin(cv_err))
    print(f"learning: tree depth with lowest CV error {depths[kbest]} (CV {cv_err[kbest]:.3f}, test {te_err[kbest]:.3f});"
          f" depth 20 train {tr_err[-1]:.3f} test {te_err[-1]:.3f}; Bayes {be:.3f}")
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 2.75), gridspec_kw=dict(width_ratios=[1, 1.25]))
    ax.plot(depths, 100 * np.array(tr_err), "-o", color=BLUE, ms=2.5, lw=1.3, label="training error")
    ax.plot(depths, 100 * np.array(cv_err), "-o", color=ORANGE, ms=2.5, lw=1.3, label="validation error (5-fold CV)")
    ax.axhline(100 * be, color=RED, lw=0.8, ls="--")
    ax.text(20, 100 * be + 0.6, "irreducible error", fontsize=6.4, color=RED, ha="right", va="bottom")
    ax.axvline(depths[kbest], color=GREY, lw=0.7, ls=":")
    ax.text(depths[kbest] + 0.4, 34, "best depth", fontsize=6.4, color=GREY)
    ax.text(1.6, 3.5, "underfitting\n(high bias)", fontsize=6.4, color=INK)
    ax.text(19.5, 3.5, "overfitting\n(high variance)", fontsize=6.4, color=INK, ha="right")
    ax.set_xlabel("Model complexity: decision-tree depth")
    ax.set_ylabel("Error (%)")
    ax.set_ylim(0, 40)
    ax.set_xlim(0.5, 20.5)
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.legend(loc="upper right", fontsize=6.4, bbox_to_anchor=(1.0, 0.86))
    ax.set_title("Bias–variance trade-off (1 000 pixels)", fontsize=8.6)
    sizes = np.array([30, 60, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    models = [("Logistic regression", lambda: LogisticRegression(), GREY),
              ("k-nearest neighbours (k = 15)", lambda: KNeighborsClassifier(15), GREEN),
              ("Random forest (100 trees)", lambda: RandomForestClassifier(100, min_samples_leaf=3, random_state=0,
                                                                         n_jobs=-1), BLUE)]
    for name, mk, col in models:
        mean, sd_, trm = [], [], []
        for nsz in sizes:
            errs, trs = [], []
            for rep in range(5):
                Xs, ys = cloud_data(int(nsz), seed=1000 + 37 * rep + int(nsz))
                if len(np.unique(ys)) < 2:
                    continue
                k = mk()
                if isinstance(k, KNeighborsClassifier) and nsz < 30:
                    continue
                k.fit(Xs, ys)
                errs.append(1 - k.score(Xte, yte))
                trs.append(1 - k.score(Xs, ys))
            mean.append(np.mean(errs)); sd_.append(np.std(errs)); trm.append(np.mean(trs))
        mean, sd_ = 100 * np.array(mean), 100 * np.array(sd_)
        bx.fill_between(sizes, mean - sd_, mean + sd_, color=col, alpha=0.15, lw=0)
        bx.semilogx(sizes, mean, "-o", color=col, ms=2.5, lw=1.4, label=name)
        if "forest" in name:
            bx.semilogx(sizes, 100 * np.array(trm), "--", color=col, lw=0.9, label="random forest, training error")
        print(f"  {name}: test error " + ", ".join(f"{n}:{m:.1f}%" for n, m in zip(sizes, mean)))
    bx.axhline(100 * be, color=RED, lw=0.8, ls="--")
    bx.text(32, 2.0, f"red dashed line: irreducible error {100 * be:.1f} % (10 % label noise + class overlap)",
            fontsize=6.2, color=RED, va="bottom")
    bx.set_xlabel("Number of training pixels")
    bx.set_ylabel("Test error (%)")
    bx.set_ylim(0, 40)
    bx.set_xlim(25, 25000)
    bx.legend(loc="center right", fontsize=6.2, bbox_to_anchor=(1.0, 0.52))
    bx.set_title("Learning curves (test set of 20 000 pixels)", fontsize=8.6)
    panel_tag(ax, "a")
    panel_tag(bx, "b")
    foot(fig, "Synthetic cloud/clear pixels, 10 % label noise; error measured against noisy labels; shading ±1σ over five training sets.", y=0.01)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.21, wspace=0.25)
    save(fig, "ch43_learning")


# ==============================================================================================
BANDS = ["Blue\n0.48", "Green\n0.56", "Red\n0.66", "NIR\n0.86", "SWIR1\n1.6", "SWIR2\n2.2"]
ENDMEMBERS = [  # approximate surface reflectance in six Landsat-like bands
    ("Water", [0.07, 0.06, 0.04, 0.02, 0.01, 0.005], NAVY),
    ("Forest", [0.03, 0.06, 0.03, 0.35, 0.15, 0.06], GREEN),
    ("Cropland", [0.05, 0.10, 0.07, 0.50, 0.27, 0.13], "#8DB33A"),
    ("Bare soil", [0.12, 0.17, 0.22, 0.28, 0.36, 0.30], ORANGE),
    ("Urban", [0.13, 0.14, 0.15, 0.19, 0.22, 0.20], GREY),
    ("Burn scar", [0.04, 0.05, 0.06, 0.10, 0.18, 0.17], RED),
]


def kmeanspca():
    from sklearn.cluster import KMeans
    from sklearn.metrics import adjusted_rand_score
    rng = np.random.default_rng(31)
    n = 3000
    E = np.array([e[1] for e in ENDMEMBERS])
    dom = rng.choice(len(E), n, p=[0.12, 0.22, 0.22, 0.16, 0.14, 0.14])
    alpha = np.full((n, len(E)), 0.25)
    alpha[np.arange(n), dom] = 8.0
    A = np.array([rng.dirichlet(a) for a in alpha])          # abundances: one dominant cover per pixel
    illum = rng.uniform(0.85, 1.15, n)[:, None]             # topographic shading
    X = illum * (A @ E) + rng.normal(0, 0.008, (n, 6))
    Xc = X - X.mean(0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    ev = S ** 2 / np.sum(S ** 2)
    pcs = Xc @ Vt.T
    km = KMeans(6, n_init=10, random_state=0).fit(X)
    ari = adjusted_rand_score(dom, km.labels_)
    inertia = [KMeans(k, n_init=10, random_state=0).fit(X).inertia_ for k in range(1, 11)]
    print("kmeanspca: explained variance", np.round(ev * 100, 2), "cum2", round(100 * ev[:2].sum(), 1),
          "cum3", round(100 * ev[:3].sum(), 1), "ARI", round(ari, 3))
    # match clusters to dominant classes for colouring and purity
    lab_of = {}
    for c in range(6):
        vals, cnt = np.unique(dom[km.labels_ == c], return_counts=True)
        lab_of[c] = vals[np.argmax(cnt)]
        print(f"  cluster {c}: size {np.sum(km.labels_ == c)}, majority {ENDMEMBERS[lab_of[c]][0]} "
              f"({cnt.max() / cnt.sum() * 100:.0f} %)")
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.6), gridspec_kw=dict(width_ratios=[1.05, 1.15, 0.9]))
    ax, bx, cx = axs
    xb = np.arange(6)
    for name, spec, col in ENDMEMBERS:
        ax.plot(xb, spec, "-o", color=col, ms=2.5, lw=1.3, label=name)
    ax.set_xticks(xb)
    ax.set_xticklabels(BANDS, fontsize=6.2)
    ax.set_ylabel("Reflectance")
    ax.set_title("Pure spectra", fontsize=8.4)
    ax.legend(fontsize=5.9, loc="upper left", ncol=2, columnspacing=0.6, handlelength=1.2)
    ax.set_ylim(0, 0.75)
    ax.set_xlabel("Band (centre wavelength, µm)", fontsize=7)
    for c in range(6):
        sel = km.labels_ == c
        col = ENDMEMBERS[lab_of[c]][2]
        bx.scatter(pcs[sel, 0], pcs[sel, 1], s=2.5, color=col, lw=0, alpha=0.7)
    cen = (km.cluster_centers_ - X.mean(0)) @ Vt.T
    bx.scatter(cen[:, 0], cen[:, 1], marker="X", s=40, color="white", edgecolor=INK, lw=0.8, zorder=5)
    for c in range(6):
        nm = ENDMEMBERS[lab_of[c]][0]
        bx.annotate(nm, (cen[c, 0], cen[c, 1]), xytext=(4, 4), textcoords="offset points", fontsize=6.0,
                    bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.5))
    bx.set_xlabel(f"PC 1 ({ev[0] * 100:.0f} % of variance)")
    bx.set_ylabel(f"PC 2 ({ev[1] * 100:.0f} %)")
    bx.set_title(f"k-means clusters in PCA space", fontsize=8.4)
    cx.bar(np.arange(1, 7), ev * 100, color=BLUE, width=0.6, label="each component")
    cx.plot(np.arange(1, 7), np.cumsum(ev) * 100, "-o", color=ORANGE, ms=3, lw=1.2, label="cumulative")
    cx.set_xlabel("Principal component")
    cx.set_ylabel("Variance explained (%)")
    cx.set_ylim(0, 105)
    cx.set_xticks(np.arange(1, 7))
    cx.legend(fontsize=6.0, loc="center right")
    cx.set_title("Scree plot", fontsize=8.4)
    for a_, t_ in zip(axs, "abc"):
        panel_tag(a_, t_)
    foot(fig, f"3 000 synthetic six-band pixels (shaded mixtures dominated by one cover, plus noise); k-means with k = 6: adjusted Rand index {ari:.2f}.", y=0.01)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.27, wspace=0.34)
    save(fig, "ch43_kmeanspca")
    return inertia


# ==============================================================================================
def grf(shape, corr_len_px, rng):
    """Gaussian random field with Gaussian covariance (correlation length in pixels), unit variance."""
    ny, nx = shape
    ky = np.fft.fftfreq(ny)[:, None]
    kx = np.fft.rfftfreq(nx)[None, :]
    k2 = kx ** 2 + ky ** 2
    spec = np.exp(-0.5 * (2 * np.pi) ** 2 * k2 * corr_len_px ** 2 / 2)
    f = np.fft.irfft2(np.fft.rfft2(rng.normal(size=shape)) * np.sqrt(spec), s=shape)
    return (f - f.mean()) / f.std()


def spatialcv():
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import KFold, GroupKFold
    from sklearn.metrics import r2_score
    rng = np.random.default_rng(41)
    dx = 0.5                                   # km per grid cell
    ny, nx = 200, 400                          # 100 km x 200 km domain
    S = grf((ny, nx), 12 / dx, rng)            # spatial signal NOT explained by the predictors
    X1 = grf((ny, nx), 6 / dx, rng)            # one genuinely informative predictor
    others = [grf((ny, nx), 20 / dx, rng) for _ in range(5)]   # smooth but irrelevant predictors
    target = 0.5 * X1 + 1.0 * S + 0.3 * rng.normal(size=(ny, nx))
    feats = np.stack([X1] + others, -1)
    ntr = 1500
    # training samples: western half (x < 100 km); 'new region' test samples: eastern half
    iy = rng.integers(0, ny, ntr); ix = rng.integers(0, nx // 2, ntr)
    jy = rng.integers(0, ny, ntr); jx = rng.integers(nx // 2, nx, ntr)
    Xtr, ytr = feats[iy, ix], target[iy, ix]
    Xnew, ynew = feats[jy, jx], target[jy, jx]
    xs_km, ys_km = ix * dx, iy * dx

    def cv_r2(groups=None):
        pred = np.zeros(ntr)
        if groups is None:
            splits = KFold(5, shuffle=True, random_state=0).split(Xtr)
        else:
            splits = GroupKFold(5).split(Xtr, ytr, groups)
        for a, b in splits:
            m = RandomForestRegressor(200, min_samples_leaf=2, random_state=0, n_jobs=-1).fit(Xtr[a], ytr[a])
            pred[b] = m.predict(Xtr[b])
        return r2_score(ytr, pred)

    r_random = cv_r2()
    blocks = [2.5, 5, 10, 20, 25, 33.4]
    r_block = []
    for B in blocks:
        g = (np.floor(xs_km / B) * 1000 + np.floor(ys_km / B)).astype(int)
        # shuffle block ids so that GroupKFold assigns blocks to folds pseudo-randomly
        u = np.unique(g)
        perm = dict(zip(u, rng.permutation(len(u))))
        r_block.append(cv_r2(np.array([perm[v] for v in g])))
    m = RandomForestRegressor(200, min_samples_leaf=2, random_state=0, n_jobs=-1).fit(Xtr, ytr)
    r_new = r2_score(ynew, m.predict(Xnew))
    # what fraction of variance is explainable by the predictors at all? (true function on the new region)
    r_oracle = r2_score(ynew, 0.5 * Xnew[:, 0])
    print(f"spatialcv: random 5-fold R2 {r_random:.2f}; block CV " +
          ", ".join(f"{b} km: {r:.2f}" for b, r in zip(blocks, r_block)) +
          f"; new region R2 {r_new:.2f}; oracle (true relation) {r_oracle:.2f}")
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw=dict(width_ratios=[1.7, 1]))
    ax.set_anchor("W")
    ax.imshow(target, origin="lower", extent=(0, nx * dx, 0, ny * dx), cmap="RdYlBu_r", vmin=-3, vmax=3)
    show = rng.choice(ntr, 600, replace=False)
    ax.scatter(xs_km[show], ys_km[show], s=1.3, color=INK, lw=0, alpha=0.9)
    ax.scatter(jx[show] * dx, jy[show] * dx, s=1.3, color="white", lw=0, alpha=0.9)
    for xg in np.arange(20, 100, 20):
        ax.plot([xg, xg], [0, 100], color="white", lw=0.6, alpha=0.9)
    for yg in np.arange(20, 100, 20):
        ax.plot([0, 100], [yg, yg], color="white", lw=0.6, alpha=0.9)
    ax.axvline(100, color=INK, lw=1.4)
    for xc, txt in [(50, "training region, 20 km blocks"), (150, "new region")]:
        ax.text(xc, 96, txt, ha="center", va="top", fontsize=6.6, bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.2))
    ax.set_xlabel("East (km)")
    ax.set_ylabel("North (km)")
    ax.grid(False)
    bx.axvspan(0, 12, color=LIGHT, zorder=0)
    bx.text(0.8, 1.08, "blocks smaller\nthan correlation\nlength (12 km)", fontsize=5.9, color=GREY, va="top")
    bx.axhline(0, color="#5B6670", lw=0.6)
    bx.axhline(r_random, color=ORANGE, lw=1.3, ls="--")
    bx.text(35.5, r_random + 0.02, f"random 5-fold CV: R² = {r_random:.2f}", color=ORANGE, fontsize=6.4, ha="right",
            va="bottom")
    bx.plot(blocks, r_block, "-o", color=BLUE, ms=3.5, lw=1.4)
    bx.text(21, r_block[3] + 0.08, "spatial-block CV", color=BLUE, fontsize=6.4)
    bx.axhline(r_oracle, color=GREEN, lw=1.0, ls=":")
    bx.text(35.5, r_oracle - 0.02, f"true relation only: {r_oracle:.2f}", color=GREEN, fontsize=6.2, ha="right",
            va="top")
    bx.axhline(r_new, color=RED, lw=1.3)
    bx.text(35.5, r_new + 0.02, f"actual skill in new region: {r_new:.2f}", color=RED, fontsize=6.4, ha="right",
            va="bottom")
    bx.set_xlim(0, 36)
    bx.set_ylim(-0.5, 1.1)
    bx.set_xlabel("Block size (km)")
    bx.set_ylabel("R² (cross-validated or tested)")
    bx.set_title("Estimated skill depends on the split", fontsize=8.6)
    ax.set_title("Synthetic, spatially autocorrelated target (red high, blue low)", fontsize=8.6)
    panel_tag(ax, "a")
    panel_tag(bx, "b")
    foot(fig, "Target = 0.5 × predictor 1 + spatial signal (correlation length 12 km) + noise; five other predictors are irrelevant smooth fields.", y=0.01)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.91, bottom=0.2, wspace=0.2)
    save(fig, "ch43_spatialcv")


# ==============================================================================================
# Timeline of AI in space, 1980-2026.  status: "op" operational, "demo" flight demonstration or pilot,
# "res" research or ground prototype.  Lanes: 2 symbolic, 1 classical ML, 0 deep learning / foundation models.
TL_A = [  # 1980-2011
    (1985.0, 2, "CLIPS rule engine\n(NASA JSC)", "op"),
    (1988.75, 2, "INCO expert system,\nShuttle Mission Control", "op"),
    (1990.3, 2, "SPIKE schedules\nHubble", "op"),
    (1999.4, 2, "Remote Agent flies\non Deep Space 1", "demo"),
    (2004.3, 2, "EO-1 onboard\nplanner (ASE)", "op"),
    (2005.1, 2, "MEXAR2 plans Mars\nExpress downlinks", "op"),
    (1985.5, 1, "Regression SST\nfrom AVHRR", "op"),
    (1989.5, 1, "k-NN national forest\ninventory (Finland)", "op"),
    (1993.5, 1, "SKICAT decision\ntrees (sky survey)", "res"),
    (2004.3, 1, "EO-1 onboard\nSVM classifiers", "op"),
    (2010.2, 1, "AEGIS picks rock\ntargets (Opportunity)", "op"),
    (2011.1, 1, "IASI: spectra\nas PCA scores", "op"),
]
TL_A_GEN = [(1986.0, "backpropagation\npopularised"), (1995.0, "support vector\nmachines"),
            (2001.0, "random\nforests"), (2006.0, "deep belief\nnetworks")]
TL_B = [  # 2012-2026
    (2013.9, 1, "Global forest-change maps\n(decision trees)", "op"),
    (2015.0, 1, "SVM solar-flare\nforecasts (SDO)", "res"),
    (2016.4, 1, "AEGIS on\nCuriosity", "op"),
    (2018.3, 1, "MODIS land cover\nby random forest", "op"),
    (2019.8, 1, "ESA collision-\navoidance challenge", "res"),
    (2017.8, 0, "LSTM telemetry\nmonitor (SMAP)", "demo"),
    (2018.1, 0, "CNN search of\nMars images (PDS)", "op"),
    (2020.7, 0, "Φsat-1 onboard\ncloud CNN", "demo"),
    (2021.5, 0, "OPS-SAT trains\nnetworks in orbit", "demo"),
    (2023.6, 0, "Prithvi EO\nfoundation model", "res"),
    (2025.15, 0, "AI weather model\noperational (ECMWF)", "op"),
    (2025.55, 0, "Dynamic targeting\n(CogniSAT-6)", "demo"),
    (2025.85, 0, "GPU, then TPU,\nprototypes in orbit", "demo"),
    (2025.93, 0, "Rover drive planned\nby generative AI", "demo"),
    (2026.23, 0, "Onboard object\ndetection (Pelican-4)", "demo"),
]
TL_B_GEN = [(2012.8, "deep CNN wins\nImageNet"), (2017.45, "transformer\narchitecture"),
            (2021.6, "'foundation\nmodels' named", "right"), (2022.9, "chat assistants\nreach the public", "left")]
LANE_STYLE = {2: ("Symbolic AI: rules, search,\nplanning, scheduling", NAVY),
              1: ("Classical machine learning", ORANGE),
              0: ("Deep learning and\nfoundation models", VIOLET)}


def _place_labels(ax, fig, items, lane_y, levels, color, fs=5.9):
    """Place two-line labels above/below a lane without overlaps (greedy, measured in display space).
    Centred labels are tried first at every level, then labels hanging to the left or right of the stem."""
    renderer = fig.canvas.get_renderer()
    axbb = ax.get_window_extent(renderer)
    for x, txt in sorted(items, key=lambda e: e[0]):
        done = False
        for ha in ("center", "right", "left"):
            for lv in levels:
                y = lane_y + lv
                dx = {"center": 0.0, "right": 0.12, "left": -0.12}[ha]
                t = ax.text(x + dx, y, txt, ha=ha, va="bottom" if lv > 0 else "top", fontsize=fs, color=INK,
                            linespacing=1.1, zorder=5, multialignment=ha if ha != "center" else "center")
                bb = t.get_window_extent(renderer).expanded(1.05, 1.1)
                inside = bb.x0 >= axbb.x0 - 2 and bb.x1 <= axbb.x1 + 2 and bb.y0 >= axbb.y0 and bb.y1 <= axbb.y1
                if inside and all(not bb.overlaps(o) for o in ax._placed):
                    ax._placed.append(bb)
                    ax.plot([x, x], [lane_y, y], color=color, lw=0.5, alpha=0.6, zorder=2)
                    done = True
                    break
                t.remove()
            if done:
                break
        if not done:
            print("  WARNING: could not place", txt.replace("\n", " "))


def timeline():
    from matplotlib.transforms import Bbox
    fig = plt.figure(figsize=(7.0, 6.3))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.22], hspace=0.12)
    panels = [(fig.add_subplot(gs[0]), TL_A, TL_A_GEN, (1975.2, 2012.7), 1982.6, [2, 1], "a",
               "1980–2011: rules, schedulers and the first learned classifiers", 3.5),
              (fig.add_subplot(gs[1]), TL_B, TL_B_GEN, (2008.25, 2026.95), 2011.6, [1, 0], "b",
               "2012–2026: deep learning reaches orbit", 4.4)]
    marker = {"op": dict(marker="o", mfc=None), "demo": dict(marker="D"), "res": dict(marker="o", mfc="white")}
    for ax, ev, gen, xl, xs, lanes, tag, title, spacing in panels:
        ax.set_xlim(*xl)
        lane_pos = {ln: 2.6 + spacing * k for k, ln in enumerate(sorted(lanes))}
        top = max(lane_pos.values()) + 2.9
        ax.set_ylim(-1.75, top)
        ax.axis("off")
        ax.set_title(title, fontsize=8.6, loc="left", pad=2)
        panel_tag(ax, tag, x=-0.005, y=1.0)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        ax._placed = [ax.title.get_window_extent(renderer).expanded(1.02, 1.2)]
        # general AI milestones band at the bottom
        ax.fill_between([xs, xl[1]], -1.25, 0.7, color="#F1F4F7", zorder=0, lw=0)
        ax.text(xl[0], -0.27, "AI in\ngeneral", fontsize=6.4, color=GREY, va="center", ha="left", style="italic",
                weight="bold", linespacing=1.05)
        for g in gen:
            x, txt = g[0], g[1]
            ha = g[2] if len(g) > 2 else "center"
            ax.plot([x], [0.25], marker="v", color=GREY, ms=4, zorder=4)
            ax.text(x + {"center": 0, "right": 0.25, "left": -0.25}[ha], 0.02, txt, ha=ha, va="top", fontsize=5.8,
                    color="#4A545E", linespacing=1.1, multialignment=ha if ha != "center" else "center")
        step = 5 if tag == "a" else 2
        for yr in range(int(np.ceil(xs / step) * step), int(xl[1]) + 1, step):
            ax.text(yr, -1.35, str(yr), ha="center", va="top", fontsize=6.2, color=GREY)
            ax.plot([yr, yr], [-1.25, top - 0.6], color="#E3E8EE", lw=0.5, zorder=0)
        for ln in lanes:
            yl = lane_pos[ln]
            name, col = LANE_STYLE[ln]
            ax.plot([xs, xl[1]], [yl, yl], color=col, lw=1.6, alpha=0.85, zorder=3)
            ax.text(xl[0], yl, name, fontsize=6.4, color=col, weight="bold", va="center", ha="left",
                    linespacing=1.05, zorder=6)
        fig.canvas.draw()
        for t in ax.texts:
            ax._placed.append(t.get_window_extent(renderer).expanded(1.03, 1.08))
        # label height in data units -> stacking levels that never overlap their neighbours
        probe = ax.text(xs, 0, "Ag\nAg", fontsize=5.9, linespacing=1.1)
        hb = probe.get_window_extent(renderer)
        probe.remove()
        h = abs(ax.transData.inverted().transform((0, hb.height))[1] - ax.transData.inverted().transform((0, 0))[1])
        levels = []
        for k in range(5):
            levels += [0.3 + k * (h + 0.12), -(0.3 + k * (h + 0.12))]
        for ln in lanes:                       # lane lines are obstacles too
            yl = lane_pos[ln]
            p0 = ax.transData.transform((xs, yl))
            p1 = ax.transData.transform((xl[1], yl))
            ax._placed.append(Bbox([[p0[0], p0[1] - 1.5], [p1[0], p1[1] + 1.5]]))
        for ln in lanes:
            yl = lane_pos[ln]
            col = LANE_STYLE[ln][1]
            items = [(x, txt) for x, l, txt, st in ev if l == ln]
            for x, l, txt, st in ev:
                if l == ln:
                    mk = marker[st]
                    ax.plot([x], [yl], marker=mk["marker"], ms=4.6 if mk["marker"] == "o" else 4.0, color=col,
                            mfc=mk.get("mfc") or col, mec=col, mew=1.0, zorder=6, ls="")
            _place_labels(ax, fig, items, yl, levels, col)
    ax = panels[0][0]
    ax.fill_between([1987.5, 1993.5], -1.25, 0.7, color="#E2E6EB", zorder=0.5, lw=0)
    ax.text(1990.5, -1.2, "second 'AI winter'", fontsize=5.6, color=GREY, ha="center", va="bottom", style="italic")
    hand = [Line2D([], [], marker="o", ls="", color=INK, ms=4.5, label="operational use"),
            Line2D([], [], marker="D", ls="", color=INK, ms=4, label="flight demonstration or pilot"),
            Line2D([], [], marker="o", ls="", color=INK, mfc="white", ms=4.5, label="research or prototype")]
    tb = panels[1][0].get_position()
    fig.legend(handles=hand, loc="lower right", ncol=3, fontsize=6.6, bbox_to_anchor=(0.995, tb.y1 - 0.004),
               handletextpad=0.3, columnspacing=1.0, borderaxespad=0.0)
    foot(fig, "Selected milestones, dated by first use. Sources: NASA, ESA, JPL, STScI, ECMWF and company releases.",
         y=0.008)
    fig.subplots_adjust(left=0.01, right=0.995, top=0.965, bottom=0.045)
    save(fig, "ch43_timeline")


# ==============================================================================================
def taxonomy():
    """AI > machine learning > deep learning > foundation models, with symbolic AI alongside."""
    fig, ax = canvas(7.0, 4.4, xlim=(0, 100), ylim=(0, 63))
    box(ax, 0.5, 0.5, 99, 62, fc="#F7F9FB", ec=NAVY, r=1.5, lw=1.1, z=0.2)
    ax.text(2.0, 60.6, "ARTIFICIAL INTELLIGENCE", fontsize=9, weight="bold", color=NAVY, va="top")
    ax.text(2.0, 57.2, "computer systems that perform tasks that normally need human intelligence: perceiving, "
            "reasoning, planning, deciding", fontsize=6.6, color=INK, va="top", style="italic")
    # symbolic AI panel
    box(ax, 2.0, 2.0, 33.0, 47.5, fc="white", ec=NAVY, r=1.0, lw=0.9, z=0.5)
    ax.text(18.5, 47.6, "Symbolic AI", fontsize=8.4, weight="bold", color=NAVY, ha="center", va="top")
    ax.text(18.5, 44.6, "knowledge written down by people", fontsize=6.4, color=GREY, ha="center", va="top",
            style="italic")
    items = [("Rules and expert systems", "INCO expert system, Shuttle\nMission Control (1988)"),
             ("Search, planning, scheduling", "SPIKE (Hubble), MEXAR2 (Mars\nExpress), Remote Agent (DS1)"),
             ("Constraint optimisation", "observation and downlink plans"),
             ("Model-based diagnosis", "fault isolation from a model\nof the spacecraft"),
             ("Fuzzy logic", "graded rules for control")]
    y = 40.8
    for head, ex in items:
        ax.text(3.6, y, "■", fontsize=5, color=NAVY, va="top")
        ax.text(5.4, y + 0.15, head, fontsize=6.6, weight="bold", color=INK, va="top")
        ax.text(5.4, y - 2.5, ex, fontsize=6.1, color="#3E4851", va="top", linespacing=1.15)
        y -= 7.3 if "\n" in ex else 5.6
    ax.text(3.6, 6.0, "+ decisions traceable and testable", fontsize=6.2, color=GREEN, ha="left",
            va="bottom", weight="bold")
    ax.text(3.6, 3.0, "– brittle outside the rules' assumptions", fontsize=6.2, color=RED, ha="left",
            va="bottom", weight="bold")
    # machine learning nest
    ax.add_patch(Ellipse((68.5, 25.5), 61, 47, fc="#EAF1F8", ec=BLUE, lw=1.1, zorder=1))
    ax.add_patch(Ellipse((72.5, 17.0), 40, 26, fc="#E4E0F0", ec=VIOLET, lw=1.0, zorder=2))
    ax.add_patch(Ellipse((73.0, 10.6), 31, 13.6, fc="#F6E3EC", ec=RED, lw=0.9, zorder=3))
    ax.text(68.5, 47.0, "Machine learning", fontsize=8.4, weight="bold", color=BLUE, ha="center", va="top", zorder=5)
    ax.text(68.5, 44.1, "knowledge learned from examples (data)", fontsize=6.4, color=GREY, ha="center", va="top",
            style="italic", zorder=5)
    ml_ex = ("Linear regression: sea-surface temperature (AVHRR)\n"
             "Decision trees, random forests: MODIS land cover\n"
             "Gradient boosting: Sentinel-2 cloud probability\n"
             "Support vector machines: EO-1 onboard classifiers\n"
             "k-means, PCA: unsupervised maps, IASI compression")
    ax.text(68.5, 41.4, ml_ex, fontsize=6.1, color=INK, ha="center", va="top", linespacing=1.22, zorder=5)
    ax.text(72.5, 28.6, "Deep learning", fontsize=7.8, weight="bold", color=VIOLET, ha="center", va="top", zorder=5)
    ax.text(72.5, 25.8, "many-layer neural networks\nCNN: Φsat-1 cloud screening\nLSTM: SMAP telemetry anomalies",
            fontsize=6.0, color=INK, ha="center", va="top", linespacing=1.25, zorder=5)
    ax.text(73.0, 15.6, "Foundation and\ngenerative models", fontsize=6.3, weight="bold", color=RED, ha="center",
            va="top", zorder=5, linespacing=1.05)
    ax.text(73.0, 11.4, "Prithvi (Earth observation),\nlanguage models",
            fontsize=5.8, color=INK, ha="center", va="top", linespacing=1.15, zorder=5)
    # statistics / estimation theory overlap
    ax.add_patch(Ellipse((43.5, 8.6), 15.5, 12.0, fc="#FFF9E8", ec=GOLD, lw=1.0, ls="--", zorder=1.5))
    ax.text(43.5, 12.6, "Statistics and\nestimation", fontsize=6.2, weight="bold", color="#8A6D12",
            ha="center", va="top", linespacing=1.05, zorder=5)
    ax.text(43.5, 7.7, "least squares,\nKalman filter", fontsize=5.8, color=INK, ha="center", va="top",
            linespacing=1.1, zorder=5)
    ax.text(98.0, 53.6, "+ learns patterns too complex to write down", fontsize=6.1, color=GREEN,
            ha="right", va="top", weight="bold", zorder=5)
    ax.text(98.0, 50.9, "– needs representative, well-labelled data; harder to verify", fontsize=6.1, color=RED,
            ha="right", va="top", weight="bold", zorder=5)
    save(fig, "ch43_taxonomy")


# ==============================================================================================
def pipeline():
    """Block diagram: where machine learning sits in a space data system, and the nine-step workflow."""
    fig, ax = canvas(7.0, 4.5, xlim=(0, 100), ylim=(0, 64))
    # --- top: system architecture
    ax.text(1, 63, "Where the model runs", fontsize=8.4, weight="bold", color=NAVY, va="top")
    box(ax, 1, 33.5, 27, 26.5, fc="#F2F6FA", ec=NAVY, r=1.0)
    ax.text(14.5, 58.6, "SPACE SEGMENT", fontsize=7, weight="bold", color=NAVY, ha="center", va="top")
    sp = [("Instrument", 52.5), ("Onboard processing\n(calibrate, tile)", 46.0), ("Edge model: screen clouds,\ndetect events",
                                                                                  39.0)]
    for t, yy in sp:
        box(ax, 3, yy - 2.6, 23, 5.4 if "\n" in t else 4.2, text=t, fs=6.2, fc="white", ec=BLUE, r=0.6)
    for y1, y2 in [(52.5 - 2.6, 46.0 + 2.8), (46.0 - 2.6, 39.0 + 2.8)]:
        arrow(ax, (14.5, y1), (14.5, y2), lw=0.9, ms=7)
    box(ax, 33, 33.5, 44, 26.5, fc="#F2F6FA", ec=NAVY, r=1.0)
    ax.text(55, 58.6, "GROUND SEGMENT", fontsize=7, weight="bold", color=NAVY, ha="center", va="top")
    gnd = [(35, 49.5, "Level-0/1\nprocessing"), (49, 49.5, "Archive and\ndata catalogue"),
           (63, 49.5, "Labels\n(experts, in situ)"),
           (35, 38.2, "Training and\nvalidation (GPU)"), (49, 38.2, "Model registry\n(versions, tests)"),
           (63, 38.2, "Inference\nservice")]
    for x, yy, t in gnd:
        box(ax, x, yy, 12, 6.0, text=t, fs=6.1, fc="white", ec=BLUE, r=0.6)
    arrow(ax, (47, 52.5), (49, 52.5), lw=0.9, ms=7)
    arrow(ax, (63, 52.5), (61, 52.5), lw=0.9, ms=7)
    arrow(ax, (55, 49.5), (41, 44.2), lw=0.9, ms=7, rad=0.0)
    arrow(ax, (47, 41.2), (49, 41.2), lw=0.9, ms=7)
    arrow(ax, (61, 41.2), (63, 41.2), lw=0.9, ms=7)
    arrow(ax, (55, 49.5), (69, 44.2), lw=0.9, ms=7, color=GREY)
    ax.text(70.2, 46.2, "new data", fontsize=5.6, color=GREY, ha="left")
    # downlink / uplink
    arrow(ax, (26, 39.5), (35, 50.5), lw=1.2, ms=8, color=ORANGE, rad=-0.25)
    ax.text(30.5, 58.6, "down-\nlink", fontsize=5.6, color=ORANGE, ha="center", va="top", linespacing=1.0,
            weight="bold")
    arrow(ax, (49, 38.2), (26, 36.5), lw=1.0, ms=7, color=VIOLET, ls="--", rad=-0.12)
    ax.text(37.0, 33.9, "uplink verified model", fontsize=5.9, color=VIOLET, ha="center")
    box(ax, 82, 33.5, 17, 26.5, fc="#F2F6FA", ec=NAVY, r=1.0)
    ax.text(90.5, 58.6, "USERS", fontsize=7, weight="bold", color=NAVY, ha="center", va="top")
    box(ax, 83.5, 46.5, 14, 7.5, text="Products,\nalerts, maps", fs=6.1, fc="white", ec=BLUE, r=0.6)
    box(ax, 83.5, 36.0, 14, 7.5, text="Decisions\nand feedback", fs=6.1, fc="white", ec=BLUE, r=0.6)
    arrow(ax, (75, 41.2), (83.5, 49.5), lw=0.9, ms=7)
    arrow(ax, (90.5, 46.5), (90.5, 43.5), lw=0.9, ms=7)
    arrow(ax, (83.5, 38.0), (75, 51.5), lw=0.9, ms=7, color=GREEN, rad=0.35)
    ax.text(79.5, 63.4, "feedback: new labels, error reports", fontsize=5.9, color=GREEN, ha="center", va="top")
    # --- bottom: workflow chevrons
    ax.text(1, 30.4, "How the model is built and kept honest", fontsize=8.4, weight="bold", color=NAVY, va="top")
    steps = [("1", "Define the\ndecision"), ("2", "Gather\ndata"), ("3", "Label"), ("4", "Set a\nbaseline"),
             ("5", "Split by\nspace, time"), ("6", "Train\nand tune"), ("7", "Evaluate,\nerror bars"),
             ("8", "Deploy\nand verify"), ("9", "Monitor\nfor drift")]
    w, gap, x0, yb, hgt = 10.2, 0.75, 1.0, 9.0, 12.5
    cols = [NAVY, NAVY, NAVY, BLUE, BLUE, BLUE, VIOLET, VIOLET, VIOLET]
    for k, ((num, txt), col) in enumerate(zip(steps, cols)):
        x = x0 + k * (w + gap)
        pts = [(x, yb), (x + w - 1.6, yb), (x + w, yb + hgt / 2), (x + w - 1.6, yb + hgt), (x, yb + hgt)]
        if k > 0:
            pts.append((x + 1.6, yb + hgt / 2))
        ax.add_patch(Polygon(pts, closed=True, fc=col, ec="white", lw=1.0, zorder=2))
        ax.text(x + w / 2 + 0.2, yb + hgt - 1.6, num, fontsize=8, weight="bold", color="white", ha="center",
                va="top", zorder=3)
        ax.text(x + w / 2 + 0.3, yb + hgt / 2 - 1.3, txt, fontsize=5.8, color="white", ha="center", va="center",
                zorder=3, linespacing=1.1)
    xe = x0 + 8 * (w + gap) + w / 2
    xs = x0 + 1 * (w + gap) + w / 2
    ax.annotate("", xy=(xs, yb - 0.3), xytext=(xe, yb - 0.3),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.2, connectionstyle="arc3,rad=-0.1",
                                mutation_scale=9))
    ax.text((xs + xe) / 2, 2.6, "retrain or relabel when performance drifts (new sensor, new region, ageing detector)",
            fontsize=6.2, color=ORANGE, ha="center", va="center")
    for k, (txt, col) in enumerate([("problem and data", NAVY), ("model building", BLUE),
                                    ("assurance and operations", VIOLET)]):
        ax.text(x0 + (3 * k + 1.5) * (w + gap) - gap / 2, 22.6, txt, fontsize=6.2, color=col, ha="center",
                style="italic")
    save(fig, "ch43_pipeline")


if __name__ == "__main__":
    fns = [timeline, taxonomy, pipeline, gdpaths, mlpoverfit, boundaries, rocpr, learning, kmeanspca, spatialcv]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
