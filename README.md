# Build-It posting

Posts the **Congrats, Engineer** (English) and **كيف تبني** (Arabic) episodes to YouTube Shorts, Instagram Reels and
TikTok through two free Buffer accounts, one per language.

- `posts/` — one file per episode: YouTube title, caption + hashtags, and the posting day.
  English goes out at 19:00 New York time, Arabic at 21:00 Riyadh time (`config.yml`).
- `media/` — the videos: `ep01-elevator-en.mp4`, `ep01-elevator-ar.mp4`, ...
- Posting runs by itself on GitHub whenever something in `posts/` or `media/` changes; each post is created once.
- Results: `state/status.md` (refreshed every 3 hours) and `state/last-run.md`.

Keys: Settings → Secrets and variables → Actions → `BUFFER_KEY_EN`, `BUFFER_KEY_AR` (never in a file here).
