# Sermon style: minimal line-art Islamic shorts

A reusable pipeline that rebuilds the look, voice and sound of the reference sermon short (dark slate background,
thin white line drawings, gold for mercy and red for sin, Arabic headline at the top, one short line underneath)
for any topic, as a 9:16 short (TikTok, Reels, Shorts) and a 16:9 YouTube cut.

First episode: **يتبع الميت ثلاثة** (Sahih al-Bukhari 6514, Sahih Muslim 2960), Egyptian Arabic narration,
hadith quoted in Fusha, about 61 seconds.

## How a video is made

| Step | What happens | Where |
| --- | --- | --- |
| 1. Script | 12 to 16 short lines: a hook, the hadith quoted exactly, Egyptian commentary, a turn, a closing call. One line = one beat on screen. Audio tags such as `[softly]`, `[sad]`, `[passionately]`, `[pleading]`, `[whispers]`, `[pause]` set the delivery. | `islamic/lines/<name>.txt` |
| 2. Voice | GitHub Actions workflow **Islamic voice take** records the whole script as one ElevenLabs take (eleven_v4) with character timings, for one or several voices. Patch mode re-records single lines with several seeds. | `.github/workflows/islamic-take.yml`, `islamic/tools/vo_take.py` |
| 3. Check | Whisper (sherpa-onnx, turbo) reads every take back; any word that comes back different from the script is re-recorded before anything is built. Hadith lines must read back exactly. | `tools/eval_takes.py` |
| 4. Sound | `assemble.py` stretches the pauses (short breaths, long stops after the key lines), adds a small room, lays the bed 15.5 LU under the voice with 5 dB ducking, and masters to -14 LUFS / -1 dBTP. | `tools/assemble.py`, `tools/make_bed.py` |
| 5. Timing | `build_episode.py` turns the word timings and the episode spec (headlines, subtitles, scenes, cue words) into frames. | `episodes/<name>.yml` → `src/data/episode.json` |
| 6. Picture | Remotion renders the composition: `Short` (1080x1920) and `Long` (1920x1080), 30 fps. | `src/` |
| 7. Mux | ffmpeg adds the mix to the silent render (AAC 192k). | see below |

## Commands

```bash
npm install
# sound and timing (after the take is in islamic/takes/<name>/)
python3 tools/make_bed.py work/bed.wav 80 --root C            # drone like the reference
python3 tools/make_bed.py work/bed_air.wav 80 --kind air        # no pitched notes (no-music version)
python3 tools/assemble.py take.wav take.json work/final --bed work/bed.wav \
  --gaps "1:0.7,2:0.9,6:1.2,8:1.3,10:1.2,11:1.3"
python3 tools/build_episode.py work/final/timeline.json episodes/three_follow.yml src/data/episode.json
# picture (REMOTION_CHROME only if Chrome cannot be downloaded, e.g. /usr/bin/google-chrome)
npx remotion studio                                   # live preview, edit and scrub
node tools/stills.mjs Short work/stills 60 600 1200   # quick still checks
npx remotion render Short out/short_silent.mp4 --muted
npx remotion render Long out/long_silent.mp4 --muted
ffmpeg -i out/short_silent.mp4 -i work/final/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out/short.mp4
```

## Look (measured from the reference)

- Background: radial gradient `#18212d` (centre) → `#111a24` → `#05090d` (edges), slow drifting dust, light grain.
- Lines `#dce1e7`, about 3 px at 1080 wide; ground line dimmer. Gold `#f0c75e` with glow for mercy, light and the key word; red `#e5574e` for sin and loss.
- Headline centred at 12.5% of the height (Cairo ExtraBold for colloquial words, Aref Ruqaa Bold for quoted and key words); illustration around 35-45%; one short line at 55%; the bottom 40% stays empty for the app's buttons and captions.
- A new headline about every 3 seconds, a new drawing about every 5; things fade in with a blur and draw themselves on.

## Voice (ElevenLabs)

- Reference narrator: Egyptian colloquial sermon talk with hadith in Fusha, high and animated (median pitch about 187 Hz,
  about 16 semitones of range), short phrases (median 1.6 s), breaths of about 0.55 s and long stops of 1.1 to 1.6 s
  after key lines, rhetorical questions that rise at the end.
- Chosen: **Haz voice - Energetic & Passionate** (`mXovlg4TtTSUsS5BeRYF`), eleven_v4, stability 0.5, similarity 0.75:
  the closest of ten Egyptian voices measured (median pitch 149 Hz, 21 semitones of range, pitch spread 5.3 semitones vs 5.0).
  Calmer alternative: Momen (`x6fvBLXv9YxzoVJQ0wp6`). Fusha channel voice: Suhail (`vRVc2UEclSTO2Z2n6vY5`).
- With eleven_v4, fully vowelled Fusha can be misread (this voice said ويتبقى for وَيَبْقَى); the same line without
  vowel marks read correctly. Write hadith with light or no tashkeel and always run the read-back check.
- Do not clone a real preacher's voice from a clip: use library voices or Voice Design.

## Sound

- Reference bed: a dark ambient drone, root and fifth (C and G) held low with a sad minor second and minor sixth drifting in,
  96% of its energy under 1 kHz, no percussion, no melody; 15.4 LU under the voice, ducked about 6.6 dB while the voice speaks;
  master about -13.7 LUFS.
- `make_bed.py` synthesises an original bed with the same colour (nothing sampled, nothing to license).
  `--kind air` makes a bed with no pitched notes at all, for a channel that avoids music.

## Background library

`library/backgrounds/`: six palettes (slate = the reference, night, teal, indigo, maroon, sand), each as a 12-second seamless
loop and a still, in 9:16 and 16:9. All generated by `tools/make_backgrounds.py`, so they are free to use anywhere.

## Rules for this channel

Authentic sources only, quoted exactly with the reference on screen; no prophet, companion, angel or depiction of Allah;
the Quran is never recited by the AI voice; a person approves every script and every video.

## Licences

Remotion is free for individuals and companies of up to 3 people (a company licence above that). Fonts: Cairo, Aref Ruqaa,
Amiri under the SIL Open Font License. Voice: ElevenLabs (paid plan, commercial use).
