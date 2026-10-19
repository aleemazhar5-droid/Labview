import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge  # noqa: F401

G0 = 9.80665


# ======================================================================================================
# 1. Timeline of crewed spacecraft
# ======================================================================================================
def timeline_fig():
    # (name, start, end, colour, flights label, planned?)
    US, SU, CN, IN = BLUE, RED, GOLD, GREEN
    rows = [
        ("Vostok", 1961, 1963.5, SU, "6", False),
        ("Mercury", 1961, 1963.5, US, "6", False),
        ("Voskhod", 1964.7, 1965.4, SU, "2", False),
        ("Gemini", 1965, 1966.95, US, "10", False),
        ("Apollo CSM", 1968.7, 1975.6, US, "15", False),
        ("Apollo Lunar Module", 1969.1, 1972.97, US, "9", False),
        ("Soyuz", 1967.2, 2026.8, SU, "≈ 155", False),
        ("Space Shuttle", 1981.25, 2011.55, US, "135", False),
        ("Shenzhou", 2003.8, 2026.8, CN, "17", False),
        ("Crew Dragon", 2020.4, 2026.8, US, "21", False),
        ("Starliner", 2024.4, 2024.7, US, "1", False),
        ("Orion", 2026.25, 2026.8, US, "1", False),
    ]
    planned = [
        ("Starliner", 2028.0, 2030.5),
        ("Orion", 2027.5, 2030.5),
        ("Gaganyaan", 2027.75, 2030.5, IN),
        ("Mengzhou", 2028.0, 2030.5, CN),
        ("Starship HLS / Blue Moon", 2028.0, 2030.5, US),
    ]
    names = [r[0] for r in rows] + ["Gaganyaan", "Mengzhou", "Starship HLS / Blue Moon"]
    ypos = {n: i for i, n in enumerate(names)}
    fig, ax = plt.subplots(figsize=(6.9, 3.9))
    for n, a, b, c, lab, _ in rows:
        y = ypos[n]
        ax.barh(y, max(b - a, 0.35), left=a, color=c, height=0.62, zorder=3)
        xt = b + 0.5
        ax.text(xt if n not in ("Starliner", "Orion") else xt, y, lab, va="center", fontsize=6.4, color=INK, zorder=4)
    for p in planned:
        n, a, b = p[0], p[1], p[2]
        c = p[3] if len(p) > 3 else BLUE
        y = ypos[n]
        ax.barh(y, b - a, left=a, color="white", edgecolor=c, hatch="////", lw=0.8, height=0.62, zorder=3)
    ax.text(2027.0, ypos["Starliner"] - 0.02, "", fontsize=6)
    # labels for crewed flight counts of planned rows
    ax.text(2026.2, ypos["Gaganyaan"], "first crewed flight planned", fontsize=6.0, color=GREY, ha="right", va="center")
    ax.text(2027.7, ypos["Mengzhou"], "crewed lunar landing goal 2030", fontsize=6.0, color=GREY, ha="right", va="center")
    ax.text(2027.7, ypos["Starship HLS / Blue Moon"], "first Artemis landing planned", fontsize=6.0, color=GREY,
            ha="right", va="center")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=7.2)
    ax.invert_yaxis()
    ax.set_xlim(1958, 2032)
    ax.set_xlabel("Year")
    ax.grid(axis="y", visible=False)
    ax.axvline(2026.8, color=GREY, lw=0.8, ls=":", zorder=1)
    ax.text(2026.6, -0.9, "Oct 2026", fontsize=6.2, color=GREY, ha="right")
    from matplotlib.patches import Patch
    h = [Patch(color=US, label="USA"), Patch(color=SU, label="USSR / Russia"), Patch(color=CN, label="China"),
         Patch(color=IN, label="India"), Patch(fc="white", ec=GREY, hatch="////", label="planned")]
    ax.legend(handles=h, loc="lower left", fontsize=6.6, ncol=1, frameon=True, framealpha=0.95, edgecolor="#ccc")
    fig.text(0.99, 0.01, "Numbers: crewed launches of each vehicle to October 2026 (Soyuz includes the 1975 and 1983 "
                         "launch aborts; Apollo CSM includes Skylab and ASTP). Planned dates as announced in 2026.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch31_timeline")


# ======================================================================================================
# 2. Anatomy of a capsule stack (Orion-like) — schematic
# ======================================================================================================
def anatomy():
    fig, ax = canvas(7.0, 3.8, xlim=(0, 100), ylim=(-4, 54))
    yc = 30
    s = 3.4  # units per metre
    # --- service module
    smx0, smx1 = 13, 28
    ax.add_patch(Rectangle((smx0, yc - 2.0 * s), smx1 - smx0, 4.0 * s, fc="#DDE3EA", ec=NAVY, lw=1.0, zorder=3))
    # propellant tanks
    for yy in (yc + 3.2, yc - 3.2):
        ax.add_patch(FancyBboxPatch((smx0 + 1.0, yy - 2.0), 12.5, 4.0, boxstyle="round,pad=0,rounding_size=2.0",
                                    fc="#F4E3C8", ec=ORANGE, lw=0.8, zorder=4))
    # main engine
    ax.add_patch(Polygon([(smx0, yc - 1.4), (smx0, yc + 1.4), (smx0 - 6, yc + 3.6), (smx0 - 6, yc - 3.6)],
                         fc="#9AA4AE", ec=INK, lw=0.7, zorder=3))
    # solar array wings (X-wing, seen edge-on as two)
    for sgn in (1, -1):
        ax.add_patch(Polygon([(smx0 + 6, yc + sgn * 2.0 * s), (smx0 + 8, yc + sgn * 2.0 * s),
                              (smx0 + 2, yc + sgn * (2.0 * s + 12)), (smx0, yc + sgn * (2.0 * s + 12))],
                             fc="#2A4E8A", ec="#1b2d4f", lw=0.5, zorder=2))
    # radiator panels
    ax.add_patch(Rectangle((smx0 + 13.6, yc - 2.0 * s), 1.2, 4.0 * s, fc="#F2F5F8", ec=GREY, lw=0.5, zorder=4))
    # --- crew module (frustum), heat shield at x=28
    cmx0, cmx1 = 28.6, 40.5
    rb, rt = 2.5 * s, 1.0 * s
    cm = [(cmx0, yc - rb), (cmx1, yc - rt), (cmx1, yc + rt), (cmx0, yc + rb)]
    ax.add_patch(Polygon(cm, fc="#EEF1F4", ec=NAVY, lw=1.1, zorder=3))
    # heat shield (thick curved)
    th = np.linspace(-1, 1, 40)
    hx = cmx0 - 0.9 * (1 - th ** 2) * 0.9 + 0.2
    ax.fill_betweenx(yc + th * rb, hx - 0.9, cmx0 + 0.2, color="#6B4A2B", zorder=4)
    # pressure vessel (dashed)
    pv = [(cmx0 + 1.6, yc - rb + 1.6), (cmx1 - 2.6, yc - rt - 0.4), (cmx1 - 2.6, yc + rt + 0.4),
          (cmx0 + 1.6, yc + rb - 1.6)]
    ax.add_patch(Polygon(pv, fc="#FFFFFF", ec=BLUE, lw=0.9, ls="--", zorder=4))
    # seats (crew couches) — simple L-shapes facing the heat shield
    for yy in (yc - 3.6, yc, yc + 3.6):
        ax.plot([cmx0 + 3.0, cmx0 + 3.0, cmx0 + 6.5], [yy + 1.3, yy - 0.6, yy - 0.6], color=INK, lw=1.0, zorder=5)
    # window
    ax.add_patch(Polygon([(cmx0 + 6.2, yc + rb - 2.8 + 0.1), (cmx0 + 7.8, yc + rb - 3.5 + 0.1),
                          (cmx0 + 7.8, yc + rb - 4.6 + 0.6), (cmx0 + 6.2, yc + rb - 3.9 + 0.6)],
                         fc=SKY, ec=NAVY, lw=0.6, zorder=6))
    # parachute bay & docking tunnel
    ax.add_patch(Rectangle((cmx1 - 2.4, yc - rt + 0.2), 2.2, 2 * rt - 0.4, fc="#F6D7B0", ec=ORANGE, lw=0.6, zorder=5))
    ax.add_patch(Rectangle((cmx1, yc - 1.4), 1.4, 2.8, fc="#C8CDD3", ec=INK, lw=0.6, zorder=5))
    # RCS thruster marks on CM
    for (xx, yy) in [(cmx0 + 4.5, yc + rb - 1.8), (cmx0 + 4.5, yc - rb + 1.8)]:
        ax.plot([xx], [yy], marker="s", ms=3.2, color=RED, zorder=6)
    # --- launch abort system: fairing + tower
    fx0 = cmx0 + 0.6
    fair = [(fx0, yc - rb - 0.6), (cmx1 + 2.2, yc - rt - 1.0), (cmx1 + 3.2, yc - 1.2), (cmx1 + 3.2, yc + 1.2),
            (cmx1 + 2.2, yc + rt + 1.0), (fx0, yc + rb + 0.6)]
    ax.add_patch(Polygon(fair, fc="none", ec=GREY, lw=0.9, ls=(0, (3, 2)), zorder=6))
    tx0, tx1 = cmx1 + 3.2, 77
    ax.add_patch(Rectangle((tx0, yc - 1.2), tx1 - tx0, 2.4, fc="#F3F6F9", ec=INK, lw=0.8, zorder=4))
    ax.add_patch(Polygon([(tx1, yc - 1.2), (tx1, yc + 1.2), (tx1 + 6, yc)], fc="#F3F6F9", ec=INK, lw=0.8, zorder=4))
    # abort motor section (nozzles canted)
    am0, am1 = tx0 + 4, tx0 + 17
    ax.add_patch(Rectangle((am0, yc - 1.2), am1 - am0, 2.4, fc="#F7D9C4", ec=ORANGE, lw=0.8, zorder=5))
    for sgn in (1, -1):
        ax.add_patch(Polygon([(am0 + 0.5, yc + sgn * 1.2), (am0 + 2.0, yc + sgn * 1.2), (am0 - 0.6, yc + sgn * 3.0),
                              (am0 - 2.0, yc + sgn * 3.0)], fc="#9AA4AE", ec=INK, lw=0.5, zorder=5))
    # jettison motor and attitude control motor
    ax.add_patch(Rectangle((am1 + 1, yc - 1.2), 6, 2.4, fc="#E6E0F0", ec=VIOLET, lw=0.8, zorder=5))
    ax.add_patch(Rectangle((am1 + 9, yc - 1.2), 5, 2.4, fc="#DCEFE4", ec=GREEN, lw=0.8, zorder=5))
    # ---- callouts
    def call(xy, txt, xt, yt, ha="center"):
        ax.annotate(txt, xy, xytext=(xt, yt), fontsize=6.4, ha=ha, va="center", color=INK, zorder=8,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.text(smx0 + 7.25, yc + 3.2, "propellant", fontsize=5.6, ha="center", va="center", zorder=6)
    ax.text(smx0 + 7.25, yc - 3.2, "propellant", fontsize=5.6, ha="center", va="center", zorder=6)
    call((smx0 - 4, yc - 1), "Main engine", 4, 13)
    call((smx0 + 1.4, yc + 2.0 * s + 10), "Solar array wing", 1, 52.5, ha="left")
    call((smx0 + 14.2, yc - 5.5), "Radiators", 25, 5.5)
    call((cmx0 - 0.9, yc - 5), "Ablative heat shield", 12, 3.0)
    call((cmx0 + 3.0, yc - 0.6), "Crew seats", 35, 3.0)
    call((cmx0 + 4.5, yc - rb + 1.8), "RCS thrusters", 41, 9.0)
    call((cmx0 + 7.0, yc + rb - 3.2), "Window", 29, 51.5)
    call((cmx0 + 9, yc + 3.6), "Pressure vessel\n(welded Al–Li)", 41, 49)
    call((cmx1 - 1.2, yc - 2.5), "Parachute bay", 50, 4.5)
    call((cmx1 + 0.8, yc + 1.2), "Docking hatch\nand mechanism", 53, 43)
    call((cmx1 + 2.5, yc - rt - 1.4), "Protective cover", 54, 13)
    call((am0 - 1.4, yc - 2.8), "Abort motor:\nnozzles canted outward", 67, 8.0)
    call((am1 + 4, yc + 1.2), "Jettison motor", 68, 41)
    call((am1 + 11.5, yc - 1.2), "Attitude control\nmotor (steers)", 86, 17)
    # brackets naming the three elements
    for a, b, t in [(smx0 - 6, smx1, "SERVICE MODULE"), (smx1 + 0.4, cmx1 + 1.4, "CREW MODULE"),
                    (cmx1 + 1.8, tx1 + 6, "LAUNCH ABORT SYSTEM")]:
        ax.plot([a, a, b, b], [-0.2, -1.2, -1.2, -0.2], color=NAVY, lw=0.9)
        ax.text((a + b) / 2, -2.6, t, fontsize=6.8, weight="bold", color=NAVY, ha="center", va="center")
    ax.text(99, 53, "Schematic, Orion-like layout;\nnot to scale in detail.", fontsize=5.9, color=GREY, ha="right",
            va="top")
    save(fig, "ch31_anatomy")


# ======================================================================================================
# 3. Acceleration tolerance (NASA-STD-3001 Vol. 2 Rev. A, Figs 2-5) + simulated entries
# ======================================================================================================
STD = {
    "+Gx": {"Return": ([0.5, 10, 30, 50, 90, 120, 150, 10000], [14, 10, 8, 6.3, 5, 4.3, 4, 4]),
            "Launch": ([0.5, 5, 300], [19, 16, 7.5]),
            "Emergency": ([0.5, 120, 300, 1200], [38, 8.8, 7.5, 5])},
    "−Gx": {"Return": ([0.5, 10, 30, 50, 90, 100, 10000], [13.5, 8, 6, 4.7, 4.05, 4, 4]),
            "Launch": ([0.5, 5, 120, 400], [22, 15, 6, 4]),
            "Emergency": ([0.5, 120, 300, 1200], [29, 7.7, 6.2, 4.3])},
    "+Gz": {"Return": ([0.5, 15, 30, 50, 80, 100, 120, 10000], [2, 1.25, 1, 0.8, 0.68, 0.6, 0.5, 0.5]),
            "Launch": ([0.5, 5, 1200], [8.3, 6.4, 4]),
            "Emergency": ([0.5, 120, 1200], [17, 6, 3.8])},
    "−Gz": {"Return": ([0.5, 10, 30, 50, 80, 100, 120, 10000], [2, 1.8, 1.2, 0.8, 0.55, 0.5, 0.5, 0.5]),
            "Launch": ([0.5, 5, 60, 1200], [6, 3.8, 2.2, 1]),
            "Emergency": ([0.5, 120, 1200], [6.5, 2.3, 1.6])},
}


def _time_above(t, n, levels):
    dt = np.gradient(t)
    return np.array([np.sum(dt[n >= L]) for L in levels])


def gtol():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.9, 3.0), gridspec_kw=dict(width_ratios=[1, 1.15]))
    cols = {"+Gx": BLUE, "−Gx": GREEN, "+Gz": ORANGE, "−Gz": RED}
    desc = {"+Gx": "+Gx  eyeballs in", "−Gx": "−Gx  eyeballs out", "+Gz": "+Gz  eyeballs down",
            "−Gz": "−Gz  eyeballs up"}
    for k, c in cols.items():
        d, a = STD[k]["Emergency"]
        a1.plot(d, a, color=c, lw=1.7, label=desc[k])
        d, a = STD[k]["Return"]
        a1.plot(d, a, color=c, lw=1.0, ls="--")
    a1.set_xscale("log"); a1.set_yscale("log")
    a1.set_xlim(0.5, 1500); a1.set_ylim(0.4, 45)
    a1.set_xlabel("Duration (s)"); a1.set_ylabel("Acceleration limit (g)")
    a1.set_title("(a) Limits by direction", fontsize=7.8)
    a1.legend(fontsize=6.0, loc="upper right")
    a1.set_yticks([0.5, 1, 2, 5, 10, 20, 40]); a1.set_yticklabels(["0.5", "1", "2", "5", "10", "20", "40"])
    # (b) +Gx limits with simulated entries
    for lab, ls, c in [("Emergency", "-", RED), ("Launch", "-.", NAVY), ("Return", "--", BLUE)]:
        d, a = STD["+Gx"][lab]
        a2.plot(d, a, color=c, lw=1.6, ls=ls, label=f"+Gx limit: {lab.lower()}")
    runs = _entry_runs()
    levels = np.linspace(0.5, 13, 260)
    for key, c in [("leo_lift", GREEN), ("leo_ball", ORANGE), ("lunar_direct", VIOLET), ("lunar_skip", SKY)]:
        o = runs[key]
        ta = _time_above(o[:, 0], o[:, 4], levels)
        m = ta > 0.5
        a2.plot(ta[m], levels[m], color=c, lw=1.3, label=ENTRY_LABEL[key])
    a2.plot([5], [15.5], "*", color=INK, ms=7, label="Soyuz T-10-1 abort (1983)")
    a2.set_xscale("log"); a2.set_yscale("log")
    a2.set_xlim(0.5, 1500); a2.set_ylim(0.2, 45)
    a2.set_yticks([0.5, 1, 2, 5, 10, 20, 40]); a2.set_yticklabels(["0.5", "1", "2", "5", "10", "20", "40"])
    a2.set_xlabel("Time spent above the level (s)"); a2.set_ylabel("Acceleration (g)")
    a2.set_title("(b) Eyeballs-in limits vs simulated entries", fontsize=7.8)
    a2.legend(fontsize=5.6, loc="lower left", ncol=1)
    fig.text(0.99, 0.01, "Limits: NASA-STD-3001 Vol. 2 Rev. A, Figs 2–5 (sustained, > 0.5 s); in (a) solid = abort/emergency "
                         "entry, dashed = nominal return. (b) Time each simulated entry\nof the entry-simulation figure spends "
                         "above a given load; T-10-1: reported 14–17 g for about 5 s.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch31_gtol")


# ======================================================================================================
# 4. Entry simulation (3-DOF point mass, exponential-interpolated US-76 density, Sutton-Graves heating)
# ======================================================================================================
RE, MU = 6371e3, 3.986e14
_HK = np.array([0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 150]) * 1e3
_RK = np.log(np.array([1.225, 0.7364, 0.4135, 0.1948, 8.891e-2, 4.008e-2, 1.841e-2, 3.996e-3, 1.027e-3, 3.097e-4,
                       8.283e-5, 1.846e-5, 3.416e-6, 5.604e-7, 9.708e-8, 2.222e-8, 8.152e-9, 2.076e-9]))


def rho(h):
    return float(np.exp(np.interp(min(max(h, 0.0), 150e3), _HK, _RK)))


def entry_run(V0, gam0, beta, LD, Rn, mode, par=None, h0=122e3, dt=0.1):
    """Returns array columns: t, h, v, downrange, n(g), qdot(W/m2), Q(J/m2), phase."""
    par = par or {}
    h, v, gam, x = h0, V0, np.radians(gam0), 0.0
    t = Q = 0.0
    phase = 0
    out = []
    while h > 8e3 and t < 4000:
        r = RE + h
        g = MU / r ** 2
        rh = rho(h)
        d = 0.5 * rh * v * v / beta
        hdot = v * np.sin(gam)
        LDe = LD
        if mode == "ballistic":
            cphi, LDe = 0.0, 0.0
        elif mode == "const":
            cphi = np.cos(np.radians(par["bank"]))
        else:
            if phase == 0:                      # full lift up until the trajectory pulls out
                cphi = 1.0
                if hdot > 0 and d > 0.5 * G0:
                    phase = 1
            if phase == 1:                      # hold a gentle descent (equilibrium-glide style)
                need = (g - v * v / r) * np.cos(gam) + 0.02 * (par.get("hdot_ref", -20.0) - hdot)
                cphi = np.clip(need / max(d * LD, 1e-6), -1, 1)
                if mode == "skip" and v < par["vskip"]:
                    phase = 2
                if mode == "direct" and v < par.get("vfinal", 6500):
                    phase = 3
            if phase == 2:                      # skip: lift up, climb out of the sensible atmosphere
                cphi = 1.0
                if d < 0.05 * G0 and hdot < 0:
                    phase = 4
            if phase == 3:
                cphi = np.cos(np.radians(par.get("bankfinal", 60)))
            if phase == 4:                      # second entry
                cphi = 1.0
                if d > 0.5 * G0:
                    phase = 5
            if phase == 5:
                need = (g - v * v / r) * np.cos(gam) + 0.02 * (-20.0 - hdot)
                cphi = np.clip(need / max(d * LD, 1e-6), -1, 1)
                if v < par.get("vfinal2", 4000):
                    phase = 6
            if phase == 6:
                cphi = np.cos(np.radians(60))
        L = d * LDe * cphi
        qd = 1.7415e-4 * np.sqrt(rh / Rn) * v ** 3
        n = d * np.sqrt(1 + LDe ** 2) / G0
        out.append((t, h, v, x, n, qd, Q, phase))
        dv = -d - g * np.sin(gam)
        dg = (L + (v * v / r - g) * np.cos(gam)) / v
        h += hdot * dt
        v += dv * dt
        gam += dg * dt
        x += v * np.cos(gam) * RE / r * dt
        Q += qd * dt
        t += dt
    return np.array(out)


BETA_SOYUZ = 2950 / (1.3 * np.pi * 2.17 ** 2 / 4)     # ≈ 610 kg/m2
BETA_ORION = 9300 / (1.35 * np.pi * 5.02 ** 2 / 4)    # ≈ 350 kg/m2
ENTRY_LABEL = {"leo_lift": "LEO, lifting (Soyuz-like)", "leo_ball": "LEO, ballistic backup",
               "lunar_direct": "Lunar, guided direct", "lunar_skip": "Lunar, skip entry"}
_RUNS = {}


def _entry_runs():
    if not _RUNS:
        _RUNS["leo_lift"] = entry_run(7600, -1.35, BETA_SOYUZ, 0.30, 2.3, "const", {"bank": 55})
        _RUNS["leo_ball"] = entry_run(7600, -1.35, BETA_SOYUZ, 0.30, 2.3, "ballistic")
        _RUNS["lunar_direct"] = entry_run(11000, -6.0, BETA_ORION, 0.27, 6.0, "direct",
                                          {"hdot_ref": -20, "vfinal": 6500, "bankfinal": 60})
        _RUNS["lunar_skip"] = entry_run(11000, -6.0, BETA_ORION, 0.27, 6.0, "skip",
                                        {"hdot_ref": -20, "vskip": 8500, "vfinal2": 4000})
    return _RUNS


def entry():
    runs = _entry_runs()
    cols = {"leo_lift": GREEN, "leo_ball": ORANGE, "lunar_direct": VIOLET, "lunar_skip": SKY}
    fig, axs = plt.subplots(2, 2, figsize=(6.9, 4.9))
    (a1, a2), (a3, a4) = axs
    for k, o in runs.items():
        t, h, v, x, n, q, Q = o[:, 0], o[:, 1], o[:, 2], o[:, 3], o[:, 4], o[:, 5], o[:, 6]
        a1.plot(x / 1e3, h / 1e3, color=cols[k], lw=1.4, label=ENTRY_LABEL[k])
        a2.plot(t / 60, n, color=cols[k], lw=1.4)
        a3.plot(t / 60, q / 1e4, color=cols[k], lw=1.4)
    a1.set_xlabel("Downrange from entry interface (km)"); a1.set_ylabel("Altitude (km)")
    a1.set_title("(a) Trajectories", fontsize=7.8); a1.set_ylim(0, 125); a1.set_xlim(0, 6500)
    a1.legend(fontsize=6.0, loc="lower left")
    a2.set_xlabel("Time from entry interface (min)"); a2.set_ylabel("Deceleration (g)")
    a2.set_title("(b) Load on the crew", fontsize=7.8); a2.set_xlim(0, 17); a2.set_ylim(0, 11)
    a3.set_xlabel("Time from entry interface (min)"); a3.set_ylabel("Stagnation heat flux (W/cm²)")
    a3.set_title("(c) Convective heating", fontsize=7.8); a3.set_xlim(0, 17); a3.set_ylim(0, 140)
    # annotate skip pulses
    o = runs["lunar_skip"]
    a3.annotate("skip: two heating pulses\nwith a cool-down between", (10.6, 30), xytext=(9.0, 85), fontsize=6.0,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    # (d) cumulative heat load
    for k, o in runs.items():
        a4.plot(o[:, 0] / 60, o[:, 6] / 1e7, color=cols[k], lw=1.4)
        a4.text(o[-1, 0] / 60 + 0.25, o[-1, 6] / 1e7, f"{o[-1, 6] / 1e7:.1f}", fontsize=6.0, color=cols[k],
                va="center")
    a4.set_xlim(0, 17); a4.set_ylim(0, 22)
    a4.set_xlabel("Time from entry interface (min)"); a4.set_ylabel("Heat load (kJ/cm²)")
    a4.set_title("(d) Total heat soaked by the shield", fontsize=7.8)
    fig.text(0.99, 0.005, "Model: 3-DOF point mass, US-76 density, Sutton–Graves convective heating only (radiative heating, "
                          "significant above 10 km/s, omitted). LEO: 7.6 km/s, −1.35°, β = 610 kg/m², L/D 0.3, bank 55°. "
                          "Lunar: 11.0 km/s, −6.0°,\nβ = 350 kg/m², L/D 0.27, simple bank-angle guidance. Entry interface 122 km. "
                          "Illustrative, not flight trajectories.", ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1), h_pad=1.0)
    save(fig, "ch31_entry")


# ======================================================================================================
# 5. Abort systems — schematic
# ======================================================================================================
def _capsule(ax, x, y, w=10, h=7, fc="#EEF1F4"):
    ax.add_patch(Polygon([(x - w / 2, y), (x + w / 2, y), (x + w * 0.2, y + h), (x - w * 0.2, y + h)], fc=fc,
                         ec=NAVY, lw=1.0, zorder=4))
    ax.add_patch(Rectangle((x - w / 2, y - 0.7), w, 0.7, fc="#6B4A2B", ec="none", zorder=4))


def _plume(ax, x, y, ang, L=6, wd=1.6, c=ORANGE):
    a = np.radians(ang)
    dx, dy = np.cos(a), np.sin(a)
    px, py = -dy, dx
    pts = [(x + px * 0.3, y + py * 0.3), (x - px * 0.3, y - py * 0.3),
           (x + dx * L - px * wd, y + dy * L - py * wd), (x + dx * L + px * wd, y + dy * L + py * wd)]
    ax.add_patch(Polygon(pts, fc=c, ec="none", alpha=0.75, zorder=3))


def abort_schem():
    fig, ax = canvas(7.0, 3.5, xlim=(0, 100), ylim=(0, 50))
    # (a) tower
    cx, cy = 14, 14
    _capsule(ax, cx, cy)
    ax.add_patch(Rectangle((cx - 0.9, cy + 7), 1.8, 15, fc="#F3F6F9", ec=INK, lw=0.8, zorder=4))
    ax.add_patch(Polygon([(cx - 0.9, cy + 22), (cx + 0.9, cy + 22), (cx, cy + 25)], fc="#F3F6F9", ec=INK, lw=0.8,
                         zorder=4))
    for sgn in (1, -1):
        _plume(ax, cx + sgn * 0.9, cy + 10, 270 + sgn * 30, L=8)
    darrow = None  # noqa
    ax.annotate("", (cx, cy + 31), (cx, cy + 26), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4))
    label(ax, cx + 2, cy + 28.5, "pulls", fs=6.4, ha="left", color=NAVY)
    label(ax, cx, 2.5, "(a) Tower (tractor)\nMercury, Apollo, Soyuz, Shenzhou,\nOrion, Gaganyaan, Mengzhou", fs=6.4)
    # (b) pusher
    cx = 40
    _capsule(ax, cx, cy, fc="#EEF1F4")
    for sgn in (1, -1):
        ax.add_patch(Rectangle((cx + sgn * 4.1 - 0.6, cy + 1.2), 1.2, 3.0, fc="#9AA4AE", ec=INK, lw=0.5, zorder=5))
        _plume(ax, cx + sgn * 4.1, cy + 1.0, 270 + sgn * 18, L=9)
    ax.add_patch(Rectangle((cx - 5, cy - 6.5), 10, 5.8, fc="#DDE3EA", ec=GREY, lw=0.7, zorder=2))
    label(ax, cx, cy - 3.6, "trunk / SM", fs=5.9, color=GREY)
    ax.annotate("", (cx, cy + 16), (cx, cy + 9), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4))
    label(ax, cx + 2, cy + 13.5, "pushes", fs=6.4, ha="left", color=NAVY)
    label(ax, cx, 2.5, "(b) Pusher (integrated engines)\nCrew Dragon, Starliner", fs=6.4)
    # (c) comparison table-like text
    x0 = 58
    rows = [("", "Tower", "Pusher"),
            ("Thrust-to-weight", "≈ 7–13", "≈ 4–6"),
            ("Burn time", "1–5 s", "≈ 5–10 s"),
            ("Available", "pad → jettison", "pad → orbit"),
            ("Mass to orbit", "jettisoned", "carried"),
            ("Re-use", "lost each flight", "with capsule"),
            ("Propellant", "solid", "hypergolic"),
            ("Risk", "jettison event", "propellant on board")]
    for i, (a, b, c) in enumerate(rows):
        y = 44 - i * 4.6
        wt = "bold" if i == 0 else "normal"
        if i > 0 and i % 2 == 1:
            ax.add_patch(Rectangle((x0 - 1, y - 2.2), 42, 4.4, fc="#F3F6F9", ec="none", zorder=1))
        ax.text(x0, y, a, fontsize=6.6, va="center", weight="bold" if i > 0 else wt, color=NAVY)
        ax.text(x0 + 19, y, b, fontsize=6.6, va="center", weight=wt, ha="center")
        ax.text(x0 + 33, y, c, fontsize=6.6, va="center", weight=wt, ha="center")
    label(ax, x0 + 20, 4.5, "(c) Trade-offs (typical values)", fs=6.6)
    save(fig, "ch31_abort")


# ======================================================================================================
# 6. Abort separation simulation (1-D, along the flight path)
# ======================================================================================================
def abort_sep(kind, case, tmax=8.0, dt=0.002):
    """Separation distance and capsule sensed acceleration after an abort command at t=0.
    kind: 'tower' (16 t, 1.8 MN, 3 s regressive) or 'pusher' (12.5 t, 0.57 MN, 6 s).
    case: 'pad' (booster stays on pad, gravity acts), 'maxq_off' (booster engines shut down at abort, q0 = 30 kPa),
          'maxq_on' (booster keeps thrusting at 1.5 g specific force)."""
    if kind == "tower":
        m, T0, tb, CdA, dm = 16000.0, 1.8e6, 3.0, 0.8 * np.pi * 5.0 ** 2 / 4, 2000.0
    else:
        m, T0, tb, CdA, dm = 12500.0, 8 * 71e3, 6.0, 0.8 * np.pi * 4.0 ** 2 / 4, 1200.0
    v0 = 0.0 if case == "pad" else 420.0           # m/s at max-Q (≈ Mach 1.4 at 11 km, q ≈ 31 kPa)
    h0 = 0.0 if case == "pad" else 11000.0
    gam = np.radians(90 if case == "pad" else 60)
    mb, CdAb = 300e3, 0.5 * np.pi * 3.7 ** 2 / 4   # booster after capsule separation
    xc = xb = 0.0
    vc = vb = v0
    t = 0.0
    T, S, A = [], [], []
    while t < tmax:
        if kind == "tower":
            Tt = T0 * max(0.0, 1.0 - 0.5 * t / tb) if t < tb else 0.0
        else:
            Tt = T0 if t < tb else 0.0
        mm = m - dm * min(t, tb) / tb
        rc = rho(h0 + xc * np.sin(gam))
        Dc = 0.5 * rc * vc * abs(vc) * CdA
        fc = (Tt - Dc) / mm
        if case == "pad":
            fb = 0.0
            ab = 0.0
        else:
            rb_ = rho(h0 + xb * np.sin(gam))
            Db = 0.5 * rb_ * vb * vb * CdAb
            fb = (1.5 * G0 if case == "maxq_on" else 0.0) - Db / mb
            ab = fb - G0 * np.sin(gam)
        ac = fc - G0 * np.sin(gam)
        vc += ac * dt; xc += vc * dt
        vb += ab * dt; xb += vb * dt
        T.append(t); S.append(xc - xb); A.append(fc / G0)
        t += dt
    return np.array(T), np.array(S), np.array(A)


def abortsim():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.9, 3.0), gridspec_kw=dict(width_ratios=[1.25, 1]))
    cases = [("tower", "pad", NAVY, "-", "Tower, pad abort"), ("pusher", "pad", ORANGE, "-", "Pusher, pad abort"),
             ("tower", "maxq_off", NAVY, "--", "Tower, max-Q, booster shut down"),
             ("pusher", "maxq_off", ORANGE, "--", "Pusher, max-Q, booster shut down"),
             ("tower", "maxq_on", NAVY, ":", "Tower, max-Q, booster still thrusting"),
             ("pusher", "maxq_on", ORANGE, ":", "Pusher, max-Q, booster still thrusting")]
    for kind, case, c, ls, lab in cases:
        t, s, a = abort_sep(kind, case)
        a1.plot(t, s, color=c, ls=ls, lw=1.5, label=lab)
        if case != "maxq_on":
            a2.plot(t, a, color=c, ls=ls, lw=1.4)
    a1.axhspan(150, 300, color=RED, alpha=0.08, zorder=0)
    a1.text(0.2, 225, "illustrative blast and\nfragment hazard zone", fontsize=5.9, color=RED, va="center")
    a1.set_xlim(0, 6); a1.set_ylim(-50, 700)
    a1.set_xlabel("Time after abort command (s)"); a1.set_ylabel("Separation from booster (m)")
    a1.set_title("(a) Getting away", fontsize=7.8)
    a1.legend(fontsize=5.6, loc="upper left")
    a2.set_xlim(0, 7); a2.set_ylim(-4, 12)
    a2.axhline(0, color=GREY, lw=0.6)
    a2.set_xlabel("Time after abort command (s)"); a2.set_ylabel("Sensed acceleration (g)")
    a2.set_title("(b) What the crew feels", fontsize=7.8)
    a2.text(6.9, 11.5, "solid: pad abort\ndashed: max-Q abort — drag\neats into thrust, then\ndecelerates the capsule", fontsize=5.8,
            color=GREY, ha="right", va="top")
    fig.text(0.99, 0.01, "1-D model along the flight path. Tower: 16 t abort vehicle, 1.8 MN regressive thrust for 3 s. "
                         "Pusher: 12.5 t, 8 × 71 kN for 6 s. Max-Q: 420 m/s at 11 km (q ≈ 31 kPa), C_D ≈ 0.8; booster 300 t.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch31_abortsim")


# ======================================================================================================
# 7. Parachutes: descent speed vs canopy size, and a descent-sequence simulation
# ======================================================================================================
def chute_v(m, D, N, cd=0.80, rho0=1.225, eff=None):
    eff = eff if eff is not None else {1: 1.0, 2: 0.95, 3: 0.92, 4: 0.90}[N]
    S = N * np.pi * D ** 2 / 4 * eff
    return np.sqrt(2 * m * G0 / (rho0 * cd * S))


def descent_sim(m=9300.0):
    """Orion-like sequence: drogues at 7.0 km, mains (3 × 35 m) at 2.6 km with two reefing stages."""
    cd_body, A_body = 1.0, np.pi * 5.0 ** 2 / 4
    Sd = 2 * np.pi * 7.0 ** 2 / 4 * 0.95 * 0.55       # drogues, Cd 0.55
    Sm = 3 * np.pi * 35.0 ** 2 / 4 * 0.92 * 0.80     # mains, Cd 0.80
    h, v, t = 12000.0, 190.0, 0.0                    # vertical descent assumption below 12 km
    out = []
    dt = 0.02
    td = tm = None
    while h > 0:
        r = rho(h)
        S = cd_body * A_body
        if h < 7000:
            if td is None:
                td = t
            S += Sd * min(1.0, (t - td) / 2.0)
        if h < 2600:
            if tm is None:
                tm = t
            tau = t - tm
            S -= Sd * min(1.0, tau / 1.0) if tau < 1 else Sd
            frac = 0.06 if tau < 6 else (0.25 if tau < 12 else 1.0)    # reefing stages
            S += Sm * frac
        D = 0.5 * r * v * v * S
        a = G0 - D / m
        out.append((t, h, v, D / (m * G0)))
        v += a * dt
        h -= v * dt
        t += dt
    return np.array(out)


def chutes():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.9, 3.1))
    D = np.linspace(15, 50, 200)
    m = 9300.0
    for N, c in [(1, GREY), (2, ORANGE), (3, BLUE), (4, GREEN)]:
        a1.plot(D, chute_v(m, D, N), color=c, lw=1.6, label=f"{N} main{'s' if N > 1 else ''}")
    a1.axhspan(6.5, 9.0, color=SKY, alpha=0.18, zorder=0)
    a1.text(15.5, 7.75, "typical splashdown speeds", fontsize=6.0, color=NAVY, ha="left", va="center")
    v3, v2 = chute_v(m, 35, 3), chute_v(m, 35, 2)
    a1.plot([35], [v3], "o", color=NAVY, ms=4.5)
    a1.plot([35], [v2], "s", color=RED, ms=4.5)
    a1.annotate(f"Orion-like: 3 × 35 m → {v3:.1f} m/s", (35, v3), xytext=(19, 3.2), fontsize=6.0,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.annotate(f"one main failed\n→ {v2:.1f} m/s", (35, v2), xytext=(36.5, 16.5), fontsize=6.0,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.set_xlim(15, 50); a1.set_ylim(0, 30)
    a1.set_xlabel("Nominal diameter of each main canopy (m)"); a1.set_ylabel("Sea-level descent speed (m/s)")
    a1.set_title("(a) Sizing the mains for a 9.3 t capsule", fontsize=7.8)
    a1.legend(fontsize=6.2, loc="upper right")
    o = descent_sim()
    t, h, v, n = o.T
    a2.plot(t, v, color=NAVY, lw=1.6, label="Descent speed")
    a2.set_yscale("log"); a2.set_ylim(5, 300)
    a2.set_yticks([5, 10, 20, 50, 100, 200]); a2.set_yticklabels(["5", "10", "20", "50", "100", "200"])
    a2.set_xlim(0, t[-1] * 1.02)
    a2.set_xlabel("Time from 12 km altitude (s)"); a2.set_ylabel("Descent speed (m/s)", color=NAVY)
    a2.set_title("(b) Simulated descent sequence", fontsize=7.8)
    b2 = a2.twinx()
    b2.plot(t, n, color=RED, lw=0.9, alpha=0.9)
    b2.set_ylim(0, 8); b2.set_ylabel("Load on crew (g)", color=RED, fontsize=7.5)
    b2.tick_params(axis="y", labelsize=7, colors=RED); b2.grid(False)
    b2.spines["right"].set_visible(True)
    i7, i26, i15 = [int(np.argmin(abs(h - hh))) for hh in (7000, 2600, 1500)]
    for txt, k, (tx, ty) in [("drogues open\n(7 km)", i7, (t[i7] + 8, 230)),
                             ("mains open, reefed\n(2.6 km)", i26, (t[i26] + 12, 120)),
                             ("mains fully open\n(1.5 km)", i15, (t[i15] + 30, 30))]:
        a2.annotate(txt, (t[k], v[k]), xytext=(tx, ty), fontsize=6.0, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a2.text(t[-1] * 0.98, v[-1] * 0.78, f"splashdown {v[-1]:.1f} m/s", fontsize=6.0, color=NAVY, ha="right", va="top")
    fig.text(0.99, 0.01, "v = √(2mg / ρ C_D S); ringsail C_D ≈ 0.8 on nominal area, cluster efficiency 0.90–0.95. "
                         "(b) drogues 2 × 7 m from 12 km at 190 m/s (vertical), mains reefed to 6 % then 25 % of area.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch31_chutes")


# ======================================================================================================
# 8. Safety: Shuttle risk progression + flights needed to demonstrate a target
# ======================================================================================================
def safety():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.9, 3.1))
    fl = [1, 5, 25, 26, 28, 87, 96, 114, 133]
    odds = [12, 10, 10, 17, 36, 21, 47, 73, 90]
    lab = ["STS-1", "STS-5", "51-L", "STS-26", "STS-29", "STS-86", "STS-103", "STS-114", "STS-133"]
    a1.step(fl + [135], odds + [90], where="post", color=RED, lw=1.6, label="Retrospective estimate (2011)")
    a1.plot(fl, odds, "o", color=RED, ms=3.5)
    offs = {"STS-1": (1, 6.0), "STS-29": (-12, 9), "STS-86": (2, -5.5), "STS-103": (-30, 8),
            "STS-114": (-28, 14), "STS-133": (-27, 16)}
    for f, o, l in zip(fl, odds, lab):
        if l in offs:
            dx, dy = offs[l]
            a1.text(f + dx, o + dy, f"{l}: 1 in {o}", fontsize=5.8, color=INK)
    a1.axhline(135 / 2, color=NAVY, lw=1.2, ls="--", label="Actual: 2 losses in 135 flights")
    a1.plot([25], [10], marker="x", color=INK, ms=7, mew=1.5)
    a1.plot([113], [47], marker="x", color=INK, ms=7, mew=1.5)
    a1.text(27, 4.5, "Challenger\n(flight 25)", fontsize=5.8, ha="left")
    a1.text(111, 38.5, "Columbia\n(flight 113)", fontsize=5.8, ha="right", va="top")
    a1.set_ylim(0, 125); a1.set_xlim(0, 140)
    a1.annotate("", (44, 124), (44, 108), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.8))
    a1.text(46, 116, "Managers' belief (reported 1986):\n1 in 100 000, far off scale", fontsize=5.8, color=GREY, va="center")
    a1.set_xlabel("Shuttle flight number"); a1.set_ylabel("Risk of losing the crew: 1 in N flights")
    a1.set_title("(a) Space Shuttle: estimated vs actual risk", fontsize=7.8)
    a1.legend(fontsize=5.8, loc="upper left", bbox_to_anchor=(0.0, 0.83))
    # (b) flights needed
    p = np.logspace(-3.3, -1, 200)
    for C, c in [(0.5, SKY), (0.8, BLUE), (0.95, NAVY)]:
        n = np.log(1 - C) / np.log(1 - p)
        a2.plot(1 / p, n, color=c, lw=1.6, label=f"{int(C * 100)} % confidence")
    a2.set_xscale("log"); a2.set_yscale("log")
    a2.set_xlabel("Target: 1 loss in N flights"); a2.set_ylabel("Failure-free flights needed")
    a2.set_title("(b) Demonstrating safety by flying", fontsize=7.8)
    for nn, t_ in [(155, "Soyuz ≈ 155"), (135, "Shuttle 135"), (21, "Crew Dragon 21")]:
        a2.axhline(nn, color=GREY, lw=0.7, ls=":")
        a2.text(1900, nn * (1.08 if nn != 135 else 0.72), t_, fontsize=5.8, color=GREY, ha="right")
    a2.axvline(270, color=GREEN, lw=1.0, ls=":")
    a2.text(285, 7, "Commercial Crew\nrequirement", fontsize=5.8, color=GREEN)
    n270 = np.log(1 - 0.8) / np.log(1 - 1 / 270)
    a2.plot([270], [n270], "o", color=GREEN, ms=4)
    a2.annotate(f"1 in 270 at 80 %\nconfidence: {n270:.0f} flights", (270, n270), xytext=(480, 40), fontsize=5.9,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a2.set_xlim(10, 2000); a2.set_ylim(5, 2e4)
    a2.legend(fontsize=5.8, loc="upper left")
    fig.text(0.99, 0.01, "(a) Hamlin et al., NASA Shuttle risk progression (2011), loss-of-crew-and-vehicle odds at selected "
                         "flights. (b) n = ln(1 − C) / ln(1 − 1/N): flights with no loss needed to show risk ≤ 1/N.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch31_safety")


if __name__ == "__main__":
    fns = [timeline_fig, anatomy, gtol, entry, abort_schem, abortsim, chutes, safety]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
