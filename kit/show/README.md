# The 4-minute show ("Survival Mode")

The owner, Nov 21 2026: "daily 4 mins videos for yt 'ar & en' plus the min short", and "the one you post on ig and tk
post it on yt shorts too". So every day, in English (@congratsengineer) and Arabic (@kef.tenbeni):

| cut | length | goes to |
|---|---|---|
| full | about 4:30 | YouTube as a regular video (over 3 minutes, so it counts toward watch hours) |
| short | about 1:20 | TikTok + Instagram (Buffer) and YouTube Shorts; it ends by sending people to the full video |

One episode = four finished builds told as four game levels. No new animation: `build_show.py` cuts the builds'
final videos and draws the game layer (level cards, a boss health bar that each fix knocks down, "achievement
unlocked", a results card), adds new narration, music and jingles.

Episodes so far: `specs/sm01.yml` Zero Electricity (windtower, falaj, igloo, ondol; English only),
`specs/sm02.yml` You vs Water (panama, venice, aswan, palmjumeirah; Egyptian narrator), `specs/sm03.yml` You vs Gravity
(pisa, machupicchu, operahouse, liberty; the first Saudi episode), `specs/sm04.yml` You vs Time (bigben, towerbridge,
shibam, greatwall), `specs/sm05.yml` You vs the Sun (colosseum, stepwell, louvre, maraya; the first with the English
lines read by J. Ballen: copy its `en:` and `ar:` blocks), `specs/sm06.yml` You vs the Sea (burjalarab, suez, pharos,
barrier). Never reuse a build.

Only v2 builds (`look: 2` in episodes.yml) fit: `build_show.py` cuts a build with its scene file `kit/episodes/<kit>.py`
(the times of its four breaks and fixes, clean pictures for the cold open and the cards). The Seedance builds
(`look: sd`, every build from 76 on except 96) have no scene file, so the show cannot use them until the builder
learns to read `kit/episodes/<kit>_sd.json` + the voice file. After sm06 the Mansour group holds 13 v2 builds
(builds 96-102 were made in the v2 look; hagiasophia is left out: the show rule). Leave out a build that posts as a
build on the episode's own day or later.

## 1. Pick four builds
- One idea that makes them one fight: an enemy (heat, water, gravity, time, ...) or a place.
- All four must have the SAME Arabic narrator, because the Arabic cut plays the builds' own voices:
  `python3 show/stock.py` lists the builds still free, by narrator (Egyptian: builds 24-40 and the even ones from 42;
  Saudi Mansour: the odd ones from 41, `ar_alt.kits` in voices.yml; Saudi NAMAA: builds 6-20).
  From Nov 22 2026 every new Arabic voice is Saudi Mansour (the owner; voices.yml `ar`), so take the four builds from
  the Mansour group and write the 8 Arabic lines in Saudi dialect. The closing lines in Saudi dialect are recorded:
  kit `survivalpromosa`. Copy the `ar:` block of `specs/sm03.yml` (`promo: survivalpromosa`, `or_boss`, `next`);
  voices.yml needs no change. The show's Arabic lines are made at the mean tempo of the episode's four builds
  (`show_tempo` in scripts/make_voices.py; Mansour's builds play at x1.04 to x1.12), so the narrator keeps one pace.
- The builds' final videos come from `media/` or, once retired, from git history. A shallow clone only reaches builds
  retired in its last commits. When `fetch` says a video was never deleted in git history, deepen the history WITHOUT
  the files (seconds, not gigabytes) and let git fetch the eight videos alone when `fetch` asks for them:
  `git config remote.origin.promisor true; git config remote.origin.partialclonefilter blob:none;
  git fetch --filter=blob:none --deepen=400 origin main` (Nov 25: 450 commits reached every build back to 41).
- Level 1 is the whole short cut: put the build with the strongest picture first. The last level's music plays under
  the results card: give it the `ondol` bed.

## 2. Write the spec and the lines
Copy `specs/sm02.yml`. Per level: `kit`, `music` (desert | oasis | arctic | ondol, each used once), `color`, and per
language `world`, `boss`, `sub`, `unlocked`, `stamp` (one or two words: it is stamped in the cold open and on the
thumbnail) and three `chips` (a number, then a label; numbers and units in Latin letters in both languages, because
the big number is drawn with the Latin font). Every number must come from the build's own checked script.
Per language: `chip`, `ribbon`, `ribbon_icon` (see `layout.ICON`; draw a new icon there when the idea needs one, as
`rock`, `flat` and `down` were for sm03, `umbrella` for sm05, `shortcut` and `lighthouse` for sm06), `no_icons` (three), `result_label` / `result_value` (the joke row on the
results card), `emph` (caption words to light up, written exactly as in the line: "والريح", not "الريح") and `cues`.
`shot` / `still` (seconds into the build; optional, per level or inside `en:` / `ar:` when the two hooks differ): the
cold open, the thumbnail and the short's boss flashes show each world from `shot`, the level card's backdrop is
`still`. The default is the end of the hook, which is often a bare start (two floors of a tower, a blueprint): run
`build_show.py <id> <lang> <work> full fetch prep thumb` (it needs no voice; it stops at the plan), look at
`<work>/<lang>/thumbnail.jpg`, and set `shot` to the hook's big picture (first 2 to 6 seconds of the build). When
that picture cannot be read in half a second (sm06's storm barrier: two thin arms on a river, seen from above), take
the build's clearest picture instead, even its problem (the storm pushing the sea over the dike). The middle of each
thumbnail column sits behind the title, so a picture whose subject is high or low in the frame shows best.
Arabic level card: a boss name that ends in a letter with a deep tail (ج ح ع ي) runs into the sub line under it, so
keep that sub shorter than the name (sm06: "الموج" over "كله بحر"); look at the four cards before the long render.

Narration, 8 lines in `series/<id>_lines.txt` and `series/<id>_lines_ar_sa.txt`:
1. Three short sentences ("No boat. No bridge. No dry land."): one icon slams in per sentence.
2. "Just you, and four ..." The four worlds flash from the word named by cue `flash` (default "four" / "أربع").
3. The title line: the ribbon lands on cue `ribbon` ("congrats" / "ومبروك"), the "4 levels" line on cue `sub`.
4-7. One line per level, read over its level card: "Level one. <place>. <the problem in one picture>."
8. The results: the joke row appears on cue `stat`; then the four enemies and the four materials.
The closing lines (three more bosses / watch all four levels on YouTube / subscribe, or the boss wins) are shared:
kit `survivalpromo`, already recorded in both languages.
A cue is the start of a word in the line; if it is not found the builder says so and uses a fixed point in the line.

## 3. Voices
Dispatch `voice.yml` with kit `<id>`, langs `en,ar` and `model=eleven_multilingual_v2`. Both languages are ElevenLabs
now (voices.yml, Nov 23): English is J. Ballen on eleven_v4 (about 850 characters; start each line with one audio tag
such as `[playful]`, `[amused]`, `[proudly]`, `[chuckles]`: they are performed, never shown), Arabic is Mansour (about
600 characters). The `model` input only changes the Arabic: it keeps Mansour on eleven_multilingual_v2, the model of
the v2 builds inside the episode and of the closing lines `survivalpromosa`, so the narrator sounds the same all
through (drop it once the episode's builds are eleven_v4 ones). The English closing lines in Ballen's voice are kit
`survivalpromob` (`promo: survivalpromob` in the spec's `en:` block); inside the levels the v2 builds still play Easton.
Check both with Whisper small (`/home/claude/tts/asr/sherpa-onnx-whisper-small`; if missing, download
`sherpa-onnx-whisper-small.tar.bz2` from the k2-fsa/sherpa-onnx GitHub release `asr-models`, 639 MB, and unpack it there):
`python3 -I tools/check_en_voice.py series/voice/<id>` (only number formats may differ: "one" -> "1") and
`python3 -I tools/check_ar_voice.py series/voice/<id>_ar_sa` (no weak lines). A misread word: reword that line and
dispatch again with `langs=en force=true` (or `langs=ar force=true model=eleven_multilingual_v2`); only the changed
lines are recorded again.

## 4. Build (about 25 minutes for the four cuts on 2 CPUs)
```
cd kit
python3 show/build_show.py <id> en <work> full          # fetch prep thumb audio stills video mux qa copy
python3 show/build_show.py <id> en <work> short audio stills video mux qa copy
python3 show/build_show.py <id> ar <work> full
python3 show/build_show.py <id> ar <work> short audio stills video mux qa copy
```
`<work>` is any folder outside the repo. Look at `<work>/<lang>/<cut>/stills/sheet.jpg` before the long render and
at frames of the finished file after it. QA must say -14 LUFS and a true peak under -1 dBFS, and it prints the
chapter times for the YouTube description. The files to post are `<work>/<id>-<lang>-<cut>.mp4` (under 95 MB) and
`<work>/<lang>/thumbnail.jpg`.

## 5. Post
A scheduled run has no browser, so it cannot upload to YouTube. It hands the episode to the main chat, which uploads
in YouTube Studio at about 16:45 PT (and again at 21:30 PT if needed): YOUTUBE_STUDIO_UPLOAD.md, "The desk".
1. Shorts: copy them to `media/<id>-en.mp4` and `media/<id>-ar.mp4`. Write `posts/<id>.yml` like `posts/sm02.yml`
   (a fixed `at:` after the full video's publish time; Arabic TikTok text without the word YouTube), but with ALL six
   targets on hold: `hold: [en.youtube, ar.youtube, en.instagram, en.tiktok, ar.instagram, ar.tiktok]`. The shorts
   promise the full video, so the main chat takes TikTok and Instagram off hold only after the YouTube uploads
   (`scripts/yt_desk.py release <id>`). The two YouTube targets stay on hold for good.
2. What YouTube shows: write `show/youtube/<id>.yml` (copy `show/youtube/sm02.yml`): the date (TOMORROW in Pacific
   time), six chapter labels per language, and per language the full video's and the short's time, title and
   description. Full: title under 75 characters, a description that opens with the hook, then `{chapters}` on its own
   line (the script fills in the times), then two or three lines of real facts and "Subscribe, or the boss wins."
   Short: a title, two lines that name the full episode, "#Shorts". Times: Arabic full 09:00, English full 10:00,
   Arabic short 10:30, English short 12:15.
3. Commit and push main (media, posts, spec, lines, the youtube file), then `python3 show/handoff.py <id> <work>`
   from `kit/`. It checks the files and the texts, puts the two full cuts, the two thumbnails and the upload sheet on
   the `show` branch, and prints the four videos with their times. `curl -sI` the link it prints: 200.
4. Tell the owner what goes out when, and that YouTube waits for the main chat's upload round.
The Studio steps themselves (for a chat that has the browser) are in the guide at the repo root.
