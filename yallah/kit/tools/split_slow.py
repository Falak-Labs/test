"""Cut a take of the hard word said slowly ("Grand... moth... er.") at its pauses into one file per part.
usage: python3 -I split_slow.py <take.mp3> <parts> <out_prefix>     e.g. split_slow.py s04a.mp3 3 /tmp/T_
Writes <out_prefix>0.wav ... ; exits 1 if the take does not have exactly <parts> sounds between pauses."""
import subprocess, sys
import numpy as np

SR = 24000
src, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]


def pieces(y, n):
    """The n loudest-separated stretches: frames of 10 ms, quiet where below 4 % of the take's peak level."""
    f = SR // 100
    e = np.sqrt(np.convolve(y ** 2, np.ones(f) / f, "same"))[::f]
    on = e > 0.04 * e.max()
    runs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            runs.append([i, j]); i = j
        else:
            i += 1
    while len(runs) > n:            # join across the shortest gap until n remain
        g = [runs[k + 1][0] - runs[k][1] for k in range(len(runs) - 1)]
        k = int(np.argmin(g)); runs[k][1] = runs[k + 1][1]; del runs[k + 1]
    return [(max(0, a * f - SR * 3 // 100), min(len(y), b * f + SR * 6 // 100)) for a, b in runs]


raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
y = np.frombuffer(raw, dtype=np.float32)
P = pieces(y, n)
if len(P) != n:
    print(f"{src}: {len(P)} sounds, want {n}"); sys.exit(1)
for i, (a, b) in enumerate(P):
    seg = y[a:b].copy(); k = min(len(seg) // 4, SR // 100)
    seg[:k] *= np.linspace(0, 1, k); seg[-k:] *= np.linspace(1, 0, k)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", f"{out}{i}.wav"], input=seg.tobytes(), check=True)
print(src, "→", " ".join(f"{(b - a) / SR:.2f}s" for a, b in P))
