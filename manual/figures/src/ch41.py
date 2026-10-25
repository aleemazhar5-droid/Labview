"""Figures for Chapter 41 — Space Resources and Asteroid Mining."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch  # noqa: F401

G0 = 9.80665


# ---------------------------------------------------------------------------------------------
# 1. The "gear ratio" of space resources
# ---------------------------------------------------------------------------------------------
def stage_ratio(dv_kms, isp=450.0, eps=0.10):
    """Expendable in-space stage: returns (m0/m_payload, m_prop/m_payload). Dry mass = eps * propellant."""
    r = np.exp(dv_kms * 1000.0 / (isp * G0))
    mp = (r - 1.0) / (1.0 - eps * (r - 1.0))
    return 1.0 + (1.0 + eps) * mp, mp


def tanker_ratio(dv_kms, isp=450.0, dry=10.0, load=30.0, dv_back=None):
    """Reusable lunar tanker: propellant produced on the Moon per kg delivered (net of the reserve kept to fly
    back to the surface, which needs dv_back; equal to dv_kms unless aerobraking helps only one way)."""
    r = np.exp(dv_kms * 1000.0 / (isp * G0))
    rb = np.exp((dv_back if dv_back else dv_kms) * 1000.0 / (isp * G0))
    ascent = (dry + load) * (r - 1.0)
    reserve = dry * (rb - 1.0)
    net = load - reserve
    return (ascent + load) / net


LAUNCH = 25.0           # kg lifted off Earth per kg placed in LEO (4 % payload fraction)


def gear():
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.05, 1.0]))
    dests = [("Low Earth orbit", 0.0, 2.8, 5.9), ("Earth–Moon L1", 3.8, 2.5, 2.5), ("Low lunar orbit", 4.0, 1.9, 1.9),
             ("Lunar surface", 5.9, 0.0, 0.0)]
    y = np.arange(len(dests))
    earth = [LAUNCH * stage_ratio(d[1])[0] for d in dests]
    moon = [tanker_ratio(d[2], dv_back=d[3]) if d[2] > 0 else 1.0 for d in dests]
    a.barh(y - 0.19, earth, height=0.36, color=BLUE, label="from Earth (lift-off mass)", zorder=2)
    a.barh(y + 0.19, moon, height=0.36, color=ORANGE, label="from the Moon (lunar propellant)", zorder=2)
    for yi, e, m in zip(y, earth, moon):
        a.text(e * 1.08, yi - 0.19, f"{e:.0f}", va="center", fontsize=6.8, color=BLUE)
        extra = " (used on site)" if m == 1.0 else (" (tanker must climb back out)" if m > 20 else "")
        a.text(m * 1.08, yi + 0.19, (f"{m:.0f}" if m > 20 else f"{m:.1f}") + extra, va="center", fontsize=6.8,
               color=ORANGE)
    a.set_xscale("log")
    a.set_xlim(0.8, 1500)
    a.set_yticks(y)
    a.set_yticklabels([d[0] for d in dests], fontsize=7.4)
    a.invert_yaxis()
    a.grid(axis="y", visible=False)
    a.set_xlabel("kg leaving the source per kg of propellant delivered", fontsize=7.6)
    a.set_title("(a) The gear ratio", fontsize=8.6)
    a.text(0.88, -0.19, "Earth lift-off mass", va="center", ha="left", fontsize=6.3, color="white", zorder=3)
    a.text(0.88, 0.19, "lunar propellant", va="center", ha="left", fontsize=6.3, color="white", zorder=3)

    p = np.logspace(0, 2.3, 200)
    earth_ls = LAUNCH * stage_ratio(5.9)[0]            # Earth lift-off per kg landed on the Moon
    for name, dvE, dvM, col, ls in [("low lunar orbit", 4.0, 1.9, GREEN, "-"), ("Earth–Moon L1", 3.8, 2.5, VIOLET, "--")]:
        e_src = LAUNCH * stage_ratio(dvE)[0]
        m_src = earth_ls * tanker_ratio(dvM) / p
        b.plot(p, m_src, color=col, ls=ls, lw=1.6, label=f"lunar propellant to {name}")
        b.axhline(e_src, color=col, ls=ls, lw=0.9, alpha=0.7)
        pb = earth_ls * tanker_ratio(dvM) / e_src
        b.plot([pb], [e_src], "o", color=col, ms=4, zorder=4)
        b.annotate(f"break-even\nP ≈ {pb:.1f}", (pb, e_src), xytext=((pb * 1.25, e_src * 2.6) if ls == "-" else (22, 30)),
                   fontsize=6.3, color=col, arrowprops=dict(arrowstyle="-", color=col, lw=0.6))
    b.text(150, 72.6 * 1.12, "Earth-sourced", fontsize=6.3, color=GREY, ha="right", va="bottom")
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlim(1, 200)
    b.set_ylim(1, 500)
    b.set_xlabel("Plant productivity P (kg produced per kg landed)", fontsize=7.6)
    b.set_ylabel("Earth lift-off mass per kg delivered", fontsize=7.6)
    b.set_title("(b) When does lunar propellant pay?", fontsize=8.6)
    b.legend(loc="lower left", fontsize=6.3, handlelength=2.0)
    fig.text(0.99, 0.01, "Launcher: 4 % of lift-off mass reaches LEO. Earth-sourced: expendable LOX/LH₂ stages, Isp 450 s, "
             "dry mass 10 % of propellant;\nΔv LEO→L1 3.8, →LLO 4.0, →lunar surface 5.9 km/s. Moon-sourced: reusable "
             "LOX/LH₂ tanker (10 t dry, 30 t loaded) keeps\npropellant to return; Δv surface→LLO 1.9, →L1 2.5, →LEO 2.8 km/s "
             "(aerobraking; 5.9 km/s back). Plant and tanker mass in (b) landed from Earth.",
             ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    save(fig, "ch41_gear")


# ---------------------------------------------------------------------------------------------
# 2. What the resources are made of
# ---------------------------------------------------------------------------------------------
OXIDE = {  # molar mass, metal symbol, metal atoms, O atoms
    "SiO2": (60.084, "Si", 1, 2), "TiO2": (79.866, "Ti", 1, 2), "Al2O3": (101.961, "Al", 2, 3),
    "FeO": (71.844, "Fe", 1, 1), "MgO": (40.304, "Mg", 1, 1), "CaO": (56.077, "Ca", 1, 1),
    "Na2O": (61.979, "other", 2, 1), "K2O": (94.196, "other", 2, 1), "Cr2O3": (151.99, "other", 2, 3),
    "MnO": (70.937, "other", 1, 1), "SO3": (80.06, "S", 1, 3), "P2O5": (141.94, "other", 2, 5),
    "H2O": (18.015, "H", 2, 1),
}


def oxides_to_elements(ox, extra=None):
    el = {}
    tot = sum(ox.values()) + (sum(extra.values()) if extra else 0.0)
    for k, wt in ox.items():
        mm, metal, nm, no = OXIDE[k]
        fo = no * 15.999 / mm
        el["O"] = el.get("O", 0) + wt * fo
        el[metal] = el.get(metal, 0) + wt * (1 - fo)
    if extra:
        for k, v in extra.items():
            el[k] = el.get(k, 0) + v
    return {k: 100 * v / tot for k, v in el.items()}


def norm(d):
    t = sum(d.values())
    return {k: 100 * v / t for k, v in d.items()}


def composition():
    highland = oxides_to_elements({"SiO2": 45.0, "TiO2": 0.54, "Al2O3": 27.3, "FeO": 5.1, "MgO": 5.7, "CaO": 15.7,
                                   "Na2O": 0.47, "K2O": 0.11})
    mare = oxides_to_elements({"SiO2": 42.2, "TiO2": 7.8, "Al2O3": 13.6, "FeO": 15.3, "MgO": 7.8, "CaO": 11.9,
                               "Na2O": 0.47, "K2O": 0.16, "Cr2O3": 0.3, "MnO": 0.2})
    mars = oxides_to_elements({"SiO2": 42.9, "TiO2": 1.2, "Al2O3": 9.4, "FeO": 19.2, "MgO": 8.7, "CaO": 7.3,
                               "Na2O": 2.7, "K2O": 0.5, "SO3": 5.5, "P2O5": 0.9, "H2O": 2.0}, extra={"other": 0.7})
    ci = norm({"O": 45.9, "Fe": 18.4, "Si": 10.65, "Mg": 9.61, "S": 5.35, "C": 3.48, "H": 1.97, "Ni": 1.08,
               "Ca": 0.92, "Al": 0.85, "other": 1.7})
    hchon = norm({"O": 35.7, "Fe": 27.5, "Si": 16.9, "Mg": 14.0, "S": 2.0, "Ca": 1.25, "Al": 1.13, "Ni": 1.6,
                  "other": 1.4})
    iron = norm({"Fe": 91.0, "Ni": 8.0, "other": 1.0})
    rows = [("Lunar highland soil\n(Apollo 16)", highland, "O 45 %, Al 14.5 %, Ca 11 %"),
            ("Lunar mare soil\n(Apollo 11, high-Ti)", mare, "O 42 %, Fe 12 %, Ti 4.7 %"),
            ("Mars soil\n(Gale crater)", mars, "O 43 %, Fe 15 %, H₂O ≈ 2 %"),
            ("C-type asteroid\n(CI chondrite)", ci, "H₂O-equivalent ≈ 18 %, C 3.5 %"),
            ("S-type asteroid\n(H chondrite)", hchon, "Fe–Ni metal grains ≈ 15–19 %"),
            ("M-type asteroid\n(iron meteorite)", iron, "Fe–Ni ≈ 99 %; Pt-group ≈ 10–40 ppm")]
    elements = [("O", NAVY), ("Si", SKY), ("Fe", RED), ("Al", "#9FB7C9"), ("Mg", GREEN), ("Ca", GOLD),
                ("Ti", VIOLET), ("Ni", "#8C564B"), ("S", "#E3C567"), ("C", INK), ("H", "#4FC1E9"), ("other", "#C8CDD3")]
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    for i, (name, comp, txt) in enumerate(rows):
        left = 0.0
        for el, col in elements:
            v = comp.get(el, 0.0)
            if v <= 0:
                continue
            ax.barh(i, v, left=left, color=col, height=0.66, edgecolor="white", lw=0.5, zorder=2)
            if v >= 5.5 or (el == "Ti" and v >= 4):
                ax.text(left + v / 2, i, el, ha="center", va="center", fontsize=6.4,
                        color="white" if is_dark(col) else INK, zorder=3)
            left += v
        ax.text(101.5, i, txt, va="center", ha="left", fontsize=6.5, color=INK)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.0)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Mass fraction of elements (%)", fontsize=7.8)
    ax.grid(axis="y", visible=False)
    for s in ("left",):
        ax.spines[s].set_visible(False)
    handles = [Rectangle((0, 0), 1, 1, fc=c) for _, c in elements]
    ax.legend(handles, [e for e, _ in elements], ncol=12, loc="lower left", bbox_to_anchor=(-0.02, 1.0),
              fontsize=6.3, handlelength=1.0, columnspacing=0.8, handletextpad=0.3)
    fig.text(0.99, 0.01, "Element fractions from average oxide analyses (lunar soils 64501-type and 10084; MSL Rocknest "
             "with ≈ 2 % H₂O),\nCI (Lodders 2003), H-chondrite and iron-meteorite averages. Representative values only.",
             ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.07, 0.79, 1))
    save(fig, "ch41_composition")


# ---------------------------------------------------------------------------------------------
# 3. Why ice survives only in cold traps
# ---------------------------------------------------------------------------------------------
KB = 1.380649e-23
AMU = 1.66054e-27
GYR = 3.156e16


def p_h2o(T):
    """Vapour pressure over ice (Pa), Murphy & Koop (2005)."""
    return np.exp(9.550426 - 5723.265 / T + 3.53068 * np.log(T) - 0.00728332 * T)


def p_co2(T):
    """Vapour pressure over CO2 ice (Pa), Clausius–Clapeyron from the triple point, L = 26.1 kJ/mol."""
    return 518e3 * np.exp(-26100 / 8.314 * (1 / T - 1 / 216.58))


def loss_m_per_gyr(p, T, m_amu, rho):
    flux = p * np.sqrt(m_amu * AMU / (2 * np.pi * KB * T))      # kg m^-2 s^-1 (Hertz–Knudsen, into vacuum)
    return flux / rho * GYR


def icestab():
    fig, ax = plt.subplots(figsize=(6.8, 3.3))
    T = np.linspace(30, 400, 800)
    lw = loss_m_per_gyr(p_h2o(T), T, 18.015, 930.0)
    lc = loss_m_per_gyr(p_co2(T), T, 44.01, 1560.0)
    zones = [(25, 60, "#DCE8F5", "coldest\ncrater\nfloors", 3e17, "top"),
             (60, 110, "#EAF1F7", "typical\npermanently\nshadowed\nregions", 3e17, "top"),
             (180, 260, "#FFF1E0", "sunlit polar\nterrain", 3e-12, "bottom"), (360, 400, "#FBE3D6", "equator\nat noon", 3e-12, "bottom")]
    for t0, t1, col, txt, yy, va in zones:
        ax.axvspan(t0, t1, color=col, zorder=0)
        ax.text((t0 + t1) / 2, yy, txt, ha="center", va=va, fontsize=6.2, color=NAVY, linespacing=1.1,
                bbox=dict(fc="white", ec="none", pad=0.8, alpha=0.7))
    ax.plot(T, lw, color=BLUE, lw=1.8, label="water ice (H₂O)")
    ax.plot(T, lc, color=ORANGE, lw=1.8, label="carbon dioxide ice (CO₂)")
    ax.axhline(1.0, color=GREY, lw=0.8, ls="--")
    ax.text(392, 1.6, "1 m lost per billion years", ha="right", va="bottom", fontsize=6.4, color=GREY)
    t1 = T[np.argmin(np.abs(np.log(lw)))]
    t2 = T[np.argmin(np.abs(np.log(lc)))]
    ax.plot([t1], [1], "o", color=BLUE, ms=4)
    ax.plot([t2], [1], "o", color=ORANGE, ms=4)
    ax.annotate(f"H₂O stable below ≈ {t1:.0f} K", (t1, 1), xytext=(t1 + 22, 1e-6), fontsize=6.6, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6))
    ax.annotate(f"CO₂ stable\nbelow ≈ {t2:.0f} K", (t2, 1), xytext=(27, 1e4), fontsize=6.6, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))
    ax.set_yscale("log")
    ax.set_ylim(1e-12, 1e18)
    ax.set_xlim(25, 400)
    ax.set_xlabel("Surface temperature (K)", fontsize=7.8)
    ax.set_ylabel("Sublimation loss of exposed ice (m per 10⁹ years)", fontsize=7.4)
    ax.legend(loc="lower right", fontsize=6.8, bbox_to_anchor=(0.99, 0.2))
    fig.text(0.99, 0.01, "Free sublimation into vacuum (Hertz–Knudsen) with ice vapour pressure from Murphy & Koop (2005) and "
             "CO₂ from Clausius–Clapeyron; a regolith cover slows the loss further.", ha="right", va="bottom",
             fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch41_icestab")


# ---------------------------------------------------------------------------------------------
# 4. ISRU process chains (schematic)
# ---------------------------------------------------------------------------------------------
def isruflow():
    fig, ax = canvas(7.0, 4.6, xlim=(0, 100), ylim=(0, 66))
    lanes = [(46, "LUNAR POLAR ICE", BLUE, "#E6F0FA"), (24, "LUNAR REGOLITH", ORANGE, "#FFF1E0"),
             (2, "MARS ATMOSPHERE\nAND ICE", RED, "#F8E4E6")]
    for y0, name, col, fc in lanes:
        ax.add_patch(FancyBboxPatch((0.5, y0), 99, 19, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec="none", zorder=0))
        label(ax, 6.5, y0 + 9.5, name, fs=6.4, color=col, weight="bold", rot=90)
    # lane 1 — water ice to LOX/LH2
    s1 = [(10, "Excavate or drill\nicy regolith\n(40–100 K)"), (26, "Heat to\n150–400 K;\nice sublimes"),
          (42, "Cold-trap\nvapour; clean\nthe water"), (58, "Electrolysis\n2H₂O → 2H₂ + O₂\n(≈ 16 MJ/kg)"),
          (74, "Liquefy and\nstore LOX\nand LH₂")]
    for x, t in s1:
        box(ax, x, 49, 14, 13, t, fc="white", ec=BLUE, fs=6.1)
    for i in range(4):
        arrow(ax, (s1[i][0] + 14.1, 55.5), (s1[i + 1][0] - 0.1, 55.5), color=BLUE, lw=1.0)
    arrow(ax, (88.1, 55.5), (90.5, 55.5), color=BLUE, lw=1.0)
    label(ax, 95.2, 55.5, "propellant,\nwater,\nbreathing\noxygen", fs=5.9, color=BLUE, ha="center")
    # lane 2 — regolith to oxygen and metals
    box(ax, 10, 30, 15, 11, "Excavate and\nsort (sieve,\nmagnetic)", fc="white", ec=ORANGE, fs=6.1)
    procs = ["H₂ reduction of ilmenite, 900–1 050 °C", "Carbothermal (CH₄), molten zone > 1 600 °C",
             "Molten regolith electrolysis, ≈ 1 600 °C", "Molten salt (FFC) electrolysis, ≈ 900 °C"]
    for k, t in enumerate(procs):
        box(ax, 29, 37.6 - k * 3.6, 34, 3.1, t, fc="white", ec=ORANGE, fs=5.9, r=0.6)
    arrow(ax, (25.1, 35.5), (28.9, 35.5), color=ORANGE, lw=1.0)
    box(ax, 68, 34.5, 14, 6.5, "Oxygen (O₂)", fc=ORANGE, ec=ORANGE, fs=6.4, color="white", weight="bold")
    box(ax, 68, 26.5, 14, 6.5, "Fe, Si, Al, Ti\nmetals and slag", fc="white", ec=ORANGE, fs=6.0)
    arrow(ax, (63.1, 36.5), (67.9, 37.5), color=ORANGE, lw=1.0)
    arrow(ax, (63.1, 29.5), (67.9, 29.5), color=ORANGE, lw=1.0)
    label(ax, 91.5, 37.7, "oxidiser,\nlife support", fs=5.9, color=ORANGE)
    label(ax, 91.5, 29.7, "structures,\nsolar cells,\nshielding", fs=5.9, color=ORANGE)
    # lane 3 — Mars
    box(ax, 10, 11.5, 16, 8.5, "Filter and\ncompress CO₂\n0.6 → ≈ 100 kPa", fc="white", ec=RED, fs=5.9)
    box(ax, 30, 11.5, 21, 8.5, "Solid-oxide electrolysis\nat 800 °C (MOXIE)\n2CO₂ → 2CO + O₂", fc="white", ec=RED, fs=5.9)
    box(ax, 10, 3, 16, 6.5, "Mine ice; electrolyse\nwater to make H₂", fc="white", ec=RED, fs=5.9)
    box(ax, 30, 3, 21, 6.5, "Sabatier, 300–400 °C\nCO₂ + 4H₂ → CH₄ + 2H₂O", fc="white", ec=RED, fs=5.9)
    arrow(ax, (26.1, 15.7), (29.9, 15.7), color=RED, lw=1.0)
    arrow(ax, (26.1, 6.2), (29.9, 6.2), color=RED, lw=1.0)
    arrow(ax, (26.1, 12.2), (31.5, 9.6), color=RED, lw=0.8, ms=7)
    label(ax, 28.0, 9.6, "CO₂", fs=5.6, color=RED)
    box(ax, 55, 13.0, 14, 6.0, "Oxygen (O₂)", fc=RED, ec=RED, fs=6.4, color="white", weight="bold")
    box(ax, 55, 3.25, 14, 6.0, "Methane (CH₄)", fc=RED, ec=RED, fs=6.4, color="white", weight="bold")
    arrow(ax, (51.1, 15.7), (54.9, 16.0), color=RED, lw=1.0)
    arrow(ax, (51.1, 6.2), (54.9, 6.2), color=RED, lw=1.0)
    label(ax, 84.5, 11.0, "Return propellant: a CH₄/O₂ ascent\nstage burns ≈ 3.6 kg O₂ per kg CH₄,\n"
          "so oxygen from CO₂ alone supplies\n≈ 78 % of the propellant mass",
          fs=5.8, color=INK)
    save(fig, "ch41_isruflow")


# ---------------------------------------------------------------------------------------------
# 5. Energy to extract water from icy regolith
# ---------------------------------------------------------------------------------------------
def cp_regolith(T):
    """Specific heat of lunar regolith (J/kg/K): Hayne et al. (2017) polynomial to 350 K, linear above."""
    T = np.asarray(T, float)
    c = -3.6125 + 2.7431 * T + 2.3616e-3 * T ** 2 - 1.2340e-5 * T ** 3 + 8.9093e-9 * T ** 4
    c350 = -3.6125 + 2.7431 * 350 + 2.3616e-3 * 350 ** 2 - 1.2340e-5 * 350 ** 3 + 8.9093e-9 * 350 ** 4
    return np.where(T < 350, c, c350 + 0.5 * (T - 350))


def heat(cpf, t0, t1, n=2000):
    T = np.linspace(t0, t1, n)
    return np.trapezoid(cpf(T), T)          # J/kg


L_SUB = 2.83e6       # J/kg, sublimation enthalpy of ice


def ice_energy_parts(w, t_end, t0=40.0):
    reg = (1 - w) / w * heat(cp_regolith, t0, t_end)
    ice = heat(lambda T: 7.73 * np.minimum(T, 273.0), t0, t_end)
    return reg / 1e6, ice / 1e6, L_SUB / 1e6


def iceenergy():
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.2), gridspec_kw=dict(width_ratios=[1.15, 1.0]))
    w = np.linspace(0.01, 0.30, 300)
    for t_end, col, lab in [(250, BLUE, "heat to 250 K (−23 °C)"), (373, ORANGE, "heat to 373 K (100 °C)")]:
        e = np.array([sum(ice_energy_parts(x, t_end)) for x in w])
        a.plot(100 * w, e, color=col, lw=1.8, label=lab)
        a.plot(100 * w, e / 0.5, color=col, lw=1.0, ls="--")
    a.axhline(15.9, color=GREY, lw=0.8, ls=":")
    a.text(29.5, 16.6, "electrolysis of 1 kg water (ideal)", fontsize=6.2, color=GREY, ha="right")
    a.text(6.2, 33, "dashed: 50 % of the\nheat reaches the ice", fontsize=6.2, color=INK)
    e5 = sum(ice_energy_parts(0.05, 250))
    a.plot([5], [e5], "o", color=BLUE, ms=4)
    a.annotate(f"5 % ice: {e5:.1f} MJ/kg", (5, e5), xytext=(9.5, 1.0), fontsize=6.4, color=BLUE,
               arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6))
    a.set_xlim(0, 30)
    a.set_ylim(0, 45)
    a.set_xlabel("Ice content of regolith (% by mass)", fontsize=7.6)
    a.set_ylabel("Thermal energy per kg of water (MJ)", fontsize=7.6)
    a.set_title("(a) Energy versus ice content", fontsize=8.6)
    a.legend(loc="upper right", fontsize=6.4)

    cases = [0.02, 0.05, 0.10, 0.30]
    parts = np.array([ice_energy_parts(c, 250) for c in cases])
    x = np.arange(len(cases))
    bottoms = np.zeros(len(cases))
    for k, (lab, col) in enumerate([("heating regolith", "#B9A47E"), ("heating ice", SKY), ("sublimation", BLUE)]):
        b.bar(x, parts[:, k], bottom=bottoms, color=col, width=0.62, label=lab, zorder=2)
        bottoms += parts[:, k]
    for xi, tot, c in zip(x, bottoms, cases):
        b.text(xi, tot + 0.15, f"{tot:.1f}", ha="center", va="bottom", fontsize=6.6)
    b.set_xticks(x)
    b.set_xticklabels([f"{100 * c:.0f} % ice\n({(1 - c) / c:.0f} kg)" for c in cases], fontsize=6.8)
    b.set_ylim(0, 9)
    b.set_ylabel("MJ per kg of water", fontsize=7.6)
    b.set_title("(b) Where the energy goes (250 K)", fontsize=8.6)
    b.grid(axis="x", visible=False)
    b.legend(loc="upper right", fontsize=6.4)
    b.set_xlabel("Ice content (regolith processed per kg of water)", fontsize=7.4)
    fig.text(0.99, 0.01, "Regolith starts at 40 K; specific heat from Hayne et al. (2017), ice c ≈ 7.7·T J/(kg·K), "
             "sublimation 2.83 MJ/kg.\nSolid lines assume all heat reaches the feedstock and all vapour is captured.",
             ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    save(fig, "ch41_iceenergy")


# ---------------------------------------------------------------------------------------------
# 6. Oxygen from regolith: yield and energy by process
# ---------------------------------------------------------------------------------------------
DHF = {"SiO2": 910.7, "TiO2": 944.0, "Al2O3": 1675.7, "FeO": 272.0, "MgO": 601.6, "CaO": 635.1, "Na2O": 418.0,
       "K2O": 361.5, "Cr2O3": 1139.7, "MnO": 385.2}          # -ΔHf at 298 K, kJ/mol
HIGHLAND = {"SiO2": 45.0, "TiO2": 0.54, "Al2O3": 27.3, "FeO": 5.1, "MgO": 5.7, "CaO": 15.7, "Na2O": 0.47, "K2O": 0.11}
MARE = {"SiO2": 42.2, "TiO2": 7.8, "Al2O3": 13.6, "FeO": 15.3, "MgO": 7.8, "CaO": 11.9, "Na2O": 0.47, "K2O": 0.16,
        "Cr2O3": 0.3, "MnO": 0.2}


def o2_from(soil, oxides, frac=1.0):
    """kg O2 per tonne and reaction enthalpy (MJ) per tonne for reducing the listed oxides completely."""
    tot = sum(soil.values())
    m_o, e = 0.0, 0.0
    for k in oxides:
        mm, _, _, no = OXIDE[k]
        mol = soil[k] / tot * 1e6 / mm * frac       # mol per tonne
        m_o += mol * no * 15.999e-3
        e += mol * DHF[k] * 1e-3                    # MJ
    return m_o, e


def o2yield():
    ilm_wt = {"highland": 1.0, "mare": 10.0}           # ilmenite, % by mass
    procs = ["H₂, ilmenite\nonly", "H₂, all FeO\n(limit)", "Carbo-\nthermal", "Molten salt\n(FFC)",
             "Molten\nregolith\nelectrolysis"]

    def yields(soil, key):
        ilm = ilm_wt[key] * 10.0 / 151.71 * 0.9          # kmol ilmenite reduced per tonne (90 %)
        y_ilm = ilm * 15.999                              # kg O per tonne
        e_ilm = ilm * 288.0                               # MJ (FeTiO3 -> Fe + TiO2 + 1/2 O2)
        y_feo, e_feo = o2_from(soil, ["FeO"])
        y_cb, e_cb = o2_from(soil, ["FeO", "TiO2", "SiO2"])
        y_all, e_all = o2_from(soil, list(soil.keys()))
        y_ffc, e_ffc = 0.96 * y_all, 0.96 * e_all
        return [(y_ilm, e_ilm), (y_feo, e_feo), (y_cb, e_cb), (y_ffc, e_ffc), (y_all, e_all)]

    hy = yields(HIGHLAND, "highland")
    my = yields(MARE, "mare")
    # sensible heat per tonne from 250 K to process temperature (+ fusion 0.48 MJ/kg if molten)
    t_proc = [1300, 1300, 1900, 1200, 1900]
    molten = [False, False, True, False, True]
    q = [heat(cp_regolith, 250, t) / 1e3 + (480 if m else 0) for t, m in zip(t_proc, molten)]   # MJ per tonne

    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.0, 1.0]))
    x = np.arange(len(procs))
    a.bar(x - 0.19, [v[0] for v in hy], width=0.36, color=SKY, label="highland soil (1 % ilmenite)", zorder=2)
    a.bar(x + 0.19, [v[0] for v in my], width=0.36, color=NAVY, label="mare soil (10 % ilmenite)", zorder=2)
    for xi, (h, m) in enumerate(zip(hy, my)):
        a.text(xi - 0.19, h[0] * 1.12, f"{h[0]:.0f}", ha="center", va="bottom", fontsize=5.9, color=BLUE)
        a.text(xi + 0.19, m[0] * 1.12, f"{m[0]:.0f}", ha="center", va="bottom", fontsize=5.9, color=NAVY)
    a.set_yscale("log")
    a.set_ylim(0.5, 2000)
    a.set_xticks(x)
    a.set_xticklabels(procs, fontsize=5.9)
    a.set_ylabel("Oxygen per tonne of regolith (kg)", fontsize=7.4)
    a.set_title("(a) Theoretical oxygen yield", fontsize=8.6)
    a.grid(axis="x", visible=False)
    a.legend(loc="upper left", fontsize=6.2)

    react = [m[1] / m[0] for m in my]
    sens = [qq / m[0] for qq, m in zip(q, my)]
    b.bar(x, react, width=0.6, color=ORANGE, label="breaking the oxide bonds (minimum)", zorder=2)
    b.bar(x, sens, bottom=react, width=0.6, color="#B9A47E", label="heating the regolith (no heat recovery)", zorder=2)
    for xi, r_, s_ in zip(x, react, sens):
        tot = r_ + s_
        b.text(xi, tot + 2, f"{tot:.0f}", ha="center", va="bottom", fontsize=6.4)
    b.set_ylim(0, 160)
    b.set_xticks(x)
    b.set_xticklabels(procs, fontsize=5.9)
    b.set_ylabel("Energy per kg of oxygen (MJ)", fontsize=7.4)
    b.set_title("(b) Energy per kg O₂, mare soil", fontsize=8.6)
    b.grid(axis="x", visible=False)
    b.legend(loc="upper right", fontsize=6.2)
    fig.text(0.99, 0.01, "Typical Apollo 16 and Apollo 11 soil oxides; 90 % of ilmenite reduced; reaction energy = enthalpy of "
             "formation of the reduced oxides (298 K).\nProcess temperatures 1 300 K (H₂), 1 200 K (FFC), 1 900 K (molten); "
             "fusion 0.48 MJ/kg. Real plants add electrical and thermal\nlosses, and can recover much of the sensible heat.",
             ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    save(fig, "ch41_o2yield")


# ---------------------------------------------------------------------------------------------
# 7. Accessibility of near-Earth asteroids
# ---------------------------------------------------------------------------------------------
# Δv from a 400 km circular LEO, computed for all 42 782 NEAs in the JPL Small-Body Database (queried 19 Oct 2026):
# two-impulse transfer from 1 AU to the asteroid's aphelion (or perihelion if Q < 1 AU), departure burn from LEO
# (Oberth), rendezvous burn matching speed; the inclination change is split optimally between the two burns.
# Phasing, node location and launch windows are ignored (in the spirit of Shoemaker & Helin 1978).
NEA_EDGES = np.arange(3.0, 12.01, 0.25)
NEA_ALL = [8, 109, 299, 492, 773, 1000, 1266, 1480, 1738, 1984, 2443, 2994, 3230, 2937, 2534, 1915, 1689, 1437, 1330,
           1098, 1061, 933, 923, 775, 770, 740, 687, 603, 585, 487, 463, 404, 367, 385, 312, 2531]
NEA_H22 = [0, 0, 1, 6, 15, 25, 34, 63, 109, 151, 214, 313, 551, 727, 750, 619, 563, 522, 505, 434, 447, 405, 432, 381,
           371, 377, 336, 289, 304, 246, 214, 189, 185, 210, 162, 1608]
NEA_H1775 = [0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 7, 12, 26, 37, 43, 43, 33, 38, 33, 27, 30, 22, 32, 33, 27, 31, 35, 28, 29, 23,
             18, 13, 26, 11, 17, 195]
NAMED = [("2022 OB5", 3.51), ("Itokawa", 4.10), ("Ryugu", 4.13), ("Bennu", 4.55), ("Didymos", 4.63),
         ("Kamoʻoalewa", 4.67), ("Apophis", 5.49), ("Eros", 5.87)]


def neadv():
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.25, 1.0]))
    e = NEA_EDGES
    a.stairs(NEA_ALL, e, fill=True, color=SKY, alpha=0.75, label=f"all known NEAs ({sum(NEA_ALL):,})".replace(",", " "))
    a.stairs(NEA_H22, e, fill=True, color=NAVY, alpha=0.85,
             label=f"larger than ≈ 140 m ({sum(NEA_H22):,})".replace(",", " "))
    for v, t in [(4.0, "LEO → low\nlunar orbit "), (5.9, "LEO → lunar\nsurface ")]:
        a.axvline(v, color=ORANGE, lw=1.0, ls="--")
        a.text(v - 0.07, 3530, t, va="top", ha="right", fontsize=6.2, color=ORANGE, linespacing=1.05)
    a.text(8.3, 2150, "Δv of some targets (km/s)\n2022 OB5 3.5 · Itokawa 4.1\nRyugu 4.1 · Bennu 4.6\n"
           "Didymos 4.6 · Kamoʻoalewa 4.7\nApophis 5.5 · Eros 5.9", fontsize=6.0, color=INK, va="top", ha="left",
           linespacing=1.35, bbox=dict(fc="white", ec="#D5DDE5", pad=3.0))
    a.text(11.85, 2650, "≥ 11.75", ha="right", fontsize=5.8, color=GREY)
    a.set_xlim(3, 12)
    a.set_ylim(0, 3600)
    a.set_yticks(range(0, 3001, 500))
    a.set_xlabel("Δv from low Earth orbit to rendezvous (km/s)", fontsize=7.6)
    a.set_ylabel("Number of asteroids per 0.25 km/s", fontsize=7.6)
    a.set_title("(a) Distribution of rendezvous Δv", fontsize=8.6)
    a.legend(loc="upper right", fontsize=6.3)

    mid = e[1:]
    for data, col, lab in [(NEA_ALL, SKY, "all"), (NEA_H22, NAVY, "> 140 m"), (NEA_H1775, RED, "> 1 km")]:
        c = np.cumsum(data)
        b.step(mid, c, where="post", color=col, lw=1.6, label=lab)
    b.set_yscale("log")
    b.set_xlim(3, 8)
    b.set_ylim(1, 1e5)
    b.axvline(4.0, color=ORANGE, lw=1.0, ls="--")
    b.axvline(5.9, color=ORANGE, lw=1.0, ls="--")
    b.set_xlabel("Δv from low Earth orbit (km/s)", fontsize=7.6)
    b.set_ylabel("Number of NEAs below this Δv", fontsize=7.6)
    b.set_title("(b) Cumulative, by size", fontsize=8.6)
    b.legend(loc="lower right", fontsize=6.4)
    fig.text(0.99, 0.01, "42 782 NEAs from the JPL Small-Body Database (19 Oct 2026). Idealised two-impulse transfer from a "
             "400 km orbit to the asteroid's aphelion,\nplane change split optimally; phasing and launch windows ignored. "
             "Size from absolute magnitude H (≤ 22 ≈ 140 m, ≤ 17.75 ≈ 1 km,\nalbedo 0.14). Real missions usually need more Δv; "
             "Earth and lunar flybys can reduce it.", ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    save(fig, "ch41_neadv")


# ---------------------------------------------------------------------------------------------
# 8. Economics: what extra supply does to price and revenue
# ---------------------------------------------------------------------------------------------
def economics():
    p0 = 53.0          # US$ thousand per kg (≈ US$ 1 650 per troy ounce, mid-October 2026)
    s0 = 170.0         # tonnes per year mined platinum
    x = np.linspace(0, 500, 501)
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.1))
    for eps, col in [(0.3, RED), (0.6, ORANGE), (1.0, BLUE)]:
        price = p0 * (1 + x / s0) ** (-1 / eps)
        rev = x * 1e3 * price * 1e3 / 1e9          # US$ billion per year
        a.plot(x, price, color=col, lw=1.7, label=f"demand elasticity {eps:.1f}")
        b.plot(x, rev, color=col, lw=1.7, label=f"elasticity {eps:.1f}")
        if eps < 1:
            xm = s0 * eps / (1 - eps)
            rm = xm * 1e3 * p0 * (1 + xm / s0) ** (-1 / eps) * 1e3 / 1e9
            b.plot([xm], [rm], "o", color=col, ms=4)
            b.annotate(f"max US\\$ {rm:.1f} bn\nat {xm:.0f} t/yr", (xm, rm), xytext=(xm + (70 if eps > 0.5 else 40), rm + (1.1 if eps > 0.5 else 0.4)),
                       fontsize=6.2, va="bottom", color=col, arrowprops=dict(arrowstyle="-", color=col, lw=0.6))
    b.plot(x, x * p0 / 1e3, color=GREY, lw=1.0, ls="--", label="if price did not fall")
    a.axvline(s0, color=GREY, lw=0.8, ls=":")
    a.text(s0 + 6, 41, "added supply =\ntoday's world\nmine output", fontsize=6.2, color=GREY, va="top")
    a.set_xlim(0, 500)
    a.set_ylim(0, 60)
    a.set_xlabel("Platinum added by space mining (t/yr)", fontsize=7.6)
    a.set_ylabel("Market price (US\\$ thousand per kg)", fontsize=7.6)
    a.set_title("(a) Price falls as supply grows", fontsize=8.6)
    a.legend(loc="upper right", fontsize=6.3)
    b.set_xlim(0, 500)
    b.set_ylim(0, 10)
    b.set_xlabel("Platinum added by space mining (t/yr)", fontsize=7.6)
    b.set_ylabel("Miner's revenue (US\\$ billion per year)", fontsize=7.6)
    b.set_title("(b) Revenue saturates", fontsize=8.6)
    b.legend(loc="upper right", fontsize=6.2)
    fig.text(0.99, 0.01, "Illustrative constant-elasticity demand P = P₀(1 + X/S₀)^(−1/ε) with P₀ = US\\$ 53 000/kg "
             "(≈ US\\$ 1 650 per troy ounce, mid-October 2026; the price ranged\nfrom about US\\$ 1 540 to 2 920 per ounce during 2026) "
             "and S₀ = 170 t/yr (world mine supply, WPIC 2025).",
             ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, "ch41_economics")


if __name__ == "__main__":
    fns = [gear, composition, icestab, isruflow, iceenergy, o2yield, neadv, economics]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
