# Build-It: the Seedance style (every build from Nov 24 2026)

Owner, Nov 23 2026 20:32 PT, after the Taipei 101 sample: "We can start making all our next videos like that?
Change the plans to the new one." The cartoon kit (make.py, v2 scenes) is retired for new builds. Every build is
made of real-looking Seedance footage, cut to the narration with `kit/tools/seedance_cut.py`.

## The look
- Full-bleed cinematic footage, slow push-in on every shot, soft vignette, a "But" line gets a short shake + thud,
  a "So" line a whoosh, a low storm/wind bed under the voice.
- Captions: 1-3 words, big, centred at 74 % of the height, the spoken word in gold (#FFC93C). English Poppins Black in
  capitals; Arabic Tajawal Black. Spoken numbers turn into big gold numerals ("660 TONS") via `numbers` in the spec.
- Small letter-spaced title + gold kicker at the top during the hook and the closer. Thin gold progress bar on top.
- Frame 0 is the post cover: "BUILD #N" badge, "CONGRATS, YOU JUST BUILT" + the name (Arabic: "مبروك، كذا بنيت").
- No cartoon HUD, no chips, no labels on things.

## Footage: two Seedance jobs per build (free, unlimited mode on the website only)
Each job: Seedance 2.5, 30 s, 9:16, 720p, Standard, sound off, Unlimited ON, 6 shots × 5 s with hard cuts.
One prompt = style line + six "Shot n (a-b s): ..." sentences. Shot plan, matched to the 14 script lines:

| job A | line | job B | line |
|---|---|---|---|
| A1 the hook picture (the strangest true image of the build) | 1 hook | B1 fix 3 | 7 |
| A2 the place / problem, wide | 2 | B2 break 4 | 8 |
| A3 fix 1 | 3 | B3 fix 4 | 9 |
| A4 break 2 (people feel it) | 4 | B4 tease of the NEXT build (LINEUP N+1) | 10 cta |
| A5 fix 2 | 5 | B5 the real thing proving it (a real event, people watching) | 11 reveal |
| A6 break 3 | 6 | B6 the tag joke, everyday life, funny slow motion | 14 tag |

Lines 12 (stat) and 13 (closer) use a free still from an unlimited image model (GPT Image 2.6 Sunburst is the most
accurate for real landmarks; Nano Banana Pro for posters) with a slow zoom, or reuse the best A shot.
The queue `higgsfield/queue.yml` holds the two prompts per build, written from the LINEUP idea BEFORE the script.
The production run then writes the script so each line fits its shot (look at the clips first). Keep the hook
checklist (claude/build-it-hook-checklist.md, kit/tools/check_hook.py).

## Making the build (production runs, no browser needed)
1. `python3 scripts/ai_media.py get buildit-<kit>-sdA.mp4 kit/out/aishots` (and sdB, and the stills). Missing →
   that build waits; take the next build whose footage is ready (queue status `done`). If NO build has footage,
   make the build in the old v2 look so the day's slots are not empty, and say so in the message.
2. Find the cut points: `ffmpeg -i clip -vf scdet=threshold=10 -f null -` (cuts land near 5/10/15/20/25 s).
   Look at one frame per shot before mapping.
3. Write `kit/episodes/<kit>_sd.json` like `kit/episodes/taipei_sd.json`: build_no, title/kicker/cover_name per
   language (Arabic without Latin letters or Western digits), numbers (EN), shots: one per line {line, src, at}.
4. Voices as before (voice.yml; voices.yml decides the engine).
5. From kit/: `python3 tools/seedance_publish.py epNN-<kit> <kit>` (about 2-3 min per language). It writes
   media/epNN-<kit>-<lang>.mp4, review/epNN-<kit>/qa_<lang>.png, cover_<lang>.jpg and report.json exactly where
   produce.yml would, with the same loudness/peak gates. Look at both qa sheets: right picture under every line,
   Arabic words in reading order. Then add `- {slug: epNN-<kit>, kit: <kit>, look: sd}` to episodes.yml, commit
   media + review, push, and post as before (the Pages deploy check still applies).
Disk: delete kit/out/<kit>_sd_* after publishing.
