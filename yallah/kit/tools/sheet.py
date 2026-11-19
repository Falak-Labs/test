"""sheet.py <out.jpg> <cols> <cell_w> <img...>  -> contact sheet of frames (keeps aspect)"""
import sys
from PIL import Image
out, cols, cw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
files = sys.argv[4:]
ims = [Image.open(f).convert("RGB") for f in files]
ch = round(cw * ims[0].height / ims[0].width)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw + (cols + 1) * 6, rows * ch + (rows + 1) * 6), (20, 20, 24))
for i, im in enumerate(ims):
    sheet.paste(im.resize((cw, ch), Image.LANCZOS), (6 + (i % cols) * (cw + 6), 6 + (i // cols) * (ch + 6)))
sheet.save(out, quality=88)
print(out, sheet.size)
