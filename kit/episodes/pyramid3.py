"""SAMPLE (Nov 18 2026), not a production episode: the opening of build 36 (hook, break1, fix1) in the proposed look 3.

Same script, timing, captions and HUD as pyramid.py; what changes is the picture:
  * golden-hour light: a low sun with god rays, a cool blue sky, warm haze on the horizon, wispy lit clouds;
  * texture: sand grain and wind ripples, stone blotches on the blocks, fields with rows;
  * shadows and depth: the pyramid casts a long soft shadow, contact shadows under people and the sledge, hazier far
    layers, rim-lit palms, a Nile that reflects the sky and glitters under the sun;
  * the look-3 finishing pass (v2.Post3): film grade, warm halation, dust in the air, a slow breathing camera.
"""
from pyramid import *  # noqa: F401,F403
from pyramid import _tri  # noqa: F401

GOLD = {"top": "#0B1630", "upper": "#1F3A60", "mid": "#7A6378", "low": "#E0975E", "horizon": "#FFD08A",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
HAZE = "#F6C489"
SAND3 = ("#BE8752", "#97653A", "#684123", "#2E1C0E")


def pyramid3(c, x, y, s, t, built=1.0, casing=0.0, glint=-1.0, a=1.0, glow=0.0, haze=0.0):
    """The Great Pyramid in golden-hour light: warm sunlit left face, cool right face, stone texture, courses, a lit
    ridge, soft darkening at the base. haze 0..1 fades it into the horizon (far pyramids)."""
    if a <= 0 or built <= 0:
        return
    A, L, F, Rr = faces(x, y, s)
    left, right = _tri(A, L, F), _tri(A, F, Rr)
    c.save()
    top = y - PH * s * built
    c.clipRect(R(x - 2000, top, 4000, 3000))
    lit = mix("#CF9356", "#E6D8BD", casing)
    cool = mix("#5B4256", "#8E86A0", casing)
    c.drawPath(left, lin_paint(L[0], L[1], A[0], A[1], [shade(lit, -0.10), lit, shade(lit, 0.16)], [0.0, 0.55, 1.0], a=a))
    c.drawPath(right, lin_paint(F[0], 0, Rr[0], 0, [shade(cool, 0.06), cool, shade(cool, -0.22)], [0.0, 0.5, 1.0], a=a))
    for face, k in ((left, 0.42), (right, 0.36)):
        tex(c, face, "stone", scale=0.9 * s, a=a * k * (1 - 0.55 * casing))
    n = 34
    for k in range(1, n):
        q = k / float(n)
        yl, xl = lerp(L[1], A[1], q), lerp(L[0], A[0], q)
        xf, yf = lerp(F[0], A[0], q), lerp(F[1], A[1], q)
        xr, yr = lerp(Rr[0], A[0], q), lerp(Rr[1], A[1], q)
        c.drawLine(xl, yl, xf, yf, P("#7A4A26", a * (0.42 - 0.36 * casing), stroke=2.0 * s))
        c.drawLine(xf, yf, xr, yr, P("#2B1E34", a * (0.42 - 0.36 * casing), stroke=2.0 * s))
        for j in range(1, 7):
            u = (j + 0.5 * (k % 2)) / 7.0
            if u < 1:
                jx, jy = lerp(xl, xf, u), lerp(yl, yf, u)
                c.drawLine(jx, jy, jx, jy + 18 * s, P("#7A4A26", 0.28 * a * (1 - casing), stroke=1.4 * s))
    base = skia.Path()                                                  # darker near the sand (bounce light is low)
    base.moveTo(*L)
    base.lineTo(*F)
    base.lineTo(*Rr)
    base.lineTo(Rr[0], Rr[1] - 120 * s)
    base.lineTo(F[0], F[1] - 120 * s)
    base.lineTo(L[0], L[1] - 120 * s)
    base.close()
    for face in (left, right):
        c.save()
        c.clipPath(face, doAntiAlias=True)
        c.drawPath(base, lin_paint(0, y + 30 * s, 0, y - 140 * s, [("#1B1020", 0.45 * a), ("#1B1020", 0.0)]))
        c.restore()
    rim = P("#FFF1D6", 0.55 * a, stroke=3.2 * s, blur=1.5)               # the sunlit ridge
    c.drawLine(A[0], A[1], F[0], F[1], rim)
    c.drawLine(A[0], A[1], L[0], L[1], P("#FFE2B0", 0.35 * a, stroke=2.4 * s, blur=1.5))
    if glint > -0.5:
        band = skia.Path()
        gx = lerp(L[0] - 300 * s, Rr[0] + 300 * s, glint)
        band.moveTo(gx - 60 * s, y + 60 * s)
        band.lineTo(gx + 40 * s, y + 60 * s)
        band.lineTo(gx + 340 * s, y - PH * s - 60 * s)
        band.lineTo(gx + 240 * s, y - PH * s - 60 * s)
        band.close()
        c.save()
        c.clipPath(left, doAntiAlias=True)
        c.drawPath(band, P("#FFFFFF", 0.42 * a * casing, blur=12))
        c.restore()
    if haze > 0:
        for face in (left, right):
            c.drawPath(face, P(HAZE, clamp(haze) * a))
    c.restore()
    if casing > 0.5:
        add_glow(c, A[0], A[1] + 40 * s, 140 * s, "#FFF3D6", 0.18 * (casing - 0.5) * 2 * a)
    if glow > 0:
        add_glow(c, x, y - PH * s * 0.5, 700 * s, "#FDE68A", 0.1 * glow * a)
    if built < 1:                                                        # blocks being set on the top course
        for i in range(3):
            q = (t * 1.4 + i / 3.0) % 1.0
            bx = lerp(x - PW * s * (1 - built) * 0.9, x + PW * s * (1 - built) * 0.5, (i + 0.5) / 3.0)
            by = top - 18 * s * (1 - q)
            c.drawRect(R(bx - 14 * s, by - 16 * s, 28 * s, 16 * s), P("#F0C890", a * (1 - q * 0.3)))
            c.drawRect(R(bx - 14 * s, by - 3 * s, 28 * s, 3 * s), P("#5A3A20", 0.5 * a * (1 - q * 0.3)))


def pyramid_shadow(c, x, y, s, built=1.0, a=1.0, length=1.15):
    """Long soft shadow of the pyramid on the sand, thrown to the right and toward us by the low sun on the left."""
    A, L, F, Rr = faces(x, y, s)
    h = PH * s * built
    tip = (x + 0.95 * h * length, y + 0.30 * h * length)
    soft_shadow(c, [L, F, tip, Rr], a=0.5 * a, blur=22 * s, col="#3A2340")
    soft_shadow(c, [(L[0] + 40 * s, L[1]), F, (F[0] + 260 * s, F[1] + 40 * s), Rr], a=0.25 * a, blur=10 * s, col="#24162E")


def palm3(c, x, y, h, sway=0.0, a=1.0, rim="#FFB866"):
    """Back-lit palm: dark trunk and fronds with a warm rim on the sun side."""
    for dx, dy, col, al, wid in ((-3.5, -2.5, rim, 0.75, 1.0), (0, 0, "#1E1712", 1.0, 1.0)):
        c.save()
        c.translate(x + dx, y + dy)
        tr = skia.Path()
        tr.moveTo(-8, 0)
        tr.quadTo(10 + sway * 10, -h * 0.5, 6 + sway * 20, -h)
        tr.lineTo(14 + sway * 20, -h)
        tr.quadTo(18 + sway * 10, -h * 0.5, 8, 0)
        tr.close()
        c.drawPath(tr, P(col if dx else "#2A1D14", a * al))
        tx, ty = 10 + sway * 20, -h
        for k in range(9):
            an = math.radians(-178 + k * 24.5 + sway * 6)
            ex, ey = tx + math.cos(an) * h * 0.46, ty + math.sin(an) * h * 0.24 + h * 0.15
            mx_, my_ = (tx + ex) / 2, ty - h * 0.16
            nx, ny = -(ey - ty), (ex - tx)
            ln = math.hypot(nx, ny) or 1.0
            nx, ny = nx / ln * h * 0.07, ny / ln * h * 0.07
            lf = skia.Path()
            lf.moveTo(tx, ty)
            lf.quadTo(mx_ + nx, my_ + ny, ex, ey)
            lf.quadTo(mx_ - nx * 0.25, my_ - ny * 0.25, tx, ty)
            lf.close()
            c.drawPath(lf, P(col if dx else "#162019", a * al))
        c.restore()


class Pyramid3(Pyramid):
    """Build 36 opening in look 3 (sample)."""
    LOOK = 3

    def __init__(self, vo_json, vo_wav, lang="en"):
        super().__init__(vo_json, vo_wav, lang)
        rng = random.Random(3)
        self.wisps = [(rng.uniform(-200, 1300), rng.uniform(140, 520), rng.uniform(260, 620), rng.uniform(16, 34),
                       rng.uniform(0.35, 0.8)) for _ in range(9)]

    # ------------------------------------------------------------------ background and foreground
    def plateau(self, c, t, cam, nile=True):
        """Golden-hour sky, sun, wispy clouds, hazy far dunes and pyramids, textured sand (screen + world)."""
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=gy - 40 * z)
        for wx, wy, ww, wh, wa in self.wisps:                           # thin clouds lit from below
            xx = (wx + t * 9 - cx * 0.03) % 1500 - 200
            yy = wy * (gy / 1224.0)
            c.drawOval(R(xx - ww / 2, yy - wh / 2 + 6, ww, wh), P("#FFB37A", 0.30 * wa, blur=10))
            c.drawOval(R(xx - ww / 2, yy - wh / 2, ww, wh * 0.8), P("#8E6E86", 0.40 * wa, blur=8))
        sx, sy = 250 - cx * 0.05, gy - 470 * z
        add_glow(c, sx, sy, 420, "#FF9F55", 0.32)
        add_glow(c, sx, sy, 150, "#FFE2A8", 0.40)
        c.drawCircle(sx, sy, 44, rad_paint(sx, sy, 44, ["#FFFBEA", "#FFEBC0", "#FFC978"], [0.0, 0.7, 1.0]))
        self.post.light, self.post.rays, self.post.dust = (sx, sy), 0.7, 0.8
        self.view(c, cam)
        for (dx, hgt) in self.dunes:                                    # far dunes in the haze
            c.drawOval(R(dx - 520, -hgt * 0.5 - 34, 1040, hgt), lin_paint(0, -hgt - 34, 0, -20,
                                                                           ["#D9A07A", "#B97A5A"], a=0.95))
        c.drawRect(R(cx - 1300 / z, -260, 2600 / z, 240), lin_paint(0, -260, 0, -20, [(HAZE, 0.0), (HAZE, 0.35)]))
        pyramid3(c, -1050, -40, 0.42, t, haze=0.42)                      # Khafre and Menkaure behind
        pyramid3(c, 1050, -30, 0.3, t, haze=0.5)
        ground = R(cx - 1300 / z, -40, 2600 / z, 3000)
        c.drawRect(ground, lin_paint(0, -40, 0, 900, [shade(SAND3[0], 0.08), SAND3[0], SAND3[1], SAND3[2], SAND3[3]],
                                     [0.0, 0.05, 0.22, 0.55, 1.0]))
        tex(c, ground, "sand", scale=1.6, a=0.5, sy=0.75)
        c.drawRect(R(cx - 1300 / z, -40, 2600 / z, 120), lin_paint(0, -40, 0, 80, [(HAZE, 0.35), (HAZE, 0.0)]))
        return gy

    def foreground(self, c, t, cam):
        """The Nile reflecting the sky with a sun glitter, rim-lit palms, textured fields (world space)."""
        cx, cy, z = cam
        sxw = (250 - cx * 0.05 - W / 2) / z + cx                       # the sun's x in world units
        water = R(cx - 1300 / z, 300, 2600 / z, 160)
        c.drawRect(water, lin_paint(0, 300, 0, 460, ["#F2C28E", "#9A8A9E", "#2F5D7E", "#163B57"], [0.0, 0.25, 0.6, 1.0]))
        rng = random.Random(9)
        for i in range(70):                                             # glitter, strongest under the sun
            gx = rng.uniform(cx - 700 / z, cx + 700 / z)
            gy_ = rng.uniform(306, 452)
            near = math.exp(-abs(gx - sxw) / 260.0)
            tw = 0.5 + 0.5 * math.sin(t * rng.uniform(3, 7) + i)
            p = P("#FFE7B8", (0.15 + 0.8 * near) * tw, stroke=rng.uniform(2, 4))
            p.setBlendMode(PLUS)
            ln = rng.uniform(14, 46) * (0.6 + near)
            gx += math.sin(t * 0.8 + i) * 6
            c.drawLine(gx - ln / 2, gy_, gx + ln / 2, gy_, p)
        c.drawRect(R(cx - 1300 / z, 296, 2600 / z, 8), P("#3A2A1C", 0.5, blur=3))
        for i in range(9):
            xx = -1100 + i * 280 + 40 * math.sin(i * 2.1)
            contact_shadow(c, xx + 30, 302, 120, a=0.35)
            palm3(c, xx, 300, 230 + 40 * (i % 3), sway=math.sin(t * 1.3 + i) * 0.4)
        fields = R(cx - 1300 / z, 460, 2600 / z, 3000)
        c.drawRect(fields, lin_paint(0, 460, 0, 1100, ["#2E5A2A", "#1D4220", "#0E2412", "#050D07"]))
        tex(c, fields, "grain", scale=1.3, a=0.5)
        for k in range(1, 9):                                           # field rows
            yy = 460 + k * k * 9
            c.drawLine(cx - 1300 / z, yy, cx + 1300 / z, yy, P("#0A1A0C", 0.35, stroke=2 + k * 0.6))

    # ------------------------------------------------------------------ set: giza (hook)
    def draw_giza(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        self.plateau(c, t, cam)
        built = self.built.at(t) if t < s("break1") else 1.0
        cas = self.casing.at(t)
        gl = prog(t, T["shine"] + 0.2, T["shine"] + 1.6) if t < s("break1") else -1.0
        pyramid_shadow(c, 0, 0, 1.0, built=built)
        contact_shadow(c, 60, 10, 1300, a=0.35, h=60)
        pyramid3(c, 0, 0, 1.0, t, built=built, casing=cas, glint=gl)
        self.foreground(c, t, cam)
        c.restore()
        self.ui["cam"] = cam

    # ------------------------------------------------------------------ set: sledge (break1, fix1)
    def draw_sledge(self, c, t):
        T, s = self.T, self.tl.s
        cam = (180, -240, 0.98)
        self.plateau(c, t, cam, nile=False)
        self.post.rays, self.post.dust = 0.55, 0.9
        pyramid_shadow(c, 260, -160, 0.62, built=0.55, a=0.8)
        pyramid3(c, 260, -160, 0.62, t, built=0.55, haze=0.12)
        fixed = t >= s("fix1") - 0.12
        d = self.slide.at(t) if fixed else 0.0
        bx = 330 - d
        wet = prog(t, T["poured"] + 0.2, T["poured"] + 0.8) if fixed else 0.0
        c.drawOval(R(bx - 520, -18, 330, 36), P("#4A2C16", 0.8 * wet, blur=4))
        if wet > 0:
            sh = P("#FFE1B0", 0.25 * wet, stroke=3)
            sh.setBlendMode(PLUS)
            c.drawLine(bx - 480, -6, bx - 230, -6, sh)
        if not fixed:
            pk = prog(t, T["sledge"] - 0.3, T["digs"] + 0.2)
            pile = skia.Path()
            pile.moveTo(bx - 330, 0)
            pile.quadTo(bx - 250, -90 * pk, bx - 185, -30 * pk)
            pile.lineTo(bx - 185, 0)
            pile.close()
            c.drawPath(pile, lin_paint(0, -90, 0, 0, [SAND3[0], SAND3[1]]))
            tex(c, pile, "sand", scale=1.2, a=0.5)
            if pk > 0.2:                                                # sand spraying up as it digs in
                for i in range(14):
                    q = (t * 1.7 + i / 14.0) % 1.0
                    px = bx - 210 - q * 140 - (i % 3) * 12
                    py = -30 - 70 * math.sin(q * math.pi) - (i % 4) * 6
                    c.drawCircle(px, py, 3 + (i % 3), P("#E8C08A", 0.7 * (1 - q) * pk))
        if not fixed:
            ca = prog(t, T["car"] - 0.3, T["car"]) * (1 - prog(t, s("fix1") - 0.4, s("fix1") - 0.12))
            contact_shadow(c, bx + 250, -36, 200, a=0.45 * ca)
            small_car(c, bx + 250, -40, 0.55, a=ca)
        soft_shadow(c, [(bx - 190, 6), (bx + 190, 6), (bx + 330, 46), (bx - 60, 46)], a=0.45, blur=10)
        sledge(c, bx, 10 if not fixed else 0, 1.0)
        crew = 8
        sit = prog(t, T["half"] - 0.2, T["half"] + 0.3) if fixed else 0.0
        for i in range(crew):
            wx = bx - 420 - i * 92
            pulling = not (fixed and i % 2 == 1 and sit > 0.5)
            lean = (-18 if not fixed else -10) if pulling else 0
            soft_shadow(c, [(wx - 26, 4), (wx + 26, 4), (wx + 90, 30), (wx + 30, 30)], a=0.35, blur=6)
            if pulling:
                c.drawLine(bx - 190, -40, wx + 6, -100, P("#C8A165", 1, stroke=5))
                c.drawLine(bx - 190, -42, wx + 6, -102, P("#FFE2B0", 0.35, stroke=1.5))
            worker(c, wx, 0, 190, t + i * 0.3, pose="carry" if pulling else ("sit" if sit > 0.8 else "cheer"),
                   lean=lean + (math.sin(t * 9 + i) * 3 if not fixed else 0), face=-1)
        if fixed:
            mx = bx - 260
            soft_shadow(c, [(mx - 26, 4), (mx + 26, 4), (mx + 90, 30), (mx + 30, 30)], a=0.35, blur=6)
            worker(c, mx, 0, 190, t, pose="carry", face=-1)
            tilt = 70 * prog(t, T["poured"] - 0.2, T["poured"] + 0.2) * (1 - prog(t, T["firm"] + 0.6, T["firm"] + 1.0))
            jar(c, mx - 50, -120, 0.9, -tilt)
            if tilt > 30:
                for i in range(14):
                    q = (t * 2.5 + i / 14.0) % 1.0
                    px, py = mx - 110 - q * 40, -120 + q * 120
                    c.drawCircle(px, py, 7, P("#9CC9F5", 0.85))
                    hp = P("#FFFFFF", 0.6, stroke=2)
                    hp.setBlendMode(PLUS)
                    c.drawLine(px - 3, py - 3, px - 1, py - 5, hp)
        c.restore()
        self.ui["cam"] = cam
        self.ui["block"] = (bx, -280)


EPISODE = Pyramid3
NAME = "pyramid3"
