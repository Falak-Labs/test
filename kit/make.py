"""Render one episode end to end: video, sound mix, final MP4, QA numbers and a check sheet.

usage:
  python3 make.py episodes/elevator.py /path/to/vo_prefix /path/to/out_dir [cover|video|audio|mux|qa ...] [lang=ar]
  (vo_prefix = the Phonon output without extension: prefix.wav + prefix.json)
  With no step names it runs all five in order. cover = out_dir/cover.png (v2 episodes), drawn as frame 0 of the
  video so the posts can use it as their cover; BIK_COVER=0 leaves it out.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import time

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
sys.path.insert(0, os.path.join(KIT, "episodes"))
from bik.render import render, mux, contact_sheet  # noqa: E402
from bik.mix import build_mix  # noqa: E402


def load(path):
    spec = importlib.util.spec_from_file_location("episode", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def qa(final, scene, out):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final],
                             capture_output=True, text=True).stdout)
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", final, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    i_lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1]
    peak = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)[-1]
    v = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate,nb_frames", "-of", "json", final],
                                  capture_output=True, text=True).stdout)["streams"][0]
    print(f"QA  duration {d:.2f}s  loudness {i_lufs} LUFS  true peak {peak} dBFS  "
          f"{v['width']}x{v['height']} @ {v['r_frame_rate']}  frames {v.get('nb_frames')}")
    # frames decoded from the final file at the middle of every beat
    shots, labels = [], []
    for lab in scene.tl.labels:
        t = (scene.tl.s(lab) + scene.tl.e(lab)) / 2
        pth = os.path.join(out, "qa", f"{lab}.png")
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", final,
                        "-frames:v", "1", pth], check=True)
        shots.append(pth)
        labels.append(f"{lab} {t:.1f}s")
    sheet = contact_sheet(shots, labels, os.path.join(out, "qa_sheet.png"), cols=5, scale=0.22)
    print("QA sheet", sheet)


def main():
    ep_path, vo, out = sys.argv[1:4]
    steps = [a for a in sys.argv[4:] if not a.startswith("lang=")] or ["cover", "video", "audio", "mux", "qa"]
    lang = next((a[5:] for a in sys.argv[4:] if a.startswith("lang=")), "en")
    os.makedirs(out, exist_ok=True)
    m = load(ep_path)
    scene = m.EPISODE(vo + ".json", vo + ".wav", lang=lang) if lang != "en" else m.EPISODE(vo + ".json", vo + ".wav")
    name = getattr(m, "NAME", "episode") + ("" if lang == "en" else "_" + lang)
    video, audio, final = (os.path.join(out, f) for f in ("video.mp4", "mix.wav", f"{name}_final.mp4"))
    print(f"{name}: {scene.duration:.2f}s, {int(round(scene.duration * 30))} frames")
    cover = os.path.join(out, "cover.png")
    use_cover = hasattr(scene, "draw_cover") and os.environ.get("BIK_COVER", "1") != "0"
    if use_cover and ("cover" in steps or ("video" in steps and not os.path.exists(cover))):
        import skia
        surf = skia.Surface(1080, 1920)
        info = scene.draw_cover(surf.getCanvas())
        surf.makeImageSnapshot().save(cover, skia.kPNG)
        scene.buf = None                                 # the render workers make their own
        print(f"cover {cover}: {info['lines']} (frame 0 of the video)")
    if "video" in steps:
        t0 = time.time()
        if use_cover:                                    # frame 0 = the cover; the posts pick it (thumbnailOffset 0)
            import skia
            scene.cover_frame = skia.Image.open(cover)
        # BIK_WORKERS overrides; default uses half the CPU threads (2 on the 2-core cloud box, 12 on a 32-thread PC)
        workers = int(os.environ.get("BIK_WORKERS", max(2, min(12, (os.cpu_count() or 2) // 2))))
        render(scene, scene.duration, video, os.path.join(out, "parts"), segments=max(8, 2 * workers), workers=workers)
        print(f"video done in {time.time() - t0:.0f}s")
    if "audio" in steps:
        build_mix(scene.tl, vo + ".wav", scene.sfx_events(), audio)
        print("audio done")
    if "mux" in steps:
        mux(video, audio, final)
        print("final", final)
    if "qa" in steps:
        qa(final, scene, out)


if __name__ == "__main__":
    main()
