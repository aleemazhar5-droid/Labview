"""Figures for Chapter 42 — Advanced Propulsion."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge  # noqa: F401
from scipy.optimize import least_squares
from scipy.integrate import solve_ivp

G0 = 9.80665
C = 2.99792458e8
MU_S = 1.32712440018e20
AU = 1.495978707e11
MU_E, MU_M = 3.986004418e14, 4.282837e13
R_E, R_M = 6378e3, 3396e3
R_MARS_ORB = 1.523679 * AU


# ---------------------------------------------------------------------------------------------
# 1. The tyranny of the rocket equation
# ---------------------------------------------------------------------------------------------
TECH = [("Chemical H₂/O₂ (450 s)", 450, NAVY), ("Nuclear thermal (900 s)", 900, ORANGE),
        ("Hall thruster (2 000 s)", 2000, GREEN), ("Gridded ion (4 000 s)", 4000, BLUE),
        ("Fusion concept (10 000 s)", 10000, VIOLET)]


def rocketeq():
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.45, 1.0]))
    dv = np.linspace(0, 60, 400)
    for name, isp, col in TECH:
        ve = isp * G0 / 1000
        a.plot(dv, np.exp(dv / ve), color=col, lw=1.7, label=name)
    a.axhspan(10, 1000, color="#F6E3E3", zorder=0)
    a.text(31.5, 900, "mass ratio > 10:\nover 90 % propellant", ha="left", va="top", fontsize=6.3, color=RED)
    inl = [(26.0, 420, "chemical\n450 s", NAVY, "right"), (46.5, 240, "nuclear thermal 900 s", ORANGE, "right"),
           (59.5, 28.0, "Hall 2 000 s", GREEN, "right"), (59.5, 5.6, "gridded ion 4 000 s", BLUE, "right"),
           (59.5, 2.05, "fusion concept 10 000 s", VIOLET, "right")]
    for x, y, t, col, ha in inl:
        a.text(x, y, t, fontsize=6.5, color=col, ha=ha, va="center", weight="bold")
    for x, t in [(4.5, "LEO → Mars orbit (Hohmann)"), (11, "Dawn's total Δv")]:
        a.axvline(x, color=GREY, lw=0.8, ls="--", zorder=1)
        a.text(x - 0.6, 22, t, fontsize=6.1, color=GREY, va="bottom", ha="right", rotation=90)
    a.axvline(38, color=GREY, lw=0.8, ls="--", zorder=1)
    a.text(38.6, 1.05, "≈ 70-day Mars trip (low thrust)", fontsize=6.1, color=GREY, va="bottom", ha="left")
    a.set_yscale("log")
    a.set_ylim(1, 1000)
    a.set_xlim(0, 60)
    a.set_xlabel("Velocity change Δv (km/s)")
    a.set_ylabel("Mass ratio  m₀ / m_f")
    a.set_title("(a) Mass ratio  e^(Δv / v_e)", fontsize=8.6)

    names = ["Chemical", "Nuclear thermal", "Hall", "Gridded ion", "Fusion concept"]
    vals = [isp * G0 / 1000 * np.log(3) for _, isp, _ in TECH]
    y = np.arange(len(names))
    b.barh(y, vals, color=[t[2] for t in TECH], height=0.6, zorder=2)
    for yi, v in zip(y, vals):
        b.text(v * 1.08, yi, f"{v:.0f} km/s" if v > 10 else f"{v:.1f} km/s", va="center", fontsize=6.8)
    b.set_xscale("log")
    b.set_xlim(1, 600)
    b.set_yticks(y)
    b.set_yticklabels(names, fontsize=7.2)
    b.invert_yaxis()
    b.grid(axis="y", visible=False)
    b.set_xlabel("Δv for mass ratio 3 (km/s)")
    b.set_title("(b) Δv when ⅔ of the mass is propellant", fontsize=8.6)
    fig.text(0.99, 0.01, "Ideal rocket equation, v_e = g₀ I_sp. Reference Δv values: Hohmann transfer from 400 km LEO to a "
             "1-sol Mars orbit (this chapter's model);\nDawn ≈ 11 km/s; 70-day trip from the power-limited model in this "
             "chapter.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    save(fig, "ch42_rocketeq")


# ---------------------------------------------------------------------------------------------
# 2. Thrust versus specific impulse map with lines of constant jet power
# ---------------------------------------------------------------------------------------------
def ptmap():
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    boxes = [  # name, isp range, thrust range (N), colour, label position (isp, thrust), ha
        ("Cold gas", (40, 75), (1e-3, 10), GREY, (52, 2.4e1), "center"),
        ("Chemical thrusters", (200, 330), (0.1, 500), NAVY, (300, 1.2e3), "center"),
        ("Launch engines", (280, 465), (2e4, 1e7), NAVY, (360, 2.2e7), "center"),
        ("Nuclear thermal", (800, 950), (2e4, 1e6), ORANGE, (1500, 3.0e5), "left"),
        ("Arcjets, resistojets", (300, 800), (0.01, 0.5), SKY, (330, 3.0e-3), "left"),
        ("Hall", (1200, 3000), (5e-3, 5.4), GREEN, (1290, 0.05), "left"),
        ("Gridded ion", (2500, 4500), (1e-3, 0.25), BLUE, (2500, 3.4e-4), "left"),
        ("MPD (pulsed / steady)", (1500, 6000), (1, 100), RED, (1700, 3.0e2), "left"),
        ("VASIMR (ground tests)", (3000, 30000), (0.5, 6), VIOLET, (15000, 0.2), "center"),
        ("FEEP, electrospray", (1000, 10000), (1e-6, 1e-3), GOLD, (3200, 3.0e-7), "center"),
        ("Fusion concepts", (1e4, 1e6), (1, 1e5), "#8C564B", (1e5, 3e5), "center"),
    ]
    for name, (i0, i1), (f0, f1), col, (lx, ly), ha in boxes:
        ax.add_patch(Rectangle((i0, f0), i1 - i0, f1 - f0, fc=col, ec=col, alpha=0.28, lw=1.0, zorder=2))
        ax.add_patch(Rectangle((i0, f0), i1 - i0, f1 - f0, fc="none", ec=col, alpha=0.9, lw=0.9, zorder=3))
        ax.text(lx, ly, name, fontsize=6.6, color=col if col not in (GOLD, SKY) else INK, ha=ha, va="center", zorder=5,
                weight="bold")
    isp = np.logspace(1, 6.3, 50)
    for P, lab, xi in [(1, "1 W", 1.4e6), (1e3, "1 kW", 1.4e6), (1e6, "1 MW", 1.4e6), (1e9, "1 GW", 1.4e6),
                       (1e12, "jet power 1 TW", 3.0e5)]:
        F = 2 * P / (G0 * isp)
        ax.plot(isp, F, color=GREY, lw=0.7, ls=":", zorder=1)
        ax.text(xi, 2 * P / (G0 * xi) * 1.6, lab, fontsize=6.2, color=GREY, rotation=-24,
                ha="center", va="bottom")
    ax.text(1.9e6, 3.2e-2, "solar sails: no propellant, I_sp → ∞\n(1 km² sail at 1 AU ≈ 8 N)", fontsize=6.4,
            color=INK, ha="right", va="center", bbox=dict(fc="white", ec="none", pad=1.0))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(20, 2e6)
    ax.set_ylim(1e-7, 1e8)
    ax.set_xlabel("Specific impulse I_sp (s)")
    ax.set_ylabel("Thrust per engine (N)")
    fig.text(0.99, 0.01, "Indicative ranges of flown or ground-tested devices (fusion: design studies only).\nDotted lines: "
             "jet power P = F g₀ I_sp / 2 — high thrust at high I_sp needs enormous power.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.065, 1, 1))
    save(fig, "ch42_ptmap")


# ---------------------------------------------------------------------------------------------
# 3. Power-limited trajectories: Mars trip time versus specific power
# ---------------------------------------------------------------------------------------------
def vsi_transfer(T, phi0, n=160):
    """Minimum J = ∫|a|² dt for a heliocentric rendezvous from Earth's circular orbit (1 AU) to Mars's (coplanar,
    circular), by direct transcription (finite differences, free arrival angle). Returns J, Δv, arrival angle."""
    h = T / n
    r1, r2 = AU, R_MARS_ORB
    v1, v2 = np.sqrt(MU_S / r1), np.sqrt(MU_S / r2)
    R0, V0 = np.array([r1, 0.0]), np.array([0.0, v1])

    def unpack(x):
        phi = x[-1]
        P = x[:-1].reshape(n - 1, 2)
        RN = r2 * np.array([np.cos(phi), np.sin(phi)])
        VN = v2 * np.array([-np.sin(phi), np.cos(phi)])
        return np.vstack([R0, P, RN]), VN

    w = np.full(n + 1, h)
    w[0] = w[-1] = h / 2

    def res(x):
        R, VN = unpack(x)
        g = -MU_S * R / np.linalg.norm(R, axis=1)[:, None] ** 3
        a = np.zeros_like(R)
        a[1:-1] = (R[2:] - 2 * R[1:-1] + R[:-2]) / h ** 2 - g[1:-1]
        a[0] = (2 * R[1] - 2 * R[0] - 2 * h * V0) / h ** 2 - g[0]
        a[-1] = (2 * R[-2] - 2 * R[-1] + 2 * h * VN) / h ** 2 - g[-1]
        return (a * np.sqrt(w)[:, None]).ravel()

    s = np.linspace(0, 1, n + 1)[1:-1]
    r = r1 + (r2 - r1) * (3 * s ** 2 - 2 * s ** 3)
    th = phi0 * s
    x0 = np.r_[np.c_[r * np.cos(th), r * np.sin(th)].ravel(), phi0]
    sol = least_squares(res, x0, x_scale=np.r_[np.full(2 * (n - 1), AU), 1.0], xtol=1e-12, ftol=1e-12,
                        max_nfev=300)
    a = sol.fun.reshape(n + 1, 2)
    J = float(np.sum(a ** 2))
    dv = float(np.sum(np.linalg.norm(a, axis=1) * np.sqrt(w)))
    return J, dv, sol.x[-1]


TRIP_DAYS = [40, 50, 60, 70, 85, 100, 120, 140, 160, 190, 220, 260, 300, 360, 420, 500]
_VSI = {}


def vsi_table():
    if not _VSI:
        for d in TRIP_DAYS:
            _VSI[d] = vsi_transfer(d * 86400.0, np.radians(d * 0.75))
    return _VSI


def neptrip():
    tab = vsi_table()
    days = np.array(TRIP_DAYS, float)
    J = np.array([tab[d][0] for d in TRIP_DAYS])
    eta = 0.6
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.35, 1.0]))
    bands = [(3, 10, "kilowatt-class\nreactors", "#E9E4F2"), (20, 60, "solar electric\nat 1 AU", "#E2F0E6"),
             (1000, 10000, "claimed for\nVASIMR-class\nfast trips;\nfusion concepts", "#F6E3E3")]
    for x0, x1, t, col in bands:
        a.axvspan(x0, x1, color=col, zorder=0)
        a.text(np.sqrt(x0 * x1), 640, t, ha="center", va="top", fontsize=6.0, color=INK, linespacing=1.1)
    for mL, col, ls in [(0.5, BLUE, "-"), (0.3, ORANGE, "--"), (0.1, GREEN, ":")]:
        alpha = J / (2 * eta * (1 - np.sqrt(mL)) ** 2)
        a.plot(alpha, days, color=col, ls=ls, lw=1.8, label=f"payload fraction {mL:.0%}".replace("%", " %"))
    a.set_xscale("log")
    a.set_xlim(2, 3e4)
    a.set_ylim(0, 650)
    a.set_xlabel("Specific power α (W per kg of power and propulsion system)")
    a.set_ylabel("One-way trip time (days)")
    a.set_title("(a) Earth–Mars trip time versus specific power", fontsize=8.6)
    a.legend(loc="center right", fontsize=6.6)
    dv = np.array([tab[d][1] for d in TRIP_DAYS]) / 1000
    b.plot(days, dv, color=NAVY, lw=1.8, marker="o", ms=3)
    b.axhline(5.65, color=GREY, ls="--", lw=0.8)
    b.text(495, 1.6, "slow-spiral limit 5.65 km/s", ha="right", va="bottom", fontsize=6.3, color=GREY)
    b.set_xlabel("One-way trip time (days)")
    b.set_ylabel("Low-thrust Δv (km/s)")
    b.set_xlim(0, 520)
    b.set_ylim(0, 72)
    b.set_title("(b) Velocity change needed", fontsize=8.6)
    fig.text(0.99, 0.01, "Optimal variable-I_sp power-limited rendezvous, Earth escape to Mars capture (coplanar circular "
             "orbits, planetary spirals excluded);\nJ = ∫a²dt by direct optimisation; payload fraction = (1 − √(J/2ηα))², "
             "η = 0.6. Shaded bands are indicative.", ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    save(fig, "ch42_neptrip")


# ---------------------------------------------------------------------------------------------
# 4. Schematic: nuclear thermal and nuclear electric propulsion
# ---------------------------------------------------------------------------------------------
def ntpnep():
    fig, ax = canvas(7.0, 3.5, xlim=(0, 140), ylim=(0, 70))
    # ---- (a) NTP
    label(ax, 3, 68.5, "(a) Nuclear thermal rocket", fs=8.6, weight="bold", color=NAVY, ha="left")
    ax.add_patch(FancyBboxPatch((4, 42), 22, 21, boxstyle="round,pad=0,rounding_size=4", fc="#DCEBFA", ec=NAVY,
                                lw=1.0, zorder=2))
    label(ax, 15, 52.5, "liquid\nhydrogen\ntank\n20 K", fs=7.0)
    ax.plot([26, 33], [52.5, 52.5], color=BLUE, lw=2.0, zorder=1)
    ax.add_patch(Circle((36, 52.5), 3.4, fc="#C8D3DD", ec=NAVY, lw=0.9, zorder=3))
    label(ax, 36, 52.5, "TP", fs=6.6, weight="bold")
    label(ax, 36, 58.2, "turbopump", fs=6.2, color=GREY)
    ax.add_patch(Rectangle((44, 43), 4, 19, fc="#8E9AA6", ec=NAVY, lw=0.8, zorder=3))
    label(ax, 45, 40.6, "shield", fs=6.2, color=GREY)
    ax.add_patch(Rectangle((48, 43), 14, 19, fc="#F2C9A0", ec=NAVY, lw=0.9, zorder=3))
    for k in range(6):
        ax.add_patch(Rectangle((49.2 + k * 2.1, 44.5), 1.2, 16, fc=ORANGE, ec="none", zorder=4))
    ax.add_patch(Circle((62, 43), 1.4, fc=GREY, ec=NAVY, lw=0.6, zorder=5))
    ax.add_patch(Circle((62, 62), 1.4, fc=GREY, ec=NAVY, lw=0.6, zorder=5))
    label(ax, 61, 66.0, "reactor core: uranium fuel\n≈ 2 500–2 800 K", fs=6.3)
    label(ax, 58.5, 40.3, "control drums", fs=6.2, color=GREY)
    ax.add_patch(Polygon([(62, 48), (62, 57), (67, 55), (76, 62), (76, 43), (67, 50)], closed=True, fc="#D7DDE3",
                         ec=NAVY, lw=0.9, zorder=3))
    for dy in (-5, 0, 5):
        arrow(ax, (77, 52.5 + dy * 0.6), (85, 52.5 + dy * 1.1), color=ORANGE, lw=1.2, ms=7)
    label(ax, 87, 52.5, "hot H₂\n≈ 9 km/s", fs=6.6, color=ORANGE, ha="left")
    arrow(ax, (36, 49.1), (36, 36.5), color=BLUE, lw=1.0, ms=7, style="-")
    ax.plot([36, 71, 71], [36.5, 36.5, 44.5], color=BLUE, lw=1.0, zorder=2)
    arrow(ax, (71, 40), (71, 44.6), color=BLUE, lw=1.0, ms=7)
    label(ax, 53.5, 34.2, "H₂ cools the nozzle walls, then flows through the core", fs=6.2, color=BLUE)
    label(ax, 122, 53, "Thrust from heat\nhigh thrust (10⁴–10⁶ N)\nI_sp ≈ 850–950 s\nburns of minutes", fs=6.6,
          color=INK)
    label(ax, 122, 12, "Thrust from electricity\nlow thrust (≈ 1 N per 20 kW)\nI_sp ≈ 2 000–5 000 s\nthrusting for months",
          fs=6.6, color=INK)
    ax.plot([105, 105], [4, 66], color="#D5DDE5", lw=0.8)
    # ---- (b) NEP
    label(ax, 3, 27.5, "(b) Nuclear electric propulsion", fs=8.6, weight="bold", color=NAVY, ha="left")
    blocks = [(2, 13, "fission\nreactor", "#F2C9A0"), (18, 9, "shield", "#C3CBD3"),
              (30, 16, "power\nconversion\n(Brayton)", LIGHT), (50, 14, "power\nprocessing\nunit", LIGHT),
              (68, 15, "electric\nthrusters", "#DFF0E4")]
    for x, w, t, col in blocks:
        box(ax, x, 3, w, 13, t, fc=col, fs=6.5, r=1.0)
    for x0, x1 in [(15, 18), (27, 30), (46, 50), (64, 68)]:
        arrow(ax, (x0, 9.5), (x1, 9.5), color=NAVY, lw=1.0, ms=7)
    box(ax, 68, 19, 15, 6.5, "xenon tank", fc="#DCEBFA", fs=6.5, r=1.0)
    arrow(ax, (75.5, 19), (75.5, 16), color=NAVY, lw=1.0, ms=7)
    ax.add_patch(Polygon([(32, 17.4), (44, 17.4), (47, 22), (35, 22)], fc="#BFD5E9", ec=NAVY, lw=0.7, zorder=2))
    label(ax, 30, 19.8, "radiator rejects\n≈ 70–80 % of the heat", fs=6.2, color=GREY, ha="right")
    for dy in (-3.5, 0, 3.5):
        arrow(ax, (84, 9.5 + dy), (93, 9.5 + dy * 1.4), color=GREEN, lw=1.2, ms=7)
    label(ax, 95, 9.5, "ions\n20–50\nkm/s", fs=6.4, color=GREEN, ha="left")
    save(fig, "ch42_ntpnep")


# ---------------------------------------------------------------------------------------------
# 5. Mars transit: chemical versus nuclear thermal (Lambert transfers)
# ---------------------------------------------------------------------------------------------
def _stumpff(z):
    if z > 1e-8:
        s = np.sqrt(z)
        return (1 - np.cos(s)) / z, (s - np.sin(s)) / s ** 3
    if z < -1e-8:
        s = np.sqrt(-z)
        return (np.cosh(s) - 1) / (-z), (np.sinh(s) - s) / s ** 3
    return 0.5, 1 / 6


def lambert(R1, R2, t, mu):
    r1n, r2n = np.linalg.norm(R1), np.linalg.norm(R2)
    dth = np.arccos(np.clip(np.dot(R1, R2) / r1n / r2n, -1, 1))
    if np.cross(R1, R2)[2] < 0:
        dth = 2 * np.pi - dth
    A = np.sin(dth) * np.sqrt(r1n * r2n / (1 - np.cos(dth)))

    def y(z):
        Cz, Sz = _stumpff(z)
        return r1n + r2n + A * (z * Sz - 1) / np.sqrt(Cz)

    def F(z):
        Cz, Sz = _stumpff(z)
        yy = y(z)
        return (yy / Cz) ** 1.5 * Sz + A * np.sqrt(yy) - np.sqrt(mu) * t

    zl, zu = -4 * np.pi ** 2, 4 * np.pi ** 2 * 0.999
    while y(zl) < 0:
        zl += 0.1
    fl, fu = F(zl), F(zu)
    if fl * fu > 0:
        return None
    for _ in range(120):
        zm = 0.5 * (zl + zu)
        fm = F(zm)
        if fl * fm <= 0:
            zu, fu = zm, fm
        else:
            zl, fl = zm, fm
    z = 0.5 * (zl + zu)
    yy = y(z)
    f = 1 - yy / r1n
    g = A * np.sqrt(yy / mu)
    gd = 1 - yy / r2n
    return (R2 - f * R1) / g, (gd * R2 - R1) / g


def mars_dv(tof_days):
    """Refined search: coarse 1° grid, then 0.05° around the best transfer angle."""
    b0 = _mars_dv(tof_days, np.arange(50, 310, 1.0))
    return _mars_dv(tof_days, np.arange(b0[3] - 1.5, b0[3] + 1.5, 0.05))


def _mars_dv(tof_days, grid):
    """Minimum TMI + MOI (km/s) over transfer angle: 400 km circular LEO → 250 × 33 793 km (1-sol) Mars orbit."""
    best = None
    t = tof_days * 86400.0
    r1, r2 = AU, R_MARS_ORB
    for th in np.radians(grid):
        if abs(th - np.pi) < np.radians(1.5):
            continue
        R1 = np.array([r1, 0, 0])
        R2 = r2 * np.array([np.cos(th), np.sin(th), 0])
        s = lambert(R1, R2, t, MU_S)
        if s is None:
            continue
        V1, V2 = s
        vE = np.sqrt(MU_S / r1) * np.array([0, 1, 0])
        vM = np.sqrt(MU_S / r2) * np.array([-np.sin(th), np.cos(th), 0])
        vi1, vi2 = np.linalg.norm(V1 - vE), np.linalg.norm(V2 - vM)
        rp = R_E + 400e3
        dv1 = np.sqrt(vi1 ** 2 + 2 * MU_E / rp) - np.sqrt(MU_E / rp)
        rpm, ra = R_M + 250e3, R_M + 33793e3
        am = (rpm + ra) / 2
        dv2 = np.sqrt(vi2 ** 2 + 2 * MU_M / rpm) - np.sqrt(MU_M * (2 / rpm - 1 / am))
        if best is None or dv1 + dv2 < best[0]:
            best = (dv1 + dv2, dv1, dv2, np.degrees(th))
    return [best[0] / 1000, best[1] / 1000, best[2] / 1000, best[3]]


def imleo(dv_kms, isp, k_inert, fixed, payload=60.0):
    """Initial mass in LEO (t) of a single propulsion stage delivering `payload` t: inert mass = k × propellant + fixed."""
    R = np.exp(dv_kms * 1000 / (isp * G0))
    q = k_inert * (R - 1)
    if q >= 1:
        return np.nan
    mf = (payload + fixed) / (1 - q)
    return mf * R


CHEM = dict(isp=450, k_inert=0.12, fixed=0.0)
NTP = dict(isp=900, k_inert=0.20, fixed=10.0)


def marstrip():
    tofs = np.arange(95, 291, 5)
    dvs = np.array([mars_dv(t)[:3] for t in tofs])
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.2))
    a.plot(tofs, dvs[:, 0], color=NAVY, lw=1.8, label="total")
    a.plot(tofs, dvs[:, 1], color=BLUE, lw=1.3, ls="--", label="trans-Mars injection (from LEO)")
    a.plot(tofs, dvs[:, 2], color=ORANGE, lw=1.3, ls=":", label="Mars orbit insertion")
    a.set_xlabel("One-way transit time (days)")
    a.set_ylabel("Δv (km/s)")
    a.set_ylim(0, 12)
    a.set_title("(a) Impulsive Δv for faster transfers", fontsize=8.6)
    a.legend(fontsize=6.4, loc="upper right")
    ch = np.array([imleo(d, **CHEM) for d in dvs[:, 0]])
    nt = np.array([imleo(d, **NTP) for d in dvs[:, 0]])
    b.plot(tofs, ch, color=NAVY, lw=1.8, label="chemical H₂/O₂, 450 s")
    b.plot(tofs, nt, color=ORANGE, lw=1.8, label="nuclear thermal, 900 s")
    b.set_yscale("log")
    b.set_ylim(100, 3000)
    b.set_xlabel("One-way transit time (days)")
    b.set_ylabel("Initial mass in LEO (t)")
    b.set_title("(b) Mass in LEO for 60 t delivered to Mars orbit", fontsize=8.6)
    b.axhline(300, color=GREY, lw=0.7, ls="--")
    b.text(285, 315, "300 t", fontsize=6.3, color=GREY, ha="right", va="bottom")
    b.legend(fontsize=6.6, loc="upper right")
    fig.text(0.99, 0.01, "Coplanar circular orbits, optimal phasing; 400 km LEO to 250 × 33 793 km Mars orbit. Stage inert mass: "
             "chemical 12 % of propellant;\nnuclear 20 % of propellant + 10 t of engines and shield. No aerocapture; "
             "one-way.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    save(fig, "ch42_marstrip")


# ---------------------------------------------------------------------------------------------
# 6. Solar sails: characteristic acceleration and spiral times
# ---------------------------------------------------------------------------------------------
P_SUN = 1361.0 / C            # N/m² at 1 AU (absorbed)
ETA_SAIL = 0.85
G_SUN_1AU = MU_S / AU ** 2    # m/s²


def a_char(sigma_gm2, eta=ETA_SAIL):
    return 2 * eta * P_SUN / (sigma_gm2 / 1000.0)


_ALPHA = np.radians(np.linspace(-89.5, 89.5, 359))


def sail_time(ac, rtarget, outward=True):
    """Years for a flat sail (characteristic acceleration ac, m/s²) starting on a circular orbit at 1 AU to first reach
    radius rtarget, steering at each instant to maximise (outward) or minimise (inward) the rate of orbital energy."""
    sgn = 1.0 if outward else -1.0

    def f(t, y):
        x, yy, vx, vy = y
        r = np.hypot(x, yy)
        er = np.array([x, yy]) / r
        et = np.array([-yy, x]) / r
        psi = np.arctan2(vx * et[0] + vy * et[1], vx * er[0] + vy * er[1])
        al = _ALPHA[np.argmax(sgn * np.cos(_ALPHA) ** 2 * np.cos(psi - _ALPHA))]
        n = np.cos(al) * er + np.sin(al) * et
        acc = ac * (AU / r) ** 2 * np.cos(al) ** 2
        return [vx, vy, *(-MU_S / r ** 2 * er + acc * n)]

    def ev(t, y):
        return np.hypot(y[0], y[1]) - rtarget
    ev.terminal = True
    s = solve_ivp(f, (0, 60 * 3.156e7), [AU, 0, 0, np.sqrt(MU_S / AU)], events=ev, rtol=1e-8, atol=1.0,
                  max_step=86400 * 5)
    return s.t_events[0][0] / 3.156e7 if len(s.t_events[0]) else np.nan


def spiral_time(ac, r1_au):
    """Quasi-circular log-spiral time (years) from 1 AU to r1 (AU) at the optimal cone angle (transverse factor 0.385)."""
    k = np.cos(np.arctan(1 / np.sqrt(2))) ** 2 * np.sin(np.arctan(1 / np.sqrt(2)))
    return np.sqrt(MU_S / AU) * abs(r1_au ** 1.5 - 1.0) / (3 * k * ac) / 3.156e7


SAILS = [("IKAROS", 310, 196), ("LightSail 2", 5.0, 32), ("NEA Scout", 14, 86), ("ACS3", 16, 80)]


def sail():
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.3))
    sig = np.logspace(-1, 4, 200)
    a.plot(sig, a_char(sig) * 1000, color=NAVY, lw=1.8, label="sail efficiency 0.85")
    a.plot(sig, a_char(sig, 1.0) * 1000, color=NAVY, lw=0.9, ls="--", label="ideal reflector")
    for n, m, A in SAILS:
        s = m / A * 1000
        a.plot(s, a_char(s) * 1000, "o", color=ORANGE, ms=5, zorder=5)
    a.annotate("LightSail 2, NEA Scout, ACS3\n156–200 g/m², ≈ 0.04–0.05 mm/s²", (175, a_char(175) * 1000),
               xytext=(250, 0.35), fontsize=6.2, color=ORANGE, ha="left",
               arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))
    a.annotate("IKAROS\n1 580 g/m²", (1582, a_char(1582) * 1000), xytext=(500, 0.0014), fontsize=6.2, color=ORANGE,
               ha="right", arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))
    for s, t, yy in [(3.5, "2.5 µm film only", 0.0016), (10.7, "7.5 µm polyimide film only", 0.0045)]:
        a.axvline(s, color=GREY, lw=0.7, ls=":")
        a.text(s * 1.12, yy, t, fontsize=6.0, color=GREY, ha="left", va="bottom")
    a.set_xscale("log")
    a.set_yscale("log")
    a.set_xlim(0.5, 1e4)
    a.set_ylim(1e-3, 30)
    a.set_xlabel("Total areal density σ = m / A (g/m²)")
    a.set_ylabel("Characteristic acceleration (mm/s²)")
    a.set_title("(a) Sail performance at 1 AU", fontsize=8.6)
    a.legend(fontsize=6.4, loc="upper right")
    acl = np.logspace(np.log10(0.03), np.log10(3.0), 50)
    acs = np.array([0.05, 0.1, 0.2, 0.5, 1.0, 2.0])
    for tgt, name, col, out in [(5.2, "Jupiter (5.2 AU)", VIOLET, True), (1.524, "Mars (1.52 AU)", ORANGE, True),
                                (0.387, "Mercury (0.39 AU)", RED, False)]:
        b.plot(acl, spiral_time(acl * 1e-3, tgt), color=col, lw=1.7, label=f"to {name}")
        if tgt < 2:
            ts = np.array([sail_time(x * 1e-3, tgt * AU, out) for x in acs])
            b.plot(acs, ts, "o", color=col, ms=4, mfc="white", mew=1.2)
    b.plot([], [], "o", color=GREY, ms=4, mfc="white", mew=1.2, label="numerical, steered for energy")
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlim(0.03, 3)
    b.set_ylim(0.1, 100)
    b.set_xlabel("Characteristic acceleration (mm/s²)")
    b.set_ylabel("Time from 1 AU (years)")
    b.set_title("(b) Spiralling from Earth's orbit", fontsize=8.6)
    b.legend(fontsize=6.4, loc="lower left")
    fig.text(0.99, 0.01, "a_c = 2ηP/(cσ), P/c = 4.54 µN/m² at 1 AU; σ uses total spacecraft mass. (b) Lines: quasi-circular spiral, "
             "cone angle 35.3°, T = √(μ/r₀) |(r/r₀)^1.5 − 1| / (3 × 0.385 a_c).\nDots: numerical flat-sail trajectories "
             "steered to change orbital energy fastest — time to first reach the distance, without matching the "
             "planet's velocity.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    save(fig, "ch42_sail")


# ---------------------------------------------------------------------------------------------
# 7. Laser sail: Starshot-class acceleration
# ---------------------------------------------------------------------------------------------
LASER_P, LAMBDA, D_ARRAY, D_SAIL = 100e9, 1.064e-6, 3000.0, 4.1


def laser_run(m, t_end=1800.0, dt=0.02):
    L0 = D_SAIL * D_ARRAY / (2.44 * LAMBDA)
    n = int(t_end / dt)
    t = np.arange(n) * dt
    x = np.zeros(n)
    v = np.zeros(n)
    acc = np.zeros(n)
    p = xx = vv = 0.0
    for i in range(n):
        f = 1.0 if xx < L0 else (L0 / xx) ** 2
        b = vv / C
        F = 2 * LASER_P * f / C * (1 - b) / (1 + b)
        gam = np.sqrt(1 + (p / (m * C)) ** 2)
        acc[i] = F / (m * gam ** 3)
        p += F * dt
        gam = np.sqrt(1 + (p / (m * C)) ** 2)
        vv = p / (gam * m)
        xx += vv * dt
        x[i], v[i] = xx, vv
    return t, x, v, acc, L0


def starshot():
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 3.2))
    for m, col in [(1e-3, BLUE), (2e-3, ORANGE), (5e-3, GREEN)]:
        t, x, v, acc, L0 = laser_run(m)
        a.plot(t / 60, v / C, color=col, lw=1.8, label=f"{m * 1000:.0f} g sail + probe")
        b.plot(x / 1e9, acc / G0, color=col, lw=1.8)
        i = np.searchsorted(x, L0)
        a.plot(t[i] / 60, v[i] / C, "o", color=col, ms=4)
    a.text(4.6, 0.04, "dots: beam spot grows larger\nthan the sail (diffraction)", fontsize=6.3, color=GREY)
    a.set_xlabel("Time after laser switch-on (minutes)")
    a.set_ylabel("Speed (fraction of light speed)")
    a.set_xlim(0, 30)
    a.set_ylim(0, 0.32)
    a.set_title("(a) Speed", fontsize=8.6)
    a.legend(fontsize=6.6, loc="lower right")
    b.axvline(L0 / 1e9, color=GREY, ls="--", lw=0.8)
    b.text(L0 / 1e9 * 1.25, 5.5e4, f"diffraction distance\n≈ {L0 / 1e9:.1f} million km", fontsize=6.3, color=GREY,
           va="bottom")
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlim(0.01, 500)
    b.set_ylim(100, 2e5)
    b.set_xlabel("Distance from the laser (million km)")
    b.set_ylabel("Acceleration (g)")
    b.set_title("(b) Acceleration", fontsize=8.6)
    fig.text(0.99, 0.01, "100 GW at 1.064 µm from a 3 km phased array, 4.1 m perfectly reflecting sail; F = (2P/c)(1−β)/(1+β) "
             "× captured fraction\n(1, or (L₀/L)² beyond the diffraction distance L₀ = D d/2.44λ); relativistic "
             "motion; light-travel delay neglected.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    save(fig, "ch42_starshot")


# ---------------------------------------------------------------------------------------------
# 8. Energy per kilogram of fuel
# ---------------------------------------------------------------------------------------------
MEV = 1.602176634e-13
U = 1.66053906660e-27


def energy():
    rows = [("Lithium-ion battery", 0.9e6, None),
            ("H₂/O₂ combustion", 13.4e6, None),
            ("Pu-238 decay (complete)", 5.59 * MEV / (238 * U), None),
            ("U-235 fission (complete)", 202.5 * MEV / (235 * U), None),
            ("D–T fusion", 17.6 * MEV / (5 * U), None),
            ("D–³He fusion", 18.3 * MEV / (5 * U), None),
            ("Matter–antimatter", C ** 2, None)]
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    y = np.arange(len(rows))
    cols = [GREY, NAVY, GOLD, ORANGE, VIOLET, VIOLET, RED]
    vals = [r[1] for r in rows]
    ax.barh(y, vals, color=cols, height=0.62, zorder=2)
    for yi, (n, e, _) in zip(y, rows):
        if n == "Matter–antimatter":
            txt = f"{e:.1e} J/kg · E = mc²: all mass becomes energy".replace("e+", "×10^")
        else:
            vmax = np.sqrt(2 * e)
            vtxt = f"{vmax / 1000:.1f} km/s" if vmax < 1e5 else f"{vmax / 1000:,.0f} km/s ({vmax / C:.3f} c)".replace(",", " ")
            txt = f"{e:.1e} J/kg · ideal v = √(2E) = {vtxt}".replace("e+", "×10^")
        txt = txt.replace("×10^0", "×10^").replace("×10^", "×10")
        ax.text(e * 1.6, yi, _sup(txt), va="center", fontsize=6.6)
    ax.set_xscale("log")
    ax.set_xlim(1e5, 1e22)
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.4)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Energy released per kilogram of reacting fuel (J/kg)")
    fig.text(0.99, 0.01, "Ideal exhaust speed if all the released energy went into the reacted mass alone (non-relativistic "
             "estimate).\nReal engines also heat or push inert propellant and lose energy as radiation and neutrons.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.085, 1, 1))
    save(fig, "ch42_energy")


def _sup(s):
    """Turn '×1013' style exponents into Unicode superscripts."""
    import re
    sup = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

    def rep(m):
        return "×10" + m.group(1).translate(sup)
    return re.sub(r"×10(\d+)", rep, s)


# ---------------------------------------------------------------------------------------------
# 9. Schematic: tethers
# ---------------------------------------------------------------------------------------------
def tether():
    fig, ax = canvas(7.0, 3.3, xlim=(0, 140), ylim=(0, 66))
    label(ax, 3, 63.5, "(a) Electrodynamic tether (drag mode)", fs=8.4, weight="bold", color=NAVY, ha="left")
    ax.add_patch(Wedge((34, -58), 70, 62, 118, fc=EARTH, ec="#1D4F8C", lw=0.8, zorder=1))
    ax.add_patch(Wedge((34, -58), 73, 62, 118, width=3, fc="#BFDDF5", ec="none", alpha=0.8, zorder=1))
    label(ax, 34, 6, "Earth", fs=7, color="white", weight="bold")
    for xx, yy in [(8, 22), (17, 22), (8, 33), (17, 33), (8, 41), (17, 41), (45, 33), (54, 33), (63, 33),
                   (45, 50), (54, 50), (63, 50)]:
        ax.text(xx, yy, "⊗", fontsize=7, color=SKY, ha="center", va="center", zorder=2)
    label(ax, 3, 15.8, "magnetic field B: into the page (north)", fs=6.2, color=SKY, ha="left")
    ax.plot([34, 34], [20, 52], color=INK, lw=1.6, zorder=4)
    satellite(ax, 34, 54, s=1.3)
    ax.add_patch(Circle((34, 19), 1.6, fc="#C8CDD3", ec="#444", lw=0.5, zorder=5))
    arrow(ax, (40, 42), (62, 42), "orbital velocity v (east)", color=NAVY, lw=1.3, fs=6.4)
    arrow(ax, (31, 25), (31, 45), color=GOLD, lw=1.6, ms=8)
    label(ax, 29.3, 35, "current I", fs=6.4, color="#8A6D00", ha="right", rot=90)
    arrow(ax, (28, 48.5), (12, 48.5), "force I L × B", color=RED, lw=1.5, fs=6.4)
    label(ax, 43, 21.5, "EMF ≈ v B L = 7.6 km/s × 30 µT × 10 km\n≈ 2 kV;  1 A of current → 0.3 N of drag", fs=6.2,
          ha="left", bg="white")
    # (b) momentum exchange
    label(ax, 78, 63.5, "(b) Momentum-exchange tether", fs=8.4, weight="bold", color=NAVY, ha="left")
    cx, cy = 106, 33
    ax.add_patch(Circle((cx, cy), 20, fc="none", ec=GREY, lw=0.7, ls="--", zorder=1))
    ang = np.radians(70)
    p1 = (cx + 20 * np.cos(ang), cy + 20 * np.sin(ang))
    p2 = (cx - 20 * np.cos(ang), cy - 20 * np.sin(ang))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=INK, lw=1.5, zorder=3)
    ax.add_patch(Circle((cx, cy), 2.4, fc="#C8CDD3", ec="#444", lw=0.6, zorder=4))
    label(ax, cx + 4, cy - 0.5, "facility", fs=6.2, ha="left", color=GREY)
    ax.add_patch(Circle(p2, 1.4, fc=ORANGE, ec="#444", lw=0.5, zorder=4))
    label(ax, p2[0] - 2.5, p2[1] + 1.5, "catch a slower\npayload", fs=6.2, ha="right", color=ORANGE)
    ax.add_patch(Circle(p1, 1.4, fc=ORANGE, ec="#444", lw=0.5, zorder=4))
    arrow(ax, (p1[0] + 1.6, p1[1]), (p1[0] + 14, p1[1]), color=ORANGE, lw=1.3)
    label(ax, p1[0] + 3, p1[1] + 3.2, "release at the top", fs=6.2, ha="left", color=ORANGE)
    arrow(ax, (cx + 19.5, cy + 13), (cx + 23, cy + 1), color=GREY, lw=0.9, rad=-0.3, ms=7)
    label(ax, cx + 23.5, cy + 9, "spin", fs=6.2, color=GREY, ha="left")
    arrow(ax, (80, 52), (92, 52), "orbital motion", color=NAVY, lw=1.0, fs=6.0, ms=7)
    label(ax, 106, 5, "the payload leaves faster than it arrived; the facility loses\nthe same momentum and must be re-boosted",
          fs=6.2, color=INK)
    save(fig, "ch42_tether")


if __name__ == "__main__":
    fns = [rocketeq, ptmap, neptrip, ntpnep, marstrip, sail, starshot, energy, tether]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
