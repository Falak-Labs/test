"""Yallah Say v2: the sound track and the timeline of one episode, from the takes pulled from GitHub.

usage: python3 build2.py <voice_dir> <page_dir> <out_dir> [--dry] [clip=take ...]
  clip=take   use another take for a clip (A_con=A_con2, v1=v1b)
  --dry       a take that is missing becomes a soft tone of a likely length (to check the picture before the voices exist)
A take is looked for in <voice_dir> (the lesson in this dialect), then beside it in kids<lesson> (the pupils' lines both
dialects share), <dialect>common (the teacher's lines that never change) and kidscommon (the pupils' goodbye).
writes <out_dir>/final.wav (48 kHz, -14 LUFS) and <page_dir>/tl.js (shots, beats, exact word times, mouth levels)."""
import json, os, re, subprocess, sys
import numpy as np, soundfile as sf, pyloudnorm as pyln

SR, FPS = 48000, 30
HOP, H10 = SR // FPS, SR // 100
VO, PAGE, OUT = sys.argv[1:4]
DRY = '--dry' in sys.argv
ALT = dict(a.split('=') for a in sys.argv[4:] if '=' in a)
os.makedirs(OUT, exist_ok=True)
S = json.loads(open(f'{PAGE}/script.js', encoding='utf-8').read()[len('window.SCRIPT='):].rstrip().rstrip(';'))
B, WD = S['beats'], S['word']
VROOT = os.path.dirname(os.path.abspath(VO))
FOLDERS = [VO, f"{VROOT}/kids{S['ep']}", f"{VROOT}/{S['theme']}common", f"{VROOT}/kidscommon"]
SYL = [s.lower() for s in WD['tts']]
TEXT = {}
for b in B:
    TEXT[b.get('clip', b['id'])] = b.get('en') or b.get('ar') or ''


def decode(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def rms10(y):
    n = len(y) // H10
    return np.sqrt((y[:n * H10].reshape(n, H10) ** 2).mean(1) + 1e-12)


def active(y):
    r = rms10(y)
    return r > max(10 ** (-46 / 20), r.max() * 10 ** (-28 / 20))


def words_of(t):
    out, cur, s0, e0 = [], '', None, None
    for ch, s, e in zip(t['chars'], t['starts'], t['ends']):
        if ch.isspace():
            if cur:
                out.append([cur, s0, e0])
            cur, s0 = '', None
            continue
        if not cur:
            s0 = s
        cur += ch
        e0 = e
    if cur:
        out.append([cur, s0, e0])
    return out


TAKES, MISSING = {}, []


def take(tid):
    if tid not in TAKES:
        d = next((d for d in FOLDERS if os.path.exists(f'{d}/{tid}.mp3')), None)
        p = f'{VO}/{tid}.mp3'
        if d:
            TAKES[tid] = (decode(f'{d}/{tid}.mp3'), json.load(open(f'{d}/{tid}.json', encoding='utf-8')))
        elif DRY:
            MISSING.append(tid)
            txt = TEXT.get(tid) or 'x' * 6
            d = 0.55 if re.fullmatch(r'[TAL]_\w+', tid) else 0.4 + 0.07 * len(txt)
            t = np.arange(int(d * SR)) / SR
            y = (0.03 * np.sin(2 * np.pi * 220 * t) * np.minimum(1, np.minimum(t, d - t) / 0.05)).astype(np.float32)
            n = len(txt)
            TAKES[tid] = (y, {'chars': list(txt), 'starts': [0.05 + (d - 0.1) * k / max(1, n) for k in range(n)], 'ends': [0.05 + (d - 0.1) * (k + 1) / max(1, n) for k in range(n)]})
        else:
            sys.exit(f'missing take {p}')
    return TAKES[tid]


def cut(y, t0, t1, words):
    """The audio between t0 and t1, trimmed to the speech and levelled. Word times move with it."""
    i0, i1 = max(0, int(t0 * SR)), min(len(y), int(t1 * SR))
    seg = y[i0:i1]
    idx = np.flatnonzero(active(seg))
    a, b = max(0, idx[0] * H10 - int(0.03 * SR)), min(len(seg), (idx[-1] + 1) * H10 + int(0.08 * SR))
    seg = seg[a:b].copy()
    shift = (i0 + a) / SR
    r = rms10(seg)
    lvl = 20 * np.log10(np.sqrt((r[active(seg)] ** 2).mean()) + 1e-9)
    seg *= min(3.2, max(0.4, 10 ** ((-20.0 - lvl) / 20)))
    k = int(0.006 * SR)
    seg[:k] *= np.linspace(0, 1, k)
    seg[-k:] *= np.linspace(1, 0, k)
    dur = len(seg) / SR
    return seg, [[w, min(dur, max(0.0, s - shift)), min(dur, max(0.0, e - shift))] for w, s, e in words]


CLIPS = {}


def clip_of(tid):
    tid = ALT.get(tid, tid)
    if tid not in CLIPS:
        y, t = take(tid)
        CLIPS[tid] = cut(y, 0, 99, [] if re.fullmatch(r'[TAL]_\w+', tid) else words_of(t))
    return CLIPS[tid]


def spread(y, words):
    """Fallback word starts when ElevenLabs' timings do not match the words: by letter count over the speech."""
    act = active(y)
    ca = np.cumsum(act) * 0.01
    wt = [max(2, len(re.sub(r'[^\w]', '', w))) for w in words]
    acc, out = 0, []
    for w in wt:
        out.append(round(min(int(np.searchsorted(ca, acc / sum(wt) * ca[-1] + 0.005)), len(act) - 1) * 0.01, 2))
        acc += w
    return out, out[1:] + [round(len(y) / SR, 2)]


snap = lambda t: float(np.ceil(t * FPS - 1e-6) / FPS)
shots, beats, place, fx, notes = [], [], [], [], []
prev_end = raw_end = 0.0
for i, b in enumerate(B):
    sil = b.get('sil')
    if sil:
        y, ws = np.zeros(int(sil * SR), dtype=np.float32), []
    else:
        y, ws = clip_of(b.get('clip', b['id']))
        if b.get('cho'):
            z = clip_of(b['cho'])[0]
            n = max(len(y), len(z))
            y = (np.pad(y, (0, n - len(y))) + np.pad(z, (0, n - len(z)))) * 0.72
    start, cutt = prev_end + b.get('pre', 0.30), None
    if i == 0 or b['shot'] != B[i - 1]['shot']:
        lead = b.get('lead', 0.22)
        cutt = 0.0 if i == 0 else snap(max(raw_end + 0.06, start - lead))
        start = max(start, cutt + min(lead, 0.18))
        shots.append({'k': b['shot'], 'a': round(cutt, 4), 'i': i})
        if b['shot'] == 'K' and lead >= 0.8:      # two soft ticks while the pupil (and the viewer) thinks
            fx += [['tick', round(cutt + 0.3, 3)], ['tick', round(cutt + 0.68, 3)]]
    end = start + len(y) / SR
    if not sil:
        place.append((start, y))
    want = (b.get('en') or b.get('ar') or '').split(' ') if not sil and (b.get('en') or b.get('ar')) else []
    if want and len(ws) == len(want):
        w, e = [round(x[1], 3) for x in ws], [round(x[2], 3) for x in ws]
    elif want:
        w, e = spread(y, want)
        notes.append(f"{b['id']}: word times estimated ({len(ws)} timed words for {len(want)})")
    else:
        w, e = [], []
    nfr = int(np.ceil(len(y) / HOP))
    yp = np.pad(y, (0, nfr * HOP - len(y)))
    env = np.sqrt((yp.reshape(nfr, HOP) ** 2).mean(1))
    env = np.minimum(1.0, env / (np.percentile(env, 92) + 1e-9)) ** 0.7 if not sil else env
    for k in range(1, nfr):
        env[k] = max(env[k], env[k - 1] * 0.5)
    env[env < 0.09] = 0
    beats.append({'a': round(start, 3), 'b': round(end, 3), 'w': w, 'e': e, 'env': ''.join(str(int(round(v * 9))) for v in env)})
    f = b.get('fx')
    if f in ('ding', 'ding2'):
        fx.append([f, round(end + 0.08, 3)])
    elif f == 'tada':
        fx.append(['tada', round(end + 0.05, 3)])
    elif f == 'tada0':
        fx.append(['tada', round(start - 0.02, 3)])
    elif f == 'whoosh':
        fx.append(['whoosh', round(cutt if cutt is not None else start, 3)])
    elif f in ('jingle', 'drum'):
        fx.append([f, round((cutt if cutt is not None else start) + 0.06, 3)])
    elif f == 'ticks':
        t0 = start + 0.3
        while t0 < end - 0.25:
            fx.append(['tick', round(t0, 3)]); t0 += 0.5
    raw_end, prev_end = end, end + b.get('post', 0.0)
dur = snap(prev_end)
nf = int(round(dur * FPS))
for s, nx in zip(shots, shots[1:] + [None]):
    s['b'] = nx['a'] if nx else round(dur, 4)

mix = np.zeros(int(dur * SR) + SR, dtype=np.float32)
for st, y in place:
    i0 = int(round(st * SR))
    mix[i0:i0 + len(y)] += y
tt = lambda d: np.arange(int(d * SR)) / SR


def bell(parts, d, amp, tau):
    t = tt(d)
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / (tau * k)) for f, a, k in parts) * np.minimum(1, t / 0.004)
    return (amp * y / np.abs(y).max()).astype(np.float32)


def run(notes_hz, step, amp, tau, d=0.9):
    y = np.zeros(int((d + step * len(notes_hz)) * SR), dtype=np.float32)
    for k, f in enumerate(notes_hz):
        c = bell([(f, 1, 1), (2 * f, .35, .6), (3 * f, .12, .4)], d, amp, tau)
        i0 = int(step * k * SR)
        y[i0:i0 + len(c)] += c
    return y


def sfx(name):
    if name == 'ding':
        return bell([(1318.5, 1, 1), (1975.5, .5, .8), (2637, .25, .6)], 0.6, 0.075, 0.12)
    if name == 'ding2':
        return bell([(1318.5, 1, 1), (1975.5, .5, .8), (2637, .25, .6)], 0.5, 0.045, 0.1)
    if name == 'tick':
        t = tt(0.06)
        return (0.03 * np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.009)).astype(np.float32)
    if name == 'jingle':
        return run([783.99, 1046.5, 1318.5], 0.1, 0.06, 0.16, 0.7)
    if name == 'drum':
        return run([392.0, 523.25, 659.25, 783.99], 0.11, 0.07, 0.2)
    if name == 'whoosh':
        t = tt(0.4)
        n = np.random.default_rng(7).standard_normal(len(t))
        y, a = np.zeros(len(t)), 0.0
        for k in range(len(t)):
            a += (0.02 + 0.25 * (k / len(t))) * (n[k] - a)
            y[k] = a
        y *= np.sin(np.pi * t / 0.4) ** 2
        return (0.045 * y / np.abs(y).max()).astype(np.float32)
    return run([523.25, 659.25, 783.99, 1046.5], 0.085, 0.08, 0.22)          # tada


for name, t0 in fx:
    y = sfx(name)
    i0 = int(max(0, t0) * SR)
    mix[i0:i0 + len(y)] += y[:len(mix) - i0]
mix = mix[:int(round(dur * SR))]
meter = pyln.Meter(SR)
mix *= 10 ** ((-14.0 - meter.integrated_loudness(mix)) / 20)
sf.write(f'{OUT}/mix.wav', np.stack([mix, mix], 1), SR, subtype='PCM_16')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/mix.wav', '-af', 'alimiter=limit=0.891:attack=2:release=40:level=false', '-ar', str(SR),
                '-c:a', 'pcm_s16le', f'{OUT}/final.tmp.wav'], check=True)
yy, _ = sf.read(f'{OUT}/final.tmp.wav')
g = 10 ** ((-14.0 - meter.integrated_loudness(yy)) / 20)
yy = np.clip(yy * min(g, 0.891 / np.abs(yy).max()), -1, 1)
sf.write(f'{OUT}/final.wav', yy, SR, subtype='PCM_16')

J = lambda o: json.dumps(o, separators=(',', ':'))
lines = ['window.TL={"dur":%s,"nf":%d,' % (round(dur, 4), nf), '"shots":' + J(shots) + ',', '"fx":' + J(fx) + ',', '"beats":['] + \
        [J(o) + (',' if i < len(beats) - 1 else '') for i, o in enumerate(beats)] + [']};']
open(f'{PAGE}/tl.js', 'w').write('\n'.join(lines) + '\n')
first = lambda k: next((s['a'] for s in shots if s['k'] == k), None)
print('duration %d:%05.2f (%d frames) | %d shots, %d beats | %.1f LUFS, peak %.3f' % (dur // 60, dur % 60, nf, len(shots), len(beats), meter.integrated_loudness(yy), np.abs(yy).max()))
print('quiz', first('R'), '| hard word', first('H'), '| end card', first('C'), '| word parts (s):', {sp: [round(len(clip_of(f'{sp}_{s}')[0]) / SR, 2) for s in SYL] for sp in 'TAL'})
if MISSING:
    print('DRY RUN, missing takes:', len(MISSING))
for n in notes:
    print('note:', n)
