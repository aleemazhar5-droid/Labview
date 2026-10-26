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

if __name__ == "__main__":
    fns = [autonomy, arch, sched, rover]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            t0 = time.time()
            fn()
            print(f"{fn.__name__}: {time.time()-t0:.1f} s")
    print("ok")
