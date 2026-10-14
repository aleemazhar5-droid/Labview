import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, Wedge, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]


def history():
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ev = [(1960.4, "MIDAS\n(first IR\nwarning tests)"), (1963.8, "Vela\n(nuclear tests)"), (1970.9, "DSP-1"),
          (1976.0, "Oko (USSR,\nMolniya orbit)"), (1991.1, "Gulf War:\nScud warnings"), (2006.5, "SBIRS HEO\npayloads"),
          (2007.9, "Last DSP"), (2009.2, "SPIRALE\n(France demo)"), (2011.4, "SBIRS GEO-1"),
          (2015.9, "EKS Tundra\n(Russia)"), (2022.6, "SBIRS GEO-6\n(last)"), (2024.1, "HBTSS\nprototypes"),
          (2025.7, "SDA Tranche 1\ntracking")]
    timeline(ax, ev, y=0, x0=1958, x1=2028, stagger=3, height=1.0, fs=6.0)
    ax.set_xlim(1956, 2029)
    ax.set_ylim(-5.0, 5.0)
    ax.axis("off")
    for yr in range(1960, 2030, 10):
        ax.text(yr, -0.35, str(yr), fontsize=6.2, ha="center", va="top", color=GREY)
    save(fig, "ch20_history")


def g(x, c, w):
    return np.exp(-((x - c) / w) ** 2)


def plume_spectrum():
    l = np.linspace(1.5, 5.2, 800)
    c1, c2 = 1.191e8, 14387.8
    bb = c1 / l ** 5 / (np.exp(c2 / (l * 1800)) - 1)
    bands = 0.08 + 0.95 * g(l, 2.75, 0.13) + 3.2 * g(l, 4.45, 0.14) + 0.5 * g(l, 4.25, 0.07) + 0.25 * g(l, 1.87, 0.06)
    plume = bb * bands
    plume /= plume.max()
    atm = np.exp(-(3.5 * g(l, 2.7, 0.09) + 2.5 * g(l, 1.87, 0.05) + 1.2 * g(l, 1.38, 0.05) + 9 * g(l, 4.27, 0.06)
                   + 1.0 * g(l, 3.2, 0.25) * 0.3 + 0.6 * g(l, 5.0, 0.15)))
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.fill_between(l, 0, atm, color=SKY, alpha=0.25, label="Atmospheric transmission, ground to space")
    ax.plot(l, atm, color=BLUE, lw=1)
    ax.plot(l, plume, color=RED, lw=1.8, label="Rocket plume emission (normalised)")
    for c, t in [(2.75, "H₂O + CO₂\nband 2.7 µm"), (4.45, "CO₂ band\n4.3 µm")]:
        ax.text(c + 0.12, 0.62, t, fontsize=6.4, color=RED)
    ax.text(3.75, 0.88, "window: Earth\nbackground bright", fontsize=6.4, ha="center", color=BLUE)
    ax.set_xlim(1.5, 5.2)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Relative value")
    ax.legend(fontsize=6.5, loc="upper left")
    note(ax, "Schematic. In the strong absorption bands the Earth below appears dark, so a plume above the absorbing layer "
             "stands out.", xy=(1, -0.16))
    save(fig, "ch20_plume")


def altitude_visibility():
    z = np.linspace(0, 70, 400)
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    for tau0, H, c, n in [(80, 2.0, BLUE, "2.7 µm band (water vapour)"), (25, 7.5, GREEN, "4.3 µm band wing (CO₂)"),
                          (2000, 7.5, RED, "4.3 µm band centre (CO₂)"), (0.15, 7.5, GREY, "3.8 µm window")]:
        tr = np.exp(-tau0 * np.exp(-z / H))
        ax.plot(tr, z, color=c, lw=1.7, label=n)
    ax.set_xlabel("Fraction of plume emission reaching space")
    ax.set_ylabel("Altitude of the plume (km)")
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 70)
    ax.axhspan(0, 12, color=GREY, alpha=0.08)
    ax.text(0.98, 6, "clouds", fontsize=6.4, ha="right", color=GREY)
    ax.legend(fontsize=6.3, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)
    note(ax, "Idealised exponential absorbers with illustrative optical depths.", xy=(1, -0.16))
    save(fig, "ch20_visibility")


def ballistic(v0, gamma_deg, h0=200.0, dt=1.0):
    mu, R = 398600.4418, 6371.0
    r = np.array([0.0, R + h0])
    g0 = np.radians(gamma_deg)
    v = v0 * np.array([np.cos(g0), np.sin(g0)])
    pts = [r.copy()]
    t = 0
    while True:
        a = -mu * r / np.linalg.norm(r) ** 3
        v = v + a * dt
        r = r + v * dt
        t += dt
        pts.append(r.copy())
        if np.linalg.norm(r) < R or t > 4000:
            break
    P = np.array(pts)
    alt = np.linalg.norm(P, axis=1) - R
    ang = np.arctan2(P[:, 0], P[:, 1])
    rng = ang * R
    return rng, alt, np.arange(len(alt)) * dt


def trajectories():
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    # ICBM
    rng, alt, t = ballistic(7.0, 17.0)
    boost_r = np.linspace(0, 280, 50)
    boost_a = 200 * (boost_r / 280) ** 0.6
    ax.plot(boost_r, boost_a, color=RED, lw=2.5, label="Boost phase (bright plume, ≈ 3–5 min)")
    ax.plot(rng + 280, alt, color=NAVY, lw=1.6, label=f"ICBM midcourse (flight ≈ {(t[-1]+180)/60:.0f} min)")
    rng2, alt2, t2 = ballistic(4.0, 12.0, h0=80)
    b2r = np.linspace(0, 120, 30)
    ax.plot(b2r, 80 * (b2r / 120) ** 0.6, color=RED, lw=2.5)
    ax.plot(rng2 + 120, alt2, color=ORANGE, lw=1.5, label=f"Depressed SLBM trajectory (≈ {(t2[-1]+90)/60:.0f} min)")
    hr = np.linspace(0, 6000, 200)
    ha = np.where(hr < 200, 90 * (hr / 200) ** 0.6, 90 - 40 * np.clip((hr - 200) / 800, 0, 1))
    ha = np.where(hr > 1000, 50 - 10 * np.sin(hr / 600) * 0.4 - 20 * np.clip((hr - 5000) / 1000, 0, 1) ** 2, ha)
    ha = np.where(hr > 5800, ha * (6000 - hr) / 200, ha)
    ax.plot(hr, ha, color=GREEN, lw=1.6, ls="--", label="Hypersonic glide vehicle (schematic)")
    ax.set_xlabel("Ground range (km)")
    ax.set_ylabel("Altitude (km)")
    ax.set_xlim(0, 11000)
    ax.set_ylim(0, 1400)
    ax.legend(fontsize=6.4, loc="upper right")
    ins = ax.inset_axes([0.07, 0.52, 0.3, 0.42])
    ins.plot(boost_r, boost_a, color=RED, lw=2)
    ins.plot(rng + 280, alt, color=NAVY, lw=1)
    ins.plot(b2r, 80 * (b2r / 120) ** 0.6, color=RED, lw=2)
    ins.plot(rng2 + 120, alt2, color=ORANGE, lw=1.2)
    ins.plot(hr, ha, color=GREEN, lw=1.2, ls="--")
    ins.set_xlim(0, 2500)
    ins.set_ylim(0, 300)
    ins.tick_params(labelsize=5.5)
    ins.set_title("first 2 500 km, below 300 km", fontsize=6)
    i = np.argmax(alt)
    ax.annotate(f"apogee ≈ {alt[i]:.0f} km", (rng[i] + 280, alt[i]), xytext=(rng[i] + 1200, alt[i] + 120), fontsize=6.4,
                arrowprops=dict(arrowstyle="->", lw=0.6, color=GREY))
    note(ax, "Two-body trajectories after burnout (ICBM: 7.0 km/s at 17°; SLBM: 4.0 km/s at 12°). Glide vehicles "
             "fly low and manoeuvre,\nso they are harder to see from GEO and require low-orbit tracking sensors.",
         xy=(1, -0.16))
    save(fig, "ch20_trajectories")


def warning_timeline():
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    rows = [("ICBM, 10 000 km", [(0, 3.5, RED, "boost"), (3.5, 31, NAVY, "midcourse"), (31, 33, ORANGE, "re-entry")]),
            ("SLBM, depressed", [(0, 1.5, RED, ""), (1.5, 11, NAVY, ""), (11, 12, ORANGE, "")]),
            ("Space-based detection", [(0.5, 1.5, GREEN, ""), (1.5, 3, SKY, "")]),
            ("Radars (over horizon)", [(9, 31, VIOLET, "track by ground-based radars after they rise above the horizon")])]
    for j, (n, segs) in enumerate(rows):
        for a, b, c, t in segs:
            ax.add_patch(Rectangle((a, j - 0.3), b - a, 0.6, fc=c, alpha=0.8))
            if t:
                ax.text((a + b) / 2, j, t, ha="center", va="center", fontsize=6.0, color="white")
    ax.text(3.3, 2, "detect (green), assess and report (blue): first warning in ≈ 1–3 min", fontsize=6.2,
            va="center")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=7)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_xlim(0, 34)
    ax.set_xlabel("Minutes after launch")
    ax.grid(axis="y", visible=False)
    note(ax, "Illustrative. Space-based infrared sensors provide the first warning, within about a minute of launch.",
         xy=(1, -0.32))
    save(fig, "ch20_warning")


def arctic():
    import cartopy.crs as ccrs
    import cartopy.feature as cf
    fig = plt.figure(figsize=(6.2, 3.4))
    for k, (title, mode) in enumerate([("Coverage from GEO", "geo"), ("Coverage from HEO apogee", "heo")]):
        ax = fig.add_subplot(1, 2, k + 1, projection=ccrs.NorthPolarStereo())
        ax.set_extent([-180, 180, 40, 90], crs=ccrs.PlateCarree())
        ax.add_feature(cf.NaturalEarthFeature("physical", "land", "110m", fc="#E4E8DC", ec="none"))
        ax.coastlines(lw=0.4, color="#8A9AA8")
        th = np.linspace(-180, 180, 361)
        if mode == "geo":
            for lon0, c in [(-100, ORANGE), (10, ORANGE), (100, ORANGE)]:
                lat = np.degrees(np.arctan(np.cos(np.radians(70)) / np.cos(np.radians(th - lon0)) * 0))
            ax.fill_between(th, 40, 72, transform=ccrs.PlateCarree(), color=ORANGE, alpha=0.25)
            ax.plot(th, np.full_like(th, 72), transform=ccrs.PlateCarree(), color=ORANGE, lw=1.2)
            ax.text(0, 74, "≈ 72° N limit", transform=ccrs.PlateCarree(), fontsize=6.2, color=ORANGE)
        else:
            ax.fill_between(th, 40, 90, transform=ccrs.PlateCarree(), color=VIOLET, alpha=0.22)
            ax.text(-45, 55, "whole Arctic in view\nfor ≈ 8 h per orbit", transform=ccrs.PlateCarree(), fontsize=6.2,
                    color=VIOLET)
        ax.set_title(title, fontsize=7.6)
    note(fig.axes[1], "Schematic: GEO sensors view poorly beyond ≈ 70–75° latitude; Molniya/Tundra-type orbits fill "
                      "the polar gap.", xy=(1, -0.06))
    save(fig, "ch20_arctic")


def scan_stare():
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.9))
    for a in axs:
        a.set_xlim(-12, 12)
        a.set_ylim(-12, 12)
        a.set_aspect("equal")
        a.axis("off")
        a.add_patch(Circle((0, 0), 9, fc=EARTH, ec="none", alpha=0.85))
    a = axs[0]
    for ang in np.linspace(0, 2 * np.pi, 7)[:-1]:
        x, y = 5 * np.cos(ang), 5 * np.sin(ang)
        a.add_patch(Rectangle((x - 0.3, y - 2.2), 0.6, 4.4, angle=np.degrees(ang), fc=GOLD, alpha=0.35,
                              rotation_point="center"))
    a.add_patch(Rectangle((4.7, -2.2), 0.6, 4.4, fc=RED, alpha=0.9))
    a.add_patch(FancyArrowPatch((6.5, 3), (3, 6.5), connectionstyle="arc3,rad=0.4", arrowstyle="-|>",
                                mutation_scale=10, color=INK))
    a.set_title("Scanning (DSP): spinning satellite sweeps\na linear detector array around the disc every ≈ 10 s",
                fontsize=6.8)
    a = axs[1]
    a.add_patch(Rectangle((-8, -8), 16, 16, fc="none", ec=ORANGE, lw=1.4, ls="--"))
    a.add_patch(Rectangle((1, 2), 5, 5, fc=RED, alpha=0.5, ec=RED))
    a.text(3.5, 7.6, "steerable\nnarrow field", fontsize=6.2, ha="center", va="bottom", color=RED)
    a.text(0, -9.6, "wide-field staring array", fontsize=6.2, color=ORANGE, ha="center", va="top")
    a.set_title("Staring (SBIRS, Next-Gen OPIR): large\nfocal-plane arrays watch continuously", fontsize=6.8)
    save(fig, "ch20_scanstare")


def detect():
    R = np.logspace(2, 4.7, 200) * 1e3
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for I, c in [(1e3, SKY), (1e4, BLUE), (1e5, NAVY), (1e6, RED)]:
        E = I / R ** 2 / 1e4
        ax.plot(R / 1e3, E, color=c, lw=1.5, label=f"source {I:.0e} W/sr".replace("e+0", "e"))
    ax.axhspan(1e-17, 1e-15, color=GREEN, alpha=0.12)
    ax.text(150, 2e-16, "typical sensitivity range of space IR sensors (illustrative)", fontsize=6.4, color=GREEN)
    for x, n in [(1000, "LEO 1 000 km"), (35786, "GEO")]:
        ax.axvline(x, color=GREY, lw=0.7, ls=":")
        ax.text(x * 1.05, 1e-9, n, fontsize=6.4, color=GREY, rotation=90, va="top")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(100, 50000)
    ax.set_ylim(1e-18, 1e-7)
    ax.set_xlabel("Range to source (km)")
    ax.set_ylabel("Irradiance at sensor (W/cm²)")
    ax.legend(fontsize=6.4, loc="upper right")
    note(ax, "Inverse-square law, no atmosphere. Brighter booster plumes are easily seen from GEO; dimmer targets favour "
             "closer LEO sensors.", xy=(1, -0.16))
    save(fig, "ch20_detect")


def clutter():
    rng = np.random.default_rng(5)
    n = 160
    from scipy.ndimage import gaussian_filter
    bg = gaussian_filter(rng.normal(0, 1, (n, n)), 6) * 40 + 100
    clouds = gaussian_filter(rng.random((n, n)) > 0.985, 3) * 400
    frames = []
    for k in range(6):
        f = bg + clouds + rng.normal(0, 1.2, (n, n))
        x, y = 40 + 12 * k, 110 - 9 * k
        yy, xx = np.mgrid[0:n, 0:n]
        f += 7 * np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / 2.0)
        frames.append(f)
    diff = frames[5] - np.median(frames[:5], axis=0)
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.5))
    axs[0].imshow(frames[5], cmap="gray")
    axs[0].set_title("Single frame (target invisible\nagainst clutter)", fontsize=7)
    axs[1].imshow(diff, cmap="gray", vmin=-4, vmax=8)
    axs[1].set_title("Frame minus background\n(target appears)", fontsize=7)
    tr = np.array([(40 + 12 * k, 110 - 9 * k) for k in range(6)])
    axs[2].imshow(diff, cmap="gray", vmin=-4, vmax=8)
    axs[2].plot(tr[:, 0], tr[:, 1], "o-", color=RED, ms=3, lw=1)
    axs[2].set_title("Track from successive frames\n(direction and speed)", fontsize=7)
    for a in axs:
        a.axis("off")
    fig.text(0.5, 0.02, "Simulated infrared frames: a faint moving source is detected by background subtraction "
             "and temporal tracking.", ha="center", fontsize=6.4, color=GREY)
    save(fig, "ch20_clutter", raster=True)


def layers():
    fig, ax = canvas(7.0, 3.6, xlim=(-60, 60), ylim=(-36, 36))
    earth(ax, 0, 0, 7)
    for r, c, n, pos in [(10, GREEN, "LEO tracking layer\n(≈ 1 000 km)", (33, -20)),
                         (19, SKY, "MEO warning/tracking\n(Space Force Epoch 1)", (-59, -4)),
                         (31, ORANGE, "GEO: SBIRS / Next-Gen OPIR GEO", (24, 30))]:
        ax.add_patch(Circle((0, 0), r, fc="none", ec=c, lw=1.4))
        ax.text(*pos, n, fontsize=6.4, color=c)
    ax.add_patch(Ellipse((0, 13), 22, 50, fc="none", ec=VIOLET, lw=1.4))
    ax.text(-30, 33, "HEO / polar: SBIRS HEO,\nNext-Gen OPIR Polar", fontsize=6.4, color=VIOLET)
    for ang in np.linspace(0, 2 * np.pi, 13)[:-1]:
        satellite(ax, 10 * np.cos(ang), 10 * np.sin(ang), s=0.35)
    for ang in (0.3, 2.4, 4.4):
        satellite(ax, 31 * np.cos(ang), 31 * np.sin(ang), s=0.6)
    for ang in (1.0, 3.1, 5.2):
        satellite(ax, 19 * np.cos(ang), 19 * np.sin(ang), s=0.5)
    satellite(ax, 0, 38 - 1.5, s=0.5)
    save(fig, "ch20_layers")


def detectors():
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    items = [("InGaAs", 0.9, 1.7, 250, 300, GREEN), ("PbS", 1.0, 3.0, 190, 240, GOLD),
             ("InSb", 1.0, 5.5, 70, 85, BLUE), ("HgCdTe (MCT)", 1.0, 14.0, 60, 200, RED),
             ("Type-II superlattice / nBn", 3.0, 12.0, 80, 160, VIOLET), ("QWIP", 7.5, 10.5, 40, 70, SKY),
             ("Microbolometer (uncooled)", 8.0, 14.0, 290, 310, GREY)]
    for n, l0, l1, t0, t1, c in items:
        ax.add_patch(Rectangle((l0, t0), l1 - l0, t1 - t0, fc=c, alpha=0.35, ec=c, lw=1.2))
        ax.text(l1 + 0.15 if n != "HgCdTe (MCT)" else 9.0, (t0 + t1) / 2 if n != "HgCdTe (MCT)" else 175, n,
                fontsize=6.6, color=c, va="center")
    for lam, t in [(2.7, "2.7 µm"), (4.3, "4.3 µm")]:
        ax.axvline(lam, color=ORANGE, lw=0.8, ls="--")
        ax.text(lam + 0.1, 318, t, fontsize=6.4, color=ORANGE)
    ax.set_xlim(0.5, 16)
    ax.set_ylim(20, 330)
    ax.set_xlabel("Spectral range (µm)")
    ax.set_ylabel("Typical operating temperature (K)")
    note(ax, "Approximate ranges. Longer-wavelength photon detectors must be cooled to suppress dark current; "
             "missile-warning sensors use SWIR and MWIR bands.", xy=(1, -0.2))
    save(fig, "ch20_detectors")


def ground_flow():
    fig, ax = canvas(7.0, 2.8, xlim=(0, 100), ylim=(0, 38))
    steps = [("IR satellites\n(GEO, HEO, LEO)", LIGHT, NAVY), ("Relay and\nground stations", LIGHT, NAVY),
             ("Mission control:\nfusion, tracks,\nlaunch & impact points", "#FFF4E5", ORANGE),
             ("Warning centres\n(e.g. NORAD)", LIGHT, NAVY), ("National leaders;\nmissile defence;\nforces & allies",
                                                               "#E8F5E9", GREEN)]
    for i, (t, fc, ec) in enumerate(steps):
        box(ax, 1 + i * 20, 14, 17, 15, t, fs=6.6, fc=fc, ec=ec)
        if i < len(steps) - 1:
            arrow(ax, (18 + i * 20, 21.5), (21 + i * 20, 21.5))
    label(ax, 50, 6, "Target timelines: detection to report in ≈ 1–3 minutes; continuous updates through the flight",
          fs=6.6, color=GREY)
    save(fig, "ch20_groundflow")


if __name__ == "__main__":
    fns = [history, plume_spectrum, altitude_visibility, trajectories, warning_timeline, arctic, scan_stare, detect,
           clutter, layers, detectors, ground_flow]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
