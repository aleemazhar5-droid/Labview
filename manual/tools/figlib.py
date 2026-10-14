"""Shared figure style and drawing helpers for the manual (matplotlib)."""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Polygon, Rectangle,  # noqa: E402
                                Wedge, Arc)
import numpy as np  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figures" / "out"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#0B2E4F"
BLUE = "#1F6FB2"
SKY = "#5FA8D3"
ORANGE = "#D9772B"
GOLD = "#C9A227"
GREEN = "#2E8B57"
RED = "#B23A48"
VIOLET = "#6D4C9F"
GREY = "#7F8C8D"
LIGHT = "#EAF1F7"
INK = "#1B1F24"
PALETTE = [BLUE, ORANGE, GREEN, VIOLET, RED, GOLD, SKY, GREY, NAVY, "#8C564B"]
EARTH = "#3D7CC9"
LAND = "#6FA36B"
SPACE = "#0A1626"

plt.rcParams.update({
    "font.family": "Inter",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "axes.edgecolor": "#5B6670",
    "axes.linewidth": 0.8,
    "axes.labelcolor": INK,
    "axes.prop_cycle": matplotlib.cycler(color=PALETTE),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#D5DDE5",
    "grid.linewidth": 0.6,
    "grid.linestyle": "-",
    "xtick.color": "#3E4851",
    "ytick.color": "#3E4851",
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "legend.frameon": False,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.04,
    "svg.fonttype": "none",
    "mathtext.fontset": "dejavusans",
    "lines.linewidth": 1.6,
})


def save(fig, name, raster=False):
    ext = "png" if raster else "svg"
    path = OUT / f"{name}.{ext}"
    fig.savefig(path, format=ext, transparent=False, facecolor="white")
    plt.close(fig)
    return path


def canvas(w=7.0, h=4.0, xlim=(0, 100), ylim=(0, 60), bg="white"):
    """Blank diagram canvas in data units (default 100 x 60)."""
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    return fig, ax


def box(ax, x, y, w, h, text="", fc=LIGHT, ec=NAVY, fs=8, color=INK, weight="normal", r=1.2, lw=1.0,
        ha="center", va="center", style="round", alpha=1.0, z=2, wrap=None):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"{style},pad=0,rounding_size={r}" if style == "round" else "square,pad=0",
                       fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z)
    ax.add_patch(p)
    if text:
        tx = x + w / 2 if ha == "center" else (x + 1.2 if ha == "left" else x + w - 1.2)
        ax.text(tx, y + h / 2, text, ha=ha, va=va, fontsize=fs, color=color, weight=weight, zorder=z + 1,
                linespacing=1.25)
    return p


def title_box(ax, x, y, w, h, title, body="", fc=LIGHT, ec=NAVY, hc=NAVY, fs=7.4, tfs=8.4, z=2):
    """Box with a coloured title bar and body text."""
    box(ax, x, y, w, h, fc=fc, ec=ec, r=0.8, z=z)
    th = min(4.2, h * 0.32)
    ax.add_patch(FancyBboxPatch((x, y + h - th), w, th, boxstyle="round,pad=0,rounding_size=0.8", fc=hc, ec=hc,
                                zorder=z + 0.5))
    ax.text(x + w / 2, y + h - th / 2, title, ha="center", va="center", fontsize=tfs, color="white", weight="bold",
            zorder=z + 1)
    if body:
        ax.text(x + w / 2, y + (h - th) / 2, body, ha="center", va="center", fontsize=fs, color=INK, zorder=z + 1,
                linespacing=1.3)


def arrow(ax, p1, p2, text=None, color=NAVY, lw=1.2, style="-|>", ms=10, fs=7, rad=0.0, tc=None, ls="-",
          toff=(0, 1.2), z=3, shrink=0):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                        connectionstyle=f"arc3,rad={rad}", linestyle=ls, zorder=z, shrinkA=shrink, shrinkB=shrink)
    ax.add_patch(a)
    if text:
        mx, my = (p1[0] + p2[0]) / 2 + toff[0], (p1[1] + p2[1]) / 2 + toff[1]
        ax.text(mx, my, text, ha="center", va="bottom", fontsize=fs, color=tc or color, zorder=z + 1)
    return a


def darrow(ax, p1, p2, **kw):
    kw.setdefault("style", "<|-|>")
    return arrow(ax, p1, p2, **kw)


def label(ax, x, y, text, fs=8, color=INK, ha="center", va="center", weight="normal", rot=0, z=5, style="normal",
          bg=None):
    kw = {}
    if bg:
        kw["bbox"] = dict(fc=bg, ec="none", pad=1.0, alpha=0.85)
    return ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va, weight=weight, rotation=rot, zorder=z,
                   style=style, **kw)


def earth(ax, cx, cy, r, z=1, atmosphere=True, land=True):
    if atmosphere:
        ax.add_patch(Circle((cx, cy), r * 1.06, fc="#BFDDF5", ec="none", alpha=0.7, zorder=z))
    ax.add_patch(Circle((cx, cy), r, fc=EARTH, ec="#1D4F8C", lw=0.8, zorder=z + 0.1))
    if land:
        rng = np.random.default_rng(7)
        for _ in range(7):
            a = rng.uniform(0, 2 * np.pi)
            d = rng.uniform(0.15, 0.7) * r
            px, py = cx + d * np.cos(a), cy + d * np.sin(a)
            pts = []
            for k in range(9):
                t = 2 * np.pi * k / 9
                rr = r * rng.uniform(0.08, 0.2)
                pts.append((px + rr * np.cos(t) * 1.4, py + rr * np.sin(t)))
            ax.add_patch(Polygon(pts, closed=True, fc=LAND, ec="none", alpha=0.85, zorder=z + 0.2))
    return


def planet(ax, cx, cy, r, color, z=1, ring=False, name=None, fs=7):
    ax.add_patch(Circle((cx, cy), r, fc=color, ec="#333", lw=0.4, zorder=z))
    if ring:
        ax.add_patch(Ellipse((cx, cy), r * 4.2, r * 1.1, fc="none", ec="#B8A27A", lw=1.4, zorder=z + 0.1))
    if name:
        ax.text(cx, cy - r - 1.5, name, ha="center", va="top", fontsize=fs, zorder=z + 1)


def satellite(ax, x, y, s=1.0, angle=0, color="#C8CDD3", panel="#2A4E8A", z=6):
    """Simple satellite icon: body + two solar wings."""
    c, si = math.cos(math.radians(angle)), math.sin(math.radians(angle))

    def rot(px, py):
        return (x + (px * c - py * si) * s, y + (px * si + py * c) * s)
    body = [rot(-0.8, -0.8), rot(0.8, -0.8), rot(0.8, 0.8), rot(-0.8, 0.8)]
    ax.add_patch(Polygon(body, closed=True, fc=color, ec="#444", lw=0.5, zorder=z))
    for sgn in (-1, 1):
        wing = [rot(sgn * 1.0, -0.55), rot(sgn * 3.4, -0.55), rot(sgn * 3.4, 0.55), rot(sgn * 1.0, 0.55)]
        ax.add_patch(Polygon(wing, closed=True, fc=panel, ec="#1b2d4f", lw=0.4, zorder=z))
        ax.plot(*zip(rot(sgn * 0.8, 0), rot(sgn * 1.0, 0)), color="#444", lw=0.6, zorder=z)


def rocket(ax, x, y, h=20, w=3, color="white", z=4, stages=2, fins=True):
    """Simple side-view rocket icon with bottom at (x, y)."""
    body_h = h * 0.82
    ax.add_patch(Rectangle((x - w / 2, y), w, body_h, fc=color, ec="#333", lw=0.6, zorder=z))
    ax.add_patch(Polygon([(x - w / 2, y + body_h), (x + w / 2, y + body_h), (x, y + h)], closed=True, fc=color,
                         ec="#333", lw=0.6, zorder=z))
    for k in range(1, stages):
        yy = y + body_h * k / stages
        ax.plot([x - w / 2, x + w / 2], [yy, yy], color="#333", lw=0.6, zorder=z + 0.1)
    if fins:
        ax.add_patch(Polygon([(x - w / 2, y), (x - w, y - 0.5), (x - w / 2, y + h * 0.12)], fc="#555", ec="#333",
                             lw=0.4, zorder=z))
        ax.add_patch(Polygon([(x + w / 2, y), (x + w, y - 0.5), (x + w / 2, y + h * 0.12)], fc="#555", ec="#333",
                             lw=0.4, zorder=z))


def orbit_ellipse(ax, a, e, cx=0, cy=0, omega=0.0, color=BLUE, lw=1.2, ls="-", z=2, n=400, frac=1.0, start=0.0):
    """Draw an ellipse with the focus at (cx, cy). a = semi-major axis, omega = argument of periapsis (deg)."""
    nu = np.linspace(start, start + 2 * np.pi * frac, n)
    p = a * (1 - e ** 2)
    r = p / (1 + e * np.cos(nu))
    w = math.radians(omega)
    x = cx + r * np.cos(nu + w)
    y = cy + r * np.sin(nu + w)
    ax.plot(x, y, color=color, lw=lw, ls=ls, zorder=z)
    return x, y


def timeline(ax, events, y=0, x0=None, x1=None, color=NAVY, fs=6.8, stagger=3, height=1.0):
    """events: list of (x, text). Draws a horizontal axis with alternating labels."""
    xs = [e[0] for e in events]
    x0 = x0 if x0 is not None else min(xs)
    x1 = x1 if x1 is not None else max(xs)
    ax.plot([x0, x1], [y, y], color=color, lw=2, zorder=2)
    for i, (x, t) in enumerate(events):
        lvl = (i % stagger) + 1
        sgn = 1 if i % 2 == 0 else -1
        yy = y + sgn * height * lvl
        ax.plot([x, x], [y, yy], color=GREY, lw=0.6, zorder=1)
        ax.plot([x], [y], "o", color=ORANGE, ms=4, zorder=3)
        ax.text(x, yy + sgn * 0.15, t, ha="center", va="bottom" if sgn > 0 else "top", fontsize=fs, zorder=4,
                linespacing=1.15)


def hbar(ax, labels, values, color=BLUE, fmt="{:,.0f}", fs=7.5, highlight=None, hcolor=ORANGE):
    y = np.arange(len(labels))
    cols = [hcolor if highlight and lab in highlight else color for lab in labels]
    ax.barh(y, values, color=cols, height=0.65, zorder=2)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    vmax = max(values)
    for yi, v in zip(y, values):
        ax.text(v + vmax * 0.01, yi, fmt.format(v), va="center", fontsize=fs, color=INK)
    ax.set_xlim(0, vmax * 1.15)


def figsize(w=7.0, h=3.6):
    return plt.subplots(figsize=(w, h))


def note(ax, text, xy=(1.0, -0.2), fs=6.3, color=GREY, ha="right", va="top"):
    """Source/credit line placed below the axes (outside the plot area)."""
    ax.text(*xy, text, transform=ax.transAxes, ha=ha, va=va, fontsize=fs, color=color)


def stack(ax, x, y, w, layers, fs=7.5, gap=0.0):
    """Vertical stack of layers [(height, label, color)] from bottom upward; returns top y."""
    cy = y
    for h, text, col in layers:
        ax.add_patch(Rectangle((x, cy), w, h, fc=col, ec="white", lw=1.0, zorder=2))
        ax.text(x + w / 2, cy + h / 2, text, ha="center", va="center", fontsize=fs, zorder=3,
                color="white" if is_dark(col) else INK)
        cy += h + gap
    return cy


def is_dark(hexcol):
    hexcol = hexcol.lstrip("#")
    if len(hexcol) != 6:
        return False
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    return (0.299 * r + 0.587 * g + 0.114 * b) < 140


def table_fig(ax, rows, col_w, x=0, y=0, row_h=4, header_fc=NAVY, fs=7, zebra="#F3F6F9"):
    """Draw a small table in diagram space (rows[0] is header)."""
    cy = y
    for i, row in enumerate(rows):
        cx = x
        for j, cell in enumerate(row):
            fc = header_fc if i == 0 else (zebra if i % 2 == 0 else "white")
            ax.add_patch(Rectangle((cx, cy - row_h), col_w[j], row_h, fc=fc, ec="#D5DDE5", lw=0.5, zorder=2))
            ax.text(cx + 0.8, cy - row_h / 2, cell, va="center", ha="left", fontsize=fs,
                    color="white" if i == 0 else INK, weight="bold" if i == 0 else "normal", zorder=3)
            cx += col_w[j]
        cy -= row_h


def logspace_axis(ax, which="x"):
    if which in ("x", "both"):
        ax.set_xscale("log")
    if which in ("y", "both"):
        ax.set_yscale("log")
    ax.grid(True, which="major", color="#D5DDE5", lw=0.6)
    ax.grid(True, which="minor", color="#EEF2F6", lw=0.4)
