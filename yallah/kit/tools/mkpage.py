"""Make the page folder of one episode in one dialect from the kit.   usage: python3 mkpage.py <ma|pa> <page_dir>
The kit is ../page and the logos are ../brand, next to this file (YS_KIT and YS_BRAND point somewhere else)."""
import os, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.environ.get('YS_KIT') or os.path.join(HERE, '..', 'page')
BRAND = os.environ.get('YS_BRAND') or os.path.join(HERE, '..', 'brand')
theme, page = sys.argv[1:3]
os.makedirs(page, exist_ok=True)
for f in ('main.js', 'art2.js', 'art3.js'):
    shutil.copy(f'{KIT}/{f}', f'{page}/{f}')
shutil.copy(f'{KIT}/art-{theme}.js', f'{page}/art.js')
c = open(f'{KIT}/chars.js', encoding='utf-8').read()
if theme == 'pa':      # the Palestinian teacher: green dress with red embroidery, white scarf
    for a, b in [('#1A2F86', '#0F3B22'), ('#2F52CF', '#1F7A45'), ('#F0CB5E', '#D7262F'), ('#B8862A', '#7A0F16'), ('#F9E08A', '#F4B3B7'), ('#C4667A', '#BDB6A4'), ('#B85468', '#A9A190')]:
        assert a in c, a
        c = c.replace(a, b)
open(f'{page}/chars.js', 'w', encoding='utf-8').write(c)
html = open(f'{KIT}/index.html', encoding='utf-8').read().replace('__BG__', {'ma': '#1B3A9C', 'pa': '#0E6A38'}[theme])
open(f'{page}/index.html', 'w', encoding='utf-8').write(html)
Image.open(f'{BRAND}/yallahsay-{theme}.png').convert('RGB').resize((288, 288), Image.LANCZOS).save(f'{page}/logo.png')
# the Fluent Emoji stickers this lesson's phrases use ("icon": "fe:<slug>" in script.js, written before this runs)
script = f'{page}/script.js'
used = sorted(set(__import__('re').findall(r'"icon":"fe:([a-z0-9_]+)"', open(script, encoding='utf-8').read()))) if os.path.exists(script) else []
if os.path.isdir(f'{page}/stk'):
    shutil.rmtree(f'{page}/stk')
for slug in used:
    src = os.path.join(HERE, '..', 'stickers', slug + '.png')
    if not os.path.exists(src):
        sys.exit(f'sticker fe:{slug} is not in the kit: add it with kit/tools/sticker.py')
    os.makedirs(f'{page}/stk', exist_ok=True)
    shutil.copy(src, f'{page}/stk/{slug}.png')
print('page', page, 'theme', theme, *(['stickers', ' '.join(used)] if used else []))
