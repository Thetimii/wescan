#!/usr/bin/env python3
"""WESCAN Brand Kit Generator — Scan Horizon Philosophy"""

from PIL import Image, ImageDraw, ImageFont
import math, os, random

random.seed(42)

FONT_DIR = os.path.expanduser("~/.claude/skills/canvas-design/canvas-fonts/")
OUT = "/Users/timsager/Desktop/tnt wescan/website/wescan-brand-kit.png"

# Canvas
W, H = 2800, 3700
MX = 160  # horizontal margin

# ── Brand Colors ──────────────────────────────────────────────────────────────
INK       = (14,  21,  32)      # #0E1520  primary dark
BLUE      = (28,  92,  230)     # #1C5CE6  scan blue
SNOW      = (246, 245, 240)     # #F6F5F0  warm white
GRAPHITE  = (58,  67,  80)      # #3A4350  secondary
FOG       = (180, 188, 200)     # #B4BCC8  neutral
WHITE     = (255, 255, 255)

BLUE_TOP   = (72,  148, 255)    # lighter — top cube face
BLUE_RIGHT = (28,  92,  230)    # mid      — right cube face
BLUE_LEFT  = (14,  55,  168)    # dark     — left cube face

DOT_BG     = (22,  36,  56)     # subtle dot grid on dark bg
LINE_RULE  = (38,  54,  76)     # subtle dividers on dark bg

# ── Font Loader ───────────────────────────────────────────────────────────────
def F(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f"  [font warn] {name}: {e}")
        return ImageFont.load_default()

# ── Isometric Cube ────────────────────────────────────────────────────────────
def iso_cube(draw, cx, cy, s, outline, lw=4,
             fill_top=None, fill_right=None, fill_left=None):
    """Draw isometric cube (3 faces visible). s = half-size."""
    top = (cx,             cy - s)
    ur  = (cx + s*0.866,   cy - s*0.5)
    lr  = (cx + s*0.866,   cy + s*0.5)
    bot = (cx,             cy + s)
    ll  = (cx - s*0.866,   cy + s*0.5)
    ul  = (cx - s*0.866,   cy - s*0.5)
    ctr = (cx,             cy)

    if fill_top:   draw.polygon([top, ur, ctr, ul], fill=fill_top)
    if fill_right: draw.polygon([ur,  lr, bot, ctr], fill=fill_right)
    if fill_left:  draw.polygon([ul, ctr, bot,  ll], fill=fill_left)

    hexpts = [top, ur, lr, bot, ll, ul]
    for i in range(6):
        draw.line([hexpts[i], hexpts[(i+1)%6]], fill=outline, width=lw)
    draw.line([top, ctr], fill=outline, width=lw)
    draw.line([lr,  ctr], fill=outline, width=lw)
    draw.line([ll,  ctr], fill=outline, width=lw)

# ── Scan Dot Cloud ────────────────────────────────────────────────────────────
def scan_cloud(draw, cx, cy, inner_r, outer_r, n, color, dim_color):
    for i in range(n):
        angle  = random.uniform(0, 2*math.pi)
        dist   = random.uniform(inner_r, outer_r)
        px     = cx + math.cos(angle) * dist
        py     = cy + math.sin(angle) * dist * 0.62  # flatten iso
        r      = random.choice([3, 4, 5, 6])
        col    = color if dist < (inner_r + outer_r)*0.6 else dim_color
        draw.ellipse([px-r, py-r, px+r, py+r], fill=col)

# ── Create Canvas ─────────────────────────────────────────────────────────────
img = Image.new('RGB', (W, H), SNOW)
d   = ImageDraw.Draw(img)

# Pre-load fonts
f_tiny    = F("GeistMono-Regular.ttf",        22)
f_label   = F("GeistMono-Regular.ttf",        26)
f_section = F("GeistMono-Regular.ttf",        24)
f_logo    = F("BigShoulders-Bold.ttf",       240)
f_var_wrd = F("BigShoulders-Bold.ttf",        76)
f_h2      = F("WorkSans-Bold.ttf",            64)
f_h3      = F("WorkSans-Bold.ttf",            42)
f_tag     = F("InstrumentSans-Italic.ttf",    44)
f_body    = F("InstrumentSans-Regular.ttf",   36)

# =============================================================================
# HERO  (dark, full width, 1120px tall)
# =============================================================================
HERO_H = 1140
d.rectangle([0, 0, W, HERO_H], fill=INK)

# Dot-grid — slightly tighter spacing for density
for row in range(0, HERO_H//50 + 2):
    for col in range(0, W//50 + 2):
        px, py = col*50 + 18, row*50 + 18
        d.ellipse([px-2, py-2, px+2, py+2], fill=DOT_BG)

# Left blue accent bar — 2px wider for more weight
d.rectangle([0, 0, 10, HERO_H], fill=BLUE)
# Bottom edge — blue accent line
d.rectangle([0, HERO_H - 4, W, HERO_H], fill=BLUE)

# Top metadata strip
d.text((MX,          68), "WESCAN — BRAND IDENTITY",     font=f_label, fill=FOG)
d.text((W - MX - 360, 68), "DEUTSCHSCHWEIZ · 2025",      font=f_label, fill=FOG)
d.rectangle([MX, 110, W-MX, 112], fill=LINE_RULE)

# Perspective grid lines from a far vanishing point — right side of hero
VPX, VPY = W + 800, HERO_H // 2   # vanishing point far right
for start_y in range(130, HERO_H, 90):
    d.line([(0, start_y), (VPX, VPY)], fill=LINE_RULE, width=1)

# Horizontal cross-lines (grid)
for gy in range(130, HERO_H, 90):
    d.line([(0, gy), (W//2 - 50, gy)], fill=LINE_RULE, width=1)

# ── Logo Icon ────────────────────────────────────────────────────────────────
ICON_CX = 400
ICON_CY = HERO_H // 2 + 20
ICON_S  = 148

# Outer glow ring — subtle circle behind cube
for ring_r, ring_col in [(230, (20, 38, 65)), (180, (24, 44, 76))]:
    d.ellipse([ICON_CX-ring_r, ICON_CY-ring_r*0.62,
               ICON_CX+ring_r, ICON_CY+ring_r*0.62], outline=(32,56,96), width=1)

scan_cloud(d, ICON_CX, ICON_CY, ICON_S * 1.3, ICON_S * 2.5, 34,
           BLUE, (48, 80, 140))

iso_cube(d, ICON_CX, ICON_CY, ICON_S, WHITE,
         fill_top=BLUE_TOP, fill_right=BLUE_RIGHT, fill_left=BLUE_LEFT, lw=3)

# ── Wordmark ─────────────────────────────────────────────────────────────────
WX = 640
WY = HERO_H // 2 - 160

# Hairline rule above wordmark
d.rectangle([WX, WY - 28, WX + 900, WY - 26], fill=(38, 56, 84))

d.text((WX, WY), "WESCAN", font=f_logo, fill=WHITE)

# Blue filled square accent after wordmark
try:
    bbox = d.textbbox((WX, WY), "WESCAN", font=f_logo)
    ww = bbox[2] - bbox[0]
except:
    ww = 1440
sq_x = WX + ww + 20
sq_y = WY + 24
d.rectangle([sq_x, sq_y, sq_x + 52, sq_y + 52], fill=BLUE)

# Thin rule between wordmark and tagline
d.rectangle([WX, WY + 256, W - MX - 100, WY + 258], fill=LINE_RULE)

# Tagline — slightly larger
d.text((WX + 4, WY + 278), "3D Raumtouren für Airbnb & Wohnungen",
       font=f_tag, fill=FOG)

# Location label
d.text((WX + 4, WY + 354), "ZÜRICH  ·  BERN  ·  LUZERN  ·  SCHWEIZ",
       font=f_label, fill=(72, 116, 192))

# Thin baseline under full block
d.rectangle([WX, WY + 400, W - MX, WY + 402], fill=LINE_RULE)


# =============================================================================
# COLOR SYSTEM
# =============================================================================
y = HERO_H + 110

d.text((MX, y), "01 — FARBSYSTEM  /  COLOR SYSTEM", font=f_section, fill=FOG)
d.rectangle([MX, y+46, W-MX, y+48], fill=FOG)
y += 88

PALETTE = [
    ("Nacht",     INK,      "#0E1520", "Primary Dark"),
    ("Scan",      BLUE,     "#1C5CE6", "Primary Accent"),
    ("Schneiss",  SNOW,     "#F6F5F0", "Background"),
    ("Graphit",   GRAPHITE, "#3A4350", "Secondary"),
    ("Nebel",     FOG,      "#B4BCC8", "Neutral"),
]
N     = len(PALETTE)
CGAP  = 44
SW    = (W - 2*MX - (N-1)*CGAP) // N
SH    = 310

for i, (name, rgb, hex_c, desc) in enumerate(PALETTE):
    sx = MX + i*(SW + CGAP)
    sy = y
    # Swatch with slight shadow offset for depth
    d.rectangle([sx+4, sy+4, sx+SW+4, sy+SH+4], fill=(210, 210, 208))  # shadow
    d.rectangle([sx, sy, sx+SW, sy+SH], fill=rgb)
    # Always draw a 1px border — invisible on dark, subtle on light
    border_col = FOG if rgb in (SNOW, FOG) else (255,255,255,0)
    if rgb in (SNOW, FOG):
        d.rectangle([sx, sy, sx+SW, sy+SH], outline=GRAPHITE, width=1)

    # Small color index number inside swatch (top-right)
    idx_f = F("GeistMono-Regular.ttf", 20)
    num_col = WHITE if rgb not in (SNOW, FOG) else GRAPHITE
    d.text((sx + SW - 42, sy + 16), f"0{i+1}", font=idx_f, fill=num_col)

    ty = sy + SH + 24
    d.text((sx, ty),       name.upper(),  font=f_h3,    fill=INK)
    d.text((sx, ty + 54),  hex_c,         font=f_label, fill=GRAPHITE)
    d.text((sx, ty + 94),  desc,          font=f_tiny,  fill=FOG)

y += SH + 220


# =============================================================================
# TYPOGRAPHY
# =============================================================================
d.text((MX, y), "02 — TYPOGRAFIE  /  TYPOGRAPHY", font=f_section, fill=FOG)
d.rectangle([MX, y+46, W-MX, y+48], fill=FOG)
y += 88

TYPE_ROWS = [
    ("BigShoulders-Bold.ttf",       112, "Display Headline",
     "BigShoulders Bold — Titel & Markenauftritt", INK),
    ("WorkSans-Bold.ttf",            66, "Abschnittstitel",
     "Work Sans Bold — Subheadings & Labels",      GRAPHITE),
    ("InstrumentSans-Regular.ttf",   42, "Fliesstext für klare Kommunikation.",
     "Instrument Sans — Body & Beschreibungen",     GRAPHITE),
    ("GeistMono-Regular.ttf",        30, "scan_ref: WSC–2025–A1",
     "Geist Mono — Technische IDs & Daten",         BLUE),
]

ROW_H = 176
for fname, fsize, sample, desc_txt, col in TYPE_ROWS:
    fs = F(fname, fsize)
    d.text((MX, y),              sample,   font=fs,      fill=col)
    d.text((MX + 4, y+fsize+12), desc_txt, font=f_tiny,  fill=FOG)
    y += ROW_H


# =============================================================================
# LOGO VARIATIONS
# =============================================================================
y += 40
d.text((MX, y), "03 — LOGO-VARIANTEN  /  LOGO VARIANTS", font=f_section, fill=FOG)
d.rectangle([MX, y+46, W-MX, y+48], fill=FOG)
y += 88

N3    = 3
VGAP  = 60
VW    = (W - 2*MX - (N3-1)*VGAP) // N3
VH    = 280

# Variant 1 — Dark background (primary)
vx = MX
d.rectangle([vx, y, vx+VW, y+VH], fill=INK)
iso_cube(d, vx+100, y+VH//2, 68, WHITE,
         fill_top=BLUE_TOP, fill_right=BLUE_RIGHT, fill_left=BLUE_LEFT, lw=2)
d.text((vx+204, y+VH//2-50), "WESCAN", font=f_var_wrd, fill=WHITE)
d.text((vx,     y+VH+18),    "Primär — Dunkler Hintergrund", font=f_tiny, fill=FOG)

# Variant 2 — Light background (secondary)
vx = MX + VW + VGAP
d.rectangle([vx, y, vx+VW, y+VH], fill=SNOW)
d.rectangle([vx, y, vx+VW, y+VH], outline=FOG, width=2)
iso_cube(d, vx+100, y+VH//2, 68, INK,
         fill_top=(100,168,255), fill_right=BLUE, fill_left=(16,55,168), lw=2)
d.text((vx+204, y+VH//2-50), "WESCAN", font=f_var_wrd, fill=INK)
d.text((vx,     y+VH+18),    "Sekundär — Heller Hintergrund",  font=f_tiny, fill=FOG)

# Variant 3 — Icon only, Scan Blue
vx = MX + 2*(VW + VGAP)
d.rectangle([vx, y, vx+VW, y+VH], fill=BLUE)
iso_cube(d, vx+VW//2, y+VH//2, 96, WHITE,
         fill_top=(110,178,255), fill_right=(44,108,240), fill_left=(18,62,186), lw=3)
d.text((vx,     y+VH+18),    "Akzent — Scan Blue / Icon",      font=f_tiny, fill=FOG)

y += VH + 90


# =============================================================================
# FOOTER
# =============================================================================
y_foot = H - 110
d.rectangle([0, y_foot - 6, W, H], fill=INK)
d.rectangle([0, y_foot - 6, W, y_foot - 2], fill=BLUE)
d.rectangle([0, 0, 10, H], fill=BLUE)   # left accent runs full height

d.text((MX,           y_foot + 18),
       "WESCAN® — 3D Raumtouren, Deutschschweiz — wescan.ch — © 2025",
       font=f_tiny, fill=FOG)
d.text((W - MX - 440, y_foot + 18),
       "Brand Identity System — Scan Horizon",
       font=f_tiny, fill=FOG)
# Small blue squares in footer as decorative endpoints
d.rectangle([W - MX - 20, y_foot + 22, W - MX, y_foot + 44], fill=BLUE)

# =============================================================================
# SAVE
# =============================================================================
img.save(OUT, "PNG", dpi=(300, 300))
print(f"✓  Saved → {OUT}")
