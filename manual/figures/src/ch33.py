import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge

P0N2 = 0.79 * 101.325        # tissue N2 after long exposure to sea-level air, kPa
HALF = 360.0                 # tissue half-time, min (NASA R-value model)
RLIM = 1.65                  # historically accepted R for the 29.6 kPa EMU
SUITS = [(25.8, "A7L"), (29.6, "EMU"), (34.5, "SpaceX"), (40.0, "Orlan"), (56.5, "xEMU max")]


def o2_co2(W, RQ=0.85):
    """O2 consumption and CO2 production (g/h) for metabolic rate W (Weir equation)."""
    kj_per_l = (3.941 + 1.106 * RQ) * 4.184
    l_h = W / 1000 / kj_per_l * 3600
    return l_h / 22.414 * 32.0, l_h * RQ / 22.414 * 44.01


# ---------------------------------------------------------------- 1. suit anatomy and layers
def suit():
    fig, ax = canvas(7.0, 3.6, xlim=(0, 120), ylim=(0, 61))
    cx = 24
    W = "#F4F5F2"
    E = "#6B7580"
    # backpack (PLSS) behind torso
    ax.add_patch(FancyBboxPatch((cx - 9.5, 29), 19, 19, boxstyle="round,pad=0,rounding_size=1.5",
                                fc="#D9DDE2", ec=E, lw=0.9, zorder=1))
    # legs
    for s in (-1, 1):
        ax.add_patch(Polygon([(cx + s * 1.0, 22), (cx + s * 7.6, 22), (cx + s * 7.0, 6.5), (cx + s * 2.2, 6.5)],
                             closed=True, fc=W, ec=E, lw=0.9, zorder=2))
        ax.add_patch(FancyBboxPatch((cx + (s * 1.6 if s > 0 else -8.6), 2.5), 7.0, 4.4,
                                    boxstyle="round,pad=0,rounding_size=1.2", fc="#C9CED4", ec=E, lw=0.9, zorder=3))
        ax.plot([cx + s * 1.3, cx + s * 7.4], [14.5, 14.5], color=E, lw=0.6, zorder=3)
    # lower torso / brief
    ax.add_patch(Polygon([(cx - 8, 30), (cx + 8, 30), (cx + 7.8, 21), (cx - 7.8, 21)], closed=True,
                         fc=W, ec=E, lw=0.9, zorder=3))
    ax.plot([cx - 8, cx + 8], [27.5, 27.5], color=GREY, lw=1.8, zorder=4)     # waist bearing
    # arms
    for s in (-1, 1):
        ax.add_patch(Polygon([(cx + s * 8.5, 44), (cx + s * 13.5, 42), (cx + s * 15.5, 30), (cx + s * 11.5, 29.5),
                              (cx + s * 8.7, 37)], closed=True, fc=W, ec=E, lw=0.9, zorder=3))
        ax.add_patch(Circle((cx + s * 13.8, 27.6), 2.2, fc="#B8BEC6", ec=E, lw=0.9, zorder=4))   # glove
        ax.plot([cx + s * 9.0, cx + s * 13.6], [43.6, 41.9], color=GREY, lw=1.8, zorder=4)       # shoulder bearing
        ax.plot([cx + s * 11.6, cx + s * 15.4], [30.8, 31.2], color=GREY, lw=1.6, zorder=4)      # wrist bearing
    # hard upper torso
    ax.add_patch(FancyBboxPatch((cx - 8.5, 29.5), 17, 15.5, boxstyle="round,pad=0,rounding_size=2.2",
                                fc=W, ec=E, lw=1.0, zorder=4))
    # display and control module
    ax.add_patch(FancyBboxPatch((cx - 4.5, 31), 9, 5, boxstyle="round,pad=0,rounding_size=0.6",
                                fc="#9AA3AD", ec=E, lw=0.8, zorder=5))
    ax.add_patch(Rectangle((cx - 3.2, 33.6), 3.6, 1.6, fc="#3B4A57", ec="none", zorder=6))
    # helmet with visor
    ax.add_patch(Circle((cx, 50.2), 6.0, fc="#E8EEF3", ec=E, lw=1.0, zorder=5))
    ax.add_patch(Ellipse((cx, 49.0), 8.4, 5.6, fc=GOLD, ec="#8A6E14", lw=0.6, alpha=0.85, zorder=6))
    for s in (-1, 1):
        ax.add_patch(Rectangle((cx + s * 6.2 - (1.6 if s > 0 else 0), 51.0), 1.6, 2.0, fc="#5B6670", ec="none",
                               zorder=7))
    # labels
    xl = 44
    L = [((cx + 5.5, 53.0), (xl, 57.5), "Helmet: sun visor, lights, cameras"),
         ((cx + 5.0, 41.5), (xl, 50.5), "Hard upper torso (fibreglass)"),
         ((cx + 4.5, 33.5), (xl, 43.5), "Display and control module"),
         ((cx + 13, 42.2), (xl, 36.5), "Shoulder, arm and wrist bearings"),
         ((cx + 16.0, 27.6), (xl, 29.5), "Gloves, sized for each astronaut"),
         ((cx + 8.0, 27.5), (xl, 22.5), "Waist bearing, lower torso"),
         ((cx + 8, 5), (xl, 7.5), "Boots")]
    for (x0, y0), (x1, y1), t in L:
        ax.plot([x0, x1 - 0.6], [y0, y1], color=GREY, lw=0.5, zorder=8)
        ax.text(x1, y1, t, fontsize=6.4, ha="left", va="center", color=INK, zorder=9)
    for (x0, y0), (x1, y1), t in [((cx - 9.5, 46), (1, 58.5), "Backpack: life support"),
                                  ((cx - 9.0, 29.6), (1, 19.5), "SAFER jet pack\nunder the\nbackpack")]:
        ax.plot([x0, x1 + 3], [y0, y1 + (-1.5 if y1 > 40 else 3.2)], color=GREY, lw=0.5, zorder=8)
        ax.text(x1, y1, t, fontsize=6.4, ha="left", va="center", color=INK, zorder=9, linespacing=1.15)
    # layer stack (right)
    x0, w = 88, 31
    layers = [(2.6, "Liquid cooling garment", "#F2C9A8"),
              (2.6, "Pressure bladder (coated nylon)", SKY),
              (2.6, "Restraint layer (polyester)", BLUE),
              (2.6, "Liner (neoprene-coated nylon)", "#A7B4C2"),
              (5.6, "Insulation: several layers\nof aluminised film", "#D8DCE0"),
              (2.8, "Outer fabric (Ortho-Fabric)", "#F7F7F2")]
    top = 44
    ax.text(x0 + w / 2, top + 4.6, "Suit wall, inside to outside", fontsize=7.0, ha="center", weight="bold",
            color=NAVY)
    ax.text(x0 + w / 2, top + 0.8, "skin side", fontsize=6.0, ha="center", va="bottom", color=GREY)
    yy = top
    for h, t, c in layers:
        yy -= h
        ax.add_patch(Rectangle((x0, yy), w, h, fc=c, ec="white", lw=0.8, zorder=2))
        ax.text(x0 + w / 2, yy + h / 2, t, fontsize=5.9, ha="center", va="center", zorder=3,
                color="white" if is_dark(c) else INK, linespacing=1.1)
    ax.text(x0 + w / 2, yy - 0.8, "vacuum side", fontsize=6.0, ha="center", va="top", color=GREY)
    b1 = top - 2.6
    b2 = b1 - 5.2
    for ya, yb, t in [(top, b1, "cooling"), (b1, b2, "pressure\ngarment"),
                      (b2, yy, "thermal and\nmicrometeoroid\ngarment")]:
        ax.plot([x0 - 0.8, x0 - 0.8], [ya - 0.2, yb + 0.2], color=NAVY, lw=1.0)
        ax.text(x0 - 1.4, (ya + yb) / 2, t, fontsize=5.9, ha="right", va="center", color=NAVY, linespacing=1.05)
    ax.text(x0 + w / 2, yy - 5.5, "At the joints, bearings, pleats and\nrestraint cables carry the\npressure load", fontsize=6.0, ha="center", va="top", color=INK, linespacing=1.15)
    save(fig, "ch33_suit")


# ---------------------------------------------------------------- 2. PLSS schematic
def plss():
    fig, ax = canvas(7.0, 3.8, xlim=(0, 100), ylim=(0, 58))
    G, Wt, F = BLUE, ORANGE, GREEN
    box(ax, 3, 40, 19, 9, "Helmet\noxygen enters at face", fc="#E3EEF8", ec=NAVY, fs=6.3)
    box(ax, 3, 6, 19, 27, "", fc="#FBEFE4", ec=NAVY)
    label(ax, 12.5, 29.5, "Torso, arms, legs", fs=6.8, weight="bold")
    label(ax, 12.5, 25.0, "gas returns from\nwrists and ankles", fs=6.2)
    # LCVG tubes
    for i in range(5):
        y = 10 + i * 2.4
        ax.plot([6, 19], [y, y], color=Wt, lw=0.9, alpha=0.8)
    label(ax, 12.5, 8.0, "cooling garment tubes", fs=6.0, color="#8A4A12")
    box(ax, 29, 4.5, 18, 10, "CO₂ and trace-gas\nremoval (LiOH or\nMETOX canister)", fc="#E3EEF8", ec=NAVY, fs=6.4)
    box(ax, 53, 4.5, 11, 10, "Fan", fc="#E3EEF8", ec=NAVY, fs=6.8)
    box(ax, 71, 4.5, 15, 30, "", fc="#EAF4EC", ec=NAVY)
    label(ax, 78.5, 31.0, "Sublimator", fs=6.9, weight="bold")
    label(ax, 78.5, 20.0, "porous plate:\nfeedwater\nfreezes, then\nsublimes", fs=6.0)
    label(ax, 78.5, 9.0, "gas and loop\nwater cooled", fs=6.0)
    box(ax, 71, 40, 15, 9, "Water separator\n(condensate)", fc="#E3EEF8", ec=NAVY, fs=6.4)
    box(ax, 53, 22, 11, 8, "Pump", fc="#FBEFE4", ec=NAVY, fs=6.8)
    box(ax, 38, 40.5, 17, 8, "Regulator\nholds 29.6 kPa", fc="#E3EEF8", ec=NAVY, fs=6.4)
    box(ax, 26, 50.5, 41, 7, "Primary O₂: 0.54 kg at 6.2 MPa\nSecondary pack: 1.2 kg at 41 MPa (≈ 30 min)",
        fc="white", ec=NAVY, fs=6.0)
    box(ax, 90, 18, 9.5, 14, "Feed-\nwater\n≈3.8 kg", fc="#EAF4EC", ec=F, fs=6.4)
    # gas loop
    arrow(ax, (12.5, 40), (12.5, 33.2), color=G, lw=1.4)
    arrow(ax, (22, 9.5), (29, 9.5), color=G, lw=1.4)
    arrow(ax, (47, 9.5), (53, 9.5), color=G, lw=1.4)
    arrow(ax, (64, 9.5), (71, 9.5), color=G, lw=1.4)
    arrow(ax, (78.5, 34.5), (78.5, 40), color=G, lw=1.4)
    arrow(ax, (71, 44.5), (55, 44.5), color=G, lw=1.4)
    arrow(ax, (38, 44.5), (22, 44.5), color=G, lw=1.4)
    arrow(ax, (46.5, 50.5), (46.5, 48.5), color=G, lw=1.2)
    # water loop
    arrow(ax, (22, 26), (53, 26), color=Wt, lw=1.4, text="warm water", toff=(-2, 0.4), fs=6.0)
    arrow(ax, (64, 26), (71, 26), color=Wt, lw=1.4)
    arrow(ax, (71, 18.5), (22, 18.5), color=Wt, lw=1.4, text="cooled water ≈ 10 °C", toff=(0, 0.4), fs=6.0)
    # feedwater
    arrow(ax, (90, 25), (86, 25), color=F, lw=1.3)
    arrow(ax, (86, 44.5), (94.5, 32.2), color=F, lw=1.0, rad=-0.25)
    label(ax, 95.5, 41.5, "condensate", fs=6.0, color=F)
    arrow(ax, (86, 12), (97, 5.5), color=GREY, lw=1.2, ls="--")
    label(ax, 96.5, 9.8, "vapour\nto space", fs=6.0, color=GREY)
    # legend
    yl = 2.0
    for i, (c, t) in enumerate([(G, "oxygen loop"), (Wt, "cooling-water loop"), (F, "feedwater")]):
        x = 3 + i * 21
        ax.plot([x, x + 4], [yl - 0.0, yl], color=c, lw=1.8)
        ax.text(x + 5, yl, t, fontsize=6.2, va="center", color=INK)
    ax.set_ylim(-0.5, 58)
    save(fig, "ch33_plss")


# ---------------------------------------------------------------- 3. why suits run at low pressure
def pressure():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.0))
    P = np.linspace(15, 62, 300)
    PH2O, PCO2 = 6.27, 5.33
    PAO2 = P - PH2O - PCO2
    sea = 0.2095 * (101.325 - PH2O) - PCO2 / 0.8
    a1.plot(P, PAO2, color=NAVY)
    a1.axhline(sea, color=GREEN, lw=0.9, ls="--")
    a1.text(61, sea + 1.0, "sea-level air ≈ 13.3 kPa", fontsize=6.2, color=GREEN, ha="right", va="bottom")
    a1.fill_between(P, 0, np.minimum(PAO2, sea), where=PAO2 < sea, color=RED, alpha=0.12, lw=0)
    a1.text(16, 2.0, "hypoxic", fontsize=6.4, color=RED, ha="left")
    for p, n in SUITS:
        y = p - PH2O - PCO2
        a1.plot([p], [y], "o", ms=4, color=ORANGE, zorder=4)
        a1.text(p - 0.8, y + 1.6, n, fontsize=6.1, ha="right", va="bottom", color=INK)
    a1.set_xlim(15, 62)
    a1.set_ylim(0, 54)
    a1.set_xlabel("Suit pressure, pure oxygen (kPa)")
    a1.set_ylabel("Oxygen pressure in the lungs (kPa)")
    a1.set_title("(a) Oxygen sets the floor", loc="left", fontsize=8.6)
    radii = [(0.01, "finger, r = 1 cm", VIOLET), (0.04, "wrist, 4 cm", GREEN), (0.055, "elbow, 5.5 cm", BLUE),
             (0.08, "knee, 8 cm", ORANGE), (0.11, "hip/waist, 11 cm", RED)]
    for r, n, c in radii:
        M = np.pi * P * 1e3 * r ** 3
        a2.plot(P, M, color=c, lw=1.4)
        a2.text(61.5, np.pi * 61.5e3 * r ** 3 * 1.13, n, fontsize=6.1, color=c, ha="right", va="bottom")
    for p, n in SUITS:
        a2.axvline(p, color=GREY, lw=0.5, ls=":")
    a2.set_yscale("log")
    a2.set_ylim(0.05, 600)
    a2.set_yticks([0.1, 1, 10, 100])
    a2.set_yticklabels(["0.1", "1", "10", "100"])
    a2.set_xlim(15, 62)
    a2.set_xlabel("Suit pressure (kPa)")
    a2.set_ylabel("Moment to fold a plain tube (N·m)")
    a2.set_title("(b) Pressure stiffens the joints", loc="left", fontsize=8.6)
    fig.text(0.99, 0.01, "(a) Alveolar gas equation with 100 % O₂, water vapour 6.3 kPa, CO₂ 5.3 kPa. "
             "(b) Collapse moment of an inflated fabric tube, M = π p r³; real joints use pleats, bearings\n"
             "and constant-volume shapes to cut this by a large factor. Dotted lines: suit pressures of panel (a).",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, "ch33_pressure")


# ---------------------------------------------------------------- 4. decompression: R and prebreathe
def dcs():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.1), gridspec_kw={"width_ratios": [1.0, 1.15]})
    P = np.linspace(20, 60, 400)
    atm = [(P0N2, "Sea-level air (101.3 kPa)", NAVY), (0.735 * 70.3, "70.3 kPa, 26.5 % O₂", BLUE),
           (0.66 * 56.5, "56.5 kPa, 34 % O₂", GREEN)]
    for n2, n, c in atm:
        t = HALF * np.log2(np.maximum(n2 / (P * RLIM), 1.0)) / 60
        a1.plot(P, t, color=c, label=n)
    for p, n in SUITS[1:4]:
        t = HALF * np.log2(P0N2 / (p * RLIM)) / 60
        a1.plot([p], [t], "o", ms=4, color=ORANGE, zorder=4)
        a1.text(p + 0.9, t + 0.05, f"{n} {t:.1f} h", fontsize=6.1, color=INK, ha="left", va="bottom")
    a1.set_xlim(20, 60)
    a1.set_ylim(0, 4.8)
    a1.set_xlabel("Suit pressure (kPa)")
    a1.set_ylabel("Oxygen prebreathe for R = 1.65 (h)")
    a1.set_title("(a) Pre-EVA cabin atmosphere", loc="left", fontsize=8.6)
    a1.legend(fontsize=6.1, loc="upper right", handlelength=1.4)
    # (b) protocol simulations
    dt = 1.0

    def run(segs):
        n2, ts, xs = P0N2, [0.0], [P0N2]
        t = 0.0
        for dur, amb in segs:
            for _ in range(int(dur / dt)):
                n2 = amb + (n2 - amb) * 2 ** (-dt / HALF)
                t += dt
                ts.append(t)
                xs.append(n2)
        return np.array(ts) / 60, np.array(xs)

    prot = [("4 h oxygen in suit", [(240, 0.0)], NAVY),
            ("Shuttle staged: 1 h O₂, 12 h at 70.3 kPa, 75 min in suit",
             [(60, 0.0), (720, 0.735 * 70.3), (75, 0.0)], BLUE)]
    for n, segs, c in prot:
        t, x = run(segs)
        a2.plot(t, x / 29.6, color=c, label=n)
        a2.plot([t[-1]], [x[-1] / 29.6], "o", ms=4, color=c)
        a2.text(t[-1] - 0.2, x[-1] / 29.6 - 0.06, f"R = {x[-1] / 29.6:.2f}", fontsize=6.2, color=c,
                ha="right" if t[-1] > 10 else "center", va="top")
    a2.plot([0, 15], [0.66 * 56.5 / 29.6] * 2, color=GREEN, lw=1.4, ls="--",
            label="Living at 56.5 kPa, 34 % O₂ (no prebreathe)")
    a2.axhline(RLIM, color=RED, lw=0.9, ls=":")
    a2.text(5.0, RLIM + 0.03, "accepted limit 1.65", fontsize=6.1, color=RED, ha="left", va="bottom")
    a2.set_xlim(0, 15)
    a2.set_ylim(1.1, 2.85)
    a2.set_xlabel("Time from start of protocol (h)")
    a2.set_ylabel("R if the suit were at 29.6 kPa")
    a2.set_title("(b) Prebreathe protocols", loc="left", fontsize=8.6)
    a2.legend(fontsize=6.0, loc="upper right", handlelength=1.6)
    fig.text(0.99, 0.01, "Single 360-min tissue (NASA R-value model): tissue N₂ relaxes exponentially towards the "
             "inspired N₂ pressure; R = tissue N₂ / suit pressure. Initial tissue N₂ = 0.79 × 101.3 kPa.\n"
             "Real protocols were validated in chamber trials; exercise during prebreathe, not modelled here, "
             "speeds nitrogen removal.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, "ch33_dcs")


# ---------------------------------------------------------------- 5. metabolic rate and consumables
def metab():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.0), gridspec_kw={"width_ratios": [1.1, 1.0]})
    K = 1.163  # W per kcal/h
    B = 0.2931  # W per Btu/h
    rows = [("Resting", 90, 90, None, GREY, "≈ 90 W"),
            ("ISS assembly EVAs\n(2001–03, 17 EVAs)", 191.5 * K, 254.9 * K, 965.3 * K, BLUE, "averages 223–296 W"),
            ("Apollo lunar EVAs", 1000 * B, 1000 * B, 2200 * B, ORANGE, "average ≈ 290 W")]
    for i, (n, lo, hi, mx, c, t) in enumerate(rows):
        y = len(rows) - 1 - i
        if mx:
            a1.plot([hi, mx], [y, y], color=c, lw=1.0)
            a1.plot([mx], [y], "|", color=c, ms=8, mew=1.2)
            a1.text(mx, y - 0.2, f"peak {mx:,.0f} W".replace(",", " "), fontsize=6.1, color=c, ha="right",
                    va="top")
        a1.barh(y, max(hi - lo, 14), left=lo - (7 if hi == lo else 0), height=0.42, color=c, zorder=3)
        a1.text(lo - 7, y + 0.27, t, fontsize=6.2, ha="left", va="bottom", color=INK, zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.6))
    a1.axvline(1600 * B, color=RED, lw=0.9, ls="--")
    a1.text(1600 * B + 14, 2.55, "EMU sized for\n1 h at 470 W", fontsize=6.1, color=RED, va="top")
    a1.set_yticks(range(len(rows)))
    a1.set_yticklabels([r[0] for r in rows][::-1], fontsize=6.6)
    a1.set_xlim(0, 1200)
    a1.set_ylim(-0.6, 2.7)
    a1.grid(axis="y", visible=False)
    a1.set_xlabel("Metabolic rate (W)")
    a1.set_title("(a) How hard spacewalkers work", loc="left", fontsize=8.6)
    W = np.linspace(150, 600, 200)
    o2, co2 = o2_co2(W)
    a2.plot(W, 540 / o2, color=BLUE, label="Primary oxygen, 0.54 kg")
    a2.plot(W, 540 / co2, color=VIOLET, label="CO₂ canister, 0.54 kg")
    a2.plot(W, 3.8 / (W / 2.83e6 * 3600), color=GREEN, label="Feedwater, 3.8 kg")
    a2.axhspan(7, 8, color=GOLD, alpha=0.18, lw=0)
    a2.text(590, 7.5, "7 h EVA + 1 h reserve", fontsize=6.1, color="#8A6E14", ha="right", va="center")
    a2.set_xlim(150, 600)
    a2.set_ylim(0, 20)
    a2.set_xlabel("Average metabolic rate (W)")
    a2.set_ylabel("Endurance (h)")
    a2.set_title("(b) Which consumable runs out first", loc="left", fontsize=8.6)
    a2.legend(fontsize=6.1, loc="upper right", handlelength=1.4)
    fig.text(0.99, 0.01, "(a) Averages and peaks from NASA ISS assembly data (Katuntsev et al. 2004) and Apollo reports. "
             "(b) Weir equation, RQ 0.85, 20.4 kJ per litre O₂; all metabolic heat\nrejected by sublimation "
             "(2.83 MJ/kg); suit leakage and heat leaks ignored. Capacities approximate those of the ISS EMU.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, "ch33_metab")


# ---------------------------------------------------------------- 6. ISS spacewalks per year
YEARS = list(range(1998, 2027))
COUNTS = [3, 1, 9, 18, 18, 2, 5, 7, 14, 23, 19, 17, 15, 10, 4, 11, 7, 7, 4, 10, 8, 11, 8, 13, 12, 12, 3, 5, 7]
HOURS = [21.4, 7.9, 59.6, 100.4, 115.1, 13.3, 19.7, 40.4, 91.3, 150.3, 127.8, 98.2, 100.1, 64.7, 27.6, 66.7, 36.7,
         42.9, 22.2, 60.8, 56.6, 72.7, 51.1, 89.6, 82.0, 80.4, 12.4, 30.3, 46.6]


def issevas():
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.bar(YEARS, COUNTS, color=SKY, width=0.72, zorder=2, label="Spacewalks per year")
    ax.set_ylabel("Spacewalks per year")
    ax.set_ylim(0, 30)
    ax.set_xlim(1997.3, 2026.7)
    ax2 = ax.twinx()
    ax2.plot(YEARS, HOURS, color=NAVY, lw=1.4, marker="o", ms=2.8, zorder=3, label="Hours outside")
    ax2.set_ylim(0, 180)
    ax2.set_ylabel("Hours outside per year")
    ax2.spines["right"].set_visible(True)
    ax2.grid(False)
    ax.axvspan(1997.3, 2011.6, color=GOLD, alpha=0.08, lw=0)
    ax.text(1998.0, 28.6, "Assembly era: Space Shuttle flights", fontsize=6.3, color="#8A6E14", va="top")
    ann = [((2003, 2.5), (2004.4, 22.5), "Columbia accident:\nShuttle grounded"),
           ((2011.6, 10.5), (2011.2, 20.5), "Shuttle\nretired"),
           ((2013, 11.6), (2014.6, 17.0), "EVA 23: water\nin helmet"),
           ((2024, 3.5), (2023.6, 19.0), "Suit leaks:\nonly 3")]
    for (x, y), (xt, yt), t in ann:
        ax.annotate(t, (x, y), (xt, yt), fontsize=6.0, ha="center", va="bottom", color=INK, linespacing=1.05,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.5, shrinkA=0, shrinkB=1), zorder=6)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=6.4)
    ax.set_xticks(range(2000, 2027, 2))
    ax.tick_params(axis="x", labelsize=7)
    fig.text(0.99, 0.01, "Data: NASA itemised list of ISS spacewalks (US and Russian), accessed October 2026, corrected for "
             "duplicates: 283 of NASA's total of 284, ≈1 790 h, December 1998 – September 2026.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch33_issevas")


# ---------------------------------------------------------------- 7. suits through time
def history():
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    rows = [("Berkut (USSR)", [(1965.0, 1965.5)], RED, "Leonov, first spacewalk"),
            ("Gemini G4C (US)", [(1965.3, 1966.9)], BLUE, "Gemini 4–12"),
            ("Yastreb (USSR)", [(1969.0, 1969.4)], RED, "Soyuz 4/5 crew transfer"),
            ("Apollo A7L / A7LB (US)", [(1969.5, 1974.1)], BLUE, "Moon 1969–72, Skylab 1973–74"),
            ("Orlan family (USSR/Russia)", [(1977.9, 2026.8)], RED, "Salyut 6, Salyut 7, Mir, ISS; Orlan-MKS from 2017"),
            ("Shuttle / ISS EMU (US)", [(1983.3, 2026.8)], BLUE, "STS-6 1983; Hubble; ISS"),
            ("Feitian (China)", [(2008.7, 2008.9), (2021.5, 2026.8)], GOLD, "Shenzhou-7; Tiangong"),
            ("SpaceX EVA suit", [(2024.7, 2024.9)], GREY, "Polaris Dawn"),
            ("Axiom AxEMU (US)", [(2027.0, 2030.0)], VIOLET, "planned: ISS test 2027, Moon 2028+"),
            ("Wangyu lunar suit (China)", [(2028.5, 2030.0)], GOLD, "planned: landing before 2030")]
    n = len(rows)
    for i, (name, spans, c, t) in enumerate(rows):
        y = n - 1 - i
        for a, b in spans:
            planned = a >= 2027
            ax.barh(y, max(b - a, 0.5), left=a, height=0.55, color=c if not planned else "white",
                    ec=c, lw=1.0, hatch="////" if planned else None, zorder=3)
        a_last = spans[-1][1]
        xt = spans[0][0] - 0.6 if spans[0][0] > 1990 else a_last + 0.6
        ha = "right" if spans[0][0] > 1990 else "left"
        if name.startswith("Orlan") or name.startswith("Shuttle"):
            xt, ha = spans[0][0] + 1.0, "left"
            ax.text(xt, y, t, fontsize=6.1, va="center", ha=ha, color="white", zorder=4)
        else:
            ax.text(xt, y, t, fontsize=6.1, va="center", ha=ha, color=INK, zorder=4)
    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=6.7)
    ax.set_xlim(1963, 2032)
    ax.set_ylim(-0.7, n - 0.3)
    ax.grid(axis="y", visible=False)
    ax.set_xticks(range(1965, 2031, 5))
    ax.tick_params(axis="x", labelsize=7)
    fig.text(0.99, 0.01, "Bars: years each suit type was used for spacewalks (hatched: planned, status October 2026). "
             "Red: Soviet/Russian; blue: NASA; gold: China.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch33_history")


# ---------------------------------------------------------------- 8. Apollo surface EVAs
def lunar():
    fig, (ax, a2) = plt.subplots(1, 2, figsize=(6.8, 2.9), gridspec_kw={"width_ratios": [1.6, 1.0]})
    m = ["A11", "A12", "A14", "A15", "A16", "A17"]
    evas = [[2 + 31 / 60], [3 + 56 / 60, 3 + 49 / 60], [4 + 47 / 60, 4 + 34 / 60],
            [6 + 32 / 60, 7 + 12 / 60, 4 + 50 / 60], [7 + 11 / 60, 7 + 23 / 60, 5 + 40 / 60],
            [7 + 12 / 60, 7 + 37 / 60, 7 + 15 / 60]]
    x = np.arange(len(m))
    cols = [SKY, BLUE, NAVY]
    for i, e in enumerate(evas):
        b = 0
        for j, h in enumerate(e):
            ax.bar(i, h, bottom=b, color=cols[j], width=0.58, ec="white", lw=0.6, zorder=3,
                   label=f"EVA {j + 1}" if i == 5 else None)
            b += h
        ax.text(i, b + 0.4, f"{b:.1f} h", fontsize=6.4, ha="center", va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels(["Apollo 11\n1969", "12\n1969", "14\n1971", "15\n1971", "16\n1972", "17\n1972"],
                       fontsize=6.8)
    ax.set_ylabel("Surface EVA time (h)")
    ax.set_ylim(0, 27)
    ax.grid(axis="x", visible=False)
    ax.axvspan(2.5, 5.5, color=GOLD, alpha=0.10, lw=0)
    ax.text(1.0, 12.5, "on foot,\n4-h backpacks", fontsize=6.3, ha="center", color=GREY)
    ax.text(4.0, 24.8, "rover missions, 8-h backpacks", fontsize=6.3, ha="center", color="#8A6E14")
    ax.legend(loc="upper left", fontsize=6.2)
    ax.set_xlim(-0.5, 5.5)
    ax.set_title("(a) Time outside on each landing", loc="left", fontsize=8.6)
    xs = np.arange(3)
    tot = [27.8, 26.7, 35.9]
    lng = [12.5, 11.6, 20.1]
    far = [5.0, 4.5, 7.6]
    a2.bar(xs - 0.25, tot, width=0.25, color=SKY, label="Total driven", zorder=3)
    a2.bar(xs, lng, width=0.25, color=BLUE, label="Longest traverse", zorder=3)
    a2.bar(xs + 0.25, far, width=0.25, color=ORANGE, label="Farthest from lander", zorder=3)
    for xi, vals in zip(xs, zip(tot, lng, far)):
        for k, v in enumerate(vals):
            a2.text(xi + (k - 1) * 0.25, v + 0.6, f"{v:g}", fontsize=5.9, ha="center", va="bottom")
    a2.set_xticks(xs)
    a2.set_xticklabels(["Apollo 15", "Apollo 16", "Apollo 17"], fontsize=6.8)
    a2.set_ylabel("Distance (km)")
    a2.set_ylim(0, 48)
    a2.grid(axis="x", visible=False)
    a2.legend(loc="upper left", fontsize=6.1)
    a2.set_title("(b) Lunar Roving Vehicle", loc="left", fontsize=8.6)
    fig.text(0.99, 0.01, "Data: NASA mission reports; NSSDC Lunar Roving Vehicle summary. "
             "Total ≈ 80 h of lunar surface EVA by 12 astronauts.", ha="right", va="bottom", fontsize=6.0,
             color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch33_lunar")


if __name__ == "__main__":
    fns = [suit, plss, pressure, dcs, metab, issevas, history, lunar]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
