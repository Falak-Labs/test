"""AI video shots (Higgsfield, release "ai-media") inside a v2 episode: the shot is drawn as the world picture, so the
finishing pass, HUD, chips and captions stay on top of it exactly as on our own animation.

    from aishot import Shot
    self.shot = Shot("buildit-taipei-hook.mp4")          # fetched with gh release download (see HIGGSFIELD.md)
    self.shot.draw(c, t_local, length=4.2, a=1.0)        # t_local: seconds since the shot starts in the episode

Frames are cut once with ffmpeg to out/aishots/<name>/ (1080x1920, 30 fps, centre crop) and read one at a time.
If the shot is shorter than the time it covers it plays slower (length = the time it covers).
"""
import os
import subprocess

import skia

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30


def fetch(name, folder=None):
    """Path of an ai-media asset, downloaded with gh when it is not here yet."""
    folder = folder or os.path.join(KIT, "out", "aishots")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        subprocess.run(["python3", os.path.join(os.path.dirname(KIT), "scripts", "ai_media.py"), "get", name, folder],
                       check=True)
    return path


class Shot:
    def __init__(self, name, folder=None, start=0.0, end=None):
        """start / end: the part of the clip to use, in seconds (a multi-shot clip gives several Shots)."""
        src = fetch(name, folder)
        self.dir = os.path.join(os.path.dirname(src), os.path.splitext(name)[0] + "_frames")
        if not os.path.isdir(self.dir) or not os.listdir(self.dir):
            os.makedirs(self.dir, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf",
                            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                            "-q:v", "2", os.path.join(self.dir, "%04d.jpg")], check=True)
        total = len([f for f in os.listdir(self.dir) if f.endswith(".jpg")])
        self.first = min(total - 1, int(start * FPS))
        last = total if end is None else min(total, int(end * FPS))
        self.n = max(1, last - self.first)
        self.duration = self.n / FPS
        self._i, self._img = -1, None

    def image(self, t_local, length=None):
        k = self.duration / length if length and length > self.duration else 1.0
        i = max(0, min(self.n - 1, int(t_local * k * FPS)))
        if i != self._i:
            self._img = skia.Image.open(os.path.join(self.dir, f"{self.first + i + 1:04d}.jpg"))
            self._i = i
        return self._img

    def draw(self, c, t_local, length=None, a=1.0, shade=0.55):
        """Full-frame shot at opacity a, with a dark band behind the caption area (shade 0..1)."""
        img = self.image(t_local, length)
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(a)
        c.drawImageRect(img, skia.Rect(0, 0, W, H), skia.SamplingOptions(skia.FilterMode.kLinear), p)
        if shade > 0:
            g = skia.Paint(Shader=skia.GradientShader.MakeLinear(
                [(0, H * 0.52), (0, H * 0.82)],
                [skia.Color4f(0, 0, 0, 0).toColor(), skia.Color4f(0, 0, 0, shade * a).toColor()]))
            c.drawRect(skia.Rect(0, H * 0.52, W, H), g)
            top = skia.Paint(Shader=skia.GradientShader.MakeLinear(
                [(0, 0), (0, H * 0.2)],
                [skia.Color4f(0, 0, 0, 0.45 * a).toColor(), skia.Color4f(0, 0, 0, 0).toColor()]))
            c.drawRect(skia.Rect(0, 0, W, H * 0.2), top)
