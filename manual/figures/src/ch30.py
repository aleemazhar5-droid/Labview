import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge, FancyArrow

MMHG = 0.133322  # kPa per mmHg
PH2O = 47 * MMHG  # water-vapour pressure in the lungs, 6.27 kPa


# ---------------------------------------------------------------- 1. duration records
def records():
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    R = [(1961.28, 1.8 / 24, "Vostok 1\n(Gagarin)"), (1961.60, 1.05, "Vostok 2"), (1962.62, 3.93, ""),
         (1963.45, 4.96, ""), (1965.64, 7.95, "Gemini 5"), (1965.93, 13.77, "Gemini 7"),
         (1970.43, 17.71, ""), (1971.45, 23.77, "Soyuz 11"), (1973.40, 28.0, ""), (1973.57, 59.5, ""),
         (1973.87, 84.0, "Skylab 4"), (1977.95, 96.4, ""), (1978.45, 139.6, ""), (1979.15, 175.0, ""),
         (1980.27, 184.8, "Salyut 6"), (1982.37, 211.4, ""), (1984.10, 237.0, "Salyut 7"),
         (1987.10, 326.5, ""), (1987.97, 365.9, ""), (1994.02, 437.7, "")]
    ax.text(1988.0, 520, "Titov & Manarov", fontsize=5.9, ha="center", va="bottom", color=INK)
    ax.text(1994.6, 437.7 * 1.22, "Polyakov 437.7 d (Mir)", fontsize=5.9, ha="left", va="bottom", color=INK)
    xs = [r[0] for r in R] + [2026.8]
    ys = [r[1] for r in R] + [R[-1][1]]
    ax.step(xs, ys, where="post", color=NAVY, lw=1.5, zorder=3, label="Single-flight record")
    ax.scatter([r[0] for r in R], [r[1] for r in R], s=12, color=NAVY, zorder=4)
    for x, y, t in R:
        if t:
            dy = 1.9 if y < 300 else 1.0
            ax.text(x - 0.4, y * dy, t, fontsize=5.9, ha="right" if y < 300 else "center", va="bottom", color=INK)
    L = [(1991.38, 311.8, "Krikalev 312 d (1991–92)", 20, "left"),
         (1998.6, 379.6, "Avdeev 380 d (1998–99)", 40, "left"),
         (2015.24, 340.4, "Kelly & Kornienko 340 d", 20, "right"),
         (2019.2, 328.6, "Koch 329 d (women's record)", 10, "right"),
         (2021.27, 355.1, "Vande Hei & Dubrov 355 d", 5, "right"),
         (2022.72, 370.9, "Rubio & Prokopyev 371 d", 2.5, "right"),
         (2023.71, 373.8, "Kononenko & Chub 374 d", 1.25, "right")]
    ax.scatter([l[0] for l in L], [l[1] for l in L], s=16, marker="D", color=ORANGE, zorder=5,
               label="Other flights longer than 300 days")
    for x, y, t, yl, ha in L:
        ax.plot([x, x], [y * 0.85, yl * 1.25], color=ORANGE, lw=0.5, zorder=2)
        ax.text(x + (0.5 if ha == "right" else -0.5), yl, t, fontsize=5.8, ha=ha, va="center", color=ORANGE)
    ax.axhline(900, color=RED, lw=0.9, ls="--")
    ax.text(1960.5, 1000, "Mars conjunction-class mission ≈ 900 days", fontsize=6.2, color=RED, va="bottom")
    ax.set_yscale("log")
    ax.set_ylim(0.05, 3000)
    ax.set_xlim(1960, 2027)
    ax.set_yticks([0.1, 1, 10, 100, 1000])
    ax.set_yticklabels(["0.1", "1", "10", "100", "1 000"])
    ax.set_ylabel("Duration of one flight (days, log)")
    ax.set_xlabel("Year of launch")
    ax.legend(loc="lower right", fontsize=6.4, bbox_to_anchor=(1.0, 0.0))
    fig.text(0.99, 0.01, "Record progression from mission durations; Kononenko holds the cumulative record, 1 111 days over five flights (2024).",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch30_records")


# ---------------------------------------------------------------- 2. body adaptation and bone loss
def body():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.2), gridspec_kw={"width_ratios": [1.0, 1.15]})
    # (a) bone mineral density model
    t = np.linspace(0, 48, 600)
    thalf = 9.0

    def bmd(T, r):
        y = np.where(t <= T, 100 - r * t, 0)
        loss = r * T
        rec = 100 - loss * np.exp(-np.log(2) * (t - T) / thalf)
        return np.where(t <= T, y, rec)

    a1.fill_between(t, bmd(6, 1.0), bmd(6, 1.5), color=BLUE, alpha=0.30, lw=0)
    a1.plot(t, bmd(6, 1.0), color=BLUE, lw=1.0)
    a1.plot(t, bmd(6, 1.5), color=BLUE, lw=1.0)
    a1.fill_between(t, bmd(12, 1.0), bmd(12, 1.5), color=ORANGE, alpha=0.30, lw=0)
    a1.plot(t, bmd(12, 1.0), color=ORANGE, lw=1.0)
    a1.plot(t, bmd(12, 1.5), color=ORANGE, lw=1.0)
    a1.annotate("6-month flight:\n6–9 % lost", (6.0, 91.8), (0.8, 83.6), fontsize=6.2, color=BLUE, va="center",
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6))
    a1.text(13.5, 82.5, "1-year flight:\n12–18 % lost", fontsize=6.2, color=ORANGE, va="center")
    a1.text(33, 86.2, "after landing: exponential\nrecovery, half-time ≈ 9 months", fontsize=6.2, color=INK, ha="center")
    a1.set_xlim(0, 48)
    a1.set_ylim(80, 100.5)
    a1.set_xlabel("Months after launch")
    a1.set_ylabel("Hip bone mineral density (% of pre-flight)")
    a1.set_title("(a) Bone loss and recovery (model)", fontsize=7.6)

    # (b) timeline of adaptation
    rows = [("Fluid shift (≈ 2 L headward)", 0.03, 72, 1e5, BLUE),
            ("Space motion sickness", 1, 72, None, VIOLET),
            ("Plasma volume −10–20 %", 12, 168, 1e5, SKY),
            ("Spine lengthens, back pain", 12, 400, 1e5, GOLD),
            ("Muscle atrophy", 72, 1e5, None, GREEN),
            ("Bone loss 1–1.5 %/month", 200, 1e5, None, ORANGE),
            ("Neuro-ocular changes (SANS)", 700, 1e5, None, RED),
            ("Radiation dose accumulates", 0.03, 1e5, None, GREY)]
    for i, (name, t0, t1, t2, c) in enumerate(rows):
        a2.barh(i, t1 - t0, left=t0, color=c, height=0.55, zorder=2)
        if t2:
            a2.barh(i, t2 - t1, left=t1, color=c, alpha=0.28, height=0.55, zorder=2)
    a2.set_xscale("log")
    a2.set_xlim(0.03, 1e5)
    a2.set_xticks([1, 24, 24 * 7, 24 * 30, 24 * 365])
    a2.set_xticklabels(["1 h", "1 d", "1 wk", "1 mo", "1 yr"], fontsize=6.6)
    a2.set_yticks(range(len(rows)))
    a2.set_yticklabels([r[0] for r in rows], fontsize=6.4)
    a2.invert_yaxis()
    a2.grid(axis="y", visible=False)
    a2.set_xlabel("Time in weightlessness (log)")
    a2.set_title("(b) When the body changes (typical)", fontsize=7.6)
    fig.text(0.99, 0.01, "(a) Linear loss of 1–1.5 %/month in flight, exponential recovery with 9-month half-time (Sibonga et al. 2007); "
             "modern resistive exercise reduces the loss. (b) Dark: onset/main phase; pale: new steady state.",
             ha="right", va="bottom", fontsize=5.9, color=GREY, wrap=True)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "ch30_body")


# ---------------------------------------------------------------- 3. radiation dose
def dose():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.2), gridspec_kw={"width_ratios": [1.15, 1.0]})
    B = [("Natural background on Earth, 1 year", 2.4, GREEN),
         ("Lunar mission: 10 d transit + 30 d surface", 1.84 * 10 + 1.37 * 30, BLUE),
         ("ISS, 6 months (mean of 19 crew)", 72, SKY),
         ("ISS, 340 days (Scott Kelly)", 146, SKY),
         ("Mars opposition class: 440 d + 30 d", 1.84 * 440 + 0.64 * 30, ORANGE),
         ("Mars conjunction class: 360 d + 500 d", 1.84 * 360 + 0.64 * 500, RED)]
    y = np.arange(len(B))
    a1.barh(y, [b[1] for b in B], color=[b[2] for b in B], height=0.6, zorder=2)
    for yi, b in zip(y, B):
        a1.text(b[1] + 15, yi, f"{b[1]:,.0f}".replace(",", " ") if b[1] >= 10 else f"{b[1]:.1f}",
                va="center", fontsize=6.4)
    a1.axvline(600, color=NAVY, lw=1.2, ls="--", zorder=3)
    a1.text(615, 0.6, "NASA career\nlimit 600 mSv", fontsize=6.1, color=NAVY, va="center")
    a1.set_yticks(y)
    a1.set_yticklabels([b[0] for b in B], fontsize=6.3)
    a1.invert_yaxis()
    a1.set_xlim(0, 1150)
    a1.set_xlabel("Effective dose (mSv)")
    a1.grid(axis="y", visible=False)
    a1.set_title("(a) Mission doses", fontsize=7.6)

    # (b) cumulative dose through a Mars mission
    def path(segs):
        t, d, tt, dd = [0], [0], 0, 0
        for days, rate in segs:
            tt += days
            dd += days * rate
            t.append(tt)
            d.append(dd)
        return t, d

    tc, dc = path([(180, 1.84), (500, 0.64), (180, 1.84)])
    to, do = path([(220, 1.84), (30, 0.64), (220, 1.84)])
    a2.plot(tc, dc, color=RED, lw=1.6, label="Conjunction class (860 d)")
    a2.plot(to, do, color=ORANGE, lw=1.6, label="Opposition class (470 d)")
    a2.plot([0, 365], [0, 0.40 * 365], color=SKY, lw=1.6, label="ISS (≈ 0.4 mSv/day)")
    a2.axhline(600, color=NAVY, lw=1.1, ls="--")
    a2.plot([600], [600], "o", color=RED, ms=4)
    a2.annotate("limit reached\non day 600,\non the surface", (600, 600), (780, 330), fontsize=6.0, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.6), ha="center")
    a2.text(15, 760, "cruise\n1.84 mSv/d", fontsize=6.0, color=INK, ha="left")
    a2.text(450, 320, "Mars surface\n0.64 mSv/d", fontsize=6.0, color=INK, ha="center")
    a2.set_xlim(0, 900)
    a2.set_ylim(0, 1100)
    a2.set_xlabel("Mission day")
    a2.set_ylabel("Cumulative effective dose (mSv)")
    a2.legend(loc="lower right", fontsize=6.0)
    a2.set_title("(b) Dose accumulated during a Mars mission", fontsize=7.6)
    fig.text(0.99, 0.01, "Rates: MSL/RAD cruise 1.84 mSv/day and Mars surface 0.64 mSv/day (2012–13); lunar surface 1.37 mSv/day "
             "(Chang'e 4 LND); ISS from Cucinotta et al. 2008 and the Twins Study. No large solar particle event included.",
             ha="right", va="bottom", fontsize=5.9, color=GREY, wrap=True)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "ch30_dose")


# ---------------------------------------------------------------- 4. cabin atmosphere design space
def atmos():
    fig, ax = plt.subplots(figsize=(6.6, 4.1))
    P = np.linspace(20, 120, 400)

    def f_of(pio2_mmhg):
        return 100 * pio2_mmhg * MMHG / (P - PH2O)

    hyp = f_of(127)
    ax.fill_between(P, 0, np.minimum(hyp, 100), color=VIOLET, alpha=0.10, lw=0)
    ax.plot(P, hyp, color=VIOLET, lw=1.2)
    ax.fill_between(P, f_of(145), f_of(155), color=GREEN, alpha=0.30, lw=0)
    hyper = f_of(356)
    ax.fill_between(P, np.minimum(hyper, 100), 100, color=GOLD, alpha=0.14, lw=0)
    ax.plot(P, np.minimum(hyper, 100), color=GOLD, lw=1.2)
    ax.axhline(30, color=RED, lw=1.0, ls="--")
    ax.fill_between(P, 30, 100, color=RED, alpha=0.05, lw=0)
    ax.text(119, 30.6, "30 % O₂: materials flammability test level", fontsize=6.0, color=RED, ha="right", va="bottom")
    ax.text(21.5, 45, "Hypoxic\n(inspired O₂\nbelow 127 mmHg)", fontsize=6.2, color=VIOLET, ha="left", va="center")
    ax.text(40, 77, "Normoxic band\n(inspired O₂ 145–155 mmHg)", fontsize=6.2, color=GREEN, ha="left", va="center")
    ax.text(100, 72, "Hyperoxic: inspired O₂\nabove 356 mmHg", fontsize=6.3, color="#8A6D0B", ha="center")
    pts = [(101.3, 20.9, "Sea level; ISS, Soyuz,\nCrew Dragon, Orion", NAVY, (101.3, 14.2), "center"),
           (75.3, 20.9, "Airliner cabin\n(2 400 m)", GREY, (75.3, 14.6), "center"),
           (33.7, 20.9, "Everest\nsummit", GREY, (33.7, 14.6), "center"),
           (70.3, 26.5, "Shuttle pre-EVA, ISS campout (70.3 kPa, 26.5 %)", BLUE, (78, 36.5), "left"),
           (56.5, 34.0, "Exploration atmosphere (56.5 kPa, 34 %)", ORANGE, (64, 45), "left"),
           (34.5, 72.0, "Skylab (34.5 kPa, 72 %)", BLUE, (40.5, 65.0), "left"),
           (34.5, 100.0, "Mercury, Gemini,\nApollo in flight", BLUE, (36.5, 94.5), "left"),
           (29.6, 100.0, "EMU", GREY, (30.2, 96.0), "left"),
           (115.0, 100.0, "Apollo 1 ground\ntest, Jan 1967", RED, (113.5, 94.0), "right")]
    for x, y, t, c, (tx, ty), ha in pts:
        ax.plot(x, y, "o", color=c, ms=5, zorder=5, mec="white", mew=0.6)
        if abs(tx - x) > 6 or abs(ty - y) > 9:
            ax.plot([x, tx - 0.5], [y, ty], color=c, lw=0.5, zorder=4)
        ax.text(tx, ty, t, fontsize=6.0, color=c, ha=ha, va="center", zorder=6)
    ax.set_xlim(20, 120)
    ax.set_ylim(10, 104)
    ax.set_xlabel("Total cabin pressure (kPa)")
    ax.set_ylabel("Oxygen fraction (%)")
    fig.text(0.99, 0.01, "Inspired O₂ partial pressure = (total pressure − 47 mmHg water vapour) × O₂ fraction; limits from "
             "NASA-STD-3001 Vol. 2 (Rev F, 2026). Lower total pressure means less nitrogen and shorter pre-EVA oxygen prebreathe.",
             ha="right", va="bottom", fontsize=5.9, color=GREY, wrap=True)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch30_atmos")


# ---------------------------------------------------------------- 5. CO2 build-up and scrubber flow
def co2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.0))
    R, T = 8.314, 295.0
    gen = 1.0 / 0.04401 / 86400  # mol/s per crew member (1.0 kg/day)
    rate = gen * R * T / MMHG / 1000 * 3600  # mmHg per hour per (crew/m3)
    t = np.linspace(0, 24, 400)
    for v, c, lab in [(2.5, RED, "2.5 m³/person (4 crew, 10 m³ capsule)"), (5, ORANGE, "5 m³/person"),
                      (25, BLUE, "25 m³/person (small habitat)"), (130, GREEN, "130 m³/person (ISS, 7 crew)")]:
        a1.plot(t, 2.5 + rate / v * t, color=c, lw=1.5, label=lab)
    for lvl, txt in [(3.0, "NASA 1-h limit 3 mmHg"), (7.6, "1 % CO₂"), (15.2, "2 %"), (38, "5 %")]:
        a1.axhline(lvl, color=GREY, lw=0.7, ls=":")
        if lvl == 3.0:
            a1.text(23.8, lvl - 0.4, txt, fontsize=5.9, color=GREY, ha="right", va="top")
        else:
            a1.text(23.8, lvl + 0.5, txt, fontsize=5.9, color=GREY, ha="right", va="bottom")
    a1.set_xlim(0, 24)
    a1.set_ylim(0, 42)
    a1.set_xlabel("Hours after CO₂ removal stops")
    a1.set_ylabel("CO₂ partial pressure (mmHg)")
    a1.legend(loc="upper right", bbox_to_anchor=(1.0, 0.80), fontsize=5.8)
    a1.set_title("(a) Build-up with no scrubbing", fontsize=7.6)

    Q = np.linspace(1, 40, 400)  # L/s effective (flow x capture efficiency)
    for n, c in [(4, BLUE), (7, ORANGE)]:
        pp = n * gen * R * T / (Q / 1000) / 1000 / MMHG
        a2.plot(Q, pp, color=c, lw=1.6, label=f"{n} crew")
        qreq = n * gen * R * T / (3.0 * MMHG * 1000) * 1000
        a2.plot([qreq], [3.0], "o", color=c, ms=4)
        tx, ty = (2.0, 1.0) if n == 4 else (14.5, 4.4)
        a2.plot([qreq, tx + 2.0], [3.0, ty + (0.35 if n == 4 else -0.25)], color=c, lw=0.5)
        a2.text(tx, ty, f"{qreq:.1f} L/s for 3 mmHg", fontsize=6.0, color=c, va="center", ha="left")
    a2.axhline(3.0, color=GREY, lw=0.7, ls=":")
    a2.set_xlim(0, 40)
    a2.set_ylim(0, 15)
    a2.set_xlabel("Effective scrubber flow, Q × capture efficiency (L/s)")
    a2.set_ylabel("Steady-state CO₂ (mmHg)")
    a2.legend(loc="upper right", fontsize=6.2)
    a2.set_title("(b) Steady state with scrubbing", fontsize=7.6)
    fig.text(0.99, 0.01, "Ideal gas at 22 °C, well-mixed cabin, 1.0 kg CO₂ per person per day. (a) dp/dt = ṅRT/V; "
             "(b) p = ṅRT/(Qη).", ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch30_co2")


# ---------------------------------------------------------------- 6. metabolic mass balance
def massbal():
    fig, ax = canvas(6.8, 3.7, xlim=(0, 100), ylim=(0, 54))
    k = 2.3  # data units of width per kg

    def flow(x0, x1, y, m, c, txt, side):
        w = max(m * k, 0.45)
        ax.add_patch(FancyArrow(x0, y, x1 - x0, 0, width=w, head_width=w + 1.6, head_length=1.8,
                                length_includes_head=True, fc=c, ec="none", zorder=3))
        if side == "L":
            ax.text(x0 - 1.0, y, txt, ha="right", va="center", fontsize=6.6, color=INK)
        else:
            ax.text(x1 + 1.0, y, txt, ha="left", va="center", fontsize=6.6, color=INK)

    box(ax, 40, 7, 20, 40, "", fc="#F6EEE4", ec=ORANGE, r=2.0)
    label(ax, 50, 39, "One crew\nmember", fs=8.2, weight="bold", color=INK)
    label(ax, 50, 30, "82 kg, RQ 0.86,\n90 min exercise\nper day", fs=6.4, color=INK)
    label(ax, 50, 18.5, "metabolic water\n+0.49 kg made\ninside the body", fs=6.1, color=GREEN)
    label(ax, 50, 10.5, "In = out\n= 5.67 kg/day", fs=6.4, weight="bold", color=NAVY)
    ins = [(44, 0.895, BLUE, "Oxygen 0.90 kg"),
           (35, 0.800, GOLD, "Food solids 0.80 kg\n(12.8 MJ)"),
           (24, 3.217, GREEN, "Drinking and food-\npreparation water 3.22 kg"),
           (12, 0.760, SKY, "Water in food 0.76 kg")]
    for y, m, c, t in ins:
        flow(23, 40, y, m, c, t, "L")
    outs = [(44, 1.085, ORANGE, "Carbon dioxide 1.09 kg"),
            (34, 2.946, SKY, "Breath and sweat water 2.95 kg"),
            (23, 1.481, GOLD, "Urine 1.48 kg (water 1.42)"),
            (15, 0.133, GREY, "Faeces 0.13 kg"),
            (10, 0.027, GREY, "Sweat solids 0.03 kg")]
    for y, m, c, t in outs:
        flow(60, 77, y, m, c, t, "R")
    ax.add_patch(FancyArrow(50, 47, 0, 4.0, width=1.8, head_width=3.6, head_length=1.6,
                            length_includes_head=True, fc=RED, ec="none", zorder=3))
    label(ax, 53.5, 51.5, "Heat 12.4 MJ/day (144 W): 6.3 MJ sensible + 6.1 MJ latent", fs=6.5, color=RED, ha="left")
    label(ax, 22, 49.0, "INPUTS (kg per day)", fs=6.8, weight="bold", color=NAVY, ha="right")
    label(ax, 61, 47.6, "OUTPUTS", fs=6.8, weight="bold", color=NAVY, ha="left")
    label(ax, 0.5, 2.0, "Arrow width proportional to mass per day. Food as supplied with packaging: 1.8–2.4 kg/day.",
          fs=6.0, color=GREY, ha="left")
    save(fig, "ch30_massbal")


# ---------------------------------------------------------------- 7. ECLSS schematic
def eclss():
    fig, ax = canvas(6.9, 4.3, xlim=(-6, 100), ylim=(0, 62))
    AIR, CO2C, H2C, WAT, WST = BLUE, ORANGE, VIOLET, GREEN, GREY

    def tb(x, y, w, h, title, body, hc):
        title_box(ax, x, y, w, h, title, body, hc=hc, ec=hc, fs=6.0, tfs=6.7)

    box(ax, 36, 40, 28, 14, "", fc="#FFF6EA", ec=NAVY, lw=1.3, r=1.5)
    label(ax, 50, 50.5, "CABIN AIR AND CREW", fs=7.6, weight="bold", color=NAVY)
    label(ax, 50, 45.0, "101 kPa, 21 % O₂, 18–27 °C\nCO₂ < 3 mmHg", fs=6.2)
    tb(4, 43, 24, 10, "CO₂ removal", "CDRA / 4-bed zeolite\nor amine swing bed", CO2C)
    tb(4, 25, 24, 10, "CO₂ reduction", "Sabatier reactor\nCO₂ + 4H₂ → CH₄ + 2H₂O", CO2C)
    tb(4, 5, 24, 10, "O₂ generation", "water electrolysis (OGA,\nElektron) 2H₂O → 2H₂ + O₂", AIR)
    tb(35, 25, 14, 10, "Humidity", "condensing heat\nexchanger", AIR)
    tb(51, 25, 14, 10, "Trace gases", "charcoal,\ncatalytic oxidiser", AIR)
    tb(36, 4, 28, 11, "Water processor (WPA)", "filters, ion exchange,\ncatalytic oxidation, iodine", WAT)
    tb(73, 43, 24, 10, "Urine processor (UPA)", "vacuum distillation\n~85 % of urine water", WST)
    tb(76, 25, 21, 10, "Brine processor", "evaporates the\nremaining brine", WST)
    # air loop
    darrow(ax, (28.2, 48), (35.8, 48), color=AIR, lw=1.1)
    label(ax, 32, 50.2, "air", fs=6.0, color=AIR)
    arrow(ax, (16, 42.8), (16, 35.3), color=CO2C, lw=1.3)
    label(ax, 17, 39, "CO₂", fs=6.2, color=CO2C, ha="left")
    arrow(ax, (10, 15.2), (10, 24.8), color=H2C, lw=1.3)
    label(ax, 9, 20, "H₂", fs=6.2, color=H2C, ha="right")
    arrow(ax, (4, 30), (-4.5, 30), color=WST, lw=1.2)
    label(ax, -1.5, 32.5, "CH₄\nvented", fs=5.9, color=WST)
    arrow(ax, (28.2, 13), (35.8, 42.5), color=AIR, lw=1.4)
    label(ax, 31.2, 31, "O₂", fs=6.4, color=AIR, weight="bold", ha="right")
    darrow(ax, (41.5, 35.2), (41.5, 39.8), color=AIR, lw=1.0)
    darrow(ax, (58.5, 35.2), (58.5, 39.8), color=AIR, lw=1.0)
    # water loop
    arrow(ax, (41.5, 24.8), (41.5, 15.2), color=WAT, lw=1.2)
    label(ax, 40.8, 20, "condensate", fs=5.9, color=WAT, ha="right")
    arrow(ax, (24, 24.8), (36.5, 13.5), color=WAT, lw=1.2)
    label(ax, 32.0, 22.6, "water", fs=5.9, color=WAT, ha="left")
    arrow(ax, (64.2, 47), (72.8, 47), color=WST, lw=1.2)
    label(ax, 68.5, 48.6, "urine", fs=5.9, color=WST)
    arrow(ax, (86, 42.8), (86, 35.2), color=WST, lw=1.2)
    label(ax, 87, 39, "brine", fs=5.9, color=WST, ha="left")
    arrow(ax, (76, 42.8), (64.2, 12.5), color=WAT, lw=1.2)
    label(ax, 72.5, 31, "distillate", fs=5.9, color=WAT, ha="right")
    arrow(ax, (86, 24.8), (64.2, 9), color=WAT, lw=1.2)
    label(ax, 80, 15.5, "water", fs=5.9, color=WAT, ha="left")
    arrow(ax, (97, 30), (99.5, 22), color=WST, lw=1.0)
    label(ax, 98, 20, "dry\nresidue", fs=5.6, color=WST, va="top")
    arrow(ax, (50, 15.2), (50, 24.6), color=WAT, lw=1.6)
    arrow(ax, (50, 35.4), (50, 39.8), color=WAT, lw=1.6)
    label(ax, 50.6, 20, "potable\nwater", fs=5.9, color=WAT, ha="left")
    arrow(ax, (35.8, 8), (28.2, 8), color=WAT, lw=1.3)
    label(ax, 32, 9.2, "water", fs=5.9, color=WAT)
    arrow(ax, (50, 61), (50, 54.2), color=NAVY, lw=1.2)
    label(ax, 51, 59, "resupply: N₂/O₂ gas, food, spares, filters", fs=6.0, color=NAVY, ha="left")
    xk = -5.5
    for c, w in [(AIR, "air, O₂"), (CO2C, "CO₂"), (H2C, "H₂"), (WAT, "water"), (WST, "urine, brine, CH₄")]:
        ax.plot([xk, xk + 2.6], [59.5, 59.5], color=c, lw=2.2, solid_capstyle="butt")
        ax.text(xk + 3.2, 59.5, w, fontsize=5.9, va="center", ha="left", color=INK)
        xk += 4.2 + 1.25 * len(w)
    box(ax, 67, 0.8, 32.5, 8.2, "Also: pressure control (N₂/O₂ make-up),\nfire detection and suppression,\nrelief valves, microbial monitoring",
        fc="white", ec=GREY, fs=5.6, r=0.8, lw=0.7)
    save(fig, "ch30_eclss")


# ---------------------------------------------------------------- 8. open vs closed loop trade
def trade():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.1), gridspec_kw={"width_ratios": [1.15, 1.0]})
    t = np.linspace(0, 1000, 500)
    daily_open = 32.23
    sysm = 7062
    resid = 0.42 * 4 * 18.015 / 16 + 472 / 365
    a1.plot(t, daily_open * t / 1000, color=RED, lw=1.7, label="Open loop (stored O₂, water, LiOH)")
    a1.plot(t, (sysm + resid * t) / 1000, color=BLUE, lw=1.7, label="ISS-type regenerative ECLSS")
    tb = sysm / (daily_open - resid)
    a1.plot([tb], [daily_open * tb / 1000], "o", color=NAVY, ms=4.5, zorder=5)
    a1.annotate(f"break-even ≈ {tb:.0f} days", (tb, daily_open * tb / 1000), (480, 5.6), fontsize=6.3, color=NAVY,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.6))
    for x0, x1, txt in [(0, 30, "lunar sortie"), (430, 470, "Mars\ntransit"), (840, 900, "Mars\nconjunction")]:
        a1.axvspan(x0, x1, color=GREY, alpha=0.12, lw=0)
        if x0 == 0:
            a1.text(3, 29.5, txt, fontsize=5.9, ha="left", va="top", color=INK)
        else:
            a1.text((x0 + x1) / 2, 0.8, txt, fontsize=5.9, ha="center", va="bottom", color=INK)
    a1.set_xlim(0, 1000)
    a1.set_ylim(0, 30)
    a1.set_xlabel("Mission duration (days)")
    a1.set_ylabel("Life-support mass, 4 crew (t)")
    a1.legend(loc="upper left", bbox_to_anchor=(0.04, 0.86), fontsize=6.0)
    a1.set_title("(a) Cumulative mass, food excluded", fontsize=7.6)

    S = [("CO₂ removal (CDRA)", 95, ORANGE), ("Condensate/hygiene water", 132, GREEN),
         ("Whole water recovery", 190, GREEN), ("Complete ISS ECLSS", 219, NAVY),
         ("CO₂ reduction (Sabatier)", 301, ORANGE), ("Urine processing", 319, GREY),
         ("O₂ generation (OGS)", 557, BLUE)]
    y = np.arange(len(S))
    a2.barh(y, [s[1] for s in S], color=[s[2] for s in S], height=0.6, zorder=2)
    for yi, s in zip(y, S):
        a2.text(s[1] + 10, yi, f"{s[1]} d", va="center", fontsize=6.3)
    a2.axvline(450, color=RED, lw=1.0, ls="--")
    a2.text(445, -0.95, "450-day Mars transit", fontsize=6.0, color=RED, va="center", ha="right")
    a2.set_yticks(y)
    a2.set_yticklabels([s[0] for s in S], fontsize=6.4)
    a2.invert_yaxis()
    a2.set_xlim(0, 700)
    a2.set_ylim(6.6, -1.4)
    a2.set_xlabel("Days to pay back its own mass")
    a2.grid(axis="y", visible=False)
    a2.set_title("(b) Break-even by subsystem", fontsize=7.6)
    fig.text(0.99, 0.01, "ISS hardware with three spare sets (7 062 kg) replacing 32.2 kg/day of supplies for 4 crew (Jones, ICES-2017-85); "
             "(a) adds 3.2 kg/day residual resupply (O₂ not recovered by Sabatier, filters). Tankage neglected.",
             ha="right", va="bottom", fontsize=5.9, color=GREY, wrap=True)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "ch30_trade")


if __name__ == "__main__":
    fns = [records, body, dose, atmos, co2, massbal, eclss, trade]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
