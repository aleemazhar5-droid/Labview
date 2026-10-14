import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403

MU = 3.986004418e14
RE = 6378137.0
SIGMA = 5.670374e-8

# Approximate thermospheric density (kg/m^3) for low and high solar activity (MSIS-like values)
ALT = np.array([100, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000])
RHO_MIN = np.array([5.3e-7, 2.2e-8, 2.0e-9, 2.1e-10, 4.0e-11, 1.0e-11, 3.0e-12, 1.0e-12, 3.5e-13, 1.3e-13,
                    2.2e-14, 5.5e-15, 2.0e-15, 9.0e-16, 5.0e-16])
RHO_MAX = np.array([5.6e-7, 2.4e-8, 2.2e-9, 3.5e-10, 1.0e-10, 3.9e-11, 1.7e-11, 7.5e-12, 3.6e-12, 1.8e-12,
                    5.0e-13, 1.6e-13, 5.5e-14, 2.1e-14, 8.5e-15])


def rho(h_km, level=0.5):
    lmin = np.interp(h_km, ALT, np.log(RHO_MIN))
    lmax = np.interp(h_km, ALT, np.log(RHO_MAX))
    return np.exp(lmin + level * (lmax - lmin))


def temperature_profile():
    z = np.linspace(0, 500, 1001)
    layers = [(0, 288.15, -6.5), (11, 216.65, 0), (20, 216.65, 1.0), (32, 228.65, 2.8), (47, 270.65, 0),
              (51, 270.65, -2.8), (71, 214.65, -2.0)]

    def t_std(h):
        for k in range(len(layers) - 1, -1, -1):
            if h >= layers[k][0]:
                h0, t0, lr = layers[k]
                return t0 + lr * (h - h0)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for tinf, col, lab in [(700, BLUE, "Solar minimum (T∞ ≈ 700 K)"), (1000, GREEN, "Moderate (T∞ ≈ 1000 K)"),
                           (1400, RED, "Solar maximum (T∞ ≈ 1400 K)")]:
        T = []
        for h in z:
            if h <= 86:
                T.append(t_std(min(h, 86)))
            elif h <= 120:
                t86 = t_std(86)
                T.append(t86 + (360 - t86) * ((h - 86) / 34) ** 2.2)
            else:
                T.append(tinf - (tinf - 360) * np.exp(-0.02 * (h - 120) * 360 / tinf * 1.6))
        ax.plot(T, z, color=col, label=lab)
    for h, name in [(11, "Tropopause"), (47, "Stratopause"), (86, "Mesopause")]:
        ax.axhline(h, color=GREY, lw=0.6, ls="--")
        ax.text(1480, h + 3, name, fontsize=7, color=GREY, ha="right")
    for h, name in [(5, "Troposphere"), (30, "Stratosphere"), (66, "Mesosphere"), (250, "Thermosphere"),
                    (470, "Exobase region (≈500 km) → exosphere")]:
        ax.text(560, h, name, fontsize=8, color=NAVY, weight="bold", va="center")
    ax.axhspan(80, 105, color=ORANGE, alpha=0.08)
    ax.text(1480, 96, "Meteors burn up, aurora", fontsize=6.8, color=ORANGE, ha="right")
    ax.axhline(400, color=BLUE, lw=0.5, ls=":")
    ax.text(160, 404, "ISS ≈ 400–420 km", fontsize=7, color=BLUE)
    ax.set_xlim(150, 1500)
    ax.set_ylim(0, 500)
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Altitude (km)")
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.62))
    save(fig, "ch02_temperature")


def density():
    h = np.linspace(100, 1000, 400)
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    ax.fill_betweenx(h, rho(h, 0), rho(h, 1), color=SKY, alpha=0.35, label="Range: solar min → solar max")
    ax.plot(rho(h, 0), h, color=BLUE, lw=1.4, label="Solar minimum (F10.7 ≈ 70)")
    ax.plot(rho(h, 1), h, color=RED, lw=1.4, label="Solar maximum (F10.7 ≈ 230)")
    ax.set_xscale("log")
    ax.set_xlabel("Neutral mass density (kg/m³)")
    ax.set_ylabel("Altitude (km)")
    for y, t in [(410, "ISS"), (550, "Starlink shells (≈480–560 km)"), (705, "Landsat / Sentinel-2 (≈700–790 km)")]:
        ax.axhline(y, color=GREY, lw=0.5, ls=":")
        ax.text(2e-16, y + 8, t, fontsize=7, color=GREY)
    ax.set_xlim(1e-16, 1e-6)
    ax.legend(loc="upper right")
    note(ax, "Representative values from empirical models (NRLMSIS-type); density at 400 km varies by ~10× over a solar cycle.",
         xy=(1, -0.17))
    save(fig, "ch02_density")


def lifetime():
    def life(h0, bc, level):
        a = RE + h0 * 1e3
        t = 0.0
        while a - RE > 150e3:
            hk = (a - RE) / 1e3
            r = rho(hk, level)
            dadt = -r * np.sqrt(MU * a) / bc
            dt = min(5 * 86400.0, max(600.0, 0.002 * (a - RE - 140e3) / abs(dadt)))
            a += dadt * dt
            t += dt
            if t > 400 * 3.156e7:
                break
        return t / 3.156e7
    h0s = np.arange(200, 905, 20)
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    for bc, col in [(25, ORANGE), (100, BLUE), (400, NAVY)]:
        lmid = [life(h, bc, 0.5) for h in h0s]
        lmin = [life(h, bc, 0.0) for h in h0s]
        lmax = [life(h, bc, 1.0) for h in h0s]
        ax.fill_between(h0s, lmax, lmin, color=col, alpha=0.12)
        ax.plot(h0s, lmid, color=col, label=f"m/(C$_D$A) = {bc} kg/m²")
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 400)
    ax.set_xlim(200, 900)
    for y, t in [(1 / 365, "1 day"), (1 / 12, "1 month"), (1, "1 year"), (5, "5 years (FCC disposal rule)"),
                 (25, "25 years (old guideline)"), (100, "1 century")]:
        ax.axhline(y, color=GREY, lw=0.5, ls=":")
        ax.text(205, y * 1.12, t, fontsize=6.8, color=GREY)
    ax.set_xlabel("Initial circular-orbit altitude (km)")
    ax.set_ylabel("Orbital lifetime (years, log scale)")
    ax.legend(loc="lower right")
    note(ax, "Lines: moderate solar activity; shaded bands: solar max (shorter) to solar min (longer). "
             "Simple drag model (decay to 150 km).", xy=(1, -0.16))
    save(fig, "ch02_lifetime")


def thermal_alpha_eps():
    S = 1361.0
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    a = np.linspace(0.02, 1.0, 300)
    e = np.linspace(0.02, 1.0, 300)
    A, E = np.meshgrid(a, e)
    # isothermal sphere in sunlight, no Earth input: T = (alpha S /(4 eps sigma))^(1/4)
    T = (A * S / (4 * E * SIGMA)) ** 0.25 - 273.15
    cs = ax.contour(A, E, T, levels=[-100, -50, -20, 0, 20, 50, 100, 200, 300], colors=GREY, linewidths=0.6)
    ax.clabel(cs, fmt="%d °C", fontsize=6.5)
    coat = [("White paint (Z93/S13G)", 0.18, 0.90), ("Optical solar reflector (OSR)", 0.08, 0.80),
            ("Black paint (Z306)", 0.95, 0.89), ("Polished aluminium", 0.15, 0.05), ("Vapour-deposited gold", 0.25, 0.03),
            ("Kapton (aluminised, Kapton side)", 0.40, 0.65), ("Silver Teflon", 0.08, 0.78),
            ("Solar cell (GaAs, cover glass)", 0.91, 0.85), ("Anodised aluminium (black)", 0.65, 0.82),
            ("Germanium-coated Kapton", 0.47, 0.81), ("Beta cloth", 0.36, 0.86)]
    off = {"Silver Teflon": (0.015, -0.035), "Optical solar reflector (OSR)": (0.015, 0.012),
           "Anodised aluminium (black)": (-0.015, -0.04), "Germanium-coated Kapton": (-0.02, 0.018),
           "Vapour-deposited gold": (0.015, -0.01), "Polished aluminium": (0.015, 0.012)}
    for n, al, ep in coat:
        ax.scatter(al, ep, color=ORANGE, s=26, zorder=3, edgecolor="white", lw=0.5)
        dx, dy = off.get(n, (0.015, 0.012))
        ax.text(al + dx, ep + dy, n, fontsize=6.6, zorder=4, ha="left" if dx > 0 else "right",
                bbox=dict(fc="white", ec="none", pad=0.4, alpha=0.8))
    ax.set_xlabel("Solar absorptance α")
    ax.set_ylabel("Infrared emittance ε")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.02)
    note(ax, "Contours: equilibrium temperature of an isolated sphere in full sunlight at 1 AU, T = (αS/4εσ)^¼.",
         xy=(1, -0.13))
    save(fig, "ch02_alpha_eps")


def belts():
    fig, ax = canvas(7.2, 4.0, (-11, 11), (-6, 6), bg=SPACE)
    th = np.linspace(-np.pi / 2, np.pi / 2, 400)

    def shell(L1, L2, color, alpha):
        for L in np.linspace(L1, L2, 26):
            r = L * np.cos(th) ** 2
            for s in (1, -1):
                ax.fill(s * r * np.cos(th), r * np.sin(th), color=color, alpha=alpha, lw=0)
    shell(1.25, 2.4, "#E07A5F", 0.05)
    shell(3.2, 7.0, "#3D8BD9", 0.03)
    for L in [1.5, 2, 3, 4, 5, 6.6, 8, 10]:
        r = L * np.cos(th) ** 2
        for s in (1, -1):
            ax.plot(s * r * np.cos(th), r * np.sin(th), color="#9fb3c8", lw=0.4, alpha=0.6)
    earth(ax, 0, 0, 1.0, z=5)
    for s in (1, -1):
        ax.add_patch(Circle((0, 0), 6.62, fc="none", ec="#F2C14E", lw=0.8, ls="--", zorder=4))
        ax.add_patch(Circle((0, 0), 4.17, fc="none", ec="#B0E0A8", lw=0.8, ls="--", zorder=4))
    ax.text(0, 6.75, "GEO (6.6 R$_E$)", color="#F2C14E", fontsize=7, ha="center")
    ax.text(0, 4.3, "GNSS MEO (≈4.2 R$_E$)", color="#B0E0A8", fontsize=7, ha="center")
    ax.text(-1.85, -0.25, "Inner belt\nprotons 10–400 MeV\n(L ≈ 1.2–2.5)", color="#F4A582", fontsize=6.6, ha="center",
            va="center")
    ax.text(5.1, 0.0, "Outer belt\nelectrons 0.1–10 MeV\n(L ≈ 3–7)", color="#9ECAE9", fontsize=6.6, ha="center",
            va="center")
    ax.text(2.9, -0.0, "slot", color="white", fontsize=6.3, ha="center", va="center")
    ax.text(-10.6, 5.4, "Earth's radiation belts (meridian cross-section)", color="white", fontsize=8.5,
            weight="bold")
    ax.text(-10.6, -5.6, "Field lines: dipole L-shells, r = L cos²λ (R$_E$)", color="#9fb3c8", fontsize=6.5)
    ax.annotate("South Atlantic Anomaly:\ninner belt dips to ≈200 km", xy=(0.4, -0.95), xytext=(3.2, -4.4),
                color="white", fontsize=6.6, arrowprops=dict(arrowstyle="-", color="white", lw=0.6))
    save(fig, "ch02_belts")


def saa_map():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.2, 3.6))
    ax = world_axes(fig, proj=ccrs.PlateCarree())
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-90, 90, 181)
    LON, LAT = np.meshgrid(lon, lat)
    f = np.exp(-(((LON + 48) / 38) ** 2 + ((LAT + 26) / 15) ** 2)) + 0.25 * np.exp(-(((LON + 5) / 25) ** 2 + ((LAT + 32) / 11) ** 2))
    pole = 0.35 * (np.exp(-((LAT - 70) / 7) ** 2) + np.exp(-((LAT + 68) / 7) ** 2))
    flux = f + pole
    cf_ = ax.contourf(LON, LAT, flux, levels=[0.1, 0.2, 0.35, 0.5, 0.7, 0.9, 1.1], cmap="YlOrRd", alpha=0.75,
                      transform=ccrs.PlateCarree())
    lonT, latT = ground_track(6378 + 415, 51.6, hours=24)
    plot_track(ax, lonT, latT, color=BLUE, lw=0.5, alpha=0.6)
    ax.text(-60, -5, "South Atlantic\nAnomaly", fontsize=7.5, weight="bold", color="#7a1f0f", ha="center")
    ax.text(10, 75, "Auroral-zone\nelectron precipitation", fontsize=6.6, color="#7a1f0f", ha="center")
    cb = fig.colorbar(cf_, ax=ax, orientation="vertical", fraction=0.025, pad=0.02)
    cb.set_label("Relative trapped-particle flux at ≈500 km", fontsize=7)
    cb.ax.tick_params(labelsize=6)
    ax.set_title("Schematic radiation hot spots at LEO altitude, with 24 h of ISS ground track", fontsize=8.5)
    save(fig, "ch02_saa", raster=True)


def dose_depth():
    t = np.array([0.5, 1, 2, 3, 5, 7, 10, 15, 20])
    curves = {"GNSS MEO (20 200 km, 55°)": (BLUE, 900, 1.9), "GEO": (RED, 300, 1.7),
              "LEO polar (800 km SSO)": (GREEN, 25, 1.1), "LEO ISS (400 km, 51.6°)": (ORANGE, 4, 0.9)}
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    for name, (c, d1, k) in curves.items():
        dose = d1 * t ** (-k) * np.exp(-0.03 * t)
        dose = np.where(t > 5, dose * (1 + 0.0 * t), dose)
        floor = {"GEO": 0.3, "GNSS MEO (20 200 km, 55°)": 0.6, "LEO polar (800 km SSO)": 0.35,
                 "LEO ISS (400 km, 51.6°)": 0.08}[name]
        ax.plot(t, dose + floor, color=c, marker="o", ms=3, label=name)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Aluminium shield thickness (mm), solid-sphere geometry")
    ax.set_ylabel("Total ionising dose (krad(Si) per year)")
    for y, t_ in [(5, "typical COTS part tolerance (5–10 krad total)"), (100, "radiation-hardened parts (≥100 krad)")]:
        ax.axhline(y, color=GREY, ls="--", lw=0.6)
        ax.text(0.52, y * 1.12, t_, fontsize=6.6, color=GREY)
    ax.legend(loc="upper right")
    ax.set_ylim(0.05, 3000)
    note(ax, "Illustrative order-of-magnitude curves for solar-maximum trapped + solar-proton environments "
             "(AE8/AP8-SHIELDOSE style). Always compute mission-specific doses.", xy=(1, -0.15))
    save(fig, "ch02_dose_depth")


def weibull():
    let = np.linspace(0, 100, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    for L0, W, s, sat, c, n in [(1.5, 20, 1.5, 1e-7, RED, "Commercial SRAM (soft)"),
                                (15, 30, 2.0, 3e-8, ORANGE, "Rad-tolerant FPGA config. memory"),
                                (40, 40, 2.5, 5e-9, BLUE, "Rad-hard-by-design SRAM")]:
        x = np.clip(let - L0, 0, None)
        sig = sat * (1 - np.exp(-(x / W) ** s))
        ax.plot(let, np.where(sig > 0, sig, np.nan), color=c, label=n)
        ax.axvline(L0, color=c, lw=0.5, ls=":")
    ax.set_yscale("log")
    ax.set_ylim(1e-11, 3e-7)
    ax.set_xlabel("Linear energy transfer, LET (MeV·cm²/mg)")
    ax.set_ylabel("SEE cross-section (cm²/bit)")
    ax.legend(loc="lower right")
    ax.text(62, 1.4e-7, "saturated cross-section σ$_{sat}$", fontsize=7, color=GREY)
    ax.text(16, 2e-11, "threshold LET$_{th}$", fontsize=7, color=GREY, rotation=90)
    note(ax, "Weibull fits σ(L) = σsat·[1 − exp(−((L − L0)/W)^s)], as used to predict upset rates (e.g., with CREME96).",
         xy=(1, -0.18))
    save(fig, "ch02_weibull")


def mmod_flux():
    d = np.logspace(-3, 1.3, 200)  # cm
    met = 2.0e-1 * (d / 0.01) ** -2.6
    deb = 6.0e-1 * (d / 0.01) ** -2.3
    deb = np.where(d > 0.1, deb * (d / 0.1) ** 0.35, deb)
    met = np.where(d > 0.1, met * (d / 0.1) ** -0.4, met)
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    ax.plot(d * 10, deb, color=RED, label="Orbital debris (ORDEM-like, 400 km, 51.6°)")
    ax.plot(d * 10, met, color=VIOLET, label="Meteoroids (MEM-like)")
    ax.plot(d * 10, deb + met, color=NAVY, lw=2, label="Total")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Particle diameter (mm)")
    ax.set_ylabel("Cumulative flux, particles ≥ d (per m² per year)")
    for x, t in [(1, "≈1 mm: penetrates\nunshielded walls"), (10, "≈1 cm: defeats\nWhipple shields"),
                 (100, "≥10 cm:\ntracked")]:
        ax.axvline(x, color=GREY, lw=0.5, ls=":")
        ax.text(x * 1.1, 3e1, t, fontsize=6.6, color=GREY, va="top")
    ax.set_xlim(1e-2, 200)
    ax.set_ylim(1e-9, 1e3)
    ax.legend(loc="lower left")
    note(ax, "Illustrative cumulative flux at ISS altitude; actual risk assessments use NASA ORDEM 3.x / ESA MASTER and MEM.",
         xy=(1, -0.15))
    save(fig, "ch02_mmod_flux")


def whipple():
    fig, ax = canvas(7.0, 2.8, (0, 100), (0, 38))
    ax.add_patch(Rectangle((32, 4), 1.2, 30, fc="#9AA5B1", ec="none"))
    ax.add_patch(Rectangle((62, 4), 3.5, 30, fc="#5B6670", ec="none"))
    ax.text(32.6, 35.5, "Bumper\n(1–2 mm Al)", ha="center", fontsize=7)
    ax.text(63.7, 35.5, "Rear wall\n(pressure hull)", ha="center", fontsize=7)
    ax.add_patch(Circle((12, 19), 1.4, fc=ORANGE, ec="none"))
    arrow(ax, (14, 19), (31, 19), "projectile ≈7–15 km/s", color=ORANGE, fs=7)
    rng = np.random.default_rng(2)
    for k in range(70):
        ang = rng.normal(0, 0.28)
        L = rng.uniform(6, 27)
        x0, y0 = 33.5, 19
        x1, y1 = x0 + L * np.cos(ang), y0 + L * np.sin(ang)
        ax.plot([x0, x1], [y0, y1], color=RED, lw=0.5, alpha=0.6)
        ax.add_patch(Circle((x1, y1), rng.uniform(0.15, 0.5), fc=RED, alpha=0.7, ec="none"))
    ax.text(20, 6, "Debris cloud (molten / vaporised\nfragments) spreads the momentum\nover a large area of the rear wall",
            fontsize=6.6, ha="center", color=RED)
    darrow(ax, (33.5, 8), (62, 8), color=GREY, lw=0.8)
    ax.text(48, 9.2, "standoff S (10–30 cm)", fontsize=6.8, color=GREY, ha="center")
    ax.add_patch(Rectangle((47, 14), 2, 10, fc="#E9C46A", alpha=0.5, ec="none"))
    ax.text(48, 25.5, "optional Kevlar /\nNextel blanket\n(stuffed Whipple)", fontsize=6.4, ha="center")
    ax.text(80, 19, "Ballistic limit:\ncritical particle diameter\nthat just perforates the\nrear wall, d$_c$(v, θ, ρ)",
            fontsize=7, va="center")
    save(fig, "ch02_whipple")


def gevs():
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    f = np.array([20, 50, 800, 2000])
    q = np.array([0.026, 0.16, 0.16, 0.026])
    a = q / 2.0
    ax.loglog(f, q, color=RED, lw=2, label="Qualification (14.1 g rms)")
    ax.loglog(f, a, color=BLUE, lw=2, label="Acceptance (10.0 g rms)")
    ax.set_xlim(10, 3000)
    ax.set_ylim(0.005, 0.5)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Acceleration spectral density (g²/Hz)")
    ax.text(25, 0.06, "+6 dB/oct", fontsize=7, color=GREY, rotation=35)
    ax.text(1050, 0.075, "−6 dB/oct", fontsize=7, color=GREY, rotation=-35)
    ax.legend(loc="lower center")
    note(ax, "Generalized random-vibration test levels for components ≤ 22.7 kg (NASA GSFC-STD-7000, GEVS). "
             "Duration 2 min/axis (qual), 1 min/axis (acceptance).", xy=(1, -0.18))
    save(fig, "ch02_gevs")


def solar_spectrum():
    lam = np.linspace(0.1, 30, 3000) * 1e-6
    h, c, k = 6.62607e-34, 2.998e8, 1.380649e-23

    def planck(T):
        return 2 * h * c ** 2 / lam ** 5 / (np.exp(h * c / (lam * k * T)) - 1)
    sun = planck(5772) * (6.957e8 / 1.496e11) ** 2 * np.pi
    earth_ir = planck(255) * np.pi
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.plot(lam * 1e6, sun / 1e6, color=ORANGE, label="Sunlight at 1 AU (5772 K blackbody, total 1361 W/m²)")
    ax.plot(lam * 1e6, earth_ir / 1e6, color=RED, label="Earth's emitted IR (≈255 K, ≈240 W/m²)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 3e3)
    ax.set_xlim(0.1, 30)
    ax.axvspan(0.38, 0.75, color=GOLD, alpha=0.12)
    ax.text(0.43, 1.2e3, "visible", fontsize=7)
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Spectral irradiance (W/m² per µm)")
    ax.legend(loc="lower left", fontsize=7)
    note(ax, "Spacecraft thermal design separates the 'solar' band (0.2–3 µm, absorptance α) from the 'thermal IR' band "
             "(3–50 µm, emittance ε).", xy=(1, -0.18))
    save(fig, "ch02_spectrum")


def env_matrix():
    rows = ["Atmospheric drag", "Atomic oxygen", "Trapped protons", "Trapped electrons", "Solar particle events",
            "Galactic cosmic rays", "Surface charging", "Internal charging", "Debris flux", "Thermal cycling"]
    cols = ["VLEO\n<350 km", "LEO\n350–1000", "Polar LEO\n/SSO", "MEO\nGNSS", "GEO", "HEO /\nMolniya",
            "Cislunar\n/ L2", "Deep\nspace"]
    M = np.array([
        [3, 2, 2, 0, 0, 1, 0, 0],
        [3, 2, 2, 0, 0, 1, 0, 0],
        [1, 2, 2, 2, 0, 3, 0, 0],
        [0, 1, 2, 3, 3, 3, 1, 0],
        [0, 1, 2, 3, 3, 3, 3, 3],
        [0, 1, 1, 2, 3, 2, 3, 3],
        [0, 0, 2, 2, 3, 3, 1, 1],
        [0, 0, 1, 3, 3, 3, 1, 1],
        [1, 3, 3, 1, 1, 1, 0, 0],
        [3, 3, 3, 1, 1, 2, 1, 1]])
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["#F3F6F9", "#CFE3F3", "#7FB3DA", "#1F6FB2"])
    ax.imshow(M, cmap=cmap, aspect="auto", vmin=0, vmax=3)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, fontsize=7)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows, fontsize=7.5)
    ax.xaxis.tick_top()
    ax.grid(False)
    lab = ["–", "low", "med", "high"]
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, lab[M[i, j]], ha="center", va="center", fontsize=6.6,
                    color="white" if M[i, j] == 3 else INK)
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, "ch02_env_matrix")


def deep_space_env():
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    bodies = ["Mercury", "Venus (surface)", "Earth", "Moon", "Mars", "Jupiter (Europa orbit)", "Saturn (Titan)",
              "Pluto"]
    tmin = [-180, 462, -89, -248, -153, -223, -180, -240]
    tmax = [430, 470, 58, 120, 20, -148, -179, -218]
    y = np.arange(len(bodies))
    for yi, a, b in zip(y, tmin, tmax):
        ax.plot([a, b], [yi, yi], color=ORANGE, lw=6, solid_capstyle="round")
        ax.text(b + 12, yi, f"{a}…{b} °C", va="center", fontsize=6.8)
    ax.set_yticks(y)
    ax.set_yticklabels(bodies)
    ax.invert_yaxis()
    ax.set_xlim(-280, 560)
    ax.axvline(0, color=GREY, lw=0.5)
    ax.set_xlabel("Surface (or local) temperature range (°C)")
    ax.grid(axis="y", visible=False)
    note(ax, "Lunar permanently shadowed craters reach ≈ −248 °C (25 K); Venus' surface is nearly isothermal at ≈465 °C.",
         xy=(1, -0.17))
    save(fig, "ch02_planet_temps")


if __name__ == "__main__":
    temperature_profile(); density(); lifetime(); thermal_alpha_eps(); belts(); saa_map(); dose_depth(); weibull()
    mmod_flux(); whipple(); gevs(); solar_spectrum(); env_matrix(); deep_space_env()
