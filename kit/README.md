# Build-It Kit — "Congrats, you just built X" series

Everything needed to make one 65–70 s vertical explainer (TikTok, YouTube Shorts, Instagram Reels — one
cut for all three) with free, open tools: Phonon voice (Apache 2.0), skia drawing, ffmpeg, Poppins (OFL).

```
kit/
  make.py              render one episode end to end: video -> mix -> final MP4 -> QA sheet
  bik/                 the drawing + timing library every episode uses
    core.py            easing, Timeline (beats from the voice JSON), Camera, Track, Steps
    draw.py            rect / circle / poly / gradients / glow / text
    world.py           sky, skyline, ground cutaway, trees, houses, people, rooms, pointing hand
    fx.py              red vignette, flash, check + alert badges, outline, pause icon, FOLLOW pill,
                       confetti, sparks, speed lines, stat badges
    captions.py        word timings from the voice audio + one-word pop captions
    sfx.py             ~30 synthesized sound effects (no samples, no licences)
    mix.py             voice + effects on the timeline, ducking, master to -14 LUFS
    render.py          parallel frame render -> H.264 segments -> concat; stills and contact sheets
  episodes/elevator.py the pilot — copy it to start a new episode
  tools/make_vo.py     script lines -> Phonon voice (Easton) -> timed WAV/JSON/MP3 (+ Whisper check)
  tools/verify_vo.py   transcribe the voice back and count word errors
  series/              the scripts (scripts.txt), voice lines, and voice/ masters (elevator.wav/.json/.mp3)
                       so an episode can be re-rendered without running Phonon again
  fonts/               Poppins (OFL)
```

## The format (never change these)

| Rule | Detail |
|---|---|
| Beats | 14 lines: `hook, break1, fix1, break2, fix2, break3, fix3, break4, fix4, cta, reveal, stat, closer, tag` |
| Hook | "If you … , congrats, you just built a ___." — the simplest possible version, built in the first 3 s |
| Break → Fix ×4 | every break raises the stakes (weight → height → people → power); every fix names 2–3 real parts |
| Second person | "you add…", "your arms quit…", never "engineers" |
| Fake pause | at ~75 % the picture freezes with a pause icon, then "But before you ___, follow, because next we're building ___" |
| Reveal | hide the machine behind something ordinary ("two shiny doors and a little ding") |
| Stat | three-beat number line ("One shaft, twenty floors, zero stairs") with three badges |
| Closer | "And congrats — you just built a ___ yourself." + confetti |
| Comedy tag | one relatable joke line after the closer ("And no, pressing the button ten times won't make it come any faster."): snap-zoom back to a character, a visual punchline, `sfx.womp()`. 3–4 s, every episode |
| Length | ~230 words with the tag → ~66 s of voice → ~70 s video (TikTok rewards need > 60 s; Shorts/Reels take up to 3 min) |
| Look | flat cutaway, one evolving set, camera zooms IN on problems and OUT on wins |
| Colour code | red glow + alert badge = problem, green check = fixed, white outline = the part being named, yellow = emphasis word |
| Captions | one word at a time, Poppins Black, white with black stroke, at y = 1345 (70 %), emphasis words yellow |
| Sound | no music bed; a sound on every action; voice on top; master -14 LUFS, true peak ≤ -1.2 dB |

## Make an episode (the process)

1. **Script** — write the 14 lines in `series/scripts.txt` (one `### NAME` block per episode). Read it aloud:
   each break must be a picture, each fix must be 2–3 nameable parts, and the tag must be a joke people
   recognise from real life (the thing everyone does, the thing that always goes wrong).
2. **Voice** — one line per row in `series/<name>_lines.txt`, then
   `python3 -I tools/make_vo.py series/<name>_lines.txt series/voice/<name> --verify`
   (Easton, tempo 0.96, 0.35 s between lines). Accept only 0 % word errors; if a word is wrong, rephrase
   that line (avoid "…" and "—": the tool turns them into commas anyway).
3. **Scene** — copy `episodes/elevator.py` to `episodes/<name>.py`. Keep the structure:
   * `LABELS` (the 14 beats) and `EMPH` (yellow words),
   * `_tracks()`: word anchors `T["…"] = w(beat, WORD)` → every motion starts on a spoken word,
     `Track`/`Steps` for moving values, `Camera.key(t, x, y, zoom, dur)` for the shots,
   * `draw()` = sky → skyline → world (set, parts, people) → world FX → screen FX → captions,
   * `sfx_events()` = (time, sound, gain dB) for every visible action,
   * `NAME`, `EPISODE` at the bottom.
4. **Look before rendering** — render stills at the busiest moments and read the contact sheet:
   `bik.render.still(scene, t, path)` + `contact_sheet(...)`. Check: subject in the upper 2/3, caption zone
   (y ≈ 1345) not covering the action, every named part visible when its word is spoken, nothing left
   over from an earlier beat.
5. **Render** — `python3 make.py episodes/<name>.py series/voice/<name> out/<name>` (≈ 2.5 min on 2 CPUs).
   Re-render the pilot: `python3 make.py episodes/elevator.py series/voice/elevator out/elevator`.
6. **QA** — the script prints duration, loudness and true peak and writes `qa_sheet.png` (one frame per
   beat, decoded from the final file). Ship only if: duration 61–70 s, -14 ±1 LUFS, peak ≤ -1 dB,
   1080×1920 at 30 fps, and the sheet shows the right picture under every beat.
7. **Post** — same file to all three platforms. Cover frame: the snap/alert moment or the stat badges.

## Setup in a fresh session

```
unzip build-it-kit.zip -d ~ && unzip phonon.zip -d ~/tts/phonon   # phonon-31m-en + phonon-voices
pip install skia-python numpy scipy soundfile pillow ptts sherpa-onnx uharfbuzz --break-system-packages
# Arabic voice only: pip install torch transformers loguru misaki --break-system-packages && pip install --no-deps kokoro
# Saudi voice only: pip install --no-deps chatterbox-tts==0.1.7 && pip install librosa==0.11.0 s3tokenizer \
#   diffusers==0.29.0 resemble-perth conformer==0.3.2 pyloudnorm omegaconf --break-system-packages
# Whisper base.en for the voice check (GitHub release, reachable from the workspace):
#   sherpa-onnx-whisper-base.en -> ~/tts/asr/
```
ffmpeg must be on the PATH. Fonts are in `fonts/`.

## Arabic version (Palestinian) — same picture, second voice

- Script: `series/<name>_lines_ar.txt`, 14 lines in Palestinian Arabic, numbers spelled out as words.
- Voice: Sofelia TTS 82M (Apache-2.0, Kokoro-82M fine-tune, female voice "Eliaa", 24 kHz). Hugging Face is
  blocked in the workspace: the user runs `tools/fetch_sofelia.py` at home and attaches `sofelia.zip`.
  `python3 -I tools/make_vo_ar.py series/<name>_lines_ar.txt series/voice/<name>_ar --speed 1.3 --gap 0.3 --verify`
  Write the Arabic lines WITH vowel marks in colloquial spelling (espeak drops vowels of bare words); the JSON
  and captions get the text without marks, and exact word times from the model's own phoneme durations.
  Setup: torch from PyPI; `pip install --no-deps kokoro` (0.7.16 on Python 3.13) and
  `pip install --no-deps --ignore-requires-python misaki==0.9.4` (its EspeakG2P returns (phonemes, None), which
  the Sofelia frontend expects). The tool remaps the checkpoint's weight-norm keys; without that the model
  loads silently half-initialised and outputs pure noise.
- Check: `tools/verify_vo_ar.py` with multilingual Whisper small (sherpa-onnx release `asr-models`,
  `sherpa-onnx-whisper-small.tar.bz2`); dialect spelling inflates the error rate, so read the transcripts.
- Scene: the episode class takes `lang="ar"`: `AR_KEYS` maps each English anchor word to its Arabic word,
  `EMPH_AR` for yellow words, `TEXT["ar"]` for the FOLLOW pill and stat badges (badges read right to left).
  Captions and labels use `bik/arabic.py` (HarfBuzz shaping, Tajawal font in `fonts/ar/`).
- Render: `python3 make.py episodes/<name>.py series/voice/<name>_ar out/<name>_ar lang=ar`

## Saudi version — NAMAA Saudi voice (male), same picture

- Script: `series/<name>_lines_ar_sa.txt`, 14 lines in everyday Saudi wording (الحين، لين، لا = إذا، كذا،
  للحين، ترى، يادوب). Plain letters, no vowel marks needed; numbers as words.
- Voice: NAMAA Saudi TTS (MIT), a Saudi fine-tune of Resemble AI's Chatterbox Multilingual (MIT), 0.5B,
  24 kHz, CPU only. Built-in voice = the model's `conds.pt`. Do not use the demo Space's reference clip (a
  real person's recording with no license); `--voice clip.wav` only for a voice we have the right to use.
- Get it: Hugging Face is blocked here, so the user runs `tools/fetch_namaa.py` at home (downloads, halves
  t3/s3gen to bf16, packs ~6 parts of 300 MB; 450 MB was refused by the chat, 328 MB worked) and attaches `namaa_saudi.zip.001…`. Unpack into its own folder:
  `mkdir -p ~/tts && cat namaa_saudi.zip.0* > /tmp/namaa.zip && unzip -o /tmp/namaa.zip -d ~/tts` (gives
  `~/tts/namaa-saudi/`).
- Make it: `TTS_HOME=~/tts python3 -I tools/make_vo_namaa.py series/<name>_lines_ar_sa.txt series/voice/<name>_ar_sa --asr --verify`
  About 6 s of CPU per second of speech (8-10 min an episode on 2 cores). Word times come from the model's
  own text-to-speech attention. `<out>_lines/` keeps one take per line: edit a line and rerun, or `--only 3,7`
  for fresh takes of those lines. `--tempo 1.05` if it runs long; `--lead 0.05` if captions feel early.
  Bad takes (stopped early, far too fast/slow, Whisper far off) are redone with another seed automatically.
  The wav carries Resemble's inaudible Perth watermark (marks it as AI-made): keep it.
- Scene: `lang="ar_sa"` uses `AR_KEYS_SA`, `EMPH_SA` and `TEXT["ar_sa"]` in the episode file.
- Render: `python3 make.py episodes/<name>.py series/voice/<name>_ar_sa out/<name>_ar_sa lang=ar_sa`
