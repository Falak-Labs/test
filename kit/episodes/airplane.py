"""Episode 11 - An airplane.  v2 look: seven small sets with whip cuts.

cliff   a bus with wings glued on drives off a cliff ... and falls into the lake far below
foil    one wing in the wind: flat, then curved and tilted, with a jet engine under it
cruise  high up: the bus (everyone asleep), then the sealed cabin fed with air from the engines
rear    the airliner seen from behind: wobbling, then tail, rudder, elevators, ailerons
runway  landing: too fast with no brakes, then flaps, landing gear, thrust reversers
final   the finished airliner on the apron and climbing away
cabin   three seats, two armrests in the middle
"""
from v2_base import *  # noqa: F401,F403

BUSC, JETC, WINGC = "#FACC15", "#F1F5F9", "#CBD5E1"
FALL = 5200.0                                   # how far below the cliff top the lake is
KIDS = ("#22D3EE", "#F97316", "#A3E635", "#F472B6")


# ====================================================================================== pieces
def sky_set(c, t, alt=0.0, hy=None, speed=40.0, seed=0, cl=1.0):
    v2.sky(c, W, H, alt, horizon_y=H * 0.82 if hy is None else hy)
    v2.stars(c, W, H, t, 0.5 + 0.5 * alt)
    for i, (py, s_) in enumerate(((430, 1.0), (790, 0.8), (1090, 1.25), (250, 0.6))):
        x = (300 * i + 220 - t * speed * (0.5 + 0.25 * i)) % (W + 760) - 380
        v2.cloud(c, x, py, s_, a=0.8 * (1 - alt) * cl, seed=seed + i)


def nacelle(c, x, y, s=1.0, rev=0.0, power=0.0, t=0.0, a=1.0):
    """Jet engine pod seen from the side, intake to the right. rev 0..1 slides the back of the cowl open."""
    if power > 0:
        v2.flame(c, x - 62 * s, y, 20 * s, 150 * s * power, t, power * 0.8, seed=3, ang=180)
    c.drawRRect(rr(x - 66 * s - 22 * s * rev, y - 22 * s, 60 * s, 44 * s, 16 * s), P("#94A3B8", a))
    if rev > 0:
        c.drawRect(R(x - 22 * s * rev - 8 * s, y - 20 * s, 22 * s * rev + 6 * s, 40 * s), P("#F97316", 0.9 * a))
    c.drawRRect(rr(x - 10 * s, y - 25 * s, 76 * s, 50 * s, 20 * s), lin_paint(0, y - 25 * s, 0, y + 25 * s, [("#F8FAFC", a), ("#CBD5E1", a), ("#64748B", a)]))
    c.drawOval(R(x + 52 * s, y - 21 * s, 14 * s, 42 * s), P("#0B1220", a))
    c.drawOval(R(x + 55 * s, y - 13 * s, 8 * s, 26 * s), P("#475569", a))


def bus(c, t, wings=0.0, good=0.0, eng=0.0, cut=0.0, power=0.0):
    """The bus, centred on the origin, nose to the right, wheels touching y = 88."""
    k = e_back(clamp(wings))
    if k > 0:                                                                        # the far wing
        far = skia.Path()
        far.moveTo(60, -30)
        far.lineTo(-50, -30)
        far.lineTo(-110, -30 - 46 * k)
        far.lineTo(-30, -30 - 46 * k)
        far.close()
        c.drawPath(far, P("#94A3B8"))
    c.drawRRect(rr(-190, -62, 380, 124, 24), lin_paint(0, -62, 0, 62, [shade(BUSC, 0.22), BUSC, shade(BUSC, -0.3)]))
    if cut > 0:
        c.drawRRect(rr(-176, -50, 352, 92, 14), P("#27324F"))
        c.drawRect(R(-176, 30, 352, 5), P("#7C8499"))
        add_glow(c, 0, -30, 200, "#FFE9B8", 0.25)
    else:
        for i in range(6):
            c.drawRRect(rr(-172 + i * 52, -46, 40, 36, 6), P("#7DD3FC", 0.85))
        c.drawRRect(rr(146, -46, 32, 46, 7), P("#BAE6FD"))
    c.drawRect(R(-190, 46, 380, 9), P("#11151F", 0.85))
    for wx in (-118, 118):
        c.drawCircle(wx, 62, 26, P("#11151F"))
        c.drawCircle(wx, 62, 11, P("#94A3B8"))
    c.drawRRect(rr(178, 20, 16, 12, 4), P("#FFF3C4"))
    if k > 0:                                                                        # the near wing
        if eng > 0:
            nacelle(c, -86, 74, 0.95 * e_back(clamp(eng)), 0.0, power, t)
        w = skia.Path()
        w.moveTo(74, 0)
        w.lineTo(-58, 0)
        w.lineTo(-176, 62 * k)
        w.lineTo(-70, 62 * k)
        w.close()
        c.drawPath(w, lin_paint(0, 0, 0, 62, [shade(WINGC, 0.2), WINGC, shade(WINGC, -0.25)]))
        if good > 0:                                                                 # a proper rounded leading edge
            c.drawLine(74, 0, -70, 62 * k, P("#F8FAFC", good, stroke=9))
        else:
            for gx in (-40, -6, 30, 58):                                             # glue
                c.drawOval(R(gx - 7, -6, 14, 9 + 5 * math.sin(gx)), P("#FEF3C7", 0.95))


def jet_path():
    p = skia.Path()
    p.moveTo(300, 2)
    p.cubicTo(292, -46, 236, -64, 172, -64)
    p.lineTo(-220, -64)
    p.cubicTo(-300, -60, -350, -34, -384, -20)
    p.lineTo(-384, 0)
    p.cubicTo(-330, 40, -262, 60, -200, 62)
    p.lineTo(190, 62)
    p.cubicTo(250, 60, 294, 40, 300, 2)
    p.close()
    return p


def jet(c, t, tail=1.0, gear=0.0, squat=0.0, flaps=0.0, rev=0.0, win=0.0, cut=0.0, power=0.0, hot=0.0, box=0.0, inner=None):
    """The airliner from the side, centred on the origin, nose to the right; with the gear down the wheels reach y = 132."""
    tk = e_back(clamp(tail))
    if tk > 0:                                                                       # fin and stabiliser
        fin = skia.Path()
        fin.moveTo(-232, -60)
        fin.lineTo(-300 - 78 * tk, -60 - 128 * tk)
        fin.lineTo(-300 - 34 * tk, -60 - 128 * tk)
        fin.lineTo(-296, -58)
        fin.close()
        c.drawPath(fin, lin_paint(-380, 0, -230, 0, ["#0F766E", ACCENT]))
        c.drawCircle(-318, -122 * tk, 13 * tk, P("#F8FAFC"))
    g = clamp(gear)
    if g > 0:                                                                        # landing gear
        for gx, n in ((214, 1), (-36, 2)):
            ly = 58 + (60 - 10 * squat) * g
            c.drawLine(gx, 54, gx, ly, P("#94A3B8", 1, stroke=7))
            c.drawLine(gx, 54, gx - 16, 54 + 26 * g, P("#64748B", 1, stroke=4))
            for j in range(n):
                wx = gx + (j * 30 - 15 if n == 2 else 0)
                c.drawCircle(wx, ly + 2, 14, P("#11151F"))
                c.drawCircle(wx, ly + 2, 6, P(mix("#94A3B8", "#FF6B2C", hot)))
                if hot > 0:
                    add_glow(c, wx, ly + 2, 26, "#FF6B2C", 0.8 * hot)
    body = jet_path()
    c.drawPath(body, lin_paint(0, -64, 0, 62, ["#FFFFFF", JETC, "#94A3B8"], [0.0, 0.5, 1.0]))
    c.save()
    c.clipPath(body, skia.ClipOp.kIntersect, True)
    c.drawRect(R(-400, 8, 720, 7), P(ACCENT))
    if cut > 0:
        c.drawRRect(rr(-250, -52, 470, 96, 30), P("#27324F"))
        c.drawRect(R(-250, 24, 470, 5), P("#7C8499"))
        add_glow(c, -20, -40, 260, "#FFE9B8", 0.22)
        if inner:
            inner(c, t)
    if box > 0:                                                                      # the "black" box, back in the tail
        c.drawCircle(-276, -18, 30 * e_back(clamp(box)), P("#1B2238"))
        c.drawRRect(rr(-290, -30, 28, 22, 4), P("#F97316", clamp(box)))
        c.drawRect(R(-290, -22, 28, 4), P("#FFFFFF", 0.8 * clamp(box)))
        add_glow(c, -276, -19, 44, "#FB923C", 0.8 * clamp(box) * (0.6 + 0.4 * math.sin(t * 8)))
    c.restore()
    wshield = skia.Path()
    wshield.moveTo(236, -44)
    wshield.lineTo(266, -30)
    wshield.lineTo(256, -22)
    wshield.lineTo(228, -26)
    wshield.close()
    c.drawPath(wshield, P("#0B1220"))
    if win > 0 and cut <= 0:
        n = 16
        for i in range(n):
            wk = e_back(clamp(win * n - i))
            if wk > 0:
                c.drawRRect(rr(-218 + i * 26 - 6 * wk, -34 - 8 * wk + 8, 12 * wk, 16 * wk, 5 * wk), P("#0B1220"))
                c.drawRRect(rr(-218 + i * 26 - 4 * wk, -24 - 5 * wk, 8 * wk, 6 * wk, 3 * wk), P("#FDE68A", 0.9))
    c.drawRRect(rr(176, -40, 22, 50, 6), P("#94A3B8", 0.55, stroke=2))               # the door
    # the wing, its flap, the engine
    nacelle(c, -30, 86, 1.0, rev, power, t)
    f = clamp(flaps)
    if f > 0:
        fp = skia.Path()
        fp.moveTo(-40, 16)
        fp.lineTo(-186, 80)
        fp.lineTo(-206 - 20 * f, 80 + 34 * f)
        fp.lineTo(-64 - 20 * f, 16 + 34 * f)
        fp.close()
        c.drawPath(fp, P("#94A3B8"))
    wing = skia.Path()
    wing.moveTo(66, 10)
    wing.lineTo(-40, 14)
    wing.lineTo(-190, 80)
    wing.lineTo(-128, 80)
    wing.close()
    c.drawPath(wing, lin_paint(0, 10, 0, 80, ["#F8FAFC", WINGC, "#94A3B8"]))
    c.drawLine(66, 10, -128, 80, P("#FFFFFF", 0.9, stroke=6))
    if tk > 0:
        st = skia.Path()
        st.moveTo(-292, -22)
        st.lineTo(-300 - 70 * tk, -34)
        st.lineTo(-300 - 50 * tk, -14)
        st.lineTo(-282, -8)
        st.close()
        c.drawPath(st, P(WINGC))


def rear(c, t, tail=0.0, rud=0.0, elev=0.0, ail=0.0, hl=None):
    """The airliner from behind, centred on the origin. rud, elev, ail -1..1 move the control surfaces. hl names the
    surface to light up: "rud" | "elev" | "ail"."""
    for sd in (-1, 1):                                                               # wings and engines
        w = skia.Path()
        w.moveTo(sd * 60, 18)
        w.lineTo(sd * 440, -22)
        w.lineTo(sd * 440, -12)
        w.lineTo(sd * 60, 44)
        w.close()
        c.drawPath(w, lin_paint(0, -22, 0, 44, ["#F8FAFC", WINGC, "#94A3B8"]))
        c.drawCircle(sd * 196, 62, 38, lin_paint(0, 24, 0, 100, ["#E2E8F0", "#64748B"]))
        c.drawCircle(sd * 196, 62, 24, P("#1B2238"))
        add_glow(c, sd * 196, 62, 40, "#FF9A4D", 0.75)
        c.drawCircle(sd * 196, 62, 11, P("#FFD9A0"))
        a = ail * sd                                                                 # ailerons: one up, one down
        col = HILITE if hl == "ail" else "#94A3B8"
        if tail > 0:
            c.drawRect(R(sd * 440 - (96 if sd > 0 else 0), -17 - (30 * a if a > 0 else 0) + (0 if a > 0 else 4), 96, 8 + 30 * abs(a)), P(col))
    tk = e_back(clamp(tail))
    if tk > 0:
        for sd in (-1, 1):                                                           # stabilisers and elevators
            c.drawRect(R(sd * 20 - (180 if sd < 0 else 0), -64, 180, 10), P(WINGC))
            col = HILITE if hl == "elev" else "#94A3B8"
            c.drawRect(R(sd * 60 - (130 if sd < 0 else 0), -62 - (26 * elev if elev > 0 else 0), 130, 6 + 26 * abs(elev)), P(col))
        fin = skia.Path()
        fin.moveTo(-9, -60)
        fin.lineTo(-5, -60 - 250 * tk)
        fin.lineTo(5, -60 - 250 * tk)
        fin.lineTo(9, -60)
        fin.close()
        c.drawPath(fin, lin_paint(0, -310, 0, -60, [ACCENT, "#0F766E"]))
        rd = skia.Path()                                                             # the rudder swings out to one side
        rd.moveTo(-5, -90)
        rd.lineTo(5, -90)
        rd.lineTo(5 + 46 * rud, -290 * tk)
        rd.lineTo(-5 + 46 * rud, -290 * tk)
        rd.close()
        c.drawPath(rd, P(HILITE if hl == "rud" else "#5EEAD4"))
    c.drawCircle(0, 0, 76, rad_paint(-22, -26, 130, ["#FFFFFF", JETC, "#94A3B8"]))
    c.drawCircle(0, 0, 76, P("#64748B", 0.5, stroke=3))
    c.drawRect(R(-76, 18, 152, 7), P(ACCENT, 0.9))


def screech(d=0.7, seed=50):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    tone = np.sin(2 * np.pi * np.cumsum(1500 - 500 * tt / d + 60 * np.sin(2 * np.pi * 23 * tt)) / sfx.SR)
    nz = sfx._bp(sfx._rng(seed).standard_normal(n), 1200, 5200)
    return sfx._norm((tone * 0.6 + nz * 0.5) * sfx._ar(n, 0.02, d * 0.4), 0.6)


def roar(d=2.0, seed=51):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 90, 1600) + 0.6 * sfx._lp(sfx._rng(seed + 1).standard_normal(n), 220)
    return sfx._norm(x * sfx._ar(n, d * 0.25, d * 0.4), 0.7)


def water_snd(d=0.6, seed=60):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 500, 5000)
    return sfx._norm(x * sfx._env(n, 0.004, d * 0.28), 0.8)


# ====================================================================================== the episode
class Airplane(EpisodeV2):
    BUILD_NO = 11
    FIRST_SET = "cliff"
    CLEAR = "#0B1024"
    TITLE = {"en": "AIRPLANE", "ar_sa": "طيارة"}
    EMPH = {"en": ["CONGRATS", "AIRPLANE", "WINGS", "CLIFF", "NOTHING", "FALLING", "CURVE", "TILT", "UP", "JET", "THIN", "NAP", "PILOT",
                   "SEAL", "OUTFLOW", "SODA", "WOBBLES", "PAPER", "RUDDER", "ELEVATORS", "AILERONS", "LAND", "BRAKES", "FLAPS", "GEAR",
                   "REVERSERS", "FOLLOW", "FIREWORKS", "WINDOWS", "PRETZELS", "ORANGE", "ZERO", "YOURSELF", "ARMREST", "SCIENCE"],
            "ar_sa": ["مبروك", "طيارة", "جنحان", "جرف", "شي", "يطيح", "فتقوّس", "وتميّلها", "لفوق", "النفاث", "يخف", "غفوة", "الطيار",
                      "فتقفّل", "بلف", "غازية", "تتمايل", "ورق", "دفّة", "وروافع", "وجنيحات", "النزول", "فرامل", "قلابات", "وعجلات",
                      "وعاكسات", "تابعني", "نارية", "شبابيك", "مكسرات", "برتقالي", "وصفر", "بيدك", "ومسند", "العلم"]}
    KEYS = {"ar_sa": {
        ("hook", "GLUE"): "لزّقت", ("hook", "BUS"): "باص", ("hook", "DRIVE"): "وسقته", ("hook", "CLIFF"): "جرف", ("hook", "CONGRATS"): "مبروك",
        ("break1", "FLAT"): "المسطحة", ("break1", "NOTHING"): "شي", ("break1", "FALLING"): "يطيح", ("break1", "STEPS"): "زيادة",
        ("fix1", "CURVE"): "فتقوّس", ("fix1", "TILT"): "وتميّلها", ("fix1", "PUSH"): "تدف", ("fix1", "DOWN"): "لتحت", ("fix1", "UP"): "لفوق",
        ("fix1", "JET"): "ومحركات", ("fix1", "COMING"): "يجي",
        ("break2", "FLIES"): "تطير", ("break2", "THIN"): "يخف", ("break2", "MINUTE"): "دقيقة", ("break2", "NAP"): "غفوة", ("break2", "PILOT"): "الطيار",
        ("fix2", "SEAL"): "فتقفّل", ("fix2", "PUMP"): "وتضخ", ("fix2", "ENGINES"): "المحركات", ("fix2", "OUTFLOW"): "بلف",
        ("fix2", "SODA"): "علبة", ("fix2", "SEATS"): "كراسي",
        ("break3", "WOBBLES"): "تتمايل", ("break3", "PAPER"): "ورق", ("break3", "BENT"): "معوج",
        ("fix3", "TAIL"): "ذيل", ("fix3", "RUDDER"): "دفّة", ("fix3", "ELEVATORS"): "وروافع", ("fix3", "UP"): "فوق", ("fix3", "DOWN"): "وتحت",
        ("fix3", "AILERONS"): "وجنيحات", ("fix3", "ROLL"): "تقلبه",
        ("break4", "STEERS"): "تتوجه", ("break4", "LAND"): "النزول", ("break4", "TWICE"): "بضعف", ("break4", "BRAKES"): "فرامل",
        ("fix4", "FLAPS"): "قلابات", ("fix4", "SLOWER"): "أبطأ", ("fix4", "GEAR"): "وعجلات", ("fix4", "BRAKES"): "بفرامل",
        ("fix4", "REVERSERS"): "وعاكسات", ("fix4", "FORWARD"): "لقدام",
        ("cta", "SEATBELT"): "الحزام", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "WINDOWS"): "شبابيك", ("reveal", "PRETZELS"): "مكسرات", ("reveal", "BLACK"): "وصندوق", ("reveal", "ORANGE"): "برتقالي",
        ("stat", "TWO"): "جناحين", ("stat", "THREE"): "ثلاث", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "ARMREST"): "ومسند", ("tag", "NOBODY"): "محد", ("tag", "SCIENCE"): "العلم", ("tag", "ANSWER"): "جواب"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: fireworks"),
                   "stat": [("2", "WINGS"), ("300", "SEATS"), ("0", "LEGROOM")],
                   "L": {"wing": "FLAT WINGS", "foil": "CURVED + TILTED", "lift": "LIFT", "airdn": "AIR GOES DOWN", "eng": "JET ENGINE",
                         "alt": "ALTITUDE", "oxy": "AIR TO BREATHE", "cab": "CABIN AIR", "valve": "OUTFLOW VALVE",
                         "can": "A SODA CAN WITH SEATS", "rud": "RUDDER", "elev": "ELEVATORS", "ail": "AILERONS", "speed": "SPEED",
                         "flaps": "FLAPS", "gear": "LANDING GEAR", "rev": "THRUST REVERSERS", "box": "THE BLACK BOX",
                         "sci": "SCIENCE: NO ANSWER"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: ألعاب نارية"),
                      "stat": [("2", "جناحين"), ("300", "كرسي"), ("0", "مساحة")],
                      "L": {"wing": "جنحان مسطحة", "foil": "مقوّس ومايل", "lift": "رفع", "airdn": "الهوا ينزل تحت", "eng": "محرك نفاث",
                            "alt": "الارتفاع", "oxy": "هوا للتنفس", "cab": "هوا الكبينة", "valve": "بلف الزايد",
                            "can": "علبة غازية بكراسي", "rud": "الدفّة", "elev": "الروافع", "ail": "الجنيحات", "speed": "السرعة",
                            "flaps": "القلابات", "gear": "العجلات", "rev": "عاكسات الدفع", "box": "الصندوق الأسود",
                            "sci": "العلم: بدون جواب"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "glue": ("hook", "GLUE", 0.12), "bus": ("hook", "BUS", 0.3), "drive": ("hook", "DRIVE", 0.4), "cliff": ("hook", "CLIFF", 0.58),
            "congrats": ("hook", "CONGRATS", 0.63),
            "flat": ("break1", "FLAT", 0.1), "nothing": ("break1", "NOTHING", 0.35), "falling": ("break1", "FALLING", 0.7), "steps": ("break1", "STEPS", 0.95),
            "curve": ("fix1", "CURVE", 0.08), "tilt": ("fix1", "TILT", 0.2), "push": ("fix1", "PUSH", 0.43), "down": ("fix1", "DOWN", 0.5),
            "up": ("fix1", "UP", 0.67), "jet": ("fix1", "JET", 0.76), "coming": ("fix1", "COMING", 0.95),
            "flies": ("break2", "FLIES", 0.1), "thin": ("break2", "THIN", 0.32), "minute": ("break2", "MINUTE", 0.52), "nap": ("break2", "NAP", 0.76),
            "pilot": ("break2", "PILOT", 0.94),
            "seal": ("fix2", "SEAL", 0.09), "pump": ("fix2", "PUMP", 0.25), "engines": ("fix2", "ENGINES", 0.45), "outflow": ("fix2", "OUTFLOW", 0.66),
            "soda": ("fix2", "SODA", 0.82), "seats": ("fix2", "SEATS", 0.95),
            "wobbles": ("break3", "WOBBLES", 0.18), "paper": ("break3", "PAPER", 0.55), "bent": ("break3", "BENT", 0.84),
            "tail": ("fix3", "TAIL", 0.15), "rudder": ("fix3", "RUDDER", 0.24), "elevators": ("fix3", "ELEVATORS", 0.45), "up2": ("fix3", "UP", 0.63),
            "down2": ("fix3", "DOWN", 0.68), "ailerons": ("fix3", "AILERONS", 0.78), "roll": ("fix3", "ROLL", 0.96),
            "steers": ("break4", "STEERS", 0.14), "land": ("break4", "LAND", 0.5), "twice": ("break4", "TWICE", 0.6), "brakes": ("break4", "BRAKES", 0.92),
            "flaps": ("fix4", "FLAPS", 0.17), "slower": ("fix4", "SLOWER", 0.3), "gear": ("fix4", "GEAR", 0.44), "brakes2": ("fix4", "BRAKES", 0.52),
            "reversers": ("fix4", "REVERSERS", 0.67), "forward": ("fix4", "FORWARD", 0.92),
            "seatbelt": ("cta", "SEATBELT", 0.32), "follow": ("cta", "FOLLOW", 0.44),
            "windows": ("reveal", "WINDOWS", 0.27), "pretzels": ("reveal", "PRETZELS", 0.47), "black": ("reveal", "BLACK", 0.7), "orange": ("reveal", "ORANGE", 0.92),
            "s1": ("stat", "TWO", 0.04), "s2": ("stat", "THREE", 0.33), "s3": ("stat", "ZERO", 0.68),
            "cong2": ("closer", "CONGRATS", 0.16),
            "armrest": ("tag", "ARMREST", 0.17), "nobody": ("tag", "NOBODY", 0.3), "science": ("tag", "SCIENCE", 0.66), "answer": ("tag", "ANSWER", 0.88)})
        T["edge"] = max(T["cliff"] + 0.05, T["drive"] + 0.5)         # the wheels leave the cliff
        T["impact"] = min(T["steps"], e("break1") - 0.35)           # the lake
        T["asleep"] = T["nap"] - 0.1
        T["touch1"] = T["land"]                                     # break 4: belly on the runway
        T["off"] = max(T["brakes"] - 0.1, T["touch1"] + 1.0)        # ... and off the far end of it
        T["touch2"] = max(T["brakes2"] - 0.35, T["gear"] + 0.35)    # fix 4: wheels on the runway
        T["stop"] = T["forward"] + 0.35
        T["off2"] = T["s1"] - 0.5                                   # the finished airliner starts its take-off run
        self.cut(s("fix1") - 0.12, "foil", 1)
        self.cut(s("break2") - 0.1, "cruise", -1)
        self.cut(s("break3") - 0.1, "rear", 1)
        self.cut(s("break4") - 0.12, "runway", -1)
        self.cut(s("fix4") - 0.12, "runway", 1)
        self.cut(s("cta") + 0.05, "final", -1)
        self.cut(s("tag") - 0.2, "cabin", 1)
        self.cams = {"cliff": Camera(-130, -200, 1.1), "cruise": Camera(0, 138, 1.45), "final": Camera(-40, -216, 1.25)}
        cm = self.cams
        cm["cliff"].key(0.05, -150, -190, 1.22, 1.3).key(T["drive"] - 0.1, 60, -190, 1.2, T["edge"] - T["drive"] + 0.1)
        cm["cruise"].key(s("break2") - 0.1, 0, 120, 1.7, 0.0).key(T["asleep"] - 0.6, 0, 96, 2.05, 1.0)
        cm["cruise"].key(s("fix2") - 0.1, -30, 150, 1.3, 0.5).key(T["outflow"] - 0.35, -90, 130, 1.5, 0.7).key(T["soda"] - 0.3, -30, 150, 1.3, 0.6)
        cm["final"].key(s("cta") + 0.05, -40, -216, 1.25, 0.0).key(s("reveal") - 0.1, 0, -230, 1.18, 0.8)
        cm["final"].key(T["black"] - 0.35, -200, -180, 1.5, 0.6).key(T["s1"] - 0.4, 60, -400, 0.72, 1.0).key(s("closer"), 90, -400, 0.76, 2.2)
        # ---- the wing in the wind
        self.curve = Track(0.0).to(T["curve"] - 0.05, 1.0, 0.45, e_io)
        self.tilt = Track(0.0).to(T["tilt"] - 0.05, 1.0, 0.5, e_io)
        self.wind = Track(1.0).to(T["jet"], 2.4, 0.6)
        # ---- cruise
        self.alt = Track(0.34).to(s("break2"), 0.74, max(1.0, T["thin"] - s("break2") + 0.3))
        self.cabair = Track(0.15).to(T["pump"] + 0.2, 1.0, max(0.8, T["engines"] - T["pump"] + 0.6))
        # ---- controls (rear view): what the stick does
        tr, te, ta = T["rudder"], T["elevators"], T["ailerons"]
        self.rud = Track(0.0).to(tr + 0.1, 1.0, 0.25).to(tr + 0.5, -1.0, 0.35).to(te - 0.15, 0.0, 0.2)
        self.elev = Track(0.0).to(T["up2"] - 0.15, 1.0, 0.22).to(T["down2"] - 0.05, -1.0, 0.3).to(ta - 0.2, 0.0, 0.2)
        self.ail = Track(0.0).to(ta + 0.25, 1.0, 0.25).to(T["roll"] - 0.1, -1.0, 0.4).to(T["roll"] + 0.45, 0.0, 0.3)
        # ---- landing
        self.flapk = Track(0.0).to(T["flaps"], 1.0, 0.45)
        self.geark = Track(0.0).to(T["gear"] - 0.35, 1.0, 0.4)
        self.revk = Track(0.0).to(T["reversers"] - 0.1, 1.0, 0.3).to(T["stop"] + 0.2, 0.0, 0.3)
        self.spans = [(T["falling"] - 0.4, T["coming"]), (T["asleep"], T["seats"] - 0.3), (T["wobbles"], T["roll"] + 0.3),
                      (T["off"], T["stop"])]
        self.shakes = [(T["glue"], 0.2, 8), (T["impact"], 0.6, 24), (T["seal"], 0.25, 8), (T["touch1"], 0.6, 20), (T["off"], 0.5, 16),
                       (T["touch2"], 0.35, 10), (T["tail"], 0.2, 7)]

    # ------------------------------------------------------------------ set: the cliff
    def bus_pose(self, t):
        T = self.T
        if t < T["drive"]:
            return -330.0, -88.0, 0.0
        if t < T["edge"]:
            return lerp(-330, 300, e_in(prog(t, T["drive"], T["edge"]))), -88.0, 0.0
        if t < T["impact"]:
            u = prog(t, T["edge"], T["impact"])
            return (300 + 430 * e_out(u), -88 + (FALL + 40) * u ** 2.3, 62 * e_out(clamp(u * 1.6)) + math.sin(t * 5) * 5 * u)
        v = t - T["impact"]
        return 730.0, FALL - 30 + 50 * math.exp(-v * 3) * math.cos(v * 8), 62 - 50 * e_out(clamp(v * 1.5))

    def draw_cliff(self, c, t):
        T, s = self.T, self.tl.s
        bx, by, rot = self.bus_pose(t)
        cam = self.cams["cliff"].at(t)
        if t >= T["edge"] - 0.2:
            b = e_io(prog(t, T["edge"] - 0.2, T["edge"] + 0.5))
            cam = (lerp(cam[0], bx - 110, b), lerp(cam[1], min(by - 30, FALL - 150), b), lerp(cam[2], 1.45, b))
        cam = (cam[0] + math.sin(t * 0.6) * 4, cam[1], cam[2])
        cx, cy, z = cam
        gy = (FALL - cy) * z + H / 2
        self.backdrop(c, t, cx * 0.2, cy * 0.2, min(gy, H * 1.02))
        falling = T["edge"] + 0.8 <= t < T["impact"]
        if falling:                                                                  # clouds rushing up past the window
            for i in range(3):
                u = ((t - T["edge"]) * (0.55 + 0.12 * i) + i * 0.37) % 1.0
                v2.cloud(c, 420 + i * 260 - 80 * i * i, H * (1.25 - 1.6 * u), 0.9 + 0.2 * i, a=0.75, seed=20 + i)
        self.view(c, cam)
        c.save()
        c.translate(0, FALL)
        sea(c, 200, 4200, t)
        c.restore()
        vrect(c, -3000, 0, 3240, FALL + 900, ["#4A4674", "#2F2C52", "#1B1936"], [0.0, 0.3, 1.0])     # the cliff
        c.drawRect(R(-3000, -10, 3246, 16), P("#3F7A4E"))
        c.drawRect(R(232, 6, 9, FALL + 900), P("#9C93C9", 0.45))
        rng = random.Random(4)
        yy = 90.0
        while yy < FALL + 200:
            wdt = rng.uniform(30, 150)
            c.drawRRect(rr(240 - wdt, yy, wdt + rng.uniform(4, 26), rng.uniform(10, 22), 6), P("#000000" if rng.random() < 0.6 else "#B7AEE0", 0.22))
            yy += rng.uniform(60, 150)
        if t < T["edge"] + 1.2:                                                      # the crew, on top
            went = prog(t, T["edge"], T["edge"] + 0.8)
            pose = "stand" if t < T["glue"] else "cheer" if t < T["edge"] + 0.5 else "look"
            self.crew(c, t, pose, xs=(lerp(-610, 40, e_out(went)), lerp(-566, 96, e_out(went)), lerp(-522, 152, e_out(went))), face=1)
        c.save()
        c.translate(bx, by)
        c.rotate(rot)
        bus(c, t, wings=prog(t, T["glue"] - 0.12, T["glue"] + 0.12))
        c.restore()
        if t < T["drive"] + 0.4 and t >= T["drive"]:
            v2.smoke(c, bx - 190, -20, t, T["drive"], T["edge"], rate=24, life=0.8, spread=(-160, -30), rise=-40, size=(14, 46), col="#B7AEE0",
                     lit=None, lit_until=0, seed=3, a=0.6)
        if t >= T["impact"]:
            splash(c, 730, FALL, t, T["impact"], 1.3, n=44, speed=980, width=2.0)
            splash(c, 700, FALL, t, T["impact"] + 0.1, 1.1, n=26, speed=700, width=1.5, seed=9)
        c.restore()
        if falling:
            v2.speed_streaks(c, W, H, t, 0.5 * prog(t, T["edge"] + 0.8, T["edge"] + 1.6), ang=270, seed=7, n=30)
        self.ui["cam"] = cam
        self.ui["bus"] = (bx, by)

    # ------------------------------------------------------------------ set: one wing in the wind
    def draw_foil(self, c, t):
        T = self.T
        cv, tl_, wind = self.curve.at(t), self.tilt.at(t), self.wind.at(t)
        sky_set(c, t, 0.4, hy=H * 1.2, speed=260 * wind, seed=3)
        cam = (0, 40, 1.22)
        self.view(c, cam)
        k = cv * tl_
        for j in range(12):                                                          # the air, drawn as stream lines
            y0 = -330 + j * 60
            if abs(y0) < 20:
                continue
            path = skia.Path()
            for i, x in enumerate(range(-700, 701, 28)):
                sg = -1 if y0 < 0 else 1
                d1 = sg * 74 * math.exp(-(y0 / 110) ** 2) * math.exp(-(x / 250) ** 2)
                sm = clamp((x + 80) / 460)
                d2 = k * 170 * sm * sm * (3 - 2 * sm) * math.exp(-(y0 / 430) ** 2)
                yy = y0 + d1 + d2
                path.moveTo(x, yy) if i == 0 else path.lineTo(x, yy)
            c.drawPath(path, dash_paint("#BFE4FF", 0.55, 5, t * 7 * wind, dash=36, gap=30))
        if t >= T["jet"] - 0.1:                                                      # the engine under the wing
            ek = e_back(prog(t, T["jet"] - 0.1, T["jet"] + 0.2))
            c.save()
            c.translate(-30, 112)
            c.scale(-1, 1)                                                           # (here the wind comes from the left)
            nacelle(c, 0, 0, 2.3 * ek, 0.0, 1.0, t)
            c.restore()
            c.drawRect(R(-30, 30, 22, 44), P("#94A3B8"))
        c.save()
        c.rotate(9 * tl_)
        flat = 1 - cv
        if flat > 0:
            c.drawRRect(rr(-270, -15, 540, 30, 10), P(WINGC, flat))
        if cv > 0:
            af = skia.Path()
            af.moveTo(270, 4)
            af.cubicTo(120, -64 * cv, -170, -92 * cv, -262, -16)
            af.cubicTo(-292, 6, -250, 30, -200, 30)
            af.cubicTo(-60, 36, 130, 18, 270, 4)
            af.close()
            c.drawPath(af, lin_paint(0, -90, 0, 36, [("#FFFFFF", cv), (WINGC, cv), ("#64748B", cv)]))
            c.drawPath(af, P("#F8FAFC", 0.8 * cv, stroke=3))
        c.restore()
        c.restore()
        self.ui["cam"] = cam

    # ------------------------------------------------------------------ set: high up
    def draw_cruise(self, c, t):
        T, s = self.T, self.tl.s
        alt = self.alt.at(t)
        sky_set(c, t, alt, hy=H * (1.02 + 0.5 * alt), speed=220, seed=5, cl=0.9)
        cam = self.cams["cruise"].at(t)
        sealed = t >= T["seal"] - 0.1
        rng = random.Random(8)
        for i in range(int(lerp(70, 10, clamp((alt - 0.34) / 0.4)))):                # air: fewer and fewer bits of it
            px = (rng.uniform(0, W) - t * rng.uniform(200, 420)) % W
            c.drawCircle(px, rng.uniform(220, 1220), rng.uniform(2, 4), P("#E0F2FE", 0.5))
        self.view(c, cam)
        asleep = prog(t, T["asleep"], T["asleep"] + 0.4) if not sealed else 0.0
        pilot_out = prog(t, T["pilot"] - 0.15, T["pilot"] + 0.2) if not sealed else 0.0
        droop = e_io(prog(t, T["pilot"], T["pilot"] + 1.2)) if not sealed else 0.0
        c.save()
        c.translate(0, math.sin(t * 1.4) * 6 + 70 * droop)
        c.rotate(-5 * (1 - droop) + 9 * droop if not sealed else math.sin(t * 1.1) * 1.2)

        def riders(c, t, xs, floor, awake=True, pilot_x=118):
            for i, px in enumerate(xs):
                slump = 0.0 if awake else asleep
                c.save()
                c.translate(px, floor)
                c.rotate(16 * slump)
                person(c, 0, 0, 62, KIDS[i % 4], t + i, "sit" if not (awake and t >= T["seats"] - 0.4) else "cheer", face=1, hat=("cap", "none")[i % 2])
                c.restore()
                if slump > 0.5:
                    u = (t * 0.7 + i * 0.3) % 1.0
                    text(c, "z", px + 16 + u * 16, floor - 74 - u * 34, 18 + 10 * u, "#DCE7FF", "Poppins-Black", a=1 - u)
            c.save()
            c.translate(pilot_x, floor)
            c.rotate(18 * (0.0 if awake else pilot_out))
            engineer(c, 0, 0, 66, SHIRTS[1], t, "sit", face=1)
            c.restore()
            if not awake and pilot_out > 0.5:
                u = (t * 0.7 + 0.15) % 1.0
                text(c, "z", pilot_x + 18 + u * 16, floor - 78 - u * 34, 18 + 10 * u, HILITE, "Poppins-Black", a=1 - u)

        if not sealed:
            bus(c, t, wings=1.0, good=1.0, eng=1.0, cut=1.0, power=1.0 - 0.6 * droop)
            riders(c, t, (-136, -76, -16, 44), 30, awake=False)
        else:
            sk = e_back(prog(t, T["seal"] - 0.1, T["seal"] + 0.25))
            c.scale(lerp(0.7, 1.0, sk), sk)

            def inner(c, t):
                air = self.cabair.at(t)
                rng2 = random.Random(3)
                for _ in range(int(60 * air)):
                    px = -240 + (rng2.uniform(0, 450) + t * rng2.uniform(-20, 20)) % 450
                    c.drawCircle(px, rng2.uniform(-44, 18) + math.sin(t * 2 + px) * 3, 2.5, P("#BAE6FD", 0.55))
                c.drawLine(-230, -46, 200, -46, P("#38BDF8", 0.85, stroke=5))          # the air duct in the ceiling
                riders(c, t, (-190, -130, -70, -10, 50, 110), 24, awake=True, pilot_x=176)

            jet(c, t, tail=0.0, cut=1.0, power=1.0, inner=inner)
            if t >= T["pump"] - 0.1:                                                 # bleed air: engine -> cabin
                pk = prog(t, T["pump"] - 0.1, T["pump"] + 0.25)
                pipe = skia.Path()
                pipe.moveTo(-10, 66)
                pipe.lineTo(-10, lerp(66, -46, pk))
                c.drawPath(pipe, P("#0B1220", 0.8, stroke=12))
                c.drawPath(pipe, dash_paint("#7DD3FC", 1.0, 7, -t * 5, dash=14, gap=10))
            vk = prog(t, T["outflow"] - 0.2, T["outflow"] + 0.1)
            if vk > 0:                                                               # the outflow valve, low in the tail
                op = 0.5 + 0.5 * math.sin(t * 5)
                c.drawRRect(rr(-286, 34, 30, 12, 4), P("#0B1220", vk))
                c.save()
                c.translate(-286, 46)
                c.rotate(38 * op * vk)
                c.drawRRect(rr(0, -4, 30, 7, 3), P(HILITE, vk))
                c.restore()
                for i in range(4):
                    u = (t * 1.4 + i / 4) % 1.0
                    c.drawCircle(-276 - 70 * u, 58 + 44 * u, 5 + 6 * u, P("#BAE6FD", 0.6 * (1 - u) * vk))
            tab = e_back(prog(t, T["soda"] - 0.05, T["soda"] + 0.2))
            if tab > 0:                                                              # ... a soda can
                c.drawOval(R(20 - 30 * tab, -86, 60 * tab, 24 * tab), P("#94A3B8", 1, stroke=7))
                c.drawRect(R(16, -70, 8, 10), P("#94A3B8"))
        c.restore()
        c.restore()
        self.ui["cam"] = cam

    # ------------------------------------------------------------------ set: from behind
    def draw_rear(self, c, t):
        T, s = self.T, self.tl.s
        sky_set(c, t, 0.45, hy=H * 1.05, speed=30, seed=9)
        fixed = t >= T["tail"] - 0.15
        if not fixed:
            w = prog(t, s("break3"), s("break3") + 0.4)
            roll = (24 * math.sin(t * 3.3) + 9 * math.sin(t * 7.7)) * w
            ox, oy = 46 * math.sin(t * 2.1) * w, 30 * math.sin(t * 2.9) * w
        else:
            settle = 1 - prog(t, T["tail"] - 0.15, T["tail"] + 0.35)
            roll = 24 * math.sin(t * 3.3) * settle + 20 * self.ail.at(t - 0.08)
            ox, oy = -70 * self.rud.at(t - 0.1), -60 * self.elev.at(t - 0.1)
        hl = None
        if fixed:
            hl = "rud" if T["rudder"] - 0.1 <= t < T["elevators"] - 0.2 else "elev" if T["elevators"] - 0.2 <= t < T["ailerons"] - 0.2 else \
                "ail" if t >= T["ailerons"] - 0.2 else None
        cam = (0, 240, 1.12)
        self.view(c, cam)
        c.save()
        c.translate(ox, 60 + oy)
        c.rotate(roll)
        rear(c, t, prog(t, T["tail"] - 0.15, T["tail"] + 0.15), self.rud.at(t), self.elev.at(t), self.ail.at(t), hl)
        c.restore()
        if T["paper"] - 0.3 <= t < T["tail"]:                                        # like a paper plane with a bent wing
            u = prog(t, T["paper"] - 0.3, T["tail"])
            px, py = lerp(520, 150, u) + math.sin(t * 6) * 40, -420 + 260 * u + math.cos(t * 5) * 50
            c.save()
            c.translate(px, py)
            c.rotate(t * 260)
            pp = skia.Path()
            pp.moveTo(0, -44)
            pp.lineTo(36, 34)
            pp.lineTo(0, 16)
            pp.lineTo(-36, 34)
            pp.close()
            c.drawPath(pp, P("#F8FAFC"))
            c.drawLine(0, -44, 0, 16, P("#94A3B8", 1, stroke=2))
            c.drawLine(36, 34, 54, 16, P("#F8FAFC", 1, stroke=7))
            c.restore()
        c.restore()
        self.ui["cam"] = cam
        self.ui["rear"] = (ox, 60 + oy, roll)

    # ------------------------------------------------------------------ set: the runway
    def run_pose(self, t):
        """x of the airliner, its height above the runway, its pitch."""
        T, s = self.T, self.tl.s
        if t < s("fix4") - 0.12:
            t0 = s("break4") - 0.12
            if t < T["touch1"]:
                u = prog(t, t0, T["touch1"])
                return lerp(-2500, -700, u), 330 * (1 - u) ** 1.6, -3.0
            u = prog(t, T["touch1"], T["off"] + 0.9)
            return lerp(-700, 2350, 1 - (1 - u) ** 1.5), 0.0, 0.0
        t0 = s("fix4") - 0.12
        if t < T["touch2"]:
            u = prog(t, t0, T["touch2"])
            return lerp(-1900, -620, u), 300 * (1 - u) ** 1.5, -4.0
        u = prog(t, T["touch2"], T["stop"])
        return lerp(-620, 520, 1 - (1 - u) ** 2.2), 0.0, 0.0

    def draw_runway(self, c, t):
        T, s = self.T, self.tl.s
        first = t < s("fix4") - 0.12
        px, hgt, pitch = self.run_pose(t)
        z = 1.0 if first else 1.22
        cam = (px + (160 if first else 60) + math.sin(t * 0.6) * 4, -270 / z - (hgt * 0.35), z)
        cx, cy, _ = cam
        gy = (0 - cy) * z + H / 2
        self.backdrop(c, t, cx * 0.3, cy, gy)
        self.view(c, cam)
        v2.ground(c, cx - 900, cx + 900, surface="#2F6B46")
        c.drawRect(R(-3400, -4, 4900, 26), P("#1B2238"))                             # the runway
        for mx in range(-3300, 1500, 180):
            c.drawRect(R(mx, 4, 90, 6), P("#F8FAFC", 0.8))
        for lx in range(-3300, 1500, 120):
            c.drawCircle(lx, -8, 5, P("#FDE68A"))
            add_glow(c, lx, -8, 22, "#FDE68A", 0.6)
        for i in range(6):                                                           # the far end: red lights, then grass
            c.drawCircle(1500 + i * 14, -10, 7, P("#FF4D4F"))
            add_glow(c, 1500 + i * 14, -10, 30, "#FF4D4F", 0.8)
        gear = 0.0 if first else self.geark.at(t)
        down = gear * 70
        squat = bump(t, T["touch2"], T["touch2"] + 0.45) if not first else 0.0
        c.save()
        c.translate(px, -64 - hgt - down + 8 * squat - (0 if not first else -2))
        c.rotate(pitch)
        jet(c, t, tail=1.0, gear=gear, squat=squat, flaps=0.0 if first else self.flapk.at(t), rev=0.0 if first else self.revk.at(t),
            power=0.9 if (first or t < T["touch2"]) else 0.2,
            hot=0.0 if first else prog(t, T["brakes2"] - 0.05, T["brakes2"] + 0.3) * (1 - prog(t, T["stop"], T["stop"] + 0.8)))
        c.restore()
        if first and t >= T["touch1"]:                                               # on its belly, far too fast
            for i in range(9):
                t0 = T["touch1"] + i * 0.16
                if t0 <= t < t0 + 0.5 and px < 1500:
                    sparks_shower(c, px - 40 + i * 7, -2, t, t0, 0.5, n=14, speed=560, seed=i, cone=(150, 215))
            if t >= T["off"]:
                v2.smoke(c, px - 100, -10, t, T["off"], T["off"] + 0.7, rate=30, life=1.4, spread=(-260, -60), rise=-70, size=(30, 110),
                         col="#7C6F57", lit=None, lit_until=0, seed=5, a=0.8)
                v2.debris(c, px - 60, -6, t, T["off"], 1.2, n=12, speed=520, seed=6, cols=("#3F7A4E", "#2F6B46", "#5B4A2E"), floor=0, size=(8, 22))
        if not first:
            rv = self.revk.at(t)
            if rv > 0.3:                                                             # engine air thrown forward
                for i in range(5):
                    u = (t * 2.2 + i / 5) % 1.0
                    ax = px - 60 + 150 * u
                    c.drawLine(ax, 26 - 30 * u, ax + 34, 20 - 36 * u, P("#FDBA74", (1 - u) * 0.9 * rv, stroke=7))
            if T["touch2"] <= t < T["touch2"] + 0.5:
                v2.smoke(c, px - 36, 0, t, T["touch2"], T["touch2"] + 0.12, rate=60, life=0.7, spread=(-200, -30), rise=-60, size=(14, 60),
                         col="#CBD5E1", lit=None, lit_until=0, seed=7, a=0.7)
        c.restore()
        self.ui["cam"] = cam
        self.ui["plane"] = (px, -64 - hgt - down)
        self.ui["speed"] = (1.0 if first else lerp(0.95, 0.5, self.flapk.at(t)) * (1 - 0.92 * e_out(prog(t, T["touch2"], T["stop"]))))
        if first:
            self.ui["speed"] = lerp(1.0, 0.82, prog(t, T["touch1"], T["off"] + 0.9))

    # ------------------------------------------------------------------ set: the finished airliner
    def draw_final(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["final"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 4, cam[1], cam[2])
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        self.backdrop(c, t, cx * 0.4, cy, gy)
        self.view(c, cam)
        v2.ground(c, -3400, 3400, surface="#3A4258")
        skyline_night(c, -1400, 1400, 0.0, seed=4, hmin=90, hmax=230, lit=0.45, t=t)
        c.drawRect(R(-3400, -4, 6800, 6), P("#FDE68A", 0.35))
        go = t >= T["off2"]
        up = e_io(prog(t, T["off2"] + 0.45, T["off2"] + 3.8)) if go else 0.0
        px, py = 170 * e_in(prog(t, T["off2"], T["off2"] + 0.7)) + 330 * up, -134 - 590 * up
        c.save()
        c.translate(px, py)
        c.rotate(-13 * math.sin(clamp(up * 1.25) * math.pi) - 4 * up)
        c.scale(1 - 0.42 * up, 1 - 0.42 * up)
        jet(c, t, tail=1.0, gear=1 - prog(t, T["off2"] + 1.3, T["off2"] + 1.9) if go else 1.0, win=prog(t, T["windows"] - 0.05, T["windows"] + 0.55),
            power=0.9 if go else 0.0, box=prog(t, T["black"] - 0.1, T["black"] + 0.2) * (1 - prog(t, T["s1"] - 0.5, T["s1"] - 0.3)))
        c.restore()
        if not go:
            c.drawRect(R(170, -124, 8, 124), P("#64748B"))                           # the stairs to the door
            for i in range(6):
                c.drawRect(R(178 + i * 18, -118 + i * 20, 24, 6), P("#94A3B8"))
            c.drawLine(178, -124, 292, 0, P("#64748B", 1, stroke=5))
        closing = t >= s("closer") - 0.2
        xs = (-330, -276, -222) if not closing else (-330, -276, -222)
        pose = "stand" if t < T["windows"] else "cheer" if (t < T["pretzels"] or closing or go) else "look"
        self.crew(c, t, pose, xs=xs, face=1)
        if closing:
            hats_in_the_air(c, xs, -150, t, T["cong2"])
        if T["pretzels"] - 0.1 <= t < T["s1"] - 0.3:                                  # one tiny bag of snacks
            pk = e_back(prog(t, T["pretzels"] - 0.1, T["pretzels"] + 0.15))
            uu = e_io(prog(t, T["pretzels"] + 0.2, T["pretzels"] + 0.9))
            bx, by = lerp(187, -276, uu), lerp(-190, -190, uu) - 170 * math.sin(uu * math.pi)
            c.save()
            c.translate(bx, by)
            c.rotate(uu * 360)
            c.scale(pk, pk)
            c.drawRRect(rr(-15, -19, 30, 38, 5), P("#EF4444"))
            c.drawRect(R(-15, -19, 30, 6), P("#FCA5A5"))
            c.drawCircle(-4, 2, 5, P("#FDE68A", 1, stroke=3))
            c.drawCircle(5, 2, 5, P("#FDE68A", 1, stroke=3))
            c.restore()
        c.restore()
        self.ui["cam"] = cam
        self.ui["plane"] = (px, py)

    # ------------------------------------------------------------------ set: row 23, seats A B C
    def draw_cabin(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#1F2A44", "#2B3A5C", "#141B30"], [0.0, 0.5, 1.0])
        cam = (0, -300, 1.0 + 0.06 * e_io(prog(t, self.tl.s("tag") - 0.2, self.tl.s("tag") + 2.5)))
        self.view(c, cam)
        box(c, -700, -900, 1400, 150, "#CBD5E1", r=20)                               # overhead bins
        for bx in (-470, -160, 150, 460):
            c.drawRRect(rr(bx - 140, -880, 280, 110, 14), P("#94A3B8", 0.5, stroke=3))
        for wx in (-430, -150, 130, 410):                                            # tiny windows
            c.drawRRect(rr(wx - 34, -640, 68, 96, 30), P("#E2E8F0"))
            vrect(c, wx - 26, -632, 52, 80, ["#1B1C4A", "#74406F", "#FF9D73"], r=24)
        fight = math.sin(t * 9)
        for i, sx in enumerate((-290, 0, 290)):                                      # three seats
            c.drawRRect(rr(sx - 126, -470, 252, 470, 40), lin_paint(0, -470, 0, 0, ["#3B5BA9", "#2A4380", "#1B2C5A"]))
            c.drawRRect(rr(sx - 84, -520, 168, 90, 28), P("#4C6FC7"))
            c.drawRRect(rr(sx - 60, -506, 120, 60, 18), P("#F1F5F9", 0.85))
        people = ((-290, SHIRTS[0], 1), (0, SHIRTS[1], 0), (290, SHIRTS[2], -1))
        for px, col, sd in people:
            mid = sd == 0
            w_ = 150 if not mid else 104
            c.drawRRect(rr(px - w_ / 2, -330, w_, 300, 50), lin_paint(px - w_ / 2, 0, px + w_ / 2, 0, [shade(col, 0.2), col, shade(col, -0.3)]))
            c.drawRect(R(px - w_ / 2, -210, w_, 26), P("#F8FAFC", 0.8))
            hy = -410 + (6 * math.sin(t * 3 + px) if not mid else 4 * fight)
            c.drawCircle(px, hy, 62, rad_paint(px - 18, hy - 20, 100, ["#F2C7A0", "#E8B48A", "#B98562"]))
            dome = skia.Path()
            dome.moveTo(px - 68, hy - 10)
            dome.cubicTo(px - 68, hy - 104, px + 68, hy - 104, px + 68, hy - 10)
            dome.close()
            c.drawPath(dome, lin_paint(px - 68, 0, px + 68, 0, ["#FDE68A", "#FACC15", "#CA8A04"]))
            c.drawRRect(rr(px - 84, hy - 20, 168, 22, 10), P("#EAB308"))
            for ex in (-22, 22):
                c.drawCircle(px + ex, hy + 12, 7, P("#1B1B2B"))
            if mid:
                c.drawArc(R(px - 20, hy + 34, 40, 22), 200, 140, False, P("#7C2D12", 1, stroke=5))
            else:
                c.drawLine(px - 22 * 1, hy + 40, px + 22, hy + 36 + 6 * sd, P("#7C2D12", 1, stroke=5))
        for i, ax in enumerate((-145, 145)):                                         # the two armrests in the middle
            box(c, ax - 30, -250, 60, 250, "#11182B", r=12)
            c.drawRRect(rr(ax - 34, -262, 68, 26, 10), P("#475569"))
            sd = -1 if i == 0 else 1
            push = 16 * fight * sd
            c.save()                                                                 # the neighbour's elbow, well dug in
            c.translate(ax + push * 0.6, -258)
            c.drawRRect(rr(-52 if sd < 0 else -18, -34, 70, 34, 16), P(SHIRTS[0] if i == 0 else SHIRTS[2]))
            c.drawCircle(18 * sd * -1 + (-18 if sd < 0 else 18) * 0, -17, 0, P("#000000", 0))
            c.restore()
            c.save()                                                                 # the middle passenger's elbow
            c.translate(ax - push * 0.6, -258)
            c.drawRRect(rr(-18 if sd < 0 else -52, -30, 70, 30, 15), P(SHIRTS[1]))
            c.restore()
            if t >= T["nobody"]:
                q = e_back(prog(t, T["nobody"] + i * 0.15, T["nobody"] + 0.25 + i * 0.15))
                text(c, "?", ax, -330 - 10 * math.sin(t * 5 + i), 110 * q, HILITE, "Poppins-Black")
        c.restore()
        self.ui["cam"] = cam

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.3, horizon_y=H * 0.8)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    def ui_cliff(self, c, t, tw):
        T, s = self.T, self.tl.s
        bx, by = self.ui.get("bus", (0, 0))
        x0, y0 = self.at(bx - 60, by + 10)
        if tw >= s("break1"):
            self.label(x0, y0, 780, y0 - 300, "wing", T["flat"] + 0.1, T["nothing"] + 0.6, WARN)
        self.badge("alert", T["falling"] - 0.4, s("fix1") - 0.2)
        self.red(T["falling"] - 0.4, 2.0)

    def ui_foil(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, y0 = self.at(-60, -70)
        self.label(x0, y0, 290, y0 - 250, "foil", T["tilt"] + 0.2, T["push"] - 0.1)
        dn = self.span(T["down"] - 0.25, s("break2") - 0.2)
        if dn > 0:                                                                   # air down ...
            ax, ay = self.at(250, 130)
            c.drawLine(ax, ay, ax, ay + 150 * dn, P("#7DD3FC", dn, stroke=16))
            ar = skia.Path()
            ar.moveTo(ax - 34, ay + 150 * dn)
            ar.lineTo(ax + 34, ay + 150 * dn)
            ar.lineTo(ax, ay + 150 * dn + 46)
            ar.close()
            c.drawPath(ar, P("#7DD3FC", dn))
            v2.chip(c, ax - 30, ay - 46, self.L["airdn"], dn, size=30, accent="#7DD3FC")
        up = self.span(T["up"] - 0.25, s("break2") - 0.2)
        if up > 0:                                                                   # ... wing up
            ax, ay = self.at(-90, -120)
            c.drawLine(ax, ay, ax, ay - 170 * up, P(GOOD, up, stroke=18))
            ar = skia.Path()
            ar.moveTo(ax - 38, ay - 170 * up)
            ar.lineTo(ax + 38, ay - 170 * up)
            ar.lineTo(ax, ay - 170 * up - 52)
            ar.close()
            c.drawPath(ar, P(GOOD, up))
            v2.chip(c, ax + 150, ay - 190, self.L["lift"], up, size=44, accent=GOOD)
        ex, ey = self.at(-60, 150)
        self.label(ex, ey + 30, 790, ey + 190, "eng", T["jet"] + 0.25, s("break2") - 0.2, "#FDBA74")
        self.badge("check", T["coming"], s("break2") - 0.15, x=880, y=360)

    def ui_cruise(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.1:
            p = self.span(s("break2") + 0.15, s("fix2") - 0.25)
            alt = self.alt.at(tw)
            if p > 0:
                oxy = clamp(1.05 - (alt - 0.34) / 0.36)
                v2.gauge(c, 60, 250, [(self.L["alt"], clamp((alt - 0.2) / 0.54), "#A78BFA"), (self.L["oxy"], oxy, mix(WARN, GOOD, oxy))], p, w=380)
            self.badge("alert", T["asleep"], s("fix2") - 0.2, x=880, y=330)
            self.red(T["asleep"], 2.0)
        else:
            p = self.span(T["pump"] - 0.1, s("break3") - 0.25)
            if p > 0:
                v2.gauge(c, 60, 250, [(self.L["cab"], self.cabair.at(tw), GOOD if self.cabair.at(tw) > 0.7 else "#F59E0B")], p, w=340)
            vx, vy = self.at(-272, 48)
            self.label(vx, vy, 300, vy + 250, "valve", T["outflow"] + 0.05, T["soda"] - 0.15, HILITE)
            self.chip(540, 470, "can", T["soda"] + 0.1, s("break3") - 0.2, accent=HILITE, size=38)
            self.badge("check", T["seats"] - 0.3, s("break3") - 0.15, x=900, y=330)

    def ui_rear(self, c, t, tw):
        T, s = self.T, self.tl.s
        ox, oy, roll = self.ui.get("rear", (0, 60, 0))
        if tw < T["tail"] - 0.15:
            self.badge("alert", T["wobbles"], T["tail"] - 0.3, x=880, y=360)
            self.red(T["wobbles"], 1.8)
            return
        x0, y0 = self.at(ox, oy - 250)
        self.label(x0 + 10, y0, 800, y0 - 110, "rud", T["rudder"], T["elevators"] - 0.2, HILITE)
        x1, y1 = self.at(ox - 150, oy - 64)
        self.label(x1, y1, 250, y1 - 260, "elev", T["elevators"] - 0.05, T["ailerons"] - 0.2, HILITE)
        x2, y2 = self.at(ox + 400, oy - 16)
        self.label(x2, y2, 800, y2 + 260, "ail", T["ailerons"] + 0.05, s("break4") - 0.3, HILITE)
        self.badge("check", T["roll"] + 0.3, s("break4") - 0.15, x=230, y=1100)

    def ui_runway(self, c, t, tw):
        T, s = self.T, self.tl.s
        first = tw < s("fix4") - 0.12
        t0 = s("break4") + 0.2 if first else s("fix4") + 0.1
        p = self.span(t0, (s("fix4") - 0.25) if first else 1e9)
        if p > 0:
            sp = self.ui.get("speed", 1.0)
            v2.gauge(c, 60, 250, [(self.L["speed"], sp, mix(GOOD, WARN, clamp((sp - 0.3) / 0.5)))], p, w=340)
        if first:
            self.badge("alert", T["off"], s("fix4") - 0.2, x=880, y=330)
            self.red(T["off"], 1.8)
            return
        px, py = self.ui.get("plane", (0, -64))
        x0, y0 = self.at(px - 150, py + 96)
        self.label(x0, y0, 250, y0 - 330, "flaps", T["flaps"] + 0.15, T["gear"] - 0.45)
        x1, y1 = self.at(px - 36, py + 120)
        self.label(x1, y1, 300, y1 - 430, "gear", T["gear"] - 0.2, T["reversers"] - 0.2)
        x2, y2 = self.at(px - 60, py + 86)
        self.label(x2, y2, 760, y2 - 400, "rev", T["reversers"] + 0.1, T["stop"] + 0.3, "#FDBA74")
        self.badge("check", T["stop"], 1e9, x=880, y=330)

    def ui_final(self, c, t, tw):
        T, s = self.T, self.tl.s
        px, py = self.ui.get("plane", (0, -196))
        x0, y0 = self.at(px - 276, py - 20)
        self.label(x0, y0, x0 + 240, y0 - 250, "box", T["black"] + 0.1, T["s1"] - 0.5, "#FB923C")

    def ui_cabin(self, c, t, tw):
        T = self.T
        self.chip(540, 330, "sci", T["science"] - 0.05, self.duration + 1, accent=HILITE, size=44)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (T["glue"] - 0.1, sfx.thud(0.3, 61), -4), (T["glue"] + 0.05, sfx.pop(62), -7),
              (T["drive"], roar(1.2, 63), -8), (T["edge"], sfx.whoosh(0.7, False, 64), -6), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 65), -9)]
        ev += [(T["flat"], sfx.creak(0.6, 66), -9), (T["falling"] - 0.4, sfx.alarm(3, 820), -11), (T["edge"] + 1.2, sfx.whoosh(2.2, False, 67), -11),
               (T["falling"] - 0.3, sfx.whoosh(1.6, False, 68), -10), (T["impact"], water_snd(1.2, 69), 0), (T["impact"] + 0.05, sfx.thud(0.5, 70), -3)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["curve"] - 0.05, sfx.creak(0.5, 72), -6), (T["tilt"] - 0.05, sfx.creak(0.4, 73), -7),
               (T["down"] - 0.25, sfx.pop(74), -6), (T["up"] - 0.25, sfx.charge_up(0.6), -8), (T["jet"] - 0.1, sfx.thud(0.3, 75), -5),
               (T["jet"] + 0.1, roar(1.6, 76), -9), (T["coming"], sfx.chime(), -6)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, False, 77), -4), (s("break2"), roar(2.5, 78), -13), (T["thin"], sfx.power_down(1.2, 79), -10),
               (T["asleep"], sfx.alarm(3, 820), -11), (T["pilot"], sfx.womp(), -8)]
        ev += [(T["seal"] - 0.1, sfx.clank(240, 0.5, 80), -3), (T["engines"] + 0.5, gas_hiss(1.0, 81), -13), (T["engines"] + 0.55, sfx.whirr(0.8, 200, 320, 82), -14),
               (T["outflow"] - 0.2, sfx.lock_click(83), -5), (T["soda"] - 0.05, sfx.snap(84), -6), (T["soda"] + 0.1, gas_hiss(0.4, 85), -7),
               (T["seats"] - 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, True, 86), -4), (T["wobbles"], sfx.alarm(3, 820), -11), (T["wobbles"] + 0.1, sfx.creak(0.8, 87), -7),
               (T["paper"] - 0.3, sfx.whoosh(0.6, True, 88), -9)]
        ev += [(T["tail"] - 0.15, sfx.thud(0.3, 89), -4), (T["rudder"] + 0.1, sfx.creak(0.3, 90), -8), (T["rudder"] + 0.5, sfx.creak(0.3, 91), -8),
               (T["elevators"] - 0.2, sfx.pop(92), -6), (T["up2"] - 0.15, sfx.whoosh(0.3, True, 93), -9), (T["down2"] - 0.05, sfx.whoosh(0.3, False, 94), -9),
               (T["ailerons"] - 0.2, sfx.pop(95), -6), (T["ailerons"] + 0.25, sfx.whoosh(0.4, True, 96), -9), (T["roll"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 97), -4), (s("break4"), roar(1.8, 98), -10), (T["touch1"], sfx.thud(0.5, 99), -2),
               (T["touch1"] + 0.05, screech(1.6, 100), -6), (T["off"], boom(0.9, 101), -3), (T["off"] + 0.05, sfx.alarm(3, 820), -10)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 102), -4), (T["flaps"], sfx.whirr(0.6, 180, 260, 103), -8),
               (T["gear"] - 0.35, sfx.whirr(0.4, 140, 200, 104), -8), (T["gear"] + 0.05, sfx.lock_click(105), -4), (T["touch2"], sfx.thud(0.35, 106), -4),
               (T["touch2"] + 0.03, screech(0.5, 107), -9), (T["brakes2"], screech(0.7, 108), -10), (T["reversers"] - 0.1, sfx.clank(300, 0.3, 109), -6),
               (T["reversers"] + 0.1, roar(1.5, 110), -8), (T["stop"], sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(111), 0), (T["follow"] - 0.15, sfx.pop(112), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 113), -7),
               (T["seatbelt"], sfx.ding(), -7)]
        ev += [(T["windows"] - 0.05 + i * 0.035, sfx.tap(114 + i), -12) for i in range(12)]
        ev += [(T["pretzels"] - 0.1, sfx.pop(127), -5), (T["black"] - 0.1, sfx.beep(1500, 0.08), -7), (T["black"] + 0.2, sfx.beep(1500, 0.08), -8),
               (T["orange"], sfx.sparkle(0.5, 6, 128), -9)]
        ev += [(T["off2"], roar(3.2, 129), -10), (T["s1"], sfx.pop(130), -3), (T["s2"], sfx.pop(131), -3), (T["s3"], sfx.pop(132), -3),
               (T["s1"] - 0.3, sfx.whoosh(1.2, True, 133), -12)]
        ev += [(T["cong2"], sfx.pop(134), -2), (T["cong2"], sfx.sparkle(1.0, 14, 135), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 136), -6), (T["armrest"], sfx.thud(0.2, 137), -8), (T["armrest"] + 0.35, sfx.thud(0.2, 138), -8),
               (T["nobody"], sfx.pop(139), -6), (T["nobody"] + 0.15, sfx.pop(140), -7), (T["answer"] + 0.3, sfx.womp(), -3)]
        return ev


NAME = "airplane"
EPISODE = Airplane
