"""Episode 48 - A Moroccan riad.  v2 look: warm afternoon light in the old medina (Fez / Marrakech): ochre mud walls
outside, and inside a courtyard with zellige tiles, carved wood, orange trees and a fountain.

Sets: court (hook: the courtyard with its fountain and orange trees, then the blank street wall slides shut in front
of it and opens again as a cutaway; the reveal: the zellige laid piece by piece, the orange trees, the fountain; the
closer), city (break1: the packed medina from above, alleys barely wider than a donkey, the sun beating down),
section (fix1: the house turned inside out, blank walls to the street and every room opening onto the courtyard;
break2: the sun pours into the courtyard; fix2: taller walls and a narrower courtyard keep it in shade, cool night air
sinks in and stays through the morning), wall (break3: rain melts a mud wall and a bathroom soaks through; fix3: lime
plaster, polished with a river stone, black soap, and water rolls off), door (break4/fix4: the entrance from above, a
passer-by looks straight into the courtyard; the entrance turns a corner and all he sees is a wall), fez (the stat:
old Fez from above, 9,000+ alleys and no cars), tag (the neighbour across the street knows what you had for dinner).
World (court): front view into the courtyard, the far wall's base at y = 0, the floor comes toward the viewer.
World (section): side view, the ground at y = 0, the street on the left, the courtyard in the middle.
"""
from v2_base import *  # noqa: F401,F403
from falaj import word  # noqa: E402
from windtower import sun, arrow, heat_lines, flow  # noqa: E402
from panama import rain  # noqa: E402

AFTERNOON = {"top": "#1E3A8A", "upper": "#2F5DB8", "mid": "#5B8BD9", "low": "#9CC3EE", "horizon": "#F6D7A8",
             "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHT = {"top": "#020617", "upper": "#0B1033", "mid": "#1B1F4F", "low": "#2E2D63", "horizon": "#4B3F72",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
OCHRE, OCHRE_D = "#C98A5A", "#8E5A36"
PINK = "#C9846A"
LIME = "#EADFC8"
ZG = ["#1E5AA8", "#167A5C", "#F2EAD8", "#C2742C", "#0F3B66"]       # zellige colours
LEAF, LEAF_D = "#2F6B3A", "#1C4426"
ORANGE = "#F59E0B"
CEDAR = "#7A4A26"


# ====================================================================================== pieces
def zellige_star(c, x, y, r, a=1.0, k=1.0, cols=None, rot=0.0):
    """One eight-point star tile with its ring of small pieces; k 0..1 = how many pieces are laid."""
    if a <= 0 or k <= 0:
        return
    cols = cols or ZG
    pts = []
    for i in range(16):
        an = math.radians(rot + i * 22.5)
        rr_ = r if i % 2 == 0 else r * 0.62
        pts.append((x + math.cos(an) * rr_, y + math.sin(an) * rr_))
    sp = skia.Path()
    sp.moveTo(*pts[0])
    for p_ in pts[1:]:
        sp.lineTo(*p_)
    sp.close()
    c.drawPath(sp, P(cols[0], a * clamp(k * 3)))
    c.drawCircle(x, y, r * 0.42, P(cols[2], a * clamp(k * 3 - 0.5)))
    c.drawCircle(x, y, r * 0.22, P(cols[3], a * clamp(k * 3 - 1.0)))
    n = 8
    for i in range(n):
        if (i + 1) / float(n) > k:
            break
        an = math.radians(rot + 22.5 + i * 45)
        px, py = x + math.cos(an) * r * 1.05, y + math.sin(an) * r * 1.05
        c.drawCircle(px, py, r * 0.2, P(cols[1], a))
    c.drawPath(sp, P("#F8F1E2", 0.6 * a * clamp(k * 3), stroke=max(1.0, r * 0.06)))


def zellige_band(c, x0, x1, y0, y1, t, a=1.0, k=1.0, seed=0):
    """A wall band of zellige: a row of stars on a dark ground; k lays the pieces left to right."""
    if a <= 0:
        return
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), P("#0F2E4A", a))
    h = y1 - y0
    r = h * 0.36
    n = int((x1 - x0) / (h * 0.95)) + 1
    for i in range(n):
        x = x0 + (i + 0.5) * (x1 - x0) / n
        kk = clamp(k * (n + 2) - i)
        zellige_star(c, x, y0 + h / 2, r, a=a, k=kk, rot=22.5 * (i % 2))
    c.drawLine(x0, y0, x1, y0, P("#E8D9B5", a, stroke=3))
    c.drawLine(x0, y1, x1, y1, P("#E8D9B5", a, stroke=3))


def horseshoe(c, x, y, w, h, fill, a=1.0, trim=None):
    """A horseshoe arch opening, base centred at (x, y)."""
    p_ = skia.Path()
    p_.moveTo(x - w * 0.42, y)
    p_.lineTo(x - w * 0.42, y - h + w * 0.55)
    p_.arcTo(R(x - w / 2, y - h, w, w * 1.1), 160, 220, False)
    p_.lineTo(x + w * 0.42, y)
    p_.close()
    c.drawPath(p_, P(fill, a))
    if trim:
        c.drawPath(p_, P(trim, a, stroke=max(2.0, w * 0.05)))


def orange_tree(c, x, y, s, t, a=1.0, grow=1.0):
    if a <= 0 or grow <= 0:
        return
    s = s * e_out(grow)
    c.drawRect(R(x - 8 * s, y - 120 * s, 16 * s, 120 * s), P("#5B3A22", a))
    c.drawOval(R(x - 70 * s, y - 16 * s, 140 * s, 30 * s), P("#000000", 0.2 * a))
    rng = random.Random(int(x))
    for k in range(7):
        cx_ = x + rng.uniform(-60, 60) * s
        cy_ = y - 150 * s + rng.uniform(-50, 40) * s
        c.drawCircle(cx_, cy_, rng.uniform(40, 60) * s, P(LEAF if k % 2 else shade(LEAF, 0.1), a))
    for k in range(14):
        c.drawCircle(x + rng.uniform(-70, 70) * s, y - 150 * s + rng.uniform(-60, 50) * s, 8 * s, P(ORANGE, a))


def fountain(c, x, y, s, t, a=1.0, jet=1.0):
    """The courtyard fountain: a round zellige basin seen from the front, a jet of water."""
    c.drawOval(R(x - 170 * s, y - 40 * s, 340 * s, 80 * s), P("#0F2E4A", a))
    c.drawOval(R(x - 150 * s, y - 32 * s, 300 * s, 58 * s), lin_paint(0, y - 32 * s, 0, y + 26 * s, ["#7DD3FC", "#0369A1"], a=a))
    c.drawRect(R(x - 170 * s, y, 340 * s, 50 * s), lin_paint(x - 170 * s, 0, x + 170 * s, 0, [ZG[0], ZG[1], ZG[0]], a=a))
    for k in range(9):
        zellige_star(c, x - 150 * s + k * 37.5 * s, y + 25 * s, 13 * s, a=a, rot=22.5 * (k % 2))
    c.drawOval(R(x - 170 * s, y + 34 * s, 340 * s, 32 * s), P("#0F2E4A", 0.9 * a))
    c.drawRect(R(x - 12 * s, y - 70 * s, 24 * s, 50 * s), P("#E8D9B5", a))
    if jet > 0:
        hh = 150 * s * jet
        c.drawLine(x, y - 70 * s, x, y - 70 * s - hh, P("#E0F2FE", 0.9 * a, stroke=8 * s))
        for k in range(10):
            q = (t * 1.2 + k / 10.0) % 1.0
            sd = -1 if k % 2 else 1
            dx = sd * (20 + 60 * q) * s
            dy = -70 * s - hh + (hh * 0.9) * q * q + 20 * s * math.sin(q * math.pi) * 0
            c.drawCircle(x + dx, y + dy * (1 - q) + (y - 10 * s) * 0, 5 * s, P("#BAE6FD", a * (1 - q)))
        add_glow(c, x, y - 70 * s - hh, 60 * s, "#E0F2FE", 0.4 * jet * a)


def courtyard(c, t, tiles=1.0, trees=1.0, jet=1.0, dusk=0.0, lamps=0.0):
    """The riad's courtyard in world space (front view): far wall with two floors of arches, side walls, the
    zellige floor, orange trees, the fountain."""
    c.drawRect(R(-1200, -1500, 2400, 600), lin_paint(0, -1500, 0, -900, [AFTERNOON["upper"], AFTERNOON["low"]]))
    wall = lin_paint(0, -940, 0, 0, ["#D9A97C", "#C68C5C", "#A86E42"])
    c.drawRect(R(-460, -940, 920, 940), wall)                              # far wall
    tex(c, R(-460, -940, 920, 940), "sand", 0.8, 0.3)
    for i, ax in enumerate((-300, 0, 300)):                                 # ground floor arches
        horseshoe(c, ax, 0, 210, 330, "#3A2416", trim="#F1E4C8")
    c.drawRect(R(-460, -400, 920, 30), P("#F1E4C8"))                        # carved stucco band
    for k in range(40):
        c.drawCircle(-450 + k * 23, -385, 6, P("#D9C7A0"))
    c.drawRect(R(-460, -650, 920, 240), P(CEDAR))                           # the upper gallery, carved cedar
    for k in range(18):
        x = -450 + k * 52
        c.drawRect(R(x, -640, 40, 200), P("#5A3418"))
        c.drawLine(x + 20, -640, x + 20, -440, P("#9A6236", 0.8, stroke=4))
    c.drawRect(R(-460, -420, 920, 20), P("#5A3418"))
    c.drawRect(R(-480, -700, 960, 56), lin_paint(0, -700, 0, -644, ["#2F7A4A", "#1E5A34"]))   # green roof tiles
    for k in range(32):
        c.drawLine(-480 + k * 30, -700, -480 + k * 30, -644, P("#164A2A", stroke=3))
    for sd in (-1, 1):                                                      # side walls in perspective
        sp = skia.Path()
        sp.moveTo(sd * 460, -940)
        sp.lineTo(sd * 1100, -1400)
        sp.lineTo(sd * 1100, 700)
        sp.lineTo(sd * 460, 0)
        sp.close()
        c.drawPath(sp, lin_paint(sd * 460, 0, sd * 1100, 0, ["#C98E5E", "#A86E42"]))
        ap = skia.Path()                                                    # one arch on each side wall
        ap.moveTo(sd * 560, 140)
        ap.lineTo(sd * 560, -220)
        ap.quadTo(sd * 660, -380, sd * 780, -260)
        ap.lineTo(sd * 780, 300)
        ap.close()
        c.drawPath(ap, P("#3A2416"))
        c.drawPath(ap, P("#F1E4C8", stroke=8))
        bp = skia.Path()                                                    # zellige band on the side wall
        bp.moveTo(sd * 460, -120)
        bp.lineTo(sd * 1100, -40)
        bp.lineTo(sd * 1100, 700)
        bp.lineTo(sd * 460, 0)
        bp.close()
        c.drawPath(bp, P("#0F2E4A", tiles))
        for k in range(5):
            u = (k + 0.5) / 5.0
            zx = lerp(460, 1100, u) * sd
            zy = lerp(-60, 330, u)
            zellige_star(c, zx, zy, lerp(30, 70, u), a=tiles, rot=22.5 * (k % 2))
    zellige_band(c, -460, 460, -120, 0, t, a=1.0, k=tiles)                  # far wall wainscot
    fp = skia.Path()                                                        # the floor
    fp.moveTo(-460, 0)
    fp.lineTo(460, 0)
    fp.lineTo(1100, 700)
    fp.lineTo(-1100, 700)
    fp.close()
    c.drawPath(fp, lin_paint(0, 0, 0, 700, ["#BFA984", "#CDBB9A", "#B59F78"]))
    c.save()
    c.clipPath(fp, doAntiAlias=True)
    for i in range(-12, 13):                                                # floor tiles in perspective
        c.drawLine(i * 40, 0, i * 100, 700, P("#9C8460", 0.8, stroke=3))
    for j in range(1, 9):
        yy = 700 * (j / 9.0) ** 1.6
        c.drawLine(-1200, yy, 1200, yy, P("#9C8460", 0.8, stroke=3))
    for i in range(-5, 6):
        for j in range(1, 7):
            u = (j / 7.0) ** 1.6
            zx = i * lerp(80, 190, u)
            zy = 700 * u
            kk = clamp(tiles * 13 - (abs(i) + j))
            if kk > 0 and (i + j) % 2 == 0:
                zellige_star(c, zx, zy, lerp(14, 34, u), a=1.0, k=kk, rot=22.5 * (j % 2))
    c.restore()
    for sx in (-330, 330):                                                  # orange trees in their beds
        c.drawOval(R(sx - 110, 300, 220, 50), P("#6B4A2A"))
        orange_tree(c, sx, 330, 1.35, t, grow=trees)
    fountain(c, 0, 250, 1.0, t, jet=jet)
    if lamps > 0:
        for lx in (-300, 0, 300):
            c.drawLine(lx, -330, lx, -260, P("#B45309", stroke=3))
            add_glow(c, lx, -240, 80, "#FDBA74", 0.8 * lamps)
            c.drawCircle(lx, -240, 14, P("#FDE68A", lamps))
    if dusk > 0:
        c.drawRect(R(-1200, -1500, 2400, 2300), P("#0B1033", 0.35 * dusk))


def facade(c, t, a=1.0, open_=0.0):
    """The blank mud wall on the alley: the two halves slide apart by open_ (0 shut, 1 gone)."""
    if a <= 0 or open_ >= 1:
        return
    for sd in (-1, 1):
        c.save()
        c.translate(sd * open_ * 1300, 0)
        x0 = -1300 if sd < 0 else 0
        c.drawRect(R(x0, -1500, 1300, 2300), lin_paint(x0, 0, x0 + 1300, 0, [OCHRE, shade(OCHRE, 0.06), OCHRE_D]
                                                         if sd > 0 else [OCHRE_D, shade(OCHRE, 0.06), OCHRE], a=a))
        tex(c, R(x0, -1500, 1300, 2300), "sand", 1.0, 0.45 * a)
        rng = random.Random(3 + sd)
        for k in range(30):                                                 # cracks and patches in the mud
            x = rng.uniform(x0, x0 + 1300)
            y = rng.uniform(-1400, 700)
            c.drawLine(x, y, x + rng.uniform(-30, 30), y + rng.uniform(10, 40), P(OCHRE_D, 0.4 * a, stroke=3))
        c.restore()
    dk = a * (1 - open_)
    if dk > 0:                                                              # the small studded door
        c.save()
        c.translate(0, 0)
        horseshoe(c, 0, 300, 250, 420, "#5A2E14", a=dk, trim="#E8C99A")
        for k in range(5):
            for j in range(3):
                c.drawCircle(-60 + j * 60, 120 + k * 40, 6, P("#E2B04A", dk))
        c.restore()


def donkey(c, x, y, s, t, a=1.0):
    """A donkey with saddlebags, seen from above."""
    c.drawOval(R(x - 26 * s, y - 60 * s, 52 * s, 120 * s), P("#8B7D6B", a))
    c.drawOval(R(x - 14 * s, y - 92 * s, 28 * s, 44 * s), P("#7A6C5A", a))
    for sd in (-1, 1):
        c.drawOval(R(x + sd * 24 * s - 10 * s, y - 108 * s, 14 * s, 26 * s), P("#6B5E4E", a))
        c.drawRRect(rr(x + sd * 40 * s - 18 * s, y - 34 * s, 36 * s, 60 * s, 8 * s), P("#B45309", a))


def roofs(c, t, x0, x1, y0, y1, seed=2, a=1.0, courts=0.0, dense=1.0):
    """The medina from above: flat roofs packed together, thin alleys between, some courtyards."""
    rng = random.Random(seed)
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), P("#3A2416", a))
    y = y0
    while y < y1:
        hh = rng.uniform(90, 170)
        x = x0
        while x < x1:
            ww = rng.uniform(80, 180)
            col = rng.choice(["#C99A72", "#B9865E", "#D3A983", "#A8744F", "#CDA584"])
            gap = rng.uniform(10, 18) / dense
            c.drawRect(R(x + gap / 2 + 8, y + gap / 2 + 10, ww - gap, hh - gap), P("#2A1A10", 0.55 * a))   # shadow
            c.drawRect(R(x + gap / 2, y + gap / 2, ww - gap, hh - gap), P(col, a))
            c.drawRect(R(x + gap / 2, y + gap / 2, ww - gap, hh - gap), P(shade(col, -0.25), a, stroke=5))   # parapet
            c.drawRect(R(x + gap / 2, y + gap / 2, ww - gap, 6), P("#FFFFFF", 0.12 * a))
            if courts > 0 and rng.random() < 0.18 and ww > 120 and hh > 120:
                cw = ww * 0.36
                c.drawRect(R(x + ww / 2 - cw / 2, y + hh / 2 - cw / 2, cw, cw), P("#2F6B3A", courts * a))
                c.drawCircle(x + ww / 2, y + hh / 2, cw * 0.25, P("#3F8A4A", courts * a))
            elif rng.random() < 0.12:
                c.drawCircle(x + ww * 0.7, y + hh * 0.3, 9, P("#F1F5F9", 0.9 * a))           # a dish on a roof
            x += ww
        y += hh


def plate(c, x, y, s, food, a=1.0):
    c.drawOval(R(x - 70 * s, y - 20 * s, 140 * s, 40 * s), P("#F8FAFC", a))
    c.drawOval(R(x - 50 * s, y - 14 * s, 100 * s, 26 * s), P(food, a))


# ====================================================================================== the episode
class Riad(EpisodeV2):
    BUILD_NO = 48
    FIRST_SET = "court"
    CLEAR = "#1E3A8A"
    TITLE = {"en": "MOROCCAN RIAD", "ar_sa": "رياض مغربي"}
    EMPH = {"en": ["CONGRATS", "HIDE", "GARDEN", "FOUNTAIN", "BLANK", "MUD", "WALL", "MOROCCAN", "RIAD", "OLD", "CITY",
                   "PACKED", "ALLEYS", "DONKEY", "SUMMER", "SUN", "BAKES", "INSIDE", "OUT", "WINDOWS", "STREET",
                   "ROOM", "COURTYARD", "SKY", "HEAT", "POUR", "TALL", "NARROW", "SHADE", "COOL", "NIGHT", "SINKS",
                   "MORNING", "WALLS", "MELT", "RAIN", "BATHROOM", "SOAK", "COAT", "LIME", "POLISH", "STONE",
                   "BLACK", "SOAP", "ROLLS", "ANYONE", "DOOR", "LOOK", "STRAIGHT", "ENTRANCE", "TURNS", "CORNER",
                   "ALLEY", "SEE", "FOLLOW", "HAGIA", "SOPHIA'S", "DOME", "TILE", "ZELLIGE", "THOUSANDS", "TINY",
                   "HAND", "ORANGE", "TREES", "NINE", "THOUSAND", "FEZ", "TWELVE", "CENTURIES", "SINGLE", "CAR",
                   "YOURSELF", "NEIGHBOR", "KNOWS", "DINNER"],
            "ar_sa": ["مبروك", "خبّيت", "جنينة", "ونافورة", "حيطة", "طين", "صمّا", "رياض", "مغربي", "القديمة", "زحمة",
                      "الحواري", "حمار", "والشمس", "الصيف", "بتشوي", "فتقلب", "لجوه", "شبابيك", "الشارع", "أوضة", "حوش",
                      "الحوش", "للسما", "الحر", "فتعليه", "وتضيّقه", "تضلّله", "الليل", "الساقع", "الصبح", "بتدوب",
                      "المطر", "والحمام", "هيشرب", "جير", "وتلمّعها", "بحجر", "بالصابون", "البلدي", "تزحلق", "معدّي",
                      "الباب", "هيبص", "جوه", "فتلف", "زاوية", "الحارة", "ميشوفش", "تابعني", "قبة", "آيا", "صوفيا",
                      "زليج", "آلاف", "بالإيد", "برتقان", "النافورة", "تسع", "تلاف", "فاس", "اتناشر", "قرن", "عربية",
                      "بإيدك", "محدش", "وجارتك", "عارفة", "اتغديتو"]}
    KEYS = {"ar_sa": {
        ("hook", "HIDE"): "خبّيت", ("hook", "GARDEN"): "جنينة", ("hook", "FOUNTAIN"): "ونافورة", ("hook", "BLANK"): "صمّا",
        ("hook", "MUD"): "طين", ("hook", "WALL"): "حيطة", ("hook", "CONGRATS"): "مبروك", ("hook", "MOROCCAN"): "رياض",
        ("break1", "OLD"): "القديمة", ("break1", "PACKED"): "زحمة", ("break1", "ALLEYS"): "الحواري", ("break1", "DONKEY"): "حمار",
        ("break1", "SUN"): "والشمس", ("break1", "BAKES"): "بتشوي",
        ("fix1", "TURN"): "فتقلب", ("fix1", "INSIDE"): "لجوه", ("fix1", "WINDOWS"): "شبابيك", ("fix1", "STREET"): "الشارع",
        ("fix1", "ROOM"): "أوضة", ("fix1", "COURTYARD"): "حوش",
        ("break2", "COURTYARD"): "الحوش", ("break2", "SKY"): "للسما", ("break2", "HEAT"): "الحر", ("break2", "POUR"): "هيدخله",
        ("fix2", "TALL"): "فتعليه", ("fix2", "NARROW"): "وتضيّقه", ("fix2", "SHADE"): "تضلّله", ("fix2", "NIGHT"): "الليل",
        ("fix2", "SINKS"): "ينزل", ("fix2", "MORNING"): "الصبح",
        ("break3", "MUD"): "الطين", ("break3", "MELT"): "بتدوب", ("break3", "RAIN"): "المطر", ("break3", "BATHROOM"): "والحمام",
        ("break3", "SOAK"): "هيشرب",
        ("fix3", "COAT"): "فتلبّسها", ("fix3", "LIME"): "جير", ("fix3", "POLISH"): "وتلمّعها", ("fix3", "STONE"): "بحجر",
        ("fix3", "SOAP"): "بالصابون", ("fix3", "ROLLS"): "تزحلق",
        ("break4", "ANYONE"): "حد", ("break4", "WALKING"): "معدّي", ("break4", "DOOR"): "الباب", ("break4", "LOOK"): "هيبص",
        ("break4", "STRAIGHT"): "جوه",
        ("fix4", "ENTRANCE"): "المدخل", ("fix4", "TURNS"): "فتلف", ("fix4", "CORNER"): "زاوية", ("fix4", "ALLEY"): "الحارة",
        ("fix4", "SEE"): "ميشوفش", ("fix4", "WALL"): "حيطة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "TILE"): "لبّسه", ("reveal", "ZELLIGE"): "زليج", ("reveal", "THOUSANDS"): "آلاف", ("reveal", "HAND"): "بالإيد",
        ("reveal", "ORANGE"): "برتقان", ("reveal", "FOUNTAIN"): "النافورة",
        ("stat", "NINE"): "تسع", ("stat", "TWELVE"): "اتناشر", ("stat", "CAR"): "عربية",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "CENTURIES"): "قرون", ("tag", "NOBODY"): "محدش", ("tag", "NEIGHBOR"): "وجارتك", ("tag", "KNOWS"): "عارفة",
        ("tag", "DINNER"): "اتغديتو"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Hagia Sophia's dome"),
                   "stat": [("9,000+", "ALLEYS IN OLD FEZ"), ("1,200", "YEARS OLD"), ("0", "CARS")],
                   "L": {"garden": "A GARDEN + A FOUNTAIN", "blank": "BEHIND A BLANK MUD WALL", "name": "A MOROCCAN RIAD",
                         "packed": "PACKED TIGHT", "donkey": "ALLEYS BARELY FIT A DONKEY", "bakes": "THE SUN BAKES IT",
                         "inside": "TURN IT INSIDE OUT", "nowin": "NO WINDOWS ON THE STREET",
                         "rooms": "ROOMS OPEN ONTO THE COURTYARD", "pour": "THE HEAT POURS IN",
                         "tall": "TALL + NARROW", "shade": "THE WALLS SHADE IT", "cool": "COOL NIGHT AIR SINKS IN",
                         "morning": "STAYS ALL MORNING", "melt": "MUD MELTS IN THE RAIN", "soak": "THE BATHROOM SOAKS",
                         "lime": "LIME PLASTER", "stone": "POLISHED WITH A STONE", "soap": "BLACK SOAP",
                         "rolls": "WATER ROLLS OFF", "look": "THEY LOOK STRAIGHT IN", "corner": "THE ENTRANCE TURNS",
                         "wall": "ALL YOU SEE IS A WALL", "zellige": "ZELLIGE", "hand": "EVERY PIECE CUT BY HAND",
                         "trees": "ORANGE TREES", "dinner": "PASTA AGAIN?", "hot": "40°+"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: قبة آيا صوفيا"),
                      "stat": [("9,000+", "حارة في فاس القديمة"), ("1,200", "سنة"), ("0", "عربيات")],
                      "L": {"garden": "جنينة ونافورة", "blank": "ورا حيطة طين صمّا", "name": "رياض مغربي",
                            "packed": "زحمة", "donkey": "الحارة يا دوب تساع حمار", "bakes": "الشمس بتشوي",
                            "inside": "اقلب البيت لجوه", "nowin": "مفيش شبابيك على الشارع",
                            "rooms": "كل أوضة على الحوش", "pour": "الحر بيدخل", "tall": "عالي وضيق",
                            "shade": "الحيطان تضلله", "cool": "هوا الليل الساقع ينزل", "morning": "ويفضل طول الصبح",
                            "melt": "الطين بيدوب في المطر", "soak": "الحمام بيشرب مية", "lime": "جير",
                            "stone": "تلميع بحجر", "soap": "صابون بلدي", "rolls": "المية بتزحلق",
                            "look": "هيبص جوه على طول", "corner": "المدخل بيلف", "wall": "ميشوفش غير حيطة",
                            "zellige": "زليج", "hand": "كل حتة بالإيد", "trees": "شجر برتقان",
                            "dinner": "ملوخية تاني؟", "hot": "40°+"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "hide": ("hook", "HIDE", 0.1), "garden": ("hook", "GARDEN", 0.2), "fountain": ("hook", "FOUNTAIN", 0.32),
            "blank": ("hook", "BLANK", 0.5), "mud": ("hook", "MUD", 0.55), "wall": ("hook", "WALL", 0.6),
            "congrats": ("hook", "CONGRATS", 0.66), "moroccan": ("hook", "MOROCCAN", 0.88),
            "old": ("break1", "OLD", 0.1), "packed": ("break1", "PACKED", 0.22), "alleys": ("break1", "ALLEYS", 0.35),
            "donkey": ("break1", "DONKEY", 0.58), "sun": ("break1", "SUN", 0.75), "bakes": ("break1", "BAKES", 0.85),
            "turn": ("fix1", "TURN", 0.08), "inside": ("fix1", "INSIDE", 0.2), "windows": ("fix1", "WINDOWS", 0.42),
            "street": ("fix1", "STREET", 0.55), "room": ("fix1", "ROOM", 0.75), "courtyard": ("fix1", "COURTYARD", 0.9),
            "court2": ("break2", "COURTYARD", 0.15), "sky": ("break2", "SKY", 0.45), "heat": ("break2", "HEAT", 0.7),
            "pour": ("break2", "POUR", 0.8),
            "tall": ("fix2", "TALL", 0.15), "narrow": ("fix2", "NARROW", 0.25), "shade": ("fix2", "SHADE", 0.42),
            "night": ("fix2", "NIGHT", 0.6), "sinks": ("fix2", "SINKS", 0.68), "morning": ("fix2", "MORNING", 0.9),
            "mud2": ("break3", "MUD", 0.1), "melt": ("break3", "MELT", 0.22), "rain": ("break3", "RAIN", 0.4),
            "bathroom": ("break3", "BATHROOM", 0.6), "soak": ("break3", "SOAK", 0.78),
            "coat": ("fix3", "COAT", 0.08), "lime": ("fix3", "LIME", 0.2), "polish": ("fix3", "POLISH", 0.3),
            "stone": ("fix3", "STONE", 0.45), "soap": ("fix3", "SOAP", 0.68), "rolls": ("fix3", "ROLLS", 0.9),
            "anyone": ("break4", "ANYONE", 0.1), "walking": ("break4", "WALKING", 0.25), "door": ("break4", "DOOR", 0.55),
            "look": ("break4", "LOOK", 0.7), "straight": ("break4", "STRAIGHT", 0.82),
            "entrance": ("fix4", "ENTRANCE", 0.12), "turns": ("fix4", "TURNS", 0.2), "corner": ("fix4", "CORNER", 0.3),
            "alley": ("fix4", "ALLEY", 0.55), "see": ("fix4", "SEE", 0.75), "wall2": ("fix4", "WALL", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "tile": ("reveal", "TILE", 0.05), "zellige": ("reveal", "ZELLIGE", 0.15), "thousands": ("reveal", "THOUSANDS", 0.25),
            "hand": ("reveal", "HAND", 0.6), "orange": ("reveal", "ORANGE", 0.75), "fountain2": ("reveal", "FOUNTAIN", 0.92),
            "s1": ("stat", "NINE", 0.08), "s2": ("stat", "TWELVE", 0.48), "s3": ("stat", "CAR", 0.85),
            "cong2": ("closer", "CONGRATS", 0.16),
            "centuries": ("tag", "CENTURIES", 0.05), "nobody": ("tag", "NOBODY", 0.25), "neighbor": ("tag", "NEIGHBOR", 0.55),
            "knows": ("tag", "KNOWS", 0.75), "dinner": ("tag", "DINNER", 0.9)})
        T["shut0"] = min(T["blank"], T["mud"], T["wall"]) - 0.2
        T["see0"] = min(T["see"], T["wall2"])
        # ---- sets
        self.cut(s("break1") - 0.12, "city", 1)
        self.cut(s("fix1") - 0.12, "section", -1)
        self.cut(s("break3") - 0.12, "wall", 1)
        self.cut(s("break4") - 0.12, "door", -1)
        self.cut(s("reveal") - 0.12, "court", 1)
        self.cut(s("stat") - 0.12, "fez", -1)
        self.cut(s("closer") - 0.12, "court", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- court camera
        cm = Camera(0, -240, 1.05)
        cm.key(0.2, 0, -200, 1.12, max(1.0, T["shut0"] - 0.3))
        cm.key(T["shut0"], 0, -150, 0.92, 0.9)
        cm.key(T["congrats"], 0, -220, 1.0, 1.2)
        cm.key(s("reveal") - 0.12, 0, -60, 1.2, 0.0).key(T["orange"] - 0.4, 0, -160, 1.05, 1.2)
        cm.key(s("closer") - 0.12, 0, 40, 1.0, 0.0).key(self.duration, 0, 30, 1.04, 4.0)
        self.cam = cm
        self.spans = [(T["bakes"], T["courtyard"] + 0.3), (T["pour"], T["morning"] + 0.3), (T["soak"], T["rolls"] + 0.3),
                      (T["straight"], T["wall2"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["shut0"] + 0.5, 0.3, 6), (T["bakes"], 0.3, 6), (T["melt"] + 0.2, 0.3, 6),
                       (T["straight"], 0.3, 6), (s("closer") + 0.2, 0.35, 9), (T["knows"], 0.3, 6)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    # ------------------------------------------------------------------ set: court (hook, reveal, closer)
    def draw_court(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1") - 0.12
        reveal = s("reveal") - 0.12 <= t < s("stat") - 0.12
        v2.sky(c, W, H, 0.0, pal=AFTERNOON, horizon_y=700)
        self.view(c, cam)
        tiles = trees = jet = 1.0
        if reveal:
            tiles = prog(t, T["tile"] - 0.1, T["hand"] + 0.3)
            trees = prog(t, T["orange"] - 0.2, T["orange"] + 0.5)
            jet = prog(t, T["fountain2"] - 0.2, T["fountain2"] + 0.4)
        courtyard(c, t, tiles=tiles, trees=trees, jet=jet, lamps=0.0)
        if hook:
            shut = e_io(prog(t, T["shut0"], T["shut0"] + 0.7))
            opn = e_io(prog(t, T["congrats"] - 0.1, T["congrats"] + 0.7))
            if shut > 0:
                facade(c, t, a=1.0, open_=lerp(1.0, 0.0, shut) if opn <= 0 else opn)
        if reveal and t < T["hand"] + 0.6:                                  # a hand laying a piece
            hx = lerp(-400, 400, prog(t, T["tile"], T["hand"] + 0.3))
            c.drawCircle(hx, -60, 28, P("#C68B59"))
            c.drawRect(R(hx - 8, -110, 16, 50), P("#C68B59"))
        c.restore()
        self.ui["cam"] = cam

    def ui_court(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 420, "garden", T["garden"] - 0.15, T["shut0"], accent=GOOD, size=42)
            self.chip(540, 420, "blank", T["shut0"], T["congrats"] - 0.1, accent="#FDBA74", size=40)
            self.chip(540, 420, "name", T["moroccan"] - 0.15, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            self.chip(540, 420, "zellige", T["zellige"] - 0.15, T["hand"] - 0.15, accent="#60A5FA", size=46)
            self.chip(540, 420, "hand", T["hand"] - 0.15, T["orange"] - 0.15, accent=HILITE, size=40)
            self.chip(540, 420, "trees", T["orange"] - 0.15, s("stat") - 0.15, accent=ORANGE, size=42)

    # ------------------------------------------------------------------ set: city (break1)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        z = lerp(1.0, 1.25, prog(t, s("break1"), s("fix1")))
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(z, z)
        c.translate(-W / 2, -H / 2 + 60)
        roofs(c, t, -200, W + 200, -200, H + 200, seed=4)
        ax = 540                                                            # the alley with the donkey
        c.drawRect(R(ax - 60, -200, 120, H + 400), P("#4A3020"))
        dy = lerp(1300, 820, prog(t, T["alleys"] - 0.4, T["donkey"] + 0.6))
        donkey(c, ax, dy, 1.7, t)
        c.drawCircle(ax, dy + 190, 30, P("#1D4ED8"))
        c.drawCircle(ax, dy + 184, 18, P("#C68B59"))
        c.restore()
        hk = prog(t, T["sun"] - 0.3, T["bakes"])
        if hk > 0:
            c.drawRect(R(0, 0, W, H), P("#F97316", 0.18 * hk))
            heat_lines(c, 100, 980, 600, 1200, t, a=hk)
            sun(c, 880, 300, 80, heat=1.0, a=hk)

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 420, "packed", T["packed"] - 0.15, T["alleys"] - 0.1, accent="#FDBA74", size=42)
        self.chip(540, 420, "donkey", T["alleys"] - 0.1, T["sun"] - 0.15, accent="#E2E8F0", size=36)
        self.chip(540, 420, "bakes", T["sun"] - 0.15, s("fix1") - 0.15, accent=WARN, size=42)
        self.badge("alert", T["bakes"] + 0.05, s("fix1") - 0.2, x=880, y=520)
        self.red(T["bakes"] + 0.05, 1.2)

    # ------------------------------------------------------------------ set: section (fix1, break2, fix2)
    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        tallk = e_io(prog(t, min(T["tall"], T["narrow"]) - 0.2, max(T["tall"], T["narrow"]) + 0.5)) if t >= s("fix2") - 0.12 else 0.0
        night = 0.0
        if t >= s("fix2") - 0.12:
            night = prog(t, T["night"] - 0.3, T["night"] + 0.3) * (1 - prog(t, T["morning"] - 0.3, T["morning"] + 0.2))
        cam = (0, lerp(-160, -270, tallk), lerp(1.0, 0.92, tallk))
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=AFTERNOON, horizon_y=gy - 20)
        if night > 0:
            v2.sky(c, W, H, 0.0, pal=NIGHT, horizon_y=gy - 20)
            c.drawRect(R(0, 0, W, H), P("#000000", 0.0))
        self.view(c, cam)
        c.drawRect(R(-3000, 0, 6000, 2000), lin_paint(0, 0, 0, 600, ["#8A6A4A", "#4A3424"]))
        top = lerp(-520, -760, tallk)
        cw = lerp(150, 90, tallk)                                           # half width of the courtyard
        hx0, hx1 = -420, 420
        wall_c = lin_paint(hx0, 0, hx1, 0, [OCHRE, shade(OCHRE, 0.08), OCHRE_D])
        c.drawRect(R(hx0, top, hx1 - hx0, -top), wall_c)                    # the house in section
        nf = 3 if tallk > 0.5 else 2
        fh = -top / nf
        for sd in (-1, 1):                                                  # rooms on each side
            xa, xb = (hx0 + 50, -cw) if sd < 0 else (cw, hx1 - 50)
            for f in range(nf):
                yb = -f * fh
                c.drawRect(R(xa, yb - fh + 20, xb - xa, fh - 20), lin_paint(0, yb - fh, 0, yb, ["#CDB08A", "#B8986E"]))
                c.drawRect(R(xa, yb - 14, xb - xa, 14), P("#B88A5A"))
                if t >= s("fix1") - 0.12:                                   # doors onto the courtyard
                    dx = -cw if sd < 0 else cw
                    horseshoe(c, dx - sd * 30, yb - 14, 50, fh * 0.62, "#5A3418")
        cy0 = 0
        c.drawRect(R(-cw, top, 2 * cw, -top), lin_paint(0, top, 0, 0, ["#7FA6D6", "#BFA57E"]))   # the courtyard
        fk = 1.0
        c.drawRect(R(-cw, -24, 2 * cw, 24), P("#1E5AA8"))
        fountain(c, 0, -26, 0.25, t, jet=fk)
        ok_win = 1 - e_io(prog(t, T["windows"] - 0.3, T["street"] + 0.2)) if t < s("break2") - 0.12 else 0.0
        for f in range(nf):                                                 # windows on the street wall
            wy = -f * fh - fh * 0.6
            if ok_win > 0:
                c.drawRect(R(hx0 + 4, wy, 40, fh * 0.32 * ok_win), P("#1E293B"))
        rmk = prog(t, T["room"] - 0.2, T["courtyard"] + 0.3) if t < s("break2") - 0.12 else (1.0 if t < s("fix2") else 0.0)
        if rmk > 0:
            for sd in (-1, 1):
                for f in range(nf):
                    yy = -f * fh - fh * 0.35
                    arrow(c, sd * (cw + 150), yy, sd * (cw + 30), yy, GOOD, a=rmk * 0.9, w=12, head=26)
        sx_, sy_ = 380, top - 360                                           # the sun
        sun_a = (1 - night)
        if t >= s("break2") - 0.12:
            shaft = skia.Path()
            if tallk < 0.5:
                pk = prog(t, T["sky"] - 0.3, T["pour"] + 0.3)
                shaft.moveTo(sx_, sy_)
                shaft.lineTo(-cw, 0)
                shaft.lineTo(cw, 0)
                shaft.close()
                c.drawPath(shaft, P("#FDE68A", 0.35 * pk))
                c.drawRect(R(-cw, -60, 2 * cw, 60), P("#F97316", 0.45 * pk))
                heat_lines(c, -cw, cw, top * 0.6, -10, t, a=pk)
            else:
                shaft.moveTo(sx_, sy_)
                shaft.lineTo(-cw, top + 60)
                shaft.lineTo(cw - 10, top)
                shaft.close()
                c.drawPath(shaft, P("#FDE68A", 0.3 * (1 - night)))
                c.drawRect(R(-cw, top + 80, 2 * cw, -top - 80), P("#1E3A8A", 0.25 * prog(t, T["shade"] - 0.3, T["shade"] + 0.3)))
        sun(c, sx_, sy_, 50, heat=0.5, a=sun_a)
        if night > 0:
            v2.moon(c, -300, top - 300, 46, a=night)
        if t >= s("fix2") - 0.12:
            ck = prog(t, T["sinks"] - 0.4, T["sinks"] + 0.2)
            for k in range(4):                                              # cool air sinks in
                q = (t * 0.7 + k / 4.0) % 1.0
                yy = lerp(top - 120, -60, q)
                arrow(c, -cw * 0.5 + k * cw * 0.33, yy - 60, -cw * 0.5 + k * cw * 0.33, yy, "#60A5FA", a=ck * (1 - q * 0.4), w=12, head=24)
            mk = prog(t, T["sinks"], T["morning"] + 0.3)
            c.drawRect(R(-cw, -200 * mk, 2 * cw, 200 * mk), P("#3B82F6", 0.28 * mk))
            hk = prog(t, T["morning"] - 0.3, T["morning"] + 0.3)            # the street outside is hot again
            if hk > 0:
                c.drawRect(R(-1200, top, 1200 + hx0, -top), P("#F97316", 0.25 * hk))
                heat_lines(c, -900, hx0 - 20, top * 0.8, -20, t, a=hk)
        person(c, -620, 0, 150, "#2563EB", t, pose="walk", face=1, hat="cap", hair="#1C1917")
        if night > 0:
            c.drawRect(R(-3000, -3000, 6000, 6000), P("#020617", 0.25 * night))
        c.restore()
        self.ui["cam"] = cam
        self.ui["cw"] = cw
        self.ui["top"] = top

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (0, -160, 1.0))
        if tw < s("break2") - 0.12:
            self.chip(540, 420, "inside", T["turn"] - 0.1, T["windows"] - 0.15, accent=HILITE, size=42)
            wx, wy = self.at(cam, -400, -200)
            self.label(wx, wy, 300, 560, "nowin", T["windows"] - 0.15, s("break2") - 0.15, "#FDBA74", size=34)
            self.chip(540, 420, "rooms", T["room"] - 0.15, s("break2") - 0.15, accent=GOOD, size=34)
            self.badge("check", T["courtyard"] + 0.05, s("break2") - 0.15, x=880, y=520)
            return
        if tw < s("fix2") - 0.12:
            self.chip(540, 420, "pour", T["sky"] - 0.15, s("fix2") - 0.15, accent=WARN, size=42)
            k = self.span(T["heat"] - 0.2, s("fix2") - 0.15)
            if k > 0:
                v2.chip(c, 540, 560, self.L["hot"], k, accent=WARN, size=46)
            self.badge("alert", T["pour"] + 0.05, s("fix2") - 0.2, x=880, y=520)
            self.red(T["pour"] + 0.05, 1.2)
            return
        self.chip(540, 420, "tall", min(T["tall"], T["narrow"]) - 0.15, T["shade"] - 0.1, accent=HILITE, size=42)
        self.chip(540, 420, "shade", T["shade"] - 0.1, T["night"] - 0.15, accent="#93C5FD", size=40)
        self.chip(540, 420, "cool", T["night"] - 0.15, T["morning"] - 0.15, accent="#60A5FA", size=38)
        self.chip(540, 420, "morning", T["morning"] - 0.15, s("break3") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["morning"] + 0.1, s("break3") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: wall (break3, fix3)
    def draw_wall(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        vrect(c, 0, 0, W, H, ["#3E4C66", "#5B6B85"] if not fixed else ["#5B7FAE", "#9C8466"])
        wx0, wx1, wy0, wy1 = 90, 990, 380, 1200
        melt = prog(t, T["melt"] - 0.2, T["soak"] + 0.6) if not fixed else 0.0
        wp = skia.Path()                                                    # the wall, its foot washing away
        wp.moveTo(wx0, wy0)
        wp.lineTo(wx1, wy0)
        n = 18
        for i in range(n + 1):
            x = lerp(wx1, wx0, i / float(n))
            y = wy1 - melt * (60 + 40 * math.sin(i * 1.7))
            wp.lineTo(x, y)
        wp.close()
        c.drawPath(wp, lin_paint(wx0, 0, wx1, 0, [OCHRE, shade(OCHRE, 0.06), OCHRE_D]))
        tex(c, wp, "sand", 1.0, 0.5)
        for k in range(9):                                                  # mud bricks
            yy = wy0 + k * 90
            c.drawLine(wx0, yy, wx1, yy, P(OCHRE_D, 0.5, stroke=3))
            for j in range(6):
                xx = wx0 + j * 150 + (k % 2) * 75
                c.drawLine(xx, yy, xx, yy + 90, P(OCHRE_D, 0.4, stroke=3))
        if not fixed:
            rain(c, 0, W, 0, 1300, t, a=prog(t, T["rain"] - 0.6, T["rain"]) * 0.9 + 0.3, n=90, seed=7)
            for k in range(10):                                             # mud running down
                x = wx0 + 60 + k * 85
                L_ = 200 * melt * (0.5 + 0.5 * math.sin(k * 2.1))
                c.drawLine(x, wy1 - 300, x, wy1 - 300 + L_, P("#6B4423", 0.7 * melt, stroke=10))
            sk = prog(t, T["bathroom"] - 0.2, T["soak"] + 0.4)              # the wet patch from the bathroom
            if sk > 0:
                c.drawOval(R(520 - 220 * sk, 640 - 160 * sk, 440 * sk, 320 * sk), P("#3B2410", 0.45 * sk))
                for k in range(4):
                    q = (t * 1.2 + k / 4.0) % 1.0
                    c.drawCircle(460 + k * 40, 700 + q * 200 * sk, 8, P("#7DD3FC", sk * (1 - q)))
        else:
            lk = prog(t, T["coat"] - 0.1, T["lime"] + 0.6)                  # lime plaster spreads left to right
            xe = lerp(wx0, wx1, lk)
            c.drawRect(R(wx0, wy0, xe - wx0, wy1 - wy0), lin_paint(0, wy0, 0, wy1, ["#D2C3A4", "#B5A27E"]))
            if 0 < lk < 1:
                c.drawRRect(rr(xe - 20, 700, 120, 60, 10), P("#9CA3AF"))
                c.drawLine(xe + 40, 700, xe + 80, 620, P("#78350F", stroke=14))
            pk = prog(t, T["polish"] - 0.2, T["soap"])
            if pk > 0:                                                      # a river stone polishing in circles
                sx_ = 540 + math.cos(t * 7) * 160
                sy_ = 760 + math.sin(t * 7) * 120
                c.drawOval(R(sx_ - 60, sy_ - 40, 120, 80), P("#4B5563", pk))
                c.drawOval(R(sx_ - 40, sy_ - 30, 50, 20), P("#9CA3AF", pk))
                for k in range(6):
                    a0 = t * 7 - k * 0.3
                    c.drawCircle(540 + math.cos(a0) * 160, 760 + math.sin(a0) * 120, 30, P("#FFFFFF", 0.12 * pk))
            sk = prog(t, T["soap"] - 0.2, T["soap"] + 0.5)
            if sk > 0:                                                      # black soap: a deep sheen
                c.drawRect(R(wx0, wy0, wx1 - wx0, wy1 - wy0), P("#7C5A3A", 0.22 * sk))
                c.drawRect(R(wx0, wy0, (wx1 - wx0) * sk, 60), lin_paint(wx0, 0, wx1, 0, [("#FFFFFF", 0.0), ("#FFFFFF", 0.4 * sk), ("#FFFFFF", 0.0)]))
            rk = prog(t, T["rolls"] - 0.6, T["rolls"])
            if rk > 0:                                                      # water beads and rolls off
                for k in range(14):
                    q = (t * 0.9 + k * 0.137) % 1.0
                    x = wx0 + 50 + k * 62
                    y = lerp(wy0 - 20, wy1 + 60, q)
                    c.drawCircle(x, y, 13, P("#BAE6FD", 0.9 * rk))
                    c.drawCircle(x - 4, y - 4, 4, P("#FFFFFF", rk))

    def ui_wall(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "melt", T["melt"] - 0.15, T["bathroom"] - 0.15, accent="#FDBA74", size=40)
            self.chip(540, 300, "soak", T["bathroom"] - 0.15, s("fix3") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["soak"] + 0.05, s("fix3") - 0.2, x=900, y=300)
            self.red(T["soak"] + 0.05, 1.2)
            return
        self.chip(540, 300, "lime", T["coat"] - 0.1, T["polish"] - 0.15, accent=LIME, size=44)
        self.chip(540, 300, "stone", T["polish"] - 0.15, T["soap"] - 0.15, accent="#9CA3AF", size=40)
        self.chip(540, 300, "soap", T["soap"] - 0.15, T["rolls"] - 0.3, accent="#A16207", size=42)
        self.chip(540, 300, "rolls", T["rolls"] - 0.3, s("break4") - 0.15, accent="#7DD3FC", size=42)
        self.badge("check", T["rolls"] + 0.1, s("break4") - 0.15, x=900, y=300)

    # ------------------------------------------------------------------ set: door (break4, fix4), from above
    def draw_door(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        vrect(c, 0, 0, W, H, ["#B07A50", "#9A6A44"])
        c.drawRect(R(0, 1060, W, 220), P("#6E4A30"))                        # the alley
        for k in range(12):
            c.drawLine(k * 100, 1060, k * 100 + 40, 1280, P("#5A3A24", 0.5, stroke=4))
        c.drawRect(R(140, 360, 800, 700), P(OCHRE))                         # the house from above (walls)
        c.drawRect(R(330, 400, 420, 380), P("#C2AA84"))                     # the courtyard
        for k in range(4):
            zellige_star(c, 380 + k * 107, 740, 18, rot=22.5 * (k % 2))
        c.drawCircle(540, 590, 70, P("#0F2E4A"))
        c.drawCircle(540, 590, 56, P("#38BDF8"))
        for sx in (390, 690):
            c.drawCircle(sx, 470, 50, P(LEAF))
            for k in range(5):
                c.drawCircle(sx - 30 + k * 15, 460 + (k % 2) * 20, 6, P(ORANGE))
        for i, (fx_, col) in enumerate(((460, "#DB2777"), (620, "#2563EB"), (560, "#F59E0B"))):    # the family
            c.drawCircle(fx_, 700 - i * 30, 22, P(col))
            c.drawCircle(fx_, 700 - i * 30, 12, P("#C68B59"))
        bend = e_io(prog(t, min(T["entrance"], T["turns"]) - 0.1, T["corner"] + 0.4)) if fixed else 0.0
        cor = skia.Path()                                                   # the entrance corridor
        if bend < 0.5:
            cor.addRect(R(500, 780, 80, 280))
        else:
            cor.moveTo(500, 1060)
            cor.lineTo(580, 1060)
            cor.lineTo(580, 930)
            cor.lineTo(330, 930)
            cor.lineTo(330, 780)
            cor.lineTo(250, 780)
            cor.lineTo(250, 860)
            cor.lineTo(500, 860)
            cor.close()
        c.drawPath(cor, P("#3A2416"))
        if bend >= 0.5:
            c.drawRect(R(500, 780, 80, 80), P(OCHRE))
        c.drawRect(R(490, 1050, 100, 18), P("#5A2E14"))                     # the door
        px = 540 + (0 if fixed else lerp(-400, 0, prog(t, s("break4"), T["door"])))
        py = 1180
        c.drawCircle(px, py, 34, P("#1D4ED8"))                              # the passer-by, from above
        c.drawCircle(px, py - 6, 20, P("#C68B59"))
        lk = prog(t, T["look"] - 0.3, T["look"]) if not fixed else prog(t, T["alley"] - 0.3, T["alley"])
        if lk > 0:
            yend = 560 if not fixed else 880
            dash = skia.Path()
            dash.moveTo(px, py - 40)
            dash.lineTo(px, lerp(py - 40, yend, lk))
            c.drawPath(dash, dash_paint(HILITE if not fixed else WARN, lk, w=6, t=t))
            if fixed and lk >= 1:
                c.drawLine(px - 26, yend - 26, px + 26, yend + 26, P(WARN, stroke=10))
                c.drawLine(px - 26, yend + 26, px + 26, yend - 26, P(WARN, stroke=10))
        self.ui["px"] = px

    def ui_door(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 280, "look", T["look"] - 0.2, s("fix4") - 0.15, accent=HILITE, size=40)
            self.badge("alert", T["straight"] + 0.05, s("fix4") - 0.2, x=900, y=280)
            self.red(T["straight"] + 0.05, 1.2)
            return
        self.chip(540, 280, "corner", min(T["entrance"], T["turns"]) - 0.1, T["see0"] - 0.2, accent="#FDBA74", size=42)
        self.chip(540, 280, "wall", T["see0"] - 0.2, s("cta") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["wall2"] + 0.1, s("cta") - 0.15, x=900, y=280)

    # ------------------------------------------------------------------ set: fez (the stat)
    def draw_fez(self, c, t):
        T, s = self.T, self.tl.s
        z = lerp(1.3, 0.8, e_io(prog(t, s("stat") - 0.12, s("closer"))))
        c.save()
        c.translate(W / 2, H / 2 + 120)
        c.scale(z, z)
        c.translate(-W / 2, -H / 2)
        roofs(c, t, -800, W + 800, -700, H + 700, seed=9, courts=1.0, dense=1.0)
        c.restore()
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, 700, [("#FDBA74", 0.35), ("#FDBA74", 0.0)]))
        k = self.span(T["s3"] - 0.1, s("closer") - 0.1)
        if k > 0:                                                           # no cars
            cx_, cy_ = 540, 860
            c.drawCircle(cx_, cy_, 120, P(GLASS, 0.85 * k))
            c.drawRRect(rr(cx_ - 70, cy_ - 26, 140, 50, 16), P("#E5E7EB", k))
            c.drawRRect(rr(cx_ - 40, cy_ - 56, 80, 36, 12), P("#E5E7EB", k))
            for sd in (-1, 1):
                c.drawCircle(cx_ + sd * 40, cy_ + 26, 16, P("#111827", k))
            c.drawCircle(cx_, cy_, 110, P(WARN, k, stroke=12))
            c.drawLine(cx_ - 78, cy_ + 78, cx_ + 78, cy_ - 78, P(WARN, k, stroke=14))

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#1E293B", "#334155"])
        for sd, x0 in ((-1, 0), (1, 600)):                                  # two buildings across a narrow street
            c.drawRect(R(x0, 0, 480, 1300), lin_paint(x0, 0, x0 + 480, 0, ["#D6C3A5", "#B8A483"] if sd < 0 else ["#C9B08E", "#A88E6C"]))
        c.drawRect(R(480, 0, 120, 1300), P("#0F172A"))
        vrect(c, 0, 1240, W, H - 1240, ["#0F172A", "#020617"])
        c.drawRect(R(60, 560, 360, 380), P("#FDE68A"))                      # our window: dinner
        c.drawRect(R(60, 560, 360, 380), P("#7C5A3A", stroke=14))
        c.drawRect(R(80, 820, 320, 30), P("#92400E"))
        food = "#365314" if self.rtl else "#F59E0B"
        plate(c, 240, 815, 1.1, food)
        person(c, 330, 860, 180, "#2563EB", t, pose="sit", face=-1, hat="none", hair="#1C1917")
        c.drawRect(R(660, 480, 360, 420), P("#FCD9A0"))                    # the neighbour's window
        c.drawRect(R(660, 480, 360, 420), P("#7C5A3A", stroke=14))
        nk = prog(t, T["neighbor"] - 0.3, T["neighbor"] + 0.2)
        lean = lerp(0, -60, nk)
        person(c, 840 + lean, 900, 300, "#DB2777", t, pose="look", face=-1, hat="none", hair="#4A2A1A")
        if nk > 0:                                                          # binoculars
            u = 300 / 140.0
            bx_, by_ = 840 + lean - 20 * u, 900 - 128 * u
            for k in range(2):
                c.drawCircle(bx_ - 10 * u, by_ + (k * 12 - 6) * u, 7 * u, P("#111827", nk))
            c.drawRect(R(bx_ - 30 * u, by_ - 12 * u, 20 * u, 24 * u), P("#111827", nk))
        c.drawRect(R(640, 880, 400, 40), P("#B8A483"))                      # her window sill

    def ui_tag(self, c, t, tw):
        T = self.T
        k = self.span(T["knows"] - 0.15, self.duration + 1)
        if k > 0:
            bx, by = 760, 360
            sz = 42
            lab = self.L["dinner"]
            wdt = (arabic.width_ar(lab, sz * 1.15, "Tajawal-Black") if arabic.is_ar(lab) else text_width(lab, sz, "Poppins-Black")) + 70
            kk = e_back(clamp(k))
            c.save()
            c.translate(bx, by)
            c.scale(kk, kk)
            c.drawRRect(rr(-wdt / 2, -60, wdt, 110, 50), P("#F8FAFC"))
            tp = skia.Path()
            tp.moveTo(0, 46)
            tp.lineTo(40, 46)
            tp.lineTo(30, 100)
            tp.close()
            c.drawPath(tp, P("#F8FAFC"))
            word(c, lab, 0, 14, sz, "#111827")
            c.restore()

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=AFTERNOON, horizon_y=H * 0.6)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.0, T["shut0"]), 61), -18), (0.1, sfx.sparkle(0.8, 9, 62), -12),
              (T["fountain"], sfx.tap(63), -12), (T["shut0"], sfx.whoosh(0.6, False, 64), -10),
              (T["shut0"] + 0.6, sfx.thud(0.4, 65), -6), (T["congrats"] - 0.1, sfx.whoosh(0.6, True, 66), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 11, 67), -8), (T["moroccan"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 68), -4), (T["donkey"], sfx.clank(700.0, 0.2, 69), -14),
               (T["donkey"] + 0.25, sfx.clank(660.0, 0.2, 70), -14), (T["sun"], sfx.sizzle(0.8, 71), -12),
               (T["bakes"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["windows"], sfx.thud(0.3, 73), -10),
               (T["street"], sfx.thud(0.3, 74), -10), (T["room"], sfx.pop(75), -8), (T["courtyard"] + 0.1, sfx.ding(), -8),
               (T["courtyard"] + 0.3, sfx.chime(), -6)]
        ev += [(T["sky"], sfx.riser(0.8, 76), -14), (T["heat"], sfx.sizzle(0.6, 77), -12), (T["pour"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(min(T["tall"], T["narrow"]), sfx.whirr(0.8, 180.0, 260.0, 78), -14), (T["shade"], sfx.whoosh(0.5, False, 79), -12),
               (T["night"], sfx.sparkle(0.6, 7, 80), -14), (T["sinks"], sfx.whoosh(0.8, False, 81), -12),
               (T["morning"] + 0.1, sfx.ding(), -8), (T["morning"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 82), -4), (s("break3"), sfx.hiss(2.5, 83), -10),
               (T["melt"], sfx.creak(0.6), -12), (T["soak"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 84), -4), (T["coat"], sfx.hiss(0.8, 85), -14),
               (T["polish"], sfx.whirr(1.4, 300.0, 340.0, 86), -16), (T["soap"], sfx.sparkle(0.6, 8, 87), -12),
               (T["rolls"], sfx.tap(88), -8), (T["rolls"] + 0.1, sfx.ding(), -8), (T["rolls"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 89), -4), (T["look"], sfx.pop(90), -8),
               (T["straight"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 91), -4), (T["turns"], sfx.thud(0.3, 92), -8),
               (T["see0"], sfx.buzz(0.3), -12), (T["wall2"] + 0.1, sfx.ding(), -8), (T["wall2"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(93), 0), (T["follow"] - 0.15, sfx.pop(94), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 95), -6)]
        for k in range(8):
            ev.append((T["tile"] + k * 0.3, sfx.tap(96 + k), -12))
        ev += [(T["orange"], sfx.pop(104), -8), (T["fountain2"], sfx.hiss(1.2, 105), -14)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 106), -6), (T["s1"], sfx.pop(107), -3), (T["s2"], sfx.pop(108), -3),
               (T["s3"], sfx.pop(109), -3)]
        ev += [(T["cong2"], sfx.pop(110), -2), (T["cong2"], sfx.sparkle(1.0, 14, 111), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 112), -6), (T["neighbor"], sfx.creak(0.5), -12),
               (T["knows"], sfx.pop(113), -6), (T["dinner"] + 0.2, sfx.tick(), -10)]
        return ev


NAME = "riad"
EPISODE = Riad
