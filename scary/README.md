# The Dark Told Me (scary stories)

Scary-story videos, one channel per language: English `@TheDarkToldMe`, Arabic `@TheDarkToldMeAR`.

- Posting: `queue/<slug>-<lang>.json` holds the schedule. The workflow "Scary posts" runs the Yallah Say script
  (`yallah/post_due.py`) with `YALLAH_DIR=scary`, so it reads `scary/config.json` and `scary/queue/` and writes
  `scary/state/`. A post is handed to Buffer about 10 minutes before its time and Buffer publishes it a few random
  minutes later. Off while `config.json` says `"enabled": false`.
- Buffer keys: Actions secrets `SCARY` (English account) and `SCARYAR` (Arabic account).
- Videos are not in this repo. They sit on the Higgsfield CDN; `raw_base` in `config.json` is that folder and each
  queue entry names its file.
- YouTube: Buffer's free plan sends 2 YouTube posts per channel in any 24 hours, so a queue entry lists `youtube`
  in `platforms` only when it is one of those two. The rest go up through YouTube Studio (`/YOUTUBE_STUDIO_UPLOAD.md`)
  once the owner has verified the two channels. The Studio page can fetch these files straight from the CDN link.
- The plan, the format rules and the launch log live in the Claude project "Scary videos".
