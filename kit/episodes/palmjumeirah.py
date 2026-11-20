"""Episode 52 - The Palm Jumeirah.  v2 look: a turquoise Gulf seen from above, a palm of sand with sixteen fronds and a
crescent of rock around it, Dubai's coast at the bottom.

Sets: top (hook: the palm grows out of the sea, the crescent closes round it, villas appear; reveal: two gaps open in
the crescent and fresh sea water flows in, villas fill the fronds; stat; closer at dusk with the lights on), coast
(break1: a short strip of beach packed with hotels), plan (fix1: the blueprint, a trunk and sixteen fronds counted one by
one, beach lines glowing along every frond), sand (break2: fine desert sand washed away by a wave; fix2: a dredger sucks
sand off the sea floor and sprays it in a huge arc, rainbowing, onto the growing frond), storm (break3: storm waves eat
the frond tips; fix3: a crescent of rock 11 km long closes round the palm, then a crane barge sets one boulder), quake
(break4: loose wet sand turns to soup and a villa sinks; fix4: vibrating probes shake the grains tight and the villa
stands), tag (a sandwich at the beach, full of sand).
World (top): seen from above, the crown's centre at (0, 0), 1 unit is about 5 m; the coast at y = 900.
"""
from v2_base import *  # noqa: F401,F403
from burjalarab import path_of, wave, palm_tree, sea_band  # noqa: E402
from windtower import arrow, sun  # noqa: E402
from falaj import word  # noqa: E402

GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
TURQ, TURQ_D, SHALLOW = "#16879A", "#0A4E66", "#3CB3BC"
SANDC, SAND_D, BEACH = "#C4A870", "#8E7244", "#D8C08A"
ROCKC, ROCK_D = "#7E858F", "#4B5260"
ROOFS = ("#D9D4CA", "#B4532A", "#CFC6B6", "#9A4A2A")
R_TIP, RC, RC_Y = 450.0, 548.0, 12.0                     # frond tip circle, crescent radius and centre y
GAPS = (24.0, 156.0)                                     # the two openings in the crescent (degrees)


def frond(i, side):
    """Base and tip of frond i (0 = nearest the coast .. 7 = top) on side +1 (right) or -1 (left)."""
    y0 = 300 - i * 82
    ph = math.radians(lerp(-25, 62, i / 7.0))
    return (0.0, y0), (side * R_TIP * math.cos(ph), -R_TIP * math.sin(ph))


FRONDS = [frond(i, sd) for i in range(8) for sd in (1, -1)]           # 16 fronds, ordered bottom to top


def arc_pts(a0, a1, r=RC, n=60, cy=RC_Y):
    """Points of the crescent's centre line from angle a0 to a1 (degrees, counter-clockwise, 0 = right, 90 = up)."""
    return [(r * math.cos(math.radians(lerp(a0, a1, k / float(n)))), cy - r * math.sin(math.radians(lerp(a0, a1, k / float(n)))))
            for k in range(n + 1)]


def stroke_path(c, pts, col, w, a=1.0):
    if len(pts) >= 2 and a > 0:
        c.drawPath(path_of(pts), P(col, a, stroke=w))


def sea_top(c, t, x0=-2000, x1=2000, y0=-2200, y1=2200, dusk=0.0, storm=0.0):
    """The sea seen from above (world space): turquoise with moving glints."""
    top = mix(mix(TURQ, "#0E5A78", storm), "#2A8FA0", dusk)
    deep = mix(mix(TURQ_D, "#082A44", storm), "#245A7A", dusk)
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), lin_paint(0, y0, 0, y1, [deep, top, top], [0.0, 0.55, 1.0]))
    rng = random.Random(3)
    for _ in range(140):
        gx, gy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        ph = rng.uniform(0, 6.28)
        L_ = rng.uniform(14, 40)
        aa = (0.18 + 0.2 * storm) * (0.5 + 0.5 * math.sin(t * 1.6 + ph))
        c.drawLine(gx - L_ / 2 + math.sin(t + ph) * 6, gy, gx + L_ / 2 + math.sin(t + ph) * 6, gy, P("#BDEFFF", aa * (1 - 0.6 * dusk), stroke=3))


def coast_top(c, t, y=900, dusk=0.0):
    """Dubai's coast at the bottom (world space): beach, road and city blocks with their shadows."""
    c.drawRect(R(-1400, y, 2800, 40), P(BEACH))
    c.drawRect(R(-1400, y + 40, 2800, 900), P(mix("#5E6470", "#2A2E40", dusk)))
    c.drawRect(R(-1400, y + 70, 2800, 14), P("#3A3F4C"))
    rng = random.Random(8)
    for k in range(40):
        bx = -1380 + k * 70 + rng.uniform(-10, 10)
        bw, bh = rng.uniform(34, 58), rng.uniform(30, 70)
        by = y + 110 + rng.uniform(0, 160)
        c.drawRect(R(bx + 10, by + 10, bw, bh), P("#1E222C", 0.5))
        c.drawRect(R(bx, by, bw, bh), P(mix(rng.choice(("#9AA2B0", "#B8BEC8", "#7E8696")), "#3A3F58", dusk)))
        if dusk > 0:
            c.drawRect(R(bx + 6, by + 6, bw - 12, bh - 12), P("#FFD58A", 0.35 * dusk))


def villa_top(c, x, y, s, seed, a=1.0, lit=0.0):
    rng = random.Random(seed)
    col = ROOFS[seed % 4]
    c.drawRect(R(x - 4 * s + 2, y - 4 * s + 2, 8 * s, 8 * s), P("#1E2A30", 0.35 * a))
    c.drawRect(R(x - 4 * s, y - 4 * s, 8 * s, 8 * s), P(col, a))
    if rng.random() < 0.6:
        c.drawRect(R(x + 4 * s, y - 2 * s, 4 * s, 3 * s), P("#38BDF8", 0.9 * a))           # a pool
    c.drawCircle(x - 5 * s, y + 4 * s, 2.6 * s, P("#3F7D3A", a))                      # a tree
    if lit > 0:
        add_glow(c, x, y, 9 * s, "#FFD58A", 0.45 * lit * a)


def palm_island(c, t, grow=1.0, crescent=1.0, villas=0.0, gaps=0.0, dusk=0.0, erode=0.0, flow=0.0, shallow=1.0):
    """The island seen from above (world space).  grow 0..1: the trunk, then the fronds one by one; crescent 0..1 closes
    the ring of rock from both ends to the top; villas 0..1 appear along the fronds; gaps 0..1 opens the two gaps;
    erode 0..1 eats the frond tips (the storm); flow 0..1 shows fresh water moving in through the gaps."""
    tk = clamp(grow / 0.25)                                           # trunk first, from the coast up
    ytop = lerp(900, -360, e_out(tk))
    fr = []
    for n, (b, tip) in enumerate(FRONDS):
        u = clamp((grow - 0.22 - (n // 2) * 0.07) / 0.2)
        if b[1] < ytop - 10 or u <= 0:
            continue
        u = e_out(u) * (1 - 0.28 * erode * (0.6 + 0.4 * ((n * 7) % 5) / 4.0))
        fr.append((b, (lerp(b[0], tip[0], u), lerp(b[1], tip[1], u)), u))
    if crescent > 0:                                                  # the crescent closes from both ends
        a0, a1 = -42.0, 222.0
        k = e_io(clamp(crescent))
        segs = [(a0, lerp(a0, 90, k)), (lerp(a1, 90, k), a1)]
        if gaps > 0:
            g = 3.2 * e_out(clamp(gaps))
            out = []
            for s0, s1 in segs:
                lo, hi = min(s0, s1), max(s0, s1)
                cur = lo
                for gc in sorted(GAPS):
                    if lo < gc - g < hi:
                        out.append((cur, gc - g))
                        cur = gc + g
                out.append((cur, hi))
            segs = out
        for s0, s1 in segs:
            if abs(s1 - s0) > 0.3:
                stroke_path(c, arc_pts(s0, s1, n=max(4, int(abs(s1 - s0) / 3))), SHALLOW, 90, 0.45 * shallow)
    for b, tp, u in fr:                                               # shallow water halo
        stroke_path(c, [b, tp], SHALLOW, 78, 0.42 * shallow)
    if tk > 0:
        stroke_path(c, [(0, 900), (0, ytop)], SHALLOW, 120, 0.42 * shallow)
    for b, tp, u in fr:                                               # beach edge, then the land
        stroke_path(c, [b, tp], BEACH, 34)
        stroke_path(c, [b, tp], mix(SANDC, "#8A8A5A", 0.25), 22)
    if tk > 0:
        stroke_path(c, [(0, 900), (0, ytop)], BEACH, 76)
        stroke_path(c, [(0, 900), (0, ytop)], mix(SANDC, "#7A7A60", 0.2), 62)
        c.drawLine(0, 900, 0, ytop + 20, P("#4A4F5A", stroke=8))      # the road down the trunk
        c.drawLine(-14, 900, -14, max(ytop + 20, 330), P("#9CA3AF", 0.9, stroke=3))   # the monorail
        if tk >= 1:
            rng = random.Random(4)
            for k in range(14):                                           # towers on the trunk
                yy = 860 - k * 40
                if yy < 340:
                    break
                for sd in (-1, 1):
                    w_ = rng.uniform(14, 20)
                    c.drawRect(R(sd * 30 - w_ / 2 + 3, yy + 3, w_, 16), P("#1E2A30", 0.4))
                    c.drawRect(R(sd * 30 - w_ / 2, yy, w_, 16), P(mix("#B8BEC8", "#4A5068", dusk)))
                    if dusk > 0:
                        add_glow(c, sd * 30, yy + 8, 12, "#FFD58A", 0.4 * dusk)
    if villas > 0:                                                    # villas on both sides of every frond
        for n, (b, tp, u) in enumerate(fr):
            dx, dy = tp[0] - b[0], tp[1] - b[1]
            L_ = math.hypot(dx, dy)
            if L_ < 30:
                continue
            ux, uy = dx / L_, dy / L_
            nx, ny = -uy, ux
            m = int(L_ / 26)
            for j in range(1, m):
                q = (j + n * 0.37) / max(1.0, m + n * 0.37)
                vk = clamp((villas * 1.6 - q) * 4)
                if vk <= 0:
                    continue
                px, py = b[0] + ux * j * 26, b[1] + uy * j * 26
                for sd in (-1, 1):
                    villa_top(c, px + nx * sd * 8, py + ny * sd * 8, 1.0 * e_back(vk), n * 31 + j * 3 + (sd > 0), lit=dusk)
    if crescent > 0:                                                  # the crescent: rock outside, a thin strip of land
        for s0, s1 in segs:
            if abs(s1 - s0) <= 0.3:
                continue
            nn = max(4, int(abs(s1 - s0) / 3))
            stroke_path(c, arc_pts(s0, s1, r=RC + 8, n=nn), ROCK_D, 16)
            stroke_path(c, arc_pts(s0, s1, r=RC + 6, n=nn), ROCKC, 10)
            for k in range(int(abs(s1 - s0) / 1.2)):
                an = math.radians(lerp(s0, s1, (k + 0.5) / max(1, int(abs(s1 - s0) / 1.2))))
                rr_ = RC + 11 + (k % 3) * 2
                c.drawCircle(rr_ * math.cos(an), RC_Y - rr_ * math.sin(an), 4.2 + (k * 7 % 3), P(("#9AA1AB", "#6B7280", "#878E99")[k % 3]))
            stroke_path(c, arc_pts(s0, s1, n=nn), BEACH, 18)
            stroke_path(c, arc_pts(s0, s1, r=RC - 2, n=nn), mix(SANDC, "#7A7A60", 0.2), 9)
            for k in range(int(abs(s1 - s0) / 7)):                    # hotels along the crescent
                an = math.radians(lerp(s0, s1, (k + 0.5) / max(1, int(abs(s1 - s0) / 7))))
                hx, hy = (RC - 2) * math.cos(an), RC_Y - (RC - 2) * math.sin(an)
                c.drawRect(R(hx - 5, hy - 5, 10, 10), P(mix("#C9C2B4", "#4A5068", dusk)))
                if dusk > 0:
                    add_glow(c, hx, hy, 10, "#FFD58A", 0.5 * dusk)
        if crescent >= 0.98:                                          # the big hotel at the top of the crescent
            ax, ay = 0, RC_Y - RC
            c.drawRect(R(ax - 34, ay - 16, 68, 24), P("#1E2A30", 0.4))
            c.drawRRect(rr(ax - 36, ay - 20, 72, 24, 6), P(mix("#E8A28A", "#7A4A6A", dusk * 0.6)))
            c.drawRect(R(ax - 9, ay - 20, 18, 24), P(mix("#C9705A", "#4A2A4A", dusk * 0.6)))
            if dusk > 0:
                add_glow(c, ax, ay - 8, 60, "#FFB37A", 0.55 * dusk)
    if flow > 0:                                                      # fresh water moving in through the gaps
        for gc in GAPS:
            an = math.radians(gc)
            ox, oy = (RC + 140) * math.cos(an), RC_Y - (RC + 140) * math.sin(an)
            ix, iy = (RC - 150) * math.cos(an), RC_Y - (RC - 150) * math.sin(an)
            for j in range(4):
                q = (t * 0.6 + j / 4.0) % 1.0
                x_, y_ = lerp(ox, ix, q), lerp(oy, iy, q)
                arrow(c, x_ - (ix - ox) * 0.06, y_ - (iy - oy) * 0.06, x_ + (ix - ox) * 0.06, y_ + (iy - oy) * 0.06,
                      "#7FE7FF", a=flow * math.sin(q * math.pi), w=9, head=22)
    return fr


def dredger_top(c, x, y, ang, s, t, a=1.0):
    """A small dredger seen from above, bow towards ang (degrees, screen)."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    c.drawPath(path_of([(-26, -9), (16, -9), (28, 0), (16, 9), (-26, 9)], close=True), P("#E5E7EB", a))
    c.drawRect(R(-20, -6, 14, 12), P("#F97316", a))
    for k in range(4):
        c.drawLine(-30 - k * 14, -6 - k * 2, -40 - k * 14, -9 - k * 3, P("#E0F7FF", 0.5 * a * (1 - k / 4.0), stroke=3))
        c.drawLine(-30 - k * 14, 6 + k * 2, -40 - k * 14, 9 + k * 3, P("#E0F7FF", 0.5 * a * (1 - k / 4.0), stroke=3))
    c.restore()


def sand_arc(c, x0, y0, x1, y1, h, t, a=1.0, rainbow=0.0, width=16):
    """A jet of sand flying from (x0, y0) to (x1, y1), its top h above the start (screen or world space)."""
    if a <= 0:
        return
    mx_, my_ = (x0 + x1) / 2, min(y0, y1) - h
    p_ = skia.Path()
    p_.moveTo(x0, y0)
    p_.quadTo(mx_, my_, x1, y1)
    c.drawPath(p_, P("#D8B878", 0.55 * a, stroke=width * 1.6))
    c.drawPath(p_, P("#F0D9A6", 0.75 * a, stroke=width * 0.7))
    for k in range(26):                                               # grains flying along it
        q = (t * 0.9 + k / 26.0) % 1.0
        bx = (1 - q) ** 2 * x0 + 2 * (1 - q) * q * mx_ + q * q * x1
        by = (1 - q) ** 2 * y0 + 2 * (1 - q) * q * my_ + q * q * y1
        c.drawCircle(bx + math.sin(k * 3.1) * width * 0.6, by + math.cos(k * 2.3) * width * 0.6, width * 0.22, P("#FFF1C9", 0.8 * a))
    if rainbow > 0:                                                   # the mist catches the sun
        for k, col in enumerate(("#EF4444", "#F59E0B", "#FDE047", "#22C55E", "#3B82F6", "#8B5CF6")):
            q_ = skia.Path()
            off = (k - 2.5) * width * 0.55 - width * 2.2
            q_.moveTo(x0 + width, y0 + off * 0.2)
            q_.quadTo(mx_, my_ + off, x1 - width, y1 + off * 0.2)
            c.drawPath(q_, P(col, 0.42 * rainbow * a, stroke=width * 0.5))


def grains(n_x, n_y, x0, y0, d, seed=2):
    rng = random.Random(seed)
    out = []
    for j in range(n_y):
        for i in range(n_x):
            out.append((x0 + i * d + (j % 2) * d / 2 + rng.uniform(-2, 2), y0 + j * d * 0.87 + rng.uniform(-2, 2),
                        rng.uniform(0.86, 1.08), rng.choice(("#B08A55", "#9C7A48", "#C29A62", "#A88350"))))
    return out


def house_side(c, x, y, s, a=1.0, rot=0.0):
    """A white villa seen from the side, standing on (x, y)."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    contact_shadow(c, 0, 0, 260, 0.5, 20)
    box(c, -120, -150, 240, 150, "#B9B2A6", r=6, a=a)
    box(c, -150, -168, 300, 22, "#8E867A", r=4, a=a)
    for k in range(3):
        c.drawRect(R(-96 + k * 72, -120, 44, 52), P("#3B82F6", 0.55 * a))
    c.drawRect(R(-20, -66, 40, 66), P("#6B4A2A", a))
    c.restore()
    palm_tree(c, x + 190 * s, y, 1.1 * s, 0.0, a=a)


def towel_person(c, x, y, s, t, bite=0.0, grimace=0.0):
    """Close-up for the tag: a person on a beach towel holding a sandwich (screen space), head at (x, y)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-150, 70, 300, 340, 90), P("#2563EB"))                       # shirt
    c.drawRRect(rr(-170, 110, 60, 220, 30), P("#E8B48A"))                     # left arm
    c.drawCircle(0, 0, 92, P("#E8B48A"))                                      # head
    c.drawPath(path_of([(-92, -20), (-80, -80), (-20, -104), (40, -100), (88, -60), (92, -18), (60, -50), (-60, -54)],
                       close=True), P("#2B2530"))
    for sd in (-1, 1):
        if grimace > 0.5:
            c.drawLine(sd * 34 - 14, -12, sd * 34 + 14, -2, P("#1F2937", stroke=7))
            c.drawLine(sd * 34 - 14, 8, sd * 34 + 14, -2, P("#1F2937", stroke=7))
        else:
            c.drawCircle(sd * 34, -6, 9, P("#1F2937"))
    mouth = skia.Path()
    mouth.moveTo(-30, 44)
    mouth.quadTo(0, 44 - 20 * (1 - grimace) + 14 * grimace, 30, 44)
    c.drawPath(mouth, P("#7F1D1D", stroke=7))
    hx, hy = lerp(150, 70, bite), lerp(170, 70, bite)                         # the sandwich in the right hand
    c.drawRRect(rr(hx - 70, hy - 30, 140, 60, 24), P("#E8C27A"))
    c.drawRect(R(hx - 66, hy - 6, 132, 12), P("#4ADE80"))
    c.drawRect(R(hx - 64, hy + 4, 128, 8), P("#EF4444"))
    c.drawCircle(hx + 70, hy + 30, 28, P("#E8B48A"))
    rng = random.Random(5)
    for _ in range(int(40 + 60 * bite)):                                       # sand in it
        c.drawCircle(hx + rng.uniform(-64, 64), hy + rng.uniform(-28, 28), rng.uniform(2, 4.5), P("#B08A55", 0.9))
    c.restore()


# ====================================================================================== the episode
class PalmJumeirah(EpisodeV2):
    BUILD_NO = 52
    FIRST_SET = "top"
    CLEAR = "#0A4E66"
    TITLE = {"en": "PALM JUMEIRAH", "ar_sa": "نخلة جميرا"}
    EMPH = {"en": ["CONGRATS", "GROW", "PALM", "TREE", "SEA", "BIG", "LIVE", "YOURSELF", "JUMEIRAH", "DUBAI", "SHORT",
                   "BEACH", "HOTEL", "SPOT", "SHAPE", "LAND", "TRUNK", "SIXTEEN", "FRONDS", "DESERT", "SAND", "FINE",
                   "WASH", "AWAY", "SHIPS", "SUCK", "FLOOR", "SPRAY", "HUGE", "ARCS", "RAINBOWING", "STORM", "TEAR",
                   "APART", "WRAP", "CRESCENT", "ROCK", "ELEVEN", "KILOMETERS", "BOULDER", "CRANE", "EARTHQUAKE",
                   "LOOSE", "WET", "SOUP", "GIANT", "VIBRATING", "PROBES", "SHAKE", "GRAINS", "TIGHT", "FOLLOW",
                   "REFRIGERATOR", "GAPS", "FRESH", "WATER", "VILLAS", "NINETY-FOUR", "MILLION", "SEVEN", "TONNES",
                   "CONCRETE", "STEEL", "ISLAND", "SANDWICH"],
            "ar_sa": ["مبروك", "نخلة", "البحر", "كبيرة", "تعيش", "جميرا", "دبي", "قصير", "فندق", "مكان", "فترسم", "جذع",
                      "وستاشر", "سعفة", "بلاج", "رمل", "الصحرا", "ناعم", "والموج", "هيشيله", "فالمراكب", "تشفط", "قاع",
                      "وترشّه", "قوس", "قزح", "عاصفة", "هتقطّع", "السعف", "فتلفّها", "بهلال", "صخر", "حداشر", "كيلو",
                      "صخرة", "ونش", "المبلول", "زلزال", "يسيح", "الشوربة", "فتغرز", "مكن", "عملاق", "بيترج", "يرصّ",
                      "الحبايات", "تابعني", "تلاجة", "فتحتين", "الهلال", "تتجدد", "فيلات", "مليون", "طن", "خرسانة",
                      "حديدة", "جزيرة", "ساندوتش", "يقرمش", "بإيدك"]}
    KEYS = {"ar_sa": {
        ("hook", "GROW"): "تطلّع", ("hook", "PALM"): "نخلة", ("hook", "SEA"): "البحر", ("hook", "BIG"): "كبيرة",
        ("hook", "LIVE"): "تعيش", ("hook", "CONGRATS"): "مبروك", ("hook", "JUMEIRAH"): "جميرا",
        ("break1", "DUBAI"): "دبي", ("break1", "SHORT"): "قصير", ("break1", "BEACH"): "شطّها", ("break1", "HOTEL"): "فندق",
        ("break1", "SPOT"): "مكان",
        ("fix1", "SHAPE"): "فترسم", ("fix1", "PALM"): "نخلة", ("fix1", "TRUNK"): "جذع", ("fix1", "SIXTEEN"): "ستاشر",
        ("fix1", "FRONDS"): "سعفة", ("fix1", "BEACH"): "بلاج",
        ("break2", "DESERT"): "الصحرا", ("break2", "GRAINS"): "رمل", ("break2", "FINE"): "ناعم", ("break2", "SEA"): "الموج",
        ("break2", "WASH"): "هيشيله",
        ("fix2", "SHIPS"): "مراكب", ("fix2", "SUCK"): "تشفط", ("fix2", "FLOOR"): "قاع", ("fix2", "SPRAY"): "ترشّه",
        ("fix2", "ARCS"): "قوس", ("fix2", "RAINBOWING"): "قزح",
        ("break3", "STORM"): "عاصفة", ("break3", "TEAR"): "هتقطّع", ("break3", "FRONDS"): "السعف",
        ("fix3", "WRAP"): "تلفّها", ("fix3", "CRESCENT"): "هلال", ("fix3", "ROCK"): "صخر", ("fix3", "ELEVEN"): "حداشر",
        ("fix3", "BOULDER"): "صخرة", ("fix3", "CRANE"): "ونش",
        ("break4", "EARTHQUAKE"): "زلزال", ("break4", "WET"): "المبلول", ("break4", "SOUP"): "الشوربة",
        ("fix4", "PUSH"): "فتغرز", ("fix4", "VIBRATING"): "بيترج", ("fix4", "PROBES"): "مكن", ("fix4", "GRAINS"): "الحبايات",
        ("fix4", "TIGHT"): "يرصّ",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "CUT"): "افتح", ("reveal", "GAPS"): "فتحتين", ("reveal", "CRESCENT"): "الهلال", ("reveal", "FRESH"): "المية",
        ("reveal", "FLOWS"): "تتجدد", ("reveal", "FILL"): "واملا", ("reveal", "VILLAS"): "فيلات",
        ("stat", "NINETY"): "أربعة", ("stat", "SEVEN"): "وسبعة", ("stat", "CONCRETE"): "خرسانة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "BUILT"): "عملوا", ("tag", "STILL"): "وانت", ("tag", "SANDWICH"): "ساندوتش", ("tag", "WITHOUT"): "يقرمش"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a refrigerator"),
                   "stat": [("94M m³", "OF SAND"), ("7M t", "OF ROCK"), ("0", "CONCRETE OR STEEL")],
                   "L": {"grow": "A PALM OUT OF THE SEA", "live": "BIG ENOUGH TO LIVE ON", "name": "THE PALM JUMEIRAH",
                         "short": "A SHORT STRIP OF BEACH", "spot": "EVERY HOTEL WANTS A SPOT", "trunk": "A TRUNK",
                         "fronds": "16 FRONDS", "beach": "BEACH ON EVERY FROND", "desert": "DESERT SAND",
                         "fine": "TOO FINE", "wash": "THE SEA WASHES IT AWAY", "suck": "SAND FROM THE SEA FLOOR",
                         "rainbow": "RAINBOWING", "storm": "ONE BIG STORM", "tear": "FRONDS TORN APART",
                         "crescent": "11 km OF ROCK", "crane": "EVERY BOULDER BY CRANE", "quake": "EARTHQUAKE",
                         "soup": "LOOSE WET SAND = SOUP", "probes": "VIBRATING PROBES", "tight": "GRAINS SHAKEN TIGHT",
                         "gaps": "TWO GAPS", "fresh": "FRESH SEA WATER IN", "villas": "VILLAS ON EVERY FROND",
                         "crunch": "SAND IN EVERY BITE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: تلاجة"),
                      "stat": [("94", "مليون متر مكعب رمل"), ("7", "مليون طن صخر"), ("0", "حديد أو خرسانة")],
                      "L": {"grow": "نخلة من وسط البحر", "live": "الناس تعيش عليها", "name": "نخلة جميرا",
                            "short": "دبي شطها قصير", "spot": "كل فندق عايز مكان", "trunk": "جذع",
                            "fronds": "ستاشر سعفة", "beach": "بلاج حوالين كل سعفة", "desert": "رمل الصحرا",
                            "fine": "ناعم أوي", "wash": "الموج بيشيله", "suck": "رمل من قاع البحر",
                            "rainbow": "قوس قزح", "storm": "عاصفة جامدة", "tear": "السعف بيتقطع",
                            "crescent": "هلال صخر حداشر كيلو", "crane": "كل صخرة بونش", "quake": "زلزال",
                            "soup": "الرمل المبلول بيسيح", "probes": "مكن بيترج", "tight": "الحبايات تترص",
                            "gaps": "فتحتين", "fresh": "المية تتجدد", "villas": "فيلات على السعف",
                            "crunch": "رمل في كل قطمة"}}}
    COVER_T = ("closer", 0.6)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "grow": ("hook", "GROW", 0.12), "palm": ("hook", "PALM", 0.2), "sea": ("hook", "SEA", 0.36),
            "big": ("hook", "BIG", 0.45), "live": ("hook", "LIVE", 0.55), "congrats": ("hook", "CONGRATS", 0.68),
            "jume": ("hook", "JUMEIRAH", 0.9),
            "dubai": ("break1", "DUBAI", 0.08), "short": ("break1", "SHORT", 0.3), "beach": ("break1", "BEACH", 0.45),
            "hotel": ("break1", "HOTEL", 0.65), "spot": ("break1", "SPOT", 0.85),
            "shape": ("fix1", "SHAPE", 0.08), "palm1": ("fix1", "PALM", 0.3), "trunk": ("fix1", "TRUNK", 0.45),
            "sixteen": ("fix1", "SIXTEEN", 0.55), "fronds": ("fix1", "FRONDS", 0.62), "beach1": ("fix1", "BEACH", 0.9),
            "desert": ("break2", "DESERT", 0.1), "grains": ("break2", "GRAINS", 0.4), "fine": ("break2", "FINE", 0.55),
            "sea2": ("break2", "SEA", 0.7), "wash": ("break2", "WASH", 0.85),
            "ships": ("fix2", "SHIPS", 0.06), "suck": ("fix2", "SUCK", 0.12), "floor": ("fix2", "FLOOR", 0.3),
            "spray": ("fix2", "SPRAY", 0.4), "arcs": ("fix2", "ARCS", 0.62), "rainbow": ("fix2", "RAINBOWING", 0.92),
            "storm": ("break3", "STORM", 0.3), "tear": ("break3", "TEAR", 0.55), "fronds3": ("break3", "FRONDS", 0.8),
            "wrap": ("fix3", "WRAP", 0.08), "crescent": ("fix3", "CRESCENT", 0.22), "rock": ("fix3", "ROCK", 0.3),
            "eleven": ("fix3", "ELEVEN", 0.4), "boulder": ("fix3", "BOULDER", 0.7), "crane": ("fix3", "CRANE", 0.9),
            "quake": ("break4", "EARTHQUAKE", 0.2), "wet": ("break4", "WET", 0.6), "soup": ("break4", "SOUP", 0.9),
            "push": ("fix4", "PUSH", 0.08), "vib": ("fix4", "VIBRATING", 0.3), "probes": ("fix4", "PROBES", 0.4),
            "grains4": ("fix4", "GRAINS", 0.8), "tight": ("fix4", "TIGHT", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "cut": ("reveal", "CUT", 0.05), "gaps": ("reveal", "GAPS", 0.12), "cres2": ("reveal", "CRESCENT", 0.3),
            "fresh": ("reveal", "FRESH", 0.45), "flows": ("reveal", "FLOWS", 0.6), "fill": ("reveal", "FILL", 0.75),
            "villas": ("reveal", "VILLAS", 0.92),
            "s1": ("stat", "NINETY", 0.03), "s2": ("stat", "SEVEN", 0.4), "s3": ("stat", "CONCRETE", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_built": ("tag", "BUILT", 0.05), "t_still": ("tag", "STILL", 0.45), "t_sand": ("tag", "SANDWICH", 0.65),
            "t_bite": ("tag", "WITHOUT", 0.85)})
        T["soup1"] = max(T["soup"], T["quake"], T["wet"]) + 0.2
        T["tight1"] = max(T["tight"], T["grains4"], T["vib"]) + 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "coast", 1)
        self.cut(s("fix1") - 0.12, "plan", -1)
        self.cut(s("break2") - 0.12, "sand", 1)
        self.cut(s("break3") - 0.12, "storm", -1)
        self.cut(s("break4") - 0.12, "quake", 1)
        self.cut(s("reveal") - 0.12, "top", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- top camera (hook, reveal, stat, closer)
        cm = Camera(0, 330, 0.8)
        cm.key(0.1, 0, 310, 0.84, max(1.0, T["live"]))
        cm.key(T["congrats"], 0, 300, 0.9, 1.6)
        cm.key(s("reveal") - 0.12, 0, -120, 0.9, 0.0).key(T["fresh"] - 0.2, 0, 120, 0.8, 1.4)
        cm.key(T["fill"] - 0.3, 160, 40, 1.3, 1.4)
        cm.key(s("stat") - 0.12, 0, 60, 0.62, 0.0).key(s("stat"), 0, 70, 0.65, max(0.5, s("closer") - s("stat") - 0.2))
        cm.key(s("closer") - 0.1, 0, 200, 0.76, 1.0).key(s("closer") + 0.9, 0, 205, 0.79, 3.0)
        self.cam = cm
        sc = Camera(0, 250, 0.72)                                     # storm camera
        sc.key(s("break3") - 0.12, 170, -120, 1.05, 0.0).key(T["storm"], 150, -110, 1.12, 1.6)
        sc.key(s("fix3") - 0.12, 0, 170, 0.7, 0.0)
        sc.key(T["boulder"] - 0.4, 386, -386, 2.6, 0.9)
        self.scam = sc
        self.spans = [(T["spot"], T["beach1"] + 0.3), (T["wash"], T["rainbow"] + 0.3), (T["fronds3"], T["crane"] + 0.4),
                      (T["soup1"], T["tight1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["spot"], 0.35, 6), (T["wash"], 0.4, 7), (T["tear"], 0.5, 9),
                       (T["quake"], 1.4, 16), (T["soup"], 0.6, 10), (s("closer") + 0.2, 0.35, 9), (T["t_bite"], 0.3, 7)]

    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    # ------------------------------------------------------------------ set: top (hook, reveal, stat, closer)
    def draw_top(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        dusk = 0.75 * prog(t, s("closer") - 0.6, s("closer") + 0.8)
        hook = t < s("break1")
        if hook:
            grow = clamp(prog(t, 0.1, T["big"] + 0.2) * 1.08)
            cres = prog(t, T["sea"] - 0.3, T["big"] + 0.6)
            vil = prog(t, T["big"] - 0.1, T["live"] + 0.6) * 0.55
            gaps = flow = 0.0
        else:
            grow, cres = 1.0, 1.0
            gaps = prog(t, T["gaps"] - 0.2, T["gaps"] + 0.5)
            flow = prog(t, T["fresh"] - 0.3, T["fresh"]) * (1 - prog(t, s("stat") - 0.4, s("stat")))
            vil = lerp(0.55, 1.0, prog(t, T["fill"] - 0.2, T["villas"] + 0.6))
        self.view(c, cam)
        sea_top(c, t, dusk=dusk)
        coast_top(c, t, dusk=dusk)
        fr = palm_island(c, t, grow=grow, crescent=cres, villas=vil, gaps=gaps, dusk=dusk, flow=flow)
        if hook and grow < 1:                                         # dredgers spraying the growing fronds
            for b, tp, u in fr[-2:]:
                if u < 0.98:
                    sd = 1 if tp[0] >= 0 else -1
                    dx, dy = tp[0] + sd * 120, tp[1] + 40
                    dredger_top(c, dx, dy, 180 if sd > 0 else 0, 1.3, t)
                    sand_arc(c, dx - sd * 30, dy, tp[0], tp[1], 50, t, a=0.9, width=10)
        boat_k = 1 - dusk * 0.5
        for k in range(3):                                            # little boats in the lagoon
            q = (t * 0.03 + k * 0.33) % 1.0
            an = math.radians(lerp(10, 170, q))
            bx, by = 500 * math.cos(an), RC_Y - 500 * math.sin(an)
            dredger_top(c, bx, by, -math.degrees(an) - 90, 0.7, t, a=boat_k * prog(t, 1.0, 2.0))
        c.restore()
        if dusk > 0:                                                  # sunset light from the top of the frame
            c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#FF9D5C", "#FF9D5C", "#3A2A60"], [0.0, 0.25, 1.0], a=0.22 * dusk))
            add_glow(c, 900, 120, 420, "#FFB37A", 0.35 * dusk)
        self.ui["cam"] = cam

    def ui_top(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (0, 300, 0.8))
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "grow", T["grow"] - 0.1, T["big"] - 0.1, accent="#7FE7FF", size=42)
            self.chip(540, 300, "live", T["big"] - 0.1, T["congrats"] - 0.05, accent=HILITE, size=42)
            self.chip(540, 300, "name", T["jume"] - 0.2, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            for gc in GAPS:
                an = math.radians(gc)
                gx, gy = self.at(cam, RC * math.cos(an), RC_Y - RC * math.sin(an))
                self.label(gx, gy, 540 + (gx - 540) * 0.5, 470, "gaps", T["gaps"], T["fresh"] - 0.1, HILITE, size=38)
            self.chip(540, 300, "fresh", T["fresh"] - 0.1, T["fill"] - 0.2, accent="#7FE7FF", size=42)
            self.chip(540, 300, "villas", T["fill"] - 0.2, s("stat") - 0.15, accent=GOOD, size=42)

    # ------------------------------------------------------------------ set: coast (break1), a short beach full of hotels
    def draw_coast(self, c, t):
        T = self.T
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=820)
        sun(c, 860, 600, 52, heat=0.4)
        sea_band(c, -40, W + 40, 820, 260, t)
        c.drawRect(R(0, 1060, W, H - 1060), lin_paint(0, 1060, 0, 1300, [BEACH, SAND_D]))
        c.drawRect(R(0, 1240, W, H - 1240), P("#3A3F4C"))                   # the road behind the beach
        sq = prog(t, T["hotel"] - 0.3, T["spot"] + 0.3)
        n = 7
        xs = [lerp(60, 1020, (k + 0.5) / n) for k in range(n)]
        for k, x in enumerate(xs):                                         # hotels packed along the beach
            push = math.sin(t * 7 + k * 1.3) * 6 * sq
            h = 380 + ((k * 53) % 5) * 60
            w_ = 132 - 26 * sq
            bx = x + push - w_ / 2 + (k - 3) * -6 * sq
            box(c, bx, 1060 - h, w_, h, ("#B8BEC8", "#9AA2B0", "#C9C2B4", "#8E96A8")[k % 4], r=6)
            for j in range(int(h / 46)):
                c.drawRect(R(bx + 14, 1060 - h + 20 + j * 46, w_ - 28, 16), P("#1E3A6E", 0.55))
        if sq > 0:                                                          # one more hotel squeezing in from above
            nx_ = lerp(-200, 540, e_out(prog(t, T["spot"] - 0.5, T["spot"] + 0.2)))
            box(c, nx_ - 50, 1060 - 520 - 400 * (1 - sq), 100, 520, "#E5A07A", r=6)
        rng = random.Random(4)
        for k in range(26):                                                # people packed on the beach
            px = 40 + k * 39 + rng.uniform(-8, 8)
            py = 1120 + (k % 3) * 34
            c.drawCircle(px, py - 16, 9, P("#E8B48A"))
            c.drawRRect(rr(px - 10, py - 8, 20, 22, 8), P(SHIRTS[k % len(SHIRTS)]))
            if k % 4 == 0:
                c.drawPath(path_of([(px - 34, py - 40), (px + 34, py - 40), (px, py - 66)], close=True), P(("#EF4444", "#F59E0B", "#22C55E")[k % 3]))
                c.drawLine(px, py - 40, px, py, P("#E5E7EB", stroke=3))
        bk = prog(t, T["short"] - 0.2, T["short"] + 0.3)                    # the "short" measuring bar
        if bk > 0:
            c.drawLine(80, 1200, lerp(80, 1000, bk), 1200, P(WARN, stroke=8))
            c.drawLine(80, 1180, 80, 1220, P(WARN, stroke=8))
            if bk >= 1:
                c.drawLine(1000, 1180, 1000, 1220, P(WARN, stroke=8))

    def ui_coast(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "short", T["short"] - 0.2, T["hotel"] - 0.2, accent=WARN, size=44)
        self.chip(540, 300, "spot", T["hotel"] - 0.2, s("fix1") - 0.15, accent="#FDBA74", size=42)
        self.badge("alert", T["spot"] + 0.05, s("fix1") - 0.2, x=920, y=420)
        self.red(T["spot"] + 0.05, 1.2)

    # ------------------------------------------------------------------ set: plan (fix1), the blueprint
    def draw_plan(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#0E2A5A", "#0A1E44"])
        for k in range(0, W + 1, 60):
            c.drawLine(k, 0, k, H, P("#5B8BD6", 0.18, stroke=2))
        for k in range(0, H + 1, 60):
            c.drawLine(0, k, W, k, P("#5B8BD6", 0.18, stroke=2))
        cam = (0, 250, 0.82)
        self.view(c, cam)
        tk = prog(t, T["shape"] - 0.2, T["trunk"] + 0.3)
        ytop = lerp(900, -360, e_out(tk))
        if tk > 0:                                                          # the trunk, drawn as an outline
            c.drawRRect(rr(-30, ytop, 60, 900 - ytop, 30), P("#E0F2FE", 0.95, stroke=5))
        nk = prog(t, T["sixteen"] - 0.3, T["fronds"] + 1.0)
        nshow = 16 * nk
        bk = prog(t, T["beach1"] - 0.3, T["beach1"] + 0.6)
        for n, (b, tp) in enumerate(FRONDS):
            u = clamp(nshow - n)
            if u <= 0:
                continue
            ex, ey = lerp(b[0], tp[0], e_out(u)), lerp(b[1], tp[1], e_out(u))
            dx, dy = ex - b[0], ey - b[1]
            L_ = max(1.0, math.hypot(dx, dy))
            nx, ny = -dy / L_ * 13, dx / L_ * 13
            pts = [(b[0] + nx, b[1] + ny), (ex + nx, ey + ny), (ex - nx, ey - ny), (b[0] - nx, b[1] - ny)]
            c.drawPath(path_of(pts, close=True), P("#E0F2FE", 0.95, stroke=4))
            if bk > 0:                                                      # beach lines glow along both edges
                c.drawLine(b[0] + nx * 1.5, b[1] + ny * 1.5, ex + nx * 1.5, ey + ny * 1.5, P(HILITE, bk, stroke=6))
                c.drawLine(b[0] - nx * 1.5, b[1] - ny * 1.5, ex - nx * 1.5, ey - ny * 1.5, P(HILITE, bk, stroke=6))
            if u >= 1:
                text(c, str(n + 1), tp[0] * 1.1, tp[1] * 1.1 + 14, 34, "#FDE68A", "Poppins-Black", a=clamp((nshow - n - 1) * 3 + 1) * (1 - bk * 0.6))
        c.drawPath(path_of(arc_pts(-42, 222)), dash_paint("#93C5FD", 0.4, w=4, t=t))   # where the crescent will go
        c.restore()
        self.ui["nshow"] = nshow

    def ui_plan(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "trunk", T["trunk"] - 0.2, T["sixteen"] - 0.3, accent="#E0F2FE", size=44)
        self.chip(540, 300, "fronds", T["sixteen"] - 0.3, T["beach1"] - 0.2, accent="#FDE68A", size=48)
        self.chip(540, 300, "beach", T["beach1"] - 0.2, s("break2") - 0.15, accent=HILITE, size=42)
        self.badge("check", T["beach1"] + 0.3, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: sand (break2, fix2)
    def draw_sand(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=700)
        sun(c, 900, 420, 58, heat=0.4)
        if not fixed:                                                       # desert sand on the shore, then a wave
            c.drawRect(R(0, 700, W, H - 700), lin_paint(0, 700, 0, H, [TURQ, TURQ_D]))
            wk = prog(t, T["sea2"] - 0.2, T["wash"] + 0.5)
            pile = skia.Path()
            pile.moveTo(120, 1150)
            pile.quadTo(360, 760 + 300 * wk, 640, 1150)
            pile.close()
            c.drawPath(pile, lin_paint(0, 760, 0, 1150, ["#E0A860", "#B07A3A"], a=1 - 0.8 * wk))
            c.drawRect(R(0, 1150, W, H - 1150), lin_paint(0, 1150, 0, H, ["#2A7F95", "#0A3A55"]))
            rng = random.Random(7)
            for k in range(60):                                             # grains carried off by the water
                if wk <= 0:
                    break
                gx = 200 + rng.uniform(0, 420) + wk * rng.uniform(200, 600)
                gy = 900 + rng.uniform(0, 250) + wk * rng.uniform(-100, 300)
                c.drawCircle(gx, gy, 4, P("#F0C78A", 0.8 * (1 - wk * 0.7)))
            wave(c, lerp(1250, 420, e_in(wk)), 960, 300, 200, t, k=1.0, a=prog(t, T["sea2"] - 0.4, T["sea2"]))
            mk = prog(t, T["grains"] - 0.3, T["grains"])                    # the magnifier on the grains
            if mk > 0:
                mx_, my_ = 640, 650
                c.drawCircle(mx_, my_, 210 * mk, P("#3A2A18", 0.9))
                rng2 = random.Random(3)
                for k in range(170):
                    a_ = rng2.uniform(0, 6.28)
                    r_ = 196 * math.sqrt(rng2.random()) * mk
                    jig = math.sin(t * 9 + k) * 3 * wk
                    c.drawCircle(mx_ + math.cos(a_) * r_ + jig, my_ + math.sin(a_) * r_ + wk * 40 * math.sin(k), 9 * mk,
                                 P(rng2.choice(("#E0A860", "#D49A55", "#F0C07A")), 1.0))
                c.drawCircle(mx_, my_, 210 * mk, P("#E5E7EB", stroke=14))
                c.drawLine(mx_ - 150 * mk, my_ + 150 * mk, mx_ - 260 * mk, my_ + 260 * mk, P("#9CA3AF", stroke=26))
            return
        sea_y, bed_y = 760, 1180                                            # fix2: section through the sea
        c.drawRect(R(0, sea_y, W, bed_y - sea_y), lin_paint(0, sea_y, 0, bed_y, [TURQ, TURQ_D], a=0.95))
        c.drawRect(R(0, bed_y, W, H - bed_y), lin_paint(0, bed_y, 0, H, ["#9C7A48", "#4A3520"]))
        tex(c, R(0, bed_y, W, H - bed_y), "sand", 0.9, 0.35)
        gk = prog(t, T["spray"] - 0.2, T["rainbow"] + 0.8)                  # the island rising on the left
        top = lerp(bed_y, sea_y - 60, e_out(gk))
        ip = skia.Path()
        ip.moveTo(-40, bed_y)
        ip.lineTo(-40, top)
        ip.lineTo(140, top)
        ip.quadTo(260, top + 40, 380, bed_y)
        ip.close()
        c.drawPath(ip, lin_paint(0, top, 0, bed_y, [BEACH, SAND_D]))
        sea_band(c, 0, W, sea_y, 30, t, a=0.6)
        shx, shy = 760, sea_y - 10                                          # the dredger on the surface
        sk = prog(t, T["ships"] - 0.2, T["ships"] + 0.3)
        c.save()
        c.translate(lerp(1300, shx, e_out(sk)), shy)
        c.scale(1.25, 1.25)
        hull = path_of([(-240, -40), (230, -40), (200, 40), (-210, 40)], close=True)
        c.drawPath(hull, lin_paint(0, -40, 0, 40, ["#C2410C", "#7C2D12"]))
        box(c, 40, -150, 150, 112, "#E5E7EB", r=8)
        c.drawRect(R(70, -130, 90, 24), P("#1E3A6E", 0.8))
        c.drawRect(R(-200, -70, 200, 32), P("#9CA3AF"))
        c.restore()
        pk = prog(t, T["suck"] - 0.2, T["floor"] + 0.2)                     # the suction pipe down to the sea floor
        px0, py0 = shx + 120, shy + 30
        px1, py1 = lerp(px0, shx + 230, pk), lerp(py0, bed_y - 10, pk)
        if pk > 0:
            c.drawLine(px0, py0, px1, py1, P("#6B7280", stroke=26))
            c.drawLine(px0, py0, px1, py1, P("#9CA3AF", stroke=12))
            c.drawRRect(rr(px1 - 34, py1 - 20, 68, 34, 10), P("#374151"))
            if pk >= 1:
                for k in range(10):                                         # sand going up the pipe
                    q = (t * 1.2 + k / 10.0) % 1.0
                    c.drawCircle(lerp(px1, px0, q), lerp(py1, py0, q), 7, P("#F0D9A6", 0.9))
                v2.puff(c, px1, py1 + 6, 60, "#9C7A48", 0.5, k=1)
        ak = prog(t, T["spray"] - 0.2, T["spray"] + 0.4)                    # the jet: the bow nozzle to the island
        if ak > 0:
            sand_arc(c, shx - 250, shy - 50, lerp(shx - 250, 200, ak), lerp(shy - 50, top - 10, ak), 300 * ak, t,
                     a=1.0, rainbow=prog(t, T["rainbow"] - 0.4, T["rainbow"] + 0.2), width=22)
            v2.puff(c, 200, top - 10, 70 * ak, "#F0D9A6", 0.5 * ak, k=2)

    def ui_sand(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "desert", T["desert"] - 0.2, T["fine"] - 0.2, accent="#FDBA74", size=44)
            self.chip(540, 300, "fine", T["fine"] - 0.2, T["sea2"] - 0.2, accent=WARN, size=46)
            self.chip(540, 300, "wash", T["sea2"] - 0.2, s("fix2") - 0.15, accent="#7FE7FF", size=40)
            self.badge("alert", T["wash"] + 0.05, s("fix2") - 0.2, x=920, y=420)
            self.red(T["wash"] + 0.05, 1.2)
            return
        self.chip(540, 300, "suck", T["suck"] - 0.2, T["arcs"] - 0.2, accent="#F0D9A6", size=42)
        self.chip(540, 300, "rainbow", T["arcs"] - 0.2, s("break3") - 0.15, accent=HILITE, size=50)
        self.badge("check", T["rainbow"] + 0.2, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: storm (break3, fix3), seen from above
    def draw_storm(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        cam = self.scam.at(t)
        st = 1.0 if not fixed else 1 - 0.5 * prog(t, T["eleven"], T["boulder"])
        er = 1.6 * prog(t, T["tear"] - 0.3, T["fronds3"] + 0.5) if not fixed else 0.5
        cr = prog(t, T["wrap"] - 0.2, T["eleven"] + 0.3) if fixed else 0.0
        self.view(c, cam)
        sea_top(c, t, storm=st)
        palm_island(c, t, grow=1.0, crescent=cr, villas=0.0, erode=er)
        if not fixed or cr < 1:                                             # storm waves rolling in from the top right
            for k in range(7):
                q = (t * 0.35 + k / 7.0) % 1.0
                d = lerp(1100, 380, q)
                an0, an1 = math.radians(5), math.radians(85)
                pts = [(d * math.cos(lerp(an0, an1, j / 12.0)), -d * math.sin(lerp(an0, an1, j / 12.0))) for j in range(13)]
                stroke_path(c, pts, "#E0F7FF", 16 + 14 * q, (0.75 * math.sin(q * math.pi)) * st * (1 - cr))
                stroke_path(c, [(x_ * 1.03, y_ * 1.03) for x_, y_ in pts], "#7FB8D0", 30, (0.35 * math.sin(q * math.pi)) * st * (1 - cr))
        if not fixed:
            for b, tp in FRONDS[8:]:                                        # sand plumes torn off the tips
                if tp[0] > 0:
                    v2.puff(c, tp[0] * (1 - 0.28 * er), tp[1] * (1 - 0.28 * er), 50 + 50 * er, "#D8B878", 0.55 * min(1.0, er), k=2)
        else:
            if cr > 0:                                                      # waves now break on the crescent
                for k in range(16):
                    an = math.radians(lerp(-40, 220, (k + 0.5) / 16.0))
                    q = (t * 0.8 + k * 0.3) % 1.0
                    fx_, fy_ = (RC + 30) * math.cos(an), RC_Y - (RC + 30) * math.sin(an)
                    kk = e_io(clamp(cr))
                    deg = math.degrees(an)
                    if deg <= lerp(-42, 90, kk) or deg >= lerp(222, 90, kk):
                        v2.puff(c, fx_, fy_, 30 + 20 * q, "#E0F7FF", 0.5 * (1 - q), k=1)
            bk = prog(t, T["boulder"] - 0.4, T["crane"] + 0.4)              # close-up: a crane barge sets a boulder
            if bk > 0:
                an = math.radians(45)
                bx, by = (RC + 44) * math.cos(an), RC_Y - (RC + 44) * math.sin(an)
                c.save()
                c.translate(bx + 40, by - 30)
                c.rotate(-45)
                c.drawRect(R(-60, -22, 120, 44), P("#4B5563", bk))
                c.drawRect(R(-50, -14, 40, 28), P("#F59E0B", bk))
                c.restore()
                drop = e_in(prog(t, T["crane"] - 0.5, T["crane"] + 0.1))
                rx, ry = lerp(bx + 20, (RC + 8) * math.cos(an), drop), lerp(by - 50, RC_Y - (RC + 8) * math.sin(an), drop)
                c.drawLine(bx + 40, by - 30, rx, ry, P("#1F2937", bk, stroke=2))
                c.drawCircle(rx + 2, ry + 2, 9, P("#1F2937", 0.4 * bk))
                c.drawCircle(rx, ry, 9 * (1.2 - 0.2 * drop), P("#9CA3AF", bk))
        c.restore()
        if not fixed:
            c.drawRect(R(0, 0, W, H), P("#0B1030", 0.12))

    def ui_storm(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "storm", T["storm"] - 0.2, T["tear"] - 0.1, accent="#93C5FD", size=46)
            self.chip(540, 300, "tear", T["tear"] - 0.1, s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["fronds3"] + 0.05, s("fix3") - 0.2, x=920, y=420)
            self.red(T["fronds3"] + 0.05, 1.2)
            return
        self.chip(540, 300, "crescent", T["crescent"] - 0.1, T["boulder"] - 0.3, accent="#CBD5E1", size=46)
        self.chip(540, 300, "crane", T["boulder"] - 0.3, s("break4") - 0.15, accent=HILITE, size=42)
        self.badge("check", T["crane"] + 0.3, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: quake (break4, fix4), section
    def draw_quake(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        vrect(c, 0, 0, W, H, ["#1E3A6E", "#3E6AA8"])
        gy = 860
        if not fixed:
            loose = prog(t, T["quake"], T["soup1"])
            sink = e_io(prog(t, T["wet"] - 0.2, T["soup1"] + 0.4))
            tight = 0.0
        else:
            loose, tight = 0.0, prog(t, T["vib"], T["tight1"])
            sink = 0.0
        dense = lerp(1.0, 0.86, tight)
        top_y = gy + 30 * tight
        c.drawRect(R(0, top_y, W, H - top_y), P("#3A7FA6", 0.9))                # water between the grains
        if not hasattr(self, "_gr"):
            self._gr = grains(19, 21, 10, gy + 40, 60)
        for (x, y, r_, col) in self._gr:
            yy = top_y + (y - gy) * dense
            xx = 540 + (x - 540) * (1.0 if not fixed else lerp(1.0, 0.97, tight))
            jx = math.sin(t * 23 + x * 0.3 + y) * 9 * loose
            jy = math.cos(t * 19 + x + y * 0.2) * 9 * loose + loose * 10 * math.sin(x * 0.05)
            c.drawCircle(xx + jx, yy + jy, 27 * r_ * (1 - 0.25 * loose), P(col))
            c.drawCircle(xx + jx - 7, yy + jy - 8, 8 * r_, P("#E5C690", 0.35))
        if loose > 0:                                                       # the soup: a wavy wet surface
            sp = skia.Path()
            sp.moveTo(0, top_y)
            for k in range(28):
                sp.lineTo(k * 40, top_y + math.sin(t * 6 + k) * 10 * loose)
            sp.lineTo(W, top_y - 40)
            sp.lineTo(0, top_y - 40)
            sp.close()
            c.drawPath(sp, P("#7A5E3A", 0.3 * loose))
        hy = top_y + 150 * sink
        house_side(c, 470, hy, 1.1, rot=-11 * sink)
        if fixed:
            for k, px in enumerate((200, 540, 880)):                        # vibrating probes
                dk = prog(t, T["push"] - 0.2 + k * 0.15, T["probes"] + 0.3 + k * 0.15)
                if dk <= 0:
                    continue
                bot = lerp(top_y - 260, top_y + 720, e_io(dk))
                vib = math.sin(t * 60 + k) * 5 * prog(t, T["vib"] - 0.2, T["vib"])
                c.drawLine(px + vib, top_y - 420, px + vib, bot, P("#4B5563", stroke=40))
                c.drawLine(px + vib, top_y - 420, px + vib, bot, P("#9CA3AF", stroke=22))
                c.drawCircle(px + vib, bot, 22, P("#374151"))
                vk = prog(t, T["vib"] - 0.2, T["vib"]) * (1 - prog(t, T["tight1"], T["tight1"] + 0.6))
                if vk > 0:
                    for j in range(3):
                        q = (t * 2.5 + j / 3.0) % 1.0
                        c.drawCircle(px, bot - 120, 60 + 200 * q, P("#FDE68A", 0.5 * vk * (1 - q), stroke=5))
        self.ui["top_y"] = top_y

    def ui_quake(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "quake", T["quake"] - 0.2, T["wet"] - 0.1, accent=WARN, size=48)
            self.chip(540, 300, "soup", T["wet"] - 0.1, s("fix4") - 0.15, accent="#FDBA74", size=40)
            self.badge("alert", T["soup1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["soup1"], 1.2)
            return
        self.chip(540, 300, "probes", T["push"] - 0.1, T["grains4"] - 0.2, accent="#E5E7EB", size=44)
        self.chip(540, 300, "tight", T["grains4"] - 0.2, s("cta") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["tight1"] + 0.2, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=760)
        sun(c, 860, 520, 56, heat=0.3)
        sea_band(c, -40, W + 40, 760, 260, t)
        c.drawRect(R(0, 1000, W, H - 1000), lin_paint(0, 1000, 0, H, [BEACH, SAND_D]))
        c.drawRect(R(120, 1110, 840, 480), P("#F472B6"))                     # the towel
        for k in range(5):
            c.drawRect(R(120, 1150 + k * 90, 840, 36), P("#FDE68A", 0.8))
        c.drawLine(880, 1180, 980, 520, P("#E5E7EB", stroke=10))             # the umbrella
        c.drawPath(path_of([(700, 560), (1240, 480), (990, 380)], close=True), P("#EF4444"))
        wind = prog(t, T["t_still"] - 0.4, T["t_still"] + 0.2)
        rng = random.Random(6)
        for k in range(50):                                                 # sand blowing in
            q = (t * 0.9 + k / 50.0) % 1.0
            sx_ = lerp(-60, 900, q)
            sy_ = 860 + rng.uniform(0, 300) + math.sin(q * 6 + k) * 20
            c.drawLine(sx_, sy_, sx_ + 26, sy_ - 3, P("#E0C48E", 0.7 * wind, stroke=4))
        bite = e_io(prog(t, T["t_sand"] - 0.3, T["t_bite"]))
        gri = prog(t, T["t_bite"], T["t_bite"] + 0.25)
        towel_person(c, 470, 820, 1.25, t, bite=bite, grimace=gri)
        if gri > 0:
            for k in range(8):
                an = k * 0.785 + 0.3
                q = prog(t, T["t_bite"], T["t_bite"] + 0.5)
                c.drawCircle(560 + math.cos(an) * 130 * q, 880 + math.sin(an) * 100 * q, 7, P("#C29A62", 1 - q))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "crunch", T["t_bite"] - 0.1, self.duration + 1, accent="#FDBA74", size=44)

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, [TURQ_D, TURQ]))

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.5, T["big"]), 61), -18), (T["grow"], sfx.whoosh(0.5, False, 62), -12),
              (T["palm"], sfx.hiss(0.9, 63), -14), (T["sea"], sfx.hiss(0.9, 64), -14), (T["big"], sfx.sparkle(0.7, 9, 65), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 66), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 67), -8),
              (T["jume"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 68), -4), (T["short"], sfx.pop(69), -8),
               (T["hotel"], sfx.thud(0.4, 70), -12), (T["spot"], sfx.thud(0.4, 71), -8), (T["spot"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["trunk"], sfx.tap(73), -10)]
        for k in range(8):
            ev.append((T["sixteen"] - 0.3 + k * 0.16, sfx.tap(74 + k), -14))
        ev += [(T["beach1"], sfx.sparkle(0.7, 10, 82), -10), (T["beach1"] + 0.3, sfx.ding(), -8), (T["beach1"] + 0.5, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 83), -4), (T["grains"], sfx.pop(84), -10),
               (T["sea2"], sfx.hiss(1.2, 85), -8), (T["wash"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 86), -4), (T["ships"], sfx.hum(1.4, 70.0), -14),
               (T["suck"], sfx.whirr(1.2, 120.0, 180.0, 87), -14), (T["spray"], sfx.hiss(1.6, 88), -10),
               (T["rainbow"], sfx.sparkle(0.8, 12, 89), -8), (T["rainbow"] + 0.3, sfx.ding(), -8), (T["rainbow"] + 0.5, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 90), -4), (T["storm"], rumble(1.6, 91), -8),
               (T["tear"], sfx.hiss(1.0, 92), -8), (T["fronds3"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 93), -4)]
        for k in range(6):
            ev.append((T["wrap"] + k * 0.22, sfx.thud(0.3, 94 + k), -14))
        ev += [(T["crane"], sfx.thud(0.5, 100), -6), (T["crane"] + 0.3, sfx.ding(), -8), (T["crane"] + 0.5, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 101), -4), (T["quake"], rumble(2.0, 102), -6),
               (T["soup"], sfx.womp(), -8), (T["soup1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 103), -4), (T["push"], sfx.thunk(104), -8),
               (T["vib"], sfx.buzz(1.2), -14), (T["tight1"], sfx.ding(), -8), (T["tight1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(105), 0), (T["follow"] - 0.15, sfx.pop(106), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 107), -6), (T["gaps"], sfx.snap(108), -8),
               (T["fresh"], sfx.hiss(1.4, 109), -12), (T["villas"], sfx.sparkle(0.8, 12, 110), -8)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 111), -6), (T["s1"], sfx.pop(112), -3), (T["s2"], sfx.pop(113), -3),
               (T["s3"], sfx.pop(114), -3)]
        ev += [(T["cong2"], sfx.pop(115), -2), (T["cong2"], sfx.sparkle(1.0, 14, 116), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 117), -6), (T["t_still"], sfx.hiss(0.9, 118), -12),
               (T["t_bite"], sfx.snap(119), -6), (T["t_bite"] + 0.1, sfx.snap(120), -8)]
        return ev


NAME = "palmjumeirah"
EPISODE = PalmJumeirah
