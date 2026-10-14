import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse

BODIES = {"Moon": (4902.8, 1737.4, 2.03e-4, 27.32), "Mercury": (22032.0, 2439.7, 5.0e-5, 58.65),
          "Venus": (324859.0, 6051.8, 4.46e-6, -243.0), "Earth": (398600.4, 6378.1, 1.0826e-3, 0.99727),
          "Mars": (42828.4, 3396.2, 1.9605e-3, 1.02596)}
YEAR = {"Mars": 686.98, "Earth": 365.256}


def sso():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    for n, c in [("Mars", RED), ("Earth", BLUE)]:
        mu, R, J2, _ = BODIES[n]
        h = np.linspace(150, 1500, 300)
        a = R + h
        nmot = np.sqrt(mu / a ** 3)
        need = 2 * np.pi / (YEAR[n] * 86400)
        cosi = -need / (1.5 * nmot * J2 * (R / a) ** 2)
        i = np.degrees(np.arccos(np.clip(cosi, -1, 1)))
        ax.plot(h, i, color=c, lw=1.8, label=f"{n}")
    for nme, h, i in [("Mars Global Surveyor / MRO / Odyssey (≈ 92.9–93.2°)", 300, 93.0), ("Landsat (98.2°)", 705, 98.2)]:
        ax.plot(h, i, "o", color=NAVY, ms=5)
        ax.annotate(nme, (h, i), xytext=(8, 4), textcoords="offset points", fontsize=6.4)
    ax.set_xlabel("Circular orbit altitude (km)")
    ax.set_ylabel("Sun-synchronous inclination (°)")
    ax.legend(fontsize=6.6, loc="upper left")
    ax.set_xlim(150, 1500)
    note(ax, "cos i = −(dΩ/dt)_required / [1.5 n J₂ (R/a)²]. Mars's larger J₂ and longer year make its sun-synchronous "
             "orbits nearly polar.", xy=(1, -0.16))
    save(fig, "ch25_sso")


def periods():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    for n, c in [("Moon", GREY), ("Mercury", "#8C564B"), ("Mars", RED), ("Venus", ORANGE), ("Earth", BLUE)]:
        mu, R, _, _ = BODIES[n]
        h = np.logspace(1.7, 4.3, 200)
        T = 2 * np.pi * np.sqrt((R + h) ** 3 / mu) / 60
        ax.plot(h, T, color=c, lw=1.6, label=n)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Altitude of circular orbit (km)")
    ax.set_ylabel("Orbital period (minutes)")
    for p, nme in [(120, "2 h"), (1440, "1 day")]:
        ax.axhline(p, color=GREY, lw=0.5, ls=":")
        ax.text(55, p * 1.08, nme, fontsize=6.3, color=GREY)
    ax.legend(fontsize=6.6, loc="lower right")
    note(ax, "Two-body periods. Low lunar orbits last about 2 hours; a low Mars orbit about 1 h 50 min.", xy=(1, -0.16))
    save(fig, "ch25_periods")


def mars_timeline():
    rows = [("Mariner 9 (USA)", 1971.9, 1972.8), ("Viking 1 & 2 orbiters (USA)", 1976.5, 1980.6),
            ("Phobos 2 (USSR)", 1989.1, 1989.3), ("Mars Global Surveyor (USA)", 1997.7, 2006.9),
            ("Mars Odyssey (USA)", 2001.8, 2026.8), ("Mars Express (ESA)", 2003.98, 2026.8),
            ("Mars Reconnaissance Orbiter (USA)", 2006.2, 2026.8), ("MAVEN (USA)", 2014.7, 2026.8),
            ("Mangalyaan / MOM (India)", 2014.7, 2022.7), ("ExoMars TGO (ESA/Russia)", 2016.8, 2026.8),
            ("Hope (UAE)", 2021.1, 2026.8), ("Tianwen-1 orbiter (China)", 2021.1, 2026.8)]
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    for j, (n, a, b) in enumerate(rows):
        c = BLUE if "USA" in n else (GREEN if "ESA" in n else (RED if "China" in n else (ORANGE if "India" in n else
                                                                                      (VIOLET if "UAE" in n else GREY))))
        ax.barh(j, b - a, left=a, color=c, height=0.6)
        ax.text(a - 0.3, j, n, ha="right", va="center", fontsize=6.3)
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_xlim(1955, 2028)
    ax.set_xlabel("Year")
    ax.grid(axis="y", visible=False)
    note(ax, "Periods in orbit around Mars (bars extending to 2026 are still operating). Orbiters also relay most "
             "data from landers and rovers.", xy=(1, -0.16))
    save(fig, "ch25_marstimeline")


def juno_orbit():
    fig, ax = canvas(7.0, 3.5, xlim=(-20, 110), ylim=(-32, 32))
    for r, a in [(6, 0.18), (4, 0.25), (2.6, 0.32)]:
        ax.add_patch(Ellipse((0, 0), 2 * r * 1.6, 2 * r, fc=RED, alpha=a * 0.6, ec="none"))
    label(ax, 0, -13, "most intense radiation belts", fs=6.2, color=RED)
    ax.add_patch(Circle((0, 0), 1.6, fc="#D8B48A", ec="#8C6A3E"))
    t = np.linspace(0, 2 * np.pi, 400)
    a, e = 55, 0.98
    r = a * (1 - e ** 2) / (1 + e * np.cos(t))
    x, y = r * np.cos(t), r * np.sin(t)
    ang = np.radians(80)
    xr, yr = x * np.cos(ang) - y * np.sin(ang), x * np.sin(ang) + y * np.cos(ang)
    ax.plot(xr * 0.55 + 0, yr * 0.55, color=BLUE, lw=1.4)
    label(ax, 7, 25, "53-day polar orbit:\nperijove ≈ 4 000 km above the clouds,\napojove ≈ 8 million km", fs=6.4,
          color=BLUE, ha="left")
    label(ax, 3.5, 3.2, "fast dive\nunder the belts", fs=5.8, color=BLUE, ha="left")
    box(ax, 40, -28, 66, 22, "Radiation design:\n• electronics in a 1 cm titanium vault (≈ 180 kg)\n• polar orbit "
        "passes between the belts and the\n  atmosphere, minimising dose per orbit\n• orbit precesses with time, "
        "gradually increasing dose", fs=6.2, fc="white", ha="left")
    save(fig, "ch25_juno")


def relay():
    fig, ax = canvas(7.0, 3.0, xlim=(0, 100), ylim=(0, 40))
    planet(ax, 30, -55, 70, "#C1440E")
    ax.add_patch(Rectangle((27, 13.5), 3, 1.6, fc=NAVY))
    label(ax, 28.5, 11.2, "rover", fs=6.4, color="white")
    satellite(ax, 50, 30, s=0.7)
    label(ax, 50, 34, "orbiter (MRO, TGO, MAVEN, Odyssey)", fs=6.4)
    ax.plot([29, 49], [15.5, 29], color=GREEN, lw=1.4)
    label(ax, 33, 23, "UHF relay\n≈ 0.25–2 Mbit/s\n≈ 10 min pass", fs=6.0, color=GREEN)
    earth(ax, 92, 32, 4)
    ax.plot([52, 88], [30.5, 32], color=ORANGE, lw=1.4, ls="--")
    label(ax, 72, 35.5, "X-band to DSN", fs=6.2, color=ORANGE)
    ax.plot([29, 88], [16, 29], color=GREY, lw=0.7, ls=":")
    label(ax, 74, 22, "direct-to-Earth X-band:\nlow rate (kbit/s)", fs=6.0, color=GREY)
    save(fig, "ch25_relay")


def finale():
    fig, ax = canvas(7.0, 3.2, xlim=(-24, 24), ylim=(-11, 11))
    ax.add_patch(Circle((0, 0), 6, fc="#E3C78F", ec="#B08D4C", zorder=2))
    for x0, x1, a_ in [(7.3, 9.3, 0.5), (9.6, 12.5, 0.8), (12.8, 14.5, 0.6)]:
        for sgn in (1, -1):
            ax.add_patch(Rectangle((sgn * x0 if sgn > 0 else -x1, -0.25), x1 - x0, 0.5, fc="#C9B48A", alpha=a_, ec="none",
                                   zorder=3))
    t = np.linspace(-3.2, 3.2, 200)
    for k, dx in enumerate(np.linspace(6.35, 7.0, 6)):
        ax.plot(dx + 0.55 * t ** 2, 3.2 * t, color=BLUE, lw=0.8, alpha=0.75, zorder=4)
    tt = np.linspace(-3.2, 0.0, 100)
    ax.plot(5.2 + 0.7 * tt ** 2, 3.2 * tt + 0.0, color=RED, lw=1.4, zorder=4)
    ax.annotate("gap between the rings\nand the atmosphere (≈ 2 000 km)", (6.7, 0.3), xytext=(-21, 8), fontsize=6.4,
                color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.7))
    label(ax, 17, 7, "22 Grand Finale orbits\n(April–September 2017)", fs=6.4, color=BLUE)
    label(ax, 15, -8.5, "final plunge into Saturn's\natmosphere, 15 September 2017", fs=6.4, color=RED)
    label(ax, -12, -2.2, "rings (edge-on)", fs=6.2, color="#8A6D3B")
    save(fig, "ch25_finale")


def sounder():
    fig, ax = canvas(7.0, 3.0, xlim=(0, 100), ylim=(0, 40))
    satellite(ax, 50, 36, s=0.8)
    ax.add_patch(Rectangle((0, 0), 100, 20, fc="#D9B48F", ec="none"))
    ax.add_patch(Rectangle((0, 6), 100, 6, fc="#BFD7EA", ec="none"))
    label(ax, 85, 9, "buried ice layer", fs=6.4, color=BLUE)
    label(ax, 85, 16, "dust and regolith", fs=6.4, color="#6E4B2A")
    for x0 in (44, 50, 56):
        ax.plot([50, x0], [34.5, 20], color=ORANGE, lw=0.8)
        ax.plot([x0, x0 + 0.5], [20, 12], color=ORANGE, lw=0.8, ls="--")
    label(ax, 30, 28, "radar pulses (MHz frequencies)\nreflect from the surface and\nfrom subsurface interfaces", fs=6.3,
          color=ORANGE)
    box(ax, 63, 23, 35, 12, "MARSIS (Mars Express): 1.8–5 MHz, km depth\nSHARAD (MRO): 20 MHz, 15 m vertical\nresolution, "
        "hundreds of metres depth", fs=6.0, fc="white")
    save(fig, "ch25_sounder")


def insertion():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.0))
    mu, R = 42828.4, 3396.2
    vinf = np.linspace(1.5, 5.0, 200)
    rp = R + 300
    for lbl, ra, c in [("300 km circular orbit", R + 300, RED), ("1-sol ellipse (24.6 h)", None, ORANGE),
                       ("35-hour ellipse (MRO capture)", None, GOLD), ("Barely captured (parabolic)", np.inf, GREY)]:
        if lbl.startswith("1-sol"):
            a = (mu * (88775.0 / (2 * np.pi)) ** 2) ** (1 / 3); ra = 2 * a - rp
        elif lbl.startswith("35"):
            a = (mu * (35 * 3600 / (2 * np.pi)) ** 2) ** (1 / 3); ra = 2 * a - rp
        vhyp = np.sqrt(vinf ** 2 + 2 * mu / rp)
        vcap = np.sqrt(2 * mu / rp) if np.isinf(ra) else np.sqrt(2 * mu * ra / (rp * (rp + ra)))
        a1.plot(vinf, (vhyp - vcap), color=c, lw=1.8, label=lbl)
    a1.set_xlabel("Arrival $v_\\infty$ (km/s)")
    a1.set_ylabel("Insertion Δv (km/s)")
    a1.set_title("(a) Mars: Δv depends on the capture orbit", fontsize=7.6)
    a1.legend(fontsize=5.8, loc="upper left")
    a1.set_ylim(0, 3.2)
    PL = [("Mercury", 22032.0, 2439.7, "#8C564B"), ("Venus", 324859.0, 6051.8, ORANGE), ("Mars", 42828.4, 3396.2, RED),
          ("Jupiter", 1.26687e8, 71492.0, VIOLET), ("Saturn", 3.7931e7, 60268.0, BLUE)]
    v = np.linspace(1, 10, 200)
    for n, m, Rb, c in PL:
        rp = 1.1 * Rb if n in ("Jupiter", "Saturn") else Rb + 400
        ra = 100 * Rb
        dv = np.sqrt(v ** 2 + 2 * m / rp) - np.sqrt(2 * m * ra / (rp * (rp + ra)))
        a2.plot(v, dv, color=c, lw=1.8, label=n)
    a2.set_xlabel("Arrival $v_\\infty$ (km/s)")
    a2.set_title("(b) Capture into an ellipse with apoapsis 100 R", fontsize=7.6)
    a2.legend(fontsize=6.0, loc="upper left")
    a2.set_ylim(0, 4)
    fig.text(0.99, 0.01, "Periapsis 300 km in (a); 400 km (1.1 R for the giants) in (b). A deep gravity well makes capture "
                          "cheap: the burn is made where the spacecraft is fastest (the Oberth effect).",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch25_insertion")


def aerobrake():
    mu, R = 42828.4, 3396.2
    rho, beta, H, hp = 4.5e-8, 18.0, 10.0, 100.0
    rp, ra = R + hp, R + 45000.0
    t = 0.0; T = []; A = []; P = []; D = []
    while ra - R > 460:
        a = (rp + ra) / 2; per = 2 * np.pi * np.sqrt(a ** 3 / mu)
        vp = np.sqrt(2 * mu * ra / (rp * (rp + ra)))
        dv = rho * vp * 1e3 / (2 * beta) * np.sqrt(2 * np.pi * rp * H)
        vp2 = vp - dv
        a2 = -mu / (2 * (vp2 ** 2 / 2 - mu / rp)); ra = 2 * a2 - rp
        t += per; T.append(t / 86400); A.append(ra - R); P.append(per / 3600); D.append(dv * 1e3)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.9))
    a1.plot(T, np.array(A) / 1000, color=RED, lw=1.8)
    a1.set_xlabel("Days of aerobraking")
    a1.set_ylabel("Apoapsis altitude (1 000 km)")
    ax2 = a1.twinx(); ax2.plot(T, P, color=BLUE, lw=1.2, ls="--"); ax2.set_ylabel("Orbit period (h)", color=BLUE)
    ax2.tick_params(axis="y", colors=BLUE)
    a1.set_title(f"(a) {len(T)} drag passes in {T[-1]:.0f} days", fontsize=7.6)
    a2.plot(np.arange(1, len(D) + 1), D, color=NAVY, lw=1.4)
    a2.set_xlabel("Drag pass number")
    a2.set_ylabel("Δv per pass (m/s)")
    a2.set_title(f"(b) Total Δv from drag ≈ {sum(D)/1000:.2f} km/s", fontsize=7.6)
    fig.text(0.99, 0.01, "Model: periapsis 100 km, density held at 4.5×10⁻⁸ kg/m³ by corridor control, scale height "
                          "10 km, ballistic coefficient 18 kg/m², drag applied impulsively at periapsis.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch25_aerobrake")


if __name__ == "__main__":
    fns = [sso, periods, mars_timeline, juno_orbit, relay, finale, sounder, insertion, aerobrake]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
