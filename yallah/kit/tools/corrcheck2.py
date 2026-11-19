"""Is every take intact and in place in the finished file?  For each spoken line, the stretch of the MP4's sound track where the
timeline puts it is matched against the original take (correlation 1.0 = identical apart from level).
usage: VO=<voice_dir> corrcheck2.py <final.mp4> <page_dir> [clip=take ...]"""
import json, subprocess, sys
import numpy as np
SR, VO = 16000, __import__('os').environ['VO']
MP4, PAGE = sys.argv[1], sys.argv[2]
ALT = dict(x.split('=') for x in sys.argv[3:] if '=' in x)
js = lambda n: json.loads(open(f'{PAGE}/{n}', encoding='utf-8').read().split('=', 1)[1].rstrip().rstrip(';'))
S, T = js('script.js'), js('tl.js')
def decode(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vn', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)
Y = decode(MP4); low = []
for i, b in enumerate(S['beats']):
    if b.get('syl') is not None or b.get('sil') or b.get('cho'): continue      # word parts, pauses and two-voice lines are checked by ear below
    a, e = T['beats'][i]['a'], T['beats'][i]['b']
    tid = b.get('clip', b['id']); tid = ALT.get(tid, tid)
    seg = Y[int(a * SR):int(e * SR)]; y = decode(f"{VO}/{tid}.mp3")
    y = np.concatenate([np.zeros(SR // 4), y, np.zeros(SR // 4)])
    c = np.correlate(y, seg, 'valid'); n = len(seg)
    cs = np.concatenate([[0], np.cumsum(y ** 2)]); en = np.sqrt((cs[n:] - cs[:-n]) * (seg ** 2).sum()) + 1e-9
    r = c / en; k = int(np.argmax(r))
    if r[k] < 0.9: low.append(b['id'])
    print(f"{'ok  ' if r[k] >= 0.9 else 'LOOK'} {b['id']:7s} at {a:7.2f}s len {e - a:4.2f}s  match {r[k]:.3f}  (take offset {k / SR - .25:+.2f}s)")
print('below 0.9:', low or 'none')
