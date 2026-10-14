import importlib.util
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("c03", HERE / "ch03.py")
C3M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C3M)
C3M.EL.update({
    "venus": [0.72333566, 0.00000390, 0.00677672, -0.00004107, 3.39467605, -0.00078890, 181.97909950,
              58517.81538729, 131.60246718, 0.00268329, 76.67984255, -0.27769418],
    "jupiter": [5.20288700, -0.00011607, 0.04838624, -0.00013253, 1.30439695, -0.00183714, 34.39644051,
                3034.74612775, 14.72847983, 0.21252668, 100.47390909, 0.20469106]})
AU = C3M.AU
MU_S = C3M.MU_S

PL = {"Mercury": (0.387, 22032.0, 2440), "Venus": (0.723, 324859.0, 6052), "Earth": (1.0, 398600.4, 6371),
      "Mars": (1.524, 42828.4, 3390), "Jupiter": (5.203, 126686534.0, 69911), "Saturn": (9.537, 37931187.0, 58232),
      "Uranus": (19.19, 5793939.0, 25362), "Neptune": (30.07, 6836529.0, 24622)}


def mars_windows():
    res = []
    for yr, mo in [(2026, 10), (2028, 11), (2031, 1), (2033, 3), (2035, 5), (2037, 7), (2039, 9), (2041, 11)]:
        center = datetime(yr, mo, 15)
        best = (1e9, None, None, None)
        for dl in range(-110, 111, 4):
            ld = center + timedelta(days=dl)
            rE, vE = C3M.planet_rv("earth", C3M.jd_of(ld))
            for tof in range(130, 341, 6):
                ad = ld + timedelta(days=tof)
                rM, vM = C3M.planet_rv("mars", C3M.jd_of(ad))
                try:
                    v1, v2 = C3M.lambert(rE, rM, tof * 86400.0)
                except Exception:  # noqa: BLE001
                    continue
                c3 = np.linalg.norm(v1 - vE) ** 2
                if c3 < best[0]:
                    best = (c3, ld, tof, np.linalg.norm(v2 - vM))
        res.append(best)
        print(yr, round(best[0], 2), best[1].date(), best[2], round(best[3], 2))
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    x = np.arange(len(res))
    ax.bar(x, [r[0] for r in res], color=BLUE, width=0.6, label="Minimum launch energy C3")
    ax2 = ax.twinx()
    ax2.plot(x, [r[3] for r in res], "o-", color=RED, label="Arrival v∞ at that solution")
    ax2.set_ylabel("Arrival v∞ at Mars (km/s)", color=RED)
    ax2.set_ylim(2, 7)
    ax2.grid(False)
    for xi, r in zip(x, res):
        ax.text(xi, r[0] + 0.3, f"{r[0]:.1f}\n{r[1]:%b %Y}\n{r[2]} d", ha="center", fontsize=5.8)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{r[1]:%Y}" for r in res])
    ax.set_ylabel("C3 (km²/s²)")
    ax.set_ylim(0, 22)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=6.4, loc="upper right")
    note(ax, "Computed for this manual: single-revolution Lambert solutions minimising C3 in each window (labels: C3, "
             "launch month, flight time).", xy=(1, -0.16))
    save(fig, "ch24_marswindows")


def c3_planets():
    muS = MU_S
    names = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    c3, tof = [], []
    r1 = AU
    for n in names:
        r2 = PL[n][0] * AU
        a = (r1 + r2) / 2
        v1 = np.sqrt(muS / r1)
        vt = np.sqrt(muS * (2 / r1 - 1 / a))
        c3.append((vt - v1) ** 2)
        tof.append(np.pi * np.sqrt(a ** 3 / muS) / 86400 / 365.25)
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    x = np.arange(len(names))
    ax.bar(x, c3, color=NAVY, width=0.6, label="C3 for a Hohmann transfer")
    for xi, v, t in zip(x, c3, tof):
        ax.text(xi, v + 3, f"{v:.0f}\n{t:.1f} yr" if t >= 1 else f"{v:.0f}\n{t*12:.0f} mo", ha="center", fontsize=6.3)
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("C3 (km²/s²)")
    ax.set_ylim(0, 175)
    for c, n in [(12, "Falcon 9 / Atlas V class (several tonnes)"), (80, "requires heavy launcher, kick stage or gravity assists")]:
        ax.axhline(c, color=GREY, lw=0.6, ls=":")
        ax.text(6.4, c + 2, n, fontsize=6.2, color=GREY, ha="right")
    note(ax, "Circular coplanar orbits; labels give C3 (km²/s²) and transfer time. Real missions use gravity assists "
             "to reach the outer planets with lower C3.", xy=(1, -0.16))
    save(fig, "ch24_c3planets")


def ga_turn():
    vinf = np.linspace(1, 20, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    for n, rp_alt, c in [("Venus", 300, ORANGE), ("Earth", 300, BLUE), ("Mars", 300, RED), ("Jupiter", 300000, GOLD),
                         ("Saturn", 100000, VIOLET), ("Moon", 100, GREY)]:
        if n == "Moon":
            mu, R = 4902.8, 1737
        else:
            mu, R = PL[n][1], PL[n][2]
        rp = R + rp_alt
        delta = 2 * np.degrees(np.arcsin(1 / (1 + rp * vinf ** 2 / mu)))
        ax.plot(vinf, delta, color=c, lw=1.6, label=f"{n} (r_p = R + {rp_alt:,} km)")
    ax.set_xlabel("Hyperbolic excess speed v∞ (km/s)")
    ax.set_ylabel("Maximum turn angle (°)")
    ax.set_ylim(0, 180)
    ax.set_xlim(1, 20)
    ax.legend(fontsize=6.3, loc="upper right")
    note(ax, "δ = 2 arcsin[1 / (1 + r_p v∞² / μ)]. A flyby rotates the velocity relative to the planet; in the Sun's "
             "frame this changes speed and direction.", xy=(1, -0.16))
    save(fig, "ch24_gaturn")


def power():
    r = np.linspace(0.3, 40, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.plot(r, 1361 / r ** 2, color=ORANGE, lw=1.8)
    for n, d in [("Venus", 0.72), ("Earth", 1), ("Mars", 1.52), ("asteroid belt", 2.8), ("Jupiter", 5.2), ("Saturn", 9.5),
                 ("Uranus", 19.2), ("Neptune", 30.1)]:
        ax.axvline(d, color=GREY, lw=0.5, ls=":")
        ax.text(d * 1.04, 2500, n, fontsize=6.2, rotation=90, va="top", color=GREY)
    for n, d, y in [("Juno (≈ 60 m² arrays)", 5.2, 1361 / 5.2 ** 2), ("Lucy (two 7.3 m arrays, to 5.7 AU)", 5.7, 1361 / 5.7 ** 2),
                    ("Rosetta (64 m², to 5.25 AU)", 5.25, 1361 / 5.25 ** 2 * 0.7)]:
        ax.plot(d, y, "o", color=NAVY, ms=4)
        off = {"J": (-120, 12), "L": (8, 10), "R": (8, -12)}[n[0]]
        ax.annotate(n, (d, y), xytext=off, textcoords="offset points", fontsize=6.2,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.5))
    ax.axvspan(9, 40, color=VIOLET, alpha=0.07)
    ax.text(14, 0.6, "radioisotope power needed\n(Cassini, New Horizons, Voyager)", fontsize=6.4, color=VIOLET)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.3, 40)
    ax.set_ylim(0.3, 3000)
    ax.set_xlabel("Distance from the Sun (AU)")
    ax.set_ylabel("Solar irradiance (W/m²)")
    note(ax, "Solar flux falls as 1/r²: at Jupiter it is 3.7 % of that at Earth, and cells are also colder and dimmer.",
         xy=(1, -0.16))
    save(fig, "ch24_power")


def lowthrust():
    dv = np.linspace(0, 20, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    for isp, c, n in [(230, GREY, "monopropellant hydrazine (230 s)"), (320, BLUE, "bipropellant (320 s)"),
                      (450, GREEN, "LOX/LH₂ (450 s)"), (1600, ORANGE, "Hall thruster (1 600 s)"),
                      (3100, RED, "gridded ion engine (3 100 s)")]:
        ax.plot(dv, (1 - np.exp(-dv * 1000 / (isp * 9.80665))) * 100, color=c, lw=1.6, label=n)
    for d, n in [(11, "Dawn ≈ 11 km/s"), (4.5, "Mars orbit insertion\n+ manoeuvres")]:
        ax.axvline(d, color=GREY, lw=0.6, ls=":")
        ax.text(d + 0.15, 8, n, fontsize=6.2, color=GREY)
    ax.set_xlabel("Mission Δv (km/s)")
    ax.set_ylabel("Propellant (% of initial mass)")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=6.3, loc="center right")
    note(ax, "Rocket equation m_p/m_0 = 1 − exp(−Δv / (I_sp g₀)). Electric propulsion makes large Δv affordable, but "
             "only with low thrust.", xy=(1, -0.16))
    save(fig, "ch24_lowthrust")


def orbits_plot():
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    th = np.linspace(0, 2 * np.pi, 400)
    for n, c in [("Mercury", GREY), ("Venus", ORANGE), ("Earth", BLUE), ("Mars", RED), ("Jupiter", GOLD)]:
        r = PL[n][0]
        ax.plot(r * np.cos(th), r * np.sin(th), color=c, lw=0.9)
        ang = {"Mercury": 2.4, "Venus": 1.9, "Earth": 1.2, "Mars": 0.75, "Jupiter": 0.6}[n]
        ax.text(r * np.cos(ang) + 0.05, r * np.sin(ang) + 0.05, n, fontsize=6.4, color=c)
    for r2, c, n in [(1.524, RED, "Hohmann Earth → Mars: 259 days"), (5.203, GOLD, "Hohmann Earth → Jupiter: 2.7 years"),
                     (0.723, ORANGE, "Hohmann Earth → Venus: 146 days")]:
        a = (1 + r2) / 2
        e = abs(r2 - 1) / (r2 + 1)
        t = np.linspace(0, np.pi, 200)
        rr = a * (1 - e ** 2) / (1 + e * np.cos(t))
        sgn = 1 if r2 > 1 else -1
        ax.plot(sgn * rr * np.cos(t), sgn * rr * np.sin(t), color=c, lw=1.6, ls="--", label=n)
    ax.plot(0, 0, "o", color="#F6A623", ms=9)
    ax.set_aspect("equal")
    ax.set_xlim(-5.6, 5.6)
    ax.set_ylim(-5.6, 5.6)
    ax.set_xlabel("AU")
    ax.set_ylabel("AU")
    ax.legend(fontsize=6.4, loc="lower right")
    note(ax, "Half-ellipse Hohmann transfers between circular orbits (to scale).", xy=(1, -0.11))
    save(fig, "ch24_orbits")


def lighttime():
    items = [("Moon", 384400), ("L2 (JWST)", 1.5e6), ("Venus (closest–farthest)", (38e6, 261e6)),
             ("Mars (closest–farthest)", (55e6, 401e6)), ("Jupiter", (588e6, 968e6)), ("Saturn", (1.2e9, 1.66e9)),
             ("New Horizons (2026)", 62.5 * 1.496e8), ("Voyager 1 (Nov 2026)", 2.59e10)]
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    c = 299792.458
    for k, (n, d) in enumerate(items):
        if isinstance(d, tuple):
            ax.plot([d[0] / c, d[1] / c], [k, k], color=BLUE, lw=6, solid_capstyle="butt")
            t = d[1] / c
        else:
            ax.plot(d / c, k, "o", color=NAVY, ms=6)
            t = d / c
        lab = f"{t:.1f} s" if t < 60 else (f"{t/60:.0f} min" if t < 3600 else f"{t/3600:.1f} h")
        ax.text(t * 1.25, k, lab, va="center", fontsize=6.4)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([i[0] for i in items], fontsize=7)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlabel("One-way light time (s)")
    for s, n in [(60, "1 min"), (3600, "1 h"), (86400, "1 day")]:
        ax.axvline(s, color=GREY, lw=0.5, ls=":")
        ax.text(s, 7.7, n, fontsize=6.2, color=GREY, ha="center")
    ax.set_xlim(0.5, 3e5)
    ax.grid(axis="y", visible=False)
    note(ax, "Round-trip times are twice these values: spacecraft beyond the Moon must act autonomously.", xy=(1, -0.16))
    save(fig, "ch24_lighttime")


def bplane():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 100), ylim=(0, 46))
    planet(ax, 70, 22, 5, "#C1440E")
    ax.annotate("", (64, 26), (10, 37), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4))
    label(ax, 22, 39.5, "incoming asymptote (direction of v∞)", fs=6.6, color=NAVY)
    ax.plot([70, 66.6], [22, 31.8], color=RED, lw=1.4)
    label(ax, 64, 31, "B", fs=8, color=RED, weight="bold")
    t = np.linspace(-1.2, 1.3, 100)
    ax.plot(70 + 10 * np.sinh(t) * 0.6 - 5, 22 + 9.5 * np.cosh(t) * 0.55, color=ORANGE, lw=1.4)
    label(ax, 88, 33, "hyperbolic flyby\ntrajectory", fs=6.4, color=ORANGE)
    box(ax, 4, 4, 42, 18, "B-plane: perpendicular to v∞ through the planet's centre.\nB vector: where the trajectory "
        "would pierce it.\nNavigators target B·R and B·T; the size of the\nB-plane error ellipse sets the risk and "
        "accuracy\nof flybys, orbit insertion and entry.", fs=6.2, fc="white", ha="left")
    save(fig, "ch24_bplane")


def ddor():
    fig, ax = canvas(7.0, 3.0, xlim=(0, 100), ylim=(0, 40))
    earth(ax, 50, -40, 50, atmosphere=False)
    for x in (30, 70):
        ax.add_patch(Polygon([[x - 3, 9.7], [x + 3, 9.7], [x, 13]], closed=True, fc="white", ec=NAVY))
    label(ax, 22, 15, "DSN station 1", fs=6.4, color=NAVY)
    label(ax, 78, 15, "DSN station 2", fs=6.4, color=NAVY)
    for x in (30, 70):
        ax.plot([x, 47], [13, 38], color=ORANGE, lw=1)
        ax.plot([x, 60], [13, 38], color=VIOLET, lw=0.8, ls="--")
    satellite(ax, 47, 38.5, s=0.6)
    label(ax, 40, 38.5, "spacecraft", fs=6.4, color=ORANGE, ha="right")
    ax.plot(60, 38.5, "*", color=VIOLET, ms=9)
    label(ax, 62, 38.5, "quasar (reference direction)", fs=6.4, color=VIOLET, ha="left")
    box(ax, 72, 16, 27, 14, "Delta-DOR: difference in arrival\ntimes at two stations, calibrated\nagainst a nearby "
        "quasar →\nangular accuracy ≈ 1 nrad\n(≈ 0.2 km at Mars)", fs=6.0, fc="white")
    save(fig, "ch24_ddor")


def clipper_timeline():
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    rows = [("Concept and Phase A", 2013, 2015.5, GREY), ("Design (B, C)", 2015.5, 2019.7, BLUE),
            ("Build and test (D)", 2019.7, 2024.8, NAVY), ("Cruise: Mars and Earth flybys", 2024.78, 2030.3, ORANGE),
            ("Science: ≈ 49 Europa flybys", 2030.3, 2034.8, RED)]
    for j, (n, a, b, c) in enumerate(rows):
        ax.barh(j, b - a, left=a, color=c, height=0.6)
        ax.text(b + 0.2, j, n, va="center", fontsize=6.6)
    for x, n, dy in [(2024.78, "launch 14 Oct 2024", -0.9), (2025.17, "Mars flyby Mar 2025", -1.5),
                     (2026.92, "Earth flyby Dec 2026", -0.9), (2030.3, "Jupiter arrival 2030", -1.5)]:
        ax.axvline(x, color=GREY, lw=0.6, ls=":")
        ax.text(x + 0.15, dy, n, fontsize=5.8, ha="left", color=GREY, va="bottom")
    ax.set_ylim(len(rows) - 0.4, -1.9)
    ax.set_xlim(2012.5, 2040)
    ax.set_yticks([])
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Year")
    save(fig, "ch24_clipper")


def nrho():
    fig, ax = canvas(7.0, 3.3, xlim=(-10, 110), ylim=(-28, 28))
    earth(ax, 0, 0, 4)
    planet(ax, 75, 0, 1.6, "#BDBDBD")
    label(ax, 75, -3.8, "Moon", fs=6.6)
    for x, n in [(64, "L1"), (87, "L2")]:
        ax.plot(x, 0, "+", color=INK, ms=7)
        label(ax, x, 2.5, n, fs=6.6)
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(86 + 3.5 * np.cos(t), 4 + 15 * np.sin(t) * (0.6 + 0.4 * np.sin(t)), color=RED, lw=1.5)
    label(ax, 97, 18, "L2 southern NRHO\n(perilune ≈ 3 000 km,\napolune ≈ 70 000 km,\nperiod ≈ 6.5 days)", fs=6.0,
          color=RED, ha="left")
    ax.add_patch(Ellipse((75, 0), 26, 40, fc="none", ec=GREEN, lw=1.3, ls="--"))
    label(ax, 75, 22, "distant retrograde orbit (DRO)", fs=6.2, color=GREEN)
    ax.plot(np.linspace(4, 73, 100), 12 * np.sin(np.linspace(0, np.pi, 100)), color=BLUE, lw=1)
    label(ax, 35, 13.5, "translunar transfer (≈ 3–5 days)", fs=6.2, color=BLUE)
    ax.plot(np.linspace(4, 73, 100), -18 * np.sin(np.linspace(0, np.pi, 100)) ** 0.5, color=VIOLET, lw=1, ls="--")
    label(ax, 30, -21, "low-energy (ballistic) transfer via Sun–Earth L1 region (≈ 3–4 months)", fs=6.2, color=VIOLET)
    save(fig, "ch24_cislunar")


if __name__ == "__main__":
    fns = [mars_windows, c3_planets, ga_turn, power, lowthrust, orbits_plot, lighttime, bplane, ddor, clipper_timeline,
           nrho]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
