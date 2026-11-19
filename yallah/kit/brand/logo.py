"""Yallah Say logos (profile pictures), one layout in two colourways. Text is drawn as outlines, so the SVG needs no font.

usage: python3 logo.py            -> out/yallahsay-ma.svg, out/yallahsay-pa.svg (+ .png 1080) and out/preview.jpg
"""
import datetime, json, math, os, re, subprocess, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

D = '/home/claude/brand'
FONT = f'{D}/font/FredokaOne-Regular.ttf'
tt = TTFont(FONT); gs = tt.getGlyphSet(); upm = tt['head'].unitsPerEm
hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))
f = lambda n: round(n, 1)
INK, CREAM, MARK = '#2A1B14', '#FFFDF6', '#FFDA6B'


def text_path(text, size, x, y, anchor='start'):
    """outline of `text` (kerned) with its baseline start at x,y; returns (path d, (x0,y0,x1,y1), advance width)"""
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {'kern': True, 'liga': False})
    s = size / upm
    adv = sum(p.x_advance for p in buf.glyph_positions) * s
    x0 = x - (adv if anchor == 'end' else adv / 2 if anchor == 'middle' else 0)
    pen, bp, cx = SVGPathPen(gs, ntos=lambda v: str(f(v))), BoundsPen(gs), 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        g = gs[tt.getGlyphName(info.codepoint)]
        t = (s, 0, 0, -s, x0 + (cx + pos.x_offset) * s, y - pos.y_offset * s)
        g.draw(TransformPen(pen, t)); g.draw(TransformPen(bp, t))
        cx += pos.x_advance
    return pen.getCommands(), bp.bounds, adv


def star_pts(cx, cy, R, n, ratio, rot=0):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180 / n - 90)
        r = R if i % 2 == 0 else R * ratio
        pts.append(f'{f(cx + r * math.cos(a))},{f(cy + r * math.sin(a))}')
    return ' '.join(pts)


def pentagram(cx, cy, r):
    p = []
    for k in (0, 2, 4, 1, 3):
        a = math.radians(k * 72 - 90)
        p.append(f'{f(cx + r * math.cos(a))} {f(cy + r * math.sin(a))}')
    return 'M' + 'L'.join(p) + 'Z'


def sparkle(cx, cy, r, fill, op=1):
    k = r * 0.2
    return (f'<path d="M{cx} {cy - r}C{cx + k} {cy - k} {cx + k} {cy - k} {cx + r} {cy}C{cx + k} {cy + k} {cx + k} {cy + k} {cx} {cy + r}'
            f'C{cx - k} {cy + k} {cx - k} {cy + k} {cx - r} {cy}C{cx - k} {cy - k} {cx - k} {cy - k} {cx} {cy - r}Z" fill="{fill}" opacity="{op}"/>')


def pattern_ma(pid):
    """zellige: eight-pointed stars with small diamonds between them"""
    s = 216; h = s / 2
    st = lambda x, y, R, op: f'<polygon points="{star_pts(x, y, R, 8, 0.7654)}" fill="#fff" fill-opacity="{op}"/>'
    dia = lambda x, y, r, op: f'<polygon points="{x},{f(y - r)} {f(x + r)},{y} {x},{f(y + r)} {f(x - r)},{y}" fill="#fff" fill-opacity="{op}"/>'
    body = st(0, 0, 62, .1) + st(s, 0, 62, .1) + st(0, s, 62, .1) + st(s, s, 62, .1) + st(h, h, 62, .1)
    body += ''.join(f'<polygon points="{star_pts(x, y, 30, 8, 0.7654, 22.5)}" fill="#7E1016" fill-opacity=".28"/>' for x, y in ((0, 0), (s, 0), (0, s), (s, s), (h, h)))
    body += dia(h, 0, 20, .09) + dia(h, s, 20, .09) + dia(0, h, 20, .09) + dia(s, h, 20, .09)
    return f'<pattern id="{pid}" width="{s}" height="{s}" patternUnits="userSpaceOnUse" patternTransform="translate(-36 -36)">{body}</pattern>'


def pattern_pa(pid):
    """tatreez: cross-stitched eight-pointed stars with one stitch between every four"""
    ST = ['....#....', '...###...', '..#.#.#..', '.#.###.#.', '#.#####.#', '.#.###.#.', '..#.#.#..', '...###...', '....#....']
    s = 190; c = s / 10
    cell = lambda x, y, op: f'<rect x="{f(x * c + 1.5)}" y="{f(y * c + 1.5)}" width="{f(c - 3)}" height="{f(c - 3)}" fill="#fff" fill-opacity="{op}"/>'
    body = ''.join(cell(x, y, .17 if (x + y) % 2 else .1) for y, row in enumerate(ST) for x, ch in enumerate(row) if ch == '#')
    body += cell(9, 9, .14)
    return f'<pattern id="{pid}" width="{s}" height="{s}" patternUnits="userSpaceOnUse" patternTransform="translate(-30 -30)">{body}</pattern>'


def roundel_ma(cx, cy, r, cid):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#C1272D"/>'
            f'<path d="{pentagram(cx, cy + r * 0.04, r * 0.6)}" fill="none" stroke="#006233" stroke-width="{f(r * 0.12)}" stroke-linejoin="round"/>')


def roundel_pa(cx, cy, r, cid):
    x, y, w = cx - r, cy - r, 2 * r
    t = w / 3
    return (f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><g clip-path="url(#{cid})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{f(t + 1)}" fill="#000"/><rect x="{x}" y="{f(y + t)}" width="{w}" height="{f(t + 1)}" fill="#fff"/>'
            f'<rect x="{x}" y="{f(y + 2 * t)}" width="{w}" height="{f(t)}" fill="#007A3D"/>'
            f'<path d="M{x} {y}L{f(x + w * 0.5)} {cy}L{x} {f(y + w)}Z" fill="#CE1126"/></g>')


THEMES = {
    'ma': dict(bg=('#DB3A40', '#B01E25'), deep='#7E1016', pattern=pattern_ma, roundel=roundel_ma, title='Yallah Say Morocco', label='Yallah Say logo with the flag of Morocco', file='Main.dc.html'),
    'pa': dict(bg=('#1F9552', '#0B5E32'), deep='#063D20', pattern=pattern_pa, roundel=roundel_pa, title='Yallah Say Palestine', label='Yallah Say logo with the flag of Palestine', file='Palestine.dc.html'),
}


def parts(key):
    """(defs, body) of one logo; ids carry the key so two logos can share a document"""
    T = THEMES[key]; p = 'ys' + key
    bx, by, bw, bh, br = 118, 196, 844, 566, 150            # the speech bubble
    yb = by + bh
    bubble = (f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{br}"/>'
              f'<path d="M296 {yb - 6}C298 {yb + 58} 280 {yb + 100} 232 {yb + 132}C330 {yb + 128} 418 {yb + 84} 452 {yb - 6}Z" stroke-width="12" stroke-linejoin="round"/>')
    # wordmark: two lines of equal width.  line 1 "Yallah", line 2 "Say" on the caption highlight + the flag
    size, W = 100, 610
    _, b1, _ = text_path('Yallah', size, 0, 0)
    size = size * W / (b1[2] - b1[0])                       # line 1 fills the block width
    d1, b1, _ = text_path('Yallah', size, 0, 0)
    x0 = 540 - W / 2 - b1[0]
    cap = -text_path('Y', size, 0, 0)[1][1]                 # cap height
    _, bs, _ = text_path('Say', size, 0, 0)
    desc = bs[3]                                            # depth of the y below the baseline
    gap, pad = 86, 30
    block_h = cap + gap + cap + desc + pad                  # line1 caps, gap, line2 caps, descender, pill padding
    base1 = by + (bh - block_h) / 2 + cap + 4
    base2 = base1 + gap + cap
    d1, b1, _ = text_path('Yallah', size, x0, base1)
    px0 = 540 - W / 2                                       # pill left edge
    d2, b2, _ = text_path('Say', size, px0 + pad - bs[0], base2)
    pill = (px0, base2 - cap - pad, (b2[2] - b2[0]) + 2 * pad, cap + desc + 2 * pad)
    r = (540 + W / 2 - (pill[0] + pill[2]) - 34) / 2        # the flag takes the rest of the line
    r = min(r, pill[3] / 2 - 4)
    fx, fy = 540 + W / 2 - r, pill[1] + pill[3] / 2
    defs = (f'<linearGradient id="{p}bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg"][0]}"/><stop offset="1" stop-color="{T["bg"][1]}"/></linearGradient>'
            f'<radialGradient id="{p}glow" cx=".5" cy=".42" r=".62"><stop offset="0" stop-color="#fff" stop-opacity=".2"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            + T['pattern'](p + 'pt'))
    body = (f'<rect width="1080" height="1080" fill="url(#{p}bg)"/><rect width="1080" height="1080" fill="url(#{p}pt)"/><rect width="1080" height="1080" fill="url(#{p}glow)"/>'
            f'<g fill="{T["deep"]}" stroke="{T["deep"]}" opacity=".55" transform="translate(0 20)">{bubble}</g>'
            f'<g fill="{CREAM}" stroke="{CREAM}">{bubble}</g>'
            f'<path d="{d1}" fill="{INK}"/>'
            f'<rect x="{f(pill[0])}" y="{f(pill[1])}" width="{f(pill[2])}" height="{f(pill[3])}" rx="34" fill="{MARK}"/>'
            f'<path d="{d2}" fill="{INK}"/>'
            f'<circle cx="{f(fx)}" cy="{f(fy + 5)}" r="{f(r + 5)}" fill="{INK}" opacity=".16"/>'
            + T['roundel'](f(fx), f(fy), f(r), p + 'cp') +
            f'<circle cx="{f(fx)}" cy="{f(fy)}" r="{f(r)}" fill="none" stroke="{INK}" stroke-width="7"/>'
            + sparkle(706, 902, 50, MARK) + sparkle(790, 846, 24, '#fff', .9) + sparkle(318, 116, 30, '#fff', .9) + sparkle(776, 112, 22, MARK))
    return defs, body


def closed(svg):
    """every element gets an explicit closing tag (the canvas format wants none self-closed)"""
    return re.sub(r'<(\w+)([^<>]*?)/>', r'<\1\2></\1>', svg)


def logo(key):
    T = THEMES[key]; defs, body = parts(key)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080" role="img" aria-label="{T["label"]}">'
            f'<defs>{defs}</defs>{body}</svg>')


def artboard(key):
    """one canvas artboard (.dc.html): the logo as inline SVG in a fixed 1080 x 1080 root"""
    T = THEMES[key]; defs, body = parts(key)
    svg = closed(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080" role="img" aria-label="{T["label"]}" style="display: block">'
                 f'<defs>{defs}</defs>{body}</svg>')
    assert '{' not in svg and '/>' not in svg
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{T["title"]}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<style>
body{{margin:0}}
</style>
</helmet>
<div style="width: 1080px; height: 1080px; overflow: hidden; background: {T["bg"][1]}">
{svg}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1080,"height":1080}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''


def write_board(key, with_index=False):
    root = f'{D}/canvas/project'; os.makedirs(root, exist_ok=True)
    if with_index:
        boards, x = {}, 0
        for k, T in THEMES.items():
            boards[T['file']] = {'x': x, 'y': 0, 'w': 1080, 'h': 1080, 'title': T['title']}; x += 1160
        idx = {'v': 3, 'createdOnFiles': {'v': 1, 'at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
               'title': 'Yallah Say logos', 'launch': {'view': 'canvas'}, 'pages': [], 'boards': boards,
               'order': [T['file'] for T in THEMES.values()], 'notes': {}, 'designSystems': []}
        open(f'{root}/canvas.json', 'w').write(json.dumps(idx, indent=1))
    open(f'{root}/{THEMES[key]["file"]}', 'w').write(artboard(key))
    print('wrote', THEMES[key]['file'], os.path.getsize(f'{root}/{THEMES[key]["file"]}'), 'bytes')


if __name__ == '__main__':
    if sys.argv[1:2] == ['board']:
        write_board(sys.argv[2], with_index='index' in sys.argv); sys.exit()
    from PIL import Image, ImageDraw
    for k in THEMES:
        open(f'{D}/out/yallahsay-{k}.svg', 'w').write(logo(k))
        subprocess.run(['rsvg-convert', '-w', '1080', '-h', '1080', f'{D}/out/yallahsay-{k}.svg', '-o', f'{D}/out/yallahsay-{k}.png'], check=True)
    # preview: the full square, then the circle crop at profile and feed sizes on light and on dark
    sheet = Image.new('RGB', (1500, 1160), '#F2F2F2'); dr = ImageDraw.Draw(sheet)
    dr.rectangle([950, 0, 1500, 1160], fill='#121212')
    for i, k in enumerate(THEMES):
        im = Image.open(f'{D}/out/yallahsay-{k}.png').convert('RGB')
        y = 20 + i * 570
        sheet.paste(im.resize((540, 540), Image.LANCZOS), (20, y))
        mask = Image.new('L', (1080, 1080), 0); ImageDraw.Draw(mask).ellipse([0, 0, 1079, 1079], fill=255)
        circ = im.copy(); circ.putalpha(mask)
        def row(x, yy, sizes):
            for sz in sizes:
                c = circ.resize((sz, sz), Image.LANCZOS); sheet.paste(c, (x, yy), c); x += sz + 14
        row(580, y, (320,)); row(580, y + 350, (150, 96, 48, 32))
        row(1060, y, (320,)); row(1000, y + 350, (150, 96, 48, 32))
    sheet.save(f'{D}/out/preview.jpg', quality=92)
    print('ok')
