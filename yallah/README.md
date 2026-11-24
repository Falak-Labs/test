# Yallah Say

Short English lessons for Arabic speakers, one channel per dialect (Moroccan Darija: @YallahSayMa; Palestinian: @YallahSayPa on Instagram and TikTok, @YallahSay-Pa on YouTube).

- `kit/page/` the lesson engine (one HTML page that draws any frame of an episode), `kit/tools/` the scripts
  (`gen2.py` script and voice lines, `build2.py` sound track and timeline, `mkpage.py` page folder per dialect,
  `render.sh` + `shoot.py` rendering, checks), `kit/brand/` the logos and their generator.
- Voices: `darija/lines/<episode>.txt` + `darija/voices_<episode>.json`, recorded by the "Darija lesson voice" workflow.
- Posting: `queue/<slug>.json` holds the schedule; `post_due.py` (workflow "Yallah Say posts") hands a post to Buffer
  about 20 minutes before its time and Buffer publishes it a few random minutes later. Off until `config.json` says
  `"enabled": true` and the secrets `BUFFER_KEY_MA` / `BUFFER_KEY_PA` exist.

Format of an episode (75-95 s): a question as the hook, five phrases with a second to think before each answer,
a quiz, the hard word (parts, whole word, a sentence close to home, its meaning, "your turn"), end card.

## Daily plan (the owner, Nov 21 2026)
- Every day, per dialect: 3 Shorts, each to TikTok, YouTube and Instagram (18 short posts a day in all), plus one long
  lesson of about 5 minutes (16:9) on that dialect's YouTube channel only. Every video ends by sending viewers to the
  accounts and the YouTube channel. Posts are public.
- Times (local, in `config.json`): Morocco Shorts 13:00, 18:30, 21:30 and the long lesson 17:00; Palestine Shorts 13:30,
  18:00, 21:00 and the long lesson 17:00. `plan_day.py <day> <short> <short> <short> --long <slug> --write` stamps the
  queue files with these times and their UTC offsets (Morocco is on GMT all year since 20 Sep 2026, so +00:00;
  Palestine is +02:00 in winter, +03:00 in summer) and with each platform's route from `config.json`.
- The owner's rule (Nov 21 2026): ALWAYS TRY EVERY METHOD to post. Each platform has its methods in order in
  `config.json` (`accounts.<dialect>.routes`); when one fails, post with the next, and report to the owner only when
  all of them have failed. `post_due.py --channels` (workflow "Yallah Say posting", `inputs[channels]=true`) saves
  every post's outcome and lists in `state/other-route.md` what Buffer did not get out and the method to try next.
  When Studio refuses an upload, add `youtube` to that video's `platforms` in the queue so Buffer posts it.
- The methods today. Both Buffer accounts hold all three channels since Nov 21 (YouTube, Instagram, TikTok).
  Buffer (`post_due.py`, handed over just before the time): Instagram, TikTok, and YouTube Shorts, but its free plan
  sends only 2 YouTube posts per channel in any 24 hours and no long videos. YouTube Studio in the owner's Chrome
  (`/YOUTUBE_STUDIO_UPLOAD.md`, can schedule a day ahead): the third Short of the day, every long lesson, and
  whatever Buffer failed; what each channel allows is in `state/youtube.md` (the Palestinian channel refused Studio
  uploads on Nov 21 until the owner verifies it). `browser` in the routes means the platform's own site in the
  owner's Chrome, the last resort for Instagram and TikTok; it has not been tried yet.
- Known risk: the planner gives Buffer the first and the last Short of each day for YouTube. Buffer's limit counts
  any 24 hours, so a post that goes out a little earlier in the day than yesterday's can be refused. Watch
  `state/other-route.md` in the first days and, if it happens, alternate the days or hold those posts a minute longer.
- Making a Short: `python3 yallah/make.py <lesson> <ma|pa> <out_dir>` does everything from the script to the checked
  MP4 with the voices already in `darija/voice/`. The workflow "Yallah Say production" runs it on the runner, one
  dialect per machine (`dest=lab` for a test copy on the yallah-lab branch, `dest=media` to publish for posting).
  Tested twice on Nov 22 (UTC) by rebuilding lesson 01 in both dialects: script.js and tl.js came out identical to the
  published build every time; final.wav was identical on three of four machines and differed only by rounding on the
  fourth (another CPU; the two sound tracks correlate at 0.9999). The picture matches the chat sandbox's render at a
  mean similarity (SSIM) of 0.993: only the edge smoothing of shapes and letters differs. A machine draws 15 to 22
  frames a second, so a Short takes 2 to 3 minutes to make and the whole run 4 to 5 minutes.
- A lesson is data: `lessons/<NN>.json` (the hard word, the English phrases both dialects share, and each dialect's
  hook, phrases and home sentence). `lessons/WEEK1.md` is the plan for the first 21 Shorts and 7 long lessons, the
  outline of the 5-minute lesson and what the voices cost. Lesson 01 keeps the closing line it was recorded with;
  new lessons get the default one in `kit/tools/gen2.py`, which sends viewers to YouTube too.
- Voices are recorded once: `python3 yallah/lines.py <lesson> --write` writes the scripts to record (the lesson in
  each dialect, the pupils' lines both dialects share, and once only the fixed lines) and prints the characters each
  will cost; record each script with the workflow "Darija lesson voice" (`inputs[episode]=ma02`, `pa02`, `kids02`,
  and once `macommon`, `pacommon`, `kidscommon`). Lessons 02 and 03 are written and drawn but NOT recorded: the owner
  has not said to spend credits.
- Before the voices exist: `python3 yallah/make.py <lesson> <ma|pa> <out_dir> --dry --sheet` draws the lesson with
  soft tones in place of the voices and makes a sheet of frames to look at.
- A phrase's picture is a kit sticker by name or any Fluent Emoji as `"icon": "fe:<slug>"` (see `lessons/WEEK1.md`).
- Still to build: the 16:9 long lesson, the sheet for the daily YouTube Studio upload, the timers and scheduled tasks.
- Voices: one Short is about 825 characters (ma01 806, pa01 843). The plan needs about 10,000 ElevenLabs credits a day.
  `darija/tools/credits.py` (workflow "Darija voice find", tool credits.py) writes what is left to
  `darija/voice/_find/credits.json`: check it before every batch and stop, telling the owner, when it would run out.

## Checking the words before a lesson is built (the owner, Nov 23 2026: "check always the words and how it says")
1. New lessons set `"slow_take": true`: each voice says the hard word slowly in one take ("Grand... moth... er.", or the
   lesson's own `word.slow`), and make.py cuts it at its pauses into the parts. Parts recorded one by one came out wrong
   (the teacher read "Thur" as "Thursday" and "Kum" as "Kumari" in lessons 4 and 5).
2. After the voices are recorded and before the build, run
   `python3 -I yallah/kit/tools/saycheck.py <NN ...>` (Whisper small.en). Every voice's parts, joined, must be heard as the
   word; anything under "listen to:" gets another slow text (`word.slow`, e.g. "Usu... ally.") and is recorded again.
3. Read every script line once more for sense: the hook asks something the video answers, Darija/Palestinian and Arabic
   lines say the same thing, the English is what a beginner would say.
