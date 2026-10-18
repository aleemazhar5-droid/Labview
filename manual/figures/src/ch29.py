import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge


def masses():
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    M = [("Apollo 11–17 (1969–72)", 382e3, BLUE), ("Chang'e 6, far side (2024)", 1935.3, ORANGE),
         ("Chang'e 5 (2020)", 1731, ORANGE), ("Luna 16, 20, 24 (1970–76)", 326, GREY),
         ("OSIRIS-REx, Bennu (2023)", 121.6, RED), ("Hayabusa2, Ryugu (2020)", 5.4, VIOLET),
         ("Stardust, comet Wild 2 (2006)", 1e-3, GREEN), ("Hayabusa, Itokawa (2010)", 1e-3, VIOLET),
         ("Genesis, solar wind (2004)", 4e-4, GOLD)]
    y = np.arange(len(M))
    ax.barh(y, [m[1] for m in M], color=[m[2] for m in M], height=0.65, zorder=2)
    ax.set_xscale("log"); ax.set_xlim(1e-4, 3e6)
    ax.set_yticks(y); ax.set_yticklabels([m[0] for m in M], fontsize=6.6); ax.invert_yaxis()
    txt = ["382 kg", "1 935 g", "1 731 g", "326 g", "121.6 g", "5.4 g", "< 1 mg", "< 1 mg (≈ 1 500 grains)", "≈ 0.4 mg of ions"]
    for yi, (m, t) in enumerate(zip(M, txt)):
        ax.text(m[1] * 1.4, yi, t, va="center", fontsize=6.3)
    ax.set_xlabel("Mass returned to Earth (grams, log scale)")
    ax.grid(axis="y", visible=False)
    save(fig, "ch29_masses")


def timeline():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    R = [("Apollo 11–17", 1969.5, 1972.97, BLUE, "Moon"), ("Luna 16, 20, 24", 1970.7, 1976.65, GREY, "Moon"),
         ("Stardust", 1999.1, 2006.04, GREEN, "Comet"), ("Genesis", 2001.6, 2004.7, GOLD, "Solar wind"),
         ("Hayabusa", 2003.36, 2010.45, VIOLET, "Asteroid"), ("Hayabusa2", 2014.92, 2020.93, VIOLET, "Asteroid"),
         ("OSIRIS-REx", 2016.69, 2023.73, RED, "Asteroid"), ("Chang'e 5", 2020.9, 2020.96, ORANGE, "Moon"),
         ("Chang'e 6", 2024.34, 2024.48, ORANGE, "Moon, far side"), ("Tianwen-2", 2025.41, 2027.91, ORANGE, "Asteroid"),
         ("Chandrayaan-4", 2027.5, 2027.8, GREEN, "Moon"), ("MMX", 2026.8, 2031.6, VIOLET, "Phobos"),
         ("Tianwen-3", 2028.8, 2031.6, ORANGE, "Mars")]
    for i, (n, a, b, c, tg) in enumerate(R):
        planned = a > 2025.5 or n == "Tianwen-2"
        ax.barh(i, max(b - a, 0.25), left=a, color=c, alpha=0.45 if planned else 1.0,
                hatch="///" if planned else None, edgecolor=c, height=0.6, zorder=2)
        ax.text(max(b, a + 0.25) + 0.4, i, tg, va="center", fontsize=6.0, color=INK)
    ax.set_yticks(range(len(R))); ax.set_yticklabels([r[0] for r in R], fontsize=6.6); ax.invert_yaxis()
    ax.axvline(2026.79, color=RED, lw=0.8, ls=":")
    ax.text(2026.9, -0.6, "Oct 2026", fontsize=6.0, color=RED)
    ax.set_xlim(1967, 2036); ax.set_xlabel("Year (bar: launch to sample delivery; pale = in progress or planned)")
    ax.grid(axis="y", visible=False)
    save(fig, "ch29_timeline")


def ascent():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.9))
    B = [("Bennu", 0.0002, GREY), ("Phobos", 0.011, VIOLET), ("Moon", 1.9, BLUE), ("Mars", 4.2, RED), ("Earth", 9.4, NAVY)]
    a1.bar(range(5), [b[1] for b in B], color=[b[2] for b in B], width=0.6, zorder=2)
    a1.set_yscale("log"); a1.set_ylim(1e-4, 30)
    for i, b in enumerate(B):
        a1.text(i, b[1] * 1.5, f"{b[1] * 1000:.1f} m/s" if b[1] < 0.1 else f"{b[1]:.1f} km/s", ha="center", fontsize=6.2)
    a1.set_xticks(range(5)); a1.set_xticklabels([b[0] for b in B], fontsize=6.8)
    a1.set_ylabel("Δv from surface to orbit (km/s, log)")
    a1.set_title("(a) Climbing out of the gravity well", fontsize=7.6)
    dv = np.linspace(0, 10, 200)
    for isp, c, lab in [(290, ORANGE, "Solid or storable propellant, Isp 290 s"), (450, BLUE, "Hydrogen–oxygen, Isp 450 s")]:
        a2.plot(dv, 1 - np.exp(-dv * 1000 / (isp * 9.80665)), color=c, lw=1.8, label=lab)
    for x, n in [(1.9, "Moon"), (4.2, "Mars"), (9.4, "Earth")]:
        a2.axvline(x, color=GREY, ls=":", lw=0.8)
        a2.text(x + 0.1, 0.05, n, fontsize=6.2, color=GREY, rotation=90)
    a2.axhline(0.85, color=RED, lw=0.8, ls="--")
    a2.text(0.2, 0.87, "Practical single-stage limit ≈ 85 %", fontsize=6.0, color=RED)
    a2.set_xlabel("Δv (km/s)"); a2.set_ylabel("Propellant fraction of lift-off mass")
    a2.set_title("(b) Propellant needed rises steeply with Δv", fontsize=7.6)
    a2.legend(fontsize=5.9, loc="center right"); a2.set_ylim(0, 1.05)
    fig.text(0.99, 0.01, "Δv includes typical gravity and drag losses. Phobos and Bennu: escape speeds; a sample can be "
                         "lifted off with a gentle push.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch29_ascent")


def msr():
    fig, ax = canvas(7.0, 3.9, xlim=(0, 100), ylim=(0, 56))
    label(ax, 2, 53, "NASA–ESA Mars Sample Return architecture (2020–2024 baseline; unfunded from 2026)", fs=7.4,
          ha="left", weight="bold", color=NAVY)
    steps = [(1, "Perseverance\ncollects and\nseals samples"), (17.5, "Sample Retrieval\nLander receives\ntubes"),
             (34, "Mars Ascent\nVehicle launches\ncontainer to orbit"), (50.5, "Earth Return\nOrbiter captures\ncontainer"),
             (67, "Cruise to\nEarth; release\nentry capsule"), (83.5, "Capsule lands\nin Utah; sealed\nfacility")]
    for x, t in steps:
        box(ax, x, 35, 15.5, 13, t, fc=LIGHT, ec=NAVY, fs=6.4)
    for i in range(5):
        arrow(ax, (steps[i][0] + 15.6, 41.5), (steps[i + 1][0] - 0.1, 41.5), color=NAVY, lw=1.1)
    label(ax, 50, 31, "Two launches from Earth and an estimated US$ 8–11 billion; samples on Earth in the late 2030s at the earliest",
          fs=6.4, color=GREY)
    label(ax, 2, 24, "China's Tianwen-3 (launch 2028, return 2031)", fs=7.4, ha="left", weight="bold", color=ORANGE)
    steps2 = [(1, "Lander drills\nand scoops at\nits own site"), (21, "Ascender\nlaunches\nsamples"),
              (41, "Orbiter docks,\ntransfers\ncontainer"), (61, "Return\ncruise"), (81, "Capsule\nlands in\nChina")]
    for x, t in steps2:
        box(ax, x, 5, 17.5, 13, t, fc="#FFF1E0", ec=ORANGE, fs=6.4)
    for i in range(4):
        arrow(ax, (steps2[i][0] + 17.6, 11.5), (steps2[i + 1][0] - 0.1, 11.5), color=ORANGE, lw=1.1)
    label(ax, 50, 1.5, "Two Long March 5 launches; simpler 'grab and go' design with no rover — several hundred grams of material",
          fs=6.4, color=GREY)
    save(fig, "ch29_msr")


def techniques():
    fig, axs = plt.subplots(1, 4, figsize=(7.0, 2.4))
    for ax in axs:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
    # (a) scoop and drill
    a = axs[0]
    a.add_patch(Rectangle((0, 0), 10, 3, fc="#C8B89A", ec="none"))
    a.add_patch(Rectangle((2.2, 1.0), 0.5, 6.5, fc=GREY, ec=INK, lw=0.6))
    a.add_patch(Rectangle((1.6, 7.5), 1.7, 1.2, fc=LIGHT, ec=INK, lw=0.6))
    a.plot([6, 7.5, 8.2], [7.5, 5.0, 3.2], color=INK, lw=1.4)
    a.add_patch(Polygon([(7.8, 3.4), (8.9, 3.0), (8.6, 2.4), (7.6, 2.8)], fc=GREY, ec=INK, lw=0.6))
    a.text(5, 9.6, "(a) Drill and scoop", ha="center", fontsize=6.8, weight="bold")
    a.text(2.45, 0.3, "core", ha="center", fontsize=5.8)
    a.text(8.3, 0.8, "scoop", ha="center", fontsize=5.8)
    a.text(5, -1.2, "Luna, Chang'e 5 and 6", ha="center", fontsize=6.0, color=GREY)
    # (b) TAG
    b = axs[1]
    b.add_patch(Rectangle((0, 0), 10, 2.5, fc="#9E9488", ec="none"))
    for xx in np.linspace(0.5, 9.5, 9):
        b.add_patch(Circle((xx, 2.5), 0.45, fc="#7F776D", ec="none"))
    b.plot([5, 5], [2.9, 8.5], color=INK, lw=1.6)
    b.add_patch(Rectangle((3.8, 2.6), 2.4, 1.0, fc=LIGHT, ec=INK, lw=0.7))
    for dx in [-1.6, -0.9, 0.9, 1.6]:
        b.annotate("", (5 + dx * 1.6, 3.8 + abs(dx) * 0.6), (5 + dx * 0.6, 3.1),
                   arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.8))
    b.text(5, 9.6, "(b) Touch-and-go", ha="center", fontsize=6.8, weight="bold")
    b.text(8.6, 6.4, "N₂ gas\nlifts\nregolith", ha="center", fontsize=5.6, color=BLUE)
    b.text(5, -1.2, "OSIRIS-REx (≈ 6 s contact)", ha="center", fontsize=6.0, color=GREY)
    # (c) projectile horn
    c = axs[2]
    c.add_patch(Rectangle((0, 0), 10, 2.5, fc="#5E5A55", ec="none"))
    c.add_patch(Polygon([(4.0, 3.0), (6.0, 3.0), (5.4, 8.5), (4.6, 8.5)], fc=LIGHT, ec=INK, lw=0.7))
    c.annotate("", (5, 2.6), (5, 6.5), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
    for dx in [-0.8, -0.3, 0.3, 0.8]:
        c.annotate("", (5 + dx * 0.5, 6.0), (5 + dx, 3.0), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.7))
    c.text(5, 9.6, "(c) Projectile and horn", ha="center", fontsize=6.8, weight="bold")
    c.text(7.6, 5.2, "5 g bullet\nat 300 m/s;\nfragments\nfly up", ha="center", fontsize=5.6, color=RED)
    c.text(5, -1.2, "Hayabusa, Hayabusa2", ha="center", fontsize=6.0, color=GREY)
    # (d) aerogel
    d = axs[3]
    d.add_patch(Rectangle((1.5, 2), 7, 5.5, fc="#DCE9F5", ec=NAVY, lw=0.8))
    for i, (x0, l) in enumerate([(3, 3.0), (5, 2.0), (6.6, 3.6)]):
        d.plot([x0, x0 + 0.2], [7.5, 7.5 - l], color=GREY, lw=1.0)
        d.add_patch(Circle((x0 + 0.2, 7.5 - l), 0.18, fc=INK))
        d.annotate("", (x0, 7.6), (x0 - 0.1, 9.2), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.8))
    d.text(5, 9.6, "(d) Aerogel capture", ha="center", fontsize=6.8, weight="bold")
    d.text(5, 1.0, "particles at 6.1 km/s\nstop in carrot-shaped tracks", ha="center", fontsize=5.6)
    d.text(5, -1.2, "Stardust", ha="center", fontsize=6.0, color=GREY)
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.12, top=0.95, wspace=0.08)
    save(fig, "ch29_techniques")


if __name__ == "__main__":
    fns = [masses, timeline, ascent, msr, techniques]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
