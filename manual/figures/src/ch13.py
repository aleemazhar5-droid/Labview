import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403


def g(x, c, w):
    return np.exp(-((x - c) / w) ** 2)


def signatures():
    l = np.linspace(0.4, 2.5, 600)
    vis = 0.04 + 0.07 * g(l, 0.55, 0.035) - 0.015 * g(l, 0.67, 0.02)
    edge = 1 / (1 + np.exp(-(l - 0.715) / 0.012))
    nir = 0.48 - 0.12 * np.clip((l - 1.15) / 0.5, 0, 1) - 0.18 * np.clip((l - 1.7) / 0.6, 0, 1)
    veg = vis * (1 - edge) + nir * edge
    veg = veg * (1 - 0.55 * g(l, 1.45, 0.05)) * (1 - 0.75 * g(l, 1.94, 0.07)) * (1 - 0.12 * g(l, 1.2, 0.04))
    soil = 0.08 + 0.12 * (l - 0.4) - 0.04 * g(l, 1.4, 0.05) - 0.06 * g(l, 1.9, 0.06) - 0.03 * (l > 2.2) * (l - 2.2)
    water = 0.06 * g(l, 0.48, 0.12) + 0.02 * np.exp(-(l - 0.4) / 0.25)
    snow = (0.96 - 0.05 * (l - 0.4)) * np.exp(-np.clip(l - 0.9, 0, None) * 0.8)
    snow = snow * (1 - 0.25 * g(l, 1.03, 0.05)) * (1 - 0.9 * g(l, 1.5, 0.11)) * (1 - 0.92 * g(l, 2.0, 0.13))
    urban = 0.15 + 0.05 * (l - 0.4) - 0.02 * g(l, 1.9, 0.1)
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    for y, c, n in [(veg, GREEN, "Green vegetation"), (soil, "#8C564B", "Dry bare soil"), (water, BLUE, "Clear water"),
                    (snow, SKY, "Fresh snow"), (urban, GREY, "Concrete / urban")]:
        ax.plot(l, np.clip(y, 0, 1), color=c, lw=1.8, label=n)
    for a, b, t in [(0.45, 0.52, "B"), (0.53, 0.59, "G"), (0.64, 0.67, "R"), (0.85, 0.88, "NIR"), (1.57, 1.65, "SWIR1"),
                    (2.11, 2.29, "SWIR2")]:
        ax.axvspan(a, b, color=GOLD, alpha=0.18)
        ax.text((a + b) / 2, 0.97, t, ha="center", fontsize=6.6)
    ax.text(0.72, 0.6, "red edge", fontsize=6.8, color=GREEN)
    ax.text(1.36, 0.02, "water absorption", fontsize=6.4, color=GREY)
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Reflectance")
    ax.set_ylim(0, 1.02)
    ax.set_xlim(0.4, 2.5)
    ax.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1, 0.9))
    note(ax, "Schematic spectra after USGS/ECOSTRESS spectral libraries; shaded: Landsat 8/9 OLI bands.", xy=(1, -0.16))
    save(fig, "ch13_signatures")


def blackbodies():
    lam = np.logspace(-1, 2, 600) * 1e-6
    h, c, k = 6.62607e-34, 2.998e8, 1.380649e-23
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    for T, col, n in [(5772, ORANGE, "Sun (5 772 K)"), (1200, RED, "Wildfire flames (≈ 1 200 K)"),
                      (300, GREEN, "Earth's surface (300 K)"), (220, BLUE, "Cloud tops (220 K)")]:
        B = 2 * h * c ** 2 / lam ** 5 / (np.exp(h * c / (lam * k * T)) - 1)
        ax.loglog(lam * 1e6, B / B.max(), color=col, label=n)
        lm = 2898 / T
        ax.plot(lm, 1, "o", color=col, ms=4)
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Normalised spectral radiance")
    ax.set_ylim(1e-4, 2)
    ax.set_xlim(0.1, 100)
    ax.legend(fontsize=7, loc="lower left")
    note(ax, "Planck curves, each normalised to its peak. Wien's law: λ_max = 2 898 µm·K / T — sunlight peaks at 0.5 µm, "
             "Earth's emission at ≈ 10 µm, fires at ≈ 2.4 µm.", xy=(1, -0.16))
    save(fig, "ch13_blackbodies")


def chain():
    fig, ax = canvas(7.2, 3.4, (0, 100), (0, 46))
    ax.add_patch(Circle((8, 39), 4, fc=GOLD, ec=ORANGE))
    ax.text(8, 32, "Sun (source)", fontsize=6.8, ha="center")
    satellite(ax, 70, 40, 1.2)
    ax.text(70, 34.5, "sensor", fontsize=6.8, ha="center")
    ax.add_patch(Rectangle((0, 18), 100, 8, fc="#EAF4FB", ec="none"))
    ax.text(97, 22, "atmosphere:\nscattering,\nabsorption,\nemission", fontsize=6.2, ha="right", va="center", color=BLUE)
    ax.add_patch(Rectangle((0, 8), 100, 4, fc="#D9EAD3", ec="none"))
    ax.text(50, 6, "surface: reflection (BRDF), absorption, emission, backscatter", fontsize=6.6, ha="center")
    arrow(ax, (11, 36), (34, 12.5), color=ORANGE, lw=1.4)
    arrow(ax, (36, 12.5), (66, 37), color=ORANGE, lw=1.4)
    ax.text(18, 27, "① illumination", fontsize=6.6, color=ORANGE)
    ax.text(47, 30, "② reflected / emitted\nradiance", fontsize=6.6, color=ORANGE)
    arrow(ax, (20, 22), (66, 36), color=SKY, lw=0.8, ls="--")
    ax.text(28, 25.5, "path radiance (haze)", fontsize=6.2, color=SKY)
    arrow(ax, (54, 10), (68, 36), color=RED, lw=1.0, ls=":")
    ax.text(58, 14.5, "thermal\nemission", fontsize=6.2, color=RED)
    box(ax, 76, 26, 22, 7, "③ downlink → L0–L4\nprocessing", fc="#E8F1FA", ec=BLUE, fs=6.4)
    box(ax, 76, 36.5, 22, 7, "④ analysis, AI,\nusers & decisions", fc="#F3EFF9", ec=VIOLET, fs=6.4)
    arrow(ax, (72, 38), (76, 31), color=BLUE)
    arrow(ax, (87, 33), (87, 36.5), color=VIOLET)
    save(fig, "ch13_chain")


def tradespace():
    s = [("WorldView Legion", 0.29, 9, BLUE), ("Pléiades Neo", 0.3, 14, BLUE), ("SkySat", 0.5, 6, BLUE),
         ("Pelican (Planet)", 0.4, 10, BLUE), ("SPOT 6/7", 1.5, 60, VIOLET), ("PlanetScope (SuperDove)", 3.0, 32, VIOLET),
         ("Sentinel-2 MSI", 10, 290, GREEN), ("Landsat 8/9 OLI", 30, 185, GREEN), ("Sentinel-1 (IW)", 5, 250, ORANGE),
         ("ICEYE spotlight", 0.25, 5, ORANGE), ("NISAR (L-band)", 7, 240, ORANGE), ("MODIS", 250, 2330, RED),
         ("VIIRS", 375, 3040, RED), ("Sentinel-3 OLCI", 300, 1270, RED), ("GOES-R ABI (full disk)", 500, 12000, GOLD),
         ("EMIT (hyperspectral)", 60, 75, "#8C564B"), ("EnMAP", 30, 30, "#8C564B")]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    off = {"Pléiades Neo": (1.15, 1.25, "left"), "Pelican (Planet)": (1.15, 1.0, "left"), "WorldView Legion": (0.85, 0.85, "right"),
           "SkySat": (1.15, 0.85, "left"), "ICEYE spotlight": (0.85, 0.8, "right"), "Sentinel-1 (IW)": (0.85, 1.0, "right"),
           "Sentinel-2 MSI": (1.15, 1.25, "left"), "NISAR (L-band)": (1.15, 0.72, "left"), "MODIS": (0.85, 1.0, "right")}
    for n, gsd, sw, c in s:
        ax.scatter(gsd, sw, s=50, color=c, zorder=3, edgecolor="white")
        fx, fy, ha = off.get(n, (1.15, 1.07, "left"))
        ax.text(gsd * fx, sw * fy, n, fontsize=6.5, ha=ha)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Best ground sampling distance (m)")
    ax.set_ylabel("Swath width (km)")
    ax.set_xlim(0.15, 3000)
    ax.set_ylim(3, 30000)
    x = np.logspace(-1, 3.5, 50)
    ax.plot(x, x * 30, color=GREY, ls=":", lw=0.8)
    ax.text(60, 4000, "swath ≈ 30 000 pixels × GSD", fontsize=6.6, color=GREY, rotation=31)
    for c, t in [(BLUE, "very-high-res optical"), (VIOLET, "high-res optical"), (GREEN, "medium-res optical"),
                 (ORANGE, "SAR"), (RED, "low-res / global"), (GOLD, "geostationary"), ("#8C564B", "hyperspectral")]:
        ax.scatter([], [], color=c, label=t)
    ax.legend(fontsize=6.6, loc="upper left")
    save(fig, "ch13_tradespace")


def four_res():
    fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.2))
    rng = np.random.default_rng(3)
    img = rng.random((40, 40))
    from scipy.ndimage import gaussian_filter
    img = gaussian_filter(img, 3)
    axs[0].imshow(img, cmap="Greens")
    axs[0].imshow(img[::8, ::8].repeat(8, 0).repeat(8, 1), cmap="Greens", alpha=0.0)
    axs[0].set_title("Spatial: pixel size\n(GSD)", fontsize=7)
    sm = img[::8, ::8].repeat(8, 0).repeat(8, 1)
    axs[0].imshow(np.hstack([img[:, :20], sm[:, 20:]]), cmap="Greens")
    axs[0].axvline(19.5, color="white", lw=1)
    lam = np.linspace(0.4, 2.5, 300)
    axs[1].plot(lam, 0.3 + 0.2 * np.sin(lam * 5), color=GREY, lw=0.8)
    for a, b in [(0.45, 0.52), (0.53, 0.6), (0.63, 0.69), (0.76, 0.9), (1.55, 1.75), (2.08, 2.35)]:
        axs[1].axvspan(a, b, color=ORANGE, alpha=0.4)
    axs[1].set_title("Spectral: number & width\nof bands", fontsize=7)
    axs[1].set_yticks([])
    axs[1].tick_params(labelsize=6)
    x = np.linspace(0, 1, 300)
    axs[2].step(x, np.round(x * 4) / 4, color=RED, label="2-bit")
    axs[2].step(x, np.round(x * 64) / 64, color=BLUE, lw=0.8, label="6-bit")
    axs[2].set_title("Radiometric: bits &\nsensitivity", fontsize=7)
    axs[2].legend(fontsize=5.6)
    axs[2].tick_params(labelsize=6)
    days = [0, 5, 10, 15, 20, 25]
    axs[3].bar(days, [1] * len(days), width=1.2, color=GREEN)
    axs[3].bar([0, 16], [0.6, 0.6], width=1.2, color=GREY)
    axs[3].set_title("Temporal: revisit\n(green 5 d vs grey 16 d)", fontsize=7)
    axs[3].set_yticks([])
    axs[3].tick_params(labelsize=6)
    for a in axs[:1]:
        a.set_xticks([])
        a.set_yticks([])
    save(fig, "ch13_four_res")


def scattering():
    lam = np.linspace(0.35, 2.5, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ray = 0.0088 * lam ** -4.05
    ax.semilogy(lam, ray, color=BLUE, lw=2, label="Rayleigh (molecules): optical depth ∝ λ⁻⁴")
    for a, c, n in [(1.3, ORANGE, "Aerosol, Ångström α = 1.3 (fine smoke)"), (0.3, RED, "Aerosol, α = 0.3 (coarse dust)")]:
        ax.semilogy(lam, 0.2 * (lam / 0.55) ** -a, color=c, lw=1.6, label=n)
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Vertical optical depth")
    ax.legend(fontsize=7)
    ax.text(0.37, 0.004, "blue sky: short waves scatter most", fontsize=6.8, color=BLUE)
    note(ax, "Rayleigh optical depth from standard formulas; aerosol curves illustrative (AOD 0.2 at 550 nm).",
         xy=(1, -0.18))
    save(fig, "ch13_scattering")


def ndvi_bars():
    surf = ["Dense forest", "Crop (healthy)", "Crop (stressed)", "Bare soil", "Water", "Cloud / snow"]
    red = np.array([0.03, 0.05, 0.10, 0.22, 0.04, 0.80])
    nir = np.array([0.45, 0.40, 0.28, 0.28, 0.02, 0.78])
    ndvi = (nir - red) / (nir + red)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1.3, 1], wspace=0.55))
    x = np.arange(len(surf))
    a1.bar(x - 0.18, red, 0.36, color=RED, label="Red reflectance")
    a1.bar(x + 0.18, nir, 0.36, color="#8C2D04", label="NIR reflectance")
    a1.set_xticks(x)
    a1.set_xticklabels(surf, rotation=30, ha="right", fontsize=6.8)
    a1.legend(fontsize=6.8)
    a1.set_ylabel("Reflectance")
    a2.barh(x, ndvi, color=[GREEN if v > 0.4 else GOLD if v > 0.15 else GREY for v in ndvi])
    a2.set_yticks(x)
    a2.set_yticklabels(surf, fontsize=6.8)
    a2.invert_yaxis()
    a2.axvline(0, color=INK, lw=0.6)
    a2.set_xlabel("NDVI = (NIR − Red)/(NIR + Red)")
    for k, v in enumerate(ndvi):
        a2.text(v + (0.02 if v >= 0 else -0.02), k, f"{v:.2f}", va="center", fontsize=6.8, ha="left" if v >= 0 else "right")
    a2.set_xlim(-0.6, 1.0)
    save(fig, "ch13_ndvi")


def levels():
    fig, ax = canvas(7.2, 3.0, (0, 100), (0, 38))
    lv = [("Level 0", "raw instrument data,\ntime-ordered,\ncommunications\nartefacts removed", GREY),
          ("Level 1A/B", "calibrated radiance,\nsensor geometry,\nlocation tags", BLUE),
          ("Level 1C / 1T", "orthorectified,\nmap-projected\ntop-of-atmosphere\nreflectance", SKY),
          ("Level 2", "geophysical variables:\nsurface reflectance,\nSST, soil moisture,\ncloud mask", GREEN),
          ("Level 3", "gridded, composited\nin space and time\n(e.g., monthly NDVI)", ORANGE),
          ("Level 4", "model output or\nanalysis combining\nmany sources\n(e.g., reanalysis)", VIOLET)]
    for k, (t, b, c) in enumerate(lv):
        title_box(ax, 0.5 + k * 16.6, 5, 15.6, 28, t, b, hc=c, ec=c, fc="white", fs=5.7, tfs=6.8)
        if k < 5:
            arrow(ax, (16.1 + k * 16.6, 19), (17.1 + k * 16.6, 19), color=GREY, ms=5)
    ax.text(50, 1, "CEOS Analysis Ready Data (CARD4L) defines Level-2-type products that users can analyse directly.",
            fontsize=6.4, ha="center", color=GREY)
    save(fig, "ch13_levels")


def mtf():
    f = np.linspace(0, 1.2, 300)
    diff = np.where(f < 1.0, 2 / np.pi * (np.arccos(np.clip(f, 0, 1)) - f * np.sqrt(np.clip(1 - f ** 2, 0, 1))), 0)
    det = np.abs(np.sinc(f * 0.85))
    jit = np.exp(-(f * 1.2) ** 2 * 0.6)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(f, diff, color=BLUE, label="Optics (diffraction-limited)")
    ax.plot(f, det, color=ORANGE, label="Detector pixel aperture")
    ax.plot(f, jit, color=GREEN, label="Motion / jitter")
    ax.plot(f, diff * det * jit, color=NAVY, lw=2.2, label="System MTF (product)")
    ax.axvline(0.5 / 0.85, color=GREY, ls=":", lw=0.8)
    ax.text(0.6, 0.85, "detector Nyquist", fontsize=6.8, color=GREY)
    ax.set_xlabel("Spatial frequency (normalised to optical cut-off)")
    ax.set_ylabel("MTF (contrast transfer)")
    ax.legend(fontsize=7)
    ax.set_ylim(0, 1.05)
    save(fig, "ch13_mtf")


def relief():
    fig, ax = canvas(6.8, 3.2, (0, 100), (0, 42))
    satellite(ax, 30, 39, 1.0)
    ax.plot([0, 100], [6, 6], color="#8C564B", lw=2)
    ax.add_patch(Polygon([(55, 6), (62, 22), (69, 6)], fc="#C9B79C", ec="#8C564B"))
    ax.plot([30, 62], [38, 22], color=ORANGE, lw=1)
    ax.plot([62, 72.5], [22, 6], color=ORANGE, lw=1, ls="--")
    ax.plot([62, 62], [22, 6], color=GREY, lw=0.8, ls=":")
    ax.plot(62, 6, "o", color=GREEN, ms=5)
    ax.plot(72.5, 6, "o", color=RED, ms=5)
    ax.text(62, 2.5, "true position", fontsize=6.6, ha="center", color=GREEN)
    ax.text(76, 2.5, "apparent position", fontsize=6.6, ha="center", color=RED)
    ax.text(44, 28, "line of sight", fontsize=6.6, color=ORANGE, rotation=-27)
    ax.text(98, 39, "Relief displacement: d = h · tan(θ_view).\nOrthorectification uses a digital elevation\n"
            "model to move each pixel to its true\nground position.", fontsize=6.8, ha="right", va="top")
    save(fig, "ch13_relief")


if __name__ == "__main__":
    signatures(); blackbodies(); chain(); tradespace(); four_res(); scattering(); ndvi_bars(); levels(); mtf(); relief()
