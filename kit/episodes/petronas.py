"""Episode 72 - the Petronas Twin Towers and the sky bridge that slides.  v2 look: the towers in elevation (1 m = 2
units, ground y = 0): two silver towers of stacked setbacks with pinnacles, 58 m apart, joined at 170 m by a
two-floor bridge that rests on bearings and an arch of two legs, so it slides in and out of each tower as they sway.

Sets: city (hook: close on the bridge in a storm, the towers swaying apart and together while its ends slide in their
slots, out to both towers over Kuala Lumpur; fix1: x-ray, a concrete core and a ring of columns, the sway halves; stat:
dusk; closer: night, the towers lit and fireworks), ship (break1: a ship loaded with steel girders under a price tag),
ground (break2: double weight on cracked limestone full of caves, a tower starts to tilt; fix2: both towers slide 60 m
onto softer rock and piles go down 114 m), bridge (break3: a fire on the 40th floor and the long stairs down; fix3:
the bridge, people cross to the other tower; break4: a bolted bridge snaps in the storm; fix4: bearings, the ends
slide, the legs pivot on hinges), race (reveal: the Japanese and the Korean tower race up; Korea starts a month late
and tops out first), tag (a coffee shop: two towers connected in the sky, and your phone can't join the Wi-Fi).
"""
from v2_base import *  # noqa: F401,F403
from burjalarab import path_of, saudi_man  # noqa: E402
from liberty import rain, lightning  # noqa: E402
from bridge import wind  # noqa: E402
from taipei import firework  # noqa: E402
from windtower import arrow  # noqa: E402

SILVER = ("#D5DCE6", "#A9B3C2", "#7D889B", "#465166")
GLASS_B = "#3E5C7E"
TX = 105.0                                       # tower centres at -TX / +TX (world)
TW = 46.0                                        # half width of a tower's base (world, 1 m = 2 units)
BRIDGE_Y = -340.0                                # 170 m
LEG_Y = -240.0                                   # the legs sit on floor 29 (about 120 m)
DUSKP = {"top": "#0A0F2E", "upper": "#24215C", "mid": "#5B3A7A", "low": "#D0705E", "horizon": "#F6A86A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STORMP = {"top": "#05070F", "upper": "#0E1424", "mid": "#1B2436", "low": "#2A3548", "horizon": "#3A475C",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#3A3A78", "horizon": "#7A5A9A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
# (height from, height to, half width) of the stacked sections, world units
SECTIONS = [(0, 560, 46), (560, 640, 41), (640, 700, 35), (700, 744, 29), (744, 772, 22), (772, 790, 15)]
SPIRE = (790, 904)


def sway_x(y, sw):
    """Sideways offset of a tower point at height -y for a sway sw (units at the top)."""
    h = clamp(-y / SPIRE[1])
    return sw * h * h


def tower(c, cx, t, sw=0.0, lit=0.0, night=0.0, xray=0.0, slot=True, a=1.0, build=1.0):
    """One Petronas tower centred on x = cx (world, base on y = 0); sw = sway at the top; build 0..1 grows it."""
    if a <= 0 or build <= 0:
        return
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    top_h = SPIRE[1] * build
    for y0, y1, hw in SECTIONS:
        if y0 >= top_h:
            break
        y1_ = min(y1, top_h)
        pts = [(cx - hw + sway_x(-y0, sw), -y0), (cx + hw + sway_x(-y0, sw), -y0), (cx + hw + sway_x(-y1_, sw), -y1_),
               (cx - hw + sway_x(-y1_, sw), -y1_)]
        dk = 0.45 * night
        c.drawPath(path_of(pts, close=True), lin_paint(cx - hw, 0, cx + hw, 0,
                                                        [mix(SILVER[3], "#141A2A", dk), mix(SILVER[1], "#2A3450", dk),
                                                         mix(SILVER[0], "#56627E", dk), mix(SILVER[2], "#222A40", dk),
                                                         mix(SILVER[3], "#141A2A", dk)],
                                                        [0.0, 0.3, 0.45, 0.7, 1.0]))
        # floor bands and the fluted columns
        yy = y0 + 8
        while yy < y1_:
            ox = sway_x(-yy, sw)
            c.drawLine(cx - hw + ox, -yy, cx + hw + ox, -yy,
                       P(mix(GLASS_B, "#FFD58A", lit), 0.45 + 0.3 * lit, stroke=2.2))
            yy += 8
        for k in range(-2, 3):
            xx = cx + k * hw * 0.42
            c.drawLine(xx + sway_x(-y0, sw), -y0, xx + sway_x(-y1_, sw), -y1_, P("#FFFFFF", 0.22, stroke=2))
    if top_h > SPIRE[0]:                                                   # the pinnacle with its rings
        y1_ = min(SPIRE[1], top_h)
        bx, tx_ = cx + sway_x(-SPIRE[0], sw), cx + sway_x(-y1_, sw)
        c.drawPath(path_of([(bx - 7, -SPIRE[0]), (bx + 7, -SPIRE[0]), (tx_ + 1.5, -y1_), (tx_ - 1.5, -y1_)], close=True),
                   lin_paint(bx - 7, 0, bx + 7, 0, [SILVER[2], SILVER[0], SILVER[3]]))
        for k in range(6):
            ry = SPIRE[0] + 10 + k * 14
            if ry < y1_:
                rx = cx + sway_x(-ry, sw)
                c.drawOval(R(rx - 10 + k, -ry - 2.5, 20 - 2 * k, 5), P(mix(SILVER[1], "#FFFFFF", lit), 0.9))
        if build >= 1:
            beacon(c, tx_, -y1_, t, hz=0.9, r=4)
    if slot and build >= 0.45:                                             # the bridge's slot in the tower face
        side = 1 if cx < 0 else -1
        fx = cx + side * TW + sway_x(BRIDGE_Y, sw)
        c.drawRect(R(fx - (8 if side > 0 else 0), BRIDGE_Y - 18, 8, 20), P("#0B1220", 0.9))
    if xray > 0:                                                           # the concrete core and the ring of columns
        for k in range(8):
            xx = cx - 38 + k * 76 / 7
            pts = [(xx + sway_x(-yy, sw), -yy) for yy in range(0, 700, 20)]
            c.drawPath(path_of(pts), P("#CBD5E1", 0.95 * xray, stroke=5))
        pts = [(cx + sway_x(-yy, sw), -yy) for yy in range(0, 760, 20)]
        c.drawPath(path_of(pts), P("#94A3B8", 0.8 * xray, stroke=26))
        c.drawPath(path_of(pts), P("#E2E8F0", 0.9 * xray, stroke=6))
    if a < 1:
        c.restore()


def sky_bridge(c, t, swl, swr, lit=0.0, a=1.0, snap=0.0, bolts=0.0, bear=0.0):
    """The two-floor bridge between the faces of the two towers at 170 m and its two legs down to floor 29 (world).
    swl / swr are the sways of the left / right tower; the deck keeps its length, so its ends slide in the slots."""
    if a <= 0:
        return
    lf = -TX + TW + sway_x(BRIDGE_Y, swl)                                  # the left tower's face
    rf = TX - TW + sway_x(BRIDGE_Y, swr)
    mid = (lf + rf) / 2
    half = (2 * (TX - TW)) / 2 + 6                                         # the deck reaches 6 units into each tower
    x0, x1 = mid - half, mid + half
    deck = [mix("#8FA0B8", "#FFE7B8", lit), mix("#5B6B82", "#C9A877", lit)]
    if snap <= 0:
        c.drawRect(R(x0, BRIDGE_Y - 18, x1 - x0, 18), lin_paint(0, BRIDGE_Y - 18, 0, BRIDGE_Y, deck, a=a))
        for k in range(1, 9):
            xx = lerp(x0, x1, k / 9)
            c.drawLine(xx, BRIDGE_Y - 17, xx, BRIDGE_Y - 1, P("#E2E8F0", 0.6 * a, stroke=1.5))
        c.drawLine(x0, BRIDGE_Y - 9, x1, BRIDGE_Y - 9, P("#E2E8F0", 0.7 * a, stroke=2))
    else:                                                                  # it breaks in the middle and the halves drop
        for side, xa, xb in ((-1, x0, mid), (1, mid, x1)):
            c.save()
            px = xa if side < 0 else xb
            c.translate(px, BRIDGE_Y - 9)
            c.rotate(-side * 24 * e_in(clamp(snap)))
            c.drawRect(R(xa - px, -9, xb - xa, 18), lin_paint(0, -9, 0, 9, deck, a=a))
            c.restore()
    # the legs: an upside-down V from under the deck down to the tower faces
    lm = (lf + rf) / 2
    for side, fx in ((-1, lf), (1, rf)):
        c.drawLine(lm, BRIDGE_Y + 2, fx, LEG_Y, P(mix("#94A3B8", "#FFE7B8", lit * 0.6), a, stroke=4))
        if bear > 0:
            c.drawCircle(fx, LEG_Y, 6, P("#FACC15", bear * a))
            c.drawCircle(fx, LEG_Y, 6, P("#0B1220", bear * a, stroke=1.5))
    if bear > 0:
        c.drawCircle(lm, BRIDGE_Y + 2, 5, P("#FACC15", bear * a))
        for ex in (x0 + 3, x1 - 3):                                        # rollers at the deck ends
            for k in range(3):
                c.drawCircle(ex + (k - 1) * 3, BRIDGE_Y + 1.5, 1.6, P("#FACC15", bear * a))
    if bolts > 0:
        for ex in (x0 + 4, x1 - 4):
            for k in range(3):
                c.drawCircle(ex, BRIDGE_Y - 15 + k * 6, 2.2, P("#EF4444", bolts * a))
    if lit > 0:
        add_glow(c, mid, BRIDGE_Y - 9, 70, "#FFE7B8", 0.35 * lit * a)


def kl_city(c, t, night=0.0, a=1.0):
    """Kuala Lumpur around the towers: the KL tower on a hill, blocks, the mall at the foot (world)."""
    c.drawRect(R(-2000, 0, 4000, 1400), lin_paint(0, 0, 0, 800, [mix("#334155", "#0B1220", night), "#05080C"], a=a))
    v2.ridge(c, -1800, 1800, 0, 120, mix("#2A4A3A", "#0C1A16", night), mix("#1C3428", "#08120E", night), seed=21, step=120, rough=0.4)
    skyline_night(c, -1500, -330, 0, seed=11, hmin=40, hmax=200, lit=0.25 + 0.5 * night)
    skyline_night(c, 330, 1500, 0, seed=13, hmin=40, hmax=220, lit=0.25 + 0.5 * night)
    kx = 520.0                                                             # the KL tower with its pod
    c.drawRect(R(kx - 6, -330, 12, 330), P(mix("#64748B", "#1E293B", night), a))
    c.drawOval(R(kx - 26, -350, 52, 34), P(mix("#94A3B8", "#334155", night), a))
    c.drawLine(kx, -350, kx, -420, P("#94A3B8", a, stroke=3))
    beacon(c, kx, -420, t, hz=0.7, r=3)
    c.drawRect(R(-230, -46, 460, 46), lin_paint(0, -46, 0, 0, [mix("#9CA3AF", "#3A4256", night), mix("#6B7280", "#202636", night)], a=a))
    if night > 0:
        for k in range(10):
            c.drawRect(R(-215 + k * 44, -34, 30, 14), P("#FFD58A", 0.7 * night * a))


def ship(c, x, y, s, t, a=1.0):
    """A cargo ship loaded with steel girders (screen), waterline on y."""
    c.save()
    c.translate(x, y + math.sin(t * 1.6) * 6)
    c.rotate(math.sin(t * 1.2) * 1.5)
    c.scale(s, s)
    c.drawPath(path_of([(-330, -60), (330, -60), (290, 40), (-300, 40)], close=True), lin_paint(0, -60, 0, 40, ["#B91C1C", "#7F1D1D"], a=a))
    c.drawRect(R(-330, -70, 660, 14), P("#F8FAFC", a))
    c.drawRect(R(200, -190, 100, 120), P("#F8FAFC", a))
    for k in range(3):
        c.drawRect(R(212 + k * 30, -175, 20, 16), P("#1E3A8A", a))
    for row in range(4):                                                   # stacked steel girders (I-beams end-on)
        for k in range(6):
            gx = -290 + k * 76
            gy = -96 - row * 34
            c.drawRect(R(gx, gy, 64, 6), P("#94A3B8", a))
            c.drawRect(R(gx + 28, gy, 8, 30), P("#94A3B8", a))
            c.drawRect(R(gx, gy + 24, 64, 6), P("#94A3B8", a))
    c.restore()


def price_tag(c, x, y, s, t, a=1.0, text_="$$$"):
    """A swinging price tag (screen)."""
    c.save()
    c.translate(x, y)
    c.rotate(math.sin(t * 2.2) * 8)
    c.scale(s, s)
    c.drawLine(0, -120, 0, -40, P("#E5E7EB", a, stroke=4))
    c.drawPath(path_of([(-90, -40), (90, -40), (110, 10), (90, 110), (-90, 110), (-110, 10)], close=True), P("#FACC15", a))
    c.drawCircle(0, -20, 9, P("#1F2937", a))
    text(c, text_, 0, 70, 64, "#1F2937", "Poppins-Black", a=a)
    c.restore()


def flag(c, x, y, w, kind, t, a=1.0):
    """A small waving flag on a pole (screen): 'jp' or 'kr' (simplified)."""
    c.drawLine(x, y, x, y - w * 1.4, P("#E5E7EB", a, stroke=4))
    fy = y - w * 1.4
    wave_ = math.sin(t * 5) * 3
    c.drawRect(R(x, fy, w, w * 0.66 + wave_ * 0.2), P("#F8FAFC", a))
    cx, cy = x + w / 2, fy + w * 0.33
    if kind == "jp":
        c.drawCircle(cx, cy, w * 0.18, P("#BC002D", a))
    else:
        c.drawArc(R(cx - w * 0.17, cy - w * 0.17, w * 0.34, w * 0.34), 180, 180, True, P("#CD2E3A", a))
        c.drawArc(R(cx - w * 0.17, cy - w * 0.17, w * 0.34, w * 0.34), 0, 180, True, P("#0047A0", a))
        for dx, dy in ((-0.36, -0.2), (0.36, -0.2), (-0.36, 0.2), (0.36, 0.2)):
            for k in range(3):
                c.drawLine(cx + dx * w - 5, cy + dy * w + (k - 1) * 3, cx + dx * w + 5, cy + dy * w + (k - 1) * 3, P("#111827", a, stroke=1.6))


def crane(c, x, y, s, t, a=1.0):
    """A tower crane on top of a growing tower (screen), base at (x, y)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRect(R(-6, -120, 12, 120), P("#FACC15", a))
    c.drawRect(R(-90, -132, 170, 10), P("#FACC15", a))
    c.drawRect(R(-90, -122, 26, 18), P("#475569", a))
    hx = 50 + math.sin(t * 1.5) * 16
    c.drawLine(hx, -122, hx, -70, P("#1F2937", a, stroke=2))
    c.drawRect(R(hx - 10, -70, 20, 6), P("#94A3B8", a))
    c.restore()


def wifi(c, x, y, r, t, ok=0.0, a=1.0):
    """A Wi-Fi symbol whose arcs blink in turn (searching), red cross when it fails (screen)."""
    for k in range(3):
        on = 1.0 if int(t * 4) % 4 > k else 0.25
        c.drawArc(R(x - r * (k + 1) / 3, y - r * (k + 1) / 3, 2 * r * (k + 1) / 3, 2 * r * (k + 1) / 3), 225, 90, False,
                  P("#F8FAFC", a * on, stroke=r * 0.12))
    c.drawCircle(x, y, r * 0.08, P("#F8FAFC", a))


# ====================================================================================== the episode
class Petronas(EpisodeV2):
    BUILD_NO = 72
    FIRST_SET = "city"
    CLEAR = "#0B1220"
    TITLE = {"en": "PETRONAS TOWERS", "ar_sa": "أبراج بتروناس"}
    EMPH = {"en": ["CONGRATS", "HANG", "LOOSE", "BRIDGE", "SKYSCRAPERS", "SLIDE", "SWAY", "PETRONAS", "TWIN", "TOWERS",
                   "YOURSELF", "STEEL", "SHIPPED", "HUGE", "PRICE", "SUPER", "CONCRETE", "TWICE", "DOUBLES", "WEIGHT",
                   "LIMESTONE", "HOLES", "SHIFT", "SIXTY", "SOFTER", "PILES", "HUNDRED", "DEEP", "FIRE", "FORTIETH",
                   "LONG", "ESCAPE", "SEVENTY", "STORM", "SWAYS", "SNAP", "BOLTED", "BEARINGS", "SLIDES", "FOLLOW",
                   "LIGHTHOUSE", "ALEXANDRIA", "JAPAN", "KOREA", "RACE", "MONTH", "FIRST", "FIFTY", "EIGHTY", "SIX",
                   "TALLEST", "CONNECTED", "SKY", "CONNECT", "WI-FI"],
            "ar_sa": ["مبروك", "جسر", "السما", "برجين", "سايب", "ينزلق", "تمايلوا", "أبراج", "بتروناس", "بيدك", "الحديد",
                      "نار", "خرسانة", "قوية", "ضعف", "تضاعف", "الوزن", "جيري", "فراغات", "ستين", "ألين", "أعمدة",
                      "وأربعطعش", "حريق", "الأربعين", "طويل", "بدورين", "وسبعين", "تهرب", "العاصفة", "ينكسر", "مربوط",
                      "محامل", "تابعني", "منارة", "الإسكندرية", "يابانية", "كورية", "مسابقة", "شهر", "قبل", "أربعمية",
                      "وثمانين", "سنين", "متصلين", "تتصل", "فاي"]}
    KEYS = {"ar_sa": {
        ("hook", "HANG"): "تعلق", ("hook", "LOOSE"): "سايب", ("hook", "BRIDGE"): "جسر", ("hook", "SKYSCRAPERS"): "برجين",
        ("hook", "SLIDE"): "ينزلق", ("hook", "SWAY"): "تمايلوا", ("hook", "CONGRATS"): "مبروك", ("hook", "PETRONAS"): "بتروناس",
        ("break1", "STEEL"): "الحديد", ("break1", "SHIPPED"): "ينجاب", ("break1", "HUGE"): "سعره", ("break1", "PRICE"): "نار",
        ("fix1", "SUPER"): "قوية", ("fix1", "CONCRETE"): "خرسانة", ("fix1", "FIGHTS"): "تقاوم", ("fix1", "TWICE"): "ضعف",
        ("break2", "CONCRETE"): "الخرسانة", ("break2", "DOUBLES"): "تضاعف", ("break2", "WEIGHT"): "الوزن",
        ("break2", "HALF"): "نص", ("break2", "LIMESTONE"): "جيري", ("break2", "HOLES"): "فراغات",
        ("fix2", "SHIFT"): "تزحزح", ("fix2", "SIXTY"): "ستين", ("fix2", "SOFTER"): "ألين", ("fix2", "DIG"): "تنزل",
        ("fix2", "PILES"): "أعمدة", ("fix2", "HUNDRED"): "مية", ("fix2", "DEEP"): "اربعطعش",
        ("break3", "FIRE"): "حريق", ("break3", "FORTIETH"): "الأربعين", ("break3", "LONG"): "طويل", ("break3", "WALK"): "مشوار",
        ("fix3", "BRIDGE"): "جسر", ("fix3", "JOINS"): "يربطهم", ("fix3", "HUNDRED"): "مية", ("fix3", "ESCAPE"): "تهرب",
        ("fix3", "OTHER"): "الثاني",
        ("break4", "STORM"): "العاصف", ("break4", "SWAYS"): "يتمايل", ("break4", "OWN"): "كيفه", ("break4", "BOLTED"): "المربوط",
        ("break4", "SNAP"): "ينكسر",
        ("fix4", "BRIDGE"): "الجسر", ("fix4", "BOLTED"): "مربوط", ("fix4", "BEARINGS"): "محامل", ("fix4", "SLIDES"): "يدخل",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "JAPAN"): "يابانية", ("reveal", "KOREA"): "كورية", ("reveal", "RACE"): "مسابقة", ("reveal", "MONTH"): "شهر",
        ("reveal", "TOP"): "فوق", ("reveal", "FIRST"): "قبل",
        ("stat", "FOUR"): "أربعمية", ("stat", "EIGHTY"): "ثمانيه", ("stat", "SIX"): "سنين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "CONNECTED"): "متصلين", ("tag", "SKY"): "السما", ("tag", "CONNECT"): "تتصل", ("tag", "COFFEE"): "الكوفي",
        ("tag", "WIFI"): "فاي"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Lighthouse of Alexandria"),
                   "stat": [("452 m", "TALL"), ("88", "FLOORS"), ("6 yrs", "WORLD'S TALLEST")],
                   "L": {"loose": "A LOOSE BRIDGE", "slides": "IT SLIDES AS THEY SWAY", "name": "PETRONAS TWIN TOWERS",
                         "steel": "STEEL: SHIPPED IN", "price": "AT A HUGE PRICE", "concrete": "SUPER-STRONG CONCRETE",
                         "twice": "FIGHTS SWAY 2x BETTER", "heavy": "2x THE WEIGHT", "lime": "LIMESTONE FULL OF HOLES",
                         "soft": "SOFTER ROCK", "shift": "60 m OVER", "piles": "PILES 114 m DEEP", "fire": "FIRE ON FLOOR 40",
                         "walk": "A VERY LONG WALK DOWN", "bridge": "A BRIDGE 170 m UP", "escape": "ESCAPE TO THE OTHER TOWER",
                         "storm": "EACH TOWER SWAYS ITS OWN WAY", "snap": "BOLTED? IT SNAPS", "bear": "ON BEARINGS: IT SLIDES",
                         "japan": "JAPAN", "korea": "KOREA", "race": "A RACE", "late": "A MONTH LATE...", "first": "...TOP FIRST!",
                         "nowifi": "CAN'T CONNECT", "wifi": "COFFEE SHOP WI-FI"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: منارة الإسكندرية"),
                      "stat": [("452", "متر"), ("88", "دور"), ("6", "سنين الأطول")],
                      "L": {"loose": "جسر سايب", "slides": "ينزلق إذا تمايلوا", "name": "أبراج بتروناس",
                            "steel": "الحديد ينجاب من برا", "price": "وسعره نار", "concrete": "خرسانة قوية مرة",
                            "twice": "تقاوم التمايل ضعف", "heavy": "ضعف الوزن", "lime": "صخر جيري مليان فراغات",
                            "soft": "صخر ألين", "shift": "60 متر", "piles": "أعمدة لين 114 متر", "fire": "حريق في الدور 40",
                            "walk": "مشوار طويل للأرض", "bridge": "جسر على 170 متر", "escape": "اهرب للبرج الثاني",
                            "storm": "كل برج على كيفه", "snap": "مربوط؟ ينكسر", "bear": "على محامل: ينزلق",
                            "japan": "اليابان", "korea": "كوريا", "race": "مسابقة", "late": "تأخروا شهر...", "first": "...ووصلوا قبل!",
                            "nowifi": "ما يتصل", "wifi": "واي فاي الكوفي"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "hang": ("hook", "HANG", 0.05), "loose": ("hook", "LOOSE", 0.1), "bridge": ("hook", "BRIDGE", 0.15),
            "sky": ("hook", "SKYSCRAPERS", 0.3), "slide": ("hook", "SLIDE", 0.45), "sway": ("hook", "SWAY", 0.55),
            "congrats": ("hook", "CONGRATS", 0.7), "name": ("hook", "PETRONAS", 0.88),
            "steel": ("break1", "STEEL", 0.15), "shipped": ("break1", "SHIPPED", 0.45), "huge": ("break1", "HUGE", 0.8),
            "price": ("break1", "PRICE", 0.9),
            "super": ("fix1", "SUPER", 0.2), "concrete": ("fix1", "CONCRETE", 0.35), "fights": ("fix1", "FIGHTS", 0.55),
            "twice": ("fix1", "TWICE", 0.8),
            "concrete2": ("break2", "CONCRETE", 0.08), "doubles": ("break2", "DOUBLES", 0.2), "weight": ("break2", "WEIGHT", 0.35),
            "half": ("break2", "HALF", 0.5), "lime": ("break2", "LIMESTONE", 0.75), "holes": ("break2", "HOLES", 0.92),
            "shift": ("fix2", "SHIFT", 0.08), "sixty": ("fix2", "SIXTY", 0.25), "softer": ("fix2", "SOFTER", 0.4),
            "dig": ("fix2", "DIG", 0.55), "piles": ("fix2", "PILES", 0.6), "hundred": ("fix2", "HUNDRED", 0.75),
            "deep": ("fix2", "DEEP", 0.95),
            "fire": ("break3", "FIRE", 0.15), "fortieth": ("break3", "FORTIETH", 0.35), "long": ("break3", "LONG", 0.7),
            "walk": ("break3", "WALK", 0.85),
            "bridge3": ("fix3", "BRIDGE", 0.15), "joins": ("fix3", "JOINS", 0.25), "hundred3": ("fix3", "HUNDRED", 0.4),
            "escape": ("fix3", "ESCAPE", 0.75), "other": ("fix3", "OTHER", 0.9),
            "storm": ("break4", "STORM", 0.12), "sways": ("break4", "SWAYS", 0.3), "own": ("break4", "OWN", 0.5),
            "bolted": ("break4", "BOLTED", 0.75), "snap": ("break4", "SNAP", 0.92),
            "bridge4": ("fix4", "BRIDGE", 0.08), "notbolted": ("fix4", "BOLTED", 0.25), "bearings": ("fix4", "BEARINGS", 0.5),
            "slides": ("fix4", "SLIDES", 0.7),
            "follow": ("cta", "FOLLOW", 0.35),
            "japan": ("reveal", "JAPAN", 0.12), "korea": ("reveal", "KOREA", 0.3), "race": ("reveal", "RACE", 0.45),
            "month": ("reveal", "MONTH", 0.62), "top": ("reveal", "TOP", 0.85), "first": ("reveal", "FIRST", 0.95),
            "s1": ("stat", "FOUR", 0.05), "s2": ("stat", "EIGHTY", 0.4), "s3": ("stat", "SIX", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_connected": ("tag", "CONNECTED", 0.15), "t_sky": ("tag", "SKY", 0.3), "t_coffee": ("tag", "COFFEE", 0.8),
            "t_wifi": ("tag", "WIFI", 0.95)})
        T["t_connect"] = self.w("tag", "CONNECT", 0.65, nth=1 if self.lang == "en" else 0)
        T["price1"] = max(T["price"], T["huge"]) + 0.15
        T["holes1"] = max(T["holes"], T["lime"]) + 0.15
        T["walk1"] = max(T["walk"], T["long"]) + 0.15
        T["snap1"] = max(T["snap"], T["bolted"]) + 0.1
        T["twice1"] = max(T["twice"], T["fights"]) + 0.2
        T["deep1"] = max(T["deep"], T["hundred"]) + 0.2
        T["other1"] = max(T["other"], T["escape"]) + 0.2
        T["slides1"] = max(T["slides"], T["bearings"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "ship", 1)
        self.cut(s("fix1") - 0.12, "city", -1)
        self.cut(s("break2") - 0.12, "ground", 1)
        self.cut(s("break3") - 0.12, "bridge", -1)
        self.cut(s("reveal") - 0.12, "race", 1)
        self.cut(s("stat") - 0.12, "city", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- city camera: close on the bridge in the storm, out to both towers
        cm = Camera(0, BRIDGE_Y + 10, 4.4)
        cm.key(0.05, 0, BRIDGE_Y + 6, 4.1, 1.2)
        cm.key(max(1.2, T["congrats"] - 1.0), 0, -262, 0.84, max(1.0, T["name"] - T["congrats"] + 1.0))
        cm.key(s("fix1") - 0.12, 0, -262, 0.84, 0.0)
        cm.key(s("stat") - 0.12, 0, -382, 0.72, 0.0)
        cm.key(s("closer") - 0.1, 0, -275, 0.8, 1.0)
        self.cam = cm
        self.spans = [(T["price1"], T["twice1"] + 0.3), (T["holes1"], T["deep1"] + 0.3), (T["walk1"], T["other1"] + 0.3),
                      (T["snap1"], T["slides1"] + 0.3)]
        self.shakes = [(T["sway"], 0.5, 6), (T["congrats"], 0.35, 8), (T["holes1"], 0.6, 12), (T["fire"], 0.3, 6),
                       (T["storm"], 0.6, 8), (T["snap1"], 0.6, 14), (T["first"], 0.3, 6), (s("closer") + 0.2, 0.35, 9)]

    def sways(self, t, amp):
        """Each tower sways its own way (different periods)."""
        return amp * math.sin(t * 2 * math.pi / 2.6), amp * math.sin(t * 2 * math.pi / 3.3 + 1.7)

    # ------------------------------------------------------------------ set: city (hook, fix1, stat, closer)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1") - 0.12
        stat = s("stat") - 0.12 <= t < s("closer") - 0.1
        closer = t >= s("closer") - 0.1
        gy = self.to_screen(cam, 0, 0)[1]
        if hook:
            v2.sky(c, W, H, 0.0, pal=STORMP, horizon_y=gy)
        elif stat:
            v2.sky(c, W, H, 0.0, pal=DUSKP, horizon_y=gy)
            v2.stars(c, W, H, t, 0.3)
        elif closer:
            v2.sky(c, W, H, 0.0, pal=NIGHTP, horizon_y=gy)
            v2.stars(c, W, H, t, 0.8)
        else:
            v2.sky(c, W, H, 0.0, horizon_y=gy)
            v2.stars(c, W, H, t, 0.5)
        if hook:
            for i in range(4):
                v2.cloud(c, (i * 330 + t * 50) % (W + 600) - 300, 240 + (i % 2) * 140, 1.6, body="#1E293B", rim="#475569",
                         a=0.9, seed=i)
        night = 1.0 if (hook or closer) else (0.6 if not stat else 0.3)
        self.view(c, cam)
        kl_city(c, t, night=night)
        amp = 0.0
        if hook:
            amp = 9.0
        elif s("fix1") - 0.12 <= t < s("break2"):
            amp = 8.0 * (1 - 0.5 * prog(t, T["fights"] - 0.3, T["twice"] + 0.3))
        swl, swr = self.sways(t, amp)
        xr = prog(t, T["concrete"] - 0.4, T["concrete"] + 0.2) if s("fix1") - 0.12 <= t < s("break2") else 0.0
        lit = 1.0 if (hook or closer) else (0.5 if stat else 0.3)
        tower(c, -TX, t, sw=swl, lit=lit, night=night * 0.7, xray=xr)
        tower(c, TX, t, sw=swr, lit=lit, night=night * 0.7, xray=xr)
        sky_bridge(c, t, swl, swr, lit=lit, bear=0.0)
        c.restore()
        if hook:
            rain(c, t, a=0.8, seed=5)
            wind(c, 0, 700, W, t, n=8, a=0.6, spread=300, seed=1)
            fl = max(0.0, math.sin(t * 2.1) - 0.93) * 12
            if fl > 0:
                lightning(c, 880, 100, 600, t, int(t * 2.1), a=clamp(fl))
                c.drawRect(R(0, 0, W, H), P("#C7D2FE", 0.1 * clamp(fl)))
            if t < T["congrats"] - 0.5:                                    # arrows on the sliding ends
                k = prog(t, T["slide"] - 0.4, T["slide"]) * (1 - prog(t, T["congrats"] - 0.9, T["congrats"] - 0.5))
                if k > 0:
                    for side in (-1, 1):
                        fx, fy = self.to_screen(cam, side * (TX - TW), BRIDGE_Y - 30)
                        ph = math.sin(t * 2 * math.pi / 2.6) * side
                        arrow(c, fx, fy - 30, fx + ph * 70, fy - 30, HILITE, a=k, w=10, head=28)
        if closer:
            fk = prog(t, s("closer"), s("closer") + 0.4)
            for i, (dx, dy, col) in enumerate(((-300, -260, "#F472B6"), (300, -200, "#FDE047"), (-240, 60, "#60A5FA"),
                                                (260, 120, "#34D399"))):
                tx_, ty_ = self.to_screen(cam, 0, -620)
                period = 1.8
                t0 = s("closer") + i * 0.35
                kk = math.floor(max(0.0, t - t0) / period)
                firework(c, tx_ + dx, ty_ + dy, t, t0 + kk * period, col, a=fk)
        self.ui["cam"] = cam

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "loose", T["loose"] - 0.2, T["slide"] - 0.2, accent=HILITE, size=50)
            self.chip(540, 300, "slides", T["slide"] - 0.2, T["congrats"] - 0.2, accent="#93C5FD", size=44)
            self.chip(540, 300, "name", T["congrats"] - 0.2, s("break1") + 0.1, accent=HILITE, size=50)
            return
        if tw < s("break2") - 0.12:
            self.chip(540, 300, "concrete", T["super"] - 0.2, T["fights"] - 0.2, accent="#CBD5E1", size=46)
            self.chip(540, 300, "twice", T["fights"] - 0.2, s("break2") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["twice1"] + 0.1, s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: ship (break1)
    def draw_ship(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.0, horizon_y=900)
        c.drawRect(R(0, 900, W, H - 900), lin_paint(0, 900, 0, H, ["#1E5A80", "#0B2A40"]))
        for k in range(6):
            dashed(c, 0, 930 + k * 40, W, 930 + k * 40, "#BDE6FF", w=3, dash=50, gap=30, phase=t * 40 + k * 30, a=0.4)
        sx = lerp(1300, 560, e_out(prog(t, s("break1") - 0.1, T["shipped"] + 0.3)))
        ship(c, sx, 960, 1.15, t)
        pk = e_back(prog(t, T["huge"] - 0.4, T["huge"] + 0.1))
        if pk > 0:
            price_tag(c, 540, 620, 1.3 * pk, t)
            if t > T["price1"]:
                for k in range(10):                                         # coins flying off
                    u = (t * 1.3 + k / 10) % 1.0
                    c.drawCircle(540 + math.cos(k * 2.3) * 300 * u, 640 - math.sin(u * math.pi) * 200 + 200 * u,
                                 12, P("#FACC15", 0.9 * (1 - u)))

    def ui_ship(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "steel", T["steel"] - 0.2, T["huge"] - 0.2, accent="#CBD5E1", size=46)
        self.chip(540, 300, "price", T["huge"] - 0.2, s("fix1") - 0.15, accent=WARN, size=50)
        self.badge("alert", T["price1"], s("fix1") - 0.2, x=920, y=440)
        self.red(T["price1"], 1.2)

    # ------------------------------------------------------------------ set: ground (break2, fix2)
    def draw_ground(self, c, t):
        T, s = self.T, self.tl.s
        G = 640.0                                                           # the ground surface (screen)
        K = 2.2                                                             # px per metre
        v2.sky(c, W, H, 0.0, horizon_y=G)
        # soft rock everywhere, limestone on the left behind a steep underground cliff
        c.drawRect(R(0, G, W, H - G), lin_paint(0, G, 0, H, ["#9A6B44", "#6E4A2C"]))
        lime = path_of([(0, G), (370, G), (330, G + 150), (260, G + 420), (220, H), (0, H)], close=True)
        c.drawPath(lime, lin_paint(0, G, 0, H, ["#B5AFA6", "#857E75"]))
        rng = random.Random(6)
        for k in range(16):                                                 # caves in the limestone
            cx_ = rng.uniform(30, 300)
            cy_ = rng.uniform(G + 60, G + 560)
            if cx_ < 380 - (cy_ - G) * 0.3:
                c.drawOval(R(cx_ - 30, cy_ - 16, rng.uniform(40, 80), rng.uniform(22, 40)), P("#1C1917", 0.85))
        c.drawPath(lime, P("#78716C", 1.0, stroke=4))
        fixed = t >= s("fix2") - 0.12
        shift = e_io(prog(t, T["shift"] - 0.2, T["softer"] + 0.2)) if fixed else 0.0
        tilt = (prog(t, T["half"] - 0.2, T["holes1"] + 0.5) * 2.5) if not fixed else 0.0
        hk = prog(t, T["doubles"] - 0.3, T["weight"] + 0.2) if not fixed else 0.0
        base_x = 432 + shift * 60 * K                                       # centre between the two towers
        dx = (TX / 2) * K                                                   # half the distance between tower centres (m * K)
        for side in (-1, 1):
            tx_ = base_x + side * dx
            c.save()
            c.translate(tx_, G)
            if side < 0:
                c.rotate(-tilt)
            hw = 23.1 * K
            c.drawRect(R(-hw, -G - 40, 2 * hw, G + 40), lin_paint(-hw, 0, hw, 0, [SILVER[2], SILVER[0], SILVER[1], SILVER[3]],
                                                                    [0.0, 0.42, 0.6, 1.0]))
            yy = -10.0
            while yy > -G - 40:
                c.drawLine(-hw, yy, hw, yy, P(GLASS_B, 0.45, stroke=2.5))
                yy -= 18
            if hk > 0:                                                      # double weight pushing down
                arrow(c, 0, -420, 0, -40, WARN, a=hk, w=16, head=44)
            c.restore()
        if fixed:                                                           # the raft and the piles
            pk = prog(t, T["dig"] - 0.3, T["deep1"])
            depth = 114 * K * pk
            c.drawRect(R(base_x - dx - 60, G, 2 * dx + 120, 4.5 * K * 2), P("#9CA3AF", prog(t, T["dig"] - 0.4, T["dig"])))
            for k in range(14):
                px = base_x - dx - 50 + k * (2 * dx + 100) / 13
                d = depth * (0.55 + 0.45 * abs(math.sin(k * 1.7)))
                c.drawRect(R(px - 5, G + 10, 10, d), P("#CBD5E1", 1.0))
            if pk > 0.3:
                yy = G + 114 * K
                dashed(c, base_x + dx + 90, G, base_x + dx + 90, yy, "#FDE68A", w=4, dash=14, gap=8, a=pk)
                c.drawLine(base_x + dx + 75, yy, base_x + dx + 105, yy, P("#FDE68A", pk, stroke=4))
        if fixed and shift > 0:
            arrow(c, 300, G - 40, 300 + 60 * K * shift + 10, G - 40, HILITE, a=1.0, w=12, head=34)
        if tilt > 0.5:                                                      # cracks in the limestone
            ck = clamp((tilt - 0.5) / 1.5)
            c.drawPath(path_of([(330, G), (300, G + 60), (330, G + 120), (290, G + 200)]), P("#111827", ck, stroke=5))

    def ui_ground(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "heavy", T["doubles"] - 0.2, T["half"] - 0.2, accent=WARN, size=50)
            self.chip(540, 300, "lime", T["half"] - 0.2, s("fix2") - 0.15, accent="#D6D3D1", size=42)
            self.badge("alert", T["holes1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["holes1"], 1.2)
            return
        self.chip(540, 300, "shift", T["shift"] - 0.2, T["dig"] - 0.2, accent=HILITE, size=50)
        self.chip(540, 300, "piles", T["dig"] - 0.2, s("break3") - 0.15, accent="#FDE68A", size=46)
        self.badge("check", T["deep1"] + 0.1, s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: bridge (break3, fix3, break4, fix4, cta)
    def draw_bridge(self, c, t):
        T, s = self.T, self.tl.s
        storm = t >= s("break4") - 0.12
        vrect(c, 0, 0, W, H, ["#05070F", "#141C2E", "#1E293B"] if storm else ["#0A1238", "#16204A", "#24305E"])
        Z = 3.2                                                             # zoom on the middle of the towers
        cam = (0, -300, Z)
        if storm:
            for i in range(3):
                v2.cloud(c, (i * 360 + t * 60) % (W + 600) - 300, 300 + (i % 2) * 160, 1.5, body="#1E293B", rim="#475569",
                         a=0.85, seed=i + 3)
        amp = 0.0
        snap = 0.0
        bolts = 0.0
        bear = 0.0
        show_bridge = 0.0
        if t < s("fix3") - 0.12:
            show_bridge = 0.0
        elif t < s("break4") - 0.12:
            show_bridge = e_out(prog(t, T["bridge3"] - 0.3, T["joins"] + 0.3))
        elif t < s("fix4") - 0.12:
            amp = 14.0 * prog(t, T["storm"] - 0.3, T["sways"])
            show_bridge = 1.0
            bolts = 1.0
            snap = prog(t, T["snap"] - 0.15, T["snap"] + 0.5)
        else:
            amp = 14.0
            show_bridge = 1.0
            bear = prog(t, T["bearings"] - 0.3, T["bearings"] + 0.2)
        swl, swr = self.sways(t, amp) if amp > 0 else (0.0, 0.0)
        self.view(c, cam)
        tower(c, -TX, t, sw=swl, lit=0.6, night=0.6)
        tower(c, TX, t, sw=swr, lit=0.6, night=0.6)
        if show_bridge > 0:
            c.save()
            c.translate(0, (1 - show_bridge) * -260)
            sky_bridge(c, t, swl, swr, lit=0.6, a=show_bridge, snap=snap, bolts=bolts, bear=bear)
            c.restore()
        if t < s("fix3") - 0.12:                                            # fire on floor 40 and the stairs down
            fk = prog(t, T["fire"] - 0.3, T["fire"] + 0.2)
            fy = -322.0
            for k in range(5):
                fx = -TX - 30 + k * 15
                fl = 8 + 5 * math.sin(t * 13 + k)
                c.drawPath(path_of([(fx - 5, fy), (fx + 5, fy), (fx, fy - fl)], close=True), P("#F97316", fk))
                c.drawCircle(fx, fy - 2, 3, P("#FDE047", fk))
            for k in range(4):                                              # smoke
                u = (t * 0.6 + k / 4) % 1.0
                c.drawCircle(-TX - 10 + u * 20, fy - 10 - u * 60, 6 + u * 12, P("#6B7280", 0.45 * fk * (1 - u)))
            wk = prog(t, T["long"] - 0.4, T["walk1"] + 0.3)
            if wk > 0:                                                      # zigzag stairs down the tower
                pts = []
                yy = fy + 6
                k = 0
                while yy < -150:
                    pts.append((-TX + (-12 if k % 2 else 12), yy))
                    yy += 8
                    k += 1
                pp = path_of(pts)
                pm = skia.PathMeasure(pp, False)
                seg = skia.Path()
                pm.getSegment(0, pm.getLength() * wk, seg, True)
                c.drawPath(seg, P("#FDE68A", 0.9, stroke=2))
        if s("fix3") - 0.12 <= t < s("break4") - 0.12:                      # people crossing to the other tower
            ek = prog(t, T["escape"] - 0.4, T["other1"] + 0.6)
            for k in range(6):
                u = clamp(ek * 1.4 - k * 0.08)
                if 0 < u < 1:
                    px = lerp(-TX + TW - 4, TX - TW + 4, u)
                    c.drawCircle(px, BRIDGE_Y - 8, 2.2, P("#FDE68A", 1.0))
                    c.drawLine(px, BRIDGE_Y - 6, px, BRIDGE_Y - 2, P("#FDE68A", 1.0, stroke=1.5))
        c.restore()
        if storm:
            rain(c, t, a=0.7, seed=9)
            wind(c, 0, 900, W, t, n=8, a=0.6, spread=300, seed=2)
            if 0 < snap < 1 and t < s("fix4") - 0.12:
                c.drawRect(R(0, 0, W, H), P("#FFFFFF", 0.35 * (1 - snap)))
        self.ui["swl"], self.ui["swr"] = swl, swr
        self.ui["cam"] = cam

    def ui_bridge(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "fire", T["fire"] - 0.2, T["long"] - 0.2, accent=WARN, size=48)
            self.chip(540, 300, "walk", T["long"] - 0.2, s("fix3") - 0.15, accent="#FDE68A", size=46)
            self.badge("alert", T["walk1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["walk1"], 1.2)
            return
        if tw < s("break4") - 0.12:
            self.chip(540, 300, "bridge", T["bridge3"] - 0.2, T["escape"] - 0.2, accent=HILITE, size=48)
            self.chip(540, 300, "escape", T["escape"] - 0.2, s("break4") - 0.15, accent=GOOD, size=42)
            self.badge("check", T["other1"] + 0.1, s("break4") - 0.15, x=920, y=440)
            return
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "storm", T["storm"] - 0.2, T["bolted"] - 0.2, accent="#93C5FD", size=40)
            self.chip(540, 300, "snap", T["bolted"] - 0.2, s("fix4") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["snap1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["snap1"], 1.2)
            return
        self.chip(540, 300, "bear", T["notbolted"] - 0.2, s("cta") - 0.15, accent=HILITE, size=46)
        bk = self.span(T["bearings"] - 0.3, s("cta") - 0.15)
        if bk > 0:                                                          # arrows at the sliding ends
            cam = self.ui.get("cam", (0, -300, 3.2))
            for side, sw_ in ((-1, self.ui.get("swl", 0.0)), (1, self.ui.get("swr", 0.0))):
                fx, fy = self.to_screen(cam, side * (TX - TW) + sway_x(BRIDGE_Y, sw_), BRIDGE_Y - 34)
                ph = math.sin(tw * 2 * math.pi / (2.6 if side < 0 else 3.3) + (0 if side < 0 else 1.7))
                arrow(c, fx, fy - 20, fx + ph * 60, fy - 20, HILITE, a=bk, w=10, head=26)
        self.badge("check", T["slides1"] + 0.1, s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: race (reveal)
    def draw_race(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.0, horizon_y=1150)
        c.drawRect(R(0, 1150, W, H - 1150), lin_paint(0, 1150, 0, H, ["#334155", "#0B1220"]))
        t0 = s("reveal")
        jp = prog(t, T["japan"] - 0.3, T["top"] + 1.2)                       # Japan: early start, steady
        kr_start = T["month"] - 0.6
        kr = prog(t, max(T["korea"], kr_start - 0.8), T["top"] + 0.2)          # Korea: a month later, faster, first
        kr = e_in(kr) if t < T["top"] + 0.2 else 1.0
        jp = min(jp, 0.97) if t < T["first"] + 0.6 else jp
        for side, kind, k in ((-1, "jp", jp), (1, "kr", kr)):
            cx = 540 + side * 220
            sc = 0.8
            c.save()
            c.translate(cx, 1150)
            c.scale(sc, sc)
            tower(c, 0, t, sw=0.0, lit=0.3, night=0.2, slot=False, build=max(0.02, k))
            c.restore()
            topy = 1150 - SPIRE[1] * sc * max(0.02, k)
            if k < 0.995:
                crane(c, cx, topy, 0.9, t)
            flag(c, cx + 60, 1150 - 10, 60, kind, t)
            if side > 0 and k >= 0.995:
                hats_in_the_air(c, [cx - 40, cx, cx + 40], topy - 10, t, T["top"] + 0.2)

    def ui_race(self, c, t, tw):
        T, s = self.T, self.tl.s
        v2.chip(c, 320, 1200, self.L["japan"], self.span(T["japan"] - 0.2, s("stat") - 0.15), accent="#FCA5A5", size=40)
        v2.chip(c, 760, 1200, self.L["korea"], self.span(T["korea"] - 0.2, s("stat") - 0.15), accent="#93C5FD", size=40)
        self.chip(540, 300, "race", T["race"] - 0.2, T["month"] - 0.2, accent=HILITE, size=50)
        self.chip(540, 300, "late", T["month"] - 0.2, T["top"] - 0.1, accent="#93C5FD", size=46)
        self.chip(540, 300, "first", T["top"] - 0.1, s("stat") - 0.15, accent=GOOD, size=50)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#3B2A22", "#2A1D17"])
        c.drawRect(R(0, 0, W, 760), lin_paint(0, 0, 0, 760, ["#0B1430", "#1E2A55"]))       # a window on the night city
        for side in (-1, 1):
            c.save()
            c.translate(540 + side * 120, 760)
            c.scale(0.62, 0.62)
            tower(c, 0, t, sw=0.0, lit=1.0, night=0.8, slot=False)
            c.restore()
        c.drawRect(R(448, 760 + BRIDGE_Y * 0.62 - 12, 184, 12), P("#FFE7B8", 0.9))
        c.drawRect(R(0, 740, W, 30), P("#5B4636"))
        c.drawRect(R(0, 1080, W, H - 1080), P("#4A3426"))
        c.drawRRect(rr(160, 980, 760, 40, 10), P("#8A5A3C"))                 # the table
        c.drawRect(R(520, 1020, 40, 200), P("#6B4430"))
        c.drawRRect(rr(220, 930, 70, 50, 10), P("#F8FAFC"))                  # a coffee cup
        c.drawPath(path_of([(290, 945), (310, 950), (300, 970), (288, 968)]), P("#F8FAFC", 1.0, stroke=6))
        for k in range(3):
            u = (t * 0.7 + k / 3) % 1.0
            c.drawLine(240 + k * 14, 920 - u * 60, 246 + k * 14, 900 - u * 60, P("#E5E7EB", 0.5 * (1 - u), stroke=4))
        if self.rtl:
            saudi_man(c, 760, 1180, 330, t, pose="look", face=-1)
        else:
            person(c, 760, 1180, 330, "#2563EB", t, pose="look", face=-1, hair="#3B2A20")
        c.drawRRect(rr(600, 840, 70, 120, 12), P("#111827"))                 # the phone
        c.drawRRect(rr(606, 848, 58, 104, 8), P("#1E3A8A"))
        wifi(c, 635, 920, 46, t)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "wifi", T["t_coffee"] - 0.2, T["t_wifi"] + 0.2, accent="#93C5FD", size=46)
        self.chip(540, 300, "nowifi", T["t_wifi"] + 0.2, self.duration + 1, accent=WARN, size=54)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0B1220", "#1E293B"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.5, T["congrats"]), 61), -18), (T["loose"], sfx.creak(1.0, 62), -12),
              (T["slide"], sfx.whoosh(0.6, True, 63), -12),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["shipped"], sfx.womp(), -14),
               (T["huge"], sfx.ring(0.9), -12), (T["price1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 67), -4), (T["concrete"], sfx.thud(0.5, 68), -8),
               (T["twice1"], sfx.ding(), -8), (T["twice1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 69), -4), (T["weight"], sfx.thud(0.6, 70), -6),
               (T["holes"], rumble(1.2, 71), -10), (T["holes1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["shift"], sfx.creak(1.0, 72), -10), (T["dig"], sfx.whirr(1.4, 120.0, 200.0, 73), -12),
               (T["deep1"], sfx.ding(), -8), (T["deep1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, False, 74), -4), (T["fire"], sfx.sizzle(1.0, 75), -10),
               (T["walk1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["bridge3"], sfx.whoosh(0.5, False, 76), -8), (T["joins"], sfx.clank(300.0, 0.5, 77), -10),
               (T["other1"], sfx.ding(), -8), (T["other1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["storm"], sfx.hiss(1.6, 78), -14), (T["snap"], sfx.snap(79), -4), (T["snap1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 80), -6), (T["bearings"], sfx.click(81), -8),
               (T["slides"], sfx.whoosh(0.4, False, 82), -12), (T["slides1"], sfx.ding(), -8), (T["slides1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(83), 0), (T["follow"] - 0.15, sfx.pop(84), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 85), -6), (T["race"], sfx.riser(1.0, 86), -14),
               (T["top"], sfx.chime(), -8), (T["first"], sfx.sparkle(1.0, 12, 87), -8)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 88), -6), (T["s1"], sfx.pop(89), -3), (T["s2"], sfx.pop(90), -3),
               (T["s3"], sfx.pop(91), -3)]
        ev += [(T["cong2"], sfx.pop(92), -2), (T["cong2"], sfx.sparkle(1.4, 18, 93), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("closer") + 0.3, boom(1.2, 94), -18), (s("closer") + 1.1, boom(1.2, 95), -20)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 96), -6), (T["t_connect"], sfx.beep(1200.0, 0.09), -12),
               (T["t_connect"] + 0.3, sfx.beep(1200.0, 0.09), -12), (T["t_wifi"] + 0.2, sfx.buzz(0.42), -8)]
        return ev


NAME = "petronas"
EPISODE = Petronas
