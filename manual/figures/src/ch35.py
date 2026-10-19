"""Figures for Chapter 35 - Rocket Propulsion.

Computed figures rest on the ideal-rocket (isentropic, frozen-gamma) relations, on shifting-equilibrium
thermochemistry computed once with an equilibrium code (Cantera 3.2 with the NASA Glenn thermodynamic data,
reactant enthalpies from NASA CEA; results embedded below), on solid-motor ballistics (r = a p^n) with a
level-set burn-back of the grain cross-section, and on published engine data (notes/currency/ch35.md).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

G0 = 9.80665


# ----------------------------------------------------------------------------- ideal-rocket relations
def area_ratio(M, g):
    return (1.0 / M) * ((2.0 / (g + 1)) * (1 + 0.5 * (g - 1) * M ** 2)) ** ((g + 1) / (2 * (g - 1)))


def mach_from_area(eps, g, supersonic=True):
    lo, hi = (1.0, 50.0) if supersonic else (1e-6, 1.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = area_ratio(mid, g) - eps
        if supersonic:
            lo, hi = (mid, hi) if f < 0 else (lo, mid)
        else:
            lo, hi = (lo, mid) if f < 0 else (mid, hi)
    return 0.5 * (lo + hi)


def pe_over_pc(eps, g):
    M = mach_from_area(eps, g)
    return (1 + 0.5 * (g - 1) * M ** 2) ** (-g / (g - 1))


def cf(eps, g, pc, pa):
    pr = pe_over_pc(eps, g)
    mom = np.sqrt(2 * g ** 2 / (g - 1) * (2 / (g + 1)) ** ((g + 1) / (g - 1)) * (1 - pr ** ((g - 1) / g)))
    return mom + (pr - pa / pc) * eps, pr * pc


def isa_pressure(h_km):
    """US Standard Atmosphere 1976 pressure (Pa), 0-86 km (layer formulae)."""
    h = np.atleast_1d(np.asarray(h_km, float))
    layers = [(0, 288.15, -6.5, 101325.0), (11, 216.65, 0.0, 22632.06), (20, 216.65, 1.0, 5474.889),
              (32, 228.65, 2.8, 868.0187), (47, 270.65, 0.0, 110.9063), (51, 270.65, -2.8, 66.93887),
              (71, 214.65, -2.0, 3.956420)]
    gmr = 34.1632  # g0*M/R in K/km
    out = np.zeros_like(h)
    for i, hh in enumerate(h):
        for j in range(len(layers) - 1, -1, -1):
            hb, Tb, L, pb = layers[j]
            if hh >= hb:
                break
        if L == 0:
            out[i] = pb * np.exp(-gmr * (hh - hb) / Tb)
        else:
            out[i] = pb * (Tb / (Tb + L * (hh - hb))) ** (gmr / L)
    return out


# ----------------------------------------------------------------------------- equilibrium data
# Theoretical performance, shifting equilibrium, infinite-area combustor, pc = 6.895 MPa (1 000 psia).
# isl: optimum expansion to 1 atm; ivac: vacuum with expansion ratio 50; tc: chamber temperature (K).
THERMO = {
    'LOX/LH2': dict(mr=[2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5,
                        6.75, 7.0, 7.25, 7.5, 7.75, 8.0],
                    tc=[2143, 2302, 2451, 2591, 2720, 2839, 2948, 3046, 3135, 3215, 3286, 3348, 3403, 3449, 3488, 3520,
                        3546, 3565, 3579, 3589, 3594, 3596, 3595],
                    ivac=[439.8, 444.5, 448.3, 451.4, 453.8, 455.7, 457.0, 458.0, 458.6, 458.9, 458.8, 458.5, 458.0,
                          457.2, 456.1, 454.9, 453.4, 451.7, 449.7, 447.5, 444.9, 441.7, 437.9]),
    'LOX/CH₄': dict(mr=[2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8,
                        3.9, 4.0, 4.1, 4.2],
                    tc=[2553, 2699, 2834, 2957, 3067, 3165, 3250, 3322, 3383, 3432, 3471, 3501, 3524, 3541, 3553, 3560,
                        3565, 3567, 3566, 3564, 3561, 3556, 3550],
                    ivac=[332.3, 337.8, 343.1, 347.9, 352.2, 356.0, 359.4, 362.4, 365.0, 367.2, 369.1, 370.5, 371.6,
                          372.4, 372.8, 372.8, 372.4, 371.6, 370.4, 368.8, 367.1, 365.2, 363.3]),
    'LOX/RP-1': dict(mr=[1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4],
                     tc=[2714, 2905, 3074, 3219, 3341, 3440, 3518, 3577, 3621, 3652, 3674, 3688, 3697, 3701, 3702, 3701,
                         3697, 3692, 3686],
                     ivac=[316.8, 324.4, 331.4, 337.7, 343.1, 347.7, 351.6, 354.8, 357.4, 359.4, 360.8, 361.6, 361.8,
                           361.4, 360.5, 359.2, 357.6, 355.9, 354.1]),
    'NTO/MMH': dict(mr=[1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5],
                    tc=[2365, 2532, 2684, 2822, 2945, 3054, 3146, 3224, 3285, 3330, 3362, 3382, 3392, 3394, 3390, 3382],
                    ivac=[307.4, 312.4, 317.2, 321.7, 325.8, 329.5, 332.8, 335.6, 338.0, 340.1, 341.8, 343.1, 344.1,
                          344.7, 344.8, 343.8]),
    'NTO/UDMH': dict(mr=[1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0],
                     tc=[2277, 2439, 2589, 2726, 2851, 2964, 3064, 3152, 3226, 3287, 3335, 3372, 3398, 3416, 3426, 3431,
                         3431, 3427, 3420],
                     ivac=[300.1, 305.0, 309.7, 314.1, 318.2, 322.1, 325.6, 328.8, 331.5, 333.9, 336.1, 337.9, 339.4,
                           340.6, 341.6, 342.3, 342.6, 342.6, 342.1]),
}
# typical engine mixture ratios (marked) and liquid densities (kg/m3)
TYPICAL_MR = {'LOX/LH2': 6.0, 'LOX/CH₄': 3.6, 'LOX/RP-1': 2.6, 'NTO/MMH': 2.0, 'NTO/UDMH': 2.6}
DENS = {'LOX/LH2': (1141, 70.8), 'LOX/CH₄': (1141, 422.6), 'LOX/RP-1': (1141, 810), 'NTO/MMH': (1443, 874),
        'NTO/UDMH': (1443, 791)}
SHOW = {'LOX/LH2': 'LOX/LH₂'}
PCOL = {'LOX/LH2': BLUE, 'LOX/CH₄': GREEN, 'LOX/RP-1': ORANGE, 'NTO/MMH': VIOLET, 'NTO/UDMH': RED}


# ----------------------------------------------------------------------------- 1. nozzle flow
def nozzleflow():
    fig = plt.figure(figsize=(7.0, 3.5))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.15], height_ratios=[0.8, 2.0], wspace=0.30, hspace=0.06)
    ax = fig.add_subplot(gs[:, 0])
    for g, c in [(1.13, RED), (1.2, BLUE), (1.3, GREEN), (1.4, GREY)]:
        Ms = np.linspace(0.06, 6.0, 600)
        ax.plot(Ms, area_ratio(Ms, g), color=c, lw=1.4, label=f"γ = {g}")
    ax.set_yscale("log")
    ax.set_ylim(0.9, 400)
    ax.set_xlim(0, 6)
    ax.axvline(1, color=GREY, lw=0.7, ls=":")
    ax.text(0.5, 70, "subsonic\n(converging)", ha="center", va="center", fontsize=6.1, color=GREY)
    ax.text(1.15, 25, "supersonic\n(diverging)", ha="left", va="center", fontsize=6.1, color=GREY)
    for name, eps in [("Merlin 1D, ε = 16", 16), ("RS-25, ε = 69", 69), ("RL10B-2, ε = 280", 280)]:
        M = mach_from_area(eps, 1.2)
        ax.plot(M, eps, "o", color=NAVY, ms=4, zorder=5)
        if eps < 200:
            ax.text(M + 0.15, eps * 0.80, name, ha="left", va="top", fontsize=6.3, color=NAVY,
                    bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.9), zorder=6)
        else:
            ax.annotate(name, (M - 0.1, eps), (1.15, eps), fontsize=6.3, color=NAVY, va="center",
                        arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.6))
    ax.set_xlabel("Mach number M")
    ax.set_ylabel("Area ratio A/A*")
    ax.legend(loc="lower right", fontsize=6.6, frameon=False)
    ax.set_title("(a) Area–Mach relation", loc="left", fontsize=8.6)

    # (b) flow along a nozzle, gamma = 1.2, contraction 3, expansion 40
    g = 1.2
    xs = np.linspace(-1.0, 4.0, 700)
    rt = 0.5

    def radius(x):
        if x < 0:   # converging section, contraction ratio 3
            return rt * (1 + (np.sqrt(3) - 1) * (np.sin(np.pi / 2 * min(-x, 1.0))) ** 1.2)
        return rt * (1 + (np.sqrt(40) - 1) * (1 - (1 - x / 4.0) ** 1.9))  # bell-like divergent section
    r = np.array([radius(x) for x in xs])
    A = (r / rt) ** 2
    M = np.array([mach_from_area(a, g, supersonic=(x > 0)) if a > 1.0005 else 1.0 for a, x in zip(A, xs)])
    T = 1 / (1 + 0.5 * (g - 1) * M ** 2)
    p = T ** (g / (g - 1))
    v = np.sqrt(1 - T)    # fraction of limiting velocity
    axn = fig.add_subplot(gs[0, 1])
    axn.fill_between(xs, r, -r, color="#DCE6F0")
    axn.plot(xs, r, color=NAVY, lw=1.2)
    axn.plot(xs, -r, color=NAVY, lw=1.2)
    axn.fill_between([-1.6, -1.0], [r[0], r[0]], [-r[0], -r[0]], color="#F4D9C6")
    axn.text(-1.3, 0, "chamber", ha="center", va="center", fontsize=6.0, color=INK, rotation=90)
    axn.annotate("throat", (0, rt), (0.4, 1.9), fontsize=6.4, ha="left", color=INK,
                 arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    axn.text(3.95, 0, "exit, ε = 40", ha="right", va="center", fontsize=6.4, color=NAVY)
    axn.set_xlim(-1.6, 4.0)
    axn.set_ylim(-3.4, 3.4)
    axn.axis("off")
    axn.set_title("(b) Flow through a nozzle (γ = 1.2)", loc="left", fontsize=8.6)
    axb = fig.add_subplot(gs[1, 1], sharex=axn)
    axb.plot(xs, p, color=BLUE, lw=1.4, label="pressure p/pc")
    axb.plot(xs, T, color=RED, lw=1.4, label="temperature T/Tc")
    axb.plot(xs, v, color=GREEN, lw=1.4, label="velocity v/v_max")
    axb.axvline(0, color=GREY, lw=0.7, ls=":")
    axb.set_ylim(0, 1.05)
    axb.set_ylabel("Fraction of chamber value")
    axb.set_xlabel("Axial distance from throat (throat diameters)")
    ax2 = axb.twinx()
    ax2.plot(xs, M, color=NAVY, lw=1.2, ls="--", label="Mach number")
    ax2.set_ylim(0, 4.6)
    ax2.set_ylabel("Mach number", color=NAVY)
    ax2.spines["right"].set_visible(True)
    h1, l1 = axb.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    axb.legend(h1 + h2, l1 + l2, loc="center right", fontsize=6.2, frameon=True, framealpha=0.95,
               bbox_to_anchor=(1.0, 0.585), edgecolor="none")
    fig.text(0.99, 0.01, "Isentropic flow of a perfect gas with constant γ; at the throat M = 1, p/pc = 0.56, "
             "T/Tc = 0.91. Expansion ratios of real engines marked on the γ = 1.2 curve.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.subplots_adjust(left=0.08, right=0.93, top=0.92, bottom=0.18)
    save(fig, "ch35_nozzleflow")


# ----------------------------------------------------------------------------- 2. altitude / expansion
def altitude():
    g, pc, cstar = 1.2, 10e6, 1800.0
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.3))
    eps = np.logspace(np.log10(2), np.log10(300), 400)
    for pa, c, lab in [(0.0, NAVY, "vacuum"), (0.3 * 101325, GREEN, "0.3 atm (≈ 9 km)"), (101325.0, ORANGE, "1 atm (sea level)")]:
        vals = np.array([cf(e, g, pc, pa) for e in eps])
        isp = cstar * vals[:, 0] / G0
        pe = vals[:, 1]
        ok = pe >= 0.4 * pa
        ax.plot(eps[ok], isp[ok], color=c, lw=1.5, label=lab)
        if (~ok).any():
            ax.plot(eps[~ok], isp[~ok], color=c, lw=1.0, ls=":")
            j = np.argmax(isp)
            ax.plot(eps[j], isp[j], "o", color=c, ms=4)
            xe = eps[~ok][0]
            ax.plot(xe, isp[~ok][0], "x", color=c, ms=5, mew=1.2)
    ax.set_xscale("log")
    ax.set_xlim(2, 300)
    ax.set_ylim(220, 380)
    ax.set_xlabel("Expansion ratio ε = Ae/At")
    ax.set_ylabel("Specific impulse (s)")
    ax.legend(loc="upper left", fontsize=6.5, frameon=False)
    ax.text(2.2, 224, "●  best ε: exit pressure = ambient\n×  separation expected (pe < 0.4 pa);\n    dotted: ideal, attached flow",
            fontsize=6.2, color=INK, va="bottom")
    ax.set_title("(a) Isp versus expansion ratio", loc="left", fontsize=8.6)

    h = np.linspace(0, 60, 400)
    pa = isa_pressure(h)
    for e, c, lab in [(16, ORANGE, "ε = 16 (sea-level nozzle)"), (40, GREEN, "ε = 40"), (165, BLUE, "ε = 165 (vacuum nozzle)")]:
        vals = np.array([cf(e, g, pc, p) for p in pa])
        isp = cstar * vals[:, 0] / G0
        pe = vals[:, 1]
        ok = pe >= 0.4 * pa
        ax2.plot(h[ok], isp[ok], color=c, lw=1.5, label=lab)
        if (~ok).any():
            ax2.plot(h[~ok], isp[~ok], color=c, lw=1.0, ls=":")
    # ideal altitude-compensating nozzle: pe = pa (capped at eps 165)
    env = []
    for p in pa:
        best = max(cf(e, g, pc, p)[0] for e in np.logspace(0.3, np.log10(165), 120))
        env.append(cstar * best / G0)
    ax2.plot(h, env, color=GREY, lw=1.0, ls="--", label="ideal adaptive nozzle (ε ≤ 165)")
    ax2.set_xlim(0, 60)
    ax2.set_ylim(150, 380)
    ax2.set_xlabel("Altitude (km)")
    ax2.set_ylabel("Specific impulse (s)")
    ax2.legend(loc="lower right", fontsize=6.4, frameon=False)
    ax2.text(7.0, 225, "dotted: flow\nwould separate", fontsize=6.2, color=BLUE, va="center")
    ax2.set_title("(b) Isp during ascent", loc="left", fontsize=8.6)
    fig.text(0.99, 0.01, "Ideal rocket, γ = 1.2, chamber pressure 10 MPa, c* = 1 800 m/s (typical of LOX/RP-1 or LOX/CH₄); "
             "US Standard Atmosphere; Summerfield separation criterion pe ≈ 0.4 pa.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch35_altitude")


# ----------------------------------------------------------------------------- 3. propellant performance
def propellants():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.1))
    for k, d in THERMO.items():
        c = PCOL[k]
        ax.plot(d["mr"], d["ivac"], color=c, lw=1.5, label=SHOW.get(k, k))
        ax2.plot(d["mr"], d["tc"], color=c, lw=1.5, label=k)
        m = TYPICAL_MR[k]
        iv = np.interp(m, d["mr"], d["ivac"])
        tc = np.interp(m, d["mr"], d["tc"])
        ax.plot(m, iv, "o", color=c, ms=4.5, mec="white", mew=0.6, zorder=5)
        ax2.plot(m, tc, "o", color=c, ms=4.5, mec="white", mew=0.6, zorder=5)
    ax.set_xlabel("Mixture ratio O/F (by mass)")
    ax.set_ylabel("Theoretical vacuum Isp, ε = 50 (s)")
    ax.set_xlim(0.8, 8.2)
    ax.set_ylim(290, 470)
    ax.legend(loc="lower right", fontsize=6.6, frameon=False)
    ax.set_title("(a) Specific impulse", loc="left", fontsize=8.6)
    ax2.set_xlabel("Mixture ratio O/F (by mass)")
    ax2.set_ylabel("Chamber temperature (K)")
    ax2.set_xlim(0.8, 8.2)
    ax2.set_ylim(2000, 3900)
    ax2.set_title("(b) Adiabatic flame temperature", loc="left", fontsize=8.6)
    ax2.text(7.9, 2080, "dots: typical engine mixture ratios", fontsize=6.3, ha="right", color=GREY)
    fig.text(0.99, 0.01, "Shifting equilibrium, chamber pressure 6.9 MPa (1 000 psia), computed with an equilibrium "
             "code and NASA thermodynamic data; liquid propellants at their normal storage temperatures.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch35_propellants")


# ----------------------------------------------------------------------------- 4. density impulse
def densityisp():
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    rr = np.linspace(200, 2000, 300)
    for di in [150, 250, 350, 450, 550]:
        ax.plot(rr, di * 1000 / rr, color="#C9D3DD", lw=0.8, zorder=1)
        yy = 252 if di < 550 else 296
        ax.text(di * 1000 / yy, yy, f"{di}", fontsize=6.2, color=GREY, ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=0.6), zorder=2)
    ax.text(1990, 462, "grey curves: equal density impulse\nρ·Isp (kg·s/L), labelled at the bottom",
            fontsize=6.3, color=GREY, ha="right", va="top")
    for k, d in THERMO.items():
        ro, rf = DENS[k]
        mr = np.array(d["mr"])
        rho = (1 + mr) / (mr / ro + 1 / rf)
        c = PCOL[k]
        ax.plot(rho, d["ivac"], color=c, lw=1.6, zorder=3)
        m = TYPICAL_MR[k]
        rb = (1 + m) / (m / ro + 1 / rf)
        iv = np.interp(m, d["mr"], d["ivac"])
        ax.plot(rb, iv, "o", color=c, ms=5, mec="white", mew=0.6, zorder=5)
        off = {'LOX/LH2': (25, 6, "left"), 'LOX/CH₄': (-25, 8, "right"), 'LOX/RP-1': (30, 4, "left"),
               'NTO/MMH': (40, 8, "left"), 'NTO/UDMH': (-140, -52, "right")}[k]
        ax.text(rb + off[0], iv + off[1], f"{SHOW.get(k, k)} (O/F {m:g})", fontsize=6.8, color=c, ha=off[2],
                weight="bold")
    # solid propellant (delivered, not theoretical)
    ax.plot(1800, 280, "s", color=GOLD, ms=5.5, zorder=5)
    ax.text(1780, 300, "APCP solid (delivered,\nGEM 63XL: 280 s)", fontsize=6.6, color="#8A6D00", ha="right",
            va="bottom", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.set_xlim(200, 2000)
    ax.set_ylim(240, 480)
    ax.set_xlabel("Bulk propellant density (kg/m³)")
    ax.set_ylabel("Vacuum specific impulse (s)")
    fig.text(0.99, 0.01, "Lines: theoretical Isp (ε = 50, 6.9 MPa, shifting equilibrium) as the mixture ratio varies; "
             "dots: typical mixture ratios. Bulk density ρ = (1 + O/F)/(O/F/ρo + 1/ρf).",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch35_densityisp")


# ----------------------------------------------------------------------------- 5. engine cycles (schematic)
OXC, FUC, HOT = BLUE, ORANGE, RED


def _tank(ax, x, y, text, c, w=6.0, h=8.0):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=2.2",
                                fc=c, ec=NAVY, lw=0.8, alpha=0.25, zorder=2))
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=2.2",
                                fc="none", ec=NAVY, lw=0.8, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=6.4, color=INK, zorder=4)


def _pump(ax, x, y, c, lab="P", r=1.5):
    ax.add_patch(Circle((x, y), r, fc="white", ec=c, lw=1.2, zorder=5))
    ax.text(x, y, lab, ha="center", va="center", fontsize=5.8, color=c, weight="bold", zorder=6)


def _turb(ax, x, y, w=2.4, h=3.0, c=HOT, lab="T"):
    ax.add_patch(Polygon([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2 - 0.5), (x + w / 2, y + h / 2 + 0.5),
                          (x - w / 2, y + h / 2)], closed=True, fc="white", ec=c, lw=1.2, zorder=5))
    ax.text(x, y, lab, ha="center", va="center", fontsize=5.8, color=c, weight="bold", zorder=6)


def _burner(ax, x, y, c=HOT, lab="GG", w=3.4, h=2.2):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.6",
                                fc="#F8DCDC", ec=c, lw=1.0, zorder=5))
    ax.text(x, y, lab, ha="center", va="center", fontsize=5.6, color=c, weight="bold", zorder=6)


def _chamber(ax, x, y, jacket=False):
    """Combustion chamber whose injector face is at y (top); nozzle below."""
    pts = [(x - 2.6, y), (x + 2.6, y), (x + 2.6, y - 3.0), (x + 1.0, y - 4.4), (x + 3.4, y - 8.4),
           (x - 3.4, y - 8.4), (x - 1.0, y - 4.4), (x - 2.6, y - 3.0)]
    ax.add_patch(Polygon(pts, closed=True, fc="#E6E9EE", ec=NAVY, lw=1.0, zorder=4))
    if jacket:
        jp = [(x + 2.6, y - 0.6), (x + 2.6, y - 3.0), (x + 1.0, y - 4.4), (x + 3.4, y - 8.4)]
        ax.plot([p[0] + 0.55 for p in jp], [p[1] for p in jp], color=FUC, lw=1.6, zorder=4)
        jp2 = [(x - 2.6, y - 0.6), (x - 2.6, y - 3.0), (x - 1.0, y - 4.4), (x - 3.4, y - 8.4)]
        ax.plot([p[0] - 0.55 for p in jp2], [p[1] for p in jp2], color=FUC, lw=1.6, zorder=4)
    ax.add_patch(Polygon([(x - 1.8, y - 8.6), (x + 1.8, y - 8.6), (x + 0.6, y - 11.0), (x - 0.6, y - 11.0)],
                         closed=True, fc="#F6C28B", ec="none", alpha=0.8, zorder=3))


def _line(ax, pts, c, lw=1.3, arrow_at_end=True, z=3, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=c, lw=lw, zorder=z, solid_capstyle="round", ls=ls)
    if arrow_at_end and len(pts) >= 2:
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        ax.annotate("", xy=(x2, y2), xytext=(x1 + 0.92 * (x2 - x1) - 0.0, y1 + 0.92 * (y2 - y1)),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=lw, mutation_scale=7), zorder=z)


def _panel_frame(ax, x0, y0, w, h, title, ex):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc="#FBFCFD",
                                ec="#B8C4CF", lw=0.8, zorder=0))
    ax.text(x0 + 1.2, y0 + h - 1.3, title, ha="left", va="top", fontsize=7.4, weight="bold", color=NAVY)
    ax.text(x0 + w / 2, y0 + 1.0, ex, ha="center", va="bottom", fontsize=6.1, color=INK, style="italic")


def cycles():
    fig, ax = canvas(7.0, 5.05, xlim=(0, 108), ylim=(0, 78))
    W, H = 34.5, 37.0
    xs = [1, 37, 73]
    ys = [40, 1.5]

    # ---- (a) pressure-fed
    x0, y0 = xs[0], ys[0]
    _panel_frame(ax, x0, y0, W, H, "(a) Pressure-fed", "Spacecraft engines, AJ10, Aestus")
    cx = x0 + W / 2
    ax.add_patch(Circle((x0 + 5.5, y0 + 26.5), 2.6, fc="#EDEDED", ec=NAVY, lw=0.8, zorder=3))
    ax.text(x0 + 5.5, y0 + 26.5, "He", ha="center", va="center", fontsize=6.2)
    _tank(ax, x0 + 12.5, y0 + 24, "Ox", OXC)
    _tank(ax, x0 + 24.5, y0 + 24, "Fuel", FUC)
    _line(ax, [(x0 + 5.5, y0 + 29.1), (x0 + 5.5, y0 + 31.0), (x0 + 24.5, y0 + 31.0), (x0 + 24.5, y0 + 28.0)], GREY, lw=0.9)
    _line(ax, [(x0 + 12.5, y0 + 31.0), (x0 + 12.5, y0 + 28.0)], GREY, lw=0.9)
    ax.text(x0 + 8.7, y0 + 31.4, "regulator", fontsize=5.6, color=GREY, va="bottom")
    _line(ax, [(x0 + 12.5, y0 + 20), (x0 + 12.5, y0 + 17), (cx - 1.2, y0 + 17), (cx - 1.2, y0 + 15.0)], OXC)
    _line(ax, [(x0 + 24.5, y0 + 20), (x0 + 24.5, y0 + 17), (cx + 1.2, y0 + 17), (cx + 1.2, y0 + 15.0)], FUC)
    _chamber(ax, cx, y0 + 15.0)
    ax.text(x0 + W - 1.2, y0 + 9.5, "tank pressure\n> chamber\npressure:\nheavy tanks,\nPc ≈ 0.7–2 MPa",
            fontsize=5.8, ha="right", va="center", color=INK)

    # ---- (b) gas generator
    x0, y0 = xs[1], ys[0]
    _panel_frame(ax, x0, y0, W, H, "(b) Gas generator", "Merlin, F-1, Vulcain, CE-20, TQ-12")
    cx = x0 + 15
    _tank(ax, x0 + 6, y0 + 27, "Ox", OXC)
    _tank(ax, x0 + 24, y0 + 27, "Fuel", FUC)
    py = y0 + 18.5
    ax.plot([x0 + 6, x0 + 24], [py, py], color=GREY, lw=1.6, zorder=4)  # shaft
    _pump(ax, x0 + 6, py, OXC)
    _pump(ax, x0 + 24, py, FUC)
    _turb(ax, x0 + 15, py)
    _line(ax, [(x0 + 6, y0 + 23), (x0 + 6, py + 1.5)], OXC, arrow_at_end=False)
    _line(ax, [(x0 + 24, y0 + 23), (x0 + 24, py + 1.5)], FUC, arrow_at_end=False)
    _line(ax, [(x0 + 6, py - 1.5), (x0 + 6, y0 + 15.5), (cx - 1.2, y0 + 15.5), (cx - 1.2, y0 + 14.0)], OXC)
    _line(ax, [(x0 + 24, py - 1.5), (x0 + 24, y0 + 15.5), (cx + 1.2, y0 + 15.5), (cx + 1.2, y0 + 14.0)], FUC)
    _burner(ax, x0 + 15, y0 + 23.6, lab="GG")
    _line(ax, [(x0 + 7.5, y0 + 21.2), (x0 + 12.4, y0 + 23.0)], OXC, lw=0.9)
    _line(ax, [(x0 + 22.5, y0 + 21.2), (x0 + 17.6, y0 + 23.0)], FUC, lw=0.9)
    _line(ax, [(x0 + 15, y0 + 22.5), (x0 + 15, py + 2.0)], HOT, lw=1.0)
    _line(ax, [(x0 + 16.2, py - 1.6), (x0 + 30.5, y0 + 9.0), (x0 + 30.5, y0 + 4.0)], HOT, lw=1.0, ls="--")
    ax.text(x0 + 31.5, y0 + 12.0, "turbine\nexhaust\ndumped", fontsize=5.6, color=HOT, ha="left", va="center")
    _chamber(ax, cx, y0 + 14.0)

    # ---- (c) closed expander
    x0, y0 = xs[2], ys[0]
    _panel_frame(ax, x0, y0, W, H, "(c) Expander (closed)", "RL10, Vinci   (bleed: LE-9, BE-3U)")
    cx = x0 + 15
    _tank(ax, x0 + 6, y0 + 27, "Ox", OXC)
    _tank(ax, x0 + 24, y0 + 27, "Fuel\n(H₂)", FUC)
    py = y0 + 17.5
    ax.plot([x0 + 6, x0 + 24], [py, py], color=GREY, lw=1.6, zorder=4)
    _pump(ax, x0 + 6, py, OXC)
    _pump(ax, x0 + 24, py, FUC)
    _turb(ax, cx, py, c=FUC)
    _line(ax, [(x0 + 6, y0 + 23), (x0 + 6, py + 1.5)], OXC, arrow_at_end=False)
    _line(ax, [(x0 + 24, y0 + 23), (x0 + 24, py + 1.5)], FUC, arrow_at_end=False)
    _line(ax, [(x0 + 6, py - 1.5), (x0 + 6, y0 + 14.8), (cx - 1.4, y0 + 14.8), (cx - 1.4, y0 + 13.4)], OXC)
    # cold H2: pump -> nozzle exit -> cooling jacket -> up to turbine -> injector
    _line(ax, [(x0 + 24, py - 1.5), (x0 + 24, y0 + 4.8), (cx + 4.0, y0 + 4.8)], FUC, lw=1.1)
    _chamber(ax, cx, y0 + 13.4, jacket=True)
    _line(ax, [(cx + 3.15, y0 + 12.8), (cx + 3.15, y0 + 21.6), (cx, y0 + 21.6), (cx, py + 2.1)], FUC, lw=1.1)
    _line(ax, [(cx, py - 2.1), (cx, y0 + 13.4)], FUC, lw=1.1, ls="--")
    ax.text(x0 + 25.5, y0 + 9.0, "H₂ warmed in\nthe cooling\njacket drives\nthe turbine,\nthen burns", fontsize=5.6,
            color=FUC, ha="left", va="center")

    # ---- (d) oxidiser-rich staged combustion
    x0, y0 = xs[0], ys[1]
    _panel_frame(ax, x0, y0, W, H, "(d) Staged combustion (ox-rich)", "RD-180, RD-191, BE-4, YF-100")
    cx = x0 + 15
    _tank(ax, x0 + 6, y0 + 27, "Ox", OXC)
    _tank(ax, x0 + 24, y0 + 27, "Fuel", FUC)
    py = y0 + 18.5
    ax.plot([x0 + 6, x0 + 24], [py, py], color=GREY, lw=1.6, zorder=4)
    _pump(ax, x0 + 6, py, OXC)
    _pump(ax, x0 + 24, py, FUC)
    _turb(ax, x0 + 15, py)
    _line(ax, [(x0 + 6, y0 + 23), (x0 + 6, py + 1.5)], OXC, arrow_at_end=False)
    _line(ax, [(x0 + 24, y0 + 23), (x0 + 24, py + 1.5)], FUC, arrow_at_end=False)
    _burner(ax, x0 + 15, y0 + 23.6, lab="PB")
    _line(ax, [(x0 + 7.5, y0 + 19.5), (x0 + 9.5, y0 + 23.6), (x0 + 13.3, y0 + 23.6)], OXC, lw=1.4)
    ax.text(x0 + 9.2, y0 + 20.4, "all ox", fontsize=5.4, color=OXC, ha="left")
    _line(ax, [(x0 + 22.5, y0 + 21.0), (x0 + 16.7, y0 + 23.2)], FUC, lw=0.9)
    _line(ax, [(x0 + 15, y0 + 22.5), (x0 + 15, py + 2.0)], HOT, lw=1.3)
    _line(ax, [(x0 + 15, py - 2.0), (x0 + 15, y0 + 14.0)], HOT, lw=1.6)
    _line(ax, [(x0 + 24, py - 1.5), (x0 + 24, y0 + 15.8), (cx + 1.6, y0 + 15.8), (cx + 1.6, y0 + 14.0)], FUC)
    _chamber(ax, cx, y0 + 14.0)
    ax.text(x0 + 21.5, y0 + 9.5, "hot oxygen-rich\ngas from turbine\ninjected into\nchamber: no\ndumped flow",
            fontsize=5.6, color=HOT, ha="left", va="center")

    # ---- (e) full-flow staged combustion
    x0, y0 = xs[1], ys[1]
    _panel_frame(ax, x0, y0, W, H, "(e) Full-flow staged combustion", "Raptor")
    cx = x0 + 17.2
    _tank(ax, x0 + 5, y0 + 27, "Ox", OXC)
    _tank(ax, x0 + 29, y0 + 27, "Fuel", FUC)
    py = y0 + 19.0
    ax.plot([x0 + 5, x0 + 11.5], [py, py], color=GREY, lw=1.6, zorder=4)
    ax.plot([x0 + 22.5, x0 + 29], [py, py], color=GREY, lw=1.6, zorder=4)
    _pump(ax, x0 + 5, py, OXC)
    _pump(ax, x0 + 29, py, FUC)
    _turb(ax, x0 + 11.5, py, c=OXC)
    _turb(ax, x0 + 22.5, py, c=FUC)
    _line(ax, [(x0 + 5, y0 + 23), (x0 + 5, py + 1.5)], OXC, arrow_at_end=False)
    _line(ax, [(x0 + 29, y0 + 23), (x0 + 29, py + 1.5)], FUC, arrow_at_end=False)
    _burner(ax, x0 + 11.5, y0 + 25.6, lab="ox PB", w=4.4)
    _burner(ax, x0 + 22.5, y0 + 25.6, lab="fuel PB", w=4.6)
    _line(ax, [(x0 + 6.4, py + 0.8), (x0 + 9.4, y0 + 24.4)], OXC, lw=1.3)
    _line(ax, [(x0 + 27.6, py + 0.8), (x0 + 24.6, y0 + 24.4)], FUC, lw=1.3)
    _line(ax, [(x0 + 11.5, y0 + 24.5), (x0 + 11.5, py + 2.0)], HOT, lw=1.2)
    _line(ax, [(x0 + 22.5, y0 + 24.5), (x0 + 22.5, py + 2.0)], HOT, lw=1.2)
    _line(ax, [(x0 + 11.5, py - 2.0), (x0 + 11.5, y0 + 15.5), (cx - 1.2, y0 + 15.5), (cx - 1.2, y0 + 14.0)], HOT, lw=1.4)
    _line(ax, [(x0 + 22.5, py - 2.0), (x0 + 22.5, y0 + 15.5), (cx + 1.2, y0 + 15.5), (cx + 1.2, y0 + 14.0)], HOT, lw=1.4)
    ax.text(x0 + 10.6, y0 + 16.3, "ox-rich", fontsize=5.3, color=HOT, ha="right")
    ax.text(x0 + 23.4, y0 + 16.3, "fuel-rich", fontsize=5.3, color=HOT, ha="left")
    _chamber(ax, cx, y0 + 14.0)
    ax.text(x0 + 1.3, y0 + 9.5, "all ox and all\nfuel pass through\na turbine, then\nmeet as hot gas", fontsize=5.6,
            color=INK, ha="left", va="center")
    ax.text(x0 + 33.0, y0 + 9.5, "Pc ≈ 30–35\nMPa", fontsize=5.6, color=INK, ha="right", va="center")

    # ---- (f) electric pump
    x0, y0 = xs[2], ys[1]
    _panel_frame(ax, x0, y0, W, H, "(f) Electric pump", "Rutherford (Electron)")
    cx = x0 + 15
    _tank(ax, x0 + 6, y0 + 27, "Ox", OXC)
    _tank(ax, x0 + 24, y0 + 27, "Fuel", FUC)
    py = y0 + 18.5
    _pump(ax, x0 + 6, py, OXC)
    _pump(ax, x0 + 24, py, FUC)
    for xm in (x0 + 10.0, x0 + 20.0):
        ax.add_patch(Rectangle((xm - 1.4, py - 1.3), 2.8, 2.6, fc="white", ec=VIOLET, lw=1.1, zorder=5))
        ax.text(xm, py, "M", ha="center", va="center", fontsize=5.8, color=VIOLET, weight="bold", zorder=6)
    ax.plot([x0 + 7.5, x0 + 8.6], [py, py], color=GREY, lw=1.6, zorder=4)
    ax.plot([x0 + 21.4, x0 + 22.5], [py, py], color=GREY, lw=1.6, zorder=4)
    ax.add_patch(Rectangle((x0 + 12.4, y0 + 23.6), 5.2, 3.2, fc="#E9E1F3", ec=VIOLET, lw=1.0, zorder=5))
    ax.text(x0 + 15, y0 + 25.2, "battery", ha="center", va="center", fontsize=5.6, color=VIOLET, zorder=6)
    ax.plot([x0 + 13.4, x0 + 10.0, x0 + 10.0], [y0 + 23.6, y0 + 22.0, py + 1.3], color=VIOLET, lw=0.9)
    ax.plot([x0 + 16.6, x0 + 20.0, x0 + 20.0], [y0 + 23.6, y0 + 22.0, py + 1.3], color=VIOLET, lw=0.9)
    _line(ax, [(x0 + 6, y0 + 23), (x0 + 6, py + 1.5)], OXC, arrow_at_end=False)
    _line(ax, [(x0 + 24, y0 + 23), (x0 + 24, py + 1.5)], FUC, arrow_at_end=False)
    _line(ax, [(x0 + 6, py - 1.5), (x0 + 6, y0 + 15.5), (cx - 1.2, y0 + 15.5), (cx - 1.2, y0 + 14.0)], OXC)
    _line(ax, [(x0 + 24, py - 1.5), (x0 + 24, y0 + 15.5), (cx + 1.2, y0 + 15.5), (cx + 1.2, y0 + 14.0)], FUC)
    _chamber(ax, cx, y0 + 14.0)
    ax.text(x0 + 21.5, y0 + 9.5, "no turbine;\nbattery mass\nlimits it to small\nengines", fontsize=5.6,
            color=VIOLET, ha="left", va="center")

    # legend
    handles = [Line2D([0], [0], color=OXC, lw=1.6, label="oxidiser"), Line2D([0], [0], color=FUC, lw=1.6, label="fuel"),
               Line2D([0], [0], color=HOT, lw=1.6, label="hot gas"),
               Line2D([0], [0], marker="o", color="w", mec=NAVY, ms=6, label="P pump"),
               Line2D([0], [0], marker=">", color="w", mec=HOT, ms=6, label="T turbine"),
               Line2D([0], [0], marker="s", color="w", mec=HOT, mfc="#F8DCDC", ms=6, label="GG gas generator / PB preburner")]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.045), ncol=6, fontsize=6.2, frameon=False,
              handlelength=1.6, columnspacing=1.2)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.04)
    save(fig, "ch35_cycles")


# ----------------------------------------------------------------------------- 6. engine map
# name, thrust (kN), vacuum Isp (s), chamber pressure (MPa), cycle, propellant
ENG = [
    ("Merlin 1D", 914, 311, 9.7, "GG", "RP-1"),
    ("Raptor 2", 2256, 347, 30.0, "FFSC", "CH4"),
    ("Raptor 3", 2452, 350, 33.0, "FFSC", "CH4"),
    ("RS-25", 2279, 452, 20.6, "SC", "LH2"),
    ("RL10B-2", 110, 465.5, 4.4, "EXP", "LH2"),
    ("RD-180", 4150, 338, 26.7, "SC", "RP-1"),
    ("RD-191", 2090, 337, 25.8, "SC", "RP-1"),
    ("Vulcain 2.1", 1371, 432, 11.7, "GG", "LH2"),
    ("Vinci", 180, 457, 6.0, "EXP", "LH2"),
    ("YF-100", 1340, 335, 18.0, "SC", "RP-1"),
    ("YF-77", 700, 428, 10.1, "GG", "LH2"),
    ("TQ-12", 745, 337, 10.1, "GG", "CH4"),
    ("LE-9", 1471, 426, 10.0, "EXP", "LH2"),
    ("Rutherford Vac", 26, 343, None, "EP", "RP-1"),
    ("Archimedes Vac", 890, 365, 10.0, "SC", "CH4"),
    ("Vikas", 821, 293, 5.85, "GG", "NTO"),
    ("CE-20", 200, 442, 6.0, "GG", "LH2"),
]
EXTRA_PC = [("BE-4", 13.4, "SC"), ("Prometheus", 10.0, "GG"), ("F-1 (1967)", 7.0, "GG")]
CYC_COL = {"GG": ORANGE, "SC": BLUE, "FFSC": VIOLET, "EXP": GREEN, "EP": GOLD}
CYC_NAME = {"GG": "gas generator", "SC": "staged combustion", "FFSC": "full-flow staged comb.",
            "EXP": "expander", "EP": "electric pump"}
PROP_MK = {"RP-1": "o", "CH4": "D", "LH2": "s", "NTO": "^"}


def enginemap():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.9), gridspec_kw=dict(width_ratios=[1.35, 1]))
    pos = {"Merlin 1D": (1060, 311, "left"), "Raptor 2": None, "Raptor 3": None, "RS-25": (2650, 452, "left"),
           "RL10B-2": (128, 465.5, "left"), "RD-180": (4800, 338, "left"), "RD-191": (2350, 328, "left"),
           "Vulcain 2.1": (1240, 438, "right"), "Vinci": (208, 457, "left"), "YF-100": (1340, 326, "center"),
           "YF-77": (610, 428, "right"), "TQ-12": (650, 337, "right"), "LE-9": (1700, 425, "left"),
           "Rutherford Vac": (31, 343, "left"), "Archimedes Vac": (1030, 365, "left"), "Vikas": (950, 293, "left"),
           "CE-20": (172, 442, "right")}
    for n, F, isp, pc, cyc, prop in ENG:
        ax.plot(F, isp, PROP_MK[prop], color=CYC_COL[cyc], ms=5.5, mec="white", mew=0.5, zorder=4)
        if pos[n]:
            x, y, ha = pos[n]
            ax.text(x, y, n, fontsize=6.0, ha=ha, va="center", color=INK)
    ax.text(2800, 358, "Raptor 2 and 3", fontsize=6.0, ha="left", va="center", color=INK)
    ax.set_xscale("log")
    ax.set_xlim(15, 8000)
    ax.set_ylim(280, 480)
    ax.set_xlabel("Thrust (kN, log scale)")
    ax.set_ylabel("Vacuum specific impulse (s)")
    ax.set_title("(a) Thrust and efficiency", loc="left", fontsize=8.6)
    hp = [Line2D([0], [0], marker=PROP_MK[p], color="w", mfc=GREY, ms=5.5, label=l)
          for p, l in [("LH2", "LOX/LH₂"), ("CH4", "LOX/CH₄"), ("RP-1", "LOX/kerosene"), ("NTO", "NTO/UH25")]]
    ax.legend(handles=hp, loc="lower left", fontsize=6.0, frameon=False, ncol=1, handletextpad=0.3)

    rows = [(n, pc, cyc) for n, F, isp, pc, cyc, prop in ENG if pc] + EXTRA_PC
    rows.sort(key=lambda r: r[1])
    y = np.arange(len(rows))
    ax2.barh(y, [r[1] for r in rows], color=[CYC_COL[r[2]] for r in rows], height=0.7)
    ax2.set_yticks(y)
    ax2.set_yticklabels([r[0].replace(" Vac", "") for r in rows], fontsize=6.1)
    for yi, r in zip(y, rows):
        ax2.text(r[1] + 0.4, yi, f"{r[1]:g}", va="center", fontsize=5.8, color=INK)
    ax2.set_xlim(0, 38)
    ax2.set_xlabel("Chamber pressure (MPa)")
    ax2.set_title("(b) Chamber pressure", loc="left", fontsize=8.6)
    hc = [Rectangle((0, 0), 1, 1, color=CYC_COL[k], label=CYC_NAME[k]) for k in ["GG", "EXP", "SC", "FFSC", "EP"]]
    ax2.legend(handles=hc, loc="lower right", fontsize=6.0, frameon=True, framealpha=0.95, edgecolor="none")
    ax2.tick_params(axis="y", length=0)
    fig.text(0.99, 0.01, "Thrust: vacuum where published (sea level for Raptor). Raptor Isp: vacuum value of the "
             "sea-level engine. Colours give the cycle in both panels. Sources: manufacturers and agencies (2024–26).",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    save(fig, "ch35_enginemap")


# ----------------------------------------------------------------------------- solid-motor ballistics
RHO_P, CSTAR_S, N_S = 1770.0, 1550.0, 0.35
A_S = 7.0e-3 / (7.0e6) ** N_S        # burn rate 7 mm/s at 7 MPa


def srmequil():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.1))
    pc = np.linspace(0.2e6, 14e6, 400)
    At = 0.05
    Ab = 330 * At   # Kn = 330
    gen = RHO_P * A_S * pc ** N_S * Ab
    noz = pc * At / CSTAR_S
    ax.plot(pc / 1e6, gen, color=ORANGE, lw=1.6, label="gas generated, ρ a pⁿ Ab  (n = 0.35)")
    ax.plot(pc / 1e6, noz, color=BLUE, lw=1.6, label="gas leaving nozzle, p At / c*")
    peq = (RHO_P * A_S * CSTAR_S * Ab / At) ** (1 / (1 - N_S))
    meq = peq * At / CSTAR_S
    ax.plot(peq / 1e6, meq, "o", color=INK, ms=5, zorder=5)
    ax.annotate(f"equilibrium: {peq/1e6:.1f} MPa,\n{meq:.0f} kg/s", (peq / 1e6, meq), (0.6, 330),
                fontsize=6.6, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.annotate("", (peq / 1e6 - 0.5, 25), (peq / 1e6 - 3.0, 25), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2))
    ax.annotate("", (peq / 1e6 + 0.5, 25), (peq / 1e6 + 3.0, 25), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2))
    ax.text(peq / 1e6 - 1.75, 34, "p rises", fontsize=6.2, color=GREEN, ha="center", va="bottom")
    ax.text(peq / 1e6 + 1.75, 34, "p falls", fontsize=6.2, color=GREEN, ha="center", va="bottom")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 540)
    ax.set_xlabel("Chamber pressure (MPa)")
    ax.set_ylabel("Mass flow (kg/s)")
    ax.legend(loc="upper left", fontsize=6.2, frameon=False)
    ax.set_title("(a) Self-stabilising chamber pressure", loc="left", fontsize=8.6)

    kn = np.linspace(100, 500, 300)
    for n, c in [(0.2, GREEN), (0.35, BLUE), (0.5, ORANGE), (0.7, RED)]:
        a = 7.0e-3 / (7.0e6) ** n
        p = (RHO_P * a * CSTAR_S * kn) ** (1 / (1 - n)) / 1e6
        ax2.plot(kn, p, color=c, lw=1.5, label=f"n = {n}")
    ax2.set_xlim(100, 500)
    ax2.set_ylim(0, 25)
    ax2.set_xlabel("Kn = burning area / throat area")
    ax2.set_ylabel("Equilibrium chamber pressure (MPa)")
    ax2.legend(loc="upper left", fontsize=6.4, frameon=False)
    ax2.text(108, 13.0, f"+10 % in Kn raises pc by {100*(1.1**(1/0.65)-1):.0f} % (n = 0.35)\n"
             f"and by {100*(1.1**(1/0.3)-1):.0f} % (n = 0.7)", fontsize=6.2, ha="left", va="center", color=INK)
    ax2.set_title("(b) Sensitivity to burning area", loc="left", fontsize=8.6)
    fig.text(0.99, 0.01, "pc = (ρp a c* Kn)^(1/(1−n)); propellant density 1 770 kg/m³, c* = 1 550 m/s, burn rate 7 mm/s "
             "at 7 MPa for every n; (a) Kn = 330, At = 0.05 m².", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch35_srmequil")


def _grain_masks(kind, N=601):
    x = np.linspace(-1, 1, N)
    X, Y = np.meshgrid(x, x)
    R = np.hypot(X, Y)
    TH = np.arctan2(Y, X)
    case = R <= 1.0
    if kind == "tube":
        port = R < 0.35
    elif kind == "star":
        npts, ri, ro = 7, 0.25, 0.65      # chosen by a parameter search for the flattest burning area
        # star boundary radius as function of angle: slender points with concave flanks
        ang = np.mod(TH, 2 * np.pi / npts) - np.pi / npts
        rb = ri + (ro - ri) * np.clip(1 - np.abs(ang) / (np.pi / npts), 0, 1) ** 2.0
        port = R < rb
    elif kind == "rodtube":
        port = (R > 0.3) & (R < 0.7)
    elif kind == "external":
        port = (R > 0.75) & case
    else:
        raise ValueError(kind)
    prop = case & ~port
    return x, X, Y, R, case, port, prop


def _burnback(kind):
    from scipy import ndimage
    import contourpy
    x, X, Y, R, case, port, prop = _grain_masks(kind)
    h = x[1] - x[0]
    d = ndimage.distance_transform_edt(~port) * h
    d_m = np.where(case, d, np.nan)
    gen = contourpy.contour_generator(x, x, d_m)
    webs = np.linspace(0.015, 0.8, 158)
    per = []
    for w in webs:
        lines = gen.lines(w)
        L = 0.0
        for seg in lines:
            if len(seg) < 2:
                continue
            dd = np.diff(seg, axis=0)
            mids = 0.5 * (seg[1:] + seg[:-1])
            inside = np.hypot(mids[:, 0], mids[:, 1]) < 0.995
            L += np.sum(np.hypot(dd[:, 0], dd[:, 1])[inside])
        per.append(L)
    per = np.array(per)
    # first point (web 0) by linear extrapolation from the smooth part of the curve
    p0 = per[0] - (per[1] - per[0]) * webs[0] / (webs[1] - webs[0])
    return x, d_m, prop, port, np.r_[0.0, webs], np.r_[p0, per]


def grains():
    kinds = [("tube", "Internal tube\n(progressive)", ORANGE), ("star", "7-point star\n(nearly neutral)", BLUE),
             ("rodtube", "Rod and tube\n(neutral)", GREEN), ("external", "External-burning rod\n(regressive)", RED)]
    fig = plt.figure(figsize=(7.0, 4.1))
    gs = fig.add_gridspec(2, 4, height_ratios=[1, 1.35], hspace=0.16, wspace=0.12)
    axb = fig.add_subplot(gs[1, :])
    Rcase, Lg = 0.5, 4.0           # 1 m diameter, 4 m long grain, ends inhibited
    for i, (k, lab, c) in enumerate(kinds):
        x, d_m, prop, port, webs, per = _burnback(k)
        a = fig.add_subplot(gs[0, i])
        img = np.where(prop, 1.0, np.nan)
        a.imshow(img, extent=(-1, 1, -1, 1), origin="lower", cmap=matplotlib.colors.ListedColormap(["#E8D7B0"]),
                 vmin=0, vmax=1)
        a.contour(x, x, np.where(prop, d_m, np.nan), levels=np.arange(0.1, 0.8, 0.1), colors=[c], linewidths=0.6)
        a.contour(x, x, d_m, levels=[0.004], colors=[INK], linewidths=1.0)
        a.add_patch(Circle((0, 0), 1.0, fc="none", ec=NAVY, lw=1.6))
        a.set_xlim(-1.08, 1.08)
        a.set_ylim(-1.08, 1.08)
        a.set_aspect("equal")
        a.axis("off")
        a.set_title(lab, fontsize=7.0, color=c, weight="bold")
        # ballistics: Ab(w) = perimeter * L ; integrate web with r = a p^n
        Pw = per * Rcase            # metres of perimeter (unit-circle grid scaled to radius 0.5 m)
        wv = webs * Rcase
        Ab = Pw * Lg
        valid = Ab > 1e-3
        wmax = wv[valid][-1]
        Abm = np.mean(Ab[valid])
        At = RHO_P * A_S * CSTAR_S * Abm / (6.0e6) ** (1 - N_S)   # throat chosen for 6 MPa at mean area
        t, w, T, F = 0.0, 0.0, [], []
        dt = 0.05
        while w < wmax:
            ab = np.interp(w, wv, Ab)
            if ab < 1e-3:
                break
            p = (RHO_P * A_S * CSTAR_S * ab / At) ** (1 / (1 - N_S))
            T.append(t)
            F.append(1.6 * p * At / 1e6)
            w += A_S * p ** N_S * dt
            t += dt
        axb.plot(T, F, color=c, lw=1.6, label=lab.replace("\n", " "))
    axb.set_xlabel("Time (s)")
    axb.set_ylabel("Thrust (MN)")
    axb.set_xlim(0, None)
    axb.set_ylim(0, None)
    axb.legend(loc="center right", bbox_to_anchor=(1.0, 0.56), fontsize=6.4, frameon=False, ncol=1)
    fig.text(0.99, 0.01, "Grain 1 m in diameter, 4 m long, ends inhibited; burning surface traced by a level-set "
             "(distance-field) burn-back, contours every 5 cm of web; r = a p^0.35 (7 mm/s at 7 MPa), "
             "throat sized for 6 MPa at mean area, CF = 1.6.", ha="right", va="bottom", fontsize=6.0, color=GREY,
             wrap=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.93, bottom=0.17)
    save(fig, "ch35_grains")


# ----------------------------------------------------------------------------- hybrid regression
def hybrid():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))
    G = np.logspace(1, np.log10(800), 200)
    r_htpb = 0.0304 * G ** 0.681                    # mm/s, G in kg/m2/s
    r_par = 0.488 * (G / 10.0) ** 0.62              # mm/s (G in g/cm2/s inside)
    ax.loglog(G, r_htpb, color=ORANGE, lw=1.6, label="HTPB (n = 0.68)")
    ax.loglog(G, r_par, color=VIOLET, lw=1.6, label="paraffin wax (n = 0.62)")
    ax.axhspan(7.0, 10.0, color=GREY, alpha=0.18, lw=0)
    ax.text(12, 8.4, "typical APCP solid at 7 MPa (for scale)", fontsize=6.2, color=INK, va="center")
    ax.set_xlabel("Oxidiser mass flux G (kg/m²/s)")
    ax.set_ylabel("Fuel regression rate (mm/s)")
    ax.set_xlim(10, 800)
    ax.set_ylim(0.1, 20)
    ax.legend(loc="lower right", fontsize=6.3, frameon=False)
    ax.set_title("(a) Regression rate, r = a Gⁿ", loc="left", fontsize=8.6)

    # single-port grain with constant oxidiser flow; each grain length chosen to start at O/F = 2.4
    mox, r0, of0 = 10.0, 0.08, 2.4
    cases = [("HTPB, n = 0.68", ORANGE, 930.0, lambda g: 0.0304e-3 * g ** 0.681, "-"),
             ("paraffin, n = 0.62", VIOLET, 900.0, lambda g: 0.488e-3 * (g / 10) ** 0.62, "-"),
             ("n = 0.5 (constant O/F)", GREY, 930.0, lambda g: 0.0304e-3 * 497.0 ** 0.181 * g ** 0.5, "--"),
             ("n = 0.8 (for comparison)", RED, 930.0, lambda g: 0.0304e-3 * 497.0 ** -0.119 * g ** 0.8, ":")]
    for lab, c, rf, rate, ls in cases:
        g_init = mox / (np.pi * r0 ** 2)
        L = mox / (of0 * rf * 2 * np.pi * r0 * rate(g_init))
        t, r, T, OF = 0.0, r0, [], []
        while t <= 40.0:
            g = mox / (np.pi * r ** 2)
            rd = rate(g)
            T.append(t)
            OF.append(mox / (rf * 2 * np.pi * r * L * rd))
            r += rd * 0.02
            t += 0.02
        ax2.plot(T, OF, color=c, lw=1.6, ls=ls, label=f"{lab}: port {r0*100:.0f} → {r*100:.0f} cm")
    ax2.set_xlabel("Burn time (s)")
    ax2.set_ylabel("Oxidiser-to-fuel ratio O/F")
    ax2.set_xlim(0, 40)
    ax2.set_ylim(1.5, 4.5)
    ax2.legend(loc="upper left", fontsize=6.0, frameon=False)
    ax2.set_title("(b) Mixture-ratio shift, one port", loc="left", fontsize=8.6)
    fig.text(0.99, 0.01, "Laboratory correlations for gaseous oxygen. (b) Constant oxidiser flow 10 kg/s, single circular port of "
             "8 cm initial radius, length set for O/F = 2.4 at ignition; O/F varies as r^(2n−1).",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch35_hybrid")


if __name__ == "__main__":
    fns = [nozzleflow, altitude, propellants, densityisp, cycles, enginemap, srmequil, grains, hybrid]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
