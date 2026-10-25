import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge  # noqa: F401

MU = 398600.4418e9          # m^3/s^2
RE = 6378.137e3             # m
G0 = 9.80665


# ----------------------------------------------------------------------------------------------------------------
def timeline():
    """Milestones of servicing, assembly and manufacturing in two panels (1970-2012, 2013-2026)."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.0, 4.6), gridspec_kw={"height_ratios": [1, 1.12]})
    C = {"c": BLUE, "r": ORANGE, "m": GREEN}
    E1 = [  # (year, text, level, category)
        (1973.4, "Skylab saved by\nspacewalkers", 2, "c"),
        (1978.05, "Progress 1 refuels\nSalyut 6", -1.2, "r"),
        (1984.27, "Solar Max captured\nand repaired (STS-41C)", 2.2, "c"),
        (1984.87, "Palapa B2, Westar 6\nretrieved (STS-51A)", -2.4, "c"),
        (1992.37, "Intelsat 603 rescued\n(three-person EVA)", 2, "c"),
        (1993.95, "Hubble SM1\n(5 missions to 2009)", -1.2, "c"),
        (1997.9, "ETS-VII robotic\ndocking (Japan)", 1.0, "r"),
        (1998.9, "ISS assembly begins\n(to 2011)", -2.6, "c"),
        (2007.2, "Orbital Express: robotic\nrefuelling, part swaps", 2.2, "r"),
        (2009.37, "Hubble SM4", -1.2, "c"),
        (2011.53, "Robotic Refuelling\nMission on ISS", 1.0, "r"),
    ]
    E2 = [
        (2014.9, "First 3D print\non ISS", 1.0, "m"),
        (2018.95, "RRM3 cryogen\ntest (ISS)", -1.2, "r"),
        (2020.15, "MEV-1 docks\nIntelsat 901", 2.4, "r"),
        (2021.28, "MEV-2 docks in GEO;\nELSA-d launched", -2.5, "r"),
        (2022.06, "Shijian-21 tows\ndead BeiDou", 1.0, "r"),
        (2023.4, "SSPD-1 beams\npower (Caltech)", -1.0, "m"),
        (2024.14, "Varda W-1 capsule\nlands in Utah", 2.6, "m"),
        (2024.68, "Metal part printed on ISS;\nZBLAN > 11 km", -2.6, "m"),
        (2024.92, "ADRAS-J 15 m\nfrom H-IIA stage", 0.9, "r"),
        (2025.5, "SJ-25 docks\nwith SJ-21", -1.2, "r"),
        (2026.55, "MRV + 3 MEPs\nlaunched", 2.4, "r"),
        (2026.62, "Katalyst Swift\nreboost abandoned", -2.5, "r"),
    ]
    for ax, E, x0, x1, ttl in [(a1, E1, 1970, 2013, "(a) 1970–2012: astronauts and the Space Shuttle"),
                                (a2, E2, 2013.5, 2027.6, "(b) 2013–2026: commercial robotic servicing and manufacturing")]:
        ax.plot([x0, x1], [0, 0], color=NAVY, lw=2, zorder=2)
        for x, t, lv, cat in E:
            ax.plot([x, x], [0, lv], color=GREY, lw=0.6, zorder=1)
            ax.plot([x], [0], "o", color=C[cat], ms=5, zorder=3, mec="white", mew=0.6)
            ax.text(x, lv + (0.1 if lv > 0 else -0.1), t, ha="center", va="bottom" if lv > 0 else "top",
                    fontsize=6.0, color=INK, linespacing=1.1, zorder=4)
        ax.set_xlim(x0, x1)
        ax.set_ylim(-4.0, 3.9)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.grid(False)
        ax.set_title(ttl, fontsize=7.6, loc="left")
        ax.tick_params(axis="x", labelsize=6.8)
    a1.set_xticks(range(1970, 2014, 5))
    a2.set_xticks(range(2014, 2028, 2))
    for cat, lab in [("c", "Crewed servicing and assembly"), ("r", "Robotic servicing and debris removal"),
                     ("m", "In-space manufacturing and power")]:
        a2.plot([], [], "o", color=C[cat], label=lab, ms=5)
    a2.legend(loc="lower center", bbox_to_anchor=(0.5, -0.42), ncol=3, fontsize=6.4)
    fig.tight_layout(h_pad=0.6)
    save(fig, "ch40_timeline")


# ----------------------------------------------------------------------------------------------------------------
def _cw(n, x0, y0, vx, vy, t):
    """Clohessy-Wiltshire closed-form solution. x radial (up), y along-track (direction of flight)."""
    s, c = np.sin(n * t), np.cos(n * t)
    x = (4 - 3 * c) * x0 + (s / n) * vx + (2 / n) * (1 - c) * vy
    y = 6 * (s - n * t) * x0 + y0 + (2 / n) * (c - 1) * vx + (4 * s - 3 * n * t) / n * vy
    return x, y


def approach():
    n = np.sqrt(MU / (RE + 420e3) ** 3)
    T = 2 * np.pi / n
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(7.0, 3.0), gridspec_kw={"width_ratios": [1.35, 1, 1]})
    # (a) V-bar approach by radial hops
    t = np.linspace(0, T / 2, 400)
    legs = [(-3000.0, 2000.0), (-1000.0, 800.0)]
    for i, (y0, L) in enumerate(legs):
        dv = n * L / 4
        x, y = _cw(n, 0, y0, -dv, 0, t)
        a1.plot(y, x, color=BLUE, lw=1.6)
        a1.annotate("", xy=(y[205], x[205]), xytext=(y[195], x[195]),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0))
        lx, lha = (y0 + L / 2, "center") if i == 0 else (-950, "left")
        a1.text(lx, -L / 4 - (60 if i == 0 else 40), f"hop {i + 1}: 2 burns of {dv:.2f} m/s\n{L / 1000:.1f} km in {T / 120:.0f} min",
                ha=lha, va="top", fontsize=6.0, color=BLUE)
    a1.plot([-200, -15], [0, 0], color=ORANGE, lw=2.4)
    a1.annotate("final approach\nat 0.1 m/s", xy=(-110, 8), xytext=(-420, 250), fontsize=6.0, color=ORANGE,
                ha="center", va="bottom", arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))
    for yh, lab in [(-3000, "start"), (-1000, "hold 1 km")]:
        a1.plot(yh, 0, "s", color=NAVY, ms=4, zorder=4)
        a1.text(yh, 50, lab, ha="center", va="bottom", fontsize=6.0, color=NAVY)
    a1.plot(-200, 0, "s", color=NAVY, ms=4, zorder=4)
    a1.text(-160, -45, "hold\n200 m", ha="left", va="top", fontsize=6.0, color=NAVY)
    a1.plot(0, 0, "*", color=RED, ms=9, zorder=5)
    a1.text(40, 40, "target", ha="left", va="bottom", fontsize=6.0, color=RED)
    a1.set_xlim(-3300, 450); a1.set_ylim(-900, 420)
    a1.set_xlabel("Along-track position, V-bar (m)", fontsize=7)
    a1.set_ylabel("Radial position, R-bar (m)", fontsize=7)
    a1.set_title("(a) V-bar approach by radial hops", fontsize=7.4)
    # (b) R-bar approach from below with free-drift aborts
    a2.plot([0, 0], [-1400, -20], color=ORANGE, lw=2.4)
    a2.text(-60, -1250, "forced\napproach\nalong\nR-bar", fontsize=6.0, color=ORANGE, va="bottom", ha="right")
    tt = np.linspace(0, 0.2 * T, 300)
    for x0, vx, c, (tx, ty) in [(-600, 0.3, BLUE, (690, -1000)), (-300, 0.15, VIOLET, (560, -560))]:
        x, y = _cw(n, x0, 0, vx, 0, tt)
        a2.plot(y, x, color=c, lw=1.4, ls="--")
        a2.plot(0, x0, "o", color=c, ms=3.5, zorder=4)
        a2.text(tx, ty, f"thrust lost at\n{-x0} m, {vx} m/s:\nfalls away", fontsize=5.9, color=c, ha="center",
                va="center")
    a2.plot(0, 0, "*", color=RED, ms=9, zorder=5)
    a2.set_xlim(-450, 950); a2.set_ylim(-1500, 150)
    a2.set_xlabel("Along-track (m)", fontsize=7)
    a2.set_title("(b) R-bar approach from below", fontsize=7.4)
    # (c) V-bar passive safety after thruster failure
    tt = np.linspace(0, T, 1200)
    a3.add_patch(Circle((0, 0), 30, fc="#F6D7DB", ec=RED, lw=0.7, zorder=1))
    xl, yl = (-160, 70), (-60, 330)
    for v, c in [(0.05, GREEN), (0.1, BLUE), (0.2, ORANGE), (0.3, RED)]:
        x, y = _cw(n, 0, -100, 0, v, tt)
        a3.plot(y, x, color=c, lw=1.3)
        inside = (y > xl[0]) & (y < xl[1]) & (x > yl[0]) & (x < yl[1])
        k = np.argmax(~inside[5:]) + 4
        ha = "left" if y[k] < xl[0] + 5 else "center"
        a3.text(max(y[k], xl[0] + 3), min(x[k], yl[1] - 10), f"{v:.2f} m/s", fontsize=5.9, color=c, ha=ha,
                va="top", bbox=dict(fc="white", ec="none", pad=0.4, alpha=0.8))
    a3.plot(-100, 0, "s", color=NAVY, ms=4, zorder=4)
    a3.plot(0, 0, "*", color=RED, ms=9, zorder=5)
    a3.text(0, -40, "30 m keep-out", fontsize=5.9, color=RED, ha="center", va="top")
    a3.set_xlim(*xl); a3.set_ylim(*yl)
    a3.set_xlabel("Along-track (m)", fontsize=7)
    a3.set_title("(c) Free drift if thrust fails at 100 m", fontsize=7.4)
    for a in (a1, a2, a3):
        a.tick_params(labelsize=6.3)
    fig.text(0.99, 0.01, "Clohessy–Wiltshire solutions for a target in a 420 km circular orbit (period 93 min). "
             "Radial axis up = away from Earth; target flies to the right. Axes not to equal scale.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1), w_pad=0.6)
    save(fig, "ch40_approach")


# ----------------------------------------------------------------------------------------------------------------
def capture():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 2.9))
    w = np.logspace(-1, 1, 200)            # deg/s
    wr = np.radians(w)
    for r, c in [(1, GREEN), (2, BLUE), (5, ORANGE), (10, RED)]:
        a1.plot(w, wr * r * 100, color=c, lw=1.6, label=f"{r} m from spin axis")
    a1.axhspan(0.1, 5, color="#E3F1E7", zorder=0)
    a1.text(9.5, 3.0, "gentle capture\n(≤ a few cm/s)", fontsize=6.0, color=GREEN, ha="right", va="center")
    a1.axvline(2.67, color=GREY, ls=":", lw=0.9)
    a1.text(2.8, 150, "Envisat\n(2013)", fontsize=5.9, color=GREY, va="center")
    a1.set_xscale("log"); a1.set_yscale("log")
    a1.set_xlim(0.1, 10); a1.set_ylim(0.1, 300)
    a1.set_xlabel("Tumble rate (°/s)", fontsize=7)
    a1.set_ylabel("Speed of the grasp point (cm/s)", fontsize=7)
    a1.set_title("(a) A grapple point moves fast on a big tumbling object", fontsize=7.2)
    a1.legend(fontsize=5.9, loc="lower right")
    # (b) angular momentum to be removed
    objs = [("PROBA-1 (95 kg)", 8, GREEN), ("Dead GEO comsat (2.5 t)", 2.0e4, VIOLET),
            ("H-IIA upper stage (3 t)", 3.3e4, BLUE), ("SL-16 stage (9 t)", 1.0e5, ORANGE),
            ("Envisat (8.2 t)", 1.3e5, RED)]
    for name, I, c in objs:
        a2.plot(w, I * wr, color=c, lw=1.5, label=name)
    for H, lab in [(1, "small-satellite wheel ≈ 1 N·m·s"), (100, "large wheel ≈ 100 N·m·s"),
                   (4760, "ISS control-moment gyro 4 760 N·m·s")]:
        a2.axhline(H, color=GREY, ls="--", lw=0.8)
        right = H == 100
        a2.text(9.5 if right else 0.105, H * 1.3, lab, fontsize=5.9, color=GREY, va="bottom",
                ha="right" if right else "left", bbox=dict(fc="white", ec="none", pad=0.3, alpha=0.85))
    a2.set_xscale("log"); a2.set_yscale("log")
    a2.set_xlim(0.1, 10); a2.set_ylim(1e-2, 1e5)
    a2.set_xlabel("Tumble rate (°/s)", fontsize=7)
    a2.set_ylabel("Angular momentum (N·m·s)", fontsize=7)
    a2.set_title("(b) Momentum the servicer must absorb", fontsize=7.2)
    a2.legend(fontsize=5.7, loc="lower right")
    for a in (a1, a2):
        a.tick_params(labelsize=6.3)
    fig.text(0.99, 0.01, "v = ωr; H = Iω about the largest principal axis. Moments of inertia approximated from mass and "
             "dimensions (stages as uniform cylinders; Envisat ≈ 1.3 × 10⁵ kg·m²). Envisat rate from laser ranging.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch40_capture")


# ----------------------------------------------------------------------------------------------------------------
def interfaces():
    fig, ax = canvas(7.0, 4.1, xlim=(0, 105), ylim=(0, 61))
    W, H = 33, 28.5
    cells = [(1, 31.5), (36, 31.5), (71, 31.5), (1, 1), (36, 1), (71, 1)]
    titles = ["Probe in the apogee engine", "Grapple fixture and snare", "Arm grasps launch-adapter ring",
              "Robotic refuelling coupling", "Magnetic docking plate", "Net or harpoon (no fixture)"]
    notes = ["MEV-1, MEV-2 (2020–21): no preparation\nneeded; works on most GEO buses",
             "Shuttle, ISS (Canadarm2), Tiangong:\nprepared client; very reliable",
             "MRV/RSGS, OSAM-1 design (planned):\nring and bolt holes on most satellites",
             "RRM tools (unprepared valves);\nRAFTI, ASSIST (prepared ports)",
             "ELSA-d (2021), ELSA-M: plate\nfitted to client before launch",
             "RemoveDEBRIS tests (2018–19): for\ntumbling debris; hard to control"]
    for (x, y), t, nt in zip(cells, titles, notes):
        ax.add_patch(FancyBboxPatch((x, y), W, H, boxstyle="round,pad=0,rounding_size=0.8", fc="#F7FAFC", ec="#B8C6D3",
                                    lw=0.8, zorder=0))
        label(ax, x + W / 2, y + H - 2.2, t, fs=7.0, weight="bold", color=NAVY)
        label(ax, x + W / 2, y + 3.6, nt, fs=5.9, color=INK)
    SV, CL = "#C8CDD3", "#E9D8A6"
    # 1. probe into nozzle
    x, y = cells[0]
    ax.add_patch(Rectangle((x + 2, y + 9), 10, 12, fc=SV, ec="#555", lw=0.6))
    label(ax, x + 7, y + 15, "servicer", fs=5.9)
    ax.add_patch(Rectangle((x + 23, y + 8), 9, 14, fc=CL, ec="#555", lw=0.6))
    label(ax, x + 27.5, y + 15, "client", fs=5.9, rot=90)
    ax.add_patch(Polygon([(x + 23, y + 13), (x + 17.5, y + 11), (x + 17.5, y + 19), (x + 23, y + 17)], fc="#9AA5B1",
                         ec="#555", lw=0.6))
    ax.plot([x + 12, x + 21.5], [y + 15, y + 15], color=RED, lw=1.6)
    ax.plot([x + 21.5], [y + 15], "o", color=RED, ms=3)
    for yy in (y + 9.5, y + 20.5):
        ax.plot([x + 12, x + 22.6], [yy, yy], color=NAVY, lw=1.0)
    label(ax, x + 16, y + 23.2, "stanchions press on ring", fs=5.8, color=NAVY)
    label(ax, x + 16.7, y + 13.4, "probe", fs=5.8, color=RED)
    # 2. grapple fixture
    x, y = cells[1]
    ax.add_patch(Rectangle((x + 22, y + 8), 10, 14, fc=CL, ec="#555", lw=0.6))
    ax.add_patch(Rectangle((x + 19.5, y + 13), 2.5, 4, fc="#888", ec="#444", lw=0.5))
    ax.plot([x + 15, x + 19.5], [y + 15, y + 15], color="#444", lw=1.6)
    ax.plot([x + 15], [y + 15], "o", color="#444", ms=3)
    ax.add_patch(Rectangle((x + 3, y + 11), 9, 8, fc=SV, ec="#555", lw=0.6))
    for dy in (-2.2, 0, 2.2):
        ax.plot([x + 12, x + 15.5], [y + 15 + dy, y + 15 - dy * 0.3], color=RED, lw=0.9)
    label(ax, x + 7.5, y + 15, "end\neffector", fs=5.8)
    label(ax, x + 17, y + 21.5, "grapple pin", fs=5.8, color="#444")
    label(ax, x + 13.5, y + 9.0, "snare wires", fs=5.8, color=RED)
    # 3. ring grasp
    x, y = cells[2]
    ax.add_patch(Rectangle((x + 19, y + 8), 12, 14, fc=CL, ec="#555", lw=0.6))
    ax.add_patch(Rectangle((x + 16.5, y + 9.5), 2.5, 11, fc="#9AA5B1", ec="#555", lw=0.6))
    ax.add_patch(Rectangle((x + 2, y + 10), 7, 10, fc=SV, ec="#555", lw=0.6))
    ax.plot([x + 9, x + 12, x + 14.5], [y + 18, y + 22.5, y + 20.5], color=NAVY, lw=1.6)
    ax.plot([x + 14.5, x + 16.5], [y + 20.5, y + 20.0], color=NAVY, lw=2.2)
    ax.plot([x + 9, x + 12, x + 14.5], [y + 12, y + 7.5, y + 10.0], color=NAVY, lw=1.6)
    ax.plot([x + 14.5, x + 16.5], [y + 10.0, y + 10.5], color=NAVY, lw=2.2)
    label(ax, x + 18, y + 23.8, "launch-adapter ring", fs=5.8, color="#444")
    label(ax, x + 5.5, y + 15, "arms", fs=5.8)
    # 4. refuelling coupling
    x, y = cells[3]
    ax.add_patch(Rectangle((x + 22, y + 8), 10, 14, fc=CL, ec="#555", lw=0.6))
    ax.add_patch(Rectangle((x + 19.5, y + 13.5), 2.5, 3, fc=GOLD, ec="#555", lw=0.5))
    ax.add_patch(Rectangle((x + 11, y + 12.5), 7, 5, fc="#9AA5B1", ec="#555", lw=0.5))
    ax.plot([x + 3, x + 7, x + 11], [y + 21, y + 18, y + 15], color=NAVY, lw=1.6)
    ax.plot([x + 4, x + 11], [y + 10, y + 13], color=BLUE, lw=1.2, ls="-")
    label(ax, x + 14.5, y + 20, "tool", fs=5.8)
    label(ax, x + 21, y + 11, "valve", fs=5.8, color="#7A5C00")
    label(ax, x + 5.5, y + 8.3, "hose", fs=5.8, color=BLUE)
    # 5. magnetic plate
    x, y = cells[4]
    ax.add_patch(Rectangle((x + 22, y + 9), 9, 12, fc=CL, ec="#555", lw=0.6))
    ax.add_patch(Rectangle((x + 20.5, y + 11), 1.5, 8, fc="#666", ec="#333", lw=0.5))
    ax.add_patch(Rectangle((x + 3, y + 10), 9, 10, fc=SV, ec="#555", lw=0.6))
    ax.add_patch(Rectangle((x + 12, y + 13), 4, 4, fc=RED, ec="#555", lw=0.5))
    for k in range(3):
        ax.plot([x + 16.5 + k * 1.2, x + 16.5 + k * 1.2], [y + 12.5, y + 17.5], color=RED, lw=0.6, ls=":")
    label(ax, x + 21, y + 22.5, "ferromagnetic plate", fs=5.8, color="#333")
    label(ax, x + 14, y + 10.8, "magnet", fs=5.8, color=RED)
    # 6. net
    x, y = cells[5]
    ax.add_patch(Polygon([(x + 21, y + 9), (x + 30, y + 12), (x + 28, y + 21), (x + 19, y + 18)], fc=CL, ec="#555",
                         lw=0.6))
    th = np.linspace(-1.2, 1.2, 9)
    for k in th:
        ax.plot([x + 10, x + 24.5 + 8 * np.cos(k)], [y + 15, y + 15 + 8 * np.sin(k)], color=GREY, lw=0.4)
    ax.add_patch(Wedge((x + 24.5, y + 15), 8, -70, 70, width=0.6, fc=GREY, ec="none", alpha=0.7))
    ax.add_patch(Rectangle((x + 3, y + 11), 7, 8, fc=SV, ec="#555", lw=0.6))
    label(ax, x + 14, y + 22.3, "tethered net", fs=5.8, color=GREY)
    save(fig, "ch40_interfaces")


# ----------------------------------------------------------------------------------------------------------------
def aperture():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.9, 3.1), gridspec_kw={"width_ratios": [1.15, 1]})
    d = np.linspace(3, 10, 50)
    for k, lab in [(1, "D = d"), (3, "3d"), (10, "10d"), (30, "30d")]:
        a1.plot(d, k * d, color="#B8C6D3", lw=0.9, ls="--", zorder=1)
        a1.text(9.75, k * 9.75 * 1.08, lab, fontsize=6.0, color=GREY, ha="right", va="bottom")
    P = [  # name, fairing/bay diameter (m), aperture (m), kind, label x, label y, ha
        ("Hubble 2.4 m mirror\n(Shuttle bay)", 4.6, 2.4, "m", 4.45, 2.4, "right"),
        ("Roman 2.4 m\n(Falcon Heavy)", 5.2, 2.4, "m", 5.38, 2.25, "left"),
        ("JWST 6.5 m segmented\n(Ariane 5)", 5.4, 6.5, "s", 5.6, 6.5, "left"),
        ("NISAR 12 m mesh\n(GSLV)", 4.0, 12, "a", 3.85, 12, "right"),
        ("TerreStar-1 18 m\n(Ariane 5)", 5.4, 18, "a", 5.6, 18, "left"),
        ("SkyTerra-1 22 m\n(Proton)", 4.35, 22, "a", 4.2, 26, "right"),
        ("ISS truss 109 m\n(assembled 1998–2009)", 4.6, 109, "x", 4.8, 109, "left"),
    ]
    mk = {"m": ("o", BLUE, "Monolithic mirror"), "s": ("D", VIOLET, "Folded segmented mirror"),
          "a": ("^", ORANGE, "Deployable mesh antenna"), "x": ("s", RED, "Assembled in orbit")}
    seen = set()
    for name, df, D, k, lx, ly, ha in P:
        m, c, lab = mk[k]
        a1.plot(df, D, m, color=c, ms=6, zorder=3, label=None if k in seen else lab)
        seen.add(k)
        a1.text(lx, ly, name, fontsize=5.9, ha=ha, va="center", color=INK)
    a1.axvline(9, color=GREY, lw=0.8, ls=":")
    a1.text(8.9, 50, "Starship\n9 m", fontsize=5.9, color=GREY, ha="right", va="center")
    a1.set_yscale("log"); a1.set_xlim(2.6, 10); a1.set_ylim(1.0, 400)
    a1.set_xlabel("Fairing or payload-bay diameter d (m)", fontsize=7)
    a1.set_ylabel("Aperture or structure size D (m)", fontsize=7)
    a1.set_title("(a) Folding beats the fairing; assembly escapes it", fontsize=7.2)
    a1.legend(fontsize=5.8, loc="lower right")
    # (b) assembled aperture vs number of launches
    N = np.arange(1, 21)
    for dfair, kseg, c, lab in [(4.6, 6, BLUE, "5 m fairing: 6 segments of 3.9 m per launch"),
                                (8.0, 6, ORANGE, "9 m fairing: 6 segments of 6.8 m per launch"),
                                (8.0, 12, RED, "9 m fairing: 12 segments of 6.8 m per launch")]:
        s = 0.85 * dfair
        A = N * kseg * (np.sqrt(3) / 2) * s ** 2
        D = np.sqrt(4 * A / np.pi)
        a2.plot(N, D, "o-", color=c, ms=2.8, lw=1.4, label=lab)
    a2.axhline(6.5, color=VIOLET, ls=":", lw=0.9)
    a2.text(20, 7.3, "JWST 6.5 m", fontsize=6.0, color=VIOLET, ha="right")
    a2.set_xlim(0, 21); a2.set_ylim(0, 115)
    a2.set_xticks([1, 5, 10, 15, 20])
    a2.set_xlabel("Number of launches", fontsize=7)
    a2.set_ylabel("Equivalent circular aperture (m)", fontsize=7)
    a2.set_title("(b) Aperture assembled from hexagonal segments", fontsize=7.2)
    a2.legend(fontsize=5.8, loc="upper left")
    for a in (a1, a2):
        a.tick_params(labelsize=6.3)
    fig.text(0.99, 0.01, "(a) Nominal fairing/bay outer diameters. (b) Hexagons with flat-to-flat width 0.85 × usable "
             "fairing diameter (4.6 m or 8 m); D = √(4A/π); gaps, edge losses and support structure ignored.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch40_aperture")


# ----------------------------------------------------------------------------------------------------------------
def lifeext():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 2.95))
    isp = 290.0
    ve = isp * G0
    dv_sk = 50.0                        # m/s per year, N-S + E-W station keeping
    dv_dis = 11.0                       # m/s, raise orbit ~300 km above GEO
    P = np.linspace(0, 400, 200)
    for m, c in [(1500, GREEN), (2500, BLUE), (4000, ORANGE)]:
        reserve = m * (1 - np.exp(-dv_dis / ve))
        per_year = m * (1 - np.exp(-dv_sk / ve))
        life = np.clip((P - reserve) / per_year, 0, None)
        a1.plot(P, life, color=c, lw=1.7, label=f"{m:,} kg satellite: {per_year:.0f} kg/yr".replace(",", " "))
    a1.set_xlim(0, 400); a1.set_ylim(0, 16)
    a1.set_xlabel("Usable propellant remaining (kg)", fontsize=7)
    a1.set_ylabel("Remaining station-keeping life (years)", fontsize=7)
    a1.set_title("(a) A GEO satellite's life is its propellant", fontsize=7.2)
    a1.legend(fontsize=5.9, loc="upper left")
    # (b) NPV of a life-extension contract
    r = 0.08
    fee = 13.0
    n = np.arange(0, 11)
    for R, c in [(10, RED), (25, GOLD), (40, GREEN), (70, BLUE)]:
        npv = [sum((R - fee) / (1 + r) ** t for t in range(1, k + 1)) for k in n]
        a2.plot(n, npv, "o-", color=c, ms=2.6, lw=1.5, label=f"satellite earns ${R} M/yr")
    rep = 300.0
    dfr = [rep * (1 - (1 + r) ** -k) - sum(fee / (1 + r) ** t for t in range(1, k + 1)) for k in n]
    a2.plot(n, dfr, "--", color=VIOLET, lw=1.4, label="value of deferring a $300 M\nreplacement, minus fees")
    a2.axhline(0, color=INK, lw=0.6)
    a2.set_xlim(0, 10); a2.set_ylim(-40, 380)
    a2.set_xlabel("Years of life extension", fontsize=7)
    a2.set_ylabel("Net present value to operator ($ M)", fontsize=7)
    a2.set_title("(b) Value of extension at $13 M per year", fontsize=7.2)
    a2.legend(fontsize=5.8, loc="upper left")
    for a in (a1, a2):
        a.tick_params(labelsize=6.3)
    fig.text(0.99, 0.01, "(a) Δv 50 m/s per year, chemical Isp 290 s, 11 m/s reserved for disposal 300 km above GEO. "
             "(b) Fee ≈ $13 M/yr (reported MEV price); discount rate 8 %; net revenue and replacement cost illustrative.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch40_lifeext")


# ----------------------------------------------------------------------------------------------------------------
def _dv_deorbit(h_km, hp_km):
    r1 = RE + h_km * 1e3
    rp = RE + hp_km * 1e3
    v1 = np.sqrt(MU / r1)
    a = (r1 + rp) / 2
    va = np.sqrt(MU * (2 / r1 - 1 / a))
    return v1 - va


def adr():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 2.95), gridspec_kw={"width_ratios": [1, 1.1]})
    h = np.linspace(400, 1500, 200)
    a1.plot(h, _dv_deorbit(h, 50), color=RED, lw=1.8, label="controlled re-entry (perigee 50 km)")
    a1.plot(h, _dv_deorbit(h, 250), color=BLUE, lw=1.6, label="perigee 250 km (uncontrolled re-entry)")
    a1.plot(h, _dv_deorbit(h, 350), color=GREEN, lw=1.4, ls="--", label="perigee 350 km (slower decay)")
    a1.set_xlim(400, 1500); a1.set_ylim(0, 420)
    a1.set_xlabel("Initial circular altitude (km)", fontsize=7)
    a1.set_ylabel("Δv for one perigee-lowering burn (m/s)", fontsize=7)
    a1.set_title("(a) Δv to dispose of an object", fontsize=7.2)
    a1.legend(fontsize=5.8, loc="upper left")
    # (b) propellant for a tug (dry 800 kg) + target, controlled re-entry, Isp 300 s
    T = [("PROBA-1", 95, 600), ("H-IIA upper stage", 3000, 600), ("Envisat", 8200, 770), ("SL-16 (Zenit) stage", 9000, 840)]
    tug = 800.0
    ve = 300 * G0
    y = np.arange(len(T))
    props, dvs = [], []
    for name, m, hh in T:
        dv = _dv_deorbit(hh, 50) + 20.0          # + approach/margin
        mp = (tug + m) * (np.exp(dv / ve) - 1)   # propellant carried, final mass = tug + target
        props.append(mp); dvs.append(dv)
    a2.barh(y, props, color=[GREEN, BLUE, RED, ORANGE], height=0.6, zorder=2)
    for yi, (p, dv, t) in enumerate(zip(props, dvs, T)):
        a2.text(p + 25, yi, f"{p:,.0f} kg  ({t[1]:,} kg at {t[2]} km, Δv {dv:.0f} m/s)".replace(",", " "),
                va="center", fontsize=5.9)
    a2.set_yticks(y); a2.set_yticklabels([t[0] for t in T], fontsize=6.4); a2.invert_yaxis()
    a2.set_xlim(0, 1500)
    a2.set_xlabel("Propellant for controlled re-entry (kg)", fontsize=7)
    a2.set_title("(b) Propellant for an 800 kg tug plus target", fontsize=7.2)
    a2.grid(axis="y", visible=False)
    for a in (a1, a2):
        a.tick_params(labelsize=6.3)
    fig.text(0.99, 0.01, "Single impulsive burn from a circular orbit. (b) Isp 300 s; +20 m/s for rendezvous and "
             "attitude margin; target masses and altitudes approximate.", ha="right", va="bottom", fontsize=6.0,
             color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch40_adr")


# ----------------------------------------------------------------------------------------------------------------
def _fill(need, P, cadence, boil, eta=0.97, eta2=0.97):
    """Number of tanker flights and days to accumulate `need` (t) in an HLS via a depot."""
    target = need / eta2
    dep, k, t = 0.0, 0, 0
    hist = [(0, 0.0)]
    while dep < target and k < 200:
        if k > 0:
            for _ in range(cadence):
                dep *= (1 - boil)
                t += 1
                hist.append((t, dep))
        dep += P * eta
        k += 1
        hist.append((t, dep))
    return k, t, hist


def tankers():
    dry, pay, dv, isp = 120.0, 15.0, 8900.0, 375.0
    need = (dry + pay) * (np.exp(dv / (isp * G0)) - 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 2.95))
    Ps = np.arange(60, 201, 5)
    for boil, c, lab in [(0.0, GREEN, "no boil-off"), (0.001, BLUE, "0.1 % per day"), (0.003, ORANGE, "0.3 % per day"),
                         (0.006, RED, "0.6 % per day")]:
        Ns = [_fill(need, P, 6, boil)[0] for P in Ps]
        a1.step(Ps, Ns, where="mid", color=c, lw=1.5, label=lab)
    a1.axvspan(95, 105, color="#EEF2F6", zorder=0)
    a1.axvspan(145, 155, color="#EEF2F6", zorder=0)
    a1.text(100, 37, "≈ 100 t", fontsize=5.9, ha="center", color=GREY)
    a1.text(150, 37, "≈ 150 t", fontsize=5.9, ha="center", color=GREY)
    a1.set_xlim(60, 200); a1.set_ylim(0, 40)
    a1.set_xlabel("Propellant delivered per tanker flight (t)", fontsize=7)
    a1.set_ylabel("Tanker flights per lunar landing", fontsize=7)
    a1.set_title(f"(a) Tankers to load {need:,.0f} t (one launch / 6 days)".replace(",", " "), fontsize=7.2)
    a1.legend(fontsize=5.9, loc="upper right", title="depot boil-off", title_fontsize=5.9)
    for cad, c in [(6, BLUE), (12, ORANGE)]:
        k, t, hist = _fill(need, 100, cad, 0.002)
        tt, dd = zip(*hist)
        a2.plot(tt, dd, color=c, lw=1.4, label=f"one tanker every {cad} days: {k} flights, {t} days")
    a2.axhline(need / 0.97, color=RED, ls="--", lw=0.9)
    a2.text(2, need / 0.97 + 30, "needed in depot", fontsize=6.0, color=RED)
    a2.set_xlim(0, 230); a2.set_ylim(0, 1700)
    a2.set_xlabel("Days since first tanker", fontsize=7)
    a2.set_ylabel("Propellant in depot (t)", fontsize=7)
    a2.set_title("(b) Filling a depot: 100 t per flight, 0.2 %/day loss", fontsize=7.2)
    a2.legend(fontsize=5.9, loc="lower right")
    for a in (a1, a2):
        a.tick_params(labelsize=6.3)
    fig.text(0.99, 0.01, f"Assumed lander: 120 t dry + 15 t payload, Δv 8.9 km/s after leaving LEO (to NRHO, landing, "
             f"ascent), Isp 375 s → {need:,.0f} t of propellant. 97 % efficiency for each transfer. Illustrative; "
             "not SpaceX figures.".replace(",", " "), ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch40_tankers")


if __name__ == "__main__":
    fns = [timeline, approach, capture, interfaces, aperture, lifeext, adr, tankers]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
