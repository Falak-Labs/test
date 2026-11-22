"""Add a Fluent Emoji picture to the kit, so a phrase can use it as its sticker ("icon": "fe:<slug>").

usage: python3 sticker.py <slug> "<path under assets/ in github.com/microsoft/fluentui-emoji>"
   e.g. python3 sticker.py house "House with garden/3D/house_with_garden_3d.png"

Saves the 256 px picture as ../stickers/<slug>.png and notes where it came from in ../stickers/SOURCES.md.
Fluent Emoji is Microsoft's, under the MIT licence (../stickers/LICENSE-FluentEmoji.txt)."""
import os, re, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "stickers")
slug, src = sys.argv[1:3]
assert re.fullmatch(r"[a-z0-9_]+", slug), "slug: small letters, digits and _"
url = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/" + urllib.parse.quote(src)
data = urllib.request.urlopen(url, timeout=60).read()
assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG: " + url
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, slug + ".png"), "wb").write(data)
notes = os.path.join(OUT, "SOURCES.md")
rows = [l for l in (open(notes, encoding="utf-8").read().splitlines() if os.path.exists(notes) else []) if l.startswith("| ") and not l.startswith(f"| {slug} |") and not l.startswith("| slug") and not l.startswith("| ---")]
rows.append(f"| {slug} | assets/{src} |")
open(notes, "w", encoding="utf-8").write("# Stickers from Fluent Emoji\n\nMicrosoft Fluent Emoji, MIT licence (LICENSE-FluentEmoji.txt), from github.com/microsoft/fluentui-emoji.\n\n| slug | source |\n| --- | --- |\n" + "\n".join(sorted(rows)) + "\n")
print(slug, len(data), "bytes")
