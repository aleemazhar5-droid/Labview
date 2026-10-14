import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[2]
G = json.loads((ROOT / "data/gcat_stats.json").read_text())
GX = json.loads((ROOT / "data/gcat_extra.json").read_text())
RE = 6378.137
MU = 398600.4418


def geometry():
    fig, ax = canvas(7.0, 4.2, (0, 100), (0, 60))
    cx, cy, R = 30, -40, 70
    th = np.linspace(np.radians(50), np.radians(130), 300)
    ax.plot(cx + R * np.cos(th), cy + R * np.sin(th), color=EARTH, lw=2.5)
    ax.fill_between(cx + R * np.cos(th), cy + R * np.sin(th), -20, color="#DCEBF7")
    sat = (cx, cy + R + 22)
    satellite(ax, *sat, 1.4)
    tgt_ang = np.radians(62)
    tgt = (cx + R * np.cos(tgt_ang), cy + R * np.sin(tgt_ang))
    ax.plot([cx, sat[0]], [cy + R - 2, sat[1]], color=GREY, ls="--", lw=0.8)
    ax.plot([sat[0], tgt[0]], [sat[1], tgt[1]], color=ORANGE, lw=1.6)
    ax.plot(*tgt, "o", color=RED, ms=6)
    ax.text(tgt[0] + 1.5, tgt[1] - 3, "ground terminal /\nimaged point", fontsize=7)
    tx = (np.cos(tgt_ang + np.pi / 2), np.sin(tgt_ang + np.pi / 2))
    ax.plot([tgt[0] - 18 * tx[0], tgt[0] + 10 * tx[0]], [tgt[1] - 18 * tx[1], tgt[1] + 10 * tx[1]], color=GREEN, lw=1,
            ls=":")
    ax.text(tgt[0] - 2, tgt[1] + 11, "local\nhorizon", fontsize=6.5, color=GREEN, ha="right")
    ax.text(tgt[0] - 9, tgt[1] + 2.5, "ε", fontsize=11, color=GREEN)
    ax.add_patch(Arc(sat, 14, 14, theta1=-90 - 0, theta2=np.degrees(np.arctan2(tgt[1] - sat[1], tgt[0] - sat[0])), color=VIOLET))
    ax.text(sat[0] + 2.5, sat[1] - 9, "η", fontsize=11, color=VIOLET)
    ax.text((sat[0] + tgt[0]) / 2 + 2, (sat[1] + tgt[1]) / 2 + 1, "slant range ρ", fontsize=7, color=ORANGE)
    ax.text(sat[0] - 2, sat[1] - 11, "h", fontsize=10, color=GREY, ha="right")
    ax.text(60, 52, "sin η = (R / (R + h)) cos ε\nλ = 90° − η − ε  (Earth central angle)\nρ = R sin λ / sin η\n"
            "coverage area = 2πR²(1 − cos λ)", fontsize=7.6, va="top",
            bbox=dict(fc="#F3F6F9", ec=GREY, lw=0.5, pad=4))
    ax.text(cx + 2, 22, "Earth", fontsize=8, color=EARTH)
    save(fig, "ch11_geometry")


def footprint_vs_alt():
    h = np.logspace(np.log10(200), np.log10(36000), 300)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.3))
    for el, c in [(0, GREY), (10, BLUE), (25, ORANGE), (40, RED)]:
        e = np.radians(el)
        eta = np.arcsin(RE / (RE + h) * np.cos(e))
        lam = np.pi / 2 - eta - e
        a1.loglog(h, lam * RE, color=c, label=f"ε ≥ {el}°")
        n = np.sqrt(MU / (RE + h) ** 3)
        tpass = 2 * lam / (n - 7.29e-5 * 0.5) / 60
        a2.loglog(h, tpass, color=c)
    a1.set_xlabel("Altitude (km)")
    a1.set_ylabel("Coverage radius (km, ground arc)")
    a1.legend(fontsize=7)
    a2.set_xlabel("Altitude (km)")
    a2.set_ylabel("Max. pass duration overhead (min)")
    a2.set_ylim(1, 3000)
    a2.axhline(1440, color=GREY, ls=":", lw=0.7)
    a2.text(220, 1600, "GEO: always visible", fontsize=6.6, color=GREY)
    save(fig, "ch11_footprint")


def alt_histogram():
    C = json.loads((ROOT / "data/celestrak_stats.json").read_text())
    hist, ha = C["hist"], C["hist_active"]
    xs = np.array(sorted(int(k) for k in hist))
    ys = np.array([hist[str(k)] for k in xs])
    ya = np.array([ha.get(str(k), 0) for k in xs])
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.bar(xs + 12.5, ys, width=24, color="#C9D3DD", zorder=2, label="All catalogued objects (incl. debris, rocket bodies)")
    ax.bar(xs + 12.5, ya, width=24, color=BLUE, zorder=3, label="Operational payloads")
    ax.set_xlim(150, 2100)
    ax.set_xlabel("Mean orbital altitude (km), 25 km bins")
    ax.set_ylabel("Objects in orbit")
    ax.legend(fontsize=7, loc="upper right")
    for x, t, f in [(470, "Starlink\n(≈ 480–560 km)", 0.75), (790, "Iridium, sun-synchronous\nEO & debris (≈ 750–900 km)", 0.32),
                    (1200, "OneWeb\n1 200 km", 0.2), (1414, "Globalstar\n1 414 km", 0.12)]:
        ax.annotate(t, xy=(x, ys[np.argmin(abs(xs - x))]), xytext=(x + 60, ys.max() * f), fontsize=6.6,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.5))
    note(ax, f"Data: CelesTrak SATCAT, October 2026 ({C['in_orbit']:,} objects in Earth orbit, {C['active']:,} operational "
             "payloads); current apogee/perigee.", xy=(1, -0.16))
    save(fig, "ch11_alt_hist")


def constellation_views():
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.6))

    def view(ax, planes, inc, a, nsat, phase_f, title, col):
        ax.set_aspect("equal")
        ax.axis("off")
        el, az = np.radians(20), np.radians(30)

        def proj(X, Y, Z):
            x1 = X * np.cos(az) - Y * np.sin(az)
            y1 = X * np.sin(az) + Y * np.cos(az)
            depth = y1 * np.cos(el) - Z * np.sin(el)
            return x1, y1 * np.sin(el) + Z * np.cos(el), depth
        ax.add_patch(Circle((0, 0), 1.0, fc=EARTH, ec="#1D4F8C", zorder=2))
        u = np.linspace(0, 2 * np.pi, 300)
        for p in range(planes):
            raan = 2 * np.pi * p / planes * (1 if inc < 80 else 0.5)
            i = np.radians(inc)
            X = a * (np.cos(raan) * np.cos(u) - np.sin(raan) * np.sin(u) * np.cos(i))
            Y = a * (np.sin(raan) * np.cos(u) + np.cos(raan) * np.sin(u) * np.cos(i))
            Z = a * np.sin(u) * np.sin(i)
            px, py, d = proj(X, Y, Z)
            front = ~((px ** 2 + py ** 2 < 1.0) & (d > 0))
            ax.plot(np.where(front, px, np.nan), np.where(front, py, np.nan), color=col, lw=0.8, zorder=3)
            for k in range(nsat):
                uk = 2 * np.pi * k / nsat + 2 * np.pi * phase_f * p / (planes * nsat)
                Xs = a * (np.cos(raan) * np.cos(uk) - np.sin(raan) * np.sin(uk) * np.cos(i))
                Ys = a * (np.sin(raan) * np.cos(uk) + np.cos(raan) * np.sin(uk) * np.cos(i))
                Zs = a * np.sin(uk) * np.sin(i)
                sx, sy, sd = proj(Xs, Ys, Zs)
                if not (sx ** 2 + sy ** 2 < 1.0 and sd > 0):
                    ax.plot(sx, sy, "o", color=ORANGE, ms=3.2, zorder=4, mec=NAVY, mew=0.3)
        ax.set_xlim(-a * 1.1, a * 1.1)
        ax.set_ylim(-a * 1.1, a * 1.1)
        ax.set_title(title, fontsize=8)
    view(axs[0], 6, 55, 4.17, 4, 1, "Walker delta 24/6/1 at 20 200 km, i = 55°\n(GPS-like MEO constellation)", BLUE)
    view(axs[1], 6, 86.4, 1.12, 11, 1, "Polar 'street-of-coverage' 66/6, i = 86.4°\n(Iridium-like, 780 km; altitude exaggerated)",
         GREEN)
    save(fig, "ch11_constellations")


def sats_for_coverage():
    h = np.logspace(np.log10(400), np.log10(36000), 300)
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    for el, c in [(10, BLUE), (25, ORANGE), (40, RED)]:
        e = np.radians(el)
        eta = np.arcsin(RE / (RE + h) * np.cos(e))
        lam = np.pi / 2 - eta - e
        N = 1.8 * 2 / (1 - np.cos(lam))
        ax.loglog(h, N, color=c, label=f"minimum elevation {el}°")
    pts = [("Iridium (66, 780 km)", 780, 66), ("Globalstar (48, 1 414 km)", 1414, 48), ("O3b mPOWER (13, 8 062 km)", 8062, 13),
           ("GPS (24 baseline, 20 200 km)", 20200, 24), ("OneWeb Gen 1 (648, 1 200 km)", 1200, 648),
           ("Starlink (≈ 10 000, 480–560 km)", 520, 10000), ("Three GEO satellites (no poles)", 35786, 3)]
    for n, x, y in pts:
        ax.plot(x, y, "o", color=NAVY, ms=4)
        ax.text(x * 1.08, y * 1.15, n, fontsize=6.4)
    ax.set_xlabel("Altitude (km)")
    ax.set_ylabel("Satellites for continuous global coverage")
    ax.legend(fontsize=7, loc="upper right")
    note(ax, "Approximate: N ≈ 1.8 × 4π / cap area (overlap factor 1.8). Broadband constellations use far more satellites "
             "than coverage needs, to provide capacity and high elevation angles.", xy=(1, -0.16))
    save(fig, "ch11_sats_coverage")


def mega():
    data = [("Starlink (SpaceX)", 10655, 15000, BLUE), ("Eutelsat OneWeb", 654, 648 + 1280, VIOLET),
            ("Amazon Leo (Kuiper)", 392, 3232, ORANGE), ("Qianfan / Thousand Sails (China)", 239, 14000, RED),
            ("Guowang / China SatNet", 204, 13000, RED), ("AST SpaceMobile (D2D)", 13, 248, GREEN),
            ("SDA Transport & Tracking Layers", 42, 1000, NAVY), ("Telesat Lightspeed", 0, 198, GREY),
            ("IRIS² (EU)", 0, 348 + 66, GOLD)]
    fig, ax = plt.subplots(figsize=(7.0, 3.7))
    y = np.arange(len(data))
    ax.barh(y, [d[2] for d in data], color="#E3E8EE", height=0.65, label="Planned / authorised (first-generation goal)")
    ax.barh(y, [max(d[1], 0.5) for d in data], color=[d[3] for d in data], height=0.65, label="In orbit, Oct 2026")
    for k, d in enumerate(data):
        ax.text(max(d[2], 1) * 1.15, k, f"{d[1]:,} / {d[2]:,}", va="center", fontsize=6.8)
    ax.set_yticks(y)
    ax.set_yticklabels([d[0] for d in data], fontsize=7.4)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(1, 1.5e5)
    ax.set_xlabel("Number of satellites (log scale)")
    ax.legend(fontsize=6.8, loc="lower right")
    ax.grid(axis="y", visible=False)
    note(ax, "In-orbit counts: GCAT (Oct 2026) and company/agency reports; planned numbers are first-generation "
             "authorisations or declared targets and change frequently.", xy=(1, -0.16))
    save(fig, "ch11_mega")


def shells():
    pts = [("Starlink Gen1 shells", [(550, 53.0), (540, 53.2), (570, 70.0), (560, 97.6)], BLUE),
           ("Starlink Gen2 (V2 Mini)", [(525, 53.0), (530, 43.0), (535, 33.0), (480, 53.0)], SKY),
           ("Amazon Leo", [(590, 33.0), (610, 42.0), (630, 51.9)], ORANGE), ("OneWeb", [(1200, 87.9)], VIOLET),
           ("Iridium NEXT", [(780, 86.4)], GREEN), ("Globalstar", [(1414, 52.0)], GOLD),
           ("Qianfan (first shell)", [(800, 89.0)], RED), ("ISS / Tiangong", [(415, 51.6), (385, 41.5)], GREY)]
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    for n, p, c in pts:
        ax.scatter([q[1] for q in p], [q[0] for q in p], s=46, color=c, label=n, zorder=3, edgecolor="white")
    ax.set_xlabel("Inclination (deg)")
    ax.set_ylabel("Altitude (km)")
    ax.legend(fontsize=6.6, ncol=2, loc="upper left")
    ax.set_ylim(350, 1550)
    note(ax, "Representative published shells; constellations are reconfigured over time (e.g., Starlink lowering "
             "shells from ≈ 550 to ≈ 480 km during 2026).", xy=(1, -0.16))
    save(fig, "ch11_shells")


def mass_classes():
    mc = GX["mass_class_by_year"]
    years = [str(y) for y in range(2010, 2026)]
    cls = ["<10 kg", "10–100 kg", "100–500 kg", "500–2500 kg", ">2500 kg"]
    cols = [GREEN, SKY, BLUE, ORANGE, RED]
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    bottom = np.zeros(len(years))
    for c, col in zip(cls, cols):
        v = np.array([mc.get(y, {}).get(c, 0) for y in years])
        ax.bar([int(y) for y in years], v, bottom=bottom, color=col, label=c, width=0.8, zorder=2)
        bottom += v
    ax.set_ylabel("Payloads launched")
    ax.legend(fontsize=7, title="Launch mass", title_fontsize=7, loc="upper left")
    note(ax, "Data: GCAT. Starlink V1/V1.5 (≈ 260–310 kg) fill the 100–500 kg class to 2022; V2 Mini (≈ 800 kg) and Amazon "
             "Leo (≈ 600 kg) fill the 500–2 500 kg class from 2023.", xy=(1, -0.15))
    save(fig, "ch11_mass_classes")


def cubesat_sizes():
    fig, ax = canvas(7.0, 3.0, (0, 100), (0, 38))
    items = [("1U\n10×10×11 cm\n≤ 2 kg", 1, 1), ("3U\n10×10×34 cm\n≤ 6 kg", 1, 3), ("6U\n10×22×34 cm\n≤ 14 kg", 2, 3),
             ("12U\n22×22×34 cm\n≤ 24 kg", 4, 3), ("16U\n22×22×45 cm\n≤ 32 kg", 4, 4)]
    x = 3
    for t, w, hgt in items:
        ww = 4.2 * (2 if w >= 2 else 1)
        dd = 4.2 * (2 if w == 4 else 1)
        hh = 4.0 * hgt
        y0 = 6
        ax.add_patch(Polygon([(x, y0), (x + ww, y0), (x + ww, y0 + hh), (x, y0 + hh)], fc="#C9D3DD", ec=NAVY))
        ax.add_patch(Polygon([(x, y0 + hh), (x + ww, y0 + hh), (x + ww + dd * 0.5, y0 + hh + dd * 0.4),
                              (x + dd * 0.5, y0 + hh + dd * 0.4)], fc="#E3E8EE", ec=NAVY))
        ax.add_patch(Polygon([(x + ww, y0), (x + ww + dd * 0.5, y0 + dd * 0.4), (x + ww + dd * 0.5, y0 + hh + dd * 0.4),
                              (x + ww, y0 + hh)], fc="#AEB9C4", ec=NAVY))
        for k in range(1, hgt):
            ax.plot([x, x + ww], [y0 + 4.0 * k, y0 + 4.0 * k], color=NAVY, lw=0.4)
        ax.text(x + ww / 2, 1.5, t, ha="center", va="center", fontsize=6.3)
        x += ww + dd * 0.5 + 9
    ax.text(97, 34, "CubeSat Design Specification (Cal Poly, rev. 14):\n1U = 10 cm cube; rails slide in a\nspring-loaded deployer",
            fontsize=6.6, ha="right", va="top", color=GREY)
    save(fig, "ch11_cubesats")


def raan_spread():
    J2 = 1.08263e-3
    days = np.linspace(0, 200, 400)
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    for dh, c in [(0, GREY), (-50, BLUE), (-100, ORANGE), (-150, RED), (-200, VIOLET)]:
        a = RE + 550 + dh
        a0 = RE + 550
        def rate(aa):
            n = np.sqrt(MU / aa ** 3)
            return -1.5 * n * J2 * (RE / aa) ** 2 * np.cos(np.radians(53))
        d = np.degrees((rate(a) - rate(a0)) * 86400 * days)
        ax.plot(days, d, color=c, label=f"parked {abs(dh)} km below the final shell" if dh else "final shell (550 km)")
    ax.set_xlabel("Days after launch")
    ax.set_ylabel("RAAN separation from the final shell (deg)")
    ax.legend(fontsize=7)
    note(ax, "J₂ nodal drift at 53° inclination. Satellites from one launch wait at different altitudes and drift apart "
             "in RAAN for free before climbing to the operational shell — 'differential precession' plane phasing.",
         xy=(1, -0.18))
    save(fig, "ch11_raan_spread")


if __name__ == "__main__":
    raan_spread()
    geometry(); footprint_vs_alt(); alt_histogram(); constellation_views(); sats_for_coverage(); mega(); shells()
    mass_classes(); cubesat_sizes()
