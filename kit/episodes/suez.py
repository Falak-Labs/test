"""Episode 55 - The Suez Canal.  v2 look: a giant ship sliding through the desert, maps, sections and top views.

Sets: desert (hook: a container ship longer than the Eiffel Tower glides over the sand, the tower lies on it for
scale, the near dune drops away and shows the canal; closer at dusk with the ship lit), map (break1: Europe, Africa and
India, a ship takes the long way round Africa; reveal: the short way through the canal, almost 9,000 km shorter), cut
(fix1: the isthmus from above, the cut drawn from the Mediterranean to the Red Sea; reveal: the two seas run in and
meet in the Bitter Lakes), camp (break2: a camp in the desert with an empty jar; fix2: fresh water arrives from the
Nile, palms, and the camp grows into a city), dig (break3: workers carry sand out of the trench in baskets; fix3: a
steam dredger with a bucket chain pours the sand down a long slide onto the bank), lakes (break4: one lane, two ships
nose to nose; fix4: convoys, one waits in the Bitter Lake while the other passes; the lake bed was dry salt), level
(stat: both seas at the same level, no locks), tag (EN: the stuck ship and one tiny digger, then you and your laundry
pile; AR: the guy who parks behind your car and switches his phone off).
World (desert): side view, the ground at y = 0, the canal's water at y = 30.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow, sun, heat_lines  # noqa: E402
from burjalarab import path_of, saudi_man  # noqa: E402
from panama import cargo_ship, ship_top, word  # noqa: E402
from camel import camel  # noqa: E402
from eiffel import eiffel  # noqa: E402
from falaj import mudhouse, jar, timer  # noqa: E402
from pyramid import palm  # noqa: E402
from phone import bubble  # noqa: E402
from barrier import suv  # noqa: E402
from airplane import water_snd  # noqa: E402

DESERT = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3F6CA6", "low": "#D89A66", "horizon": "#F2C089",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DUSKP = {"top": "#070B24", "upper": "#191A4E", "mid": "#47306E", "low": "#B5576A", "horizon": "#F09A6A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SAND = ("#B48A55", "#9A7444", "#7A5A34")
SEA_C, SEA_D = "#1D5F99", "#0E3460"
YW = 30.0                                            # the canal's water line (desert set)
EVER = "#2F7D4F"                                     # the green hull of the stuck ship


def geo(lon, lat):
    """Map world position of a longitude / latitude (degrees)."""
    return (lon - 30.0) * 10.4, (30.0 - lat) * 10.8


def geo_path(pts, close=True):
    return path_of([geo(lo, la) for lo, la in pts], close=close)


AFRICA = [(-17.1, 21.0), (-16.5, 14.7), (-15.0, 11.0), (-12.5, 7.8), (-7.5, 4.4), (-2.0, 4.8), (2.0, 6.2), (6.0, 4.3),
          (9.5, 3.9), (9.8, 0.5), (12.0, -5.5), (13.3, -11.5), (11.8, -17.0), (14.5, -22.9), (16.5, -28.6),
          (18.4, -34.2), (20.0, -34.8), (25.6, -34.0), (30.5, -30.8), (32.6, -26.0), (35.4, -23.9), (35.2, -21.0),
          (40.5, -15.2), (40.4, -10.5), (39.3, -6.5), (40.9, -2.0), (43.8, 2.0), (47.5, 5.5), (51.2, 11.8),
          (45.0, 10.5), (43.3, 11.8), (42.5, 13.5), (39.5, 15.7), (37.3, 18.9), (35.6, 23.2), (34.0, 26.6),
          (32.6, 29.9), (32.3, 31.3), (30.0, 31.3), (25.0, 31.6), (20.0, 30.6), (19.9, 32.2), (15.5, 32.2),
          (11.1, 33.3), (10.4, 36.9), (3.0, 36.8), (-2.0, 35.1), (-5.9, 35.8), (-9.4, 32.3), (-13.2, 27.7)]
MADAGASCAR = [(44.3, -16.2), (47.0, -12.9), (50.4, -15.5), (49.5, -17.5), (47.2, -25.0), (45.2, -25.5), (43.6, -21.8)]
EURASIA = [(-8.9, 37.0), (-6.3, 36.5), (-5.6, 36.0), (-2.2, 36.7), (0.2, 38.7), (-0.3, 39.5), (3.2, 41.9),
           (6.0, 43.1), (9.0, 44.4), (10.5, 43.0), (12.0, 41.8), (15.6, 38.0), (16.6, 38.5), (17.2, 40.4),
           (18.5, 40.1), (16.0, 41.5), (13.7, 43.6), (12.3, 45.3), (13.6, 45.7), (15.3, 44.2), (19.4, 41.8),
           (19.4, 40.3), (21.0, 38.3), (22.5, 36.5), (23.2, 37.9), (24.0, 40.2), (26.1, 40.6), (26.8, 39.0),
           (27.3, 37.0), (28.3, 36.7), (30.6, 36.8), (32.5, 36.1), (34.6, 36.8), (36.2, 36.6), (35.8, 35.0),
           (35.0, 32.8), (34.2, 31.3), (32.4, 31.2), (32.45, 30.6), (32.6, 30.0), (33.0, 29.5), (33.6, 28.5),
           (34.3, 27.8), (34.5, 28.5), (34.9, 29.5), (35.2, 28.0), (36.6, 25.8), (38.9, 22.0), (40.8, 19.5),
           (42.7, 16.3), (43.4, 12.7), (45.0, 12.8), (48.5, 14.0), (52.2, 15.6), (55.4, 17.6), (57.8, 19.0),
           (59.8, 22.5), (58.5, 23.6), (56.4, 26.3), (56.1, 24.8), (54.0, 24.2), (51.6, 24.6), (51.5, 26.0),
           (50.0, 26.6), (48.3, 28.8), (48.0, 30.0), (50.2, 30.1), (51.5, 27.9), (54.5, 26.6), (56.5, 27.1),
           (58.0, 25.6), (61.6, 25.2), (66.5, 25.3), (67.3, 24.0), (68.8, 23.0), (70.2, 22.8), (69.0, 22.3),
           (70.9, 20.7), (72.6, 21.3), (72.8, 19.0), (73.3, 16.5), (74.8, 12.8), (76.3, 9.5), (77.5, 8.1),
           (78.2, 9.0), (79.3, 10.3), (79.8, 11.8), (80.2, 13.2), (80.2, 15.5), (82.3, 17.0), (86.0, 20.0),
           (88.0, 21.8), (92.0, 22.0), (95.0, 20.0), (100.0, 15.0), (110.0, 30.0), (110.0, 70.0), (-12.0, 70.0),
           (5.0, 62.0), (5.5, 59.0), (8.0, 58.0), (10.6, 57.7), (10.0, 56.0), (8.6, 55.5), (8.6, 53.8), (6.0, 53.4),
           (4.2, 51.9), (3.0, 51.3), (1.6, 50.9), (0.2, 49.6), (-1.3, 48.8), (-4.7, 48.4), (-4.4, 47.8),
           (-2.2, 47.2), (-1.2, 46.0), (-1.4, 44.5), (-1.8, 43.4), (-4.5, 43.4), (-8.0, 43.7), (-9.2, 43.0),
           (-8.8, 41.9), (-9.5, 38.8)]
UK = [(-5.7, 50.0), (-3.0, 50.6), (1.4, 51.2), (1.7, 52.7), (0.2, 53.5), (-1.6, 55.6), (-2.1, 57.6), (-3.1, 58.6),
      (-5.0, 58.6), (-6.2, 56.9), (-4.9, 55.0), (-3.0, 54.0), (-3.2, 53.2), (-4.7, 52.8), (-4.0, 52.0), (-5.2, 51.7),
      (-3.4, 51.4)]
IRELAND = [(-6.0, 55.2), (-10.3, 54.2), (-10.5, 51.6), (-6.4, 52.2)]
SRILANKA = [(79.8, 9.8), (81.9, 7.5), (81.0, 6.0), (79.9, 6.5)]
BLACKSEA = [(28.0, 41.6), (29.0, 41.2), (31.0, 41.1), (34.0, 42.0), (38.0, 41.0), (41.5, 41.5), (41.8, 42.6),
            (39.5, 44.0), (37.5, 44.7), (36.5, 45.3), (33.5, 44.5), (32.5, 45.4), (30.5, 46.5), (29.5, 45.3), (28.6, 44.0)]
CASPIAN = [(47.0, 44.5), (49.0, 46.5), (53.0, 47.0), (53.0, 45.0), (51.5, 43.0), (53.0, 40.0), (53.9, 37.3),
           (50.5, 37.0), (49.0, 38.5), (49.5, 40.5), (47.5, 42.5)]
LONG = [(0.5, 50.6), (-5.0, 49.0), (-10.0, 44.0), (-11.5, 37.0), (-17.0, 28.5), (-19.5, 20.0), (-19.0, 12.0),
        (-12.0, 2.5), (2.0, 2.0), (8.0, -3.0), (10.0, -12.0), (11.0, -20.0), (14.0, -30.0), (18.5, -37.0),
        (24.0, -37.0), (32.0, -32.0), (38.0, -26.0), (42.5, -19.0), (43.0, -11.0), (45.0, -4.0), (52.0, 3.0),
        (58.0, 9.0), (65.0, 14.5), (72.0, 18.4)]
SHORT = [(0.5, 50.6), (-5.0, 49.0), (-10.0, 44.0), (-10.5, 37.5), (-6.5, 36.0), (-2.0, 36.2), (5.0, 37.8),
         (11.5, 37.6), (14.0, 35.5), (20.0, 34.5), (27.0, 33.0), (32.3, 31.6), (32.4, 30.6), (32.6, 29.7),
         (33.3, 28.0), (35.5, 25.0), (38.0, 21.0), (40.5, 17.0), (42.8, 13.8), (43.5, 12.4), (47.0, 12.6),
         (52.0, 13.5), (60.0, 15.8), (66.0, 17.5), (72.0, 18.4)]
MAPCAM = (0.0, 446.0, 0.95)
# the isthmus from above (cut set, screen space): the canal from Port Said (top) to Suez (bottom)
CAN = [(560, 420), (564, 500), (571, 590), (566, 660), (566, 705), (580, 780), (600, 840), (612, 885), (632, 930),
       (650, 968), (664, 1012), (672, 1064)]


def poly_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def along(pts, u):
    """Point and direction (degrees) at fraction u of a polyline, plus the part drawn so far."""
    want = poly_len(pts) * clamp(u)
    out = [pts[0]]
    for a_, b_ in zip(pts, pts[1:]):
        d = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
        ang = math.degrees(math.atan2(b_[1] - a_[1], b_[0] - a_[0]))
        if want <= d:
            p = (a_[0] + (b_[0] - a_[0]) * want / max(d, 1e-6), a_[1] + (b_[1] - a_[1]) * want / max(d, 1e-6))
            out.append(p)
            return p, ang, out
        out.append(b_)
        want -= d
    return pts[-1], ang, out


def stroke(c, pts, paint):
    if len(pts) > 1:
        c.drawPath(path_of(pts), paint)


def dunes(c, x0, x1, y, h, cols, seed=1, a=1.0, step=160):
    """A row of soft dunes (world space) standing on y, height h."""
    rng = random.Random(seed)
    p = skia.Path()
    p.moveTo(x0, y + 600)
    p.lineTo(x0, y)
    x = x0
    while x < x1:
        w_ = step * rng.uniform(0.7, 1.4)
        hh = h * rng.uniform(0.4, 1.0)
        p.quadTo(x + w_ * 0.55, y - hh * 2, x + w_, y)
        x += w_
    p.lineTo(x1, y + 600)
    p.close()
    c.drawPath(p, lin_paint(0, y - h, 0, y + 200, cols, a=a))


def head_basket(c, x, y, s, a=1.0):
    """A basket of sand carried on the head (its bottom at (x, y))."""
    bp = path_of([(x - 30 * s, y - 34 * s), (x + 30 * s, y - 34 * s), (x + 22 * s, y), (x - 22 * s, y)], close=True)
    c.drawPath(bp, P("#A16207", a))
    for k in range(5):
        c.drawCircle(x - 20 * s + k * 10 * s, y - 36 * s - (k % 2) * 5 * s, 9 * s, P(SAND[0], a))


def tent(c, x, y, s, col="#E7D7B5", a=1.0):
    tp = path_of([(x - 70 * s, y), (x, y - 90 * s), (x + 70 * s, y)], close=True)
    c.drawPath(tp, lin_paint(x - 70 * s, 0, x + 70 * s, 0, [shade(col, -0.25), col, shade(col, -0.1)], a=a))
    c.drawPath(path_of([(x - 14 * s, y), (x, y - 50 * s), (x + 14 * s, y)], close=True), P("#3A2A1A", a))
    c.drawLine(x, y - 90 * s, x, y - 110 * s, P("#5A4030", a, stroke=4 * s))


def dredger(c, x, y, s, t, run=1.0, a=1.0):
    """A steam bucket-chain dredger (side view): hull floating at y, the ladder down to the bottom on the right,
    the long slide to the left bank. Returns the slide's lower end (world)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    hull = path_of([(-150, -20), (150, -20), (130, 30), (-130, 30)], close=True)
    c.drawPath(hull, lin_paint(0, -20, 0, 30, ["#3B3F4A", "#262A33"], a=a))
    c.drawRect(R(-120, -90, 120, 70), lin_paint(-120, 0, 0, 0, ["#7A5A44", "#5A4030"], a=a))       # boiler house
    c.drawRect(R(-80, -190, 26, 100), P("#2B2B30", a))                                               # the stack
    c.drawRect(R(-84, -198, 34, 12), P("#8A3A2A", a))
    c.drawRect(R(-110, -70, 24, 22), P("#FDBA74", 0.7 * a))
    # the bucket ladder: from the deck (60, -60) down to the bottom (260, 230)
    lx0, ly0, lx1, ly1 = 40, -110, 250, 230
    c.drawLine(lx0, ly0, lx1, ly1, P("#4B5563", a, stroke=16))
    c.drawLine(lx0 + 14, ly0, lx1 + 14, ly1, P("#374151", a, stroke=6))
    L = math.hypot(lx1 - lx0, ly1 - ly0)
    ux, uy = (lx1 - lx0) / L, (ly1 - ly0) / L
    for k in range(9):                                                          # buckets running up the ladder
        q = ((k / 9.0) - t * 0.35 * run) % 1.0
        bx, by = lx1 - ux * L * q, ly1 - uy * L * q
        c.save()
        c.translate(bx - uy * 14, by + ux * 14)
        c.rotate(math.degrees(math.atan2(uy, ux)))
        c.drawRRect(rr(-14, -12, 28, 24, 5), P("#6B7280", a))
        c.drawRect(R(-12, -14, 24, 8), P(SAND[0], a * (0.9 if q > 0.05 else 0.0)))
        c.restore()
    c.drawLine(-20, -110, lx0, ly0, P("#4B5563", a, stroke=10))                # the gantry
    c.drawLine(-20, -110, -20, -20, P("#4B5563", a, stroke=10))
    c.restore()
    return x + (-20) * s, y + (-110) * s


def slide_sand(c, x0, y0, x1, y1, t, a=1.0, w=26):
    """The long chute from the dredger to the bank with sand running down it."""
    c.drawLine(x0, y0, x1, y1, P("#5A4632", a, stroke=w))
    c.drawLine(x0, y0 - w * 0.45, x1, y1 - w * 0.45, P("#8A6A4A", a, stroke=5))
    for k in range(14):
        q = (t * 0.9 + k / 14.0) % 1.0
        c.drawCircle(lerp(x0, x1, q), lerp(y0, y1, q) - 8, 8, P(SAND[0], a))
    for k in range(6):                                                          # spilling at the end
        q = (t * 1.3 + k / 6.0) % 1.0
        c.drawCircle(x1 - 10 - q * 40, y1 + q * q * 90, 9 * (1 - q * 0.5), P(SAND[0], a * (1 - q)))


def excavator(c, x, y, s, t, dig=1.0, a=1.0, face=-1):
    """A small yellow excavator (top-ish side view), digging with its arm."""
    c.save()
    c.translate(x, y)
    c.scale(s * face, s)
    c.drawRRect(rr(-50, -20, 100, 22, 8), P("#1F2937", a))                       # tracks
    c.drawRRect(rr(-38, -62, 70, 44, 8), P("#FACC15", a))                        # cab body
    c.drawRRect(rr(-30, -56, 28, 24, 4), P("#93C5FD", 0.8 * a))
    ang = -20 - 25 * dig * (0.5 + 0.5 * math.sin(t * 3.2))
    c.translate(28, -50)
    c.rotate(ang)
    c.drawRect(R(0, -7, 80, 14), P("#EAB308", a))
    c.translate(80, 0)
    c.rotate(70 + 20 * dig * math.sin(t * 3.2 + 1))
    c.drawRect(R(0, -6, 60, 12), P("#EAB308", a))
    c.drawPath(path_of([(56, -12), (80, 6), (52, 16)], close=True), P("#4B5563", a))
    c.restore()


def laundry(c, x, y, s, a=1.0, seed=4):
    """A huge heap of clothes."""
    rng = random.Random(seed)
    cols = ["#EF4444", "#3B82F6", "#F59E0B", "#10B981", "#A855F7", "#F8FAFC", "#EC4899", "#64748B", "#22D3EE"]
    for k in range(70):
        u = rng.random()
        px = x + (rng.random() - 0.5) * 520 * s * (1 - 0.6 * u)
        py = y - u * 460 * s
        w_, h_ = rng.uniform(60, 130) * s, rng.uniform(30, 60) * s
        c.save()
        c.translate(px, py)
        c.rotate(rng.uniform(-40, 40))
        col = cols[rng.randrange(len(cols))]
        c.drawRRect(rr(-w_ / 2, -h_ / 2, w_, h_, 14 * s), lin_paint(0, -h_ / 2, 0, h_ / 2, [col, shade(col, -0.3)], a=a))
        if rng.random() < 0.3:                                                   # a sock or a sleeve
            c.drawRRect(rr(w_ / 2 - 10 * s, -10 * s, 40 * s, 20 * s, 10 * s), P(col, a))
        c.restore()


def car_top(c, x, y, s, col, ang=0.0, a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawRRect(rr(-48 * s, -95 * s, 96 * s, 190 * s, 26 * s), P(col, a))
    c.drawRRect(rr(-38 * s, -50 * s, 76 * s, 42 * s, 10 * s), P("#1E293B", 0.85 * a))
    c.drawRRect(rr(-38 * s, 30 * s, 76 * s, 32 * s, 10 * s), P("#1E293B", 0.85 * a))
    c.restore()


# ====================================================================================== the episode
class Suez(EpisodeV2):
    BUILD_NO = 55
    FIRST_SET = "desert"
    CLEAR = "#0B1A3A"
    TITLE = {"en": "SUEZ CANAL", "ar_sa": "قناة السويس"}
    EMPH = {"en": ["CONGRATS", "SHIP", "LONGER", "EIFFEL", "TOWER", "DESERT", "SUEZ", "CANAL", "YOURSELF", "EUROPE",
                   "ASIA", "AROUND", "AFRICA", "SHORTCUT", "MEDITERRANEAN", "RED", "SEA", "NO", "DRINKING", "WATER",
                   "THOUSANDS", "FRESH", "NILE", "CITY", "HAND", "BASKET", "FOREVER", "STEAM", "DREDGERS", "SLIDES",
                   "ONE", "LANE", "BOTH", "CONVOYS", "BITTER", "LAKES", "SALT", "FLOODED", "FOLLOW", "ESCALATOR",
                   "EIGHTEEN", "SIXTY-NINE", "LONDON", "INDIA", "NINE", "THOUSAND", "KILOMETERS", "SHORTER", "HUNDRED",
                   "NINETY-THREE", "TEN", "YEARS", "ZERO", "LOCKS", "LEVEL", "STUCK", "SIDEWAYS", "SIX", "DAYS",
                   "TINY", "DIGGER", "LAUNDRY"],
            "ar_sa": ["مبروك", "سفينة", "أطول", "إيفل", "الصحرا", "قناة", "السويس", "بيدك", "أوروبا", "آسيا", "أفريقيا",
                      "مختصر", "المتوسط", "الأحمر", "موية", "العمال", "حلوة", "النيل", "مدينة", "زنبيل", "عمر",
                      "كراكات", "بخار", "زحاليق", "واحد", "الجهتين", "قوافل", "المرة", "ملح", "غرقته", "تابعني",
                      "كهربائي", "البحرين", "لندن", "للهند", "أقصر", "كيلو", "عشر", "هويس", "المستوى", "بالعرض", "ستة",
                      "يصف", "جواله"]}
    KEYS = {"ar_sa": {
        ("hook", "SHIP"): "سفينة", ("hook", "LONGER"): "أطول", ("hook", "EIFFEL"): "إيفل", ("hook", "DESERT"): "الصحرا",
        ("hook", "CONGRATS"): "مبروك", ("hook", "SUEZ"): "السويس",
        ("break1", "EUROPE"): "أوروبا", ("break1", "ASIA"): "آسيا", ("break1", "AROUND"): "تلف", ("break1", "AFRICA"): "أفريقيا",
        ("fix1", "CUT"): "تشق", ("fix1", "SHORTCUT"): "مختصر", ("fix1", "MEDITERRANEAN"): "المتوسط", ("fix1", "RED"): "الأحمر",
        ("break2", "NO"): "ولا", ("break2", "WATER"): "موية", ("break2", "THOUSANDS"): "آلاف",
        ("fix2", "FRESH"): "حلوة", ("fix2", "NILE"): "النيل", ("fix2", "CAMP"): "المخيم", ("fix2", "CITY"): "مدينة",
        ("break3", "SAND"): "الرمل", ("break3", "HAND"): "بيدك", ("break3", "BASKET"): "زنبيل", ("break3", "FOREVER"): "عمر",
        ("fix3", "STEAM"): "بخار", ("fix3", "DREDGERS"): "كراكات", ("fix3", "BOTTOM"): "القاع", ("fix3", "POUR"): "تزحلق",
        ("fix3", "BANKS"): "الضفة", ("fix3", "SLIDES"): "زحاليق",
        ("break4", "ONE"): "واحد", ("break4", "LANE"): "مسار", ("break4", "BOTH"): "الجهتين",
        ("fix4", "CONVOYS"): "قوافل", ("fix4", "PASS"): "تتلاقى", ("fix4", "BITTER"): "البحيرات", ("fix4", "SALT"): "ملح",
        ("fix4", "FLOODED"): "غرقته",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "EIGHTEEN"): "ألف", ("reveal", "MET"): "تقابل", ("reveal", "TRIP"): "طريق", ("reveal", "LONDON"): "لندن",
        ("reveal", "INDIA"): "هند", ("reveal", "NINE"): "بتسعة", ("reveal", "SHORTER"): "أقصر",
        ("stat", "HUNDRED"): "مية", ("stat", "TEN"): "عشر", ("stat", "ZERO"): "هويس", ("stat", "LEVEL"): "المستوى",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "TWENTY"): "ألفين", ("tag", "STUCK"): "وقفت", ("tag", "SIDEWAYS"): "بالعرض", ("tag", "SIX"): "ستة",
        ("tag", "CHEERED"): "سكرت", ("tag", "DIGGER"): "يصف", ("tag", "LAUNDRY"): "جواله"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an escalator"),
                   "stat": [("193 km", "LONG"), ("10 yrs", "OF DIGGING"), ("0", "LOCKS")],
                   "L": {"longer": "LONGER THAN THE EIFFEL TOWER", "desert": "THROUGH THE DESERT",
                         "name": "THE SUEZ CANAL", "europe": "EUROPE", "africa": "AFRICA", "asia": "ASIA",
                         "india": "INDIA", "london": "LONDON", "around": "ALL THE WAY AROUND AFRICA",
                         "cut": "A SHORTCUT", "med": "MEDITERRANEAN", "red": "RED SEA", "nile": "NILE",
                         "nowater": "NO DRINKING WATER", "fresh": "FRESH WATER FROM THE NILE",
                         "city": "A WHOLE NEW CITY: ISMAILIA", "hand": "BASKET AFTER BASKET", "forever": "TAKES FOREVER",
                         "dredger": "STEAM DREDGER", "slide": "SAND DOWN A LONG SLIDE", "lane": "ONE LANE",
                         "both": "SHIPS FROM BOTH ENDS", "convoy": "CONVOYS", "lakes": "THE BITTER LAKES",
                         "salt": "ONCE A DRY SALT VALLEY", "met": "1869: THE TWO SEAS MEET",
                         "shorter": "ALMOST 9,000 km SHORTER", "level": "BOTH SEAS ALMOST LEVEL",
                         "nolocks": "NO LOCKS", "stuck": "STUCK SIDEWAYS FOR 6 DAYS", "digger": "ONE TINY DIGGER",
                         "you": "YOU", "laundry": "YOUR LAUNDRY"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: درج كهربائي"),
                      "stat": [("193", "كيلو طول"), ("10", "سنين حفر"), ("0", "هويس")],
                      "L": {"longer": "أطول من برج إيفل", "desert": "وسط الصحرا", "name": "قناة السويس",
                            "europe": "أوروبا", "africa": "أفريقيا", "asia": "آسيا", "india": "الهند",
                            "london": "لندن", "around": "تلف حول أفريقيا كلها", "cut": "طريق مختصر",
                            "med": "البحر المتوسط", "red": "البحر الأحمر", "nile": "النيل",
                            "nowater": "ولا نقطة موية", "fresh": "موية حلوة من النيل", "city": "مدينة كاملة: الإسماعيلية",
                            "hand": "زنبيل ورا زنبيل", "forever": "بتاخذ عمر", "dredger": "كراكة بخار",
                            "slide": "زحاليق الرمل", "lane": "مسار واحد بس", "both": "سفن من الجهتين",
                            "convoy": "قوافل", "lakes": "البحيرات المرة", "salt": "كانت وادي ملح ناشف",
                            "met": "تقابل البحرين", "shorter": "أقصر بتسعة آلاف كيلو", "level": "البحرين بنفس المستوى",
                            "nolocks": "ولا هويس", "stuck": "وقفت بالعرض ستة أيام", "parked": "صافّ وراك!",
                            "phone": "جواله مقفل!"}}}
    COVER_T = ("closer", 0.55)
    SKY_ALT = {}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "ship": ("hook", "SHIP", 0.05), "longer": ("hook", "LONGER", 0.15), "eiffel": ("hook", "EIFFEL", 0.3),
            "desert": ("hook", "DESERT", 0.5), "congrats": ("hook", "CONGRATS", 0.65), "suez": ("hook", "SUEZ", 0.9),
            "europe": ("break1", "EUROPE", 0.2), "asia": ("break1", "ASIA", 0.35), "around": ("break1", "AROUND", 0.7),
            "africa": ("break1", "AFRICA", 0.9),
            "cut": ("fix1", "CUT", 0.1), "shortcut": ("fix1", "SHORTCUT", 0.2), "med": ("fix1", "MEDITERRANEAN", 0.6),
            "red": ("fix1", "RED", 0.9),
            "no": ("break2", "NO", 0.3), "water": ("break2", "WATER", 0.5), "thousands": ("break2", "THOUSANDS", 0.75),
            "fresh": ("fix2", "FRESH", 0.25), "nile": ("fix2", "NILE", 0.45), "camp": ("fix2", "CAMP", 0.65),
            "city": ("fix2", "CITY", 0.92),
            "sand": ("break3", "SAND", 0.15), "hand": ("break3", "HAND", 0.35), "basket": ("break3", "BASKET", 0.5),
            "forever": ("break3", "FOREVER", 0.9),
            "steam": ("fix3", "STEAM", 0.05), "dredgers": ("fix3", "DREDGERS", 0.12), "bottom": ("fix3", "BOTTOM", 0.35),
            "pour": ("fix3", "POUR", 0.5), "banks": ("fix3", "BANKS", 0.7), "slides": ("fix3", "SLIDES", 0.92),
            "one": ("break4", "ONE", 0.25), "lane": ("break4", "LANE", 0.4), "both": ("break4", "BOTH", 0.85),
            "convoys": ("fix4", "CONVOYS", 0.15), "pass": ("fix4", "PASS", 0.3), "bitter": ("fix4", "BITTER", 0.5),
            "salt": ("fix4", "SALT", 0.75), "flooded": ("fix4", "FLOODED", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "e1869": ("reveal", "EIGHTEEN", 0.05), "met": ("reveal", "MET", 0.3), "trip": ("reveal", "TRIP", 0.45),
            "london": ("reveal", "LONDON", 0.55), "india": ("reveal", "INDIA", 0.65), "nine": ("reveal", "NINE", 0.8),
            "shorter": ("reveal", "SHORTER", 0.95),
            "s1": ("stat", "HUNDRED", 0.05), "s2": ("stat", "TEN", 0.4), "s3": ("stat", "ZERO", 0.6),
            "level": ("stat", "LEVEL", 0.9),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_20": ("tag", "TWENTY", 0.05), "t_stuck": ("tag", "STUCK", 0.2), "t_side": ("tag", "SIDEWAYS", 0.28),
            "t_six": ("tag", "SIX", 0.35), "t_cheer": ("tag", "CHEERED", 0.5), "t_dig": ("tag", "DIGGER", 0.65),
            "t_laund": ("tag", "LAUNDRY", 0.9)})
        T["africa1"] = max(T["africa"], T["around"]) + 0.1
        T["thou1"] = max(T["thousands"], T["water"]) + 0.1
        T["forever1"] = max(T["forever"], T["basket"]) + 0.1
        T["both1"] = max(T["both"], T["lane"]) + 0.1
        T["red1"] = max(T["red"], T["med"]) + 0.2
        T["city1"] = max(T["city"], T["camp"]) + 0.2
        T["slides1"] = max(T["slides"], T["banks"]) + 0.2
        T["flood1"] = max(T["flooded"], T["salt"]) + 0.2
        T["trip1"] = max(T["trip"], T["met"] + 0.5)
        # ---- sets
        self.cut(s("break1") - 0.12, "map", 1)
        self.cut(s("fix1") - 0.12, "cut", -1)
        self.cut(s("break2") - 0.12, "camp", 1)
        self.cut(s("break3") - 0.12, "dig", -1)
        self.cut(s("break4") - 0.12, "lakes", 1)
        self.cut(s("reveal") - 0.12, "cut", -1)
        self.cut(T["trip1"] - 0.12, "map", 1)
        self.cut(s("stat") - 0.12, "level", -1)
        self.cut(s("closer") - 0.12, "desert", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- desert camera: the hook, then the closer
        cm = Camera(-40, -62, 1.05)
        cm.key(0.1, -20, -58, 1.08, max(1.0, T["congrats"] - 0.2))
        cm.key(T["congrats"] - 0.1, 0, -50, 1.1, 0.6)
        cm.key(s("closer") - 0.12, 0, -60, 1.1, 0.0).key(s("closer"), 0, -55, 1.16, max(1.0, e("closer") - s("closer")))
        self.cam = cm
        self.spans = [(T["africa1"], T["red1"] + 0.3), (T["thou1"], T["city1"] + 0.3), (T["forever1"], T["slides1"] + 0.3),
                      (T["both1"], T["flood1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["africa1"], 0.4, 7), (T["thou1"], 0.4, 7), (T["forever1"], 0.4, 7),
                       (T["both1"], 0.45, 8), (T["met"], 0.4, 8), (s("closer") + 0.2, 0.35, 9), (T["t_stuck"], 0.4, 8)]

    # ------------------------------------------------------------------ set: desert (hook, closer)
    def draw_desert(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        hook = t < s("break1")
        dusk = 0.0 if hook else 1.0
        v2.sky(c, W, H, 0.0, pal=DUSKP if dusk else DESERT, horizon_y=gy - 70 * z)
        if dusk:
            v2.stars(c, W, H, t, 0.5)
            sun(c, 250 - cx * 0.04, gy - 230 * z, 48, heat=0.7)
        else:
            sun(c, 860 - cx * 0.04, gy - 560 * z, 50, heat=1.0)
        for i, (px, py, s_) in enumerate(((240, 900, 0.9), (830, 1130, 0.7))):
            v2.cloud(c, (px + t * (5 + i * 3)) % (W + 600) - 300, gy - py * z, s_,
                     body=mix("#8A7A9A", "#2A2050", dusk), rim=mix("#FFD3A0", "#FF8A6A", dusk), a=0.6, seed=i)
        self.view(c, cam)
        dunes(c, -2400, 2400, -70, 60, [mix("#C6A06A", "#5A4058", dusk), mix("#A88050", "#3A2A40", dusk)], seed=3, step=260)
        dunes(c, -2400, 2400, -10, 40, [mix(SAND[0], "#6A4A48", dusk), mix(SAND[1], "#3A2A38", dusk)], seed=7, step=200)
        c.drawRect(R(-2400, -6, 4800, 12), P(mix("#C9A46E", "#7A5A50", dusk)))         # the far bank's edge
        for k in range(7):                                                               # palms on the far bank
            if not hook:
                palm(c, -900 + k * 300 + (k % 2) * 60, -4, 120 + (k % 3) * 20, sway=math.sin(t + k) * 0.2, a=0.9)
        reveal = 1.0 if not hook else e_io(prog(t, T["congrats"] - 0.25, T["congrats"] + 0.6))
        c.drawRect(R(-2400, YW, 4800, 160), lin_paint(0, YW, 0, YW + 160, [mix(SEA_C, "#3A4A8A", dusk), SEA_D], a=reveal))
        c.drawRect(R(-2400, YW, 4800, 4), P("#BFE6FF", 0.6 * reveal))
        if hook:
            sx = lerp(-420, 60, e_out(prog(t, 0.0, T["congrats"] + 0.8)))
        else:
            sx = lerp(-80, 80, prog(t, s("closer") - 0.2, self.duration))
        cargo_ship(c, sx, YW, 760, t, face=1, lit=dusk)
        kk = 760 / 260.0                                                                 # tone the white bridge down
        c.drawRect(R(sx - 124 * kk, YW - 101 * kk, 50 * kk, 76 * kk), P(mix("#475569", "#1E1B3A", dusk), 0.45))
        if reveal > 0:                                                                   # the hull under water
            c.drawRect(R(-2400, YW + 3, 4800, 157), P(SEA_C, 0.5 * reveal))
        if dusk:
            for k in range(6):
                add_glow(c, sx - 330 + k * 16, YW - 220 + (k % 3) * 17, 14, "#FDE68A", 0.5)
            add_glow(c, sx + 380, YW - 60, 26, "#F87171", 0.7)
        if reveal > 0:                                                                   # the bow wave
            for k in range(5):
                q = (t * 0.8 + k / 5.0) % 1.0
                c.drawLine(sx + 405 + q * 60, YW + 6, sx + 405 + q * 140, YW + 6 + q * 10, P("#E0F2FE", 0.6 * reveal * (1 - q), stroke=3))
        if hook:                                                                         # the tower lying on the ship
            ek = prog(t, T["longer"] - 0.15, T["longer"] + 0.25) * (1 - prog(t, T["desert"] + 0.2, T["congrats"]))
            if ek > 0:
                c.save()
                c.translate(sx - 228, YW - 300)
                c.rotate(90)
                eiffel(c, 0, 0, 0.7, t, a=ek, k3=0.0)
                c.restore()
        # the near bank: covers the canal in the hook, drops away on "congrats"
        top = lerp(-36, 190, reveal)
        nb = skia.Path()
        nb.moveTo(-2400, 900)
        nb.lineTo(-2400, top)
        xx = -2400
        while xx < 2400:
            nb.quadTo(xx + 120, top - 26 * (1 - 0.6 * reveal), xx + 240, top)
            xx += 240
        nb.lineTo(2400, 900)
        nb.close()
        c.drawPath(nb, lin_paint(0, top - 30, 0, top + 400, [mix(SAND[0], "#6A4A40", dusk), mix(SAND[2], "#2A1E28", dusk)]))
        tex(c, nb, "sand", 0.8, 0.25)
        if reveal > 0:                                                                   # the cut face of the near bank
            c.drawRect(R(-2400, top, 4800, 10), P(mix("#D9B27A", "#8A6A5A", dusk), reveal))
        cam_x = 470 if hook else 560
        c.save()                                                                         # the camel, facing the ship
        c.translate(cam_x, top - 4)
        c.scale(-1, 1)
        camel(c, 0, 0, 0.42, t * 2.2, run=0.25 if hook else 0.0)
        c.restore()
        if hook:
            heat_lines(c, -500, 500, -260, -40, t, a=0.35 * (1 - reveal))
        c.restore()
        self.ui["ship"] = self.to_screen(cam, sx, YW - 120)

    def ui_desert(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "longer", T["longer"] - 0.1, T["desert"] - 0.1, accent=HILITE, size=40)
            self.chip(540, 300, "desert", T["desert"] - 0.1, T["suez"] - 0.2, accent="#FDBA74", size=44)
            self.chip(540, 300, "name", T["suez"] - 0.2, s("break1") + 0.1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: map (break1, reveal part 2)
    def map_route(self, c, pts, u, t, col, a=1.0, ship=True, w=7):
        P_ = [geo(lo, la) for lo, la in pts]
        p, ang, drawn = along(P_, u)
        if u > 0:
            stroke(c, drawn, dash_paint(col, a, w, t, 18, 12))
        if ship and u > 0:
            c.save()
            c.translate(*p)
            c.rotate(ang + 90)
            c.drawPath(path_of([(0, -22), (11, 12), (-11, 12)], close=True), P("#F8FAFC", a))
            c.restore()
            add_glow(c, p[0], p[1], 30, col, 0.5 * a)
        return p

    def draw_map(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0B2447", "#0E3A66", "#0B2447"])
        self.view(c, MAPCAM)
        for la in range(-40, 70, 10):
            c.drawLine(-700, geo(0, la)[1], 700, geo(0, la)[1], P("#1E4F80", 0.35, stroke=2))
        land = lin_paint(0, -400, 0, 700, ["#5A8A55", "#B09060", "#C2A06A", "#5A8A50", "#3F7A45"], [0, 0.35, 0.55, 0.8, 1])
        for poly in (EURASIA, AFRICA, MADAGASCAR, UK, IRELAND, SRILANKA):
            pth = geo_path(poly)
            c.drawPath(pth, land)
            tex(c, pth, "sand", 0.6, 0.15)
            c.drawPath(pth, P("#E9D8A6", 0.35, stroke=2.5))
        for poly in (BLACKSEA, CASPIAN):
            c.drawPath(geo_path(poly), P("#0E3A66"))
        revealing = t >= s("reveal") - 0.12
        if not revealing:
            rk = prog(t, T["around"] - 0.6, T["africa1"] + 0.6)
            self.map_route(c, LONG, rk, t, WARN if t > T["africa1"] else "#FDE68A")
        else:
            self.map_route(c, LONG, 1.0, t, "#94A3B8", a=0.55, ship=False, w=5)
            sk = prog(t, T["trip1"] - 0.1, T["india"] + 0.5)
            self.map_route(c, SHORT, sk, t, GOOD, w=9)
            px, py = geo(32.4, 30.6)
            add_glow(c, px, py, 40, HILITE, 0.8 * prog(t, T["trip1"], T["trip1"] + 0.4))
        for lo, la in ((0.5, 50.8), (72.6, 19.0)):                                     # London and Mumbai
            x_, y_ = geo(lo, la)
            c.drawCircle(x_, y_, 9, P(HILITE))
        c.restore()
        self.ui["ldn"] = self.to_screen(MAPCAM, *geo(0.5, 50.8))
        self.ui["ind"] = self.to_screen(MAPCAM, *geo(72.6, 19.0))

    def ui_map(self, c, t, tw):
        T, s = self.T, self.tl.s
        lk = self.span(s("break1") - 0.12, self.duration)
        for key, lo, la, sz in (("europe", 22, 47.5, 40), ("africa", 20, 8, 46), ("asia", 66, 36, 44)):
            x_, y_ = self.to_screen(MAPCAM, *geo(lo, la))
            word(c, self.L[key], x_, y_, sz, "#F8FAFC", 0.85 * lk)
        lx, ly = self.ui["ldn"]
        ix, iy = self.ui["ind"]
        word(c, self.L["london"], lx - 20, ly - 26, 30, HILITE, lk, align="right")
        word(c, self.L["india"], ix - 30, iy - 40, 32, HILITE, lk)
        if tw < s("fix1") - 0.12:
            self.chip(540, 1170, "around", T["around"] - 0.2, s("fix1") - 0.15, accent=WARN, size=38)
            self.badge("alert", T["africa1"], s("fix1") - 0.2, x=920, y=420)
            self.red(T["africa1"], 1.3)
        else:
            self.chip(540, 1170, "shorter", T["nine"] - 0.2, s("stat") - 0.15, accent=GOOD, size=42)

    # ------------------------------------------------------------------ set: cut (fix1; reveal part 1), from above
    def isthmus(self, c, t, cut_u=1.0, water=0.0, meet=0.0):
        vrect(c, 0, 0, W, H, ["#B08A55", "#A47C48", "#8C683C"])
        tex(c, R(0, 0, W, H), "sand", 1.2, 0.3)
        med = skia.Path()                                                               # the Mediterranean, top
        med.moveTo(0, 0)
        med.lineTo(W, 0)
        med.lineTo(W, 330)
        for k in range(12, -1, -1):
            med.lineTo(k * W / 12.0, 405 + 18 * math.sin(k * 1.3) + (12 - k) * 2)
        med.close()
        c.drawPath(med, lin_paint(0, 0, 0, 420, ["#0E3460", SEA_C]))
        nile = skia.Path()                                                              # the Nile delta, left
        nile.moveTo(0, 420)
        nile.lineTo(330, 425)
        nile.quadTo(200, 600, 60, 760)
        nile.lineTo(0, 780)
        nile.close()
        c.drawPath(nile, lin_paint(0, 420, 0, 780, ["#3F7A45", "#2E5E36"]))
        c.drawPath(path_of([(150, 760), (170, 640), (240, 520), (300, 430)]), P("#2B7BBF", 0.9, stroke=8))
        gulf = skia.Path()                                                              # the Gulf of Suez, bottom
        gulf.moveTo(660, 1062)
        gulf.lineTo(686, 1062)
        gulf.lineTo(820, H)
        gulf.lineTo(610, H)
        gulf.close()
        c.drawPath(gulf, lin_paint(0, 1062, 0, H, [SEA_C, "#0E3460"]))
        for (lx, ly, rx, ry, rot) in ((566, 705, 46, 24, 0), (612, 885, 74, 46, 30), (650, 968, 30, 20, 30)):
            c.save()                                                                    # the lake beds (salt)
            c.translate(lx, ly)
            c.rotate(rot)
            c.drawOval(R(-rx, -ry, 2 * rx, 2 * ry), P("#E7E1D2", 0.75))
            if water > 0:
                c.drawOval(R(-rx * water, -ry * water, 2 * rx * water, 2 * ry * water), P(SEA_C, 0.95))
            c.restore()
        pt, ang, drawn = along(CAN, cut_u)
        stroke(c, drawn, P("#5A3E22", 1.0, stroke=20))                                    # the dug cut
        stroke(c, drawn, P("#D8B27A", 0.8, stroke=4))
        if 0 < cut_u < 1:
            add_glow(c, pt[0], pt[1], 60, HILITE, 0.8)
            c.drawCircle(pt[0], pt[1], 12, P(HILITE))
        if water > 0:                                                                   # the seas run in from both ends
            _, _, top_part = along(CAN, 0.5 * water)
            stroke(c, top_part, P(SEA_C, 1.0, stroke=14))
            rev = list(reversed(CAN))
            _, _, bot_part = along(rev, 0.5 * water)
            stroke(c, bot_part, P("#1B6FB0", 1.0, stroke=14))
        if meet > 0:
            add_glow(c, 612, 885, 160, "#BFE6FF", 0.7 * meet * (1 - meet))
        return pt

    def draw_cut(self, c, t):
        T, s = self.T, self.tl.s
        if t < s("cta"):
            u = e_io(prog(t, T["cut"] - 0.1, T["red1"]))
            self.isthmus(c, t, cut_u=u)
        else:
            wk = e_io(prog(t, s("reveal") - 0.1, T["met"] + 0.1))
            mk = prog(t, T["met"], T["met"] + 1.0)
            self.isthmus(c, t, cut_u=1.0, water=wk, meet=mk)
            if mk > 0:                                                                  # fireworks for 1869
                for k in range(3):
                    v2.puff(c, 612 + (k - 1) * 150, 640 - k * 40, 26 + 60 * mk, ["#FDE68A", "#F87171", "#93C5FD"][k],
                            0.6 * (1 - mk), k=k)

    def ui_cut(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("cta"):
            self.chip(540, 300, "cut", T["shortcut"] - 0.15, T["med"] - 0.15, accent=HILITE, size=46)
            self.chip(540, 300, "med", T["med"] - 0.15, T["red"] - 0.1, accent="#93C5FD", size=44)
            self.chip(540, 300, "red", T["red"] - 0.1, s("break2") - 0.15, accent="#93C5FD", size=44)
            word(c, self.L["nile"], 150, 600, 30, "#F8FAFC", self.span(T["cut"], s("break2")))
            self.badge("check", T["red1"] + 0.1, s("break2") - 0.15, x=920, y=420)
        else:
            self.chip(540, 300, "met", T["e1869"] - 0.1, T["trip1"], accent=HILITE, size=44)

    # ------------------------------------------------------------------ set: camp (break2, fix2), side view
    def draw_camp(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        cam = (0, -85, 1.9)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=DESERT, horizon_y=gy - 80)
        sun(c, 820, 420, 56, heat=1.0)
        self.view(c, cam)
        dunes(c, -600, 600, -24, 30, [SAND[0], SAND[1]], seed=11, step=150)
        c.drawRect(R(-600, 0, 1200, 2000), lin_paint(0, 0, 0, 300, [SAND[0], SAND[2]]))
        tex(c, R(-600, 0, 1200, 600), "sand", 0.6, 0.25)
        ck = prog(t, T["city"] - 0.5, T["city1"] + 0.3) if fixed else 0.0
        for k in range(7):                                                              # the city rising behind
            hh = (70 + (k * 37) % 60) * e_out(clamp(ck * 1.3 - k * 0.06))
            if hh > 2:
                mudhouse(c, -270 + k * 90, -14, 80, hh, lit=0.6, seed=k)
        for k, (tx, ts) in enumerate(((-230, 0.9), (-70, 1.1), (110, 0.95), (250, 0.85))):
            tent(c, tx, -8, ts, a=1 - 0.85 * ck)
        wk = prog(t, T["fresh"] - 0.3, T["nile"] + 0.6) if fixed else 0.0
        if wk > 0:
            x1 = lerp(-300, 300, wk)
            for k in range(5):                                                          # palms along the water
                px_ = -250 + k * 125
                if px_ < x1 - 20:
                    palm(c, px_, -6, 130 + (k % 2) * 24, sway=math.sin(t + k) * 0.3, a=clamp((x1 - px_) / 80))
        for k, px in enumerate((-150, 20, 175)):                                        # the workers
            shirt = ("#E7E5E4", "#D6D3D1", "#F5F5F4")[k]
            if not fixed:
                person(c, px, -2, 120, shirt, t + k, pose="shrug" if k == 1 else "stand", face=1 if px < 0 else -1,
                       hat="none", skin="#B07A4F", hair="#1C1917")
            else:
                person(c, px, -2, 120, shirt, t + k, pose="cheer" if t > T["nile"] + 0.3 else "stand", face=1,
                       hat="none", skin="#B07A4F", hair="#1C1917", a=1 - ck)
        jar(c, 262, -2, 1.0)
        if wk > 0:                                                                      # the fresh water canal, in front
            c.drawRect(R(-300, 8, x1 + 300, 26), lin_paint(0, 8, 0, 34, ["#3B9AE1", "#1D5F99"]))
            c.drawRect(R(-300, 8, x1 + 300, 3), P("#BFE6FF", 0.8))
            add_glow(c, x1, 20, 30, "#BFE6FF", 0.6 * (1 - wk))
        if not fixed:
            dk = prog(t, T["water"] - 0.2, T["water"] + 0.3)
            q = (t * 0.6) % 1.0
            c.drawCircle(262, -92 - 20 * q, 7, P("#7DD3FC", dk * (1 - q)))
            heat_lines(c, -280, 280, -200, -20, t, a=0.5)
        c.restore()

    def ui_camp(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "nowater", T["no"] - 0.2, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["thou1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["thou1"], 1.2)
            return
        self.chip(540, 300, "fresh", T["fresh"] - 0.2, T["city"] - 0.2, accent="#7DD3FC", size=40)
        self.chip(540, 300, "city", T["city"] - 0.2, s("break3") - 0.15, accent=GOOD, size=38)
        self.badge("check", T["city1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: dig (break3, fix3), the trench in section
    def draw_dig(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        cam = (0, 256, 1.15)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=DESERT, horizon_y=gy - 30)
        self.view(c, cam)
        dunes(c, -700, 700, -16, 30, [SAND[0], SAND[1]], seed=5, step=200)
        bank_h = 50 + (110 * prog(t, T["pour"] - 0.2, T["slides1"] + 1.0) if fixed else 20 * prog(t, T["basket"], T["forever1"]))
        trench = path_of([(-700, 0), (-300, 0), (-170, 380), (170, 380), (300, 0), (700, 0), (700, 2000), (-700, 2000)], close=True)
        c.drawPath(trench, lin_paint(0, 0, 0, 700, [SAND[1], SAND[2], "#5A4028"]))
        tex(c, trench, "sand", 0.9, 0.3)
        spoil = path_of([(-520, 0), (-450, -bank_h), (-360, -bank_h * 0.85), (-310, 0)], close=True)
        c.drawPath(spoil, lin_paint(0, -bank_h, 0, 0, [SAND[0], SAND[1]]))
        if not fixed:
            for k in range(5):                                                         # workers with baskets on the slope
                q = (t * 0.07 + k / 5.0) % 1.0
                px = lerp(-180, -305, q)
                py = lerp(375, -2, q)
                person(c, px, py, 120, "#F5F5F4", t * 0.6 + k, pose="carry", face=-1, hat="none", skin="#B07A4F",
                       hair="#1C1917")
                head_basket(c, px - 2, py - 122, 0.8)
            fk = prog(t, T["forever"] - 0.3, T["forever"] + 0.2)
            if fk > 0:
                timer(c, 70, 190, 80, (t * 0.4) % 1.0, a=fk)
        else:
            c.drawPath(path_of([(-232, 200), (232, 200), (170, 380), (-170, 380)], close=True),
                       lin_paint(0, 200, 0, 380, [SEA_C, SEA_D]))                     # water in the cut
            c.drawRect(R(-232, 200, 464, 4), P("#BFE6FF", 0.7))
            dk = e_out(prog(t, T["dredgers"] - 0.4, T["dredgers"] + 0.2))
            dx_ = lerp(150, 30, dk)
            ex, ey = dredger(c, dx_, 200, 0.75, t, run=prog(t, T["bottom"] - 0.3, T["bottom"]), a=dk)
            if t > T["pour"] - 0.3:
                v2.smoke(c, dx_ - 50, 200 - 148, t, T["steam"] - 0.2, rate=10, life=2.4,
                         spread=(50, -30), rise=-60, size=(16, 60), col="#9CA3AF")
                sk = prog(t, T["pour"] - 0.3, T["pour"] + 0.2)
                slide_sand(c, ex, ey, -400, -bank_h + 10, t, a=sk, w=20)
        c.restore()

    def ui_dig(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "hand", T["hand"] - 0.2, T["forever"] - 0.2, accent="#FDBA74", size=44)
            self.chip(540, 300, "forever", T["forever"] - 0.2, s("fix3") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["forever1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["forever1"], 1.2)
            return
        self.chip(540, 300, "dredger", T["dredgers"] - 0.2, T["pour"] - 0.2, accent="#CBD5E1", size=44)
        self.chip(540, 300, "slide", T["pour"] - 0.2, s("break4") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["slides1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: lakes (break4, fix4), from above
    def draw_lakes(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        vrect(c, 0, 0, W, H, ["#B08A55", "#9A7444"])
        tex(c, R(0, 0, W, H), "sand", 1.0, 0.3)
        c.drawRect(R(470, 0, 140, H), lin_paint(470, 0, 610, 0, [SEA_D, SEA_C, SEA_D]))     # the channel
        c.drawRect(R(462, 0, 8, H), P("#D9B27A"))
        c.drawRect(R(610, 0, 8, H), P("#D9B27A"))
        if not fixed:
            mk = e_out(prog(t, s("break4") - 0.1, T["both1"]))
            ship_top(c, 540, lerp(1300, 720, mk), 96, 380)                              # northbound, bow up
            c.save()
            c.translate(540, lerp(140, 680, mk))
            c.rotate(180)
            ship_top(c, 0, 0, 96, 380)                                                  # southbound, bow down
            c.restore()
            xk = prog(t, T["both1"], T["both1"] + 0.3)
            if xk > 0:
                c.drawLine(480, 640, 600, 760, P(WARN, xk, stroke=14))
                c.drawLine(600, 640, 480, 760, P(WARN, xk, stroke=14))
            return
        lake = skia.Path()
        lake.addOval(R(170, 420, 740, 560))
        c.drawPath(lake, lin_paint(0, 420, 0, 980, [SEA_C, "#16518A"]))
        c.drawPath(lake, P("#D9B27A", 1.0, stroke=8))
        saltk = prog(t, T["salt"] - 0.2, T["salt"] + 0.2) * (1 - prog(t, T["flooded"] - 0.1, T["flood1"] + 0.3))
        if saltk > 0:
            c.save()
            c.clipPath(lake, doAntiAlias=True)
            c.drawRect(R(0, 0, W, H), P("#ECE6D6", saltk))
            rng = random.Random(5)
            for _ in range(60):
                xx, yy = rng.uniform(180, 900), rng.uniform(430, 970)
                c.drawLine(xx, yy, xx + rng.uniform(-40, 40), yy + rng.uniform(-30, 30), P("#B8AE98", saltk, stroke=3))
            c.restore()
        ck = prog(t, T["convoys"] - 0.5, s("cta"))
        for k in range(3):                                                              # southbound: into the lake, anchor
            pts = [(540, -300 - k * 340), (540, 380), (280 + k * 100, 560), (280 + k * 100, 770)]
            self.ship_on(c, pts, clamp(ck * 1.8 - k * 0.12), 66, 250)
        for k in range(3):                                                              # northbound: straight through
            pts = [(540, 2100 + k * 340), (540, 1000), (700, 880), (700, 520), (540, 400), (540, -700)]
            self.ship_on(c, pts, clamp(ck * 1.05 - 0.05 - k * 0.05), 66, 250)

    def ship_on(self, c, pts, u, Wd, Ln, a=1.0):
        p, ang, _ = along(pts, u)
        c.save()
        c.translate(*p)
        c.rotate(ang + 90)
        ship_top(c, 0, 0, Wd, Ln, a=a)
        c.restore()

    def ui_lakes(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "lane", T["one"] - 0.2, T["both"] - 0.2, accent="#93C5FD", size=46)
            self.chip(540, 300, "both", T["both"] - 0.2, s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["both1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["both1"], 1.2)
            return
        self.chip(540, 300, "convoy", T["convoys"] - 0.2, T["bitter"] - 0.2, accent=HILITE, size=48)
        self.chip(540, 300, "lakes", T["bitter"] - 0.2, T["salt"] - 0.2, accent="#93C5FD", size=46)
        self.chip(540, 300, "salt", T["salt"] - 0.2, s("cta") - 0.15, accent="#E7E1D2", size=40)
        self.badge("check", T["flood1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: level (stat), side section
    def draw_level(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.0, pal=DESERT, horizon_y=700)
        wl = 760
        c.drawRect(R(0, wl, W, H - wl), lin_paint(0, wl, 0, 1300, ["#8C683C", "#5A4028"]))   # ground under it all
        land = path_of([(170, wl), (210, 690), (330, 670), (520, 682), (700, 664), (860, 688), (910, wl)], close=True)
        c.drawPath(land, lin_paint(0, 660, 0, wl, [SAND[0], SAND[1]]))
        c.drawRect(R(0, wl, 190, 300), lin_paint(0, wl, 0, 1060, [SEA_C, SEA_D]))         # Mediterranean
        c.drawRect(R(890, wl, 190, 300), lin_paint(0, wl, 0, 1060, ["#1B6FB0", SEA_D]))   # Red Sea
        c.drawRect(R(190, wl, 700, 70), lin_paint(0, wl, 0, wl + 70, [SEA_C, "#1B6FB0"]))   # the canal at sea level
        c.drawRect(R(0, wl - 2, W, 4), P("#BFE6FF", 0.8))
        c.save()
        c.translate(lerp(240, 840, prog(t, s("stat"), s("closer"))), wl)
        c.scale(0.22, 0.22)
        cargo_ship(c, 0, 0, 760, t)
        c.restore()
        lk = prog(t, T["level"] - 0.4, T["level"])
        c.drawLine(0, wl - 14, W, wl - 14, dash_paint(HILITE, lk, 5, t))
        zk = prog(t, T["s3"] - 0.2, T["s3"] + 0.3)
        if zk > 0:                                                                     # a ghost staircase of locks, crossed out
            for k in range(3):
                c.drawRect(R(420 + k * 70, wl - 60 - k * 50, 70, 60 + k * 50), P("#F8FAFC", 0.35 * zk, stroke=4))
            c.drawLine(400, 590, 660, 790, P(WARN, zk, stroke=12))
            c.drawLine(660, 590, 400, 790, P(WARN, zk, stroke=12))
        word(c, self.L["med"], 100, 900, 26, "#F8FAFC", 0.9)
        word(c, self.L["red"], 985, 900, 26, "#F8FAFC", 0.9)

    def ui_level(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 1120, "level", T["level"] - 0.3, s("closer") - 0.1, accent=HILITE, size=40)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#B08A55", "#9A7444"])
        tex(c, R(0, 0, W, H), "sand", 1.0, 0.3)
        second = self.span(T["t_dig"] - 0.1, self.duration + 1, 0.4, 0.2) if self.rtl else \
            self.span(T["t_laund"] - 0.6, self.duration + 1, 0.4, 0.2)
        if second < 1:
            c.save()
            c.saveLayerAlpha(None, int(255 * (1 - second)))
            c.drawRect(R(380, 0, 320, H), lin_paint(380, 0, 700, 0, [SEA_D, SEA_C, SEA_D]))
            c.save()                                                                   # the ship stuck across the canal
            c.translate(540, 800)
            c.rotate(-58 * e_out(prog(t, T["t_stuck"] - 0.4, T["t_side"] + 0.2)))
            c.drawRRect(rr(-60, -330, 120, 660, 50), lin_paint(-60, 0, 60, 0, ["#1F5A3A", EVER, "#1F5A3A"]))
            rng = random.Random(8)
            for r_ in range(11):
                for k_ in range(3):
                    c.drawRect(R(-48 + k_ * 32, -250 + r_ * 44, 30, 40), P(["#E5E7EB", "#3B82F6", "#F59E0B", "#EF4444"][rng.randrange(4)], 0.95))
            c.drawRect(R(-50, 250, 100, 60), P("#F1F5F9"))
            c.restore()
            dk = prog(t, T["t_cheer"] - 0.4, T["t_cheer"])
            if not self.rtl:
                excavator(c, 760, 560, 0.9, t, dig=1.0, a=max(dk, 0.0))
            for k in range(3):                                                         # waiting ships, top and bottom
                ship_top(c, 540, -120 - k * 300 + 0, 60, 220, a=0.8 * prog(t, T["t_six"] - 0.3, T["t_six"]))
            c.restore()
            c.restore()
        if second > 0:
            if not self.rtl:                                                           # you against your laundry pile
                laundry(c, 640, 1150, 1.25, a=second)
                person(c, 230, 1160, 150, "#2563EB", t, pose="carry", face=1, hat="none", a=second)
                c.drawRRect(rr(250, 1040, 90, 50, 10), P("#D6D3D1", second))
            else:                                                                      # the car parked behind yours
                c.drawRect(R(0, 1000, W, 200), P("#4B5563", second))
                c.drawRect(R(0, 1000, W, 10), P("#9CA3AF", second))
                suv(c, 330, 1150, 1.1, "#F8FAFC", a=second)
                pk = e_out(prog(t, T["t_dig"] - 0.1, T["t_dig"] + 0.5))
                suv(c, lerp(1400, 640, pk), 1150, 1.1, "#1F2937", a=second)
                saudi_man(c, 160, 1170, 200, t, pose="look", face=1, a=second)
                c.drawRRect(rr(182, 990, 26, 46, 6), P("#111827", second))

    def ui_tag(self, c, t, tw):
        T = self.T
        if not self.rtl:
            self.chip(540, 300, "stuck", T["t_stuck"] - 0.2, T["t_cheer"] - 0.1, accent=WARN, size=42)
            self.chip(540, 300, "digger", T["t_cheer"] - 0.1, T["t_laund"] - 0.6, accent=HILITE, size=44)
            sk = self.span(T["t_laund"] - 0.4, self.duration + 1)
            v2.chip(c, 250, 960, self.L["you"], sk, accent=HILITE, size=44)
            v2.chip(c, 660, 560, self.L["laundry"], sk, accent=WARN, size=44)
        else:
            self.chip(540, 300, "stuck", T["t_stuck"] - 0.2, T["t_dig"] - 0.1, accent=WARN, size=42)
            self.chip(540, 300, "parked", T["t_dig"] + 0.2, self.duration + 1, accent=HILITE, size=44)
            bubble(c, 330, 860, self.L["phone"], self.span(T["t_laund"] - 0.1, self.duration + 1), tail_left=True, size=46)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DESERT, horizon_y=H * 0.62)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.5, T["congrats"]), 61), -24), (0.2, sfx.whoosh(0.8, False, 62), -16),
              (T["longer"], sfx.pop(63), -8), (T["desert"], sfx.whoosh(0.5, False, 64), -14),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10), (T["congrats"] + 0.1, water_snd(0.6, 41), -12),
              (T["congrats"] + 0.15, sfx.sparkle(0.9, 12, 66), -8), (T["suez"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["around"], sfx.whirr(1.4, 70.0, 90.0, 68), -16),
               (T["africa1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -4), (T["cut"], rumble(1.6, 70), -14),
               (T["red1"], sfx.ding(), -8), (T["red1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["water"], sfx.buzz(0.4), -14),
               (T["thou1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["fresh"], sfx.hiss(1.2, 73), -16),
               (T["city"], sfx.sparkle(0.7, 10, 74), -10), (T["city1"], sfx.ding(), -8), (T["city1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 75), -4)]
        for k in range(4):
            ev.append((T["basket"] + k * 0.35, sfx.thud(0.25, 76 + k), -16))
        ev += [(T["forever1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 80), -4), (T["steam"], sfx.hiss(0.8, 81), -12),
               (T["bottom"], sfx.whirr(1.6, 60.0, 80.0, 82), -14), (T["pour"], sfx.hiss(1.4, 83), -18),
               (T["slides1"], sfx.ding(), -8), (T["slides1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 84), -4), (T["both1"], sfx.clank(300.0, 0.5, 85), -8),
               (T["both1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 86), -4), (T["convoys"], sfx.whoosh(0.7, False, 87), -14),
               (T["flooded"], water_snd(0.6, 41), -12), (T["flood1"], sfx.ding(), -8), (T["flood1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(88), 0), (T["follow"] - 0.15, sfx.pop(89), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 90), -6), (T["met"], water_snd(0.6, 41), -10),
               (T["met"] + 0.1, sfx.sparkle(1.0, 14, 91), -8), (T["trip1"] - 0.12, sfx.whoosh(0.45, True, 92), -6),
               (T["shorter"], sfx.chime(), -8)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 93), -6), (T["s1"], sfx.pop(94), -3), (T["s2"], sfx.pop(95), -3),
               (T["s3"], sfx.pop(96), -3)]
        ev += [(T["cong2"], sfx.pop(97), -2), (T["cong2"], sfx.sparkle(1.4, 18, 98), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 99), -6), (T["t_stuck"], sfx.creak(0.9, 100), -10),
               (T["t_cheer"], sfx.pop(101), -6), (T["t_dig"], sfx.buzz(0.3), -14), (T["t_laund"], sfx.pop(102), -6)]
        return ev


NAME = "suez"
EPISODE = Suez
