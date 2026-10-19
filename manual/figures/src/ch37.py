"""Figures for Chapter 37 — Spaceports and Ground Infrastructure."""
import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge, Arc  # noqa: F401

RAW = ROOT / "data" / "raw"
OMEGA_R = 465.1  # equatorial rotation speed, m/s


# ---------------------------------------------------------------- GCAT helpers
def load(name):
    with open(RAW / name, encoding="utf-8", errors="replace") as f:
        hdr = f.readline().lstrip("#").rstrip("\n").split("\t")
        rows = []
        for r in csv.reader(f, delimiter="\t"):
            if not r or r[0].startswith("#"):
                continue
            rows.append({h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(hdr)})
    return rows


# GCAT site codes grouped into spaceports
GROUP = {"CC": "Cape Canaveral / KSC", "KSC": "Cape Canaveral / KSC", "SPFLA": "Cape Canaveral / KSC",
         "SPFL": "Cape Canaveral / KSC", "V": "Vandenberg", "VS": "Vandenberg", "VSFBS": "Vandenberg",
         "VSFB": "Vandenberg", "PA": "Vandenberg", "MARS": "Wallops", "WI": "Wallops", "WIMB": "Wallops",
         "NIIP-5": "Baikonur", "GIK-5": "Baikonur", "NIIP-53": "Plesetsk", "GIK-1": "Plesetsk",
         "GNIIPV": "Plesetsk", "GNIIP": "Plesetsk", "VOST": "Vostochny", "CSG": "Kourou", "JQ": "Jiuquan",
         "TYSC": "Taiyuan", "XSC": "Xichang", "WEN": "Wenchang", "HCSLS": "Wenchang", "SHAR": "Sriharikota",
         "SDSC": "Sriharikota", "TNSC": "Tanegashima", "KASC": "Uchinoura", "USC": "Uchinoura", "MAHIA": "Mahia",
         "STB": "Starbase", "NARO": "Naro", "PALB": "Palmachim", "SEM": "Semnan", "SHAHR": "Shahroud",
         "SOHAE": "Sohae", "HHAI": "China (sea)", "YJ": "China (sea)", "ECS": "China (sea)", "KMR": "Kwajalein",
         "PSCA": "Kodiak", "KLC": "Kodiak", "AND": "Andøya", "ALCA": "Alcântara", "KII": "Kii", "BOWEN": "Bowen",
         "KLA": "Sea Launch", "GTsP-4": "Kapustin Yar", "GTsMP-4": "Kapustin Yar", "YAS": "Yasny",
         "GIK-2": "Svobodny", "MHV": "Mojave (air)", "NEWQ": "Cornwall (air)"}
# representative coordinates (lon, lat)
COORD = {"Cape Canaveral / KSC": (-80.58, 28.52), "Vandenberg": (-120.61, 34.68), "Wallops": (-75.48, 37.84),
         "Baikonur": (63.3, 45.96), "Plesetsk": (40.5, 62.9), "Vostochny": (128.33, 51.82),
         "Kourou": (-52.75, 5.24), "Jiuquan": (100.3, 40.96), "Taiyuan": (111.6, 38.85),
         "Xichang": (102.03, 28.25), "Wenchang": (110.95, 19.61), "Sriharikota": (80.23, 13.72),
         "Tanegashima": (130.97, 30.40), "Uchinoura": (131.08, 31.25), "Mahia": (177.87, -39.26),
         "Starbase": (-97.15, 26.0), "Naro": (127.54, 34.43), "Palmachim": (34.7, 31.9), "Semnan": (53.92, 35.23),
         "Shahroud": (55.33, 36.23), "Sohae": (124.71, 39.66), "China (sea)": (121.2, 34.9),
         "Kwajalein": (167.72, 8.99), "Kodiak": (-152.34, 57.44), "Andøya": (16.02, 69.29),
         "Alcântara": (-44.37, -2.32), "Kii": (135.89, 33.54), "Bowen": (148.11, -19.96)}


def orbital_launches(y0=1957, y1=2026):
    out = []
    for L in load("launch.tsv"):
        c = L["LaunchCode"]
        if not c or c[0] not in "OD":
            continue
        y = L["Launch_Date"][:4]
        if not y.isdigit() or not (y0 <= int(y) <= y1):
            continue
        out.append((int(y), GROUP.get(L["Launch_Site"], "Other"), L))
    return out


# ---------------------------------------------------------------- 1. azimuth and rotation gain
def azimuth():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.1))
    sites = [("Kourou 5.2°", 5.24, ORANGE), ("Cape 28.5°", 28.5, BLUE),
             ("Baikonur 46.0°", 45.96, RED), ("Plesetsk 62.9°", 62.9, VIOLET)]
    for name, phi, col in sites:
        i = np.linspace(phi + 1e-6, 180 - phi - 1e-6, 600)
        s = np.cos(np.radians(i)) / np.cos(np.radians(phi))
        az = np.degrees(np.arcsin(np.clip(s, -1, 1)))
        a1.plot(i, az, color=col, lw=1.5, label=name)
        a1.plot([phi], [90], "o", color=col, ms=4, zorder=5)
    a1.legend(fontsize=6.0, loc="lower left", frameon=False, title="launch site latitude φ", title_fontsize=6.0)
    a1.axhline(90, color=GREY, lw=0.6, ls=":")
    a1.axhline(0, color=GREY, lw=0.6, ls=":")
    a1.axvline(90, color=GREY, lw=0.6, ls=":")
    a1.text(178, 38, "south-going launch into\nthe same orbit: 180° − Az", fontsize=6.0, color=GREY, ha="right")
    a1.text(92, 60, "polar orbit:\ndue north", fontsize=6.0, color=GREY, ha="left")
    a1.set_xlim(0, 180)
    a1.set_ylim(-95, 108)
    a1.set_yticks([-90, -45, 0, 45, 90])
    a1.set_xticks([0, 30, 60, 90, 120, 150, 180])
    a1.set_xlabel("Orbit inclination i (°)")
    a1.set_ylabel("Launch azimuth Az (° east of north)")
    a1.set_title("(a) Azimuth for each inclination", fontsize=8.6)

    i = np.linspace(0, 180, 361)
    a2.plot(i, OMEGA_R * np.cos(np.radians(i)), color=NAVY, lw=1.6)
    a2.axhline(0, color=GREY, lw=0.6)
    pts = [("Kourou", 5.24), ("Sriharikota", 13.72), ("Cape Canaveral", 28.5), ("Vandenberg", 34.68),
           ("Mahia", 39.26), ("Baikonur", 45.96), ("Plesetsk", 62.9)]
    ylab = [520, 460, 400, 340, 280, 220, 160]
    for (n, phi), yl in zip(pts, ylab):
        g = OMEGA_R * np.cos(np.radians(phi))
        a2.plot(phi, g, "o", color=ORANGE, mec=NAVY, mew=0.5, ms=4.5, zorder=5)
        a2.annotate(f"{n} {phi:.0f}°: {g:.0f} m/s", (phi, g), xytext=(82, yl), fontsize=6.0, va="center",
                    arrowprops=dict(arrowstyle="-", color="#B8C2CC", lw=0.5))
    for name, inc, col, xt, yt in [("ISS 51.6°", 51.64, GREEN, 8, 120), ("SSO 97.5°", 97.5, RED, 116, -110)]:
        g = OMEGA_R * np.cos(np.radians(inc))
        a2.plot(inc, g, "s", color=col, ms=4.5, zorder=5)
        a2.annotate(f"{name}: {g:+.0f} m/s", (inc, g), xytext=(xt, yt), fontsize=6.2, color=col,
                    arrowprops=dict(arrowstyle="-", color=col, lw=0.6))
    a2.set_xlim(0, 180)
    a2.set_ylim(-500, 540)
    a2.set_xticks([0, 30, 60, 90, 120, 150, 180])
    a2.set_xlabel("Orbit inclination i (°)")
    a2.set_ylabel("Velocity gained from rotation (m/s)")
    a2.set_title("(b) Rotation gain = 465 m/s × cos i", fontsize=8.6)
    fig.text(0.99, 0.01, "sin Az = cos i / cos φ; surface speed 465.1 m/s × cos φ. Dots in (b): the most each site can "
             "gain, launching due east into i = φ. Range-safety limits on azimuth ignored.", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch37_azimuth")


# ---------------------------------------------------------------- 2. inclinations actually flown
def incflown():
    sat = collections.defaultdict(list)
    for s in load("satcat.tsv"):
        sat[s["Launch_Tag"].strip()].append(s)
    data = collections.defaultdict(list)
    for y, g, L in orbital_launches(2010, 2026):
        if L["LaunchCode"][:2] not in ("OS", "DS"):
            continue
        objs = sat.get(L["Launch_Tag"].strip(), [])
        rb = sorted([o for o in objs if o["Type"].startswith("R")], key=lambda o: o["Type"])
        pick = rb[-1] if rb else next((o for o in objs if o["Type"].startswith("P")), None)
        if not pick:
            continue
        try:
            data[g].append(float(pick["Inc"]))
        except ValueError:
            pass
    order = ["Kourou", "Sriharikota", "Wenchang", "Xichang", "Cape Canaveral / KSC", "Tanegashima",
             "Palmachim", "Vandenberg", "Wallops", "Taiyuan", "Mahia", "Jiuquan", "Baikonur", "Vostochny",
             "Plesetsk"]
    short = {"Cape Canaveral / KSC": "Cape / KSC"}
    fig, ax = plt.subplots(figsize=(7.0, 3.1))
    rng = np.random.default_rng(3)
    for k, g in enumerate(order):
        phi = abs(COORD[g][1])
        ax.add_patch(Rectangle((k - 0.38, phi), 0.76, 180 - 2 * phi, fc="#E8EEF4", ec="none", zorder=0))
        ax.plot([k - 0.38, k + 0.38], [phi, phi], color=NAVY, lw=0.9, zorder=1)
        v = np.array(data.get(g, []))
        if len(v) == 0:
            continue
        jit = rng.uniform(-0.3, 0.3, len(v))
        ok = v >= phi - 1.0
        ax.scatter(k + jit[ok], v[ok], s=5, color=BLUE, alpha=0.45, lw=0, zorder=3)
        ax.scatter(k + jit[~ok], v[~ok], s=7, facecolors="none", edgecolors=ORANGE, lw=0.6, zorder=3)
        ax.text(k, 154, f"{len(v)}", fontsize=5.9, ha="center", color=GREY)
    ax.text(-0.55, 162, "number of launches:", fontsize=5.9, ha="left", color=GREY)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([f"{short.get(g, g)} {abs(COORD[g][1]):.0f}°{' S' if COORD[g][1] < 0 else ''}" for g in order], fontsize=6.2, rotation=32,
                       ha="right", rotation_mode="anchor")
    ax.set_xlim(-0.6, len(order) - 0.4)
    ax.set_ylim(-3, 168)
    ax.set_yticks([0, 30, 60, 90, 120, 150])
    ax.set_ylabel("Orbit inclination (°)")
    ax.grid(axis="x", visible=False)
    ax.scatter([], [], s=12, color=BLUE, label="direct ascent")
    ax.scatter([], [], s=12, facecolors="none", edgecolors=ORANGE, label="below site latitude (dog-leg or plane change)")
    ax.add_patch(Rectangle((0, 0), 0, 0, fc="#E8EEF4", label="reachable by direct launch (φ ≤ i ≤ 180° − φ)"))
    ax.legend(fontsize=6.0, loc="upper center", bbox_to_anchor=(0.5, 1.13), ncol=3, frameon=False)
    fig.text(0.99, 0.01, "Successful orbital launches 2010 – 13 Oct 2026 (GCAT, J. McDowell). Inclination of the final "
             "rocket stage (or first payload). Sites ordered by latitude.", ha="right", va="bottom", fontsize=6.0,
             color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch37_incflown")


# ---------------------------------------------------------------- 3. world map of launches per site
def worldmap():
    import cartopy.crs as ccrs
    cnt = collections.Counter()
    c25 = collections.Counter()
    for y, g, L in orbital_launches(2016, 2025):
        cnt[g] += 1
        if y == 2025:
            c25[g] += 1
    fig = plt.figure(figsize=(7.0, 2.85))
    proj = ccrs.PlateCarree(central_longitude=5)
    ax = world_axes(fig, borders=True, proj=proj)
    ax.set_extent([-180, 180, -48, 74], crs=proj)
    lab = {"Cape Canaveral / KSC": (12, -12, "left"), "Vandenberg": (-9, -2, "right"),
           "Wallops": (3, 4, "left"), "Starbase": (-6, -6, "right"), "Kourou": (6, -3, "left"),
           "Baikonur": (5, 8, "left"), "Plesetsk": (5, 4, "left"), "Vostochny": (4, 4, "left"),
           "Jiuquan": (-9, 6, "right"), "Taiyuan": (3, 9, "left"), "Xichang": (-9, -6, "right"),
           "Wenchang": (0, -10, "center"), "China (sea)": (7, 1, "left"), "Sriharikota": (-3, -9, "center"),
           "Tanegashima": (5, -6, "left"), "Mahia": (-6, 0, "right"), "Palmachim": (-4, -5, "right"),
           "Semnan": (-3, -7, "right"), "Kodiak": (3, -6, "left"), "Alcântara": (3, -5, "left"),
           "Andøya": (-4, -3, "right"), "Bowen": (3, -4, "left")}
    for g, n in sorted(cnt.items(), key=lambda x: -x[1]):
        if g not in COORD:
            continue
        lon, lat = COORD[g]
        size = 8 + 2.2 * n
        col = RED if c25.get(g, 0) >= 10 else (ORANGE if c25.get(g, 0) > 0 else GREY)
        ax.scatter(lon, lat, s=size, color=col, alpha=0.55, edgecolor=NAVY, lw=0.5,
                   transform=ccrs.PlateCarree(), zorder=4)
        if g in lab:
            dx, dy, ha = lab[g]
            nm = "Cape / KSC" if g.startswith("Cape") else g
            ax.text(lon + dx, lat + dy, f"{nm} {n}", fontsize=5.9, ha=ha, va="center",
                    transform=ccrs.PlateCarree(), zorder=6)
    for n, s in [(10, 10), (50, 50), (200, 200)]:
        ax.scatter([], [], s=8 + 2.2 * s, color=GREY, alpha=0.4, edgecolor=NAVY, lw=0.5, label=f"{n} launches")
    ax.scatter([], [], s=30, color=RED, alpha=0.55, label="≥ 10 in 2025")
    ax.scatter([], [], s=30, color=ORANGE, alpha=0.55, label="1–9 in 2025")
    ax.scatter([], [], s=30, color=GREY, alpha=0.55, label="none in 2025")
    ax.legend(loc="lower left", fontsize=5.9, ncol=2, frameon=True, framealpha=0.9, labelspacing=1.3,
              borderpad=0.9, columnspacing=1.2)
    fig.text(0.99, 0.01, "Orbital launch attempts 2016–2025 by spaceport (GCAT, J. McDowell; Wenchang includes the "
             "Hainan commercial site; Chinese sea launches plotted at Haiyang).", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.075)
    save(fig, "ch37_worldmap", raster=True)


# ---------------------------------------------------------------- 4. launches per year by spaceport
def trend():
    cats = [("Florida", ["Cape Canaveral / KSC"], BLUE), ("Vandenberg", ["Vandenberg"], SKY),
            ("Starbase, Wallops, Kodiak", ["Starbase", "Wallops", "Kodiak", "Kwajalein"], NAVY),
            ("Mahia (Rocket Lab)", ["Mahia"], GREEN),
            ("China", ["Jiuquan", "Taiyuan", "Xichang", "Wenchang", "China (sea)"], RED),
            ("Russia & Kazakhstan", ["Baikonur", "Plesetsk", "Vostochny", "Yasny", "Svobodny", "Kapustin Yar"],
             VIOLET),
            ("Kourou", ["Kourou"], GOLD), ("India & Japan", ["Sriharikota", "Tanegashima", "Uchinoura", "Kii"],
                                           ORANGE)]
    years = np.arange(2000, 2027)
    tab = {c[0]: np.zeros(len(years)) for c in cats}
    other = np.zeros(len(years))
    idx = {g: c[0] for c in cats for g in c[1]}
    for y, g, L in orbital_launches(2000, 2026):
        k = y - 2000
        if g in idx:
            tab[idx[g]][k] += 1
        else:
            other[k] += 1
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    bottom = np.zeros(len(years))
    for name, _, col in cats:
        ax.bar(years, tab[name], bottom=bottom, color=col, width=0.8, label=name, lw=0)
        bottom += tab[name]
    ax.bar(years, other, bottom=bottom, color=GREY, width=0.8, label="Other", lw=0)
    bottom += other
    for y, v in zip(years, bottom):
        if y in (2000, 2010, 2016, 2020, 2023, 2024, 2025):
            ax.text(y, v + 4, f"{v:.0f}", ha="center", fontsize=6.0)
    ax.text(2026.2, bottom[-1] + 4, f"{bottom[-1]:.0f}\n(to 13 Oct)", ha="center", fontsize=5.9, linespacing=1.1)
    ax.set_xlim(1999.3, 2026.7)
    ax.set_ylim(0, 365)
    ax.set_ylabel("Orbital launch attempts")
    ax.legend(fontsize=6.2, loc="upper left", ncol=2, frameon=False)
    ax.grid(axis="x", visible=False)
    fig.text(0.99, 0.01, "GCAT (J. McDowell), orbital and deep-space launch attempts including failures and Starship "
             "test flights; 2026 to 13 October.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch37_trend")


# ---------------------------------------------------------------- 5. launch corridors (Americas)
def gc_path(lon0, lat0, az, dist_km, n=200):
    R = 6371.0
    d = np.linspace(0, dist_km, n) / R
    la1, lo1, a = np.radians(lat0), np.radians(lon0), np.radians(az)
    la2 = np.arcsin(np.sin(la1) * np.cos(d) + np.cos(la1) * np.sin(d) * np.cos(a))
    lo2 = lo1 + np.arctan2(np.sin(a) * np.sin(d) * np.cos(la1), np.cos(d) - np.sin(la1) * np.sin(la2))
    return np.degrees(lo2), np.degrees(la2)


def azimuth_for(inc, phi, south=False):
    s = np.cos(np.radians(inc)) / np.cos(np.radians(phi))
    az = np.degrees(np.arcsin(np.clip(s, -1, 1)))
    return (180 - az) if south else az % 360


def corridors():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.0, 3.75))
    ax = world_axes(fig, borders=True, extent=[-130, -20, -6, 52], res="50m")
    sites = {"Cape": (-80.58, 28.52), "Vandenberg": (-120.61, 34.68), "Kourou": (-52.75, 5.24),
             "Starbase": (-97.15, 26.0)}
    tracks = [  # site, inclination, south-going?, label, colour, label lon/lat, ha
        ("Cape", 28.5, False, "GTO 28.5° (90°)", BLUE, -66.0, 29.2, "left"),
        ("Cape", 51.64, False, "ISS 51.6° (45°)", GREEN, -63.0, 46.5, "left"),
        ("Cape", 43.0, False, "Starlink 43° (56°)", SKY, -58.5, 39.0, "left"),
        ("Vandenberg", 97.5, True, "SSO 97.5° (189°)", RED, -121.0, 11.5, "right"),
        ("Vandenberg", 70.0, True, "70° (155°)", VIOLET, -111.5, 14.5, "left"),
        ("Kourou", 6.0, False, "GTO 6° (87°)", BLUE, -32.0, 7.6, "left"),
        ("Kourou", 97.5, False, "SSO 97.5° (352°)", RED, -54.2, 23.5, "left"),
        ("Kourou", 51.64, False, "51.6° (39°)", GREEN, -40.0, 17.5, "left"),
        ("Starbase", 26.5, True, "Starship 26.5° (95°)", NAVY, -97.0, 19.8, "left")]
    for site, inc, south, name, col, tx, ty, ha in tracks:
        lon0, lat0 = sites[site]
        az = azimuth_for(inc, lat0, south)
        lo, la = gc_path(lon0, lat0, az, 2200)
        ax.plot(lo, la, color=col, lw=1.4, transform=ccrs.Geodetic(), zorder=4)
        lo6, la6 = gc_path(lon0, lat0, az, 600, n=2)
        ax.plot(lo6[-1], la6[-1], "o", ms=3.2, color="white", mec=col, mew=1.0, transform=ccrs.PlateCarree(),
                zorder=5)
        ax.text(tx, ty, name, fontsize=6.0, color=col, transform=ccrs.PlateCarree(), zorder=6, ha=ha,
                bbox=dict(fc="white", ec="none", alpha=0.6, pad=0.3))
    for n, (lon, lat) in sites.items():
        ax.plot(lon, lat, "^", ms=6, color=GOLD, mec=NAVY, mew=0.6, transform=ccrs.PlateCarree(), zorder=7)
        dx, dy, ha = {"Cape": (-1.5, -2.5, "right"), "Vandenberg": (-1.5, -1.8, "right"),
                      "Kourou": (-1.5, -2.2, "right"), "Starbase": (-1.2, 1.2, "right")}[n]
        ax.text(lon + dx, lat + dy, n, fontsize=6.6, weight="bold", ha=ha, transform=ccrs.PlateCarree(), zorder=7)
    ax.text(-128.5, -4.6, "Open circles: 600 km downrange, roughly where a Falcon 9 booster lands on a droneship.\n"
            "Azimuth (in brackets) from sin Az = cos i / cos φ; great-circle paths 2 200 km long.",
            fontsize=5.9, color=INK, transform=ccrs.PlateCarree(), zorder=8,
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.5))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, "ch37_corridors", raster=True)


# ---------------------------------------------------------------- 6. launch pad schematic
def pad():
    fig, ax = canvas(7.0, 4.3, (0, 140), (0, 86))
    ground = 24
    # terrain and pad deck
    ax.add_patch(Rectangle((0, 0), 140, ground, fc="#E9E4D8", ec="none", zorder=0))
    ax.add_patch(Polygon([(18, ground), (30, ground + 7), (66, ground + 7), (78, ground)], fc="#D2CCBE",
                         ec="#8C8576", lw=0.8, zorder=1))
    # flame trench and deflector
    ax.add_patch(Rectangle((33, 5), 36, ground + 7 - 5, fc="#B8B1A3", ec="#6F695D", lw=0.8, zorder=2))
    ax.add_patch(Rectangle((44.5, ground + 4), 11, 3.2, fc="white", ec="none", zorder=3))  # flame hole
    ax.add_patch(Polygon([(43, 5), (50, 19), (57, 5)], fc="#5B6670", ec=NAVY, lw=0.8, zorder=4))
    for sgn in (-1, 1):
        xs = 50 + sgn * np.array([1.5, 6, 12, 17])
        ys = np.array([17, 11, 8, 7])
        ax.plot(xs, ys, color=ORANGE, lw=2.2, alpha=0.8, zorder=5)
        ax.annotate("", xy=(50 + sgn * 19, 7), xytext=(50 + sgn * 16, 7.3),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4), zorder=5)
    # deluge sprays
    for x in (36, 64):
        for k in range(5):
            ax.plot([x, x + (k - 2) * 1.2], [ground + 2, ground - 4], color=SKY, lw=0.8, zorder=5)
    for x in (41, 59):
        ax.plot([x, x], [ground + 7, ground + 9.5], color=SKY, lw=2.0, zorder=6)
    # launch mount and rocket
    ax.add_patch(Rectangle((40, ground + 7), 20, 3.0, fc="#7A8590", ec=NAVY, lw=0.8, zorder=6))
    ax.add_patch(Rectangle((46, ground + 10), 8, 36, fc="white", ec="#333", lw=0.8, zorder=7))
    ax.add_patch(Polygon([(46, ground + 46), (54, ground + 46), (50, ground + 54)], fc="white", ec="#333", lw=0.8,
                         zorder=7))
    ax.plot([46, 54], [ground + 33, ground + 33], color="#333", lw=0.6, zorder=8)
    for x in (45, 55):
        ax.add_patch(Rectangle((x - 1, ground + 10), 2, 3, fc=RED, ec="none", zorder=8))
    # umbilical tower
    tx = 66
    ax.add_patch(Rectangle((tx, ground + 7), 7, 48, fc="none", ec=NAVY, lw=1.0, zorder=6))
    for yy in np.arange(ground + 7, ground + 55, 4.8):
        ax.plot([tx, tx + 7], [yy, yy + 4.8], color=NAVY, lw=0.4, zorder=6)
        ax.plot([tx + 7, tx], [yy, yy + 4.8], color=NAVY, lw=0.4, zorder=6)
    ax.plot([54, tx], [ground + 42, ground + 42], color=NAVY, lw=2.0, zorder=7)       # crew access arm
    ax.plot([54, tx], [ground + 29, ground + 29], color=GREEN, lw=1.6, zorder=7)      # stage-2 umbilical
    ax.plot([54, tx], [ground + 16, ground + 16], color=GREEN, lw=1.6, zorder=7)      # stage-1 umbilical
    # lightning masts and catenary
    for x in (8, 112):
        ax.plot([x, x], [ground, ground + 60], color="#5B6670", lw=1.6, zorder=3)
    ax.plot([8, 50, 112], [ground + 60, ground + 57, ground + 60], color="#5B6670", lw=0.6, ls="--", zorder=3)
    # water tower
    ax.plot([90, 90], [ground, ground + 14], color="#5B6670", lw=1.2)
    ax.plot([96, 96], [ground, ground + 14], color="#5B6670", lw=1.2)
    ax.add_patch(Rectangle((88, ground + 14), 10, 7, fc="#CFE4F5", ec=NAVY, lw=0.8, zorder=3))
    ax.plot([93, 93, 64], [ground + 1, ground - 3, ground - 3], color=SKY, lw=1.6, zorder=2)
    # propellant farm
    ax.add_patch(Circle((106, ground + 6), 6, fc="#DDEBF7", ec=BLUE, lw=1.0, zorder=3))
    ax.add_patch(Circle((124, ground + 6), 6, fc="#F7E6D9", ec=ORANGE, lw=1.0, zorder=3))
    ax.add_patch(Rectangle((114, ground), 4, 3, fc="#CCCCCC", ec="#555", lw=0.6, zorder=3))
    ax.plot([106, 106, 74], [ground, ground - 6, ground - 6], color=BLUE, lw=1.6, zorder=2)
    ax.plot([124, 124, 74], [ground, ground - 8, ground - 8], color=ORANGE, lw=1.6, zorder=2)
    ax.plot([74, 74], [ground - 8, ground + 7], color=NAVY, lw=1.0, zorder=2)
    for k in range(4):
        ax.add_patch(Rectangle((128 + k * 2.4, ground), 1.8, 9, fc="#E6E6E6", ec="#555", lw=0.5, zorder=3))

    def lab(x, y, t, xt, yt, ha="left"):
        ax.annotate(t, (x, y), xytext=(xt, yt), fontsize=6.3, ha=ha, va="center", color=INK, zorder=10,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    lab(48, ground + 48, "Launch vehicle", 27, ground + 50, "right")
    lab(45, ground + 12, "Hold-down clamps\nrelease at lift-off", 27, ground + 22, "right")
    lab(42, ground + 8.5, "Launch mount with\nflame hole", 27, ground + 11, "right")
    lab(36, ground - 1, "Deluge / sound-\nsuppression water", 27, ground - 2, "right")
    lab(47, 13, "Flame deflector", 27, 13, "right")
    lab(37, 7, "Flame trench", 27, 6, "right")
    lab(tx + 7, ground + 52, "Umbilical / service tower", tx + 10, ground + 53)
    lab(60, ground + 42, "Crew access arm", tx + 10, ground + 46)
    lab(60, ground + 29, "Propellant, gas, power and\ndata umbilicals", tx + 10, ground + 36)
    lab(112, ground + 56, "Lightning mast and\ncatenary wire", 114, ground + 52)
    lab(93, ground + 21, "Deluge water tower", 99, ground + 28)
    lab(106, ground + 12, "LOX sphere", 101, ground + 17.5)
    lab(124, ground + 12, "Fuel (LH₂, CH₄ or RP-1)", 116, ground + 22.5)
    lab(131, ground + 9, "He / N₂ bottles", 133, ground + 14, "center")
    lab(95, ground - 7, "Vacuum-jacketed cryogenic lines", 96, 12)
    ax.text(100, 3, "Schematic, not to scale; loosely based on a modern\nliquid-propellant pad such as LC-39A/B or SLC-40.",
            fontsize=6.0, color=GREY, ha="center")
    save(fig, "ch37_pad")


# ---------------------------------------------------------------- 7. integration approaches
def integration():
    fig, ax = canvas(7.0, 3.1, (0, 150), (-1, 67))
    gy = 14

    def ground(x0, x1):
        ax.plot([x0, x1], [gy, gy], color="#8C8576", lw=1.0)

    def rocket_v(x, y, h=26, w=3.2, col="white"):
        ax.add_patch(Rectangle((x - w / 2, y), w, h * 0.85, fc=col, ec="#333", lw=0.7, zorder=5))
        ax.add_patch(Polygon([(x - w / 2, y + h * 0.85), (x + w / 2, y + h * 0.85), (x, y + h)], fc=col, ec="#333",
                             lw=0.7, zorder=5))

    def rocket_h(x, y, L=24, w=3.0):
        ax.add_patch(Rectangle((x, y), L * 0.85, w, fc="white", ec="#333", lw=0.7, zorder=5))
        ax.add_patch(Polygon([(x + L * 0.85, y), (x + L * 0.85, y + w), (x + L, y + w / 2)], fc="white", ec="#333",
                             lw=0.7, zorder=5))
    # (a) vertical in VAB, then crawler
    ground(2, 48)
    ax.add_patch(Rectangle((4, gy), 16, 38, fc="#E3E8EE", ec=NAVY, lw=1.0, zorder=2))
    ax.add_patch(Rectangle((6, gy), 7.5, 4, fc="#7A8590", ec=NAVY, lw=0.6, zorder=4))
    rocket_v(9.7, gy + 4, h=28)
    ax.add_patch(Rectangle((30, gy + 2.5), 10, 3, fc="#7A8590", ec=NAVY, lw=0.6, zorder=4))
    ax.add_patch(Rectangle((31, gy), 8, 2.5, fc="#444", ec="none", zorder=4))
    rocket_v(35, gy + 5.5, h=28)
    ax.annotate("", xy=(28, gy + 9), xytext=(21, gy + 9), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4))
    ax.text(12, gy + 40, "assembly building", fontsize=6.0, ha="center")
    ax.text(35, gy + 36, "crawler +\nmobile launcher", fontsize=5.9, ha="center", va="bottom")
    ax.text(25, 64, "(a) Vertical assembly,\nvertical transfer", fontsize=7.4, weight="bold", ha="center")
    ax.text(25, 6, "Saturn V, Shuttle, SLS (VAB);\nH3 (Tanegashima); Long March 2F,\n5 and 7 (rail platform); Vulcan (VIF)",
            fontsize=5.9, ha="center", va="center")
    # (b) horizontal hangar, transporter-erector
    ground(52, 98)
    ax.add_patch(Rectangle((53, gy), 22, 14, fc="#E3E8EE", ec=NAVY, lw=1.0, zorder=2))
    rocket_h(54, gy + 4, L=20)
    ax.add_patch(Rectangle((54, gy + 1.5), 18, 2, fc="#7A8590", ec=NAVY, lw=0.5, zorder=4))
    ax.text(64, gy + 16, "integration hangar", fontsize=6.0, ha="center")
    ax.annotate("", xy=(83, gy + 6), xytext=(76, gy + 6), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4))
    # erector at pad
    ax.plot([87, 87 + 26 * np.cos(np.radians(70))], [gy + 2, gy + 2 + 26 * np.sin(np.radians(70))], color="#7A8590",
            lw=2.2, zorder=4)
    ax.add_patch(Rectangle((84, gy), 12, 2, fc="#7A8590", ec=NAVY, lw=0.5, zorder=4))
    tr = matplotlib.transforms.Affine2D().rotate_deg_around(89.5, gy + 3, 70) + ax.transData
    p1 = Rectangle((89.5, gy + 3), 22, 3.0, fc="white", ec="#333", lw=0.7, zorder=5)
    p1.set_transform(tr)
    ax.add_patch(p1)
    ax.annotate("", xy=(97, gy + 24), xytext=(97, gy + 12), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.0,
                                                                            connectionstyle="arc3,rad=0.4"))
    ax.text(75, 64, "(b) Horizontal integration,\nerected at the pad", fontsize=7.4, weight="bold", ha="center")
    ax.text(75, 6, "Soyuz, Angara, Falcon 9 and\nFalcon Heavy, Electron,\nAntares, Minotaur", fontsize=5.9,
            ha="center", va="center")
    # (c) vertical on the pad in a mobile gantry
    ground(102, 148)
    ax.add_patch(Rectangle((106, gy), 4, 40, fc="none", ec=NAVY, lw=1.0, zorder=3))
    rocket_v(117, gy + 3, h=32)
    ax.add_patch(Rectangle((110.5, gy), 13, 3, fc="#7A8590", ec=NAVY, lw=0.5, zorder=4))
    ax.add_patch(Rectangle((127, gy), 16, 42, fc="#E3E8EE", ec=NAVY, lw=1.0, alpha=0.9, zorder=2))
    ax.annotate("", xy=(146, gy + 22), xytext=(129, gy + 22), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4))
    ax.text(135, gy + 25, "gantry rolls\nback before\nlaunch", fontsize=5.9, ha="center", va="bottom")
    ax.text(125, 64, "(c) Vertical integration\non the pad", fontsize=7.4, weight="bold", ha="center")
    ax.text(125, 6, "Ariane 6 (ELA-4), Vega-C;\nStarship (stacked on the pad\nby the tower's arms)",
            fontsize=5.9, ha="center", va="center")
    save(fig, "ch37_integration")


# ---------------------------------------------------------------- 8. launch noise vs distance
def noise():
    vehicles = [  # name, thrust (N), exhaust speed (m/s), colour, measured Lw if known
        ("Electron", 9 * 24.9e3, 3050, GREEN, None),
        ("Falcon 9", 7.607e6, 2770, BLUE, 196.0),
        ("SLS Block 1 (Artemis I)", 39.1e6, None, ORANGE, 202.4),
        ("Saturn V (estimate)", 34.8e6, None, VIOLET, 204.7),
        ("Super Heavy (33 Raptor 2)", 33 * 2.26e6, 3200, RED, None),
    ]
    eta, Q = 0.003, 5.0
    r = np.logspace(np.log10(300), np.log10(50000), 300)
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    rows = []
    for name, F, ve, col, Lmeas in vehicles:
        if Lmeas is not None:
            Lw = Lmeas
        else:
            Lw = 10 * np.log10(eta * 0.5 * F * ve / 1e-12)
        Lp = Lw + Q - 10 * np.log10(2 * np.pi * r ** 2)
        ax.semilogx(r / 1000, Lp, color=col, lw=1.6, label=f"{name}: L$_W$ ≈ {Lw:.0f} dB")
        r120 = np.sqrt(10 ** ((Lw + Q - 120) / 10) / (2 * np.pi))
        rows.append((name, Lw, r120))
    ax.errorbar([1.43], [137], yerr=[2], fmt="o", color=ORANGE, mec=NAVY, ms=5, capsize=2, zorder=6)
    ax.annotate("SLS measured, 1.43 km\n(137 ± 2 dB)", (1.43, 137), xytext=(1.9, 143.5), fontsize=6.2,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.plot([9.7], [125], "D", color=RED, mec=NAVY, ms=5, zorder=6)
    ax.annotate("Starship Flight 5, ≈ 10 km\n(≈ 125 dB reported)", (9.7, 125), xytext=(14, 131), fontsize=6.2,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.axhline(140, color=GREY, lw=0.7, ls="--")
    ax.text(48, 141, "140 dB: limit for unprotected ears (impulse noise)", fontsize=6.0, color=GREY, ha="right")
    ax.axhline(120, color=GREY, lw=0.7, ls="--")
    ax.text(0.31, 117.2, "120 dB", fontsize=6.0, color=GREY)
    ax.set_xlim(0.3, 50)
    ax.set_ylim(95, 170)
    ax.set_xticks([0.3, 1, 3, 10, 30, 50])
    ax.set_xticklabels(["0.3", "1", "3", "10", "30", "50"])
    ax.set_xlabel("Distance from pad (km)")
    ax.set_ylabel("Max. overall sound level (dB re 20 µPa)")
    ax.legend(fontsize=6.0, loc="upper right", frameon=False)
    fig.text(0.99, 0.01, "L$_p$ = L$_W$ + 5 dB (directivity) − 10 log₁₀(2πr²): hemispherical spreading over hard ground, "
             "no atmospheric absorption. L$_W$ = 10 log₁₀(η·½·F·v$_e$ / 1 pW) with η = 0.3 %, or measured/estimated "
             "values (Kellison & Gee 2023, 2024). Super Heavy: 33 × 2.26 MN, v$_e$ ≈ 3.2 km/s.", ha="right", va="bottom", fontsize=5.9, color=GREY, wrap=True)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "ch37_noise")
    for n, lw, rr in rows:
        print(f"  {n:28s} Lw={lw:6.1f} dB  r(120 dB)={rr/1000:5.1f} km  Lp(10 km)={lw + Q - 10*np.log10(2*np.pi*1e8):5.1f}")


# ---------------------------------------------------------------- 9. weather climatology and scrub odds
THUNDER_DAYS = [1, 2, 3, 3, 8, 13, 16, 14, 10, 4, 1, 1]   # NASA TM-103498, CCAFS/SLF 1950-52, 1957-80
MDAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]


def weather():
    p_th = np.array(THUNDER_DAYS) / np.array(MDAYS)
    p_tech = 0.10
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.9), gridspec_kw=dict(width_ratios=[1, 1.1]))
    a1.bar(range(12), THUNDER_DAYS, color=[RED if v >= 10 else SKY for v in THUNDER_DAYS], width=0.7)
    for k, v in enumerate(THUNDER_DAYS):
        a1.text(k, v + 0.3, f"{v}", ha="center", fontsize=6.0)
    a1.set_xticks(range(12))
    a1.set_xticklabels(MONTHS)
    a1.set_ylabel("Days with thunderstorms")
    a1.set_ylim(0, 18.5)
    a1.set_yticks([0, 4, 8, 12, 16])
    a1.set_title("(a) Cape Canaveral thunderstorm days", fontsize=8.4)
    a1.grid(axis="x", visible=False)
    n = np.arange(1, 8)
    for m, col in [(0, BLUE), (3, GREEN), (5, ORANGE), (6, RED), (8, VIOLET)]:
        p = (1 - p_th[m]) * (1 - p_tech)
        a2.plot(n, 1 - (1 - p) ** n, "o-", color=col, ms=3.5, lw=1.4,
                label=f"{['January','','','April','','June','July','','September'][m]}: P(go) = {p:.2f}")
    a2.set_xlabel("Number of launch attempts (days)")
    a2.set_ylabel("Probability launched by then")
    a2.set_ylim(0.3, 1.02)
    a2.set_xticks(n)
    a2.set_title("(b) Odds of an afternoon launch", fontsize=8.4)
    a2.legend(fontsize=6.0, loc="lower right", frameon=False)
    fig.text(0.99, 0.01, "(a) NASA TM-103498 (1950–52, 1957–80). (b) Assumes an afternoon window is lost on any "
             "thunderstorm day, a 10 % chance of a non-weather scrub, and independent days.", ha="right",
             va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch37_weather")


if __name__ == "__main__":
    fns = [azimuth, incflown, worldmap, trend, corridors, pad, integration, noise, weather]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
