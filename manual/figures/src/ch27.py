import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse
from scipy.integrate import solve_ivp

G0 = 9.80665


# ---------- lunar powered descent (Apollo-like, ZEM/ZEV guidance) ----------
def _descent(tf, h0=15000., isp=311., m0=15100., hT=150., vT=(0., -1.), dt=0.5):
    g, R, mu = 1.62, 1737.4e3, 4.9028e12
    rp, ra = R + h0, R + 110e3
    v0 = np.sqrt(2 * mu * ra / (rp * (rp + ra)))
    x, h, vx, vh, m, t, dv, tw = 0., h0, v0, 0., m0, 0., 0., 0.
    out = []
    while t < tf - 1:
        tgo = tf - t
        geff = -(g - vx ** 2 / (R + h))
        ax = (vT[0] - vx) / tgo
        zem = hT - (h + vh * tgo + 0.5 * geff * tgo ** 2)
        zev = vT[1] - (vh + geff * tgo)
        ah = 6 * zem / tgo ** 2 - 2 * zev / tgo
        a = np.hypot(ax, ah)
        dv += a * dt
        tw = max(tw, a * m / (m0 * g))
        m -= m * a / (isp * G0) * dt
        vx += ax * dt; vh += (ah + geff) * dt; x += vx * dt; h += vh * dt; t += dt
        out.append((t, x, h, vx, vh))
    return np.array(out), dv, tw, v0


def lunar_descent():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.0), gridspec_kw=dict(width_ratios=[1.35, 1]))
    o, dv, tw, v0 = _descent(600)
    sc = a1.scatter(o[::6, 1] / 1e3, o[::6, 2] / 1e3, c=np.hypot(o[::6, 3], o[::6, 4]), cmap="viridis", s=6, zorder=3)
    cb = fig.colorbar(sc, ax=a1, pad=0.02); cb.set_label("Speed (m/s)", fontsize=6.5); cb.ax.tick_params(labelsize=6)
    for tt, txt, dx, dy in [(0, "Powered descent\ninitiation, 15 km,\n1 690 m/s", 15, -6.5), (470, "Pitch-over: landing\nsite comes into view", -230, 2.5),
                            (599, "Terminal descent", -150, 0.6)]:
        k = min(int(tt / 0.5), len(o) - 1)
        a1.annotate(txt, (o[k, 1] / 1e3, o[k, 2] / 1e3), xytext=(o[k, 1] / 1e3 + dx, o[k, 2] / 1e3 + dy), fontsize=5.9,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.set_xlabel("Distance travelled (km)"); a1.set_ylabel("Altitude (km)")
    a1.set_title("(a) A 10-minute guided descent", fontsize=7.6)
    a1.set_xlim(-20, 540); a1.set_ylim(0, 17)
    T, D, W = [], [], []
    for tf in np.arange(330, 900, 20):
        _, d, w, _ = _descent(tf)
        T.append(tf); D.append(d); W.append(w)
    a2.plot(W, D, color=RED, lw=1.8)
    a2.axhline(v0, color=GREY, ls="--", lw=0.9)
    a2.text(2.9, v0 + 12, "Orbital speed at 15 km\n(impulsive ideal)", fontsize=5.9, color=GREY, ha="right", va="bottom")
    a2.plot(tw, dv, "o", color=NAVY, ms=5)
    a2.annotate(f"Case (a): {dv:,.0f} m/s", (tw, dv), xytext=(tw + 0.25, dv + 60), fontsize=6.0,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a2.set_xlabel("Peak thrust / initial lunar weight"); a2.set_ylabel("Descent Δv (m/s)")
    a2.set_title("(b) Gravity losses fall as thrust rises", fontsize=7.6)
    a2.set_xlim(1.0, 3.0); a2.set_ylim(1650, 2150)
    fig.text(0.99, 0.01, "Simulation: Apollo-class lander (15.1 t, Isp 311 s) from a 15 × 110 km orbit to 150 m altitude "
                         "above the site, using an optimal-guidance law of the kind flown by Apollo.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch27_lunardescent")


# ---------- Mars EDL ----------
def _edl():
    g, R, H, rho0 = 3.71, 3389.5e3, 11.1e3, 0.020
    rho = lambda h: rho0 * np.exp(-h / H)
    m, A, CD, LD, bank = 3440., np.pi * 4.5 ** 2 / 4, 1.68, 0.24, np.radians(50)

    def f(t, y):
        h, v, gam = y
        D = 0.5 * rho(h) * v * v * CD * A / m
        return [v * np.sin(gam), -D - g * np.sin(gam), D * LD * np.cos(bank) / v - (g / v - v / (R + h)) * np.cos(gam)]
    ev = lambda t, y: y[1] - 420; ev.terminal = True
    s = solve_ivp(f, (0, 600), [125e3, 5330., np.radians(-15.5)], events=ev, max_step=0.5, rtol=1e-8)
    t, h, v = list(s.t), list(s.y[0]), list(s.y[1])
    acc = list(0.5 * rho(s.y[0]) * s.y[1] ** 2 * CD * A / m / G0)
    # parachute: 21.5 m disk-gap-band, drag area 0.6 x 363 m2; heat shield (≈ 400 kg) released 20 s later
    tc, hc, vc, mm = t[-1], h[-1], v[-1], m
    gam = s.y[2, -1]
    vx, vz = vc * np.cos(gam), vc * np.sin(gam)
    dt = 0.1
    while hc > 2100:
        if tc - t[-1] > 20 and mm > 3100:
            mm -= 400
        Ds = 0.5 * rho(hc) * (vx ** 2 + vz ** 2) * (0.6 * 363 + (CD * A if mm > 3100 else 0.0)) / mm
        vv = np.hypot(vx, vz)
        vx += -Ds * vx / vv * dt; vz += (-Ds * vz / vv - g) * dt
        hc += vz * dt; tc += dt
        t.append(tc); h.append(hc); v.append(np.hypot(vx, vz)); acc.append(Ds / G0)
    t_chute = s.t[-1]
    t_bss = tc
    # powered descent: decelerate to 0.75 m/s at 21 m, then sky crane to touchdown
    v1 = np.hypot(vx, vz); h1 = hc
    a_pd = (v1 ** 2 - 0.75 ** 2) / (2 * (h1 - 21))
    while hc > 21:
        v1 = max(v1 - a_pd * dt, 0.75)
        hc -= v1 * dt; tc += dt
        t.append(tc); h.append(hc); v.append(v1); acc.append(a_pd / G0)
    t_sky = tc
    while hc > 0:
        hc -= 0.75 * dt; tc += dt
        t.append(tc); h.append(hc); v.append(0.75); acc.append(0.0)
    return np.array(t), np.array(h), np.array(v), np.array(acc), t_chute, t_bss, t_sky


def mars_edl():
    t, h, v, acc, tch, tbs, tsk = _edl()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.1))
    a1.plot(t, h / 1e3, color=RED, lw=1.8, label="Altitude")
    ax2 = a1.twinx()
    ax2.semilogy(t, v, color=BLUE, lw=1.2, ls="--", label="Speed")
    ax2.set_ylabel("Speed (m/s, dashed)", color=BLUE); ax2.tick_params(axis="y", colors=BLUE, labelsize=6.5)
    ax2.set_ylim(0.5, 8000); ax2.grid(False)
    kpk = int(np.argmax(acc[:2000]))
    ev = [(t[kpk], "Peak heating and\ndeceleration", 112), (tch, "Parachute", 100), (tch + 20, "Heat shield\noff", 84),
          (tbs, "Powered\ndescent", 100), (tsk, "Sky crane", 70), (t[-1], "Touch-\ndown", 50)]
    for x, txt, y in ev:
        a1.axvline(x, color=GREY, ls=":", lw=0.7)
        a1.text(x + 3, y, txt, fontsize=5.8, color=INK, va="top")
    a1.set_xlabel("Time from entry interface (s)"); a1.set_ylabel("Altitude (km, solid)", color=RED)
    a1.set_title("(a) Altitude and speed", fontsize=7.6)
    a1.set_ylim(0, 128); a1.set_xlim(-5, t[-1] + 45)
    a2.plot(t, acc, color=NAVY, lw=1.4)
    a2.set_xlabel("Time from entry interface (s)"); a2.set_ylabel("Deceleration (g)")
    a2.set_title(f"(b) Seven minutes: entry to touchdown in {t[-1]:.0f} s", fontsize=7.6)
    for x, txt, y in [(tch, "parachute", 3.2), (tbs, "powered\ndescent", 2.2)]:
        a2.axvline(x, color=GREY, ls=":", lw=0.8)
        a2.text(x + 5, y, txt, fontsize=6.0, color=GREY)
    fig.text(0.99, 0.01, "Simulation of a Perseverance-class entry: 3.4 t, 4.5 m aeroshell, lift-to-drag 0.24, entry at "
                         "5.3 km/s and −15.5°, exponential atmosphere (scale height 11.1 km).", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch27_marsedl")


def ellipses():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.0), gridspec_kw=dict(width_ratios=[1.25, 1]))
    E = [("Mars Pathfinder (1997)", 200, 100, GREY), ("InSight (2018)", 130, 27, VIOLET), ("Phoenix (2008)", 100, 20, BLUE),
         ("Spirit (2004)", 80, 12, GREEN), ("Curiosity (2012)", 20, 7, ORANGE), ("Perseverance (2021)", 7.7, 6.6, RED)]
    for n, a, b, c in E:
        a1.add_patch(Ellipse((0, 0), a, b, fc="none", ec=c, lw=1.6))
    a1.set_xlim(-110, 110); a1.set_ylim(-60, 60); a1.set_aspect("equal")
    a1.set_xlabel("km"); a1.set_title("(a) Landing ellipses drawn to scale", fontsize=7.6)
    a1.grid(alpha=0.3)
    labs = [n for n, *_ in E]
    area = [np.pi * a * b / 4 for _, a, b, _ in E]
    a2.barh(range(len(E)), area, color=[c for *_, c in E], zorder=2)
    a2.set_xscale("log"); a2.set_yticks(range(len(E))); a2.set_yticklabels(labs, fontsize=6.3); a2.invert_yaxis()
    for i, ar in enumerate(area):
        a2.text(ar * 1.15, i, f"{ar:,.0f} km²", va="center", fontsize=6.2)
    a2.set_xlim(10, 1e5); a2.set_xlabel("Ellipse area (km², log scale)")
    a2.set_title("(b) A 400-fold improvement", fontsize=7.6)
    a2.grid(axis="y", visible=False)
    fig.text(0.99, 0.01, "Guided lifting entry (Curiosity) and terrain-relative navigation (Perseverance) shrank the ellipses; "
                         "Japan's SLIM landed within 100 m of its lunar target in 2024.", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch27_ellipses")


def tipover():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.0), gridspec_kw=dict(width_ratios=[1, 1.25]))
    a1.set_xlim(-3.2, 3.2); a1.set_ylim(-0.6, 4.2); a1.set_aspect("equal"); a1.axis("off")
    for cx, r, hh, col, nm in [(-1.6, 1.3, 1.0, BLUE, "Low and wide"), (1.6, 0.8, 2.2, RED, "Tall and narrow")]:
        a1.plot([cx - r, cx + r], [0, 0], color=INK, lw=1.2)
        a1.add_patch(Rectangle((cx - 0.55, 0.35), 1.1, 2 * hh - 0.7, fc=LIGHT, ec=col, lw=1.2))
        a1.plot([cx - r, cx - 0.55], [0, 0.6], color=col, lw=1.2); a1.plot([cx + r, cx + 0.55], [0, 0.6], color=col, lw=1.2)
        a1.plot(cx, hh, "o", color=col, ms=6)
        a1.plot([cx + r, cx], [0, hh], color=GREY, lw=0.8, ls="--")
        ang = np.degrees(np.arctan(r / hh))
        a1.text(cx, -0.45, f"{nm}\nstatic limit {ang:.0f}°", ha="center", va="top", fontsize=6.4, color=col)
        a1.text(cx + 0.12, hh + 0.12, "CG", fontsize=6, color=col)
    a1.set_title("(a) Geometry: CG height h, footprint radius r", fontsize=7.6)
    g = 1.62
    sl = np.linspace(0, 25, 200)
    for r, hh, col, nm in [(1.3, 1.0, BLUE, "Low and wide (r = 1.3 m, h = 1.0 m)"), (0.8, 2.2, RED, "Tall and narrow (r = 0.8 m, h = 2.2 m)")]:
        L = np.hypot(r, hh); k = 0.8
        phi = np.arctan(r / hh) - np.radians(sl)
        dH = np.where(phi > 0, L * (1 - np.cos(phi)), 0)
        vc = np.sqrt(2 * g * dH * (k ** 2 + L ** 2)) / hh
        a2.plot(sl, vc, color=col, lw=1.8, label=nm)
    a2.set_xlabel("Downhill slope at the landing site (°)")
    a2.set_ylabel("Lateral speed that tips the lander (m/s)")
    a2.set_title("(b) Dynamic stability on the Moon", fontsize=7.6)
    a2.legend(fontsize=5.9, loc="upper right")
    a2.set_ylim(0, 3.2)
    fig.text(0.99, 0.01, "Lander pivots about its downhill feet; it tips if the kinetic energy of rotation exceeds the work "
                         "needed to raise the CG over the pivot. Radius of gyration 0.8 m; lunar gravity.",
             ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch27_tipover")


ATTEMPTS = [  # (year, name, outcome S/P/F, operator)
    (1965, "Luna 5", "F"), (1965, "Luna 7", "F"), (1965, "Luna 8", "F"),
    (1966, "Luna 9", "S"), (1966, "Surveyor 1", "S"), (1966, "Surveyor 2", "F"), (1966, "Luna 13", "S"),
    (1967, "Surveyor 3", "S"), (1967, "Surveyor 4", "F"), (1967, "Surveyor 5", "S"), (1967, "Surveyor 6", "S"),
    (1968, "Surveyor 7", "S"), (1969, "Luna 15", "F"), (1970, "Luna 16", "S"), (1970, "Luna 17", "S"),
    (1971, "Luna 18", "F"), (1972, "Luna 20", "S"), (1973, "Luna 21", "S"), (1974, "Luna 23", "P"), (1976, "Luna 24", "S"),
    (2013, "Chang'e 3", "S"), (2019, "Chang'e 4", "S"), (2019, "Beresheet", "F"), (2019, "Vikram", "F"),
    (2020, "Chang'e 5", "S"), (2023, "Hakuto-R M1", "F"), (2023, "Luna 25", "F"), (2023, "Chandrayaan-3", "S"),
    (2024, "SLIM", "P"), (2024, "IM-1 Odysseus", "P"), (2024, "Chang'e 6", "S"), (2025, "Blue Ghost M1", "S"),
    (2025, "IM-2 Athena", "P"), (2025, "Resilience", "F")]


def lunar_attempts():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.4), sharey=True, gridspec_kw=dict(width_ratios=[12, 13]))
    col = {"S": GREEN, "P": GOLD, "F": RED}
    for ax, (x0, x1) in [(a1, (1964.5, 1976.5)), (a2, (2012.5, 2025.5))]:
        cnt = {}
        for y, n, o in ATTEMPTS:
            if x0 < y < x1:
                k = cnt.get(y, 0); cnt[y] = k + 1
                ax.add_patch(Rectangle((y - 0.42, k), 0.84, 0.9, fc=col[o], ec="white", lw=0.6, zorder=3))
                ax.text(y, k + 0.45, n, rotation=90, ha="center", va="center", fontsize=4.9,
                        color="white" if o != "P" else INK, zorder=4)
        ax.set_xlim(x0, x1); ax.set_ylim(0, 4.6)
        ax.set_xticks(range(int(x0 + 0.5), int(x1 + 0.5), 2 if x0 < 2000 else 2))
        ax.tick_params(axis="x", labelsize=6.3, rotation=0)
        ax.grid(axis="x", visible=False)
    a1.set_ylabel("Robotic soft-landing attempts")
    a1.set_yticks([])
    a1.set_title("1965–1976: USSR and USA", fontsize=7.6)
    a2.set_title("2013–2025: new nations and companies", fontsize=7.6)
    for o, lab in [("S", "Success"), ("P", "Landed but damaged or tipped over"), ("F", "Crashed or lost")]:
        a2.bar([0], [0], color=col[o], label=lab)
    a2.legend(fontsize=6.0, loc="upper left")
    fig.text(0.99, 0.01, "Excludes the six crewed Apollo landings (1969–72, all successful) and missions lost before reaching the "
                         "Moon. No lunar landing was attempted in 2026 up to October.", ha="right", va="bottom",
             fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch27_lunarattempts")


def mars_interior():
    from matplotlib.patches import Wedge
    fig, ax = canvas(6.4, 3.4, xlim=(-2, 110), ylim=(-2, 56))
    cx, cy, R = 30, 27, 26
    layers = [(3390, "#B5400F"), (3340, "#D9805C"), (1690, "#E0A040"), (1670, "#F2C66D"), (613, "#F7E3A1")]
    for r, c in layers:
        ax.add_patch(Wedge((cx, cy), R * r / 3390, 90, 270, fc=c, ec="white", lw=0.8))
    ax.plot([cx, cx], [cy - R, cy + R], color=INK, lw=0.6)
    items = [(3365, "Crust: 24–72 km thick (InSight, 2021)", 50),
             (2500, "Mantle: solid silicate rock", 40),
             (1680, "Molten silicate layer, ≈ 150 km thick, above the core (2023)", 30),
             (1150, "Liquid iron-rich core, radius ≈ 1 650–1 700 km\n(revised from 1 830 km)", 19),
             (300, "Possible solid inner core, radius ≈ 600 km\n(reported 2025; debated)", 7)]
    for r, txt, ty in items:
        y = cy + R * r / 3390 if ty > 25 else cy - R * (3390 - r) / 3390 * 0 - R * r / 3390 * (0 if ty > 25 else 1) * 0 + (cy - cy)
        y = cy + R * r / 3390 * (1 if ty > 25 else -1) if r > 700 else cy - R * r / 3390 * 0.5
        ax.plot([cx, 60], [y, ty], color=GREY, lw=0.6)
        ax.plot(cx, y, "o", color=INK, ms=2.5, zorder=4)
        label(ax, 61, ty, txt, fs=6.6, ha="left")
    label(ax, cx - 8, -1, "Mars (radius 3 390 km), interior from InSight seismology", fs=6.6, color=GREY)
    save(fig, "ch27_marsinterior")


if __name__ == "__main__":
    fns = [lunar_descent, mars_edl, ellipses, tipover, lunar_attempts, mars_interior]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
