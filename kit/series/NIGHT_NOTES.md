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

## Nov 11, 18:35 UTC: 80 of 90 Season 2 posts live
- YouTube 11-20 went out on both channels through Buffer, 16:50-18:20 UTC Nov 11 (requeue.py for the 7 failed
  posts per channel, post.yml for 18-20), once 24 h had passed since the last uploads. Unverified channels: 10
  uploads per 24 h each.
- Arabic TikTok 8-15 went out on Nov 11 03:25-03:32 UTC (one a minute, no spam flag); 16-20 were refused by TikTok
  ("large number of posts published through the API ... wait 24 hours": 15 API posts in 24 h) and wait in Buffer
  for Nov 12 04:00-04:40 UTC. English TikTok 16-20: on hold until the user decides.
- The user wants to post from a browser without Buffer. Claude in Chrome connected once (Nov 10 20:50 PT) for five
  minutes: no account was signed in. Videos are served at https://falaklabs.com/test/media/ (github.io redirects
  there). Page scripts can fetch them on youtube.com; tiktok.com and instagram.com block the fetch (CSP). Details
  in the project handoff doc.

## Nov 12, 06:10 UTC: Season 2 fully posted, 90 of 90 live
- Status run 06:10 UTC: 120 of 120 rows "sent" (Season 1 + Season 2), nothing waiting in Buffer, no holds left.
- Nov 12 02:16-02:21 UTC ("publish everything now, use buffer"): English TikTok 16-20 and Arabic TikTok 20 went
  out; Arabic TikTok 16-19 were refused as "potential spam" when sent together.
- The same four passed one at a time, 45 minutes apart (requeue.py): 03:46, 04:32, 05:16, 06:01 UTC.
- Lesson: the Arabic TikTok spam refusal is on the request, not on the video or the daily count. Send, check the
  status once, and requeue a blocked post later; do not send several Arabic TikToks in the same minute.
- Next: Episode 21 "a cruise ship" (Season 3). Before it, shrink media/ on Pages (limit near 900 MB).

## Season 3 (Nov 12): ElevenLabs voices, Egyptian Arabic, three builds a day
- Narrators (voices.yml): English ElevenLabs XA3P1cj7XJexe6Zq0ATX, Arabic ElevenLabs IES4nrmZdUBHByLBde0P, model
  eleven_multilingual_v2, made on the runner by tools/make_vo_eleven.py (secret ELEVENLABS_API_KEY). Takes are saved per
  line in series/voice/KIT[_ar_sa]_lines/ and reused while the text is the same: to change one line, edit it, delete
  only KIT[_ar_sa].json + .wav and run produce again (only the changed lines cost credits).
- The Arabic voice is EGYPTIAN (user, Nov 12 03:37 PT). Write every Arabic script in Egyptian: "لو …، مبروك، كده انت
  بنيت …" / "بس قبل ما …، تابعني، عشان اللي جاي هنبني …" / "ومبروك، كده انت بنيت … بإيدك"; Egyptian words (دلوقتي، عايز،
  أوضة، مية، ساقعة، برة، المكن، طلمبات، كوباية) and Egyptian jokes (build 23: the fish turns into fesikh). Files keep the
  _ar_sa name and lang=ar_sa. KEYS["ar_sa"] must use the Egyptian words.
- Length: ElevenLabs reads slower than Easton/NAMAA; make_vo_eleven speeds up to 1.12 at most. At that cap English runs
  ~3.4 words/s and Egyptian ~2.4 words/s. Keep English to about 225 words (232 gave 71.3 s, over the 70.5 s gate) and
  Arabic to about 165 words (166 gave 72.7 s; the Arabic gate is 60.5-80 s).
- check_ar_voice on the Egyptian takes: weak lines none, 0-23% per line (the high ones are numbers heard as digits).
- Chat bubbles and other text boxes: size them to the text (arabic.width_ar / text_width); a fixed 240 px bubble cut the
  Arabic question in build 22.
- Posting: posts/epNN-KIT.yml may carry `at:` inside each language block (post.py fixed_time(ep, platform, lang)).
  Day slots: English 06:00, 10:00, 16:00 PT; Arabic 09:00, 11:00, 13:00 PT (7, 9, 11 pm Cairo), Arabic TikToks 2 h apart.
  Push a post file only after its videos are committed AND a Pages deployment after that commit ended in success.

## Voices from Nov 12 2026 17:41 PT: English back on free Easton, only Arabic on ElevenLabs
- Owner: "use English voice the free one ... no need to waste money on new voice. So only Arabic use ElevenLabs."
  voices.yml: en {engine: phonon, voice: Easton}, ar {engine: eleven, voice: IES4nrmZdUBHByLBde0P}. Builds 21-23 keep
  their ElevenLabs English (already posted).
- The runner now makes Easton itself: requirements-ci.txt has ptts==0.6.0, ci_models.sh "en" fetches
  gradium/phonon-31m-en and the Easton embedding (gradium/phonon-voices voices/LMDIYE0Oa377Qh6Z.safetensors) from
  Hugging Face, and produce.py runs tools/make_vo.py --verify then tools/align_words.py (word times).
- New workflow "Make voices" (.github/workflows/voice.yml, scripts/make_voices.py): narration only, inputs kit, langs,
  force; commits kit/series/voice/KIT* and prints each voice's length. Make the voices before animating, then check
  the scene with the real timings. Test Nov 13 01:51Z: build 24 English 221 words -> 63.84 s, 0% word errors.
- Credits now: only Arabic, about 950 per build, about 57,000 a month at two builds a day.

## Nov 13 2026 (daily task, first run 02:40 UTC): builds 24 nuclear and 25 aircraft carrier
- Fresh cloud box: pip install skia-python numpy scipy soundfile pillow pyyaml uharfbuzz sherpa-onnx
  --break-system-packages. check_ar_voice needs /home/claude/tts/asr/sherpa-onnx-whisper-small: download
  https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2 (639 MB) and
  extract only "*int8*" and "*tokens*". The GitHub MCP tools (actions_run_trigger, actions_list, get_job_logs) start
  and read the workflows; git push from /home/claude/test works.
- Voices: nuclear EN 221 words -> 63.8 s, AR 160 words -> 66.3 s; carrier EN 224 words -> 62.5 s, AR 166 words ->
  66.0 s (tempo 1.11). Easton's --verify diffs were number formats and "sails" heard as "sales" only.
- nuclear.py (seven sets): Integral() = smooth spin/flow phases from a Track (never t * speed(t)); a chain reaction
  from precomputed split times per atom (rate grows 2x every 0.5 s, then follows the control-rod depth); neutrons
  stop at a control rod they cross; fuel_rod(heat, melt); trefoil(); tower() rises out of the ground; dome_path()
  cross-sections (steel shell + concrete ring); kettle morph of the cooling tower; tea_glass() for the Egyptian tag.
- carrier.py (four worlds): jet_side(), jet_top(), side-view ship in red primer (the reveal paints it gray from
  above), fields() overlay, deck_path(ang) morphs the straight deck into the angled deck, strip(ang) gives the
  landing axis, the caught cable bends into a V at the hook, gas_station() at sea, car() for the parking tag.
- A whip cut to the SAME set hides a reset (site at fix4, top at fix3).
- A callout leader is vertical then horizontal: give the card the anchor's own y (ly = ay) for a flat leader that
  does not cross the subject.
- AUDIO PEAKS (build 25 Arabic failed the gate at +0.1 dBFS true peak): ffmpeg's native AAC encoder's PNS and TNS tools
  made random 2-4 dB inter-sample overshoots on the dense ElevenLabs Arabic voice, after the -2.2 dBFS brick wall; a
  lower limiter did not help (it moved the spike). bik/render.py mux() now encodes with -aac_pns 0 -aac_tns 0 (falls
  back to the old command if an ffmpeg lacks them): the same mixes then measure -1.5 to -2.7 dBFS. Local check of a
  mix: build_mix() to a wav, ffmpeg -c:a aac -b:a 192k -aac_pns 0 -aac_tns 0, then ebur128=peak=true.
- PAGES SIZE: media/ is about 844 MB after build 25 (50 videos). Deployments slow down near 900 MB and timed out
  above it before. BEFORE the next produce run, take the posted Season 1 videos out of media/ (ep01-ep05, 162 MB,
  all 30 posts are live and Buffer no longer needs them): git rm media/ep0[1-5]-*.mp4, commit, push, and wait for a
  successful Pages run.
- Scheduled Nov 13 04:15 UTC, all 12 targets "scheduled" in state/: build 24 AR 17:00Z (09:00 PT), EN 18:00Z
  (10:00 PT); build 25 AR 20:00Z (12:00 PT), EN 00:00Z Nov 14 (16:00 PT). Next: 26 the world's tallest tower (promised
  by 25), 27 tunnel boring machine.

## Arabic voice from Nov 12 2026 20:33 PT: UZbXudn9g5q7bjznYXcC
- The owner switched the Arabic ElevenLabs voice to UZbXudn9g5q7bjznYXcC (voices.yml); it replaced IES4nrmZdUBHByLBde0P.
  Builds 24-25 (posting Nov 13) keep the old voice. A three-line Egyptian sample (kit/series/sample_lines_ar_sa.txt,
  voice/sample_ar_sa.*) checks clean: 3-8% per line, weak lines none. Scripts stay Egyptian until the owner names
  another dialect for this voice. The ElevenLabs key is Text-to-Speech only: GET /v1/voices/{id} answers 400, so the
  voice's labels cannot be read from the runner.
- Make voices: a kit whose name starts with "sample" keeps natural speed (no 59-66 s fitting).
- Nov 12 21:12 PT: the owner did NOT like UZbXudn9g5q7bjznYXcC. He is trying kU20U5bOr9ND3yqlsdwV with a JORDANIAN
  script: sample kit/series/sample_jo_lines_ar_sa.txt (4 lines, 2.42 words/s, 3-14% per line, no weak lines; Whisper
  hears the Jordanian "g" for qaf). Until he approves it, voices.yml is back on IES4nrmZdUBHByLBde0P with
  dialect: egyptian. If he approves: voices.yml ar {voice: kU20U5bOr9ND3yqlsdwV, dialect: jordanian}, and write the
  Arabic in Jordanian ("لو ...، مبروك، هيك إنت بنيت ..." / "بس قبل ما ...، تابعني، لأنه الجاي رح نبني ..." /
  "ومبروك، هيك إنت بنيت ... بإيدك"). Make voices can try any voice without touching voices.yml: input voice=<ID>.

## Nov 14 2026 (daily task, run of Nov 13 18:37 PT): builds 26 tallest tower and 27 tunnel boring machine
- Status 02:40Z: Nov 13 posts 10 of 12 sent. 25 ar.tiktok waited for 04:00Z (requeued the run before); 24 ar.tiktok got
  "potential spam" again at 02:00Z and was requeued to 06:00Z (2 h after 25's).
- PAGES: the posted Season 1 videos are off the site (git rm media/ep0[1-5]-*.mp4, 162 MB). episodes.yml marks them
  `retired: true` and produce.py's plan skips retired episodes, so a run without `only` never remakes them. media/ is
  about 765 MB after builds 26-27 and every build adds about 40 MB. TO DO BEFORE THE NEXT PRODUCE RUN: retire the next
  posted builds the same way (ep06-ep10, about 200 MB: all their posts are live), then wait for a green Pages run.
- Check that `git push` really went through before dispatching a workflow: a post.yml state commit landed between my
  commit and push, the push was refused, and the first voice runs ran on the old main (cancelled, dispatched again).
- Easton read "side to side" as "side to side to side" (both Whisper models heard the repeat). Reworded the line and made
  the English again. Read the --verify diff lines for repeated words, not only number formats.
- The mix check heard "wings" as "wanes": three -6 dB pops sat right on the word. Sounds that land on a key word: -15 dB.
- check_ar_voice flags the all-numbers stat line as weak (68%, 48%) because Whisper writes the numbers as digits; the
  digits were right, so no fix run. Every other line 1-23%.
- New tool: tools/save_check.py <kit> [lang=ar_sa] draws every 0.25 s and reports frames that leave the canvas save
  count changed (a missing restore makes the picture drift without any error). Run it with the sweeps.
- tower.py (desert, ground, plan, sky, pump, lobby): tower() is a stack of 27 tiers with wing (skinny core -> winged),
  step (straight box -> setbacks on alternate sides = the spiral), built, spire, lights; vortex(), crane(), mixer() with
  a turning drum, ice(), pencil(), tripod(), hexagon(), big_arrow(); v2.sky(pal=...) takes a mixed day/night palette.
- tunnel.py (city, face, side, portal): tbm_side() (shield, back-up gear, teeth, packed chamber, name plate),
  tbm_front() (spokes, disc cutters popping in), a Gaussian street trough with tilting houses, the side cutaway scrolls
  the world (rings, stones) instead of moving the machine, phone() with signal bars, portal arch + cell tower arcs.
- Facts (tower = Burj Khalifa): 828 m, 163 floors, 57 lifts (burjkhalifa.ae); 192 piles, 1.5 m x 43 m, more than 50 m
  deep; 27 spiral setbacks against wind vortices; 2,909 stairs (Wikipedia); concrete pumped a record 606 m, poured at
  night with ice in the mix (Putzmeister, Pumps & Systems); spire of 4,000+ t steel built inside and jacked up to over
  200 m (burjkhalifa.ae). TBM: disc cutters, screw conveyor, ring segments, pushing off the lining, earth pressure
  balance (Wikipedia); women's names for good luck, Saint Barbara (ICE); Bertha 17.5 m wide, 99 m long, 6,100 t.
- Scheduled for Nov 14 PT: 26 AR 09:00 (17:00Z), EN 10:00 (18:00Z); 27 AR 12:00 (20:00Z), EN 16:00 (00:00Z Nov 15).
  Next: 28 bullet train (promised by 27), 29 humanoid robot.

## Nov 14 2026 ~00:00 PT: video covers (the owner: "Can't we start having a video cover? ... if someone open my account they can see the video covers you design")
- Every v2 video's FRAME 0 is now a designed cover: the finished build (the world at the middle of the closer beat, no
  HUD/labels/captions), a yellow "BUILD #N" / "البناء رقم N" badge, and "CONGRATS, YOU JUST BUILT" + the name in big
  yellow letters ("مبروك، كده انت بنيت" + name in Arabic). The name is parsed from the closer line ("you just built X
  yourself" / "بنيت ... بإيدك"; a/an dropped), so keep closers in that form. All text sits inside y 240-1680, the 3:4
  middle that TikTok and Instagram profile grids show.
- Code: kit/bik/cover.py (design), EpisodeV2.draw_world() (split out of draw()), draw_cover(), COVER_T (a beat label,
  (label, fraction) or seconds; default ("closer", 0.5); tunnel.py uses ("fix1", 0.6), the cutter head).
  make.py's first step "cover" writes out/cover.png and bik/render.py draws it as frame 0 (BIK_COVER=0 turns it off).
  produce.py keeps review/<slug>/cover_<lang>.jpg and report.json says "cover": true. Look at a cover on its own with
  python3 -I tools/make_cover.py <kit> [lang=ar_sa] [t=<beat or seconds>] (prints whether the text is inside the crop).
- Posting: post.py / requeue.py / move_up.py send assets[].video.metadata.thumbnailOffset = 0 (ms) on TikTok and
  Instagram, so both pick frame 0 as the cover (a post file may set cover_ms). Read back with tools.yml
  cmd=show_assets args="<lang> <slug> ..." (prints Buffer's stored video URL, thumbnailOffset, due time).
  YouTube: Buffer cannot set a Shorts thumbnail through the frame offset (thumbnailOffset stays null); YouTube picks
  its own frame. VideoAssetInput also has thumbnailUrl (a custom image URL): untested; worth a try for YouTube once the
  channels are verified (custom thumbnails need a verified channel).
- Builds 26-27 (already scheduled) were re-rendered with covers (run 43570294697, same lengths and checks) and their
  12 Buffer posts edited at the same times to media/<slug>-<lang>-cover.mp4 (new names so Buffer fetched them fresh;
  show_assets confirmed the URLs and thumbnailOffset 0 on TikTok/Instagram). The old names media/ep26-tower-*.mp4 and
  media/ep27-tunnel-*.mp4 now hold the same covered videos; nothing points at them any more. media/ is about 836 MB:
  retire ep06-ep10 (and drop those four duplicates) BEFORE the next produce run, as noted above.
- Posts made before Nov 14 keep their old covers: TikTok cannot change a cover after posting; Instagram can only in the
  app (Edit > Edit cover).
- Nov 14 01:41-01:42 PT: the owner phone-verified BOTH YouTube channels (screenshots "Phone number verified", the
  blue hard-hat avatar = English, the green one = Arabic). That unlocks YouTube's intermediate features: custom
  thumbnails, videos over 15 minutes, live streaming. The higher daily UPLOAD limit is an advanced feature (channel
  history or an ID check), so keep the "daily video upload limit" requeue rule; two uploads a day per channel stay far
  below it anyway. YouTube covers via Buffer (VideoAssetInput.thumbnailUrl) are still untested; the owner said covers
  on YouTube are "not that important", so only try it if he asks.

## Nov 15 2026 (daily task, run of Nov 14 18:37 PT, three builds a day): 28 bullet train, 29 humanoid robot, 30 self-cooling stadium
- Status 02:40Z: all 12 posts of Nov 14 (builds 26-27) sent; all 162 rows "sent". Metrics 02:42Z: Buffer refreshed only
  English Instagram since Nov 14 morning (the other channels' numbers are stale, see the performance doc).
- The cloud copy was a SHALLOW clone with an old local main (no merge base with origin): fetch, then
  `git reset --hard origin/main` (the working tree was clean).
- PAGES: retired ep06-ep12 (episodes.yml `retired: true`, git rm media) and dropped the four old-named copies
  media/ep26-tower-{en,ar}.mp4 and media/ep27-tunnel-{en,ar}.mp4 (Buffer used the -cover files): media/ 836 -> 517 MB.
  Three builds add about 120 MB a day, so retire about three posted builds per run from now on (next: ep13-ep15).
- Voices: three Make voices runs at once work (the concurrency group is per kit). Easton 63.9 / 63.6 / 65.5 s for
  226 / 228 / 231 words; ElevenLabs Egyptian 69.9 / 68.1 / 69.2 s for 168 / 167 / 167 words (2,710 characters).
  Whisper base.en in the verify step heard "dives" as "dyes" and "built" as "build"; the local Whisper small heard both
  right (a 15-line script: sherpa whisper-small with language="en" on the line's span). Check that way before rewording.
  In the MIX of build 28 even Whisper small heard "dyes" (moving the sounds off the word did not help), so line 7 became
  "which dives into water without a splash": English voice remade (voice.yml langs=en force=true, free) and the English
  video rendered again (produce only=ep28-bullettrain langs=en force=true); the Arabic video was kept.
- A missing `xx += 900` in a while loop made v2_check hang for 10 minutes with no output. When a check seems stuck,
  time one frame per beat with a small script (every frame should take under a second).
- v2.speed_streaks only moves streaks vertically; for sideways speed use hstreaks (racecar.py, copied into bullettrain.py).
- Bright day skies plus the bloom pass wash the whole frame white: keep dusk palettes (stadium.py DAYSKY is dusk) and a
  small sun glow. A translucent effect drawn OVER the stands (the stadium's cool-air bubble) reads; behind them it vanishes.
- Language-specific tag pictures: `if self.rtl:` (humanoid: the fitted sheet in English, the mother sending it for bread
  with the battery dying in Arabic; stadium: the guy in a jacket vs. the mother saying "close the AC").
- bullettrain.py (line, power, map, tunnel, quake, station): train_side(tip, n, k, ...) with k morphing a round nose into
  the kingfisher beak and an x-ray motors overlay, old_train(), fuji(), kingfisher(), bower() (a cleaner who bows),
  gauge() speedometer, board() station clock, Poly (walk a polyline: x, y, angle), train_top() with a derail point,
  an air wave running ahead of the nose through the tunnel, P/S earthquake rings and line-side sensors.
- humanoid.py (lab, sim, hand, road): a front-view robot on two-bone IK (pose()/mixp()/robot()/robot_at()), the backflip
  is a rotation around the pelvis with a tuck pose, falls are rotations around a foot edge, a support zone + weight line
  for the step, run_pose() toward the camera on a perspective road, hand() with curling fingers and fingertip pads,
  egg()/splat(), lantern(), stick() for the push, sheet() for the tag.
- stadium.py (bowl, stands): stands_path()/roof_path(wing) for a cut-open bowl, thermo(), tank(), chiller(), nozzle(),
  puff_air(), lever(), jacket_guy(), mom() (headscarf), bubble(); the stands close-up seats fans on maroon seats with a
  grille under each.
- Facts: Shinkansen 320 km/h (E5, Wikipedia), 16 cars / 1,323 seats (N700), 24 s average delay (JR Central, fiscal 2016,
  nippon.com), kingfisher nose of the 500 Series (Eiji Nakatsu; booms heard 400 m away), UrEDAS stops trains from the
  P-wave (web-japan.org), 7-minute cleaning (Japan Today). Humanoids: years of practice in hours in simulation (Figure),
  tactile fingertips (Optimus Gen 2 egg demo, Unitree Dex3), Beijing half marathon Apr 19 2025: 21 km, Tiangong Ultra
  2 h 40 min, three battery swaps (AP via ABC, Al Jazeera). Qatar stadiums: spot cooling, outlets under every seat and
  nozzles by the pitch, roof edge shaped like a wing, chilled water made at night and stored, air pulled back and
  re-cooled, about 21 C, Khalifa International first in 2017 + six new = seven cooled, 40,000 people = 80,000 laptops of
  heat, switched on two hours before an event (The Athletic, AP via Yahoo, Gulf Times).

## Nov 16 2026 (daily task, run of Nov 15 18:37 PT): 31 wind turbine, 32 space telescope, 33 robot camel jockey
- Status 02:41Z: Nov 15 posts 15 of 18 sent. Requeued: 28 ar.tiktok ("potential spam") to 05:00Z; 30 en.youtube and
  ar.youtube to 03:30Z / 03:40Z (Buffer "An unknown error has occurred. Please retry the post again": first time seen,
  both YouTube posts of the same build, Instagram and TikTok took the same files).
- Metrics 02:55Z: all six channels refreshed; 107,685 views in total. English TikTok's nuclear plant jumped to 7,226
  two days after posting (watched 11%); the humanoid robot was the weakest opener (6% watched on English TikTok).
  Details in the project doc claude/build-it-performance.md.
- PAGES: retired ep13-ep15 (episodes.yml `retired: true`, git rm media): media/ 627 -> 523 MB before today's six
  videos. Next to retire: ep16-ep18.
- Voices (three Make voices runs at once): Easton 62.95 / 67.47 / 64.49 s for 229 / 231 / 226 words; the telescope was
  over 67 s, five lines trimmed to 223 words and English remade (langs=en force=true, free): 66.38 s. ElevenLabs
  Egyptian 66.1 / 66.5 / 66.7 s for 168 / 166 / 165 words (908 + 903 + 903 characters). check_ar_voice: only the
  telescope's all-numbers stat line flagged (45%, Whisper writes digits).
- Local English check with Whisper small (the "15-line script" of Nov 15): sherpa whisper-small, language="en", each
  line's span padded with 0.5 s before and 2 s after, words compared with difflib. Only number formats this time.
- DO NOT run `python3 scripts/post.py --help` locally: it is not a help flag, it runs the posting pass without keys and
  writes state/last-run.md plus empty state/epNN.json for every new post file. Revert those, never commit them.
- turbine.py (farm, foil, top, gear): turbine(c, x, s, ang, air, wk, black, blur, sway, dark, ring) in front view;
  blade_pts(L, air, wk) morphs a flat wooden paddle into a tapered wing (air) and squeezes it edge-on (wk = pitch);
  Spin = integral of a turns-per-second Track (the storm spins up and the feathered rotor stops without jumps);
  far_turbine() silhouettes on two ridges pop in for "a hundred of them"; foil_path(k) plate -> airfoil with
  streamlines that bunch or curve and a LIFT arrow; a top view with eight yaw motors, a wind vane and the rotor drawn
  as three projected blades; gear() and a one-stage gearbox cutaway; eagle(), skyscraper(), house(), desk_fan(),
  comment_card(), mustache_dad() (Arabic tag: the dad switches the house lights off).
- telescope.py (space, light, rocket, focus, map, deep, room): mirror() = 18 hexagons in axial coordinates around an
  empty centre, the two 3-segment side wings fold about their hinges (x' = hinge + (x - hinge) cos a); shield() five
  layers that unfold; giraffe() for scale; wave() a light wave whose wavelength stretches and reddens, dashed where it
  is invisible heat; clamshell fairing halves that swing shut on the folded mirror; the focus board with 18 blurry
  copies that merge into one star with Webb's 6 + 2 spikes; galaxy(), star_spikes(), couch(), mom().
- camel.py (track, scale, road): camel() side view with two-segment legs (Run = integral of a speed Track, the ground
  and rail posts scroll past a camel that stays near x = 0); robot_new() = saddle pad, battery/radio box, antenna, a
  cordless drill spinning a plastic whip, a speaker, a mannequin face with cap and sunglasses, racing silks;
  robot_old(); suv() with the owner in ghutra and agal and a walkie-talkie; scale_dial(), suitcase(), keyfob().
  The gallop thuds are built in sfx_events from the speed Track (about 140 sounds: fine).
- ARABIC STAT CARDS: the big value is drawn in Poppins only, so Arabic letters there come out as boxes ("107 م",
  "300 كم/س", "48 جرام" did on the first render). Keep the big value to digits and symbols ("107", "300", "6.5",
  "1,000,000+", "233°") and put the Arabic unit in the small label ("متر طول الريشة", "كم/س سرعة الطرف"). The three
  Arabic videos were rendered again (produce only=... langs=ar force=true; the voices were reused, no credits).
- The CI mix check (Whisper base.en) heard the telescope's "a mirror" as "a mere"; Whisper small on the same mix heard
  it right (ffmpeg the mp4 to 16 kHz mono, cut the line at voice time + 0.5 s lead). No re-render needed.
- A warm sunset + orange sand + a tan camel washed out under the bloom pass: a navy-to-plum sky, darker sand and a
  dark outline on the animal fixed it. A pale subject on a darker background, as always.
- Facts: wind: GE Haliade-X 107 m blades, one rotation powers a UK home for more than two days (GE); blade tips over
  100 m/s (Hackaday, leading-edge erosion); Smøla, Norway, one black blade = 71.9% fewer bird deaths (Ecology and
  Evolution, via Smithsonian); yaw, pitch, feathering and brakes (scienceinsights.org); gearbox 1:78 on a 1.5 MW
  turbine (Kirkwood); Zafarana on the Red Sea, average wind over 9 m/s (Bibliotheca Alexandrina). Webb (NASA): 6.5 m,
  18 beryllium segments, gold about 100 nm, 48 g in all (Big Think), wings of 3 segments folded like a drop-leaf table,
  6 + 1 actuators per segment, 10 nm steps = 1/10,000 of a hair (Space.com), sunshield 21 x 14 m, five Kapton layers,
  85°C / -233°C, L2 1.5 million km, galaxies more than 13 billion light-years away. Camels: first working robot 2003
  (Qatar Scientific Club), Swiss K-Team robots for Qatar 2004-05 about 25 kg with saddle (swissinfo), later 2-3 kg
  (Wikipedia), cordless drill + whip + two-way radio (Hackaday), mannequin faces, sunglasses, silks and jockeys'
  perfume because the first robots scared the camels (Wikipedia), one SUV per robot beside the track (Scholastic),
  65 km/h bursts, 40 km/h over distance, races 4-10 km, camels over Dh1 million, season October-April (Khaleej Times).
- Scheduled for Nov 16 PT (post run 04:16Z, all 18 targets "scheduled"): 31 EN 06:00 (14:00Z), AR 09:00 (17:00Z);
  32 EN 10:00 (18:00Z), AR 12:00 (20:00Z); 33 AR 15:00 (23:00Z), EN 16:00 (00:00Z Nov 17). Also waiting in Buffer:
  28 ar.tiktok 05:00Z, 30 en.youtube 13:30Z and 30 ar.youtube 16:30Z (the YouTube pair failed twice with Buffer's
  "unknown error"; tools.yml cmd=show_assets showed the same asset as build 29's, which went out). Next: 34 electric
  car (promised by 33), 35 smartphone, 36 the Great Pyramid of Giza.
- Nov 16 13:45 PT status: builds 26-29 6/6 live. YouTube failing on BOTH channels since Nov 15: "unknown error" and, on
  31 ar.youtube, "Buffer has lost authorization to post on your behalf. Please refresh your channel". Likely tied to
  the owner moving his YouTube channels to Brand Accounts. Asked him to reconnect both YouTube channels in Buffer.
  Until he says it's done, don't keep requeueing YouTube; afterwards requeue 30/31/32 youtube (en + ar), spaced.
  Arabic TikTok 31 and 32 ("potential spam") requeued to 01:30Z and 04:00Z Nov 17.
- Nov 16 14:25 PT: the owner reconnected both YouTube channels in Buffer. The six failed YouTube posts of builds 30-32
  went out right away (22:21-22:25Z, Buffer retried them on reconnect). YouTube works again: requeue as usual.

## Nov 17 2026 (daily task, run of Nov 16 18:37 PT): 34 electric car, 35 smartphone, 36 Great Pyramid of Giza
- Status 02:41Z: Nov 16 posts 17 of 18 sent; 32 ar.tiktok went out on its 04:00Z requeue (04:01Z): 198 of 198 "sent".
- Metrics 02:43Z: 118,509 views (+10,824). Buffer has not refreshed YouTube numbers since Nov 15 03:27Z / 05:10Z (the lost
  authorization): YouTube posts of builds 28-33 read 0, not real zeros. Details in claude/build-it-performance.md.
- PAGES: retired ep16-ep18 (episodes.yml `retired: true`, git rm media): media/ 630 -> 529 MB, about 620 MB with today's
  six videos (13-17 MB each). Next to retire: ep19-ep21.
- Voices: Easton 63.95 / 64.96 / 65.1 s for 228 / 226 / 233 words; ElevenLabs Egyptian 67.7 / 66.0 / 69.0 s for 160 / 167
  / 166 words (922 + 912 + 938 characters, plus one pyramid line remade). check_ar_voice: only the all-numbers stat lines
  flagged (digits). Videos: EN 67.1 / 68.1 / 68.2 s, AR 70.8 / 69.1 / 72.1 s, peaks -1.3 to -2.2 dBFS, covers in.
- Whisper small on the first English takes caught: "down the Nile on boats" -> "nylon boats" (now "on boats down the
  Nile"); "Great Pyramid of Giza" in the phone's line 10 -> "Diza" (now "Egypt's Great Pyramid"; the pyramid's own lines
  say Giza fine); "case it in polished white stone" -> "in case it" (now "cover it in"); "gleamed" -> "gleaned" (now "was
  once shiny white"). Arabic: "أقل من عُشر درجة" came back as "10 درجة" (a tenth read as ten): now "كسر صغير من درجة".
  The pyramid English was rendered twice (produce only=ep36-pyramid langs=en force=true after the voice remake).
  The CI mix check (base.en) still writes "Diza" and "an appointed roof"; Whisper small on the MIX hears "Giza" and "and a
  pointed roof" (scratch tool: Timeline(...).s/e per line on the mp4's 16 kHz audio).
- BUG PATTERN: Track.to(t, v, dur) STARTS the move at t. I passed arrival times as t four times (evcar: the car and the
  walker in the crossing, the charge and the dawn): the motion began when it should have ended. Write .to(start, v, dur).
- evcar.py's x-ray set: view() plus an inner save need two restores; save_check caught the missing one.
- A white casing under the bloom pass washed the pyramid into a flat white triangle: casing #CFC2A3 / #7E7464 with faint
  course lines and a weak glint keeps the faces and the cover readable.
- evcar.py (street, xray, cross, garage, uncle): ev_side() (pearl sedan, the front-trunk hood opens on a grocery bag,
  xray mode), sports_car(), traffic_light(), cells() (cells fly from a block into a flat layer), battery_block(),
  cg_mark(), gas_engine() (pumping pistons, sparks, gears), motor() (copper stator, magnet rotor), dash_line() (moving
  dashes along a polyline), pedal(), battery_pill(), speaker_waves() (or a crossed-out speaker), ev_top() + walker_top()
  for a top view of a zebra crossing, window_sky() (night to sunrise), overalls_man() (mechanic with a mustache).
- phone.py (moon, brick, screen, space, night, mom): phone() front view with screen content (cat video, apps, map, dark)
  and an inner(c, sx, sy, sw, sh) callback, content_rot (the landscape fix), a touch grid; cat_face(); lander() (Apollo
  LM); earth(); satellite(); mini_clock(); brick() (the 1973 phone); chip() whose grid gets finer; finger(); rice();
  mems() (a proof mass on springs with comb fingers); pocket(); flower_card() (good-morning picture); mom().
- pyramid.py (giza, sledge, nile, inside, base, shelf): pyramid() two-face view with courses, built 0..1 (stacks from the
  bottom), casing 0..1 and a glint band; palm(); worker() (white kilt); sledge(); small_car() for scale; jar(); a Nile map
  (river_pts/at_river walk the river, boats sail it); boat(); arrow(); a cut through the pyramid with the king's room, five
  relieving rooms and a gable; compass(); level_tool(); books() falling off a shelf.
- Facts: EV: 8,256 cells in a Model S P100D pack (Teslarati teardown); EU AVAS on every new EV since July 2021, sound up to
  about 20 km/h and when reversing (BVRLA); 96% of new cars sold in Norway in 2025 were electric (Reuters and others).
  Phone: Martin Cooper, Apr 3 1973, about 2.5 lb, 10 h to charge, 35 min of talk (AARP); Apollo Guidance Computer 2,048
  words of RAM vs a phone's GBs, a million times and more (Big Think); A17 Pro 19 billion transistors (Wikipedia);
  capacitive grid, gloves don't work (ScienceAlert); MEMS accelerometer smaller than a grain of rice (MakeTechEasier);
  GPS about 20,200 km up, clocks 38 µs a day fast, about 10-11 km a day without the fix; Night Sight merges up to 15
  frames (Google Research). Pyramid (Wikipedia): 146.6 m, about 2.3 million blocks, tallest for 3,800+ years, base level
  to 21 mm, sides about 3.6' off the cardinal directions, Aswan granite 900+ km away, five relieving chambers; wet sand
  halves the pull (Univ. of Amsterdam 2014, Live Science; Djehutihotep painting); Diary of Merer: Tura limestone by
  boat to the Giza harbour.
- Scheduled for Nov 18 PT (post runs 04:05Z and 04:19Z, all 18 targets "scheduled"): 34 EN 06:00 (14:00Z), AR 09:00
  (17:00Z); 35 EN 10:00 (18:00Z), AR 12:00 (20:00Z); 36 AR 15:00 (23:00Z), EN 16:00 (00:00Z Nov 19). Next: 37 a desert
  wind tower that cools a house (promised by 36; Egyptian "ملقف" / Gulf "برجيل"), 38 Petra, 39 Japanese pagoda.

## Nov 17 2026 ~18:15 PT: an empty day, and the fix
- The run of Nov 16 18:37 PT scheduled builds 34-36 for Nov 18 PT instead of Nov 17: it took "tomorrow" from the UTC
  date (18:37 PT is already the next day in UTC). Nothing posted on Nov 17 until the owner asked at 17:59 PT ("I didn't
  see anything posted?").
- Fixed the same hour with requeue (all 18 targets "scheduled" at the new times): English tonight: 34 at 18:40 PT
  (02:40Z Nov 18), 35 at 20:00 PT (04:00Z), 36 at 21:30 PT (05:30Z). Arabic in the Arab morning: 34 at 06:00Z (22:00 PT,
  8 am Cairo), 35 at 08:30Z, 36 at 11:00Z (03:00 PT, 1 pm Cairo). The at: lines in posts/ep34-36 follow.
- So Nov 18 PT is FREE for builds 37-39 at the normal slots (EN 06:00 / 10:00 / 16:00, AR 09:00 / 12:00 / 15:00 PT).
  Arabic 36 goes out at 11:00Z, six hours before Arabic 37 at 17:00Z.
- The daily task's prompt now has a DATES paragraph (TODAY = `TZ=America/Los_Angeles date` at the start of the run; turn
  every at: time back into PT before pushing) and its step 0 goes by state/ (not by the dates in post files) and counts
  what went out today.
- Handoff doc (claude/build-it-series-handoff.md): this is not in it yet. Add these lines to its daily log when you
  update it tonight.

## Nov 18 2026 (daily task, run of Nov 17 18:37 PT): 37 desert wind tower, 38 Petra, 39 Japanese pagoda
- TODAY was Nov 17 PT, TOMORROW Nov 18 PT (checked with `TZ=America/Los_Angeles date` first, and every at: time turned
  back into PT before the push). Status 02:42Z: nothing went out during the day of Nov 17 (the slip of the Nov 16 run);
  English 34 went out at 18:40 PT, the rest of 34-36 follow tonight and early Nov 18 (see "an empty day" above).
  Nothing to requeue. Metrics 02:45Z: 127,679 views; English YouTube Shorts now about 1,100 a build (doc updated).
- The GH_TOKEN for `gh` was invalid in this cloud session: workflows were dispatched and watched with the GitHub MCP
  tools (actions_run_trigger, actions_list, actions_get); git push worked as usual.
- Another project shares the repo: a Darija lessons voice workflow (darija/, other Claude sessions push to main). Pull
  with --rebase before every push; its ElevenLabs use comes out of the same plan.
- Local checks need: pip install skia-python numpy scipy soundfile pillow pyyaml uharfbuzz sherpa-onnx; Whisper small
  for check_ar_voice.py: the GitHub release asset k2-fsa/sherpa-onnx asr-models/sherpa-onnx-whisper-small.tar.bz2
  (640 MB, downloads fine through the proxy), keep only small-{encoder,decoder}.int8.onnx + small-tokens.txt in
  /home/claude/tts/asr/sherpa-onnx-whisper-small.
- Bash calls stop at 10 minutes: run sweeps, save checks and covers as separate calls (two sweeps take ~3.5 min).
- PAGES: retired ep19-ep21 (episodes.yml `retired: true`, git rm media): media/ 616 -> 509 MB before today's six videos.
  Next to retire: ep22-ep24.
- Voices: Easton 64.25 / 64.84 / 69.33 s for 231 / 229 / 232 words: the pagoda was too long (Japanese names and
  numbers read slowly); four lines trimmed to 219 words and English remade (langs=en force=true): 65.68 s.
  ElevenLabs Egyptian 66.0 / 66.0 / 68.6 s for 165 / 166 / 168 words (872 + 860 + 921 characters, one take each).
  check_ar_voice: no weak lines (max 25%, the all-numbers stat lines). Whisper small heard Petra's "1812" right on the
  last 2.2 s of the line (the whole line gave "1882").
- Produce: one slug per run as each scene was ready (37 at 03:25Z, 38 at 03:47Z, 39 at 04:04Z); runs can overlap
  (save_state.sh re-applies files onto a fresh main).
- windtower.py (house, street, top, still, water, ac): house() = a mud house in section with tower_body() on the roof
  (TX0..TX1, openings OPEN0..OPEN1 with the barjeel's wooden sticks, split = a wall down the shaft, heat glow, wet
  cloths), flow() = moving dashes along a smoothed polyline (PathMeasure segment + arrowhead) for air in / out / stack /
  low inflow, thermo() + readout() for 45° outside / 35° inside, a top view of the tower with an X of walls and the
  quarter facing the wind in blue, a limp flag for "no wind", a pool with vapour, town silhouettes for the reveal,
  ac_unit() smoking for the tag. The cover needs the closer camera zoomed out (0.74) so the tower top clears the badge.
- petra.py (cliff, carve, pipe, map, siq, urn): treasury() front view (6 columns, pediment, side pavilions with half
  pediments, the tholos and the urn), carved 0..1 top-down or bottom-up through a clip band, cracks, bullet dents;
  cliff() with striations; tomb() with crow-steps; theater(); chips_fall(); the pipe set (channel cut into the wall,
  clay pipes laid one by one, water running inside); a map (wadi, Siq, dam, tunnel around the city); the Siq view with
  the Treasury glowing at the end; camel riders imported from camel.py (`from camel import camel`); the tag's blue
  cookie tin. The salmon cliff behind a salmon facade had no contrast: ROCK darkened to #9E5646..#3A1A18.
- pagoda.py (temple, quake, xray, eaves, home): pagoda() five storeys (body + upturned tiled roof, eave 0..1 width,
  rot stains, red 0..1 posts, x-ray, the trunk drawn over the floors in x-ray, a 'gone' storey that slides off, nine
  rings on the spire), sway() = the snake dance (alternating offsets) or one rigid lean, fuji() from bullettrain.py and
  mom() from phone.py, skytree() with its glowing core, jenga() and dishes() that topple. Language-specific tag: Jenga +
  "ACHOO!" in English, the dish stack in the sink that falls from mom's look in Arabic.
- Facts: wind tower: up to ~10 °C cooler (Ferrovial; Dubai studies via Matador), barjeel about 5 m above the roof, open
  on four sides, works as a solar chimney with no wind, water sprinkled under it (Bayut), wet cloths on poles (Matador),
  lee-side suction and internal walls (Wikipedia), Yazd about 700 windcatchers, Dowlatabad 33 m (AFP via Al-Monitor),
  ancient Egyptian windcatchers on the house of Nakht (Book of the Dead, 18th Dynasty) and nearly every Cairo house in
  Napoleon's drawings (TheCollector). Petra: Treasury facade 39.5 m, 60 BC-AD 50, bullet marks on the urn from people
  hoping to break it open, Burckhardt 1812 (Petra authority pdtra.gov.jo); top-down carving (Lonely Planet, the
  Unfinished Tomb); pipes from Ain Mousa along the Siq wall, about 20,000 people, a diversion dam and tunnel at the Siq
  entrance (MDPI Water 2020); Siq 1.2 km, 3 m at its narrowest (Wikipedia). Pagoda: only two pagodas lost to
  earthquakes in 1,400 years, Horyu-ji pillar from a cypress felled in 594 (Wikipedia Shinbashira); about a thousand
  mortise joints, almost no nails, storeys sway in alternating directions like a snake dance (web-japan.org Nipponia);
  the pillar stops a storey that swings too far (The Economist 1997, Ishida's shake-table models); wide eaves add
  stability (Wikipedia); Skytree 634 m, a 375 m concrete central column, up to about 50% less shaking
  (gov-online.go.jp).

## Nov 17 2026 ~21:00 PT: six builds a day from Nov 19, new English voice and a richer look on the way
- The owner: "I will pay the Pro" (ElevenLabs Pro, 600,000 credits a month) and "Let's start posting 6 videos a day".
  Two runs a day, three builds each, both for TOMORROW (PT): "Build-It midday production" (11:23 PT, new) takes
  TOMORROW's first three slots, English 06:00 / 08:30 / 11:00 and Arabic 00:00 / 03:00 / 06:00 PT; "Build-It daily
  production" (18:37 PT) takes the last three, English 13:30 / 16:00 / 18:30 and Arabic 09:00 / 12:00 / 15:00 PT.
  kit/series/LINEUP.md is the shared lineup (posting order, line 10 promises, how to add ideas). First six-a-day day:
  Thu Nov 19 (40-42 from the midday run of Nov 18, 43-45 from the evening run of Nov 18).
- ElevenLabs account on Nov 17 (MCP account_get_usage): Creator, 58,098 of 127,949 used, resets Dec 12. Six Arabic
  builds a day is about 5,400 credits a day: Creator alone would run out before Dec 12, hence Pro.
- He is bothered by the English Easton voice: samples of four ElevenLabs English voices go to him tonight; English
  stays on Easton until he picks one (then voices.yml en: {engine: eleven, voice: <id>, model: ...}).
- He wants "some taste": he picked "richer animation" and "cinematic AI shots" (Higgsfield: a 5 s Kling 3.0 clip,
  9:16, no sound, costs about 7.5 credits; Veo 3.1 fast 4 s about 16; Seedance 2.5 720p 5 s about 35; the Higgsfield
  balance was 55.83 credits on the Plus plan). Samples first; keep the v2 look until he approves one.
- Repo size: GitHub reports 2.1 GB for Falak-Labs/test (search API `size`), most of it videos in git history;
  GitHub asks for under 5 GB. Six builds a day add about 250 MB a day: move the videos to GitHub Releases soon.

## Nov 17 2026 ~21:50 PT: the Arabic accounts, by the numbers (the owner asked "do you think we still have a hope for Arabic accounts? I don't feel they are doing good")
- Check-in 21:45 PT: all nine English posts of builds 34-36 are live (34 at 18:40, 35 at 20:00, 36 at 21:30 PT); 37-39
  are "scheduled" on Nov 18 PT at the right times, so the DATES fix worked. Arabic 34-36 go out 06:00Z, 08:30Z, 11:00Z.
- Numbers (metrics of 02:44Z Nov 18, builds 1-33): Arabic 26,069 views, English 101,610 (Arabic is a fifth of the total).
  Arabic Instagram 20,138 (median 195; English median 1,976), Arabic TikTok 4,882 (last eight 113-444, like a typical
  English TikTok, median 184), Arabic YouTube 1,049 (median 10; two at 256 and 312; English Season 3 about 1,000 each).
- Arabic Instagram is two-level: a video gets either about 150-250 views or 1,200-2,400. Builds 1-20 (Saudi voice, all
  sent on Nov 10, the account's first day): 8 of 20 took off (pool, waterslide, claw, submarine, toilet, vault, aircon,
  bridge), 17,417 views. Builds 21-33 (Egyptian voice and #مصر tags, 2-3 a day): 1 of 13 (the Qatar stadium, 1,248),
  2,721 views, and three got only 6-10 views (data center, nuclear, tower). Arabic/English ratio per build on Instagram:
  median 0.74 in Season 2, 0.09 since build 21, while English Instagram went UP. Not known which change did it: the
  dialect and tags, the topics (heavy machines), or the first-day batch.
- Told the owner: there is hope (TikTok recovered, YouTube is waking, nine Instagram videos passed 1,200) but Arabic is
  behind; proposed a test of a Gulf-dialect ElevenLabs voice against the Egyptian one for a few days, Arab-world and
  everyday topics for Arabic, and a decision on Dec 1. NOTHING is decided: keep Arabic exactly as voices.yml says until
  he answers. Evening run: carry these numbers into claude/build-it-performance.md with your next entry.

## Nov 17 2026 ~22:40 PT: second daily run created, voice and style samples sent
- Scheduled tasks: "Build-It midday production" (trig_01ALubp472TNeQtwzvYgGG9A, 11:23 PT daily, first run Nov 18 for
  Nov 19's first three slots) and "Build-It daily production" (trig_018LnswgiUywWnrkauA1Ujhd, 18:37 PT, last three).
  Both prompts point at LINEUP.md, which now has a claim rule: mark the three entries you take "(taken: midday|evening
  run of <date>)" and push LINEUP.md right away, so the two runs never make the same build.
- English voice samples (owner to pick one): scripts kit/series/sample_{brian,liam,todd,dan}_lines.txt (pyramid lines
  1, 2, 3, 10, 12, 13, 14), voices kit/series/voice/sample_*.{wav,json,mp3}. make_voices.py: the `voice` input of
  Make voices now also applies to English when the kit name starts with "sample". IDs: 1 Brian nPczCjzI2devNBz1zQrb
  (premade, deep narrator), 2 Liam "Viral Short-Form Storyteller" VCgLBmBjldJmfphyB8sZ (library), 3 Todd "Clear,
  Engaging and Educational" g14YnDYCsy3k7XLlcKlO (library), 4 Dan XA3P1cj7XJexe6Zq0ATX (builds 21-23). Library voices
  work over the API on a paid plan without adding them. All four were clean in Whisper small (number formats only).
- At natural speed these voices read 3.1-3.3 words/s (117 words = 35.6-38.2 s), slower than Easton: with an ElevenLabs
  English voice keep scripts to about 205-215 words (make_vo_eleven speeds up 12% at most to fit --max 66 s).
  When he picks: voices.yml en: {engine: eleven, voice: <id>, model: eleven_multilingual_v2}; about 1,300 credits a build.
- Look 3 proposal (sample only, production stays on v2 until he approves): bik/v2.py Post3 (film grade, warm halation,
  god rays from post.light, dust, breathing camera) and helpers tex()/texture() (tileable sand, stone, grain, cloud),
  soft_shadow(), tile_noise(); sample scene episodes/pyramid3.py (not in episodes.yml) = build 36's opening in golden-hour
  light with textures, cast shadows, haze, rim-lit palms, a glittering Nile. Lessons from the first pass: bright flat
  areas + bloom + rays wash the frame out; keep mid-tones darker, bloom threshold 0.74, rays only from the sun's glow.
  Speed: after blurring the bloom levels at low resolution (no image filter on the scaled-up draws) Post3 takes about
  0.33 s a frame against 0.54 s for v2's Post; a whole look-3 frame of the sample is about 0.9-1.0 s (v2 0.6-0.7 s),
  the extra being the textures on big areas.
- Sent to the owner (~22:20 PT): deliver files before_after_pyramid.mp4 (current left, new right) and
  new_look_pyramid.mp4, 17.5 s each, narrated by Brian for lines 1-3 (a hybrid voice: sample lines 1-3 + build 36's
  lines 4-14, made by a scratch script). He was asked for: voice 1-4, new look yes/no, AI shots yes/no.
- IF HE APPROVES THE NEW LOOK: set `LOOK = 3` in the scene class (EpisodeV2 then finishes with v2.Post3). In every
  draw_<set>: self.post.light = (screen x, y) of the key light (sun, lamp), self.post.rays 0.3-0.7 when that light is
  in or near the frame, self.post.dust 0.5-0.9 outdoors / in workshops (0 underwater or in space). Paint big surfaces
  with tex(c, path_or_rect, "sand" | "stone" | "grain" | "cloud", scale, a) (overlay blend; it moves with the world),
  cast shadows with soft_shadow(c, points, a, blur), contact shadows under everything that touches the ground, haze
  between far and near layers, a rim light on silhouettes, darker mid-tones (no big bright flat areas: they bloom).
  Reference: episodes/pyramid3.py (plateau, foreground, pyramid3, palm3).
- AI shots: Kling 3.0 pro, 5 s, 9:16, no sound = 8.75 Higgsfield credits (std 7.5, Kling 2.6 5.0, Seedance 480p 15).
  Two sample clips were made for the pyramid (jobs b8f74f06-0cf1-467d-82e0-1a0d7745db71 hook, dd1dfecb-5302-4ac6-be1f-
  0c814dcb0ce7 sledge and water); balance after: about 38 credits on Plus. This session's network policy refuses
  Higgsfield's file host (d8j0ntlcm91z4.cloudfront.net), so the clips cannot be checked or mixed into videos here.
  Do not fetch them any other way: mixing AI shots needs the owner to allow that host, or another decision from him.
- Nov 17 22:10 PT: the owner asked for "a couple samples of gulf voice". Sent three Saudi (white dialect) ElevenLabs
  library voices reading five wind-tower lines in Saudi dialect (kit/series/sample_gulf_a/b/c_lines_ar_sa.txt, Make
  voices with the voice input, eleven_multilingual_v2): 1 Mansour 5HAezIQAaoSgJypcI0NP, 2 Raed lBgZD85rJJVmqahd7yzK,
  3 Adam iw6tHUyMo0UfbjntW0h3. 31-33 s for 71 words (about 2.2 words/s), check_ar_voice 1-7% per line, no weak lines,
  qaf read as "g". Library voices work with the API key directly on his paid plan. About 1,200 credits. Waiting for
  his pick; voices.yml stays on the Egyptian voice until he says. Saudi frames, as in Seasons 1-2: "لو ...، مبروك، كذا
  سويت لك ..." / "بس قبل لا ...، تابعني، لأن الجاي بنبني ..." / "ومبروك، كذا سويت لك ... بيدك".
- Nov 17 22:15 PT: the owner picked Gulf voice 1 (Mansour 5HAezIQAaoSgJypcI0NP). A/B test set up: voices.yml ar_alt
  (Saudi dialect, kits list) + make_voices.py uses it for kits listed there; LINEUP.md rule: odd builds from 41 get
  Mansour with a Saudi script, even builds stay Egyptian (IES4nrmZdUBHByLBde0P). Builds 37-40 are unchanged. Decision on
  Dec 1: compare Arabic views per voice (metrics.json), keep the winner. Record each voice per build in performance doc.
- The two run prompts (last changed Nov 17 ~21:40 PT) were written before the Arabic A/B test and name only the
  Egyptian and Jordanian frames. Follow LINEUP.md and voices.yml `ar_alt` anyway: every odd build from 41 gets a Saudi
  script and Mansour (add the kit to ar_alt.kits and push before its voice is made); even builds stay Egyptian.
  (Changing a scheduled task's prompt needs the owner's OK in a chat turn; a scheduled run cannot do it.)

## Nov 18 2026 (midday run, 11:23 PT): 40 Panama Canal locks, 41 Dutch storm barrier, 42 Venice (first six-a-day day)
- TODAY Nov 18 PT, TOMORROW Thu Nov 19 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT before
  the push). PST from Nov 1: 00:00 / 03:00 / 06:00 PT = 08:00Z / 11:00Z / 14:00Z; 06:00 / 08:30 / 11:00 PT = 14:00Z /
  16:30Z / 19:00Z.
- Status 19:26Z: Arabic 35-36 (00:30, 03:00 PT) and English 37-38 (06:00, 10:00 PT) all live; Arabic 37 Instagram and
  YouTube live, its TikTok "potential spam" at 17:00Z -> requeued to 02:00Z Nov 19 (18:00 PT Nov 18): 3 h after Arabic
  39's TikTok (23:00Z), 6 h before Arabic 40's (08:00Z). The evening run's step 0 should see it "sent".
- Pages: retired ep22-ep24 (all sent): media/ 609 -> 507 MB before today's six videos (about 105 MB). Next: ep25-ep27.
- A/B test: 41 is odd -> `barrier` added to voices.yml ar_alt.kits (Mansour, Saudi script). scripts/produce.py now
  applies ar_alt too (before, any Arabic voice produce.py had to make, or a `fix` run, used the Egyptian voice).
- Voices: Easton 66.41 / 64.93 / 66.26 s (227 / 232 / 225 words; Venice was 67.02 s at 228 words, trimmed and remade).
  ElevenLabs (one take each, 961 + 868 + 920 characters): Egyptian panama 71.57 s (166 words) and venice 68.68 s
  (165), Mansour barrier 68.63 s (155 words). All three hit make_vo_eleven's 12% speed-up cap (tempo 1.12): Mansour
  reads about 2.0 words/s, so keep Saudi scripts near 145-150 words; Egyptian 165 words lands at 69-72 s.
- Whisper small on the first English voices misheard "riverbed" (river but), "tonnes an arm" (tons in arm), "rots"
  (rods) and "Istrian" (history and): reworded ("to the bottom", "per arm", "goes rotten", "hard white stone").
  check_ar_voice: no weak lines; the Saudi lines over 10% (barrier 9 and 12) are digits only (Whisper writes numbers).
- Scenes: panama.py (canal = side view of the staircase, levels(u) gives every chamber's water and the ship for climb
  progress u 0..3, gate_closed(); map of the Americas with the long way round; dam; lock = one chamber in section with
  the culvert, floor holes, a crossed-out pump and a bath duck; gate = one leaf = 400 cars, x-ray hollow cells, then the
  two leaves from above closing into a V; mules = top view, ship_top(), mule()); barrier.py (river/dam/docks from above:
  arm_pose(swing) turns each arm 90 degrees about its ball joint J, gate_arm() draws truss + curved gate; surge and sink
  in section; tag: riders on old bikes in English, the dallah and the desert in Arabic); venice.py (city cut open:
  palaces on pile forests, tree() flips into a pile, the Rialto arch, carbody() -> gondola; mud with the drop-weight
  rig and singing crew; deep with the rock far below and the spiral of pile heads from above; rot; wall with bricks
  that soak up salt, sawn piles, boards and the stone band; cafe with the folded napkin).
- Lessons: Track.to(t, v, dur): dur is the length of the move; dur 0 jumps (the first hook climb sat still).
  v2 has no splash(): use splash() from v2set (v2_base imports it). Bright yellow facades bloom white in v2's Post:
  keep big flat areas mid-tone (Venice facades were darkened). A glyph like the subscript 2 or an arrow may be missing
  in Poppins: write "O2", avoid arrows.
- Produce: one slug per run as each scene was ready (40 at 20:21Z, 41 at 20:28Z, 42 at 20:35Z).
- Videos: 40 EN 69.5 s / AR 74.7 s, 41 EN 68.0 / AR 71.7 (Mansour), 42 EN 69.4 / AR 71.8; -14 LUFS, peaks -1.7 to
  -2.2 dBFS, covers in. Whisper small on the English mixes: number formats, plus Easton's "in dry docks" -> "and dry
  docks" and "gate bobs" -> "gatebods" in 41 (captions carry the words; left as is). All 18 targets "scheduled" for
  Thu Nov 19 PT (state/ep40-42 checked by turning every dueAt back into PT).
- Arabic 38 TikTok got "potential spam" at 20:00Z: requeued to 05:00Z Nov 19 (21:00 PT Nov 18), 3 h from Arabic 37's
  requeue (02:00Z) and 40's (08:00Z). Arabic TikTok is refusing about one post a day: keep 3 h between Arabic TikToks.

## Nov 18 2026 (evening run, 18:37 PT): 43 Great Wall of China, 44 Omani falaj, 45 Machu Picchu (for Thu Nov 19)
- TODAY Nov 18 PT, TOMORROW Thu Nov 19 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT before the
  push). PST: Arabic 09:00 / 12:00 / 15:00 PT = 17:00Z / 20:00Z / 23:00Z Nov 19; English 13:30 / 16:00 / 18:30 PT =
  21:30Z Nov 19 / 00:00Z / 02:30Z Nov 20.
- Status 02:40Z: English 37-39 all live; Arabic 35-36 and 37-39 Instagram + YouTube live. Arabic TikTok refused all three
  of the day ("potential spam": 37 twice, 38, 39). 38 waits for 05:00Z Nov 19; 37 and 39 requeued to 02:00Z and 05:00Z
  Nov 20 (one requeue call can carry several slug=time pairs). With seven Arabic TikToks a day from Nov 19 (05, 08, 11,
  14, 17, 20, 23Z) the only 3-hour gaps left are at night UTC: put refused Arabic TikToks at 02:00Z / 05:00Z.
- Pages: retired ep25-ep27 (all sent): media/ 619 -> 515 MB before tonight's videos. Next to retire: ep28-ep30.
- A/B test: 43 and 45 are odd -> `greatwall` and `machupicchu` added to voices.yml ar_alt.kits (Mansour, Saudi scripts);
  44 falaj is Egyptian.
- Voices: Easton 64.6 / 65.6 / 70.1 s at first (226 / 224 / 226 words): Machu Picchu was too long (the name, Pachacuti,
  "fourteen fifty"); trimmed to 215 words -> 65.8 s. Whisper small then caught "Ming" -> "main" (twice, even as "the Ming
  dynasty": now "Centuries later, it's rebuilt in brick"), "in sight of" -> "inside of" (now "that can see each other"),
  "so gently sloped" -> "slope", "wells sixty" -> "while 60", "so well hidden" -> "so while hidden". English remakes are
  free: langs=en force=true. Final: greatwall 65.2 s, falaj 65.5 s, machupicchu 65.8 s.
  ElevenLabs one take each (Arabic): Mansour greatwall 66.0 s (157 words, tempo 1.04: faster than barrier), Egyptian falaj
  68.6 s (168 words, 1.12 cap), Mansour machupicchu 68.5 s (159 words, 1.12 cap). check_ar_voice: no weak lines except
  the digit lines (greatwall 12 at 34%, falaj 12 at 31%); "ماتشو بيتشو" is heard as "ما تشو بيتشو"-like (name only).
- A Make voices run hung 20+ minutes in apt-get ("ffmpeg and the libraries Skia needs"): cancel it and dispatch again.
- Scenes (all three on v2_base, look 2):
  - greatwall.py (ridge, plain, gobi, mortar, beacon, chat): crest(x, seed) sine crests for three parallax ranges,
    wall_on(c, fn, x0, x1, u) draws a wall along any crest function (band, lit walkway, merlons, shadow), tower() with
    arched windows and a beacon fire, smoke_col() = v2.smoke columns (n columns for "five smokes"), horse() galloping
    rider with banner (rear for the cliff), house_cn(), tent(), bowl() of rice soup, earth_globe() with a >180 degree
    arc, wok(), crystals() magnifier (loose vs packed), phone_chat() for the tag, wolf_icon(). The beacon relay timing
    adapts (dt_relay) so the last tower lights before "one smoke".
  - falaj.py (oasis, section, dig, aerial, share, bath): channel() side view of the stone channel with a flow front,
    mouth(), mudhouse(), fort_tower(), section with surf(x) plain + aquifer band + mother well + tunnel_pts() and
    windtower.flow() for the water, dig set with pick_digger() + timer() + lit shafts + windlass()/basket(), an aerial
    set (dotted line of shaft mounds + plane), share set with gates that open one at a time + sundial() + night stars,
    door_queue() for the tag (bathroom at 7 a.m.). Imports palm (pyramid), flow/sun/heat_lines/arrow/plug_off
    (windtower), pump (panama).
  - machupicchu.py (city, slope, layers, water, quake, stones, ac): huayna() peak, front_terraces() = the terraced slope
    seen from the front (grey wall bands + green steps, widening downward) - this is what makes it read as Machu Picchu;
    side-view terraces did not show at all. house() stone houses with a side face, trapezoid door, thatched gable.
    gauge() rain tube with a person for scale, helmet() for "the Spanish never found it", ashlar_stones() polygons,
    a trapezoid doorway, window_ac() + facade() for the tag.
- Framing lessons tonight: put the ground at screen y ~1000-1150 (camera cy so that (0 - cy) * z + 960 lands there),
  never in 1240-1420; when a section diagram is wider than the frame, pan along it (well -> village -> wide) instead of
  zooming out to 0.4; fill everything under a close-up set (a sky gradient left under a wall shows a bright band).
- falaj's first produce run was cancelled to render it again with a closer closer shot (bigger channel on the cover).
- Machu Picchu was rendered three times: the hook's "knife-edge" came out as "9th edge" in Whisper small on the mix.
  Moving the whoosh and lowering the rain hiss (-10 -> -20 dB) did not change Whisper small (the voice alone reads
  right, CI's base.en reads the final mix right): Easton's "knife" is just borderline. Accepted; the caption shows
  KNIFE-EDGE. make.py <scene> <vo prefix> <out> audio builds only the mix locally: test effect changes that way first.
- Final videos: 43 EN 68.3 / AR 69.1 s, 44 EN 68.6 / AR 71.7 s, 45 EN 68.9 / AR 71.5 s; -14 LUFS, peaks -1.7 to -2.6
  dBFS, covers in. ElevenLabs (MCP account_get_usage, 04:36Z): still Creator, 62,444 of 127,949 used, reset Dec 12; at
  about 5,400 a day (six Arabic voices) it lasts until about Dec 1.

## Nov 19 2026 (midday run, 11:23 PT): 46 Aswan High Dam, 47 igloo, 48 Moroccan riad (for Fri Nov 20)
- TODAY Nov 19 PT, TOMORROW Fri Nov 20 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT before the
  push). PST: Arabic 00:00 / 03:00 / 06:00 PT = 08:00Z / 11:00Z / 14:00Z; English 06:00 / 08:30 / 11:00 PT = 14:00Z /
  16:30Z / 19:00Z Nov 20.
- **YOUTUBE: Buffer now takes only 2 posts a day per YouTube channel.** New on Nov 19 (between 08:00Z and 11:00Z):
  Arabic YouTube 41, 42, 43 failed at post time with "The daily posting limit for this channel has been reached!", and
  requeue answers "You have already scheduled the maximum number of posts YouTube allows in a day (2)". New tool:
  tools.yml cmd=limits (scripts/limits.py) prints Buffer's dailyPostingLimits per channel for today and the next two
  days: YouTube 2, TikTok 25, Instagram 50 a day; the day is the channel's time zone (all six are America/Los_Angeles),
  and it counts scheduled + sent posts of that PT day. Six builds a day cannot all reach YouTube.
  Rule until the owner decides: each run gives YouTube to ONE build per language per day, its FIRST build (midday: EN
  06:00 / AR 00:00 PT; evening: EN 13:30 / AR 09:00 PT); its other two post files carry
  `hold: [en.youtube, ar.youtube]`. Before requeueing any YouTube post, run cmd=limits and pick a PT day with room.
  Nov 19 PT has four English YouTube posts queued (43 13:30, 44 16:00, 42 19:12, 41 20:58 PT): two will fail (if
  Buffer counts the day's sent + scheduled, 43 and 44 fail and 42 / 41 go out). Arabic 45 (15:00 PT) should go out
  (only 40 sent that day). EN 40 / 45 and AR 41-44 YouTube stay failed (no free day); the owner was told.
- Today's posts (status 19:28Z): English Instagram 40, 41, 42, 44 and English TikTok 40, 43, 44, 45 went out early
  at 05:40-05:43Z (21:40 PT Nov 18). No workflow of ours ran then (post 05:09Z, status 07:31Z): most likely "share now"
  in Buffer. English YouTube 40 and 45 failed "unknown error" at 07:25Z; English YouTube 41 and 42 were moved in Buffer
  to 03:12Z / 04:58Z Nov 20. Arabic 40, 41 live except 41's YouTube; Arabic TikTok 42 (14:00Z) and 43 (17:00Z)
  "potential spam" -> requeued to 01:30Z and 04:00Z Nov 21 (the 3-hour grid of Nov 20 is full). Status 21:09Z: Arabic
  44 Instagram live, its TikTok "potential spam" (20:00Z) -> requeued to 06:00Z Nov 21 (22:00 PT Nov 20), its YouTube
  failed on the daily limit with only 40 sent that day: Buffer counts sent + still-scheduled posts of the day at post
  time, so on a day with more than 2 queued the EARLIER ones fail. Arabic 45 at 15:00 PT, English 43-45 at 13:30 /
  16:00 / 18:30 PT. Next free Arabic TikTok gap 2 h from the others: after 23:00Z Nov 21 (the evening run of Nov 20
  fills 17:00 / 20:00 / 23:00Z).
- Pages: retired ep28-ep30 (all 18 sent): media/ 629 -> 520 MB before today's six videos. Next: ep31-ep33.
- A/B test: 47 is odd -> `igloo` in voices.yml ar_alt.kits (Mansour, Saudi script); 46 and 48 Egyptian.
- Voices: Easton aswan 65.69 s (226 words), igloo 63.99 s (229), riad 64.88 s (231). ElevenLabs one take each:
  Egyptian aswan 66.0 s (164 words, 863 characters), Mansour igloo 66.0 s (159 words, tempo 1.075, 825 characters),
  Egyptian riad 67.6 s (164 words). check_ar_voice: no weak lines (max 21%, the number lines).
- Whisper small heard Easton's "riad" as "riot" (riad lines 1 and 13, igloo line 10). tools/make_vo.py now has a SAY
  map (riad -> "ree-ahd") used only for the text sent to Easton; captions and the json keep the script's spelling.
  English remade free for igloo and riad (langs=en force=true): Whisper now writes "re aid" / "riyadh" (the right
  sound). Add a word to SAY whenever Easton says a name wrong.
- Scenes (all v2 look 2):
  - aswan.py (valley, section, divert, temple, shower): valley = raised view upstream, lake_half(y) with the inlets of
    the shore, up_half / dn_half for the river, mini_pyramid() x17 in two rows for the hook, the dam face with stepped
    berms, crest road + lamps, power house and outflow, flood (mud colour, houses half under) / dry (cracks, a thread
    of water) states, months() bars panel (all in summer -> every month), pylons at dusk; section = the hill of rock
    and sand with along() seepage paths stopped by the clay core and the cement curtain; divert = from above, a dump
    truck whose rocks are swept away, blasts along CHAN, water in the channel, a rock barrier; temple = facade() with
    statue() (the head drawn 1.35x about the neck; the second colossus broken, its head at its feet), cut lines,
    lifted 300 with cranes while the water rises; shower_guy() for the tag.
  - igloo.py (tundra, wind, blocks, build, cut, tag): aurora() curtains, blizzard(), igloo_outside() with spiral
    seams, the tunnel and warm light, a cutaway (interior() clipped to the dome) for the hook, hood_person() parka,
    magnifier() of snow grains, jacket_icon(), the spiral build with a key block, shell() of the wall in section with
    an ice glaze, lamp() qulliq, the trench where cold air pools; tag EN mom with a jacket, AR a Saudi man in a red
    shemagh who puts on the farwa (fur_cloak()) by a fire with the dallah (from barrier.py) at 20 degrees.
  - riad.py (court, city, section, wall, door, fez, tag): courtyard() front view (far wall arches, cedar gallery,
    green roof tiles, zellige_band() / zellige_star() laid piece by piece, perspective floor, orange trees,
    fountain()), facade() halves that slide shut and open, roofs() of the medina from above with shadows and green
    courtyards, donkey(), the house in section growing taller / narrower with the sun's shaft and cool night air, the
    wall that melts in rain then lime plaster + stone + black soap + beading water, the entrance from above (sight line
    stopped by the bent corridor), the neighbour with binoculars for the tag ("PASTA AGAIN?" / "ملوخية تاني؟").
- Lessons: skia Path.getLastPt() returns a bool in this binding (keep your own last point). Light snow, white domes,
  light floors and plaster bloom to pure white in v2's Post: keep them mid-tone (snow #AFC3DA..#5A7396, dome
  #DCE6F2..#6E88A8, riad floor #BFA984..#B59F78, rooms #CDB08A). draw.P takes 6-digit hex plus an alpha, not
  "#RRGGBBAA". In a shell, `cd X && (A) & (B) &` puts the cd in A's background shell only: start background chains
  after a plain `cd X;`. The riad's fountain sat behind the cover's name block (y 1227+): the closer camera was moved
  so the subject's key part sits above y 1200.
- Final: aswan EN 68.8 s / AR 69.1 s, igloo EN 67.1 s / AR 69.1 s (Mansour), riad EN 68.0 s / AR 70.7 s; all -14 LUFS,
  peaks -1.8 to -2.4 dBFS, covers in. Whisper small on the English mixes: number formats, riad -> "riyade" / "re aid"
  (the respelling), zellige -> "zelage"; nothing else. Credits 863 + 825 + 918 characters. 46 posts to all six targets;
  47 and 48 hold YouTube (four targets each).

## Nov 19 2026 (evening run, 18:37 PT): 49 Hagia Sophia's dome, 50 Korean heated floor, 51 Burj Al Arab (for Fri Nov 20)
- TODAY Nov 19 PT, TOMORROW Fri Nov 20 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT before the
  push). PST: Arabic 09:00 / 12:00 / 15:00 PT = 17:00Z / 20:00Z / 23:00Z Nov 20; English 13:30 / 16:00 / 18:30 PT =
  21:30Z Nov 20 / 00:00Z / 02:30Z Nov 21.
- Status 02:42Z (Nov 19 PT, the first six-a-day day): Arabic Instagram 40-45 all six live at their slots; Arabic TikTok
  only 40 and 41 (42, 43, 44 wait for 01:30Z / 04:00Z / 06:00Z Nov 21; 45 refused at 23:00Z); Arabic YouTube only 40.
  English Instagram + TikTok of all six live, but eight of those twelve went out at 21:40 PT Nov 18 (not our runs, most
  likely "share now" in Buffer); English YouTube only 43 so far (40 and 45 "unknown error" at 23:25 PT Nov 18, 44 the
  daily limit at 16:00 PT; 41 and 42 still queued for 20:58 / 19:12 PT Nov 19 and will probably fail).
- **Buffer counts FAILED YouTube posts toward the day's 2**: Arabic 45's YouTube (15:00 PT) failed on the daily limit
  with only 40 sent that day, after 41-44 had failed. So a failed YouTube post uses up its day's slot: never requeue a
  YouTube post onto a PT day that already has two YouTube posts sent, scheduled OR failed (check with cmd=limits).
- Requeued: Arabic TikTok 37 (third refusal, 02:00Z) and 45 (23:00Z) to 01:30Z and 04:30Z Nov 22 (17:30 / 20:30 PT
  Nov 21): the 3-hour grid of Nov 20-21 UTC is full, these are the first gaps 2 h from every other Arabic TikTok. The
  failed YouTube posts (EN 40, 44, 45; AR 41-45) stay failed: no PT day has room while each run keeps its YouTube slot.
- Metrics 02:51Z: 157,183 views (+16,139). Arabic YouTube woke up (car 1,159, phone 1,029, wind tower 988, pyramid
  536); the pagoda is the best Arabic Instagram post of Season 3 (1,588, 46% watched). Doc updated.
- Pages: retired ep31-ep33 (all 18 sent): media/ 634 -> 527 MB before tonight's six videos. Next to retire: ep34-ep36.
- A/B test: 49 and 51 are odd -> `hagiasophia` and `burjalarab` in voices.yml ar_alt.kits (Mansour, Saudi scripts);
  50 ondol is Egyptian.
- Voices (one take each): Easton hagiasophia 66.50 s (229 words), ondol 65.99 s (230), burjalarab 63.25 s (228).
  ElevenLabs: Mansour hagiasophia 72.57 s (163 words, 872 characters), Egyptian ondol 70.35 s (168 words, 930),
  Mansour burjalarab 66.03 s (155 words, 815); all three at the 1.12 speed-up cap. Mansour at 163 words is near the top:
  keep Saudi scripts at 150-160 words. Whisper small on the English voices: number formats, its/it's, here/hear,
  Easton's "shaped like" -> "shape like"; "Hagia Sophia's" and "Burj Al Arab" come out right. check_ar_voice: no weak
  lines (max 29%, the digit line). The voice runs took 5-8 minutes each, the three in parallel.
- ElevenLabs (MCP account_get_usage 04:15Z): still Creator, 69,490 of 127,949 used, reset Dec 12; at about 5,400 a
  day it lasts until about Dec 1 (the Pro upgrade has not happened yet).
- Scenes (all v2 look 2):
  - hagiasophia.py (hall, pend, frame, city, tag): hall() = the building cut through its middle (section mass, aisle
    arcades with green marble columns, the far tympanum with three rows of windows, gold spandrels, the window band
    with win_x() for the far half's 20 windows, the dome's inner far half with ribs as projected meridians, gold that
    spreads from the crown, cracks, `lift` to float it, sun beams with an additive paint Padd()). pend = a real 3D
    pendentive diagram: p3() orthographic projection (yaw 32, pitch 24), pier3(), arch3() in the planes x = +-A3 /
    z = +-A3, pend3(k) = the sphere patch between two arches filled from the corner up (the horizontal section at
    height hk is an arc of radius sqrt(2A^2 - hk^2)), ring3(), dome3() (upper half circle + front half of the ring's
    ellipse); a round drum morphs into a square box with red corners; emperor() with a crown. frame() = the dome on two
    piers in section: piers that tip out (lean), half domes sliding in, buttresses hugging the piers, the first dome
    breaking into falling chunks with dust, a dashed ghost of the old profile; bricks_mag() = a magnifier with mortar as
    thick as the bricks swaying. exterior() = the south elevation (body, exedrae, half domes, tympanum, buttresses,
    drum with windows, lead dome with ribs, four minarets) for the stat, closer and cover. Tag: phone() from phone.py
    slides off a couch and cracks (crack_snd from humanoid.py).
  - ondol.py (house, winter, plan, layers, room, city, tag): hanok() = the house in section (sunken kitchen, stove with
    the rice pot and fire(), the room's layered floor: flues with stone supports, stones, clay, oiled paper, a warm
    glow; the pit and chimney; a tiled roof with snow); smoke_dash() = moving dashes along a smoothed path (dash phase
    from t); plan = the floor's underside from above with a heat-map grid (heat()), one channel vs rows of channels,
    stone_slab() laid one by one; layers = section close-up with clock(), battery(), sleeper(); room = front view, the
    oiled paper laid strip by strip with a shine sweep and a wipe; city = tower_block() cut open with red pipes, a pan
    to an American house; tag EN: dad in sunglasses guarding a thermostat inside a vault door with lasers; AR: the
    barefoot kid on cold tiles and mom (phone.mom) with a slipper, bubble "البس الشبشب!" (different visual per language).
  - burjalarab.py (coast, island, piles, shore, sail, tag): burj() = the hotel from the side (the sail's curve is a
    quadratic, the body with floors, the fabric band, a two-leg steel exoskeleton with X bracing, the restaurant pod, a
    cantilevered helipad with two tennis players), island(), skyline() drawn far away (scaled 0.42, with the tallest
    tower), sea_band(), wave(), hexagon() armour blocks, saudi_man() (thobe, red shemagh, agal), shampoo(). The section
    sets work in screen space. Tag EN: tiny shampoo bottles filling a suitcase in a gold room; AR: the uncle at his door,
    "فندق؟! وبيتي وش فيه؟" (the third "فندق" of the line, found with self.w(..., nth=2)).
- Lessons: bik.draw.P() takes no blend mode: build the paint and call setBlendMode(PLUS). Arabic stat cards: the big
  value stays digits only and the unit goes in the small Arabic label ("55" + "متر علو", not "55 m"; the first ep49
  render was cancelled to fix it). Bright flat areas bloom (snow ground #B9C9DE, gold-leaf walls, white tiles in a
  tag): keep them mid-tone (snow #8DA2C0..#4E6488). A frame-wide darkening belongs in screen space (a world rect shows
  its edges when the camera moves). Where two shapes meet along a slope (sand and sea), build the second from the
  first one's edge or the sky shows through the gap. A far skyline drawn at full scale looks like it stands next to the
  subject: scale it down.
- Produce: one slug per run as each scene was ready (49 at 03:33Z, after a 1-minute cancelled run; 50 at 03:51Z; 51 at
  04:07Z), about 25 minutes each.
- Final videos: hagiasophia EN 69.6 s / AR 75.7 s, ondol EN 69.1 s / AR 73.4 s, burjalarab EN 66.4 s / AR 69.1 s; all
  -14 LUFS, peaks -1.8 to -2.6 dBFS, covers in and inside the grid crop. Whisper small on the English mixes: number
  formats and homophones only (49 "in mortar" -> "and mortar", 51 "sail" -> "sale", "two tennis" -> "to tennis").
  Local scratch tools for this (not in the repo): Whisper small line by line on a voice json + wav, and on the mp4's
  16 kHz audio cut by Timeline(vo_json, LABELS, lead=0.5, pause=0.6, tail=2.0).s/e per line.
- Posts: 49 all six targets "scheduled" (YouTube at EN 13:30 / AR 09:00 PT Nov 20, this run's slot); 50 and 51 hold
  YouTube; their English Instagram + TikTok and Arabic Instagram are "scheduled" at 16:00 / 18:30 PT and 12:00 / 15:00
  PT. **Their Arabic TikToks "wait": the Arabic TikTok channel already had 10 posts queued** (39 at 05:00Z, 46-49 on
  Nov 20, the requeued 42-44 on Nov 21 and 37, 45 on Nov 22; config.yml queue_limit 10). post.py adds a waiting
  target only when post.yml runs again (a push to posts/ or media/, or a dispatch), so a check-in of this session at
  08:20Z Nov 20 (send_later, trig_01KpU6SFMYCu3dFe1NrAWrm1) dispatches post.yml once 39 and 46 have left the queue.
  If state/ep50-ondol.json or state/ep51-burjalarab.json still has no ar.tiktok when the midday run of Nov 20 starts,
  that run should dispatch post.yml first (before 20:00Z) and requeue whichever time has already passed. With
  refusals being requeued 1-2 days out, the Arabic TikTok queue will keep hitting 10: from now on, check
  state/last-run.md for "waits" after every post push.
- Resolved Nov 20 08:24Z: ep50's Arabic TikTok was added by the 05:30Z post run (started by the config push), ep51's by
  the check-in's post.yml dispatch; both "scheduled" (12:00 and 15:00 PT Nov 20). Arabic TikTok 39 (05:00Z) and 46
  (08:00Z) went out first try.
- Nov 19 21:13 PT: owner chose "option 1" for YouTube: 2 builds a day per channel get YouTube, the other 4 are held
  (rule in LINEUP.md). Builds 46 and 49 already carry YouTube for Nov 20, 47/48/50/51 hold it; failed YouTube posts stay failed.
- Nov 19 21:18 PT, the owner: "Let's start mention at the end, follow us on YouTube for more videos and give it the
  @congratsengineer and the other one", and asked for a deep check of the money plan ("I need 10 million views and 1000
  subscriber ... are we going to the right path ... in a couple months maybe we'll start making money"). Done / found:
  - config.yml cta: English default (Instagram + TikTok) and Arabic Instagram now end with a second line "Follow us on
    YouTube for more builds: @congratsengineer" / "وتابعنا على يوتيوب لفيديوهات أكثر: @kef.tenbeni" (the handles are the
    same on all three apps per the owner; the YouTube pages could not be opened from this session to confirm). Arabic
    TikTok left out for now (potential-spam refusals); he was told. Applies to posts created from now on (52+);
    posts already in Buffer (46-51) keep their captions. Checked with caption_for on ep51: no issues on any platform.
  - **The 2-a-day YouTube limit is Buffer's FREE plan** (support.buffer.com daily posting limits: YouTube Shorts free 2,
    paid 100 with a verified email). Essentials is $6 a channel a month ($5 yearly), 3 channels per account = $18, both
    accounts $36; it also removes the 10-scheduled-posts cap. Not bought: our own numbers say 2-3 YouTube posts a day get
    ~1,000 views each while the bulk days got a median of 11, so more YouTube posts a day is not the lever. His call.
  - Money rules checked Nov 19 2026 (details + sources in the project doc claude/build-it-money-plan.md): YouTube ads =
    1,000 subs + 10M Shorts views / 90 days or 4,000 watch hours / 12 months; **from Feb 1 2027 new channels need 20M /
    90 days or 8,000 hours, and Shorts ads pay only channels holding 10M / 90 days**. YouTube's July 2026 "inauthentic
    content" clarification names template-based, AI-heavy, near-identical videos made in volume as not monetizable.
    TikTok Creator Rewards: 10k followers + 100k views / 30 days, videos over 1 minute, 8 countries (no Arab country),
    about $0.40-1.00 per 1,000 qualified views. Instagram: no per-view pay.
  - Where we are (metrics 02:51Z Nov 20): EN YouTube about 2,000 views a day against 111,000 a day needed (~55x), AR
    YouTube about 800 a day; EN TikTok 26,195 views in 10 days; EN Instagram 77,586 (half of all 157,183). Follower and
    subscriber counts are unknown here (Buffer gives none); asked him for the six numbers.
  - Told him: payouts in a couple of months are unlikely at this pace; proposed 3 builds a day again with the effort
    going into the first seconds, English TikTok + English YouTube as the money targets, and one long YouTube
    compilation a week (watch hours, long-form ad rates). WAITING for his yes/no: do not change the pace until he answers.
  - The config.yml push (05:28Z Nov 20) started post.yml, as any config.yml push does: it scheduled 50's waiting Arabic
    TikTok (20:00Z Nov 20) because the queue had one free place; 51's Arabic TikTok still waits (10 queued). Nothing
    else changed. The money plan is saved as the project doc claude/build-it-money-plan.md.
- Nov 19 22:15 PT, the owner: "What the next strategy to post longer videos that entertaining on YouTube plus other
  social media". PROPOSED (not started, waiting for his go; the daily runs change nothing):
  - "One story, three sizes": the daily 65 s build stays; twice a week a vertical 3-minute "trilogy" (three builds that
    beat one problem, one hook, no repeated intros or follow lines) for Instagram, TikTok and YouTube Shorts; once a
    week a 9-10 minute HORIZONTAL YouTube episode (eight builds as one adventure, new hook + linking lines + a running
    joke and counter, the vertical animation in the middle with a designed side panel).
  - Why these lengths (checked Nov 19 2026): YouTube treats vertical/square up to 3:00 as a Short and Shorts time never
    counts toward watch hours; 16:9 is a regular video at any length; mid-roll ads need 8:00+. Instagram allows 20-minute
    Reels but recommends only up to 3 minutes to non-followers (Buffer study: 90 s to 3 min reach best). TikTok: 60 s+
    gets more reach and is the floor for Creator Rewards; uploads up to 60 minutes. A plain stitch of Shorts adds
    nothing under YouTube's reuse rule: the long video must be a new story.
  - Buffer posts only Shorts to YouTube: a long video needs a YouTube Studio upload (the owner, or his Chrome).
  - First samples offered, English, private until he has watched them: trilogy "3 ways people beat the desert with no
    electricity" (37 wind tower, 44 falaj, 48 riad) and episode "No engines: build 8 wonders anyway" (36 pyramid, 38
    Petra, 39 pagoda, 42 Venice, 43 Great Wall, 44 falaj, 45 Machu Picchu, 49 Hagia Sophia). All are in media/; older
    builds are in git history (the clone is not shallow). The mixes have no music bed, so lines can be cut cleanly.

## Nov 20 2026 (midday run, 11:23 PT): 52 Palm Jumeirah, 53 refrigerator, 54 Eiffel Tower (for Sat Nov 21)
- TODAY Nov 20 PT, TOMORROW Sat Nov 21 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT before the
  push). PST: Arabic 00:00 / 03:00 / 06:00 PT = 08:00Z / 11:00Z / 14:00Z; English 06:00 / 08:30 / 11:00 PT = 14:00Z /
  16:30Z / 19:00Z Nov 21.
- Status 19:29Z (Nov 20 PT, builds 46-51): 46-48 English Instagram + TikTok live; 46 Arabic all three live; 47 all four
  live; 48 Arabic Instagram "an issue with the media attached" (14:00Z) -> requeued to 21:00Z Nov 20, and its Arabic
  TikTok "potential spam" -> 01:30Z Nov 23; 49 Arabic Instagram + YouTube live, its TikTok "potential spam" (17:00Z) ->
  04:30Z Nov 23. Status 20:27Z: 50 Arabic Instagram live, its TikTok "potential spam" (20:00Z) -> 21:00Z Nov 20
  (exactly 2 h before 51's 23:00Z). The only 2-hour gaps left in the Arabic TikTok grid are at night UTC after the
  23:00Z slot (01:30Z / 04:30Z the next day), already used through Nov 23 UTC.
- **English YouTube 46 (06:00 PT Nov 20) failed on the daily limit although Nov 20 PT had only 46 and 49 queued.**
  The English channel had 42 sent at 03:12Z and 40/41/44/45 failed at 04:59Z, all on Nov 20 UTC (19:12-20:59 PT Nov 19).
  So Buffer's 2-a-day YouTube count is NOT the PT day. 49's English YouTube (21:30Z Nov 20) will probably fail the same
  way. [Corrected by the 23:30Z check-in at the end of this section: the count is 2 SENT posts in a rolling 24 h,
  failed posts do not count, and the evening run's English YouTube must NOT be its 13:30 PT build.] This run's YouTube
  posts: EN 19:00Z, AR 14:00Z Nov 21.
- Pages: retired ep34-ep36 (all 18 sent): media/ 636 -> 549 MB before today's six videos (about 128 MB). Next: ep37-ep39
  (37's Arabic TikTok waits for 01:30Z Nov 22: retire 37 only after it is sent).
- A/B test: 53 is odd -> `fridge` in voices.yml ar_alt.kits (Mansour, Saudi script); 52 and 54 Egyptian.
- YouTube slot: given to 54 the Eiffel Tower (the strongest topic of the three, as the performance doc asks), not to the
  first build: 52 and 53 carry `hold: [en.youtube, ar.youtube]`; 54 posts YouTube at EN 11:00 / AR 06:00 PT.
- Voices: Easton palmjumeirah 63.29 s (227 words), fridge 64.21 s (228), eiffel 67.20 s at first (229 words, many
  numbers) -> trimmed to 223 words, 66.08 s. Whisper small heard "seabed" as "sieved" and "tide" as "tie": reworded
  ("sea floor", "fresh sea water flows in") and English remade free. "Jumeirah" comes out as "Jumira" / "you mirror"
  (name only; the caption carries it). ElevenLabs (one take each): Egyptian palmjumeirah 66.0 s (165 words), Mansour
  fridge 66.0 s (156 words), Egyptian eiffel 70.6 s (165 words). check_ar_voice: fridge line 8 "للحين مضغوط" was 20%
  (heard "الحمد غوط"), rewritten "بس هذا السائل للحين تحت ضغط قوي" -> 6% (one line remade); everything else under 22%.
- Research: WebSearch here returns only titles and links (no page text), and agents are not allowed, so facts were
  checked against result titles (toureiffel.paris "Why does the Eiffel Tower change size?", the 15 cm summer growth,
  compressed-air caissons in Google Arts & Culture, Scientific American on the Einstein-Szilard refrigerators, the
  magnetic door seal patent) plus well-documented figures (Palm: 94 million m3 of sand, 7 million t of rock, 11 km
  crescent, 16 fronds, rainbowing, vibro-compaction, two gaps; Eiffel: 18,038 parts, 2.5 million rivets, 57 m first
  floor, 60 t of paint in three shades, 20-year permit; melted = 7,300 t / 7.87 t/m3 / 125 m x 125 m = 5.9 cm).
- Scenes (all v2 look 2):
  - palmjumeirah.py (top, coast, plan, sand, storm, quake, tag): palm_island() draws the island from above: frond(i,
    side) gives the 16 fronds (tips on a circle), arc_pts() the crescent (closes from both ends, GAPS opens two cuts,
    boulders along the outer edge), shallow-water halos, villas_top(), towers on the trunk, the big hotel at the top,
    `dusk` for the sunset closer; sea_top()/coast_top(); dredger_top() + sand_arc() (rainbow option) for rainbowing;
    plan = blueprint with numbered fronds and glowing beach lines; quake = grains() section, soup jitter, vibro probes
    with rings, house_side(); tag = towel_person() biting a sandy sandwich.
  - fridge.py (kitchen, ice, loop, tag): LOOP = the refrigerant path (compressor -> condenser zigzag on the back ->
    capillary coil -> evaporator in the freezer -> suction line), loop_at(s) / temp_col(s) colour the dots by
    temperature; the loop set shows one part per beat (evaporator boils, compressor cutaway piston, coils with heat
    lines, two gauges, capillary) then the whole loop flowing; fridge_front() front view with the door swinging open;
    ship() with ice blocks for break1; tag: an empty lit fridge, a person staring, a spinning clock; AR adds mom (phone.mom)
    with "سكّر الثلاجة!".
  - eiffel.py (paris, wind, ground, legs, rivets, tag): eiffel() draws the tower from w_out(h) / w_in(h) (outline and the
    gap between the legs, metres x U=2.4), lattice diagonals per panel, the arch, three platforms, shades by height,
    `lit` + `sparkle` for the night closer, `solid` and `sway` for the sail; rooftops() of Paris; caisson section with an
    air hose and two diggers; legs set at zoom 3.2 with one leg low and a jack; rivets close-up (gusset plate, red-hot
    rivets cooling, forge, hammer); tag: the protest letter, the pinch photo; AR adds the aunt: "برج القاهرة أحلى!".
- Lessons: light interiors bloom white in v2's Post (fridge inside, frozen lake): keep them mid-tone (#7FA8CC..#5E86AE,
  body #8E98A6). A stat-beat camera key `.key(s("closer"), ...)` overrides the closer's own key: end the stat drift
  before the closer. Captions over a low sun wash out: keep the sun above y ~700. The Arabic TikTok queue (10) is the
  bottleneck at six builds a day plus requeues: 54's Arabic TikTok "waits" until 51 (23:00Z) leaves the queue.
- Produce: one slug per run as each scene was ready (52 at 20:05Z, 53 at 20:22Z, 54 at 20:29Z), 24-30 minutes each.
  Final videos: palmjumeirah EN 66.4 s / AR 69.1 s, fridge EN 67.3 s / AR 69.1 s (Mansour), eiffel EN 69.2 s / AR 73.7 s;
  all -14 LUFS, peaks -1.8 to -2.4 dBFS, covers in and inside the grid crop. Whisper small on the English mixes: number
  formats, "Jumeirah", "so fresh" -> "soap fresh", "in sawdust" -> "and sawdust" (captions carry the words).
- Posts (state 21:06Z): 52 and 53 four targets each "scheduled" (YouTube held), 54 five of six: its Arabic TikTok
  "waits" (queue 10). A check-in of this session at 23:20Z Nov 20 (send_later trig_011SuFGKr9sKkow9RpoeyDb4) dispatches
  post.yml once 51 (23:00Z) has left the queue; if that did not happen, the evening run's own post push adds it (its
  slot is 14:00Z Nov 21).
- 21:06Z: 48's Arabic Instagram went out on its requeue (21:00Z); 50's Arabic TikTok was refused again at 21:00Z. Its
  requeue is left to the 23:20Z check-in, AFTER post.yml has added 54's Arabic TikTok: post.py counts scheduled future
  posts against the 10, so requeueing 50 first would keep 54 waiting. Free 2-hour gaps: 01:30Z / 04:30Z Nov 24.
- 23:20Z check-in: post.yml (dispatch, state 23:25Z) put 54's Arabic TikTok on Buffer, "scheduled" for 14:00Z Nov 21
  (06:00 PT Sat): all 14 targets of 52-54 are scheduled. 51's Arabic TikTok went out at 23:01Z on its first try. 50's
  Arabic TikTok requeue (01:30Z Nov 24) was REFUSED by Buffer: "Scheduled posts limit reached. You have 10 scheduled
  posts out of 10 allowed" (Buffer's own count: an errored post does not count, putting it back does). 50 stays "error"
  and goes to the evening run: requeue it to 01:30Z Nov 24 (still free) only AFTER post.yml has put that run's own three
  Arabic TikToks (17:00Z / 20:00Z / 23:00Z Nov 21) on Buffer. The queue empties as 42 (01:30Z), 43 (04:00Z), 44
  (06:00Z), 52 (08:00Z), 53 (11:00Z) and 54 (14:00Z Nov 21) go out: at ~05:00Z there is room for two, so plan a
  check-in for the third and for 50.
- **YouTube limit, corrected: 2 SENT posts per channel in any rolling 24 h; failed posts do not count.** At about
  21:43Z the failed English YouTube posts were retried in Buffer (not by our runs): 41 went out at 21:43:50Z, 13 minutes
  after 43's send (21:30:56Z Nov 19) left its 24 h window, and 40, 44, 45, 46, 49 failed again (42 at 03:12Z and 41 in
  the window). That fits every YouTube result since the limit appeared on Nov 19 (46 at 14:00Z and 49 at 21:30Z failed
  with 43 + 42 in the window; Arabic 45 at 23:00Z Nov 19 with 39 at 23:02Z Nov 18 + 40); the UTC-day and PT-day ideas
  do not. Rule: a YouTube post at T passes only if fewer than 2 posts of that channel were SENT in the 24 h before T
  (sentAt in state/status.md, plus scheduled ones due before T); keep 15 min of margin, a post sends 0-4 min after its
  slot. For the evening run of Nov 20 (55-57): English has 41 (21:43:50Z Nov 20) and 54 (19:00Z Nov 21), so 13:30 PT
  (21:30Z) FAILS, 16:00 PT (00:00Z Nov 22) and 18:30 PT (02:30Z) pass; Arabic has 49 (17:02Z Nov 20) and 54 (14:00Z
  Nov 21), so 09:00 PT (17:00Z) FAILS, 12:00 PT (20:00Z) and 15:00 PT (23:00Z) pass. Give YouTube to its 2nd or 3rd
  build (put the strongest topic there) and hold it on the 1st. The same slot on the next day fails too (the earlier
  post is still in the window by seconds), so every run checks the rule for each YouTube slot and holds YouTube for a
  language when none of its slots passes (Sunday's midday slots all fail after 54 + the evening run's post).

## Nov 20 2026 (evening run, 18:37 PT): 55 Suez Canal, 56 escalator, 57 Sydney Opera House (for Sat Nov 21)
- TODAY Nov 20 PT, TOMORROW Sat Nov 21 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT before the
  push). PST: Arabic 09:00 / 12:00 / 15:00 PT = 17:00Z / 20:00Z / 23:00Z Nov 21; English 13:30 / 16:00 / 18:30 PT =
  21:30Z Nov 21 / 00:00Z / 02:30Z Nov 22.
- Status 02:43Z (Nov 20 PT, builds 46-51): English Instagram + TikTok all six live at their slots; English YouTube 46
  and 49 failed on the 2-in-24-h limit (41 went out at 21:43Z on a retry made in Buffer). Arabic Instagram all six live
  (48 on its requeue); Arabic YouTube 46 and 49 live; Arabic TikTok 46, 47, 51 live, 48 / 49 refused and waiting for
  01:30Z / 04:30Z Nov 23, 50 refused twice ("error"), and 42's requeue (01:30Z Nov 21) was refused again ("error").
- Metrics 02:47Z: 168,374 views (+11,191). English YouTube numbers have not been refreshed by Buffer since Nov 20
  02:25Z (+0, not real); English Instagram last refreshed 19:09Z. Arabic Instagram's best day of Season 3 (+4,340:
  igloo 1,629 Mansour, Aswan 1,427, ondol 910). Six a day: English views per post less than half of the Season 3
  median (EN Instagram 809 vs 1,980, EN TikTok 65 vs 328), Arabic per post unchanged. Doc updated.
- Pages: retired ep38, ep39, ep47 (all posts sent; 37 still waits for its Arabic TikTok, 40-46 and 48-50 have failed
  YouTube or waiting/errored Arabic TikToks): media/ 669 -> 570 MB before tonight's six videos. Next: the oldest builds
  whose posts are all "sent" (51 is; 37 after 01:30Z Nov 22).
- A/B test: 55 and 57 are odd -> `suez` and `operahouse` in voices.yml ar_alt.kits (Mansour, Saudi scripts); 56
  escalator Egyptian.
- YouTube (rolling 24 h rule, checked per slot): English 13:30 PT fails (41 at 21:43:50Z Nov 20 + 54), 16:00 / 18:30
  pass; Arabic 09:00 PT fails (49 at 17:02Z Nov 20 + 54), 12:00 / 15:00 pass. YouTube went to 57 (EN 18:30, AR 15:00
  PT); 55 and 56 hold it. For the midday run of Nov 21 (Sun Nov 22 PT): English 14:00Z / 16:30Z / 19:00Z Nov 22 all have
  54 (19:00Z Nov 21, by seconds) or 57 (02:30Z Nov 22) in their window -> hold English YouTube; Arabic 08:00Z / 11:00Z /
  14:00Z Nov 22 have 54 (14:00Z Nov 21, by seconds) + 57 (23:00Z Nov 21) -> hold Arabic YouTube too.
- Voices: Easton suez 67.58 s at first (230 words) -> trimmed twice to 222 words, 66.47 s; escalator 64.04 s (231);
  operahouse 66.49 s (229). ElevenLabs one take each: Mansour suez 67.77 s (161 words, 890 characters), Egyptian
  escalator 66.37 s (165, 890), Mansour operahouse 67.70 s (159, 861); all at the 1.12 cap. check_ar_voice: no weak
  lines (max 26%, the digit lines). Whisper small on the English voices: number formats, "fresh water" ->
  "freshwater", "sails" -> "sales", "mould" written "mold" (the script now says mold); escalator line 11 "with" heard as
  "of" (reworded: "staff stood at the top with brandy and smelling salts").
- ElevenLabs (MCP account_get_usage, ~03:40Z Nov 21): still Creator, 101,849 of 127,949 used (26,100 left), reset Dec 12.
  That is +32,359 since Nov 20 04:15Z, while this project's six Arabic voices of Nov 20 used about 5,400: the other
  projects on the plan are burning about 27,000 a day. At that pace the plan runs out within about a day: the owner
  was told (the Pro upgrade has not happened).
- Research: WebSearch still gives titles and links only; facts were checked against result titles (NASA Earth
  Observatory "The New Suez Canal", House Divided "130 mile fresh water canal ... completed", napoleon.org "Dredgers
  specially built for the Suez Canal", The National on the Ever Given digger operator, The Vintage News on Harrods'
  first escalator and the cognac, CNN on Hong Kong's escalator, sydneyoperahouse.com "The spherical solution", Guinness
  "Largest proportional increase in cost for a building project", NSW Treasury "The House the Lotteries Built") plus
  well-documented figures.
- Scenes (all v2 look 2):
  - suez.py (desert, map, cut, camp, dig, lakes, level, tag): desert = side view with the canal's water hidden behind
    the near dune so the container ship (panama.cargo_ship, 760 long) seems to sail on sand; the Eiffel Tower
    (eiffel.eiffel rotated 90, scale 0.7) lies on the containers for scale; on "congrats" the near bank drops to show
    the water. map = geo(lon, lat) -> world (10.4 x 10.8 units a degree), polygons for Africa, Eurasia, the UK,
    Madagascar, Black Sea and Caspian, the long route round the Cape and the short one through the canal drawn with
    along(); cut = the isthmus from above (Mediterranean, Nile delta, Gulf of Suez, lake beds, the cut drawn top to
    bottom, then both seas running in and meeting in the Bitter Lakes); camp (tents -> mudhouse city, a fresh water
    canal with palms); dig (trench section, workers with head baskets, dredger() bucket chain + slide_sand());
    lakes (one lane nose to nose; ship_on(pts, u) moves panama.ship_top along a polyline: southbound convoy anchors
    in the lake, northbound passes; the lake bed flashes white salt); level (both seas level, a crossed-out ghost lock
    staircase); tag EN: the stuck ship + excavator(), then laundry() vs you; AR: barrier.suv blocked by a second car
    and burjalarab.saudi_man with a bubble "جواله مقفل!".
  - escalator.py (mall, stairs, wheels, comb, rail, harrods, long, tag): ypass(x) = the passenger side (flat, 30 degree
    incline, flat), steps_at(t) puts NSTEP steps on a loop (top run moving right, return run RET below moving left,
    hidden turnarounds), step_top() draws tread + riser so the stairs form and flatten by themselves, step_ret() the
    upside-down return, truss_path() the side panel (see-through in the x-ray of the hook and fix1, with the dashed
    chain, sprockets and the motor). wheels = the lower transition at zoom 2.6 with the two tracks (yellow ypass+30,
    cyan ypass(x + D - 16)+30) and two wheels per step; comb = top view of grooved plates sliding under the floor plate,
    a sneaker with a red lace, then yellow comb teeth; rail = the camera follows one rider up the slope, the rider tips
    back when the rail lags; harrods = 1898 moving ramp, dizzy shopper, staff with a tray (no glass in Arabic);
    long = Moscow's long tunnel escalator + Japan's 5-step one; tag EN: up to the GYM, then a stair machine; AR:
    grandma() in a headscarf at the bottom, waiting for a step to stop.
  - operahouse.py (harbour, sketch, sphere, molds, cranes, tiles, tag): shell_path(bx, bw, h, d) = a sail-like shell
    leaning toward d, SHELLS = the front and back rows, opera() = podium + shells (tile chevrons clipped to each shell,
    dirt, glare, lit); bridge() = the harbour's arch bridge far away; sphere_ball() with a highlighted spherical
    triangle, orange() peeling; molds (a different mold per shape and $$$, then identical rib_piece()s); cranes (a ghost
    shell, rib pieces placed up its edge, crane() hook, steel cable glowing); tiles (dirty + glare flash, then tiles
    and rain); harbour at dusk for the reveal (fireworks for 1973, the architect's boat sailing away), the 67 m ruler
    for the stat, night for the closer; tag EN: the bill unrolling x14 and a calendar 1963 -> 1973; AR: the
    contractor's bubble "أسبوعين وأسلمك!".
- Produce: one slug per run as each scene was ready (55 at 03:29Z, 56 at 03:32Z, 57 at 03:35Z), about 25 minutes each.
  Final videos: suez EN 69.6 s / AR 70.9 s (Mansour), escalator EN 67.2 / AR 69.5, operahouse EN 69.6 / AR 70.8
  (Mansour); all -14 LUFS, peaks -1.9 to -2.6 dBFS, covers in and inside the grid crop. Whisper small on the English
  mixes: number formats, "sails" -> "sales", "you'd" -> "you", "cover it in" -> "cover in" (captions carry the words).
  media/ 681 MB with the six new videos.
- Posts (state 04:09Z): 13 of 14 targets "scheduled" at their Sat Nov 21 PT slots (checked by turning every dueAt back
  into PT); 55 and 56 hold YouTube; 57's Arabic TikTok "waits" (queue 10: 44, 52-56, 37, 45, 48, 49). 43's Arabic
  TikTok went out at 04:01Z on its requeue. A check-in of this session at 11:20Z Nov 21 (send_later
  trig_01JmXxJMDHQE1PryN529GJ48) dispatches post.yml for 57's Arabic TikTok (slot 23:00Z) and requeues 50 and 42 to
  01:30Z / 04:30Z Nov 24. If state/ep57-operahouse.json still has no ar.tiktok when the midday run of Nov 21 starts,
  that run does both first.
- YouTube with fixed daily slots: a post sends 0-4 minutes after its slot, so the previous day's post in the SAME slot
  is still inside the 24 h window (54 at 19:00Z Nov 21 blocks every 19:00Z-or-earlier slot of Nov 22). To get two a
  day again, give each YouTube post its own at: (posts accept a per-platform map, e.g. at: {default: ..., youtube:
  ...}) about 20 minutes after the matching YouTube post of the day before, or accept one a day on some days.
- 11:20Z Nov 21 check-in (status 11:23Z): 44's Arabic TikTok (06:01Z, its requeue) and 52 / 53 in Arabic (08:02Z /
  11:03Z) went out. post.yml (dispatch, state 11:29Z) put 57's Arabic TikTok on Buffer, "scheduled" 23:00Z Nov 21 (15:00
  PT): all 14 targets of 55-57 are scheduled. Requeued 50 -> 01:30Z and 42 -> 04:30Z Nov 24 (17:30 / 20:30 PT Mon Nov
  23); the Arabic TikTok queue is 10 of 10 (when the midday run starts at 19:23Z only 54 and 55 will have gone: room for
  two of its three). English YouTube: a retry made in Buffer at 03:12Z Nov 21 sent 44 (45 failed again), so 54's English
  YouTube (19:00Z Nov 21) will fail on the limit (41 at 21:43Z Nov 20 + 44 in its window); 57's (02:30Z Nov 22) still
  passes. That changes the plan above for the midday run of Nov 21: with 54 failed, English 14:00Z Nov 22 has only 57 in
  its window (one English YouTube can go there, 16:30Z / 19:00Z then fail); check the status first. Arabic: still hold
  (54 + 57).
- Lessons: a sweep or a save check runs about 2 minutes here; queue them with nohup + tools/slot.sh and write the next
  scene meanwhile. A sand-coloured ground rect must reach the bottom of the frame (the sky shows a pale band below).
  falaj.basket() draws a 1200-unit rope (it hangs from a windlass): write your own head basket. panama.cargo_ship's
  white bridge blooms: tone it down with a grey overlay. English anchors: "HAND" also matches "HANDRAIL" (startswith):
  use self.w(..., nth=1) for English only.
- Nov 20 20:44 PT, the owner: "Every day 4 mins videos / We need to upgrade our contents / Try new themes new sounds effects
  new sounds / We need to be come a trend everywhere / Let's work on something that will attrac people to watch and get to
  the moooon". Done the same evening (this chat): a PILOT of the 4-minute show, sent to him to watch. NOT POSTED, and the
  daily runs are unchanged until he answers.
  - "SURVIVAL MODE: ZERO ELECTRICITY", 264.6 s (4:24.6), 1080x1920, -14.0 LUFS, true peak -2.1 dBFS. One story from four
    finished English builds as four game levels: 37 wind tower (boss HEAT), 44 falaj (THIRST), 47 igloo (COLD), 50 ondol
    (THE NIGHT). No new animation. Each build is cut to hook..fix4 (the follow line and its pause dropped), the reveal, a
    2.5 s level-clear panel (achievement + three stat cards + score), then the joke; stat line and closer dropped.
  - New on top: a cold open (three "no" icons, four clean world shots drawn with draw_world, the title), a level card
    before each build, a game bar that covers the kit's HUD pill (level, boss name, a health bar that each fix knocks
    down by a quarter, score +250 per fix), "achievement unlocked", a results card ("WORLD CLEAR", power used 0 W, rank).
    New narration: kit/series/survival1_lines.txt (9 lines; voice.yml kit=survival1 langs=en -> series/voice/survival1.*).
    New sound, all synthesized in kit/show/sounds.py (no samples, no licences): a music bed per world that adds layers
    with every fix (desert: D Phrygian dominant, maqsum drums, oud-like plucks; falaj: water drops; arctic: bells and
    wind; ondol: G pentatonic in 12/8 with a janggu), and game jingles in each level's key (boss appears / attacks / hit
    / down, achievement, level start, fanfare). Music sits about 13 dB under the voice and dips 6 dB while anyone talks.
  - How to build it again: python3 kit/show/build_survival.py <dir with windtower.mp4 falaj.mp4 igloo.mp4 ondol.mp4> <out>
    (steps prep audio stills video mux qa; here prep 90 s, audio 60 s, video 280 s on 2 CPUs). The builds' videos are
    media/ep37-windtower-en.mp4, ep44-falaj-en.mp4, ep50-ondol-en.mp4 and `git show 7897b0a:media/ep47-igloo-en.mp4`
    (retired from media/). The 124.8 MB master is NOT in the repo; the owner got a 43.6 MB copy.
  - Checked: 28 frames across the finished file and every kind of cut (sheet), each sound piece against the final mix
    (all within 4 ms of the plan), every music pattern against its scale. NOT checked: how it sounds. This session
    cannot listen, and the owner was told his ears are the test.
  - Platform rules for a vertical video over 3 minutes (checked Nov 19-20): YouTube treats it as a regular video (it
    counts toward watch hours), but Buffer only posts Shorts to YouTube, so it needs a YouTube Studio upload (untested).
    Instagram allows it (Buffer: Reels of 3 s to 15 min, under 300 MB) but does not recommend Reels over 3 minutes to
    non-followers: post it there as two halves under 3 minutes. TikTok takes it (over 1 minute is also the pay floor).
  - If he likes it: a daily episode from four builds (57 builds = 14 episodes in stock), the day's builds planned in sets
    of four on one theme, two more themes to test against this one ("The King's Engineer", "Level Up"), an Arabic
    version (about 700 ElevenLabs characters for the nine lines; the plan was almost empty on Nov 20), and a workflow so
    the runs can build it on Actions. The spec is in the project doc claude/build-it-4-minute-show.md.
- Nov 21 09:26 PT, the owner: "Ok my plan is we start promoting the YT channel after we post on social media! Like now we
  have 4 min video. We still can post one or two mins and at the end to check out yt channel has everything or something
  idk. But we can keep the tk and ig short and YouTube 4 mins". Done the same morning (this chat):
  - Two cuts from one builder: python3 kit/show/build_survival.py <src> <out> full|short [thumb prep audio stills video
    mux qa] (files land in <out>/full and <out>/short; the cache is shared). FULL (YouTube) 264.83 s: the pilot with a
    YouTube ending ("The next world is coming. Subscribe, or the boss wins.", NEXT WORLD COMING, a SUBSCRIBE pill). SHORT
    (TikTok + Instagram) 78.67 s: cover, cold open, level 1 whole, three flashes of the other bosses ("Three more bosses
    are waiting."), a card ALL 4 LEVELS / ON YOUTUBE / @congratsengineer ("Watch all four levels on our YouTube channel,
    Congrats Engineer."), then "Subscribe, or the boss wins." (cut out of the third line at its real pause). Closing
    lines: kit/series/survivalpromo_lines.txt (voice.yml kit=survivalpromo). Both -14.0 LUFS, true peak under -2 dBFS,
    new lines within 4 ms of the plan, frames checked from the finished files. `thumb` draws a 1280x720 thumbnail.
    The voice JSON's word times are estimates (0.2 s off at a sentence break): snap_pauses() moves them onto the real
    silences for the closing lines.
  - Buffer cannot publish a video over 3 minutes to YouTube (its help page: such videos "can't be published
    automatically", they become phone notifications; no long-form support). Its YouTube limit is 2 posts per 24 hours
    on the free plan. So the full video went up in YouTube Studio through the owner's own Chrome (Claude in Chrome; he is
    signed in there; one Google login holds four channels: Yallah Say MA, Congrats Engineer, Yalla Say PS, Kef Tenbeni;
    switch with the account menu, and switch back when done). How, since the browser tool's file upload stops at 3.8 MB:
    push the file to a throwaway branch (`uploads`), open studio.youtube.com/channel/<id>/videos/upload?d=ud, and in the
    page fetch https://raw.githubusercontent.com/Falak-Labs/test/uploads/<file> (CORS is open there; the Pages address
    fails), wrap it in a File, set it on `ytcp-uploads-file-picker input[type=file]` with a DataTransfer and fire
    `change`. Title and description: focus `#title-textarea #textbox` / `#description-textarea #textbox`, select all,
    document.execCommand('insertText'). Thumbnail: the same File trick on `ytcp-thumbnail-uploader input#file-loader`.
    Radios by name (VIDEO_MADE_FOR_KIDS_NOT_MFK, VIDEO_PAID_PRODUCT_PLACEMENT_NO, VIDEO_HAS_ALTERED_CONTENT_NO, PRIVATE /
    PUBLIC), language under `#language-input`, then #next-button x3 and #done-button. Screenshots time out in that
    browser: read the DOM instead, and never print a URL with a query string (the tool blocks the whole answer).
  - Result: https://youtu.be/Z-o9Kc-oCe4 uploaded 18:00Z Nov 21 on Congrats Engineer, PRIVATE, 4:25, listed under Videos
    (not Shorts), checks "No issues found". Title "Survival Mode: Beat 4 Deadly Places With Zero Electricity"; the
    description has six chapters (0:00, 0:11, 1:09, 2:10, 3:11, 4:11); thumbnail set; not made for kids; no paid
    promotion; the AI question answered No (it asks about realistic fakes of people, places or events and AI music as
    the main focus; this is cartoon animation with background music); language English; category Education.
  - Making it PUBLIC was stopped by this chat's permission check (publishing through his browser needs his own yes;
    that is also what he agreed for browser posting: his OK before a batch goes public). He was asked. Until the video
    is public the short stays on hold: posts/sm01-survival.yml holds en.youtube (for good), en.tiktok and en.instagram
    (until the go; then set `at:` and drop those two from `hold`). media/sm01-survival-en.mp4 is 28 MB.
  - Numbers read in YouTube Studio (the first real ones): Congrats Engineer 50 subscribers (+50 in 28 days), 18.9K views
    and 124.7 watch hours in 28 days; latest Short (falaj) 813 views in 14.5 h, 73.1% average viewed. Its Earn page
    (data of Nov 16): fan-funding step 50 of 500 subscribers + 3 uploads (done) + 3,000 watch hours or 3M qualified
    Shorts views in 90 days (0 h, 8.3K views); ads step 50 of 1,000 subscribers + 4,000 hours or 10M (0 h, 8.3K). Shorts
    add nothing to the hours: only videos over 3 minutes do. Kef Tenbeni: 10 subscribers.
  - Open: a daily 4-minute episode still needs a builder that takes any four builds (levels, bosses, lines from a spec)
    and a workflow; the YouTube upload needs his computer on with Chrome open and his yes to publish; the Arabic version
    needs narration (ElevenLabs was almost empty on Nov 20). Idea to offer him: link the four builds' Shorts to the full
    video with the "Related video" field in Studio (a tappable link inside the Shorts player).

## Nov 21 2026 (midday run, 11:23 PT): 58 giant Ferris wheel, 59 Statue of Liberty, 60 microwave oven (for Sun Nov 22)
- TODAY Nov 21 PT, TOMORROW Sun Nov 22 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT with
  `TZ=America/Los_Angeles date -d` before the push). PST: Arabic 00:00 / 03:00 / 06:00 PT = 08:00Z / 11:00Z / 14:00Z;
  English 06:00 / 08:30 / 11:00 PT = 14:00Z / 16:30Z / 19:00Z Nov 22.
- Status 19:31Z (Nov 21 PT, builds 52-57): 52 and 53 all four live; 54 Arabic Instagram + YouTube and English
  Instagram + TikTok live, its Arabic TikTok refused ("potential spam", 14:00Z) and its English YouTube failed on the
  limit at 19:00Z (as planned: 41 + 44 in its window); 55 Arabic Instagram live, its Arabic TikTok refused (17:00Z); the
  rest of 55-57 scheduled ahead. A retry made in Buffer at 17:27Z Nov 21 (not ours) failed 45 / 46 / 49 English YouTube
  again. Old YouTube failures (EN 40, 45, 46, 49, 54; AR 41-45) stay failed: no 24 h window has room for them.
- NOT requeued by this run: 54 and 55's Arabic TikToks. The next free 2-hour gaps are 01:30Z / 04:30Z Nov 25, and the
  Arabic TikTok queue (10) only had room for this run's own three (37, 42, 45, 48, 49, 50, 57 + 58, 59, 60 = 10 at the
  push). The evening run of Nov 21 requeues them to 01:30Z / 04:30Z Nov 25 AFTER its own three Arabic TikToks are on
  Buffer (57 leaves at 23:00Z, 37 at 01:30Z and 45 at 04:30Z Nov 22; Buffer refuses a requeue while 10 are pending).
- Pages: retired ep51-ep53 (all posts sent): media/ 707 -> 591 MB before today's six videos, 719 MB after. Next to
  retire: 37 once its Arabic TikTok (01:30Z Nov 22) is out, 56 and 57 once all their posts are sent.
- A/B test: 59 is odd -> `liberty` in voices.yml ar_alt.kits (Mansour, Saudi script); 58 and 60 Egyptian.
- YouTube (2 SENT posts per channel in any rolling 24 h): Sun Nov 22 PT has room for ONE English and ONE Arabic post,
  because 57 (English 02:30Z, Arabic 23:00Z Nov 21) is in every Sunday window. Both went to 59, the strongest topic:
  English at its own slot 16:30Z (08:30 PT; window: only 57), Arabic with a per-platform at: {default: 11:00Z, youtube:
  14:20Z} (06:20 PT), 19 minutes after 54's send (14:01:09Z Nov 21) leaves the window, so only 57 is in it. 58 and 60
  hold YouTube. **The evening run of Nov 21 must hold YouTube in both languages** (every Sunday slot has 57 + 59 in its
  window). For the midday run of Nov 22 (Mon Nov 23): English 14:00Z passes (only 59 at 16:30Z Nov 22 in the window) and
  19:00Z passes (59 has left, only 14:00Z in it), 16:30Z fails; Arabic 08:00Z passes (only 59 at 14:20Z Nov 22), 11:00Z
  and 14:00Z fail, a youtube at: of 14:40Z or later passes. Check the status first: a retry made in Buffer can send an
  old failed post at any time and fill a window.
- Voices: Easton ferriswheel 64.42 s (229 words), liberty 65.96 s (230) -> three lines reworded after Whisper small
  ("in salty air" heard "and salty air", "shellac-soaked" -> "shellax", "a refund" -> "to refund") and English remade
  free: 66.73 s (231 words); microwave 65.51 s (229). ElevenLabs one take each: Egyptian ferriswheel 69.70 s (169
  words), Mansour liberty 73.78 s (167 words: long for Mansour, keep Saudi scripts near 160), Egyptian microwave 69.14 s
  (169). check_ar_voice: no weak lines (liberty line 12 30% and line 9 19% are digits and the Saudi "g" for qaf).
  ElevenLabs (MCP account_get_usage, 19:30Z Nov 21): still Creator, 101,993 of 127,949 used (25,956 left, reset Dec 12):
  only +144 since 03:40Z, so the other projects slowed down; about 2,700 more for these three.
- Research: WebSearch still gives titles and links only (no agents); facts were checked against result titles (NPS
  "Statue Statistics" and "Fun Facts", Smithsonian "The Statue of Liberty arrived in 350 pieces", Atlas Obscura "Well
  traveled before she reached her final home", NIST / copper.org on the 1980s restoration and the galvanic corrosion,
  Building "Millennium Wheel hoisted upright" and Mammoet's London Eye case, NPR / The National / Khaleej Times on Ain
  Dubai, Post-Gazette "When a Pittsburgher went to Chicago to beat France" on Ferris 1893, APS / IEEE Spectrum /
  Smithsonian on Percy Spencer, HyperPhysics and maketecheasier "flips an electric field 2.45 billion times a second")
  plus well-documented figures. Ain Dubai has been closed and reopened (Dec 2024) more than once: the scripts say what
  it is (250 m, 48 cabins, 38 minutes a turn), not that it is open today.
- Scenes (all v2 look 2):
  - ferriswheel.py (dubai, spokes, cabin, drive, lift, chicago, tag): wheel(c, t, rot, cabins, spokes, thick, buckle,
    glow, lit, legs, cab_n, bolted, cx, cy) = front view: two leg pairs, 64 laced cables (glow = the tension highlight),
    a rim of two rings with a zigzag truss, LEDs at night, 48 cabins outside the rim (cab_n hangs them one by one);
    thick + buckle = wagon-wheel beams bending at the bottom; cabin() = glass capsule (detail=True draws real people,
    ring= its own ring); island() with a boarding deck; bicycle(); gear(); tyre(); old_wheel() = Chicago 1893 with 36
    cars next to eiffel.eiffel(). Hook: the camera rises from the boarding deck to the whole wheel by "Dubai" (the
    "lift"). lift set: the wheel drawn with c.scale(1, sin(angle)) around its bottom edge = lying flat -> upright, cables
    from a mast; LONDON grey palette because a white wheel on the golden horizon disappears.
  - liberty.py (harbor, frame, skin, battery, paris, tag): statue(c, x, y, s, t, green, xray, crumple, sway, lit, steel,
    glint) = front view 300 units tall (robe with folds, raised arm, torch, tablet, crown of seven rays), green 0..1 =
    copper -> patina, xray shows Eiffel's pylon + the thin bars, crumple squashes the skin like foil; pedestal() = star
    fort + granite pedestal; hook = her copper face in a storm (STORMP palette, rain(), lightning()) pulling back to the
    whole statue, a two-coin inset; paris = 1884 over eiffel.rooftops, then pieces flying into crates on fridge.ship;
    tag EN: the ring and the green finger, "REFUND!"; AR: saudi_man + "وش هالغش؟!".
  - microwave.py (kitchen, fire, box, spots, door, lab, tag): oven(c, t, xray, door, light, running, waves, plate_ang,
    food, heat, display) = front view 560 x 340 (cavity, turntable, mug/bowl, mesh door, panel with display text),
    xray shows the magnetron + waveguide and bounce_path() rays drawn with wave_line() (a sine along a polyline);
    molecule() = a water V; magnetron(); first_oven() = the 1947 Radarange; hook = x-ray mug boiling with a magnifier of
    flipping molecules; spots = top view, hot/cold grid, burnt and frosted spots, then the turntable; door fix4 = two
    hooks + switches and an ON/OFF lamp; tag EN: stop at 0:01; AR: phone.mom + "ابعد عن الميكروويف!".
- Produce: one slug per run as each scene was ready (58 and 59 at 20:09Z, 60 at 20:11Z), about 20-26 minutes each.
  Final videos: ferriswheel EN 67.5 s / AR 72.8 s, liberty EN 69.9 s / AR 76.9 s (Mansour), microwave EN 68.6 s / AR
  72.2 s; all -14 LUFS, peaks -1.7 to -2.1 dBFS, covers in and inside the grid crop. Whisper small on the English
  mixes: number formats, "tyres" -> "tire", "door's" -> "doors", "replaced" -> "replace" (captions carry the words; the
  CI base.en also wrote "waits" -> "wakes", "melted" -> "knelt it", "bolt" -> "both", "wet" -> "what", which Whisper
  small heard right).
- Posts (post.yml on the push, state 20:44Z): all 14 targets of 58-60 "scheduled" at their Sun Nov 22 PT slots (every
  dueAt turned back into PT): 58 and 60 four each (YouTube held), 59 all six (Arabic YouTube 14:20Z = 06:20 PT). No
  Arabic TikTok had to wait. Pushed only after "pages build and deployment" for the last produce commit (2363b80)
  ended in success.
- Lessons: Camera.key(t, x, y, z, dur) starts moving AT t: to finish a pull-back on a word, start it early and let dur
  end on the word. A white or pale subject on the golden horizon washes out (the lift set): use a grey or dusk palette
  there. person(): the "point" hand is at (x + 40u*face, y - 150u) with u = h / 140 (put a held phone there).

## Nov 21 2026, afternoon (this chat): the 4-minute show goes daily, in English and Arabic
- The owner answered "Publish now" (14:07 PT) and wrote at 14:08 PT: "Let's keep the shorts too / The one you post on ig
  and tk post it on yt shorts too , and 4 min video. / We gonna do it daily. / So we gonna do daily 4 mins videos for yt
  'ar & en' plus the min short".
- Episode 1 (sm01, English only) is out: full video public 22:09Z https://youtu.be/Z-o9Kc-oCe4; short on YouTube Shorts
  22:13Z https://youtube.com/shorts/5N4qtsV9x6s (269 views in its first 55 minutes; the channel's Shorts get 100-800 in
  a day), on Instagram and TikTok 22:45Z (state/sm01-survival.json has the links).
- New: kit/show/build_show.py builds any episode from kit/show/specs/<id>.yml in `en` or `ar` (the old
  build_survival.py still builds the pilot). kit/show/README.md is the guide (pick, spec, lines, voices, build, post);
  kit/show/stock.py lists the builds still free by Arabic narrator (10 episodes in stock on Nov 21). The layer now
  draws Arabic (layout.text / fit / text_width route Arabic through bik.arabic with Tajawal; `side()` mirrors panels),
  takes every word from a table (layout.T, filled from the spec), has an icon library (layout.ICON), and finds its
  cues by word ("four", "congrats", ...) instead of fixed word numbers. sm01 through the new builder gives the same
  7,945 / 2,360 frames as the published files.
- Episode 2 (sm02) "You vs Water": panama, venice, aswan, palmjumeirah (all four Egyptian in Arabic). English full
  4:28.9, short 1:20.7; Arabic full 4:52.1, short 1:32.8; all -14.0 LUFS, true peak about -2 dBFS; frames of the four
  finished files checked. Voices: Easton 8 lines (one harmless diff, "tamed the" heard "tame the"; line 7 reworded
  after "The open sea." was heard wrong), Egyptian ElevenLabs 8 lines (521 characters; check_ar_voice 3-9% a line) and
  the three shared closing lines in Arabic (kit survivalpromo, 142 characters; line 1 scores 21% only because Whisper
  splits "زعماء").
- Posted for Sun Nov 22 PT. YouTube, uploaded in Studio and SCHEDULED there (they go public by themselves, the
  owner's computer can be off): Arabic full https://youtu.be/ugHmQS08wiY 09:00 PT (20:00 Riyadh), English full
  https://youtu.be/DUbMYDcOxaY 10:00 PT, Arabic Short https://youtube.com/shorts/jGhNKsbtOr4 10:30 PT, English Short
  https://youtube.com/shorts/ijimsOUeC9A 12:15 PT. Buffer (posts/sm02.yml): Arabic Instagram + TikTok 18:30Z, English
  Instagram + TikTok 20:15Z. post.py: `text:` may now be {default: ..., tiktok: ...} (the Arabic TikTok caption leaves
  out the word YouTube).
- YouTube Studio, more of the how-to (see the morning entry for the upload itself): channels Congrats Engineer
  UCDkfxHa7q5Ea0OoiSSi8DHA, Kef Tenbeni UC8qDuZpMDQXRrowaNp29vow; switch with the Account button > "Switch account" >
  the `ytd-account-item-renderer` whose text has the handle (the page reloads: read the result in a second call), and
  switch back to the channel you found it on (Yallah Say MA on Nov 21). To schedule: on the Visibility step click
  `#second-container-expand-button`, the date in `#datepicker-trigger` is already tomorrow (the browser is on Pacific
  time), put the time into `ytcp-datetime-picker #time-of-day-container input` (focus, select, insertText "10:00 AM",
  Enter, blur), wait until the progress label no longer says "Uploading", then `#done-button` (it reads "Schedule");
  the dialog answers "Your video will be set to public on ...". After the Next clicks the Details radios are gone from
  the DOM: read them before. A video over 3:00 lands under Videos, a shorter vertical one under Shorts
  (/videos/short). The "Related video" link on a Short is refused: "Only channel owner can gain access" (the Chrome
  login is a manager; the primary owner must finish YouTube's verification). Large files travel on the `uploads`
  branch: force-push one orphan commit with the files, fetch them in the page from raw.githubusercontent.com, then
  force-push an empty commit again (the proxy refuses to delete the branch).
- The permission check of this chat refused "Public" until the owner said yes; after his "We gonna do it daily" the
  four scheduled uploads went through. A run that is refused must leave the video private and tell him.
- ElevenLabs at 22:15Z, before episode 2's Arabic: 24,701 characters left, reset Dec 12. Six Arabic builds a day use
  2,500-5,400, the show about 520 more: the Arabic voice runs out in about a week, well before the reset. The owner
  was told with the options (Pro is $99 a month for 600,000; Creator is $22 for 121,000).
- For the build runs: see the new LINEUP rule (leave posts/sm*.yml and media/sm* alone; the show's Arabic TikTok and
  Instagram posts sit in the same Buffer queues as the builds).
- Daily task: "Build-It 4-minute show", every day 13:17 PT (created Nov 21 from this chat; first run Sun Nov 22 makes
  episode 3 for Mon Nov 23). It was created without a binding to the owner's computer ("runs in the cloud only"), so
  whether its session gets the Claude in Chrome tools is only known after the first run. If it does not, the run stops
  before YouTube, keeps the short cuts back and tells the owner; this chat looks at 15:40 PT on Nov 22 and can do the
  Studio uploads itself (its browser tools worked all day on Nov 21).
