import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Ellipse, Wedge

ROOT = Path(__file__).resolve().parents[2]


def geometry():
    fig, ax = canvas(7.0, 3.9, xlim=(0, 100), ylim=(0, 56))
    ax.plot([2, 98], [6, 6], color="#8B7D5A", lw=2)
    ax.add_patch(Rectangle((2, 2), 96, 4, fc="#E9E1C9", ec="none"))
    sx, sy = 14, 48
    satellite(ax, sx, sy, s=1.1)
    ax.annotate("", (34, 48), (20, 48), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.2))
    label(ax, 27, 50.5, "flight (azimuth) direction", fs=6.8, color=NAVY)
    ax.plot([sx, sx], [sy - 2, 6], color=GREY, lw=0.8, ls="--")
    label(ax, sx - 2.0, 4.2, "nadir", fs=6.6, color=GREY)
    near, far = 46, 88
    ax.add_patch(Polygon([[sx + 1, sy - 2], [near, 6], [far, 6]], closed=True, fc=ORANGE, alpha=0.18, ec="none"))
    for x in (near, far):
        ax.plot([sx + 1, x], [sy - 2, 6], color=ORANGE, lw=1)
    mid = (near + far) / 2
    ax.plot([sx + 1, mid], [sy - 2, 6], color=RED, lw=1.2, ls="--")
    label(ax, 43, 30, "slant range R", fs=7, color=RED, rot=-44)
    darrow(ax, (near, 9), (far, 9), color=NAVY)
    label(ax, mid, 11.2, "swath (ground range)", fs=7, color=NAVY)
    label(ax, near, 3.6, "near range", fs=6.6)
    label(ax, far, 3.6, "far range", fs=6.6)
    # look angle arc
    th = np.linspace(np.pi * 1.5, np.pi * 1.5 + np.arctan((mid - sx) / (sy - 6)), 30)
    ax.plot(sx + 1 + 7 * np.cos(th), sy - 2 + 7 * np.sin(th), color=INK, lw=0.8)
    label(ax, sx + 5.5, sy - 12, "look\nangle θ", fs=6.6)
    # incidence angle at mid
    ax.plot([mid, mid], [6, 18], color=GREY, lw=0.8)
    a0 = np.pi / 2
    a1 = np.pi / 2 + np.arctan((mid - sx) / (sy - 6))
    t2 = np.linspace(a0, a1, 30)
    ax.plot(mid + 6 * np.cos(t2), 6 + 6 * np.sin(t2), color=INK, lw=0.8)
    label(ax, mid - 12, 19.5, "incidence\nangle θᵢ", fs=6.6)
    label(ax, mid + 2, 19.5, "local vertical", fs=6.2, color=GREY, ha="left")
    box(ax, 62, 30, 34, 18, "Side-looking geometry\nθᵢ > θ because of Earth curvature\nTypical θᵢ = 20–50°\nSwath 5–400 km depending on mode",
        fs=6.8, fc="white")
    save(fig, "ch15_geometry")


def chirp():
    B, T = 50e6, 10e-6
    fs = 400e6
    t = np.arange(-T / 2, T / 2, 1 / fs)
    k = B / T
    s = np.exp(1j * np.pi * k * t ** 2)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.8), gridspec_kw=dict(wspace=0.3))
    a1.plot(t * 1e6, k * t / 1e6, color=BLUE, lw=1.6)
    a1.set_xlabel("Time within pulse (µs)")
    a1.set_ylabel("Instantaneous frequency offset (MHz)")
    a1.set_title(f"Transmitted chirp: {T*1e6:.0f} µs, {B/1e6:.0f} MHz sweep", fontsize=7.8)
    a1.set_xlim(-5, 5)
    a1.text(0.5, -20, "frequency rises linearly\n(\"chirp\") during the pulse", fontsize=6.6, color=GREY)
    rx = np.zeros(8 * len(t), complex)
    rx[len(t) * 3:len(t) * 4] = s
    mf = np.convolve(rx, np.conj(s[::-1]), mode="same")
    tt = (np.arange(len(rx)) - len(rx) / 2) / fs - 0.5 * len(t) / fs
    p = 20 * np.log10(np.abs(mf) / np.abs(mf).max() + 1e-9)
    i0 = np.argmax(p)
    tc = (np.arange(len(rx)) - i0) / fs
    a2.plot(tc * 1e9, p, color=NAVY, lw=1)
    a2.set_xlim(-120, 120)
    a2.set_ylim(-40, 3)
    a2.set_xlabel("Time from peak (ns)")
    a2.set_ylabel("Compressed output (dB)")
    a2.set_title("After matched filtering", fontsize=7.8)
    a2.axhline(-3, color=ORANGE, lw=0.8, ls="--")
    a2.text(28, -14, f"−3 dB width ≈ {0.886/B*1e9:.0f} ns\n→ slant-range resolution ≈ 3 m", fontsize=6.6, color=ORANGE)
    note(a2, "Time–bandwidth product 500: the 1.5 km-long pulse is compressed to ≈ 3 m.", xy=(1, -0.24))
    save(fig, "ch15_chirp")


def synthetic():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 100), ylim=(0, 46))
    ax.plot([4, 96], [6, 6], color="#8B7D5A", lw=2)
    tx, ty = 50, 6
    ax.plot(tx, ty, "*", color=RED, ms=11, zorder=5)
    label(ax, tx, 2.5, "point target", fs=6.8, color=RED)
    xs = [22, 36, 50, 64, 78]
    for i, x in enumerate(xs):
        satellite(ax, x, 38, s=0.8)
        ax.add_patch(Polygon([[x, 36.5], [x - 14, 6], [x + 14, 6]], closed=True, fc=ORANGE, alpha=0.07, ec=ORANGE,
                             lw=0.4))
        ax.plot([x, tx], [36.5, ty], color=BLUE, lw=0.6, ls=":")
    darrow(ax, (22, 43.5), (78, 43.5), color=NAVY, text="synthetic aperture  L_sa = λR / L", fs=7, toff=(0, 0.3))
    label(ax, 8, 38, "real antenna\nlength L", fs=6.6, ha="left")
    box(ax, 66, 13, 31, 14, "Stripmap azimuth resolution\nδa ≈ L / 2\nindependent of range and λ", fs=6.8,
        fc="white")
    box(ax, 3, 13, 31, 14, "Real-aperture resolution\nδa = λR / L ≈ 4.7 km\n(C-band, R = 850 km, L = 10 m)",
        fs=6.8, fc="white")
    save(fig, "ch15_synthetic")


def penetration():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 100), ylim=(0, 46))
    ax.add_patch(Rectangle((0, 0), 100, 6, fc="#C9B98F", ec="none"))
    rng = np.random.default_rng(1)
    for x in np.arange(6, 98, 9):
        h = rng.uniform(22, 28)
        ax.plot([x, x], [6, 6 + h * 0.6], color="#7A5230", lw=2.2, zorder=2)
        ax.add_patch(Ellipse((x, 6 + h * 0.75), 10, h * 0.55, fc="#3E7D46", ec="none", alpha=0.85, zorder=2))
    bands = [("X  3.1 cm", 12, 33, BLUE), ("C  5.6 cm", 32, 27, SKY), ("S  9.4 cm", 50, 21, GREEN),
             ("L  24 cm", 68, 9, ORANGE), ("P  69 cm", 86, 3.5, RED)]
    for name, x, ystop, c in bands:
        ax.annotate("", (x, ystop), (x, 45), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2), zorder=4)
        label(ax, x + 1.2, 43.5, name, fs=7, color=c, ha="left", weight="bold")
    label(ax, 50, -2.0, "Longer wavelengths penetrate deeper into vegetation (and dry sand, snow and ice).", fs=6.8,
          color=GREY)
    ax.set_ylim(-4, 46)
    save(fig, "ch15_penetration")


def mechanisms():
    fig, axs = plt.subplots(1, 4, figsize=(7.0, 2.2))
    for a in axs:
        a.set_xlim(0, 10)
        a.set_ylim(0, 8)
        a.set_aspect("equal")
        a.axis("off")
    a = axs[0]
    a.plot([0.5, 9.5], [1.5, 1.5], color="#555", lw=1.5)
    a.annotate("", (5, 1.5), (1, 6.5), arrowprops=dict(arrowstyle="-|>", color=ORANGE))
    a.annotate("", (9, 6.5), (5, 1.5), arrowprops=dict(arrowstyle="-|>", color=BLUE))
    a.set_title("Smooth surface\n(specular: dark)", fontsize=7.2)
    a = axs[1]
    xx = np.linspace(0.5, 9.5, 60)
    a.plot(xx, 1.5 + 0.35 * np.sin(xx * 5) * np.cos(xx * 2.3), color="#555", lw=1.2)
    a.annotate("", (5, 1.6), (1, 6.5), arrowprops=dict(arrowstyle="-|>", color=ORANGE))
    for ang in (35, 65, 95, 125, 150):
        r = np.radians(ang)
        a.annotate("", (5 + 2.4 * np.cos(r), 1.6 + 2.4 * np.sin(r)), (5, 1.6),
                   arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.8))
    a.set_title("Rough surface\n(diffuse: bright)", fontsize=7.2)
    a = axs[2]
    a.plot([0.5, 9.5], [1.5, 1.5], color="#555", lw=1.5)
    a.add_patch(Rectangle((6.5, 1.5), 1.6, 5, fc="#BBB", ec="#555"))
    a.plot([1, 4.8, 6.5], [6.2, 1.5, 4.0], color=ORANGE, lw=1)
    a.annotate("", (1.3, 6.9), (6.5, 4.0), arrowprops=dict(arrowstyle="-|>", color=BLUE))
    a.set_title("Double bounce\n(buildings: very bright)", fontsize=7.2)
    a = axs[3]
    a.plot([0.5, 9.5], [1.2, 1.2], color="#555", lw=1.5)
    a.add_patch(Ellipse((5, 4.0), 7, 4.4, fc="#3E7D46", alpha=0.5, ec="none"))
    a.plot([1, 4.6], [7.4, 4.3], color=ORANGE, lw=1)
    rng = np.random.default_rng(4)
    pts = [(4.6, 4.3), (3.6, 3.4), (5.6, 3.0), (4.7, 2.4), (6.3, 4.6)]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        a.plot([x0, x1], [y0, y1], color=ORANGE, lw=0.8)
    a.annotate("", (8.8, 7.4), (6.3, 4.6), arrowprops=dict(arrowstyle="-|>", color=BLUE))
    a.set_title("Volume scattering\n(forest canopy)", fontsize=7.2)
    fig.text(0.5, 0.02, "Orange: incident wave from the radar (upper left); blue: scattered energy.", ha="center",
             fontsize=6.6, color=GREY)
    save(fig, "ch15_mechanisms")


def distortions():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 100), ylim=(0, 44))
    ax.plot([2, 98], [8, 8], color="#8B7D5A", lw=1.5)
    mts = [([8, 30, 42], 7, "Foreshortening"), ([42, 54, 66], 12, "Layover"), ([70, 76, 82], 14, "Shadow")]
    look = np.radians(35)
    d = np.array([np.sin(look), -np.cos(look)])
    for (x0, xp, x1), h, name in mts:
        ax.add_patch(Polygon([[x0, 8], [xp, 8 + h], [x1, 8]], closed=True, fc="#C9B98F", ec="#8B7D5A"))
        label(ax, xp, 2.8, name, fs=7.2, weight="bold")
    for xs in np.arange(-10, 90, 6):
        ax.plot([xs, xs + 40 * d[0]], [44, 44 + 40 * d[1]], color=ORANGE, lw=0.5, alpha=0.6)
    tpk = (22 - 8) / np.cos(look)
    xe = 76 + tpk * np.sin(look)
    ax.add_patch(Polygon([[76, 22], [xe, 8], [82, 8]], closed=True, fc="#555", alpha=0.45, ec="none"))
    ax.plot([76, xe], [22, 8], color="#555", lw=0.6, ls="--")
    label(ax, xe + 1, 10.5, "radar shadow", fs=6.3, color="#333", ha="left")
    label(ax, 50, 41.5, "radar illumination from the upper left (look angle 35°)", fs=6.8, color=ORANGE)
    box(ax, 3, 25, 30, 10, "Slope facing the radar (gentler\nthan θ) is compressed and bright", fs=6.4, fc="white")
    box(ax, 36, 25, 28, 10, "Slope steeper than θ: the peak is\nimaged before (over) its base", fs=6.4, fc="white")
    box(ax, 67, 25, 30, 10, "Back slope steeper than 90° − θ\nis hidden from the radar", fs=6.4, fc="white")
    save(fig, "ch15_distortions")


def speckle():
    rng = np.random.default_rng(7)
    n = 240
    scene = np.full((n, n), 0.05)
    scene[:, 80:160] = 0.2
    scene[:, 160:] = 0.6
    yy, xx = np.mgrid[0:n, 0:n]
    scene[(xx - 60) ** 2 + (yy - 170) ** 2 < 25 ** 2] = 1.0
    scene[30:60, 180:215] = 0.02

    def look(L):
        I = np.zeros_like(scene)
        for _ in range(L):
            I += scene * rng.exponential(1.0, scene.shape)
        return I / L
    fig, axs = plt.subplots(1, 4, figsize=(7.0, 2.2), gridspec_kw=dict(wspace=0.08))
    imgs = [scene, look(1), look(4), look(16)]
    tl = ["Noise-free scene", "1 look", "4 looks", "16 looks"]
    for a, im, t in zip(axs, imgs, tl):
        a.imshow(10 * np.log10(im + 1e-4), cmap="gray", vmin=-22, vmax=3, interpolation="nearest")
        a.set_title(t, fontsize=7.6)
        a.axis("off")
    fig.text(0.5, 0.02, "Simulated fully developed speckle (exponential intensity statistics); displayed in dB.",
             ha="center", fontsize=6.4, color=GREY)
    save(fig, "ch15_speckle", raster=True)


def antenna():
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    inc = np.radians(np.linspace(15, 50, 100))
    Re, h = 6371e3, 650e3
    v = 7.5e3
    for lam, c, n in [(0.031, BLUE, "X-band (3.1 cm)"), (0.0555, GREEN, "C-band (5.6 cm)"), (0.094, GOLD, "S-band (9.4 cm)"),
                      (0.238, ORANGE, "L-band (24 cm)")]:
        look = np.arcsin(Re / (Re + h) * np.sin(inc))
        R = (Re + h) * np.cos(look) - np.sqrt(Re ** 2 - ((Re + h) * np.sin(look)) ** 2)
        A = 4 * v * lam * R * np.tan(inc) / 3e8
        ax.plot(np.degrees(inc), A, color=c, lw=1.6, label=n)
    pts = [("ICEYE (X)", 30, 3.2 * 0.4), ("Sentinel-1 (C)", 35, 12.3 * 0.82), ("ALOS-2 (L)", 35, 9.9 * 2.9),
           ("NISAR 12 m reflector (L)", 37, np.pi * 6 ** 2)]
    for n, x, y in pts:
        ax.plot(x, y, "s", color=NAVY, ms=5)
        ax.annotate(n, (x, y), xytext=(6, -3), textcoords="offset points", fontsize=6.6)
    ax.set_yscale("log")
    ax.set_xlabel("Incidence angle (°)")
    ax.set_ylabel("Minimum antenna area (m²)")
    ax.set_xlim(15, 50)
    ax.set_ylim(0.2, 300)
    ax.legend(fontsize=6.7, loc="upper left")
    note(ax, "A > 4vλR tanθᵢ / c for unambiguous single-beam stripmap imaging; 650 km altitude. "
             "NISAR's SweepSAR technique avoids the limit.", xy=(1, -0.16))
    save(fig, "ch15_antenna")


def sigma0():
    th = np.linspace(5, 60, 200)
    t = np.radians(th)
    calm = 10 * np.log10(8 * np.exp(-np.tan(t) ** 2 / 0.012) / np.cos(t) ** 4 + 10 ** (-3.0))
    rough = 10 * np.log10(1.5 * np.exp(-np.tan(t) ** 2 / 0.08) / np.cos(t) ** 4 + 10 ** (-2.3) * np.cos(t) ** 2)
    soil = 10 * np.log10(0.25 * np.cos(t) ** 2.6)
    forest = 10 * np.log10(0.2 * np.cos(t) ** 0.6)
    urban = 10 * np.log10(1.0 * np.cos(t) ** 1.2)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for y, c, n in [(urban, VIOLET, "Urban (double bounce)"), (forest, GREEN, "Forest (volume)"),
                    (soil, "#8C564B", "Moist bare soil"), (rough, SKY, "Wind-roughened sea"), (calm, BLUE, "Calm water")]:
        ax.plot(th, y, color=c, lw=1.6, label=n)
    ax.set_xlim(5, 60)
    ax.set_ylim(-32, 12)
    ax.set_xlabel("Incidence angle (°)")
    ax.set_ylabel("Backscatter σ⁰ (dB)")
    ax.legend(fontsize=6.7, loc="upper right")
    ax.text(31, -29.8, "calm water and smooth surfaces appear black", fontsize=6.4, color=BLUE)
    note(ax, "Schematic C-band VV behaviour; actual values depend on wavelength, polarisation, moisture and roughness.",
         xy=(1, -0.16))
    save(fig, "ch15_sigma0")


def modes():
    fig, axs = plt.subplots(1, 4, figsize=(7.0, 2.6))
    for a in axs:
        a.set_xlim(0, 10)
        a.set_ylim(0, 14)
        a.set_aspect("equal")
        a.axis("off")
        a.plot([1, 1], [0.5, 13.5], color=GREY, lw=0.8)
        a.annotate("", (1, 13.6), (1, 11.5), arrowprops=dict(arrowstyle="-|>", color=GREY))
    a = axs[0]
    a.add_patch(Rectangle((4, 1), 2.5, 12, fc=BLUE, alpha=0.6))
    a.set_title("Stripmap", fontsize=7.8)
    a.text(5.2, -0.6, "3–5 m, 30–80 km", fontsize=6.2, ha="center", color=GREY)
    a = axs[1]
    cols = [BLUE, SKY, NAVY]
    for j, x in enumerate([3, 5, 7]):
        for k, y in enumerate(np.arange(1, 13, 2.4)):
            a.add_patch(Rectangle((x, y + 0.8 * j), 2, 2.4, fc=cols[j], alpha=0.55, ec="white", lw=0.4))
    a.set_title("ScanSAR / TOPS", fontsize=7.8)
    a.text(5.8, -0.6, "20–100 m, 250–500 km", fontsize=6.2, ha="center", color=GREY)
    a = axs[2]
    a.add_patch(Rectangle((4.5, 5.5), 2.5, 3, fc=ORANGE, alpha=0.8))
    for y in (1.5, 4, 7, 10, 12.5):
        a.plot([1.2, 5.75], [y, 7], color=ORANGE, lw=0.6, alpha=0.7)
    a.set_title("Spotlight", fontsize=7.8)
    a.text(5.5, -0.6, "0.25–1 m, 3–10 km", fontsize=6.2, ha="center", color=GREY)
    a = axs[3]
    for y in np.arange(1, 13, 3):
        a.add_patch(Rectangle((4, y), 2.5, 1.2, fc=RED, alpha=0.6))
    a.add_patch(Rectangle((7.2, 2), 2.3, 9, fc=SKY, alpha=0.3, ec=SKY))
    a.text(8.35, 6.5, "sweep\nbeams", fontsize=6, ha="center", rotation=90, va="center")
    a.set_title("Wave / SweepSAR", fontsize=7.8)
    a.text(5.5, -0.6, "special modes", fontsize=6.2, ha="center", color=GREY)
    fig.text(0.5, 0.0, "Grey arrow: satellite ground track and direction of flight. The radar looks to one side.",
             ha="center", fontsize=6.4, color=GREY)
    save(fig, "ch15_modes")


def res_swath():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    groups = {
        "Sentinel-1": (BLUE, [("SM", 5, 80), ("IW", 10, 250), ("EW", 28, 400)]),
        "NISAR": (ORANGE, [("L-band", 7, 240)]),
        "TerraSAR-X": (GREEN, [("Staring Spotlight", 0.25, 4), ("Stripmap", 3, 30), ("ScanSAR", 18, 100),
                               ("Wide ScanSAR", 40, 270)]),
        "RADARSAT Constellation": (VIOLET, [("Spotlight", 1.5, 20), ("High res.", 5, 30), ("Low res.", 100, 500)]),
        "ICEYE": (RED, [("Dwell", 0.25, 5), ("Strip", 3, 30), ("Scan", 15, 100)]),
        "Capella": (GOLD, [("Spotlight", 0.5, 5), ("Stripmap", 1.2, 10)]),
    }
    for g, (c, pts) in groups.items():
        xs = [p[1] for p in pts]
        ys = [p[2] for p in pts]
        ax.plot(xs, ys, "o-", color=c, ms=4.5, lw=0.8, label=g)
        for n, x, y in pts:
            ax.annotate(n, (x, y), xytext=(6, -2) if g == "Capella" else (4, -9 if g == "TerraSAR-X" else 4), textcoords="offset points",
                        fontsize=5.8, color=c)
    x = np.logspace(-1, 2.5, 50)
    ax.plot(x, x * 20000 / 1000, color=GREY, ls=":", lw=0.8)
    ax.text(1.6, 40, "20 000 pixels across swath", fontsize=6.2, color=GREY, rotation=31)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.15, 200)
    ax.set_ylim(2, 800)
    ax.set_xlabel("Resolution (m)")
    ax.set_ylabel("Swath width (km)")
    ax.legend(fontsize=6.4, loc="lower right")
    note(ax, "Approximate values from operator specifications.", xy=(1, -0.15))
    save(fig, "ch15_resswath")


def insar_geom():
    fig, ax = canvas(7.0, 3.4, xlim=(0, 100), ylim=(0, 48))
    ax.plot([2, 98], [6, 6], color="#8B7D5A", lw=1.5)
    ax.add_patch(Polygon([[55, 6], [66, 14], [78, 6]], closed=True, fc="#C9B98F", ec="#8B7D5A"))
    s1, s2 = (14, 40), (24, 44)
    satellite(ax, *s1, s=0.9)
    satellite(ax, *s2, s=0.9)
    label(ax, 10, 44, "pass 1", fs=6.8)
    label(ax, 27.5, 47.2, "pass 2 (days later)", fs=6.8, ha="left")
    P = (66, 14)
    ax.plot([s1[0], P[0]], [s1[1] - 1, P[1]], color=BLUE, lw=1)
    ax.plot([s2[0], P[0]], [s2[1] - 1, P[1]], color=ORANGE, lw=1)
    label(ax, 37, 22.5, "R₁", fs=7.5, color=BLUE)
    label(ax, 48, 30.5, "R₂", fs=7.5, color=ORANGE)
    darrow(ax, (15, 41.5), (23, 45.5), color=NAVY)
    label(ax, 17, 46.0, "baseline B", fs=6.8, color=NAVY)
    box(ax, 1, 9, 44, 11, "Interferometric phase  φ = 4π (R₂ − R₁) / λ\n(+ topography, deformation, atmosphere, noise)",
        fs=6.6, fc="white")
    box(ax, 60, 26, 37, 16, "One fringe (2π) =\n• λ/2 of motion along the line of sight\n  (2.8 cm at C-band, 12 cm at L-band)\n"
        "• height of ambiguity λR sinθ / (2 B_perp)\n  of topography", fs=6.5, fc="white", ha="left")
    save(fig, "ch15_insargeom")


def mogi():
    n = 300
    x = np.linspace(-20e3, 20e3, n)
    X, Y = np.meshgrid(x, x)
    d, dV, nu = 4e3, 12e6, 0.25
    r2 = X ** 2 + Y ** 2
    coef = (1 - nu) * dV / np.pi
    uz = coef * d / (d ** 2 + r2) ** 1.5
    ux = coef * X / (d ** 2 + r2) ** 1.5
    inc = np.radians(35)
    los = uz * np.cos(inc) - ux * np.sin(inc)
    lam = 0.0555
    phase = np.mod(4 * np.pi * los / lam, 2 * np.pi)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw=dict(width_ratios=[1, 1.25], wspace=0.35))
    im = a1.imshow(phase, cmap="hsv", extent=(-20, 20, -20, 20), origin="lower")
    a1.set_xlabel("East (km)", fontsize=7)
    a1.set_ylabel("North (km)", fontsize=7)
    a1.tick_params(labelsize=6.5)
    a1.set_title("Wrapped C-band interferogram", fontsize=7.6)
    a1.annotate("", (-14, 15), (-19, 15), arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4))
    a1.text(-19, 16.5, "look", fontsize=6.4, color="white")
    j = n // 2
    a2.plot(x / 1e3, uz[j] * 100, color=NAVY, lw=1.5, label="Vertical uplift")
    a2.plot(x / 1e3, ux[j] * 100, color=GREEN, lw=1.2, label="East displacement")
    a2.plot(x / 1e3, los[j] * 100, color=ORANGE, lw=1.5, ls="--", label="Line-of-sight change")
    a2.set_xlabel("East (km)", fontsize=7)
    a2.set_ylabel("Displacement (cm)", fontsize=7)
    a2.tick_params(labelsize=6.5)
    a2.legend(fontsize=6.2, loc="upper right")
    a2.set_title("Profile through the centre", fontsize=7.6)
    note(a2, "Mogi point source: 12 million m³ at 4 km depth; incidence 35°.", xy=(1, -0.2))
    save(fig, "ch15_mogi", raster=True)


def coherence():
    t = np.linspace(0, 120, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    for g0, ginf, tau, c, n in [(0.95, 0.85, 200, NAVY, "Urban / bare rock (any band)"),
                                (0.85, 0.35, 60, ORANGE, "Vegetated land, L-band"),
                                (0.75, 0.15, 12, GREEN, "Vegetated land, C-band"),
                                (0.6, 0.05, 4, BLUE, "Cropland in growing season, X-band")]:
        ax.plot(t, ginf + (g0 - ginf) * np.exp(-t / tau), color=c, lw=1.6, label=n)
    ax.axhline(0.3, color=GREY, lw=0.7, ls=":")
    ax.text(118, 0.32, "usable threshold ≈ 0.3", fontsize=6.4, color=GREY, ha="right")
    ax.set_xlabel("Time between acquisitions (days)")
    ax.set_ylabel("Interferometric coherence")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=6.6, loc="upper right")
    note(ax, "Schematic temporal decorrelation behaviour.", xy=(1, -0.18))
    save(fig, "ch15_coherence")


def timeline_fig():
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ev = [(1978.5, "Seasat"), (1981.9, "SIR-A"), (1987.5, "Kosmos-1870\n(Almaz)"), (1991.6, "ERS-1"),
          (1992.2, "JERS-1"), (1994.3, "SIR-C/X-SAR"), (1995.9, "RADARSAT-1"), (2000.1, "SRTM"),
          (2002.2, "Envisat"), (2006.1, "ALOS"), (2007.5, "TerraSAR-X,\nCOSMO-SkyMed"), (2010.5, "TanDEM-X"),
          (2014.3, "Sentinel-1A,\nALOS-2"), (2018.0, "ICEYE-X1,\nSAOCOM"), (2019.5, "RCM"),
          (2020.6, "Capella"), (2025.4, "BIOMASS,\nNISAR"), (2025.9, "Sentinel-1D")]
    timeline(ax, ev, y=0, x0=1976, x1=2028, stagger=3, height=1.0, fs=6.2)
    ax.set_xlim(1975, 2029)
    ax.set_ylim(-4.6, 4.6)
    ax.axis("off")
    for yr in range(1980, 2030, 10):
        ax.text(yr, -0.35, str(yr), fontsize=6.2, ha="center", va="top", color=GREY)
    save(fig, "ch15_timeline")


def fleets():
    d = json.load(open(ROOT / "data/eo_fleets.json"))["sar"]
    d.pop("Yaogan (China, military)", None)
    items = sorted(d.items(), key=lambda kv: -kv[1])
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    gov = ["Sentinel-1", "NISAR", "COSMO-SkyMed", "RADARSAT", "TerraSAR/TanDEM-X", "PAZ", "ALOS-2/4", "SAOCOM",
           "EOS-04/RISAT", "BIOMASS"]
    hbar(ax, [k for k, _ in items], [v for _, v in items], color=BLUE, highlight=gov, fs=6.8)
    ax.tick_params(axis="y", labelsize=6.8)
    ax.set_xlabel("Active satellites (14 Oct 2026)")
    note(ax, "Orange: government programmes; blue: commercial. Name-matched active payloads in the CelesTrak SATCAT\n"
             "(approximate). China's Yaogan series (≈170 satellites of several types) is not shown.", xy=(1, -0.17))
    save(fig, "ch15_fleets")


if __name__ == "__main__":
    fns = [geometry, chirp, synthetic, penetration, mechanisms, distortions, speckle, antenna, sigma0, modes, res_swath,
           insar_geom, mogi, coherence, timeline_fig, fleets]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
