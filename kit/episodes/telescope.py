"""Episode 32 - A space telescope (the James Webb kind).  v2 look: deep space, a golden honeycomb mirror on a
five-layer sunshield, whip cuts to close-up boards.

Sets: space (the telescope unfolds in space; the Sun heats it until it glows, then the sunshield opens between them;
the stat and the closer), light (a far galaxy's light stretches into invisible heat; a gold coat bounces it into the
detector), rocket (a 6.5 m mirror over a 5.4 m rocket fairing; eighteen hexagons and the side wings fold back like a
drop-leaf table), focus (the view through it: eighteen blurry copies of one star; tiny motors nudge each segment until
they become one sharp star), map (Earth, Moon and the trip to the parking spot 1.5 million km away), deep (a deep field
of galaxies 13 billion years back; the tag's crosshair), room (the tag: the TV remote nobody can find).
"""
from v2_base import *  # noqa: F401,F403

GOLD = ["#FFE6A0", "#D99A1E", "#7A520C"]
SQ3 = math.sqrt(3.0)
HEXES = [(q, r) for q in range(-2, 3) for r in range(-2, 3) if abs(q + r) <= 2 and (q, r) != (0, 0)]
SPACE = {"top": "#02030A", "upper": "#050816", "mid": "#0B1030", "low": "#141A45", "horizon": "#1E2563",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def hex_path(cx, cy, r, sx=1.0):
    p = skia.Path()
    for i in range(6):
        a = math.radians(60 * i - 90)
        x, y = cx + r * math.cos(a) * sx, cy + r * math.sin(a)
        if i == 0:
            p.moveTo(x, y)
        else:
            p.lineTo(x, y)
    p.close()
    return p


def wing_of(q, r):
    u = q + r / 2.0
    return -1 if u < -1.25 else (1 if u > 1.25 else 0)


def mirror(c, x, y, size, fold=0.0, gold=1.0, glow=0.0, a=1.0, t=0.0, struts=1.0, lines=1.0):
    """The primary mirror: 18 gold hexagons around an empty centre.  fold 0..1 swings the two 3-segment side wings
    back about their hinges; gold 0..1 (0 = bare grey beryllium)."""
    if a <= 0:
        return
    th = math.radians(170 * e_io(clamp(fold)))
    ct = math.cos(th)
    hinge = 1.25 * SQ3 * size
    back, front = [], []
    for q, r in HEXES:
        hx, hy = SQ3 * size * (q + r / 2.0), 1.5 * size * r
        w = wing_of(q, r)
        sx = 1.0
        if w:
            hx = w * hinge + (hx - w * hinge) * ct
            sx = abs(ct)
        (back if (w and ct < 0) else front).append((hx, hy, sx, w))
    c.drawPath(hex_path(x, y, size * 0.95, 1.0), P("#1E293B", a))           # the dark backplane in the middle
    for lst, dark in ((back, 0.55), (front, 0.0)):
        for hx, hy, sx, w in lst:
            col = [mix(mix("#9CA3AF", g, gold), "#1F2937", dark) for g in GOLD]
            hp = hex_path(x + hx, y + hy, size * 0.94, max(0.05, sx))
            c.drawPath(hp, rad_paint(x + hx - size * 0.35 * sx, y + hy - size * 0.4, size * 1.5, col, a=a))
            if lines > 0:
                c.drawPath(hp, P("#3B2A0A", 0.55 * a * lines, stroke=3))
            if dark == 0 and gold > 0.3:
                sh = (t * 0.25 + (hx + hy) / 900.0) % 1.0
                c.save()
                c.clipPath(hp, skia.ClipOp.kIntersect, True)
                c.drawLine(x + hx - size + sh * size * 4 - size, y + hy + size, x + hx + sh * size * 4 - size, y + hy - size,
                           P("#FFFFFF", 0.35 * a * gold, stroke=size * 0.25))
                c.restore()
    if glow > 0:
        add_glow(c, x, y, size * 4.5, "#FF5A36", 0.6 * glow * a)
    if struts > 0:
        k = a * struts
        sx_, sy_ = x, y - size * 0.4
        for ex, ey in ((x - 2.1 * SQ3 * size * 0.55, y + 2.6 * size), (x + 2.1 * SQ3 * size * 0.55, y + 2.6 * size), (x, y - 3.3 * size)):
            c.drawLine(ex, ey, sx_, sy_, P("#CBD5E1", 0.85 * k, stroke=max(2.0, size * 0.07)))
        c.drawCircle(sx_, sy_, size * 0.32, rad_paint(sx_ - 5, sy_ - 5, size * 0.4, GOLD, a=k))


def shield(c, x, y, sc, k=1.0, hot=0.0, a=1.0):
    """The five-layer sunshield seen from a little above: a long diamond.  k 0..1 unfolds it."""
    if a <= 0 or k <= 0:
        return
    for i in range(5):
        kk = e_out(clamp(k * 1.25 - i * 0.06))
        if kk <= 0:
            continue
        sx, sy = lerp(0.1, 1.0, kk), lerp(0.4, 1.0, kk)
        dy = -i * 16 * sc * kk
        p = skia.Path()
        p.moveTo(x - 760 * sc * sx, y + dy)
        p.lineTo(x - 120 * sc * sx, y + dy + 150 * sc * sy)
        p.lineTo(x + 120 * sc * sx, y + dy + 150 * sc * sy)
        p.lineTo(x + 760 * sc * sx, y + dy)
        p.lineTo(x + 90 * sc * sx, y + dy - 120 * sc * sy)
        p.lineTo(x - 90 * sc * sx, y + dy - 120 * sc * sy)
        p.close()
        base = mix("#E9D5FF", "#F1F5F9", i / 4.0)
        if i == 0:
            base = mix(base, "#FB923C", hot)
        if i == 4:
            base = mix(base, "#93C5FD", 0.35 * hot)
        c.drawPath(p, lin_paint(x - 760 * sc, y, x + 760 * sc, y, [shade(base, -0.25), base, shade(base, -0.15)], a=a * (0.92 if i else 1)))
        c.drawPath(p, P("#6B5B95", 0.5 * a, stroke=2))


def telescope(c, x, y, sc, fold=0.0, shield_k=1.0, gold=1.0, glow=0.0, hot=0.0, t=0.0, a=1.0):
    """The whole observatory: shield below, a tower, the mirror above.  (x, y) = mirror centre."""
    sy = y + 330 * sc
    c.drawRRect(rr(x - 130 * sc, sy + 20 * sc, 260 * sc, 90 * sc, 14 * sc), P("#334155", a))           # the bus
    c.drawRect(R(x + 130 * sc, sy + 40 * sc, 240 * sc, 40 * sc), lin_paint(0, sy + 40 * sc, 0, sy + 80 * sc, ["#1D4ED8", "#1E3A8A"], a=a))
    shield(c, x, sy, sc, shield_k, hot, a)
    c.drawRect(R(x - 22 * sc, y + 150 * sc, 44 * sc, sy - y - 150 * sc), P("#94A3B8", a))           # the tower
    c.drawRRect(rr(x - 110 * sc, y + 110 * sc, 220 * sc, 120 * sc, 10 * sc), P("#475569", a))       # instruments
    mirror(c, x, y, 70 * sc, fold, gold, glow, a, t, struts=1.0 - fold)


def giraffe(c, x, y, h, a=1.0):
    """A giraffe standing on (x, y), h tall, facing left (for scale)."""
    if a <= 0:
        return
    u = h / 500.0
    col, sp = "#E8A33D", "#8A4B14"
    for lx in (-60, -30, 40, 70):
        c.drawRRect(rr(x + lx * u, y - 210 * u, 16 * u, 210 * u, 6 * u), P(col, a))
    c.drawOval(R(x - 90 * u, y - 290 * u, 190 * u, 110 * u), P(col, a))
    neck = skia.Path()
    neck.moveTo(x - 70 * u, y - 260 * u)
    neck.lineTo(x - 120 * u, y - 470 * u)
    neck.lineTo(x - 85 * u, y - 480 * u)
    neck.lineTo(x - 20 * u, y - 270 * u)
    neck.close()
    c.drawPath(neck, P(col, a))
    c.drawOval(R(x - 170 * u, y - 500 * u, 90 * u, 40 * u), P(col, a))
    for ox in (-110, -95):
        c.drawLine(x + ox * u, y - 495 * u, x + ox * u, y - 525 * u, P(sp, a, stroke=6 * u))
    c.drawCircle(x - 140 * u, y - 486 * u, 4 * u, P("#1F2937", a))
    rng = random.Random(3)
    for _ in range(14):
        c.drawCircle(x + rng.uniform(-70, 80) * u, y + rng.uniform(-280, -200) * u, rng.uniform(8, 14) * u, P(sp, 0.8 * a))
    for _ in range(6):
        f = rng.uniform(0.1, 0.8)
        c.drawCircle(x + lerp(-50, -100, f) * u, y + lerp(-280, -450, f) * u, 7 * u, P(sp, 0.8 * a))


def galaxy(c, x, y, r, rot, a=1.0, col1="#BFDBFE", col2="#A78BFA", arms=2):
    if a <= 0:
        return
    add_glow(c, x, y, r * 1.6, col2, 0.35 * a)
    rng = random.Random(int(r * 7))
    for arm in range(arms):
        for i in range(36):
            f = i / 36.0
            ang = rot + arm * 360.0 / arms + f * 300
            rr_ = r * f
            px = x + math.cos(math.radians(ang)) * rr_
            py = y + math.sin(math.radians(ang)) * rr_ * 0.55
            c.drawCircle(px + rng.uniform(-4, 4), py + rng.uniform(-3, 3), r * 0.05 * (1.2 - f), P(mix(col1, col2, f), 0.8 * a))
    add_glow(c, x, y, r * 0.35, "#FFF7D6", 0.9 * a)


def star_spikes(c, x, y, r, a=1.0, col="#FFFFFF"):
    """A sharp star with Webb's six long spikes and two short ones."""
    if a <= 0:
        return
    add_glow(c, x, y, r * 2.2, col, 0.7 * a)
    for i in range(6):
        ang = math.radians(90 + i * 60)
        c.drawLine(x - math.cos(ang) * r * 3.2, y - math.sin(ang) * r * 3.2, x + math.cos(ang) * r * 3.2, y + math.sin(ang) * r * 3.2,
                   P(col, 0.75 * a, stroke=max(1.5, r * 0.08)))
    c.drawLine(x - r * 1.6, y, x + r * 1.6, y, P(col, 0.6 * a, stroke=max(1.0, r * 0.05)))
    c.drawCircle(x, y, r * 0.28, P("#FFFFFF", a))


def wave(c, x0, y0, x1, y1, head, t, lam0, lam1, cols, amp=26.0, a=1.0, dash_from=2.0, w=8.0):
    """A light wave from (x0, y0) toward (x1, y1), drawn up to fraction head; wavelength grows lam0 -> lam1 and the
    colour runs through cols; from fraction dash_from on it is drawn dashed (invisible heat)."""
    L = math.hypot(x1 - x0, y1 - y0)
    if L <= 0 or head <= 0 or a <= 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    ph = -t * 9.0
    prev = None
    s = 0.0
    n = int(L * head / 6) + 1
    for i in range(n + 1):
        s = L * head * i / n
        f = s / L
        lam = lerp(lam0, lam1, f)
        ph += 2 * math.pi * (L * head / n) / lam
        px, py = x0 + ux * s + nx * math.sin(ph) * amp, y0 + uy * s + ny * math.sin(ph) * amp
        if prev is not None and not (f > dash_from and (i // 3) % 2):
            k = f * (len(cols) - 1)
            j = min(int(k), len(cols) - 2)
            col = mix(cols[j], cols[j + 1], k - j)
            c.drawLine(prev[0], prev[1], px, py, P(col, a, stroke=w))
        prev = (px, py)


def couch(c, x, y, w, a=1.0):
    c.drawRRect(rr(x - w / 2, y - 220, w, 150, 40), P("#7C3AED", a))
    c.drawRRect(rr(x - w / 2 - 30, y - 150, 80, 150, 30), P("#6D28D9", a))
    c.drawRRect(rr(x + w / 2 - 50, y - 150, 80, 150, 30), P("#6D28D9", a))
    c.drawRRect(rr(x - w / 2 + 40, y - 110, w - 80, 70, 24), P("#8B5CF6", a))
    for k in (-1, 1):
        c.drawRRect(rr(x + k * w * 0.22 - 110, y - 200, 220, 110, 30), P("#A78BFA", a))


def mom(c, x, y, h, t, a=1.0):
    """A mother with a headscarf, pointing."""
    person(c, x, y, h, "#DB2777", t, pose="point", face=-1, hat="none", hair="#3F2A1A", a=a)
    u = h / 140.0
    sc = skia.Path()
    sc.addCircle(x, y - 132 * u, 21 * u)
    c.drawPath(sc, P("#0EA5E9", a))
    c.drawCircle(x - 4 * u, y - 128 * u, 12 * u, P("#E8B48A", a))
    c.drawRRect(rr(x - 20 * u, y - 116 * u, 40 * u, 16 * u, 8 * u), P("#0EA5E9", a))


def bubble(c, x, y, s, p):
    if p <= 0:
        return
    k = e_back(clamp(p * 1.25))
    size = 42
    w = (arabic.width_ar(s, size * 1.15, "Tajawal-Black") if arabic.is_ar(s) else text_width(s, size, "Poppins-Black")) + 80
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    tail = skia.Path()
    tail.moveTo(w * 0.15, 40)
    tail.lineTo(w * 0.3, 100)
    tail.lineTo(w * 0.32, 40)
    tail.close()
    c.drawRRect(rr(-w / 2, -60, w, 120, 40), P("#000000", 0.35 * p, blur=14))
    c.drawPath(tail, P("#FFFFFF", p))
    c.drawRRect(rr(-w / 2, -60, w, 120, 40), P("#FFFFFF", p))
    word(c, s, 0, 16, size, "#0F172A", p)
    c.restore()


def dim_arrow(c, x0, x1, y, label, a=1.0, col="#F8FAFC"):
    """A width dimension: |<---->| with a label above."""
    if a <= 0:
        return
    c.drawLine(x0, y, x1, y, P(col, a, stroke=5))
    for xx, d in ((x0, 1), (x1, -1)):
        c.drawLine(xx, y - 22, xx, y + 22, P(col, a, stroke=5))
        p = skia.Path()
        p.moveTo(xx, y)
        p.lineTo(xx + d * 26, y - 12)
        p.lineTo(xx + d * 26, y + 12)
        p.close()
        c.drawPath(p, P(col, a))
    word(c, label, (x0 + x1) / 2, y - 26, 40, col, a)


# ====================================================================================== the episode
class Telescope(EpisodeV2):
    BUILD_NO = 32
    COVER_T = ("closer", 0.55)
    FIRST_SET = "space"
    CLEAR = "#02030A"
    TITLE = {"en": "SPACE TELESCOPE", "ar_sa": "تلسكوب فضائي"}
    EMPH = {"en": ["CONGRATS", "GOLDEN", "MIRROR", "GIRAFFE", "FOLD", "ORIGAMI", "OPEN", "SPACE", "TELESCOPE",
                   "OLDEST", "GALAXIES", "FAR", "LIGHT", "STRETCHED", "HEAT", "SEE", "COAT", "GOLD", "BOUNCES", "SIX",
                   "HALF", "METERS", "WIDE", "FIT", "ROCKET", "EIGHTEEN", "HEXAGONS", "SIDES", "TABLE", "SUN",
                   "WARMS", "GLOWS", "BLINDS", "SUNSHADE", "TENNIS", "COURT", "FIVE", "LAYERS", "HAIR", "BLURRY",
                   "STARS", "SHARP", "MOTORS", "NUDGE", "STEPS", "TEN", "THOUSAND", "ONE", "FOLLOW", "ROBOT",
                   "CAMEL", "JOCKEY", "PARK", "MILLION", "LOOK", "THIRTEEN", "BILLION", "YEARS", "FORTY-EIGHT",
                   "GRAMS", "MINUS", "SHADE", "YOURSELF", "REMOTE", "FIND"],
            "ar_sa": ["مبروك", "مراية", "دهب", "الزرافة", "وطبقتها", "الورق", "الفضا", "تلسكوب", "فضائي", "المجرات",
                      "بعيدة", "نورها", "حرارة", "تتشافش", "فتدهن", "الدهب", "بيرجع", "ستة", "متر", "عرضها",
                      "هتدخل", "صاروخ", "تمنتاشر", "خلية", "النحل", "جنابها", "الترابيزة", "الشمس", "بتسخن", "بينور",
                      "ويعمي", "شمسية", "تنس", "خمس", "طبقات", "الشعرة", "مغبشة", "نجمة", "فمواتير", "تزق", "واحدة",
                      "تابعني", "روبوت", "الهجن", "ركنه", "مليون", "مليار", "سنة", "جرام", "الصفر", "بإيدك",
                      "الريموت", "أمك", "أمين"]}
    KEYS = {"ar_sa": {
        ("hook", "GOLDEN"): "دهب", ("hook", "MIRROR"): "مراية", ("hook", "GIRAFFE"): "الزرافة",
        ("hook", "FOLD"): "وطبقتها", ("hook", "ORIGAMI"): "الورق", ("hook", "OPEN"): "وفتحتها",
        ("hook", "SPACE"): "الفضا", ("hook", "CONGRATS"): "مبروك", ("hook", "TELESCOPE"): "تلسكوب",
        ("break1", "GALAXIES"): "المجرات", ("break1", "FAR"): "بعيدة", ("break1", "LIGHT"): "نورها",
        ("break1", "STRETCHED"): "بيوصل", ("break1", "HEAT"): "حرارة", ("break1", "SEE"): "تتشافش",
        ("fix1", "COAT"): "فتدهن", ("fix1", "GOLD"): "دهب", ("fix1", "BOUNCES"): "بيرجع", ("fix1", "WELL"): "كويس",
        ("break2", "SIX"): "ستة", ("break2", "WIDE"): "عرضها", ("break2", "FIT"): "هتدخل", ("break2", "ROCKET"): "صاروخ",
        ("fix2", "EIGHTEEN"): "تمنتاشر", ("fix2", "HEXAGONS"): "خلية", ("fix2", "FOLD"): "وتطبق",
        ("fix2", "SIDES"): "جنابها", ("fix2", "TABLE"): "الترابيزة",
        ("break3", "SUN"): "الشمس", ("break3", "WARMS"): "بتسخن", ("break3", "GLOWS"): "بينور",
        ("break3", "BLINDS"): "ويعمي",
        ("fix3", "SUNSHADE"): "شمسية", ("fix3", "TENNIS"): "تنس", ("fix3", "FIVE"): "خمس", ("fix3", "LAYERS"): "طبقات",
        ("fix3", "HAIR"): "الشعرة",
        ("break4", "MIRRORS"): "مراية", ("break4", "BLURRY"): "مغبشة", ("break4", "STARS"): "نجمة",
        ("break4", "SHARP"): "صورة",
        ("fix4", "MOTORS"): "مواتير", ("fix4", "NUDGE"): "تزق", ("fix4", "STEPS"): "حتة", ("fix4", "BECOME"): "تبقى",
        ("fix4", "ONE"): "واحدة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PARK"): "ركنه", ("reveal", "MILLION"): "مليون", ("reveal", "AWAY"): "كيلو", ("reveal", "LOOK"): "وبص",
        ("reveal", "BILLION"): "مليار", ("reveal", "YEARS"): "سنة",
        ("stat", "SIX"): "ستة", ("stat", "FORTY"): "تمانية", ("stat", "MINUS"): "وميتين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "GALAXIES"): "مجرات", ("tag", "FIND"): "لاقي", ("tag", "REMOTE"): "الريموت", ("tag", "TV"): "امين"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a robot camel jockey"),
                   "stat": [("6.5 m", "MIRROR"), ("48 g", "OF GOLD"), ("-233°C", "IN THE SHADE")],
                   "L": {"mirror": "GOLDEN MIRROR", "giraffe": "TALLER THAN A GIRAFFE", "origami": "FOLDS LIKE ORIGAMI",
                         "tele": "YOUR SPACE TELESCOPE", "stretched": "LIGHT STRETCHED INTO HEAT",
                         "cantsee": "YOUR EYES CAN'T SEE IT", "gold": "GOLD BOUNCES HEAT", "w65": "6.5 m",
                         "w54": "ROCKET: 5.4 m", "nofit": "WON'T FIT", "hex": "18 HEXAGONS", "table": "SIDES FOLD BACK",
                         "fits": "IT FITS", "sun": "SUN", "glows": "IT GLOWS AND BLINDS ITSELF",
                         "shade": "SUNSHADE = A TENNIS COURT", "layers": "5 LAYERS, THIN AS A HAIR", "hot": "+85°C",
                         "cold": "-233°C", "blurry": "18 BLURRY STARS", "motors": "TINY MOTORS",
                         "steps": "STEPS 10,000x THINNER THAN A HAIR", "one": "ONE SHARP STAR", "earth": "EARTH",
                         "moon": "MOON", "l2": "1.5 MILLION KM", "back": "13 BILLION YEARS AGO",
                         "found": "GALAXY FOUND", "remote": "TV REMOTE", "notfound": "NOT FOUND", "safe": ""}},
            "ar_sa": {"follow": ("تابعني", "الجاي: روبوت سباق الهجن"),
                      "stat": [("6.5 م", "مراية"), ("48 جرام", "دهب"), ("233°", "تحت الصفر")],
                      "L": {"mirror": "مراية دهب", "giraffe": "أطول من الزرافة", "origami": "بتتطبق زي الورق",
                            "tele": "التلسكوب بتاعك", "stretched": "النور وصل حرارة", "cantsee": "العين ما تشوفهاش",
                            "gold": "الدهب بيرجّع الحرارة", "w65": "6.5 م", "w54": "الصاروخ: 5.4 م",
                            "nofit": "مش هتدخل", "hex": "18 حتة زي خلية النحل", "table": "الجناب بتتطبق لورا",
                            "fits": "دخلت", "sun": "الشمس", "glows": "بينوّر ويعمي نفسه",
                            "shade": "شمسية قد ملعب تنس", "layers": "5 طبقات زي الشعرة", "hot": "85°",
                            "cold": "233° تحت الصفر", "blurry": "18 نجمة مغبّشة", "motors": "مواتير صغيرة",
                            "steps": "حركة أرفع من الشعرة 10,000 مرة", "one": "نجمة واحدة واضحة", "earth": "الأرض",
                            "moon": "القمر", "l2": "مليون ونص كيلو", "back": "من 13 مليار سنة",
                            "found": "لقينا المجرة", "remote": "الريموت", "notfound": "مش لاقيه",
                            "safe": "حطيته في مكان أمين!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "golden": ("hook", "GOLDEN", 0.05), "mirror": ("hook", "MIRROR", 0.1), "giraffe": ("hook", "GIRAFFE", 0.25),
            "fold": ("hook", "FOLD", 0.35), "origami": ("hook", "ORIGAMI", 0.45), "open": ("hook", "OPEN", 0.55),
            "space": ("hook", "SPACE", 0.62), "congrats": ("hook", "CONGRATS", 0.7), "tele": ("hook", "TELESCOPE", 0.9),
            "galaxies": ("break1", "GALAXIES", 0.2), "far": ("break1", "FAR", 0.35), "light": ("break1", "LIGHT", 0.45),
            "stretched": ("break1", "STRETCHED", 0.6), "heat": ("break1", "HEAT", 0.75), "see": ("break1", "SEE", 0.95),
            "coat": ("fix1", "COAT", 0.1), "gold": ("fix1", "GOLD", 0.35), "bounces": ("fix1", "BOUNCES", 0.6),
            "well": ("fix1", "WELL", 0.9),
            "six": ("break2", "SIX", 0.2), "wide": ("break2", "WIDE", 0.5), "fit": ("break2", "FIT", 0.7),
            "rocket": ("break2", "ROCKET", 0.9),
            "eighteen": ("fix2", "EIGHTEEN", 0.2), "hexagons": ("fix2", "HEXAGONS", 0.35), "fold2": ("fix2", "FOLD", 0.55),
            "sides": ("fix2", "SIDES", 0.65), "table": ("fix2", "TABLE", 0.9),
            "sun": ("break3", "SUN", 0.1), "warms": ("break3", "WARMS", 0.25), "glows": ("break3", "GLOWS", 0.7),
            "blinds": ("break3", "BLINDS", 0.85),
            "sunshade": ("fix3", "SUNSHADE", 0.15), "tennis": ("fix3", "TENNIS", 0.4), "five": ("fix3", "FIVE", 0.6),
            "layers": ("fix3", "LAYERS", 0.7), "hair": ("fix3", "HAIR", 0.95),
            "mirrors": ("break4", "MIRRORS", 0.2), "blurry": ("break4", "BLURRY", 0.5), "stars": ("break4", "STARS", 0.6),
            "sharp": ("break4", "SHARP", 0.85),
            "motors": ("fix4", "MOTORS", 0.1), "nudge": ("fix4", "NUDGE", 0.2), "steps": ("fix4", "STEPS", 0.35),
            "become": ("fix4", "BECOME", 0.85), "one": ("fix4", "ONE", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "park": ("reveal", "PARK", 0.1), "million": ("reveal", "MILLION", 0.25), "away": ("reveal", "AWAY", 0.5),
            "look": ("reveal", "LOOK", 0.6), "billion": ("reveal", "BILLION", 0.8), "years": ("reveal", "YEARS", 0.95),
            "s1": ("stat", "SIX", 0.04), "s2": ("stat", "FORTY", 0.35), "s3": ("stat", "MINUS", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "tgal": ("tag", "GALAXIES", 0.1), "find": ("tag", "FIND", 0.6), "remote": ("tag", "REMOTE", 0.75),
            "safe": ("tag", "TV", 0.9)})
        T["unf"] = min(T["open"], T["space"]) - 0.2                            # hook: it unfolds
        T["fold0"] = min(T["fold"], T["origami"]) - 0.15
        T["shut"] = min(T["fit"], T["rocket"]) - 0.2                           # break2: the mirror hits the rim
        T["wings"] = min(T["fold2"], T["sides"]) - 0.1
        T["drop"] = max(T["table"], T["wings"] + 0.9)
        T["sh0"] = T["sunshade"] - 0.15
        T["conv"] = T["nudge"]                                                  # fix4: the copies move in
        T["shp"] = max(T["become"], T["conv"] + 1.0)
        T["lk"] = max(T["look"] - 0.12, T["away"] + 0.4)                         # reveal: cut to the deep field
        T["room0"] = max(T["find"] - 0.2, T["tgal"] + 0.8)                       # tag: cut to the living room
        # ---- sets
        self.cut(s("break1") - 0.12, "light", 1)
        self.cut(s("break2") - 0.12, "rocket", -1)
        self.cut(s("break3") - 0.12, "space", 1)
        self.cut(s("break4") - 0.12, "focus", -1)
        self.cut(s("cta") - 0.12, "space", 1)
        self.cut(s("reveal") - 0.12, "map", -1)
        self.cut(T["lk"], "deep", 1)
        self.cut(s("stat") - 0.12, "space", -1)
        self.cut(s("tag") - 0.2, "deep", 1)
        self.cut(T["room0"], "room", -1)
        # ---- cameras (space set: the mirror centre is the origin)
        cm = Camera(0, -20, 1.35)
        cm.key(0.05, 0, -30, 1.4, 1.0).key(T["giraffe"] - 0.3, 110, 20, 1.05, 1.0)
        cm.key(T["unf"] - 0.2, 0, 60, 1.0, 1.4).key(T["tele"] - 0.3, 0, 90, 0.9, 1.4)
        cm.key(s("break3") - 0.12, -140, 120, 0.95, 0.0).key(s("break3"), -130, 110, 0.97, 3.0)
        cm.key(s("fix3") - 0.12, -60, 190, 0.78, 0.5)
        cm.key(s("cta") - 0.12, 0, 80, 0.8, 0.0)
        cm.key(s("stat") - 0.12, 0, -60, 0.72, 0.0).key(s("stat"), 0, -90, 0.74, 3.0)
        cm.key(s("closer") - 0.1, 0, 100, 0.95, 1.2)
        self.cam = cm
        # ---- tracks
        self.fold = Track(0.85).to(0.1, 0.85, 0.0).to(T["unf"], 0.0, 1.2)        # hook: wings open
        self.shk = Track(0.15).to(T["unf"] - 0.1, 1.0, 1.4)                      # hook: the shield opens
        self.giraffe_a = Track(0.0).to(T["giraffe"] - 0.1, 1.0, 0.3).to(T["fold0"], 0.0, 0.4)
        self.head = Track(0.0).to(T["light"] - 0.2, 1.0, max(1.0, T["heat"] - T["light"] + 0.4))
        self.goldk = Track(0.0).to(T["coat"], 1.0, max(0.7, T["gold"] - T["coat"] + 0.3))
        self.refl = Track(0.0).to(T["bounces"] - 0.1, 1.0, 0.7)
        self.shell = Track(32.0).to(s("break2") + 0.3, 9.0, max(0.6, T["shut"] - s("break2") - 0.3))   # halves swing in
        self.shell.to(T["shut"] + 0.1, 12.0, 0.25).to(T["drop"], 0.0, 0.8)
        self.wfold = Track(0.0).to(T["wings"], 1.0, 1.0)
        self.hlines = Track(0.0).to(T["eighteen"] - 0.1, 1.0, 0.5)
        self.heatk = Track(0.0).to(T["warms"] - 0.1, 1.0, max(0.8, T["glows"] - T["warms"])).to(T["sh0"] + 0.6, 0.0, 1.0)
        self.sh3 = Track(0.0).to(T["sh0"], 1.0, 1.6)
        self.conv = Track(0.0).to(T["conv"], 1.0, max(1.2, T["shp"] - T["conv"]))
        self.trip = Track(0.0).to(T["park"] - 0.1, 1.0, max(1.2, T["away"] - T["park"] + 0.3))
        self.spans = [(T["see"], T["well"] + 0.3), (T["rocket"], T["table"] + 0.3),
                      (T["blinds"], T["hair"] + 0.3), (T["sharp"], T["one"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 8), (T["see"], 0.3, 5), (T["shut"], 0.4, 12), (T["blinds"], 0.4, 8),
                       (T["sharp"], 0.3, 6), (s("closer") + 0.2, 0.35, 10)]
        rng = random.Random(32)
        self.blobs = [(SQ3 * 70 * (q + r / 2.0) * 2.3 + rng.uniform(-60, 60), 1.5 * 70 * r * 2.3 + rng.uniform(-60, 60))
                      for q, r in HEXES]
        self.gals = [(rng.uniform(-100, 1180), rng.uniform(100, 1700), rng.uniform(16, 78), rng.uniform(0, 360),
                      rng.choice((("#BFDBFE", "#A78BFA"), ("#FDE68A", "#F97316"), ("#FBCFE8", "#DB2777"), ("#A7F3D0", "#0EA5E9"))))
                     for _ in range(46)]

    # ------------------------------------------------------------------ helpers
    def starfield(self, c, t, a=1.0, dx=0.0, dy=0.0):
        v2.sky(c, W, H, 1.0, pal=SPACE, horizon_y=H * 1.2)
        add_glow(c, 820 + dx * 0.5, 420 + dy * 0.5, 620, "#5B21B6", 0.22 * a)       # faint nebulas
        add_glow(c, 160 + dx * 0.5, 1500 + dy * 0.5, 560, "#0E7490", 0.18 * a)
        v2.stars(c, W, H, t, a, dx=dx, dy=dy)

    # ------------------------------------------------------------------ set: space
    def draw_space(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        self.starfield(c, t, 1.0, dx=-cx * 0.05, dy=-cy * 0.05)
        in3 = s("break3") - 0.12 <= t < s("cta") - 0.12
        heat = self.heatk.at(t) if in3 else 0.0
        if in3:                                                         # the Sun, low on the left
            sx, sy = self.to_screen(cam, -700, 560)
            add_glow(c, sx, sy, 520, "#FFB347", 0.75)
            c.drawCircle(sx, sy, 150, P("#FFE7A3"))
            c.drawCircle(sx, sy, 118, P("#FFF7E0"))
        self.view(c, cam)
        if t < s("break1"):
            fold, shk = self.fold.at(t), self.shk.at(t)
        elif in3:
            fold, shk = 0.0, self.sh3.at(t)
        else:
            fold, shk = 0.0, 1.0
        hot = clamp(self.sh3.at(t)) if in3 else (1.0 if t >= s("cta") - 0.12 else 0.0)
        telescope(c, 0, 0, 1.0, fold=fold, shield_k=shk, gold=1.0, glow=heat * (1 - self.sh3.at(t) if in3 else 1), hot=hot * 0.8, t=t)
        if in3 and heat > 0.02:                                          # heat rays from the Sun
            shield_on = self.sh3.at(t)
            for i in range(6):
                ph = (t * 0.8 + i / 6.0) % 1.0
                x0, y0 = -640 + i * 30, 500 - i * 40
                x1, y1 = lerp(x0, -40 + i * 40, ph), lerp(y0, lerp(-60 + i * 50, 380, shield_on), ph)
                c.drawLine(x0, y0, x1, y1, P("#FB923C", 0.55 * (1 - ph) * max(heat, 0.6), stroke=10))
        if t < s("break1"):
            ga = self.giraffe_a.at(t)
            if ga > 0:
                giraffe(c, 420, 280, 480, ga)
        c.restore()
        self.ui["cam"] = cam
        if in3 and heat > 0.05:                                          # the glare it sees: its own heat
            k = heat * (1 - self.sh3.at(t))
            rng = random.Random(int(t * 30))
            c.drawRect(R(0, 0, W, H), P("#FF7A45", 0.18 * k))
            for _ in range(int(70 * k)):
                x, y = rng.uniform(0, W), rng.uniform(0, H)
                c.drawCircle(x, y, rng.uniform(2, 5), P("#FFFFFF", 0.35 * k))

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    def ui_space(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            x0, y0 = self.at(-150, -150)
            self.label(x0, y0, 280, 520, "mirror", T["mirror"] - 0.05, T["giraffe"] - 0.05, HILITE, size=34)
            self.chip(760, 1100, "giraffe", T["giraffe"] - 0.05, T["fold0"] + 0.2, accent="#E8A33D", size=34)
            self.chip(540, 1100, "origami", T["fold0"] + 0.1, T["congrats"], accent="#E9D5FF", size=36)
            self.chip(540, 470, "tele", T["tele"] - 0.15, s("break1") + 0.1, accent=ACCENT, size=38)
            return
        if s("break3") - 0.12 <= tw < s("cta") - 0.12:
            sx, sy = self.at(-700, 560)
            v2.chip(c, max(150, sx + 150), sy - 270, self.L["sun"], self.span(T["sun"] - 0.1, T["sh0"]), accent="#FFB347", size=36)
            self.chip(540, 470, "glows", T["glows"] - 0.1, s("fix3") - 0.15, accent=WARN, size=36)
            self.badge("alert", T["blinds"] + 0.1, s("fix3") - 0.2, x=880, y=330)
            self.red(T["blinds"] + 0.1, 1.6)
            self.chip(540, 470, "shade", T["tennis"] - 0.2, T["layers"] - 0.1, accent="#E9D5FF", size=36)
            self.chip(540, 470, "layers", T["layers"] - 0.05, s("break4") - 0.15, accent=GOOD, size=36)
            x0, y0 = self.at(-500, 380)
            v2.chip(c, x0, y0 + 90, self.L["hot"], self.span(T["five"], s("break4") - 0.15), accent="#FB923C", size=36)
            x1, y1 = self.at(420, 250)
            v2.chip(c, x1 + 40, y1 - 140, self.L["cold"], self.span(T["five"] + 0.3, s("break4") - 0.15), accent="#93C5FD", size=36)
            self.badge("check", T["hair"] + 0.1, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: light (break1, fix1)
    def draw_light(self, c, t):
        T, s = self.T, self.tl.s
        self.starfield(c, t, 1.0)
        galaxy(c, 230, 400, 150, t * 12, 1.0)
        gk = self.goldk.at(t)
        mx, my = 760, 1030                                             # the mirror: a concave dish facing up-left
        c.save()
        c.translate(mx, my)
        c.rotate(-45)
        dish = skia.Path()
        dish.moveTo(-230, -40)
        dish.quadTo(0, 60, 230, -40)
        dish.lineTo(230, -10)
        dish.quadTo(0, 90, -230, -10)
        dish.close()
        c.drawPath(dish, lin_paint(-230, 0, 230, 0, [mix("#9CA3AF", g, gk) for g in GOLD]))
        if 0 < gk < 1:
            c.drawLine(-230 + 460 * gk, -60, -230 + 460 * gk, 100, P("#FFFFFF", 0.7, stroke=10))
        c.restore()
        head = self.head.at(t)
        wave(c, 300, 470, mx - 40, my - 60, head, t, 34, 150, ["#93C5FD", "#60A5FA", "#F87171", "#991B1B"], amp=28,
             dash_from=0.62, w=8)
        rk = self.refl.at(t)
        if rk > 0:                                                     # bounced to the detector
            wave(c, mx - 40, my - 60, 330, 1100, rk, t, 150, 150, ["#FCD34D", "#FCD34D"], amp=26, w=9)
            c.drawRRect(rr(250, 1050, 160, 110, 18), P("#1E293B"))
            add_glow(c, 330, 1105, 120, "#FCD34D", 0.7 * rk)
            c.drawRRect(rr(270, 1070, 120, 70, 10), P(mix("#334155", "#FCD34D", rk)))
        else:
            c.drawRRect(rr(250, 1050, 160, 110, 18), P("#1E293B"))
            c.drawRRect(rr(270, 1070, 120, 70, 10), P("#334155"))
        if s("break1") <= t < s("fix1"):                                # an eye that sees nothing
            ek = self.span(T["see"] - 0.25, s("fix1") - 0.1)
            if ek > 0:
                ex, ey = 640, 700
                c.drawOval(R(ex - 70, ey - 40, 140, 80), P("#F8FAFC", ek))
                c.drawCircle(ex, ey, 26, P("#1E3A8A", ek))
                c.drawLine(ex - 90, ey - 70, ex + 90, ey + 70, P(WARN, ek, stroke=14))

    def ui_light(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 470, "stretched", T["stretched"] - 0.1, s("fix1") - 0.15, accent="#F87171", size=34)
            self.chip(640, 820, "cantsee", T["see"] - 0.1, s("fix1") - 0.15, accent=WARN, size=32)
            self.badge("alert", T["see"] + 0.1, s("fix1") - 0.2, x=880, y=330)
            self.red(T["see"] + 0.1, 1.5)
            return
        self.chip(540, 470, "gold", T["gold"] - 0.1, s("break2") - 0.15, accent=HILITE, size=38)
        self.badge("check", T["well"] + 0.05, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: rocket (break2, fix2)
    def draw_rocket(self, c, t):
        T, s = self.T, self.tl.s
        self.starfield(c, t, 0.6)
        base = 1150
        c.drawRect(R(230, base, 620, 900), lin_paint(230, 0, 850, 0, ["#64748B", "#CBD5E1", "#A3B1C2", "#475569"]))
        c.drawRect(R(230, base + 150, 620, 46), P("#1E293B", 0.85))
        c.drawRect(R(420, base - 30, 240, 30), P("#475569"))                       # the adapter it sits on
        wf = self.wfold.at(t)
        my = base - 330
        mirror(c, 540, my, 75.0, fold=wf, gold=1.0, a=1.0, t=t, struts=0.0, lines=self.hlines.at(t))
        ang = self.shell.at(t)                                                     # fairing halves: 32 = open
        hit = s("break2") <= t < s("fix2") and t >= T["shut"] - 0.05
        for side in (-1, 1):
            c.save()
            c.translate(540 + side * 310, base)
            c.rotate(side * ang)
            c.scale(-side, 1)
            p = skia.Path()
            p.moveTo(0, 0)
            p.lineTo(0, -470)
            p.cubicTo(0, -650, 160, -800, 310, -830)
            p.lineTo(310, -770)
            p.cubicTo(200, -740, 70, -620, 70, -450)
            p.lineTo(70, 0)
            p.close()
            c.drawPath(p, lin_paint(0, 0, 310, 0, ["#7C8BA1", "#C7D0DC", "#5B6B82"]))
            c.drawPath(p, P("#1E293B", 0.9, stroke=5))
            c.restore()
            if hit:
                add_glow(c, 540 - side * 260, my, 110, WARN, 0.8 * (1 - prog(t, T["shut"] + 0.5, s("fix2"))))
        self.ui["my"] = my

    def ui_rocket(self, c, t, tw):
        T, s = self.T, self.tl.s
        my = self.ui.get("my", 820)
        if tw < s("fix2") - 0.12:
            dim_arrow(c, 540 - 325, 540 + 325, my - 340, self.L["w65"], self.span(T["six"] - 0.1, s("fix2") - 0.15), HILITE)
            dim_arrow(c, 300, 780, 1222, self.L["w54"], self.span(T["fit"] - 0.3, s("fix2") - 0.15), "#0F172A")
            self.chip(540, 330, "nofit", T["fit"] - 0.05, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["rocket"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["rocket"] + 0.05, 1.5)
            return
        self.chip(540, 330, "hex", T["eighteen"] - 0.1, T["wings"] + 0.1, accent=HILITE, size=36)
        self.chip(540, 330, "table", T["wings"] + 0.15, T["drop"], accent="#E9D5FF", size=36)
        self.chip(540, 330, "fits", T["drop"] + 0.1, s("break3") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["drop"] + 0.2, s("break3") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: focus (break4, fix4)
    def draw_focus(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#000000", "#03040A", "#000000"])
        v2.stars(c, W, H, t, 0.35, seed=8)
        cx, cy = 540, 800
        c.drawCircle(cx, cy, 470, P("#1E293B", 0.9, stroke=4))
        c.drawLine(cx - 500, cy, cx + 500, cy, P("#334155", 0.6, stroke=2))
        c.drawLine(cx, cy - 500, cx, cy + 500, P("#334155", 0.6, stroke=2))
        k = self.conv.at(t) if t >= s("fix4") - 0.12 else 0.0
        app = prog(t, s("break4") - 0.1, T["blurry"])
        for i, (bx, by) in enumerate(self.blobs):
            bx, by = cx + bx * 0.75 * (1 - k), cy + by * 0.75 * (1 - k)
            r = lerp(52, 14, k)
            jit = (1 - k) * 4
            bx += math.sin(t * 5 + i) * jit
            by += math.cos(t * 4 + i * 2) * jit
            c.drawCircle(bx, by, r, rad_paint(bx, by, r, ["#FFFFFF", "#BFDBFE", "#1E3A8A"], a=clamp(app * 1.5 - i * 0.03) * (1 - k * 0.9)))
        if k > 0.7:
            star_spikes(c, cx, cy, lerp(20, 60, prog(t, T["shp"] - 0.3, T["shp"] + 0.3)), clamp((k - 0.7) * 3.4))
        # inset: one segment and the motors behind it
        ik = self.span(T["motors"] - 0.2, s("cta") - 0.2) if t >= s("fix4") - 0.12 else 0.0
        if ik > 0:
            ix, iy = 790, 1100
            c.drawRRect(rr(ix - 230, iy - 130, 460, 260, 30), P("#0F172A", 0.92 * ik))
            c.drawRRect(rr(ix - 230, iy - 130, 460, 260, 30), P("#475569", ik, stroke=4))
            step = math.floor(t * 4) % 3
            c.drawRRect(rr(ix - 170, iy - 70 - step * 4, 340, 34, 8), lin_paint(ix - 170, 0, ix + 170, 0, GOLD, a=ik))
            for j, dx in enumerate((-110, 0, 110)):
                hgt = 50 + ((step + j) % 3) * 4
                c.drawRRect(rr(ix + dx - 14, iy - 36 - step * 4, 28, hgt, 6), P("#94A3B8", ik))
                c.drawRRect(rr(ix + dx - 26, iy + 14, 52, 44, 8), P("#475569", ik))

    def ui_focus(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 330, "blurry", T["blurry"] - 0.1, s("fix4") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["sharp"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["sharp"] + 0.05, 1.5)
            return
        self.chip(790, 920, "motors", T["motors"] - 0.1, s("cta") - 0.2, accent="#94A3B8", size=32)
        self.chip(540, 330, "steps", T["steps"] - 0.1, T["become"] - 0.1, accent=HILITE, size=30)
        self.chip(540, 330, "one", T["shp"] - 0.1, s("cta") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["shp"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: map (reveal)
    def draw_map(self, c, t):
        T = self.T
        self.starfield(c, t, 0.8)
        add_glow(c, -260, 820, 700, "#FFB347", 0.6)
        ex, ey = 290, 820
        c.drawOval(R(ex - 250, ey - 100, 500, 200), P("#94A3B8", 0.4, stroke=3))
        ma = t * 25
        mx, my = ex + math.cos(math.radians(ma)) * 250, ey + math.sin(math.radians(ma)) * 100
        c.drawCircle(ex, ey, 120, rad_paint(ex - 40, ey - 40, 160, ["#93C5FD", "#2563EB", "#1E3A8A"]))
        c.drawPath(_land(ex, ey), P("#16A34A", 0.85))
        add_glow(c, ex, ey, 140, "#60A5FA", 0.3)
        c.drawCircle(mx, my, 30, rad_paint(mx - 8, my - 8, 40, ["#F8FAFC", "#94A3B8"]))
        lx = 920
        dashed(c, ex + 100, ey, lx, ey, "#CBD5E1", w=5, dash=18, gap=14, phase=-t * 40, a=0.8)
        c.drawCircle(lx, ey, 14, P(HILITE, 0.9, stroke=4))
        q = e_io(self.trip.at(t))
        px = lerp(ex + 110, lx, q)
        c.save()
        c.translate(px, ey - 10 - math.sin(q * math.pi) * 60)
        c.scale(0.22, 0.22)
        telescope(c, 0, 0, 1.0, t=t)
        c.restore()
        self.ui["earth"] = (ex, ey)
        self.ui["moon"] = (mx, my)

    def ui_map(self, c, t, tw):
        T, s = self.T, self.tl.s
        ex, ey = self.ui.get("earth", (300, 820))
        v2.chip(c, ex, ey + 170, self.L["earth"], self.span(s("reveal"), T["lk"]), accent="#60A5FA", size=32)
        dim_arrow(c, ex + 110, 920, ey - 160, self.L["l2"], self.span(T["million"] - 0.1, T["lk"] + 0.1), HILITE)

    # ------------------------------------------------------------------ set: deep (reveal, tag)
    def draw_deep(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#05030C", "#0A0618", "#04020A"])
        zt = t - (T["lk"] if t < s("stat") else s("tag") - 0.2)
        z = 1.0 + zt * 0.05
        c.save()
        c.translate(540, 900)
        c.scale(z, z)
        c.translate(-540, -900)
        v2.stars(c, W, H, t, 0.5, seed=21)
        for i, (gx, gy, r, rot, cols) in enumerate(self.gals):
            ap = clamp(zt * 3.0 - i * 0.04)
            if ap > 0:
                galaxy(c, gx, gy, r, rot + t * 6, ap, cols[0], cols[1], arms=2 if i % 3 else 3)
        for i in range(5):
            sx, sy = 140 + i * 210, 300 + (i * 397) % 1300
            star_spikes(c, sx, sy, 10 + (i % 2) * 6, 0.8)
        c.restore()
        if t >= s("tag") - 0.2:                                            # the crosshair locks onto a tiny red galaxy
            q = e_io(prog(t, s("tag"), T["tgal"] + 0.4))
            tx, ty = 700, 640
            x, y = lerp(300, tx, q), lerp(1100, ty, q)
            galaxy(c, tx, ty, 26, t * 20, 1.0, "#FCA5A5", "#DC2626")
            col = GOOD if q >= 1 else "#F8FAFC"
            c.drawCircle(x, y, 70, P(col, 0.9, stroke=6))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c.drawLine(x + dx * 50, y + dy * 50, x + dx * 100, y + dy * 100, P(col, 0.9, stroke=6))
            self.ui["lock"] = (x, y, q)

    def ui_deep(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("stat"):
            self.chip(540, 470, "back", T["billion"] - 0.2, s("stat") - 0.15, accent=HILITE, size=40)
            return
        x, y, q = self.ui.get("lock", (700, 640, 0))
        if q >= 1:
            v2.chip(c, x, y + 120, self.L["found"], self.span(T["tgal"] + 0.4, T["room0"] + 0.2), accent=GOOD, size=34)

    # ------------------------------------------------------------------ set: room (tag)
    def draw_room(self, c, t):
        T = self.T
        room(c, 0, 0, W, H, wall="#2A2F4A", floor="#3B4160", t=t, lamp=True, lamp_x=860)
        c.drawRRect(rr(120, 430, 520, 320, 16), P("#0B1020"))                   # the TV
        c.drawRRect(rr(140, 450, 480, 280, 10), P("#1E3A8A", 0.8))
        c.drawRect(R(360, 750, 40, 60), P("#111827"))
        couch(c, 540, 1230, 760)
        c.drawRRect(rr(330, 1110, 420, 30, 10), P("#7C4A2B"))                    # coffee table, behind the captions
        q = (t - T["room0"]) * 0.7                                               # the crosshair searches
        x = 540 + math.sin(q * 3.1) * 300
        y = 820 + math.sin(q * 2.3 + 1) * 180
        col = WARN if t >= T["remote"] else "#F8FAFC"
        c.drawCircle(x, y, 80, P(col, 0.9, stroke=6))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.drawLine(x + dx * 60, y + dy * 60, x + dx * 110, y + dy * 110, P(col, 0.9, stroke=6))
        if self.rtl:
            mom(c, 930, 1230, 200, t, a=prog(t, T["safe"] - 0.6, T["safe"] - 0.3))

    def ui_room(self, c, t, tw):
        T = self.T
        k = self.span(T["remote"] - 0.2, self.duration + 1, 0.25, 0.1)
        if k > 0:
            v2.chip(c, 540, 330, self.L["remote"] + ": " + self.L["notfound"] if not self.rtl else self.L["remote"] + ": " + self.L["notfound"],
                    k, accent=WARN, size=40)
        if self.rtl:
            bubble(c, 760, 760, self.L["safe"], self.span(T["safe"] - 0.3, self.duration + 1, 0.3, 0.1))

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 1.0, pal=SPACE, horizon_y=H * 1.2)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8), (0.1, sfx.hum(2.6, 55.0), -16), (T["mirror"], sfx.sparkle(0.7, 9, 61), -10),
              (T["giraffe"], sfx.pop(62), -9), (T["unf"], sfx.whirr(1.2, 120.0, 220.0, 63), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 64), -9), (T["tele"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 65), -4), (T["light"], sfx.riser(1.4), -14),
               (T["see"], sfx.womp(), -8), (T["see"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 66), -5), (T["coat"], sfx.sparkle(0.9, 12, 67), -10),
               (T["bounces"], sfx.ding(), -8), (T["well"] + 0.15, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 68), -4), (T["shut"], sfx.clank(), -6),
               (T["rocket"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 69), -5), (T["eighteen"], sfx.tick(), -8),
               (T["wings"], sfx.creak(0.9), -10), (T["drop"], sfx.whoosh(0.5, False, 70), -8),
               (T["drop"] + 0.7, sfx.thunk(71), -6), (T["drop"] + 0.9, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 72), -4), (T["warms"], sfx.sizzle(1.4, 73), -10),
               (T["blinds"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["sh0"], sfx.whirr(1.4, 140.0, 260.0, 74), -10), (T["hair"] + 0.15, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 75), -4), (T["blurry"], sfx.womp(), -10),
               (T["sharp"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["motors"], sfx.whirr(1.6, 400.0, 500.0, 76), -14), (T["steps"], sfx.tick(), -10),
               (T["shp"], sfx.sparkle(0.8, 12, 77), -8), (T["one"] + 0.15, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(78), 0), (T["follow"] - 0.15, sfx.pop(79), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 80), -6), (T["park"], sfx.riser(1.2), -12),
               (T["lk"], sfx.whoosh(0.5, True, 81), -6), (T["billion"], sfx.sparkle(1.0, 12, 82), -10)]
        ev += [(T["s1"], sfx.pop(83), -3), (T["s2"], sfx.pop(84), -3), (T["s3"], sfx.pop(85), -3)]
        ev += [(T["cong2"], sfx.pop(86), -2), (T["cong2"], sfx.sparkle(1.0, 14, 87), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 88), -6), (T["tgal"] + 0.4, sfx.beep(), -10),
               (T["room0"], sfx.whoosh(0.4, False, 89), -8), (T["remote"], sfx.buzz(), -10)]
        if self.rtl:
            ev += [(T["safe"] - 0.3, sfx.pop(90), -8)]
        return ev


def _land(ex, ey):
    p = skia.Path()
    p.moveTo(ex - 40, ey - 70)
    p.cubicTo(ex + 10, ey - 80, ex + 40, ey - 30, ex + 10, ey - 5)
    p.cubicTo(ex - 10, ey + 20, ex + 30, ey + 60, ex - 10, ey + 80)
    p.cubicTo(ex - 50, ey + 50, ex - 70, ey - 20, ex - 40, ey - 70)
    p.close()
    return p


NAME = "telescope"
EPISODE = Telescope
