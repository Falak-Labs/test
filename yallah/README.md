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
- Instagram and TikTok go through Buffer, handed over just before their time (`post_due.py`). YouTube goes up through
  YouTube Studio in the owner's Chrome, scheduled a day ahead (`/YOUTUBE_STUDIO_UPLOAD.md`); what was uploaded and what
  each channel allows is in `state/youtube.md`. Buffer's free plan sends 2 YouTube posts per channel in any 24 hours
  and no long videos. Until the Palestinian channel accepts Studio uploads (the owner's verification), its route for
  YouTube is Buffer, so only its first and last Short of the day reach YouTube.
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
