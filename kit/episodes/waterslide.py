"""Episode 5: The Water Slide.  Build -> break -> fix, four times, keyed to the voiceover words.

Water-park side view. Ground at y=0, up negative. Two slides: the small plastic ramp of the hook, then the big tower
slide (from break2) with two hairpin turns, a closed tube, a run-out lane and a splash pool. Riders move along a slide
by a path parameter u.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bi_base import (Episode, W, H, Track, Camera, clamp, lerp, prog, e_io, e_out, e_in, e_back, bump,  # noqa: E402
                     text, rect, grad_rect, glow, circle, poly, line, mix, shade, world, fx, sfx, ring_pts,
                     WHITE, RED, YELLOW)

RAMP = [(-430, -450), (230, -30)]
BIG = [(-430, -950), (-300, -935), (-150, -880), (150, -700), (290, -615), (335, -560), (290, -505), (140, -455),
       (-150, -330), (-255, -270), (-275, -215), (-200, -170), (200, -100), (640, -42), (700, -40)]
RUN_END = 1120.0
POOL_X1 = 1560
DECK = "#E9DFC9"
FLUME = "#38BDF8"
RAINBOW = ("#EF4444", "#F97316", "#FACC15", "#22C55E", "#3B82F6", "#8B5CF6")
WATER0, WATER1 = "#7DD3FC", "#0EA5E9"

EMPH_EN = ["CONGRATS", "STUCK", "PUMPS", "BUSHES", "TUBE", "CRASHES", "RED", "STONE", "RUNOUT", "FOLLOW",
           "COLOR", "ZERO", "YOURSELF", "HOT"]
EMPH_SA = ["مبروك", "تعلق", "مضخات", "الشجر", "أنبوب", "يصدمك", "حمرا", "حجر", "ممر", "تابعني",
           "لون", "صفر", "بيدك", "حارة"]
KEYS_SA = {
    ("hook", "POUR"): "كبيت", ("hook", "WATER"): "موية", ("hook", "RAMP"): "لوح", ("hook", "CONGRATS"): "مبروك",
    ("break1", "WATER"): "الموية", ("break1", "HALFWAY"): "النص", ("break1", "STUCK"): "تعلق",
    ("break1", "BURNING"): "حار", ("break1", "PLASTIC"): "البلاستيك",
    ("fix1", "PUMPS"): "مضخات", ("fix1", "TOP"): "فوق", ("fix1", "NONSTOP"): "وقفة", ("fix1", "SHEET"): "طبقة",
    ("fix1", "CARRIES"): "تشيلك", ("fix1", "DOWN"): "تحت",
    ("break2", "FAST"): "سريعة", ("break2", "SHARP"): "حادة", ("break2", "LAUNCHES"): "ترميك",
    ("break2", "SIDE"): "برا", ("break2", "BUSHES"): "الشجر",
    ("fix2", "BANK"): "تميل", ("fix2", "CURVES"): "اللفات", ("fix2", "RACETRACK"): "سباق", ("fix2", "RAISE"): "تعلي",
    ("fix2", "WALLS"): "الجدران", ("fix2", "WRAP"): "تلف", ("fix2", "FASTEST"): "أسرع", ("fix2", "CLOSED"): "مسكر",
    ("fix2", "TUBE"): "أنبوب",
    ("break3", "NEXT"): "اللي", ("break3", "SOON"): "بدري", ("break3", "CATCHES"): "يلحقك",
    ("break3", "CRASHES"): "يصدمك",
    ("fix3", "LIGHT"): "إشارة", ("fix3", "TOP"): "فوق", ("fix3", "RED"): "حمرا", ("fix3", "SENSOR"): "حساس",
    ("fix3", "SEES"): "يشوفك", ("fix3", "BOTTOM"): "تحت",
    ("break4", "SAFE"): "آمنة", ("break4", "SHOOT"): "تنطلق", ("break4", "END"): "آخر",
    ("break4", "SKIP"): "تنقز", ("break4", "STONE"): "حجر",
    ("fix4", "LONG"): "طويل", ("fix4", "RUNOUT"): "ممر", ("fix4", "SHALLOW"): "قليلة", ("fix4", "SLOWS"): "تهديك",
    ("fix4", "SPLASH"): "مسبح", ("fix4", "DEEP"): "غويط", ("fix4", "LAND"): "تنزل",
    ("cta", "FOLLOW"): "تابعني",
    ("reveal", "PAINT"): "اصبغها", ("reveal", "COLOR"): "لون", ("reveal", "TWIST"): "لف",
    ("reveal", "SLIDES"): "زحاليق", ("reveal", "TOWER"): "البرج", ("reveal", "OPEN"): "افتح",
    ("reveal", "GATES"): "البوابات",
    ("stat", "ONE"): "برج", ("stat", "SIX"): "ست", ("stat", "ZERO"): "صفر",
    ("closer", "CONGRATS"): "مبروك",
    ("tag", "SCARIEST"): "أخوف", ("tag", "BAREFOOT"): "حافي", ("tag", "HOT"): "حارة",
}
TEXT = {
    "en": {"follow": ("FOLLOW", "next: a rocket that lands itself"),
           "stat": [("1", "TOWER"), ("6", "SLIDES"), ("0", "DRY SWIMSUITS")],
           "pump": "PUMP", "hot": "HOT!", "bank": "BANKED", "walls": "HIGH WALLS", "tube": "CLOSED TUBE",
           "sensor": "SENSOR", "runout": "RUN-OUT", "deep": "DEEP POOL", "ouch": "OUCH!"},
    "ar_sa": {"follow": ("تابعني", "الجاي: صاروخ ينزل بروحه"),
              "stat": [("1", "برج"), ("6", "زحاليق"), ("0", "مايوه ناشف")],
              "pump": "مضخة", "hot": "حار!", "bank": "مايلة", "walls": "جدران عالية", "tube": "أنبوب مسكر",
              "sensor": "حساس", "runout": "ممر تهدئة", "deep": "مسبح غويط", "ouch": "آي!"},
}


def catmull(pts, n=26):
    out = []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        for k in range(n):
            u = k / n
            u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def up_normal(ang):
    nx, ny = math.sin(ang), -math.cos(ang)
    return (-nx, -ny) if ny > 0 else (nx, ny)


class Line:
    """A polyline measured by arc length."""
    def __init__(self, pts):
        self.x, self.y, self.s = [pts[0][0]], [pts[0][1]], [0.0]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            d = math.hypot(x1 - x0, y1 - y0)
            if d > 1e-6:
                self.x.append(x1)
                self.y.append(y1)
                self.s.append(self.s[-1] + d)
        self.L = self.s[-1]

    def pos(self, u):
        if u >= self.L:
            ang = self.angle(self.L - 1)
            return self.x[-1] + math.cos(ang) * (u - self.L), self.y[-1] + math.sin(ang) * (u - self.L)
        u = max(0.0, u)
        lo, hi = 0, len(self.s) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.s[mid] <= u:
                lo = mid
            else:
                hi = mid
        f = (u - self.s[lo]) / max(1e-9, self.s[hi] - self.s[lo])
        return lerp(self.x[lo], self.x[hi], f), lerp(self.y[lo], self.y[hi], f)

    def angle(self, u):
        x0, y0 = self.pos(max(0.0, u - 3))
        x1, y1 = self.pos(min(self.L, u + 3))
        return math.atan2(y1 - y0, x1 - x0)


class WaterSlide(Episode):
    EMPH = {"en": EMPH_EN, "ar_sa": EMPH_SA}
    KEYS = {"ar_sa": KEYS_SA}
    TEXT = TEXT
    STAT_COLORS = ("#111827", "#3B82F6", "#EF4444")

    def _tracks(self):
        tl = self.tl
        s, e = tl.s, tl.e
        self.ramp = Line(RAMP)
        self.big = Line(catmull(BIG) + [(RUN_END, -40)])
        self.L_exit = Line(catmull(BIG)).L                                  # end of the slide before the run-out
        big = self.big
        self.u_turn1 = min(range(0, int(self.L_exit), 4), key=lambda u: -big.pos(u)[0] if big.pos(u)[1] < -480 else 1e9)
        self.u_turn2 = min(range(0, int(self.L_exit), 4), key=lambda u: big.pos(u)[0] if -330 < big.pos(u)[1] < -150 else 1e9)
        self.u_tube0 = 150.0
        self.u_tube1 = self.u_turn1 - 120
        self.anchors({
            "pour": ("hook", "POUR", 0.1), "water0": ("hook", "WATER", 0.18), "ramp": ("hook", "RAMP", 0.4),
            "cong": ("hook", "CONGRATS", 0.5),
            "runs": ("break1", "WATER", 0.15), "halfway": ("break1", "HALFWAY", 0.35), "stuck": ("break1", "STUCK", 0.6),
            "burning": ("break1", "BURNING", 0.75), "plastic": ("break1", "PLASTIC", 0.9),
            "pumps": ("fix1", "PUMPS", 0.12), "top1": ("fix1", "TOP", 0.43), "nonstop": ("fix1", "NONSTOP", 0.5),
            "sheet": ("fix1", "SHEET", 0.65), "carries": ("fix1", "CARRIES", 0.78), "down1": ("fix1", "DOWN", 0.95),
            "fast": ("break2", "FAST", 0.15), "sharp": ("break2", "SHARP", 0.35), "launches": ("break2", "LAUNCHES", 0.45),
            "side": ("break2", "SIDE", 0.7), "bushes": ("break2", "BUSHES", 0.92),
            "bank": ("fix2", "BANK", 0.1), "curves": ("fix2", "CURVES", 0.17), "racetrack": ("fix2", "RACETRACK", 0.3),
            "raise": ("fix2", "RAISE", 0.42), "walls": ("fix2", "WALLS", 0.5), "wrap": ("fix2", "WRAP", 0.58),
            "fastest": ("fix2", "FASTEST", 0.67), "closed": ("fix2", "CLOSED", 0.87), "tube": ("fix2", "TUBE", 0.95),
            "next": ("break3", "NEXT", 0.18), "soon": ("break3", "SOON", 0.45), "catches": ("break3", "CATCHES", 0.55),
            "crashes": ("break3", "CRASHES", 0.75),
            "light": ("fix3", "LIGHT", 0.2), "top3": ("fix3", "TOP", 0.33), "red": ("fix3", "RED", 0.47),
            "sensor": ("fix3", "SENSOR", 0.65), "sees": ("fix3", "SEES", 0.73), "bottom": ("fix3", "BOTTOM", 0.92),
            "safe": ("break4", "SAFE", 0.15), "shoot": ("break4", "SHOOT", 0.37), "end": ("break4", "END", 0.52),
            "skip": ("break4", "SKIP", 0.62), "stone": ("break4", "STONE", 0.95),
            "long": ("fix4", "LONG", 0.18), "runout": ("fix4", "RUNOUT", 0.22), "shallow": ("fix4", "SHALLOW", 0.36),
            "slows": ("fix4", "SLOWS", 0.5), "splash": ("fix4", "SPLASH", 0.68), "deep": ("fix4", "DEEP", 0.76),
            "land": ("fix4", "LAND", 0.9),
            "follow": ("cta", "FOLLOW", 0.4),
            "paint": ("reveal", "PAINT", 0.1), "color": ("reveal", "COLOR", 0.27), "twist": ("reveal", "TWIST", 0.37),
            "slides": ("reveal", "SLIDES", 0.5), "tower": ("reveal", "TOWER", 0.7), "open": ("reveal", "OPEN", 0.85),
            "gates": ("reveal", "GATES", 0.95),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "SIX", 0.3), "s3": ("stat", "ZERO", 0.6),
            "cong2": ("closer", "CONGRATS", 0.1),
            "scariest": ("tag", "SCARIEST", 0.15), "barefoot": ("tag", "BAREFOOT", 0.55), "hot": ("tag", "HOT", 0.85),
        })
        T = self.T
        T["womp"] = e("tag") + 0.35
        # what exists when
        self.small = Track(1.0).to(s("break2") - 0.4, 0.0, 0.5)
        self.build = Track(0.0).to(s("break2") - 0.4, 1.0, max(0.9, T["fast"] - s("break2") + 0.6), e_out)
        self.pump = Track(0.0).to(T["pumps"] - 0.2, 1.0, 0.4)
        self.bankt = Track(0.0).to(T["bank"] - 0.1, 1.0, 0.5, e_back)
        self.wallt = Track(0.0).to(T["raise"] - 0.1, 1.0, 0.5, e_back)
        self.tubet = Track(0.0).to(T["wrap"], 1.0, max(0.8, T["tube"] + 0.2 - T["wrap"]), e_out)
        self.lightt = Track(0.0).to(T["light"] - 0.2, 1.0, 0.35, e_back)
        self.sensort = Track(0.0).to(T["sensor"] - 0.2, 1.0, 0.35, e_back)
        self.runt = Track(0.0).to(T["long"] - 0.2, 1.0, max(0.7, T["runout"] + 0.4 - T["long"]), e_out)
        self.deept = Track(0.0).to(T["splash"] - 0.2, 1.0, max(0.7, T["land"] - T["splash"]), e_io)
        self.paintt = Track(0.0).to(T["paint"], 1.0, max(0.7, T["color"] + 0.3 - T["paint"]), e_io)
        self.extra = Track(0.0).to(T["twist"] - 0.1, 1.0, max(1.0, T["tower"] + 0.3 - T["twist"]), e_out)
        self.gate = Track(0.0).to(T["open"] - 0.1, 1.0, 0.6, e_out)
        # the hook water stream (fraction of the ramp that is wet)
        self.wet = Track(0.0).to(T["pour"] + 0.05, 1.0, 0.9, e_out)
        self.wet.to(T["runs"], 0.48, 0.8, e_in)              # second try: runs out halfway
        self.wet.to(T["pumps"] + 0.3, 1.0, 0.8, e_out)        # pumps: wet all the way
        # camera
        cam = self.cam = Camera(0, -270, 1.0)
        cam.key(0.05, 0, -250, 1.06, 2.6)
        cam.key(T["stuck"] - 0.5, -60, -230, 1.3, 0.6)
        cam.key(T["pumps"] - 0.4, -320, -280, 0.95, 0.6)
        cam.key(T["carries"] - 0.5, -60, -260, 1.0, 0.6)
        cam.key(s("break2") - 0.45, 150, -500, 0.58, 0.8)
        cam.key(T["launches"] - 0.2, 380, -380, 0.8, 0.5)
        cam.key(s("fix2") - 0.1, 30, -520, 0.66, 0.6)
        cam.key(T["wrap"] - 0.3, -60, -720, 0.8, 0.6)
        cam.key(s("break3") - 0.1, 110, -640, 0.9, 0.6)
        cam.key(T["light"] - 0.4, -360, -920, 1.25, 0.5)
        cam.key(T["sensor"] - 0.4, 640, -170, 1.2, 0.5)
        cam.key(s("break4") - 0.1, 760, -230, 0.95, 0.6)
        cam.key(T["shoot"] + 0.1, 1240, -210, 0.95, 1.6)
        cam.key(T["long"] - 0.3, 900, -200, 0.9, 0.5)
        cam.key(T["splash"] - 0.4, 1130, -180, 0.95, 0.6)
        cam.key(s("cta") + 0.2, 200, -560, 0.5, 3.0)
        cam.key(T["paint"] - 0.3, 60, -560, 0.62, 1.0)
        cam.key(T["open"] - 0.45, -760, -330, 0.62, 0.7)
        cam.key(s("stat") - 0.1, -150, -560, 0.45, 0.9)
        cam.key(s("closer") - 0.1, -100, -540, 0.48, 2.4)
        cam.key(s("tag") - 0.22, 1700, -130, 1.9, 0.45)
        self.shakes = [(T["bushes"] - 0.1, 0.4, 10), (T["crashes"], 0.4, 12), (T["stone"] - 0.2, 0.3, 6)]

    def red_level(self, t):
        T = self.T
        return (0.8 * bump(t, T["stuck"] - 0.2, T["plastic"] + 1.0) + 0.9 * bump(t, T["launches"], T["bushes"] + 1.0)
                + 0.9 * bump(t, T["crashes"] - 0.1, T["crashes"] + 1.3) + 0.8 * bump(t, T["skip"], T["stone"] + 1.0))

    # ------------------------------------------------------------------ backdrop
    def draw_backdrop(self, c, t, dusk):
        cx, cy, z = self.cam_state
        gy = (0 - cy) * z + H / 2
        zf = clamp(0.62 * z ** 0.6, 0.18, 0.9)
        c.save()
        c.translate(W / 2, gy)
        c.scale(zf, zf)
        c.translate(-cx * 0.25, 0)
        for i, x in enumerate(range(-3200, 3400, 420)):
            palm(c, x + (i * 53) % 90, 1.2 + 0.25 * (i % 3), "#9CC9A8")
        c.restore()

    # ------------------------------------------------------------------ world
    def draw_world(self, c, t, dusk, z):
        T = self.T
        world.ground(c, -6000, 6000, 3000, dusk)
        rect(c, -1500, 0, 3600, 22, DECK)
        for x in range(-1500, 2100, 110):
            line(c, x, 2, x, 20, "#D6C7AA", 3)
        self.draw_bushes(c, t)
        self.draw_pool(c, t)
        self.draw_pump(c, t)
        if self.small.at(t) > 0:
            self.draw_small(c, t)
        if self.build.at(t) > 0:
            self.draw_tower(c, t)
            self.draw_extra(c, t)
            self.draw_big(c, t, z)
        self.draw_riders(c, t)
        self.draw_crowd(c, t)

    def draw_bushes(self, c, t):
        T = self.T
        rustle = bump(t, T["bushes"] - 0.1, T["bushes"] + 0.8)
        ba = self.build.at(t)
        for bx in (430, 520, 610):
            dx = 8 * rustle * math.sin(t * 30 + bx)
            for ox, oy, r in ((-40, -50, 52), (30, -60, 58), (0, -95, 50)):
                circle(c, bx + ox + dx, oy, r * ba, "#3E9B4F")
            circle(c, bx + dx - 10, -100, 22 * ba, "#66BB6A", 0.7)
        # far bushes where the stone-skipper lands: only there for break4 (off screen when they come and go)
        fa = prog(t, self.tl.s("break4") - 0.1, self.tl.s("break4") + 0.2) * (1 - prog(t, self.tl.s("fix4") + 0.3, self.tl.s("fix4") + 0.6))
        if fa > 0:
            for bx in (1640, 1760):
                for ox, oy, r in ((-40, -50, 52), (30, -60, 58), (0, -95, 50)):
                    circle(c, bx + ox, oy, r * fa, "#3E9B4F")

    def pool_geom(self, t):
        x0 = lerp(780, RUN_END, self.runt.at(t))
        depth = lerp(70, 230, self.deept.at(t))
        return x0, POOL_X1, depth

    def draw_pool(self, c, t):
        small = self.small.at(t)
        if small > 0:
            rect(c, 210, 0, 330, 80, "#A7B0B9", small)
            grad_rect(c, 220, 4, 310, 70, WATER0, WATER1, small)
        if self.build.at(t) > 0:
            a = self.build.at(t)
            x0, x1, d = self.pool_geom(t)
            rect(c, x0 - 16, 0, x1 - x0 + 32, d + 16, "#A7B0B9", a)
            grad_rect(c, x0, 4, x1 - x0, d, WATER0, WATER1, a)
            for i in range(int((x1 - x0) / 90)):
                xx = x0 + 30 + i * 90 + 14 * math.sin(t * 2 + i)
                line(c, xx, 8, xx + 40, 8, "#E0F7FF", 4, 0.6 * a)

    def draw_pump(self, c, t):
        a = self.pump.at(t)
        if a <= 0:
            return
        x0 = -760
        rect(c, x0 - 110, -170, 220, 170, "#64748B", a, r=12)
        rect(c, x0 - 110, -170, 220, 30, "#475569", a, r=10)
        circle(c, x0, -80, 48, "#E2E8F0", a)
        for b in range(4):
            ang = t * 12 + b * math.pi / 2
            line(c, x0, -80, x0 + math.cos(ang) * 40, -80 + math.sin(ang) * 40, "#0EA5E9", 9, a)
        circle(c, x0, -80, 10, "#1E293B", a)
        # pipe to the top of whichever slide stands
        big = self.build.at(t)
        top_x, top_y = (-470, -990) if big > 0.5 else (-480, -470)
        pts = [(x0 + 110, -60), (-520, -60), (-520, top_y), (top_x + 40, top_y)]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            line(c, xa, ya, xb, yb, "#94A3B8", 26, a)
            line(c, xa, ya, xb, yb, "#38BDF8", 12, a)
        for i in range(10):
            u = (t * 0.8 + i / 10) % 1.0
            yy = lerp(-60, top_y, u)
            circle(c, -520, yy, 5, "#E0F7FF", a)

    def draw_small(self, c, t):
        T = self.T
        a = self.small.at(t)
        # ladder + platform
        for x in (-510, -450):
            line(c, x, 0, x, -450, "#B45309", 10, a)
        for y in range(-40, -450, -45):
            line(c, -510, y, -450, y, "#B45309", 7, a)
        rect(c, -530, -462, 110, 16, "#92400E", a, r=4)
        (x0, y0), (x1, y1) = RAMP
        line(c, x0, y0 + 14, x1, y1 + 14, "#CBD5E1", 34, a)
        line(c, x0, y0, x1, y1, "#F8FAFC", 24, a)
        # wet part
        wf = self.wet.at(t)
        if wf > 0:
            xm, ym = lerp(x0, x1, wf), lerp(y0, y1, wf)
            line(c, x0, y0 - 2, xm, ym - 2, "#7DD3FC", 14, a * 0.95)
            for i in range(8):
                u = ((t * 1.4 + i / 8) % 1.0) * wf
                circle(c, lerp(x0, x1, u), lerp(y0, y1, u) - 4, 5, "#E0F7FF", a)
        # heat on the dry part
        hot = bump(t, T["burning"] - 0.4, T["pumps"] - 0.1)
        if hot > 0:
            for i in range(5):
                u = 0.55 + 0.08 * i
                hx, hy = lerp(x0, x1, u), lerp(y0, y1, u)
                for k in range(3):
                    yy = hy - 30 - 40 * ((t * 1.2 + k / 3 + i * 0.13) % 1.0)
                    line(c, hx - 10, yy, hx + 10, yy - 14, "#F97316", 5, hot * 0.8)

    def draw_tower(self, c, t):
        a = self.build.at(t)
        h = 990 * e_out(a)
        for x in (-520, -400):
            line(c, x, 0, x, -h, "#64748B", 16)
        for y in range(-80, int(-h), -120):
            line(c, -520, y, -400, y - 60, "#94A3B8", 8)
            line(c, -400, y, -520, y - 60, "#94A3B8", 8)
        if a > 0.95:
            rect(c, -560, -1000, 200, 18, "#475569", r=4)
            line(c, -560, -1060, -360, -1060, "#94A3B8", 8)
            for x in (-560, -460, -360):
                line(c, x, -1000, x, -1060, "#94A3B8", 8)
            # stairs zig-zag
            for i in range(9):
                y = -i * 110
                line(c, -620, y, -540, y - 110, "#A16207", 8)

    def flume_col(self, t, u):
        p = self.paintt.at(t)
        if p <= 0:
            return FLUME
        k = clamp((p * (self.big.L + 600) - u) / 400)
        return mix(FLUME, RAINBOW[int(u / 330) % len(RAINBOW)], k)

    def draw_big(self, c, t, z):
        T, B = self.T, self.big
        a = self.build.at(t)
        vis = B.L_exit if False else self.L_exit * e_out(a) + (B.L - self.L_exit) * self.runt.at(t)
        step = 8.0
        pts = []
        u = 0.0
        while u <= vis:
            pts.append((u, B.pos(u)))
            u += step
        if len(pts) < 2:
            return
        # supports
        for u, (x, y) in pts:
            if y < -120 and int(u) % 220 < step and x > -380:
                line(c, x, y + 16, x, 0, "#94A3B8", 10)
        wall = 16 + 12 * self.wallt.at(t)
        for (ua, (xa, ya)), (ub, (xb, yb)) in zip(pts, pts[1:]):
            col = self.flume_col(t, ua)
            ang = math.atan2(yb - ya, xb - xa)
            nx, ny = up_normal(ang)
            line(c, xa, ya, xb, yb, shade(col, -0.25), 34 + wall * 0.6)
            line(c, xa + nx * 6, ya + ny * 6, xb + nx * 6, yb + ny * 6, col, 24)
            line(c, xa + nx * (10 + wall * 0.5), ya + ny * (10 + wall * 0.5), xb + nx * (10 + wall * 0.5), yb + ny * (10 + wall * 0.5),
                 shade(col, 0.2), 7)
            # water sheet
            if ua < self.L_exit + (B.L - self.L_exit) * self.runt.at(t):
                line(c, xa + nx * 2, ya + ny * 2, xb + nx * 2, yb + ny * 2, "#BAE6FD", 6, 0.9)
        for i in range(int(vis / 60)):
            uu = (i * 60 + t * 520) % max(vis, 1)
            x, y = B.pos(uu)
            circle(c, x, y - 4, 4, "#FFFFFF", 0.8)
        # raised side walls at the two hairpins
        wl = self.wallt.at(t)
        if wl > 0:
            for ut in (self.u_turn1, self.u_turn2):
                lo, hi = [], []
                for k in range(-18, 19):
                    uu = ut + k * 14
                    x, y = B.pos(uu)
                    nx, ny = up_normal(B.angle(uu))
                    hgt = 48 * wl * (1 - (abs(k) / 19) ** 3)
                    lo.append((x + nx * 12, y + ny * 12))
                    hi.append((x + nx * (12 + hgt), y + ny * (12 + hgt)))
                poly(c, lo + hi[::-1], "#93C5FD", 0.85)
                for (xa, ya), (xb, yb) in zip(hi, hi[1:]):
                    line(c, xa, ya, xb, yb, "#FFFFFF", 6, 0.9 * wl)
        # banked curves: racetrack kerbs
        bk = self.bankt.at(t)
        if bk > 0:
            for ut, side in ((self.u_turn1, 1), (self.u_turn2, -1)):
                for k in range(-9, 10):
                    uu = ut + k * 12
                    x, y = B.pos(uu)
                    ang = B.angle(uu)
                    nx, ny = math.sin(ang), -math.cos(ang)
                    out = 30 + 22 * bk * (1 - abs(k) / 10)
                    col = RED if (k + 20) % 2 else "#FFFFFF"
                    circle(c, x + side * math.cos(ang - math.pi / 2) * 0 + nx * out * 0.0 + (side * 30 * bk),
                           y - out * 0.6, 9 * bk, col)
        # the closed tube
        tb = self.tubet.at(t)
        if tb > 0:
            u1 = lerp(self.u_tube0, self.u_tube1, tb)
            u = self.u_tube0
            prev = None
            while u <= u1:
                x, y = B.pos(u)
                if prev:
                    line(c, prev[0], prev[1] - 10, x, y - 10, "#0369A1", 78, 0.95)
                    line(c, prev[0], prev[1] - 22, x, y - 22, "#38BDF8", 30, 0.55)
                prev = (x, y)
                u += 10
            u = self.u_tube0
            while u <= u1:
                x, y = B.pos(u)
                ang = B.angle(u)
                nx, ny = up_normal(ang)
                line(c, x - nx * 30, y - ny * 30 - 10, x + nx * 50, y + ny * 50 - 10, "#075985", 6, 0.8)
                u += 70
        # traffic light at the top + exit sensor
        la = self.lightt.at(t)
        if la > 0:
            green = prog(t, self.T["bottom"] - 0.05, self.T["bottom"] + 0.15) * (1 - prog(t, self.T["safe"] - 0.3, self.T["safe"]))
            rect(c, -330, -1180, 70, 170, "#111827", la, r=14)
            circle(c, -295, -1140, 24, mix("#7F1D1D", RED, 1 - green), la)
            circle(c, -295, -1060, 24, mix("#14532D", "#22C55E", green), la)
            line(c, -295, -1010, -295, -960, "#475569", 10, la)
            if green < 0.5:
                glow(c, -295, -1140, 60, RED, 0.5 * la)
            else:
                glow(c, -295, -1060, 60, "#22C55E", 0.5 * la)
        sa = self.sensort.at(t)
        if sa > 0:
            ex, ey = B.pos(self.L_exit - 30)
            rect(c, ex - 10, ey - 130, 20, 130, "#334155", sa)
            circle(c, ex, ey - 130, 14, RED, sa)
            beam = bump(t, self.T["sees"] - 0.1, self.T["bottom"] + 0.3)
            line(c, ex, ey - 110, ex, ey + 6, RED, 5, 0.5 * sa + 0.5 * beam)

    def draw_extra(self, c, t):
        """More slides twisting around the tower (reveal)."""
        a = self.extra.at(t)
        if a <= 0:
            return
        for i, (amp, ph, col) in enumerate(((160, 0.0, RAINBOW[0]), (220, 1.6, RAINBOW[3]), (140, 3.1, RAINBOW[4]),
                                             (240, 4.4, RAINBOW[5]))):
            pts = []
            n = 60
            for k in range(int(n * a) + 1):
                v = k / n
                x = -460 + amp * math.sin(v * 3 * math.pi + ph) + (i - 1.5) * 40 + v * 120
                y = lerp(-930 + i * 40, -40, v)
                pts.append((x, y))
            for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                line(c, xa, ya, xb, yb, shade(col, -0.25), 34)
                line(c, xa, ya - 5, xb, yb - 5, col, 22)

    # ------------------------------------------------------------------ riders
    def rider_on(self, c, line_, u, col, a, off=0.0, spin=0.0, flat=1.0):
        x, y = line_.pos(u)
        ang = line_.angle(u)
        nx, ny = up_normal(ang)
        rider(c, x + nx * (14 + off), y + ny * (14 + off), math.degrees(ang) + spin, col, a)

    def draw_riders(self, c, t):
        T, tl = self.T, self.tl
        R, B = self.ramp, self.big
        Lr = R.L
        # hook: pour, then slide down the ramp into the little pool
        if t < tl.s("break2") - 0.3:
            col = world.crowd_colors(1)
            if t < T["runs"] - 0.2:
                if t < T["ramp"] + 0.2:
                    x, y = R.pos(20)
                    world.person(c, x - 20, y - 6, 112, arms_up=0.5, **col)
                    bucket(c, x + 18, y - 70, t, T["pour"])
                else:
                    u = Lr * e_in(prog(t, T["ramp"] + 0.2, T["cong"] + 0.5))
                    if u < Lr - 5:
                        self.rider_on(c, R, u, col, 1.0)
                    else:
                        swimhead(c, 380, 6, col, t)
            elif t < T["pumps"] + 0.3:
                # second rider stops halfway, hops on the hot plastic
                u = min(Lr * 0.5, Lr * 0.56 * e_out(prog(t, T["runs"], T["stuck"])))
                if t < T["stuck"]:
                    self.rider_on(c, R, u, world.crowd_colors(2), 1.0)
                else:
                    x, y = R.pos(Lr * 0.5)
                    hop = abs(math.sin((t - T["stuck"]) * 9)) * 28 * bump(t, T["burning"] - 0.3, T["pumps"])
                    world.person(c, x, y - 10 - hop, 112, arms_up=0.6, sweat=1.0, **world.crowd_colors(2))
            else:
                # pumps on: all the way down
                u = Lr * e_in(prog(t, T["carries"] - 0.3, T["down1"] + 0.2))
                if u < Lr - 5:
                    self.rider_on(c, R, u, world.crowd_colors(3), 1.0)
                else:
                    swimhead(c, 400, 6, world.crowd_colors(3), t)
                    splash(c, 330, 0, prog(t, T["down1"] + 0.2, T["down1"] + 0.9))
        # break2: down the big slide, flies off at the first hairpin into the bushes
        if T["fast"] - 0.3 < t < s_of(self, "fix2"):
            col = world.crowd_colors(4)
            u_fly = self.u_turn1 - 30
            if t < T["launches"]:
                u = u_fly * e_in(prog(t, T["fast"] - 0.3, T["launches"]))
                self.rider_on(c, B, u, col, 1.0)
            else:
                f = prog(t, T["launches"], T["bushes"] - 0.1)
                x0, y0 = B.pos(u_fly)
                x = lerp(x0, 520, f)
                y = lerp(y0, -90, f) - 260 * math.sin(f * math.pi)
                if f < 1:
                    rider(c, x, y, 540 * f, col, 1.0)
                else:
                    world.person(c, 520, -110, 100, arms_up=1.0, a=1 - prog(t, T["bushes"] + 0.8, T["bushes"] + 1.2), **col)
        # fix2: a clean run through banked turns and the tube
        if T["tube"] - 1.2 < t < T["tube"] + 1.8:
            u = (self.L_exit - 10) * prog(t, T["tube"] - 1.2, T["tube"] + 1.6)
            inside = self.u_tube0 < u < self.u_tube1
            self.rider_on(c, B, u, world.crowd_colors(5), 0.25 if inside else 1.0)
        # break3: rider A, then B too soon; B catches A at the first hairpin
        if T["next"] - 0.4 < t < s_of(self, "fix3"):
            ua = self.u_turn1 * e_out(prog(t, T["next"] - 0.4, T["crashes"]))
            ub = self.u_turn1 * e_in(prog(t, T["soon"] - 0.3, T["crashes"]))
            if t < T["crashes"]:
                self.rider_on(c, B, ua, world.crowd_colors(6), 1.0)
                self.rider_on(c, B, ub, world.crowd_colors(7), 1.0)
            else:
                x, y = B.pos(self.u_turn1)
                k = prog(t, T["crashes"], T["crashes"] + 0.5)
                self.rider_on(c, B, self.u_turn1 - 10, world.crowd_colors(6), 1.0, spin=200 * k)
                self.rider_on(c, B, self.u_turn1 - 50, world.crowd_colors(7), 1.0, spin=-140 * k)
                stars(c, x, y - 70, t, 1 - prog(t, T["crashes"] + 1.0, T["crashes"] + 1.4))
        # fix3: a rider leaves the bottom, the sensor sees it, the light turns green
        if T["light"] < t < T["safe"] - 0.2:
            u = lerp(self.L_exit - 600, self.L_exit + 120, prog(t, T["sensor"] - 0.6, T["bottom"] + 0.3))
            if u < self.L_exit + 100:
                self.rider_on(c, B, u, world.crowd_colors(8), 1.0)
            # the next rider waits at the top
            x, y = B.pos(10)
            world.person(c, x - 40, y - 12, 104, arms_up=0.2, **world.crowd_colors(9))
        # break4: shoots off the end and skips across the pool
        if T["safe"] - 0.2 < t < s_of(self, "fix4") + 0.4:
            u = lerp(self.L_exit - 700, self.L_exit, e_in(prog(t, T["safe"] - 0.2, T["shoot"] + 0.2)))
            col = world.crowd_colors(10)
            if t < T["shoot"] + 0.2:
                self.rider_on(c, B, u, col, 1.0)
            else:
                t0s, t1s = T["shoot"] + 0.2, T["stone"] + 0.3
                f = prog(t, t0s, t1s)
                x = lerp(700, 1680, f)
                hop = abs(math.sin(f * math.pi * 4)) * (140 * (1 - f) + 30)
                for k in (1, 2, 3):
                    tb = lerp(t0s, t1s, k / 4)
                    splash(c, lerp(700, 1680, k / 4), 0, prog(t, tb, tb + 0.7), big=1.3 - 0.2 * k)
                if f < 1:
                    rider(c, x, -20 - hop, -10, col, 1.0)
                else:
                    world.person(c, 1700, -120, 100, arms_up=1.0, **col)
        # fix4: slides into the run-out lane and slows down
        if T["shallow"] - 0.6 < t < T["land"] + 1.6:
            col = world.crowd_colors(11)
            if t < T["land"] - 0.35:
                u = lerp(self.L_exit - 500, self.L_exit + 330, e_out(prog(t, T["shallow"] - 0.6, T["slows"] + 0.5)))
                u += (RUN_END - 20 - self.big.pos(self.L_exit + 330)[0]) * prog(t, T["splash"] - 0.3, T["land"] - 0.35)
                self.rider_on(c, B, u, col, 1.0)
                if u > self.L_exit:
                    x, y = B.pos(u)
                    spray(c, x + 30, y - 20, t, prog(t, T["shallow"], T["slows"] + 0.4) * (1 - prog(t, T["slows"] + 0.4, T["slows"] + 0.8)))
            elif t < T["land"]:
                f = prog(t, T["land"] - 0.35, T["land"])
                rider(c, lerp(RUN_END + 10, RUN_END + 110, f), -40 + 60 * f * f, 30 * f, col, 1.0)
            else:
                splash(c, RUN_END + 120, 0, prog(t, T["land"], T["land"] + 0.8), big=1.4)
                swimhead(c, RUN_END + 130, 6, col, t)
        # reveal + stat + closer: riders on all the slides
        if T["gates"] - 0.2 < t < self.tl.s("tag") - 0.2:
            for i in range(3):
                u = (t * 420 + i * 700) % (B.L - 50)
                self.rider_on(c, B, u, world.crowd_colors(i + 2), 1.0 if not (self.u_tube0 < u < self.u_tube1) else 0.25)

    def draw_crowd(self, c, t):
        T, tl = self.T, self.tl
        g = self.gate.at(t)
        if g > 0 or t > T["open"]:
            # gate on the left
            rect(c, -1300, -220, 26, 220, "#475569")
            rect(c, -1050, -220, 26, 220, "#475569")
            rect(c, -1300, -260, 276, 44, "#F97316", r=10)
            for side, x0 in ((-1, -1274), (1, -1050)):
                w = 110 * (1 - g)
                rect(c, x0 if side < 0 else x0 - w, -180, w, 160, "#94A3B8", 0.9)
            for i in range(10):
                f = prog(t, T["gates"] + i * 0.12, T["gates"] + 2.2 + i * 0.12)
                if f > 0:
                    x = lerp(-1360 - i * 40, -760 + i * 120, e_out(f))
                    world.person(c, x, 0, 108, walk=t * 2 if f < 1 else 0, **world.crowd_colors(i))
        # the tag: barefoot on the hot deck
        a = prog(t, tl.s("tag") - 0.5, tl.s("tag") - 0.2)
        if a > 0:
            heat = a * (0.6 + 0.4 * prog(t, T["barefoot"] - 0.4, T["hot"]))
            grad_rect(c, 1580, -3, 340, 26, "#FB923C", "#EF4444", heat * 0.85, r=6, horizontal=True)
            for i in range(9):                                  # heat shimmer rising off the deck
                u = (t * 0.9 + i / 9) % 1.0
                hx = 1600 + i * 38 + 10 * math.sin(t * 5 + i)
                yy = -14 - 150 * u
                line(c, hx, yy, hx + 10 * math.sin(t * 9 + i), yy - 26, "#F97316", 7, heat * 0.9 * (1 - u))
            jump = prog(t, T["barefoot"] - 0.3, T["barefoot"])
            ph = t * 10
            hop = abs(math.sin(ph)) * 52 * jump
            x = 1720 + 26 * math.sin(t * 3)
            world.person(c, x, -hop, 132, arms_up=0.5 + 0.45 * abs(math.sin(ph)), walk=t * 5 * jump, sweat=1.0, a=a,
                         **world.crowd_colors(4))
            if jump > 0 and hop < 10:                           # a puff of steam every time a foot lands
                for k in range(4):
                    circle(c, x - 18 + 12 * k, -8 - 6 * k, 9 + 3 * k, "#FFFFFF", 0.5 * a)

    # ------------------------------------------------------------------ overlays
    def draw_overlays(self, c, t, tw, dusk):
        T, tx, tl = self.T, self.tx, self.tl
        B = self.big
        R = self.ramp
        # hook outline
        (x0, y0), (x1, y1) = RAMP
        self.outline(c, tw, T["cong"] + 0.05, (x0 - 40, y0 - 40, x1 - x0 + 80, y1 - y0 + 80), 1.2)
        self.wpill(c, tw, tx["hot"], R.pos(R.L * 0.62)[0] + 40, R.pos(R.L * 0.62)[1] - 150, T["burning"] - 0.1, T["pumps"] - 0.2,
                   fg="#FFFFFF", bg="#F97316", size=44)
        self.outline(c, tw, T["pumps"] + 0.05, (-870, -175, 220, 180), 1.2)
        self.wpill(c, tw, tx["pump"], -760, -240, T["pumps"], T["sheet"])
        tx1, ty1 = B.pos(self.u_turn1)
        tx2, ty2 = B.pos(self.u_turn2)
        self.outline(c, tw, T["bank"] + 0.1, (tx1 - 120, ty1 - 110, 190, 230), 1.1)
        self.wpill(c, tw, tx["bank"], tx1 + 120, ty1 - 150, T["bank"], T["raise"] - 0.2, fg="#FFFFFF", bg=RED)
        self.wpill(c, tw, tx["walls"], tx2 - 40, ty2 - 160, T["raise"], T["wrap"] - 0.2)
        ax, ay = B.pos(self.u_tube0)
        bx, by = B.pos(self.u_tube1)
        self.outline(c, tw, T["tube"] - 0.2, (ax - 40, ay - 80, bx - ax + 80, by - ay + 120), 1.1)
        self.wpill(c, tw, tx["tube"], (ax + bx) / 2, min(ay, by) - 140, T["closed"], T["tube"] + 1.4, fg="#FFFFFF", bg="#0369A1")
        self.outline(c, tw, T["light"] + 0.1, (-340, -1190, 90, 190), 1.1)
        ex, ey = B.pos(self.L_exit - 30)
        self.outline(c, tw, T["sensor"] + 0.1, (ex - 30, ey - 160, 60, 170), 1.0)
        self.wpill(c, tw, tx["sensor"], ex + 160, ey - 160, T["sensor"], T["bottom"] + 0.6)
        rx0, ry0 = B.pos(self.L_exit)
        self.outline(c, tw, T["runout"] + 0.2, (rx0, ry0 - 50, RUN_END - rx0, 70), 1.1)
        self.wpill(c, tw, tx["runout"], (rx0 + RUN_END) / 2, ry0 - 130, T["runout"], T["splash"] - 0.2)
        px0, px1, d = self.pool_geom(tw)
        self.outline(c, tw, T["deep"] + 0.1, (px0, 0, px1 - px0, d + 10), 1.1)
        self.wpill(c, tw, tx["deep"], (px0 + px1) / 2, -110, T["deep"], T["land"] + 0.9, fg="#FFFFFF", bg="#0EA5E9")
        self.wpill(c, tw, tx["ouch"], 1700, -330, T["hot"] - 0.2, T["hot"] + 2.0, fg="#FFFFFF", bg=RED, size=46)
        # alerts + checks
        self.alert(c, tw, T["stuck"], T["pumps"] - 0.3, R.pos(R.L * 0.5)[0] + 160, R.pos(R.L * 0.5)[1] - 220)
        self.alert(c, tw, T["launches"] + 0.1, T["bank"] - 0.3, 470, -420)
        self.alert(c, tw, T["crashes"] + 0.05, T["light"] - 0.3, tx1 + 150, ty1 - 220)
        self.alert(c, tw, T["skip"], T["long"] - 0.3, 1300, -330)
        for t0, wx, wy, nxt in ((T["down1"] + 0.1, 150, -420, tl.s("break2")), (T["tube"] + 0.05, tx1 + 180, ty1 - 260, tl.s("break3")),
                                (T["bottom"] + 0.15, ex + 140, ey - 300, tl.s("break4")), (T["land"] + 0.2, 1340, -320, T["pause"] + 0.2)):
            self.check(c, tw, t0, wx, wy, dur=min(1.5, nxt + 0.25 - t0))
        # the light at the top, shown in a corner while the camera watches the sensor at the bottom
        ml = prog(tw, T["sensor"] - 0.3, T["sensor"]) * (1 - prog(tw, T["bottom"] + 0.9, T["bottom"] + 1.2))
        if ml > 0:
            g = prog(tw, T["bottom"] + 0.05, T["bottom"] + 0.2)
            c.save()
            c.translate(W - 150, 270)
            k = e_back(clamp(ml))
            c.scale(k, k)
            rect(c, -50, -104, 100, 208, "#000000", 0.3, r=24, blur=8)
            rect(c, -48, -100, 96, 200, "#111827", 1.0, r=22)
            glow(c, 0, -46, 80, RED, 0.6 * (1 - g))
            glow(c, 0, 46, 80, "#22C55E", 0.6 * g)
            circle(c, 0, -46, 30, mix("#7F1D1D", RED, 1 - g))
            circle(c, 0, 46, 30, mix("#14532D", "#22C55E", g))
            c.restore()

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, tl = self.T, self.tl
        s, e = tl.s, tl.e
        ev = [(0.0, sfx.whoosh(0.4, True, 1), -10), (T["pour"], sfx.hiss(1.0, 2), -8), (T["ramp"] + 0.2, sfx.whoosh(0.9, False, 3), -6),
              (T["cong"] + 0.5, sfx.hiss(0.5, 4), -4), (T["cong"] + 0.5, sfx.thud(0.3, 5), -8), (T["cong"], sfx.pop(), -2),
              (T["cong"], sfx.sparkle(), -8)]
        ev += [(T["runs"], sfx.hiss(0.8, 6), -10), (T["stuck"], sfx.creak(0.4, 7), -6), (T["stuck"] + 0.05, sfx.buzz(), -8),
               (T["burning"], sfx.sizzle(1.0, 8), -6)]
        ev += [(T["pumps"] - 0.1, sfx.clank(300, 0.4, 9), -6), (T["pumps"], sfx.whirr(2.0, 120, 220, 10), -10),
               (T["sheet"], sfx.hiss(1.6, 11), -10), (T["carries"] - 0.2, sfx.whoosh(1.0, False, 12), -6),
               (T["down1"] + 0.2, sfx.hiss(0.6, 13), -4), (T["down1"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.4, sfx.riser(1.0, 14), -10), (T["fast"] - 0.3, sfx.whoosh(1.0, False, 15), -6),
               (T["launches"], sfx.whoosh(0.8, True, 16), -4), (T["bushes"] - 0.1, sfx.thud(0.4, 17), -4),
               (T["bushes"], sfx.hiss(0.5, 18), -8), (T["bushes"] + 0.1, sfx.alarm(2, 850), -12)]
        ev += [(T["bank"], sfx.clank(400, 0.5, 19), -8), (T["racetrack"], sfx.sparkle(0.5, 6, 20), -10),
               (T["raise"], sfx.clank(600, 0.4, 21), -8), (T["wrap"], sfx.whoosh(1.0, True, 22), -10),
               (T["tube"] - 1.2, sfx.whoosh(2.0, False, 23), -10), (T["tube"] + 0.3, sfx.chime(), -6)]
        ev += [(T["next"] - 0.4, sfx.whoosh(0.8, False, 24), -10), (T["soon"] - 0.3, sfx.whoosh(0.8, False, 25), -8),
               (T["crashes"], sfx.thud(0.4, 26), -2), (T["crashes"], sfx.clank(200, 0.3, 27), -8), (T["crashes"] + 0.05, sfx.buzz(), -8)]
        ev += [(T["light"] - 0.2, sfx.pop(28), -6), (T["red"], sfx.beep(600, 0.12), -8), (T["sensor"] - 0.2, sfx.pop(29), -6),
               (T["sees"], sfx.beep(1500, 0.08), -8), (T["bottom"], sfx.ding(), -6), (T["bottom"] + 0.2, sfx.chime(), -8)]
        ev += [(T["safe"] - 0.2, sfx.whoosh(0.9, False, 30), -6), (T["shoot"] + 0.2, sfx.whoosh(0.5, True, 31), -6)]
        ev += [(T["shoot"] + 0.2 + k * 0.42, sfx.hiss(0.25, 32 + k), -6) for k in range(4)]
        ev += [(T["stone"], sfx.thud(0.3, 36), -4), (T["skip"] + 0.1, sfx.alarm(2, 850), -12)]
        ev += [(T["long"] - 0.2, sfx.clank(500, 0.4, 37), -8), (T["shallow"], sfx.hiss(1.4, 38), -6),
               (T["splash"] - 0.2, sfx.whoosh(0.8, True, 39), -10), (T["land"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(40), 0), (T["follow"] - 0.15, sfx.pop(41), -4)]
        ev += [(T["paint"], sfx.sparkle(1.0, 12, 42), -6), (T["twist"], sfx.whoosh(1.2, True, 43), -10),
               (T["open"], sfx.clank(300, 0.5, 44), -8), (T["gates"], sfx.sparkle(0.8, 10, 45), -8)]
        ev += [(T["s1"], sfx.pop(46), -3), (T["s2"], sfx.pop(47), -3), (T["s3"], sfx.pop(48), -3)]
        ev += [(T["cong2"], sfx.pop(49), -2), (T["cong2"], sfx.sparkle(1.0, 14, 50), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.22, sfx.whoosh(0.45, False, 51), -6), (T["barefoot"], sfx.sizzle(1.2, 52), -10)]
        ev += [(T["barefoot"] + 0.29 * k, sfx.tap(53 + k), -8) for k in range(5)]
        ev += [(T["hot"], sfx.pop(58), -6), (T["womp"], sfx.womp(), -2)]
        return ev


def s_of(ep, lab):
    return ep.tl.s(lab)


# ---------------------------------------------------------------- small drawings (world space)
def rider(c, x, y, deg, col, a):
    """Someone lying feet-first on a slide: head at the back, arms crossed."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    if math.cos(math.radians(deg)) < 0:        # moving left: mirror instead of turning upside down
        c.scale(-1, 1)
        deg = 180 - deg
    c.rotate(deg)
    rect(c, -26, -14, 54, 26, col["shirt"], a, r=12)
    rect(c, 26, -10, 34, 18, col["pants"], a, r=8)
    circle(c, -36, -6, 17, col["skin"], a)
    circle(c, -40, -12, 14, col["hair"], a)
    line(c, -10, -12, 16, -22, col["skin"], 7, a)
    c.restore()


def swimhead(c, x, y, col, t):
    circle(c, x, y - 14 + 3 * math.sin(t * 3), 18, col["skin"])
    circle(c, x, y - 20 + 3 * math.sin(t * 3), 16, col["hair"])
    circle(c, x, y + 2, 34, "#E0F7FF", 0.4, stroke=4)


def splash(c, x, y, u, big=1.0):
    if u <= 0 or u >= 1:
        return
    for i in range(11):
        ang = math.pi * (0.1 + 0.8 * i / 10)
        r = (24 + 120 * u) * big
        circle(c, x + math.cos(ang) * r, y - math.sin(ang) * r * (1.1 - u * 0.5), (13 * (1 - u) + 4) * big, "#E0F2FE", 1 - u)
    circle(c, x, y, (30 + 60 * u) * big, "#FFFFFF", 0.5 * (1 - u), stroke=5)


def spray(c, x, y, t, a):
    if a <= 0:
        return
    for i in range(10):
        u = (t * 2.2 + i / 10) % 1.0
        circle(c, x - 40 * u + 10 * math.sin(i), y - 50 * math.sin(u * math.pi), 8 * (1 - u) + 3, "#E0F7FF", a * (1 - u))


def stars(c, x, y, t, a):
    if a <= 0:
        return
    for i in range(5):
        ang = t * 4 + i * 2 * math.pi / 5
        sx, sy = x + math.cos(ang) * 60, y + math.sin(ang) * 22
        pts = [(sx + math.cos(k * math.pi / 5 - math.pi / 2) * (16 if k % 2 == 0 else 7),
                sy + math.sin(k * math.pi / 5 - math.pi / 2) * (16 if k % 2 == 0 else 7)) for k in range(10)]
        poly(c, pts, YELLOW, a)


def bucket(c, x, y, t, t_pour):
    tilt = 70 * prog(t, t_pour - 0.2, t_pour + 0.2)
    c.save()
    c.translate(x, y)
    c.rotate(tilt)
    poly(c, [(-22, -26), (22, -26), (16, 22), (-16, 22)], "#EF4444")
    rect(c, -24, -30, 48, 8, "#B91C1C", r=3)
    c.restore()
    if tilt > 40:
        for i in range(6):
            u = (t * 3 + i / 6) % 1.0
            circle(c, x + 26 + 30 * u, y - 10 + 60 * u, 7, "#7DD3FC")


def palm(c, x, s, col):
    line(c, x, 0, x + 40 * s, -330 * s, shade(col, -0.25), 22 * s)
    for k in range(6):
        ang = -math.pi / 2 + (k - 2.5) * 0.55
        ex, ey = x + 40 * s + math.cos(ang) * 150 * s, -330 * s + math.sin(ang) * 80 * s + 40 * s
        poly(c, [(x + 40 * s, -330 * s), (ex, ey), (x + 40 * s + math.cos(ang) * 60 * s, -330 * s + 26 * s)], col)


NAME = "waterslide"
EPISODE = WaterSlide
