"""Free speech check: transcribe every take with Whisper (sherpa-onnx, large-v3-turbo) and compare with the script."""
import difflib, json, re, subprocess, sys, time
import numpy as np, sherpa_onnx
VO, M = sys.argv[1], '/home/claude/models/sherpa-onnx-whisper-turbo'
def rec(lang):
    return sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f'{M}/turbo-encoder.int8.onnx', decoder=f'{M}/turbo-decoder.int8.onnx',
                                                      tokens=f'{M}/turbo-tokens.txt', language=lang, task='transcribe', num_threads=2)
R = {'en': rec('en'), 'ar': rec('ar')}
def norm(s):
    s = re.sub(r'\[[^\]]*\]', ' ', s.lower())
    s = re.sub(r'[ً-ْـ]', '', s)
    return ' '.join(re.sub(r"[^\w' ]", ' ', s).split())
man = json.load(open(f'{VO}/manifest.json', encoding='utf-8'))
only = set(sys.argv[2:]); t0 = time.monotonic(); bad = 0
for L in man['lines']:
    if only and L['id'] not in only: continue
    lang = 'ar' if re.search(r'[؀-ۿ]', L['text']) else 'en'
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f"{VO}/{L['id']}.mp3", '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, dtype=np.float32)
    st = R[lang].create_stream(); st.accept_waveform(16000, np.concatenate([y, np.zeros(8000, np.float32)])); R[lang].decode_stream(st)
    heard = st.result.text.strip(); score = difflib.SequenceMatcher(None, norm(L['text']), norm(heard)).ratio()
    flag = 'ok ' if score >= (0.8 if lang == 'en' else 0.6) else 'LOOK'; bad += flag == 'LOOK'
    print(f"{flag} {score:.2f} {L['id']:7s} {L['speaker']} | {L['text']} | {heard}", flush=True)
print(f"checked in {time.monotonic() - t0:.0f} s; {bad} lines to look at")
