"""Reusable scenery and characters (world space unless noted).

World convention: x to the right, y down, ground surface at y = 0, everything above
ground has negative y. One world unit = one pixel at camera zoom 1.
"""
import math
import random
from .core import clamp, lerp
from .draw import (C, P, R, rect, grad_rect, grad_stops, glow, circle, poly, line, mix, shade, shadow)

SKY_DAY = ("#5BB8EC", "#BFE8FA")
SKY_DUSK = ("#27335E", "#F08A64", "#FFD39A")

SHIRTS = ["#EF4444", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#14B8A6", "#F97316",
          "#6366F1", "#84CC16", "#0EA5E9"]
SKINS = ["#F2C9A0", "#E0A97E", "#C68642", "#8D5524", "#FFDBAC", "#D9A27A"]
HAIRS = ["#2D2A26", "#6B4226", "#D6B370", "#111827", "#9A3412", "#4B5563"]
PANTS = ["#374151", "#1E3A8A", "#4B5563", "#3F3F46", "#7C2D12"]


def sky(c, W, H, dusk=0.0, t=0.0):
    """Screen-space sky with sun and drifting clouds."""
    top = mix(SKY_DAY[0], SKY_DUSK[0], dusk)
    mid = mix(mix(SKY_DAY[0], SKY_DAY[1], 0.5), SKY_DUSK[1], dusk)
    bot = mix(SKY_DAY[1], SKY_DUSK[2], dusk)
    grad_stops(c, 0, 0, W, H, [top, mid, bot], [0.0, 0.55, 1.0])
    # sun: high and pale by day, low and orange at dusk
    sx, sy = lerp(W * 0.80, W * 0.70, dusk), lerp(H * 0.12, H * 0.42, dusk)
    sun = mix("#FFF3B0", "#FF9E5E", dusk)
    glow(c, sx, sy, 260, sun, 0.45)
    circle(c, sx, sy, 78, sun, 1.0)
    # clouds
    rng = random.Random(7)
    for i in range(6):
        speed = 6 + rng.random() * 10
        cx = (rng.random() * (W + 600) + t * speed) % (W + 600) - 300
        cy = 140 + rng.random() * H * 0.33
        s = 0.7 + rng.random() * 0.9
        cloud(c, cx, cy, s, a=lerp(0.92, 0.55, dusk), color=mix("#FFFFFF", "#FFD6C4", dusk))


def cloud(c, x, y, s=1.0, a=0.9, color="#FFFFFF"):
    for dx, dy, r in ((-60, 10, 42), (-15, -14, 58), (40, 0, 46), (78, 16, 32)):
        circle(c, x + dx * s, y + dy * s, r * s, color, a)
    rect(c, x - 100 * s, y + 10 * s, 210 * s, 40 * s, color, a, r=20 * s)


def skyline(c, x0, x1, dusk=0.0, seed=3):
    """Distant city silhouettes standing on the ground line (world space)."""
    rng = random.Random(seed)
    far = mix("#9CC9E3", "#5B4B7A", dusk)
    near = mix("#86B8D6", "#4A3D68", dusk)
    x = x0
    while x < x1:
        w = rng.randint(160, 420)
        h = rng.randint(500, 2000)
        col = far if rng.random() < 0.5 else near
        rect(c, x, -h, w, h, col, 1.0)
        if dusk > 0.3:  # lit windows at dusk
            rr = random.Random(int(x))
            for wy in range(-h + 40, -40, 70):
                for wx in range(int(x) + 25, int(x + w) - 30, 60):
                    if rr.random() < 0.35:
                        rect(c, wx, wy, 26, 34, "#FFE29A", 0.85 * clamp((dusk - 0.3) / 0.5))
        x += w + rng.randint(30, 140)


def ground(c, x0, x1, depth=6000, dusk=0.0, seed=11):
    """Ground surface at y=0 with a cutaway of the soil below (world space)."""
    grass = mix("#5DBB63", "#3F7F55", dusk)
    grass_dark = mix("#3E9B4F", "#2E6143", dusk)
    top_soil = mix("#6E4A30", "#47301F", dusk)
    soil_top = mix("#9A6B47", "#5E3F2A", dusk)
    soil_bot = mix("#4E321F", "#24170B", dusk)
    grad_rect(c, x0, 14, x1 - x0, depth, soil_top, soil_bot)
    for i, (y, hh) in enumerate(((150, 22), (330, 30), (620, 40), (1050, 52))):
        rect(c, x0, y, x1 - x0, hh, shade(soil_top, -0.12 - 0.04 * i), 0.45)
    rect(c, x0, 14, x1 - x0, 40, top_soil)
    rect(c, x0, -4, x1 - x0, 22, grass)
    rect(c, x0, 12, x1 - x0, 8, grass_dark)
    rng = random.Random(seed)
    for _ in range(int((x1 - x0) / 140)):
        rx = rng.uniform(x0, x1)
        ry = rng.uniform(90, 1400)
        rr = rng.uniform(10, 34)
        circle(c, rx, ry, rr, shade(soil_top, -0.25), 0.55)
        circle(c, rx - rr * 0.25, ry - rr * 0.25, rr * 0.45, shade(soil_top, 0.12), 0.35)


def hand(c, x, y, s=1.0, a=1.0, skin="#E0A97E", sleeve="#3B82F6"):
    """A hand pointing left with the fingertip at (x, y); the arm comes in from the right."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, 150, -40, 520, 70, sleeve, a, r=24)
    rect(c, 140, -42, 22, 74, shade(sleeve, -0.18), a, r=8)
    rect(c, 64, -34, 94, 62, skin, a, r=26)
    rect(c, 0, -11, 88, 22, skin, a, r=11)
    rect(c, 72, 8, 50, 20, shade(skin, -0.1), a, r=10)
    rect(c, 80, -50, 44, 20, shade(skin, -0.06), a, r=10)
    c.restore()


def tree(c, x, s=1.0, dusk=0.0, kind=0):
    trunk = mix("#7C4A2D", "#4A2E1D", dusk)
    leaf = mix(["#4CAF50", "#3E9B4F", "#66BB6A"][kind % 3], "#2F5A3E", dusk)
    leaf_hi = shade(leaf, 0.18)
    rect(c, x - 12 * s, -170 * s, 24 * s, 170 * s, trunk, r=6 * s)
    for dx, dy, r in ((-55, -210, 72), (50, -220, 66), (0, -285, 84), (0, -200, 70)):
        circle(c, x + dx * s, dy * s, r * s, leaf)
    circle(c, x - 20 * s, -300 * s, 40 * s, leaf_hi, 0.6)


def house(c, x, w=420, h=300, wall="#F4E3C3", roof="#B84A3A", dusk=0.0, lit=0.0):
    wall = mix(wall, shade(wall, -0.45), dusk)
    roof = mix(roof, shade(roof, -0.45), dusk)
    shadow(c, x - w / 2, -h, w, h, r=4, a=0.18, blur=10, dy=6)
    rect(c, x - w / 2, -h, w, h, wall)
    poly(c, [(x - w / 2 - 30, -h + 4), (x, -h - h * 0.55), (x + w / 2 + 30, -h + 4)], roof)
    win = mix("#BDE6F7", "#FFD98A", lit)
    for wx in (x - w * 0.32, x + w * 0.12):
        rect(c, wx, -h * 0.72, w * 0.2, h * 0.28, "#FFFFFF", r=4)
        rect(c, wx + 6, -h * 0.72 + 6, w * 0.2 - 12, h * 0.28 - 12, win, r=3)
    rect(c, x - w * 0.06, -h * 0.42, w * 0.13, h * 0.42, shade(wall, -0.35), r=4)


def person(c, x, y, h=140, shirt="#3B82F6", skin="#F2C9A0", hair="#2D2A26", pants="#374151",
           arms_up=0.0, lean=0.0, walk=0.0, a=1.0, sweat=0.0, scale_y=1.0, hair_style=0):
    """Faceless rounded character standing with feet at (x, y)."""
    if a <= 0:
        return
    u = h / 140.0
    c.save()
    c.translate(x, y)
    c.rotate(lean * 12)
    c.scale(1, scale_y)
    # legs (walk swings them)
    sw = math.sin(walk * math.pi * 2) * 10 * u if walk else 0
    rect(c, -16 * u + sw * 0.3, -52 * u, 13 * u, 52 * u, pants, a, r=6 * u)
    rect(c, 3 * u - sw * 0.3, -52 * u, 13 * u, 52 * u, pants, a, r=6 * u)
    # arms behind body
    arm_y = -100 * u
    for side in (-1, 1):
        ex = side * 30 * u
        ey = lerp(-48 * u, -140 * u, arms_up)
        line(c, side * 18 * u, arm_y, ex, ey, skin, w=11 * u, a=a)
    # body
    rect(c, -22 * u, -112 * u, 44 * u, 66 * u, shirt, a, r=16 * u)
    rect(c, -22 * u, -112 * u, 44 * u, 18 * u, shade(shirt, 0.12), a * 0.6, r=9 * u)
    # head + hair
    circle(c, 0, -128 * u, 19 * u, skin, a)
    if hair_style == 0:
        poly_hair(c, u, hair, a)
    else:
        circle(c, 0, -136 * u, 17 * u, hair, a)
        rect(c, -19 * u, -137 * u, 38 * u, 10 * u, hair, a, r=4 * u)
    if sweat > 0:
        for i, (sx, sy) in enumerate(((24, -150), (-26, -142))):
            yy = sy * u + ((sweat * 40 + i * 13) % 26) * u
            circle(c, sx * u, yy, 4.5 * u, "#7DD3FC", a * min(1, sweat * 2))
            poly(c, [(sx * u - 4.5 * u, yy), (sx * u, yy - 11 * u), (sx * u + 4.5 * u, yy)], "#7DD3FC", a * min(1, sweat * 2))
    c.restore()


def poly_hair(c, u, hair, a):
    path_pts = [(-20 * u, -126 * u), (-18 * u, -140 * u), (-8 * u, -149 * u), (8 * u, -149 * u),
                (19 * u, -140 * u), (20 * u, -128 * u), (12 * u, -136 * u), (-6 * u, -138 * u)]
    poly(c, path_pts, hair, a)


def crowd_colors(i):
    return dict(shirt=SHIRTS[i % len(SHIRTS)], skin=SKINS[(i * 3 + 1) % len(SKINS)],
                hair=HAIRS[(i * 5 + 2) % len(HAIRS)], pants=PANTS[(i * 2) % len(PANTS)], hair_style=i % 2)


def room_decor(c, x, y_ceil, w, h, seed, lights=1.0, dusk=0.0):
    """Back-wall details for a cutaway room spanning [x, x+w] x [y_ceil, y_ceil+h] (floor at bottom)."""
    rng = random.Random(seed)
    floor_y = y_ceil + h
    # window on the back wall
    ww, wh = w * 0.26, h * 0.42
    wx = x + w * rng.uniform(0.45, 0.62)
    wy = y_ceil + h * 0.18
    rect(c, wx - 6, wy - 6, ww + 12, wh + 12, "#FFFFFF", 0.95, r=6)
    view = mix("#AEE1F7", "#3A3F6B", dusk)
    rect(c, wx, wy, ww, wh, view, 1.0, r=3)
    line(c, wx + ww / 2, wy, wx + ww / 2, wy + wh, "#FFFFFF", 5)
    # floor line / baseboard
    rect(c, x, floor_y - 10, w, 10, "#000000", 0.08)
    kind = rng.randint(0, 2)
    if kind == 0:  # couch
        col = rng.choice(["#E76F51", "#2A9D8F", "#457B9D", "#B5838D"])
        rect(c, x + w * 0.12, floor_y - 62, w * 0.3, 52, col, r=12)
        rect(c, x + w * 0.12, floor_y - 84, w * 0.3, 30, shade(col, -0.12), r=10)
    elif kind == 1:  # desk + chair
        rect(c, x + w * 0.1, floor_y - 74, w * 0.26, 12, "#8D6E63", r=4)
        rect(c, x + w * 0.11, floor_y - 64, 8, 64, "#6D4C41")
        rect(c, x + w * 0.33, floor_y - 64, 8, 64, "#6D4C41")
        rect(c, x + w * 0.2, floor_y - 100, 44, 28, "#263238", r=4)
    else:  # bookshelf
        rect(c, x + w * 0.1, floor_y - 150, w * 0.14, 150, "#A1887F", r=4)
        for k in range(4):
            for b in range(5):
                bc = ["#E63946", "#457B9D", "#F4A261", "#2A9D8F", "#8338EC"][(b + k) % 5]
                rect(c, x + w * 0.1 + 6 + b * (w * 0.14 - 12) / 5, floor_y - 140 + k * 36,
                     (w * 0.14 - 14) / 5, 26, bc, 0.9)
    # plant
    px = x + w * rng.uniform(0.82, 0.9)
    rect(c, px - 14, floor_y - 36, 28, 36, "#C0754A", r=5)
    for ang in (-40, -10, 20, 45):
        rad = math.radians(ang - 90)
        line(c, px, floor_y - 34, px + math.cos(rad) * 34, floor_y - 34 + math.sin(rad) * 44, "#3E9B4F", 9)
    # ceiling lamp
    lx = x + w * rng.uniform(0.3, 0.5)
    line(c, lx, y_ceil, lx, y_ceil + 26, "#555555", 3)
    poly(c, [(lx - 20, y_ceil + 44), (lx - 10, y_ceil + 26), (lx + 10, y_ceil + 26), (lx + 20, y_ceil + 44)], "#374151")
    if lights > 0:
        glow(c, lx, y_ceil + 50, 120, "#FFE7A3", 0.55 * lights)
        circle(c, lx, y_ceil + 46, 7, "#FFF6C9", lights)
