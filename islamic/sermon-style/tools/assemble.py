"""Turn one ElevenLabs take into the episode's sound and timeline.

  assemble.py take.wav take.json out_dir --gaps "8:1.1,10:0.9" [--bed bed.wav] [--min-gap 0.45] [--lead 0.6]

1. Pauses between lines are stretched to at least --min-gap, and to the given seconds after listed lines (1-based),
   so the pacing matches the reference (short breaths, long dramatic stops after the key lines).
2. Voice chain: 70 Hz high-pass, gentle compression, a small room (the reference voice sits in a hall).
3. Bed: drone 15.5 LU under the voice, ducked ~5 dB while the voice speaks (the reference ducks about 6.6 dB).
4. Master: -14 LUFS integrated, true peak -1 dBTP (TikTok, Reels, Shorts and YouTube all play near -14).
Writes out_dir/voice.wav, out_dir/mix.wav, out_dir/timeline.json (lines and words with final times).
"""
import argparse, json, os, subprocess, tempfile
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt, fftconvolve

ap = argparse.ArgumentParser()
ap.add_argument("wav"); ap.add_argument("json"); ap.add_argument("out")
ap.add_argument("--gaps", default="")
ap.add_argument("--min-gap", type=float, default=0.45)
ap.add_argument("--lead", type=float, default=0.6, help="silence before the first word")
ap.add_argument("--tail", type=float, default=2.5, help="seconds after the last word")
ap.add_argument("--bed", default="")
ap.add_argument("--bed-under", type=float, default=15.5)
ap.add_argument("--duck", type=float, default=5.0)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
SR = 44100
y, sr = sf.read(a.wav)
assert sr == SR
meta = json.load(open(a.json, encoding="utf-8"))
lines = meta["lines"]
want = {int(k): float(v) for k, v in (p.split(":") for p in a.gaps.split(",") if p.strip())}

# --- cut points between lines (middle of the silence), then rebuild with longer pauses
pieces, shifts, t_cut_prev = [], [], 0.0
cuts = []
hop10 = int(0.01 * SR)
rms10 = np.sqrt(np.convolve(y ** 2, np.ones(hop10) / hop10, mode="same") + 1e-12)
quiet_thr = 0.03 * np.percentile(rms10[::hop10], 95)


def quiet_cut(e, s):
    """Cut in the quietest 30 ms between the end of one line and the start of the next (word times can include
    punctuation, so they are only a guide); returns the cut time and the length of the natural pause around it."""
    lo, hi = max(0.0, min(e, s) - 0.15), max(e, s) + 0.10
    seg = y[int(lo * SR):int(hi * SR)]
    win, hop = int(0.03 * SR), int(0.005 * SR)
    best = min(range(0, max(1, len(seg) - win), hop), key=lambda k: float(np.sum(seg[k:k + win] ** 2)))
    c = lo + (best + win / 2) / SR
    ci = int(c * SR)
    l = ci
    while l > 0 and rms10[l] < quiet_thr:
        l -= hop10
    r = ci
    while r < len(y) - 1 and rms10[r] < quiet_thr:
        r += hop10
    return c, max(0.0, (r - l) / SR)


for i in range(len(lines) - 1):
    e, s = lines[i]["end"], lines[i + 1]["start"]
    c, gap = quiet_cut(e, s)
    target = max(a.min_gap, want.get(i + 1, 0.0))
    cuts.append((c, max(0.0, target - gap)))
start0 = max(0.0, lines[0]["start"] - 0.08)
seg_from = start0
out = [np.zeros(int(a.lead * SR))]
offset = a.lead - start0   # final_time = take_time + offset (+ inserted silences so far)
offsets = []
for (c, extra) in cuts:
    out.append(y[int(seg_from * SR):int(c * SR)])
    offsets.append((seg_from, c, offset))
    offset += extra
    out.append(np.zeros(int(extra * SR)))
    seg_from = c
end_t = min(len(y) / SR, lines[-1]["end"] + 0.35)
out.append(y[int(seg_from * SR):int(end_t * SR)])
offsets.append((seg_from, end_t, offset))
out.append(np.zeros(int(a.tail * SR)))
v = np.concatenate(out).astype(np.float64)


def remap(t):
    for s0, s1, off in offsets:
        if t < s1 + 1e-6:
            return round(t + off, 3)
    return round(t + offsets[-1][2], 3)


timeline = []
for i, L in enumerate(lines):
    ws = [{"w": w["w"], "start": remap(w["start"]), "end": remap(w["end"])} for w in L["words"]]
    timeline.append({"line": i + 1, "text": L["text"], "start": ws[0]["start"], "end": ws[-1]["end"], "words": ws})

# --- voice chain
sos = butter(2, 70, btype="high", fs=SR, output="sos")
v = sosfilt(sos, v)
# gentle compression (RMS follower, 2.5:1 above -22 dBFS)
env = np.sqrt(np.convolve(v ** 2, np.ones(int(0.03 * SR)) / int(0.03 * SR), mode="same") + 1e-12)
lev = 20 * np.log10(env)
gr = np.where(lev > -22, (lev + 22) * (1 - 1 / 2.5), 0.0)
gr = np.convolve(gr, np.ones(int(0.02 * SR)) / int(0.02 * SR), mode="same")
v = v * 10 ** (-gr / 20)
# small room: short decaying IR, 8% wet
rng = np.random.default_rng(11)
L = int(0.9 * SR); tt = np.arange(L) / SR
ir = rng.normal(0, 1, L) * np.exp(-tt / 0.22)
ir = sosfilt(butter(2, [250, 5000], btype="band", fs=SR, output="sos"), ir)
wet = fftconvolve(v, ir)[: len(v)]
wet *= np.std(v) / (np.std(wet) + 1e-12)
v = 0.92 * v + 0.08 * wet
meter = pyln.Meter(SR)
v = pyln.normalize.loudness(v, meter.integrated_loudness(v), -16.0)
sf.write(os.path.join(a.out, "voice.wav"), v.astype(np.float32), SR, subtype="FLOAT")
dur = len(v) / SR

# --- bed, ducked under the voice
mix = np.stack([v, v], 1)
if a.bed:
    b, bsr = sf.read(a.bed, always_2d=True)
    assert bsr == SR
    if len(b) < len(v):
        b = np.concatenate([b, np.zeros((len(v) - len(b), 2))])
    b = b[: len(v)]
    b = pyln.normalize.loudness(b, meter.integrated_loudness(b), -16.0 - a.bed_under)
    act = (np.abs(v) > 10 ** (-38 / 20)).astype(float)
    k_att, k_rel = int(0.08 * SR), int(0.6 * SR)
    sm = np.zeros_like(act); g = 0.0
    # simple attack/release follower, vectorised per 10 ms block
    blk = int(0.01 * SR)
    blocks = act[: len(act) // blk * blk].reshape(-1, blk).max(1)
    gb = np.zeros(len(blocks))
    for i, x in enumerate(blocks):
        g = g + (x - g) * (0.12 if x > g else 0.016)
        gb[i] = g
    gain_db = -a.duck * np.repeat(gb, blk)
    gain_db = np.concatenate([gain_db, np.full(len(v) - len(gain_db), gain_db[-1] if len(gain_db) else 0)])
    b = b * (10 ** (gain_db / 20))[:, None]
    fo = min(len(b), int(3.0 * SR))   # let the bed breathe out at the very end
    b[-fo:] *= (np.linspace(1, 0, fo) ** 1.6)[:, None]
    mix = mix + b
with tempfile.TemporaryDirectory() as td:
    raw = os.path.join(td, "raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.0:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", str(SR), os.path.join(a.out, "mix.wav")], check=True)
json.dump({"duration": round(dur, 3), "lead": a.lead, "lines": timeline}, open(os.path.join(a.out, "timeline.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"voice {dur:.2f}s, {len(lines)} lines -> {a.out}")
