import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, Wedge

ROOT = Path(__file__).resolve().parents[2]
ASAT = json.load(open(ROOT / "data/asat_debris.json"))


def functions():
    fig, ax = canvas(7.0, 4.0, xlim=(0, 100), ylim=(0, 58))
    ax.add_patch(Circle((50, 29), 9, fc=NAVY, ec="none"))
    label(ax, 50, 29, "National\nsecurity\nspace", fs=7.6, color="white", weight="bold")
    items = [("Intelligence, surveillance\n& reconnaissance", "imagery, SIGINT, MASINT", 50, 52, BLUE),
             ("Missile warning\n& tracking", "infrared satellites (Ch. 20)", 82, 44, RED),
             ("Positioning, navigation\n& timing", "military GNSS signals (Ch. 18)", 86, 27, GREEN),
             ("Satellite\ncommunications", "protected, wideband,\nnarrowband, commercial", 82, 10, VIOLET),
             ("Environmental\nmonitoring", "military weather", 50, 5, SKY),
             ("Space domain\nawareness", "tracking & characterising\nobjects (Ch. 21)", 18, 10, GOLD),
             ("Space control", "protect own systems,\ncounter adversary systems", 12, 27, ORANGE),
             ("Launch & ranges", "assured access to space", 18, 44, GREY)]
    for t, sub, x, y, c in items:
        ax.plot([50, x], [29, y], color=c, lw=1, alpha=0.6, zorder=0)
        box(ax, x - 13.5, y - 4.8, 27, 9.6, "", fc="white", ec=c, lw=1.2, z=2)
        ax.text(x, y + 1.6, t, ha="center", va="center", fontsize=6.6, weight="bold", color=c, zorder=3)
        ax.text(x, y - 2.8, sub, ha="center", va="center", fontsize=5.8, color=INK, zorder=3)
    save(fig, "ch19_functions")


def history():
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ev = [(1960.5, "GRAB\n(first SIGINT sat)"), (1960.6, "Corona film\nreturn"), (1962.3, "Zenit"),
          (1963.8, "Vela nuclear\ndetection"), (1970.9, "DSP early\nwarning"), (1976.9, "First digital\nimaging (public)"),
          (1978.2, "GPS"), (1991.1, "Gulf War: 'first\nspace war'"), (1992.7, "NRO existence\ndeclassified"),
          (1995.1, "Corona imagery\ndeclassified"), (2007.0, "Chinese\nASAT test"), (2019.97, "US Space Force"),
          (2021.9, "Russian\nASAT test"), (2022.2, "War in Ukraine:\ncommercial space")]
    timeline(ax, ev, y=0, x0=1958, x1=2028, stagger=4, height=0.95, fs=5.8)
    ax.set_xlim(1956, 2030)
    ax.set_ylim(-5.6, 5.6)
    ax.axis("off")
    for yr in range(1960, 2030, 10):
        ax.text(yr, -0.35, str(yr), fontsize=6.2, ha="center", va="top", color=GREY)
    save(fig, "ch19_history")


def tdoa_fdoa():
    c = 299792.458
    h = 600.0
    s1 = np.array([-40.0, 0.0, h])
    s2 = np.array([40.0, 0.0, h])
    v = np.array([0.0, 7.5, 0.0])
    x = np.linspace(-500, 500, 400)
    y = np.linspace(-500, 500, 400)
    X, Y = np.meshgrid(x, y)
    P = np.stack([X, Y, np.zeros_like(X)], -1)
    d1 = np.linalg.norm(P - s1, axis=-1)
    d2 = np.linalg.norm(P - s2, axis=-1)
    tdoa = (d1 - d2) / c * 1e6
    s2b = np.array([40.0, -30.0, h])
    v2 = np.array([0.0, 7.5, 0.3])
    u1 = (P - s1) / d1[..., None]
    d2b = np.linalg.norm(P - s2b, axis=-1)
    u2 = (P - s2b) / d2b[..., None]
    lam = 0.03
    fdoa = ((u1 @ v) - (u2 @ v2)) / lam * 1e3 / 1e3
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.2), gridspec_kw=dict(wspace=0.25))
    cs = a1.contour(X, Y, tdoa, levels=np.arange(-250, 251, 25), colors=BLUE, linewidths=0.7)
    a1.clabel(cs, fontsize=5.5, fmt="%d µs")
    a1.plot([s1[0], s2[0]], [s1[1], s2[1]], "s", color=NAVY, ms=6)
    a1.set_title("Time difference of arrival (TDOA)", fontsize=7.6)
    a1.set_xlabel("km", fontsize=7)
    a1.set_ylabel("km", fontsize=7)
    cs2 = a2.contour(X, Y, fdoa, levels=15, colors=ORANGE, linewidths=0.7)
    a2.contour(X, Y, tdoa, levels=np.arange(-250, 251, 25), colors=BLUE, linewidths=0.4, alpha=0.4)
    a2.plot([s1[0], s2b[0]], [s1[1], s2b[1]], "s", color=NAVY, ms=6)
    a2.set_title("Frequency difference (FDOA) curves cross TDOA curves", fontsize=7.6)
    a2.set_xlabel("km", fontsize=7)
    for a in (a1, a2):
        a.set_aspect("equal")
        a.tick_params(labelsize=6.3)
        a.plot(180, -120, "*", color=RED, ms=10)
    a1.text(190, -150, "emitter", fontsize=6.4, color=RED)
    note(a2, "Two satellites 80 km apart at 600 km altitude (squares: sub-satellite points). Each measurement "
             "places the emitter on a curve;\ncombining TDOA and FDOA (or three satellites) fixes its position.",
         xy=(1, -0.2))
    save(fig, "ch19_tdoa")


def footprint():
    D = np.logspace(0, 3, 200)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for f, c in [(0.15, RED), (1.0, ORANGE), (3.0, GREEN), (10.0, BLUE)]:
        lam = 0.3 / f
        bw = 70 * lam / D
        for R, ls in [(36000, "-"), (600, "--")]:
            fp = np.radians(bw) * R
            ax.plot(D, fp, color=c, ls=ls, lw=1.4, label=f"{f:g} GHz, {'GEO' if R > 1000 else 'LEO 600 km'}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 1000)
    ax.set_ylim(1, 1e5)
    ax.axhline(100, color=GREY, lw=0.7, ls=":")
    ax.text(1.1, 115, "100 km", fontsize=6.4, color=GREY)
    ax.set_xlabel("Receiving antenna diameter (m)")
    ax.set_ylabel("Beam footprint on the ground (km)")
    ax.legend(fontsize=6.0, ncol=2, loc="upper right")
    note(ax, "Half-power beamwidth ≈ 70 λ/D degrees. Separating emitters by beam alone from GEO requires antennas "
             "of tens to hundreds of metres.", xy=(1, -0.16))
    save(fig, "ch19_footprint")


def aoa():
    fig, ax = canvas(7.0, 3.0, xlim=(0, 100), ylim=(0, 40))
    ax.plot([30, 60], [6, 6], color=NAVY, lw=3)
    for x in (30, 60):
        ax.add_patch(Polygon([[x - 2, 6], [x + 2, 6], [x, 10]], closed=True, fc=NAVY))
    darrow(ax, (30, 3), (60, 3), color=GREY, text="baseline d", fs=6.6, toff=(0, -3.6))
    th = np.radians(35)
    for x0 in (30, 60):
        ax.plot([x0, x0 + 40 * np.sin(th)], [10, 10 + 40 * np.cos(th)], color=ORANGE, lw=1)
    ax.plot([60, 60 - 30 * np.sin(th) * np.cos(th) * 0 + 0], [10, 10], color="none")
    px = 30 + 30 * np.sin(th) ** 2
    py = 10 + 30 * np.sin(th) * np.cos(th)
    ax.plot([60, px], [10, py], color=RED, lw=1.5)
    label(ax, 52, 19, "path difference\nΔ = d sin θ", fs=6.6, color=RED)
    label(ax, 88, 34, "incoming\nwavefront\nfrom emitter", fs=6.6, color=ORANGE)
    box(ax, 66, 4, 32, 12, "Phase difference φ = 2π d sin θ / λ\nlong baselines: precise but ambiguous\n"
        "short baselines: resolve ambiguity", fs=6.3, fc="white")
    save(fig, "ch19_aoa")


def asat():
    t = ASAT["tests"]
    names = list(t)
    cat = [t[n]["catalogued"] for n in names]
    orb = [t[n]["in_orbit"] for n in names]
    alt = ["≈ 525 km", "≈ 865 km", "≈ 247 km", "≈ 283 km", "≈ 480 km"]
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    y = np.arange(len(names))
    ax.barh(y, cat, color=GREY, height=0.6, label="Debris catalogued")
    ax.barh(y, orb, color=RED, height=0.6, label="Still in orbit, Oct 2026")
    for yi, cv, ov, a in zip(y, cat, orb, alt):
        ax.text(cv + 40, yi, f"{cv:,} catalogued; {ov:,} remain  (intercept {a})", va="center", fontsize=6.4)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(0, 6200)
    ax.set_xlabel("Number of tracked fragments")
    ax.legend(fontsize=6.6, loc="lower right")
    ax.grid(axis="y", visible=False)
    note(ax, "Debris objects by international designator in the CelesTrak SATCAT. Higher-altitude tests leave "
             "long-lived debris.", xy=(1, -0.17))
    save(fig, "ch19_asat")


def antijam():
    R = np.logspace(2, 9, 200)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for W, c, n in [(1e6, SKY, "1 MHz spread (UHF)"), (1e8, BLUE, "100 MHz spread"), (2e9, NAVY, "2 GHz hop band (EHF)")]:
        pg = 10 * np.log10(W / R)
        ax.plot(R, pg, color=c, lw=1.6, label=n)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xscale("log")
    ax.set_xlabel("User data rate (bit/s)")
    ax.set_ylabel("Processing gain (dB)")
    ax.set_xlim(100, 1e9)
    ax.set_ylim(-10, 80)
    ax.legend(fontsize=6.6, loc="lower left")
    for r, n in [(2.4e3, "voice\n2.4 kbit/s"), (1e6, "video\n1 Mbit/s"), (1e8, "imagery\n100 Mbit/s")]:
        ax.axvline(r, color=GREY, lw=0.6, ls=":")
        ax.text(r * 1.15, 70, n, fontsize=6.2, color=GREY, va="top")
    note(ax, "Processing gain = 10 log(spread bandwidth / data rate): protected links trade data rate for jam "
             "resistance.", xy=(1, -0.16))
    save(fig, "ch19_antijam")


def pwsa():
    fig, ax = canvas(7.0, 3.6, xlim=(0, 100), ylim=(0, 52))
    earth(ax, 50, -52, 70, atmosphere=False)
    for i, x in enumerate(np.linspace(6, 94, 12)):
        y = 30 - 0.0045 * (x - 50) ** 2
        satellite(ax, x, y, s=0.6)
        if i < 11:
            x2 = np.linspace(6, 94, 12)[i + 1]
            ax.plot([x, x2], [y, 30 - 0.0045 * (x2 - 50) ** 2], color=VIOLET, lw=0.8, ls="--")
    for x in np.linspace(14, 86, 6):
        y = 40 - 0.0035 * (x - 50) ** 2
        satellite(ax, x, y, s=0.6, panel="#8A2A2A")
    label(ax, 50, 47.5, "Tracking layer: wide- and medium-field infrared sensors detect and track missiles", fs=6.6,
          color=RED)
    label(ax, 50, 34.5, "Transport layer: mesh of optical inter-satellite links, Ka-band and Link 16 to forces", fs=6.6,
          color=VIOLET)
    ax.plot([30, 22], [27, 13], color=GREEN, lw=1)
    ax.plot([70, 80], [27, 13], color=GREEN, lw=1)
    label(ax, 14, 18, "ships, aircraft,\nground forces", fs=6.2, color=GREEN)
    label(ax, 87, 18, "missile defence\ninterceptors", fs=6.2, color=GREEN)
    label(ax, 50, 3, "Proliferated LEO: hundreds of satellites at ≈ 1 000 km, replaced in two-year 'tranches'", fs=6.6,
          color="white")
    save(fig, "ch19_pwsa")


def counterspace():
    fig, ax = canvas(7.0, 3.6, xlim=(0, 100), ylim=(0, 52))
    cats = [("Kinetic physical", ["direct-ascent ASAT missiles", "co-orbital interceptors",
                                  "attacks on ground stations"], RED, "irreversible; debris;\nattributable"),
            ("Non-kinetic physical", ["high-power lasers (blinding)", "high-power microwaves",
                                      "nuclear detonation (EMP)"], ORANGE, "temporary to permanent;\nhard to attribute"),
            ("Electronic", ["uplink and downlink jamming", "GNSS spoofing", "meaconing"], GOLD,
             "reversible; widely used;\nlocalised"),
            ("Cyber", ["data interception", "malware in ground systems", "command takeover"], VIOLET,
             "reversible or permanent;\nvery hard to attribute")]
    for i, (n, items, c, prop) in enumerate(cats):
        x = 2 + i * 24.5
        box(ax, x, 38, 23, 9, n, fs=7.2, fc=c, ec=c, color="white", weight="bold")
        for j, it in enumerate(items):
            box(ax, x, 27 - j * 7.5, 23, 6.3, it, fs=6.2, fc="white", ec=c)
        label(ax, x + 11.5, 3.5, prop, fs=6.0, color=GREY)
    label(ax, 50, 50, "Counterspace capabilities (after public assessments by Secure World Foundation and CSIS)",
          fs=6.8, weight="bold")
    save(fig, "ch19_counterspace")


def rpo():
    n = 2 * np.pi / 86164
    t = np.linspace(0, 86164, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    for b, c, lab in [(5, BLUE, "2:1 relative ellipse, 5 km"), (2, GREEN, "2:1 relative ellipse, 2 km")]:
        x = 2 * b * np.cos(n * t)
        y = b * np.sin(n * t)
        ax.plot(x, y, color=c, lw=1.6, label=lab)
    drift_x = np.linspace(-12, 12, 100)
    ax.plot(drift_x, np.full_like(drift_x, -8), color=ORANGE, lw=1.2, ls="--", label="drift past (slightly different altitude)")
    ax.plot(0, 0, "s", color=NAVY, ms=8)
    ax.text(0.4, 0.5, "target", fontsize=6.6)
    ax.set_aspect("equal")
    ax.set_xlabel("Along-track offset (km)")
    ax.set_ylabel("Radial offset (km)")
    ax.set_xlim(-13, 13)
    ax.set_ylim(-10, 7)
    ax.legend(fontsize=6.3, loc="upper right")
    note(ax, "Clohessy–Wiltshire relative motion in GEO: natural motion circumnavigation (a 2:1 ellipse each day) "
             "lets an inspector view a target from all sides.", xy=(1, -0.16))
    save(fig, "ch19_rpo")




def regimes():
    d = json.load(open(ROOT / "data/mil_regimes.json"))["groups"]
    d = {k: v for k, v in d.items() if v}
    names = list(d)
    regs = [("LEO", BLUE), ("MEO", GREEN), ("GEO", ORANGE), ("HEO", VIOLET), ("unknown", GREY)]
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    y = np.arange(len(names))
    left = np.zeros(len(names))
    for r, c in regs:
        v = np.array([d[n].get(r, 0) for n in names])
        ax.barh(y, v, left=left, color=c, height=0.6, label=r if r != "unknown" else "orbit not published")
        left += v
    for yi, tot in zip(y, left):
        ax.text(tot + 5, yi, f"{int(tot)}", va="center", fontsize=6.6)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=6.8)
    ax.invert_yaxis()
    ax.set_xlabel("Active satellites, October 2026")
    ax.legend(fontsize=6.4, loc="lower right", ncol=2)
    ax.grid(axis="y", visible=False)
    note(ax, "Name-matched active payloads in the CelesTrak SATCAT. The US 'USA' series includes NRO proliferated "
             "satellites;\nthe Russian 'Cosmos' series includes GLONASS navigation satellites in MEO.", xy=(1, -0.17))
    save(fig, "ch19_regimes")


def revisit():
    R = 6378.137
    h = 500.0
    lam_max = np.degrees(np.arcsin((R + h) / R * np.sin(np.radians(30)))) - 30
    lat_t, lon_t = np.radians(35.0), np.radians(20.0)
    hours = 24 * 10
    res_opt, res_sar = [], []
    Ns = [1, 2, 4, 6, 8, 12, 16, 24]
    for N in Ns:
        acc_o, acc_s = [], []
        for k in range(N):
            lon, lat = ground_track(R + h, 97.4, hours=hours, raan0=-45 + 90 * k / max(N, 1), u0=37 * k, n=int(hours * 120))
            t = np.linspace(0, hours, len(lon))
            la, lo = np.radians(lat), np.radians(lon)
            cg = np.sin(la) * np.sin(lat_t) + np.cos(la) * np.cos(lat_t) * np.cos(lo - lon_t)
            vis = np.degrees(np.arccos(np.clip(cg, -1, 1))) < lam_max
            desc = np.r_[np.diff(lat) < 0, False]
            acc_s.append(t[vis])
            acc_o.append(t[vis & desc])
        for acc, res in ((acc_o, res_opt), (acc_s, res_sar)):
            tt = np.sort(np.concatenate(acc))
            if len(tt) < 2:
                res.append(np.nan)
                continue
            gaps = np.diff(tt)
            gaps = gaps[gaps > 0.3]
            res.append(np.mean(gaps) if len(gaps) else np.nan)
    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    ax.plot(Ns, res_opt, "o-", color=ORANGE, lw=1.5, label="Optical (daylight passes only)")
    ax.plot(Ns, res_sar, "s-", color=BLUE, lw=1.5, label="Radar (day and night passes)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(Ns)
    ax.set_xticklabels([str(n) for n in Ns])
    ax.set_yticks([1, 2, 4, 8, 16, 32, 64])
    ax.set_yticklabels(["1", "2", "4", "8", "16", "32", "64"])
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Number of agile satellites (sun-synchronous, 500 km, ±30° pointing)")
    ax.set_ylabel("Mean time between looks (h)")
    ax.legend(fontsize=6.5, loc="upper right")
    note(ax, "Simulated over 10 days for a target at 35° N; orbit planes spread over local times 07:30–13:30; access radius "
             f"≈ {lam_max*111:.0f} km.", xy=(1, -0.18))
    save(fig, "ch19_revisit")


if __name__ == "__main__":
    fns = [functions, history, tdoa_fdoa, footprint, aoa, asat, antijam, pwsa, counterspace, rpo, regimes, revisit]
    sel = sys.argv[1:]
    for f in fns:
        if not sel or f.__name__ in sel:
            f()
    print("ok")
