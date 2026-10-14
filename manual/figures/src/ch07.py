import sys
from math import erfc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403

C = 299792458.0


def bands():
    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    b = [("VHF", 0.03, 0.3, GREY, "amateur, AIS,\nbeacons"), ("UHF", 0.3, 1, SKY, "CubeSat TT&C,\nmil. SATCOM, ORBCOMM"),
         ("L", 1, 2, GREEN, "GNSS, Iridium,\nInmarsat, D2D"), ("S", 2, 4, BLUE, "TT&C, Globalstar,\nradar, D2D"),
         ("C", 4, 8, VIOLET, "TV distribution,\nweather radar"), ("X", 8, 12, RED, "EO downlink,\ndeep space, SAR, mil."),
         ("Ku", 12, 18, ORANGE, "DTH TV, VSAT,\nStarlink user"), ("K", 18, 27, GOLD, "Ka downlinks\n(17.7–21.2 GHz)"),
         ("Ka", 27, 40, "#8C564B", "HTS, gateways,\ndeep-space Ka, EO"), ("V", 40, 75, "#E377C2", "next-gen gateways,\nfeeder links"),
         ("W", 75, 110, "#17BECF", "experimental\n(W-band)")]
    for k, (n, f1, f2, c, use) in enumerate(b):
        ax.add_patch(Rectangle((f1, 0), f2 - f1, 1, fc=c, ec="white", alpha=0.85))
        ax.text(np.sqrt(f1 * f2), 0.5, n, ha="center", va="center", fontsize=8, weight="bold", color="white")
        ax.text(np.sqrt(f1 * f2), -0.12, f"{f1:g}–{f2:g}", ha="center", va="top", fontsize=5.6, rotation=90)
    ax.set_xscale("log")
    ax.set_xlim(0.03, 400)
    ax.set_ylim(-1.3, 2.2)
    ax.set_yticks([])
    ax.add_patch(Rectangle((190, 0), 200, 1, fc="#FADADD", ec="white"))
    ax.text(280, 0.5, "optical\n(~194 THz,\n1550 nm)", fontsize=5.8, ha="center", va="center")
    ax.text(150, 1.6, "→ axis break: optical\nfrequencies ~2 000× higher", fontsize=6.2, color=GREY, ha="center")
    ax.set_xlabel("Frequency (GHz, log scale) — IEEE radar band letters")
    ax.grid(False)
    for s in ("left", "top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "ch07_bands")


def fspl():
    d = np.logspace(2, 10, 300)
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    for f, c, n in [(2.2e9, BLUE, "S-band 2.2 GHz"), (8.4e9, RED, "X-band 8.4 GHz"), (32e9, ORANGE, "Ka-band 32 GHz"),
                    (C / 1550e-9, VIOLET, "Optical 1550 nm")]:
        L = 20 * np.log10(4 * np.pi * d * 1e3 * f / C)
        ax.plot(d, L, color=c, label=n)
    for x, t in [(1000, "LEO pass"), (36000, "GEO"), (384400, "Moon"), (2.25e8, "Mars (avg.)"), (6e9, "Pluto")]:
        ax.axvline(x, color=GREY, lw=0.5, ls=":")
        ax.text(x * 1.1, 330, t, fontsize=6.8, color=GREY, rotation=90, va="bottom")
    ax.set_xscale("log")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Free-space path loss (dB)")
    ax.legend(fontsize=7, loc="lower right")
    note(ax, "L = 20 log₁₀(4πdf/c). Higher frequencies lose more in free space but antennas of the same size gain more, "
             "so the net link improves with frequency.", xy=(1, -0.16))
    save(fig, "ch07_fspl")


def atten():
    f = np.array([1, 2, 4, 8, 10, 15, 20, 22.2, 25, 30, 35, 40, 45, 50, 54, 57, 60, 63, 66, 70, 80, 90, 100])
    gas = np.array([0.035, 0.038, 0.04, 0.05, 0.055, 0.09, 0.25, 0.45, 0.3, 0.22, 0.25, 0.35, 0.6, 1.5, 15, 90, 250, 90,
                    10, 1.5, 0.8, 0.9, 1.1])
    rain = np.array([0.0, 0.01, 0.1, 0.6, 1.1, 2.8, 5.0, 5.8, 7.0, 9.5, 12, 15, 17, 19, 21, 22, 23, 24, 25, 26, 28, 29, 30])
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    ax.semilogy(f, gas, color=BLUE, lw=2, label="Atmospheric gases, zenith (O₂ + H₂O)")
    ax.semilogy(f[1:], rain[1:], color=RED, lw=2, label="Rain, 30° elevation, exceeded 0.1 % of year (temperate)")
    ax.axvspan(50, 70, color=GREY, alpha=0.1)
    ax.text(52, 400, "O₂ absorption\nband (60 GHz)", fontsize=6.8)
    ax.text(15.5, 0.6, "H₂O line\n22.2 GHz", fontsize=6.8)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Attenuation (dB)")
    ax.set_xlim(1, 100)
    ax.set_ylim(0.02, 1000)
    ax.legend(fontsize=7, loc="upper left")
    note(ax, "Approximate, after ITU-R P.676 and P.618. Rain fade dominates link margins above ≈ 10 GHz; site diversity "
             "and adaptive coding mitigate it.", xy=(1, -0.16))
    save(fig, "ch07_atten")


def link_waterfall():
    items = [("Transmitter\noutput 10 W", 10.0), ("Tx line\nlosses", -1.5), ("Tx antenna\n(6 dBi)", 6.0),
             ("Free-space loss\n2 000 km, 8.2 GHz", -176.7), ("Atmosphere\n& rain", -1.5), ("Pointing &\npolarisation", -1.0),
             ("Rx antenna\n5.4 m, 51 dBi", 51.0)]
    levels = [0.0]
    for _, v in items:
        levels.append(levels[-1] + v)
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    x = np.arange(len(levels))
    ax.step(x, levels, where="post", color=NAVY, lw=1.8)
    ax.plot(x, levels, "o", color=NAVY, ms=4)
    for k, (n, v) in enumerate(items):
        c = GREEN if v > 0 else RED
        ax.annotate("", xy=(k + 1, levels[k + 1]), xytext=(k + 1, levels[k]),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.6))
        ax.text(k + 1.08, (levels[k] + levels[k + 1]) / 2, f"{v:+.1f} dB", fontsize=7, color=c, va="center")
    ax.text(0.1, 6, "0 dBW", fontsize=7)
    ax.text(len(levels) - 1 - 0.1, levels[-1] - 12, f"Received carrier\nC = {levels[-1]:.1f} dBW", fontsize=7.5,
            color=NAVY, ha="right", weight="bold")
    ax.text(1.5, 18, "EIRP = 10 − 1.5 + 6 = 14.5 dBW", fontsize=7, color=GREY)
    ax.set_xticks(np.arange(1, len(levels)))
    ax.set_xticklabels([n for n, _ in items], fontsize=6.4)
    ax.set_ylabel("Signal level (dBW)")
    ax.set_xlim(-0.2, len(levels) - 0.4)
    ax.set_ylim(-190, 30)
    save(fig, "ch07_link_waterfall")
    return levels[-1]


def constellations():
    fig, axs = plt.subplots(1, 4, figsize=(7.2, 2.1))
    sets = {"BPSK (1 bit/sym)": np.exp(1j * np.array([0, np.pi])),
            "QPSK (2 bits/sym)": np.exp(1j * (np.pi / 4 + np.arange(4) * np.pi / 2)),
            "8PSK (3 bits/sym)": np.exp(1j * np.arange(8) * np.pi / 4),
            "16APSK (4 bits/sym)": np.concatenate([0.4 * np.exp(1j * (np.pi / 4 + np.arange(4) * np.pi / 2)),
                                                   1.0 * np.exp(1j * (np.pi / 12 + np.arange(12) * np.pi / 6))])}
    rng = np.random.default_rng(1)
    for ax, (n, pts) in zip(axs, sets.items()):
        noisy = np.repeat(pts, 60) + (rng.normal(0, 0.06, len(pts) * 60) + 1j * rng.normal(0, 0.06, len(pts) * 60))
        ax.scatter(noisy.real, noisy.imag, s=1, color=SKY, alpha=0.5)
        ax.scatter(pts.real, pts.imag, s=18, color=NAVY)
        ax.set_aspect("equal")
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)
        ax.set_title(n, fontsize=7.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axhline(0, color=GREY, lw=0.4)
        ax.axvline(0, color=GREY, lw=0.4)
    save(fig, "ch07_constellations")


def ber():
    eb = np.linspace(-2, 12, 300)

    def q(x):
        return 0.5 * np.array([erfc(v / np.sqrt(2)) for v in x])
    unc = q(np.sqrt(2 * 10 ** (eb / 10)))
    conv = q(np.sqrt(2 * 10 ** ((eb + 5.0) / 10))) * 3
    rs_conv = q(np.sqrt(2 * 10 ** ((eb + 7.2) / 10) * 1.0)) * 5
    turbo = np.where(eb > 0.6, 10 ** (-(eb - 0.6) * 9 - 1.5), 0.15)
    ldpc = np.where(eb > 1.2, 10 ** (-(eb - 1.2) * 8 - 1.5), 0.15)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.semilogy(eb, unc, color=GREY, lw=2, label="Uncoded BPSK/QPSK")
    ax.semilogy(eb, np.clip(conv, 1e-12, 0.5), color=BLUE, label="Convolutional r = 1/2, K = 7 (Viterbi)")
    ax.semilogy(eb, np.clip(rs_conv, 1e-12, 0.5), color=GREEN, label="Concatenated RS(255,223) + convolutional")
    ax.semilogy(eb, np.clip(turbo, 1e-12, 0.5), color=ORANGE, label="Turbo code r = 1/6 (CCSDS)")
    ax.semilogy(eb, np.clip(ldpc, 1e-12, 0.5), color=VIOLET, label="LDPC r = 1/2 (CCSDS AR4JA / DVB-S2)")
    ax.axvline(-1.59, color=RED, ls="--", lw=1)
    ax.text(-1.45, 3e-10, "Shannon limit\n(r → 0): −1.59 dB", fontsize=7, color=RED)
    ax.set_ylim(1e-10, 0.5)
    ax.set_xlim(-2, 12)
    ax.set_xlabel("Eb/N0 (dB)")
    ax.set_ylabel("Bit error rate")
    ax.legend(fontsize=6.8, loc="upper right")
    ax.annotate("coding gain ≈ 9 dB\nat BER 10⁻⁶", xy=(1.5, 1e-6), xytext=(3.0, 1e-8), fontsize=7,
                arrowprops=dict(arrowstyle="<->", color=NAVY))
    note(ax, "Uncoded curve exact; coded curves schematic, based on CCSDS 130.1-G and published performance.",
         xy=(1, -0.15))
    save(fig, "ch07_ber")


def antenna_gain():
    D = np.logspace(-1, 2, 200)
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    for f, c, n in [(0.4e9, GREY, "UHF 400 MHz"), (2.2e9, BLUE, "S 2.2 GHz"), (8.4e9, RED, "X 8.4 GHz"),
                    (32e9, ORANGE, "Ka 32 GHz")]:
        lam = C / f
        G = 10 * np.log10(0.6 * (np.pi * D / lam) ** 2)
        ax.semilogx(D, G, color=c, label=n)
    for d, t in [(0.3, "CubeSat\ndeployable"), (3, "Europa Clipper\nHGA 3 m"), (34, "DSN 34 m"), (70, "DSN 70 m")]:
        ax.axvline(d, color=GREY, lw=0.5, ls=":")
        ax.text(d * 1.05, -2, t, fontsize=6.6, color=GREY)
    ax.set_xlabel("Antenna diameter (m)")
    ax.set_ylabel("Gain (dBi), efficiency 60 %")
    ax.legend(fontsize=7)
    ax.set_ylim(-5, 90)
    note(ax, "G = η(πD/λ)²; half-power beamwidth θ ≈ 70 λ/D degrees — a 34 m dish at Ka band has a beam only 0.018° wide.",
         xy=(1, -0.16))
    save(fig, "ch07_antenna_gain")


def antenna_types():
    fig, axs = plt.subplots(1, 5, figsize=(7.2, 1.9))
    for a in axs:
        a.set_xlim(0, 10)
        a.set_ylim(0, 10)
        a.set_aspect("equal")
        a.axis("off")
    t = np.linspace(-1, 1, 100)
    axs[0].plot(5 + 4 * t, 2 + 4 * t ** 2, color=NAVY, lw=2)
    axs[0].plot([5, 5], [2, 7], color=GREY, lw=0.8)
    axs[0].add_patch(Rectangle((4.6, 6.6), 0.8, 0.8, fc=ORANGE))
    axs[0].set_title("Parabolic reflector", fontsize=7)
    z = np.linspace(1, 9, 300)
    axs[1].plot(5 + 1.6 * np.sin(z * 4), z, color=NAVY, lw=1.5)
    axs[1].plot([2.5, 7.5], [1, 1], color=GREY, lw=2)
    axs[1].set_title("Helix (circular pol.)", fontsize=7)
    axs[2].add_patch(Polygon([(3, 2), (7, 2), (9, 8), (1, 8)], fc="#EAF1F7", ec=NAVY))
    axs[2].set_title("Horn", fontsize=7)
    for i in range(3):
        for j in range(3):
            axs[3].add_patch(Rectangle((1.5 + i * 2.6, 1.5 + j * 2.6), 1.6, 1.6, fc=ORANGE, ec=NAVY, lw=0.6))
    axs[3].set_title("Patch array", fontsize=7)
    for i in range(6):
        for j in range(6):
            axs[4].add_patch(Circle((1.2 + i * 1.5, 1.2 + j * 1.5), 0.5, fc=GOLD if (i + j) % 2 else SKY, ec="none"))
    axs[4].set_title("Phased array (electronic\nbeam steering)", fontsize=7)
    save(fig, "ch07_antenna_types")


def dsn_map():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.3, 3.6))
    ax = world_axes(fig, borders=True)
    sites = [("Goldstone\n(California)", -116.89, 35.43), ("Madrid\n(Robledo, Spain)", -4.25, 40.43),
             ("Canberra\n(Tidbinbilla, Australia)", 148.98, -35.40)]
    cols = [BLUE, RED, GREEN]
    for (n, lon, lat), c in zip(sites, cols):
        ax.plot(lon, lat, "o", color=c, ms=7, transform=ccrs.PlateCarree(), mec="white")
        ax.text(lon + 4, lat + 4, n, fontsize=7, color=c, weight="bold", transform=ccrs.PlateCarree())
    ax.set_title("NASA Deep Space Network: three complexes ≈ 120° apart in longitude", fontsize=8.5)
    save(fig, "ch07_dsn_map", raster=True)


def data_rates():
    d = [("Mariner 4 (Mars, 1965)", 1965, 8.33), ("Viking orbiters (1976)", 1976, 16e3),
         ("Voyager 2 at Jupiter (1979)", 1979, 115.2e3), ("Galileo LGA (1996)", 1996, 160),
         ("Cassini at Saturn (2004)", 2004, 166e3), ("Mars Reconnaissance Orbiter (2006)", 2006, 6e6),
         ("LRO Ka-band (2009)", 2009, 100e6), ("LADEE LLCD laser, Moon (2013)", 2013, 622e6),
         ("New Horizons at Pluto (2015)", 2015, 1e3), ("EDRS laser relay (2016)", 2016, 1.8e9),
         ("TBIRD laser, LEO (2022)", 2022, 200e9), ("DSOC laser from 0.2 AU (2023)", 2023, 267e6),
         ("Starlink laser ISL (2024)", 2024, 100e9), ("Artemis II O2O laser (2026)", 2026, 260e6)]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    off = {"DSOC laser from 0.2 AU (2023)": 0.25, "Artemis II O2O laser (2026)": 4.0, "LADEE LLCD laser, Moon (2013)": 1.3,
           "EDRS laser relay (2016)": 1.6, "Starlink laser ISL (2024)": 0.35}
    for n, y, r in d:
        c = VIOLET if "laser" in n.lower() else BLUE
        ax.scatter(y, r, s=40, color=c, zorder=3, edgecolor="white")
        ax.text(y + 0.8, r * off.get(n, 1.3), n, fontsize=6.4)
    ax.set_yscale("log")
    ax.set_xlim(1962, 2040)
    ax.set_ylim(1, 1e12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Downlink / link data rate (bit/s)")
    ax.scatter([], [], color=BLUE, label="Radio frequency")
    ax.scatter([], [], color=VIOLET, label="Optical (laser)")
    ax.legend(fontsize=7, loc="upper left")
    note(ax, "Rates at the stated distance; deep-space rates fall with the square of distance.", xy=(1, -0.15))
    save(fig, "ch07_data_rates")


def ground_arch():
    fig, ax = canvas(7.2, 3.8, (0, 100), (0, 50))
    satellite(ax, 50, 46, 1.2)
    box(ax, 4, 26, 18, 9, "Ground stations\n(TT&C + payload\nreception)", fc="#EEF7F1", ec=GREEN, fs=6.8)
    box(ax, 28, 26, 20, 9, "Mission operations\ncentre (MOC):\ncommanding, monitoring", fc="#E8F1FA", ec=BLUE, fs=6.6)
    box(ax, 54, 26, 18, 9, "Flight dynamics:\norbit determination,\nmanoeuvre planning", fc="#E8F1FA", ec=BLUE, fs=6.4)
    box(ax, 78, 26, 19, 9, "Mission planning\n& scheduling", fc="#E8F1FA", ec=BLUE, fs=6.8)
    box(ax, 4, 8, 26, 10, "Payload data ground segment:\nL0 → L1 → L2 processing,\ncalibration", fc="#FCF3EA", ec=ORANGE, fs=6.4)
    box(ax, 36, 8, 22, 10, "Archive &\ndistribution\n(cloud, APIs)", fc="#FCF3EA", ec=ORANGE, fs=6.6)
    box(ax, 64, 8, 33, 10, "Users: scientists, forecasters,\ncustomers, apps, AI analytics", fc="#F3EFF9", ec=VIOLET,
        fs=6.6)
    arrow(ax, (48, 44), (14, 35), color=GREEN, style="<|-|>", rad=0.1)
    arrow(ax, (22, 30), (28, 30), color=NAVY, style="<|-|>")
    arrow(ax, (48, 30), (54, 30), color=NAVY, style="<|-|>")
    arrow(ax, (72, 30), (78, 30), color=NAVY, style="<|-|>")
    arrow(ax, (13, 26), (13, 18), color=ORANGE)
    arrow(ax, (30, 13), (36, 13), color=ORANGE)
    arrow(ax, (58, 13), (64, 13), color=ORANGE)
    ax.text(26, 44, "RF / optical links", fontsize=6.6, color=GREEN)
    ax.text(50, 2, "Secure terrestrial networks connect all elements; cybersecurity covers the whole chain.", fontsize=6.6,
            ha="center", color=GREY)
    save(fig, "ch07_ground_arch")


def ccsds_stack():
    fig, ax = canvas(7.0, 3.4, (0, 100), (0, 44))
    layers = [("Application", "File delivery (CFDP), image/data compression (CCSDS 121/122/123), "
               "Mission Operations services", "#E8F1FA"),
              ("Transport / network", "Space Packet Protocol, Encapsulation, IP over CCSDS, Delay/Disruption-Tolerant "
               "Networking (Bundle Protocol)", "#D6E6F4"),
              ("Data link — protocol", "TM / TC / AOS / Proximity-1 / USLP transfer frames; Space Data Link Security (SDLS)",
               "#C2D9EE"),
              ("Data link — coding & sync", "Reed–Solomon, convolutional, turbo, LDPC codes; randomisation; frame sync",
               "#A9C9E6"),
              ("Physical", "RF modulation (BPSK, QPSK, GMSK, APSK), ranging; optical (CCSDS 141/142 O3K, HPE)",
               "#8DB7DE")]
    for k, (n, d, c) in enumerate(layers):
        y = 4 + (4 - k) * 8
        ax.add_patch(Rectangle((2, y), 96, 7.2, fc=c, ec="white"))
        ax.text(4, y + 3.6, n, fontsize=7.4, weight="bold", va="center", color=NAVY)
        ax.text(28, y + 3.6, d, fontsize=6.4, va="center")
    save(fig, "ch07_ccsds")


def contact_time():
    lats = np.arange(-90, 91, 5)
    R = 6378.137
    h = 600.0
    elmin = np.radians(5)
    lon, lat = ground_track(R + h, 97.8, hours=24 * 3, n=60000)
    sx = np.cos(np.radians(lat)) * np.cos(np.radians(lon))
    sy = np.cos(np.radians(lat)) * np.sin(np.radians(lon))
    sz = np.sin(np.radians(lat))
    S = np.vstack([sx, sy, sz]).T * (R + h)
    dt = 3 * 24 * 60 / len(lon)
    mins = []
    for la in lats:
        gs = np.array([np.cos(np.radians(la)), 0, np.sin(np.radians(la))]) * R
        v = S - gs
        el = np.arcsin(np.einsum("ij,j->i", v, gs / R) / np.linalg.norm(v, axis=1))
        mins.append((el > elmin).sum() * dt / 3)
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.plot(lats, mins, color=BLUE, lw=2)
    ax.fill_between(lats, 0, mins, color=SKY, alpha=0.3)
    for la, n in [(78.2, "Svalbard"), (67.9, "Kiruna"), (-72.0, "Troll"), (0, "Equator"), (-77.8, "McMurdo")]:
        ax.axvline(la, color=GREY, lw=0.5, ls=":")
        ax.text(la, max(mins) * 1.02, n, fontsize=6.6, ha="center", color=GREY, rotation=90, va="bottom")
    ax.set_xlabel("Ground station latitude (deg)")
    ax.set_ylabel("Contact time per day (minutes)")
    ax.set_xlim(-90, 90)
    ax.set_ylim(0, max(mins) * 1.35)
    note(ax, "Computed for a 600 km sun-synchronous satellite, 5° minimum elevation (3-day average). Polar stations see "
             "every orbit — the reason for Svalbard and Antarctic ground stations.", xy=(1, -0.16))
    save(fig, "ch07_contact_time")


if __name__ == "__main__":
    bands(); fspl(); atten(); c = link_waterfall(); print("C =", c); constellations(); ber(); antenna_gain()
    antenna_types(); dsn_map(); data_rates(); ground_arch(); ccsds_stack(); contact_time()
