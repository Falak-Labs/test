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
`specs/sm02.yml` You vs Water (panama, venice, aswan, palmjumeirah). Never reuse a build.

## 1. Pick four builds
- One idea that makes them one fight: an enemy (heat, water, gravity, time, ...) or a place.
- All four must have the SAME Arabic narrator, because the Arabic cut plays the builds' own voices:
  `python3 show/stock.py` lists the builds still free, by narrator (Egyptian: builds 24-40 and the even ones from 42;
  Saudi Mansour: the odd ones from 41, `ar_alt.kits` in voices.yml; Saudi NAMAA: builds 6-20).
  A Saudi episode needs Saudi lines read by Mansour: add the episode's kit to `ar_alt.kits`, and for the closing
  lines copy `series/survivalpromo_lines_ar_sa.txt` to a new kit in Saudi dialect (also in `ar_alt.kits`), then set
  `promo: <kit>` and `or_boss` / `next` in the spec's `ar:` block.
- Level 1 is the whole short cut: put the build with the strongest picture first. The last level's music plays under
  the results card: give it the `ondol` bed.

## 2. Write the spec and the lines
Copy `specs/sm02.yml`. Per level: `kit`, `music` (desert | oasis | arctic | ondol, each used once), `color`, and per
language `world`, `boss`, `sub`, `unlocked`, `stamp` (one or two words: it is stamped in the cold open and on the
thumbnail) and three `chips` (a number, then a label; numbers and units in Latin letters in both languages, because
the big number is drawn with the Latin font). Every number must come from the build's own checked script.
Per language: `chip`, `ribbon`, `ribbon_icon` (see `layout.ICON`), `no_icons` (three), `result_label` /
`result_value` (the joke row on the results card), `emph` (caption words to light up) and `cues` (below).

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
Dispatch `voice.yml` with kit `<id>`, langs `en,ar` (English is free; Arabic costs about 520 ElevenLabs characters).
English: the log must show 0 word errors apart from harmless ones ("tamed the" heard "tame the"); reword and run
again with `langs=en force=true` otherwise. Arabic: `python3 -I tools/check_ar_voice.py series/voice/<id>_ar_sa`.

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
- Shorts to TikTok + Instagram: copy to `media/<id>-<lang>.mp4`, write `posts/<id>.yml` like `posts/sm02.yml`
  (`hold: [en.youtube, ar.youtube]` for good; a fixed `at:` after the full video's publish time; Arabic TikTok text
  without the word YouTube).
- YouTube (the full video and the short): Buffer cannot post a video over 3 minutes and its free plan sends 2
  YouTube posts per 24 hours, which the builds use. Upload in YouTube Studio through the owner's Chrome (Claude in
  Chrome). The steps and the selectors are in `series/NIGHT_NOTES.md` (Nov 21 2026). Switch the account to the right
  channel first and back afterwards. Publishing needs the owner's yes in the chat unless he has given it for that day.
- If his Chrome is not connected: leave the files ready, say so, and do not post the shorts (they promise the full
  video).
