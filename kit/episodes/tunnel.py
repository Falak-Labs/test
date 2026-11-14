"""Episode 27 - A tunnel boring machine.  v2 look: a city at dusk cut open, four sets with whip cuts.

Sets: city (side cut: the street, houses and cars on top, the yellow machine crawling through the mud below with its
lined tunnel behind it; later every scoop of mud makes the street sink and a house tilts; with the chamber packed with
mud pushing back the street stays level; the cta, the name plate, the stat and the cheer), face (the cutting head from
the front: a normal drill grinds and gets stuck; steel discs appear, roll and crack the rock into chips), side (the
front of the machine cut open: the rubble piles up and buries the head; a giant screw pulls it in and a belt carries it
out; the unlined tunnel caves in; a robot arm sets concrete rings and the jacks push off them), portal (the tag: a car
drives into a tunnel and the phone loses its signal).
Side views: the street is y = 0 and down is positive in the city set; the machine's axis is y = 0 in the side set.
"""
from v2_base import *  # noqa: F401,F403

TBM_Y, TR, SHIELD = 560.0, 110.0, 300.0         # city set: the machine's axis depth, radius and shield length
YEL = "#F2B134"
RINGC = "#A3A9B3"
MUDS = ("#7A5434", "#5E4029", "#45301E", "#2A1C12")
HX, HR = 330.0, 230.0                           # side set: the head's x and the machine's radius
RW = 70.0                                       # side set: one ring's width


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


def car(c, x, y, L=170, col="#EF4444", a=1.0, lights=0.0):
    """A small car from the side, centred on x, wheels on y (facing right)."""
    if a <= 0:
        return
    cab = skia.Path()
    cab.moveTo(x - L * 0.32, y - 46)
    cab.lineTo(x - L * 0.2, y - 80)
    cab.lineTo(x + L * 0.16, y - 80)
    cab.lineTo(x + L * 0.3, y - 46)
    cab.close()
    c.drawPath(cab, P(shade(col, -0.1), a))
    c.drawRRect(rr(x - L * 0.17, y - 75, L * 0.14, 25, 5), P("#BFE6FF", 0.85 * a))
    c.drawRRect(rr(x + L * 0.01, y - 75, L * 0.13, 25, 5), P("#BFE6FF", 0.85 * a))
    c.drawRRect(rr(x - L / 2, y - 52, L, 36, 13), lin_paint(0, y - 52, 0, y - 16, [shade(col, 0.25), col, shade(col, -0.3)], a=a))
    for wx in (x - L * 0.3, x + L * 0.3):
        c.drawCircle(wx, y - 13, 15, P("#111827", a))
        c.drawCircle(wx, y - 13, 6, P("#9CA3AF", a))
    if lights > 0:
        add_glow(c, x + L / 2, y - 40, 70, "#FDE68A", 0.6 * lights * a)


def house(c, x, y, w, h, col, roof, t, a=1.0, seed=0):
    """A small house (or shop) standing on (x, y), centred on x."""
    box(c, x - w / 2, y - h, w, h, col, r=6, a=a)
    path = skia.Path()
    path.moveTo(x - w / 2 - 14, y - h + 4)
    path.lineTo(x, y - h - w * 0.36)
    path.lineTo(x + w / 2 + 14, y - h + 4)
    path.close()
    c.drawPath(path, P(roof, a))
    rng = random.Random(seed)
    for k in range(2):
        for j in range(max(1, int(w / 60))):
            wx = x - w / 2 + 18 + j * 56
            wy = y - h + 22 + k * 60
            if wy + 34 < y - 10:
                c.drawRRect(rr(wx, wy, 30, 34, 4), P("#FDE68A" if rng.random() < 0.7 else "#1F2937", 0.9 * a))
    c.drawRRect(rr(x - 14, y - 50, 28, 50, 4), P(shade(col, -0.45), a))


def tbm_side(c, x, y, r, t, ang=0.0, a=1.0, chamber=0.0, plate=None, plate_k=0.0):
    """The machine from the side: head at x (facing right), axis at y, radius r, back-up gear trailing behind."""
    L = SHIELD * r / TR
    for k in range(5):                                                              # the back-up gear
        bx = x - L - 20 - k * 150 * r / TR
        bw, bh = 132 * r / TR, r * 1.05
        box(c, bx - bw, y - bh / 2, bw, bh, "#4B5563" if k % 2 else "#57606E", r=8 * r / TR, a=a)
        c.drawRect(R(bx - bw, y - 6, bw, 12), P(YEL, 0.75 * a))
        for wx in (bx - bw * 0.8, bx - bw * 0.2):
            c.drawCircle(wx, y + bh / 2 + 6 * r / TR, 9 * r / TR, P("#111827", a))
    c.drawRRect(rr(x - L, y - r, L, 2 * r, 18 * r / TR), lin_paint(0, y - r, 0, y + r, [shade(YEL, 0.35), YEL, shade(YEL, -0.45)], a=a))
    for k in range(1, 4):
        c.drawLine(x - L * k / 4, y - r + 4, x - L * k / 4, y + r - 4, P("#7C5A12", 0.45 * a, stroke=3))
    c.drawRect(R(x - L, y - r * 0.12, L, r * 0.24), P("#1F2937", 0.25 * a))
    if chamber > 0:                                                                  # the chamber, packed with mud
        c.drawRRect(rr(x - L * 0.24, y - r + 8, L * 0.2, 2 * r - 16, 8), P("#8B5E34", 0.95 * chamber * a))
    c.drawRRect(rr(x - 4, y - r - 8, 24 * r / TR, 2 * r + 16, 10), P("#6B7280", a))
    n = 9
    for k in range(n):                                                               # teeth sliding past as it spins
        u = ((k / n + ang / (2 * math.pi)) % 1.0)
        yy = y - r + u * 2 * r
        c.drawRRect(rr(x + 18 * r / TR, yy - 5, 12 * r / TR, 10, 3), P("#E5E7EB", a * (0.4 + 0.6 * math.sin(u * math.pi))))
    if plate and plate_k > 0:                                                        # the name plate on the shield
        k = e_back(plate_k)
        c.save()
        c.translate(x - L * 0.55, y)
        c.scale(k, k)
        wpl = max(150.0, (arabic.width_ar(plate, 40) if arabic.is_ar(plate) else text_width(plate, 36, "Poppins-Black")) + 50)
        c.drawRRect(rr(-wpl / 2, -36, wpl, 72, 16), P("#FFFFFF", a))
        c.drawRRect(rr(-wpl / 2, -36, wpl, 72, 16), P("#F472B6", a, stroke=5))
        word(c, plate, 0, 13, 36, "#BE185D", a)
        c.restore()


def tbm_front(c, r, ang, discs=0.0, t=0.0, a=1.0, stuck=0.0):
    """The cutting head seen from the front, centred at (0, 0).  discs 0..1: steel disc cutters popping in."""
    c.drawCircle(0, 0, r + 26, P("#000000", 0.45, blur=18))
    c.drawCircle(0, 0, r + 12, P(YEL, a))
    c.drawCircle(0, 0, r, rad_paint(-r * 0.3, -r * 0.3, r * 1.4, ["#8B95A5", "#5B6574", "#353C48"], a=a))
    c.save()
    c.rotate(math.degrees(ang))
    for k in range(6):                                                               # spokes
        c.save()
        c.rotate(k * 60)
        c.drawRRect(rr(20, -26, r - 30, 52, 14), lin_paint(0, -26, 0, 26, ["#A3ADBB", "#6B7584", "#424956"], a=a))
        c.drawRect(R(40, -4, r - 70, 8), P("#2B313C", 0.6 * a))
        c.restore()
    if discs < 1:                                                                    # stubby teeth of a normal drill
        for k in range(6):
            q = math.radians(k * 60 + 30)
            c.drawCircle(math.cos(q) * r * 0.8, math.sin(q) * r * 0.8, 14, P("#9CA3AF", (1 - discs) * a))
    if discs > 0:
        idx = 0
        for k in range(6):
            for j, rad in enumerate((70, 125, 180, 235, r - 30)):
                q = math.radians(k * 60 + (j % 2) * 14 - 7)
                kk = clamp(discs * 32 - idx * 0.9)
                idx += 1
                if kk <= 0:
                    continue
                px, py = math.cos(q) * rad, math.sin(q) * rad
                c.save()
                c.translate(px, py)
                c.rotate(k * 60 + 90 + (j % 2) * 14 - 7)
                s_ = e_back(kk)
                c.scale(s_, s_)
                c.drawRRect(rr(-22, -8, 44, 16, 8), lin_paint(0, -8, 0, 8, ["#F8FAFC", "#CBD5E1", "#64748B"], a=a))
                c.drawCircle(0, 0, 5, P("#334155", a))
                c.restore()
    c.drawCircle(0, 0, 54, P("#424956", a))
    c.drawCircle(0, 0, 54, P("#1F2937", a, stroke=6))
    c.drawCircle(0, 0, 18, P(YEL, a))
    c.restore()
    if stuck > 0:
        c.drawCircle(0, 0, r + 12, P(WARN, 0.25 * stuck, stroke=10))


def arrow_h(c, x0, x1, y, w, col, a):
    """A fat horizontal arrow from x0 to x1."""
    if a <= 0:
        return
    d = 1 if x1 > x0 else -1
    head = 1.1 * w
    path = skia.Path()
    path.moveTo(x0, y - w / 2)
    path.lineTo(x1 - d * head, y - w / 2)
    path.lineTo(x1 - d * head, y - w)
    path.lineTo(x1, y)
    path.lineTo(x1 - d * head, y + w)
    path.lineTo(x1 - d * head, y + w / 2)
    path.lineTo(x0, y + w / 2)
    path.close()
    c.drawPath(path, P(col, a))


def phone(c, x, y, bars, t, a=1.0, title="", sub=""):
    """A phone on a call (screen space), centred at (x, y); bars 0..4."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    k = e_back(clamp(a * 1.2))
    c.scale(k, k)
    c.drawRRect(rr(-130, -230, 260, 460, 38), P("#000000", 0.5, blur=16))
    c.drawRRect(rr(-130, -230, 260, 460, 38), P("#111827"))
    c.drawRRect(rr(-116, -214, 232, 428, 28), lin_paint(0, -214, 0, 214, ["#1E3A8A", "#312E81", "#0F172A"]))
    for i in range(4):                                                               # signal bars
        on = clamp(bars - i)
        c.drawRRect(rr(-96 + i * 16, -170 - i * 9, 11, 14 + i * 9, 3), P("#FFFFFF", 0.25 + 0.75 * on))
    if bars <= 0.05:
        c.drawLine(-100, -194, -38, -152, P(WARN, 1, stroke=6))
    c.drawCircle(0, -56, 50, P("#F9A8D4"))
    c.drawCircle(0, -70, 20, P("#FFFFFF", 0.9))
    c.drawRRect(rr(-30, -46, 60, 32, 16), P("#FFFFFF", 0.9))
    if title:
        word(c, title, 0, 40, 26, "#FFFFFF")
    if sub:
        word(c, sub, 0, 80, 22, "#C7D2FE")
    c.drawCircle(0, 160, 32, P("#EF4444"))
    c.drawLine(-14, 160, 14, 160, P("#FFFFFF", 1, stroke=6))
    c.restore()


# ---------------------------------------------------------------------------------------------- sounds
def grind_snd(d=1.4, seed=80):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 300, 2400) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 9 * tt)))
    return sfx._norm(x * sfx._ar(n, 0.05, 0.3) * np.linspace(1.0, 0.4, n), 0.6)


def crunch_snd(d=0.5, seed=81):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 400, 3200) * np.exp(-tt * 9)
    return sfx._norm(x, 0.7)


def ringtone(d=1.2):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sin(2 * np.pi * 880 * tt) * (np.sin(2 * np.pi * 7 * tt) > 0) * (tt % 0.6 < 0.4)
    return sfx._norm(x * sfx._ar(n, 0.01, 0.1), 0.35)


# ====================================================================================== the episode
class Tunnel(EpisodeV2):
    BUILD_NO = 27
    FIRST_SET = "city"
    CLEAR = "#070B1F"
    TITLE = {"en": "TUNNEL BORING MACHINE", "ar_sa": "مكنة حفر أنفاق"}
    EMPH = {"en": ["CONGRATS", "DRILL", "HOUSE", "CRAWLS", "CITIES", "TUNNEL", "BORING", "MACHINE", "ROCK", "HARD",
                   "NORMAL", "GRINDS", "STUCK", "SPINNING", "STEEL", "DISCS", "ROLL", "CRACK", "CHIPS", "DIGS", "BROKEN",
                   "PILES", "BURIES", "GIANT", "SCREW", "RUBBLE", "CONVEYOR", "BELT", "OUT", "CITY", "SOFT", "MUD",
                   "CAVES", "ROBOT", "ARM", "CONCRETE", "RINGS", "PUSHES", "FORWARD", "MOVING", "SCOOP", "STREET",
                   "SINK", "CHAMBER", "PACKED", "PUSHING", "GROUND", "FOLLOW", "BULLET", "TRAIN", "WOMAN'S", "NAME",
                   "LUCK", "DIGGING", "SEVENTEEN", "HUNDRED", "SIX", "THOUSAND", "YOURSELF", "PHONE", "SIGNAL"],
            "ar_sa": ["مبروك", "بريمة", "بيت", "وبتزحف", "المدن", "مكنة", "أنفاق", "الصخر", "ناشف", "العادية", "وتتزنق",
                      "أقراص", "حديد", "بتتدحرج", "وتكسره", "حتت", "بتحفر", "الردم", "بيتكوم", "ويدفن", "حلزونة", "تسحب",
                      "وسير", "يطلعه", "لبرة", "المدينة", "طين", "طري", "يقع", "روبوت", "حلقات", "خرسانة", "تزق", "لقدام",
                      "ماشية", "الشارع", "يهبط", "فتملا", "الأوضة", "بالطين", "يزق", "تابعني", "الطلقة", "سميها", "ست",
                      "الحظ", "احفر", "سبعتاشر", "مية", "تلاف", "بإيدك", "الشبكة", "تقطع", "ألو"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "DRILL"): "بريمة", ("hook", "HOUSE"): "بيت", ("hook", "CRAWLS"): "وبتزحف", ("hook", "CITIES"): "المدن",
        ("hook", "CONGRATS"): "مبروك", ("hook", "TUNNEL"): "مكنة",
        ("break1", "ROCK"): "الصخر", ("break1", "HARD"): "ناشف", ("break1", "NORMAL"): "العادية", ("break1", "GRINDS"): "تلف",
        ("break1", "STUCK"): "وتتزنق",
        ("fix1", "COVER"): "فتركب", ("fix1", "SPINNING"): "بتلف", ("fix1", "DISCS"): "أقراص", ("fix1", "ROLL"): "بتتدحرج",
        ("fix1", "CRACK"): "وتكسره", ("fix1", "CHIPS"): "حتت",
        ("break2", "DIGS"): "بتحفر", ("break2", "BROKEN"): "الردم", ("break2", "PILES"): "بيتكوم", ("break2", "FRONT"): "قدامها",
        ("break2", "BURIES"): "ويدفن",
        ("fix2", "SCREW"): "حلزونة", ("fix2", "PULLS"): "تسحب", ("fix2", "RUBBLE"): "الردم", ("fix2", "CONVEYOR"): "وسير",
        ("fix2", "CARRIES"): "يطلعه", ("fix2", "OUT"): "لبرة",
        ("break3", "CITY"): "المدينة", ("break3", "MUD"): "طين", ("break3", "DIG"): "تحفر", ("break3", "CAVES"): "يقع",
        ("fix3", "ROBOT"): "روبوت", ("fix3", "RINGS"): "حلقات", ("fix3", "BEHIND"): "ورا", ("fix3", "PUSHES"): "تزق",
        ("fix3", "FORWARD"): "لقدام",
        ("break4", "MOVING"): "ماشية", ("break4", "SCOOP"): "تشيل", ("break4", "STREET"): "الشارع", ("break4", "SINK"): "يهبط",
        ("fix4", "CHAMBER"): "الأوضة", ("fix4", "PACKED"): "فتملا", ("fix4", "PUSHING"): "يزق", ("fix4", "GROUND"): "الأرض",
        ("cta", "BREAK"): "توصل", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "NAME"): "سميها", ("reveal", "WOMAN"): "ست", ("reveal", "LUCK"): "الحظ", ("reveal", "CREWS"): "عمال",
        ("reveal", "DIGGING"): "احفر",
        ("stat", "SEVENTEEN"): "سبعتاشر", ("stat", "HUNDRED"): "مية", ("stat", "SIX"): "ست",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "DIGGING"): "حفرت", ("tag", "CITY"): "البلد", ("tag", "PHONE"): "أول", ("tag", "LOSES"): "تقطع",
        ("tag", "GO"): "تدخل"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a bullet train"),
                   "stat": [("17", "METERS WIDE"), ("100", "METERS LONG"), ("6,000", "TONS")],
                   "L": {"tbm": "YOUR TUNNEL BORING MACHINE", "house": "AS WIDE AS A HOUSE", "hard": "HARD ROCK",
                         "stuck": "STUCK", "discs": "STEEL DISCS", "roll": "THEY ROLL", "chips": "CRACKED INTO CHIPS",
                         "rubble": "RUBBLE", "buried": "BURIED", "screw": "GIANT SCREW", "belt": "CONVEYOR BELT",
                         "mud": "SOFT MUD", "caves": "CAVES IN", "robot": "ROBOT ARM", "rings": "CONCRETE RINGS",
                         "push": "PUSHES OFF THE RINGS", "sink": "THE STREET SINKS", "chamber": "PACKED WITH MUD",
                         "balance": "PUSHES BACK", "level": "STREET STAYS LEVEL", "wall": "STATION", "name": "BERTHA",
                         "luck": "FOR GOOD LUCK", "nosignal": "NO SIGNAL", "hello": "HELLO? HELLO?", "calling": "MOM",
                         "call": "calling..."}},
            "ar_sa": {"follow": ("تابعني", "الجاي: القطر الطلقة"),
                      "stat": [("17", "متر عرض"), ("100", "متر طول"), ("6,000", "طن")],
                      "L": {"tbm": "مكنة حفر الأنفاق بتاعتك", "house": "عرضها قد بيت", "hard": "صخر ناشف",
                            "stuck": "اتزنقت", "discs": "أقراص حديد", "roll": "بتتدحرج", "chips": "اتكسر حتت",
                            "rubble": "ردم", "buried": "اتدفنت", "screw": "حلزونة كبيرة", "belt": "سير",
                            "mud": "طين طري", "caves": "النفق وقع", "robot": "دراع روبوت", "rings": "حلقات خرسانة",
                            "push": "بتزق فيهم", "sink": "الشارع بيهبط", "chamber": "مليانة طين",
                            "balance": "بيزق قصاد الأرض", "level": "الشارع ثابت", "wall": "محطة", "name": "نفرتيتي",
                            "luck": "عشان الحظ", "nosignal": "مفيش شبكة", "hello": "ألو؟ سامعني؟", "calling": "ماما",
                            "call": "بيتصل..."}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "drill": ("hook", "DRILL", 0.1), "house": ("hook", "HOUSE", 0.3), "crawls": ("hook", "CRAWLS", 0.45),
            "cities": ("hook", "CITIES", 0.6), "congrats": ("hook", "CONGRATS", 0.7), "tbm": ("hook", "TUNNEL", 0.9),
            "rock": ("break1", "ROCK", 0.1), "hard": ("break1", "HARD", 0.3), "normal": ("break1", "NORMAL", 0.5),
            "grinds": ("break1", "GRINDS", 0.7), "stuck": ("break1", "STUCK", 0.92),
            "cover": ("fix1", "COVER", 0.1), "spinning": ("fix1", "SPINNING", 0.25), "discs": ("fix1", "DISCS", 0.45),
            "roll": ("fix1", "ROLL", 0.6), "crack": ("fix1", "CRACK", 0.8), "chips": ("fix1", "CHIPS", 0.95),
            "digs": ("break2", "DIGS", 0.1), "broken": ("break2", "BROKEN", 0.35), "piles": ("break2", "PILES", 0.55),
            "front": ("break2", "FRONT", 0.7), "buries": ("break2", "BURIES", 0.9),
            "screw": ("fix2", "SCREW", 0.15), "pulls": ("fix2", "PULLS", 0.3), "rubble": ("fix2", "RUBBLE", 0.4),
            "belt": ("fix2", "CONVEYOR", 0.65), "carries": ("fix2", "CARRIES", 0.85), "out": ("fix2", "OUT", 0.95),
            "city": ("break3", "CITY", 0.15), "mud": ("break3", "MUD", 0.45), "dig": ("break3", "DIG", 0.7),
            "caves": ("break3", "CAVES", 0.92),
            "robot": ("fix3", "ROBOT", 0.1), "rings": ("fix3", "RINGS", 0.3), "behind": ("fix3", "BEHIND", 0.45),
            "pushes": ("fix3", "PUSHES", 0.75), "forward": ("fix3", "FORWARD", 0.95),
            "moving": ("break4", "MOVING", 0.1), "scoop": ("break4", "SCOOP", 0.35), "street": ("break4", "STREET", 0.75),
            "sink4": ("break4", "SINK", 0.95),
            "chamber": ("fix4", "CHAMBER", 0.15), "packed": ("fix4", "PACKED", 0.4), "pushing": ("fix4", "PUSHING", 0.6),
            "ground4": ("fix4", "GROUND", 0.9),
            "breakthru": ("cta", "BREAK", 0.2), "follow": ("cta", "FOLLOW", 0.35),
            "woman": ("reveal", "WOMAN", 0.15), "name": ("reveal", "NAME", 0.2), "luck": ("reveal", "LUCK", 0.35),
            "crews": ("reveal", "CREWS", 0.6), "digging": ("reveal", "DIGGING", 0.92),
            "s1": ("stat", "SEVENTEEN", 0.04), "s2": ("stat", "HUNDRED", 0.4), "s3": ("stat", "SIX", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "after": ("tag", "DIGGING", 0.1), "city2": ("tag", "CITY", 0.3), "phone": ("tag", "PHONE", 0.5),
            "loses": ("tag", "LOSES", 0.6), "goin": ("tag", "GO", 0.9)})
        T["stop"] = T["stuck"] - 0.1                                        # break1: the plain drill stops
        T["pk"] = min(T["packed"], T["chamber"]) - 0.1                       # fix4: the chamber fills with mud
        T["plate"] = min(T["woman"], T["name"]) - 0.1
        T["enter"] = min(T["goin"], T["loses"]) - 0.6
        T["drop"] = max(T["goin"], T["loses"]) - 0.1
        T["ring1"] = T["robot"] - 0.2                                        # fix3: two rings placed, two pushes
        T["push1"] = max(T["ring1"] + 1.0, T["pushes"] - 0.3)
        T["ring2"] = T["push1"] + 0.7
        T["push2"] = max(T["ring2"] + 0.8, T["forward"] - 0.2)
        # ---- sets
        self.cut(s("break1") - 0.12, "face", 1)
        self.cut(s("fix1") - 0.12, "face", -1)                     # same set: the stuck drill is swapped for discs
        self.cut(s("break2") - 0.12, "side", 1)
        self.cut(s("fix2") - 0.12, "side", -1)                     # same set: the pile is cleared away
        self.cut(s("break3") - 0.12, "side", 1)
        self.cut(s("fix3") - 0.12, "side", -1)                     # same set: the collapse is cleared, rings appear
        self.cut(s("break4") - 0.12, "city", 1)
        self.cut(s("fix4") - 0.12, "city", -1)                     # same set: the street is level again
        self.cut(s("tag") - 0.2, "portal", 1)
        self.cams = {"city": Camera(-160, 560, 1.5), "face": Camera(0, 100, 1.0), "side": Camera(60, 100, 0.95),
                     "portal": Camera(-60, -250, 1.05)}
        cm = self.cams
        cm["city"].key(0.1, 120, 600, 1.05, max(0.8, T["house"] - 0.1))
        cm["city"].key(T["crawls"], 60, 667, 0.6, max(0.9, T["cities"] - T["crawls"] + 0.6))
        cm["city"].key(s("break4") - 0.12, 250, 520, 0.72, 0.0).key(s("break4"), 260, 470, 0.78, 3.0)
        cm["city"].key(s("fix4") - 0.12, 300, 560, 0.74, 0.0).key(s("fix4"), 320, 560, 0.76, 3.0)
        cm["city"].key(s("cta") - 0.4, 340, 640, 0.62, 1.0)
        cm["city"].key(s("reveal") - 0.1, 220, 600, 1.15, 1.2)
        cm["city"].key(T["s1"] - 0.3, -40, 640, 0.56, 1.0).key(s("closer") - 0.2, 0, 640, 0.58, 1.0)
        cm["face"].key(s("break1"), 0, 100, 1.05, 4.0).key(s("fix1") - 0.12, 0, 100, 1.0, 0.0)
        cm["face"].key(s("fix1"), 0, 100, 1.04, 4.0)
        cm["side"].key(s("break2") - 0.12, 60, 100, 0.95, 0.0).key(s("break2"), 70, 100, 0.97, 3.5)
        cm["side"].key(s("fix2") - 0.12, 20, 100, 0.92, 0.0).key(s("fix2"), -60, 100, 0.92, 3.0)
        cm["side"].key(s("break3") - 0.12, -260, 80, 0.92, 0.0).key(s("break3"), -280, 70, 0.95, 3.0)
        cm["side"].key(s("fix3") - 0.12, -120, 100, 0.92, 0.0)
        cm["portal"].key(s("tag"), -30, -250, 1.08, 3.0)
        # ---- tracks
        self.spin = Track(1.0).to(T["grinds"] - 0.2, 0.5, 0.6).to(T["stop"], 0.0, 0.3)
        self.spin.to(s("fix1") - 0.12, 0.0, 0.0).to(T["spinning"] - 0.1, 2.4, 0.6)
        self.ang = Integral(lambda t: self.spin.at(t), 0, self.tl.duration + 1)
        self.discs = Track(0.0).to(T["discs"] - 0.25, 1.0, 0.7, lambda u: u)
        self.pile = Track(0.0).to(T["broken"] - 0.2, 1.0, max(1.2, T["buries"] - T["broken"] + 0.4), e_io)
        self.clear = Track(1.0).to(T["pulls"] - 0.1, 0.0, max(1.4, T["carries"] - T["pulls"] + 0.6), e_io)
        self.cave = Track(0.0).to(T["dig"] - 0.1, 1.0, max(0.8, T["caves"] - T["dig"] + 0.4), e_in)
        self.adv = Track(0.0).to(T["push1"], RW, 0.6).to(T["push2"], 2 * RW, 0.6)
        self.trough = Track(0.0).to(T["scoop"] - 0.1, 70.0, max(1.0, T["sink4"] - T["scoop"] + 0.4), e_in)
        self.trough.to(s("fix4") - 0.12, 0.0, 0.0)
        self.chamber = Track(0.0).to(T["pk"], 1.0, 0.6)
        self.plate = Track(0.0).to(T["plate"], 1.0, 0.5)
        self.go = Track(0.0).to(T["digging"] - 0.1, 1.0, 0.4)
        self.carx = Track(-700.0).to(T["after"] - 0.2, 140.0, max(1.0, T["enter"] - T["after"] + 0.2), lambda u: u)
        self.carx.to(T["enter"], 340.0, 0.8, lambda u: u)
        self.bars = Track(4.0).to(T["drop"] - 0.2, 0.0, 0.6)
        self.speed = Track(1.0).to(T["digging"], 3.0, 0.6)
        self.dist = Integral(lambda t: 9.0 * self.speed.at(t), 0, self.tl.duration + 1)
        self.spans = [(T["stuck"], T["chips"] + 0.3), (T["buries"], T["out"] + 0.3), (T["caves"], T["forward"] + 0.3),
                      (T["sink4"], T["ground4"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 8), (T["stop"], 0.5, 12), (T["crack"], 0.4, 8), (T["buries"], 0.4, 10),
                       (T["caves"], 0.7, 16), (T["push1"], 0.25, 8), (T["push2"], 0.25, 8), (T["sink4"], 0.6, 12),
                       (T["digging"], 0.3, 8), (s("closer") + 0.2, 0.35, 10), (T["drop"], 0.25, 6)]
        rng = random.Random(27)
        self.houses = [(-1650 + i * 230 + rng.uniform(-30, 30), rng.uniform(150, 210), rng.uniform(150, 330),
                        rng.choice(("#7C3AED", "#2563EB", "#0EA5E9", "#DB2777", "#059669", "#D97706")),
                        rng.choice(("#7F1D1D", "#1E293B", "#312E81"))) for i in range(16)]
        self.rubble = [(rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(10, 22), rng.uniform(0, 360)) for _ in range(70)]

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    def tbm_x(self, t):
        return -60.0 + self.dist.at(t)

    # ------------------------------------------------------------------ set: the city, cut open
    def street_y(self, x, t):
        d = self.trough.at(t)
        if d <= 0:
            return 0.0
        xc = self.tbm_x(t) - 120
        return d * math.exp(-((x - xc) / 240.0) ** 2)

    def draw_city(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.cams["city"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        self.backdrop(c, t, cx, cy, gy, moon=True)
        self.view(c, cam)
        x0, x1 = cx - 760 / z, cx + 760 / z
        tx = self.tbm_x(t)
        ys = [(xx, self.street_y(xx, t)) for xx in range(int(x0) - 40, int(x1) + 80, 30)]
        soil = skia.Path()                                                            # the ground, cut open
        soil.moveTo(ys[0][0], ys[0][1])
        for xx, yy in ys[1:]:
            soil.lineTo(xx, yy)
        soil.lineTo(ys[-1][0], 3000)
        soil.lineTo(ys[0][0], 3000)
        soil.close()
        c.drawPath(soil, lin_paint(0, 0, 0, 1300, [MUDS[0], MUDS[1], MUDS[2], MUDS[3]], [0, 0.3, 0.65, 1]))
        rng = random.Random(3)
        for _ in range(int((x1 - x0) / 50)):
            rx, ry = rng.uniform(x0, x1), rng.uniform(60, 1250)
            c.drawCircle(rx, ry, rng.uniform(6, 18), P("#2A1C12", 0.5))
        for yy_, hh in ((240, 30), (420, 40), (800, 50)):
            c.drawRect(R(x0, yy_, x1 - x0, hh), P("#FFFFFF", 0.035))
        tunnel_l = -2400
        c.drawRect(R(tunnel_l, TBM_Y - TR - 6, tx - SHIELD - tunnel_l, 2 * TR + 12), P("#14161C"))   # the lined tunnel
        k0 = int((tx - SHIELD - tunnel_l) / 44)
        for k in range(k0 + 1):
            rx = tx - SHIELD - (k + 1) * 44
            if rx + 44 < x0 - 50:
                break
            for yy_ in (TBM_Y - TR - 6, TBM_Y + TR - 16):
                c.drawRect(R(rx + 2, yy_, 40, 22), P(RINGC))
            c.drawLine(rx, TBM_Y - TR - 6, rx, TBM_Y + TR + 6, P("#4B5563", 0.8, stroke=2))
        for k in range(6):                                                            # lamps in the tunnel
            lx = tx - SHIELD - 820 - k * 260
            add_glow(c, lx, TBM_Y - TR + 30, 60, "#FDE68A", 0.35)
        wall_x = tx + 330                                                             # the station box ahead
        if t >= s("cta") - 0.6:
            box(c, wall_x, TBM_Y - 260, 520, 520, "#64748B", r=10)
            c.drawRect(R(wall_x + 26, TBM_Y - 230, 468, 460), P("#1E293B"))
            for k in range(4):
                add_glow(c, wall_x + 90 + k * 110, TBM_Y - 200, 50, "#FDE68A", 0.4)
            c.drawRect(R(wall_x + 26, TBM_Y + 150, 468, 30), P("#94A3B8"))
        ang = t * 2.0
        ch = self.chamber.at(t) if t >= s("fix4") - 0.12 else 0.0
        tbm_side(c, tx, TBM_Y, TR, t, ang=ang * 3, chamber=ch, plate=self.L["name"],
                 plate_k=self.plate.at(t) if t >= s("reveal") - 0.2 else 0.0)
        if self.go.at(t) > 0 and t >= s("reveal"):
            v2.smoke(c, tx + 30, TBM_Y, t, T["digging"], T["digging"] + 1.6, rate=20, life=1.0, spread=(120, -30),
                     rise=-10, size=(14, 50), col="#8B6B4A", lit=None, lit_until=0.0, seed=33, a=0.6)
        if ch > 0 and t < s("cta") - 0.4:                                              # pressure: in and back out
            pk = prog(t, T["pushing"] - 0.2, T["pushing"] + 0.3)
            for k, dy in enumerate((-60, 0, 60)):
                arrow_h(c, tx + 220, tx + 70, TBM_Y + dy, 18, "#C08A5A", 0.85 * pk)
                arrow_h(c, tx - 40, tx + 50, TBM_Y + dy, 18, GOOD, 0.9 * pk)
        # the street on top
        st = skia.Path()
        st.moveTo(ys[0][0], ys[0][1] - 4)
        for xx, yy in ys[1:]:
            st.lineTo(xx, yy - 4)
        c.drawPath(st, P("#374151", 1, stroke=26))
        c.drawPath(st, dash_paint("#F8FAFC", 0.6, w=4, t=0.0, dash=30, gap=26))
        for i, (hx, hw, hh, col, roof) in enumerate(self.houses):
            if hx + hw < x0 - 100 or hx - hw > x1 + 100:
                continue
            by = self.street_y(hx, t)
            tilt = math.degrees(math.atan2(self.street_y(hx + 40, t) - self.street_y(hx - 40, t), 80)) * 1.4
            c.save()
            c.translate(hx, by - 14)
            c.rotate(tilt)
            house(c, 0, 0, hw, hh, col, roof, t, seed=i)
            c.restore()
        for k, (sp, col, off) in enumerate(((140, "#EF4444", 0), (-110, "#22D3EE", 700), (90, "#FACC15", 1400))):
            cx_ = (off + t * sp) % 3400 - 1700
            car(c, cx_, self.street_y(cx_, t) - 16, 130, col, lights=1.0)
        if t >= s("break4") - 0.12 and t < s("fix4") - 0.12:                           # cracks in the road
            ck = prog(t, T["street"] - 0.2, T["sink4"] + 0.3)
            xc = tx - 120
            for sd in (-1, 1):
                path = skia.Path()
                path.moveTo(xc + sd * 120, self.street_y(xc + sd * 120, t) - 6)
                for j in range(1, 5):
                    path.lineTo(xc + sd * (120 + j * 20), self.street_y(xc + sd * (120 + j * 20), t) + j * 16 * ck)
                c.drawPath(path, P("#0B0E1A", ck, stroke=4))
        if t >= T["cong2"]:
            for k in range(4):
                v2.shock_ring(c, tx - 700 + k * 300, -300 - (k % 2) * 140, t, T["cong2"] + 0.25 * k, 0.9, r1=170,
                              col=("#FDE68A", "#F472B6", "#7DD3FC", "#A7F3D0")[k], width=7, squash=1.0)
        c.restore()
        self.ui["cam"] = cam

    def ui_city(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        tx = self.tbm_x(tw)
        if tw < s("break1"):
            x0, y0 = self.at(tx - 160, TBM_Y - TR)
            self.label(x0, y0, 330, 1150, "house", T["house"] - 0.1, T["tbm"] - 0.2, HILITE, size=30)
            self.chip(540, 470, "tbm", T["tbm"] - 0.15, s("break1") + 0.2, accent=HILITE, size=34)
            return
        if tw < s("fix4") - 0.12:
            self.chip(540, 470, "sink", T["street"] - 0.1, s("fix4") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["sink4"] + 0.2, s("fix4") - 0.2, x=880, y=330)
            self.red(T["sink4"] + 0.2, 1.8)
            return
        if tw < s("cta") - 0.4:
            x0, y0 = self.at(tx - 60, TBM_Y + 40)
            self.label(x0, y0, 290, 1150, "chamber", T["pk"] + 0.1, s("cta") - 0.4, "#D6A46C", size=30)
            self.chip(540, 470, "balance", T["pushing"] - 0.1, T["ground4"] + 0.2, accent=GOOD, size=36)
            self.chip(540, 470, "level", T["ground4"] + 0.25, s("cta") - 0.4, accent=GOOD, size=38)
            self.badge("check", T["ground4"] + 0.3, s("cta") - 0.4, x=880, y=330)
            return
        if tw < s("reveal") - 0.1:
            x0, y0 = self.at(tx + 590, TBM_Y - 260)
            self.label(x0, y0, 800, 640, "wall", s("cta") - 0.3, s("reveal") - 0.2, "#CBD5E1", size=30)
            return
        if tw < T["s1"] - 0.3:
            self.chip(540, 470, "luck", T["luck"] - 0.1, T["s1"] - 0.35, accent="#F472B6", size=40)

    # ------------------------------------------------------------------ set: the head from the front (break1, fix1)
    def draw_face(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["face"].at(t)
        cx, cy, z = cam
        c.drawRect(R(0, 0, W, H), P("#0C0A0E"))
        self.view(c, cam)
        vrect(c, -900, -1200, 1800, 2600, ["#3A3238", "#4A3F3E", "#2C2428", "#16121A"], [0, 0.35, 0.7, 1])
        rng = random.Random(11)
        for k in range(18):                                                            # strata and old cracks
            yy = -1100 + k * 130 + rng.uniform(-20, 20)
            path = skia.Path()
            path.moveTo(-900, yy)
            for xx in range(-900, 960, 90):
                path.lineTo(xx, yy + math.sin(xx * 0.01 + k) * 14)
            c.drawPath(path, P("#000000", 0.18, stroke=8))
        fixed = t >= s("fix1") - 0.12
        ck = prog(t, T["crack"] - 0.1, T["crack"] + 0.5) if fixed else 0.0
        if ck > 0:                                                                     # the rock cracking around the head
            for k in range(14):
                q = math.radians(k * 360 / 14 + 7)
                path = skia.Path()
                r0 = 350
                path.moveTo(math.cos(q) * r0, math.sin(q) * r0)
                for j in range(1, 6):
                    rr_ = r0 + j * 60 * ck
                    qq = q + math.sin(j * 1.7 + k) * 0.08
                    path.lineTo(math.cos(qq) * rr_, math.sin(qq) * rr_)
                c.drawPath(path, P("#F59E0B", 0.55 * ck, stroke=5))
                c.drawPath(path, P("#0B0B0F", ck, stroke=3))
        add_glow(c, 0, 0, 520, "#FDBA74", 0.18)
        stuck = prog(t, T["stop"], T["stop"] + 0.4) if not fixed else 0.0
        jig = (math.sin(t * 60) * 5 * prog(t, T["grinds"] - 0.3, T["grinds"]) * (1 - stuck)) if not fixed else 0.0
        c.save()
        c.translate(jig, 0)
        tbm_front(c, 330, self.ang.at(t), discs=self.discs.at(t) if fixed else 0.0, t=t, stuck=stuck)
        c.restore()
        if not fixed:
            if T["grinds"] - 0.6 <= t < T["stop"] + 0.2:
                for k in range(3):
                    q = math.radians(200 + k * 70)
                    sparks_shower(c, math.cos(q) * 340, math.sin(q) * 340, t, T["grinds"] - 0.6 + k * 0.25, dur=0.6, n=14,
                                  speed=520, seed=20 + k)
            if t >= T["stop"]:
                v2.smoke(c, 0, -250, t, T["stop"], T["stop"] + 1.4, rate=18, life=1.4, spread=(160, -60), rise=-60,
                         size=(20, 80), col="#6B7280", lit=None, lit_until=0.0, seed=24, a=0.6)
        else:
            if t >= T["roll"] - 0.1:                                                    # chips flying off the rim
                for k in range(10):
                    t0 = T["roll"] - 0.1 + k * 0.28
                    q = math.radians(k * 137 % 360)
                    v2.debris(c, math.cos(q) * 345, math.sin(q) * 345, t, t0, dur=1.0, n=7, speed=420, seed=30 + k,
                              gravity=1300, cols=("#9C8C7E", "#6B5E55", "#C8B7A6"))
        c.restore()
        self.ui["cam"] = cam

    def ui_face(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 470, "hard", T["hard"] - 0.1, T["stuck"] - 0.15, accent="#FDBA74", size=40)
            self.chip(540, 470, "stuck", T["stuck"] - 0.1, s("fix1") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["stop"] + 0.2, s("fix1") - 0.2, x=880, y=330)
            self.red(T["stop"] + 0.2, 1.8)
            return
        x0, y0 = self.at(math.cos(math.radians(-60 + math.degrees(self.ang.at(tw)))) * 235,
                         math.sin(math.radians(-60 + math.degrees(self.ang.at(tw)))) * 235)
        if tw < T["roll"] + 0.9:
            self.label(x0, y0, 780, 350, "discs", T["discs"] + 0.1, T["roll"] + 0.9, "#E5E7EB", size=32)
        self.chip(540, 470, "roll", T["roll"] - 0.05, T["crack"] - 0.1, accent=HILITE, size=38)
        self.chip(540, 470, "chips", T["crack"] - 0.05, s("break2") - 0.15, accent=GOOD, size=38)
        self.badge("check", T["chips"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: the machine cut open (break2..fix3)
    def draw_side(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["side"].at(t)
        cx, cy, z = cam
        c.drawRect(R(0, 0, W, H), P("#120C08"))
        self.view(c, cam)
        phase = 2 if t < s("fix2") - 0.12 else 3 if t < s("break3") - 0.12 else 4 if t < s("fix3") - 0.12 else 5
        adv = self.adv.at(t) if phase == 5 else 0.0
        x0, x1 = cx - 760 / z, cx + 760 / z
        vrect(c, x0, -1400, x1 - x0, 2800, [MUDS[0], MUDS[1], MUDS[2], MUDS[3]], [0, 0.35, 0.7, 1])
        rng = random.Random(6)
        for _ in range(70):                                                           # stones drift back as it advances
            rx = (rng.uniform(-1600, 1600) - adv) % 3200 - 1600
            ry = rng.uniform(-1200, 1200)
            if abs(ry) < HR + 30 and rx < HX + 40:
                continue
            c.drawCircle(rx, ry, rng.uniform(8, 22), P("#2A1C12", 0.55))
        c.drawRect(R(-1700, -HR, HX + 1700, 2 * HR), P("#17191F"))                     # the bore
        tail = -160
        cave = self.cave.at(t) if phase == 4 else 0.0
        if phase in (2, 3, 5):                                                         # concrete rings behind the tail
            for k in range(30):
                rx = tail - RW * (k + 1) - adv
                if phase == 5:
                    rx += 2 * RW
                if rx + RW < x0 - 40:
                    break
                if rx >= tail:
                    continue
                for y0_ in (-HR, HR - 40):
                    c.drawRect(R(rx + 2, y0_, RW - 4, 40), lin_paint(0, y0_, 0, y0_ + 40, [shade(RINGC, 0.2), RINGC, shade(RINGC, -0.3)]))
                c.drawLine(rx, -HR, rx, HR, P("#0B0E14", 0.6, stroke=2))
        if phase == 4:                                                                 # no rings: the mud caves in
            sag = skia.Path()
            sag.moveTo(x0 - 50, -HR - 2)
            for xx in range(int(x0) - 50, int(tail) + 1, 20):
                d = cave * 190 * math.exp(-((xx + 420) / 240.0) ** 2)
                sag.lineTo(xx, -HR + d)
            sag.lineTo(tail, -HR - 2)
            sag.close()
            c.drawPath(sag, lin_paint(0, -HR, 0, -HR + 190, ["#5E4029", "#7A5434"]))
            c.drawPath(sag, P("#2A1C12", 0.8, stroke=4))
            for k in range(14):                                                        # lumps falling in
                t0 = T["dig"] - 0.1 + k * 0.09
                u = prog(t, t0, t0 + 0.7)
                if u <= 0:
                    continue
                fx_ = -420 + ((k * 67) % 300) - 150
                fy = lerp(-HR + 20, HR - 30 - (k % 4) * 22, e_in(u))
                c.drawCircle(fx_, fy, 20 + (k % 3) * 7, P("#8A6440"))
                c.drawCircle(fx_ - 6, fy - 6, 7, P("#B08A62", 0.7))
            mound = cave * 130
            if mound > 1:
                c.drawOval(R(-720, HR - mound, 600, mound * 2), P("#7A5434"))
            for sd in (-1, 1):
                path = skia.Path()
                path.moveTo(-420 + sd * 160, -HR - 10)
                for j in range(1, 6):
                    path.lineTo(-420 + sd * (160 + j * 30), -HR - j * 70 * cave)
                c.drawPath(path, P("#0B0B0F", cave, stroke=5))
        # the machine
        c.drawRect(R(tail, -HR, HX - tail, 30), lin_paint(0, -HR, 0, -HR + 30, [shade(YEL, 0.3), shade(YEL, -0.3)]))
        c.drawRect(R(tail, HR - 30, HX - tail, 30), lin_paint(0, HR - 30, 0, HR, [shade(YEL, 0.1), shade(YEL, -0.45)]))
        c.drawRect(R(HX - 110, -HR + 30, 22, 2 * HR - 60), P("#475569"))              # the bulkhead
        pile = self.pile.at(t) if phase == 2 else 0.0
        clear = self.clear.at(t) if phase == 3 else 0.0
        cham = pile if phase == 2 else clear * 0.9 if phase == 3 else 0.25
        if cham > 0:                                                                   # rubble in the chamber
            c.drawRect(R(HX - 88, HR - 30 - (2 * HR - 60) * cham, 88, (2 * HR - 60) * cham), P("#8B6B4A"))
            rr2 = random.Random(9)
            for _ in range(int(22 * cham)):
                px_, py_ = HX - 80 + rr2.uniform(0, 70), HR - 40 - rr2.uniform(0, (2 * HR - 70) * cham)
                c.drawCircle(px_, py_, rr2.uniform(6, 12), P("#A1846A"))
        sx0, sy0, sx1, sy1 = HX - 100, HR - 70, -40, -70                                # the screw conveyor
        if phase >= 3:
            sk = 1.0 if phase > 3 else prog(t, T["screw"] - 0.2, T["screw"] + 0.3)
            if sk > 0:
                c.save()
                c.translate(sx0, sy0)
                ang = math.degrees(math.atan2(sy1 - sy0, sx1 - sx0))
                Ls = math.hypot(sx1 - sx0, sy1 - sy0)
                c.rotate(ang)
                c.scale(e_out(sk), 1)
                c.drawRRect(rr(0, -30, Ls, 60, 28), P("#334155"))
                path = skia.Path()
                for j in range(int(Ls / 6)):
                    xx = j * 6
                    yy = 22 * math.sin(xx * 0.09 - t * 14 * (1 if phase == 3 else 0.4))
                    (path.moveTo if j == 0 else path.lineTo)(xx, yy)
                c.drawPath(path, P("#CBD5E1", 0.9, stroke=6))
                if phase == 3 and clear > 0.02:
                    for j in range(8):                                                 # rubble riding up the screw
                        u = ((j / 8 + t * 0.9) % 1.0)
                        c.drawCircle(u * Ls, 8 * math.sin(u * 30), 11, P("#A1846A"))
                c.restore()
        belt_y = -90
        c.drawRect(R(x0 - 50, belt_y, -40 - x0 + 50, 16), P("#1F2937"))               # the belt conveyor
        for xx in range(int(x0) - 40, -40, 60):
            c.drawCircle(xx, belt_y + 22, 9, P("#475569"))
        if phase == 3:
            bk = prog(t, T["belt"] - 0.3, T["belt"] + 0.2) * (0.3 + 0.7 * clear)
            for j in range(16):
                u = ((j / 16 + t * 0.35) % 1.0)
                bx = -60 - u * 900
                c.drawCircle(bx, belt_y - 9, 10 + (j % 3) * 3, P("#A1846A", bk))
        jy = (-HR + 70, HR - 70)                                                       # thrust jacks
        ext = 0.0
        if phase == 5:
            for i, tp in enumerate((T["push1"], T["push2"])):
                if tp - 0.05 <= t < tp + 0.9:
                    ext = clamp(self.adv.at(t) - i * RW, 0, RW) * (1 - prog(t, tp + 0.65, tp + 0.9))
        rod_end = tail + RW - ext
        for yy in jy:
            c.drawRRect(rr(HX - 260, yy - 16, 140, 32, 10), P("#64748B"))
            c.drawLine(HX - 260, yy, rod_end + 6, yy, P("#E2E8F0", 1, stroke=12))
            c.drawRect(R(rod_end - 2, yy - 22, 14, 44), P("#94A3B8"))
        arm_busy = False
        if phase == 5:                                                                 # the erector sets a new ring
            for i, (tr_, tp) in enumerate(((T["ring1"], T["push1"]), (T["ring2"], T["push2"]))):
                u = prog(t, tr_, tr_ + 0.9)
                if u <= 0 or t >= tp + 0.6:
                    continue
                shift = clamp(self.adv.at(t) - i * RW, 0, RW)
                for seg, sgn in ((0, -1), (1, 1)):
                    v = clamp(u * 2 - seg)
                    if v <= 0:
                        continue
                    ex = lerp(-60, tail + RW / 2, e_io(v)) - shift
                    ey = sgn * lerp(0, HR - 20, e_io(v))
                    if v < 1:
                        arm_busy = True
                        c.drawLine(-40, 0, ex, ey, P(YEL, 1, stroke=18))
                    c.drawRect(R(ex - (RW - 4) / 2, ey - 20, RW - 4, 40), lin_paint(0, ey - 20, 0, ey + 20, [shade(RINGC, 0.3), RINGC, shade(RINGC, -0.3)]))
        if not arm_busy:
            c.drawLine(-40, 0, -100, 0, P(YEL, 1, stroke=18))
        c.drawCircle(-40, 0, 18, P("#334155"))
        # the head
        spin_on = 1.0 if phase != 2 else 1 - prog(t, T["buries"] - 0.3, T["buries"] + 0.2)
        c.drawRect(R(HX, -HR - 10, 26, 2 * HR + 20), P("#6B7280"))
        for k in range(9):
            u = ((k / 9 + t * 0.6 * spin_on) % 1.0)
            yy = -HR + u * 2 * HR
            c.drawCircle(HX + 30, yy, 10, P("#E5E7EB", 0.4 + 0.6 * math.sin(u * math.pi)))
        front = pile if phase == 2 else clear if phase == 3 else 0.0
        if front > 0:                                                                  # the rubble piling up in front
            for (u, v, rad, rot) in self.rubble:
                if v > front:
                    continue
                px_ = HX + 30 + u * 140 * (1.2 - v)
                py_ = HR + 10 - v * (2 * HR + 60)
                c.drawCircle(px_, py_, rad, P("#8B6B4A"))
                c.drawCircle(px_ - rad * 0.3, py_ - rad * 0.3, rad * 0.4, P("#B49A7E", 0.6))
        c.restore()
        self.ui["cam"] = cam
        self.ui["phase"] = phase

    def ui_side(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.ui.get("phase", 2)
        if ph == 2:
            x0, y0 = self.at(HX + 80, HR - 60)
            self.label(x0, y0, 820, 1150, "rubble", T["broken"] + 0.1, s("fix2") - 0.15, "#D6B892", size=32)
            self.chip(540, 470, "buried", T["buries"] - 0.1, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["buries"] + 0.2, s("fix2") - 0.2, x=880, y=330)
            self.red(T["buries"] + 0.2, 1.8)
            return
        if ph == 3:
            x0, y0 = self.at(HX - 140, 90)
            self.label(x0, y0, 790, 470, "screw", T["screw"], s("break3") - 0.15, "#CBD5E1", size=32)
            x1, y1 = self.at(-500, -90)
            self.label(x1, y1, 290, 640, "belt", T["belt"], s("break3") - 0.15, HILITE, size=32)
            self.badge("check", T["out"] + 0.1, s("break3") - 0.15, x=880, y=330)
            return
        if ph == 4:
            self.chip(540, 470, "mud", T["mud"] - 0.1, s("fix3") - 0.15, accent="#D6A46C", size=40)
            self.chip(540, 1150, "caves", T["caves"] - 0.1, s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["caves"] + 0.2, s("fix3") - 0.2, x=880, y=330)
            self.red(T["caves"] + 0.2, 1.8)
            return
        x0, y0 = self.at(-40, 0)
        self.label(x0, y0, 290, 470, "robot", T["robot"], T["pushes"] - 0.2, HILITE, size=32)
        x1, y1 = self.at(-200, HR - 20)
        self.label(x1, y1, 300, 1150, "rings", T["rings"], s("break4") - 0.15, "#E5E7EB", size=32)
        self.chip(540, 470, "push", T["pushes"] - 0.1, s("break4") - 0.15, accent=GOOD, size=36)
        self.badge("check", T["forward"] + 0.2, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: the tunnel portal (the tag)
    def draw_portal(self, c, t):
        T = self.T
        cam = self.cams["portal"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        self.backdrop(c, t, cx, cy, gy, moon=True)
        self.view(c, cam)
        v2.ground(c, cx - 760 / z, cx + 760 / z, surface="#3F4656")
        c.drawRect(R(cx - 760 / z, -24, 1520 / z, 24), P("#374151"))
        for xx in range(int(cx - 760 / z), int(cx + 760 / z), 60):
            c.drawRect(R(xx, -14, 30, 4), P("#F8FAFC", 0.6))
        hill = skia.Path()                                                             # the hill
        hill.moveTo(40, 0)
        hill.cubicTo(120, -420, 420, -700, 1300, -640)
        hill.lineTo(1300, 0)
        hill.close()
        c.drawPath(hill, lin_paint(0, -700, 0, 0, ["#2F5D3A", "#1E3F28", "#132818"]))
        for k in range(4):                                                             # trees on the hill
            tx_ = 520 + k * 150
            ty_ = -620 - (k % 2) * 20
            c.drawRect(R(tx_ - 6, ty_, 12, 40), P("#3F2A1A"))
            c.drawCircle(tx_, ty_ - 10, 40, P("#2E7D4F"))
        ax_, at_ = 330, -560                                                           # the cell tower and its signal
        lattice(c, ax_, at_, at_ - 200, w=26, col="#94A3B8")
        beacon(c, ax_, at_ - 206, t, r=5)
        sig = clamp(self.bars.at(t) / 4)
        for k in range(3):
            u = ((t * 0.8 + k / 3) % 1.0)
            rad = 40 + u * 220
            path = skia.Path()
            path.addArc(R(ax_ - rad, at_ - 200 - rad, 2 * rad, 2 * rad), 200, 140)
            c.drawPath(path, P("#7DD3FC", 0.7 * (1 - u) * sig, stroke=6))
        px_, pw, ph = 300, 300, 290                                                    # the portal, facing us
        arch = skia.Path()
        arch.moveTo(px_ - pw / 2, 0)
        arch.lineTo(px_ - pw / 2, -ph + pw / 2)
        arch.arcTo(R(px_ - pw / 2, -ph, pw, pw), 180, 180, False)
        arch.lineTo(px_ + pw / 2, 0)
        arch.close()
        c.save()
        c.translate(px_, 0)
        c.scale(1.18, 1.12)
        c.translate(-px_, 0)
        c.drawPath(arch, lin_paint(0, -ph, 0, 0, ["#CBD5E1", "#94A3B8", "#64748B"]))
        c.restore()
        c.drawPath(arch, rad_paint(px_, -60, 260, ["#000000", "#05070C", "#111827"]))
        for k in range(4):
            add_glow(c, px_ - 60 + k * 40, -ph + 60 + k * 30, 18, "#FDE68A", 0.35 * (1 - k * 0.2))
        cx_ = self.carx.at(t)                                                          # the car drives in and is gone
        k = prog(cx_, px_ - 160, px_ + 40)
        if k < 1:
            c.save()
            c.translate(cx_, -6)
            c.scale(1 - 0.45 * k, 1 - 0.45 * k)
            car(c, 0, 0, 170, "#EF4444", a=1 - k, lights=1.0)
            c.restore()
        c.restore()
        self.ui["cam"] = cam

    def ui_portal(self, c, t, tw):
        T = self.T
        p = self.span(T["phone"] - 0.3, self.duration, 0.3, 0.1)
        if p > 0:
            phone(c, 250, 620, self.bars.at(tw), tw, p, self.L["calling"], self.L["call"])
        self.chip(540, 1150, "nosignal", T["drop"] + 0.2, self.duration, accent=WARN, size=40)
        hk = self.span(T["drop"] + 0.5, self.duration, 0.2, 0.1)
        if hk > 0:
            x0, y0 = self.at(150, -330)
            v2.chip(c, max(250, x0), y0 - 60, self.L["hello"], hk, accent=HILITE, size=34)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, sfx.whirr(2.0, 90.0, 140.0, 61), -14),
              (T["crawls"], rumble(1.6, 62), -10), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 63), -9),
              (T["tbm"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 64), -4), (s("break1"), sfx.whirr(1.6, 120.0, 90.0, 65), -10),
               (T["grinds"] - 0.6, grind_snd(1.4, 66), -6), (T["stop"], sfx.power_down(0.8, 67), -6),
               (T["stop"] + 0.1, sfx.clank(240.0, 0.5, 68), -8), (T["stop"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -5)]
        ev += [(T["discs"] - 0.25 + 0.06 * i, sfx.pop(70 + i), -12) for i in range(10)]
        ev += [(T["spinning"] - 0.1, sfx.whirr(2.4, 140.0, 260.0, 80), -10), (T["crack"], crunch_snd(0.6, 81), -5),
               (T["crack"] + 0.4, crunch_snd(0.5, 82), -8), (T["chips"] + 0.1, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 83), -4), (T["broken"], crunch_snd(0.5, 84), -9),
               (T["piles"], crunch_snd(0.6, 85), -8), (T["buries"], sfx.thud(0.5, 86), -5), (T["buries"] + 0.1, sfx.power_down(0.8, 87), -8),
               (T["buries"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 88), -5), (T["screw"] - 0.2, sfx.whirr(2.0, 100.0, 180.0, 89), -10),
               (T["belt"] - 0.2, sfx.hum(1.6, 110.0), -14), (T["out"] + 0.1, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 90), -4), (T["dig"], rumble(1.4, 91), -6),
               (T["caves"], sfx.thud(0.6, 92), -4), (T["caves"] + 0.1, crunch_snd(0.6, 93), -6), (T["caves"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 94), -5)]
        for tr_ in (T["ring1"], T["ring2"]):
            ev += [(tr_ + 0.2, sfx.whirr(0.5, 200.0, 300.0, 95), -12), (tr_ + 0.45, sfx.clank(500.0, 0.3, 96), -8),
                   (tr_ + 0.9, sfx.clank(460.0, 0.3, 97), -8)]
        ev += [(T["push1"], sfx.hiss(0.5, 98), -10), (T["push1"] + 0.1, sfx.thunk(99), -6), (T["push2"], sfx.hiss(0.5, 100), -10),
               (T["push2"] + 0.1, sfx.thunk(101), -6), (T["forward"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 102), -4), (T["scoop"], rumble(1.6, 103), -8),
               (T["street"], sfx.creak(1.0, 104), -8), (T["sink4"], sfx.thud(0.5, 105), -6), (T["sink4"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 106), -5), (T["pk"], sfx.hiss(0.6, 107), -10),
               (T["pushing"], sfx.riser(0.8, 108), -10), (T["ground4"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(109), 0), (T["follow"] - 0.15, sfx.pop(110), -4), (s("cta") + 0.1, rumble(1.8, 111), -12)]
        ev += [(T["plate"], sfx.pop(112), -5), (T["plate"] + 0.1, sfx.sparkle(0.8, 10, 113), -8), (T["luck"], sfx.chime(), -9),
               (T["digging"], sfx.whirr(1.6, 120.0, 260.0, 114), -8), (T["digging"] + 0.1, rumble(1.4, 115), -8)]
        ev += [(T["s1"], sfx.pop(116), -3), (T["s2"], sfx.pop(117), -3), (T["s3"], sfx.pop(118), -3)]
        ev += [(T["cong2"], sfx.pop(119), -2), (T["cong2"], sfx.sparkle(1.0, 14, 120), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 121), -6), (T["phone"] - 0.3, ringtone(1.2), -10),
               (T["enter"], sfx.whoosh(0.8, False, 122), -10), (T["drop"], sfx.power_down(0.6, 123), -9),
               (T["drop"] + 0.5, sfx.beep(1200.0, 0.12), -12), (T["drop"] + 0.75, sfx.beep(1200.0, 0.12), -12)]
        return ev


NAME = "tunnel"
EPISODE = Tunnel
