import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[2]
HC_K = 14387.77  # hc/k in um*K


def planck(lam_um, T):
    """Spectral radiance, W m-2 sr-1 um-1."""
    c1 = 1.191042e8  # 2hc^2 in W um^4 m-2 sr-1
    return c1 / lam_um ** 5 / (np.exp(HC_K / (lam_um * T)) - 1)


def inv_planck(lam_um, L):
    c1 = 1.191042e8
    return HC_K / (lam_um * np.log(c1 / (lam_um ** 5 * L) + 1))


def landsat_timeline():
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    missions = [("Landsat 1", 1972.56, 1978.05, "MSS (80 m)", BLUE), ("Landsat 2", 1975.06, 1982.15, "MSS", BLUE),
                ("Landsat 3", 1978.18, 1983.75, "MSS", BLUE), ("Landsat 4", 1982.54, 1993.95, "TM (30 m) + MSS", GREEN),
                ("Landsat 5", 1984.17, 2013.05, "TM + MSS - 28.8 years, a record", GREEN),
                ("Landsat 6", 1993.76, 1993.80, "launch failure", RED),
                ("Landsat 7", 1999.29, 2024.05, "ETM+ (15 m pan)", ORANGE),
                ("Landsat 8", 2013.12, 2026.8, "OLI + TIRS", VIOLET), ("Landsat 9", 2021.74, 2026.8, "OLI-2 + TIRS-2", VIOLET),
                ("Landsat Next", 2031.0, 2033.5, "planned, under review", GREY)]
    for i, (n, a, b, s, c) in enumerate(missions):
        hatch = "///" if n == "Landsat Next" else None
        ax.barh(i, b - a, left=a, color=c if not hatch else "white", ec=c, hatch=hatch, height=0.6, zorder=2)
        tx = b + 0.4 if n not in ("Landsat 8", "Landsat 9") else a - 0.4
        ax.text(tx, i, s, va="center", ha="left" if tx > b else "right", fontsize=6.6)
    ax.set_yticks(range(len(missions)))
    ax.set_yticklabels([m[0] for m in missions], fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(1970, 2036)
    ax.axvline(2008.7, color=GOLD, lw=1.2, ls="--")
    ax.text(2009.2, 5.0, "archive made free\n(Oct 2008)", fontsize=6.4, color=GOLD, va="center")
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Year of science operations")
    note(ax, "Bars show years of science data acquisition. Source: USGS Landsat mission pages.", xy=(1, -0.17))
    save(fig, "ch14_landsat")


def bands():
    sensors = {
        "PlanetScope\nSuperDove": [(0.431, 0.452), (0.465, 0.515), (0.513, 0.549), (0.547, 0.583), (0.600, 0.620),
                                   (0.650, 0.680), (0.697, 0.713), (0.845, 0.885)],
        "WorldView-3": [(0.40, 0.45), (0.45, 0.51), (0.51, 0.58), (0.585, 0.625), (0.63, 0.69), (0.705, 0.745),
                        (0.77, 0.895), (0.86, 1.04), (1.195, 1.225), (1.55, 1.59), (1.64, 1.68), (1.71, 1.75),
                        (2.145, 2.185), (2.185, 2.225), (2.235, 2.285), (2.295, 2.365)],
        "Sentinel-2 MSI": [(0.433, 0.453), (0.458, 0.523), (0.543, 0.578), (0.650, 0.680), (0.698, 0.713),
                           (0.733, 0.748), (0.773, 0.793), (0.785, 0.900), (0.855, 0.875), (0.935, 0.955),
                           (1.360, 1.390), (1.565, 1.655), (2.100, 2.280)],
        "Landsat 8/9\nOLI + TIRS": [(0.433, 0.453), (0.450, 0.515), (0.525, 0.600), (0.630, 0.680), (0.845, 0.885),
                                    (1.360, 1.390), (1.560, 1.660), (2.100, 2.300), (10.6, 11.19), (11.5, 12.51)],
        "Terra ASTER": [(0.52, 0.60), (0.63, 0.69), (0.78, 0.86), (8.125, 8.475), (8.475, 8.825), (8.925, 9.275),
                        (10.25, 10.95), (10.95, 11.65)],
        "ECOSTRESS": [(8.11, 8.47), (8.61, 8.95), (9.03, 9.37), (10.31, 10.67), (11.85, 12.33)],
    }
    pans = {"WorldView-3": (0.45, 0.80), "Landsat 8/9\nOLI + TIRS": (0.50, 0.68)}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[3.2, 1], wspace=0.06))
    names = list(sensors)
    cols = [GREEN, NAVY, BLUE, VIOLET, ORANGE, RED]
    for i, n in enumerate(names):
        for ax in (a1, a2):
            for lo, hi in sensors[n]:
                ax.add_patch(Rectangle((lo, i - 0.28), hi - lo, 0.56, fc=cols[i], ec="white", lw=0.4, alpha=0.85))
            if n in pans:
                lo, hi = pans[n]
                ax.add_patch(Rectangle((lo, i + 0.3), hi - lo, 0.14, fc=GREY, ec="none"))
    for ax, xl in ((a1, (0.39, 2.42)), (a2, (8.0, 12.6))):
        ax.set_xlim(*xl)
        ax.set_ylim(len(names) - 0.4, -0.6)
        ax.grid(axis="y", visible=False)
    for lo, hi, t in [(0.4, 0.7, "VIS"), (0.7, 1.3, "NIR"), (1.3, 2.42, "SWIR")]:
        a1.text((lo + hi) / 2, -0.52, t, ha="center", fontsize=6.6, color=GREY)
    a2.text(10.3, -0.52, "TIR", ha="center", fontsize=6.6, color=GREY)
    a1.set_yticks(range(len(names)))
    a1.set_yticklabels(names, fontsize=6.8)
    a2.set_yticks([])
    a1.set_xlabel("Wavelength (µm)")
    a2.set_xlabel("Wavelength (µm)")
    a1.text(1.9, 4.0, "ASTER SWIR bands\nfailed in 2008", fontsize=6.2, color=GREY, ha="center", va="center")
    note(a1, "Grey bars: panchromatic bands. Band limits from operator specifications.", xy=(0, -0.17), ha="left")
    save(fig, "ch14_bands")


def optics():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    D = np.logspace(np.log10(0.05), np.log10(4), 200)
    lam = 0.6e-6
    for h, c in [(300e3, GREEN), (500e3, BLUE), (700e3, NAVY)]:
        ax.plot(D, 1.22 * lam * h / D, color=c, lw=1.4, label=f"Diffraction limit, {h/1e3:.0f} km")
    pts = [("Sentinel-2 MSI (10 m)", 0.15, 10, 786), ("PlanetScope Dove", 0.09, 3.7, 475),
           ("SkySat", 0.35, 0.65, 500), ("Pléiades 1A/B", 0.65, 0.70, 694), ("GeoEye-1", 1.1, 0.41, 681),
           ("WorldView-3", 1.1, 0.31, 617)]
    offs = {"Sentinel-2 MSI (10 m)": (6, 0), "PlanetScope Dove": (6, 2), "SkySat": (6, 0), "Pléiades 1A/B": (6, 2),
            "GeoEye-1": (6, 3), "WorldView-3": (-4, -11)}
    for n, d, g_, h in pts:
        ax.plot(d, g_, "o", color=ORANGE, ms=5, zorder=3)
        ax.annotate(n, (d, g_), xytext=offs[n], textcoords="offset points", fontsize=6.6)
    ax.axhline(0.1, color=GREY, lw=0.8, ls=":")
    ax.text(0.055, 0.112, "10 cm", fontsize=6.4, color=GREY)
    ax.annotate("10 cm from 500 km needs\na ≈3.7 m aperture", (3.66, 0.1), xytext=(1.25, 0.03), fontsize=6.6,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.05, 4)
    ax.set_ylim(0.02, 30)
    ax.set_xlabel("Telescope aperture diameter D (m)")
    ax.set_ylabel("Ground resolution (m)")
    ax.legend(fontsize=6.8, loc="upper right")
    note(ax, "Rayleigh criterion 1.22 λh/D at λ = 0.6 µm. Points: published GSD (pan) and aperture.", xy=(1, -0.15))
    save(fig, "ch14_optics")


def photons():
    L, eta, Eph = 100.0, 0.4, 6.626e-34 * 3e8 / 0.6e-6
    systems = [("Sentinel-2\n10 m, green", 0.15, 786e3, 10.0, 0.035), ("PlanetScope\n3.7 m, green", 0.09, 475e3, 3.7, 0.036),
               ("SkySat\n0.65 m pan", 0.35, 500e3, 0.65, 0.45), ("Pléiades\n0.7 m pan", 0.65, 694e3, 0.70, 0.35),
               ("WorldView-3\n0.31 m pan", 1.1, 617e3, 0.31, 0.35)]
    names, ne = [], []
    for n, D, h, gsd, dl in systems:
        A = np.pi * D ** 2 / 4
        omega = (gsd / h) ** 2
        vg = 7.9e3 * np.sqrt(6371e3 / (6371e3 + h)) * 6371e3 / (6371e3 + h)
        t = gsd / vg
        N = L * dl * A * omega * t * eta / Eph
        names.append(n)
        ne.append(N)
        print(f"{n.replace(chr(10),' '):28s} t={t*1e6:7.1f} us  e-={N:9.0f}  TDI for 1e4: {1e4/N:6.1f}")
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    x = np.arange(len(names))
    ax.bar(x, ne, color=[BLUE, BLUE, ORANGE, ORANGE, ORANGE], zorder=2, width=0.6)
    ax.set_yscale("log")
    ax.axhline(1e4, color=GREEN, lw=1.2, ls="--")
    ax.text(4.45, 1.25e4, "10 000 e⁻ → shot-noise SNR ≈ 100", fontsize=6.6, color=GREEN, ha="right")
    for xi, v in zip(x, ne):
        stages = 1e4 / v
        txt = f"{v:,.0f} e⁻" + (f"\n×{int(np.ceil(stages))} needed" if stages > 1 else "")
        ax.text(xi, v * 1.25, txt, ha="center", fontsize=6.4, va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=6.6)
    ax.set_ylim(10, 3e5)
    ax.set_ylabel("Photo-electrons per pixel\nin one line time (no TDI)")
    ax.grid(axis="x", visible=False)
    note(ax, "Assumes L = 100 W m⁻² sr⁻¹ µm⁻¹, optics × detector efficiency 0.4, dwell = GSD / ground speed.\n"
             "Push-broom imagers make up the shortfall with TDI; frame cameras (Dove, SkySat) stack several frames.",
         xy=(1, -0.2))
    save(fig, "ch14_photons")


def revisit():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    N = np.logspace(0, np.log10(400), 200)
    orbits = 14.6
    for sw, c, lab in [(24, GREEN, "24 km (PlanetScope)"), (185, BLUE, "185 km (Landsat)"),
                       (290, NAVY, "290 km (Sentinel-2)"), (2330, ORANGE, "2 330 km (MODIS)")]:
        ax.plot(N, 40075 / (orbits * sw * N), color=c, lw=1.4, label=f"Swath {lab}")
    pts = [("Landsat 8 + 9\n(actual 8 d)", 2, 40075 / (orbits * 185 * 2)),
           ("Sentinel-2A + 2B\n(actual 5 d)", 2, 40075 / (orbits * 290 * 2)),
           ("Terra MODIS\n(actual 1–2 d)", 1, 40075 / (orbits * 2330)),
           ("≈130 Doves\n(near-daily)", 130, 40075 / (orbits * 24 * 130))]
    for n, x, y in pts:
        ax.plot(x, y, "o", color=RED, ms=4.5, zorder=3)
        ax.annotate(n, (x, y), xytext=(6, -2) if "Dove" not in n else (6, 4), textcoords="offset points", fontsize=6.4)
    ax.axhline(1, color=GREY, lw=0.7, ls=":")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 400)
    ax.set_ylim(0.05, 200)
    ax.set_xlabel("Number of satellites in the constellation")
    ax.set_ylabel("Days for full equatorial coverage")
    ax.legend(fontsize=6.6, loc="upper right")
    note(ax, "Idealised: coverage time ≈ 40 075 km / (orbits per day × swath × N), nadir viewing, no overlap.",
         xy=(1, -0.15))
    save(fig, "ch14_revisit")


def offnadir():
    R, h = 6371.0, 617.0
    th = np.radians(np.linspace(0, 45, 200))
    phi = np.arcsin((R + h) / R * np.sin(th))
    rho = (R + h) * np.cos(th) - np.sqrt(R ** 2 - (R + h) ** 2 * np.sin(th) ** 2)
    along = rho / h
    cross = rho / h / np.cos(phi - th) / np.cos(th) * np.cos(th)  # slant + projection on tilted ground
    cross = rho / h / np.cos(phi)
    gm = np.sqrt(along * cross)
    ground = R * (phi - th)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    d = np.degrees(th)
    ax.plot(d, along * 0.31, color=BLUE, lw=1.4, label="Along-track GSD")
    ax.plot(d, cross * 0.31, color=ORANGE, lw=1.4, label="Cross-track GSD")
    ax.plot(d, gm * 0.31, color=NAVY, lw=2, label="Geometric mean GSD")
    ax.set_xlabel("Off-nadir viewing angle (°)")
    ax.set_ylabel("GSD (m)")
    ax.set_xlim(0, 45)
    ax.set_ylim(0.25, 1.0)
    ax2 = ax.twinx()
    ax2.plot(d, ground, color=GREY, lw=1, ls="--")
    ax2.set_ylabel("Ground distance from nadir (km)", color=GREY)
    ax2.set_ylim(0, 700)
    ax2.grid(False)
    i30 = np.argmin(abs(d - 30))
    ax2.annotate(f"30° → {ground[i30]:.0f} km;\naccess swath ≈ {2*ground[i30]:.0f} km", (30, ground[i30]),
                 xytext=(15.5, 560), fontsize=6.6, color=GREY, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.legend(fontsize=6.8, loc="upper left")
    note(ax, "WorldView-3-like case: 617 km altitude, 0.31 m GSD at nadir, spherical Earth.", xy=(1, -0.2))
    save(fig, "ch14_offnadir")


def modes():
    fig, axs = plt.subplots(1, 4, figsize=(7.0, 2.3))
    for ax in axs:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(Rectangle((0.2, 0.2), 9.6, 13.0, fc="#EEF2E6", ec=GREY, lw=0.6))
        ax.annotate("", (5, 13.7), (5, 12.0), arrowprops=dict(arrowstyle="<-", color=GREY, lw=0.8))
    a = axs[0]
    a.add_patch(Rectangle((3.8, 1), 1.6, 11.5, fc=BLUE, alpha=0.75))
    a.set_title("Long strip", fontsize=8)
    a = axs[1]
    for i, x in enumerate([1.4, 3.0, 4.6, 6.2]):
        a.add_patch(Rectangle((x, 3), 1.7, 7, fc=[BLUE, SKY][i % 2], alpha=0.8, ec="white", lw=0.5))
    a.set_title("Area mosaic", fontsize=8)
    a = axs[2]
    a.add_patch(Rectangle((3.6, 4.5), 2.6, 4.5, fc=ORANGE, alpha=0.6))
    for y0, s in [(0.6, "fore"), (12.6, "aft")]:
        a.annotate("", (4.9, 6.75), (4.9 + (1.6 if s == "fore" else -1.6), y0),
                   arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.9))
    a.text(5.2, 2.0, "look 1", fontsize=6.4)
    a.text(1.0, 11.6, "look 2", fontsize=6.4)
    a.set_title("Same-pass stereo", fontsize=8)
    a = axs[3]
    rng = np.random.default_rng(3)
    for x, y in rng.uniform([1, 1], [9, 12.5], size=(16, 2)):
        a.add_patch(Rectangle((x - 0.35, y - 0.35), 0.7, 0.7, fc=RED, alpha=0.85))
    a.set_title("Many point targets", fontsize=8)
    fig.text(0.5, 0.02, "Arrows show the direction of flight. Agile satellites slew between targets in seconds.",
             ha="center", fontsize=6.6, color=GREY)
    save(fig, "ch14_modes")


def stereo():
    fig, ax = canvas(7.0, 3.2, xlim=(0, 100), ylim=(0, 46))
    ax.plot([5, 95], [6, 6], color="#8B7D5A", lw=2)
    ax.add_patch(Polygon([[38, 6], [50, 20], [62, 6]], closed=True, fc="#C9B98F", ec="#8B7D5A"))
    s1, s2 = (18, 40), (82, 40)
    for s in (s1, s2):
        satellite(ax, s[0], s[1], s=1.0)
        ax.plot([s[0], 50], [s[1] - 1.5, 20], color=ORANGE, lw=1)
        ax.plot([s[0], 50], [s[1] - 1.5, 6], color=BLUE, lw=0.8, ls="--")
    darrow(ax, (21, 44.5), (79, 44.5), color=NAVY, text="base B", fs=7, toff=(0, 0.4))
    darrow(ax, (95, 6), (95, 39), color=NAVY)
    label(ax, 97.5, 22, "height H", rot=90, fs=7)
    label(ax, 50, 23, "peak", fs=6.8)
    label(ax, 50, 2.5, "parallax: the peak appears shifted between the two images", fs=6.8, color=GREY)
    box(ax, 6, 13, 30, 13, "Height precision\nσ_h ≈ σ_p · H / B\nσ_p = matching error on ground\nB/H ≈ 0.3–0.8 typical",
        fs=6.8, fc="white")
    save(fig, "ch14_stereo")


def evolution():
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    pts = [(1972.5, 79, "Landsat 1 MSS"), (1986.1, 10, "SPOT 1"), (1995.9, 5.8, "IRS-1C"), (1999.7, 0.82, "IKONOS"),
           (2001.8, 0.61, "QuickBird"), (2007.7, 0.50, "WorldView-1"), (2008.7, 0.41, "GeoEye-1"),
           (2014.6, 0.31, "WorldView-3"), (2021.3, 0.30, "Pléiades Neo"), (2024.3, 0.34, "WorldView Legion")]
    xs, ys = zip(*[(p[0], p[1]) for p in pts])
    ax.plot(xs, ys, "o-", color=NAVY, ms=5, lw=1.2, zorder=3)
    pos = {"Landsat 1 MSS": (1.0, 1.0, "left", "bottom"), "SPOT 1": (0.6, 1.15, "left", "bottom"),
           "IRS-1C": (0.6, 1.15, "left", "bottom"), "Pléiades Neo": (-0.3, 1.2, "right", "bottom"),
           "WorldView Legion": (0.6, 1.08, "left", "bottom")}
    lead = {"IKONOS": (1984, 0.50), "QuickBird": (1986, 0.30), "WorldView-1": (1989, 0.18), "GeoEye-1": (1993, 0.11),
            "WorldView-3": (2001, 0.068)}
    for x, y, n in pts:
        if n in pos:
            dx, fy, ha, va = pos[n]
            ax.text(x + dx, y * fy, n, fontsize=6.6, ha=ha, va=va)
        else:
            ax.annotate(f"{n} ({int(x)})", (x, y), xytext=lead[n], fontsize=6.6, va="center",
                        arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6, shrinkB=3))
    ax.plot([2025.2], [0.10], "o", mfc="white", mec=RED, ms=6, zorder=3)
    ax.text(2024.6, 0.085, "VLEO 10 cm target\n(Albedo Clarity-1, 2025)", fontsize=6.4, color=RED, ha="right", va="top")
    lim = [(1994, 2000, 1.0), (2000, 2014.45, 0.5), (2014.45, 2026.8, 0.25)]
    for a, b, v in lim:
        ax.plot([a, b], [v, v], color=ORANGE, lw=2.2, alpha=0.8)
    ax.text(1993.7, 1.18, "US licence limit for commercial sale", fontsize=6.4, color=ORANGE, ha="left", va="bottom")
    ax.text(2026.8, 0.22, "0.25 m (2014)", fontsize=6.4, color=ORANGE, ha="right", va="top")
    ax.set_yscale("log")
    ax.set_xlim(1970, 2032)
    ax.set_ylim(0.04, 150)
    ax.set_ylabel("Best GSD (m, panchromatic)")
    ax.set_xlabel("Launch year")
    note(ax, "Civil/commercial systems only. The 2020 NOAA rule replaced fixed limits with a tiered licensing system.",
         xy=(1, -0.15))
    save(fig, "ch14_evolution")


def fleets():
    d = json.load(open(ROOT / "data/eo_fleets.json"))["optical"]
    items = sorted(d.items(), key=lambda kv: -kv[1])
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    hbar(ax, [k for k, _ in items], [v for _, v in items], color=BLUE,
         highlight=["Sentinel-2 (EU)", "Landsat (USA)", "Gaofen (China, govt.)", "Cartosat (India)"], fs=6.8)
    ax.tick_params(axis="y", labelsize=6.8)
    ax.set_xlabel("Active satellites (14 Oct 2026)")
    note(ax, "Orange: government programmes; blue: commercial. Name-matched active payloads in the CelesTrak SATCAT;\n"
             "approximate (excludes military imaging series such as Yaogan).", xy=(1, -0.17))
    save(fig, "ch14_fleets")


def pansharpen():
    from PIL import Image
    im = np.asarray(Image.open(ROOT / "figures/photos/ch13_gardencity.jpg").convert("RGB")).astype(float) / 255
    h, w, _ = im.shape
    c = im[h // 2 - 160:h // 2 + 160, w // 2 - 160:w // 2 + 160]
    pan = c @ np.array([0.30, 0.45, 0.25])
    k = 4
    small = c.reshape(80, k, 80, k, 3).mean(axis=(1, 3))
    ms_nn = np.kron(small, np.ones((k, k, 1)))
    from scipy.ndimage import zoom
    ms_bl = np.clip(zoom(small, (k, k, 1), order=1), 0, 1)
    inten = ms_bl @ np.array([0.30, 0.45, 0.25])
    fused = np.clip(ms_bl * (pan / np.maximum(inten, 1e-3))[..., None], 0, 1)
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.6))
    for a, img, t in zip(axs, [ms_nn, pan, fused], ["Multispectral (4× coarser)", "Panchromatic (full resolution)",
                                                   "Pan-sharpened result"]):
        a.imshow(img, cmap="gray" if img.ndim == 2 else None, interpolation="nearest")
        a.set_title(t, fontsize=7.6)
        a.axis("off")
    fig.text(0.5, 0.02, "Simulated with a Landsat 7 false-colour scene (NASA); ratio (Brovey-type) fusion.",
             ha="center", fontsize=6.4, color=GREY)
    save(fig, "ch14_pansharpen", raster=True)


def fire():
    p = np.logspace(-6, -1, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for lam, c, n in [(3.9, RED, "MWIR 3.9 µm"), (11.0, BLUE, "LWIR 11 µm")]:
        for Tf, ls in [(1000, "-"), (700, "--")]:
            Lp = p * planck(lam, Tf) + (1 - p) * planck(lam, 300)
            ax.plot(p, inv_planck(lam, Lp), color=c, ls=ls, lw=1.5, label=f"{n}, fire {Tf} K")
    ax.set_xscale("log")
    ax.set_xlim(1e-6, 1e-1)
    ax.set_ylim(295, 480)
    ax.axvline(1e-4, color=GREY, lw=0.7, ls=":")
    ax.text(1.1e-4, 452, "100 m² fire in a\n1 km² pixel", fontsize=6.6, color=GREY)
    ax.set_xlabel("Fraction of the pixel on fire")
    ax.set_ylabel("Pixel brightness temperature (K)")
    ax.legend(fontsize=6.6, loc="upper left")
    note(ax, "Background 300 K, emissivity 1, no atmosphere. Computed with Planck's law.", xy=(1, -0.2))
    save(fig, "ch14_fire")


def emissivity():
    l = np.linspace(7.8, 13.2, 500)

    def g(x, c, w):
        return np.exp(-((x - c) / w) ** 2)
    quartz = 0.97 - 0.22 * g(l, 8.4, 0.28) - 0.25 * g(l, 9.1, 0.30) - 0.05 * g(l, 12.6, 0.15)
    calc = 0.97 - 0.10 * g(l, 11.25, 0.15)
    basalt = 0.96 - 0.06 * g(l, 9.6, 0.7)
    veg = 0.975 + 0.005 * np.sin(l)
    water = 0.99 - 0.015 * np.clip(l - 11.5, 0, None)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for y, c, n in [(veg, GREEN, "Green vegetation"), (water, BLUE, "Water"), (basalt, "#555", "Basalt"),
                    (calc, GOLD, "Limestone (calcite)"), (quartz, RED, "Quartz sand")]:
        ax.plot(l, y, color=c, lw=1.6, label=n)
    for lo, hi in [(8.125, 8.475), (8.475, 8.825), (8.925, 9.275), (10.25, 10.95), (10.95, 11.65)]:
        ax.axvspan(lo, hi, color=GOLD, alpha=0.13, lw=0)
    ax.text(9.0, 1.003, "ASTER TIR bands 10–14", fontsize=6.4, color=GREY, ha="center")
    ax.text(9.55, 0.74, "quartz reststrahlen\nfeature", fontsize=6.6, color=RED, ha="left")
    ax.set_xlim(7.8, 13.2)
    ax.set_ylim(0.66, 1.02)
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Emissivity")
    ax.legend(fontsize=6.6, loc="lower right")
    note(ax, "Schematic after the ECOSTRESS (ASTER) spectral library.", xy=(1, -0.2))
    save(fig, "ch14_emissivity")


def hypercube():
    from PIL import Image
    im = np.asarray(Image.open(ROOT / "figures/photos/ch13_sf.jpg").convert("RGB").resize((200, 200)))
    fig = plt.figure(figsize=(7.0, 3.0))
    ax = fig.add_axes([0.0, 0.02, 0.5, 0.96])
    ax.set_xlim(0, 66)
    ax.set_ylim(0, 44)
    ax.set_aspect("equal")
    ax.axis("off")
    cmap = plt.get_cmap("Spectral_r")
    nb, dx, dy = 22, 0.7, 0.6
    for i in range(nb, 0, -1):
        col = cmap(i / nb)
        ax.add_patch(Polygon([[6 + i * dx, 6 + i * dy], [36 + i * dx, 6 + i * dy], [36 + i * dx + 0.01, 36 + i * dy],
                              [6 + i * dx, 36 + i * dy]], closed=True, fc=col, ec="white", lw=0.3))
    ax.imshow(im, extent=(6, 36, 6, 36), zorder=5)
    ax.annotate("", (36 + nb * dx + 1, 36 + nb * dy + 1), (37, 37), arrowprops=dict(arrowstyle="->", color=NAVY))
    ax.text(53, 40, "λ: 100–400\nbands", fontsize=7, ha="left", va="center", color=NAVY)
    ax.text(21, 3, "x (cross-track)", fontsize=7, ha="center")
    ax.text(2.5, 21, "y (along-track)", fontsize=7, rotation=90, va="center")
    ax.plot([22], [24], "o", ms=5, mfc="none", mec="yellow", mew=1.5, zorder=6)
    ax.plot([13], [14], "s", ms=5, mfc="none", mec="cyan", mew=1.5, zorder=6)
    ax2 = fig.add_axes([0.58, 0.2, 0.39, 0.72])
    l = np.linspace(0.4, 2.5, 300)

    def g(x, c, w):
        return np.exp(-((x - c) / w) ** 2)
    edge = 1 / (1 + np.exp(-(l - 0.715) / 0.012))
    veg = (0.05 + 0.04 * g(l, 0.55, 0.04)) * (1 - edge) + (0.45 - 0.2 * np.clip((l - 1.2) / 1.2, 0, 1)) * edge
    veg *= (1 - 0.5 * g(l, 1.45, 0.05)) * (1 - 0.7 * g(l, 1.94, 0.07))
    mineral = 0.18 + 0.1 * (l - 0.4) - 0.08 * g(l, 2.2, 0.03) - 0.05 * g(l, 0.9, 0.12)
    mineral *= (1 - 0.5 * g(l, 1.45, 0.05)) * (1 - 0.7 * g(l, 1.94, 0.07))
    ax2.plot(l, veg, color=GREEN, lw=1.4, label="pixel ○ vegetation")
    ax2.plot(l, mineral, color="#8C564B", lw=1.4, label="pixel □ clay-rich soil")
    ax2.annotate("Al-OH absorption\n2.20 µm", (2.2, mineral[np.argmin(abs(l - 2.2))]), xytext=(1.5, 0.05),
                 fontsize=6.4, arrowprops=dict(arrowstyle="->", lw=0.7, color=GREY))
    ax2.set_xlabel("Wavelength (µm)", fontsize=7)
    ax2.set_ylabel("Reflectance", fontsize=7)
    ax2.tick_params(labelsize=6.5)
    ax2.legend(fontsize=6.4, loc="upper right")
    ax2.set_ylim(0, 0.6)
    save(fig, "ch14_hypercube", raster=True)


if __name__ == "__main__":
    fns = [landsat_timeline, bands, optics, photons, revisit, offnadir, modes, stereo, evolution, fleets, pansharpen,
           fire, emissivity, hypercube]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
