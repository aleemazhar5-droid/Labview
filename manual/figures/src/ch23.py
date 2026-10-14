import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, Wedge

ROOT = Path(__file__).resolve().parents[2]


def dipole():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    lam = np.linspace(-np.pi / 2, np.pi / 2, 400)
    for L in [1.5, 2, 3, 4, 5, 6.6, 8, 10]:
        r = L * np.cos(lam) ** 2
        x, z = r * np.cos(lam), r * np.sin(lam)
        m = r >= 1
        c = ORANGE if L == 6.6 else (RED if L in (1.5, 2) else (GREEN if L in (4, 5) else BLUE))
        ax.plot(x[m], z[m], color=c, lw=1.0)
        ax.plot(-x[m], z[m], color=c, lw=1.0)
        ax.text(L + 0.1, 0.15, f"L={L:g}", fontsize=5.8, color=c)
    ax.add_patch(Circle((0, 0), 1, fc=EARTH, ec="none", zorder=3))
    ax.add_patch(Ellipse((-2, 0), 1.4 * 2 * 1.4 * 1.1, 1.4 * 2 * 1.4, fc="none", ec="none"))
    ax.text(6.7, -0.55, "GEO (6.6 R_E)", fontsize=6.2, color=ORANGE)
    ax.text(1.4, -1.6, "inner belt", fontsize=6.2, color=RED)
    ax.text(3.6, -2.1, "outer belt", fontsize=6.2, color=GREEN)
    ax.set_aspect("equal")
    ax.set_xlim(-11, 11)
    ax.set_ylim(-5.5, 5.5)
    ax.set_xlabel("Distance in magnetic equatorial plane (Earth radii)")
    ax.set_ylabel("R_E")
    note(ax, "Dipole field lines r = L cos²λ. Charged particles are trapped on these lines; L labels each field-line "
             "shell by its equatorial distance.", xy=(1, -0.16))
    save(fig, "ch23_dipole")


def magnetosphere():
    fig, ax = canvas(7.0, 3.8, xlim=(-40, 60), ylim=(-27, 27))
    th = np.linspace(-np.pi * 0.62, np.pi * 0.62, 200)

    def shue(r0, alpha, th):
        return r0 * (2 / (1 + np.cos(th))) ** alpha
    r = shue(10, 0.58, th)
    ax.plot(r * np.cos(th), r * np.sin(th), color=GREEN, lw=1.6)
    rb = shue(13, 0.8, th)
    ax.plot(rb * np.cos(th), rb * np.sin(th), color=VIOLET, lw=1.4, ls="--")
    ax.fill_between([-40, -6], [-11, -6], [11, 6], color=GREEN, alpha=0.06)
    ax.add_patch(Ellipse((-22, 0), 32, 3.2, fc=ORANGE, alpha=0.35, ec="none"))
    earth(ax, 0, 0, 1.3)
    ax.add_patch(Circle((0, 0), 4.5, fc=SKY, alpha=0.15, ec=SKY, lw=0.6))
    for a, b in [(2.0, 1.3), (5.0, 3.0)]:
        ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, fc="none", ec=RED, lw=1.2, ls="-"))
    for y in (-20, -14, 14, 20):
        ax.annotate("", (16, y), (50, y), arrowprops=dict(arrowstyle="->", color=GOLD, lw=1))
    label(ax, 40, 23, "solar wind", fs=7, color="#8A6D00")
    label(ax, 16, 16, "bow shock", fs=6.6, color=VIOLET)
    label(ax, 6, 11.5, "magnetopause", fs=6.6, color=GREEN)
    label(ax, 13, 4.5, "magneto-\nsheath", fs=6.2, color=GREY)
    label(ax, -22, 2.8, "plasma sheet", fs=6.4, color="#8A4B00")
    label(ax, -26, 8.5, "tail lobes", fs=6.4, color=GREEN)
    label(ax, 2.5, -5.2, "plasmasphere", fs=6.0, color=BLUE)
    label(ax, -6.2, -3.6, "radiation\nbelts", fs=6.0, color=RED)
    ax.plot([7, 2], [8, 3.5], color=GREY, lw=0.6)
    label(ax, 8.5, 9, "cusp", fs=6.2, color=GREY)
    label(ax, -35, -24, "magnetotail extends > 200 R_E", fs=6.4, color=GREY, ha="left")
    save(fig, "ch23_magnetosphere")


def standoff():
    P = np.logspace(-1, 2, 200)
    B0 = 3.1e-5
    mu0 = 4e-7 * np.pi
    r = (2 * B0 ** 2 / (mu0 * P * 1e-9)) ** (1 / 6)
    r_shue = (10.22 + 1.29 * np.tanh(0.184 * (0 + 8.14))) * P ** (-1 / 6.6)
    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    ax.plot(P, r, color=NAVY, lw=1.6, label="Pressure balance (Chapman–Ferraro, dipole ×2)")
    ax.plot(P, r_shue, color=GREEN, lw=1.4, ls="--", label="Empirical (Shue et al. 1998, B_z = 0)")
    ax.axhline(6.6, color=ORANGE, lw=0.9, ls=":")
    ax.text(0.12, 6.0, "geostationary orbit 6.6 R_E: GEO satellites exposed to the solar wind below this", fontsize=6.3,
            color=ORANGE)
    ax.axvspan(1, 3, color=GREY, alpha=0.1)
    ax.text(1.1, 14.2, "typical", fontsize=6.3, color=GREY)
    ax.set_xscale("log")
    ax.set_xlabel("Solar-wind dynamic pressure ρv² (nPa)")
    ax.set_ylabel("Subsolar magnetopause (R_E)")
    ax.set_ylim(4, 16)
    ax.legend(fontsize=6.4, loc="upper right")
    note(ax, "Strong storms with high pressure and southward IMF can push the magnetopause inside GEO.", xy=(1, -0.16))
    save(fig, "ch23_standoff")


def periods():
    E = np.logspace(-3, 3, 200)
    me, mp, c, q = 0.511, 938.27, 2.998e8, 1.602e-19
    RE = 6.371e6
    L = 4.5
    B = 3.1e-5 / L ** 3
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for m0, col, n in [(me, BLUE, "electron"), (mp, RED, "proton")]:
        g = 1 + E / m0
        beta = np.sqrt(1 - 1 / g ** 2)
        mass = m0 * 1e6 * q / c ** 2
        v = beta * c
        Tg = 2 * np.pi * g * mass / (q * B)
        Tb = 4 * L * RE / v * (1.30 - 0.56 * 1.0)
        Td = 2 * np.pi * q * B * (L * RE) ** 2 / (3 * g * mass * v ** 2 / 2)
        ax.plot(E, Tg, color=col, lw=1.0, ls=":", label=f"{n}: gyration")
        ax.plot(E, Tb, color=col, lw=1.4, ls="--", label=f"{n}: bounce")
        ax.plot(E, Td, color=col, lw=2.0, label=f"{n}: drift around Earth")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Kinetic energy (MeV)")
    ax.set_ylabel("Period (s)")
    for p_, n in [(1e-3, "1 ms"), (1, "1 s"), (3600, "1 h"), (86400, "1 day")]:
        ax.axhline(p_, color=GREY, lw=0.5, ls=":")
        ax.text(1.2e-3, p_ * 1.4, n, fontsize=6.2, color=GREY)
    ax.set_ylim(1e-6, 1e7)
    ax.legend(fontsize=6.0, loc="upper right", ncol=2)
    note(ax, "Dipole field at L = 4.5 (GNSS altitudes), equatorially mirroring particles. Drift periods depend on energy, not mass, so the two drift curves almost coincide.",
         xy=(1, -0.16))
    save(fig, "ch23_periods")


def motion():
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.4))
    t = np.linspace(0, 12 * np.pi, 800)
    a = axs[0]
    a.plot(t / 6, np.cos(t) * 0.5, color=BLUE, lw=1)
    a.annotate("", (4.5, 0), (0, 0), arrowprops=dict(arrowstyle="->", color=GREY))
    a.set_title("Gyration around the field\n(ms for electrons)", fontsize=7)
    a = axs[1]
    lam = np.linspace(-1.0, 1.0, 200)
    r = 4 * np.cos(lam) ** 2
    a.plot(r * np.cos(lam), r * np.sin(lam), color=GREY, lw=0.8)
    a.add_patch(Circle((0, 0), 1, fc=EARTH))
    tt = np.linspace(0, 6 * np.pi, 600)
    lam_p = 0.75 * np.sin(tt)
    rp = 4 * np.cos(lam_p) ** 2
    a.plot(rp * np.cos(lam_p) + 0.12 * np.cos(tt * 18), rp * np.sin(lam_p), color=RED, lw=0.7)
    a.text(2.6, 2.6, "mirror point", fontsize=6.2, color=RED)
    a.set_title("Bounce between mirror\npoints (≈ 0.1–1 s)", fontsize=7)
    a.set_aspect("equal")
    a = axs[2]
    a.add_patch(Circle((0, 0), 1, fc=EARTH))
    th = np.linspace(0, 2 * np.pi, 300)
    a.plot(4 * np.cos(th), 4 * np.sin(th), color=GREEN, lw=1.3)
    a.annotate("", (4 * np.cos(1.1), 4 * np.sin(1.1)), (4 * np.cos(0.8), 4 * np.sin(0.8)),
               arrowprops=dict(arrowstyle="-|>", color=GREEN))
    a.text(0, -5.3, "electrons drift east, ions west", fontsize=6.2, ha="center", color=GREEN)
    a.set_title("Drift around the Earth\n(minutes to hours)", fontsize=7)
    a.set_aspect("equal")
    for a in axs:
        a.axis("off")
    axs[1].set_xlim(-1.5, 5)
    axs[1].set_ylim(-3.5, 3.5)
    axs[2].set_xlim(-6, 6)
    axs[2].set_ylim(-6, 6)
    save(fig, "ch23_motion")


def belts():
    L = np.linspace(1.05, 9, 400)
    p = 3e4 * np.exp(-((L - 1.6) / 0.35) ** 2)
    ei = 1e5 * np.exp(-((L - 1.5) / 0.3) ** 2)
    eo = 3e6 * np.exp(-((L - 4.5) / 1.0) ** 2)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(L, p, color=RED, lw=1.8, label="protons > 10 MeV (inner belt)")
    ax.plot(L, ei + eo, color=BLUE, lw=1.8, label="electrons > 1 MeV (inner and outer belts)")
    ax.plot(L, 30 * eo * np.exp(-((L - 3.0) / 0.4) ** 2) / eo.max() * 3e6 * 0 + ei + eo * 6 * np.exp(-((L - 4.2) / 1.5) ** 2),
            color=BLUE, lw=1, ls="--", label="outer belt after a storm (schematic)")
    ax.axvspan(2.0, 3.0, color=GREY, alpha=0.1)
    ax.text(2.1, 3e6, "slot\nregion", fontsize=6.4, color=GREY)
    for x, n in [(1.1, "LEO\n(ISS)"), (4.2, "GNSS\nMEO"), (6.6, "GEO")]:
        ax.axvline(x, color=GREY, lw=0.6, ls=":")
        ax.text(x + 0.05, 1.5e7, n, fontsize=6.2, color=GREY, va="top")
    ax.set_yscale("log")
    ax.set_ylim(1e1, 3e7)
    ax.set_xlim(1, 9)
    ax.set_xlabel("L shell (Earth radii)")
    ax.set_ylabel("Omnidirectional flux (cm⁻² s⁻¹)")
    ax.legend(fontsize=6.3, loc="lower right")
    note(ax, "Schematic equatorial flux profiles after AE8/AP8 and Van Allen Probes results; values vary by orders of "
             "magnitude with activity.", xy=(1, -0.16))
    save(fig, "ch23_belts")


def dungey():
    fig, ax = canvas(7.0, 3.5, xlim=(-42, 42), ylim=(-21, 21))
    lam = np.linspace(-1.3, 1.3, 200)
    for L in (3.5, 6):
        r = L * np.cos(lam) ** 2
        x, z = r * np.cos(lam), r * np.sin(lam)
        ax.plot(x * 1.2, z, color=BLUE, lw=1.1)
        ax.plot(-x * 1.9, z, color=BLUE, lw=1.1)
    earth(ax, 0, 0, 1.6)
    for sgn in (1, -1):
        xs = np.linspace(-1, -40, 100)
        ax.plot(xs, sgn * (2 + 8 * (1 - np.exp(xs / 12))), color=GREEN, lw=1.2)
        xs2 = np.linspace(0.5, 12, 60)
        ax.plot(xs2, sgn * (1.8 + 0.9 * xs2), color=GREEN, lw=1.2)
        ax.plot([12, 12], [sgn * 12.6, sgn * 20], color=GREEN, lw=1.2)
    for x in (18, 25, 32, 39):
        ax.annotate("", (x, -17), (x, 17), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.0))
    label(ax, 32, 19.5, "southward interplanetary field", fs=6.4, color="#8A6D00")
    ax.plot(9, 0, "X", color=RED, ms=10)
    label(ax, 9.5, -3.6, "dayside\nreconnection", fs=6.2, color=RED)
    ax.plot(-24, 0, "X", color=RED, ms=10)
    label(ax, -24, -3.6, "tail\nreconnection", fs=6.2, color=RED)
    ax.annotate("", (-14, 15.5), (8, 15.5), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4))
    ax.annotate("", (-14, -15.5), (8, -15.5), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4))
    label(ax, -3, 18, "open field lines carried tailward over the poles", fs=6.2, color=ORANGE)
    ax.annotate("", (-3, 0.6), (-17, 0.6), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4, ls="--"))
    label(ax, -10, 2.4, "return flow", fs=6.0, color=ORANGE)
    label(ax, -33, 13.5, "tail lobe (open)", fs=6.2, color=GREEN)
    label(ax, 35, -19.5, "Sun →", fs=6.6, color=GREY)
    save(fig, "ch23_dungey")


def chapman(z, n0, z0, H):
    y = (z - z0) / H
    return n0 * np.exp(0.5 * (1 - y - np.exp(-y)))


def ionosphere():
    z = np.linspace(50, 1000, 600)
    day = chapman(z, 1.2e12, 300, 60) + chapman(z, 2.5e11, 180, 25) + chapman(z, 1.5e11, 110, 10) + chapman(z, 1e9, 80, 6)
    day += 3e10 * np.exp(-(z - 300) / 250) * (z > 300)
    night = chapman(z, 3e11, 330, 65) + chapman(z, 5e9, 110, 10)
    night += 1e10 * np.exp(-(z - 330) / 250) * (z > 330)
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    ax.plot(day, z, color=ORANGE, lw=1.8, label="Day (solar maximum, mid-latitude)")
    ax.plot(night, z, color=NAVY, lw=1.8, label="Night")
    for zz, n in [(80, "D"), (110, "E"), (180, "F1"), (300, "F2")]:
        ax.text(2e12, zz, n, fontsize=7, color=GREY, va="center")
    ax.set_xscale("log")
    ax.set_xlim(1e8, 5e12)
    ax.set_ylim(50, 1000)
    ax.set_xlabel("Electron density (m⁻³)")
    ax.set_ylabel("Altitude (km)")
    ax.legend(fontsize=6.6, loc="upper left")
    note(ax, "Sum of Chapman layers (schematic). Plasma frequency f_p ≈ 9√n_e Hz: 10¹² m⁻³ → 9 MHz.", xy=(1, -0.15))
    save(fig, "ch23_ionosphere")


def ionogram():
    z = np.linspace(80, 600, 4000)
    n = chapman(z, 1.0e12, 300, 55) + chapman(z, 1.2e11, 110, 9) + chapman(z, 2.0e11, 180, 22)
    fp = 8.98 * np.sqrt(n) / 1e6
    freqs = np.linspace(1.0, fp.max() * 0.999, 400)
    hv = []
    for f in freqs:
        idx = np.argmax(fp >= f)
        if fp[idx] < f:
            hv.append(np.nan)
            continue
        zz = z[:idx]
        mu_g = 1 / np.sqrt(np.clip(1 - (fp[:idx] / f) ** 2, 1e-4, 1))
        hv.append(80 + np.trapezoid(mu_g, zz) if hasattr(np, "trapezoid") else 80 + np.trapz(mu_g, zz))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.1), gridspec_kw=dict(wspace=0.3))
    a1.plot(fp, z, color=NAVY, lw=1.6)
    a1.set_xlabel("Plasma frequency (MHz)")
    a1.set_ylabel("True height (km)")
    a1.set_title("Model profile", fontsize=7.6)
    a2.plot(freqs, hv, color=ORANGE, lw=1.6)
    a2.set_xlabel("Sounding frequency (MHz)")
    a2.set_ylabel("Virtual height (km)")
    a2.set_title("Computed ionogram (ordinary wave)", fontsize=7.6)
    a2.axvline(fp.max(), color=RED, lw=0.8, ls="--")
    a2.text(fp.max() - 0.2, 650, f"foF2 = {fp.max():.1f} MHz", fontsize=6.4, color=RED, ha="right")
    a2.set_ylim(80, 800)
    note(a2, "Virtual height h' = ∫ μ_g dz with group index μ_g = 1/√(1 − f_p²/f²), no magnetic field or collisions.",
         xy=(1, -0.2))
    save(fig, "ch23_ionogram")


def tec_map():
    import cartopy.crs as ccrs
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-89, 89, 179)
    LON, LAT = np.meshgrid(lon, lat)
    lt = (LON / 15 + 14) % 24
    dip = 9 * np.sin(np.radians(LON + 70)) - 2
    mlat = LAT - dip
    day = np.clip(np.cos(np.radians((lt - 14) * 15)), 0, None) ** 1.2
    tec = 5 + 45 * day * np.exp(-((LAT) / 45) ** 2) + 50 * day * (np.exp(-((mlat - 15) / 7) ** 2) + np.exp(-((mlat + 15) / 7) ** 2)) * \
        np.clip((lt - 9) / 5, 0, 1)
    fig = plt.figure(figsize=(7.0, 3.4))
    ax = world_axes(fig)
    pc = ax.pcolormesh(LON, LAT, tec, cmap="magma", alpha=0.75, transform=ccrs.PlateCarree(), shading="auto")
    ax.coastlines(lw=0.4, color="white")
    cb = fig.colorbar(pc, ax=ax, shrink=0.75, pad=0.02)
    cb.set_label("TEC (TECU)", fontsize=7)
    cb.ax.tick_params(labelsize=6.5)
    ax.text(150, -40, "night", fontsize=7, color="white", transform=ccrs.PlateCarree())
    ax.text(-30, 25, "equatorial ionization anomaly crests", fontsize=6.6, color="white", transform=ccrs.PlateCarree(),
            ha="center")
    note(ax, "Schematic total electron content at 14:00 local time over 0° longitude, near solar maximum (illustrative "
             "model, not data).", xy=(1, -0.03))
    save(fig, "ch23_tecmap", raster=True)


def auroral_oval():
    import cartopy.crs as ccrs
    import cartopy.feature as cf
    fig = plt.figure(figsize=(6.4, 3.4))
    for k, Kp in enumerate([2, 5, 9]):
        ax = fig.add_subplot(1, 3, k + 1, projection=ccrs.NorthPolarStereo())
        ax.set_extent([-180, 180, 25, 90], crs=ccrs.PlateCarree())
        ax.add_feature(cf.NaturalEarthFeature("physical", "land", "110m", fc="#E4E8DC", ec="none"))
        ax.coastlines(lw=0.3, color="#8A9AA8")
        mlt = np.linspace(0, 2 * np.pi, 200)
        eq = 67 - 2.2 * Kp + 4.5 * np.cos(mlt)
        po = 75 - 0.6 * Kp + 5 * np.cos(mlt)
        plon, plat = -72.7, 80.7
        lons, lats_e, lats_p = [], [], []
        for a, le, lp in zip(mlt, eq, po):
            lons.append(np.degrees(a) + plon - 180)
            lats_e.append(le)
            lats_p.append(lp)
        lons = np.array(lons)
        ax.fill_between(lons, lats_e, lats_p, transform=ccrs.PlateCarree(), color=GREEN, alpha=0.45)
        ax.set_title(f"Kp = {Kp}", fontsize=7.6)
    note(fig.axes[2], "Schematic auroral oval (geographic coordinates, approximate). The oval expands towards the "
                      "equator as activity increases.", xy=(1, -0.06))
    save(fig, "ch23_oval")


def missions():
    fig, ax = plt.subplots(figsize=(7.0, 3.1))
    ev = [(1958.1, "Explorer 1\n(Van Allen belts)"), (1961.7, "Explorer 12"), (1977.8, "ISEE 1/2"),
          (1981.6, "Dynamics\nExplorer"), (1992.6, "Geotail"), (1996.2, "Polar, Wind"), (2000.6, "Cluster (4)"),
          (2007.1, "THEMIS (5)"), (2012.7, "Van Allen\nProbes"), (2013.9, "Swarm (3)"), (2015.2, "MMS (4)"),
          (2016.9, "Arase"), (2018.1, "GOLD"), (2019.8, "ICON"), (2025.6, "TRACERS"), (2026.4, "SMILE")]
    timeline(ax, ev, y=0, x0=1956, x1=2029, stagger=3, height=1.0, fs=6.0)
    ax.set_xlim(1954, 2030)
    ax.set_ylim(-4.8, 4.8)
    ax.axis("off")
    for yr in range(1960, 2030, 10):
        ax.text(yr, -0.35, str(yr), fontsize=6.2, ha="center", va="top", color=GREY)
    save(fig, "ch23_missions")


def atmosphere():
    z = np.linspace(0, 600, 601)
    T = np.zeros_like(z)
    for i, h in enumerate(z):
        if h < 11:
            T[i] = 288.15 - 6.5 * h
        elif h < 20:
            T[i] = 216.65
        elif h < 32:
            T[i] = 216.65 + (h - 20)
        elif h < 47:
            T[i] = 228.65 + 2.8 * (h - 32)
        elif h < 51:
            T[i] = 270.65
        elif h < 71:
            T[i] = 270.65 - 2.8 * (h - 51)
        elif h < 86:
            T[i] = 214.65 - 2.0 * (h - 71)
        else:
            T[i] = 1000 - (1000 - 186.9) * np.exp(-0.02 * (h - 86))
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.plot(T, z, color=RED, lw=1.8, label="Neutral temperature")
    T2 = np.where(z > 86, 1400 - (1400 - 186.9) * np.exp(-0.02 * (z - 86)), T)
    T3 = np.where(z > 86, 700 - (700 - 186.9) * np.exp(-0.02 * (z - 86)), T)
    ax.fill_betweenx(z, T3, T2, color=RED, alpha=0.12, label="solar minimum – maximum range")
    for y, n in [(5, "troposphere"), (30, "stratosphere"), (68, "mesosphere"), (450, "thermosphere")]:
        ax.text(1180, y, n, fontsize=6.6, color=GREY, ha="right", va="center")
    ax.axhspan(60, 1000, xmin=0.94, xmax=1.0, color=VIOLET, alpha=0.3)
    ax.text(1390, 330, "ionosphere (60–1 000 km)", fontsize=6.4, color=VIOLET, rotation=90, va="center")
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Altitude (km)")
    ax.set_xlim(150, 1500)
    ax.set_ylim(0, 600)
    ax.legend(fontsize=6.4, loc="upper left")
    note(ax, "US Standard Atmosphere 1976 below 86 km; Bates-type thermosphere profile above (illustrative).",
         xy=(1, -0.15))
    save(fig, "ch23_atmosphere")


if __name__ == "__main__":
    fns = [dipole, magnetosphere, standoff, periods, motion, belts, dungey, ionosphere, ionogram, tec_map, auroral_oval,
           missions, atmosphere]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
