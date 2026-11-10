"""Episode 3: The Disappearing Pool.  Build -> break -> fix, four times, keyed to the voiceover words.

Backyard side cutaway. World units: ground (patio) at y=0, down is positive. Pool cavity x -520..520, bottom y=500.
The floor is one slab whose top sits at self.floor_y(t) (0 = flush with the patio).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bi_base import (Episode, W, H, Track, Camera, clamp, lerp, prog, e_io, e_out, e_in, e_back, bump,  # noqa: E402
                     text, rect, grad_rect, glow, circle, poly, line, mix, shade, world, fx, sfx, ring_pts,
                     tap_ripple, WHITE, RED, YELLOW)

PX0, PX1, PB, WALL = -400, 400, 720, 36
WL = 26                      # water surface when nothing pushes it
FT = 44                      # steel floor thickness
DEEP = 420                   # floor top when lowered for swimming
GAP = 20
PIT_X0, PIT_X1, PIT_Y0, PIT_Y1 = 520, 870, 540, 710
WOOD, WOOD_DK = "#C98B4E", "#8A5A2F"
STEEL, STEEL_DK, STEEL_LT = "#B8C2CC", "#6B7785", "#E5EAF0"
TILE, TILE_DK = "#E7DCCB", "#C8B9A2"
WATER0, WATER1 = "#7DD3FC", "#0EA5E9"
CONCRETE = "#A7B0B9"
PINK = "#F472B6"

EMPH_EN = ["CONGRATS", "TIPS", "STEEL", "DOWN", "OIL", "SOMEWHERE", "GAP", "RISING", "PARTY", "FOLLOW",
           "POOL", "ZERO", "YOURSELF", "PATIO"]
EMPH_SA = ["مبروك", "ينقلب", "ستانلس", "تنزل", "زيت", "تروح", "فتحة", "طالعة", "حفلة", "تابعني", "مسبح",
           "صفر", "بيدك", "الحوش"]
KEYS_SA = {
    ("hook", "FLOAT"): "تطفي", ("hook", "DECK"): "خشب", ("hook", "CONGRATS"): "مبروك", ("hook", "PATIO"): "حوش",
    ("break1", "THREE"): "ثلاثة", ("break1", "CORNER"): "طرف", ("break1", "TIPS"): "ينقلب",
    ("break1", "SWIMMING"): "يسبح", ("break1", "CLOTHES"): "بملابسه",
    ("fix1", "STAINLESS"): "ستانلس", ("fix1", "STEEL"): "ستيل", ("fix1", "AIR"): "هوا", ("fix1", "CHAMBERS"): "غرف",
    ("fix1", "CORNER"): "زاوية", ("fix1", "CABLES"): "كيابل", ("fix1", "STAYS"): "تظل", ("fix1", "LEVEL"): "مستوي",
    ("break2", "ROCK"): "ثابت", ("break2", "SWIM"): "تسبح", ("break2", "DOWN"): "تنزل",
    ("fix2", "PULLEYS"): "بكرات", ("fix2", "CABLES"): "كيابل", ("fix2", "PISTON"): "مكبس", ("fix2", "WATER"): "موية",
    ("fix2", "OIL"): "زيت", ("fix2", "PULLING"): "يسحب", ("fix2", "FLOOR"): "الأرضية", ("fix2", "DEPTH"): "عمق",
    ("break3", "MOVES"): "تتحرك", ("break3", "THOUSANDS"): "آلاف", ("break3", "GALLONS"): "جالونات",
    ("break3", "WATER"): "موية", ("break3", "SOMEWHERE"): "تروح",
    ("fix3", "GAP"): "فتحة", ("fix3", "EDGE"): "الطرف", ("fix3", "WATER"): "الموية", ("fix3", "FLOWS"): "تمشي",
    ("fix3", "DRAINING"): "تصريف", ("fix3", "PUMPING"): "شفط", ("fix3", "FLOODING"): "غرق",
    ("break4", "FLOAT"): "عوامة", ("break4", "UNDER"): "تحت", ("break4", "EDGE"): "الطرف", ("break4", "RISING"): "طالعة",
    ("fix4", "SENSORS"): "حساسات", ("fix4", "INSTANTLY"): "طول", ("fix4", "LOCKS"): "أقفال",
    ("fix4", "TOP"): "فوق", ("fix4", "FRAME"): "هيكل", ("fix4", "PARTY"): "حفلة",
    ("cta", "FOLLOW"): "تابعني",
    ("reveal", "TILE"): "بلّط", ("reveal", "PRESS"): "اضغط", ("reveal", "BUTTON"): "زر", ("reveal", "FIVE"): "خمس",
    ("reveal", "SINKS"): "ينزل", ("reveal", "POOL"): "مسبح",
    ("stat", "ONE"): "حوش", ("stat", "TWO"): "مكانين", ("stat", "ZERO"): "صفر",
    ("closer", "CONGRATS"): "مبروك",
    ("tag", "DOG"): "الكلب", ("tag", "TRUST"): "يثق", ("tag", "PATIO"): "الحوش",
}
TEXT = {
    "en": {"follow": ("FOLLOW", "next: a roller coaster"),
           "stat": [("1", "BACKYARD"), ("2", "SPACES"), ("0", "COMPROMISES")],
           "steel": "STAINLESS STEEL", "air": "AIR CHAMBERS", "cables": "CABLES", "pulleys": "PULLEYS",
           "piston": "PISTON", "nooil": "WATER, NOT OIL", "gap": "GAP", "no": ["DRAINING", "PUMPING", "FLOODING"],
           "sensor": "SENSOR", "lock": "LOCK", "frame": "FRAME", "min": "MIN"},
    "ar_sa": {"follow": ("تابعني", "الجاي: قطار الموت"),
              "stat": [("1", "حوش"), ("2", "مكانين"), ("0", "تنازلات")],
              "steel": "ستانلس ستيل", "air": "غرف هوا", "cables": "كيابل", "pulleys": "بكرات",
              "piston": "مكبس", "nooil": "موية مو زيت", "gap": "فتحة", "no": ["تصريف", "شفط", "غرق"],
              "sensor": "حساس", "lock": "قفل", "frame": "هيكل", "min": "دقايق"},
}


class Pool(Episode):
    EMPH = {"en": EMPH_EN, "ar_sa": EMPH_SA}
    KEYS = {"ar_sa": KEYS_SA}
    TEXT = TEXT
    STAT_COLORS = ("#111827", "#0EA5E9", "#EF4444")

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        tl = self.tl
        s, e = tl.s, tl.e
        self.anchors({
            "float": ("hook", "FLOAT", 0.1), "deck": ("hook", "DECK", 0.2), "cong": ("hook", "CONGRATS", 0.4),
            "patio": ("hook", "PATIO", 0.95),
            "three": ("break1", "THREE", 0.1), "corner": ("break1", "CORNER", 0.3), "tips": ("break1", "TIPS", 0.45),
            "swim1": ("break1", "SWIMMING", 0.75), "clothes": ("break1", "CLOTHES", 0.9),
            "stainless": ("fix1", "STAINLESS", 0.2), "steel": ("fix1", "STEEL", 0.27), "air": ("fix1", "AIR", 0.38),
            "corner1": ("fix1", "CORNER", 0.65), "cables1": ("fix1", "CABLES", 0.75), "level": ("fix1", "LEVEL", 0.95),
            "rock": ("break2", "ROCK", 0.15), "swim": ("break2", "SWIM", 0.6), "wont": ("break2", "DOWN", 0.95),
            "pulleys": ("fix2", "PULLEYS", 0.15), "cables2": ("fix2", "CABLES", 0.27), "piston": ("fix2", "PISTON", 0.4),
            "water2": ("fix2", "WATER", 0.58), "oil": ("fix2", "OIL", 0.7), "pulling": ("fix2", "PULLING", 0.78),
            "depth": ("fix2", "DEPTH", 0.97),
            "moves": ("break3", "MOVES", 0.27), "gallons": ("break3", "GALLONS", 0.5),
            "somewhere": ("break3", "SOMEWHERE", 0.8),
            "gap": ("fix3", "GAP", 0.15), "edge": ("fix3", "EDGE", 0.3), "flows": ("fix3", "FLOWS", 0.5),
            "draining": ("fix3", "DRAINING", 0.65), "pumping": ("fix3", "PUMPING", 0.78),
            "flooding": ("fix3", "FLOODING", 0.92),
            "float4": ("break4", "FLOAT", 0.4), "under": ("break4", "UNDER", 0.55), "edge4": ("break4", "EDGE", 0.7),
            "rising": ("break4", "RISING", 0.92),
            "sensors": ("fix4", "SENSORS", 0.12), "instantly": ("fix4", "INSTANTLY", 0.3), "locks": ("fix4", "LOCKS", 0.45),
            "top": ("fix4", "TOP", 0.55), "frame": ("fix4", "FRAME", 0.7), "party": ("fix4", "PARTY", 0.95),
            "follow": ("cta", "FOLLOW", 0.4),
            "tile": ("reveal", "TILE", 0.1), "press": ("reveal", "PRESS", 0.37), "button": ("reveal", "BUTTON", 0.45),
            "five": ("reveal", "FIVE", 0.6), "sinks": ("reveal", "SINKS", 0.8), "pool5": ("reveal", "POOL", 0.95),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "TWO", 0.4), "s3": ("stat", "ZERO", 0.72),
            "cong2": ("closer", "CONGRATS", 0.1),
            "dog": ("tag", "DOG", 0.2), "trust": ("tag", "TRUST", 0.6), "patio2": ("tag", "PATIO", 0.9),
        })
        T = self.T
        T["womp"] = e("tag") + 0.3
        # floor: top y, half width, thickness, tilt, material (0 wood -> 1 steel -> 2 tile)
        top = self.ftop = Track(WL - 14.0)
        top.to(T["stainless"] - 0.1, 0.0, 0.8)                               # steel floor floats flush
        top.to(T["pulling"] - 0.05, DEEP, max(0.9, T["depth"] + 0.15 - T["pulling"]), e_io)   # pulled down
        top.to(T["moves"] - 0.05, 180.0, max(1.2, T["somewhere"] - T["moves"]), e_io)        # rises: water spills
        top.to(T["gap"] + 0.4, DEEP, max(1.0, T["flows"] + 0.6 - T["gap"]), e_io)            # down again, flows through gap
        top.to(T["rising"] - 0.45, 10.0, 1.0, e_in)                                          # rising onto the float
        top.to(T["instantly"], 58.0, 0.25, e_out)                                            # sensors: stop and back off
        top.to(T["locks"] - 0.25, 0.0, 0.5, e_io)                                            # up to the locks
        top.to(T["sinks"] - 0.3, 620.0, max(1.2, T["pool5"] + 0.5 - T["sinks"] + 0.3), e_io)  # the reveal: patio sinks
        top.to(T["cong2"] + 0.4, 0.0, 2.0, e_io)                                             # and comes back up
        self.hw = Track(330.0).to(T["stainless"], PX1 - 2.0, 0.6).to(T["gap"] - 0.05, PX1 - GAP, 0.4, e_out)
        self.thick = Track(24.0).to(T["stainless"], float(FT), 0.6)
        self.metal = Track(0.0).to(T["stainless"] - 0.05, 1.0, 0.5).to(T["tile"] - 0.05, 2.0, 0.7)
        self.tilt = Track(0.0).to(T["tips"] - 0.15, 14.0, 0.45, e_in).to(T["clothes"], 0.0, 0.9)
        self.chambers = Track(0.0).to(T["air"] - 0.15, 1.0, 0.4)
        self.cab1 = Track(0.0).to(T["cables1"] - 0.25, 1.0, 0.45)
        self.pul = Track(0.0).to(T["pulleys"] - 0.15, 1.0, 0.35)
        self.cab2 = Track(0.0).to(T["cables2"] - 0.15, 1.0, 0.5)
        self.pis = Track(0.0).to(T["piston"] - 0.2, 1.0, 0.35)
        self.pwater = Track(0.0).to(T["water2"] - 0.2, 1.0, 0.6)
        self.flood = Track(0.0).to(T["moves"] + 0.2, 1.0, max(1.2, T["somewhere"] + 0.4 - T["moves"]), e_out)
        self.flood.to(T["gap"] + 0.2, 0.0, 1.4, e_io)
        self.sens = Track(0.0).to(T["sensors"] - 0.15, 1.0, 0.3)
        self.lock = Track(0.0).to(T["locks"] + 0.25, 1.0, 0.3, e_back).to(T["sinks"] - 0.6, 0.0, 0.3)
        self.lock.to(T["cong2"] + 2.3, 1.0, 0.3, e_back)
        self.squish = Track(0.0).to(T["rising"] - 0.05, 1.0, 0.4, e_in).to(T["instantly"] + 0.05, 0.0, 0.35, e_back)
        # camera
        cam = self.cam = Camera(0, 340, 0.95)
        cam.key(0.05, 0, 390, 1.05, 2.4)
        cam.key(T["corner"] - 0.7, 110, 370, 1.15, 0.6)
        cam.key(T["stainless"] - 0.5, 0, 400, 1.0, 0.6)
        cam.key(T["air"] - 0.3, 0, 440, 1.15, 0.5)
        cam.key(T["cables1"] - 0.35, 0, 430, 1.0, 0.5)
        cam.key(T["level"] - 0.6, 0, 380, 1.05, 0.5)
        cam.key(T["rock"] - 0.4, 0, 360, 1.15, 0.5)
        cam.key(T["pulleys"] - 0.35, 0, 460, 1.0, 0.5)
        cam.key(T["piston"] - 0.4, 260, 470, 0.92, 0.5)
        cam.key(T["pulling"] - 0.25, 60, 420, 0.95, 0.6)
        cam.key(T["moves"] - 0.35, 0, 230, 0.86, 0.6)
        cam.key(T["gap"] - 0.4, -370, 330, 1.5, 0.5)
        cam.key(T["flows"] - 0.4, -330, 400, 1.3, 0.5)
        cam.key(T["draining"] - 0.35, 0, 400, 0.95, 0.5)
        cam.key(T["float4"] - 0.5, 200, 300, 1.2, 0.6)
        cam.key(T["rising"] - 0.45, 320, 120, 1.7, 0.5)
        cam.key(T["sensors"] - 0.3, 320, 80, 1.6, 0.4)
        cam.key(T["locks"] - 0.3, -320, 80, 1.6, 0.5)
        cam.key(T["frame"] - 0.35, 0, 360, 1.0, 0.5)
        cam.key(T["party"] - 0.6, 0, 270, 0.95, 0.6)
        cam.key(s("cta") + 0.2, -300, 200, 0.7, 3.0)
        cam.key(T["press"] - 0.45, -680, 60, 1.25, 0.5)
        cam.key(T["five"] - 0.2, -100, 330, 0.85, 0.6)
        cam.key(s("stat") - 0.1, -250, 260, 0.66, 0.8)
        cam.key(s("closer") - 0.1, -150, 300, 0.75, 2.4)
        cam.key(s("tag") - 0.22, -440, -40, 2.0, 0.45)
        self.shakes = [(T["tips"], 0.4, 8), (T["somewhere"] - 0.3, 0.6, 10), (T["rising"] + 0.05, 0.3, 10),
                       (T["locks"] + 0.25, 0.2, 6)]

    def red_level(self, t):
        T = self.T
        return (0.8 * bump(t, T["tips"] - 0.1, T["tips"] + 1.4) + 0.8 * bump(t, T["wont"] - 0.3, T["wont"] + 1.0)
                + 0.9 * bump(t, T["gallons"] - 0.2, T["gallons"] + 1.8) + 0.9 * bump(t, T["rising"] - 0.1, T["rising"] + 1.1))

    # ------------------------------------------------------------------ geometry
    def water_top(self, t):
        """Surface of the water inside the pool (rises when the floor pushes it before the gap exists)."""
        return WL - 70 * self.flood.at(t)

    # ------------------------------------------------------------------ world
    def draw_backdrop(self, c, t, dusk):
        cx, cy, z = self.cam_state
        gy = (0 - cy) * z + H / 2
        zf = clamp(0.7 * z ** 0.7, 0.2, 0.95)
        c.save()
        c.translate(W / 2, gy)
        c.scale(zf, zf)
        c.translate(-cx * 0.35, 0)
        for i, x in enumerate(range(-3200, 3300, 520)):
            world.tree(c, x + (i % 3) * 60, 1.5 + (i % 2) * 0.35, dusk, i)
        # fence
        for x in range(-3400, 3400, 70):
            rect(c, x, -230, 54, 230, mix("#E8D2B0", "#6B5A48", dusk), r=6)
        rect(c, -3400, -170, 6800, 22, mix("#D4BC96", "#5E4F40", dusk))
        c.restore()

    def draw_world(self, c, t, dusk, z):
        T = self.T
        world.ground(c, -6000, 6000, 3000, dusk)
        world.house(c, -1150, 560, 420, dusk=dusk)
        world.tree(c, 1150, 1.6, dusk, 1)
        self.draw_patio(c, t)
        self.draw_pit(c, t)
        self.draw_pool(c, t)
        self.draw_people(c, t)
        self.draw_dog(c, t)

    def draw_patio(self, c, t):
        for x0, x1 in ((-1300, PX0 - WALL), (PX1 + WALL, 1300)):
            rect(c, x0, 0, x1 - x0, 18, TILE)
            for x in range(int(x0), int(x1), 120):
                line(c, x, 1, x, 17, TILE_DK, 3)
        # button post near the house (reveal)
        rect(c, -773, -120, 26, 120, "#475569", r=6)
        circle(c, -760, -122, 22, "#E2E8F0")
        circle(c, -760, -122, 15, RED if prog(t, self.T["press"] - 0.1, self.T["press"] + 0.2) < 1 else GREEN_DK)

    def draw_pit(self, c, t):
        a = self.pis.at(t)
        if a <= 0:
            return
        rect(c, PIT_X0 - 18, PIT_Y0 - 18, PIT_X1 - PIT_X0 + 36, PIT_Y1 - PIT_Y0 + 36, "#6B7280", a, r=10)
        rect(c, PIT_X0, PIT_Y0, PIT_X1 - PIT_X0, PIT_Y1 - PIT_Y0, "#3F4752", a, r=6)
        # piston cylinder with water inside, rod toward the pool
        d = clamp(self.ftop.at(t) / 620.0)
        cx0, cx1, cy0, cy1 = 600, 850, 590, 660
        rect(c, cx0, cy0, cx1 - cx0, cy1 - cy0, STEEL_DK, a, r=14)
        rect(c, cx0 + 8, cy0 + 8, cx1 - cx0 - 16, cy1 - cy0 - 16, "#1F2937", a, r=10)
        wf = self.pwater.at(t)
        fill_x = cx0 + 8 + (cx1 - cx0 - 16) * (1 - 0.35 * d)
        if wf > 0:
            grad_rect(c, cx0 + 8, cy0 + 8, (fill_x - cx0 - 8) * wf, cy1 - cy0 - 16, WATER0, WATER1, a, r=10)
        head = cx0 + 20 + (cx1 - cx0 - 60) * (0.75 * d)
        rect(c, head - 12, cy0 + 4, 24, cy1 - cy0 - 8, STEEL_LT, a, r=6)
        rod_x = head
        line(c, PIT_X0 - 30, 625, rod_x, 625, STEEL_LT, 14, a)
        self.rod_x = rod_x

    def floor_geom(self, t):
        ft = self.ftop.at(t)
        if t < 1.2:  # frame one: the deck is falling onto the water, then bobs
            ft += -320 * (1 - e_in(prog(t, 0.0, 0.32))) + 12 * math.sin((t - 0.32) * 14) * clamp(1.2 - t) * (t > 0.32)
        return ft, self.hw.at(t), self.thick.at(t), self.tilt.at(t), self.metal.at(t)

    def draw_pool(self, c, t):
        T = self.T
        ft, hw, th, tilt, metal = self.floor_geom(t)
        wt = self.water_top(t)
        # shell
        rect(c, PX0 - WALL, -2, (PX1 - PX0) + 2 * WALL, PB + WALL + 2, CONCRETE)
        rect(c, PX0, 0, PX1 - PX0, PB, "#DCEEF7")
        for x in range(PX0 + 52, PX1, 52):
            line(c, x, 6, x, PB - 4, "#C6E3F1", 2)
        # water: everything below the surface
        grad_rect(c, PX0, wt, PX1 - PX0, PB - wt, WATER0, WATER1, 0.88)
        k = (t * 1.3) % 1.0
        for i in range(9):
            x = PX0 + 40 + i * 115 + 30 * math.sin(t * 2 + i)
            line(c, x, wt + 6, x + 46, wt + 6, "#E0F7FF", 4, 0.6)
        # spill over the coping and the flooded patio
        fl = self.flood.at(t)
        if fl > 0:
            for side in (-1, 1):
                x_in = PX1 if side > 0 else PX0
                x_out = x_in + side * WALL
                spread = 1000 * e_out(fl)
                # overflow sheet curling over the coping
                sheet = [(x_in - side * 30, wt), (x_in + side * 10, wt - 24 * fl), (x_out + side * 30, -14 * fl),
                         (x_out + side * 46, 18), (x_in - side * 30, 18)]
                poly(c, sheet, WATER1, 0.9 * min(1, fl * 2))
                # flood sheet on the patio with waves
                pts = [(x_out, 18)]
                n = 18
                for i in range(n + 1):
                    xx = x_out + side * spread * i / n
                    yy = -80 * fl * (1 - 0.65 * i / n) - 12 * math.sin(t * 7 + i * 0.8) * fl
                    pts.append((xx, yy))
                pts += [(x_out + side * spread, 18)]
                poly(c, pts, "#0284C7", 0.92)
                poly(c, [(x, y - 3) for x, y in pts[1:-1]] + [(x, y + 4) for x, y in reversed(pts[1:-1])], "#E0F7FF", 0.6)
                # fountains at the edge
                fz = bump(t, T["moves"], T["somewhere"] + 0.8)
                if fz > 0:
                    for j in range(9):
                        u = ((t * 1.4 + j / 9) % 1.0)
                        px = x_in + side * (-20 + 230 * u)
                        py = wt - 260 * fz * math.sin(u * math.pi)
                        circle(c, px, py, 22 + 14 * (1 - u), "#E0F7FF", 0.95 * fz)
                        circle(c, px, py, 12 + 8 * (1 - u), "#38BDF8", 0.9 * fz)
            # a rubber duck sails off on the flood
            dx = 120 + 520 * e_io(prog(t, T["gallons"] - 0.3, T["gallons"] + 2.4))
            duck(c, PX1 + WALL + dx, -16 * fl - 4, 1.7, min(1, fl * 2))
        # cables + pulleys (behind the floor)
        self.draw_rigging(c, t, ft, hw, th)
        # air chambers under the floor
        ch = self.chambers.at(t)
        if ch > 0:
            n = 3
            span = 2 * hw - 120
            for i in range(n):
                cx_ = -hw + 60 + span * (i + 0.5) / n
                rect(c, cx_ - span / n / 2 + 18, ft + th + 2, span / n - 36, 58 * e_back(ch), "#E2E8F0", ch, r=26)
                rect(c, cx_ - span / n / 2 + 30, ft + th + 10, span / n - 60, 12 * ch, "#FFFFFF", 0.6 * ch, r=6)
        # the floor slab
        c.save()
        c.translate(0, ft + th / 2)
        c.rotate(tilt)
        self.draw_slab(c, t, hw, th, metal)
        c.restore()
        # coping stones on top of the walls (cover the gap edges)
        for x0 in (PX0 - WALL - 6, PX1 - 6):
            rect(c, x0, -8, WALL + 12, 20, "#E7E2D8", r=4)
        # gap flow arrows (fix3)
        fa = bump(t, T["gap"] + 0.3, T["draining"] + 0.4)
        if fa > 0 and hw < PX1 - 5:
            down = self.ftop.at(t + 0.05) > ft + 0.5          # floor going down: water goes up through the gap
            for side in (-1, 1):
                gx = side * (hw + GAP / 2)
                for m in range(5):
                    u = (t * 1.1 + m / 5) % 1.0
                    yy = lerp(PB - 60, 30, u) if down else lerp(30, PB - 60, u)
                    tip = -26 if down else 26
                    al = fa * min(1.0, 4 * min(u, 1 - u))
                    poly(c, [(gx - 15, yy - tip / 2), (gx + 15, yy - tip / 2), (gx, yy + tip / 2)], "#FFFFFF", al)
                    poly(c, [(gx - 9, yy - tip / 3), (gx + 9, yy - tip / 3), (gx, yy + tip / 3)], "#1D4ED8", al)
        # sensors on the coping, beams down the gap (fix4)
        sa = self.sens.at(t)
        if sa > 0:
            for side in (-1, 1):
                bx = side * (PX1 + WALL / 2)
                rect(c, bx - 16, -40, 32, 30, "#111827", sa, r=6)
                circle(c, bx, -25, 7, RED, sa)
                beam = sa * (0.55 + 0.45 * math.sin(t * 20))
                line(c, side * (PX1 - GAP / 2 + 1), 2, side * (PX1 - GAP / 2 + 1), 260, RED, 4, 0.7 * beam)
                glow(c, side * (PX1 - GAP / 2), 40, 70, RED, 0.25 * beam)
        # locks at the top (fix4)
        la = self.lock.at(t)
        if la > 0:
            for side in (-1, 1):
                x_w = side * PX1
                rect(c, x_w - (36 if side > 0 else 0) + side * (-30 * la), 14, 36, 18, "#334155", 1.0, r=4)
        # the float (break4)
        self.draw_float(c, t, ft, wt)
        if t < 1.0:
            for x in (-300, 300):
                splash(c, x, wt, prog(t, 0.3, 0.95))

    def draw_slab(self, c, t, hw, th, metal):
        if metal < 1:
            a = 1 - metal
            rect(c, -hw, -th / 2, 2 * hw, th, WOOD, 1.0, r=6)
            for i in range(int(-hw) + 60, int(hw), 80):
                line(c, i, -th / 2 + 2, i, th / 2 - 2, WOOD_DK, 3, a)
        if metal > 0:
            a = min(1.0, metal)
            rect(c, -hw, -th / 2, 2 * hw, th, STEEL, a, r=6)
            rect(c, -hw, -th / 2, 2 * hw, 8, STEEL_LT, a, r=4)
            rect(c, -hw, th / 2 - 8, 2 * hw, 8, STEEL_DK, a, r=4)
            for i in range(int(-hw) + 40, int(hw), 90):
                circle(c, i, 0, 4, STEEL_DK, a)
        if metal > 1:
            a = metal - 1
            rect(c, -hw, -th / 2, 2 * hw, 18, TILE, a, r=4)
            for i in range(int(-hw) + 60, int(hw), 120):
                line(c, i, -th / 2 + 1, i, -th / 2 + 17, TILE_DK, 3, a)

    def draw_rigging(self, c, t, ft, hw, th):
        T = self.T
        a1, a2, pa = self.cab1.at(t), self.cab2.at(t), self.pul.at(t)
        corners = (-hw + 30, hw - 30)
        if a1 > 0 and a2 <= 0.01:
            for x in corners:
                y0 = ft + th
                line(c, x, y0, x, y0 + (PB - 8 - y0) * a1, "#475569", 6)
                rect(c, x - 16, PB - 14, 32, 14, "#475569", a1, r=3)
        if pa > 0:
            for x in (PX0 + 36, PX1 - 36):
                k = e_back(pa)
                circle(c, x, PB - 30, 24 * k, "#334155")
                circle(c, x, PB - 30, 9 * k, STEEL_LT)
        if a2 > 0:
            col = "#475569"
            pl, pr = PX0 + 36, PX1 - 36
            y0 = ft + th
            for x, px in ((corners[0], pl), (corners[1], pr)):
                line(c, x, y0, px, PB - 54, col, 6, a2)
            line(c, pl, PB - 6, pr, PB - 6, col, 6, a2)
            rod = getattr(self, "rod_x", PIT_X0)
            if self.pis.at(t) > 0:
                line(c, pr, PB - 6, PX1 + WALL + 10, 625, col, 6, a2)
                line(c, PX1 + WALL + 10, 625, rod, 625, col, 6, a2)

    def draw_float(self, c, t, ft, wt):
        T = self.T
        a = prog(t, T["float4"] - 0.6, T["float4"] - 0.2) * (1 - prog(t, s_rev(self) - 0.4, s_rev(self)))
        if a <= 0:
            return
        x = lerp(60, PX1 - 40, e_io(prog(t, T["float4"] - 0.2, T["edge4"] + 0.3)))
        x -= 300 * e_out(prog(t, T["instantly"] + 0.2, T["instantly"] + 1.8))
        y = min(wt, ft) - 6
        sq = self.squish.at(t)
        flamingo(c, x, y, 1.0, sq, a, t)

    # ------------------------------------------------------------------ people
    def draw_people(self, c, t):
        T, tl = self.T, self.tl
        ft, hw, th, tilt, metal = self.floor_geom(t)
        wt = self.water_top(t)
        P = world.person
        # hook: two friends step onto the floating deck; break1: three walk to one corner and slide in
        if t < T["stainless"]:
            for i in range(3):
                col = world.crowd_colors(i + 1)
                if t < T["three"] - 0.2:
                    xs = (-150, 0, 150)[i]
                    enter = prog(t, 1.2 + 0.25 * i, 2.2 + 0.25 * i)
                    x = lerp(-640 - 90 * i, xs, e_out(enter))
                    a = prog(t, 1.0 + 0.25 * i, 1.3 + 0.25 * i)
                    yb = WL - 14 if enter > 0.8 else (0 if x < PX0 - 10 else WL - 14)
                    P(c, x, yb, 120, walk=t * 2 if enter < 1 else 0, a=a, **col)
                else:
                    go = e_io(prog(t, T["three"], T["corner"] + 0.2))
                    x = lerp((-150, 0, 150)[i], (190, 240, 290)[i], go)
                    slide = prog(t, T["tips"] - 0.05, T["tips"] + 0.55 + 0.08 * i)
                    if slide <= 0:
                        P(c, x, ft + x * math.sin(math.radians(tilt)), 120, walk=t * 2 if go < 1 else 0,
                          lean=0.6 * prog(t, T["tips"] - 0.2, T["tips"]), **col)
                    else:
                        sx = lerp(x, 345 + 18 * i, e_out(slide))
                        if slide < 1:
                            P(c, sx, lerp(WL - 14, WL + 70, slide), 120, arms_up=slide, lean=1.5, **col)
                        sw = prog(t, T["tips"] + 0.5, T["tips"] + 0.7) * (1 - prog(t, T["stainless"] - 0.4, T["stainless"]))
                        swimmer(c, 360 - 10 * i - 60 * i * prog(t, T["swim1"], T["clothes"] + 0.5), wt, t + i, sw, col)
                        if slide < 0.6:
                            splash(c, 360, wt, prog(t, T["tips"] + 0.05 * i, T["tips"] + 0.6 + 0.05 * i))
        # fix1: two people test the corner, the floor stays level
        a = prog(t, T["corner1"] - 0.2, T["corner1"] + 0.2) * (1 - prog(t, T["rock"] - 0.5, T["rock"] - 0.2))
        if a > 0:
            for i in range(2):
                x = lerp(-160 + 100 * i, 230 + 70 * i, e_io(prog(t, T["corner1"], T["level"] - 0.1)))
                P(c, x, ft, 120, walk=t * 2, a=a, **world.crowd_colors(i + 4))
        # break2: a swimmer in goggles jumps on the floor, it won't go down
        a = prog(t, T["rock"] - 0.3, T["rock"]) * (1 - prog(t, T["pulling"] + 0.2, T["pulling"] + 0.5))
        if a > 0:
            hop = abs(math.sin((t - T["rock"]) * 7)) * 60 * bump(t, T["rock"], T["wont"] + 0.4)
            P(c, 40, ft - hop, 124, shirt="#F97316", arms_up=0.7 * bump(t, T["swim"] - 0.3, T["wont"] + 0.6), a=a)
            goggles(c, 40, ft - hop, 124, a)
        a = prog(t, T["pulling"] + 0.3, T["pulling"] + 0.6) * (1 - prog(t, T["float4"] - 0.6, T["float4"] - 0.3))
        if a > 0:
            swimmer(c, 40 + 60 * math.sin(t * 0.8), min(self.water_top(t), ft), t, a, dict(shirt="#F97316", skin="#F2C9A0", hair="#2D2A26"),
                    goggles_on=True)
        # fix4: the party
        a = prog(t, T["party"] - 0.5, T["party"]) * (1 - prog(t, tl.s("reveal") - 0.2, tl.s("reveal") + 0.2))
        if a > 0:
            for i in range(8):
                x = -330 + i * 94
                bounce = abs(math.sin(t * 6 + i)) * 18
                P(c, x, ft - bounce, 118, arms_up=0.5 + 0.5 * math.sin(t * 5 + i * 1.3), a=a, **world.crowd_colors(i))
        # reveal: someone presses the button by the house
        a = prog(t, tl.s("reveal") - 0.3, tl.s("reveal")) * (1 - prog(t, tl.s("tag") - 0.3, tl.s("tag")))
        if a > 0:
            P(c, -840, 0, 124, shirt="#8B5CF6", arms_up=0.35 * bump(t, T["press"] - 0.2, T["press"] + 0.5), a=a)
        # stat + closer: swimmers in the pool
        a = prog(t, T["pool5"], T["pool5"] + 0.4) * (1 - prog(t, T["cong2"] + 0.2, T["cong2"] + 0.8))
        if a > 0:
            for i in range(3):
                swimmer(c, -240 + 220 * i + 40 * math.sin(t + i), self.water_top(t), t + i * 0.7, a, world.crowd_colors(i + 2))

    def draw_dog(self, c, t):
        T, tl = self.T, self.tl
        a = prog(t, tl.s("tag") - 0.5, tl.s("tag") - 0.2)
        if a <= 0:
            return
        paw = bump(t, T["dog"] + 0.2, T["trust"] + 0.1)
        back = prog(t, T["trust"], T["trust"] + 0.3)
        dog(c, -560 - 20 * back, 0, 1.0, t, paw * (1 - back), back, a)
        q = prog(t, T["trust"] + 0.1, T["trust"] + 0.35)
        if q > 0:
            text(c, "?", -540, -205, 90 * e_back(q), "#111827", "Poppins-Black")

    # ------------------------------------------------------------------ overlays
    def draw_overlays(self, c, t, tw, dusk):
        T, tx, tl = self.T, self.tx, self.tl
        ft, hw, th, tilt, metal = self.floor_geom(tw)
        # outlines
        self.outline(c, tw, T["cong"] + 0.1, (-hw, ft - 4, 2 * hw, th + 8), 1.2)
        self.outline(c, tw, T["steel"] + 0.05, (-hw, ft - 4, 2 * hw, th + 8), 1.0)
        self.outline(c, tw, T["air"] + 0.25, (-hw + 60, ft + th, 2 * hw - 120, 64), 1.1)
        self.outline(c, tw, T["cables1"] + 0.15, (-hw + 10, ft + th, 40, PB - ft - th), 1.0)
        self.outline(c, tw, T["pulleys"] + 0.15, (PX0 + 6, PB - 60, 60, 60), 1.0)
        self.outline(c, tw, T["piston"] + 0.1, (590, 580, 270, 90), 1.1)
        self.outline(c, tw, T["gap"] + 0.2, (PX0 - 6, 0, GAP + 12, 260), 1.1)
        self.outline(c, tw, T["sensors"] + 0.15, (PX1 + 2, -46, 32, 40), 1.0)
        self.outline(c, tw, T["locks"] + 0.4, (PX0 - 6, 6, 70, 32), 1.0)
        self.outline(c, tw, T["frame"] + 0.1, (-hw, ft, 2 * hw, th + 70), 1.1)
        # labels
        self.wpill(c, tw, tx["steel"], 0, ft - 70, T["steel"] - 0.05, T["air"] - 0.1)
        self.wpill(c, tw, tx["air"], 0, ft + th + 120, T["air"], T["cables1"] - 0.2)
        self.wpill(c, tw, tx["cables"], -hw + 30, ft + 220, T["cables1"] - 0.1, T["level"] - 0.4, dx=150)
        self.wpill(c, tw, tx["pulleys"], PX0 + 120, PB - 110, T["pulleys"], T["piston"] - 0.3, dx=60)
        self.wpill(c, tw, tx["piston"], 720, 520, T["piston"], T["oil"] - 0.1)
        self.wpill(c, tw, tx["nooil"], 720, 520, T["oil"] - 0.1, T["depth"] + 0.6, fg="#FFFFFF", bg="#0EA5E9")
        self.wpill(c, tw, tx["gap"], PX0 + 110, 100, T["gap"] + 0.1, T["flows"] - 0.2, fg="#FFFFFF", bg="#1D4ED8", size=44)
        self.wpill(c, tw, tx["sensor"], PX1 - 120, -90, T["sensors"], T["locks"] - 0.4)
        self.wpill(c, tw, tx["lock"], PX0 + 120, -60, T["locks"] + 0.2, T["frame"] - 0.3)
        self.wpill(c, tw, tx["frame"], 0, ft + 170, T["frame"], T["party"] - 0.6)
        # "no draining, no pumping, no flooding"
        for i, (key, word) in enumerate(zip(("draining", "pumping", "flooding"), tx["no"])):
            p = prog(t, T[key] - 0.1, T[key] + 0.2) * (1 - prog(t, tl.s("break4") - 0.2, tl.s("break4") + 0.1))
            if p > 0:
                y = 300 + i * 120
                self.pill(c, word, W / 2, y, p, fg="#111827", bg="#FFFFFF", size=46)
                k = prog(t, T[key] + 0.1, T[key] + 0.3)
                tw_ = 300
                line(c, W / 2 - tw_ / 2, y + 22, W / 2 - tw_ / 2 + tw_ * k, y - 22, RED, 10, p)
        # five-minute clock
        p = prog(t, T["five"] - 0.15, T["five"] + 0.15) * (1 - prog(t, T["s1"] - 0.2, T["s1"] + 0.1))
        if p > 0:
            k = e_back(p)
            cx_, cy_ = W / 2, 330
            c.save()
            c.translate(cx_, cy_)
            c.scale(k, k)
            circle(c, 0, 8, 96, "#000000", 0.25, blur=10)
            circle(c, 0, 0, 96, "#FFFFFF")
            circle(c, 0, 0, 96, "#111827", stroke=8)
            ang = -math.pi / 2 + 2 * math.pi * prog(t, T["five"], T["pool5"] + 0.4)
            line(c, 0, 0, math.cos(ang) * 64, math.sin(ang) * 64, RED, 9)
            text(c, "5", -4, 40, 46, "#111827", "Poppins-Black")
            c.restore()
            self.pill(c, ["5", tx["min"]], cx_, cy_ + 140, p, fg="#FFFFFF", bg="#111827", size=40)
        # button press ripple
        if T["press"] - 0.1 <= tw < T["press"] + 0.8:
            x, y = self.sc(-760, -122)
            tap_ripple(c, x, y, tw, T["press"], 1.2)
        # alerts + checks
        self.alert(c, tw, T["tips"] + 0.1, T["stainless"] - 0.2, -180, -170)
        self.alert(c, tw, T["wont"] - 0.2, T["pulleys"] - 0.3, 200, ft - 200)
        self.alert(c, tw, T["gallons"] - 0.1, T["gap"] - 0.3, 330, -260)
        self.alert(c, tw, T["rising"] + 0.05, T["sensors"] - 0.1, 220, -110)
        self.check(c, tw, T["level"] + 0.15, -200, -200)
        self.check(c, tw, T["depth"] + 0.2, 300, 200)
        self.check(c, tw, T["flooding"] + 0.25, 330, -240)
        self.check(c, tw, T["party"] + 0.15, 330, -260)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, tl = self.T, self.tl
        s, e = tl.s, tl.e
        ev = [(0.0, sfx.whoosh(0.4, False, 1), -8), (0.35, sfx.thud(0.35, 2), -4), (0.38, sfx.hiss(0.5, 3), -10)]
        ev += [(1.25 + 0.25 * i, sfx.tap(i), -12) for i in range(6)]
        ev += [(T["cong"], sfx.pop(), -2), (T["cong"], sfx.sparkle(), -8)]
        ev += [(T["three"] + 0.1 * i, sfx.tap(10 + i), -12) for i in range(6)]
        ev += [(T["tips"] - 0.1, sfx.creak(0.6, 4), -6), (T["tips"] + 0.2, sfx.whoosh(0.4, False, 5), -6),
               (T["tips"] + 0.5, sfx.hiss(0.7, 6), -4), (T["tips"] + 0.5, sfx.thud(0.4, 7), -6), (T["tips"] + 0.3, sfx.buzz(), -8)]
        ev += [(T["stainless"], sfx.clank(500, 0.6, 8), -6), (T["steel"], sfx.sparkle(0.5, 6, 9), -10),
               (T["air"], sfx.pop(10), -6), (T["air"] + 0.12, sfx.pop(11), -7), (T["air"] + 0.24, sfx.pop(12), -8),
               (T["cables1"] - 0.2, sfx.snap(), -10), (T["cables1"], sfx.clank(900, 0.3, 13), -10),
               (T["level"] + 0.15, sfx.chime(), -6)]
        ev += [(T["rock"] + 0.1 * i * 4, sfx.thud(0.3, 14 + i), -6) for i in range(4)]
        ev += [(T["wont"], sfx.buzz(), -6)]
        ev += [(T["pulleys"], sfx.pop(20), -6), (T["cables2"], sfx.whirr(0.8, 200, 300, 21), -10),
               (T["piston"], sfx.clank(300, 0.6, 22), -6), (T["water2"], sfx.hiss(0.9, 23), -10),
               (T["oil"], sfx.pop(24), -6), (T["pulling"], sfx.hum(1.4, 70), -6), (T["pulling"], sfx.whirr(1.4, 120, 90, 25), -12),
               (T["depth"] + 0.2, sfx.chime(), -6)]
        ev += [(T["moves"], sfx.hum(1.0, 60), -8), (T["moves"] + 0.3, sfx.hiss(2.2, 26), -6),
               (T["gallons"], sfx.alarm(3, 850), -12), (T["somewhere"], sfx.whoosh(0.8, True, 27), -6)]
        ev += [(T["gap"], sfx.click(28), -6), (T["flows"], sfx.hiss(1.2, 29), -12),
               (T["draining"] + 0.1, sfx.pop(30), -6), (T["pumping"] + 0.1, sfx.pop(31), -6),
               (T["flooding"] + 0.1, sfx.pop(32), -6), (T["flooding"] + 0.25, sfx.chime(), -6)]
        ev += [(T["float4"] - 0.4, sfx.pop(33), -10), (T["rising"] - 0.45, sfx.hum(1.0, 65), -8),
               (T["rising"] + 0.05, sfx.creak(0.5, 34), -4), (T["rising"] + 0.1, sfx.alarm(2, 900), -12)]
        ev += [(T["sensors"], sfx.beep(1500, 0.08), -8), (T["sensors"] + 0.15, sfx.beep(1500, 0.08), -8),
               (T["instantly"], sfx.thud(0.3, 35), -6), (T["locks"] + 0.25, sfx.lock_click(36), -4),
               (T["locks"] + 0.4, sfx.lock_click(37), -4), (T["frame"], sfx.clank(400, 0.5, 38), -8),
               (T["party"] - 0.4, sfx.sparkle(1.0, 12, 39), -8), (T["party"] + 0.15, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(40), 0), (T["follow"] - 0.15, sfx.pop(41), -4)]
        ev += [(T["tile"], sfx.sparkle(0.7, 9, 42), -8)] + [(T["tile"] + 0.08 * i, sfx.tap(43 + i), -12) for i in range(6)]
        ev += [(T["press"], sfx.beep(1200, 0.1), -4), (T["five"], sfx.tick(), -6), (T["five"] + 0.5, sfx.tick(), -6),
               (T["sinks"] - 0.3, sfx.hum(1.6, 60), -8), (T["sinks"], sfx.hiss(1.4, 44), -8),
               (T["pool5"], sfx.whoosh(0.6, False, 45), -6), (T["pool5"] + 0.3, sfx.hiss(0.6, 46), -6)]
        ev += [(T["s1"], sfx.pop(47), -3), (T["s2"], sfx.pop(48), -3), (T["s3"], sfx.pop(49), -3)]
        ev += [(T["cong2"], sfx.pop(50), -2), (T["cong2"], sfx.sparkle(1.0, 14, 51), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.22, sfx.whoosh(0.45, False, 52), -6), (T["dog"] + 0.2, sfx.tap(53), -8),
               (T["trust"] + 0.05, sfx.whoosh(0.3, True, 54), -10), (T["trust"] + 0.15, sfx.pop(55), -6),
               (T["womp"], sfx.womp(), -2)]
        return ev


GREEN_DK = "#16A34A"


def s_rev(ep):
    return ep.tl.s("reveal")


# ---------------------------------------------------------------- small drawings (world space)
def swimmer(c, x, y_surf, t, a, col, goggles_on=False):
    if a <= 0:
        return
    bob = 4 * math.sin(t * 3)
    y = y_surf + bob
    circle(c, x, y - 18, 21, col.get("skin", "#F2C9A0"), a)
    circle(c, x, y - 26, 18, col.get("hair", "#2D2A26"), a)
    rect(c, x - 19, y - 27, 38, 9, col.get("hair", "#2D2A26"), a, r=4)
    if goggles_on:
        rect(c, x - 21, y - 22, 42, 9, "#0EA5E9", a, r=4)
    for side in (-1, 1):
        ang = t * 4 + (0 if side < 0 else math.pi)
        line(c, x + side * 18, y - 4, x + side * (34 + 10 * math.cos(ang)), y - 20 - 12 * math.sin(ang),
             col.get("skin", "#F2C9A0"), 9, a)
    circle(c, x, y + 2, 40, "#E0F7FF", 0.35 * a, stroke=4)


def splash(c, x, y, u):
    if u <= 0 or u >= 1:
        return
    for i in range(9):
        ang = math.pi * (0.15 + 0.7 * i / 8)
        r = 30 + 120 * u
        circle(c, x + math.cos(ang) * r * (1 if i % 2 else -1) * 0.8, y - math.sin(ang) * r * (1 - u * 0.4),
               12 * (1 - u) + 4, "#BAE6FD", 1 - u)


def goggles(c, x, y, h, a):
    u = h / 140.0
    rect(c, x - 21 * u, y - 133 * u, 42 * u, 10 * u, "#0EA5E9", a, r=4 * u)


def duck(c, x, y, s, a):
    if a <= 0.05:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, -26, -26, 52, 26, "#FACC15", a, r=13)
    circle(c, 16, -36, 15, "#FACC15", a)
    poly(c, [(28, -38), (42, -34), (28, -30)], "#F97316", a)
    circle(c, 19, -40, 3, "#111827", a)
    c.restore()


def flamingo(c, x, y, s, squish, a, t):
    c.save()
    c.translate(x, y)
    c.scale(s * (1 + 0.35 * squish), s * (1 - 0.55 * squish))
    tilt = 4 * math.sin(t * 2)
    c.rotate(tilt)
    poly(c, ring_pts(0, 0, 90, 30), PINK, a)
    poly(c, ring_pts(0, -2, 48, 13), "#7DD3FC", a)
    line(c, 60, -10, 70, -90, PINK, 16, a)
    line(c, 70, -90, 50, -120, PINK, 16, a)
    circle(c, 46, -124, 15, PINK, a)
    poly(c, [(34, -126), (16, -116), (34, -116)], "#111827", a)
    c.restore()


def dog(c, x, y, s, t, paw, back, a):
    """A small brown dog facing right, feet at y; paw = front paw lifted (0..1), back = leaning back."""
    if a <= 0:
        return
    col, dk = "#B7793F", "#8A5A2B"
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.rotate(-6 * back)
    wag = 18 * math.sin(t * 14)
    line(c, -64, -84, -96, -120 + wag * 0.3, dk, 12, a)
    for lx, lift in ((-46, 0), (-26, 0), (34, 0), (52, paw)):
        rect(c, lx - 7, -48 - 26 * lift, 14, 48 - 4 * lift, dk, a, r=6)
    rect(c, -70, -96, 140, 56, col, a, r=28)
    circle(c, 74, -112, 32, col, a)
    rect(c, 86, -112, 40, 24, col, a, r=12)
    circle(c, 124, -103, 7, "#111827", a)
    circle(c, 80, -120, 5, "#111827", a)
    poly(c, [(52, -136), (64, -96), (40, -100)], dk, a)
    c.restore()


NAME = "pool"
EPISODE = Pool
