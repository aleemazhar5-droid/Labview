import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403


def adcs_loop():
    fig, ax = canvas(7.2, 3.3, (0, 100), (0, 44))
    box(ax, 2, 26, 14, 10, "Commanded\nattitude\n(guidance)", fc="#F3EFF9", ec=VIOLET, fs=7)
    ax.add_patch(Circle((22, 31), 2.2, fc="white", ec=NAVY))
    ax.text(22, 31, "Σ", ha="center", va="center", fontsize=9)
    box(ax, 28, 26, 16, 10, "Controller\n(PID, LQR, MPC;\nmomentum mgmt)", fc="#E8F1FA", ec=BLUE, fs=6.8)
    box(ax, 50, 26, 16, 10, "Actuators\nwheels, CMGs,\nthrusters, MTQs", fc="#FCF3EA", ec=ORANGE, fs=6.8)
    box(ax, 72, 26, 24, 10, "Spacecraft dynamics\nIω̇ + ω × Iω = T", fc=NAVY, ec=NAVY, color="white", fs=7.2)
    box(ax, 72, 6, 24, 10, "Sensors\nstar trackers, gyros, Sun\nsensors, magnetometers, GNSS", fc="#EEF7F1", ec=GREEN,
        fs=6.6)
    box(ax, 36, 6, 24, 10, "Estimator\n(extended / multiplicative\nKalman filter)", fc="#E8F1FA", ec=BLUE, fs=6.6)
    arrow(ax, (16, 31), (19.8, 31), color=NAVY)
    arrow(ax, (24.2, 31), (28, 31), color=NAVY)
    arrow(ax, (44, 31), (50, 31), color=NAVY)
    arrow(ax, (66, 31), (72, 31), color=NAVY)
    arrow(ax, (84, 26), (84, 16), color=NAVY)
    arrow(ax, (72, 11), (60, 11), color=NAVY)
    arrow(ax, (36, 11), (22, 11), None, color=NAVY)
    arrow(ax, (22, 11), (22, 28.8), color=NAVY)
    ax.text(23, 25.5, "−", fontsize=9)
    ax.text(84, 38.5, "disturbance torques: gravity gradient, drag,\nsolar pressure, magnetic, propellant slosh",
            fontsize=6.6, ha="center", color=RED)
    arrow(ax, (84, 40), (84, 36), color=RED, lw=0.9, ms=7)
    ax.text(24, 13, "estimated attitude & rate", fontsize=6.5, color=GREY)
    save(fig, "ch06_adcs_loop")


def sensor_accuracy():
    items = [("Magnetometer (+ model)", 0.3, 5, GREY), ("Coarse Sun sensor", 1, 10, GOLD), ("Fine Sun sensor", 0.005, 0.1, ORANGE),
             ("Earth horizon sensor", 0.03, 0.3, GREEN), ("GNSS multi-antenna attitude", 0.1, 1, SKY),
             ("Star tracker (cross-boresight)", 0.0003, 0.003, BLUE), ("Fine guidance sensor (telescopes)", 2e-6, 3e-5, NAVY),
             ("MEMS gyro (rate, drift over 1 h)", 1, 10, VIOLET), ("Fibre-optic / HRG gyro (drift over 1 h)", 0.0005, 0.01, RED)]
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    for k, (n, lo, hi, c) in enumerate(items):
        ax.barh(k, hi - lo, left=lo, color=c, height=0.55)
        ax.text(hi * 1.3, k, n, va="center", fontsize=7.2)
    ax.set_xscale("log")
    ax.set_xlim(1e-6, 1e3)
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_xlabel("Typical accuracy (degrees, log scale)")
    for v, t in [(1 / 3600, "1 arcsec"), (1 / 60, "1 arcmin"), (1, "1°")]:
        ax.axvline(v, color=GREY, lw=0.5, ls=":")
        ax.text(v, -0.9, t, fontsize=6.6, color=GREY, ha="center")
    ax.grid(axis="y", visible=False)
    save(fig, "ch06_sensor_accuracy")


def disturbances():
    h = np.linspace(300, 40000, 400)
    R = 6378e3
    mu = 3.986e14
    r = R + h * 1e3
    Iz, Iy = 1500.0, 900.0
    gg = 1.5 * mu / r ** 3 * abs(Iz - Iy) * np.sin(np.radians(2 * 1.0))
    srp = 4.56e-6 * 1.5 * 8.0 * 0.3 * np.ones_like(h)
    B = 3.1e-5 * (R / r) ** 3 * 2
    mag = 1.0 * B
    import importlib.util
    spec = importlib.util.spec_from_file_location("c2", Path(__file__).parent / "ch02.py")
    c2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c2)
    aero = []
    for hh, rr in zip(h, r):
        rho = c2.rho(min(hh, 1000), 0.5) * (np.exp(-(hh - 1000) / 300) if hh > 1000 else 1)
        v = np.sqrt(mu / rr)
        aero.append(0.5 * rho * v ** 2 * 2.2 * 8.0 * 0.3)
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    ax.loglog(h, gg, color=BLUE, label="Gravity gradient (1° off principal axes)")
    ax.loglog(h, aero, color=RED, label="Aerodynamic (8 m², 0.3 m offset)")
    ax.loglog(h, srp, color=ORANGE, label="Solar radiation pressure (8 m², 0.3 m offset)")
    ax.loglog(h, mag, color=VIOLET, label="Magnetic (1 A·m² residual dipole)")
    ax.set_ylim(1e-9, 1e-2)
    ax.set_xlabel("Altitude (km)")
    ax.set_ylabel("Disturbance torque (N·m)")
    ax.legend(fontsize=7)
    note(ax, "Example 1 000 kg spacecraft (I = 900–1 500 kg·m²); order-of-magnitude, worst-case formulas from SMAD.",
         xy=(1, -0.16))
    save(fig, "ch06_disturbances")


def wheel_pyramid():
    fig, ax = canvas(6.4, 3.2, (0, 100), (0, 48))
    ax.add_patch(Polygon([(20, 8), (60, 8), (72, 20), (32, 20)], fc="#EAF1F7", ec=NAVY))
    for (x, y), ang in [((26, 11), 35), ((54, 11), 145), ((36, 18), 60), ((64, 18), 120)]:
        e = Ellipse((x, y + 8), 9, 4.2, angle=0, fc="#C9D3DD", ec=NAVY, lw=1)
        ax.add_patch(e)
        dx, dy = 8 * np.cos(np.radians(ang)), 12 * np.sin(np.radians(ang))
        arrow(ax, (x, y + 8), (x + dx * 0.6, y + 8 + dy), color=ORANGE, lw=1.4, ms=8)
    ax.text(46, 44, "Four reaction wheels in a pyramid: any three give 3-axis control;\nthe fourth adds redundancy "
            "and extra momentum capacity", fontsize=7, ha="center")
    ax.text(78, 26, "spin axes tilted\n≈ 54.7° (or 60°)\nfrom the base", fontsize=6.8, color=ORANGE)
    ax.text(46, 3, "Wheel: 0.1–0.3 N·m torque, 4–200 N·m·s momentum, ±6 000 rpm", fontsize=6.8, ha="center", color=GREY)
    save(fig, "ch06_wheels")


def isp_thrust():
    tech = [("Cold gas", 1e-3, 10, 40, 75, GREY), ("Hydrazine monoprop", 0.1, 500, 200, 235, BLUE),
            ("Green monoprop (AF-M315E, LMP-103S)", 0.1, 30, 235, 255, GREEN),
            ("Storable biprop (MMH/NTO)", 5, 5e4, 285, 330, NAVY), ("Solid rocket motor", 1e2, 1.5e7, 250, 300, GOLD),
            ("Cryogenic biprop (LOX/LH₂)", 1e4, 2.5e6, 420, 465, SKY), ("Methalox (LOX/CH₄)", 1e4, 2.6e6, 330, 380, "#8C564B"),
            ("Resistojet / arcjet", 0.05, 1, 300, 800, RED), ("Hall thruster", 0.01, 5, 1200, 2800, ORANGE),
            ("Gridded ion engine", 0.001, 0.5, 2500, 4500, VIOLET), ("Electrospray / FEEP", 1e-6, 1e-3, 1500, 8000, "#E377C2"),
            ("Nuclear thermal (NERVA, tested)", 1e4, 3.3e5, 800, 900, "#17BECF")]
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    pos = {"Storable biprop (MMH/NTO)": (2e2, 150, "center"), "Solid rocket motor": (3e5, 205, "center"),
           "Cryogenic biprop (LOX/LH₂)": (3e5, 560, "center"), "Methalox (LOX/CH₄)": (2e6, 355, "left"),
           "Hydrazine monoprop": (0.3, 170, "center"), "Green monoprop (AF-M315E, LMP-103S)": (1e-2, 300, "center"),
           "Nuclear thermal (NERVA, tested)": (2e4, 1000, "center")}
    for n, f1, f2, i1, i2, c in tech:
        ax.add_patch(Rectangle((f1, i1), f2 - f1, i2 - i1, fc=c, ec=c, alpha=0.35))
        x, y, ha = pos.get(n, (np.sqrt(f1 * f2), np.sqrt(i1 * i2), "center"))
        ax.text(x, y, n, fontsize=6.4, ha=ha, va="center", color=INK)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(5e-7, 3e7)
    ax.set_ylim(30, 1.2e4)
    ax.set_xlabel("Thrust per thruster (N)")
    ax.set_ylabel("Specific impulse Isp (s)")
    note(ax, "Typical in-space operating ranges. Chemical propulsion: high thrust, low Isp; electric propulsion: "
             "low thrust, high Isp.", xy=(1, -0.15))
    save(fig, "ch06_isp_thrust")


def rocket_eq():
    dv = np.linspace(0, 6000, 300)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for isp, c, n in [(70, GREY, "Cold gas (70 s)"), (225, BLUE, "Hydrazine (225 s)"), (320, NAVY, "Biprop (320 s)"),
                      (450, SKY, "LOX/LH₂ (450 s)"), (1600, ORANGE, "Hall thruster (1600 s)"),
                      (3000, VIOLET, "Ion engine (3000 s)")]:
        frac = 1 - np.exp(-dv / (isp * 9.80665))
        ax.plot(dv / 1000, frac * 100, color=c, label=n)
    ax.set_xlabel("Δv (km/s)")
    ax.set_ylabel("Propellant as % of initial mass")
    ax.legend(fontsize=7, loc="lower right")
    for x, t in [(0.3, "LEO station-\nkeeping & de-orbit"), (1.8, "GTO → GEO"), (3.9, "LEO → GEO")]:
        ax.axvline(x, color=GREY, lw=0.5, ls=":")
        ax.text(x + 0.05, 92, t, fontsize=6.4, color=GREY, va="top")
    ax.set_ylim(0, 100)
    save(fig, "ch06_rocket_eq")


def monoprop():
    fig, ax = canvas(7.0, 3.4, (0, 100), (0, 46))
    ax.add_patch(Ellipse((14, 26), 20, 30, fc="#E8F1FA", ec=NAVY, lw=1.2))
    ax.add_patch(Rectangle((5, 26), 18, 14, fc="#FFFFFF", ec="none", alpha=0.0))
    ax.fill_between([5.5, 22.5], 12, 25, color=SKY, alpha=0.5)
    ax.text(14, 33, "N₂ or He\npressurant", ha="center", fontsize=6.8)
    ax.text(14, 18, "liquid\nhydrazine", ha="center", fontsize=6.8)
    ax.plot([5.5, 22.5], [25, 25], color=GREY, lw=0.6, ls="--")
    ax.text(14, 6.5, "diaphragm or PMD\ntank (blowdown)", ha="center", fontsize=6.4, color=GREY)
    ax.plot([24, 36], [16, 16], color=NAVY, lw=2)
    for x, t in [(28, "filter"), (33, "latch\nvalve")]:
        ax.add_patch(Rectangle((x - 1.5, 14.5), 3, 3, fc="white", ec=NAVY))
        ax.text(x, 19.5, t, fontsize=6, ha="center")
    ax.plot([36, 50], [16, 16], color=NAVY, lw=2)
    ax.add_patch(Rectangle((50, 12), 8, 8, fc="#C9D3DD", ec=NAVY))
    ax.text(54, 22, "solenoid\nvalve", fontsize=6.3, ha="center")
    ax.add_patch(Rectangle((58, 11), 14, 10, fc="#F4B266", ec=RED))
    ax.text(65, 16, "catalyst bed\n(Ir on Al₂O₃)", fontsize=6.3, ha="center", va="center")
    ax.add_patch(Polygon([(72, 13), (72, 19), (86, 25), (86, 7)], fc="#9AA5B1", ec=NAVY))
    for k in range(5):
        arrow(ax, (87, 16 + (k - 2) * 2.5), (97, 16 + (k - 2) * 4.0), color=ORANGE, lw=0.8, ms=6)
    ax.text(56, 38, "3 N₂H₄ → 4 NH₃ + N₂ (exothermic)\n4 NH₃ → 2 N₂ + 6 H₂ (partial, endothermic)\n"
            "Exhaust ≈ 900–1 000 °C, Isp ≈ 220–235 s", fontsize=6.8, ha="center")
    ax.text(84, 3, "nozzle", fontsize=6.3, ha="center")
    save(fig, "ch06_monoprop")


def biprop():
    fig, ax = canvas(7.0, 3.6, (0, 100), (0, 48))
    ax.add_patch(FancyBboxPatch((40, 36), 20, 9, boxstyle="round,pad=0,rounding_size=4", fc="#F3F6F9", ec=NAVY))
    ax.text(50, 40.5, "He high-pressure\ntank (≈ 300 bar)", fontsize=6.5, ha="center", va="center")
    ax.add_patch(Rectangle((47, 29), 6, 4, fc="white", ec=NAVY))
    ax.text(57, 31, "pressure regulator → ≈ 18 bar", fontsize=6.3, va="center")
    ax.plot([50, 50], [36, 33], color=NAVY, lw=1.5)
    ax.plot([50, 50], [29, 26], color=NAVY, lw=1.5)
    ax.plot([22, 78], [26, 26], color=NAVY, lw=1.5)
    for x, t, c in [(22, "Fuel tank\n(MMH)", "#E3C565"), (78, "Oxidiser tank\n(NTO / MON-3)", "#E59866")]:
        ax.plot([x, x], [26, 23], color=NAVY, lw=1.5)
        ax.add_patch(Ellipse((x, 15), 18, 16, fc=c, ec=NAVY, alpha=0.8))
        ax.text(x, 15, t, ha="center", va="center", fontsize=6.6)
        ax.plot([x, 50], [7, 3], color=NAVY, lw=1.5)
    ax.add_patch(Polygon([(46, 3), (54, 3), (57, -6 + 8), (43, -6 + 8)], fc="#9AA5B1", ec=NAVY))
    ax.text(50, 0.3, "400–500 N apogee engine (Isp ≈ 320 s) + 10–22 N attitude thrusters", fontsize=6.4, ha="center",
            color=NAVY)
    ax.text(2, 44, "Pressure-regulated bipropellant system\n(typical GEO satellite)", fontsize=7.5, weight="bold",
            color=NAVY, va="top")
    ax.text(83, 40, "hypergolic: ignites on\ncontact, no igniter", fontsize=6.6, color=GREY)
    save(fig, "ch06_biprop")


def ion_hall():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.1))
    for a in (a1, a2):
        a.set_xlim(0, 50)
        a.set_ylim(0, 40)
        a.set_aspect("equal")
        a.axis("off")
    a1.set_title("Gridded ion engine", fontsize=8.5)
    a1.add_patch(Rectangle((4, 8), 26, 24, fc="#EAF1F7", ec=NAVY))
    a1.text(17, 26, "discharge chamber\n(xenon plasma)", fontsize=6.4, ha="center")
    for x, c, t in [(30.5, RED, "screen grid (+1 kV)"), (33, BLUE, "accel grid (−200 V)")]:
        for y in np.linspace(9, 31, 12):
            a1.plot([x, x], [y, y + 1.2], color=c, lw=2)
    a1.text(31.5, 34, "screen (+) / accel (−) grids", fontsize=6, ha="center")
    for y in np.linspace(11, 29, 6):
        a1.annotate("", xy=(47, y), xytext=(35, y), arrowprops=dict(arrowstyle="-|>", color=VIOLET, lw=0.8))
    a1.text(41, 5, "Xe⁺ beam\n30–40 km/s", fontsize=6.4, ha="center", color=VIOLET)
    a1.add_patch(Circle((40, 33), 1.5, fc=ORANGE))
    a1.text(40, 36.5, "neutraliser\n(e⁻)", fontsize=6, ha="center")
    a1.text(2, 2, "Isp 2 500–4 500 s; ≈ 25–40 mN/kW", fontsize=6.4, color=GREY)
    a2.set_title("Hall-effect thruster (cross-section)", fontsize=8.5)
    a2.add_patch(Rectangle((6, 6), 22, 28, fc="#C9D3DD", ec=NAVY))
    a2.add_patch(Rectangle((12, 12), 16, 4, fc="#F4F6F8", ec=NAVY))
    a2.add_patch(Rectangle((12, 24), 16, 4, fc="#F4F6F8", ec=NAVY))
    a2.text(4, 20, "magnetic\ncircuit", fontsize=6, ha="right", va="center", rotation=90)
    a2.text(20, 20, "annular channel:\nradial B field traps e⁻,\naxial E field accelerates ions", fontsize=5.8,
            ha="center", va="center")
    a2.text(13, 9.5, "anode + Xe/Kr feed", fontsize=6, ha="left")
    for y in (14, 26):
        a2.annotate("", xy=(45, y), xytext=(29, y), arrowprops=dict(arrowstyle="-|>", color=VIOLET, lw=1.2))
    a2.add_patch(Circle((40, 33), 1.5, fc=ORANGE))
    a2.text(40, 36.5, "cathode", fontsize=6, ha="center")
    a2.text(2, 2, "Isp 1 200–2 800 s; ≈ 50–70 mN/kW", fontsize=6.4, color=GREY)
    save(fig, "ch06_ion_hall")


def cdh_arch():
    fig, ax = canvas(7.2, 3.6, (0, 100), (0, 48))
    box(ax, 36, 30, 28, 12, "Onboard computer (OBC)\nprocessor ×2 (cold/hot spare),\nwatchdog, safeguard memory",
        fc=NAVY, ec=NAVY, color="white", fs=6.8)
    box(ax, 72, 32, 24, 9, "Mass memory\n(Flash/NAND, Tbit,\nEDAC, file system)", fc="#E8F1FA", ec=BLUE, fs=6.6)
    box(ax, 4, 32, 24, 9, "TT&C transponder\n(telecommand decoder,\ntelemetry encoder)", fc="#EEF7F1", ec=GREEN, fs=6.6)
    box(ax, 72, 16, 24, 9, "Payload processor /\nFPGA / AI accelerator", fc="#F3EFF9", ec=VIOLET, fs=6.6)
    box(ax, 4, 16, 24, 9, "Remote interface units\n(sensor & actuator I/O,\nthermistors, heaters)", fc="#FCF3EA", ec=ORANGE, fs=6.6)
    box(ax, 38, 16, 24, 9, "GNC sensors &\nactuators", fc="#FCF3EA", ec=ORANGE, fs=6.6)
    ax.plot([8, 92], [8, 8], color=BLUE, lw=3)
    ax.text(50, 4, "Platform bus: MIL-STD-1553B / CAN / RS-422          High-rate payload links: SpaceWire / "
            "SpaceFibre / Ethernet (TSN)", fontsize=6.4, ha="center", color=BLUE)
    for x in (16, 50, 84):
        ax.plot([x, x], [8, 16], color=BLUE, lw=1.5)
    ax.plot([50, 50], [25, 30], color=BLUE, lw=1.5)
    arrow(ax, (64, 36), (72, 36), style="<|-|>", color=NAVY)
    arrow(ax, (28, 36), (36, 36), style="<|-|>", color=NAVY)
    arrow(ax, (84, 25), (84, 32), style="<|-|>", color=VIOLET)
    save(fig, "ch06_cdh")


def processors():
    data = [("Apollo Guidance Computer", 1966, 0.04, GREY), ("1802 (Galileo, Magellan)", 1989, 0.5, GREY),
            ("Mongoose-V (New Horizons)", 1998, 10, BLUE), ("RAD6000 (Spirit, Opportunity)", 1996, 35, BLUE),
            ("RAD750 (Curiosity, JWST, Perseverance)", 2001, 260, BLUE), ("LEON3FT / GR712RC", 2011, 140, GREEN),
            ("GR740 (quad LEON4)", 2016, 1000, GREEN), ("RAD5545", 2015, 5600, BLUE),
            ("Snapdragon 801 (Ingenuity, COTS)", 2021, 15000, ORANGE),
            ("Jetson-class GPU modules (LEO, COTS)", 2023, 60000, ORANGE),
            ("HPSC (Microchip PIC64-HPSC)", 2025, 26000, RED)]
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    for n, y, v, c in data:
        ax.scatter(y, v, s=55, color=c, zorder=3, edgecolor="white")
        ax.text(y + 0.8, v * 1.15, n, fontsize=6.6)
    ax.set_yscale("log")
    ax.set_xlim(1962, 2040)
    ax.set_ylim(0.01, 3e5)
    ax.set_xlabel("Year of first flight / availability")
    ax.set_ylabel("Approx. integer performance (MIPS / DMIPS)")
    ax.scatter([], [], color=BLUE, label="Rad-hard (US)")
    ax.scatter([], [], color=GREEN, label="Rad-hard (Europe)")
    ax.scatter([], [], color=ORANGE, label="Commercial (COTS), mitigated")
    ax.scatter([], [], color=RED, label="Next-generation rad-hard multicore")
    ax.legend(fontsize=6.8, loc="upper left")
    note(ax, "Approximate single-figure performance; AI accelerators are measured in TOPS rather than MIPS (Chapter 43).",
         xy=(1, -0.15))
    save(fig, "ch06_processors")


def fsw_layers():
    fig, ax = canvas(7.0, 3.6, (0, 100), (0, 46))
    layers = [(4, "Hardware: processor, memory, I/O, timers, watchdog", "#C9D3DD"),
              (4, "Board support package & drivers", "#B8CCE0"),
              (4, "Real-time OS (RTEMS, VxWorks, FreeRTOS, Linux+PREEMPT_RT) + OS abstraction layer", "#9FBEDC"),
              (4, "Core flight executive / framework (cFS, F Prime): software bus, time, events, tables", "#6FA0CF"),
              (10, "", "#FFFFFF")]
    y = 4
    for h, t, c in layers[:4]:
        ax.add_patch(Rectangle((4, y), 92, h, fc=c, ec="white"))
        ax.text(50, y + h / 2, t, ha="center", va="center", fontsize=6.8, color=INK if not is_dark(c) else "white")
        y += h + 0.6
    apps = ["Command\n& telemetry", "Scheduler", "GNC / ADCS", "Power &\nthermal", "Payload\nmanager",
            "FDIR &\nsafe mode", "Data storage\n& file xfer", "Autonomy /\nplanning / AI"]
    for k, a in enumerate(apps):
        box(ax, 4 + k * 11.6, y + 0.4, 10.8, 10, a, fc="#EEF7F1", ec=GREEN, fs=6.2, r=0.6)
    ax.text(50, y + 13, "Applications", ha="center", fontsize=7.5, weight="bold", color=GREEN)
    ax.text(50, 0.8, "Layering isolates applications from hardware so that they can be reused across missions "
            "(NASA cFS has flown on dozens of spacecraft; JPL's F Prime flew on Ingenuity).", fontsize=6.4,
            ha="center", color=GREY)
    save(fig, "ch06_fsw_layers")


def fdir():
    fig, ax = canvas(6.8, 3.6, (0, 100), (0, 46))
    levels = [("Level 0 — unit: EDAC, latch-up protection, local watchdog", 6, "#9BD3A8"),
              ("Level 1 — subsystem: switch to redundant unit, reconfigure", 14, "#F7E08A"),
              ("Level 2 — system: software FDIR, mode transitions, load shedding", 22, "#F4B266"),
              ("Level 3 — safe mode: Sun-pointing, minimum power, beacon to ground", 30, "#E3646B"),
              ("Level 4 — ground: diagnosis, recovery, software patches", 38, "#B23A48")]
    for k, (t, y, c) in enumerate(levels):
        w = 86 - k * 4
        ax.add_patch(Rectangle((44 - w / 2, y - 3.5), w, 7, fc=c, ec="white"))
        ax.text(44, y, t, ha="center", va="center", fontsize=6.4, color="white" if k >= 3 else INK)
    ax.text(97, 4, "fast,\nlocal,\nautomatic", fontsize=6.4, ha="right", color=GREY)
    ax.text(97, 41, "slow,\nglobal,\nhuman", fontsize=6.4, ha="right", color=GREY)
    save(fig, "ch06_fdir")


if __name__ == "__main__":
    adcs_loop(); sensor_accuracy(); disturbances(); wheel_pyramid(); isp_thrust(); rocket_eq(); monoprop(); biprop()
    ion_hall(); cdh_arch(); processors(); fsw_layers(); fdir()
