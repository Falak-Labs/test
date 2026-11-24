"""Background library: seamless looping backgrounds in the reference style (dark radial gradient, vignette, slow dust,
film grain), in several palettes, for 9:16 shorts and 16:9 long videos. Everything is generated, so there is no licence
to track: use them anywhere (CapCut, Premiere, Remotion, HyperFrames).

usage: make_backgrounds.py out_dir [--seconds 12] [--fps 30]
Writes <palette>_9x16.mp4, <palette>_16x9.mp4 (seamless loops) and <palette>_9x16.png, <palette>_16x9.png (stills).
"""
import argparse, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PALETTES = {  # centre, mid, edge, dust
    "slate": ("#18212d", "#111a24", "#05090d", "#c8d3e0"),   # the reference
    "teal": ("#122a2c", "#0c1d20", "#040b0c", "#bfe0dc"),
    "maroon": ("#2a1618", "#1c0f11", "#080405", "#e8cfc8"),
    "indigo": ("#1a1a36", "#111127", "#05050d", "#cfd0f0"),
    "sand": ("#2a2216", "#1c170f", "#090705", "#efdcb8"),
    "night": ("#0f1620", "#0a0f16", "#030508", "#d6dde8"),
}
ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--seconds", type=float, default=12); ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--only", default="")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)


def hexrgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def gradient(w, h, c0, c1, c2, cy):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    rx, ry = w * 0.95, h * 0.62
    d = np.sqrt(((x - w / 2) / rx) ** 2 + ((y - cy) / ry) ** 2)
    d = np.clip(d, 0, 1)[..., None]
    t1 = np.clip(d / 0.45, 0, 1)
    t2 = np.clip((d - 0.45) / 0.55, 0, 1)
    col = np.where(d < 0.45, c0 + (c1 - c0) * t1, c1 + (c2 - c1) * t2)
    return col


rng = np.random.default_rng(5)
grain = [rng.normal(0, 1, (960, 540)).astype(np.float32) for _ in range(4)]
for name, (c0, c1, c2, dust) in PALETTES.items():
    if a.only and name not in a.only.split(","):
        continue
    for tag, (w, h) in {"9x16": (1080, 1920), "16x9": (1920, 1080)}.items():
        base = gradient(w, h, hexrgb(c0), hexrgb(c1), hexrgb(c2), h * (0.4 if h > w else 0.52))
        dcol = tuple(int(v) for v in hexrgb(dust))
        n = 70 if h > w else 80
        r_ = np.random.default_rng(len(name) * 7 + w)
        x0, y0 = r_.uniform(0, w, n), r_.uniform(0, h, n)
        ax, ay = r_.uniform(8, 30, n), r_.uniform(20, 70, n)     # orbit sizes (periodic => seamless loop)
        ph, tw = r_.uniform(0, 2 * np.pi, n), r_.integers(1, 4, n)  # twinkles per loop: whole numbers
        rad = r_.uniform(0.8, 2.4, n)
        frames = int(a.seconds * a.fps)
        # static grain baked into the gradient: stops banding, costs almost no bitrate (it never changes)
        g = np.asarray(Image.fromarray(grain[0]).resize((w, h), Image.NEAREST), np.float32)
        still = np.clip(base + g[..., None] * 1.4, 0, 255)
        still8 = still.astype(np.uint8)
        yy, xx = np.mgrid[-4:5, -4:5]
        mp4 = os.path.join(a.out, f"{name}_{tag}.mp4")
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                              "-r", str(a.fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                              "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
        dc = np.array(dcol, np.float32)
        for fi in range(frames):
            u = 2 * np.pi * fi / frames
            frame = still.copy()
            xs = x0 + ax * np.sin(u + ph)
            ys = (y0 - ay * np.cos(u + ph * 0.7)) % h
            ops = 0.15 + 0.85 * (0.5 + 0.5 * np.sin(u * tw + ph))
            for k in range(n):
                cx, cy = int(xs[k]) % w, int(ys[k])
                if cx < 5 or cy < 5 or cx > w - 6 or cy > h - 6:
                    continue
                spr = np.exp(-((xx - (xs[k] % 1)) ** 2 + (yy - (ys[k] % 1)) ** 2) / (2 * (rad[k] * 0.7) ** 2)) * ops[k] * 0.55
                sl = frame[cy - 4:cy + 5, cx - 4:cx + 5]
                sl += (dc - sl) * spr[..., None]
            p.stdin.write(frame.astype(np.uint8).tobytes())
            if fi == 0:
                Image.fromarray(frame.astype(np.uint8)).save(os.path.join(a.out, f"{name}_{tag}.png"))
        p.stdin.close(); p.wait()
        print(mp4, flush=True)
