"""
HUD texture generator using Pillow.
Creates SVG-quality PNG textures for each cockpit panel.
"""

import os
import math
import tempfile


def _pil_to_texture(img, name):
    """Convert PIL Image to Panda3D Texture via a temp PNG file."""
    from panda3d.core import PNMImage, Texture

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".png", prefix="hud_")
    try:
        os.close(tmp_fd)
        img.save(tmp_path, format="PNG")

        pnm = PNMImage()
        pnm.read(tmp_path)

        tex = Texture(name)
        tex.load(pnm)
        tex.set_minfilter(Texture.FT_linear)
        tex.set_magfilter(Texture.FT_linear)
        return tex
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def create_radar_bg(size=512):
    """
    Radar background: dark navy field, three concentric green rings,
    8-point crosshair, tick marks, north arrow, corner brackets.
    """
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (size, size), (0, 8, 22, 238))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r_max = int(size * 0.43)
    r_mid = r_max * 2 // 3
    r_min = r_max // 3

    G   = (0, 255, 80, 220)   # bright green
    Gd  = (0, 200, 60, 140)   # medium green
    Gf  = (0, 140, 40, 70)    # faint green
    Gcx = (0, 180, 55, 45)    # crosshair

    # ── concentric rings ─────────────────────────────────────────────
    draw.ellipse([cx-r_max, cy-r_max, cx+r_max, cy+r_max], outline=G,  width=2)
    draw.ellipse([cx-r_mid, cy-r_mid, cx+r_mid, cy+r_mid], outline=Gd, width=1)
    draw.ellipse([cx-r_min, cy-r_min, cx+r_min, cy+r_min], outline=Gf, width=1)

    # ── crosshairs ──────────────────────────────────────────────────
    draw.line([(cx, cy - r_max), (cx, cy + r_max)],       fill=Gcx, width=1)
    draw.line([(cx - r_max, cy), (cx + r_max, cy)],       fill=Gcx, width=1)
    d = int(r_max * 0.707)
    draw.line([(cx-d, cy-d), (cx+d, cy+d)], fill=(0, 140, 40, 25), width=1)
    draw.line([(cx+d, cy-d), (cx-d, cy+d)], fill=(0, 140, 40, 25), width=1)

    # ── tick marks on outer ring (every 30°, longer at cardinal) ────
    for deg in range(0, 360, 30):
        rad = math.radians(deg - 90)        # −90 so 0 ° = top
        ca, sa = math.cos(rad), math.sin(rad)
        is_card = (deg % 90 == 0)
        tick_len   = 14 if is_card else 7
        tick_color = G  if is_card else Gd
        tick_w     = 2  if is_card else 1
        x1 = cx + int((r_max - tick_len) * ca)
        y1 = cy + int((r_max - tick_len) * sa)
        x2 = cx + int(r_max * ca)
        y2 = cy + int(r_max * sa)
        draw.line([(x1, y1), (x2, y2)], fill=tick_color, width=tick_w)

    # ── north triangle ───────────────────────────────────────────────
    tip = cy - r_max - 6
    draw.polygon(
        [(cx, tip - 10), (cx - 6, tip + 4), (cx + 6, tip + 4)],
        fill=(0, 255, 80, 230),
    )

    # ── ship dot at center ───────────────────────────────────────────
    draw.ellipse([cx-8, cy-8, cx+8, cy+8], outline=(0, 200, 60, 120), width=1)
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(0, 255, 80, 255))

    # ── outer border ─────────────────────────────────────────────────
    draw.rectangle([1, 1, size-2, size-2], outline=(0, 170, 55, 180), width=1)

    # ── corner brackets ──────────────────────────────────────────────
    clen = 22
    cc   = (0, 255, 80, 230)
    for (x0, y0), (dx, dy) in [
        ((0, 0),        ( clen, 0)),   ((0, 0),        (0,  clen)),
        ((size-1, 0),   (-clen, 0)),   ((size-1, 0),   (0,  clen)),
        ((0, size-1),   ( clen, 0)),   ((0, size-1),   (0, -clen)),
        ((size-1,size-1),(-clen,0)),   ((size-1,size-1),(0,-clen)),
    ]:
        draw.line([(x0, y0), (x0+dx, y0+dy)], fill=cc, width=3)

    # ── subtle inner glow ────────────────────────────────────────────
    for step in range(1, 5):
        rg = r_max * step // 5
        draw.ellipse([cx-rg, cy-rg, cx+rg, cy+rg], fill=(0, 255, 80, 4))

    return _pil_to_texture(img, "RadarBG")


def create_status_panel_bg(width=256, height=420):
    """
    Status panel: dark purple-black, green corner brackets,
    horizontal section dividers, decorative side bars.
    """
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (width, height), (4, 0, 18, 238))
    draw = ImageDraw.Draw(img)

    G   = (0, 210, 70, 220)
    Gbr = (0, 255, 80, 230)
    Gd  = (0, 150, 50, 100)

    # Outer border
    draw.rectangle([0, 0, width-1, height-1], outline=G, width=1)

    # Corner brackets
    clen = 16
    for (x0, y0), (dx, dy) in [
        ((0, 0),           ( clen, 0)),   ((0, 0),           (0,  clen)),
        ((width-1, 0),     (-clen, 0)),   ((width-1, 0),     (0,  clen)),
        ((0, height-1),    ( clen, 0)),   ((0, height-1),    (0, -clen)),
        ((width-1,height-1),(-clen,0)),   ((width-1,height-1),(0,-clen)),
    ]:
        draw.line([(x0, y0), (x0+dx, y0+dy)], fill=Gbr, width=3)

    # Title bar shading
    draw.rectangle([2, 2, width-2, 46], fill=(0, 30, 10, 90))

    # Section dividers (horizontal lines with diamond end caps)
    dividers = [48, 118, 188, 258, 328, 378]
    for sy in dividers:
        if 0 < sy < height:
            draw.line([(8, sy), (width-8, sy)], fill=Gd, width=1)
            draw.polygon([(4,sy),(8,sy-4),(12,sy),(8,sy+4)], fill=Gd)
            draw.polygon([(width-4,sy),(width-8,sy-4),(width-12,sy),(width-8,sy+4)], fill=Gd)

    # Side indicator bars
    for i in range(14):
        y = 28 + i * (height - 56) // 14
        h = 4 + (i % 3) * 2
        draw.rectangle([2, y, 3, y+h],         fill=(0, 180, 50, 140))
        draw.rectangle([width-4, y, width-3, y+h], fill=(0, 180, 50, 140))

    return _pil_to_texture(img, "StatusPanel")


def create_comms_panel_bg(width=480, height=160):
    """
    Comms panel: dark navy, cyan corner brackets, signal-wave
    decoration, horizontal divider below the title area.
    """
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (width, height), (0, 5, 25, 235))
    draw = ImageDraw.Draw(img)

    C   = (0, 190, 255, 200)
    Cbr = (0, 225, 255, 245)

    # Outer border
    draw.rectangle([0, 0, width-1, height-1], outline=C, width=1)

    # Corner brackets
    clen = 16
    for (x0, y0), (dx, dy) in [
        ((0, 0),          ( clen, 0)),   ((0, 0),          (0,  clen)),
        ((width-1, 0),    (-clen, 0)),   ((width-1, 0),    (0,  clen)),
        ((0, height-1),   ( clen, 0)),   ((0, height-1),   (0, -clen)),
        ((width-1,height-1),(-clen,0)),  ((width-1,height-1),(0,-clen)),
    ]:
        draw.line([(x0, y0), (x0+dx, y0+dy)], fill=Cbr, width=3)

    # Title bar shading
    draw.rectangle([2, 2, width-2, 44], fill=(0, 20, 50, 90))
    draw.line([(5, 45), (width-5, 45)], fill=(0, 140, 200, 100), width=1)

    # Signal wave bars (left side decoration)
    for i in range(8):
        bh = int(12 * abs(math.sin(i * 0.65)) + 5)
        bx = 8 + i * 7
        by = height - 20 - bh
        alpha = max(60, 160 - i * 15)
        draw.rectangle([bx, by, bx+4, by+bh], fill=(0, 200, 255, alpha))

    # Diamond top decorations
    for xd in [width//4, width//2, 3*width//4]:
        draw.polygon([(xd,0),(xd+5,5),(xd,10),(xd-5,5)], fill=(0, 190, 255, 160))

    return _pil_to_texture(img, "CommsPanel")


def create_bottom_panel_bg(width=512, height=160):
    """Controls / help panel with cyan decorations."""
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (width, height), (0, 4, 22, 225))
    draw = ImageDraw.Draw(img)

    C   = (0, 180, 255, 190)
    Cbr = (0, 220, 255, 230)

    draw.rectangle([0, 0, width-1, height-1], outline=C, width=1)

    clen = 14
    for (x0, y0), (dx, dy) in [
        ((0, 0),          ( clen, 0)),   ((0, 0),          (0,  clen)),
        ((width-1, 0),    (-clen, 0)),   ((width-1, 0),    (0,  clen)),
        ((0, height-1),   ( clen, 0)),   ((0, height-1),   (0, -clen)),
        ((width-1,height-1),(-clen,0)),  ((width-1,height-1),(0,-clen)),
    ]:
        draw.line([(x0, y0), (x0+dx, y0+dy)], fill=Cbr, width=2)

    draw.rectangle([2, 2, width-2, 44], fill=(0, 18, 45, 90))
    draw.line([(5, 45), (width-5, 45)], fill=(0, 120, 180, 100), width=1)

    return _pil_to_texture(img, "BottomPanel")


def create_crosshair(size=256):
    """
    Transparent targeting reticle: broken outer ring,
    corner brackets, small inner crosshair, center dot.
    """
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    G   = (0, 255, 80, 200)
    Gd  = (0, 180, 55, 120)

    # Broken ring (4 arcs, each 30° wide, at 45° diagonals)
    r = 68
    for start in (25, 115, 205, 295):
        draw.arc([cx-r, cy-r, cx+r, cy+r], start=start, end=start+30,
                 fill=G, width=2)

    # Corner targeting brackets
    blen = 20
    boff = 52
    for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        bx, by = cx + dx * boff, cy + dy * boff
        draw.line([(bx, by), (bx + dx*blen, by)], fill=G, width=2)
        draw.line([(bx, by), (bx, by + dy*blen)], fill=G, width=2)

    # Short inner crosshair arms (gap in centre)
    gap, arm = 9, 18
    draw.line([(cx - gap - arm, cy), (cx - gap, cy)], fill=Gd, width=1)
    draw.line([(cx + gap, cy),        (cx + gap + arm, cy)], fill=Gd, width=1)
    draw.line([(cx, cy - gap - arm),  (cx, cy - gap)], fill=Gd, width=1)
    draw.line([(cx, cy + gap),        (cx, cy + gap + arm)], fill=Gd, width=1)

    # Centre dot
    draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(0, 255, 80, 220))

    return _pil_to_texture(img, "Crosshair")


def create_blip_texture(r, g, b, size=20):
    """Glowing coloured dot for a radar entity blip."""
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    outer = size // 2 - 1

    draw.ellipse([cx-outer-1, cy-outer-1, cx+outer+1, cy+outer+1],
                 fill=(r, g, b, 45))
    draw.ellipse([cx-outer,   cy-outer,   cx+outer,   cy+outer],
                 fill=(r, g, b, 180))
    draw.ellipse([cx-2, cy-2, cx+2, cy+2],
                 fill=(r, g, b, 255))

    return _pil_to_texture(img, f"Blip_{r}_{g}_{b}")
