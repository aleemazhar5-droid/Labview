import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403

SIGMA = 5.670374e-8


def materials():
    mats = [("Aluminium 7075-T6", 2810, 71.7, 503, BLUE), ("Aluminium 6061-T6", 2700, 68.9, 276, SKY),
            ("Titanium Ti-6Al-4V", 4430, 114, 880, GREY), ("Stainless steel 304", 8000, 193, 215, NAVY),
            ("Magnesium AZ31", 1770, 45, 220, GOLD), ("Beryllium", 1850, 287, 345, GREEN),
            ("CFRP quasi-isotropic", 1600, 70, 600, ORANGE), ("CFRP high-modulus UD", 1650, 300, 1100, RED),
            ("Al-Li 2195", 2700, 76, 560, VIOLET), ("Invar 36", 8050, 141, 275, "#8C564B")]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    for n, rho, E, S, c in mats:
        x = E * 1e9 / rho / 1e6
        y = S * 1e6 / rho / 1e3
        ax.scatter(x, y, s=60, color=c, zorder=3, edgecolor="white")
        dy = {"Titanium Ti-6Al-4V": 1.12, "Al-Li 2195": 0.93, "Aluminium 7075-T6": 0.86}.get(n, 1.02)
        ax.text(x * 1.04, y * dy, n, fontsize=7, zorder=4)
    ax.set_xlabel("Specific stiffness E/ρ (MJ/kg = 10⁶ m²/s²)")
    ax.set_ylabel("Specific strength σᵧ/ρ (kJ/kg)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(8, 300)
    ax.set_ylim(20, 1000)
    note(ax, "Representative room-temperature properties; CFRP values are laminate-dependent. Beryllium: high stiffness "
             "for optics (JWST mirrors) but toxic to machine.", xy=(1, -0.15))
    save(fig, "ch05_materials")


def sandwich():
    fig, ax = canvas(7.0, 3.0, (0, 100), (0, 40))
    ax.add_patch(Rectangle((8, 28), 60, 2.2, fc="#9AA5B1", ec="#555", lw=0.6))
    ax.add_patch(Rectangle((8, 10), 60, 2.2, fc="#9AA5B1", ec="#555", lw=0.6))
    for k in range(12):
        x = 9 + k * 5
        pts = [(x, 12.2), (x + 1.4, 20), (x, 28), (x + 2.6, 28), (x + 4, 20), (x + 2.6, 12.2)]
        ax.add_patch(Polygon(pts, closed=True, fc="#F3E3B5", ec="#B08D3C", lw=0.6))
    ax.text(70, 29, "face sheet (Al 0.2–0.5 mm or CFRP)", fontsize=7, va="center")
    ax.text(70, 20, "honeycomb core (Al 5056, Nomex)\n10–50 mm, ~30–80 kg/m³", fontsize=7, va="center")
    ax.text(70, 11, "face sheet", fontsize=7, va="center")
    ax.add_patch(Circle((38, 20), 2.2, fc="#555", ec="#333"))
    ax.text(38, 4.5, "potted insert for bolting equipment", fontsize=7, ha="center")
    arrow(ax, (38, 6.5), (38, 17.5), color=GREY, lw=0.7, ms=6)
    ax.text(2, 36.5, "Bending stiffness grows with the square of the core thickness: doubling the core thickness "
            "makes the panel ~4× stiffer for a few % more mass.", fontsize=7, color=NAVY)
    save(fig, "ch05_sandwich")


def config_types():
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6))
    titles = ["Central cylinder + shear panels\n(GEO platforms, large EO)", "Box / panel structure\n(small and medium satellites)",
              "Truss structure\n(stations, large antennas)"]
    for ax, t in zip(axs, titles):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(t, fontsize=7.5)
    a = axs[0]
    a.add_patch(Rectangle((1.5, 1), 7, 7.5, fc="#EAF1F7", ec=NAVY))
    a.add_patch(Rectangle((3.8, 1), 2.4, 7.5, fc="#C6DBEF", ec=BLUE))
    a.plot([1.5, 3.8], [4.75, 4.75], color=NAVY, lw=1)
    a.plot([6.2, 8.5], [4.75, 4.75], color=NAVY, lw=1)
    a.text(5, 0.4, "launch adapter ring", fontsize=6, ha="center")
    b = axs[1]
    b.add_patch(Polygon([(2, 1.5), (7, 1.5), (8.5, 3), (8.5, 8), (3.5, 8), (2, 6.5)], fc="#EAF1F7", ec=NAVY))
    b.plot([2, 7, 8.5], [6.5, 6.5, 8], color=NAVY, lw=0.8)
    b.plot([7, 7], [1.5, 6.5], color=NAVY, lw=0.8)
    b.plot([2, 7], [4, 4], color=GREY, lw=0.6, ls="--")
    c = axs[2]
    pts = [(1, 1), (9, 1), (1, 9), (9, 9), (5, 5)]
    for x in np.linspace(1, 9, 5):
        c.plot([x, x], [1, 9], color=NAVY, lw=0.8)
        c.plot([1, 9], [x, x], color=NAVY, lw=0.8)
    for x in np.linspace(1, 7, 4):
        c.plot([x, x + 2], [1, 3], color=GREY, lw=0.6)
        c.plot([x, x + 2], [3, 1], color=GREY, lw=0.6)
    save(fig, "ch05_structures")


def mli():
    fig, ax = canvas(7.0, 3.0, (0, 100), (0, 40))
    ax.add_patch(Rectangle((5, 32), 60, 2.0, fc="#F2F0E6", ec="#999", lw=0.5))
    ax.text(67, 33, "outer layer: beta cloth / black Kapton / Ge-Kapton (UV, AO, ESD)", fontsize=6.8, va="center")
    for k in range(10):
        y = 30 - k * 2.0
        ax.add_patch(Rectangle((5, y), 60, 0.5, fc="#D6A84B", ec="none"))
        ax.add_patch(Rectangle((5, y - 0.9), 60, 0.6, fc="#FFFFFF", ec="#DDD", lw=0.3))
    ax.text(67, 21, "10–30 reflector layers: aluminised Mylar or Kapton\n(ε ≈ 0.03), separated by Dacron or silk netting",
            fontsize=6.8, va="center")
    ax.add_patch(Rectangle((5, 7), 60, 2.0, fc="#E8D8B0", ec="#999", lw=0.5))
    ax.text(67, 8, "inner layer facing the spacecraft", fontsize=6.8, va="center")
    ax.add_patch(Rectangle((5, 2), 60, 4.0, fc="#C9D3DD", ec="#777"))
    ax.text(35, 4, "spacecraft panel", fontsize=6.8, ha="center", va="center")
    for x in (20, 50):
        arrow(ax, (x, 39), (x, 34.5), color=ORANGE, lw=1.2, ms=8)
    ax.text(21, 37.5, "sunlight / IR", fontsize=6.6, color=ORANGE)
    ax.text(2, -1.5, "Effective emittance ε* ≈ 0.01–0.05 in practice (seams, vents and edges dominate); "
            "each layer radiates only to its neighbours.", fontsize=6.8, color=GREY)
    save(fig, "ch05_mli")


def heatpipe():
    fig, ax = canvas(7.0, 2.6, (0, 100), (0, 34))
    ax.add_patch(FancyBboxPatch((8, 12), 84, 12, boxstyle="round,pad=0,rounding_size=6", fc="#EAF1F7", ec=NAVY, lw=1.2))
    ax.add_patch(Rectangle((10, 13), 80, 2.0, fc="#C9A27A", ec="none"))
    ax.add_patch(Rectangle((10, 21), 80, 2.0, fc="#C9A27A", ec="none"))
    ax.text(50, 17.8, "vapour flows to the cold end", fontsize=7.5, ha="center", color=RED)
    arrow(ax, (25, 18.5), (75, 18.5), None, color=RED, lw=1.4)
    ax.text(50, 9.5, "liquid returns by capillary action in the wick / axial grooves", fontsize=7.5, ha="center",
            color=BLUE)
    arrow(ax, (75, 14), (25, 14), None, color=BLUE, lw=1.0)
    for x in (12, 16, 20):
        arrow(ax, (x, 3), (x, 11.5), None, color=ORANGE, lw=1.2, ms=7)
    for x in (80, 84, 88):
        arrow(ax, (x, 25), (x, 32), None, color=SKY, lw=1.2, ms=7)
    ax.text(16, 1, "EVAPORATOR (heat in from electronics)", fontsize=6.8, ha="center", color=ORANGE)
    ax.text(84, 32.5, "CONDENSER (heat out to radiator)", fontsize=6.8, ha="center", color=SKY, va="bottom")
    ax.text(50, -2.5, "Working fluid: ammonia (−60 to +100 °C), also methanol, water, propylene; "
            "conductance ~1000× a solid aluminium bar of the same mass", fontsize=6.6, ha="center", color=GREY)
    save(fig, "ch05_heatpipe")


def radiator_sizing():
    T = np.linspace(-40, 80, 200) + 273.15
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for eps, sink, c, lab in [(0.85, 0, BLUE, "ε = 0.85, deep space sink"), (0.85, 200, GREEN, "ε = 0.85, LEO with Earth IR (≈200 K sink)"),
                              (0.85, 250, ORANGE, "ε = 0.85, partial sun/albedo (≈250 K sink)")]:
        q = eps * SIGMA * (T ** 4 - sink ** 4)
        ax.plot(T - 273.15, q, color=c, label=lab)
    ax.set_xlabel("Radiator temperature (°C)")
    ax.set_ylabel("Heat rejected (W per m²)")
    ax.legend(fontsize=7)
    ax.text(-38, 520, "Rule of thumb: a radiator at 20 °C rejects\n≈ 350 W/m² to space (single-sided)", fontsize=7.2,
            color=GREY)
    save(fig, "ch05_radiator")


def solar_eff():
    data = [(1958, 9, "Vanguard 1 Si"), (1965, 11, "Si"), (1975, 13, "Si BSR"), (1985, 15, "Si BSFR"),
            (1990, 18, "GaAs/Ge"), (1996, 22, "Dual-junction"), (2001, 26, "Triple-junction"), (2006, 28.3, "TJ"),
            (2012, 29.5, "ZTJ / 3G30"), (2016, 30.7, "IMM / 4J"), (2020, 32, "4G32 / IMM4"), (2024, 33.5, "Quad/5J lab")]
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    x = [d[0] for d in data]
    y = [d[1] for d in data]
    ax.plot(x, y, "-o", color=ORANGE, ms=4)
    for xi, yi, t in data:
        ax.text(xi, yi + 1.0, t, fontsize=6.3, ha="center")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cell efficiency, AM0, BOL (%)")
    ax.set_ylim(5, 38)
    ax.axhline(36, color=GREY, ls=":", lw=0.6)
    note(ax, "Approximate flight-qualified (and late lab) AM0 efficiencies at beginning of life, 28 °C. "
             "Commercial LEO constellations often use cheaper Si or thin-film cells.", xy=(1, -0.17))
    save(fig, "ch05_solar_eff")


def iv_curve():
    V = np.linspace(0, 2.75, 300)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for T, c, Isc, Voc in [(28, BLUE, 0.52, 2.70), (80, RED, 0.535, 2.47), (-50, GREEN, 0.50, 3.0)]:
        Vt = 0.075
        I = Isc * (1 - np.exp((V - Voc) / Vt))
        I = np.clip(I, 0, None)
        P = V * I
        k = np.argmax(P)
        ax.plot(V, I, color=c, label=f"{T} °C")
        ax.plot(V[k], I[k], "o", color=c, ms=5)
    ax.set_xlim(0, 3.1)
    ax.set_ylim(0, 0.62)
    ax.set_xlabel("Cell voltage (V)")
    ax.set_ylabel("Current (A), triple-junction cell ≈ 30 cm²")
    ax.legend(title="Cell temperature", fontsize=7, title_fontsize=7, loc="lower left")
    ax.text(1.9, 0.56, "● maximum power point (MPP)", fontsize=7)
    ax.text(0.1, 0.36, "Higher temperature lowers voltage (≈ −6 mV/°C per triple-junction cell)\nand power; cold cells give more power.", fontsize=6.8, color=GREY)
    save(fig, "ch05_iv")


def batteries():
    chem = [("Ni-Cd", 30, 40, GREY), ("Ni-H₂ (IPV)", 55, 45, SKY), ("Li-ion (2000s)", 120, 200, BLUE),
            ("Li-ion 18650 (2020s)", 200, 500, NAVY), ("Li-ion pouch (high-energy)", 240, 550, VIOLET),
            ("Ag-Zn (primary)", 120, 230, GOLD), ("Li-SOCl₂ (primary)", 400, 900, ORANGE),
            ("Li-S / solid-state (R&D)", 400, 700, GREEN)]
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    offs = {"Li-ion 18650 (2020s)": (0.62, 1.0, "right"), "Li-ion pouch (high-energy)": (0.62, 1.12, "right"),
            "Li-ion (2000s)": (1.05, 0.86, "left"), "Ag-Zn (primary)": (1.05, 1.06, "left"),
            "Li-S / solid-state (R&D)": (1.05, 0.78, "left")}
    for n, e, v, c in chem:
        ax.scatter(e, v, s=70, color=c, zorder=3, edgecolor="white")
        fx, fy, ha = offs.get(n, (1.04, 1.04, "left"))
        ax.text(e * (fx if ha == "left" else 0.96), v * fy, n, fontsize=7, ha=ha)
    ax.set_xlabel("Specific energy at cell level (Wh/kg)")
    ax.set_ylabel("Energy density (Wh/L)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(20, 700)
    ax.set_ylim(25, 1500)
    note(ax, "Battery-level values are 20–40 % lower (packaging, wiring, thermal control). Primary = non-rechargeable.",
         xy=(1, -0.16))
    save(fig, "ch05_batteries")


def dod_cycles():
    dod = np.linspace(10, 90, 100)
    cycles = 2.0e5 * (dod / 10) ** -2.1
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(dod, cycles, color=BLUE, lw=2)
    ax.set_yscale("log")
    ax.set_xlabel("Depth of discharge per cycle (%)")
    ax.set_ylabel("Cycle life (to 80 % capacity)")
    ax.axhline(5.5e4, color=GREY, lw=0.6, ls="--")
    ax.text(62, 6.2e4, "LEO, 10 years ≈ 55 000 cycles", fontsize=7, color=GREY)
    ax.axhline(1350, color=GREY, lw=0.6, ls="--")
    ax.text(62, 1500, "GEO, 15 years ≈ 1 350 cycles", fontsize=7, color=GREY)
    ax.axvspan(15, 30, color=GREEN, alpha=0.08)
    ax.text(16, 2500, "typical LEO\ndesign DoD", fontsize=7, color=GREEN)
    ax.axvspan(60, 80, color=ORANGE, alpha=0.08)
    ax.text(62, 3.0e4, "typical GEO\ndesign DoD", fontsize=7, color=ORANGE)
    note(ax, "Illustrative Li-ion trend; real cycle life depends on cell type, temperature and charge voltage.",
         xy=(1, -0.16))
    save(fig, "ch05_dod")


def orbit_power():
    t = np.linspace(0, 2 * 95, 1000)
    sun = ((t % 95) < 60)
    gen = np.where(sun, 1350, 0.0)
    load = 750 + 150 * ((t % 95) > 20) * ((t % 95) < 32)
    soc = np.zeros_like(t)
    soc[0] = 0.72
    cap = 1500.0 * 3600
    dt = t[1] - t[0]
    for k in range(1, len(t)):
        net = gen[k] - load[k]
        if net > 0 and soc[k - 1] >= 1.0:
            net = 0
        eff = 0.95 if net > 0 else 1 / 0.95
        soc[k] = min(1.0, soc[k - 1] + net * eff * dt * 60 / cap)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 3.8), sharex=True, gridspec_kw=dict(height_ratios=[1.3, 1]))
    a1.fill_between(t, 0, gen, where=sun, color=GOLD, alpha=0.35, step="pre", label="Solar array output")
    a1.plot(t, load, color=RED, lw=1.5, label="Spacecraft load")
    a1.set_ylabel("Power (W)")
    a1.legend(fontsize=7, loc="upper center", ncol=2, bbox_to_anchor=(0.45, 1.22))
    a1.set_ylim(0, 1600)
    for k in range(2):
        a1.axvspan(60 + 95 * k, 95 + 95 * k, color=NAVY, alpha=0.08)
        a1.text(61 + 95 * k, 1420, "eclipse", fontsize=7, color=NAVY)
    a2.plot(t, soc * 100, color=GREEN, lw=1.8)
    a2.set_ylabel("Battery SoC (%)")
    a2.set_xlabel("Time (minutes) — two 95-minute LEO orbits")
    a2.set_ylim(60, 102)
    save(fig, "ch05_orbit_power")


def power_arch():
    fig, ax = canvas(7.2, 3.6, (0, 100), (0, 48))
    box(ax, 2, 30, 16, 12, "Solar array\n(strings)", fc="#FBF3D9", ec=GOLD, fs=7.5)
    box(ax, 26, 30, 18, 12, "Array regulator\n(S3R shunt or\nMPPT converter)", fc="#E8F1FA", ec=BLUE, fs=7)
    box(ax, 52, 30, 16, 12, "Main power bus\n(28 V, 50 V or\n100 V regulated)", fc=NAVY, ec=NAVY, color="white", fs=7)
    box(ax, 26, 8, 18, 12, "Battery charge/\ndischarge\nregulators", fc="#E8F1FA", ec=BLUE, fs=7)
    box(ax, 2, 8, 16, 12, "Li-ion battery\n(series cells,\nparallel strings)", fc="#EEF7F1", ec=GREEN, fs=7)
    box(ax, 76, 36, 22, 9, "Power distribution unit\n(latching current limiters,\nswitches, fuses)", fc="#F3EFF9",
        ec=VIOLET, fs=6.6)
    box(ax, 76, 22, 22, 10, "Loads: payload, ADCS,\nC&DH, TT&C, heaters,\npropulsion valves", fc="white", ec=GREY, fs=6.6)
    box(ax, 76, 6, 22, 10, "Point-of-load DC/DC\nconverters (5 V, 3.3 V,\n1.0 V core, ±15 V)", fc="white", ec=GREY,
        fs=6.6)
    arrow(ax, (18, 36), (26, 36), color=GOLD, lw=1.4)
    arrow(ax, (44, 36), (52, 36), color=BLUE, lw=1.4)
    arrow(ax, (60, 30), (35, 20), None, color=BLUE, lw=1.0, style="<|-|>")
    arrow(ax, (26, 14), (18, 14), None, color=GREEN, lw=1.2, style="<|-|>")
    arrow(ax, (68, 38), (76, 40), color=VIOLET)
    arrow(ax, (87, 36), (87, 32), color=GREY)
    arrow(ax, (87, 22), (87, 16), color=GREY)
    ax.text(2, 1.5, "Direct-energy-transfer (DET) systems pass array power straight to a regulated bus; "
            "MPPT systems extract maximum array power at the cost of converter losses.", fontsize=6.6, color=GREY)
    save(fig, "ch05_power_arch")


def solar_distance():
    r = np.linspace(0.3, 10, 400)
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.plot(r, 1361 / r ** 2, color=ORANGE, lw=2)
    ax.set_yscale("log")
    ax.set_xscale("log")
    for d, n in [(0.387, "Mercury"), (0.723, "Venus"), (1, "Earth"), (1.524, "Mars"), (2.77, "Ceres"),
                 (5.2, "Jupiter (Juno: 3×9 m arrays,\n≈ 500 W at Jupiter)"), (9.54, "Saturn")]:
        ax.plot(d, 1361 / d ** 2, "o", color=NAVY, ms=4)
        ax.text(d * 1.06, 1361 / d ** 2 * 1.15, n, fontsize=6.8)
    ax.set_xlabel("Distance from the Sun (AU)")
    ax.set_ylabel("Solar irradiance (W/m²)")
    ax.text(0.33, 20, "Beyond Jupiter, solar power becomes impractical\n→ radioisotope power (RTGs)", fontsize=7,
            color=GREY)
    save(fig, "ch05_solar_distance")


def rtg():
    fig, ax = canvas(7.0, 3.4, (0, 100), (0, 46))
    cx, cy = 66, 23
    for k in range(8):
        a = np.radians(22.5 + k * 45)
        x0, y0 = cx + 9 * np.cos(a), cy + 9 * np.sin(a)
        x1, y1 = cx + 21 * np.cos(a), cy + 21 * np.sin(a)
        ax.plot([x0, x1], [y0, y1], color="#8A949E", lw=6, solid_capstyle="butt")
    ax.add_patch(Circle((cx, cy), 11, fc="#C9D3DD", ec=NAVY, lw=1.2))
    ax.add_patch(Circle((cx, cy), 7.5, fc="#F4B266", ec=RED, lw=0.8))
    ax.add_patch(Circle((cx, cy), 4.0, fc="#E3646B", ec="#7a1f0f", lw=0.8))
    ax.text(cx, cy, "Pu-238\nheat\nsource", fontsize=6, ha="center", va="center", color="white")
    ax.annotate("thermoelectric couples\nbetween hot shoe (≈530 °C)\nand housing", xy=(cx + 8.5, cy + 3), xytext=(88, 40),
                fontsize=6.4, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6), ha="center")
    ax.annotate("radiator fins\n(≈150–200 °C)", xy=(cx + 16, cy - 12), xytext=(92, 6), fontsize=6.4,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6), ha="center")
    ax.text(cx, 0.5, "cross-section (schematic)", fontsize=6.4, ha="center", color=GREY)
    ax.text(1, 43, "MMRTG — Curiosity, Perseverance, Dragonfly", fontsize=8, weight="bold", color=NAVY, va="top")
    ax.text(1, 36, "• 8 GPHS modules, 4.8 kg PuO₂\n• ≈ 2 000 W thermal\n• ≈ 110 W electric at launch\n"
            "• conversion efficiency ≈ 6 %\n• output falls ≈ 4 % per year\n  (Pu-238 half-life 87.7 years\n"
            "  plus thermocouple ageing)\n• mass 45 kg, length 0.66 m", fontsize=6.8, va="top")
    save(fig, "ch05_rtg")


def mechanisms():
    fig, ax = canvas(7.2, 2.6, (0, 100), (0, 34))
    items = [("Hold-down/release", "Pyro bolt cutters,\nFrangibolt (SMA),\nNEA split-spool,\nthermal knife", BLUE),
             ("Hinges & deployers", "Spring hinges,\ndampers, latches,\nbooms (STEM,\ncoilable, telescopic)", GREEN),
             ("Rotating", "Solar array drive\n(SADA), antenna\npointing, scan\nmirrors, slip rings", ORANGE),
             ("Separation", "Clamp bands\n(Ø 937–1666 mm),\nLightband rings,\nCubeSat deployers", VIOLET),
             ("Precision", "Hexapods, focus\nmechanisms,\nfilter wheels,\ncryocooler drives", RED)]
    for k, (t, b, c) in enumerate(items):
        title_box(ax, 1 + k * 19.8, 4, 18.5, 26, t, b, hc=c, ec=c, fc="white", fs=5.7, tfs=6.6)
    save(fig, "ch05_mechanisms")


if __name__ == "__main__":
    materials(); sandwich(); config_types(); mli(); heatpipe(); radiator_sizing(); solar_eff(); iv_curve()
    batteries(); dod_cycles(); orbit_power(); power_arch(); solar_distance(); rtg(); mechanisms()
