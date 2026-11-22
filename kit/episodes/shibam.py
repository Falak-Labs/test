"""Episode 65 - Shibam, the mud-brick skyscraper city (Hadhramaut).  v2 look: a city of tall mud towers with white
lime tops on a mound in a desert valley between flat-topped cliffs, at golden hour; at night their windows lit.

Sets: wadi (hook: the towers rise out of the mound one by one, then a dashed New York skyline shows they came centuries
earlier; stat: wide by day; closer: at dusk, windows lit), flood (break1: a flash flood roars down the valley over a
flat town; fix1: the city on its raised mound inside a wall, the flood flowing around it), plan (break2: low houses
spill off the small mound; fix2: they grow up into five-to-eleven-storey towers packed wall to wall), wall (break3: a
straight tower section, the weight crushes its bottom walls; fix3: walls thick at the bottom and thinner every floor,
the tower tapering), rain (break4: rain melts the mud walls; fix4: white lime on the tops and a family patching the
wall with fresh mud), inside (reveal: one tower cut open: grain and goats below with no windows, the family up high),
tag (a brand-new ceiling leaking into a bucket at the first drizzle).
World: 1 m = 10 units, the valley floor at y = 0, the mound's top at y = -60, the city centred on x = 0.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of, saudi_man, palm_tree  # noqa: E402
from liberty import rain  # noqa: E402

GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DUSKP = {"top": "#0A0A2A", "upper": "#24215C", "mid": "#6A3A78", "low": "#D0705E", "horizon": "#F6A86A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DAYP = {"top": "#1E3A8A", "upper": "#2F5DB8", "mid": "#5B8BD9", "low": "#9CC3EE", "horizon": "#F0DDBA",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STORMP = {"top": "#0A0F1E", "upper": "#1A2238", "mid": "#2E3A52", "low": "#4A5468", "horizon": "#6A7284",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
MUD = "#A87548"
MUD_L = "#C28E5E"
MUD_D = "#74492E"
LIME = "#E9E1D2"
WOOD = "#5A3A22"
FLOOD = "#6E5640"
TOP = -60.0
FH = 30.0                                                        # one floor, 3 m


def _city():
    """The towers: (row, x, width, floors, seed), back row first."""
    rng = random.Random(65)
    out = []
    for row, (y_off, fl0, fl1) in enumerate(((0, 8, 11), (0, 6, 10), (0, 5, 8))):
        x = -620 + rng.uniform(0, 40)
        while x < 600:
            w = rng.uniform(56, 104)
            out.append((row, x + w / 2, w, rng.randint(fl0, fl1), rng.randint(0, 999)))
            x += w + rng.uniform(-6, 4)
    return out


CITY = _city()


def tower_house(c, x, y, w, floors, t, built=1.0, lime=1.0, seed=0, dark=0.0, melt=0.0, a=1.0, lit=0.0, taper=0.08,
                win=1.0):
    """One mud tower house standing on (x, y): floors x 3 m, tapering by `taper`, the top floors whitewashed with lime.
    built 0..1 raises it floor by floor; melt 0..1 streaks and softens the mud; lit 0..1 lights the windows."""
    if a <= 0 or built <= 0:
        return
    h = floors * FH + 12
    hv = h * built
    rng = random.Random(seed)
    col = mix(mix(MUD, MUD_L, rng.random() * 0.6), "#3A2A3A", dark)
    cd = mix(MUD_D, "#2A1E2A", dark)
    wt = w * (1 - taper)
    yt = y - hv
    k = built
    tw = lerp(w, wt, k)
    body = path_of([(x - w / 2, y), (x + w / 2, y), (x + tw / 2, yt), (x - tw / 2, yt)], close=True)
    c.drawPath(body, lin_paint(x - w / 2, 0, x + w / 2, 0, [shade(col, 0.12), col, col, cd], [0.0, 0.3, 0.7, 1.0], a=a))
    if lime > 0 and built > 0.75:                                # the white lime on the top floor
        ly = y - h + 1.15 * FH
        if ly > yt:
            wl = lerp(w, wt, (y - ly) / h)
            lp = path_of([(x - wl / 2, ly), (x + wl / 2, ly), (x + tw / 2, yt), (x - tw / 2, yt)], close=True)
            c.drawPath(lp, P(mix(LIME, "#8A8090", dark), a * lime))
            for kk in range(int(tw / 14)):                       # crenellated parapet
                c.drawRect(R(x - tw / 2 + 3 + kk * 14, yt - 8, 8, 9), P(mix(LIME, "#8A8090", dark), a * lime))
    for f in range(2, floors):                                   # windows from the third floor up
        fy = y - (f + 0.5) * FH
        if fy < yt + 8:
            break
        n = 1 if w < 62 else 2
        for kk in range(n):
            wx = x + (kk - (n - 1) / 2) * w * 0.38
            wc = mix(mix("#2A1A12", "#FFC870", lit * (0.5 + 0.5 * random.Random(seed * 7 + f * 3 + kk).random())), "#1A1420", dark * 0.5)
            c.drawRect(R(wx - 6, fy - 8, 12, 15), P(wc, a * win))
            c.drawRect(R(wx - 8, fy + 7, 16, 3), P(WOOD, 0.8 * a * win))
    if melt > 0:                                                 # rain streaks eating the mud
        for kk in range(int(w / 10)):
            sx = x - w / 2 + 5 + kk * 10
            ln = (20 + (seed * 13 + kk * 31) % 50) * melt
            c.drawLine(sx, yt + 10, sx, yt + 10 + ln, P(cd, 0.6 * a, stroke=3))
    c.drawLine(x - w / 2, y, x - tw / 2, yt, P(shade(col, 0.25), 0.5 * a, stroke=2))
    c.drawLine(x + w / 2, y, x + tw / 2, yt, P("#3A2418", 0.55 * a, stroke=3))


def city(c, t, built=None, lime=1.0, dark=0.0, lit=0.0, melt=0.0, only_rows=(0, 1, 2), grow=1.0):
    """All the towers on the mound. built(i, row) -> 0..1 if given."""
    for i, (row, x, w, fl, sd) in enumerate(CITY):
        if row not in only_rows:
            continue
        b = 1.0 if built is None else built(i, row, x)
        fl2 = max(2, int(round(lerp(2, fl, grow))))
        tower_house(c, x, TOP - row * 4, w, fl2, t, built=b, lime=lime, seed=sd, dark=dark + (2 - row) * 0.06 * 0,
                    lit=lit, melt=melt)


def mound(c, night=0.0, a=1.0):
    """The raised mound the city stands on, with its sloping sides (world)."""
    p_ = path_of([(-760, 2), (-600, TOP), (600, TOP), (760, 2)], close=True)
    c.drawPath(p_, lin_paint(0, TOP, 0, 0, [mix("#B08458", "#3A2E3A", night), mix("#8A6440", "#2A2030", night)], a=a))


def city_wall(c, x0, x1, night=0.0, a=1.0, gate=True):
    """The mud wall round the city along the mound's front edge (world)."""
    col = mix("#A57A50", "#3A2C38", night)
    c.drawRect(R(x0, TOP - 70, x1 - x0, 72), lin_paint(0, TOP - 70, 0, TOP, [shade(col, 0.1), col, shade(col, -0.2)], a=a))
    x = x0
    while x < x1:
        c.drawRect(R(x, TOP - 84, 16, 16), P(shade(col, 0.05), a))
        x += 30
    for bx in (x0 + 60, -260, 260, x1 - 60):                     # round bastions
        if x0 < bx < x1:
            c.drawRect(R(bx - 22, TOP - 96, 44, 98), P(shade(col, 0.08), a))
    if gate:
        c.drawRect(R(-40, TOP - 110, 80, 112), P(shade(col, 0.12), a))
        p_ = skia.Path()
        p_.moveTo(-22, TOP)
        p_.lineTo(-22, TOP - 50)
        p_.quadTo(0, TOP - 76, 22, TOP - 50)
        p_.lineTo(22, TOP)
        p_.close()
        c.drawPath(p_, P(mix("#3A2416", "#120C10", night), a))


def cliffs(c, cx, cy, z, t, night=0.0, a=1.0):
    """The valley's flat-topped sandstone walls behind the city (screen, with parallax)."""
    gy = (0 - cy) * z + H / 2
    for side in (-1, 1):
        c.save()
        c.translate(W / 2 - cx * 0.25 * z, gy)
        c.scale(z * 0.7, z * 0.7)
        x0 = side * 520
        x1 = side * 1900
        top = -820 if side < 0 else -760
        pts = [(x0, 30), (x0 + side * 60, top + 120), (x0 + side * 140, top + 20), (x0 + side * 260, top)]
        rng = random.Random(3 + side)
        xx = x0 + side * 260
        while abs(xx) < abs(x1):
            xx += side * rng.uniform(60, 140)
            pts.append((xx, top + rng.uniform(-14, 14)))
        pts += [(x1, 30)]
        col = mix("#C08A5A", "#3A2A44", night)
        c.drawPath(path_of(pts, close=True), lin_paint(0, top, 0, 30, [shade(col, 0.1), col, mix(col, "#7A4E34", 0.5)], a=a))
        for k in range(14):                                      # rock layers
            yy = top + 40 + k * 60
            c.drawLine(x0 + side * 120, yy, x1, yy + rng.uniform(-6, 6), P(shade(col, -0.25), 0.35 * a, stroke=4))
        c.restore()


def valley_floor(c, night=0.0, a=1.0):
    c.drawRect(R(-3000, 0, 6000, 1600), lin_paint(0, 0, 0, 600, [mix("#C9A070", "#2A2232", night), mix("#9A7448", "#1A1622", night)], a=a))


def palms(c, t, night=0.0, a=1.0, xs=(-900, -820, -740, 760, 840, 930, -1060, 1080)):
    for k, x in enumerate(xs):
        palm_tree(c, x, 4, 0.9 + 0.15 * (k % 3), t + k, a=a * (1 - 0.6 * night))


def ny_ghost(c, x, y, s, a=1.0):
    """A dashed outline of a 1930s New York skyline (world)."""
    if a <= 0:
        return
    pts = [(-260, 0), (-260, -260), (-200, -260), (-200, -340), (-130, -340), (-130, -220), (-70, -220), (-70, -520),
           (-50, -540), (-50, -620), (-30, -640), (-30, -720), (-20, -760), (-10, -720), (-10, -640), (10, -620),
           (10, -540), (30, -520), (30, -300), (110, -300), (110, -400), (180, -400), (180, -240), (260, -240), (260, 0)]
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    p_ = path_of(pts, close=True)
    c.drawPath(p_, P("#FFFFFF", 0.08 * a))
    c.drawPath(p_, dash_paint("#FFFFFF", 0.85 * a, w=5 / s, dash=18, gap=12))
    c.restore()


def flood_water(c, x0, x1, level, t, a=1.0, front=None):
    """Brown flood water over the valley floor up to `level` (world y, negative = higher), its front at x = front."""
    if a <= 0:
        return
    xe = x1 if front is None else min(x1, front)
    if xe <= x0:
        return
    top = [(xx, level + math.sin(xx * 0.02 + t * 7) * 5) for xx in range(int(x0), int(xe), 30)]
    top.append((xe, level + 30))
    pts = top + [(xe, 600), (x0, 600)]
    c.drawPath(path_of(pts, close=True), lin_paint(0, level, 0, level + 300, [FLOOD, "#4A3A2C"], a=0.95 * a))
    c.drawPath(path_of(top), P("#F1E6CF", 0.85 * a, stroke=5))
    for k in range(18):                                          # foam streaks racing downstream
        xx = (x0 + ((t * 520 + k * 133) % max(1.0, xe - x0)))
        yy = level + 12 + (k % 5) * 16
        c.drawLine(xx, yy, xx + 70, yy + 2, P("#E8D8B8", 0.55 * a, stroke=3))
    if front is not None and front < x1:
        c.drawCircle(xe, level + 14, 26, P("#E8D8B8", 0.7 * a))


def section(c, x, y, s, t, floors=11, taper=0.0, crush=0.0, thick=0.0, arrows=0.0, a=1.0):
    """A tall tower house cut in half (screen, standing on (x, y)): its mud walls, floors and the load arrows.
    taper 0..1 makes the walls thick at the bottom and thin at the top; crush 0..1 squashes the bottom walls."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    fh = 60.0
    h = floors * fh
    hw = 170.0
    for f in range(floors):
        y0 = -f * fh
        y1 = y0 - fh
        u = f / max(1, floors - 1)
        wall = lerp(26, lerp(60, 16, u), taper) if taper > 0 else 26.0
        sq = 0.0
        if crush > 0 and f < 2:
            sq = crush * (14 if f == 0 else 6)
        lean = lerp(0.0, 22.0, taper) * u
        xl, xr = -hw + lean, hw - lean
        c.drawRect(R(xl, y1 + sq, wall, fh - sq), lin_paint(xl, 0, xl + wall, 0, [MUD_L, MUD, MUD_D], a=a))
        c.drawRect(R(xr - wall, y1 + sq, wall, fh - sq), lin_paint(xr - wall, 0, xr, 0, [MUD_D, MUD, MUD_L], a=a))
        c.drawRect(R(xl + wall, y1, xr - xl - 2 * wall, 7), P(WOOD, a))          # the floor beams
        c.drawRect(R(xl + wall, y1 + 7, xr - xl - 2 * wall, fh - 7), P("#2A1E1A", 0.55 * a))
        if crush > 0.3 and f == 0:                               # cracks in the crushed bottom walls
            for sx in (xl + wall * 0.5, xr - wall * 0.5):
                c.drawPath(path_of([(sx, y1 + 10), (sx - 6, y1 + 26), (sx + 5, y1 + 38), (sx - 4, y0 - 6)]),
                           P(WARN, crush * a, stroke=3))
    top_y = -h
    c.drawRect(R(-hw + lerp(0, 22, taper), top_y - 10, 2 * (hw - lerp(0, 22, taper)), 12), P(LIME, a))
    if arrows > 0:
        for k in range(4):
            yy = top_y + k * h / 4 + ((t * 120) % (h / 4))
            arrow(c, -hw - 40, yy - 40, -hw - 40, yy + 30, WARN if crush > 0 else "#FDE047", a=arrows, w=10, head=24)
            arrow(c, hw + 40, yy - 40, hw + 40, yy + 30, WARN if crush > 0 else "#FDE047", a=arrows, w=10, head=24)
    if thick > 0:                                                # wall thickness markers
        c.drawLine(-hw, 20, -hw + 60, 20, P("#FDE047", thick * a, stroke=6))
        c.drawLine(-hw + 22, top_y - 20, -hw + 38, top_y - 20, P("#FDE047", thick * a, stroke=6))
    c.restore()


def goat(c, x, y, s, t, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawOval(R(-30, -40, 60, 30), P("#E7E5E4", a))
    for lx in (-20, -8, 10, 22):
        c.drawLine(lx, -14, lx, 0, P("#57534E", a, stroke=4))
    c.drawOval(R(22, -52, 20, 16), P("#E7E5E4", a))
    c.drawLine(28, -52, 22, -62, P("#78716C", a, stroke=3))
    c.drawLine(34, -52, 38, -62, P("#78716C", a, stroke=3))
    c.restore()


def sack(c, x, y, s, a=1.0):
    c.drawRRect(rr(x - 20 * s, y - 44 * s, 40 * s, 44 * s, 12 * s), P("#C8A878", a))
    c.drawLine(x - 10 * s, y - 40 * s, x + 10 * s, y - 40 * s, P("#8A6A4A", a, stroke=3))


def bucket(c, x, y, s, fill=0.0, a=1.0, col="#64748B"):
    c.drawPath(path_of([(x - 40 * s, y - 70 * s), (x + 40 * s, y - 70 * s), (x + 30 * s, y), (x - 30 * s, y)], close=True), P(col, a))
    if fill > 0:
        c.drawRect(R(x - 34 * s, y - 64 * s * fill, 68 * s, 60 * s * fill), P("#60A5FA", 0.8 * a))


# ====================================================================================== the episode
class Shibam(EpisodeV2):
    BUILD_NO = 65
    FIRST_SET = "wadi"
    CLEAR = "#0B1A3A"
    TITLE = {"en": "SHIBAM", "ar_sa": "شبام"}
    EMPH = {"en": ["CONGRATS", "RAISE", "CITY", "SKYSCRAPERS", "DESERT", "MUD", "CENTURIES", "NEW", "YORK", "SHIBAM",
                   "YOURSELF", "VALLEY", "RAIN", "FLASH", "FLOOD", "ROARS", "RAISED", "MOUND", "MIDDLE", "WALL",
                   "FLOODS", "AROUND", "SMALL", "TOWN", "FIT", "UP", "FIVE", "HUNDRED", "TOWER", "HOUSES", "ELEVEN",
                   "FLOORS", "PACKED", "HEAVY", "STACKED", "HIGH", "BOTTOM", "CRUSHED", "THICK", "THINNER", "TAPERS",
                   "RISES", "MELTS", "PAINT", "WHITE", "LIME", "FAMILIES", "PATCH", "FRESH", "FOLLOW", "LONDON'S",
                   "BRIDGE", "STORY", "WINDOWS", "GRAIN", "GOATS", "FAMILY", "SAFE", "RAIDERS", "THIRTY", "METERS",
                   "BRAND-NEW", "CEILING", "LEAKS", "DRIZZLE"],
            "ar_sa": ["مبروك", "مدينة", "ناطحات", "سحاب", "طين", "الصحرا", "نيويورك", "بقرون", "شبام", "بيدك",
                      "وادي", "المطر", "سيل", "يكتسح", "تلة", "مرتفعة", "بسور", "والسيل", "صغيرة", "تنحشر", "لفوق",
                      "خمسمية", "برج", "لإحدعش", "دور", "لازقة", "ثقيل", "تنسحق", "عريض", "ويرق", "يضيق", "يذوب",
                      "بالنورة", "البيضا", "يلبّسون", "جديد", "تابعني", "جسر", "البرج", "شبابيك", "الحب", "والغنم",
                      "والعيلة", "الغزاة", "إحدعش", "الثلاثين", "ومجلسكم", "خرّ", "السقف"]}
    KEYS = {"ar_sa": {
        ("hook", "RAISE"): "بنيت", ("hook", "CITY"): "مدينه", ("hook", "SKYSCRAPERS"): "ناطحات", ("hook", "MUD"): "طين",
        ("hook", "CENTURIES"): "قبل", ("hook", "NEW"): "نيويورك", ("hook", "CONGRATS"): "مبروك", ("hook", "SHIBAM"): "شبام",
        ("break1", "VALLEY"): "وادي", ("break1", "RAIN"): "المطر", ("break1", "FLASH"): "سيل", ("break1", "ROARS"): "يكتسح",
        ("break1", "THROUGH"): "الوادي",
        ("fix1", "RAISED"): "مرتفعه", ("fix1", "MOUND"): "تله", ("fix1", "MIDDLE"): "وسط", ("fix1", "WALL"): "بسور",
        ("fix1", "FLOODS"): "والسيل", ("fix1", "AROUND"): "حولها",
        ("break2", "SMALL"): "صغيره", ("break2", "TOWN"): "والبلد", ("break2", "FIT"): "تنحشر",
        ("fix2", "UP"): "لفوق", ("fix2", "FIVE"): "خمسميه", ("fix2", "TOWER"): "برج", ("fix2", "ELEVEN"): "لاحدعش",
        ("fix2", "PACKED"): "لازقه",
        ("break3", "HEAVY"): "ثقيل", ("break3", "STACKED"): "رصيته", ("break3", "HIGH"): "لهالطول",
        ("break3", "BOTTOM"): "تحت", ("break3", "CRUSHED"): "تنسحق",
        ("fix3", "THICK"): "عريض", ("fix3", "THINNER"): "ويرق", ("fix3", "EVERY"): "دور", ("fix3", "TAPERS"): "يضيق",
        ("fix3", "RISES"): "طالع",
        ("break4", "MUD"): "طين", ("break4", "MELTS"): "يذوب", ("break4", "RAIN"): "المطر",
        ("fix4", "PAINT"): "فتصبغ", ("fix4", "LIME"): "بالنوره", ("fix4", "AFTER"): "وبعد", ("fix4", "FAMILIES"): "يلبسون",
        ("fix4", "PATCH"): "الجدران", ("fix4", "FRESH"): "جديد",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "STORY"): "والسالفه", ("reveal", "WINDOWS"): "شبابيك", ("reveal", "GRAIN"): "الحب",
        ("reveal", "GOATS"): "والغنم", ("reveal", "FAMILY"): "والعيله", ("reveal", "HIGH"): "فوق", ("reveal", "SAFE"): "بعيد",
        ("stat", "FIVE"): "خمسميه", ("stat", "ELEVEN"): "احدعش", ("stat", "THIRTY"): "الثلاثين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "MUD"): "خمسميه", ("tag", "CENTURIES"): "سنه", ("tag", "RAIN"): "والمطر", ("tag", "CEILING"): "ومجلسكم",
        ("tag", "LEAKS"): "خر", ("tag", "DRIZZLE"): "السقف"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: London's Tower Bridge"),
                   "stat": [("~500", "TOWER HOUSES"), ("11", "FLOORS, AT MOST"), ("30+ m", "OF MUD")],
                   "L": {"mudsky": "SKYSCRAPERS OF MUD", "before": "CENTURIES BEFORE NEW YORK", "name": "SHIBAM, YEMEN",
                         "valley": "A DESERT VALLEY", "flood": "FLASH FLOOD!", "mound": "A RAISED MOUND", "wall": "CITY WALL",
                         "around": "THE FLOOD GOES AROUND", "small": "A SMALL MOUND", "nofit": "NO ROOM",
                         "up": "BUILD UP", "five": "~500 TOWER HOUSES", "floors": "5 TO 11 FLOORS", "packed": "WALL TO WALL",
                         "heavy": "MUD IS HEAVY", "crushed": "BOTTOM WALLS CRUSHED", "thick": "THICK AT THE BOTTOM",
                         "thin": "THINNER EVERY FLOOR", "taper": "IT TAPERS AS IT RISES", "melts": "MUD MELTS IN THE RAIN",
                         "lime": "WHITE LIME ON TOP", "patch": "FRESH MUD AFTER EVERY RAIN", "nowin": "NO WINDOWS DOWN HERE",
                         "grain": "GRAIN + GOATS", "family": "THE FAMILY, HIGH UP", "safe": "SAFE FROM RAIDERS",
                         "leak": "DRIP... DRIP...", "new": "BRAND-NEW CEILING"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: جسر البرج"),
                      "stat": [("500", "بيت برج"), ("11", "دور"), ("30+", "متر من الطين")],
                      "L": {"mudsky": "ناطحات سحاب من طين", "before": "قبل نيويورك بقرون", "name": "شبام، حضرموت",
                            "valley": "وادي في الصحرا", "flood": "سيل!", "mound": "تلة مرتفعة", "wall": "السور",
                            "around": "السيل يمشي من حولها", "small": "التلة صغيرة", "nofit": "ما فيه مكان",
                            "up": "ابنِ لفوق", "five": "قرابة خمسمية بيت", "floors": "من خمس لإحدعش دور",
                            "packed": "لازقة في بعض", "heavy": "الطين ثقيل", "crushed": "الجدران تنسحق",
                            "thick": "عريض تحت", "thin": "يرق مع كل دور", "taper": "يضيق وهو طالع",
                            "melts": "الطين يذوب مع المطر", "lime": "نورة بيضا فوق", "patch": "طين جديد بعد كل مطرة",
                            "nowin": "تحت بدون شبابيك", "grain": "الحب والغنم", "family": "العيلة فوق",
                            "safe": "بعيد عن الغزاة", "leak": "خرّ السقف!", "new": "المجلس الجديد"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "raise": ("hook", "RAISE", 0.1), "city": ("hook", "CITY", 0.2), "sky": ("hook", "SKYSCRAPERS", 0.3),
            "mud": ("hook", "MUD", 0.45), "centuries": ("hook", "CENTURIES", 0.55), "york": ("hook", "NEW", 0.65),
            "congrats": ("hook", "CONGRATS", 0.75), "shibam": ("hook", "SHIBAM", 0.92),
            "valley": ("break1", "VALLEY", 0.3), "rain": ("break1", "RAIN", 0.5), "flash": ("break1", "FLASH", 0.75),
            "roars": ("break1", "ROARS", 0.85), "through": ("break1", "THROUGH", 0.95),
            "raised": ("fix1", "RAISED", 0.15), "mound": ("fix1", "MOUND", 0.25), "middle": ("fix1", "MIDDLE", 0.4),
            "wall": ("fix1", "WALL", 0.6), "floods": ("fix1", "FLOODS", 0.8), "around": ("fix1", "AROUND", 0.95),
            "small": ("break2", "SMALL", 0.3), "town": ("break2", "TOWN", 0.55), "fit": ("break2", "FIT", 0.85),
            "up": ("fix2", "UP", 0.1), "five": ("fix2", "FIVE", 0.25), "tower": ("fix2", "TOWER", 0.4),
            "eleven": ("fix2", "ELEVEN", 0.65), "packed": ("fix2", "PACKED", 0.85),
            "heavy": ("break3", "HEAVY", 0.2), "stacked": ("break3", "STACKED", 0.4), "high": ("break3", "HIGH", 0.55),
            "bottom": ("break3", "BOTTOM", 0.75), "crushed": ("break3", "CRUSHED", 0.92),
            "thick": ("fix3", "THICK", 0.15), "thinner": ("fix3", "THINNER", 0.4), "every": ("fix3", "EVERY", 0.55),
            "tapers": ("fix3", "TAPERS", 0.8), "rises": ("fix3", "RISES", 0.95),
            "mud4": ("break4", "MUD", 0.2), "melts": ("break4", "MELTS", 0.6), "rain4": ("break4", "RAIN", 0.9),
            "paint": ("fix4", "PAINT", 0.1), "lime": ("fix4", "LIME", 0.3), "after": ("fix4", "AFTER", 0.45),
            "families": ("fix4", "FAMILIES", 0.6), "patch": ("fix4", "PATCH", 0.75), "fresh": ("fix4", "FRESH", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "story": ("reveal", "STORY", 0.05), "windows": ("reveal", "WINDOWS", 0.3), "grain": ("reveal", "GRAIN", 0.5),
            "goats": ("reveal", "GOATS", 0.6), "family": ("reveal", "FAMILY", 0.7), "high2": ("reveal", "HIGH", 0.8),
            "safe": ("reveal", "SAFE", 0.92),
            "s1": ("stat", "FIVE", 0.05), "s2": ("stat", "ELEVEN", 0.4), "s3": ("stat", "THIRTY", 0.8),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_mud": ("tag", "MUD", 0.05), "t_cent": ("tag", "CENTURIES", 0.25), "t_rain": ("tag", "RAIN", 0.4),
            "t_ceiling": ("tag", "CEILING", 0.6), "t_leaks": ("tag", "LEAKS", 0.8), "t_drizzle": ("tag", "DRIZZLE", 0.95)})
        T["through1"] = max(T["through"], T["roars"]) + 0.15
        T["fit1"] = max(T["fit"], T["town"]) + 0.15
        T["crushed1"] = max(T["crushed"], T["bottom"]) + 0.15
        T["rain41"] = max(T["rain4"], T["melts"]) + 0.15
        T["around1"] = max(T["around"], T["floods"]) + 0.3
        T["packed1"] = max(T["packed"], T["eleven"]) + 0.3
        T["rises1"] = max(T["rises"], T["tapers"]) + 0.3
        T["fresh1"] = max(T["fresh"], T["patch"]) + 0.3
        # ---- sets
        self.cut(s("break1") - 0.12, "flood", 1)
        self.cut(s("break2") - 0.12, "plan", -1)
        self.cut(s("break3") - 0.12, "wall", 1)
        self.cut(s("break4") - 0.12, "rain", -1)
        self.cut(s("reveal") - 0.12, "inside", 1)
        self.cut(s("stat") - 0.12, "wadi", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        cm = Camera(0, -189, 2.1)
        cm.key(0.05, 0, -190, 2.08, 0.5)
        cm.key(max(0.6, T["mud"] - 0.2), 0, -240, 1.5, max(1.0, T["congrats"] - T["mud"] + 0.5))
        cm.key(s("stat") - 0.12, 0, -300, 1.1, 0.0).key(s("stat"), 0, -302, 1.11, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 0, -190, 2.0, 1.0).key(s("closer") + 0.9, 0, -192, 2.06, 3.0)
        self.cam = cm
        pc = Camera(0, -150, 1.6)
        pc.key(s("fix2") - 0.12, 0, -150, 1.6, 0.0)
        pc.key(T["up"] - 0.1, 0, -240, 1.35, max(0.8, T["eleven"] - T["up"]))
        self.pcam = pc
        self.spans = [(T["through1"], T["around1"] + 0.3), (T["fit1"], T["packed1"] + 0.3), (T["crushed1"], T["rises1"] + 0.3),
                      (T["rain41"], T["fresh1"] + 0.3)]
        self.shakes = [(0.1, 0.5, 5), (T["congrats"], 0.35, 8), (T["flash"], 0.8, 9), (T["fit1"], 0.3, 6),
                       (T["crushed1"], 0.5, 9), (T["rain41"], 0.3, 6), (s("closer") + 0.2, 0.35, 9)]

    # ------------------------------------------------------------------ set: wadi (hook, stat, closer)
    def draw_wadi(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        closer = t >= s("closer") - 0.1
        stat = s("stat") - 0.12 <= t < s("closer") - 0.1
        night = prog(t, s("closer") - 0.1, s("closer") + 0.8) * 0.85 if closer else 0.0
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSKP if closer else DAYP if stat else GOLDEN, horizon_y=gy - 200 * z)
        if closer:
            v2.stars(c, W, H, t, 0.7 * night)
        elif not stat:
            add_glow(c, 820 - cx * 0.03, gy - 520 * z, 420, "#FFC98A", 0.45)
        cliffs(c, cx, cy, z, t, night=night * 0.9)
        self.view(c, cam)
        valley_floor(c, night)
        hook = t < s("break1")
        gk = prog(t, T["centuries"] - 0.25, T["centuries"] + 0.1) * (1 - prog(t, T["congrats"] - 0.1, T["congrats"] + 0.3)) if hook else 0.0
        ny_ghost(c, 360, TOP, 0.62, a=gk)
        palms(c, t, night)
        mound(c, night)
        if hook:
            def bf(i, row, x):
                st = -0.25 + abs(x) / 640 * 1.5 + row * 0.1
                return lerp(0.5, 1.0, e_out(prog(t, st, st + 0.6)))
            city(c, t, built=bf, lit=0.0)
        else:
            city(c, t, lit=night, dark=0.4 * night)
        city_wall(c, -600, 600, night)
        for k, x in enumerate((-560, 580)):
            palm_tree(c, x, 0, 1.3, t + k, a=1 - 0.5 * night)
        if closer:
            add_glow(c, 0, -200, 520, "#FFB870", 0.12 * night)
        c.restore()
        self.ui["cam"] = cam

    def ui_wadi(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "mudsky", T["sky"] - 0.2, T["centuries"] - 0.25, accent="#FDE047", size=48)
            self.chip(540, 300, "before", T["centuries"] - 0.25, T["congrats"] - 0.1, accent="#93C5FD", size=40)
            self.chip(540, 300, "name", T["shibam"] - 0.4, s("break1") + 0.1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: flood (break1, fix1)
    def draw_flood(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        cam = (0, -150, 0.8) if fixed else (0, -130, 1.0)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=STORMP if not fixed else GOLDEN, horizon_y=gy - 200 * z)
        cliffs(c, cx, cy, z, t, night=0.35 if not fixed else 0.0)
        self.view(c, cam)
        valley_floor(c, 0.25 if not fixed else 0.0)
        palms(c, t)
        if not fixed:                                            # a flat town on the valley floor, swamped
            for k in range(9):
                x = -480 + k * 120
                tower_house(c, x, 0, 90, 2 + (k % 2), t, lime=0.6, seed=k * 11)
            fr = lerp(-1500, 1600, prog(t, T["rain"], T["through1"] + 0.4))
            lvl = lerp(-6, -48, prog(t, T["flash"] - 0.3, T["through1"] + 0.3))
            flood_water(c, -1600, 1600, lvl, t, front=fr)
        else:
            rise = e_io(prog(t, T["raised"] - 0.3, T["mound"] + 0.3))
            c.save()
            c.translate(0, (1 - rise) * 60)
            mound(c)
            city(c, t)
            wk = prog(t, T["wall"] - 0.3, T["wall"] + 0.1)
            if wk > 0:
                c.save()
                c.translate(0, (1 - wk) * 80)
                city_wall(c, -600, 600)
                c.restore()
            c.restore()
            flood_water(c, -1600, 1600, -26, t)
            ak = prog(t, T["floods"] - 0.3, T["around1"])
            if ak > 0:
                for sd in (-1, 1):
                    arrow(c, sd * 1000, -20, sd * 700, 20, "#E8D8B8", a=ak, w=10, head=26)
        if not fixed and t > T["rain"] - 0.3:
            c.restore()
            rain(c, t, a=prog(t, T["rain"] - 0.3, T["rain"]))
            self.view(c, cam)
        self.ui["mound"] = self.to_screen(cam, 420, -40)
        self.ui["wall"] = self.to_screen(cam, -260, TOP - 90)
        self.ui["water"] = self.to_screen(cam, -300, -30)
        c.restore()

    def ui_flood(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "valley", T["valley"] - 0.2, T["flash"] - 0.2, accent="#FDE68A", size=46)
            self.chip(540, 300, "flood", T["flash"] - 0.2, s("fix1") - 0.15, accent=WARN, size=56)
            self.badge("alert", T["through1"], s("fix1") - 0.2, x=920, y=420)
            self.red(T["through1"], 1.2)
            return
        mx, my = self.ui.get("mound", (800, 1100))
        self.label(mx, my, 760, 560, "mound", T["raised"] - 0.2, s("break2") - 0.2, accent="#FDE68A", size=38)
        wx, wy = self.ui.get("wall", (300, 1000))
        self.label(wx, wy, 300, 640, "wall", T["wall"] - 0.2, s("break2") - 0.2, accent="#E5E7EB", size=38)
        self.chip(540, 300, "around", T["floods"] - 0.2, s("break2") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["around1"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: plan (break2, fix2)
    def draw_plan(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        if not fixed:                                            # from above: the small mound and a town that won't fit
            c.drawRect(R(0, 0, W, H), P("#C9A070"))
            c.drawPath(path_of([(0, 420), (W, 520), (W, 640), (0, 560)], close=True), P("#B8905E"))
            c.drawPath(path_of([(0, 1180), (W, 1100), (W, 1240), (0, 1300)], close=True), P("#B8905E"))
            mp = path_of([(330, 640), (760, 600), (820, 860), (740, 1060), (330, 1060), (270, 840)], close=True)
            c.drawPath(mp, P("#A87C50"))
            c.drawPath(mp, P("#7A5034", stroke=8))
            rng = random.Random(4)
            for gx in range(330, 780, 44):
                for gy in range(650, 1050, 44):
                    if mp.contains(gx + 20, gy + 20):
                        c.drawRect(R(gx, gy, 38, 38), P(rng.choice(["#D8B890", "#C8A070", "#E9E1D2"])))
            sk = prog(t, T["town"] - 0.3, T["fit"])
            rk = prog(t, T["fit"] - 0.3, T["fit1"])
            spill = [(140, 700), (160, 780), (150, 900), (180, 990), (880, 700), (900, 800), (880, 940), (850, 1110),
                     (420, 1120), (520, 1130), (620, 1120), (460, 560), (580, 540)]
            for k, (hx, hy) in enumerate(spill):
                q = clamp(sk * 1.4 - k * 0.03)
                if q > 0:
                    c.drawRect(R(hx, hy, 38, 38), P("#D8B890", q))
                    if rk > 0:
                        c.drawRect(R(hx - 4, hy - 4, 46, 46), P(WARN, rk * q, stroke=5))
            for palm in ((100, 1250), (980, 520), (60, 480)):
                c.drawCircle(palm[0], palm[1], 34, P("#2F6B3A"))
            self.ui["mound"] = (540, 1060)
            return
        cam = self.pcam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy - 200 * z)
        cliffs(c, cx, cy, z, t)
        self.view(c, cam)
        valley_floor(c)
        palms(c, t, xs=(-1240, -1160, 1180, 1260))
        mound(c)
        grow = e_io(prog(t, T["up"] - 0.1, T["eleven"] + 0.3)) if fixed else 0.0
        city(c, t, grow=grow, lime=1.0)
        out_k = 1.0 - (prog(t, s("fix2") - 0.12, T["up"]) if fixed else 0.0)
        if out_k > 0:                                            # the houses that do not fit
            rk = prog(t, T["fit"] - 0.4, T["fit1"])
            for k, x in enumerate((-1000, -900, -800, 800, 900, 1000)):
                tower_house(c, x, 0, 88, 2, t, lime=0.6, seed=200 + k, a=out_k)
                if rk > 0:
                    c.drawRect(R(x - 48, -74, 96, 78), P(WARN, 0.8 * rk * out_k, stroke=5))
        if fixed:
            rk = prog(t, T["eleven"] - 0.4, T["eleven"] + 0.2)
            if rk > 0:                                           # a floor ruler on the tallest tower
                c.drawLine(640, TOP, 640, TOP - 11 * FH, P("#FDE047", rk, stroke=5))
                for f in range(12):
                    c.drawLine(626, TOP - f * FH, 654, TOP - f * FH, P("#FDE047", rk, stroke=3 if f % 5 else 5))
        self.ui["mound"] = self.to_screen(cam, 0, TOP + 20)
        self.ui["ruler"] = self.to_screen(cam, 640, TOP - 330)
        c.restore()

    def ui_plan(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            mx, my = self.ui.get("mound", (540, 1100))
            self.label(mx, my, 540, 1160, "small", T["small"] - 0.2, T["fit"] - 0.2, accent="#FDE68A", size=40)
            self.chip(540, 300, "nofit", T["fit"] - 0.3, s("fix2") - 0.15, accent=WARN, size=52)
            self.badge("alert", T["fit1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["fit1"], 1.2)
            return
        self.chip(540, 300, "up", T["up"] - 0.2, T["five"] - 0.2, accent=GOOD, size=52)
        self.chip(540, 300, "five", T["five"] - 0.2, T["eleven"] - 0.2, accent="#FDE68A", size=44)
        rx, ry = self.ui.get("ruler", (900, 700))
        self.label(rx, ry, 700, 560, "floors", T["eleven"] - 0.3, s("break3") - 0.2, accent="#FDE047", size=38)
        self.chip(540, 300, "packed", T["packed"] - 0.2, s("break3") - 0.15, accent="#93C5FD", size=44)
        self.badge("check", T["packed1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: wall (break3, fix3)
    def draw_wall(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#2A2040", "#5A3A4A", "#9A6A4A"]))
        for k, (x, fl) in enumerate(((120, 7), (960, 8))):       # neighbours in the shade
            tower_house(c, x, 1180, 200, fl, t, lime=1.0, seed=50 + k, dark=0.45, win=0.6)
        c.drawRect(R(0, 1180, W, 100), P("#6A4A34"))
        if not fixed:
            ar_ = prog(t, T["heavy"] - 0.2, T["heavy"] + 0.2)
            cr = prog(t, T["bottom"] - 0.2, T["crushed1"] + 0.2)
            section(c, 540, 1180, 0.92, t, floors=11, crush=cr, arrows=ar_)
        else:
            tp = e_io(prog(t, T["thick"] - 0.2, T["tapers"] + 0.3))
            section(c, 540, 1180, 0.92, t, floors=11, taper=tp, thick=prog(t, T["thick"] - 0.2, T["thick"] + 0.2),
                    arrows=0.6 * (1 - prog(t, T["thick"], T["thick"] + 0.4)))
        self.ui["bottom"] = (540 - 150, 1110)
        self.ui["top"] = (540 - 120, 1180 - 0.92 * 650)

    def ui_wall(self, c, t, tw):
        T, s = self.T, self.tl.s
        bx, by = self.ui.get("bottom", (400, 1100))
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "heavy", T["heavy"] - 0.2, T["bottom"] - 0.2, accent="#FDE68A", size=48)
            self.label(bx, by, 300, 470, "crushed", T["bottom"] - 0.2, s("fix3") - 0.2, accent=WARN, size=38)
            self.badge("alert", T["crushed1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["crushed1"], 1.2)
            return
        self.label(bx, by, 300, 470, "thick", T["thick"] - 0.2, s("break4") - 0.2, accent="#FDE047", size=38)
        tx, ty = self.ui.get("top", (420, 600))
        self.label(tx, ty, 760, 640, "thin", T["thinner"] - 0.2, s("break4") - 0.2, accent="#FDE047", size=38)
        self.chip(540, 300, "taper", T["tapers"] - 0.2, s("break4") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["rises1"] + 0.1, s("break4") - 0.15, x=920, y=640)

    # ------------------------------------------------------------------ set: rain (break4, fix4)
    def draw_rain(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        cam = (60, -200, 2.2)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=STORMP if not fixed else GOLDEN, horizon_y=gy - 200 * z)
        cliffs(c, cx, cy, z, t, night=0.4 if not fixed else 0.0)
        self.view(c, cam)
        valley_floor(c, 0.3 if not fixed else 0.0)
        mound(c, 0.3 if not fixed else 0.0)
        melt = prog(t, T["melts"] - 0.4, T["rain41"] + 0.4) if not fixed else 1.0 - prog(t, T["patch"], T["fresh1"])
        lime = 0.25 if not fixed else lerp(0.25, 1.0, prog(t, T["paint"] - 0.1, T["lime"] + 0.4))
        dk = 0.25 if not fixed else 0.0
        tower_house(c, -80, TOP, 104, 7, t, lime=lime, seed=7, melt=melt, dark=dk)
        tower_house(c, 200, TOP, 112, 8, t, lime=lime, seed=9, melt=melt, dark=dk)
        tower_house(c, 60, TOP, 124, 9, t, lime=lime, seed=8, melt=melt, dark=dk)
        if fixed:
            pk = prog(t, T["paint"] - 0.3, T["paint"])
            if pk > 0:                                           # a man on the roof with lime and a brush
                person(c, 40, TOP - 9 * FH - 12, 46, "#F8FAFC", t, pose="carry", face=1, a=pk)
                bucket(c, 84, TOP - 9 * FH - 12, 0.22, fill=0.8, col="#E5E7EB")
            fk = prog(t, T["families"] - 0.4, T["families"])
            if fk > 0:                                           # someone patching the wall with fresh mud
                c.drawLine(-10, TOP - 9 * FH, -10, TOP - 80, P("#8A6A4A", fk, stroke=3))
                person(c, -24, TOP - 80, 44, "#2563EB", t, pose="point", face=1, a=fk)
                pt = prog(t, T["patch"] - 0.2, T["fresh1"])
                for k in range(4):
                    if pt > k / 4:
                        c.drawOval(R(2 + k * 4, TOP - 150 - k * 36, 34, 24), P(MUD_L, 0.9))
        c.restore()
        if not fixed:
            rain(c, t, a=prog(t, s("break4") - 0.2, T["mud4"]))
        self.ui["top"] = self.to_screen(cam, 60, TOP - 8.5 * FH)
        self.ui["wall"] = self.to_screen(cam, 20, TOP - 120)

    def ui_rain(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "melts", T["mud4"] - 0.1, s("fix4") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["rain41"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["rain41"], 1.2)
            return
        tx, ty = self.ui.get("top", (600, 600))
        self.label(tx, ty, 760, 470, "lime", T["lime"] - 0.2, s("cta") - 0.2, accent="#F8FAFC", size=38)
        wx, wy = self.ui.get("wall", (500, 900))
        self.label(wx, wy, 330, 620, "patch", T["families"] - 0.2, s("cta") - 0.2, accent="#FDE68A", size=34)
        self.badge("check", T["fresh1"] + 0.1, s("cta") - 0.15, x=920, y=1060)

    # ------------------------------------------------------------------ set: inside (reveal)
    def draw_inside(self, c, t):
        T, s = self.T, self.tl.s
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#3E6AA8", "#E39A6A", "#FFC98A"]))
        c.drawRect(R(0, 1190, W, 100), P("#9A7448"))
        x0, x1, fh = 210.0, 870.0, 108.0
        wall = 34.0
        for f in range(6):
            yb = 1190 - f * fh
            yt = yb - fh
            c.drawRect(R(x0, yt, wall, fh), P(MUD))
            c.drawRect(R(x1 - wall, yt, wall, fh), P(MUD_D))
            c.drawRect(R(x0 + wall, yt, x1 - x0 - 2 * wall, fh), P("#6A4E3A" if f < 2 else "#D8B890"))
            c.drawRect(R(x0 + wall, yt, x1 - x0 - 2 * wall, 8), P(WOOD))
            if f >= 2:                                           # windows only up here
                for sx in (x0, x1 - wall):
                    c.drawRect(R(sx, yt + 34, wall, 40), P("#FFD27A" if f >= 4 else "#C8A060"))
        c.drawRect(R(x0 - 6, 1190 - 6 * fh - 16, x1 - x0 + 12, 18), P(LIME))
        gk = prog(t, T["grain"] - 0.3, T["grain"])
        for k in range(4):
            sack(c, 300 + k * 60, 1190 - fh - 2, 1.0, a=gk)
        gt = prog(t, T["goats"] - 0.3, T["goats"])
        for k in range(3):
            goat(c, 330 + k * 160, 1186, 1.0 + 0.1 * (k % 2), t, a=gt)
        fk = prog(t, T["family"] - 0.3, T["family"])
        if fk > 0:
            c.drawRect(R(x0 + wall + 20, 1190 - 4 * fh - 10, 420, 10), P("#B91C1C", fk))    # carpets
            c.drawRect(R(x0 + wall + 20, 1190 - 5 * fh - 10, 420, 10), P("#1D4ED8", fk))
            person(c, 380, 1190 - 4 * fh - 10, 80, "#7C3AED", t, pose="sit", face=1, a=fk)
            person(c, 520, 1190 - 4 * fh - 10, 86, "#16A34A", t, pose="stand", face=-1, a=fk)
            person(c, 640, 1190 - 5 * fh - 10, 60, "#F59E0B", t, pose="cheer", face=-1, a=fk)
            add_glow(c, 560, 1190 - 4.6 * fh, 220, "#FFD27A", 0.4 * fk)
        sk = prog(t, T["safe"] - 0.3, T["safe"])
        if sk > 0:
            arrow(c, 960, 1100, 960, 640, GOOD, a=sk, w=12, head=30)
        self.ui["low"] = (x0 + 20, 1190 - fh * 0.5)
        self.ui["grain"] = (360, 1190 - fh - 30)
        self.ui["fam"] = (520, 1190 - 4.5 * fh)

    def ui_inside(self, c, t, tw):
        T, s = self.T, self.tl.s
        lx, ly = self.ui.get("low", (230, 1130))
        self.label(lx, ly, 330, 470, "nowin", T["windows"] - 0.3, T["grain"] - 0.1, accent=WARN, size=36)
        gx, gy = self.ui.get("grain", (360, 1050))
        self.label(gx, gy, 330, 470, "grain", T["grain"] - 0.1, T["family"] - 0.1, accent="#FDE68A", size=40)
        fx_, fy_ = self.ui.get("fam", (520, 700))
        self.label(fx_, fy_, 540, 420, "family", T["family"] - 0.1, T["safe"] - 0.1, accent=GOOD, size=40)
        self.chip(540, 300, "safe", T["safe"] - 0.2, s("stat") - 0.15, accent=GOOD, size=46)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#D9CDB8", "#C9B79C", "#A8916E"]))
        c.drawRect(R(0, 0, W, 560), P("#E4DED2"))               # the brand-new ceiling
        c.drawRect(R(0, 556, W, 8), P("#D6CCBC"))
        c.drawCircle(700, 600, 30, P("#FFF7D6"))
        add_glow(c, 700, 620, 200, "#FFF1C0", 0.4)
        c.drawRect(R(0, 564, W, 620), lin_paint(0, 564, 0, 1180, ["#D8C8AE", "#C2AE8E"]))
        c.drawRRect(rr(760, 660, 230, 280, 12), P("#7A8BA8"))    # a window with drizzle outside
        c.save()
        c.clipRRect(rr(760, 660, 230, 280, 12))
        for k in range(14):
            xx = 760 + ((k * 37 + t * 60) % 250)
            yy = 660 + ((k * 53 + t * 700) % 300)
            c.drawLine(xx, yy, xx - 6, yy + 18, P("#E0F2FE", 0.7, stroke=2))
        c.restore()
        c.drawRect(R(0, 1180, W, 760), P("#B89A78"))
        lk = prog(t, T["t_leaks"] - 0.3, T["t_leaks"])
        if lk > 0:                                               # the leak
            c.drawPath(path_of([(380, 564), (420, 580), (400, 600), (430, 620)]), P("#8A7A6A", lk, stroke=5))
            c.drawOval(R(360, 560, 140, 30), P("#B8A890", 0.5 * lk))
            for k in range(3):
                q = ((t - T["t_leaks"]) * 1.4 + k / 3) % 1.0
                c.drawOval(R(420, lerp(620, 1090, q), 14, 20), P("#60A5FA", lk))
        if not self.rtl:
            c.drawRRect(rr(80, 960, 560, 150, 40), P("#475569"))
            c.drawRRect(rr(80, 900, 560, 90, 40), P("#64748B"))
            person(c, 760, 1180, 330, "#16A34A", t, pose="shrug" if lk > 0 else "stand", face=-1)
        else:
            for k in range(4):
                c.drawRRect(rr(40 + k * 170, 1080, 160, 90, 20), P(("#B91C1C", "#14532D", "#B91C1C", "#14532D")[k]))
            saudi_man(c, 760, 1180, 330, t, pose="shrug" if lk > 0 else "look", face=-1)
        bucket(c, 426, 1180, 1.2, fill=prog(t, T["t_leaks"], T["t_drizzle"] + 1.5), col="#2563EB")

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 420, "new", T["t_ceiling"] - 0.2, T["t_leaks"] - 0.1, accent="#93C5FD", size=46)
        self.chip(540, 420, "leak", T["t_leaks"] - 0.1, self.duration + 1, accent=WARN, size=52)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1E3A6E", "#3E6AA8", "#E39A6A"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.1, sfx.riser(1.6, 61), -12), (T["sky"], sfx.thunk(62), -8), (T["mud"], sfx.thud(0.4, 63), -10),
              (T["centuries"], sfx.whoosh(0.5, False, 64), -12), (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 66), -8), (T["shibam"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["rain"], sfx.hiss(1.4, 68), -14),
               (T["flash"], rumble(2.0, 69), -8), (T["through1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 70), -4), (T["mound"], sfx.thud(0.5, 71), -8),
               (T["wall"], sfx.thunk(72), -8), (T["floods"], sfx.whoosh(0.8, False, 73), -14), (T["around1"], sfx.ding(), -8),
               (T["around1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["town"], sfx.pop(75), -8), (T["fit1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 76), -4), (T["up"], sfx.riser(1.4, 77), -12),
               (T["eleven"], sfx.pop(78), -8), (T["packed1"], sfx.ding(), -8), (T["packed1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["heavy"], sfx.thud(0.5, 80), -8),
               (T["crushed"], sfx.creak(1.0, 81), -8), (T["crushed1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 82), -4), (T["thick"], sfx.thunk(83), -8),
               (T["tapers"], sfx.whoosh(0.6, True, 84), -12), (T["rises1"], sfx.ding(), -8), (T["rises1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 85), -4), (T["mud4"], sfx.hiss(1.4, 86), -14),
               (T["rain41"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 87), -4), (T["lime"], sfx.tap(88), -8),
               (T["patch"], sfx.tap(89), -8), (T["fresh1"], sfx.ding(), -8), (T["fresh1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(90), 0), (T["follow"] - 0.15, sfx.pop(91), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 92), -6), (T["grain"], sfx.pop(93), -8),
               (T["goats"], sfx.pop(94), -8), (T["family"], sfx.sparkle(0.6, 8, 95), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 96), -6), (T["s1"], sfx.pop(97), -3), (T["s2"], sfx.pop(98), -3),
               (T["s3"], sfx.pop(99), -3)]
        ev += [(T["cong2"], sfx.pop(100), -2), (T["cong2"], sfx.sparkle(1.4, 18, 101), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 102), -6), (T["t_leaks"], sfx.tap(103), -6),
               (T["t_leaks"] + 0.7, sfx.tap(104), -8), (T["t_drizzle"], sfx.tap(105), -8)]
        return ev


NAME = "shibam"
EPISODE = Shibam
