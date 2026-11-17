"""Episode 36 - The Great Pyramid of Giza.  v2 look: the Giza plateau at dusk with the Nile and palms in front.

Sets: giza (hook: courses of blocks stack up into the pyramid, then its casing gleams white; the reveal: thousands of
workers, not slaves, and the polished white casing; the stat and the closer), sledge (break1: a block heavier than a
car on a wooden sledge digs into the sand; fix1: water poured in front firms the sand and half the crew can pull it),
nile (break2/fix2: a map of the Nile: white stone at Tura across the river, granite at Aswan 900 km away, boats down the
Nile to a harbor by the site), inside (break3/fix3: a cut through the pyramid: the king's room under a mountain of stone,
then five empty rooms of granite beams and a pointed roof that pushes the weight aside), base (break4/fix4: a crooked
base whose corners never meet at the top, then a level base aimed at north), shelf (the tag).
World (giza, sledge, inside, base): side or front view, the ground is y = 0.
"""
from v2_base import *  # noqa: F401,F403

DUSK = {"top": "#0B0A2A", "upper": "#2A1B5C", "mid": "#7A3B6E", "low": "#E0795A", "horizon": "#FFB070",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SAND = ("#C7955A", "#A8733F", "#7A4E26", "#3E2712")
LIME = "#E9DFC8"
GRANITE = "#B48A86"
NILE = "#2563EB"
PH = 762.0           # pyramid height in the giza world
PW = 600.0           # half base


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def faces(x, y, s):
    """Two visible faces of the pyramid (apex, left corner, front corner, right corner) at base centre (x, y)."""
    A = (x, y - PH * s)
    L = (x - PW * s, y - 18 * s)
    F = (x + PW * 0.22 * s, y + 26 * s)
    Rr = (x + PW * 0.92 * s, y - 40 * s)
    return A, L, F, Rr


def _tri(a, b, c_):
    p = skia.Path()
    p.moveTo(*a)
    p.lineTo(*b)
    p.lineTo(*c_)
    p.close()
    return p


def pyramid(c, x, y, s, t, built=1.0, casing=0.0, glint=-1.0, a=1.0, glow=0.0):
    """The Great Pyramid: courses of blocks up to 'built' (0..1 of the height), a white casing 0..1, a glint sweep."""
    if a <= 0 or built <= 0:
        return
    A, L, F, Rr = faces(x, y, s)
    left, right = _tri(A, L, F), _tri(A, F, Rr)
    c.save()
    top = y - PH * s * built
    c.clipRect(R(x - 2000, top, 4000, 3000))
    stone_l = mix("#D9A766", "#CFC2A3", casing)
    stone_r = mix("#8A5A2B", "#7E7464", casing)
    c.drawPath(left, lin_paint(L[0], 0, F[0], 0, [shade(stone_l, 0.12), stone_l], a=a))
    c.drawPath(right, lin_paint(F[0], 0, Rr[0], 0, [stone_r, shade(stone_r, -0.2)], a=a))
    if True:                                                             # courses and joints (faint on the casing)
        n = 34
        for k in range(1, n):
            q = k / float(n)
            yl = lerp(L[1], A[1], q)
            xl = lerp(L[0], A[0], q)
            xf = lerp(F[0], A[0], q)
            yf = lerp(F[1], A[1], q)
            xr = lerp(Rr[0], A[0], q)
            yr = lerp(Rr[1], A[1], q)
            c.drawLine(xl, yl, xf, yf, P("#6B4423", a * (0.55 - 0.45 * casing), stroke=2.2 * s))
            c.drawLine(xf, yf, xr, yr, P("#3B2410", a * (0.55 - 0.45 * casing), stroke=2.2 * s))
            for j in range(1, 7):
                u = (j + 0.5 * (k % 2)) / 7.0
                if u < 1:
                    jx, jy = lerp(xl, xf, u), lerp(yl, yf, u)
                    c.drawLine(jx, jy, jx, jy + 18 * s, P("#6B4423", 0.35 * a * (1 - casing), stroke=1.6 * s))
    if built < 1:                                                        # the working edge of the top course
        c.drawLine(x - 2000, top, x + 2000, top, P("#FDE68A", 0.0))
    if glint > -0.5:
        band = skia.Path()
        gx = lerp(L[0] - 300 * s, Rr[0] + 300 * s, glint)
        band.moveTo(gx - 60 * s, y + 60 * s)
        band.lineTo(gx + 40 * s, y + 60 * s)
        band.lineTo(gx + 340 * s, y - PH * s - 60 * s)
        band.lineTo(gx + 240 * s, y - PH * s - 60 * s)
        band.close()
        c.save()
        c.clipPath(left, doAntiAlias=True)
        c.drawPath(band, P("#FFFFFF", 0.35 * a * casing, blur=10))
        c.restore()
    c.restore()
    if casing > 0.5:
        add_glow(c, A[0], A[1] + 40 * s, 120 * s, "#FFF7E0", 0.25 * (casing - 0.5) * 2 * a)
    if glow > 0:
        add_glow(c, x, y - PH * s * 0.5, 700 * s, "#FDE68A", 0.1 * glow * a)
    if built < 1:                                                        # blocks being set on the top course
        A2 = (x, top)
        for i in range(3):
            q = (t * 1.4 + i / 3.0) % 1.0
            bx = lerp(x - PW * s * (1 - built) * 0.9, x + PW * s * (1 - built) * 0.5, (i + 0.5) / 3.0)
            by = top - 18 * s * (1 - q)
            c.drawRect(R(bx - 14 * s, by - 16 * s, 28 * s, 16 * s), P("#E7C18A", a * (1 - q * 0.3)))
        _ = A2


def palm(c, x, y, h, sway=0.0, a=1.0):
    c.save()
    c.translate(x, y)
    tr = skia.Path()
    tr.moveTo(-8, 0)
    tr.quadTo(10 + sway * 10, -h * 0.5, 6 + sway * 20, -h)
    tr.lineTo(14 + sway * 20, -h)
    tr.quadTo(18 + sway * 10, -h * 0.5, 8, 0)
    tr.close()
    c.drawPath(tr, P("#3B2410", a))
    tx, ty = 10 + sway * 20, -h
    for k in range(7):
        an = math.radians(-170 + k * 30 + sway * 6)
        lf = skia.Path()
        lf.moveTo(tx, ty)
        ex, ey = tx + math.cos(an) * h * 0.42, ty + math.sin(an) * h * 0.22 + h * 0.12
        lf.quadTo((tx + ex) / 2, ty - h * 0.14, ex, ey)
        c.drawPath(lf, P("#14532D", a, stroke=10))
    c.restore()


def worker(c, x, y, h, t, pose="stand", lean=0.0, a=1.0, face=-1):
    """An ancient worker in a white linen kilt."""
    c.save()
    c.translate(x, y)
    c.rotate(lean)
    person(c, 0, 0, h, "#B07A4F", t, pose=pose, face=face, hat="none", hair="#1C1917", skin="#B07A4F",
           pants="#F5F5F4", a=a)
    c.restore()


def sledge(c, x, y, s, a=1.0, wet=0.0):
    """A wooden sledge with a block on it (x, y = front-bottom... centre of the runners)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    run = skia.Path()
    run.moveTo(-190, -10)
    run.lineTo(170, -10)
    run.quadTo(210, -12, 220, -44)
    run.lineTo(190, -44)
    run.quadTo(185, -30, 160, -30)
    run.lineTo(-190, -30)
    run.close()
    c.drawPath(run, P("#7C4A21", a))
    for bx in (-150, -50, 50, 150):
        c.drawRect(R(bx - 10, -52, 20, 24), P("#5B3415", a))
    c.drawRect(R(-200, -60, 380, 14), P("#8B5A2B", a))
    c.drawRect(R(-170, -280, 320, 222), lin_paint(-170, 0, 150, 0, ["#E7C18A", "#D9A766", "#B9874A"], a=a))
    c.drawRect(R(-170, -280, 320, 222), P("#7A4E26", a, stroke=4))
    for k in range(5):
        c.drawLine(-150 + k * 70, -270, -140 + k * 70, -70, P("#A8733F", 0.4 * a, stroke=3))
    c.restore()


def small_car(c, x, y, s, a=1.0):
    """A modern car silhouette for scale."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    body = skia.Path()
    body.moveTo(-210, -40)
    body.lineTo(-200, -110)
    body.lineTo(-120, -120)
    body.lineTo(-70, -180)
    body.lineTo(80, -180)
    body.lineTo(140, -120)
    body.lineTo(210, -105)
    body.lineTo(215, -40)
    body.close()
    c.drawPath(body, P("#60A5FA", 0.85 * a))
    c.drawRect(R(-60, -168, 60, 44), P("#DBEAFE", 0.8 * a))
    c.drawRect(R(10, -168, 60, 44), P("#DBEAFE", 0.8 * a))
    for wx in (-130, 130):
        c.drawCircle(wx, -40, 40, P("#1F2937", a))
        c.drawCircle(wx, -40, 16, P("#CBD5E1", a))
    c.restore()


def jar(c, x, y, s, tilt, a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(tilt)
    c.scale(s, s)
    jp = skia.Path()
    jp.moveTo(-26, -70)
    jp.lineTo(26, -70)
    jp.quadTo(54, -30, 30, 20)
    jp.lineTo(-30, 20)
    jp.quadTo(-54, -30, -26, -70)
    jp.close()
    c.drawPath(jp, P("#B45309", a))
    c.drawRect(R(-18, -86, 36, 18), P("#92400E", a))
    c.restore()


def boat(c, x, y, s, ang=0.0, a=1.0, cargo=GRANITE):
    """A Nile boat with a block (top view-ish icon), heading along ang (degrees)."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    hull = skia.Path()
    hull.moveTo(-60, 0)
    hull.quadTo(0, 30, 60, 0)
    hull.quadTo(0, -30, -60, 0)
    c.drawPath(hull, P("#7C4A21", a))
    c.drawRect(R(-26, -14, 36, 28), P(cargo, a))
    sail = skia.Path()
    sail.moveTo(20, 0)
    sail.lineTo(20, -70)
    sail.lineTo(64, -6)
    sail.close()
    c.drawPath(sail, P("#F8FAFC", a))
    c.restore()


def arrow(c, x0, y0, x1, y1, col, a=1.0, w=12, head=30):
    if a <= 0:
        return
    an = math.atan2(y1 - y0, x1 - x0)
    c.drawLine(x0, y0, x1 - math.cos(an) * head * 0.6, y1 - math.sin(an) * head * 0.6, P(col, a, stroke=w))
    hp = skia.Path()
    hp.moveTo(x1, y1)
    hp.lineTo(x1 - math.cos(an - 0.45) * head, y1 - math.sin(an - 0.45) * head)
    hp.lineTo(x1 - math.cos(an + 0.45) * head, y1 - math.sin(an + 0.45) * head)
    hp.close()
    c.drawPath(hp, P(col, a))


def compass(c, x, y, r, rot, a=1.0, ok=0.0):
    """Top view: the square base inside a compass ring with N; rot = the base's error in degrees."""
    if a <= 0:
        return
    c.drawCircle(x, y, r + 10, P("#000000", 0.4 * a, blur=14))
    c.drawCircle(x, y, r, P("#0F172A", 0.95 * a))
    c.drawCircle(x, y, r, P(mix("#94A3B8", GOOD, ok), a, stroke=6))
    nt = skia.Path()
    nt.moveTo(x, y - r + 8)
    nt.lineTo(x - 18, y - r + 44)
    nt.lineTo(x + 18, y - r + 44)
    nt.close()
    c.drawPath(nt, P(WARN, a))
    word(c, "N", x, y - r - 18, 40, "#F8FAFC", a)
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    q = r * 0.5
    c.drawRect(R(-q, -q, 2 * q, 2 * q), P("#D9A766", a))
    c.drawLine(-q, -q, q, q, P("#7A4E26", a, stroke=4))
    c.drawLine(q, -q, -q, q, P("#7A4E26", a, stroke=4))
    c.restore()


def level_tool(c, x, y, w, off, a=1.0):
    """A spirit level: the bubble sits off-centre by 'off' (0 = level)."""
    if a <= 0:
        return
    c.drawRRect(rr(x - w / 2, y - 26, w, 52, 14), P("#F59E0B", a))
    c.drawRRect(rr(x - 70, y - 16, 140, 32, 16), P("#ECFCCB", a))
    c.drawLine(x - 24, y - 16, x - 24, y + 16, P("#365314", a, stroke=3))
    c.drawLine(x + 24, y - 16, x + 24, y + 16, P("#365314", a, stroke=3))
    c.drawOval(R(x - 20 + off * 46, y - 11, 40, 22), P("#A3E635", a))


def books(c, x, y, k, a=1.0):
    cols = ("#DC2626", "#2563EB", "#16A34A", "#F59E0B", "#7C3AED", "#0EA5E9")
    for i, col in enumerate(cols):
        bx = x - 120 + i * 42
        fall = clamp(k * 1.4 - i * 0.08)
        c.save()
        c.translate(bx + fall * (i - 2.5) * 30, y - fall * fall * 0 + fall * 520)
        c.rotate(fall * (40 + i * 25) * (1 if i % 2 else -1))
        c.drawRect(R(-16, -90, 32, 90), P(col, a))
        c.drawRect(R(-16, -70, 32, 8), P("#FFFFFF", 0.6 * a))
        c.restore()


# ====================================================================================== the episode
class Pyramid(EpisodeV2):
    BUILD_NO = 36
    FIRST_SET = "giza"
    CLEAR = "#160F2E"
    TITLE = {"en": "GREAT PYRAMID", "ar_sa": "الهرم الأكبر"}
    EMPH = {"en": ["CONGRATS", "STACK", "TWO", "MILLION", "STONE", "BLOCKS", "MOUNTAIN", "GLEAMED", "WHITE", "GREAT",
                   "PYRAMID", "GIZA", "OUTWEIGH", "CAR", "SLEDGE", "DIGS", "POUR", "WATER", "FIRM", "HALF", "CREW",
                   "ACROSS", "RIVER", "GRANITE", "NINE", "HUNDRED", "FLOAT", "BOATS", "NILE", "HARBOR", "KING'S",
                   "DEEP", "ROOF", "FIVE", "EMPTY", "ROOMS", "BEAMS", "POINTED", "PUSHES", "ASIDE", "BASE", "HAND",
                   "CORNERS", "NEVER", "LEVEL", "CENTIMETERS", "NORTH", "TENTH", "DEGREE", "FOLLOW", "WIND", "TOWER",
                   "COOLS", "THOUSANDS", "WORKERS", "SLAVES", "POLISHED", "FORTY-SIX", "TALLEST", "THIRTY-EIGHT",
                   "CENTURIES", "YOURSELF", "FORTY-FIVE", "STANDS", "SHELF", "FLOOR"],
            "ar_sa": ["مبروك", "رصيت", "مليونين", "حجر", "جبل", "أبيض", "وبيلمع", "الهرم", "الأكبر", "أتقل", "عربية",
                      "والزلاجة", "بتغرز", "فتصب", "مية", "بتتماسك", "ونص", "الرجالة", "الأبيض", "البر", "التاني",
                      "والجرانيت", "أسوان", "تسعمية", "مراكب", "النيل", "ميناء", "أوضة", "الملك", "جوة", "سقفها",
                      "خمس", "فاضية", "بكمرات", "جرانيت", "مدبب", "يزق", "الجناب", "القاعدة", "مايلة", "شبر", "الأركان",
                      "فتظبط", "اتنين", "سنتي", "الشمال", "كسر", "تابعني", "برج", "هوا", "بيبرد", "آلاف", "العمال",
                      "عبيد", "ملمع", "وأطول", "قرن", "بإيدك", "واقف", "والرف", "الصنايعي", "وقع"]}
    KEYS = {"ar_sa": {
        ("hook", "STACK"): "رصيت", ("hook", "MILLION"): "مليونين", ("hook", "MOUNTAIN"): "جبل", ("hook", "GLEAMED"): "وبيلمع",
        ("hook", "CONGRATS"): "مبروك", ("hook", "PYRAMID"): "الهرم",
        ("break1", "OUTWEIGH"): "أتقل", ("break1", "CAR"): "عربية", ("break1", "SLEDGE"): "والزلاجة", ("break1", "DIGS"): "بتغرز",
        ("fix1", "POUR"): "فتصب", ("fix1", "WATER"): "مية", ("fix1", "FIRM"): "بتتماسك", ("fix1", "HALF"): "ونص",
        ("fix1", "PULL"): "يشدوها",
        ("break2", "WHITE"): "الأبيض", ("break2", "RIVER"): "البر", ("break2", "GRANITE"): "والجرانيت", ("break2", "NINE"): "تسعمية",
        ("fix2", "FLOAT"): "فتنقلهم", ("fix2", "BOATS"): "مراكب", ("fix2", "NILE"): "النيل", ("fix2", "HARBOR"): "ميناء",
        ("break3", "KING"): "الملك", ("break3", "DEEP"): "جوة", ("break3", "MOUNTAIN"): "جبل", ("break3", "ROOF"): "سقفها",
        ("fix3", "FIVE"): "خمس", ("fix3", "EMPTY"): "فاضية", ("fix3", "GRANITE"): "بكمرات", ("fix3", "POINTED"): "مدبب",
        ("fix3", "PUSHES"): "يزق", ("fix3", "ASIDE"): "الجناب",
        ("break4", "BASE"): "القاعدة", ("break4", "HAND"): "شبر", ("break4", "CORNERS"): "الأركان", ("break4", "TOP"): "فوق",
        ("fix4", "LEVEL"): "فتظبط", ("fix4", "TWO"): "اتنين", ("fix4", "NORTH"): "الشمال", ("fix4", "DEGREE"): "درجة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "THOUSANDS"): "آلاف", ("reveal", "WORKERS"): "العمال", ("reveal", "SLAVES"): "عبيد",
        ("reveal", "CASE"): "ولبسه", ("reveal", "POLISHED"): "ملمع",
        ("stat", "HUNDRED"): "مية", ("stat", "TWO"): "مليونين", ("stat", "TALLEST"): "وأطول",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "CENTURIES"): "سنة", ("tag", "STANDS"): "واقف", ("tag", "SHELF"): "والرف", ("tag", "FLOOR"): "وقع"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a wind tower"),
                   "stat": [("146 m", "TALL WHEN NEW"), ("2,300,000", "BLOCKS"), ("3,800", "YEARS THE TALLEST")],
                   "L": {"blocks": "2.3 MILLION BLOCKS", "white": "IT GLEAMED WHITE", "gp": "THE GREAT PYRAMID",
                         "car": "HEAVIER THAN A CAR", "digs": "IT DIGS IN", "water": "WATER ON THE SAND",
                         "firm": "WET SAND = FIRM", "half": "HALF THE CREW", "tura": "WHITE STONE: TURA",
                         "river": "ACROSS THE RIVER", "aswan": "GRANITE: ASWAN", "km": "900 km", "giza": "GIZA",
                         "boats": "BY BOAT, DOWN THE NILE", "harbor": "HARBOR BY THE SITE", "king": "KING'S ROOM",
                         "weight": "A MOUNTAIN OF STONE", "crack": "CRACKS!", "five": "5 EMPTY ROOMS",
                         "beams": "GRANITE BEAMS", "pointed": "POINTED ROOF", "aside": "WEIGHT PUSHED ASIDE",
                         "off": "BASE OFF BY A HAND", "miss": "CORNERS DON'T MEET", "level": "LEVEL TO 2 cm",
                         "north": "< 0.1° OFF NORTH", "workers": "THOUSANDS OF WORKERS", "slaves": "NOT SLAVES",
                         "polish": "POLISHED WHITE CASING", "still": "4,500 YEARS: STILL STANDING",
                         "week": "1 WEEK: ON THE FLOOR"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: برج هوا"),
                      "stat": [("146", "متر وهو جديد"), ("2,300,000", "حجر"), ("3,800", "سنة أطول مبنى")],
                      "L": {"blocks": "مليونين وتلتمية ألف حجر", "white": "كان أبيض وبيلمع", "gp": "الهرم الأكبر",
                            "car": "أتقل من عربية", "digs": "بتغرز", "water": "مية على الرملة",
                            "firm": "الرملة المبلولة بتتماسك", "half": "نص الرجالة بس", "tura": "الحجر الأبيض: طرة",
                            "river": "في البر التاني", "aswan": "الجرانيت: أسوان", "km": "900 كيلو", "giza": "الجيزة",
                            "boats": "مراكب في النيل", "harbor": "ميناء جنب الموقع", "king": "أوضة الملك",
                            "weight": "جبل حجارة", "crack": "هيتشرخ!", "five": "خمس أوض فاضية",
                            "beams": "كمرات جرانيت", "pointed": "سقف مدبب", "aside": "التقل على الجناب",
                            "off": "القاعدة مايلة شبر", "miss": "الأركان مش بتتقابل", "level": "مظبوطة لحد 2 سنتي",
                            "north": "على الشمال بالظبط", "workers": "آلاف العمال", "slaves": "مش عبيد",
                            "polish": "حجر أبيض ملمع", "still": "4,500 سنة: لسه واقف", "week": "الرف: وقع النهارده"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "stack": ("hook", "STACK", 0.05), "million": ("hook", "MILLION", 0.2), "mountain": ("hook", "MOUNTAIN", 0.45),
            "gleamed": ("hook", "GLEAMED", 0.6), "congrats": ("hook", "CONGRATS", 0.7), "pyramid": ("hook", "PYRAMID", 0.9),
            "outweigh": ("break1", "OUTWEIGH", 0.2), "car": ("break1", "CAR", 0.4), "sledge": ("break1", "SLEDGE", 0.6),
            "digs": ("break1", "DIGS", 0.85),
            "pour": ("fix1", "POUR", 0.1), "water": ("fix1", "WATER", 0.2), "firm": ("fix1", "FIRM", 0.5),
            "half": ("fix1", "HALF", 0.7), "pull": ("fix1", "PULL", 0.9),
            "white": ("break2", "WHITE", 0.15), "river": ("break2", "RIVER", 0.4), "granite": ("break2", "GRANITE", 0.6),
            "nine": ("break2", "NINE", 0.8),
            "float": ("fix2", "FLOAT", 0.1), "boats": ("fix2", "BOATS", 0.3), "nile": ("fix2", "NILE", 0.5),
            "harbor": ("fix2", "HARBOR", 0.75),
            "king": ("break3", "KING", 0.2), "deep": ("break3", "DEEP", 0.4), "mount3": ("break3", "MOUNTAIN", 0.7),
            "roof": ("break3", "ROOF", 0.9),
            "five": ("fix3", "FIVE", 0.15), "empty": ("fix3", "EMPTY", 0.3), "granite3": ("fix3", "GRANITE", 0.4),
            "pointed": ("fix3", "POINTED", 0.65), "pushes": ("fix3", "PUSHES", 0.75), "aside": ("fix3", "ASIDE", 0.92),
            "base": ("break4", "BASE", 0.2), "hand": ("break4", "HAND", 0.45), "corners": ("break4", "CORNERS", 0.65),
            "top": ("break4", "TOP", 0.92),
            "level": ("fix4", "LEVEL", 0.1), "two": ("fix4", "TWO", 0.3), "north": ("fix4", "NORTH", 0.55),
            "degree": ("fix4", "DEGREE", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "thousands": ("reveal", "THOUSANDS", 0.15), "workers": ("reveal", "WORKERS", 0.3), "slaves": ("reveal", "SLAVES", 0.45),
            "case": ("reveal", "CASE", 0.65), "polished": ("reveal", "POLISHED", 0.8),
            "s1": ("stat", "HUNDRED", 0.04), "s2": ("stat", "TWO", 0.35), "s3": ("stat", "TALLEST", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "cent": ("tag", "CENTURIES", 0.2), "stands": ("tag", "STANDS", 0.4), "shelf": ("tag", "SHELF", 0.6),
            "floor": ("tag", "FLOOR", 0.85)})
        T["built"] = max(min(T["mountain"], T["gleamed"]) - 0.1, 1.6)
        T["shine"] = max(T["gleamed"] - 0.2, T["built"] + 0.2)
        T["poured"] = max(min(T["pour"], T["water"]) - 0.1, s("fix1") + 0.1)
        T["slide"] = max(T["firm"] - 0.1, T["poured"] + 0.6)
        T["sail"] = max(min(T["float"], T["boats"]) - 0.1, s("fix2") + 0.05)
        T["crack"] = max(T["roof"] - 0.1, T["king"] + 0.6)
        T["rooms"] = max(min(T["five"], T["empty"]) - 0.15, s("fix3") + 0.05)
        T["gable"] = max(T["pointed"] - 0.15, T["rooms"] + 0.8)
        T["fixb"] = max(T["level"] - 0.1, s("fix4") + 0.05)
        T["cas2"] = max(min(T["case"], T["polished"]) - 0.2, T["slaves"] + 0.3)
        T["fall"] = max(T["floor"] - 0.5, T["shelf"] + 0.2)
        # ---- sets
        self.cut(s("break1") - 0.12, "sledge", 1)
        self.cut(s("break2") - 0.12, "nile", -1)
        self.cut(s("break3") - 0.12, "inside", 1)
        self.cut(s("break4") - 0.12, "base", -1)
        self.cut(s("reveal") - 0.12, "giza", 1)
        self.cut(s("tag") - 0.2, "shelf", 1)
        # ---- cameras
        cm = Camera(0, -300, 0.9)
        cm.key(0.05, 0, -300, 0.88, 1.0)
        cm.key(T["shine"], 0, -330, 0.94, 1.6)
        cm.key(s("reveal") - 0.12, 80, -150, 1.12, 0.0).key(T["workers"], 40, -160, 1.05, 1.6)
        cm.key(T["cas2"], 0, -300, 0.88, 1.2)
        cm.key(s("stat") - 0.12, 0, -400, 0.8, 0.0).key(s("stat"), 0, -400, 0.82, 3.0)
        cm.key(s("closer") - 0.1, 0, -186, 0.85, 1.0)
        self.cam = cm
        ci = Camera(0, -420, 0.72)
        ci.key(T["king"] - 0.3, 0, -330, 1.25, 1.2)
        ci.key(s("fix3") - 0.12, 0, -420, 1.15, 0.8)
        self.cami = ci
        self.built = Track(0.3).to(0.05, 1.0, max(1.0, T["built"] - 0.05), e_out)
        self.casing = Track(0.0).to(T["shine"], 1.0, 0.6).to(s("break1") - 0.12, 0.0, 0.0)
        self.casing.to(s("reveal") - 0.12, 0.0, 0.0).to(T["cas2"], 1.0, 0.9)
        self.slide = Track(0.0).to(T["slide"], 380.0, max(1.0, s("break2") - 0.3 - T["slide"]), e_io)
        self.tiltb = Track(1.0).to(T["fixb"], 0.0, 0.8)
        self.rotn = Track(9.0).to(T["north"] - 0.2, 0.0, 0.8)
        self.spans = [(T["digs"], T["pull"] + 0.3), (T["nine"], T["harbor"] + 0.3), (T["roof"], T["aside"] + 0.3),
                      (T["top"], T["degree"] + 0.3)]
        self.shakes = [(T["built"], 0.3, 6), (T["congrats"], 0.3, 8), (T["digs"], 0.3, 6), (T["crack"], 0.45, 12),
                       (T["fixb"] + 0.5, 0.25, 5), (T["fall"] + 0.3, 0.35, 10), (s("closer") + 0.2, 0.35, 10)]
        rng = random.Random(36)
        self.dunes = [(rng.uniform(-1600, 1600), rng.uniform(60, 160)) for _ in range(9)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def plateau(self, c, t, cam, nile=True):
        """Dusk sky, sun, far dunes and the two smaller pyramids (screen space), then the ground and the Nile (world)."""
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 40 * z)
        v2.stars(c, W, H, t, 0.5)
        sx, sy = 210 - cx * 0.05, gy - 620 * z
        add_glow(c, sx, sy, 300, "#FF8A4C", 0.5)
        c.drawCircle(sx, sy, 62, P("#FFD39A", 0.95))
        self.view(c, cam)
        for (dx, hgt) in self.dunes:
            c.drawOval(R(dx - 500, -hgt * 0.5 - 30, 1000, hgt), P("#9C5B3B", 0.9))
        pyramid(c, -1050, -40, 0.42, t)                                   # Khafre and Menkaure behind
        pyramid(c, 1050, -30, 0.3, t)
        vrect(c, cx - 1200 / z, -40, 2400 / z, 3000, [SAND[0], SAND[1], SAND[2], SAND[3]], [0, 0.08, 0.35, 1])
        if nile:
            vrect(c, cx - 1200 / z, 300, 2400 / z, 160, ["#3B82F6", NILE, "#1E3A8A"])
            for i in range(9):
                xx = -1100 + i * 280 + 40 * math.sin(i * 2.1)
                palm(c, xx, 300, 230 + 40 * (i % 3), sway=math.sin(t * 1.3 + i) * 0.4)
            vrect(c, cx - 1200 / z, 460, 2400 / z, 3000, ["#14532D", "#0F3D21", "#06180D"])
        return gy

    # ------------------------------------------------------------------ set: giza (hook, reveal, stat, closer)
    def draw_giza(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        self.plateau(c, t, cam)
        built = self.built.at(t) if t < s("break1") else 1.0
        cas = self.casing.at(t)
        gl = -1.0
        if t < s("break1"):
            gl = prog(t, T["shine"] + 0.2, T["shine"] + 1.6)
        elif t >= s("reveal") - 0.12:
            gl = prog(t, T["cas2"] + 0.4, T["cas2"] + 1.8)
            if t >= s("stat") - 0.12:
                gl = ((t - s("stat")) * 0.35) % 1.4 - 0.2
        glow = prog(t, s("closer"), s("closer") + 0.5) if t >= s("closer") - 0.1 else 0.0
        pyramid(c, 0, 0, 1.0, t, built=built, casing=cas, glint=gl, glow=glow)
        if s("reveal") - 0.12 <= t < s("stat") - 0.12:                     # thousands of workers
            k = prog(t, T["thousands"] - 0.3, T["thousands"] + 0.3)
            rng = random.Random(5)
            for i in range(60):
                wx = rng.uniform(-900, 900)
                wy = rng.uniform(40, 140)
                worker(c, wx + math.sin(t * 2 + i) * 6, wy, 54 + wy * 0.08, t + i, pose="walk" if i % 3 else "carry",
                       a=k, face=1 if i % 2 else -1)
        c.restore()
        self.ui["cam"] = cam

    def ui_giza(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            self.chip(540, 470, "blocks", T["million"] - 0.1, T["shine"], accent="#E7C18A", size=38)
            self.chip(540, 470, "white", T["shine"], T["pyramid"] - 0.1, accent="#FFFFFF", size=40)
            self.chip(540, 470, "gp", T["pyramid"] - 0.1, s("break1") + 0.1, accent=HILITE, size=44)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            self.chip(540, 470, "workers", T["thousands"] - 0.1, T["slaves"] - 0.1, accent="#E7C18A", size=40)
            self.chip(540, 470, "slaves", T["slaves"] - 0.1, T["cas2"], accent=GOOD, size=44)
            self.chip(540, 470, "polish", T["cas2"], s("stat") - 0.15, accent="#FFFFFF", size=40)

    # ------------------------------------------------------------------ set: sledge (break1, fix1)
    def draw_sledge(self, c, t):
        T, s = self.T, self.tl.s
        cam = (180, -240, 0.98)
        self.plateau(c, t, cam, nile=False)
        pyramid(c, 260, -160, 0.62, t, built=0.55)
        fixed = t >= s("fix1") - 0.12
        d = self.slide.at(t) if fixed else 0.0
        bx = 330 - d
        wet = prog(t, T["poured"] + 0.2, T["poured"] + 0.8) if fixed else 0.0
        c.drawOval(R(bx - 520, -18, 330, 36), P("#5B3A1E", 0.75 * wet))
        if not fixed:                                                    # the pile of sand it pushes up
            pk = prog(t, T["sledge"] - 0.3, T["digs"] + 0.2)
            pile = skia.Path()
            pile.moveTo(bx - 330, 0)
            pile.quadTo(bx - 250, -90 * pk, bx - 185, -30 * pk)
            pile.lineTo(bx - 185, 0)
            pile.close()
            c.drawPath(pile, P(SAND[1]))
        if not fixed:
            small_car(c, bx + 250, -40, 0.55, a=prog(t, T["car"] - 0.3, T["car"]) * (1 - prog(t, s("fix1") - 0.4, s("fix1") - 0.12)))
        sledge(c, bx, 10 if not fixed else 0, 1.0)
        # ropes and the crew
        crew = 8
        sit = prog(t, T["half"] - 0.2, T["half"] + 0.3) if fixed else 0.0
        for i in range(crew):
            wx = bx - 420 - i * 92
            pulling = not (fixed and i % 2 == 1 and sit > 0.5)
            lean = (-18 if not fixed else -10) if pulling else 0
            if pulling:
                c.drawLine(bx - 190, -40, wx + 6, -100, P("#C8A165", 1, stroke=5))
            worker(c, wx, 0, 190, t + i * 0.3, pose="carry" if pulling else ("sit" if sit > 0.8 else "cheer"),
                   lean=lean + (math.sin(t * 9 + i) * 3 if not fixed else 0), face=-1)
        if fixed:                                                        # the water man and his jar
            mx = bx - 260
            worker(c, mx, 0, 190, t, pose="carry", face=-1)
            tilt = 70 * prog(t, T["poured"] - 0.2, T["poured"] + 0.2) * (1 - prog(t, T["firm"] + 0.6, T["firm"] + 1.0))
            jar(c, mx - 50, -120, 0.9, -tilt)
            if tilt > 30:
                for i in range(10):
                    q = (t * 2.5 + i / 10.0) % 1.0
                    c.drawCircle(mx - 110 - q * 40, -120 + q * 120, 8, P("#93C5FD", 0.85))
        c.restore()
        self.ui["cam"] = cam
        self.ui["block"] = (bx, -280)

    def ui_sledge(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (180, -240, 0.98))
        bx, by = self.ui.get("block", (330, -280))
        sx, sy = self.at(cam, bx, by)
        if tw < s("fix1") - 0.12:
            self.chip(540, 470, "car", T["outweigh"] - 0.1, T["digs"] - 0.1, accent=HILITE, size=40)
            px, py = self.at(cam, bx - 260, -60)
            self.label(px, py, 300, 600, "digs", T["digs"] - 0.15, s("fix1") - 0.15, WARN, size=38)
            self.badge("alert", T["digs"] + 0.05, s("fix1") - 0.2, x=880, y=330)
            self.red(T["digs"] + 0.05, 1.4)
            return
        wx, wy = self.at(cam, bx - 330, -10)
        self.label(wx, wy, 300, 600, "water", T["poured"], T["firm"] - 0.1, "#93C5FD", size=36)
        self.chip(540, 470, "firm", T["firm"] - 0.1, T["half"] - 0.1, accent="#93C5FD", size=38)
        self.chip(540, 470, "half", T["half"] - 0.1, s("break2") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["pull"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: nile (break2, fix2)
    def river_pts(self):
        return [(560, 380), (600, 470), (575, 560), (610, 660), (640, 760), (600, 860), (630, 960), (700, 1060),
                (690, 1150), (720, 1240)]

    def at_river(self, q):
        pts = self.river_pts()
        f = clamp(q) * (len(pts) - 1)
        i = min(int(f), len(pts) - 2)
        u = f - i
        return lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u)

    def draw_nile(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#C9A066", "#B98A52", "#A5743F"])
        rng = random.Random(3)
        for i in range(40):
            c.drawOval(R(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(80, 240), rng.uniform(20, 60)), P("#D8B47C", 0.35))
        dl = skia.Path()                                                  # the delta
        dl.moveTo(560, 380)
        dl.lineTo(380, 150)
        dl.quadTo(560, 110, 760, 150)
        dl.close()
        c.drawPath(dl, P("#4D7C0F", 0.9))
        pts = self.river_pts()
        rp = skia.Path()
        rp.moveTo(*pts[0])
        for p_ in pts[1:]:
            rp.lineTo(*p_)
        c.drawPath(rp, P("#4D7C0F", 0.9, stroke=70))
        c.drawPath(rp, P(NILE, 1, stroke=24))
        c.drawRect(R(0, 0, W, 120), P("#1E3A8A", 0.9))                   # the Mediterranean
        gz = (520, 420)
        pyramid(c, gz[0] - 40, gz[1] + 20, 0.08, t)
        c.drawCircle(gz[0], gz[1], 14, P("#FFFFFF"))
        tura = (640, 450)
        c.drawCircle(tura[0], tura[1], 14, P("#F8FAFC"))
        asw = self.at_river(1.0)
        c.drawCircle(asw[0], asw[1], 16, P(GRANITE))
        c.drawCircle(asw[0], asw[1], 16, P("#FFFFFF", 1, stroke=4))
        if t >= T["nine"] - 0.2 and t < s("fix2") + 0.2:                  # 900 km dimension line
            k = prog(t, T["nine"] - 0.2, T["nine"] + 0.3)
            c.drawLine(880, gz[1], 880, lerp(gz[1], asw[1], k), P("#FFFFFF", 0.9, stroke=6))
            c.drawLine(850, gz[1], 910, gz[1], P("#FFFFFF", 0.9, stroke=6))
            if k >= 1:
                c.drawLine(850, asw[1], 910, asw[1], P("#FFFFFF", 0.9, stroke=6))
        if t >= s("fix2") - 0.12:
            for i in range(4):                                            # boats sail down from Aswan
                q = 1.0 - prog(t, T["sail"] + i * 0.35, T["sail"] + i * 0.35 + 2.2)
                if q >= 1.0 or q <= 0.0:
                    continue
                bx, by = self.at_river(q)
                bx2, by2 = self.at_river(max(0.0, q - 0.02))
                boat(c, bx, by, 0.9, math.degrees(math.atan2(by2 - by, bx2 - bx)))
            q = prog(t, T["sail"], T["sail"] + 1.4)                       # a boat crosses from Tura
            if 0 < q < 1:
                boat(c, lerp(tura[0], gz[0] + 20, q), lerp(tura[1], gz[1], q), 0.8, 180, cargo="#F8FAFC")
            hk = prog(t, T["harbor"] - 0.3, T["harbor"])
            if hk > 0:
                c.drawRect(R(gz[0] - 70, gz[1] + 40, 60, 16 * hk), P("#7C4A21"))
                c.drawRect(R(gz[0] - 70, gz[1] + 40, 16, 60 * hk), P("#7C4A21"))
                add_glow(c, gz[0] - 40, gz[1] + 50, 70, GOOD, 0.6 * hk)
        self.ui["gz"], self.ui["tura"], self.ui["asw"] = gz, tura, asw

    def ui_nile(self, c, t, tw):
        T, s = self.T, self.tl.s
        gz, tura, asw = self.ui.get("gz", (520, 420)), self.ui.get("tura", (640, 450)), self.ui.get("asw", (720, 1240))
        word(c, self.L["giza"], gz[0] - 120, gz[1] + 8, 34, "#FFFFFF", self.span(s("break2") - 0.1, s("break3") - 0.2))
        if tw < s("fix2") - 0.12:
            self.label(tura[0], tura[1], 820, 560, "tura", T["white"] - 0.1, s("fix2") - 0.15, "#F8FAFC", size=32)
            self.chip(820, 650, "river", T["river"] - 0.1, s("fix2") - 0.15, accent="#93C5FD", size=30)
            self.label(asw[0], asw[1], 330, 1150, "aswan", T["granite"] - 0.1, s("fix2") - 0.15, GRANITE, size=34)
            self.chip(880, 820, "km", T["nine"] - 0.1, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["nine"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["nine"] + 0.05, 1.3)
            return
        self.chip(330, 900, "boats", T["boats"] - 0.1, T["harbor"] - 0.2, accent="#93C5FD", size=34)
        self.label(gz[0] - 40, gz[1] + 50, 300, 640, "harbor", T["harbor"] - 0.1, s("break3") - 0.15, GOOD, size=34)
        self.badge("check", T["harbor"] + 0.1, s("break3") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: inside (break3, fix3)
    def draw_inside(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cami.at(t)
        vrect(c, 0, 0, W, H, ["#1A1033", "#2B1B4A", "#1A1033"])
        self.view(c, cam)
        hw, hh = 760.0, 968.0
        tri = _tri((0, -hh), (-hw, 0), (hw, 0))
        c.drawPath(tri, lin_paint(-hw, 0, hw, 0, ["#B9874A", "#D9A766", "#A8733F"]))
        c.save()
        c.clipPath(tri, doAntiAlias=True)
        for k in range(1, 44):
            yy = -k * 22
            c.drawLine(-hw, yy, hw, yy, P("#7A4E26", 0.45, stroke=2))
            for j in range(-20, 21):
                xx = j * 60 + (30 if k % 2 else 0)
                c.drawLine(xx, yy, xx, yy + 22, P("#7A4E26", 0.25, stroke=1.5))
        c.restore()
        c.drawPath(tri, P("#5B3415", 1, stroke=6))
        ky = -300.0                                                        # the king's room
        c.drawLine(-260, -60, -40, ky + 40, P("#3B2410", 1, stroke=34))     # the grand gallery
        c.drawRect(R(-110, ky - 90, 220, 90), P("#1C1206"))
        c.drawRect(R(-110, ky - 90, 220, 90), P(GRANITE, 1, stroke=6))
        c.drawRect(R(-40, ky - 50, 80, 40), P("#57534E"))                  # the sarcophagus
        fixed = t >= s("fix3") - 0.12
        cr = prog(t, T["crack"], T["crack"] + 0.3) if not fixed else 0.0
        if not fixed:
            wk = prog(t, T["mount3"] - 0.3, T["mount3"] + 0.2)
            for i in range(5):
                xx = -80 + i * 40
                q = (t * 1.2 + i * 0.2) % 1.0
                arrow(c, xx, ky - 330 + q * 60, xx, ky - 120 + q * 20, WARN, a=wk * 0.95, w=10, head=26)
            if cr > 0:
                cp = skia.Path()
                cp.moveTo(-60, ky - 90)
                cp.lineTo(-40, ky - 70 * cr - 20)
                cp.lineTo(-10, ky - 80)
                cp.lineTo(20, ky - 60 * cr - 30)
                cp.lineTo(50, ky - 90)
                c.drawPath(cp, P("#FDE68A", cr, stroke=5))
        else:
            n = 5
            for i in range(n):                                             # five relieving rooms
                q = prog(t, T["rooms"] + i * 0.22, T["rooms"] + i * 0.22 + 0.3)
                if q <= 0:
                    continue
                yy = ky - 90 - (i + 1) * 46
                c.drawRect(R(-120, yy - 8 * q, 240, 12 * q), P(GRANITE, 1))
                c.drawRect(R(-110, yy + 4, 220, 30 * q), P("#1C1206", 0.9))
                for j in range(5):
                    c.drawLine(-120 + j * 60, yy - 8, -120 + j * 60, yy + 4, P("#7F5F5B", q, stroke=2))
            gk = prog(t, T["gable"], T["gable"] + 0.4)
            top = ky - 90 - 5 * 46 - 14
            if gk > 0:
                g = skia.Path()
                g.moveTo(-170, top)
                g.lineTo(0, top - 110 * gk)
                g.lineTo(170, top)
                c.drawPath(g, P("#E7C18A", 1, stroke=26))
                ak = prog(t, T["pushes"] - 0.2, T["pushes"] + 0.3)
                for sd in (-1, 1):
                    q = (t * 1.1) % 1.0
                    arrow(c, 0 + sd * 10, top - 300 + q * 40, sd * 260, top - 40 + q * 20, GOOD, a=ak, w=12, head=30)
                    arrow(c, sd * 120, top - 330, sd * 330, top - 20, GOOD, a=ak * 0.7, w=10, head=26)
        c.restore()
        self.ui["cam"] = cam
        self.ui["ky"] = ky

    def ui_inside(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cami.at(tw))
        ky = self.ui.get("ky", -300)
        kx, kyy = self.at(cam, 110, ky - 45)
        if tw < s("fix3") - 0.12:
            self.label(kx, kyy, 820, 1150, "king", T["king"] - 0.1, s("fix3") - 0.15, GRANITE, size=36)
            self.chip(540, 470, "weight", T["mount3"] - 0.15, T["crack"], accent=WARN, size=38)
            self.chip(540, 470, "crack", T["crack"], s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["roof"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["crack"], 1.5)
            return
        rx, ry = self.at(cam, -120, ky - 90 - 3 * 46)
        self.label(rx, ry, 250, 1150, "five", T["rooms"], T["gable"] + 0.4, "#E7C18A", size=34)
        bx, by = self.at(cam, 120, ky - 90 - 2 * 46)
        self.label(bx, by, 830, 1150, "beams", T["granite3"] - 0.1, s("break4") - 0.15, GRANITE, size=34)
        self.chip(540, 470, "pointed", T["gable"], T["pushes"] - 0.1, accent="#E7C18A", size=38)
        self.chip(540, 470, "aside", T["pushes"] - 0.1, s("break4") - 0.15, accent=GOOD, size=38)
        self.badge("check", T["aside"] + 0.1, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: base (break4, fix4, cta)
    def draw_base(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0F172A", "#1E1B4B", "#0F172A"])
        for k in range(16):                                                 # blueprint grid
            c.drawLine(k * 80, 0, k * 80, H, P("#312E81", 0.5, stroke=2))
        for k in range(26):
            c.drawLine(0, k * 80, W, k * 80, P("#312E81", 0.5, stroke=2))
        e_ = self.tiltb.at(t)
        cx_, gy, hw, hh = 540, 1080, 380, 480
        Lx, Ly = cx_ - hw, gy + 46 * e_
        Rx, Ry = cx_ + hw, gy - 46 * e_
        gap = 70 * e_
        tl_ = (cx_ - gap, gy - hh + 30 * e_)
        tr_ = (cx_ + gap, gy - hh - 40 * e_)
        c.drawLine(Lx, Ly, Rx, Ry, P(mix(GOOD, WARN, e_), 1, stroke=10))
        lf = _tri(tl_, (Lx, Ly), (cx_, (Ly + Ry) / 2))
        rf = _tri(tr_, (cx_, (Ly + Ry) / 2), (Rx, Ry))
        c.drawPath(lf, P("#D9A766", 0.9))
        c.drawPath(rf, P("#A8733F", 0.9))
        c.drawPath(lf, P("#FDE68A", 1, stroke=4))
        c.drawPath(rf, P("#FDE68A", 1, stroke=4))
        if e_ > 0.05:
            c.drawCircle(cx_, gy - hh - 5, 90 * e_ + 20, P(WARN, 0.9 * e_, stroke=8))
        else:
            add_glow(c, cx_, gy - hh, 90, GOOD, 0.6)
        lk = prog(t, T["fixb"] - 0.1, T["fixb"] + 0.3) if t >= s("fix4") - 0.12 else 0.0
        level_tool(c, cx_, gy + 110, 420, e_ * 1.0, a=lk if lk > 0 else prog(t, T["hand"] - 0.3, T["hand"]))
        ck = prog(t, T["north"] - 0.4, T["north"]) if t >= s("fix4") - 0.12 else 0.0
        compass(c, 820, 620, 150, self.rotn.at(t), a=ck, ok=prog(t, T["north"] + 0.6, T["north"] + 1.0))

    def ui_base(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 470, "off", T["hand"] - 0.15, T["corners"] - 0.1, accent=WARN, size=38)
            self.chip(540, 470, "miss", T["corners"] - 0.1, s("fix4") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["top"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["top"] + 0.05, 1.3)
            return
        if tw < s("cta") - 0.12:
            self.chip(330, 470, "level", T["two"] - 0.15, s("cta") - 0.15, accent=GOOD, size=34)
            self.chip(820, 830, "north", T["degree"] - 0.6, s("cta") - 0.15, accent=GOOD, size=32)
            self.badge("check", T["degree"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: shelf (tag)
    def draw_shelf(self, c, t):
        T = self.T
        room(c, 0, 0, W, 1250, wall="#5B4636", floor="#3F2F24", t=t, lamp=True, lamp_x=760)
        vrect(c, 0, 1250, W, H - 1250, ["#3F2F24", "#2A1F18", "#150F0B"])
        c.drawRect(R(130, 360, 400, 300), P("#3B2410"))                     # the framed pyramid
        c.save()
        c.clipRect(R(150, 380, 360, 260))
        vrect(c, 150, 380, 360, 260, ["#2A1B5C", "#E0795A", "#FFB070"])
        pyramid(c, 330, 600, 0.26, t, casing=1.0)
        c.drawRect(R(150, 600, 360, 40), P(SAND[1]))
        c.restore()
        add_glow(c, 330, 510, 260, "#FDE68A", 0.25 * prog(t, T["cent"] - 0.2, T["cent"] + 0.3))
        fk = prog(t, T["fall"], T["fall"] + 0.5)
        c.save()
        c.translate(740, 760)
        c.rotate(fk * 38)
        c.translate(0, fk * fk * 480)
        c.drawRect(R(-200, 0, 400, 22), P("#A16207"))
        c.restore()
        c.drawRect(R(540, 750, 14, 30), P("#94A3B8"))
        c.drawRect(R(930, 750, 14, 30), P("#94A3B8"))
        books(c, 740, 760, fk)
        if self.rtl:                                                       # the handyman, shrugging
            person(c, 860, 1250, 300, "#475569", t, pose="shrug" if fk > 0.5 else "stand", face=-1, hat="cap",
                   hair="#1F1A17", skin="#C68B5E", pants="#1E3A8A")
            c.drawRRect(rr(930, 1170, 90, 60, 8), P("#DC2626"))
        else:
            c.save()                                                       # the drill on the floor
            c.translate(880, 1220)
            c.rotate(-10)
            c.drawRRect(rr(-60, -20, 120, 40, 12), P("#F59E0B"))
            c.drawRect(R(-10, 18, 30, 50), P("#111827"))
            c.drawRect(R(60, -6, 50, 12), P("#9CA3AF"))
            c.restore()

    def ui_shelf(self, c, t, tw):
        T = self.T
        self.chip(330, 300 + 0, "still", T["cent"] - 0.1, self.duration + 1, accent=GOOD, size=30)
        k = self.span(T["fall"] + 0.2, self.duration + 1, 0.25, 0.1)
        if k > 0:
            v2.chip(c, 700, 1150, self.L["week"], k, accent=WARN, size=36)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8)]
        for k in range(8):
            ev.append((0.15 + k * max(0.15, (T["built"] - 0.2) / 8.0), sfx.thunk(61 + k), -16))
        ev += [(T["shine"], sfx.sparkle(1.0, 12, 70), -8), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 71), -9),
               (T["pyramid"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 72), -4), (T["car"], sfx.beep(900.0), -16), (T["sledge"], sfx.creak(1.0), -10),
               (T["digs"], sfx.thud(0.5), -8), (T["digs"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["poured"], sfx.hiss(0.9, 73), -10), (T["slide"], sfx.creak(1.2), -12), (T["half"], sfx.pop(74), -8),
               (T["pull"] + 0.1, sfx.ding(), -8), (T["pull"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 75), -4), (T["granite"], sfx.thud(0.4), -10),
               (T["nine"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["sail"], sfx.whoosh(0.8, False, 76), -12), (T["harbor"], sfx.ding(), -8), (T["harbor"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 77), -4), (T["mount3"], rumble(1.4, 78), -12),
               (T["crack"], sfx.snap(79), -6), (T["crack"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["rooms"] + i * 0.22, sfx.thunk(80 + i), -12) for i in range(5)]
        ev += [(T["gable"], sfx.clank(), -10), (T["aside"] + 0.1, sfx.ding(), -8), (T["aside"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 86), -4), (T["top"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["fixb"], sfx.creak(0.6), -12), (T["fixb"] + 0.8, sfx.click(87), -8), (T["north"], sfx.tick(), -10),
               (T["degree"] + 0.1, sfx.ding(), -8), (T["degree"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(88), 0), (T["follow"] - 0.15, sfx.pop(89), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 90), -6), (T["thousands"], rumble(1.2, 91), -16),
               (T["cas2"], sfx.sparkle(1.2, 14, 92), -8)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 93), -6), (T["s1"], sfx.pop(94), -3), (T["s2"], sfx.pop(95), -3),
               (T["s3"], sfx.pop(96), -3)]
        ev += [(T["cong2"], sfx.pop(97), -2), (T["cong2"], sfx.sparkle(1.0, 14, 98), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 99), -6), (T["cent"], sfx.chime(), -10), (T["fall"] + 0.1, sfx.creak(0.5), -10),
               (T["fall"] + 0.4, sfx.thud(0.5), -6), (T["fall"] + 0.6, sfx.clank(300.0, 0.5, 100), -10)]
        return ev


NAME = "pyramid"
EPISODE = Pyramid
