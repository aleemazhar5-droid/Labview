"""Figures for Chapter 48 - AI for Autonomy, Navigation and Robotics.

Most figures run real optimisation or machine-learning code with fixed random seeds on synthetic problems built from
simple physical models:
  autonomy   - ground response time and the autonomy level it implies for representative missions (model)
  arch       - block diagram of an autonomous spacecraft (diagram)
  sched      - observation scheduling: greedy vs randomised local search vs exact MILP (scipy/HiGHS)
  rover      - Mars rover distance per sol vs light-time for teleoperation, ground planning and autonomy (model)
  trn        - terrain-relative navigation: FFT/NCC landmark matching on synthetic terrain and error budget
  crater     - crater detection: template matching vs a numpy neural network, and the resulting position fix
  pnp        - PnP pose estimation (DLT + Levenberg-Marquardt + RANSAC) vs keypoint noise
  gfold      - fuel-optimal powered-descent divert by linear programming vs polynomial (E-) guidance
  rl         - policy search (cross-entropy method, numpy network) for a lunar landing vs a PD controller, with a
               runtime-assurance shield
Numbers quoted in the chapter are printed by each function.
"""
import os
import re
import sys
import textwrap
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch  # noqa: F401
from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap
from matplotlib.lines import Line2D
from scipy import ndimage as ndi

FOOT = 6.0


def panel_tag(ax, s, x=-0.02, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, weight="bold", ha="right", va="bottom", color=INK)


def foot(fig, text, y=0.01, width=150):
    text = re.sub(r"(\d) (?=\d{3}\b)", "\\1\u00a0", text)
    fig.text(0.99, y, "\n".join(textwrap.wrap(text, width)), ha="right", va="bottom", fontsize=FOOT, color=GREY,
             multialignment="right", linespacing=1.25)


def img_axes(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color("#9AA5B1")
        s.set_linewidth(0.6)


# ----------------------------------------------------------------------------------------------------------------
# 1. How much autonomy?  Ground response time model
# ----------------------------------------------------------------------------------------------------------------
MISSIONS = [
    # name, one-way light time [s], contact fraction, contact cycle [h]
    ("GEO comsat", 0.12, 1.00, 24.0),
    ("ISS (relay)", 0.25, 0.95, 1.53),
    ("LEO imager", 0.005, 0.08, 1.65),
    ("Lunar lander", 1.28, 1.00, 24.0),
    ("Asteroid approach", 40.0, 1.00, 24.0),
    ("Mars EDL", 11.4 * 60, 1.00, 24.0),
    ("Mars rover", 12.5 * 60, 0.06, 24.66),
    ("Jupiter orbiter", 43 * 60, 0.33, 24.0),
    ("Pluto flyby", 4.5 * 3600, 0.33, 24.0),
    ("Voyager 1", 23.5 * 3600, 0.25, 24.0),
]
T_DECIDE = 0.5 * 3600      # time for a ground team to analyse and approve a response [s]

CRITICAL = {"Lunar lander", "Asteroid approach", "Mars EDL"}
EVENTS = [
    # label, time constant [s], kind, applicable missions
    ("Equipment\nfault", 60.0, "F", None),
    ("Landing\nguidance", 60.0, "E", {"Lunar lander", "Asteroid approach", "Mars EDL"}),
    ("Driving\nhazard", 10.0, "E", {"Mars rover"}),
    ("Science\nevent", 2 * 3600.0, "E", {"LEO imager", "Mars rover", "Jupiter orbiter", "Pluto flyby",
                                                     "Asteroid approach"}),
    ("Plan\nchange", 6 * 3600.0, "E", {"LEO imager", "Mars rover", "Jupiter orbiter", "Pluto flyby",
                                                      "Voyager 1", "ISS (relay)", "GEO comsat"}),
    ("Collision\nwarning", 24 * 3600.0, "E", {"GEO comsat", "ISS (relay)", "LEO imager", "Jupiter orbiter"}),
]


def ground_time(tau, f, P_h):
    W = (1 - f) ** 2 * P_h * 3600 / 2.0        # mean wait for the next contact window
    return 2 * tau, 2 * W, T_DECIDE


def level_for(R, kind):
    if kind == "F":
        if R < 0.3:
            return "ground"
        return "F2" if R >= 30 else "F1"
    if R < 0.3:
        return "E2"
    return "E4" if R >= 10 else "E3"


def autonomy():
    names = [m[0] for m in MISSIONS]
    parts = np.array([ground_time(*m[1:]) for m in MISSIONS])
    total = parts.sum(1)
    n = len(names)
    fig = plt.figure(figsize=(7.0, 4.2))
    ax = fig.add_axes([0.13, 0.31, 0.30, 0.60])
    y = np.arange(n)[::-1]
    ax.barh(y, total - 1.0, left=1.0, color="#D5DEE7", height=0.66, edgecolor="none", label="Total")
    mk = [("D", SKY, "Round-trip light-time"), ("o", GOLD, "Waiting for contacts"),
          ("s", GREY, "Ground decision (30 min)")]
    for k, (m, c, lab) in enumerate(mk):
        v = parts[:, k]
        ok = v > 1.0
        ax.scatter(v[ok], y[ok], marker=m, s=16, color=c, zorder=3, label=lab, edgecolor="white", lw=0.4)
    ax.set_xscale("log")
    ax.set_xlim(1, 6e5)
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=7.4)
    ax.set_xticks([1, 60, 3600, 86400])
    ax.set_xticklabels(["1 s", "1 min", "1 h", "1 day"], fontsize=7.4)
    ax.set_xlabel("Time for the ground to respond", fontsize=8)
    ax.grid(axis="y", visible=False)
    for yy, t in zip(y, total):
        txt = f"{t/3600:.1f} h" if t >= 3600 else f"{t/60:.0f} min"
        ax.text(t * 1.3, yy, txt, va="center", fontsize=6.6, color=INK)
    ax.legend(loc="upper left", bbox_to_anchor=(-0.42, -0.16), fontsize=6.4, ncol=2, handlelength=1.2,
              columnspacing=0.8, handletextpad=0.4)
    panel_tag(ax, "a", x=-0.02)

    axm = fig.add_axes([0.53, 0.31, 0.46, 0.60])
    ev = [e[0] for e in EVENTS]
    M = np.full((n, len(ev)), np.nan)
    L = [["" for _ in ev] for _ in names]
    for i, (nm, tot) in enumerate(zip(names, total)):
        for j, (lab, tc, kind, app) in enumerate(EVENTS):
            if app is not None and nm not in app:
                continue
            R = tot / tc
            M[i, j] = np.log10(R)
            if kind == "F":
                L[i][j] = "ground" if R < 0.3 else ("F2" if (tot >= 6 * 3600 or nm in CRITICAL) else "F1")
            else:
                L[i][j] = "E2" if R < 0.3 else ("E4" if R >= 10 else "E3")
    cmap = LinearSegmentedColormap.from_list("aut", ["#DDEFE3", "#FBE7C6", "#F3B7A3", "#C8504F"])
    axm.imshow(np.ma.masked_invalid(M), cmap=cmap, vmin=-1.5, vmax=4, aspect="auto")
    for i in range(n):
        for j in range(len(ev)):
            if np.isnan(M[i, j]):
                axm.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fc="#F4F6F8", ec="white", lw=0.8))
                axm.text(j, i, "–", ha="center", va="center", fontsize=6.5, color="#B0B8C0")
            else:
                axm.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fc="none", ec="white", lw=0.8))
                axm.text(j, i, L[i][j], ha="center", va="center", fontsize=6.8, color=INK,
                         weight="bold" if L[i][j] in ("E4", "F2") else "normal")
    axm.set_xticks(range(len(ev)))
    axm.set_xticklabels(ev, fontsize=6.4)
    axm.xaxis.tick_top()
    axm.set_yticks(range(n))
    axm.set_yticklabels([])
    axm.set_ylim(n - 0.5, -0.5)
    axm.grid(False)
    for s_ in axm.spines.values():
        s_.set_visible(False)
    axm.tick_params(length=0)
    axm.text(-0.03, 1.10, "b", transform=axm.transAxes, fontsize=9, weight="bold", ha="right", va="bottom")
    for nm, tot in zip(names, total):
        print(f"  {nm:18s} ground response {tot/3600:7.2f} h")
    foot(fig, "Model: response = 2 × one-way light-time + 2 × mean wait for a contact, (1 − f)²P/2 for contact "
              "fraction f and cycle P, + 30 min for a ground decision. (b) compares it with each event's time "
              "constant (fault, guidance 1 min; driving hazard 10 s; science event 2 h; plan change 6 h; "
              "conjunction 1 day): ratio < 0.3 ground in the loop (E2); 0.3–10 onboard reactions (E3, F1); ≥ 10 "
              "onboard re-planning (E4); F2 where ground recovery takes ≥ 6 h or in critical phases. "
              "Illustrative heuristic, not an ECSS rule.", width=150)
    save(fig, "ch48_autonomy")


# ----------------------------------------------------------------------------------------------------------------
# 2. Architecture block diagram
# ----------------------------------------------------------------------------------------------------------------
def arch():
    fig, ax = canvas(7.0, 4.3, xlim=(0, 100), ylim=(0, 61))
    # ground
    box(ax, 1, 44, 17, 15, "", fc="#EEF3F8", ec=GREY, r=1.0)
    label(ax, 9.5, 56.8, "GROUND", fs=7.6, weight="bold", color=NAVY)
    label(ax, 9.5, 49.6, "Goals, priorities,\nmodels, rules;\nplan review,\nsoftware updates",
          fs=6.3, color=INK)
    box(ax, 1, 4, 17, 36, "", fc="#EEF3F8", ec=GREY, r=1.0)
    label(ax, 9.5, 37.6, "LINK", fs=7.6, weight="bold", color=NAVY)
    label(ax, 9.5, 23, "Light-time:\n0.1 s – 23 h\n\nContact:\nminutes to\ncontinuous\n\nUplink: goals,\nrules, models\n"
          "Downlink: events,\nsummaries,\nselected data", fs=6.3, color=INK)
    # spacecraft frame
    box(ax, 21, 1, 78, 59, "", fc="white", ec=NAVY, r=1.4, lw=1.2)
    label(ax, 60, 58, "SPACECRAFT", fs=7.8, weight="bold", color=NAVY)
    ax.add_patch(Circle((73.4, 58.0), 0.95, fc=GOLD, ec="white", lw=0.5, zorder=6))
    label(ax, 74.8, 58.0, "learned models in use or on trial", fs=6.2, ha="left", color=INK)
    # deliberative
    title_box(ax, 24, 43, 50, 12.5, "Deliberative layer (minutes – hours)",
              "Planner / scheduler: goals → timeline\n"
              "Science and event detection: what is worth doing\n"
              "Navigation planning: paths, manoeuvres", fc="#EAF1F7", hc=NAVY, fs=6.6, tfs=7.2)
    title_box(ax, 24, 26.5, 50, 13, "Executive layer (seconds – minutes)",
              "Sequencer or behaviour tree: runs the plan\n"
              "Resource and timing checks; plan repair requests\n"
              "Mode management; recovery procedures", fc="#EAF4EE", hc=GREEN, fs=6.6, tfs=7.2)
    title_box(ax, 24, 10.5, 50, 12.5, "Functional layer (milliseconds – seconds)",
              "Guidance, navigation and control loops\n"
              "Perception: cameras, lidar → features, pose, hazards\n"
              "Payload and device control", fc="#FDF1E6", hc=ORANGE, fs=6.6, tfs=7.2)
    box(ax, 24, 2.5, 50, 5, "Sensors and actuators", fc="#F3F6F9", ec=GREY, fs=6.8)
    # FDIR column
    title_box(ax, 77, 26.5, 20, 29, "FDIR",
              "Fault detection,\nisolation, recovery\n\nModel-based\ndiagnosis:\nwhich fault\nexplains the\nsymptoms?",
              fc="#F6EEF7", hc=VIOLET, fs=6.4, tfs=7.2)
    title_box(ax, 77, 2.5, 20, 20.5, "Runtime monitor",
              "Checks every\ncommand against\nsafety rules;\nswitches to a\nsafe fallback",
              fc="#FBEAEA", hc=RED, fs=6.4, tfs=7.2)
    # arrows within stack
    arrow(ax, (42, 43), (42, 39.5), color=NAVY, lw=1.0)
    label(ax, 43, 41.3, "plan", fs=6.2, ha="left", color=NAVY)
    arrow(ax, (58, 39.5), (58, 43), color=GREEN, lw=1.0)
    label(ax, 59, 41.3, "status, repair request", fs=6.2, ha="left", color=GREEN)
    arrow(ax, (42, 26.5), (42, 23), color=GREEN, lw=1.0)
    label(ax, 43, 24.8, "commands", fs=6.2, ha="left", color=GREEN)
    arrow(ax, (58, 23), (58, 26.5), color=ORANGE, lw=1.0)
    label(ax, 59, 24.8, "estimates, events", fs=6.2, ha="left", color=ORANGE)
    darrow(ax, (49, 10.5), (49, 7.5), color=GREY, lw=1.0)
    # where learned models are used today
    for (bx, by) in [(71.6, 15.6), (71.6, 46.4)]:
        ax.add_patch(Circle((bx, by), 0.95, fc=GOLD, ec="white", lw=0.5, zorder=6))
    ax.add_patch(Circle((26.0, 5.0 - 3.4), 0.0, fc="none"))
    ax.add_patch(Circle((79.2, 59.0 - 0.6), 0.0, fc="none"))
    # FDIR links
    arrow(ax, (74, 16), (77, 30), color=VIOLET, lw=0.9)
    arrow(ax, (77, 36), (74, 33), color=VIOLET, lw=0.9)
    arrow(ax, (74, 12.5), (77, 12.5), color=RED, lw=0.9)
    arrow(ax, (77, 8), (74, 5), color=RED, lw=0.9)
    # ground links
    darrow(ax, (18, 51), (24, 49.5), color=NAVY, lw=1.0)
    darrow(ax, (18, 30), (24, 32), color=NAVY, lw=1.0, ls="--")
    save(fig, "ch48_arch")


# ----------------------------------------------------------------------------------------------------------------
# 3. Observation scheduling: greedy, randomised local search (simulated annealing), exact MILP
# ----------------------------------------------------------------------------------------------------------------
ORBIT = 96.0          # min
GAP = 2.0             # min slew/settle time between observations
PASSES = [180.0, 540.0, 900.0, 1260.0]   # downlink passes (memory emptied)


def sched_instance(seed, K=45, horizon=1440.0):
    rng = np.random.default_rng(seed)
    ops = []
    for k in range(K):
        nop = rng.integers(1, 4)
        v = float(rng.integers(1, 11))
        rate = rng.choice([1.0, 3.0], p=[0.6, 0.4])     # multispectral / hyperspectral data units per minute
        for _ in range(nop):
            d = rng.uniform(3, 10)
            t0 = rng.uniform(0, horizon - d)
            ops.append((k, t0, t0 + d, v, d * 1.0, d * rate))
    ops = np.array(ops)
    return ops


def sched_constraints(ops, B=14.0, C=40.0, horizon=1440.0):
    """Build A x <= b for the MILP (and for feasibility checks)."""
    n = len(ops)
    rows, b = [], []
    tgt = ops[:, 0].astype(int)
    for k in np.unique(tgt):                       # one opportunity per target (visibility)
        r = np.zeros(n); r[tgt == k] = 1; rows.append(r); b.append(1.0)
    s_, e_ = ops[:, 1], ops[:, 2] + GAP
    for t in s_:                                    # interval-graph cliques: no overlap (one instrument)
        r = ((s_ <= t) & (e_ > t)).astype(float)
        if r.sum() > 1:
            rows.append(r); b.append(1.0)
    orb = (s_ // ORBIT).astype(int)
    for k in np.unique(orb):                       # payload energy per orbit
        r = np.where(orb == k, ops[:, 4], 0.0); rows.append(r); b.append(B)
    edges = [0.0] + PASSES + [horizon + 1]
    for a, c in zip(edges[:-1], edges[1:]):       # memory between downlink passes
        m = (ops[:, 2] > a) & (ops[:, 2] <= c)
        r = np.where(m, ops[:, 5], 0.0); rows.append(r); b.append(C)
    return np.array(rows), np.array(b)


def sched_greedy(ops, A, b):
    dens = ops[:, 3] / (ops[:, 4] / 14.0 + ops[:, 5] / 40.0 + 0.2)
    order = np.argsort(-dens)
    x = np.zeros(len(ops)); load = np.zeros(len(b))
    for i in order:
        if np.all(load + A[:, i] <= b + 1e-9):
            x[i] = 1; load += A[:, i]
    return x


def sched_anneal(ops, A, b, x0, iters=1500, seed=0):
    """Simulated annealing over selections: insert a random opportunity, repair violations by removing
    random conflicting ones, then refill greedily at random; Metropolis acceptance."""
    rng = np.random.default_rng(seed)
    v = ops[:, 3]
    x = x0.copy(); load = A @ x; val = v @ x
    best, bestv = x.copy(), val
    n = len(ops)
    Ab = A > 0
    T0 = 2.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.02
        i = rng.integers(n)
        if x[i] == 1:
            continue
        xn = x.copy(); xn[i] = 1; ln = load + A[:, i]
        viol = ln > b + 1e-9
        while viol.any():
            cand = np.where((xn == 1) & Ab[viol].any(0))[0]
            cand = cand[cand != i]
            if len(cand) == 0:
                break
            j = rng.choice(cand)
            xn[j] = 0; ln -= A[:, j]
            viol = ln > b + 1e-9
        if viol.any():
            continue
        while True:                                   # random greedy refill (vectorised feasibility test)
            fit = np.where((xn == 0) & np.all(A <= (b - ln)[:, None] + 1e-9, axis=0))[0]
            if len(fit) == 0:
                break
            j = rng.choice(fit)
            xn[j] = 1; ln += A[:, j]
        nv = v @ xn
        if nv >= val or rng.random() < np.exp((nv - val) / T):
            x, load, val = xn, ln, nv
            if val > bestv:
                best, bestv = x.copy(), val
    return best


def sched_milp(ops, A, b):
    from scipy.optimize import milp, LinearConstraint, Bounds
    res = milp(c=-ops[:, 3], constraints=LinearConstraint(A, -np.inf, b), integrality=np.ones(len(ops)),
               bounds=Bounds(0, 1), options={"time_limit": 60})
    return np.round(res.x)


def sched():
    rng_seeds = range(100, 140)
    rel_g, rel_a, tg, ta, tm = [], [], [], [], []
    for sd in rng_seeds:
        ops = sched_instance(sd)
        A, b = sched_constraints(ops)
        t0 = time.perf_counter(); xg = sched_greedy(ops, A, b); t1 = time.perf_counter()
        xa = sched_anneal(ops, A, b, xg, seed=sd); t2 = time.perf_counter()
        xm = sched_milp(ops, A, b); t3 = time.perf_counter()
        vg, va, vm = ops[:, 3] @ xg, ops[:, 3] @ xa, ops[:, 3] @ xm
        assert np.all(A @ xm <= b + 1e-6) and np.all(A @ xa <= b + 1e-6)
        rel_g.append(vg / vm); rel_a.append(va / vm)
        tg.append(t1 - t0); ta.append(t2 - t1); tm.append(t3 - t2)
    rel_g, rel_a = np.array(rel_g) * 100, np.array(rel_a) * 100
    print(f"  40 instances (~{len(sched_instance(100))} opportunities): greedy {rel_g.mean():.1f} % of optimum "
          f"(min {rel_g.min():.1f}), annealing {rel_a.mean():.1f} % (min {rel_a.min():.1f}), "
          f"optimal found by annealing in {np.sum(rel_a > 99.999)} of 40")
    print(f"  median times: greedy {np.median(tg)*1e3:.2f} ms, annealing {np.median(ta)*1e3:.0f} ms, "
          f"MILP {np.median(tm)*1e3:.0f} ms")
    # scaling
    sizes = [25, 50, 100, 200, 300]
    sc = {"g": [], "a": [], "m": [], "n": [], "rg": [], "ra": []}
    for K in sizes:
        tgl, tal, tml, rgl, ral = [], [], [], [], []
        for sd in range(2):
            ops = sched_instance(500 + sd, K=K)
            A, b = sched_constraints(ops)
            t0 = time.perf_counter(); xg = sched_greedy(ops, A, b); t1 = time.perf_counter()
            xa = sched_anneal(ops, A, b, xg, seed=sd); t2 = time.perf_counter()
            xm = sched_milp(ops, A, b); t3 = time.perf_counter()
            tgl.append(t1 - t0); tal.append(t2 - t1); tml.append(t3 - t2)
            vm = ops[:, 3] @ xm
            rgl.append(ops[:, 3] @ xg / vm); ral.append(ops[:, 3] @ xa / vm)
        sc["g"].append(np.median(tgl)); sc["a"].append(np.median(tal)); sc["m"].append(np.median(tml))
        sc["n"].append(len(ops)); sc["rg"].append(np.mean(rgl)); sc["ra"].append(np.mean(ral))
        print(f"  K={K:3d} n={len(ops):4d}: greedy {sc['g'][-1]*1e3:.1f} ms, anneal {sc['a'][-1]*1e3:.0f} ms, "
              f"MILP {sc['m'][-1]*1e3:.0f} ms; greedy {sc['rg'][-1]*100:.1f} %, anneal {sc['ra'][-1]*100:.1f} %")

    # example instance for the timeline
    ops = sched_instance(101)
    A, b = sched_constraints(ops)
    xg = sched_greedy(ops, A, b); xa = sched_anneal(ops, A, b, xg, seed=101); xm = sched_milp(ops, A, b)
    fig = plt.figure(figsize=(7.0, 4.9))
    ax = fig.add_axes([0.08, 0.60, 0.90, 0.35])
    w0, w1 = 0, 480
    rows = [("All opportunities", np.ones(len(ops)), "#C9D2DB"), ("Greedy", xg, ORANGE),
            ("Local search", xa, BLUE), ("Optimal (MILP)", xm, GREEN)]
    for r, (lab, x, c) in enumerate(rows):
        yy = 3 - r
        for i in np.where(x > 0.5)[0]:
            s0, e0 = ops[i, 1], ops[i, 2]
            if e0 < w0 or s0 > w1:
                continue
            if r == 0:
                # stack overlapping opportunities slightly
                ax.add_patch(Rectangle((s0, yy - 0.32 + 0.12 * (i % 6)), e0 - s0, 0.1, fc=c, ec="none"))
            else:
                ax.add_patch(Rectangle((s0, yy - 0.3), e0 - s0, 0.6, fc=c, ec="white", lw=0.4))
                ax.text((s0 + e0) / 2, yy, f"{ops[i,3]:.0f}", ha="center", va="center", fontsize=5.6,
                        color="white")
        if r > 0:
            tot = ops[:, 3] @ x
            ax.text(w1 + 4, yy, f"value {tot:.0f}", va="center", fontsize=6.8, color=c)
    for k in range(int(w1 // ORBIT) + 1):
        ax.axvline(k * ORBIT, color="#B8C3CE", lw=0.6, ls=":")
    for pz in PASSES:
        if pz <= w1:
            ax.axvline(pz, color=VIOLET, lw=1.0, ls="--")
            ax.text(pz + 2, 3.55, "downlink", fontsize=6.0, color=VIOLET, va="bottom")
    ax.set_xlim(w0, w1 + 40)
    ax.set_ylim(-0.6, 3.9)
    ax.set_yticks([3, 2, 1, 0])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7)
    ax.set_xticks(np.arange(0, w1 + 1, 60))
    ax.set_xticklabels([f"{h}" for h in range(0, w1 // 60 + 1)], fontsize=7)
    ax.set_xlabel("Time (h); dotted lines are orbit boundaries (energy budget per orbit)", fontsize=7.4)
    ax.grid(False)
    panel_tag(ax, "a")
    print(f"  example instance 101 (24 h): greedy {ops[:,3]@xg:.0f}, local search {ops[:,3]@xa:.0f}, "
          f"MILP {ops[:,3]@xm:.0f}; n={len(ops)} opportunities, {len(b)} constraints")

    ax2 = fig.add_axes([0.08, 0.20, 0.36, 0.29])
    bp = ax2.boxplot([rel_g, rel_a], orientation="horizontal", widths=0.5, patch_artist=True, showfliers=True,
                     medianprops=dict(color=INK, lw=1.0), flierprops=dict(marker="o", ms=2.5, mec=GREY))
    for patch, c in zip(bp["boxes"], [ORANGE, BLUE]):
        patch.set_facecolor(c); patch.set_alpha(0.75); patch.set_edgecolor(INK); patch.set_linewidth(0.6)
    ax2.set_yticks([1, 2]); ax2.set_yticklabels(["Greedy", "Local\nsearch"], fontsize=7)
    ax2.set_xlabel("Value achieved (% of optimum), 40 problems", fontsize=7.4)
    ax2.set_xlim(min(rel_g.min(), 80) - 2, 101)
    ax2.axvline(100, color=GREEN, lw=1.0)
    ax2.grid(axis="y", visible=False)
    panel_tag(ax2, "b")

    ax3 = fig.add_axes([0.58, 0.20, 0.40, 0.29])
    n_ = np.array(sc["n"])
    ax3.plot(n_, np.array(sc["g"]) * 1e3, "o-", color=ORANGE, ms=3.5, label="Greedy")
    ax3.plot(n_, np.array(sc["a"]) * 1e3, "s-", color=BLUE, ms=3.5, label="Local search (1 500 moves)")
    ax3.plot(n_, np.array(sc["m"]) * 1e3, "D-", color=GREEN, ms=3.5, label="MILP (HiGHS)")
    ax3.set_xscale("log"); ax3.set_yscale("log")
    ax3.set_xticks([50, 100, 200, 500]); ax3.set_xticklabels(["50", "100", "200", "500"])
    ax3.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax3.set_xlabel("Number of observation opportunities", fontsize=7.4)
    ax3.set_ylabel("Run time on a laptop (ms)", fontsize=7.4)
    ax3.legend(fontsize=6.3, loc="upper left")
    panel_tag(ax3, "c")
    foot(fig, "Synthetic day of 45 targets with 1–3 visibility windows each (3–10 min), values 1–10, one "
              "instrument with 2 min slews, payload energy ≤ 14 units per 96-min orbit, memory ≤ 40 units between "
              "four downlink passes. Exact solution by mixed-integer linear programming (scipy/HiGHS). Flight "
              "processors are 100–1 000 times slower than a laptop.", width=160)
    save(fig, "ch48_sched")

# ----------------------------------------------------------------------------------------------------------------
# 4. Rover: distance per sol vs light-time
# ----------------------------------------------------------------------------------------------------------------
def rover_model(tau, T_d=3.5 * 3600, step=10.0, v_drive=0.042, t_op=60.0, d_vis=40.0, v_sg=20.0, v_en=110.0):
    teleop = T_d * step / (step / v_drive + 2 * tau + t_op)
    t_blind = d_vis / v_drive
    ground = np.full_like(tau, d_vis)
    stopgo = d_vis + v_sg / 3600 * (T_d - t_blind)
    enav = d_vis + v_en / 3600 * (T_d - t_blind)
    return teleop, ground, np.full_like(tau, stopgo), np.full_like(tau, enav)


def rover():
    tau = np.logspace(-1, np.log10(4000), 300)
    tel, gr, sg, en = rover_model(tau)
    fig = plt.figure(figsize=(7.0, 3.2))
    ax = fig.add_axes([0.08, 0.26, 0.52, 0.66])
    ax.axvspan(182, 1342, color="#F7E3D4", lw=0)
    ax.text(np.sqrt(182 * 1342), 520, "Mars\n3–22 min", ha="center", va="top", fontsize=6.8, color=ORANGE)
    ax.axvline(1.28, color=GREY, lw=0.8, ls=":")
    ax.text(1.4, 520, "Moon\n1.3 s", ha="left", va="top", fontsize=6.8, color=GREY)
    ax.plot(tau, tel, color=RED, label="Teleoperation, continuous link (move and wait)")
    ax.plot(tau, gr, color=GREY, label="Ground-planned drive, once per sol")
    ax.plot(tau, sg, color=GOLD, label="+ autonomous stop-and-go (20 m/h)")
    ax.plot(tau, en, color=BLUE, label="+ thinking while driving (110 m/h)")
    ax.set_xscale("log")
    ax.set_xlim(0.1, 4000)
    ax.set_ylim(0, 540)
    ax.set_xlabel("One-way light-time (s)", fontsize=8)
    ax.set_ylabel("Distance per sol (m)", fontsize=8)
    ax.legend(fontsize=6.3, loc="center left", bbox_to_anchor=(0.0, 0.47))
    panel_tag(ax, "a")
    for t in [1.28, 4 * 60, 12.5 * 60, 22 * 60]:
        tl, g_, s_, e_ = rover_model(np.array([t]))
        print(f"  tau={t:7.1f} s: teleop {tl[0]:5.0f} m, ground {g_[0]:.0f} m, stop-go {s_[0]:.0f} m, "
              f"ENav {e_[0]:.0f} m")
    ax2 = fig.add_axes([0.70, 0.26, 0.28, 0.66])
    rov = ["Spirit,\nOpportunity", "Curiosity", "Perseverance"]
    share = [5, 6.2, 90]
    bars = ax2.bar(range(3), share, color=[GREY, GOLD, BLUE], width=0.6)
    for i, v in enumerate(share):
        ax2.text(i, v + 2, ("> 90 %" if i == 2 else f"≈ {v:g} %"), ha="center", va="bottom", fontsize=7)
    ax2.set_xticks(range(3)); ax2.set_xticklabels(rov, fontsize=6.8)
    ax2.set_ylim(0, 105)
    ax2.set_ylabel("Share of distance driven autonomously (%)", fontsize=7.4)
    ax2.grid(axis="x", visible=False)
    panel_tag(ax2, "b")
    foot(fig, "(a) Model: 3.5 h drive window per sol; top speed 4.2 cm/s; teleoperation in 10 m steps, each "
              "waiting a round trip plus 60 s of operator time; ground plans 40 m blind per sol; autonomous "
              "average speeds assumed. (b) NASA and IEEE Spectrum figures to 2024–26.", width=150)
    save(fig, "ch48_rover")

# ----------------------------------------------------------------------------------------------------------------
# 5. Terrain-relative navigation: landmark matching on synthetic terrain
# ----------------------------------------------------------------------------------------------------------------
def fractal_dem(n, dx, beta=3.2, rms=8.0, seed=0):
    rng = np.random.default_rng(seed)
    kx = np.fft.fftfreq(n, d=dx)
    k = np.sqrt(kx[:, None] ** 2 + kx[None, :] ** 2)
    k[0, 0] = 1.0
    amp = k ** (-beta / 2)
    amp[0, 0] = 0
    ph = np.exp(2j * np.pi * rng.random((n, n)))
    z = np.real(np.fft.ifft2(amp * ph))
    return z / z.std() * rms


def add_craters(z, dx, ncr, rmin, rmax, seed=1, alpha=2.0, fresh=(0.2, 1.0)):
    """Add bowl craters with raised rims; radii from a power law. Returns DEM and crater list (x, y, R in px)."""
    rng = np.random.default_rng(seed)
    n = z.shape[0]
    u = rng.random(ncr)
    R = (rmin ** (1 - alpha) + u * (rmax ** (1 - alpha) - rmin ** (1 - alpha))) ** (1 / (1 - alpha))   # metres
    cr = []
    for Rm in R:
        Rp = Rm / dx
        cx, cy = rng.uniform(0, n), rng.uniform(0, n)
        fr = rng.uniform(*fresh)                    # degradation: 1 fresh, small = eroded
        h = 0.2 * Rm * fr
        w = int(3 * Rp) + 2
        x0, x1 = int(max(cx - w, 0)), int(min(cx + w, n))
        y0, y1 = int(max(cy - w, 0)), int(min(cy + w, n))
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1]
        r = np.hypot(xx - cx, yy - cy) / Rp
        prof = np.where(r < 1, h * (r ** 2 - 1) + 0.25 * h, 0.25 * h * np.exp(-(r - 1) / 0.35))
        z[y0:y1, x0:x1] += prof
        cr.append((cx, cy, Rp, fr))
    return z, np.array(cr)


def shade(z, dx, el_deg, az_deg, albedo=None):
    gy, gx = np.gradient(z, dx)
    nrm = np.sqrt(gx ** 2 + gy ** 2 + 1)
    el, az = np.radians(el_deg), np.radians(az_deg)
    sx, sy, sz = np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)
    I = np.clip((-gx * sx - gy * sy + sz) / nrm, 0, None)
    if albedo is not None:
        I = I * albedo
    return I


def block(img, f):
    n = img.shape[0] // f * f
    return img[:n, :n].reshape(n // f, f, n // f, f).mean(axis=(1, 3))


def ncc_search(tpl, win):
    from numpy.lib.stride_tricks import sliding_window_view
    T = tpl.shape[0]
    V = sliding_window_view(win, (T, T))
    t = (tpl - tpl.mean()) / (tpl.std() + 1e-9)
    Vm = V.mean(axis=(2, 3), keepdims=True)
    Vs = V.std(axis=(2, 3), keepdims=True) + 1e-9
    C = np.einsum("ijkl,kl->ij", (V - Vm) / Vs, t) / (T * T)
    i, j = np.unravel_index(np.argmax(C), C.shape)
    # sub-pixel parabola fit
    def sub(a, b, c):
        d = a - 2 * b + c
        return 0.0 if abs(d) < 1e-12 else 0.5 * (a - c) / d
    di = sub(C[i - 1, j], C[i, j], C[i + 1, j]) if 0 < i < C.shape[0] - 1 else 0.0
    dj = sub(C[i, j - 1], C[i, j], C[i, j + 1]) if 0 < j < C.shape[1] - 1 else 0.0
    return i + di, j + dj, C


def trn():
    dx = 1.5
    n = 2048
    rng = np.random.default_rng(7)
    z = fractal_dem(n, dx, seed=3)
    z, _ = add_craters(z, dx, 1200, 5, 260, seed=4)
    alb = 1 + 0.08 * ndi.gaussian_filter(rng.standard_normal((n, n)), 6) / 0.02
    alb = np.clip(alb, 0.7, 1.3)
    map_img = shade(z, dx, 25, 200, alb)
    T, W = 32, 20
    gsds = [3.0, 6.0, 12.0]
    dazs = [0, 20, 40, 60, 90]
    res = {}
    maps = {g: block(map_img, int(round(g / dx))) for g in gsds}
    for daz in dazs:
        des = shade(z, dx, 25 + 0.1 * daz, 200 + daz, alb)
        for g in gsds:
            f = int(round(g / dx))
            M = maps[g]
            errs = []
            for trial in range(40):
                sh = rng.integers(0, f, size=2)
                D = block(np.roll(des, (-sh[0], -sh[1]), axis=(0, 1)), f)
                D = D + rng.normal(0, 0.03, D.shape)
                m = M.shape[0]
                ci, cj = rng.integers(W + T, m - W - 2 * T, size=2)
                tpl = D[ci:ci + T, cj:cj + T]
                win = M[ci - W:ci + T + W, cj - W:cj + T + W]
                pi, pj, _ = ncc_search(tpl, win)
                ei = (pi - W) - sh[0] / f
                ej = (pj - W) - sh[1] / f
                errs.append(np.hypot(ei, ej) * g)
            errs = np.array(errs)
            res[(g, daz)] = errs
    for g in gsds:
        for daz in dazs:
            errs = res[(g, daz)]
            print(f"  GSD {g:4.1f} m, sun azimuth change {daz:2d} deg: median {np.median(errs):6.2f} m, "
                  f"90th pct {np.percentile(errs, 90):7.1f} m, fail(>3 px) {np.mean(errs > 3 * g)*100:4.0f} %")
    fig = plt.figure(figsize=(7.0, 3.3))
    # (a) map tile and template
    f = 4
    M = block(map_img, f)
    D = block(shade(z, dx, 25 + 0.1 * 60, 260, alb), f)
    ci, cj = 150, 210
    axa = fig.add_axes([0.015, 0.40, 0.19, 0.50])
    view = M[ci - W - 10:ci + T + W + 10, cj - W - 10:cj + T + W + 10]
    axa.imshow(view, cmap="gray", vmin=0, vmax=np.percentile(view, 99.5))
    axa.add_patch(Rectangle((W + 10 - 0.5, W + 10 - 0.5), T, T, fc="none", ec=ORANGE, lw=1.2))
    axa.add_patch(Rectangle((10 - 0.5, 10 - 0.5), T + 2 * W, T + 2 * W, fc="none", ec=SKY, lw=1.0, ls="--"))
    img_axes(axa)
    axa.set_title("Map, 6 m pixels", fontsize=6.8, pad=2)
    axa.text(0.5, -0.04, "blue: search window\norange: true position", transform=axa.transAxes, fontsize=5.9,
             ha="center", va="top", color=INK)
    axi = fig.add_axes([0.215, 0.52, 0.10, 0.27])
    axi.imshow(D[ci:ci + T, cj:cj + T], cmap="gray")
    img_axes(axi)
    for sp in axi.spines.values():
        sp.set_color(ORANGE); sp.set_linewidth(1.2)
    axi.set_title("Descent template\n(sun moved 60°)", fontsize=6.2, pad=2)
    panel_tag(axa, "a", x=0.02)
    # (b) error vs sun change
    axb = fig.add_axes([0.40, 0.28, 0.26, 0.62])
    for g, c in zip(gsds, [GREEN, BLUE, VIOLET]):
        med = [np.median(res[(g, d)]) for d in dazs]
        p90 = [np.percentile(res[(g, d)], 90) for d in dazs]
        axb.plot(dazs, med, "o-", color=c, ms=3.5, label=f"{g:g} m map")
        axb.plot(dazs, p90, "--", color=c, lw=0.9)
    axb.set_yscale("log")
    axb.set_xlabel("Sun azimuth change, map → descent (°)", fontsize=7.0)
    axb.set_ylabel("Landmark position error (m)", fontsize=7.4)
    axb.set_xticks(dazs)
    axb.legend(fontsize=6.3, loc="upper left", title="median (—), 90 % (- -)", title_fontsize=6.0)
    panel_tag(axb, "b")
    # (c) error budget vs altitude
    axc = fig.add_axes([0.74, 0.28, 0.25, 0.62])
    h = np.linspace(500, 6000, 100)
    s_lm = np.median(res[(6.0, 20)])
    N = 15
    for s_map, att, c, lab in [(3.0, 0.03, BLUE, "map tie 3 m, attitude 0.03°"),
                               (10.0, 0.1, RED, "map tie 10 m, attitude 0.1°")]:
        tot = np.sqrt(s_lm ** 2 / N + s_map ** 2 + (h * np.radians(att)) ** 2)
        axc.plot(h / 1000, tot, color=c, label=lab)
        print(f"  budget {lab}: at 4 km {np.sqrt(s_lm**2/N + s_map**2 + (4000*np.radians(att))**2):.2f} m; "
              f"landmark term {s_lm/np.sqrt(N):.2f} m (s_lm={s_lm:.2f} m), attitude term "
              f"{4000*np.radians(att):.2f} m")
    axc.axhline(s_lm / np.sqrt(N), color=GREEN, ls=":", lw=1.0, label=f"{N} landmarks alone")
    axc.set_xlabel("Altitude (km)", fontsize=7.4)
    axc.set_ylabel("Position-fix error, 1σ (m)", fontsize=7.4)
    axc.set_ylim(0, 16)
    axc.legend(fontsize=5.9, loc="upper left")
    panel_tag(axc, "c")
    foot(fig, "Synthetic 3 km terrain (fractal relief, 1 200 craters, albedo noise) rendered at 25° sun elevation; "
              "32 × 32-pixel descent templates matched by normalised cross-correlation in a ±20-pixel window, "
              "40 trials per point. (c) Root-sum-square of landmark error/√N (6 m map, 20° sun change), map "
              "registration and attitude-knowledge error projected over the altitude.", width=150)
    save(fig, "ch48_trn")

# ----------------------------------------------------------------------------------------------------------------
# 6. Crater detection: template matching vs a small neural network; position fix from crater matching
# ----------------------------------------------------------------------------------------------------------------
CR_BINS = [4.0, 6.0, 9.0, 13.5]      # crater radius bins in pixels (5 m pixels)
CR_WIN = 2.6                         # window size / radius
CR_P = 16                            # network input size (16 x 16)


class MLP:
    """Two-layer perceptron (ReLU hidden layer, sigmoid output) trained with Adam on binary cross-entropy."""

    def __init__(self, n_in, hidden=48, seed=0):
        rng = np.random.default_rng(seed)
        self.W1 = rng.normal(0, np.sqrt(2 / n_in), (n_in, hidden)); self.b1 = np.zeros(hidden)
        self.W2 = rng.normal(0, np.sqrt(1 / hidden), (hidden, 1)); self.b2 = np.zeros(1)
        self.params = [self.W1, self.b1, self.W2, self.b2]
        self.m = [np.zeros_like(q) for q in self.params]; self.v = [np.zeros_like(q) for q in self.params]
        self.t = 0

    def forward(self, X):
        H = np.maximum(X @ self.W1 + self.b1, 0)
        return H, 1 / (1 + np.exp(-(H @ self.W2 + self.b2)[:, 0]))

    def predict(self, X, batch=50000):
        out = np.empty(len(X))
        for i in range(0, len(X), batch):
            out[i:i + batch] = self.forward(X[i:i + batch])[1]
        return out

    def fit(self, X, y, epochs=25, lr=2e-3, batch=256, wd=1e-4, seed=0):
        rng = np.random.default_rng(seed)
        hist = []
        for ep in range(epochs):
            idx = rng.permutation(len(X))
            tot = 0.0
            for i in range(0, len(X), batch):
                b = idx[i:i + batch]
                H, p = self.forward(X[b])
                p = np.clip(p, 1e-7, 1 - 1e-7)
                tot += -np.sum(y[b] * np.log(p) + (1 - y[b]) * np.log(1 - p))
                d = (p - y[b])[:, None] / len(b)
                gW2 = H.T @ d + wd * self.W2; gb2 = d.sum(0)
                dH = (d @ self.W2.T) * (H > 0)
                gW1 = X[b].T @ dH + wd * self.W1; gb1 = dH.sum(0)
                self.t += 1
                for k, g in enumerate([gW1, gb1, gW2, gb2]):
                    self.m[k] = 0.9 * self.m[k] + 0.1 * g
                    self.v[k] = 0.999 * self.v[k] + 0.001 * g * g
                    mh = self.m[k] / (1 - 0.9 ** self.t); vh = self.v[k] / (1 - 0.999 ** self.t)
                    self.params[k] -= lr * mh / (np.sqrt(vh) + 1e-8)
            hist.append(tot / len(X))
        return hist


def crater_scene(seed, n=400, dx=5.0, ncr=170):
    z = fractal_dem(n, dx, beta=3.4, rms=3.0, seed=seed)
    z, cr = add_craters(z, dx, ncr, 12, 110, seed=seed + 1000, alpha=2.2, fresh=(0.15, 1.0))
    rng = np.random.default_rng(seed + 7)
    alb = np.clip(1 + 0.12 * ndi.gaussian_filter(rng.standard_normal((n, n)), 4) / 0.05, 0.6, 1.4)
    return z, cr, alb


def render_scene(z, alb, el, az, dx=5.0, seed=0, noise=0.025):
    rng = np.random.default_rng(seed)
    I = shade(z, dx, el, az, alb)
    I = I + rng.normal(0, noise, I.shape)
    return I


def std_patches(P):
    P = P.reshape(len(P), -1)
    return (P - P.mean(1, keepdims=True)) / (P.std(1, keepdims=True) + 1e-3)


def crater_windows(I, R, stride=2):
    from numpy.lib.stride_tricks import sliding_window_view
    s = CR_P / (CR_WIN * R)
    Z = ndi.zoom(I, s, order=1)
    V = sliding_window_view(Z, (CR_P, CR_P))[::stride, ::stride]
    gi, gj = V.shape[:2]
    X = std_patches(V.reshape(gi * gj, CR_P, CR_P))
    ci = (np.arange(gi) * stride + CR_P / 2 - 0.5) / s
    cj = (np.arange(gj) * stride + CR_P / 2 - 0.5) / s
    return X, ci, cj, (gi, gj)


def crater_train_set(n_img=10, seed=0):
    rng = np.random.default_rng(seed)
    Xs, ys = [], []
    for k in range(n_img):
        z, cr, alb = crater_scene(200 + k)
        el, az = rng.uniform(8, 60), rng.uniform(0, 360)
        I = render_scene(z, alb, el, az, seed=300 + k)
        for R in CR_BINS:
            s = CR_P / (CR_WIN * R)
            Z = ndi.zoom(I, s, order=1)
            m = Z.shape[0]
            inb = cr[(cr[:, 2] > R / 1.25) & (cr[:, 2] < R * 1.25)]
            pos = []
            for cx, cy, Rp, fr in inb:
                for _ in range(3):
                    jx = cx * s + rng.normal(0, 0.12 * Rp * s)
                    jy = cy * s + rng.normal(0, 0.12 * Rp * s)
                    i0, j0 = int(round(jy - CR_P / 2 + 0.5)), int(round(jx - CR_P / 2 + 0.5))
                    if 0 <= i0 < m - CR_P and 0 <= j0 < m - CR_P:
                        pos.append(Z[i0:i0 + CR_P, j0:j0 + CR_P])
            neg = []
            while len(neg) < 8 * max(len(pos), 20):
                i0, j0 = rng.integers(0, m - CR_P, size=2)
                yc, xc = (i0 + CR_P / 2) / s, (j0 + CR_P / 2) / s
                d = np.hypot(cr[:, 0] - xc, cr[:, 1] - yc)
                close = (d < 0.45 * cr[:, 2]) & (cr[:, 2] > R / 1.25) & (cr[:, 2] < R * 1.25)
                if not close.any():
                    neg.append(Z[i0:i0 + CR_P, j0:j0 + CR_P])
            Xs += [std_patches(np.array(pos)), std_patches(np.array(neg))]
            ys += [np.ones(len(pos)), np.zeros(len(neg))]
    X = np.vstack(Xs); y = np.concatenate(ys)
    # rotation augmentation by 90-degree turns would change the shading direction; keep as rendered
    return X, y


def crater_template(R, el, az, dx=5.0):
    w = int(np.ceil(CR_WIN * R / 2))
    n = 2 * w + 1
    z = np.zeros((n, n))
    yy, xx = np.mgrid[0:n, 0:n]
    r = np.hypot(xx - w, yy - w) / R
    h = 0.2 * R * dx * 0.7
    z += np.where(r < 1, h * (r ** 2 - 1) + 0.25 * h, 0.25 * h * np.exp(-(r - 1) / 0.35))
    return shade(z, dx, el, az)


def ncc_map(I, t):
    from scipy.signal import fftconvolve
    h = t.shape[0]
    tn = (t - t.mean()) / (t.std() + 1e-9) / t.size
    num = fftconvolve(I, tn[::-1, ::-1], mode="same")
    mu = ndi.uniform_filter(I, h)
    var = np.clip(ndi.uniform_filter(I * I, h) - mu * mu, 1e-9, None)
    return num / np.sqrt(var)


def peaks(S, size, thr):
    mx = ndi.maximum_filter(S, size=size)
    ii, jj = np.where((S == mx) & (S > thr))
    return ii, jj, S[ii, jj]


def nms(dets):
    if not len(dets):
        return np.zeros((0, 4))
    d = np.array(dets, float)
    d = d[np.argsort(-d[:, 3])]
    keep = []
    for k in range(len(d)):
        if keep:
            kk = d[keep]
            if np.any(np.hypot(kk[:, 0] - d[k, 0], kk[:, 1] - d[k, 1]) <= 0.7 * np.maximum(kk[:, 2], d[k, 2])):
                continue
        keep.append(k)
    return d[keep]


def subpix(S, i, j):
    def sub(a, b, c):
        den = a - 2 * b + c
        return 0.0 if abs(den) < 1e-12 else float(np.clip(0.5 * (a - c) / den, -0.5, 0.5))
    di = sub(S[i - 1, j], S[i, j], S[i + 1, j]) if 0 < i < S.shape[0] - 1 else 0.0
    dj = sub(S[i, j - 1], S[i, j], S[i, j + 1]) if 0 < j < S.shape[1] - 1 else 0.0
    return i + di, j + dj


def detect_template(I, el, az, thr=0.25):
    dets = []
    for R in CR_BINS:
        S = ncc_map(I, crater_template(R, el, az))
        ii, jj, v = peaks(S, int(1.2 * R), thr)
        for i, j, val in zip(ii, jj, v):
            fi, fj = subpix(S, i, j)
            dets.append((fj, fi, R, val))
    return nms(dets)


def detect_net(I, net, thr=0.3, stride=2):
    dets = []
    for R in CR_BINS:
        X, ci, cj, shp = crater_windows(I, R, stride=stride)
        P = net.predict(X).reshape(shp)
        s = CR_P / (CR_WIN * R)
        ii, jj, v = peaks(P, max(3, int(1.2 * R * s / stride)), thr)
        for i, j, val in zip(ii, jj, v):
            fi, fj = subpix(P, i, j)
            dets.append(((fj * stride + CR_P / 2 - 0.5) / s, (fi * stride + CR_P / 2 - 0.5) / s, R, val))
    return nms(dets)


def match_eval(dets, cr, n=400):
    """Greedy matching by score; returns sorted scores, TP flags and number of reference craters."""
    ref = cr[(cr[:, 2] >= CR_BINS[0] / 1.25) & (cr[:, 2] <= CR_BINS[-1] * 1.25)
             & (cr[:, 0] > 8) & (cr[:, 0] < n - 8) & (cr[:, 1] > 8) & (cr[:, 1] < n - 8)]
    used = np.zeros(len(ref), bool)
    tp = []
    for d in dets[np.argsort(-dets[:, 3])] if len(dets) else []:
        dd = np.hypot(ref[:, 0] - d[0], ref[:, 1] - d[1])
        ok = (dd < 0.5 * ref[:, 2] + 1.0) & (ref[:, 2] / d[2] < 1.6) & (d[2] / ref[:, 2] < 1.6) & ~used
        if ok.any():
            k = np.argmin(np.where(ok, dd, np.inf)); used[k] = True; tp.append(1)
        else:
            tp.append(0)
    sc = np.sort(dets[:, 3])[::-1] if len(dets) else np.array([])
    return sc, np.array(tp), len(ref)


def pr_curve(tp, nref):
    ctp = np.cumsum(tp); cfp = np.cumsum(1 - tp)
    prec = ctp / np.maximum(ctp + cfp, 1); rec = ctp / nref
    # average precision (all-point interpolation)
    pm = np.maximum.accumulate(prec[::-1])[::-1]
    ap = np.sum(np.diff(np.concatenate([[0], rec])) * pm)
    return rec, prec, ap


def position_fix(dets, cr, top=40, prior=40, rng=None):
    """Estimate the image offset from crater matches by RANSAC over single-pair hypotheses."""
    if len(dets) < 3:
        return np.array([np.nan, np.nan])
    d = dets[np.argsort(-dets[:, 3])][:top]
    cat = cr[(cr[:, 2] >= 3.2) & (cr[:, 2] <= 17)]
    best, bestn = None, 0
    for di in d:
        cand = cat[(np.abs(cat[:, 0] - di[0]) < prior) & (np.abs(cat[:, 1] - di[1]) < prior)
                   & (cat[:, 2] / di[2] < 1.5) & (di[2] / cat[:, 2] < 1.5)]
        for c in cand:
            off = c[:2] - di[:2]
            moved = d[:, :2] + off
            dist = np.min(np.hypot(moved[:, 0, None] - cat[None, :, 0], moved[:, 1, None] - cat[None, :, 1]), axis=1)
            inl = dist < np.maximum(0.4 * d[:, 2], 2.0)
            if inl.sum() > bestn:
                bestn, best = inl.sum(), (off, inl)
    if best is None or bestn < 3:
        return np.array([np.nan, np.nan])
    off, inl = best
    moved = d[inl, :2] + off
    j = np.argmin(np.hypot(moved[:, 0, None] - cat[None, :, 0], moved[:, 1, None] - cat[None, :, 1]), axis=1)
    return np.mean(cat[j, :2] - d[inl, :2], axis=0)


def crater():
    t0 = time.time()
    X, y = crater_train_set()
    net = MLP(X.shape[1], hidden=64, seed=1)
    hist = net.fit(X, y, epochs=30)
    print(f"  training patches {len(X)} ({int(y.sum())} craters), {X.shape[1]*64+64+65} weights, "
          f"final loss {hist[-1]:.3f}, {time.time()-t0:.1f} s")
    els = [10, 25, 45, 65]
    az = 250.0
    res = {}
    rng = np.random.default_rng(5)
    for el in els:
        for kind in ("tm", "nn"):
            res[(el, kind)] = {"tp": [], "nref": 0, "err": []}
        for k in range(3):
            z, cr, alb = crater_scene(900 + k)
            I = render_scene(z, alb, el, az, seed=950 + k)
            for kind in ("tm", "nn"):
                dets = detect_template(I, el, az) if kind == "tm" else detect_net(I, net)
                sc, tp, nref = match_eval(dets, cr)
                r = res[(el, kind)]
                r["tp"].append((sc, tp)); r["nref"] += nref
                off = position_fix(dets, cr, rng=rng)
                r["err"].append(np.hypot(*off) * 5.0 if np.all(np.isfinite(off)) else np.inf)
                if el == 25 and k == 0:
                    res[("example", kind)] = (I, dets, cr)
    for el in els:
        for kind in ("tm", "nn"):
            r = res[(el, kind)]
            sc = np.concatenate([a for a, b in r["tp"]]); tp = np.concatenate([b for a, b in r["tp"]])
            o = np.argsort(-sc)
            rec, prec, ap = pr_curve(tp[o], r["nref"])
            r["rec"], r["prec"], r["ap"] = rec, prec, ap
            e = np.array(r["err"])
            print(f"  sun {el:2d} deg {kind}: AP {ap:.2f}, max recall {rec[-1]:.2f}, "
                  f"position-fix errors {np.round(e, 1)} m")
    fig = plt.figure(figsize=(7.0, 4.3))
    axa = fig.add_axes([0.01, 0.14, 0.38, 0.79])
    I, dets, cr = res[("example", "nn")]
    axa.imshow(I, cmap="gray", vmin=0, vmax=np.percentile(I, 99.5))
    sc, tp, nref = match_eval(dets, cr)
    dd = dets[np.argsort(-dets[:, 3])]
    ntp = 0
    nshow = 100
    for (x, y_, R, v), t in list(zip(dd, tp))[:nshow]:
        ntp += t
        axa.add_patch(Circle((x, y_), R, fc="none", ec=GREEN if t else RED, lw=0.9))
    print(f"  example (sun 25): top {nshow} of {len(dd)} network detections, {ntp} correct; {nref} catalogued")
    img_axes(axa)
    axa.set_xlim(0, 300); axa.set_ylim(300, 0)
    axa.set_title("Network: 100 highest-scoring detections, sun 25°", fontsize=7.0, pad=3)
    axa.text(0.0, -0.02, "green: matches a catalogued crater;  red: no match", transform=axa.transAxes,
             fontsize=6.2, va="top")
    panel_tag(axa, "a", x=0.04)
    axb = fig.add_axes([0.47, 0.58, 0.23, 0.35])
    cols = {10: RED, 25: ORANGE, 45: BLUE, 65: GREEN}
    for el in [10, 25, 45]:
        for kind, ls in (("tm", "--"), ("nn", "-")):
            r = res[(el, kind)]
            axb.plot(r["rec"], r["prec"], ls=ls, color=cols[el], lw=1.1)
    axb.set_xlim(0, 1); axb.set_ylim(0, 1.02)
    axb.set_xlabel("Recall", fontsize=7.2); axb.set_ylabel("Precision", fontsize=7.2)
    hand = [Line2D([], [], color=cols[e], lw=1.4, label=f"sun {e}°") for e in [10, 25, 45]]
    hand += [Line2D([], [], color=GREY, ls="-", label="network"), Line2D([], [], color=GREY, ls="--",
                                                                          label="template")]
    axb.legend(handles=hand, fontsize=5.8, loc="lower left", bbox_to_anchor=(1.0, -0.05), handlelength=1.6)
    panel_tag(axb, "b")
    axc = fig.add_axes([0.87, 0.58, 0.12, 0.35])
    wdt = 0.38
    for k, (kind, c, lab) in enumerate((("tm", GOLD, "template"), ("nn", BLUE, "network"))):
        aps = [res[(el, kind)]["ap"] for el in els]
        axc.bar(np.arange(len(els)) + (k - 0.5) * wdt, aps, wdt, color=c, label=lab)
    axc.set_xticks(range(len(els))); axc.set_xticklabels([f"{e}°" for e in els], fontsize=6.4)
    axc.set_xlabel("Sun elevation", fontsize=7.2)
    axc.set_ylabel("Average precision", fontsize=7.2)
    axc.set_ylim(0, 1)
    axc.legend(fontsize=5.8, loc="upper right")
    axc.grid(axis="x", visible=False)
    panel_tag(axc, "c")
    axd = fig.add_axes([0.47, 0.14, 0.52, 0.30])
    for k, (kind, c, lab, m) in enumerate((("tm", GOLD, "template", "s"), ("nn", BLUE, "network", "o"))):
        for i, el in enumerate(els):
            e = np.array(res[(el, kind)]["err"])
            e_plot = np.where(np.isfinite(e), e, 400.0)
            xs = i + (k - 0.5) * 0.3 + np.array([-0.06, 0, 0.06])
            axd.scatter(xs, np.clip(e_plot, 0.1, 400), color=c, marker=m, s=16, zorder=3,
                        label=lab if i == 0 else None, edgecolor="white", lw=0.4)
    axd.axhspan(30, 600, color="#FBEAEA", lw=0)
    axd.text(3.45, 300, "wrong match", fontsize=6.2, color=RED, ha="right", va="center")
    axd.set_yscale("log"); axd.set_ylim(0.1, 600)
    axd.set_xticks(range(len(els))); axd.set_xticklabels([f"sun {e}°" for e in els], fontsize=7)
    axd.set_ylabel("Position-fix error (m)", fontsize=7.2)
    axd.legend(fontsize=6.2, loc="upper left", ncol=2)
    axd.grid(axis="x", visible=False)
    panel_tag(axd, "d")
    foot(fig, "Synthetic 2 km × 2 km scenes, 5 m pixels, 170 craters of 12–110 m radius with random erosion, "
              "albedo and noise. Template: normalised cross-correlation with an ideal crater rendered at the true "
              "sun angle. Network: 256–64–1 perceptron trained on patches from ten other scenes under random "
              "lighting. (d) Position fix by RANSAC matching of the 40 best detections to the crater catalogue, "
              "three test scenes per sun angle.", width=160)
    save(fig, "ch48_crater")

# ----------------------------------------------------------------------------------------------------------------
# 7. Pose estimation: PnP with keypoint noise and outliers
# ----------------------------------------------------------------------------------------------------------------
F_PX, CX, CY = 3003.0, 960.0, 600.0       # SPEED-like camera: 17.6 mm lens, 5.86 um pixels, 1920 x 1200


def tango_points():
    a, b, h = 0.40, 0.40, 0.16
    body = np.array([[x, y, z] for x in (-a, a) for y in (-b, b) for z in (-h, h)])
    ant = np.array([[0.55, 0.0, 0.32], [-0.55, 0.0, 0.32], [0.0, 0.0, -0.45]])
    return np.vstack([body, ant])


def rodrigues(w):
    th = np.linalg.norm(w)
    if th < 1e-12:
        return np.eye(3)
    k = w / th
    Kx = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th) * Kx + (1 - np.cos(th)) * Kx @ Kx


def project(X, R, t):
    Y = X @ R.T + t
    return np.column_stack([F_PX * Y[:, 0] / Y[:, 2] + CX, F_PX * Y[:, 1] / Y[:, 2] + CY])


def dlt_pose(X, u):
    """Direct linear transform with Hartley normalisation of image points, projected onto a rotation."""
    xn = np.column_stack([(u[:, 0] - CX) / F_PX, (u[:, 1] - CY) / F_PX])
    m = xn.mean(0)
    sc = np.sqrt(2) / (np.sqrt(((xn - m) ** 2).sum(1)).mean() + 1e-12)
    Tn = np.array([[sc, 0, -sc * m[0]], [0, sc, -sc * m[1]], [0, 0, 1]])
    xs = (xn - m) * sc
    n = len(X)
    A = np.zeros((2 * n, 12))
    Xh = np.column_stack([X, np.ones(n)])
    A[0::2, 0:4] = Xh; A[0::2, 8:12] = -xs[:, :1] * Xh
    A[1::2, 4:8] = Xh; A[1::2, 8:12] = -xs[:, 1:2] * Xh
    _, _, Vt = np.linalg.svd(A)
    P = np.linalg.solve(Tn, Vt[-1].reshape(3, 4))
    M = P[:, :3]
    U, S, Vt2 = np.linalg.svd(M)
    R = U @ Vt2
    scale = S.mean()
    t = P[:, 3] / scale
    if np.linalg.det(R) < 0:
        R, t = -R, -t
    if t[2] < 0:
        R, t = -R, -t
        if np.linalg.det(R) < 0:
            R = -R
    return R, t


def refine_pose(X, u, R, t, iters=8):
    w = np.zeros(3)
    p = np.concatenate([w, t])
    R0 = R
    def res(p):
        return (project(X, rodrigues(p[:3]) @ R0, p[3:]) - u).ravel()
    lam = 1e-3
    r = res(p)
    for _ in range(iters):
        J = np.empty((len(r), 6))
        for k in range(6):
            dp = np.zeros(6); dp[k] = 1e-6 if k < 3 else 1e-5
            J[:, k] = (res(p + dp) - r) / dp[k]
        H = J.T @ J
        g = J.T @ r
        step = -np.linalg.solve(H + lam * np.diag(np.diag(H) + 1e-12), g)
        rn = res(p + step)
        if rn @ rn < r @ r:
            p, r, lam = p + step, rn, lam * 0.3
        else:
            lam *= 10
    return rodrigues(p[:3]) @ R0, p[3:]


def reproj_rms(X, u, R, t):
    return np.sqrt(np.mean(np.sum((project(X, R, t) - u) ** 2, axis=1)))


def posit(X, u, iters=12):
    """DeMenthon-Davis POSIT: scaled-orthographic iterations, good at long range."""
    xn = np.column_stack([(u[:, 0] - CX) / F_PX, (u[:, 1] - CY) / F_PX])
    A = X[1:] - X[0]
    B = np.linalg.pinv(A)
    eps = np.zeros(len(X) - 1)
    for _ in range(iters):
        xp = xn[1:, 0] * (1 + eps) - xn[0, 0]
        yp = xn[1:, 1] * (1 + eps) - xn[0, 1]
        I, J = B @ xp, B @ yp
        nI, nJ = np.linalg.norm(I), np.linalg.norm(J)
        if nI < 1e-12 or nJ < 1e-12:
            break
        s_ = np.sqrt(nI * nJ)
        i, j = I / nI, J / nJ
        k = np.cross(i, j); k /= np.linalg.norm(k) + 1e-12
        Z0 = 1.0 / s_
        eps = A @ k / Z0
    U, _, Vt = np.linalg.svd(np.vstack([i, j, k]))
    R = U @ Vt
    t0 = np.array([xn[0, 0] * Z0, xn[0, 1] * Z0, Z0])
    t = t0 - R @ X[0]
    return R, t


def pnp_ls(X, u, rng=None):
    """Initialise with DLT and with POSIT, refine both by Levenberg-Marquardt, keep the better fit."""
    best = None
    for init in (dlt_pose, posit):
        try:
            R, t = init(X, u)
        except np.linalg.LinAlgError:
            continue
        if not np.all(np.isfinite(t)) or t[2] <= 0:
            continue
        R, t = refine_pose(X, u, R, t)
        e = reproj_rms(X, u, R, t)
        if best is None or e < best[0]:
            best = (e, R, t)
    if best is None:
        R, t = refine_pose(X, u, np.eye(3), np.array([0, 0, 10.0]), iters=15)
        best = (reproj_rms(X, u, R, t), R, t)
    return best[1], best[2]


def pnp(X, u, ransac=False, rng=None, thr=12.0, iters=40):
    if not ransac:
        return pnp_ls(X, u, rng)
    best, bestn = None, -1
    n = len(X)
    for _ in range(iters):
        idx = rng.choice(n, 5, replace=False)
        try:
            R, t = posit(X[idx], u[idx])
        except np.linalg.LinAlgError:
            continue
        if not np.all(np.isfinite(t)) or t[2] <= 0:
            continue
        e = np.linalg.norm(project(X, R, t) - u, axis=1)
        inl = e < thr
        if inl.sum() > bestn:
            bestn, best = inl.sum(), inl
    if best is None or best.sum() < 5:
        return pnp_ls(X, u, rng)
    R, t = pnp_ls(X[best], u[best], rng)
    inl = np.linalg.norm(project(X, R, t) - u, axis=1) < thr     # re-collect inliers with the refined pose
    if inl.sum() >= 5:
        R, t = pnp_ls(X[inl], u[inl], rng)
    return R, t


def rand_rot(rng):
    q = rng.standard_normal(4); q /= np.linalg.norm(q)
    a, b, c, d = q
    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                     [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
                     [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]])


def pose_errors(R, t, Rt, tt):
    c = (np.trace(R @ Rt.T) - 1) / 2
    eq = np.arccos(np.clip(c, -1, 1))
    et = min(np.linalg.norm(t - tt) / np.linalg.norm(tt), 1.0)   # cap gross failures at 100 % of range
    return np.degrees(eq), et, eq + et


def pnp_fig():
    X = tango_points()
    rng = np.random.default_rng(11)
    sig = np.array([0.5, 1, 2, 4, 8, 16])
    ranges = [5.0, 15.0, 30.0]
    ntr = 120
    out = {}
    for rg in ranges:
        for sg in sig:
            eqs, ets, scs = [], [], []
            for _ in range(ntr):
                Rt = rand_rot(rng)
                tt = np.array([rng.uniform(-0.15, 0.15) * rg, rng.uniform(-0.1, 0.1) * rg, rg])
                u = project(X, Rt, tt) + rng.normal(0, sg, (len(X), 2))
                R, t = pnp(X, u, rng=rng)
                eq, et, sc = pose_errors(R, t, Rt, tt)
                eqs.append(eq); ets.append(et); scs.append(sc)
            out[(rg, sg)] = (np.median(eqs), np.median(ets), np.mean(scs))
    for rg in ranges:
        print(f"  range {rg:4.0f} m: " + ", ".join(f"σ={sg:g}px: {out[(rg,sg)][0]:.2f}°/{out[(rg,sg)][1]*100:.2f}%"
                                                  f"/S={out[(rg,sg)][2]:.3f}" for sg in sig))
    # outliers at 15 m
    rg = 15.0
    sc_out = {"clean": [], "outl": [], "ransac": []}
    for sg in sig:
        acc = {k: [] for k in sc_out}
        for _ in range(ntr):
            Rt = rand_rot(rng)
            tt = np.array([rng.uniform(-0.15, 0.15) * rg, rng.uniform(-0.1, 0.1) * rg, rg])
            u = project(X, Rt, tt) + rng.normal(0, sg, (len(X), 2))
            acc["clean"].append(pose_errors(*pnp(X, u, rng=rng), Rt, tt)[2])
            uo = u.copy()
            bad = rng.choice(len(X), 2, replace=False)
            uo[bad] += rng.uniform(40, 150, (2, 2)) * rng.choice([-1, 1], (2, 2))
            acc["outl"].append(pose_errors(*pnp(X, uo, rng=rng), Rt, tt)[2])
            acc["ransac"].append(pose_errors(*pnp(X, uo, ransac=True, rng=rng, thr=max(12.0, 4 * sg)), Rt, tt)[2])
        for k in sc_out:
            sc_out[k].append(np.mean(acc[k]))
    print("  15 m mean score: " + "; ".join(f"σ={sg:g}: clean {a:.3f}, 2 outliers {b:.3f}, RANSAC {c:.3f}"
                                            for sg, a, b, c in zip(sig, sc_out['clean'], sc_out['outl'],
                                                                   sc_out['ransac'])))
    fig = plt.figure(figsize=(7.0, 3.1))
    axa = fig.add_axes([0.01, 0.27, 0.23, 0.63])
    Rt = rodrigues(np.array([0.5, -0.6, 0.3])); tt = np.array([0.1, -0.05, 6.0])
    uv = project(X, Rt, tt)
    edges = [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]
    for a, b in edges:
        axa.plot(uv[[a, b], 0], uv[[a, b], 1], color=GREY, lw=1.0)
    for k, (a, b) in enumerate([(9, 1), (8, 7), (10, 0)]):
        pass
    ctr = project(np.array([[0.0, 0, 0.16], [0.0, 0.0, -0.16]]), Rt, tt)
    axa.plot([uv[8, 0], ctr[0, 0]], [uv[8, 1], ctr[0, 1]], color=GREY, lw=0.8)
    axa.plot([uv[9, 0], ctr[0, 0]], [uv[9, 1], ctr[0, 1]], color=GREY, lw=0.8)
    axa.plot([uv[10, 0], ctr[1, 0]], [uv[10, 1], ctr[1, 1]], color=GREY, lw=0.8)
    rr = np.random.default_rng(3)
    un = uv + rr.normal(0, 8, uv.shape)
    un[2] += [70, -50]
    axa.scatter(uv[:, 0], uv[:, 1], s=14, color=NAVY, zorder=3, label="true keypoints")
    axa.scatter(un[:, 0], un[:, 1], s=14, marker="x", color=ORANGE, zorder=4, label="detected (noisy)")
    axa.annotate("outlier", un[2], xytext=(un[2, 0] + 40, un[2, 1] + 90), fontsize=6.4, color=RED,
                 arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    axa.set_xlim(uv[:, 0].min() - 120, uv[:, 0].max() + 120)
    axa.set_ylim(uv[:, 1].max() + 140, uv[:, 1].min() - 120)
    axa.set_aspect("equal")
    img_axes(axa)
    axa.legend(fontsize=6.0, loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=1)
    axa.set_title("11 keypoints, 6 m range", fontsize=7.0, pad=2)
    panel_tag(axa, "a", x=0.04)
    axb = fig.add_axes([0.33, 0.27, 0.25, 0.63])
    for rg, c in zip(ranges, [GREEN, BLUE, VIOLET]):
        axb.plot(sig, [out[(rg, sg)][0] for sg in sig], "o-", color=c, ms=3.2, label=f"{rg:g} m")
    axb.set_xscale("log"); axb.set_yscale("log")
    axb.set_xticks(sig); axb.set_xticklabels([f"{x:g}" for x in sig])
    axb.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axb.set_xlabel("Keypoint noise σ (pixels)", fontsize=7.4)
    axb.set_ylabel("Median attitude error (°)", fontsize=7.4)
    axb.legend(fontsize=6.4, title="range", title_fontsize=6.2, loc="upper left")
    panel_tag(axb, "b")
    axc = fig.add_axes([0.66, 0.27, 0.22, 0.63])
    axc.plot(sig, sc_out["clean"], "o-", color=BLUE, ms=3.2, label="no outliers")
    axc.plot(sig, sc_out["outl"], "s-", color=RED, ms=3.2, label="2 outliers, least squares")
    axc.plot(sig, sc_out["ransac"], "D--", color=GREEN, ms=3.2, label="2 outliers, RANSAC")
    import matplotlib.transforms as mtrans
    trb = mtrans.blended_transform_factory(axc.transAxes, axc.transData)
    for yv, txt in [(0.0094, "SPEC2019\nwinner,\nsynthetic"), (0.065, "SPEC2021\nwinners,\nlab images"),
                    (0.375, "SPEC2019\nwinner,\nreal images")]:
        axc.axhline(yv, color=GREY, lw=0.7, ls=":")
        axc.text(1.03, yv, txt, fontsize=5.7, color=GREY, va="center", ha="left", transform=trb)
    axc.set_xscale("log"); axc.set_yscale("log")
    axc.set_xticks(sig); axc.set_xticklabels([f"{x:g}" for x in sig])
    axc.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axc.set_xlabel("Keypoint noise σ (pixels)", fontsize=7.4)
    axc.set_ylabel("Pose score (rad + range fraction)", fontsize=7.2)
    axc.legend(fontsize=5.9, loc="upper left", bbox_to_anchor=(0.0, 0.87))
    panel_tag(axc, "c")
    foot(fig, "Monte Carlo, 120 random attitudes per point; SPEED-like camera (focal length 3 003 pixels); 11 "
              "keypoints on a 0.8 m body with antennas; DLT and POSIT initialisation, Levenberg–Marquardt refinement, "
              "RANSAC on 5-point POSIT samples. (c) at 15 m; mean score as in the ESA–Stanford challenges, position error capped at 100 %.", width=150)
    save(fig, "ch48_pnp")

# ----------------------------------------------------------------------------------------------------------------
# 8. Convex (LP) fuel-optimal powered descent vs polynomial guidance
# ----------------------------------------------------------------------------------------------------------------
GM = 3.71                     # Mars gravity
A_MAX, A_MIN = 6.5, 2.0       # thrust acceleration limits (m/s^2)
TH_MAX = np.radians(60)       # thrust pointing limit from vertical
GS = np.radians(10)           # glide-slope angle above the ground
R0 = np.array([0.0, 1500.0]); V0 = np.array([20.0, -75.0])


def descent_lp(xT, tf, N=40, npoly=16):
    from scipy.optimize import linprog
    dt = tf / N
    nr, nv, nu = 2 * (N + 1), 2 * (N + 1), 2 * N
    iR, iV, iU, iS = 0, nr, nr + nv, nr + nv + nu
    nvar = iS + N
    g = np.array([0.0, -GM])
    Aeq, beq = [], []
    def row():
        return np.zeros(nvar)
    for d in range(2):
        r = row(); r[iR + d] = 1; Aeq.append(r); beq.append(R0[d])
        r = row(); r[iV + d] = 1; Aeq.append(r); beq.append(V0[d])
        r = row(); r[iR + 2 * N + d] = 1; Aeq.append(r); beq.append([xT, 0.0][d])
        r = row(); r[iV + 2 * N + d] = 1; Aeq.append(r); beq.append(0.0)
    for k in range(N):
        for d in range(2):
            r = row(); r[iV + 2 * (k + 1) + d] = 1; r[iV + 2 * k + d] = -1; r[iU + 2 * k + d] = -dt
            Aeq.append(r); beq.append(g[d] * dt)
            r = row(); r[iR + 2 * (k + 1) + d] = 1; r[iR + 2 * k + d] = -1; r[iV + 2 * k + d] = -dt
            r[iU + 2 * k + d] = -0.5 * dt * dt
            Aeq.append(r); beq.append(0.5 * g[d] * dt * dt)
    Aub, bub = [], []
    ph = np.linspace(0, 2 * np.pi, npoly, endpoint=False)
    for k in range(N):
        for a in ph:
            r = row(); r[iU + 2 * k] = np.cos(a); r[iU + 2 * k + 1] = np.sin(a); r[iS + k] = -1
            Aub.append(r); bub.append(0.0)
        r = row(); r[iU + 2 * k + 1] = -1; r[iS + k] = np.cos(TH_MAX); Aub.append(r); bub.append(0.0)
    for k in range(1, N):
        for sgn in (1, -1):
            r = row(); r[iR + 2 * k + 1] = -1; r[iR + 2 * k] = sgn * np.tan(GS)
            Aub.append(r); bub.append(sgn * np.tan(GS) * xT)
    c = np.zeros(nvar); c[iS:iS + N] = dt
    bounds = [(None, None)] * (iS) + [(A_MIN, A_MAX)] * N
    res = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=np.array(Aeq), b_eq=np.array(beq),
                  bounds=bounds, method="highs")
    if res.status != 0:
        return None
    x = res.x
    return dict(dv=res.fun, r=x[iR:iR + nr].reshape(-1, 2), u=x[iU:iU + nu].reshape(-1, 2),
                s=x[iS:iS + N], t=np.arange(N + 1) * dt, tf=tf)


def descent_best(xT):
    best = None
    for tf in np.arange(20, 121, 5.0):
        sol = descent_lp(xT, tf)
        if sol is not None and (best is None or sol["dv"] < best["dv"]):
            best = sol
    if best is None:
        return None
    t0 = best["tf"]
    for tf in np.arange(t0 - 4, t0 + 4.1, 1.0):
        if tf < 5:
            continue
        sol = descent_lp(xT, tf)
        if sol is not None and sol["dv"] < best["dv"]:
            best = sol
    return best


def poly_guidance(xT, tf, n=400):
    """Acceleration linear in time meeting final position and velocity (energy-optimal 'E-guidance' form)."""
    t = np.linspace(0, tf, n)
    rT = np.array([xT, 0.0])
    # net acceleration a(t) = c0 + c1 t
    M = np.array([[tf, tf ** 2 / 2], [tf ** 2 / 2, tf ** 3 / 6]])
    rhs = np.stack([-V0, rT - R0 - V0 * tf])
    C = np.linalg.solve(M, rhs)                    # rows: c0, c1 (each 2-vector)
    a = C[0][None, :] + C[1][None, :] * t[:, None]
    u = a - np.array([0.0, -GM])
    un = np.linalg.norm(u, axis=1)
    r = R0 + V0 * t[:, None] + C[0] * t[:, None] ** 2 / 2 + C[1] * t[:, None] ** 3 / 6
    feas = (un.max() <= A_MAX + 1e-9) and (un.min() >= A_MIN - 1e-9) and np.all(u[:, 1] >= un * np.cos(TH_MAX) - 1e-9)
    feas = feas and np.all(r[1:-1, 1] >= np.tan(GS) * np.abs(r[1:-1, 0] - xT) - 1e-6)
    dv = np.trapezoid(un, t)
    return feas, dv, r, un, t


def poly_best(xT):
    best = None
    for tf in np.arange(10, 160, 0.5):
        f, dv, r, un, t = poly_guidance(xT, tf)
        if f and (best is None or dv < best[0]):
            best = (dv, tf, r, un, t)
    return best


def gfold():
    divs = np.arange(-3000, 4001, 250.0)
    lp, pg = [], []
    for xT in divs:
        b = descent_best(xT)
        lp.append(b["dv"] if b else np.nan)
        q = poly_best(xT)
        pg.append(q[0] if q else np.nan)
    lp, pg = np.array(lp), np.array(pg)
    for xT, a, b in zip(divs, lp, pg):
        print(f"  divert {xT:6.0f} m: convex dv {a:6.1f} m/s, polynomial {b:6.1f} m/s")
    okl = divs[np.isfinite(lp)]; okp = divs[np.isfinite(pg)]
    print(f"  reachable diverts: convex {okl.min():.0f}..{okl.max():.0f} m, polynomial {okp.min():.0f}.."
          f"{okp.max():.0f} m")
    fig = plt.figure(figsize=(7.0, 3.2))
    axa = fig.add_axes([0.07, 0.29, 0.36, 0.62])
    show = [okl.min(), -1000, 0, 1000, okl.max()]
    cm = [VIOLET, BLUE, GREEN, ORANGE, RED]
    for xT, c in zip(show, cm):
        b = descent_best(xT)
        axa.plot(b["r"][:, 0], b["r"][:, 1], color=c, lw=1.4)
        axa.plot([xT], [0], marker="v", color=c, ms=5)
        q = poly_best(xT)
        if q:
            axa.plot(q[2][:, 0], q[2][:, 1], color=c, lw=0.9, ls="--")
    axa.plot([0], [1500], "o", color=INK, ms=4)
    axa.text(-2900, 1560, "start: 1 500 m up,\n75 m/s down,\n20 m/s across", fontsize=6.2, va="bottom")
    axa.set_xlabel("Downrange (m)", fontsize=7.6); axa.set_ylabel("Altitude (m)", fontsize=7.6)
    axa.set_ylim(-60, 2000)
    axa.legend(handles=[Line2D([], [], color=GREY, lw=1.4, label="convex (LP)"),
                        Line2D([], [], color=GREY, lw=0.9, ls="--", label="polynomial")],
               fontsize=6.4, loc="upper right")
    panel_tag(axa, "a")
    axb = fig.add_axes([0.52, 0.29, 0.22, 0.62])
    axb.plot(divs, lp, "o-", color=BLUE, ms=3, label="convex (LP)")
    axb.plot(divs, pg, "s--", color=ORANGE, ms=3, label="polynomial")
    axb.set_xlabel("Target shift (m)", fontsize=7.6); axb.set_ylabel("Δv used (m/s)", fontsize=7.6)
    axb.legend(fontsize=6.3, loc="upper left")
    panel_tag(axb, "b")
    axc = fig.add_axes([0.82, 0.29, 0.17, 0.62])
    b = descent_best(okl.max())
    tt = b["t"][:-1]
    axc.step(tt, b["s"], where="post", color=RED, lw=1.3)
    axc.axhline(A_MAX, color=GREY, ls=":", lw=0.8); axc.axhline(A_MIN, color=GREY, ls=":", lw=0.8)
    axc.set_ylim(0, 7.5)
    axc.set_xlabel("Time (s)", fontsize=7.6); axc.set_ylabel("Thrust / mass (m/s²)", fontsize=7.6)
    axc.text(0.05, 0.06, f"shift {okl.max():.0f} m:\nmax–min–max", transform=axc.transAxes, fontsize=6.2,
             ha="left", color=RED)
    panel_tag(axc, "c")
    print(f"  max divert {okl.max():.0f} m: tf {b['tf']:.0f} s, dv {b['dv']:.1f} m/s")
    foot(fig, "2-D Mars landing (g = 3.71 m/s²), thrust acceleration 2–6.5 m/s², within 60° of vertical, 10° glide "
              "slope. Convex: 40-step discretisation, ‖u‖ ≤ σ by a 16-sided polygon, minimise Σσ Δt by linear "
              "programming (HiGHS) with a search over flight time. Polynomial: acceleration linear in time, best "
              "feasible flight time.", width=150)
    save(fig, "ch48_gfold")

# ----------------------------------------------------------------------------------------------------------------
# 9. Learning to land: cross-entropy policy search vs PD control, with a runtime-assurance shield
# ----------------------------------------------------------------------------------------------------------------
G_MOON, AMAX_L, DT_L, NSTEP_L = 1.62, 4.0, 0.2, 400
NH = 12


def pol_unpack(theta):
    """theta (..., P): W1 (2 x NH), b1 (NH), w2 (NH), b2 (1)."""
    W1 = theta[..., :2 * NH].reshape(theta.shape[:-1] + (2, NH))
    b1 = theta[..., 2 * NH:3 * NH]
    w2 = theta[..., 3 * NH:4 * NH]
    b2 = theta[..., 4 * NH]
    return W1, b1, w2, b2


NPAR = 4 * NH + 1


def pol_act(theta, h, v):
    """Batch policy: theta (C, NPAR), h, v (C, E) -> thrust acceleration (C, E)."""
    W1, b1, w2, b2 = pol_unpack(theta)
    x = np.stack([h / 100.0, v / 10.0], axis=-1)                    # (C, E, 2)
    H = np.tanh(np.einsum("cek,ckh->ceh", x, W1) + b1[:, None, :])
    z = np.einsum("ceh,ch->ce", H, w2) + b2[:, None]
    return AMAX_L / (1 + np.exp(-z))


def pd_act(h, v, K=2.0):
    vref = -(0.9 + 0.11 * h)
    return np.clip(G_MOON + K * (vref - v), 0, AMAX_L)


def shield(h, v, a):
    """Runtime monitor: if the lander cannot stop in the remaining height with assured braking, brake fully."""
    a_assured = 0.7 * AMAX_L - G_MOON
    d_stop = np.where(v < 0, v * v / (2 * a_assured), 0.0)
    unsafe = (h < 1.25 * d_stop + 3.0) & (v < -1.2)
    return np.where(unsafe, AMAX_L, a), unsafe


def simulate(act_fn, h0, v0, thrust_eff=1.0, use_shield=False, record=False):
    """act_fn(h, v) -> a for arrays shaped like h0. Returns touchdown speed, dv, landed flag, (traj)."""
    h, v = h0.copy(), v0.copy()
    done = np.zeros(h.shape, bool)
    vtd = np.zeros(h.shape); dv = np.zeros(h.shape); nover = np.zeros(h.shape)
    traj = []
    for k in range(NSTEP_L):
        a = act_fn(h, v)
        if use_shield:
            a, uns = shield(h, v, a)
            nover += uns & ~done
        a = np.where(done, 0.0, a)
        dv += a * DT_L
        v_new = v + (thrust_eff * a - G_MOON) * DT_L
        h_new = h + 0.5 * (v + v_new) * DT_L
        hit = (h_new <= 0) & ~done
        vtd = np.where(hit, v_new, vtd)
        done = done | hit
        h = np.where(done, 0.0, h_new); v = np.where(done, v, v_new)
        if record:
            traj.append((h.copy(), v.copy()))
        if done.all():
            break
    vtd = np.where(done, vtd, np.nan)
    if record:
        return vtd, dv, done, traj, nover
    return vtd, dv, done, nover


def land_return(vtd, dv, done):
    spd = np.where(done, np.abs(vtd), 0.0)
    return -dv / 20.0 - 2.0 * np.maximum(spd - 1.0, 0) - 10.0 * (~done)


def init_states(rng, n, shifted=False):
    h0 = rng.uniform(80, 150, n)
    v0 = rng.uniform(-20, -4, n) if shifted else rng.uniform(-15, -5, n)
    return h0, v0


def rl():
    t0 = time.time()
    rng = np.random.default_rng(21)
    C, E, NEL, ITERS = 64, 24, 8, 60
    mu = np.zeros(NPAR); mu[-1] = 0.5
    sd = np.full(NPAR, 0.8)
    hist_mean, hist_succ, hist_best, hist_dv = [], [], [], []
    hv, vv = init_states(np.random.default_rng(99), 300)
    for it in range(ITERS):
        th = mu + sd * rng.standard_normal((C, NPAR))
        h0, v0 = init_states(rng, E)
        H0, V0 = np.tile(h0, (C, 1)), np.tile(v0, (C, 1))
        vtd, dv, done, _ = simulate(lambda h, v: pol_act(th, h, v), H0, V0)
        ret = land_return(vtd, dv, done).mean(1)
        el = np.argsort(-ret)[:NEL]
        mu = th[el].mean(0)
        sd = np.sqrt(th[el].var(0) + 0.02 ** 2 + 0.3 * np.exp(-it / 8.0) ** 2)
        # evaluate the mean policy on a fixed validation set
        vtd_v, dv_v, done_v, _ = simulate(lambda h, v: pol_act(mu[None, :], h, v), hv[None, :], vv[None, :])
        hist_mean.append(land_return(vtd_v, dv_v, done_v).mean())
        hist_dv.append(dv_v.mean())
        hist_succ.append(np.mean(done_v & (np.abs(np.nan_to_num(vtd_v, nan=99)) <= 1.5)) * 100)
        hist_best.append(ret.max())
    theta = mu[None, :]
    nep = (it + 1) * C * E
    print(f"  CEM: {ITERS} generations x {C} policies x {E} episodes = {nep} episodes, {time.time()-t0:.1f} s;"
          f" final validation success {hist_succ[-1]:.1f} %, return {hist_mean[-1]:.2f}")
    # PD baseline on validation
    vtd_p, dv_p, done_p, _ = simulate(lambda h, v: pd_act(h, v), hv, vv)
    print(f"  PD validation: success {np.mean(done_p & (np.abs(vtd_p) <= 1.5))*100:.1f} %, "
          f"return {land_return(vtd_p, dv_p, done_p).mean():.2f}, mean dv {dv_p.mean():.1f} m/s")
    vtd_l, dv_l, done_l, _ = simulate(lambda h, v: pol_act(theta, h[None, :], v[None, :])[0], hv, vv)
    print(f"  learned validation: mean dv {dv_l.mean():.1f} m/s, mean touchdown speed "
          f"{np.nanmean(np.abs(vtd_l)):.2f} m/s")
    # nominal and shifted tests
    tests = {}
    rt = np.random.default_rng(123)
    for cond, (eff, shifted) in {"nominal": (1.0, False), "shifted": (0.8, True)}.items():
        h0, v0 = init_states(rt, 1000, shifted)
        for name, fn, sh in [("PD", lambda h, v: pd_act(h, v), False),
                             ("learned", lambda h, v: pol_act(theta, h[None, :], v[None, :])[0], False),
                             ("learned + shield", lambda h, v: pol_act(theta, h[None, :], v[None, :])[0], True)]:
            vtd, dv, done, nov = simulate(fn, h0, v0, thrust_eff=eff, use_shield=sh)
            succ = np.mean(done & (np.abs(np.nan_to_num(vtd, nan=99)) <= 1.5)) * 100
            crash = np.mean(done & (np.abs(np.nan_to_num(vtd, nan=0)) > 3.0)) * 100
            tests[(cond, name)] = (succ, crash, dv.mean(), np.mean(nov > 0) * 100)
            print(f"  {cond:8s} {name:17s}: success {succ:5.1f} %, hard (>3 m/s) {crash:5.1f} %, "
                  f"mean dv {dv.mean():5.1f} m/s, shield active in {np.mean(nov>0)*100:4.1f} % of runs")
    fig = plt.figure(figsize=(7.0, 3.1))
    ax = fig.add_axes([0.07, 0.27, 0.25, 0.63])
    gen = np.arange(1, ITERS + 1)
    ret_pd = land_return(vtd_p, dv_p, done_p).mean()
    ax.plot(gen, hist_mean, color=BLUE, lw=1.4, label="learned policy")
    ax.axhline(ret_pd, color=ORANGE, ls="--", lw=1.0, label="PD controller")
    first = int(np.argmax(np.array(hist_succ) >= 99.99)) + 1
    ax.axvline(first, color=GREY, ls=":", lw=0.8)
    ax.text(first + 1.5, -9, f"all validation\nlandings soft\nfrom generation {first}", fontsize=6.0, color=GREY,
            va="bottom")
    ax.set_xlabel(f"Generation ({C} policies × {E} landings each)", fontsize=6.8)
    ax.set_ylabel("Mean return (higher is better)", fontsize=7.2)
    ax.set_ylim(-12, 0)
    ax.legend(fontsize=6.3, loc="lower right")
    print(f"  learning: return {hist_mean[0]:.2f} -> {hist_mean[-1]:.2f} (PD {ret_pd:.2f}); validation dv "
          f"{hist_dv[first-1]:.1f} m/s at gen {first} -> {hist_dv[-1]:.1f} m/s")
    panel_tag(ax, "a")
    ax2 = fig.add_axes([0.40, 0.27, 0.25, 0.63])
    hs, vs = np.array([140.0, 120, 90, 100]), np.array([-14.0, -6, -10, -12.5])
    _, _, _, trL, _ = simulate(lambda h, v: pol_act(theta, h[None, :], v[None, :])[0], hs, vs, record=True)
    _, _, _, trP, _ = simulate(lambda h, v: pd_act(h, v), hs, vs, record=True)
    for tr, c, ls in [(trL, BLUE, "-"), (trP, ORANGE, "--")]:
        Hh = np.array([t[0] for t in tr]); Vv = np.array([t[1] for t in tr])
        for j in range(len(hs)):
            m = Hh[:, j] > 0
            ax2.plot(Vv[m, j], Hh[m, j], color=c, ls=ls, lw=1.0)
    hh = np.linspace(0, 150, 100)
    a_ass = 0.7 * AMAX_L - G_MOON
    ax2.fill_betweenx(hh, -np.sqrt(np.maximum(2 * a_ass * (hh - 3.0) / 1.25, 0)), -25, color="#FBEAEA", lw=0)
    ax2.text(-19, 20, "shield\nbrakes\nhere", fontsize=6.2, color=RED)
    ax2.set_xlim(-21, 1); ax2.set_ylim(0, 155)
    ax2.set_xlabel("Vertical speed (m/s)", fontsize=7.4); ax2.set_ylabel("Height (m)", fontsize=7.4)
    ax2.legend(handles=[Line2D([], [], color=BLUE, label="learned"), Line2D([], [], color=ORANGE, ls="--",
                                                                         label="PD")], fontsize=6.3, loc="upper right")
    panel_tag(ax2, "b")
    ax3 = fig.add_axes([0.74, 0.27, 0.25, 0.63])
    names = ["PD", "learned", "learned + shield"]
    cols = [ORANGE, BLUE, GREEN]
    w = 0.26
    for i, (nm, c) in enumerate(zip(names, cols)):
        vals = [tests[("nominal", nm)][0], tests[("shifted", nm)][0]]
        ax3.bar(np.arange(2) + (i - 1) * w, vals, w, color=c, label=nm)
        for j, vv_ in enumerate(vals):
            ax3.text(j + (i - 1) * w, vv_ + 1.5, f"{vv_:.0f}", ha="center", fontsize=5.8)
    ax3.set_xticks([0, 1]); ax3.set_xticklabels(["nominal", "weaker engine,\nfaster start"], fontsize=6.8)
    ax3.set_ylabel("Soft landings (%)", fontsize=7.4)
    ax3.set_ylim(0, 150)
    ax3.set_yticks([0, 20, 40, 60, 80, 100])
    ax3.legend(fontsize=5.9, loc="upper center", ncol=2, columnspacing=0.8, handlelength=1.2)
    ax3.grid(axis="x", visible=False)
    panel_tag(ax3, "c")
    foot(fig, "1-D lunar landing (g = 1.62 m/s², thrust acceleration 0–4 m/s², 0.2 s steps) from 80–150 m at "
              "5–15 m/s descent; soft landing ≤ 1.5 m/s. Policy: 2–12–1 network trained by the cross-entropy method "
              "on return = −Δv/20 − 2 × excess touchdown speed. Shifted test: 20 % less thrust, start up to "
              "20 m/s. Shield: full braking when the stopping distance at 70 % of rated thrust nears the height.",
         width=150)
    save(fig, "ch48_rl")

if __name__ == "__main__":
    fns = [autonomy, arch, sched, rover, trn, crater, pnp_fig, gfold, rl]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            t0 = time.time()
            fn()
            print(f"{fn.__name__}: {time.time()-t0:.1f} s")
    print("ok")
