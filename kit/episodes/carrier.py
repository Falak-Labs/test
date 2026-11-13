"""Episode 25 - An aircraft carrier.  v2 look: the sea at dusk and at night, four worlds with whip cuts.

Sets: sea (side view, bow to the right: a runway drops onto a ship still in red primer; three football fields measure
the deck and a jet rolls off the bow into the sea; the catapult flings the next one off with a speed readout; a jet
comes back too fast and shoots off the end; later the fuel gauge drains and the ship keeps stopping at a floating gas
station, until the hull opens on two glowing nuclear reactors and it sails away for twenty years), hook (from above:
steel cables stretch across the landing area, the tailhook catches one and the jet stops), top (the whole ship from
above, bow to the right: a jet that misses every cable slams into the planes parked at the bow; the landing strip
swings out to the side and the next one just takes off again; later the wide shot: the paint goes navy gray, more than
sixty aircraft appear, the stat cards and the cheer), street (the tag: the pilot cannot parallel park his car).
Side views: the sea surface is y = 0, down is positive.  Top views: x along the ship (bow at +x), y across it.
"""
from v2_base import *  # noqa: F401,F403

PRIMER, NAVYG, DECKC, DECKP = "#8A4B3C", "#66707F", "#3C424E", "#4A3A36"
JETC, SEA_T = "#AEB7C6", "#0E2A5C"
SKINS = ("#E8B48A", "#C68B5E", "#F1C9A5", "#8D5A3B", "#E0A47A")
DECK_Y = -152                                  # side view: the flight deck


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


class Integral:
    """Running integral of f(t) sampled at 60 Hz."""

    def __init__(self, f, t0, t1):
        self.t0, self.dt = t0, 1.0 / 60
        acc, self.v = 0.0, []
        for i in range(int((t1 - t0) * 60) + 3):
            self.v.append(acc)
            acc += f(t0 + i * self.dt) * self.dt

    def at(self, t):
        i = (t - self.t0) / self.dt
        if i <= 0:
            return self.v[0]
        j = min(int(i), len(self.v) - 2)
        return lerp(self.v[j], self.v[j + 1], clamp(i - j))


def jet_side(c, x, y, s=1.0, rot=0.0, hook=0.0, burn=0.0, t=0.0, gear=1.0, a=1.0):
    """A fighter jet from the side, facing right; (x, y) = where the wheels touch."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    if burn > 0:
        v2.flame(c, -60, -20, 14, 70, t, power=burn, ang=180.0)
    fin = skia.Path()
    fin.moveTo(-36, -26)
    fin.lineTo(-56, -58)
    fin.lineTo(-44, -58)
    fin.lineTo(-18, -26)
    fin.close()
    c.drawPath(fin, P(shade(JETC, -0.2), a))
    body = skia.Path()
    body.moveTo(-58, -30)
    body.lineTo(20, -32)
    body.quadTo(52, -30, 66, -21)
    body.quadTo(52, -12, 20, -10)
    body.lineTo(-58, -12)
    body.close()
    c.drawPath(body, lin_paint(0, -32, 0, -10, [shade(JETC, 0.3), JETC, shade(JETC, -0.35)], a=a))
    c.drawOval(R(4, -40, 34, 14), P("#38BDF8", a))
    c.drawOval(R(10, -38, 12, 5), P("#FFFFFF", 0.6 * a))
    wing = skia.Path()
    wing.moveTo(-6, -20)
    wing.lineTo(-40, -14)
    wing.lineTo(-30, -18)
    wing.close()
    c.drawPath(wing, P(shade(JETC, -0.45), a))
    c.drawRect(R(-62, -28, 6, 14), P("#374151", a))
    if gear > 0:
        for gx in (-22, 30):
            c.drawLine(gx, -12, gx, -12 + 10 * gear, P("#475569", a, stroke=3))
            c.drawCircle(gx, -4 + 2 * (1 - gear), 5 * gear, P("#111827", a))
    if hook > 0:
        c.drawLine(-50, -14, -50 - 14 * hook, -14 + 16 * hook, P(HILITE, a, stroke=4))
    c.restore()


def jet_top(c, x, y, s=1.0, rot=0.0, hook=0.0, burn=0.0, t=0.0, col=JETC, a=1.0, shadow=0.0):
    """A fighter jet seen from above, nose to +x."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    if shadow > 0:
        c.save()
        c.translate(30 * shadow, 40 * shadow)
        c.scale(1 - 0.2 * shadow, 1 - 0.2 * shadow)
        c.drawCircle(0, 0, 60, P("#000000", 0.25 * a, blur=12))
        c.restore()
    if burn > 0:
        v2.flame(c, -84, 0, 18, 80, t, power=burn, ang=180.0)
    wing = skia.Path()
    wing.moveTo(34, 0)
    wing.lineTo(-30, -64)
    wing.lineTo(-48, -64)
    wing.lineTo(-38, 0)
    wing.lineTo(-48, 64)
    wing.lineTo(-30, 64)
    wing.close()
    c.drawPath(wing, P(shade(col, -0.18), a))
    tail = skia.Path()
    tail.moveTo(-56, 0)
    tail.lineTo(-80, -28)
    tail.lineTo(-90, -28)
    tail.lineTo(-80, 0)
    tail.lineTo(-90, 28)
    tail.lineTo(-80, 28)
    tail.close()
    c.drawPath(tail, P(shade(col, -0.25), a))
    body = skia.Path()
    body.moveTo(84, 0)
    body.quadTo(64, -13, 22, -14)
    body.lineTo(-84, -11)
    body.lineTo(-84, 11)
    body.lineTo(22, 14)
    body.quadTo(64, 13, 84, 0)
    body.close()
    c.drawPath(body, lin_paint(0, -14, 0, 14, [shade(col, 0.3), col, shade(col, -0.3)], a=a))
    c.drawOval(R(26, -7, 34, 14), P("#38BDF8", a))
    if hook > 0:
        c.drawLine(-84, 0, -84 - 30 * hook, 0, P(HILITE, a, stroke=5))
        c.drawCircle(-84 - 30 * hook, 0, 5, P(HILITE, a))
    c.restore()


def gas_station(c, x, y, t, a=1.0):
    """A cartoon gas station floating on the sea: a raft, a pump, a sign."""
    if a <= 0:
        return
    bob = math.sin(t * 2.0) * 4
    c.save()
    c.translate(x, y + bob)
    c.drawRRect(rr(-80, -16, 160, 30, 10), P("#7C2D12", a))
    c.drawRect(R(-80, -16, 160, 8), P("#B45309", a))
    box(c, -50, -140, 64, 124, "#DC2626", r=10, a=a)
    c.drawRRect(rr(-40, -126, 44, 34, 6), P("#FEF3C7", a))
    c.drawLine(14, -100, 36, -100, P("#111827", a, stroke=6))
    c.drawLine(36, -100, 42, -40, P("#111827", a, stroke=6))
    c.drawRect(R(56, -230, 10, 214), P("#94A3B8", a))
    c.drawRRect(rr(14, -280, 96, 56, 10), P("#F8FAFC", a))
    word(c, "GAS", 62, -239, 32, "#DC2626", a)
    c.restore()


def car(c, x, y, L=200, col="#EF4444", t=0.0, pilot=False, flash=0.0, a=1.0):
    """A small car from the side, centred on x, wheels on y (facing right)."""
    if a <= 0:
        return
    cab = skia.Path()
    cab.moveTo(x - L * 0.32, y - 50)
    cab.lineTo(x - L * 0.2, y - 88)
    cab.lineTo(x + L * 0.16, y - 88)
    cab.lineTo(x + L * 0.3, y - 50)
    cab.close()
    c.drawPath(cab, P(shade(col, -0.1), a))
    c.drawRRect(rr(x - L * 0.17, y - 82, L * 0.14, 28, 5), P("#BFE6FF", 0.85 * a))
    c.drawRRect(rr(x + L * 0.01, y - 82, L * 0.13, 28, 5), P("#BFE6FF", 0.85 * a))
    if pilot:                                                                     # a helmet with a visor
        c.drawCircle(x + L * 0.07, y - 70, 15, P("#F8FAFC", a))
        c.drawRRect(rr(x + L * 0.07, y - 76, 14, 10, 4), P("#F59E0B", a))
    c.drawRRect(rr(x - L / 2, y - 56, L, 38, 14), lin_paint(0, y - 56, 0, y - 18, [shade(col, 0.25), col, shade(col, -0.3)], a=a))
    for wx in (x - L * 0.3, x + L * 0.3):
        c.drawCircle(wx, y - 14, 17, P("#111827", a))
        c.drawCircle(wx, y - 14, 7, P("#9CA3AF", a))
    c.drawRRect(rr(x + L / 2 - 10, y - 50, 10, 10, 3), P("#FDE68A", a))
    c.drawRRect(rr(x - L / 2, y - 50, 8, 10, 3), P("#EF4444", a))
    if flash > 0:
        for fx_ in (x + L / 2 - 5, x - L / 2 + 4):
            add_glow(c, fx_, y - 45, 60, "#FBBF24", 0.8 * flash * a)


def fields(c, x0, x1, y, h, k, t):
    """Three football fields laid end to end over the deck (side view measure)."""
    w = (x1 - x0) / 3
    for i in range(3):
        p = clamp(k * 3 - i)
        if p <= 0:
            continue
        fx = x0 + i * w
        c.save()
        c.translate(fx + w / 2, y + h)
        c.scale(1.0, e_back(p))
        c.translate(-(fx + w / 2), -(y + h))
        c.drawRRect(rr(fx + 4, y, w - 8, h, 8), P("#16A34A", 0.88))
        c.drawRect(R(fx + 4, y, w * 0.08, h), P("#15803D", 0.95))
        c.drawRect(R(fx + w * 0.92 - 4, y, w * 0.08, h), P("#15803D", 0.95))
        for k_ in range(1, 10):
            xx = fx + w * 0.08 + k_ * w * 0.084
            c.drawLine(xx, y + 6, xx, y + h - 6, P("#FFFFFF", 0.7, stroke=2))
        c.drawCircle(fx + w / 2, y + h / 2, 22, P("#FFFFFF"))
        text(c, str(i + 1), fx + w / 2, y + h / 2 + 11, 30, "#15803D", "Poppins-Black")
        c.restore()


def splash_big(c, x, t, t0, seed=4):
    splash(c, x, 0, t, t0, 1.1, n=36, speed=760, width=1.8, seed=seed)
    v2.shock_ring(c, x, 0, t, t0, 0.8, r1=260, col="#DBEAFE", width=10, squash=0.25)


def ring_marks(c, x, y, t, a=1.0):
    """Cartoon dizzy stars."""
    for i in range(4):
        q = t * 5 + i * math.pi / 2
        sx, sy = x + math.cos(q) * 40, y + math.sin(q) * 14
        path = skia.Path()
        for k in range(10):
            r_ = 11 if k % 2 == 0 else 4.5
            qq = -math.pi / 2 + k * math.pi / 5
            (path.moveTo if k == 0 else path.lineTo)(sx + math.cos(qq) * r_, sy + math.sin(qq) * r_)
        path.close()
        c.drawPath(path, P("#FDE047", a))


# ---------------------------------------------------------------------------------------------- sounds
def jet_snd(d=1.6, seed=60):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 500, 5000) + 0.3 * np.sin(2 * np.pi * (900 + 600 * tt / d) * tt)
    return sfx._norm(x * sfx._ar(n, 0.25, 0.5), 0.6)


def cat_snd(d=1.2, seed=61):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._hp(sfx._rng(seed).standard_normal(n), 800) * np.exp(-tt * 3) + 0.4 * np.sin(2 * np.pi * (200 + 900 * tt) * tt)
    return sfx._norm(x * sfx._ar(n, 0.02, 0.4), 0.7)


def honk_snd(d=0.35):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sign(np.sin(2 * np.pi * 420 * tt)) * 0.5 + np.sign(np.sin(2 * np.pi * 520 * tt)) * 0.5
    return sfx._norm(sfx._lp(x, 2500) * sfx._ar(n, 0.01, 0.05), 0.5)


def wire_snd(d=0.8, seed=62):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sin(2 * np.pi * (380 - 200 * tt) * tt) * np.exp(-tt * 4) + 0.5 * sfx._hp(sfx._rng(seed).standard_normal(n), 3000) * np.exp(-tt * 8)
    return sfx._norm(x, 0.7)


def water_snd(d=1.0, seed=63):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 250, 2600)
    return sfx._norm(x * sfx._ar(n, 0.02, 0.6), 0.6)


# ====================================================================================== the episode
class Carrier(EpisodeV2):
    BUILD_NO = 25
    FIRST_SET = "sea"
    CLEAR = "#06102A"
    TITLE = {"en": "AIRCRAFT CARRIER", "ar_sa": "حاملة طيارات"}
    EMPH = {"en": ["CONGRATS", "RUNWAY", "SHIP", "AIRCRAFT", "CARRIER", "DECK", "THREE", "FOOTBALL", "SHORT", "JET",
                   "CATAPULT", "FLINGS", "HUNDRED", "SIXTY", "TWO", "SECONDS", "FLIES", "LANDS", "FAST", "SHOOTS", "END",
                   "STRETCH", "STEEL", "CABLES", "HOOK", "TAIL", "GRABS", "STOPS", "MISSES", "SLAMS", "PLANES", "ANGLE",
                   "LANDING", "SIDE", "GAS", "TAKES", "HEAVY", "STOP", "FUEL", "NUCLEAR", "REACTORS", "PLANT", "TWENTY",
                   "REFUELING", "FOLLOW", "PAINT", "NAVY", "GRAY", "PARK", "FIVE", "ZERO", "YOURSELF", "PILOTS", "NIGHT",
                   "PARALLEL"],
            "ar_sa": ["مبروك", "ممر", "مركب", "حاملة", "السطح", "تلات", "ملاعب", "قصير", "نفاثة", "منجنيق", "يرمي", "لميتين",
                      "تانيتين", "بتطير", "بتنزل", "بسرعة", "الآخر", "فتشد", "كابلات", "وخطاف", "ديلها", "يمسك", "ويوقفها",
                      "تفوت", "تخبط", "الطيارات", "قدام", "فتميل", "النزول", "جنب", "بنزين", "وتطير", "بالتقل", "يقف",
                      "يمون", "مفاعلين", "نوويين", "المحطة", "عشرين", "تمون", "تابعني", "ادهنها", "رمادي", "واركن", "ستين",
                      "مية", "خمس", "وصفر", "بإيدك", "والطيار", "بالليل", "يركن", "البلد"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "RUNWAY"): "ممر", ("hook", "SHIP"): "مركب", ("hook", "CONGRATS"): "مبروك", ("hook", "AIRCRAFT"): "حاملة",
        ("break1", "DECK"): "السطح", ("break1", "THREE"): "تلات", ("break1", "FOOTBALL"): "ملاعب", ("break1", "SHORT"): "قصير",
        ("break1", "JET"): "نفاثة", ("break1", "OFF"): "تطير",
        ("fix1", "CATAPULT"): "منجنيق", ("fix1", "FLINGS"): "يرمي", ("fix1", "HUNDRED"): "ميتين", ("fix1", "TWO"): "تانيتين",
        ("fix1", "SECONDS"): "تانيتين",
        ("break2", "FLIES"): "بتطير", ("break2", "COMING"): "راجعة", ("break2", "LANDS"): "بتنزل", ("break2", "FAST"): "بسرعة",
        ("break2", "SHOOTS"): "تكمل", ("break2", "END"): "الآخر",
        ("fix2", "STRETCH"): "فتشد", ("fix2", "CABLES"): "كابلات", ("fix2", "HOOK"): "وخطاف", ("fix2", "TAIL"): "ديلها",
        ("fix2", "GRABS"): "يمسك", ("fix2", "STOPS"): "ويوقفها",
        ("break3", "JET"): "الطيارة", ("break3", "MISSES"): "تفوت", ("break3", "CABLE"): "الكابلات", ("break3", "SLAMS"): "تخبط",
        ("break3", "PLANES"): "الطيارات", ("break3", "FRONT"): "قدام",
        ("fix3", "ANGLE"): "فتميل", ("fix3", "LANDING"): "النزول", ("fix3", "SIDE"): "جنب", ("fix3", "MISSES"): "فوتت",
        ("fix3", "GAS"): "بنزين", ("fix3", "TAKES"): "وتطير",
        ("break4", "WORKS"): "شغالة", ("break4", "HEAVY"): "بالتقل", ("break4", "STOP"): "يقف", ("break4", "FUEL"): "يمون",
        ("break4", "TIME"): "شوية",
        ("fix4", "REACTORS"): "مفاعلين", ("fix4", "PLANT"): "المحطة", ("fix4", "SAILS"): "وتمشي", ("fix4", "TWENTY"): "عشرين",
        ("fix4", "REFUELING"): "تمون",
        ("cta", "LAUNCH"): "تطلع", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PAINT"): "ادهنها", ("reveal", "GRAY"): "رمادي", ("reveal", "PARK"): "واركن", ("reveal", "SIXTY"): "ستين",
        ("reveal", "AIRCRAFT"): "طيارة",
        ("stat", "HUNDRED"): "مية", ("stat", "FIVE"): "خمس", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "PILOTS"): "والطيار", ("tag", "LAND"): "بينزل", ("tag", "NIGHT"): "بالليل", ("tag", "PARALLEL"): "بيلف",
        ("tag", "PARK"): "يركن"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the world's tallest tower"),
                   "stat": [("100,000", "TONS"), ("5,000", "PEOPLE"), ("0", "GAS STATIONS")],
                   "L": {"runway": "RUNWAY", "ship": "YOUR AIRCRAFT CARRIER", "short": "TOO SHORT", "cat": "CATAPULT",
                         "unit": "MPH", "sec2": "2 SECONDS", "fast": "TOO FAST", "cables": "STEEL CABLES", "hook": "TAILHOOK",
                         "stopped": "STOPPED IN 2 SECONDS", "miss": "MISSED EVERY CABLE", "parked": "PARKED PLANES",
                         "angled": "ANGLED LANDING STRIP", "again": "TAKES OFF AGAIN", "fuel": "FUEL",
                         "stopfuel": "STOP FOR FUEL. AGAIN.", "reactors": "2 NUCLEAR REACTORS", "likeplant": "LIKE OUR NUCLEAR PLANT",
                         "years": "YEARS", "gray": "NAVY GRAY", "sixty": "60+ AIRCRAFT", "landship": "LANDS ON A SHIP AT NIGHT",
                         "parking": "PARALLEL PARKING"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: أطول برج في الدنيا"),
                      "stat": [("100,000", "طن"), ("5,000", "واحد"), ("0", "بنزينة")],
                      "L": {"runway": "ممر طيارات", "ship": "حاملة طياراتك", "short": "قصير أوي", "cat": "منجنيق",
                            "unit": "كم/س", "sec2": "تانيتين", "fast": "سريعة أوي", "cables": "كابلات حديد", "hook": "خطاف الديل",
                            "stopped": "وقفت في تانيتين", "miss": "فوتت كل الكابلات", "parked": "طيارات راكنة",
                            "angled": "ممر نزول مايل", "again": "طارت تاني", "fuel": "البنزين", "stopfuel": "وقفة بنزين تاني",
                            "reactors": "مفاعلين نوويين", "likeplant": "زي محطتنا النووية", "years": "سنة", "gray": "رمادي",
                            "sixty": "+60 طيارة", "landship": "بينزل على مركب بالليل", "parking": "الركنة في وسط البلد"}}}
    SKY_ALT = {}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "runway": ("hook", "RUNWAY", 0.2), "ship": ("hook", "SHIP", 0.35), "congrats": ("hook", "CONGRATS", 0.55),
            "carrier": ("hook", "AIRCRAFT", 0.85),
            "deck": ("break1", "DECK", 0.1), "three": ("break1", "THREE", 0.3), "football": ("break1", "FOOTBALL", 0.4),
            "short": ("break1", "SHORT", 0.65), "jet": ("break1", "JET", 0.8), "off": ("break1", "OFF", 0.95),
            "catapult": ("fix1", "CATAPULT", 0.15), "flings": ("fix1", "FLINGS", 0.3), "hundred": ("fix1", "HUNDRED", 0.55),
            "two": ("fix1", "TWO", 0.85), "seconds": ("fix1", "SECONDS", 0.95),
            "flies": ("break2", "FLIES", 0.1), "coming": ("break2", "COMING", 0.3), "lands": ("break2", "LANDS", 0.5),
            "fast": ("break2", "FAST", 0.6), "shoots": ("break2", "SHOOTS", 0.75), "end": ("break2", "END", 0.95),
            "stretch": ("fix2", "STRETCH", 0.1), "cables": ("fix2", "CABLES", 0.25), "hook": ("fix2", "HOOK", 0.5),
            "tail": ("fix2", "TAIL", 0.6), "grabs": ("fix2", "GRABS", 0.7), "stops": ("fix2", "STOPS", 0.85),
            "jet3": ("break3", "JET", 0.1), "misses": ("break3", "MISSES", 0.3), "cable3": ("break3", "CABLE", 0.45),
            "slams": ("break3", "SLAMS", 0.6), "planes": ("break3", "PLANES", 0.75), "front": ("break3", "FRONT", 0.95),
            "angle": ("fix3", "ANGLE", 0.1), "landing": ("fix3", "LANDING", 0.2), "side": ("fix3", "SIDE", 0.4),
            "misses2": ("fix3", "MISSES", 0.55), "gas": ("fix3", "GAS", 0.75), "takes": ("fix3", "TAKES", 0.85),
            "works": ("break4", "WORKS", 0.1), "heavy": ("break4", "HEAVY", 0.35), "stop": ("break4", "STOP", 0.6),
            "fuel": ("break4", "FUEL", 0.75), "time": ("break4", "TIME", 0.95),
            "reactors": ("fix4", "REACTORS", 0.25), "plant": ("fix4", "PLANT", 0.45), "sails": ("fix4", "SAILS", 0.7),
            "twenty": ("fix4", "TWENTY", 0.78), "refuel": ("fix4", "REFUELING", 0.95),
            "launch": ("cta", "LAUNCH", 0.2), "follow": ("cta", "FOLLOW", 0.35),
            "paint": ("reveal", "PAINT", 0.15), "gray": ("reveal", "GRAY", 0.35), "park": ("reveal", "PARK", 0.55),
            "sixty": ("reveal", "SIXTY", 0.75), "aircraft": ("reveal", "AIRCRAFT", 0.9),
            "s1": ("stat", "HUNDRED", 0.04), "s2": ("stat", "FIVE", 0.4), "s3": ("stat", "ZERO", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "pilots": ("tag", "PILOTS", 0.12), "land2": ("tag", "LAND", 0.25), "night": ("tag", "NIGHT", 0.45),
            "parallel": ("tag", "PARALLEL", 0.8), "park2": ("tag", "PARK", 0.92)})
        T["roll0"] = min(T["jet"] - 0.35, T["off"] - 1.2)                 # break1: the jet rolls and drops off the bow
        T["drop"] = T["off"] - 0.05
        T["fling0"] = T["flings"] - 0.05
        T["td"] = T["lands"]                                               # break2: touchdown, then off the end
        T["over"] = max(T["shoots"] + 0.1, T["td"] + 0.8)
        T["catch"] = T["grabs"]
        T["halt"] = max(T["stops"] + 0.2, T["catch"] + 1.1)
        T["crash"] = T["slams"]
        T["bolter"] = T["misses2"]
        T["pay"] = min(T["park"], T["sixty"])
        T["pk2"] = min(T["parallel"], T["park2"])
        # ---- sets
        self.cut(s("fix2") - 0.12, "hook", 1)
        self.cut(s("break3") - 0.12, "top", -1)
        self.cut(s("fix3") - 0.12, "top", 1)                      # same set: the crash is cleared away
        self.cut(s("break4") - 0.12, "sea", 1)
        self.cut(s("cta") + 0.05, "top", -1)
        self.cut(s("tag") - 0.2, "street", 1)
        self.cams = {"sea": Camera(20, -306, 0.74), "hook": Camera(40, 60, 0.85), "top": Camera(0, 140, 0.72),
                     "street": Camera(-80, -186, 1.45)}
        cm = self.cams
        cm["sea"].key(0.05, 20, -300, 0.78, 1.6).key(T["congrats"], 30, -306, 0.74, 1.2)
        cm["sea"].key(T["roll0"] - 0.2, 260, -300, 0.84, 1.0)
        cm["sea"].key(s("fix1") - 0.1, 360, -262, 1.05, 0.8).key(T["fling0"] + 0.5, 470, -330, 0.95, 0.9)
        cm["sea"].key(s("break2") - 0.1, 40, -300, 0.74, 0.9).key(T["over"] - 0.4, 260, -300, 0.84, 0.8)
        cm["sea"].key(s("break4") - 0.12, 230, -306, 0.72, 0.0).key(s("fix4"), 60, -280, 0.76, 1.0)
        cm["hook"].key(s("fix2"), 60, 60, 0.85, 3.0)
        cm["top"].key(s("break3") - 0.12, 0, 140, 0.72, 0.0).key(s("fix3") - 0.12, 0, 140, 0.72, 0.0)
        cm["top"].key(s("cta") + 0.05, 0, 120, 0.66, 0.0).key(s("reveal") - 0.1, 30, 110, 0.7, 1.2)
        cm["top"].key(T["s1"] - 0.3, 30, -40, 0.56, 1.0).key(s("closer") - 0.2, 20, 60, 0.64, 0.9)
        cm["street"].key(s("tag") - 0.2, -40, -186, 1.45, 0.0).key(T["pilots"] + 0.3, -90, -196, 1.4, 1.0)
        # ---- tracks
        self.rdrop = Track(-1150.0).to(0.1, -760.0, max(0.6, T["runway"] - 0.45), e_out)
        self.rdrop.to(T["runway"] - 0.25, 0.0, max(0.5, T["ship"] - T["runway"] + 0.25), e_in)
        self.fieldk = Track(0.0).to(T["three"] - 0.15, 1.0, max(0.6, T["football"] - T["three"] + 0.5))
        self.fieldk.to(T["roll0"] - 0.3, 0.0, 0.4)
        self.fuel = Track(0.95).to(T["works"], 0.12, max(1.0, T["stop"] - T["works"]))
        self.fuel.to(T["stop"] + 0.4, 0.95, 0.35).to(T["fuel"], 0.15, max(0.6, T["time"] - T["fuel"]))
        self.fuel.to(T["time"] + 0.3, 0.95, 0.35)
        self.speed = Track(1.0).to(T["stop"] - 0.3, 0.0, 0.5).to(T["stop"] + 0.6, 1.0, 0.5)
        self.speed.to(T["time"] - 0.2, 0.0, 0.4).to(s("fix4") + 0.2, 0.0, 0.1).to(T["sails"] - 0.2, 2.6, 1.2)
        self.cutk = Track(0.0).to(T["reactors"] - 0.5, 1.0, 0.6, e_out)
        self.angle = Track(0.0).to(T["angle"] - 0.15, 1.0, 0.8, e_io)
        self.paint = Track(0.0).to(T["paint"] - 0.1, 1.0, max(0.8, T["gray"] - T["paint"] + 0.5), e_io)
        t_end = self.tl.duration + 1
        self.dist = Integral(lambda t: 260 * self.speed.at(t), 0, t_end)
        self.spans = [(T["off"], T["seconds"] + 0.3), (T["end"], T["stops"] + 0.4), (T["slams"], T["takes"] + 0.4),
                      (T["time"], T["refuel"] + 0.3)]
        self.shakes = [(T["ship"], 0.35, 12), (T["drop"] + 0.42, 0.4, 12), (T["fling0"], 0.35, 10), (T["over"] + 0.4, 0.4, 12),
                       (T["catch"], 0.3, 10), (T["crash"], 0.6, 22), (T["angle"] + 0.6, 0.25, 6), (T["gas"], 0.3, 8),
                       (T["stop"], 0.3, 8), (T["time"], 0.3, 8), (T["sails"], 0.4, 10), (s("closer") + 0.2, 0.35, 10),
                       (T["pk2"], 0.3, 12)]
        # sixty-odd aircraft for the reveal (top view, deck coordinates)
        spots = []
        for i in range(6):
            for j in range(3):
                spots.append((480 + j * 70 - (i % 2) * 10, -105 + i * 42, 30))
        for i in range(14):
            spots.append((-560 + i * 60, 118, 130))
        for i in range(10):
            spots.append((-640 + i * 58, -118, -130))
        for i in range(8):
            spots.append((280 + i * 54, 140, 120))
        for i in range(6):
            for j in range(2):
                spots.append((-680 + j * 56, -60 + i * 26, 0))
        for i in range(8):
            spots.append((120 + i * 48, -200 + (i % 2) * 18, -150))
        self.spots = spots[:64]

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    # ------------------------------------------------------------------ shared drawing (side view)
    def surface_y(self, cam):
        cx, cy, z = cam
        return (0 - cy) * z + H / 2

    def veil(self, c, t, cam, a=0.55):
        cx, cy, z = cam
        x0, x1 = cx - 640 / z, cx + 640 / z
        c.drawRect(R(x0, 0, x1 - x0, 3000), P(SEA_T, a))
        for k in range(3):
            path = skia.Path()
            xx = x0
            path.moveTo(xx, k * 12)
            while xx < x1:
                xx += 36
                path.lineTo(xx, k * 12 + math.sin(xx * 0.012 + t * (1.2 + k * 0.3) + k) * (4 + k))
            c.drawPath(path, P("#D6EEFF", 0.6 - k * 0.18, stroke=3.5 - k * 0.5))

    def ship_side(self, c, t, runway=1.0, rdy=0.0, cut=0.0):
        """The carrier from the side, bow to the right, still in red primer."""
        hull = skia.Path()
        hull.moveTo(-690, -140)
        hull.lineTo(690, -140)
        hull.quadTo(704, -20, 600, 70)
        hull.lineTo(-620, 70)
        hull.quadTo(-684, 40, -690, -40)
        hull.close()
        c.drawPath(hull, lin_paint(0, -140, 0, 70, [shade(PRIMER, 0.15), PRIMER, shade(PRIMER, -0.45)], a=1 - 0.75 * cut))
        if cut > 0:                                                                 # cut open: two reactors inside
            c.save()
            c.clipPath(hull, skia.ClipOp.kIntersect, True)
            c.drawRect(R(-700, -140, 1420, 220), P("#0B1222", 0.85 * cut))
            for rx in (-300, 40):
                cyl(c, rx - 60, -118, 120, 150, "#64748B", r=56, a=cut)
                add_glow(c, rx, -44, 150, "#38BDF8", 0.75 * cut)
                c.drawCircle(rx, -44, 26, P("#7DD3FC", 0.9 * cut))
            c.drawLine(-240, -30, -680, 30, P("#94A3B8", 0.8 * cut, stroke=8))
            c.restore()
            c.drawPath(hull, P("#FBBF24", 0.6 * cut, stroke=3))
        for i in range(6):                                                          # hangar openings
            c.drawRect(R(-520 + i * 190, -118, 90, 34), P("#1B1F2A", 0.8 * (1 - cut)))
        c.drawLine(-690, -60, 690, -60, P("#000000", 0.18, stroke=3))
        if runway > 0:                                                              # the flight deck on top
            c.save()
            c.translate(0, rdy)
            c.drawRect(R(-706, DECK_Y, 1446, 14), P(DECKC))
            c.drawRect(R(-706, DECK_Y, 1446, 3), P("#6B7280"))
            for xx in range(-660, 720, 70):
                c.drawRect(R(xx, DECK_Y + 4, 34, 3), P("#F8FAFC", 0.9))
            c.restore()
        box(c, 210, -320, 110, 170, PRIMER, r=8)                                    # the island
        for i in range(4):
            c.drawRect(R(222 + i * 24, -300, 16, 14), P("#FDE68A", 0.8))
        c.drawRect(R(258, -430, 8, 110), P("#4B5563"))
        c.drawRect(R(236, -400, 52, 8), P("#4B5563"))
        c.drawRect(R(246, -378, 32, 6), P("#4B5563"))
        beacon(c, 262, -436, t, hz=1.0, r=5)

    def wake(self, c, t, k=1.0):
        """Foam along the waterline that slides back as the ship moves; bow wave."""
        if k <= 0:
            return
        d = self.dist.at(t)
        for i in range(16):
            u = ((i * 97 + d) % 1500) / 1500
            x = 700 - u * 2200
            c.drawRRect(rr(x, -6 + (i % 3) * 7, 60 + 30 * (i % 2), 6, 3), P("#E0F2FE", 0.55 * k * (1 - u * 0.6)))
        c.drawOval(R(620, -20, 120, 32), P("#E0F2FE", 0.5 * k))

    # ------------------------------------------------------------------ set: the sea, side view (hook..break2, break4, fix4)
    def draw_sea(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["sea"].at(t)
        cam = (cam[0], cam[1] + math.sin(t * 0.7) * 3, cam[2])
        cx, cy, z = cam
        self.backdrop(c, t, cx, cy, self.surface_y(cam), sea_=True, moon=True)
        self.view(c, cam)
        sea(c, cx - 680 / z, cx + 680 / z, t, moon_x=-420)
        late = t >= s("break4") - 0.2
        bob = math.sin(t * 1.3) * 3
        c.save()
        c.translate(0, bob)
        rdy = self.rdrop.at(t) if not late else 0.0
        has_rw = 1.0
        self.ship_side(c, t, runway=has_rw, rdy=rdy, cut=self.cutk.at(t) if late else 0.0)
        if not late:
            fields(c, -700, 740, -232, 64, self.fieldk.at(t), t)
            self.side_jets(c, t)
        c.restore()
        self.wake(c, t, (self.speed.at(t) * 0.8 if late else 0.6))
        if late:
            for tk in (T["stop"] + 0.2, T["time"] + 0.2):                           # gas stations at sea, one per stop
                gx = 830 + (self.dist.at(tk) - self.dist.at(t))
                if -1300 < gx < 1700:
                    gas_station(c, gx, 0, t)
            if s("fix4") - 0.2 <= t:                                                 # a picture of our nuclear plant
                pk = prog(t, T["plant"] - 0.2, T["plant"] + 0.25) * (1 - prog(t, T["sails"] + 0.3, T["sails"] + 0.7))
                if pk > 0:
                    c.save()
                    c.translate(-200, -640)
                    c.scale(e_back(pk) * 1.25, e_back(pk) * 1.25)
                    glass(c, -190, -190, 380, 250, r=26, a=pk)
                    c.drawRRect(rr(-190, -190, 380, 250, 26), P(HILITE, 0.8 * pk, stroke=4))
                    for tx in (-100, -10):
                        tp = skia.Path()
                        tp.moveTo(tx - 42, 30)
                        tp.quadTo(tx - 22, -40, tx - 28, -100)
                        tp.lineTo(tx + 28, -100)
                        tp.quadTo(tx + 22, -40, tx + 42, 30)
                        tp.close()
                        c.drawPath(tp, lin_paint(tx - 42, 0, tx + 42, 0, ["#94A3B8", "#F1F5F9", "#94A3B8"], a=pk))
                        c.drawCircle(tx, -126, 24, P("#FFFFFF", 0.85 * pk))
                        c.drawCircle(tx + 12, -150, 18, P("#FFFFFF", 0.7 * pk))
                    c.drawRect(R(50, -40, 100, 70), P("#E2E8F0", pk))
                    c.drawCircle(100, -40, 50, P("#E2E8F0", pk))
                    c.drawLine(-180, 30, 180, 30, P("#94A3B8", pk, stroke=4))
                    c.restore()
        self.veil(c, t, cam, 0.5)
        if not late:
            if T["drop"] < t < T["drop"] + 2.0:
                splash_big(c, 868, t, T["drop"] + 0.42, seed=5)
            if T["over"] < t < T["over"] + 2.0:
                splash_big(c, 870, t, T["over"] + 0.42, seed=7)
        c.restore()
        self.ui["cam"] = cam

    def side_jets(self, c, t):
        T, s = self.T, self.tl.s
        # break1: rolls the whole deck and drops off the bow
        if T["roll0"] - 0.6 <= t < T["drop"] + 0.6:
            if t < T["drop"]:
                x = -600 + 1340 * e_in(prog(t, T["roll0"], T["drop"]))
                jet_side(c, x, DECK_Y, 1.25, 0, t=t, burn=0.7 * prog(t, T["roll0"] - 0.2, T["roll0"]))
            else:
                a_ = t - T["drop"]
                jet_side(c, 740 + 300 * a_, DECK_Y + 900 * a_ * a_, 1.25, 70 * a_ / 0.42, t=t, burn=0.5)
        # fix1: the catapult flings the next one
        if s("fix1") - 0.2 <= t < s("break2") - 0.15:
            slot = prog(t, T["catapult"] - 0.3, T["catapult"] + 0.1)
            c.drawRect(R(140, DECK_Y + 1, 520 * slot, 5), P(HILITE, 0.9))
            for xx in range(150, int(140 + 520 * slot), 40):
                c.drawRect(R(xx, DECK_Y + 1, 18, 5), P("#111827", 0.9))
            if t < T["fling0"]:
                jet_side(c, 170, DECK_Y, 1.25, 0, t=t, burn=0.6 * prog(t, T["fling0"] - 0.8, T["fling0"] - 0.3))
                v2.smoke(c, 200, DECK_Y - 4, t, s("fix1"), None, rate=10, life=1.0, spread=(60, -60), rise=-60, size=(10, 40),
                         col="#FFFFFF", lit=None, lit_until=0.0, seed=21, a=0.7)
            else:
                a_ = t - T["fling0"]
                u = prog(a_, 0.0, 0.7)
                if a_ < 0.7:
                    x, y, rot = 170 + 520 * e_in(u), DECK_Y, 0.0
                else:
                    b_ = a_ - 0.7
                    x, y, rot = 690 + 1100 * b_, DECK_Y - 260 * b_ * b_ - 90 * b_, -14 * min(1.0, b_ * 3)
                jet_side(c, x, y, 1.25, rot, t=t, burn=1.0, gear=1 - prog(a_, 0.8, 1.1))
                v2.smoke(c, 170, DECK_Y - 4, t, T["fling0"], T["fling0"] + 0.6, rate=30, life=1.4, spread=(160, -70), rise=-50,
                         size=(14, 60), col="#FFFFFF", lit=None, lit_until=0.0, seed=22, a=0.8, origin=lambda tb: (170 + 520 * e_in(prog(tb - T["fling0"], 0, 0.7)), DECK_Y - 4))
        # break2: comes back too fast and shoots off the end
        if T["coming"] - 0.8 <= t < T["over"] + 0.6:
            if t < T["td"]:
                u = prog(t, T["coming"] - 0.8, T["td"])
                jet_side(c, lerp(-1250, -600, u), lerp(-560, DECK_Y, e_out(u)), 1.25, 9 * (1 - u), t=t, burn=0.3, hook=0.0)
            elif t < T["over"]:
                x = -600 + 1340 * prog(t, T["td"], T["over"])
                jet_side(c, x, DECK_Y, 1.25, 0, t=t, burn=0.4)
                if t < T["td"] + 0.4:
                    v2.smoke(c, -600, DECK_Y, t, T["td"], T["td"] + 0.15, rate=40, life=0.8, spread=(80, -30), rise=-40,
                             size=(10, 36), col="#E5E7EB", lit=None, lit_until=0.0, seed=23, a=0.8)
            else:
                a_ = t - T["over"]
                jet_side(c, 740 + 380 * a_, DECK_Y + 900 * a_ * a_, 1.25, 60 * a_ / 0.42, t=t, burn=0.3)

    def ui_sea(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            x0, y0 = self.at(-300, DECK_Y - 4)
            self.label(x0, y0, 300, 560, "runway", T["runway"] + 0.2, T["carrier"] - 0.2, HILITE)
            self.chip(540, 470, "ship", T["carrier"] - 0.15, s("break1") + 0.2, accent=HILITE, size=38)
            return
        if tw < s("fix1"):
            self.chip(540, 470, "short", T["short"] - 0.05, s("fix1") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["drop"] + 0.4, s("fix1") - 0.2, x=880, y=640)
            self.red(T["drop"] + 0.4, 2.0)
            return
        if tw < s("break2") - 0.12:
            x0, y0 = self.at(400, DECK_Y)
            self.label(x0, y0, 300, 560, "cat", T["catapult"] + 0.1, T["two"] - 0.1, HILITE)
            p = self.span(T["fling0"], s("break2") - 0.2, 0.2, 0.2)
            if p > 0:
                top = 260 if self.rtl else 160
                v = int(round(top * e_out(prog(tw, T["fling0"], max(T["hundred"] + 0.5, T["fling0"] + 1.2)))))
                v2.chip(c, 540, 470, f"{v} {self.L['unit']}", p, accent=GOOD, size=58)
            self.chip(540, 600, "sec2", T["two"] - 0.05, s("break2") - 0.2, accent=GOOD, size=40)
            self.badge("check", T["seconds"] + 0.2, s("break2") - 0.15, x=880, y=760)
            return
        if tw < s("fix2"):
            self.chip(540, 470, "fast", T["fast"] - 0.05, s("fix2") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["over"] + 0.4, s("fix2") - 0.2, x=880, y=640)
            self.red(T["over"] + 0.4, 2.0)
            return
        if tw < s("fix4"):
            p = self.span(s("break4") - 0.1, s("fix4") + 0.3)
            if p > 0:
                k = self.fuel.at(tw)
                v2.gauge(c, 60, 300, [(self.L["fuel"], k, mix(WARN, GOOD, k))], p, w=330)
            self.chip(540, 560, "stopfuel", T["stop"] - 0.05, s("fix4") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["time"], s("fix4") - 0.2, x=900, y=330)
            self.red(T["time"], 2.0)
            return
        x0, y0 = self.at(-300, -44)
        self.label(x0, y0, 290, 420, "reactors", T["reactors"] - 0.1, T["sails"] - 0.1, NEUT_C)
        x1, y1 = self.at(30, -700)
        self.label(x1, y1, 780, 420, "likeplant", T["plant"] + 0.2, T["sails"] + 0.4, HILITE, size=30)
        p = self.span(T["twenty"] - 0.3, s("cta") - 0.1, 0.2, 0.2)
        if p > 0:
            n = int(round(20 * prog(tw, T["twenty"] - 0.3, T["twenty"] + 0.6)))
            v2.chip(c, 540, 560, f"{n} {self.L['years']}", p, accent=GOOD, size=58)
        self.badge("check", T["refuel"] + 0.2, s("cta") - 0.05, x=880, y=720)

    # ------------------------------------------------------------------ set: the hook (fix2, from above)
    CAB = (60, 140, 220, 300)

    def jet_x(self, t):
        T = self.T
        if t < T["catch"]:
            return 290 + 600 * (t - T["catch"])
        return 290 + 200 * e_out(prog(t, T["catch"], T["halt"]))

    def draw_hook(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["hook"].at(t)
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0B2A55", "#071A3A"]))
        self.view(c, cam)
        rng = random.Random(8)
        for i in range(40):                                                          # the sea far below
            x = (rng.uniform(-900, 900) - t * 40) % 1800 - 900
            c.drawRRect(rr(x, rng.uniform(-1200, 1300), rng.uniform(40, 120), 4, 2), P("#9CC9F5", 0.18))
        c.drawRect(R(-1000, -250, 2000, 500), P("#000000", 0.35, blur=24))
        c.drawRect(R(-1000, -240, 2000, 480), lin_paint(0, -240, 0, 240, [shade(DECKC, 0.12), DECKC, shade(DECKC, -0.2)]))
        for yy in (-200, 200):
            c.drawLine(-1000, yy, 1000, yy, P("#F8FAFC", 0.8, stroke=5))
        for xx in range(-1000, 1000, 120):
            c.drawRect(R(xx, -4, 60, 8), P("#F8FAFC", 0.8))
        jx = self.jet_x(t)
        hx = jx - 150
        for i, cx_ in enumerate(self.CAB):                                           # the steel cables
            k = prog(t, T["stretch"] - 0.1 + i * 0.12, T["stretch"] + 0.3 + i * 0.12)
            if k <= 0:
                continue
            for sd in (-1, 1):
                c.drawRRect(rr(cx_ - 14, sd * 214 - 12, 28, 24, 6), P("#1F2937"))
            if i == 1 and t >= T["catch"]:
                path = skia.Path()
                path.moveTo(cx_, -200)
                path.lineTo(hx, 0)
                path.lineTo(cx_, 200)
                c.drawPath(path, P("#E5E7EB", 1, stroke=6))
            else:
                c.drawLine(cx_, -200, cx_, -200 + 400 * e_out(k), P("#E5E7EB", 1, stroke=6))
        if jx > -900:
            hk = prog(t, T["hook"] - 0.3, T["hook"] + 0.1)
            jet_top(c, jx, 0, 1.35, 0, hook=hk, t=t, burn=0.4 if t < T["catch"] else 0.4 * (1 - prog(t, T["catch"], T["catch"] + 0.5)))
            if t >= T["catch"]:
                v2.smoke(c, jx - 20, 0, t, T["catch"], T["catch"] + 0.6, rate=26, life=0.9, spread=(60, -30), rise=0,
                         size=(10, 40), col="#D1D5DB", lit=None, lit_until=0.0, seed=31, a=0.6, origin=lambda tb: (self.jet_x(tb) - 20, 40))
        c.restore()
        self.ui["cam"] = cam

    def ui_hook(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, y0 = self.at(300, -200)
        self.label(x0, y0, 780, 450, "cables", T["cables"] + 0.1, T["hook"] - 0.2, "#E5E7EB")
        jx = self.jet_x(tw)
        x1, y1 = self.at(jx - 150 - 30 * prog(tw, T["hook"] - 0.3, T["hook"] + 0.1), 0)
        if tw < T["catch"] + 0.4:
            self.label(x1, y1, 300, 450, "hook", T["hook"], T["catch"] + 0.4, HILITE)
        self.chip(540, 560, "stopped", T["stops"] - 0.05, s("break3") - 0.15, accent=GOOD, size=38)
        self.badge("check", T["halt"] - 0.1, s("break3") - 0.15, x=900, y=360)

    # ------------------------------------------------------------------ set: the whole ship from above (break3, fix3, cta..closer)
    def deck_path(self, ang):
        p = skia.Path()
        p.moveTo(-700, -150)
        p.lineTo(-40, -150)
        p.lineTo(200, lerp(-150, -218, ang))
        p.lineTo(360, lerp(-150, -218, ang))
        p.lineTo(420, -150)
        p.lineTo(620, -150)
        p.quadTo(740, -122, 762, 0)
        p.quadTo(740, 122, 620, 150)
        p.lineTo(-700, 150)
        p.close()
        return p

    def strip(self, ang):
        """Start, end and unit vectors of the landing strip (straight -> angled)."""
        x0, y0 = -650, lerp(0, 30, ang)
        x1, y1 = lerp(650, 340, ang), lerp(0, -134, ang)
        L = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        return (x0, y0), (x1, y1), (ux, uy), (-uy, ux), L

    PARKED = ((530, -96, 30), (530, -8, 30), (530, 80, 30), (632, -60, 30), (632, 30, 30))

    def draw_top(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["top"].at(t)
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0D2E5E", "#081C3E"]))
        self.view(c, cam)
        cx, cy, z = cam
        rng = random.Random(9)
        for i in range(60):                                                          # whitecaps drifting past
            x = (rng.uniform(-1600, 1600) - t * 60) % 3200 - 1600
            c.drawRRect(rr(x, rng.uniform(-1600, 1700), rng.uniform(30, 90), 4, 2), P("#BFDBFE", 0.16))
        for i in range(10):                                                          # the wake behind the stern
            u = ((t * 0.5 + i / 10) % 1.0)
            c.drawOval(R(-720 - u * 900, -60 - u * 120, 160, 120 + u * 240), P("#E0F2FE", 0.10 * (1 - u)))
        late = t >= s("cta") + 0.05
        ang = 1.0 if late else self.angle.at(t)
        pk = self.paint.at(t) if late else 0.0
        dp = self.deck_path(ang)
        c.drawPath(dp, P("#000000", 0.4, blur=22))
        c.save()                                                                    # hull rim colour: primer -> navy gray (bow first)
        c.translate(0, 0)
        c.drawPath(dp, P(PRIMER))
        if pk > 0:
            c.save()
            c.clipRect(R(780 - 1560 * pk, -400, 1560 * pk + 40, 800))
            c.drawPath(dp, P(NAVYG))
            c.restore()
        c.restore()
        c.save()
        c.translate(0, 0)
        c.scale(0.985, 0.92)
        c.drawPath(dp, P(mix(DECKP, DECKC, pk)))
        c.restore()
        (x0, y0), (x1, y1), (ux, uy), (nx, ny), L = self.strip(ang)
        mk = 0.55 + 0.45 * pk
        for sd in (-1, 1):                                                          # strip edges and the centre line
            c.drawLine(x0 + nx * 70 * sd, y0 + ny * 70 * sd, x1 + nx * 70 * sd, y1 + ny * 70 * sd, P("#F8FAFC", 0.75 * mk, stroke=4))
        d = 0.0
        while d < L - 30:
            c.drawLine(x0 + ux * d, y0 + uy * d, x0 + ux * (d + 34), y0 + uy * (d + 34), P("#F8FAFC", 0.85 * mk, stroke=4))
            d += 70
        if not late and T["landing"] - 0.2 <= t < s("break4"):                      # the new strip lights up
            gl = bump(t, T["landing"] - 0.2, T["landing"] + 0.9)
            for sd in (-1, 1):
                c.drawLine(x0 + nx * 70 * sd, y0 + ny * 70 * sd, x1 + nx * 70 * sd, y1 + ny * 70 * sd, P(HILITE, gl, stroke=8))
        for i in range(4):                                                          # cables across the strip
            dd = 110 + i * 46
            ax, ay = x0 + ux * dd, y0 + uy * dd
            c.drawLine(ax - nx * 76, ay - ny * 76, ax + nx * 76, ay + ny * 76, P("#E5E7EB", 0.9, stroke=4))
        for yy in (-60, 60):                                                        # bow catapults
            c.drawLine(230, yy, 700, yy * 0.6, P(HILITE, 0.5, stroke=3))
        box(c, 120, 150, 150, 52, mix(PRIMER, NAVYG, clamp(pk * 1.6 - 0.6)), r=8)     # the island (starboard)
        c.drawCircle(196, 176, 12, P("#1F2937"))
        beacon(c, 196, 176, t, hz=1.0, r=5)
        # parked planes at the bow
        crash = (not late) and T["crash"] <= t < s("fix3") - 0.12
        for i, (px, py, rot) in enumerate(self.PARKED if not (late and t >= T["pay"] - 0.2) else ()):
            if crash:
                a_ = t - T["crash"]
                k = e_out(clamp(a_ / 0.4))
                rng2 = random.Random(i)
                px, py, rot = px + rng2.uniform(10, 60) * k, py + rng2.uniform(-50, 50) * k, rot + rng2.uniform(-40, 40) * k
            jet_top(c, px, py, 0.45, rot, col="#94A3B8")
        if late:                                                                    # the reveal: sixty-odd aircraft
            for i, (px, py, rot) in enumerate(self.spots):
                k = prog(t, T["pay"] - 0.2 + i * 0.025, T["pay"] + 0.1 + i * 0.025)
                if k > 0:
                    jet_top(c, px, py, 0.32 * e_back(k), rot, col="#A7B0BF")
            if T["launch"] - 0.3 <= t < s("reveal"):                                 # a jet waits on the catapult
                jet_top(c, 300, -60, 0.5, 0, col=JETC, burn=0.5)
                v2.smoke(c, 280, -60, t, T["launch"] - 0.3, None, rate=8, life=1.2, spread=(40, -10), rise=0, size=(8, 30),
                         col="#FFFFFF", lit=None, lit_until=0.0, seed=41, a=0.6)
            if pk > 0 and pk < 1:                                                   # the paint roller
                rx = 780 - 1560 * pk
                c.drawRect(R(rx - 10, -240, 20, 480), P(HILITE, 0.9))
                c.drawRect(R(rx - 26, -250, 52, 20), P("#334155"))
            c.restore()
            self.ui["cam"] = cam
            return
        # break3: misses every cable and slams into the parked planes
        if s("break3") - 0.2 <= t < s("fix3") - 0.12:
            v = 1100.0
            if t < T["crash"]:
                x = 440 - v * (T["crash"] - t)
                if x > -1100:
                    jet_top(c, x, 0, 0.75, 0, hook=1.0, t=t, burn=0.4)
                    for i in range(4):                                              # the hook skips over the cables
                        cxx = -650 + 110 + i * 46
                        if abs((x - 85) - cxx) < 22:
                            add_glow(c, cxx, 0, 50, HILITE, 0.8)
            else:
                a_ = t - T["crash"]
                jet_top(c, 440 + 30 * e_out(clamp(a_ / 0.3)), 6, 0.75, 18 * e_out(clamp(a_ / 0.3)), t=t, col="#9CA3AF")
                v2.smoke(c, 500, 0, t, T["crash"], T["crash"] + 0.5, rate=24, life=1.6, spread=(160, -60), rise=0,
                         size=(20, 90), col="#6B7280", lit="#FF8A3D", lit_until=0.5, seed=43, a=0.8)
                ring_marks(c, 470, -40, t, a=1 - prog(a_, 2.0, 2.4))
        # fix3: along the angled strip, misses, hits the gas and takes off again
        if s("fix3") - 0.12 <= t < s("break4"):
            tb = T["bolter"]
            dd = 150 + 900 * (t - tb)
            if t >= T["gas"]:
                g = t - T["gas"]
                dd = 150 + 900 * (T["gas"] - tb) + 900 * g + 300 * g * g
                if dd > L:                                                          # airborne: slower on screen, climbing
                    gl = (L - 150 - 900 * (T["gas"] - tb)) / 900.0
                    g0 = max(0.0, min(g, gl))
                    dd = L + 420 * (g - g0)
            if dd > -700:
                x, y = x0 + ux * dd, y0 + uy * dd
                air = prog(dd, L - 120, L + 200)
                jet_top(c, x, y, 0.75 * (1 + 0.35 * air), math.degrees(math.atan2(uy, ux)), hook=1.0 - air, t=t,
                        burn=0.35 + 0.65 * prog(t, T["gas"] - 0.05, T["gas"] + 0.2), shadow=air)
        c.restore()
        self.ui["cam"] = cam

    def ui_top(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw >= s("cta") + 0.05:
            if s("reveal") - 0.1 <= tw < T["s1"] - 0.3:
                x0, y0 = self.at(196, 176)
                self.label(x0, y0, 300, 560, "gray", T["gray"] - 0.1, T["s1"] - 0.35, "#CBD5E1")
                self.chip(760, 470, "sixty", T["sixty"] - 0.05, T["s1"] - 0.35, accent=HILITE, size=40)
            return
        if tw < s("fix3") - 0.12:
            self.chip(540, 470, "miss", T["misses"], T["crash"] + 0.6, accent=WARN, size=38)
            x0, y0 = self.at(560, -96)
            self.label(x0, y0, 780, 560, "parked", T["planes"] - 0.1, s("fix3") - 0.15, "#E5E7EB")
            self.badge("alert", T["crash"] + 0.1, s("fix3") - 0.2, x=880, y=360)
            self.red(T["crash"], 2.2)
            return
        (x0, y0), (x1, y1), (ux, uy), (nx, ny), L = self.strip(self.angle.at(tw))
        ax, ay = self.at(x0 + ux * 640 + nx * 70, y0 + uy * 640 + ny * 70)
        self.label(ax, ay, 300, 470, "angled", T["landing"], T["gas"] - 0.1, HILITE)
        self.chip(540, 560, "again", T["takes"] - 0.05, s("break4") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["takes"] + 0.2, s("break4") - 0.15, x=900, y=360)

    # ------------------------------------------------------------------ set: the street (tag)
    def park_x(self, t):
        T = self.T
        if t < T["pilots"]:
            return 260.0
        u = t - T["pilots"]
        base = lerp(260.0, -100.0, e_out(clamp(u / 0.9)))
        return base + (55 * math.sin((u - 0.9) * 7.5) if u > 0.9 else 0.0)

    def draw_street(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["street"].at(t)
        cx, cy, z = cam
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0B1030", "#2B2466", "#74406F"], [0.0, 0.5, 0.8]))
        v2.stars(c, W, H, t, 0.6)
        self.view(c, cam)
        skyline_night(c, cx - 760 / z, cx + 760 / z, -40, seed=6, hmin=260, hmax=760, t=t)
        c.drawRect(R(cx - 760 / z, -40, 1520 / z, 40), P("#4B5563"))
        c.drawRect(R(cx - 760 / z, -42, 1520 / z, 6), P("#9CA3AF"))
        c.drawRect(R(cx - 760 / z, 0, 1520 / z, 900), lin_paint(0, 0, 0, 500, ["#262B3A", "#0F1220"]))
        for xx in range(int(cx - 760 / z) // 160 * 160, int(cx + 760 / z), 160):
            c.drawRect(R(xx, 40, 80, 8), P("#FDE68A", 0.5))
        for lx in (-560, 380):                                                       # street lamps
            c.drawRect(R(lx - 5, -360, 10, 320), P("#475569"))
            c.drawRRect(rr(lx - 30, -372, 60, 16, 8), P("#475569"))
            add_glow(c, lx, -350, 180, "#FDE68A", 0.25)
        px = self.park_x(t)
        u = t - T["pilots"]
        bumpA = u > 0.9 and math.sin((u - 0.9) * 7.5) < -0.96
        bumpB = u > 0.9 and math.sin((u - 0.9) * 7.5) > 0.96
        car(c, -360, 0, 220, "#3B82F6", t, flash=1.0 if bumpA else 0.0)
        car(c, 160, 0, 220, "#22C55E", t, flash=1.0 if bumpB else 0.0)
        car(c, px, 0, 200, "#EF4444", t, pilot=True)
        if self.rtl and t >= T["pk2"] - 0.2:                                        # an hour goes by
            k = prog(t, T["pk2"] - 0.2, T["pk2"] + 0.1)
            c.save()
            c.translate(px, -190)
            c.scale(e_back(k), e_back(k))
            c.drawCircle(0, 0, 40, P("#F8FAFC"))
            c.drawCircle(0, 0, 40, P("#1F2937", 1, stroke=5))
            q = t * 12
            c.drawLine(0, 0, math.cos(q) * 30, math.sin(q) * 30, P("#1F2937", 1, stroke=5))
            c.drawLine(0, 0, math.cos(q / 12) * 20, math.sin(q / 12) * 20, P(WARN, 1, stroke=6))
            c.restore()
        c.restore()
        self.ui["cam"] = cam

    def ui_street(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 470, "landship", T["night"] - 0.1, T["pk2"] - 0.2, accent=GOOD, size=36)
        self.chip(540, 470, "parking", T["pk2"] - 0.1, self.duration, accent=WARN, size=44)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (T["runway"] - 0.25, sfx.whoosh(0.6, False, 61), -8),
              (T["ship"], sfx.thud(0.5, 62), -2), (T["ship"] + 0.05, sfx.clank(300.0, 0.6, 63), -8),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 64), -9)]
        ev += [(T["three"] + 0.15 * i, sfx.pop(65 + i), -6) for i in range(3)]
        ev += [(T["roll0"], jet_snd(1.6, 68), -8), (T["drop"] + 0.42, water_snd(1.0, 69), -3), (T["drop"] + 0.5, sfx.womp(), -8)]
        ev += [(T["catapult"] - 0.2, sfx.clank(500.0, 0.4, 70), -6), (T["fling0"], cat_snd(1.2, 71), -4),
               (T["fling0"] + 0.1, jet_snd(2.0, 72), -6), (T["two"], sfx.ding(), -8), (T["seconds"] + 0.2, sfx.chime(), -6)]
        ev += [(T["coming"] - 0.8, jet_snd(1.6, 73), -8), (T["td"], sfx.thud(0.3, 74), -6), (T["td"] + 0.02, sfx.hiss(0.4, 75), -12),
               (T["over"] + 0.42, water_snd(1.0, 76), -3), (T["over"] + 0.5, sfx.alarm(3, 820.0), -11)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 77), -4)]
        ev += [(T["stretch"] + 0.12 * i, sfx.snap(78 + i), -10) for i in range(4)]
        ev += [(T["catch"] - 1.2, jet_snd(1.4, 82), -9), (T["catch"], wire_snd(0.9, 83), -4), (T["catch"], sfx.thunk(84), -4),
               (T["halt"] - 0.1, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, False, 85), -4), (T["crash"] - 0.8, jet_snd(1.0, 86), -9),
               (T["crash"], boom(1.2, 87), -4), (T["crash"] + 0.05, sfx.clank(240.0, 0.6, 88), -6), (T["crash"] + 0.3, sfx.alarm(3, 820.0), -11)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 89), -6), (T["angle"], sfx.whirr(0.8, 140.0, 220.0, 90), -12),
               (T["bolter"] - 0.5, jet_snd(1.2, 91), -9), (T["gas"], sfx.riser(0.8, 92), -8), (T["gas"] + 0.1, jet_snd(1.6, 93), -5),
               (T["takes"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 94), -4), (T["stop"], sfx.power_down(0.8, 95), -8),
               (T["stop"] + 0.3, sfx.ding(), -9), (T["time"], sfx.power_down(0.8, 96), -8), (T["time"] + 0.2, sfx.alarm(2, 820.0), -12)]
        ev += [(T["reactors"] - 0.5, sfx.charge_up(0.8), -9), (T["plant"], sfx.pop(97), -6), (T["sails"] - 0.2, rumble(1.6, 98), -6),
               (T["twenty"], sfx.whirr(1.0, 300.0, 600.0, 99), -14), (T["refuel"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(100), 0), (T["follow"] - 0.15, sfx.pop(101), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 102), -7),
               (T["launch"] - 0.3, sfx.hiss(0.8, 103), -12)]
        ev += [(T["paint"] - 0.1, sfx.whoosh(1.0, True, 104), -10)]
        ev += [(T["pay"] + 0.06 * i, sfx.pop(105 + i), -12) for i in range(8)]
        ev += [(T["s1"], sfx.pop(115), -3), (T["s2"], sfx.pop(116), -3), (T["s3"], sfx.pop(117), -3)]
        ev += [(T["cong2"], sfx.pop(118), -2), (T["cong2"], sfx.sparkle(1.0, 14, 119), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 120), -6)]
        k = 0
        while T["pilots"] + 0.9 + (0.5 + k) * math.pi / 7.5 < self.duration - 0.2 and k < 8:
            ev.append((T["pilots"] + 0.9 + (0.5 + k) * math.pi / 7.5, sfx.thud(0.25, 121 + k), -8))
            k += 1
        ev += [(T["pk2"], honk_snd(), -6), (T["pk2"] + 0.4, honk_snd(), -7)]
        return ev


NEUT_C = "#7DD3FC"
NAME = "carrier"
EPISODE = Carrier
