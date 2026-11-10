"""Episode 4: The Roller Coaster.  Build -> break -> fix, four times, keyed to the voiceover words.

Theme-park side view. Ground at y=0, up negative. The track is one path measured by a parameter u (arc length for the
hills and the brake run, evenly spread angle for the loop, so the loop can morph from a circle into a teardrop without
moving anything else). The train is a position u(t); its cars sit behind it along the path.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bi_base import (Episode, W, H, Track, Camera, clamp, lerp, prog, e_io, e_out, e_in, e_back, bump,  # noqa: E402
                     text, rect, grad_rect, glow, circle, poly, line, mix, shade, world, fx, sfx, ring_pts,
                     WHITE, RED, YELLOW)

SPLINE = [(-2700, -120), (-1050, -120), (-900, -200), (-200, -820), (-60, -900), (80, -860), (420, -300),
          (600, -110), (780, -150), (1060, -520), (1150, -560), (1240, -520), (1500, -160), (1650, -110), (1900, -110)]
LOOP_X, LOOP_BASE, LOOP_R, LOOP_SHIFT = 1900.0, -110.0, 300.0, 140.0
END_X = 3500.0
CAR_L, CAR_GAP = 150.0, 162.0
RAIL, RAIL_DK = "#E2E8F0", "#64748B"
TRACK_RED, TRACK_RED_DK = "#EF4444", "#991B1B"
CAR_COLS = ("#2563EB", "#F59E0B", "#10B981")

EMPH_EN = ["CONGRATS", "PUSH", "CHAIN", "TRACK", "WHEELS", "CRUSHED", "TEARDROP", "POWER", "MAGNETIC", "FOLLOW",
           "RED", "THOUSAND", "YOURSELF", "FIX"]
EMPH_SA = ["مبروك", "يدفها", "سلسلة", "السكة", "كفرات", "ينعصرون", "دمعة", "الكهربا", "مغناطيس", "تابعني",
           "أحمر", "ألف", "بيدك", "حل"]
KEYS_SA = {
    ("hook", "ROLL"): "دحرجت", ("hook", "CART"): "عربية", ("hook", "HILL"): "تلة", ("hook", "CONGRATS"): "مبروك",
    ("break1", "STOPS"): "توقف", ("break1", "BOTTOM"): "تحت", ("break1", "PUSH"): "يدفها", ("break1", "UP"): "فوق",
    ("fix1", "CHAIN"): "سلسلة", ("fix1", "DRAGS"): "تسحب", ("fix1", "TRAIN"): "القطار", ("fix1", "HILL"): "التلة",
    ("fix1", "SAFETY"): "أمان", ("fix1", "DOGS"): "مسكات", ("fix1", "CLACK"): "تطقطق", ("fix1", "RATCHET"): "مسننات",
    ("fix1", "NEVER"): "أبد", ("fix1", "BACK"): "ورا",
    ("break2", "THRILLING"): "حماس", ("break2", "FAST"): "سريعة", ("break2", "THROWS"): "ترمي",
    ("break2", "TRACK"): "السكة",
    ("fix2", "GIVE"): "تحط", ("fix2", "THREE"): "ثلاث", ("fix2", "WHEELS"): "كفرات", ("fix2", "TOP"): "فوق",
    ("fix2", "SIDE"): "جنب", ("fix2", "UNDERNEATH"): "تحت", ("fix2", "LOCKED"): "مقفولة",
    ("break3", "ROUND"): "دائرية", ("break3", "LOOP"): "لفة", ("break3", "RIDERS"): "الركاب",
    ("break3", "CRUSHED"): "ينعصر",
    ("fix3", "STRETCH"): "تمط", ("fix3", "LOOP"): "اللفة", ("fix3", "TEARDROP"): "دمعة", ("fix3", "TIGHT"): "ضيقة",
    ("fix3", "WIDE"): "واسعة", ("fix3", "LOCK"): "تقفل", ("fix3", "SHOULDER"): "أكتاف", ("fix3", "BARS"): "مساند",
    ("break4", "EVERYTHING"): "كل", ("break4", "STOP"): "توقف", ("break4", "POWER"): "الكهربا",
    ("break4", "OUT"): "تطفي",
    ("fix4", "MAGNETIC"): "مغناطيس", ("fix4", "BRAKES"): "فرامل", ("fix4", "POWER"): "كهربا",
    ("fix4", "FASTER"): "أسرع", ("fix4", "TRAIN"): "القطار", ("fix4", "HARDER"): "أقوى", ("fix4", "SLOW"): "هدته",
    ("cta", "FOLLOW"): "تابعني",
    ("reveal", "PAINT"): "اصبغ", ("reveal", "TRACK"): "السكة", ("reveal", "RED"): "أحمر", ("reveal", "LINE"): "طابور",
    ("reveal", "ZIGZAGS"): "يتعرج",
    ("stat", "ONE"): "تلة", ("stat", "LOOP"): "لفة", ("stat", "THOUSAND"): "ألف",
    ("closer", "CONGRATS"): "مبروك",
    ("tag", "LINE"): "الطابور", ("tag", "TWO"): "ساعتين", ("tag", "FIX"): "حل",
}
TEXT = {
    "en": {"follow": ("FOLLOW", "next: a water slide"),
           "stat": [("1", "HILL"), ("1", "LOOP"), ("1000", "RIDERS / HOUR")],
           "chain": "CHAIN LIFT", "dogs": "ANTI-ROLLBACK", "top": "TOP", "side": "SIDE", "under": "UNDER",
           "locked": "LOCKED ON", "g": "G", "tight": "TIGHT", "wide": "WIDE", "bars": "SHOULDER BARS",
           "magnets": "MAGNETS", "nopower": "NO POWER", "wait": "WAIT", "hours": "2 HRS", "hours2": "3 HRS"},
    "ar_sa": {"follow": ("تابعني", "الجاي: زحليقة موية"),
              "stat": [("1", "تلة"), ("1", "لفة"), ("1000", "راكب بالساعة")],
              "chain": "سلسلة", "dogs": "ضد الرجوع", "top": "فوق", "side": "جنب", "under": "تحت",
              "locked": "مقفولة", "g": "G", "tight": "ضيقة", "wide": "واسعة", "bars": "مساند أكتاف",
              "magnets": "مغناطيس", "nopower": "بدون كهربا", "wait": "انتظار", "hours": "ساعتين", "hours2": "3 ساعات"},
}


def catmull(pts, n=28):
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


class Path:
    def __init__(self):
        a = catmull(SPLINE)
        self.ax, self.ay, self.au = [a[0][0]], [a[0][1]], [0.0]
        for (x0, y0), (x1, y1) in zip(a, a[1:]):
            d = math.hypot(x1 - x0, y1 - y0)
            if d < 1e-6:
                continue
            self.ax.append(x1)
            self.ay.append(y1)
            self.au.append(self.au[-1] + d)
        self.LA = self.au[-1]
        self.LL = 2 * math.pi * LOOP_R + LOOP_SHIFT
        self.LB = END_X - (LOOP_X + LOOP_SHIFT)
        self.U = self.LA + self.LL + self.LB

    def pos(self, u, m=0.0):
        if u <= self.LA:
            u = max(u, 0.0)
            lo, hi = 0, len(self.au) - 1
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if self.au[mid] <= u:
                    lo = mid
                else:
                    hi = mid
            f = (u - self.au[lo]) / max(1e-9, self.au[hi] - self.au[lo])
            return lerp(self.ax[lo], self.ax[hi], f), lerp(self.ay[lo], self.ay[hi], f)
        if u <= self.LA + self.LL:
            th = 2 * math.pi * (u - self.LA) / self.LL
            rb, rt = LOOP_R * (1 + 0.15 * m), LOOP_R * (1 - 0.42 * m)
            rx = rb * (1 + math.cos(th)) / 2 + rt * (1 - math.cos(th)) / 2
            hh = 2 * LOOP_R * (1 + 0.24 * m)
            return LOOP_X + rx * math.sin(th) + LOOP_SHIFT * th / (2 * math.pi), LOOP_BASE - hh * (1 - math.cos(th)) / 2
        return LOOP_X + LOOP_SHIFT + (u - self.LA - self.LL), LOOP_BASE

    def angle(self, u, m=0.0):
        x0, y0 = self.pos(u - 2, m)
        x1, y1 = self.pos(u + 2, m)
        return math.atan2(y1 - y0, x1 - x0)


class Coaster(Episode):
    EMPH = {"en": EMPH_EN, "ar_sa": EMPH_SA}
    KEYS = {"ar_sa": KEYS_SA}
    TEXT = TEXT
    STAT_COLORS = ("#111827", "#111827", "#EF4444")

    def _tracks(self):
        tl = self.tl
        s, e = tl.s, tl.e
        P = self.path = Path()
        # landmarks on the path
        def lowest_in(x0, x1):
            return max(((u, P.pos(u)[1]) for u in range(0, int(P.LA), 4) if x0 <= P.pos(u)[0] <= x1), key=lambda q: q[1])[0]

        def highest_in(x0, x1):
            return min(((u, P.pos(u)[1]) for u in range(0, int(P.LA), 4) if x0 <= P.pos(u)[0] <= x1), key=lambda q: q[1])[0]

        self.u_crest = highest_in(-300, 200)
        self.u_valley = lowest_in(400, 800)
        self.u_air = highest_in(900, 1400)
        self.u_lift0 = next(u for u in range(0, int(P.LA), 4) if P.pos(u)[0] >= -1000)
        self.u_station = next(u for u in range(0, int(P.LA), 4) if P.pos(u)[0] >= -1250)
        self.u_loop0 = P.LA
        self.u_loop1 = P.LA + P.LL
        self.u_brake0 = P.LA + P.LL + 500
        self.u_end = P.U - 80
        self.anchors({
            "roll": ("hook", "ROLL", 0.1), "cart": ("hook", "CART", 0.2), "hill": ("hook", "HILL", 0.35),
            "cong": ("hook", "CONGRATS", 0.5),
            "stops": ("break1", "STOPS", 0.15), "bottom": ("break1", "BOTTOM", 0.3), "push": ("break1", "PUSH", 0.6),
            "up": ("break1", "UP", 0.97),
            "chain": ("fix1", "CHAIN", 0.15), "drags": ("fix1", "DRAGS", 0.2), "train": ("fix1", "TRAIN", 0.27),
            "hill1": ("fix1", "HILL", 0.4), "safety": ("fix1", "SAFETY", 0.5), "dogs": ("fix1", "DOGS", 0.57),
            "clack": ("fix1", "CLACK", 0.63), "ratchet": ("fix1", "RATCHET", 0.73), "never": ("fix1", "NEVER", 0.88),
            "back": ("fix1", "BACK", 0.97),
            "thrilling": ("break2", "THRILLING", 0.15), "fast": ("break2", "FAST", 0.45),
            "throws": ("break2", "THROWS", 0.57), "track": ("break2", "TRACK", 0.93),
            "give": ("fix2", "GIVE", 0.1), "three": ("fix2", "THREE", 0.25), "wheels": ("fix2", "WHEELS", 0.35),
            "top": ("fix2", "TOP", 0.43), "side": ("fix2", "SIDE", 0.67), "under": ("fix2", "UNDERNEATH", 0.76),
            "locked": ("fix2", "LOCKED", 0.92),
            "round": ("break3", "ROUND", 0.25), "loop": ("break3", "LOOP", 0.32), "riders": ("break3", "RIDERS", 0.55),
            "crushed": ("break3", "CRUSHED", 0.7),
            "stretch": ("fix3", "STRETCH", 0.08), "teardrop": ("fix3", "TEARDROP", 0.28), "tight": ("fix3", "TIGHT", 0.37),
            "wide": ("fix3", "WIDE", 0.52), "lock": ("fix3", "LOCK", 0.7), "bars": ("fix3", "BARS", 0.95),
            "flows": ("break4", "EVERYTHING", 0.1), "stop": ("break4", "STOP", 0.6), "power": ("break4", "POWER", 0.8),
            "out": ("break4", "OUT", 0.95),
            "magnetic": ("fix4", "MAGNETIC", 0.12), "nopower": ("fix4", "POWER", 0.35), "faster": ("fix4", "FASTER", 0.53),
            "harder": ("fix4", "HARDER", 0.8), "slow": ("fix4", "SLOW", 0.9),
            "follow": ("cta", "FOLLOW", 0.4),
            "paint": ("reveal", "PAINT", 0.15), "red": ("reveal", "RED", 0.4), "line": ("reveal", "LINE", 0.65),
            "zigzag": ("reveal", "ZIGZAGS", 0.8),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "LOOP", 0.38), "s3": ("stat", "THOUSAND", 0.6),
            "cong2": ("closer", "CONGRATS", 0.1),
            "line2": ("tag", "LINE", 0.1), "two": ("tag", "TWO", 0.25), "fix": ("tag", "FIX", 0.95),
        })
        T = self.T
        T["womp"] = e("tag") + 0.35
        T["blackout"] = T["power"] + 0.25
        # track visible from v0 to v1 (path parameter)
        self.v0 = Track(self.u_crest - 120.0).to(T["chain"] - 0.2, 0.0, 0.8, e_out)
        self.v1 = Track(self.u_crest + 260.0).to(0.0, self.u_valley + 420.0, 0.7, e_out)
        self.v1.to(T["thrilling"] - 0.6, self.u_loop0, 0.8, e_out)
        self.v1.to(T["round"] - 0.5, self.u_loop1 + 150, 0.6, e_io)
        self.v1.to(T["flows"] - 0.4, P.U, 0.9, e_out)
        self.morph = Track(0.0).to(T["stretch"], 1.0, max(0.8, T["teardrop"] + 0.3 - T["stretch"]), e_io)
        self.paint = Track(0.0).to(T["paint"], 1.0, max(0.8, T["red"] + 0.3 - T["paint"]), e_io)
        # the cart (hook / break1)
        uc, uv = self.u_crest, self.u_valley
        cart = self.cart = Track(uc - 40.0)
        cart.to(T["roll"], uv, 0.95, e_in).to(T["roll"] + 0.95, uv + 300, 0.7, e_out)
        cart.to(T["roll"] + 1.65, uv - 170, 1.0, e_io).to(T["roll"] + 2.65, uv + 90, 0.9, e_io)
        cart.to(T["roll"] + 3.55, uv, 0.9, e_io)
        cart.to(T["push"] - 0.3, uv - 260, max(0.8, T["up"] + 0.3 - T["push"]), e_io)
        # the train (from fix1): head position on the path
        tr = self.train = Track(self.u_station + 2 * CAR_GAP)
        crest_u = self.u_crest - 70
        lift_time = max(2.2, T["safety"] + 0.2 - T["drags"])
        tr.to(T["drags"] - 0.1, crest_u - 260, lift_time, lambda x: x)                    # up the chain lift
        tr.to(T["never"] - 0.05, crest_u - 285, 0.25, e_out)                               # tries to roll back
        tr.to(T["never"] + 0.25, crest_u - 276, 0.15, e_out)                               # caught by the dogs
        tr.to(s("break2") - 0.25, crest_u + 30, 0.6, e_in)                                 # over the top
        tr.to(T["thrilling"] + 0.05, self.u_valley + 2 * CAR_GAP, 0.75, e_in)              # first drop
        tr.to(T["fast"] - 0.2, self.u_air + CAR_GAP, 0.75, e_out)                          # up the fast hill
        tr.to(T["give"] - 0.4, self.u_air + CAR_GAP, 0.01)                                 # parked for the close-up
        tr.to(T["locked"] + 0.25, self.u_loop0 - 120, 0.9, e_in)                           # over the hill, wheels locked
        tr.to(T["riders"] - 0.6, self.u_loop1 + 2 * CAR_GAP + 40, 1.1, lambda x: x)        # through the round loop
        tr.to(T["crushed"] + 0.8, self.u_loop1 + 2 * CAR_GAP + 900, 0.9, e_in)             # leaves to the right
        tr.to(s("fix3") - 0.2, self.u_loop0 - 800, 0.01)                                   # comes back from the left
        tr.to(s("fix3"), self.u_loop0 - 300, 0.9, e_out)                                    # waits at the loop
        tr.to(T["tight"] - 0.7, self.u_loop1 + 2 * CAR_GAP + 300, 1.6, lambda x: x)        # smooth teardrop pass
        tr.to(T["flows"] - 0.3, crest_u + 60, 0.01)                                        # full ride from the top
        tr.to(T["flows"] - 0.25, self.u_valley + 2 * CAR_GAP, 0.7, e_in)
        tr.to(T["flows"] + 0.45, self.u_air + 2 * CAR_GAP, 0.6, lambda x: x)
        tr.to(T["flows"] + 1.05, self.u_loop1 + 2 * CAR_GAP, 1.0, lambda x: x)
        tr.to(T["flows"] + 2.05, self.u_end - 300, max(0.8, T["out"] + 0.2 - T["flows"] - 2.05), lambda x: x)
        tr.to(T["magnetic"] - 0.3, self.u_loop1 + 2 * CAR_GAP + 120, 0.01)                 # replay into the brakes
        tr.to(T["faster"] - 0.3, self.u_brake0 + 380, max(0.5, T["harder"] - T["faster"] + 0.2), e_out)
        tr.to(T["slow"] + 0.3, self.u_end - 200, 0.9, e_out)
        tr.to(s("reveal") - 0.2, self.u_station + 2 * CAR_GAP, 0.01)                        # back in the station
        tr.to(T["s1"] - 0.3, self.u_loop1 + 2 * CAR_GAP, max(2.5, T["cong2"] - T["s1"]), e_io)
        self.lift = Track(0.0).to(T["throws"] - 0.05, 1.0, 0.5, e_out).to(T["give"] - 0.45, 0.0, 0.3)
        self.wheel = [Track(0.0).to(T[k] - 0.15, 1.0, 0.35, e_back) for k in ("top", "side", "under")]
        self.bars = Track(0.0).to(T["lock"] - 0.1, 1.0, 0.6, e_out)
        self.dark = Track(0.0).to(T["blackout"], 1.0, 0.15).to(T["slow"] + 0.6, 0.0, 0.6)
        self.mag = Track(0.0).to(T["magnetic"] - 0.2, 1.0, 0.5)
        self.queue = Track(0.0).to(T["line"] - 0.2, 1.0, 0.7)
        # camera
        cam = self.cam = Camera(280, -260, 0.85)
        cam.key(0.05, 330, -250, 0.92, 2.5)
        cam.key(T["push"] - 0.6, 420, -230, 1.05, 0.6)
        cam.key(T["chain"] - 0.45, -800, -390, 0.62, 0.6)
        def at(u, dy=0.0):
            x, y = self.path.pos(u)
            return x, y + dy
        x, y = at(tr.at(T["train"] + 0.6) - 60, 0)
        cam.key(T["drags"] + 0.1, x, y - 30, 0.8, 1.0)
        x, y = at(tr.at(T["dogs"]) - 2 * CAR_GAP)
        cam.key(T["safety"] - 0.35, x, y + 25, 2.3, 0.5)
        cam.key(T["back"] + 0.4, -250, -560, 0.75, 0.5)
        cam.key(s("break2") - 0.1, 700, -420, 0.55, 0.6)
        cam.key(T["throws"] - 0.3, 1150, -500, 0.85, 0.4)
        x, y = at(self.u_air)
        cam.key(T["give"] - 0.4, x + 60, y - 20, 2.5, 0.5)
        cam.key(T["locked"] + 0.35, 1450, -330, 0.62, 0.6)
        cam.key(s("break3") - 0.1, 2020, -280, 0.8, 0.6)
        x, y = at(self.u_loop1 + 300)
        cam.key(T["lock"] - 0.45, x + 40, y - 20, 2.3, 0.4)
        cam.key(T["bars"] + 0.35, 2040, -320, 0.72, 0.5)
        cam.key(s("break4") - 0.1, 1200, -420, 0.45, 0.5)
        cam.key(T["stop"] - 0.3, 2700, -260, 0.62, 0.8)
        cam.key(T["magnetic"] - 0.35, 2850, -260, 0.75, 0.5)
        cam.key(s("cta") + 0.2, 500, -520, 0.23, 3.0)
        cam.key(T["line"] - 0.4, -1950, -220, 0.62, 0.6)
        cam.key(s("stat") - 0.1, 450, -520, 0.24, 0.8)
        cam.key(s("closer") - 0.1, 450, -500, 0.25, 2.4)
        cam.key(s("tag") - 0.22, -1720, -170, 1.75, 0.45)
        self.shakes = [(T["throws"] + 0.1, 0.5, 12), (T["crushed"] - 0.1, 0.5, 10), (T["blackout"], 0.3, 6)]

    def red_level(self, t):
        T = self.T
        return (0.8 * bump(t, T["push"] - 0.2, T["up"] + 0.8) + 0.9 * bump(t, T["throws"], T["track"] + 1.0)
                + 0.9 * bump(t, T["crushed"] - 0.3, T["crushed"] + 1.4) + 0.8 * bump(t, T["blackout"], T["out"] + 1.2))

    # ------------------------------------------------------------------ backdrop
    def draw_backdrop(self, c, t, dusk):
        cx, cy, z = self.cam_state
        gy = (0 - cy) * z + H / 2
        zf = clamp(0.6 * z ** 0.6, 0.15, 0.9)
        c.save()
        c.translate(W / 2, gy)
        c.scale(zf, zf)
        c.translate(-cx * 0.22, 0)
        far = "#A9C9E8"
        # Ferris wheel
        fx_, fr = -1400, 560
        line(c, fx_ - 260, 0, fx_, -fr - 80, far, 30)
        line(c, fx_ + 260, 0, fx_, -fr - 80, far, 30)
        circle(c, fx_, -fr - 80, fr, far, stroke=26)
        for i in range(12):
            a = t * 0.15 + i * math.pi / 6
            line(c, fx_, -fr - 80, fx_ + math.cos(a) * fr, -fr - 80 + math.sin(a) * fr, far, 8)
            rect(c, fx_ + math.cos(a) * fr - 34, -fr - 80 + math.sin(a) * fr, 68, 56, far, r=12)
        # tents and towers
        for i, x in enumerate(range(-3600, 3800, 700)):
            if abs(x - fx_) < 500:
                continue
            h = 260 + (i * 97) % 220
            poly(c, [(x - 220, 0), (x - 220, -h), (x, -h - 200), (x + 220, -h), (x + 220, 0)], far)
            line(c, x, -h - 200, x, -h - 300, far, 10)
            poly(c, [(x, -h - 300), (x + 90, -h - 270), (x, -h - 240)], "#C3D8EE")
        c.restore()

    # ------------------------------------------------------------------ world
    def draw_world(self, c, t, dusk, z):
        T = self.T
        world.ground(c, -8000, 8000, 4000, dusk)
        for x in (-3000, -2200, 2600, 3900):
            world.tree(c, x, 1.6, dusk, int(abs(x)) % 3)
        self.draw_station(c, t)
        self.draw_queue(c, t)
        self.draw_track(c, t, z)
        self.draw_magnets(c, t)
        self.draw_train(c, t, z)
        self.draw_people(c, t)

    def draw_station(self, c, t):
        a = prog(t, self.T["chain"] - 0.4, self.T["chain"])
        if a <= 0:
            return
        x0, x1 = -1650, -1080
        rect(c, x0, -100, x1 - x0, 100, "#CBD5E1", a)
        rect(c, x0, -110, x1 - x0, 14, "#94A3B8", a)
        for x in (x0 + 20, x1 - 40):
            rect(c, x, -420, 20, 320, "#64748B", a)
        poly(c, [(x0 - 60, -400), (x1 + 60, -400), (x1 + 20, -470), (x0 - 20, -470)], "#F97316", a)
        for i in range(8):
            xx = x0 - 50 + i * (x1 - x0 + 100) / 8
            poly(c, [(xx, -400), (xx + (x1 - x0 + 100) / 8, -400), (xx + (x1 - x0 + 100) / 16, -370)],
                 "#FDE68A" if i % 2 else "#F97316", a)

    def draw_queue(self, c, t):
        q = self.queue.at(t)
        if q <= 0:
            return
        x0, x1 = -2650, -1700
        # zigzag rails (switchbacks seen from the side as stacked rails)
        for r in range(4):
            y = -40 - r * 46
            xa = x0 + (60 if r % 2 else 0)
            xb = x1 - (0 if r % 2 else 60)
            line(c, xa, y, xa + (xb - xa) * e_out(q), y, "#94A3B8", 8, q)
            for x in range(int(xa), int(xa + (xb - xa) * q), 120):
                line(c, x, y, x, y + 40, "#64748B", 6, q)
        # sign
        rect(c, -1700, -330, 14, 330, "#475569", q)
        rect(c, -1830, -440, 260, 120, "#111827", q, r=10)
        if arabic_text(self.tx["wait"]):
            from bik import arabic as _ar
            _ar.text_ar(c, self.tx["wait"], -1700, -394, 38, "#FACC15")
        else:
            text(c, self.tx["wait"], -1700, -398, 34, "#FACC15", "Poppins-Black")
        flip = prog(t, self.T["fix"] - 0.6, self.T["fix"] - 0.3)
        txt = self.tx["hours2"] if flip > 0.5 else self.tx["hours"]
        if arabic_text(txt):
            from bik import arabic as _ar
            _ar.text_ar(c, txt, -1700, -342, 46, "#FFFFFF")
        else:
            text(c, txt, -1700, -342, 46, "#FFFFFF", "Poppins-Black")

    def track_col(self, t, u):
        p = self.paint.at(t)
        if p <= 0:
            return RAIL, RAIL_DK
        k = clamp((p * (self.path.U + 400) - u) / 300)
        return mix(RAIL, TRACK_RED, k), mix(RAIL_DK, TRACK_RED_DK, k)

    def draw_track(self, c, t, z):
        T, P = self.T, self.path
        m = self.morph.at(t)
        v0, v1 = self.v0.at(t), self.v1.at(t)
        step = 10.0 if z > 0.5 else 22.0
        pts = []
        u = v0
        while u <= v1:
            pts.append((u, P.pos(u, m)))
            u += step
        if len(pts) < 2:
            return
        # supports
        for u, (x, y) in pts:
            if y < -140 and int(u) % 180 < step and not (self.u_loop0 < u < self.u_loop1):
                line(c, x, y + 20, x, 0, "#94A3B8", 12)
        loop_on = v1 > self.u_loop0 + 50
        if loop_on:
            line(c, LOOP_X + 30, 0, LOOP_X + LOOP_SHIFT / 2, LOOP_BASE - 20, "#94A3B8", 14)
            line(c, LOOP_X + LOOP_SHIFT + 110, 0, LOOP_X + LOOP_SHIFT / 2 + 40, LOOP_BASE - 20, "#94A3B8", 14)
        # spine + ties + rail
        for (ua, (xa, ya)), (ub, (xb, yb)) in zip(pts, pts[1:]):
            col, dk = self.track_col(t, ua)
            ang = math.atan2(yb - ya, xb - xa)
            nx, ny = -math.sin(ang), math.cos(ang)
            line(c, xa + nx * 22, ya + ny * 22, xb + nx * 22, yb + ny * 22, dk, 12)
            line(c, xa, ya, xb, yb, col, 16)
            if int(ua) % 60 < step:
                line(c, xa, ya, xa + nx * 22, ya + ny * 22, dk, 6)
        # chain on the lift + anti-rollback teeth
        ch = prog(t, T["chain"] - 0.2, T["chain"] + 0.3)
        if ch > 0 and v0 < self.u_crest:
            for u in range(int(self.u_lift0), int(self.u_crest - 90), 18):
                x, y = P.pos(u)
                ang = P.angle(u)
                nx, ny = -math.sin(ang), math.cos(ang)
                ph = (t * 140) % 18
                xx, yy = P.pos(u + ph)
                circle(c, xx + nx * 34, yy + ny * 34, 5, "#334155", ch)
                tooth = [(x + nx * 10, y + ny * 10), (x + nx * 10 + math.cos(ang) * 14, y + ny * 10 + math.sin(ang) * 14),
                         (x + nx * 2 + math.cos(ang) * 14, y + ny * 2 + math.sin(ang) * 14)]
                poly(c, tooth, "#475569", ch)

    def draw_magnets(self, c, t):
        a = self.mag.at(t)
        if a <= 0:
            return
        P = self.path
        head = self.train.at(t)
        for i, u in enumerate(range(int(self.u_brake0), int(self.u_end), 70)):
            x, y = P.pos(u)
            near = clamp(1 - abs((head - CAR_GAP) - u) / 260) if self.speed(t) > 30 else 0
            k = e_back(prog(t, self.T["magnetic"] - 0.2 + i * 0.03, self.T["magnetic"] + 0.15 + i * 0.03))
            rect(c, x - 22, y + 26, 44, 30 * k, "#EF4444" if i % 2 else "#3B82F6", a, r=5)
            if near > 0:
                glow(c, x, y + 40, 60, "#93C5FD", 0.7 * near)

    def speed(self, t):
        return abs(self.train.at(t + 0.04) - self.train.at(t - 0.04)) / 0.08

    # ------------------------------------------------------------------ cars
    def car_poses(self, t, head, n):
        P, m = self.path, self.morph.at(t)
        out = []
        for i in range(n):
            u = head - i * CAR_GAP
            x, y = P.pos(u, m)
            out.append((x, y, P.angle(u, m), u))
        return out

    def draw_train(self, c, t, z):
        T, tl = self.T, self.tl
        # the single cart (hook / break1)
        ca = 1 - prog(t, T["chain"] - 0.4, T["chain"])
        if ca > 0:
            x, y, ang, u = self.car_poses(t, self.cart.at(t), 1)[0]
            self.draw_car(c, t, x, y, ang, CAR_COLS[0], ca, riders=1, cart=True, idx=0)
        if t < T["chain"] - 0.4:
            return
        head = self.train.at(t)
        a = prog(t, T["chain"] - 0.4, T["chain"])
        lift = self.lift.at(t)
        for i, (x, y, ang, u) in enumerate(self.car_poses(t, head, 3)):
            off = 0.0
            spin = 0.0
            if lift > 0:
                off = lift * (90 + 50 * i) * (1 + 0.2 * math.sin(t * 9 + i))
                spin = lift * (14 - 12 * i) * math.sin(t * 6 + i)
            nx, ny = math.sin(ang), -math.cos(ang)
            self.draw_car(c, t, x + nx * off, y + ny * off, ang + math.radians(spin), CAR_COLS[i], a, riders=2, idx=i)

    def draw_car(self, c, t, x, y, ang, col, a, riders=2, cart=False, idx=0):
        T = self.T
        c.save()
        c.translate(x, y)
        c.rotate(math.degrees(ang))
        L = CAR_L
        # wheels: road on top of the rail; guide on the rail; upstop under it (from fix2)
        full = prog(t, T["top"] - 0.15, T["top"]) if not cart else 0.0
        wk = [w.at(t) for w in self.wheel]
        for wx in (-L * 0.32, L * 0.32):
            circle(c, wx, -14, 13, "#1F2937", a)
            circle(c, wx, -14, 5, "#9CA3AF", a)
            if wk[1] > 0:
                circle(c, wx, 0, 11 * wk[1], "#0F172A", a)
                circle(c, wx, 0, 4 * wk[1], "#CBD5E1", a)
            if wk[2] > 0:
                circle(c, wx, 18, 10 * wk[2], "#1F2937", a)
                circle(c, wx, 18, 4 * wk[2], "#9CA3AF", a)
            if wk[2] > 0 or wk[1] > 0:
                line(c, wx, -14, wx, 18 * max(wk[2], 0.01), "#475569", 6, a)
        # body
        body_y = -30
        rect(c, -L / 2, body_y - 50, L, 50, col, a, r=14)
        rect(c, -L / 2, body_y - 50, L, 12, shade(col, 0.25), a, r=8)
        rect(c, L / 2 - 26, body_y - 70, 20, 40, shade(col, -0.2), a, r=6)
        # riders
        crushed = bump(t, T["riders"] - 0.3, T["crushed"] + 1.2) if not cart else 0.0
        bars = self.bars.at(t) if not cart else 0.0
        for r in range(riders):
            rx = -L * 0.22 + r * L * 0.4 if riders > 1 else 0
            sy = 1 - 0.45 * crushed
            cs = world.crowd_colors(idx * 2 + r + 1)
            head_y = body_y - 50 - 30 * sy
            rect(c, rx - 16, body_y - 50 - 34 * sy, 32, 36 * sy, cs["shirt"], a, r=10)
            circle(c, rx, head_y - 8 * sy, 15, cs["skin"], a)
            circle(c, rx, head_y - 14 * sy, 13, cs["hair"], a)
            up = 0.0 if crushed > 0.2 else (0.8 + 0.2 * math.sin(t * 6 + r))
            if bars < 0.5:
                for side in (-1, 1):
                    line(c, rx + side * 12, body_y - 64 * sy, rx + side * 22, body_y - 64 * sy - 40 * up, cs["skin"], 7, a)
            if bars > 0:
                yb = lerp(body_y - 140, body_y - 62, bars)
                line(c, rx - 22, yb, rx - 22, yb + 40, "#111827", 9, a)
                line(c, rx - 22, yb, rx + 18, yb - 6, "#111827", 9, a)
        if not cart:
            # anti-rollback dog under the car (a little pawl)
            k = (self.train.at(t) % 18) / 18
            pawl = math.radians(25 + 20 * (1 - k)) if T["drags"] < t < T["thrilling"] else math.radians(10)
            px, py = -L * 0.45, 26
            line(c, px, py - 10, px + math.cos(pawl) * 26, py - 10 + math.sin(pawl) * 26, "#F97316", 8, a)
        c.restore()

    # ------------------------------------------------------------------ people
    def draw_people(self, c, t):
        T, tl = self.T, self.tl
        P = world.person
        # break1: someone pushes the cart back up
        a = prog(t, T["bottom"] - 0.1, T["bottom"] + 0.3) * (1 - prog(t, T["chain"] - 0.4, T["chain"] - 0.1))
        if a > 0:
            u = self.cart.at(t) + CAR_L * 0.65
            x, y = self.path.pos(u)
            ang = self.path.angle(u)
            P(c, x, y - 4, 130, shirt="#8B5CF6", lean=-1.6 * prog(t, T["push"] - 0.4, T["push"]), a=a,
              walk=t * 1.4 if T["push"] < t < T["up"] + 0.3 else 0, sweat=prog(t, T["push"], T["up"]))
        # queue (reveal + tag)
        q = self.queue.at(t)
        if q > 0:
            for i in range(14):
                r = i // 4
                x = -2600 + 70 + (i % 4) * 220 + (110 if r % 2 else 0)
                y = -40 - r * 46
                ai = q * prog(t, T["line"] - 0.1 + i * 0.05, T["line"] + 0.2 + i * 0.05)
                sag = bump(t, T["two"] - 0.1, T["two"] + 2.5)
                P(c, x, y + 30, 112, lean=0.25 * sag * math.sin(i), a=ai, **world.crowd_colors(i))
            # the engineer at the sign
            ea = prog(t, tl.s("tag") - 0.4, tl.s("tag"))
            if ea > 0:
                sh = bump(t, T["fix"] - 0.7, T["fix"] + 0.9)
                P(c, -1560, 0, 140, shirt="#F97316", arms_up=0.85 * sh, a=ea)
                rect(c, -1586, -158, 52, 14, YELLOW, ea, r=7)
                rect(c, -1578, -178, 36, 24, YELLOW, ea, r=11)

    # ------------------------------------------------------------------ overlays
    def draw_overlays(self, c, t, tw, dusk):
        T, tx, tl = self.T, self.tx, self.tl
        P = self.path
        dk = self.dark.at(tw)
        if dk > 0:
            fx.dim(c, W, H, 0.62 * dk, "#020617")
            x, y = self.sc(2700, -700)
            self.pill(c, tx["nopower"], W / 2, 420, dk * prog(tw, T["blackout"], T["blackout"] + 0.25),
                      fg="#FFFFFF", bg="#111827", size=44)
        head = self.train.at(tw)
        # outlines
        cx_, cy_ = P.pos(self.cart.at(tw))
        self.outline(c, tw, T["cong"] + 0.05, (cx_ - 100, cy_ - 140, 200, 170), 1.1)
        self.outline(c, tw, T["chain"] + 0.1, (-1000, -900, 900, 820), 1.2)
        u_last = head - 2 * CAR_GAP
        lx, ly = P.pos(u_last)
        self.outline(c, tw, T["ratchet"] - 0.1, (lx - 110, ly - 10, 110, 70), 1.2)
        ax, ay = P.pos(self.u_air)
        for key, (ox, oy, ww, hh) in (("top", (-15, -29, 30, 30)), ("side", (-12, -12, 24, 24)), ("under", (-11, 7, 22, 22))):
            self.outline(c, tw, T[key] + 0.05, (ax + CAR_L * 0.32 + ox, ay + oy, ww, hh), 1.0, r=10, width=6, pad=4)
        mx = LOOP_X + LOOP_SHIFT / 2
        top_y = LOOP_BASE - 2 * LOOP_R * (1 + 0.24 * self.morph.at(tw))
        self.outline(c, tw, T["teardrop"] + 0.1, (mx - 340, top_y - 40, 680, LOOP_BASE - top_y + 60), 1.2)
        self.outline(c, tw, T["magnetic"] + 0.15, (P.pos(self.u_brake0)[0] - 30, -110, P.pos(self.u_end)[0] - P.pos(self.u_brake0)[0] + 60, 90), 1.2)
        # labels
        self.wpill(c, tw, tx["chain"], -560, -680, T["chain"], T["safety"] - 0.4, dx=-60)
        self.wpill(c, tw, tx["dogs"], lx - 60, ly + 100, T["dogs"], T["back"] + 0.4, fg="#FFFFFF", bg="#F97316", size=34)
        wx = ax + CAR_L * 0.32
        for key, dy, wy in (("top", -46, -14), ("side", 2, 0), ("under", 50, 18)):
            p = prog(tw, T[key], T[key] + 0.3) * (1 - prog(tw, T["locked"] + 0.3, T["locked"] + 0.55))
            if p > 0:
                x0, y0 = self.sc(wx + 14, ay + wy)
                x1, y1 = self.sc(wx + 70, ay + dy)
                line(c, x0, y0, x1, y1, "#FFFFFF", 5, p)
                circle(c, x0, y0, 7, "#FFFFFF", p)
                self.pill(c, tx[key], x1 + 80, y1, p, size=38)
        self.wpill(c, tw, tx["locked"], wx - 40, ay - 150, T["locked"] - 0.05, T["locked"] + 0.9, fg="#FFFFFF", bg="#16A34A", size=40)
        gv = bump(tw, T["riders"] - 0.2, T["crushed"] + 1.3)
        if gv > 0:
            x, y = self.sc(mx, top_y - 90)
            self.pill(c, ["12", tx["g"]], x, y, gv, fg="#FFFFFF", bg=RED, size=46)
        gv = bump(tw, T["wide"] - 0.6, T["wide"] + 1.0)
        if gv > 0:
            x, y = self.sc(mx, top_y - 90)
            self.pill(c, ["4", tx["g"]], x, y, gv, fg="#FFFFFF", bg="#16A34A", size=46)
        self.wpill(c, tw, tx["tight"], mx + 260, top_y + 40, T["tight"], T["lock"] - 0.5, size=36)
        self.wpill(c, tw, tx["wide"], mx + 330, LOOP_BASE - 120, T["wide"], T["lock"] - 0.5, size=36)
        bx, by = P.pos(self.u_loop1 + 300)
        self.wpill(c, tw, tx["bars"], bx, by - 230, T["lock"], T["bars"] + 0.4, size=34)
        self.wpill(c, tw, tx["magnets"], 2850, 60, T["magnetic"], T["slow"] + 0.4, fg="#FFFFFF", bg="#2563EB")
        # alerts + checks
        cx_, cy_ = P.pos(self.cart.at(tw))
        self.alert(c, tw, T["push"], T["chain"] - 0.3, cx_ + 60, cy_ - 260)
        self.alert(c, tw, T["throws"] + 0.1, T["give"] - 0.3, 1150, -900)
        self.alert(c, tw, T["crushed"], T["stretch"] - 0.2, mx + 330, top_y - 40)
        self.alert(c, tw, T["blackout"] + 0.1, T["magnetic"] - 0.3, 3200, -420)
        self.check(c, tw, T["back"] + 0.25, lx + 120, ly - 160, size=1.2)
        self.check(c, tw, T["locked"] + 0.2, ax + 240, ay - 160)
        self.check(c, tw, T["bars"] + 0.2, bx + 220, by - 240)
        self.check(c, tw, T["slow"] + 0.35, 3200, -380)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, tl = self.T, self.tl
        s, e = tl.s, tl.e
        ev = [(0.0, sfx.whoosh(0.5, True, 1), -10), (0.05, sfx.pop(2), -6), (T["roll"], sfx.whirr(1.4, 150, 420, 3), -8),
              (T["roll"] + 0.9, sfx.whoosh(0.8, False, 4), -6), (T["cong"], sfx.pop(), -2), (T["cong"], sfx.sparkle(), -8)]
        ev += [(T["stops"], sfx.thud(0.3, 5), -8), (T["push"] - 0.2, sfx.creak(1.2, 6), -10), (T["push"] + 0.3, sfx.buzz(), -8)]
        ev += [(T["chain"] - 0.3, sfx.clank(300, 0.5, 7), -6)]
        tt, i = T["drags"], 0
        while tt < T["never"] + 0.4:
            ev.append((tt, sfx.click(10 + i), -9 if i % 2 else -11))
            tt += 0.16
            i += 1
        ev += [(T["drags"], sfx.hum(T["never"] - T["drags"] + 0.3, 60), -12), (T["never"] + 0.25, sfx.clank(700, 0.4, 8), -4),
               (T["back"] + 0.25, sfx.chime(), -6)]
        ev += [(T["thrilling"] - 0.1, sfx.whoosh(0.8, False, 9), -4), (T["thrilling"], sfx.riser(0.8, 11), -12),
               (T["throws"], sfx.snap(), -4), (T["throws"] + 0.1, sfx.whoosh(0.6, True, 12), -6),
               (T["throws"] + 0.2, sfx.alarm(3, 850), -12)]
        ev += [(T["give"] - 0.55, sfx.whoosh(0.35, False, 13), -13)]
        ev += [(T[k] - 0.1, sfx.clank(500 + 150 * j, 0.35, 14 + j), -6) for j, k in enumerate(("top", "side", "under"))]
        ev += [(T["locked"], sfx.lock_click(17), -2), (T["locked"] + 0.2, sfx.chime(), -6),
               (T["locked"] + 0.3, sfx.whoosh(0.7, False, 18), -8)]
        ev += [(T["round"] - 0.3, sfx.clank(250, 0.6, 19), -8), (T["riders"] - 0.6, sfx.whoosh(1.0, True, 20), -6),
               (T["crushed"], sfx.thud(0.5, 21), -2), (T["crushed"] + 0.05, sfx.buzz(), -6)]
        ev += [(T["stretch"], sfx.creak(1.0, 22), -8), (T["teardrop"], sfx.sparkle(0.6, 8, 23), -8),
               (T["wide"] - 0.2, sfx.whoosh(1.0, True, 24), -8), (T["lock"], sfx.lock_click(25), -4),
               (T["lock"] + 0.2, sfx.lock_click(26), -4), (T["bars"] + 0.2, sfx.chime(), -6)]
        ev += [(T["flows"] - 0.25, sfx.whoosh(0.8, False, 27), -6), (T["flows"] + 0.6, sfx.whoosh(1.0, True, 28), -8),
               (T["blackout"], sfx.power_down(1.2, 29), -4), (T["blackout"] + 0.2, sfx.alarm(3, 800), -10)]
        ev += [(T["magnetic"] - 0.2, sfx.sparkle(0.6, 9, 30), -10), (T["magnetic"], sfx.clank(900, 0.3, 31), -8),
               (T["faster"] - 0.3, sfx.whoosh(0.6, True, 32), -6), (T["faster"] - 0.1, sfx.hum(1.6, 90), -8),
               (T["harder"], sfx.whirr(1.0, 380, 90, 33), -8), (T["slow"] + 0.35, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(34), 0), (T["follow"] - 0.15, sfx.pop(35), -4)]
        ev += [(T["paint"], sfx.whoosh(1.2, True, 36), -10), (T["red"], sfx.sparkle(0.8, 10, 37), -6)]
        ev += [(T["line"] + 0.05 * i, sfx.tap(40 + i), -14) for i in range(10)]
        ev += [(T["s1"], sfx.pop(50), -3), (T["s2"], sfx.pop(51), -3), (T["s3"], sfx.pop(52), -3),
               (T["s1"] - 0.3, sfx.whoosh(1.5, False, 53), -12)]
        ev += [(T["cong2"], sfx.pop(54), -2), (T["cong2"], sfx.sparkle(1.0, 14, 55), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.22, sfx.whoosh(0.45, False, 56), -6), (T["two"], sfx.ding(), -10),
               (T["fix"] - 0.45, sfx.click(57), -6), (T["womp"], sfx.womp(), -2)]
        return ev


def arabic_text(s):
    return any("؀" <= ch <= "ۿ" for ch in s)


NAME = "coaster"
EPISODE = Coaster
