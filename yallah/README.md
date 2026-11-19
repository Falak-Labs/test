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
