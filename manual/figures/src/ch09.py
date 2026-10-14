import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403

MU = 3.986004418e14
RE = 6371e3


def ballistic(v0, gamma_deg, h0=40e3, dt=0.5):
    """Drag-free ballistic flight over a spherical rotating-free Earth from burnout state."""
    g = np.radians(gamma_deg)
    x, y = 0.0, RE + h0
    vx, vy = v0 * np.cos(g), v0 * np.sin(g)
    ts, hs, ds = [0], [h0], [0]
    t = 0
    while True:
        r = np.hypot(x, y)
        ax_, ay_ = -MU * x / r ** 3, -MU * y / r ** 3
        vx += ax_ * dt
        vy += ay_ * dt
        x += vx * dt
        y += vy * dt
        t += dt
        r = np.hypot(x, y)
        h = r - RE
        ts.append(t)
        hs.append(h)
        ds.append(RE * np.arctan2(x, y))
        if h < 0 or t > 6000:
            break
    return np.array(ts), np.array(hs) / 1e3, np.array(ds) / 1e3


def trajectories():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.4))
    cases = [("Terrier-Improved Orion (≈ 120 km)", 1.45e3, 87, GREY, 30e3), ("VSB-30 / TEXUS (≈ 260 km)", 2.1e3, 86, GREEN, 45e3),
             ("Black Brant IX (≈ 330 km)", 2.35e3, 86, BLUE, 50e3), ("MAXUS (≈ 700 km)", 3.3e3, 87, ORANGE, 60e3),
             ("Black Brant XII (≈ 1 100 km)", 4.15e3, 87, RED, 70e3)]
    for n, v, gm, c, hb in cases:
        t, h, d = ballistic(v, gm, h0=hb)
        a1.plot(t / 60, h, color=c, label=n)
        a2.plot(d, h, color=c)
    for a in (a1, a2):
        a.axhline(100, color=VIOLET, ls="--", lw=0.8)
    a1.text(0.2, 108, "100 km", fontsize=6.8, color=VIOLET)
    a1.set_xlabel("Time after burnout (min)")
    a1.set_ylabel("Altitude (km)")
    a1.legend(fontsize=6.4, loc="upper right")
    a2.set_xlabel("Downrange distance (km)")
    a2.set_ylim(0, 1300)
    a1.set_ylim(0, 1300)
    note(a2, "Drag-free trajectories from burnout, computed for this manual; real launches add a few km of drag losses.",
         xy=(1, -0.2))
    save(fig, "ch09_trajectories")


def micro_time():
    ap = np.linspace(105, 1500, 200)
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    for floor, c, lab in [(100, BLUE, "time above 100 km"), (80, SKY, "time above 80 km")]:
        gavg = MU / (RE + (ap + floor) / 2 * 1e3) ** 2
        tt = 2 * np.sqrt(2 * (ap - floor) * 1e3 / gavg)
        ax.plot(ap, tt / 60, color=c, lw=2, label=lab + " (vertical ballistic flight)")
    pts = [("New Shepard", 106, 3.2), ("SpaceShipTwo (apogee ≈ 86 km)", 86, 3.5), ("TEXUS (VSB-30)", 260, 6.0),
           ("MAXUS", 705, 12.5), ("Black Brant IX", 330, 7.5), ("Black Brant XII", 1100, 16)]
    for n, a, t in pts:
        ax.plot(a, t, "o", color=ORANGE, ms=5)
        ax.text(a + 15, t - (2.4 if "SpaceShip" in n else 0.9), n, fontsize=6.6)
    ax.set_xlabel("Apogee altitude (km)")
    ax.set_ylabel("Time above the stated altitude (min)")
    ax.legend(fontsize=7, loc="lower right")
    ax.set_xlim(60, 1550)
    ax.set_ylim(0, 25)
    note(ax, "Orange points: typical quoted weightless times for each vehicle (they start after engine shutdown and "
             "despin, so are shorter than the time above 100 km).", xy=(1, -0.16))
    save(fig, "ch09_micro_time")


def platforms():
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    items = [("Drop tower (ZARM Bremen,\n4.7 s / 9.3 s catapult)", 4.7, 9.3, 1e-6, 1e-5, GREY),
             ("Parabolic flight\n(A310 Zero-G, ≈ 22 s × 31)", 18, 25, 1e-2, 5e-2, SKY),
             ("Suborbital crewed\n(New Shepard, VSS)", 150, 240, 1e-3, 1e-2, ORANGE),
             ("Sounding rockets\n(TEXUS, MAXUS, Black Brant)", 180, 900, 1e-5, 1e-4, BLUE),
             ("Re-entry capsules /\nfree-flyers (Varda, Photon)", 1e5, 4e6, 1e-6, 1e-5, GREEN),
             ("ISS, Tiangong\n(continuous)", 1e7, 3e8, 1e-6, 1e-4, VIOLET)]
    for n, t1, t2, g1, g2, c in items:
        ax.add_patch(Rectangle((t1, g1), t2 - t1, g2 - g1, fc=c, alpha=0.4, ec=c))
        ax.text(np.sqrt(t1 * t2), g2 * 1.6, n, fontsize=6.4, ha="center", va="bottom")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 1e9)
    ax.set_ylim(1e-7, 1)
    ax.set_xlabel("Duration of reduced gravity (seconds)")
    ax.set_ylabel("Residual acceleration (g)")
    for x, t in [(60, "1 min"), (3600, "1 h"), (86400, "1 day"), (3.15e7, "1 year")]:
        ax.axvline(x, color=GREY, lw=0.5, ls=":")
        ax.text(x * 1.1, 0.25, t, fontsize=6.6, color=GREY)
    save(fig, "ch09_platforms")


def anatomy():
    fig, ax = canvas(7.4, 2.8, (0, 100), (0, 34))
    secs = [(2, 26, "Booster motor\n(Terrier Mk 70)", "#9AA5B1"), (28, 21, "Sustainer motor\n(Black Brant)", "#B8C2CC"),
            (49, 7, "Ignition &\ndespin", "#F3E3B5"), (56, 8, "Telemetry\n& power", "#EEF7F1"),
            (64, 8, "Attitude\ncontrol\n(ACS)", "#E8F1FA"), (72, 12, "Experiment\nmodules", "#FCF3EA"),
            (84, 7, "Recovery\n(parachute)", "#F3EFF9")]
    for x, w, t, c in secs:
        ax.add_patch(Rectangle((x, 12), w, 10, fc=c, ec=NAVY, lw=0.8))
        ax.text(x + w / 2, 17, t, ha="center", va="center", fontsize=6.3)
    ax.add_patch(Polygon([(91, 12), (91, 22), (99, 17)], fc="#C9D3DD", ec=NAVY, lw=0.8))
    ax.text(96, 24, "nose cone\n(ejected)", fontsize=6.2, ha="center")
    for x0 in (3, 29):
        ax.add_patch(Polygon([(x0, 12), (x0 - 1.5, 7), (x0 + 6, 12)], fc="#5B6670"))
        ax.add_patch(Polygon([(x0, 22), (x0 - 1.5, 27), (x0 + 6, 22)], fc="#5B6670"))
    darrow(ax, (2, 4), (99, 4), color=GREY, lw=0.8)
    ax.text(50, 1, "two-stage Black Brant IX: ≈ 17 m long, 0.44 m diameter, ≈ 2.7 t at lift-off", fontsize=6.6,
            ha="center", color=GREY)
    ax.text(2, 31, "Spin-stabilised during powered flight (fins canted ≈ 4 Hz), despun by yo-yo weights, then "
            "3-axis pointed by cold-gas ACS for experiments", fontsize=6.6, color=NAVY)
    save(fig, "ch09_anatomy")


def nasa_family():
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    fam = [("Terrier-Improved Orion", [(50, 190), (150, 130), (300, 95), (450, 75)], GREY),
           ("Terrier-Improved Malemute", [(50, 650), (100, 480), (200, 340), (300, 250)], GREEN),
           ("Black Brant IX (Terrier–BB)", [(150, 420), (300, 330), (500, 250), (700, 190)], BLUE),
           ("Terrier-Oriole", [(150, 450), (300, 330), (500, 240), (650, 190)], VIOLET),
           ("Black Brant X / XI", [(100, 900), (200, 700), (400, 520), (700, 380)], ORANGE),
           ("Black Brant XII (4-stage)", [(100, 1500), (300, 1000), (500, 800), (800, 600)], RED)]
    for n, pts, c in fam:
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]
        ax.plot(x, y, color=c, lw=1.8, marker="o", ms=3, label=n)
    ax.set_xlabel("Payload mass (kg)")
    ax.set_ylabel("Apogee (km)")
    ax.legend(fontsize=6.8)
    note(ax, "Approximate performance envelopes for launches near sea level at 85–87° elevation, after the NASA "
             "Sounding Rocket Program Handbook.", xy=(1, -0.16))
    save(fig, "ch09_nasa_family")


def suborbital_profiles():
    fig, ax = canvas(7.4, 4.0, (0, 100), (0, 55))
    ax.axhline(30 + 0, color=VIOLET, lw=0.6, ls="--")
    ax.plot([0, 100], [44, 44], color=RED, lw=0.6, ls="--")
    ax.text(99, 44.6, "Kármán line 100 km", fontsize=6.4, color=RED, ha="right")
    ax.text(46, 38.6, "80 km (US astronaut wings)", fontsize=6.4, color=VIOLET, ha="left")
    ax.plot([0, 100], [38, 38], color=VIOLET, lw=0.6, ls="--")
    ax.lines[0].remove()
    x = np.linspace(4, 44, 200)
    y = 4 + 43 * np.sin(np.pi * (x - 4) / 40) ** 0.75
    ax.plot(x, y, color=BLUE, lw=2)
    ax.text(2, 52, "NEW SHEPARD (vertical)", fontsize=7.5, weight="bold", color=BLUE)
    pts = [(6, 9, "lift-off,\nBE-3PM\nLOX/LH₂"), (14, 33, "MECO,\ncapsule\nseparates"), (36, 46, "apogee ≈ 105–107 km;\n≈ 3 min weightless"),
           (36, 20, "drogue + 3 main\nparachutes"), (44, 6, "touchdown\n(retro-thrust)")]
    for px, py, t in pts:
        ax.text(px, py, t, fontsize=6.0, ha="center")
    ax.plot([8, 10, 12], [4, 12, 4], color=GREY, lw=0.8, ls=":")
    ax.text(12, 1.5, "booster lands\nvertically on pad", fontsize=6.0, ha="center", color=GREY)
    x2 = np.linspace(56, 98, 300)
    y2 = np.where(x2 < 62, 4 + (x2 - 56) * 1.5, 0)
    seg = (x2 >= 62)
    y2[seg] = 13 + 28 * np.sin(np.pi * (x2[seg] - 62) / 26) ** 0.8 * (x2[seg] < 88)
    tail = x2 >= 88
    y2[tail] = 13 * np.exp(-(x2[tail] - 88) / 3.5) + 0.0
    ax.plot(x2, np.clip(y2, 1, None), color=ORANGE, lw=2)
    ax.text(55, 52, "SPACESHIPTWO / DELTA (air-launched)", fontsize=7.5, weight="bold", color=ORANGE)
    pts2 = [(59, 17, "carried by\nmothership\nto ≈ 14 km"), (66, 32, "hybrid rocket\nburn ≈ 60 s,\nMach 3"),
            (88, 38.5, "apogee ≈ 85–90 km;\nfeather raised"), (85, 25, "feathered\nre-entry"), (95, 9, "glide to\nrunway landing")]
    for px, py, t in pts2:
        ax.text(px, py, t, fontsize=6.0, ha="center")
    ax.plot([0, 100], [1, 1], color=GREEN, lw=2)
    save(fig, "ch09_suborbital_profiles")


def ranges_map():
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(7.3, 3.7))
    ax = world_axes(fig, borders=True)
    sites = [("Wallops", -75.47, 37.94), ("White Sands, Spaceport America,\nVan Horn (Blue Origin)", -106.48, 32.38),
             ("Poker Flat", -147.49, 65.12),
             ("Andøya, Esrange", 16.02, 69.29), ("SvalRak (Ny-Ålesund)", 11.85, 78.93),
             ("Woomera", 136.5, -30.95), ("Kwajalein", 167.73, 9.40), ("Thumba", 76.87, 8.53),
             ("Uchinoura,\nTanegashima", 131.08, 31.25), ("Alcântara", -44.37, -2.37), ("Barreira do Inferno", -35.16, -5.92),
             ("El Arenosillo", -6.73, 37.10), ("Jiuquan", 100.29, 40.96), ("Hainan (Danzhou)", 109.6, 19.5),
             ("Kapustin Yar", 45.78, 48.58)]
    for n, lon, lat in sites:
        ax.plot(lon, lat, "^", color=ORANGE, ms=5.5, mec=NAVY, mew=0.5, transform=ccrs.PlateCarree())
        dx, dy = {"White Sands, Spaceport America,\nVan Horn (Blue Origin)": (-3, -12), "Wallops": (2, 1)}.get(n, (2.2, 1.2))
        ax.text(lon + dx, lat + dy, n, fontsize=5.8, transform=ccrs.PlateCarree(), ha="right" if dx < 0 else "left")
    ax.set_title("Selected sounding-rocket and suborbital launch sites", fontsize=8.5)
    save(fig, "ch09_ranges", raster=True)


def hybrid_motor():
    fig, ax = canvas(7.0, 2.8, (0, 100), (0, 36))
    ax.add_patch(FancyBboxPatch((4, 12), 22, 14, boxstyle="round,pad=0,rounding_size=6", fc="#E8F1FA", ec=NAVY))
    ax.text(15, 19, "N₂O oxidiser tank\n(self-pressurising\nliquid)", fontsize=6.6, ha="center", va="center")
    ax.plot([26, 32], [19, 19], color=NAVY, lw=2)
    ax.add_patch(Rectangle((31, 16.5), 3, 5, fc="white", ec=NAVY))
    ax.text(32.5, 24, "valve /\ninjector", fontsize=6.2, ha="center")
    ax.add_patch(Rectangle((35, 10), 40, 18, fc="#F3F6F9", ec=NAVY))
    ax.add_patch(Rectangle((35, 10), 40, 5, fc="#5B6670", ec="none"))
    ax.add_patch(Rectangle((35, 23), 40, 5, fc="#5B6670", ec="none"))
    ax.text(55, 19, "combustion port: fuel grain surface\nvaporises and burns with the oxidiser", fontsize=6.4,
            ha="center", va="center")
    ax.text(55, 8, "solid fuel grain (HTPB rubber, polyamide or paraffin)", fontsize=6.4, ha="center", color=GREY)
    ax.add_patch(Polygon([(75, 14), (75, 24), (90, 30), (90, 8)], fc="#9AA5B1", ec=NAVY))
    for k in range(4):
        arrow(ax, (91, 19 + (k - 1.5) * 3), (99, 19 + (k - 1.5) * 4.5), color=ORANGE, lw=0.8, ms=6)
    ax.text(50, 33, "Hybrid rocket motor: liquid oxidiser + solid fuel — can be throttled and shut down, "
            "cannot detonate like a solid; Isp ≈ 250 s", fontsize=6.8, ha="center", color=NAVY)
    save(fig, "ch09_hybrid")


def sequence_timeline():
    fig, ax = plt.subplots(figsize=(7.2, 2.7))
    ev = [(0, "T+0 s\nlift-off\n(rail)"), (6, "T+6 s\nTerrier\nburnout"), (12, "T+12 s\nBlack Brant\nignition"),
          (44, "T+44 s\nBB burnout\n≈ 2.3 km/s"), (60, "T+60 s\nnose cone off,\ndespin"), (70, "T+70 s\nACS on,\ndoors open"),
          (90, "T+90 s\n>100 km:\nobserving"), (280, "T+280 s\napogee\n≈ 320 km"), (470, "T+470 s\ndoors closed,\nend of data"),
          (560, "T+560 s\nre-entry"), (720, "T+720 s\nchute at\n≈ 5 km"), (900, "T+15 min\nlanding")]
    X = lambda t: np.sqrt(t)  # noqa: E731
    ax.set_xlim(-1, 31.5)
    ax.set_ylim(-5, 5)
    ax.axis("off")
    ax.plot([0, X(920)], [0, 0], color=NAVY, lw=2)
    ax.axvspan(X(90), X(470), ymin=0.45, ymax=0.55, color=GREEN, alpha=0.3)
    for i, (t, txt) in enumerate(ev):
        y = 1.1 if i % 2 == 0 else -1.1
        ax.plot([X(t), X(t)], [0, y * 0.8], color=GREY, lw=0.6)
        ax.plot(X(t), 0, "o", color=ORANGE, ms=4)
        ax.text(X(t), y, txt, ha="center", va="bottom" if y > 0 else "top", fontsize=5.9)
    ax.text(X(250), -4.6, "≈ 6.5 minutes of science above 100 km (green); time axis is square-root scaled",
            fontsize=6.6, color=GREEN, ha="center")
    save(fig, "ch09_sequence")


if __name__ == "__main__":
    hybrid_motor(); sequence_timeline()
    trajectories(); micro_time(); platforms(); anatomy(); nasa_family(); suborbital_profiles(); ranges_map()
