# Background music library (Islamic channel)

Voice-only nasheed pads, no instruments, no words. Downloaded on the GitHub runner (workflow "Islamic music find").
Source, licence and check result for every file: `candidates/index.json`.

| File | Track | Use |
|---|---|---|
| nasheed_bg_37 | Background Nasheed 37, I_read_quran (Pixabay) | ok |
| nasheed_bg_27 | Background Nasheed 27, I_read_quran (Pixabay) | ok |
| nasheed_bg_25 | Background Nasheed 25, I_read_quran (Pixabay) | ok (51 s, loop it) |
| nasheed_bg_60 | Background Nasheed 60, I_read_quran (Pixabay) | ok |
| nasheed_bg_sufisama | Nasheed Islamic Background, SufiSama99 (Pixabay) | ok, low hum |
| nasheed_peaceful_reflection | alex-morgan (Pixabay) | rejected: drums |
| nasheed_abdul2025 | abdul2025 (Pixabay) | rejected: percussion and bass |

Licence: Pixabay Content License (https://pixabay.com/service/license-summary/): free for commercial use in videos,
no credit needed. Some uploaders register tracks with Content ID; if a claim comes, dispute it with the track page
link and the licence. Pixabay blocks the runner, so take the direct file link from the track page in a browser and
pass `name=<cdn link>` to the workflow's `pages` input.
