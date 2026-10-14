import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse

ROOT = Path(__file__).resolve().parents[2]
GN = json.load(open(ROOT / "data/gnss_sats.json"))
SYSCOL = {"GPS": BLUE, "Galileo": NAVY, "GLONASS": RED, "BeiDou": ORANGE, "QZSS": GREEN, "NavIC": VIOLET}


def orbits():
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for k, c in SYSCOL.items():
        p = np.array(GN["systems"][k]["pts"])
        ax.scatter(p[:, 1], p[:, 0] / 1000, color=c, s=18, alpha=0.8, label=f"{k} ({GN['systems'][k]['count']})",
                   edgecolor="white", lw=0.4)
    ax.axhline(35.786, color=GREY, lw=0.7, ls=":")
    ax.text(70, 36.3, "geosynchronous altitude", fontsize=6.4, color=GREY, ha="right")
    ax.set_xlabel("Inclination (°)")
    ax.set_ylabel("Mean altitude (thousand km)")
    ax.set_xlim(-3, 72)
    ax.set_ylim(15, 40)
    ax.legend(fontsize=6.6, loc="center left", title="Active satellites, Oct 2026", title_fontsize=6.6)
    for t, x, y, ha in [("GLONASS: 19 100 km, 64.8°", 64.5, 16.6, "center"), ("GPS: 20 200 km, 55°", 51, 19.7, "right"),
                        ("BeiDou: 21 500 km, 55°", 51, 21.4, "right"), ("Galileo: 23 200 km, 56°", 51, 23.2, "right"),
                        ("GEO and inclined GEO\n(BeiDou, QZSS, NavIC)", 25, 33.3, "left")]:
        ax.text(x, y, t, fontsize=6.2, ha=ha, va="center", color=GREY)
    note(ax, "Each point is an active satellite (CelesTrak SATCAT, name-matched, includes spares and test satellites).",
         xy=(1, -0.15))
    save(fig, "ch18_orbits")


def trilateration():
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.1))
    sats = [(-3, 7), (6, 6), (1, -6)]
    user = (1.0, 1.0)
    for a, bias, title in [(axs[0], 0.0, "True ranges meet at one point"),
                           (axs[1], 1.3, "Receiver clock error: pseudoranges do not")]:
        for (x, y), c in zip(sats, [BLUE, ORANGE, GREEN]):
            r = np.hypot(user[0] - x, user[1] - y) + bias
            a.add_patch(Circle((x, y), r, fc="none", ec=c, lw=1.4))
            a.plot(x, y, "s", color=c, ms=6)
        a.plot(*user, "*", color=RED, ms=11, zorder=5)
        a.set_xlim(-9, 12)
        a.set_ylim(-9, 12)
        a.set_aspect("equal")
        a.axis("off")
        a.set_title(title, fontsize=7.6)
    axs[1].text(1.5, -8.6, "a fourth satellite allows the clock error\nto be solved as an extra unknown", fontsize=6.6,
                ha="center", color=GREY)
    save(fig, "ch18_trilat")


def ca_code(prn):
    taps = {1: (2, 6), 2: (3, 7), 3: (4, 8), 4: (5, 9), 5: (1, 9), 6: (2, 10), 7: (1, 8), 8: (2, 9)}
    g1 = [1] * 10
    g2 = [1] * 10
    out = []
    t1, t2 = taps[prn]
    for _ in range(1023):
        g2o = g2[t1 - 1] ^ g2[t2 - 1]
        out.append(g1[9] ^ g2o)
        f1 = g1[2] ^ g1[9]
        f2 = g2[1] ^ g2[2] ^ g2[5] ^ g2[7] ^ g2[8] ^ g2[9]
        g1 = [f1] + g1[:9]
        g2 = [f2] + g2[:9]
    return np.array(out)


def correlation():
    c1 = 1 - 2 * ca_code(1)
    c2 = 1 - 2 * ca_code(2)
    print("first 10 chips PRN1 (octal check 1440):", "".join(str(b) for b in ca_code(1)[:10]))
    lags = np.arange(-511, 512)
    ac = np.array([np.sum(c1 * np.roll(c1, k)) for k in lags])
    cc = np.array([np.sum(c1 * np.roll(c2, k)) for k in lags])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.8), gridspec_kw=dict(wspace=0.3))
    a1.plot(lags, ac, color=NAVY, lw=0.8)
    a1.set_title("Autocorrelation, GPS C/A code PRN 1", fontsize=7.6)
    a1.set_xlabel("Code offset (chips)")
    a1.set_ylabel("Correlation")
    a1.set_ylim(-100, 1100)
    a1.text(30, 1000, "peak = 1023", fontsize=6.6)
    a1.text(-500, 120, f"sidelobes: {sorted(int(v) for v in set(ac[lags != 0]))}", fontsize=6.4, color=GREY)
    a2.plot(lags, cc, color=ORANGE, lw=0.8)
    a2.set_title("Cross-correlation, PRN 1 × PRN 2", fontsize=7.6)
    a2.set_xlabel("Code offset (chips)")
    a2.set_ylim(-100, 1100)
    a2.text(-500, 120, f"values: {sorted(int(v) for v in set(cc))}", fontsize=6.4, color=GREY)
    note(a2, "Computed with the IS-GPS-200 G1/G2 Gold-code generators (1 023 chips, 1.023 Mchip/s).", xy=(1, -0.24))
    save(fig, "ch18_correlation")


def walker(a, inc, planes, per, phase=1, raan0=0):
    sats = []
    for p in range(planes):
        for s in range(per):
            raan = raan0 + 360 * p / planes
            u = 360 * s / per + 360 * phase * p / (planes * per)
            sats.append((a, inc, raan, u))
    return sats


def positions(sats, t):
    mu, we = 398600.4418, 7.2921159e-5
    out = []
    for a, inc, raan, u0 in sats:
        n = np.sqrt(mu / a ** 3)
        u = np.radians(u0) + n * t
        O = np.radians(raan) - we * t
        i = np.radians(inc)
        x = a * (np.cos(O) * np.cos(u) - np.sin(O) * np.sin(u) * np.cos(i))
        y = a * (np.sin(O) * np.cos(u) + np.cos(O) * np.sin(u) * np.cos(i))
        z = a * np.sin(u) * np.sin(i)
        out.append((x, y, z))
    return np.array(out)


def dop():
    lat, lon = np.radians(40), 0.0
    R = 6378.137
    obs = R * np.array([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)])
    up = obs / np.linalg.norm(obs)
    systems = {"GPS": walker(26560, 55, 6, 4, 1), "Galileo": walker(29600, 56, 3, 8, 1, 10),
               "GLONASS": walker(25510, 64.8, 3, 8, 1, 20), "BeiDou": walker(27906, 55, 3, 8, 1, 35)}
    T = np.arange(0, 86400, 300)
    res = {"GPS": ([], []), "All four": ([], [])}
    for t in T:
        rows = {}
        for k, s in systems.items():
            P = positions(s, t)
            los = P - obs
            rng = np.linalg.norm(los, axis=1)
            u = los / rng[:, None]
            el = np.degrees(np.arcsin(u @ up))
            rows[k] = u[el > 10]
        for name, keys in [("GPS", ["GPS"]), ("All four", list(systems))]:
            H = []
            for j, k in enumerate(keys):
                for uu in rows[k]:
                    clk = [0] * len(keys)
                    clk[j] = 1
                    H.append(list(-uu) + clk)
            H = np.array(H)
            Q = np.linalg.inv(H.T @ H)
            res[name][0].append(len(H))
            res[name][1].append(np.sqrt(np.trace(Q[:3, :3])))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 3.6), sharex=True, gridspec_kw=dict(hspace=0.12))
    for name, c in [("GPS", BLUE), ("All four", ORANGE)]:
        a1.plot(T / 3600, res[name][0], color=c, lw=1.4, label="GPS only (24)" if name == "GPS" else
                "GPS + Galileo + GLONASS + BeiDou MEO (96)")
        a2.plot(T / 3600, res[name][1], color=c, lw=1.4)
    a1.set_ylabel("Satellites above 10°", fontsize=7)
    a2.set_ylabel("PDOP", fontsize=7)
    a2.set_xlabel("Hours")
    a1.legend(fontsize=6.4, loc="center right")
    a2.set_ylim(0, 3.2)
    a2.set_xlim(0, 24)
    note(a2, "Simulated nominal constellations (Walker patterns) seen from 40° N, 0° E, 10° elevation mask.",
         xy=(1, -0.42))
    save(fig, "ch18_dop")


def dop_geom():
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.9), subplot_kw=dict(projection="polar"))
    for a, az, el, title, ell in [(axs[0], [20, 110, 200, 290, 0], [30, 25, 35, 20, 85], "Good geometry: PDOP ≈ 1.6",
                                   (0.6, 0.6)),
                                  (axs[1], [40, 55, 65, 50], [40, 50, 35, 60], "Poor geometry: PDOP ≈ 8", (2.4, 0.7))]:
        a.set_theta_zero_location("N")
        a.set_theta_direction(-1)
        a.set_rlim(90, 0)
        a.set_rticks([0, 30, 60, 90])
        a.set_yticklabels(["", "30°", "60°", ""], fontsize=5.5)
        a.set_xticks(np.radians([0, 90, 180, 270]))
        a.set_xticklabels(["N", "E", "S", "W"], fontsize=6.5)
        a.plot(np.radians(az), el, "o", color=ORANGE, ms=7, mec="white")
        a.set_title(title, fontsize=7.4, pad=10)
    fig.text(0.5, 0.01, "Sky plots: satellites spread across the sky give small position errors; clustered satellites "
             "amplify errors.", ha="center", fontsize=6.4, color=GREY)
    save(fig, "ch18_dopgeom")


def signals():
    f = np.linspace(1150, 1620, 6000)

    def bpsk(fc, rc):
        x = (f - fc) / rc
        return np.sinc(x) ** 2

    def boc(fc, fs, rc):
        x = (f - fc)
        y = (np.sinc(x / rc) * np.tan(np.pi * x / (2 * fs) + 1e-9)) ** 2
        y = np.where(np.abs(x) < 3 * fs + 2 * rc, y, 0)
        return 0.85 * y / y.max()
    rows = [("GPS", [("L5", bpsk(1176.45, 10.23), BLUE), ("L2C / P(Y)", bpsk(1227.6, 10.23) * 0.7, BLUE),
                     ("L1 C/A", bpsk(1575.42, 1.023), BLUE), ("M-code", np.clip(boc(1575.42, 10.23, 5.115), 0, 1) * 0.6, GREY)]),
            ("Galileo", [("E5a", bpsk(1176.45, 10.23), NAVY), ("E5b", bpsk(1207.14, 10.23), NAVY),
                         ("E6", bpsk(1278.75, 5.115), NAVY), ("E1", np.clip(boc(1575.42, 1.023, 1.023), 0, 1), NAVY)]),
            ("BeiDou", [("B2a", bpsk(1176.45, 10.23), ORANGE), ("B2b", bpsk(1207.14, 10.23), ORANGE),
                        ("B3I", bpsk(1268.52, 10.23), ORANGE), ("B1I", bpsk(1561.098, 2.046), ORANGE),
                        ("B1C", np.clip(boc(1575.42, 1.023, 1.023), 0, 1), ORANGE)]),
            ("GLONASS", [("G2 (FDMA)", bpsk(1246.0, 0.511 * 3) * 0.8, RED), ("G3 (CDMA)", bpsk(1202.025, 10.23), RED),
                         ("G1 (FDMA)", bpsk(1602.0, 0.511 * 3) * 0.8, RED)])]
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 3.4), gridspec_kw=dict(width_ratios=[2.6, 1], wspace=0.05))
    for j, (sysname, sigs) in enumerate(rows):
        base = (len(rows) - 1 - j) * 1.3
        for name, sp, c in sigs:
            for axx in (ax, bx):
                axx.fill_between(f, base, base + sp, color=c, alpha=0.45, lw=0)
            k = np.argmax(sp)
            tgt = ax if f[k] < 1400 else bx
            dx = {"B1I": -6, "B1C": 5, "L1 C/A": -4, "M-code": 9, "E1": 0}.get(name, 0)
            tgt.text(f[k] + dx, base + 1.03, name, fontsize=5.8, ha="center", va="bottom", color=c)
        ax.text(1143, base + 0.3, sysname, fontsize=7, ha="right", weight="bold")
    for x0, x1, n in [(1164, 1215, "lower L-band (ARNS)"), (1215, 1300, "L2 / E6 band")]:
        ax.axvspan(x0, x1, color=GOLD, alpha=0.07)
        ax.text((x0 + x1) / 2, -0.4, n, fontsize=6.0, ha="center", color="#7A5C00")
    bx.axvspan(1559, 1610, color=GOLD, alpha=0.07)
    bx.text(1584, -0.4, "upper L-band (ARNS)", fontsize=6.0, ha="center", color="#7A5C00")
    ax.set_xlim(1145, 1300)
    bx.set_xlim(1550, 1615)
    for axx in (ax, bx):
        axx.set_ylim(-0.65, 5.4)
        axx.set_yticks([])
        axx.grid(axis="y", visible=False)
    ax.spines["right"].set_visible(False)
    bx.spines["left"].set_visible(False)
    ax.set_xlabel("Frequency (MHz)")
    bx.set_xlabel("Frequency (MHz)")
    note(bx, "Schematic power spectra (normalised). Shared centre frequencies (1575.42, 1176.45 MHz)\nsimplify "
             "multi-GNSS receivers.", xy=(1, -0.17))
    save(fig, "ch18_signals")


def errors():
    items = [("Satellite clock & orbit", 0.5, 0.5), ("Ionosphere", 4.0, 0.1), ("Troposphere", 0.3, 0.3),
             ("Multipath", 0.8, 0.8), ("Receiver noise", 0.3, 0.2)]
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    y = np.arange(len(items))
    ax.barh(y - 0.18, [i[1] for i in items], height=0.34, color=RED, label="Single-frequency (L1 C/A)")
    ax.barh(y + 0.18, [i[2] for i in items], height=0.34, color=BLUE, label="Dual-frequency (L1/L5, E1/E5a)")
    ax.set_yticks(y)
    ax.set_yticklabels([i[0] for i in items], fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("Typical 1-σ range error (m)")
    s1 = np.sqrt(sum(i[1] ** 2 for i in items))
    s2 = np.sqrt(sum(i[2] ** 2 for i in items))
    ax.legend(fontsize=6.6, loc="lower right")
    ax.text(4.2, 0.3, f"UERE ≈ {s1:.1f} m\n(× PDOP ≈ 2 → ≈ {2*s1:.0f} m)", fontsize=6.6, color=RED, va="top")
    ax.text(4.2, 2.3, f"UERE ≈ {s2:.1f} m\n(× PDOP ≈ 2 → ≈ {2*s2:.1f} m)", fontsize=6.6, color=BLUE, va="top")
    ax.set_xlim(0, 6.5)
    ax.grid(axis="y", visible=False)
    note(ax, "Representative mid-latitude values for a good open-sky receiver; ionospheric errors vary strongly with "
             "solar activity.", xy=(1, -0.17))
    save(fig, "ch18_errors")


def iono():
    f = np.linspace(1000, 2600, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    for tec, c in [(10, SKY), (50, BLUE), (100, NAVY), (200, RED)]:
        ax.plot(f, 40.3 * tec * 1e16 / (f * 1e6) ** 2, color=c, lw=1.5, label=f"{tec} TECU")
    for fr, n in [(1176.45, "L5/E5a"), (1227.6, "L2"), (1575.42, "L1/E1"), (2492.0, "NavIC S")]:
        ax.axvline(fr, color=GREY, lw=0.6, ls=":")
        ax.text(fr + 10, 1, n, fontsize=6.3, color=GREY, rotation=90, va="bottom")
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Zenith ionospheric delay (m)")
    ax.set_ylim(0, 62)
    ax.legend(fontsize=6.6, title="Total electron content", title_fontsize=6.6, loc="upper right")
    note(ax, "First-order delay = 40.3·TEC/f². 1 TECU = 10¹⁶ electrons/m². Dual-frequency receivers remove it.",
         xy=(1, -0.21))
    save(fig, "ch18_iono")


def relativity():
    GM, c, R = 3.986004418e14, 299792458.0, 6371e3
    h = np.logspace(np.log10(200e3), np.log10(60000e3), 400)
    r = R + h
    v = np.sqrt(GM / r)
    grav = GM / c ** 2 * (1 / R - 1 / r) * 86400e6
    vel = -v ** 2 / (2 * c ** 2) * 86400e6
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.plot(h / 1e3, grav, color=GREEN, lw=1.4, label="Gravitational (general relativity): clock runs faster")
    ax.plot(h / 1e3, vel, color=RED, lw=1.4, label="Orbital velocity (special relativity): clock runs slower")
    ax.plot(h / 1e3, grav + vel, color=NAVY, lw=2, label="Net effect")
    ax.axhline(0, color=INK, lw=0.6)
    hg = 20200e3
    tot = (GM / c ** 2 * (1 / R - 1 / (R + hg)) - GM / (R + hg) / (2 * c ** 2)) * 86400e6
    ax.plot(20200, tot, "o", color=ORANGE, ms=6)
    ax.annotate(f"GPS: +{tot:.1f} µs/day\n(≈ 11 km/day of range error\nif uncorrected)", (20200, tot), xytext=(1500, 30),
                fontsize=6.6, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.set_xscale("log")
    ax.set_xlabel("Orbit altitude (km)")
    ax.set_ylabel("Clock offset vs ground (µs per day)")
    ax.set_xlim(200, 60000)
    ax.set_ylim(-32, 62)
    ax.legend(fontsize=6.3, loc="upper left")
    note(ax, "Circular orbits, spherical Earth; ground clock at sea level (Earth-rotation term neglected).", xy=(1, -0.16))
    save(fig, "ch18_relativity")


def accuracy():
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    pts = [("Standalone, single-freq.", 3, 0.5, RED), ("Standalone, dual-freq. (L1/L5 phones)", 1.4, 0.5, ORANGE),
           ("SBAS", 0.9, 2, GOLD), ("Code DGNSS", 0.5, 0.7, GREEN),
           ("PPP (global corrections)", 0.04, 20, BLUE), ("PPP-AR / Galileo HAS", 0.2, 5, SKY),
           ("PPP-RTK", 0.03, 1, VIOLET), ("RTK (base ≤ 20 km)", 0.015, 0.1, NAVY),
           ("Post-processed geodetic\n(daily solutions)", 0.003, 1440, GREY)]
    for n, acc, t, c in pts:
        ax.plot(t, acc, "o", color=c, ms=7, mec="white")
        ax.annotate(n, (t, acc), xytext=(7, -2), textcoords="offset points", fontsize=6.4, color=c)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.0005, 20000)
    ax.set_ylim(0.002, 10)
    ax.set_xlabel("Time to reach accuracy (minutes)")
    ax.set_ylabel("Horizontal accuracy (m, ≈ 95 %)")
    note(ax, "Representative values; actual performance depends on receiver, antenna, environment and service.",
         xy=(1, -0.16))
    save(fig, "ch18_accuracy")


def sbas():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.0, 3.3))
    ax = world_axes(fig, extent=(-180, 180, -55, 80))
    areas = [("WAAS (USA)", (-170, -50, 10, 72), BLUE), ("EGNOS (EU)", (-25, 40, 27, 72), GREEN),
             ("SDCM (Russia)", (40, 180, 45, 78), RED), ("BDSBAS (China)", (73, 135, 15, 54), ORANGE),
             ("GAGAN (India)", (66, 98, 5, 37), VIOLET), ("MSAS (Japan)", (125, 150, 24, 46), NAVY),
             ("KASS (Korea)", (124, 132, 33, 39), GOLD), ("SouthPAN (Aus/NZ)", (110, 180, -48, -9), SKY),
             ("A-SBAS (Africa)", (-20, 52, -35, 25), GREY)]
    for n, (x0, x1, y0, y1), c in areas:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, alpha=0.18, ec=c, lw=1.1,
                               transform=ccrs.PlateCarree()))
        ax.text((x0 + x1) / 2, y0 + 2, n, fontsize=6.2, color=c, ha="center", va="bottom", weight="bold",
                transform=ccrs.PlateCarree())
    note(ax, "Approximate service regions of satellite-based augmentation systems (SBAS) operating or in development.",
         xy=(1, -0.03))
    save(fig, "ch18_sbas")


def rtk():
    fig, ax = canvas(7.0, 3.0, xlim=(0, 100), ylim=(0, 42))
    ax.plot([2, 98], [6, 6], color="#8B7D5A", lw=1.5)
    for x, y in [(15, 38), (50, 40), (85, 37)]:
        satellite(ax, x, y, s=0.8)
        ax.plot([x, 22], [y - 1.5, 10], color=ORANGE, lw=0.6, ls="--")
        ax.plot([x, 74], [y - 1.5, 10], color=BLUE, lw=0.6, ls="--")
    ax.add_patch(Polygon([[20, 6], [24, 6], [22, 10]], closed=True, fc=ORANGE))
    label(ax, 22, 2.5, "base station\n(known position)", fs=6.6, color=ORANGE)
    ax.add_patch(Rectangle((72, 6), 4, 4, fc=BLUE))
    label(ax, 74, 2.5, "rover (tractor, drone,\nsurvey pole)", fs=6.6, color=BLUE)
    arrow(ax, (26, 12), (70, 12), color=GREEN, text="corrections via radio / internet (RTCM)", fs=6.6, toff=(0, 0.6))
    box(ax, 30, 18, 40, 13, "Carrier phase λ ≈ 19 cm (L1): measured to ≈ 1 mm,\nbut the whole number of cycles (ambiguity)"
        " is unknown.\nDifferencing with the base cancels common errors;\nresolving ambiguities gives cm accuracy.",
        fs=6.4, fc="white")
    save(fig, "ch18_rtk")


def jamming():
    d = np.logspace(-1, 3, 300)
    fspl = 32.45 + 20 * np.log10(1575.42) + 20 * np.log10(d)
    S = -128.5
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for p_w, c in [(0.01, SKY), (1, BLUE), (100, NAVY), (10000, RED)]:
        J = 10 * np.log10(p_w * 1000) - fspl
        ax.plot(d, J - S, color=c, lw=1.5, label=f"{p_w:g} W jammer")
    ax.axhline(40, color=ORANGE, lw=1, ls="--")
    ax.text(0.12, 42, "C/A-code tracking lost (J/S ≈ 40 dB)", fontsize=6.6, color=ORANGE)
    ax.axhline(55, color=GREEN, lw=1, ls=":")
    ax.text(0.12, 57, "robust military receiver (illustrative)", fontsize=6.6, color=GREEN)
    ax.set_xscale("log")
    ax.set_xlabel("Distance from jammer, line of sight (km)")
    ax.set_ylabel("Jamming-to-signal ratio J/S (dB)")
    ax.set_xlim(0.1, 1000)
    ax.set_ylim(-20, 130)
    ax.legend(fontsize=6.6, loc="upper right")
    note(ax, "Free-space propagation at 1 575 MHz, isotropic antennas; GNSS signal −128.5 dBm. Terrain and the "
             "radio horizon limit real ranges.", xy=(1, -0.17))
    save(fig, "ch18_jamming")


def history():
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ev = [(1960.3, "Transit 1B\n(first navsat)"), (1967.0, "Timation"), (1973.7, "GPS approved\n(NAVSTAR)"),
          (1978.2, "First GPS\nBlock I"), (1982.8, "First GLONASS"), (1995.3, "GPS full\noperational"),
          (2000.4, "Selective\nAvailability off"), (2000.8, "BeiDou-1"), (2005.9, "GIOVE-A\n(Galileo)"),
          (2010.7, "QZS-1"), (2011.8, "GLONASS\nrestored to 24"), (2013.5, "IRNSS-1A"),
          (2016.9, "Galileo initial\nservices"), (2018.9, "First GPS III"), (2020.6, "BeiDou-3\ncomplete"),
          (2023.1, "Galileo HAS"), (2025.5, "Galileo OSNMA"), (2026.3, "Last GPS III")]
    timeline(ax, ev, y=0, x0=1958, x1=2028, stagger=3, height=1.0, fs=6.0)
    ax.set_xlim(1956, 2029)
    ax.set_ylim(-4.9, 4.9)
    ax.axis("off")
    for yr in range(1960, 2030, 10):
        ax.text(yr, -0.35, str(yr), fontsize=6.2, ha="center", va="top", color=GREY)
    save(fig, "ch18_history")


def space_volume():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 100), ylim=(0, 46))
    earth(ax, 30, 23, 6)
    for ang in np.linspace(0, 2 * np.pi, 9)[:-1]:
        x, y = 30 + 13 * np.cos(ang), 23 + 13 * np.sin(ang)
        satellite(ax, x, y, s=0.5)
    ax.add_patch(Circle((30, 23), 13, fc="none", ec=GREY, lw=0.5, ls=":"))
    ax.add_patch(Circle((30, 23), 22, fc="none", ec=GREY, lw=0.5, ls="--"))
    label(ax, 30, 3.5, "GNSS MEO shell (≈ 20 000 km) and GEO (36 000 km)", fs=6.4, color=GREY)
    xs, ys = 43, 23
    ax.add_patch(Polygon([[xs, ys], [92, ys + 9], [92, ys - 9]], closed=True, fc=ORANGE, alpha=0.12, ec="none"))
    label(ax, 76, 34.5, "main-lobe and side-lobe signals\nspilling past the Earth", fs=6.4, color=ORANGE)
    planet(ax, 92, 23, 3.0, "#BDBDBD")
    label(ax, 92, 17.5, "Moon\n(384 000 km)", fs=6.4)
    satellite(ax, 61, 37, s=0.6)
    label(ax, 61, 41.5, "GEO / HEO users", fs=6.4)
    box(ax, 50, 3, 40, 11, "LuGRE (2025) tracked GPS and Galileo on the Moon:\nsignals ≈ 30 dB weaker than on Earth, "
        "high-gain antenna\nand sensitive receiver needed", fs=6.2, fc="white")
    save(fig, "ch18_spacevolume")


if __name__ == "__main__":
    fns = [orbits, trilateration, correlation, dop, dop_geom, signals, errors, iono, relativity, accuracy, sbas, rtk,
           jamming, history, space_volume]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
