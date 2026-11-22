"""Episode 63 - A washing machine.  v2 look: a front-loading washer on bathroom tiles, shown in x-ray with its drum,
tub, springs, shock absorbers and the concrete block.

Sets: laundry (hook: close on the porthole, clothes tumbling, then the spin blurs and a speedometer passes a car's
highway speed; out to the whole machine; stat: by day; closer: in the evening, folded clothes on top), soak (break1:
a shirt soaking in a bucket, a magnifier shows dirt stuck between the threads; fix1: the drum full of holes turning back
and forth, three paddles lifting the clothes and dropping them), soap (break2: water beading off a grease blob on a
thread; fix2: detergent molecules, water-loving head and grease-loving tail, wrap the grease and carry it away), spin
(break3: a dripping heavy pile; fix3: the drum at 1,400 turns a minute, water flying out through the holes into the
tub), walk (break4: one heavy towel on one side and the machine shakes and walks across the floor; fix4: x-ray of the
concrete block bolted to the tub, the springs above and the shock absorbers below, the machine standing still), old
(reveal: washday a century ago, boiling and scrubbing on a washboard, then the first electric washer), tag (the machine
walking across the bathroom until somebody sits on it; AR: mom shouting from the door).
World: front view, the floor at y = 0, the machine 420 x 540 units standing at x = 0.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of  # noqa: E402
from bullettrain import gauge  # noqa: E402
from phone import bubble, mom  # noqa: E402

MW, MH = 420.0, 540.0
PCY = -262.0                                   # porthole centre (world)
PR = 150.0                                     # porthole glass radius
WHITE = ("#F8FAFC", "#E2E8F0", "#CBD5E1")
CLOTHES = ("#EF4444", "#3B82F6", "#F59E0B", "#10B981", "#A855F7", "#F472B6", "#FDE047")
WATER = "#60A5FA"
CONCRETE = "#9CA3AF"


def tiles(c, t, night=0.0):
    """Bathroom wall and floor tiles (world: wall above y = 0, floor below)."""
    wall = mix("#24405A", "#141E30", night)
    c.drawRect(R(-2000, -1600, 4000, 1600), lin_paint(0, -1600, 0, 0, [shade(wall, 0.05), wall], a=1.0))
    for k in range(-20, 21):
        c.drawLine(k * 110, -1600, k * 110, 0, P("#9FC4DA", 0.14, stroke=2))
    for k in range(15):
        c.drawLine(-2000, -k * 110, 2000, -k * 110, P("#9FC4DA", 0.14, stroke=2))
    add_glow(c, 0, -700, 700, "#7DD3FC", 0.10)
    floor = mix("#2A3E54", "#121A28", night)
    c.drawRect(R(-2000, 0, 4000, 1400), lin_paint(0, 0, 0, 700, [floor, shade(floor, -0.3)]))
    for k in range(-20, 21):
        c.drawLine(k * 160, 0, k * 220, 700, P("#9FC4DA", 0.12, stroke=2))
    for k in range(1, 6):
        c.drawLine(-2000, k * k * 22, 2000, k * k * 22, P("#9FC4DA", 0.10, stroke=2))


def drum_holes(c, cx, cy, r, ang, a=1.0):
    """The perforated drum seen through the door: rings of holes turning with ang (degrees)."""
    for ring in range(1, 5):
        rr_ = r * ring / 4.6
        n = 6 * ring
        for k in range(n):
            q = math.radians(ang + k * 360 / n + ring * 7)
            c.drawCircle(cx + math.cos(q) * rr_, cy + math.sin(q) * rr_, 4.2, P("#475569", 0.7 * a))


def paddles(c, cx, cy, r, ang, a=1.0):
    for k in range(3):
        q = math.radians(ang + k * 120)
        x0, y0 = cx + math.cos(q) * r * 0.98, cy + math.sin(q) * r * 0.98
        x1, y1 = cx + math.cos(q) * r * 0.72, cy + math.sin(q) * r * 0.72
        c.drawLine(x0, y0, x1, y1, P("#94A3B8", a, stroke=22))
        c.drawLine(x0, y0, x1, y1, P("#CBD5E1", a, stroke=10))


def garment(c, x, y, s, col, rot=0.0, a=1.0):
    """A small T-shirt shape."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    c.drawPath(path_of([(-14, -16), (-6, -20), (6, -20), (14, -16), (22, -6), (14, -2), (12, 18), (-12, 18), (-14, -2),
                        (-22, -6)], close=True), P(col, a))
    c.restore()


def tumble_pos(k, ang, r):
    """Where garment k sits in a slowly turning drum: lifted by the paddles, then dropping back (front view)."""
    ph = (ang + k * 51.4) % 360.0
    base = math.radians(90)                                        # bottom of the drum (y down)
    if ph < 130:                                                   # riding up the wall
        q = base + math.radians(ph)
        return math.cos(q) * r * 0.78, math.sin(q) * r * 0.78
    if ph < 175:                                                   # falling back across the drum
        f = (ph - 130) / 45.0
        q0 = base + math.radians(130)
        x0, y0 = math.cos(q0) * r * 0.78, math.sin(q0) * r * 0.78
        x1, y1 = -18 + k * 6, r * 0.6
        return lerp(x0, x1, f), lerp(y0, y1, f * f)
    f = (ph - 175) / 185.0                                         # in the pile at the bottom, rolling along
    return lerp(-60, 60, f) + k * 4, r * 0.62 - math.sin(f * math.pi) * 10


def machine(c, t, x=0.0, s=1.0, xray=0.0, ang=0.0, spin=0.0, clothes=1.0, water=0.0, towel=0.0, parts=0.0, rot=0.0,
            run=1.0, display="1:12", fly=0.0, wet=0.0, foam=0.0, a=1.0, lit=0.0):
    """The washer standing on y = 0 (world) at x. xray 0..1 shows the tub and its parts; ang = drum angle (degrees);
    spin 0..1 blurs the clothes into a ring; water 0..1 the water level; towel 0..1 one heavy towel on one side;
    parts 0..1 the concrete block, springs and shock absorbers; fly 0..1 water flying out through the holes."""
    if a <= 0:
        return
    c.save()
    c.translate(x, 0)
    c.scale(s, s)
    c.rotate(rot)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    contact_shadow(c, 0, 0, MW * 1.05, 0.5, 26)
    for fx_ in (-170, 170):
        c.drawRRect(rr(fx_ - 18, -10, 36, 14, 5), P("#475569"))
    body = mix(WHITE[0], "#FFE7C2", 0.25 * lit)
    c.drawRRect(rr(-MW / 2, -MH, MW, MH - 6, 26), lin_paint(-MW / 2, 0, MW / 2, 0, [WHITE[1], body, WHITE[1], WHITE[2]]))
    if xray > 0:                                                   # see through the cabinet
        c.drawRRect(rr(-MW / 2 + 12, -MH + 70, MW - 24, MH - 90, 18), P("#1E293B", 0.85 * xray))
        tub_r = 186.0
        c.drawCircle(0, PCY, tub_r, P("#334155", xray))
        c.drawCircle(0, PCY, tub_r, P("#94A3B8", xray, stroke=6))
        if parts > 0:
            for sd in (-1, 1):                                    # springs from the top corners
                x0, y0, x1, y1 = sd * 170, -MH + 80, sd * 110, PCY - tub_r + 30
                pts = []
                for k in range(15):
                    f = k / 14
                    pts.append((lerp(x0, x1, f) + (12 if k % 2 else -12) * (0 < k < 14), lerp(y0, y1, f)))
                c.drawPath(path_of(pts), P("#FDE047", parts * xray, stroke=5))
            for sd in (-1, 1):                                    # shock absorbers below
                x0, y0, x1, y1 = sd * 140, -16, sd * 90, PCY + tub_r - 20
                c.drawLine(x0, y0, lerp(x0, x1, 0.5), lerp(y0, y1, 0.5), P("#F97316", parts * xray, stroke=16))
                c.drawLine(lerp(x0, x1, 0.45), lerp(y0, y1, 0.45), x1, y1, P("#CBD5E1", parts * xray, stroke=8))
            c.drawRRect(rr(-120, PCY - tub_r - 6, 240, 46, 8), P(CONCRETE, parts * xray))   # the concrete block
            for k in range(6):
                c.drawCircle(-100 + k * 40, PCY - tub_r + 16, 4, P("#6B7280", parts * xray))
            c.drawRRect(rr(-120, PCY - tub_r - 6, 240, 46, 8), P("#4B5563", parts * xray, stroke=3))
        c.drawRRect(rr(-60, -88, 120, 60, 12), P("#64748B", xray))  # the motor
    # control strip
    c.drawRRect(rr(-MW / 2 + 14, -MH + 12, MW - 28, 62, 14), P("#E2E8F0" if xray < 0.5 else "#CBD5E1"))
    c.drawCircle(-MW / 2 + 70, -MH + 43, 22, P("#94A3B8"))
    c.drawLine(-MW / 2 + 70, -MH + 43, -MW / 2 + 70 + 14 * math.cos(t), -MH + 43 + 14 * math.sin(t), P("#334155", 1, stroke=4))
    c.drawRRect(rr(40, -MH + 24, 130, 38, 8), P("#0F172A"))
    text(c, display, 105, -MH + 54, 30, "#34D399" if run > 0.5 else "#64748B", "Poppins-Black", align="center")
    # the porthole: chrome ring, glass, the drum inside
    c.drawCircle(0, PCY, PR + 26, lin_paint(0, PCY - PR, 0, PCY + PR, ["#F1F5F9", "#94A3B8", "#E2E8F0"]))
    c.save()
    gp = skia.Path()
    gp.addCircle(0, PCY, PR)
    c.clipPath(gp, doAntiAlias=True)
    c.drawCircle(0, PCY, PR, P("#0F1B2E"))
    drum_holes(c, 0, PCY, PR, ang if spin < 0.5 else ang * 0.05)
    if water > 0:
        wl = PCY + PR - water * PR * 0.9
        wp = [(x_, wl + math.sin(x_ * 0.04 + t * 6) * 5) for x_ in range(-int(PR), int(PR) + 1, 10)]
        c.drawPath(path_of(wp + [(PR, PCY + PR), (-PR, PCY + PR)], close=True), P(WATER, 0.45))
    if foam > 0:
        for k in range(10):
            c.drawCircle(-PR + 20 + k * 30, PCY + PR - water * PR * 0.9 - 6, 16, P("#FFFFFF", 0.7 * foam))
    if clothes > 0:
        if spin < 0.5:
            paddles(c, 0, PCY, PR, ang)
            for k in range(7):
                dx, dy = tumble_pos(k, ang, PR)
                garment(c, dx, PCY + dy, 1.5, CLOTHES[k], rot=ang * 0.7 + k * 40, a=clothes)
            if towel > 0:                                          # one heavy towel stuck on one side
                q = math.radians(ang + 90)
                c.drawRRect(rr(math.cos(q) * PR * 0.7 - 40, PCY + math.sin(q) * PR * 0.7 - 26, 80, 52, 16), P("#DC2626", towel))
        else:                                                      # spinning: clothes pressed to the wall, blurred
            for k in range(14):
                p_ = skia.Path()
                p_.addArc(R(-PR * 0.86, PCY - PR * 0.86, PR * 1.72, PR * 1.72), ang * 0.3 + k * 25.7, 22)
                c.drawPath(p_, P(CLOTHES[k % 7], 0.85 * clothes, stroke=34, cap="butt"))
            for k in range(3):
                p_ = skia.Path()
                p_.addArc(R(-PR * 0.6, PCY - PR * 0.6, PR * 1.2, PR * 1.2), (t * 900 + k * 120) % 360, 70)
                c.drawPath(p_, P("#FFFFFF", 0.35, stroke=4))
    c.drawCircle(0, PCY, PR, rad_paint(-40, PCY - 60, PR * 1.4, [("#FFFFFF", 0.22), ("#FFFFFF", 0.0)]))
    c.restore()
    c.drawCircle(0, PCY, PR + 26, P("#64748B", 1, stroke=4))
    if fly > 0 and xray > 0:                                       # water thrown out through the holes into the tub
        rng = random.Random(3)
        for k in range(36):
            q = math.radians(rng.uniform(0, 360))
            f = (t * 2.2 + rng.random()) % 1.0
            r0 = lerp(PR * 0.9, 186, f)
            c.drawLine(math.cos(q) * r0, PCY + math.sin(q) * r0, math.cos(q) * (r0 + 18), PCY + math.sin(q) * (r0 + 18),
                       P(WATER, fly * (1 - f), stroke=5))
    if wet > 0:
        for k in range(5):
            q = (t * 1.3 + k * 0.2) % 1.0
            c.drawCircle(-150 + k * 70, -8 + q * 30, 6, P(WATER, wet * (1 - q)))
    if a < 1:
        c.restore()
    c.restore()


def rpm_gauge(c, x, y, rpm, a=1.0, top=1400.0):
    """A rev counter (screen space) up to 1,400 turns a minute."""
    if a <= 0:
        return
    r = 130
    c.save()
    c.translate(x, y)
    k = e_back(clamp(a * 1.3))
    c.scale(k, k)
    c.drawCircle(0, 0, r + 18, P("#000000", 0.45, blur=16))
    c.drawCircle(0, 0, r + 12, P("#0F172A", 0.92))
    for i in range(15):
        q = math.radians(150 + i * 240 / 14)
        r0 = r - (22 if i % 2 == 0 else 12)
        c.drawLine(math.cos(q) * r0, math.sin(q) * r0, math.cos(q) * (r - 4), math.sin(q) * (r - 4),
                   P(WARN if i >= 12 else "#E2E8F0", 0.9, stroke=4))
    v = clamp(rpm / top)
    arc = skia.Path()
    arc.addArc(R(-r + 10, -r + 10, 2 * r - 20, 2 * r - 20), 150, 240 * v)
    c.drawPath(arc, P(HILITE, 0.9, stroke=10, cap="butt"))
    q = math.radians(150 + 240 * v)
    c.drawLine(0, 0, math.cos(q) * (r - 28), math.sin(q) * (r - 28), P(WARN, 1, stroke=8))
    c.drawCircle(0, 0, 12, P("#E2E8F0"))
    text(c, f"{int(round(rpm)):,}", 0, 70, 46, "#FFFFFF", "Poppins-Black")
    text(c, "rpm", 0, 104, 26, "#94A3B8", "Poppins-Bold")
    c.restore()


def bucket(c, x, y, s, t, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawPath(path_of([(-130, -220), (130, -220), (100, 0), (-100, 0)], close=True), lin_paint(-130, 0, 130, 0, ["#38BDF8", "#0EA5E9", "#0369A1"], a=a))
    c.drawOval(R(-130, -236, 260, 32), P("#7DD3FC", a))
    c.drawOval(R(-118, -232, 236, 24), P(WATER, 0.8 * a))
    garment(c, 0, -226, 3.0, "#F8FAFC", rot=10, a=a)
    c.drawPath(path_of([(-130, -220), (-60, -330), (60, -330), (130, -220)]), P("#64748B", a, stroke=6))
    c.restore()


def fibers(c, cx, cy, r, t, grease=1.0, a=1.0):
    """Magnified threads (screen space) inside a circle, with a grease blob on them."""
    c.drawCircle(cx, cy, r, P("#0B1426", 0.95 * a))
    c.save()
    cp = skia.Path()
    cp.addCircle(cx, cy, r)
    c.clipPath(cp, doAntiAlias=True)
    for k in range(-4, 5):
        c.drawLine(cx - r, cy + k * 52 - 20, cx + r, cy + k * 52 + 20, P("#E5E7EB", 0.8 * a, stroke=26))
        c.drawLine(cx - r, cy + k * 52 - 20, cx + r, cy + k * 52 + 20, P("#CBD5E1", 0.8 * a, stroke=10))
    if grease > 0:
        c.drawOval(R(cx - 110, cy - 60, 220, 120), P("#A16207", 0.9 * grease * a))
        c.drawOval(R(cx - 80, cy - 46, 90, 40), P("#FDE68A", 0.5 * grease * a))
    c.restore()
    c.drawCircle(cx, cy, r, P("#E5E7EB", a, stroke=10))


def soap_mol(c, x, y, ang, s=1.0, a=1.0):
    """A detergent molecule: water-loving blue head, grease-loving orange tail (screen space)."""
    q = math.radians(ang)
    tx, ty = x + math.cos(q) * 46 * s, y + math.sin(q) * 46 * s
    pts = [(lerp(x, tx, f) + math.sin(f * 9) * 5 * s * -math.sin(q), lerp(y, ty, f) + math.sin(f * 9) * 5 * s * math.cos(q))
           for f in [k / 8 for k in range(9)]]
    c.drawPath(path_of(pts), P("#FB923C", a, stroke=6 * s))
    c.drawCircle(x, y, 11 * s, P("#3B82F6", a))
    c.drawCircle(x - 3 * s, y - 3 * s, 4 * s, P("#BFDBFE", a))


def washboard(c, x, y, s, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRect(R(-60, -200, 120, 200), P("#A16207", a))
    for k in range(10):
        c.drawRect(R(-48, -180 + k * 16, 96, 8), P("#D6D3D1", a))
    c.restore()


def old_washer(c, x, y, s, t, run=1.0, a=1.0):
    """An early electric washer: a wooden tub on legs, a motor below, a wringer on top (world)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for lx in (-110, 110):
        c.drawLine(lx, 0, lx * 0.8, -160, P("#57534E", a, stroke=14))
    c.drawRRect(rr(-140, -420, 280, 270, 30), lin_paint(-140, 0, 140, 0, ["#B45309", "#92400E", "#78350F"], a=a))
    for k in range(4):
        c.drawLine(-140, -400 + k * 70, 140, -400 + k * 70, P("#451A03", 0.6 * a, stroke=6))
    c.drawRRect(rr(-50, -140, 100, 60, 10), P("#64748B", a))                     # motor
    c.drawRect(R(-120, -470, 240, 30), P("#9CA3AF", a))                         # wringer rollers
    c.drawRect(R(-120, -440, 240, 16), P("#6B7280", a))
    c.drawLine(120, -455, 160, -500 + 20 * math.sin(t * 4 * run), P("#374151", a, stroke=8))
    c.restore()


# ====================================================================================== the episode
class Washer(EpisodeV2):
    BUILD_NO = 63
    FIRST_SET = "laundry"
    CLEAR = "#0F172A"
    TITLE = {"en": "WASHING MACHINE", "ar_sa": "غسالة"}
    EMPH = {"en": ["CONGRATS", "WASH", "CLOTHES", "HANDS", "SPIN", "FASTER", "CAR", "HIGHWAY", "WASHING", "MACHINE",
                   "YOURSELF", "SOAKING", "DIRTY", "DIRT", "THREADS", "TUMBLE", "DRUM", "HOLES", "PADDLES", "LIFT", "DROP",
                   "WATER", "GREASE", "DETERGENT", "MOLECULES", "END", "AWAY", "DRIPPING", "HEAVY", "FOURTEEN", "HUNDRED",
                   "MINUTE", "FLIES", "TOWEL", "SIDE", "WALKS", "FLOOR", "BOLT", "CONCRETE", "SPRINGS", "SHOCK",
                   "ABSORBERS", "FOLLOW", "BIG", "BEN'S", "CLOCK", "WASHDAY", "BOILING", "SCRUBBING", "ELECTRIC",
                   "CENTURY", "TURNS", "FIVE", "GRAVITY", "TWENTY-FIVE", "KILO", "TAMED", "SHAKING", "BATHROOM", "SITS"],
            "ar_sa": ["مبروك", "تغسل", "الملابس", "تلمسها", "وتعصرها", "أسرع", "سيارة", "السريع", "غسالة", "بيدك",
                      "تنقعها", "الوسخ", "الخيوط", "فتقلّبها", "حوض", "خروم", "زعانف", "وتطيّحها", "الموية", "الدهون",
                      "صابون", "جزيئاته", "الدهن", "مبلولة", "وثقيلة", "فتلف", "ألف", "وأربعمية", "الدقيقة", "تطير",
                      "الخروم", "فوطة", "جهة", "تمشي", "الحمام", "خرسانة", "سوست", "مساعدات", "تابعني", "ساعة", "بيغ",
                      "بن", "الغسيل", "غلي", "وفرك", "الكهربا", "مية", "خمسمية", "الجاذبية", "خمسة", "وعشرين", "كيلو",
                      "ضبطوا", "الرجّة", "بالخرسانة", "وأمك", "اقعد"]}
    KEYS = {"ar_sa": {
        ("hook", "WASH"): "تغسل", ("hook", "HANDS"): "تلمسها", ("hook", "SPIN"): "وتعصرها", ("hook", "CAR"): "سيارة",
        ("hook", "CONGRATS"): "مبروك", ("hook", "MACHINE"): "غسالة",
        ("break1", "SOAKING"): "تنقعها", ("break1", "DIRTY"): "الوسخ", ("break1", "THREADS"): "الخيوط",
        ("fix1", "TUMBLE"): "فتقلّبها", ("fix1", "DRUM"): "حوض", ("fix1", "HOLES"): "خروم", ("fix1", "PADDLES"): "زعانف",
        ("fix1", "DROP"): "وتطيّحها",
        ("break2", "WATER"): "الموية", ("break2", "GREASE"): "الدهون",
        ("fix2", "DETERGENT"): "صابون", ("fix2", "MOLECULES"): "جزيئاته", ("fix2", "GREASE"): "الدهن",
        ("fix2", "WATER"): "والموية", ("fix2", "DIRT"): "الوسخ",
        ("break3", "DRIPPING"): "مبلولة", ("break3", "HEAVY"): "وثقيلة",
        ("fix3", "SPIN"): "فتلف", ("fix3", "FOURTEEN"): "ألف", ("fix3", "MINUTE"): "الدقيقة", ("fix3", "FLIES"): "تطير",
        ("fix3", "HOLES"): "الخروم",
        ("break4", "TOWEL"): "فوطة", ("break4", "SIDE"): "جهة", ("break4", "WALKS"): "تمشي", ("break4", "FLOOR"): "الحمام",
        ("fix4", "CONCRETE"): "خرسانة", ("fix4", "SPRINGS"): "سوست", ("fix4", "ABSORBERS"): "مساعدات",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "WASHDAY"): "الغسيل", ("reveal", "BOILING"): "غلي", ("reveal", "SCRUBBING"): "وفرك",
        ("reveal", "ELECTRIC"): "الكهربا", ("reveal", "CENTURY"): "مية",
        ("stat", "FOURTEEN"): "ألف", ("stat", "FIVE"): "خمسمية", ("stat", "TWENTY-FIVE"): "خمسة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "TAMED"): "ضبطوا", ("tag", "CONCRETE"): "بالخرسانة", ("tag", "WALKS"): "تمشي", ("tag", "SITS"): "اقعد"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Big Ben's clock"),
                   "stat": [("1,400", "TURNS A MINUTE"), ("500×", "GRAVITY"), ("25 kg", "OF CONCRETE")],
                   "L": {"nohands": "NO HANDS", "speed": "DRUM WALL: ~130 KM/H", "name": "A WASHING MACHINE",
                         "soak": "SOAKING ISN'T WASHING", "stuck": "DIRT STUCK IN THE THREADS", "tumble": "TUMBLE IT",
                         "holes": "A DRUM FULL OF HOLES", "paddles": "PADDLES LIFT + DROP", "grease": "WATER SLIDES OFF GREASE",
                         "soap": "DETERGENT", "mol": "GRABS GREASE + WATER", "away": "DIRT DRAGGED AWAY",
                         "heavy": "DRIPPING + HEAVY", "rpm": "1,400 TURNS A MINUTE", "fly": "WATER FLIES OUT",
                         "towel": "ONE HEAVY TOWEL", "walks": "IT WALKS!", "concrete": "CONCRETE BLOCK",
                         "springs": "SPRINGS", "shocks": "SHOCK ABSORBERS", "still": "STANDS STILL",
                         "washday": "WASHDAY: A WHOLE DAY", "first": "ELECTRIC, 100+ YEARS AGO", "sit": "SIT ON IT!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: ساعة بيغ بن"),
                      "stat": [("1,400", "لفة في الدقيقة"), ("500×", "الجاذبية"), ("25", "كيلو خرسانة")],
                      "L": {"nohands": "بدون ما تلمسها", "speed": "الحوض أسرع من سيارة", "name": "غسالة",
                            "soak": "النقع ما يغسل", "stuck": "الوسخ لاصق في الخيوط", "tumble": "تقلّبها",
                            "holes": "حوض كله خروم", "paddles": "زعانف ترفع وتطيّح", "grease": "الموية تتزحلق على الدهن",
                            "soap": "صابون", "mol": "يمسك الدهن والموية", "away": "ويسحب الوسخ",
                            "heavy": "مبلولة وثقيلة", "rpm": "ألف وأربعمية لفة", "fly": "الموية تطير",
                            "towel": "فوطة ثقيلة على جهة", "walks": "تمشي!", "concrete": "حجر خرسانة",
                            "springs": "سوست", "shocks": "مساعدات", "still": "ثابتة",
                            "washday": "يوم الغسيل: يوم كامل", "first": "الكهربا، قبل مية سنة وزيادة",
                            "sit": "اقعد عليها!"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "wash": ("hook", "WASH", 0.05), "hands": ("hook", "HANDS", 0.2), "spin": ("hook", "SPIN", 0.35),
            "car": ("hook", "CAR", 0.5), "congrats": ("hook", "CONGRATS", 0.7), "machine": ("hook", "MACHINE", 0.92),
            "soaking": ("break1", "SOAKING", 0.15), "dirty": ("break1", "DIRTY", 0.35), "threads": ("break1", "THREADS", 0.9),
            "tumble": ("fix1", "TUMBLE", 0.1), "drum": ("fix1", "DRUM", 0.3), "holes": ("fix1", "HOLES", 0.4),
            "paddles": ("fix1", "PADDLES", 0.65), "drop": ("fix1", "DROP", 0.92),
            "water": ("break2", "WATER", 0.1), "grease": ("break2", "GREASE", 0.9),
            "deterg": ("fix2", "DETERGENT", 0.15), "mol": ("fix2", "MOLECULES", 0.3), "grease2": ("fix2", "GREASE", 0.45),
            "water2": ("fix2", "WATER", 0.65), "dirt": ("fix2", "DIRT", 0.9),
            "dripping": ("break3", "DRIPPING", 0.6), "heavy": ("break3", "HEAVY", 0.9),
            "spin3": ("fix3", "SPIN", 0.1), "f1400": ("fix3", "FOURTEEN", 0.3), "minute": ("fix3", "MINUTE", 0.5),
            "flies": ("fix3", "FLIES", 0.7), "holes3": ("fix3", "HOLES", 0.92),
            "towel": ("break4", "TOWEL", 0.15), "side": ("break4", "SIDE", 0.35), "walks": ("break4", "WALKS", 0.8),
            "floor": ("break4", "FLOOR", 0.95),
            "concrete": ("fix4", "CONCRETE", 0.2), "springs": ("fix4", "SPRINGS", 0.5), "absorb": ("fix4", "ABSORBERS", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "washday": ("reveal", "WASHDAY", 0.1), "boiling": ("reveal", "BOILING", 0.35),
            "scrub": ("reveal", "SCRUBBING", 0.45), "electric": ("reveal", "ELECTRIC", 0.7), "century": ("reveal", "CENTURY", 0.92),
            "s1": ("stat", "FOURTEEN", 0.05), "s2": ("stat", "FIVE", 0.4), "s3": ("stat", "TWENTY-FIVE", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_tamed": ("tag", "TAMED", 0.05), "t_conc": ("tag", "CONCRETE", 0.2), "t_walks": ("tag", "WALKS", 0.5),
            "t_sits": ("tag", "SITS", 0.9)})
        T["threads1"] = max(T["threads"], T["dirty"]) + 0.1
        T["grease1"] = max(T["grease"], T["water"]) + 0.1
        T["heavy1"] = max(T["heavy"], T["dripping"]) + 0.1
        T["floor1"] = max(T["floor"], T["walks"]) + 0.1
        T["drop1"] = max(T["drop"], T["paddles"]) + 0.2
        T["dirt1"] = max(T["dirt"], T["water2"]) + 0.2
        T["holes31"] = max(T["holes3"], T["flies"]) + 0.2
        T["absorb1"] = max(T["absorb"], T["springs"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "soak", 1)
        self.cut(s("break2") - 0.12, "soap", -1)
        self.cut(s("break3") - 0.12, "spin", 1)
        self.cut(s("break4") - 0.12, "walk", -1)
        self.cut(s("reveal") - 0.12, "old", 1)
        self.cut(s("stat") - 0.12, "laundry", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- laundry camera: from the porthole close up, out to the whole machine
        cm = Camera(0, PCY + 20, 2.9)
        cm.key(0.05, 0, PCY + 18, 2.8, 0.4)
        cm.key(max(0.5, T["congrats"] - 0.8), 40, -330, 1.45, max(1.0, T["machine"] - T["congrats"] + 0.6))
        cm.key(s("stat") - 0.12, 0, -400, 1.25, 0.0).key(s("stat"), 0, -402, 1.26, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 0, -330, 1.5, 1.0).key(s("closer") + 0.9, 0, -328, 1.58, 3.0)
        self.cam = cm
        self.spans = [(T["threads1"], T["drop1"] + 0.3), (T["grease1"], T["dirt1"] + 0.3), (T["heavy1"], T["holes31"] + 0.3),
                      (T["floor1"], T["absorb1"] + 0.3)]
        self.shakes = [(T["spin"], 0.6, 6), (T["congrats"], 0.35, 8), (T["threads1"], 0.3, 6), (T["grease1"], 0.3, 6),
                       (T["heavy1"], 0.3, 6), (T["walks"] - 0.3, 1.2, 12), (s("closer") + 0.2, 0.35, 9), (T["t_walks"], 0.8, 8)]

    def drum_angle(self, t, t_spin, wash_speed=50.0, spin_max=2400.0, ramp=1.2):
        """Drum angle in degrees: slow wash turns (back and forth) until t_spin, then a ramp up to a fast spin."""
        if t < t_spin:
            return math.sin(t * 0.9) * 140 + t * wash_speed * 0.2
        d = t - t_spin
        if d < ramp:
            return math.sin(t_spin * 0.9) * 140 + t_spin * wash_speed * 0.2 + spin_max * d * d / (2 * ramp)
        return math.sin(t_spin * 0.9) * 140 + t_spin * wash_speed * 0.2 + spin_max * ramp / 2 + spin_max * (d - ramp)

    # ------------------------------------------------------------------ set: laundry (hook, stat, closer)
    def draw_laundry(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        closer = t >= s("closer") - 0.1
        night = 0.5 * prog(t, s("closer") - 0.1, s("closer") + 0.8) if closer else 0.0
        self.view(c, cam)
        tiles(c, t, night)
        if hook:
            sk = prog(t, T["spin"] - 0.2, T["spin"] + 0.6)
            ang = self.drum_angle(t, T["spin"] - 0.2)
            xr = 0.0
            machine(c, t, xray=xr, ang=ang, spin=1.0 if sk > 0.5 else 0.0, water=0.35 * (1 - sk), foam=0.6 * (1 - sk),
                    display="1400" if sk > 0.5 else "0:48")
        else:
            machine(c, t, ang=t * 40, water=0.0, clothes=0.0 if closer else 1.0, display="END" if closer else "0:12",
                    run=0.0 if closer else 1.0, lit=night)
            if closer:                                               # folded clothes on top
                for k, col in enumerate(("#3B82F6", "#F59E0B", "#10B981")):
                    c.drawRRect(rr(-120, -MH - 30 - k * 26, 200, 26, 8), P(col))
            st = s("stat") - 0.12 <= t < s("closer") - 0.1
            if st:
                person(c, 330, 0, 300, "#2563EB", t, pose="look", face=-1, a=prog(t, T["s3"] - 0.4, T["s3"]))
        c.restore()
        if closer and night > 0:
            c.drawRect(R(0, 0, W, H), P("#2A1E40", 0.25 * night))
        if hook:
            gk = prog(t, T["car"] - 0.4, T["car"]) * (1 - prog(t, T["congrats"] - 0.1, T["congrats"] + 0.3))
            if gk > 0:
                kmh = lerp(0, 130, prog(t, T["car"] - 0.4, T["car"] + 0.5))
                c.save()
                c.translate(860, 600)
                c.scale(0.72, 0.72)
                gauge(c, 0, 0, kmh, a=gk, label="km/h")
                c.restore()

    def ui_laundry(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "nohands", T["wash"] - 0.1, T["car"] - 0.4, accent="#93C5FD", size=46)
            self.chip(540, 300, "speed", T["car"] - 0.4, T["machine"] - 0.3, accent=WARN, size=42)
            self.chip(540, 300, "name", T["machine"] - 0.3, s("break1") + 0.1, accent=HILITE, size=48)

    # ------------------------------------------------------------------ set: soak (break1, fix1)
    def draw_soak(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        if not fixed:
            cam = (0, -330, 1.5)
            self.view(c, cam)
            tiles(c, t)
            bucket(c, -40, 0, 1.4, t)
            c.restore()
            mk = prog(t, T["dirty"] - 0.3, T["dirty"])
            if mk > 0:
                fibers(c, 760, 700, 210, t, grease=0.0, a=mk)
                rng = random.Random(5)
                for k in range(16):                              # dirt grains stuck between the threads
                    c.drawCircle(760 + rng.uniform(-150, 150), 700 + rng.uniform(-150, 150), rng.uniform(9, 16),
                                 P("#78350F", mk))
            return
        cam = (0, PCY, 2.6)
        self.view(c, cam)
        tiles(c, t)
        ang = math.sin((t - s("fix1")) * 1.6) * 160 + (t - s("fix1")) * 60
        machine(c, t, xray=0.0, ang=ang, water=0.4, foam=0.4)
        c.restore()
        self.ui["paddle"] = self.to_screen(cam, math.cos(math.radians(ang)) * PR * 0.85, PCY + math.sin(math.radians(ang)) * PR * 0.85)

    def ui_soak(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "soak", T["soaking"] - 0.2, T["dirty"] - 0.1, accent="#93C5FD", size=46)
            self.chip(540, 300, "stuck", T["dirty"] - 0.1, s("fix1") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["threads1"], s("fix1") - 0.2, x=920, y=420)
            self.red(T["threads1"], 1.2)
            return
        self.chip(540, 300, "tumble", T["tumble"] - 0.2, T["drum"] - 0.1, accent="#FDE68A", size=52)
        self.chip(540, 300, "holes", T["drum"] - 0.1, T["paddles"] - 0.2, accent="#CBD5E1", size=44)
        self.chip(540, 300, "paddles", T["paddles"] - 0.2, s("break2") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["drop1"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: soap (break2, fix2), magnified
    def draw_soap(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        vrect(c, 0, 0, W, H, ["#0B1426", "#13233F"])
        cx, cy, r = 540, 820, 380
        if not fixed:
            fibers(c, cx, cy, r, t, grease=1.0)
            wk = prog(t, T["water"] - 0.3, T["grease1"] + 0.6)
            for k in range(5):                                   # water drops sliding off the grease
                q = (t * 0.9 + k * 0.2) % 1.0
                xx = cx - 140 + k * 70
                yy = cy - 220 + q * 200
                if abs(xx - cx) < 110 and yy > cy - 70:
                    xx += (1 if xx > cx else -1) * (yy - (cy - 70)) * 1.5
                c.drawCircle(xx, yy, 18, P(WATER, 0.9 * wk))
                c.drawCircle(xx - 6, yy - 6, 6, P("#FFFFFF", 0.7 * wk))
            return
        lift = prog(t, T["water2"] - 0.2, T["dirt1"] + 0.4)
        fibers(c, cx, cy, r, t, grease=0.0)
        gx, gy = cx + lift * 60, cy - lift * 300
        c.drawOval(R(gx - 110, gy - 60, 220, 120), P("#A16207", 0.95))
        mk = prog(t, T["mol"] - 0.3, T["grease2"] + 0.3)
        for k in range(14):                                      # tails in the grease, heads out in the water
            q = k * 360 / 14
            qq = math.radians(q)
            rx, ry = 110 + 70 * (1 - mk) + 40, 60 + 70 * (1 - mk) + 40
            hx, hy = gx + math.cos(qq) * rx, gy + math.sin(qq) * ry
            soap_mol(c, hx, hy, q + 180, s=1.3, a=prog(t, T["deterg"] - 0.3, T["deterg"]))
        if lift > 0:
            for k in range(6):
                c.drawCircle(cx - 300 + k * 120, cy + 300 - ((t * 120 + k * 50) % 600), 10, P("#BFDBFE", 0.5 * lift))

    def ui_soap(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "grease", T["water"] - 0.2, s("fix2") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["grease1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["grease1"], 1.2)
            return
        self.chip(540, 300, "soap", T["deterg"] - 0.2, T["mol"] - 0.1, accent="#93C5FD", size=52)
        self.chip(540, 300, "mol", T["mol"] - 0.1, T["dirt"] - 0.2, accent="#FB923C", size=44)
        self.chip(540, 300, "away", T["dirt"] - 0.2, s("break3") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["dirt1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: spin (break3, fix3)
    def draw_spin(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        if not fixed:
            cam = (0, -150, 1.6)
            self.view(c, cam)
            tiles(c, t)
            for k, col in enumerate(CLOTHES):                    # a heavy wet pile
                c.drawRRect(rr(-180 + (k % 4) * 90, -60 - (k // 4) * 60 - (k % 2) * 10, 120, 60, 24), P(shade(col, -0.25)))
            for k in range(10):
                q = (t * 1.5 + k * 0.1) % 1.0
                c.drawCircle(-170 + k * 38, -30 + q * 60, 7, P(WATER, 0.9 * (1 - q)))
            hk = prog(t, T["heavy"] - 0.4, T["heavy1"])
            if hk > 0:
                c.drawRRect(rr(-80, -340, 160, 90, 14), P("#0F172A", hk))
                text(c, "+ kg", 0, -278, 54, WARN, "Poppins-Black", align="center", a=hk)
            c.restore()
            return
        cam = (0, PCY, 1.9)
        self.view(c, cam)
        tiles(c, t)
        ang = self.drum_angle(t, T["spin3"] - 0.2)
        machine(c, t, xray=1.0, ang=ang, spin=1.0, water=0.0, fly=prog(t, T["flies"] - 0.3, T["flies"]), display="1400")
        c.restore()
        rk = prog(t, T["f1400"] - 0.4, T["minute"])
        if rk > 0:
            rpm_gauge(c, 860, 560, lerp(0, 1400, rk), a=rk)

    def ui_spin(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "heavy", T["dripping"] - 0.3, s("fix3") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["heavy1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["heavy1"], 1.2)
            return
        self.chip(540, 300, "rpm", T["spin3"] - 0.2, T["flies"] - 0.2, accent=HILITE, size=44)
        self.chip(540, 300, "fly", T["flies"] - 0.2, s("break4") - 0.15, accent=WATER, size=46)
        self.badge("check", T["holes31"] + 0.1, s("break4") - 0.15, x=920, y=900)

    # ------------------------------------------------------------------ set: walk (break4, fix4)
    def draw_walk(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        cam = (60, -300, 1.35)
        self.view(c, cam)
        tiles(c, t)
        if not fixed:
            wk = prog(t, T["side"] - 0.2, T["floor1"] + 0.6)
            ang = self.drum_angle(t, T["side"] - 0.3, spin_max=900.0)
            jit = math.sin(t * 47) * 6 * wk
            machine(c, t, x=wk * 220 + jit, ang=ang, towel=prog(t, T["towel"] - 0.3, T["towel"]), rot=math.sin(t * 31) * 3 * wk,
                    spin=0.0)
            if wk > 0.2:
                for k in range(3):
                    c.drawLine(-260 + wk * 220, -100 - k * 60, -320 + wk * 220, -110 - k * 60, P("#FFFFFF", 0.6 * wk, stroke=6))
            self.ui["m"] = self.to_screen(cam, wk * 220, -MH)
        else:
            ang = self.drum_angle(t, s("fix4") - 0.4)
            pk = prog(t, T["concrete"] - 0.4, T["concrete"])
            machine(c, t, x=0, ang=ang, spin=1.0, xray=1.0, parts=pk, towel=0.0, rot=math.sin(t * 31) * 0.4,
                    display="1400")
            self.ui["conc"] = self.to_screen(cam, 0, PCY - 186 + 16)
            self.ui["spr"] = self.to_screen(cam, 150, -MH + 120)
            self.ui["abs"] = self.to_screen(cam, 120, -60)
        c.restore()

    def ui_walk(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "towel", T["towel"] - 0.2, T["walks"] - 0.2, accent="#FCA5A5", size=46)
            self.chip(540, 300, "walks", T["walks"] - 0.2, s("fix4") - 0.15, accent=WARN, size=56)
            self.badge("alert", T["floor1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["floor1"], 1.2)
            return
        cx_, cy_ = self.ui.get("conc", (540, 700))
        self.label(cx_, cy_, 300, 520, "concrete", T["concrete"] - 0.2, s("cta") - 0.2, accent="#CBD5E1", size=36)
        sx_, sy_ = self.ui.get("spr", (700, 600))
        self.label(sx_, sy_, 820, 440, "springs", T["springs"] - 0.2, s("cta") - 0.2, accent="#FDE047", size=36)
        ax_, ay_ = self.ui.get("abs", (700, 1150))
        self.label(ax_, ay_, 840, 1080, "shocks", T["absorb"] - 0.3, s("cta") - 0.2, accent="#F97316", size=34)
        self.chip(540, 300, "still", T["absorb1"], s("cta") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["absorb1"] + 0.1, s("cta") - 0.15, x=920, y=640)

    # ------------------------------------------------------------------ set: old (reveal)
    def draw_old(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#4A3A28", "#3A2C1E", "#2A1E14"])
        c.drawRect(R(0, 1230, W, H - 1230), P("#5A4630"))
        first = t >= T["electric"] - 0.3
        if not first:
            c.drawOval(R(140, 1010, 420, 120), P("#57534E"))      # the boiling tub over a fire
            c.drawRRect(rr(150, 900, 400, 180, 30), P("#78716C"))
            v2.flame(c, 350, 1220, 260, 140, t, power=prog(t, T["boiling"] - 0.4, T["boiling"]), ang=-90.0)
            for k in range(4):
                v2.puff(c, 220 + k * 90, 860 - ((t * 60 + k * 40) % 160), 40, "#E7E5E4", 0.4, k=k)
            washboard(c, 760, 1180, 1.6)
            person(c, 900, 1235, 420, "#7C2D12", t, pose="carry", face=-1, hair="#3F2A1A")
            sk = prog(t, T["scrub"] - 0.2, T["scrub"])
            if sk > 0:
                garment(c, 760 + math.sin(t * 14) * 24, 1000, 4.0, "#F8FAFC", rot=0, a=sk)
        else:
            old_washer(c, 540, 1235, 1.5, t, run=1.0, a=prog(t, T["electric"] - 0.3, T["electric"]))
        c.drawRect(R(0, 0, W, H), P("#704214", 0.12))

    def ui_old(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "washday", T["washday"] - 0.2, T["electric"] - 0.3, accent="#FDE68A", size=44)
        self.chip(540, 300, "first", T["electric"] - 0.3, s("stat") - 0.15, accent=GOOD, size=40)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        cam = (120, -320, 1.25)
        self.view(c, cam)
        tiles(c, t)
        wk = prog(t, T["t_conc"], T["t_walks"] + 0.4)
        sit = t >= T["t_sits"] - 0.15
        jit = math.sin(t * 47) * 8 * wk * (0.2 if sit else 1.0)
        mx = wk * 260 + jit
        machine(c, t, x=mx, ang=self.drum_angle(t, T["t_tamed"], spin_max=900.0), rot=math.sin(t * 31) * 3 * wk * (0.2 if sit else 1),
                spin=0.0)
        if sit:
            person(c, mx, -MH + 4, 300, "#16A34A", t, pose="sit", face=1, hair="#1F2937")
        c.restore()
        if self.rtl:
            mk = prog(t, T["t_walks"] - 0.2, T["t_walks"] + 0.3)
            mom(c, lerp(-200, 150, e_out(mk)), 1500, 520, t, a=1.0)

    def ui_tag(self, c, t, tw):
        T = self.T
        if self.rtl:
            bubble(c, 420, 560, self.L["sit"], self.span(T["t_sits"] - 0.5, self.duration + 1), tail_left=True, size=54)
        else:
            self.chip(540, 300, "sit", T["t_sits"] - 0.2, self.duration + 1, accent=HILITE, size=52)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#C9D9E6", "#9FB4C4"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whirr(max(1.0, T["spin"]), 90.0, 120.0, 61), -16), (T["spin"] - 0.2, sfx.riser(1.2, 62), -12),
              (T["spin"] + 0.6, sfx.whirr(1.6, 400.0, 700.0, 63), -14), (T["car"], sfx.whoosh(0.6, True, 64), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 66), -8),
              (T["machine"], sfx.beep(1500.0, 0.12), -10), (T["machine"] + 0.2, sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["soaking"], sfx.tap(68), -10),
               (T["threads1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -4), (T["tumble"], sfx.thud(0.4, 70), -10),
               (T["paddles"], sfx.thud(0.4, 71), -10), (T["drop1"], sfx.ding(), -8), (T["drop1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 72), -4), (T["water"], sfx.tap(73), -10),
               (T["grease1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 74), -4), (T["mol"], sfx.sparkle(0.6, 8, 75), -10),
               (T["dirt1"], sfx.ding(), -8), (T["dirt1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 76), -4), (T["dripping"], sfx.tap(77), -10),
               (T["heavy1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 78), -4), (T["spin3"], sfx.riser(1.0, 79), -12),
               (T["f1400"], sfx.whirr(2.0, 500.0, 900.0, 80), -14), (T["holes31"], sfx.ding(), -8),
               (T["holes31"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 81), -4), (T["side"], sfx.thud(0.5, 82), -8),
               (T["walks"], rumble(1.2, 83), -10), (T["floor1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 84), -4), (T["concrete"], sfx.clank(300.0, 0.5, 85), -8),
               (T["springs"], sfx.snap(86), -10), (T["absorb1"], sfx.ding(), -8), (T["absorb1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(87), 0), (T["follow"] - 0.15, sfx.pop(88), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 89), -6), (T["scrub"], sfx.hiss(0.6, 90), -14),
               (T["electric"], sfx.hum(1.0, 110.0), -14)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 91), -6), (T["s1"], sfx.pop(92), -3), (T["s2"], sfx.pop(93), -3),
               (T["s3"], sfx.pop(94), -3)]
        ev += [(T["cong2"], sfx.pop(95), -2), (T["cong2"], sfx.sparkle(1.4, 18, 96), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 97), -6), (T["t_walks"], rumble(1.0, 98), -12),
               (T["t_sits"], sfx.thud(0.4, 99), -8)]
        return ev


NAME = "washer"
EPISODE = Washer
