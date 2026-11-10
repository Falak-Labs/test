"""Episode 1: The Elevator.  Build -> break -> fix, four times, keyed to the voiceover words."""
import math
import os
import random
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)

from bik.core import Timeline, Camera, Track, Steps, clamp, lerp, prog, e_io, e_out, e_in, e_back, bump, fade  # noqa: E402
from bik.draw import text, text_width, rect, grad_rect, grad_alpha, glow, circle, poly, line, dashed, mix, shade, shadow, C, P  # noqa: E402
from bik import world, fx, sfx, arabic  # noqa: E402
from bik.captions import Captions, word_timings  # noqa: E402

W, H = 1080, 1920
LABELS = ["hook", "break1", "fix1", "break2", "fix2", "break3", "fix3", "break4", "fix4", "cta", "reveal", "stat",
          "closer", "tag"]
EMPH = ["CONGRATS", "UNTIL", "SNAPS", "DEAD", "POWER", "STRANGERS", "FOLLOW", "DING", "ZERO", "YOURSELF", "QUIT",
        "FASTER"]

# ---- Arabic (Palestinian) version: same picture, Arabic narration, captions and labels
EMPH_AR = ["مبروك", "لحد", "ينقطع", "دغري", "الكهربا", "غريب", "تابعني", "رنة", "صفر", "بإيدك", "بيستسلموا",
           "أسرع"]
# English anchor word -> the Arabic word that carries the same moment in that beat
AR_KEYS = {
    ("hook", "ROPE"): "حبل", ("hook", "PULL"): "سحبت", ("hook", "CONGRATS"): "مبروك",
    ("break1", "FOUR"): "أربع", ("break1", "ARMS"): "إيديك", ("break1", "QUIT"): "بيستسلموا",
    ("fix1", "MOTOR"): "موتور", ("fix1", "PULLEY"): "بكرة", ("fix1", "COUNTERWEIGHT"): "ثقل",
    ("fix1", "BARELY"): "بالكاد",
    ("break2", "UNTIL"): "لحد", ("break2", "SNAPS"): "ينقطع",
    ("fix2", "RAILS"): "سكك", ("fix2", "CABLES"): "كوابل", ("fix2", "GOVERNOR"): "منظم",
    ("fix2", "FALLS"): "نزل", ("fix2", "BITE"): "بتعض", ("fix2", "DEAD"): "دغري",
    ("break3", "OPENS"): "فتح", ("break3", "ONE"): "الأول",
    ("fix3", "LOCK"): "قفل", ("fix3", "BEAM"): "شعاع", ("fix3", "EDGES"): "حواف", ("fix3", "TOUCH"): "تلمس",
    ("break4", "CUTS"): "تقطع", ("break4", "ELEVEN"): "إحدعش",
    ("fix4", "BATTERY"): "بطارية", ("fix4", "PHONE"): "تلفون", ("fix4", "RESCUE"): "إنقاذ",
    ("fix4", "CRAWLS"): "بيمشي", ("fix4", "OPENS"): "بيفتح",
    ("cta", "FOLLOW"): "تابعني",
    ("reveal", "HIDE"): "خبي", ("reveal", "SHINY"): "لامعين", ("reveal", "BUTTONS"): "أزرار", ("reveal", "DING"): "رنة",
    ("stat", "ONE"): "بير", ("stat", "TWENTY"): "عشرين", ("stat", "ZERO"): "صفر",
    ("closer", "CONGRATS"): "مبروك",
    ("tag", "PRESSING"): "كبست", ("tag", "TEN"): "عشر", ("tag", "FASTER"): "أسرع",
}
# ---- Saudi version (lang="ar_sa"): NAMAA Saudi voice, Saudi dialect script
EMPH_SA = ["مبروك", "لين", "ينقطع", "طول", "الكهربا", "غريب", "تابعني", "رنة", "صفر", "بيدك", "تفصل", "أسرع"]
AR_KEYS_SA = {
    ("hook", "ROPE"): "حبل", ("hook", "PULL"): "سحبته", ("hook", "CONGRATS"): "مبروك",
    ("break1", "FOUR"): "أربعة", ("break1", "ARMS"): "يدينك", ("break1", "QUIT"): "تفصل",
    ("fix1", "MOTOR"): "ماطور", ("fix1", "PULLEY"): "بكرة", ("fix1", "COUNTERWEIGHT"): "ثقل",
    ("fix1", "BARELY"): "يادوب",
    ("break2", "UNTIL"): "لين", ("break2", "SNAPS"): "ينقطع",
    ("fix2", "RAILS"): "سكك", ("fix2", "CABLES"): "كيابل", ("fix2", "GOVERNOR"): "منظم",
    ("fix2", "FALLS"): "نزل", ("fix2", "BITE"): "تكمش", ("fix2", "DEAD"): "طول",
    ("break3", "OPENS"): "فتح", ("break3", "ONE"): "الأول",
    ("fix3", "LOCK"): "قفل", ("fix3", "BEAM"): "شعاع", ("fix3", "EDGES"): "أطراف", ("fix3", "TOUCH"): "تلمس",
    ("break4", "CUTS"): "تطفي", ("break4", "ELEVEN"): "إحدعش",
    ("fix4", "BATTERY"): "بطارية", ("fix4", "PHONE"): "تلفون", ("fix4", "RESCUE"): "إنقاذ",
    ("fix4", "CRAWLS"): "يمشي", ("fix4", "OPENS"): "يفتح",
    ("cta", "FOLLOW"): "تابعني",
    ("reveal", "HIDE"): "خب", ("reveal", "SHINY"): "يلمعون", ("reveal", "BUTTONS"): "أزرار", ("reveal", "DING"): "رنة",
    ("stat", "ONE"): "بير", ("stat", "TWENTY"): "عشرين", ("stat", "ZERO"): "صفر",
    ("closer", "CONGRATS"): "مبروك",
    ("tag", "PRESSING"): "ضغطت", ("tag", "TEN"): "عشر", ("tag", "FASTER"): "أسرع",
}
# ---- Syrian version (lang="ar_sy"): Microsoft voice Laith (ar-SY-LaithNeural), Damascene script
EMPH_SY = ["مبروك", "لحتى", "ينقطع", "دغري", "الكهربا", "غريب", "تابعني", "رنة", "صفر", "بإيدك", "بيستسلموا",
           "أسرع"]
AR_KEYS_SY = {
    ("hook", "ROPE"): "حبل", ("hook", "PULL"): "شديت", ("hook", "CONGRATS"): "مبروك",
    ("break1", "FOUR"): "أربع", ("break1", "ARMS"): "إيديك", ("break1", "QUIT"): "بيستسلموا",
    ("fix1", "MOTOR"): "موتور", ("fix1", "PULLEY"): "بكرة", ("fix1", "COUNTERWEIGHT"): "ثقل",
    ("fix1", "BARELY"): "يادوب",
    ("break2", "UNTIL"): "لحتى", ("break2", "SNAPS"): "ينقطع",
    ("fix2", "RAILS"): "سكك", ("fix2", "CABLES"): "كبلات", ("fix2", "GOVERNOR"): "منظم",
    ("fix2", "FALLS"): "نزل", ("fix2", "BITE"): "بتعض", ("fix2", "DEAD"): "دغري",
    ("break3", "OPENS"): "فتح", ("break3", "ONE"): "الأول",
    ("fix3", "LOCK"): "قفل", ("fix3", "BEAM"): "شعاع", ("fix3", "EDGES"): "حواف", ("fix3", "TOUCH"): "تلمس",
    ("break4", "CUTS"): "تقطع", ("break4", "ELEVEN"): "إحدعش",
    ("fix4", "BATTERY"): "بطارية", ("fix4", "PHONE"): "تلفون", ("fix4", "RESCUE"): "إنقاذ",
    ("fix4", "CRAWLS"): "بيمشي", ("fix4", "OPENS"): "بيفتح",
    ("cta", "FOLLOW"): "تابعني",
    ("reveal", "HIDE"): "خبي", ("reveal", "SHINY"): "بيلمعوا", ("reveal", "BUTTONS"): "كبسات", ("reveal", "DING"): "رنة",
    ("stat", "ONE"): "بير", ("stat", "TWENTY"): "عشرين", ("stat", "ZERO"): "صفر",
    ("closer", "CONGRATS"): "مبروك",
    ("tag", "PRESSING"): "كبست", ("tag", "TEN"): "عشر", ("tag", "FASTER"): "أسرع",
}
KEYS_BY_LANG = {"ar": AR_KEYS, "ar_sa": AR_KEYS_SA, "ar_sy": AR_KEYS_SY}
EMPH_BY_LANG = {"en": EMPH, "ar": EMPH_AR, "ar_sa": EMPH_SA, "ar_sy": EMPH_SY}
TEXT = {
    "en": {"follow": ("FOLLOW", "next: a skyscraper"), "stat": [("1", "SHAFT"), ("20", "FLOORS"), ("0", "STAIRS")]},
    "ar": {"follow": ("تابعني", "الجاي: ناطحة سحاب"), "stat": [("1", "بير"), ("20", "طابق"), ("0", "درج")]},
    "ar_sa": {"follow": ("تابعني", "الجاي: ناطحة سحاب"), "stat": [("1", "بير"), ("20", "دور"), ("0", "درج")]},
    "ar_sy": {"follow": ("تابعني", "الجاي: ناطحة سحاب"), "stat": [("1", "بير"), ("20", "طابق"), ("0", "درج")]},
}

FH, SLAB = 260, 16                 # floor height, slab thickness
BX0, BX1, WALL = -380, 380, 20     # building outer x, wall thickness
SX0, SX1 = -360, -100              # shaft
IW0, IW1 = -100, -82               # inner wall (shaft | rooms)
CAR_X0, CAR_W, CAR_H = -300, 190, 205
CAR_CX = CAR_X0 + CAR_W / 2        # -205
CW_X0, CW_W, CW_H = -352, 34, 170
SHV_X, SHV_R = -270, 65            # sheave: right tangent = car center, left = counterweight center
RAIL_L, RAIL_R = -307, -106
MR_X0, MR_X1, MR_H = -380, 60, 215  # machine room on the roof
DOOR_H = 205

WALLS = ["#FBE3C8", "#DDEBDD", "#E3E0F5", "#FCE6EA", "#DCEBF7", "#F6F0D6", "#E8F4F1", "#FDE9D9"]
FACADE, FACADE_DK = "#EDE6DA", "#CFC5B6"
CONCRETE, CONCRETE_HI = "#9AA3AD", "#BAC2CA"
SHAFT_TOP, SHAFT_BOT = "#2B3240", "#3B4252"
WOOD, WOOD_DK, WOOD_LT = "#C98B4E", "#8A5A2F", "#E0A86A"
STEEL, STEEL_DK, STEEL_LT = "#9CA3AF", "#4B5563", "#E5E7EB"


def fy(k):
    """Floor surface y of floor k (floor 1 = ground)."""
    return -(k - 1) * FH


class Elevator:
    def __init__(self, vo_json, vo_wav, lang="en"):
        self.lang = lang
        self.tl = tl = Timeline(vo_json, LABELS, lead=0.5, pause=0.6, tail=2.2)
        self.words = word_timings(vo_wav, tl)
        self.cap = Captions(self.words, EMPH_BY_LANG[lang], hide=[(tl.pause_start, tl.s("cta"))])
        self.duration = tl.duration
        self._tracks()

    # word time helper: start of a word in a beat, or a fraction of the beat as fallback
    def w(self, lab, key, frac=0.5, nth=0):
        if self.lang in KEYS_BY_LANG:
            key = KEYS_BY_LANG[self.lang].get((lab, key), key)
        t = self.cap.find(lab, key, nth)
        if t is None:
            t = lerp(self.tl.s(lab), self.tl.e(lab), frac)
        return t

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        tl, w = self.tl, self.w
        s, e, has = tl.s, tl.e, tl.has
        T = self.T = {}
        T["rope"] = w("hook", "ROPE", 0.15)
        T["pull"] = w("hook", "PULL", 0.4)
        T["cong"] = w("hook", "CONGRATS", 0.65)
        T["four"] = w("break1", "FOUR", 0.2)
        T["arms"] = w("break1", "ARMS", 0.55)
        T["quit"] = w("break1", "QUIT", 0.7)
        T["motor"] = w("fix1", "MOTOR", 0.15)
        T["pulley"] = w("fix1", "PULLEY", 0.3)
        T["cw"] = w("fix1", "COUNTERWEIGHT", 0.45)
        T["barely"] = w("fix1", "BARELY", 0.85)
        T["until2"] = w("break2", "UNTIL", 0.6)
        T["snap"] = w("break2", "SNAPS", 0.92)
        T["rails"] = w("fix2", "RAILS", 0.12)
        T["cables"] = w("fix2", "CABLES", 0.22)
        T["gov"] = w("fix2", "GOVERNOR", 0.38)
        T["falls"] = w("fix2", "FALLS", 0.55)
        T["bite"] = w("fix2", "BITE", 0.75)
        T["dead"] = w("fix2", "DEAD", 0.95)
        if has("break3"):
            T["opens3"] = w("break3", "OPENS", 0.45)
            T["one3"] = w("break3", "ONE", 0.95)
            T["lock"] = w("fix3", "LOCK", 0.15)
            T["beam"] = w("fix3", "BEAM", 0.55)
            T["edges"] = w("fix3", "EDGES", 0.8)
            T["touch"] = w("fix3", "TOUCH", 0.95)
        T["cut"] = w("break4", "CUTS", 0.45)
        T["eleven"] = w("break4", "ELEVEN", 0.85)
        T["batt"] = w("fix4", "BATTERY", 0.15)
        T["phone"] = w("fix4", "PHONE", 0.35)
        T["rescue"] = w("fix4", "RESCUE", 0.5)
        T["crawls"] = w("fix4", "CRAWLS", 0.62)
        T["opens4"] = w("fix4", "OPENS", 0.88)
        T["pause"] = tl.pause_start
        T["follow"] = w("cta", "FOLLOW", 0.4)
        T["hide"] = w("reveal", "HIDE", 0.1)
        T["shiny"] = w("reveal", "SHINY", 0.4)
        T["buttons"] = w("reveal", "BUTTONS", 0.7)
        T["ding"] = w("reveal", "DING", 0.95)
        T["one"] = w("stat", "ONE", 0.1)
        T["twenty"] = w("stat", "TWENTY", 0.4)
        T["zero"] = w("stat", "ZERO", 0.75)
        T["cong2"] = w("closer", "CONGRATS", 0.1)
        # comedy tag: mash the call button ten times, the display still says 20, then ticks to 19 (womp)
        T["tag"] = s("tag")
        T["press"] = w("tag", "PRESSING", 0.2)
        T["faster"] = w("tag", "FASTER", 0.9)
        n_taps = 10
        t0, t1 = T["press"], max(T["press"] + 1.2, T["faster"])
        self.taps = [lerp(t0, t1, i / (n_taps - 1)) for i in range(n_taps)]
        T["flip"] = e("tag") + 0.25

        # --- box floor position
        bf = self.bf = Track(1.0)
        bf.to(T["pull"], 2.0, T["cong"] - T["pull"])
        bf.to(s("break1") - 0.05, 1.0, 0.5, e_io)
        bf.to(T["four"] + 0.5, 1.32, max(0.6, T["quit"] - T["four"] - 0.5), e_out)
        bf.to(T["quit"], 1.0, 0.32, e_in)
        bf.to(T["barely"] - 0.4, 3.0, clamp(s("break2") + 0.2 - (T["barely"] - 0.4), 1.0, 2.0))
        bf.to(s("break2") + 0.25, 9.0, max(1.2, T["snap"] - s("break2") - 0.6))
        bf.to(T["snap"], 8.3, 0.55, e_in)
        bf.to(T["falls"] - 0.05, 6.6, max(0.3, T["bite"] - T["falls"] + 0.05), e_in)
        bf.to(T["bite"] + 0.02, 6.7, 0.12, e_out)
        bf.to(T["bite"] + 0.16, 6.6, 0.18, e_out)
        if has("break3"):
            bf.to(s("break3"), 1.0, 1.4)
        bf.to(s("break4") + 0.1, 6.5, max(1.0, T["cut"] - s("break4") - 0.2))
        bf.to(T["crawls"], 6.0, max(0.8, T["opens4"] - T["crawls"]))
        bf.to(s("reveal"), 1.0, 1.0)

        self.floors = Steps(3.0)
        g0 = s("break2") + 0.1
        g1 = max(g0 + 1.4, T["until2"] - 0.1)
        self.grow1 = (g0, (g1 - g0) / 7)
        self.floors.add(g0, (g1 - g0) / 7, 7)
        self.grow2 = (s("stat") + 0.05, 0.13)
        self.floors.add(s("stat") + 0.05, 0.13, 10)

        self.dusk = Track(0.0).to(s("stat") - 0.4, 0.85, 2.2)
        self.dim = Track(0.0).to(T["cut"], 0.38, 0.25).to(T["rescue"], 0.2, 0.8).to(e("fix4") - 0.35, 0.0, 0.4)
        self.lights = Track(1.0).to(T["cut"], 0.0, 0.18).to(e("fix4") - 0.35, 1.0, 0.3)

        # camera
        cam = self.cam = Camera(-40, -300, 1.12)
        cam.key(0.0, -60, -260, 1.28, 0.6)                 # quick push-in on the first frame
        cam.key(0.7, -80, -265, 1.36, T["cong"] - 0.7)     # slow drift while the box goes up
        cam.key(s("break1"), -110, -235, 1.48, 0.8)
        cam.key(s("fix1") + 0.05, 0, -430, 0.98, 1.0)
        cam.key(s("break2") + 0.1, 0, -1260, 0.5, 2.0)
        cam.key(T["snap"] - 0.25, -170, fy(9) - 120, 0.85, 0.45)
        cam.key(s("fix2") + 0.05, -110, -2330, 0.6, 0.8)
        cam.key(T["falls"] - 0.35, -180, fy(7.2) - 60, 0.85, 0.6)
        if has("break3"):
            cam.key(s("break3"), -60, -700, 0.9, 1.2)
            cam.key(T["opens3"] - 0.5, -90, fy(5) - 120, 1.25, 0.7)
            cam.key(T["one3"] - 0.6, -60, -700, 0.9, 0.8)
            cam.key(T["beam"] - 0.45, -130, -230, 1.35, 0.8)
        cam.key(s("break4"), -60, fy(6) - 200, 0.74, 1.4)
        cam.key(T["batt"] - 0.3, -160, fy(6.5) - 150, 1.1, 0.7)
        cam.key(s("reveal") - 0.1, -40, -1330, 0.52, 1.0)
        cam.key(T["shiny"] - 0.45, -175, -255, 1.32, 1.3)
        cam.key(s("stat") - 0.05, 0, -3000, 0.2, 1.7)
        cam.key(s("closer"), 0, -2950, 0.21, 3.2)
        cam.key(s("tag") - 0.2, -170, -215, 1.6, 0.55)  # comic snap-zoom back to the lobby

        self.shakes = [(T["quit"] + 0.3, 0.35, 14), (T["snap"], 0.6, 26), (T["bite"], 0.35, 18), (T["cut"], 0.3, 8)]
        self.rng = random.Random(42)

    # ----------------------------------------------------------------- helpers
    def checks(self):
        T, tl = self.T, self.tl
        out = [(T["barely"] + 0.5, "motor"), (T["dead"] + 0.1, "car"), (tl.e("fix4") - 0.2, "car")]
        if tl.has("fix3"):
            out.append((tl.e("fix3") - 0.25, "door1"))
        return out

    def car_y(self, t):
        return fy(self.bf.at(t))  # car floor (bottom) y

    def top_y(self, t):
        return fy(1) - self.floors.at(t) * FH

    # ------------------------------------------------------------------ frame
    def draw(self, c, t):
        T, tl = self.T, self.tl
        real_t = t
        if tl.pause_start <= t < tl.s("cta"):
            t = tl.pause_start  # the fake pause freezes the picture
        dusk = self.dusk.at(t)
        world.sky(c, W, H, dusk, t)
        cx, cy, z = self.cam.at(t)
        for t0, d, amp in self.shakes:
            if t0 <= t < t0 + d:
                k = (1 - (t - t0) / d) * amp
                cx += math.sin(t * 91) * k / z
                cy += math.cos(t * 77) * k / z
        ground_sy = (0 - cy) * z + H / 2
        # far skyline: parallax layer anchored on the horizon
        zf = clamp(0.55 * z ** 0.6, 0.12, 0.85)
        c.save()
        c.translate(W / 2, ground_sy)
        c.scale(zf, zf)
        c.translate(-cx * 0.25, 0)
        world.skyline(c, -4200, 4200, dusk)
        c.restore()
        # world layer
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(z, z)
        c.translate(-cx, -cy)
        self.draw_neighbors(c, t, dusk)
        world.ground(c, -12000, 12000, 9000, dusk)
        self.draw_building(c, t, dusk)
        self.draw_world_fx(c, t)
        c.restore()
        # screen overlays
        self.draw_screen_fx(c, real_t, dusk)
        self.cap.draw(c, W, real_t)

    # -------------------------------------------------------------- neighbors
    def draw_neighbors(self, c, t, dusk):
        lit = clamp((dusk - 0.3) / 0.5)
        for x, kind in ((-640, 0), (650, 1), (-1420, 2), (1460, 0), (-2300, 1), (2350, 2)):
            world.tree(c, x, 1.15, dusk, kind)
        world.house(c, -1020, 470, 320, "#F4E3C3", "#B84A3A", dusk, lit)
        world.house(c, 1050, 440, 300, "#DDE7F0", "#4A6FA5", dusk, lit)
        world.house(c, -1880, 420, 290, "#E8F0DA", "#7A5C3E", dusk, lit)
        world.house(c, 1900, 460, 320, "#F7DCDC", "#5B4B8A", dusk, lit)

    # --------------------------------------------------------------- building
    def draw_building(self, c, t, dusk):
        T, tl = self.T, self.tl
        n = self.floors.at(t)
        nf = int(math.ceil(n - 1e-6))
        top = self.top_y(t)
        lights = self.lights.at(t)
        shaft_a = e_io(prog(t, tl.s("fix1") + 0.15, tl.s("fix1") + 0.8))
        # building shadow on the ground
        rect(c, BX0 - 10, -6, BX1 - BX0 + 20, 30, "#000000", 0.18, r=12, blur=10)
        c.save()
        c.clipRect(C_rect(BX0 - 60, top, BX1 - BX0 + 120, -top + 40))
        # rooms + shaft per floor
        for k in range(1, nf + 1):
            y_floor = fy(k)
            y_ceil = fy(k + 1) + SLAB
            if y_floor < top - 1:
                continue
            col = mix(WALLS[(k - 1) % len(WALLS)], shade(WALLS[(k - 1) % len(WALLS)], -0.5), dusk * 0.6)
            dark = 1 - lights
            rect(c, BX0 + WALL, y_ceil, BX1 - BX0 - 2 * WALL, y_floor - y_ceil, mix(col, "#1B2233", dark * 0.75))
            world.room_decor(c, IW1, y_ceil, BX1 - WALL - IW1, y_floor - y_ceil, seed=k * 13 + 1,
                             lights=lights, dusk=dusk)
            grad_alpha(c, BX0 + WALL, y_ceil, BX1 - BX0 - 2 * WALL, 34, "#000000", 0.16, 0.0)
            if dark > 0:
                rect(c, IW1, y_ceil, BX1 - WALL - IW1, y_floor - y_ceil, "#0B1020", dark * 0.55)
            if shaft_a > 0:
                grad_rect(c, SX0, y_ceil - SLAB, SX1 - SX0, y_floor - y_ceil + SLAB, SHAFT_TOP, SHAFT_BOT, a=shaft_a)
        # slabs
        for k in range(1, nf + 2):
            ys = fy(k)
            if ys < top - 1:
                continue
            if k == 1:
                continue
            # slab across rooms
            rect(c, IW0, ys, BX1 - IW0, SLAB, CONCRETE)
            rect(c, IW0, ys, BX1 - IW0, 4, CONCRETE_HI)
            # slab across the shaft fades out once the shaft exists; floor 2 has the hole in the house phase
            if k == 2:
                rect(c, BX0, ys, (CAR_X0 - 18) - BX0, SLAB, CONCRETE, 1 - shaft_a)
                rect(c, CAR_X0 + CAR_W + 4, ys, IW0 - (CAR_X0 + CAR_W + 4), SLAB, CONCRETE, 1 - shaft_a)
                rect(c, CAR_X0 - 18, ys, CAR_W + 22, SLAB, shade(CONCRETE, -0.5), 1 - shaft_a)  # the hole
            elif k <= nf:
                rect(c, BX0, ys, IW0 - BX0, SLAB, CONCRETE, 1 - shaft_a)
        c.restore()
        hide = e_out(prog(t, T["hide"] - 0.05, T["hide"] + 0.6))
        if shaft_a * (1 - hide) > 0:
            self.draw_pit(c, shaft_a * (1 - hide))
        # roof slab + parapet (moves with the top)
        rect(c, BX0 - 10, top - 4, BX1 - BX0 + 20, SLAB + 8, shade(CONCRETE, -0.08))
        rect(c, BX0 - 10, top - 34, 22, 34, FACADE_DK)
        rect(c, BX1 - 12, top - 34, 22, 34, FACADE_DK)
        # outer walls
        rect(c, BX0, top, WALL, -top, FACADE)
        rect(c, BX1 - WALL, top, WALL, -top, FACADE)
        # inner wall with hoistway doors
        if shaft_a > 0:
            self.draw_inner_wall(c, t, nf, top, shaft_a)
        # machine room on the roof
        mr_p = e_back(prog(t, T["motor"] - 0.45, T["motor"] - 0.05))
        if mr_p > 0:
            self.draw_machine_room(c, t, top, mr_p)
        # rails, counterweight, ropes, car
        self.draw_shaft_parts(c, t, top, shaft_a)
        self.draw_people_in_rooms(c, t, nf, top)
        # facade panel with elevator doors (reveal onward)
        fp = e_out(prog(t, T["hide"] - 0.05, T["hide"] + 0.6))
        if fp > 0:
            self.draw_facade(c, t, nf, top, fp)
        if t >= self.tl.s("tag") - 0.4:
            self.draw_gag(c, t)

    def draw_pit(self, c, a):
        rect(c, SX0 - 16, 0, SX1 - SX0 + 32, 132, "#7B8490", a)
        grad_rect(c, SX0, 0, SX1 - SX0, 116, SHAFT_BOT, "#1C212C", a=a)
        for bx in (CAR_X0 + 42, CAR_X0 + CAR_W - 42):
            rect(c, bx - 24, 102, 48, 14, "#4B5563", a, r=3)
            pts = [(bx + (-15 if i % 2 else 15), 102 - i * 9) for i in range(9)]
            poly(c, pts, "#F59E0B", a, stroke=5, close=False)
            rect(c, bx - 19, 16, 38, 12, "#4B5563", a, r=3)

    def draw_inner_wall(self, c, t, nf, top, a):
        for k in range(1, nf + 1):
            y_floor = fy(k)
            y_ceil = fy(k + 1) + SLAB
            if y_floor < top - 1:
                continue
            rect(c, IW0, y_ceil - SLAB, IW1 - IW0, y_floor - y_ceil + SLAB - DOOR_H, "#CBD5E1", a)
            o = self.door_open(k, t)
            dy = DOOR_H * o
            c.save()
            c.clipRect(C_rect(IW0 - 2, y_ceil, IW1 - IW0 + 4, y_floor - y_ceil))
            rect(c, IW0, y_floor - DOOR_H - dy, IW1 - IW0, DOOR_H, "#94A3B8", a)
            rect(c, IW0 + 3, y_floor - DOOR_H - dy + 6, 4, DOOR_H - 12, "#E2E8F0", a * 0.8)
            c.restore()
            # locks (fix3)
            if "lock" in self.T:
                lp = prog(t, self.T["lock"] + 0.05 * k, self.T["lock"] + 0.05 * k + 0.3)
                lp *= 1 - prog(t, self.T["hide"] - 0.05, self.T["hide"] + 0.4)
                if lp > 0:
                    unlocked = abs(self.bf.at(t) - k) < 0.15
                    self.padlock(c, IW1 + 34, y_floor - 112, 1.5 * e_back(lp), unlocked, a)

    def door_open(self, k, t):
        T, tl = self.T, self.tl
        o = 0.0
        if "opens3" in T and k == 5:
            o = e_out(prog(t, T["opens3"], T["opens3"] + 0.5)) * (1 - e_io(prog(t, T["lock"] + 0.35, T["lock"] + 0.8)))
        if "edges" in T and k == 1:
            # open while parked, closes on "edges", hits the rider, bounces back open on "touch"
            start = e_out(prog(t, tl.s("break3") + 1.3, tl.s("break3") + 1.8))
            close = e_io(prog(t, T["edges"], T["touch"])) * 0.36
            reopen = e_out(prog(t, T["touch"], T["touch"] + 0.35))
            leave = e_io(prog(t, tl.s("break4"), tl.s("break4") + 0.4))
            o = start * (1 - close * (1 - reopen)) * (1 - leave)
        if k == 6:
            o = e_out(prog(t, T["opens4"], T["opens4"] + 0.5)) * (1 - prog(t, tl.s("reveal"), tl.s("reveal") + 0.4))
        return o

    def padlock(self, c, x, y, s, unlocked, a=1.0):
        c.save()
        c.translate(x, y)
        c.scale(s, s)
        col = "#22C55E" if unlocked else "#F59E0B"
        rect(c, -18, -6, 36, 30, col, a, r=6)
        circle(c, 0, 8, 5, "#1F2937", a)
        sh = -10 if unlocked else 0
        c.drawArc(C_rect(-12, -26 + sh, 24, 30), 180, 180, False, P("#4B5563", a, stroke=6))
        c.restore()

    def draw_machine_room(self, c, t, top, p):
        T = self.T
        h = MR_H * p
        rect(c, MR_X0, top - h, MR_X1 - MR_X0, h, FACADE_DK)
        rect(c, MR_X0 + 14, top - h + 14, MR_X1 - MR_X0 - 28, max(0, h - 14), "#3A4150")
        rect(c, MR_X0 - 6, top - h - 14, MR_X1 - MR_X0 + 12, 16, shade(CONCRETE, -0.1))
        yb = top  # machine room floor = roof
        # motor housing (drops in on "motor")
        mp = prog(t, T["motor"], T["motor"] + 0.35)
        if mp > 0:
            dy = (1 - e_back(mp)) * -160
            rect(c, -255, yb - 175 + dy, 115, 100, "#2F6FDE", r=14)
            rect(c, -255, yb - 175 + dy, 115, 24, "#4C8BF5", r=12)
            for i in range(4):
                rect(c, -238 + i * 22, yb - 140 + dy, 10, 52, "#245BB8", r=4)
            # load gauge
            gx, gy = 10, yb - 140
            circle(c, gx, gy, 36, "#F8FAFC")
            circle(c, gx, gy, 36, "#334155", stroke=6)
            c.drawArc(C_rect(gx - 28, gy - 28, 56, 56), 200, 50, False, P("#22C55E", 1, stroke=8, cap="butt"))
            c.drawArc(C_rect(gx - 28, gy - 28, 56, 56), 250, 40, False, P("#F59E0B", 1, stroke=8, cap="butt"))
            c.drawArc(C_rect(gx - 28, gy - 28, 56, 56), 290, 50, False, P("#EF4444", 1, stroke=8, cap="butt"))
            strain = e_out(prog(t, T["motor"] + 0.2, T["motor"] + 0.6))
            relief = e_out(prog(t, T["barely"] - 0.15, T["barely"] + 0.45))
            ang = lerp(-150, lerp(-30, -125, relief), strain)
            r = math.radians(ang)
            line(c, gx, gy, gx + math.cos(r) * 26, gy + math.sin(r) * 26, "#111827", 5)
            circle(c, gx, gy, 5, "#111827")
            line(c, gx - 34, gy + 14, -140, yb - 128 + dy, "#111827", 4)
        # sheave (drops in on "pulley"), rotates with the rope
        sp = prog(t, T["pulley"], T["pulley"] + 0.35)
        if sp > 0:
            dy = (1 - e_back(sp)) * -160
            sy = yb - 92 + dy
            self.sheave_xy = (SHV_X, sy)
            rot = self.bf.at(t) * FH / SHV_R
            rect(c, SHV_X - 8, sy, 16, yb - sy, "#4B5563")
            circle(c, SHV_X, sy, SHV_R, "#6B7280")
            circle(c, SHV_X, sy, SHV_R - 8, STEEL)
            for i in range(5):
                a = rot + i * 2 * math.pi / 5
                line(c, SHV_X, sy, SHV_X + math.cos(a) * (SHV_R - 12), sy + math.sin(a) * (SHV_R - 12), "#6B7280", 8)
            circle(c, SHV_X, sy, 14, "#374151")
        # governor (fix2)
        gp = prog(t, T["gov"], T["gov"] + 0.35)
        if gp > 0:
            gy = yb - 52
            s = e_back(gp)
            c.save()
            c.translate(-126, gy)
            c.scale(s, s)
            circle(c, 0, 0, 22, "#F59E0B")
            circle(c, 0, 0, 22, "#92400E", stroke=5)
            rot = self.bf.at(t) * 4
            for i in range(4):
                a = rot + i * math.pi / 2
                line(c, 0, 0, math.cos(a) * 16, math.sin(a) * 16, "#92400E", 4)
            c.restore()

    def battery(self, c, x, y, s, t):
        c.save()
        c.translate(x, y)
        c.scale(s, s)
        glow(c, 0, 0, 90, "#22C55E", 0.35 + 0.15 * math.sin(t * 6))
        rect(c, -34, -48, 68, 96, "#111827", r=10)
        rect(c, -12, -58, 24, 12, "#111827", r=4)
        lvl = 0.5 + 0.5 * math.sin(t * 3) ** 2
        rect(c, -26, 40 - 80 * lvl, 52, 80 * lvl, "#22C55E", r=6)
        poly(c, [(4, -30), (-12, 4), (0, 4), (-6, 30), (14, -6), (2, -6)], "#FFFFFF")
        c.restore()

    def draw_shaft_parts(self, c, t, top, shaft_a):
        T, tl = self.T, self.tl
        f = self.bf.at(t)
        car_bottom = fy(f)
        car_top = car_bottom - CAR_H
        sheave_ready = t >= T["pulley"] + 0.3
        sy = top - 92
        # rails (fix2)
        rp = e_out(prog(t, T["rails"], T["rails"] + 0.45))
        if rp > 0:
            ln = (0 - top) * rp
            rect(c, RAIL_L - 3, top, 8, ln, STEEL_LT)
            rect(c, RAIL_R - 3, top, 8, ln, STEEL_LT)
            rect(c, RAIL_L - 3, top, 3, ln, STEEL_DK, 0.6)
            rect(c, RAIL_R - 3, top, 3, ln, STEEL_DK, 0.6)
        # governor rope down the shaft
        if prog(t, T["gov"], T["gov"] + 0.35) > 0:
            line(c, -104, top - 52, -104, 0, "#B45309", 3, a=e_out(prog(t, T["gov"] + 0.2, T["gov"] + 0.6)))
        # counterweight (drops in on "counterweight")
        cwp = prog(t, T["cw"], T["cw"] + 0.5)
        if cwp > 0 and sheave_ready:
            ff = f
            if T["snap"] <= t < T["cables"]:
                ff = self.bf.at(T["snap"])
            cw_top_target = min(top + 24 + (ff - 1) * FH, -CW_H - 12)
            cw_top = lerp(top - 120, cw_top_target, e_in(cwp))
            rect(c, CW_X0, cw_top, CW_W, CW_H, "#374151", r=4)
            for i in range(5):
                y0 = cw_top + 18 + i * 30
                poly(c, [(CW_X0, y0), (CW_X0 + CW_W, y0 - 14), (CW_X0 + CW_W, y0), (CW_X0, y0 + 14)], "#FACC15", 0.9)
            line(c, CW_X0 + CW_W / 2, sy, CW_X0 + CW_W / 2, cw_top, "#C8A26B" if t < T["cables"] else "#4B5563", 6)
            self.cw_rect = (CW_X0, cw_top, CW_W, CW_H)
        # ropes from the car
        if t < T["pulley"] + 0.3:
            # house phase: little ceiling pulley on floor 2 and the hauler
            py = fy(3) + SLAB + 34
            ps_ = e_back(prog(t, T["rope"] - 0.25, T["rope"] + 0.05))
            if ps_ > 0:
                c.save()
                c.translate(CAR_CX, fy(3) + SLAB)
                c.scale(ps_, ps_)
                c.translate(-CAR_CX, -(fy(3) + SLAB))
                line(c, CAR_CX, py - 18, CAR_CX, fy(3) + SLAB, "#4B5563", 6)
                circle(c, CAR_CX, py, 18, "#6B7280")
                circle(c, CAR_CX, py, 6, "#374151")
                c.restore()
            hx, hy = self.hauler_hands(t)
            ha = 1 - prog(t, tl.s("fix1"), tl.s("fix1") + 0.4)
            k = e_out(prog(t, T["rope"], T["rope"] + 0.5))
            if k > 0:
                k1, k2 = clamp(k * 2), clamp(k * 2 - 1)
                line(c, CAR_CX, car_top, CAR_CX, lerp(car_top, py, k1), "#C8A26B", 7)
                if k2 > 0:
                    line(c, CAR_CX + 16, py, lerp(CAR_CX + 16, hx, k2), lerp(py, hy, k2), "#C8A26B", 7, a=ha)
        else:
            if t < T["snap"]:
                arc_rope(c, SHV_X, sy, SHV_R, "#C8A26B", 7)
                line(c, CAR_CX, sy, CAR_CX, car_top, "#C8A26B", 7)
            elif t < T["cables"]:
                # snapped: stub on the car whips, top end recoils
                k = prog(t, T["snap"], T["snap"] + 0.5)
                arc_rope(c, SHV_X, sy, SHV_R, "#C8A26B", 7)
                line(c, CAR_CX, sy, CAR_CX + 30 * math.sin(t * 30) * (1 - k), sy + lerp(400, 120, e_out(k)), "#C8A26B", 7)
                line(c, CAR_CX, car_top, CAR_CX - 40 * math.sin(t * 25) * (1 - k * 0.6), car_top - 120, "#C8A26B", 7)
            else:
                cp = e_out(prog(t, T["cables"], T["cables"] + 0.4))
                arc_rope(c, SHV_X, sy, SHV_R, "#4B5563", 6)
                for dx in (-12, 0, 12):
                    y_end = lerp(sy, car_top, cp)
                    line(c, CAR_CX + dx, sy, CAR_CX + dx, y_end, "#4B5563", 5)
        # the car
        self.draw_car(c, t, car_bottom)
        # clamps (fix2 "bite")
        cl = prog(t, T["bite"] - 0.05, T["bite"] + 0.1) * (1 - prog(t, T["dead"] + 0.5, T["dead"] + 0.8))
        if cl > 0:
            for x0, d in ((RAIL_L, 1), (RAIL_R, -1)):
                xx = x0 + 4 * d
                poly(c, [(xx, car_bottom - 8), (xx + 26 * d, car_bottom - 8), (xx, car_bottom + 26)], "#F97316", cl)
                poly(c, [(xx, car_bottom - 8), (xx + 26 * d, car_bottom - 8), (xx, car_bottom + 26)], "#7C2D12", cl, stroke=3)
            fx.sparks(c, RAIL_L, car_bottom, t, T["bite"], 0.8, seed=3, size=1.2)
            fx.sparks(c, RAIL_R, car_bottom, t, T["bite"], 0.8, seed=4, size=1.2)
        # speed lines while falling
        fall_a = bump(t, T["snap"], T["snap"] + 0.6) + bump(t, T["falls"] - 0.05, T["bite"] + 0.05)
        if fall_a > 0:
            fx.speed_lines(c, CAR_X0, car_top, CAR_W, CAR_H, fall_a, t, up=True)
        rise_a = bump(t, self.tl.s("break2") + 0.3, T["snap"] - 0.3) * 0.6
        if rise_a > 0:
            fx.speed_lines(c, CAR_X0, car_top, CAR_W, CAR_H, rise_a, t, up=False)

    def hauler_hands(self, t):
        T = self.T
        pulling = (T["pull"] - 0.2 <= t < T["cong"]) or (T["four"] + 0.3 <= t < T["quit"])
        ph = math.sin(t * 9) if pulling else 0
        return -40 + 18, fy(2) - 118 + ph * 22

    def draw_car(self, c, t, bottom):
        pop = e_back(prog(t, 0.08, 0.42))
        if pop <= 0:
            return
        if pop != 1.0:
            c.save()
            c.translate(CAR_CX, bottom)
            c.scale(pop, pop)
            c.translate(-CAR_CX, -bottom)
        self._draw_car_body(c, t, bottom)
        if pop != 1.0:
            c.restore()

    def _draw_car_body(self, c, t, bottom):
        T, tl = self.T, self.tl
        x0, top = CAR_X0, bottom - CAR_H
        shadow(c, x0, top, CAR_W, CAR_H, r=10, a=0.25, blur=12, dy=6)
        # back wall planks
        for i in range(5):
            rect(c, x0 + 6, top + 8 + i * 39, CAR_W - 12, 36, WOOD if i % 2 else shade(WOOD, -0.08))
        # emergency light inside when the power is out
        em = prog(t, T["batt"] + 0.2, T["batt"] + 0.5) * (1 - prog(t, tl.e("fix4") - 0.35, tl.e("fix4")))
        if em > 0:
            glow(c, x0 + CAR_W / 2, top + 30, 140, "#FFE7A3", 0.5 * em)
        # passengers
        for d in self.riders(t):
            if d["inside"]:
                world.person(c, d["x"], d["y"], d["h"], walk=d["walk"], sweat=d["sweat"], **world.crowd_colors(d["ci"]))
        # frame: floor, roof, posts, brackets
        rect(c, x0, bottom - 14, CAR_W, 14, WOOD_DK, r=3)
        rect(c, x0, top, CAR_W, 14, WOOD_DK, r=3)
        rect(c, x0, top, 12, CAR_H, WOOD_DK, r=3)
        rect(c, x0 + CAR_W - 12, top, 12, CAR_H, WOOD_DK, r=3)
        for (bx, by) in ((x0, top), (x0 + CAR_W - 22, top), (x0, bottom - 22), (x0 + CAR_W - 22, bottom - 22)):
            rect(c, bx, by, 22, 22, "#6B7280", r=4)
        circle(c, CAR_CX, top - 6, 9, "#6B7280")
        bp = prog(t, T["batt"], T["batt"] + 0.35) * (1 - prog(t, tl.s("reveal") - 0.2, tl.s("reveal")))
        if bp > 0:
            self.battery(c, x0 + CAR_W - 42, top - 30, 0.6 * e_back(bp), t)
            line(c, x0 + CAR_W - 42, top - 4, CAR_CX + 12, top - 2, "#111827", 4, a=bp)
        # emergency phone (fix4)
        pp = prog(t, T["phone"], T["phone"] + 0.3) * (1 - prog(t, tl.s("reveal"), tl.s("reveal") + 0.3))
        if pp > 0:
            s = e_back(pp)
            c.save()
            c.translate(x0 + 34, top + 70)
            c.scale(s, s)
            rect(c, -14, -22, 28, 44, "#EF4444", r=6)
            rect(c, -9, -14, 18, 10, "#FEE2E2", r=3)
            ring = (t * 2.2) % 1
            c.drawArc(C_rect(-34 - ring * 10, -34 - ring * 10, 68 + ring * 20, 68 + ring * 20), -60, 120, False,
                      P("#FFFFFF", 1 - ring, stroke=4))
            c.restore()
        # light curtain across the doorway (fix3)
        if "beam" in T:
            bp = prog(t, T["beam"], T["beam"] + 0.25) * (1 - prog(t, tl.s("break4"), tl.s("break4") + 0.3))
            if bp > 0:
                ex = [d for d in self.riders(t) if d["ci"] == 3]
                blocked = bool(ex) and -132 <= ex[0]["x"] <= -64
                bx0, bx1 = x0 + CAR_W - 4, IW1 + 16
                rect(c, bx0, bottom - 196, bx1 - bx0, 186, "#EF4444", 0.10 * bp)
                for i in range(7):
                    yy = bottom - 22 - i * 27
                    hit = blocked and i <= 4
                    col = "#FDE047" if hit else "#EF4444"
                    line(c, bx0, yy, bx1, yy, col, 12, a=0.22 * bp * (0.35 if hit else 1.0))
                    dashed(c, bx0, yy, bx1, yy, col, 5, 9, 6, -t * 60, bp * (0.35 if hit else 1.0))
                    circle(c, bx0, yy, 4.5, "#FCA5A5", bp)
                    circle(c, bx1, yy, 4.5, "#FCA5A5", bp)

    def riders(self, t):
        """Everyone who rides the box: dicts with x, y (feet), h, ci, walk, sweat, inside."""
        T = self.T
        out = []
        if t < T["four"]:
            return out
        bottom = fy(self.bf.at(t)) - 4
        cut = T["cut"] <= t < T["opens4"] + 0.3
        crowd = [(-268, 0.90), (-236, 0.92), (-204, 0.88), (-172, 0.93), (-142, 0.89),
                 (-252, 0.84), (-218, 0.86), (-186, 0.84)]
        four = [(-276, 0.96), (-238, 0.98), (-196, 0.95), (-156, 0.97)]
        roster = []  # (t_in, x, scale, color index, leaves on floor 1)
        for j, (x, sc) in enumerate(crowd[:5]):
            roster.append((T["eleven"] + j * 0.06, x, sc, 4 + j, False))
        for i, (x, sc) in enumerate(four):
            roster.append((T["four"] + i * 0.08, x, sc, i, i == 3 and "edges" in T))
        for j, (x, sc) in enumerate(crowd[5:]):
            roster.append((T["eleven"] + (5 + j) * 0.06, x, sc, 9 + j, False))
        ps, pz = self.tl.pause_start, self.tl.pause
        te = t if t < ps else max(ps, t - pz)
        order = 0
        for t_in, x, sc, ci, exits1 in roster:
            p = prog(t, t_in, t_in + 0.18)
            if p <= 0:
                continue
            d = dict(x=x, y=bottom, h=132 * sc * e_back(p), ci=ci, walk=0.0, sweat=t if cut else 0.0, inside=True)
            if exits1:
                d.update(self._floor1_exit(t, x))
            else:
                k0 = T["opens4"] + 0.25 + order * 0.1
                k = prog(te, k0, k0 + 1.0)
                if k > 0:
                    d.update(x=lerp(x, 10 + order * 27, e_io(k)), y=fy(6) - 4, walk=te * 2 if k < 1 else 0.0,
                             sweat=0.0, inside=k < 0.25)
                order += 1
            out.append(d)
        return out

    def _floor1_exit(self, t, x0):
        """The rider who steps out on floor 1 during the door-safety demo (fix3)."""
        T = self.T
        if t < T["beam"] + 0.1:
            return {}
        y = fy(1) - 4
        if t < T["edges"]:
            k = prog(t, T["beam"] + 0.1, T["edges"])
            return dict(x=lerp(x0, -98, e_io(k)), y=y, walk=t * 2 if k < 1 else 0.0, inside=k < 0.4)
        if t < T["touch"] + 0.15:
            return dict(x=-98, y=y, walk=0.0, inside=False)
        k = prog(t, T["touch"] + 0.15, T["touch"] + 1.4)
        return dict(x=lerp(-98, 210, e_io(k)), y=y, walk=t * 2 if k < 1 else 0.0, inside=False)

    def draw_people_in_rooms(self, c, t, nf, top):
        T, tl = self.T, self.tl
        # the hauler (house phase)
        ha = 1 - prog(t, tl.s("fix1"), tl.s("fix1") + 0.4)
        if ha > 0:
            hx, hy = self.hauler_hands(t)
            straining = T["four"] + 0.3 <= t < T["quit"] + 0.8
            world.person(c, -40, fy(2) - 0, 140, shirt="#F97316", skin="#E0A97E", hair="#2D2A26", pants="#1E3A8A",
                         arms_up=lerp(0.75, 0.55, (math.sin(t * 9) + 1) / 2) if hy != fy(2) - 118 else 0.62,
                         lean=-0.25 if straining else -0.1, a=ha, sweat=t if straining else 0)
            if T["quit"] <= t < T["quit"] + 1.4:
                fx.alert_badge(c, 40, fy(2) - 230, prog(t, T["quit"], T["quit"] + 0.25), 0.9, t)
        # floor-5 neighbor who opens the door (break3)
        if "opens3" in T:
            a = fade(t, tl.s("break3") - 0.2, tl.s("break3") + 0.2, tl.s("break4"), tl.s("break4") + 0.3)
            if a > 0:
                walk_k = prog(t, tl.s("break3") + 0.2, T["opens3"] + 0.3)
                back = e_io(prog(t, T["lock"] + 0.3, T["lock"] + 0.9))
                x = lerp(lerp(200, -52, e_io(walk_k)), 40, back)
                lean = 0.45 * bump(t, T["opens3"] + 0.4, T["lock"] + 0.6) if back < 0.5 else 0
                world.person(c, x, fy(5), 138, shirt="#8B5CF6", skin="#F2C9A0", hair="#9A3412", a=a,
                             walk=t * 2 if 0 < walk_k < 1 or 0 < back < 1 else 0, lean=lean)
        for d in self.riders(t):
            if not d["inside"]:
                world.person(c, d["x"], d["y"], d["h"], walk=d["walk"], sweat=d["sweat"], **world.crowd_colors(d["ci"]))
        # a few residents for life
        res = [(3, 210, 2), (4, 120, 5), (7, 240, 7), (8, 90, 9), (9, 260, 1), (12, 150, 3), (15, 230, 6), (18, 120, 8)]
        for k, x, ci in res:
            if k <= nf and fy(k + 1) > top - 1:
                world.person(c, x + 6 * math.sin(t * 0.8 + k), fy(k), 130, **world.crowd_colors(ci))

    def draw_facade(self, c, t, nf, top, p):
        T, tl = self.T, self.tl
        off = (1 - p) * -460
        c.save()
        c.translate(off, 0)
        x0, x1 = BX0, IW1
        rect(c, x0, top, x1 - x0, -top, "#F1EEE8", p)
        c.restore()
        # penthouse cover over the machine room
        rect(c, MR_X0 - 6, top - MR_H - 14, MR_X1 - MR_X0 + 12, MR_H + 14, "#E4DED3", p, r=6)
        rect(c, MR_X0 - 6, top - MR_H - 14, MR_X1 - MR_X0 + 12, 18, "#CFC7B8", p, r=6)
        c.save()
        c.translate(off, 0)
        for k in range(1, nf + 1):
            yb = fy(k)
            if yb < top - 1:
                continue
            rect(c, x0, yb - 6, x1 - x0, 6, "#D6D0C4", p)
            dx0, dw = -322, 184
            rect(c, dx0 - 12, yb - DOOR_H - 12, dw + 24, DOOR_H + 12, "#9CA3AF", p, r=6)
            op = 0.0
            if k == 1:
                op = e_io(prog(t, T["ding"] + 0.02, T["ding"] + 0.55)) * (1 - e_io(prog(t, tl.s("stat") + 0.4, tl.s("stat") + 0.9)))
            leaf = dw / 2
            if op > 0:
                # car interior visible through the opening
                rect(c, dx0, yb - DOOR_H, dw, DOOR_H, "#C98B4E", p)
                for i, ci in enumerate((1, 4, 7)):
                    world.person(c, dx0 + 40 + i * 52, yb - 4, 130, **world.crowd_colors(ci))
            c.save()
            c.clipRect(C_rect(dx0, yb - DOOR_H, dw, DOOR_H))
            for side in (0, 1):
                lx = dx0 + side * leaf + (-1 if side == 0 else 1) * op * (leaf - 6)
                grad_rect(c, lx, yb - DOOR_H, leaf, DOOR_H, "#E5E7EB", "#A1A7B0", p, horizontal=True)
                rect(c, lx, yb - DOOR_H, leaf, DOOR_H, "#6B7280", p, stroke=2)
            c.restore()
            # shine sweep on "shiny"
            sh = prog(t, T["shiny"] - 0.5 + 0.05 * k, T["shiny"] + 0.2 + 0.05 * k)
            if 0 < sh < 1:
                sx = dx0 + lerp(-60, dw + 60, sh)
                c.save()
                c.clipRect(C_rect(dx0, yb - DOOR_H, dw, DOOR_H))
                poly(c, [(sx, yb - DOOR_H), (sx + 40, yb - DOOR_H), (sx - 30, yb), (sx - 70, yb)], "#FFFFFF", 0.55)
                c.restore()
            # floor indicator light: tracks the car while it zips (stat)
            zipf = self.zip_floor(t)
            on = 1.0 if (zipf is not None and abs(zipf - k) < 0.5) else 0.0
            circle(c, dx0 + dw / 2, yb - DOOR_H - 30, 11, "#FBBF24" if on else "#57534E", p)
            if on:
                glow(c, dx0 + dw / 2, yb - DOOR_H - 30, 46, "#FBBF24", 0.7 * p)
        # call panel on the ground floor
        pp = prog(t, w_or(T, "buttons", 0) - 0.6, w_or(T, "buttons", 0) - 0.3)
        if pp > 0:
            px, py = -126, fy(1) - 160
            rect(c, px, py, 32, 74, "#D1D5DB", p, r=8)
            pressed = t >= T["buttons"] + 0.15
            for i, yy in enumerate((py + 22, py + 52)):
                circle(c, px + 16, yy, 10, "#60A5FA" if (pressed and i == 0) else "#9CA3AF", p)
                if pressed and i == 0:
                    glow(c, px + 16, yy, 34, "#60A5FA", 0.8)
            # tap: a touch dot lands on the button and rings out
            bx_, by_ = px + 16, py + 22
            tp = prog(t, T["buttons"] - 0.12, T["buttons"] + 0.15)
            if 0 < tp and t < T["buttons"] + 0.9:
                al = 1 - prog(t, T["buttons"] + 0.5, T["buttons"] + 0.9)
                circle(c, bx_, by_, lerp(46, 22, e_out(tp)), "#FFFFFF", 0.55 * al)
                rk = prog(t, T["buttons"] + 0.12, T["buttons"] + 0.8)
                if rk > 0:
                    circle(c, bx_, by_, lerp(24, 90, e_out(rk)), "#FFFFFF", (1 - rk) * 0.9, stroke=6)
        c.restore()

    def draw_gag(self, c, t):
        """Comedy tag: the hauler from the hook mashes the call button; the display won't budge."""
        T, tl = self.T, self.tl
        px, py = -126, fy(1) - 160          # call panel (see draw_facade)
        bx, by = px + 16, py + 22           # the up/down button
        a = prog(t, tl.s("tag") - 0.4, tl.s("tag") - 0.1)
        # floor display above the ground-floor doors
        dx, dy = -230, fy(1) - DOOR_H - 44
        rect(c, dx - 52, dy - 26, 104, 52, "#111827", a, r=10)
        rect(c, dx - 52, dy - 26, 104, 52, "#374151", a, r=10, stroke=4)
        flip = prog(t, T["flip"], T["flip"] + 0.12)
        num = "19" if flip >= 1 else "20"
        sq = 1 - 0.6 * bump(t, T["flip"] - 0.02, T["flip"] + 0.14)
        c.save()
        c.translate(dx + 12, dy)
        c.scale(1, sq)
        text(c, num, 0, 15, 42, "#FBBF24", "Poppins-Black", a=a)
        c.restore()
        poly(c, [(dx - 38, dy - 8), (dx - 22, dy - 8), (dx - 30, dy + 6)], "#FBBF24", a)
        # taps: count how many have happened, jiggle the arm on each
        n = sum(1 for tt in self.taps if t >= tt)
        jig = 0.0
        for tt in self.taps:
            k = prog(t, tt - 0.02, tt + 0.1)
            if 0 < k < 1:
                jig = math.sin(math.pi * k)
            rk = prog(t, tt, tt + 0.35)
            if 0 < rk < 1:
                circle(c, bx, by, lerp(14, 52, e_out(rk)), "#FFFFFF", (1 - rk) * 0.9, stroke=5)
        if n:
            glow(c, bx, by, 34, "#60A5FA", 0.9 * a)
            circle(c, bx, by, 10, "#60A5FA", a)
            # the counter badge
            pk = prog(t, self.taps[n - 1], self.taps[n - 1] + 0.12)
            sc = lerp(1.25, 1.0, e_out(pk))
            fade_out = 1 - prog(t, T["flip"] + 0.6, T["flip"] + 1.0)
            c.save()
            c.translate(bx + 6, py - 64)
            c.scale(sc, sc)
            lab = f"×{n}"
            wv = text_width(lab, 40, "Poppins-Black") + 34
            rect(c, -wv / 2, -30, wv, 56, "#FFFFFF", fade_out, r=28)
            text(c, lab, 0, 14, 40, "#EF4444" if n >= 10 else "#111827", "Poppins-Black", a=fade_out)
            c.restore()
        # the masher
        slump = e_out(prog(t, T["flip"] + 0.05, T["flip"] + 0.5))
        self.masher(c, -36, fy(1), 140, (bx + 4 + 9 * jig, by + 2), slump, t, a)

    def masher(self, c, x, y, h, hand, slump, t, a):
        """A person (the hook's hauler colours) reaching one arm to the button; slumps at the end."""
        u = h / 140.0
        shirt, skin, hair, pants = "#F97316", "#E0A97E", "#2D2A26", "#1E3A8A"
        c.save()
        c.translate(x, y)
        c.rotate(-6 * slump)
        c.scale(1, 1 - 0.05 * slump)
        rect(c, -16 * u, -52 * u, 13 * u, 52 * u, pants, a, r=6 * u)
        rect(c, 3 * u, -52 * u, 13 * u, 52 * u, pants, a, r=6 * u)
        line(c, 18 * u, -100 * u, 26 * u, -48 * u, skin, w=11 * u, a=a)          # free arm hangs
        rect(c, -22 * u, -112 * u, 44 * u, 66 * u, shirt, a, r=16 * u)
        rect(c, -22 * u, -112 * u, 44 * u, 18 * u, shade(shirt, 0.12), a * 0.6, r=9 * u)
        hy = -128 * u + 8 * u * slump
        circle(c, 0, hy, 19 * u, skin, a)
        poly(c, [(-20 * u, hy + 2 * u), (-18 * u, hy - 12 * u), (-8 * u, hy - 21 * u), (8 * u, hy - 21 * u),
                 (19 * u, hy - 12 * u), (20 * u, hy), (12 * u, hy - 8 * u), (-6 * u, hy - 10 * u)], hair, a)
        c.restore()
        # pressing arm, drawn in world space so the hand lands on the button; it drops when he slumps
        sx, sy = x - 18 * u, y - 100 * u
        hx = lerp(hand[0], sx - 8 * u, slump)
        hy2 = lerp(hand[1], y - 50 * u, slump)
        line(c, sx, sy, hx, hy2, skin, w=11 * u, a=a)
        circle(c, hx, hy2, 7 * u, skin, a)
        if slump > 0.3:  # sweat drop of defeat
            k = (t * 1.6) % 1.0
            circle(c, x + 22 * u, y - 150 * u + k * 30 * u, 5 * u, "#7DD3FC", a * (1 - k))

    def zip_floor(self, t):
        s = self.tl.s("stat")
        if t < s - 0.1:
            return None
        if t >= self.tl.s("tag") - 0.3:
            return self.floors.at(t)
        nf = self.floors.at(t)
        ph = ((t - s) / 2.4) % 1.0
        tri = ph * 2 if ph < 0.5 else 2 - ph * 2
        return 1 + tri * (nf - 1)

    # ------------------------------------------------------------- world FX
    def draw_world_fx(self, c, t):
        T, tl = self.T, self.tl
        f = self.bf.at(t)
        bottom = fy(f)
        car = (CAR_X0, bottom - CAR_H, CAR_W, CAR_H)
        top = self.top_y(t)
        # outlines on named parts
        def ol(t0, rectv, dur=1.3):
            a = 1 - prog(t, t0 + dur - 0.3, t0 + dur)
            fx.outline(c, *rectv, prog(t, t0, t0 + 0.35), a=a)
        ol(T["cong"], car)
        ol(T["motor"] + 0.3, (-255, top - 175, 115, 100))
        ol(T["pulley"] + 0.3, (SHV_X - SHV_R, top - 92 - SHV_R, SHV_R * 2, SHV_R * 2))
        if hasattr(self, "cw_rect") and t >= T["cw"] + 0.5:
            ol(T["cw"] + 0.5, self.cw_rect)
        ol(T["rails"] + 0.3, (RAIL_L - 10, top, RAIL_R - RAIL_L + 20, -top), 1.0)
        ol(T["cables"] + 0.25, (CAR_CX - 24, top - 92, 48, bottom - CAR_H - (top - 92)), 1.0)
        ol(T["gov"] + 0.3, (-152, top - 78, 52, 52))
        if "beam" in T:
            ol(T["beam"] + 0.2, (CAR_X0 + CAR_W - 6, bottom - 190, 120, 180), 1.1)
        ol(T["batt"] + 0.3, (CAR_X0 + CAR_W - 68, bottom - CAR_H - 70, 52, 70), 1.0)
        ol(T["phone"] + 0.25, (CAR_X0 + 14, bottom - CAR_H + 42, 40, 56), 1.0)
        # red trouble markers
        if T["quit"] <= t < T["quit"] + 1.3:
            fx.red_glow_rect(c, CAR_CX - 14, fy(3) + SLAB + 30, 28, bottom - CAR_H - (fy(3) + SLAB + 30), 1 - prog(t, T["quit"] + 1.0, T["quit"] + 1.3), t)
        if T["snap"] <= t < tl.s("fix2") + 0.4:
            fx.alert_badge(c, CAR_X0 + CAR_W + 70, bottom - CAR_H - 40, prog(t, T["snap"], T["snap"] + 0.25), 1.4, t)
        if "opens3" in T and T["opens3"] + 0.3 <= t < T["lock"] + 0.6:
            a = 1 - prog(t, T["lock"] + 0.3, T["lock"] + 0.6)
            fx.red_glow_rect(c, IW0 - 4, fy(5) - DOOR_H, IW1 - IW0 + 8, DOOR_H, a, t)
            fx.alert_badge(c, 60, fy(5) - 250, prog(t, T["opens3"] + 0.3, T["opens3"] + 0.55), 1.2, t)
        if T["cut"] <= t < T["batt"]:
            fx.alert_badge(c, CAR_X0 + CAR_W + 80, bottom - CAR_H - 30, prog(t, T["cut"] + 0.2, T["cut"] + 0.45), 1.2, t)
        if "touch" in T:
            k = bump(t, T["touch"] - 0.05, T["touch"] + 0.35)
            if k > 0:
                glow(c, -91, fy(1) - 134, 80, "#FDE047", 0.9 * k)
                circle(c, -91, fy(1) - 134, 10 * k, "#FFFFFF", k)
        # green checks
        for t0, where in self.checks():
            p = prog(t, t0, t0 + 0.35) * (1 - prog(t, t0 + 1.3, t0 + 1.6))
            if p <= 0:
                continue
            if where == "motor":
                fx.check_badge(c, -60, top - 260, p, 1.4)
            elif where == "car":
                fx.check_badge(c, CAR_X0 + CAR_W + 80, bottom - CAR_H - 20, p, 1.2)
            elif where == "door1":
                fx.check_badge(c, 60, fy(1) - 260, p, 1.1)
        # shaft outline on "one shaft"
        if T["one"] <= t < tl.s("closer"):
            a = 1 - prog(t, tl.s("closer") - 0.3, tl.s("closer"))
            fx.outline(c, BX0, top, IW1 - BX0, -top, prog(t, T["one"], T["one"] + 0.35), color="#FFD43B", r=40,
                       width=44, pad=40, a=a)

    # ------------------------------------------------------------ screen FX
    def draw_screen_fx(self, c, t, dusk):
        T, tl = self.T, self.tl
        fx.dim(c, W, H, self.dim.at(t))
        red = bump(t, T["quit"], T["quit"] + 0.9) * 0.8 + 1.4 * bump(t, T["snap"], T["snap"] + 1.4)
        if "opens3" in T:
            red += bump(t, T["opens3"] + 0.3, T["opens3"] + 1.4) * 0.8
        red += bump(t, T["cut"], T["cut"] + 1.2) * 0.6
        fx.red_vignette(c, W, H, clamp(red))
        fx.flash(c, W, H, 0.55 * bump(t, T["snap"], T["snap"] + 0.12))
        fx.flash(c, W, H, 0.35 * bump(t, T["bite"], T["bite"] + 0.1), "#FFE8A3")
        # soft vignette for polish
        p = skiaradial()
        c.drawRect(C_rect(0, 0, W, H), p)
        # fake pause + follow pill
        pz = prog(t, T["pause"], T["pause"] + 0.25) * (1 - prog(t, tl.s("cta") + 0.55, tl.s("cta") + 0.85))
        if pz > 0:
            fx.dim(c, W, H, 0.3 * pz)
            fx.pause_icon(c, W, H, pz, t)
        pill = prog(t, T["follow"] - 0.15, T["follow"] + 0.2) * (1 - prog(t, tl.e("cta") + 0.1, tl.e("cta") + 0.4))
        label, sub = TEXT[self.lang]["follow"]
        if self.lang.startswith("ar"):
            arabic.cta_pill_ar(c, W, label, sub, pill)
        else:
            fx.cta_pill(c, W, label, sub, pill)
        # stat badges
        bt = 1 - prog(t, tl.s("closer") - 0.1, tl.s("closer") + 0.3)
        rtl = self.lang.startswith("ar")
        xs = (W * 0.8, W * 0.5, W * 0.2) if rtl else (W * 0.2, W * 0.5, W * 0.8)  # reading order
        badge = arabic.stat_badge_ar if rtl else fx.stat_badge
        for (big, small), x, key, col in zip(TEXT[self.lang]["stat"], xs, ("one", "twenty", "zero"),
                                             ("#111827", "#111827", "#EF4444")):
            badge(c, x, 330, big, small, prog(t, T[key], T[key] + 0.3) * bt, color=col)
        # confetti at the final congrats
        fx.confetti(c, W, H, t, T["cong2"], 2.6)
        fx.confetti(c, W, H, t, T["cong"] + 0.05, 1.6, seed=8, n=40)

    # ------------------------------------------------------------- sound
    def sfx_events(self):
        T, tl = self.T, self.tl
        s, e = tl.s, tl.e
        ev = [(0.0, sfx.whoosh(0.5, True, 1), -10), (0.1, sfx.thud(), -4), (0.14, sfx.pop(100), -8),
              (T["rope"] - 0.25, sfx.click(31), -8), (T["rope"], sfx.whoosh(0.45, True, 30), -12)]
        ev += [(T["pull"], sfx.creak(max(0.5, T["cong"] - T["pull"])), -12), (T["cong"], sfx.pop(), -2),
               (T["cong"], sfx.sparkle(), -8)]
        ev += [(T["four"] + i * 0.08, sfx.pop(i), -8) for i in range(4)]
        ev += [(T["four"] + 0.5, sfx.creak(max(0.4, T["quit"] - T["four"] - 0.5), 3), -10),
               (T["quit"], sfx.whoosh(0.35, False, 2), -8), (T["quit"] + 0.3, sfx.thud(), -3),
               (T["quit"] + 0.35, sfx.buzz(), -6)]
        ev += [(s("fix1") + 0.15, sfx.whoosh(0.5, True, 3), -10), (T["motor"] - 0.1, sfx.thunk(), -6),
               (T["motor"] + 0.3, sfx.clank(300), -4), (T["pulley"] + 0.3, sfx.clank(520, 0.6, 4), -4),
               (T["cw"] + 0.45, sfx.thud(), -2), (T["cw"] + 0.45, sfx.clank(200, 0.5, 5), -8),
               (T["motor"] + 0.3, sfx.alarm(1, 600, 0.12, 0.05), -12),
               (T["barely"] - 0.4, sfx.hum(2.4), -10), (T["barely"] - 0.4, sfx.whirr(2.2), -14),
               (T["barely"] + 0.5, sfx.chime(), -6)]
        g0, gd = self.grow1
        ev += [(g0 + (i + 1) * gd - 0.03, sfx.thunk(10 + i), -12) for i in range(7)]
        ev += [(s("break2") + 0.25, sfx.whirr(max(1.0, T["snap"] - s("break2") - 0.3), 160, 300), -12),
               (T["snap"] - 1.1, sfx.riser(1.1), -14), (T["snap"], sfx.snap(), 0),
               (T["snap"] + 0.05, sfx.whoosh(0.5, False, 6), -6), (T["snap"] + 0.15, sfx.alarm(3), -8)]
        ev += [(T["rails"], sfx.whoosh(0.4, True, 7), -8), (T["rails"] + 0.4, sfx.clank(700, 0.4, 7), -8)]
        ev += [(T["cables"] + i * 0.1, sfx.click(20 + i), -6) for i in range(3)]
        ev += [(T["gov"] + 0.25, sfx.clank(900, 0.3, 8), -8), (T["gov"] + 0.25, sfx.tick(), -6),
               (T["falls"] - 0.05, sfx.whoosh(0.45, False, 9), -4), (T["bite"], sfx.clank(260, 0.9, 9), 0),
               (T["bite"], sfx.sizzle(), -4), (T["dead"] + 0.1, sfx.chime(), -6)]
        if "opens3" in T:
            ev += [(s("break3"), sfx.whoosh(0.8, False, 11), -12), (T["opens3"], sfx.hiss(), -6),
                   (T["opens3"] + 0.35, sfx.alarm(3, 1000), -8)]
            ev += [(T["lock"] + 0.05 * k, sfx.lock_click(30 + k), -10) for k in range(1, 9)]
            ev += [(T["lock"] + 0.35, sfx.hiss(0.4, 12), -8), (T["beam"], sfx.beep(1900), -8),
                   (T["beam"] + 0.14, sfx.beep(1900), -8), (T["edges"], sfx.hiss(0.5, 13), -8),
                   (T["touch"], sfx.beep(900, 0.12), -6), (T["touch"] + 0.05, sfx.hiss(0.35, 14), -8),
                   (e("fix3") - 0.25, sfx.chime(), -6)]
        ev += [(s("break4") + 0.1, sfx.whirr(max(1.0, T["cut"] - s("break4") - 0.2), 150, 240, 15), -12),
               (T["cut"], sfx.power_down(), -5)]
        ev += [(T["eleven"] + j * 0.06, sfx.pop(40 + j), -12) for j in range(7)]
        ev += [(T["batt"], sfx.charge_up(), -6), (T["batt"], sfx.click(50), -8), (T["phone"], sfx.ring(), -8),
               (T["crawls"], sfx.hum(max(1.0, T["opens4"] - T["crawls"]), 70), -12),
               (T["opens4"], sfx.hiss(0.5, 16), -6), (e("fix4") - 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(60), 0), (T["follow"] - 0.15, sfx.pop(61), -4)]
        ev += [(s("reveal") - 0.05, sfx.charge_up(0.5), -10), (T["hide"], sfx.whoosh(0.5, True, 17), -6),
               (T["shiny"], sfx.sparkle(0.6, 7, 18), -6), (T["buttons"] + 0.15, sfx.beep(1500), -4),
               (T["ding"], sfx.ding(), 0), (T["ding"] + 0.05, sfx.hiss(0.5, 19), -8)]
        ev += [(s("stat") - 0.05, sfx.whoosh(1.0, True, 21), -6)]
        st0, sd = self.grow2
        ev += [(st0 + (i + 1) * sd - 0.02, sfx.thunk(70 + i), -16) for i in range(10)]
        ev += [(T["one"], sfx.pop(80), -3), (T["twenty"], sfx.pop(81), -3), (T["zero"], sfx.pop(82), -3)]
        ev += [(T["cong2"], sfx.pop(90), -2), (T["cong2"], sfx.sparkle(1.0, 14, 91), -4),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.22, sfx.whoosh(0.45, False, 95), -6)]
        ev += [(tt, sfx.tap(i), -6 + (2 if i == 9 else 0)) for i, tt in enumerate(self.taps)]
        ev += [(T["flip"], sfx.beep(520, 0.07), -8), (T["flip"] + 0.12, sfx.womp(), -2)]
        return ev


# ---------------------------------------------------------------- small utils
import skia  # noqa: E402


def C_rect(x, y, w, h):
    return skia.Rect.MakeXYWH(x, y, w, h)


def arc_rope(c, cx, cy, r, color, width):
    c.drawArc(C_rect(cx - r, cy - r, 2 * r, 2 * r), 180, 180, False, P(color, 1, stroke=width))


def w_or(T, key, default):
    return T.get(key, default)


_VIG = None


def skiaradial():
    global _VIG
    if _VIG is None:
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.45), H * 0.78,
                                                   [C("#000000", 0), C("#000000", 0), C("#000000", 0.22)],
                                                   [0.0, 0.6, 1.0]))
        _VIG = p
    return _VIG


NAME = "elevator"
EPISODE = Elevator
