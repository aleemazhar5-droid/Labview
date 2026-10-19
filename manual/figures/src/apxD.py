import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Rectangle

DATA = Path(__file__).resolve().parents[2] / "data/itu_attenuation.json"

IEEE = [("L", 1, 2), ("S", 2, 4), ("C", 4, 8), ("X", 8, 12), ("Ku", 12, 18), ("K", 18, 27), ("Ka", 27, 40),
        ("V", 40, 75), ("W", 75, 110)]


def atten():
    d = json.loads(DATA.read_text())
    f = np.array(d["f"])
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(6.9, 3.3), gridspec_kw={"width_ratios": [1.35, 1]})
    ax.semilogy(f, d["std"], color=BLUE, lw=1.3, label="Standard atmosphere (7.5 g/m³ water vapour)")
    ax.semilogy(f, d["dry"], color=ORANGE, lw=1.0, ls="--", label="Dry air (oxygen only)")
    ax.set_xlim(0, 350)
    ax.set_ylim(0.02, 4000)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Zenith attenuation (dB)")
    for x, y, t in [(22.2, 0.9, "H₂O\n22.2 GHz"), (60, 230, "O₂ 60 GHz"), (118.75, 160, "O₂ 118.75"),
                    (183.3, 115, "H₂O 183.3")]:
        ax.annotate(t, (x, y), ha="center", va="bottom", fontsize=6.2, color=INK)
    for x, t in [(35, "35 GHz\nwindow"), (94, "94 GHz\nwindow"), (140, "140 GHz\nwindow")]:
        ax.annotate(t, (x, 0.035), ha="center", va="bottom", fontsize=5.9, color=GREY)
    ax.legend(loc="upper right", fontsize=6.0, frameon=False)
    ax.set_title("Clear-sky gases, looking straight up", fontsize=8)
    ax.grid(alpha=0.25, which="both", lw=0.4)

    fr = np.array(d["frain"])
    for R, c in [(5, SKY), (25, BLUE), (100, NAVY)]:
        bx.loglog(fr, d[f"rain{R}"], color=c, lw=1.3, label=f"{R} mm/h")
    bx.set_xlim(1, 100)
    bx.set_ylim(1e-3, 300)
    bx.set_xlabel("Frequency (GHz)")
    bx.set_ylabel("Specific rain attenuation (dB/km)")
    bx.set_title("Rain", fontsize=8)
    bx.legend(title="Rain rate", fontsize=6.0, title_fontsize=6.2, frameon=False, loc="lower right")
    bx.grid(alpha=0.25, which="both", lw=0.4)
    for name, lo, hi in IEEE:
        if hi <= 100:
            bx.axvspan(lo, hi, ymin=0.94, ymax=1.0, color=LIGHT if IEEE.index((name, lo, hi)) % 2 else "#d9e2ef", lw=0)
            bx.text(np.sqrt(lo * hi), 190, name, ha="center", va="center", fontsize=5.9, color=INK)
    fig.text(0.99, 0.01, "Gases: ITU-R P.676 line-by-line model, sea level, 1013 hPa, 15 °C. Rain: ITU-R P.838, "
             "40° elevation, circular polarisation. Computed with ITU-Rpy.", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "apxD_atten")


SERVICES = [
    # (label, lo GHz, hi GHz, row, colour)
    ("VHF/UHF amateur & CubeSat TT&C", 0.144, 0.438, 0, GREEN),
    ("UHF military satcom", 0.24, 0.40, 1, RED),
    ("GNSS (L1/L2/L5, E1/E5/E6, B1/B2/B3)", 1.164, 1.61, 2, VIOLET),
    ("L-band mobile (Inmarsat, Iridium)", 1.518, 1.6605, 3, ORANGE),
    ("S-band TT&C (2.025–2.29)", 2.025, 2.29, 4, NAVY),
    ("C-band FSS (3.7–4.2 / 5.925–6.425)", 3.7, 6.425, 5, BLUE),
    ("X-band EO downlink, deep space, military", 7.25, 8.5, 6, NAVY),
    ("Ku FSS/BSS, Starlink user links", 10.7, 14.5, 7, BLUE),
    ("Ka commercial & military", 17.7, 31.0, 8, BLUE),
    ("Deep-space Ka (31.8–32.3 / 34.2–34.7)", 31.8, 34.7, 9, NAVY),
    ("Q/V feeder links", 37.5, 51.4, 10, SKY),
    ("E-band (71–76 / 81–86)", 71, 86, 11, SKY),
]
SAR = [("P", 0.435), ("L", 1.26), ("S", 3.2), ("C", 5.405), ("X", 9.65), ("Ku", 13.5), ("Ka", 35.75)]


def bandmap():
    fig, ax = plt.subplots(figsize=(6.9, 3.6))
    ax.set_xscale("log")
    ax.set_xlim(0.1, 110)
    n = len(SERVICES)
    ax.set_ylim(-2.3, n + 0.9)
    for i, (name, lo, hi) in enumerate(IEEE):
        ax.add_patch(Rectangle((lo, n + 0.05), hi - lo, 0.7, color=LIGHT if i % 2 else "#d9e2ef", lw=0))
        ax.text(np.sqrt(lo * hi), n + 0.4, name, ha="center", va="center", fontsize=6.4, color=INK, weight="bold")
    ax.text(0.31, n + 0.4, "VHF / UHF", ha="center", va="center", fontsize=6.4, color=INK, weight="bold")
    ax.add_patch(Rectangle((0.1, n + 0.05), 0.9, 0.7, color="#eef1f5", lw=0))
    for lbl, lo, hi, row, c in SERVICES:
        y = n - 1 - row
        ax.add_patch(Rectangle((lo, y - 0.32), hi - lo, 0.64, color=c, alpha=0.85, lw=0))
        right = hi < 3
        ax.text(hi * 1.12 if right else lo / 1.12, y, lbl, ha="left" if right else "right", va="center",
                fontsize=6.0, color=INK)
    for name, fc in SAR:
        ax.plot([fc], [-1.25], marker="v", color=RED, ms=5)
        ax.text(fc, -1.75, name, ha="center", va="center", fontsize=6.0, color=RED)
    ax.text(0.105, -1.25, "SAR bands", ha="left", va="center", fontsize=6.0, color=RED)
    for fc, t in [(1.4135, "1.4 GHz\nSMOS/SMAP"), (23.8, "23.8"), (54.0, "50–58\nO₂ sounding")]:
        ax.plot([fc], [-0.5], marker="o", color=GREEN, ms=3.5)
        ax.text(fc * 1.1, -0.5, t.replace("\n", " "), ha="left", va="center", fontsize=5.8, color=GREEN)
    ax.text(0.105, -0.5, "Passive radiometry", ha="left", va="center", fontsize=6.0, color=GREEN)
    ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel("Frequency (GHz, logarithmic)")
    ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100])
    ax.set_xticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10", "20", "50", "100"])
    fig.text(0.99, 0.01, "Approximate band edges; exact allocations depend on ITU Region and service "
             "(ITU Radio Regulations, Article 5).", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "apxD_bandmap")


if __name__ == "__main__":
    fns = [atten, bandmap]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
