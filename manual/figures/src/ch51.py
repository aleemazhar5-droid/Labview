"""Figures for Chapter 51 - AI for Space Science, Planetary Exploration and Human Spaceflight.

Most figures run real search, optimisation or machine-learning code with fixed random seeds on synthetic data built
from simple physical models:
  alerts     - block diagram: from a survey telescope to alerts, brokers, follow-up and feedback (diagram)
  funnel     - discovery funnels from published numbers: Kepler DR25, ExoMiner, ExoMiner++, Euclid Q1 lenses (data)
  transit    - simulated Kepler-like light curve, detrending and a box-least-squares (BLS) period search
  vetting    - numpy neural network vs a rule-based vetter on synthetic phase-folded transit signals
  photoz     - random-forest photometric redshifts from synthetic six-band galaxy colours; training-set bias
  transients - random-forest classification of synthetic multi-band transient light curves; early classification
  craters    - crater size-frequency distribution with a synthetic detector, completeness correction and a
               maximum-likelihood model age (Neukum production and chronology functions)
  unmixing   - linear spectral unmixing (fully constrained least squares) and blind NMF on synthetic spectra
  delay      - Earth-Mars light-time from orbital elements and the response time of ground support
  eclss      - predictive maintenance of synthetic life-support fans with gradient-boosted trees
Numbers quoted in the chapter are printed by each function.
"""
import os
import sys
import textwrap
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch  # noqa: F401
from matplotlib.lines import Line2D  # noqa: F401
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker

FOOT = 6.0


def panel_tag(ax, s, x=-0.02, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, weight="bold", ha="right", va="bottom", color=INK)


def foot(fig, text, y=0.01, width=165):
    fig.text(0.99, y, "\n".join(textwrap.wrap(text, width)), ha="right", va="bottom", fontsize=FOOT, color=GREY,
             multialignment="right", linespacing=1.25)


# ==============================================================================================
# 1. Block diagram: survey -> alerts -> brokers -> follow-up, with feedback
def alerts():
    fig, ax = canvas(7.0, 3.55, xlim=(0, 140), ylim=(0, 71))
    # top row: observatory
    label(ax, 2, 68.5, "OBSERVATORY (automatic, about 60 s per image)", fs=7.2, color=NAVY, ha="left", weight="bold")
    top = [
        (2, "Telescope and camera", "3.2 gigapixels\nevery ~40 s\n~10 TB per night"),
        (36, "Difference imaging", "calibrate, align,\nsubtract a deep\ntemplate image"),
        (70, "Real/bogus filter", "network rejects\nartefacts, cosmic\nrays, bad subtractions"),
        (104, "Alert packets", "≤ 82 KB each, within\n60 s; up to 7–10 million\nper night"),
    ]
    for x, t, b in top:
        title_box(ax, x, 41, 31, 25, t, b, fs=6.7, tfs=7.4)
    for i in range(3):
        arrow(ax, (top[i][0] + 31.3, 52), (top[i + 1][0] - 0.3, 52), lw=1.3)
    # bottom row: community
    label(ax, 2, 2.2, "COMMUNITY (machine learning ranks, people decide)", fs=7.2, color=ORANGE, ha="left",
          weight="bold")
    bot = [
        (104, "Brokers (7)", "cross-match catalogues;\nclassify with forests,\nCNNs, RNNs", ORANGE),
        (70, "Filters and ranking", "each team asks for\n'young SN Ia', 'kilonova',\n'new NEO' ..."),
        (36, "Follow-up", "spectra, other bands,\nother telescopes:\ntens to hundreds a night"),
        (2, "Labels and catalogues", "confirmed classes\nretrain the models\n(active learning)"),
    ]
    for item in bot:
        x, t, b = item[:3]
        hc = item[3] if len(item) > 3 else NAVY
        title_box(ax, x, 6.5, 31, 24.5, t, b, fs=6.7, tfs=7.4, hc=hc, ec=hc)
    arrow(ax, (119.5, 40.6), (119.5, 31.4), lw=1.3)
    for i in range(3):
        arrow(ax, (bot[i][0] - 0.3, 18.5), (bot[i + 1][0] + 31.3, 18.5), lw=1.3)
    # feedback loop
    arrow(ax, (12, 31.4), (12, 40.6), color=GREEN, lw=1.3, ls="--")
    arrow(ax, (30, 31.4), (78, 40.6), color=GREEN, lw=1.1, ls="--", rad=-0.12)
    label(ax, 14, 36.0, "retrained models", fs=6.5, color=GREEN, ha="left", bg="white")
    label(ax, 52, 36.6, "better training sets", fs=6.5, color=GREEN, ha="left", bg="white")
    label(ax, 121, 36.0, "stream", fs=6.5, color=NAVY, ha="left")
    save(fig, "ch51_alerts")


# ==============================================================================================
# 2. Discovery funnels from published numbers
def funnel():
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.9), gridspec_kw=dict(width_ratios=[1.15, 1, 1]))
    sets = [
        ("Kepler DR25 + ExoMiner", [("Stars searched", 198709), ("Threshold crossings", 34032),
                                    ("Objects of interest", 8054), ("Planet candidates", 4034),
                                    ("ExoMiner score > 0.99", 368), ("Newly validated", 301)], BLUE),
        ("TESS + ExoMiner++", [("2-min threshold\ncrossings", 147568), ("Planet candidates", 7330),
                               ("Existing TOIs", 1868), ("New community\nTOIs", 50)], VIOLET),
        ("Euclid Q1 lens search", [("Lens candidates\n(grade A + B)", 497), ("Grade A", 250),
                                   ("Grade A, new", 243)], GREEN),
    ]
    for k, (ax, (title, rows, col)) in enumerate(zip(axs, sets)):
        names = [r[0] for r in rows][::-1]
        vals = [r[1] for r in rows][::-1]
        y = np.arange(len(vals))
        ax.barh(y, vals, color=col, alpha=0.85, height=0.62)
        ax.set_xscale("log")
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=6.6)
        ax.set_xlim(10, 2e6 if k < 2 else 3e4)
        for yy, v in zip(y, vals):
            ax.text(v * 1.25, yy, f"{v:,}".replace(",", " "), va="center", fontsize=6.4, color=INK)
        ax.set_title(title, fontsize=8)
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="x", labelsize=6.8)
        panel_tag(ax, "abc"[k], x=-0.02 if k else -0.05)
    foot(fig, "Sources: Kepler DR25 catalogue (Thompson et al. 2018; 198 709 stars searched, 34 032 TCEs); "
              "ExoMiner (Valizadegan et al. 2022, 1 922 unlabelled KOIs scored); ExoMiner++ (Valizadegan et al. 2025); "
              "Euclid Q1 strong-lensing discovery engine (Euclid Collaboration 2025/26, 63 deg²).")
    fig.tight_layout(rect=(0, 0.08, 1, 1), w_pad=0.6)
    save(fig, "ch51_funnel")


# ==============================================================================================
# 3. Transit light curve and box-least-squares search
RSUN_REARTH = 109.2


def transit_model(t, P, t0, depth, dur):
    ph = ((t - t0 + 0.5 * P) % P) - 0.5 * P
    x = np.abs(ph) / (0.5 * dur)
    f = np.zeros_like(t)
    inside = x < 1
    # limb-darkened, slightly rounded bottom (quadratic law approximation) with short ingress
    mu = np.sqrt(np.clip(1 - x[inside] ** 2, 0, 1))
    shape = (1 - 0.45 * (1 - mu) - 0.2 * (1 - mu) ** 2) / (1 - 0.0)
    edge = np.clip((1 - x[inside]) / 0.08, 0, 1)
    f[inside] = -depth * shape * edge / 0.93
    return f


def bls(t, y, periods, qs, nb=800):
    """Box least squares: for each trial period fold, bin and scan boxes of duration q*P. Returns SNR spectrum."""
    w = np.ones_like(y)
    best = np.zeros(len(periods))
    info = []
    sig = np.std(y)
    for i, P in enumerate(periods):
        ph = (t % P) / P
        b = np.minimum((ph * nb).astype(int), nb - 1)
        s = np.bincount(b, weights=y, minlength=nb)
        n = np.bincount(b, weights=w, minlength=nb)
        s2 = np.concatenate([s, s])
        n2 = np.concatenate([n, n])
        cs, cn = np.concatenate([[0], np.cumsum(s2)]), np.concatenate([[0], np.cumsum(n2)])
        bb = 0
        bi = None
        for q in qs:
            k = max(1, int(round(q * nb)))
            ss = cs[k:k + nb] - cs[:nb]
            nn = cn[k:k + nb] - cn[:nb]
            dep = -ss / np.maximum(nn, 1)
            snr = dep * np.sqrt(nn) / sig
            j = np.argmax(snr)
            if snr[j] > bb:
                bb, bi = snr[j], (j, k, dep[j])
        best[i] = bb
        info.append(bi)
    return best, info


def transit():
    rng = np.random.default_rng(51)
    days = 730.0
    cad = 0.5 / 24
    t = np.arange(0, days, cad)
    # quarterly data gaps (downlinks) and random missing points
    keep = np.ones_like(t, bool)
    for g in np.arange(90, days, 90):
        keep &= ~((t > g) & (t < g + 1.5))
    keep &= rng.random(len(t)) > 0.02
    t = t[keep]
    # star: Sun-like, rotation 25 d, spot modulation 0.6 ppt; white noise 250 ppm per 30-min point
    P_true, t0_true = 17.63, 5.21
    Rp = 1.3
    depth_true = (Rp / RSUN_REARTH) ** 2
    a_au = (P_true / 365.25) ** (2 / 3)
    dur = P_true / np.pi * (0.00465 / a_au)
    var = 6e-4 * (np.sin(2 * np.pi * t / 25.1 + 0.4) * (1 + 0.4 * np.sin(2 * np.pi * t / 160)) +
                  0.35 * np.sin(4 * np.pi * t / 25.1 + 1.3))
    noise = 250e-6 * rng.standard_normal(len(t))
    flux = 1 + var + transit_model(t, P_true, t0_true, depth_true, dur) + noise
    # detrend: running median over 1 day (masked iteratively is unnecessary for a shallow transit)
    from scipy.ndimage import median_filter
    w = int(round(2.0 / cad)) | 1
    trend = median_filter(flux, size=w, mode="nearest")
    y = flux / trend - 1
    periods = np.exp(np.linspace(np.log(1.0), np.log(60.0), 40000))
    qs = [0.003, 0.005, 0.008, 0.011, 0.015, 0.02, 0.03]
    snr, info = bls(t, y, periods, qs)
    # remove slow trend of the SNR spectrum (normalise by running median, as in BLS 'SDE')
    base = median_filter(snr, size=401, mode="nearest")
    sde = (snr - base)
    i = int(np.argmax(snr))
    Pbest = periods[i]
    j, k, dep = info[i]
    t0_best = (j + 0.5 * k) / 800 * Pbest
    nt = int(np.sum([(np.abs(((t - t0_true + 0.5 * P_true) % P_true) - 0.5 * P_true) < dur / 2).any()]))
    ntr = len(np.unique(np.round((t[np.abs(((t - t0_true + 0.5 * P_true) % P_true) - 0.5 * P_true) < dur / 2]
                                  - t0_true) / P_true)))
    print(f"transit: std of detrended flux {np.std(y)*1e6:.0f} ppm")
    print(f"transit: true P={P_true} d depth={depth_true*1e6:.0f} ppm dur={dur*24:.2f} h; transits observed={ntr}")
    print(f"transit: BLS best P={Pbest:.3f} d, SNR={snr[i]:.1f}, box depth={dep*1e6:.0f} ppm, "
          f"box duration={k/800*Pbest*24:.2f} h; next highest peak outside 1% of P: "
          f"{np.max(snr[(np.abs(periods/Pbest-1)>0.01) & (np.abs(periods/(Pbest/2)-1)>0.01) & (np.abs(periods/(2*Pbest)-1)>0.01)]):.1f}")
    # expected SNR from simple formula
    npts = dur / cad
    print(f"transit: expected SNR = depth/sigma*sqrt(N_in) = {depth_true/250e-6*np.sqrt(npts*ntr*0.98):.1f}")

    fig = plt.figure(figsize=(7.0, 4.4))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1.2], width_ratios=[1.35, 1], hspace=0.8, wspace=0.28)
    ax = fig.add_subplot(gs[0, :])
    ax.plot(t, (flux - 1) * 1e3, ".", ms=0.6, color=GREY, rasterized=True)
    ax.plot(t, (trend - 1) * 1e3, "-", lw=0.8, color=ORANGE)
    intr = np.abs(((t - t0_true + 0.5 * P_true) % P_true) - 0.5 * P_true) < dur / 2
    ax.plot(t[intr], (flux[intr] - 1) * 1e3, ".", ms=1.2, color=RED, rasterized=True)
    ax.set_xlim(0, days)
    ax.set_ylabel("Flux − 1 (ppt)")
    ax.set_xlabel("Time (days)", labelpad=0, fontsize=7)
    ax.set_title("Two years of simulated photometry: spots, noise and a hidden 1.3 Earth-radius planet", fontsize=8.4)
    panel_tag(ax, "a", x=-0.035)
    ax2 = fig.add_subplot(gs[1, :])
    ax2.plot(periods, snr, lw=0.6, color=BLUE)
    ax2.set_xscale("log")
    ax2.set_xlim(1, 60)
    ax2.set_xticks([1, 2, 5, 10, 20, 50])
    ax2.set_xticklabels(["1", "2", "5", "10", "20", "50"])
    ax2.set_xlabel("Trial period (days)", labelpad=1)
    ax2.set_ylabel("BLS SNR")
    ax2.axhline(7.1, color=RED, lw=0.8, ls="--")
    ax2.text(1.05, 7.6, "7.1σ threshold", color=RED, fontsize=6.6)
    ax2.annotate(f"P = {Pbest:.2f} d", (Pbest, snr[i]), (Pbest * 1.35, snr[i] * 0.92), fontsize=7, color=INK,
                 arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    for m, lab in [(0.5, "P/2"), (2, "2P")]:
        jj = np.argmin(np.abs(periods - Pbest * m))
        ax2.text(periods[jj], snr[jj] + 0.6, lab, fontsize=6.4, color=GREY, ha="center")
    ax2.set_title("Box-least-squares search over 40 000 trial periods", fontsize=8.4)
    panel_tag(ax2, "b", x=-0.035)
    ax3 = fig.add_subplot(gs[2, 0])
    ph = ((t - t0_best + 0.5 * Pbest) % Pbest) - 0.5 * Pbest
    m = np.abs(ph) < 0.6
    ax3.plot(ph[m] * 24, y[m] * 1e6, ".", ms=1.0, color=GREY, alpha=0.5, rasterized=True)
    edges = np.linspace(-0.6, 0.6, 49)
    cen = 0.5 * (edges[1:] + edges[:-1])
    idx = np.digitize(ph[m], edges) - 1
    bm = np.array([np.mean(y[m][idx == q]) for q in range(len(cen))])
    be = np.array([np.std(y[m][idx == q]) / np.sqrt(max(1, np.sum(idx == q))) for q in range(len(cen))])
    ax3.errorbar(cen * 24, bm * 1e6, be * 1e6, fmt="o", ms=2.6, color=NAVY, lw=0.7, capsize=0)
    tt = np.linspace(-0.6, 0.6, 600)
    ax3.plot(tt * 24, transit_model(tt + t0_true, P_true, t0_true, depth_true, dur) * 1e6, color=RED, lw=1.1)
    ax3.set_xlim(-14, 14)
    ax3.set_ylim(-420, 300)
    ax3.set_xlabel("Hours from mid-transit", labelpad=1)
    ax3.set_ylabel("Detrended flux (ppm)")
    ax3.set_title(f"Folded at {Pbest:.2f} d: depth ≈ {dep*1e6:.0f} ppm", fontsize=8.4)
    panel_tag(ax3, "c", x=-0.07)
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis("off")
    txt = (f"Injected:  P = {P_true} d, depth {depth_true*1e6:.0f} ppm,\n"
           f"   {dur*24:.1f} h, {ntr} transits\n"
           f"Recovered:  P = {Pbest:.3f} d,\n"
           f"   box depth {dep*1e6:.0f} ppm, SNR {snr[i]:.1f}\n"
           f"Noise: 250 ppm per 30-min point;\n"
           f"   one transit has SNR ≈ {depth_true/250e-6*np.sqrt(npts):.1f}")
    ax4.text(0.02, 1.0, txt, transform=ax4.transAxes, va="top", fontsize=6.8, color=INK, linespacing=1.4)
    foot(fig, "Simulation: 730 days at 30-min cadence with gaps; starspot modulation (25-day rotation, ~0.6 ppt), white "
              "noise 250 ppm per point; limb-darkened transit of a 1.3 R⊕ planet on a Sun-like star. Detrending by a 2-day "
              "running median; BLS with seven box durations and 800 phase bins per trial period. Seed 51.", y=0.0)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.15)
    save(fig, "ch51_transit")


# ==============================================================================================
# 4. Vetting: numpy neural network vs rule-based vetter on synthetic folded signals
NG, NL = 201, 61


def make_views(rng, n):
    """Synthetic global (full orbit) and local (around transit) views. Classes: 0 planet, 1 EB, 2 artefact."""
    cls = rng.choice(3, n, p=[0.4, 0.35, 0.25])
    snr = np.exp(rng.uniform(np.log(6), np.log(40), n))
    xg = np.linspace(-0.5, 0.5, NG)
    G = np.zeros((n, NG))
    L = np.zeros((n, NL))
    meta = np.zeros((n, 3))
    for i in range(n):
        w = np.exp(rng.uniform(np.log(0.012), np.log(0.06)))   # duration as fraction of period
        xl = np.linspace(-2.5 * w, 2.5 * w, NL)
        c = cls[i]
        sec = 0.0
        if c == 0:
            # U-shaped transit; 15 % grazing (V-like) planets
            ing = rng.uniform(0.05, 0.25) if rng.random() > 0.1 else rng.uniform(0.6, 1.0)
            prof = lambda x, ing=ing: trap(x, w, ing) * (0.85 + 0.15 * np.sqrt(np.clip(1 - (2 * x / w) ** 2, 0, 1)))
            oe = 0.0
        elif c == 1:
            kind = rng.choice(3, p=[0.55, 0.15, 0.3])
            if kind == 0:     # V-shaped eclipse with a clear secondary
                ing, sec = rng.uniform(0.55, 1.0), rng.uniform(0.1, 0.6)
            elif kind == 1:   # diluted background binary: U-like, weak secondary
                ing, sec = rng.uniform(0.15, 0.5), rng.uniform(0.05, 0.3)
            else:             # V-shaped, eccentric orbit hides the secondary
                ing, sec = rng.uniform(0.55, 1.0), 0.0
            prof = lambda x, ing=ing: trap(x, w, ing)
            oe = rng.choice([0.0, rng.uniform(0.1, 0.4)], p=[0.5, 0.5])
        else:
            kind = rng.integers(3)
            if kind == 0:   # asymmetric dropout with exponential recovery (sensor artefact)
                prof = lambda x: np.where(x > -w / 2, np.exp(-np.clip(x + w / 2, 0, None) / (0.6 * w)), 0) * \
                    (x < 3 * w)
            elif kind == 1:  # sinusoid-like variability caught by the search
                ph0 = rng.uniform(0, 2 * np.pi)
                prof = lambda x, ph0=ph0: 0.5 * (1 + np.cos(2 * np.pi * x / (6 * w))) * (np.abs(x) < 3 * w) + \
                    0.25 * np.cos(2 * np.pi * x * 2 + ph0)
            else:            # single-event outlier: narrow spike plus noise-like wiggle
                prof = lambda x: np.exp(-0.5 * (x / (0.15 * w)) ** 2)
            oe = 0.0
        # noise per global bin chosen so that the in-transit SNR equals snr
        nin = max(1.0, w * NG)
        sig = 1.0 / (snr[i] / np.sqrt(nin))
        g = -prof(xg) - sec * prof(np.where(np.abs(xg) > 0.25, xg - np.sign(xg) * 0.5, 9))
        if c == 1 and oe > 0:
            g = g * (1 - 0.5 * oe)
        G[i] = g + sig * rng.standard_normal(NG)
        sigl = sig * np.sqrt(NG * 5 * w / NL)
        # odd/even depth difference shows up as extra scatter in the local view of the deeper events
        loc = -prof(xl) * (1 + (oe * rng.choice([-1, 1]) if c == 1 else 0) * 0.5)
        L[i] = loc + sigl * rng.standard_normal(NL)
        meta[i] = (snr[i], w, sec)
    # normalise each view by its minimum depth (as AstroNet does)
    G = G / np.abs(G.min(1, keepdims=True))
    L = L / np.abs(L.min(1, keepdims=True))
    return G, L, cls, meta


def trap(x, w, ing):
    h = w / 2
    a = np.abs(x)
    return np.clip((h - a) / (ing * h + 1e-9), 0, 1)


def nn_init(sizes, rng):
    return [[rng.normal(0, np.sqrt(2.0 / a), (a, b)), np.zeros(b)] for a, b in zip(sizes[:-1], sizes[1:])]


def nn_fwd(P, X, drop=0.0, rng=None):
    hs = [X]
    masks = []
    for i, (W, b) in enumerate(P):
        z = hs[-1] @ W + b
        if i < len(P) - 1:
            h = np.maximum(z, 0)
            if drop > 0:
                mk = (rng.random(h.shape) > drop) / (1 - drop)
                h = h * mk
                masks.append(mk)
            else:
                masks.append(None)
            hs.append(h)
        else:
            hs.append(1 / (1 + np.exp(-z)))
    return hs, masks


def nn_train(P, X, y, epochs, lr, rng, bs=128, l2=1e-4, drop=0.2):
    m = [[np.zeros_like(W), np.zeros_like(b)] for W, b in P]
    v = [[np.zeros_like(W), np.zeros_like(b)] for W, b in P]
    t = 0
    for ep in range(epochs):
        idx = rng.permutation(len(X))
        for s in range(0, len(X), bs):
            j = idx[s:s + bs]
            hs, masks = nn_fwd(P, X[j], drop, rng)
            g = (hs[-1][:, 0] - y[j])[:, None] / len(j)
            t += 1
            for i in range(len(P) - 1, -1, -1):
                W, b = P[i]
                grads = [hs[i].T @ g + l2 * W, g.sum(0)]
                if i > 0:
                    g = (g @ W.T) * (hs[i] > 0)
                    if masks[i - 1] is not None:
                        g = g * masks[i - 1]
                for q in range(2):
                    m[i][q] = 0.9 * m[i][q] + 0.1 * grads[q]
                    v[i][q] = 0.999 * v[i][q] + 0.001 * grads[q] ** 2
                    P[i][q] -= lr * (m[i][q] / (1 - 0.9 ** t)) / (np.sqrt(v[i][q] / (1 - 0.999 ** t)) + 1e-8)
        lr *= 0.85
    return P


def rule_features(G, L, meta):
    """Four hand-designed tests in the spirit of rule-based vetters: secondary-eclipse significance, V shape,
    asymmetry and depth just outside the transit in the local view."""
    xg = np.linspace(-0.5, 0.5, NG)
    F = np.zeros((len(G), 4))
    c = NL // 2
    for i in range(len(G)):
        w = meta[i, 1]
        noise = np.std(G[i][np.abs(xg) > 0.1])
        secm = np.abs(np.abs(xg) - 0.5) < w / 2
        sec = -np.mean(G[i][secm]) / (noise / np.sqrt(max(1, secm.sum())))
        loc = L[i]
        mid = np.mean(loc[c - 1:c + 2])
        half = 0.5 * (np.mean(loc[c - 4:c - 2]) + np.mean(loc[c + 3:c + 5]))
        vshape = np.clip(half / mid, 0, 1.5) if mid < -0.2 else 0.0
        asym = (np.mean(loc[c + 8:c + 20]) - np.mean(loc[c - 20:c - 8])) / (np.std(loc[:8]) + 1e-6)
        wings = np.mean(np.concatenate([loc[c - 15:c - 9], loc[c + 10:c + 16]]))   # 0.75-1.25 durations out
        F[i] = (sec, abs(1 - vshape), abs(asym), abs(wings))
    return F


def pr_curve(y, s):
    o = np.argsort(-s)
    tp = np.cumsum(y[o] == 1)
    fp = np.cumsum(y[o] == 0)
    prec = tp / np.maximum(tp + fp, 1)
    rec = tp / max(1, (y == 1).sum())
    return prec, rec


def recall_at_precision(y, s, p0):
    prec, rec = pr_curve(y, s)
    ok = prec >= p0
    return rec[ok].max() if ok.any() else 0.0


def vetting():
    rng = np.random.default_rng(510)
    G, L, cls, meta = make_views(rng, 36000)
    X = np.hstack([G, L])
    y = (cls == 0).astype(float)
    ntr, nva = 24000, 4000
    Xtr, ytr = X[:ntr], y[:ntr]
    Xte, yte, mte, cte = X[ntr + nva:], y[ntr + nva:], meta[ntr + nva:], cls[ntr + nva:]
    P = nn_init([X.shape[1], 64, 32, 1], rng)
    P = nn_train(P, Xtr, ytr, epochs=18, lr=2e-3, rng=rng)
    s_nn = nn_fwd(P, Xte)[0][-1][:, 0]
    from sklearn.linear_model import LogisticRegression
    Ftr = rule_features(G[:ntr], L[:ntr], meta[:ntr])
    Fte = rule_features(G[ntr + nva:], L[ntr + nva:], mte)
    lr_ = LogisticRegression(max_iter=1000).fit(Ftr, ytr)
    s_rule = lr_.predict_proba(Fte)[:, 1]
    acc = np.mean((s_nn > 0.5) == (yte == 1))
    print(f"vetting: test set {len(yte)} ({int(yte.sum())} planets); NN accuracy {acc*100:.1f}%")
    for p0 in (0.95, 0.99):
        print(f"vetting: recall at precision {p0}: NN {recall_at_precision(yte, s_nn, p0)*100:.1f}%, "
              f"rules {recall_at_precision(yte, s_rule, p0)*100:.1f}%")
    # AUC
    def auc(y, s):
        o = np.argsort(s)
        r = np.empty(len(s))
        r[o] = np.arange(1, len(s) + 1)
        n1 = (y == 1).sum()
        n0 = len(y) - n1
        return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    print(f"vetting: ROC AUC NN {auc(yte, s_nn):.3f}, rules {auc(yte, s_rule):.3f}")

    fig = plt.figure(figsize=(7.0, 2.85))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1, 1], wspace=0.42)
    ax = fig.add_subplot(gs[0])
    xg = np.linspace(-0.5, 0.5, NG)
    picks = []
    for c in (0, 1, 2):
        ii = np.where((cte == c) & (mte[:, 0] > 14) & (mte[:, 0] < 22))[0]
        if c == 1:
            ii = ii[mte[ii, 2] > 0.25]
        picks.append(ii[0])
    names = ["Planet", "Eclipsing binary", "Instrumental artefact"]
    cols = [BLUE, ORANGE, GREY]
    for k, (i, nme, col) in enumerate(zip(picks, names, cols)):
        g = G[ntr + nva + i]
        ax.plot(xg, g - 3.2 * k, lw=0.7, color=col)
        ax.text(-0.49, -3.2 * k + 0.55, f"{nme} (score {s_nn[i]:.2f})", fontsize=6.4, color=col)
    ax.set_yticks([])
    ax.set_ylim(-8.0, 1.3)
    ax.set_xlabel("Orbital phase", labelpad=1)
    ax.set_xlim(-0.5, 0.5)
    ax.set_title("Global views (normalised)", fontsize=8.2)
    panel_tag(ax, "a")
    ax = fig.add_subplot(gs[1])
    for s, col, lab in [(s_nn, BLUE, "Neural network"), (s_rule, ORANGE, "Four hand-made tests")]:
        prec, rec = pr_curve(yte, s)
        ax.plot(rec, prec, color=col, lw=1.3, label=lab)
    ax.set_xlabel("Recall (planets kept)", labelpad=1)
    ax.set_ylabel("Precision (kept that are planets)")
    ax.set_ylim(0.4, 1.01)
    ax.set_xlim(0, 1)
    ax.legend(loc="lower left", fontsize=6.6)
    ax.set_title("Precision–recall, test set", fontsize=8.2)
    panel_tag(ax, "b")
    ax = fig.add_subplot(gs[2])
    bins = np.array([6, 8, 10, 13, 17, 23, 30, 40])
    cen = np.sqrt(bins[1:] * bins[:-1])
    for s, col, lab in [(s_nn, BLUE, "Neural network"), (s_rule, ORANGE, "Hand-made tests")]:
        # threshold set for 98 % precision on the whole test set
        prec, rec = pr_curve(yte, s)
        o = np.argsort(-s)
        ok = np.where(prec >= 0.98)[0]
        thr = s[o][ok.max()] if len(ok) else np.inf
        r = []
        for a, b in zip(bins[:-1], bins[1:]):
            mm = (mte[:, 0] >= a) & (mte[:, 0] < b) & (yte == 1)
            r.append(np.mean(s[mm] >= thr))
        ax.plot(cen, np.array(r) * 100, "o-", color=col, ms=3, lw=1.2, label=lab)
        print(f"vetting: {lab} recall by SNR bin at 98% precision: " + ", ".join(f"{x*100:.0f}" for x in r))
    ax.set_xscale("log")
    ax.set_xticks([6, 10, 20, 40])
    ax.set_xticklabels(["6", "10", "20", "40"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Signal-to-noise ratio", labelpad=1)
    ax.set_ylabel("Planets kept at 98 % precision (%)")
    ax.set_ylim(0, 102)
    ax.set_title("Where the gain comes from", fontsize=8.2)
    panel_tag(ax, "c")
    foot(fig, "Synthetic data: 36 000 folded signals (40 % planets, 35 % eclipsing binaries with V shapes, secondary "
              "eclipses or odd–even differences, 25 % artefacts), SNR 6–40. Network: 262 inputs (201-bin global and 61-bin "
              "local views), two ReLU layers (64, 32), dropout, Adam; trained on 24 000, tested on 8 000. Seed 510.")
    fig.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.27)
    save(fig, "ch51_vetting")


# ==============================================================================================
# 5. Photometric redshifts with a random forest
FILT = {"u": (367, 50), "g": (482, 140), "r": (622, 140), "i": (755, 130), "z": (869, 100), "y": (971, 90)}
DEPTH5 = {"u": 25.6, "g": 26.9, "r": 26.9, "i": 26.4, "z": 25.6, "y": 24.8}   # approx. 10-year 5-sigma depths


def sed(lam_A, t):
    """Rest-frame f_lambda (arbitrary units) for a galaxy type t in [0, 1] (0 = old elliptical, 1 = starburst).
    Continuum slope, 4000 A break and emission lines are interpolated with t."""
    beta = 1.6 - 3.2 * t                     # f_lambda ~ lambda^-beta*... red to blue
    f = (lam_A / 5000.0) ** (-beta + 2.0)
    brk = 0.6 * (1 - t) ** 1.2 + 0.08
    f = f * np.where(lam_A < 4000, 1 - brk * 1 / (1 + np.exp(-(4000 - lam_A) / 60)), 1.0)
    uv = np.where(lam_A < 2500, np.exp(-(2500 - lam_A) / (300 + 2500 * t)), 1.0)
    f = f * (uv if t < 0.5 else 1.0)
    for lc, ew in [(3727, 40), (4861, 15), (5007, 45), (6563, 90)]:  # emission lines grow with t
        w = ew * t ** 1.5
        f = f + w / (8 * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((lam_A - lc) / 8) ** 2) * np.interp(lc, lam_A, f)
    return f


def photometry(z, t, m_i, rng, av=None):
    lam_obs = np.linspace(3000, 11000, 1600)          # Angstrom
    out = np.zeros((len(z), 6))
    names = list(FILT)
    T = {k: np.exp(-0.5 * ((lam_obs / 10 - c) / (w / 2.35)) ** 2) for k, (c, w) in FILT.items()}
    for n in range(len(z)):
        lr = lam_obs / (1 + z[n])
        fl = sed(lr, t[n])
        if av is not None:
            fl = fl * 10 ** (-0.4 * av[n] * (5500.0 / lr) ** 0.9)     # simple dust attenuation
        tau = np.where(lam_obs < 1216 * (1 + z[n]), 0.0036 * (lam_obs / 1216) ** 3.46, 0.0)
        fl = fl * np.exp(-tau) * (lr > 912)
        fnu = fl * lam_obs ** 2
        fx = np.array([np.sum(fnu * T[k] / lam_obs) / np.sum(T[k] / lam_obs) for k in names])
        out[n] = fx / fx[3]                      # normalise to i band
    flux = out * 10 ** (-0.4 * (m_i[:, None] - 30))
    err = np.array([10 ** (-0.4 * (DEPTH5[k] - 30)) / 5 for k in names])
    noisy = flux + err * rng.standard_normal(flux.shape)
    return noisy, err


def asinh_mag(f, err):
    b = 1.04 * err
    return -2.5 / np.log(10) * (np.arcsinh(f / (2 * b)) + np.log(b)) + 30


def lum_dist(z):
    zz = np.linspace(0, 4, 4001)
    Ez = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    dc = np.concatenate([[0], np.cumsum(0.5 * (1 / Ez[1:] + 1 / Ez[:-1]) * np.diff(zz))]) * 2998.0 / 0.7   # Mpc
    return np.interp(z, zz, dc) * (1 + z)


def photoz():
    from sklearn.ensemble import RandomForestRegressor
    rng = np.random.default_rng(5151)
    n0 = 160000
    z = rng.gamma(2.2, 0.42, n0)
    z = z[(z > 0.02) & (z < 3.0)][:n0]
    t = rng.beta(1.3, 1.6, len(z))
    M = rng.normal(-20.4, 1.3, len(z)) - 0.8 * np.log10(1 + z)       # mild luminosity evolution
    av = rng.uniform(0, 1.2, len(z)) * (0.3 + 0.7 * t)                # dustier star-forming galaxies
    m_i = M + 5 * np.log10(lum_dist(z) * 1e5)
    keep = (m_i < 25.3) & (m_i > 18.5)
    z, t, m_i, av = z[keep], t[keep], m_i[keep], av[keep]
    n = min(len(z), 60000)
    z, t, m_i, av = z[:n], t[:n], m_i[:n], av[:n]
    flux, err = photometry(z, t, m_i, rng, av)
    mags = asinh_mag(flux, err)
    X = np.column_stack([mags[:, 3]] + [mags[:, k] - mags[:, k + 1] for k in range(5)])
    ntr = 30000
    Xtr, ztr, Xte, zte, mte = X[:ntr], z[:ntr], X[ntr:], z[ntr:], m_i[ntr:]

    def stats(zp, zs):
        dz = (zp - zs) / (1 + zs)
        nmad = 1.4826 * np.median(np.abs(dz - np.median(dz)))
        return nmad, np.mean(np.abs(dz) > 0.15), np.median(dz)
    rf = RandomForestRegressor(n_estimators=120, min_samples_leaf=3, n_jobs=2, random_state=0).fit(Xtr, ztr)
    zp = rf.predict(Xte)
    s_all = stats(zp, zte)
    bright = (m_i[:ntr] < 22.5) & (ztr < 1.2)      # like a typical spectroscopic training sample
    rfb = RandomForestRegressor(n_estimators=120, min_samples_leaf=3, n_jobs=2, random_state=0).fit(
        Xtr[bright], ztr[bright])
    zpb = rfb.predict(Xte)
    s_b = stats(zpb, zte)
    print(f"photoz: {len(z)} galaxies (i<25.3), median z {np.median(z):.2f}; train {ntr}, test {len(zte)}")
    print(f"photoz: representative training: sigma_NMAD={s_all[0]:.3f}, outliers={s_all[1]*100:.1f}%, bias={s_all[2]:+.4f}")
    print(f"photoz: spectroscopic-like training (i<22.5, z<1.2, n={bright.sum()}): "
          f"sigma_NMAD={s_b[0]:.3f}, outliers={s_b[1]*100:.1f}%, bias={s_b[2]:+.4f}")
    mb = np.array([19, 21, 22, 23, 24, 24.7, 25.3])
    rows = []
    for a, b in zip(mb[:-1], mb[1:]):
        k = (mte >= a) & (mte < b)
        rows.append((0.5 * (a + b), *stats(zp[k], zte[k]), *stats(zpb[k], zte[k])))
    rows = np.array(rows)
    for r in rows:
        print(f"photoz: i~{r[0]:.1f}: repr NMAD {r[1]:.3f} out {r[2]*100:.1f}% | bright NMAD {r[4]:.3f} out {r[5]*100:.1f}%")

    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.9), gridspec_kw=dict(wspace=0.38))
    for ax, zz, col, ttl, st in [(axs[0], zp, BLUE, "Representative training", s_all),
                                 (axs[1], zpb, ORANGE, "Bright, low-z training", s_b)]:
        ax.hexbin(zte, zz, gridsize=55, extent=(0, 3, 0, 3), bins="log", cmap="Blues" if col == BLUE else "Oranges",
                  mincnt=1, linewidths=0)
        xx = np.linspace(0, 3, 10)
        ax.plot(xx, xx, color=INK, lw=0.6)
        for sgn in (-1, 1):
            ax.plot(xx, xx + sgn * 0.15 * (1 + xx), color=GREY, lw=0.6, ls="--")
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        ax.set_xlabel("True redshift", labelpad=1)
        ax.set_ylabel("Photometric redshift", labelpad=1)
        ax.set_title(ttl, fontsize=8)
        ax.text(0.05, 0.95, f"σ_NMAD = {st[0]:.3f}\noutliers = {st[1]*100:.1f} %", transform=ax.transAxes,
                fontsize=6.8, va="top", color=INK, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
        ax.grid(False)
    panel_tag(axs[0], "a")
    panel_tag(axs[1], "b")
    ax = axs[2]
    ax.plot(rows[:, 0], rows[:, 2] * 100, "o-", color=BLUE, ms=3, label="Representative training")
    ax.plot(rows[:, 0], rows[:, 5] * 100, "s--", color=ORANGE, ms=3, label="Bright, low-z training")
    ax.axhline(10, color=RED, lw=0.8, ls=":")
    ax.text(19.1, 11.5, "LSST limit 10 %", fontsize=6.4, color=RED)
    ax.set_xlabel("i magnitude", labelpad=1)
    ax.set_ylabel("Outliers (%)")
    ax.set_ylim(0, 70)
    ax.legend(fontsize=6.2, loc="upper left", bbox_to_anchor=(0.0, 0.88))
    ax.set_title("Outliers against brightness", fontsize=8)
    panel_tag(ax, "c")
    foot(fig, "Synthetic galaxies: continuum, 4000 Å break and emission lines varying with type, dust; Lyman-α forest "
              "absorption; six LSST-like Gaussian filters with 10-year depths; i < 25.3. Random forest (120 trees) on i "
              "magnitude and five colours; 30 000 training (b: only the 13 929 with i < 22.5 and z < 1.2), 30 000 test galaxies; outliers |Δz|/(1+z) > 0.15. Seed 5151.")
    fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.3)
    save(fig, "ch51_photoz")


# ==============================================================================================
# 6. Transient light-curve classification
TCLS = ["SN Ia", "SN II", "SN Ib/c", "AGN", "Variable star"]


def bazin(t, A, t0, trise, tfall):
    return A * np.exp(-(t - t0) / tfall) / (1 + np.exp(-(t - t0) / trise))


def make_lc(c, rng, tmax=120.0):
    """Two-band (g, r) light curve in flux units, Rubin-like irregular cadence with seasonal gaps."""
    nobs = rng.integers(28, 46)
    tt = np.sort(rng.uniform(-30, tmax, nobs))
    band = rng.integers(0, 2, nobs)
    A = 10 ** rng.uniform(0, 1.0)
    if c == 0:
        p = [(rng.normal(19, 2), rng.normal(1.5, 0.3), rng.normal(18, 3)), (rng.normal(21, 2), rng.normal(1.8, 0.3), rng.normal(28, 4))]
        col = [1.0, 0.85]
        f = np.array([bazin(x, A * col[b], 0, p[b][1], p[b][2]) for x, b in zip(tt, band)])
        f += np.array([0.25 * A * np.exp(-0.5 * ((x - 30) / 8) ** 2) if b == 1 else 0 for x, b in zip(tt, band)])
    elif c == 1:
        plat = rng.uniform(60, 100)
        f = np.array([A * (1 if b else 0.75) * (1 - np.exp(-(x + 10) / 4)) * (x > -10) *
                      np.where(x < plat, np.exp(-x / 400 if b else -x / 150), 0.35 * np.exp(-(x - plat) / 30))
                      for x, b in zip(tt, band)])
    elif c == 2:
        tr, tf = rng.normal(1.0, 0.25), rng.normal(11, 2.5)
        f = np.array([bazin(x, A * (0.7 if b == 0 else 1.0), 0, tr, tf if b else tf * 0.8) for x, b in zip(tt, band)])
    elif c == 3:
        # damped random walk (Ornstein-Uhlenbeck), tau 100-300 d
        tau, sig = rng.uniform(80, 300), A * rng.uniform(0.15, 0.4)
        base = A * rng.uniform(0.6, 1.5)
        x = np.zeros(nobs)
        x[0] = rng.normal(0, sig)
        for k in range(1, nobs):
            dt = tt[k] - tt[k - 1]
            a = np.exp(-dt / tau)
            x[k] = a * x[k - 1] + sig * np.sqrt(1 - a * a) * rng.standard_normal()
        f = base + x * np.where(band == 0, 1.3, 1.0)
    else:
        per = 10 ** rng.uniform(-0.5, 1.3)
        amp = A * rng.uniform(0.3, 0.8)
        ph0 = rng.uniform(0, 1)
        f = A + amp * np.where(band == 0, 1.2, 1.0) * np.sin(2 * np.pi * (tt / per + ph0)) ** 3
    sig_n = 0.08 + 0.04 * rng.random()
    fobs = f + sig_n * rng.standard_normal(nobs)
    return tt, band, fobs, sig_n


def lc_features(tt, band, f, sig, tcut):
    """Features from observations up to tcut days after the first 5-sigma detection."""
    det = np.where(f > 5 * sig)[0]
    if len(det) == 0:
        return None
    t1 = tt[det[0]]
    m = tt <= t1 + tcut
    tt, band, f = tt[m], band[m], f[m]
    feats = []
    for b in (0, 1):
        k = band == b
        if k.sum() < 2:
            feats += [0, 0, 0, 0, 0]
            continue
        x, y = tt[k], f[k]
        j = np.argmax(y)
        rise = (y[j] - y[0]) / max(1.0, x[j] - x[0])
        fall = (y[j] - y[-1]) / max(1.0, x[-1] - x[j])
        feats += [y.max(), np.std(y) / (np.mean(np.abs(y)) + 1e-3), rise / (y.max() + 1e-3), fall / (y.max() + 1e-3),
                  (x[j] - t1)]
    # colour and variability statistics
    g, r = f[band == 0], f[band == 1]
    col = (np.mean(g) - np.mean(r)) / (np.mean(np.abs(f)) + 1e-3) if (len(g) and len(r)) else 0
    d = np.diff(f) / (np.std(f) + 1e-3)
    pre = np.mean(f[tt < t1 - 5]) / (f.max() + 1e-3) if np.any(tt < t1 - 5) else 0   # flux before detection
    feats += [col, np.mean(np.abs(d)), pre, tt.max() - t1, len(f)]
    return feats


def transients():
    from sklearn.ensemble import RandomForestClassifier
    rng = np.random.default_rng(5152)
    prior = np.array([0.3, 0.25, 0.1, 0.2, 0.15])
    n = 9000
    cls = rng.choice(5, n, p=prior)
    lcs = [make_lc(c, rng) for c in cls]
    cuts = [5, 10, 20, 40, 150]
    acc = []
    res_full = None
    ntr = 6000
    for tc in cuts:
        F, y = [], []
        for (tt, band, f, sg), c in zip(lcs, cls):
            v = lc_features(tt, band, f, sg, tc)
            F.append(v if v is not None else [0] * 15)
            y.append(c)
        F, y = np.array(F, float), np.array(y)
        rf = RandomForestClassifier(n_estimators=200, min_samples_leaf=2, n_jobs=2, random_state=1,
                                    class_weight="balanced").fit(F[:ntr], y[:ntr])
        pr = rf.predict(F[ntr:])
        yt = y[ntr:]
        a = np.mean(pr == yt)
        rec = [np.mean(pr[yt == k] == k) for k in range(5)]
        acc.append((a, rec))
        print(f"transients: {tc:3d} d after detection: accuracy {a*100:.1f}%; recall " +
              ", ".join(f"{TCLS[k]} {rec[k]*100:.0f}%" for k in range(5)))
        if tc == cuts[-1]:
            res_full = (yt, pr)
    yt, pr = res_full
    cm = np.zeros((5, 5))
    for a_, b_ in zip(yt, pr):
        cm[a_, b_] += 1
    cmn = cm / cm.sum(1, keepdims=True)

    fig = plt.figure(figsize=(7.0, 2.75))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 1.05], wspace=0.45)
    ax = fig.add_subplot(gs[0])
    cols = [BLUE, RED, ORANGE, VIOLET, GREEN]
    rr = np.random.default_rng(7)
    off = {0: 0.0, 1: -1.0, 3: -2.0}
    for k, lab in ((0, "SN Ia"), (1, "SN II"), (3, "AGN")):
        tt, band, f, sg = make_lc(k, rr)
        f = f / max(1e-3, np.percentile(f, 98)) * 0.8
        for b, mk in ((0, "o"), (1, "s")):
            m = band == b
            ax.plot(tt[m], f[m] + off[k], mk, ms=2.2, color=cols[k], alpha=0.85,
                    mfc="none" if b == 0 else cols[k], mew=0.7, lw=0)
        ax.text(118, off[k] + 0.55, lab, fontsize=6.6, color=cols[k], ha="right")
    ax.text(-28, -2.3, "○ g band   ■ r band", fontsize=6.0, color=GREY)
    ax.set_yticks([])
    ax.set_xlim(-32, 122)
    ax.set_ylim(-2.4, 1.15)
    ax.set_xlabel("Days", labelpad=1)
    ax.set_ylabel("Scaled flux (offset)")
    ax.set_title("Sparse two-band light curves", fontsize=8)
    panel_tag(ax, "a")
    ax = fig.add_subplot(gs[1])
    im = ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
    for a_ in range(5):
        for b_ in range(5):
            ax.text(b_, a_, f"{cmn[a_, b_]*100:.0f}", ha="center", va="center", fontsize=6.4,
                    color="white" if cmn[a_, b_] > 0.6 else INK)
    short = ["Ia", "II", "Ib/c", "AGN", "Var"]
    ax.set_xticks(range(5))
    ax.set_xticklabels(short, fontsize=6.6)
    ax.set_yticks(range(5))
    ax.set_yticklabels(short, fontsize=6.6)
    ax.set_xlabel("Predicted class", labelpad=1)
    ax.set_ylabel("True class", labelpad=0)
    ax.grid(False)
    ax.set_title("Full light curves (%)", fontsize=8)
    panel_tag(ax, "b")
    ax = fig.add_subplot(gs[2])
    ax.plot(cuts, [a[0] * 100 for a in acc], "o-", color=NAVY, lw=1.5, ms=3.5, label="All classes")
    for k, col in zip(range(5), cols):
        ax.plot(cuts, [a[1][k] * 100 for a in acc], "-", color=col, lw=0.9, alpha=0.9, label=TCLS[k])
    ax.set_xscale("log")
    ax.set_xticks(cuts)
    ax.set_xticklabels([str(c) for c in cuts])
    ax.set_xlabel("Days of data after first detection", labelpad=1)
    ax.set_ylabel("Accuracy or recall (%)")
    ax.set_ylim(0, 102)
    ax.legend(fontsize=5.8, loc="lower right", ncol=1, handlelength=1.4)
    ax.set_title("Early classification", fontsize=8)
    panel_tag(ax, "c")
    foot(fig, "Synthetic two-band light curves: SN Ia, II, Ib/c (Bazin-type profiles with class-dependent rise, decline, "
              "colour and secondary peak), AGN (damped random walk) and periodic variables; 28–45 irregular epochs with "
              "noise. Random forest (200 trees, 15 features); 6 000 training and 3 000 test objects. Seed 5152.")
    fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.27)
    save(fig, "ch51_transients")


# ==============================================================================================
# 7. Crater counting with a synthetic detector, completeness correction and model age
NPF_A = [-3.0876, -3.557528, 0.781027, 1.021521, -0.156012, -0.444058, 0.019977, 0.086850, -0.005874, -0.006809,
         8.25e-4, 5.54e-5]


def npf_shape(D_km):
    """log10 N(>D) per km^2 for the lunar production function (Neukum et al. 2001), normalised to N(1 km) = 1."""
    x = np.log10(D_km)
    return sum(a * x ** k for k, a in enumerate(NPF_A)) - NPF_A[0]


def n1_age(T):
    """Cumulative density of craters >= 1 km per km^2 for age T (Gyr), Neukum chronology."""
    return 5.44e-14 * (np.exp(6.93 * T) - 1) + 8.38e-4 * T


def ncum(D_km, T):
    return n1_age(T) * 10 ** npf_shape(D_km)


def sample_craters(rng, area, T, dmin=0.004, dmax=1.0):
    n = rng.poisson(area * (ncum(dmin, T) - ncum(dmax, T)))
    lg = np.linspace(np.log10(dmin), np.log10(dmax), 800)
    c = ncum(10 ** lg, T)
    u = rng.uniform(c[-1], c[0], n)
    return 10 ** np.interp(u, c[::-1], lg[::-1])


PIX_KM = 0.0015                       # 1.5 m pixels (LROC NAC class)


def detector(rng, D, area):
    """Synthetic detector: recall rises with size in pixels (50 % at 7 px, 95 % plateau); 7 % diameter error;
    false positives (shadows, boulders) concentrated near the resolution limit."""
    px = D / PIX_KM
    p = 0.95 / (1 + np.exp(-(px - 7) / 1.4))
    hit = rng.random(len(D)) < p
    Dm = D[hit] * np.exp(0.07 * rng.standard_normal(hit.sum()))
    nfp = rng.poisson(160.0 * area)            # per km^2, above 4 px
    fp = 4 * PIX_KM * (1 + rng.pareto(5.0, nfp))
    return np.concatenate([Dm, fp]), hit


EDG = 10 ** np.arange(np.log10(0.006), np.log10(0.6) + 1e-9, 0.1)    # 6 m - 600 m, 10 bins per decade


def fit_age(counts, area, comp=None, fpd=None, use=None):
    from scipy.optimize import minimize_scalar
    if use is None:
        use = np.ones(len(counts), bool)
    shape = 10 ** npf_shape(EDG)
    dN = shape[:-1] - shape[1:]                # per unit N(1)

    def nll(logT):
        T = 10 ** logT
        lam = area * n1_age(T) * dN
        if comp is not None:
            lam = lam * comp + fpd * area
        lam = np.maximum(lam[use], 1e-12)
        return np.sum(lam - counts[use] * np.log(lam))
    r = minimize_scalar(nll, bounds=(-3, 0.6), method="bounded")
    return 10 ** r.x


def craters():
    rng = np.random.default_rng(5153)
    T_true, area = 0.05, 10.0
    # calibration: injection-recovery on a separate labelled area of 5 km^2 (several realisations)
    hits_b, tot_b, fp_b = np.zeros(len(EDG) - 1), np.zeros(len(EDG) - 1), np.zeros(len(EDG) - 1)
    cal_area = 0
    for k in range(6):
        Dt = sample_craters(rng, 5.0, T_true * 2)
        det, hit = detector(rng, Dt, 5.0)
        tot_b += np.histogram(Dt, EDG)[0]
        hits_b += np.histogram(Dt[hit], EDG)[0]
        nreal = hit.sum()
        fp_b += np.histogram(det[nreal:], EDG)[0]
        cal_area += 5.0
    comp = np.clip(hits_b / np.maximum(tot_b, 1), 0.02, 1)
    fpd = fp_b / cal_area
    # one realisation for panel (a)
    Dt = sample_craters(rng, area, T_true)
    det, hit = detector(rng, Dt, area)
    cnt = np.histogram(det, EDG)[0].astype(float)
    tru = np.histogram(Dt, EDG)[0].astype(float)
    corr = np.clip((cnt - fpd * area) / comp, 0, None)
    big = EDG[:-1] >= 0.030
    good = comp > 0.5
    a_naive = fit_age(cnt, area)
    a_big = fit_age(cnt, area, use=big)
    a_corr = fit_age(cnt, area, comp, fpd, use=good)
    print(f"craters: area {area} km2, true age {T_true*1e3:.0f} Myr; true craters >=6 m: {np.sum(Dt>=0.006)}, "
          f"detections (incl. false) >=6 m: {np.sum(det>=0.006)}; craters >=30 m: {np.sum(Dt>=0.03)}")
    print("craters: bin edges (m) " + ", ".join(f"{e*1e3:.1f}" for e in EDG[:8]) + "; completeness " +
          ", ".join(f"{c:.2f}" for c in comp[:7]) + f"; first fitted bin starts {EDG[:-1][good][0]*1e3:.1f} m" +
          f"; false-positive share of detections 6-10 m: {fpd[:2].sum()*area/max(1,cnt[:2].sum())*100:.0f}%")
    print(f"craters: single run ages (Myr): naive all bins {a_naive*1e3:.0f}, only D>=30 m {a_big*1e3:.0f}, "
          f"corrected {a_corr*1e3:.0f}")
    # Monte Carlo of estimator bias and spread
    res = {"naive": [], "big": [], "corr": []}
    for k in range(200):
        Dt_ = sample_craters(rng, area, T_true)
        det_, _ = detector(rng, Dt_, area)
        c_ = np.histogram(det_, EDG)[0].astype(float)
        res["naive"].append(fit_age(c_, area))
        res["big"].append(fit_age(c_, area, use=big))
        res["corr"].append(fit_age(c_, area, comp, fpd, use=good))
    for k, v in res.items():
        v = np.array(v) * 1e3
        print(f"craters: MC {k}: median {np.median(v):.0f} Myr, 16-84% {np.percentile(v,16):.0f}-{np.percentile(v,84):.0f}")
    areas = [0.3, 1, 3, 10, 30]
    spread = {"big": [], "corr": []}
    for A in areas:
        vb, vc = [], []
        for k in range(120):
            Dt_ = sample_craters(rng, A, T_true)
            det_, _ = detector(rng, Dt_, A)
            c_ = np.histogram(det_, EDG)[0].astype(float)
            vb.append(fit_age(c_, A, use=big))
            vc.append(fit_age(c_, A, comp, fpd, use=good))
        spread["big"].append(0.5 * (np.percentile(vb, 84) - np.percentile(vb, 16)) / T_true * 100)
        spread["corr"].append(0.5 * (np.percentile(vc, 84) - np.percentile(vc, 16)) / T_true * 100)
    print("craters: relative 1-sigma age error vs area (km2) " + ", ".join(
        f"{A}: big {b:.0f}% corr {c:.0f}%" for A, b, c in zip(areas, spread["big"], spread["corr"])))

    fig, axs = plt.subplots(1, 3, figsize=(7.0, 3.0), gridspec_kw=dict(width_ratios=[1.15, 1, 0.9], wspace=0.4))
    ax = axs[0]
    Dc = EDG[:-1] * 1e3
    cum = lambda h: np.cumsum(h[::-1])[::-1] / area
    for T, ls in [(0.025, ":"), (0.05, "-"), (0.1, "--")]:
        dd = np.logspace(np.log10(0.005), np.log10(0.6), 100)
        ax.plot(dd * 1e3, ncum(dd, T), color=GREY, lw=0.7, ls=ls)
        ax.text(330, ncum(0.33, T) * (2.2 if T > 0.06 else (0.25 if T < 0.03 else 1)), f"{T*1e3:.0f} Myr",
                fontsize=6.0, color=GREY, ha="left", va="center")
    ax.plot(Dc, cum(tru), "o", ms=2.6, color=INK, mfc="none", mew=0.6, label="All craters (truth)")
    ax.plot(Dc, cum(cnt), "s", ms=2.6, color=ORANGE, label="Raw detections")
    ax.plot(Dc, cum(corr), "^", ms=2.8, color=BLUE, label="Corrected")
    ax.axvspan(5, EDG[:-1][good][0] * 1e3, color=LIGHT, zorder=0)
    ax.text(5.6, 3e-3, "detector\nincomplete", fontsize=6.0, color=GREY)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(5, 700)
    ax.set_ylim(1e-3, 3e4)
    ax.set_xlabel("Crater diameter D (m)", labelpad=1)
    ax.set_ylabel("Cumulative density N(≥D) per km²")
    ax.legend(fontsize=6.0, loc="upper right")
    ax.set_title(f"One count, {area:.0f} km², true age {T_true*1e3:.0f} Myr", fontsize=7.8)
    panel_tag(ax, "a")
    ax = axs[1]
    bins = np.linspace(10, 90, 41)
    for k, col, lab in [("naive", ORANGE, "Raw, all sizes"), ("big", GREY, "Raw, D ≥ 30 m only"),
                        ("corr", BLUE, f"Corrected, D ≥ {EDG[:-1][good][0]*1e3:.0f} m")]:
        v = np.array(res[k]) * 1e3
        ax.hist(v, bins, color=col, alpha=0.55 if k != "corr" else 0.75, label=lab)
    ax.axvline(T_true * 1e3, color=INK, lw=0.8, ls="--")
    ax.set_xlabel("Model age (Myr)", labelpad=1)
    ax.set_ylabel("Count in 200 trials")
    ax.set_ylim(0, 270)
    ax.legend(fontsize=6.0, loc="upper right", frameon=True, facecolor="white", edgecolor="none", framealpha=0.9)
    ax.set_title("Bias and spread of the age", fontsize=7.8)
    panel_tag(ax, "b")
    ax = axs[2]
    ax.plot(areas, spread["big"], "o-", color=GREY, ms=3, label="D ≥ 30 m only")
    ax.plot(areas, spread["corr"], "^-", color=BLUE, ms=3, label="Corrected")
    ax.set_xscale("log")
    ax.set_ylim(0, 55)
    ax.set_xticks(areas)
    ax.set_xticklabels([str(a) for a in areas])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Count area (km²)", labelpad=1)
    ax.set_ylabel("Age uncertainty, 1σ (%)")
    ax.legend(fontsize=6.0, loc="upper right")
    ax.set_title("Bigger areas, smaller errors", fontsize=7.8)
    panel_tag(ax, "c")
    foot(fig, "Lunar production and chronology functions of Neukum et al. (2001). Synthetic detector on 1.5 m pixels: "
              "recall 50 % at 7 px rising to 95 %, 7 % diameter error, false positives near the resolution limit. "
              "Completeness and false-positive rates measured by injection on a separate 30 km² labelled set; ages by "
              "Poisson maximum likelihood in 10 bins per decade. Seed 5153.")
    fig.subplots_adjust(left=0.08, right=0.99, top=0.9, bottom=0.31)
    save(fig, "ch51_craters")


# ==============================================================================================
# 8. Linear spectral unmixing on synthetic hyperspectral pixels
WL = np.arange(0.40, 2.601, 0.01)        # micrometres, 221 bands


def absorb(bands):
    return np.exp(-sum(a * np.exp(-0.5 * ((WL - c) / w) ** 2) for c, w, a in bands))


def endmembers():
    ferric = lambda d: 1 - d * np.exp(-0.5 * ((WL - 0.45) / 0.12) ** 2)
    E = {
        "Olivine": (0.22 + 0.06 * WL) * absorb([(0.85, 0.07, 0.25), (1.05, 0.10, 0.55), (1.25, 0.13, 0.45)]) * ferric(0.3),
        "Pyroxene": (0.20 + 0.05 * WL) * absorb([(0.92, 0.08, 0.45), (1.92, 0.20, 0.40)]) * ferric(0.25),
        "Mg carbonate": (0.42 + 0.03 * WL) * absorb([(1.0, 0.25, 0.10), (1.91, 0.03, 0.12), (2.30, 0.04, 0.35),
                                                     (2.51, 0.045, 0.42)]) * ferric(0.15),
        "Fe/Mg smectite": (0.30 + 0.03 * WL) * absorb([(1.41, 0.02, 0.20), (1.91, 0.03, 0.35), (2.29, 0.025, 0.25),
                                                       (2.39, 0.03, 0.12)]) * ferric(0.35),
        "Dust": np.clip(0.42 - 0.27 * np.exp(-(WL - 0.40) / 0.22), 0, None) * absorb([(0.88, 0.08, 0.08)]),
    }
    return list(E), np.array(list(E.values()))


def smooth_field(rng, shape, scale):
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(rng.standard_normal(shape), scale) * scale


def fcls(E, X, delta=50.0):
    from scipy.optimize import nnls
    k = E.shape[0]
    A = np.vstack([E.T, delta * np.ones((1, k))])
    out = np.zeros((X.shape[0], k))
    res = np.zeros(X.shape[0])
    for i, x in enumerate(X):
        a, _ = nnls(A, np.concatenate([x, [delta]]))
        out[i] = a
        res[i] = np.linalg.norm(E.T @ a - x) / np.sqrt(len(x))
    return out, res


def unmixing():
    from sklearn.decomposition import NMF
    from scipy.optimize import linear_sum_assignment
    rng = np.random.default_rng(5154)
    names, E = endmembers()
    H, W = 48, 72
    yy, xx = np.mgrid[0:H, 0:W]
    # scene: a fan (carbonate + smectite) in the upper left, olivine sand in a channel, pyroxene floor, dust cover
    fan = np.exp(-(((xx - 18) / 16) ** 2 + ((yy - 14) / 11) ** 2))
    chan = np.exp(-((yy - (30 + 6 * np.sin(xx / 9))) / 4.5) ** 2)
    logits = np.stack([
        2.8 * chan + 0.5 * smooth_field(rng, (H, W), 3),
        1.2 + 0.5 * smooth_field(rng, (H, W), 4),
        3.0 * fan * (xx > 14) + 0.5 * smooth_field(rng, (H, W), 3) - 1.0,
        3.0 * fan * (xx <= 22) + 0.5 * smooth_field(rng, (H, W), 3) - 1.0,
        0.6 + 0.6 * smooth_field(rng, (H, W), 5),
    ])
    Atrue = np.exp(logits) / np.exp(logits).sum(0)
    At = Atrue.reshape(5, -1).T
    # each pixel sees slightly different endmembers (band depth and brightness vary by grain size, illumination)
    npx = At.shape[0]
    X = np.zeros((npx, len(WL)))
    for k in range(5):
        depth = np.exp(0.15 * rng.standard_normal(npx))[:, None]
        cont = np.max(E[k]) * np.ones_like(E[k])
        Ek = cont - (cont - E[k]) * depth                      # deeper or shallower bands
        Ek = Ek * np.exp(0.05 * rng.standard_normal(npx))[:, None]
        X += At[:, [k]] * Ek
    shade = np.clip(1 + 0.06 * smooth_field(rng, (H, W), 2).ravel(), 0.85, 1.15)
    X = X * shade[:, None]                                        # topographic shading
    snr = 150.0
    X = X + (X.mean() / snr) * rng.standard_normal(X.shape)
    est, res = fcls(E, X)
    rmse = np.sqrt(np.mean((est - At) ** 2, axis=0))
    ls = np.linalg.lstsq(E.T, X.T, rcond=None)[0].T
    print("unmixing: FCLS abundance RMSE (percentage points): " + ", ".join(f"{n} {r*100:.1f}" for n, r in zip(names, rmse)))
    print(f"unmixing: unconstrained LS: share of negative abundances {np.mean(ls < 0)*100:.1f}%, "
          f"RMSE {np.sqrt(np.mean((ls - At) ** 2))*100:.1f} pp vs FCLS {np.sqrt(np.mean((est - At) ** 2))*100:.1f} pp")
    # missing endmember: library without smectite
    keep = [0, 1, 2, 4]
    est4, res4 = fcls(E[keep], X)
    print(f"unmixing: residual RMS full library {np.median(res)*1e3:.2f}e-3; without smectite: median "
          f"{np.median(res4)*1e3:.2f}e-3, 99th pct {np.percentile(res4,99)*1e3:.2f}e-3")
    # blind NMF
    nmf = NMF(n_components=5, init="nndsvda", max_iter=1500, random_state=0, tol=1e-6)
    Wn = nmf.fit_transform(X)
    Hn = nmf.components_
    def sam(a, b):
        return np.degrees(np.arccos(np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)))
    C = np.array([[sam(E[i], Hn[j]) for j in range(5)] for i in range(5)])
    r_, c_ = linear_sum_assignment(C)
    print("unmixing: NMF spectral angle to true endmember (deg): " + ", ".join(f"{names[i]} {C[i, j]:.1f}" for i, j in zip(r_, c_)))
    # NMF abundances (scale so that sum of abundance x mean reflectance matches)
    Wsc = Wn * Hn.mean(1)
    Wsc = Wsc / Wsc.sum(1, keepdims=True)
    carb_nmf = Wsc[:, c_[list(r_).index(2)]]
    print(f"unmixing: NMF carbonate abundance RMSE {np.sqrt(np.mean((carb_nmf - At[:, 2]) ** 2))*100:.1f} pp")

    fig = plt.figure(figsize=(7.0, 4.0))
    gs = fig.add_gridspec(2, 6, height_ratios=[1.1, 1], hspace=0.62, wspace=0.9)
    ax = fig.add_subplot(gs[0, :3])
    cols = [GREEN, NAVY, ORANGE, VIOLET, RED]
    for k, (nme, col) in enumerate(zip(names, cols)):
        ax.plot(WL, E[k], color=col, lw=1.2, label=nme)
    for c in (1.05, 1.92, 2.30, 2.51):
        ax.axvline(c, color=GREY, lw=0.4, ls=":")
    ax.set_xlim(0.4, 2.6)
    ax.set_ylim(0, 0.66)
    ax.set_xlabel("Wavelength (µm)", labelpad=1)
    ax.set_ylabel("Reflectance")
    ax.legend(fontsize=5.9, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.02), handlelength=1.2, columnspacing=0.8)
    ax.set_title("Endmember library (synthetic)", fontsize=8)
    panel_tag(ax, "a")
    ax = fig.add_subplot(gs[0, 3:])
    for k, col in enumerate(cols):
        ax.plot(At[::4, k] * 100, est[::4, k] * 100, ".", ms=1.6, color=col, alpha=0.6)
    ax.plot([0, 100], [0, 100], color=INK, lw=0.6)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("True abundance (%)", labelpad=1)
    ax.set_ylabel("Estimated (%)")
    ax.text(3, 95, "RMSE (points):\n" + "\n".join(f"{n} {r*100:.1f}" for n, r in zip(names, rmse)), fontsize=6.0,
            va="top", color=INK)
    ax.set_title("Fully constrained least squares", fontsize=8)
    panel_tag(ax, "b")
    maps = [(At[:, 2], "True carbonate", "Greens", (0, 0.8)), (est[:, 2], "Estimated carbonate", "Greens", (0, 0.8)),
            (res4, "Residual, library\nwithout smectite", "Purples", (0, np.percentile(res4, 99.5)))]
    for k, (m, ttl, cm, lim) in enumerate(maps):
        ax = fig.add_subplot(gs[1, 2 * k:2 * k + 2])
        ax.imshow(m.reshape(H, W), cmap=cm, vmin=lim[0], vmax=lim[1], interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_title(ttl, fontsize=7.6)
        panel_tag(ax, "cde"[k])
    foot(fig, f"Synthetic 48 × 72-pixel scene, 221 bands (0.40–2.60 µm), five endmembers with absorption bands at the "
              f"positions of real minerals, linear (areal) mixing, noise SNR {snr:.0f}. FCLS = non-negative least squares "
              "with a sum-to-one row. Without the smectite spectrum, the residual map outlines where the library is "
              "incomplete. Seed 5154.")
    fig.subplots_adjust(left=0.07, right=0.99, top=0.94, bottom=0.13)
    save(fig, "ch51_unmixing")


# ==============================================================================================
# 9. Earth-Mars light-time and the speed of ground support
def helio(L0, n, a, e, pibar, d):
    M = np.radians((L0 + n * d - pibar) % 360)
    Ecc = M.copy()
    for _ in range(12):
        Ecc = Ecc - (Ecc - e * np.sin(Ecc) - M) / (1 - e * np.cos(Ecc))
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(Ecc / 2), np.sqrt(1 - e) * np.cos(Ecc / 2))
    r = a * (1 - e * np.cos(Ecc))
    lon = nu + np.radians(pibar)
    return r * np.cos(lon), r * np.sin(lon)


def delay():
    import datetime as dt
    d0 = (dt.date(2026, 1, 1) - dt.date(2000, 1, 1)).days - 0.5
    d = d0 + np.arange(0, 3.5 * 365.25, 0.5)
    xe, ye = helio(100.46457, 0.98560912, 1.00000261, 0.01671123, 102.93768, d)
    xm, ym = helio(-4.55343, 0.52402068, 1.52371034, 0.09339410, -23.94363, d)
    dist = np.hypot(xm - xe, ym - ye)
    lt = dist * 149.598e6 / 299792.458 / 60          # minutes
    # Sun-Earth-Mars elongation at Earth
    ve, vm = np.stack([-xe, -ye]), np.stack([xm - xe, ym - ye])
    elong = np.degrees(np.arccos(np.sum(ve * vm, 0) / np.linalg.norm(ve, axis=0) / np.linalg.norm(vm, axis=0)))
    dates = [dt.date(2000, 1, 1) + dt.timedelta(days=float(x + 0.5)) for x in d]
    i_min, i_max = np.argmin(lt), np.argmax(lt)
    blk = elong < 2.0
    print(f"delay: one-way light-time {lt.min():.1f}-{lt.max():.1f} min; closest {dates[i_min]}, farthest {dates[i_max]}")
    for lim in (2.0, 3.0):
        b = (elong < lim).astype(int)
        st = np.where(np.diff(np.concatenate([[0], b])) == 1)[0]
        en = np.where(np.diff(np.concatenate([b, [0]])) == -1)[0]
        for a_, b_ in zip(st, en):
            print(f"delay: elongation < {lim} deg {dates[a_]} to {dates[b_]} ({(b_-a_)*0.5:.0f} d), "
                  f"min elong {elong[a_:b_+1].min():.2f} on {dates[a_ + np.argmin(elong[a_:b_+1])]}, lt {lt[a_:b_+1].max():.1f} min")
    # CO2 build-up example: 4 crew, 1.0 kg CO2 per person per day, 100 m3 free volume, 22 C
    rate = 4 * 1.0 / 24 / 0.044 * 8.314 * 295 / 100      # Pa per hour
    print(f"delay: CO2 rise {rate:.0f} Pa/h; 0.4 -> 1.0 kPa in {600/rate:.1f} h")

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.9), gridspec_kw=dict(width_ratios=[1.0, 1.15], wspace=0.75))
    ax = axs[0]
    yrs = np.array([x.year + (x.timetuple().tm_yday - 0.5) / 365.25 for x in dates])
    ax.plot(yrs, lt, color=BLUE, lw=1.4, label="One-way light-time")
    ax.plot(yrs, 2 * lt + 30, color=ORANGE, lw=1.2, ls="--", label="Ground loop: 2 × light-time + 30 min")
    ax.fill_between(yrs, 0, 100, where=elong < 3, color=RED, alpha=0.15, lw=0)
    if (elong < 3).any():
        jj = np.where(elong < 3)[0]
        ax.text(yrs[jj][-1] + 0.05, 97, "solar\nconjunction:\nno link", fontsize=6.2, color=RED, ha="left", va="top")
    ax.set_xlim(yrs[0], yrs[-1])
    ax.set_ylim(0, 100)
    ax.set_xticks([2026, 2027, 2028, 2029])
    ax.set_xticklabels(["2026", "2027", "2028", "2029"])
    ax.set_ylabel("Minutes")
    ax.legend(fontsize=6.2, loc="upper left", bbox_to_anchor=(0.0, 0.88))
    ax.set_title("Earth–Mars delay, 2026–29", fontsize=8)
    panel_tag(ax, "a")
    ax = axs[1]
    ev = [("Fire, rapid leak of cabin air", 10, 300), ("Cardiac arrest", 60, 600), ("Severe allergic reaction", 120, 1200),
          ("Toxic leak (ammonia)", 60, 1800), ("CO₂ removal stops (4 crew)", 3 * 3600, 8 * 3600),
          ("Abdominal pain, diagnosis", 6 * 3600, 3 * 86400), ("Pump fails, spare on board", 86400, 10 * 86400),
          ("Plan a repair with no spare", 3 * 86400, 30 * 86400)]
    loops = [("Moon", 2 * 1.3 + 300), ("Mars, close", 2 * lt.min() * 60 + 1800), ("Mars, far", 2 * lt.max() * 60 + 1800),
             ("Solar\nconjunction", 14 * 86400)]
    n = len(ev)
    for k, (nme, a, b) in enumerate(ev[::-1]):
        far = loops[2][1]
        col = RED if b < loops[1][1] else (GOLD if b < far * 3 else GREEN)
        ax.barh(k, np.log10(b) - np.log10(a), left=np.log10(a), height=0.6, color=col, alpha=0.8)
    ax.set_yticks(range(n))
    ax.set_yticklabels([e[0] for e in ev[::-1]], fontsize=6.3)
    lab_pos = {"Moon": (n + 0.15, "left"), "Mars, close": (n + 0.75, "left"), "Mars, far": (n + 0.15, "left"),
               "Solar\nconjunction": (n + 0.75, "right")}
    for nme, tt in loops:
        ax.plot([np.log10(tt)] * 2, [-0.6, n - 0.4], color=NAVY, lw=0.8, ls="--")
        if "conjunction" in nme:
            ax.text(np.log10(tt) - 0.06, n - 0.5, "Solar conjunction", fontsize=6.0, color=NAVY, rotation=90,
                    ha="right", va="top")
            continue
        yv, ha = lab_pos[nme]
        ax.text(np.log10(tt) + (0.05 if ha == "left" else -0.05), yv, nme, fontsize=6.0, color=NAVY, ha=ha,
                va="bottom")
    ticks = [(1, "1 s"), (60, "1 min"), (3600, "1 h"), (86400, "1 day"), (30 * 86400, "1 month")]
    ax.set_xticks([np.log10(t) for t, _ in ticks])
    ax.set_xticklabels([l for _, l in ticks], fontsize=7)
    ax.set_xlim(-0.4, np.log10(60 * 86400))
    ax.set_ylim(-0.6, len(ev) + 1.3)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Time available to act", labelpad=1)
    ax.set_title("Who must decide?", fontsize=8)
    panel_tag(ax, "b", x=-0.6)
    foot(fig, "(a) Heliocentric Keplerian orbits of Earth and Mars (J2000 elements, coplanar approximation); shading "
              "where Mars is within 3° of the Sun. (b) Approximate times available before harm, compared with a ground "
              "loop of two light-times plus 30 minutes for experts to respond. Red: crew must act alone; green: ground "
              "advice can arrive in time, except during solar conjunction.")
    fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.28)
    save(fig, "ch51_delay")


# ==============================================================================================
# 10. Predictive maintenance of life-support fans
def eclss():
    from sklearn.ensemble import HistGradientBoostingClassifier
    rng = np.random.default_rng(5155)
    nunit, ndays = 60, 1100
    rows, meta = [], []
    for u in range(nunit):
        tf = rng.weibull(2.5) * 900 + 60            # failure day
        tau = rng.uniform(15, 40)                   # wear acceleration time scale (days)
        days = np.arange(ndays)
        alive = days < tf
        h = np.exp(np.clip((days - tf) / tau, -30, 0))           # health indicator 0 -> 1 at failure
        speed = np.where(rng.random(ndays) < 0.35, 1.0, 0.0)   # high-speed days (e.g. sleep vs work)
        speed = np.round(np.convolve(speed, np.ones(5) / 5, "same"))
        amb = 22 + 1.2 * np.sin(2 * np.pi * days / 90) + 0.4 * rng.standard_normal(ndays)
        vib = (1.0 + 0.6 * speed) * (1 + 0.8 * h + 0.08 * rng.standard_normal(ndays))
        cur = 1.0 + 0.35 * speed + 0.02 * (amb - 22) + 0.12 * h + 0.025 * rng.standard_normal(ndays)
        tmp = amb + 6 + 2 * speed + 4 * h + 0.5 * rng.standard_normal(ndays)
        lab = (tf - days <= 30) & alive
        for k in np.where(alive)[0]:
            lo = max(0, k - 30)
            w7 = slice(max(0, k - 6), k + 1)
            sp = speed[w7]
            rows.append([speed[k], amb[k], vib[k], cur[k], tmp[k],
                         np.mean(vib[w7] / (1 + 0.6 * speed[w7])) - np.mean(vib[lo:k + 1] / (1 + 0.6 * speed[lo:k + 1])),
                         np.mean(cur[w7] - 0.35 * sp), np.mean(tmp[w7] - amb[w7] - 2 * sp)])
            meta.append((u, k, tf, lab[k], vib[k] / (1 + 0 * speed[k])))
    X = np.array(rows)
    M = np.array(meta)
    unit, day, tfail, y = M[:, 0].astype(int), M[:, 1], M[:, 2], M[:, 3].astype(bool)
    train = unit < 40
    clf = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, random_state=0)
    clf.fit(X[train], y[train])
    score = clf.predict_proba(X)[:, 1]
    test = ~train
    nfail = len(np.unique(unit[test & (tfail < ndays)]))
    unit_years = np.sum(test) / 365.25

    def evaluate(sc, thr, persist=3):
        warn, fa = [], 0
        for u in np.unique(unit[test]):
            m = test & (unit == u)
            s_, d_, tf_ = sc[m], day[m], tfail[m][0]
            al = np.convolve(s_ > thr, np.ones(persist), "full")[:len(s_)] >= persist
            # false alarm episodes: alarms more than 30 days before failure (or on units that never fail)
            early = al & (tf_ - d_ > 30)
            fa += np.sum(np.diff(np.concatenate([[0], early.astype(int)])) == 1)
            if tf_ < ndays:
                late = al & (tf_ - d_ <= 30)
                warn.append(tf_ - d_[late][0] if late.any() else 0.0)
        return np.median(warn) if warn else 0, fa / unit_years, np.mean(np.array(warn) > 0) if warn else 0
    curves = {}
    for nme, sc, thrs in [("ml", score, np.quantile(score[test], np.linspace(0.5, 0.9995, 60))),
                          ("limit", X[:, 2], np.linspace(1.1, 3.5, 60))]:
        curves[nme] = np.array([evaluate(sc, t) for t in thrs])
    for nme in curves:
        c = curves[nme]
        ok = c[:, 1] <= 0.5
        best = c[ok][np.argmax(c[ok][:, 0])] if ok.any() else c[-1]
        print(f"eclss: {nme}: at <=0.5 false alarms per unit-year, median warning {best[0]:.0f} d, "
              f"failures warned {best[2]*100:.0f}% (false alarms {best[1]:.2f}/unit-yr)")
    print(f"eclss: test units 20 ({nfail} fail within {ndays} d), {unit_years:.1f} unit-years")

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.75), gridspec_kw=dict(width_ratios=[1.3, 1], wspace=0.45))
    ax = axs[0]
    cand = [u for u in range(40, 60) if 300 < tfail[unit == u][0] < ndays]
    u = cand[0]
    m = unit == u
    dd = day[m]
    ax.set_xlim(max(0, tfail[m][0] - 260), tfail[m][0] + 8)
    ax.plot(dd, X[m, 2], color=GREY, lw=0.5, label="Vibration (raw, changes with fan speed)")
    ax.plot(dd, X[m, 2] / (1 + 0.6 * X[m, 0]), color=BLUE, lw=0.8, label="Vibration, speed-normalised")
    ax.set_ylabel("Vibration (relative)")
    ax.set_xlabel("Day", labelpad=1)
    ax.axvline(tfail[m][0], color=RED, lw=1)
    ax.text(tfail[m][0] - 3, 3.3, "failure", color=RED, fontsize=6.6, ha="right")
    ax2 = ax.twinx()
    ax2.plot(dd, score[m], color=ORANGE, lw=0.9, label="Model risk of failure within 30 days")
    ax2.set_ylim(0, 1.6)
    ax2.set_yticks([0, 0.5, 1.0])
    ax2.set_ylabel("Risk score", color=ORANGE)
    ax2.grid(False)
    ax2.spines["right"].set_visible(True)
    ax.set_ylim(0.6, 4.8)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=6.0, loc="upper left")
    ax.set_title("One test fan before its failure", fontsize=8)
    panel_tag(ax, "a")
    ax = axs[1]
    for nme, col, lab in [("ml", ORANGE, "Gradient-boosted trees"), ("limit", GREY, "Fixed vibration limit")]:
        c = curves[nme]
        o = np.argsort(c[:, 1])
        ax.plot(c[o, 1], c[o, 0], "o-", ms=2.2, lw=1.1, color=col, label=lab)
    ax.set_xscale("symlog", linthresh=0.1)
    ax.set_xlim(0, 30)
    ax.set_xticks([0, 0.1, 1, 10])
    ax.set_xticklabels(["0", "0.1", "1", "10"])
    ax.set_xlabel("False alarms per fan-year", labelpad=1)
    ax.set_ylabel("Median warning (days)")
    ax.set_ylim(0, 32)
    ax.legend(fontsize=6.2, loc="lower right")
    ax.set_title("Warning time against false alarms", fontsize=8)
    panel_tag(ax, "b")
    foot(fig, "Synthetic fleet of 60 cabin fans over 1 100 days: Weibull failure times, wear that grows in the last weeks, "
              "fan-speed changes and cabin temperature as confounders. Model trained on 40 fans and tested on 20 others; "
              "an alarm needs three days in a row above threshold. Seed 5155.")
    fig.subplots_adjust(left=0.08, right=0.99, top=0.9, bottom=0.25)
    save(fig, "ch51_eclss")


if __name__ == "__main__":
    fns = [alerts, funnel, transit, vetting, photoz, transients, craters, unmixing, delay, eclss]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
