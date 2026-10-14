import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[2]
G = json.loads((ROOT / "data/gcat_stats.json").read_text())


def regimes():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    items = [
        ("Commercial airliners", 9, 13, GREY),
        ("High-altitude aircraft (U-2, ER-2)", 18, 21, GREY),
        ("HAPS: solar aircraft & airships", 18, 25, GREEN),
        ("Stratospheric balloons", 25, 49.7, GREEN),
        ("Near space (\"edge of space\")", 20, 100, SKY),
        ("Suborbital tourism (New Shepard, VSS)", 85, 107, ORANGE),
        ("Sounding rockets", 100, 1500, ORANGE),
        ("ISS / Tiangong", 370, 430, BLUE),
        ("Low Earth orbit (LEO)", 160, 2000, BLUE),
        ("Medium Earth orbit: GNSS", 19100, 23222, VIOLET),
        ("Geostationary orbit", 35700, 35870, RED),
        ("Moon (mean distance)", 384000, 386000, GOLD),
        ("Sun–Earth L1 / L2", 1.45e6, 1.55e6, NAVY),
    ]
    for i, (name, lo, hi, c) in enumerate(items):
        ax.barh(i, hi - lo, left=lo, color=c, height=0.62, zorder=3)
        ax.text(hi * 1.18, i, name, va="center", fontsize=7.6)
    ax.set_xscale("log")
    ax.set_xlim(5, 2e7)
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.axvline(100, color=RED, lw=1, ls="--", zorder=2)
    ax.text(100, -0.9, "Kármán line 100 km", color=RED, fontsize=7.4, ha="center")
    ax.axvline(80, color=ORANGE, lw=0.8, ls=":", zorder=2)
    ax.text(70, len(items) - 0.2, "US astronaut\nwings 80 km", color=ORANGE, fontsize=6.6, ha="right", va="bottom")
    ax.set_xlabel("Altitude / distance from Earth's surface (km, logarithmic scale)")
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    save(fig, "ch01_regimes")


def segments():
    fig, ax = canvas(7.2, 4.4, (0, 100), (0, 62))
    title_box(ax, 30, 44, 40, 15, "SPACE SEGMENT", "Satellites, probes, stations,\nconstellations, relay satellites",
              fc="#E8F1FA", hc=BLUE)
    title_box(ax, 2, 4, 30, 17, "GROUND SEGMENT", "Mission & satellite control,\nground stations, payload\ndata processing, archives",
              fc="#EEF7F1", hc=GREEN)
    title_box(ax, 68, 4, 30, 17, "USER SEGMENT", "Receivers, terminals, phones,\nscientists, forecasters,\napps & analytics",
              fc="#FCF3EA", hc=ORANGE)
    title_box(ax, 36, 4, 28, 13, "LAUNCH SEGMENT", "Launch vehicles, spaceports,\nranges, integration", fc="#F3EFF9",
              hc=VIOLET)
    satellite(ax, 50, 39.5, 0.9)
    arrow(ax, (30, 46), (19, 21.5), None, color=GREEN, rad=0.15)
    ax.text(17, 36, "TT&C uplink /\ndownlink", color=GREEN, fontsize=7, ha="center")
    arrow(ax, (70, 46), (81, 21.5), None, color=ORANGE, rad=-0.15)
    ax.text(85, 36, "Service signals\n(comms, PNT, data)", color=ORANGE, fontsize=7, ha="center")
    arrow(ax, (50, 17.5), (50, 36), "Ascent &\ninsertion", color=VIOLET, toff=(6, -2))
    arrow(ax, (32, 12), (68, 12), None, color=GREY, ls="--", style="<|-|>")
    ax.text(50, 0.8, "Terrestrial networks (fibre, internet, cloud) link ground stations, data centres and users",
            ha="center", fontsize=7, color=GREY)
    ax.text(17, 28.5, "(link segment: RF\nand optical links)", fontsize=7, color=NAVY, ha="center", style="italic")
    save(fig, "ch01_segments")


def launches_by_year():
    ly = G["launches_by_year"]
    years = [str(y) for y in range(1957, 2026)]
    groups = ["United States", "USSR / Russia", "China", "Europe", "Japan", "India", "Other"]
    cols = [BLUE, RED, GOLD, VIOLET, GREEN, ORANGE, GREY]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    bottom = np.zeros(len(years))
    for g, c in zip(groups, cols):
        vals = np.array([ly.get(y, {}).get(g, 0) for y in years])
        ax.bar([int(y) for y in years], vals, bottom=bottom, color=c, width=0.85, label=g, zorder=2)
        bottom += vals
    ax.set_xlim(1956, 2026)
    ax.set_ylabel("Orbital launch attempts per year")
    ax.legend(ncol=4, loc="upper left")
    ax.annotate("1967: Cold War peak\n(≈140 attempts)", xy=(1967, 140), xytext=(1972, 205), fontsize=7,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    tot25 = ly["2025"]["_all"]
    ax.annotate(f"2025: record {tot25}\nattempts", xy=(2025, tot25), xytext=(2009, 300), fontsize=7,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.annotate("2015: first orbital\nbooster landing", xy=(2015, 87), xytext=(1995, 190), fontsize=7,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    note(ax, "Data: J. McDowell, GCAT (planet4589.org), updated 13 Oct 2026. Includes failures.")
    save(fig, "ch01_launches_year")


def payloads_by_year():
    py = G["payloads_launched_by_year"]
    sl = G["starlink_launched_by_year"]
    years = list(range(1990, 2026))
    tot = np.array([py.get(str(y), 0) for y in years])
    stl = np.array([sl.get(str(y), 0) for y in years])
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.bar(years, tot - stl, color=BLUE, label="All other payloads", zorder=2)
    ax.bar(years, stl, bottom=tot - stl, color=ORANGE, label="Starlink", zorder=2)
    ax.set_ylabel("Payloads launched per year")
    ax.legend(loc="upper left")
    ax.set_xlim(1989, 2026)
    for y in (2019, 2022, 2025):
        v = py.get(str(y), 0)
        ax.text(y, v + 60, f"{v:,}", ha="center", fontsize=7)
    note(ax, "Data: GCAT satellite catalogue, Oct 2026. 'Payload' = satellite or probe, including CubeSats.")
    save(fig, "ch01_payloads_year")


def in_orbit():
    t = G["in_orbit_by_type"]
    r = G["payloads_in_orbit_by_regime"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.1))
    labels = ["Payloads\n(active + dead)", "Debris\nfragments", "Rocket\nbodies", "Mission-related\ncomponents"]
    vals = [t["P"], t["D"], t["R"], t["C"]]
    w, _ = a1.pie(vals, colors=[BLUE, RED, GREY, GOLD], startangle=90, counterclock=False,
                  wedgeprops=dict(width=0.38, edgecolor="white"))
    a1.text(0, 0, f"{sum(vals):,}\ncatalogued\nobjects", ha="center", va="center", fontsize=8, weight="bold",
            color=NAVY)
    a1.legend(w, [f"{l.replace(chr(10), ' ')}: {v:,}" for l, v in zip(labels, vals)], loc="upper center",
              bbox_to_anchor=(0.5, 0.02), fontsize=6.8, ncol=2)
    a1.set_title("Objects in Earth orbit", fontsize=9)
    regs = ["LEO", "MEO", "GEO", "HEO/GTO"]
    v2 = [r.get(k, 0) for k in regs]
    a2.bar(regs, v2, color=[BLUE, VIOLET, RED, GOLD], zorder=2)
    a2.set_yscale("log")
    a2.set_ylim(100, 40000)
    for i, v in enumerate(v2):
        a2.text(i, v * 1.15, f"{v:,}", ha="center", fontsize=7.5)
    a2.set_title("Payloads in orbit by regime", fontsize=9)
    a2.set_ylabel("Number (log scale)")
    fig.text(0.99, -0.06, "Data: GCAT, 13 Oct 2026. Tracked objects ≳10 cm; ~1 million objects 1–10 cm are untracked.",
             ha="right", fontsize=6.5, color=GREY)
    save(fig, "ch01_in_orbit")


def economy():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.2), gridspec_kw=dict(width_ratios=[1, 1.25]))
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    vals = [424, 447, 469, 546, 570, 613, 686]
    a1.bar(years, vals, color=[SKY] * 6 + [ORANGE], zorder=2)
    for x, v in zip(years, vals):
        a1.text(x, v + 8, f"{v}", ha="center", fontsize=7)
    a1.set_ylabel("Global space economy (US$ billion)")
    a1.set_ylim(0, 760)
    a1.set_title("Growth of the space economy", fontsize=9)
    parts = [("Commercial space\nproducts & services,\ninfrastructure,\nsupport industries", 544.3, BLUE),
             ("Government\nspace budgets\n(civil + defence)", 141.0, ORANGE)]
    w, _ = a2.pie([p[1] for p in parts], colors=[p[2] for p in parts], startangle=90, counterclock=False,
                  wedgeprops=dict(width=0.42, edgecolor="white"))
    a2.text(0, 0, "2025\n$686 B", ha="center", va="center", fontsize=9, weight="bold", color=NAVY)
    a2.legend(w, [f"{p[0].replace(chr(10), ' ')}: ${p[1]:.0f} B" for p in parts], loc="upper center",
              bbox_to_anchor=(0.5, 0.0), fontsize=6.8)
    a2.set_title("Commercial vs government (2025)", fontsize=9)
    fig.text(0.99, -0.1, "Source: Space Foundation, The Space Report (2019–2025 editions; 2025 data released July 2026). "
             "Values in nominal US$.", ha="right", fontsize=6.3, color=GREY)
    save(fig, "ch01_economy")


def timeline_fig():
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.set_xlim(1954, 2029)
    ax.set_ylim(-9.2, 9.2)
    ax.axis("off")
    ev = [(1957, "Sputnik 1"), (1961, "Gagarin:\nfirst human"), (1962, "Telstar:\nlive TV relay"),
          (1965, "First EVA;\nMariner 4 at Mars"), (1969, "Apollo 11\nMoon landing"), (1971, "Salyut 1:\nfirst station"),
          (1972, "Landsat 1"), (1976, "Viking lands\non Mars"), (1977, "Voyagers\nlaunched"), (1981, "Space Shuttle"),
          (1986, "Mir"), (1990, "Hubble"), (1995, "GPS full\noperation"), (1998, "ISS assembly\nbegins"),
          (2003, "China's first\nastronaut"), (2004, "SpaceShipOne"), (2012, "Curiosity;\nDragon to ISS"),
          (2015, "Falcon 9 booster\nlands"), (2019, "Chang'e 4 far\nside; Starlink"), (2020, "Crew Dragon"),
          (2021, "JWST; Ingenuity;\nTiangong"), (2023, "Chandrayaan-3\nsouth-pole region"),
          (2024, "Chang'e 6 far-side\nsample; tower catch"), (2026, "Artemis II crew\naround the Moon; Roman")]
    ax.plot([1955, 2028], [0, 0], color=NAVY, lw=2.2)
    for k, x in enumerate(range(1960, 2030, 10)):
        ax.text(x, -0.55, str(x), ha="center", va="top", fontsize=7, color=GREY)
        ax.plot([x, x], [-0.2, 0.2], color=NAVY, lw=1)
    for i, (x, t) in enumerate(ev):
        lvl = [1.3, 4.0, 6.7][i % 3]
        sgn = 1 if (i // 1) % 2 == 0 else -1
        y = sgn * lvl
        ax.plot([x, x], [0, y * 0.93], color="#9AA5B1", lw=0.6)
        ax.plot([x], [0], "o", color=ORANGE, ms=4, zorder=4)
        ax.text(x, y, f"{x}\n{t}" if sgn > 0 else f"{t}\n{x}", ha="center", va="bottom" if sgn > 0 else "top",
                fontsize=5.9, linespacing=1.1, color=INK)
    save(fig, "ch01_timeline")


def cost_per_kg():
    data = [("Vanguard (1958)", 1958, 1_000_000, GREY), ("Saturn V (1967)", 1967, 5400, GREY),
            ("Space Shuttle (1981)", 1981, 54500, RED), ("Titan IV (1989)", 1989, 43000, GREY),
            ("Ariane 4 (1988)", 1988, 18000, VIOLET), ("Proton (1965)", 1975, 4300, RED),
            ("Delta II (1989)", 1990, 14000, GREY), ("Ariane 5 (1996)", 1996, 9000, VIOLET),
            ("Atlas V (2002)", 2002, 11000, BLUE), ("Long March 3B (1996)", 1997, 6000, GOLD),
            ("Electron (2017)", 2017, 25000, GREEN), ("Falcon 9 (2010)", 2010, 2700, ORANGE),
            ("Falcon Heavy (2018)", 2018, 1500, ORANGE), ("Starship goal", 2028, 200, ORANGE)]
    fig, ax = plt.subplots(figsize=(7.0, 3.7))
    for n, x, v, c in data:
        mk = "*" if "goal" in n else "o"
        ax.scatter(x, v, s=46 if mk == "o" else 110, color=c, zorder=3, marker=mk, edgecolor="white", lw=0.6)
        dy = {"Titan IV (1989)": 0.8, "Space Shuttle (1981)": 1.15, "Ariane 5 (1996)": 1.12, "Atlas V (2002)": 1.1,
              "Long March 3B (1996)": 0.62, "Delta II (1989)": 0.86, "Ariane 4 (1988)": 1.15}.get(n, 1.12)
        ha = "right" if n in ("Ariane 5 (1996)", "Ariane 4 (1988)") else "left"
        ax.text(x + (0.8 if ha == "left" else -0.8), v * dy, n, fontsize=6.8, va="bottom", ha=ha)
    ax.set_yscale("log")
    ax.set_ylim(100, 3e6)
    ax.set_xlim(1955, 2036)
    ax.set_ylabel("Approx. cost to LEO (2021 US$ per kg)")
    ax.set_xlabel("Year of first flight")
    note(ax, "Approximate: list price ÷ maximum LEO payload (reusable vehicles at commercial price). After NASA/CSIS "
             "compilations; real costs vary by mission.", fs=6.0, xy=(1.0, -0.17))
    save(fig, "ch01_cost_per_kg")


def ecosystem_map():
    fig, ax = canvas(7.4, 6.2, (0, 100), (0, 84))
    ax.add_patch(Circle((50, 42), 9.5, fc=NAVY, ec="none", zorder=3))
    ax.text(50, 42, "SPACE\nECOSYSTEM", ha="center", va="center", color="white", fontsize=9, weight="bold", zorder=4)
    nodes = [
        (50, 76, "Access to space", "Launch vehicles · reusability\nspaceports · ranges", VIOLET),
        (82, 66, "Earth orbit services", "EO · SAR · weather · comms\nGNSS · ISR · SIGINT", BLUE),
        (88, 42, "Space safety & security", "SSA · debris · space traffic\nmissile warning · resilience", RED),
        (80, 16, "Science", "Space weather · magnetosphere\nobservatories · Earth science", GREEN),
        (50, 7, "Exploration", "Moon · Mars · asteroids · outer\nplanets · sample return", GOLD),
        (19, 16, "Human spaceflight", "Stations · crew vehicles\nEVA · life support", ORANGE),
        (12, 42, "Near space & suborbital", "Balloons · HAPS · sounding\nrockets · spaceplanes", SKY),
        (18, 66, "Emerging frontiers", "ISAM · in-space manufacturing\nspace resources · new propulsion", "#8C564B"),
    ]
    for x, y, t, b, c in nodes:
        ax.plot([50, x], [42, y], color=c, lw=2.2, alpha=0.5, zorder=1)
        box(ax, x - 13.5, y - 5.6, 27, 11.2, fc="white", ec=c, lw=1.6, r=1.5, z=3)
        ax.text(x, y + 2.6, t, ha="center", va="center", fontsize=7.8, weight="bold", color=c, zorder=4)
        ax.text(x, y - 1.8, b, ha="center", va="center", fontsize=6.4, color=INK, zorder=4, linespacing=1.25)
    ax.add_patch(Circle((50, 42), 22, fc="none", ec=GREY, lw=0.8, ls="--", zorder=2))
    ax.text(50, 30.5, "Enablers: systems engineering · ground segment ·\nspectrum · AI & data · finance · law & policy · workforce",
            ha="center", va="center", fontsize=6.0, color=GREY, zorder=4, linespacing=1.3)
    save(fig, "ch01_ecosystem_map")


def actors():
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    names = ["United States", "China", "Japan", "France", "Russia", "Germany", "India", "Italy", "United Kingdom",
             "South Korea"]
    vals = [79.7, 19.9, 6.8, 4.2, 3.4, 2.6, 1.9, 1.5, 1.4, 0.8]
    hbar(ax, names, vals, fmt="${:.1f} B", highlight={"United States"}, color=SKY)
    ax.set_xlabel("Estimated government space spending, 2024 (US$ billion; civil + defence; ESA contributions "
                  "counted under members)")
    note(ax, "Approximate values compiled from Novaspace (Government Space Programs, 2025) and national budgets; "
         "China and Russia are estimates.", fs=6.0)
    save(fig, "ch01_gov_budgets")


def families():
    fam = G["families_2025"][:12]
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    hbar(ax, [f[0] for f in fam], [f[1] for f in fam], highlight={"Falcon 9"}, color=BLUE)
    ax.set_xlabel("Orbital launch attempts in 2025, by launch-vehicle family")
    note(ax, "Data: GCAT, Oct 2026. 'Long March' groups all CZ variants.")
    save(fig, "ch01_families_2025")


if __name__ == "__main__":
    regimes(); segments(); launches_by_year(); payloads_by_year(); in_orbit(); economy(); timeline_fig()
    cost_per_kg(); ecosystem_map(); actors(); families()
