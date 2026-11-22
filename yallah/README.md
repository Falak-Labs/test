# Yallah Say

Short English lessons for Arabic speakers, one channel per dialect (Moroccan Darija: @YallahSayMa, Palestinian: @YallahSayPa).

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
  18:00, 21:00 and the long lesson 17:00. Write `at` with an explicit offset (Morocco +01:00, Palestine +02:00 in
  winter): the chat sandbox's time-zone data is out of date.
- Instagram and TikTok go through Buffer, handed over just before their time (`post_due.py`). YouTube goes up through
  YouTube Studio in the owner's Chrome, scheduled a day ahead (`/YOUTUBE_STUDIO_UPLOAD.md`); what was uploaded and what
  each channel allows is in `state/youtube.md`. Buffer's free plan sends too few YouTube posts a day for this plan and
  no long videos.
- Voices: one Short is about 825 characters (ma01 806, pa01 843). The plan needs about 10,000 ElevenLabs credits a day.
  `darija/tools/credits.py` (workflow "Darija voice find", tool credits.py) writes what is left to
  `darija/voice/_find/credits.json`: check it before every batch and stop, telling the owner, when it would run out.
