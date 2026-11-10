# Night of Nov 9-10 2026 — working notes (read this first after any context reset)

## Where things stand (update the table at the bottom as episodes finish)
- Season 1 (Ep 1-5) is LIVE in English (15/15 posts) and Arabic (15 posts sent 08:50-09:10 UTC Nov 10; confirm with
  the status table in the repo: `state/status.md`).
- The user (asleep since ~00:40 PT) wants Episodes 6-20 (15 new, EN + Saudi) built tonight in the NEW format, stored
  for his review, NOT posted. New episodes therefore have NO file in `posts/` (post texts go to `drafts/`).
- He asked for "30 agents". 15 script agents were launched, then stopped by his interrupt at 00:39 PT. The harness
  says: only start new agents if he explicitly asks again. He was told to reply "go". Until he does: work inline.
  If he says go: one agent per remaining episode, brief = `series/AGENT_BRIEF_SCRIPTS.md` then
  `series/AGENT_BRIEF_ANIMATION.md` (model fable).
- Working alone is fast in wall-clock time (castle: ~15 min); the limit is context. Keep outputs small.

## Recipe for one episode (KIT = kit name), all from /home/claude/kit
1. Script `series/KIT_lines.txt` (14 lines). Several were already polished by the stopped agents and have a recorded
   voice `series/voice/KIT.{json,wav}`: check `diff` between the json texts and the lines file; re-record only if they
   differ: `python3 -I tools/make_vo.py series/KIT_lines.txt series/voice/KIT --tts-home /home/claude/tts --verify`
   (accept only number-format / homophone diffs; target 61.5-66.5 s). Then ALWAYS
   `python3 -I tools/align_words.py series/voice/KIT` and print the word times.
2. Saudi script `series/KIT_lines_ar_sa.txt`: same 14 beats, simple everyday Saudi (الحين، لين، كذا، عشان، مرة، محد،
   موية), no digits, no Latin letters. Line 1 "لو …، مبروك، كذا سويت لك …", line 10 "بس قبل لا …، تابعني، لأن الجاي
   بنبني …", line 13 "ومبروك، كذا سويت لك … بيدك".
3. Scene `episodes/KIT.py` on `episodes/v2_base.py` (pattern: `episodes/castle.py` = one world + several cameras;
   `episodes/rocket.py` = several worlds). Class data: BUILD_NO, FIRST_SET, TITLE, EMPH, KEYS["ar_sa"], TEXT (follow,
   stat, L) in en + ar_sa. `_tracks`: `self.anchors({...})`, `self.cut(t, set, ±1)`, cameras, `self.spans` (4 pairs),
   `self.shakes`. `draw_<set>`, `ui_<set>` (self.label / chip / badge / red / span), `sfx_events`.
4. Check: `tools/slot.sh python3 -I tools/v2_check.py KIT` (one frame per beat), then chosen times
   (`KIT 3.2,7.5 scale=0.34 cols=6 out=out/KIT_a`), read the sheet PNG, fix. Then
   `KIT lang=ar_sa nostills=1` (must say "anchors: all found"), `KIT sweep=0.5`, `KIT lang=ar_sa sweep=1.5`.
5. Copy the files to `/home/claude/test/kit/...`, add `- {slug: epNN-KIT, kit: KIT, look: 2}` to
   `/home/claude/test/episodes.yml`, commit, push, then
   `gh api -X POST repos/Falak-Labs/test/actions/workflows/produce.yml/dispatches -f ref=main -f "inputs[only]=epNN-KIT" -f "inputs[langs]=en,ar"`.
   The run writes `media/epNN-KIT-{en,ar}.mp4`, `review/epNN-KIT/{report.json,qa_en.png,qa_ar.png}` and the Saudi voice
   into `kit/series/voice/`. Read report.json (length 61-70.5 EN / 60.5-80 AR, -14 LUFS, peak <= -0.9, Saudi lines
   flagged by Whisper) and look at the QA sheets.
6. Post texts to `/home/claude/test/drafts/epNN-KIT.yml` (same format as posts/*.yml) — NOT in posts/.

## Framing rules learned tonight
- Portrait frame: zoom in. Ground line at screen y ~1230 means camera y = -270 / zoom. Close shots zoom 1.4-2.0,
  wide beauty shots 0.8-1.05. Captions live at y 1240-1420: nothing important there; cutaways under the ground only
  when the camera is aimed at them (hide them in wide shots).
- Crew (self.crew) must be inside the frame of the current camera; move them per beat.
- Labels need at least ~0.8 s on screen; keep them inside x 40..1040.
- First frame must already show the subject (start the first action at t = 0.1).
- Night overlay at most ~0.26 alpha. Stat cards at y 440: keep the hero below them in the stat shot.
- Arabic: one Saudi word per anchor via KEYS, must appear in that line; no digits in Arabic labels.

## CI / repo
- Repo /home/claude/test = github.com/Falak-Labs/test. `gh api` REST only. Workflows: produce.yml (videos),
  post.yml (schedules what is in posts/), tools.yml (`inputs[cmd]=status|diag|move_up`), status.yml.
- Pages limit 1 GB: new videos ~21 MB each (crf 24, preset medium). Migrate media to release assets later.
- Buffer API: free plan 600 requests/day, 3,000/30 days per account; schema cached in state/buffer-schema.json.

## Episode table (EN voice s = recorded length; A = Saudi script; scene; CI)
| # | kit | EN voice | Saudi script | scene | CI render |
|---|---|---|---|---|---|
| 6 | rocket | 65.6 final | done | done | EN ok (68.7 s, 20.7 MB); Saudi voice made on CI (66.4 s); AR render re-dispatched 09:51 UTC |
| 7 | castle | 66.2 final | done | done | dispatched 09:17 UTC |
| 8 | claw | 65.8 final, aligned | done | done (episodes/claw.py: arcade, 4 cameras; EN mix 0 errors) | dispatched 09:51 UTC en+ar |
| 9 | submarine | 64.9 final (lines 2,3,7 reworded), aligned | done | done | dispatched 10:13 UTC |
| 10 | toilet | 64.9 final, aligned | done | done | dispatched ~10:55 UTC |
| 11 | airplane | 66.9 final (lines 4, 9 trimmed), aligned | done | done | done; Saudi line 13 re-recorded (fix run 11:51 UTC) |
| 12 | fireworks | 64.4 final, aligned | done | done | EN done; AR re-run 11:45 UTC after the limiter fix (was peak -0.7) |
| 13 | vault | 62.3 aligned | done | done | dispatched 11:24 UTC |
| 14 | aircon | 60.5 recorded tonight (quotes removed from line 14), aligned | done | done | dispatched 11:44 UTC |
| 15 | station | 65.9 re-recorded (line 5 reworded), aligned | done | done | dispatched 12:07 UTC |
| 16 | bridge | 65.7 final, aligned | done | done | EN ok 68.8 s; AR ok 65.5 s; AR re-rendered 13:43 UTC (number fix: "من 1937"); Saudi line 14 weak (34%) -> fix run to do |
| 17 | vending | 66.2 re-recorded, aligned | done | done | EN ok 69.4 s; AR ok 70.5 s; voice ok |
| 18 | metro | 66.5 final (quotes removed line 11), aligned | done | done | EN ok 69.6 s; AR ok 66.8 s; AR re-rendered 13:43 UTC (number fix: "لندن، 1863") |
| 19 | dam | 66.9 re-recorded (line 3 trimmed, closer says "a hydroelectric dam"), aligned | done | done | EN ok 70.0 s; AR ok 65.7 s; voice ok |
| 20 | racecar | 65.9 final, aligned | done | done (episodes/racecar.py) | dispatched 13:43 UTC en+ar |

## Notes added 09:55 UTC
- All 30 Season-1 posts are sent (state/status.md shows 30 "sent").
- claw.py is the newest pattern for an INDOOR one-world episode (cutaway of a machine, flights of small objects,
  Track-driven claw). Robust-timing trick for Arabic word order: T["kid0"] = min(two anchors) etc.
- v2_base.label now keeps every label at least 0.85 s.
- Local mix check before pushing: `python3 make.py episodes/KIT.py series/voice/KIT out/KIT audio` then
  `python3 -I tools/verify_mix.py series/voice/KIT out/KIT` (must be 0 errors apart from number formats).
- Front framing for a tall narrow hero: z about 1.2, crew xs (262,300,338), badge at x=975,y=470.

## Notes added ~10:55 UTC
- CI Saudi voice check was cutting Whisper transcripts short (sherpa token limit): fixed by padding 3 s of silence and
  comparing letters (threshold 30%); rate limit now 14.5 letters/s. New workflow input `fix` re-records chosen Saudi
  lines: `-f "inputs[only]=epNN-kit" -f "inputs[langs]=ar" -f "inputs[force]=true" -f "inputs[fix]=6,11"`.
- Local check of a CI-made Saudi voice (after git pull): `python3 -I tools/check_ar_voice.py /home/claude/test/kit/series/voice/KIT_ar_sa`
  (rocket: no weak lines; castle: line 6 weak -> fix run dispatched 10:19 UTC for lines 6,11).
- White things behind the captions: draw a dark plate in ui_<set> (see toilet.py ui_tank).
- English key matching is startswith: "SEA" also matches "SEAL", "S" matches "SO". Use another word or self.w(..., nth=1).

## Notes added 12:08 UTC
- Ep 13-15 built inline (vault, aircon, station); each ~25 min. Remaining: 16 bridge, 17 vending, 18 metro, 19 dam, 20 racecar.
- Mastering now ends with `aresample,alimiter=limit=0.776` (brick wall at -2.2 dBFS): fireworks AR had failed the gate
  at -0.7 dBFS after AAC. Any video that fails with "peak" only needs a re-dispatch.
- Bottom of the frame belongs to the platform UI: in machine close-ups keep the subject in the upper-middle, captions
  under it, nothing important below (aircon.py "unit" view hides couch and crew).
- One world + whip cuts between cameras of the SAME set works (vault.py, station.py "inside"): cut(t, same_name, dir)
  with a camera key of duration 0 at the cut.
- aircon.py has reusable bits: Line (walk a polyline by distance), pipe(), fan(), wisps() (moving air), a room
  temperature pill (thermo) that follows a Track.
- Still to do after the last episode: read report.json + qa sheets for 8-20, check_ar_voice for each Saudi voice
  (done: rocket, castle, claw, submarine, toilet, fireworks OK; airplane line 13 re-recorded), drafts/epNN-*.yml post
  texts, update the project handoff doc, morning report to the user (agents were stopped; Buffer keys to rotate).

## Notes added 14:05 UTC (all 15 scenes written)
- ALL FIFTEEN (6-20) are written, checked and dispatched. Reports read for 6-19: every EN and AR file ok (length, -14 LUFS,
  peak <= -1.1). Mix diffs are number formats / near-homophones only.
- BUG FOUND AND FIXED in bik/arabic.py: a label that mixes Arabic with a multi-digit number was shaped as one right-to-left
  run, so the digits came out reversed ("1937" drawn as "7391"). shape() now lays the label out run by run (numbers and Latin
  words left to right). Only bridge ("من 1937") and metro ("لندن، 1863") had such labels: both AR videos re-rendered with
  force (run 13:43 UTC). Episodes 1-5 (posted) had none. Racecar uses "320 كم/س", "20 شخص", "12 طن", "N زر": fine now.
- Saudi voices measured with tools/check_ar_voice.py: all fine except station line 6 (fix run dispatched 13:57 UTC) and
  bridge line 14 (the year; 34%: fix=14 to dispatch after the forced bridge run ends).
- Draft post texts for 6-20 are in the repo: drafts/epNN-kit.yml (dates 2026-11-11 .. 11-25 proposed: Season 1 all went out Nov 9-10, so no gap). Buffer free plan queues at most 10
  posts per channel: move 6-15 first, 16-20 once some have gone out. To schedule after his
  approval: git mv drafts/epNN-kit.yml posts/ and push (the post workflow reads posts/ only).
- racecar.py reusable bits: car() with parts as 0..1 parameters (wings, halo, nose crumple, paint wipe, stickers, x-ray);
  world that scrolls past a fixed car (self.speed Track -> self.dist_at(t), tiles drawn modulo a period, long periods so the
  kerb does not strobe at 30 fps); hstreaks(); stopwatch(); foil() card; pit crew that runs in (crew_x); custom sounds rev(),
  screech(), gun_snd(), crunch().
- Light subject on a dark, calm background: the first racecar pass had a dark car in front of bright boards and was unreadable.

## Notes added 15:00 UTC (delivery)
- Episode 20 final: EN 69.0 s, AR 68.8 s. The Saudi line 14 was reworded to name the Gulf podium drink (rose water,
  checked: Bahrain, Abu Dhabi and Saudi races use a non-alcoholic sparkling rose-water drink) and re-recorded (fix=14).
- Re-recorded this morning: station line 6 (now 16%), bridge line 14 (the year is heard right now).
- PAGES: deployments timed out once the published repo passed about 900 MB, so new videos were not public. Fixed by
  `_config.yml` (exclude everything but media/) and removing `.nojekyll`; first good deployment 14:59 UTC. Every push
  cancels the deployment in progress: push once, then wait for a successful "pages build and deployment" run.
- Review page for the user: https://claude.ai/artifact/CNbhyzqS3HDGTBVVneyLQG (generator kept only in the session:
  it embeds one thumbnail per build and links to falak-labs.github.io/test/media/<slug>-en.mp4 / -ar.mp4).
- Waiting for his approval. Nothing is in posts/ for 6-20.

## Posting day, Nov 10 (the user approved all 15 at 07:26 PT)
- He asked for one episode every 10 minutes on all six channels, and for no more than 10 posts queued per channel
  at once (Buffer free plan; failed posts count too). posts/*.yml now carry `at:` times and `hold:` lists.
- TikTok, Arabic account: TikTok blocked builds 7, 8, 9 as "potential spam" at a 10-minute rhythm and again at
  40 minutes (7 went through on the retry). 10-15 are parked at 2026-11-20 placeholders; 16-20 held. English TikTok
  took 6-15 with no block (15 posts in 24 h).
- YouTube: unverified channels take 10 uploads per 24 h; 11-17 failed, 18-20 held. Needs youtube.com/verify or a
  re-post from Nov 11 16:50 UTC.
- Buffer API: the EN account ran out of daily allowance at ~18:28 UTC (status polling in post.yml every 30 s for
  8 minutes, several runs). post.yml now checks once.
- New scripts: requeue.py (edit posts, also failed ones, to new times), find_posts.py (diagnostics).
