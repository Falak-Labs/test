"""Local preview harness that drives the page the same way the remote renderer does.

usage:
  shoot.py stills <page_dir> <out_dir> t1 t2 ...        -> one JPEG per time
  shoot.py video  <page_dir> <out.mp4> [start] [dur]    -> silent mp4 (30 fps)
  shoot.py grid   <page_dir> <out.txt> t1 t2 ...        -> 9x16 mean-colour grid per time (parity check)
"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

SEEK = "t => window.renderFrame(t)"
FPS = 30


def open_page(p, page_dir):
    browser = p.chromium.launch(args=["--disable-dev-shm-usage"])
    page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    logs = []
    page.on("console", lambda m: logs.append(f"[{m.type}] {m.text}"))
    page.on("pageerror", lambda e: logs.append(f"[pageerror] {e}"))
    page.clock.install(time=0)
    page.goto((Path(page_dir) / "index.html").resolve().as_uri())
    try:
        page.evaluate("async () => { await document.fonts.ready; await window.RENDER_READY; }")
    finally:
        for line in logs:
            print(line)
    return browser, page


def main():
    mode, page_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rest = sys.argv[4:]
    started = time.monotonic()
    with sync_playwright() as p:
        browser, page = open_page(p, page_dir)
        if mode == "stills":
            Path(out).mkdir(parents=True, exist_ok=True)
            for t in rest:
                page.evaluate(SEEK, float(t))
                page.screenshot(path=str(Path(out) / f"t{float(t):06.2f}.jpg"), type="jpeg", quality=92)
        elif mode == "grid":
            from io import BytesIO
            from PIL import Image
            rows = []
            for t in rest:
                page.evaluate(SEEK, float(t))
                im = Image.open(BytesIO(page.screenshot(type="png"))).convert("RGB").resize((9, 16), Image.BOX)
                rows.append(f"{float(t):.2f} " + im.tobytes().hex())
            Path(out).write_text("\n".join(rows) + "\n")
        else:
            start = float(rest[0]) if rest else 0.0
            dur = float(rest[1]) if len(rest) > 1 else page.evaluate("window.RENDER_DURATION") - start
            frames = round(dur * FPS)
            tmp = Path(out).with_suffix(".part.mp4")
            ff = subprocess.Popen(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
                 "-movflags", "+faststart", str(tmp)], stdin=subprocess.PIPE)
            for i in range(frames):
                page.evaluate(SEEK, start + i / FPS)
                ff.stdin.write(page.screenshot(type="jpeg", quality=92))
            ff.stdin.close()
            if ff.wait() == 0:
                tmp.rename(out)
            print(f"{frames} frames in {time.monotonic() - started:.1f}s -> {out}")
        browser.close()


if __name__ == "__main__":
    main()
