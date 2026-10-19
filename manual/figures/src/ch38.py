import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge  # noqa: F401
from scipy.special import j1

H, C, K, SIG = 6.62607e-34, 2.99792e8, 1.380649e-23, 5.670374e-8
MAS = 206264.806e3          # mas per radian


def planck_nu(lam, T):
    """B_nu (W m^-2 Hz^-1 sr^-1) at wavelength lam (m)."""
    nu = C / lam
    x = np.clip(H * nu / (K * T), 1e-9, 700)
    return 2 * H * nu ** 3 / C ** 2 / np.expm1(x)


# ---------------------------------------------------------------- 1. atmospheric opacity
def atmos():
    # approximate altitude (km) at which half of the incoming radiation has been absorbed
    pts = [(1e-15, 22), (1e-13, 26), (1.2e-12, 31), (1.2e-11, 37), (4e-11, 42), (1.2e-10, 47),
           (4e-10, 70), (1.2e-9, 90), (4e-9, 100), (1.2e-8, 112), (3e-8, 125), (6e-8, 130), (9e-8, 120),
           (1.0e-7, 105), (1.15e-7, 88), (1.216e-7, 74), (1.3e-7, 95), (1.5e-7, 105), (1.75e-7, 95),
           (1.9e-7, 62), (2.2e-7, 50), (2.5e-7, 46), (2.8e-7, 38), (2.95e-7, 25), (3.05e-7, 10), (3.2e-7, 0),
           (8.9e-7, 0), (9.4e-7, 2.5), (1.0e-6, 0), (1.35e-6, 0), (1.4e-6, 7), (1.47e-6, 0), (1.8e-6, 0),
           (1.9e-6, 7), (2.0e-6, 0), (2.45e-6, 0), (2.7e-6, 10), (3.0e-6, 3), (3.2e-6, 0), (4.1e-6, 0),
           (4.3e-6, 14), (4.5e-6, 0), (5.2e-6, 0), (6.3e-6, 11), (7.5e-6, 4), (8.0e-6, 0), (9.5e-6, 2),
           (1.3e-5, 0), (1.5e-5, 18), (1.75e-5, 6), (2.0e-5, 3), (2.4e-5, 4), (3.0e-5, 12), (1e-4, 14),
           (3.0e-4, 12), (3.4e-4, 4), (3.7e-4, 7), (4.5e-4, 4), (5.5e-4, 7), (8.5e-4, 3), (1.1e-3, 1.5),
           (2.5e-3, 6), (3.2e-3, 0), (4.8e-3, 0), (5.0e-3, 15), (5.4e-3, 0), (1.25e-2, 0), (1.35e-2, 2),
           (1.5e-2, 0), (15, 0)]
    lx = np.log10([p[0] for p in pts])
    hy = np.array([p[1] for p in pts])
    xs = np.linspace(-15, np.log10(15), 2400)
    ys = np.interp(xs, lx, hy)
    fig, ax = plt.subplots(figsize=(6.8, 3.5))
    ax.fill_between(10 ** xs, 0, ys, color="#C9D7E6", lw=0, zorder=1)
    ax.plot(10 ** xs, ys, color=NAVY, lw=1.1, zorder=2)
    # ionosphere
    ax.add_patch(Rectangle((15, 0), 300 - 15, 160, fc="#E9DDF2", ec="none", zorder=1))
    ax.text(60, 80, "Reflected by\nthe ionosphere\n(> ~20 m)", fontsize=6.0, color=VIOLET, ha="center", va="center",
            rotation=90)
    for h, txt in [(4.5, "High mountain sites (4–5 km)"), (13, "Aircraft (12–14 km)"),
                   (38, "Balloons (30–40 km)"), (100, "Kármán line (100 km)")]:
        ax.axhline(h, color=GREY, ls=(0, (4, 3)), lw=0.7, zorder=3)
        ax.text(12 if h < 50 else 2.5e-15, h + 1.4, txt, fontsize=6.0, color=GREY, va="bottom",
                ha="right" if h < 50 else "left", zorder=4, bbox=dict(fc="white", ec="none", pad=0.3, alpha=0.8))
    bands = [(1e-15, 1e-11, "γ-rays", VIOLET), (1e-11, 1e-8, "X-rays", BLUE), (1e-8, 3.8e-7, "UV", SKY),
             (3.8e-7, 7.5e-7, "Vis", GOLD), (7.5e-7, 3e-4, "Infrared", RED), (3e-4, 1e-3, "Sub-mm", ORANGE),
             (1e-3, 300, "Radio", GREEN)]
    for a, b, t, col in bands:
        ax.add_patch(Rectangle((a, 152), b - a, 8, fc=col, ec="white", lw=0.6, zorder=5, alpha=0.9))
        if t != "Vis":
            ax.text(np.sqrt(a * b), 156, t, fontsize=6.2, color="white", ha="center", va="center", weight="bold",
                    zorder=6)
    for x, y, t in [(5.5e-7, 21, "Optical\nwindow"), (0.1, 60, "Radio window:\nreaches the ground"),
                    (1e-4, 31, "Water vapour\nbands"), (5e-14, 52, "Compton scattering\nand pair production")]:
        ax.text(x, y, t, fontsize=6.0, ha="center", va="center", color=INK, zorder=6)
    ax.annotate("Photoelectric\nabsorption", xy=(3e-10, 60), xytext=(1.5e-12, 92), fontsize=6.0, ha="center",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6), zorder=6)
    ax.annotate("Ozone and O₂", xy=(2.6e-7, 44), xytext=(2e-5, 75), fontsize=6.0, ha="center",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6), zorder=6)
    ax.set_xscale("log")
    ax.set_xlim(1e-15, 300)
    ax.set_ylim(0, 160)
    ticks = [1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1, 100]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["1 fm", "1 pm", "1 nm", "1 µm", "1 mm", "1 m", "100 m"])
    ax.minorticks_off()
    ax.set_xlabel("Wavelength")
    ax.set_ylabel("Altitude where half the\nradiation is absorbed (km)")
    ax.grid(axis="x", visible=False)
    fig.text(0.99, 0.01, "Schematic: approximate half-absorption altitudes after Giacconi et al. (1968) and standard "
             "texts; X/γ values from air attenuation coefficients and the standard atmosphere.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch38_atmos")


# ---------------------------------------------------------------- 2. why IR telescopes must be cold
def thermal():
    lam = np.logspace(np.log10(1e-6), np.log10(1e-3), 600)
    D, eps = 6.5, 0.05
    omega = np.pi * (lam / D) ** 2           # solid angle of a beam of radius lambda/D
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    for T, col, lab, yl in [(290, RED, "Telescope at 290 K\n(Hubble, ground)", 1e-4),
                            (40, BLUE, "40 K (JWST)", 1e-10), (7, VIOLET, "7 K", 1e-10),
                            (2.725, GREY, "Cosmic microwave\nbackground, 2.7 K", 1e-10)]:
        e = 1.0 if T == 2.725 else eps
        f = e * planck_nu(lam, T) * omega / 1e-26  # Jy in the beam
        ax.plot(lam * 1e6, f, color=col, lw=1.6 if T != 2.725 else 1.1, ls="-" if T != 2.725 else "--")
        xl = lam[np.argmax(f > yl)] * 1e6
        ax.text(xl * 1.15, yl, lab, fontsize=6.3, color=col, va="center", ha="left")
    for m, ls, x0 in [(25, "-", 16.5), (30, ":", 13.5)]:
        fs = 3631 * 10 ** (-0.4 * m)
        ax.axhline(fs, color=GREEN, lw=1.0, ls=ls)
        ax.text(x0, fs * 1.6, f"Galaxy AB = {m} ({fs * 1e9:,.1f} nJy)" if m == 30 else
                f"Galaxy AB = {m} ({fs * 1e6:.2f} µJy)", fontsize=6.2, color=GREEN, va="bottom")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1, 1000); ax.set_ylim(1e-12, 1e3)
    ax.set_yticks([1e-12, 1e-9, 1e-6, 1e-3, 1, 1e3]); ax.minorticks_off()
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000])
    ax.set_xticklabels(["1", "2", "5", "10", "20", "50", "100", "200", "500", "1 000"])
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Thermal emission in one\nresolution element (Jy)")
    ax.text(5.3, 1e-11, "MIRI\n5–28 µm", fontsize=6.0, ha="left", va="center", color=NAVY)
    ax.axvspan(5, 28, color=LIGHT, zorder=0)
    fig.text(0.99, 0.01, "Model: emissivity 0.05 × Planck function, integrated over a beam of radius λ/D for a "
             "6.5 m aperture; 1 Jy = 10⁻²⁶ W m⁻² Hz⁻¹.", ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch38_thermal")


# ---------------------------------------------------------------- 3. diffraction: Airy pattern and resolution
def resolution():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.1), gridspec_kw=dict(width_ratios=[1, 1.25]))
    u = np.linspace(1e-6, 3.2, 800)      # theta in units of lambda/D
    x = np.pi * u
    for eps_o, col, lab in [(0.0, NAVY, "Unobstructed"), (0.33, ORANGE, "33 % central obstruction")]:
        I = ((2 * j1(x) - eps_o ** 2 * 2 * j1(eps_o * x)) / x) ** 2 / (1 - eps_o ** 2) ** 2
        a1.plot(u, I, color=col, lw=1.4, label=lab)
    a1.axvline(1.22, color=GREY, ls="--", lw=0.8)
    a1.text(1.3, 0.45, "First dark ring\nθ = 1.22 λ/D", fontsize=6.0, color=GREY)
    sig = 1.03 / 2.355 * 3
    a1.plot(u, np.exp(-u ** 2 / (2 * sig ** 2)) * 0.11, color=GREEN, lw=1.0, ls=":")
    a1.text(1.45, 0.16, "Seeing disc (3× wider, same light)", fontsize=5.9, color=GREEN, ha="left")
    a1.set_xlabel("Angle from centre (λ/D)")
    a1.set_ylabel("Relative intensity")
    a1.set_title("(a) Airy pattern of a circular aperture", fontsize=7.6)
    a1.legend(fontsize=6.0, loc="upper right")
    a1.set_xlim(0, 3.2); a1.set_ylim(0, 1.05)
    ins = a1.inset_axes([0.66, 0.36, 0.3, 0.3])
    g = np.linspace(-3.2, 3.2, 241)
    X, Y = np.meshgrid(g, g)
    r = np.pi * np.hypot(X, Y) + 1e-9
    img = (2 * j1(r) / r) ** 2
    ins.imshow(np.log10(img + 1e-4), cmap="magma", extent=(-3.2, 3.2, -3.2, 3.2))
    ins.set_xticks([]); ins.set_yticks([])
    ins.set_title("log scale", fontsize=5.8, pad=1)
    # (b) resolution vs aperture
    D = np.logspace(-1, 2, 200)
    for lam, col, lab in [(0.15e-6, VIOLET, "0.15 µm (UV)"), (0.5e-6, GOLD, "0.5 µm (visible)"),
                          (2e-6, ORANGE, "2 µm (near-IR)"), (20e-6, RED, "20 µm (mid-IR)"),
                          (500e-6, NAVY, "500 µm (sub-mm)")]:
        a2.plot(D, 1.22 * lam / D * 206264.8, color=col, lw=1.4, label=lab)
    a2.axhspan(0.4, 1.0, color=LIGHT, zorder=0)
    a2.text(11, 0.62, "Ground seeing 0.4–1″", fontsize=6.0, color=NAVY, va="center")
    for d, lam, t, xt, yt in [(2.4, 0.5e-6, "Hubble", 7, 0.006), (6.5, 2e-6, "JWST", 16, 0.16),
                              (0.85, 24e-6, "Spitzer", 0.28, 30), (3.5, 250e-6, "Herschel", 12, 70)]:
        th = 1.22 * lam / d * 206264.8
        a2.plot(d, th, "o", color=INK, ms=3.5, zorder=5)
        a2.annotate(t, (d, th), xytext=(xt, yt), fontsize=6.2, ha="center",
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.5))
    a2.set_xscale("log"); a2.set_yscale("log")
    a2.set_xlim(0.1, 100); a2.set_ylim(0.001, 1000)
    a2.set_xlabel("Aperture diameter D (m)")
    a2.set_ylabel("Diffraction limit 1.22 λ/D (arcsec)")
    a2.set_title("(b) Resolution versus aperture", fontsize=7.6)
    a2.legend(fontsize=5.9, loc="lower left", ncol=1)
    a2.set_xticks([0.1, 1, 10, 100]); a2.set_xticklabels(["0.1", "1", "10", "100"])
    fig.text(0.99, 0.01, "Airy intensity [2J₁(x)/x]², x = πθD/λ; the obstructed curve is normalised to its own peak.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch38_resolution")


# ---------------------------------------------------------------- 4. high-energy optics schematics
def highenergy():
    fig, axs = plt.subplots(1, 3, figsize=(6.9, 2.75), gridspec_kw=dict(width_ratios=[1.45, 1, 1]))
    # (a) Wolter type I: nested paraboloid + hyperboloid shells (cross-section, exaggerated angles)
    a = axs[0]
    a.set_xlim(0, 100); a.set_ylim(-34, 34); a.axis("off")
    F = 96.0
    for r0, col in [(26, NAVY), (20, BLUE), (14, SKY)]:
        # grazing angle alpha such that two reflections deflect by 4 alpha onto focus
        alpha = np.arctan(r0 / (F - 30)) / 4
        # paraboloid segment from x=18 to 30, hyperboloid 30 to 42
        xp = np.array([18, 30]); xh = np.array([30, 42])
        yp = r0 + (30 - xp) * np.tan(alpha)
        yh = r0 - (xh - 30) * np.tan(3 * alpha)
        for s in (1, -1):
            a.plot(xp, s * yp, color=col, lw=2.6, solid_capstyle="butt")
            a.plot(xh, s * yh, color=col, lw=2.6, solid_capstyle="butt")
            # ray: comes in parallel, hits paraboloid at x=24, hyperboloid at x~36, goes to focus
            y1 = r0 + (30 - 24) * np.tan(alpha) - 0.6
            x2 = 36.0
            y2 = y1 - (x2 - 24) * np.tan(2 * alpha)
            a.plot([2, 24], [s * y1, s * y1], color=ORANGE, lw=0.7)
            a.plot([24, x2], [s * y1, s * y2], color=ORANGE, lw=0.7)
            a.plot([x2, F], [s * y2, 0], color=ORANGE, lw=0.7)
    a.plot(F, 0, "o", color=RED, ms=4)
    a.text(F - 1, -4.5, "Focus", fontsize=6.0, ha="center", color=RED)
    a.text(25, 32, "Paraboloids", fontsize=6.0, ha="right", color=NAVY)
    a.text(33, 32, "Hyperboloids", fontsize=6.0, ha="left", color=NAVY)
    a.text(4, -31, "X-rays", fontsize=6.0, color=ORANGE)
    a.text(78, 31, "Nested shells reflect\nat grazing angles\n< 1° (angles\nexaggerated here)", fontsize=5.9,
           ha="center", va="top", color=INK)
    a.set_title("(a) Wolter-I grazing-incidence mirrors", fontsize=7.3)
    # (b) coded mask
    b = axs[1]
    b.set_xlim(0, 60); b.set_ylim(0, 62); b.axis("off")
    pattern = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]
    for i, v in enumerate(pattern):
        if v:
            b.add_patch(Rectangle((6 + i * 3, 46), 3, 2.2, fc=INK, ec="none"))
    b.plot([6, 54], [47.1, 47.1], color=INK, lw=0.4)
    b.add_patch(Rectangle((6, 10), 48, 4, fc=GOLD, ec=NAVY, lw=0.6))
    b.text(30, 6.5, "Position-sensitive detector (CZT)", fontsize=5.9, ha="center")
    b.text(30, 50.5, "Mask of opaque tiles", fontsize=5.9, ha="center")
    for x0, col in [(14, BLUE), (44, RED)]:
        for xi in np.linspace(8, 52, 7):
            b.plot([x0 + (xi - 30) * 0.15 + (xi - 30) * 0.0, xi], [60, 14], color=col, lw=0.45, alpha=0.7)
    b.text(14, 61, "Source A", fontsize=5.9, color=BLUE, ha="center", va="bottom")
    b.text(44, 61, "Source B", fontsize=5.9, color=RED, ha="center", va="bottom")
    b.text(30, 27, "Each source casts a\nshifted shadow of the\nmask; decoding the\npattern gives positions",
           fontsize=5.9, ha="center", bbox=dict(fc="white", ec="none", pad=0.4, alpha=0.9))
    b.set_title("(b) Coded-aperture imaging", fontsize=7.3)
    # (c) pair-conversion telescope
    c = axs[2]
    c.set_xlim(0, 60); c.set_ylim(0, 62); c.axis("off")
    for k in range(7):
        y = 50 - k * 5
        c.plot([10, 50], [y, y], color=SKY, lw=1.6)
        c.plot([10, 50], [y - 0.9, y - 0.9], color=GREY, lw=0.7)
    c.add_patch(Rectangle((10, 6), 40, 9, fc="#F1E3C6", ec=NAVY, lw=0.7))
    c.text(30, 10.5, "CsI calorimeter", fontsize=5.9, ha="center")
    c.plot([30, 30], [62, 45], color=VIOLET, lw=1.0, ls="--")
    c.text(31, 58, "γ (> 20 MeV)", fontsize=5.9, color=VIOLET)
    c.plot([30, 22, 17], [45, 30, 15], color=RED, lw=0.9)
    c.plot([30, 36, 40], [45, 30, 15], color=BLUE, lw=0.9)
    c.text(14, 27, "e⁻", fontsize=6.5, color=RED)
    c.text(42, 27, "e⁺", fontsize=6.5, color=BLUE)
    c.text(52, 37, "W foils +\nSi strip\ntrackers", fontsize=5.9, ha="left", va="center")
    c.set_title("(c) Pair-conversion telescope", fontsize=7.3)
    c.set_xlim(0, 66)
    fig.tight_layout(w_pad=0.6)
    save(fig, "ch38_highenergy")


# ---------------------------------------------------------------- 5. photon budget and SNR
def _snr(V, D, t, lam=550e-9, dl=88.0, eta=0.30, obs=0.33, sky=22.7, dark=0.005, rn=3.0, tsub=1000.):
    N0 = 3.63e-11 / (H * C / lam)                     # photons s-1 m-2 nm-1 at V = 0
    A = np.pi / 4 * D ** 2 * (1 - obs ** 2)
    lamD = lam / D * 206264.8
    r = 1.22 * lamD
    area = np.pi * r ** 2
    npix = area / (lamD / 2) ** 2
    S = 0.8 * N0 * 10 ** (-0.4 * V) * dl * A * eta * t
    B = N0 * 10 ** (-0.4 * sky) * dl * A * eta * area * t
    nread = np.maximum(1, np.ceil(t / tsub))
    noise = np.sqrt(S + B + npix * dark * t + npix * nread * rn ** 2)
    return S / noise, S, B


def snr():
    V = np.linspace(20, 33, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    for D, col, lab in [(0.3, GREEN, "0.3 m (small satellite)"), (2.4, BLUE, "2.4 m (Hubble class)"),
                        (6.5, ORANGE, "6.5 m (JWST class)")]:
        s1, _, _ = _snr(V, D, 3600.)
        s10, _, _ = _snr(V, D, 36000.)
        ax.plot(V, s1, color=col, lw=1.6, label=f"{lab}, 1 h")
        ax.plot(V, s10, color=col, lw=1.1, ls="--")
    ax.plot([], [], color=GREY, ls="--", lw=1.1, label="dashed: 10 h")
    ax.axhline(10, color=GREY, lw=0.8)
    ax.text(20.2, 11.5, "SNR = 10", fontsize=6.2, color=GREY)
    s, S, B = _snr(25.0, 2.4, 3600.)
    ax.plot(25, s, "o", color=NAVY, ms=4, zorder=5)
    ax.text(24.85, s * 0.8, f"SNR ≈ {float(s):.0f}", fontsize=6.2, color=NAVY, va="top", ha="right")
    ax.set_yscale("log")
    ax.set_xlim(20, 33); ax.set_ylim(0.3, 3000)
    ax.set_xlabel("Visual magnitude of a point source (V)")
    ax.set_ylabel("Signal-to-noise ratio")
    ax.legend(fontsize=6.3, loc="upper right")
    fig.text(0.99, 0.01, "Model: V band (550 nm, 88 nm wide), 30 % throughput, 33 % obstruction, diffraction-limited "
             "aperture r = 1.22 λ/D holding 80 % of the light,\nzodiacal sky 22.7 mag/arcsec², Nyquist pixels, "
             "dark 0.005 e⁻/s, read noise 3 e⁻ per 1 000 s sub-exposure.", ha="right", va="bottom", fontsize=5.9,
             color=GREY)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "ch38_snr")


# ---------------------------------------------------------------- 6. sunshield layers
def sunshield():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.0), gridspec_kw=dict(width_ratios=[1.05, 1]))
    a1.set_xlim(0, 100); a1.set_ylim(0, 70); a1.axis("off")
    # five flared layers (side view): closer together at centre, wider at edges
    cols = [ORANGE, GOLD, "#C8B98A", "#A9B6C2", SKY]
    for i in range(5):
        yc = 14 + i * 4.2
        spread = 1.0 + 0.55 * i
        xs = np.array([12, 50, 88])
        ys = np.array([yc + spread * 2.4, yc, yc + spread * 2.4])
        a1.plot(xs, ys, color=cols[i], lw=2.0)
        a1.text(90, ys[-1], f"{i + 1}", fontsize=6.0, va="center", ha="left", color=INK)
    a1.text(97, 32, "Layer", fontsize=5.9, rotation=90, va="center")
    for x in [20, 35, 50, 65, 80]:
        a1.annotate("", xy=(x, 15.5), xytext=(x, 3), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.0))
    a1.text(50, 0.5, "Sunlight ≈ 1 340 W/m² (> 200 kW on the shield)", fontsize=6.0, ha="center", va="bottom",
            color=ORANGE)
    for s in (-1, 1):
        for k in range(3):
            y = 22 + k * 5
            x0 = 50 + s * 30
            a1.annotate("", xy=(x0 + s * 12, y + 2.5), xytext=(x0, y),
                        arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.8))
    a1.text(8, 44, "Heat escapes\nout of the\nopen edges", fontsize=6.0, color=RED, ha="center")
    a1.add_patch(Rectangle((38, 46), 24, 3, fc=GOLD, ec=NAVY, lw=0.6))
    a1.plot([50, 50], [49, 60], color=NAVY, lw=1.0)
    a1.add_patch(Rectangle((47.5, 60), 5, 2, fc=GREY, ec=NAVY, lw=0.5))
    a1.text(66, 53, "Telescope\n< 50 K", fontsize=6.2, ha="left", color=NAVY)
    a1.set_title("(a) Five flared Kapton layers", fontsize=7.6)
    # (b) model temperatures
    T1 = 360.0
    n = np.arange(1, 6)
    g = 0.1                                   # each vented layer passes ~1/10 of the flux it receives
    Tv = T1 * g ** ((n - 1) / 4)
    eps = 0.05
    R = 2 / eps - 1
    T5s = T1 / (1 + 4 * R * eps) ** 0.25
    Ts = (T1 ** 4 - (n - 1) * R * eps * T5s ** 4) ** 0.25
    a2.plot(n, Ts, "s-", color=GREY, lw=1.4, ms=4, label="Sealed stack (no edge loss)")
    a2.plot(n, Tv, "o-", color=BLUE, lw=1.6, ms=4, label="Vented layers (each passes ~10 %)")
    for i in range(5):
        a2.text(n[i] + 0.1 if i else 0.72, Tv[i] + 4 if i else Tv[i] - 30, f"{Tv[i]:.0f} K", fontsize=6.0,
                color=BLUE, va="bottom")
        if i:
            a2.text(n[i], Ts[i] + 9, f"{Ts[i]:.0f} K", fontsize=6.0, color=GREY, ha="center", va="bottom")
    a2.axhspan(0, 50, color=LIGHT, zorder=0)
    a2.text(1.0, 40, "Needed on the telescope side", fontsize=6.0, color=NAVY, va="top")
    a2.set_xticks(n)
    a2.set_xlabel("Layer (1 faces the Sun)")
    a2.set_ylabel("Temperature (K)")
    a2.set_ylim(0, 490); a2.set_xlim(0.7, 5.6)
    a2.legend(fontsize=6.0, loc="upper right")
    a2.set_title("(b) Simple radiative model", fontsize=7.6)
    fig.text(0.99, 0.01, "Model: layer 1 at 360 K; sealed: four gaps with ε = 0.05 faces, layer 5 radiating to space; "
             "vented: flux falls ×10 per layer (reported for JWST). NASA quotes ≈383 K maximum and ≈36 K.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch38_sunshield")


# ---------------------------------------------------------------- 7. pointing jitter vs image quality
def jitter():
    sj = np.linspace(0, 30, 400)           # per-axis rms jitter, mas
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 2.95))
    cases = [(2.4, 0.5e-6, BLUE, "2.4 m at 0.5 µm (Hubble)"), (6.5, 2e-6, ORANGE, "6.5 m at 2 µm (JWST)"),
             (6.0, 0.5e-6, VIOLET, "6 m at 0.5 µm (future UV/optical)")]
    for D, lam, col, lab in cases:
        lamD = lam / D * MAS
        fwhm0 = 1.03 * lamD
        fw = np.sqrt(fwhm0 ** 2 + (2.355 * sj) ** 2)
        a1.plot(sj, fw, color=col, lw=1.5, label=lab)
        strehl = 1 / (1 + (np.pi ** 2 / 2) * (sj / lamD) ** 2)
        a2.plot(sj, strehl, color=col, lw=1.5, label=lab)
    for x, t in [(7, "Hubble requirement\n7 mas"), (1, "JWST achieved\n≈1 mas")]:
        for a in (a1, a2):
            a.axvline(x, color=GREY, ls="--", lw=0.7)
        a2.text(x + 0.6, 0.10 if x == 7 else 0.30, t, fontsize=6.0, color=GREY)
    a1.set_xlabel("Line-of-sight jitter, rms per axis (mas)")
    a1.set_ylabel("Image FWHM (mas)")
    a1.set_title("(a) Blurred image width", fontsize=7.6)
    a1.set_xlim(0, 30); a1.set_ylim(0, 90)
    a1.legend(fontsize=6.0, loc="lower right")
    a2.set_xlabel("Line-of-sight jitter, rms per axis (mas)")
    a2.set_ylabel("Peak intensity / perfect peak")
    a2.set_title("(b) Loss of peak brightness", fontsize=7.6)
    a2.set_xlim(0, 30); a2.set_ylim(0, 1.02)
    fig.text(0.99, 0.01, "Gaussian jitter convolved with the diffraction core: FWHM² = (1.03 λ/D)² + (2.355 σ)²; "
             "peak ratio ≈ 1/[1 + (π²/2)(σD/λ)²].", ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch38_jitter")


# ---------------------------------------------------------------- 8. orbits for telescopes
def orbits():
    fig, axs = plt.subplots(1, 3, figsize=(6.9, 2.9), gridspec_kw=dict(width_ratios=[1, 1.05, 1.1]))
    RE = 6378.
    # (a) Earth-centred, to scale (thousand km)
    a = axs[0]
    a.set_aspect("equal"); a.axis("off")
    a.add_patch(Circle((0, 0), RE / 1e3, fc=EARTH, ec="none", zorder=3))
    a.add_patch(Circle((0, 0), (RE + 470) / 1e3, fc="none", ec=BLUE, lw=0.9, zorder=4))
    rp, ra = RE + 12650, RE + 136200
    sa, e = (rp + ra) / 2, (ra - rp) / (ra + rp)
    th = np.linspace(0, 2 * np.pi, 400)
    r = sa * (1 - e ** 2) / (1 + e * np.cos(th))
    a.plot(r * np.cos(th) / 1e3, r * np.sin(th) / 1e3, color=RED, lw=1.1)
    a.annotate("Chandra\n12 650 ×\n136 200 km", xy=(-140, -20), xytext=(-215, -215), fontsize=5.9, color=RED,
               ha="center", va="center", arrowprops=dict(arrowstyle="-", color=RED, lw=0.5))
    rp2, ra2 = RE + 119000, RE + 364000
    sa2, e2 = (rp2 + ra2) / 2, (ra2 - rp2) / (ra2 + rp2)
    r2 = sa2 * (1 - e2 ** 2) / (1 + e2 * np.cos(th))
    a.plot(r2 * np.cos(th + 2.2) / 1e3, r2 * np.sin(th + 2.2) / 1e3, color=GREEN, lw=1.0)
    a.text(130, 175, "TESS\n(≈14 d)", fontsize=5.9, color=GREEN, ha="center")
    a.add_patch(Circle((0, 0), 384.4, fc="none", ec=GREY, lw=0.7, ls="--"))
    a.text(0, -400, "Moon's orbit", fontsize=5.9, color=GREY, ha="center", va="top")
    a.text(30, 30, "Hubble\n470 km", fontsize=5.9, color=BLUE, ha="left")
    a.set_xlim(-420, 420); a.set_ylim(-440, 420)
    a.set_title("(a) Around the Earth (to scale)", fontsize=7.4)
    # (b) Sun-Earth rotating frame: L2 (schematic halo)
    b = axs[1]
    b.axis("off"); b.set_xlim(-0.6, 2.3); b.set_ylim(-1.3, 1.3)
    b.add_patch(Circle((0, 0), 0.08, fc=EARTH, ec="none"))
    b.text(0, -0.17, "Earth", fontsize=6.0, ha="center", va="top")
    b.add_patch(Circle((0, 0), 0.384, fc="none", ec=GREY, lw=0.6, ls="--"))
    b.plot(1.5, 0, "x", color=INK, ms=5)
    b.text(1.5, -0.12, "L2", fontsize=6.2, ha="center", va="top")
    tt = np.linspace(0, 2 * np.pi, 300)
    b.plot(1.5 + 0.25 * np.cos(tt), 0.75 * np.sin(tt), color=ORANGE, lw=1.2)
    b.annotate("", xy=(1.5, 0.0), xytext=(0.08, 0), arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.6))
    b.text(0.78, 0.06, "1.5 million km", fontsize=5.9, ha="center", va="bottom", color=GREY)
    b.text(1.5, 0.95, "Halo orbit (JWST,\nEuclid, Roman)", fontsize=5.9, ha="center", color=ORANGE)
    b.annotate("", xy=(-0.55, 0), xytext=(-0.25, 0), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.2))
    b.text(-0.42, 0.12, "Sun", fontsize=6.0, ha="center", color=GOLD)
    b.text(0.75, -1.05, "Sun, Earth and Moon all lie\nbehind the sunshield", fontsize=5.9, ha="center", color=INK)
    b.set_title("(b) Sun–Earth L2 (rotating frame)", fontsize=7.4)
    # (c) Earth-trailing drift: period 372.5 d, a = 1.013 AU
    c = axs[2]
    c.set_aspect("equal"); c.axis("off")
    c.plot(0, 0, "o", color=GOLD, ms=7)
    c.text(0.0, -0.13, "Sun", fontsize=6.0, ha="center", va="top")
    c.add_patch(Circle((0, 0), 1.0, fc="none", ec=EARTH, lw=0.6, ls=":"))
    w = 2 * np.pi * (1 - 365.25 / 372.5)       # rad per year lag
    yrs = np.arange(0, 10)
    ang = np.pi / 2 + w * yrs
    c.plot(np.cos(ang), np.sin(ang), "o", color=VIOLET, ms=3)
    for y_ in [1, 4, 9]:
        c.text(1.12 * np.cos(ang[y_]), 1.12 * np.sin(ang[y_]), f"{y_} yr", fontsize=5.8, ha="center",
               va="center", color=VIOLET)
    c.plot(0, 1, "o", color=EARTH, ms=5)
    c.text(0.0, 1.12, "Earth", fontsize=6.0, ha="center", va="bottom", color=EARTH)
    d9 = 2 * np.sin(w * 9.6 / 2)
    c.plot([0, np.cos(ang[9])], [1, np.sin(ang[9])], color=GREY, lw=0.6, ls="--")
    c.text(0.05, 0.25, f"{d9:.1f} AU after\n9.6 years", fontsize=5.9, color=GREY, ha="center")
    c.set_xlim(-1.35, 1.35); c.set_ylim(-0.5, 1.4)
    c.set_title("(c) Earth-trailing (Kepler)", fontsize=7.4)
    fig.text(0.99, 0.01, "(a) to scale; (b) schematic; (c) circular-orbit approximation of Kepler's 372.5-day "
             "heliocentric orbit (lag ≈ 7° per year), shown in a frame rotating with the Earth.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1), w_pad=0.4)
    save(fig, "ch38_orbits")


if __name__ == "__main__":
    fns = [atmos, thermal, resolution, highenergy, snr, sunshield, jitter, orbits]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
