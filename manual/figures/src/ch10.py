import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403

MU = 3.986004418e14
RE = 6371e3
G0 = 9.80665


def rho(h):
    return 1.225 * np.exp(-h / 7200.0)


def entry(V0, gam0_deg, beta, LD, h0=122e3, rn=1.0, dt=0.2, bank_eq=False):
    """2-D point-mass entry. beta = m/(Cd A) kg/m^2. Returns dict of time histories."""
    V, gam, h, s = V0, np.radians(gam0_deg), h0, 0.0
    out = {k: [] for k in ("t", "V", "h", "g", "q", "s")}
    t = 0
    while h > 5e3 and t < 4000:
        r = RE + h
        g = MU / r ** 2
        D = 0.5 * rho(h) * V ** 2 / beta
        L = D * LD
        if bank_eq:   # bank modulation: command vertical lift to null flight-path angle (equilibrium glide)
            Lcmd = (g - V ** 2 / r) * np.cos(gam) - 0.03 * gam * V
            L = float(np.clip(Lcmd, -D * LD, D * LD))
        dV = -D - g * np.sin(gam)
        dgam = (L - (g - V ** 2 / r) * np.cos(gam)) / V
        V += dV * dt
        gam += dgam * dt
        h += V * np.sin(gam) * dt
        s += V * np.cos(gam) * dt * RE / r
        t += dt
        qdot = 1.7415e-4 * np.sqrt(rho(h) / rn) * V ** 3 / 1e4   # W/cm^2 (Sutton-Graves)
        out["t"].append(t)
        out["V"].append(V)
        out["h"].append(h)
        out["g"].append(np.hypot(D, L) / G0)
        out["q"].append(qdot)
        out["s"].append(s)
    return {k: np.array(v) for k, v in out.items()}


def entry_profiles():
    cases = [("Ballistic capsule (L/D = 0), γ = −2.0°", 7800, -2.0, 400, 0.0, False, RED, 1.0),
             ("Lifting capsule (L/D = 0.3), γ = −1.5°", 7800, -1.5, 400, 0.3, False, BLUE, 2.0),
             ("Winged orbiter (L/D ≈ 1, bank-modulated)", 7600, -1.2, 330, 1.0, True, GREEN, 0.6),
             ("Lunar return capsule (effective L/D = 0.18), γ = −6.2°", 11000, -6.2, 450, 0.18, False, VIOLET, 4.7)]
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 3.2))
    res = {}
    for n, V0, g0, b, ld, eq, c, rn in cases:
        r = entry(V0, g0, b, ld, rn=rn, bank_eq=eq)
        res[n] = r
        axs[0].plot(r["V"] / 1000, r["h"] / 1000, color=c, label=n)
        axs[1].plot(r["t"] / 60, r["g"], color=c)
        axs[2].plot(r["t"] / 60, r["q"], color=c)
    axs[0].set_xlabel("Velocity (km/s)")
    axs[0].set_ylabel("Altitude (km)")
    axs[1].set_xlabel("Time from entry interface (min)")
    axs[1].set_ylabel("Deceleration (g)")
    axs[2].set_xlabel("Time from entry interface (min)")
    axs[2].set_ylabel("Stagnation heat flux (W/cm²)")
    axs[1].set_xlim(0, 30)
    axs[2].set_xlim(0, 30)
    fig.legend(loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=6.8)
    fig.tight_layout()
    fig.text(0.99, -0.17, "Computed for this manual: 2-D point-mass entry from 122 km, exponential atmosphere, Sutton–Graves "
             "stagnation heating; illustrative parameters.", ha="right", fontsize=6.0, color=GREY)
    save(fig, "ch10_entry_profiles")
    for n, r in res.items():
        print(f"{n}: peak g {r['g'].max():.1f}, peak q {r['q'].max():.0f} W/cm2, range {r['s'][-1]/1000:.0f} km")


def allen_eggers():
    gam = np.linspace(0.5, 15, 200)
    H = 7200.0
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for V, c, n in [(7800, BLUE, "LEO return, 7.8 km/s"), (11000, VIOLET, "Lunar return, 11.0 km/s"),
                    (12500, RED, "Mars return / sample capsules, 12.5 km/s")]:
        nmax = V ** 2 * np.sin(np.radians(gam)) / (2 * np.e * H * G0)
        ax.plot(gam, nmax, color=c, label=n)
    ax.axhspan(0, 8, color=GREEN, alpha=0.08)
    ax.text(0.7, 5.5, "tolerable for crews (< 8 g, eyeballs-in)", fontsize=7, color=GREEN)
    ax.set_xlabel("Entry flight-path angle |γ| (deg)")
    ax.set_ylabel("Peak deceleration (g)")
    ax.legend(fontsize=7)
    ax.set_ylim(0, 120)
    note(ax, "Allen–Eggers ballistic result: n_max = V_E² sin|γ| / (2 e H g₀), independent of the ballistic coefficient.",
         xy=(1, -0.16))
    save(fig, "ch10_allen_eggers")


def corridor():
    fig, ax = canvas(7.0, 3.6, (0, 100), (0, 48))
    ax.add_patch(Wedge((50, -150), 175, 60, 120, fc="#E8F1FA", ec="none"))
    ax.add_patch(Wedge((50, -150), 160, 60, 120, fc="white", ec="none"))
    earth_arc = np.linspace(np.radians(60), np.radians(120), 200)
    ax.plot(50 + 160 * np.cos(earth_arc), -150 + 160 * np.sin(earth_arc), color=EARTH, lw=3)
    ax.plot(50 + 175 * np.cos(earth_arc), -150 + 175 * np.sin(earth_arc), color=SKY, lw=1, ls="--")
    ax.text(10, 25.5, "entry interface ≈ 120 km", fontsize=6.8, color=SKY)
    x = np.linspace(2, 60, 100)
    ax.plot(x, 44 - 0.08 * (x - 2) ** 1.25, color=GREEN, lw=1.5)
    ax.plot(x, 44 - 0.18 * (x - 2) ** 1.2, color=GREEN, lw=1.5)
    ax.fill_between(x, 44 - 0.18 * (x - 2) ** 1.2, 44 - 0.08 * (x - 2) ** 1.25, color=GREEN, alpha=0.15)
    ax.text(30, 36.5, "safe entry corridor", fontsize=7.5, color=GREEN, weight="bold")
    xs = np.linspace(2, 95, 200)
    ax.plot(xs, 44 - 0.04 * (xs - 2) + 0.0035 * (xs - 50) ** 2 * (xs > 50), color=ORANGE, lw=1.3, ls="--")
    ax.text(72, 40, "too shallow:\nskips out or\noverheats on a\nlong path", fontsize=6.8, color=ORANGE)
    x2 = np.linspace(2, 35, 100)
    ax.plot(x2, 44 - 0.6 * (x2 - 2) ** 1.05, color=RED, lw=1.3, ls="--")
    ax.text(14, 16, "too steep:\nexcessive g-load\nand peak heating", fontsize=6.8, color=RED)
    ax.text(2, 46, "returning spacecraft", fontsize=7, color=NAVY)
    save(fig, "ch10_corridor")


def blunt_body():
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.8))
    for a in axs:
        a.set_xlim(0, 10)
        a.set_ylim(0, 6)
        a.set_aspect("equal")
        a.axis("off")
    a = axs[0]
    a.add_patch(Polygon([(3, 3), (9, 3.8), (9, 2.2)], fc="#C9D3DD", ec=NAVY))
    y = np.linspace(0.6, 5.4, 50)
    a.plot(3 + 0.9 * np.abs(y - 3) ** 1.6, y, color=RED, lw=1.5)
    a.text(0.5, 5.4, "Sharp body:\nattached oblique shock,\nhot gas close to the nose;\nheat flux ∝ 1/√(nose radius)",
           fontsize=6.6, va="top")
    a = axs[1]
    a.add_patch(Wedge((8.0, 3), 3.0, 140, 220, fc="#C9D3DD", ec=NAVY))
    a.add_patch(Polygon([(5.7, 4.9), (9.5, 4.0), (9.5, 2.0), (5.7, 1.1)], fc="#C9D3DD", ec=NAVY))
    a.plot(4.0 + 0.25 * (y - 3) ** 2, y, color=RED, lw=1.5)
    a.annotate("", xy=(4.0, 3), xytext=(4.95, 3), arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.8))
    a.text(3.5, 3.4, "shock\nstand-off", fontsize=6.2, color=GREY, ha="right")
    a.text(0.2, 5.9, "Blunt body (Allen & Eggers, 1951):\ndetached bow shock; most heat goes\ninto the shocked air, "
           "not the vehicle", fontsize=6.6, va="top")
    save(fig, "ch10_blunt")


def tps_materials():
    mats = [("Reinforced carbon-carbon (RCC)", 1650, 1600, RED), ("LI-900 silica tile (HRSI)", 1260, 144, NAVY),
            ("LI-2200 tile", 1260, 352, BLUE), ("FRCI-12 / AETB tiles", 1400, 192, SKY),
            ("TUFROC (X-37B nose)", 1700, 400, ORANGE), ("Nextel/AFRSI blankets", 650, 140, GREY),
            ("FRSI felt", 370, 100, GREY), ("PICA (Stardust, Mars 2020)", 2500, 260, GREEN),
            ("PICA-X / PICA-3 (Dragon)", 2500, 270, GREEN), ("Avcoat (Apollo, Orion)", 2800, 512, GOLD),
            ("SLA-561V (Mars landers)", 1800, 256, VIOLET), ("Carbon phenolic (Galileo probe)", 3300, 1450, "#8C564B"),
            ("3D-woven HEEET", 3000, 1000, "#E377C2"), ("Starship ceramic hex tiles", 1400, 300, "#17BECF")]
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    dy = {"PICA-X / PICA-3 (Dragon)": -130, "Starship ceramic hex tiles": -110, "FRCI-12 / AETB tiles": 40,
          "LI-2200 tile": -90}
    for n, T, d, c in mats:
        mk = "s" if T > 1800 else "o"
        ax.scatter(d, T, s=55, color=c, marker=mk, zorder=3, edgecolor="white")
        ax.text(d * 1.06, T + dy.get(n, 25), n, fontsize=6.5)
    ax.set_xscale("log")
    ax.set_xlim(80, 3000)
    ax.set_ylim(200, 3600)
    ax.set_xlabel("Density (kg/m³)")
    ax.set_ylabel("Approx. maximum surface temperature (°C)")
    ax.scatter([], [], marker="o", color=GREY, label="Reusable (insulators, RCC)")
    ax.scatter([], [], marker="s", color=GREY, label="Ablative (single use)")
    ax.legend(fontsize=7, loc="upper left")
    note(ax, "Representative values; ablators survive far higher heat fluxes than their surface temperatures suggest "
             "by consuming material.", xy=(1, -0.15))
    save(fig, "ch10_tps_materials")


def shuttle_tps():
    fig, ax = canvas(7.0, 3.8, (0, 100), (0, 52))
    body = [(8, 26), (14, 31), (60, 32), (72, 44), (88, 47), (92, 46), (86, 32), (96, 30), (96, 22), (86, 20),
            (92, 6), (88, 5), (72, 8), (60, 20), (14, 21)]
    ax.add_patch(Polygon(body, closed=True, fc="#1B1F24", ec=NAVY, lw=1))
    ax.add_patch(Polygon([(60, 32), (72, 44), (88, 47), (85, 33)], fc="#2F3640", ec="none"))
    ax.add_patch(Polygon([(60, 20), (72, 8), (88, 5), (85, 19)], fc="#2F3640", ec="none"))
    ax.add_patch(Polygon([(8, 26), (14, 31), (16, 26), (14, 21)], fc="#7F8C8D", ec="none"))
    ax.plot([60, 72, 88], [32, 44, 47], color="#9AA5B1", lw=4)
    ax.plot([60, 72, 88], [20, 8, 5], color="#9AA5B1", lw=4)
    ax.text(3, 46, "Orbiter underside (schematic)", fontsize=8, weight="bold", color=NAVY)
    legend = [("#9AA5B1", "RCC: nose cap & wing leading edges (> 1 260 °C)"),
              ("#1B1F24", "HRSI black tiles (LI-900/2200), underside (≤ 1 260 °C)"),
              ("#F2F2F2", "LRSI white tiles & AFRSI blankets, upper surfaces (≤ 650 °C)"),
              ("#E9D8A6", "FRSI felt, payload bay doors & upper wing (≤ 370 °C)")]
    for k, (c, t) in enumerate(legend):
        ax.add_patch(Rectangle((3, 14 - k * 4), 3, 2.5, fc=c, ec=GREY, lw=0.5))
        ax.text(7.5, 15.2 - k * 4, t, fontsize=6.6, va="center")
    ax.text(50, 49, "≈ 24 300 tiles, ≈ 2 300 blankets, 44 RCC panels", fontsize=7, color=GREY, ha="center")
    save(fig, "ch10_shuttle_tps")


def reuse_econ():
    N = np.arange(1, 51)
    build = 100.0
    ops = 10.0
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.axhline(build + ops, color=GREY, ls="--", lw=1)
    ax.text(12, build + ops - 7, "expendable: build + operations every flight", fontsize=7, color=GREY)
    for frac, c in [(0.02, GREEN), (0.1, BLUE), (0.3, ORANGE), (0.6, RED)]:
        cost = build / N + frac * build + ops
        ax.plot(N, cost, color=c, label=f"refurbishment {int(frac * 100)} % of build cost per flight")
    ax.set_xlabel("Number of flights per vehicle")
    ax.set_ylabel("Average cost per flight (expendable = 110)")
    ax.legend(fontsize=7, loc="center right")
    ax.set_ylim(0, 125)
    note(ax, "Simple model: reuse pays only if refurbishment and operations are cheap; the Space Shuttle's high refurbishment "
             "effort limited its savings.", xy=(1, -0.16))
    save(fig, "ch10_reuse_econ")


def timeline():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    progs = [("X-15", 1959, 1968, GREY), ("X-20 Dyna-Soar (cancelled)", 1957, 1963, GREY), ("Space Shuttle", 1981, 2011, BLUE),
             ("Buran (1 flight)", 1988, 1988.6, RED), ("HOPE-X / HYFLEX (Japan)", 1994, 2003, GREEN),
             ("X-37B (USAF/USSF)", 2010, 2026.8, NAVY), ("Shenlong / CSSHQ (China)", 2020, 2026.8, GOLD),
             ("ISRO RLV-TD / LEX", 2016, 2026.8, ORANGE), ("IXV (ESA, 1 flight)", 2015, 2015.6, VIOLET),
             ("Dream Chaser (first flight planned)", 2026.7, 2028, SKY), ("Space Rider (planned)", 2028, 2030, VIOLET),
             ("SpaceShipOne / Two (suborbital)", 2004, 2024.5, "#8C564B")]
    for k, (n, a, b, c) in enumerate(progs):
        ax.barh(k, b - a, left=a, color=c, height=0.6, alpha=0.9 if "planned" not in n else 0.4)
        ax.text(b + 0.7 if b < 2018 else a - 0.7, k, n, va="center", fontsize=6.8, ha="left" if b < 2018 else "right")
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_xlim(1955, 2031)
    ax.axvline(2026.8, color=RED, ls=":", lw=0.8)
    ax.text(2026.9, -0.7, "Oct 2026", fontsize=6.6, color=RED)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Year")
    save(fig, "ch10_timeline")


def entry_speeds():
    items = [("Space Shuttle (LEO)", 7.8, BLUE), ("Soyuz / Crew Dragon (LEO)", 7.8, BLUE),
             ("Apollo / Orion (lunar return)", 11.0, VIOLET), ("Hayabusa2 capsule", 11.7, GREEN),
             ("OSIRIS-REx capsule", 12.4, GREEN), ("Stardust capsule", 12.9, GREEN), ("Mars entry (Perseverance)", 5.4, RED),
             ("Titan entry (Huygens)", 6.0, GOLD), ("Venus entry (Pioneer Venus probes)", 11.6, ORANGE),
             ("Jupiter entry (Galileo probe)", 47.4, "#8C564B")]
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    hbar(ax, [i[0] for i in items], [i[1] for i in items], fmt="{:.1f} km/s", color=SKY)
    for k, (_, v, c) in enumerate(items):
        ax.barh(k, v, color=c, height=0.65)
    ax.set_xscale("log")
    ax.set_xlim(3, 90)
    ax.set_xlabel("Entry speed relative to the atmosphere (km/s, log scale)")
    save(fig, "ch10_entry_speeds")


def rate_load():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    pts = [("Space Shuttle\n(RCC nose)", 60, 40, BLUE), ("Soyuz", 140, 35, BLUE), ("Crew Dragon", 120, 30, BLUE),
           ("Apollo", 470, 200, VIOLET), ("Orion (Artemis I)", 450, 180, VIOLET), ("Stardust", 1200, 290, GREEN),
           ("Mars Science Lab.", 200, 60, RED), ("Huygens (Titan)", 140, 30, GOLD), ("Galileo probe", 30000, 200000, "#8C564B"),
           ("Pioneer Venus large probe", 4500, 11000, ORANGE)]
    for n, q, Q, c in pts:
        ax.scatter(q, Q, s=60, color=c, zorder=3, edgecolor="white")
        ax.text(q * 1.15, Q * 1.05, n, fontsize=6.6)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(20, 1e5)
    ax.set_ylim(10, 1e6)
    ax.set_xlabel("Peak stagnation heat flux (W/cm²) → drives material choice")
    ax.set_ylabel("Integrated heat load (J/cm²) → drives TPS thickness")
    ax.axvspan(20, 120, color=GREEN, alpha=0.06)
    ax.text(22, 4e5, "reusable\ninsulators\nfeasible", fontsize=6.8, color=GREEN)
    ax.text(3000, 30, "ablators required", fontsize=6.8, color=RED)
    note(ax, "Approximate published values; illustrative of the two quantities that size a heat shield.", xy=(1, -0.15))
    save(fig, "ch10_rate_load")


def landing_systems():
    fig, ax = canvas(7.2, 2.8, (0, 100), (0, 36))
    items = [("Parachutes →\nwater", "Apollo, Orion,\nCrew Dragon,\nStarliner (land, airbags)", BLUE),
             ("Parachutes +\nretro-rockets", "Soyuz, Shenzhou\n(solid motors at ≈ 1 m),\nMengzhou", GREEN),
             ("Parafoil", "Space Rider, X-38\n(test), cargo return\ncapsules", VIOLET),
             ("Runway\nglide", "Shuttle, Buran,\nX-37B, Dream Chaser,\nShenlong", ORANGE),
             ("Propulsive", "Starship, Falcon 9\nbooster, New Shepard\nbooster, lunar landers", RED)]
    for k, (t, b, c) in enumerate(items):
        title_box(ax, 1 + k * 19.8, 4, 18.5, 28, t, b, hc=c, ec=c, fc="white", fs=6.0, tfs=6.8)
    save(fig, "ch10_landing")


if __name__ == "__main__":
    entry_speeds(); landing_systems()
    entry_profiles(); allen_eggers(); corridor(); blunt_body(); tps_materials(); shuttle_tps(); reuse_econ(); timeline()
