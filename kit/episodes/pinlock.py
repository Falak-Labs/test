"""Episode 111 - A pin tumbler lock (giant wooden pin locks about 4,000 years ago; Linus Yale Sr. and Jr., 1840s-1860s).

Sets: door (hook: an x-ray of the lock in a front door showing five little pins on springs, out to the whole door; cta,
stat; closer: the working lock cut open in front of the door, its key turned and every gap on the shear line), cutaway
(break1: with no pins any key turns the plug; fix1: springs push pins down into the plug and it is stuck; break2: then
even your own key cannot turn it; fix2: each pin cut in two, your key lifts every cut to the plug's edge, click; break3:
the neighbour's key; fix3: pins of different lengths, the neighbour's key misses, thousands of keys), ancient (break4: a
giant wooden pin lock on an old door; fix4: shrunk to a small cylinder and a flat metal key), copy (reveal: the lock only
checks heights, so a copy works), tag (English: the spare key under the doormat; Arabic: searching for the key that is
in your pocket).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

BRASS = ("#C9A24A", "#A7802F", "#7A5A1E")
PLUGC = ("#D8B865", "#B8943F")
WOOD = ("#8B5A2B", "#6E4420", "#4E2F15")
SKIN = ("#E8B48A", "#C68E62", "#A8754E", "#8D5A3B")
OK_, BAD = "#4ADE80", "#F87171"

# the lock in section
HX0, HX1, HY0, HY1 = 140, 940, 540, 1010              # housing
SHEAR = 770                                            # the plug's top edge: the shear line
PY1 = 980                                              # the plug's bottom
PIN_X = (310, 440, 570, 700, 830)
PIN_W = 54
CH_TOP = 580                                           # top of the pin chambers
KEY_LEN = (92, 70, 110, 80, 100)                       # key pins of different lengths (your key)
NEIGH = (70, 104, 80, 110, 72)                         # the neighbour's key cuts
DRIVER = 78
BLADE_TOP, BLADE_BOT = 820, 945                        # the key blade (its ridges are at BLADE_TOP)
TIP_FINAL = 900


def blade_top_at(x, cuts, off):
    """y of the key blade's top edge at screen x when the key sits `off` px short of fully in."""
    xx = x + off
    y = BLADE_TOP
    for px, kl in zip(PIN_X, cuts):
        d = abs(xx - px)
        y = max(y, SHEAR + kl - d * 1.1)               # a V-notch whose bottom lifts that pin's gap to the shear line
    return min(y, SHEAR + max(cuts))


def key_shape(c, cuts, off, col=BRASS, a=1.0, bow=True):
    """The flat key in the keyway, its tip at TIP_FINAL - off."""
    if a <= 0:
        return
    tip = TIP_FINAL - off
    p = skia.Path()
    p.moveTo(60 - off, BLADE_BOT)
    xs = list(range(int(60 - off), int(tip) + 1, 6))
    for x in xs:
        p.lineTo(x, blade_top_at(x, cuts, off))
    p.lineTo(tip + 20, BLADE_TOP + 40)
    p.lineTo(tip, BLADE_BOT)
    p.close()
    c.drawPath(p, lin_paint(0, BLADE_TOP, 0, BLADE_BOT, [col[0], col[1]], a=a))
    c.drawPath(p, P(col[2], a, stroke=3))
    if bow:
        c.drawCircle(40 - off, (BLADE_TOP + BLADE_BOT) / 2, 70, P(col[1], a))
        c.drawCircle(40 - off, (BLADE_TOP + BLADE_BOT) / 2, 24, P("#0F172A", a))


def spring(c, x, y0, y1, a=1.0):
    n = 9
    pts = [(x + (14 if k % 2 else -14) * (0 < k < n), lerp(y0, y1, k / n)) for k in range(n + 1)]
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, P("#CBD5E1", a, stroke=5))


def lock_section(c, t, pins=1.0, cut=1.0, cuts=None, off=None, key_col=BRASS, turn=0.0, blocked=0.0, shear_glow=0.0,
                 lens=False, show_key=True, screwdriver=None, wrong=0.0, lengths=KEY_LEN):
    """The lock cut open. pins 0..1 drops the pins in; cut 0 solid pins, 1 cut in two; cuts: the key in the keyway
    (None: no key); off: how far it is from fully in; turn 0..1 rotates the plug (shown by its stripes)."""
    if not lens:
        vrect(c, 0, 0, W, H, ["#111827", "#1E293B"])
    c.drawRRect(rr(HX0, HY0, HX1 - HX0, HY1 - HY0, 40), lin_paint(0, HY0, 0, HY1, [BRASS[1], BRASS[2]]))
    c.drawRRect(rr(HX0 + 18, SHEAR - 6, HX1 - HX0 - 36, PY1 - SHEAR + 12, 30), P("#3A2A10"))       # the gap round the plug
    # the plug, with stripes that slide when it turns
    pl = rr(HX0 + 24, SHEAR, HX1 - HX0 - 48, PY1 - SHEAR, 26)
    c.drawRRect(pl, lin_paint(0, SHEAR, 0, PY1, [PLUGC[0], PLUGC[1]]))
    c.save()
    c.clipRRect(pl, skia.ClipOp.kIntersect, True)
    for k in range(-1, 9):
        y = SHEAR + ((k * 34 + turn * 220) % 300)
        c.drawLine(HX0, y, HX1, y, P("#9C7A30", 0.35, stroke=6))
    c.drawRect(R(HX0 + 24, BLADE_TOP - 8, HX1 - HX0 - 48, BLADE_BOT - BLADE_TOP + 16), P("#2A1F0C", 0.8))   # the keyway
    c.restore()
    # the pin chambers
    for i, px in enumerate(PIN_X):
        c.drawRect(R(px - PIN_W / 2 - 4, CH_TOP, PIN_W + 8, BLADE_TOP - CH_TOP), P("#2A1F0C", 0.9))
    # the key (or a screwdriver)
    off_v = 0.0 if off is None else off
    if cuts is not None and show_key:
        key_shape(c, cuts, off_v, key_col)
    if screwdriver is not None:
        tip = TIP_FINAL - screwdriver
        c.drawRect(R(tip - 700, BLADE_TOP + 30, 700, 40), P("#94A3B8"))
        c.drawRRect(rr(tip - 900, BLADE_TOP + 10, 220, 80, 30), P("#EF4444"))
    # the pin stacks
    for i, px in enumerate(PIN_X):
        kl = lengths[i]
        if cuts is not None:
            bottom = blade_top_at(px, cuts, off_v)
        else:
            bottom = BLADE_TOP + 8
        drop = (1 - e_out(clamp(pins))) * 320
        kp_top = bottom - kl - drop
        dr_top = kp_top - DRIVER
        a = clamp(pins * 3)
        if a <= 0:
            continue
        spring(c, px, CH_TOP + 4, dr_top, a)
        if cut < 0.5:                                  # one solid pin
            c.drawRRect(rr(px - PIN_W / 2, dr_top, PIN_W, kl + DRIVER, 12), lin_paint(px - PIN_W / 2, 0, px + PIN_W / 2, 0,
                                                                                    ["#6B7484", "#A3ACB9", "#6B7484"], a=a))
        else:
            c.drawRRect(rr(px - PIN_W / 2, dr_top, PIN_W, DRIVER - 3, 10), lin_paint(px - PIN_W / 2, 0, px + PIN_W / 2, 0,
                                                                                  ["#5A6577", "#9AA6B6", "#5A6577"], a=a))
            c.drawRRect(rr(px - PIN_W / 2, kp_top + 3, PIN_W, kl - 3, 10), lin_paint(px - PIN_W / 2, 0, px + PIN_W / 2, 0,
                                                                                    [BRASS[2], BRASS[0], BRASS[2]], a=a))
            gap = kp_top
            if shear_glow > 0 and abs(gap - SHEAR) < 3:
                add_glow(c, px, SHEAR, 40, OK_, 0.9 * shear_glow)
            if wrong > 0 and abs(gap - SHEAR) >= 6:
                c.drawCircle(px, SHEAR, 22, P(BAD, 0.9 * wrong, stroke=6))
    # the shear line
    dashed(c, HX0 + 24, SHEAR, HX1 - 24, SHEAR, OK_ if shear_glow > 0 else "#F8FAFC", 4, 18, 12, t * 40, 0.6 + 0.4 * shear_glow)
    if blocked > 0:
        add_glow(c, 540, SHEAR, 420, BAD, 0.35 * blocked)


def end_view(c, x, y, r, turn=0.0, stuck=0.0, t=0.0, a=1.0):
    """The lock's face: the plug with its keyway, turning (turn 0..1 = a quarter turn) or rattling when stuck."""
    if a <= 0:
        return
    c.drawCircle(x, y, r + 16, P("#0F172A", 0.92 * a))
    c.drawCircle(x, y, r, lin_paint(x - r, 0, x + r, 0, [BRASS[1], BRASS[0]], a=a))
    c.drawCircle(x, y, r * 0.72, P(PLUGC[0], a))
    ang = turn * 90 + math.sin(t * 40) * 6 * stuck
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawRRect(rr(-8, -r * 0.55, 16, r * 1.1, 6), P("#2A1F0C", a))
    c.restore()
    if stuck > 0:
        c.drawCircle(x, y, r + 8, P(BAD, stuck * a, stroke=8))
    if turn > 0.95:
        c.drawCircle(x, y, r + 8, P(OK_, a, stroke=8))


# ====================================================================================== the door
def door_scene(c, t, dusk=0.0, xray=0.0, mat_lift=0.0, glow_key=0.0):
    vrect(c, 0, 0, W, H, [mix("#5B6B8C", "#1E2246", dusk), mix("#8E9BB5", "#3A2F5C", dusk)])
    for k in range(10):                                # siding boards
        c.drawLine(0, 380 + k * 90, W, 380 + k * 90, P("#3E4A66", 0.4, stroke=3))
    c.drawRRect(rr(300, 330, 480, 860, 20), P("#2B1A10"))                       # the door frame
    c.drawRRect(rr(320, 350, 440, 830, 14), lin_paint(320, 0, 760, 0, [WOOD[1], WOOD[0], WOOD[1]]))
    for (x, y, w, h) in ((360, 400, 160, 300), (560, 400, 160, 300), (360, 760, 160, 360), (560, 760, 160, 360)):
        c.drawRRect(rr(x, y, w, h, 10), P(WOOD[2], 0.45))
    c.drawCircle(700, 790, 26, lin_paint(674, 0, 726, 0, [BRASS[1], BRASS[0]]))    # the knob
    c.drawCircle(700, 700, 22, lin_paint(678, 0, 722, 0, [BRASS[1], BRASS[0]]))    # the lock
    c.drawRRect(rr(696, 688, 8, 24, 3), P("#2A1F0C"))
    if dusk > 0:
        add_glow(c, 860, 420, 160, "#FFD98A", 0.6 * dusk)
        c.drawRRect(rr(836, 380, 48, 70, 10), P("#FFE9B0", dusk))
    c.drawRect(R(0, 1180, W, 70), P("#4B4F57"))
    mat_y = 1170 - 120 * mat_lift
    if glow_key > 0:
        add_glow(c, 540, 1185, 90, "#FFE29A", 0.8 * glow_key)
        c.save()
        c.translate(540, 1188)
        c.scale(0.35, 0.35)
        c.translate(-500, -880)
        key_shape(c, KEY_LEN, 0, bow=True)
        c.restore()
    c.save()
    c.translate(540, 1185)
    c.rotate(-20 * mat_lift)
    c.drawRRect(rr(-190, -16 - (1185 - mat_y) * 0.2, 380, 34, 8), P("#7C4A1F"))
    for j in range(5):
        c.drawLine(-150 + j * 75, -10 - (1185 - mat_y) * 0.2, -150 + j * 75, 12 - (1185 - mat_y) * 0.2, P("#E8C79A", 0.5, stroke=4))
    c.restore()
    c.drawCircle(220, 1110, 60, P("#2F6B3A"))                                   # a potted plant
    c.drawRRect(rr(180, 1110, 80, 70, 10), P("#9A4B2A"))
    if xray > 0:                                       # an x-ray lens over the lock
        c.save()
        cp = skia.Path()
        cp.addCircle(700, 700, 230 * xray)
        c.clipPath(cp, skia.ClipOp.kIntersect, True)
        c.drawRect(R(0, 0, W, H), P("#0B1220", 0.94))
        c.translate(700, 700)
        c.scale(0.4, 0.4)
        c.translate(-540, -775)
        lock_section(c, t, pins=1.0, cut=1.0, lens=True)
        c.restore()
        c.drawCircle(700, 700, 230 * xray, P("#7DD3FC", xray, stroke=8))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E2230", "#0B0E18"]))


# ====================================================================================== the ancient lock
def ancient(c, t, shrink=0.0):
    vrect(c, 0, 0, W, H, ["#3B2A1A", "#6B4A2B", "#2A1C10"], [0.0, 0.6, 1.0])
    c.drawRect(R(0, 1140, W, 110), P("#5A4330"))
    k = e_io(clamp(shrink))
    a_old = 1 - k
    if a_old > 0:
        c.save()
        c.saveLayerAlpha(None, int(255 * a_old))
        c.drawRect(R(560, 300, 420, 840), lin_paint(560, 0, 980, 0, [WOOD[1], WOOD[0]]))     # an old wooden door
        for j in range(5):
            c.drawLine(560 + j * 84, 300, 560 + j * 84, 1140, P(WOOD[2], 0.6, stroke=4))
        c.drawRect(R(330, 640, 560, 80), lin_paint(0, 640, 0, 720, [WOOD[0], WOOD[1]]))     # the long wooden bolt
        c.drawRect(R(600, 520, 240, 320), lin_paint(0, 520, 0, 840, ["#9C6B38", WOOD[1]]))   # the lock box
        for j in range(4):                             # wooden pins dropping into the bolt
            c.drawRect(R(630 + j * 52, 560, 26, 110), P("#C49A6C"))
        # a giant wooden key, as long as an arm
        c.save()
        c.translate(250 + math.sin(t * 2) * 6, 900)
        c.rotate(-8)
        c.drawRect(R(0, -16, 330, 32), P("#B07A45"))
        for j in range(4):
            c.drawRect(R(290 - j * 26, -60, 14, 44), P("#B07A45"))
        c.restore()
        person(c, 190, 1150, 300, "#2563EB", t, pose="shrug", face=1, skin=SKIN[1], hair="#141414")
        c.restore()
        c.restore()
    if k > 0:                                          # the modern lock and its flat key
        c.save()
        c.translate(540, 720)
        s = lerp(1.6, 1.0, k)
        c.scale(s, s)
        c.drawCircle(-150, 0, 120, lin_paint(-270, 0, -30, 0, [BRASS[1], BRASS[0]], a=k))
        c.drawCircle(-150, 0, 86, P(PLUGC[0], k))
        c.drawRRect(rr(-158, -60, 16, 120, 6), P("#2A1F0C", k))
        c.save()
        c.translate(90, 0)
        c.scale(0.55, 0.55)
        c.translate(-500, -880)
        key_shape(c, KEY_LEN, 0, a=k)
        c.restore()
        c.restore()
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E140E", "#0B0E18"]))


# ====================================================================================== tags
def search_tag(c, t, panic=0.0, reveal=0.0):
    vrect(c, 0, 0, W, H, ["#2B3448", "#3D4760"])
    c.drawRect(R(0, 1000, W, 250), P("#5B5146"))
    c.drawRRect(rr(80, 520, 300, 200, 14), P("#7C5A3A"))                   # a cupboard with drawers flung open
    for j in range(3):
        c.drawRRect(rr(96, 540 + j * 60, 268, 46, 8), P("#946B45"))
    for k in range(7):                                 # stuff flying out
        u = (t * 0.9 + k / 7) % 1.0
        x = 230 + math.cos(k * 2.3) * 260 * u
        y = 600 - 300 * u + 420 * u * u
        c.drawRRect(rr(x - 18, y - 12, 36, 24, 6), P(["#F59E0B", "#3B82F6", "#EF4444", "#22C55E", "#A855F7", "#F8FAFC", "#EC4899"][k], 0.9 * panic))
    person(c, 640 + math.sin(t * 7) * 30 * panic, 1180, 440, "#0EA5E9", t, pose="shrug", face=-1, skin=SKIN[2], hair="#141414")
    if reveal > 0:                                     # the key, in the pocket all along
        add_glow(c, 600, 1000, 70, "#FFE29A", 0.9 * reveal)
        c.save()
        c.translate(600, 1000)
        c.scale(0.22, 0.22)
        c.translate(-500, -880)
        key_shape(c, KEY_LEN, 0, a=reveal)
        c.restore()


class PinLock(EpisodeV2):
    BUILD_NO = 111
    FIRST_SET = "door"
    CLEAR = "#0B0E18"
    COVER_T = ("closer", 0.55)
    TITLE = {"en": "PIN TUMBLER LOCK", "ar_sa": "قفل الدبابيس"}
    EMPH = {"en": ["FRONT", "DOOR", "GUARDED", "FIVE", "LITTLE", "PINS", "ANY", "KEY", "TURN", "KNOW", "SPRING", "PUSHES",
                   "PLUG", "STUCK", "OWN", "COULDN'T", "CUT", "TWO", "LIFTS", "EDGE", "CLICK", "NEIGHBOR'S", "SAME",
                   "DIFFERENT", "LENGTHS", "THOUSANDS", "KEYS", "FIRST", "GIANT", "BLOCKS", "WOOD", "EIGHTEEN", "SIXTIES",
                   "FATHER", "SON", "SHRANK", "FLAT", "METAL", "FOLLOW", "SYDNEY", "COATHANGER", "DOESN'T", "HEIGHTS",
                   "COPY", "WORKS", "FOUR", "THOUSAND", "YEARS", "CONGRATS", "YOURSELF", "TINY", "SPARE", "DOORMAT"],
            "ar_sa": ["باب", "بيتكم", "يحرسه", "خمس", "دبابيس", "صغيرة", "مفتاح", "يفتحه", "يعرف", "زنبركات", "قلب",
                      "يلف", "مفتاحك", "مقصوص", "نصين", "يرفع", "لحافة", "طق", "جارك", "أطوال", "مختلفة", "آلاف",
                      "خشب", "ضخمة", "مية", "وخمسين", "أب", "وولده", "صغروه", "مسطح", "متابعة", "سيدني", "الشماعة",
                      "يعرف", "الأطوال", "نسخة", "تفتحه", "عمرها", "أربعة", "مبروك", "تحرس", "تدور", "جيبك"]}
    KEYS = {"ar_sa": {
        ("hook", "DOOR"): "باب", ("hook", "GUARDED"): "يحرسه", ("hook", "FIVE"): "خمس", ("hook", "PINS"): "دبابيس",
        ("break1", "WITHOUT"): "بدونها", ("break1", "ANY"): "أي", ("break1", "KNOW"): "يعرف",
        ("fix1", "SPRING"): "زنبركات", ("fix1", "PLUG"): "قلب", ("fix1", "STUCK"): "يلف",
        ("break2", "OWN"): "حتى", ("break2", "TURN"): "يلفه",
        ("fix2", "CUT"): "مقصوص", ("fix2", "LIFTS"): "يرفع", ("fix2", "EDGE"): "لحافة", ("fix2", "CLICK"): "طق",
        ("break3", "NEIGHBOR"): "جارك", ("break3", "SAME"): "نفس",
        ("fix3", "DIFFERENT"): "أطوال", ("fix3", "THOUSANDS"): "آلاف",
        ("break4", "FIRST"): "أول", ("break4", "WOOD"): "خشب",
        ("fix4", "EIGHTEEN"): "مية", ("fix4", "FATHER"): "وولده", ("fix4", "FLAT"): "مسطح",
        ("cta", "FOLLOW"): "متابعة", ("cta", "COATHANGER"): "الشماعة",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "DOESN'T"): "يعرف", ("reveal", "HEIGHTS"): "الأطوال",
        ("reveal", "COPY"): "نسخة",
        ("stat", "FIVE"): "خمس", ("stat", "THOUSANDS"): "آلاف", ("stat", "FOUR"): "أربعة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "TINY"): "دبابيس", ("tag", "SPARE"): "تدور", ("tag", "DOORMAT"): "جيبك"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Sydney's Coathanger"),
                   "stat": [("5", "PINS"), ("1000s", "OF KEYS"), ("4,000", "YEARS OLD")],
                   "L": {"five": "5 LITTLE PINS", "any": "ANY KEY TURNS IT", "know": "HOW DOES IT KNOW YOUR KEY?",
                         "spring": "SPRINGS PUSH PINS DOWN", "stuck": "STUCK!", "own": "YOUR KEY TOO!",
                         "cut": "EACH PIN CUT IN TWO", "click": "CLICK! IT TURNS", "neigh": "YOUR NEIGHBOR'S KEY?",
                         "lengths": "DIFFERENT LENGTHS", "thousands": "THOUSANDS OF KEYS", "wood": "GIANT BLOCKS OF WOOD!",
                         "small": "1860s: A FLAT METAL KEY", "doesnt": "IT ONLY CHECKS HEIGHTS", "copy": "ANY COPY WORKS",
                         "name": "THE PIN TUMBLER LOCK", "guard": "5 PINS ON GUARD", "mat": "THE SPARE KEY..."}},
            "ar_sa": {"follow": ("تابعني", "الجاي: جسر الشمّاعة"),
                      "stat": [("5", "دبابيس"), ("1000+", "مفتاح مختلف"), ("4000", "سنة")],
                      "L": {"five": "خمس دبابيس صغيرة", "any": "أي مفتاح يفتحه", "know": "كيف يعرف مفتاحك؟",
                            "spring": "زنبركات تدز الدبابيس", "stuck": "ما يلف!", "own": "حتى مفتاحك!",
                            "cut": "كل دبوس نصين", "click": "طق! يلف", "neigh": "مفتاح جارك؟",
                            "lengths": "أطوال مختلفة", "thousands": "آلاف المفاتيح", "wood": "قطع خشب ضخمة!",
                            "small": "مفتاح حديد مسطّح", "doesnt": "يشيك على الأطوال بس", "copy": "أي نسخة تفتحه",
                            "name": "قفل الدبابيس", "guard": "خمس دبابيس تحرسك", "mat": "وهو في جيبك!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "door": ("hook", "DOOR", 0.25), "guarded": ("hook", "GUARDED", 0.45), "five": ("hook", "FIVE", 0.75),
            "pins": ("hook", "PINS", 0.95),
            "without": ("break1", "WITHOUT", 0.05), "any": ("break1", "ANY", 0.25), "know": ("break1", "KNOW", 0.8),
            "spring": ("fix1", "SPRING", 0.15), "plug": ("fix1", "PLUG", 0.6), "stuck": ("fix1", "STUCK", 0.95),
            "own": ("break2", "OWN", 0.4), "turn2": ("break2", "TURN", 0.85),
            "cut": ("fix2", "CUT", 0.2), "lifts": ("fix2", "LIFTS", 0.5), "edge": ("fix2", "EDGE", 0.8), "click": ("fix2", "CLICK", 0.95),
            "neighbor": ("break3", "NEIGHBOR", 0.4), "same": ("break3", "SAME", 0.9),
            "different": ("fix3", "DIFFERENT", 0.35), "thousands": ("fix3", "THOUSANDS", 0.75),
            "first": ("break4", "FIRST", 0.3), "wood": ("break4", "WOOD", 0.95),
            "eighteen": ("fix4", "EIGHTEEN", 0.2), "father": ("fix4", "FATHER", 0.5), "flat": ("fix4", "FLAT", 0.85),
            "follow": ("cta", "FOLLOW", 0.1), "coathanger": ("cta", "COATHANGER", 0.9),
            "answer": ("reveal", "ANSWER", 0.05), "doesnt": ("reveal", "DOESN'T", 0.2), "heights": ("reveal", "HEIGHTS", 0.55),
            "copy": ("reveal", "COPY", 0.8),
            "s1": ("stat", "FIVE", 0.05), "s2": ("stat", "THOUSANDS", 0.35), "s3": ("stat", "FOUR", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_tiny": ("tag", "TINY", 0.1), "t_spare": ("tag", "SPARE", 0.6), "t_mat": ("tag", "DOORMAT", 0.9)})
        T["any1"] = max(T["any"], s("break1") + 0.3)
        T["stuck1"] = max(T["stuck"], T["spring"] + 0.4)
        T["own1"] = max(T["own"], s("break2") + 0.3)
        T["click1"] = max(T["click"], T["lifts"] + 0.6)
        T["neigh1"] = max(T["neighbor"], s("break3") + 0.2)
        T["thou1"] = max(T["thousands"], T["different"] + 0.4)
        T["wood1"] = max(T["wood"], s("break4") + 0.3)
        T["flat1"] = max(T["flat"], T["father"] + 0.4)
        # ---- sets
        self.cut(s("break1") - 0.12, "cutaway", 1)
        self.cut(s("break4") - 0.12, "ancient", -1)
        self.cut(s("cta") - 0.12, "door", 1)
        self.cut(s("reveal") - 0.12, "copy", -1)
        self.cut(s("stat") - 0.12, "door", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["any1"], T["stuck1"]), (T["own1"], T["click1"]), (T["neigh1"], T["thou1"]), (T["wood1"], T["flat1"])]
        self.shakes = [(T["pins"], 0.3, 4), (T["any1"], 0.3, 5), (T["stuck1"], 0.4, 7), (T["own1"], 0.3, 6), (T["click1"], 0.25, 4),
                       (T["neigh1"], 0.3, 5), (T["wood1"], 0.4, 7), (T["copy"], 0.3, 5), (s("closer") + 0.2, 0.35, 6),
                       (T["t_mat"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: door (hook, cta, stat, closer)
    def draw_door(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            k = e_io(prog(t, T["five"] - 0.6, s("break1") - 0.25))
            z = lerp(2.6, 1.0, k)
            fx, fy = lerp(700, 540, k), lerp(700, 760, k)
            c.save()
            c.translate(540, 720)
            c.scale(z, z)
            c.translate(-fx, -fy)
            door_scene(c, t, xray=1.0)
            c.restore()
            c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E2230", "#0B0E18"]))
        elif ph == "closer":
            door_scene(c, t, dusk=1.0, xray=0.0)
            c.drawRect(R(0, 0, W, 1250), P("#0B0E18", 0.55))
            c.save()
            c.translate(540, 760)
            c.scale(0.92, 0.92)
            c.translate(-540, -775)
            k = prog(t, s("closer") + 0.1, s("closer") + 0.9)
            lock_section(c, t, pins=1.0, cut=1.0, cuts=KEY_LEN, off=0.0, turn=k, shear_glow=1.0, lens=True)
            c.restore()
            end_view(c, 860, 470, 70, turn=k, t=t)
        else:
            door_scene(c, t, dusk=0.0 if ph == "stat" else 0.3, xray=0.0 if ph == "cta" else 0.8)

    def ui_door(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "five", T["five"] - 0.3, s("break1") + 0.1, accent=HILITE, size=60)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=54)

    # ------------------------------------------------------------------ set: cutaway (break1 .. fix3)
    def draw_cutaway(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        ev = dict(turn=0.0, stuck=0.0)
        if ph == "break1":
            sd = lerp(820, 0, e_out(prog(t, s("break1"), T["any"] + 0.3)))
            tr = prog(t, T["any1"], T["any1"] + 0.6)
            lock_section(c, t, pins=0.0, screwdriver=sd, turn=tr)
            ev = dict(turn=tr)
        elif ph == "fix1":
            pins = prog(t, T["spring"] - 0.3, T["spring"] + 0.4)
            lock_section(c, t, pins=pins, cut=0.0, blocked=prog(t, T["stuck"] - 0.3, T["stuck"] + 0.2))
            ev = dict(stuck=prog(t, T["plug"], T["stuck1"]))
        elif ph == "break2":
            off = lerp(820, 0, e_out(prog(t, s("break2"), T["own"] + 0.3)))
            lock_section(c, t, cut=0.0, cuts=KEY_LEN, off=off, blocked=prog(t, T["own1"], T["own1"] + 0.3))
            ev = dict(stuck=prog(t, T["own1"], T["own1"] + 0.3))
        elif ph == "fix2":
            cut = prog(t, T["cut"] - 0.2, T["cut"] + 0.2)
            off = lerp(820, 0, e_io(prog(t, T["cut"] + 0.1, T["edge"])))
            glow = prog(t, T["edge"], T["click1"])
            tr = prog(t, T["click1"] - 0.1, T["click1"] + 0.5)
            lock_section(c, t, cut=cut, cuts=KEY_LEN, off=off, shear_glow=glow, turn=tr)
            ev = dict(turn=tr)
        elif ph == "break3":
            off = lerp(820, 0, e_out(prog(t, s("break3"), T["neighbor"] + 0.4)))
            lock_section(c, t, cuts=NEIGH, off=off, key_col=("#98A3B3", "#788395", "#465264"),
                         wrong=prog(t, T["same"] - 0.3, T["same"]))
        else:
            lock_section(c, t, cuts=NEIGH, off=0.0, key_col=("#98A3B3", "#788395", "#465264"), wrong=1.0,
                         blocked=prog(t, T["different"], T["different"] + 0.4))
            ev = dict(stuck=prog(t, T["different"], T["different"] + 0.3))
            k = prog(t, T["thousands"] - 0.3, T["thousands"] + 0.4)
            if k > 0:                                  # a fan of different keys
                for j in range(9):
                    c.save()
                    c.translate(540, 1180)
                    c.rotate(-60 + j * 15)
                    c.translate(0, -420 * e_back(k))
                    c.scale(0.18, 0.18)
                    c.translate(-500, -880)
                    cuts = tuple(70 + ((j * 7 + q * 13) % 5) * 10 for q in range(5))
                    key_shape(c, cuts, 0, col=[BRASS, ("#98A3B3", "#788395", "#465264"), ("#F59E0B", "#B45309", "#78350F")][j % 3],
                              a=k)
                    c.restore()
        end_view(c, 900, 1120, 70, t=t, **ev)
        c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E2230", "#0B0E18"]))

    def ui_cutaway(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "any", T["any"] - 0.2, T["know"] - 0.3, accent=WARN, size=58)
            self.chip(540, 300, "know", T["know"] - 0.3, s("fix1") - 0.1, accent=HILITE, size=48)
            self.badge("alert", T["any1"], s("fix1") - 0.2, x=160, y=470)
            self.red(T["any1"], 1.2)
        elif ph == "fix1":
            self.chip(540, 300, "spring", T["spring"] - 0.2, T["stuck"] - 0.2, accent="#CBD5E1", size=52)
            self.chip(540, 300, "stuck", T["stuck"] - 0.2, s("break2") - 0.15, accent=GOOD, size=64)
            self.badge("check", T["stuck1"], s("break2") - 0.15, x=160, y=470)
        elif ph == "break2":
            self.chip(540, 300, "own", T["own"] - 0.2, s("fix2") - 0.15, accent=WARN, size=62)
            self.badge("alert", T["own1"], s("fix2") - 0.2, x=160, y=470)
            self.red(T["own1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "cut", T["cut"] - 0.2, T["edge"] - 0.1, accent="#CBD5E1", size=56)
            self.chip(540, 300, "click", T["edge"] - 0.1, s("break3") - 0.15, accent=GOOD, size=62)
            self.badge("check", T["click1"], s("break3") - 0.15, x=160, y=470)
        elif ph == "break3":
            self.chip(540, 300, "neigh", T["neighbor"] - 0.2, s("fix3") - 0.15, accent=WARN, size=54)
            self.badge("alert", T["neigh1"], s("fix3") - 0.2, x=160, y=470)
            self.red(T["neigh1"], 1.2)
        else:
            self.chip(540, 300, "lengths", T["different"] - 0.2, T["thousands"] - 0.2, accent="#CBD5E1", size=56)
            self.chip(540, 300, "thousands", T["thousands"] - 0.2, s("break4") - 0.15, accent=GOOD, size=58)
            self.badge("check", T["thou1"], s("break4") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: ancient (break4, fix4)
    def draw_ancient(self, c, t):
        T, s = self.T, self.tl.s
        ancient(c, t, shrink=prog(t, T["eighteen"] - 0.2, T["flat"]))

    def ui_ancient(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "wood", T["first"] - 0.2, s("fix4") - 0.15, accent=WARN, size=56)
            self.badge("alert", T["wood1"], s("fix4") - 0.2, x=160, y=470)
            self.red(T["wood1"], 1.2)
        else:
            self.chip(540, 300, "small", T["eighteen"] - 0.2, s("cta") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["flat1"], s("cta") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: copy (reveal)
    def draw_copy(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#111827", "#1E293B"])
        k = prog(t, T["heights"] - 0.3, T["heights"] + 0.4)
        for j, (y, col) in enumerate(((560, BRASS), (860, ("#94A3B8", "#64748B", "#334155")))):
            c.save()
            c.translate(560, y)
            c.scale(0.9, 0.9)
            c.translate(-500, -880)
            key_shape(c, KEY_LEN, 0, col=col, a=prog(t, s("reveal") + j * 0.3, s("reveal") + j * 0.3 + 0.3))
            c.restore()
        for i, (px, kl) in enumerate(zip(PIN_X, KEY_LEN)):     # the same heights, measured on both keys
            x = 560 + (px - 500) * 0.9
            for y in (560, 860):
                yy = y + (SHEAR + kl - 880) * 0.9
                c.drawLine(x, yy, x, yy - 120 * k, P(OK_, k, stroke=6))
                c.drawCircle(x, yy - 120 * k, 9, P(OK_, k))
        cp = prog(t, T["copy"] - 0.2, T["copy"] + 0.3)
        if cp > 0:
            v2.badge(c, 880, 1080, cp, "check", t, 1.2)
        c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E2230", "#0B0E18"]))

    def ui_copy(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "doesnt", T["doesnt"] - 0.2, T["copy"] - 0.2, accent=HILITE, size=54)
        self.chip(540, 300, "copy", T["copy"] - 0.2, s("stat") - 0.15, accent=GOOD, size=60)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:
            door_scene(c, t, dusk=0.4, xray=0.0, mat_lift=prog(t, T["t_spare"], T["t_mat"] + 0.2),
                       glow_key=prog(t, T["t_mat"] - 0.2, T["t_mat"] + 0.2))
        else:
            search_tag(c, t, panic=prog(t, T["t_tiny"], T["t_spare"]), reveal=prog(t, T["t_mat"] - 0.3, T["t_mat"] + 0.1))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "guard", T["t_tiny"] - 0.2, T["t_spare"] - 0.2, accent=HILITE, size=56)
        self.chip(540, 300, "mat", T["t_spare"] - 0.2, self.duration + 1, accent=WARN, size=62)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#111827", "#1F2937"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, sfx.hum(3.0, 80.0), -20), (T["five"], sfx.tick(), -6),
              (T["pins"], sfx.ding(), -8)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 63), -6), (T["any"], sfx.clank(420.0, 0.5, 64), -10),
               (T["any1"] + 0.2, sfx.creak(0.6, 65), -10), (T["any1"] + 0.3, sfx.alarm(3, 820.0), -14)]
        ev += [(T["spring"], sfx.clank(600.0, 0.4, 66), -10), (T["stuck1"], sfx.thunk(67), -6), (T["stuck1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["own"], sfx.clank(500.0, 0.5, 68), -10), (T["own1"] + 0.2, sfx.thunk(69), -8), (T["own1"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(T["cut"], sfx.snap(70), -10), (T["lifts"], sfx.clank(700.0, 0.4, 71), -12), (T["click1"], sfx.click(72), -2),
               (T["click1"] + 0.15, sfx.ding(), -8), (T["click1"] + 0.3, sfx.chime(), -6)]
        ev += [(T["neighbor"], sfx.clank(450.0, 0.5, 73), -10), (T["neigh1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["different"], sfx.thunk(74), -8), (T["thou1"], sfx.sparkle(1.0, 12, 75), -8), (T["thou1"], sfx.ding(), -8),
               (T["thou1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, False, 76), -6), (T["wood1"], sfx.thud(0.5, 77), -6),
               (T["wood1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["eighteen"], sfx.whoosh(0.8, True, 78), -10), (T["flat1"], sfx.ding(), -8), (T["flat1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["heights"], sfx.tick(), -6), (T["copy"], sfx.click(95), -4),
               (T["copy"] + 0.15, sfx.ding(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (s("closer") + 0.5, sfx.click(103), -4),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 104), -6), (T["t_spare"], sfx.creak(0.6, 105), -10),
               (T["t_mat"], sfx.womp(), -8)]
        return ev


NAME = "pinlock"
EPISODE = PinLock
