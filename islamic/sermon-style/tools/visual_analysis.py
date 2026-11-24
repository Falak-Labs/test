"""Visual analysis of the reference: palette, background gradient, scene changes, motion, text bands."""
import sys, json, subprocess
import numpy as np
import cv2

src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
idx = 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    if idx % 3 == 0:  # 10 fps, half size, uint8
        frames.append(cv2.resize(f, (f.shape[1] // 2, f.shape[0] // 2), interpolation=cv2.INTER_AREA))
    idx += 1
n = len(frames)
H, W = frames[0].shape[:2]
t = np.arange(n) * 3 / fps
end = int(np.argmax(t > 64.5)) if (t > 64.5).any() else n  # creator content ends ~64.5 s (TikTok outro after)
F = np.stack(frames[:end])  # uint8

# ---- background: per-pixel temporal median over the whole clip, then sample a vertical profile
med = np.median(F[::10], axis=0)
prof = med[:, W // 2 - 20:W // 2 + 20].mean(axis=1)  # BGR down the frame centre
corner = np.median(F[::5, 3:30, 3:30].reshape(-1, 3), axis=0)
center = np.median(F[::5, H // 2 - 15:H // 2 + 15, W // 2 - 15:W // 2 + 15].reshape(-1, 3), axis=0)

def hexc(bgr):
    b, g, r = [int(round(x)) for x in bgr]
    return f"#{r:02x}{g:02x}{b:02x}"

res = {
    "fps": fps, "size": [W, H], "creator_content_end_s": round(float(t[end - 1]), 2),
    "bg_median_corner": hexc(corner), "bg_median_center": hexc(center),
    "bg_vertical_profile": {f"{int(100*y/H)}%": hexc(prof[y]) for y in range(0, H, H // 10)},
}

# ---- palette: classify bright pixels
allpx = F[::4, ::2, ::2].reshape(-1, 3).astype(np.float32)
hsv = cv2.cvtColor(allpx.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_BGR2HSV).reshape(-1, 3).astype(np.float32)
v, s, h = hsv[:, 2], hsv[:, 1], hsv[:, 0] * 2
bright = v > 150
gold = bright & (s > 110) & (h > 30) & (h < 55)
red = bright & (s > 110) & ((h < 12) | (h > 345))
white = (v > 200) & (s < 40)
for name, m in [("gold", gold), ("red", red), ("white_line", white)]:
    if m.sum() > 50:
        res[f"{name}_median"] = hexc(np.median(allpx[m], axis=0))
        res[f"{name}_share_of_pixels_pct"] = round(100 * m.mean(), 3)

# ---- scene changes and motion
gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in F]
diff = np.array([np.mean(np.abs(gray[i] - gray[i - 1])) for i in range(1, len(gray))])
res["motion_mean_abs_diff"] = round(float(diff.mean()), 3)
# a "beat change" = big change in the top text band (headline swaps)
band = [g[int(0.08 * H):int(0.18 * H)] for g in gray]
bdiff = np.array([np.mean(np.abs(band[i] - band[i - 1])) for i in range(1, len(band))])
thr = np.percentile(bdiff, 93)
peaks = [i for i in range(1, len(bdiff) - 1) if bdiff[i] > thr and bdiff[i] >= bdiff[i - 1] and bdiff[i] >= bdiff[i + 1]]
merged = []
for p in peaks:
    if not merged or (p - merged[-1]) > 8:
        merged.append(p)
res["headline_change_times_s"] = [round(float(t[p + 1]), 1) for p in merged]
gaps = np.diff([0] + res["headline_change_times_s"] + [res["creator_content_end_s"]])
res["headline_hold_s_median"] = round(float(np.median(gaps)), 2)

# ---- where things sit: brightness by row (time-averaged max)
rowmax = np.percentile(np.stack(gray), 99, axis=0).max(axis=1)
active = [int(100 * y / H) for y in range(0, H, 8) if rowmax[y] > 120]
res["rows_with_bright_content_pct"] = sorted(set(active))
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
cv2.imwrite(out.replace(".json", "_median_bg.png"), med.astype(np.uint8))
