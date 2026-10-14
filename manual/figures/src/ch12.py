import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403


def spectrum():
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(7.4, 4.0), sharex=True, gridspec_kw=dict(height_ratios=[3.2, 0.7]))
    bands = [("γ", 1e-13, 1e-11, VIOLET), ("X-ray", 1e-11, 1e-8, "#9467BD"), ("UV", 1e-8, 3.8e-7, "#5E3C99"),
             ("Vis", 3.8e-7, 7.5e-7, GOLD), ("NIR/SWIR", 7.5e-7, 3e-6, ORANGE),
             ("MWIR/TIR", 3e-6, 1.5e-5, RED), ("Far-IR / sub-mm", 1.5e-5, 1e-3, "#8C564B"),
             ("Microwave", 1e-3, 0.3, BLUE), ("Radio", 0.3, 100, NAVY)]
    for n, a, b, c in bands:
        bx.add_patch(Rectangle((a, 0), b - a, 1, fc=c, ec="white", alpha=0.9))
        bx.text(np.sqrt(a * b), 0.5, n, ha="center", va="center", fontsize=6.3, color="white",
                rotation=0 if b / a > 30 else 90)
    inst = [("Gamma-ray & X-ray telescopes (Fermi, Chandra, XRISM)", 1e-12, 1e-9),
            ("UV spectrometers (ozone, aurora, solar EUV)", 1e-8, 4e-7),
            ("Optical cameras & multispectral imagers", 4e-7, 1.0e-6),
            ("Lidar (355, 532, 1 064 nm)", 3.5e-7, 1.07e-6),
            ("Hyperspectral imagers (0.4–2.5 µm)", 4e-7, 2.5e-6),
            ("Thermal-IR imagers & sounders (3–15 µm)", 3.5e-6, 1.5e-5),
            ("Infrared astronomy (JWST 0.6–28 µm)", 6e-7, 2.8e-5),
            ("Microwave radiometers & sounders (1–200 GHz)", 1.5e-3, 0.3),
            ("Radars: altimeter, scatterometer, SAR (P- to Ka-band)", 7e-3, 0.7),
            ("GNSS (L-band) and radio occultation", 0.19, 0.26)]
    for k, (n, a, b) in enumerate(inst):
        ax.plot([a, b], [k, k], color=NAVY, lw=4, solid_capstyle="butt")
    ax.set_yticks(range(len(inst)))
    ax.set_yticklabels([i[0] for i in inst], fontsize=6.6)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(1e-13, 300)
    ax.grid(axis="y", visible=False)
    bx.set_ylim(0, 1)
    bx.set_yticks([])
    bx.set_xlabel("Wavelength (m)")
    bx.grid(False)
    save(fig, "ch12_spectrum")


def taxonomy():
    fig, ax = canvas(7.4, 3.9, (0, 100), (0, 52))
    box(ax, 38, 44, 24, 6, "Payload instruments", fc=NAVY, ec=NAVY, color="white", fs=8, weight="bold")
    cats = [("Passive remote sensing", 2, ["Optical / IR imagers", "Spectrometers", "Microwave radiometers", "GNSS-RO / reflectometry", "Photometers, polarimeters"], BLUE),
            ("Active remote sensing", 27, ["Synthetic aperture radar", "Altimeters (radar, laser)", "Scatterometers", "Precipitation & cloud radar", "Lidar (aerosol, wind, DIAL)"], ORANGE),
            ("In-situ (fields & particles)", 52, ["Magnetometers", "Plasma & particle detectors", "Electric field & waves", "Dust & mass spectrometers", "Accelerometers, gravity"], GREEN),
            ("Service payloads", 77, ["Comms transponders", "Navigation (clocks, signals)", "Data relay, AIS/ADS-B", "Search & rescue", "Laser comm terminals"], VIOLET)]
    for t, x, items, c in cats:
        box(ax, x, 34, 21, 6, t, fc=c, ec=c, color="white", fs=6.8, weight="bold")
        ax.plot([50, x + 10.5], [44, 40], color=GREY, lw=0.6)
        for k, it in enumerate(items):
            box(ax, x + 1, 26 - k * 5.6, 19, 4.6, it, fc="white", ec=c, fs=6.0, r=0.6)
    save(fig, "ch12_taxonomy")


def telescopes():
    fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.4))
    for a in axs:
        a.set_xlim(0, 10)
        a.set_ylim(0, 6)
        a.set_aspect("equal")
        a.axis("off")
    a = axs[0]
    a.add_patch(Ellipse((2, 3), 0.6, 4, fc="#CFE3F3", ec=NAVY))
    for y in (1.3, 3, 4.7):
        a.plot([0, 2], [y, y], color=ORANGE, lw=0.7)
        a.plot([2, 8.5], [y, 3], color=ORANGE, lw=0.7)
    a.plot(8.5, 3, "o", color=RED, ms=3)
    a.set_title("Refractor (lens)", fontsize=7)
    a = axs[1]
    yy = np.linspace(-2.2, 2.2, 50)
    a.plot(8 - 0.12 * yy ** 2, yy + 3, color=NAVY, lw=2)
    a.plot(3.2 + 0.18 * np.linspace(-0.6, 0.6, 20) ** 2, np.linspace(-0.6, 0.6, 20) + 3, color=NAVY, lw=2)
    for y in (1.2, 4.8):
        a.plot([0, 7.6], [y, y], color=ORANGE, lw=0.7)
        a.plot([7.6, 3.25], [y, 3 + (y - 3) * 0.28], color=ORANGE, lw=0.7)
        a.plot([3.25, 9.5], [3 + (y - 3) * 0.28, 3], color=ORANGE, lw=0.7)
    a.plot(9.5, 3, "o", color=RED, ms=3)
    a.set_title("Cassegrain / Ritchey–Chrétien", fontsize=7)
    a = axs[2]
    a.plot(8 - 0.1 * (yy) ** 2, yy + 3.5, color=NAVY, lw=2)
    a.plot(2 + 0.1 * np.linspace(-0.8, 0.8, 20) ** 2, np.linspace(-0.8, 0.8, 20) + 1.5, color=NAVY, lw=2)
    a.plot(6.5 - 0.05 * np.linspace(-0.9, 0.9, 20) ** 2, np.linspace(-0.9, 0.9, 20) + 0.6, color=NAVY, lw=2)
    for y in (2.4, 4.6):
        a.plot([0, 7.7], [y, y], color=ORANGE, lw=0.7)
        a.plot([7.7, 2.05], [y, 1.5 + (y - 3.5) * 0.3], color=ORANGE, lw=0.7)
        a.plot([2.05, 6.45], [1.5 + (y - 3.5) * 0.3, 0.6 + (y - 3.5) * 0.25], color=ORANGE, lw=0.7)
        a.plot([6.45, 9.5], [0.6 + (y - 3.5) * 0.25, 1.6], color=ORANGE, lw=0.7)
    a.plot(9.5, 1.6, "o", color=RED, ms=3)
    a.set_title("Off-axis three-mirror\nanastigmat (TMA)", fontsize=7)
    a = axs[3]
    a.add_patch(Polygon([(1, 1), (9, 1), (5, 5.5)], fc="none", ec=NAVY))
    for k in range(-3, 4):
        a.add_patch(RegularPolygon((5 + k * 0.95, 3.0 + abs(k) * 0.05), 6, radius=0.5, fc="#D6A84B", ec="#7a5c1b", lw=0.4))
    a.set_title("Segmented primary\n(JWST, future telescopes)", fontsize=7)
    save(fig, "ch12_telescopes")


def detector_qe():
    lam = np.linspace(0.2, 14, 600)
    def band(l, lo, hi, peak, edge=0.08):
        rise = 1 / (1 + np.exp(-(l - lo) / edge))
        fall = 1 / (1 + np.exp((l - hi) / (edge * hi)))
        return peak * rise * fall
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.plot(lam, band(lam, 0.3, 1.0, 0.9, 0.03) * (0.6 + 0.4 * np.exp(-((lam - 0.65) / 0.25) ** 2)), color=BLUE, label="Silicon CCD / CMOS (back-illuminated)")
    ax.plot(lam, band(lam, 0.9, 1.7, 0.85, 0.04), color=GREEN, label="InGaAs (short-wave IR)")
    ax.plot(lam, band(lam, 1.0, 5.3, 0.8, 0.08), color=ORANGE, label="InSb (mid-wave IR, cooled ≈ 80 K)")
    ax.plot(lam, band(lam, 0.8, 2.5, 0.8, 0.06), color=VIOLET, ls="--", label="HgCdTe, cut-off 2.5 µm (JWST NIRCam, hyperspectral)")
    ax.plot(lam, band(lam, 1.0, 12.5, 0.65, 0.12), color=RED, label="HgCdTe long-wave (cut-off ≈ 12.5 µm, ≈ 40–60 K)")
    ax.plot(lam, np.where(lam > 7.5, 0.6 * band(lam, 7.6, 13.8, 1.0, 0.05), 0), color=GREY, label="Uncooled microbolometer (8–14 µm)")
    ax.set_xscale("log")
    ax.set_xlim(0.2, 14)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Quantum efficiency / relative response")
    ax.legend(fontsize=6.4, loc="upper right")
    note(ax, "Schematic responses. Longer cut-off wavelengths mean smaller band gaps and higher dark current, so IR detectors "
             "must be cooled.", xy=(1, -0.16))
    save(fig, "ch12_detector_qe")


def scan_modes():
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.8))
    for a in axs:
        a.set_xlim(0, 10)
        a.set_ylim(0, 10)
        a.set_aspect("equal")
        a.axis("off")
    titles = ["Whiskbroom (cross-track scanning)\nAVHRR, MODIS, Landsat 1–7",
              "Pushbroom (linear arrays)\nLandsat 8/9, Sentinel-2, WorldView", "Framing / step-stare (2-D arrays)\nSkySat, Dove, GEO imagers, JWST"]
    for a, t in zip(axs, titles):
        a.set_title(t, fontsize=6.8)
        satellite(a, 5, 9, 0.35)
        a.add_patch(Polygon([(1, 0.5), (9, 0.5), (9, 4.5), (1, 4.5)], fc="#EEF5EA", ec=GREY, lw=0.5))
        a.annotate("", xy=(5, 6.2), xytext=(5, 8.0), arrowprops=dict(arrowstyle="-|>", color=GREY))
        a.text(5.3, 7, "flight", fontsize=6, color=GREY)
    a = axs[0]
    a.plot([5, 1.5], [8.6, 3], color=ORANGE, lw=0.8)
    a.plot([5, 8.5], [8.6, 3], color=ORANGE, lw=0.8)
    for y in np.arange(1, 4.5, 0.5):
        a.plot([1.3, 8.7], [y, y], color=ORANGE, lw=0.8, alpha=0.7)
    a.add_patch(Rectangle((4.6, 2.8), 0.4, 0.4, fc=RED))
    a = axs[1]
    a.plot([5, 1.3], [8.6, 3], color=BLUE, lw=0.8)
    a.plot([5, 8.7], [8.6, 3], color=BLUE, lw=0.8)
    a.add_patch(Rectangle((1.3, 2.8), 7.4, 0.35, fc=BLUE))
    for y in np.arange(1, 2.8, 0.35):
        a.plot([1.3, 8.7], [y, y], color=BLUE, lw=0.5, alpha=0.5)
    a = axs[2]
    for k, y in enumerate([0.8, 2.5]):
        a.add_patch(Rectangle((2.5, y), 5, 1.6, fc=GREEN, alpha=0.35 + 0.3 * k, ec=GREEN))
    a.plot([5, 2.5], [8.6, 4.1], color=GREEN, lw=0.8)
    a.plot([5, 7.5], [8.6, 4.1], color=GREEN, lw=0.8)
    save(fig, "ch12_scan_modes")


def interfaces():
    fig, ax = canvas(7.2, 3.4, (0, 100), (0, 46))
    box(ax, 4, 6, 34, 34, "", fc="#EEF5FA", ec=NAVY, lw=1.2)
    ax.text(21, 37, "SPACECRAFT BUS", fontsize=8, weight="bold", color=NAVY, ha="center")
    box(ax, 62, 6, 34, 34, "", fc="#FCF3EA", ec=ORANGE, lw=1.2)
    ax.text(79, 37, "PAYLOAD", fontsize=8, weight="bold", color=ORANGE, ha="center")
    rows = [("Mechanical: mounting, alignment, stiffness, launch loads", NAVY),
            ("Electrical power: regulated/unregulated bus, peak & average W, grounding", RED),
            ("Thermal: conductive interface, radiator view, heater control, cryo", ORANGE),
            ("Data & commands: SpaceWire / 1553 / Ethernet, rates, mass memory", BLUE),
            ("Time & position: PPS, GNSS time, attitude quaternions for geolocation", GREEN),
            ("Pointing & stability: accuracy, jitter, agility, keep-out zones", VIOLET),
            ("Contamination & EMC: cleanliness, outgassing, emissions/susceptibility", GREY)]
    for k, (t, c) in enumerate(rows):
        y = 32 - k * 4.0
        arrow(ax, (38, y), (62, y), color=c, style="<|-|>", lw=1.2, ms=8)
        ax.text(50, y + 0.6, t, fontsize=5.6, ha="center", va="bottom", color=c,
                bbox=dict(fc="white", ec="none", pad=0.2, alpha=0.9))
    ax.text(50, 1.5, "All captured in an interface control document (ICD) and verified in integration testing",
            fontsize=6.6, ha="center", color=GREY)
    save(fig, "ch12_interfaces")


def atmos_windows():
    lam = np.logspace(np.log10(0.2), np.log10(20), 1200)
    T = np.ones_like(lam)
    T *= np.where(lam < 0.3, 0.0, 1.0)
    T *= 1 - 0.25 * np.exp(-((lam - 0.3) / 0.03) ** 2)
    for c, w, d in [(0.76, 0.01, 0.6), (0.94, 0.03, 0.6), (1.13, 0.04, 0.7), (1.4, 0.08, 0.98), (1.9, 0.1, 0.99),
                    (2.7, 0.15, 0.99), (4.3, 0.12, 0.99), (6.3, 0.9, 0.99), (9.6, 0.25, 0.5), (15, 2.0, 0.99)]:
        T *= 1 - d * np.exp(-((lam - c) / w) ** 2)
    T *= 0.92 - 0.25 * np.exp(-((lam - 0.35) / 0.15) ** 2)
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.fill_between(lam, 0, T, color=SKY, alpha=0.6)
    ax.plot(lam, T, color=BLUE, lw=1)
    ax.set_xscale("log")
    ax.set_xlim(0.2, 20)
    ax.set_ylim(0, 1)
    for c, t in [(0.55, "visible"), (1.6, "SWIR\nwindows"), (3.8, "MWIR\n3–5 µm"), (11, "LWIR\n8–14 µm")]:
        ax.text(c, 0.92, t, ha="center", fontsize=6.8)
    for c, t in [(1.4, "H₂O"), (1.9, "H₂O"), (2.7, "H₂O/CO₂"), (4.3, "CO₂"), (6.3, "H₂O"), (9.6, "O₃"), (15, "CO₂")]:
        ax.text(c, 0.05, t, ha="center", fontsize=6.2, color=RED)
    ax.set_xlabel("Wavelength (µm)")
    ax.set_ylabel("Atmospheric transmission")
    note(ax, "Schematic vertical transmission of a mid-latitude atmosphere. Imagers use the windows; sounders deliberately "
             "observe within absorption bands to probe different heights.", xy=(1, -0.2))
    save(fig, "ch12_windows")


def calibration():
    fig, ax = canvas(7.2, 2.9, (0, 100), (0, 38))
    steps = [("Pre-launch\nlaboratory", "integrating spheres,\nblackbodies, NIST-\ntraceable standards", BLUE),
             ("Onboard\nreferences", "solar diffusers, lamps,\nblackbodies, deep-space\nviews", GREEN),
             ("Lunar & stellar\ncalibration", "Moon as a stable\nradiometric target;\nstar fields", VIOLET),
             ("Vicarious\ncalibration", "desert sites (RadCalNet),\nDome C, field campaigns,\nbuoys", ORANGE),
             ("Inter-\ncalibration", "simultaneous nadir\noverpasses (GSICS),\nreference sensors", RED)]
    for k, (t, b, c) in enumerate(steps):
        title_box(ax, 1 + k * 19.8, 6, 18.5, 26, t, b, hc=c, ec=c, fc="white", fs=5.9, tfs=6.6)
        if k < 4:
            arrow(ax, (19.5 + k * 19.8, 19), (20.9 + k * 19.8, 19), color=GREY, ms=6)
    ax.text(50, 1.5, "Goal: traceability to SI units with known uncertainty — e.g., ≤ 3 % reflectance (Landsat, Sentinel-2), "
            "≤ 0.1 K (sea-surface temperature)", fontsize=6.4, ha="center", color=GREY)
    save(fig, "ch12_calibration")


def geo_power():
    data = [(1965, 0.04, "Early Bird"), (1975, 0.5, "Intelsat IV"), (1985, 1.5, "Intelsat V"), (1990, 3, "HS-601"),
            (1997, 8, "Intelsat 801 / HS-702"), (2005, 15, "Boeing 702"), (2012, 18, "ViaSat-1"), (2019, 22, "ViaSat-2"),
            (2023, 30, "ViaSat-3 (≈ 30 kW)"), (2026, 25, "Typical large HTS")]
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.semilogy([d[0] for d in data], [d[1] for d in data], "-o", color=ORANGE, ms=4)
    for x, y, t in data:
        ax.text(x + 0.8, y * 1.2, t, fontsize=6.4)
    ax.set_xlabel("Year")
    ax.set_ylabel("Spacecraft power (kW, log)")
    ax.set_xlim(1962, 2034)
    note(ax, "Approximate end-of-life power of representative geostationary communications satellites.", xy=(1, -0.18))
    save(fig, "ch12_geo_power")


if __name__ == "__main__":
    from matplotlib.patches import RegularPolygon  # noqa: F401
    globals()["RegularPolygon"] = RegularPolygon
    spectrum(); taxonomy(); telescopes(); detector_qe(); scan_modes(); interfaces(); atmos_windows(); calibration()
    geo_power()
