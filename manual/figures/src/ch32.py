"""Figures for Chapter 32 — Space Stations and Habitats."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403
from matplotlib.patches import Rectangle, Polygon  # noqa: F401
import matplotlib.ticker  # noqa: E402

MU = 3.986004418e14
RE = 6378137.0
G0 = 9.80665
SIGMA = 5.670374e-8

# Thermospheric density (kg/m^3), same MSIS-like table as Chapter 2 (low / high solar activity)
ALT = np.array([100, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000])
RHO_MIN = np.array([5.3e-7, 2.2e-8, 2.0e-9, 2.1e-10, 4.0e-11, 1.0e-11, 3.0e-12, 1.0e-12, 3.5e-13, 1.3e-13,
                    2.2e-14, 5.5e-15, 2.0e-15, 9.0e-16, 5.0e-16])
RHO_MAX = np.array([5.6e-7, 2.4e-8, 2.2e-9, 3.5e-10, 1.0e-10, 3.9e-11, 1.7e-11, 7.5e-12, 3.6e-12, 1.8e-12,
                    5.0e-13, 1.6e-13, 5.5e-14, 2.1e-14, 8.5e-15])


def rho(h_km, level=0.5):
    lmin = np.interp(h_km, ALT, np.log(RHO_MIN))
    lmax = np.interp(h_km, ALT, np.log(RHO_MAX))
    return np.exp(lmin + level * (lmax - lmin))


# ISS-class station: 450 t with visiting vehicles, C_D*A ~ 3 000 m^2  -> B ~ 150 kg/m^2
M_STN = 450e3
B_STN = 150.0
ISP_CHEM = 290.0
ISP_HALL = 1600.0
LEVELS = [(0.0, BLUE, "Solar minimum"), (0.5, GREEN, "Moderate activity"), (1.0, RED, "Solar maximum")]


# ---------------------------------------------------------------------------------------------
def timeline():
    rows = [
        ("Salyut 1", 1971.30, 1971.78, RED, "s"),
        ("Skylab", 1973.37, 1979.53, BLUE, "s"),
        ("Salyut 3, 4, 5 (Almaz/DOS)", 1974.48, 1977.60, RED, "s"),
        ("Salyut 6", 1977.74, 1982.57, RED, "s"),
        ("Salyut 7", 1982.30, 1991.10, RED, "s"),
        ("Mir", 1986.14, 2001.23, RED, "s"),
        ("International Space Station", 1998.89, 2030.9, VIOLET, "s"),
        ("Tiangong-1", 2011.75, 2018.25, GOLD, "s"),
        ("Tiangong-2", 2016.71, 2019.55, GOLD, "s"),
        ("Tiangong", 2021.32, 2036.0, GOLD, "s"),
        ("Vast Haven-1 (planned)", 2027.1, 2030.1, GREEN, "p"),
        ("Axiom Station (planned)", 2028.0, 2036.0, GREEN, "p"),
        ("Starlab (planned)", 2029.0, 2036.0, GREEN, "p"),
        ("Russian ROS (planned)", 2028.0, 2036.0, RED, "p"),
        ("Bharatiya Antariksh Stn (planned)", 2028.9, 2036.0, ORANGE, "p"),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    for i, (name, t0, t1, col, kind) in enumerate(rows):
        y = len(rows) - 1 - i
        if kind == "s":
            ax.barh(y, t1 - t0, left=t0, height=0.62, color=col, alpha=0.9, zorder=2)
        else:
            ax.barh(y, t1 - t0, left=t0, height=0.62, color="white", edgecolor=col, hatch="////", lw=0.9,
                    zorder=2)
        ax.text(t0 - 0.6, y, name, ha="right", va="center", fontsize=7.0, color=INK)
    # ISS planned part hatched overlay (after 2026)
    y_iss = len(rows) - 1 - 6
    ax.barh(y_iss, 2030.9 - 2026.8, left=2026.8, height=0.62, color="none", edgecolor="white", hatch="////",
            lw=0, zorder=3)
    ax.axvline(2026.8, color=GREY, lw=0.8, ls="--", zorder=1)
    ax.text(2026.6, len(rows) - 0.35, "Oct 2026", fontsize=6.6, color=GREY, ha="right", va="bottom")
    ax.annotate("continuously crewed since Nov 2000", xy=(2000.84, y_iss - 0.31), xytext=(1999.5, y_iss - 1.0),
                ha="right", va="center",
                fontsize=6.4, color=VIOLET, arrowprops=dict(arrowstyle="-", color=VIOLET, lw=0.6))
    ax.annotate("deorbit\n≈2030–31", xy=(2030.9, y_iss), xytext=(2032.2, y_iss + 0.9), fontsize=6.4,
                color=VIOLET, arrowprops=dict(arrowstyle="-", color=VIOLET, lw=0.6))
    ax.set_xlim(1958, 2037)
    ax.set_ylim(-0.7, len(rows) - 0.1)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks(np.arange(1970, 2040, 5))
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Year")
    handles = [Rectangle((0, 0), 1, 1, color=c) for c in (RED, BLUE, VIOLET, GOLD)] + \
        [Rectangle((0, 0), 1, 1, fc="white", ec=GREEN, hatch="////")]
    ax.legend(handles, ["USSR / Russia", "USA", "International", "China", "Planned (dates uncertain)"],
              loc="lower left", fontsize=6.6, ncol=1, bbox_to_anchor=(0.0, 0.0))
    fig.text(0.99, 0.01, "Bars show time in orbit (launch to re-entry). Planned dates as reported in October 2026; "
             "Salyut 2 (failed 1973) omitted.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "ch32_timeline")


# ---------------------------------------------------------------------------------------------
def isslayout():
    fig, ax = canvas(7.0, 4.4, (0, 140), (0, 88))
    RU, US, EU, JP, CO = "#F3D3D7", "#D6E6F5", "#F6EBC8", "#D5EDDF", "#E6DDF2"
    y0, h = 40, 9
    ln = dict(color="#5B6670", lw=0.9, zorder=0)

    def mod(x, y, w, hh, name, fc, ec, fs=6.2):
        box(ax, x, y, w, hh, name, fc=fc, ec=ec, fs=fs, r=0.8, lw=0.9)

    def link(p, q):
        ax.plot([p[0], q[0]], [p[1], q[1]], **ln)

    # main axis (aft at left, forward at right)
    mod(8, y0, 18, h, "Zvezda\n(service module)", RU, RED)
    mod(27, y0, 12, h, "Zarya\n(FGB)", RU, RED)
    box(ax, 39.6, y0 + 2.7, 2.8, 3.6, "", fc="#EEE", ec="#777", r=0.4)
    mod(43, y0 - 0.5, 11, h + 1, "Unity\n(Node 1)", US, BLUE)
    mod(55, y0, 16, h, "Destiny\n(US lab)", US, BLUE)
    mod(72, y0 - 0.5, 11, h + 1, "Harmony\n(Node 2)", US, BLUE)
    box(ax, 83.4, y0 + 2.7, 2.8, 3.6, "", fc="#EEE", ec="#777", r=0.4)
    ax.text(41, y0 - 1.8, "PMA-1", ha="center", va="top", fontsize=5.6, color=GREY)
    # Russian side ports
    mod(12.5, y0 + 13, 9, 7, "Poisk", RU, RED)
    link((17, y0 + h), (17, y0 + 13))
    mod(8, y0 - 16, 18, 8, "Nauka (MLM)", RU, RED)
    link((17, y0), (17, y0 - 8))
    mod(12, y0 - 28, 10, 6.5, "Prichal", RU, RED)
    link((17, y0 - 16), (17, y0 - 21.5))
    mod(28, y0 - 13, 10, 7, "Rassvet", RU, RED)
    link((33, y0), (33, y0 - 6))
    # Unity side ports
    mod(42, y0 + 18, 14, 8, "Tranquility\n(Node 3)", US, BLUE)
    link((48.5, y0 + h + 0.5), (48.5, y0 + 18))
    mod(29, y0 + 19, 10, 6, "BEAM", CO, VIOLET)
    link((39, y0 + 22), (42, y0 + 22))
    mod(58, y0 + 19, 10.5, 6, "Leonardo", US, BLUE)
    link((56, y0 + 22), (58, y0 + 22))
    mod(40, y0 + 30, 9, 5.5, "Bishop", CO, VIOLET, fs=6.0)
    link((44.5, y0 + 26), (44.5, y0 + 30))
    mod(50, y0 + 30, 9, 5.5, "Cupola", US, BLUE, fs=6.0)
    link((54.5, y0 + 26), (54.5, y0 + 30))
    mod(42, y0 - 13, 8, 7, "Quest\nairlock", US, BLUE, fs=5.9)
    link((46, y0 - 0.5), (46, y0 - 6))
    mod(51, y0 - 13, 7, 7, "CBM\nport", "#F4F6F8", GREY, fs=5.7)
    link((52, y0 - 0.5), (54.5, y0 - 6))
    # Harmony side ports
    mod(73.5, y0 + 13, 8, 7, "PMA-3\nIDA-3", "#EEE", "#777", fs=5.7)
    link((77.5, y0 + h + 0.5), (77.5, y0 + 13))
    mod(87, y0 + 13, 17, 8, "Kibo PM (JAXA)", JP, GREEN)
    link((82, y0 + h + 0.5), (87, y0 + 16))
    mod(89.5, y0 + 24, 12, 5.5, "Kibo ELM", JP, GREEN, fs=6.0)
    link((95.5, y0 + 21), (95.5, y0 + 24))
    mod(107, y0 + 13.5, 13, 7, "Kibo exposed\nfacility", JP, GREEN, fs=5.8)
    link((104, y0 + 17), (107, y0 + 17))
    mod(73.5, y0 - 13, 8, 7, "CBM\nport", "#F4F6F8", GREY, fs=5.7)
    link((77.5, y0 - 0.5), (77.5, y0 - 6))
    mod(87, y0 - 13, 17, 8, "Columbus (ESA)", EU, GOLD)
    link((82, y0 - 0.5), (87, y0 - 9))
    # truss
    box(ax, 57, y0 + 37, 32, 7, "Integrated truss (S0 on Destiny): 109 m,\n8 array wings + iROSAs, radiators",
        fc="#E3E7EB", ec="#5B6670", fs=5.8, r=0.6)
    link((70, y0 + h), (70, y0 + 37))
    # visiting vehicles
    vv = dict(fontsize=5.8, color=ORANGE, style="italic")
    ax.text(7, y0 + 4.5, "Soyuz/\nProgress", ha="right", va="center", **vv)
    ax.text(22.5, y0 + 16.5, "Soyuz/Progress", ha="left", va="center", **vv)
    ax.text(23, y0 - 24.8, "Soyuz/Progress", ha="left", va="center", **vv)
    ax.text(33, y0 - 14.5, "Soyuz/\nProgress", ha="center", va="top", **vv)
    ax.text(54.5, y0 - 14.5, "Cygnus", ha="center", va="top", **vv)
    ax.text(77.5, y0 - 14.5, "HTV-X /\nCygnus", ha="center", va="top", **vv)
    ax.text(77.5, y0 + 21, "Dragon", ha="center", va="bottom", **vv)
    ax.text(87.2, y0 + 4.5, "Crew / Cargo Dragon,\nStarliner", ha="left", va="center", **vv)
    ax.text(14, 3, "Russian Orbital Segment", ha="center", fontsize=7.4, color=RED, weight="bold")
    ax.text(82, 3, "US Orbital Segment (NASA, ESA, JAXA, CSA)", ha="center", fontsize=7.4, color=BLUE,
            weight="bold")
    ax.plot([41, 41], [8, 84], color=GREY, lw=0.6, ls=":")
    arrow(ax, (110, 26), (132, 26), "forward (flight direction)", color=NAVY, fs=6.2)
    ax.text(121, 21, "Schematic, not to scale.\nAbove axis: zenith or port ports;\nbelow axis: nadir or "
            "starboard ports.", ha="center", va="top", fontsize=5.9, color=GREY)
    save(fig, "ch32_isslayout")


# ---------------------------------------------------------------------------------------------
def decay():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.3))
    for lv, col, lab in LEVELS:
        a = RE + 420e3
        t = 0.0
        ts, hs = [0.0], [420.0]
        while a - RE > 200e3 and t < 8 * 3.156e7:
            hk = (a - RE) / 1e3
            dadt = -rho(hk, lv) * np.sqrt(MU * a) / B_STN
            dt = 6 * 3600.0
            a += dadt * dt
            t += dt
            ts.append(t / 86400.0)
            hs.append((a - RE) / 1e3)
        ax1.plot(np.array(ts) / 365.25, hs, color=col, label=lab)
        ax1.plot(ts[-1] / 365.25, hs[-1], "o", color=col, ms=3)
        ax1.text(ts[-1] / 365.25 + 0.15, hs[-1] + 4, f"{ts[-1] / 365.25:.1f} yr", fontsize=6.4, color=col,
                 ha="left", va="bottom")
    ax1.set_xlabel("Years without reboost")
    ax1.set_ylabel("Altitude (km)")
    ax1.set_ylim(190, 430)
    ax1.set_xlim(0, 7)
    ax1.set_title("(a) Decay from 420 km", fontsize=8.6, loc="left")
    ax1.legend(loc="lower center", fontsize=6.6, bbox_to_anchor=(0.70, 0.03))
    h = np.linspace(340, 500, 161)
    for lv, col, lab in LEVELS:
        a = RE + h * 1e3
        v = np.sqrt(MU / a)
        dv = rho(h, lv) * v ** 2 / (2 * B_STN) * 3.156e7
        mp = M_STN * (1 - np.exp(-dv / (G0 * ISP_CHEM)))
        ax2.plot(h, mp / 1e3, color=col, label=lab)
    a = RE + h * 1e3
    v = np.sqrt(MU / a)
    dvm = rho(h, 0.5) * v ** 2 / (2 * B_STN) * 3.156e7
    mpi = M_STN * (1 - np.exp(-dvm / (G0 * ISP_HALL)))
    ax2.plot(h, mpi / 1e3, color=GREEN, ls="--", lw=1.2, label="Moderate, Hall thrusters")
    ax2.set_yscale("log")
    ax2.set_ylim(0.05, 40)
    ax2.set_xlim(340, 500)
    ax2.set_xlabel("Altitude (km)")
    ax2.set_ylabel("Reboost propellant (t per year)")
    ax2.set_title("(b) Propellant to hold altitude", fontsize=8.6, loc="left")
    for x, t in [(385, "Tiangong"), (415, "ISS")]:
        ax2.axvline(x, color=GREY, lw=0.6, ls=":")
        ax2.text(x + 2, 0.06, t, fontsize=6.4, color=GREY, rotation=90, va="bottom")
    ax2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax2.legend(loc="upper right", fontsize=6.2)
    fig.text(0.99, 0.01, "Model: da/dt = −ρ√(μa)/B with B = m/(C_D A) = 150 kg/m² (450 t, C_D A ≈ 3 000 m²); "
             "MSIS-like density table of Chapter 2; chemical I_sp = 290 s, Hall I_sp = 1 600 s.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch32_decay")


# ---------------------------------------------------------------------------------------------
def powerthermal():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.25))
    h = 420.0
    r = RE / 1e3 + h
    P = 2 * np.pi * np.sqrt((r * 1e3) ** 3 / MU) / 60
    beta = np.linspace(0, 80, 401)
    bstar = np.degrees(np.arcsin(RE / 1e3 / r))
    arg = np.sqrt(h * h + 2 * RE / 1e3 * h) / (r * np.cos(np.radians(beta)))
    fe = np.where(beta < bstar, np.degrees(np.arccos(np.clip(arg, -1, 1))) / 180, 0.0)
    te = fe * P
    td = P - te
    ratio = (te / 0.65 + td / 0.85) / td
    ax1.plot(beta, te, color=NAVY, label="Eclipse duration (min)")
    ax1.set_xlabel("Solar beta angle β (degrees)")
    ax1.set_ylabel("Eclipse per orbit (min)", color=NAVY)
    ax1.set_ylim(0, 60)
    ax1.set_xlim(0, 80)
    ax1r = ax1.twinx()
    ax1r.plot(beta, ratio, color=ORANGE, label="Array power / average load")
    ax1r.set_ylabel("Array power ÷ orbit-average load", color=ORANGE)
    ax1r.set_ylim(1.0, 2.4)
    ax1r.spines["right"].set_visible(True)
    ax1r.grid(False)
    ax1.axvline(bstar, color=GREY, lw=0.6, ls=":")
    ax1.text(bstar - 1.5, 57, f"no eclipse\nabove β ≈ {bstar:.0f}°", fontsize=6.3, color=GREY, ha="right",
             va="top")
    ax1.text(2, 31.5, f"eclipse {te[0]:.0f} min of {P:.0f} min", fontsize=6.4, color=NAVY, va="top")
    ax1.text(2, 56.5, f"array ≈ {ratio[0]:.2f} × load", fontsize=6.4, color=ORANGE, va="top")
    ax1.set_title("(a) Eclipses at 420 km", fontsize=8.6, loc="left")
    T = np.linspace(263, 333, 200)
    for Ts, col, lab in [(150, BLUE, "Sink 150 K (edge-on to Earth)"), (220, GREEN, "Sink 220 K"),
                         (250, RED, "Sink 250 K (sunlit, Earth view)")]:
        q = 0.85 * SIGMA * (T ** 4 - Ts ** 4) * 0.85  # emissivity 0.85, fin efficiency 0.85
        ax2.plot(T - 273.15, 10e3 / q, color=col, label=lab)
    ax2.set_yscale("log")
    ax2.set_ylim(15, 1000)
    ax2.set_xlim(-10, 60)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax2.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax2.set_xlabel("Radiator temperature (°C)")
    ax2.set_ylabel("Radiating area per 10 kW (m²)")
    ax2.set_title("(b) Radiator area", fontsize=8.6, loc="left")
    ax2.axvspan(0, 6, color=SKY, alpha=0.25)
    ax2.text(6.8, 18, "ammonia\nloops ≈ 0–6 °C", fontsize=6.3, color=NAVY, va="bottom")
    ax2.legend(loc="upper right", fontsize=6.0)
    fig.text(0.99, 0.01, "(a) Path efficiencies 0.65 (via battery) and 0.85 (direct). (b) q = ε η σ(T⁴ − T_sink⁴), "
             "ε = 0.85, fin efficiency η = 0.85; one radiating face.", ha="right", va="bottom", fontsize=5.9,
             color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch32_powerthermal")


# ---------------------------------------------------------------------------------------------
def whipple_dc(V, th=0.0, tb=0.16, tw=0.32, S=10.0, sig=57.0, rp=2.8, rb=2.7):
    """Christiansen (NASA) Whipple ballistic limit, cm. tb, tw, S in cm; sigma in ksi; V km/s."""
    c = np.cos(np.radians(th))

    def bal(v):
        return ((tw * (sig / 40) ** 0.5 + tb) / (0.6 * c ** (5 / 3) * rp ** 0.5 * v ** (2 / 3))) ** (18 / 19)

    def hyp(v):
        return 3.918 * tw ** (2 / 3) * rp ** (-1 / 3) * rb ** (-1 / 9) * (v * c) ** (-2 / 3) * S ** (1 / 3) * \
            (sig / 70) ** (1 / 3)
    vl, vh = 3 / c ** 0.5, 7 / c ** (1 / 3)
    if V <= vl:
        return bal(V)
    if V >= vh:
        return hyp(V)
    return bal(vl) + (hyp(vh) - bal(vl)) * (V - vl) / (vh - vl)


def single_dc(V, th=0.0, t=0.48, BH=95, rp=2.8, rt=2.7, C=5.1, k=1.8):
    """Cour-Palais thin-plate perforation limit (k = 1.8), cm."""
    vn = V * np.cos(np.radians(th))
    return (t / (k * 5.24 * BH ** -0.25 * (rp / rt) ** 0.5 * (vn / C) ** (2 / 3))) ** (18 / 19)


def flux(dcm):
    """Illustrative cumulative MMOD flux at ISS altitude (Chapter 2 model), per m^2 per year."""
    deb = 0.6 * (dcm / 0.01) ** -2.3 * ((dcm / 0.1) ** 0.35 if dcm > 0.1 else 1.0)
    met = 0.2 * (dcm / 0.01) ** -2.6 * ((dcm / 0.1) ** -0.4 if dcm > 0.1 else 1.0)
    return deb + met


def mmod():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.3))
    V = np.linspace(1.5, 15, 300)
    w0 = [whipple_dc(v, 0) * 10 for v in V]
    w45 = [whipple_dc(v, 45) * 10 for v in V]
    s0 = [single_dc(v, th=0) * 10 for v in V]
    ax1.plot(V, w0, color=BLUE, label="Whipple, normal impact")
    ax1.plot(V, w45, color=BLUE, ls="--", lw=1.2, label="Whipple, 45°")
    ax1.plot(V, s0, color=RED, label="Single wall, same mass")
    ax1.axhline(13, color=GREEN, lw=1.0, ls="-.")
    ax1.text(1.8, 13.3, "ISS stuffed Whipple ≈ 13 mm (design point)", fontsize=6.3, color=GREEN, ha="left",
             va="bottom")
    for x, t in [(2.25, "ballistic"), (5, "shatter"), (11, "melt / vaporise")]:
        ax1.text(x, 0.3, t, fontsize=6.2, color=GREY, ha="center")
    ax1.axvspan(3, 7, color=LIGHT, alpha=0.8, zorder=0)
    ax1.set_xlim(1.5, 15)
    ax1.set_ylim(0, 15)
    ax1.set_xlabel("Impact speed (km/s)")
    ax1.set_ylabel("Critical aluminium sphere diameter (mm)")
    ax1.set_title("(a) Ballistic limit", fontsize=8.6, loc="left")
    ax1.legend(loc="upper right", fontsize=6.3, bbox_to_anchor=(1.0, 0.84))
    # (b) PNP vs exposure time for 100 m^2
    yrs = np.linspace(0, 15, 200)
    A = 100.0
    for d, col, lab in [(single_dc(9, th=45), RED, "Single wall"), (whipple_dc(9, 45), BLUE, "Whipple"),
                        (1.3, GREEN, "Stuffed Whipple")]:
        F = flux(d)
        ax2.plot(yrs, np.exp(-F * A * yrs), color=col, label=f"{lab}: d_c = {d * 10:.1f} mm")
        ax2.plot(10, np.exp(-F * A * 10), "o", color=col, ms=3.5)
        pv = np.exp(-F * A * 10)
        ax2.text(10.3, pv + (0.015 if pv > 0.95 else -0.02), f"{pv:.2f}", fontsize=6.4, color=col,
                 va="bottom" if pv > 0.95 else "top")
    ax2.set_ylim(0, 1.04)
    ax2.set_xlim(0, 15)
    ax2.set_xlabel("Exposure time (years)")
    ax2.set_ylabel("Probability of no penetration")
    ax2.set_title("(b) 100 m² module", fontsize=8.6, loc="left")
    ax2.legend(loc="lower left", fontsize=6.2)
    fig.text(0.99, 0.01, "Shield: 1.6 mm Al bumper, 10 cm gap, 3.2 mm Al 2219 wall (single wall 4.8 mm). "
             "Christiansen/Cour-Palais equations; flux from Chapter 2 model; (b) at 9 km/s, 45°.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch32_mmod")


# ---------------------------------------------------------------------------------------------
def volume():
    pts = [  # name, habitable volume per person (m^3), longest single stay (days), colour, label offset
        ("Skylab", 120.0, 84, BLUE, (6, 2)),
        ("Mir", 45.0, 438, RED, (6, -6)),
        ("Salyut 7", 33.5, 237, RED, (6, -6)),
        ("ISS (388 m³, 7 crew)", 388 / 7, 374, VIOLET, (-10, 8)),
        ("Tiangong (122 m³, 3 crew)", 122 / 3, 186, GOLD, (-12, 9)),
        ("Haven-1 (45 m³, 4 crew)", 45 / 4, 14, GREEN, (6, 3)),
        ("Orion (≈9 m³, 4 crew)", 9 / 4, 21, GREY, (6, -2)),
    ]
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for name, v, d, col, off in pts:
        ax.plot(d, v, "o", color=col, ms=6, zorder=3)
        ax.annotate(name, (d, v), xytext=off, textcoords="offset points", fontsize=6.8, color=col,
                    ha="left" if off[0] > 0 else "right", va="center")
    ax.axhline(25, color=ORANGE, lw=1.1, ls="--")
    ax.text(5.5, 27, "NASA HRP minimum for a 912-day Mars mission: 25 m³ per person", fontsize=6.6,
            color=ORANGE, va="bottom")
    ax.axvline(912, color=ORANGE, lw=0.6, ls=":")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(5, 1500)
    ax.set_ylim(1, 300)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("Longest single stay or design duration (days)")
    ax.set_ylabel("Habitable volume per person (m³)")
    fig.text(0.99, 0.01, "Skylab, Salyut, Mir per-person values from the NASA HRP consensus report (2014); "
             "others computed from habitable volume ÷ nominal crew. Durations: record stays or design values.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch32_volume")


# ---------------------------------------------------------------------------------------------
def logistics():
    rows = [  # name, up (t), down (t), status
        ("Progress MS", 2.5, 0.0, "op"),
        ("Cygnus (enhanced)", 3.75, 0.0, "op"),
        ("Cygnus XL", 5.0, 0.0, "op"),
        ("HTV-X", 5.8, 0.0, "op"),
        ("Cargo Dragon", 6.0, 3.0, "op"),
        ("Tianzhou", 6.9, 0.0, "op"),
        ("Dream Chaser", 5.5, 1.85, "plan"),
        ("HTV (Kounotori)", 6.0, 0.0, "ret"),
        ("ATV", 7.7, 0.0, "ret"),
        ("Shuttle + MPLM", 9.0, 9.0, "ret"),
    ]
    fig, ax = plt.subplots(figsize=(6.8, 3.5))
    y = np.arange(len(rows))[::-1]
    for yi, (n, up, dn, st) in zip(y, rows):
        cu = {"op": BLUE, "plan": SKY, "ret": "#B6C0C9"}[st]
        cd = {"op": ORANGE, "plan": GOLD, "ret": "#D9C8B4"}[st]
        ax.barh(yi + 0.18, up, height=0.34, color=cu, zorder=2, hatch="///" if st == "plan" else None,
                edgecolor="white" if st == "plan" else None)
        ax.text(up + 0.08, yi + 0.18, f"{up:g}", va="center", fontsize=6.4)
        if dn > 0:
            ax.barh(yi - 0.18, dn, height=0.34, color=cd, zorder=2)
            ax.text(dn + 0.08, yi - 0.18, f"{dn:g}", va="center", fontsize=6.4)
        else:
            ax.text(0.08, yi - 0.18, "burns up with waste", va="center", fontsize=6.0, color=GREY, style="italic")
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.2)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 10.5)
    ax.set_xlabel("Cargo mass per flight (t)")
    ax.axhline(2.5, color=GREY, lw=0.6, ls=":")
    ax.text(10.4, 2.62, "planned / retired below", fontsize=6.2, color=GREY, ha="right", va="bottom")
    handles = [Rectangle((0, 0), 1, 1, color=BLUE), Rectangle((0, 0), 1, 1, color=ORANGE)]
    ax.legend(handles, ["Up-mass (to station)", "Down-mass (returned to Earth)"], loc="upper right", fontsize=6.6)
    fig.text(0.99, 0.01, "Maximum or typical capacities from operator data; Progress includes propellant and water; "
             "ATV up to 7.7 t including refuelling propellant. Dream Chaser not yet flown.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch32_logistics")


# ---------------------------------------------------------------------------------------------
def gravity():
    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    r = np.logspace(0, 3.2, 400)
    ax.axhspan(0.1, 2, color=GREEN, alpha=0.10, zorder=0)
    ax.axhspan(2, 6, color=GOLD, alpha=0.12, zorder=0)
    ax.axhspan(6, 60, color=RED, alpha=0.08, zorder=0)
    ax.text(1.15, 1.75, "≤ 2 rpm: comfortable for nearly everyone", fontsize=6.4, color=GREEN, va="top")
    ax.text(1.15, 5.4, "2–6 rpm: acceptable after adaptation", fontsize=6.4, color="#8A6D12", va="top")
    ax.text(1400, 52, "> 6 rpm: motion sickness likely", fontsize=6.4, color=RED, va="top", ha="right")
    for gg, col, lab in [(0.38, VIOLET, "0.38 g (Mars)"), (1.0, NAVY, "1 g")]:
        w = np.sqrt(gg * G0 / r)
        ax.plot(r, w * 60 / (2 * np.pi), color=col, lw=1.5 if gg == 1 else 1.1)
        xl = 1100 if gg == 1.0 else 150
        yy = np.sqrt(gg * G0 / xl) * 60 / (2 * np.pi)
        if gg == 1.0:
            ax.text(xl, yy * 1.1, lab, fontsize=6.6, color=col, ha="center", va="bottom")
        else:
            ax.text(xl, yy / 1.15, lab, fontsize=6.6, color=col, ha="center", va="top", rotation=-20)
    w = 6.0 / r
    ax.plot(r, w * 60 / (2 * np.pi), color=GREY, lw=0.9, ls="--")
    ax.text(40, 1.13, "rim speed 6 m/s", fontsize=6.2, color=GREY, ha="center", va="center", rotation=-37)
    pts = [
        (223.6, 2.0, "1 g at 2 rpm: r = 224 m", (420, 4.0)),
        (55.9, 4.0, "1 g at 4 rpm: r = 56 m", (110, 10.0)),
        (830, 1.0, "Stanford torus (1975 study):\nr ≈ 830 m, 1 rpm, 1 g", (420, 0.42)),
        (38, 3.0, "von Braun wheel (1952):\nr ≈ 38 m, 3 rpm, ≈ 0.38 g", (3.5, 0.75)),
        (2.8, 17.9, "short-arm human centrifuge\n(1 g at the feet)", (4.5, 32.0)),
    ]
    for x, yv, t, (tx, ty) in pts:
        ax.plot(x, yv, "o", color=ORANGE, ms=4.5, zorder=4)
        ax.annotate(t, (x, yv), xytext=(tx, ty), textcoords="data", fontsize=6.3, color=INK, ha="left",
                    va="center", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6, shrinkA=2, shrinkB=3))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 1500)
    ax.set_ylim(0.3, 60)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("Radius of rotation (m)")
    ax.set_ylabel("Rotation rate (rpm)")
    fig.text(0.99, 0.01, "ω = √(a/r). Comfort bands follow limits commonly quoted in the artificial-gravity literature "
             "(compiled by T. W. Hall); individual tolerance varies.", ha="right", va="bottom", fontsize=5.9,
             color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch32_gravity")


if __name__ == "__main__":
    fns = [timeline, isslayout, decay, powerthermal, mmod, volume, logistics, gravity]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
