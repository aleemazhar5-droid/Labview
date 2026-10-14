import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, Wedge

ROOT = Path(__file__).resolve().parents[2]
SW = json.load(open(ROOT / "data/spaceweather.json"))


def tdec(tag):
    y, m = tag.split("-")[:2]
    return int(y) + (int(m) - 0.5) / 12


def cycles():
    mon = SW["monthly"]
    t = np.array([tdec(r[0]) for r in mon])
    s = np.array([r[1] for r in mon], float)
    sm = np.array([r[2] if r[2] and r[2] > 0 else np.nan for r in mon], float)
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    ax.plot(t, s, color=SKY, lw=0.4, alpha=0.8)
    ax.plot(t, sm, color=NAVY, lw=1.3)
    mins = [1755.2, 1766.5, 1775.5, 1784.7, 1798.3, 1810.6, 1823.3, 1833.9, 1843.5, 1855.9, 1867.2, 1878.9, 1890.2,
            1902.0, 1913.6, 1923.6, 1933.8, 1944.2, 1954.3, 1964.9, 1976.5, 1986.8, 1996.4, 2008.9, 2019.9]
    for k, (a, b) in enumerate(zip(mins[:-1], mins[1:] + [2031])):
        if k % 2 == 0 or k >= 22:
            ax.text((a + b) / 2, 395, str(k + 1), fontsize=5.6, ha="center", color=GREY)
    ax.text(2025, 395, "25", fontsize=5.6, ha="center", color=RED)
    ax.axvspan(1645, 1715, color=GREY, alpha=0.1)
    ax.set_xlim(1749, 2030)
    ax.set_ylim(0, 410)
    ax.set_ylabel("Sunspot number")
    ax.text(1752, 395, "cycle:", fontsize=5.6, color=GREY, ha="left")
    note(ax, "Light blue: monthly means; dark: 13-month smoothed. Data: SILSO / Royal Observatory of Belgium (v2), via NOAA SWPC.", xy=(1, -0.12))
    save(fig, "ch22_cycles")


def cycle25():
    mon = SW["monthly"]
    t = np.array([tdec(r[0]) for r in mon])
    s = np.array([r[1] for r in mon], float)
    sm = np.array([r[2] if r[2] and r[2] > 0 else np.nan for r in mon], float)
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    for start, c, n in [(2008.9, GREY, "Cycle 24 (began Dec 2008)"), (2019.9, RED, "Cycle 25 (began Dec 2019)")]:
        sel = (t >= start) & (t < start + 12)
        ax.plot(t[sel] - start, sm[sel], color=c, lw=1.8, label=n)
        ax.plot(t[sel] - start, s[sel], color=c, lw=0.5, alpha=0.4)
    p = SW["pred"]
    tp = np.array([tdec(r[0]) for r in p]) - 2019.9
    ax.fill_between(tp, [r[2] for r in p], [r[3] for r in p], color=RED, alpha=0.12, label="NOAA forecast range")
    ax.axhline(115, color=ORANGE, lw=0.9, ls="--")
    ax.text(0.2, 119, "2019 expert panel forecast peak: 115", fontsize=6.4, color=ORANGE)
    i = np.nanargmax(np.where(t > 2019.9, sm, np.nan))
    ax.annotate(f"Cycle 25 maximum: {sm[i]:.1f}\n({mon[i][0]})", (t[i] - 2019.9, sm[i]), xytext=(6.6, 170),
                fontsize=6.6, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 230)
    ax.set_xlabel("Years since start of cycle")
    ax.set_ylabel("Sunspot number")
    ax.legend(fontsize=6.4, loc="upper left")
    note(ax, "Thin lines: monthly values; thick lines: 13-month smoothed. Data: SILSO, NOAA SWPC.", xy=(1, -0.16))
    save(fig, "ch22_cycle25")


def storms_by_year():
    a = SW["annual"]
    yrs = sorted(int(k) for k in a if int(k) < 2026)
    f = np.array([a[str(y)]["f107"] or np.nan for y in yrs])
    sd = np.array([a[str(y)]["storm_days_ap50"] for y in yrs])
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.bar(yrs, sd, color=RED, width=0.8, label="Days with Ap ≥ 50 (major storms)")
    ax.set_ylabel("Storm days per year", color=RED)
    ax2 = ax.twinx()
    ax2.plot(yrs, f, color=NAVY, lw=1.2, label="Annual mean F10.7 solar radio flux")
    ax2.set_ylabel("F10.7 (sfu)", color=NAVY)
    ax2.grid(False)
    ax.set_xlim(1932, 2026)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=6.4, loc="upper left")
    note(ax, "Data: GFZ Potsdam Kp/Ap index and F10.7 flux (Penticton/Ottawa). Storms are most frequent in the "
             "declining phase of each cycle.", xy=(1, -0.16))
    save(fig, "ch22_stormsyears")


def may2024():
    rows = SW["may2024"]
    kp = np.array([k for _, ks in rows for k in ks])
    t = np.arange(len(kp)) * 3 / 24
    cols = [GREEN if k < 5 else (GOLD if k < 6 else (ORANGE if k < 7 else (RED if k < 8 else "#7A0019"))) for k in kp]
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.bar(t + 1.5 / 24, kp, width=3 / 24 * 0.9, color=cols)
    ax.set_xticks(np.arange(0, 7, 1))
    ax.set_xticklabels([f"{d} May" for d in range(8, 15)], fontsize=6.8)
    ax.set_ylim(0, 9.4)
    ax.set_ylabel("Kp index (3-hourly)")
    for g, lv in [("G1", 5), ("G2", 6), ("G3", 7), ("G4", 8), ("G5", 9)]:
        ax.axhline(lv, color=GREY, lw=0.5, ls=":")
        ax.text(7.02, lv, g, fontsize=6.4, va="center", color=GREY)
    ax.set_xlim(0, 7.2)
    note(ax, "Data: GFZ Potsdam definitive Kp. The 10–11 May 2024 'Gannon storm' reached Kp 9 (G5), the strongest "
             "since 2003.", xy=(1, -0.16))
    save(fig, "ch22_may2024")


def sun_earth():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 100), ylim=(0, 46))
    ax.add_patch(Circle((6, 23), 10, fc="#F6A623", ec="#E07B00", lw=1.5))
    label(ax, 6, 23, "Sun", fs=7.5, weight="bold")
    ax.add_patch(Ellipse((30, 30), 18, 12, angle=-10, fc=RED, alpha=0.25, ec=RED))
    label(ax, 30, 30, "CME\n1 000–3 000 km/s", fs=6.4, color=RED)
    for y in (10, 16, 36, 40):
        ax.annotate("", (55, y), (17, y), arrowprops=dict(arrowstyle="->", color=SKY, lw=0.8))
    label(ax, 36, 12.5, "solar wind 300–800 km/s", fs=6.4, color=BLUE)
    ax.annotate("", (88, 23), (15, 23), arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2, ls="--"))
    label(ax, 47, 24.8, "light & X-rays: 8 min; energetic particles: 15 min – hours", fs=6.2, color="#8A6D00")
    ax.plot(68, 23, "s", color=NAVY, ms=5)
    label(ax, 68, 19.5, "L1 monitors\n(1.5 million km)", fs=6.2, color=NAVY)
    th = np.linspace(-1.1, 1.1, 60)
    ax.plot(88 - 8 * np.cos(th) * 1.2, 23 + 12 * np.sin(th), color=VIOLET, lw=1.2)
    label(ax, 76, 36, "bow shock", fs=6.2, color=VIOLET)
    ax.plot(88 - 4.5 * np.cos(th), 23 + 8 * np.sin(th), color=GREEN, lw=1.2)
    label(ax, 84, 33, "magnetopause", fs=6.0, color=GREEN)
    earth(ax, 90, 23, 2.5)
    for r in (4, 6):
        ax.add_patch(Ellipse((90, 23), r * 1.6, r * 1.1, fc="none", ec=ORANGE, lw=0.8, ls=":"))
    label(ax, 94, 15, "radiation\nbelts", fs=6.0, color=ORANGE)
    label(ax, 90, 4, "Earth", fs=6.8)
    save(fig, "ch22_sunearth")


def warning_time():
    v = np.linspace(250, 3000, 300)
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    ax.plot(v, 1.5e6 / v / 60, color=NAVY, lw=1.6, label="L1 to Earth (1.5 million km)")
    ax.plot(v, 1.496e8 / v / 3600, color=ORANGE, lw=1.6, label="Sun to Earth (hours)")
    ax.set_xlabel("Speed (km/s)")
    ax.set_ylabel("Travel time (minutes / hours)")
    for x, n in [(400, "slow wind"), (750, "fast wind"), (2000, "extreme CME")]:
        ax.axvline(x, color=GREY, lw=0.6, ls=":")
        ax.text(x + 20, 4, n, fontsize=6.3, color=GREY)
    ax.set_ylim(0, 110)
    ax.set_xlim(250, 3000)
    ax.legend(fontsize=6.4, loc="center right")
    note(ax, "Blue: minutes of warning from an L1 monitor; orange: hours for a CME to travel from the Sun to the Earth.",
         xy=(1, -0.16))
    save(fig, "ch22_warningtime")


def drag():
    F = np.linspace(65, 250, 200)
    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    for Ap, c in [(4, GREEN), (15, BLUE), (50, ORANGE), (150, RED), (300, "#7A0019")]:
        T = 379 + 3.24 * F + 1.3 * Ap
        rho = 3e-12 * np.exp((T - 1000) / 200)
        ax.plot(F, rho * 1e12, color=c, lw=1.6, label=f"Ap = {Ap}")
    ax.set_xlabel("Solar F10.7 flux (sfu)")
    ax.set_ylabel("Density at 400 km (10⁻¹² kg/m³)")
    ax.set_yscale("log")
    ax.legend(fontsize=6.4, title="geomagnetic activity", title_fontsize=6.4, loc="upper left")
    note(ax, "Illustrative empirical scaling of exospheric temperature with F10.7 and Ap (after Jacchia-type models). "
             "Storms can multiply density several-fold.", xy=(1, -0.16))
    save(fig, "ch22_drag")


def gic():
    fig, ax = canvas(7.0, 3.2, xlim=(0, 100), ylim=(0, 44))
    ax.add_patch(Rectangle((0, 0), 100, 14, fc="#D9CBA7", ec="none"))
    ax.add_patch(Rectangle((0, 0), 100, 5, fc="#BBA77A", ec="none"))
    label(ax, 50, 2.5, "resistive bedrock: larger induced electric field", fs=6.4, color="#4E3D16")
    for x in (15, 85):
        ax.plot([x, x], [14, 30], color=GREY, lw=2)
        ax.add_patch(Rectangle((x - 4, 14), 8, 6, fc=NAVY, ec="none"))
        label(ax, x, 17, "transformer", fs=5.8, color="white")
    ax.plot([15, 85], [30, 30], color=GREY, lw=1.4)
    label(ax, 50, 32, "high-voltage transmission line", fs=6.4, color=GREY)
    ax.annotate("", (80, 10), (20, 10), arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    label(ax, 50, 11.8, "geoelectric field E (V/km) induced by changing magnetic field", fs=6.4, color=RED)
    for x in np.linspace(10, 90, 9):
        ax.annotate("", (x, 38), (x, 43), arrowprops=dict(arrowstyle="->", color=VIOLET, lw=0.8))
    label(ax, 50, 41, "ionospheric electrojet currents → rapidly varying dB/dt at ground", fs=6.4, color=VIOLET)
    ax.annotate("", (15, 22), (15, 28), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
    label(ax, 25, 25, "quasi-DC current\nflows through grounded\nneutrals → saturation,\nheating, harmonics", fs=6.0,
          color=ORANGE, ha="left")
    save(fig, "ch22_gic")


def scint_map():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.0, 3.2))
    ax = world_axes(fig)
    lon = np.linspace(-180, 180, 361)
    dip = 9 * np.sin(np.radians(lon + 70)) - 2
    ax.fill_between(lon, dip - 18, dip + 18, color=ORANGE, alpha=0.25, transform=ccrs.PlateCarree())
    ax.fill_between(lon, 58 + 6 * np.cos(np.radians(lon + 70)), 76 + 4 * np.cos(np.radians(lon + 70)), color=VIOLET,
                    alpha=0.25, transform=ccrs.PlateCarree())
    ax.fill_between(lon, -76 - 4 * np.cos(np.radians(lon - 110)), -58 - 6 * np.cos(np.radians(lon - 110)), color=VIOLET,
                    alpha=0.25, transform=ccrs.PlateCarree())
    ax.text(-30, 2, "equatorial anomaly: strongest scintillation after sunset", fontsize=6.4, color="#8A4B00",
            transform=ccrs.PlateCarree(), ha="center")
    ax.text(-100, 66, "auroral / polar regions", fontsize=6.4, color=VIOLET, transform=ccrs.PlateCarree(), ha="center")
    note(ax, "Schematic regions of frequent ionospheric scintillation affecting GNSS and satellite communications "
             "(after NOAA SWPC).", xy=(1, -0.03))
    save(fig, "ch22_scint")


def event_timeline():
    fig, ax = plt.subplots(figsize=(7.0, 2.5))
    rows = [("Flare X-rays / EUV (R scale)", 0.14, 1.5, GOLD), ("Radio bursts", 0.14, 2.0, SKY),
            ("Solar energetic particles (S scale)", 0.3, 72, RED), ("CME arrival, geomagnetic storm (G scale)", 24, 96, VIOLET)]
    for j, (n, a, b, c) in enumerate(rows):
        ax.barh(j, b - a, left=a, color=c, height=0.55, alpha=0.85)
        ax.text(a, j - 0.38, n, fontsize=6.5, va="bottom")
    ax.set_xscale("log")
    ax.set_xlim(0.1, 150)
    ax.set_ylim(len(rows) - 0.4, -0.9)
    ax.set_yticks([])
    ax.set_xticks([0.14, 1, 6, 24, 72])
    ax.set_xticklabels(["8 min", "1 h", "6 h", "1 day", "3 days"])
    ax.set_xlabel("Time after the eruption (log scale)")
    ax.grid(axis="y", visible=False)
    save(fig, "ch22_eventtimeline")


if __name__ == "__main__":
    fns = [cycles, cycle25, storms_by_year, may2024, sun_earth, warning_time, drag, gic, scint_map, event_timeline]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
