"""Episode 54 - The Eiffel Tower.  v2 look: Paris at golden hour and at night, the tower drawn as real iron lace.

Sets: paris (hook: the tower rises out of Paris in two years, 300 m; reveal: painters on ropes, three shades lighter
towards the top; stat; closer at night with the lights sparkling), wind (break1: a solid tower catches the wind like a
sail and rocks; fix1: open lace lets the wind through and the curved legs carry the push to the ground), ground (break2:
a leg by the river sinks into soft wet mud; fix2: an iron box full of pumped-in air sinks while workers dig inside it,
dry, down to firm ground), legs (break3: two legs leaning in miss each other at 57 m; fix3: a hydraulic jack in the foot
nudges the leg a millimetre at a time until the beams line up), rivets (break4: pieces shaking loose in the wind; fix4:
red-hot rivets hammered in, cooling and clamping), tag (the tourists' pinch photo; AR: and the aunt says Cairo Tower is
nicer).
World (paris): side view, the ground at y = 0, 1 m = 2.4 units (the tower about 720 units tall).
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow, sun  # noqa: E402
from burjalarab import path_of, sea_band  # noqa: E402
from phone import bubble, mom  # noqa: E402

GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#2A2A60", "horizon": "#4A3A7A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
U = 2.4                                                   # world units per metre
IRON = ("#5A3F30", "#6E5040", "#86664E")                  # the three shades, bottom to top
LIT = "#FFB347"


def w_out(h):
    """Half width of the tower's outline at height h (m)."""
    return 62.5 * math.exp(-h / 75.0) + 3.0


def w_in(h):
    """Half width of the gap between the legs at height h (m); 0 once they meet."""
    if h <= 57:
        return 36.0 * (1 - 0.55 * h / 57.0)
    return max(0.0, 16.2 * (1 - (h - 57) / 58.0))


def shade_at(h, k3=1.0):
    """Paint colour at height h: three shades, lighter towards the top (k3 = 0 gives one flat colour)."""
    if k3 <= 0:
        return IRON[1]
    i = 0 if h < 100 else 1 if h < 200 else 2
    return mix(IRON[1], IRON[i], k3)


def eiffel(c, x, y, s, t, build=1.0, solid=0.0, lit=0.0, k3=1.0, sparkle=0.0, a=1.0, sway=0.0, paint=1.0):
    """The tower standing on (x, y), side view.  build 0..1 raises it from the ground; solid 0..1 fills the lace (the
    'solid tower' of break1); lit 0..1 the night lighting; paint 0..1 how far up the fresh paint has gone."""
    if a <= 0 or build <= 0:
        return
    top = 300.0 * build
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if sway:
        c.rotate(sway)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))

    def P_(h, side, inner=False):
        return (side * (w_in(h) if inner else w_out(h)) * U, -h * U)

    def col(h):
        base = shade_at(h, k3) if h <= paint * 312 else mix(IRON[1], "#4A3A30", 0.4)
        return mix(base, LIT, 0.55 * lit)

    # the legs, from the ground to where they meet (115 m)
    for side in (-1, 1):
        hs = [k * 115.0 / 24 for k in range(25) if k * 115.0 / 24 <= top]
        if len(hs) < 2:
            hs = [0.0, min(top, 4.0)]
        pts = [P_(h, side) for h in hs] + [P_(h, side, True) for h in reversed(hs)]
        c.drawPath(path_of(pts, close=True), P(col(min(top, 60)), 0.35 + 0.65 * solid))
        for j in range(len(hs) - 1):                                   # lattice: crossing diagonals in each panel
            h0, h1 = hs[j], hs[j + 1]
            o0, o1, i0, i1 = P_(h0, side), P_(h1, side), P_(h0, side, True), P_(h1, side, True)
            cc = col(h0)
            c.drawLine(o0[0], o0[1], i1[0], i1[1], P(cc, 1.0, stroke=3.2))
            c.drawLine(i0[0], i0[1], o1[0], o1[1], P(cc, 1.0, stroke=3.2))
            c.drawLine(o0[0], o0[1], i0[0], i0[1], P(cc, 0.9, stroke=2.4))
        c.drawPath(path_of([P_(h, side) for h in hs]), P(col(30), 1.0, stroke=7))
        c.drawPath(path_of([P_(h, side, True) for h in hs if w_in(h) > 0.5]), P(col(30), 1.0, stroke=5))
    if top > 40:                                                       # the big arch between the legs
        ar = skia.Path()
        ar.moveTo(-w_in(2) * U, -2 * U)
        ar.cubicTo(-w_in(2) * U, -34 * U, -12 * U, -40 * U, 0, -40 * U)
        ar.cubicTo(12 * U, -40 * U, w_in(2) * U, -34 * U, w_in(2) * U, -2 * U)
        c.drawPath(ar, P(col(20), 1.0, stroke=6))
        c.drawPath(ar, P(col(20), 0.5, stroke=14))
    if top > 115:                                                      # the shaft above the second platform
        hs = [115 + k * (min(top, 276) - 115) / 20.0 for k in range(21)]
        pts = [P_(h, -1) for h in hs] + [P_(h, 1) for h in reversed(hs)]
        c.drawPath(path_of(pts, close=True), P(col(200), 0.35 + 0.65 * solid))
        for j in range(len(hs) - 1):
            h0, h1 = hs[j], hs[j + 1]
            l0, l1, r0, r1 = P_(h0, -1), P_(h1, -1), P_(h0, 1), P_(h1, 1)
            cc = col(h0)
            c.drawLine(l0[0], l0[1], r1[0], r1[1], P(cc, 1.0, stroke=2.6))
            c.drawLine(r0[0], r0[1], l1[0], l1[1], P(cc, 1.0, stroke=2.6))
            c.drawLine(0, l0[1], 0, l1[1], P(cc, 0.8, stroke=2.0))
        for side in (-1, 1):
            c.drawPath(path_of([P_(h, side) for h in hs]), P(col(200), 1.0, stroke=6))
    if top > 276:                                                      # the top and the antenna
        tp = path_of([(-w_out(276) * U, -276 * U), (-2.2 * U, -300 * U), (2.2 * U, -300 * U), (w_out(276) * U, -276 * U)], close=True)
        c.drawPath(tp, P(col(290)))
        c.drawLine(0, -300 * U, 0, -min(top + 12, 312) * U, P(col(300), 1.0, stroke=4))
    for hp, wd, th in ((57, 3.5, 6.0), (115, 2.5, 4.5), (276, 2.0, 3.5)):   # the three platforms
        if top >= hp:
            ww = (w_out(hp) + wd) * U
            c.drawRect(R(-ww, -hp * U - th * U * 0.5, 2 * ww, th * U), P(mix(col(hp), "#2A1E18", 0.25)))
            c.drawRect(R(-ww, -hp * U - th * U * 0.5, 2 * ww, 3), P(mix(col(hp), "#F8E8C8", 0.3)))
            if lit > 0:
                for k in range(int(2 * ww / 14)):
                    add_glow(c, -ww + 7 + k * 14, -hp * U, 6, "#FFE08A", 0.6 * lit)
    if lit > 0:
        add_glow(c, 0, -150 * U, 300 * U * 0.5, LIT, 0.22 * lit)
        add_glow(c, 0, -312 * U, 30, "#FFF1C9", 0.8 * lit)
    if sparkle > 0:                                                    # the hourly sparkle
        rng = random.Random(int(t * 12))
        for _ in range(60):
            h = rng.uniform(0, min(top, 300))
            xx = rng.uniform(-w_out(h), w_out(h)) * U
            if abs(xx) < w_in(h) * U:
                continue
            add_glow(c, xx, -h * U, rng.uniform(4, 9), "#FFFFFF", sparkle * rng.uniform(0.5, 1.0))
    if a < 1:
        c.restore()
    c.restore()


def rooftops(c, x0, x1, y, t, lit=0.0, a=1.0, seed=3):
    """Paris rooftops (world space): cream stone buildings with blue-grey zinc roofs and chimneys."""
    rng = random.Random(seed)
    x = x0
    while x < x1:
        w_ = rng.uniform(70, 130)
        h_ = rng.uniform(60, 90)
        c.drawRect(R(x, y - h_, w_, h_), P(mix("#A8977C", "#3A3550", lit * 0.6), a))
        roof = path_of([(x - 4, y - h_), (x + 10, y - h_ - 34), (x + w_ - 10, y - h_ - 34), (x + w_ + 4, y - h_)], close=True)
        c.drawPath(roof, P(mix("#5A6478", "#2A2E48", lit * 0.6), a))
        for k in range(int(w_ / 26)):
            c.drawRect(R(x + 8 + k * 26, y - h_ + 14, 12, 18), P("#FFD58A" if lit > 0.3 and rng.random() < 0.6 else "#3A4258", a))
        c.drawRect(R(x + w_ * 0.7, y - h_ - 46, 10, 16), P("#8A6A5A", a))
        x += w_ + rng.uniform(0, 8)


def worker(c, x, y, h, t, pose="carry", a=1.0, shirt="#1E3A8A"):
    person(c, x, y, h, shirt, t, pose=pose, face=1, hat="cap", a=a)


def hammer(c, x, y, s, ang, a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawRect(R(-4 * s, 0, 8 * s, 80 * s), P("#8A5A30", a))
    c.drawRRect(rr(-22 * s, -14 * s, 44 * s, 22 * s, 4 * s), P("#4B5563", a))
    c.restore()


def jack(c, x, y, s, ext, a=1.0):
    """Hydraulic jack under a leg's foot (screen/world), piston out by ext 0..1."""
    c.drawRRect(rr(x - 40 * s, y - 70 * s, 80 * s, 70 * s, 8 * s), P("#B91C1C", a))
    c.drawRect(R(x - 18 * s, y - 70 * s - 40 * s * ext, 36 * s, 40 * s * ext + 2), P("#D1D5DB", a))
    c.drawRect(R(x - 46 * s, y - 8 * s, 92 * s, 10 * s), P("#374151", a))


# ====================================================================================== the episode
class Eiffel(EpisodeV2):
    BUILD_NO = 54
    FIRST_SET = "paris"
    CLEAR = "#0B1A3A"
    TITLE = {"en": "EIFFEL TOWER", "ar_sa": "برج إيفل"}
    EMPH = {"en": ["CONGRATS", "RAISE", "THREE", "HUNDRED", "METERS", "IRON", "PARIS", "TWO", "YEARS", "EIFFEL", "TOWER",
                   "YOURSELF", "WIND", "BRUTAL", "SOLID", "SAIL", "OPEN", "LACE", "BLOWS", "CURVED", "LEGS", "PUSH",
                   "RIVER", "SOFT", "WET", "GROUND", "SINK", "BOXES", "PUMPED-IN", "AIR", "DIG", "DRY", "FIRM", "LEAN",
                   "FOUR", "MEET", "FIFTY-SEVEN", "HYDRAULIC", "JACKS", "NUDGE", "MILLIMETER", "LINE", "EIGHTEEN",
                   "THOUSAND", "PIECES", "HOLD", "HALF", "MILLION", "RED-HOT", "RIVETS", "COOL", "SHRINK", "CLAMP",
                   "TIGHT", "FOLLOW", "SUEZ", "CANAL", "PAINT", "HAND", "SIXTY", "TONNES", "SHADES", "LIGHTER", "TOP",
                   "TWENTY", "FIFTEEN", "CENTIMETERS", "SUMMER", "MELTED", "SIX", "THICK", "MONSTER", "PHOTO",
                   "PINCHING", "FINGERS"],
            "ar_sa": ["مبروك", "ترفع", "تلتميت", "متر", "حديد", "باريس", "سنتين", "برج", "إيفل", "بإيدك", "الهوا", "جامد",
                      "المقفول", "الشراع", "مخرّم", "الدانتيلا", "المقوّسة", "للأرض", "النهر", "طرية", "ومبلولة", "صناديق",
                      "مضغوط", "يحفروا", "ناشف", "الجامدة", "مايلة", "يتقابلوا", "وخمسين", "جاك", "هيدروليك", "مللي",
                      "تمنتاشر", "ألف", "حتة", "ماسكة", "بمليونين", "ونص", "برشام", "نار", "يتقلص", "ويقفل", "تابعني",
                      "قناة", "السويس", "ادهنه", "ستين", "طن", "بوية", "لفوق", "واحد", "عشرين", "خمستاشر", "سانتي",
                      "سيّحته", "ستة", "وحش", "بتتصور", "عمتك", "القاهرة", "أحلى"]}
    KEYS = {"ar_sa": {
        ("hook", "RAISE"): "ترفع", ("hook", "THREE"): "تلتميت", ("hook", "IRON"): "حديد", ("hook", "PARIS"): "باريس",
        ("hook", "TWO"): "سنتين", ("hook", "CONGRATS"): "مبروك", ("hook", "EIFFEL"): "إيفل",
        ("break1", "WIND"): "الهوا", ("break1", "BRUTAL"): "جامد", ("break1", "SOLID"): "المقفول", ("break1", "SAIL"): "الشراع",
        ("fix1", "LACE"): "مخرّم", ("fix1", "BLOWS"): "يعدّي", ("fix1", "CURVED"): "المقوّسة", ("fix1", "PUSH"): "زقّته",
        ("fix1", "DOWN"): "للأرض",
        ("break2", "LEGS"): "رجلين", ("break2", "RIVER"): "النهر", ("break2", "SOFT"): "طرية", ("break2", "WET"): "ومبلولة",
        ("fix2", "SINK"): "فتنزّل", ("fix2", "BOXES"): "صناديق", ("fix2", "AIR"): "مضغوط", ("fix2", "DIG"): "يحفروا",
        ("fix2", "DRY"): "ناشف", ("fix2", "FIRM"): "الجامدة",
        ("break3", "LEAN"): "مايلة", ("break3", "FOUR"): "الأربعة", ("break3", "MEET"): "يتقابلوا", ("break3", "FIFTY-SEVEN"): "وخمسين",
        ("fix3", "HYDRAULIC"): "هيدروليك", ("fix3", "JACKS"): "جاك", ("fix3", "NUDGE"): "يزقّها", ("fix3", "MILLIMETER"): "مللي",
        ("fix3", "LINE"): "مللي",
        ("break4", "EIGHTEEN"): "تمنتاشر", ("break4", "PIECES"): "حتة", ("break4", "HOLD"): "ماسكة",
        ("fix4", "JOIN"): "فتربطهم", ("fix4", "MILLION"): "بمليونين", ("fix4", "RED-HOT"): "نار", ("fix4", "COOL"): "يبرد",
        ("fix4", "SHRINK"): "يتقلص", ("fix4", "CLAMP"): "ويقفل",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PAINT"): "ادهنه", ("reveal", "SIXTY"): "ستين", ("reveal", "SHADES"): "بوية", ("reveal", "LIGHTER"): "تفتّح",
        ("reveal", "EVEN"): "واحد",
        ("stat", "TWENTY"): "عشرين", ("stat", "FIFTEEN"): "خمستاشر", ("stat", "MELTED"): "سيّحته",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "ARTISTS"): "فنانين", ("tag", "MONSTER"): "وحش", ("tag", "PHOTO"): "بتتصور", ("tag", "PINCHING"): "عمتك"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Suez Canal"),
                   "stat": [("20 yrs", "MEANT TO LAST"), ("+15 cm", "IN SUMMER"), ("6 cm", "MELTED DOWN")],
                   "L": {"tall": "300 m OF IRON", "years": "IN 2 YEARS", "name": "THE EIFFEL TOWER",
                         "wind": "BRUTAL WIND UP THERE", "sail": "A SOLID TOWER = A SAIL", "lace": "OPEN IRON LACE",
                         "legs": "CURVED LEGS CARRY THE PUSH", "river": "BY THE RIVER", "soft": "SOFT, WET GROUND",
                         "box": "IRON BOX FULL OF AIR", "dry": "DIGGING IN THE DRY", "firm": "FIRM GROUND",
                         "meet": "THEY MUST MEET AT 57 m", "miss": "MISSED!", "jack": "HYDRAULIC JACK",
                         "mm": "1 mm AT A TIME", "pieces": "18,000 PIECES", "loose": "SHAKING LOOSE",
                         "rivets": "2,500,000 RIVETS", "clamp": "COOL, SHRINK, CLAMP", "paint": "60 TONNES OF PAINT",
                         "shades": "3 SHADES: LIGHTER AT THE TOP", "monster": "\"A USELESS MONSTER\"",
                         "pinch": "THE PINCH PHOTO"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: قناة السويس"),
                      "stat": [("20", "سنة وكان يتشال"), ("+15", "سانتي في الصيف"), ("6", "سانتي لو سيّحته")],
                      "L": {"tall": "تلتميت متر حديد", "years": "في سنتين", "name": "برج إيفل",
                            "wind": "الهوا فوق جامد", "sail": "البرج المقفول = شراع", "lace": "حديد مخرّم زي الدانتيلا",
                            "legs": "الرجلين المقوّسة توصّل الزقة للأرض", "river": "جنب النهر", "soft": "أرض طرية ومبلولة",
                            "box": "صناديق حديد فيها هوا مضغوط", "dry": "بيحفروا وهي ناشفة", "firm": "الأرض الجامدة",
                            "meet": "لازم يتقابلوا بالظبط", "miss": "مش راكبين!", "jack": "جاك هيدروليك",
                            "mm": "مللي مللي", "pieces": "تمنتاشر ألف حتة", "loose": "بتتهز وتفك",
                            "rivets": "مليونين ونص مسمار برشام", "clamp": "يبرد ويتقلص ويقفل", "paint": "ستين طن بوية",
                            "shades": "تفتّح لفوق", "monster": "قالوا عليه وحش", "pinch": "الصورة إياها",
                            "bubble": "برج القاهرة أحلى!"}}}
    COVER_T = ("closer", 0.6)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "raise": ("hook", "RAISE", 0.1), "three": ("hook", "THREE", 0.2), "iron": ("hook", "IRON", 0.35),
            "paris": ("hook", "PARIS", 0.45), "two": ("hook", "TWO", 0.55), "congrats": ("hook", "CONGRATS", 0.68),
            "eiffel": ("hook", "EIFFEL", 0.9),
            "wind": ("break1", "WIND", 0.25), "brutal": ("break1", "BRUTAL", 0.4), "solid": ("break1", "SOLID", 0.6),
            "sail": ("break1", "SAIL", 0.92),
            "lace": ("fix1", "LACE", 0.25), "blows": ("fix1", "BLOWS", 0.45), "curved": ("fix1", "CURVED", 0.65),
            "push": ("fix1", "PUSH", 0.85), "down": ("fix1", "DOWN", 0.95),
            "legs2": ("break2", "LEGS", 0.15), "river": ("break2", "RIVER", 0.4), "soft": ("break2", "SOFT", 0.7),
            "wet": ("break2", "WET", 0.85),
            "sink": ("fix2", "SINK", 0.05), "boxes": ("fix2", "BOXES", 0.15), "air": ("fix2", "AIR", 0.35),
            "dig": ("fix2", "DIG", 0.6), "dry": ("fix2", "DRY", 0.75), "firm": ("fix2", "FIRM", 0.92),
            "lean": ("break3", "LEAN", 0.2), "four": ("break3", "FOUR", 0.45), "meet": ("break3", "MEET", 0.6),
            "f57": ("break3", "FIFTY-SEVEN", 0.85),
            "hyd": ("fix3", "HYDRAULIC", 0.1), "jacks": ("fix3", "JACKS", 0.15), "nudge": ("fix3", "NUDGE", 0.4),
            "mm": ("fix3", "MILLIMETER", 0.65), "line": ("fix3", "LINE", 0.92),
            "eighteen": ("break4", "EIGHTEEN", 0.1), "pieces": ("break4", "PIECES", 0.35), "hold": ("break4", "HOLD", 0.6),
            "join": ("fix4", "JOIN", 0.05), "million": ("fix4", "MILLION", 0.3), "redhot": ("fix4", "RED-HOT", 0.45),
            "cool": ("fix4", "COOL", 0.65), "shrink": ("fix4", "SHRINK", 0.8), "clamp": ("fix4", "CLAMP", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "paint": ("reveal", "PAINT", 0.08), "sixty": ("reveal", "SIXTY", 0.3), "shades": ("reveal", "SHADES", 0.5),
            "lighter": ("reveal", "LIGHTER", 0.65), "even": ("reveal", "EVEN", 0.95),
            "s1": ("stat", "TWENTY", 0.1), "s2": ("stat", "FIFTEEN", 0.4), "s3": ("stat", "MELTED", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_art": ("tag", "ARTISTS", 0.05), "t_mon": ("tag", "MONSTER", 0.3), "t_photo": ("tag", "PHOTO", 0.6),
            "t_pinch": ("tag", "PINCHING", 0.85)})
        T["sail1"] = max(T["sail"], T["solid"]) + 0.1
        T["wet1"] = max(T["wet"], T["soft"]) + 0.1
        T["meet1"] = max(T["f57"], T["meet"]) + 0.1
        T["hold1"] = max(T["hold"], T["pieces"]) + 0.1
        T["firm1"] = max(T["firm"], T["dry"], T["dig"]) + 0.1
        T["line1"] = max(T["line"], T["mm"]) + 0.2
        T["clamp1"] = max(T["clamp"], T["shrink"], T["cool"]) + 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "wind", 1)
        self.cut(s("break2") - 0.12, "ground", -1)
        self.cut(s("break3") - 0.12, "legs", 1)
        self.cut(s("break4") - 0.12, "rivets", -1)
        self.cut(s("reveal") - 0.12, "paris", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- paris camera
        cm = Camera(0, -280, 1.0)
        cm.key(0.1, 0, -278, 1.01, max(1.0, T["two"]))
        cm.key(T["congrats"], 0, -264, 1.06, 1.6)
        cm.key(s("reveal") - 0.12, 0, -470, 1.5, 0.0).key(T["lighter"] - 0.3, 0, -290, 0.98, 1.4)
        cm.key(s("stat") - 0.12, 0, -275, 0.8, 0.0).key(s("stat"), 0, -278, 0.81, max(0.5, s("closer") - s("stat") - 0.2))
        cm.key(s("closer") - 0.1, 0, -264, 1.06, 1.0).key(s("closer") + 0.9, 0, -255, 1.1, 3.0)
        self.cam = cm
        self.spans = [(T["sail1"], T["down"] + 0.3), (T["wet1"], T["firm1"] + 0.3), (T["meet1"], T["line1"] + 0.3),
                      (T["hold1"], T["clamp1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["brutal"], 0.6, 8), (T["sail1"], 0.4, 8), (T["wet1"], 0.4, 7),
                       (T["meet1"], 0.3, 6), (T["hold1"], 0.5, 8), (s("closer") + 0.2, 0.35, 9), (T["t_pinch"], 0.25, 6)]

    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    # ------------------------------------------------------------------ set: paris (hook, reveal, stat, closer)
    def draw_paris(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        night = prog(t, s("closer") - 0.6, s("closer") + 0.6)
        hook = t < s("break1")
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy - 40 * z)
        if night > 0:
            c.save()
            c.saveLayerAlpha(None, int(255 * night))
            v2.sky(c, W, H, 0.0, pal=NIGHTP, horizon_y=gy - 40 * z)
            v2.stars(c, W, H, t, 0.8)
            c.restore()
            c.restore()
        if night < 1:
            sun(c, 850 - cx * 0.05, gy - 600 * z, 54, heat=0.5, a=1 - night)
        for i, (px, py, s_) in enumerate(((220, 980, 1.0), (820, 1160, 0.8), (520, 1380, 0.7))):
            v2.cloud(c, (px + t * (6 + i * 3)) % (W + 600) - 300, gy - py * z, s_, body=mix("#7A6A9A", "#1A1E48", night),
                     rim=mix("#FFB37A", "#3A3A78", night), a=0.75, seed=i)
        self.view(c, cam)
        c.save()                                                       # far rooftops, scaled down
        c.translate(0, -6)
        c.scale(0.55, 0.55)
        rooftops(c, -2600, 2600, 0, t, lit=night, a=0.8, seed=5)
        c.restore()
        if hook:
            build = e_io(prog(t, 0.1, T["two"] + 0.4))
            paint = 1.0
        else:
            build = 1.0
            paint = prog(t, T["paint"] - 0.2, T["lighter"] + 0.6) if t < s("stat") - 0.12 else 1.0
        k3 = 1.0 if (hook or t >= s("stat") - 0.12) else prog(t, T["shades"] - 0.2, T["lighter"] + 0.4)
        spk = prog(t, T["cong2"], T["cong2"] + 0.3) * (1 - prog(t, s("tag") - 0.6, s("tag")))
        eiffel(c, 0, 0, 1.0, t, build=build, lit=night, k3=k3, sparkle=spk * night, paint=paint)
        if hook and build < 1:                                         # scaffolding cranes at the growing top
            ht = 300 * build * U
            for sd in (-1, 1):
                cxp = sd * w_out(300 * build) * U
                c.drawLine(cxp, -ht, cxp + sd * 60, -ht - 40, P("#F59E0B", stroke=5))
                c.drawLine(cxp + sd * 60, -ht - 40, cxp + sd * 60, -ht + 10, P("#1F2937", stroke=2))
        if not hook and s("reveal") - 0.12 <= t < s("stat") - 0.12:   # painters on ropes
            pk = prog(t, T["paint"] - 0.2, T["paint"] + 0.3)
            for k, (hh, sd) in enumerate(((70, -1), (140, 1), (210, -1), (95, 1))):
                h_ = hh + 10 * math.sin(t * 0.8 + k)
                px_ = sd * (w_out(h_) * U + 18)
                c.drawLine(px_, -h_ * U - 60, px_, -h_ * U, P("#E5E7EB", pk, stroke=2))
                person(c, px_, -h_ * U + 26, 24, ("#F8FAFC", "#FDE68A", "#93C5FD", "#FCA5A5")[k], t + k, pose="point",
                       face=-sd, hat="cap", a=pk)
        rooftops(c, -1500, -260, 0, t, lit=night, seed=9)               # near rooftops either side
        rooftops(c, 260, 1500, 0, t, lit=night, seed=11)
        c.drawRect(R(-1600, 0, 3200, 60), P(mix("#5A6A4A", "#1A2030", night)))   # the Champ de Mars
        c.drawRect(R(-1600, 60, 3200, 900), P(mix("#3A3A48", "#14162A", night)))
        if hook:
            rk = prog(t, T["three"] - 0.2, T["three"] + 0.3)               # the height ruler
            if rk > 0:
                rx = 260
                c.drawLine(rx, 0, rx, -300 * U * rk, P(HILITE, rk, stroke=5))
                for k in range(7):
                    if k * 50 <= 300 * rk:
                        c.drawLine(rx - 12, -k * 50 * U, rx + 12, -k * 50 * U, P(HILITE, rk, stroke=4))
        c.restore()
        self.ui["cam"] = cam

    def ui_paris(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "tall", T["three"] - 0.1, T["two"] - 0.15, accent=HILITE, size=44)
            self.chip(540, 300, "years", T["two"] - 0.15, T["congrats"] - 0.05, accent="#FDBA74", size=44)
            self.chip(540, 300, "name", T["eiffel"] - 0.2, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            self.chip(540, 300, "paint", T["paint"] - 0.1, T["shades"] - 0.2, accent="#D6A77A", size=44)
            self.chip(540, 300, "shades", T["shades"] - 0.2, s("stat") - 0.15, accent=HILITE, size=38)

    # ------------------------------------------------------------------ set: wind (break1, fix1)
    def draw_wind(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1180)
        for i in range(5):
            v2.cloud(c, (t * 260 + i * 330) % (W + 600) - 300, 380 + i * 140, 0.8, body="#6A5A8A", rim="#FFB37A", a=0.6, seed=i)
        cam = (0, -280, 1.0)
        self.view(c, cam)
        rooftops(c, -1500, 1500, 0, t, seed=9)
        c.drawRect(R(-1600, 0, 3200, 900), P("#3A3A48"))
        wk = prog(t, T["wind"] - 0.3, T["wind"])
        if not fixed:
            sol = prog(t, T["solid"] - 0.4, T["solid"])
            rock = math.sin(t * 5) * 3.5 * prog(t, T["solid"], T["sail1"]) + 2.5 * prog(t, T["solid"], T["sail1"])
            eiffel(c, 0, 0, 1.0, t, solid=sol, k3=0.0, sway=rock)
            if sol > 0:                                                # stone grey when it is solid
                c.save()
                c.rotate(rock)
                pts = [(-w_out(h) * U, -h * U) for h in range(0, 301, 10)] + [(w_out(h) * U, -h * U) for h in range(300, -1, -10)]
                c.drawPath(path_of(pts, close=True), P("#7A7268", sol))
                c.restore()
        else:
            eiffel(c, 0, 0, 1.0, t, k3=0.0)
            ck = prog(t, T["curved"] - 0.3, T["curved"] + 0.2)
            if ck > 0:                                                 # the curved legs carry the push down
                for sd in (-1, 1):
                    pts = [(sd * w_out(h) * U, -h * U) for h in range(0, 281, 10)]
                    c.drawPath(path_of(pts), P(HILITE, ck, stroke=10))
                    for j in range(4):
                        q = (t * 0.7 + j / 4.0) % 1.0
                        h_ = lerp(260, 10, q)
                        x_ = sd * w_out(h_) * U
                        arrow(c, x_ + sd * 6, -h_ * U - 24, x_ + sd * 10, -h_ * U + 24, HILITE, a=ck * math.sin(q * math.pi), w=8, head=20)
        for k in range(9):                                             # the wind
            q = (t * 0.9 + k / 9.0) % 1.0
            yy = -60 - k * 76
            x0_ = lerp(-700, 700, q)
            if not fixed:
                xe = min(x0_ + 160, -w_out(-yy / U) * U - 8)
                if xe > x0_:
                    arrow(c, x0_, yy, xe, yy, "#E0F2FE", a=wk * 0.85 * math.sin(q * math.pi), w=10, head=24)
                else:
                    v2.puff(c, -w_out(-yy / U) * U - 20, yy, 24, "#E0F2FE", 0.4 * wk, k=1)
            else:
                arrow(c, x0_, yy, x0_ + 160, yy, "#E0F2FE", a=wk * 0.85 * math.sin(q * math.pi), w=10, head=24)
        c.restore()

    def ui_wind(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "wind", T["wind"] - 0.2, T["solid"] - 0.2, accent="#BAE6FD", size=44)
            self.chip(540, 300, "sail", T["solid"] - 0.2, s("fix1") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["sail1"], s("fix1") - 0.2, x=920, y=420)
            self.red(T["sail1"], 1.2)
            return
        self.chip(540, 300, "lace", T["lace"] - 0.2, T["curved"] - 0.3, accent="#D6A77A", size=46)
        self.chip(540, 300, "legs", T["curved"] - 0.3, s("break2") - 0.15, accent=HILITE, size=38)
        self.badge("check", T["down"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: ground (break2, fix2), section
    def draw_ground(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=500)
        gy, firm = 560, 1190
        c.drawRect(R(0, gy, W, firm - gy), lin_paint(0, gy, 0, firm, ["#6A4E34", "#4A3626"]))   # soft wet mud
        rng = random.Random(3)
        for _ in range(70):
            c.drawCircle(rng.uniform(0, W), rng.uniform(gy + 20, firm - 10), rng.uniform(4, 9), P("#5A9AC0", 0.35))
        c.drawRect(R(0, firm, W, H - firm), lin_paint(0, firm, 0, H, ["#6B6F7A", "#4A4E58"]))  # firm ground
        for k in range(30):
            c.drawCircle((k * 71) % W, firm + 30 + (k * 37) % 400, 10, P("#8A8F9A", 0.6))
        c.drawRect(R(0, gy - 8, 430, 12), P("#7A8A5A"))
        sea_band(c, -40, 300, gy + 4, 160, t, col="#2A6A8A", dark="#1A4A6A")        # the river on the left
        if not fixed:
            sk = prog(t, T["soft"] - 0.3, T["wet1"] + 0.5)
            c.save()                                                   # a leg's foot sinking and tilting
            c.translate(700, gy + 160 * sk)
            c.rotate(-8 * sk)
            c.drawRect(R(-130, -40, 260, 60), P("#8A8578"))
            pts = [(-120, -40), (-60, -520), (40, -520), (120, -40)]
            c.drawPath(path_of(pts, close=True), P(IRON[1], 0.5))
            for k in range(8):
                y0_ = -40 - k * 60
                c.drawLine(lerp(-120, -60, k / 8.0), y0_, lerp(120, 40, (k + 1) / 8.0), y0_ - 60, P(IRON[1], stroke=5))
                c.drawLine(lerp(120, 40, k / 8.0), y0_, lerp(-120, -60, (k + 1) / 8.0), y0_ - 60, P(IRON[1], stroke=5))
            c.restore()
            if sk > 0:
                for k in range(6):
                    q = (t * 1.2 + k / 6.0) % 1.0
                    c.drawCircle(580 + k * 50, gy + 40 + q * 80, 6, P("#7DD3FC", 0.7 * sk * (1 - q)))
            return
        dk = e_io(prog(t, T["sink"] - 0.2, T["firm1"]))                  # the caisson sinking while they dig
        top_ = lerp(gy - 140, firm - 300, dk)
        bx, bw, bh = 470, 460, 300
        mud_top = top_ + bh
        c.drawRect(R(bx - 10, gy, bw + 20, max(0, top_ + bh - gy)), P("#3A2A1E", 0.6))   # the shaft dug so far
        c.drawRect(R(bx, top_, bw, bh), P("#4B5563"))                   # the iron box
        c.drawRect(R(bx + 14, top_ + 110, bw - 28, bh - 110), P("#BFE3F5", 0.55 * prog(t, T["air"] - 0.3, T["air"])))  # air chamber
        c.drawRect(R(bx, top_ + 96, bw, 16), P("#374151"))
        c.drawPath(path_of([(bx, top_ + bh), (bx + 26, top_ + bh), (bx + 10, top_ + bh + 30)], close=True), P("#374151"))
        c.drawPath(path_of([(bx + bw, top_ + bh), (bx + bw - 26, top_ + bh), (bx + bw - 10, top_ + bh + 30)], close=True), P("#374151"))
        c.drawLine(bx + bw * 0.7, gy - 220, bx + bw * 0.7, top_ + 110, P("#1F2937", stroke=10))          # the air hose
        box(c, bx + bw * 0.7 - 50, gy - 300, 100, 80, "#B45309", r=8)                                     # the pump
        ak = prog(t, T["air"] - 0.3, T["air"] + 0.2)
        for k in range(5):
            q = (t * 1.5 + k / 5.0) % 1.0
            c.drawCircle(bx + bw * 0.7, lerp(gy - 220, top_ + 110, q), 7, P("#E0F2FE", 0.9 * ak))
        dgk = prog(t, T["dig"] - 0.3, T["dig"])
        for k, px in enumerate((bx + 110, bx + 300)):                   # workers digging inside, dry
            worker(c, px, top_ + bh - 6, 150, t + k * 0.7, pose="carry", a=dgk, shirt=("#2563EB", "#DC2626")[k])
            ang = 30 + 25 * math.sin(t * 6 + k * 2)
            c.save()
            c.translate(px + 30, top_ + bh - 70)
            c.rotate(ang)
            c.drawLine(0, 0, 0, 70, P("#8A5A30", dgk, stroke=6))
            c.drawRect(R(-12, 64, 24, 20), P("#9CA3AF", dgk))
            c.restore()
        if dk >= 0.98:
            fk = prog(t, T["firm1"] - 0.1, T["firm1"] + 0.3)
            c.drawLine(bx - 40, firm, bx + bw + 40, firm, P(GOOD, fk, stroke=8))
        self.ui["mud"] = mud_top

    def ui_ground(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "river", T["river"] - 0.2, T["soft"] - 0.2, accent="#7DD3FC", size=44)
            self.chip(540, 300, "soft", T["soft"] - 0.2, s("fix2") - 0.15, accent="#D6A77A", size=44)
            self.badge("alert", T["wet1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["wet1"], 1.2)
            return
        self.chip(540, 300, "box", T["boxes"] - 0.15, T["dig"] - 0.2, accent="#BFE3F5", size=40)
        self.chip(540, 300, "dry", T["dig"] - 0.2, T["firm"] - 0.2, accent="#FDE68A", size=42)
        self.chip(540, 300, "firm", T["firm"] - 0.2, s("break3") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["firm1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: legs (break3, fix3), the first floor
    def draw_legs(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1250)
        cam = (0, -75, 3.2)
        self.view(c, cam)
        c.drawRect(R(-900, 0, 1800, 600), P("#4A4038"))
        off = 7.0 if not fixed else 7.0 * (1 - e_io(prog(t, T["nudge"] - 0.2, T["line1"])))
        for sd in (-1, 1):                                             # two legs leaning in, the right one too low
            dy = off * U if sd > 0 else 0.0
            c.save()
            c.translate(0, dy)
            hs = [k * 57.0 / 12 for k in range(13)]
            pts = [(sd * w_out(h) * U, -h * U) for h in hs] + [(sd * w_in(h) * U, -h * U) for h in reversed(hs)]
            c.drawPath(path_of(pts, close=True), P(IRON[0], 0.4))
            for j in range(12):
                h0, h1 = hs[j], hs[j + 1]
                c.drawLine(sd * w_out(h0) * U, -h0 * U, sd * w_in(h1) * U, -h1 * U, P(IRON[1], stroke=4))
                c.drawLine(sd * w_in(h0) * U, -h0 * U, sd * w_out(h1) * U, -h1 * U, P(IRON[1], stroke=4))
            c.drawPath(path_of([(sd * w_out(h) * U, -h * U) for h in hs]), P(IRON[1], stroke=8))
            c.drawPath(path_of([(sd * w_in(h) * U, -h * U) for h in hs]), P(IRON[1], stroke=6))
            bx0 = sd * w_in(57) * U                                    # a beam stub reaching for the middle
            c.drawRect(R(min(bx0, bx0 - sd * 40), -57 * U - 8, 40, 16), P("#3A2A20"))
            c.restore()
            fx_ = sd * (w_out(0) + w_in(0)) / 2 * U
            fw_ = (w_out(0) - w_in(0)) * U + 30
            c.drawRect(R(fx_ - fw_ / 2, -6, fw_, 14), P("#8A8578"))
        bk = prog(t, T["meet"] - 0.3, T["meet"]) if not fixed else 1.0
        c.drawRect(R(-w_in(57) * U + 30, -57 * U - 8 + (0 if fixed and off < 0.3 else -2), 2 * w_in(57) * U - 60, 16), P("#5A4030", bk))
        if not fixed:
            mk = prog(t, T["meet1"] - 0.2, T["meet1"] + 0.2)
            if mk > 0:
                c.drawLine(w_in(57) * U - 40, -57 * U, w_in(57) * U - 40, -57 * U + off * U, P(WARN, mk, stroke=6))
        jk = 1.0 if fixed else 0.0
        if jk > 0:
            jack(c, (w_out(0) + w_in(0)) / 2 * U, 4, 0.5, 1 - off / 7.0, a=jk)
            if off < 0.3:
                c.drawLine(-w_in(57) * U + 30, -57 * U - 14, w_in(57) * U - 30, -57 * U - 14, P(GOOD, prog(t, T["line1"] - 0.1, T["line1"] + 0.3), stroke=6))
        mk2 = prog(t, T["f57"] - 0.3, T["f57"])                         # the 57 m marker
        c.drawLine(-w_in(0) * U + 24, 0, -w_in(0) * U + 24, -57 * U, dash_paint(HILITE, mk2, w=2, t=t))
        c.restore()

    def ui_legs(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "meet", T["lean"] - 0.2, T["meet1"] - 0.1, accent=HILITE, size=42)
            self.chip(540, 300, "miss", T["meet1"] - 0.1, s("fix3") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["meet1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["meet1"], 1.2)
            return
        self.chip(540, 300, "jack", T["hyd"] - 0.2, T["mm"] - 0.2, accent="#FCA5A5", size=44)
        self.chip(540, 300, "mm", T["mm"] - 0.2, s("break4") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["line1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: rivets (break4, fix4), close-up of a joint
    def draw_rivets(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        vrect(c, 0, 0, W, H, ["#3E6AA8", "#E39A6A"])
        shakek = prog(t, T["pieces"] - 0.3, T["hold1"]) if not fixed else 0.0
        jig = math.sin(t * 30) * 10 * shakek
        c.save()                                                       # two girders crossing at a gusset plate
        c.translate(540, 900)
        c.rotate(-20)
        c.drawRect(R(-700, -70 + jig * 0.3, 1400, 140), P(IRON[1]))
        c.drawRect(R(-700, -70 + jig * 0.3, 1400, 18), P(IRON[2]))
        c.restore()
        c.save()
        c.translate(540, 900)
        c.rotate(55 + jig * 0.15)
        c.translate(jig, 0)
        c.drawRect(R(-700, -60, 1400, 120), P(IRON[0]))
        c.drawRect(R(-700, -60, 1400, 16), P(IRON[1]))
        c.restore()
        c.drawRRect(rr(380 + jig * 0.5, 740, 320, 320, 30), P(mix(IRON[1], "#2A1E18", 0.2)))   # the gusset plate
        holes = [(450 + i * 90, 810 + j * 90) for j in range(3) for i in range(3)]
        n_done = 0
        if fixed:
            n_done = int(9 * prog(t, T["redhot"] - 0.2, T["clamp1"]))
        for k, (hx, hy) in enumerate(holes):
            hx += jig * 0.5
            if k < n_done:
                age = (t - lerp(T["redhot"] - 0.2, T["clamp1"], k / 9.0))
                heat = clamp(1 - age / 1.6)
                c.drawCircle(hx, hy, 30, P(mix("#3A2A20", "#FF5A1F", heat)))
                c.drawCircle(hx - 8, hy - 8, 10, P(mix("#5A4030", "#FFD08A", heat), 0.8))
                if heat > 0:
                    add_glow(c, hx, hy, 60, "#FF7A1F", 0.5 * heat)
                ck = prog(t, T["clamp"] - 0.3, T["clamp"] + 0.3)
                if ck > 0 and k % 3 == 1:
                    for sd in (-1, 1):
                        arrow(c, hx + sd * 70, hy, hx + sd * 38, hy, GOOD, a=ck, w=6, head=16)
            else:
                c.drawCircle(hx, hy, 22, P("#1A1410"))
        if fixed:                                                      # the forge, the flying rivet and the hammer
            fk = prog(t, T["join"] - 0.3, T["join"])
            c.drawRRect(rr(80, 1380, 220, 120, 20), P("#374151", fk))
            for k in range(7):
                c.drawCircle(110 + k * 26, 1390, 14, P(mix("#FF5A1F", "#FFD08A", (k % 3) / 2.0), fk))
            add_glow(c, 190, 1390, 120, "#FF7A1F", 0.5 * fk)
            if n_done < 9:
                q = (t * 1.6) % 1.0
                tx_, ty_ = holes[min(8, n_done)]
                rx_, ry_ = lerp(190, tx_, q), lerp(1360, ty_, q) - math.sin(q * math.pi) * 300
                c.drawCircle(rx_, ry_, 16, P("#FF5A1F", fk))
                add_glow(c, rx_, ry_, 40, "#FF7A1F", 0.6 * fk)
                hammer(c, tx_ + 80, ty_ - 80, 1.4, -40 + 30 * math.sin(t * 14), a=fk)
        else:
            lk = prog(t, T["pieces"] - 0.2, T["pieces"] + 0.3)
            for k in range(6):                                         # loose bits flying off
                q = (t * 0.8 + k / 6.0) % 1.0
                c.drawRect(R(560 + k * 60 + q * 200, 760 + k * 40 + q * 300, 22, 22), P(IRON[0], lk * (1 - q)))

    def ui_rivets(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "pieces", T["eighteen"] - 0.2, T["hold"] - 0.2, accent="#D6A77A", size=46)
            self.chip(540, 300, "loose", T["hold"] - 0.2, s("fix4") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["hold1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["hold1"], 1.2)
            return
        self.chip(540, 300, "rivets", T["million"] - 0.2, T["cool"] - 0.2, accent="#FB923C", size=40)
        self.chip(540, 300, "clamp", T["cool"] - 0.2, s("cta") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["clamp1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1100)
        c.save()                                                       # the tower far away
        c.translate(640, 1100)
        c.scale(0.55, 0.55)
        eiffel(c, 0, 0, 1.0, t)
        c.restore()
        c.drawRect(R(0, 1100, W, H - 1100), P("#4A5A3A"))
        mk = prog(t, T["t_mon"] - 0.3, T["t_mon"] + 0.2) * (1 - prog(t, T["t_photo"] - 0.3, T["t_photo"]))
        if mk > 0:                                                     # the artists' angry protest letter
            c.drawRRect(rr(140, 420, 360, 440, 16), P("#F1E9D8", mk))
            for k in range(9):
                c.drawLine(180, 480 + k * 40, 460 - (k % 3) * 40, 480 + k * 40, P("#6B5A4A", mk, stroke=6))
            c.drawLine(180, 820, 300, 800, P("#1F2937", mk, stroke=5))
        pk = prog(t, T["t_photo"] - 0.3, T["t_photo"])                  # the tourist posing for the pinch photo
        person(c, 330, 1500, 520, "#E11D48", t, pose="point", face=1, hat="cap", a=pk)
        if pk > 0:
            hx, hy = 640 - 4, 1100 - 312 * U * 0.55 - 6                 # thumb and finger round the tip
            fk = prog(t, T["t_pinch"] - 0.3, T["t_pinch"])
            gap = lerp(60, 14, e_out(fk))
            c.save()
            c.translate(hx, hy)
            c.drawRRect(rr(-190, -70, 120, 150, 50), P("#E8B48A", pk))                  # the palm, lower left
            c.drawRRect(rr(-110, -gap - 26, 120, 30, 15), P("#E8B48A", pk))             # index finger
            c.drawRRect(rr(-10, -gap - 22, 18, 22, 8), P("#F5D0B5", pk))
            c.drawRRect(rr(-100, gap - 4, 106, 32, 16), P("#E0A878", pk))               # thumb
            c.drawRRect(rr(-12, gap, 16, 22, 8), P("#F5D0B5", pk))
            c.restore()
        if self.rtl:                                                   # the aunt is not impressed
            ak = prog(t, T["t_pinch"] - 0.3, T["t_pinch"])
            if ak > 0:
                mom(c, lerp(1200, 900, e_out(ak)), 1500, 380, t, a=1.0)
        fl = prog(t, T["t_photo"] + 0.6, T["t_photo"] + 0.7) * (1 - prog(t, T["t_photo"] + 0.7, T["t_photo"] + 1.0))
        if fl > 0:
            c.drawRect(R(0, 0, W, H), P("#FFFFFF", 0.6 * fl))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "monster", T["t_mon"] - 0.2, T["t_photo"] - 0.2, accent=WARN, size=42)
        if self.rtl:
            self.chip(540, 300, "pinch", T["t_photo"] - 0.2, T["t_pinch"] - 0.1, accent=HILITE, size=44)
            bubble(c, 760, 900, self.L["bubble"], self.span(T["t_pinch"] - 0.1, self.duration + 1), tail_left=False, size=50)
        else:
            self.chip(540, 300, "pinch", T["t_photo"] - 0.2, self.duration + 1, accent=HILITE, size=44)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=H * 0.62)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.5, T["two"]), 61), -20)]
        for k in range(8):
            ev.append((0.2 + k * max(0.25, (T["two"] - 0.2) / 8.0), sfx.clank(520.0, 0.3, 62 + k), -14))
        ev += [(T["three"], sfx.whoosh(0.5, False, 70), -12), (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 71), -10),
               (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 72), -8), (T["eiffel"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 73), -4), (T["wind"], sfx.hiss(2.4, 74), -10),
               (T["solid"], sfx.creak(0.9, 75), -10), (T["sail1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 76), -4), (T["blows"], sfx.whoosh(0.8, False, 77), -12),
               (T["curved"], sfx.sparkle(0.6, 8, 78), -10), (T["down"] + 0.1, sfx.ding(), -8), (T["down"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["soft"], sfx.womp(), -10),
               (T["wet1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 80), -4), (T["air"], sfx.hiss(0.8, 81), -12)]
        for k in range(5):
            ev.append((T["dig"] + k * 0.3, sfx.thud(0.25, 82 + k), -16))
        ev += [(T["firm1"], sfx.thunk(87), -8), (T["firm1"] + 0.2, sfx.ding(), -8), (T["firm1"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 88), -4), (T["meet1"], sfx.clank(300.0, 0.5, 89), -8),
               (T["meet1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 90), -4), (T["nudge"], sfx.whirr(1.2, 90.0, 140.0, 91), -14)]
        for k in range(4):
            ev.append((T["mm"] + k * 0.25, sfx.tick(), -10))
        ev += [(T["line1"], sfx.clank(600.0, 0.4, 92), -8), (T["line1"] + 0.2, sfx.ding(), -8), (T["line1"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 93), -4), (T["pieces"], rumble(1.2, 94), -12),
               (T["hold1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 95), -4), (T["join"], sfx.sizzle(0.6, 96), -12)]
        for k in range(9):
            ev.append((lerp(T["redhot"] - 0.2, T["clamp1"], k / 9.0), sfx.clank(700.0, 0.2, 97 + k), -14))
        ev += [(T["clamp1"], sfx.ding(), -8), (T["clamp1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(106), 0), (T["follow"] - 0.15, sfx.pop(107), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 108), -6), (T["paint"], sfx.hiss(0.7, 109), -14),
               (T["lighter"], sfx.sparkle(0.7, 10, 110), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 111), -6), (T["s1"], sfx.pop(112), -3), (T["s2"], sfx.pop(113), -3),
               (T["s3"], sfx.pop(114), -3)]
        ev += [(T["cong2"], sfx.pop(115), -2), (T["cong2"], sfx.sparkle(1.4, 18, 116), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 117), -6), (T["t_mon"], sfx.buzz(0.4), -14),
               (T["t_photo"] + 0.6, sfx.click(118), -4), (T["t_pinch"], sfx.pop(119), -6)]
        return ev


NAME = "eiffel"
EPISODE = Eiffel
