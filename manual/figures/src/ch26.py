import importlib.util
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("c03", HERE / "ch03.py")
C3M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C3M)
# JPL approximate Keplerian elements (Standish), valid 1800-2050: a, da, e, de, i, di, L, dL, varpi, dvarpi, Omega, dOmega
C3M.EL.update({
    "jupiter": [5.20288700, -0.00011607, 0.04838624, -0.00013253, 1.30439695, -0.00183714, 34.39644051,
                3034.74612775, 14.72847983, 0.21252668, 100.47390909, 0.20469106],
    "saturn": [9.53667594, -0.00125060, 0.05386179, -0.00050991, 2.48599187, 0.00193609, 49.95424423,
               1222.49362201, 92.59887831, -0.41897216, 113.66242448, -0.28867794],
    "uranus": [19.18916464, -0.00196176, 0.04725744, -0.00004397, 0.77263783, -0.00242939, 313.23810451,
               428.48202785, 170.95427630, 0.40805281, 74.01692503, 0.04240589],
    "neptune": [30.06992276, 0.00026291, 0.00859048, 0.00005105, 1.77004347, 0.00035372, -55.12002969,
                218.45945325, 44.96476227, -0.32241464, 131.78422574, -0.00508664],
    "pluto": [39.48211675, -0.00031596, 0.24882730, 0.00005170, 17.14001206, 0.00004818, 238.92903833,
              145.20780515, 224.06891629, -0.04062942, 110.30393684, -0.01183482]})
AU = C3M.AU


def pos(name, y, m, d):
    r, _ = C3M.planet_rv(name, C3M.jd_of(datetime(y, m, d)))
    return np.array(r[:2]) / AU

from scipy.integrate import solve_ivp


def arc(name1, d1, name2, d2, n=200):
    """Heliocentric Lambert arc between body1 at date d1 and body2 at date d2 (2-D projection, AU)."""
    j1, j2 = C3M.jd_of(datetime(*d1)), C3M.jd_of(datetime(*d2))
    r1, _ = C3M.planet_rv(name1, j1)
    r2, _ = C3M.planet_rv(name2, j2)
    tof = (j2 - j1) * 86400
    v1, _ = C3M.lambert(np.array(r1), np.array(r2), tof)
    f = lambda t, y: np.r_[y[3:], -C3M.MU_S * y[:3] / np.linalg.norm(y[:3]) ** 3]
    sol = solve_ivp(f, (0, tof), np.r_[r1, v1], t_eval=np.linspace(0, tof, n), rtol=1e-9, atol=1)
    return sol.y[0] / AU, sol.y[1] / AU


def unit(lon):
    return np.array([np.cos(np.radians(lon)), np.sin(np.radians(lon))])


def grandtour():
    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    ax.set_facecolor("#0B1630")
    th = np.linspace(0, 2 * np.pi, 400)
    for n in ["earth", "jupiter", "saturn", "uranus", "neptune"]:
        a = C3M.EL[n][0]
        ax.plot(a * np.cos(th), a * np.sin(th), color="#3A4A6A", lw=0.6, zorder=1)
    MISS = [
        ("Pioneer 10", "#9AA5B1", [("earth", (1972, 3, 3)), ("jupiter", (1973, 12, 4))], 70, "≈ 139 AU (silent since 2003)"),
        ("Pioneer 11", "#C9B98A", [("earth", (1973, 4, 6)), ("jupiter", (1974, 12, 3)), ("saturn", (1979, 9, 1))], 285,
         "≈ 118 AU (silent since 1995)"),
        ("Voyager 1", GOLD, [("earth", (1977, 9, 5)), ("jupiter", (1979, 3, 5)), ("saturn", (1980, 11, 12))], 255,
         "≈ 172 AU, 35° north of the ecliptic"),
        ("Voyager 2", SKY, [("earth", (1977, 8, 20)), ("jupiter", (1979, 7, 9)), ("saturn", (1981, 8, 26)),
                            ("uranus", (1986, 1, 24)), ("neptune", (1989, 8, 25))], 290, "≈ 144 AU, 34° south"),
        ("New Horizons", "#F08A8A", [("earth", (2006, 1, 19)), ("jupiter", (2007, 2, 28)), ("pluto", (2015, 7, 14))], 288,
         "≈ 66 AU"),
    ]
    for name, col, legs, lon, dist in MISS:
        for (b1, d1), (b2, d2) in zip(legs[:-1], legs[1:]):
            x, y = arc(b1, d1, b2, d2)
            ax.plot(x, y, color=col, lw=1.4, zorder=3)
        last = pos(legs[-1][0], *legs[-1][1])
        u = unit(lon)
        end = last + u * 13
        ax.annotate("", end, last, arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2, ls="--"), zorder=3)
    LBL = {"Pioneer 10": (17, 19), "Pioneer 11": (-21, -33), "Voyager 1": (-22, -22), "Voyager 2": (19, -44),
           "New Horizons": (23, -27)}
    for name, col, legs, lon, dist in MISS:
        x, y = LBL[name]
        legs = [m for m in MISS if m[0] == name][0]
        tip = pos(legs[2][-1][0], *legs[2][-1][1]) + unit(legs[3]) * 13
        ax.plot([x, tip[0]], [y, tip[1]], color=col, lw=0.5, ls=":", zorder=2)
        ax.text(x, y, f"{name}\n{dist}", color=col, fontsize=6.6, ha="center", va="center", zorder=6,
                bbox=dict(fc="#0B1630", ec=col, lw=0.6, boxstyle="round,pad=0.3"))
    enc = [("jupiter", (1979, 7, 9), "Jupiter\n1979 (V2)"), ("saturn", (1981, 8, 26), "Saturn\n1981 (V2)"),
           ("uranus", (1986, 1, 24), "Uranus\n1986"), ("neptune", (1989, 8, 25), "Neptune\n1989"),
           ("pluto", (2015, 7, 14), "Pluto\n2015")]
    off = {"jupiter": (-5, 1.5), "saturn": (-5, -3), "uranus": (6, 0), "neptune": (-6.5, 1), "pluto": (5.5, 2.5)}
    for n, d, t in enc:
        p = pos(n, *d)
        ax.plot(*p, "o", color="white", ms=4, zorder=5)
        ax.text(p[0] + off[n][0], p[1] + off[n][1], t, color="white", fontsize=6.4, ha="center", va="center", zorder=6)
    ax.plot(0, 0, "o", color=GOLD, ms=6, zorder=5)
    ax.set_xlim(-36, 36); ax.set_ylim(-50, 34)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)
    ax.text(-35, 32.5, "View from ecliptic north.\nSolid: Lambert arcs between\nthe actual encounter dates.\n"
                       "Dashed: direction of escape.\nDistances in October 2026.", color="#C8D0DC", fontsize=6.2,
            va="top")
    ax.plot([-33, -23], [-47, -47], color="white", lw=1.5)
    ax.text(-28, -46, "10 AU", color="white", fontsize=6.4, ha="center", va="bottom")
    save(fig, "ch26_grandtour")


def heliosphere():
    fig, ax = canvas(7.0, 4.6, xlim=(-265, 215), ylim=(-178, 178), bg="white")
    ax.set_aspect("equal")
    y = np.linspace(-178, 178, 300)
    xh = -120 + y ** 2 / 300
    ax.fill_betweenx(y, xh, 215, color="#E8EEF7", zorder=0)
    ax.plot(xh, y, color=NAVY, lw=1.8, zorder=2)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.fill(20 + 110 * np.cos(th), 95 * np.sin(th), color="#FFF4DC", zorder=1)
    ax.plot(20 + 110 * np.cos(th), 95 * np.sin(th), color=ORANGE, lw=1.3, ls="--", zorder=2)
    ax.plot(-178 + y ** 2 / 240, y, color=GREY, lw=1.0, ls=":", zorder=2)
    ax.add_patch(Circle((0, 0), 5, color=GOLD, zorder=5))
    label(ax, 0, -14, "Sun", fs=7)
    for yy in [-120, -60, 0, 60, 120]:
        arrow(ax, (-262, yy), (-232, yy), color=GREY, lw=1.0)
    label(ax, -262, 160, "Interstellar wind\n(≈ 26 km/s)", fs=6.6, color=GREY, ha="left")
    label(ax, -168, -150, "Bow wave", fs=6.4, color=GREY, ha="left")
    label(ax, 60, 40, "Supersonic\nsolar wind", fs=7, color=ORANGE)
    label(ax, 125, 128, "Heliosheath:\nslowed, heated\nsolar wind", fs=6.8, color=NAVY)
    label(ax, 150, -110, "Termination shock\n(dashed)", fs=6.6, color=ORANGE)
    label(ax, -40, 165, "Heliopause", fs=7, color=NAVY, weight="bold")
    for nm, ang, col, txt, ty in [("Voyager 1", 145, GOLD, "Voyager 1 (172 AU)\nTermination shock 94 AU, Dec 2004\n"
                                   "Heliopause 121.6 AU, Aug 2012", 120),
                                  ("Voyager 2", 215, SKY, "Voyager 2 (144 AU)\nTermination shock 84 AU, Aug 2007\n"
                                   "Heliopause 119 AU, Nov 2018", -120)]:
        R = 172 if nm == "Voyager 1" else 144
        u = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))])
        ax.plot([0, R * u[0]], [0, R * u[1]], color=col, lw=1.8, zorder=4)
        ax.plot(R * u[0], R * u[1], "o", color=col, ms=6, zorder=5, mec=INK, mew=0.5)
        ax.text(-262, ty, txt, fontsize=6.3, color=INK, va="center", ha="left",
                bbox=dict(fc="white", ec=col, lw=0.8, boxstyle="round,pad=0.3"), zorder=6)
    label(ax, 205, 0, "Heliotail →", fs=6.8, color=NAVY, ha="right")
    save(fig, "ch26_heliosphere")


def voyager_power():
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    yr = np.linspace(1977.7, 2036, 400)
    t = yr - 1977.7
    P0 = 470.0
    tau = 48.5 / np.log(P0 / 220.0)
    P = P0 * np.exp(-t / tau)
    Pu = P0 * 0.5 ** (t / 87.7)
    ax.plot(yr, P, color=RED, lw=2, label="Electrical output (model: 470 W at launch, ≈ 220 W in 2026)")
    ax.plot(yr, Pu, color=GREY, lw=1.2, ls="--", label="If only Pu-238 decay (87.7-year half-life) reduced output")
    events = [(1979.5, "Jupiter", (1983, 520)), (1980.9, "Saturn (V1)", (1986, 490)), (1986.1, "Uranus", (1991, 460)),
              (1989.6, "Neptune", (1985, 330)), (1990.1, "Pale Blue Dot;\ncameras off", (1994, 300)),
              (2012.6, "V1 heliopause", (2008, 220)), (2018.8, "V2 heliopause", (2014, 345)),
              (2025.2, "V1 CRS and\nV2 LECP off", (2022, 150)), (2026.3, "V1 LECP off", (2031, 255))]
    for x, tx, (lx, ly) in events:
        y = P0 * np.exp(-(x - 1977.7) / tau)
        ax.plot(x, y, "o", color=NAVY, ms=3.5, zorder=4)
        ax.annotate(tx, (x, y), xytext=(lx, ly), fontsize=6.0, ha="center",
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.5))
    ax.text(2032, 70, "2030s: last\ninstruments\nswitched off", fontsize=6.2, color=INK, ha="center")
    ax.set_xlabel("Year"); ax.set_ylabel("Power per spacecraft (W)")
    ax.set_xlim(1976, 2036); ax.set_ylim(0, 560)
    ax.legend(fontsize=6.0, loc="lower left")
    fig.text(0.99, 0.01, "Three MHW-RTGs per spacecraft. Output also falls as the thermocouples age; the decline is now "
                         "about 4 W per year.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch26_power")


def nh_encounter():
    v = 13.78
    dca = 12500 + 1188.0
    tt = np.linspace(-48, 6, 2000)
    rng = np.sqrt(dca ** 2 + (v * tt * 3600) ** 2)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.9))
    a1.semilogy(tt, rng * 4.96e-6 * 1000, color=BLUE, lw=1.8, label="LORRI (4.96 µrad pixels)")
    a1.semilogy(tt, rng * 20e-6 * 1000, color=ORANGE, lw=1.8, label="Ralph/MVIC colour (20 µrad)")
    a1.axhline(1188 * 2 * 1000 / 1024, color=GREY, lw=0.8, ls=":")
    a1.text(-47, 1188 * 2 * 1000 / 1024 * 1.2, "Pluto fills the 1024-pixel LORRI frame", fontsize=5.8, color=GREY)
    a1.set_xlabel("Hours from closest approach (14 July 2015, 11:50 UTC)")
    a1.set_ylabel("Resolution (m per pixel)")
    a1.legend(fontsize=5.8, loc="lower left")
    a1.set_title("(a) Resolution improves until closest approach", fontsize=7.6)
    w = v * dca / (dca ** 2 + (v * tt * 3600) ** 2)
    a2.semilogy(tt, np.degrees(w), color=RED, lw=1.8)
    a2.set_xlabel("Hours from closest approach")
    a2.set_ylabel("Angular rate of Pluto's centre (°/s)")
    a2.set_title("(b) …but the target sweeps past ever faster", fontsize=7.6)
    a2.axhline(np.degrees(4.96e-6 / 0.01), color=GREY, lw=0.8, ls=":")
    a2.text(-47, np.degrees(4.96e-6 / 0.01) * 1.25, "1 LORRI pixel per 10 ms exposure", fontsize=5.8, color=GREY)
    fig.text(0.99, 0.01, "Flyby speed 13.78 km/s; closest approach 12 500 km above Pluto's surface. Data were stored on board "
                         "and returned over the next 15 months.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch26_nhflyby")


def downlink():
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    d = np.logspace(np.log10(3), np.log10(200), 300)
    k = 1.380649e-23
    f = 8.415e9
    lam = 3e8 / f
    Pt = 21.3
    Gt = 0.55 * (np.pi * 3.66 / lam) ** 2
    req = 10 ** ((2.5 + 3.0) / 10)
    for D, T, col, lbl in [(70, 22, NAVY, "70 m DSN antenna"), (34, 30, BLUE, "34 m DSN antenna"),
                           (None, 22, GREEN, "Array: 70 m + three 34 m")]:
        if D is None:
            Gr = 0.6 * (np.pi * 70 / lam) ** 2 + 3 * 0.6 * (np.pi * 34 / lam) ** 2
        else:
            Gr = 0.6 * (np.pi * D / lam) ** 2
        L = (4 * np.pi * d * AU * 1e3 / lam) ** 2
        R = Pt * Gt * Gr / (L * k * T * req * 10 ** 0.3)
        ax.loglog(d, R, color=col, lw=1.6, label=lbl)
    pts = [(5.2, 115200, "Jupiter 1979\n115.2 kbit/s"), (9.6, 44800, "Saturn 1981\n44.8 kbit/s"),
           (19.2, 21600, "Uranus 1986\n21.6 kbit/s"), (30.1, 21600, "Neptune 1989\n21.6 kbit/s (arrays)"),
           (172, 160, "Voyager 1, 2026\n160 bit/s")]
    for x, y, t in pts:
        ax.plot(x, y, "o", color=ORANGE, ms=5, zorder=4)
        ax.annotate(t, (x, y), xytext=(6, 4), textcoords="offset points", fontsize=6.0)
    ax.set_xlabel("Distance from Earth (AU)")
    ax.set_ylabel("Achievable data rate (bit/s)")
    ax.set_xlim(3, 220); ax.set_ylim(30, 1e6)
    ax.legend(fontsize=6.2, loc="lower left")
    fig.text(0.99, 0.01, "Model: Voyager X-band link — 21.3 W, 3.66 m antenna, coded Eb/N0 ≈ 2.5 dB plus 3 dB margin.\n"
                         "At Jupiter and Saturn the DSN dishes were 64 m; for Uranus and Neptune they were enlarged and arrayed "
                         "with other radio telescopes.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, "ch26_downlink")


def entry():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.0), gridspec_kw=dict(width_ratios=[1.15, 1]))
    g = np.linspace(2, 70, 200)
    BOD = [("Jupiter, 47.4 km/s", 47.4, 27.0, VIOLET), ("Venus, 11.5 km/s", 11.5, 15.9, ORANGE),
           ("Earth, 11.0 km/s", 11.0, 7.2, BLUE), ("Mars, 5.8 km/s", 5.8, 11.1, RED), ("Titan, 6.0 km/s", 6.0, 40.0, GOLD)]
    for lbl, v, H, c in BOD:
        a = (v * 1e3) ** 2 * np.sin(np.radians(g)) / (2 * np.e * H * 1e3) / 9.81
        a1.semilogy(g, a, color=c, lw=1.6, label=lbl)
    a1.plot(8.5, (47400 ** 2 * np.sin(np.radians(8.5)) / (2 * np.e * 27000)) / 9.81, "o", color=NAVY, ms=5)
    a1.annotate("Galileo probe (1995):\nmodel 230 g, measured 228 g", (8.5, 230), xytext=(14, 900), fontsize=6.0,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.set_xlabel("Entry flight-path angle (°)")
    a1.set_ylabel("Peak deceleration (g)")
    a1.set_title("(a) Allen–Eggers peak deceleration", fontsize=7.6)
    a1.legend(fontsize=5.6, loc="lower right")
    a1.set_ylim(3, 3000)
    names = ["Galileo probe (Jupiter)", "Stardust capsule (Earth)", "OSIRIS-REx capsule (Earth)", "Pioneer Venus probes",
             "Apollo / Orion (Earth)", "Huygens (Titan)", "Curiosity (Mars)"]
    vals = [47.4, 12.9, 12.4, 11.5, 11.0, 6.0, 5.8]
    hbar(a2, names, vals, color=BLUE, fmt="{:.1f}", fs=6.2, highlight=["Galileo probe (Jupiter)"])
    a2.tick_params(axis="y", labelsize=6.2)
    a2.set_xlabel("Entry speed (km/s)")
    a2.set_title("(b) Entry speeds", fontsize=7.6)
    fig.text(0.99, 0.01, "Peak deceleration a = v² sin γ / (2 e H) for a ballistic entry into an exponential atmosphere of scale "
                         "height H; it does not depend on the vehicle's mass or shape.", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch26_entry")


def dart():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.0), gridspec_kw=dict(width_ratios=[1.2, 1]))
    a1.set_xlim(-2.0, 2.0); a1.set_ylim(-1.6, 1.6); a1.set_aspect("equal"); a1.axis("off")
    a1.add_patch(Circle((0, 0), 0.38, color="#8C7B6B", zorder=3))
    a1.text(0, 0, "Didymos\n≈ 760 m", ha="center", va="center", fontsize=6.4, color="white", zorder=4)
    th = np.linspace(0, 2 * np.pi, 300)
    a1.plot(1.19 * np.cos(th), 1.19 * np.sin(th), color=GREY, lw=1.0, ls="--")
    a1.plot(1.15 * np.cos(th), 1.15 * np.sin(th) * 0.97, color=RED, lw=1.0)
    a1.add_patch(Circle((0, -1.19), 0.1, color="#6B5B4B", zorder=4))
    a1.text(0.18, -1.36, "Dimorphos ≈ 150 m", fontsize=6.4, ha="left")
    a1.annotate("", (0, -1.12), (-1.3, -0.6), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
    a1.text(-1.95, -0.45, "DART, 580 kg\nat 6.1 km/s\n26 Sep 2022", fontsize=6.4, color=ORANGE)
    a1.annotate("", (0.6, -1.03), (0.15, -1.18), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.0))
    a1.text(0.45, -0.8, "orbital\nmotion", fontsize=6.0, color=NAVY)
    a1.text(0, 1.38, "Orbit radius ≈ 1.19 km. Period 11 h 55 min before, 11 h 22 min after.", fontsize=6.2, ha="center")
    a1.set_title("(a) The Didymos binary system", fontsize=7.6)
    labs = ["Mission requirement", "Expected with β = 1\n(no ejecta push)", "Measured"]
    vals = [73 / 60, 7.0, 33.0]
    a2.bar(range(3), vals, color=[GREY, BLUE, RED], width=0.6, zorder=2)
    a2.errorbar(2, 33.0, yerr=1.0, color=INK, capsize=4, zorder=3)
    for i, v in enumerate(vals):
        a2.text(i, v + 1.2, f"{v:.1f} min" if i else "73 s", ha="center", fontsize=6.8)
    a2.set_xticks(range(3)); a2.set_xticklabels(labs, fontsize=6.2)
    a2.set_ylabel("Change in orbital period (min)")
    a2.set_ylim(0, 40)
    a2.set_title("(b) Shortening of Dimorphos's orbit", fontsize=7.6)
    fig.text(0.99, 0.01, "Ejecta thrown back from the impact site multiplied the push: momentum enhancement β ≈ 3.6 "
                         "(2.2–4.9, depending on Dimorphos's density, which Hera will measure).", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch26_dart")


def history():
    fig, ax = canvas(7.0, 3.6, xlim=(1955, 2037), ylim=(-7.5, 7.5))
    ev = [(1959, 1, "Luna 1\nfirst escape"), (1962.9, -1, "Mariner 2\nVenus"), (1965.5, 3, "Mariner 4\nMars"),
          (1973.9, -3, "Pioneer 10\nJupiter"), (1974.2, 1, "Mariner 10\nVenus–Mercury"),
          (1979.3, -1, "Voyagers at\nJupiter"), (1981, 5, "Voyagers at\nSaturn"), (1986.1, -5, "Uranus;\nHalley Armada"),
          (1989.6, 3, "Neptune"), (1995.9, -1, "Galileo\nprobe"), (2005.5, 1, "Deep Impact"),
          (2012.6, -3, "Voyager 1\nheliopause"), (2015.5, 3, "New Horizons\nPluto"), (2019, -1, "Arrokoth"),
          (2022.7, 1, "DART"), (2025.3, -4, "Lucy:\nDonaldjohanson"), (2027.6, 5, "Lucy:\nfirst Trojans"),
          (2033.2, -2, "Lucy:\nPatroclus")]
    ax.plot([1956, 2036], [0, 0], color=NAVY, lw=2, zorder=2)
    for yr in range(1960, 2040, 10):
        ax.plot([yr, yr], [-0.25, 0.25], color=NAVY, lw=1)
        ax.text(yr, -0.45, str(yr), fontsize=6.0, color=GREY, ha="center", va="top", zorder=3,
                bbox=dict(fc="white", ec="none", pad=0.4))
    for x, lv, t in ev:
        yy = lv * 1.2
        ax.plot([x, x], [0, yy], color=GREY, lw=0.6, zorder=1)
        ax.plot([x], [0], "o", color=ORANGE, ms=4, zorder=3)
        ax.text(x, yy + (0.15 if lv > 0 else -0.15), t, ha="center", va="bottom" if lv > 0 else "top", fontsize=6.0,
                linespacing=1.1, zorder=4)
    save(fig, "ch26_history")


if __name__ == "__main__":
    fns = [grandtour, heliosphere, voyager_power, nh_encounter, downlink, entry, dart, history]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
