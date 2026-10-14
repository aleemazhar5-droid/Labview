import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403


def vmodel():
    fig, ax = canvas(7.2, 4.2, (0, 100), (0, 58))
    left = [("Mission needs &\nconcept of operations", 1, 48), ("System\nrequirements", 8, 38),
            ("System architecture /\nsubsystem requirements", 15, 28), ("Detailed design\n(components, software)", 22, 18)]
    right = [("Validation:\nin-orbit commissioning", 77, 48), ("System verification\n(spacecraft tests)", 70, 38),
             ("Subsystem integration\n& verification", 63, 28), ("Unit tests &\ncomponent qualification", 56, 18)]
    for t, x, y in left:
        box(ax, x, y, 22, 8, t, fc="#E8F1FA", ec=BLUE, fs=6.8)
    for t, x, y in right:
        box(ax, x, y, 22, 8, t, fc="#EEF7F1", ec=GREEN, fs=6.8)
    box(ax, 37, 6, 26, 8, "Build: manufacture,\ncode, procure", fc="#FCF3EA", ec=ORANGE, fs=6.8)
    for (t1, x1, y1), (t2, x2, y2) in zip(left, right):
        arrow(ax, (x1 + 22, y1 + 4), (x2, y2 + 4), None, color=GREY, ls="--", lw=0.8, style="<|-|>")
    for a, b in zip(left[:-1], left[1:]):
        arrow(ax, (a[1] + 6, a[2]), (b[1] + 6, b[2] + 8), color=BLUE)
    for a, b in zip(right[1:], right[:-1]):
        arrow(ax, (a[1] + 16, a[2] + 8), (b[1] + 16, b[2]), color=GREEN)
    arrow(ax, (left[-1][1] + 8, left[-1][2]), (37, 10), color=BLUE)
    arrow(ax, (63, 10), (right[-1][1] + 14, right[-1][2]), color=GREEN)
    ax.text(14, 57, "DECOMPOSITION & DEFINITION", fontsize=7.5, color=BLUE, weight="bold")
    ax.text(68, 57, "INTEGRATION & VERIFICATION", fontsize=7.5, color=GREEN, weight="bold")
    ax.text(50, 44, "verification\nplanned at each level", fontsize=6.6, color=GREY, ha="center", style="italic")
    ax.annotate("", xy=(97, 3), xytext=(3, 3), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.8))
    ax.text(50, 0.3, "time →", fontsize=6.8, color=GREY, ha="center")
    save(fig, "ch04_vmodel")


def lifecycle():
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 30)
    ax.axis("off")
    phases = [("Pre-A\nConcept\nstudies", 0, 9, "#DCE8F4"), ("A\nConcept &\ntechnology", 9, 19, "#C6DBEF"),
              ("B\nPreliminary\ndesign", 19, 31, "#9ECAE1"), ("C\nFinal design &\nfabrication", 31, 49, "#6BAED6"),
              ("D\nAssembly, integration,\ntest & launch", 49, 66, "#4292C6"),
              ("E\nOperations &\nsustainment", 66, 92, "#2171B5"), ("F\nClose-\nout", 92, 100, "#08519C")]
    for name, a, b, c in phases:
        ax.add_patch(Rectangle((a, 12), b - a, 10, fc=c, ec="white", lw=1.5))
        ax.text((a + b) / 2, 17, name, ha="center", va="center", fontsize=6.8,
                color="white" if is_dark(c) else INK, linespacing=1.15)
    ax.text(4.5, 25.5, "FORMULATION", fontsize=7.5, weight="bold", color=NAVY)
    ax.text(50, 25.5, "IMPLEMENTATION", fontsize=7.5, weight="bold", color=NAVY)
    ax.plot([1, 30.5], [24.5, 24.5], color=NAVY, lw=1)
    ax.plot([31.5, 99], [24.5, 24.5], color=NAVY, lw=1)
    kdp = [(9, "KDP A"), (19, "KDP B"), (31, "KDP C"), (49, "KDP D"), (66, "KDP E"), (92, "KDP F")]
    for x, t in kdp:
        ax.plot(x, 12, marker="v", color=ORANGE, ms=7)
        ax.text(x, 10.3, t, fontsize=6.3, ha="center", color=ORANGE, va="top")
    reviews = [(7, "MCR"), (14, "SRR"), (18, "MDR/SDR"), (29, "PDR"), (41, "CDR"), (50, "SIR"), (59, "ORR"),
               (64, "FRR"), (65.8, "LRR"), (70, "PLAR"), (90, "DR")]
    for i, (x, t) in enumerate(reviews):
        y = 5.5 if i % 2 == 0 else 2.5
        ax.plot([x, x], [y + 1.2, 11.8], color=GREY, lw=0.4)
        ax.text(x, y, t, fontsize=6.2, ha="center", color=INK)
    ax.text(0, 0, "MCR mission concept · SRR system requirements · MDR/SDR mission/system definition · PDR preliminary "
            "design · CDR critical design · SIR system integration · ORR operational readiness · FRR flight readiness · "
            "LRR launch readiness · PLAR post-launch assessment · DR decommissioning", fontsize=5.6, color=GREY,
            wrap=True)
    save(fig, "ch04_lifecycle")


def cost_commit():
    x = np.linspace(0, 100, 300)
    committed = 100 * (1 - np.exp(-x / 18))
    spent = 100 / (1 + np.exp(-(x - 62) / 11))
    spent = (spent - spent[0]) / (spent[-1] - spent[0]) * 100
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ax.plot(x, committed, color=RED, lw=2, label="Life-cycle cost committed by decisions")
    ax.plot(x, spent, color=BLUE, lw=2, label="Life-cycle cost actually spent")
    ax.fill_between(x, spent, committed, color=ORANGE, alpha=0.12)
    for xv, t in [(9, "A"), (19, "B"), (31, "C"), (49, "D"), (66, "E")]:
        ax.axvline(xv, color=GREY, lw=0.5, ls=":")
        ax.text(xv + 0.7, 3, t, fontsize=7.5, color=GREY)
    ax.set_xlabel("Project time (phases)")
    ax.set_ylabel("Percentage of life-cycle cost")
    ax.text(22, 72, "≈70–80 % of cost is locked in\nby the end of preliminary design", fontsize=7.5, color=RED)
    ax.legend(loc="lower right", fontsize=7.5)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 105)
    note(ax, "Schematic, after NASA Systems Engineering Handbook (SP-2016-6105 Rev 2) and DAU studies.", xy=(1, -0.18))
    save(fig, "ch04_cost_committed")


def trl():
    fig, ax = canvas(7.0, 4.4, (0, 100), (0, 64))
    levels = [(1, "Basic principles observed and reported"), (2, "Technology concept and/or application formulated"),
              (3, "Analytical and experimental proof of concept"), (4, "Component / breadboard validated in laboratory"),
              (5, "Component / breadboard validated in relevant environment"),
              (6, "System / subsystem prototype demonstrated in relevant environment"),
              (7, "System prototype demonstrated in an operational (space) environment"),
              (8, "Actual system completed and flight qualified through test and demonstration"),
              (9, "Actual system flight proven through successful mission operations")]
    cmap = plt.get_cmap("Blues")
    for k, (n, t) in enumerate(levels):
        y = 2 + k * 6.6
        w = 40 + k * 5.0
        c = cmap(0.12 + 0.05 * k)
        ax.add_patch(Rectangle((2, y), w, 5.6, fc=c, ec="white"))
        ax.text(5, y + 2.8, f"TRL {n}", fontsize=8, weight="bold", va="center", color=NAVY)
        ax.text(17, y + 2.8, t, fontsize=6.9, va="center", color=INK)
    for y0, y1, lab, col in [(2, 22, "Research", GREY), (21.8, 41.6, "Development\n('valley of\ndeath')", ORANGE),
                             (41.6, 61.4, "Demonstration\n& deployment", GREEN)]:
        ax.plot([84.5, 84.5], [y0 + 0.5, y1 - 0.5], color=col, lw=3)
        ax.text(86, (y0 + y1) / 2, lab, fontsize=7, color=col, ha="left", va="center", weight="bold")
    save(fig, "ch04_trl")


def req_tree():
    fig, ax = canvas(7.2, 3.8, (0, 100), (0, 52))
    box(ax, 38, 42, 24, 8, "Mission objectives &\nstakeholder needs", fc=NAVY, ec=NAVY, color="white", fs=7.2)
    box(ax, 38, 30, 24, 7, "Mission / system\nrequirements (L1–L2)", fc="#C6DBEF", ec=BLUE, fs=7)
    segs = [("Space segment", 6), ("Ground segment", 30), ("Launch segment", 54), ("Operations", 78)]
    for t, x in segs:
        box(ax, x, 18, 18, 6, t, fc="#E8F1FA", ec=BLUE, fs=6.8)
        arrow(ax, (50, 30), (x + 9, 24), color=GREY, lw=0.7, ms=7)
    subs = ["Payload", "Structure", "Thermal", "Power", "ADCS", "Propulsion", "C&DH / FSW", "TT&C"]
    for k, t in enumerate(subs):
        x = 1 + k * 12.3
        box(ax, x, 5, 11, 6, t, fc="#EEF7F1", ec=GREEN, fs=6.4)
        arrow(ax, (15, 18), (x + 5.5, 11), color="#B5C3CF", lw=0.5, ms=5)
    arrow(ax, (50, 42), (50, 37), color=GREY)
    ax.text(1, 1, "Each requirement: unique ID · 'shall' statement · rationale · parent trace · verification method "
            "(Test / Analysis / Inspection / Demonstration) · owner", fontsize=6.4, color=GREY)
    save(fig, "ch04_req_tree")


def mass_pie():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.3))
    for ax, title, parts in [
        (a1, "LEO Earth-observation satellite", [("Payload", 32), ("Structure & mechanisms", 20), ("Power", 18),
                                                 ("ADCS", 7), ("Thermal", 4), ("C&DH", 4), ("TT&C", 3),
                                                 ("Propulsion (dry)", 4), ("Harness", 5), ("Propellant", 3)]),
        (a2, "GEO communications satellite", [("Payload", 25), ("Structure & mechanisms", 9), ("Power", 13),
                                               ("ADCS", 3), ("Thermal", 4), ("C&DH + TT&C", 2), ("Propulsion (dry)", 5),
                                               ("Harness", 3), ("Propellant", 36)])]:
        cols = PALETTE[:len(parts)]
        w, _ = ax.pie([p[1] for p in parts], colors=cols, startangle=90, counterclock=False,
                      wedgeprops=dict(width=0.42, edgecolor="white"))
        ax.set_title(title, fontsize=8.5)
        ax.legend(w, [f"{p[0]} {p[1]} %" for p in parts], loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=2,
                  fontsize=6.4)
    fig.text(0.99, -0.2, "Representative fractions of launch (wet) mass, after SMAD (Wertz et al., 2011) "
             "and published spacecraft data.", ha="right", fontsize=6.3, color=GREY)
    save(fig, "ch04_mass_pie")


def margins():
    phases = ["Pre-A", "A", "B (PDR)", "C (CDR)", "D", "Launch"]
    x = np.arange(len(phases))
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    for name, vals, c in [("Mass margin (new design)", [35, 30, 25, 15, 8, 2], BLUE),
                          ("Mass margin (heritage design)", [15, 12, 10, 6, 3, 1], SKY),
                          ("Power margin", [30, 25, 20, 15, 10, 5], ORANGE),
                          ("Flight-software CPU / memory margin", [60, 55, 50, 40, 30, 25], GREEN)]:
        ax.plot(x, vals, marker="o", color=c, label=name)
    ax.set_xticks(x)
    ax.set_xticklabels(phases)
    ax.set_ylabel("Recommended margin (%)")
    ax.legend(fontsize=7)
    note(ax, "Typical contingency guidance, after AIAA S-120A-2015, ECSS-E-ST-10C and NASA GSFC Gold Rules; "
             "organisations differ.", xy=(1, -0.16))
    save(fig, "ch04_margins")


def bathtub_and_redundancy():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.1))
    t = np.linspace(0.01, 10, 400)
    h = 0.6 * np.exp(-t / 0.4) + 0.05 + 0.0006 * np.exp(t / 1.3)
    a1.plot(t, h, color=NAVY, lw=2)
    a1.set_xlabel("Time")
    a1.set_ylabel("Failure rate λ(t)")
    a1.set_yticks([])
    a1.set_xticks([])
    a1.text(0.4, 0.45, "infant\nmortality", fontsize=7)
    a1.text(3.4, 0.11, "useful life (constant λ)", fontsize=7)
    a1.text(7.4, 0.35, "wear-out", fontsize=7)
    a1.set_title("The 'bathtub' curve", fontsize=8.5)
    a1.set_ylim(0, 0.7)
    yrs = np.linspace(0, 20, 300)
    lam = 1 / 30.0
    R1 = np.exp(-lam * yrs)
    R2 = 1 - (1 - R1) ** 2
    R23 = 3 * R1 ** 2 - 2 * R1 ** 3
    Rs = R1 * (1 + lam * yrs)
    a2.plot(yrs, R1, color=RED, label="single unit (MTTF 30 yr)")
    a2.plot(yrs, R2, color=BLUE, label="two units, active (1-of-2)")
    a2.plot(yrs, Rs, color=GREEN, label="two units, cold standby")
    a2.plot(yrs, R23, color=ORANGE, label="2-of-3 voting")
    a2.set_xlabel("Mission time (years)")
    a2.set_ylabel("Reliability R(t)")
    a2.legend(fontsize=6.6, loc="lower left")
    a2.set_title("Effect of redundancy", fontsize=8.5)
    a2.set_ylim(0.4, 1.01)
    save(fig, "ch04_reliability")


def risk_matrix():
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    M = np.array([[1, 1, 2, 2, 3], [1, 2, 2, 3, 3], [2, 2, 3, 3, 4], [2, 3, 3, 4, 4], [3, 3, 4, 4, 4]])
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["#9BD3A8", "#F7E08A", "#F4B266", "#E3646B"])
    ax.imshow(M, cmap=cmap, origin="lower", vmin=1, vmax=4)
    ax.set_xticks(range(5))
    ax.set_xticklabels(["1\nMinimal", "2\nMinor", "3\nModerate", "4\nSignificant", "5\nSevere"], fontsize=7)
    ax.set_yticks(range(5))
    ax.set_yticklabels(["1 Very low\n(< 0.1 %)", "2 Low\n(0.1–1 %)", "3 Moderate\n(1–10 %)", "4 High\n(10–50 %)",
                        "5 Very high\n(> 50 %)"], fontsize=7)
    ax.set_xlabel("Consequence (impact on mission, cost, schedule, safety)")
    ax.set_ylabel("Likelihood")
    ax.grid(False)
    risks = [(4, 1, "R1"), (2, 3, "R2"), (3, 2, "R3"), (1, 4, "R4"), (0, 2, "R5")]
    for x, y, t in risks:
        ax.add_patch(Circle((x, y), 0.25, fc="white", ec=NAVY, lw=1.2))
        ax.text(x, y, t, ha="center", va="center", fontsize=7, weight="bold", color=NAVY)
    ax.annotate("", xy=(3, 1), xytext=(4, 1), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1, ls="--"))
    ax.text(3.5, 1.35, "mitigation", fontsize=6.5, ha="center", color=NAVY)
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, "ch04_risk_matrix")


def model_philosophy():
    fig, ax = canvas(7.2, 3.3, (0, 100), (0, 44))
    cols = [("Development\nmodels", ["Breadboards", "Engineering model (EM)\n— form & function"], GREY),
            ("Qualification", ["Structural-thermal\nmodel (STM)", "Qualification model (QM)\n— tested to qual levels"], BLUE),
            ("Flight", ["Flight model (FM)\n— acceptance levels", "Flight spare (FS)"], GREEN)]
    for k, (h, items, c) in enumerate(cols):
        x = 3 + k * 33
        box(ax, x, 34, 28, 7, h, fc=c, ec=c, color="white", fs=8, weight="bold")
        for j, it in enumerate(items):
            box(ax, x, 22 - j * 11, 28, 9, it, fc="white", ec=c, fs=7)
    box(ax, 3, 0.5, 94, 6, "Protoflight approach: a single protoflight model (PFM) tested to qualification levels for "
        "acceptance durations — cheaper, more risk", fc="#FCF3EA", ec=ORANGE, fs=7)
    save(fig, "ch04_models")


def ait_flow():
    fig, ax = canvas(7.4, 3.0, (0, 100), (0, 40))
    steps = ["Unit\ndelivery &\nincoming\ninspection", "Mechanical\nintegration", "Electrical\nintegration &\nfunctional\ntests",
             "EMC / RF\ncompatibility", "Sine &\nrandom\nvibration,\nacoustic", "Shock /\nseparation\ntest",
             "Thermal\nvacuum &\nthermal\nbalance", "Final\nfunctional &\nmass\nproperties", "Shipment,\nlaunch-site\nprocessing,\nencapsulation"]
    w = 10.2
    for k, s in enumerate(steps):
        x = 1 + k * 11
        c = [GREY, BLUE, BLUE, VIOLET, RED, RED, ORANGE, GREEN, NAVY][k]
        box(ax, x, 12, w, 18, s, fc="white", ec=c, fs=6.2, lw=1.4)
        if k < len(steps) - 1:
            arrow(ax, (x + w, 21), (x + 11, 21), color=GREY, lw=0.8, ms=7)
    ax.text(1, 4, "Functional (\"aliveness\") tests are repeated after every environmental test to detect damage; "
            "a complete spacecraft test campaign typically\nlasts 6–18 months.", fontsize=6.8, color=GREY)
    save(fig, "ch04_ait_flow")


def mbse():
    fig, ax = canvas(7.2, 3.5, (0, 100), (0, 46))
    box(ax, 36, 18, 28, 12, "Central system model\n(SysML v2 repository)", fc=NAVY, ec=NAVY, color="white", fs=8,
        weight="bold")
    sats = [("Requirements\ndiagrams", 4, 34), ("Use cases &\nConOps", 36, 36), ("Structure\n(block definition,\ninternal block)", 70, 34),
            ("Behaviour\n(activity, state,\nsequence)", 4, 4), ("Parametrics\n(budgets, equations)", 36, 2),
            ("Analysis tools\n(CAD, FEM, thermal,\norbit, cost)", 70, 4)]
    for t, x, y in sats:
        box(ax, x, y, 26, 9, t, fc="#E8F1FA", ec=BLUE, fs=6.8)
        arrow(ax, (x + 13, y + 9 if y < 18 else y), (50, 30 if y > 18 else 18), color=GREY, lw=0.7, ms=6,
              style="<|-|>")
    save(fig, "ch04_mbse")


if __name__ == "__main__":
    vmodel(); lifecycle(); cost_commit(); trl(); req_tree(); mass_pie(); margins(); bathtub_and_redundancy()
    risk_matrix(); model_philosophy(); ait_flow(); mbse()
