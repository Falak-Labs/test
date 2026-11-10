"""Frame loop -> H.264 segments -> concat -> mux. Plus still frames for checking."""
import multiprocessing as mp
import os
import subprocess
import skia

W, H, FPS = 1080, 1920, 30
_SCENE = None


def _encode_range(f0, f1, out_path):
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    tmp = out_path[:-4] + ".part.mp4"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", os.environ.get("BIK_PRESET", "veryfast"), "-crf", os.environ.get("BIK_CRF", "18"),
           "-pix_fmt", "yuv420p", "-threads", "2", tmp]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        c.save()
        _SCENE.draw(c, f / FPS)
        c.restore()
        proc.stdin.write(surf.makeImageSnapshot().tobytes())
    proc.stdin.close()
    if proc.wait() == 0:
        os.replace(tmp, out_path)
    return out_path


def render(scene, duration, out_mp4, workdir, segments=8, workers=2):
    global _SCENE
    _SCENE = scene
    os.makedirs(workdir, exist_ok=True)
    frames = int(round(duration * FPS))
    bounds = [round(frames * i / segments) for i in range(segments + 1)]
    jobs = [(bounds[i], bounds[i + 1], os.path.join(workdir, f"seg{i:02d}.mp4")) for i in range(segments)]
    with mp.get_context("fork").Pool(workers) as pool:
        outs = pool.starmap(_encode_range, jobs)
    lst = os.path.join(workdir, "list.txt")
    with open(lst, "w") as fh:
        for o in outs:
            fh.write(f"file '{os.path.abspath(o)}'\n")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c", "copy", out_mp4], check=True)
    return out_mp4


def mux(video, audio, out):
    tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video, "-i", audio,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
    return out


def still(scene, t, path):
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    scene.draw(c, t)
    surf.makeImageSnapshot().save(path, skia.kPNG)
    return path


def contact_sheet(paths, labels, out, cols=4, scale=0.3):
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert("RGB") for p in paths]
    w, h = int(W * scale), int(H * scale)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * (h + 28)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(ims, labels)):
        x, y = (i % cols) * w, (i // cols) * (h + 28)
        sheet.paste(im.resize((w, h)), (x, y + 28))
        d.text((x + 6, y + 6), lab, fill="black")
    sheet.save(out)
    return out
