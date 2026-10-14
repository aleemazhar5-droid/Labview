import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403

MU_E = 398600.4418
R_E = 6378.137
MU_S = 1.32712440018e11
AU = 1.495978707e8


def conics():
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.set_aspect("equal")
    ax.axis("off")
    p = 1.0
    for e, c, lab in [(0.0, BLUE, "circle  e = 0"), (0.6, GREEN, "ellipse  0 < e < 1"), (1.0, ORANGE, "parabola  e = 1"),
                      (1.6, RED, "hyperbola  e > 1")]:
        if e < 1:
            nu = np.linspace(0, 2 * np.pi, 400)
        else:
            lim = np.arccos(-1 / e) - 0.06 if e > 1 else np.pi - 0.35
            nu = np.linspace(-lim, lim, 400)
        r = p / (1 + e * np.cos(nu))
        ax.plot(r * np.cos(nu), r * np.sin(nu), color=c, lw=1.8, label=lab)
    ax.plot(0, 0, "o", color=NAVY, ms=7)
    ax.text(0.05, -0.18, "focus\n(central body)", fontsize=7.5, color=NAVY)
    ax.set_xlim(-2.8, 1.4)
    ax.set_ylim(-1.7, 1.7)
    ax.legend(loc="upper left", fontsize=8)
    ax.text(-2.75, -1.6, "All have the same semi-latus rectum p; r = p / (1 + e cos ν)", fontsize=7.5, color=GREY)
    save(fig, "ch03_conics")


def ellipse_geom():
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    ax.set_aspect("equal")
    ax.axis("off")
    a, e = 3.0, 0.6
    b = a * np.sqrt(1 - e ** 2)
    c = a * e
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(a * np.cos(t) - c, b * np.sin(t), color=BLUE, lw=1.8)
    earth(ax, 0, 0, 0.32, z=3, atmosphere=False)
    ax.plot(-2 * c, 0, "o", color=GREY, ms=4)
    ax.text(-2 * c, -0.3, "empty focus", fontsize=7, ha="center", color=GREY)
    ax.plot([-a - c, a - c], [0, 0], color=GREY, lw=0.6, ls="--")
    ax.plot([-c, -c], [0, b], color=GREY, lw=0.6, ls="--")
    darrow(ax, (-a - c, -2.25), (-c, -2.25), color=NAVY, lw=0.8, ms=7)
    ax.text(-a / 2 - c, -2.15, "a (semi-major axis)", fontsize=7.5, ha="center", color=NAVY, va="bottom")
    darrow(ax, (-c - 0.1, 0), (-c - 0.1, b), color=NAVY, lw=0.8, ms=7)
    ax.text(-c - 0.2, b / 2, "b", fontsize=8, ha="right", color=NAVY)
    darrow(ax, (0, -0.55), (a - c, -0.55), color=GREEN, lw=0.8, ms=7)
    ax.text((a - c) / 2, -0.75, "r$_p$ = a(1−e)", fontsize=7.5, ha="center", color=GREEN, va="top")
    darrow(ax, (-a - c, 0.25), (0, 0.25), color=RED, lw=0.8, ms=7)
    ax.text(-a / 2 - 1.5, 0.35, "r$_a$ = a(1+e)", fontsize=7.5, ha="center", color=RED)
    ax.text(a - c + 0.1, 0.12, "periapsis", fontsize=7.5)
    ax.text(-a - c - 0.1, 0.12, "apoapsis", fontsize=7.5, ha="right")
    nu = np.radians(65)
    r = a * (1 - e ** 2) / (1 + e * np.cos(nu))
    x, y = r * np.cos(nu), r * np.sin(nu)
    ax.plot([0, x], [0, y], color=ORANGE, lw=1.2)
    satellite(ax, x, y, 0.12, angle=-30)
    ax.add_patch(Arc((0, 0), 1.2, 1.2, theta1=0, theta2=65, color=ORANGE, lw=1))
    ax.text(0.7, 0.35, "ν", fontsize=10, color=ORANGE)
    ax.text(x / 2 - 0.25, y / 2 + 0.1, "r", fontsize=9, color=ORANGE)
    ax.text(1.2, 2.25, "e = c / a = √(1 − b²/a²)\nr = a(1 − e²) / (1 + e cos ν)", fontsize=8, color=INK)
    ax.set_xlim(-5.3, 2.2)
    ax.set_ylim(-2.6, 2.7)
    save(fig, "ch03_ellipse")


def elements3d():
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.set_aspect("equal")
    ax.axis("off")
    # oblique projection of 3D points
    el, az = np.radians(22), np.radians(-35)

    def P(x, y, z):
        x1 = x * np.cos(az) - y * np.sin(az)
        y1 = x * np.sin(az) + y * np.cos(az)
        return x1, y1 * np.sin(el) + z * np.cos(el)
    t = np.linspace(0, 2 * np.pi, 400)
    # equatorial plane disk
    R = 3.2
    ex, ey = P(R * np.cos(t), R * np.sin(t), 0 * t)
    ax.fill(ex, ey, color=SKY, alpha=0.15)
    ax.plot(ex, ey, color=SKY, lw=0.8)
    ax.text(*P(R * 0.75, -R * 0.95, 0), "Equatorial plane", fontsize=7.5, color=BLUE)
    # orbit
    inc, raan, argp = np.radians(50), np.radians(40), np.radians(70)
    a, e = 2.4, 0.35
    nu = np.linspace(0, 2 * np.pi, 600)
    r = a * (1 - e ** 2) / (1 + e * np.cos(nu))
    xp, yp = r * np.cos(nu), r * np.sin(nu)

    def rot(xp, yp):
        cO, sO, ci, si, cw, sw = np.cos(raan), np.sin(raan), np.cos(inc), np.sin(inc), np.cos(argp), np.sin(argp)
        X = (cO * cw - sO * sw * ci) * xp + (-cO * sw - sO * cw * ci) * yp
        Y = (sO * cw + cO * sw * ci) * xp + (-sO * sw + cO * cw * ci) * yp
        Z = (sw * si) * xp + (cw * si) * yp
        return X, Y, Z
    X, Y, Z = rot(xp, yp)
    px, py = P(X, Y, Z)
    above = Z >= 0
    ax.plot(np.where(above, px, np.nan), np.where(above, py, np.nan), color=ORANGE, lw=2)
    ax.plot(np.where(~above, px, np.nan), np.where(~above, py, np.nan), color=ORANGE, lw=1.2, ls="--")
    earth(ax, 0, 0, 0.45, z=4, atmosphere=False)
    # axes
    for v, lab in [((3.6, 0, 0), "♈ vernal equinox (X)"), ((0, 3.6, 0), "Y"), ((0, 0, 3.0), "Z (north pole)")]:
        x1, y1 = P(*v)
        ax.annotate("", xy=(x1, y1), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=0.9))
        ax.text(x1 * 1.05, y1 * 1.05, lab, fontsize=7.5, color=NAVY)
    # line of nodes
    n1 = P(3.4 * np.cos(raan), 3.4 * np.sin(raan), 0)
    n2 = P(-3.4 * np.cos(raan), -3.4 * np.sin(raan), 0)
    ax.plot([n2[0], n1[0]], [n2[1], n1[1]], color=GREY, lw=0.8, ls="-.")
    ax.text(n1[0] + 0.05, n1[1] - 0.25, "ascending node ☊\n(line of nodes)", fontsize=7, color=GREY)
    # RAAN arc
    tt = np.linspace(0, raan, 50)
    ax.plot(*P(1.4 * np.cos(tt), 1.4 * np.sin(tt), 0 * tt), color=GREEN, lw=1.4)
    ax.text(*P(1.7 * np.cos(raan / 2), 1.7 * np.sin(raan / 2), 0), "Ω", color=GREEN, fontsize=11)
    # periapsis
    Xp, Yp, Zp = rot(np.array([a * (1 - e)]), np.array([0.0]))
    pp = P(Xp[0], Yp[0], Zp[0])
    ax.plot([0, pp[0]], [0, pp[1]], color=RED, lw=1)
    ax.plot(*pp, "o", color=RED, ms=4)
    ax.text(pp[0] + 0.08, pp[1], "periapsis", fontsize=7.5, color=RED)
    # argp arc in orbit plane
    tt = np.linspace(0, argp, 50)
    cO, sO, ci, si = np.cos(raan), np.sin(raan), np.cos(inc), np.sin(inc)
    xa = 1.1 * np.cos(tt)
    ya = 1.1 * np.sin(tt)
    Xa = cO * xa - sO * ci * ya
    Ya = sO * xa + cO * ci * ya
    Za = si * ya
    ax.plot(*P(Xa, Ya, Za), color=RED, lw=1.4)
    ax.text(*P(1.35 * np.cos(argp / 2) * cO - sO * ci * 1.35 * np.sin(argp / 2),
               sO * 1.35 * np.cos(argp / 2) + cO * ci * 1.35 * np.sin(argp / 2), si * 1.35 * np.sin(argp / 2)),
            "ω", color=RED, fontsize=11)
    # satellite position and true anomaly
    nus = np.radians(115)
    rs = a * (1 - e ** 2) / (1 + e * np.cos(nus))
    Xs, Ys, Zs = rot(np.array([rs * np.cos(nus)]), np.array([rs * np.sin(nus)]))
    sp = P(Xs[0], Ys[0], Zs[0])
    ax.plot([0, sp[0]], [0, sp[1]], color=VIOLET, lw=1)
    satellite(ax, sp[0], sp[1], 0.09, angle=20)
    ax.text(sp[0] - 0.2, sp[1] + 0.35, "satellite (ν = true anomaly,\nmeasured from periapsis)", fontsize=7, color=VIOLET, ha="right")
    # inclination label
    ax.text(*P(2.6 * np.cos(raan) + 0.2, 2.6 * np.sin(raan), 0.55), "i", fontsize=11, color=BLUE)
    ax.text(-4.6, -2.6, "Size & shape: a, e    Orientation: i, Ω, ω    Position: ν (or mean anomaly M)", fontsize=7.6,
            color=INK)
    ax.set_xlim(-4.7, 4.3)
    ax.set_ylim(-2.8, 3.4)
    save(fig, "ch03_elements")


def anomalies():
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.set_aspect("equal")
    ax.axis("off")
    a, e = 3, 0.55
    b = a * np.sqrt(1 - e ** 2)
    c = a * e
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(a * np.cos(t), a * np.sin(t), color=GREY, lw=0.8, ls="--")
    ax.plot(a * np.cos(t), b * np.sin(t), color=BLUE, lw=1.8)
    F = (c, 0)
    ax.plot(0, 0, "+", color=GREY)
    ax.plot(*F, "o", color=NAVY, ms=6)
    E = np.radians(110)
    Q = (a * np.cos(E), a * np.sin(E))
    S = (a * np.cos(E), b * np.sin(E))
    ax.plot([0, Q[0]], [0, Q[1]], color=GREEN, lw=1)
    ax.plot([Q[0], S[0]], [Q[1], S[1]], color=GREY, lw=0.6, ls=":")
    ax.plot([F[0], S[0]], [F[1], S[1]], color=ORANGE, lw=1.2)
    ax.plot(*S, "o", color=ORANGE, ms=5)
    ax.plot(*Q, "o", color=GREEN, ms=4)
    ax.add_patch(Arc((0, 0), 1.0, 1.0, theta1=0, theta2=110, color=GREEN))
    ax.text(0.2, 0.55, "E", color=GREEN, fontsize=10)
    nu = np.degrees(np.arctan2(S[1] - F[1], S[0] - F[0]))
    ax.add_patch(Arc(F, 1.3, 1.3, theta1=0, theta2=nu, color=ORANGE))
    ax.text(F[0] + 0.55, 0.5, "ν", color=ORANGE, fontsize=10)
    ax.plot([-a - 0.2, a + 0.2], [0, 0], color=GREY, lw=0.5)
    ax.text(3.4, 2.1, "Kepler's equation:\nM = E − e sin E\nM = n (t − t$_p$),  n = √(μ/a³)\n\n"
            "tan(ν/2) = √((1+e)/(1−e)) tan(E/2)", fontsize=8, va="top")
    ax.text(Q[0] - 0.1, Q[1] + 0.12, "auxiliary circle", fontsize=7, color=GREEN, ha="right")
    ax.set_xlim(-3.4, 7.6)
    ax.set_ylim(-3.2, 3.3)
    save(fig, "ch03_anomalies")


def speeds_periods():
    h = np.logspace(np.log10(150), np.log10(400000), 400)
    r = R_E + h
    vc = np.sqrt(MU_E / r)
    ve = np.sqrt(2 * MU_E / r)
    T = 2 * np.pi * np.sqrt(r ** 3 / MU_E) / 3600
    fig, a1 = plt.subplots(figsize=(7.0, 3.7))
    a1.plot(h, vc, color=BLUE, label="Circular orbital speed")
    a1.plot(h, ve, color=RED, label="Escape speed")
    a1.set_xscale("log")
    a1.set_xlabel("Altitude above Earth's surface (km)")
    a1.set_ylabel("Speed (km/s)")
    a2 = a1.twinx()
    a2.plot(h, T, color=ORANGE, label="Orbital period", lw=1.4, ls="--")
    a2.set_yscale("log")
    a2.set_ylabel("Period (hours, log)", color=ORANGE)
    a2.spines["right"].set_visible(True)
    a2.grid(False)
    for hh, name in [(400, "ISS"), (20200, "GPS"), (35786, "GEO"), (384400 - R_E, "Moon")]:
        a1.axvline(hh, color=GREY, lw=0.5, ls=":")
        a1.text(hh * 1.05, 11.4, name, fontsize=7, color=GREY)
    l1, lab1 = a1.get_legend_handles_labels()
    l2, lab2 = a2.get_legend_handles_labels()
    a1.legend(l1 + l2, lab1 + lab2, loc="center left")
    a1.set_ylim(0, 12)
    save(fig, "ch03_speeds")


def perturbations():
    h = np.logspace(np.log10(200), np.log10(60000), 300)
    r = (R_E + h) * 1e3
    mu = MU_E * 1e9
    g0 = mu / r ** 2
    J2 = 1.0826e-3 * 3 * mu * (R_E * 1e3) ** 2 / r ** 4
    J22 = 1.8e-6 * 3 * mu * (R_E * 1e3) ** 2 / r ** 4
    moon = 2 * 4.9028e12 * r / (384400e3) ** 3
    sun = 2 * 1.327e20 * r / (1.496e11) ** 3
    srp = 4.56e-6 * 1.3 * 0.02 * np.ones_like(r)
    from_drag = []
    import importlib.util
    spec = importlib.util.spec_from_file_location("c2", Path(__file__).parent / "ch02.py")
    c2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c2)
    for hh, rr in zip(h, r):
        v = np.sqrt(mu / rr)
        rho = c2.rho(min(hh, 1000), 0.5) if hh <= 1000 else c2.rho(1000, 0.5) * np.exp(-(hh - 1000) / 250)
        from_drag.append(0.5 * rho * v ** 2 * 0.02 * 2.2)
    rel = 6 * mu / r ** 3 * 0.0 + 3.0e-7 * g0 * 0  # placeholder (not plotted)
    fig, ax = plt.subplots(figsize=(7.0, 4.1))
    ax.loglog(h, g0, color=NAVY, lw=2, label="Central gravity (point mass)")
    ax.loglog(h, J2, color=BLUE, label="Earth oblateness J₂")
    ax.loglog(h, J22, color=SKY, label="Higher harmonics (e.g., J₂₂)")
    ax.loglog(h, moon, color=VIOLET, label="Moon (tidal)")
    ax.loglog(h, sun, color=GOLD, label="Sun (tidal)")
    ax.loglog(h, srp, color=ORANGE, label="Solar radiation pressure (A/m = 0.02 m²/kg)")
    ax.loglog(h, from_drag, color=RED, label="Atmospheric drag (A/m = 0.02 m²/kg)")
    ax.set_ylim(1e-14, 20)
    ax.set_xlim(200, 60000)
    ax.set_xlabel("Altitude (km)")
    ax.set_ylabel("Acceleration (m/s²)")
    ax.axvline(35786, color=GREY, lw=0.5, ls=":")
    ax.text(31000, 3, "GEO", fontsize=7, color=GREY, ha="right")
    ax.legend(loc="lower left", fontsize=6.8, ncol=2)
    note(ax, "Orders of magnitude after Montenbruck & Gill (2000). Drag uses moderate solar activity.", xy=(1, -0.15))
    save(fig, "ch03_perturbations")


def j2_effects():
    J2 = 1.08263e-3
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.3))
    inc = np.linspace(0, 180, 361)
    for h, c in [(400, RED), (800, BLUE), (1500, GREEN), (20200, VIOLET)]:
        a = R_E + h
        n = np.sqrt(MU_E / a ** 3)
        rd = -1.5 * n * J2 * (R_E / a) ** 2 * np.cos(np.radians(inc))
        a1.plot(inc, np.degrees(rd) * 86400, color=c, label=f"{h} km")
    a1.axhline(360 / 365.2422, color=ORANGE, lw=0.8, ls="--")
    a1.text(5, 1.2, "+0.9856°/day:\nsun-synchronous", fontsize=6.6, color=ORANGE)
    a1.set_xlabel("Inclination (deg)")
    a1.set_ylabel("Nodal precession dΩ/dt (deg/day)")
    a1.legend(fontsize=6.6, loc="lower right")
    a1.set_xlim(0, 180)
    hs = np.linspace(200, 2000, 300)
    ss = []
    for h in hs:
        a = R_E + h
        n = np.sqrt(MU_E / a ** 3)
        ci = -np.radians(360 / 365.2422) / 86400 / (1.5 * n * J2 * (R_E / a) ** 2)
        ss.append(np.degrees(np.arccos(ci)) if abs(ci) <= 1 else np.nan)
    a2.plot(hs, ss, color=ORANGE, lw=2)
    for h, n in [(500, "500 km: 97.4°"), (705, "Landsat 705 km: 98.2°"), (1336, "Jason/Sentinel-6 1336 km\n(66°, not SSO)")][:2]:
        a = R_E + h
        nn = np.sqrt(MU_E / a ** 3)
        ci = -np.radians(360 / 365.2422) / 86400 / (1.5 * nn * J2 * (R_E / a) ** 2)
        ii = np.degrees(np.arccos(ci))
        a2.plot(h, ii, "o", color=NAVY, ms=3.5)
        if n:
            a2.text(h + 60, ii - 0.35, n, fontsize=6.6)
    a2.set_xlabel("Altitude (km)")
    a2.set_ylabel("Sun-synchronous inclination (deg)")
    a2.set_xlim(200, 2000)
    save(fig, "ch03_j2")


def hohmann():
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.set_aspect("equal")
    ax.axis("off")
    r1, r2 = 1.0, 2.6
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(r1 * np.cos(t), r1 * np.sin(t), color=BLUE, lw=1.6)
    ax.plot(r2 * np.cos(t), r2 * np.sin(t), color=GREEN, lw=1.6)
    a = (r1 + r2) / 2
    e = (r2 - r1) / (r2 + r1)
    nu = np.linspace(0, np.pi, 200)
    r = a * (1 - e ** 2) / (1 + e * np.cos(nu))
    ax.plot(r * np.cos(nu), r * np.sin(nu), color=ORANGE, lw=2)
    nu2 = np.linspace(np.pi, 2 * np.pi, 200)
    r_ = a * (1 - e ** 2) / (1 + e * np.cos(nu2))
    ax.plot(r_ * np.cos(nu2), r_ * np.sin(nu2), color=ORANGE, lw=0.8, ls=":")
    earth(ax, 0, 0, 0.42, z=3, atmosphere=False)
    ax.annotate("", xy=(1.0, 0.75), xytext=(1.0, 0.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(1.08, 0.35, "Δv₁\n(perigee burn)", fontsize=8, color=RED)
    ax.annotate("", xy=(-2.6, -0.65), xytext=(-2.6, 0.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(-2.5, -0.55, "Δv₂\n(apogee burn,\ncircularise)", fontsize=8, color=RED)
    ax.text(0.55, -0.75, "initial orbit r₁", fontsize=8, color=BLUE)
    ax.text(1.9, -2.0, "final orbit r₂", fontsize=8, color=GREEN)
    ax.text(-1.6, 1.85, "transfer ellipse\na = (r₁+r₂)/2", fontsize=8, color=ORANGE)
    ax.text(-3.2, -3.05, "Δv₁ = √(μ/r₁)·(√(2r₂/(r₁+r₂)) − 1)     Δv₂ = √(μ/r₂)·(1 − √(2r₁/(r₁+r₂)))     "
            "t = π√(a³/μ)", fontsize=7.4)
    ax.set_xlim(-3.3, 3.3)
    ax.set_ylim(-3.2, 2.9)
    save(fig, "ch03_hohmann")


def hohmann_vs_bielliptic():
    R = np.linspace(1.01, 40, 400)
    hoh = (1 / np.sqrt(R) - np.sqrt(2) * (1 - R) / np.sqrt(R * (1 + R)) - 1)
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    ax.plot(R, hoh, color=BLUE, lw=2, label="Hohmann (two impulses)")
    for Rs, c in [(15, ORANGE), (40, RED), (200, VIOLET)]:
        dv = []
        for Rv in R:
            alpha = Rv
            beta = Rs
            v = np.sqrt(2 * (alpha + beta) / (alpha * beta)) - (1 + np.sqrt(alpha)) / np.sqrt(alpha) \
                - np.sqrt(2 / (beta * (1 + beta))) * (1 - beta) if False else None
            r1, r2, rb = 1.0, Rv, Rs * 1.0
            a1 = (r1 + rb) / 2
            a2 = (r2 + rb) / 2
            d1 = np.sqrt(2 / r1 - 1 / a1) - 1
            d2 = np.sqrt(2 / rb - 1 / a2) - np.sqrt(2 / rb - 1 / a1)
            d3 = np.sqrt(2 / r2 - 1 / a2) - np.sqrt(1 / r2)
            dv.append(abs(d1) + abs(d2) + abs(d3))
        ax.plot(R, dv, color=c, lw=1.2, ls="--", label=f"Bi-elliptic, r$_b$ = {Rs} r₁")
    ax.plot(R, np.sqrt(2) - 1 + 0 * R, color=GREY, lw=0.6, ls=":")
    ax.text(30, 0.42, "escape: (√2 − 1)·v₁", fontsize=7, color=GREY)
    ax.axvline(11.94, color=GREY, lw=0.6, ls=":")
    ax.axvline(15.58, color=GREY, lw=0.6, ls=":")
    ax.text(12.1, 0.18, "11.94", fontsize=7, color=GREY)
    ax.text(15.8, 0.18, "15.58", fontsize=7, color=GREY)
    ax.set_xlabel("Radius ratio r₂ / r₁")
    ax.set_ylabel("Total Δv / initial circular speed v₁")
    ax.legend(fontsize=7, loc="lower right")
    ax.set_xlim(1, 40)
    ax.set_ylim(0.0, 0.6)
    save(fig, "ch03_bielliptic")


def plane_change():
    th = np.linspace(0, 60, 200)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for v, c, lab in [(7.67, RED, "LEO, 7.67 km/s"), (3.07, BLUE, "GEO, 3.07 km/s"), (1.6, GREEN, "GTO apogee, 1.6 km/s"),
                      (1.02, VIOLET, "Moon orbit around Earth, 1.02 km/s")]:
        ax.plot(th, 2 * v * np.sin(np.radians(th) / 2), color=c, label=lab)
    ax.set_xlabel("Plane change angle Δi (deg)")
    ax.set_ylabel("Δv = 2v sin(Δi/2)  (km/s)")
    ax.legend(fontsize=7.5)
    ax.text(1, 5.3, "A 28.5° change in LEO costs 3.8 km/s —\nmore than going from LEO to GEO by Hohmann (3.9 km/s total)",
            fontsize=7, color=GREY, ha="left")
    save(fig, "ch03_plane_change")


def cw_motion():
    n = 2 * np.pi / 5550.0
    t = np.linspace(0, 2 * 5550.0, 1200)

    def cw(x0, y0, vx0, vy0, tt=t):
        x = (4 - 3 * np.cos(n * tt)) * x0 + np.sin(n * tt) / n * vx0 + 2 / n * (1 - np.cos(n * tt)) * vy0
        y = 6 * (np.sin(n * tt) - n * tt) * x0 + y0 - 2 / n * (1 - np.cos(n * tt)) * vx0 + \
            (4 * np.sin(n * tt) - 3 * n * tt) / n * vy0
        return x, y
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    x, y = cw(0, -1500, 0.4, 0)
    ax.plot(y, x, color=BLUE, lw=1.5, label="Radial impulse 0.4 m/s at 1.5 km behind: ellipse, no net drift")
    x, y = cw(300, 0, 0, -2 * n * 300)
    ax.plot(y, x, color=GREEN, lw=1.5, label="Natural-motion circumnavigation (2:1 ellipse around target)")
    x, y = cw(0, -3000, 0, 0.25)
    ax.plot(y, x, color=ORANGE, lw=1.5, label="Posigrade impulse 0.25 m/s: rises, then falls behind")
    x, y = cw(-200, -2500, 0, 0)
    ax.plot(y, x, color=RED, lw=1.5, label="200 m lower orbit: drifts forward toward target")
    ax.plot(0, 0, "s", color=NAVY, ms=8)
    ax.text(150, 60, "target", fontsize=7.5, color=NAVY)
    ax.set_xlabel("Along-track position relative to target, y (m)  — direction of flight →")
    ax.set_ylabel("Radial, x (m, up)")
    ax.legend(fontsize=6.6, loc="lower left")
    ax.set_xlim(-9000, 6000)
    ax.set_ylim(-1700, 1700)
    note(ax, "Clohessy–Wiltshire solutions for a 400 km circular target orbit (period 92.5 min), two orbits shown. "
         "ẍ − 3n²x − 2nẏ = 0, ÿ + 2nẋ = 0.", xy=(1, -0.16))
    save(fig, "ch03_cw")


def ground_tracks():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.3, 4.0))
    ax = world_axes(fig)
    lon, lat = ground_track(R_E + 415, 51.64, hours=3.1, u0=0, raan0=60)
    plot_track(ax, lon, lat, color=RED, lw=1.2, label="ISS 415 km, 51.6° (2 orbits)")
    lon, lat = ground_track(R_E + 705, 98.2, hours=3.3, u0=0, raan0=150)
    plot_track(ax, lon, lat, color=BLUE, lw=1.2, label="Sun-synchronous 705 km, 98.2° (2 orbits)")
    # Molniya
    a = 26560.0
    e = 0.72
    i = np.radians(63.4)
    w = np.radians(270)
    n = np.sqrt(MU_E / a ** 3)
    t = np.linspace(0, 24 * 3600, 3000)
    M = n * t
    E = M.copy()
    for _ in range(30):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    u = nu + w
    raan = np.radians(-30)
    x = np.cos(raan) * np.cos(u) - np.sin(raan) * np.sin(u) * np.cos(i)
    y = np.sin(raan) * np.cos(u) + np.cos(raan) * np.sin(u) * np.cos(i)
    z = np.sin(u) * np.sin(i)
    latm = np.degrees(np.arcsin(z))
    lonm = (np.degrees(np.arctan2(y, x) - 7.2921159e-5 * t) + 180) % 360 - 180
    plot_track(ax, lonm, latm, color=VIOLET, lw=1.2, label="Molniya 12 h, 63.4° (1 day)")
    ax.plot([-75], [0], "o", color=GOLD, ms=6, transform=ccrs.PlateCarree(), label="GEO satellite (fixed point)")
    lon, lat = ground_track(42164 * 1.0, 40, hours=24, raan0=20)
    plot_track(ax, lon, lat, color=GREEN, lw=1.2, label="Inclined GSO / QZSS-like 40° (figure-8)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=2, fontsize=7)
    save(fig, "ch03_groundtracks", raster=True)


def tle_figure():
    fig, ax = canvas(7.4, 3.0, (0, 100), (0, 40))
    l0 = "ISS (ZARYA)"
    l1 = "1 25544U 98067A   26286.50000000  .00012345  00000+0  21914-3 0  9993"
    l2 = "2 25544  51.6390 112.4321 0004712 101.2345 258.9123 15.49912345587612"
    x0, cw = 4.0, 1.205
    fs = 8.4
    for txt, y in [(l0, 33.5), (l1, 24), (l2, 16)]:
        for k, ch in enumerate(txt):
            ax.text(x0 + k * cw, y, ch, family="DejaVu Sans Mono", fontsize=fs, va="center", ha="center", color=NAVY)
    f1 = [(3, 7, "satellite\ncatalogue no."), (10, 17, "international\ndesignator"), (19, 32, "epoch (yy, day of year)"),
          (34, 43, "dn/dt ÷ 2"), (54, 61, "B* drag term"), (69, 69, "check-\nsum")]
    f2 = [(9, 16, "inclination (°)"), (18, 25, "RAAN Ω (°)"), (27, 33, "eccentricity\n(decimal assumed)"),
          (35, 42, "arg. of\nperigee ω (°)"), (44, 51, "mean\nanomaly M (°)"), (53, 63, "mean motion\n(rev/day)"),
          (64, 68, "revolution\nnumber")]
    cols = [BLUE, ORANGE, GREEN, VIOLET, RED, GREY, GOLD]
    for k, (c1, c2, lab) in enumerate(f1):
        xa, xb = x0 + (c1 - 1) * cw - 0.5, x0 + (c2 - 1) * cw + 0.5
        ax.plot([xa, xb], [26.2, 26.2], color=cols[k % 7], lw=2)
        ax.text((xa + xb) / 2, 27.0, lab, fontsize=6.3, ha="center", va="bottom", color=cols[k % 7])
    for k, (c1, c2, lab) in enumerate(f2):
        xa, xb = x0 + (c1 - 1) * cw - 0.5, x0 + (c2 - 1) * cw + 0.5
        ax.plot([xa, xb], [13.8, 13.8], color=cols[k % 7], lw=2)
        ax.text((xa + xb) / 2, 13.0, lab, fontsize=6.3, ha="center", va="top", color=cols[k % 7])
    ax.text(2, 1.5, "TLEs are mean elements for the SGP4/SDP4 propagator, not osculating Keplerian elements. "
            "Illustrative values; current sets are\npublished by CelesTrak and Space-Track.org (also in the newer "
            "OMM / CCSDS format to allow catalogue numbers > 99 999).", fontsize=6.6, color=GREY)
    save(fig, "ch03_tle")


# ---------- interplanetary: ephemerides and Lambert ----------
EL = {"earth": [1.00000261, 0.00000562, 0.01671123, -0.00004392, -0.00001531, -0.01294668, 100.46457166,
                35999.37244981, 102.93768193, 0.32327364, 0.0, 0.0],
      "mars": [1.52371034, 0.00001847, 0.09339410, 0.00007882, 1.84969142, -0.00813131, -4.55343205,
               19140.30268499, -23.94362959, 0.44441088, 49.55953891, -0.29257343]}


def planet_rv(name, jd):
    a0, ad, e0, ed, i0, idt, L0, Ld, w0, wd, O0, Od = EL[name]
    T = (jd - 2451545.0) / 36525
    a = (a0 + ad * T) * AU
    e = e0 + ed * T
    i = np.radians(i0 + idt * T)
    L = np.radians(L0 + Ld * T)
    wbar = np.radians(w0 + wd * T)
    O = np.radians(O0 + Od * T)
    w = wbar - O
    M = (L - wbar + np.pi) % (2 * np.pi) - np.pi
    E = M
    for _ in range(25):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    p = a * (1 - e ** 2)
    r = p / (1 + e * np.cos(nu))
    rp = np.array([r * np.cos(nu), r * np.sin(nu), 0])
    vp = np.sqrt(MU_S / p) * np.array([-np.sin(nu), e + np.cos(nu), 0])
    cO, sO, ci, si, cw, sw = np.cos(O), np.sin(O), np.cos(i), np.sin(i), np.cos(w), np.sin(w)
    Rm = np.array([[cO * cw - sO * sw * ci, -cO * sw - sO * cw * ci, sO * si],
                   [sO * cw + cO * sw * ci, -sO * sw + cO * cw * ci, -cO * si],
                   [sw * si, cw * si, ci]])
    return Rm @ rp, Rm @ vp


def stumpff(z):
    if z > 1e-6:
        s = np.sqrt(z)
        return (1 - np.cos(s)) / z, (s - np.sin(s)) / s ** 3
    if z < -1e-6:
        s = np.sqrt(-z)
        return (np.cosh(s) - 1) / (-z), (np.sinh(s) - s) / s ** 3
    return 0.5, 1 / 6


def lambert(r1, r2, tof, mu=MU_S):
    R1, R2 = np.linalg.norm(r1), np.linalg.norm(r2)
    cosd = np.dot(r1, r2) / (R1 * R2)
    cz = np.cross(r1, r2)[2]
    dnu = np.arccos(np.clip(cosd, -1, 1))
    if cz < 0:
        dnu = 2 * np.pi - dnu
    A = np.sin(dnu) * np.sqrt(R1 * R2 / (1 - cosd))
    lo, hi = -4 * np.pi ** 2, 4 * np.pi ** 2
    z = 0.0
    for _ in range(100):
        C, S = stumpff(z)
        y = R1 + R2 + A * (z * S - 1) / np.sqrt(C)
        if A > 0 and y < 0:
            lo = z
            z = (lo + hi) / 2
            continue
        x = np.sqrt(y / C)
        t = (x ** 3 * S + A * np.sqrt(y)) / np.sqrt(mu)
        if t < tof:
            lo = z
        else:
            hi = z
        z = (lo + hi) / 2
        if abs(t - tof) < 1:
            break
    C, S = stumpff(z)
    y = R1 + R2 + A * (z * S - 1) / np.sqrt(C)
    f = 1 - y / R1
    g = A * np.sqrt(y / mu)
    gd = 1 - y / R2
    return (r2 - f * r1) / g, (gd * r2 - r1) / g


def jd_of(d):
    return 2451545.0 + (d - datetime(2000, 1, 1, 12)).total_seconds() / 86400


def porkchop():
    l0 = datetime(2026, 8, 15)
    a0 = datetime(2027, 5, 15)
    L = [l0 + timedelta(days=k) for k in range(0, 170, 3)]
    A = [a0 + timedelta(days=k) for k in range(0, 330, 4)]
    C3 = np.full((len(A), len(L)), np.nan)
    VINF = np.full((len(A), len(L)), np.nan)
    for j, ld in enumerate(L):
        rE, vE = planet_rv("earth", jd_of(ld))
        for i, ad in enumerate(A):
            tof = (ad - ld).total_seconds()
            if tof < 100 * 86400:
                continue
            rM, vM = planet_rv("mars", jd_of(ad))
            try:
                v1, v2 = lambert(rE, rM, tof)
            except Exception:  # noqa: BLE001
                continue
            C3[i, j] = np.linalg.norm(v1 - vE) ** 2
            VINF[i, j] = np.linalg.norm(v2 - vM)
    C3 = np.where(C3 > 26, np.nan, C3)
    VINF = np.where(VINF > 6.5, np.nan, VINF)
    import matplotlib.dates as mdates
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    Lx = mdates.date2num(L)
    Ay = mdates.date2num(A)
    cs = ax.contour(Lx, Ay, C3, levels=[9.5, 10, 11, 12, 14, 17, 20, 25], colors=[BLUE], linewidths=1.0)
    ax.clabel(cs, fmt="%d", fontsize=6.5)
    cs2 = ax.contour(Lx, Ay, VINF, levels=[2.75, 3, 3.5, 4, 5, 6], colors=[RED], linewidths=0.8, linestyles="--")
    ax.clabel(cs2, fmt="%.1f", fontsize=6.5)
    for days, c in [(150, GREY), (200, GREY), (250, GREY), (300, GREY)]:
        ax.plot(Lx, Lx + days, color=c, lw=0.5, ls=":")
        ax.text(Lx[-1] - 2, Lx[-1] + days - 6, f"TOF {days} d", fontsize=6.3, color=GREY, ha="right")
    idx = np.nanargmin(C3)
    i, j = np.unravel_index(idx, C3.shape)
    ax.plot(Lx[j], Ay[i], "*", color=ORANGE, ms=12)
    ax.text(Lx[j] + 3, Ay[i] - 10, f"min C3 ≈ {C3[i, j]:.1f} km²/s²", fontsize=7.5, color=ORANGE)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%Y"))
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_xlabel("Launch date from Earth")
    ax.set_ylabel("Arrival date at Mars")
    ax.set_ylim(Ay[0], Ay[-1])
    ax.plot([], [], color=BLUE, label="Launch energy C3 (km²/s²)")
    ax.plot([], [], color=RED, ls="--", label="Arrival v∞ at Mars (km/s)")
    ax.legend(loc="upper left", fontsize=7)
    note(ax, "Computed for this manual: Lambert solutions, single-revolution, using JPL approximate planetary elements.",
         xy=(1, -0.17))
    save(fig, "ch03_porkchop")
    return L[j], A[i], C3[i, j], VINF[i, j]


def gravity_assist():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.5), gridspec_kw=dict(width_ratios=[1, 1.1]))
    for a in (a1, a2):
        a.set_aspect("equal")
        a.axis("off")
    # left: hyperbolic flyby in planet frame
    e = 1.6
    p = 1.4
    lim = np.arccos(-1 / e) - 0.12
    nu = np.linspace(-lim, lim, 300)
    r = p / (1 + e * np.cos(nu))
    x, y = r * np.cos(nu), r * np.sin(nu)
    rot = np.radians(90)
    X = x * np.cos(rot) - y * np.sin(rot)
    Y = x * np.sin(rot) + y * np.cos(rot)
    a1.plot(X, Y, color=ORANGE, lw=2)
    planet(a1, 0, 0, 0.35, "#C9A27A")
    a1.annotate("", xy=(X[5], Y[5]), xytext=(X[0], Y[0]), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
    a1.annotate("", xy=(X[-1], Y[-1]), xytext=(X[-6], Y[-6]), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
    a1.text(0.0, -0.75, "planet", fontsize=7.5, ha="center")
    a1.text(-3.6, 3.3, "Planet-centred frame", fontsize=8.5, weight="bold", color=NAVY)
    a1.text(-3.6, -3.4, "|v∞,out| = |v∞,in|; the flyby only\nturns v∞ by the angle δ:\nsin(δ/2) = 1 / (1 + r$_p$ v∞² / μ)",
            fontsize=7, va="bottom")
    a1.text(0.55, 0.15, "r$_p$", fontsize=8, color=GREY)
    a1.plot([0, 0.0], [0, 0.0])
    a1.set_xlim(-3.7, 3.7)
    a1.set_ylim(-3.5, 3.6)
    # right: velocity triangle in Sun frame
    a2.text(-0.2, 3.3, "Sun-centred frame (vector sum)", fontsize=8.5, weight="bold", color=NAVY)
    O = np.array([0.0, 0.0])
    Vp = np.array([3.0, 0.0])
    vin = np.array([-1.0, 1.4])
    d = np.radians(-95)
    R = np.array([[np.cos(d), -np.sin(d)], [np.sin(d), np.cos(d)]])
    vout = R @ vin

    def arr(p0, v, c, lab, off=(0, 0.15), lw=1.8, ls="-"):
        a2.annotate("", xy=(p0[0] + v[0], p0[1] + v[1]), xytext=p0,
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=lw, linestyle=ls))
        a2.text(p0[0] + v[0] / 2 + off[0], p0[1] + v[1] / 2 + off[1], lab, fontsize=7.6, color=c, ha="center")
    arr(O, Vp, NAVY, "V$_{planet}$", off=(0, -0.35))
    arr(O + Vp, vin, BLUE, "v∞,in", off=(-0.35, 0.0))
    arr(O + Vp, vout, RED, "v∞,out", off=(0.45, 0.1))
    arr(O, Vp + vin, GREY, "V$_{in}$", off=(-0.35, 0.25), lw=1.2)
    arr(O, Vp + vout, GREEN, "V$_{out}$", off=(0.1, -0.4), lw=1.8)
    a2.text(0.0, -2.6, f"|V$_{{in}}$| = {np.linalg.norm(Vp + vin):.2f}   →   |V$_{{out}}$| = {np.linalg.norm(Vp + vout):.2f}"
            "\nThe spacecraft gains heliocentric energy;\nthe planet loses an imperceptible amount.",
            fontsize=7, va="top")
    a2.set_xlim(-0.6, 5.0)
    a2.set_ylim(-3.6, 3.6)
    save(fig, "ch03_gravity_assist")


def lagrange():
    mu = 0.01215
    x = np.linspace(-1.6, 1.6, 700)
    y = np.linspace(-1.4, 1.4, 600)
    X, Y = np.meshgrid(x, y)
    r1 = np.sqrt((X + mu) ** 2 + Y ** 2)
    r2 = np.sqrt((X - 1 + mu) ** 2 + Y ** 2)
    Om = 0.5 * (X ** 2 + Y ** 2) + (1 - mu) / r1 + mu / r2
    C = 2 * Om
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.set_aspect("equal")
    lv = [2.95, 2.988, 3.012, 3.10, 3.172, 3.188, 3.3, 3.6]
    ax.contourf(X, Y, np.clip(C, 2.9, 3.9), levels=[2.9, 2.988, 3.012, 3.172, 3.188, 3.3, 3.6, 3.9],
                colors=["#FFFFFF", "#F1F6FB", "#E1ECF6", "#CFE1F1", "#B8D3EA", "#9CC1E0", "#7FAED6"], alpha=0.9)
    ax.contour(X, Y, C, levels=lv, colors=NAVY, linewidths=0.5, alpha=0.7)

    def dOmdx(xx):
        a = abs(xx + mu)
        b = abs(xx - 1 + mu)
        return xx - (1 - mu) * (xx + mu) / a ** 3 - mu * (xx - 1 + mu) / b ** 3
    from scipy.optimize import brentq
    L1 = brentq(dOmdx, 0.5, 1 - mu - 1e-3)
    L2 = brentq(dOmdx, 1 - mu + 1e-3, 1.5)
    L3 = brentq(dOmdx, -1.5, -mu - 1e-3)
    pts = {"L1": (L1, 0), "L2": (L2, 0), "L3": (L3, 0), "L4": (0.5 - mu, np.sqrt(3) / 2),
           "L5": (0.5 - mu, -np.sqrt(3) / 2)}
    ax.plot(-mu, 0, "o", color=EARTH, ms=11)
    ax.text(-mu, -0.13, "Earth", ha="center", fontsize=8)
    ax.plot(1 - mu, 0, "o", color="#BBBBBB", ms=6, mec="#555")
    ax.text(1 - mu, -0.12, "Moon", ha="center", fontsize=8)
    offs = {"L1": (-0.13, 0.08), "L2": (0.04, 0.08), "L3": (-0.05, 0.08), "L4": (0.05, 0.05), "L5": (0.05, -0.12)}
    for k, (px, py) in pts.items():
        ax.plot(px, py, "X", color=ORANGE, ms=8, mec="white", mew=0.6)
        ax.text(px + offs[k][0], py + offs[k][1], k, fontsize=9, color=ORANGE, weight="bold")
    ax.set_xlabel("x (Earth–Moon distance units, rotating frame)")
    ax.set_ylabel("y")
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.3, 1.3)
    ax.grid(False)
    note(ax, f"Contours of the Jacobi constant (zero-velocity curves) for μ = 0.01215. L1 at {(L1 + mu) * 384400:,.0f} km "
             f"and L2 at {(L2 + mu) * 384400:,.0f} km from Earth.", xy=(1, -0.13))
    save(fig, "ch03_lagrange")


def dv_map():
    fig, ax = canvas(7.4, 4.4, (0, 120), (0, 70))
    nodes = {"Earth\nsurface": (8, 10), "LEO\n(400 km)": (30, 10), "GTO": (50, 22), "GEO": (68, 32),
             "Earth escape\n(C3 = 0)": (55, 45), "Trans-lunar\ninjection": (52, 10), "NRHO / Gateway\norbit": (74, 10),
             "Low lunar\norbit": (90, 18), "Lunar\nsurface": (110, 18), "Mars\ntransfer": (78, 52),
             "Low Mars\norbit": (100, 52), "Mars\nsurface": (114, 64), "Sun–Earth\nL2": (78, 38)}
    cols = {"Earth\nsurface": NAVY, "LEO\n(400 km)": BLUE, "GTO": SKY, "GEO": RED, "Earth escape\n(C3 = 0)": VIOLET,
            "Trans-lunar\ninjection": GOLD, "NRHO / Gateway\norbit": GOLD, "Low lunar\norbit": GOLD,
            "Lunar\nsurface": GOLD, "Mars\ntransfer": ORANGE, "Low Mars\norbit": ORANGE, "Mars\nsurface": ORANGE,
            "Sun–Earth\nL2": GREEN}
    edges = [("Earth\nsurface", "LEO\n(400 km)", "9.3–9.6"), ("LEO\n(400 km)", "GTO", "2.44"), ("GTO", "GEO", "1.47*"),
             ("LEO\n(400 km)", "Trans-lunar\ninjection", "3.15"), ("Trans-lunar\ninjection", "NRHO / Gateway\norbit", "0.45"),
             ("NRHO / Gateway\norbit", "Low lunar\norbit", "0.73"), ("Low lunar\norbit", "Lunar\nsurface", "1.87"),
             ("LEO\n(400 km)", "Earth escape\n(C3 = 0)", "3.22"), ("Earth escape\n(C3 = 0)", "Mars\ntransfer", "0.39–0.6"),
             ("Mars\ntransfer", "Low Mars\norbit", "2.1 (0 aerocapture)"), ("Low Mars\norbit", "Mars\nsurface", "≈4.1 (≈1 with EDL)"),
             ("Earth escape\n(C3 = 0)", "Sun–Earth\nL2", "≈0.1–0.4")]
    for a_, b_, t in edges:
        (x1, y1), (x2, y2) = nodes[a_], nodes[b_]
        ax.plot([x1, x2], [y1, y2], color="#9AA5B1", lw=3, zorder=1, solid_capstyle="round")
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.8, t, fontsize=6.6, ha="center", color=INK, zorder=3,
                bbox=dict(fc="white", ec="none", pad=0.6))
    for k, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 2.2, fc=cols[k], ec="white", lw=1.5, zorder=2))
        ax.text(x, y - 3.5, k, fontsize=6.6, ha="center", va="top", zorder=3)
    ax.text(2, 66, "Approximate Δv between states (km/s), impulsive, one way", fontsize=8.5, weight="bold", color=NAVY)
    ax.text(2, 61, "* GTO→GEO includes ≈1.47 km/s with plane change from 28.5° (less from low-latitude sites)",
            fontsize=6.4, color=GREY)
    save(fig, "ch03_dv_map")


def frames():
    fig, ax = canvas(7.0, 3.6, (0, 100), (0, 50))
    earth(ax, 25, 25, 12, z=1, land=False)
    for (dx, dy), lab in [((0, 20), "Z (spin axis)"), ((18, -6), "X → vernal equinox"), ((-14, -10), "Y")]:
        arrow(ax, (25, 25), (25 + dx, 25 + dy), color=NAVY, lw=1.2)
        ax.text(25 + dx * 1.05, 25 + dy * 1.05, lab, fontsize=7, color=NAVY)
    ax.text(3, 47, "ECI (GCRF / J2000): inertial,\norigin at Earth's centre", fontsize=7.5, va="top")
    ax.text(3, 6, "ECEF (ITRF): rotates with the Earth\n(used for ground stations and GNSS)", fontsize=7.5)
    ax.add_patch(Arc((25, 25), 54, 54, theta1=-15, theta2=55, color=ORANGE, lw=1.6))
    sx, sy = 25 + 27 * np.cos(np.radians(25)), 25 + 27 * np.sin(np.radians(25))
    satellite(ax, sx, sy, 1.0, angle=25)
    rd = np.array([np.cos(np.radians(25)), np.sin(np.radians(25))])
    td = np.array([-np.sin(np.radians(25)), np.cos(np.radians(25))])
    arrow(ax, (sx, sy), (sx + 10 * rd[0], sy + 10 * rd[1]), color=RED)
    ax.text(sx + 11 * rd[0], sy + 11 * rd[1], "R (radial)", fontsize=7, color=RED)
    arrow(ax, (sx, sy), (sx + 10 * td[0], sy + 10 * td[1]), color=GREEN)
    ax.text(sx + 11 * td[0] - 6, sy + 11 * td[1], "T / S (along-track)", fontsize=7, color=GREEN)
    ax.add_patch(Circle((sx, sy), 1.0, fc="white", ec=VIOLET, lw=1.2, zorder=8))
    ax.plot(sx, sy, ".", color=VIOLET, zorder=9)
    ax.text(sx + 2, sy - 3.5, "N / W (orbit normal, out of page)", fontsize=7, color=VIOLET)
    ax.text(62, 12, "RTN / RSW / LVLH: orbit-fixed frames used\nfor relative motion, rendezvous, attitude\n"
            "and covariance (radial, in-track, cross-track).\n\nBody frame: fixed to the spacecraft.\n"
            "Perifocal (PQW): x to periapsis, z = orbit normal.", fontsize=7.2, va="bottom")
    save(fig, "ch03_frames")


def kepler2():
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.set_aspect("equal")
    ax.axis("off")
    a, e = 3.0, 0.62
    c = a * e
    t = np.linspace(0, 2 * np.pi, 400)
    b = a * np.sqrt(1 - e ** 2)
    ax.plot(a * np.cos(t) - c, b * np.sin(t), color=BLUE, lw=1.5)
    ax.plot(0, 0, "o", color=GOLD, ms=12)
    n = 1
    T = 2 * np.pi

    def pos(tt):
        M = tt
        E = M
        for _ in range(30):
            E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        return a * np.cos(E) - c, b * np.sin(E)
    for (t0, t1), col in [((-0.35, 0.35), ORANGE), ((np.pi - 0.35, np.pi + 0.35), GREEN)]:
        ts = np.linspace(t0, t1, 50)
        pts = [pos(tt) for tt in ts]
        poly = [(0, 0)] + pts
        ax.add_patch(Polygon(poly, closed=True, fc=col, alpha=0.4, ec=col))
    ax.text(a - c + 0.2, 0, "fast near\nperiapsis", fontsize=7.5, va="center")
    ax.text(-a - c - 0.15, 0, "slow near\napoapsis", fontsize=7.5, va="center", ha="right")
    ax.text(-5.5, -2.8, "Kepler's 2nd law: equal areas in equal times (shaded areas: same Δt)", fontsize=7.5)
    ax.set_xlim(-6.6, 2.6)
    ax.set_ylim(-2.9, 2.5)
    save(fig, "ch03_kepler2")


if __name__ == "__main__":
    conics(); ellipse_geom(); elements3d(); anomalies(); speeds_periods(); perturbations(); j2_effects()
    hohmann(); hohmann_vs_bielliptic(); plane_change(); cw_motion(); ground_tracks(); tle_figure()
    res = porkchop(); print("porkchop min:", res)
    gravity_assist(); lagrange(); dv_map(); frames(); kepler2()
