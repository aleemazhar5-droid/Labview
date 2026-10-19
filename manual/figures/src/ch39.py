"""Figures for Chapter 39: Great Observatories and Deep-Space Telescopes."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge  # noqa: F401
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.integrate import quad

# ---------------------------------------------------------------------------------------------
# Common data
# ---------------------------------------------------------------------------------------------
HC = 1.23984e-6          # h c in eV m
BAND_COL = {"gamma": VIOLET, "xray": BLUE, "opt": GREEN, "ir": RED, "mw": ORANGE, "gw": GREY}
BAND_NAME = {"gamma": "Gamma ray", "xray": "X-ray", "opt": "UV / visible / near-IR", "ir": "Infrared",
             "mw": "Microwave / radio", "gw": "Gravitational waves"}


def kev(e):
    """Photon energy in keV -> wavelength in m."""
    return HC / (e * 1e3)


def ghz(f):
    return 2.99792458e8 / (f * 1e9)


UM = 1e-6

# ---------------------------------------------------------------------------------------------
# 1. Electromagnetic-spectrum coverage
# ---------------------------------------------------------------------------------------------
def emcoverage():
    # (name, band, [(lam_min, lam_max), ...], planned)
    rows = [
        ("Fermi LAT", "gamma", [(kev(3e8), kev(2e4))], False),
        ("Fermi GBM", "gamma", [(kev(4e4), kev(8))], False),
        ("Compton (CGRO)", "gamma", [(kev(3e7), kev(20))], False),
        ("Swift BAT / XRT / UVOT", "gamma", [(kev(150), kev(15)), (kev(10), kev(0.2)), (0.17 * UM, 0.60 * UM)], False),
        ("NuSTAR", "xray", [(kev(79), kev(3))], False),
        ("Chandra", "xray", [(kev(10), kev(0.1))], False),
        ("XMM-Newton", "xray", [(kev(15), kev(0.15))], False),
        ("eROSITA", "xray", [(kev(10), kev(0.2))], False),
        ("IXPE", "xray", [(kev(8), kev(2))], False),
        ("XRISM (Resolve)", "xray", [(kev(12), kev(1.7))], False),
        ("Einstein Probe", "xray", [(kev(10), kev(0.3))], False),
        ("NewAthena", "xray", [(kev(12), kev(0.2))], True),
        ("Hubble", "opt", [(0.115 * UM, 1.7 * UM)], False),
        ("Gaia", "opt", [(0.33 * UM, 1.05 * UM)], False),
        ("Kepler", "opt", [(0.42 * UM, 0.90 * UM)], False),
        ("TESS", "opt", [(0.60 * UM, 1.00 * UM)], False),
        ("Euclid", "opt", [(0.55 * UM, 2.0 * UM)], False),
        ("Roman", "opt", [(0.48 * UM, 2.3 * UM)], False),
        ("PLATO", "opt", [(0.50 * UM, 1.0 * UM)], True),
        ("JWST", "ir", [(0.6 * UM, 28.5 * UM)], False),
        ("SPHEREx", "ir", [(0.75 * UM, 5.0 * UM)], False),
        ("WISE", "ir", [(3.4 * UM, 22 * UM)], False),
        ("Spitzer", "ir", [(3.6 * UM, 160 * UM)], False),
        ("Herschel", "ir", [(55 * UM, 672 * UM)], False),
        ("PRIMA", "ir", [(24 * UM, 235 * UM)], True),
        ("COBE", "mw", [(1.25 * UM, 240 * UM), (100 * UM, 10e-3)], False),
        ("WMAP", "mw", [(ghz(94), ghz(23))], False),
        ("Planck", "mw", [(ghz(857), ghz(30))], False),
        ("RadioAstron", "mw", [(0.0119, 0.92)], False),
    ]
    fig = plt.figure(figsize=(7.0, 6.3))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 11.5], hspace=0.04)
    axs = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1], sharex=axs)
    xmin, xmax = 1e-18, 30.0

    # --- atmospheric transparency strip (schematic)
    segs = [(xmin, 0.3 * UM, 0), (0.3 * UM, 1.0 * UM, 2), (1.0 * UM, 30 * UM, 1), (30 * UM, 300 * UM, 0),
            (300 * UM, 1e-2, 1), (1e-2, 15.0, 2), (15.0, xmax, 0)]
    cols = {0: "#3E4851", 1: "#9AA7B2", 2: "#E8EEF3"}
    for a, b, k in segs:
        axs.add_patch(Rectangle((a, 0), b - a, 1, fc=cols[k], ec="white", lw=0.8))
    axs.set_ylim(0, 1)
    axs.set_yticks([])
    axs.grid(False)
    for s in ["left", "bottom"]:
        axs.spines[s].set_visible(False)
    axs.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    axs.text(np.sqrt(xmin * 0.3 * UM), 0.5, "Absorbed by the atmosphere: observe from space", ha="center", va="center",
             fontsize=6.6, color="white")
    axs.text(3e-1, 0.5, "radio window", ha="center", va="center", fontsize=6.4, color=INK)
    axs.text(0.0, 1.25, "Earth's atmosphere (schematic): dark = opaque, mid = partial windows, light = transparent",
             transform=axs.transAxes, fontsize=6.6, color=GREY, ha="left", va="bottom")

    # --- mission bars
    n = len(rows)
    for i, (name, band, ranges, planned) in enumerate(rows):
        y = n - 1 - i
        c = BAND_COL[band]
        for lo, hi in ranges:
            if planned:
                ax.add_patch(Rectangle((lo, y - 0.32), hi - lo, 0.64, fc="white", ec=c, lw=1.0, hatch="////"))
            else:
                ax.add_patch(Rectangle((lo, y - 0.32), hi - lo, 0.64, fc=c, ec="white", lw=0.6))
    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] + ("  (planned)" if r[3] else "") for r in rows][::-1], fontsize=7.0)
    ax.set_ylim(-1.5, n + 0.5)
    ax.set_xscale("log")
    ax.set_xlim(xmin, xmax)
    ax.set_xlabel("Wavelength (m)")
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    # band names along the top of the plot
    regions = [(1e-18, 1e-11, "gamma rays"), (1e-11, 1e-8, "X-rays"), (1e-8, 3.8e-7, "UV"),
               (7.5e-7, 1e-3, "infrared"), (1e-3, 1e-1, "microwave"), (1e-1, 30, "radio")]
    for a, b, t in regions:
        ax.axvline(b, color="#C9D2DA", lw=0.6, zorder=0)
        ax.text(np.sqrt(a * b), n - 0.15, t, ha="center", va="center", fontsize=6.6, color=GREY, style="italic")
    # energy markers
    for e, t in [(1e9, "1 GeV"), (1e6, "1 MeV"), (1e3, "1 keV"), (1.0, "1 eV")]:
        lam = HC / e
        ax.plot([lam, lam], [-1.5, -0.95], color=GREY, lw=0.7)
        ax.text(lam * 1.4, -1.2, t, fontsize=6.2, color=GREY, va="center", ha="left")
    handles = [Patch(fc=BAND_COL[b], ec="none", label=BAND_NAME[b]) for b in ["gamma", "xray", "opt", "ir", "mw"]]
    handles.append(Patch(fc="white", ec=GREY, hatch="////", label="planned"))
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.0, 0.06), fontsize=6.6, ncol=2,
              frameon=True, facecolor="white", edgecolor="#D5DDE5")
    fig.text(0.99, 0.005, "Ranges are the nominal bands of each mission's instruments (energy E = hc/λ). Hubble: current "
             "instruments; XRISM Resolve above 1.7 keV while its gate valve stays closed.", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.subplots_adjust(left=0.22, right=0.98, top=0.95, bottom=0.10)
    save(fig, "ch39_emcoverage")


# ---------------------------------------------------------------------------------------------
# 2. Gantt chart of observatories
# ---------------------------------------------------------------------------------------------
NOW = 2026.8
GANTT = [
    # name, band, start, end (None = operating), planned
    ("COBE", "mw", 1989.9, 1993.97, False),
    ("Hubble", "opt", 1990.31, None, False),
    ("ROSAT", "xray", 1990.42, 1999.12, False),
    ("Compton (CGRO)", "gamma", 1991.26, 2000.42, False),
    ("ISO", "ir", 1995.87, 1998.35, False),
    ("Chandra", "xray", 1999.56, None, False),
    ("XMM-Newton", "xray", 1999.95, None, False),
    ("WMAP", "mw", 2001.5, 2010.7, False),
    ("Spitzer", "ir", 2003.65, 2020.08, False),
    ("Swift", "gamma", 2004.89, NOW, False),
    ("Fermi", "gamma", 2008.44, None, False),
    ("Herschel", "ir", 2009.37, 2013.33, False),
    ("Planck", "mw", 2009.37, 2013.81, False),
    ("Kepler / K2", "opt", 2009.18, 2018.83, False),
    ("WISE / NEOWISE", "ir", 2009.95, 2024.6, False),
    ("RadioAstron", "mw", 2011.55, 2019.08, False),
    ("NuSTAR", "xray", 2012.45, None, False),
    ("Gaia", "opt", 2013.97, 2025.04, False),
    ("TESS", "opt", 2018.3, None, False),
    ("eROSITA", "xray", 2019.53, 2022.15, False),
    ("CHEOPS", "opt", 2019.97, None, False),
    ("IXPE", "xray", 2021.94, None, False),
    ("JWST", "ir", 2021.98, None, False),
    ("Euclid", "opt", 2023.5, None, False),
    ("XRISM", "xray", 2023.68, None, False),
    ("Einstein Probe", "xray", 2024.02, None, False),
    ("SVOM", "gamma", 2024.47, None, False),
    ("SPHEREx", "ir", 2025.2, None, False),
    ("Roman", "opt", 2026.66, None, False),
    ("PLATO", "opt", 2027.05, 2031.0, True),
    ("Xuntian (CSST)", "opt", 2027.5, 2037.0, True),
    ("Ariel", "ir", 2029.5, 2033.5, True),
    ("PRIMA", "ir", 2033.0, 2038.0, True),
    ("LISA", "gw", 2035.0, 2040.0, True),
    ("NewAthena", "xray", 2037.0, 2040.0, True),
]


def gantt():
    fig, ax = plt.subplots(figsize=(7.0, 5.9))
    n = len(GANTT)
    for i, (name, band, s, e, planned) in enumerate(GANTT):
        y = n - 1 - i
        c = BAND_COL[band]
        if planned:
            ax.add_patch(Rectangle((s, y - 0.33), e - s, 0.66, fc="white", ec=c, lw=1.0, hatch="////"))
            ax.text(s - 0.3, y, name, ha="right", va="center", fontsize=6.7, color=INK)
            continue
        end = NOW if e is None else e
        ax.add_patch(Rectangle((s, y - 0.33), end - s, 0.66, fc=c, ec="white", lw=0.5))
        if e is None:
            ax.annotate("", xy=(end + 1.6, y), xytext=(end, y),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=1.0, mutation_scale=7))
        if s < 2001:
            ax.text(s - 0.3, y, name, ha="right", va="center", fontsize=6.7, color=INK)
        else:
            ax.text(s - 0.3, y, name, ha="right", va="center", fontsize=6.7, color=INK)
    nplan = sum(1 for g in GANTT if g[4])
    ax.plot([NOW, NOW], [nplan - 0.5, n + 0.4], color=RED, lw=1.0, ls="--")
    ax.text(NOW + 0.3, n + 0.1, "Oct 2026", color=RED, fontsize=7, va="bottom", ha="left")
    ax.set_xlim(1981, 2041)
    ax.set_ylim(-0.8, n + 1.0)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.grid(axis="y", visible=False)
    ax.set_xticks(range(1990, 2041, 5))
    ax.set_xlabel("Year")
    handles = [Patch(fc=BAND_COL[b], ec="none", label=BAND_NAME[b]) for b in ["gamma", "xray", "opt", "ir", "mw", "gw"]]
    handles.append(Patch(fc="white", ec=GREY, hatch="////", label="planned (launch target)"))
    handles.append(Line2D([0], [0], color=GREY, lw=1.0, marker=">", markersize=4, label="still operating"))
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.0, 0.0), fontsize=6.6, ncol=1, frameon=True,
              facecolor="white", edgecolor="#D5DDE5")
    fig.text(0.99, 0.005, "Bars run from launch to end of science operations. Planned bars start at the launch target "
             "(Oct 2026) and show nominal mission length; Swift was expected to re-enter in late 2026.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, "ch39_gantt")


# ---------------------------------------------------------------------------------------------
# 3. Aperture vs launch year and survey etendue
# ---------------------------------------------------------------------------------------------
def apertures():
    data = [  # name, year, aperture (m), band, planned, label x, label y, ha
        ("IRAS", 1983.1, 0.57, "ir", False, 1984.0, 0.57, "left"),
        ("Hubble", 1990.3, 2.4, "opt", False, 1991.2, 2.4, "left"),
        ("ISO", 1995.9, 0.60, "ir", False, 1996.8, 0.60, "left"),
        ("Chandra*", 1999.6, 1.2, "xray", False, 1998.7, 1.2, "right"),
        ("Spitzer", 2003.6, 0.85, "ir", False, 2002.7, 0.85, "right"),
        ("Kepler", 2009.2, 0.95, "opt", False, 2010.2, 0.95, "left"),
        ("Herschel", 2009.4, 3.5, "ir", False, 2008.4, 3.5, "right"),
        ("Planck", 2009.4, 1.5, "mw", False, 2008.4, 1.5, "right"),
        ("WISE", 2009.95, 0.40, "ir", False, 2010.9, 0.40, "left"),
        ("Gaia", 2013.97, 1.45, "opt", False, 2014.9, 1.45, "left"),
        ("TESS", 2018.3, 0.105, "opt", False, 2017.4, 0.105, "right"),
        ("CHEOPS", 2019.97, 0.32, "opt", False, 2020.9, 0.32, "left"),
        ("JWST", 2021.98, 6.5, "ir", False, 2021.0, 6.5, "right"),
        ("Euclid", 2023.5, 1.2, "opt", False, 2023.5, 0.97, "center"),
        ("SPHEREx", 2025.2, 0.20, "ir", False, 2026.1, 0.20, "left"),
        ("Roman", 2026.66, 2.4, "opt", False, 2025.8, 2.4, "right"),
        ("Xuntian", 2027.5, 2.0, "opt", True, 2028.2, 2.65, "left"),
        ("PLATO (26 cameras)", 2027.05, 0.12, "opt", True, 2028.0, 0.12, "left"),
        ("Ariel", 2029.5, 1.1, "ir", True, 2030.4, 1.1, "left"),
        ("PRIMA", 2033.0, 1.8, "ir", True, 2033.9, 1.8, "left"),
        ("HWO concept", 2041.0, 6.0, "opt", True, 2040.0, 6.0, "right"),
    ]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.5), gridspec_kw=dict(width_ratios=[1.5, 1.0]))
    for name, yr, d, band, planned, lx, ly, ha in data:
        c = BAND_COL[band]
        if planned:
            a1.scatter(yr, d, s=30, facecolor="white", edgecolor=c, linewidth=1.2, zorder=3)
        else:
            a1.scatter(yr, d, s=30, color=c, edgecolor="white", linewidth=0.8, zorder=3)
        a1.text(lx, ly, name, fontsize=6.3, va="top" if ha == "center" else "center", ha=ha, color=INK)
    a1.set_yscale("log")
    a1.set_ylim(0.07, 40)
    a1.set_xlim(1980, 2046)
    a1.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20])
    a1.set_yticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10", "20"])
    a1.set_ylabel("Primary mirror diameter (m)")
    a1.set_xlabel("Launch year")
    a1.set_title("(a) Aperture of space telescopes", loc="left", fontsize=8.6)
    handles = [Line2D([0], [0], marker="o", ls="", color=BAND_COL[b], markersize=5, label=BAND_NAME[b])
               for b in ["xray", "opt", "ir", "mw"]]
    handles.append(Line2D([0], [0], marker="o", ls="", markerfacecolor="white", markeredgecolor=GREY, markersize=5,
                          label="planned / concept"))
    a1.legend(handles=handles, loc="upper left", fontsize=6.1, ncol=2, columnspacing=0.8, handletextpad=0.3)

    # etendue A*Omega of main survey camera
    et = [  # name, aperture m, FoV deg2, kind
        ("Hubble ACS/WFC", 2.4, 0.00315, "opt"),
        ("JWST NIRCam", 6.5, 0.0027, "ir"),
        ("Spitzer IRAC", 0.85, 0.0075, "ir"),
        ("Euclid VIS", 1.2, 0.54, "opt"),
        ("Roman WFI", 2.4, 0.281, "opt"),
        ("SPHEREx", 0.20, 39.6, "ir"),
        ("Xuntian (planned)", 2.0, 1.1, "opt"),
        ("Kepler", 0.95, 105.0, "opt"),
        ("TESS (4 cameras)", None, 2304.0, "opt"),
    ]
    names, vals, cols = [], [], []
    for nme, d, fov, k in et:
        area = np.pi * 0.0525 ** 2 if d is None else np.pi * (d / 2) ** 2   # TESS: each camera sees 1/4 of the field
        if nme.startswith("JWST"):
            area = 25.4
        names.append(nme)
        vals.append(area * fov)
        cols.append(BAND_COL[k])
    order = np.argsort(vals)
    y = np.arange(len(vals))
    a2.barh(y, [vals[i] for i in order], color=[cols[i] for i in order], height=0.62, edgecolor="white")
    a2.set_yticks(y)
    a2.set_yticklabels([names[i] for i in order], fontsize=6.6)
    a2.set_xscale("log")
    a2.set_xlim(3e-3, 3e3)
    for yy, i in zip(y, order):
        v = vals[i]
        a2.text(v * 1.25, yy, f"{v:.3g}", va="center", fontsize=6.2, color=INK)
    a2.set_xlabel("Étendue A·Ω (m² deg²)")
    a2.grid(axis="y", visible=False)
    a2.tick_params(axis="y", length=0)
    a2.set_title("(b) Survey power: area × field of view", loc="left", fontsize=8.6)
    fig.text(0.99, 0.005, "*Chandra: outer diameter of nested grazing-incidence mirrors. HWO: ~6 m concept, 2040s. "
             "Étendue uses geometric aperture area (JWST 25.4 m²) and the field of the main survey camera(s).",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch39_apertures")


# ---------------------------------------------------------------------------------------------
# 4. Exoplanet discoveries per year by method (NASA Exoplanet Archive, pscomppars, 19 Oct 2026)
# ---------------------------------------------------------------------------------------------
EXO = {1992: {'Pulsar Timing': 2}, 1994: {'Pulsar Timing': 1}, 1995: {'Radial Velocity': 1},
       1996: {'Radial Velocity': 6}, 1997: {'Radial Velocity': 1}, 1998: {'Radial Velocity': 6},
       1999: {'Radial Velocity': 13}, 2000: {'Radial Velocity': 16}, 2001: {'Radial Velocity': 12},
       2002: {'Radial Velocity': 28, 'Transit': 1}, 2003: {'Pulsar Timing': 1, 'Radial Velocity': 21},
       2004: {'Imaging': 3, 'Microlensing': 1, 'Radial Velocity': 18, 'Transit': 5},
       2005: {'Imaging': 1, 'Microlensing': 2, 'Radial Velocity': 33},
       2006: {'Imaging': 5, 'Microlensing': 1, 'Radial Velocity': 21, 'Transit': 5},
       2007: {'Imaging': 1, 'Pulsation Timing Variations': 1, 'Radial Velocity': 34, 'Transit': 16},
       2008: {'Imaging': 7, 'Microlensing': 4, 'Radial Velocity': 36, 'Transit': 15},
       2009: {'Eclipse Timing Variations': 1, 'Microlensing': 2, 'Radial Velocity': 66, 'Transit': 18},
       2010: {'Eclipse Timing Variations': 2, 'Imaging': 6, 'Microlensing': 2, 'Radial Velocity': 37, 'Transit': 46},
       2011: {'Eclipse Timing Variations': 5, 'Imaging': 2, 'Microlensing': 1, 'Orbital Brightness Modulation': 2,
              'Pulsar Timing': 1, 'Radial Velocity': 49, 'Transit Timing Variations': 1, 'Transit': 80},
       2012: {'Eclipse Timing Variations': 1, 'Imaging': 2, 'Microlensing': 7, 'Radial Velocity': 39,
              'Transit Timing Variations': 1, 'Transit': 94},
       2013: {'Astrometry': 1, 'Imaging': 7, 'Microlensing': 5, 'Orbital Brightness Modulation': 1,
              'Radial Velocity': 34, 'Transit Timing Variations': 1, 'Transit': 79},
       2014: {'Imaging': 2, 'Microlensing': 6, 'Orbital Brightness Modulation': 3, 'Radial Velocity': 48,
              'Transit Timing Variations': 3, 'Transit': 810},
       2015: {'Eclipse Timing Variations': 1, 'Imaging': 5, 'Microlensing': 4, 'Radial Velocity': 46, 'Transit': 99},
       2016: {'Imaging': 2, 'Microlensing': 10, 'Pulsation Timing Variations': 1, 'Radial Velocity': 58,
              'Transit Timing Variations': 1, 'Transit': 1432},
       2017: {'Eclipse Timing Variations': 1, 'Imaging': 3, 'Microlensing': 10, 'Pulsar Timing': 2,
              'Radial Velocity': 48, 'Transit Timing Variations': 1, 'Transit': 87},
       2018: {'Eclipse Timing Variations': 1, 'Imaging': 3, 'Microlensing': 21, 'Radial Velocity': 38,
              'Transit Timing Variations': 1, 'Transit': 244},
       2019: {'Disk Kinematics': 1, 'Eclipse Timing Variations': 2, 'Imaging': 4, 'Microlensing': 14,
              'Radial Velocity': 65, 'Transit Timing Variations': 1, 'Transit': 107},
       2020: {'Imaging': 3, 'Microlensing': 20, 'Radial Velocity': 46, 'Transit Timing Variations': 1, 'Transit': 164},
       2021: {'Imaging': 5, 'Microlensing': 21, 'Orbital Brightness Modulation': 3, 'Radial Velocity': 77,
              'Transit Timing Variations': 1, 'Transit': 457},
       2022: {'Astrometry': 1, 'Eclipse Timing Variations': 2, 'Imaging': 4, 'Microlensing': 51,
              'Radial Velocity': 115, 'Transit Timing Variations': 2, 'Transit': 192},
       2023: {'Astrometry': 1, 'Eclipse Timing Variations': 1, 'Imaging': 7, 'Microlensing': 30,
              'Radial Velocity': 56, 'Transit Timing Variations': 3, 'Transit': 225},
       2024: {'Imaging': 11, 'Microlensing': 28, 'Pulsar Timing': 1, 'Radial Velocity': 29,
              'Transit Timing Variations': 4, 'Transit': 187},
       2025: {'Astrometry': 3, 'Imaging': 8, 'Microlensing': 23, 'Radial Velocity': 62,
              'Transit Timing Variations': 6, 'Transit': 144},
       2026: {'Imaging': 7, 'Microlensing': 29, 'Radial Velocity': 45, 'Transit Timing Variations': 2, 'Transit': 278}}


def exoplanets():
    years = np.arange(1992, 2027)
    groups = [("Transit", BLUE, ["Transit"]), ("Radial velocity", ORANGE, ["Radial Velocity"]),
              ("Microlensing", GREEN, ["Microlensing"]), ("Direct imaging", VIOLET, ["Imaging"])]
    known = sum((g[2] for g in groups), [])
    series = {}
    for label_, col, keys in groups:
        series[label_] = np.array([sum(EXO.get(y, {}).get(k, 0) for k in keys) for y in years])
    series["Other"] = np.array([sum(v for k, v in EXO.get(y, {}).items() if k not in known) for y in years])
    colors = {g[0]: g[1] for g in groups}
    colors["Other"] = GREY
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.2), gridspec_kw=dict(width_ratios=[1.35, 1.0]))
    bottom = np.zeros(len(years))
    for k in ["Transit", "Radial velocity", "Microlensing", "Direct imaging", "Other"]:
        a1.bar(years, series[k], bottom=bottom, color=colors[k], width=0.78, label=k, edgecolor="white", lw=0.3)
        bottom += series[k]
    a1.set_xlim(1991, 2027)
    a1.set_ylim(0, 1650)
    a1.set_ylabel("Planets confirmed per discovery year")
    a1.grid(axis="x", visible=False)
    a1.annotate("Kepler bulk\nvalidation (2014)", xy=(2014, 880), xytext=(2004.5, 860), fontsize=6.4,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7), color=INK)
    a1.annotate("Kepler statistical\nvalidation (2016)", xy=(2016.4, 1480), xytext=(2018.0, 1330), fontsize=6.4,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7), color=INK)
    a1.annotate("TESS era", xy=(2021, 570), xytext=(2017.2, 760), fontsize=6.4,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7), color=INK)
    a1.text(2026, bottom[-1] + 25, "2026\n(to Oct)", fontsize=5.9, ha="center", va="bottom", color=GREY)
    a1.legend(loc="upper left", fontsize=6.4)
    a1.set_title("(a) Discoveries per year by method", loc="left", fontsize=8.6)
    # cumulative
    tot = np.zeros(len(years))
    for k in ["Transit", "Radial velocity", "Microlensing", "Direct imaging", "Other"]:
        cum = np.cumsum(series[k])
        tot += series[k]
        a2.plot(years, cum, color=colors[k], lw=1.6)
        nudge = {"Transit": 0.86, "Direct imaging": 1.2, "Other": 0.78}.get(k, 1.0)
        a2.text(2026.6, cum[-1] * nudge, f"{k} {cum[-1]:,}".replace(",", " "), fontsize=6.2, va="center", color=INK)
    ct = np.cumsum(tot)
    a2.plot(years, ct, color=NAVY, lw=2.0)
    a2.text(2026.6, ct[-1] * 1.18, f"All {int(ct[-1]):,}".replace(",", " "), fontsize=6.4, va="center", color=INK,
            weight="bold")
    a2.set_yscale("log")
    a2.set_ylim(1, 1.5e4)
    a2.set_xlim(1992, 2039)
    a2.set_xticks([1995, 2005, 2015, 2025])
    a2.set_ylabel("Cumulative confirmed planets")
    a2.set_title("(b) Cumulative total", loc="left", fontsize=8.6)
    fig.text(0.99, 0.005, "Data: NASA Exoplanet Archive, Planetary Systems Composite table, queried 19 Oct 2026 "
             "(6 451 planets). 'Other' = timing, astrometry, brightness modulation, disk kinematics.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch39_exoplanets")


# ---------------------------------------------------------------------------------------------
# 5. Cosmology: look-back time and distances (flat LCDM, H0 = 67.7, Om = 0.31, radiation included)
# ---------------------------------------------------------------------------------------------
H0, OM = 67.7, 0.31
OR = 4.15e-5 / (H0 / 100) ** 2          # photons + three massless neutrino species
OL = 1 - OM - OR
TH = 3.0856775814913673e19 / H0 / 3.15576e16   # Hubble time in Gyr
DH = 299792.458 / H0                          # Hubble distance in Mpc
GLY_PER_MPC = 3.26156e-3


def Ez(z):
    return np.sqrt(OR * (1 + z) ** 4 + OM * (1 + z) ** 3 + OL)


def age(z):
    return TH * quad(lambda x: 1 / ((1 + x) * Ez(x)), z, np.inf, limit=400)[0]


def lookback(z):
    return TH * quad(lambda x: 1 / ((1 + x) * Ez(x)), 0, z, limit=400)[0]


def dcom(z):
    return DH * quad(lambda x: 1 / Ez(x), 0, z, limit=400)[0]


def lookbackfig():
    zz = np.logspace(-2, np.log10(1500), 300)
    ages = np.array([age(z) for z in zz])
    lbs = np.array([lookback(z) for z in zz])
    dc = np.array([dcom(z) for z in zz]) * GLY_PER_MPC
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.3))
    x = 1 + zz
    zl = np.linspace(0, 20, 400)
    a1.plot(zl, [lookback(z) for z in zl], color=BLUE, label="Look-back time (light-travel time)")
    a1.plot(zl, [age(z) for z in zl], color=ORANGE, label="Age of the Universe when light left")
    for z, t in [(6.0, "z = 6"), (10.6, "GN-z11"), (14.44, "MoM-z14")]:
        a1.axvline(z, color="#C9D2DA", lw=0.8, ls="--", zorder=0)
        a1.text(z, 15.0, t, fontsize=6.3, ha="center", va="center", color=INK)
    z14 = 14.44
    a1.scatter([z14, z14], [lookback(z14), age(z14)], color=INK, s=12, zorder=4)
    a1.annotate(f"{lookback(z14):.2f} Gyr ago", xy=(z14, lookback(z14)), xytext=(15.6, 11.4), fontsize=6.3,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6), color=INK)
    a1.annotate(f"{age(z14) * 1000:.0f} Myr after\nthe Big Bang", xy=(z14, age(z14)), xytext=(15.6, 2.4),
                fontsize=6.3, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6), color=INK)
    a1.annotate(f"z = 1: {lookback(1):.1f} Gyr ago,\nUniverse {age(1):.1f} Gyr old", xy=(1.0, lookback(1)),
                xytext=(2.4, 6.3), fontsize=6.3, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6), color=INK)
    a1.text(19.8, 4.7, f"CMB (z ≈ 1100): {age(1100) * 1e3:.2f} Myr", fontsize=6.0, ha="right", color=GREY)
    a1.set_xlim(0, 20)
    a1.set_ylim(0, 15.8)
    a1.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
    a1.set_xlabel("Redshift z")
    a1.set_ylabel("Time (billion years)")
    a1.legend(loc="center right", fontsize=6.3, bbox_to_anchor=(1.0, 0.56))
    a1.set_title("(a) Look-back time and cosmic age", loc="left", fontsize=8.6)

    lt = lbs   # light-travel distance in Gly equals look-back time in Gyr
    da = dc / (1 + zz)
    dl = dc * (1 + zz)
    a2.plot(x, dc, color=BLUE, label="Comoving (proper distance today)")
    a2.plot(x, lt, color=ORANGE, label="Light-travel distance")
    a2.plot(x, da, color=GREEN, label="Angular-diameter distance")
    a2.plot(x, dl, color=VIOLET, label="Luminosity distance")
    a2.set_xscale("log")
    a2.set_yscale("log")
    a2.set_xlim(1.01, 1600)
    a2.set_ylim(0.1, 3e4)
    a2.set_xticks([1, 2, 3, 5, 11, 16, 101, 1101])
    a2.set_xticklabels(["0", "1", "2", "4", "10", "15", "100", "1100"])
    a2.set_xlabel("Redshift z (axis scaled as 1 + z)")
    a2.set_ylabel("Distance (billion light-years)")
    a2.legend(loc="upper left", fontsize=6.2)
    a2.set_title("(b) Four meanings of 'distance'", loc="left", fontsize=8.6)
    z14 = 14.44
    a2.scatter([1 + z14] * 3, [dcom(z14) * GLY_PER_MPC, lookback(z14), dcom(z14) * GLY_PER_MPC / (1 + z14)],
               color=INK, s=10, zorder=4)
    fig.text(0.99, 0.005, "Flat ΛCDM: H₀ = 67.7 km/s/Mpc, Ωm = 0.31, Ωr = 9.1 × 10⁻⁵, ΩΛ = 1 − Ωm − Ωr. "
             f"Present age {age(0):.2f} Gyr. Dots: MoM-z14.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch39_lookback")


# ---------------------------------------------------------------------------------------------
# 6. Redshifted emission lines vs instrument coverage
# ---------------------------------------------------------------------------------------------
def redshiftlines():
    z = np.linspace(0, 16, 400)
    lines = [("Lyman-α 121.6 nm", 0.1216, VIOLET), ("[O II] 372.7 nm", 0.3727, BLUE),
             ("[O III] 500.7 nm", 0.5007, GREEN), ("Hα 656.3 nm", 0.6563, RED)]
    fig, ax = plt.subplots(figsize=(6.8, 3.7))
    bands = [(0.115, 1.7, "Hubble (UV–near-IR, to 1.7 µm)", "#E3EEF8"),
             (1.7, 5.3, "JWST NIRCam / NIRSpec (0.6–5.3 µm)", "#FBE9DA"),
             (5.3, 28.5, "JWST MIRI (4.9–28.5 µm)", "#F6DDE1")]
    for lo, hi, t, c in bands:
        ax.axhspan(lo, hi, color=c, zorder=0)
        ax.text(15.8, np.sqrt(lo * hi) * (1.0 if hi < 20 else 1.45), t, ha="right", va="center", fontsize=6.6,
                color=INK, zorder=5, bbox=dict(fc=c, ec="none", pad=1.2))
    ax.axhline(0.6, color=ORANGE, lw=0.7, ls=":", zorder=1)
    ax.text(6.2, 0.585, "JWST short-wavelength limit 0.6 µm", fontsize=6.0, color=INK, va="top", ha="left")
    for name, l0, c in lines:
        ax.plot(z, l0 * (1 + z), color=c, lw=1.7, label=name)
    for zr, t in [(10.6, "GN-z11"), (14.44, "MoM-z14")]:
        ax.axvline(zr, color=GREY, lw=0.8, ls="--")
        ax.text(zr - 0.15, 0.15, t, rotation=90, fontsize=6.4, color=INK, va="bottom", ha="right")
    ax.set_yscale("log")
    ax.set_ylim(0.1, 30)
    ax.set_xlim(0, 16)
    ax.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20])
    ax.set_yticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10", "20"])
    ax.set_xlabel("Redshift z")
    ax.set_ylabel("Observed wavelength (µm)")
    ax.legend(loc="upper left", fontsize=6.6, frameon=True, facecolor="white", edgecolor="#D5DDE5")
    fig.text(0.99, 0.005, "λ(observed) = λ(emitted) × (1 + z). Shading: wavelength range of the instruments; "
             "Earth's atmosphere blocks most light beyond 2.5 µm and below 0.3 µm.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch39_redshiftlines")


# ---------------------------------------------------------------------------------------------
# 7. Transit depth and atmospheric signal
# ---------------------------------------------------------------------------------------------
RE_KM, RSUN_KM = 6371.0, 695700.0


def transit():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.1, 1.0]))
    rp = np.logspace(np.log10(0.5), np.log10(15), 200)
    for rs, c, t in [(1.0, ORANGE, "Sun-like star (1.0 R$_\\odot$)"), (0.5, GREEN, "K dwarf (0.5 R$_\\odot$)"),
                     (0.2, RED, "M dwarf (0.2 R$_\\odot$)"), (0.12, VIOLET, "TRAPPIST-1 (0.12 R$_\\odot$)")]:
        a1.plot(rp, (rp * RE_KM / (rs * RSUN_KM)) ** 2 * 1e6, color=c, label=t)
    a1.axvline(1.0, color=GREY, lw=0.7, ls="--")
    a1.text(1.04, 2.0, "Earth", fontsize=6.3, color=INK, rotation=90, va="bottom")
    a1.axvline(11.2, color=GREY, lw=0.7, ls="--")
    a1.text(10.4, 2.0, "Jupiter", fontsize=6.3, color=INK, rotation=90, va="bottom")
    a1.scatter([1.0], [83.9], color=INK, s=14, zorder=4)
    a1.annotate("84 ppm", xy=(1.0, 83.9), xytext=(1.12, 36), fontsize=6.4,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    for v, t in [(60, "≈60 ppm in 1 h: TESS requirement (bright star)"), (20, "≈20 ppm in 6.5 h: Kepler goal (12th mag)")]:
        a1.axhline(v, color=NAVY, lw=0.7, ls=":")
        a1.text(14.5, v * 1.12, t, fontsize=6.0, ha="right", va="bottom", color=INK,
                bbox=dict(fc="white", ec="none", pad=0.6))
    a1.set_xscale("log")
    a1.set_yscale("log")
    a1.set_xlim(0.5, 15)
    a1.set_ylim(1, 1e5)
    a1.set_xticks([0.5, 1, 2, 5, 10])
    a1.set_xticklabels(["0.5", "1", "2", "5", "10"])
    a1.set_xlabel("Planet radius (Earth radii)")
    a1.set_ylabel("Transit depth (ppm)")
    a1.legend(loc="upper left", fontsize=6.1, frameon=True, facecolor="white", edgecolor="#D5DDE5", framealpha=1.0)
    a1.set_title("(a) Transit depth $(R_p/R_\\star)^2$", loc="left", fontsize=8.6)

    # atmospheric signal: 2 H Rp / R*^2 x 5 scale heights (values from NASA Exoplanet Archive, mu assumed)
    k, mH, G = 1.380649e-23, 1.6735e-27, 6.674e-11
    RE, ME, RS = 6.371e6, 5.972e24, 6.957e8
    pl = [("WASP-39 b (hot Saturn, H₂)", 14.336, 89.31, 1166, 0.939, 2.3),
          ("GJ 1214 b (sub-Neptune, H₂)", 2.733, 8.41, 567, 0.2162, 2.3),
          ("K2-18 b (sub-Neptune, H₂)", 2.37, 8.92, 284, 0.411, 2.3),
          ("TRAPPIST-1 e (rocky, N₂)", 0.92, 0.692, 249.7, 0.1192, 28.0),
          ("LHS 1140 b (rocky, N₂)", 1.73, 5.6, 226, 0.2159, 28.0),
          ("Earth seen around the Sun", 1.0, 1.0, 255, 1.0, 29.0)]
    names, sig = [], []
    for nme, r, m, T, rs, mu in pl:
        g = G * m * ME / (r * RE) ** 2
        H = k * T / (mu * mH * g)
        names.append(nme)
        sig.append(2 * H * r * RE / (rs * RS) ** 2 * 1e6)
    y = np.arange(len(pl))[::-1]
    a2.barh(y, sig, color=[BLUE, BLUE, BLUE, GREEN, GREEN, GREY], height=0.6, edgecolor="white")
    for yy, s in zip(y, sig):
        txt = f"{s:.0f} ppm" if s >= 10 else f"{s:.2g} ppm"
        a2.text(s * 1.2, yy, txt, va="center", fontsize=6.3, color=INK, zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.6))
    a2.set_yticks(y)
    a2.set_yticklabels(names, fontsize=6.5)
    a2.set_xscale("log")
    a2.set_xlim(0.08, 3e3)
    a2.axvline(20, color=NAVY, lw=0.7, ls=":")
    a2.text(24, 0.0, "≈20 ppm: indicative\nJWST precision", fontsize=6.0, color=INK, va="center")
    a2.set_xlabel("Signal of one atmospheric scale height (ppm)")
    a2.grid(axis="y", visible=False)
    a2.tick_params(axis="y", length=0)
    a2.set_title("(b) Signal of an atmosphere in transmission", loc="left", fontsize=8.6)
    fig.text(0.99, 0.005, "Scale height H = kT/(μ m_H g), T = equilibrium temperature; signal = 2H·Rp/R*²; strong bands "
             "span 2–5 H. Data: NASA Exoplanet Archive; μ = 2.3 (H₂) or 28–29 (N₂-rich) assumed.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch39_transit")


# ---------------------------------------------------------------------------------------------
# 8. Where observatories fly: distance from Earth
# ---------------------------------------------------------------------------------------------
def orbits():
    groups = [
        ("Low Earth orbit", [("Swift (Oct 2026)", 278, 282), ("Hubble", 468, 471), ("Fermi", 487, 498),
                             ("NuSTAR", 532, 542), ("IXPE", 528, 537)], BLUE),
        ("High Earth orbit", [("Chandra", 12650, 136200), ("XMM-Newton", 29480, 91640),
                              ("TESS (2:1 lunar resonance)", 119090, 364460)], ORANGE),
        ("Sun–Earth L2", [("JWST, Gaia, Euclid, Roman,\nPlanck, Herschel, eROSITA", 1.2e6, 1.8e6)], GREEN),
        ("Earth-trailing solar orbit", [("Kepler (at retirement 2018)", 1.70e8, 1.70e8),
                                        ("Spitzer (at shutdown 2020)", 2.656e8, 2.656e8)], VIOLET),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 3.05))
    y = 0
    yt, yl = [], []
    for g, items, c in groups:
        for name, lo, hi in items:
            if hi / lo > 1.05:
                ax.plot([lo, hi], [y, y], color=c, lw=4.0, solid_capstyle="butt")
            else:
                ax.scatter([lo], [y], color=c, s=40, zorder=3)
            yt.append(y)
            yl.append(name)
            y -= 1
        gx = {"Low Earth orbit": 2.0e3, "High Earth orbit": 1.2e6, "Earth-trailing solar orbit": 8e7}.get(g, 1.4e9)
        gha = "left" if g in ("Low Earth orbit", "High Earth orbit") else "right"
        ax.text(gx, y + 0.5 + len(items) / 2, g, fontsize=7.0, color=c, weight="bold", ha=gha, va="center")
        y -= 0.6
    refs = [(35786, "GEO 35 786 km"), (384400, "Moon 384 400 km"), (1.496e8, "1 AU")]
    for v, t in refs:
        ax.axvline(v, color=GREY, lw=0.7, ls="--", zorder=0)
        ax.text(v * 1.08, 0.75, t, fontsize=6.3, color=GREY, va="bottom", ha="left")
    ax.set_yticks(yt)
    ax.set_yticklabels(yl, fontsize=6.6)
    ax.set_xscale("log")
    ax.set_xlim(150, 1.6e9)
    ax.set_ylim(y + 0.3, 1.6)
    ax.set_xlabel("Distance from Earth's surface (km)")
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    fig.text(0.99, 0.005, "Bars: perigee–apogee (Earth orbits, CelesTrak elements Oct 2026) or approximate range of "
             "distance for L2 halo orbits. Dots: distance at end of mission (JPL Horizons).", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch39_orbits")


if __name__ == "__main__":
    fns = [emcoverage, gantt, apertures, exoplanets, lookbackfig, redshiftlines, transit, orbits]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
