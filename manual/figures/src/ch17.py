import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, RegularPolygon, Wedge

ROOT = Path(__file__).resolve().parents[2]
CC = json.load(open(ROOT / "data/comms_constellations.json"))
GC = json.load(open(ROOT / "data/gcat_stats.json"))


def history():
    fig, ax = plt.subplots(figsize=(7.0, 3.1))
    ev = [(1960.6, "Echo 1\n(passive balloon)"), (1962.5, "Telstar 1\n(first live TV\nacross Atlantic)"),
          (1963.6, "Syncom 2\n(first GSO)"), (1965.3, "Intelsat I\n'Early Bird'"), (1965.4, "Molniya 1"),
          (1983.3, "TDRS-1"), (1994.5, "DirecTV DBS"), (1998.4, "Iridium\n(LEO voice)"),
          (2004.0, "IPSTAR\n(early HTS)"), (2011.8, "ViaSat-1\n(140 Gbit/s)"), (2013.5, "O3b (MEO)"),
          (2017.0, "Iridium NEXT"), (2019.4, "Starlink\nfirst 60"), (2023.3, "ViaSat-3,\nJupiter 3"),
          (2024.1, "Direct-to-cell\nsatellites"), (2025.3, "Amazon Leo\nproduction")]
    timeline(ax, ev, y=0, x0=1958, x1=2028, stagger=3, height=1.0, fs=6.0)
    ax.set_xlim(1956, 2029)
    ax.set_ylim(-4.9, 4.9)
    ax.axis("off")
    for yr in range(1960, 2030, 10):
        ax.text(yr, -0.35, str(yr), fontsize=6.2, ha="center", va="top", color=GREY)
    save(fig, "ch17_history")


def rain():
    tab = [(1, 2.59e-5, 0.9691), (2, 8.47e-5, 1.0664), (4, 1.071e-4, 1.6009), (6, 7.056e-4, 1.59),
           (8, 4.115e-3, 1.3905), (10, 1.217e-2, 1.2571), (12, 2.386e-2, 1.1825), (15, 4.481e-2, 1.1233),
           (20, 9.164e-2, 1.0568), (25, 0.1571, 0.9991), (30, 0.2403, 0.9485), (35, 0.3374, 0.9047),
           (40, 0.4431, 0.8673), (50, 0.66, 0.8084), (60, 0.8606, 0.7656)]
    f = np.array([t[0] for t in tab])
    lk = np.log10([t[1] for t in tab])
    al = np.array([t[2] for t in tab])
    ff = np.logspace(0, np.log10(60), 300)
    k = 10 ** np.interp(np.log10(ff), np.log10(f), lk)
    a = np.interp(np.log10(ff), np.log10(f), al)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for R, c in [(5, SKY), (12.5, BLUE), (25, NAVY), (50, ORANGE), (100, RED)]:
        ax.plot(ff, k * R ** a * 5.0, color=c, lw=1.6, label=f"{R:g} mm/h")
    for x0, x1, n in [(3.4, 7, "C"), (10.7, 14.5, "Ku"), (17.7, 31, "Ka"), (37.5, 51.4, "Q/V")]:
        ax.axvspan(x0, x1, color=GOLD, alpha=0.13)
        ax.text(np.sqrt(x0 * x1), 0.012, n, ha="center", fontsize=7, color="#7A5C00")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 60)
    ax.set_ylim(0.01, 300)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Rain attenuation (dB)")
    ax.legend(fontsize=6.6, title="Rain rate", title_fontsize=6.8, loc="upper left")
    note(ax, "Specific attenuation from ITU-R P.838-3 coefficients (horizontal polarisation) over a 5 km effective path.",
         xy=(1, -0.16))
    save(fig, "ch17_rain")


def latency():
    h = np.logspace(np.log10(300), np.log10(40000), 200)
    c = 299792.458
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.plot(h, 4 * h / c * 1000, color=NAVY, lw=1.6, label="Minimum round trip, bent pipe (4h/c)")
    pts = [("Starlink 550 km", 550), ("Iridium 780 km", 780), ("OneWeb 1 200 km", 1200),
           ("O3b mPOWER (MEO) 8 062 km", 8062), ("GEO 35 786 km", 35786)]
    for n, x in pts:
        y = 4 * x / c * 1000
        ax.plot(x, y, "o", color=ORANGE, ms=5, zorder=3)
        ax.annotate(f"{n}: {y:.0f} ms", (x, y), xytext=(-8, 6) if x > 5000 else (8, -9), textcoords="offset points", fontsize=6.5, ha="right" if x > 5000 else "left")
    ax.axhline(70, color=GREEN, lw=0.9, ls="--")
    ax.text(320, 76, "London–New York over fibre ≈ 70 ms", fontsize=6.5, color=GREEN)
    ax.axhspan(100, 150, color=GREY, alpha=0.08)
    ax.text(320, 112, "interactive voice/video comfortable below ≈ 150 ms", fontsize=6.4, color=GREY)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(300, 50000)
    ax.set_ylim(2, 1000)
    ax.set_xlabel("Satellite altitude (km)")
    ax.set_ylabel("Round-trip time (ms)")
    ax.legend(fontsize=6.6, loc="lower right")
    note(ax, "Propagation only, satellite overhead; real systems add slant range, routing, processing and queuing.",
         xy=(1, -0.16))
    save(fig, "ch17_latency")


def reuse():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw=dict(width_ratios=[1.25, 1]))
    cols = [BLUE, ORANGE, GREEN, VIOLET]
    r = 1.0
    for i in range(-4, 5):
        for j in range(-3, 4):
            x = i * 1.5 * r
            y = j * np.sqrt(3) * r + (i % 2) * np.sqrt(3) / 2 * r
            c = cols[(i % 2) * 2 + (j % 2)]
            a1.add_patch(RegularPolygon((x, y), 6, radius=r * 0.98, orientation=np.pi / 6, fc=c, alpha=0.55,
                                        ec="white", lw=1))
    a1.set_xlim(-6, 6)
    a1.set_ylim(-5, 5)
    a1.set_aspect("equal")
    a1.axis("off")
    a1.set_title("Four-colour reuse of spot beams", fontsize=7.8)
    for k, (c, t) in enumerate(zip(cols, ["band 1, RHCP", "band 2, RHCP", "band 1, LHCP", "band 2, LHCP"])):
        a2.add_patch(Rectangle((0.05, 0.78 - k * 0.13), 0.08, 0.08, fc=c, alpha=0.7, transform=a2.transAxes))
        a2.text(0.17, 0.82 - k * 0.13, t, fontsize=7, va="center", transform=a2.transAxes)
    a2.text(0.05, 0.22, "Total spectrum is divided into 2 sub-bands × 2 polarisations.\n"
            "Every cell reuses half the band; neighbours always differ.\n"
            "With 100 beams, the same spectrum is reused ≈ 25 times.", fontsize=6.6, transform=a2.transAxes,
            va="center")
    a2.axis("off")
    save(fig, "ch17_reuse")


def capacity():
    geo = [(1965.3, 0.015, "Early Bird"), (1971.1, 0.25, "Intelsat IV"), (1989.8, 1.5, "Intelsat VI"),
           (2005.6, 45, "IPSTAR"), (2010.9, 90, "KA-SAT"), (2011.8, 140, "ViaSat-1"), (2016.9, 220, "Jupiter 2"),
           (2017.4, 260, "ViaSat-2"), (2023.6, 500, "Jupiter 3"), (2023.3, 1000, "ViaSat-3 (design)")]
    leo = [(2019.4, 20, "Starlink v1 (est.)"), (2023.2, 100, "Starlink V2 Mini (est.)"), (2026.7, 1000, "Starlink V3 (stated)")]
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    pos = {"Early Bird": (1966, 0.015, "left", "center"), "Intelsat IV": (1972, 0.25, "left", "center"),
           "Intelsat VI": (1990.6, 1.5, "left", "center"), "IPSTAR": (2004.8, 45, "right", "center"),
           "KA-SAT": (2010.2, 115, "right", "bottom"), "ViaSat-1": (2012.4, 105, "left", "top"),
           "Jupiter 2": (2017.6, 175, "left", "top"), "ViaSat-2": (2016.8, 330, "right", "bottom"),
           "Jupiter 3": (2024.3, 430, "left", "center"), "ViaSat-3 (design)": (2022.6, 1250, "right", "bottom"),
           "Starlink v1 (est.)": (2020.1, 15, "left", "top"), "Starlink V2 Mini (est.)": (2023.9, 75, "left", "top"),
           "Starlink V3 (stated)": (2026.7, 1700, "center", "bottom")}
    x, y, n = zip(*geo)
    ax.plot(x, y, "o", color=NAVY, ms=5, label="GEO satellites")
    x2, y2, n2 = zip(*leo)
    ax.plot(x2, y2, "s", mfc="white", mec=ORANGE, mew=1.4, ms=5.5, label="LEO, per satellite")
    for xi, yi, ni in geo + leo:
        tx, ty, ha, va = pos[ni]
        ax.text(tx, ty, ni, fontsize=6.3, ha=ha, va=va, color=ORANGE if "Starlink" in ni else INK)
    ax.set_yscale("log")
    ax.set_xlim(1962, 2032)
    ax.set_ylim(0.005, 5000)
    ax.set_xlabel("Launch year")
    ax.set_ylabel("Throughput per satellite (Gbit/s)")
    ax.legend(fontsize=6.6, loc="upper left")
    note(ax, "Early satellites converted from voice circuits at 64 kbit/s. Operator figures; LEO values are estimates "
             "or company statements.", xy=(1, -0.16))
    save(fig, "ch17_capacity")


def waterfall():
    steps = [("Satellite EIRP", 52.0), ("Free-space loss\n(38 000 km, 12 GHz)", -205.6), ("Atmosphere,\npointing", -1.0),
             ("Dish gain\n(60 cm)", 35.7), ("System noise\ntemp. (120 K)", -20.8), ("Boltzmann\nconstant", 228.6),
             ("Bandwidth\n(27 MHz)", -74.3)]
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    cum = 0
    for i, (n, v) in enumerate(steps):
        lo, hi = (cum, cum + v) if v > 0 else (cum + v, cum)
        ax.bar(i, hi - lo, bottom=lo, color=GREEN if v > 0 else RED, width=0.62, alpha=0.85)
        ax.text(i, hi + 6, f"{v:+.1f}", ha="center", fontsize=6.6)
        if i < len(steps) - 1:
            ax.plot([i + 0.31, i + 0.69], [cum + v, cum + v], color=GREY, lw=0.6)
        cum += v
    ax.bar(len(steps), cum, color=NAVY, width=0.62)
    ax.text(len(steps), cum + 6, f"C/N = {cum:.1f} dB", ha="center", fontsize=7, weight="bold")
    ax.set_xticks(range(len(steps) + 1))
    ax.set_xticklabels([s[0] for s in steps] + ["Result"], fontsize=6.3)
    ax.set_ylabel("Cumulative level (dB)")
    ax.set_ylim(-200, 300)
    ax.axhline(0, color=INK, lw=0.6)
    ax.grid(axis="x", visible=False)
    note(ax, "Ku-band direct-to-home TV downlink. DVB-S2 8PSK rate 3/4 needs ≈ 8 dB, leaving ≈ 6.6 dB for rain fade.",
         xy=(1, -0.2))
    save(fig, "ch17_waterfall")


def constellations():
    d = CC["counts"]
    items = sorted(d.items(), key=lambda kv: -kv[1])
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    labels = [k for k, _ in items]
    vals = [v for _, v in items]
    y = np.arange(len(labels))
    ax.barh(y, vals, color=[ORANGE if "Starlink" in k else BLUE for k in labels], height=0.65)
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=6.8)
    ax.invert_yaxis()
    for yi, v in zip(y, vals):
        ax.text(v * 1.08, yi, f"{v:,}", va="center", fontsize=6.6)
    ax.set_xlim(5, 40000)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Active satellites, 14 October 2026 (log scale)")
    note(ax, "Name-matched active payloads in the CelesTrak SATCAT; includes satellites still raising orbit.",
         xy=(1, -0.16))
    save(fig, "ch17_constellations")


def starlink_growth():
    d = GC["starlink_launched_by_year"]
    yrs = sorted(int(k) for k in d)
    v = [d[str(k)] for k in yrs]
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    ax.bar(yrs, v, color=BLUE, width=0.65, label="Launched in year")
    ax2 = ax.twinx()
    ax2.plot(yrs, np.cumsum(v), "o-", color=ORANGE, lw=1.5, ms=4, label="Cumulative launched")
    ax2.grid(False)
    ax2.set_ylabel("Cumulative", color=ORANGE)
    for x, y in zip(yrs, v):
        ax.text(x, y + 50, f"{y:,}", ha="center", fontsize=6.4)
    ax.set_ylabel("Satellites launched")
    ax.set_xlabel("Year (2026 to mid-October)")
    ax.set_ylim(0, 3600)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=6.6, loc="upper left")
    note(ax, f"Source: GCAT (J. McDowell). {GC['starlink_in_orbit']:,} Starlink satellites in orbit on 13 Oct 2026."
         if isinstance(GC['starlink_in_orbit'], int) else
         f"Source: GCAT (J. McDowell). About {int(GC['starlink_in_orbit']):,} Starlink satellites in orbit in mid-October 2026.",
         xy=(1, -0.18))
    save(fig, "ch17_starlink")


def shells():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    cols = {"Starlink (SpaceX)": ORANGE, "OneWeb (Eutelsat)": BLUE, "Amazon Leo (Kuiper)": GREEN,
            "Qianfan / Spacesail (China)": RED, "Guowang (China SatNet)": VIOLET, "Iridium NEXT": NAVY,
            "Globalstar": GOLD, "Rassvet (Bureau 1440, Russia)": GREY}
    for k, c in cols.items():
        p = np.array(CC["shells"].get(k, []))
        if len(p) == 0:
            continue
        sel = (p[:, 0] > 250) & (p[:, 0] < 1600)
        ax.scatter(p[sel, 1], p[sel, 0], s=3 if "Starlink" in k else 6, color=c, alpha=0.5 if "Starlink" in k else 0.8,
                   label=k, lw=0)
    ax.set_xlabel("Inclination (°)")
    ax.set_ylabel("Mean altitude (km)")
    ax.set_xlim(25, 105)
    ax.set_ylim(250, 1600)
    lg = ax.legend(fontsize=6.2, loc="upper left", markerscale=3, ncol=2)
    note(ax, "Each dot is an active satellite (CelesTrak SATCAT, Oct 2026). Dots below the shells are satellites "
             "raising or lowering orbit.", xy=(1, -0.15))
    save(fig, "ch17_shells")


def payload():
    fig, ax = canvas(7.0, 3.2, xlim=(0, 100), ylim=(0, 44))
    label(ax, 50, 42, "Bent-pipe (transparent) transponder", fs=7.6, weight="bold")
    blocks = [("Receive\nantenna", 1), ("LNA", 14), ("Input filter\n& down-\nconverter", 27), ("Input mux\n(channels)", 40),
              ("Channel\namplifiers\nTWTA / SSPA", 53), ("Output\nmux", 66), ("Transmit\nantenna", 79)]
    for n, x in blocks:
        box(ax, x, 26, 11, 12, n, fs=6.4, fc=LIGHT)
    for (_, x1), (_, x2) in zip(blocks[:-1], blocks[1:]):
        arrow(ax, (x1 + 11, 32), (x2, 32))
    label(ax, 50, 21.5, "uplink e.g. 14 GHz → downlink 12 GHz; signal is filtered, shifted and amplified but not decoded",
          fs=6.4, color=GREY)
    label(ax, 50, 16, "Regenerative / digital payload", fs=7.6, weight="bold")
    blocks2 = [("Receive\nphased array", 1), ("LNA &\nADC", 16), ("Digital processor: demodulate, route,\nswitch, "
                                                                    "beamform, remodulate", 31), ("DAC &\namplifiers", 66),
               ("Transmit\nphased array", 81)]
    widths = [13, 12, 32, 12, 14]
    for (n, x), w in zip(blocks2, widths):
        box(ax, x, 2, w, 11, n, fs=6.4, fc="#FFF4E5" if "Digital" in n else LIGHT, ec=ORANGE if "Digital" in n else NAVY)
    for i in range(len(blocks2) - 1):
        arrow(ax, (blocks2[i][1] + widths[i], 7.5), (blocks2[i + 1][1], 7.5))
    save(fig, "ch17_payload")


def terminals():
    items = [("Smartphone (direct-to-cell, 2 GHz)", 0.0), ("Handheld satellite phone (L-band)", 2.0),
             ("Starlink user terminal (Ku, ≈0.5 m²)", 10 * np.log10(0.6 * 4 * np.pi * 0.5 / (0.025 ** 2))),
             ("60 cm TV dish (Ku, 12 GHz)", 10 * np.log10(0.65 * (np.pi * 0.6 / 0.025) ** 2)),
             ("1.2 m VSAT (Ka, 20 GHz)", 10 * np.log10(0.65 * (np.pi * 1.2 / 0.015) ** 2)),
             ("7.3 m gateway (Ka, 20 GHz)", 10 * np.log10(0.65 * (np.pi * 7.3 / 0.015) ** 2)),
             ("AST BlueBird array in orbit (≈ 223 m², 0.85 GHz)", 10 * np.log10(0.6 * 4 * np.pi * 223 / (0.353 ** 2)))]
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    hbar(ax, [i[0] for i in items], [i[1] for i in items], color=BLUE, fmt="{:.0f} dBi", fs=6.6,
         highlight=["Smartphone (direct-to-cell, 2 GHz)", "AST BlueBird array in orbit (≈ 223 m², 0.85 GHz)"])
    ax.tick_params(axis="y", labelsize=6.6)
    ax.set_xlabel("Antenna gain (dBi)")
    note(ax, "G = η(πD/λ)² or 4πAη/λ² with η ≈ 0.6–0.65. A phone's missing ≈ 35 dB must be supplied by a huge "
             "antenna in orbit.", xy=(1, -0.17))
    save(fig, "ch17_terminals")


def laser_mesh():
    fig, ax = canvas(7.0, 3.0, xlim=(0, 100), ylim=(0, 40))
    earth(ax, 50, -105, 120, atmosphere=False)
    ys = [24, 32]
    pos = {}
    for j, y in enumerate(ys):
        for i, x in enumerate(np.arange(8 + j * 6, 95, 14)):
            yy = y - 0.004 * (x - 50) ** 2
            pos[(j, i)] = (x, yy)
            satellite(ax, x, yy, s=0.7)
    for (j, i), (x, y) in pos.items():
        if (j, i + 1) in pos:
            ax.plot([x, pos[(j, i + 1)][0]], [y, pos[(j, i + 1)][1]], color=RED, lw=1.2)
        if j == 0 and (1, i) in pos:
            ax.plot([x, pos[(1, i)][0]], [y, pos[(1, i)][1]], color=VIOLET, lw=1, ls="--")
    ax.plot([pos[(0, 0)][0], 6], [pos[(0, 0)][1], 13], color=GREEN, lw=1.2)
    label(ax, 6, 11, "user", fs=6.6, color=GREEN)
    ax.plot([pos[(0, 6)][0], 94], [pos[(0, 6)][1], 13], color=GREEN, lw=1.2)
    label(ax, 94, 11, "gateway", fs=6.6, color=GREEN)
    label(ax, 50, 38.5, "red: in-plane laser links   violet: cross-plane laser links   green: radio links", fs=6.6,
          color=GREY)
    label(ax, 50, 6, "Optical links of up to ≈ 100 Gbit/s route traffic across oceans without ground stations", fs=6.6,
          color="white")
    save(fig, "ch17_lasermesh")


def gso_arc():
    phi = np.radians(40.0)
    dl = np.radians(np.linspace(-75, 75, 300))
    cg = np.cos(dl) * np.cos(phi)
    el = np.degrees(np.arctan((cg - 0.1513) / np.sqrt(1 - cg ** 2)))
    az = 180 + np.degrees(np.arctan2(np.tan(dl), np.sin(phi)))
    m = el > 0
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.fill_between(az[m], np.maximum(el[m] - 12, 0), el[m] + 12, color=RED, alpha=0.12, lw=0)
    ax.plot(az[m], el[m], color=GOLD, lw=2, label="Geostationary arc seen from 40° N")
    t = np.linspace(0, 1, 200)
    tracks = [(95, 15, 260, 70), (110, 70, 250, 10), (140, 5, 225, 85), (200, 80, 265, 20)]
    for k, (a0, e0, a1, e1) in enumerate(tracks):
        A = a0 + (a1 - a0) * t
        E = e0 + (e1 - e0) * t + 18 * np.sin(np.pi * t)
        Eg = np.interp(A, az[m], el[m])
        inside = np.abs(E - Eg) < 12
        ax.plot(np.where(inside, np.nan, A), E, color=GREEN, lw=1.3, label="LEO pass (usable)" if k == 0 else None)
        ax.plot(np.where(inside, A, np.nan), E, color=GREY, lw=1.3, ls=":", label="Pass segment avoided" if k == 0 else None)
    ax.text(180, 50, "exclusion zone (illustrative ±12°)", fontsize=6.6, color=RED, ha="center")
    ax.set_xlim(90, 270)
    ax.set_ylim(0, 90)
    ax.set_xticks([90, 135, 180, 225, 270])
    ax.set_xticklabels(["E", "SE", "S", "SW", "W"])
    ax.set_xlabel("Azimuth seen by a ground terminal")
    ax.set_ylabel("Elevation (°)")
    ax.legend(fontsize=6.4, loc="upper right")
    note(ax, "ITU EPFD limits protect GEO networks: non-geostationary systems must not transmit along the line of sight "
             "to the GEO arc.", xy=(1, -0.16))
    save(fig, "ch17_gsoarc")


if __name__ == "__main__":
    fns = [history, rain, latency, reuse, capacity, waterfall, constellations, starlink_growth, shells, payload,
           terminals, laser_mesh, gso_arc]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
