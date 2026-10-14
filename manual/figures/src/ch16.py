import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Wedge

ROOT = Path(__file__).resolve().parents[2]
CLIM = json.load(open(ROOT / "data/climate_series.json"))


def geo_ring():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.0, 3.7))
    ax = world_axes(fig, proj=ccrs.PlateCarree(central_longitude=0))
    sats = [("GOES-18\n(GOES-West)", -137.0, BLUE), ("GOES-19\n(GOES-East)", -75.2, BLUE),
            ("Meteosat-12\n(MTG-I1)", 0.0, GREEN), ("Meteosat-9\n(IODC)", 45.5, GREEN),
            ("INSAT-3DS", 82.0, ORANGE), ("FY-4B", 105.0, RED), ("GK-2A", 128.2, VIOLET),
            ("Himawari-9", 140.7, NAVY), ("Elektro-L", 76.0, GREY)]
    lat = np.linspace(-89, 89, 179)
    lon = np.linspace(-180, 180, 361)
    LON, LAT = np.meshgrid(lon, lat)
    cnt = np.zeros_like(LON)
    for n, l0, c in sats:
        cosg = np.cos(np.radians(LAT)) * np.cos(np.radians(LON - l0))
        cnt += np.degrees(np.arccos(np.clip(cosg, -1, 1))) < 70
    from matplotlib.colors import ListedColormap, BoundaryNorm
    cmap = ListedColormap(["#FFFFFF00", "#CFE3F3", "#9CC5E6", "#5FA8D3", "#2F7DB8"])
    ax.pcolormesh(LON, LAT, np.minimum(cnt, 4), cmap=cmap, norm=BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], 5),
                  alpha=0.4, transform=ccrs.PlateCarree(), zorder=0.8, shading="auto")
    lab = {"GOES-18\n(GOES-West)": (-137, -22), "GOES-19\n(GOES-East)": (-75, -22), "Meteosat-12\n(MTG-I1)": (0, -22),
           "Meteosat-9\n(IODC)": (40, 22), "Elektro-L": (68, 40), "INSAT-3DS": (88, -22), "FY-4B": (100, 30),
           "GK-2A": (125, -40), "Himawari-9": (152, 22)}
    for n, l0, c in sats:
        ax.plot(l0, 0, "o", color=c, ms=5, mec="white", mew=0.6, transform=ccrs.PlateCarree(), zorder=5)
        x, y = lab[n]
        ax.plot([l0, x], [0, y * 0.8], color=c, lw=0.6, transform=ccrs.PlateCarree(), zorder=4)
        ax.text(x, y, n, fontsize=6.0, color=c, ha="center", va="top" if y < 0 else "bottom",
                transform=ccrs.PlateCarree(), zorder=6, bbox=dict(fc="white", ec="none", alpha=0.8, pad=0.6))
    note(ax, "Approximate 2026 positions of primary meteorological geostationary satellites. Shading: number of satellites "
             "viewing each point\nwithin 70° Earth-central angle (the practical limit for quantitative imagery).", xy=(1, -0.02))
    save(fig, "ch16_georing")


def orbits_lt():
    fig, ax = canvas(6.4, 4.1, xlim=(-60, 60), ylim=(-42, 36))
    ax.add_patch(Circle((0, 0), 6, fc=EARTH, ec="none", zorder=3))
    ax.add_patch(Wedge((0, 0), 6, 90, 270, fc=SPACE, alpha=0.55, ec="none", zorder=4))
    arrow(ax, (58, 0), (40, 0), color=ORANGE, lw=2)
    label(ax, 50, 3, "sunlight", fs=6.8, color=ORANGE)
    label(ax, -20, -14, "Earth seen from above\nthe North Pole", fs=6.2, color=GREY, bg="white")
    planes = [(5.5, RED, "Early morning: FY-3E (05:30)"), (9.5, GREEN, "Mid-morning: Metop, Metop-SG (09:30)"),
              (13.5, BLUE, "Afternoon: NOAA-20, NOAA-21 (13:30)")]
    for h, c, n in planes:
        ang = np.radians((h - 12) * 15)
        dx, dy = np.cos(ang), np.sin(ang)
        ax.plot([-30 * dx, 30 * dx], [-30 * dy, 30 * dy], color=c, lw=2.2, zorder=2)
        ax.plot([30 * dx], [30 * dy], "o", color=c, ms=5, zorder=5)
        if abs(dx) < 0.3:
            ax.text(31.5 * dx + 2, 31.5 * dy, n, fontsize=6.6, color=c, ha="left", va="center")
        else:
            ha = "left" if dx > 0 else "right"
            ax.text(31.5 * dx + (1.5 if dx > 0 else -1.5), 31.5 * dy, n, fontsize=6.6, color=c, ha=ha, va="center")
    label(ax, 0, 33, "Orbit planes (edge-on) of the three polar orbits of the WMO baseline", fs=7, weight="bold")
    label(ax, 0, -40, "The plane stays fixed relative to the Sun, so each satellite crosses the equator at the same "
          "local times every day", fs=6.4, color=GREY)
    save(fig, "ch16_orbitslt")


def abi_scan():
    fig, ax = plt.subplots(figsize=(7.0, 2.3))
    rows = [("Full disk", [(0, 10)], NAVY), ("CONUS / PACUS", [(0, 5), (5, 10)], BLUE),
            ("Mesoscale 1", [(i, i + 1) for i in range(10)], ORANGE), ("Mesoscale 2", [(i, i + 1) for i in range(10)], GOLD)]
    for j, (n, segs, c) in enumerate(rows):
        for a, b in segs:
            ax.add_patch(Rectangle((a + 0.03, j - 0.32), b - a - 0.06, 0.64, fc=c, alpha=0.8))
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=7)
    ax.set_xlim(0, 10)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_xlabel("Minutes (ABI Mode 6)")
    ax.grid(axis="y", visible=False)
    ax.text(10, 3.75, "two mesoscale boxes can be co-located for 30-second imaging", fontsize=6.4, color=GREY,
            ha="right")
    note(ax, "The scans are interleaved; each bar shows how often a complete image of that domain is produced.",
         xy=(1, -0.42))
    save(fig, "ch16_abiscan")


def weighting():
    z = np.linspace(0, 60, 600)
    H = 7.5
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    cols = [RED, ORANGE, GOLD, GREEN, BLUE, VIOLET]
    for k, c in zip([1.5, 4, 12, 40, 150, 600], cols):
        u = np.exp(-z / H)
        W = k / H * u * np.exp(-k * u)
        ax.plot(W / W.max(), z, color=c, lw=1.6, label=f"peak ≈ {H*np.log(k):.0f} km")
    ax.set_xlabel("Weighting function (normalised)")
    ax.set_ylabel("Altitude (km)")
    ax.set_ylim(0, 60)
    ax.set_xlim(0, 1.05)
    ax.legend(fontsize=6.6, loc="upper right", title="Channel", title_fontsize=6.8)
    ax.text(0.03, 1.5, "surface-sensitive window channel", fontsize=6.4, color=RED)
    note(ax, "Idealised channels with increasing absorption (e.g. towards the centre of the 50–60 GHz O₂ band\n"
             "or the 15 µm CO₂ band); exponential atmosphere, scale height 7.5 km.", xy=(1, -0.15))
    save(fig, "ch16_weighting")


def mw_spectrum():
    f = np.linspace(1, 200, 4000)

    def lor(f0, w, s):
        return s * w ** 2 / ((f - f0) ** 2 + w ** 2)
    tau = 0.006 + 3e-5 * f ** 2 + lor(22.235, 3.5, 0.18) + lor(183.31, 3.5, 30) + lor(118.75, 1.0, 40)
    o2 = np.exp(-((f - 60) / 4.5) ** 2) * 160 + lor(60, 4, 3)
    tau = tau + o2
    T = np.exp(-tau)
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.plot(f, T, color=NAVY, lw=1.2)
    ax.fill_between(f, T, 0, color=SKY, alpha=0.25)
    for f0, t in [(22.235, "H₂O\n22 GHz"), (60, "O₂\n50–70 GHz\n(temperature)"), (118.75, "O₂\n118 GHz"),
                  (183.31, "H₂O 183 GHz\n(humidity)")]:
        ax.text(f0, 1.03, t, fontsize=6.4, ha="center", va="bottom")
    for a, b, t in [(1.4, 1.43, "SMOS/SMAP\n1.4 GHz"), (10.6, 10.7, ""), (36.5, 37, "window\nchannels"), (89, 90, ""),
                    (150, 166, "")]:
        ax.axvspan(a, b, color=GOLD, alpha=0.4)
    ax.text(36.8, 0.12, "window\nchannels", fontsize=6.3, ha="center", color="#7A5C00")
    ax.text(4, 0.12, "L-band\nsoil moisture", fontsize=6.3, ha="left", color="#7A5C00")
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 1.32)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Zenith transmittance")
    note(ax, "Schematic for a mid-latitude atmosphere; gold bands: typical window channels used for surface and "
             "precipitation sensing.", xy=(1, -0.17))
    save(fig, "ch16_mwspectrum")


def nwp_flow():
    fig, ax = canvas(7.0, 3.0, xlim=(0, 100), ylim=(0, 42))
    box(ax, 1, 24, 20, 16, "Observations\nsatellites (> 90 % of\nassimilated data),\nradiosondes, aircraft,\nsurface, radar",
        fs=6.6, fc=LIGHT)
    box(ax, 26, 24, 18, 16, "Quality control,\nbias correction,\nthinning", fs=6.8, fc=LIGHT)
    box(ax, 49, 24, 22, 16, "Data assimilation\n(4D-Var / ensemble)\nbest estimate of the\nstate: the analysis",
        fs=6.8, fc="#FFF4E5", ec=ORANGE)
    box(ax, 76, 24, 22, 16, "Forecast model\nphysics- or AI-based\nensembles of 50+\nmembers", fs=6.8, fc=LIGHT)
    for a, b in [((21, 32), (26, 32)), ((44, 32), (49, 32)), ((71, 32), (76, 32))]:
        arrow(ax, a, b)
    arrow(ax, (82, 24), (60, 24), color=GREY, rad=-0.6)
    label(ax, 58, 15.5, "short forecast = first guess\nfor the next cycle", fs=6.4, color=GREY, ha="right")
    box(ax, 76, 2, 22, 10, "Products: forecasts,\nwarnings, reanalyses", fs=6.8, fc="#E8F5E9", ec=GREEN)
    arrow(ax, (87, 24), (87, 12), color=GREEN)
    label(ax, 25, 6, "Cycle repeated every 6–12 hours (hourly for regional models)", fs=6.6, color=GREY)
    save(fig, "ch16_nwpflow")


def skill():
    yr = np.arange(1981, 2025)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))

    def curve(a, b, k, x0):
        return a + (b - a) / (1 + np.exp(-(yr - x0) / k))
    for d, (nh, sh), c in [(3, ((0.86, 0.985), (0.70, 0.98)), NAVY), (5, ((0.66, 0.92), (0.45, 0.91)), BLUE),
                           (7, ((0.42, 0.80), (0.25, 0.79)), GREEN), (10, ((0.18, 0.55), (0.10, 0.53)), ORANGE)]:
        ax.plot(yr, curve(nh[0], nh[1], 7, 1996), color=c, lw=1.8, label=f"Day {d}")
        ax.plot(yr, curve(sh[0], sh[1], 5.5, 1999), color=c, lw=1.1, ls="--")
    ax.set_ylim(0.0, 1.0)
    ax.set_xlim(1981, 2024)
    ax.set_xlabel("Year")
    ax.set_ylabel("Forecast skill (anomaly correlation)")
    ax.legend(fontsize=6.6, loc="lower right", ncol=2)
    ax.text(1982, 0.04, "solid: Northern Hemisphere   dashed: Southern Hemisphere", fontsize=6.5, color=GREY)
    ax.annotate("hemispheres converge as satellite\nradiances are assimilated directly", (2002, 0.86),
                xytext=(1984, 0.58), fontsize=6.5, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    note(ax, "Schematic redrawn after published ECMWF 500 hPa height anomaly-correlation records (Bauer et al., 2015).",
         xy=(1, -0.2))
    save(fig, "ch16_skill")


def sea_ice():
    a = np.array(CLIM["arctic_sep_extent_mkm2"])
    s = np.array(CLIM["antarctic_feb_extent_mkm2"])
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.plot(a[:, 0], a[:, 1], "o-", color=BLUE, ms=3, lw=1.2, label="Arctic, September minimum")
    ax.plot(s[:, 0], s[:, 1], "s-", color=ORANGE, ms=3, lw=1.2, label="Antarctic, February minimum")
    m, b = np.polyfit(a[:, 0], a[:, 1], 1)
    ax.plot(a[:, 0], m * a[:, 0] + b, color=BLUE, lw=0.8, ls="--")
    base = a[(a[:, 0] >= 1981) & (a[:, 0] <= 2010), 1].mean()
    pct = m * 10 / base * 100
    ax.text(1980, 3.2, f"Arctic trend {m*10:+.2f} million km² per decade\n(≈ {pct:.0f} % per decade relative to 1981–2010)",
            fontsize=6.6, color=BLUE)
    i12 = np.argmin(a[:, 1])
    ax.annotate(f"record low {int(a[i12,0])}: {a[i12,1]:.2f}", (a[i12, 0], a[i12, 1]), xytext=(1996, 2.1),
                fontsize=6.6, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea-ice extent (million km²)")
    ax.set_ylim(1.5, 8.2)
    ax.legend(fontsize=6.7, loc="upper right")
    note(ax, "Data: NSIDC Sea Ice Index (passive microwave, SMMR, SSM/I, SSMIS, AMSR2).", xy=(1, -0.2))
    save(fig, "ch16_seaice")


def sea_level():
    d = CLIM["gmsl_noaa_mm"]
    arr = np.array(d["data"])
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    cols = [GREY, SKY, BLUE, NAVY, ORANGE]
    for i, (n, c) in enumerate(zip(d["missions"], cols)):
        sel = arr[arr[:, 1] == i]
        ax.plot(sel[:, 0], sel[:, 2], ".", color=c, ms=2.5, label=n)
    t, y = arr[:, 0], arr[:, 2]
    p = np.polyfit(t - 1993, y, 2)
    tt = np.linspace(t.min(), t.max(), 200)
    ax.plot(tt, np.polyval(p, tt - 1993), color=RED, lw=1.6)
    r93 = p[1] + 2 * p[0] * (1993 - 1993)
    r24 = p[1] + 2 * p[0] * (2024 - 1993)
    lin = np.polyfit(t, y, 1)[0]
    ax.text(1993.5, 72, f"mean rate {lin:.1f} mm/yr\nquadratic fit: {r93:.1f} mm/yr (1993) → {r24:.1f} mm/yr (2024)",
            fontsize=6.6, color=RED)
    ax.set_xlabel("Year")
    ax.set_ylabel("Global mean sea level (mm)")
    ax.legend(fontsize=6.3, loc="lower right", markerscale=3)
    note(ax, "Altimetry data are provided by NOAA Laboratory for Satellite Altimetry (seasonal signals removed, "
             "no GIA correction).", xy=(1, -0.2))
    save(fig, "ch16_sealevel")


def ozone():
    oz = np.array(CLIM["ozone_hole"])
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.bar(oz[:, 0], oz[:, 1], color=VIOLET, alpha=0.8, width=0.8, label="Ozone-hole area (Sep–Oct mean)")
    ax.set_ylabel("Area (million km²)")
    ax.set_xlabel("Year")
    ax2 = ax.twinx()
    ax2.plot(oz[:, 0], oz[:, 2], "o-", color=ORANGE, ms=3, lw=1.1, label="Minimum ozone")
    ax2.set_ylabel("Minimum total ozone (DU)", color=ORANGE)
    ax2.set_ylim(80, 240)
    ax2.grid(False)
    ax.axvline(1987.7, color=GREEN, lw=1, ls="--")
    ax.text(1988.2, 28.5, "Montreal Protocol (1987)", fontsize=6.5, color=GREEN, va="top")
    ax.set_ylim(0, 30)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=6.6, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)
    note(ax, "Data: NASA Ozone Watch (TOMS, OMI, OMPS; gaps filled with MERRA-2). No satellite data in 1995.",
         xy=(1, -0.2))
    save(fig, "ch16_ozone")


def aq_geo():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.0, 3.0))
    ax = world_axes(fig, extent=(-170, 170, -10, 75))
    boxes = [("TEMPO (USA, 2023)", (-130, -60, 15, 60), BLUE), ("Sentinel-4 (Europe, 2025)", (-30, 45, 28, 70), GREEN),
             ("GEMS (Korea, 2020)", (75, 150, -5, 45), ORANGE)]
    for n, (x0, x1, y0, y1), c in boxes:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, alpha=0.18, ec=c, lw=1.2,
                               transform=ccrs.PlateCarree()))
        ax.text((x0 + x1) / 2, y1 + 1.5, n, fontsize=6.8, color=c, ha="center", va="bottom",
                transform=ccrs.PlateCarree(), weight="bold")
    note(ax, "Approximate fields of regard of the geostationary air-quality constellation (hourly daytime NO₂, O₃, "
             "HCHO, aerosols).", xy=(1, -0.04))
    save(fig, "ch16_aqgeo")


def radio_occ():
    fig, ax = canvas(7.0, 3.2, xlim=(0, 100), ylim=(0, 46))
    earth(ax, 50, -70, 85, atmosphere=False)
    for r, a in [(88, 0.18), (91, 0.12), (94, 0.07)]:
        ax.add_patch(Circle((50, -70), r, fc="none", ec=SKY, lw=6, alpha=a))
    satellite(ax, 8, 36, s=0.9)
    satellite(ax, 92, 33, s=0.9)
    label(ax, 8, 41.5, "GNSS satellite\n(20 000 km away)", fs=6.6)
    label(ax, 92, 39, "LEO receiver", fs=6.6)
    xs = np.linspace(8, 92, 200)
    ys = 36 - (xs - 8) * 3 / 84 - 15 * np.sin(np.pi * (xs - 8) / 84) ** 6
    ax.plot(xs, ys, color=ORANGE, lw=1.6)
    ax.plot([50], [ys[100]], "o", color=RED, ms=4)
    label(ax, 50, ys[100] + 2.6, "tangent point", fs=6.6, color=RED)
    ax.plot([8, 92], [36, 33], color=GREY, lw=0.7, ls=":")
    label(ax, 71, 30, "straight line (no atmosphere)", fs=6.2, color=GREY)
    box(ax, 3, 4, 34, 11, "Bending angle α(height) → refractivity\n→ temperature, pressure, humidity profiles",
        fs=6.4, fc="white")
    box(ax, 64, 4, 33, 11, "Self-calibrating, all-weather,\n≈ 0.1–1.5 km vertical resolution", fs=6.4, fc="white")
    save(fig, "ch16_radioocc")


def altimetry():
    fig, ax = canvas(7.0, 3.4, xlim=(0, 100), ylim=(0, 48))
    x = np.linspace(0, 100, 300)
    ssh = 12 + 1.5 * np.sin(x / 9) + 0.6 * np.sin(x / 2.3)
    geoid = 11 + 1.2 * np.sin(x / 9 + 0.4)
    ax.fill_between(x, 0, ssh, color=EARTH, alpha=0.35)
    ax.plot(x, ssh, color=BLUE, lw=1.4)
    ax.plot(x, geoid, color=GREEN, lw=1, ls="--")
    ax.plot(x, np.full_like(x, 6), color=GREY, lw=1, ls="-.")
    label(ax, 3, 4.2, "reference ellipsoid", fs=6.4, color=GREY, ha="left", bg="white")
    label(ax, 99, geoid[-1] - 2.2, "geoid", fs=6.4, color=GREEN, ha="right", bg="white")
    label(ax, 3, ssh[10] + 1.8, "sea surface", fs=6.4, color=BLUE, ha="left")
    satellite(ax, 50, 42, s=1.0)
    ax.plot(x, 42 + 0 * x, color=GREY, lw=0.6, ls=":")
    label(ax, 3, 43.5, "orbit known to ≈ 1 cm (GNSS, DORIS, laser ranging)", fs=6.4, color=GREY, ha="left")
    i = 150
    darrow(ax, (52, 40.5), (52, ssh[i]), color=ORANGE)
    label(ax, 53.5, 27, "range R from radar\npulse travel time", fs=6.6, color=ORANGE, ha="left")
    darrow(ax, (40, 6), (40, 42), color=NAVY)
    label(ax, 38.5, 25, "orbit\nheight H", fs=6.6, color=NAVY, ha="right")
    box(ax, 62, 30, 36, 9, "SSH = H − R − corrections\n(ionosphere, troposphere, sea state, tides)", fs=6.4,
        fc="white")
    save(fig, "ch16_altimetry")


if __name__ == "__main__":
    fns = [geo_ring, orbits_lt, abi_scan, weighting, mw_spectrum, nwp_flow, skill, sea_ice, sea_level, ozone, aq_geo,
           radio_occ, altimetry]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
