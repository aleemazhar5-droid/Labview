import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403


def std_atm(h_km):
    """US Standard Atmosphere 1976 (to 86 km): returns T (K), p (Pa), rho (kg/m3)."""
    g0, R, M = 9.80665, 8.31446, 0.0289644
    layers = [(0, 288.15, -6.5, 101325.0), (11, 216.65, 0.0, 22632.06), (20, 216.65, 1.0, 5474.889),
              (32, 228.65, 2.8, 868.0187), (47, 270.65, 0.0, 110.9063), (51, 270.65, -2.8, 66.93887),
              (71, 214.65, -2.0, 3.956420)]
    h = np.atleast_1d(h_km).astype(float)
    T = np.zeros_like(h)
    p = np.zeros_like(h)
    for i, hh in enumerate(h):
        for k in range(len(layers) - 1, -1, -1):
            h0, T0, L, p0 = layers[k]
            if hh >= h0:
                break
        Tl = T0 + L * (hh - h0)
        if L == 0:
            pl = p0 * np.exp(-g0 * M * (hh - h0) * 1e3 / (R * T0))
        else:
            pl = p0 * (Tl / T0) ** (-g0 * M / (R * L * 1e-3))
        T[i], p[i] = Tl, pl
    rho = p * M / (R * T)
    return T, p, rho


def balloon_types():
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 3.2))
    for a in axs:
        a.set_xlim(0, 10)
        a.set_ylim(0, 12)
        a.set_aspect("equal")
        a.axis("off")
    a = axs[0]
    a.add_patch(Circle((5, 8), 2.4, fc="#F2F2F2", ec=GREY))
    a.plot([5, 5], [5.6, 3], color=GREY, lw=0.8)
    a.add_patch(Rectangle((4.3, 2.0), 1.4, 1.0, fc=ORANGE))
    a.set_title("Latex sounding balloon\n(radiosonde, 30–35 km, bursts)", fontsize=7.2)
    a.text(5, 0.6, "expands ~100× in volume\nuntil it bursts; 1–3 h flight", fontsize=6.2, ha="center", color=GREY)
    a = axs[1]
    t = np.linspace(0, np.pi, 100)
    a.fill(5 + 3.6 * np.cos(t) * np.sin(t / 2 + 0.2), 6 + 4.5 * np.sin(t) * 0.8, color="#EDEDED", ec=GREY)
    a.plot([3, 2.6], [6.4, 4.8], color=GREY, lw=0.8)
    a.plot([7, 7.4], [6.4, 4.8], color=GREY, lw=0.8)
    a.text(1.2, 4.4, "vent\nducts", fontsize=6.2, color=GREY)
    a.plot([5, 5], [6, 2.8], color=GREY, lw=0.8)
    a.add_patch(Rectangle((4.0, 1.8), 2, 1.0, fc=BLUE))
    a.set_title("Zero-pressure balloon\n(open at base; 30–42 km)", fontsize=7.2)
    a.text(5, 0.6, "loses gas at sunset; ballast\ndrops keep altitude; days–weeks", fontsize=6.2, ha="center", color=GREY)
    a = axs[2]
    th = np.linspace(0, 2 * np.pi, 400)
    r = 2.6 + 0.18 * np.cos(14 * th)
    a.fill(5 + r * np.cos(th), 7.5 + 0.75 * r * np.sin(th), color="#E8F1FA", ec=NAVY, lw=0.8)
    for k in range(-6, 7):
        a.plot([5 + k * 0.38, 5 + k * 0.38], [7.5 - 1.8 * np.sqrt(max(0, 1 - (k / 7) ** 2)),
                                                 7.5 + 1.8 * np.sqrt(max(0, 1 - (k / 7) ** 2))], color=NAVY, lw=0.3)
    a.plot([5, 5], [5.5, 2.8], color=GREY, lw=0.8)
    a.add_patch(Rectangle((4.0, 1.8), 2, 1.0, fc=GREEN))
    a.set_title("Super-pressure balloon\n(sealed 'pumpkin'; 33 km)", fontsize=7.2)
    a.text(5, 0.6, "pressurised hull holds constant\nvolume & altitude; weeks–months", fontsize=6.2, ha="center",
           color=GREY)
    save(fig, "ch08_balloon_types")


def lift_vs_alt():
    h = np.linspace(0, 50, 300)
    T, p, rho = std_atm(h)
    rho_he = rho * 4.0026 / 28.9644
    rho_h2 = rho * 2.016 / 28.9644
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.3))
    a1.semilogx((rho - rho_he) * 1000, h, color=BLUE, label="Helium")
    a1.semilogx((rho - rho_h2) * 1000, h, color=ORANGE, ls="--", label="Hydrogen")
    a1.set_xlabel("Net lift (g per m³ of gas)")
    a1.set_ylabel("Altitude (km)")
    a1.legend(fontsize=7)
    a1.set_title("Lift per cubic metre", fontsize=8.5)
    hh = np.linspace(15, 45, 200)
    T, p, rho = std_atm(hh)
    netlift = rho * (1 - 4.0026 / 28.9644)
    for m, c in [(500, GREEN), (2000, BLUE), (4000, RED)]:
        sysmass = m * 1.6
        V = sysmass / netlift
        a2.semilogy(hh, V, color=c, label=f"{m:,} kg suspended load")
    a2.axhline(1.13e6, color=GREY, ls=":", lw=0.8)
    a2.text(44.5, 8.0e5, "NASA 40 MCF balloon\n(1.13 million m³)", fontsize=6.4, color=GREY, ha="right", va="top")
    a2.set_xlabel("Float altitude (km)")
    a2.set_ylabel("Balloon volume at float (m³)")
    a2.legend(fontsize=6.8, loc="upper left")
    a2.set_title("Volume needed", fontsize=8.5)
    note(a2, "Gross mass ≈ 1.6 × load (balloon envelope, ballast, rigging). US Standard Atmosphere 1976.",
         xy=(1, -0.2))
    save(fig, "ch08_lift")


def diurnal():
    t = np.linspace(0, 96, 4000)

    def zp_alt(tt):
        hr = tt % 24
        day_n = int(tt // 24)
        if 7 <= hr < 18:
            return 39.0 - 0.15 * day_n
        if 18 <= hr < 20.5:
            return 39.0 - 0.15 * day_n - (hr - 18) / 2.5 * 4.2
        if hr >= 20.5 or hr < 6:
            h2 = hr - 20.5 if hr >= 20.5 else hr + 3.5
            base = 34.8 - 0.15 * day_n
            return base - 0.35 * (h2 % 3) + 0.0
        return 34.8 - 0.15 * day_n + (hr - 6) * 4.2
    zp = np.array([zp_alt(x) for x in t])
    sp = 33.5 + 0.12 * np.sin(2 * np.pi * (t - 9) / 24)
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    for k in range(5):
        ax.axvspan(-6 + 24 * k, 6 + 24 * k, color=NAVY, alpha=0.07)
    ax.plot(t, zp, color=BLUE, lw=1.6, label="Zero-pressure balloon (ballast dropped during the night)")
    ax.plot(t, sp, color=GREEN, lw=1.6, label="Super-pressure balloon (sealed, constant volume)")
    ax.set_xlabel("Time (hours from midnight of launch day) — shaded: night")
    ax.set_ylabel("Float altitude (km)")
    ax.set_xlim(0, 96)
    ax.set_ylim(30, 41)
    ax.legend(fontsize=7, loc="lower left")
    note(ax, "Schematic. At sunset the lifting gas cools and a zero-pressure balloon sinks until ballast is released; "
             "at sunrise it warms and rises, venting gas. Each night costs ballast, limiting flight duration.",
         xy=(1, -0.18))
    save(fig, "ch08_diurnal")


def haps_energy():
    hrs = np.linspace(0, 24, 500)
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    S = 1361 * 0.98
    for lat, decl, c, n in [(0, 0, ORANGE, "Equator, equinox"), (25, -23.4, GOLD, "25° N, winter solstice"),
                            (50, -23.4, BLUE, "50° N, winter solstice"), (50, 23.4, GREEN, "50° N, summer solstice")]:
        phi, d = np.radians(lat), np.radians(decl)
        H = np.radians((hrs - 12) * 15)
        cz = np.sin(phi) * np.sin(d) + np.cos(phi) * np.cos(d) * np.cos(H)
        flux = S * np.clip(cz, 0, None)
        e = np.trapezoid(flux, hrs) / 1000
        ax.plot(hrs, flux, color=c, label=f"{n}: {e:.1f} kWh/m²/day")
    ax.axhline(130, color=RED, ls="--", lw=1)
    ax.text(0.3, 145, "example power demand ≈ 130 W per m² of wing (night: from battery)", fontsize=6.8, color=RED)
    ax.set_xlabel("Local solar time (h)")
    ax.set_ylabel("Sunlight on a horizontal wing at 20 km (W/m²)")
    ax.set_xlim(0, 24)
    ax.legend(fontsize=6.8, loc="upper right")
    note(ax, "Computed clear-sky irradiance above most of the atmosphere. Winter nights at high latitude are the design "
             "case: little energy to collect, long nights to survive.", xy=(1, -0.16))
    save(fig, "ch08_haps_energy")


def winds():
    h = np.linspace(0, 40, 300)
    w = 8 + 32 * np.exp(-((h - 11.5) / 3.5) ** 2) - 3 * np.exp(-((h - 21) / 3) ** 2) + 0.9 * np.clip(h - 24, 0, None)
    w_w = 10 + 50 * np.exp(-((h - 11) / 3.2) ** 2) - 4 * np.exp(-((h - 20) / 3) ** 2) + 1.4 * np.clip(h - 23, 0, None)
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    ax.plot(w, h, color=BLUE, lw=1.8, label="Annual mean, mid-latitudes")
    ax.plot(w_w, h, color=RED, lw=1.2, ls="--", label="Winter 99th percentile (schematic)")
    ax.axhspan(17, 23, color=GREEN, alpha=0.1)
    ax.text(30, 20, "HAPS layer:\nweakest winds,\nabove weather &\ncontrolled airspace", fontsize=7, color=GREEN,
            va="center")
    ax.text(42, 11.5, "jet stream", fontsize=7, color=GREY)
    ax.set_xlabel("Wind speed (m/s)")
    ax.set_ylabel("Altitude (km)")
    ax.set_xlim(0, 70)
    ax.legend(fontsize=6.8, loc="upper right")
    save(fig, "ch08_winds")


def coverage():
    R = 6371.0
    h = np.logspace(np.log10(10), np.log10(36000), 300)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for el, c in [(5, BLUE), (15, ORANGE), (30, RED)]:
        e = np.radians(el)
        lam = np.arccos(R / (R + h) * np.cos(e)) - e
        ax.loglog(h, lam * R, color=c, label=f"minimum elevation {el}°")
    for x, t in [(20, "HAPS 20 km"), (35, "balloon 35 km"), (550, "Starlink 550 km"), (35786, "GEO")]:
        ax.axvline(x, color=GREY, lw=0.5, ls=":")
        ax.text(x * 1.08, 15, t, fontsize=6.8, rotation=90, color=GREY, va="bottom")
    ax.set_xlabel("Platform altitude (km)")
    ax.set_ylabel("Coverage radius on ground (km)")
    ax.legend(fontsize=7)
    note(ax, "A HAPS at 20 km covers a disc ≈ 70 km in radius at 15° elevation — a whole city or region, "
             "with ≈ 0.1 ms one-way delay.", xy=(1, -0.16))
    save(fig, "ch08_coverage")


def platforms_map():
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    items = [("Commercial airliner", 12, 0.6, GREY, (1.3, 0)), ("RQ-4 Global Hawk", 18, 1.4, GREY, (1.3, -1.4)),
             ("ER-2 / U-2", 21, 0.5, GREY, (1.3, 0.6)), ("PHASA-35 (trials)", 20, 3, ORANGE, (-0.75, -1.4)),
             ("Zephyr (record ≈ 67 d)", 21, 67, ORANGE, (0.08, 1.6)), ("Sceye airship", 20, 30, GOLD, (-0.75, 1.2)),
             ("Loon (record 312 d)", 18, 312, GREEN, (1.3, -1.0)), ("Weather balloon", 33, 0.08, SKY, (1.3, 0)),
             ("NASA zero-pressure", 38, 1.5, BLUE, (1.3, 0.6)), ("NASA LDB, Antarctica (≈ 30–57 d)", 38, 40, BLUE, (1.3, 0.8)),
             ("NASA super-pressure", 33, 50, BLUE, (1.3, -0.9)), ("CNES Stratéole-2", 19, 90, VIOLET, (1.3, 0.9))]
    for n, alt, d, c, (fx, dy) in items:
        ax.scatter(d, alt, s=50, color=c, zorder=3, edgecolor="white")
        ax.text(d * abs(fx), alt + dy, n, fontsize=6.6, va="center", ha="right" if fx < 0 else "left")
    ax.set_xscale("log")
    ax.set_xlabel("Typical (or record) mission endurance (days)")
    ax.set_ylabel("Operating altitude (km)")
    ax.set_xlim(0.04, 3000)
    ax.set_ylim(8, 44)
    ax.axhspan(17, 23, color=GREEN, alpha=0.07)
    ax.text(0.045, 17.5, "stratospheric 'HAPS layer'", fontsize=6.8, color=GREEN)
    save(fig, "ch08_platforms")


def haps_arch():
    fig, ax = canvas(7.2, 2.9, (0, 100), (0, 38))
    title_box(ax, 2, 3, 30, 31, "Solar fixed-wing (HTA)",
              "Zephyr, PHASA-35, Sunglider\n\n+ station-keeping in wind\n+ can be recovered & reused\n− payload ≈ 5–15 kg\n"
              "− fragile; ≤ 25 kg/m² wing load\n− winter night energy limit", hc=ORANGE, ec=ORANGE, fc="white", fs=6.4)
    title_box(ax, 35, 3, 30, 31, "Airship (LTA, powered)",
              "Sceye, Stratobus, HiSentinel\n\n+ payload 50–250 kg\n+ large solar area & power\n− huge volume (≈ 100 m long)\n"
              "− drag; hard to hold station\n  in strong winds", hc=GOLD, ec=GOLD, fc="white", fs=6.4)
    title_box(ax, 68, 3, 30, 31, "Free balloon (LTA, unpowered)",
              "Loon, Aerostar, NASA, CNES\n\n+ cheapest per flight-day\n+ heavy payloads (to 3.6 t)\n− goes where wind blows;\n"
              "  steer by changing altitude\n− fleets needed for persistence", hc=BLUE, ec=BLUE, fc="white", fs=6.4)
    save(fig, "ch08_haps_arch")


def sounding():
    h = np.linspace(0, 32, 300)
    T, p, rho = std_atm(h)
    Tc = T - 273.15 + 4 * np.exp(-h / 2)
    Td = Tc - (2 + 1.5 * h) - 6 * np.clip(h - 3, 0, None) ** 0.5
    Td = np.minimum(Td, Tc - 0.5)
    wind = 6 + 30 * np.exp(-((h - 11) / 3.5) ** 2) + 0.4 * np.clip(h - 22, 0, None)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.6), sharey=True, gridspec_kw=dict(width_ratios=[1.4, 1]))
    a1.plot(Tc, h, color=RED, lw=1.8, label="Temperature")
    a1.plot(Td, h, color=GREEN, lw=1.4, label="Dew point")
    a1.axhline(11.5, color=GREY, ls=":", lw=0.7)
    a1.text(-95, 12.0, "tropopause", fontsize=7, color=GREY)
    a1.set_xlabel("Temperature (°C)")
    a1.set_ylabel("Altitude (km)")
    a1.legend(fontsize=7)
    a1.set_xlim(-100, 30)
    a2.plot(wind, h, color=BLUE, lw=1.8)
    a2.set_xlabel("Wind speed (m/s)")
    ax2 = a2.twiny()
    ax2.plot(p / 100, h, color=GREY, lw=0.8, ls="--")
    ax2.set_xscale("log")
    ax2.set_xlabel("Pressure (hPa, dashed)", fontsize=7.5, color=GREY)
    ax2.tick_params(labelsize=6.5, colors=GREY)
    ax2.grid(False)
    a1.set_title("A typical mid-latitude radiosonde profile (schematic)", fontsize=8.5, loc="left")
    save(fig, "ch08_sounding")


def natural_shape():
    fig, ax = canvas(6.8, 4.0, (0, 100), (0, 60))
    t = np.linspace(-1, 1, 300)
    x = 50 + 26 * np.sin(np.pi * (t + 1) / 2) ** 0.9 * np.sign(t) * np.abs(np.sin(np.pi * (t + 1) / 2)) ** 0.1
    th = np.linspace(0, np.pi, 300)
    shapex = 50 + 27 * np.sin(th) ** 1.15 * np.cos(np.linspace(np.pi / 2, -np.pi / 2, 300)) * 0
    R = 27 * np.sin(th) ** 1.1
    zz = 10 + 42 * (1 - (th / np.pi) ** 1.35)
    ax.fill_betweenx(zz, 50 - R, 50 + R, color="#F1F4F7", ec=NAVY)
    for k in np.linspace(-0.85, 0.85, 9):
        ax.plot(50 + k * R, zz, color="#9AA5B1", lw=0.6)
    ax.plot(50 + R, zz, color=NAVY, lw=1.2)
    ax.plot(50 - R, zz, color=NAVY, lw=1.2)
    ax.add_patch(Circle((50, 52.5), 1.3, fc=ORANGE, ec="none"))
    ax.annotate("apex fitting & valve\n(gas release)", xy=(51, 52.5), xytext=(68, 49), fontsize=6.8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.annotate("gores: polyethylene film\n≈ 20 µm thick, heat-sealed", xy=(62, 38), xytext=(80, 44), fontsize=6.8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.annotate("load tapes along seams\ncarry the payload weight", xy=(38, 30), xytext=(2, 40), fontsize=6.8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.plot([50, 50], [10, 3], color=GREY, lw=1)
    ax.add_patch(Rectangle((47, 0.5), 6, 2.5, fc=BLUE))
    ax.annotate("base fitting → parachute →\ngondola", xy=(50, 9), xytext=(60, 5), fontsize=6.8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.annotate("vent duct", xy=(29, 22), xytext=(6, 16), fontsize=6.8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.text(50, 57.5, "Zero-pressure balloon at float ('natural shape')", ha="center", fontsize=8, weight="bold",
            color=NAVY)
    save(fig, "ch08_natural_shape")


def gondola():
    fig, ax = canvas(7.0, 3.4, (0, 100), (0, 46))
    ax.plot([50, 50], [46, 38], color=GREY, lw=1.2)
    box(ax, 44, 36, 12, 3, "rotator / pivot", fc="#F3EFF9", ec=VIOLET, fs=6.3)
    ax.plot([50, 50], [36, 33], color=GREY, lw=1.2)
    ax.add_patch(Polygon([(24, 33), (76, 33), (70, 8), (30, 8)], fc="#F3F6F9", ec=NAVY))
    box(ax, 34, 14, 22, 15, "telescope / instrument\n(elevation drive)", fc="#E8F1FA", ec=BLUE, fs=6.6)
    box(ax, 58, 22, 14, 7, "star cameras,\ngyros, GPS", fc="#EEF7F1", ec=GREEN, fs=6.2)
    box(ax, 58, 12, 14, 8, "flight computer,\ntelemetry, Iridium/\nTDRSS/Starlink", fc="#FCF3EA", ec=ORANGE, fs=5.9)
    ax.add_patch(Rectangle((6, 14), 16, 12, fc="#2A4E8A", ec="#1b2d4f"))
    ax.add_patch(Rectangle((78, 14), 16, 12, fc="#2A4E8A", ec="#1b2d4f"))
    ax.text(14, 11.5, "solar panels", fontsize=6.4, ha="center")
    ax.text(86, 11.5, "solar panels", fontsize=6.4, ha="center")
    ax.add_patch(Rectangle((40, 3.5), 20, 4, fc="#C9D3DD", ec=NAVY))
    ax.text(50, 5.5, "crush pads / ballast hopper", fontsize=6.2, ha="center")
    ax.text(2, 42, "Typical astrophysics gondola: 1–3.6 t,\npointing to arcseconds by torquing\nagainst the flight train "
            "and a reaction wheel", fontsize=6.8, va="top")
    save(fig, "ch08_gondola")


if __name__ == "__main__":
    sounding(); natural_shape(); gondola()
    balloon_types(); lift_vs_alt(); diurnal(); haps_energy(); winds(); coverage(); platforms_map(); haps_arch()
