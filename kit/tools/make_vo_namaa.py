"""Saudi Arabic voiceover with NAMAA Saudi TTS (MIT license; a Saudi-dialect fine-tune of Resemble AI's
Chatterbox Multilingual, also MIT). Runs on CPU, no internet needed.

usage:
  python3 -I tools/make_vo_namaa.py <lines_ar_sa.txt> <out_prefix> [--model-dir ~/tts/namaa-saudi]
        [--voice builtin|clip.wav] [--seed 11] [--tempo 1.0] [--gap 0.3] [--asr] [--verify] [--only 3,7]

Outputs, same as make_vo_ar.py: <out>.wav / .json (line and word timings) / .mp3, <out>_raw.*, plus
<out>_lines/ with one saved take per line. Run it again after editing a line and only that line is made
again; --only 3,7 makes a fresh take of lines 3 and 7 and keeps the rest.

- Plain Arabic letters are enough (vowel marks optional). Write numbers as words.
- Word times come from the model's own text-to-speech attention (the heads Chatterbox watches to know
  where it is in the text), so captions and animation cues land on the spoken words.
- A take is made again with another seed when it stops before the end of its text, runs far too fast
  or slow, or (with --asr) Whisper hears something too different.
- --voice builtin is the conds.pt voice shipped with the model. A clip (10-20 s, one clean speaker)
  clones that voice: only use a voice you have the right to use (your own, or one licensed for this).
- The final wav carries Resemble AI's inaudible Perth watermark, which marks it as AI-made. Keep it.
"""
import argparse
import difflib
import hashlib
import importlib
import json
import logging
import os
import re
import subprocess
import sys
import time

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # everything is local: never wait on the network
import numpy as np
import soundfile as sf
import torch
import torch.nn.functional as F
from safetensors.torch import load_file

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("lines")
ap.add_argument("out")
ap.add_argument("--tts-home", default=os.environ.get("TTS_HOME", os.path.expanduser("~/tts")))
ap.add_argument("--model-dir", default=None, help="default: <tts-home>/namaa-saudi")
ap.add_argument("--voice", default="builtin")
ap.add_argument("--exaggeration", type=float, default=0.5)
ap.add_argument("--cfg", type=float, default=0.5)
ap.add_argument("--temperature", type=float, default=0.8)
ap.add_argument("--rep-penalty", type=float, default=2.0)
ap.add_argument("--min-p", type=float, default=0.05)
ap.add_argument("--top-p", type=float, default=1.0)
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--tries", type=int, default=3)
ap.add_argument("--min-rate", type=float, default=7.0, help="slowest acceptable take, letters per second")
ap.add_argument("--max-rate", type=float, default=22.0, help="fastest acceptable take, letters per second")
ap.add_argument("--tempo", type=float, default=1.0)
ap.add_argument("--gap", type=float, default=0.3)
ap.add_argument("--max-pause", type=float, default=0.45, help="pauses inside a line longer than this ...")
ap.add_argument("--keep-pause", type=float, default=0.3, help="... are shortened to this")
ap.add_argument("--lead", type=float, default=0.0, help="shift every word time by this many seconds")
ap.add_argument("--dtype", choices=["bf16", "fp32"], default="fp32", help="speech-token model precision")
ap.add_argument("--max-new-tokens", type=int, default=1000)
ap.add_argument("--only", default="")
ap.add_argument("--asr", action="store_true", help="also check each take with Whisper small")
ap.add_argument("--verify", action="store_true")
a = ap.parse_args()
md = os.path.expanduser(a.model_dir or os.path.join(a.tts_home, "namaa-saudi"))
torch.set_num_threads(max(1, min(16, os.cpu_count() or 1)))  # more threads than cores slows decoding

# Chatterbox, quiet and Arabic-only (skip the Chinese helper that would try to download a file)
t3mod = importlib.import_module("chatterbox.models.t3.t3")
t3mod.tqdm = lambda it, **kw: it
tokmod = importlib.import_module("chatterbox.models.tokenizers.tokenizer")
tokmod.ChineseCangjieConverter._load_cangjie_mapping = lambda self, model_dir=None: None
tokmod.ChineseCangjieConverter._init_segmenter = lambda self: None
from chatterbox.mtl_tts import ChatterboxMultilingualTTS, Conditionals, punc_norm  # noqa: E402
from chatterbox.models.s3gen import S3Gen  # noqa: E402
from chatterbox.models.s3tokenizer import drop_invalid_tokens  # noqa: E402
from chatterbox.models.t3 import T3  # noqa: E402
from chatterbox.models.t3.inference.alignment_stream_analyzer import LLAMA_ALIGNED_HEADS  # noqa: E402
from chatterbox.models.t3.modules.cond_enc import T3Cond  # noqa: E402
from chatterbox.models.t3.modules.t3_config import T3Config  # noqa: E402
from chatterbox.models.tokenizers import MTLTokenizer  # noqa: E402
from chatterbox.models.voice_encoder import VoiceEncoder  # noqa: E402


class Catch(logging.Handler):
    """Collect the alignment checker's warnings (forced stops) for the take report."""
    def __init__(self):
        super().__init__()
        self.msgs = []

    def emit(self, record):
        self.msgs.append(record.getMessage())


catch = Catch()
_lg = logging.getLogger("chatterbox.models.t3.inference.alignment_stream_analyzer")
_lg.addHandler(catch)
_lg.setLevel(logging.INFO)
_lg.propagate = False
logging.getLogger("chatterbox.models.t3.t3").setLevel(logging.WARNING)

SR, FR = 24000, 0.04  # output sample rate; one speech token = 40 ms of audio
TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟـ]")
PUNCT = set(",.;:!?،؛؟\"'()")
SWAP = {"،": ",", "؛": ",", "؟": "?"}


# ---------------------------------------------------------------- model
def find(stem):
    for ext in (".bf16.safetensors", ".safetensors", ".pt"):
        p = os.path.join(md, stem + ext)
        if os.path.exists(p):
            return p
    raise SystemExit(f"{stem}.* not found in {md} (unzip namaa_saudi.zip so its files sit there)")


def read_sd(p):
    sd = load_file(p) if p.endswith(".safetensors") else torch.load(p, map_location="cpu", weights_only=True)
    if isinstance(sd.get("model"), (list, tuple)):
        sd = sd["model"][0]
    for pre in ("module.", "model."):
        if sd and all(k.startswith(pre) for k in sd):
            sd = {k[len(pre):]: v for k, v in sd.items()}
    return sd


def load_into(m, sd, name):
    missing, extra = m.load_state_dict(sd, strict=False)
    bufs = {k for k, _ in m.named_buffers()}
    hard = [k for k in missing if k not in bufs]  # buffers (mel filters, windows) are rebuilt at init
    if hard:
        raise SystemExit(f"{name}: {len(hard)} weights missing, e.g. {hard[:3]}")
    if extra:
        print(f"  {name}: ignored {len(extra)} extra tensors, e.g. {extra[:2]}")
    return m.eval()


t_load = time.time()
sd = read_sd(find("t3_mtl23ls_v2"))
n_text = sd["text_emb.weight"].shape[0]
hp = T3Config(text_tokens_dict_size=n_text)
if not hp.is_multilingual:  # a resized vocabulary: keep Chatterbox's alignment checker switched on
    T3Config.is_multilingual = property(lambda self: True)
t3 = load_into(T3(hp), sd, "t3")
del sd
if a.dtype == "bf16":  # optional; on a 2-core CPU it was barely faster. Logits stay fp32 either way
    t3.to(torch.bfloat16)
    t3.speech_head.float()
    t3.speech_head.register_forward_pre_hook(lambda mod, args: (args[0].float(),) + tuple(args[1:]))
s3gen = load_into(S3Gen(), read_sd(find("s3gen")), "s3gen")
ve = load_into(VoiceEncoder(), read_sd(find("ve")), "ve")

tok = None
for name in ("mtl_tokenizer.json", "grapheme_mtl_merged_expanded_v1.json", "tokenizer.json"):
    p = os.path.join(md, name)
    if os.path.exists(p):
        try:
            cand = MTLTokenizer(p)
        except Exception as e:  # noqa: BLE001
            print(f"  skip {name}: {e}")
            continue
        if cand.tokenizer.get_vocab_size() <= n_text:
            tok, tok_name = cand, name
            break
if tok is None:
    raise SystemExit(f"no tokenizer in {md} fits the model's {n_text} text tokens")

conds = Conditionals.load(os.path.join(md, "conds.pt")) if os.path.exists(os.path.join(md, "conds.pt")) else None
tts = ChatterboxMultilingualTTS(t3, s3gen, ve, tok, "cpu", conds=conds)
if a.voice != "builtin":
    tts.prepare_conditionals(a.voice, exaggeration=a.exaggeration)
    conds = tts.conds
if conds is None:
    raise SystemExit("no conds.pt in the model folder: pass --voice clip.wav")
if abs(float(a.exaggeration) - float(conds.t3.emotion_adv.view(-1)[0])) > 1e-6:
    c = conds.t3
    conds.t3 = T3Cond(speaker_emb=c.speaker_emb, cond_prompt_speech_tokens=c.cond_prompt_speech_tokens,
                      emotion_adv=a.exaggeration * torch.ones(1, 1, 1))
conds.t3 = conds.t3.to(dtype=torch.bfloat16 if a.dtype == "bf16" else torch.float32)
UNK = tok.tokenizer.token_to_id("[UNK]")
print(f"model ready in {time.time() - t_load:.0f}s  (tokenizer {tok_name}, {n_text} text tokens, "
      f"voice {a.voice}, {a.dtype})", flush=True)


# ---------------------------------------------------------------- text
def tokenize(text):
    """Token ids, the word index of each text position (SOT .. EOT; -1 = space/punctuation), word count."""
    proc = tok.preprocess_text(punc_norm(text), language_id="ar")  # lowercase + NFKD, as in training
    bad = sorted({ch for ch in proc if ch != " " and tok.tokenizer.token_to_id(ch) is None})
    if bad:
        proc = "".join(SWAP.get(ch, "") if ch in bad else ch for ch in proc)
    full, cmap, w = "[ar]", [-1] * 4, 0
    for ch in proc:
        if ch == " ":
            full += "[SPACE]"
            cmap += [-1] * 7
            w += 1
        else:
            full += ch
            cmap.append(-1 if ch in PUNCT else w)
    enc = tok.tokenizer.encode(full)
    ids, tw = list(enc.ids), [-1]
    for s, e in enc.offsets:
        tw.append(next((cmap[c] for c in range(s, e) if cmap[c] >= 0), -1))
    tw.append(-1)
    unk = sum(1 for i in ids if i == UNK)
    return ids, tw, w + 1, bad, unk


def letters(s):
    return len(re.findall(r"[ء-ي]", TASHKEEL.sub("", s)))


# ---------------------------------------------------------------- one take
def take(text, seed):
    ids, tw, n_w, _, _ = tokenize(text)
    tt = torch.tensor([ids, ids], dtype=torch.long)  # two rows: conditional + unconditional (CFG)
    tt = F.pad(F.pad(tt, (1, 0), value=t3.hp.start_text_token), (0, 1), value=t3.hp.stop_text_token)
    for li in {l for l, _ in LLAMA_ALIGNED_HEADS}:  # drop the last take's attention spies
        t3.tfmr.layers[li].self_attn._forward_hooks.clear()
    torch.manual_seed(seed)
    catch.msgs.clear()
    with torch.inference_mode():
        sp = t3.inference(t3_cond=conds.t3, text_tokens=tt, max_new_tokens=a.max_new_tokens,
                          temperature=a.temperature, cfg_weight=a.cfg, repetition_penalty=a.rep_penalty,
                          min_p=a.min_p, top_p=a.top_p)
        an = t3.patched_model.alignment_stream_analyzer
        toks = drop_invalid_tokens(sp[0])
        toks = toks[toks < 6561]
        if toks.numel() == 0:
            return np.zeros(int(0.2 * SR), np.float32), [None] * n_w, False, list(catch.msgs)
        wav, _ = s3gen.inference(speech_tokens=toks, ref_dict=conds.gen)
    wav = wav.squeeze(0).float().cpu().numpy()
    spans = word_spans(an.alignment.float().numpy(), toks.numel(), tw, n_w)
    return wav, spans, bool(an.complete), list(catch.msgs)


def word_spans(A, n_tok, tw, n_w, jump=4):
    """Monotonic path through the attention map (row k+1 belongs to speech token k), then word spans."""
    rows = A[1:n_tok + 1]
    if len(rows) == 0:
        return [None] * n_w
    L = np.log(rows + 1e-4)
    T, S = L.shape
    dp = np.full((T, S), -1e9)
    bp = np.zeros((T, S), int)
    dp[0, :min(4, S)] = L[0, :min(4, S)]
    ar = np.arange(S)
    for k in range(1, T):
        best, arg = np.full(S, -1e9), ar.copy()
        for d in range(jump + 1):
            cand = np.full(S, -1e9)
            cand[d:] = dp[k - 1, :S - d]
            m = cand > best
            best[m], arg[m] = cand[m], ar[m] - d
        dp[k], bp[k] = best + L[k], arg
    path = np.zeros(T, int)
    path[-1] = int(dp[-1].argmax())
    for k in range(T - 1, 0, -1):
        path[k - 1] = bp[k, path[k]]
    tw = np.array(tw[:S] + [-1] * max(0, S - len(tw)))
    spans = []
    for w in range(n_w):
        P = np.nonzero(tw == w)[0]
        hit = np.nonzero(path >= P.min())[0] if len(P) else []
        if len(hit) == 0:
            spans.append(None)
            continue
        after = np.nonzero(path > P.max())[0]
        k0, k1 = int(hit[0]), int(after[0]) if len(after) else T
        spans.append((k0 * FR, max(k1, k0 + 1) * FR))
    return spans


def tidy(x, spans):
    """Trim both ends (keep 30 ms), shorten long pauses inside the line, and move word times along."""
    win = int(0.01 * SR)
    n = len(x) // win
    if n == 0:
        return x, spans
    db = 20 * np.log10(np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12) + 1e-12)
    voiced = db > max(db.max() - 42, -60)
    idx = np.nonzero(voiced)[0]
    if len(idx) == 0:
        return x, spans
    i0, i1 = max(idx[0] - 3, 0), min(idx[-1] + 4, n)
    cuts, j = [(0, i0 * win), (i1 * win, len(x))], i0
    while j < i1:
        if voiced[j]:
            j += 1
            continue
        k = j
        while k < i1 and not voiced[k]:
            k += 1
        run = (k - j) * win / SR
        if run > a.max_pause:
            drop = int((run - a.keep_pause) * SR)
            s = (j + k) * win // 2 - drop // 2
            cuts.append((s, s + drop))
        j = k
    cuts.sort()
    keep, pos = [], 0
    for s, e in cuts:
        if s > pos:
            keep.append(x[pos:s])
        pos = max(pos, e)
    y = np.concatenate(keep) if keep else x[:0]

    def move(t):
        s_ = t * SR
        gone = sum(min(max(s_ - c0, 0), c1 - c0) for c0, c1 in cuts)
        return min(max(0.0, (s_ - gone) / SR), len(y) / SR)
    return y, [None if sp is None else (move(sp[0]), move(sp[1])) for sp in spans]


def fill(spans, d):
    """Words the alignment never reached get times spread over the gap around them."""
    out, i = list(spans), 0
    while i < len(out):
        if out[i] is not None:
            i += 1
            continue
        j = i
        while j < len(out) and out[j] is None:
            j += 1
        t0 = out[i - 1][1] if i else 0.0
        t1 = out[j][0] if j < len(out) else d
        step = max(t1 - t0, 0.06 * (j - i)) / (j - i)
        for q in range(i, j):
            out[q] = (t0 + (q - i) * step, t0 + (q - i + 1) * step)
        i = j
    clean, last = [], 0.0
    for s, e in out:  # monotonic, at least 60 ms each
        s = max(s, last)
        e = max(e, s + 0.06)
        clean.append((s, e))
        last = s
    return clean


REC = None


def asr(y, text):
    global REC
    if REC is None:
        import sherpa_onnx
        wd = os.path.join(a.tts_home, "asr", "sherpa-onnx-whisper-small")
        REC = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=f"{wd}/small-encoder.int8.onnx", decoder=f"{wd}/small-decoder.int8.onnx",
            tokens=f"{wd}/small-tokens.txt", language="ar", task="transcribe", num_threads=2)
    from scipy.signal import resample_poly
    st = REC.create_stream()
    st.accept_waveform(16000, resample_poly(y, 2, 3).astype(np.float32))
    REC.decode_stream(st)
    hyp = st.result.text.strip()

    def norm(s):
        s = re.sub("[إأآٱ]", "ا", TASHKEEL.sub("", s)).replace("ى", "ي").replace("ة", "ه")
        return re.findall(r"[ء-ي0-9]+", s)
    r, h = norm(text), norm(hyp)
    ops = difflib.SequenceMatcher(a=r, b=h).get_opcodes()
    return sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in ops if op != "equal") / max(len(r), 1), hyp


def make_line(i, line, seed0):
    best = None
    for t in range(a.tries):
        seed, t0 = seed0 + 1000 * t, time.time()
        wav, spans, complete, msgs = take(line, seed)
        y, spans = tidy(wav, spans)
        d = len(y) / SR
        rate = letters(line) / max(d, 1e-3)
        probs = []
        if not complete:
            probs.append("stopped early")
        if sum(sp is None for sp in spans):
            probs.append(f"{sum(sp is None for sp in spans)} words unaligned")
        if not a.min_rate <= rate <= a.max_rate:
            probs.append(f"{rate:.0f} letters/s")
        err, hyp = None, ""
        if a.asr:
            err, hyp = asr(y, line)
            if err > 0.5:
                probs.append(f"Whisper {err:.0%} off")
        forced = [m for m in msgs if "forcing EOS" in m]
        print(f"  L{i:>2} seed {seed:<5} {d:5.2f}s {rate:4.1f} l/s  {', '.join(probs) or 'ok'}"
              f"{'  [forced stop]' if forced else ''}{f'  asr {err:.0%}' if err is not None else ''}"
              f"  ({time.time() - t0:.0f}s)", flush=True)
        score = (len(probs), err or 0.0)
        if best is None or score < best[0]:
            best = (score, y, spans, seed, probs, hyp)
        if not probs:
            break
    _, y, spans, seed, probs, hyp = best
    return y, fill(spans, len(y) / SR), seed, probs, hyp


# ---------------------------------------------------------------- all lines
lines = [l.strip() for l in open(a.lines, encoding="utf-8") if l.strip()]
for i, line in enumerate(lines, 1):
    _, _, _, bad, unk = tokenize(line)
    if bad or unk:
        print(f"  L{i}: the model's alphabet lacks {bad or '?'} ({unk} unknown) - those marks are dropped")
only = {int(x) for x in a.only.replace(" ", "").split(",") if x}
cache = a.out + "_lines"
os.makedirs(cache, exist_ok=True)
settings = [a.voice, a.seed, a.cfg, a.temperature, a.exaggeration, a.rep_penalty, a.min_p, a.top_p, a.dtype,
            a.max_pause, a.keep_pause]
pieces, timing, t, t_all = [], [], 0.0, time.time()
for i, line in enumerate(lines, 1):
    key = hashlib.sha1(json.dumps([line] + settings, ensure_ascii=False).encode()).hexdigest()[:12]
    cj, cw = os.path.join(cache, f"L{i:02d}.json"), os.path.join(cache, f"L{i:02d}.wav")
    saved = json.load(open(cj, encoding="utf-8")) if os.path.exists(cj) and os.path.exists(cw) else None
    if only:
        redo = i in only
        if not redo and saved is None:
            raise SystemExit(f"line {i} has no saved take yet: run once without --only")
    else:
        redo = saved is None or saved.get("key") != key
    if redo:
        seed0 = saved["seed"] + 1 if (only and saved) else a.seed + i
        y, spans, seed, probs, hyp = make_line(i, line, seed0)
        sf.write(cw, y, SR, subtype="FLOAT")
        json.dump({"key": key, "text": line, "seed": seed, "problems": probs, "whisper": hyp, "words": spans},
                  open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    else:
        y = sf.read(cw, dtype="float32")[0]
        spans, probs = [tuple(s) for s in saved["words"]], saved.get("problems", [])
    d = len(y) / SR
    shown = TASHKEEL.sub("", line)
    words = shown.split()
    entry = {"line": i, "start": round(t, 3), "end": round(t + d, 3), "text": shown}
    if len(words) == len(spans):
        entry["words"] = [{"w": w, "start": round(t + min(max(0.0, s0 + a.lead), d), 3),
                           "end": round(t + min(max(0.0, s1 + a.lead), d), 3)} for w, (s0, s1) in zip(words, spans)]
    else:
        print(f"  L{i}: {len(words)} words vs {len(spans)} timed, captions will estimate")
    if probs:
        entry["problems"] = probs
    timing.append(entry)
    pieces.append(y)
    t += d
    if i < len(lines):
        pieces.append(np.zeros(int(a.gap * SR), np.float32))
        t += a.gap

raw = a.out + "_raw"
full = np.concatenate(pieces)
sf.write(raw + ".wav", full, SR)
n_words = sum(len(re.findall(r"[؀-ۿ]+", l)) for l in lines)
voice = "NAMAA Saudi " + ("built-in" if a.voice == "builtin" else os.path.basename(a.voice))
json.dump({"voice": voice, "duration": round(len(full) / SR, 2), "words": n_words, "lines": timing},
          open(raw + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if abs(a.tempo - 1.0) > 1e-6:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", raw + ".wav",
                    "-af", f"atempo={a.tempo}", a.out + ".wav"], check=True)
    for ln in timing:
        ln["start"], ln["end"] = round(ln["start"] / a.tempo, 3), round(ln["end"] / a.tempo, 3)
        for w in ln.get("words", []):
            w["start"], w["end"] = round(w["start"] / a.tempo, 3), round(w["end"] / a.tempo, 3)
    final = sf.read(a.out + ".wav", dtype="float32")[0]
else:
    final = full
final = np.asarray(tts.watermarker.apply_watermark(final, sample_rate=SR), np.float32)
sf.write(a.out + ".wav", final, SR)
dur = len(final) / SR
json.dump({"voice": voice, "tempo": a.tempo, "gap": a.gap, "seed": a.seed, "watermark": "perth",
           "duration": round(dur, 2), "words": n_words, "words_per_sec": round(n_words / dur, 2), "lines": timing},
          open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.out + ".wav",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k",
                a.out + ".mp3"], check=True)
flagged = [e["line"] for e in timing if e.get("problems")]
print(f"{voice}: {len(lines)} lines, {n_words} words, {dur:.2f}s ({n_words / dur:.2f} words/s), "
      f"{time.time() - t_all:.0f}s -> {a.out}.wav" + (f"  CHECK lines {flagged}" if flagged else ""))
if a.verify:
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "verify_vo_ar.py"),
                    os.path.join(a.tts_home, "asr", "sherpa-onnx-whisper-small"), a.out + ".wav", a.out + ".json"])
