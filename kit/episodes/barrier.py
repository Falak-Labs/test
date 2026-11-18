"""Episode 41 - The Dutch storm surge barrier (Maeslantkering, Rotterdam).  v2 look: a stormy North Sea at dusk, the
river seen from above, two white steel arms that swing shut.

Sets: river (hook: from above, two arms longer than two football fields swing out of their docks and close the river
while a storm hits from the sea; the reveal: a computer watches the sea and closes them by itself; the stat; the
closer), surge (break1: in section, the land below the sea, the storm pushes the sea up the river into Rotterdam), dam
(fix1: a dam slams across the river; break2: ships pile up at it, the road to Europe's biggest port is shut), docks
(fix2: the two hollow gates wait open in dry docks; break3: each is heavier than a thousand elephants, a door hinge
snaps; fix3: the docks flood, the gate floats and swings out on a ball joint like a shoulder), sink (break4: in section,
a floating gate bobs and the sea slips under it; fix4: water in, it sinks to the bottom, a 22 m steel wall; the cta),
tag (English: Dutch riders on old bikes race into the storm, the headwind championship; Arabic: at the first cloud the
family loads the coffee pot and heads out to the desert).
World (river, dam, docks): seen from above, the river runs up the screen (the sea at the top), x = 0 mid-river,
banks at x = +-RW; the right arm turns about J (the ball joint), the left arm is its mirror image.
"""
from v2_base import *  # noqa: F401,F403
from panama import cargo_ship, ship_top, water as water_side, rain, rain_cloud  # noqa: E402

STORM = {"top": "#070B1C", "upper": "#151C3A", "mid": "#33385E", "low": "#6B5A7A", "horizon": "#B98A86",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
RW = 360.0                                # half width of the river
GH = 205.0                                # half length of one gate
J = (560.0, 120.0)                        # the right ball joint (top view)
GC = (205.0, 0.0)                         # the right gate's centre when closed
RIVER, RIVER_D = "#1F5E86", "#0C2C47"
SEA_C = "#173E5E"
LAND, LAND_D = "#3F5A3A", "#24361F"
WHITE = "#EEF2F7"


def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def rot(px, py, ox, oy, ang):
    """Point (px, py) turned by ang degrees about (ox, oy) (screen coordinates, y down)."""
    a = math.radians(ang)
    dx, dy = px - ox, py - oy
    return ox + dx * math.cos(a) - dy * math.sin(a), oy + dx * math.sin(a) + dy * math.cos(a)


def arm_pose(swing, side=1):
    """Gate centre, gate direction and joint for one arm. swing 0 = open (in its dock), 1 = closed across the river."""
    ang = 90.0 * (1 - swing)                                   # open = turned 90 degrees about the joint
    jx, jy = J
    gx, gy = rot(GC[0], GC[1], jx, jy, ang)
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    if side < 0:
        return (-gx, gy), (-ux, uy), (-jx, jy)
    return (gx, gy), (ux, uy), (jx, jy)


def gate_arm(c, swing, side, t, a=1.0, xray=0.0, glow=0.0):
    """One arm from above: the white truss from the ball joint to the curved gate."""
    (gx, gy), (ux, uy), (jx, jy) = arm_pose(swing, side)
    e1 = (gx - ux * GH, gy - uy * GH)
    e2 = (gx + ux * GH, gy + uy * GH)
    for (ex, ey) in (e1, e2):                                  # the truss
        c.drawLine(jx, jy, ex, ey, P(WHITE, a, stroke=16))
    for k in range(1, 6):                                      # cross bracing
        f = k / 6.0
        p1 = (lerp(jx, e1[0], f), lerp(jy, e1[1], f))
        p2 = (lerp(jx, e2[0], f), lerp(jy, e2[1], f))
        c.drawLine(p1[0], p1[1], p2[0], p2[1], P("#CBD5E1", 0.9 * a, stroke=6))
        if k < 5:
            p3 = (lerp(jx, e2[0], (k + 1) / 6.0), lerp(jy, e2[1], (k + 1) / 6.0))
            c.drawLine(p1[0], p1[1], p3[0], p3[1], P("#CBD5E1", 0.7 * a, stroke=4))
    gp = skia.Path()                                           # the gate: a thick curved wall, bulging to the sea
    bulge = 34.0
    pts = []
    for i in range(21):
        s_ = -1 + i / 10.0
        off = bulge * (1 - s_ * s_)
        px = gx + ux * GH * s_
        py = gy + uy * GH * s_
        dx_, dy_ = (jx - px), (jy - py)                        # bulge away from the joint (toward the sea)
        dl = math.hypot(dx_, dy_) or 1.0
        pts.append((px - dx_ / dl * off, py - dy_ / dl * off))
    gp.moveTo(*pts[0])
    for p_ in pts[1:]:
        gp.lineTo(*p_)
    c.drawPath(gp, P("#64748B", a, stroke=40))
    c.drawPath(gp, P(WHITE, a, stroke=26))
    if xray > 0:
        c.drawPath(gp, P("#38BDF8", 0.8 * xray * a, stroke=12))
    if glow > 0:
        add_glow(c, gx, gy, 260, "#FDE68A", 0.4 * glow * a)
    c.drawCircle(jx, jy, 46, rad_paint(jx - 14, jy - 14, 60, ["#F8FAFC", "#94A3B8", "#475569"], a=a))   # ball joint
    c.drawCircle(jx, jy, 46, P("#1E293B", a, stroke=4))


def elephant(c, x, y, s, col, a=1.0):
    c.drawOval(R(x - 10 * s, y - 7 * s, 18 * s, 11 * s), P(col, a))
    c.drawCircle(x + 9 * s, y - 5 * s, 5 * s, P(col, a))
    c.drawLine(x + 13 * s, y - 3 * s, x + 14 * s, y + 6 * s, P(col, a, stroke=2.2 * s))
    for lx in (-7, -2, 3, 7):
        c.drawRect(R(x + lx * s - 1.6 * s, y + 2 * s, 3.2 * s, 6 * s), P(col, a))


def windmill(c, x, y, s, t, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    tower = skia.Path()
    tower.moveTo(-30, 0)
    tower.lineTo(-18, -120)
    tower.lineTo(18, -120)
    tower.lineTo(30, 0)
    tower.close()
    c.drawPath(tower, P("#3B2F2A", a))
    c.save()
    c.translate(0, -120)
    c.rotate(t * 60)
    for k in range(4):
        c.rotate(90)
        c.drawRect(R(-6, -110, 12, 110), P("#E2E8F0", 0.9 * a))
    c.restore()
    c.restore()


def bike_rider(c, x, y, s, t, shirt, a=1.0):
    """A rider on an old upright bike pedalling to the left into the wind (side view)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for wx in (-60, 60):
        c.drawCircle(wx, -40, 38, P("#111827", a, stroke=7))
        ang = t * 4
        c.drawLine(wx, -40, wx + math.cos(ang) * 36, -40 + math.sin(ang) * 36, P("#6B7280", a, stroke=2))
    c.drawLine(-60, -40, 0, -40, P("#1F2937", a, stroke=6))
    c.drawLine(0, -40, -40, -110, P("#1F2937", a, stroke=6))
    c.drawLine(0, -40, 30, -105, P("#1F2937", a, stroke=6))
    c.drawLine(60, -40, 30, -105, P("#1F2937", a, stroke=6))
    c.drawLine(-60, -40, -40, -110, P("#1F2937", a, stroke=6))
    c.drawRect(R(-56, -118, 34, 8), P("#111827", a))                      # handlebar
    lean = -18
    c.save()
    c.translate(30, -110)
    c.rotate(lean)
    c.drawRRect(rr(-16, -78, 32, 80, 14), P(shirt, a))                    # body leaning into the wind
    c.drawCircle(0, -98, 20, P("#E8B48A", a))
    c.drawLine(-6, -60, -66, -14, P(shirt, a, stroke=12))                 # arms to the handlebar
    for i in range(3):                                                    # hair blown back
        c.drawLine(6, -110 + i * 6, 26 + math.sin(t * 20 + i) * 4, -112 + i * 7, P("#F59E0B", a, stroke=4))
    c.restore()
    ph = t * 4
    for k in (0, math.pi):
        fx_, fy_ = math.cos(ph + k) * 18, math.sin(ph + k) * 18
        c.drawLine(30, -100, fx_, -40 + fy_, P("#1F2937", a, stroke=10))
    c.restore()


def dallah(c, x, y, s, a=1.0):
    """An Arabic coffee pot."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    body = skia.Path()
    body.moveTo(-26, 0)
    body.quadTo(-34, -40, -14, -56)
    body.lineTo(-10, -80)
    body.lineTo(10, -80)
    body.lineTo(14, -56)
    body.quadTo(34, -40, 26, 0)
    body.close()
    c.drawPath(body, lin_paint(-30, 0, 30, 0, ["#B45309", "#FBBF24", "#B45309"], a=a))
    c.drawCircle(0, -88, 9, P("#FBBF24", a))
    spout = skia.Path()
    spout.moveTo(-18, -30)
    spout.quadTo(-50, -60, -62, -86)
    c.drawPath(spout, P("#D97706", a, stroke=7))
    c.drawLine(18, -64, 34, -30, P("#B45309", a, stroke=6))
    c.restore()


def suv(c, x, y, s, col="#F8FAFC", a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-130, -90, 260, 70, 16), P(col, a))
    c.drawRRect(rr(-90, -140, 170, 60, 14), P(shade(col, -0.08), a))
    c.drawRRect(rr(-80, -132, 70, 40, 8), P("#93C5FD", 0.85 * a))
    c.drawRRect(rr(0, -132, 70, 40, 8), P("#93C5FD", 0.85 * a))
    c.drawRect(R(-100, -160, 200, 14), P("#4B5563", a))                      # roof rack
    for wx in (-80, 80):
        c.drawCircle(wx, -18, 30, P("#111827", a))
        c.drawCircle(wx, -18, 12, P("#9CA3AF", a))
    c.restore()


# ====================================================================================== the episode
class Barrier(EpisodeV2):
    BUILD_NO = 41
    FIRST_SET = "river"
    CLEAR = "#070B1C"
    TITLE = {"en": "DUTCH STORM BARRIER", "ar_sa": "حاجز العواصف الهولندي"}
    EMPH = {"en": ["CONGRATS", "SWING", "TWO", "STEEL", "ARMS", "LONGER", "FOOTBALL", "FIELDS", "STOP", "SEA", "DUTCH",
                   "STORM", "BARRIER", "QUARTER", "NETHERLANDS", "BELOW", "STORMS", "PUSH", "NORTH", "ROTTERDAM",
                   "WALL", "DAM", "ROAD", "EUROPE'S", "BIGGEST", "PORT", "HOLLOW", "GATES", "DRY", "DOCKS",
                   "HEAVIER", "THOUSAND", "ELEPHANTS", "HINGE", "FLOOD", "FLOAT", "BALL", "JOINT", "SHOULDER",
                   "FLOATING", "BOBS", "SLIPS", "UNDER", "WATER", "SINK", "BOTTOM", "TWENTY-TWO", "FOLLOW", "VENICE",
                   "WOODEN", "PILES", "COMPUTER", "THREE", "BY", "ITSELF", "SIX", "TONNES", "TEN", "YEARS", "REAL",
                   "YOURSELF", "RACE", "OLD", "BIKES", "HEADWIND", "CHAMPIONSHIP"],
            "ar_sa": ["مبروك", "سكرت", "بذراعين", "حديد", "أطول", "ملعبين", "توقف", "البحر", "كذا", "سويت", "حاجز",
                      "العواصف", "الهولندي", "ربع", "هولندا", "تحت", "والعاصفة", "تدف", "روتردام", "طيب", "بسد",
                      "طريق", "السفن", "ميناء", "أوروبا", "بوابتين", "مجوفة", "أحواض", "أثقل", "ألف", "فيل", "مفصلة",
                      "موية", "تطفو", "وتلف", "كورة", "الكتف", "الطافية", "تتهز", "الموج", "تحتها", "تعبيهم",
                      "وينزلون", "القاع", "جدار", "وعشرين", "تابعني", "فينيسيا", "الخشب", "الزر", "للكمبيوتر",
                      "بيرتفع", "ثلاثة", "بروحه", "آلاف", "طن", "للذراع", "عشرة", "سنين", "عاصفة", "جد", "بيدك",
                      "يصد", "تغيم", "الدلة", "البر"]}
    KEYS = {"ar_sa": {
        ("hook", "SWING"): "سكرت", ("hook", "ARMS"): "بذراعين", ("hook", "FOOTBALL"): "ملعبين", ("hook", "STOP"): "توقف",
        ("hook", "CONGRATS"): "مبروك", ("hook", "DUTCH"): "حاجز",
        ("break1", "QUARTER"): "ربع", ("break1", "BELOW"): "تحت", ("break1", "STORMS"): "والعاصفة",
        ("break1", "PUSH"): "تدف", ("break1", "ROTTERDAM"): "روتردام",
        ("fix1", "WALL"): "أسكر", ("fix1", "DAM"): "بسد",
        ("break2", "ROAD"): "طريق", ("break2", "BIGGEST"): "لأكبر", ("break2", "PORT"): "ميناء",
        ("fix2", "HOLLOW"): "مجوفة", ("fix2", "WAIT"): "تنتظر", ("fix2", "DOCKS"): "أحواض",
        ("break3", "HEAVIER"): "أثقل", ("break3", "ELEPHANTS"): "فيل", ("break3", "HINGE"): "مفصلة",
        ("fix3", "FLOOD"): "فتعبي", ("fix3", "FLOAT"): "تطفو", ("fix3", "SWINGS"): "وتلف", ("fix3", "BALL"): "كورة",
        ("fix3", "SHOULDER"): "الكتف",
        ("break4", "FLOATING"): "الطافية", ("break4", "BOBS"): "تتهز", ("break4", "UNDER"): "تحتها",
        ("fix4", "MEET"): "يتقابلون", ("fix4", "WATER"): "موية", ("fix4", "SINK"): "وينزلون", ("fix4", "WALL"): "جدار",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "BUTTON"): "الزر", ("reveal", "COMPUTER"): "للكمبيوتر", ("reveal", "THREE"): "ثلاثة",
        ("reveal", "ITSELF"): "بروحه",
        ("stat", "SIX"): "ستة", ("stat", "TEN"): "عشرة", ("stat", "YEARS"): "سنين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "STORM"): "العاصفة", ("tag", "RACE"): "تغيم", ("tag", "BIKES"): "الدلة", ("tag", "HEADWIND"): "البر"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Venice on wooden piles"),
                   "stat": [("6,800 t", "EACH ARM"), ("10 m", "BALL JOINTS"), ("10 yrs", "TILL ITS FIRST STORM")],
                   "L": {"arms": "TWO STEEL ARMS", "fields": "EACH > 2 FOOTBALL FIELDS", "stop": "STOP THE SEA",
                         "name": "DUTCH STORM BARRIER", "below": "1/4 BELOW SEA LEVEL",
                         "sealvl": "SEA LEVEL", "push": "THE SEA COMES UP THE RIVER", "rdam": "ROTTERDAM",
                         "dam": "WALL IT OFF?", "port": "ROAD TO EUROPE'S BIGGEST PORT", "stuck": "SHIPS STUCK",
                         "hollow": "HOLLOW GATES", "docks": "WAITING IN DRY DOCKS", "heavy": "HEAVIER THAN",
                         "eleph": "1,000 ELEPHANTS", "hinge": "NO HINGE CAN TAKE IT", "flood": "FLOOD THE DOCKS",
                         "float": "THE GATE FLOATS", "joint": "A GIANT BALL JOINT", "shoulder": "LIKE A SHOULDER",
                         "bobs": "IT BOBS ON THE WAVES", "under": "THE SEA SLIPS UNDER", "fill": "LET WATER IN",
                         "sink": "IT SINKS TO THE BOTTOM", "wall22": "A 22 m STEEL WALL", "sea": "SEA SIDE",
                         "city": "CITY SIDE", "pc": "SEA FORECAST", "plus3": "+3 m: CLOSE", "auto": "CLOSES BY ITSELF",
                         "race": "DUTCH HEADWIND CHAMPIONSHIP", "go": "INTO THE STORM!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: فينيسيا على الخشب"),
                      "stat": [("6,800", "طن للذراع"), ("10", "متر عرض الكورة"), ("10", "سنين لين أول عاصفة")],
                      "L": {"arms": "ذراعين حديد", "fields": "كل وحدة أطول من ملعبين", "stop": "توقف البحر",
                            "name": "حاجز العواصف الهولندي", "below": "ربع هولندا تحت البحر",
                            "sealvl": "مستوى البحر", "push": "العاصفة تدف البحر في النهر", "rdam": "روتردام",
                            "dam": "أسكره بسد؟", "port": "طريق أكبر ميناء في أوروبا", "stuck": "السفن واقفة",
                            "hollow": "بوابات مجوفة", "docks": "تنتظر في أحواض", "heavy": "أثقل من",
                            "eleph": "1,000 فيل", "hinge": "ولا مفصلة تشيلها", "flood": "عبّ الأحواض موية",
                            "float": "البوابة تطفو", "joint": "كورة حديد عملاقة", "shoulder": "زي مفصل الكتف",
                            "bobs": "تتهز مع الموج", "under": "البحر يدخل من تحتها", "fill": "عبّيها موية",
                            "sink": "تنزل للقاع", "wall22": "جدار حديد 22 متر", "sea": "جهة البحر",
                            "city": "جهة المدينة", "pc": "توقع البحر", "plus3": "+3 متر: سكّر", "auto": "يسكّر بروحه",
                            "race": "أول غيمة: البر!", "go": "شيل الدلة!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "swing": ("hook", "SWING", 0.08), "arms": ("hook", "ARMS", 0.2), "fields": ("hook", "FOOTBALL", 0.38),
            "stop": ("hook", "STOP", 0.6), "congrats": ("hook", "CONGRATS", 0.72), "dutch": ("hook", "DUTCH", 0.88),
            "quarter": ("break1", "QUARTER", 0.1), "below": ("break1", "BELOW", 0.3), "storms": ("break1", "STORMS", 0.5),
            "push": ("break1", "PUSH", 0.6), "rdam": ("break1", "ROTTERDAM", 0.92),
            "wall": ("fix1", "WALL", 0.3), "dam": ("fix1", "DAM", 0.85),
            "road": ("break2", "ROAD", 0.4), "biggest": ("break2", "BIGGEST", 0.7), "port": ("break2", "PORT", 0.9),
            "hollow": ("fix2", "HOLLOW", 0.3), "wait": ("fix2", "WAIT", 0.5), "docks": ("fix2", "DOCKS", 0.75),
            "heavier": ("break3", "HEAVIER", 0.25), "eleph": ("break3", "ELEPHANTS", 0.5), "hinge": ("break3", "HINGE", 0.8),
            "flood": ("fix3", "FLOOD", 0.12), "float": ("fix3", "FLOAT", 0.3), "swings": ("fix3", "SWINGS", 0.45),
            "ball": ("fix3", "BALL", 0.7), "shoulder": ("fix3", "SHOULDER", 0.92),
            "floating": ("break4", "FLOATING", 0.15), "bobs": ("break4", "BOBS", 0.35), "under": ("break4", "UNDER", 0.85),
            "meet": ("fix4", "MEET", 0.1), "water": ("fix4", "WATER", 0.3), "sink": ("fix4", "SINK", 0.5),
            "wall22": ("fix4", "WALL", 0.8),
            "follow": ("cta", "FOLLOW", 0.35),
            "button": ("reveal", "BUTTON", 0.15), "pc": ("reveal", "COMPUTER", 0.3), "three": ("reveal", "THREE", 0.65),
            "itself": ("reveal", "ITSELF", 0.92),
            "s1": ("stat", "SIX", 0.04), "s2": ("stat", "TEN", 0.4), "s3": ("stat", "YEARS", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "storm": ("tag", "STORM", 0.2), "race": ("tag", "RACE", 0.45), "bikes": ("tag", "BIKES", 0.6),
            "headwind": ("tag", "HEADWIND", 0.85)})
        T["slam"] = max(T["dam"] - 0.35, s("fix1") + 0.1)
        T["snap"] = max(T["hinge"] - 0.1, T["eleph"] + 0.3)
        T["out"] = max(T["swings"] - 0.2, T["float"] + 0.3)
        T["auto"] = max(T["itself"] - 0.9, T["three"] + 0.1)
        # ---- sets
        self.cut(s("break1") - 0.12, "surge", 1)
        self.cut(s("fix1") - 0.12, "dam", -1)
        self.cut(s("fix2") - 0.12, "docks", 1)
        self.cut(s("break4") - 0.12, "sink", -1)
        self.cut(s("reveal") - 0.12, "river", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- the two arms: hook swings them shut, the reveal opens and closes them again
        self.swing_hook = Track(0.0).to(0.05, 0.0, 0.0).to(0.15, 1.0, max(1.5, T["stop"] - 0.15), e_io)
        self.swing_rev = Track(0.2).to(T["auto"], 1.0, max(0.8, s("stat") - 0.2 - T["auto"]), e_io)
        self.storm_hook = Track(0.2).to(0.05, 1.0, 2.5)
        cm = Camera(0, 130, 0.78)
        cm.key(0.05, 0, 120, 0.76, 3.0).key(T["congrats"], 0, 100, 0.7, 2.0)
        cm.key(s("reveal") - 0.12, 0, -150, 0.62, 0.0)
        cm.key(s("stat") - 0.12, 0, 90, 0.64, 0.0)
        cm.key(s("closer") - 0.1, 0, 60, 0.95, 0.0).key(self.duration, 0, 50, 0.98, 2.0)
        self.cam = cm
        self.spans = [(T["rdam"], T["dam"] + 0.3), (T["port"], T["docks"] + 0.3), (T["hinge"], T["shoulder"] + 0.3),
                      (T["under"], T["wall22"] + 0.3)]
        self.shakes = [(T["stop"], 0.4, 8), (T["congrats"], 0.3, 7), (T["push"] + 0.3, 0.6, 8), (T["slam"] + 0.25, 0.4, 12),
                       (T["snap"], 0.35, 10), (T["sink"] + 0.4, 0.4, 9), (s("closer") + 0.2, 0.35, 9)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def landscape(self, c, t, cam, storm=0.0, docks_wet=1.0):
        """Seen from above: the river, the banks, the two docks, the sea at the top, the city at the bottom."""
        cx, cy, z = cam
        vrect(c, 0, 0, W, H, [LAND_D, LAND])
        self.view(c, cam)
        c.drawRect(R(-3000, -3000, 6000, 6000), lin_paint(0, -2000, 0, 2000, [LAND, LAND_D]))
        rng = random.Random(4)
        for i in range(60):                                         # fields and ditches on the banks
            fx_ = rng.choice([-1, 1]) * rng.uniform(RW + 80, 2600)
            fy_ = rng.uniform(-2600, 2600)
            c.drawRect(R(fx_, fy_, rng.uniform(140, 320), rng.uniform(90, 220)),
                       P(rng.choice(["#4D6B3A", "#5B7A43", "#3A5531", "#6B8A4A"]), 0.8))
        for sd in (-1, 1):                                          # the docks, cut into the banks
            dock = skia.Path()
            dock.moveTo(sd * (RW - 4), -540)
            dock.lineTo(sd * 900, -540)
            dock.lineTo(sd * 900, 60)
            dock.lineTo(sd * (RW - 4), 60)
            dock.close()
            c.drawPath(dock, P("#8B95A5"))
            for k in range(1, 8):                                   # dock floor slabs
                c.drawLine(sd * (RW + k * 70), -540, sd * (RW + k * 70), 60, P("#6B7280", 0.6, stroke=3))
            if docks_wet > 0:
                c.drawPath(dock, lin_paint(0, -540, 0, 60, ["#2A6E96", "#15466A"], a=0.92 * docks_wet))
            c.drawPath(dock, P("#CBD5E1", 1, stroke=12))
        c.drawRect(R(-RW, -3000, 2 * RW, 6000), lin_paint(0, -2400, 0, 2400, [SEA_C, RIVER, RIVER_D]))
        for sd in (-1, 1):                                          # stone embankments
            c.drawLine(sd * RW, -3000, sd * RW, -540, P("#94A3B8", 1, stroke=10))
            c.drawLine(sd * RW, 60, sd * RW, 3000, P("#94A3B8", 1, stroke=10))
        for k in range(26):                                         # ripples drifting downstream
            yy = -2600 + ((k * 210 + t * 50) % 5200)
            xx = -RW + 40 + (k * 97) % (2 * RW - 120)
            c.drawLine(xx, yy, xx + 70, yy, P("#93C5FD", 0.25, stroke=4))
        if storm > 0:                                               # the storm rolls in from the sea (top)
            for k in range(14):
                yy = -1800 + k * 70 + math.sin(t * 2 + k) * 10
                c.drawLine(-RW, yy, RW, yy + 20, P("#E0F2FE", 0.35 * storm * (1 - k / 16), stroke=8))
        for i in range(12):                                         # the city at the bottom: roofs and lights
            bx = -1000 + i * 180
            by = 1500 + (i % 3) * 60
            c.drawRect(R(bx, by, 140, 120), P("#475569"))
            add_glow(c, bx + 70, by + 60, 60, "#FDE68A", 0.35)

    # ------------------------------------------------------------------ set: river (hook, reveal, stat, closer)
    def draw_river(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        if hook:
            sw = self.swing_hook.at(t)
            storm = self.storm_hook.at(t)
        elif t < s("closer") - 0.1:
            sw = self.swing_rev.at(t)
            storm = 0.4 + 0.6 * prog(t, T["three"] - 0.3, T["auto"])
        else:
            sw, storm = 1.0, 1.0
        self.landscape(c, t, cam, storm)
        if sw > 0.98 and storm > 0.5:                               # sea side rough, city side calm
            for k in range(10):
                q = (t * 0.8 + k / 10.0) % 1.0
                yy = -40 - q * 500
                c.drawLine(-RW, yy, RW, yy, P("#F8FAFC", 0.45 * (1 - q) * storm, stroke=10))
            splash(c, -120, -40, t, t - (t % 0.9), dur=0.9, n=10, speed=380)
            splash(c, 160, -40, t, t - ((t + 0.45) % 0.9), dur=0.9, n=10, speed=380)
        if hook:                                                    # a ship slips through just before the storm
            shp = prog(t, 0.0, 2.2)
            if shp < 1:
                ship_top(c, 0, lerp(-900, 1500, shp), 190, 760, a=1 - prog(t, 1.8, 2.2))
        fk = self.span(T["fields"] - 0.15, T["congrats"]) if hook else 0.0
        if fk > 0:                                                  # two football pitches beside the arm
            for k in range(2):                                      # 2 x 105 m = one gate, the arm is longer
                px, py = -410 + k * 205, -420
                c.drawRect(R(px, py, 205, 136), P("#16A34A", 0.92 * fk))
                c.drawRect(R(px, py, 205, 136), P("#F8FAFC", fk, stroke=5))
                c.drawLine(px + 102, py, px + 102, py + 136, P("#F8FAFC", fk, stroke=4))
                c.drawCircle(px + 102, py + 68, 26, P("#F8FAFC", fk, stroke=4))
        for sd in (-1, 1):
            gate_arm(c, sw, sd, t, glow=prog(t, T["stop"] - 0.2, T["stop"] + 0.2) * (1 - prog(t, T["stop"] + 0.4, T["stop"] + 1.0)) if hook else 0.0)
        c.restore()
        if storm > 0.2:                                             # rain over the whole picture
            rain(c, -100, W + 100, -200, H, t, a=0.5 * storm, n=70, seed=8)
        self.ui["cam"] = cam
        self.ui["sw"] = sw

    def ui_river(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam.at(tw))
        if tw < s("break1"):
            self.chip(540, 380, "arms", T["swing"] - 0.1, T["fields"] - 0.15, accent="#E2E8F0", size=40)
            self.chip(540, 380, "fields", T["fields"] - 0.15, T["stop"] - 0.1, accent=GOOD, size=36)
            self.chip(540, 380, "stop", T["stop"] - 0.1, T["dutch"] - 0.1, accent=WARN, size=44)
            self.chip(540, 380, "name", T["dutch"] - 0.1, s("break1") + 0.1, accent=HILITE, size=40)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:                # the computer that watches the sea
            k = self.span(T["button"] - 0.1, s("stat") - 0.15)
            if k > 0:
                c.drawRRect(rr(140, 300, 800, 430, 26), P("#0B1220", 0.92 * k))
                c.drawRRect(rr(140, 300, 800, 430, 26), P("#38BDF8", 0.7 * k, stroke=4))
                v2.chip(c, 540, 350, self.L["pc"], k, accent="#38BDF8", size=30)
                y3 = 470
                c.drawLine(190, y3, 890, y3, P("#F87171", 0.8 * k, stroke=4))
                pth = skia.Path()
                gk = prog(tw, T["pc"] - 0.2, T["auto"])
                n = 40
                for i in range(n + 1):
                    u = i / n
                    if u > gk:
                        break
                    xx = 190 + u * 700
                    yy = 680 - 260 * (u ** 1.6) + math.sin(u * 30) * 10
                    (pth.moveTo if i == 0 else pth.lineTo)(xx, yy)
                c.drawPath(pth, P("#38BDF8", k, stroke=6))
                v2.chip(c, 760, 430, self.L["plus3"], self.span(T["three"] - 0.1, s("stat") - 0.15), accent=WARN, size=28)
                v2.chip(c, 540, 780, self.L["auto"], self.span(T["itself"] - 0.2, s("stat") - 0.15), accent=GOOD, size=40)

    # ------------------------------------------------------------------ set: surge (break1)
    def draw_surge(self, c, t):
        T, s = self.T, self.tl.s
        cam = (0, 120, 0.9)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=STORM, horizon_y=gy - 80 * z)
        self.view(c, cam)
        sk = prog(t, T["storms"] - 0.3, T["rdam"])                  # the sea rises
        sea_y = lerp(0, -230, e_io(sk))
        land = skia.Path()                                          # dike and polder, lower than the sea
        land.moveTo(-200, 4000)
        land.lineTo(-200, 40)
        land.lineTo(-140, -110)
        land.lineTo(-60, -110)
        land.lineTo(20, 80)
        land.lineTo(1400, 80)
        land.lineTo(1400, 4000)
        land.close()
        water_side(c, -1400, -140, sea_y, 600, t)
        c.drawRect(R(-1400, 600, 1300, 3400), lin_paint(0, 600, 0, 1400, ["#3D2A1C", "#21160E"]))
        for k in range(6):                                          # storm waves
            wx = -1200 + k * 200 + (t * 160) % 200
            c.drawArc(R(wx, sea_y - 40, 160, 80), 180, 180, False, P("#E0F2FE", 0.6, stroke=6))
        c.drawPath(land, lin_paint(0, -110, 0, 600, ["#4D6B3A", "#3D2A1C", "#21160E"]))
        c.drawLine(-1400, 0, 1400, 0, P(HILITE, 0.7 * prog(t, T["below"] - 0.3, T["below"]), stroke=4))
        for i, hx in enumerate((160, 330, 520, 700)):              # houses and a windmill on the polder
            c.drawRect(R(hx, 10, 90, 70), P(["#B45309", "#9A3412", "#7C2D12", "#B91C1C"][i]))
            tri = skia.Path()
            tri.moveTo(hx - 8, 12)
            tri.lineTo(hx + 45, -40)
            tri.lineTo(hx + 98, 12)
            tri.close()
            c.drawPath(tri, P("#1F2937"))
            c.drawRect(R(hx + 30, 34, 26, 24), P("#FDE68A", 0.9))
        windmill(c, 900, 80, 1.1, t)
        ok = prog(t, T["push"], T["rdam"] + 0.3)                    # water over the dike, up the river into the city
        if ok > 0:
            fl = skia.Path()
            fl.moveTo(-140, sea_y)
            fl.quadTo(-40, sea_y - 10, 20, -20 + 100 * (1 - ok))
            fl.lineTo(1400 * ok + 20, 80)
            fl.lineTo(20, 80)
            fl.close()
            c.drawPath(fl, P("#2B7BBF", 0.75))
            c.drawRect(R(20, 80 - 70 * ok, 1400 * ok, 70 * ok), P("#2B7BBF", 0.6))
        rain_cloud(c, -500, -900, 1.6, t, a=prog(t, T["storms"] - 0.5, T["storms"]), seed=5)
        rain_cloud(c, 100, -980, 1.4, t, a=prog(t, T["storms"] - 0.5, T["storms"]), seed=6)
        rain(c, -900, 900, -900, 200, t, a=prog(t, T["storms"] - 0.4, T["storms"]) * 0.8, n=80)
        c.restore()
        self.ui["cam"] = cam
        self.ui["sea_y"] = sea_y

    def ui_surge(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (0, 120, 0.9))
        self.chip(540, 380, "below", T["quarter"] - 0.1, T["storms"] - 0.1, accent=HILITE, size=40)
        sx, sy = self.at(cam, 600, 0)
        self.chip(sx, sy - 30, "sealvl", T["below"] - 0.1, T["storms"] - 0.1, accent=HILITE, size=26)
        self.chip(540, 380, "push", T["storms"] - 0.1, s("fix1") - 0.15, accent=WARN, size=38)
        self.chip(780, 1150, "rdam", T["rdam"] - 0.2, s("fix1") - 0.15, accent="#E2E8F0", size=36)
        self.badge("alert", T["rdam"] + 0.05, s("fix1") - 0.2, x=880, y=330)
        self.red(T["rdam"] + 0.05, 1.3)

    # ------------------------------------------------------------------ set: dam (fix1, break2)
    def draw_dam(self, c, t):
        T, s = self.T, self.tl.s
        cam = (0, -200, 0.7)
        self.landscape(c, t, cam, storm=0.3)
        dk = e_out(prog(t, T["slam"], T["slam"] + 0.3))             # a wall slams across the river
        if dk > 0:
            c.drawRect(R(-RW - 60, -40 - 30 * dk, 2 * RW + 120, 80), P("#9CA3AF", dk))
            c.drawRect(R(-RW - 60, -40 - 30 * dk, 2 * RW + 120, 80), P("#475569", dk, stroke=6))
        if t >= s("break2") - 0.12:                                 # ships queue up at the wall
            for i in range(4):
                arr = prog(t, s("break2") + i * 0.35, s("break2") + i * 0.35 + 1.2)
                yy = lerp(-1700, -330 - i * 520, e_out(arr))
                xx = (-1) ** i * 120
                ship_top(c, xx, yy, 170, 480, a=arr)
                if arr > 0.95:
                    add_glow(c, xx, yy - 10, 50, "#F87171", 0.6 * (0.5 + 0.5 * math.sin(t * 8 + i)))
        c.restore()
        self.ui["cam"] = cam

    def ui_dam(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break2") - 0.12:
            self.chip(540, 380, "dam", T["wall"] - 0.1, s("break2") - 0.15, accent="#E2E8F0", size=44)
            return
        self.chip(540, 380, "port", T["road"] - 0.2, s("fix2") - 0.15, accent="#93C5FD", size=32)
        self.chip(540, 1150, "stuck", T["biggest"] - 0.1, s("fix2") - 0.15, accent=WARN, size=40)
        self.badge("alert", T["port"] + 0.05, s("fix2") - 0.2, x=880, y=330)
        self.red(T["port"] + 0.05, 1.3)

    # ------------------------------------------------------------------ set: docks (fix2, break3, fix3)
    def draw_docks(self, c, t):
        T, s = self.T, self.tl.s
        cam = (420, -220, 1.05)
        f3 = t >= s("fix3") - 0.12
        wet = prog(t, T["flood"] - 0.2, T["float"]) if f3 else 0.0
        self.landscape(c, t, cam, storm=0.2, docks_wet=wet)
        sw = e_io(prog(t, T["out"], T["shoulder"] + 0.3)) * 0.55 if f3 else 0.0
        bob = math.sin(t * 2.4) * 6 * wet
        c.save()
        c.translate(0, bob)
        xr = self.span(T["hollow"] - 0.2, s("break3") - 0.1) if not f3 else 0.0
        for sd in (-1, 1):
            gate_arm(c, sw, sd, t, xray=xr)
        c.restore()
        c.restore()
        self.ui["cam"] = cam

    def ui_docks(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (420, -220, 1.05))
        if tw < s("break3") - 0.12:
            (gx, gy), _, _ = arm_pose(0.0, 1)
            ax, ay = self.at(cam, gx, gy)
            self.label(ax, ay, 300, 470, "hollow", T["hollow"] - 0.1, T["docks"] - 0.1, "#38BDF8", size=38)
            self.chip(540, 380, "docks", T["docks"] - 0.1, s("break3") - 0.15, accent=GOOD, size=40)
            self.badge("check", T["docks"] + 0.1, s("break3") - 0.15, x=880, y=330)
            return
        if tw < s("fix3") - 0.12:                                    # 1,000 elephants and a snapped hinge
            k = self.span(T["heavier"] - 0.1, s("fix3") - 0.12)
            if k > 0:
                c.drawRRect(rr(60, 560, 960, 560, 30), P("#0B1220", 0.9 * k))
                ek = prog(tw, T["heavier"], T["eleph"] + 0.2)
                n = int(1000 * ek)
                for i in range(n):
                    r_, q = divmod(i, 40)
                    elephant(c, 100 + q * 22.5, 610 + r_ * 20, 0.9, "#CBD5E1", a=k)
                v2.chip(c, 540, 500, self.L["heavy"] + " " + self.L["eleph"], k, accent=WARN, size=36)
            hk = self.span(T["snap"] - 0.3, s("fix3") - 0.12)
            if hk > 0:                                              # a door hinge, snapping
                sn = prog(tw, T["snap"], T["snap"] + 0.3)
                c.save()
                c.translate(540, 1180)
                for sd in (-1, 1):
                    c.save()
                    c.rotate(sd * 25 * sn)
                    c.drawRRect(rr(-90 if sd < 0 else 6, -40, 84, 80, 10), P("#9CA3AF", hk))
                    c.restore()
                c.drawRect(R(-8, -50, 16, 100), P("#6B7280", hk * (1 - sn)))
                c.restore()
                v2.chip(c, 540, 380, self.L["hinge"], self.span(T["hinge"] - 0.1, s("fix3") - 0.15), accent=WARN, size=40)
            self.badge("alert", T["hinge"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["snap"], 1.3)
            return
        self.chip(540, 380, "flood", T["flood"] - 0.1, T["float"] - 0.1, accent="#93C5FD", size=40)
        self.chip(540, 380, "float", T["float"] - 0.1, T["ball"] - 0.1, accent=GOOD, size=40)
        jx, jy = self.at(cam, J[0], J[1])
        self.label(jx, jy, 760, 470, "joint", T["ball"] - 0.1, s("break4") - 0.15, "#E2E8F0", size=34)
        k = self.span(T["shoulder"] - 0.2, s("break4") - 0.15)
        if k > 0:                                                    # inset: a shoulder joint
            c.drawRRect(rr(90, 520, 360, 360, 30), P("#0B1220", 0.9 * k))
            c.drawCircle(270, 650, 60, P("#F8FAFC", k))
            c.drawArc(R(190, 570, 160, 160), 200, 140, False, P("#94A3B8", k, stroke=18))
            c.drawLine(270, 650, 330, 820, P("#E2E8F0", k, stroke=34))
            v2.chip(c, 270, 920, self.L["shoulder"], k, accent=HILITE, size=30)
        self.badge("check", T["shoulder"] + 0.1, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: sink (break4, fix4, cta)
    def draw_sink(self, c, t):
        T, s = self.T, self.tl.s
        cam = (40, 40, 1.6)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=STORM, horizon_y=gy - 30 * z)
        self.view(c, cam)
        fixed = t >= s("fix4") - 0.12
        sk = e_io(prog(t, T["water"], T["sink"] + 0.6)) if fixed else 0.0
        bottom = lerp(100, 170, sk) + (math.sin(t * 2.6) * 8 * (1 - sk))
        top = bottom - 220
        sea_y = lerp(-6, -30, sk)
        city_y = 0.0
        water_side(c, -600, -75, sea_y, 170, t)
        water_side(c, 75, 800, city_y, 170, t)
        if not fixed or sk < 0.9:                                   # water slips under the gate
            gap = max(0.0, 170 - bottom)
            if gap > 4:
                c.drawRect(R(-75, bottom, 150, gap), P("#2B7BBF", 0.94))
                fk = prog(t, T["under"] - 0.4, T["under"]) if not fixed else 1 - sk
                for k in range(4):
                    q = (t * 1.2 + k / 4.0) % 1.0
                    xx = lerp(-200, 260, q)
                    c.drawLine(xx, bottom + gap * 0.5, xx + 50, bottom + gap * 0.5, P("#F8FAFC", 0.8 * fk, stroke=6))
        c.drawRect(R(-800, 170, 1600, 900), lin_paint(0, 170, 0, 700, ["#5B4A3A", "#2A2018"]))
        c.drawRect(R(-110, 160, 220, 18), P("#6B7280"))              # the sill on the river bed
        for k in range(6):                                          # sea-side waves
            wx = -600 + k * 100 + (t * 120) % 100
            c.drawArc(R(wx, sea_y - 26, 80, 50), 180, 180, False, P("#E0F2FE", 0.6, stroke=5))
        c.drawRect(R(-75, top, 150, 220), lin_paint(-75, 0, 75, 0, ["#CBD5E1", WHITE, "#94A3B8"]))
        for i in range(4):                                          # compartments inside the gate
            for j in range(2):
                cell = R(-62 + j * 64, top + 12 + i * 52, 60, 46)
                fill = clamp((sk * 4.2) - (3 - i))                  # water fills from the bottom up
                c.drawRect(cell, P("#1E293B", 0.5))
                if fixed and fill > 0:
                    c.drawRect(R(cell.left(), cell.bottom() - 46 * fill, 60, 46 * fill), P("#38BDF8", 0.85))
                c.drawRect(cell, P("#475569", 1, stroke=2))
        c.restore()
        self.ui["cam"] = cam
        self.ui["top"] = top

    def ui_sink(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (40, 40, 1.6))
        if tw < s("fix4") - 0.12:
            self.chip(540, 380, "bobs", T["bobs"] - 0.2, T["under"] - 0.1, accent="#FDE68A", size=40)
            self.chip(540, 380, "under", T["under"] - 0.1, s("fix4") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["under"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["under"] + 0.05, 1.3)
            return
        if tw < s("cta") - 0.12:
            self.chip(540, 380, "fill", T["water"] - 0.1, T["sink"] - 0.1, accent="#38BDF8", size=40)
            self.chip(540, 380, "sink", T["sink"] - 0.1, T["wall22"] - 0.1, accent=GOOD, size=40)
            self.chip(540, 380, "wall22", T["wall22"] - 0.1, s("cta") - 0.15, accent=HILITE, size=40)
            self.badge("check", T["wall22"] + 0.1, s("cta") - 0.15, x=880, y=330)
        k = self.span(T["wall22"] - 0.1, self.duration + 1)
        if k > 0:
            sx, sy = self.at(cam, -210, -90)
            v2.chip(c, sx, sy - 40, self.L["sea"], k, accent="#93C5FD", size=30)
            cx_, cy_ = self.at(cam, 230, -90)
            v2.chip(c, cx_, cy_ + 10, self.L["city"], k, accent=GOOD, size=30)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:                                            # riders on a storm barrier, into the wind
            v2.sky(c, W, H, 0.0, pal=STORM, horizon_y=1000)
            water_side(c, -10, W + 10, 1000, 1300, t)
            c.drawRect(R(0, 980, W, 60), P("#6B7280"))
            c.drawRect(R(0, 1040, W, 260), lin_paint(0, 1040, 0, 1300, ["#4B5563", "#1F2937"]))
            vrect(c, 0, 1240, W, H - 1240, ["#1F2937", "#0E1218"])
            rk = prog(t, T["race"] - 0.4, T["race"])
            for i, (bx, col) in enumerate(((330, "#F97316"), (640, "#38BDF8"), (900, "#A3E635"))):
                x = bx - rk * 60 * (1 + i * 0.3) + math.sin(t * 3 + i) * 6
                bike_rider(c, x, 985, 1.05, t + i * 0.4, col, a=rk)
            for k in range(40):                                     # wind streaks blowing at them
                q = (t * 1.6 + k / 40.0) % 1.0
                yy = 300 + (k * 53) % 650
                c.drawLine(W * (1 - q) - 300, yy, W * (1 - q) - 180, yy + 10, P("#E0F2FE", 0.35, stroke=3))
            rain(c, -100, W + 100, 0, 1000, t, a=0.7, n=70, seed=4)
        else:                                                       # the first cloud: coffee pot, car, desert
            sk = {"top": "#141C38", "upper": "#2B3560", "mid": "#585C86", "low": "#9A7458", "horizon": "#B98A5E",
                  "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
            v2.sky(c, W, H, 0.0, pal=sk, horizon_y=1050)
            for i in range(3):
                v2.cloud(c, 160 + i * 380, 320 + (i % 2) * 70, 1.4, body="#5B6690", rim="#C7CCE8", a=0.95, seed=i)
            dune = skia.Path()
            dune.moveTo(-20, 1050)
            dune.quadTo(300, 960, 560, 1040)
            dune.quadTo(820, 1110, 1100, 1000)
            dune.lineTo(1100, 1300)
            dune.lineTo(-20, 1300)
            dune.close()
            c.drawPath(dune, lin_paint(0, 960, 0, 1300, ["#B98447", "#8F5E2B", "#6B451D"]))
            vrect(c, 0, 1240, W, H - 1240, ["#6B451D", "#3A2410"])
            ck = prog(t, T["race"] - 0.3, T["race"] + 0.2)
            suv(c, 760, 1180, 1.25, a=ck)
            pk = prog(t, T["bikes"] - 0.3, T["bikes"] + 0.1)
            person(c, 330, 1190, 260, "#F8FAFC", t, pose="walk", face=1, hat="none", hair="#1F2937", pants="#F1F5F9", a=pk)
            if pk > 0:                                              # red-and-white headdress
                hd = skia.Path()
                hd.moveTo(330 - 40, 1190 - 230)
                hd.lineTo(330 + 40, 1190 - 230)
                hd.lineTo(330 + 30, 1190 - 160)
                hd.lineTo(330 - 50, 1190 - 150)
                hd.close()
                c.drawPath(hd, P("#DC2626", pk))
                c.drawRect(R(330 - 42, 1190 - 236, 84, 12), P("#111827", pk))
            dallah(c, 420, 1100, 1.1, a=pk)

    def ui_tag(self, c, t, tw):
        T = self.T
        k = self.span(T["race"] - 0.2, self.duration + 1)
        if k > 0:
            v2.chip(c, 540, 470, self.L["race"], k, accent=HILITE, size=38 if not self.rtl else 46)
        k2 = self.span(T["headwind"] - 0.2, self.duration + 1)
        if k2 > 0:
            v2.chip(c, 540, 600, self.L["go"], k2, accent=GOOD, size=40)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=STORM, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(2.5, 61), -14), (0.1, rumble(2.4, 62), -10), (T["arms"], sfx.creak(1.2), -10),
              (T["fields"], sfx.whoosh(0.6, True, 63), -12), (T["stop"], sfx.clank(140.0, 0.9, 64), -4),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 65), -9), (T["dutch"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["storms"], rumble(2.0, 67), -8),
               (T["push"], sfx.hiss(1.6, 68), -10), (T["rdam"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -4), (T["slam"] + 0.2, sfx.thud(0.6), -4),
               (T["slam"] + 0.25, sfx.clank(120.0, 0.7, 70), -8)]
        ev += [(T["road"], sfx.beep(600.0, 0.3), -14), (T["biggest"], sfx.beep(520.0, 0.4), -12),
               (T["port"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["hollow"], sfx.sparkle(0.6, 8, 72), -10),
               (T["docks"] + 0.1, sfx.ding(), -8), (T["docks"] + 0.3, sfx.chime(), -6)]
        ev += [(T["heavier"], sfx.click(73), -10), (T["eleph"], sfx.thud(0.4), -8), (T["snap"], sfx.snap(74), -4),
               (T["hinge"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["flood"], sfx.hiss(1.6, 75), -12), (T["float"], sfx.creak(1.0), -10), (T["out"], sfx.whoosh(1.0, False, 76), -12),
               (T["shoulder"] + 0.1, sfx.ding(), -8), (T["shoulder"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 77), -4), (T["bobs"], sfx.creak(0.8), -10),
               (T["under"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["water"], sfx.hiss(1.4, 78), -12), (T["sink"] + 0.4, sfx.thud(0.6), -4),
               (T["wall22"] + 0.1, sfx.ding(), -8), (T["wall22"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(79), 0), (T["follow"] - 0.15, sfx.pop(80), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 81), -6), (T["pc"], sfx.beep(1400.0, 0.08), -10),
               (T["three"], sfx.beep(1700.0, 0.12), -8), (T["auto"], sfx.creak(1.2), -10), (T["itself"], sfx.clank(140.0, 0.8, 82), -6)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 83), -6), (T["s1"], sfx.pop(84), -3), (T["s2"], sfx.pop(85), -3),
               (T["s3"], sfx.pop(86), -3)]
        ev += [(T["cong2"], sfx.pop(87), -2), (T["cong2"], sfx.sparkle(1.0, 14, 88), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 89), -6), (T["storm"], sfx.hiss(2.0, 90), -12),
               (T["race"], sfx.pop(91), -6), (T["headwind"], sfx.ding(), -8)]
        return ev


NAME = "barrier"
EPISODE = Barrier
