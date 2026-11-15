"""Episode 29 - A humanoid robot.  v2 look: a robot lab at dusk, a simulation wall, a hand and an egg, a marathon road.

Sets: lab (front view of the robot on a mat: the backflip hook; it tips over, then an inner ear keeps it up; it lifts
a leg and falls, then it shifts its weight over the other foot first and steps; a push knocks it down; after the
practice it takes the push and stays up; the cta with the robot on the floor; the tag: a fitted sheet in English,
in Arabic the mother sends it for bread and the battery dies), sim (thousands of copies falling and getting up on a
wall of screens), hand (break4, fix4: the hand crushes the egg, then touch sensors in the fingertips hold it),
road (the reveal: cameras for eyes, a battery, then the half marathon under red lanterns; the stat and the cheer).
The robot is drawn in its own frame: feet on y = 0, standing height 470.
"""
from v2_base import *  # noqa: F401,F403

SHELL = ("#FFFFFF", "#E2E8F0", "#9AA6B8")
JOINT = "#1F2937"
CYAN = "#22D3EE"
LAMP = "#E11D48"
PELV = -244.0                                  # pelvis height when standing
SHO = (78.0, -143.0)                           # shoulder offset from the pelvis (torso frame)
THIGH, SHIN, UPPER, FORE = 108.0, 108.0, 92.0, 88.0


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def ik2(hx, hy, fx, fy, l1, l2, bend):
    """Two-bone IK from (hx, hy) toward (fx, fy): returns the middle joint and the reachable end."""
    dx, dy = fx - hx, fy - hy
    d = clamp(math.hypot(dx, dy), abs(l1 - l2) + 1e-3, l1 + l2 - 1e-3)
    ang = math.atan2(dy, dx)
    a1 = math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1.0, 1.0))
    q = ang + bend * a1
    return hx + math.cos(q) * l1, hy + math.sin(q) * l1, hx + math.cos(ang) * d, hy + math.sin(ang) * d


def pose(**kw):
    """A pose of the robot (front view).  px, py: pelvis; lean: torso turn (deg); fl, fr: feet; hl, hr: hands in
    the torso frame (relative to the pelvis); head: head tilt (deg)."""
    p = {"px": 0.0, "py": PELV, "lean": 0.0, "fl": (-44.0, 0.0), "fr": (44.0, 0.0), "hl": (-96.0, 30.0),
         "hr": (96.0, 30.0), "head": 0.0}
    p.update(kw)
    return p


def mixp(a, b, k):
    out = {}
    for key in a:
        va, vb = a[key], b[key]
        out[key] = (lerp(va[0], vb[0], k), lerp(va[1], vb[1], k)) if isinstance(va, tuple) else lerp(va, vb, k)
    return out


def limb(c, x0, y0, x1, y1, w, a=1.0):
    c.drawLine(x0, y0, x1, y1, P("#64748B", a, stroke=w + 6))
    c.drawLine(x0, y0, x1, y1, P("#E5E9F0", a, stroke=w))
    c.drawLine(x0 - w * 0.18, y0, x1 - w * 0.18, y1, P("#FFFFFF", 0.55 * a, stroke=w * 0.3))


def joint(c, x, y, r, a=1.0, glow=0.0):
    c.drawCircle(x, y, r, P(JOINT, a))
    c.drawCircle(x, y, r * 0.45, P("#475569", a))
    if glow > 0:
        add_glow(c, x, y, r * 3.2, CYAN, 0.9 * glow * a)
        c.drawCircle(x, y, r * 0.5, P(CYAN, glow * a))


def robot(c, p, t=0.0, a=1.0, eyes=1.0, glow=None, gyro=0.0, bat=None, bib=None, cam=0.0, err=0.0, brain=0.0,
          shade_k=0.0):
    """The robot in its own frame (feet on y = 0).  glow: dict joint name -> 0..1 (hip, knee, ankle, shoulder)."""
    g = glow or {}
    px, py = p["px"], p["py"]
    for side, foot in ((-1, p["fl"]), (1, p["fr"])):                              # legs
        hx, hy = px + side * 34, py + 10
        fx, fy = foot
        kx, ky, ax, ay = ik2(hx, hy, fx, fy - 24, THIGH, SHIN, 1 if side < 0 else -1)
        limb(c, hx, hy, kx, ky, 40, a)
        limb(c, kx, ky, ax, ay, 34, a)
        joint(c, kx, ky, 17, a, g.get("knee", 0.0))
        joint(c, ax, ay, 12, a, g.get("ankle", 0.0))
        c.drawRRect(rr(ax - 34, ay + 6, 68, 22, 9), P(JOINT, a))                  # foot
        c.drawRRect(rr(ax - 32, ay + 4, 64, 12, 6), P("#475569", a))
        joint(c, hx, hy, 16, a, g.get("hip", 0.0))
    c.drawRRect(rr(px - 52, py - 18, 104, 42, 16), lin_paint(0, py - 18, 0, py + 24, list(SHELL), a=a))   # pelvis
    c.save()
    c.translate(px, py)
    c.rotate(p["lean"])
    c.drawRRect(rr(-22, -40, 44, 30, 8), P(JOINT, a))                                # waist
    tor = skia.Path()                                                                # chest
    tor.moveTo(-50, -34)
    tor.lineTo(-84, -138)
    tor.quadTo(-84, -160, -60, -162)
    tor.lineTo(60, -162)
    tor.quadTo(84, -160, 84, -138)
    tor.lineTo(50, -34)
    tor.close()
    c.drawPath(tor, lin_paint(-84, 0, 84, 0, ["#B8C2D0", "#FFFFFF", "#E2E8F0", "#A5B1C2"], a=a))
    c.drawPath(tor, P("#64748B", 0.6 * a, stroke=3))
    c.drawRRect(rr(-34, -128, 68, 46, 10), P("#0F172A", a))                          # chest display
    if bat is not None:                                                              # battery icon
        lvl = clamp(bat)
        col = mix(WARN, GOOD, clamp(lvl * 2 - 0.2))
        c.drawRRect(rr(-24, -118, 44, 26, 5), P("#E2E8F0", a, stroke=3))
        c.drawRect(R(20, -110, 5, 10), P("#E2E8F0", a))
        c.drawRect(R(-20, -114, 36 * lvl, 18), P(col, a))
    elif bib is not None:
        c.drawRRect(rr(-46, -132, 92, 62, 6), P("#FFFFFF", a))
        c.drawRRect(rr(-46, -132, 92, 14, 4), P(LAMP, a))
        text(c, bib, 0, -78, 40, "#0F172A", "Poppins-Black", a=a)
    else:
        c.drawCircle(0, -105, 9, P(CYAN, (0.5 + 0.5 * math.sin(t * 4)) * a * eyes))
    if gyro > 0:                                                                     # the inner ear
        add_glow(c, 0, -105, 70, CYAN, 0.6 * gyro * a)
        c.save()
        c.translate(0, -105)
        c.drawCircle(0, 0, 20, P(CYAN, gyro * a, stroke=4))
        c.rotate(t * 220)
        c.drawOval(R(-20, -8, 40, 16), P("#A5F3FC", gyro * a, stroke=3))
        c.rotate(90)
        c.drawOval(R(-20, -8, 40, 16), P("#A5F3FC", gyro * a, stroke=3))
        c.restore()
    for side, hand in ((-1, p["hl"]), (1, p["hr"])):                               # arms
        sx, sy = side * SHO[0], SHO[1]
        ex, ey, wx, wy = ik2(sx, sy, hand[0], hand[1], UPPER, FORE, 1 if side < 0 else -1)
        limb(c, sx, sy, ex, ey, 30, a)
        limb(c, ex, ey, wx, wy, 26, a)
        joint(c, ex, ey, 13, a, g.get("elbow", 0.0))
        c.drawCircle(wx, wy, 17, P(JOINT, a))
        c.drawCircle(wx, wy, 11, P("#475569", a))
        c.drawCircle(sx, sy, 24, lin_paint(sx - 24, 0, sx + 24, 0, list(SHELL), a=a))
        joint(c, sx, sy, 13, a, g.get("shoulder", 0.0))
    c.save()                                                                         # the head
    c.translate(0, -170)
    c.rotate(p["head"])
    c.drawRRect(rr(-14, -18, 28, 20, 6), P(JOINT, a))
    c.drawRRect(rr(-46, -96, 92, 82, 34), lin_paint(-46, 0, 46, 0, ["#C3CCD8", "#FFFFFF", "#E5E9F0", "#B0BCCB"], a=a))
    c.drawRRect(rr(-38, -76, 76, 38, 17), lin_paint(0, -76, 0, -38, ["#1E293B", "#0B1120"], a=a))
    if err > 0:
        word(c, "ERROR", 0, -48, 20, WARN, err * a)
    elif eyes > 0:
        ek = 0.8 + 0.2 * math.sin(t * 3)
        for ex_ in (-17, 17):
            c.drawRRect(rr(ex_ - 11, -62, 22, 10, 5), P(CYAN, eyes * ek * a))
            add_glow(c, ex_, -57, 30, CYAN, 0.5 * eyes * a)
            if cam > 0:
                c.drawCircle(ex_, -57, 13 * cam, P("#E0F2FE", cam * a, stroke=3))
    if brain > 0:
        add_glow(c, 0, -60, 120, "#F0ABFC", 0.8 * brain * a)
    c.restore()
    c.restore()
    if shade_k > 0:
        c.drawRect(R(px - 160, -520, 320, 560), P("#000000", shade_k))


def robot_at(c, x, y, s, p, pivot=None, ang=0.0, **kw):
    """robot() placed at (x, y) with scale s; ang turns it around pivot (robot frame) or around its pelvis."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if ang:
        ox, oy = pivot if pivot is not None else (p["px"], p["py"])
        c.translate(ox, oy)
        c.rotate(ang)
        c.translate(-ox, -oy)
    robot(c, p, **kw)
    c.restore()


def run_pose(ph, amp=1.0):
    """Jogging toward the camera: feet lift in turn, arms pump, the body bobs."""
    up = math.sin(ph)
    lift_l, lift_r = max(0.0, up) * 90 * amp, max(0.0, -up) * 90 * amp
    bob = abs(math.cos(ph)) * 14 * amp
    return pose(py=PELV - bob, fl=(-46 + lift_l * 0.1, -lift_l), fr=(46 - lift_r * 0.1, -lift_r),
                hl=(-92, -10 - 40 * up * amp), hr=(92, -10 + 40 * up * amp), lean=0.0)


def egg(c, x, y, s=1.0, a=1.0):
    c.drawOval(R(x - 75 * s, y - 96 * s, 150 * s, 192 * s), rad_paint(x - 25 * s, y - 40 * s, 170 * s, ["#FFFBF0", "#F5E6CC", "#D9C29A"], a=a))
    c.drawOval(R(x - 50 * s, y - 70 * s, 34 * s, 50 * s), P("#FFFFFF", 0.45 * a))


def splat(c, x, y, k, a=1.0):
    """A crushed egg: white spreading, the yolk, bits of shell."""
    if k <= 0:
        return
    rng = random.Random(4)
    p = skia.Path()
    n = 18
    for i in range(n + 1):
        q = i / n * 2 * math.pi
        r_ = (120 + 60 * math.sin(q * 3 + 1) + rng.uniform(-14, 14)) * e_out(k)
        px_, py_ = x + math.cos(q) * r_ * 1.25, y + 40 + math.sin(q) * r_ * 0.7
        (p.moveTo if i == 0 else p.lineTo)(px_, py_)
    p.close()
    c.drawPath(p, P("#FFFDF5", 0.92 * a))
    c.drawCircle(x + 10, y + 40, 52 * e_back(clamp(k * 1.4)), rad_paint(x, y + 30, 60, ["#FFE066", "#FBBF24", "#F59E0B"], a=a))
    for i in range(9):
        q = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(60, 170) * e_out(k)
        sx, sy = x + math.cos(q) * d, y + 20 + math.sin(q) * d * 0.6
        sh = skia.Path()
        sh.moveTo(sx - 18, sy)
        sh.lineTo(sx + 4, sy - 16)
        sh.lineTo(sx + 20, sy + 6)
        sh.close()
        c.drawPath(sh, P("#EBD9B4", a))
    for i in range(4):                                                         # drips
        dx = -60 + i * 40
        dl = 40 + 80 * prog(k, 0.3, 1.0) * (0.5 + 0.5 * math.sin(i * 2.3))
        c.drawLine(x + dx, y + 80, x + dx, y + 80 + dl, P("#FFFDF5", 0.9 * a, stroke=14))


def hand(c, close, t, a=1.0, pads=0.0, crush=0.0):
    """A robot hand from the side, palm on the right, closing around (0, 0).  close 0 open .. 1 wrapped."""
    c.drawRRect(rr(330, -60, 260, 120, 30), lin_paint(0, -60, 0, 60, list(SHELL), a=a))   # wrist / forearm
    c.drawCircle(330, 0, 46, P(JOINT, a))
    c.drawRRect(rr(130, -150, 200, 300, 50), lin_paint(130, 0, 330, 0, ["#B8C2D0", "#FFFFFF", "#D5DCE6"], a=a))
    c.drawRRect(rr(130, -150, 200, 300, 50), P("#64748B", 0.6 * a, stroke=4))
    k = close + 0.25 * crush
    for j, (bx, by, dz) in enumerate(((150, -120, 0.0), (160, -88, 1.0))):         # two fingers seen from the side
        ang = 180.0
        x, y = bx, by
        segs = (96, 78, 60)
        for i, L in enumerate(segs):
            ang -= k * (36, 52, 50)[i]
            x1, y1 = x + math.cos(math.radians(ang)) * L, y + math.sin(math.radians(ang)) * L
            col = "#D5DCE6" if dz else "#FFFFFF"
            c.drawLine(x, y, x1, y1, P("#64748B", a, stroke=40 - i * 5))
            c.drawLine(x, y, x1, y1, P(col, a, stroke=32 - i * 5))
            c.drawCircle(x, y, 15 - i * 2, P(JOINT, a))
            x, y = x1, y1
        if pads > 0:
            add_glow(c, x, y, 50, CYAN, 0.8 * pads * a)
            c.drawCircle(x, y, 12, P(CYAN, pads * a))
    ang = 180.0                                                                      # the thumb
    x, y = 150, 118
    for i, L in enumerate((90, 70)):
        ang += k * (34, 56)[i]
        x1, y1 = x + math.cos(math.radians(ang)) * L, y + math.sin(math.radians(ang)) * L
        c.drawLine(x, y, x1, y1, P("#64748B", a, stroke=42 - i * 6))
        c.drawLine(x, y, x1, y1, P("#FFFFFF", a, stroke=34 - i * 6))
        c.drawCircle(x, y, 16 - i * 2, P(JOINT, a))
        x, y = x1, y1
    if pads > 0:
        add_glow(c, x, y, 50, CYAN, 0.8 * pads * a)
        c.drawCircle(x, y, 12, P(CYAN, pads * a))


def lantern(c, x, y, s, t, a=1.0):
    sw = math.sin(t * 1.6 + x * 0.01) * 4
    c.save()
    c.translate(x, y)
    c.rotate(sw)
    c.drawLine(0, -40 * s, 0, -24 * s, P("#7C2D12", a, stroke=3))
    add_glow(c, 0, 10 * s, 70 * s, "#F97316", 0.45 * a)
    c.drawOval(R(-34 * s, -26 * s, 68 * s, 64 * s), rad_paint(-8 * s, 0, 50 * s, ["#FF5A5A", "#DC2626", "#991B1B"], a=a))
    c.drawRect(R(-18 * s, -30 * s, 36 * s, 8 * s), P("#F59E0B", a))
    c.drawRect(R(-18 * s, 34 * s, 36 * s, 8 * s), P("#F59E0B", a))
    c.drawLine(0, 42 * s, 0, 70 * s, P("#F59E0B", a, stroke=3))
    c.restore()


def stick(c, x, y, ang, a=1.0):
    """A long pole with a pad (the push), its pad end at (x, y)."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawLine(0, 0, -900, 0, P("#92400E", a, stroke=20))
    c.drawLine(0, -6, -900, -6, P("#B45309", a, stroke=6))
    c.drawRRect(rr(-10, -34, 30, 68, 12), P("#FACC15", a))
    c.restore()


def sheet(c, x, y, w, h, t, a=1.0, wrap=0.0):
    """A fitted sheet: a soft pink cloth with elastic corners; wrap 0..1 flops it over the robot."""
    rng = random.Random(3)
    p = skia.Path()
    n = 16
    pts = []
    for i in range(n):
        q = i / n * 2 * math.pi
        rx = w / 2 * (1 - 0.25 * wrap) + 18 * math.sin(t * 3 + i)
        ry = h / 2 * (1 + 0.6 * wrap) + 14 * math.cos(t * 2.4 + i * 1.3)
        pts.append((x + math.cos(q) * rx + rng.uniform(-10, 10), y + math.sin(q) * ry * (0.7 if math.sin(q) < 0 else 1.0)))
    p.moveTo(*pts[0])
    for i in range(1, n + 1):
        q0, q1 = pts[i - 1], pts[i % n]
        p.quadTo(q0[0], q0[1], (q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2)
    p.close()
    c.drawPath(p, lin_paint(0, y - h / 2, 0, y + h / 2, ["#FBCFE8", "#F9A8D4", "#F472B6"], a=a))
    for i in range(5):
        c.drawLine(x - w * 0.3 + i * w * 0.15, y - h * 0.3, x - w * 0.25 + i * w * 0.14, y + h * 0.35, P("#DB2777", 0.35 * a, stroke=4))
    for cx_, cy_ in ((x - w * 0.42, y - h * 0.3), (x + w * 0.42, y - h * 0.3)):     # the elastic corners
        c.drawCircle(cx_, cy_, 22, P("#EC4899", 0.8 * a, stroke=6))


def bubble(c, x, y, s, p, rtl=False):
    """A speech bubble (screen space) with text s; its tail points down-left."""
    if p <= 0:
        return
    w = (arabic.width_ar(s, 44) if arabic.is_ar(s) else text_width(s, 40, "Poppins-Black")) + 70
    c.save()
    c.translate(x, y)
    k = e_back(clamp(p * 1.2))
    c.scale(k, k)
    c.drawRRect(rr(-w / 2, -50, w, 100, 40), P("#000000", 0.35, blur=12))
    c.drawRRect(rr(-w / 2, -50, w, 100, 40), P("#FFFFFF"))
    tail = skia.Path()
    tail.moveTo(-w / 2 + 60, 40)
    tail.lineTo(-w / 2 + 20, 90)
    tail.lineTo(-w / 2 + 100, 44)
    tail.close()
    c.drawPath(tail, P("#FFFFFF"))
    word(c, s, 0, 14, 40, "#0F172A")
    c.restore()


# ---------------------------------------------------------------------------------------------- sounds
def servo(d=0.25, f0=600.0, f1=900.0, seed=0):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = np.linspace(f0, f1, n)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / sfx.SR)) * 0.3 + sfx._bp(sfx._rng(seed).standard_normal(n), 800, 3000) * 0.4
    return sfx._norm(x * sfx._ar(n, 0.01, 0.06), 0.35)


def crack_snd(d=0.5, seed=7):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 1500, 6000) * np.exp(-tt * 18)
    return sfx._norm(x, 0.7)


def crowd(d=2.0, seed=8):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 300, 2500)
    return sfx._norm(x * np.sin(np.linspace(0, np.pi, n)) ** 0.6, 0.5)


# ====================================================================================== the episode
class Humanoid(EpisodeV2):
    BUILD_NO = 29
    COVER_T = ("closer", 0.9)                    # cover: arms up at the finish arch, after the cheer rings
    FIRST_SET = "lab"
    CLEAR = "#070B1F"
    TITLE = {"en": "HUMANOID ROBOT", "ar_sa": "روبوت شبه البني آدم"}
    EMPH = {"en": ["CONGRATS", "TWO", "LEGS", "BACKFLIP", "HUMANOID", "ROBOT", "SMALL", "FEET", "TIPS", "INNER", "EAR",
                   "SENSOR", "TILT", "MOTORS", "CORRECT", "HUNDREDS", "STANDS", "LIFTS", "LEG", "FALLS", "FACE", "STEP",
                   "SHIFTS", "WEIGHT", "OTHER", "FOOT", "WALKS", "BUMP", "PUSH", "DOWN", "THOUSANDS", "COPIES",
                   "COMPUTER", "FALLING", "YEARS", "HOURS", "REAL", "BRAIN", "STEADY", "EGG", "CRUSHES", "TOUCH",
                   "FINGERTIPS", "FEELS", "SQUEEZES", "FOLLOW", "STADIUM", "COOLS", "CAMERAS", "EYES", "BATTERY",
                   "HALF", "MARATHON", "BEIJING", "TWENTY-ONE", "THREE", "FORTY", "FASTEST", "YOURSELF", "BACKFLIPS",
                   "FOLD", "FITTED", "SHEET"],
            "ar_sa": ["مبروك", "رجلين", "بتتشقلب", "روبوت", "يقع", "ودن", "حساس", "ميلة", "موتورات", "مئات", "يرفع",
                      "وشه", "خطوة", "ينقل", "وزنه", "التانية", "بيمشي", "مطب", "زقة", "آلاف", "النسخ", "الكمبيوتر",
                      "سنين", "ساعة", "المخ", "ثابت", "بيضة", "يفعصها", "لمس", "صوابعه", "يحس", "بيضغط", "بالراحة",
                      "تابعني", "استاد", "كاميرات", "وبطارية", "ماراتون", "بكين", "واحد", "تلات", "ساعتين", "بإيدك",
                      "أمك", "عيش", "البطارية", "تخلص"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "LEGS"): "رجلين", ("hook", "BACKFLIP"): "بتتشقلب", ("hook", "CONGRATS"): "مبروك",
        ("hook", "HUMANOID"): "روبوت",
        ("break1", "FEET"): "رجلين", ("break1", "TIPS"): "يقع", ("break1", "LET"): "تسيبه",
        ("fix1", "INNER"): "ودن", ("fix1", "SENSOR"): "حساس", ("fix1", "TILT"): "ميلة", ("fix1", "MOTORS"): "موتورات",
        ("fix1", "CORRECT"): "تعدله", ("fix1", "HUNDREDS"): "مئات",
        ("break2", "STANDS"): "واقف", ("break2", "LIFTS"): "يرفع", ("break2", "FALLS"): "يقع", ("break2", "FACE"): "وشه",
        ("fix2", "STEP"): "خطوة", ("fix2", "SHIFTS"): "ينقل", ("fix2", "WEIGHT"): "وزنه", ("fix2", "OTHER"): "التانية",
        ("fix2", "LIKE"): "زيك",
        ("break3", "WALKS"): "بيمشي", ("break3", "BUMP"): "مطب", ("break3", "PUSH"): "زقة", ("break3", "DOWN"): "يقع",
        ("fix3", "THOUSANDS"): "آلاف", ("fix3", "COPIES"): "النسخ", ("fix3", "COMPUTER"): "الكمبيوتر",
        ("fix3", "FALLING"): "تقع", ("fix3", "GETTING"): "وتقوم", ("fix3", "YEARS"): "سنين", ("fix3", "HOURS"): "ساعة",
        ("fix3", "REAL"): "والروبوت", ("fix3", "BRAIN"): "المخ",
        ("break4", "STEADY"): "ثابت", ("break4", "EGG"): "بيضة", ("break4", "CRUSHES"): "يفعصها",
        ("fix4", "TOUCH"): "لمس", ("fix4", "FINGERTIPS"): "صوابعه", ("fix4", "FEELS"): "يحس", ("fix4", "SQUEEZES"): "بيضغط",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "CAMERAS"): "كاميرات", ("reveal", "EYES"): "كاميرات", ("reveal", "BATTERY"): "بطارية",
        ("reveal", "HALF"): "نص", ("reveal", "MARATHON"): "ماراتون", ("reveal", "BEIJING"): "بكين",
        ("stat", "TWENTY"): "واحد", ("stat", "THREE"): "تلات", ("stat", "TWO"): "ساعتين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "AFTER"): "وبعد", ("tag", "BACKFLIPS"): "يجري", ("tag", "FOLD"): "أمك", ("tag", "FITTED"): "عيش",
        ("tag", "SHEET"): "تخلص"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a stadium that cools itself"),
                   "stat": [("21", "KILOMETERS"), ("3", "BATTERY CHANGES"), ("2:40", "FASTEST ROBOT")],
                   "L": {"robot": "YOUR HUMANOID ROBOT", "feet": "TWO SMALL FEET", "tips": "TIPS OVER",
                         "ear": "INNER EAR", "fixes": "HUNDREDS OF FIXES A SECOND", "lift": "LIFTS A LEG",
                         "falls": "FLAT ON ITS FACE", "weight": "ITS WEIGHT", "over": "WEIGHT OVER THE OTHER FOOT",
                         "push": "ONE PUSH", "down": "DOWN AGAIN", "copies": "THOUSANDS OF COPIES",
                         "years": "YEARS OF PRACTICE", "hours": "IN HOURS", "brain": "THE NEW BRAIN",
                         "stays": "STAYS UP", "egg": "EGG", "crush": "CRUSHED", "pads": "TOUCH SENSORS",
                         "feels": "FEELS THE SQUEEZE", "gentle": "JUST RIGHT", "cams": "CAMERAS",
                         "battery": "BATTERY", "marathon": "HALF MARATHON", "arch": "21 KM", "sim": "SIMULATION",
                         "sheet": "FITTED SHEET", "bread": "", "dead": ""}},
            "ar_sa": {"follow": ("تابعني", "الجاي: استاد بيبرّد نفسه"),
                      "stat": [("21", "كيلو"), ("3", "مرات تغيير بطارية"), ("2:40", "أسرع روبوت")],
                      "L": {"robot": "الروبوت بتاعك", "feet": "رجلين صغيرين", "tips": "وقع",
                            "ear": "ودن من جوه", "fixes": "مئات المرات في الثانية", "lift": "رفع رجل",
                            "falls": "وقع على وشه", "weight": "وزنه", "over": "وزنه على الرجل التانية",
                            "push": "زقة صغيرة", "down": "وقع تاني", "copies": "آلاف النسخ",
                            "years": "سنين تمرين", "hours": "في كام ساعة", "brain": "المخ الجديد",
                            "stays": "ثابت", "egg": "بيضة", "crush": "اتفعصت", "pads": "حساسات لمس",
                            "feels": "بيحس بالضغط", "gentle": "بالراحة", "cams": "كاميرات",
                            "battery": "بطارية", "marathon": "نص ماراتون", "arch": "21 كيلو", "sim": "محاكاة",
                            "sheet": "", "bread": "انزل هات عيش!", "dead": "البطارية خلصت"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "legs": ("hook", "LEGS", 0.3), "backflip": ("hook", "BACKFLIP", 0.5), "congrats": ("hook", "CONGRATS", 0.65),
            "humanoid": ("hook", "HUMANOID", 0.9),
            "feet": ("break1", "FEET", 0.3), "tips": ("break1", "TIPS", 0.55), "letgo": ("break1", "LET", 0.85),
            "inner": ("fix1", "INNER", 0.15), "sensor": ("fix1", "SENSOR", 0.3), "tilt": ("fix1", "TILT", 0.45),
            "motors": ("fix1", "MOTORS", 0.6), "correct": ("fix1", "CORRECT", 0.7), "hundreds": ("fix1", "HUNDREDS", 0.8),
            "stands": ("break2", "STANDS", 0.15), "lifts": ("break2", "LIFTS", 0.5), "falls": ("break2", "FALLS", 0.75),
            "face": ("break2", "FACE", 0.95),
            "step": ("fix2", "STEP", 0.15), "shifts": ("fix2", "SHIFTS", 0.3), "weight": ("fix2", "WEIGHT", 0.45),
            "other": ("fix2", "OTHER", 0.6), "like": ("fix2", "LIKE", 0.8),
            "walks": ("break3", "WALKS", 0.15), "bump": ("break3", "BUMP", 0.45), "push": ("break3", "PUSH", 0.7),
            "down": ("break3", "DOWN", 0.95),
            "thousands": ("fix3", "THOUSANDS", 0.05), "copies": ("fix3", "COPIES", 0.12), "computer": ("fix3", "COMPUTER", 0.3),
            "falling": ("fix3", "FALLING", 0.4), "getting": ("fix3", "GETTING", 0.5), "years": ("fix3", "YEARS", 0.6),
            "hours": ("fix3", "HOURS", 0.72), "real": ("fix3", "REAL", 0.82), "brain": ("fix3", "BRAIN", 0.95),
            "steady": ("break4", "STEADY", 0.15), "egg": ("break4", "EGG", 0.55), "crushes": ("break4", "CRUSHES", 0.85),
            "touch": ("fix4", "TOUCH", 0.25), "fingertips": ("fix4", "FINGERTIPS", 0.5), "feels": ("fix4", "FEELS", 0.7),
            "squeezes": ("fix4", "SQUEEZES", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "cameras": ("reveal", "CAMERAS", 0.15), "eyes": ("reveal", "EYES", 0.25), "battery": ("reveal", "BATTERY", 0.4),
            "half": ("reveal", "HALF", 0.6), "marathon": ("reveal", "MARATHON", 0.7), "beijing": ("reveal", "BEIJING", 0.92),
            "s1": ("stat", "TWENTY", 0.04), "s2": ("stat", "THREE", 0.35), "s3": ("stat", "TWO", 0.6),
            "cong2": ("closer", "CONGRATS", 0.16),
            "after": ("tag", "AFTER", 0.1), "flips": ("tag", "BACKFLIPS", 0.35), "fold": ("tag", "FOLD", 0.6),
            "fitted": ("tag", "FITTED", 0.75), "sheet": ("tag", "SHEET", 0.9)})
        T["flip0"] = 0.12                                                     # hook: the backflip
        T["tip1"] = min(T["tips"], T["letgo"]) - 0.2                          # break1: it tips over
        T["lift2"] = T["lifts"] - 0.1                                        # break2: lifts a leg, falls
        T["fall2"] = max(T["lift2"] + 0.6, min(T["falls"], T["face"]) - 0.1)
        T["shift"] = min(T["shifts"], T["weight"]) - 0.15                    # fix2: weight over the left foot
        T["push3"] = max(T["push"], T["bump"] + 0.3) - 0.1                   # break3: the push
        T["cut3"] = T["real"] - 0.15                                         # fix3: back to the lab
        T["crush4"] = T["crushes"] - 0.15
        T["grip4"] = min(T["feels"], T["squeezes"]) - 0.3
        T["run"] = min(T["half"], T["marathon"]) - 0.2                       # reveal: off it runs
        T["t_end"] = min(T["fitted"], T["sheet"]) - 0.3                        # tag: tangled / the battery dies
        # ---- sets
        for lab in ("break1", "fix1", "break2", "fix2", "break3"):
            self.cut(s(lab) - 0.12, "lab", 1 if lab.startswith("break") else -1)
        self.cut(s("fix3") - 0.12, "sim", -1)
        self.cut(T["cut3"], "lab", 1)
        self.cut(s("break4") - 0.12, "hand", 1)
        self.cut(s("fix4") - 0.12, "hand", -1)
        self.cut(s("cta") - 0.12, "lab", 1)
        self.cut(s("reveal") - 0.12, "road", 1)
        self.cut(s("tag") - 0.2, "lab", 1)
        self.cams = {"lab": Camera(0, -230, 1.2), "hand": Camera(60, 0, 1.0)}
        cm = self.cams["lab"]
        cm.key(T["flip0"] + 1.6, 0, -210, 1.35, 1.2)
        cm.key(s("break1") - 0.12, 0, -170, 1.45, 0.0).key(T["tip1"], 140, -150, 1.25, 1.2)
        cm.key(s("fix1") - 0.12, 0, -200, 1.45, 0.0).key(s("fix1"), 0, -210, 1.5, 4.0)
        cm.key(s("break2") - 0.12, 0, -190, 1.35, 0.0).key(T["fall2"], 120, -160, 1.25, 1.0)
        cm.key(s("fix2") - 0.12, 0, -190, 1.35, 0.0)
        cm.key(s("break3") - 0.12, -60, -200, 1.3, 0.0).key(T["push3"], 100, -170, 1.25, 1.0)
        cm.key(T["cut3"], 0, -200, 1.3, 0.0)
        cm.key(s("cta") - 0.12, 200, -160, 1.25, 0.0)
        cm.key(s("tag") - 0.2, 0, -200, 1.3, 0.0).key(s("tag"), 0, -210, 1.35, 3.0)
        self.cams["hand"].key(s("break4"), 40, 0, 1.08, 3.5).key(s("fix4") - 0.12, 60, 0, 1.0, 0.0)
        self.cams["hand"].key(s("fix4"), 40, 0, 1.08, 3.5)
        # ---- tracks
        self.hand_close = Track(0.0).to(T["egg"] + 0.1, 0.72, 0.6).to(T["crush4"], 1.05, 0.25, e_in)
        self.hand_close.to(s("fix4") - 0.12, 0.0, 0.0).to(T["fingertips"], 0.72, 0.7).to(T["grip4"], 0.76, 0.4)
        self.pads = Track(0.0).to(T["touch"] - 0.1, 1.0, 0.4)
        self.meter = Track(0.0).to(T["egg"] + 0.1, 0.55, 0.6).to(T["crush4"], 1.0, 0.25)
        self.meter.to(s("fix4") - 0.12, 0.0, 0.0).to(T["fingertips"], 0.5, 0.7).to(T["grip4"], 0.58, 0.4)
        self.spans = [(T["tip1"] + 0.4, T["hundreds"] + 0.3), (T["fall2"] + 0.4, T["like"] + 0.3),
                      (T["push3"] + 0.4, T["brain"] + 0.4), (T["crush4"] + 0.1, T["squeezes"] + 0.3)]
        self.shakes = [(T["flip0"] + 1.0, 0.3, 10), (T["congrats"], 0.3, 6), (T["tip1"] + 0.55, 0.4, 14),
                       (T["fall2"] + 0.5, 0.4, 14), (T["push3"] + 0.55, 0.4, 14), (T["crush4"] + 0.1, 0.35, 10),
                       (s("closer") + 0.2, 0.35, 10)]
        rng = random.Random(29)
        self.sims = [(rng.uniform(0, 2.6), rng.random() < 0.5) for _ in range(30)]
        self.crowd = [(rng.uniform(-1, 1), rng.uniform(0, 1), rng.choice(("#1E1B4B", "#312E81", "#3B0764", "#172554")))
                      for _ in range(60)]

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    # ------------------------------------------------------------------ the lab and the robot's moves
    def lab_back(self, c, t, cam):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, gy, ["#0B1030", "#141A45", "#1D2456"]))
        wx0, wy0 = 120 - cx * 0.15 * z, gy - 1050 * z ** 0.4                       # the big window
        ww, wh = 840, 720
        c.save()
        c.clipRect(R(wx0, wy0, ww, wh))
        v2.sky(c, W, H, 0.0, horizon_y=wy0 + wh * 0.82)
        v2.stars(c, W, H, t, 0.6)
        skyline_night(c, wx0 - 40, wx0 + ww + 40, base_y=wy0 + wh, seed=7, hmin=140, hmax=420, t=t)
        c.restore()
        for k in range(1, 3):
            c.drawRect(R(wx0 + k * ww / 3 - 6, wy0, 12, wh), P("#0B1030"))
        c.drawRect(R(wx0 + 0, wy0 + wh / 2 - 6, ww, 12), P("#0B1030"))
        c.drawRect(R(wx0, wy0, ww, wh), P("#2B3470", 1, stroke=14))
        c.drawRect(R(0, gy, W, H - gy), lin_paint(0, gy, 0, H, ["#2A3166", "#151A3A", "#0A0D20"]))
        c.drawRect(R(0, gy - 3, W, 6), P("#3B4486"))
        return gy

    def robot_lab(self, t):
        """The robot's pose and placement in the lab: (pose, pivot, angle, extra kwargs, dx, dy)."""
        T, s = self.T, self.tl.s
        st = pose()
        if t < s("break1") - 0.12:                                                   # hook: the backflip
            u = t - T["flip0"]
            if u < 0.25:
                k = e_out(clamp(u / 0.25))
                return mixp(st, pose(py=PELV + 70, hl=(-60, -40), hr=(60, -40), lean=0), k), None, 0.0, {}, 0.0, 0.0
            if u < 1.15:
                v = (u - 0.25) / 0.9
                tuck = math.sin(v * math.pi)
                p = mixp(pose(py=PELV + 20), pose(py=PELV + 60, fl=(-50, -170), fr=(50, -170), hl=(-70, 80), hr=(70, 80)), tuck)
                jy = -4 * 280 * v * (1 - v)
                return p, None, -360 * e_io(v), {}, 0.0, jy
            k = clamp((u - 1.15) / 0.35)
            land = pose(py=PELV + 60 * (1 - e_out(k)), hl=(-120, -20 + 50 * k), hr=(120, -20 + 50 * k))
            if t > T["humanoid"] - 0.3:
                q = prog(t, T["humanoid"] - 0.3, T["humanoid"] + 0.2)
                land = mixp(land, pose(hl=(-150, -260), hr=(150, -260)), q)
            return land, None, 0.0, {}, 0.0, 0.0
        if t < s("fix1") - 0.12:                                                     # break1: tips over
            u = prog(t, T["tip1"], T["tip1"] + 0.7)
            wob = math.sin((t - s("break1")) * 9) * 2 * (1 - u)
            return pose(hl=(-110, 20), hr=(110, 20)), (44 + 34, 0), wob + 88 * e_in(u), {}, 0.0, 0.0
        if t < s("break2") - 0.12:                                                   # fix1: the inner ear
            u = t - s("fix1")
            sway = math.sin(u * 4.2) * 9 * math.exp(-max(0.0, t - T["motors"]) * 1.4) * prog(t, s("fix1"), s("fix1") + 0.4)
            arm = sway * 2.5
            p = pose(lean=-sway * 0.6, hl=(-110 - arm, 20 + arm), hr=(110 - arm, 20 - arm))
            gl = 0.6 * clamp(abs(math.sin(u * 30))) * prog(t, T["motors"] - 0.2, T["motors"] + 0.2)
            return p, (0, 0), sway, {"gyro": prog(t, T["inner"] - 0.2, T["inner"] + 0.3),
                                     "glow": {"ankle": gl, "knee": gl * 0.8, "hip": gl * 0.7}}, 0.0, 0.0
        if t < s("fix2") - 0.12:                                                     # break2: lift a leg, fall
            k = prog(t, T["lift2"], T["lift2"] + 0.4)
            p = pose(fr=(54, -110 * e_out(k)), hl=(-120, 0), hr=(120, 0))
            u = prog(t, T["fall2"], T["fall2"] + 0.6)
            return p, (-10, 0), 84 * e_in(u) + 4 * k, {}, 0.0, 0.0
        if t < s("break3") - 0.12:                                                   # fix2: shift, then step
            u = t - T["shift"]
            cyc = 1.5
            if u < 0:
                return pose(hl=(-110, 20), hr=(110, 20)), None, 0.0, {}, 0.0, 0.0
            ph = (u % (2 * cyc)) / cyc
            side = -1 if ph < 1 else 1                                               # -1: weight on the left foot
            ph = ph % 1.0
            sh = e_io(clamp(ph / 0.35)) if ph < 0.85 else 1 - e_io(clamp((ph - 0.85) / 0.15))
            lift = math.sin(clamp((ph - 0.35) / 0.5) * math.pi) * 90 if ph > 0.35 else 0.0
            px = side * 42 * sh
            p = pose(px=px, lean=-side * 4 * sh, hl=(-110 + side * 20 * sh, 20), hr=(110 + side * 20 * sh, 20))
            if side < 0:
                p["fr"] = (44, -lift)
            else:
                p["fl"] = (-44, -lift)
            return p, None, 0.0, {}, 0.0, 0.0
        if t < s("fix3") - 0.12:                                                     # break3: walking, then the push
            u = t - s("break3")
            ph = u * 4.2
            lift = max(0.0, math.sin(ph)) * 60
            lift2 = max(0.0, -math.sin(ph)) * 60
            sh = math.sin(ph) * 30
            p = pose(px=-sh, fl=(-44, -lift2), fr=(44, -lift), hl=(-110, 20 + sh), hr=(110, 20 - sh))
            k = prog(t, T["push3"], T["push3"] + 0.25)
            fall = prog(t, T["push3"] + 0.2, T["push3"] + 0.8)
            if k > 0:
                p = mixp(p, pose(hl=(-150, -60), hr=(150, -60), fl=(-44, 0), fr=(44, 0)), k)
            return p, (44 + 34, 0), 10 * k + 78 * e_in(fall), {}, 0.0, 0.0
        if t < s("break4") - 0.12:                                                   # fix3 (end): the new brain
            k = prog(t, T["brain"] + 0.25, T["brain"] + 0.45)
            rec = prog(t, T["brain"] + 0.45, T["brain"] + 0.9)
            p = pose(hl=(-110, 20), hr=(110, 20))
            if k > 0:
                p = mixp(p, pose(px=30, fr=(120, 0), hl=(-150, -40), hr=(150, -40)), math.sin(rec * math.pi) if rec < 1 else 0.0)
            ang = 12 * k * (1 - rec)
            return p, (44 + 34, 0), ang, {"brain": prog(t, T["brain"] - 0.1, T["brain"] + 0.3) * (1 - prog(t, T["brain"] + 0.6, T["brain"] + 1.2))}, 0.0, 0.0
        if t < s("reveal") - 0.12:                                                   # cta: on the floor, trying to get up
            p = pose(hl=(-150, -40), hr=(130, -60 + 20 * math.sin(t * 3)), fl=(-50, -10), fr=(40, 0))
            return p, (44 + 34, 0), 86, {}, 0.0, 0.0
        # the tag
        if self.rtl:                                                                 # the battery dies
            k = prog(t, T["t_end"], T["t_end"] + 0.7)
            p = mixp(pose(hl=(-110, 20), hr=(110, 20)), pose(py=PELV + 60, lean=0, hl=(-80, 110), hr=(80, 110), head=0.0), e_in(k))
            p["head"] = 18 * e_in(k)
            return p, None, 0.0, {"bat": lerp(0.9, 0.0, prog(t, T["fold"], T["t_end"] + 0.3)), "eyes": 1 - k}, 0.0, 0.0
        u = t - s("tag")
        wrap = prog(t, T["t_end"], T["t_end"] + 0.6)
        flip = prog(t, T["flips"] - 0.5, T["flips"] + 0.3)
        p = pose(hl=(-150, -150 + 60 * math.sin(u * 5)), hr=(150, -150 - 60 * math.sin(u * 5)))
        if wrap > 0:
            p = mixp(p, pose(hl=(-60, -190), hr=(70, -170), lean=10 * math.sin(t * 6), fl=(-60, 0), fr=(30, 0)), wrap)
        return p, None, 0.0, {"err": wrap}, 0.0, 0.0

    def draw_lab(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["lab"].at(t)
        self.lab_back(c, t, cam)
        self.view(c, cam)
        c.drawOval(R(-330, -24, 660, 48), P("#3B4486", 0.6))                         # the mat
        c.drawOval(R(-280, -16, 560, 32), P("#4C56A0", 0.5))
        p, pivot, ang, kw, dx, dy = self.robot_lab(t)
        sup = s("break2") - 0.12 <= t < s("break3") - 0.12                            # weight and support (break2, fix2)
        if sup:
            self.support(c, p, t, ang, zone=True)
        contact_shadow(c, dx, 0, 220, 0.5)
        if t < s("break1") - 0.12 and T["flip0"] + 0.25 <= t < T["flip0"] + 1.15:
            c.save()
            c.translate(dx, dy + PELV + 30)
            c.rotate(ang)
            c.translate(0, -(PELV + 30))
            robot(c, p, t=t, **kw)
            c.restore()
            v2.smoke(c, 0, -10, t, T["flip0"] + 0.25, T["flip0"] + 0.6, rate=20, life=0.6, spread=(200, -10), rise=-20,
                     size=(14, 50), col="#94A3B8", lit=None, lit_until=0.0, seed=3, a=0.4)
        else:
            robot_at(c, dx, dy, 1.0, p, pivot=pivot, ang=ang, t=t, **kw)
        if sup:
            self.support(c, p, t, ang, zone=False)
        if t < s("break1") - 0.12 and t >= T["flip0"] + 1.15:
            v2.smoke(c, 0, -10, t, T["flip0"] + 1.15, T["flip0"] + 1.5, rate=20, life=0.6, spread=(260, -10), rise=-20,
                     size=(14, 60), col="#94A3B8", lit=None, lit_until=0.0, seed=4, a=0.45)
        if s("break3") - 0.12 <= t < s("fix3") - 0.12:                                # the push
            u = prog(t, T["push3"] - 0.5, T["push3"] + 0.1)
            if u > 0:
                stick(c, lerp(-900, -100, e_in(u)), -330, 8)
        if T["cut3"] <= t < s("break4") - 0.12:                                       # the push it takes now
            u = prog(t, T["brain"] + 0.05, T["brain"] + 0.3) * (1 - prog(t, T["brain"] + 0.6, T["brain"] + 0.9))
            if u > 0:
                stick(c, lerp(-900, -100, e_in(u)), -330, 8)
            bk = prog(t, T["brain"] - 0.4, T["brain"] - 0.05)
            if 0 < bk < 1:                                                           # the brain drops in
                bx, by = 0, lerp(-1100, -560, e_in(bk))
                add_glow(c, bx, by, 90, "#F0ABFC", 0.9)
                c.drawCircle(bx, by, 34, P("#F0ABFC"))
                for j in range(5):
                    q = j * 1.3
                    c.drawCircle(bx + math.cos(q) * 18, by + math.sin(q) * 14, 9, P("#FFFFFF", 0.6))
        if t >= s("tag") - 0.2 and not self.rtl:                                     # the fitted sheet
            wrap = prog(t, T["t_end"], T["t_end"] + 0.6)
            if wrap <= 0:
                sheet(c, 0, -500, 440, 230, t)
            else:
                sheet(c, 0, lerp(-500, -300, wrap), lerp(440, 380, wrap), lerp(230, 250, wrap), t, wrap=wrap)
        c.restore()
        self.ui["cam"] = cam
        self.ui["pose"] = (p, pivot, ang)

    def support(self, c, p, t, ang=0.0, zone=True):
        """break2 / fix2: the green zone under the standing feet (zone) and the line down from the robot's weight."""
        feet = [f for f in (p["fl"], p["fr"]) if f[1] > -8]
        if not feet:
            return
        x0, x1 = min(f[0] for f in feet) - 40, max(f[0] for f in feet) + 40
        if zone:
            c.drawRRect(rr(x0, -6, x1 - x0, 14, 7), P(GOOD, 0.85))
            add_glow(c, (x0 + x1) / 2, 0, (x1 - x0) * 0.6, GOOD, 0.4)
            return
        wx = p["px"]
        if abs(ang) > 6:
            return
        inside = x0 <= wx <= x1
        col = GOOD if inside else WARN
        c.drawLine(wx, PELV - 40, wx, -8, dash_paint(col, 0.95, w=6, t=t, dash=18, gap=12))
        c.drawCircle(wx, PELV - 40, 22, P(HILITE))
        c.drawCircle(wx, PELV - 40, 22, P("#0F172A", 1, stroke=4))

    def ui_lab(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 470, "robot", T["humanoid"] - 0.15, s("break1") + 0.2, accent=HILITE, size=38)
            return
        if tw < s("fix1") - 0.12:
            x0, y0 = self.at(44, -10)
            self.label(x0, y0, 820, 1090, "feet", T["feet"] - 0.1, T["tip1"] + 0.2, HILITE, size=32)
            self.chip(540, 470, "tips", T["tip1"] + 0.3, s("fix1") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["tip1"] + 0.6, s("fix1") - 0.2, x=880, y=330)
            self.red(T["tip1"] + 0.6, 1.8)
            return
        if tw < s("break2") - 0.12:
            p, pivot, ang = self.ui.get("pose", (pose(), None, 0.0))
            x0, y0 = self.at(0, PELV - 105)
            self.label(x0, y0, 250, 640, "ear", T["inner"], T["motors"] + 0.4, CYAN, size=34)
            self.chip(540, 470, "fixes", T["correct"] - 0.2, s("break2") - 0.15, accent=CYAN, size=34)
            self.badge("check", T["hundreds"] + 0.2, s("break2") - 0.15, x=880, y=330)
            return
        if tw < s("fix2") - 0.12:
            self.chip(540, 470, "lift", T["lift2"], T["fall2"] + 0.2, accent=HILITE, size=40)
            self.chip(540, 470, "falls", T["fall2"] + 0.3, s("fix2") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["fall2"] + 0.5, s("fix2") - 0.2, x=880, y=330)
            self.red(T["fall2"] + 0.5, 1.8)
            return
        if tw < s("break3") - 0.12:
            p, pivot, ang = self.ui.get("pose", (pose(), None, 0.0))
            x0, y0 = self.at(p["px"], PELV - 40)
            self.label(x0, y0, 820, 640, "weight", T["weight"] - 0.2, T["like"], HILITE, size=32)
            self.chip(540, 470, "over", T["other"] - 0.2, s("break3") - 0.15, accent=GOOD, size=34)
            self.badge("check", T["like"] + 0.1, s("break3") - 0.15, x=880, y=330)
            return
        if tw < s("fix3") - 0.12:
            self.chip(540, 470, "push", T["push3"] - 0.2, T["push3"] + 0.6, accent="#FDBA74", size=40)
            self.chip(540, 470, "down", T["push3"] + 0.7, s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["push3"] + 0.8, s("fix3") - 0.2, x=880, y=330)
            self.red(T["push3"] + 0.8, 1.6)
            return
        if tw < s("break4") - 0.12:
            x0, y0 = self.at(0, -440)
            self.label(x0, y0, 780, 600, "brain", T["brain"] - 0.1, s("break4") - 0.15, "#F0ABFC", size=32)
            self.chip(540, 470, "stays", T["brain"] + 0.6, s("break4") - 0.15, accent=GOOD, size=40)
            self.badge("check", T["brain"] + 0.7, s("break4") - 0.15, x=880, y=330)
            return
        if tw < s("reveal") - 0.12:
            return
        if self.rtl:                                                                    # tag (Arabic): bread
            bubble(c, 330, 560, self.L["bread"], self.span(T["fold"] - 0.1, self.duration, 0.25, 0.1), rtl=True)
            self.chip(540, 1120, "dead", T["t_end"] + 0.4, self.duration, accent=WARN, size=40)
        else:
            x0, y0 = self.at(180, -600)
            self.label(x0, y0, 800, 560, "sheet", T["fold"] - 0.1, self.duration, "#F9A8D4", size=34)

    # ------------------------------------------------------------------ set: the simulation wall (fix3)
    def draw_sim(self, c, t):
        T, s = self.T, self.tl.s
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#060A1E", "#0B1030", "#05070F"]))
        k = prog(t, s("fix3") - 0.12, s("fix3") + 0.2)
        x0, y0, w, h = 50, 470, 980, 690
        c.drawRRect(rr(x0 - 14, y0 - 14, w + 28, h + 28, 30), P("#1E293B"))
        c.drawRRect(rr(x0, y0, w, h, 20), lin_paint(0, y0, 0, y0 + h, ["#0E1B3D", "#0A1430"]))
        c.save()
        c.clipRRect(rr(x0, y0, w, h, 20), skia.ClipOp.kIntersect, True)
        for gx in range(0, w, 40):
            c.drawLine(x0 + gx, y0, x0 + gx, y0 + h, P(CYAN, 0.06, stroke=1))
        for gy in range(0, h, 40):
            c.drawLine(x0, y0 + gy, x0 + w, y0 + gy, P(CYAN, 0.06, stroke=1))
        cols, rows = 6, 5
        cw, chh = w / cols, (h - 56) / rows
        speed = 1.0 + 2.5 * prog(t, T["years"] - 0.3, T["hours"])
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                ph0, side = self.sims[idx]
                cyc = 2.4
                u = ((t * speed + ph0) % cyc) / cyc
                fx, fy = x0 + cw * (j + 0.5), y0 + 56 + chh * (i + 0.88)
                c.drawLine(fx - cw * 0.4, fy + 2, fx + cw * 0.4, fy + 2, P(CYAN, 0.3, stroke=2))
                if u < 0.35:
                    ang = 0.0
                elif u < 0.5:
                    ang = 85 * e_in((u - 0.35) / 0.15)
                elif u < 0.7:
                    ang = 85.0
                else:
                    ang = 85 * (1 - e_io((u - 0.7) / 0.3))
                ang *= -1 if side else 1
                sc = 0.21 * e_back(clamp(k * 1.5 - idx * 0.02)) if k < 1 else 0.21
                if sc <= 0.01:
                    continue
                pv = (44 + 34, 0) if ang > 0 else (-78, 0)
                robot_at(c, fx, fy, sc, pose(hl=(-110, 20), hr=(110, 20)), pivot=pv, ang=ang, t=t, eyes=0.8)
        c.restore()
        c.drawRRect(rr(x0, y0, w, h, 20), P(CYAN, 0.35, stroke=4))
        c.drawRRect(rr(x0, y0, w, 56, 20), P(CYAN, 0.18))
        word(c, self.L["sim"], 540, y0 + 40, 30, CYAN, 0.95)
        for j in range(3):
            c.drawCircle(x0 + 34 + j * 26, y0 + 28, 8, P(("#F87171", "#FBBF24", "#34D399")[j]))
        self.ui["cam"] = (0, 0, 1.0)

    def ui_sim(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 340, "copies", T["thousands"], T["years"] - 0.1, accent=CYAN, size=38)
        k = self.span(T["years"] - 0.15, T["cut3"], 0.2, 0.1)
        if k > 0:
            yrs = int(1 + 49 * e_in(prog(tw, T["years"], T["cut3"])))
            hrs = 1 + int(3 * prog(tw, T["years"], T["cut3"]))
            hk = k * prog(tw, T["hours"] - 0.2, T["hours"])
            if self.rtl:
                v2.chip(c, 540, 340, f"{self.L['years']}: {yrs}", k, accent=HILITE, size=38)
                v2.chip(c, 540, 418, f"{self.L['hours']}", hk, accent=GOOD, size=34)
            else:
                v2.chip(c, 540, 340, f"{self.L['years']}: {yrs}", k, accent=HILITE, size=38)
                v2.chip(c, 540, 418, f"{self.L['hours']} ({hrs} h)", hk, accent=GOOD, size=34)

    # ------------------------------------------------------------------ set: the hand and the egg (break4, fix4)
    def draw_hand(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["hand"].at(t)
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#101640", "#1A2156", "#0B0F2A"]))
        add_glow(c, 540, 820, 700, "#3B82F6", 0.25)
        self.view(c, cam)
        fixed = t >= s("fix4") - 0.12
        c.drawRect(R(-900, 230, 1800, 1400), lin_paint(0, 230, 0, 900, ["#2A3166", "#121634"]))  # the table
        c.drawRect(R(-900, 226, 1800, 8), P("#3B4486"))
        cl = self.hand_close.at(t)
        crushed = (not fixed) and t >= T["crush4"]
        hy = 0.0
        if fixed:
            hy = -60 * prog(t, T["squeezes"], T["squeezes"] + 0.8)                     # lifts it, gently
        c.save()
        c.translate(0, hy)
        if not crushed:
            egg(c, 0, 0, 1.0)
        c.restore()
        if crushed:
            splat(c, 0, 60, prog(t, T["crush4"], T["crush4"] + 0.5))
        c.save()
        c.translate(0, hy)
        hand(c, cl, t, pads=self.pads.at(t) if fixed else 0.0, crush=0.0)
        c.restore()
        c.restore()
        self.ui["cam"] = cam
        self.ui["fixed"] = fixed

    def ui_hand(self, c, t, tw):
        T, s = self.T, self.tl.s
        fixed = self.ui.get("fixed")
        m = self.meter.at(tw)                                                        # the squeeze meter
        k = self.span(s("break4"), s("cta") - 0.15)
        if k > 0:
            x, y0, hgt = 960, 420, 380
            c.drawRRect(rr(x - 34, y0 - 14, 68, hgt + 28, 30), P("#0F172A", 0.92 * k))
            c.drawRect(R(x - 18, y0 + hgt * 0.32, 36, hgt * 0.22), P(GOOD, 0.35 * k))
            col = GOOD if m < 0.7 else WARN
            c.drawRRect(rr(x - 18, y0 + hgt * (1 - m), 36, hgt * m, 14), P(col, k))
            c.drawRRect(rr(x - 34, y0 - 14, 68, hgt + 28, 30), P("#FFFFFF", 0.3 * k, stroke=3))
        if not fixed:
            x0, y0_ = self.at(0, -96)
            self.label(x0, y0_, 300, 560, "egg", T["egg"] - 0.1, T["crush4"], "#FDE68A", size=34)
            self.chip(540, 470, "crush", T["crush4"] + 0.1, s("fix4") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["crush4"] + 0.3, s("fix4") - 0.2, x=880, y=330)
            self.red(T["crush4"] + 0.3, 1.8)
            return
        x0, y0_ = self.at(-60, -150)
        self.label(x0, y0_, 300, 560, "pads", T["touch"], T["feels"], CYAN, size=34)
        self.chip(540, 470, "feels", T["feels"] - 0.2, s("cta") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["squeezes"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: the marathon road (reveal, stat, closer)
    def draw_road(self, c, t):
        T, s = self.T, self.tl.s
        hy = 760.0
        v2.sky(c, W, H, 0.0, horizon_y=hy)
        v2.stars(c, W, H, t, 0.7)
        skyline_night(c, -60, W + 60, base_y=hy, seed=11, hmin=120, hmax=380, t=t)
        run = prog(t, T["run"], T["run"] + 0.6)
        ph = (t - T["run"]) * 9.0 if t > T["run"] else 0.0
        c.drawRect(R(0, hy, W, H - hy), lin_paint(0, hy, 0, H, ["#2B2350", "#1A1636", "#0B0A18"]))
        road = skia.Path()
        road.moveTo(540 - 50, hy)
        road.lineTo(540 + 50, hy)
        road.lineTo(1500, H)
        road.lineTo(-420, H)
        road.close()
        c.drawPath(road, lin_paint(0, hy, 0, H, ["#3A3F55", "#4A5068", "#2A2E40"]))
        dist = (t - T["run"]) * 1.4 * run if t > T["run"] else 0.0
        for i in range(14):                                                           # centre dashes rushing at us
            zf = ((i * 2.2 - dist * 6) % 30.8) + 1.0
            y0, y1 = hy + 1160 / zf, hy + 1160 / (zf + 0.9)
            w0 = 26 / zf + 2
            c.drawRect(R(540 - w0, min(y0, y1), 2 * w0, abs(y0 - y1)), P("#F8FAFC", 0.75))
        for side in (-1, 1):                                                          # the crowd
            for j, (u, v, col) in enumerate(self.crowd):
                if (j % 2 == 0) != (side < 0):
                    continue
                zf = 1.6 + v * 6
                bx = 540 + side * (560 + 300 * u) / zf * 1.7
                by = hy + 1160 / zf
                hh = 260 / zf
                bob = abs(math.sin(t * 6 + j)) * 10 / zf * (1 + 2 * run)
                c.drawRRect(rr(bx - hh * 0.18, by - hh - bob, hh * 0.36, hh, hh * 0.12), P(col, 0.95))
                c.drawCircle(bx, by - hh - bob - hh * 0.14, hh * 0.14, P(col, 0.95))
                if j % 3 == 0:
                    c.drawLine(bx + hh * 0.15, by - hh * 0.85 - bob, bx + hh * 0.35, by - hh * 1.25 - bob, P(col, 0.95, stroke=hh * 0.08))
        ak = prog(t, s("reveal") + 0.2, s("reveal") + 0.8)                            # the start/finish arch
        ay = hy + 1160 / 7.0
        aw = 900 / 7.0 * 1.7
        c.drawLine(540 - aw, ay, 540 - aw, ay - 340, P(LAMP, ak, stroke=26))
        c.drawLine(540 + aw, ay, 540 + aw, ay - 340, P(LAMP, ak, stroke=26))
        c.drawRRect(rr(540 - aw - 30, ay - 430, 2 * aw + 60, 96, 30), P(LAMP, ak))
        c.drawRRect(rr(540 - aw - 30, ay - 430, 2 * aw + 60, 96, 30), P("#FDE68A", ak, stroke=4))
        word(c, self.L["arch"], 540, ay - 366, 46, "#FFFFFF", ak)
        rope = skia.Path()                                                            # lanterns across the top
        rope.moveTo(-20, 300)
        rope.quadTo(540, 430, 1100, 300)
        c.drawPath(rope, P("#3F2A1A", 1, stroke=4))
        for i in range(7):
            u = (i + 0.5) / 7
            lx = lerp(-20, 1100, u)
            ly = 300 + 4 * 65 * u * (1 - u) * 1.0 + 60
            lantern(c, lx, ly, 1.2, t)
        # the robot, jogging toward us
        sc = 1.2
        feet_y = 1230.0
        if t < T["run"]:
            p = pose(hl=(-110, 20), hr=(110, 20))
        else:
            p = mixp(pose(hl=(-110, 20), hr=(110, 20)), run_pose(ph), run)
        if t >= s("closer") - 0.1:
            q = prog(t, s("closer") - 0.1, s("closer") + 0.3)
            p = mixp(p, pose(hl=(-170, -280), hr=(170, -280), py=PELV - 30 * abs(math.sin(t * 6))), q)
        bat = None
        if T["battery"] - 0.2 <= t < T["run"] + 1.0:
            bat = prog(t, T["battery"] - 0.1, T["battery"] + 0.8)
        bib = "29" if t >= T["run"] + 1.0 else None
        contact_shadow(c, 540, feet_y, 260, 0.5)
        robot_at(c, 540, feet_y, sc, p, t=t, eyes=lerp(0.25, 1.0, prog(t, T["cameras"] - 0.2, T["cameras"] + 0.3)),
                 cam=prog(t, T["cameras"] - 0.1, T["cameras"] + 0.4) * (1 - prog(t, T["run"], T["run"] + 0.5)), bat=bat, bib=bib)
        if t >= T["cong2"]:
            for k in range(4):
                v2.shock_ring(c, 220 + k * 210, 640 + (k % 2) * 80, t, T["cong2"] + 0.2 * k, 0.9, r1=160,
                              col=("#FDE68A", "#F472B6", "#7DD3FC", "#A7F3D0")[k], width=7, squash=1.0)
        self.ui["cam"] = (0, 0, 1.0)

    def ui_road(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("stat") - 0.15:
            self.label(540 + 17 * 1.2, 1230 - 1.2 * (170 + 57 + 232), 820, 600, "cams", T["cameras"] - 0.1, T["battery"] - 0.1, CYAN, size=34)
            self.label(540, 1230 - 1.2 * (105 + 232), 270, 640, "battery", T["battery"], T["run"] + 0.3, GOOD, size=34)
            self.chip(540, 470, "marathon", T["run"] + 0.2, s("stat") - 0.15, accent=LAMP, size=42)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8), (T["flip0"], servo(0.3, 500.0, 1100.0, 61), -10),
              (T["flip0"] + 0.2, sfx.whoosh(0.8, False, 62), -8), (T["flip0"] + 1.15, sfx.thud(0.4, 63), -6),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 64), -9), (T["humanoid"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 65), -4), (T["tip1"], sfx.creak(0.8, 66), -10),
               (T["tip1"] + 0.6, sfx.thud(0.5, 67), -4), (T["tip1"] + 0.65, sfx.clank(300.0, 0.5, 68), -8),
               (T["tip1"] + 0.9, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -5), (T["inner"], sfx.charge_up(0.6), -12)]
        ev += [(T["motors"] + 0.12 * i, servo(0.12, 700.0 + 60 * i, 900.0 + 60 * i, 70 + i), -16) for i in range(8)]
        ev += [(T["hundreds"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 80), -4), (T["lift2"], servo(0.3, 600.0, 900.0, 81), -10),
               (T["fall2"] + 0.5, sfx.thud(0.5, 82), -4), (T["fall2"] + 0.55, sfx.clank(280.0, 0.5, 83), -8),
               (T["fall2"] + 0.8, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 84), -5)]
        ev += [(T["shift"] + 0.5 + 1.5 * i, sfx.tap(85 + i), -8) for i in range(3)]
        ev += [(T["like"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 90), -4)]
        ev += [(s("break3") + 0.37 * i, sfx.tap(91 + i), -12) for i in range(6)]
        ev += [(T["push3"], sfx.thunk(97), -6), (T["push3"] + 0.75, sfx.thud(0.5, 98), -4),
               (T["push3"] + 0.8, sfx.clank(260.0, 0.5, 99), -8), (T["push3"] + 1.0, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 100), -5), (T["thousands"], sfx.sparkle(1.0, 14, 101), -10),
               (T["years"], sfx.riser(1.2, 102), -12), (T["brain"] - 0.4, sfx.whoosh(0.5, False, 103), -10),
               (T["brain"], sfx.pop(104), -6), (T["brain"] + 0.2, sfx.thunk(105), -8), (T["brain"] + 0.5, sfx.tap(106), -8),
               (T["brain"] + 0.7, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 107), -4), (T["egg"] + 0.1, servo(0.5, 500.0, 800.0, 108), -12),
               (T["crush4"], crack_snd(0.5, 109), -4), (T["crush4"] + 0.05, sfx.thud(0.3, 110), -10),
               (T["crush4"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 111), -5), (T["touch"], sfx.charge_up(0.5), -12),
               (T["fingertips"], servo(0.5, 500.0, 760.0, 112), -12), (T["feels"], sfx.beep(1300.0, 0.08), -14),
               (T["squeezes"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(113), 0), (T["follow"] - 0.15, sfx.pop(114), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.4, True, 115), -6), (T["cameras"], sfx.beep(1700.0, 0.1), -10),
               (T["cameras"] + 0.15, sfx.beep(2100.0, 0.1), -10), (T["battery"], sfx.charge_up(0.8), -10),
               (T["run"], crowd(2.5, 116), -10), (T["run"] + 0.3, sfx.ding(), -10)]
        ev += [(T["s1"], sfx.pop(117), -3), (T["s2"], sfx.pop(118), -3), (T["s3"], sfx.pop(119), -3)]
        ev += [(T["cong2"], sfx.pop(120), -2), (T["cong2"], sfx.sparkle(1.0, 14, 121), -4), (T["cong2"] + 0.1, crowd(1.8, 122), -10),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 123), -6)]
        if self.rtl:
            ev += [(T["fold"], sfx.pop(124), -8), (T["t_end"], sfx.power_down(1.0, 125), -6)]
        else:
            ev += [(s("tag") + 0.2, sfx.whoosh(0.6, False, 126), -12),
                   (T["t_end"], sfx.womp(), -8), (T["t_end"] + 0.3, sfx.alarm(2, 600.0), -14)]
        return ev


NAME = "humanoid"
EPISODE = Humanoid
