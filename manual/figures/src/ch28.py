import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch


def distances():
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    D = [("Opportunity (Mars, 2004–18)", 45.16, RED), ("Perseverance (Mars, 2021– ; early 2026)", 42.0, RED),
         ("Lunokhod 2 (Moon, 1973)", 39.0, GREY), ("Curiosity (Mars, 2012– ; 2026)", 37.0, RED),
         ("Apollo 17 LRV (Moon, 1972)", 35.7, BLUE), ("Apollo 15 LRV (Moon, 1971)", 27.8, BLUE),
         ("Apollo 16 LRV (Moon, 1972)", 26.7, BLUE), ("Lunokhod 1 (Moon, 1970–71)", 10.5, GREY),
         ("Spirit (Mars, 2004–10)", 7.73, RED), ("Zhurong (Mars, 2021–22)", 1.92, ORANGE),
         ("Yutu-2 (Moon far side, 2019– )", 1.61, ORANGE), ("Yutu (Moon, 2013–16)", 0.114, ORANGE),
         ("Sojourner (Mars, 1997)", 0.10, RED), ("Pragyan (Moon, 2023)", 0.10, GREEN)]
    labs = [d[0] for d in D]; vals = [d[1] for d in D]
    y = np.arange(len(D))
    ax.barh(y, vals, color=[d[2] for d in D], height=0.7, zorder=2)
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=6.6); ax.invert_yaxis()
    for yi, v in zip(y, vals):
        ax.text(v + 0.5, yi, f"{v:.2f} km" if v < 1 else f"{v:.1f} km", va="center", fontsize=6.3)
    ax.set_xlim(0, 52); ax.set_xlabel("Total distance driven (km)")
    ax.grid(axis="y", visible=False)
    for c, t in [(RED, "NASA Mars rovers"), (GREY, "Soviet Lunokhods"), (BLUE, "Apollo Lunar Roving Vehicles (crewed)"),
                 (ORANGE, "Chinese rovers"), (GREEN, "Indian rover")]:
        ax.bar([0], [0], color=c, label=t)
    ax.legend(fontsize=6.0, loc="lower right")
    save(fig, "ch28_distances")


def rocker():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 100), ylim=(0, 46))
    ax.add_patch(Rectangle((0, 3), 100, 1.2, fc="#D9C6A5", ec="none"))
    ax.add_patch(Rectangle((62, 4.2), 38, 6.0, fc="#D9C6A5", ec="none"))
    R = 4.2
    wheels = [(14, 3 + 4.2 + R - 4.2), (36, 7.2), (63.5, 10.2 + R)]
    wheels = [(14, 4.2 + R), (36, 4.2 + R), (60.5, 10.2 + R)]
    for (x, yy) in wheels:
        ax.add_patch(Circle((x, yy), R, fc="#4A4A4A", ec=INK, lw=1, zorder=4))
        ax.add_patch(Circle((x, yy), 1.0, fc="#BBBBBB", ec=INK, lw=0.6, zorder=5))
    bog = (25, 17.5)
    ax.plot([wheels[0][0], bog[0], wheels[1][0]], [wheels[0][1], bog[1], wheels[1][1]], color=BLUE, lw=3, zorder=3)
    piv = (44, 24)
    ax.plot([bog[0], piv[0], wheels[2][0]], [bog[1], piv[1], wheels[2][1]], color=ORANGE, lw=3.4, zorder=3)
    ax.add_patch(FancyBboxPatch((28, 25), 34, 9, boxstyle="round,pad=0.4", fc=LIGHT, ec=NAVY, lw=1.2, zorder=2))
    ax.plot(*piv, "o", color=NAVY, ms=7, zorder=6)
    ax.plot(*bog, "o", color=NAVY, ms=6, zorder=6)
    label(ax, 45, 30, "Body (warm electronics box)", fs=7)
    label(ax, 74, 31, "Differential: when one rocker\ntilts up, the other tilts down,\nkeeping the body level",
          fs=6.4, ha="left")
    arrow(ax, (73.5, 30), (46, 24.5), color=GREY, lw=0.8)
    label(ax, 55, 23.5, "Rocker", fs=7, color=ORANGE, weight="bold")
    label(ax, 12, 20.5, "Bogie", fs=7, color=BLUE, weight="bold")
    label(ax, 70, 18, "Front wheel climbs an\nobstacle up to about one\nwheel diameter high", fs=6.4, ha="left")
    label(ax, 25, 1.5, "No springs: all six wheels stay in contact, sharing the load", fs=6.4, color=INK)
    label(ax, 88, 41, "Side view (one side shown)", fs=6.4, color=GREY)
    save(fig, "ch28_rocker")


def _dp(W, b=0.4, r=0.26, s=None, n=1.0, kc=1400., kphi=820000., c=170., phi=np.radians(35), K=0.018):
    if s is None:
        s = np.linspace(0.01, 0.9, 120)
    z = (3 * W / ((3 - n) * (kc + b * kphi) * np.sqrt(2 * r))) ** (2 / (2 * n + 1))
    Rc = (kc + b * kphi) * z ** (n + 1) / (n + 1)
    L = r * np.arccos(1 - z / r)
    H = (b * L * c + W * np.tan(phi)) * (1 - K / (s * L) * (1 - np.exp(-s * L / K)))
    return s, z, Rc, (H - Rc) / W


def terra():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.0))
    for W, lab, col in [(556, "Curiosity on Mars (556 N per wheel)", RED),
                        (1470, "Same rover on Earth (1 470 N per wheel)", BLUE),
                        (90, "Sojourner on Mars (≈ 18 N... scaled wheel)", GREY)][:2]:
        s, z, Rc, d = _dp(W)
        a1.plot(s * 100, d, color=col, lw=1.8, label=f"{lab}; sinkage {z * 1000:.0f} mm")
    a1.axhline(0, color=INK, lw=0.6)
    a1.set_xlabel("Wheel slip (%)"); a1.set_ylabel("Drawbar pull / wheel load")
    a1.set_title("(a) Traction on loose sand", fontsize=7.6)
    a1.legend(fontsize=5.8, loc="lower right")
    a1.set_ylim(-0.25, 0.5)
    Ws = np.linspace(50, 3000, 100)
    for b, col in [(0.2, ORANGE), (0.4, RED), (0.6, VIOLET)]:
        mx = [np.degrees(np.arctan(_dp(W, b=b)[3].max())) for W in Ws]
        a2.plot(Ws, mx, color=col, lw=1.8, label=f"Wheel width {b:.1f} m")
    a2.set_xlabel("Load per wheel (N)"); a2.set_ylabel("Steepest climbable sand slope (°)")
    a2.set_title("(b) Wide, lightly loaded wheels climb better", fontsize=7.6)
    a2.legend(fontsize=6.0, loc="upper right")
    fig.text(0.99, 0.01, "Bekker–Wong terramechanics for a rigid wheel of 0.26 m radius on cohesionless sand "
                         "(n = 1, kc = 1.4 kN/m², kφ = 820 kN/m³, c = 0.17 kPa, φ = 35°). Representative values.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch28_terra")


def flight():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.0))
    W = [("Earth (sea level)", 9.81, 1.225, BLUE), ("Mars (surface)", 3.71, 0.017, RED), ("Titan (surface)", 1.35, 5.4, GOLD)]
    DL = 1.8 / (np.pi * 0.605 ** 2)
    vals = [g ** 1.5 * np.sqrt(DL / (2 * rho)) for _, g, rho, _ in W]
    a1.bar(range(3), vals, color=[w[3] for w in W], width=0.6, zorder=2)
    for i, v in enumerate(vals):
        a1.text(i, v * 1.05 + 1, f"{v:.0f} W/kg" if v >= 1 else f"{v:.2f} W/kg", ha="center", fontsize=6.6)
    a1.set_xticks(range(3)); a1.set_xticklabels([w[0] for w in W], fontsize=6.6)
    a1.set_ylabel("Ideal hover power per kg (W/kg)")
    a1.set_ylim(0, max(vals) * 1.22)
    a1.set_title("(a) Same rotor loading: Titan is ≈ 40× easier than Earth", fontsize=7.4)
    rpm = np.linspace(500, 3200, 200)
    tip = np.pi * 1.21 * rpm / 60
    a2.plot(rpm, tip / 343, color=BLUE, lw=1.8, label="Earth (speed of sound 343 m/s)")
    a2.plot(rpm, tip / 240, color=RED, lw=1.8, label="Mars (speed of sound ≈ 240 m/s)")
    a2.axhline(0.7, color=GREY, ls="--", lw=0.8)
    a2.text(560, 0.72, "Practical tip-Mach limit ≈ 0.7", fontsize=6.0, color=GREY)
    a2.plot(2537, np.pi * 1.21 * 2537 / 60 / 240, "o", color=NAVY, ms=5)
    a2.annotate("Ingenuity: 1.21 m rotors\nat ≈ 2 500 rpm", (2537, 0.67), xytext=(1500, 0.95), fontsize=6.0,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a2.set_xlabel("Rotor speed (rpm)"); a2.set_ylabel("Blade-tip Mach number")
    a2.set_title("(b) Mars rotors must spin fast but not too fast", fontsize=7.4)
    a2.legend(fontsize=5.9, loc="lower right")
    a2.set_ylim(0, 1.1)
    fig.text(0.99, 0.01, "Momentum theory: ideal hover power per unit mass = g^1.5 √(disk loading / 2ρ), here for "
                         "Ingenuity's disk loading (1.8 kg on a 1.21 m disk). Real power is roughly twice the ideal.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch28_flight")


def autonomy():
    fig, ax = canvas(7.0, 2.9, xlim=(0, 100), ylim=(0, 40))
    steps = [(2, "Stereo\ncameras", "Image pairs of the\nterrain ahead"), (21, "3-D terrain\nmap", "Height of every\npoint in view"),
             (40, "Hazard\nassessment", "Slopes, rocks,\nsteps scored for\nthe rover's footprint"),
             (59, "Path\nplanning", "Choose the arc\nthat makes most\nprogress safely"),
             (78, "Drive and\nlocalise", "Visual odometry\ncorrects for wheel\nslip; repeat")]
    for x, t, d in steps:
        box(ax, x, 21, 17, 12, t, fc=LIGHT, ec=NAVY, fs=7.2, weight="bold")
        label(ax, x + 8.5, 12, d, fs=6.2, color=INK)
    for i in range(4):
        arrow(ax, (steps[i][0] + 17.2, 27), (steps[i + 1][0] - 0.2, 27), color=NAVY, lw=1.2)
    ax.annotate("", (10.5, 33.5), (86.5, 33.5), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.2,
                                                                 connectionstyle="arc3,rad=0.25"))
    label(ax, 48.5, 38.5, "Loop repeats every few metres — on Perseverance, while the rover keeps driving", fs=6.6,
          color=ORANGE)
    label(ax, 50, 2.5, "Ground controllers set the goal and the 'keep-out' zones; the rover finds its own way.", fs=6.6,
          color=GREY)
    save(fig, "ch28_autonav")


def polar():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.9))
    H = np.linspace(0, 360, 400)
    for lat, dec, col, ls, lab in [(-89.5, -1.54, RED, "-", "89.5° S, southern summer"),
                                   (-89.5, 1.54, RED, "--", "89.5° S, southern winter"),
                                   (-85.0, -1.54, BLUE, "-", "85° S, southern summer"),
                                   (-85.0, 1.54, BLUE, "--", "85° S, southern winter")]:
        phi, d = np.radians(lat), np.radians(dec)
        el = np.degrees(np.arcsin(np.sin(phi) * np.sin(d) + np.cos(phi) * np.cos(d) * np.cos(np.radians(H))))
        a1.plot(H / 360 * 29.53, el, color=col, ls=ls, lw=1.5, label=lab)
    a1.axhline(0, color=INK, lw=0.7)
    a1.set_xlabel("Days through one lunar day–night cycle"); a1.set_ylabel("Sun elevation (°)")
    a1.set_title("(a) The Sun skims the horizon near the poles", fontsize=7.4)
    a1.legend(fontsize=5.6, loc="upper center", ncol=2)
    a1.set_ylim(-8, 9.5)
    e = np.linspace(0.5, 10, 200)
    a2.semilogy(e, 1 / np.tan(np.radians(e)), color=NAVY, lw=1.8)
    a2.set_xlabel("Sun elevation (°)"); a2.set_ylabel("Shadow length of a 1 m rock (m)")
    a2.set_title("(b) Long shadows hide hazards", fontsize=7.4)
    for x in [1.5, 3]:
        y = 1 / np.tan(np.radians(x))
        a2.plot(x, y, "o", color=ORANGE, ms=4)
        a2.annotate(f"{y:.0f} m at {x}°", (x, y), xytext=(x + 1.2, y * 1.3), fontsize=6.2,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    fig.text(0.99, 0.01, "The Moon's spin axis is tilted only 1.54° to the ecliptic, so near the poles the Sun circles "
                         "the horizon and crater floors can stay dark for billions of years.", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch28_polar")


if __name__ == "__main__":
    fns = [distances, rocker, terra, flight, autonomy, polar]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
