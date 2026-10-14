import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse

ROOT = Path(__file__).resolve().parents[2]
S = json.load(open(ROOT / "data/ssa_stats.json"))
TCOL = {"PAY": BLUE, "R/B": ORANGE, "DEB": RED, "UNK": GREY}
TNAME = {"PAY": "Payloads", "R/B": "Rocket bodies", "DEB": "Debris", "UNK": "Unknown"}


def population():
    yrs = np.array(S["years"])
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    data = [np.array(S["pop"][t]) for t in ["PAY", "R/B", "DEB", "UNK"]]
    ax.stackplot(yrs, *data, colors=[TCOL[t] for t in ["PAY", "R/B", "DEB", "UNK"]], alpha=0.85,
                 labels=[TNAME[t] for t in ["PAY", "R/B", "DEB", "UNK"]])
    for yr, txt, dy in [(2007, "Chinese ASAT test", 2500), (2009, "Iridium–Cosmos\ncollision", 5200),
                        (2019, "Starlink deployment\nbegins", 2500), (2021.9, "Russian\nASAT test", 6500)]:
        ytot = sum(d[np.searchsorted(yrs, int(yr))] for d in data)
        ax.annotate(txt, (yr, ytot), xytext=(yr - 12, ytot + dy), fontsize=6.4,
                    arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.set_xlim(1957, 2026.8)
    ax.set_ylim(0, 40000)
    ax.set_xlabel("Year")
    ax.set_ylabel("Catalogued objects in Earth orbit")
    ax.legend(fontsize=6.6, loc="upper left")
    tot = sum(d[-1] for d in data)
    note(ax, f"Computed from launch and decay dates in the CelesTrak SATCAT (publicly catalogued objects only); "
             f"{tot:,} in orbit on 14 Oct 2026.", xy=(1, -0.16))
    save(fig, "ch21_population")


def density():
    edges = np.arange(200, 2025, 25)
    R = 6371.0
    vol = 4 / 3 * np.pi * ((R + edges[1:]) ** 3 - (R + edges[:-1]) ** 3)
    fig, ax = plt.subplots(figsize=(6.8, 3.3))
    bottom = np.zeros(len(edges) - 1)
    for t in ["PAY", "R/B", "DEB", "UNK"]:
        h, _ = np.histogram(S["leo_alt"].get(t, []), bins=edges)
        dens = h / vol * 1e8
        ax.bar(edges[:-1], dens, width=25, bottom=bottom, align="edge", color=TCOL[t], label=TNAME[t], alpha=0.9)
        bottom += dens
    ax.set_xlim(200, 2000)
    ax.set_xlabel("Mean altitude (km)")
    ax.set_ylabel("Spatial density (objects per 10⁸ km³)")
    ax.legend(fontsize=6.6, loc="upper right")
    ax.annotate("Starlink shells", (530, bottom[np.searchsorted(edges, 525) - 1]), xytext=(700, bottom.max() * 0.9),
                fontsize=6.6, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.annotate("old debris and rocket bodies\n(Fengyun-1C, Iridium–Cosmos)", (850, bottom[np.searchsorted(edges, 850) - 1]),
                xytext=(1100, bottom.max() * 0.55), fontsize=6.6, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    note(ax, "Objects binned by mean altitude, 25 km shells (CelesTrak SATCAT, October 2026).", xy=(1, -0.16))
    save(fig, "ch21_density")


LABELS = {"1999-025": "Fengyun-1C ASAT test (2007)", "1982-092": "Cosmos 1408 ASAT test (2021)",
          "1993-036": "Cosmos 2251 collision (2009)", "2022-151": "Long March 6A stage (2022)",
          "1994-029": "Pegasus HAPS stage (1996)", "2024-140": "Long March 6A stage (2024)",
          "1997-051": "Iridium 33 collision (2009)", "2006-026": "Cosmos 2421 (2008)",
          "1986-019": "Ariane 1 stage (1986)", "1981-053": "Cosmos 1275 (1981)",
          "1965-082": "Titan IIIC transtage (1965)", "2000-055": "NOAA 16 (2015)"}


def fragmentations():
    top = [t for t in S["top_frag"] if t[0] in LABELS][:12]
    names = [LABELS[t[0]] for t in top]
    cat = [t[2] for t in top]
    orb = [t[3] for t in top]
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    y = np.arange(len(names))
    ax.barh(y, cat, color=GREY, height=0.65, label="Catalogued fragments")
    ax.barh(y, orb, color=RED, height=0.65, label="Still in orbit (Oct 2026)")
    for yi, c, o in zip(y, cat, orb):
        ax.text(c + 30, yi, f"{c:,} / {o:,}", va="center", fontsize=6.4)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=6.8)
    ax.invert_yaxis()
    ax.set_xlim(0, 4200)
    ax.set_xlabel("Number of catalogued debris objects")
    ax.legend(fontsize=6.6, loc="lower right")
    ax.grid(axis="y", visible=False)
    note(ax, "Debris grouped by the international designator of the parent launch (CelesTrak SATCAT).", xy=(1, -0.14))
    save(fig, "ch21_fragmentations")


def reentries():
    d = S["reentries"]
    yrs = sorted(int(k) for k in d)
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    bottom = np.zeros(len(yrs))
    for t in ["PAY", "R/B", "DEB", "UNK"]:
        v = np.array([d[str(y)].get(t, 0) for y in yrs])
        ax.bar(yrs, v, bottom=bottom, color=TCOL[t], label=TNAME[t], width=0.75)
        bottom += v
    ax.set_xlabel("Year (2026 to mid-October)")
    ax.set_ylabel("Catalogued objects re-entering")
    ax.legend(fontsize=6.6, loc="upper left")
    ax.annotate("decay of Cosmos 1408\ndebris and old Starlinks", (2022, bottom[yrs.index(2022)]), xytext=(2008, 2300),
                fontsize=6.4, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    note(ax, "CelesTrak SATCAT decay dates. Most re-entries are small objects that burn up completely.", xy=(1, -0.16))
    save(fig, "ch21_reentries")


def lifetime():
    R, mu = 6378.137e3, 3.986004418e14

    def rho(h, act):
        H = 60 + 0.12 * (h - 300) if h > 300 else 50 + (h - 200) * 0.1
        base = {"low": 1.2e-12, "high": 6e-12}[act] * 0.6
        return base * np.exp(-(h - 400) / H) if h > 120 else 1e-8
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    hs = np.arange(250, 1001, 25)
    for B, c in [(20, BLUE), (50, GREEN), (150, ORANGE)]:
        for act, ls in [("low", "-"), ("high", "--")]:
            life = []
            for h0 in hs:
                h, t = float(h0), 0.0
                while h > 150 and t < 300 * 365.25 * 86400:
                    a = R + h * 1e3
                    v = np.sqrt(mu / a)
                    dadt = -np.sqrt(mu * a) * rho(h, act) / B
                    dt = max(3600.0, min(30 * 86400.0, 0.5 * 1e3 / abs(dadt)))
                    h += dadt * dt / 1e3
                    t += dt
                life.append(t / (365.25 * 86400))
            ax.plot(hs, life, color=c, ls=ls, lw=1.4,
                    label=f"B = {B} kg/m², solar {'minimum' if act == 'low' else 'maximum'}")
    ax.axhline(25, color=RED, lw=0.9, ls=":")
    ax.text(260, 28, "25-year guideline (IADC)", fontsize=6.4, color=RED)
    ax.axhline(5, color=VIOLET, lw=0.9, ls=":")
    ax.text(260, 5.6, "5-year rule (FCC, 2024)", fontsize=6.4, color=VIOLET)
    ax.set_yscale("log")
    ax.set_ylim(0.05, 200)
    ax.set_xlim(250, 1000)
    ax.set_xlabel("Initial circular altitude (km)")
    ax.set_ylabel("Orbital lifetime (years)")
    ax.legend(fontsize=5.9, loc="lower right", ncol=2)
    note(ax, "Simplified exponential atmosphere scaled for solar activity; ballistic coefficient B = m / (C_D A). "
             "Illustrative only.", xy=(1, -0.16))
    save(fig, "ch21_lifetime")


def detectability():
    r = np.logspace(2, 4.7, 200)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    d = np.logspace(-3, 1.5, 600)

    def sig(dd, lam):
        x = np.pi * dd / lam
        return np.pi * dd ** 2 / 4 * x ** 4 / (1 + x ** 4)
    for name, lam, d0, r0, c in [("S-band radar, λ = 10 cm", 0.10, 0.10, 1000, BLUE),
                                 ("UHF radar, λ = 70 cm", 0.70, 0.30, 1000, NAVY)]:
        need = sig(d0, lam) * (r / r0) ** 4
        s_tab = sig(d, lam)
        dmin = np.interp(np.log10(need), np.log10(s_tab), d)
        dmin = np.where(need > s_tab.max(), np.nan, dmin)
        ax.plot(r, dmin * 100, color=c, lw=1.6, label=f"{name} (detects {d0*100:.0f} cm at {r0} km)")
    dopt = 0.05 * (r / 1000)
    ax.plot(r, dopt * 100, color=ORANGE, lw=1.6, label="≈ 1 m optical telescope, sunlit object (illustrative)")
    for x, n in [(1000, "LEO"), (20000, "MEO"), (35786, "GEO")]:
        ax.axvline(x, color=GREY, lw=0.6, ls=":")
        ax.text(x * 1.05, 600, n, fontsize=6.4, color=GREY)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(200, 50000)
    ax.set_ylim(0.5, 1000)
    ax.set_xlabel("Range (km)")
    ax.set_ylabel("Smallest detectable size (cm)")
    ax.legend(fontsize=6.2, loc="upper left")
    note(ax, "Radar echo ∝ σ / R⁴ (σ falls steeply for objects smaller than the wavelength); reflected sunlight ∝ size² / "
             "R². Illustrative scaling.", xy=(1, -0.16))
    save(fig, "ch21_detectability")


def pc():
    from scipy.special import erf
    miss = np.linspace(0, 3000, 300)
    R = 20.0
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for s, c in [(50, GREEN), (200, BLUE), (500, ORANGE), (2000, RED)]:
        P = (R ** 2 / (2 * s ** 2)) * np.exp(-miss ** 2 / (2 * s ** 2))
        ax.plot(miss, np.maximum(P, 1e-12), color=c, lw=1.6, label=f"position uncertainty σ = {s} m")
    ax.axhline(1e-4, color=GREY, lw=0.9, ls="--")
    ax.text(2950, 1.4e-4, "typical manoeuvre threshold 1 in 10 000", fontsize=6.4, color=GREY, ha="right")
    ax.set_yscale("log")
    ax.set_ylim(1e-10, 1e-1)
    ax.set_xlim(0, 3000)
    ax.set_xlabel("Predicted miss distance (m)")
    ax.set_ylabel("Probability of collision")
    ax.legend(fontsize=6.4, loc="upper right")
    note(ax, "Two-dimensional encounter-plane model, circular uncertainty, combined hard-body radius 20 m. Large "
             "uncertainty caps the computed probability ('dilution').", xy=(1, -0.16))
    save(fig, "ch21_pc")


def encounter():
    fig, ax = canvas(7.0, 3.1, xlim=(0, 100), ylim=(0, 42))
    ax.add_patch(Ellipse((60, 21), 46, 16, angle=15, fc=BLUE, alpha=0.12, ec=BLUE, lw=1))
    ax.add_patch(Ellipse((60, 21), 26, 9, angle=15, fc=BLUE, alpha=0.18, ec=BLUE, lw=0.8))
    ax.add_patch(Circle((67, 24), 3.0, fc=RED, alpha=0.5, ec=RED))
    ax.plot(60, 21, "+", color=NAVY, ms=10)
    darrow(ax, (60, 21), (67, 24), color=INK, text="miss vector", fs=6.4, toff=(-3, 0.5))
    label(ax, 80, 33, "combined position-uncertainty\nellipse (covariance)", fs=6.6, color=BLUE)
    label(ax, 75, 13, "hard-body circle\n(combined size)", fs=6.6, color=RED)
    box(ax, 2, 6, 34, 30, "Encounter plane\n(perpendicular to relative velocity)\n\nP_c = integral of the 2-D\nprobability "
        "density over the\nhard-body circle\n\nTypical LEO encounter:\nrelative speed 10–15 km/s,\nduration < 1 s",
        fs=6.4, fc="white")
    save(fig, "ch21_encounter")


def impact_energy():
    d = np.logspace(-4, 0, 200)
    m = 2700 * np.pi / 6 * d ** 3
    E = 0.5 * m * 10e3 ** 2
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.plot(d * 100, E, color=NAVY, lw=1.8)
    regions = [(0.01, 0.1, "erosion,\npitting", GREEN), (0.1, 1, "penetrates unshielded\nwalls; shielding works", GOLD),
               (1, 10, "too small to track,\ntoo big to shield", ORANGE), (10, 100, "tracked:\navoid by manoeuvre", RED)]
    for a, b, t, c in regions:
        ax.axvspan(a, b, color=c, alpha=0.12)
        ax.text(np.sqrt(a * b), 3e7, t, fontsize=6.4, ha="center", color=c, va="top")
    for e, n in [(4.184e6, "1 kg TNT"), (2e5, "car at 70 km/h (≈ 200 kJ)")]:
        ax.axhline(e, color=GREY, lw=0.6, ls=":")
        ax.text(0.011, e * 1.3, n, fontsize=6.2, color=GREY)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.01, 100)
    ax.set_ylim(1e-3, 1e9)
    ax.set_xlabel("Diameter of aluminium sphere (cm)")
    ax.set_ylabel("Kinetic energy at 10 km/s (J)")
    note(ax, "A 1 cm aluminium sphere at 10 km/s carries ≈ 70 kJ — the energy of a small car crash.", xy=(1, -0.16))
    save(fig, "ch21_energy")


def sensors_map():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.0, 3.4))
    ax = world_axes(fig, borders=False)
    sites = [("Space Fence (Kwajalein)", 167.7, 9.4, BLUE, "r"), ("Cobra Dane (Alaska)", 174.1, 52.7, BLUE, "r"),
             ("Pituffik/Thule", -68.7, 76.5, BLUE, "r"), ("Fylingdales (UK)", -0.67, 54.4, BLUE, "r"),
             ("Clear (Alaska)", -149.2, 64.3, BLUE, "r"), ("Beale & Cape Cod", -121.4, 39.1, BLUE, "r"),
             ("GEODSS Socorro", -106.7, 33.8, ORANGE, "o"), ("GEODSS Maui", -156.3, 20.7, ORANGE, "o"),
             ("GEODSS Diego Garcia", 72.4, -7.4, ORANGE, "o"), ("GRAVES (France)", 5.5, 47.3, GREEN, "r"),
             ("TIRA (Germany)", 7.1, 50.6, GREEN, "r"), ("ESA/EU SST optical (Spain)", -16.5, 28.3, GREEN, "o"),
             ("LeoLabs (NZ)", 170.0, -45.0, VIOLET, "r"), ("LeoLabs (Texas)", -98.0, 31.0, VIOLET, "r"),
             ("LeoLabs (Costa Rica)", -84.0, 10.0, VIOLET, "r"), ("LeoLabs (Azores)", -25.6, 37.7, VIOLET, "r"),
             ("LeoLabs (W. Australia)", 116.0, -31.0, VIOLET, "r"), ("Okno (Tajikistan)", 69.2, 38.3, RED, "o"),
             ("Krona (Russia)", 41.3, 43.8, RED, "r"), ("ISON network (Russia)", 37.6, 55.8, RED, "o")]
    for n, lon, lat, c, kind in sites:
        ax.plot(lon, lat, "^" if kind == "r" else "o", color=c, ms=5, transform=ccrs.PlateCarree(), mec="white", mew=0.4)
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker="^", ls="", color=BLUE, label="US radars"),
         Line2D([], [], marker="o", ls="", color=ORANGE, label="US optical (GEODSS)"),
         Line2D([], [], marker="^", ls="", color=GREEN, label="European sensors"),
         Line2D([], [], marker="^", ls="", color=VIOLET, label="Commercial radars (LeoLabs)"),
         Line2D([], [], marker="o", ls="", color=RED, label="Russian sensors")]
    ax.legend(handles=h, fontsize=6.2, loc="lower left")
    note(ax, "Selected ground-based space-surveillance sensors (approximate locations, public information). ▲ radar, "
             "● optical.", xy=(1, -0.02))
    save(fig, "ch21_sensors")


def cascade():
    t = np.arange(2025, 2226)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    base = 1.0
    bau = base * np.exp((t - 2025) / 95)
    pmd = base * (1 + 0.25 * (1 - np.exp(-(t - 2025) / 60)) + 0.002 * (t - 2025))
    adr = base * (1 + 0.15 * (1 - np.exp(-(t - 2025) / 50))) * np.exp(-(t - 2025) / 600)
    noaction = base * np.exp((t - 2025) / 60)
    for y, c, n in [(noaction, RED, "No mitigation"), (bau, ORANGE, "Current compliance with disposal rules"),
                    (pmd, BLUE, "90 %+ post-mission disposal"), (adr, GREEN, "Disposal + active removal of ≈ 5–10 large "
                                                                           "objects/year")]:
        ax.plot(t, y, color=c, lw=1.8, label=n)
    ax.set_xlim(2025, 2225)
    ax.set_ylim(0.6, 8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Relative number of objects ≥ 10 cm in LEO")
    ax.legend(fontsize=6.4, loc="upper left")
    note(ax, "Schematic of the qualitative conclusions of long-term debris-environment models (e.g. NASA LEGEND, "
             "ESA DELTA, IADC studies).", xy=(1, -0.16))
    save(fig, "ch21_cascade")


def alt_inc():
    p = S["alt_inc"]
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    for t, sz, al in [("DEB", 2.5, 0.35), ("R/B", 4, 0.6), ("PAY", 2, 0.35)]:
        q = np.array([[a, i] for a, i, tt in p if tt == t])
        ax.scatter(q[:, 1], q[:, 0], s=sz, color=TCOL[t], alpha=al, lw=0, label=TNAME[t])
    ax.set_xlim(0, 145)
    ax.set_ylim(150, 2100)
    ax.set_xlabel("Inclination (°)")
    ax.set_ylabel("Mean altitude (km)")
    leg = ax.legend(fontsize=6.6, loc="upper right", markerscale=4)
    for t, x, y in [("Starlink 53°", 53, 330), ("sun-synchronous\nband (97–99°)", 99, 1550),
                    ("Fengyun-1C debris", 99, 980), ("OneWeb 1 200 km", 88, 1290)]:
        ax.text(x + 1.5, y, t, fontsize=6.2, color=INK)
    note(ax, "Every catalogued object below 2 100 km in October 2026 (CelesTrak SATCAT).", xy=(1, -0.15))
    save(fig, "ch21_altinc", raster=True)


def owners():
    o = S["owners"]
    names = list(o)
    lab = {"US": "USA", "CIS": "Russia / CIS", "PRC": "China", "UK": "United Kingdom", "FR": "France", "JPN": "Japan",
           "IND": "India", "TBD": "Unattributed", "ITSO": "Intelsat", "ESA": "ESA"}
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    y = np.arange(len(names))
    left = np.zeros(len(names))
    for t in ["PAY", "R/B", "DEB", "UNK"]:
        v = np.array([o[n][t] for n in names])
        ax.barh(y, v, left=left, color=TCOL[t], height=0.62, label=TNAME[t])
        left += v
    for yi, tot in zip(y, left):
        ax.text(tot + 120, yi, f"{int(tot):,}", va="center", fontsize=6.4)
    ax.set_yticks(y)
    ax.set_yticklabels([lab.get(n, n) for n in names], fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(0, 20500)
    ax.set_xlabel("Catalogued objects in orbit (October 2026)")
    ax.legend(fontsize=6.4, loc="lower right")
    ax.grid(axis="y", visible=False)
    note(ax, "By owner/country code in the CelesTrak SATCAT. UK and France totals are dominated by OneWeb and "
             "Ariane/Eutelsat objects.", xy=(1, -0.16))
    save(fig, "ch21_owners")


if __name__ == "__main__":
    fns = [population, density, fragmentations, reentries, lifetime, detectability, pc, encounter, impact_energy,
           sensors_map, cascade, alt_inc, owners]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
