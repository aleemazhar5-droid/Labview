"""Figures for Chapter 52 - AI in Spacecraft Design, Manufacturing, Launch and the Space Business.

Most figures run real optimisation, statistics or machine-learning code with fixed random seeds on synthetic
data built from simple physical models, or plot published data:
  pipeline   - block diagram: where AI enters the life cycle, and the verification gate (diagram)
  topopt     - SIMP topology optimisation of a 2-D cantilever (numpy/scipy finite elements, optimality criteria)
  bayesopt   - Bayesian optimisation with a Gaussian-process surrogate (scikit-learn) vs random search on a toy
               Earth-observation smallsat design model
  production - payloads launched per year and their mass classes, from GCAT (J. McDowell), data/gcat_*.json
  ammonitor  - simulated in-situ melt-pool monitoring and hit/miss probability-of-detection (POD) curves
  inspection - defect classifier on synthetic X-ray CT patches: ROC curves and the cost-optimal threshold
  engine     - turbopump vibration health monitoring: fixed redline vs a learned multivariate detector
  launchrisk - launch failure rates from GCAT and a Bayesian (beta-binomial) model for new vehicles
  capacity   - satellites in view versus latitude, and constellation sizing by linear programming
Numbers quoted in the chapter are printed by each function.
"""
import json
import os
import sys
import textwrap
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch  # noqa: F401
from matplotlib.lines import Line2D  # noqa: F401
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker

ROOT = Path(__file__).resolve().parents[2]
FOOT = 6.0


def panel_tag(ax, s, x=-0.02, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, weight="bold", ha="right", va="bottom", color=INK)


def foot(fig, text, y=0.01, width=165):
    fig.text(0.99, y, "\n".join(textwrap.wrap(text, width)), ha="right", va="bottom", fontsize=FOOT, color=GREY,
             multialignment="right", linespacing=1.25)


# ==============================================================================================
# 1. Block diagram: AI across the life cycle, with a verification gate
def pipeline():
    fig, ax = canvas(7.0, 4.1, xlim=(0, 140), ylim=(0, 82))
    stages = [
        ("Requirements", "language\nmodels: quality\nchecks, trace\nlinks, lessons-\nlearned search"),
        ("Concept\nand trades", "surrogates,\nBayesian\noptimisation,\ntrade-space\nexploration"),
        ("Detailed\ndesign", "topology\noptimisation,\ngenerative\ndesign, code\nassistants"),
        ("Manufacture", "in-situ\nprocess\nmonitoring,\nCT and visual\ndefect checks"),
        ("Integration\nand test", "test-data\nanomaly\ndetection,\nsignature\ncomparison"),
        ("Launch", "engine health,\nweather,\nrange\nscheduling"),
        ("Operations\nand business", "analytics,\ncapacity,\npricing,\ninsurance\nrisk models"),
    ]
    w, gap, x0 = 18.4, 1.6, 0.6
    label(ax, 0.6, 79.5, "LIFE-CYCLE STAGE and where AI helps", fs=7.4, color=NAVY, ha="left", weight="bold")
    xs = []
    for i, (t, b) in enumerate(stages):
        x = x0 + i * (w + gap)
        xs.append(x)
        hc = NAVY if i < 5 else BLUE
        box(ax, x, 39, w, 37, fc=LIGHT, ec=hc, r=0.8)
        ax.add_patch(FancyBboxPatch((x, 66.5), w, 9.5, boxstyle="round,pad=0,rounding_size=0.8", fc=hc, ec=hc,
                                    zorder=2.5))
        label(ax, x + w / 2, 71.2, t, fs=6.7, color="white", weight="bold")
        label(ax, x + w / 2, 52.5, b, fs=6.2)
        if i < len(stages) - 1:
            arrow(ax, (x + w + 0.1, 71.2), (x + w + gap - 0.1, 71.2), lw=1.0, ms=6)
    # verification gate
    box(ax, 0.6, 24.5, 138.8, 10, "", fc="#FCEFE3", ec=ORANGE, r=1.0, lw=1.1)
    label(ax, 70, 31.4, "VERIFICATION GATE before anything enters the controlled baseline", fs=7.2, color=ORANGE,
          weight="bold")
    label(ax, 70, 27.2, "high-fidelity analysis  ·  qualification test  ·  inspection  ·  review by a "
          "responsible engineer  ·  configuration control", fs=6.6, color=INK)
    for x in xs:
        arrow(ax, (x + w / 2, 38.6), (x + w / 2, 35.0), color=ORANGE, lw=1.0, ms=7)
    # digital thread
    box(ax, 0.6, 3, 138.8, 15.5, "", fc=LIGHT, ec=NAVY, r=1.0)
    label(ax, 70, 14.6, "DIGITAL THREAD: one linked record of requirements, models, analyses, build and test data",
          fs=7.2, color=NAVY, weight="bold")
    label(ax, 70, 8.6, "every stage writes labelled data that train and check the next generation of models;\n"
          "test and flight results flow back as ground truth", fs=6.6)
    for x in xs:
        arrow(ax, (x + w / 2, 24.2), (x + w / 2, 18.8), color=NAVY, lw=0.9, ms=6, style="<|-|>")
    save(fig, "ch52_pipeline")


# ==============================================================================================
# 2. SIMP topology optimisation of a cantilever (after Andreassen et al. 2011, "88-line" code)
def _lk(nu=0.3):
    k = np.array([1 / 2 - nu / 6, 1 / 8 + nu / 8, -1 / 4 - nu / 12, -1 / 8 + 3 * nu / 8, -1 / 4 + nu / 12,
                  -1 / 8 - nu / 8, nu / 6, 1 / 8 - 3 * nu / 8])
    KE = 1 / (1 - nu ** 2) * np.array([
        [k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7]],
        [k[1], k[0], k[7], k[6], k[5], k[4], k[3], k[2]],
        [k[2], k[7], k[0], k[5], k[6], k[3], k[4], k[1]],
        [k[3], k[6], k[5], k[0], k[7], k[2], k[1], k[4]],
        [k[4], k[5], k[6], k[7], k[0], k[1], k[2], k[3]],
        [k[5], k[4], k[3], k[2], k[1], k[0], k[7], k[6]],
        [k[6], k[3], k[4], k[1], k[2], k[7], k[0], k[5]],
        [k[7], k[2], k[1], k[4], k[3], k[6], k[5], k[0]]])
    return KE


class Cantilever:
    """2-D plane-stress cantilever: left edge clamped, unit downward load at mid-height of the right edge."""

    def __init__(self, nelx, nely, rmin=1.5):
        from scipy.sparse import coo_matrix
        self.nelx, self.nely = nelx, nely
        self.KE = _lk()
        ne = nelx * nely
        self.ndof = 2 * (nelx + 1) * (nely + 1)
        edof = np.zeros((ne, 8), dtype=int)
        for elx in range(nelx):
            for ely in range(nely):
                el = ely + elx * nely
                n1 = (nely + 1) * elx + ely
                n2 = (nely + 1) * (elx + 1) + ely
                edof[el] = [2 * n1 + 2, 2 * n1 + 3, 2 * n2 + 2, 2 * n2 + 3, 2 * n2, 2 * n2 + 1, 2 * n1, 2 * n1 + 1]
        self.edof = edof
        self.iK = np.kron(edof, np.ones((8, 1))).flatten()
        self.jK = np.kron(edof, np.ones((1, 8))).flatten()
        fixed = np.arange(0, 2 * (nely + 1))
        self.free = np.setdiff1d(np.arange(self.ndof), fixed)
        remap = -np.ones(self.ndof, dtype=int)
        remap[self.free] = np.arange(self.free.size)
        self.mask = (remap[self.iK.astype(int)] >= 0) & (remap[self.jK.astype(int)] >= 0)
        self.iKf = remap[self.iK.astype(int)][self.mask]
        self.jKf = remap[self.jK.astype(int)][self.mask]
        self.f = np.zeros(self.ndof)
        node = (nely + 1) * nelx + nely // 2
        self.f[2 * node + 1] = -1.0
        # density filter
        rc = int(np.ceil(rmin))
        iH, jH, sH = [], [], []
        for i in range(nelx):
            for j in range(nely):
                row = i * nely + j
                for k in range(max(i - rc + 1, 0), min(i + rc, nelx)):
                    for l in range(max(j - rc + 1, 0), min(j + rc, nely)):
                        fac = rmin - np.hypot(i - k, j - l)
                        if fac > 0:
                            iH.append(row)
                            jH.append(k * nely + l)
                            sH.append(fac)
        self.H = coo_matrix((sH, (iH, jH)), shape=(ne, ne)).tocsr()
        self.Hs = np.asarray(self.H.sum(1)).ravel()

    def solve(self, xPhys, penal=3.0, Emin=1e-9):
        from scipy.sparse import coo_matrix
        from scipy.sparse.linalg import spsolve
        sK = ((self.KE.flatten()[np.newaxis]).T * (Emin + xPhys ** penal * (1 - Emin))).flatten(order="F")
        nf = self.free.size
        K = coo_matrix((sK[self.mask], (self.iKf, self.jKf)), shape=(nf, nf)).tocsc()
        u = np.zeros(self.ndof)
        u[self.free] = spsolve(K, self.f[self.free], permc_spec="MMD_AT_PLUS_A")
        ue = u[self.edof]
        ce = np.sum((ue @ self.KE) * ue, axis=1)
        c = float(np.sum((Emin + xPhys ** penal * (1 - Emin)) * ce))
        return c, ce

    def optimise(self, volfrac, penal=3.0, maxit=150, tol=0.01, snaps=()):
        ne = self.nelx * self.nely
        x = volfrac * np.ones(ne)
        xPhys = x.copy()
        hist, shots = [], {}
        for it in range(1, maxit + 1):
            c, ce = self.solve(xPhys, penal)
            dc = -penal * xPhys ** (penal - 1) * (1 - 1e-9) * ce
            dv = np.ones(ne)
            dc = self.H @ (dc / self.Hs)
            dv = self.H @ (dv / self.Hs)
            l1, l2, move = 0.0, 1e9, 0.2
            while (l2 - l1) / (l1 + l2) > 1e-4:
                lmid = 0.5 * (l1 + l2)
                xnew = np.clip(x * np.sqrt(np.maximum(-dc, 1e-30) / dv / lmid), np.maximum(0, x - move),
                               np.minimum(1, x + move))
                xPhysNew = (self.H @ xnew) / self.Hs
                if xPhysNew.sum() > volfrac * ne:
                    l1 = lmid
                else:
                    l2 = lmid
            change = np.max(np.abs(xnew - x))
            x, xPhys = xnew, xPhysNew
            hist.append((it, c, change))
            if it in snaps:
                shots[it] = xPhys.copy()
            if change < tol and it > 20:
                break
        shots["final"] = xPhys.copy()
        return xPhys, np.array(hist), shots

    def img(self, x):
        return x.reshape((self.nelx, self.nely)).T


def topopt():
    t0 = time.time()
    nelx, nely, vf = 120, 40, 0.40
    cant = Cantilever(nelx, nely, rmin=1.6)
    xP, hist, shots = cant.optimise(vf, snaps=(1, 5, 20))
    c_full, _ = cant.solve(np.ones(nelx * nely))
    xb = (xP > 0.5).astype(float)
    v_bw = xb.mean()
    c_bw, _ = cant.solve(np.maximum(xb, 1e-3), penal=1.0)
    c_grey = hist[-1, 1]
    t_eq = c_full / c_bw
    saving = 1 - v_bw / t_eq
    print(f"topopt: {len(hist)} iterations, compliance first {hist[0,1]:.1f} final(grey) {c_grey:.1f}; "
          f"solid plate C={c_full:.2f}; black-white design vol={v_bw:.3f}, C={c_bw:.2f}; "
          f"uniform plate needs thickness {t_eq:.3f} of solid -> mass saving {100*saving:.1f}%")
    # sweep of volume fractions (black-and-white compliance)
    sweep = []
    for v in (0.2, 0.3, 0.4, 0.5, 0.6):
        xs, h, _ = (xP, hist, None) if v == vf else cant.optimise(v, maxit=120)
        xbs = (xs > 0.5).astype(float)
        cb, _ = cant.solve(np.maximum(xbs, 1e-3), penal=1.0)
        sweep.append((xbs.mean(), cb / c_full, len(h)))
        print(f"   vol {v:.1f}: bw vol {xbs.mean():.3f}, C/Cfull {cb/c_full:.3f}, uniform-plate mass for same "
              f"stiffness {c_full/cb:.3f} -> saving {100*(1 - xbs.mean()*cb/c_full):.1f}%")
    sweep = np.array(sweep)

    fig = plt.figure(figsize=(7.0, 4.25))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 1.25, 1.0], height_ratios=[1, 1], wspace=0.32, hspace=0.62,
                          left=0.03, right=0.985, top=0.93, bottom=0.21)
    cmap = LinearSegmentedColormap.from_list("d", ["white", "#9DB8CF", NAVY])
    keys = [(1, "iteration 1"), (5, "iteration 5"), (20, "iteration 20"), ("final", f"final (iteration {len(hist)})")]
    pos = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for (k, lab), (r, cc) in zip(keys, pos):
        ax = fig.add_subplot(gs[r, cc])
        ax.imshow(cant.img(shots[k]), cmap=cmap, vmin=0, vmax=1, interpolation="nearest", aspect="equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(True)
            s.set_color("#9AA5AE")
        ax.set_title(lab, fontsize=7.6, weight="normal", pad=3)
        # clamp hatch and load arrow
        ax.plot([-0.5, -0.5], [-0.5, nely - 0.5], color=INK, lw=2.5, clip_on=False)
        ax.annotate("", xy=(nelx + 1.5, nely / 2 + 1), xytext=(nelx + 1.5, nely / 2 - 15),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.3, mutation_scale=8), annotation_clip=False)
        if (r, cc) == (0, 0):
            panel_tag(ax, "(a)", x=0.0, y=1.06)
            ax.text(0.03, -0.13, "clamped edge", transform=ax.transAxes, fontsize=6.2, color=INK, va="top")
            ax.text(0.97, -0.13, "load F", transform=ax.transAxes, fontsize=6.2, color=RED, va="top", ha="right")
    ax = fig.add_subplot(gs[0, 2])
    ax.semilogy(hist[:, 0], hist[:, 1], color=BLUE)
    ax.set_xlabel("iteration")
    ax.set_ylabel("compliance", labelpad=1)
    ax.set_title("convergence", fontsize=8, weight="normal")
    panel_tag(ax, "(b)")
    ax.set_xlim(0, len(hist) + 2)
    ax.set_yticks([200, 500, 1000, 2000])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax = fig.add_subplot(gs[1, 2])
    vv = np.linspace(0.15, 1.0, 50)
    ax.plot(vv, 1 / vv, color=GREY, lw=1.3, label="uniform plate")
    ax.plot(sweep[:, 0], sweep[:, 1], "o-", color=ORANGE, ms=3.5, label="optimised")
    ax.set_yscale("log")
    ax.set_xlabel("mass (fraction of solid block)")
    ax.set_ylabel("compliance / solid")
    ax.set_xlim(0.15, 1.02)
    ax.set_ylim(0.9, 8)
    ax.set_yticks([1, 2, 4, 8])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    i4 = 2
    ax.annotate("", xy=(sweep[i4, 0], sweep[i4, 1]), xytext=(1 / sweep[i4, 1], sweep[i4, 1]),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.1))
    ax.annotate(f"{100*(1 - sweep[i4,0]*sweep[i4,1]):.0f} % less mass", xy=(0.5 * (sweep[i4, 0] + 1 / sweep[i4, 1]),
                sweep[i4, 1]), xytext=(0.62, 2.6), fontsize=6.6, color=GREEN, ha="left",
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.6))
    ax.legend(loc="upper right", fontsize=6.6, handlelength=1.4)
    panel_tag(ax, "(c)")
    ax.set_title("same stiffness, less mass", fontsize=8, weight="normal")
    foot(fig, "SIMP method (penalty p = 3, density filter radius 1.6 elements, optimality-criteria update) on 120 × 40 "
         "four-node plane-stress elements, written in numpy/scipy after Andreassen et al. (2011). Compliance in (c) is "
         "recomputed for the black-and-white design (densities > 0.5 set to solid). The uniform plate is a plate of "
         "reduced thickness, whose stiffness scales with mass.", width=170)
    save(fig, "ch52_topopt")
    print(f"   time {time.time()-t0:.1f} s")



# ==============================================================================================
# 3. Bayesian optimisation with a Gaussian-process surrogate vs random search
BO_LO = np.array([400.0, 0.15, 1.0, 0.0])
BO_HI = np.array([800.0, 0.60, 6.0, 60.0])


def design_value(u):
    """Toy EO smallsat model. u in [0,1]^4 -> (altitude km, aperture m, array m2, propellant kg).
    Returns image value per $M (arbitrary units): lifetime x images/day x value(GSD) / cost."""
    u = np.atleast_2d(u)
    x = BO_LO + u * (BO_HI - BO_LO)
    h, D, A, mp = x.T
    m = 40 + 300 * D ** 2.2 + 5 * A + mp                       # dry + propellant mass, kg
    dv_yr = 60 * np.exp(-(h - 400) / 60) * (150 / m)            # drag make-up, m/s per year
    dv = 220 * 9.81 * np.log(m / (m - mp + 1e-9))               # hydrazine, Isp 220 s
    life = np.minimum(7.0, 0.5 * np.exp((h - 400) / 90) + dv / np.maximum(dv_yr, 1e-9))
    gsd = 1.22 * 550e-9 * h * 1e3 / D                           # diffraction-limited GSD, m
    p_img = 120 * A - 50 - 150 * D ** 2                         # power left for imaging and downlink, W
    n_img = 400 * (1 - np.exp(-np.maximum(p_img, 0) / 150))    # images per day, downlink-limited
    value = 1 / (1 + gsd ** 2)                                  # value per image falls beyond ~1 m
    cost = 8 + 0.15 * m                                         # $M
    return life * n_img * 365 * value / cost / 1000


def _gp(seed):
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern, ConstantKernel, WhiteKernel
    k = ConstantKernel(1.0) * Matern(length_scale=[0.3] * 4, length_scale_bounds=(0.02, 5), nu=2.5) + \
        WhiteKernel(1e-4, (1e-8, 1e-2))
    return GaussianProcessRegressor(k, normalize_y=True, n_restarts_optimizer=1, random_state=seed)


def _ei(mu, sd, best, xi):
    from scipy.stats import norm
    sd = np.maximum(sd, 1e-12)
    imp = mu - best - xi
    z = imp / sd
    return imp * norm.cdf(z) + sd * norm.pdf(z)


def bo_run(seed, n=40, n0=6):
    import warnings
    warnings.filterwarnings("ignore")
    r = np.random.default_rng(seed)
    X = (np.argsort(r.random((n0, 4)), axis=0) + r.random((n0, 4))) / n0      # Latin hypercube start
    Y = design_value(X)
    for _ in range(n - n0):
        gp = _gp(seed).fit(X, Y)
        cand = np.vstack([r.random((3000, 4)),
                          np.clip(X[np.argmax(Y)] + 0.05 * r.standard_normal((1000, 4)), 0, 1)])
        mu, sd = gp.predict(cand, return_std=True)
        xn = cand[np.argmax(_ei(mu, sd, Y.max(), 0.01 * abs(Y.max())))]
        X = np.vstack([X, xn])
        Y = np.append(Y, design_value(xn))
    return X, Y


def bayesopt():
    import warnings
    from scipy.optimize import minimize
    warnings.filterwarnings("ignore")
    t0 = time.time()
    rng = np.random.default_rng(0)
    U = rng.random((200000, 4))
    yU = design_value(U)
    starts = U[np.argsort(-yU)[:20]]
    res = [minimize(lambda u: -design_value(u)[0], s0, bounds=[(0, 1)] * 4) for s0 in starts]
    best = min(res, key=lambda q: q.fun)
    Jopt, uopt = -best.fun, best.x
    xopt = BO_LO + uopt * (BO_HI - BO_LO)
    p95 = np.mean(yU >= 0.95 * Jopt)
    p98 = np.mean(yU >= 0.98 * Jopt)
    print(f"bayesopt: optimum J={Jopt:.2f} at h={xopt[0]:.0f} km, D={xopt[1]:.3f} m, A={xopt[2]:.2f} m2, "
          f"mp={xopt[3]:.1f} kg; random-sample share >=95%: {100*p95:.3f}% (expected {1/p95:.0f} evals), "
          f">=98%: {100*p98:.4f}% (expected {1/p98:.0f}); median random value {np.median(yU)/Jopt:.2f} of opt")
    nseed, nb, nr = 12, 40, 500
    B = np.array([np.maximum.accumulate(bo_run(s, nb)[1]) for s in range(nseed)]) / Jopt
    R = np.array([np.maximum.accumulate(design_value(np.random.default_rng(100 + s).random((nr, 4))))
                  for s in range(nseed)]) / Jopt

    def reach(curves, f):
        return np.array([np.argmax(c >= f) + 1 if (c >= f).any() else np.nan for c in curves])
    nb95, nr95 = reach(B, 0.95), reach(R, 0.95)
    print(f"   BO reaches 95% in {np.sum(~np.isnan(nb95))}/{nseed} runs within {nb}; median {np.nanmedian(nb95):.0f} "
          f"evals; random reaches 95% in {np.sum(~np.isnan(nr95))}/{nseed} runs within {nr}; median of those "
          f"{np.nanmedian(nr95):.0f}")
    print(f"   median best after 10/20/40 evals: BO {np.median(B[:,9]):.3f}/{np.median(B[:,19]):.3f}/"
          f"{np.median(B[:,39]):.3f}; random {np.median(R[:,9]):.3f}/{np.median(R[:,19]):.3f}/{np.median(R[:,39]):.3f}"
          f"; random after 500: {np.median(R[:,-1]):.3f}")

    fig = plt.figure(figsize=(7.0, 3.35))
    gs = fig.add_gridspec(2, 3, height_ratios=[2.3, 1], width_ratios=[1.1, 1.15, 0.8], wspace=0.42, hspace=0.12,
                          left=0.075, right=0.985, top=0.91, bottom=0.3)
    # (a) 1-D illustration along altitude, other variables at their optimum
    hh = np.linspace(0, 1, 300)
    Ug = np.tile(uopt, (300, 1))
    Ug[:, 1] = hh
    ytrue = design_value(Ug)
    xs = np.array([0.04, 0.3, 0.52, 0.96])
    Us = np.tile(uopt, (len(xs), 1))
    Us[:, 1] = xs
    ys = design_value(Us)
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern, ConstantKernel
    gp1 = GaussianProcessRegressor(ConstantKernel(1.0) * Matern(0.2, (0.05, 2), nu=2.5), normalize_y=True,
                                   alpha=1e-6).fit(xs[:, None], ys)
    mu, sd = gp1.predict(hh[:, None], return_std=True)
    ei = _ei(mu, sd, ys.max(), 0.0)
    halt = BO_LO[1] + hh * (BO_HI[1] - BO_LO[1])
    ax = fig.add_subplot(gs[0, 0])
    ax.fill_between(halt, mu - 2 * sd, mu + 2 * sd, color=SKY, alpha=0.35, lw=0, label="GP ±2σ")
    ax.plot(halt, ytrue, color=INK, lw=1.0, ls="--", label="true (hidden)")
    ax.plot(halt, mu, color=BLUE, lw=1.4, label="GP mean")
    ax.plot(BO_LO[1] + xs * (BO_HI[1] - BO_LO[1]), ys, "o", color=ORANGE, ms=4, zorder=5, label="4 runs")
    ax.set_ylabel("value per $M")
    ax.set_xticklabels([])
    ax.set_xlim(BO_LO[1], BO_HI[1])
    ax.set_ylim(0, 35)
    ax.legend(fontsize=6.0, loc="lower center", ncol=2, handlelength=1.3, columnspacing=0.8)
    panel_tag(ax, "(a)")
    ax.set_title("surrogate after 4 runs", fontsize=8, weight="normal")
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.fill_between(halt, 0, ei / ei.max(), color=GREEN, alpha=0.4, lw=0)
    ax2.plot(halt, ei / ei.max(), color=GREEN, lw=1.0)
    xn = halt[np.argmax(ei)]
    ax2.axvline(xn, color=GREEN, lw=0.8, ls=":")
    ax2.text(xn + 0.01, 0.62, "next run", fontsize=6.2, color=GREEN)
    ax2.set_yticks([])
    ax2.set_ylabel("EI", fontsize=7)
    ax2.set_xlabel("telescope aperture (m)")
    ax2.set_xlim(BO_LO[1], BO_HI[1])
    # (b) convergence
    ax = fig.add_subplot(gs[:, 1])
    nn = np.arange(1, nr + 1)
    for C, col, lab, n in ((R, GREY, "random search", nr), (B, ORANGE, "Bayesian optimisation", nb)):
        q1, q2, q3 = np.percentile(C, [25, 50, 75], axis=0)
        ax.fill_between(nn[:n], q1, q3, color=col, alpha=0.25, lw=0)
        ax.plot(nn[:n], q2, color=col, lw=1.6, label=lab)
    ax.axhline(0.95, color=RED, lw=0.8, ls="--")
    ax.text(1.1, 0.958, "95 % of optimum", fontsize=6.4, color=RED)
    ax.set_xscale("log")
    ax.set_xlim(1, nr)
    ax.set_ylim(0.3, 1.02)
    ax.set_xlabel("expensive evaluations")
    ax.set_ylabel("best design found / optimum")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    ax.legend(fontsize=6.6, loc="lower right")
    panel_tag(ax, "(b)")
    ax.set_title("median and quartiles, 12 runs", fontsize=8, weight="normal")
    # (c) evaluations to reach 95%
    ax = fig.add_subplot(gs[:, 2])
    rr = np.random.default_rng(1)
    for i, (v, col) in enumerate(((nb95, ORANGE), (nr95, GREY))):
        ok = ~np.isnan(v)
        ax.plot(i + 0.12 * rr.standard_normal(ok.sum()), v[ok], "o", color=col, ms=3.5, alpha=0.85)
        if (~ok).any():
            ax.plot(i + 0.12 * rr.standard_normal((~ok).sum()), np.full((~ok).sum(), 900 if i else 70),
                    "x", color=col, ms=4)
        ax.plot([i - 0.3, i + 0.3], [np.nanmedian(v)] * 2, color=INK, lw=1.4)
    ax.axhline(1 / p95, color=GREY, ls=":", lw=0.9)
    ax.text(0.5, 1 / p95 * 1.12, f"random, expected ≈ {1/p95:.0f}", fontsize=5.9, color=GREY, va="bottom",
            ha="center")
    ax.set_yscale("log")
    ax.set_ylim(2, 1500)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Bayesian", "random"], fontsize=7)
    ax.set_xlim(-0.6, 1.5)
    ax.set_ylabel("evaluations to reach 95 %")
    panel_tag(ax, "(c)")
    ax.set_title("cost to get close", fontsize=8, weight="normal")
    foot(fig, "Toy model of an Earth-observation smallsat standing in for an expensive simulation: four variables "
         "(altitude 400–800 km, aperture 0.15–0.6 m, array 1–6 m², propellant 0–60 kg); value = lifetime × images "
         "per day × value per image / cost. Gaussian process with a Matérn kernel (scikit-learn), expected-improvement "
         "(EI) acquisition, 6 Latin-hypercube starts, 40 evaluations; crosses = runs that did not reach 95 %. In (a) "
         "the other three variables are held at their optimum values.", width=175)
    save(fig, "ch52_bayesopt")
    print(f"   time {time.time()-t0:.1f} s")


# ==============================================================================================
# 4. Payloads launched per year and mass classes (GCAT)
def production():
    g = json.load(open(ROOT / "data" / "gcat_stats.json"))
    ex = json.load(open(ROOT / "data" / "gcat_extra.json"))
    yrs = np.arange(2000, 2027)
    tot = np.array([g["payloads_launched_by_year"].get(str(y), 0) for y in yrs])
    stl = np.array([g["starlink_launched_by_year"].get(str(y), 0) for y in yrs])
    print("production: payloads", dict(zip(yrs[-8:], tot[-8:])), "starlink", dict(zip(yrs[-8:], stl[-8:])),
          "updated", g["updated"])
    print(f"   2025 starlink share {100*stl[-2]/tot[-2]:.0f}%  ; 2015->2025 x{tot[-2]/tot[15]:.1f}")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.75), gridspec_kw=dict(width_ratios=[1.25, 1], wspace=0.3))
    ax = axs[0]
    full = yrs < 2026
    ax.bar(yrs[full], (tot - stl)[full], color=BLUE, width=0.75, label="other payloads")
    ax.bar(yrs[full], stl[full], bottom=(tot - stl)[full], color=ORANGE, width=0.75, label="Starlink")
    ax.bar(yrs[~full], (tot - stl)[~full], color=BLUE, width=0.75, alpha=0.45, hatch="///", ec="white", lw=0)
    ax.bar(yrs[~full], stl[~full], bottom=(tot - stl)[~full], color=ORANGE, width=0.75, alpha=0.45, hatch="///",
           ec="white", lw=0)
    ax.text(2026, tot[-1] / 2, "2026 to 13 Oct", fontsize=6.0, ha="center", va="center", color=INK, rotation=90)
    ax.text(2025, tot[-2] + 90, f"{tot[-2]:,}".replace(",", " "), fontsize=6.6, ha="center", color=INK)
    ax.set_ylabel("payloads launched per year")
    ax.legend(loc="upper left", fontsize=7)
    ax.set_xlim(1999.3, 2026.7)
    panel_tag(ax, "(a)")
    ax = axs[1]
    classes = ["<10 kg", "10–100 kg", "100–500 kg", "500–2500 kg", ">2500 kg"]
    cols = [GREY, SKY, GREEN, ORANGE, NAVY]
    yy = np.arange(2000, 2026)
    M = np.array([[ex["mass_class_by_year"][str(y)].get(c, 0) for y in yy] for c in classes], float)
    M = M / M.sum(0) * 100
    ax.stackplot(yy, M, colors=cols, labels=classes, alpha=0.9, lw=0)
    ax.set_xlim(2000, 2025)
    ax.set_ylim(0, 100)
    ax.set_ylabel("share of payloads (%)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, fontsize=6.4, handlelength=1.0,
              columnspacing=0.8)
    ax.grid(False)
    panel_tag(ax, "(b)")
    print("   2025 mass-class shares", dict(zip(classes, np.round(M[:, -1], 1))))
    fig.text(0.99, 0.0, "Data: GCAT (J. McDowell), payloads by launch year and mass class, updated 13 October 2026.",
             ha="right", va="bottom", fontsize=FOOT, color=GREY)
    fig.subplots_adjust(left=0.08, right=0.99, top=0.93, bottom=0.27)
    save(fig, "ch52_production")


# ==============================================================================================
# 5. In-situ monitoring of powder-bed fusion and hit/miss POD curves
def _pod_fit(a, hit):
    from sklearn.linear_model import LogisticRegression
    m = LogisticRegression(C=1e6, max_iter=2000).fit(np.log(a)[:, None], hit)
    b0, b1 = m.intercept_[0], m.coef_[0, 0]
    a90 = np.exp((np.log(9) - b0) / b1)
    return b0, b1, a90


def ammonitor():
    t0 = time.time()
    r = np.random.default_rng(7)
    # (a) a synthetic layer image: melt-pool emission with scan stripes and two flaws
    n = 96
    yy, xx = np.mgrid[0:n, 0:n]
    img = 1 + 0.05 * np.sin(2 * np.pi * (xx + yy) / 9.0) + 0.06 * r.standard_normal((n, n))
    flaws = [(30, 62, 3.0, 0.55), (70, 25, 1.4, 0.45), (55, 80, 0.8, 0.35)]
    for cx, cy, sz, c in flaws:
        img -= c * np.exp(-0.5 * ((xx - cx) ** 2 + (yy - cy) ** 2) / (sz ** 2 + 1.0))
    from scipy import ndimage
    sm = ndimage.gaussian_filter(img, 1.0)
    z = (sm - ndimage.median_filter(sm, 9)) / 0.025
    # (b) hit/miss trials
    sensors = {"in-situ camera (80 µm pixels)": dict(px=80.0, noise=0.08, c=(0.3, 0.9), col=ORANGE),
               "X-ray CT (25 µm voxels)": dict(px=25.0, noise=0.06, c=(0.6, 1.0), col=BLUE)}
    res = {}
    for name, sp in sensors.items():
        a = np.exp(r.uniform(np.log(15), np.log(800), 400))
        c = r.uniform(*sp["c"], a.size)
        sig = c * (1 - np.exp(-(a / 2) ** 2 / (2 * sp["px"] ** 2)))      # disc blurred by 1-pixel Gaussian PSF
        meas = sig + sp["noise"] * r.standard_normal(a.size)
        hit = (meas > 3.5 * sp["noise"]).astype(int)                         # threshold for low false calls
        b0, b1, a90 = _pod_fit(a, hit)
        boots = []
        for _ in range(300):
            idx = r.integers(0, a.size, a.size)
            boots.append(_pod_fit(a[idx], hit[idx])[2])
        a9095 = np.percentile(boots, 95)
        res[name] = (a, hit, b0, b1, a90, a9095, sp["col"])
        print(f"ammonitor: {name}: a90 = {a90:.0f} µm, a90/95 = {a9095:.0f} µm, hits {hit.mean():.2f}")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.05), gridspec_kw=dict(width_ratios=[0.8, 1.4], wspace=0.25))
    ax = axs[0]
    ax.imshow(img, cmap="inferno", vmin=0.55, vmax=1.2, interpolation="bilinear")
    lab, nl = ndimage.label(z < -4.0)
    for k, sl in enumerate(ndimage.find_objects(lab)):
        if (lab[sl] == k + 1).sum() < 3:
            continue
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        ax.add_patch(Rectangle((x0 - 2.5, y0 - 2.5), x1 - x0 + 4, y1 - y0 + 4, fill=False, ec="#7FE0FF", lw=1.1))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_title("one layer, flagged spots", fontsize=8, weight="normal")
    ax.plot([6, 6 + 1000 / 80], [90, 90], color="white", lw=2)
    ax.text(6 + 500 / 80, 87, "1 mm", color="white", fontsize=6.4, ha="center", va="bottom")
    panel_tag(ax, "(a)")
    ax = axs[1]
    aa = np.exp(np.linspace(np.log(15), np.log(800), 300))
    for k, (name, (a, hit, b0, b1, a90, a9095, col)) in enumerate(res.items()):
        jit = 0.035 * (k * 2 - 1)
        ax.plot(a, hit + jit + 0.012 * r.standard_normal(a.size), "|", color=col, ms=3.5, alpha=0.35)
        ax.plot(aa, 1 / (1 + np.exp(-(b0 + b1 * np.log(aa)))), color=col, lw=1.8, label=name)
        ax.plot([a9095, a9095], [0, 0.9], color=col, ls=":", lw=1.0)
        ax.text(a9095 * 1.05, 0.33 + 0.18 * k, f"$a_{{90/95}}$ ≈ {a9095:.0f} µm", fontsize=6.6, color=col)
    ax.axhline(0.9, color=GREY, lw=0.7, ls="--")
    ax.set_xscale("log")
    ax.set_xlim(15, 800)
    ax.set_ylim(-0.08, 1.08)
    ax.set_xticks([20, 50, 100, 200, 500])
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("flaw diameter (µm)")
    ax.set_ylabel("probability of detection")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=6.6, ncol=2, columnspacing=1.0)
    panel_tag(ax, "(b)", y=1.09)
    foot(fig, "Synthetic data. (a) Simulated melt-pool emission image of one 7.7 mm × 7.7 mm layer with scan-track "
         "texture and three dark flaws; boxes mark pixels more than 4σ below the local median. (b) 400 simulated flaws "
         "per sensor (ticks: hits at 1, misses at 0), contrast reduced by blur of one pixel, detection at 3.5σ; "
         "logistic hit/miss POD fit in log size (MIL-HDBK-1823A style), a90/95 = 95 % bootstrap bound on the size "
         "found 90 % of the time.", width=165)
    fig.subplots_adjust(left=0.02, right=0.985, top=0.88, bottom=0.31)
    save(fig, "ch52_ammonitor")
    print(f"   time {time.time()-t0:.1f} s")


# ==============================================================================================
# 6. CT defect classifier: ROC and cost-optimal threshold
CTS = 24


def ct_patch(r, defect, yy, xx):
    S = CTS
    img = np.ones((S, S))
    img += 0.03 * np.sin(2 * np.pi * yy / r.uniform(3, 5) + r.uniform(0, 6))       # build-layer texture
    img += r.uniform(-0.15, 0.15) * (xx - S / 2) / S                                # beam-hardening gradient
    if r.random() < 0.3:                                                              # part edge, air beyond
        ang, d = r.uniform(0, 2 * np.pi), r.uniform(4, 11)
        dist = (xx - S / 2) * np.cos(ang) + (yy - S / 2) * np.sin(ang) - d
        img *= 1 / (1 + np.exp(dist / 0.8))
    if r.random() < 0.25:                                                             # ring artefact
        cx, cy = r.uniform(-40, 60, 2)
        rad = np.hypot(xx - cx, yy - cy)
        R0 = r.uniform(rad.min() + 2, rad.max() - 2)
        img += r.choice([-1, 1]) * r.uniform(0.2, 0.5) * np.exp(-0.5 * ((rad - R0) / 0.7) ** 2)
    if r.random() < 0.15:                                                             # dark streak artefact
        th, off = r.uniform(0, np.pi), r.uniform(-8, 8)
        v = -(xx - S / 2) * np.sin(th) + (yy - S / 2) * np.cos(th) - off
        img -= r.uniform(0.2, 0.45) * np.exp(-0.5 * (v / 0.7) ** 2)
    if r.random() < 0.1:                                                              # dense inclusion (harmless)
        cx, cy = r.uniform(4, 20, 2)
        img += 0.5 * np.exp(-0.5 * ((xx - cx) ** 2 + (yy - cy) ** 2) / 0.8)
    kind = 0
    if defect:
        cx, cy = r.uniform(6, 18, 2)
        if r.random() < 0.6:                                                          # gas pore
            d, c = r.uniform(1.2, 4.5), r.uniform(0.35, 0.9)
            m = np.exp(-0.5 * ((xx - cx) ** 2 + (yy - cy) ** 2) / (d / 2.355 + 0.5) ** 2)
            kind = 1
        else:                                                                         # lack-of-fusion flaw
            L, W, th, c = r.uniform(4, 9), r.uniform(0.6, 1.2), r.uniform(0, np.pi), r.uniform(0.3, 0.7)
            u = (xx - cx) * np.cos(th) + (yy - cy) * np.sin(th)
            v = -(xx - cx) * np.sin(th) + (yy - cy) * np.cos(th)
            m = np.exp(-0.5 * (u / (L / 2.355)) ** 2 - 0.5 * (v / W) ** 2)
            kind = 2
        img -= c * m * img
    img += r.normal(0, r.uniform(0.05, 0.11), (S, S))
    return img, kind


def ct_set(n, prev, seed):
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:CTS, 0:CTS]
    X = np.zeros((n, CTS, CTS))
    y = (r.random(n) < prev).astype(int)
    k = np.zeros(n, int)
    for i in range(n):
        X[i], k[i] = ct_patch(r, y[i], yy, xx)
    return X, y, k


def inspection():
    from scipy import ndimage
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import roc_auc_score, roc_curve
    t0 = time.time()
    prev = 0.03
    Xtr, ytr, _ = ct_set(20000, 0.30, 1)
    Xva, yva, _ = ct_set(30000, prev, 2)
    Xte, yte, kte = ct_set(24000, prev, 3)

    def rule(X):
        sm = ndimage.uniform_filter(X, size=(1, 3, 3))
        med = ndimage.median_filter(X, size=(1, 7, 7))
        return -(sm - med)[:, 3:-3, 3:-3].min(axis=(1, 2))
    mu, sd = Xtr.mean(), Xtr.std()
    mlp = MLPClassifier(hidden_layer_sizes=(128, 32), alpha=1e-3, max_iter=60, early_stopping=True, random_state=0)
    mlp.fit(((Xtr - mu) / sd).reshape(len(Xtr), -1), ytr)

    def net(X):
        return mlp.predict_proba(((X - mu) / sd).reshape(len(X), -1))[:, 1]
    from sklearn.linear_model import LogisticRegression
    half = len(Xva) // 2
    sc = {}
    for nm, X in (("va", Xva), ("te", Xte)):
        pn = np.clip(net(X), 1e-6, 1 - 1e-6)
        rl = rule(X)
        sc[nm] = dict(net=pn, rule=rl, F=np.column_stack([np.log(pn / (1 - pn)), rl / 0.1]))
    stack = LogisticRegression(C=10.0, max_iter=1000).fit(sc["va"]["F"][:half], yva[:half])
    print(f"   stacking weights {stack.coef_[0]}")
    yva = yva[half:]
    scores = {"network + rule": (stack.decision_function(sc["va"]["F"][half:]), stack.decision_function(sc["te"]["F"])),
              "neural network (pixels)": (sc["va"]["net"][half:], sc["te"]["net"]),
              "local-contrast rule": (sc["va"]["rule"][half:], sc["te"]["rule"])}
    C_REV, C_ESC = 1500.0, 250000.0
    out = {}
    for name, col in (("network + rule", VIOLET), ("neural network (pixels)", ORANGE), ("local-contrast rule", GREY)):
        sv, st = scores[name]
        thr = np.unique(np.quantile(sv, np.linspace(0, 1, 2001)))
        flag = np.array([(sv >= t).mean() for t in thr])
        miss = np.array([((sv < t) & (yva == 1)).sum() / max(1, (yva == 1).sum()) for t in thr])
        cost = flag * C_REV + prev * miss * C_ESC
        tbest = thr[np.argmin(cost)]
        fl_t = (st >= tbest).mean()
        rec_t = ((st >= tbest) & (yte == 1)).sum() / (yte == 1).sum()
        fpr_t = ((st >= tbest) & (yte == 0)).sum() / (yte == 0).sum()
        cost_t = fl_t * C_REV + prev * (1 - rec_t) * C_ESC
        fpr, tpr, _ = roc_curve(yte, st)
        auc = roc_auc_score(yte, st)
        out[name] = dict(fpr=fpr, tpr=tpr, auc=auc, col=col, flag=flag, cost=cost, thr=thr, fl=fl_t, rec=rec_t,
                         fp=fpr_t, ct=cost_t, st=st)
        print(f"inspection: {name}: AUC {auc:.3f}; cost-optimal (validation) -> test flag {100*fl_t:.1f}%, "
              f"recall {100*rec_t:.1f}%, FPR {100*fpr_t:.1f}%, cost/part ${cost_t:,.0f}")
    p = out["neural network (pixels)"]["st"]
    for kk, nm in ((1, "pores"), (2, "lack of fusion")):
        print(f"   NN recall at 0.5 for {nm}: {np.mean(p[kte==kk] >= 0.5):.3f}")
    d05_rec = ((p >= 0.5) & (yte == 1)).sum() / (yte == 1).sum()
    d05_fl = (p >= 0.5).mean()
    d05_cost = d05_fl * C_REV + prev * (1 - d05_rec) * C_ESC
    print(f"   NN at default 0.5: flag {100*d05_fl:.1f}%, recall {100*d05_rec:.1f}%, cost ${d05_cost:,.0f}; "
          f"no screening ${prev*C_ESC:,.0f}; review all ${C_REV:,.0f}; prevalence test {yte.mean():.4f}")

    fig = plt.figure(figsize=(7.0, 3.3))
    gs = fig.add_gridspec(2, 5, width_ratios=[0.42, 0.42, 0.22, 1.15, 1.25], wspace=0.08, hspace=0.25,
                          left=0.01, right=0.985, top=0.91, bottom=0.34)
    gs2 = fig.add_gridspec(1, 2, width_ratios=[1, 1.05], wspace=0.42, left=0.33, right=0.985, top=0.91, bottom=0.34)
    r = np.random.default_rng(11)
    yy, xx = np.mgrid[0:CTS, 0:CTS]
    examples = [(0, "sound"), (0, "sound + ring"), (1, "pore"), (1, "lack of fusion")]
    pics = []
    rr = np.random.default_rng(5)
    while len(pics) < 4:
        want = examples[len(pics)]
        im, k = ct_patch(rr, want[0], yy, xx)
        ok = (want[1] == "sound" and k == 0) or (want[1] == "pore" and k == 1) or \
             (want[1] == "lack of fusion" and k == 2) or (want[1] == "sound + ring" and k == 0 and
                                                          np.ptp(ndimage.uniform_filter(im, 3)) > 0.75)
        if ok:
            pics.append((im, want[1]))
    for i, (im, t) in enumerate(pics):
        ax = fig.add_subplot(gs[i // 2, i % 2])
        ax.imshow(im, cmap="gray", vmin=0.2, vmax=1.4)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_title(t, fontsize=6.3, weight="normal", pad=2)
        if i == 0:
            panel_tag(ax, "(a)", x=0.15, y=1.18)
    ax = fig.add_subplot(gs2[0, 0])
    for name, o in out.items():
        ax.plot(o["fpr"], o["tpr"], color=o["col"], lw=1.5, label=f"{name.split(' (')[0]} ({o['auc']:.3f})")
        ax.plot(o["fp"], o["rec"], "o", color=o["col"], ms=5, mec="white")
    ax.plot(((p >= 0.5) & (yte == 0)).sum() / (yte == 0).sum(), d05_rec, "s", color=RED, ms=4.5, mec="white")
    ax.annotate("network,\nthreshold 0.5", xy=(((p >= 0.5) & (yte == 0)).sum() / (yte == 0).sum(), d05_rec),
                xytext=(0.0013, 0.93), fontsize=6.0, color=RED, va="top",
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
    ax.set_xscale("log")
    ax.set_xlim(1e-3, 1)
    ax.set_ylim(0, 1.02)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    ax.set_xlabel("false-alarm rate (sound parts flagged)")
    ax.set_ylabel("defects found (recall)")
    ax.legend(loc="lower right", fontsize=6.0, handlelength=1.2, title="score (ROC area)", title_fontsize=6.0)
    panel_tag(ax, "(b)")
    ax = fig.add_subplot(gs2[0, 1])
    for name, o in out.items():
        ax.plot(o["flag"] * 100, o["cost"], color=o["col"], lw=1.5)
        j = np.argmin(o["cost"])
        ax.plot(o["flag"][j] * 100, o["cost"][j], "o", color=o["col"], ms=5, mec="white")
    ax.axhline(prev * C_ESC, color=RED, ls="--", lw=0.9)
    ax.text(40, prev * C_ESC * 1.06, "no screening", fontsize=6.4, color=RED, ha="center")
    ax.axhline(C_REV, color=GREEN, ls="--", lw=0.9)
    ax.text(40, C_REV * 1.07, "expert review of every part", fontsize=6.4, color=GREEN, ha="center")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 100)
    ax.set_ylim(300, 12000)
    ax.set_yticks([300, 1000, 3000, 10000])
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:,.0f}".replace(",", " ")))
    ax.set_xlabel("parts flagged for review (%)")
    ax.set_ylabel("expected cost per part ($)")
    panel_tag(ax, "(c)")
    foot(fig, "Synthetic 24 × 24-pixel CT patches with build texture, beam hardening, part edges, ring and streak "
         "artefacts and noise; defects are pores and lack-of-fusion flaws. Network: two hidden layers (128, 32), "
         "scikit-learn, trained on 20 000 patches (30 % defective); tests on 24 000 patches at 3 % prevalence; the combined score is a logistic regression on both outputs. Costs: "
         "review \\$1 500 per flagged part, escape \\$250 000 per missed defect; dots = minimum-cost threshold chosen on a "
         "separate validation set.", width=170)
    save(fig, "ch52_inspection")
    print(f"   time {time.time()-t0:.1f} s")



# ==============================================================================================
# 7. Engine health monitoring: redline vs learned multivariate detector
NCH = 6


def _throttle(t, r):
    """Power-level profile (% of rated thrust) for a 500 s hot fire."""
    knots = np.array([0, 20, 60, 120, 200, 260, 330, 400, 460, 500])
    lv = np.r_[100, r.choice([100, 104.5, 109], 8), 80]
    lv[0] = 100
    return np.interp(t, knots, lv)


def _engine_run(r, fault=False, dt=0.5, T=500.0):
    t = np.arange(0, T, dt)
    pl = _throttle(t, r) + 0.3 * r.standard_normal(t.size)
    x = (pl - 100) / 10
    # channels: sync vibration pump A, sync vibration pump B, bearing-band vibration, broadband vibration,
    # turbine discharge temperature, pump discharge pressure (all normalised units)
    base = np.array([[1.0, 0.35, 0.10], [0.8, 0.25, 0.05], [0.25, 0.04, 0.0], [1.2, 0.30, 0.08],
                     [1.0, 0.20, 0.02], [1.0, 0.45, 0.00]])
    mean = base[:, 0][:, None] + base[:, 1][:, None] * x + base[:, 2][:, None] * x ** 2
    common = np.cumsum(r.standard_normal(t.size)) * 0.004
    common -= np.convolve(common, np.ones(81) / 81, mode="same")
    noise = np.array([0.04, 0.035, 0.012, 0.05, 0.01, 0.008])[:, None] * r.standard_normal((NCH, t.size))
    Y = mean * (1 + common) + noise
    run_off = r.normal(0, 1, NCH) * np.array([0.05, 0.05, 0.015, 0.05, 0.01, 0.008])
    Y += run_off[:, None]
    if r.random() < 0.08:                                   # brief sensor glitch
        j, i0 = r.integers(0, NCH), r.integers(0, t.size - 6)
        Y[j, i0:i0 + 4] += r.choice([-1, 1]) * r.uniform(5, 12) * noise[j].std()
    t_on, t_fail = None, None
    if fault:
        t_on = r.uniform(120, 360)
        tau = r.uniform(8, 50)
        g = np.where(t > t_on, np.exp((t - t_on) / tau) - 1, 0.0)
        amp = 0.012 * g                                     # growth of the bearing-band level
        Y[2] += amp
        Y[3] += 0.8 * amp
        Y[0] += 0.3 * amp
        Y[4] += 0.02 * amp
        t_fail = t_on + tau * np.log(1 + 1.0 / 0.012)       # bearing band 1.0 above normal = failure
        keep = t <= t_fail
        t, pl, Y = t[keep], pl[keep], Y[:, keep]
    return t, pl, Y, t_on, t_fail


def _overall(Y):
    return np.sqrt(Y[0] ** 2 + Y[1] ** 2 + Y[2] ** 2 + Y[3] ** 2)


def engine():
    t0 = time.time()
    r = np.random.default_rng(21)
    train = [_engine_run(r) for _ in range(40)]
    # learned model of normal behaviour: per-channel quadratic in power level, residual covariance
    P = np.concatenate([tr[1] for tr in train])
    Y = np.concatenate([tr[2] for tr in train], axis=1)
    Xd = np.column_stack([np.ones_like(P), (P - 100) / 10, ((P - 100) / 10) ** 2])
    W, *_ = np.linalg.lstsq(Xd, Y.T, rcond=None)
    Res = Y.T - Xd @ W
    Ci = np.linalg.inv(np.cov(Res.T))

    def score(pl, Yr, lam=0.05):
        Xr = np.column_stack([np.ones_like(pl), (pl - 100) / 10, ((pl - 100) / 10) ** 2])
        e = Yr.T - Xr @ W
        d2 = np.einsum("ij,jk,ik->i", e, Ci, e)
        out = np.empty_like(d2)
        acc = NCH
        for i, v in enumerate(d2):
            acc = (1 - lam) * acc + lam * v
            out[i] = acc
        return out
    redline = 1.08 * max(_overall(tr[2]).max() for tr in train)
    val = [_engine_run(r) for _ in range(200)]
    thr = np.percentile([score(v[1], v[2]).max() for v in val], 99.5) * 1.05
    nom = [_engine_run(r) for _ in range(300)]
    fa_learn = np.mean([score(v[1], v[2]).max() > thr for v in nom])
    fa_red = np.mean([_overall(v[2]).max() > redline for v in nom])
    bad = [_engine_run(r, fault=True) for _ in range(300)]
    lead_l, lead_r = [], []
    for t, pl, Yb, ton, tf in bad:
        sc = score(pl, Yb)
        il = np.argmax(sc > thr) if (sc > thr).any() else None
        ov = _overall(Yb)
        ir = np.argmax(ov > redline) if (ov > redline).any() else None
        lead_l.append(tf - t[il] if il is not None else 0.0)
        lead_r.append(tf - t[ir] if ir is not None else 0.0)
    lead_l, lead_r = np.array(lead_l), np.array(lead_r)
    print(f"engine: redline {redline:.3f}; learned threshold {thr:.1f}; false alarms on 300 nominal runs: learned "
          f"{100*fa_learn:.1f}%, redline {100*fa_red:.1f}%; median warning before failure: learned "
          f"{np.median(lead_l):.0f} s, redline {np.median(lead_r):.0f} s; caught >=10 s before failure: learned "
          f"{100*np.mean(lead_l>=10):.0f}%, redline {100*np.mean(lead_r>=10):.0f}%; no warning: learned "
          f"{100*np.mean(lead_l<=0):.0f}%, redline {100*np.mean(lead_r<=0):.0f}%")
    # example run
    rr = np.random.default_rng(5)
    while True:
        t, pl, Yb, ton, tf = _engine_run(rr, fault=True)
        sc_ = score(pl, Yb)
        if 150 < ton < 280 and (sc_ > thr).any() and 45 < tf - t[np.argmax(sc_ > thr)] < 70:
            break
    sc = score(pl, Yb)
    ov = _overall(Yb)
    il, ir = np.argmax(sc > thr), np.argmax(ov > redline)
    print(f"   example: fault starts {ton:.0f} s, failure {tf:.0f} s, learned alarm {t[il]:.0f} s, redline "
          f"{t[ir]:.0f} s")
    fig = plt.figure(figsize=(7.0, 3.3))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1], hspace=0.12, wspace=0.28, left=0.075, right=0.985,
                          top=0.93, bottom=0.32)
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(t, ov, color=BLUE, lw=0.8, label="overall vibration")
    ax.axhline(redline, color=RED, ls="--", lw=1.0)
    ax.text(5, redline * 1.01, "fixed redline", color=RED, fontsize=6.4, va="bottom")
    ax.plot(t, Yb[2] * 4 + 0.6, color=GREEN, lw=0.8, label="bearing band (× 4, offset)")
    ax.axvline(ton, color=GREY, lw=0.8, ls=":")
    ax.axvline(tf, color=INK, lw=1.0)
    ax.text(ton - 3, 0.62, "fault starts", fontsize=6.0, color=GREY, va="bottom", ha="right")
    ax.set_xticklabels([])
    ax.set_ylabel("level")
    ax.set_xlim(0, t[-1] + 10)
    ax.legend(loc="upper left", fontsize=6.2, ncol=2, handlelength=1.2)
    panel_tag(ax, "(a)")
    ax = fig.add_subplot(gs[1, 0])
    ax.semilogy(t, sc, color=ORANGE, lw=0.9)
    ax.axhline(thr, color=ORANGE, ls="--", lw=0.9)
    ax.axvline(t[il], color=ORANGE, lw=0.8)
    ax.axvline(t[ir], color=RED, lw=0.8)
    ax.axvline(tf, color=INK, lw=1.0)
    ax.text(t[il] - 3, thr * 3, f"learned alarm\n{tf - t[il]:.0f} s early", fontsize=6.0, color=ORANGE, ha="right",
            va="bottom")
    ax.set_xlabel("time from ignition (s)")
    ax.set_ylabel("anomaly score")
    panel_tag(ax, "(b)")
    ax.set_xlim(0, t[-1] + 10)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    ax = fig.add_subplot(gs[:, 1])
    bins = np.linspace(0, 200, 21)
    ax.hist(np.minimum(lead_l, 199), bins=bins, color=ORANGE, alpha=0.75,
            label=f"learned detector ({100*fa_learn:.1f} % false alarms)")
    ax.hist(np.minimum(lead_r, 199), bins=bins, color=RED, alpha=0.5, histtype="stepfilled",
            label=f"fixed redline ({100*fa_red:.1f} % false alarms)")
    ax.set_xlabel("warning time before failure (s)")
    ax.set_ylabel("faulty runs (of 300)")
    ax.legend(loc="upper right", fontsize=6.2)
    panel_tag(ax, "(c)")
    foot(fig, "Synthetic 500 s hot fires with throttle changes between 80 % and 109 % power level; six channels (two "
         "synchronous vibration levels, bearing-band and broadband vibration, temperature, pressure). Learned "
         "detector: quadratic model of each channel against power level fitted on 40 normal runs, Mahalanobis "
         "distance of the residuals, smoothed (EWMA), threshold set on 200 validation runs. Black line: failure. Faults: bearing wear "
         "growing exponentially (time constant 8–50 s); 8 % of runs contain a brief sensor glitch.", width=170)
    save(fig, "ch52_engine")
    print(f"   time {time.time()-t0:.1f} s")


# ==============================================================================================
# 8. Launch failure rates (GCAT) and a Bayesian model for a new vehicle
def launchrisk():
    from scipy.stats import beta
    g = json.load(open(ROOT / "data" / "gcat_stats.json"))
    yrs = np.arange(1997, 2026)
    n = np.array([g["launches_by_year"][str(y)]["_all"] for y in yrs])
    k = np.array([g["failures_by_year"][str(y)] for y in yrs])
    lo, hi = beta.ppf(0.05, k + 0.5, n - k + 0.5), beta.ppf(0.95, k + 0.5, n - k + 0.5)
    m16 = (yrs >= 2016)
    rate16 = k[m16].sum() / n[m16].sum()
    m97 = (yrs <= 2006)
    print(f"launchrisk: 2016-2025 failures {k[m16].sum()}/{n[m16].sum()} = {100*rate16:.2f}%; 1997-2006 "
          f"{k[m97].sum()}/{n[m97].sum()} = {100*k[m97].sum()/n[m97].sum():.2f}%; 2025 {k[-1]}/{n[-1]} = "
          f"{100*k[-1]/n[-1]:.1f}%")
    a0, b0 = 0.9, 1.1
    ns = np.arange(0, 41)
    pm = a0 / (a0 + b0 + ns)
    plo, phi = beta.ppf(0.05, a0, b0 + ns), beta.ppf(0.95, a0, b0 + ns)
    for q in (0, 1, 2, 5, 10, 20, 40):
        print(f"   after {q} successes: mean {100*pm[q]:.1f}%  90% interval {100*plo[q]:.1f}-{100*phi[q]:.1f}%")
    # with one failure in the first 3 flights then successes
    pm_f = (a0 + 1) / (a0 + b0 + 3 + ns)
    print(f"   if 1 failure in first 3 flights, after 10 more successes: {100*pm_f[10]:.1f}%")
    n_to5 = int(np.argmax(pm <= 0.05))
    print(f"   successes needed for posterior mean <= 5%: {n_to5}; to reach mature rate {100*rate16:.1f}%: "
          f"{int(np.argmax(pm <= rate16))}")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.75), gridspec_kw=dict(width_ratios=[1.25, 1], wspace=0.58))
    ax = axs[0]
    axb = ax.twinx()
    axb.bar(yrs, n, color=LIGHT, width=0.8, zorder=0)
    axb.set_ylabel("orbital launch attempts", color=GREY)
    axb.tick_params(axis="y", colors=GREY)
    axb.spines["right"].set_visible(True)
    axb.grid(False)
    ax.set_zorder(axb.get_zorder() + 1)
    ax.patch.set_visible(False)
    ax.errorbar(yrs, 100 * k / n, yerr=[100 * (k / n - lo), 100 * (hi - k / n)], fmt="o", color=RED, ms=3,
                lw=0.8, capsize=0)
    ax.axhline(100 * rate16, xmin=(2015.5 - 1996) / 30, color=NAVY, lw=1.0, ls="--")
    ax.text(2006, 14.6, f"dashed line: 2016–25 average, {100*rate16:.1f} %", fontsize=6.4, color=NAVY, ha="center")
    ax.set_ylabel("failure rate (%), 90 % interval", color=RED)
    ax.set_xlim(1996, 2026)
    ax.set_ylim(0, 16)
    panel_tag(ax, "(a)")
    ax = axs[1]
    ax.fill_between(ns, 100 * plo, 100 * phi, color=SKY, alpha=0.35, lw=0, label="90 % credible interval")
    ax.plot(ns, 100 * pm, color=BLUE, lw=1.6, label="posterior mean")
    ax.plot([0, 1], [45, 30], "s", color=ORANGE, ms=4.5, label="observed: 1st, 2nd flights")
    ax.axhline(100 * rate16, color=NAVY, ls="--", lw=0.9)
    ax.text(40, 100 * rate16 + 1.2, "mature fleet", fontsize=6.4, color=NAVY, ha="right")
    ax.set_xlabel("consecutive successful flights")
    ax.set_ylabel("failure probability, next flight (%)")
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right", fontsize=6.4)
    panel_tag(ax, "(b)")
    foot(fig, "(a) Orbital launch attempts and failures by year from GCAT (J. McDowell, updated 13 October 2026); "
         "intervals from Jeffreys priors. (b) Beta(0.9, 1.1) prior with a mean of 45 %, the reported maiden-flight "
         "failure rate (Seradata); orange squares are the reported first- and second-flight failure rates since 1990.",
         width=165)
    fig.subplots_adjust(left=0.08, right=0.985, top=0.93, bottom=0.27)
    save(fig, "ch52_launchrisk")


# ==============================================================================================
# 9. Satellites in view versus latitude, and constellation sizing by linear programming
def _in_view(inc_deg, lats_deg, h=550.0, el_min=25.0, n=400000, seed=0):
    r = np.random.default_rng(seed)
    Re = 6371.0
    lam = np.arccos(Re * np.cos(np.radians(el_min)) / (Re + h)) - np.radians(el_min)
    u = r.uniform(0, 2 * np.pi, n)
    raan = r.uniform(0, 2 * np.pi, n)
    i = np.radians(inc_deg)
    sx = np.cos(raan) * np.cos(u) - np.sin(raan) * np.sin(u) * np.cos(i)
    sy = np.sin(raan) * np.cos(u) + np.cos(raan) * np.sin(u) * np.cos(i)
    sz = np.sin(u) * np.sin(i)
    out = []
    for la in np.radians(lats_deg):
        ux, uz = np.cos(la), np.sin(la)
        out.append(np.mean(sx * ux + sz * uz >= np.cos(lam)))
    return np.array(out), np.degrees(lam)


def capacity():
    from scipy.optimize import linprog
    t0 = time.time()
    lats = np.arange(0, 81, 1.0)
    incs = [33, 43, 53, 70, 97.6]
    cols = [SKY, GREEN, ORANGE, VIOLET, NAVY]
    G = {}
    for j, inc in enumerate(incs):
        G[inc], lam = _in_view(inc, lats, seed=j)
    print(f"capacity: footprint radius {lam:.2f} deg (550 km, 25 deg elevation)")
    for inc in incs:
        gi = G[inc] * 1000
        print(f"   i={inc}: per 1000 sats in view at 0/25/40/50/60/75 deg: " +
              "/".join(f"{gi[int(x)]:.2f}" for x in (0, 25, 40, 50, 60, 75)))
    # requirement profile: users mostly at 25-50 deg
    req = np.where(lats <= 60, 4.0, np.where(lats <= 75, 2.0, 0.0))
    req = np.where((lats >= 25) & (lats <= 50), 12.0, req)
    A = -np.array([G[i] for i in incs]).T
    sol = linprog(np.ones(len(incs)), A_ub=A, b_ub=-req, bounds=[(0, None)] * len(incs), method="highs")
    N = sol.x
    print("   LP mix:", dict(zip(incs, np.round(N).astype(int))), "total", int(round(N.sum())))
    singles = {}
    for inc in (53, 97.6):
        g = G[inc]
        need = np.max(np.where(req > 0, req / np.maximum(g, 1e-12), 0))
        singles[inc] = need
        print(f"   single shell {inc}: needs {need:,.0f} satellites" + ("" if g[75] > 0 else " (cannot reach 75 deg)"))
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.8), gridspec_kw=dict(width_ratios=[1, 1.15], wspace=0.3))
    ax = axs[0]
    for inc, c in zip(incs, cols):
        ax.plot(lats, G[inc] * 1000, color=c, lw=1.5, label=f"{inc:g}°")
    ax.set_xlabel("user latitude (°)")
    ax.set_ylabel("satellites in view per 1 000")
    ax.set_xlim(0, 80)
    ax.set_ylim(0, None)
    ax.legend(title="inclination", fontsize=6.4, title_fontsize=6.4, loc="upper left", ncol=2,
              columnspacing=0.8, handlelength=1.2)
    panel_tag(ax, "(a)")
    ax = axs[1]
    bottom = np.zeros_like(lats)
    for inc, c, nn in zip(incs, cols, N):
        if nn < 1:
            continue
        y = G[inc] * nn
        ax.fill_between(lats, bottom, bottom + y, color=c, alpha=0.85, lw=0, label=f"{inc:g}°: {nn:,.0f}".replace(",", " "))
        bottom = bottom + y
    ax.step(lats, req, where="mid", color=RED, lw=1.4, label="requirement")
    ax.set_xlabel("user latitude (°)")
    ax.set_ylabel("satellites in view")
    ax.set_xlim(0, 80)
    ax.set_ylim(0, max(bottom.max(), req.max()) * 1.15)
    ax.legend(fontsize=6.2, loc="upper right", title=f"optimal mix, {N.sum():,.0f} satellites".replace(",", " "),
              title_fontsize=6.4)
    panel_tag(ax, "(b)")
    foot(fig, "Circular shells at 550 km with satellites spread evenly in orbit position and node (Monte Carlo); "
         "a satellite is in view above 25° elevation. (b) Linear programme: choose the number of satellites in each "
         "shell to minimise the total while meeting an illustrative requirement of 12 satellites in view at 25–50° "
         "latitude, 4 elsewhere up to 60° and 2 up to 75°.", width=165)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.93, bottom=0.31)
    save(fig, "ch52_capacity")
    print(f"   time {time.time()-t0:.1f} s")


if __name__ == "__main__":
    fns = [pipeline, topopt, bayesopt, production, ammonitor, inspection, engine, launchrisk, capacity]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
