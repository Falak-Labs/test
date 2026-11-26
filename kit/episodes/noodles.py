"""Episode 99 - instant noodles.  v2 look.

Sets: macro (hook: a noodle block, then one strand blown up huge: full of tiny holes; reveal: the strand in hot oil,
steam bursting out of it leaves the holes, then hot water rushes into them), fresh (break1: fresh noodles on a plate,
the days flip and mould spots grow), dry (fix1: noodles on a drying rack in the sun), pot (break2: a slow pot, a clock
spinning, a hungry kid), shed (fix2: a backyard shed at night, a wok of hot oil frying a noodle nest next to a
tempura prawn), kitchen (break3: a pot and a stove you still need), cup (fix3: kettle into a cup; break4: x-ray of the
cup bouncing in a truck, the block at the bottom cracks and water cannot get under it; fix4: the block wedged mid-cup,
water swirling underneath; cta, stat, closer: a steaming cup), tag (English: a 3-minute timer at 0:20 and someone
already crunching; Arabic: end of the month, three cups for breakfast, lunch and dinner).
"""
from v2_base import *  # noqa: F401,F403

GOLD = ("#FDE68A", "#FBBF24", "#D97706", "#92400E")
NIGHT3 = ["#0B1020", "#1E1B4B", "#312E81"]
WARMBG = ["#7C2D12", "#9A3412", "#C2410C"]
CUPC = ("#E3D3B4", "#CDB892", "#A98F63")
RED = "#DC2626"


def noodle_block(c, x, y, w, h, t, a=1.0, crack=0.0, rot=0.0):
    """A brick of wavy fried noodles centred at (x, y) (screen or world)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    body = rr(-w / 2, -h / 2, w, h, min(w, h) * 0.18)
    c.drawRRect(body, lin_paint(0, -h / 2, 0, h / 2, [GOLD[1], GOLD[2]], a=a))
    c.save()
    c.clipRRect(body, skia.ClipOp.kIntersect, True)
    rng = random.Random(3)
    rows = int(h / 12) + 2
    for r_ in range(rows):
        yy = -h / 2 + r_ * 12
        path = skia.Path()
        ph = rng.uniform(0, 6.28)
        path.moveTo(-w / 2 - 10, yy)
        for k in range(int(w / 8) + 3):
            xx = -w / 2 - 10 + k * 8
            path.lineTo(xx, yy + math.sin(xx * 0.09 + ph) * 6)
        c.drawPath(path, P(rng.choice(GOLD[:2]), 0.95 * a, stroke=5))
        c.drawPath(path, P(GOLD[3], 0.35 * a, stroke=1.5))
    if crack > 0:                                         # cracks across the block
        for k, (x0, y0, x1, y1) in enumerate(((-w * 0.1, -h / 2, w * 0.05, h / 2), (w * 0.25, -h / 2, w * 0.18, h * 0.2))):
            pth = skia.Path()
            pth.moveTo(x0, y0)
            for j in range(1, 7):
                u = j / 6
                pth.lineTo(lerp(x0, x1, u) + (9 if j % 2 else -9) * crack, lerp(y0, y1, u * crack))
            c.drawPath(pth, P("#1C1917", a, stroke=7 * crack))
    c.restore()
    c.restore()


def strand_macro(c, cx, cy, t, holes=1.0, steam=0.0, water=0.0, oil=0.0, a=1.0):
    """One noodle strand blown up across the frame (screen): a fat golden wave with tiny holes in it. steam 0..1 bubbles
    of steam bursting out (frying); water 0..1 hot water filling the holes; oil 0..1 a hot oil glow behind."""
    if a <= 0:
        return
    if oil > 0:
        c.drawRect(R(0, cy - 380, W, 760), lin_paint(0, cy - 380, 0, cy + 380, ["#78350F", "#B45309", "#78350F"], a=0.8 * oil * a))
    path = skia.Path()
    path.moveTo(-80, cy)
    pts = []
    for k in range(0, 41):
        x = -80 + k * 31
        y = cy + math.sin(k * 0.45 + 0.6) * 110 * (1 - 0.3 * water) + math.sin(t * 2 + k * 0.3) * 6 * water
        pts.append((x, y))
        path.lineTo(x, y)
    c.drawPath(path, P(GOLD[3], a, stroke=190))
    c.drawPath(path, P(mix("#C77D0A", "#E0A82E", 0.5 * water), a, stroke=170))
    c.drawPath(path, P("#F5C35B", 0.35 * a, stroke=40))
    rng = random.Random(6)
    for k in range(70):                                   # the pores
        i = rng.randrange(1, 39)
        px, py = pts[i]
        nx, ny = pts[i + 1]
        ang = math.atan2(ny - py, nx - px) + math.pi / 2
        off = rng.uniform(-62, 62)
        hx_, hy_ = px + math.cos(ang) * off + rng.uniform(-12, 12), py + math.sin(ang) * off
        r_ = rng.uniform(7, 15) * holes
        if r_ > 0.5:
            c.drawOval(R(hx_ - r_, hy_ - r_ * 0.7, 2 * r_, 1.4 * r_), P(mix("#451A03", "#38BDF8", water), a))
            if water > 0:
                c.drawOval(R(hx_ - r_ * 0.5, hy_ - r_ * 0.5, r_, r_ * 0.6), P("#E0F2FE", 0.7 * water * a))
        if steam > 0 and k % 2 == 0:                      # steam blasting out of the strand
            u = (t * 1.6 + rng.random()) % 1.0
            sx, sy = hx_ + math.cos(ang) * (20 + 160 * u) * (1 if off > 0 else -1), hy_ + math.sin(ang) * (20 + 160 * u) * (1 if off > 0 else -1)
            c.drawCircle(sx, sy - 60 * u, lerp(6, 22, u), P("#FFFFFF", 0.7 * steam * (1 - u) * a, stroke=4))
    if water > 0:                                         # hot water rushing in from around
        for k in range(30):
            u = (t * 1.2 + k / 30) % 1.0
            px, py = pts[(k * 7) % 40]
            sd = 1 if k % 2 else -1
            c.drawCircle(px + math.sin(k) * 20, py + sd * lerp(240, 70, u), 9, P("#7DD3FC", 0.8 * water * (1 - u * 0.4) * a))


def plate(c, x, y, s, t, days=0.0, mould=0.0):
    """Fresh noodles on a plate (screen); mould spots grow with mould."""
    c.drawOval(R(x - 260 * s, y - 70 * s, 520 * s, 140 * s), P("#94A3B8"))
    c.drawOval(R(x - 220 * s, y - 56 * s, 440 * s, 112 * s), P("#CBD5E1"))
    rng = random.Random(4)
    for k in range(26):                                   # a nest of pale fresh noodles
        path = skia.Path()
        x0 = x + rng.uniform(-170, 120) * s
        y0 = y + rng.uniform(-50, 20) * s
        path.moveTo(x0, y0)
        path.cubicTo(x0 + 40 * s, y0 - 60 * s, x0 + 80 * s, y0 + 40 * s, x0 + 120 * s, y0 - 20 * s)
        c.drawPath(path, P(mix("#F2C14E", "#A3B84A", 0.4 * mould), 1.0, stroke=9 * s))
    if mould > 0:
        for k in range(14):
            mx, my = x + rng.uniform(-170, 170) * s, y + rng.uniform(-60, 20) * s
            r_ = rng.uniform(10, 26) * s * mould
            c.drawCircle(mx, my, r_, P("#4D7C0F", 0.85))
            c.drawCircle(mx + r_ * 0.3, my - r_ * 0.2, r_ * 0.5, P("#84CC16", 0.8))


def calendar(c, x, y, s, day):
    c.drawRRect(rr(x - 110 * s, y - 120 * s, 220 * s, 240 * s, 20 * s), P("#F8FAFC"))
    c.drawRRect(rr(x - 110 * s, y - 120 * s, 220 * s, 70 * s, 20 * s), P(RED))
    text(c, str(int(day)), x, y + 70 * s, 120 * s, "#0F172A", "Poppins-Black")


def drying_rack(c, t, dry=0.0):
    vrect(c, 0, 0, W, H, ["#0369A1", "#0EA5E9", "#7DD3FC"])
    c.drawCircle(860, 330, 90, P("#FDE047"))
    add_glow(c, 860, 330, 320, "#FEF08A", 0.4)
    c.drawRect(R(0, 1150, W, H - 1150), P("#A16207"))
    for x in (170, 910):
        c.drawRect(R(x - 12, 560, 24, 600), P("#78350F"))
    for k, yy in enumerate((600, 780)):
        c.drawRect(R(150, yy, 780, 16), P("#92400E"))
        for j in range(22):                               # strands hanging over the poles
            x = 190 + j * 34
            ln = 150 + (j % 3) * 14
            col = mix("#FEF9C3", GOLD[1], dry)
            c.drawLine(x, yy + 10, x + math.sin(t * 1.5 + j) * 4, yy + 10 + ln, P(col, 1.0, stroke=7))
    rng = random.Random(2)
    for k in range(16):                                   # water leaving as vapour
        u = (t * 0.5 + rng.random()) % 1.0
        x = rng.uniform(190, 930)
        c.drawCircle(x, lerp(900, 480, u), lerp(4, 12, u), P("#E0F2FE", 0.7 * (1 - u) * (1 - dry * 0.7)))


def pot_scene(c, t, wait=0.0):
    vrect(c, 0, 0, W, H, ["#334155", "#1E293B"])
    c.drawRect(R(0, 1060, W, 60), P("#475569"))
    for i, fx_ in enumerate((-90, -30, 30, 90)):
        v2.flame(c, 420 + fx_, 1050, 30, 50, t + i * 0.3, 1.0, seed=i + 2, ang=-90)
    c.drawRRect(rr(240, 800, 360, 250, 30), lin_paint(240, 0, 600, 0, ["#64748B", "#CBD5E1", "#475569"]))
    c.drawRRect(rr(220, 780, 400, 40, 20), P("#94A3B8"))
    for i in range(4):                                    # slow bubbles
        u = (t * 0.4 + i * 0.25) % 1.0
        puff(c, 330 + i * 60, lerp(770, 560, u), lerp(20, 50, u), "#E2E8F0", 0.4 * (1 - u))
    cx, cy, r_ = 790, 640, 120                            # a clock spinning
    c.drawCircle(cx, cy, r_, P("#F8FAFC"))
    c.drawCircle(cx, cy, r_, P("#0F172A", 1.0, stroke=10))
    ang = math.radians(-90 + 360 * wait * 3)
    c.drawLine(cx, cy, cx + math.cos(ang) * r_ * 0.75, cy + math.sin(ang) * r_ * 0.75, P(RED, 1.0, stroke=8))
    ang2 = math.radians(-90 + 360 * wait * 0.25)
    c.drawLine(cx, cy, cx + math.cos(ang2) * r_ * 0.5, cy + math.sin(ang2) * r_ * 0.5, P("#0F172A", 1.0, stroke=12))
    person(c, 830, 1060, 260, "#F97316", t, pose="shrug" if wait > 0.5 else "stand", face=-1)


def shed_scene(c, t, fry=0.0):
    vrect(c, 0, 0, W, H, NIGHT3)
    v2.stars(c, W, H, t, 0.7)
    c.drawRect(R(0, 1120, W, H - 1120), P("#14532D"))
    sx, sy, sw, sh = 120, 520, 840, 600                   # the shed, front wall cut away
    roof = skia.Path()
    roof.moveTo(sx - 40, sy)
    roof.lineTo(sx + sw / 2, sy - 170)
    roof.lineTo(sx + sw + 40, sy)
    roof.close()
    c.drawPath(roof, P("#7C2D12"))
    c.drawRect(R(sx, sy, sw, sh), P("#3B2A1D"))
    for k in range(9):
        c.drawLine(sx + k * sw / 9, sy, sx + k * sw / 9, sy + sh, P("#2A1D14", 1.0, stroke=4))
    c.drawRect(R(sx + 40, sy + 40, sw - 80, sh - 40), P("#1C1917"))
    add_glow(c, 540, sy + 120, 260, "#FDE68A", 0.45)      # a bulb
    c.drawCircle(540, sy + 90, 18, P("#FEF9C3"))
    c.drawRect(R(300, 960, 480, 30), P("#57534E"))        # a bench and a gas ring
    for i, fx_ in enumerate((-40, 0, 40)):
        v2.flame(c, 540 + fx_, 955, 24, 40, t + i * 0.4, 1.0, seed=i + 5, ang=-90)
    wok = skia.Path()
    wok.moveTo(380, 860)
    wok.quadTo(540, 980, 700, 860)
    wok.close()
    c.drawPath(wok, P("#1F2937"))
    c.drawOval(R(380, 840, 320, 40), P("#B45309"))       # hot oil
    noodle_block(c, 520, 850, 170, 50, t, a=fry, rot=-4)
    rng = random.Random(7)
    for k in range(18):                                   # the oil boiling round the noodles
        u = (t * 2.2 + rng.random()) % 1.0
        c.drawCircle(rng.uniform(400, 680), 850 - u * 40, lerp(3, 9, u), P("#FEF3C7", 0.8 * fry * (1 - u)))
    c.drawOval(R(600, 830, 70, 30), P(GOLD[0]))          # a tempura prawn on the side
    c.drawOval(R(650, 838, 30, 16), P("#F97316"))
    person(c, 820, 1120, 300, "#E2E8F0", t, pose="look", face=-1, hair="#1F2937")   # the inventor, from the side


def kitchen_need(c, t, k=1.0):
    vrect(c, 0, 0, W, H, ["#3F2A1D", "#2A1B12"])
    c.drawRect(R(0, 1020, W, H - 1020), P("#78350F"))
    c.drawRRect(rr(140, 720, 360, 300, 16), P("#9CA3AF"))       # a stove
    for i in range(2):
        c.drawCircle(230 + i * 180, 760, 56, P("#1F2937"))
    c.drawRRect(rr(170, 840, 300, 150, 10), P("#9CA3AF"))
    c.drawRRect(rr(560, 700, 340, 200, 26), lin_paint(560, 0, 900, 0, ["#64748B", "#CBD5E1", "#475569"]))   # a pot
    c.drawRRect(rr(540, 680, 380, 36, 18), P("#94A3B8"))
    c.drawOval(R(600, 930, 260, 80), P("#CBD5E1"))       # a bowl
    if k > 0:
        c.drawLine(120, 640, lerp(120, 960, k), lerp(640, 1060, k), P(RED, 0.9, stroke=22))


def cup(c, x, y, s, t, xray=0.0, block="mid", water=0.0, steam=0.0, crack=0.0, swirl=0.0, lid=1.0, a=1.0):
    """The cup (screen, centred at the bottom middle x, y; 300 x 440 at s=1, wider at the top). xray 0..1 shows the
    inside; block "mid" (wedged half way up) or "bottom"."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    body = skia.Path()
    body.moveTo(-120, 0)
    body.lineTo(-160, -440)
    body.lineTo(160, -440)
    body.lineTo(120, 0)
    body.close()
    c.drawPath(body, lin_paint(-160, 0, 160, 0, [CUPC[2], CUPC[0], CUPC[1]], a=a))
    if xray > 0:
        c.save()
        c.clipPath(body, skia.ClipOp.kIntersect, True)
        c.drawPath(body, P("#0F172A", 0.85 * xray * a))
        if water > 0:
            wl = lerp(0, -380, water)
            c.drawRect(R(-170, wl, 340, -wl + 4), lin_paint(0, wl, 0, 0, ["#7DD3FC", "#0284C7"], a=0.75 * xray * a))
        by = -230 if block == "mid" else -60
        bw = 250 if block == "mid" else 230
        noodle_block(c, 0, by, bw, 110, t, a=xray * a, crack=crack)
        if swirl > 0 and block == "mid":                  # water circling underneath the block
            for k in range(14):
                ang = t * 3 + k * 0.45
                c.drawCircle(math.cos(ang) * 80, -90 + math.sin(ang) * 26, 9, P("#E0F2FE", 0.9 * swirl * xray * a))
        if block == "bottom" and water > 0:               # water stuck on top, dry underneath
            c.drawRect(R(-130, -120, 260, 120), P("#0F172A", 0.6 * xray * a))
        c.restore()
    else:
        c.drawRect(R(-150, -330, 300, 120), P(RED, a))   # the band
        c.drawRect(R(-150, -322, 300, 8), P("#FBBF24", a))
    c.drawPath(body, P("#94A3B8", a, stroke=4))
    if lid > 0:
        c.drawRRect(rr(-172, -462, 344, 30, 12), P("#E2E8F0", a * lid))
        c.drawRRect(rr(-172, -462, 344, 30, 12), P("#94A3B8", a * lid, stroke=3))
    c.restore()
    if steam > 0:
        for k in range(6):
            u = (t * 0.45 + k / 6) % 1.0
            puff(c, x + math.sin(t + k) * 40 * s, y - 470 * s - u * 300 * s, lerp(30, 80, u) * s, "#F8FAFC", 0.45 * (1 - u) * steam)


def kettle(c, x, y, s, pour=0.0, t=0.0):
    c.save()
    c.translate(x, y)
    c.rotate(-35 * pour)
    c.scale(s, s)
    c.drawRRect(rr(-120, -110, 240, 200, 60), lin_paint(-120, 0, 120, 0, ["#475569", "#94A3B8", "#334155"]))
    c.drawRRect(rr(-70, -150, 140, 50, 20), P("#334155", 1.0, stroke=14))
    sp = skia.Path()
    sp.moveTo(-110, -20)
    sp.lineTo(-210, -90)
    sp.lineTo(-200, -60)
    sp.lineTo(-110, 20)
    sp.close()
    c.drawPath(sp, P("#64748B"))
    c.restore()


def van(c, x, y, t, bump_k=0.0):
    """A delivery van bouncing on a bumpy road (screen); returns the y offset of its body."""
    dy = -abs(math.sin(t * 9)) * 26 * bump_k
    c.save()
    c.translate(x, y + dy)
    c.drawRRect(rr(-330, -330, 520, 290, 26), P("#F8FAFC"))
    c.drawRRect(rr(190, -260, 150, 220, 30), P("#E2E8F0"))
    c.drawRRect(rr(220, -240, 100, 90, 16), P("#93C5FD"))
    c.drawRect(R(-330, -150, 520, 26), P(RED))
    c.restore()
    for wx in (-220, 230):
        c.drawCircle(x + wx, y + 10, 50, P("#111827"))
        c.drawCircle(x + wx, y + 10, 20, P("#9CA3AF"))
    return dy


# ====================================================================================== the episode
class Noodles(EpisodeV2):
    BUILD_NO = 99
    FIRST_SET = "macro"
    CLEAR = "#0B0F1E"
    TITLE = {"en": "INSTANT NOODLES", "ar_sa": "النودلز"}
    EMPH = {"en": ["INSTANT", "NOODLES", "TINY", "HOLES", "PURPOSE", "FRESH", "BAD", "DAYS", "DRY", "WATER", "SPOILS",
                   "SLOW", "HUNGRY", "WAITING", "SHED", "MOMOFUKU", "ANDO", "FRIED", "TEMPURA", "POT", "STOVE", "CUP",
                   "HOT", "BUMPY", "CRACK", "BOTTOM", "BLOCK", "MID-CUP", "UNDERNEATH", "FOLLOW", "HUNDRED",
                   "KILOMETER", "FRYING", "SOAKS", "NINETEEN", "FIFTY-EIGHT", "YEAR", "BILLION", "CONGRATS", "YOURSELF",
                   "THREE", "MINUTES", "NOBODY"],
            "ar_sa": ["النودلز", "خروم", "بقصد", "الطازة", "تخرب", "الخروم", "فتنشّفها", "موية", "تطول", "والجوعان",
                      "يصبر", "مخزن", "أندو", "قلاها", "السمبوسة", "قدر", "وغاز", "كوب", "حارة", "تتكسر", "لتحت",
                      "الكتلة", "نص", "وتحتها", "متابعة", "مية", "جدة", "القلي", "تدخلها", "ثمانية", "المخزن",
                      "مليار", "مبروك", "طالب", "الشهر", "والعشا"]}
    KEYS = {"ar_sa": {
        ("hook", "NOODLES"): "النودلز", ("hook", "HOLES"): "خروم", ("hook", "PURPOSE"): "بقصد",
        ("break1", "FRESH"): "الطازة", ("break1", "BAD"): "تخرب", ("break1", "HOLES"): "الخروم",
        ("fix1", "DRY"): "تنشفها", ("fix1", "WATER"): "موية", ("fix1", "SPOILS"): "تخرب",
        ("break2", "SLOW"): "تطول", ("break2", "HUNGRY"): "الجوعان", ("break2", "WAITING"): "يصبر",
        ("fix2", "SHED"): "مخزن", ("fix2", "ANDO"): "أندو", ("fix2", "FRIED"): "قلاها", ("fix2", "TEMPURA"): "السمبوسة",
        ("break3", "POT"): "قدر", ("break3", "STOVE"): "غاز",
        ("fix3", "CUP"): "كوب", ("fix3", "HOT"): "حارة",
        ("break4", "BUMPY"): "الطريق", ("break4", "CRACK"): "تتكسر", ("break4", "BOTTOM"): "لتحت",
        ("fix4", "BLOCK"): "الكتلة", ("fix4", "MID"): "نص", ("fix4", "UNDERNEATH"): "تحتها",
        ("cta", "FOLLOW"): "متابعة",
        ("reveal", "FRYING"): "القلي", ("reveal", "HOLES"): "خروم", ("reveal", "SOAKS"): "تدخلها",
        ("stat", "NINETEEN"): "ثمانية", ("stat", "ONE"): "المخزن", ("stat", "HUNDRED"): "مليار",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "CUP"): "طالب", ("tag", "THREE"): "الشهر", ("tag", "NOBODY"): "العشا"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Build #100, the Jeddah Tower"),
                   "stat": [("1958", "THE FIRST ONE"), ("1 YEAR", "IN A SHED"), ("124 B", "SERVINGS IN 2025")],
                   "L": {"name": "INSTANT NOODLES", "holes": "FULL OF TINY HOLES", "fresh": "FRESH = BAD IN DAYS",
                         "what": "WHAT ARE THE HOLES FOR?", "dry": "DRY = NOTHING SPOILS", "slow": "DRY = COOKS SLOW",
                         "hungry": "HUNGRY!", "shed": "A BACKYARD SHED, 1958", "fried": "FRIED, LIKE TEMPURA",
                         "need": "STILL NEED A POT + STOVE", "cup": "IN A CUP", "hot": "JUST ADD HOT WATER",
                         "crack": "CRACKS ON THE ROAD", "bottom": "WATER CAN'T GET UNDER", "mid": "WEDGED MID-CUP",
                         "under": "ROOM FOR WATER UNDER", "steam": "FRYING BLASTS THE WATER OUT",
                         "soak": "HOT WATER SOAKS BACK IN", "wait": "WAIT 3 MINUTES", "nobody": "NOBODY WAITS",
                         "day": "DAY"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: البناء رقم 100، برج جدة"),
                      "stat": [("1958", "أول نودلز"), ("1", "سنة في المخزن"), ("124", "مليار وجبة 2025")],
                      "L": {"name": "النودلز", "holes": "مليانة خروم صغيرة", "fresh": "الطازة تخرب بكم يوم",
                            "what": "ليش الخروم؟", "dry": "ناشفة = ما تخرب", "slow": "الناشفة تطول",
                            "hungry": "جوعان!", "shed": "مخزن ورا البيت، 1958", "fried": "قلاها بالزيت",
                            "need": "لسا تبي قدر وغاز", "cup": "في كوب", "hot": "صب موية حارة",
                            "crack": "تتكسر في الطريق", "bottom": "الموية ما توصل تحت", "mid": "معلقة في نص الكوب",
                            "under": "فراغ للموية تحت", "steam": "القلي يطيّر الموية", "soak": "والحارة تدخل الخروم",
                            "wait": "آخر الشهر", "nobody": "فطور، غدا، عشا", "day": "يوم"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "noodles": ("hook", "NOODLES", 0.3), "holes": ("hook", "HOLES", 0.65), "purpose": ("hook", "PURPOSE", 0.9),
            "fresh": ("break1", "FRESH", 0.1), "bad": ("break1", "BAD", 0.35), "what": ("break1", "HOLES", 0.85),
            "dry": ("fix1", "DRY", 0.2), "water1": ("fix1", "WATER", 0.6), "spoils": ("fix1", "SPOILS", 0.9),
            "slow": ("break2", "SLOW", 0.35), "hungry": ("break2", "HUNGRY", 0.6), "waiting": ("break2", "WAITING", 0.9),
            "shed": ("fix2", "SHED", 0.2), "ando": ("fix2", "ANDO", 0.45), "fried": ("fix2", "FRIED", 0.7),
            "tempura": ("fix2", "TEMPURA", 0.9),
            "pot": ("break3", "POT", 0.6), "stove": ("break3", "STOVE", 0.9),
            "cup": ("fix3", "CUP", 0.4), "hot": ("fix3", "HOT", 0.8),
            "bumpy": ("break4", "BUMPY", 0.25), "crack": ("break4", "CRACK", 0.5), "bottom": ("break4", "BOTTOM", 0.9),
            "block": ("fix4", "BLOCK", 0.15), "mid": ("fix4", "MID", 0.4), "under": ("fix4", "UNDERNEATH", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "frying": ("reveal", "FRYING", 0.2), "holes2": ("reveal", "HOLES", 0.5), "soaks": ("reveal", "SOAKS", 0.85),
            "s1": ("stat", "NINETEEN", 0.05), "s2": ("stat", "ONE", 0.35), "s3": ("stat", "HUNDRED", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_cup": ("tag", "CUP", 0.1), "t_three": ("tag", "THREE", 0.35), "t_nobody": ("tag", "NOBODY", 0.75)})
        T["bad1"] = max(T["bad"], T["fresh"]) + 0.2
        T["dry1"] = max(T["dry"], T["water1"]) + 0.25
        T["slow1"] = max(T["slow"], s("break2") + 0.3) + 0.2
        T["fried1"] = max(T["fried"], T["ando"]) + 0.2
        T["pot1"] = max(T["pot"], s("break3") + 0.3) + 0.1
        T["hot1"] = max(T["hot"], T["cup"]) + 0.2
        T["crack1"] = max(T["crack"], T["bumpy"]) + 0.2
        T["mid1"] = max(T["mid"], T["block"]) + 0.25
        # ---- sets
        self.cut(s("break1") - 0.12, "fresh", 1)
        self.cut(s("fix1") - 0.12, "dry", -1)
        self.cut(s("break2") - 0.12, "pot", 1)
        self.cut(s("fix2") - 0.12, "shed", -1)
        self.cut(s("break3") - 0.12, "kitchen", 1)
        self.cut(s("fix3") - 0.12, "cup", -1)
        self.cut(s("reveal") - 0.12, "macro", 1)
        self.cut(s("stat") - 0.12, "cup", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        self.spans = [(T["bad1"], T["dry1"]), (T["slow1"], T["fried1"]), (T["pot1"], T["hot1"]), (T["crack1"], T["mid1"])]
        self.shakes = [(T["holes"], 0.3, 5), (T["bad1"], 0.3, 5), (T["slow1"], 0.3, 5), (T["pot1"], 0.3, 6),
                       (T["crack1"], 0.4, 9), (s("closer") + 0.2, 0.35, 8), (T["t_nobody"], 0.3, 7)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: macro (hook, reveal)
    def draw_macro(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        vrect(c, 0, 0, W, H, WARMBG if ph == "reveal" else ["#1C1917", "#292524", "#0C0A09"])
        if ph == "hook":                                  # a block, then a zoom into one strand
            z = e_io(prog(t, T["noodles"] - 0.1, T["holes"] + 0.2))
            if z < 1:
                c.save()
                c.translate(540, 720)
                c.scale(lerp(1.0, 4.0, z), lerp(1.0, 4.0, z))
                c.translate(-540, -720)
                noodle_block(c, 540, 720, 640, 400, t, a=1 - z)
                c.restore()
            if z > 0:
                strand_macro(c, 540, 720, t, holes=e_out(prog(t, T["holes"] - 0.1, T["holes"] + 0.4)), a=z)
        else:                                             # reveal: fry, then hot water soaks in
            steam = bump(t, s("reveal"), T["holes2"] + 0.6) if t < T["soaks"] else 0.0
            water = prog(t, T["soaks"] - 0.2, T["soaks"] + 0.6)
            holes = prog(t, T["frying"], T["holes2"])
            strand_macro(c, 540, 720, t, holes=holes, steam=steam, water=water, oil=1 - water)

    def ui_macro(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "holes", T["holes"] - 0.1, s("break1") + 0.1, accent=HILITE, size=50)
        else:
            self.chip(540, 300, "steam", T["frying"] - 0.2, T["soaks"] - 0.15, accent="#FDBA74", size=40)
            self.chip(540, 300, "soak", T["soaks"] - 0.15, s("stat") - 0.15, accent="#7DD3FC", size=42)

    # ------------------------------------------------------------------ set: fresh (break1)
    def draw_fresh(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#1E3A5F", "#274B73"])
        c.drawRect(R(0, 1000, W, H - 1000), lin_paint(0, 1000, 0, H, ["#7C4A2D", "#4A2C1A"]))
        days = lerp(1, 4, prog(t, T["fresh"], T["bad"] + 0.5))
        plate(c, 560, 930, 1.4, t, days=days, mould=prog(t, T["bad"] - 0.2, T["bad"] + 0.6))
        calendar(c, 230, 600, 1.0, days)

    def ui_fresh(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "fresh", T["fresh"] - 0.1, T["what"] - 0.25, accent=WARN, size=46)
        self.chip(540, 300, "what", T["what"] - 0.25, s("fix1") - 0.15, accent=HILITE, size=48)
        self.badge("alert", T["bad1"], s("fix1") - 0.2, x=920, y=440)
        self.red(T["bad1"], 1.2)

    # ------------------------------------------------------------------ set: dry (fix1)
    def draw_dry(self, c, t):
        T = self.T
        drying_rack(c, t, dry=prog(t, T["dry"], T["spoils"] + 0.3))

    def ui_dry(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "dry", T["dry"] - 0.1, s("break2") - 0.15, accent=GOOD, size=48)
        self.badge("check", T["dry1"], s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: pot (break2)
    def draw_pot(self, c, t):
        T, s = self.T, self.tl.s
        pot_scene(c, t, wait=prog(t, s("break2"), T["waiting"] + 0.5))

    def ui_pot(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "slow", T["slow"] - 0.2, T["hungry"] - 0.1, accent=WARN, size=48)
        self.chip(540, 300, "hungry", T["hungry"] - 0.1, s("fix2") - 0.15, accent=HILITE, size=56)
        self.badge("alert", T["slow1"], s("fix2") - 0.2, x=920, y=440)
        self.red(T["slow1"], 1.2)

    # ------------------------------------------------------------------ set: shed (fix2)
    def draw_shed(self, c, t):
        T = self.T
        shed_scene(c, t, fry=prog(t, T["fried"] - 0.3, T["fried"] + 0.2))

    def ui_shed(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "shed", T["shed"] - 0.2, T["fried"] - 0.15, accent="#FDE68A", size=46)
        self.chip(540, 300, "fried", T["fried"] - 0.15, s("break3") - 0.15, accent=GOOD, size=48)
        self.badge("check", T["fried1"], s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: kitchen (break3)
    def draw_kitchen(self, c, t):
        T = self.T
        kitchen_need(c, t, k=prog(t, T["stove"], T["stove"] + 0.4))

    def ui_kitchen(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "need", T["pot"] - 0.3, s("fix3") - 0.15, accent=WARN, size=44)
        self.badge("alert", T["pot1"], s("fix3") - 0.2, x=920, y=440)
        self.red(T["pot1"], 1.2)

    # ------------------------------------------------------------------ set: cup (fix3 .. cta, stat, closer)
    def draw_cup(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph in ("stat", "closer"):
            vrect(c, 0, 0, W, H, WARMBG)
            add_glow(c, 540, 820, 420, "#FDBA74", 0.4)
            cup(c, 540, 1180 if ph == "stat" else 1130, 1.2 if ph == "stat" else 1.35, t, lid=0.0, steam=1.0)
            noodle_block(c, 540, (1180 if ph == "stat" else 1130) - 440 * (1.2 if ph == "stat" else 1.35) + 6, 300, 60, t)
            if ph == "closer":                            # a fork lifting a bundle of noodles out of the cup
                lift = e_out(prog(t, s("closer"), s("closer") + 0.8))
                fy = lerp(560, 380, lift)
                c.drawLine(720, fy - 140, 590, fy, P("#CBD5E1", 1.0, stroke=16))
                for k in range(4):
                    c.drawLine(580 + k * 10, fy, 560 + k * 10, fy + 50, P("#CBD5E1", 1.0, stroke=7))
                for k in range(7):                        # wavy strands hanging down to the cup
                    pth = skia.Path()
                    x0 = 545 + k * 9
                    pth.moveTo(x0, fy + 40)
                    for j in range(1, 9):
                        pth.lineTo(x0 + math.sin(j * 1.3 + k) * 12, fy + 40 + j * (530 - fy) / 8)
                    c.drawPath(pth, P(GOLD[1] if k % 2 else GOLD[2], 1.0, stroke=7))
            return
        vrect(c, 0, 0, W, H, ["#1E293B", "#0F172A"])
        if ph == "fix3":
            c.drawRect(R(0, 1150, W, 60), P("#78350F"))
            pour = prog(t, T["hot"] - 0.4, T["hot"])
            kettle(c, 780, 600, 1.0, pour=pour, t=t)
            if pour > 0.6:
                c.drawLine(640, 560, 560, 760, P("#7DD3FC", 0.9, stroke=14))
            cup(c, 540, 1150, 1.1, t, lid=1 - prog(t, T["cup"], T["cup"] + 0.4), steam=prog(t, T["hot"], T["hot"] + 0.6))
            return
        if ph == "break4":                                # x-ray in a bouncing van
            c.drawRect(R(0, 1170, W, H - 1170), P("#374151"))
            for k in range(6):                            # bumps on the road
                bx = (k * 220 - t * 300) % (W + 220) - 110
                c.drawOval(R(bx - 60, 1150, 120, 40), P("#4B5563"))
            dy = van(c, 560, 1160, t, bump_k=1.0)
            cup(c, 470, 1080 + dy, 0.95, t, xray=1.0, block="bottom", water=prog(t, T["bottom"] - 0.4, T["bottom"]),
                crack=prog(t, T["crack"] - 0.1, T["crack"] + 0.3))
            return
        # fix4 and cta: the block wedged mid-cup, water swirling underneath
        cup(c, 540, 1150, 1.3, t, xray=1.0, block="mid", water=prog(t, T["mid"], T["under"]) * 0.9 + 0.05,
            swirl=prog(t, T["under"] - 0.3, T["under"] + 0.2))

    def ui_cup(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "fix3":
            self.chip(540, 300, "cup", T["cup"] - 0.2, T["hot"] - 0.15, accent=GOOD, size=52)
            self.chip(540, 300, "hot", T["hot"] - 0.15, s("break4") - 0.15, accent="#7DD3FC", size=48)
            self.badge("check", T["hot1"], s("break4") - 0.15, x=920, y=440)
        elif ph == "break4":
            self.chip(540, 300, "crack", T["crack"] - 0.2, T["bottom"] - 0.25, accent=WARN, size=46)
            self.chip(540, 300, "bottom", T["bottom"] - 0.25, s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["crack1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["crack1"], 1.2)
        elif ph in ("fix4", "cta"):
            self.chip(540, 300, "mid", T["block"] - 0.1, T["under"] - 0.2, accent=GOOD, size=48)
            self.chip(540, 300, "under", T["under"] - 0.2, s("cta") - 0.15, accent="#7DD3FC", size=46)
            self.badge("check", T["mid1"], s("cta") - 0.15, x=920, y=440)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#FDE68A", "#FCD34D"])
        c.drawRect(R(0, 1060, W, H - 1060), P("#B45309"))
        if not self.rtl:                                  # a 3-minute timer still at 2:40, and he is already crunching
            cx, cy, r_ = 780, 560, 130
            c.drawCircle(cx, cy, r_, P("#F8FAFC"))
            c.drawCircle(cx, cy, r_, P("#0F172A", 1.0, stroke=10))
            secs = 180 - 20 * prog(t, T["t_cup"], T["t_nobody"])
            text(c, f"{int(secs // 60)}:{int(secs % 60):02d}", cx, cy + 30, 80, "#0F172A", "Poppins-Black")
            cup(c, 330, 1060, 0.8, t, lid=0.4, steam=0.6)
            person(c, 560, 1060, 300, "#7C3AED", t, pose="cheer" if t > T["t_nobody"] else "stand", face=-1)
            if t > T["t_nobody"]:                         # crunch!
                for k in range(6):
                    u = (t * 3 + k / 6) % 1.0
                    c.drawRect(R(520 + math.cos(k) * 90 * u, 760 - 60 * u + 200 * u * u, 14, 8), P(GOLD[1], 1 - u))
        else:                                             # end of the month: three cups for three meals
            calendar(c, 820, 520, 1.0, 30)
            for k in range(3):
                cup(c, 220 + k * 230, 1060, 0.6, t, lid=1.0 if t < T["t_nobody"] else 0.0, steam=0.4 * (k == 1))
            person(c, 880, 1060, 260, "#0EA5E9", t, pose="shrug", face=-1)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "wait", T["t_cup"] - 0.1, T["t_nobody"] - 0.15, accent="#F8FAFC", size=48)
        self.chip(540, 300, "nobody", T["t_nobody"] - 0.15, self.duration + 1, accent=WARN, size=50)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1C1917", "#292524"])

    def draw_cover(self, c):
        """As the base, but the Arabic closer's pause ("ومبروك... كذا") is read as a comma on the cover."""
        from bik import cover
        self.draw_world(c, self.cover_time())
        closer = next((ln["text"] for ln in self.tl.lines if ln["label"] == "closer"), "")
        closer = closer.replace("...", "،").replace("،،", "،")
        small, name = cover.subject(self.lang, closer, self.TITLE.get(self.lang, self.TITLE["en"]))
        return cover.overlay(c, W, H, self.BUILD_NO, self.lang, small, name)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["noodles"], sfx.riser(1.0, 62), -12), (T["holes"], sfx.sparkle(1.0, 12, 63), -8),
              (T["purpose"], sfx.ding(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 64), -6), (T["bad1"], sfx.alarm(3, 820.0), -12), (T["bad"], sfx.womp(), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 65), -6), (T["dry1"], sfx.ding(), -8), (T["dry1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.45, True, 66), -6), (T["slow"], sfx.tick(), -8), (T["slow"] + 0.4, sfx.tick(), -8),
               (T["slow1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.45, False, 67), -6), (T["fried"], sfx.sizzle(1.4, 68), -8),
               (T["fried1"], sfx.ding(), -8), (T["fried1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 69), -6), (T["stove"], sfx.buzz(0.4), -12), (T["pot1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.45, False, 70), -6), (T["cup"], sfx.pop(71), -6), (T["hot"], sfx.hiss(1.2, 72), -12),
               (T["hot1"], sfx.ding(), -8), (T["hot1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["bumpy"], sfx.thud(0.3, 73), -6), (T["bumpy"] + 0.35, sfx.thud(0.3, 74), -6), (T["crack1"], sfx.snap(75), -4),
               (T["crack1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["block"], sfx.lock_click(76), -6), (T["mid1"], sfx.ding(), -8), (T["mid1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["frying"], sfx.sizzle(1.6, 95), -8),
               (T["soaks"], sfx.hiss(1.0, 96), -12)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, False, 97), -6), (T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3),
               (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 103), -6), (T["t_three"], sfx.tick(), -8), (T["t_nobody"], sfx.snap(104), -6),
               (T["t_nobody"] + 0.4, sfx.womp(), -8)]
        return ev


NAME = "noodles"
EPISODE = Noodles
