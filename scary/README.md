# The Dark Told Me (scary stories)

Scary-story videos, one channel per language: English `@TheDarkToldMe`, Arabic `@TheDarkToldMeAR`.

- Posting: `queue/<slug>-<lang>.json` holds the schedule. The workflow "Scary posts" runs the Yallah Say script
  (`yallah/post_due.py`) with `YALLAH_DIR=scary`, so it reads `scary/config.json` and `scary/queue/` and writes
  `scary/state/`. Off while `config.json` says `"enabled": false`.
- Timing: a post is handed to Buffer up to `lead_minutes` before its time (9 hours) and Buffer publishes it at that
  time plus a few random minutes. So Buffer holds the next hours of the schedule and a late run does not delay a post.
  Keep the lead short enough that no channel has more than 8 posts waiting: Buffer's free plan holds 10 per channel
  and refuses the eleventh.
- What starts a run: GitHub's own timer (the `schedule` in the workflow) runs hours late or not at all in this repo.
  The workflow "Scary clock" waits `clock.every_minutes`, starts "Scary posts", and starts itself again, until
  `clock.until` in `config.json`. Start it once by hand; stop it by cancelling its run. Any chat can also start
  "Scary posts" by hand at any time: a second run sends nothing twice.
- Buffer keys: Actions secrets `SCARY` (English account) and `SCARYAR` (Arabic account).
- Videos are not in this repo. They sit on the Higgsfield CDN; `raw_base` in `config.json` is that folder and each
  queue entry names its file.
- YouTube: Buffer's free plan sends 2 YouTube posts per channel in any 24 hours, so a queue entry lists `youtube`
  in `platforms` only when it is one of those two. The other stories have a `-yt` file, two a day per channel, 24 h
  20 min apart. With the owner's channel verification the rest can go up through YouTube Studio
  (`/YOUTUBE_STUDIO_UPLOAD.md`; the Studio page can fetch these files straight from the CDN link): delete a story's
  `-yt` file first so it is not posted twice.
- TikTok: 15 posts through the API per account in any 24 hours. Stories 16-19 of the launch have a `-tt` file that
  sends them once the first four are 24 hours old. A post refused as "potential spam" is refused on the request, not
  on the video: give it a new queue file (`<slug>-<lang>-tt2.json`, `platforms: ["tiktok"]`) a few hours later.
- A queue file's name is its `slug`, and `state/<slug>.json` records what was handed to Buffer. To send a story again
  to one platform, add a new file with a new slug; never edit a slug that already has a state file.
- The plan, the format rules and the launch log live in the Claude project "Scary videos".
