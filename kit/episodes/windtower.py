"""Episode 37 - A desert wind tower (barjeel / malqaf) that cools a house with no power.  v2 look: a mud house at a hot
desert dusk, cut open, with its wind tower on the roof.

Sets: house (hook: a breeze pulled down the tower keeps the room ten degrees cooler, no AC, no power; the reveal: a whole
old town of wind towers; the stat and the closer), street (break1: still, hot, dusty air in the street; fix1: the tower
rises into the breeze and its open side pushes the wind down into the room), top (break2: a top view, the wind turns
away from the one opening; fix2: four open sides and an X of walls inside, one quarter brings air in, three pull hot air
out), still (break3: no wind at all; fix3: the sun heats the tower and it works like a chimney), water (break4: the
desert wind is hot; fix4: wet cloths in the openings and a pool under the shaft, evaporation cools the air), ac (the tag).
World (house, street, still, water): a side section, the ground is y = 0, the tower stands on the right of the roof.
"""
from v2_base import *  # noqa: F401,F403

DUSK = {"top": "#0E0A24", "upper": "#33163F", "mid": "#7E2B3A", "low": "#C9542F", "horizon": "#FFAA5C",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SAND = ("#B97C42", "#94602F", "#6A411E", "#2E1C0C")
PLASTER = "#E6CFA3"
PLASTER_D = "#B08E62"
WOOD = "#6B3F1D"
COOL = "#7DD3FC"
HOT = "#FB923C"
HX0, HX1, HY = -420.0, 420.0, -520.0          # house body: x range and roof height
TX0, TX1, TY = 120.0, 300.0, -1000.0          # tower: x range and top
OPEN0, OPEN1 = -975.0, -830.0                 # the openings near the top of the tower


# ====================================================================================== pieces
def smooth(pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        p.quadTo(pts[i][0], pts[i][1], mx, my)
    p.lineTo(*pts[-1])
    return p


def flow(c, pts, col, t, k=1.0, w=14, a=1.0, speed=1.0, head=True):
    """Air: moving dashes along a smooth path through pts, drawn up to fraction k, with an arrowhead at the tip."""
    if k <= 0.01 or a <= 0.01:
        return
    path = smooth(pts)
    pm = skia.PathMeasure(path, False)
    L = pm.getLength()
    seg = skia.Path()
    pm.getSegment(0, L * clamp(k), seg, True)
    c.drawPath(seg, P(col, 0.16 * a, stroke=w * 2.8, blur=10))
    pt = P(col, 0.95 * a, stroke=w)
    pt.setPathEffect(skia.DashPathEffect.Make([w * 2.4, w * 1.5], -t * 150 * speed))
    c.drawPath(seg, pt)
    if head:
        pos, tan = pm.getPosTan(L * clamp(k))
        ang = math.atan2(tan.y(), tan.x())
        hp = skia.Path()
        s = w * 2.3
        hp.moveTo(pos.x() + math.cos(ang) * s, pos.y() + math.sin(ang) * s)
        hp.lineTo(pos.x() + math.cos(ang + 2.4) * s, pos.y() + math.sin(ang + 2.4) * s)
        hp.lineTo(pos.x() + math.cos(ang - 2.4) * s, pos.y() + math.sin(ang - 2.4) * s)
        hp.close()
        c.drawPath(hp, P(col, a))


def thermo(c, x, y, s, frac, a=1.0, hot=False):
    """Wall thermometer, bulb at (x, y); frac 0..1 = how high the red goes."""
    if a <= 0:
        return
    c.drawRRect(rr(x - 15 * s, y - 190 * s, 30 * s, 200 * s, 15 * s), P("#F8FAFC", 0.95 * a))
    c.drawRRect(rr(x - 15 * s, y - 190 * s, 30 * s, 200 * s, 15 * s), P("#1F2937", a, stroke=4 * s))
    col = mix("#38BDF8", "#EF4444", clamp(frac * 1.3 - 0.15)) if not hot else "#EF4444"
    h = 160 * s * clamp(frac)
    c.drawRect(R(x - 6 * s, y - 10 * s - h, 12 * s, h + 10 * s), P(col, a))
    c.drawCircle(x, y + 8 * s, 24 * s, P(col, a))
    c.drawCircle(x, y + 8 * s, 24 * s, P("#1F2937", a, stroke=4 * s))
    for k in range(5):
        yy = y - 30 * s - k * 32 * s
        c.drawLine(x + 15 * s, yy, x + 27 * s, yy, P("#1F2937", a, stroke=3 * s))


def readout(c, x, y, deg, size, col, a=1.0):
    if a <= 0:
        return
    s = "%d°" % int(round(deg))
    tw = text_width(s, size, "Poppins-Black")
    c.drawRRect(rr(x - tw / 2 - 18, y - size * 0.95, tw + 36, size * 1.35, 14), P("#0B1220", 0.78 * a))
    text(c, s, x, y, size, col, "Poppins-Black", a=a)


def person_r(c, x, y, h, shirt, t, pose="sit", face=1, a=1.0, hat="none", sweat=0.0):
    person(c, x, y, h, shirt, t, pose=pose, face=face, hat=hat, hair="#1C1917", skin="#C68B5E", pants="#E5E7EB", a=a)
    if sweat > 0:
        for i in range(3):
            q = (t * 1.3 + i * 0.33) % 1.0
            c.drawCircle(x + (i - 1) * 14 * h / 140, y - h * 0.93 + q * h * 0.25, 5 * h / 140, P("#93C5FD", sweat * (1 - q)))


def mashrabiya(c, x, y, w, h, a=1.0):
    c.drawRRect(rr(x, y, w, h, 6), P("#2A160A", a))
    for i in range(1, 6):
        c.drawLine(x + i * w / 6, y, x + i * w / 6, y + h, P("#8B5A2B", a, stroke=4))
    for j in range(1, 8):
        c.drawLine(x, y + j * h / 8, x + w, y + j * h / 8, P("#8B5A2B", a, stroke=4))
    c.drawRRect(rr(x, y, w, h, 6), P("#4A2A12", a, stroke=6))


def tower_body(c, s, t, h=1.0, split=0.0, heat=0.0, cloth=0.0, sil=False, a=1.0):
    """The wind tower in section on the roof at x TX0..TX1 (world units at s = 1). h 0..1 = built height."""
    if h <= 0.01:
        return
    top = lerp(HY, TY, h)
    wall = 22.0
    body = mix(PLASTER, "#F59E0B", heat * 0.45) if not sil else "#2A1A2E"
    c.save()
    c.clipRect(R(TX0 - 400, top - 60, (TX1 - TX0) + 800, HY - top + 80))
    if not sil:
        c.drawRect(R(TX0 + wall, top, TX1 - TX0 - 2 * wall, HY - top + 4), P("#1F130C", a))      # the shaft
        if split > 0:
            mx = (TX0 + TX1) / 2
            c.drawRect(R(mx - 5, lerp(HY, top, 1 - split * 0.0) + 0, 10, (HY - top) * split), P(PLASTER_D, a))
    c.drawRect(R(TX0, top, wall, HY - top), lin_paint(TX0, 0, TX0 + wall, 0, [shade(body, 0.1), body], a=a))
    c.drawRect(R(TX1 - wall, top, wall, HY - top), lin_paint(TX1 - wall, 0, TX1, 0, [body, shade(body, -0.25)], a=a))
    if sil:
        c.drawRect(R(TX0, top, TX1 - TX0, HY - top), P(body, a))
    if h > 0.82 and not sil:                                            # the openings near the top: gaps in the walls
        o0, o1 = max(OPEN0, top + 30), OPEN1
        for xw in (TX0, TX1 - wall):
            c.drawRect(R(xw - 1, o0, wall + 2, o1 - o0), P("#1F130C", a))
        for k in range(4):                                              # wooden poles sticking out (the barjeel's sticks)
            yy = o0 + 20 + k * 40
            c.drawLine(TX0 - 40, yy, TX0 + 10, yy, P(WOOD, a, stroke=7))
            c.drawLine(TX1 - 10, yy, TX1 + 40, yy, P(WOOD, a, stroke=7))
        if cloth > 0:                                                   # wet cloths hung in the openings
            for xw, sd in ((TX0 - 6, -1), (TX1 + 6, 1)):
                ch = (o1 - o0) * cloth
                cp = skia.Path()
                cp.moveTo(xw - 16, o0 + 6)
                cp.lineTo(xw + 16, o0 + 6)
                cp.lineTo(xw + 16 + math.sin(t * 3) * 4, o0 + 6 + ch)
                cp.lineTo(xw - 16 + math.sin(t * 3 + 1) * 4, o0 + 6 + ch)
                cp.close()
                c.drawPath(cp, P("#94A3B8", 0.92 * a))
                c.drawPath(cp, P("#CBD5E1", 0.8 * a, stroke=3))
                for i in range(3):
                    q = (t * 1.7 + i * 0.37) % 1.0
                    c.drawCircle(xw - 8 + i * 8, o0 + 6 + ch + q * 90, 4.5, P("#7DD3FC", 0.9 * a * cloth * (1 - q)))
    if h > 0.9:                                                         # crenellated top
        cap_y = top
        c.drawRect(R(TX0 - 12, cap_y - 16, TX1 - TX0 + 24, 20), P(shade(body, -0.05) if not sil else body, a))
        for k in range(5):
            xx = TX0 - 12 + k * (TX1 - TX0 + 24 - 22) / 4.0
            c.drawRect(R(xx, cap_y - 44, 22, 30), P(body, a))
    c.restore()
    if heat > 0.05 and not sil:
        add_glow(c, TX1 - 10, lerp(HY, top, 0.55), 260, "#F97316", 0.35 * heat * a)


def house(c, t, s=1.0, x=0.0, y=0.0, tower=1.0, split=0.0, heat=0.0, cloth=0.0, hot_room=0.0, people=True, sil=False,
          a=1.0, pool=0.0, cool=0.0):
    """A mud house in section with its wind tower (world units; house centre-bottom at (x, y), scale s)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if sil:                                                              # far town: a silhouette with lit windows
        c.drawRect(R(HX0, HY, HX1 - HX0, -HY), P("#24152C", a))
        c.drawRect(R(HX0 - 10, HY - 14, HX1 - HX0 + 20, 18), P("#2E1B35", a))
        rng = random.Random(int(x * 7 + y))
        for i in range(4):
            wx = HX0 + 70 + i * 180 + rng.uniform(-20, 20)
            add_glow(c, wx + 26, HY + 220, 60, "#FFB766", 0.5 * a)
            c.drawRRect(rr(wx, HY + 180, 52, 80, 10), P("#FFC77D", 0.85 * a))
        tower_body(c, 1.0, t, h=tower, sil=True, a=a)
        c.restore()
        return
    contact_shadow(c, 0, 0, (HX1 - HX0) * 1.1, 0.5 * a, 40)
    c.drawRect(R(HX0, HY, HX1 - HX0, -HY), P(PLASTER, a))               # the cut: outer walls and roof slab
    room_l, room_r, room_t = HX0 + 34, HX1 - 34, HY + 34
    wallc = mix("#7A4A2A", "#3B5B7A", cool * 0.55)
    wallc = mix(wallc, "#9A2B1F", hot_room * 0.6)
    vrect(c, room_l, room_t, room_r - room_l, -room_t, [shade(wallc, 0.12), wallc, shade(wallc, -0.25)], a=a)
    for k in range(1, 9):                                               # mud-brick courses on the back wall
        c.drawLine(room_l, room_t + k * 52, room_r, room_t + k * 52, P("#000000", 0.07 * a, stroke=2))
    c.drawRect(R(-120, -330, 120, 160), P("#000000", 0.18 * a))          # a niche
    c.drawRRect(rr(-104, -312, 88, 124, 40), P("#3A2414", 0.8 * a))
    mashrabiya(c, room_l + 30, -390, 120, 170, a=a)
    c.drawRect(R(room_l, -40, room_r - room_l, 40), P("#5B2A1A", a))     # the rug
    for k in range(9):
        c.drawLine(room_l + 20 + k * 80, -40, room_l + 60 + k * 80, 0, P("#E0A458", 0.35 * a, stroke=4))
    if pool > 0:                                                         # a pool of water under the shaft
        px0, px1 = TX0 - 30, TX1 + 30
        c.drawRRect(rr(px0, -58, px1 - px0, 40, 16), P("#1E3A8A", a * pool))
        c.drawRRect(rr(px0 + 8, -54, px1 - px0 - 16, 24, 12), P("#3B82F6", a * pool))
        for i in range(3):
            q = (t * 0.8 + i / 3.0) % 1.0
            c.drawOval(R(lerp(px0, px1, 0.5) - 40 - q * 60, -46 - q * 6, 80 + q * 120, 14 + q * 8),
                       P("#BFDBFE", a * pool * (1 - q) * 0.8, stroke=3))
    if hot_room > 0.02:
        c.drawRect(R(room_l, room_t, room_r - room_l, -room_t), P("#EF4444", 0.22 * hot_room * a))
    if cool > 0.02:
        c.drawRect(R(room_l, room_t, room_r - room_l, -room_t), P("#38BDF8", 0.10 * cool * a))
    if people:
        sw = hot_room
        person_r(c, -250, -40, 185, "#F5F5F4", t, pose="sit", face=1, a=a, sweat=sw)
        person_r(c, -40, -40, 140, "#FCA5A5", t + 0.4, pose="sit", face=1, a=a, sweat=sw)
        person_r(c, 330, -40, 185, "#E7E5E4", t + 0.8, pose="sit", face=-1, a=a, sweat=sw)
        if cool > 0.3:                                                   # a little tea glass, all is well
            c.drawRRect(rr(100, -78, 26, 38, 5), P("#FDE68A", 0.9 * a * cool))
    c.drawRect(R(HX0, HY, 34, -HY), lin_paint(HX0, 0, HX0 + 34, 0, [PLASTER, PLASTER_D], a=a))   # cut walls
    c.drawRect(R(HX1 - 34, HY, 34, -HY), lin_paint(HX1 - 34, 0, HX1, 0, [PLASTER_D, shade(PLASTER_D, -0.2)], a=a))
    c.drawRect(R(HX0, HY, HX1 - HX0, 34), P(PLASTER, a))
    c.drawRect(R(HX0 - 14, HY - 18, HX1 - HX0 + 28, 22), P(shade(PLASTER, 0.08), a))  # parapet
    for k in range(9):
        c.drawRect(R(HX0 - 14 + k * (HX1 - HX0 + 28 - 24) / 8.0, HY - 40, 24, 24), P(PLASTER, a))
    if tower > 0.01:                                                     # the shaft opens into the ceiling
        c.drawRect(R(TX0 + 22, HY - 2, TX1 - TX0 - 44, 38), P("#1F130C", a))
    tower_body(c, 1.0, t, h=tower, split=split, heat=heat, cloth=cloth, a=a)
    c.restore()


def sun(c, x, y, r, heat=1.0, a=1.0):
    add_glow(c, x, y, r * 5, "#FF8A3D", 0.45 * heat * a)
    add_glow(c, x, y, r * 2.2, "#FFD08A", 0.6 * a)
    c.drawCircle(x, y, r, P("#FFF1C9", a))


def heat_lines(c, x0, x1, y0, y1, t, a=1.0):
    if a <= 0:
        return
    for i in range(7):
        xx = lerp(x0, x1, (i + 0.5) / 7)
        p = skia.Path()
        p.moveTo(xx, y1)
        for k in range(1, 9):
            yy = lerp(y1, y0, k / 8.0)
            p.lineTo(xx + math.sin(t * 5 + k * 1.3 + i) * 16, yy)
        q = (t * 0.6 + i * 0.13) % 1.0
        c.drawPath(p, P("#FDBA74", a * 0.85 * math.sin(q * math.pi), stroke=8))


def dust(c, x0, x1, y0, y1, t, a=1.0, seed=3):
    if a <= 0:
        return
    rng = random.Random(seed)
    for i in range(46):
        bx, by = rng.uniform(x0, x1), rng.uniform(y0, y1)
        dx = math.sin(t * 0.7 + i) * 14
        c.drawCircle(bx + dx, by + math.cos(t * 0.9 + i) * 8, rng.uniform(5, 11), P("#F3D3A0", a * rng.uniform(0.5, 0.95)))


def wind_lines(c, x0, x1, y0, y1, t, a=1.0, col="#E0F2FE", n=6, speed=600.0):
    """Breeze high above the roofs: streaks running left to right."""
    if a <= 0:
        return
    rng = random.Random(11)
    for i in range(n):
        yy = lerp(y0, y1, (i + 0.5) / n) + math.sin(t + i) * 10
        L = rng.uniform(160, 300)
        xx = x0 + ((t * speed + rng.uniform(0, 3000)) % (x1 - x0 + 600)) - 300
        c.drawLine(xx, yy, xx + L, yy, P(col, a * 0.6, stroke=7))


def plug_off(c, x, y, s, a=1.0):
    """A power plug with a red cross: no power."""
    if a <= 0:
        return
    c.drawRRect(rr(x - 34 * s, y - 30 * s, 68 * s, 60 * s, 14 * s), P("#E5E7EB", a))
    c.drawRect(R(x - 18 * s, y - 56 * s, 9 * s, 28 * s), P("#9CA3AF", a))
    c.drawRect(R(x + 9 * s, y - 56 * s, 9 * s, 28 * s), P("#9CA3AF", a))
    c.drawLine(x, y + 30 * s, x, y + 70 * s, P("#E5E7EB", a, stroke=10 * s))
    c.drawCircle(x, y, 74 * s, P(WARN, a, stroke=10 * s))
    c.drawLine(x - 52 * s, y + 52 * s, x + 52 * s, y - 52 * s, P(WARN, a, stroke=10 * s))


def ac_unit(c, x, y, w, h, t, dead=0.0, a=1.0):
    c.drawRRect(rr(x, y, w, h, 18), P("#F1F5F9", a))
    c.drawRRect(rr(x, y, w, h, 18), P("#94A3B8", a, stroke=4))
    for k in range(4):
        c.drawLine(x + 30, y + h - 46 + k * 10, x + w - 30, y + h - 46 + k * 10, P("#64748B", a, stroke=3))
    col = mix("#22C55E", "#EF4444", dead)
    c.drawCircle(x + w - 40, y + 34, 9, P(col, a))
    if dead > 0.3:
        smoke = [(x + w * 0.5 + math.sin(t * 2 + i) * 20, y - 20 - ((t * 60 + i * 40) % 160)) for i in range(5)]
        for i, (sx, sy) in enumerate(smoke):
            c.drawCircle(sx, sy, 26 + i * 4, P("#6B7280", 0.35 * a * dead))


# ====================================================================================== the episode
class WindTower(EpisodeV2):
    BUILD_NO = 37
    FIRST_SET = "house"
    CLEAR = "#140C24"
    TITLE = {"en": "WIND TOWER", "ar_sa": "برج الهوا"}
    EMPH = {"en": ["CONGRATS", "DESERT", "TEN", "DEGREES", "COOLER", "AC", "WATT", "POWER", "WIND", "TOWER", "STREET",
                   "STILL", "HOT", "DUSTY", "TALL", "BREEZE", "OPEN", "CATCHES", "DOWN", "ROOM", "CHANGING",
                   "DIRECTION", "FOUR", "SIDES", "SPLIT", "SHAFT", "IN", "OUT", "NO", "SUN", "HEATS", "RISES", "CHIMNEY",
                   "DRAGS", "WET", "CLOTHS", "WATER", "EVAPORATES", "COOLS", "FOLLOW", "PETRA", "CLIFF", "EVERY", "DUBAI",
                   "YAZD", "SEVEN", "HUNDRED", "FIVE", "METERS", "EGYPTIAN", "THREE", "THOUSAND", "YOURSELF", "FREE",
                   "BREAKS", "HOTTEST", "REPAIR", "WEEK"],
            "ar_sa": ["مبروك", "الصحرا", "أبرد", "عشر", "درجات", "تكييف", "كهربا", "برج", "هوا", "الشارع", "واقف",
                      "وسخن", "تراب", "فتعلي", "النسمة", "تلقف", "وتنزله", "الأوضة", "يغير", "اتجاهه", "الأربع", "جهات",
                      "وتقسمه", "تدخل", "يشفط", "الحر", "نسمة", "فالشمس", "تسخن", "يطلع", "المدخنة", "ويسحب", "قماش",
                      "مبلول", "مية", "بتتبخر", "تبرده", "تابعني", "البترا", "محفورة", "كل", "القاهرة", "الملقف", "خمسة",
                      "السطح", "المصريين", "تلات", "تلاف", "بإيدك", "ببلاش", "فصل", "الفني", "الفريون", "خلص"]}
    KEYS = {"ar_sa": {
        ("hook", "DESERT"): "الصحرا", ("hook", "COOLER"): "أبرد", ("hook", "AC"): "تكييف", ("hook", "WATT"): "كهربا",
        ("hook", "CONGRATS"): "مبروك", ("hook", "TOWER"): "برج",
        ("break1", "STREET"): "الشارع", ("break1", "STILL"): "واقف", ("break1", "HOT"): "وسخن", ("break1", "DUSTY"): "تراب",
        ("fix1", "RAISE"): "فتعلي", ("fix1", "BREEZE"): "النسمة", ("fix1", "CATCHES"): "تلقف", ("fix1", "DOWN"): "وتنزله",
        ("fix1", "ROOM"): "الأوضة",
        ("break2", "CHANGING"): "يغير", ("break2", "DIRECTION"): "اتجاهه",
        ("fix2", "FOUR"): "الأربع", ("fix2", "SPLIT"): "وتقسمه", ("fix2", "BRINGS"): "تدخل", ("fix2", "PULL"): "يشفط",
        ("break3", "WIND"): "نسمة",
        ("fix3", "SUN"): "فالشمس", ("fix3", "HEATS"): "تسخن", ("fix3", "RISES"): "يطلع", ("fix3", "CHIMNEY"): "المدخنة",
        ("fix3", "DRAGS"): "ويسحب",
        ("break4", "HOT"): "سخن",
        ("fix4", "CLOTHS"): "قماش", ("fix4", "WATER"): "مية", ("fix4", "EVAPORATES"): "بتتبخر", ("fix4", "COOLS"): "تبرده",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "EVERY"): "كل", ("reveal", "DUBAI"): "القاهرة", ("reveal", "SEVEN"): "الملقف",
        ("stat", "FIVE"): "خمسة", ("stat", "TEN"): "عشر", ("stat", "EGYPTIAN"): "المصريين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "FREE"): "ببلاش", ("tag", "BREAKS"): "فصل", ("tag", "REPAIR"): "الفني", ("tag", "WEEK"): "الفريون"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Petra"),
                   "stat": [("5 m", "ABOVE THE ROOF"), ("-10°", "INSIDE, NO POWER"), ("3,000+", "YEARS OLD")],
                   "L": {"cool": "10° COOLER INSIDE", "nopower": "NO AC, NO POWER", "wt": "THE WIND TOWER",
                         "still": "STILL AIR", "hot": "HOT AND DUSTY", "tall": "UP INTO THE BREEZE",
                         "catch": "OPEN SIDE CATCHES IT", "down": "PUSHED DOWN INTO THE ROOM", "turns": "THE WIND TURNS",
                         "wrong": "WRONG SIDE: NOTHING", "four": "4 SIDES OPEN", "x": "WALLS SPLIT THE SHAFT",
                         "in": "AIR IN", "out": "HOT AIR OUT", "nowind": "NO WIND", "sun": "SUN HEATS THE TOWER",
                         "chim": "RISES LIKE A CHIMNEY", "drag": "PULLS THE HOT AIR OUT", "hotw": "HOT DESERT WIND",
                         "cloth": "WET CLOTHS", "water": "WATER BELOW", "evap": "EVAPORATION COOLS IT",
                         "town": "A TOWER ON EVERY HOUSE", "dubai": "OLD DUBAI", "yazd": "YAZD: ABOUT 700",
                         "outside": "OUTSIDE", "inside": "INSIDE", "free": "3,000 YEARS OF FREE COOLING",
                         "msg": "REPAIR GUY: NEXT WEEK", "topview": "THE TOWER FROM ABOVE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: البترا"),
                      "stat": [("5", "متر فوق السطح"), ("-10°", "جوة، من غير كهربا"), ("3,000+", "سنة")],
                      "L": {"cool": "أبرد عشر درجات", "nopower": "من غير تكييف ولا كهربا", "wt": "برج الهوا",
                            "still": "الهوا واقف", "hot": "سخن ومليان تراب", "tall": "لفوق لحد النسمة",
                            "catch": "الفتحة تلقف الهوا", "down": "وتنزله جوة الأوضة", "turns": "الهوا غير اتجاهه",
                            "wrong": "الفتحة في الجهة الغلط", "four": "مفتوح من الأربع جهات", "x": "مقسوم من جوة",
                            "in": "هوا داخل", "out": "حر طالع", "nowind": "مفيش ولا نسمة", "sun": "الشمس بتسخن البرج",
                            "chim": "يطلع زي المدخنة", "drag": "ويسحب حر الأوضة", "hotw": "هوا الصحرا سخن",
                            "cloth": "قماش مبلول", "water": "مية تحت", "evap": "المية بتتبخر وتبرده",
                            "town": "برج على كل بيت", "dubai": "القاهرة زمان", "yazd": "الملقف",
                            "outside": "برة", "inside": "جوة", "free": "تبريد ببلاش من تلات تلاف سنة",
                            "msg": "الفني: الفريون خلص", "topview": "البرج من فوق"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "desert": ("hook", "DESERT", 0.12), "cooler": ("hook", "COOLER", 0.3), "noac": ("hook", "AC", 0.45),
            "watt": ("hook", "WATT", 0.6), "congrats": ("hook", "CONGRATS", 0.75), "tower": ("hook", "TOWER", 0.92),
            "street": ("break1", "STREET", 0.2), "still": ("break1", "STILL", 0.45), "hot": ("break1", "HOT", 0.65),
            "dusty": ("break1", "DUSTY", 0.85),
            "raise": ("fix1", "RAISE", 0.08), "breeze": ("fix1", "BREEZE", 0.3), "catches": ("fix1", "CATCHES", 0.55),
            "down": ("fix1", "DOWN", 0.75), "room": ("fix1", "ROOM", 0.9),
            "changing": ("break2", "CHANGING", 0.5), "direction": ("break2", "DIRECTION", 0.8),
            "four": ("fix2", "FOUR", 0.15), "split": ("fix2", "SPLIT", 0.35), "brings": ("fix2", "BRINGS", 0.65),
            "pull": ("fix2", "PULL", 0.85),
            "nowind": ("break3", "WIND", 0.7),
            "sun": ("fix3", "SUN", 0.06), "heats": ("fix3", "HEATS", 0.15), "rises": ("fix3", "RISES", 0.45),
            "chimney": ("fix3", "CHIMNEY", 0.6), "drags": ("fix3", "DRAGS", 0.8),
            "hotw": ("break4", "HOT", 0.7),
            "cloths": ("fix4", "CLOTHS", 0.2), "water": ("fix4", "WATER", 0.5), "evap": ("fix4", "EVAPORATES", 0.75),
            "cools": ("fix4", "COOLS", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "every": ("reveal", "EVERY", 0.2), "dubai": ("reveal", "DUBAI", 0.45), "yazd": ("reveal", "SEVEN", 0.75),
            "s1": ("stat", "FIVE", 0.04), "s2": ("stat", "TEN", 0.35), "s3": ("stat", "EGYPTIAN", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "free": ("tag", "FREE", 0.25), "breaks": ("tag", "BREAKS", 0.5), "repair": ("tag", "REPAIR", 0.75),
            "week": ("tag", "WEEK", 0.9)})
        T["grow"] = max(min(T["raise"], T["breeze"]) - 0.1, s("fix1") + 0.05)
        T["grown"] = T["grow"] + 1.1
        T["inflow"] = max(T["catches"] - 0.2, T["grown"] - 0.2)
        T["turn"] = max(T["changing"] - 0.3, s("break2") + 0.1)
        T["xw"] = max(T["split"] - 0.15, T["four"] + 0.3)
        T["burn"] = max(T["heats"] - 0.1, s("fix3") + 0.05)
        T["rise2"] = max(T["rises"] - 0.15, T["burn"] + 0.5)
        T["wet"] = max(T["cloths"] - 0.15, s("fix4") + 0.05)
        T["town_in"] = max(T["every"] - 0.2, s("reveal") + 0.05)
        T["msg"] = max(T["repair"] - 0.1, T["breaks"] + 0.4)
        # ---- sets
        self.cut(s("break1") - 0.12, "street", 1)
        self.cut(s("break2") - 0.12, "top", -1)
        self.cut(s("break3") - 0.12, "still", 1)
        self.cut(s("break4") - 0.12, "water", -1)
        self.cut(s("reveal") - 0.12, "house", 1)
        self.cut(s("tag") - 0.2, "ac", 1)
        # ---- cameras
        z0 = 0.95
        ch = Camera(-40, -270 / z0 - 20, z0)
        ch.key(0.05, -20, -270 / z0 - 15, z0 * 1.02, 2.0)
        ch.key(s("reveal") - 0.12, 0, -270 / 0.62 - 40, 0.62, 0.0)
        ch.key(T["town_in"], 0, -270 / 0.48 - 60, 0.48, 2.2)
        ch.key(s("stat") - 0.12, 0, -270 / 0.55 - 120, 0.55, 0.0)
        ch.key(s("closer") - 0.1, 0, -230 / 0.74, 0.74, 1.0)
        self.camh = ch
        cs = Camera(-300, -270 / 1.0, 1.0)
        cs.key(T["grow"] - 0.2, -30, -270 / z0 - 20, z0, 1.4)
        self.cams = cs
        cw = Camera(-20, -300, z0)
        cw.key(T["burn"], 20, -310, z0, 1.2)
        self.camw = cw
        cq = Camera(200, -880, 1.55)
        cq.key(T["water"] - 0.3, 0, -300, z0, 1.4)
        self.camq = cq
        self.tower_h = Track(0.0).to(T["grow"], 1.0, 1.1, e_out)
        self.wind_ang = Track(90.0).to(T["turn"], 0.0, 1.6).to(s("fix2") + 0.3, 45.0, 0.01).to(T["brings"], -60.0, 3.5)
        self.room_temp = Track(35.0)
        self.room_temp.to(s("break1") - 0.12, 45.0, 0.0).to(T["inflow"] + 0.3, 35.0, 2.2)
        self.spans = [(T["dusty"], T["room"] + 0.3), (T["direction"], T["pull"] + 0.3), (T["nowind"], T["drags"] + 0.3),
                      (T["hotw"], T["cools"] + 0.3)]
        self.shakes = [(T["tower"], 0.3, 6), (T["congrats"], 0.3, 8), (T["grown"] - 0.1, 0.35, 8),
                       (T["direction"], 0.25, 5), (T["xw"] + 0.2, 0.25, 5), (T["msg"] - 0.3, 0.3, 8),
                       (s("closer") + 0.2, 0.35, 10)]

    # ------------------------------------------------------------------ world helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def desert(self, c, t, cam, sun_xy=(965, 560), heat=1.0):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 30 * z)
        v2.stars(c, W, H, t, 0.35)
        sun(c, sun_xy[0] - cx * 0.04, sun_xy[1], 70, heat)
        self.view(c, cam)
        rng = random.Random(4)
        for i in range(9):
            dx = -2200 + i * 520 + rng.uniform(-80, 80)
            hh = rng.uniform(80, 170)
            c.drawOval(R(dx - 420, -hh * 0.5 - 20, 840, hh), P("#8A4A2E", 0.9))
        vrect(c, cx - 1400 / z, -20, 2800 / z, 3000, [SAND[0], SAND[1], SAND[2], SAND[3]], [0, 0.06, 0.3, 1])
        return gy

    # air paths in the world (the tower on the right of the roof)
    IN_PATH = [(-1200, -900), (-500, -900), (60, -900), (170, -875), (190, -700), (190, -560), (150, -420), (20, -230),
               (-140, -90), (-330, -70)]
    OUT_PATH = [(-300, -420), (-80, -470), (240, -520), (252, -680), (258, -820), (300, -905), (480, -925), (1100, -975)]
    STACK_OUT = [(-300, -380), (-60, -440), (230, -520), (240, -700), (240, -900), (252, -1030), (300, -1110)]
    LOW_IN = [(-900, -120), (-560, -120), (-400, -140), (-200, -110), (40, -120), (180, -300), (210, -460)]

    def scene(self, c, t, cam, tower=1.0, split=0.0, wind=0.0, in_k=0.0, out_k=0.0, in_col=COOL, hot_room=0.0,
              heat=0.0, cloth=0.0, pool=0.0, cool=0.0, town=0.0, stack=0.0, low_in=0.0, sun_heat=1.0, street=0.0):
        self.desert(c, t, cam, heat=sun_heat)
        if town > 0:                                                    # an old town full of wind towers
            rng = random.Random(8)
            for i in range(16):
                xx = -2400 + i * 320 + rng.uniform(-50, 50)
                if abs(xx) < 480:
                    continue
                yy = -rng.uniform(10, 60)
                sc = rng.uniform(0.5, 0.78)
                k = clamp(town * 1.6 - abs(xx) / 2600.0)
                c.save()
                c.translate(0, (1 - e_out(k)) * 600)
                house(c, t, s=sc, x=xx, y=yy, tower=1.0, sil=True, a=k)
                c.restore()
        heat_lines(c, -1200, HX0 - 40, -380, -30, t, a=street)
        dust(c, -1300, HX0 - 40, -420, -20, t, a=street)
        wind_lines(c, -1500, 1500, -1090, -820, t, a=wind)
        house(c, t, tower=tower, split=split, heat=heat, cloth=cloth, hot_room=hot_room, pool=pool, cool=cool)
        flow(c, self.IN_PATH, in_col, t, k=in_k, w=15)
        flow(c, self.OUT_PATH, HOT, t, k=out_k, w=13)
        flow(c, self.STACK_OUT, HOT, t, k=stack, w=13)
        flow(c, self.LOW_IN, COOL, t, k=low_in, w=12)
        c.drawRect(R(-496, -130, 12, 130), P(WOOD))                     # outside, on a post in the sun
        thermo(c, -490, -150, 0.9, 0.95, hot=True)
        thermo(c, -190, -240, 0.75, (self.room_temp.at(t) - 20) / 26.0)  # inside, on the back wall
        c.restore()

    # ------------------------------------------------------------------ set: house (hook, reveal, stat, closer)
    def draw_house(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.camh.at(t)
        hook = t < s("break1")
        town = prog(t, T["town_in"], T["town_in"] + 1.6) if t >= s("reveal") - 0.12 else 0.0
        kin = 1.0 if not hook else prog(t, 0.05, 1.4)
        kout = 1.0 if not hook else prog(t, 0.6, 1.9)
        self.scene(c, t, cam, tower=1.0, split=1.0, wind=1.0, in_k=kin, out_k=kout, cool=1.0, town=town)
        if hook:
            plug_off(c, 300, 660, 0.85, a=self.span(T["noac"] - 0.15, T["congrats"]))
        self.ui["cam"] = cam

    def ui_house(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.camh.at(tw))
        if tw < s("break1"):
            ox, oy = self.at(cam, -490, -330)
            ix, iy = self.at(cam, -190, -400)
            readout(c, ox, oy - 8, 45, 40, "#FCA5A5", a=self.span(0.1, s("break1") + 0.1))
            readout(c, ix, iy - 8, 35, 40, "#BAE6FD", a=self.span(0.3, s("break1") + 0.1))
            self.chip(300, 480, "cool", T["cooler"] - 0.15, T["noac"] - 0.1, accent=COOL, size=40)
            self.chip(300, 480, "nopower", T["noac"] - 0.1, T["tower"] - 0.1, accent=WARN, size=36)
            self.chip(300, 480, "wt", T["tower"] - 0.1, s("break1") + 0.1, accent=HILITE, size=44)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            self.chip(540, 560, "town", T["every"] - 0.1, T["dubai"] - 0.1, accent=HILITE, size=40)
            self.chip(540, 560, "dubai", T["dubai"] - 0.1, T["yazd"] - 0.1, accent="#FDBA74", size=40)
            self.chip(540, 560, "yazd", T["yazd"] - 0.1, s("stat") - 0.15, accent=COOL, size=40)

    # ------------------------------------------------------------------ set: street (break1, fix1)
    def draw_street(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams.at(t)
        fixed = t >= s("fix1") - 0.12
        h = self.tower_h.at(t) if fixed else 0.0
        kin = prog(t, T["inflow"], T["inflow"] + 1.6) if fixed else 0.0
        hot = 1.0 - (prog(t, T["inflow"] + 0.6, T["inflow"] + 2.2) if fixed else 0.0)
        self.scene(c, t, cam, tower=h, wind=prog(t, T["grow"] + 0.3, T["grow"] + 0.9) if fixed else 0.0, in_k=kin,
                   hot_room=hot, street=1.0 if not fixed else 1.0 - prog(t, T["grow"], T["grow"] + 0.8),
                   cool=1 - hot, sun_heat=1.0)
        self.ui["cam"] = cam

    def ui_street(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cams.at(tw))
        if tw < s("fix1") - 0.12:
            sx, sy = self.at(cam, -700, -200)
            self.label(sx, sy, 330, 470, "still", T["still"] - 0.15, T["hot"] - 0.1, "#FDBA74", size=38)
            self.chip(330, 600, "hot", T["hot"] - 0.1, s("fix1") - 0.15, accent=WARN, size=38)
            ix, iy = self.at(cam, -190, -400)
            readout(c, ix, iy - 8, self.room_temp.at(tw), 40, "#FCA5A5", a=self.span(T["street"], s("fix1") - 0.1))
            self.badge("alert", T["dusty"] + 0.05, s("fix1") - 0.2, x=880, y=330)
            self.red(T["dusty"] + 0.05, 1.4)
            return
        tx, ty = self.at(cam, TX0, -900)
        self.label(tx, ty, 300, 520, "tall", T["breeze"] - 0.2, T["catches"] - 0.1, "#E0F2FE", size=34)
        self.label(tx, ty, 300, 520, "catch", T["catches"] - 0.1, T["down"] - 0.1, COOL, size=34)
        dx, dy = self.at(cam, 150, -420)
        self.label(dx, dy, 330, 600, "down", T["down"] - 0.1, s("break2") - 0.15, COOL, size=32)
        ix, iy = self.at(cam, -190, -400)
        readout(c, ix, iy - 8, self.room_temp.at(tw), 40, mix("#FCA5A5", "#BAE6FD", prog(tw, T["inflow"], T["inflow"] + 2)),
                a=self.span(s("fix1"), s("break2") - 0.1))
        self.badge("check", T["room"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: top (break2, fix2)
    def draw_top(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0F172A", "#1E1B4B", "#0F172A"])
        for k in range(16):
            c.drawLine(k * 80, 0, k * 80, H, P("#312E81", 0.5, stroke=2))
        for k in range(26):
            c.drawLine(0, k * 80, W, k * 80, P("#312E81", 0.5, stroke=2))
        cx_, cy_, hs = 540.0, 820.0, 230.0
        fixed = t >= s("fix2") - 0.12
        ang = math.radians(self.wind_ang.at(t))                          # wind comes FROM this direction (0 = east)
        # the roof around the tower
        c.drawRect(R(cx_ - 420, cy_ - 420, 840, 840), P("#3A2A20", 0.8))
        c.drawRect(R(cx_ - 420, cy_ - 420, 840, 840), P("#6B4F3A", 1, stroke=6))
        wall = 34.0
        sq = R(cx_ - hs, cy_ - hs, hs * 2, hs * 2)
        c.drawRect(sq, P("#1F130C"))
        # which quarter faces the wind
        fx, fy = math.cos(ang), -math.sin(ang)
        quads = {"E": (1, 0), "N": (0, -1), "W": (-1, 0), "S": (0, 1)}
        best = max(quads, key=lambda q: quads[q][0] * fx + quads[q][1] * fy)
        if fixed:
            xk = prog(t, T["xw"], T["xw"] + 0.5)
            fk = prog(t, T["brings"] - 0.3, T["brings"] + 0.2)
            ok = prog(t, T["pull"] - 0.3, T["pull"] + 0.2)
            corners = {"N": ((cx_ - hs, cy_ - hs), (cx_ + hs, cy_ - hs)), "E": ((cx_ + hs, cy_ - hs), (cx_ + hs, cy_ + hs)),
                       "S": ((cx_ + hs, cy_ + hs), (cx_ - hs, cy_ + hs)), "W": ((cx_ - hs, cy_ + hs), (cx_ - hs, cy_ - hs))}
            for q, (p0, p1) in corners.items():
                tri = skia.Path()
                tri.moveTo(cx_, cy_)
                tri.lineTo(*p0)
                tri.lineTo(*p1)
                tri.close()
                if q == best:
                    c.drawPath(tri, P(COOL, 0.55 * fk))
                else:
                    c.drawPath(tri, P(HOT, 0.4 * ok))
            for d in (1, -1):                                             # the X of walls
                c.drawLine(cx_ - hs, cy_ - d * hs, lerp(cx_ - hs, cx_ + hs, xk), lerp(cy_ - d * hs, cy_ + d * hs, xk),
                           P("#B89668", 1, stroke=20, cap="butt"))
            for q, (dx, dy) in quads.items():                             # in / out marks
                mx, my = cx_ + dx * hs * 0.55, cy_ + dy * hs * 0.55
                if q == best:
                    c.drawCircle(mx, my, 34, P(COOL, fk, stroke=8))
                    c.drawLine(mx - 22, my - 22, mx + 22, my + 22, P(COOL, fk, stroke=8))
                    c.drawLine(mx - 22, my + 22, mx + 22, my - 22, P(COOL, fk, stroke=8))
                else:
                    c.drawCircle(mx, my, 34, P(HOT, ok, stroke=8))
                    c.drawCircle(mx, my, 9, P(HOT, ok))
                    for i in range(2):                                    # hot air leaving that side
                        q2 = (t * 1.2 + i * 0.5) % 1.0
                        ex, ey = cx_ + dx * (hs + 30 + q2 * 160), cy_ + dy * (hs + 30 + q2 * 160)
                        c.drawCircle(ex + dy * (i - 0.5) * 60, ey + dx * (i - 0.5) * 60, 12, P(HOT, ok * (1 - q2)))
        # the walls with openings: one opening (north) before the fix, all four after
        opens = ["N"] if not fixed else ["N", "E", "S", "W"]
        ow = hs * 1.1
        for q, (dx, dy) in quads.items():
            if dx == 0:
                y0 = cy_ + dy * hs - wall / 2
                if q in opens:
                    c.drawRect(R(cx_ - hs - wall / 2, y0, (hs * 2 - ow) / 2 + wall / 2, wall), P(PLASTER))
                    c.drawRect(R(cx_ + ow / 2, y0, (hs * 2 - ow) / 2 + wall / 2, wall), P(PLASTER))
                else:
                    c.drawRect(R(cx_ - hs - wall / 2, y0, hs * 2 + wall, wall), P(PLASTER))
            else:
                x0 = cx_ + dx * hs - wall / 2
                if q in opens:
                    c.drawRect(R(x0, cy_ - hs - wall / 2, wall, (hs * 2 - ow) / 2 + wall / 2), P(PLASTER))
                    c.drawRect(R(x0, cy_ + ow / 2, wall, (hs * 2 - ow) / 2 + wall / 2), P(PLASTER))
                else:
                    c.drawRect(R(x0, cy_ - hs - wall / 2, wall, hs * 2 + wall), P(PLASTER))
        # the wind: a big arrow coming from 'ang'
        L0, L1 = 560.0, hs + 60
        for i in range(-1, 2):
            px, py = -fy * i * 120, fx * i * 120
            q = (t * 0.9 + i * 0.3) % 1.0
            d0 = lerp(L0, L1, q)
            x0, y0 = cx_ + fx * (L0 + 200) + px, cy_ + fy * (L0 + 200) + py
            x1, y1 = cx_ + fx * d0 + px, cy_ + fy * d0 + py
            c.drawLine(x0, y0, x1, y1, P("#E0F2FE", 0.35, stroke=10))
        ax, ay = cx_ + fx * (hs + 70), cy_ + fy * (hs + 70)
        bx, by = cx_ + fx * (hs + 300), cy_ + fy * (hs + 300)
        arrow(c, bx, by, ax, ay, "#E0F2FE", a=1.0, w=22, head=50)
        if not fixed:
            okk = max(0.0, fx * 0 + fy * -1)                              # how well the wind faces the north opening
            k = clamp((okk - 0.6) / 0.4)
            if k > 0.02:
                c.drawRect(R(cx_ - ow / 2, cy_ - hs, ow, hs * 0.9), P(COOL, 0.5 * k))
            if k < 0.5 and t > T["turn"] + 0.6:
                c.drawLine(cx_ - 90, cy_ - 90, cx_ + 90, cy_ + 90, P(WARN, 1, stroke=18))
                c.drawLine(cx_ - 90, cy_ + 90, cx_ + 90, cy_ - 90, P(WARN, 1, stroke=18))
        self.ui["c"] = (cx_, cy_, hs)

    def ui_top(self, c, t, tw):
        T, s = self.T, self.tl.s
        cx_, cy_, hs = self.ui.get("c", (540, 820, 230))
        self.chip(540, 330, "topview", s("break2") - 0.1, T["direction"] - 0.05, accent="#E0F2FE", size=34)
        if tw < s("fix2") - 0.12:
            self.chip(540, 1180, "turns", T["changing"] - 0.2, T["direction"] + 0.2, accent="#E0F2FE", size=40)
            self.chip(540, 1180, "wrong", T["direction"] + 0.2, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["direction"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["direction"] + 0.05, 1.3)
            return
        self.chip(540, 1180, "four", T["four"] - 0.1, T["split"] - 0.1, accent=HILITE, size=40)
        self.chip(540, 1180, "x", T["split"] - 0.1, T["brings"] - 0.15, accent="#E6CFA3", size=40)
        self.chip(330, 1180, "in", T["brings"] - 0.1, s("break3") - 0.15, accent=COOL, size=40)
        self.chip(770, 1180, "out", T["pull"] - 0.1, s("break3") - 0.15, accent=HOT, size=40)
        self.badge("check", T["pull"] + 0.1, s("break3") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: still (break3, fix3)
    def draw_still(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.camw.at(t)
        fixed = t >= s("fix3") - 0.12
        heat = prog(t, T["burn"], T["burn"] + 0.8) if fixed else 0.0
        stack = prog(t, T["rise2"], T["rise2"] + 1.4) if fixed else 0.0
        low = prog(t, T["drags"] - 0.4, T["drags"] + 1.0) if fixed else 0.0
        hot = 1.0 - prog(t, T["drags"], T["drags"] + 1.6) if fixed else prog(t, s("break3"), s("break3") + 1.0)
        self.scene(c, t, cam, tower=1.0, split=1.0, wind=0.0, hot_room=hot, heat=heat, stack=stack, low_in=low,
                   cool=1 - hot, sun_heat=1.0 + heat)
        self.view(c, cam)                                                # a limp flag on the roof
        fx, fy = -250.0, HY - 40
        lift = prog(t, T["rise2"], T["rise2"] + 1.0) * 0.0
        c.drawLine(fx, fy, fx, fy - 300, P("#4B5563", 1, stroke=9))
        fl = skia.Path()
        fl.moveTo(fx, fy - 295)
        fl.lineTo(fx + 30, fy - 295)
        fl.quadTo(fx + 26 + math.sin(t * 2) * 3, fy - 220, fx + 22, fy - 140)
        fl.lineTo(fx + 4, fy - 146)
        fl.close()
        c.drawPath(fl, P("#DC2626"))
        _ = lift
        c.restore()
        self.ui["cam"] = cam

    def ui_still(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.camw.at(tw))
        if tw < s("fix3") - 0.12:
            fx, fy = self.at(cam, -230, HY - 240)
            self.label(fx, fy, 330, 560, "nowind", T["nowind"] - 0.3, s("fix3") - 0.15, WARN, size=40)
            self.badge("alert", T["nowind"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["nowind"] + 0.05, 1.3)
            return
        tx, ty = self.at(cam, TX1, -760)
        self.label(tx, ty, 800, 560, "sun", T["heats"] - 0.15, T["chimney"] - 0.1, "#FDBA74", size=34)
        ux, uy = self.at(cam, 250, -1080)
        self.label(ux, uy, 760, 560, "chim", T["chimney"] - 0.1, T["drags"] - 0.1, HOT, size=34)
        lx, ly = self.at(cam, -200, -110)
        self.label(lx, ly, 330, 640, "drag", T["drags"] - 0.1, s("break4") - 0.15, COOL, size=32)
        self.badge("check", T["drags"] + 0.2, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: water (break4, fix4, cta)
    def draw_water(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.camq.at(t)
        fixed = t >= s("fix4") - 0.12
        cloth = prog(t, T["wet"], T["wet"] + 0.6) if fixed else 0.0
        pool = prog(t, T["water"] - 0.3, T["water"] + 0.3) if fixed else 0.0
        cool_air = prog(t, T["evap"] - 0.2, T["evap"] + 0.8) if fixed else 0.0
        col = mix(HOT, COOL, cool_air)
        self.scene(c, t, cam, tower=1.0, split=1.0, wind=1.0, in_k=1.0, out_k=1.0, in_col=col, cloth=cloth,
                   pool=pool, hot_room=(1 - cool_air) * 0.7, cool=cool_air)
        if fixed and pool > 0.3:                                         # vapour rising off the pool
            self.view(c, cam)
            for i in range(8):
                q = (t * 0.6 + i / 8.0) % 1.0
                vx = lerp(TX0 - 20, TX1 + 20, (i + 0.5) / 8.0) + math.sin(t * 2 + i) * 10
                c.drawCircle(vx, -60 - q * 220, 10 + q * 22, P("#E0F2FE", 0.35 * (1 - q) * pool))
            c.restore()
        self.ui["cam"] = cam

    def ui_water(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.camq.at(tw))
        if tw < s("fix4") - 0.12:
            hx, hy = self.at(cam, -100, -900)
            self.label(hx, hy, 330, 560, "hotw", T["hotw"] - 0.3, s("fix4") - 0.15, HOT, size=40)
            self.badge("alert", T["hotw"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["hotw"] + 0.05, 1.3)
            return
        if tw < s("cta") - 0.12:
            cx_, cy_ = self.at(cam, TX0 - 6, OPEN0 + 60)
            self.label(cx_, cy_, 300, 560, "cloth", T["wet"] + 0.1, T["water"] - 0.2, "#CBD5E1", size=36)
            px, py = self.at(cam, (TX0 + TX1) / 2, -40)
            self.label(px, py, 760, 1120, "water", T["water"] - 0.1, s("cta") - 0.15, "#60A5FA", size=34)
            self.chip(330, 560, "evap", T["evap"] - 0.1, s("cta") - 0.15, accent=COOL, size=36)
            self.badge("check", T["cools"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: ac (tag)
    def draw_ac(self, c, t):
        T = self.T
        room(c, 0, 0, W, 1250, wall="#3B4A5C", floor="#2A3442", t=t, lamp=False)
        vrect(c, 0, 1250, W, H - 1250, ["#2A3442", "#1C232D", "#0E1218"])
        dead = prog(t, T["breaks"] - 0.2, T["breaks"] + 0.2)
        ac_unit(c, 300, 300, 480, 150, t, dead=dead)
        if dead < 0.5:                                                   # cold air before it dies
            for i in range(4):
                q = (t * 1.2 + i / 4.0) % 1.0
                c.drawLine(360 + i * 110, 470 + q * 120, 340 + i * 110, 520 + q * 140, P(COOL, 0.6 * (1 - q) * (1 - dead * 2), stroke=6))
        if dead > 0.5:
            for i in range(6):                                           # sparks
                q = (t * 3 + i / 6.0) % 1.0
                c.drawLine(540 + i * 12, 300, 540 + i * 12 + (i - 3) * 30 * q, 300 - 60 * q, P("#FDE047", (1 - q) * 0.9, stroke=4))
        c.drawRRect(rr(140, 1000, 800, 110, 30), P("#7F1D1D"))           # a couch and a sweating guy
        c.drawRRect(rr(140, 900, 120, 210, 30), P("#991B1B"))
        c.drawRRect(rr(820, 900, 120, 210, 30), P("#991B1B"))
        person_r(c, 520, 1060, 260, "#F8FAFC", t, pose="sit", face=1, sweat=dead)
        fan = math.sin(t * 14) * 18 * dead
        c.save()
        c.translate(600, 860)
        c.rotate(fan)
        c.drawRRect(rr(-10, -60, 70, 90, 8), P("#FDE68A"))
        c.restore()
        thermo(c, 900, 700, 0.8, lerp(0.4, 0.98, dead), hot=dead > 0.5)

    def ui_ac(self, c, t, tw):
        T = self.T
        self.chip(540, 1180, "free", T["free"] - 0.1, T["breaks"] - 0.05, accent=GOOD, size=32)
        k = self.span(T["msg"], self.duration + 1, 0.25, 0.1)
        if k > 0:
            v2.chip(c, 540, 1180, self.L["msg"], k, accent=WARN, size=40)
        readout(c, 900, 520, lerp(24, 44, prog(tw, T["breaks"], T["breaks"] + 1.5)), 40, "#FCA5A5",
                a=self.span(T["breaks"], self.duration + 1))

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.8, False, 60), -10), (0.6, sfx.hiss(1.2, 61), -18), (T["cooler"], sfx.sparkle(0.7, 9, 62), -10),
              (T["noac"], sfx.thud(0.3), -12), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 63), -9), (T["tower"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 64), -4), (T["still"], sfx.hiss(1.0, 65), -18),
               (T["dusty"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["grow"], sfx.creak(1.0), -10), (T["grown"] - 0.1, sfx.thunk(66), -8), (T["breeze"], sfx.whoosh(1.0, False, 67), -12),
               (T["inflow"], sfx.whoosh(0.8, True, 68), -12), (T["room"] + 0.1, sfx.ding(), -8), (T["room"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 69), -4), (T["turn"], sfx.whoosh(1.0, True, 70), -12),
               (T["direction"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["xw"], sfx.thunk(71), -10), (T["xw"] + 0.2, sfx.thunk(72), -10), (T["brings"], sfx.pop(73), -8),
               (T["pull"] + 0.1, sfx.ding(), -8), (T["pull"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["nowind"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["burn"], sfx.hiss(1.0, 75), -14), (T["rise2"], sfx.whoosh(1.2, True, 76), -12), (T["drags"] + 0.2, sfx.ding(), -8),
               (T["drags"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 77), -4), (T["hotw"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["wet"], sfx.splash() if hasattr(sfx, "splash") else sfx.hiss(0.5, 78), -12), (T["water"], sfx.hiss(0.8, 79), -14),
               (T["evap"], sfx.sparkle(0.8, 9, 80), -10), (T["cools"] + 0.1, sfx.ding(), -8), (T["cools"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(81), 0), (T["follow"] - 0.15, sfx.pop(82), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 83), -6), (T["town_in"], sfx.whoosh(1.2, True, 84), -12),
               (T["dubai"], sfx.pop(85), -10), (T["yazd"], sfx.pop(86), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 87), -6), (T["s1"], sfx.pop(88), -3), (T["s2"], sfx.pop(89), -3),
               (T["s3"], sfx.pop(90), -3)]
        ev += [(T["cong2"], sfx.pop(91), -2), (T["cong2"], sfx.sparkle(1.0, 14, 92), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 93), -6), (T["free"], sfx.chime(), -10), (T["breaks"], sfx.snap(94), -6),
               (T["breaks"] + 0.1, sfx.clank(300.0, 0.5, 95), -10), (T["msg"], sfx.beep(1200.0), -10), (T["msg"] + 0.15, sfx.beep(1200.0), -10)]
        return ev


def arrow(c, x0, y0, x1, y1, col, a=1.0, w=10, head=26):
    if a <= 0:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    c.drawLine(x0, y0, x1 - math.cos(ang) * head * 0.6, y1 - math.sin(ang) * head * 0.6, P(col, a, stroke=w))
    hp = skia.Path()
    hp.moveTo(x1, y1)
    hp.lineTo(x1 - math.cos(ang - 0.45) * head, y1 - math.sin(ang - 0.45) * head)
    hp.lineTo(x1 - math.cos(ang + 0.45) * head, y1 - math.sin(ang + 0.45) * head)
    hp.close()
    c.drawPath(hp, P(col, a))


NAME = "windtower"
EPISODE = WindTower
