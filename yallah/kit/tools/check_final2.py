"""End-to-end check of a finished episode: cut each spoken line out of the MP4's own sound track at the time the picture
shows it, transcribe it with Whisper and compare with the script.   usage: check_final.py <final.mp4> <page_dir>"""
import difflib, json, re, subprocess, sys, time
import numpy as np, sherpa_onnx
MP4, PAGE, M = sys.argv[1], sys.argv[2], __import__('os').environ.get('YS_WHISPER', '/home/claude/models/sherpa-onnx-whisper-turbo')
def js(name, var):
    return json.loads(open(f'{PAGE}/{name}', encoding='utf-8').read().split('=', 1)[1].rstrip().rstrip(';'))
S, T = js('script.js', 'SCRIPT'), js('tl.js', 'TL')
def rec(lang):
    return sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f'{M}/turbo-encoder.int8.onnx', decoder=f'{M}/turbo-decoder.int8.onnx',
                                                      tokens=f'{M}/turbo-tokens.txt', language=lang, task='transcribe', num_threads=2)
R = {'en': rec('en'), 'ar': rec('ar')}
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', MP4, '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
Y = np.frombuffer(raw, dtype=np.float32)
def norm(s):
    s = re.sub(r'[ً-ْـ]', '', s.lower())
    return ' '.join(re.sub(r"[^\w' ]", ' ', s).split())
def hear(a, b, lang):
    y = Y[max(0, int((a - 0.1) * 16000)):int((b + 0.15) * 16000)]
    st = R[lang].create_stream(); st.accept_waveform(16000, np.concatenate([y, np.zeros(8000, np.float32)])); R[lang].decode_stream(st)
    return st.result.text.strip()
t0 = time.monotonic(); bad = 0; n = 0
B = [dict(b, **T['beats'][i]) for i, b in enumerate(S['beats'])]
for b in B:
    if b.get('syl') is not None or b.get('sil'): continue
    want = b.get('en') or b.get('ar'); lang = 'en' if b.get('en') else 'ar'
    heard = hear(b['a'], b['b'], lang); score = difflib.SequenceMatcher(None, norm(want), norm(heard)).ratio(); n += 1
    flag = 'ok ' if score >= (0.8 if lang == 'en' else 0.6) else 'LOOK'; bad += flag == 'LOOK'
    print(f"{flag} {score:.2f} {b['a']:7.2f} {b['id']:7s} {b['sp']:2s} | {want} | {heard}", flush=True)
# the syllable rounds, each heard as one stretch
NP = len(S['word']['parts'])
for name, ids in (('slow', [f's{i}{k}' for i in range(NP) for k in 'ta']), ('fast teacher', [f'f{i}t' for i in range(NP)]), ('fast pupils', [f'f{i}k' for i in range(NP)])):
    bs = [b for b in B if b['id'] in ids]
    if not bs: continue
    print(f"--  {name:13s} {bs[0]['a']:7.2f}-{bs[-1]['b']:7.2f} | {hear(bs[0]['a'], bs[-1]['b'], 'en')}", flush=True)
print(f"{n} lines checked in {time.monotonic() - t0:.0f} s; {bad} to look at")
