"""Figures for Chapter 36 — Launch Vehicles of the World.

Most figures are computed from Jonathan McDowell's General Catalog of Artificial Space Objects (GCAT,
planet4589.org/space/gcat, CC-BY 4.0; raw launch.tsv in data/raw, updated 13 October 2026), counted exactly as in
Appendix E (all orbital launch attempts, launch codes O* and D*). Vehicle dimensions and payload capacities are
approximate published values (see notes/currency/ch36.md).
"""
import collections
import math
import re
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge  # noqa: F401
from matplotlib.lines import Line2D

import make_appendices as MA  # GCAT loader and the country grouping used by Appendix E

COUNTRIES = ["USA", "USSR/Russia", "China", "Europe", "Japan", "India", "Other"]
CCOL = {"USA": BLUE, "USSR/Russia": RED, "China": GOLD, "Europe": VIOLET, "Japan": GREEN, "India": ORANGE,
        "Other": GREY}
FOOT = "Data: GCAT (J. McDowell, CC-BY 4.0), launches to 13 Oct 2026."


# ---------------------------------------------------------------------------------------------- GCAT helpers
@lru_cache(None)
def launches():
    orgs = {o["Code"]: o for o in MA.load("orgs.tsv")}
    out = []
    for r in MA.load("launch.tsv"):
        code = r["LaunchCode"]
        if not code or code[0] not in "OD" or not r["Launch_Date"][:4].isdigit():
            continue
        if r["Agency"].startswith("RLAB"):
            g = "USA"
        else:
            o = orgs.get(r["Agency"].split("/")[0])
            st = o["StateCode"] if o else "?"
            g = MA.GROUPS.get(st)
            if not g:
                g = "Europe" if (st.startswith("I-") or st in ("F", "D", "I", "UK", "GB", "E", "S", "N")) else "Other"
        try:
            mass = float(r["OrbPay"] or 0)
        except ValueError:
            mass = 0.0
        y = int(r["Launch_Date"][:4])
        mon = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split().index(r["Launch_Date"][5:8]) + 1
        day = int(r["Launch_Date"][9:11].strip() or 1)
        out.append(dict(lv=r["LV_Type"].strip(), y=y, t=y + (mon - 1 + (day - 1) / 31) / 12, g=g, code=code,
                        fail=code[1:2] == "F", ok=code[1:2] == "S", pad=code[1:2] in ("A", "E"), mass=mass,
                        mission=r["Mission"]))
    return out


def ftext(fig, text, y=0.01, width=135):
    """Footnote wrapped to fit inside the figure; stores the space it needs for tight_layout."""
    import textwrap
    lines = textwrap.wrap(text, width)
    fig.text(0.99, y, "\n".join(lines), ha="right", va="bottom", fontsize=6.0, color=GREY, linespacing=1.25)
    fig._foot = (len(lines) * 0.105 + 0.06) / fig.get_size_inches()[1]


def finish(fig, name):
    fig.tight_layout(rect=(0, getattr(fig, "_foot", 0.04), 1, 1))
    save(fig, name)


# Coarse families for the timeline (label, regex on GCAT LV_Type, country)
TL_ROWS = [
    ("R-7: Sputnik, Vostok, Molniya, Soyuz", r"^(Sputnik|Vostok|Voskhod|Molniya|Polyot|Soyuz)", "USSR/Russia"),
    ("Kosmos, Tsiklon, Rokot, Dnepr", r"^(Kosmos|R-36O|Tsiklon|Rokot|Dnepr|Start|Strela|Volna|Shtil)", "USSR/Russia"),
    ("Proton", r"^(UR-500|Proton)", "USSR/Russia"),
    ("Zenit", r"^Zenit", "USSR/Russia"),
    ("N1 and Energia", r"^(N-1 11A52|Energiya)", "USSR/Russia"),
    ("Angara", r"^Angara", "USSR/Russia"),
    ("Thor, Delta to Delta II", r"^(Thor|Thorad|Delta [0-9]{4})", "USA"),
    ("Atlas to Atlas III", r"^Atlas(?! V )", "USA"),
    ("Titan", r"^(Titan|Commercial Titan)", "USA"),
    ("Scout, Pegasus, Minotaur", r"^(Scout|Blue Scout|Pegasus|Minotaur|Taurus|ARPA Taurus)", "USA"),
    ("Saturn I, IB, V", r"^(Saturn|Uprated Saturn)", "USA"),
    ("Space Shuttle", r"^Space Shuttle", "USA"),
    ("Delta IV, Atlas V, Vulcan", r"^(Delta 4|Atlas V |Vulcan)", "USA"),
    ("Falcon 9, Falcon Heavy", r"^Falcon (9|Heavy)", "USA"),
    ("Electron", r"^Electron", "USA"),
    ("SLS, New Glenn, Starship", r"^(SLS|New Glenn|Starship)", "USA"),
    ("Diamant, Europa", r"^(Diamant|Europa)", "Europe"),
    ("Ariane 1–4", r"^Ariane [1-4]", "Europe"),
    ("Ariane 5", r"^Ariane 5", "Europe"),
    ("Vega, Ariane 6, Spectrum", r"^(Vega|Ariane 6|Spectrum)", "Europe"),
    ("Long March 1–4", r"^Chang Zheng [1-4]", "China"),
    ("Long March 5–12", r"^Chang Zheng (5|6|7|8|10|11|12)", "China"),
    ("Chinese commercial", r"^(Kuaizhou|Gushenxing|Lijian|Zhuque|Yinli|Jielong|Shuang Quxian|Tianlong|Zhishenxing|OS-M)",
     "China"),
    ("Lambda, Mu, M-V, Epsilon", r"^(Lambda|Mu-|M-V|Epsilon)", "Japan"),
    ("N-I, N-II, H-I, H-II, H-IIA/B", r"^(N-1$|N-2|H-1|H-II)", "Japan"),
    ("H3", r"^H3", "Japan"),
    ("SLV-3, ASLV", r"^(SLV-3|ASLV)", "India"),
    ("PSLV", r"^PSLV", "India"),
    ("GSLV, LVM3", r"^(GSLV|LVM3)", "India"),
    ("Israel, Iran, Koreas, others", r".", "Other"),
]


def tl_row(lv, g):
    for i, (_, pat, cty) in enumerate(TL_ROWS[:-1]):
        if re.search(pat, lv):
            return i
    return len(TL_ROWS) - 1 if g == "Other" else None


# ---------------------------------------------------------------------------------------------- 1 timeline
def timeline():
    L = launches()
    n = len(TL_ROWS)
    cnt = np.zeros((n, 2027 - 1957))
    for r in L:
        i = tl_row(r["lv"], r["g"])
        if i is not None:
            cnt[i, r["y"] - 1957] += 1
    fig, ax = plt.subplots(figsize=(7.0, 4.7))
    vmax = math.log10(cnt.max() + 1)
    for i, (lab, _, cty) in enumerate(TL_ROWS):
        y = n - 1 - i
        for j in range(cnt.shape[1]):
            c = cnt[i, j]
            if c > 0:
                a = 0.18 + 0.82 * math.log10(c + 1) / vmax
                ax.add_patch(Rectangle((1957 + j, y - 0.36), 1.0, 0.72, fc=CCOL[cty], ec="none", alpha=a, zorder=2))
        tot = int(cnt[i].sum())
        ax.text(2027.6, y, f"{tot:,}".replace(",", " "), va="center", ha="left", fontsize=6.4, color=INK)
    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] for r in TL_ROWS][::-1], fontsize=6.6)
    for tl, (_, _, cty) in zip(ax.get_yticklabels(), TL_ROWS[::-1]):
        tl.set_color(CCOL[cty] if cty != "Other" else "#555555")
    ax.set_xlim(1957, 2027)
    ax.set_ylim(-0.7, n - 0.3)
    ax.set_xticks(range(1960, 2030, 10))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color="#E2E7EC", lw=0.6)
    ax.tick_params(axis="y", length=0)
    ax.text(2027.6, n - 0.2, "Total", fontsize=6.4, ha="left", va="bottom", weight="bold", clip_on=False)
    # milestones
    for x, t in [(1957.76, "Sputnik"), (1969.54, "Apollo 11"), (1981.28, "first Shuttle"), (2015.97,
                                                                                               "first booster landing")]:
        ax.axvline(x, color=GREY, lw=0.6, ls=":", zorder=1)
    # intensity key
    ax.add_patch(Rectangle((1957.6, -0.55), 15.6, 2.95, fc="white", ec="#C9D2DA", lw=0.6, zorder=3))
    ax.text(1965.4, 1.85, "Launches in a year", ha="center", va="center", fontsize=6.2, zorder=4)
    for k, c in enumerate([1, 3, 10, 30, 100]):
        a = 0.18 + 0.82 * math.log10(c + 1) / vmax
        ax.add_patch(Rectangle((1958.6 + k * 2.8, 0.45), 2.2, 0.75, fc=NAVY, alpha=a, ec="none", zorder=4))
        ax.text(1959.7 + k * 2.8, 0.0, str(c), ha="center", va="center", fontsize=6.0, zorder=4)
    for sp in ("left",):
        ax.spines[sp].set_visible(False)
    ftext(fig, "Each cell is one year; shading shows the number of orbital launch attempts (log scale). Dotted lines: "
               "Sputnik 1957, Apollo 11 1969, first Shuttle 1981, first Falcon 9 landing 2015. " + FOOT)
    finish(fig, "ch36_timeline")


# ---------------------------------------------------------------------------------------------- 2 country shares
def countries():
    L = launches()
    years = np.arange(1957, 2027)
    by = {c: np.zeros(len(years)) for c in COUNTRIES}
    fams = collections.defaultdict(set)
    for r in L:
        by[r["g"]][r["y"] - 1957] += 1
        fams[(r["g"], r["y"])].add(MA.family(r["lv"]))
    tot = sum(by.values())
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw=dict(width_ratios=[1.15, 1]))
    share = [100 * by[c] / tot for c in COUNTRIES]
    a1.stackplot(years + 0.5, share, colors=[CCOL[c] for c in COUNTRIES], alpha=0.9, lw=0)
    a1.set_xlim(1957, 2027)
    a1.set_ylim(0, 100)
    a1.set_ylabel("Share of world launches (%)")
    a1.set_title("(a) Who launches", fontsize=8.6, loc="left")
    a1.grid(False)
    for c, x, y in [("USA", 1962, 70), ("USSR/Russia", 1977, 45), ("China", 2019.5, 40), ("Europe", 1998, 12.5),
                    ("USA", 2022, 75)]:
        a1.text(x, y, c if c != "USSR/Russia" else "USSR / Russia", fontsize=6.6, color="white", ha="center",
                weight="bold")
    a1.text(2008.5, 5.0, "Japan, India,\nothers", fontsize=5.9, color="white", ha="center", va="bottom")
    for c in COUNTRIES:
        nf = [len(fams.get((c, y), ())) for y in years]
        a2.plot(years + 0.5, nf, color=CCOL[c], lw=1.1, label=c if c != "USSR/Russia" else "USSR / Russia")
    a2.set_xlim(1957, 2027)
    a2.set_ylim(0, 27)
    a2.set_ylabel("Vehicle families flown per year")
    a2.set_title("(b) How many different rockets", fontsize=8.6, loc="left")
    a2.legend(fontsize=6.0, ncol=4, loc="upper left", handlelength=1.2, columnspacing=0.6)
    ftext(fig, "Country of the launch provider (Rocket Lab counted as USA). A family groups the variants of one "
               "vehicle (Long March split by number). 2026 to 13 Oct. " + FOOT)
    finish(fig, "ch36_countries")


# ---------------------------------------------------------------------------------------------- 3 families 2025/26
def fam_display(lv):
    pairs = [(r"^Falcon 9", "Falcon 9", "USA"), (r"^Falcon Heavy", "Falcon Heavy", "USA"),
             (r"^Starship", "Starship", "USA"), (r"^Electron", "Electron", "USA"),
             (r"^Atlas V", "Atlas V", "USA"), (r"^Vulcan", "Vulcan", "USA"), (r"^New Glenn", "New Glenn", "USA"),
             (r"^(Minotaur|Pegasus|Firefly|SLS|HASTE)", "Other US", "USA"),
             (r"^Soyuz", "Soyuz-2", "USSR/Russia"), (r"^(Angara|Proton)", "Angara, Proton", "USSR/Russia"),
             (r"^Ariane 6", "Ariane 6", "Europe"), (r"^(Vega|Spectrum)", "Vega C, Spectrum", "Europe"),
             (r"^Chang Zheng (2)", "Long March 2", "China"), (r"^Chang Zheng 3", "Long March 3", "China"),
             (r"^Chang Zheng 4", "Long March 4", "China"), (r"^Chang Zheng (5)", "Long March 5", "China"),
             (r"^Chang Zheng 6", "Long March 6", "China"), (r"^Chang Zheng 7", "Long March 7", "China"),
             (r"^Chang Zheng 8", "Long March 8", "China"), (r"^Chang Zheng 1[02]", "Long March 10, 12", "China"),
             (r"^Chang Zheng 11", "Long March 11", "China"),
             (r"^Gushenxing|^Zhishenxing", "Ceres, Pallas", "China"), (r"^Lijian", "Kinetica", "China"),
             (r"^(Jielong|Kuaizhou)", "Jielong, Kuaizhou", "China"),
             (r"^(Zhuque|Tianlong|Yinli|Shuang)", "Zhuque, Gravity, others", "China"),
             (r"^(H3|H-IIA|Kairos)", "H3, H-IIA, Kairos", "Japan"),
             (r"^(PSLV|GSLV|LVM3|Vikram)", "PSLV, GSLV, LVM3, Vikram", "India")]
    for pat, name, c in pairs:
        if re.search(pat, lv):
            return name, c
    return "Others (Nuri, Shavit, Iran, ...)", "Other"


def families():
    L = launches()
    c25 = collections.Counter()
    c26 = collections.Counter()
    f25 = collections.Counter()
    f26 = collections.Counter()
    cty = {}
    for r in L:
        if r["y"] in (2025, 2026):
            name, c = fam_display(r["lv"])
            cty[name] = c
            (c25 if r["y"] == 2025 else c26)[name] += 1
            (f25 if r["y"] == 2025 else f26)[name] += r["fail"]
    names = sorted(cty, key=lambda k: (-(c25[k] + 0.6 * c26[k])))
    fig, ax = plt.subplots(figsize=(7.0, 4.9))
    y = np.arange(len(names))
    ax.barh(y, [c25[k] for k in names], height=0.62, color=[CCOL[cty[k]] for k in names], zorder=2)
    ax.scatter([c26[k] for k in names], y, marker="D", s=13, facecolor="white",
               edgecolor=[CCOL[cty[k]] if cty[k] != "Other" else INK for k in names], lw=1.0, zorder=3)
    X1, X2 = 330, 520
    ax.text(X1, -1.2, "2025", ha="right", fontsize=6.6, weight="bold", va="center")
    ax.text(X2, -1.2, "2026*", ha="right", fontsize=6.6, weight="bold", va="center")
    for yi, k in zip(y, names):
        ax.text(X1, yi, f"{c25[k]}" + (f" ({f25[k]} F)" if f25[k] else ""), ha="right", va="center", fontsize=6.3)
        ax.text(X2, yi, f"{c26[k]}" + (f" ({f26[k]} F)" if f26[k] else ""), ha="right", va="center", fontsize=6.3,
                color="#444444")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=6.7)
    for tl, k in zip(ax.get_yticklabels(), names):
        tl.set_color(CCOL[cty[k]] if cty[k] != "Other" else "#555555")
    ax.set_ylim(len(names) - 0.4, -1.8)
    ax.set_xscale("symlog", linthresh=10, linscale=0.8)
    ax.set_xticks([0, 2, 5, 10, 20, 50, 100, 200])
    ax.set_xticklabels(["0", "2", "5", "10", "20", "50", "100", "200"])
    ax.set_xlim(0, 540)
    ax.spines["bottom"].set_bounds(0, 200)
    ax.set_xlabel("Orbital launch attempts (linear to 10, logarithmic above)", x=0.36)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=False)
    for xv in (2, 5, 10, 20, 50, 100, 200):
        ax.plot([xv, xv], [len(names) - 0.4, -0.6], color="#E2E7EC", lw=0.6, zorder=0)
    leg = [Rectangle((0, 0), 1, 1, fc=GREY), Line2D([], [], marker="D", ls="", mfc="white", mec=GREY, ms=4)]
    ax.legend(leg, ["2025 (full year; 330 attempts)", "2026 to 13 October (244 attempts)"], loc="lower right",
              bbox_to_anchor=(0.6, 0.0), fontsize=6.6)
    ftext(fig, "Colour = country of the launch provider (blue USA, red Russia, gold China, violet Europe, green Japan, "
               "orange India). F = failures. *To 13 Oct. " + FOOT)
    finish(fig, "ch36_families")


# ---------------------------------------------------------------------------------------------- 4 payload mass
def mass():
    L = launches()
    years = np.arange(1957, 2027)
    by = {c: np.zeros(len(years)) for c in COUNTRIES}
    ship = np.zeros(len(years))
    sl = np.zeros(len(years))
    for r in L:
        if not r["ok"]:
            continue
        i = r["y"] - 1957
        if r["lv"].startswith(("Starship", "Space Shuttle", "Energiya/Buran")):
            ship[i] += r["mass"]
        else:
            by[r["g"]][i] += r["mass"]
            if "Starlink" in r["mission"]:
                sl[i] += r["mass"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw=dict(width_ratios=[1.25, 1]))
    m = years < 2026
    a1.stackplot(years[m] + 0.5, [by[c][m] for c in COUNTRIES], colors=[CCOL[c] for c in COUNTRIES], lw=0,
                 alpha=0.9)
    base = sum(by[c] for c in COUNTRIES)
    a1.fill_between(years[m] + 0.5, base[m], base[m] + ship[m], fc="white", ec=GREY, hatch="////", lw=0.4)
    a1.set_xlim(1957, 2026)
    a1.set_ylim(0, 3500)
    a1.set_ylabel("Mass placed in orbit (t per year)")
    a1.set_title("(a) Payload mass by launching country", fontsize=8.6, loc="left")
    a1.grid(False)
    a1.text(1969.5, 640, "Apollo", fontsize=6.3, ha="center")
    a1.annotate("Shuttle orbiters\n(hatched)", xy=(1992, 700), xytext=(1990, 1500), fontsize=6.3, ha="center",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.annotate("Starship test\nships (hatched)", xy=(2024.6, 2560), xytext=(2013.5, 2650), fontsize=6.3,
                ha="center", va="center", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    hand = [Rectangle((0, 0), 1, 1, fc=CCOL[c]) for c in COUNTRIES[:4]]
    a1.legend(hand, ["USA", "USSR / Russia", "China", "Europe"], fontsize=6.2, loc="upper left",
              bbox_to_anchor=(0.0, 0.84))
    # (b) recent years by category
    yy = np.arange(2015, 2027)
    idx = yy - 1957
    other_us = by["USA"][idx] - sl[idx]
    cats = [(sl[idx], "Falcon 9: Starlink", BLUE), (other_us, "Other US launches", SKY),
            (by["China"][idx], "China", GOLD),
            (sum(by[c][idx] for c in ("USSR/Russia", "Europe", "Japan", "India", "Other")), "Rest of world", GREY)]
    bottom = np.zeros(len(yy))
    for v, lab, col in cats:
        a2.bar(yy, v, bottom=bottom, color=col, width=0.75, label=lab, zorder=2)
        bottom += v
    a2.bar(yy, ship[idx], bottom=bottom, color="white", ec=GREY, hatch="////", lw=0.4, width=0.75,
           label="Starship test ships", zorder=2)
    a2.set_title("(b) 2015–2026, by user", fontsize=8.6, loc="left")
    a2.set_ylabel("t per year")
    a2.set_xticks([2015, 2018, 2021, 2024, 2026])
    a2.set_xticklabels(["2015", "2018", "2021", "2024", "2026*"])
    a2.legend(fontsize=6.0, loc="upper left")
    a2.grid(axis="x", visible=False)
    a2.set_ylim(0, 3500)
    ftext(fig, "Sum of GCAT payload masses on successful launches. GCAT counts reusable orbiters (Shuttle, Buran, about "
               "100 t each) and Starship test ships (120 t each) as payload: shown hatched. *2026 to 13 Oct. " + FOOT)
    finish(fig, "ch36_mass")


# ---------------------------------------------------------------------------------------------- 5 reliability
# Capacity class by GCAT LV_Type (approximate maximum payload to low Earth orbit)
CLASS_RULES = [
    ("Super-heavy", r"^(Saturn V|N-1 11A52|Energiya|SLS|Starship|Falcon Heavy)"),
    ("Heavy", r"^(Proton|UR-500|Titan 40|Space Shuttle|Ariane 5|Ariane 64|Delta 4H|Angara A5|Chang Zheng 5|Vulcan|"
              r"New Glenn|Saturn IB|Uprated Saturn)"),
    ("Medium", r"^(Falcon 9|Atlas V|Atlas I|Atlas 3|Atlas G|Atlas H|Atlas SLV-3[CD]|Atlas Centaur|Delta [2-8]|"
               r"Delta 4M|Titan|Commercial Titan|Saturn I|Soyuz|Vostok|Voskhod|Molniya|Polyot|Tsiklon|R-36O|Zenit|"
               r"Chang Zheng (2|3|4|6A|6C|7|8|10|12)|Ariane|Angara-1|H-II|H3|N-2|PSLV|GSLV|LVM3|Dnepr|Antares|"
               r"Feng Bao|Lijian-2|Zhuque-[23]|Tianlong-3|Yinli|Kosmos 11K65$|Atlas Agena|Atlas SLV-3 Agena|"
               r"Atlas SLV-3A|Atlas Burner|Atlas E|Atlas F|Atlas D|Thorad|Gushenxing-2|Nuri|Delta 1|Delta 0)"),
    ("Small", r"."),
]


def lv_class(lv):
    for c, pat in CLASS_RULES:
        if re.search(pat, lv):
            return c
    return "Small"


def jeffreys(k, n, q=(0.05, 0.95)):
    from scipy.stats import beta
    return [beta.ppf(x, k + 0.5, n - k + 0.5) for x in q]


SMALL_NEW = [  # small launchers first flown since 2000 (GCAT type regex, label, still flying in 2026?)
    (r"^Electron", "Electron (US/NZ)", True), (r"^Kuaizhou-1A", "Kuaizhou-1A (China)", True),
    (r"^Gushenxing 1", "Ceres-1 (China)", True), (r"^Chang Zheng 11", "Long March 11 (China)", True),
    (r"^Lijian-1", "Kinetica-1 (China)", True), (r"^Jielong-3", "Jielong-3 (China)", True),
    (r"^Minotaur I$", "Minotaur I (US)", False), (r"^Shuang Quxian", "Hyperbola-1 (China)", True),
    (r"^Firefly Alpha", "Firefly Alpha (US)", True), (r"^Kuaizhou-11", "Kuaizhou-11 (China)", True),
    (r"^Astra", "Astra Rocket 3 (US)", False), (r"^LauncherOne", "LauncherOne (US)", False),
    (r"^Safir", "Safir (Iran)", False), (r"^Simorgh", "Simorgh (Iran)", True), (r"^Epsilon", "Epsilon (Japan)", False),
    (r"^Falcon 1", "Falcon 1 (US)", False), (r"^SSLV", "SSLV (India)", True), (r"^Qaem", "Qaem-100 (Iran)", True),
    (r"^Kairos", "Kairos (Japan)", True), (r"^Naro", "Naro-1 (S. Korea)", False), (r"^Spectrum", "Spectrum (Germany)", True),
    (r"^Zhuque-1|^Zhuque-2$", "Zhuque-1/-2 (China)", False), (r"^Terran 1|^RS1|^Tianlong-2|^OS-M1|^Jielong-1",
                                                             "Terran 1, RS1, Tianlong-2, OS-M1", False),
    (r"^Eris|^HANBIT|^Vikram", "Eris, Hanbit-Nano, Vikram-1", True),
]


def reliability():
    L = [r for r in launches() if not r["pad"]]
    eras = [(1957, 1979), (1980, 1999), (2000, 2014), (2015, 2026)]
    classes = ["Small", "Medium", "Heavy", "Super-heavy"]
    ccol = {"Small": ORANGE, "Medium": BLUE, "Heavy": VIOLET, "Super-heavy": RED}
    N = collections.Counter()
    F = collections.Counter()
    for r in L:
        c = lv_class(r["lv"])
        for e in eras:
            if e[0] <= r["y"] <= e[1]:
                N[(c, e)] += 1
                F[(c, e)] += r["fail"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.5), gridspec_kw=dict(width_ratios=[1, 1.08]))
    w = 0.2
    seen = set()
    for k, c in enumerate(classes):
        for j, e in enumerate(eras):
            n, f = N[(c, e)], F[(c, e)]
            if n == 0:
                continue
            x = j + (k - 1.5) * w
            rate = 100 * f / n
            lo, hi = jeffreys(f, n)
            a1.bar(x, rate, width=w * 0.92, color=ccol[c], zorder=2, label=c if c not in seen else None)
            seen.add(c)
            a1.plot([x, x], [100 * lo, 100 * hi], color=INK, lw=0.6, zorder=3)
            a1.text(x, min(100 * hi, 48) + 1.0, str(n), ha="center", va="bottom", fontsize=5.0, color="#444444",
                    rotation=90)
    a1.set_xticks(range(len(eras)))
    a1.set_xticklabels([f"{a}–{str(b)[2:]}" for a, b in eras], fontsize=7)
    a1.set_ylabel("Launches that failed (%)")
    a1.set_ylim(0, 60)
    a1.set_title("(a) Failure rate by class and era", fontsize=8.6, loc="left")
    h, lab = a1.get_legend_handles_labels()
    h = [h[lab.index(c)] for c in classes]
    a1.legend(h, ["Small (< 2 t)", "Medium (2–20 t)", "Heavy (20–50 t)", "Super-heavy (> 50 t)"], fontsize=6.0,
              loc="upper right", title="LEO capacity", title_fontsize=6.2)
    a1.grid(axis="x", visible=False)
    # (b) shake-out of small launchers
    rows = []
    for pat, lab, alive in SMALL_NEW:
        sel = [r for r in L if re.search(pat, r["lv"]) and r["y"] >= 2000]
        if sel:
            rows.append((lab, sum(1 for r in sel if not r["fail"]), sum(r["fail"] for r in sel), alive))
    rows.sort(key=lambda t: -(t[1] + t[2]))
    y = np.arange(len(rows))
    a2.barh(y, [r[1] for r in rows], color=[GREEN if r[3] else "#9DB8A6" for r in rows], height=0.7, zorder=2)
    a2.barh(y, [r[2] for r in rows], left=[r[1] for r in rows], color=RED, height=0.7, zorder=2)
    for yi, r in zip(y, rows):
        a2.text(r[1] + r[2] + 1, yi, f"{r[1] + r[2]}" + (f" ({r[2]} F)" if r[2] else ""), va="center", fontsize=5.8)
    a2.set_yticks(y)
    a2.set_yticklabels([r[0] for r in rows], fontsize=5.9)
    for tl, r in zip(a2.get_yticklabels(), rows):
        tl.set_color(INK if r[3] else "#8A8F94")
    a2.invert_yaxis()
    a2.set_xscale("symlog", linthresh=10, linscale=0.7)
    a2.set_xticks([0, 5, 10, 20, 50, 100])
    a2.set_xticklabels(["0", "5", "10", "20", "50", "100"])
    a2.set_xlim(0, 160)
    a2.grid(axis="y", visible=False)
    a2.set_title("(b) Small launchers since 2000", fontsize=8.6, loc="left")
    a2.set_xlabel("Orbital attempts (successes green, failures red)", fontsize=7)
    ftext(fig, "(a) Classes by approximate maximum LEO payload (Falcon 9 as medium); bars: failed share; whiskers: 90 % "
               "Jeffreys interval; numbers: attempts; pad aborts and explosions excluded. (b) Grey labels: retired or company closed. " + FOOT)
    finish(fig, "ch36_reliability")


# ---------------------------------------------------------------------------------------------- 6 capability vs year
CAP = [  # name, first flight, max LEO payload (t), country, flying in 2026 (None = planned), label (x, y, ha, leader)
    ("Sputnik (R-7)", 1957, 1.3, "USSR/Russia", False, (1958.2, 1.3, "left", 0)),
    ("Vostok", 1960, 4.7, "USSR/Russia", False, (1959.3, 4.7, "right", 0)),
    ("Titan IIIC", 1965, 13.1, "USA", False, (1964.3, 13.1, "right", 0)),
    ("Saturn IB", 1966, 21.0, "USA", False, (1965.3, 21.0, "right", 0)),
    ("Proton-K", 1967, 19.8, "USSR/Russia", False, (1967.8, 17.0, "left", 0)),
    ("Saturn V", 1967, 140.0, "USA", False, (1967.8, 140.0, "left", 0)),
    ("N1", 1969, 95.0, "USSR/Russia", False, (1969.8, 86.0, "left", 0)),
    ("Space Shuttle", 1981, 27.5, "USA", False, (1981.8, 31.0, "left", 0)),
    ("Zenit-2", 1985, 13.7, "USSR/Russia", False, (1985.8, 12.0, "left", 0)),
    ("Energia", 1987, 100.0, "USSR/Russia", False, (1987.8, 100.0, "left", 0)),
    ("Ariane 44L", 1988, 7.6, "Europe", False, (1987.3, 7.6, "right", 0)),
    ("Delta II", 1989, 6.1, "USA", False, (1989.8, 5.5, "left", 0)),
    ("Titan IV", 1989, 21.7, "USA", False, (1988.2, 21.7, "right", 0)),
    ("Pegasus XL", 1994, 0.45, "USA", True, (1994.8, 0.45, "left", 0)),
    ("H-II", 1994, 10.0, "Japan", False, (1993.3, 10.0, "right", 0)),
    ("Ariane 5", 1996, 21.0, "Europe", False, (1995.2, 24.5, "right", 0)),
    ("Long March 3B", 1996, 11.5, "China", True, (1996.8, 11.5, "left", 0)),
    ("Proton-M", 2001, 23.0, "USSR/Russia", True, (1999.8, 31.5, "center", 1)),
    ("Atlas V", 2002, 18.8, "USA", True, (2002.8, 16.2, "left", 0)),
    ("Delta IV Heavy", 2004, 28.8, "USA", False, (2003.0, 44.0, "center", 1)),
    ("Soyuz-2.1b", 2006, 8.2, "USSR/Russia", True, (2005.2, 8.2, "right", 0)),
    ("PSLV-XL", 2008, 3.8, "India", True, (2008.0, 3.05, "center", 0)),
    ("GSLV Mk II", 2010, 6.0, "India", True, (2010.8, 6.0, "left", 0)),
    ("Falcon 9", 2010, 22.8, "USA", True, (2010.5, 35.0, "center", 1)),
    ("Angara A5", 2014, 24.5, "USSR/Russia", True, (2013.6, 18.0, "center", 1)),
    ("Long March 5", 2016, 25.0, "China", True, (2017.8, 33.0, "center", 1)),
    ("Electron", 2017, 0.3, "USA", True, (2016.2, 0.3, "right", 0)),
    ("LVM3", 2017, 10.0, "India", True, (2017.8, 8.7, "left", 0)),
    ("Falcon Heavy", 2018, 63.8, "USA", True, (2017.2, 63.8, "right", 0)),
    ("SLS Block 1", 2022, 95.0, "USA", True, (2021.2, 95.0, "right", 0)),
    ("Vega C", 2022, 3.3, "Europe", True, (2022.8, 3.3, "left", 0)),
    ("Starship (V3)", 2023, 100.0, "USA", True, (2023.8, 112.0, "left", 0)),
    ("Long March 12", 2024, 12.0, "China", True, (2023.2, 12.6, "right", 0)),
    ("Ariane 64", 2024, 21.6, "Europe", True, (2024.8, 21.0, "left", 0)),
    ("Vulcan (VC6)", 2024, 27.2, "USA", True, (2024.8, 28.5, "left", 0)),
    ("New Glenn", 2025, 45.0, "USA", True, (2025.8, 45.0, "left", 0)),
    ("Spectrum", 2025, 1.0, "Europe", True, (2025.8, 1.0, "left", 0)),
    ("Kinetica-2", 2026, 12.0, "China", True, (2026.8, 11.4, "left", 0)),
    ("Long March 10B", 2026, 16.0, "China", True, (2026.8, 15.8, "left", 0)),
    ("Vikram-1", 2026, 0.35, "India", True, (2026.8, 0.35, "left", 0)),
    ("Long March 10 (2027)", 2027, 70.0, "China", None, (2026.2, 72.0, "right", 0)),
]


def capability():
    fig, ax = plt.subplots(figsize=(7.0, 4.1))
    for name, y, m, c, live, (tx, ty, ha, lead) in CAP:
        if live is None:
            ax.scatter(y, m, s=26, facecolor="white", edgecolor=CCOL[c], lw=1.0, linestyle="--", zorder=3)
        else:
            ax.scatter(y, m, s=26, facecolor=CCOL[c] if live else "white", edgecolor=CCOL[c], lw=1.0, zorder=3)
        ax.text(tx, ty, name, fontsize=6.0, ha=ha, va="center", color=CCOL[c], zorder=4)
        if lead:
            ax.plot([y, tx], [m, ty * 0.93], color=CCOL[c], lw=0.5, zorder=2)
    ax.set_yscale("log")
    ax.set_ylim(0.2, 230)
    ax.set_xlim(1953, 2034)
    ax.set_yticks([0.3, 1, 3, 10, 30, 100])
    ax.set_yticklabels(["0.3", "1", "3", "10", "30", "100"])
    ax.yaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_ylabel("Maximum payload to low Earth orbit (t)")
    ax.set_xlabel("Year of first launch")
    for lo, hi, lab in [(2, 20, "medium"), (20, 50, "heavy"), (50, 230, "super-heavy")]:
        ax.axhspan(lo, hi, color="#F2F5F8" if lab != "heavy" else "#E9EEF3", zorder=0)
        ax.text(1953.6, math.sqrt(lo * hi) if hi < 200 else 110, lab, fontsize=6.2, color=GREY, va="center",
                rotation=90)
    ax.text(1953.6, 0.62, "small", fontsize=6.2, color=GREY, va="center", rotation=90)
    hand = [Line2D([], [], marker="o", ls="", mfc=CCOL[c], mec=CCOL[c], ms=5) for c in COUNTRIES[:6]]
    hand += [Line2D([], [], marker="o", ls="", mfc="white", mec=GREY, ms=5)]
    ax.legend(hand, ["USA", "USSR / Russia", "China", "Europe", "Japan", "India", "retired / planned"], fontsize=6.0,
              loc="lower left", bbox_to_anchor=(0.1, 0.0), ncol=4)
    ax.grid(axis="x", visible=False)
    ftext(fig, "Approximate published maximum LEO payloads (expendable configuration, low inclination; definitions "
               "vary between sources). Filled: flying in 2026.")
    finish(fig, "ch36_capability")


# ---------------------------------------------------------------------------------------------- 7 silhouettes
SIL = [  # name, height (m), core diameter (m), booster (n, diameter, height), country, fairing frac, note
    ("Saturn V", 110.6, 10.1, (0, 0, 0), "USA", 0.0, "1967–73"),
    ("Space\nShuttle", 56.1, 8.4, (2, 3.7, 45.5), "USA", 0.0, "1981–2011"),
    ("Energia", 58.7, 7.75, (4, 3.9, 39.5), "USSR/Russia", 0.0, "1987–88"),
    ("SLS\nBlock 1", 98.0, 8.4, (2, 3.7, 54.0), "USA", 0.0, ""),
    ("Starship\nV3", 124.4, 9.0, (0, 0, 0), "USA", 0.0, ""),
    ("New\nGlenn", 98.0, 7.0, (0, 0, 0), "USA", 0.0, ""),
    ("Long\nMarch 10", 92.5, 5.0, (2, 5.0, 67.0), "China", 0.0, "2027"),
    ("Falcon\nHeavy", 70.0, 3.7, (2, 3.7, 44.0), "USA", 0.0, ""),
    ("Falcon 9", 70.0, 3.7, (0, 0, 0), "USA", 0.0, ""),
    ("Vulcan", 61.6, 5.4, (2, 1.6, 22.0), "USA", 0.0, ""),
    ("Ariane 64", 63.0, 5.4, (2, 3.4, 13.5), "Europe", 0.0, ""),
    ("H3-24", 63.0, 5.2, (2, 2.5, 15.0), "Japan", 0.0, ""),
    ("Long\nMarch 5", 57.0, 5.0, (2, 3.35, 27.6), "China", 0.0, ""),
    ("Angara\nA5", 55.4, 2.9, (2, 2.9, 25.0), "USSR/Russia", 0.0, ""),
    ("Soyuz-2", 46.3, 2.95, (2, 2.68, 19.6), "USSR/Russia", 0.0, ""),
    ("LVM3", 43.4, 4.0, (2, 3.2, 26.0), "India", 0.0, ""),
    ("Electron", 18.0, 1.2, (0, 0, 0), "USA", 0.0, ""),
]


def _rocket(ax, x, H, D, boost, col, shuttle=False):
    nose = min(0.12 * H, 2.2 * D)
    body = H - nose
    ax.add_patch(Rectangle((x - D / 2, 0), D, body, fc=col, ec=INK, lw=0.4, zorder=3))
    ax.add_patch(Polygon([(x - D / 2, body), (x + D / 2, body), (x + D * 0.12, H - 0.15 * nose), (x, H),
                          (x - D * 0.12, H - 0.15 * nose)], closed=True, fc="white" if not shuttle else col, ec=INK,
                         lw=0.4, zorder=3))
    n, d, h = boost
    sides = (-1, 1) if not shuttle else (-1,)
    if n:
        bn = min(0.14 * h, 2.4 * d)
        for s in sides:
            bx = x + s * (D / 2 + d / 2)
            ax.add_patch(Rectangle((bx - d / 2, 0), d, h - bn, fc=col, ec=INK, lw=0.4, alpha=0.75, zorder=2))
            ax.add_patch(Polygon([(bx - d / 2, h - bn), (bx + d / 2, h - bn), (bx, h)], closed=True, fc=col, ec=INK,
                                 lw=0.4, alpha=0.75, zorder=2))
    if shuttle:   # orbiter (side view) attached to the external tank
        ox = x + D / 2
        ax.add_patch(Polygon([(ox, 3.0), (ox + 5.5, 3.0), (ox + 5.5, 30.0), (ox + 2.5, 40.0), (ox, 37.0)],
                             closed=True, fc="white", ec=INK, lw=0.4, zorder=4))
        ax.add_patch(Polygon([(ox + 5.5, 3.0), (ox + 5.5, 11.0), (ox + 9.0, 3.5)], closed=True, fc="white", ec=INK,
                             lw=0.4, zorder=4))


def silhouettes():
    fig, ax = plt.subplots(figsize=(7.0, 3.7))
    slot = 15.5
    for k, (name, H, D, boost, c, _, note_) in enumerate(SIL):
        x = slot * (k + 0.5) + (2.0 if k > 0 else 0) + (7.0 if k > 1 else 0)
        planned = note_ == "2027"
        col = CCOL[c] if not planned else "#EAD9A0"
        _rocket(ax, x, H, D, boost, col, shuttle="Shuttle" in name)
        ax.text(x, H + 2.0, f"{H:.0f} m", ha="center", va="bottom", fontsize=5.9)
        ax.text(x, -3.0, name, ha="center", va="top", fontsize=5.9, color=CCOL[c], linespacing=1.05)
        if note_:
            ax.text(x, -14.0, note_ if not planned else "planned 2027", ha="center", va="top", fontsize=5.2,
                    color=GREY)
    xmax = slot * len(SIL) + 10
    ax.plot([0, xmax], [0, 0], color=INK, lw=0.6)
    ax.set_xlim(-6, xmax + 1)
    ax.set_ylim(-19, 134)
    ax.set_aspect("equal")
    for yy in (25, 50, 75, 100, 125):
        ax.plot([0, xmax], [yy, yy], color="#E3E8ED", lw=0.5, zorder=0)
        ax.text(-1.5, yy, f"{yy}", ha="right", va="center", fontsize=5.8, color=GREY)
    ax.text(-1.5, 131, "m", ha="right", va="center", fontsize=5.8, color=GREY)
    ax.axis("off")
    ftext(fig, "Heights and diameters to a common scale (simplified outlines; side boosters shown in pairs). Grey dates: "
               "retired or planned vehicles.")
    finish(fig, "ch36_silhouettes")


# ---------------------------------------------------------------------------------------------- 8 cadence
CAD = [(r"^Falcon 9", "Falcon 9", BLUE), (r"^Soyuz-U", "Soyuz-U (1973–2017)", RED),
       (r"^Proton", "Proton (all)", "#E07A86"), (r"^Space Shuttle", "Space Shuttle", NAVY),
       (r"^Atlas V ", "Atlas V", SKY), (r"^Ariane 5", "Ariane 5", VIOLET), (r"^Chang Zheng 2D", "Long March 2D", GOLD),
       (r"^Chang Zheng 3B", "Long March 3B", "#9C7A14"), (r"^Electron", "Electron", "#2B8C8C"),
       (r"^PSLV", "PSLV", ORANGE), (r"^H-IIA", "H-IIA", GREEN)]


def cadence():
    L = [r for r in launches() if not r["pad"]]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.2), gridspec_kw=dict(width_ratios=[1.2, 1]))
    for pat, lab, col in CAD:
        ts = sorted(r["t"] for r in L if re.search(pat, r["lv"]))
        t0 = ts[0]
        a1.step([t - t0 for t in ts], np.arange(1, len(ts) + 1), where="post", color=col, lw=1.2 if lab != "Falcon 9"
                else 2.2, label=f"{lab}: {len(ts)}")
    a1.set_yscale("log")
    a1.set_xlim(0, 58)
    a1.set_ylim(1, 1200)
    a1.set_xlabel("Years since first launch")
    a1.set_ylabel("Cumulative orbital launches")
    a1.set_title("(a) Building a launch record", fontsize=8.6, loc="left")
    a1.set_yticks([1, 10, 100, 1000])
    a1.set_yticklabels(["1", "10", "100", "1 000"])
    a1.legend(fontsize=5.6, loc="lower right", ncol=1, handlelength=1.2, labelspacing=0.25)
    # (b) Falcon 9 launches per year and median interval
    years = np.arange(2010, 2027)
    f9 = collections.Counter(r["y"] for r in L if r["lv"] == "Falcon 9")
    vals = [f9.get(y, 0) for y in years]
    cols = [BLUE if y < 2026 else SKY for y in years]
    a2.bar(years, vals, color=cols, width=0.75, zorder=2)
    for y, v in zip(years, vals):
        if v >= 20:
            a2.text(y, v + 3, f"{v}", ha="center", fontsize=5.8)
    a2.set_title("(b) Falcon 9 launches per year", fontsize=8.6, loc="left")
    a2.set_xticks([2010, 2014, 2018, 2022, 2026])
    a2.set_xticklabels(["2010", "2014", "2018", "2022", "2026*"])
    a2.grid(axis="x", visible=False)
    ts = sorted(r["t"] for r in L if r["lv"] == "Falcon 9" and r["y"] == 2025)
    gap = np.median(np.diff(ts)) * 365.25
    a2.text(2011.0, 150, f"2025: 165 launches,\nmedian interval {gap:.1f} days", fontsize=6.4, va="top")
    a2.set_ylim(0, 185)
    ftext(fig, "Pad aborts excluded. *2026 to 13 Oct. " + FOOT)
    finish(fig, "ch36_cadence")


# ---------------------------------------------------------------------------------------------- 9 constellation
def constellation():
    N = 3000
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.1), gridspec_kw=dict(width_ratios=[1, 1]))
    k = np.arange(5, 121)
    a1.plot(k, np.ceil(N / k), color=NAVY, lw=1.4)
    pts = [("Falcon 9", 24, BLUE, (0.62, 1.0)), ("Atlas V 551", 29, SKY, (1.12, 1.12)),
           ("Ariane 64", 36, VIOLET, (1.12, 1.1)), ("New Glenn", 48, "#2B8C8C", (1.12, 1.12)),
           ("Starship (assumed 60)", 60, RED, (0.55, 0.78))]
    for lab, kk, col, (fx, fy) in pts:
        n = math.ceil(N / kk)
        a1.plot(kk, n, "o", color=col, ms=5, zorder=3)
        a1.text(kk * fx, n * fy, f"{lab}: {n}", fontsize=6.2, color=col, va="center",
                ha="left" if fx > 1 else "right")
    a1.set_xscale("log")
    a1.set_yscale("log")
    a1.set_xlim(5, 130)
    a1.set_ylim(15, 700)
    a1.set_xticks([5, 10, 20, 50, 100])
    a1.set_xticklabels(["5", "10", "20", "50", "100"])
    a1.set_yticks([20, 50, 100, 200, 500])
    a1.set_yticklabels(["20", "50", "100", "200", "500"])
    a1.yaxis.set_minor_formatter(plt.NullFormatter())
    a1.xaxis.set_minor_formatter(plt.NullFormatter())
    a1.set_xlabel("Satellites per launch")
    a1.set_ylabel("Launches for 3 000 satellites")
    a1.set_title("(a) Launches needed", fontsize=8.6, loc="left")
    # (b) chance of at least one failure during the campaign
    n = np.arange(1, 201)
    for p, col in [(0.005, GREEN), (0.01, BLUE), (0.02, ORANGE), (0.05, RED)]:
        a2.plot(n, 100 * (1 - (1 - p) ** n), color=col, lw=1.4, label=f"p = {100 * p:g} % per launch")
    for nn in (63, 84, 125):
        a2.axvline(nn, color=GREY, lw=0.6, ls=":")
    a2.text(64, 4, "63", fontsize=5.8, color=GREY)
    a2.text(85, 4, "84", fontsize=5.8, color=GREY)
    a2.text(126, 4, "125", fontsize=5.8, color=GREY)
    a2.set_xlim(0, 200)
    a2.set_ylim(0, 100)
    a2.set_xlabel("Number of launches")
    a2.set_ylabel("Chance of at least one failure (%)")
    a2.set_title("(b) Campaign risk", fontsize=8.6, loc="left")
    a2.legend(fontsize=6.2, loc="lower right")
    ftext(fig, "(a) Launches = ceil(3 000 / satellites per launch); per-launch counts from Amazon Leo missions "
               "(Starship value assumed). (b) 1 − (1 − p)^n for independent launches.")
    finish(fig, "ch36_constellation")


if __name__ == "__main__":
    fns = [timeline, countries, families, mass, reliability, capability, silhouettes, cadence, constellation]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
