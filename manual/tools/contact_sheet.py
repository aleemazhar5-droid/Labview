#!/usr/bin/env python3
"""Make labelled contact sheets of photos for visual review: contact_sheet.py out.jpg key1 key2 ... (or 'all')."""
import sys, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "figures/photos"
out = sys.argv[1]; keys = sys.argv[2:]
if keys == ["all"]:
    keys = sorted(p.stem for p in P.glob("*.jpg"))
cols = 5; tw, th = 300, 210
rows = (len(keys) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * (th + 18)), "white")
d = ImageDraw.Draw(sheet)
try:
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
except Exception:
    f = None
for i, k in enumerate(keys):
    im = Image.open(P / f"{k}.jpg"); im.thumbnail((tw - 6, th - 6))
    x, y = (i % cols) * tw, (i // cols) * (th + 18)
    sheet.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
    d.text((x + 4, y + th + 1), k, fill="black", font=f)
sheet.save(out, quality=80)
print(out, len(keys))
