"""Does each voice say the hard word right?  Whisper (small.en) listens to every take of the word: the whole word ("tw"),
each part on its own (T_, A_, L_), and the parts joined back together the way the slow round plays them.
The joined parts should be heard as the word; each part should sound like its spelling in "say".

usage: python3 -I saycheck.py <lesson numbers ...>         e.g. saycheck.py 07 08 09
       WHISPER_DIR=<sherpa-onnx-whisper-small.en folder>  (default /home/claude/tts/asr/sherpa-onnx-whisper-small.en)
Prints one block per lesson and voice, marks LOOK where a take is doubtful, and ends with the list to listen to."""
import difflib, json, os, re, subprocess, sys
import numpy as np
import sherpa_onnx

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VOICE, LESSONS = f"{ROOT}/darija/voice", f"{ROOT}/yallah/lessons"
WD = os.environ.get("WHISPER_DIR", "/home/claude/tts/asr/sherpa-onnx-whisper-small.en")
SR = 16000
pre = lambda n: os.path.join(WD, next(f for f in os.listdir(WD) if f.endswith(n)))
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=pre("encoder.int8.onnx"), decoder=pre("decoder.int8.onnx"),
                                                 tokens=pre("tokens.txt"), language="en", task="transcribe")


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def hear(y):
    y = np.concatenate([np.zeros(SR // 2, np.float32), y, np.zeros(SR // 2, np.float32)])
    s = rec.create_stream(); s.accept_waveform(SR, y); rec.decode_stream(s)
    return s.result.text.strip()


letters = lambda t: re.sub(r"[^a-z]", "", t.lower())
like = lambda a, b: difflib.SequenceMatcher(None, letters(a), letters(b)).ratio()


def find(folders, tid):
    return next((f"{d}/{tid}.mp3" for d in folders if os.path.exists(f"{d}/{tid}.mp3")), None)


look = []
for n in sys.argv[1:]:
    W = json.load(open(f"{LESSONS}/{n}.json"))["word"]
    keys = []
    for s in W["tts"]:
        k = s.lower(); keys.append(k + str(len(keys)) if k in keys else k)
    for who, folders in (("ma teacher", [f"{VOICE}/ma{n}", f"{VOICE}/ma{n[-2:]}"]), ("pa teacher", [f"{VOICE}/pa{n}"]),
                         ("Adam", [f"{VOICE}/kids{n}"]), ("Lina", [f"{VOICE}/kids{n}"])):
        sp = {"Adam": "A", "Lina": "L"}.get(who, "T")
        if sp == "T" and json.load(open(f"{LESSONS}/{n}.json")).get("own_lines") and not os.path.exists(folders[0]):
            continue
        parts = [find(folders, f"{sp}_{k}") for k in keys]
        if not all(parts):
            continue
        gap = np.zeros(int(SR * 0.08), np.float32)
        joined = hear(np.concatenate(sum([[load(p), gap] for p in parts], [])))
        r = like(joined, W["full"])
        mark = "ok  " if r >= 0.75 else "LOOK"
        if r < 0.75: look.append(f"{n} {who}: joined parts heard as \"{joined}\" (want {W['full']})")
        line = [f"{mark} {n} {who:10s} joined → \"{joined}\" ({r:.2f})"]
        for k, s, p in zip(keys, W["say"], parts):
            h = hear(load(p)); q = max(like(h, s), like(h, k))
            line.append(f"      {k:6s} → \"{h}\" ({q:.2f})")
        whole = find(folders, "tw") if sp == "T" else find(folders, f"{sp}w")
        if whole:
            h = hear(load(whole)); q = like(h, W["full"])
            line.append(f"      whole word → \"{h}\" ({q:.2f})")
            if q < 0.75: look.append(f"{n} {who}: whole word heard as \"{h}\" (want {W['full']})")
        print("\n".join(line))
print("\nlisten to:" if look else "\nall heard as the word", *look, sep="\n  ")
