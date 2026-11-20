"""Episode 50 - A Korean heated floor (the ondol).  v2 look: a snowy winter night in a hanok village, warm orange
light inside; smoke and heat shown as moving dashes and glows.

Sets: house (hook: a hanok cut open in the snow, the kitchen fire under the rice pot, its smoke running under the
room's floor to the chimney, the floor glowing warm, the family on it; fix1: the kitchen fire's double duty; reveal:
grandma at the warmest spot, dad's rice bowl under the blanket; closer), winter (break1: the village in snow, a
thermometer at minus fifteen, a small precious bundle of firewood), plan (break2/fix2: the underside of the floor from
above, one straight channel heats one strip, then rows of stone channels spread the smoke and flat stones are laid on
top), layers (break3/fix3: the floor in section, the fire dies and the night is long; thick clay soaks up the heat like a
battery and stays warm until morning), room (break4/fix4: a dusty clay floor where people sit, eat and sleep; oiled
paper glued down: smooth, shiny, wiped clean), city (stat: Seoul apartments with heating pipes in every floor, then a
low American house), tag (EN: dad guards the thermostat like a bank vault; AR: the barefoot kid on cold tiles and mom
with the slippers).
World (house): side view in section, the ground at y = 0, the room's floor surface at y = -110, about 1 m = 110 units.
"""
from v2_base import *  # noqa: F401,F403
from falaj import word  # noqa: E402
from windtower import arrow, thermo, heat_lines  # noqa: E402
from igloo import blizzard  # noqa: E402
from phone import mom  # noqa: E402

WINTER = {"top": "#030712", "upper": "#0B1433", "mid": "#1B2A55", "low": "#3A4A7A", "horizon": "#7A86B0",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SNOW, SNOW_D = "#8DA2C0", "#4E6488"
WOOD, WOOD_D = "#7A4E2E", "#4A2E1A"
WALL, WALL_D = "#D8C9A8", "#A8977A"
CLAY, CLAY_D = "#9A6B44", "#6B4528"
STONE, STONE_D = "#7C7F86", "#4A4D55"
PAPER = "#D9A441"
ROOF, ROOF_D = "#3A4150", "#232833"
FIRE = "#FF8A3D"
FLOOR_Y = -110


def heat(v):
    """0 cold blue .. 1 warm orange."""
    v = clamp(v)
    return mix("#3B82F6", "#F59E0B", v) if v < 0.75 else mix("#F59E0B", "#EF4444", (v - 0.75) / 0.25)


def path_of(pts, close=False):
    p_ = skia.Path()
    p_.moveTo(*pts[0])
    for q in pts[1:]:
        p_.lineTo(*q)
    if close:
        p_.close()
    return p_


def smooth_path(pts):
    p_ = skia.Path()
    p_.moveTo(*pts[0])
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        p_.quadTo(pts[i][0], pts[i][1], mx, my)
    p_.lineTo(*pts[-1])
    return p_


def smoke_dash(c, pts, t, col="#9CA3AF", a=1.0, w=16, speed=1.0, dash=34, gap=22):
    if a <= 0:
        return
    pnt = P(col, a, stroke=w)
    pnt.setPathEffect(skia.DashPathEffect.Make([dash, gap], -t * 160 * speed))
    c.drawPath(smooth_path(pts), pnt)


def fire(c, x, y, s, t, k=1.0, a=1.0):
    """Flames on logs at (x, y) (base), k 0..1 how strong (0 = embers)."""
    if a <= 0:
        return
    for i in range(3):
        c.save()
        c.translate(x + (i - 1) * 18 * s, y)
        c.rotate((i - 1) * 18)
        c.drawRRect(rr(-30 * s, -6 * s, 60 * s, 12 * s, 6 * s), P(WOOD_D, a))
        c.restore()
    add_glow(c, x, y - 10 * s, 90 * s * (0.4 + k), FIRE, 0.7 * a * (0.3 + 0.7 * k))
    if k > 0.05:
        v2.flame(c, x, y - 4 * s, 44 * s * k, 90 * s * k, t, power=k, seed=3)
    for i in range(5):
        c.drawCircle(x + (i - 2) * 9 * s, y - 2 * s, 5 * s, P("#FF6A2A", a * (0.5 + 0.5 * math.sin(t * 7 + i))))


def hanok(c, t, fire_k=1.0, smoke=1.0, warm=1.0, snow=1.0, paper=1.0, steam=1.0, lamp=1.0, night=1.0):
    """The house cut open (world space): kitchen with the stove and rice pot on the left, the room with its layered
    floor in the middle, the chimney outside on the right, the tiled roof with snow on top."""
    # ---- earth in section and snowy ground outside
    c.drawRect(R(-1800, 0, 3600, 1600), lin_paint(0, 0, 0, 500, ["#5A4030", "#2A1E16"]))
    for sx0, sx1 in ((-1800, -760), (420, 1800)):
        c.drawRect(R(sx0, -18, sx1 - sx0, 22), P(SNOW))
        c.drawRect(R(sx0, -18, sx1 - sx0, 6), P("#AFC3DA"))
    # ---- kitchen: sunken floor, stove, the pot
    c.drawRect(R(-760, -390, 460, 460), lin_paint(0, -390, 0, 70, ["#3A2C22", "#2A2018"]))
    c.drawRect(R(-760, 60, 460, 20), P("#4A3626"))
    st = skia.Path()                                                        # the stove (buttumak) against the room
    st.moveTo(-500, 60)
    st.lineTo(-500, -60)
    st.lineTo(-300, -60)
    st.lineTo(-300, 60)
    st.close()
    c.drawPath(st, lin_paint(-500, 0, -300, 0, ["#8A6A4E", "#6A4E38"]))
    c.drawRRect(rr(-490, -10, 70, 70, 30), P("#140C08"))                    # the firebox mouth
    fire(c, -440, 52, 0.8, t, k=fire_k)
    c.drawOval(R(-470, -96, 170, 50), P("#1F2328"))                         # the iron pot (sot) and its lid
    c.drawOval(R(-450, -112, 130, 34), P("#2E3440"))
    c.drawRect(R(-392, -128, 6, 18), P("#2E3440"))
    if steam > 0:
        for k in range(4):
            q = (t * 0.5 + k * 0.25) % 1.0
            v2.puff(c, -385 + math.sin(q * 6 + k) * 14, -130 - q * 160, 14 + q * 26, "#E5E7EB", 0.45 * steam * (1 - q), k=k)
    # ---- the room
    c.drawRect(R(-300, -440, 720, 330), lin_paint(0, -440, 0, FLOOR_Y, ["#4A3A2E", "#6A5440"]))
    win = R(-150, -380, 220, 180)                                           # a paper window, lit from inside
    c.drawRect(win, P("#F2D7A0", 0.75 * lamp + 0.15))
    for k in range(1, 4):
        c.drawLine(-150 + k * 55, -380, -150 + k * 55, -200, P(WOOD, stroke=4))
    for k in range(1, 4):
        c.drawLine(-150, -380 + k * 45, 70, -380 + k * 45, P(WOOD, stroke=4))
    c.drawRect(win, P(WOOD, stroke=8))
    c.drawRect(R(-300, -440, 22, 330), P(WOOD))
    c.drawRect(R(398, -440, 22, 330), P(WOOD))
    # ---- the floor in section: flues, stones, clay, paper
    c.drawRect(R(-300, -50, 720, 80), P("#1A120E"))                         # the flue space
    for k in range(9):                                                      # stone supports (gorae walls)
        c.drawRect(R(-280 + k * 82, -50, 22, 80), P(STONE_D))
    c.drawRect(R(-300, -72, 720, 22), lin_paint(0, -72, 0, -50, [STONE, STONE_D]))
    for k in range(8):
        c.drawLine(-290 + k * 92, -72, -290 + k * 92, -50, P("#2E3036", stroke=3))
    c.drawRect(R(-300, -104, 720, 32), lin_paint(0, -104, 0, -72, [CLAY, CLAY_D]))
    c.drawRect(R(-300, FLOOR_Y, 720, 6), P(PAPER, paper))
    if warm > 0:                                                            # warmth: hotter near the fire
        c.drawRect(R(-300, FLOOR_Y, 720, 80), lin_paint(-300, 0, 420, 0, [("#FF7A1A", 0.55 * warm), ("#FFB347", 0.35 * warm)]))
        add_glow(c, 60, FLOOR_Y - 10, 380, "#FF9A3D", 0.35 * warm)
        heat_lines(c, -260, 380, FLOOR_Y - 150, FLOOR_Y - 8, t, a=0.6 * warm)
    # ---- the pit and the chimney outside
    c.drawRect(R(420, -50, 180, 90), P("#1A120E"))
    c.drawRect(R(530, -560, 70, 560), lin_paint(530, 0, 600, 0, ["#8A8A90", "#55585F"]))
    for k in range(10):
        c.drawLine(530, -k * 56, 600, -k * 56, P("#45484F", stroke=3))
    c.drawRect(R(522, -580, 86, 24), P("#55585F"))
    if smoke > 0:
        pts = [(-440, 30), (-330, -10), (-200, -16), (60, -12), (330, -16), (440, 0), (560, -20), (565, -300), (565, -570)]
        smoke_dash(c, pts, t, col="#C8CCD4", a=0.75 * smoke, w=18, speed=1.0)
        for k in range(5):                                                  # smoke out of the chimney
            q = (t * 0.35 + k * 0.2) % 1.0
            v2.puff(c, 565 + q * 120, -600 - q * 260, 20 + q * 50, "#9CA3AF", 0.55 * smoke * (1 - q), k=k)
    # ---- walls of the kitchen, the roof
    c.drawRect(R(-780, -390, 24, 450), P(WOOD))
    rf = skia.Path()
    rf.moveTo(-900, -400)
    rf.quadTo(-700, -470, -560, -560)
    rf.quadTo(-300, -760, 60, -770)
    rf.quadTo(420, -760, 620, -560)
    rf.quadTo(760, -470, 940, -400)
    rf.lineTo(900, -430)
    rf.quadTo(600, -470, 420, -440)
    rf.lineTo(-780, -440)
    rf.quadTo(-860, -430, -900, -400)
    rf.close()
    c.drawPath(rf, lin_paint(0, -770, 0, -400, [ROOF, ROOF_D]))
    for k in range(26):                                                     # tile rows
        x = -840 + k * 70
        c.drawLine(x, -440, x + (x - 60) * 0.06, -700 + abs(x - 60) * 0.32, P("#1A1E26", 0.6, stroke=4))
    if snow > 0:
        sp = skia.Path()
        sp.moveTo(-860, -420)
        sp.quadTo(-700, -480, -560, -575)
        sp.quadTo(-300, -775, 60, -786)
        sp.quadTo(420, -775, 620, -575)
        sp.quadTo(760, -480, 900, -420)
        sp.quadTo(600, -560, 60, -740)
        sp.quadTo(-480, -560, -860, -420)
        sp.close()
        c.drawPath(sp, P("#AFC3DA", 0.92 * snow))
    c.drawRect(R(-760, -440, 1180, 16), P(WOOD_D))


def family(c, t, x0=-160, sleep=0.0, a=1.0):
    """Three people sitting on the warm floor (world space, the floor at FLOOR_Y)."""
    for k, (dx, col, h, hair) in enumerate(((0, "#9333EA", 110, "#E5E7EB"), (130, "#2563EB", 125, "#1C1917"),
                                             (240, "#F59E0B", 90, "#1C1917"))):
        person(c, x0 + dx, FLOOR_Y, h, col, t + k * 0.6, pose="sit", face=1 if k == 0 else -1, hat="none", hair=hair, a=a)


def stone_slab(c, x, y, w, h, seed, a=1.0):
    rng = random.Random(seed)
    pts = [(x + rng.uniform(-6, 6), y + rng.uniform(-6, 6)), (x + w + rng.uniform(-6, 6), y + rng.uniform(-6, 6)),
           (x + w + rng.uniform(-6, 6), y + h + rng.uniform(-6, 6)), (x + rng.uniform(-6, 6), y + h + rng.uniform(-6, 6))]
    c.drawPath(path_of(pts, close=True), lin_paint(x, y, x + w, y + h, ["#9A9EA6", STONE, STONE_D], a=a))
    c.drawPath(path_of(pts, close=True), P("#3A3D44", a, stroke=3))


def clock(c, x, y, r, hours, a=1.0):
    """A wall clock; hours = hours after midnight (fractional)."""
    if a <= 0:
        return
    c.drawCircle(x, y, r, P("#F8FAFC", a))
    c.drawCircle(x, y, r, P("#1F2937", a, stroke=r * 0.1))
    for k in range(12):
        an = math.radians(k * 30)
        c.drawLine(x + math.sin(an) * r * 0.78, y - math.cos(an) * r * 0.78, x + math.sin(an) * r * 0.9,
                   y - math.cos(an) * r * 0.9, P("#1F2937", a, stroke=r * 0.05))
    ha = math.radians((hours % 12) * 30)
    ma = math.radians((hours % 1) * 360)
    c.drawLine(x, y, x + math.sin(ha) * r * 0.5, y - math.cos(ha) * r * 0.5, P("#1F2937", a, stroke=r * 0.09))
    c.drawLine(x, y, x + math.sin(ma) * r * 0.75, y - math.cos(ma) * r * 0.75, P("#1F2937", a, stroke=r * 0.06))
    c.drawCircle(x, y, r * 0.07, P("#EF4444", a))


def battery(c, x, y, w, h, frac, a=1.0):
    if a <= 0:
        return
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, h * 0.18), P("#0B1220", 0.8 * a))
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, h * 0.18), P("#F8FAFC", a, stroke=6))
    c.drawRRect(rr(x + w / 2, y - h * 0.18, w * 0.08, h * 0.36, 4), P("#F8FAFC", a))
    fw = (w - 20) * clamp(frac)
    col = mix(WARN, GOOD, clamp(frac * 1.6))
    c.drawRRect(rr(x - w / 2 + 10, y - h / 2 + 10, fw, h - 20, 8), P(col, a))


def blanket(c, x, y, w, col, a=1.0):
    c.drawRRect(rr(x - w / 2, y - 40, w, 44, 20), P(col, a))
    c.drawRRect(rr(x - w / 2, y - 40, w, 12, 10), P(shade(col, 0.15), a))
    for k in range(4):
        c.drawLine(x - w / 2 + 20 + k * (w - 40) / 3.0, y - 34, x - w / 2 + 20 + k * (w - 40) / 3.0, y, P(shade(col, -0.2), 0.6 * a, stroke=3))


def sleeper(c, x, y, s, col, a=1.0):
    """Someone asleep on the floor (lying left to right, head on the left), under a blanket."""
    c.drawRRect(rr(x - 170 * s, y - 34 * s, 70 * s, 30 * s, 12 * s), P("#F1F5F9", a))       # pillow
    c.drawCircle(x - 135 * s, y - 40 * s, 24 * s, P("#E8B48A", a))                           # head
    c.drawArc(R(x - 160 * s, y - 66 * s, 50 * s, 40 * s), 180, 180, True, P("#1C1917", a))   # hair
    bp = skia.Path()
    bp.moveTo(x - 110 * s, y)
    bp.lineTo(x - 110 * s, y - 40 * s)
    bp.quadTo(x - 20 * s, y - 70 * s, x + 80 * s, y - 50 * s)
    bp.quadTo(x + 150 * s, y - 40 * s, x + 160 * s, y)
    bp.close()
    c.drawPath(bp, P(col, a))
    c.drawPath(bp, P(shade(col, -0.25), a, stroke=3 * s))


def rice_bowl(c, x, y, s, a=1.0, steam=1.0, t=0.0):
    c.drawRRect(rr(x - 34 * s, y - 30 * s, 68 * s, 30 * s, 14 * s), P("#E5E7EB", a))
    c.drawRect(R(x - 34 * s, y - 18 * s, 68 * s, 6 * s), P("#3B82F6", a))
    c.drawOval(R(x - 30 * s, y - 40 * s, 60 * s, 20 * s), P("#FFFFFF", a))
    if steam > 0:
        for k in range(3):
            q = (t * 0.6 + k / 3.0) % 1.0
            c.drawCircle(x + (k - 1) * 12 * s + math.sin(q * 6) * 4 * s, y - 50 * s - q * 50 * s, 6 * s * (1 + q),
                         P("#F1F5F9", 0.5 * a * steam * (1 - q)))


def tower_block(c, x, w, h, t, cut=0.0, pipes=0.0, seed=1):
    """An apartment block (screen space, base y = 1180); cut 0..1 removes the facade to show the floors."""
    base = 1180
    c.drawRect(R(x - w / 2, base - h, w, h), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#2A3352", "#1A2038"]))
    rng = random.Random(seed)
    nf = int(h / 46)
    for f in range(nf):
        y = base - (f + 1) * 46
        for k in range(int(w / 40)):
            if rng.random() < 0.6:
                c.drawRect(R(x - w / 2 + 10 + k * 40, y + 12, 22, 22), P("#FFD58A", 0.85))
    if cut > 0:
        cw = w * 0.86 * cut
        c.drawRect(R(x - cw / 2, base - h + 20, cw, h - 20), P("#3A2E2A"))
        for f in range(nf):
            y = base - f * 46
            c.drawRect(R(x - cw / 2, y - 8, cw, 8), P("#8A8F99"))
            if pipes > 0:
                pp = skia.Path()
                pp.moveTo(x - cw / 2 + 8, y - 4)
                n = 6
                for k in range(n):
                    pp.lineTo(x - cw / 2 + 8 + (k + 0.5) * (cw - 16) / n, y - 4 - (6 if k % 2 else 0))
                c.drawPath(pp, P("#EF4444", pipes, stroke=4))
                add_glow(c, x, y - 4, cw * 0.5, "#FF7A1A", 0.25 * pipes)
            person(c, x - cw * 0.2 + (f % 3) * 20, y - 8, 30, SHIRTS[f % 3], t + f, pose="sit", face=1, a=cut)


# ====================================================================================== the episode
class Ondol(EpisodeV2):
    BUILD_NO = 50
    FIRST_SET = "house"
    CLEAR = "#0B1433"
    TITLE = {"en": "KOREAN HEATED FLOOR", "ar_sa": "أرضية كورية دافية"}
    EMPH = {"en": ["CONGRATS", "FIRE", "COOKS", "RICE", "HEATS", "WHOLE", "HOUSE", "FLOOR", "KOREAN", "HEATED", "WINTERS",
                   "MINUS", "FIFTEEN", "FIREWOOD", "PRECIOUS", "KITCHEN", "DOUBLE", "DUTY", "HOT", "SMOKE", "UNDER",
                   "LEAVES", "RUSH", "STRAIGHT", "CHIMNEY", "STRIP", "REST", "COLD", "ROWS", "STONE", "CHANNELS",
                   "SPREAD", "FLAT", "STONES", "TOP", "BURNS", "HOURS", "NIGHT", "LONG", "THICK", "CLAY", "SOAKS",
                   "BATTERY", "WARM", "MORNING", "DUSTY", "SIT", "EAT", "SLEEP", "GLUE", "PAPER", "BEAN", "OIL",
                   "SMOOTH", "SHINY", "WIPE", "FOLLOW", "DUBAI'S", "SAIL-SHAPED", "HOTEL", "GRANDMA", "WARMEST",
                   "SPOT", "DAD'S", "BOWL", "BLANKET", "EVERY", "HOME", "TODAY", "FRANK", "LLOYD", "WRIGHT", "AMERICA",
                   "YOURSELF", "THOUSANDS", "YEARS", "FLOORS", "DAD", "GUARDS", "THERMOSTAT", "BANK", "VAULT"],
            "ar_sa": ["مبروك", "النار", "بتطبخ", "الرز", "بتدفّي", "البيت", "الأرضية", "أرضية", "كورية", "دافية", "الشتا",
                      "كوريا", "سالب", "خمستاشر", "والحطب", "غالي", "المطبخ", "شغلانتين", "دخانها", "السخن", "تحت",
                      "يطلع", "الدخان", "يجري", "المدخنة", "الباقي", "ساقع", "قنوات", "حجر", "توزّعه", "كلها", "ألواح",
                      "بتطفي", "ساعة", "والليل", "طويل", "بطين", "تخين", "يشرب", "البطارية", "دافي", "الصبح", "الطين",
                      "تراب", "بتقعد", "وتاكل", "وتنام", "فتلزق", "ورق", "بزيت", "الصويا", "ناعم", "ولامع", "ويتمسح",
                      "تابعني", "دبي", "شراع", "لتيتة", "أدفى", "وخبّي", "رز", "أبوك", "البطانية", "سخن", "كوري", "فرانك",
                      "لأمريكا", "بإيدك", "آلاف", "حافي", "البلاط", "وأمك", "الشبشب", "برد"]}
    KEYS = {"ar_sa": {
        ("hook", "FIRE"): "النار", ("hook", "COOKS"): "بتطبخ", ("hook", "RICE"): "الرز", ("hook", "HEATS"): "بتدفّي",
        ("hook", "HOUSE"): "البيت", ("hook", "FLOOR"): "الأرضية", ("hook", "CONGRATS"): "مبروك", ("hook", "KOREAN"): "كورية",
        ("break1", "WINTERS"): "الشتا", ("break1", "KOREAN"): "كوريا", ("break1", "MINUS"): "سالب",
        ("break1", "FIFTEEN"): "خمستاشر", ("break1", "FIREWOOD"): "والحطب", ("break1", "PRECIOUS"): "غالي",
        ("fix1", "KITCHEN"): "المطبخ", ("fix1", "DOUBLE"): "شغلانتين", ("fix1", "SMOKE"): "دخانها", ("fix1", "RUNS"): "يعدّي",
        ("fix1", "UNDER"): "تحت", ("fix1", "LEAVES"): "يطلع",
        ("break2", "SMOKE"): "الدخان", ("break2", "RUSH"): "يجري", ("break2", "CHIMNEY"): "المدخنة",
        ("break2", "STRIP"): "طول", ("break2", "REST"): "الباقي", ("break2", "COLD"): "ساقع",
        ("fix2", "ROWS"): "قنوات", ("fix2", "SPREAD"): "توزّعه", ("fix2", "WHOLE"): "كلها", ("fix2", "LAY"): "وفوقها",
        ("fix2", "FLAT"): "ألواح",
        ("break3", "FIRE"): "النار", ("break3", "BURNS"): "بتطفي", ("break3", "HOURS"): "ساعة", ("break3", "NIGHT"): "والليل",
        ("break3", "LONG"): "طويل",
        ("fix3", "COVER"): "فتغطّي", ("fix3", "CLAY"): "بطين", ("fix3", "SOAKS"): "يشرب", ("fix3", "BATTERY"): "البطارية",
        ("fix3", "WARM"): "دافي", ("fix3", "MORNING"): "الصبح",
        ("break4", "CLAY"): "الطين", ("break4", "DUSTY"): "تراب", ("break4", "PEOPLE"): "والناس", ("break4", "SIT"): "بتقعد",
        ("break4", "EAT"): "وتاكل", ("break4", "SLEEP"): "وتنام",
        ("fix4", "GLUE"): "فتلزق", ("fix4", "PAPER"): "ورق", ("fix4", "OIL"): "بزيت", ("fix4", "SMOOTH"): "ناعم",
        ("fix4", "SHINY"): "ولامع", ("fix4", "WIPE"): "ويتمسح",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "GRANDMA"): "لتيتة", ("reveal", "WARMEST"): "أدفى", ("reveal", "TUCK"): "وخبّي", ("reveal", "RICE"): "رز",
        ("reveal", "BLANKET"): "البطانية", ("reveal", "HOT"): "سخن",
        ("stat", "EVERY"): "كل", ("stat", "KOREAN"): "كوري", ("stat", "FRANK"): "فرانك", ("stat", "AMERICA"): "لأمريكا",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "THOUSANDS"): "آلاف", ("tag", "WARM"): "دافية", ("tag", "DAD"): "حافي", ("tag", "GUARDS"): "البلاط",
        ("tag", "THERMOSTAT"): "وأمك", ("tag", "VAULT"): "الشبشب"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Dubai's sail-shaped hotel"),
                   "stat": [],
                   "L": {"rice": "THE FIRE COOKS THE RICE", "floor": "AND HEATS THE FLOOR", "name": "A KOREAN HEATED FLOOR",
                         "cold": "-15°", "wood": "FIREWOOD IS PRECIOUS", "double": "ONE FIRE, TWO JOBS",
                         "under": "SMOKE RUNS UNDER THE FLOOR", "rush": "STRAIGHT TO THE CHIMNEY", "strip": "ONE HOT STRIP",
                         "restc": "THE REST STAYS COLD", "rows": "ROWS OF STONE CHANNELS", "spread": "IT SPREADS EVERYWHERE",
                         "flat": "FLAT STONES ON TOP", "out": "THE FIRE BURNS OUT", "long": "THE NIGHT IS LONG",
                         "clay": "THICK CLAY", "batt": "IT STORES THE HEAT", "morning": "WARM UNTIL MORNING",
                         "dusty": "CLAY FLOORS ARE DUSTY", "live": "SIT, EAT AND SLEEP HERE", "paper": "PAPER + BEAN OIL",
                         "shiny": "SMOOTH AND SHINY", "wipe": "WIPES CLEAN", "grandma": "THE WARMEST SPOT: GRANDMA",
                         "bowl": "DAD'S RICE, KEPT HOT", "korea": "ALMOST EVERY KOREAN HOME TODAY",
                         "flw": "FRANK LLOYD WRIGHT TOOK IT TO AMERICA", "mom": "PUT YOUR SLIPPERS ON!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: فندق دبي اللي شكله شراع"),
                      "stat": [],
                      "L": {"rice": "النار بتطبخ الرز", "floor": "وبتدفّي الأرضية", "name": "أرضية كورية دافية",
                            "cold": "-15°", "wood": "الحطب غالي", "double": "نار واحدة، شغلانتين",
                            "under": "الدخان بيعدّي تحت الأرضية", "rush": "على المدخنة على طول", "strip": "حتة واحدة سخنة",
                            "restc": "والباقي ساقع", "rows": "قنوات حجر", "spread": "توزّع الدخان على الكل",
                            "flat": "ألواح حجر فوقها", "out": "النار بتطفي", "long": "والليل طويل", "clay": "طين تخين",
                            "batt": "بيشيل السخونية", "morning": "دافي لحد الصبح", "dusty": "الطين بيعمل تراب",
                            "live": "قعدة وأكل ونوم على الأرض", "paper": "ورق بزيت الصويا", "shiny": "ناعم ولامع",
                            "wipe": "بيتمسح بسهولة", "grandma": "أدفى حتة لتيتة", "bowl": "طبق رز أبوك سخن",
                            "korea": "تحت كل بيت كوري تقريبًا", "flw": "فرانك لويد رايت نقلها لأمريكا",
                            "mom": "البس الشبشب!"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "fire": ("hook", "FIRE", 0.08), "cooks": ("hook", "COOKS", 0.15), "rice": ("hook", "RICE", 0.22),
            "heats": ("hook", "HEATS", 0.32), "house": ("hook", "HOUSE", 0.42), "floor": ("hook", "FLOOR", 0.52),
            "congrats": ("hook", "CONGRATS", 0.6), "korean": ("hook", "KOREAN", 0.82),
            "winters": ("break1", "WINTERS", 0.12), "minus": ("break1", "MINUS", 0.45), "fifteen": ("break1", "FIFTEEN", 0.52),
            "firewood": ("break1", "FIREWOOD", 0.72), "precious": ("break1", "PRECIOUS", 0.88), "kor1": ("break1", "KOREAN", 0.05),
            "kitchen": ("fix1", "KITCHEN", 0.1), "double": ("fix1", "DOUBLE", 0.28), "smoke": ("fix1", "SMOKE", 0.5),
            "runs": ("fix1", "RUNS", 0.56), "under": ("fix1", "UNDER", 0.62), "leaves": ("fix1", "LEAVES", 0.9),
            "smoke2": ("break2", "SMOKE", 0.05), "rush": ("break2", "RUSH", 0.18), "chimney": ("break2", "CHIMNEY", 0.38),
            "strip": ("break2", "STRIP", 0.62), "rest": ("break2", "REST", 0.85), "cold": ("break2", "COLD", 0.95),
            "rows": ("fix2", "ROWS", 0.15), "spread": ("fix2", "SPREAD", 0.4), "whole": ("fix2", "WHOLE", 0.58),
            "lay": ("fix2", "LAY", 0.72), "flat": ("fix2", "FLAT", 0.78),
            "fire3": ("break3", "FIRE", 0.1), "burns": ("break3", "BURNS", 0.25), "hours": ("break3", "HOURS", 0.55),
            "night": ("break3", "NIGHT", 0.8), "long": ("break3", "LONG", 0.92),
            "cover": ("fix3", "COVER", 0.06), "clay": ("fix3", "CLAY", 0.3), "soaks": ("fix3", "SOAKS", 0.45),
            "battery": ("fix3", "BATTERY", 0.62), "warm": ("fix3", "WARM", 0.8), "morning": ("fix3", "MORNING", 0.92),
            "clay4": ("break4", "CLAY", 0.08), "dusty": ("break4", "DUSTY", 0.25), "people": ("break4", "PEOPLE", 0.5),
            "sit": ("break4", "SIT", 0.6), "eat": ("break4", "EAT", 0.7), "sleep": ("break4", "SLEEP", 0.8),
            "glue": ("fix4", "GLUE", 0.08), "paper": ("fix4", "PAPER", 0.2), "oil": ("fix4", "OIL", 0.45),
            "smooth": ("fix4", "SMOOTH", 0.6), "shiny": ("fix4", "SHINY", 0.7), "wipe": ("fix4", "WIPE", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "grandma": ("reveal", "GRANDMA", 0.06), "warmest": ("reveal", "WARMEST", 0.18), "tuck": ("reveal", "TUCK", 0.4),
            "rice2": ("reveal", "RICE", 0.5), "blanket": ("reveal", "BLANKET", 0.72), "hot": ("reveal", "HOT", 0.95),
            "every": ("stat", "EVERY", 0.15), "kor2": ("stat", "KOREAN", 0.25), "frank": ("stat", "FRANK", 0.55),
            "america": ("stat", "AMERICA", 0.92),
            "cong2": ("closer", "CONGRATS", 0.16),
            "thousands": ("tag", "THOUSANDS", 0.03), "warm2": ("tag", "WARM", 0.2), "dad": ("tag", "DAD", 0.45),
            "guards": ("tag", "GUARDS", 0.55), "thermo": ("tag", "THERMOSTAT", 0.68), "vault": ("tag", "VAULT", 0.88)})
        T["t2"] = T["dad"] - 0.2
        T["t3"] = max(T["thermo"], T["vault"] - 0.4) if not self.rtl else T["vault"] - 0.3
        T["flat0"] = min(T["lay"], T["flat"]) - 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "winter", 1)
        self.cut(s("fix1") - 0.12, "house", -1)
        self.cut(s("break2") - 0.12, "plan", 1)
        self.cut(s("break3") - 0.12, "layers", -1)
        self.cut(s("break4") - 0.12, "room", 1)
        self.cut(s("reveal") - 0.12, "house", -1)
        self.cut(s("stat") - 0.12, "city", 1)
        self.cut(s("closer") - 0.12, "house", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- house camera
        cm = Camera(-260, -110, 1.3)
        cm.key(0.1, -250, -120, 1.22, max(0.5, T["rice"] - 0.1))
        cm.key(T["rice"], -100, -200, 0.95, 1.2)
        cm.key(T["floor"], -70, -250, 0.78, 1.1)
        cm.key(T["korean"], -70, -240, 0.8, 1.0)
        cm.key(s("fix1") - 0.12, -330, -60, 1.3, 0.0).key(T["smoke"] - 0.3, 0, -120, 0.85, 1.4)
        cm.key(T["leaves"] - 0.2, 0, -250, 0.74, 1.0)
        cm.key(s("reveal") - 0.12, -150, -160, 1.3, 0.0).key(T["tuck"] - 0.2, 40, -170, 1.25, 1.2)
        cm.key(s("closer") - 0.12, -75, -200, 0.74, 0.0).key(self.duration, -75, -205, 0.77, 5.0)
        self.cam = cm
        self.spans = [(T["precious"], T["leaves"] + 0.3), (T["cold"], T["flat"] + 0.3), (T["long"], T["morning"] + 0.3),
                      (T["sleep"], T["wipe"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["precious"], 0.3, 6), (T["cold"], 0.3, 6), (T["long"], 0.3, 6),
                       (T["dusty"], 0.3, 5), (s("closer") + 0.2, 0.35, 9), (T["t3"], 0.35, 8)]

    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    # ------------------------------------------------------------------ set: house
    def draw_house(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=WINTER, horizon_y=gy)
        v2.stars(c, W, H, t, 0.8)
        v2.moon(c, 860 - cx * 0.05, gy - 900 * z, 50)
        self.view(c, cam)
        for k in range(7):                                                  # snowy hills and a far house
            c.drawOval(R(-2200 + k * 700, -120, 900, 260), P("#5A6E92" if k % 2 else "#4A5C80"))
        hook = t < s("break1") - 0.12
        fix1 = s("fix1") - 0.12 <= t < s("break2") - 0.12
        reveal = s("reveal") - 0.12 <= t < s("stat") - 0.12
        smoke = warm = 1.0
        if hook:
            warm = lerp(0.55, 1.0, prog(t, T["house"] - 0.3, T["floor"] + 0.5))
        if fix1:
            smoke = prog(t, T["smoke"] - 0.3, T["runs"] + 0.4)
            warm = prog(t, T["under"], T["leaves"] + 0.6)
        hanok(c, t, fire_k=1.0, smoke=smoke, warm=warm, snow=1.0, paper=1.0)
        if reveal or t >= s("closer") - 0.12:
            gk = prog(t, T["grandma"] - 0.2, T["warmest"] + 0.3) if reveal else 1.0
            person(c, -230, FLOOR_Y, 105, "#9333EA", t, pose="sit", face=1, hat="none", hair="#E5E7EB", a=max(gk, 0.0))
            if gk > 0:
                add_glow(c, -230, FLOOR_Y - 20, 120, "#FFB347", 0.4 * gk)
            bk = prog(t, T["tuck"] - 0.2, T["blanket"] + 0.3) if reveal else 1.0
            rice_bowl(c, 120, FLOOR_Y - 34 + 30 * bk, 1.2, a=1.0, steam=1 - bk, t=t)
            blanket(c, 140, FLOOR_Y, 300, "#DC2626", a=bk)
            if t >= s("closer") - 0.12:
                blanket(c, 260, FLOOR_Y, 180, "#2563EB")
                person(c, 30, FLOOR_Y, 120, "#2563EB", t, pose="sit", face=-1, hat="none", hair="#1C1917")
                person(c, 330, FLOOR_Y, 85, "#F59E0B", t, pose="sit", face=-1, hat="none", hair="#1C1917")
        else:
            family(c, t, x0=-120)
        c.restore()
        blizzard(c, t, a=0.5, n=60, slant=0.25, speed=0.35, seed=5)
        self.ui["cam"] = cam

    def ui_house(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (0, -220, 0.8))
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "rice", T["cooks"] - 0.15, T["heats"] - 0.1, accent="#FDBA74", size=42)
            self.chip(540, 300, "floor", T["heats"] - 0.1, T["congrats"] - 0.05, accent="#FB923C", size=44)
            self.chip(540, 300, "name", T["korean"] - 0.15, s("break1") + 0.1, accent=HILITE, size=46)
            return
        if tw < s("break2") - 0.12:
            self.chip(540, 300, "double", T["kitchen"] - 0.1, T["smoke"] - 0.15, accent=HILITE, size=44)
            self.chip(540, 300, "under", T["smoke"] - 0.15, s("break2") - 0.15, accent="#E5E7EB", size=40)
            self.badge("check", T["leaves"] + 0.05, s("break2") - 0.15, x=920, y=420)
            return
        if tw < s("stat") - 0.12:
            gx, gy_ = self.at(cam, -230, FLOOR_Y - 120)
            self.label(gx, gy_, 300, 560, "grandma", T["grandma"] - 0.1, T["tuck"] - 0.1, "#FDBA74", size=36)
            bx, by = self.at(cam, 140, FLOOR_Y - 40)
            self.label(bx, by, 760, 560, "bowl", T["tuck"] - 0.1, s("stat") - 0.15, "#FCA5A5", size=36)

    # ------------------------------------------------------------------ set: winter (break1)
    def draw_winter(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.0, pal=WINTER, horizon_y=1000)
        v2.stars(c, W, H, t, 0.9)
        v2.moon(c, 820, 360, 54)
        c.drawRect(R(0, 1000, W, H - 1000), lin_paint(0, 1000, 0, H, [SNOW, SNOW_D]))
        for k in range(4):                                                  # snowy hanok roofs, far to near
            x = 120 + k * 280
            y = 1000 - (k % 2) * 30
            c.drawRect(R(x - 90, y - 90, 180, 90), P(WALL_D))
            c.drawRect(R(x - 40, y - 70, 50, 50), P("#FFD58A", 0.8))
            rp = skia.Path()
            rp.moveTo(x - 150, y - 80)
            rp.quadTo(x - 60, y - 110, x, y - 170)
            rp.quadTo(x + 60, y - 110, x + 150, y - 80)
            rp.close()
            c.drawPath(rp, P(ROOF))
            sp = skia.Path()
            sp.moveTo(x - 140, y - 90)
            sp.quadTo(x - 60, y - 118, x, y - 176)
            sp.quadTo(x + 60, y - 118, x + 140, y - 90)
            sp.quadTo(x, y - 140, x - 140, y - 90)
            c.drawPath(sp, P("#AFC3DA"))
        blizzard(c, t, a=0.9, n=110, slant=0.4, speed=0.8, seed=8)
        fk = prog(t, T["minus"] - 0.4, T["fifteen"] + 0.2)
        thermo(c, 880, 860, 1.6, lerp(0.5, 0.05, fk), a=1.0)
        if fk > 0:
            word(c, self.L["cold"], 660, 700, 96, "#93C5FD", a=fk)
        wk = prog(t, T["firewood"] - 0.3, T["firewood"] + 0.2)
        person(c, 330, 1180, 230, "#1D4ED8", t, pose="carry", face=1, hat="beanie", hair="#1C1917")
        if wk > 0:                                                          # a small bundle of firewood
            for k in range(4):
                c.drawRRect(rr(300 + k * 6, 990 - k * 14, 110, 16, 7), P(WOOD if k % 2 else WOOD_D, wk))
            c.drawLine(350, 980, 350, 1010, P("#1F2937", wk, stroke=4))
        self.ui["fk"] = fk

    def ui_winter(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "wood", T["firewood"] - 0.15, s("fix1") - 0.15, accent="#FDBA74", size=44)
        self.badge("alert", T["precious"] + 0.05, s("fix1") - 0.2, x=920, y=420)
        self.red(T["precious"] + 0.05, 1.2)

    # ------------------------------------------------------------------ set: plan (break2, fix2), from above
    def draw_plan(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        vrect(c, 0, 0, W, H, ["#1A1E2E", "#252A3E"])
        x0, x1, y0, y1 = 170, 910, 470, 1130
        c.drawRect(R(x0 - 20, y0 - 20, x1 - x0 + 40, y1 - y0 + 40), P("#5A4030"))
        c.drawRect(R(x0, y0, x1 - x0, y1 - y0), P("#2A1E16"))
        fx_, fy_ = 90, 800                                                  # the firebox (kitchen side)
        chx, chy = 1000, 800                                                # the chimney
        c.drawRRect(rr(fx_ - 60, fy_ - 60, 120, 120, 20), P("#140C08"))
        fire(c, fx_, fy_ + 30, 0.9, t, k=1.0)
        c.drawCircle(chx, chy, 46, P("#55585F"))
        c.drawCircle(chx, chy, 30, P("#1A1A1E"))
        # heat map
        nx, ny = 14, 12
        cw_, ch_ = (x1 - x0) / nx, (y1 - y0) / ny
        rows = [560, 680, 800, 920, 1040]
        spread = prog(t, T["spread"] - 0.3, T["whole"] + 0.4) if fixed else 0.0
        stripk = prog(t, T["strip"] - 0.4, T["strip"] + 0.3) if not fixed else 1 - spread
        for i in range(nx):
            for j in range(ny):
                cx_ = x0 + (i + 0.5) * cw_
                cy_ = y0 + (j + 0.5) * ch_
                d = abs(cy_ - 800) / 330.0
                v_strip = clamp(1.0 - d * 3.0) * (1 - 0.25 * i / nx)
                v_even = 0.8 - 0.15 * i / nx
                v = lerp(0.1, v_strip, stripk) * (1 - spread) + v_even * spread
                c.drawRect(R(cx_ - cw_ / 2 + 2, cy_ - ch_ / 2 + 2, cw_ - 4, ch_ - 4), P(heat(v), 0.55))
        if not fixed:
            c.drawRect(R(x0, 780, x1 - x0, 40), P("#0A0705"))
            sk = prog(t, T["smoke2"] - 0.3, T["rush"])
            smoke_dash(c, [(fx_ + 40, fy_), (500, 800), (chx - 40, chy)], t, a=sk, w=22, speed=2.2)
            if sk > 0:
                arrow(c, 900, 800, chx - 50, 800, "#E5E7EB", a=sk, w=10, head=30)
        else:
            rk = prog(t, T["rows"] - 0.3, T["rows"] + 0.6)
            c.drawRect(R(x0 + 20, y0 + 50, 40, (y1 - y0) - 100), P("#0A0705", rk))      # the feed trench
            c.drawRect(R(x1 - 60, y0 + 50, 40, (y1 - y0) - 100), P("#0A0705", rk))      # the collecting trench
            for k, ry in enumerate(rows):
                c.drawRect(R(x0 + 40, ry - 20, (x1 - x0 - 80) * clamp(rk * 1.6 - k * 0.15), 40), P("#0A0705"))
            sk = prog(t, T["spread"] - 0.4, T["spread"] + 0.2)
            for k, ry in enumerate(rows):
                smoke_dash(c, [(fx_ + 40, fy_), (x0 + 40, ry), (x1 - 40, ry), (chx - 40, chy)], t + k * 0.13, a=sk * 0.85,
                           w=16, speed=1.2)
            fl = prog(t, T["flat0"], s("break3") - 0.6)
            n = 0
            for j in range(5):                                              # flat stones laid on top, row by row
                for i in range(6):
                    if fl * 30 > n:
                        stone_slab(c, x0 + 12 + i * 123, y0 + 12 + j * 130, 116, 122, n * 7 + 3, a=clamp(fl * 30 - n))
                    n += 1
            if fl > 0:
                c.drawRect(R(x0, y0, x1 - x0, y1 - y0), P("#FF8A3D", 0.18 * fl))
        self.ui["fixed"] = fixed

    def ui_plan(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "rush", T["rush"] - 0.15, T["strip"] - 0.2, accent="#E5E7EB", size=42)
            self.chip(540, 300, "strip", T["strip"] - 0.2, T["rest"] - 0.15, accent=WARN, size=44)
            self.chip(540, 300, "restc", T["rest"] - 0.15, s("fix2") - 0.15, accent="#60A5FA", size=44)
            self.badge("alert", T["cold"] + 0.05, s("fix2") - 0.2, x=920, y=400)
            self.red(T["cold"] + 0.05, 1.2)
            return
        self.chip(540, 300, "rows", T["rows"] - 0.15, T["spread"] - 0.15, accent="#E5E7EB", size=42)
        self.chip(540, 300, "spread", T["spread"] - 0.15, T["flat0"] - 0.1, accent="#FDBA74", size=40)
        self.chip(540, 300, "flat", T["flat0"] - 0.1, s("break3") - 0.15, accent="#CBD5E1", size=42)
        self.badge("check", T["flat"] + 0.3, s("break3") - 0.15, x=920, y=400)

    # ------------------------------------------------------------------ set: layers (break3, fix3), section close-up
    def draw_layers(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        vrect(c, 0, 0, W, H, ["#0B1433", "#1B2A55"])
        win = R(620, 420, 300, 240)                                         # a window: night, then sunrise
        dawn = prog(t, T["warm"], T["morning"] + 0.3) if fixed else 0.0
        c.drawRect(win, lin_paint(0, 420, 0, 660, [mix("#0B1433", "#F59E0B", dawn), mix("#1B2A55", "#FDE68A", dawn)]))
        if dawn < 1:
            for k in range(12):
                c.drawCircle(640 + (k * 53) % 280, 440 + (k * 37) % 200, 2.5, P("#FFFFFF", 0.8 * (1 - dawn)))
        c.drawRect(win, P(WOOD, stroke=12))
        c.drawLine(770, 420, 770, 660, P(WOOD, stroke=8))
        c.drawRect(R(0, 860, W, 1100), P("#2A1E16"))
        # the layers: paper, clay (fix3), stones, flue
        clay_k = prog(t, T["cover"] - 0.2, T["clay"] + 0.4) if fixed else 0.0
        top = lerp(900, 820, clay_k)
        c.drawRect(R(0, 990, W, 130), P("#120C08"))                         # the flue
        for k in range(6):
            c.drawRect(R(60 + k * 190, 990, 34, 130), P(STONE_D))
        for k in range(6):
            stone_slab(c, k * 185 - 10, 930, 180, 60, 11 + k)
        if clay_k > 0:
            c.drawRect(R(0, top, W, 930 - top), lin_paint(0, top, 0, 930, [CLAY, CLAY_D]))
            tex(c, R(0, top, W, 930 - top), "sand", 0.8, 0.35)
        c.drawRect(R(0, top - 10, W, 10), P(PAPER))
        # the fire on the left and the heat
        fk = 1.0
        hours = 21.0
        if not fixed:
            fk = 1 - prog(t, T["burns"] - 0.2, T["hours"] + 0.3)
            hours = lerp(21, 27, prog(t, T["burns"], T["long"] + 0.3))
            floor_v = lerp(0.95, 0.15, prog(t, T["hours"], T["long"] + 0.3))
        else:
            fk = 1 - prog(t, T["soaks"], T["battery"] + 0.4)
            hours = lerp(21, 31, prog(t, T["battery"] - 0.2, T["morning"]))
            floor_v = lerp(0.9, 0.78, prog(t, T["battery"], T["morning"]))
        c.drawRect(R(-10, 980, 170, 150), P("#140C08"))
        fire(c, 70, 1110, 1.0, t, k=fk)
        if fk > 0.05:
            smoke_dash(c, [(140, 1060), (500, 1056), (1100, 1056)], t, col="#C8CCD4", a=0.7 * fk, w=18, speed=1.3)
        hv = floor_v
        c.drawRect(R(0, top - 10, W, 30), P(heat(hv), 0.45))
        if hv > 0.5:
            heat_lines(c, 80, 1000, top - 160, top - 16, t, a=(hv - 0.5) * 1.6)
        sleeper(c, 360, top - 10, 1.3, "#DC2626")
        if not fixed and hv < 0.45:
            for k in range(3):                                              # shivers
                c.drawLine(180 + k * 14, top - 150 - k * 10, 200 + k * 14, top - 130 - k * 10, P("#93C5FD", 0.9, stroke=4))
        clock(c, 220, 520, 96, hours)
        if fixed:
            bk = prog(t, T["soaks"] - 0.2, T["soaks"] + 0.6) * (1 - 0.35 * prog(t, T["battery"] + 0.3, T["morning"]))
            battery(c, 540, 760, 230, 100, bk, a=prog(t, T["soaks"] - 0.3, T["soaks"]))
        self.ui["top"] = top

    def ui_layers(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "out", T["burns"] - 0.2, T["night"] - 0.15, accent="#FDBA74", size=44)
            self.chip(540, 300, "long", T["night"] - 0.15, s("fix3") - 0.15, accent="#93C5FD", size=44)
            self.badge("alert", T["long"] + 0.05, s("fix3") - 0.2, x=920, y=400)
            self.red(T["long"] + 0.05, 1.2)
            return
        self.chip(540, 300, "clay", T["cover"] - 0.1, T["soaks"] - 0.15, accent="#D6A77A", size=46)
        self.chip(540, 300, "batt", T["soaks"] - 0.15, T["warm"] - 0.15, accent=GOOD, size=42)
        self.chip(540, 300, "morning", T["warm"] - 0.15, s("break4") - 0.15, accent="#FDBA74", size=42)
        self.badge("check", T["morning"] + 0.1, s("break4") - 0.15, x=920, y=400)

    # ------------------------------------------------------------------ set: room (break4, fix4), front view
    def draw_room(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        vrect(c, 0, 0, W, H, ["#5A4636", "#3E3026"])
        c.drawRect(R(380, 380, 320, 260), P("#F2D7A0", 0.85))               # the hanji window
        for k in range(1, 4):
            c.drawLine(380 + k * 80, 380, 380 + k * 80, 640, P(WOOD, stroke=5))
            c.drawLine(380, 380 + k * 65, 700, 380 + k * 65, P(WOOD, stroke=5))
        c.drawRect(R(380, 380, 320, 260), P(WOOD, stroke=10))
        c.drawRect(R(0, 760, W, 20), P(WOOD_D))
        fl = skia.Path()                                                    # the floor in perspective
        fl.moveTo(0, 780)
        fl.lineTo(W, 780)
        fl.lineTo(W, 1260)
        fl.lineTo(0, 1260)
        fl.close()
        c.drawPath(fl, lin_paint(0, 780, 0, 1260, [CLAY, CLAY_D]))
        tex(c, fl, "sand", 1.0, 0.45)
        pk = 0.0
        if fixed:
            pk = prog(t, T["glue"] - 0.2, T["oil"] + 0.3)
            for k in range(8):                                              # oiled paper laid strip by strip, back to front
                kk = clamp(pk * 8 - k)
                if kk <= 0:
                    continue
                y0 = 780 + k * 60
                c.drawRect(R(0, y0, W * kk, 61), lin_paint(0, y0, 0, y0 + 60, ["#C99A4A", "#A87A30"]))
                c.drawLine(0, y0, W * kk, y0, P("#A8741E", 0.6, stroke=2))
            shk = prog(t, T["shiny"] - 0.3, T["shiny"] + 0.5)
            if 0 < shk < 1:
                sx_ = lerp(-200, W + 200, shk)
                c.drawRect(R(0, 780, W, 480), lin_paint(sx_ - 160, 0, sx_ + 160, 0, [("#FFFFFF", 0.0), ("#FFFFFF", 0.35), ("#FFFFFF", 0.0)]))
        # a low table and the family
        c.drawRRect(rr(380, 900, 320, 40, 12), P(WOOD))
        c.drawRect(R(400, 940, 20, 60), P(WOOD_D))
        c.drawRect(R(660, 940, 20, 60), P(WOOD_D))
        for k in range(3):
            rice_bowl(c, 460 + k * 80, 900, 0.8, steam=1.0, t=t)
        sk = prog(t, T["sit"] - 0.3, T["sit"])
        for k, (px, col, f) in enumerate(((250, "#2563EB", 1), (830, "#DB2777", -1))):
            person(c, px, 1060, 200, col, t + k, pose="sit", face=f, hat="none", hair="#1C1917")
        if not fixed:
            dk = prog(t, T["dusty"] - 0.3, T["dusty"] + 0.3)
            for k in range(8):                                              # dust puffs
                q = (t * 0.5 + k * 0.125) % 1.0
                v2.puff(c, 150 + k * 110, 1080 - q * 160, 30 + q * 40, "#C9A27A", 0.5 * dk * (1 - q) + 0.25 * sk * (1 - q), k=k)
            c.drawRect(R(0, 780, W, 480), P("#B08A60", 0.15 * dk))
        else:
            wk = prog(t, T["wipe"] - 0.5, T["wipe"] + 0.3)
            c.drawOval(R(560, 1110, 200 * (1 - wk) + 1, 60 * (1 - wk) + 1), P("#7C3AED", 0.6 * (1 - wk)))     # a spill, wiped
            if 0 < wk < 1:
                cx_ = lerp(760, 560, wk)
                c.drawRRect(rr(cx_ - 50, 1100, 100, 60, 12), P("#F8FAFC"))
                c.drawCircle(cx_ + 20, 1090, 22, P("#C68B59"))
            if wk >= 1:
                for k in range(3):
                    add_glow(c, 600 + k * 40, 1130, 30, "#FFFFFF", 0.5)

    def ui_room(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "dusty", T["clay4"] - 0.1, T["people"] - 0.15, accent="#D6A77A", size=44)
            self.chip(540, 300, "live", T["people"] - 0.15, s("fix4") - 0.15, accent="#FDBA74", size=40)
            self.badge("alert", T["sleep"] + 0.1, s("fix4") - 0.2, x=920, y=400)
            self.red(T["sleep"] + 0.1, 1.2)
            return
        self.chip(540, 300, "paper", T["glue"] - 0.1, T["smooth"] - 0.15, accent="#FACC15", size=44)
        self.chip(540, 300, "shiny", T["smooth"] - 0.15, T["wipe"] - 0.2, accent="#FDE68A", size=44)
        self.chip(540, 300, "wipe", T["wipe"] - 0.2, s("cta") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["wipe"] + 0.1, s("cta") - 0.15, x=920, y=400)

    # ------------------------------------------------------------------ set: city (stat)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        pan = e_io(prog(t, T["frank"] - 0.4, T["frank"] + 0.8))
        v2.sky(c, W, H, 0.0, pal=WINTER, horizon_y=1180)
        v2.stars(c, W, H, t, 0.8)
        c.save()
        c.translate(-pan * 1100, 0)
        c.drawRect(R(-200, 1180, 3000, 800), P("#1A2038"))
        ck = prog(t, T["every"] - 0.3, T["kor2"] + 0.5)
        for k, (x, w, h) in enumerate(((140, 170, 620), (360, 190, 780), (580, 180, 700), (800, 200, 840), (1010, 160, 560))):
            tower_block(c, x, w, h, t, cut=ck if k in (1, 3) else 0.0, pipes=ck, seed=k + 3)
        # America: a low house with heating pipes in its slab
        ax = 1100 + 540
        c.drawRect(R(ax - 360, 1180, 720, 30), P("#8A8F99"))
        c.drawRect(R(ax - 320, 960, 640, 220), P("#C9A27A"))
        c.drawRect(R(ax - 400, 930, 800, 34), P("#5A4030"))
        for k in range(4):
            c.drawRect(R(ax - 280 + k * 150, 1000, 110, 120), P("#FFD58A", 0.8))
        pp = skia.Path()
        pp.moveTo(ax - 330, 1195)
        for k in range(16):
            pp.lineTo(ax - 330 + (k + 0.5) * 41, 1195 + (8 if k % 2 else -8))
        c.drawPath(pp, P("#EF4444", stroke=6))
        add_glow(c, ax, 1190, 360, "#FF7A1A", 0.35 * pan)
        c.restore()
        if 0 < pan < 1:                                                     # a dashed flight across
            fp = skia.Path()
            fp.moveTo(lerp(540, -560, pan), 700)
            fp.quadTo(540, 420, lerp(1640, 540, pan), 900)
            c.drawPath(fp, dash_paint("#FDE68A", 0.8, w=6, t=t))

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "korea", T["every"] - 0.2, T["frank"] - 0.3, accent="#FB923C", size=36)
        self.chip(540, 300, "flw", T["frank"] - 0.3, s("closer") - 0.15, accent=HILITE, size=32)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:                                                    # dad guards the thermostat like a vault
            vrect(c, 0, 0, W, H, ["#3A3F5A", "#2A2F48"])
            c.drawRect(R(0, 1160, W, H - 1160), P("#5A4030"))
            vk = prog(t, T["t3"] - 0.2, T["t3"] + 0.3)
            vx, vy = 700, 640
            c.drawCircle(vx, vy, 200, P("#6B7280", vk))                      # the vault door around the thermostat
            c.drawCircle(vx, vy, 200, P("#374151", vk, stroke=18))
            for k in range(8):
                an = math.radians(k * 45 + t * 30 * vk)
                c.drawLine(vx + math.cos(an) * 70, vy + math.sin(an) * 70, vx + math.cos(an) * 170, vy + math.sin(an) * 170,
                           P("#D1D5DB", vk, stroke=10))
            c.drawCircle(vx, vy, 74, P("#F8FAFC"))                          # the thermostat
            c.drawCircle(vx, vy, 74, P("#94A3B8", stroke=8))
            word(c, "20°", vx, vy + 22, 54, "#111827")
            if vk > 0:
                for k in range(4):                                          # laser beams
                    c.drawLine(420, 520 + k * 70, 980, 560 + k * 60, P("#EF4444", 0.6 * vk, stroke=3))
            dk = prog(t, T["t2"] - 0.2, T["t2"] + 0.3)
            person(c, 360, 1200, 330, "#2563EB", t, pose="stand", face=1, hat="none", hair="#1C1917", a=max(0.0, dk))
            if dk > 0:
                u = 330 / 140.0
                c.drawRRect(rr(360 - 8 * u, 1200 - 118 * u, 30 * u, 6 * u, 3 * u), P("#1C1917", dk))   # mustache
                c.drawRRect(rr(360 - 6 * u, 1200 - 132 * u, 30 * u, 9 * u, 4 * u), P("#0B0F19", dk))   # sunglasses
                c.drawLine(360 - 30 * u, 1200 - 80 * u, 360 + 30 * u, 1200 - 74 * u, P("#2563EB", dk, stroke=14 * u))   # arms crossed
            person(c, 900, 1210, 150, "#F59E0B", t, pose="look", face=-1, hat="beanie", hair="#1C1917")
            blanket(c, 900, 1150, 120, "#93C5FD")
        else:                                                               # the barefoot kid and mom with the slippers
            vrect(c, 0, 0, W, H, ["#5A6478", "#465066"])
            c.drawRect(R(0, 1000, W, H - 1000), P("#3A4458"))
            for i in range(9):                                              # cold tiles
                for j in range(6):
                    c.drawRect(R(i * 130 - 20 + (j % 2) * 65, 1000 + j * 90, 126, 86), P("#6E7E98"))
                    c.drawLine(i * 130 + (j % 2) * 65, 1010 + j * 90, i * 130 + 60 + (j % 2) * 65, 1050 + j * 90,
                               P("#C7D2E4", 0.5, stroke=3))
            c.drawRect(R(120, 380, 300, 360), P("#2A3346"))                 # a door and a calendar on the wall
            c.drawRect(R(120, 380, 300, 360), P("#7A4E2E", stroke=12))
            c.drawRect(R(640, 420, 160, 200), P("#AEB8C8", 0.8))
            c.drawRect(R(640, 420, 160, 40), P("#DC2626", 0.9))
            kx = lerp(160, 420, prog(t, T["t2"] - 0.6, T["t2"] + 1.2))
            person(c, kx, 1130, 190, "#F59E0B", t, pose="walk", face=1, hat="none", hair="#1C1917")
            for k in range(3):                                              # brr: cold lines at the feet
                q = (t * 2 + k / 3.0) % 1.0
                c.drawLine(kx - 40 + k * 30, 1140, kx - 40 + k * 30, 1140 - 30 * q, P("#3B82F6", 0.8 * (1 - q), stroke=4))
            mk = prog(t, T["thermo"] - 0.3, T["thermo"])
            mom(c, 780, 1150, 300, t, a=max(0.0, mk))
            if mk > 0:                                                      # a slipper in her hand
                u = 300 / 140.0
                c.save()
                c.translate(780 + 70 * u, 1150 - 110 * u)
                c.rotate(-25 + math.sin(t * 9) * 8)
                c.drawRRect(rr(-14 * u, -34 * u, 28 * u, 60 * u, 12 * u), P("#2563EB", mk))
                c.drawRect(R(-14 * u, -16 * u, 28 * u, 8 * u), P("#1E3A8A", mk))
                c.restore()

    def ui_tag(self, c, t, tw):
        T = self.T
        if self.rtl:
            k = self.span(T["t3"], self.duration + 1)
            if k > 0:
                kk = e_back(clamp(k))
                c.save()
                c.translate(720, 640)
                c.scale(kk, kk)
                lab = self.L["mom"]
                wdt = arabic.width_ar(lab, 48 * 1.15, "Tajawal-Black") + 70
                c.drawRRect(rr(-wdt / 2, -64, wdt, 116, 50), P("#F8FAFC"))
                c.drawRRect(rr(-wdt / 2, -64, wdt, 116, 50), P("#1F2937", stroke=4))
                tp = skia.Path()
                tp.moveTo(20, 50)
                tp.lineTo(60, 50)
                tp.lineTo(70, 110)
                tp.close()
                c.drawPath(tp, P("#F8FAFC"))
                word(c, lab, 0, 14, 48, "#111827")
                c.restore()

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=WINTER, horizon_y=H * 0.62)
        v2.stars(c, W, H, t, 0.7)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.5, T["house"]), 61), -18), (T["fire"], sfx.sizzle(0.8, 62), -14),
              (T["rice"], sfx.pop(63), -10), (T["heats"], sfx.whoosh(0.6, False, 64), -12),
              (T["floor"], sfx.sparkle(0.7, 9, 65), -10), (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 66), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 67), -8), (T["korean"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 68), -4), (s("break1"), sfx.hiss(3.0, 69), -12),
               (T["fifteen"], sfx.tick(), -8), (T["firewood"], sfx.thud(0.3, 70), -10), (T["precious"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 71), -4), (T["kitchen"], sfx.sizzle(0.6, 72), -12),
               (T["double"], sfx.pop(73), -8), (T["smoke"], sfx.whoosh(0.8, False, 74), -12),
               (T["leaves"] + 0.1, sfx.ding(), -8), (T["leaves"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 75), -4), (T["rush"], sfx.whoosh(0.5, True, 76), -10),
               (T["strip"], sfx.sizzle(0.5, 77), -12), (T["cold"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 78), -4), (T["rows"], sfx.whirr(0.7, 160.0, 240.0, 79), -14),
               (T["spread"], sfx.whoosh(0.6, False, 80), -12)]
        for k in range(6):
            ev.append((T["flat0"] + k * 0.18, sfx.thud(0.2, 81 + k), -14))
        ev += [(T["flat"] + 0.3, sfx.ding(), -8), (T["flat"] + 0.5, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 87), -4), (T["burns"], sfx.power_down(0.9, 88), -12),
               (T["hours"], sfx.tick(), -10), (T["night"], sfx.tick(), -10), (T["long"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 89), -4), (T["clay"], sfx.thud(0.4, 90), -8),
               (T["soaks"], sfx.charge_up(0.8), -12), (T["morning"], sfx.ding(), -8), (T["morning"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 91), -4), (T["dusty"], sfx.hiss(0.8, 92), -12),
               (T["sit"], sfx.thud(0.3, 93), -10), (T["sleep"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 94), -4), (T["glue"], sfx.tap(95), -10),
               (T["paper"], sfx.tap(96), -10), (T["shiny"], sfx.sparkle(0.7, 10, 97), -10),
               (T["wipe"], sfx.whoosh(0.4, False, 98), -14), (T["wipe"] + 0.2, sfx.ding(), -8), (T["wipe"] + 0.4, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(99), 0), (T["follow"] - 0.15, sfx.pop(100), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 101), -6), (T["grandma"], sfx.pop(102), -8),
               (T["tuck"], sfx.pop(103), -8), (T["hot"], sfx.chime(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 104), -6), (T["every"], sfx.pop(105), -4),
               (T["frank"], sfx.whoosh(0.8, True, 106), -10), (T["america"], sfx.pop(107), -4)]
        ev += [(s("closer") - 0.12, sfx.whoosh(0.45, False, 108), -6), (T["cong2"], sfx.pop(109), -2),
               (T["cong2"], sfx.sparkle(1.0, 14, 110), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 111), -6), (T["t2"], sfx.pop(112), -8),
               (T["t3"], sfx.lock_click(113) if not self.rtl else sfx.thud(0.3, 113), -6)]
        return ev


NAME = "ondol"
EPISODE = Ondol
