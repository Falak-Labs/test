"""Make the page folder of one episode in one dialect from the kit.   usage: python3 mkpage.py <ma|pa> <page_dir>"""
import os, shutil, sys
from PIL import Image

KIT = '/home/claude/video/kit2'
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
Image.open(f'/home/claude/brand/out/yallahsay-{theme}.png').convert('RGB').resize((288, 288), Image.LANCZOS).save(f'{page}/logo.png')
print('page', page, 'theme', theme)
