"""Episode 44 - An Omani falaj (aflaj irrigation, Oman).  v2 look: a golden afternoon over the Hajar mountains, a
stone-lined channel of clear water running through a mud-brick village and its date palms.

Sets: oasis (hook: water flows out of a stone mouth in the dry desert and runs along the channel past palms and a
village, no pump, no power, 1,500 years; the reveal: the water passes drinking, baths, washing, then the palms; the
stat; the closer), section (break1: one raindrop on hot sand, the water hidden in the rock under the mountains; fix1:
the mother well dug down to it, 60 m; break2: the village is miles away and the water stays at the bottom of the well;
fix2: the tunnel dug back from the village to the well on a gentle slope, gravity brings the water out to the fields),
dig (break3: one digger in a hot, dark tunnel, 20 minutes at a time; fix3: shafts from the surface for air and to haul
up rock), aerial (end of fix3: from a plane the shafts are a dotted line across the desert), share (break4: one stream,
200 owners, every gate open; fix4: half-hour turns, a sundial's shadow by day, a star at a mountain peak by night; the
cta), bath (the tag: the family queue at the one bathroom at 7 a.m., "almost out!").
World (oasis, share): side view, ground y = 0, the channel's water surface at y = 0..18, up is negative.
World (section): side view, the plain falls to the right (surf(x)), the water-bearing rock under the mountain.
"""
from v2_base import *  # noqa: F401,F403
from pyramid import palm  # noqa: E402
from windtower import flow, sun, heat_lines, arrow, plug_off  # noqa: E402
from panama import pump  # noqa: E402

GOLD = {"top": "#16204C", "upper": "#3E3F7C", "mid": "#B25F78", "low": "#F2A15E", "horizon": "#FFD58C",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHT_SKY = {"top": "#020617", "upper": "#0B1033", "mid": "#1B1F4F", "low": "#2E2D63", "horizon": "#4B3F72",
             "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SAND, SAND_D = "#E2B06E", "#A8733A"
MUD, MUD_D = "#C98F5A", "#8E5E36"
ROCK, ROCK_D = "#9A6448", "#4A2C22"
STONE = "#C9B48E"
AQUA, AQUA_D = "#38BDF8", "#0369A1"
FARM = "#3F7A2E"


def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def mudhouse(c, x, y, w, h, a=1.0, lit=0.5, seed=0):
    """A flat-roofed mud-brick house with a crenellated parapet, standing on (x, y)."""
    rng = random.Random(seed)
    c.drawRect(R(x - w / 2, y - h, w, h), lin_paint(x - w / 2, 0, x + w / 2, 0, [MUD, shade(MUD, -0.08), MUD_D], a=a))
    n = max(3, int(w / 26))
    for i in range(n):
        if i % 2 == 0:
            c.drawRect(R(x - w / 2 + i * w / n, y - h - 14, w / n, 14), P(MUD, a))
    for k in range(rng.randint(1, 3)):
        wx = x - w / 2 + w * (0.2 + 0.3 * k)
        c.drawRect(R(wx, y - h * 0.62, w * 0.12, h * 0.2), P("#3B2416", a))
        if lit > 0:
            c.drawRect(R(wx, y - h * 0.62, w * 0.12, h * 0.2), P("#FDBA74", lit * a * rng.uniform(0.3, 1.0)))
    c.drawRect(R(x - w * 0.1, y - h * 0.38, w * 0.2, h * 0.38), P("#5B3A22", a))
    c.drawLine(x - w / 2, y - h * 0.86, x + w / 2, y - h * 0.86, P(MUD_D, 0.4 * a, stroke=3))


def fort_tower(c, x, y, r, h, a=1.0):
    c.drawRect(R(x - r, y - h, 2 * r, h), lin_paint(x - r, 0, x + r, 0, [MUD, shade(MUD, -0.05), MUD_D], a=a))
    for i in range(5):
        if i % 2 == 0:
            c.drawRect(R(x - r + i * 2 * r / 5, y - h - 18, 2 * r / 5, 18), P(MUD, a))
    for k in range(3):
        c.drawRect(R(x - 6, y - h * (0.3 + 0.22 * k), 12, 26), P("#3B2416", a))


def channel(c, x0, x1, t, front=1.0, a=1.0, wet=1.0, flow_x=None, level=1.0):
    """The falaj seen from the side: back bank, water surface (0..18), front stone wall (18..70).
    flow_x: the water has reached x (None = full). level 0..1 lowers the water (less water)."""
    c.drawRect(R(x0, -18, x1 - x0, 12), P(shade(STONE, -0.05), a))
    c.drawRect(R(x0, -8, x1 - x0, 26), P("#6B5434", a))
    xe = x1 if flow_x is None else clamp(flow_x, x0, x1)
    if xe > x0 and wet > 0:
        top = lerp(16, -6, clamp(level))
        c.drawRect(R(x0, top, xe - x0, 18 - top), lin_paint(0, top, 0, 18, [AQUA, AQUA_D], a=wet * a))
        xx = x0 + ((t * 120) % 70)
        while xx < xe - 20:
            c.drawLine(xx, top + 5, xx + 26, top + 5, P("#E0F2FE", 0.7 * wet * a, stroke=3))
            xx += 70
        if flow_x is not None and xe < x1:
            add_glow(c, xe, 6, 40, "#BAE6FD", 0.7 * wet * a)
            c.drawCircle(xe, top + 6, 10, P("#E0F2FE", 0.8 * wet * a))
    if front > 0:
        c.drawRect(R(x0, 18, x1 - x0, 52), lin_paint(0, 18, 0, 70, [STONE, shade(STONE, -0.3)], a=front * a))
        for xx in range(int(x0), int(x1), 60):
            c.drawLine(xx, 18, xx, 70, P("#7A6545", 0.5 * front * a, stroke=2))
        c.drawLine(x0, 44, x1, 44, P("#7A6545", 0.4 * front * a, stroke=2))


def mouth(c, x, a=1.0):
    """The stone mouth where the tunnel comes out of the ground."""
    c.drawRect(R(x - 70, -96, 140, 166), lin_paint(x - 70, 0, x + 70, 0, [STONE, shade(STONE, -0.2)], a=a))
    ap = skia.Path()
    ap.moveTo(x - 40, 18)
    ap.lineTo(x - 40, -30)
    ap.arcTo(R(x - 40, -70, 80, 80), 180, 180, False)
    ap.lineTo(x + 40, 18)
    ap.close()
    c.drawPath(ap, P("#1A120C", a))
    c.drawRect(R(x - 80, -110, 160, 18), P(shade(STONE, 0.1), a))


def jar(c, x, y, s, a=1.0):
    jp = skia.Path()
    jp.moveTo(x - 18 * s, y - 70 * s)
    jp.quadTo(x - 50 * s, y - 40 * s, x - 30 * s, y)
    jp.lineTo(x + 30 * s, y)
    jp.quadTo(x + 50 * s, y - 40 * s, x + 18 * s, y - 70 * s)
    jp.close()
    c.drawPath(jp, lin_paint(x - 40 * s, 0, x + 40 * s, 0, ["#C2703D", "#E39A5F", "#8A4A26"], a=a))
    c.drawRect(R(x - 20 * s, y - 80 * s, 40 * s, 12 * s), P("#8A4A26", a))


def bath_hut(c, x, y, w, h, a=1.0):
    c.drawRect(R(x - w / 2, y - h, w, h), lin_paint(x - w / 2, 0, x + w / 2, 0, [MUD, MUD_D], a=a))
    c.drawRect(R(x - w / 2 - 10, y - h - 14, w + 20, 16), P(shade(MUD, 0.1), a))
    dp = skia.Path()
    dp.moveTo(x - 26, y)
    dp.lineTo(x - 26, y - h * 0.5)
    dp.arcTo(R(x - 26, y - h * 0.5 - 26, 52, 52), 180, 180, False)
    dp.lineTo(x + 26, y)
    dp.close()
    c.drawPath(dp, P("#2B1A10", a))


def stars_sky(c, t, a=1.0, seed=3):
    rng = random.Random(seed)
    for i in range(80):
        x, y = rng.uniform(0, W), rng.uniform(150, 1000)
        tw_ = 0.6 + 0.4 * math.sin(t * 3 + i)
        c.drawCircle(x, y, rng.uniform(1.5, 3.5), P("#F8FAFC", a * tw_))


def windlass(c, x, y, s, t, turn=0.0, a=1.0):
    """A wooden frame with a turning drum over a shaft, its rope going down."""
    c.drawLine(x - 60 * s, y, x - 40 * s, y - 120 * s, P("#7C5A3A", a, stroke=10 * s))
    c.drawLine(x + 60 * s, y, x + 40 * s, y - 120 * s, P("#7C5A3A", a, stroke=10 * s))
    c.drawLine(x - 50 * s, y - 116 * s, x + 50 * s, y - 116 * s, P("#5B3A22", a, stroke=14 * s))
    c.save()
    c.translate(x, y - 116 * s)
    c.rotate(turn * 360)
    c.drawLine(-28 * s, 0, 28 * s, 0, P("#A16207", a, stroke=6 * s))
    c.drawLine(0, -28 * s, 0, 28 * s, P("#A16207", a, stroke=6 * s))
    c.restore()


def basket(c, x, y, s, a=1.0, full=1.0):
    c.drawLine(x, y - 40 * s, x, y - 1200 * s, P("#D6C29A", a, stroke=3 * s))
    bp = skia.Path()
    bp.moveTo(x - 30 * s, y - 40 * s)
    bp.lineTo(x + 30 * s, y - 40 * s)
    bp.lineTo(x + 22 * s, y)
    bp.lineTo(x - 22 * s, y)
    bp.close()
    c.drawPath(bp, P("#A16207", a))
    if full > 0:
        for k in range(5):
            c.drawCircle(x - 20 * s + k * 10 * s, y - 44 * s - (k % 2) * 6 * s, 8 * s, P("#78716C", a * full))


def pick_digger(c, x, y, h, t, swing=1.0, a=1.0, sweat=0.0):
    """A digger crouching in a low tunnel, swinging a pick to the right."""
    person(c, x, y, h, "#F5F5F4", t, pose="duck", face=1, hat="none", hair="#1C1917", skin="#B07A4F", pants="#57534E", a=a)
    u = h / 140.0
    ang = math.radians(-70 + 80 * abs(math.sin(t * 5.0)) * swing)
    hx, hy = x + 20 * u, y - 70 * u
    ex, ey = hx + math.cos(ang) * 80 * u, hy + math.sin(ang) * 80 * u
    c.drawLine(hx, hy, ex, ey, P("#7C5A3A", a, stroke=7 * u))
    nx, ny = math.cos(ang + 1.57), math.sin(ang + 1.57)
    c.drawLine(ex - nx * 26 * u, ey - ny * 26 * u, ex + nx * 26 * u, ey + ny * 26 * u, P("#9CA3AF", a, stroke=8 * u))
    if sweat > 0:
        for k in range(3):
            q = (t * 1.4 + k / 3.0) % 1.0
            c.drawCircle(x + (k - 1) * 10 * u, y - 120 * u + q * 40 * u, 4 * u, P("#BAE6FD", sweat * a * (1 - q)))


def timer(c, x, y, r, frac, a=1.0):
    """A stopwatch ring running down from 20:00."""
    c.drawCircle(x, y, r, P("#0B1220", 0.9 * a))
    c.drawCircle(x, y, r, P("#334155", a, stroke=12))
    c.drawArc(R(x - r, y - r, 2 * r, 2 * r), -90, 360 * (1 - frac), False, P(WARN, a, stroke=12))
    sec = int(round((1 - frac) * 1200))
    text(c, f"{sec // 60:02d}:{sec % 60:02d}", x, y + r * 0.2, r * 0.52, "#F8FAFC", "Poppins-Black", a=a)
    c.drawRect(R(x - 12, y - r - 26, 24, 18), P("#334155", a))


def plane_top(c, x, y, s, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-14, -90, 28, 180, 14), P("#F8FAFC", a))
    wg = skia.Path()
    wg.moveTo(-150, 10)
    wg.lineTo(0, -30)
    wg.lineTo(150, 10)
    wg.lineTo(0, 20)
    wg.close()
    c.drawPath(wg, P("#E2E8F0", a))
    c.drawRect(R(-50, 70, 100, 16), P("#E2E8F0", a))
    c.restore()


def sundial(c, x, y, s, t, ang, a=1.0, glow=0.0):
    """A stone platform seen at an angle, a stick, its shadow at angle ang (degrees), six marker stones."""
    c.drawOval(R(x - 200 * s, y - 50 * s, 400 * s, 100 * s), P("#A8916C", a))
    c.drawOval(R(x - 200 * s, y - 50 * s, 400 * s, 100 * s), P("#6B5434", a, stroke=6 * s))
    for k in range(6):
        an = math.radians(200 + k * 28)
        mx, my = x + math.cos(an) * 160 * s, y - 10 * s + math.sin(an) * 36 * s
        c.drawOval(R(mx - 16 * s, my - 8 * s, 32 * s, 16 * s), P("#E7E5E4" if k % 2 == 0 else "#57534E", a))
    an = math.radians(ang)
    sp = skia.Path()
    sp.moveTo(x - 6 * s, y)
    sp.lineTo(x + math.cos(an) * 170 * s, y - 10 * s + math.sin(an) * 38 * s)
    sp.lineTo(x + 6 * s, y)
    sp.close()
    c.drawPath(sp, P("#1C1410", 0.75 * a))
    c.drawLine(x, y, x, y - 150 * s, P("#5B3A22", a, stroke=10 * s))
    if glow > 0:
        add_glow(c, x + math.cos(an) * 170 * s, y - 10 * s + math.sin(an) * 38 * s, 50 * s, "#FDE68A", glow * a)


def door_queue(c, t, rtl=False, bang=0.0, a=1.0):
    """The tag: a hallway, the one bathroom door, the family waiting with towels at 7 a.m."""
    vrect(c, 0, 0, W, H, ["#3A2A3F", "#2A1E30"])
    c.drawRect(R(0, 1130, W, 120), lin_paint(0, 1130, 0, 1250, ["#6B4A3A", "#3E2A20"]))
    vrect(c, 0, 1240, W, H - 1240, ["#3E2A20", "#1E140F"])
    c.drawRect(R(0, 1110, W, 22), P("#8B6A4E"))
    dx = 760
    c.drawRect(R(dx - 150, 520, 300, 610), P("#A0704A"))
    c.drawRect(R(dx - 132, 538, 264, 592), lin_paint(dx - 132, 0, dx + 132, 0, ["#C89564", "#9C6A40"]))
    shake = math.sin(t * 60) * 6 * bang
    c.drawCircle(dx - 100 + shake, 840, 12, P("#FDE68A"))
    c.drawRect(R(dx - 132, 1122, 264, 8), P("#FDE68A", 0.9))
    add_glow(c, dx, 1128, 160, "#FDE68A", 0.4)
    c.drawRRect(rr(dx - 60, 600, 120, 120, 18), P("#F8FAFC"))
    c.drawRRect(rr(dx - 30, 626, 60, 34, 8), P("#64748B"))
    c.drawOval(R(dx - 40, 656, 80, 44), P("#64748B"))
    cx_, cy_ = 300, 520
    c.drawCircle(cx_, cy_, 92, P("#F8FAFC"))
    c.drawCircle(cx_, cy_, 92, P("#475569", stroke=10))
    for k in range(12):
        an = math.radians(k * 30)
        c.drawLine(cx_ + math.cos(an) * 74, cy_ + math.sin(an) * 74, cx_ + math.cos(an) * 84, cy_ + math.sin(an) * 84,
                   P("#475569", stroke=5))
    c.drawLine(cx_, cy_, cx_, cy_ - 66, P("#111827", stroke=8))
    c.drawLine(cx_, cy_, cx_ - 40, cy_ + 24, P("#111827", stroke=10))
    people = [(560, "#2563EB", 250, "stand"), (420, "#DB2777", 236, "stand"), (280, "#16A34A", 200, "stand"),
              (150, "#F59E0B", 160, "stand")]
    for i, (px, col, h, pose) in enumerate(people):
        hop = abs(math.sin(t * 6 + i)) * 10
        person(c, px, 1180 - hop, h, col, t + i * 0.3, pose="shrug" if i == 1 else pose, face=1, hat="none",
               hair="#1C1917")
        u = h / 140.0
        c.drawRRect(rr(px - 34 * u, 1180 - hop - 104 * u, 22 * u, 60 * u, 6 * u), P("#F8FAFC", 0.95))


# ====================================================================================== the episode
class Falaj(EpisodeV2):
    BUILD_NO = 44
    FIRST_SET = "oasis"
    CLEAR = "#16204C"
    TITLE = {"en": "OMANI FALAJ", "ar_sa": "فلج عماني"}
    EMPH = {"en": ["CONGRATS", "STREAM", "FLOW", "DESERT", "PUMP", "POWER", "FIFTEEN", "CENTURIES", "OMANI", "FALAJ",
                   "BARELY", "RAINS", "DEEP", "MOUNTAINS", "MOTHER", "WELL", "SIXTY", "METERS", "VILLAGE", "MILES",
                   "CLIMB", "TUNNEL", "SLOPE", "GENTLE", "GRAVITY", "ALONE", "HAND", "UNDERGROUND", "HEAT",
                   "TWENTY", "MINUTES", "SHAFTS", "AIR", "ROCK", "PLANE", "DOTTED", "LINE", "ONE", "HUNDRED",
                   "OWNERS", "EVERYONE", "TIME", "HALF-HOUR", "TURNS", "SUNDIAL'S", "SHADOW", "STARS", "NIGHT",
                   "FOLLOW", "MACHU", "PICCHU'S", "TERRACES", "DRINKING", "BATHS", "WASHING", "PALMS", "THREE",
                   "THOUSAND", "FLOWING", "SIXTY-METER", "WELLS", "YOURSELF", "FIGHTS", "FAMILY", "BATHROOM",
                   "SEVEN"],
            "ar_sa": ["مبروك", "مية", "الصحرا", "طلمبة", "كهربا", "خمستاشر", "قرن", "فلج", "عماني", "المطر", "نادر",
                      "مستخبية", "الجبال", "بير", "أم", "ستين", "متر", "القرية", "بعيدة", "هتطلع", "نفق", "ميله",
                      "خفيف", "والجاذبية", "للغيطان", "بإيدك", "الحر", "عشرين", "دقيقة", "آبار", "للهوا", "وللصخر",
                      "الطيارة", "منقط", "واحد", "ومتين", "عايزها", "فتقسمها", "نص", "ساعة", "المزولة", "ضل",
                      "وبالليل", "النجوم", "تابعني", "ماتشو", "بيتشو", "الشرب", "الاستحمام", "الغسيل", "النخل",
                      "تلات", "آلاف", "شغالين", "بإيدك", "خناقة", "حمام", "الصبح", "خارج"]}
    KEYS = {"ar_sa": {
        ("hook", "STREAM"): "مية", ("hook", "DESERT"): "الصحرا", ("hook", "PUMP"): "طلمبة", ("hook", "POWER"): "كهربا",
        ("hook", "CENTURIES"): "قرن", ("hook", "CONGRATS"): "مبروك", ("hook", "OMANI"): "عماني",
        ("break1", "RAINS"): "المطر", ("break1", "DEEP"): "مستخبية", ("break1", "MOUNTAINS"): "الجبال",
        ("fix1", "DIG"): "فتحفر", ("fix1", "MOTHER"): "بير", ("fix1", "SIXTY"): "ستين",
        ("break2", "VILLAGE"): "القرية", ("break2", "MILES"): "بعيدة", ("break2", "CLIMB"): "هتطلع",
        ("fix2", "TUNNEL"): "نفق", ("fix2", "SLOPE"): "ميله", ("fix2", "GENTLE"): "خفيف", ("fix2", "GRAVITY"): "والجاذبية",
        ("fix2", "OUT"): "للغيطان",
        ("break3", "HAND"): "بإيدك", ("break3", "HEAT"): "الحر", ("break3", "TWENTY"): "عشرين",
        ("break3", "MINUTES"): "دقيقة",
        ("fix3", "SHAFTS"): "آبار", ("fix3", "AIR"): "للهوا", ("fix3", "ROCK"): "وللصخر", ("fix3", "PLANE"): "الطيارة",
        ("fix3", "DOTTED"): "منقط",
        ("break4", "ONE"): "واحد", ("break4", "HUNDRED"): "ومتين", ("break4", "WANTS"): "عايزها",
        ("fix4", "SHARE"): "فتقسمها", ("fix4", "HALF"): "نص", ("fix4", "SUNDIAL"): "المزولة", ("fix4", "SHADOW"): "ضل",
        ("fix4", "NIGHT"): "وبالليل", ("fix4", "STARS"): "النجوم",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "VILLAGE"): "القرية", ("reveal", "DRINKING"): "الشرب", ("reveal", "BATHS"): "الاستحمام",
        ("reveal", "WASHING"): "الغسيل", ("reveal", "PALMS"): "النخل",
        ("stat", "THREE"): "تلات", ("stat", "SIXTY"): "ستين", ("stat", "FIFTEEN"): "خمستاشر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "FIGHTS"): "خناقة", ("tag", "FAMILY"): "وعندنا", ("tag", "BATHROOM"): "حمام", ("tag", "SEVEN"): "الصبح"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Machu Picchu"),
                   "stat": [("3,000+", "STILL FLOWING"), ("60 m", "DEEP WELLS"), ("1,500", "YEARS OLD")],
                   "L": {"nopump": "NO PUMP", "nopower": "NO POWER", "years": "1,500 YEARS", "name": "AN OMANI FALAJ",
                         "rain": "IT BARELY RAINS", "deep": "WATER HIDDEN IN THE ROCK", "mother": "MOTHER WELL",
                         "m60": "UP TO 60 m", "miles": "THE VILLAGE: MILES AWAY", "climb": "WATER WON'T CLIMB OUT",
                         "tunnel": "DIG A TUNNEL BACK", "slope": "A GENTLE SLOPE", "gravity": "GRAVITY DOES THE WORK",
                         "out": "WATER OUT. NO PUMP.", "hand": "BY HAND, IN THE HEAT", "min20": "20 MIN AT A TIME",
                         "shafts": "SHAFTS FROM THE TOP", "air": "AIR + LIGHT", "rock": "HAUL UP THE ROCK",
                         "dotted": "A DOTTED LINE", "owners": "200 OWNERS", "now": "EVERYONE WANTS IT NOW",
                         "time": "SHARE IT BY TIME", "half": "30 MIN EACH", "sundial": "SUNDIAL BY DAY",
                         "stars": "STARS BY NIGHT", "s1": "1  DRINKING", "s2": "2  BATHS", "s3": "3  WASHING",
                         "s4": "4  PALMS", "outbub": "ALMOST OUT!", "seven": "7:00 AM"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: ماتشو بيتشو"),
                      "stat": [("3,000+", "فلج شغال"), ("60", "متر عمق البير"), ("15", "قرن")],
                      "L": {"nopump": "من غير طلمبة", "nopower": "ولا كهربا", "years": "خمستاشر قرن",
                            "name": "فلج عماني", "rain": "المطر نادر", "deep": "المية مستخبية في الصخر",
                            "mother": "البير الأم", "m60": "لحد 60 متر", "miles": "القرية بعيدة",
                            "climb": "المية مش هتطلع", "tunnel": "نفق راجع للبير", "slope": "ميل خفيف",
                            "gravity": "الجاذبية بتشتغل", "out": "المية طلعت من غير طلمبة", "hand": "بالإيد وفي الحر",
                            "min20": "20 دقيقة بس", "shafts": "آبار من فوق", "air": "هوا ونور",
                            "rock": "طلّع الصخر", "dotted": "خط منقط", "owners": "200 صاحب أرض",
                            "now": "كله عايزها حالًا", "time": "قسّمها بالوقت", "half": "نص ساعة لكل دور",
                            "sundial": "المزولة بالنهار", "stars": "النجوم بالليل", "s1": "الشرب الأول",
                            "s2": "بعدين الاستحمام", "s3": "بعدين الغسيل", "s4": "وفي الآخر النخل", "outbub": "خارج أهو!",
                            "seven": "7:00"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "stream": ("hook", "STREAM", 0.1), "desert": ("hook", "DESERT", 0.25), "pump": ("hook", "PUMP", 0.38),
            "power": ("hook", "POWER", 0.48), "centuries": ("hook", "CENTURIES", 0.62), "congrats": ("hook", "CONGRATS", 0.72),
            "omani": ("hook", "OMANI", 0.88),
            "rains": ("break1", "RAINS", 0.25), "deep": ("break1", "DEEP", 0.65), "mountains": ("break1", "MOUNTAINS", 0.9),
            "dig": ("fix1", "DIG", 0.1), "mother": ("fix1", "MOTHER", 0.35), "sixty": ("fix1", "SIXTY", 0.75),
            "village": ("break2", "VILLAGE", 0.15), "miles": ("break2", "MILES", 0.35), "climb": ("break2", "CLIMB", 0.7),
            "tunnel": ("fix2", "TUNNEL", 0.2), "slope": ("fix2", "SLOPE", 0.45), "gentle": ("fix2", "GENTLE", 0.55),
            "gravity": ("fix2", "GRAVITY", 0.7), "out": ("fix2", "OUT", 0.92),
            "hand": ("break3", "HAND", 0.2), "heat": ("break3", "HEAT", 0.45), "twenty": ("break3", "TWENTY", 0.7),
            "minutes": ("break3", "MINUTES", 0.8),
            "shafts": ("fix3", "SHAFTS", 0.15), "air": ("fix3", "AIR", 0.3), "rock": ("fix3", "ROCK", 0.45),
            "plane": ("fix3", "PLANE", 0.65), "dotted": ("fix3", "DOTTED", 0.85),
            "one": ("break4", "ONE", 0.1), "hundred": ("break4", "HUNDRED", 0.4), "wants": ("break4", "WANTS", 0.85),
            "share": ("fix4", "SHARE", 0.1), "half": ("fix4", "HALF", 0.3), "sundial": ("fix4", "SUNDIAL", 0.5),
            "shadow": ("fix4", "SHADOW", 0.6), "stars": ("fix4", "STARS", 0.85), "night": ("fix4", "NIGHT", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "village2": ("reveal", "VILLAGE", 0.2), "drinking": ("reveal", "DRINKING", 0.35), "baths": ("reveal", "BATHS", 0.55),
            "washing": ("reveal", "WASHING", 0.75), "palms": ("reveal", "PALMS", 0.92),
            "s1": ("stat", "THREE", 0.04), "s2": ("stat", "SIXTY", 0.4), "s3": ("stat", "FIFTEEN", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "fights": ("tag", "FIGHTS", 0.35), "family": ("tag", "FAMILY", 0.5), "bathroom": ("tag", "BATHROOM", 0.75),
            "seven": ("tag", "SEVEN", 0.88)})
        T["night0"] = min(T["stars"], T["night"]) - 0.3
        # ---- sets
        self.cut(s("break1") - 0.12, "section", 1)
        self.cut(s("break3") - 0.12, "dig", -1)
        self.cut(T["plane"] - 0.12, "aerial", 1)
        self.cut(s("break4") - 0.12, "share", -1)
        self.cut(s("reveal") - 0.12, "oasis", 1)
        self.cut(s("tag") - 0.2, "bath", -1)
        # ---- oasis camera
        cm = Camera(-80, -230, 1.05)
        cm.key(0.05, 60, -230, 1.0, 3.5).key(T["congrats"], 120, -240, 0.95, 2.0)
        cm.key(s("reveal") - 0.12, -60, -230, 1.0, 0.0).key(T["drinking"] - 0.2, 0, -230, 1.05, 0.5)
        cm.key(T["baths"] - 0.25, 380, -230, 1.05, 0.5).key(T["washing"] - 0.25, 720, -230, 1.05, 0.5)
        cm.key(T["palms"] - 0.25, 1080, -260, 1.0, 0.5)
        cm.key(s("stat") - 0.12, 420, -300, 0.72, 0.0)
        cm.key(s("closer") - 0.1, 260, -250, 0.86, 0.0).key(self.duration, 300, -250, 0.9, 3.0)
        self.cam = cm
        # ---- section camera
        cs = Camera(-700, 60, 0.62)
        cs.key(T["deep"] - 0.3, -620, 120, 0.66, 0.6)
        cs.key(s("fix1") - 0.12, -300, 150, 0.9, 0.0).key(s("fix1"), -300, 170, 0.92, 2.0)
        cs.key(s("break2") - 0.12, 420, 120, 0.44, 0.0).key(s("break2"), 460, 140, 0.44, 2.0)
        self.cam_sec = cs
        self.spans = [(T["mountains"], T["sixty"] + 0.3), (T["climb"], T["out"] + 0.3), (T["minutes"], T["dotted"] + 0.3),
                      (T["wants"], T["night"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 7), (T["dig"] + 0.2, 0.3, 6), (T["hand"], 0.3, 6), (T["wants"], 0.3, 6),
                       (s("closer") + 0.2, 0.35, 9), (T["bathroom"], 0.4, 6)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def far(self, c, t, cam, night=0.0):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=gy - 60)
        if night > 0:
            c.drawRect(R(0, 0, W, H), P("#020617", 0.85 * night))
            stars_sky(c, t, night)
        sun(c, 860 - cx * 0.03, gy - 470, 64, heat=0.6, a=1 - night)
        c.save()
        c.translate(W / 2 - cx * 0.08, gy - 40)
        v2.ridge(c, -1700, 1700, 0, 380, "#8E5A4A", "#5A3530", seed=21, step=110, rough=0.6)
        c.restore()
        c.save()
        c.translate(W / 2 - cx * 0.16, gy - 10)
        v2.ridge(c, -1700, 1700, 0, 200, "#6E4038", "#3E2420", seed=22, step=80, rough=0.7)
        c.restore()
        return gy

    def village(self, c, t, x0=300, n=6, lit=0.5):
        for i in range(n):
            mudhouse(c, x0 + i * 150, -40 - (i % 2) * 20, 130 + (i % 3) * 20, 110 + (i % 3) * 30, lit=lit, seed=i)
        fort_tower(c, x0 + n * 150 - 40, -40, 56, 260)

    # ------------------------------------------------------------------ set: oasis (hook, reveal, stat, closer)
    def draw_oasis(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        self.far(c, t, cam)
        self.view(c, cam)
        c.drawRect(R(-3000, -60, 6500, 3000), lin_paint(0, -60, 0, 700, [SAND, SAND_D, "#6B4524"]))
        for i in range(12):                                          # palms behind the channel
            px = -380 + i * 150 + (i % 3) * 30
            palm(c, px, -50 - (i % 2) * 10, 300 + (i % 4) * 45, sway=math.sin(t * 1.3 + i) * 0.3)
        self.village(c, t, x0=360, n=6, lit=0.45)
        for i in range(10):                                          # palms in front of the houses
            px = -200 + i * 190
            palm(c, px, -20, 360 + (i % 3) * 50, sway=math.sin(t * 1.1 + i * 2) * 0.3)
        fx_ = lerp(-480, 1600, e_out(prog(t, 0.0, 3.0))) if hook else None
        if not hook and t < s("stat") - 0.12:
            fx_ = None
        channel(c, -560, 2200, t, flow_x=fx_)
        mouth(c, -600)
        if hook:
            gk = 1 - prog(t, 2.6, 3.4)
            if gk > 0:
                splash(c, -540, 0, t, t - (t % 0.5), dur=0.5, n=10, speed=300)
        if not hook and s("reveal") - 0.12 <= t < s("stat") - 0.12:  # the stations along the channel
            jar(c, 0, -14, 1.3)
            c.drawRect(R(30, -60, 34, 46), P("#C2703D"))
            bath_hut(c, 380, -14, 220, 180)
            person(c, 700, -14, 130, "#DB2777", t, pose="duck", face=-1, hat="none", hair="#1C1917")
            for k in range(3):
                c.drawRect(R(600 + k * 70, -170, 50, 70), P(("#F8FAFC", "#60A5FA", "#F59E0B")[k]))
            c.drawLine(560, -172, 840, -172, P("#E5E7EB", stroke=3))
            gate = prog(t, T["palms"] - 0.2, T["palms"] + 0.3)
            c.drawRect(R(1040, -20 - 60 * gate, 70, 60), P("#7C5A3A"))
        c.restore()
        self.ui["cam"] = cam

    def ui_oasis(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            k1 = self.span(T["pump"] - 0.15, T["centuries"] - 0.05)
            if k1 > 0:
                c.drawCircle(320, 700, 110, P("#0B1220", 0.85 * k1))
                pump(c, 320, 700, 1.1, a=k1)
                c.drawCircle(320, 700, 100, P(WARN, k1, stroke=10))
                c.drawLine(250, 770, 390, 630, P(WARN, k1, stroke=12))
                v2.chip(c, 320, 860, self.L["nopump"], k1, accent=WARN, size=34)
            k2 = self.span(T["power"] - 0.15, T["centuries"] - 0.05)
            if k2 > 0:
                c.drawCircle(760, 700, 110, P("#0B1220", 0.85 * k2))
                plug_off(c, 760, 700, 1.1, a=k2)
                v2.chip(c, 760, 860, self.L["nopower"], k2, accent=WARN, size=34)
            self.chip(540, 420, "years", T["centuries"] - 0.1, T["omani"] - 0.1, accent=HILITE, size=46)
            self.chip(540, 420, "name", T["omani"] - 0.1, s("break1") + 0.1, accent=HILITE, size=46)
            return
        if tw < s("stat") - 0.12:
            for key, t0, t1 in (("s1", T["drinking"], T["baths"]), ("s2", T["baths"], T["washing"]),
                                ("s3", T["washing"], T["palms"]), ("s4", T["palms"], s("stat"))):
                self.chip(540, 420, key, t0 - 0.12, t1 - 0.12, accent=GOOD if key == "s4" else "#7DD3FC", size=46)

    # ------------------------------------------------------------------ set: section (break1, fix1, break2, fix2)
    MTN = [(-1800, -760), (-1500, -880), (-1250, -780), (-1000, -900), (-760, -620), (-560, -260), (-380, -20), (-300, 8)]
    AQ_TOP, AQ_BOT = 250.0, 350.0
    WELL_X = -300.0

    @staticmethod
    def surf(x):
        if x <= -300:
            return poly_y(Falaj.MTN, x)
        return 8 + 0.22 * (x + 300)

    def tunnel_pts(self, k=1.0):
        x0, y0 = self.WELL_X, 330.0
        x1 = 1263.0
        y1 = self.surf(x1)
        n = 30
        pts = []
        for i in range(n + 1):
            u = i / n
            if u > k:
                break
            pts.append((lerp(x0, x1, u), lerp(y0, y1, u)))
        return pts

    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam_sec.at(t)
        cx, cy, z = cam
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=(0 - cy) * z + H / 2 - 80)
        sun(c, 840, 300, 60, heat=1.0)
        self.view(c, cam)
        gp = skia.Path()
        gp.moveTo(-2600, 2600)
        gp.lineTo(-2600, -760)
        for x_, y_ in self.MTN:
            gp.lineTo(x_, y_)
        x = -300
        while x <= 2600:
            gp.lineTo(x, self.surf(x))
            x += 50
        gp.lineTo(2600, 2600)
        gp.close()
        c.drawPath(gp, lin_paint(0, -800, 0, 900, [ROCK, shade(ROCK, -0.25), ROCK_D]))
        c.save()
        c.clipPath(gp, doAntiAlias=True)
        for k in range(16):                                          # rock layers
            yy = -700 + k * 90
            c.drawLine(-2600, yy, 2600, yy + 260, P("#2E1A14", 0.25, stroke=6))
        sand = skia.Path()                                           # the sandy plain on top
        sand.moveTo(-420, 2600)
        x = -420
        while x <= 2600:
            sand.lineTo(x, self.surf(x))
            x += 50
        sand.lineTo(2600, 2600)
        sand.close()
        c.drawPath(sand, lin_paint(0, 0, 0, 260, [SAND, shade(SAND, -0.35)], a=0.75))
        aqk = clamp(0.35 + prog(t, T["deep"] - 0.3, T["deep"] + 0.3))
        aq = skia.Path()
        aq.moveTo(-2600, self.AQ_TOP)
        aq.lineTo(700, self.AQ_TOP + 30)
        aq.quadTo(820, self.AQ_TOP + 60, 700, self.AQ_BOT + 20)
        aq.lineTo(-2600, self.AQ_BOT)
        aq.close()
        c.drawPath(aq, lin_paint(0, self.AQ_TOP, 0, self.AQ_BOT, [AQUA, AQUA_D], a=0.85 * aqk))
        rng = random.Random(4)
        for _ in range(140):
            px_ = rng.uniform(-2000, 650)
            py_ = rng.uniform(self.AQ_TOP + 10, self.AQ_BOT - 6)
            c.drawCircle(px_, py_, rng.uniform(5, 10), P("#E0F2FE", 0.5 * aqk))
        if prog(t, T["deep"] - 0.3, T["deep"] + 0.3) > 0:
            add_glow(c, -700, 300, 520, "#38BDF8", 0.25 * prog(t, T["deep"] - 0.3, T["deep"] + 0.3))
        well = prog(t, T["dig"] - 0.2, T["mother"] + 0.4) if t >= s("fix1") - 0.12 else 0.0
        if well > 0:                                                 # the mother well
            wd = lerp(8, 330, e_io(well))
            c.drawRect(R(self.WELL_X - 26, 8, 52, wd - 8), P("#1A0F0A"))
            c.drawRect(R(self.WELL_X - 26, 8, 52, wd - 8), P("#5B3A22", stroke=6))
            if well >= 1:
                c.drawRect(R(self.WELL_X - 20, 285, 40, 45), P(AQUA, 0.95))
        tk = prog(t, T["tunnel"] - 0.3, T["slope"] + 0.2) if t >= s("fix2") - 0.12 else 0.0
        if tk > 0:                                                   # the tunnel, dug back from the village end
            full = self.tunnel_pts(1.0)
            n = len(full)
            m = max(2, int(n * tk))
            seg = full[n - m:]
            tp = skia.Path()
            tp.moveTo(*seg[0])
            for p_ in seg[1:]:
                tp.lineTo(*p_)
            c.drawPath(tp, P("#1A0F0A", stroke=44))
            c.drawPath(tp, P("#5B3A22", 0.6, stroke=50, blur=2))
            c.drawPath(tp, P("#1A0F0A", stroke=40))
        fk = prog(t, T["gravity"] - 0.3, T["out"] + 0.2) if t >= s("fix2") - 0.12 else 0.0
        if fk > 0:
            flow(c, self.tunnel_pts(1.0), AQUA, t, k=fk, w=22, speed=1.4)
        c.restore()
        x = 1263
        if fk >= 1 or t >= T["out"]:
            ch = skia.Path()
            ch.moveTo(1263, self.surf(1263))
            while x <= 2100:
                ch.lineTo(x, self.surf(x) - 6)
                x += 40
            c.drawPath(ch, P(AQUA, stroke=26))
        for i in range(5):                                           # the village down the slope
            hx = 1380 + i * 150
            mudhouse(c, hx, self.surf(hx) + 6, 120, 100 + (i % 2) * 30, lit=0.4, seed=i)
        green = prog(t, T["out"] - 0.2, T["out"] + 0.6) if t >= s("fix2") - 0.12 else 0.0
        for i in range(6):
            px = 1320 + i * 140
            palm(c, px, self.surf(px) + 4, 260 + (i % 3) * 40, sway=math.sin(t + i) * 0.3, a=0.35 + 0.65 * green)
        if t < s("fix1") - 0.12:                                     # one raindrop on hot sand
            dk = prog(t, T["rains"] - 0.6, T["rains"])
            if dk < 1:
                c.drawCircle(-150, lerp(-900, -12, dk ** 2), 16, P("#7DD3FC", 0.9))
            else:
                v2set.splash(c, -150, -6, t, T["rains"], dur=0.5, n=8, speed=200, col="#BAE6FD")
                add_glow(c, -150, -10, 60, "#FDBA74", 0.4 * (1 - prog(t, T["rains"], T["rains"] + 0.8)))
            heat_lines(c, -500, 300, -300, 0, t, a=0.8)
        if t >= s("fix1") - 0.12 and t < s("break2") - 0.12:         # crew and windlass at the well top
            windlass(c, self.WELL_X, 8, 1.0, t, turn=t * 0.6)
            person(c, self.WELL_X - 110, 8, 130, "#F5F5F4", t, pose="carry", face=1, hat="none", hair="#1C1917",
                   skin="#B07A4F", pants="#57534E")
            person(c, self.WELL_X + 110, 8, 124, "#E7E5E4", t, pose="look", face=-1, hat="none", hair="#1C1917",
                   skin="#9A6A44", pants="#44403C")
            rk = prog(t, T["sixty"] - 0.3, T["sixty"])
            if rk > 0:                                               # the 60 m ruler
                c.drawLine(self.WELL_X + 70, 8, self.WELL_X + 70, 8 + 322 * rk, P(HILITE, stroke=6))
                for j in range(7):
                    yy = 8 + j * 322 / 6.0
                    if yy <= 8 + 322 * rk:
                        c.drawLine(self.WELL_X + 60, yy, self.WELL_X + 82, yy, P(HILITE, stroke=5))
        if s("break2") - 0.12 <= t < s("fix2") - 0.12:               # water stuck at the bottom of the well
            uk = self.span(T["climb"] - 0.2, s("fix2") - 0.15)
            if uk > 0:
                arrow(c, self.WELL_X + 70, 300, self.WELL_X + 70, 60, WARN, a=uk, w=14, head=38)
                c.drawLine(self.WELL_X + 30, 220, self.WELL_X + 110, 140, P(WARN, uk, stroke=14))
        c.restore()
        self.ui["cam"] = cam

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam_sec.at(tw))
        if tw < s("fix1") - 0.12:
            self.chip(540, 420, "rain", T["rains"] - 0.2, T["deep"] - 0.15, accent="#FDBA74", size=40)
            self.chip(540, 420, "deep", T["deep"] - 0.15, s("fix1") - 0.15, accent="#7DD3FC", size=38)
            self.badge("alert", T["mountains"] + 0.05, s("fix1") - 0.2, x=880, y=520)
            self.red(T["mountains"] + 0.05, 1.2)
            return
        if tw < s("break2") - 0.12:
            wx, wy = self.at(cam, self.WELL_X, 180)
            self.label(wx, wy, 300, 560, "mother", T["mother"] - 0.15, s("break2") - 0.15, "#7DD3FC", size=38)
            rx, ry = self.at(cam, self.WELL_X + 70, 170)
            self.label(rx, ry, 780, 700, "m60", T["sixty"] - 0.15, s("break2") - 0.15, HILITE, size=36)
            self.badge("check", T["sixty"] + 0.1, s("break2") - 0.15, x=880, y=520)
            return
        if tw < s("fix2") - 0.12:
            vx, vy = self.at(cam, 1650, 380)
            self.label(vx, vy, 760, 560, "miles", T["miles"] - 0.2, s("fix2") - 0.15, "#E2E8F0", size=34)
            self.chip(540, 420, "climb", T["climb"] - 0.15, s("fix2") - 0.15, accent=WARN, size=38)
            self.badge("alert", T["climb"] + 0.05, s("fix2") - 0.2, x=880, y=520)
            self.red(T["climb"] + 0.05, 1.2)
            return
        self.chip(540, 420, "tunnel", T["tunnel"] - 0.15, T["slope"] - 0.1, accent="#E2E8F0", size=40)
        self.chip(540, 420, "slope", T["slope"] - 0.1, T["gravity"] - 0.1, accent=HILITE, size=40)
        self.chip(540, 420, "gravity", T["gravity"] - 0.1, T["out"] - 0.1, accent="#7DD3FC", size=40)
        self.chip(540, 420, "out", T["out"] - 0.1, s("break3") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["out"] + 0.1, s("break3") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: dig (break3, fix3)
    SHAFTS = (-560.0, -60.0, 440.0)

    def draw_dig(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        z = 1.0 if not fixed else lerp(1.0, 0.78, e_io(prog(t, s("fix3") - 0.1, T["air"])))
        cam = (0, -300, z)
        cx, cy, _ = cam
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=(-620 - cy) * z + H / 2)
        self.view(c, cam)
        c.drawRect(R(-2000, -620, 4000, 3000), lin_paint(0, -620, 0, 400, [shade(ROCK, 0.05), ROCK_D]))
        c.drawRect(R(-2000, -640, 4000, 30), P(SAND))
        for k in range(10):
            c.drawLine(-2000, -560 + k * 70, 2000, -520 + k * 70, P("#2E1A14", 0.25, stroke=5))
        c.drawRect(R(-1400, -110, 2100, 130), P("#120A06"))             # the tunnel
        c.drawRect(R(-1400, -110, 2100, 130), P("#3B2416", stroke=6))
        c.drawRect(R(-1400, 0, 2100, 20), P(AQUA, 0.5 if fixed else 0.25))
        lamp = (560, -80)
        add_glow(c, lamp[0], lamp[1], 220, "#FDBA74", 0.5)
        c.drawCircle(lamp[0], lamp[1], 10, P("#FDE68A"))
        pick_digger(c, 520, 20, 140, t, swing=1.0, sweat=0.0 if fixed else prog(t, T["heat"] - 0.3, T["heat"]))
        c.drawRect(R(690, -110, 30, 130), P("#4A2C22"))
        if not fixed:
            hk = prog(t, T["heat"] - 0.4, T["heat"])
            for i in range(5):
                xx = 200 + i * 80
                pth = skia.Path()
                pth.moveTo(xx, 0)
                for k in range(1, 6):
                    pth.lineTo(xx + math.sin(t * 6 + k + i) * 10, -k * 20)
                c.drawPath(pth, P("#FB923C", 0.6 * hk, stroke=5))
        else:
            for i, sx in enumerate(self.SHAFTS):
                k = prog(t, s("fix3") - 0.1 + i * 0.15, T["shafts"] + 0.3 + i * 0.15)
                if k <= 0:
                    continue
                top, bot = -620.0, -110.0
                c.drawRect(R(sx - 30, top, 60, (bot - top) * k), P("#120A06"))
                c.drawRect(R(sx - 30, top, 60, (bot - top) * k), P("#3B2416", stroke=5))
                c.drawOval(R(sx - 90, top - 30, 180, 40), P(shade(SAND, -0.2)))
                lk = prog(t, T["air"] - 0.3, T["air"] + 0.2) * (k >= 1)
                if lk > 0:
                    lp = skia.Path()
                    lp.moveTo(sx - 26, top)
                    lp.lineTo(sx + 26, top)
                    lp.lineTo(sx + 90, 20)
                    lp.lineTo(sx - 90, 20)
                    lp.close()
                    c.drawPath(lp, P("#FFE9B0", 0.22 * lk))
                    add_glow(c, sx, -40, 120, "#FFE9B0", 0.35 * lk)
                    for j in range(3):
                        q = (t * 0.9 + j / 3.0) % 1.0
                        c.drawLine(sx - 12 + j * 12, lerp(top, bot, q), sx - 12 + j * 12, lerp(top, bot, q) + 40,
                                   P("#BAE6FD", 0.8 * lk, stroke=5))
            rk = prog(t, T["rock"] - 0.3, T["rock"])
            if rk > 0:
                sx = self.SHAFTS[1]
                windlass(c, sx, -640, 1.0, t, turn=t * 0.8, a=rk)
                by = lerp(-120, -560, (math.sin(t * 1.6) * 0.5 + 0.5))
                basket(c, sx, by, 1.0, a=rk)
                c.drawLine(sx, -760, sx, by - 40, P("#D6C29A", rk, stroke=3))
                person(c, sx + 120, -640, 130, "#F5F5F4", t, pose="carry", face=-1, hat="none", hair="#1C1917",
                       skin="#B07A4F", pants="#57534E", a=rk)
        c.restore()
        self.ui["fixed"] = fixed

    def ui_dig(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 420, "hand", T["hand"] - 0.15, T["twenty"] - 0.15, accent="#FDBA74", size=40)
            k = self.span(T["twenty"] - 0.2, s("fix3") - 0.15)
            if k > 0:
                timer(c, 540, 640, 130, prog(tw, T["twenty"] - 0.2, s("fix3") - 0.2), a=k)
                v2.chip(c, 540, 420, self.L["min20"], k, accent=WARN, size=42)
            self.badge("alert", T["minutes"] + 0.05, s("fix3") - 0.2, x=880, y=520)
            self.red(T["minutes"] + 0.05, 1.2)
            return
        self.chip(540, 420, "shafts", T["shafts"] - 0.15, T["air"] - 0.1, accent=HILITE, size=40)
        self.chip(540, 420, "air", T["air"] - 0.1, T["rock"] - 0.1, accent="#BAE6FD", size=40)
        self.chip(540, 420, "rock", T["rock"] - 0.1, T["plane"] - 0.1, accent="#FDBA74", size=40)

    # ------------------------------------------------------------------ set: aerial (end of fix3)
    def draw_aerial(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#E9BC7C", "#D9A35E", "#C28A48"])
        rng = random.Random(8)
        for i in range(26):                                          # dune ripples
            y0 = rng.uniform(0, H)
            pth = skia.Path()
            pth.moveTo(-50, y0)
            pth.cubicTo(300, y0 - 60, 700, y0 + 60, W + 50, y0 - 20)
            c.drawPath(pth, P("#B9813F", 0.35, stroke=6))
        c.drawRect(R(0, 0, W, 300), lin_paint(0, 0, 0, 300, ["#6E4038", "#9A6448"]))
        ov = skia.Path()
        ov.addOval(R(380, 1150, 760, 420))
        c.drawPath(ov, P("#2F6B2A"))
        for k in range(30):
            ox, oy = 420 + (k * 53) % 680, 1180 + (k * 97) % 360
            c.drawCircle(ox, oy, 26, P("#1E4D1C"))
            c.drawCircle(ox - 6, oy - 6, 14, P("#3F8A36"))
        lk = prog(t, T["plane"] - 0.12, T["dotted"] + 0.2)
        n = 14
        for i in range(n):
            u = i / (n - 1.0)
            if u > lk:
                break
            x = lerp(260, 640, u) + math.sin(u * 5) * 40
            y = lerp(330, 1160, u)
            c.drawCircle(x, y, 34, P("#B98447"))
            c.drawCircle(x, y, 34, P("#8A5E2C", stroke=6))
            c.drawCircle(x, y, 13, P("#1A0F0A"))
        px = lerp(-200, W + 200, prog(t, T["plane"] - 0.4, s("break4")))
        plane_top(c, px + 120, 640, 0.9, a=0.25)
        plane_top(c, px, 560, 1.0)

    def ui_aerial(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 420, "dotted", T["plane"], s("break4") - 0.12, accent=HILITE, size=44)
        self.badge("check", T["dotted"] + 0.1, s("break4") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: share (break4, fix4, cta)
    GATES = (-480.0, -240.0, 0.0, 240.0, 480.0)

    def draw_share(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        night = prog(t, T["night0"], T["night0"] + 0.5) if fixed else 0.0
        cam = (0, -260, 1.0)
        self.far(c, t, cam, night=night)
        self.view(c, cam)
        c.drawRect(R(-3000, -80, 6000, 3000), lin_paint(0, -80, 0, 700, [SAND, SAND_D, "#6B4524"]))
        if night > 0:
            c.drawRect(R(-3000, -80, 6000, 3000), P("#020617", 0.55 * night))
        for i, gx in enumerate(self.GATES):                          # farm plots behind each gate
            c.drawRect(R(gx - 100, -250, 200, 170), P(FARM if i % 2 else shade(FARM, 0.12)))
            for k in range(4):
                c.drawLine(gx - 100, -230 + k * 40, gx + 100, -230 + k * 40, P("#2B5A20", 0.6, stroke=4))
            for k in range(2):
                palm(c, gx - 60 + k * 120, -250, 220 + (i + k) % 2 * 40, sway=math.sin(t + i + k) * 0.3)
        if night > 0:
            c.drawRect(R(-700, -700, 1400, 640), P("#020617", 0.45 * night))
        active = -1
        if not fixed:
            open_all = prog(t, T["hundred"] - 0.2, T["wants"])
        else:
            open_all = 0.0
            cyc = 0.62
            active = int(max(0.0, t - (s("fix4") - 0.1)) / cyc) % len(self.GATES)
        level = 1.0 - 0.75 * open_all
        channel(c, -900, 900, t, level=level)
        for i, gx in enumerate(self.GATES):
            op = open_all if not fixed else (1.0 if i == active else 0.0)
            c.drawRect(R(gx - 22, -60 - 50 * op, 44, 60), P("#7C5A3A"))
            if op > 0.5:
                c.drawRect(R(gx - 14, -80, 28, 70), P(AQUA, 0.9 if fixed else 0.45))
                if fixed:
                    add_glow(c, gx, -120, 110, "#7DD3FC", 0.4)
        if not fixed:
            hk = prog(t, T["hundred"] - 0.4, T["hundred"])
            for i in range(12):
                px = -560 + i * 100
                person(c, px, 150, 120 + (i % 3) * 10, ("#F5F5F4", "#E7E5E4", "#D6D3D1")[i % 3], t + i * 0.2,
                       pose="cheer" if hk > 0.5 else "stand", face=1, hat="none", hair="#1C1917", skin="#B07A4F",
                       pants="#57534E", a=hk)
        else:
            sk = prog(t, T["sundial"] - 0.3, T["sundial"]) * (1 - night)
            if sk > 0:
                ang = lerp(200, 340, prog(t, T["sundial"] - 0.3, T["night0"]))
                sundial(c, -330, 190, 1.0, t, ang, a=sk, glow=prog(t, T["shadow"] - 0.2, T["shadow"] + 0.2))
            if night > 0:
                st_x = lerp(-200, 120, prog(t, T["stars"] - 0.3, T["night"] + 0.6))
                add_glow(c, st_x, -760, 70, "#FDE68A", night)
                c.drawCircle(st_x, -760, 9, P("#FFFFFF", night))
        c.restore()
        self.ui["active"] = active

    def ui_share(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 420, "owners", T["hundred"] - 0.2, T["wants"] - 0.15, accent="#E2E8F0", size=42)
            self.chip(540, 420, "now", T["wants"] - 0.15, s("fix4") - 0.15, accent=WARN, size=38)
            self.badge("alert", T["wants"] + 0.05, s("fix4") - 0.2, x=880, y=520)
            self.red(T["wants"] + 0.05, 1.2)
            return
        if tw < s("cta") - 0.12:
            self.chip(540, 420, "time", T["share"] - 0.15, T["half"] - 0.1, accent="#7DD3FC", size=42)
            self.chip(540, 420, "half", T["half"] - 0.1, T["sundial"] - 0.15, accent=HILITE, size=42)
            self.chip(540, 420, "sundial", T["sundial"] - 0.15, T["night0"], accent="#FDE68A", size=42)
            self.chip(540, 420, "stars", T["night0"], s("cta") - 0.15, accent="#C7D2FE", size=42)
            self.badge("check", T["night"] + 0.1, s("cta") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: bath (tag)
    def draw_bath(self, c, t):
        T = self.T
        door_queue(c, t, rtl=self.rtl, bang=prog(t, T["bathroom"] - 0.2, T["bathroom"]))

    def ui_bath(self, c, t, tw):
        T = self.T
        self.chip(300, 680, "seven", T["family"] - 0.2, self.duration + 1, accent=WARN, size=36)
        k = self.span(T["seven"] - 0.1, self.duration + 1)
        if k > 0:
            bx, by = 770, 430
            sz = 44
            lab = self.L["outbub"]
            wdt = (arabic.width_ar(lab, sz * 1.15, "Tajawal-Black") if arabic.is_ar(lab) else text_width(lab, sz, "Poppins-Black")) + 70
            kk = e_back(clamp(k))
            c.save()
            c.translate(bx, by)
            c.scale(kk, kk)
            c.drawRRect(rr(-wdt / 2, -60, wdt, 110, 50), P("#F8FAFC"))
            tl_ = skia.Path()
            tl_.moveTo(-20, 46)
            tl_.lineTo(10, 46)
            tl_.lineTo(-10, 90)
            tl_.close()
            c.drawPath(tl_, P("#F8FAFC"))
            word(c, lab, 0, 14, sz, "#111827")
            c.restore()

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=H * 0.6)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(2.6, 61), -12), (0.1, sfx.whoosh(0.8, True, 62), -14), (T["pump"], sfx.buzz(0.3), -12),
              (T["power"], sfx.buzz(0.3), -12), (T["centuries"], sfx.sparkle(0.6, 8, 63), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 64), -9), (T["omani"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 65), -4), (T["rains"], sfx.tap(66), -6),
               (T["rains"] + 0.05, sfx.sizzle(0.4, 67), -14), (T["deep"], sfx.whirr(0.8), -14),
               (T["mountains"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 68), -4)]
        for k in range(6):
            ev.append((T["dig"] + k * 0.22, sfx.clank(500.0, 0.15, 69 + k), -14))
        ev += [(T["sixty"] + 0.1, sfx.ding(), -8), (T["sixty"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 75), -4), (T["miles"], sfx.whoosh(0.6, False, 76), -12),
               (T["climb"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["tunnel"], rumble(1.2, 77), -14),
               (T["gravity"], sfx.hiss(1.6, 78), -12), (T["out"] + 0.1, sfx.ding(), -8), (T["out"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, False, 79), -4)]
        for k in range(8):
            ev.append((s("break3") + 0.1 + k * 0.4, sfx.clank(640.0, 0.12, 80 + k), -15))
        ev += [(T["twenty"], sfx.tick(), -8), (T["minutes"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["shafts"], sfx.thud(0.3), -10), (T["air"], sfx.whoosh(0.7, False, 88), -12), (T["rock"], sfx.creak(0.8), -12),
               (T["plane"] - 0.12, sfx.whoosh(0.4, True, 89), -4), (T["plane"], sfx.whirr(1.4, 200.0, 260.0, 90), -12),
               (T["dotted"] + 0.1, sfx.ding(), -8), (T["dotted"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 91), -4), (T["hundred"], sfx.pop(92), -8),
               (T["wants"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["share"], sfx.click(93), -8), (T["half"], sfx.tick(), -8), (T["sundial"], sfx.sparkle(0.6, 8, 94), -10),
               (T["night0"], sfx.whoosh(0.6, False, 95), -12), (T["stars"], sfx.sparkle(0.8, 10, 96), -10),
               (T["night"] + 0.1, sfx.ding(), -8), (T["night"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(97), 0), (T["follow"] - 0.15, sfx.pop(98), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 99), -6), (T["drinking"], sfx.pop(100), -8),
               (T["baths"], sfx.pop(101), -8), (T["washing"], sfx.pop(102), -8), (T["palms"], sfx.pop(103), -6),
               (T["palms"] + 0.1, sfx.hiss(1.0, 104), -14)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 105), -6), (T["s1"], sfx.pop(106), -3), (T["s2"], sfx.pop(107), -3),
               (T["s3"], sfx.pop(108), -3)]
        ev += [(T["cong2"], sfx.pop(109), -2), (T["cong2"], sfx.sparkle(1.0, 14, 110), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 111), -6), (T["family"], sfx.tick(), -8)]
        for k in range(4):
            ev.append((T["bathroom"] - 0.2 + k * 0.16, sfx.thud(0.15, 112 + k), -8))
        ev += [(T["seven"] + 0.1, sfx.pop(116), -6)]
        return ev


def poly_y(pts, x):
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return lerp(y0, y1, (x - x0) / max(1e-6, x1 - x0))
    return pts[-1][1]


NAME = "falaj"
EPISODE = Falaj
