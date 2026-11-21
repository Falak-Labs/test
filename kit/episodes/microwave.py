"""Episode 60 - A microwave oven.  v2 look: a kitchen at night with warm light; the oven shown in x-ray with its waves
drawn as glowing yellow lines and the water molecules as little red-and-white Vs.

Sets: kitchen (hook: a mug of water boils inside the oven with no flame while a magnifier shows its water molecules
flipping back and forth, then out to the whole oven on the counter; stat: the first oven of 1947 next to today's; closer
at night, the plate turning in the warm light), fire (break1: a frozen block on a flame browns outside while its middle
stays icy; fix1: the magnetron beams waves into the food and twists its water molecules until it warms all through),
box (break2: a bare magnetron spraying waves over the kitchen and the cook; fix2: a metal box bounces them back, and the
door's mesh is a wall for 12 cm waves but a window for light), spots (break3: top view of a pizza on a grid of hot and
cold spots, burnt here and frozen there; fix3: the turntable carries every slice through the hot spots), door (break4:
the door opens while it runs and the waves come out; fix4: switches in the latch cut the power before the door opens a
crack), lab (reveal: 1945, radar engineer Percy Spencer next to a magnetron, the chocolate bar in his pocket melting),
tag (EN: stopping it at 0:01 so it won't beep; AR: mom says stand back or you'll get radiation).
World (kitchen): front view, the counter top at y = 0, the oven 560 x 340 units standing on it at x = 0.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of  # noqa: E402
from phone import bubble, mom  # noqa: E402

OW, OH = 560.0, 340.0                                      # oven size (world units)
CAV = (-262.0, -312.0, 300.0, 270.0)                       # cavity rect (x, y, w, h) inside the oven, front view
WAVE = "#FDE047"
WALL = "#2A3350"


def molecule(c, x, y, r, ang, a=1.0):
    """A water molecule: red oxygen, two white hydrogens 104 degrees apart; ang turns it."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    for sd in (-1, 1):
        q = math.radians(90 + sd * 52)
        c.drawLine(0, 0, math.cos(q) * r * 1.1, math.sin(q) * r * 1.1, P("#E5E7EB", a, stroke=r * 0.3))
        c.drawCircle(math.cos(q) * r * 1.15, math.sin(q) * r * 1.15, r * 0.55, P("#F8FAFC", a))
    c.drawCircle(0, 0, r * 0.8, P("#EF4444", a))
    c.drawCircle(-r * 0.25, -r * 0.25, r * 0.25, P("#FCA5A5", 0.8 * a))
    c.restore()


def bounce_path(x0, y0, ang, rect, length, step=6.0):
    """Points of a ray starting at (x0, y0) heading ang (degrees) that bounces inside rect (x, y, w, h)."""
    rx, ry, rw, rh = rect
    dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts, x, y, d = [(x0, y0)], x0, y0, 0.0
    while d < length:
        x, y = x + dx * step, y + dy * step
        if x < rx or x > rx + rw:
            dx = -dx
            x = clamp(x, rx, rx + rw)
        if y < ry or y > ry + rh:
            dy = -dy
            y = clamp(y, ry, ry + rh)
        pts.append((x, y))
        d += step
    return pts


def wave_line(c, pts, t, amp=10.0, wl=40.0, col=WAVE, a=1.0, w=3.5, speed=3.0):
    """A sine wave drawn along a polyline (screen or world space), moving along it."""
    if a <= 0 or len(pts) < 2:
        return
    p_ = skia.Path()
    s_ = 0.0
    for i, (x, y) in enumerate(pts):
        if i > 0:
            s_ += math.hypot(x - pts[i - 1][0], y - pts[i - 1][1])
        j = min(i + 1, len(pts) - 1)
        k = max(i - 1, 0)
        tx, ty = pts[j][0] - pts[k][0], pts[j][1] - pts[k][1]
        ln = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / ln, tx / ln
        o = math.sin((s_ / wl - t * speed) * 2 * math.pi) * amp
        if i == 0:
            p_.moveTo(x + nx * o, y + ny * o)
        else:
            p_.lineTo(x + nx * o, y + ny * o)
    c.drawPath(p_, P(col, 0.35 * a, stroke=w * 3))
    c.drawPath(p_, P(col, a, stroke=w))


def magnetron(c, x, y, s, t, on=1.0, a=1.0):
    """The magnetron: a copper block with cooling fins, ring magnets and an antenna on top (centre at x, y)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for k in range(7):                                          # cooling fins
        c.drawRect(R(-70, -54 + k * 18, 140, 8), P("#9CA3AF", a))
    c.drawRRect(rr(-44, -60, 88, 120, 10), P("#B87333", a))
    c.drawRect(R(-56, -74, 112, 18), P("#4B5563", a))           # ring magnets
    c.drawRect(R(-56, 56, 112, 18), P("#4B5563", a))
    c.drawRect(R(-10, -112, 20, 40), P("#D1D5DB", a))           # antenna
    c.drawCircle(0, -114, 13, P("#E5E7EB", a))
    if on > 0:
        add_glow(c, 0, -114, 50, WAVE, 0.6 * on * a)
        add_glow(c, 0, 0, 80, "#FB923C", 0.25 * on * a)
    c.restore()


def oven(c, t, xray=0.0, door=0.0, light=1.0, running=1.0, waves=0.0, plate_ang=0.0, food="mug", heat=0.0,
         display="1:30", lit_room=1.0, a=1.0, burnt=None):
    """The microwave oven standing on the counter at x = 0 (world space).  xray 0..1 shows the cavity, the magnetron and
    the waves; door 0..1 swings the door open; running 0..1 the hum light; heat 0..1 the food warming (steam)."""
    if a <= 0:
        return
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    x0, y0 = -OW / 2, -OH
    contact_shadow(c, 0, 0, OW * 0.9, 0.5, 20)
    c.drawRRect(rr(x0, y0, OW, OH, 26), lin_paint(0, y0, 0, 0, ["#E5E7EB", "#CBD5E1", "#94A3B8"]))
    cx_, cy_, cw, ch = CAV
    c.drawRRect(rr(cx_, cy_, cw, ch, 10), P("#1E2436"))         # the cavity
    if light > 0:
        c.drawRRect(rr(cx_, cy_, cw, ch, 10), rad_paint(cx_ + cw / 2, cy_ + 40, cw, [("#FFE6A8", 0.6 * light), ("#FFE6A8", 0.0)]))
    # the turntable and the food
    px, py = cx_ + cw / 2, cy_ + ch - 30
    c.drawOval(R(px - 120, py - 16, 240, 36), P("#CBD5E1", 0.8))
    c.drawOval(R(px - 120, py - 16, 240, 36), P("#94A3B8", 1.0, stroke=3))
    mk = (math.sin(math.radians(plate_ang)) + 1) / 2
    if food == "mug":
        mx = px + math.sin(math.radians(plate_ang)) * 30
        c.drawRRect(rr(mx - 48, py - 120, 96, 116, 14), P("#F8FAFC"))
        c.drawRRect(rr(mx - 40, py - 112, 80, 24, 8), P(mix("#60A5FA", "#F87171", heat)))
        c.drawPath(path_of([(mx + 48, py - 96), (mx + 72, py - 90), (mx + 72, py - 44), (mx + 48, py - 38)]), P("#E5E7EB", 1.0, stroke=10))
        if heat > 0.3:                                          # bubbles and steam
            for k in range(6):
                q = (t * 1.4 + k / 6.0) % 1.0
                c.drawCircle(mx - 30 + k * 12, py - 92 - q * 14, 4, P("#E0F2FE", (heat - 0.3) * (1 - q)))
            for k in range(3):
                v2.puff(c, mx - 20 + k * 20, py - 150 - ((t * 40 + k * 30) % 90), 18, "#F1F5F9", 0.35 * (heat - 0.3), k=k)
    elif food == "bowl":
        c.drawPath(path_of([(px - 70, py - 64), (px + 70, py - 64), (px + 50, py - 8), (px - 50, py - 8)], close=True), P("#F97316"))
        c.drawOval(R(px - 70, py - 74, 140, 20), P(mix("#FDBA74", "#EA580C", heat)))
        for k in range(3):
            v2.puff(c, px - 30 + k * 30, py - 110 - ((t * 40 + k * 30) % 90), 18, "#F1F5F9", 0.3 * heat, k=k)
    _ = mk
    if xray > 0:                                                # the magnetron behind the panel and its waveguide
        magnetron(c, 160, -170, 0.55, t, on=running, a=xray)
        c.drawRect(R(cx_ + cw, -250, 100, 36), P("#6B7280", xray))
        if waves > 0:
            for k, (sx, sy, ang) in enumerate(((cx_ + cw - 6, -232, 205), (cx_ + cw - 6, -228, 152))):
                pts = bounce_path(sx, sy, ang, (cx_ + 6, cy_ + 6, cw - 12, ch - 12), 900 + k * 200, step=8)
                wave_line(c, pts, t + k * 0.3, amp=7, wl=52, a=waves * xray * 0.75, w=2.6, speed=2.4)
    # the door: a frame with a mesh window over the cavity
    dk = clamp(door)
    c.save()
    if dk > 0:
        c.translate(x0, 0)
        c.scale(1 - 0.85 * dk, 1)
        c.translate(-x0, 0)
    dw = OW * 0.66
    door_a = 1.0 - 0.75 * xray
    c.drawRRect(rr(x0 + 8, y0 + 8, dw, OH - 16, 20), P("#1F2937", 0.35 * door_a, stroke=10))
    c.drawRRect(rr(x0 + 30, y0 + 30, dw - 44, OH - 60, 12), P("#0F172A", 0.55 * door_a * (1 - 0.6 * light)))
    for j in range(11):                                         # the mesh of tiny holes
        for i in range(17):
            c.drawCircle(x0 + 44 + i * 20, y0 + 44 + j * 24, 2.4, P("#0B1020", 0.45 * door_a))
    c.drawRRect(rr(x0 + dw - 30, y0 + 120, 14, 100, 7), P("#475569", door_a))   # handle
    c.restore()
    # the control panel and the display
    c.drawRRect(rr(x0 + dw + 24, y0 + 24, OW - dw - 48, 64, 10), P("#0B1020"))
    text(c, display, x0 + dw + (OW - dw) / 2, y0 + 72, 40, "#34D399" if running > 0.5 else "#64748B", "Poppins-Black",
         align="center")
    for j in range(3):
        for i in range(3):
            c.drawRRect(rr(x0 + dw + 40 + i * 46, y0 + 112 + j * 44, 36, 30, 8), P("#94A3B8"))
    c.drawRRect(rr(x0 + dw + 40, y0 + 250, 128, 40, 12), P("#22C55E" if running > 0.5 else "#64748B"))
    if a < 1:
        c.restore()


def kitchen(c, cam, t, night=1.0):
    """The kitchen behind the counter (screen space backdrop, then the counter in world space)."""
    vrect(c, 0, 0, W, H, [mix("#F3D9B1", "#2A2440", night), mix("#E8C48F", "#3A2E48", night)])
    cx, cy, z = cam
    for k in range(5):                                          # wall tiles
        yy = (-560 + k * 60 - cy) * z + H / 2
        c.drawLine(0, yy, W, yy, P("#FFFFFF", 0.06, stroke=2))
    for k in range(3):                                          # cabinets
        x_ = (-900 + k * 620 - cx) * z + W / 2
        c.drawRRect(rr(x_, (-1100 - cy) * z + H / 2, 560 * z, 380 * z, 18 * z), P(mix("#C08A5A", "#4A3A3A", night)))
        c.drawRRect(rr(x_ + 250 * z, (-860 - cy) * z + H / 2, 60 * z, 14 * z, 7 * z), P("#E5E7EB", 0.8))
    add_glow(c, (0 - cx) * z + W / 2, (-1000 - cy) * z + H / 2, 600 * z, "#FFD08A", 0.25)


def counter(c, t, night=1.0):
    c.drawRect(R(-1600, 0, 3200, 40), P(mix("#E5E0D8", "#6B6475", night)))
    c.drawRect(R(-1600, 40, 3200, 900), P(mix("#9A6A44", "#3A2A2E", night)))
    for k in range(8):
        c.drawLine(-1400 + k * 400, 60, -1400 + k * 400, 900, P("#000000", 0.15, stroke=3))


def first_oven(c, x, y, s, a=1.0):
    """The Radarange of 1947: a cabinet the size of a fridge (world, feet at y)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-110, -560, 220, 560, 14), P("#9CA3AF", a))
    c.drawRRect(rr(-90, -520, 180, 150, 10), P("#374151", a))
    c.drawRRect(rr(-90, -340, 180, 300, 10), P("#6B7280", a))
    for k in range(4):
        c.drawCircle(-50 + k * 34, -400, 10, P("#E5E7EB", a))
    c.restore()


def choc_bar(c, x, y, s, melt=0.0, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-30, -50, 60, 100, 6), P("#7C2D12", a))
    c.drawRect(R(-30, -50, 60, 40), P("#B91C1C", a))
    for k in range(int(4 * melt) + 1):
        if melt > 0:
            c.drawRRect(rr(-24 + k * 14, 40, 10, 20 + 50 * melt * ((k % 2) + 0.5), 5), P("#5A2A12", a * melt))
    c.restore()


# ====================================================================================== the episode
class Microwave(EpisodeV2):
    BUILD_NO = 60
    FIRST_SET = "kitchen"
    CLEAR = "#1E1A2E"
    TITLE = {"en": "MICROWAVE OVEN", "ar_sa": "ميكروويف"}
    EMPH = {"en": ["CONGRATS", "BOIL", "WATER", "FIRE", "SHAKING", "BILLIONS", "SECOND", "MICROWAVE", "OVEN", "YOURSELF",
                   "OUTSIDE", "MIDDLE", "WAITS", "RADAR", "TUBE", "MAGNETRON", "WAVES", "TWIST", "MOLECULES", "HEAT",
                   "SPILL", "KITCHEN", "TRAP", "METAL", "BOX", "MESH", "HOLES", "SMALL", "LIGHT", "BOUNCING", "HOT",
                   "SPOTS", "COLD", "PIZZA", "BURNS", "FROZEN", "TURNTABLE", "BITE", "TURN", "OPEN", "DOOR", "RUNS",
                   "HIT", "SWITCHES", "POWER", "CRACK", "FOLLOW", "LEANING", "TOWER", "PISA", "NINETEEN", "FORTY-FIVE",
                   "PERCY", "SPENCER", "CHOCOLATE", "POCKET", "MELTED", "HALF", "FLIPS", "TWELVE-CENTIMETER", "THREE",
                   "HUNDRED", "FORTY", "KILOS", "STOP", "ONE", "LEFT", "BEEP"],
            "ar_sa": ["مبروك", "تغلي", "المية", "نار", "تهزّها", "مليارات", "الثانية", "ميكروويف", "بإيدك", "برة", "لجوه",
                      "مستني", "الرادار", "الماجنترون", "موجاتها", "جزيئات", "تسخن", "المطبخ", "صندوق", "معدن", "شبكة",
                      "خرومها", "أصغر", "النور", "سخنة", "ساقعة", "البيتزا", "يتحرق", "تلج", "طبق", "بيلف", "لقمة",
                      "الباب", "شغال", "مفاتيح", "الكهربا", "شعرة", "تابعني", "برج", "بيزا", "المايل", "بيرسي", "سبنسر",
                      "الشوكولاتة", "جيبه", "سايحة", "مليارين", "ونص", "هزة", "اتناشر", "سانتي", "تلتمية", "وأربعين",
                      "كيلو", "أمك", "ابعد", "إشعاع"]}
    KEYS = {"ar_sa": {
        ("hook", "BOIL"): "تغلي", ("hook", "FIRE"): "نار", ("hook", "SHAKING"): "تهزّها", ("hook", "BILLIONS"): "مليارات",
        ("hook", "CONGRATS"): "مبروك", ("hook", "MICROWAVE"): "ميكروويف",
        ("break1", "FIRE"): "النار", ("break1", "OUTSIDE"): "برة", ("break1", "MIDDLE"): "والنص", ("break1", "WAITS"): "مستني",
        ("fix1", "RADAR"): "الرادار", ("fix1", "MAGNETRON"): "الماجنترون", ("fix1", "WAVES"): "موجاتها",
        ("fix1", "MOLECULES"): "جزيئات", ("fix1", "HEAT"): "تسخن",
        ("break2", "SPILL"): "هتطلع", ("break2", "KITCHEN"): "المطبخ", ("break2", "YOU"): "معاه",
        ("fix2", "TRAP"): "فتقفل", ("fix2", "METAL"): "معدن", ("fix2", "MESH"): "شبكة", ("fix2", "SMALL"): "أصغر",
        ("fix2", "LIGHT"): "النور",
        ("break3", "BOUNCING"): "بتخبط", ("break3", "HOT"): "سخنة", ("break3", "COLD"): "ساقعة",
        ("break3", "BURNS"): "يتحرق", ("break3", "FROZEN"): "تلج",
        ("fix3", "TURNTABLE"): "طبق", ("fix3", "HOT"): "السخنة", ("fix3", "BITE"): "لقمة",
        ("break4", "OPEN"): "فتحت", ("break4", "RUNS"): "شغال", ("break4", "HIT"): "عليك",
        ("fix4", "SWITCHES"): "مفاتيح", ("fix4", "POWER"): "الكهربا", ("fix4", "CRACK"): "شعرة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "STORY"): "الحكاية", ("reveal", "RADAR"): "رادار", ("reveal", "PERCY"): "بيرسي",
        ("reveal", "CHOCOLATE"): "الشوكولاتة", ("reveal", "MELTED"): "سايحة",
        ("stat", "TWO"): "مليارين", ("stat", "TWELVE-CENTIMETER"): "اتناشر", ("stat", "THREE"): "تلتمية",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SHAKES"): "أمك", ("tag", "STOP"): "ابعد", ("tag", "ONE"): "الميكروويف", ("tag", "BEEP"): "إشعاع"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Leaning Tower of Pisa"),
                   "stat": [("2.45 bn", "FLIPS A SECOND"), ("12 cm", "WAVES"), ("340 kg", "THE FIRST ONE")],
                   "L": {"nofire": "NO FIRE", "billions": "BILLIONS OF FLIPS A SECOND", "name": "A MICROWAVE OVEN",
                         "outside": "FIRE: OUTSIDE IN", "middle": "THE MIDDLE STAYS FROZEN", "magnetron": "THE MAGNETRON",
                         "twist": "WAVES TWIST WATER MOLECULES", "spill": "WAVES EVERYWHERE", "you": "COOKING YOU TOO",
                         "box": "A METAL BOX BOUNCES THEM", "mesh": "HOLES TOO SMALL FOR WAVES", "light": "LIGHT GETS THROUGH",
                         "spots": "HOT SPOTS + COLD SPOTS", "burns": "BURNT HERE, FROZEN THERE", "turntable": "THE TURNTABLE",
                         "bite": "EVERY BITE GETS ITS TURN", "open": "DOOR OPEN WHILE IT RUNS", "hit": "WAVES COME OUT!",
                         "switch": "DOOR SWITCHES", "cut": "POWER OFF BEFORE IT OPENS", "year": "1945",
                         "spencer": "PERCY SPENCER, RADAR ENGINEER", "melted": "HIS CHOCOLATE MELTED",
                         "nobeep": "NO BEEP TODAY"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: برج بيزا المايل"),
                      "stat": [("2.45", "مليار هزة في الثانية"), ("12", "سانتي طول الموجة"), ("340", "كيلو أول جهاز")],
                      "L": {"nofire": "من غير نار", "billions": "مليارات المرات في الثانية", "name": "ميكروويف",
                            "outside": "النار: من برة لجوه", "middle": "النص يفضل مستني", "magnetron": "الماجنترون",
                            "twist": "الموجات تلف جزيئات المية", "spill": "الموجات في كل حتة", "you": "وانت معاه",
                            "box": "صندوق معدن يرجّعها", "mesh": "خروم أصغر من الموجة", "light": "بس النور بيعدي",
                            "spots": "حتت سخنة وحتت ساقعة", "burns": "نص يتحرق ونص تلج", "turntable": "طبق بيلف",
                            "bite": "كل لقمة تاخد دورها", "open": "الباب اتفتح وهو شغال", "hit": "الموجات طالعة عليك!",
                            "switch": "مفاتيح في الباب", "cut": "الكهربا تفصل قبل ما يتفتح", "year": "1945",
                            "spencer": "بيرسي سبنسر، مهندس رادار", "melted": "الشوكولاتة ساحت في جيبه",
                            "nobeep": "هيجيلك إشعاع!", "bubble": "ابعد عن الميكروويف!"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "boil": ("hook", "BOIL", 0.1), "fire": ("hook", "FIRE", 0.25), "shaking": ("hook", "SHAKING", 0.35),
            "billions": ("hook", "BILLIONS", 0.45), "congrats": ("hook", "CONGRATS", 0.68), "micro": ("hook", "MICROWAVE", 0.9),
            "fire1": ("break1", "FIRE", 0.1), "outside": ("break1", "OUTSIDE", 0.5), "middle": ("break1", "MIDDLE", 0.75),
            "waits": ("break1", "WAITS", 0.92),
            "radar": ("fix1", "RADAR", 0.15), "magnetron": ("fix1", "MAGNETRON", 0.3), "waves": ("fix1", "WAVES", 0.45),
            "molecules": ("fix1", "MOLECULES", 0.65), "heat": ("fix1", "HEAT", 0.9),
            "spill": ("break2", "SPILL", 0.3), "kitch": ("break2", "KITCHEN", 0.7), "you": ("break2", "YOU", 0.92),
            "trap": ("fix2", "TRAP", 0.1), "metal": ("fix2", "METAL", 0.25), "mesh": ("fix2", "MESH", 0.55),
            "small": ("fix2", "SMALL", 0.7), "light": ("fix2", "LIGHT", 0.92),
            "bouncing": ("break3", "BOUNCING", 0.1), "hot": ("break3", "HOT", 0.3), "cold": ("break3", "COLD", 0.45),
            "burns": ("break3", "BURNS", 0.75), "frozen": ("break3", "FROZEN", 0.92),
            "turntable": ("fix3", "TURNTABLE", 0.1), "hot3": ("fix3", "HOT", 0.5), "bite": ("fix3", "BITE", 0.8),
            "open": ("break4", "OPEN", 0.1), "runs": ("break4", "RUNS", 0.5), "hit": ("break4", "HIT", 0.85),
            "switches": ("fix4", "SWITCHES", 0.1), "power": ("fix4", "POWER", 0.5), "crack": ("fix4", "CRACK", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "story": ("reveal", "STORY", 0.05), "radar2": ("reveal", "RADAR", 0.4), "percy": ("reveal", "PERCY", 0.5),
            "choc": ("reveal", "CHOCOLATE", 0.75), "melted": ("reveal", "MELTED", 0.95),
            "s1": ("stat", "TWO", 0.05), "s2": ("stat", "TWELVE-CENTIMETER", 0.35), "s3": ("stat", "THREE", 0.6),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_shake": ("tag", "SHAKES", 0.05), "t_stop": ("tag", "STOP", 0.5), "t_one": ("tag", "ONE", 0.7),
            "t_beep": ("tag", "BEEP", 0.92)})
        T["waits1"] = max(T["waits"], T["middle"]) + 0.1
        T["you1"] = max(T["you"], T["kitch"]) + 0.1
        T["frozen1"] = max(T["frozen"], T["burns"]) + 0.1
        T["hit1"] = max(T["hit"], T["runs"]) + 0.1
        T["heat1"] = max(T["heat"], T["molecules"]) + 0.2
        T["light1"] = max(T["light"], T["small"]) + 0.2
        T["bite1"] = max(T["bite"], T["hot3"]) + 0.2
        T["crack1"] = max(T["crack"], T["power"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "fire", 1)
        self.cut(s("break2") - 0.12, "box", -1)
        self.cut(s("break3") - 0.12, "spots", 1)
        self.cut(s("break4") - 0.12, "door", -1)
        self.cut(s("reveal") - 0.12, "lab", 1)
        self.cut(s("stat") - 0.12, "kitchen", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- kitchen camera: from the boiling mug out to the whole oven on the counter
        cm = Camera(-112, -150, 2.9)
        cm.key(0.05, -110, -152, 2.8, 0.3)
        cm.key(max(0.5, T["congrats"] - 0.6), 0, -230, 1.45, max(1.0, T["micro"] - T["congrats"] + 0.6))
        cm.key(s("stat") - 0.12, 220, -330, 1.0, 0.0).key(s("stat"), 220, -332, 1.01, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 0, -150, 1.5, 1.0).key(s("closer") + 0.9, 0, -145, 1.6, 3.0)
        self.cam = cm
        self.spans = [(T["waits1"], T["heat1"] + 0.3), (T["you1"], T["light1"] + 0.3), (T["frozen1"], T["bite1"] + 0.3),
                      (T["hit1"], T["crack1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["waits1"], 0.3, 6), (T["you1"], 0.4, 7), (T["frozen1"], 0.3, 6),
                       (T["hit1"], 0.4, 8), (s("closer") + 0.2, 0.35, 9), (T["t_beep"], 0.25, 6)]

    # ------------------------------------------------------------------ set: kitchen (hook, stat, closer)
    def draw_kitchen(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        night = 1.0
        kitchen(c, cam, t, night)
        self.view(c, cam)
        counter(c, t, night)
        if hook:
            xr = 1.0 - prog(t, T["congrats"] - 0.2, T["congrats"] + 0.6) * 0.65
            heat = prog(t, T["boil"], T["congrats"] + 0.3)
            oven(c, t, xray=xr, waves=1.0, plate_ang=t * 60, food="mug", heat=heat,
                 display="1:%02d" % max(0, int(30 - t * 4)))
        else:
            st = s("stat") - 0.12 <= t < s("closer") - 0.1
            if st:
                first_oven(c, 420, 0, 0.9, a=prog(t, T["s3"] - 0.4, T["s3"]))
                person(c, 640, 0, 300, "#2563EB", t, pose="look", face=-1, a=prog(t, T["s3"] - 0.4, T["s3"]))
            oven(c, t, xray=0.0, waves=0.0, plate_ang=t * 60, food="bowl", heat=0.8, display="0:%02d" % max(1, int(40 - (t % 30))))
        c.restore()
        if hook:                                                   # the magnifier: water molecules flipping
            mk = prog(t, T["boil"] - 0.3, T["boil"]) * (1 - prog(t, T["congrats"] - 0.1, T["congrats"] + 0.3))
            if mk > 0:
                mx, my, mr = 300, 560, 190
                c.drawCircle(mx, my, mr, P("#0B1426", 0.9 * mk))
                c.save()
                cp = skia.Path()
                cp.addCircle(mx, my, mr)
                c.clipPath(cp, doAntiAlias=True)
                rng = random.Random(4)
                for k in range(14):
                    px_, py_ = mx + rng.uniform(-150, 150), my + rng.uniform(-150, 150)
                    ang = rng.uniform(0, 360) + math.sin(t * 40 + k) * 70
                    molecule(c, px_, py_, 20, ang, a=mk)
                wave_line(c, [(mx - mr, my + 100), (mx + mr, my - 100)], t, amp=24, wl=110, a=0.8 * mk, w=4)
                c.restore()
                c.drawCircle(mx, my, mr, P("#E5E7EB", mk, stroke=10))
                c.drawLine(mx + mr * 0.7, my + mr * 0.7, mx + mr * 1.15, my + mr * 1.15, P("#E5E7EB", mk, stroke=22))
        self.ui["cam"] = cam

    def ui_kitchen(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "nofire", T["fire"] - 0.15, T["shaking"] - 0.1, accent="#FB923C", size=48)
            self.chip(540, 300, "billions", T["shaking"] - 0.1, T["micro"] - 0.25, accent=WAVE, size=40)
            self.chip(540, 300, "name", T["micro"] - 0.25, s("break1") + 0.1, accent=HILITE, size=48)

    # ------------------------------------------------------------------ set: fire (break1, fix1)
    def draw_fire(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        vrect(c, 0, 0, W, H, ["#1A1530", "#2A2040", "#3A2A40"])
        bx, by, bw, bh = 340, 640, 400, 300                        # the block of food, cut open
        if not fixed:
            v2.flame(c, 540, 1190, 300, 230, t, power=prog(t, T["fire1"] - 0.3, T["fire1"]), ang=-90.0)
            c.drawRRect(rr(300, 960, 480, 40, 14), P("#374151"))      # the pan
            ok = prog(t, T["outside"] - 0.4, T["waits1"] + 0.6)
            c.drawRRect(rr(bx, by, bw, bh, 30), P(mix("#93C5FD", "#B45309", ok)))
            c.drawRRect(rr(bx + 40 + 30 * ok, by + 40 + 20 * ok, bw - 80 - 60 * ok, bh - 80 - 40 * ok, 24),
                        P("#60A5FA"))                              # the frozen middle
            for k in range(8):
                rng = random.Random(k)
                c.drawLine(bx + 80 + rng.uniform(0, 240), by + 80 + rng.uniform(0, 140), bx + 90 + rng.uniform(0, 240),
                           by + 90 + rng.uniform(0, 140), P("#E0F2FE", 0.8, stroke=3))
            if ok > 0.3:
                for k in range(4):
                    v2.puff(c, bx + 40 + k * 100, by - 30 - ((t * 50 + k * 20) % 80), 24, "#6B7280", 0.4 * ok, k=k)
            return
        mk = prog(t, T["magnetron"] - 0.3, T["magnetron"])
        magnetron(c, 860, 790, 1.2, t, on=mk, a=max(0.4, prog(t, s("fix1") - 0.1, T["radar"])))
        wk = prog(t, T["waves"] - 0.3, T["waves"])
        for k in range(4):
            wave_line(c, [(780, 700 + k * 50), (300, 680 + k * 60)], t + k * 0.2, amp=16, wl=60, a=wk, w=4)
        hk = prog(t, T["molecules"], T["heat1"] + 0.5)
        c.drawRRect(rr(bx, by, bw, bh, 30), P(mix("#93C5FD", "#FB923C", hk)))
        rng = random.Random(9)
        mo = prog(t, T["molecules"] - 0.3, T["molecules"])
        for k in range(12):
            px_, py_ = bx + 50 + rng.uniform(0, bw - 100), by + 50 + rng.uniform(0, bh - 100)
            molecule(c, px_, py_, 18, rng.uniform(0, 360) + math.sin(t * 38 + k) * 80 * wk, a=mo)
        if hk > 0.4:
            for k in range(4):
                v2.puff(c, bx + 40 + k * 100, by - 30 - ((t * 50 + k * 20) % 80), 24, "#F1F5F9", 0.4 * hk, k=k)

    def ui_fire(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "outside", T["fire1"] - 0.2, T["middle"] - 0.15, accent="#FB923C", size=46)
            self.chip(540, 300, "middle", T["middle"] - 0.15, s("fix1") - 0.15, accent="#93C5FD", size=42)
            self.badge("alert", T["waits1"], s("fix1") - 0.2, x=920, y=420)
            self.red(T["waits1"], 1.2)
            return
        self.chip(540, 300, "magnetron", T["radar"] - 0.2, T["waves"] - 0.1, accent="#FDBA74", size=48)
        self.chip(540, 300, "twist", T["waves"] - 0.1, s("break2") - 0.15, accent=WAVE, size=38)
        self.badge("check", T["heat1"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: box (break2, fix2)
    def draw_box(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        cam = (0, -230, 1.45)
        kitchen(c, cam, t, 1.0)
        if not fixed:
            self.view(c, cam)
            counter(c, t)
            sk = prog(t, T["spill"] - 0.3, T["spill"])
            magnetron(c, 0, -110, 0.9, t, on=sk)
            for k in range(10):                                    # waves out in every direction
                ang = math.radians(k * 36 + t * 10)
                pts = [(math.cos(ang) * 60, -110 + math.sin(ang) * 60), (math.cos(ang) * 700, -110 + math.sin(ang) * 700)]
                wave_line(c, pts, t + k * 0.1, amp=14, wl=60, a=sk, w=4)
            yk = prog(t, T["you"] - 0.4, T["you1"] + 0.3)
            person(c, 300, 0, 260, "#2563EB", t, pose="duck" if yk > 0.5 else "look", face=-1)
            if yk > 0:
                add_glow(c, 300, -150, 200, "#EF4444", 0.45 * yk)
            c.restore()
            return
        bk = prog(t, T["trap"] - 0.3, T["metal"])
        mk = prog(t, T["mesh"] - 0.4, T["mesh"])
        if mk < 1:
            self.view(c, cam)
            counter(c, t)
            oven(c, t, xray=1.0, waves=bk, plate_ang=t * 60, food="mug", heat=0.3, a=1.0)
            c.restore()
        if mk > 0:                                                 # zoom on the door mesh
            c.drawRect(R(0, 380, W, 840), P("#0B1020", mk))
            for j in range(9):
                for i in range(11):
                    c.drawCircle(70 + i * 94, 440 + j * 92, 22, P("#334155", mk))
                    c.drawCircle(70 + i * 94, 440 + j * 92, 22, P("#64748B", mk, stroke=3))
            wk = prog(t, T["small"] - 0.3, T["small"])
            wave_line(c, [(60, 820), (480, 820)], t, amp=150, wl=520, a=wk * mk, w=10, speed=1.2)   # a 12 cm wave, blocked
            if wk > 0:
                c.drawLine(500, 640, 500, 1000, P(WARN, wk * mk, stroke=10))
            lk = prog(t, T["light"] - 0.3, T["light"])
            for k in range(3):                                     # light, tiny waves, through the holes
                y_ = 534 + k * 92
                wave_line(c, [(540, y_), (1080, y_)], t + k * 0.2, amp=4, wl=14, col="#FFF7D6", a=lk * mk, w=3, speed=6)

    def ui_box(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "spill", T["spill"] - 0.2, T["kitch"] + 0.2, accent=WAVE, size=46)
            self.chip(540, 300, "you", T["kitch"] + 0.2, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["you1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["you1"], 1.2)
            return
        self.chip(540, 300, "box", T["trap"] - 0.2, T["mesh"] - 0.2, accent="#CBD5E1", size=40)
        self.chip(540, 300, "mesh", T["mesh"] - 0.2, T["light"] - 0.2, accent=WAVE, size=40)
        self.chip(540, 300, "light", T["light"] - 0.2, s("break3") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["light1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: spots (break3, fix3), top view of the floor
    def draw_spots(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        vrect(c, 0, 0, W, H, ["#1E2436", "#141A2A"])
        cx_, cy_ = 540, 860
        gk = prog(t, T["hot"] - 0.4, T["cold"] + 0.2) if not fixed else 0.35
        for j in range(-3, 4):                                     # the grid of hot and cold spots
            for i in range(-3, 4):
                hot = (i + j) % 2 == 0
                c.drawCircle(cx_ + i * 130, cy_ + j * 130, 70, P("#EF4444" if hot else "#3B82F6", 0.35 * gk))
        ang = 0.0 if not fixed else (t - (s("fix3") - 0.12)) * 70
        c.save()
        c.translate(cx_, cy_)
        c.rotate(ang)
        if fixed:
            tk = prog(t, T["turntable"] - 0.3, T["turntable"])
            c.drawCircle(0, 0, 400, P("#CBD5E1", 0.35 * tk))
            c.drawCircle(0, 0, 400, P("#E5E7EB", tk, stroke=6))
        c.drawCircle(0, 0, 330, P("#F59E0B"))                       # the pizza
        c.drawCircle(0, 0, 300, P("#EF4444"))
        c.drawCircle(0, 0, 300, P("#FDE68A", 0.45))
        rng = random.Random(2)
        for k in range(14):                                        # pepperoni
            q, r_ = rng.uniform(0, 2 * math.pi), rng.uniform(40, 250)
            c.drawCircle(math.cos(q) * r_, math.sin(q) * r_, 26, P("#B91C1C"))
        c.restore()
        if not fixed:                                              # burnt on the hot spots, frost on the cold ones
            bk = prog(t, T["burns"] - 0.3, T["frozen1"] + 0.4)
            for j in range(-2, 3):
                for i in range(-2, 3):
                    if (i * i + j * j) * 130 * 130 > 300 * 300:
                        continue
                    px_, py_ = cx_ + i * 130, cy_ + j * 130
                    if (i + j) % 2 == 0:
                        c.drawCircle(px_, py_, 54, P("#1C1410", 0.85 * bk))
                    else:
                        c.drawCircle(px_, py_, 54, P("#E0F2FE", 0.8 * bk))
                        for k in range(6):
                            q = math.radians(k * 60)
                            c.drawLine(px_, py_, px_ + math.cos(q) * 40, py_ + math.sin(q) * 40, P("#93C5FD", bk, stroke=4))
        else:
            ek = prog(t, T["hot3"], T["bite1"] + 0.5)
            c.drawCircle(cx_, cy_, 300, P("#F59E0B", 0.25 * ek))
            for k in range(3):
                v2.puff(c, cx_ - 120 + k * 120, cy_ - 360 - ((t * 50 + k * 30) % 90), 26, "#F1F5F9", 0.35 * ek, k=k)
            sk = prog(t, T["turntable"] - 0.3, T["turntable"])
            for k in range(2):
                a0 = t * 70 + k * 180
                q = math.radians(a0)
                arrow(c, cx_ + math.cos(q) * 420, cy_ + math.sin(q) * 420, cx_ + math.cos(q + 0.4) * 420,
                      cy_ + math.sin(q + 0.4) * 420, GOOD, a=sk, w=10, head=26)

    def ui_spots(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "spots", T["bouncing"] - 0.2, T["burns"] - 0.2, accent="#FCA5A5", size=42)
            self.chip(540, 300, "burns", T["burns"] - 0.2, s("fix3") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["frozen1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["frozen1"], 1.2)
            return
        self.chip(540, 300, "turntable", T["turntable"] - 0.2, T["bite"] - 0.3, accent="#CBD5E1", size=48)
        self.chip(540, 300, "bite", T["bite"] - 0.3, s("break4") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["bite1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: door (break4, fix4)
    def draw_door(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        cam = (0, -230, 1.45)
        kitchen(c, cam, t, 1.0)
        if not fixed:
            self.view(c, cam)
            counter(c, t)
            dk = e_io(prog(t, T["open"] - 0.2, T["runs"] + 0.3))
            oven(c, t, xray=0.6, door=dk * 0.8, waves=1.0, plate_ang=t * 60, food="mug", heat=0.4)
            hk = prog(t, T["hit"] - 0.4, T["hit1"] + 0.2)
            for k in range(5):
                wave_line(c, [(-120, -230 + k * 40), (-640, -260 + k * 60)], t + k * 0.15, amp=14, wl=60, a=hk, w=4)
            c.restore()
            if hk > 0:
                c.drawRect(R(0, 0, W, H), rad_paint(120, 900, 600, [("#EF4444", 0.4 * hk), ("#EF4444", 0.0)]))
            return
        # close-up of the latch: two hooks pressing two switches; the power is cut before the door moves
        vrect(c, 0, 0, W, H, ["#2A3350", "#1A2038"])
        pk = prog(t, T["power"] - 0.3, T["power"] + 0.2)
        ok = prog(t, T["crack"] - 0.2, T["crack1"] + 0.4)
        c.drawRRect(rr(560, 400, 420, 760, 30), P("#94A3B8"))      # the oven's side with the switches
        c.drawRRect(rr(100 - 60 * ok, 400, 300, 760, 30), P("#475569"))   # the door edge with its hooks
        for k, yy in enumerate((560, 820)):
            hx = 400 + 120 * (1 - pk) - 60 * ok
            c.drawRRect(rr(330 - 60 * ok, yy - 20, hx - 330 + 60 * ok, 40, 12), P("#CBD5E1"))
            c.drawRRect(rr(660, yy - 50, 120, 100, 14), P("#1F2937"))      # the switch
            c.drawRRect(rr(640, yy - 14, 30 + 20 * (1 - pk), 28, 6), P("#F59E0B"))   # its plunger
        on = 1.0 - pk
        c.drawCircle(770, 1040, 70, P("#0F172A"))                  # the power lamp
        c.drawCircle(770, 1040, 56, P("#22C55E" if on > 0.5 else "#EF4444"))
        if on > 0.5:
            add_glow(c, 770, 1040, 110, "#22C55E", 0.4)
        text(c, "ON" if on > 0.5 else "OFF", 770, 1056, 40, "#FFFFFF", "Poppins-Black", align="center")

    def ui_door(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "open", T["open"] - 0.2, T["hit"] - 0.2, accent="#FDBA74", size=42)
            self.chip(540, 300, "hit", T["hit"] - 0.2, s("fix4") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["hit1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["hit1"], 1.2)
            return
        self.chip(540, 300, "switch", T["switches"] - 0.2, T["power"] - 0.2, accent="#FCD34D", size=46)
        self.chip(540, 300, "cut", T["power"] - 0.2, s("cta") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["crack1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: lab (reveal), 1945
    def draw_lab(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#3A3428", "#2A2418", "#1A160E"])
        c.drawRect(R(0, 1230, W, H - 1230), P("#4A4030"))
        c.drawRRect(rr(560, 520, 420, 710, 20), P("#6B6B5A"))        # the radar cabinet
        for k in range(5):
            c.drawCircle(640 + k * 70, 600, 18, P("#D1D5DB"))
        magnetron(c, 770, 860, 1.3, t, on=0.8)
        rk = prog(t, T["radar2"] - 0.3, T["radar2"])
        for k in range(3):
            wave_line(c, [(680, 760 + k * 30), (360, 760 + k * 40)], t + k * 0.2, amp=12, wl=50, a=0.6 * rk, w=3)
        person(c, 280, 1230, 560, "#F8FAFC", t, pose="look", face=1, hair="#6B7280")
        mk = prog(t, T["choc"] - 0.2, T["melted"] + 0.6)
        choc_bar(c, 300, 870, 0.9, melt=mk)                         # in his shirt pocket
        if mk > 0.3:
            add_glow(c, 300, 880, 90, "#FB923C", 0.3 * mk)
        c.drawRect(R(0, 0, W, H), P("#704214", 0.10))

    def ui_lab(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "year", T["story"] - 0.2, T["percy"] - 0.2, accent="#FDE68A", size=56)
        self.chip(540, 300, "spencer", T["percy"] - 0.2, T["choc"] - 0.1, accent="#FDBA74", size=38)
        self.chip(540, 300, "melted", T["choc"] - 0.1, s("stat") - 0.15, accent=WARN, size=42)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        cam = (100, -180, 1.9)
        kitchen(c, cam, t, 1.0)
        self.view(c, cam)
        counter(c, t)
        if not self.rtl:
            sk = prog(t, T["t_stop"] - 0.3, T["t_stop"])
            sec = max(1, int(lerp(9, 1, prog(t, T["t_shake"], T["t_one"]))))
            oven(c, t, xray=0.0, plate_ang=t * 60, food="bowl", heat=0.6, display="0:%02d" % sec,
                 running=1.0 - prog(t, T["t_one"], T["t_one"] + 0.2))
        else:
            oven(c, t, xray=0.0, plate_ang=t * 60, food="bowl", heat=0.6, display="1:30")
        c.restore()
        if not self.rtl:                                           # the finger on STOP at one second left
            fk = prog(t, T["t_stop"] - 0.4, T["t_one"])
            if fk > 0:
                hx, hy = lerp(1100, 870, e_out(fk)), lerp(1300, 1010, e_out(fk))
                c.drawRRect(rr(hx, hy, 200, 90, 40), P("#E8B48A"))
                c.drawRRect(rr(hx - 70, hy + 10, 110, 40, 20), P("#E8B48A"))
        else:
            ak = prog(t, T["t_stop"] - 0.4, T["t_stop"])
            mom(c, lerp(1200, 860, e_out(ak)), 1500, 520, t, a=1.0)

    def ui_tag(self, c, t, tw):
        T = self.T
        if not self.rtl:
            self.chip(540, 300, "nobeep", T["t_one"] - 0.1, self.duration + 1, accent=HILITE, size=48)
        else:
            bubble(c, 600, 560, self.L["bubble"], self.span(T["t_stop"], self.duration + 1), tail_left=False, size=50)
            self.chip(540, 300, "nobeep", T["t_beep"] - 0.2, self.duration + 1, accent=WARN, size=48)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#2A2440", "#3A2E48"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hum(max(1.5, T["congrats"] + 0.3), 98.0), -18), (T["fire"], sfx.buzz(0.3), -16),
              (T["shaking"], sfx.whirr(1.2, 300.0, 600.0, 61), -16), (T["billions"], sfx.sizzle(0.7, 62), -14),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 63), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 64), -8),
              (T["micro"], sfx.beep(1700.0, 0.12), -10), (T["micro"] + 0.2, sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 65), -4), (T["fire1"], sfx.hiss(1.0, 66), -12),
               (T["outside"], sfx.sizzle(0.8, 67), -12), (T["waits1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["magnetron"], sfx.hum(1.2, 120.0), -14),
               (T["molecules"], sfx.whirr(0.9, 500.0, 900.0, 69), -16), (T["heat1"], sfx.ding(), -8),
               (T["heat1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 70), -4), (T["spill"], sfx.charge_up(0.6), -12),
               (T["you1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 71), -4), (T["metal"], sfx.clank(900.0, 0.4, 72), -10),
               (T["light"], sfx.sparkle(0.6, 8, 73), -10), (T["light1"], sfx.ding(), -8), (T["light1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["burns"], sfx.sizzle(0.7, 75), -12),
               (T["frozen1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 76), -4), (T["turntable"], sfx.whirr(1.4, 90.0, 110.0, 77), -14),
               (T["bite1"], sfx.ding(), -8), (T["bite1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 78), -4), (T["open"], sfx.creak(0.6, 79), -12),
               (T["hit1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 80), -4), (T["switches"], sfx.click(81), -6),
               (T["power"], sfx.power_down(0.8, 82), -10), (T["crack1"], sfx.ding(), -8), (T["crack1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(83), 0), (T["follow"] - 0.15, sfx.pop(84), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 85), -6), (T["radar2"], sfx.hum(1.0, 140.0), -16),
               (T["melted"], sfx.womp(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 86), -6), (T["s1"], sfx.pop(87), -3), (T["s2"], sfx.pop(88), -3),
               (T["s3"], sfx.pop(89), -3)]
        ev += [(T["cong2"], sfx.pop(90), -2), (T["cong2"], sfx.sparkle(1.4, 18, 91), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 92), -6)]
        if self.rtl:
            ev += [(T["t_stop"], sfx.pop(93), -8)]
        else:
            ev += [(T["t_one"], sfx.click(94), -6)]
        return ev


NAME = "microwave"
EPISODE = Microwave
