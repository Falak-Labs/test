"""Episode 2: The Skyscraper.  Build -> break -> fix, four times, keyed to the voiceover words.

World units: ground at y=0, up is negative. 100 floors of FH=110, tower x from -560 to 560:
stairwell | express shaft | local shaft | two apartments. Overlays (labels, badges, outlines) are drawn in
screen space through self.sc(), so they keep their size at every zoom (0.14 wide shots .. 2.3 close-ups).
"""
import math
import os
import random
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)

from bik.core import Timeline, Camera, Track, clamp, lerp, prog, e_io, e_out, e_in, e_back, bump  # noqa: E402
from bik.draw import text, text_width, rect, grad_rect, glow, circle, poly, line, mix, shade, C, P  # noqa: E402
from bik import world, fx, sfx, arabic  # noqa: E402
from bik.captions import Captions, word_timings  # noqa: E402
import skia  # noqa: E402

W, H = 1080, 1920
LABELS = ["hook", "break1", "fix1", "break2", "fix2", "break3", "fix3", "break4", "fix4", "cta", "reveal", "stat",
          "closer", "tag"]
EMPH = ["CONGRATS", "STAIRS", "EXPRESS", "SEASICK", "JUMBO", "SHAKING", "BEDROCK", "FIRE", "SAFELY", "FOLLOW",
        "LIGHTS", "THOUSAND", "YOURSELF", "FOURTEEN"]

# ---- Saudi version (lang="ar_sa"): English anchor word -> the Saudi word that carries the same moment
EMPH_SA = ["مبروك", "رجوله", "سريعة", "تدوخ", "جامبو", "تهتز", "الصخر", "حريق", "آمنة", "تابعني", "الأنوار",
           "آلاف", "بيدك", "أربعطعش"]
AR_KEYS_SA = {
    ("hook", "STACK"): "كدست", ("hook", "HUNDRED"): "مية", ("hook", "CONGRATS"): "مبروك",
    ("break1", "LIVES"): "ساكن", ("break1", "NINETY"): "تسعة", ("break1", "CLIMB"): "يطلع", ("break1", "STAIRS"): "رجوله",
    ("fix1", "EXPRESS"): "مصاعد", ("fix1", "SHOOT"): "تطير", ("fix1", "LOBBIES"): "للوبي", ("fix1", "LOCAL"): "ثانية",
    ("fix1", "TRAIN"): "القطار", ("fix1", "BUS"): "الباص",
    ("break2", "HOME"): "بيته", ("break2", "STORM"): "عاصفة", ("break2", "SWAYS"): "ويتمايل", ("break2", "SEASICK"): "تدوخ",
    ("fix2", "BALL"): "كورة", ("fix2", "JUMBO"): "جامبو", ("fix2", "CABLES"): "كيابل", ("fix2", "PISTONS"): "ومساعدات",
    ("fix2", "LEANS"): "مال", ("fix2", "SWINGS"): "مالت",
    ("break3", "EARTHQUAKE"): "زلزال", ("break3", "SHAKING"): "تهتز",
    ("fix3", "FRAME"): "هيكل", ("fix3", "BENDS"): "ينثني", ("fix3", "SNAPPING"): "ينكسر", ("fix3", "SHOCK"): "مساعدات",
    ("fix3", "FOUNDATIONS"): "الأساسات", ("fix3", "BEDROCK"): "الصخر",
    ("break4", "ANYTHING"): "تقريبا", ("break4", "FIRE"): "حريق", ("break4", "EIGHTY"): "الثمانين",
    ("fix4", "SPRINKLERS"): "رشاشات", ("fix4", "EVERYWHERE"): "مكان", ("fix4", "STAIRWELLS"): "ومراوح",
    ("fix4", "FANS"): "تدف", ("fix4", "SMOKE"): "الدخان", ("fix4", "REFUGE"): "آمنة", ("fix4", "SAFELY"): "الناس",
    ("cta", "FOLLOW"): "تابعني",
    ("reveal", "WRAP"): "لفه", ("reveal", "GLASS"): "بالزجاج", ("reveal", "LIGHTS"): "الأنوار",
    ("stat", "ONE"): "أرض", ("stat", "HUNDRED"): "مية", ("stat", "TEN"): "وعشرة",
    ("closer", "CONGRATS"): "مبروك",
    ("tag", "THIRTEENTH"): "ثلطعش", ("tag", "STILL"): "موجود", ("tag", "FOURTEEN"): "أربعطعش",
}
KEYS_BY_LANG = {"ar_sa": AR_KEYS_SA}
EMPH_BY_LANG = {"en": EMPH, "ar_sa": EMPH_SA}
TEXT = {
    "en": {"follow": ("FOLLOW", "next: a pool that disappears"),
           "stat": [("1", "BLOCK"), ("100", "FLOORS"), ("10K", "PEOPLE")],
           "floor": "FLOOR", "sky": "SKY LOBBY", "express": "EXPRESS", "local": "LOCAL", "refuge": "REFUGE FLOOR",
           "bedrock": "BEDROCK", "fans": "FRESH AIR", "ton": "t"},
    "ar_sa": {"follow": ("تابعني", "الجاي: مسبح يختفي"),
              "stat": [("1", "أرض"), ("100", "دور"), ("10", "آلاف شخص")],
              "floor": "الدور", "sky": "لوبي فوق", "express": "سريع", "local": "يكمّل", "refuge": "دور آمن",
              "bedrock": "الصخر", "fans": "هوا نظيف", "ton": "طن"},
}

NF, FH, SLAB = 100, 110, 8
TX0, TX1, WALLW = -560, 560, 14
ST0, ST1 = -560, -440          # stairwell
EX0, EX1 = -440, -340          # express shaft
LX0, LX1 = -340, -240          # local shaft
AX0, AX1 = -240, 560           # apartments
PART = 160                     # wall between the two apartments of a floor
SKY_LOBBY, REFUGE, FIRE_F, F13 = 50, 75, 80, 13
DAMP_LO, DAMP_HI = 89, 95
BALL_X, BALL_R, CABLE_L = 160, 140, 300
SPIRE_H, CROWN_H = 520, 180
PILE_D, ROCK_Y0, ROCK_Y1 = 2800, 2700, 4300
PILE_XS = (-480, -320, -160, 0, 160, 320, 480)
COLS = (TX0, ST1, LX1, PART, TX1)
CAR_W, CAR_H = 72, 84

WALLS = ["#FBE3C8", "#DDEBDD", "#E3E0F5", "#FCE6EA", "#DCEBF7", "#F6F0D6", "#E8F4F1", "#FDE9D9"]
FACADE, FACADE_DK = "#E9E3D7", "#C9C0B0"
CONCRETE = "#9AA3AD"
CORE, CORE_HI = "#2B3240", "#353D4D"
STAIR_BG, STAIR = "#D5DBE3", "#7B8794"
STEEL, STEEL_DK, STEEL_LT = "#94A3B8", "#475569", "#E2E8F0"
GOLD, GOLD_DK, GOLD_LT = "#F2B632", "#B7791F", "#FDE68A"
GREEN, RED, YELLOW = "#22C55E", "#EF4444", "#FACC15"


def fy(k):
    """Floor surface y of floor k (floor 1 = ground)."""
    return -(k - 1) * FH


def lin(x):
    return x


class Skyscraper:
    def __init__(self, vo_json, vo_wav, lang="en"):
        self.lang = lang
        self.tx = TEXT.get(lang, TEXT["en"])
        self.tl = tl = Timeline(vo_json, LABELS, lead=0.5, pause=0.6, tail=2.0)
        self.words = word_timings(vo_wav, tl)
        self.cap = Captions(self.words, EMPH_BY_LANG.get(lang, EMPH), hide=[(tl.pause_start, tl.s("cta"))])
        self.duration = tl.duration
        self._tracks()
        self._people()
        self.cam_state = (0.0, 0.0, 1.0)

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
        s, e = tl.s, tl.e
        T = self.T = {}
        T["stack"] = w("hook", "STACK", 0.08)
        T["hundred"] = w("hook", "HUNDRED", 0.15)
        T["cong"] = w("hook", "CONGRATS", 0.6)
        T["lives"] = w("break1", "LIVES", 0.2)
        T["n99"] = w("break1", "NINETY", 0.3)
        T["climb"] = w("break1", "CLIMB", 0.6)
        T["stairs"] = w("break1", "STAIRS", 0.95)
        T["express"] = w("fix1", "EXPRESS", 0.1)
        T["shoot"] = w("fix1", "SHOOT", 0.3)
        T["lobby"] = w("fix1", "LOBBIES", 0.45)
        T["local"] = w("fix1", "LOCAL", 0.55)
        T["train"] = w("fix1", "TRAIN", 0.8)
        T["bus"] = w("fix1", "BUS", 0.95)
        T["home"] = w("break2", "HOME", 0.2)
        T["storm"] = w("break2", "STORM", 0.45)
        T["sways"] = w("break2", "SWAYS", 0.7)
        T["seasick"] = w("break2", "SEASICK", 0.95)
        T["ball"] = w("fix2", "BALL", 0.15)
        T["jumbo"] = w("fix2", "JUMBO", 0.3)
        T["cables"] = w("fix2", "CABLES", 0.5)
        T["pistons"] = w("fix2", "PISTONS", 0.6)
        T["leans"] = w("fix2", "LEANS", 0.8)
        T["swings"] = w("fix2", "SWINGS", 0.92)
        T["quake"] = w("break3", "EARTHQUAKE", 0.3)
        T["shaking"] = w("break3", "SHAKING", 0.9)
        T["frame"] = w("fix3", "FRAME", 0.15)
        T["bends"] = w("fix3", "BENDS", 0.22)
        T["snapping"] = w("fix3", "SNAPPING", 0.35)
        T["absorbers"] = w("fix3", "SHOCK", 0.5)
        T["found"] = w("fix3", "FOUNDATIONS", 0.8)
        T["bedrock"] = w("fix3", "BEDROCK", 0.95)
        T["anything"] = w("break4", "ANYTHING", 0.35)
        T["fire"] = w("break4", "FIRE", 0.6)
        T["eighty"] = w("break4", "EIGHTY", 0.95)
        T["sprinklers"] = w("fix4", "SPRINKLERS", 0.08)
        T["everywhere"] = w("fix4", "EVERYWHERE", 0.18)
        T["stairwells"] = w("fix4", "STAIRWELLS", 0.28)
        T["fans"] = w("fix4", "FANS", 0.4)
        T["smoke"] = w("fix4", "SMOKE", 0.6)
        T["refuge"] = w("fix4", "REFUGE", 0.75)
        T["safely"] = w("fix4", "SAFELY", 0.95)
        T["pause"] = tl.pause_start
        T["follow"] = w("cta", "FOLLOW", 0.4)
        T["wrap"] = w("reveal", "WRAP", 0.15)
        T["glass"] = w("reveal", "GLASS", 0.5)
        T["lights"] = w("reveal", "LIGHTS", 0.95)
        T["one"] = w("stat", "ONE", 0.05)
        T["hundred2"] = w("stat", "HUNDRED", 0.45)
        T["ten"] = w("stat", "TEN", 0.75)
        T["cong2"] = w("closer", "CONGRATS", 0.1)
        T["thirteen"] = w("tag", "THIRTEENTH", 0.25)
        T["still"] = w("tag", "STILL", 0.5)
        T["fourteen"] = w("tag", "FOURTEEN", 0.92)
        T["slap"] = T["fourteen"] + 0.06
        T["womp"] = T["fourteen"] + 0.5

        # --- the stack: floors drop in, slowly first, then a rush to 100
        nf = self.nf = Track(1.0)  # floor 1 stands in frame one
        nf.to(0.0, 2.0, 0.4, e_out)
        nf.to(0.45, 10.0, max(0.5, T["hundred"] + 0.3 - 0.45), lin)
        t_rush = max(0.95, T["hundred"] + 0.32)
        nf.to(t_rush, 100.0, max(0.8, T["cong"] - 0.05 - t_rush), e_in)
        self.tk = {}
        k, t = 1, 0.0
        while k <= NF and t < 12:
            v = nf.at(t)
            while k <= NF and v >= k - 1e-6:
                self.tk[k] = t
                k += 1
            t += 1 / 240
        for kk in range(k, NF + 1):
            self.tk[kk] = T["cong"]
        self.t_top = self.tk[NF]

        # --- elevators
        self.car_a = Track(0.0).to(T["express"] - 0.15, 1.0, 0.35, e_out)
        self.fe = Track(1.0).to(T["shoot"] - 0.08, float(SKY_LOBBY), 0.75, e_io)
        self.fe.to(T["home"] - 0.2, 1.0, 1.6, e_io).to(T["sways"], 30.0, 1.4, e_io)
        self.fl = Track(float(SKY_LOBBY)).to(T["local"] + 0.4, 99.0, max(0.9, T["train"] - 0.15 - T["local"] - 0.4), e_io)
        self.fl.to(T["home"] - 0.4, 72.0, 0.9, e_io).to(T["home"] + 0.6, 96.0, 1.0, e_io)

        # --- storm and sway
        self.storm = Track(0.0).to(T["storm"] - 0.1, 1.0, 0.45).to(e("fix2") - 1.0, 0.0, 1.4)
        self.sway = Track(0.0).to(T["storm"] - 0.05, 40.0, 0.5).to(T["sways"] - 0.2, 120.0, 0.6)
        self.sway.to(T["ball"] + 0.2, 60.0, 1.0).to(T["leans"] - 0.45, 0.0, 0.5)
        self.lean = Track(0.0).to(T["leans"] - 0.4, 1.0, 0.55).to(T["swings"] - 0.05, 0.0, 0.9)
        self.swing = Track(0.0).to(T["swings"] - 0.3, 1.0, 0.45).to(e("fix2") + 0.1, 0.0, 1.0)
        self.damp_a = Track(0.0).to(T["ball"] - 0.35, 1.0, 0.35)
        self.sick = Track(0.0).to(T["seasick"] - 0.35, 1.0, 0.35).to(T["swings"] + 0.3, 0.0, 0.6)

        # --- earthquake, frame, absorbers, piles
        self.quake = Track(0.0).to(T["quake"] - 0.05, 1.0, 0.25).to(T["shaking"] - 0.1, 1.35, 0.4)
        self.quake.to(T["frame"], 0.55, 0.6).to(T["absorbers"] + 0.2, 0.0, 0.8)
        self.frame = Track(0.0).to(T["frame"] - 0.3, 1.0, 0.45).to(s("break4") - 0.1, 0.0, 0.6)
        self.bend = Track(0.0).to(T["bends"] - 0.25, 1.0, 0.4).to(T["snapping"] + 0.4, 0.45, 0.6)
        self.bend.to(T["absorbers"] + 0.4, 0.0, 0.6)
        self.pile = Track(0.0).to(T["found"] - 0.05, 1.0, max(0.6, T["bedrock"] + 0.15 - T["found"]), e_io)

        # --- fire
        self.fire = Track(0.0).to(T["fire"] - 0.15, 1.0, 0.7).to(T["sprinklers"] + 0.35, 0.55, 0.5)
        self.fire.to(T["everywhere"] + 0.4, 0.0, 0.8)
        self.smoke = Track(0.0).to(T["fire"], 1.0, 1.1).to(T["smoke"] + 0.2, 0.65, 0.6).to(T["refuge"] + 0.5, 0.0, 1.2)
        self.air = Track(0.0).to(T["fans"] - 0.15, 1.0, 0.4).to(e("fix4") + 0.1, 0.0, 0.5)

        # --- reveal and night
        self.glass_n = Track(0.0).to(T["wrap"] - 0.05, float(NF + 3), max(0.7, T["lights"] - 0.2 - T["wrap"]), e_io)
        self.glass_a = Track(1.0).to(s("tag") - 0.3, 0.06, 0.35)
        self.dusk = Track(0.0).to(T["lights"] - 0.5, 0.92, 0.9)
        self.wlit = Track(0.0).to(T["lights"] - 0.05, 1.0, 0.4)

        # --- camera: the hook follows the stack, then keyed shots
        self.hook_end = self.t_top + 0.35
        cam = self.cam = Camera(*self.hook_cam(self.hook_end))
        cam.key(self.hook_end, *self.hook_cam(self.hook_end), 0.01)
        cam.key(s("break1") - 0.15, 60, -5600, 0.142, 0.5)
        cam.key(T["climb"] - 0.4, -480, -130, 1.5, 0.6)
        cam.key(T["climb"] + 0.25, -480, -430, 1.5, max(0.6, T["stairs"] + 0.45 - T["climb"] - 0.25))
        cam.key(s("fix1") - 0.1, -330, -160, 0.8, 0.6)
        cam.key(T["shoot"] - 0.08, -330, fy(SKY_LOBBY) + 25, 0.8, 0.75)
        cam.key(T["local"] + 0.55, -260, -5450, 0.142, 0.75)
        cam.key(s("break2") - 0.1, 100, -9500, 0.33, 1.0)
        cam.key(T["sways"] + 0.05, 120, fy(95) - 70, 0.62, 0.6)
        cam.key(T["seasick"] - 0.45, 250, fy(97) - 55, 1.25, 0.45)
        cam.key(s("fix2") - 0.05, 140, fy(92) - 30, 0.62, 0.6)
        cam.key(T["leans"] - 0.5, 60, fy(88) - 60, 0.42, 0.6)
        cam.key(s("break3") - 0.15, 0, -5300, 0.142, 0.8)
        cam.key(T["absorbers"] - 0.35, 0, -3900, 0.2, 0.6)
        cam.key(T["found"] - 0.4, 0, 1900, 0.3, 0.7)
        cam.key(s("break4") - 0.1, 0, -5300, 0.142, 0.8)
        cam.key(T["fire"] - 0.35, 200, fy(FIRE_F) - 55, 1.5, 0.6)
        cam.key(T["stairwells"] - 0.35, -380, fy(FIRE_F) - 55, 1.4, 0.6)
        cam.key(T["refuge"] - 0.4, 60, fy(REFUGE) - 55, 1.1, 0.7)
        cam.key(s("cta") + 0.2, 0, -5300, 0.138, 3.0)
        cam.key(s("closer") - 0.1, 0, -5450, 0.15, 2.6)
        cam.key(s("tag") - 0.22, -110, fy(F13) - 58, 2.2, 0.5)

        self.shakes = [(self.t_top, 0.3, 10), (T["quake"], 1.3, 20), (T["shaking"] - 0.1, 1.3, 28),
                       (T["slap"], 0.2, 8)]

    def hook_cam(self, t):
        n = self.nf.at(t)
        sp = e_out(prog(t, self.t_top, self.t_top + 0.35))
        need = max(1300.0, n * FH + (SPIRE_H + CROWN_H) * sp + 700)
        z = clamp(1920 * 0.80 / need, 0.138, 0.86)
        gy = lerp(1660, 1480, (z - 0.138) / (0.86 - 0.138))
        return 0.0, -(gy - 960) / z, z

    def cam_at(self, t):
        if t < self.hook_end:
            return self.hook_cam(t)
        return self.cam.at(t)

    def _people(self):
        self.ppl = {}
        for k in range(1, NF + 1):
            rng = random.Random(k * 7 + 3)
            n = rng.choice((0, 1, 1, 2))
            out = []
            for i in range(n):
                x = rng.uniform(AX0 + 50, PART - 40) if i == 0 else rng.uniform(PART + 50, AX1 - 70)
                out.append((x, rng.randint(0, 40)))
            self.ppl[k] = out

    # ------------------------------------------------------------------ motion helpers
    def dx(self, k, t):
        """Sideways offset of floor k: storm sway, the scripted lean, earthquake, frame bending."""
        u = clamp(k / NF, 0.0, 1.1)
        v = 0.0
        a = self.sway.at(t)
        if a > 0:
            v += a * math.sin(2 * math.pi * (t - self.T["storm"]) / 1.5) * u * u
        ln = self.lean.at(t)
        if ln > 0:
            v -= 140 * ln * u * u
        q = self.quake.at(t)
        if q > 0:
            g = 70 * q * math.sin(2 * math.pi * 4.3 * t)
            v += g * (1 - 0.5 * u) + 160 * q * math.sin(2 * math.pi * 1.3 * t + 0.7) * u ** 1.5
        b = self.bend.at(t)
        if b > 0:
            v += 320 * b * math.sin(2 * math.pi * 0.85 * (t - self.T["bends"])) * u * u
        return v

    def gx(self, t):
        q = self.quake.at(t)
        return 70 * q * math.sin(2 * math.pi * 4.3 * t) if q > 0 else 0.0

    def climber(self, t):
        """Stairwell climber in break1: (x, feet y, floor progress, facing)."""
        T = self.T
        p = 1.0 + 2.4 * clamp(t - (T["climb"] - 0.15), 0.0, T["stairs"] + 0.3 - (T["climb"] - 0.15))
        f = int(p)
        r = p - f
        xl, xr = ST0 + WALLW + 18, ST1 - 18
        yb = fy(f) - SLAB
        ym = yb - (FH - SLAB) / 2
        if r < 0.5:
            u = r / 0.5
            return lerp(xl, xr, u), lerp(yb, ym, u), p, 1
        u = (r - 0.5) / 0.5
        return lerp(xr, xl, u), lerp(ym, fy(f + 1) - SLAB, u), p, -1

    def ball_angle(self, t):
        return 0.42 * self.swing.at(t) - 0.12 * self.sway.at(t) / 120 * math.sin(2 * math.pi * (t - self.T["storm"]) / 1.5)

    # ------------------------------------------------------------------ screen helpers
    def sc(self, x, y):
        cx, cy, z = self.cam_state
        return (x - cx) * z + W / 2, (y - cy) * z + H / 2

    def sc_rect(self, x, y, w, h):
        x0, y0 = self.sc(x, y)
        x1, y1 = self.sc(x + w, y + h)
        return x0, y0, x1 - x0, y1 - y0

    def pill(self, c, s, x, y, p, fg="#111827", bg="#FFFFFF", size=38):
        """Screen-space label. s: a string, or a list of parts in reading order (\"FLOOR\", \"99\"); Arabic parts are
        shaped with HarfBuzz, digits stay in Poppins, and an Arabic label is laid out right to left."""
        if p <= 0 or not s:
            return
        parts = [s] if isinstance(s, str) else list(s)
        if self.lang.startswith("ar") and len(parts) > 1:
            parts = parts[::-1]
        ws = [arabic.width_ar(q, size * 1.05) if arabic.is_ar(q) else text_width(q, size, "Poppins-Black")
              for q in parts]
        gap = size * 0.3
        tw = sum(ws) + gap * (len(parts) - 1)
        k = e_back(clamp(p))
        w, h = tw + 44, size * 1.55
        c.save()
        c.translate(x, y)
        c.scale(k, k)
        rect(c, -w / 2, -h / 2 + 6, w, h, "#000000", 0.3, r=h / 2, blur=8)
        rect(c, -w / 2, -h / 2, w, h, bg, 1.0, r=h / 2)
        xx = -tw / 2
        for q, wq in zip(parts, ws):
            if arabic.is_ar(q):
                arabic.text_ar(c, q, xx, size * 0.36, size * 1.05, fg, align="left")
            else:
                text(c, q, xx, size * 0.36, size, fg, "Poppins-Black", align="left")
            xx += wq + gap
        c.restore()

    # ------------------------------------------------------------------ frame
    def draw(self, c, t):
        T, tl = self.T, self.tl
        real_t = t
        if tl.pause_start <= t < tl.s("cta"):
            t = tl.pause_start  # the fake pause freezes the picture
        dusk = self.dusk.at(t)
        world.sky(c, W, H, dusk, t)
        cx, cy, z = self.cam_at(t)
        for t0, d, amp in self.shakes:
            if t0 <= t < t0 + d:
                k = (1 - (t - t0) / d) * amp
                cx += math.sin(t * 91) * k / z
                cy += math.cos(t * 77) * k / z
        self.cam_state = (cx, cy, z)
        storm = self.storm.at(t)
        if storm > 0:
            self.draw_storm_sky(c, t, storm)
        ground_sy = (0 - cy) * z + H / 2
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
        gx = self.gx(t)
        c.save()
        c.translate(gx, 0)
        self.draw_neighbors(c, t, dusk)
        world.ground(c, -14000, 14000, 9000, dusk)
        self.draw_underground(c, t)
        self.draw_cracks(c, t)
        c.restore()
        self.draw_tower(c, t, dusk, z, cy)
        c.restore()
        # screen overlays
        self.draw_screen_fx(c, real_t, t, dusk)
        self.cap.draw(c, W, real_t)

    # -------------------------------------------------------------- storm sky
    def draw_storm_sky(self, c, t, a):
        fx.dim(c, W, H, 0.45 * a, "#1E2533")
        rng = random.Random(4)
        for i in range(7):
            x = (rng.uniform(-200, W + 200) + t * 30 * (1 + i % 3)) % (W + 400) - 200
            y = rng.uniform(60, 520)
            world.cloud(c, x, y, rng.uniform(1.4, 2.4), a * 0.85, "#4B5563")

    # -------------------------------------------------------------- neighbors
    def draw_neighbors(self, c, t, dusk):
        lit = clamp((dusk - 0.35) / 0.4)
        for i, (x0, x1, h, col) in enumerate(((-3300, -2650, 1500, "#C7D2DE"), (-2550, -1850, 2700, "#B9C6D4"),
                                              (-1750, -1000, 950, "#D6CFC2"), (1000, 1650, 1250, "#CFC6B8"),
                                              (1750, 2550, 3100, "#B8C4D2"), (2650, 3300, 1800, "#C9D3DE"))):
            colr = mix(col, "#3B3F5C", dusk * 0.85)
            rect(c, x0, -h, x1 - x0, h, colr)
            rect(c, x0, -h, x1 - x0, 26, shade(colr, -0.15))
            rr = random.Random(i * 13 + 1)
            for wy in range(int(-h + 70), -60, 120):
                for wx in range(int(x0) + 50, int(x1) - 70, 110):
                    on = rr.random() < 0.45
                    wc = mix("#E8F1F8", "#2C3150", dusk * 0.9)
                    rect(c, wx, wy, 60, 70, wc, 0.9)
                    if on and lit > 0:
                        rect(c, wx, wy, 60, 70, "#FFE29A", 0.85 * lit)

    # -------------------------------------------------------------- below ground
    def draw_underground(self, c, t):
        T = self.T
        # bedrock band
        grad_rect(c, -14000, ROCK_Y0, 28000, ROCK_Y1 - ROCK_Y0, "#5B5F66", "#3C3F45")
        rng = random.Random(21)
        for _ in range(140):
            x = rng.uniform(-6000, 6000)
            y = rng.uniform(ROCK_Y0 + 60, ROCK_Y1 - 60)
            r = rng.uniform(40, 130)
            poly(c, [(x - r, y), (x - r * 0.3, y - r * 0.7), (x + r * 0.8, y - r * 0.4), (x + r, y + r * 0.3),
                     (x, y + r * 0.6)], "#6B7078", 0.55)
        line(c, -14000, ROCK_Y0, 14000, ROCK_Y0, "#2F3237", 14)
        # footing + piles
        rect(c, TX0 - 60, -2, TX1 - TX0 + 120, 70, CONCRETE)
        rect(c, TX0 - 60, -2, TX1 - TX0 + 120, 14, "#B8C0C8")
        d = PILE_D * self.pile.at(t)
        if d > 1:
            for x in PILE_XS:
                rect(c, x - 26, 60, 52, d, "#7A828C")
                rect(c, x - 26, 60, 14, d, "#9AA3AD")
                poly(c, [(x - 26, 60 + d), (x + 26, 60 + d), (x, 60 + d + 50)], "#7A828C")
            if self.pile.at(t) < 1:
                for x in PILE_XS:  # driving dust
                    glow(c, x, 60 + d + 30, 90, "#D6C3A5", 0.5)

    def draw_cracks(self, c, t):
        T = self.T
        a = prog(t, T["shaking"] - 0.15, T["shaking"] + 0.25) * (1 - prog(t, T["found"] - 0.6, T["found"] - 0.2))
        if a <= 0:
            return
        rng = random.Random(5)
        for side in (-1, 1):
            for j in range(3):
                x = side * (TX1 + 300 + j * 650 + rng.uniform(0, 200))
                pts = [(x, -2)]
                for i in range(6):
                    px, py = pts[-1]
                    pts.append((px + rng.uniform(-60, 60), py + rng.uniform(60, 130)))
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                    line(c, x0, y0, x1, y1, "#2A1B10", 22 * a, a)

    # -------------------------------------------------------------- the tower
    def visible_floors(self, cy, z):
        y0, y1 = cy - H / 2 / z - FH * 3, cy + H / 2 / z + FH * 3
        k_hi = int(clamp(-y0 / FH + 2, 1, NF))
        k_lo = int(clamp(-y1 / FH, 1, NF))
        return k_lo, k_hi

    def draw_tower(self, c, t, dusk, z, cy):
        T = self.T
        k_lo, k_hi = self.visible_floors(cy, z)
        gn = self.glass_n.at(t)
        ga = self.glass_a.at(t)
        fv = self.frame.at(t)
        lights = 1.0
        shown = []
        for k in range(k_lo, k_hi + 1):
            tk = self.tk[k]
            if t < tk - 0.14:
                continue
            drop = (1 - e_out(prog(t, tk - 0.14, tk))) * FH * 2
            a = prog(t, tk - 0.14, tk - 0.08)
            c.save()
            c.translate(self.dx(k, t), -drop)
            self.draw_floor(c, t, k, z, dusk, lights, a)
            if fv > 0:
                rect(c, TX0, fy(k) - FH, TX1 - TX0, FH, "#0F172A", 0.72 * fv)
            c.restore()
            shown.append(k)
        self.draw_cars(c, t, z)
        if self.damp_a.at(t) > 0:
            self.draw_damper(c, t, z)
        if fv > 0:
            self.draw_frame(c, t, fv)
        if T["climb"] - 0.6 <= t < T["express"] + 0.2:
            x, y, p, face = self.climber(t)
            k = int(p)
            c.save()
            c.translate(self.dx(k, t), 0)
            c.translate(x, y)
            c.scale(face, 1)
            tired = prog(t, T["stairs"] - 0.3, T["stairs"] + 0.2)
            walk = 0.0 if t > T["stairs"] + 0.3 else (t * 3.2)
            world.person(c, 0, 0, 74, shirt="#F97316", walk=walk, sweat=tired * (t * 3 % 1 + 0.2),
                         lean=0.35 * tired, a=prog(t, T["climb"] - 0.6, T["climb"] - 0.4))
            c.restore()
        if gn > 0 and ga > 0:
            for k in shown:
                if k <= gn + 1:
                    c.save()
                    c.translate(self.dx(k, t), 0)
                    self.draw_glass(c, t, k, clamp(gn - k + 1), ga, dusk)
                    c.restore()
        if t >= self.t_top - 0.05:
            self.draw_crown(c, t, dusk, ga * clamp(gn - NF))
        fo = prog(t, self.tl.s("tag") - 0.1, self.tl.s("tag") + 0.3)
        if fo > 0:
            d13 = self.dx(F13, t)
            rect(c, TX0 - 4000 + d13, fy(NF + 8), TX1 - TX0 + 8000, fy(F13 + 1) - fy(NF + 8), "#0B1020", 0.5 * fo)
            rect(c, TX0 - 4000 + d13, fy(F13), TX1 - TX0 + 8000, 6000, "#0B1020", 0.5 * fo)

    def draw_floor(self, c, t, k, z, dusk, lights, a):
        T = self.T
        yb, yt = fy(k), fy(k) - FH
        ih = FH - SLAB
        rect(c, TX0, yt, TX1 - TX0, FH, FACADE, a)
        # stairwell
        rect(c, ST0 + WALLW, yt, ST1 - ST0 - WALLW, ih, STAIR_BG, a)
        if z > 0.22:
            xl, xr = ST0 + WALLW + 10, ST1 - 10
            ym = yb - SLAB - ih / 2
            line(c, xl, yb - SLAB, xr, ym, STAIR, 7, a)
            line(c, xr, ym, xl, yt, STAIR, 7, a)
            rect(c, xr - 20, ym - 2, 26, 6, STAIR, a)
            if z > 0.7:  # stair door
                rect(c, ST1 - 8, yb - SLAB - 70, 8, 70, "#8B5E34", a)
        # shafts
        rect(c, EX0, yt, EX1 - EX0, FH, CORE, a)
        rect(c, LX0, yt, LX1 - LX0, FH, CORE_HI, a)
        if z > 0.3:
            line(c, EX0 + 14, yt, EX0 + 14, yb, "#4B5563", 4, a)
            line(c, LX1 - 14, yt, LX1 - 14, yb, "#4B5563", 4, a)
        # apartments
        c1, c2 = WALLS[(k * 3) % len(WALLS)], WALLS[(k * 3 + 1) % len(WALLS)]
        damper_zone = DAMP_LO <= k <= DAMP_HI and self.damp_a.at(t) > 0.99
        if not damper_zone:
            if dusk > 0.2:
                c1, c2 = mix(c1, "#3D3A55", dusk * 0.55), mix(c2, "#3D3A55", dusk * 0.55)
            rect(c, AX0, yt, PART - AX0, ih, c1, a)
            rect(c, PART, yt, AX1 - WALLW - PART, ih, c2, a)
            if z >= 0.5:
                s = ih / 244.0
                for (x0, x1, seed) in ((AX0 + 8, PART - 6, k * 2), (PART + 8, AX1 - WALLW - 6, k * 2 + 1)):
                    c.save()
                    c.translate(x0, yt)
                    c.scale(s, s)
                    world.room_decor(c, 0, 0, (x1 - x0) / s, 244, seed, lights, dusk)
                    c.restore()
            else:
                for x0 in (AX0 + 70, PART + 120):
                    rect(c, x0, yt + 22, 150, 46, mix("#DDEFFC", "#FFE29A", dusk), 0.85 * a, r=4)
            rect(c, PART - 5, yt, 10, ih, FACADE_DK, a)
            if z >= 0.5:
                self.draw_people(c, t, k, z)
            if k == SKY_LOBBY and t >= T["lobby"] - 0.2:
                gl = prog(t, T["lobby"] - 0.2, T["lobby"] + 0.2)
                rect(c, EX0, yt, AX1 - WALLW - EX0, ih, GOLD_LT, 0.55 * gl * a)
            if k == REFUGE:
                ra = prog(t, T["refuge"] - 0.1, T["refuge"] + 0.3) * (1 - prog(t, self.tl.s("cta") + 0.4, self.tl.s("cta") + 0.8))
                if ra > 0:
                    rect(c, AX0, yt, AX1 - WALLW - AX0, ih, GREEN, 0.3 * ra)
                    rect(c, AX0 + 4, yt + 4, AX1 - WALLW - AX0 - 8, ih - 8, GREEN, ra, r=6, stroke=7)
            if k == FIRE_F:
                self.draw_fire_floor(c, t, yt, yb, z)
            if k == F13 and t >= self.tl.s("tag") - 0.6:
                self.draw_plate(c, t, yt)
        # highlights: floor 99 in break1, stat sweep
        if k == 99 and T["lives"] - 0.2 <= t < T["climb"] - 0.3:
            p = bump(t, T["lives"] - 0.2, T["climb"] - 0.3) * (0.6 + 0.4 * math.sin(t * 12))
            rect(c, TX0, yt, TX1 - TX0, ih, YELLOW, 0.75 * p)
        sw = (t - T["hundred2"] + 0.1) / 0.8 * NF
        if 0 < sw < NF + 6 and abs(k - sw) < 4:
            rect(c, TX0, yt, TX1 - TX0, FH, "#FFFFFF", 0.55 * (1 - abs(k - sw) / 4))
        # slab + outer walls
        rect(c, TX0, yb - SLAB, TX1 - TX0, SLAB, CONCRETE, a)
        rect(c, TX0, yt, WALLW, FH, FACADE_DK, a)
        rect(c, TX1 - WALLW, yt, WALLW, FH, FACADE_DK, a)
        if k == 1:
            rect(c, TX0 + 220, yb - SLAB - 78, 150, 78, "#7DD3FC", a * 0.9, r=4)  # lobby doors

    def draw_people(self, c, t, k, z):
        T = self.T
        if k == FIRE_F and t >= T["fire"] - 0.3:
            return
        if k == REFUGE and T["refuge"] - 0.1 <= t < self.tl.s("cta") + 0.8:
            for i in range(6):
                world.person(c, AX0 + 90 + i * 115, fy(k) - SLAB, 72, **world.crowd_colors(i + 3),
                             a=prog(t, T["refuge"] - 0.1 + i * 0.05, T["refuge"] + 0.15 + i * 0.05))
            return
        if k == F13 and t >= self.tl.s("tag") - 0.6:
            sh = bump(t, T["slap"] + 0.05, T["slap"] + 1.5)
            world.person(c, 10, fy(k) - SLAB, 78, shirt="#8B5CF6", arms_up=0.9 * sh,
                         lean=0.12 * math.sin(t * 7) * sh)
            return
        sick = self.sick.at(t) if k >= 92 else 0.0
        for i, (x, ci) in enumerate(self.ppl[k]):
            col = dict(world.crowd_colors(ci))
            if sick > 0:
                col["skin"] = mix(col["skin"], "#86EFAC", sick)
            lean = sick * 0.6 * math.sin(t * 5 + i + k)
            world.person(c, x, fy(k) - SLAB, 72, lean=lean, **col)
            if sick > 0.3:
                swirl(c, x + 22 * lean, fy(k) - SLAB - 92, 13, t * 6 + i, (sick - 0.3) / 0.7)

    def draw_fire_floor(self, c, t, yt, yb, z):
        T = self.T
        fa = self.fire.at(t)
        sm = self.smoke.at(t)
        air = self.air.at(t)
        ih = FH - SLAB
        base = yb - SLAB
        if fa > 0:
            rect(c, AX0, yt, AX1 - WALLW - AX0, ih, "#FB923C", 0.28 * fa)
            glow(c, 400, base - 45, 300, "#FB923C", 0.7 * fa)
            for j, x in enumerate(range(250, 540, 30)):
                hgt = (62 + 22 * math.sin(t * 9 + j * 1.7) + 10 * math.sin(t * 15 + j)) * fa
                wdt = 30 * fa
                poly(c, [(x - wdt, base), (x - wdt * 0.45, base - hgt * 0.6), (x, base - hgt),
                         (x + wdt * 0.5, base - hgt * 0.55), (x + wdt, base)], "#EF4444", 0.95)
                poly(c, [(x - wdt * 0.62, base), (x, base - hgt * 0.68), (x + wdt * 0.62, base)], "#FB923C", 0.95)
                poly(c, [(x - wdt * 0.3, base), (x, base - hgt * 0.38), (x + wdt * 0.3, base)], "#FDE047", 0.95)
        if sm > 0:
            rng = random.Random(9)
            for row, yy in enumerate((yt + 22, yt + 46)):
                for i in range(24):
                    sx = 520 - i * 40 + 14 * math.sin(t * 2 + i + row)
                    if sx < ST0 + 30:
                        break
                    r = 30 + rng.uniform(0, 16) - row * 6
                    al = sm * (0.85 if row == 0 else 0.6)
                    if sx < ST1 + 26:  # the stair door: smoke gets in until the fans push it back
                        if air > 0:
                            sx = max(sx, ST1 + 26 + 40 * air)
                        al *= 0.85
                    circle(c, sx, yy + rng.uniform(-6, 8), r, "#374151", al)
        # sprinklers on this ceiling
        if t >= T["sprinklers"] - 0.3:
            sa = prog(t, T["sprinklers"] - 0.3, T["sprinklers"] - 0.05)
            line(c, AX0 + 10, yt + 6, AX1 - WALLW - 10, yt + 6, "#9CA3AF", 7, sa)
            spray = prog(t, T["sprinklers"] - 0.05, T["sprinklers"] + 0.2) * (1 - prog(t, T["smoke"], T["smoke"] + 0.6))
            for hx in (-150, 0, 150, 300, 450):
                rect(c, hx - 9, yt + 6, 18, 14, "#E5E7EB", sa, r=3)
                if spray > 0:
                    for d in range(-3, 4):
                        for m in range(5):
                            u = ((t * 2.4 + m * 0.2 + d * 0.07) % 1.0)
                            px = hx + d * 20 * (0.25 + u)
                            py = yt + 22 + u * (ih - 26)
                            circle(c, px, py, 5.5, "#3B82F6", spray * (1 - u * 0.5))
                            circle(c, px - 1.5, py - 1.5, 2.2, "#DBEAFE", spray * (1 - u * 0.5))
        # fans + fresh air in the stairwell (fix4)
        if air > 0:
            for fyp in (yt + 30,):
                fxp = ST0 + WALLW + 34
                circle(c, fxp, fyp, 28, "#F8FAFC", air)
                circle(c, fxp, fyp, 28, "#64748B", air, stroke=4)
                for b in range(3):
                    ang = t * 16 + b * 2.094
                    poly(c, [(fxp, fyp), (fxp + math.cos(ang - 0.35) * 24, fyp + math.sin(ang - 0.35) * 24),
                             (fxp + math.cos(ang + 0.35) * 24, fyp + math.sin(ang + 0.35) * 24)], "#3B82F6", air)
                circle(c, fxp, fyp, 5, "#1E3A8A", air)
            for m in range(6):
                u = (t * 0.9 + m / 6) % 1.0
                ax = lerp(ST0 + 50, ST1 + 10, u)
                ay = lerp(yt + 34, base - 28, ((m * 0.37) % 1.0))
                aa = air * min(1.0, 3 * (1 - abs(u - 0.5) * 2))
                poly(c, [(ax - 6, ay - 15), (ax + 24, ay), (ax - 6, ay + 15), (ax + 2, ay)], "#0EA5E9", aa)

    def draw_plate(self, c, t, yt):
        T = self.T
        cx_, cy_ = -150, yt + 34
        pw, ph = 104, 56
        pulse = 1 + 0.08 * bump(t, T["thirteen"] - 0.05, T["thirteen"] + 0.35)
        c.save()
        c.translate(cx_, cy_)
        c.scale(pulse, pulse)
        rect(c, -pw / 2 + 3, -ph / 2 + 4, pw, ph, "#000000", 0.25, r=9)
        rect(c, -pw / 2, -ph / 2, pw, ph, "#FFFFFF", 1.0, r=9)
        rect(c, -pw / 2, -ph / 2, pw, ph, "#111827", 1.0, r=9, stroke=4)
        text(c, "13", 0, 17, 46, "#111827", "Poppins-Black")
        c.restore()
        p = prog(t, T["slap"] - 0.08, T["slap"] + 0.12)
        if p > 0:
            k = lerp(1.9, 1.0, e_out(p))
            c.save()
            c.translate(cx_ + 4, cy_ - 2)
            c.rotate(-8)
            c.scale(k, k)
            rect(c, -60, -32, 120, 66, "#000000", 0.3, r=10, blur=4)
            rect(c, -60, -35, 120, 66, YELLOW, 1.0, r=10)
            text(c, "14", 0, 16, 50, "#111827", "Poppins-Black")
            c.restore()

    def draw_glass(self, c, t, k, cover, ga, dusk):
        yb, yt = fy(k), fy(k) - FH
        h = FH * cover
        top = yb - h
        g0 = mix("#A5D8F3", "#1F3A5F", dusk)
        g1 = mix("#3B82C4", "#0E1A33", dusk)
        grad_rect(c, TX0 - 6, top, TX1 - TX0 + 12, h, g0, g1, ga)
        for x in range(TX0 + 70, TX1, 70):
            line(c, x, top, x, yb, mix("#DDEFFC", "#1E293B", dusk), 3, ga * 0.6)
        line(c, TX0 - 6, yb - 3, TX1 + 6, yb - 3, mix("#E0F2FE", "#1E293B", dusk), 5, ga * 0.7)
        # sky reflections
        if dusk < 0.6:
            ph = (k * 37) % 400
            poly(c, [(TX0 + ph, top), (TX0 + ph + 90, top), (TX0 + ph + 30, yb), (TX0 + ph - 60, yb)], "#FFFFFF",
                 0.12 * ga * (1 - dusk))
        wl = self.wlit.at(t)
        if wl > 0 and cover > 0.98:
            rr = random.Random(k * 31)
            for x in range(TX0 + 8, TX1 - 60, 70):
                if rr.random() < 0.62:
                    rect(c, x + 6, yt + 16, 56, FH - 34, "#FFD98A", 0.85 * wl * ga)

    def draw_crown(self, c, t, dusk, ga):
        T = self.T
        sp = e_back(prog(t, self.t_top - 0.05, self.t_top + 0.35))
        if sp <= 0:
            return
        top = fy(NF + 1)
        dxx = self.dx(NF + 1, t)
        c.save()
        c.translate(dxx, 0)
        ch = CROWN_H * sp
        poly(c, [(TX0 + 60, top), (TX1 - 60, top), (TX1 - 200, top - ch), (TX0 + 200, top - ch)],
             mix("#CBD5E1", "#334155", dusk))
        line(c, 0, top - ch, 0, top - ch - SPIRE_H * sp, mix("#94A3B8", "#475569", dusk), 26)
        line(c, 0, top - ch, 0, top - ch - SPIRE_H * sp, mix("#E2E8F0", "#64748B", dusk), 8)
        if dusk > 0.4:
            b = 0.5 + 0.5 * math.sin(t * 6)
            glow(c, 0, top - ch - SPIRE_H * sp, 140, "#EF4444", 0.8 * b)
            circle(c, 0, top - ch - SPIRE_H * sp, 20, "#FCA5A5", b)
            wl = self.wlit.at(t)
            glow(c, 0, top - ch / 2, 420, "#93C5FD", 0.35 * wl)
        c.restore()

    def draw_cars(self, c, t, z):
        T = self.T
        a = self.car_a.at(t)
        if a <= 0:
            return
        for (x0, fpos, col, moving) in ((EX0 + 14, self.fe.at(t), GOLD, bump(t, T["shoot"] - 0.08, T["shoot"] + 0.67)),
                                        (LX0 + 14, self.fl.at(t), "#60A5FA",
                                         bump(t, T["local"] + 0.1, T["train"] - 0.2))):
            bottom = fy(fpos) - SLAB
            dxx = self.dx(fpos, t)
            c.save()
            c.translate(dxx, 0)
            rect(c, x0, bottom - CAR_H, CAR_W, CAR_H, col, a, r=6)
            rect(c, x0 + 8, bottom - CAR_H + 10, CAR_W - 16, CAR_H - 20, shade(col, 0.25), a, r=4)
            line(c, x0 + CAR_W / 2, bottom - CAR_H, x0 + CAR_W / 2, bottom - CAR_H - 3000, "#9CA3AF", 4, a * 0.7)
            if moving > 0.05:
                for i in range(4):
                    lx = x0 + 10 + i * 18
                    ln = 260 + 140 * ((i * 37) % 3)
                    line(c, lx, bottom + 30, lx, bottom + 30 + ln, "#FFFFFF", 10, 0.7 * moving)
            c.restore()

    def draw_damper(self, c, t, z):
        T = self.T
        da = self.damp_a.at(t)
        x0, x1 = AX0 + 6, AX1 - WALLW - 6
        ytop, ybot = fy(DAMP_HI + 1), fy(DAMP_LO) - SLAB
        k_mid = (DAMP_LO + DAMP_HI) / 2
        dxx = self.dx(k_mid, t)
        c.save()
        c.translate(dxx, 0)
        grad_rect(c, x0, ytop, x1 - x0, ybot - ytop, "#3A4152", "#262C38", da)
        for k in range(DAMP_LO, DAMP_HI + 1):
            line(c, x0, fy(k) - FH * 0.5, x1, fy(k) - FH * 0.5, "#4B5563", 3, da * 0.5)
        rect(c, x0, ybot - 18, x1 - x0, 18, "#6B7280", da)
        # ball on cables, pistons below
        pop = e_back(prog(t, T["ball"] - 0.1, T["ball"] + 0.3))
        th = self.ball_angle(t)
        px, py = BALL_X, ytop + 10
        L = CABLE_L + BALL_R
        bx, by = px + math.sin(th) * L, py + math.cos(th) * L
        if pop > 0:
            for off in (-120, -50, 50, 120):
                line(c, px + off, py, bx + off * 0.45, by - BALL_R * 0.8, "#CBD5E1", 7, da)
            for side in (-1, 1):
                ax, ay = bx + side * BALL_R * 0.72, by + BALL_R * 0.62
                fx_, fy_ = BALL_X + side * 300, ybot - 18
                line(c, ax, ay, fx_, fy_, "#9CA3AF", 16, da)
                mx, my = lerp(ax, fx_, 0.55), lerp(ay, fy_, 0.55)
                line(c, lerp(ax, fx_, 0.3), lerp(ay, fy_, 0.3), mx, my, YELLOW, 30, da)
            c.save()
            c.translate(bx, by)
            c.scale(pop, pop)
            circle(c, 0, 10, BALL_R, "#000000", 0.3 * da, blur=12)
            circle(c, 0, 0, BALL_R, GOLD, da)
            for i in range(-3, 4):
                yy = i * BALL_R / 3.6
                hw = math.sqrt(max(0.0, BALL_R ** 2 - yy ** 2))
                line(c, -hw, yy, hw, yy, GOLD_DK, 4, da * 0.6)
            circle(c, -BALL_R * 0.35, -BALL_R * 0.4, BALL_R * 0.32, GOLD_LT, da * 0.7)
            circle(c, 0, 0, BALL_R, GOLD_DK, da, stroke=6)
            c.restore()
        c.restore()
        self.ball_xy = (bx + dxx, by)

    def draw_frame(self, c, t, fv):
        T = self.T
        top = NF + 1
        for x in COLS:
            pts = [(x + self.dx(k, t), fy(k)) for k in range(1, top + 1)]
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                line(c, x0, y0, x1, y1, STEEL_LT, 70, fv)
                line(c, x0, y0, x1, y1, STEEL, 40, fv)
        for k in range(1, top + 1, 2):
            d = self.dx(k, t)
            line(c, TX0 + d, fy(k), TX1 + d, fy(k), STEEL, 26, fv * 0.9)
        # shock absorbers: diagonal braces in three wide bays, a yellow piston in each
        bays = ((TX0, LX1), (LX1, PART), (PART, TX1))
        for i, k in enumerate(range(5, NF - 3, 9)):
            p = prog(t, T["absorbers"] - 0.1 + i * 0.06, T["absorbers"] + 0.2 + i * 0.06)
            if p <= 0:
                continue
            xa, xb = bays[i % 3]
            if i % 2:
                xa, xb = xb, xa
            x0, y0 = xa + self.dx(k, t), fy(k)
            x1, y1 = xb + self.dx(k + 4, t), fy(k + 4)
            line(c, x0, y0, x1, y1, STEEL_LT, 30, fv * p)
            mx0, my0 = lerp(x0, x1, 0.33), lerp(y0, y1, 0.33)
            mx1, my1 = lerp(x0, x1, 0.67), lerp(y0, y1, 0.67)
            line(c, mx0, my0, mx1, my1, YELLOW, 64 * e_back(p), fv)

    # ------------------------------------------------------------ screen FX
    def draw_screen_fx(self, c, t, tw, dusk):
        """t = real time (overlays), tw = world time (frozen during the fake pause)."""
        T, tl = self.T, self.tl
        storm = self.storm.at(tw)
        if storm > 0:
            rng = random.Random(3)
            for i in range(110):
                x = (rng.uniform(0, W) + tw * 260) % (W + 200) - 100
                y = (rng.uniform(0, H) + tw * 1700) % (H + 300) - 150
                line(c, x, y, x - 22, y + 60, "#CBD5E1", 3, 0.45 * storm)
            fx.flash(c, W, H, 0.6 * bump(tw, T["storm"], T["storm"] + 0.16) + 0.45 * bump(tw, T["sways"] + 0.3, T["sways"] + 0.42))
        red = bump(t, T["stairs"] - 0.1, T["stairs"] + 1.0) * 0.8 + bump(t, T["seasick"] - 0.1, T["seasick"] + 1.0) * 0.8
        red += bump(t, T["quake"], T["quake"] + 1.6) * 0.9 + bump(t, T["fire"], T["fire"] + 1.4) * 0.9
        fx.red_vignette(c, W, H, clamp(red))
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), skiaradial())
        self.draw_outlines(c, tw)
        self.draw_labels(c, tw)
        self.draw_badges(c, tw)
        # fake pause + follow pill
        pz = prog(t, T["pause"], T["pause"] + 0.25) * (1 - prog(t, tl.s("cta") + 0.55, tl.s("cta") + 0.85))
        if pz > 0:
            fx.dim(c, W, H, 0.3 * pz)
            fx.pause_icon(c, W, H, pz, t)
        pill = prog(t, T["follow"] - 0.15, T["follow"] + 0.2) * (1 - prog(t, tl.e("cta") + 0.1, tl.e("cta") + 0.4))
        label, sub = self.tx["follow"]
        if self.lang.startswith("ar"):
            wp = arabic.width_ar(label, 66, "Tajawal-Black") + arabic.width_ar(sub, 46, "Tajawal-Bold") + 210
        else:
            wp = text_width(label, 64, "Poppins-Black") + text_width(sub, 44, "Poppins-SemiBold") + 210
        kp = min(1.0, (W - 70) / wp)
        c.save()
        c.translate(W / 2, 210)
        c.scale(kp, kp)
        c.translate(-W / 2, -210)
        if self.lang.startswith("ar"):
            arabic.cta_pill_ar(c, W, label, sub, pill)
        else:
            fx.cta_pill(c, W, label, sub, pill)
        c.restore()
        # stat badges
        bt = 1 - prog(t, tl.s("closer") - 0.1, tl.s("closer") + 0.3)
        rtl = self.lang.startswith("ar")
        xs = (W * 0.8, W * 0.5, W * 0.2) if rtl else (W * 0.2, W * 0.5, W * 0.8)
        badge = arabic.stat_badge_ar if rtl else fx.stat_badge
        for (big, small), x, key, col in zip(self.tx["stat"], xs, ("one", "hundred2", "ten"),
                                             ("#111827", "#111827", "#2563EB")):
            badge(c, x, 330, big, small, prog(t, T[key], T[key] + 0.3) * bt, color=col)
        fx.confetti(c, W, H, t, T["cong2"], 2.6)
        fx.confetti(c, W, H, t, self.t_top + 0.05, 1.6, seed=8, n=40)

    def draw_labels(self, c, t):
        T, tx = self.T, self.tx
        # floor 99 tag
        p = prog(t, T["n99"] - 0.25, T["n99"] + 0.05) * (1 - prog(t, T["climb"] - 0.45, T["climb"] - 0.3))
        if p > 0:
            x, y = self.sc(TX1 + 40, fy(99) - FH / 2)
            self.pill(c, [tx["floor"], "99"], min(x + 120, W - 150), y, p)
        # climber counter
        if T["climb"] - 0.3 <= t < T["express"] - 0.1:
            x, y, pr, _ = self.climber(t)
            sx, sy = self.sc(x + self.dx(int(pr), t), y - 130)
            n = int(clamp(pr, 1, 98))
            tired = prog(t, T["stairs"] - 0.2, T["stairs"] + 0.1)
            self.pill(c, f"{n} / 98", sx, sy, prog(t, T["climb"] - 0.3, T["climb"] - 0.1),
                      fg=mix("#111827", "#FFFFFF", tired), bg=mix("#FFFFFF", RED, tired), size=40)
        # elevators
        a = prog(t, T["express"], T["express"] + 0.3) * (1 - prog(t, T["lobby"] - 0.2, T["lobby"]))
        if a > 0:
            x, y = self.sc(EX0 + 14 + CAR_W / 2, fy(self.fe.at(t)) - SLAB - CAR_H - 45)
            self.pill(c, tx["express"], max(x, 130), y, a, fg="#111827", bg=GOLD_LT)
        a = prog(t, T["lobby"] - 0.1, T["lobby"] + 0.2) * (1 - prog(t, T["local"] + 0.5, T["local"] + 0.7))
        if a > 0:
            x, y = self.sc(AX0 + 260, fy(SKY_LOBBY) - FH / 2)
            self.pill(c, tx["sky"], x, y, a, fg="#111827", bg=YELLOW, size=42)
        a = prog(t, T["local"], T["local"] + 0.3) * (1 - prog(t, T["local"] + 0.5, T["local"] + 0.7))
        if a > 0:
            x, y = self.sc(LX0 + 14 + CAR_W / 2, fy(self.fl.at(t)) - SLAB - CAR_H - 45)
            self.pill(c, tx["local"], x, y, a, fg="#FFFFFF", bg="#2563EB")
        self.draw_routes(c, t)
        # damper: weights
        if T["jumbo"] - 0.2 <= t < self.tl.s("break3") and hasattr(self, "ball_xy"):
            p = prog(t, T["jumbo"] - 0.15, T["jumbo"] + 0.15) * (1 - prog(t, T["leans"] - 0.5, T["leans"] - 0.2))
            bx, by = self.sc(*self.ball_xy)
            self.pill(c, ["660", tx["ton"]], bx, by + 8, p, fg="#111827", bg="#FFFFFF", size=44)
            pj = p * (1 - prog(t, T["cables"] - 0.35, T["cables"] - 0.05))
            jx, jy = self.sc(AX0 + 40, fy(94) - 20)
            jet(c, jx, jy, pj)
            self.pill(c, ["450", tx["ton"]], jx, jy + 70, pj, fg="#111827", bg="#E5E7EB", size=34)
        # bedrock, refuge, fans, fire floor
        p = prog(t, T["refuge"], T["refuge"] + 0.3) * (1 - prog(t, self.tl.s("cta") + 0.3, self.tl.s("cta") + 0.6))
        if p > 0:
            x, y = self.sc(PART, fy(REFUGE) - FH - 46)
            self.pill(c, tx["refuge"], x, y, p, fg="#FFFFFF", bg="#16A34A", size=40)
        p = prog(t, T["fans"], T["fans"] + 0.3) * (1 - prog(t, T["refuge"] - 0.5, T["refuge"] - 0.3))
        if p > 0:
            x, y = self.sc((ST0 + ST1) / 2, fy(FIRE_F + 1) - 40)
            self.pill(c, tx["fans"], max(x, 170), y, p, fg="#0C4A6E", bg="#BAE6FD", size=36)
        p = prog(t, T["eighty"] - 0.25, T["eighty"] + 0.05) * (1 - prog(t, T["stairwells"] - 0.4, T["stairwells"] - 0.2))
        if p > 0:
            x, y = self.sc(PART, fy(FIRE_F) - FH - 50)
            self.pill(c, [tx["floor"], "80"], x, y, p, fg="#FFFFFF", bg=RED, size=42)

    def draw_routes(self, c, t):
        """Wide shot of fix1: gold line = express (train), blue line = local (bus), glowing car markers."""
        T, tl = self.T, self.tl
        out = 1 - prog(t, tl.s("break2") - 0.2, tl.s("break2") + 0.2)
        if out <= 0 or t < T["local"]:
            return
        z = self.cam_state[2]
        mk = clamp((0.35 - z) / 0.15) * out
        for key, x, f0, f1, col, kind, wy in (("train", (EX0 + EX1) / 2, 1, SKY_LOBBY, GOLD, 0, fy(38)),
                                               ("bus", (LX0 + LX1) / 2, SKY_LOBBY, 99, "#3B82F6", 1, fy(80))):
            p = prog(t, T[key] - 0.15, T[key] + 0.3) * out
            if p > 0:
                x0, y0 = self.sc(x, fy(f0) - 50)
                x1, y1 = self.sc(x, fy(f1) - 50)
                ye = lerp(y0, y1, e_out(p))
                line(c, x0, y0, x1, ye, "#FFFFFF", 22, p)
                line(c, x0, y0, x1, ye, col, 12, p)
                circle(c, x0, y0, 14, col, p)
                circle(c, x1, ye, 14, col, p)
                ix, iy = self.sc(EX0 - 60, wy)
                icon(c, kind, ix - 110, iy, prog(t, T[key] - 0.1, T[key] + 0.2) * out)
        if mk > 0:
            for f, col in ((self.fe.at(t), GOLD), (self.fl.at(t), "#3B82F6")):
                x = EX0 + 50 if col == GOLD else LX0 + 50
                sx, sy = self.sc(x, fy(f) - 50)
                glow(c, sx, sy, 46, col, 0.9 * mk)
                circle(c, sx, sy, 13, "#FFFFFF", mk)
                circle(c, sx, sy, 9, col, mk)

    def draw_outlines(self, c, t):
        T = self.T

        def ol(t0, rw, dur=1.3, color="#FFFFFF"):
            a = 1 - prog(t, t0 + dur - 0.3, t0 + dur)
            if t0 <= t < t0 + dur:
                fx.outline(c, *self.sc_rect(*rw), prog(t, t0, t0 + 0.35), color=color, a=a)
        fe, fl = self.fe.at(t), self.fl.at(t)
        ol(T["express"] + 0.1, (EX0 + 14, fy(fe) - SLAB - CAR_H, CAR_W, CAR_H), 1.0)
        ol(T["lobby"] + 0.15, (EX0, fy(SKY_LOBBY) - FH, AX1 - EX0, FH), 1.0)
        ol(T["local"] + 0.05, (LX0 + 14, fy(fl) - SLAB - CAR_H, CAR_W, CAR_H), 0.5)
        if hasattr(self, "ball_xy"):
            bx, by = self.ball_xy
            ol(T["ball"] + 0.35, (bx - BALL_R, by - BALL_R, BALL_R * 2, BALL_R * 2), 1.0)
            ol(T["cables"] + 0.1, (BALL_X - 140 + self.dx(95, t), fy(DAMP_HI + 1), 280, CABLE_L), 1.0)
            ol(T["pistons"] + 0.1, (BALL_X - 320 + self.dx(91, t), by + BALL_R * 0.4, 640, fy(DAMP_LO) - (by + BALL_R * 0.4)), 1.0)
        ol(T["frame"] + 0.15, (TX0, fy(NF + 1), TX1 - TX0, -fy(NF + 1)), 1.2)
        ol(T["found"] + 0.3, (TX0 - 40, 0, TX1 - TX0 + 80, PILE_D + 120), 1.4)
        ol(T["sprinklers"] + 0.15, (AX0, fy(FIRE_F) - FH, AX1 - AX0, 40), 1.0)
        ol(T["stairwells"] + 0.15, (ST0, fy(FIRE_F + 1) - FH, ST1 - ST0, FH * 3), 1.3)
        if T["one"] <= t < self.tl.s("closer"):
            a = 1 - prog(t, self.tl.s("closer") - 0.3, self.tl.s("closer"))
            fx.outline(c, *self.sc_rect(TX0 - 260, -40, TX1 - TX0 + 520, 80), prog(t, T["one"], T["one"] + 0.35),
                       color=YELLOW, r=16, width=14, pad=10, a=a)

    def draw_badges(self, c, t):
        T, tl = self.T, self.tl
        # alerts
        if T["stairs"] - 0.1 <= t < tl.s("fix1"):
            x, y, pr, _ = self.climber(t)
            sx, sy = self.sc(x, y - 60)
            fx.alert_badge(c, sx + 120, sy - 40, prog(t, T["stairs"] - 0.1, T["stairs"] + 0.15), 1.2, t)
        if T["seasick"] - 0.15 <= t < T["ball"]:
            sx, sy = self.sc(TX1, fy(97))
            fx.alert_badge(c, min(sx + 90, W - 90), sy, prog(t, T["seasick"] - 0.15, T["seasick"] + 0.1), 1.3, t)
        if T["quake"] + 0.1 <= t < T["frame"] - 0.1:
            sx, sy = self.sc(TX1 + 200, -6000)
            fx.alert_badge(c, min(sx + 60, W - 90), sy, prog(t, T["quake"] + 0.1, T["quake"] + 0.35), 1.4, t)
        if T["fire"] + 0.2 <= t < T["sprinklers"] + 0.2:
            sx, sy = self.sc(TX1 - 60, fy(FIRE_F) - FH - 60)
            fx.alert_badge(c, min(sx, W - 90), sy, prog(t, T["fire"] + 0.2, T["fire"] + 0.45), 1.3, t)
        # checks
        for t0, wx, wy in ((T["bus"] + 0.3, LX1 + 200, -7600), (tl.e("fix2") - 0.3, TX1 + 120, fy(93)),
                           (T["bedrock"] + 0.3, TX1 + 260, ROCK_Y0 - 700), (T["safely"] + 0.15, TX1 + 80, fy(REFUGE) - 60)):
            p = prog(t, t0, t0 + 0.35) * (1 - prog(t, t0 + 1.2, t0 + 1.5))
            if p > 0:
                sx, sy = self.sc(wx, wy)
                fx.check_badge(c, clamp(sx, 90, W - 90), clamp(sy, 200, 1200), p, 1.4)
        # stat: people twinkle in the windows
        if T["ten"] - 0.1 <= t < tl.s("closer") + 0.5:
            p = prog(t, T["ten"] - 0.1, T["ten"] + 0.4) * (1 - prog(t, tl.s("closer"), tl.s("closer") + 0.5))
            rng = random.Random(77)
            for i in range(70):
                k = rng.randint(2, NF)
                x = rng.uniform(TX0 + 40, TX1 - 40)
                sx, sy = self.sc(x, fy(k) - 40)
                tw_ = 0.5 + 0.5 * math.sin(t * 9 + i)
                circle(c, sx, sy, 3.5 + 2 * tw_, "#FFFFFF", p * tw_)

    # ------------------------------------------------------------- sound
    def sfx_events(self):
        T, tl = self.T, self.tl
        s, e = tl.s, tl.e
        ev = [(0.0, sfx.whoosh(0.5, True, 1), -10)]
        for k in range(1, 11):
            ev.append((max(0.0, self.tk[k] - 0.02), sfx.pop(k), -8 - k * 0.3))
        for k in range(20, NF + 1, 10):
            ev.append((self.tk[k] - 0.02, sfx.thunk(10 + k), -16))
        ev += [(T["hundred"] + 0.3, sfx.riser(max(0.6, self.t_top - T["hundred"] - 0.3)), -12),
               (self.t_top, sfx.thud(), -3), (T["cong"], sfx.pop(), -2), (T["cong"], sfx.sparkle(), -8)]
        # break1
        ev += [(s("break1") - 0.1, sfx.whoosh(0.5, True, 3), -10), (T["n99"] - 0.1, sfx.pop(5), -6),
               (T["climb"] - 0.4, sfx.whoosh(0.5, False, 4), -10)]
        tt = T["climb"] - 0.1
        i = 0
        while tt < T["stairs"] + 0.25:
            ev.append((tt, sfx.tap(i), -12))
            tt += 0.17
            i += 1
        ev += [(T["stairs"], sfx.buzz(), -6), (T["stairs"] + 0.05, sfx.alarm(1, 700), -12)]
        # fix1
        ev += [(T["express"] - 0.1, sfx.pop(12), -6), (T["shoot"] - 0.08, sfx.whoosh(0.75, True, 13), -4),
               (T["shoot"] + 0.7, sfx.ding(), -6), (T["lobby"], sfx.sparkle(0.5, 6, 14), -10),
               (T["local"] + 0.1, sfx.whirr(1.2, 180, 320, 15), -12),
               (T["train"], sfx.bell(660, 0.5, 0.8), -10), (T["bus"], sfx.beep(520, 0.12), -8),
               (T["bus"] + 0.3, sfx.chime(), -6)]
        # break2
        ev += [(s("break2") - 0.1, sfx.whoosh(0.8, True, 16), -12), (T["home"], sfx.ding(), -12),
               (T["storm"] - 0.05, sfx.hiss(2.6, 17), -19), (T["storm"], sfx.thud(0.6, 18), -2),
               (T["storm"] + 0.02, sfx.whoosh(0.9, False, 18), -8), (T["sways"] + 0.32, sfx.creak(1.0, 19), -10),
               (T["sways"] + 0.3, sfx.thud(0.4, 20), -6), (T["seasick"], sfx.buzz(), -6),
               (T["seasick"] + 0.05, sfx.alarm(2, 800), -12)]
        # fix2
        ev += [(s("fix2") - 0.05, sfx.whoosh(0.5, True, 21), -10), (T["ball"] - 0.05, sfx.whoosh(0.4, False, 22), -8),
               (T["ball"] + 0.2, sfx.clank(180, 0.8, 23), -2), (T["ball"] + 0.2, sfx.thud(), -4),
               (T["jumbo"], sfx.whoosh(0.7, True, 24), -8)]
        ev += [(T["cables"] + i * 0.09, sfx.click(30 + i), -6) for i in range(4)]
        ev += [(T["pistons"], sfx.hiss(0.5, 25), -6), (T["pistons"] + 0.05, sfx.clank(600, 0.3, 26), -10),
               (T["leans"] - 0.3, sfx.creak(0.9, 27), -6), (T["swings"] - 0.25, sfx.whoosh(0.6, True, 28), -6),
               (e("fix2") - 0.3, sfx.chime(), -6)]
        # break3
        ev += [(s("break3") - 0.15, sfx.whoosh(0.8, False, 29), -12), (T["quake"], sfx.hum(2.6, 42), -2),
               (T["quake"], sfx.thud(0.6, 30), 0)]
        ev += [(T["quake"] + 0.3 + j * 0.33, sfx.thud(0.35, 31 + j), -6) for j in range(6)]
        ev += [(T["shaking"], sfx.snap(), -6), (T["shaking"] + 0.05, sfx.alarm(2, 900), -12)]
        # fix3
        ev += [(T["frame"] - 0.25, sfx.clank(420, 0.5, 40), -8), (T["bends"], sfx.creak(1.2, 41), -8)]
        ev += [(T["absorbers"] + i * 0.07, sfx.clank(800 - i * 40, 0.25, 50 + i), -12) for i in range(10)]
        ev += [(T["found"] - 0.4, sfx.whoosh(0.7, False, 60), -10)]
        ev += [(T["found"] + j * 0.28, sfx.thunk(61 + j), -4) for j in range(4)]
        ev += [(T["bedrock"] + 0.1, sfx.clank(150, 0.9, 65), -4), (T["bedrock"] + 0.3, sfx.chime(), -6)]
        # break4
        ev += [(s("break4") - 0.1, sfx.whoosh(0.8, True, 66), -12), (T["anything"], sfx.sparkle(0.6, 7, 67), -10),
               (T["fire"] - 0.35, sfx.whoosh(0.5, True, 68), -10), (T["fire"], sfx.sizzle(1.2, 69), -4),
               (T["fire"] + 0.05, sfx.whoosh(0.6, True, 70), -8), (T["eighty"], sfx.alarm(3, 850), -10)]
        # fix4
        ev += [(T["sprinklers"], sfx.hiss(1.6, 71), -8), (T["everywhere"] + 0.4, sfx.sizzle(0.8, 72), -8),
               (T["stairwells"] - 0.35, sfx.whoosh(0.5, False, 73), -10),
               (T["fans"] - 0.1, sfx.whirr(2.0, 110, 160, 74), -10), (T["smoke"], sfx.whoosh(0.6, True, 75), -12),
               (T["refuge"] - 0.4, sfx.whoosh(0.6, False, 76), -12), (T["refuge"] + 0.1, sfx.sparkle(0.6, 8, 77), -10),
               (T["safely"] + 0.15, sfx.chime(), -6)]
        # cta / reveal / stat / closer
        ev += [(T["pause"], sfx.click(80), 0), (T["follow"] - 0.15, sfx.pop(81), -4)]
        ev += [(T["wrap"] - 0.05, sfx.whoosh(1.2, True, 82), -6), (T["glass"], sfx.sparkle(0.8, 9, 83), -6),
               (T["lights"] - 0.05, sfx.click(84), -4), (T["lights"], sfx.charge_up(0.6), -8),
               (T["lights"] + 0.1, sfx.chime(), -8)]
        ev += [(T["one"], sfx.pop(85), -3), (T["hundred2"], sfx.pop(86), -3), (T["hundred2"], sfx.whoosh(0.8, True, 87), -12),
               (T["ten"], sfx.pop(88), -3), (T["ten"] + 0.1, sfx.sparkle(1.0, 12, 89), -10)]
        ev += [(T["cong2"], sfx.pop(90), -2), (T["cong2"], sfx.sparkle(1.0, 14, 91), -4),
               (e("closer") - 0.4, sfx.chime(), -6)]
        # tag
        ev += [(s("tag") - 0.22, sfx.whoosh(0.45, False, 95), -6), (T["thirteen"], sfx.beep(1200, 0.08), -10),
               (T["slap"], sfx.thud(0.3, 96), -2), (T["slap"], sfx.pop(97), -4), (T["womp"], sfx.womp(), -2)]
        return ev


# ---------------------------------------------------------------- small drawings (screen space)
def icon(c, kind, x, y, p):
    """Train (0) or bus (1) pictogram in a white circle."""
    if p <= 0:
        return
    k = e_back(clamp(p))
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    circle(c, 0, 6, 64, "#000000", 0.25, blur=8)
    circle(c, 0, 0, 64, "#FFFFFF")
    col = "#2563EB" if kind == 0 else "#F59E0B"
    if kind == 0:
        rect(c, -34, -36, 68, 62, col, r=16)
        rect(c, -24, -26, 48, 22, "#DBEAFE", r=5)
        circle(c, -16, 12, 6, "#FFFFFF")
        circle(c, 16, 12, 6, "#FFFFFF")
        line(c, -20, 28, -30, 42, col, 6)
        line(c, 20, 28, 30, 42, col, 6)
    else:
        rect(c, -40, -30, 80, 54, col, r=12)
        for i in range(3):
            rect(c, -32 + i * 24, -22, 18, 18, "#FEF3C7", r=3)
        circle(c, -22, 26, 9, "#111827")
        circle(c, 22, 26, 9, "#111827")
    c.restore()


def swirl(c, x, y, r, ph, a):
    """Dizzy spiral above a seasick head (world space)."""
    if a <= 0:
        return
    pts = []
    for i in range(26):
        ang = ph + i * 0.48
        rr = r * (0.15 + i / 26)
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr * 0.7))
    poly(c, pts, "#16A34A", a, stroke=4.5, close=False)


def jet(c, x, y, p):
    """Jumbo jet silhouette, pops in."""
    if p <= 0:
        return
    k = e_back(clamp(p))
    c.save()
    c.translate(x, y)
    c.scale(k * 1.1, k * 1.1)
    col = "#F8FAFC"
    rect(c, -95, -12, 190, 24, col, r=12)
    poly(c, [(-20, -6), (40, -6), (-10, -70), (-35, -70)], col)
    poly(c, [(-20, 6), (40, 6), (-10, 70), (-35, 70)], col)
    poly(c, [(-95, -6), (-70, -6), (-92, -36), (-105, -36)], col)
    rect(c, 70, -8, 30, 16, "#CBD5E1", r=8)
    c.restore()


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


NAME = "skyscraper"
EPISODE = Skyscraper
