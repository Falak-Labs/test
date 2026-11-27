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
- 16:10 PT, the owner, asked whether all six builds should go to YouTube Shorts through Studio or only the best two:
  "Ok let's keep buffer then for IG and TK / You got it boss". So YouTube leaves Buffer: see the new YouTube rule in
  LINEUP.md (every build to Shorts through Studio, Buffer as the fallback when the browser is out of reach). Done
  right away for the two builds of Sun Nov 22 that were on hold: 58 Ferris wheel (English 06:00 PT
  https://youtube.com/shorts/FWkyE8zhGCc, Arabic 00:00 PT https://youtube.com/shorts/Xp63m__gDB8) and 60 microwave
  (English 11:00 PT https://youtube.com/shorts/RScSVg5TLFU, Arabic 06:00 PT https://youtube.com/shorts/DDg7NsgvBJw),
  each scheduled in Studio from an upload sheet (scripts/yt_meta.py + the two calls in YOUTUBE_STUDIO_UPLOAD.md,
  section "Builds"; one browser_batch per video, about a minute each). 59 Statue of Liberty stays on Buffer's YouTube
  (already scheduled there), like 57 tonight. Builds 61-63 (the evening run of Nov 21) are the first to follow the
  new rule. Older builds that never reached YouTube (English 40, 45, 46, 49, 52-56; Arabic 41-45, 52-56) are NOT
  uploaded: the owner has not asked for the backlog.
- YOUTUBE_STUDIO_UPLOAD.md (repo root) is the guide for any chat; the owner pasted a short prompt pointing to it into
  another chat of his on Nov 21 (that chat posts long videos to its own channels, so check the channel name every time).

## Nov 21 2026 (evening run, 18:37 PT): 61 Leaning Tower of Pisa, 62 Bedouin tent, 63 washing machine (for Sun Nov 22)
- TODAY Nov 21 PT, TOMORROW Sun Nov 22 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT with
  `TZ=America/Los_Angeles date -d` before the push). PST: Arabic 09:00 / 12:00 / 15:00 PT = 17:00Z / 20:00Z / 23:00Z
  Nov 22; English 13:30 / 16:00 / 18:30 PT = 21:30Z Nov 22, 00:00Z / 02:30Z Nov 23.
- Status 02:43Z (Nov 21 PT, builds 52-57): six builds out in both languages (Instagram all twelve, English TikTok all
  six). English YouTube 57 FAILED at 02:30Z Nov 22 on the 2-in-24-h limit: a retry made in Buffer (not ours) sent the
  old failed 40 at 23:28:44Z Nov 21 (45, 46, 49 failed again at 23:29Z) and filled 57's window. Arabic TikTok 54, 55,
  56 refused ("potential spam"), 37's fourth try refused at 01:30Z Nov 22; 45 waits for 04:30Z Nov 22.
- YouTube: YouTube Studio was OUT OF REACH for this scheduled run (no Claude in Chrome / browser tools in the session,
  no desktop bridge), so the LINEUP fallback applied: Buffer for 2 builds per channel per PT day. Sunday has 59 (EN
  16:30Z, AR 14:20Z) and now 61 Pisa with per-platform at: EN youtube 23:50Z Nov 22 (15:50 PT; 40's send of 23:28:44Z
  Nov 21 has left the window, only 59 in it), AR youtube 23:20Z Nov 22 (15:20 PT; 57's send of 23:00:32Z Nov 21 has
  left, only 59 in it). 62 and 63 hold YouTube (and so stay off YouTube unless a chat with the browser uploads them).
  cmd=limits before the push: Sunday PT EN youtube scheduled 1, AR 1 (limit 2).
- For the midday run of Nov 22 (Mon Nov 23), if Studio is out of reach again: English 14:00Z and 16:30Z Nov 23 FAIL
  (59 at 16:30Z Nov 22 + 61 at 23:50Z Nov 22 in the window); a youtube at: of 16:50Z or later passes (only 61), e.g.
  its own 19:00Z slot: ONE English YouTube. Arabic 08:00Z, 11:00Z and 14:00Z Nov 23 FAIL (59 at 14:20Z + 61 at 23:20Z
  Nov 22); a youtube at: of 14:40Z Nov 23 (06:40 PT) or later passes: ONE Arabic YouTube. Check the status first:
  retries made in Buffer send old failed posts at any time and fill a window.
- Arabic TikTok: the show's sm02 sits at 18:30Z Nov 22, so 61's TikTok moved to 16:30Z (08:30 PT) and 62's to 20:30Z
  (12:30 PT), 2 h from it; 63 at 23:00Z. post.py counts the queue from state/: 61 and 62 go on at the push, 63 waits
  for the 08:20Z check-in (post.yml) once 58 has gone out.
- Requeues: the Arabic TikTok queue is full every night (the six builds + the show + the long-dated 48, 49 at 01:30Z /
  04:30Z Nov 23 and 50, 42 at 01:30Z / 04:30Z Nov 24), so one requeue a day at most fits without starving the next
  run's three. The 11:20Z check-in requeues 54 to 01:30Z Nov 25 (the first free 2-hour gap) if 59 has left room. Still
  in error for later runs: 55 (-> 04:30Z Nov 25), 37 and 56 (-> 01:30Z / 04:30Z Nov 26). Refusals (2-3 a day) arrive
  faster than the queue takes retries.
- Pages: retired ep40 (all sent) and ep41, ep43, ep44, ep46, whose only unsent targets were YouTube posts that failed
  on Buffer's limit and stay failed (no run requeues them; the owner has not asked for the YouTube backlog): media/
  774 -> 586 MB before tonight's six videos. Next to retire: 57 (only its failed EN YouTube is left), 45 after 04:30Z
  Nov 22, then 48-50 and 42 after their Arabic TikToks, 37 and 54-56 after their requeues.
- A/B test: 61 and 63 are odd -> `pisa`, `washer` in voices.yml ar_alt.kits (Mansour, Saudi scripts); 62 Egyptian.
- Voices: Easton pisa 65.55 s (226 words) after three free remakes: Whisper small heard "Bedouin tent" as "Badoo
  intent", "Pisa yourself" as "peace of yourself", "tilts it" as "tilted", "Pisa sits" as "pieces sits", "But build"
  as "Mabild". kit/tools/make_vo.py SAY now respells "bedouin" -> "bed-oo-in" and "pisa" -> "peesa" for Easton only
  (tested first with a throwaway 12-line kit, vtest61, langs=en, removed afterwards); three lines reworded. tent 64.0 s
  (227 words), washer 64.66 s (226). ElevenLabs one take each: Mansour pisa 66.56 s (162 words; line 2 remade after
  check_ar_voice heard "على طين" as "عالقين"), Egyptian tent 67.65 s (164), Mansour washer 69.06 s (160);
  check_ar_voice: only the digit stat lines over 30%. ElevenLabs (MCP account_get_usage, 03:58Z Nov 22): Creator,
  104,745 of 127,949 used (23,204 left, reset Dec 12): about four days of six Arabic voices.
- Research (WebSearch gives titles only; no agents): Pisa (ICE "Stabilising the Leaning Tower of Pisa", Ingenia,
  Britannica, History.com, Bristol 2018 "500-year-old Leaning Tower of Pisa mystery unveiled"): 1173, sinking by
  1178, almost a century's pause for wars, upper floors taller on the low side (curved), 5.5 deg and closed in 1990,
  600 t of lead in 1993, cables round the 3rd floor, about 38 m3 of soil drilled out 1999-2001 and 45 cm back, 56 m,
  14,500 t, 3.97 deg, at least four strong earthquakes since 1280 (dynamic soil-structure interaction). Bedouin tent
  (AramcoWorld "The Black Tent", Smithsonian Folklife, PBS, Saudipedia, UNESCO Al Sadu 2011 / 2020): goat hair woven
  by women in strips on a ground loom and sewn together, swells when wet, loose weave breathes, wall panels pinned,
  a curtain splits guests and family, packs onto camels; no figures I could check, so the stat is 0 nails, 0 bricks,
  1000s of years. Washing machine (HowStuffWorks, Whitegoods Help on concrete weights, The Henry Ford's Thor "circa
  1907"): drum with holes and paddles, surfactants, 1,400 rpm, about 500 g and about 130 km/h at the wall of a 48 cm
  drum (computed), about 25 kg of concrete, springs and shock absorbers, electric washers over a century ago.
- Scenes (all v2 look 2):
  - pisa.py (piazza, ground, floors, lead, drill, quake, tag): tower(c, x, y, s, t, lean, bend, built, lit, wedge) =
    eight floors (blind-arcade base, six galleries of columns and arches, the bell chamber); floor_frames() chains a
    numpy affine per floor, each upper floor tilted back about its bottom-LEFT corner (BEND) with the gap filled by a
    wedge (yellow with wedge=1) = built taller on the low side; tower_top() = the top centre. ghost() = dashed outline
    of the straight tower: the hook tips the tower from it to 3.97 deg (e_back) and stops. soil() = cut-open silt, soft
    clay (firm, wob = earthquake jelly) and sand; foundation(), ingots(), drill(), wedge_diagram() (two floors close
    up), wardrobe() (AR tag, cardboard under the lifted foot), viewfinder() (EN tag, a tourist "holding it up").
  - tent.py (camp, sun, weave, wind, move, loom, tag): tent(c, t, ...) = black goat-hair tent 900 wide, front view:
    roof_pts() with three pole peaks and sagging cloth, eave_pts(), strips and hairy texture clipped to the roof, rug,
    cushions, sadu_band() curtain, fire + dallah, people (duck=True in the sand), wall panels, thin=1 = a white tent;
    goat(), umbrella(flip), weave(swell) close-up. Camera zoom about 1.6 with the ground near y 1200.
  - washer.py (laundry, soak, soap, spin, walk, old, tag): machine(c, t, x, xray, ang, spin, water, towel, parts, rot,
    fly, foam) = front loader 420 x 540, porthole, drum holes, paddles, tumble_pos() (garments ride up and drop),
    spin = a blurred colour ring; xray shows the tub, springs, shock absorbers, concrete block, motor. rpm_gauge() (a
    rev counter: bullettrain.gauge always prints km/h). soap_mol() = water-loving head + grease-loving tail.
- Lessons: a wide, low subject (a tent) needs a tight camera that crops its sides; a white subject (the washer) vanished
  on light tiles, so the set went dark steel blue; run Whisper small on a closer whose name ends right before
  "yourself" (it blends) and test respellings with a throwaway English kit (free) before the real remake.
- Produce: one slug per run, all three dispatched together at 03:50Z (renders landed 04:13-04:16Z). Final videos: pisa
  EN 68.7 s / AR 69.7 s, tent EN 67.1 s / AR 70.7 s, washer EN 67.8 s / AR 72.1 s; all -14 LUFS, peaks -1.8 to -2.3
  dBFS, covers in and inside the grid crop. Whisper small on the English mixes (tools: a 30-line script that builds
  the episode's Timeline and cuts each beat from the mp4's audio): number formats and homophones, plus the tent hook's
  "weave" heard as "leave"; the hook rain went from -14 to -23 dB and the English was rendered again (langs=en,
  force=true, 04:36Z) but Whisper still writes "leave" (the caption carries it). CI's base.en mix check also writes
  "Pisa" as "pizza" and "Bedouin tent" as "bedu intent": Whisper small hears both right on the voice and the mix.
- Posts (state 04:46Z): 13 of 14 targets "scheduled" at their Sun Nov 22 PT slots (every dueAt turned back into PT):
  61 all six (YouTube on Buffer EN 15:50, AR 15:20 PT), 62 and 63 four each minus 63's Arabic TikTok, which "waits"
  (10 queued) until 58 has gone out: a send_later check-in at 11:20Z Nov 22 (trig_01HXvQXkoLfnQnSBb8xUQC2S) dispatches
  post.yml and requeues 54's Arabic TikTok to 01:30Z Nov 25 if the queue has room. The midday run's own pushes also
  add it. Pushed 61 after "pages build and deployment" for 199607d succeeded, 62 and 63 after the one for 6f6e540.

## Nov 21 2026, 21:20-22:00 PT (main chat): runs have no browser, YouTube's daily limit, the YouTube desk
- The owner asked whether every scheduled run follows the new plan. Two findings changed the YouTube part of it.
- (1) Scheduled runs get NO browser (the evening run above found no Claude in Chrome tools). Only the main chat (the
  one the owner talks to; session_013LqBzNLVgZe7hUsTDVUKn7) reaches his Chrome. So no run uploads to YouTube Studio
  any more; the main chat does it in two rounds a day, about 16:45 and 21:30 PT ("The desk" in
  YOUTUBE_STUDIO_UPLOAD.md; `scripts/yt_desk.py plan | done | refused | release | check`; record of uploads
  `youtube/ledger.json`; settings `youtube/desk.yml`).
- (2) YouTube's daily limit. At 21:30 PT the main chat tried builds 62 and 63 in Studio: both channels answered "Daily
  upload limit reached. Upload more videos daily after a one-time verification or wait 24 hours." The login had made
  10 Studio uploads since about 13:40 PT (sm01 full + short, sm02 four, builds 58 and 60 in both languages: 6 English,
  4 Arabic). The same evening the owner's other new channels were refused (The Dark Told Me 18:28 PT, Yalla Say PS
  18:39 and 18:51 PT), while Yallah Say MA, whose Advanced features are enabled, uploaded at 18:42 PT. Uploads through
  Buffer still worked (they are counted apart). Studio > Settings > Channel > Feature eligibility on Congrats
  Engineer and on Kef Tenbeni: Standard and Intermediate "Enabled", Advanced "Eligible" (it lists "Upload more videos
  daily" and "Eligible to apply for monetization"; requirements: video verification OR valid ID OR channel history;
  "Only channel owners can complete the one-time verification"; this Chrome login gets no button). The owner was told
  at 21:40 PT: the verification is his to do, and it is also needed before he can apply for monetization.
- So until `youtube/desk.yml` says `verified: true`: about 10 Studio uploads per rolling 24 hours for ALL his
  unverified channels. Build-It uploads 6 a Pacific day in Studio (`per_day`: the show's four + one build in both
  languages), which leaves 2 for his other channels (a scary-stories retry is set for Sun Nov 22 18:50 PT) and 2 spare,
  because the 24 hours roll. Each run: build #1 on Buffer's YouTube, build #2 held with `studio: 1`, build #3 held with
  `studio: 2` (the YouTube rule in LINEUP.md). In a normal day that puts 3 of the 6 builds on YouTube in both
  languages (2 through Buffer, 1 through Studio: the midday run's #2) plus the show; the evening run's #2 and both #3
  go up only when the day has room (for example when the show did not come).
- This replaces the Buffer advice in the evening note above only in one point: the midday run of Nov 22 still puts ONE
  build on Buffer's YouTube per language (English 16:50Z Nov 23 or later, Arabic 14:40Z Nov 23 or later, as computed
  there), and marks the other two `studio: 1` / `studio: 2`.
- Builds 62 and 63 (Sun Nov 22) stay off YouTube: no room in Sunday's limit. They join the builds that never reached
  YouTube (English 45, 46, 49, 52-57, 62, 63; Arabic 41-45, 52-56, 62, 63). The owner has not asked for that backlog;
  once he is verified it can go up a few a day.
- The show: the 13:17 run no longer needs a browser. It writes `kit/show/youtube/<id>.yml` (titles, descriptions,
  chapter labels), pushes media + posts with ALL six targets on hold, and runs `kit/show/handoff.py` (full cuts,
  thumbnails and sheet.json on the `show` branch; build_show.py's qa step now writes qa.json with the chapter times).
  The main chat uploads the four videos at 16:45 PT and then releases the TikTok and Instagram posts.
- Studio was found on The Dark Told Me (another chat had switched it) and was left there. The login now shows six
  channels (list in the guide). Congrats Engineer showed 56 subscribers at 21:30 PT (50 that morning).
- New call 2 in the guide stops by itself on a refusal (`.error-short` in the upload dialog); a thumbnail call for
  entries with `thumb`. Not yet run: the thumbnail call as a snippet, and handoff.py's push (its --no-push test with
  sm02's files passed).
- Scheduled tasks after 21:55 PT Nov 21: the three daily ones were rewritten to this arrangement (midday 11:23,
  show 13:17, evening 18:37 PT; none looks for a browser any more). The main chat's rounds: afternoon
  trig_012mzGGsMXgjfgBJeBV4kwFM (Sun Nov 22 16:45 PT) and evening trig_01P7og3RBmFU4kwBMyfXFUFB (Sun 21:30 PT); each
  round sets its own next day. An older check-in of the main chat stays at Sun 15:40 PT with its old wording
  (trig_0116ag8a4Z6po2KjC929Z5CK; rewriting it was refused): when it fires, do the desk round as the guide says.
  The project docs claude/build-it-money-plan.md and claude/build-it-4-minute-show.md carry the same facts.
- Wake-up test, Nov 21 21:58 PT (send_later into the main chat, trig_01LMFLZkL4dQJ4aG7c2A2JeE): the turn it started had the Claude in
  Chrome tools; tabs_context_mcp answered (the tab group was gone, as left) and list_connected_browsers showed
  "Browser 1" (Linux) connected and in use. No tab was opened. So the main chat's scheduled rounds can reach the
  owner's Chrome while it is open; a full upload from a wake-up is first tried on Sun Nov 22 (15:40 / 16:45 PT).
- Check-in Sun Nov 22 03:20 PT (11:20Z, the evening run's trig_01HXvQXkoLfnQnSBb8xUQC2S): 58 and 59 Arabic Instagram +
  TikTok sent (08:00Z, 11:00Z); every other 58-63 target scheduled for Sun PT (62/63 YouTube held), no failures.
  post.yml added 63's Arabic TikTok (23:00Z); requeue put 54's Arabic TikTok at 01:30Z Nov 25. Arabic TikTok queue 10
  of 10 until 60, 61 and sm02 go out (by 18:30Z), which leaves 3 for the midday run; 55, 37, 56 still in error.

## Nov 22 11:00 PT: both channels verified
Owner did the Advanced features verification on Congrats Engineer and Kef Tenbeni; Studio shows Advanced features: Enabled on both. youtube/desk.yml now says verified: true (the daily upload cap should be lifted; if Studio still answers "Daily upload limit reached", run yt_desk.py refused en|ar and set verified back to false).

## Nov 22 11:25 PT: ElevenLabs is now Pro, the credit rules (owner's words: "be very smart how to use credits and save more for other chats but keep the quality. Always save voice that you gonna reuse in the future so you don't need to recreate them. Be smart how to have longer videos but smart use of credits")
- Plan: Pro, 613,234 characters (credits) a month, resets Dec 22 2026 (reset 1797966947). Used so far: 1,792. Shared with the owner's other chats (scary stories, Yallah Say, others).
- BUILD-IT BUDGET: at most 8,000 characters a day in all (about 240,000 a month, under 40% of the plan). A normal day is about 5,900 (six Arabic builds at about 900 plus the show's Arabic at about 520). The rest of the plan belongs to the other chats.
- Before any voice job, a run reads the balance (elevenlabs account_get_usage). If the account has used more than 75% of its limit, or over 60% of the limit before the 15th of the period, make English only and tell the owner. Never go into overage.
- Quality stays: model eleven_multilingual_v2 for every Arabic line that ships. No cheaper model (flash/turbo) for shipping lines.
- SAVE AND REUSE: every generated line is a saved take (kit/series/voice/KIT_ar_sa.json + .wav, per line). Never make a voice again when its files exist; change one line, make only that line (tools make_vo_eleven.py already works per line). Re-rendering video from saved voice costs nothing. Time scripts with the saved takes or word counts, not with test generations. Voice IDs live in voices.yml (do not invent new voices: IES4nrmZdUBHByLBde0P Egyptian, 5HAezIQAaoSgJypcI0NP Saudi A/B). A new voice is tried once on a 150-character sample, and the winner goes into voices.yml the same day.
- No retries by hand through the elevenlabs connector's speech tool (it bills twice): voices are made only by the voice.yml/produce workflows.
- LONGER VIDEOS, cheaply: length comes from the picture, not the narrator. English narration is free (Easton), so English may run long. The 4-minute show may grow to about 6 minutes (more level time, boss fights, a recap and results card) when the four builds give the material; Arabic narration for the show stays at or under 1,500 characters a day. Builds stay 62-71 s. Do not pad lines to fill time.
- English on ElevenLabs would cost about 1,300 a build (7,800 a day): over budget for builds. Only the show's English could move to it (about 600 a day) if the owner picks a voice.

## Nov 22 11:35 PT: voices (owner: "keep Easton for all English videos. And only ElevenLabs for Arabic, not the Egyptian one")
- English: free Phonon Easton for every English video, builds and show. No ElevenLabs English.
- Arabic: ElevenLabs only, and from build 64 on EVERY new Arabic voice is Saudi Mansour (voices.yml ar = 5HAezIQAaoSgJypcI0NP, dialect saudi). Never the Egyptian voice for anything new. Scripts in the Saudi dialect: hook "لو ...، مبروك، كذا سويت لك ...", line 10 "بس قبل لا ...، تابعني، لأن الجاي بنبني ...", closer "ومبروك، كذا سويت لك ... بيدك"; Saudi everyday words (وش، كذا، زين، مرة، الحين، يبي، ما يسوى), humour from Saudi daily life; 150-160 words (Mansour reads slower). Old Egyptian builds stay as they are (already posted; nothing is remade).
- The 4-minute show: its Arabic cut plays the builds' own voices, so pick all four levels from the Mansour group (stock.py now counts every build from 64 as Mansour); the show's own Arabic lines are read by Mansour too. Until four free Mansour builds share an idea, take them from the odd builds 41-63.

## Nov 22 2026 (midday run, 11:23 PT): 64 Big Ben's clock, 65 Shibam, 66 Tower Bridge (for Mon Nov 23)
- TODAY Nov 22 PT, TOMORROW Mon Nov 23 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT with
  `TZ=America/Los_Angeles date -d` before the push). PST: Arabic 00:00 / 03:00 / 06:00 PT = 08:00Z / 11:00Z / 14:00Z;
  English 06:00 / 08:30 / 11:00 PT = 14:00Z / 16:30Z / 19:00Z Nov 23.
- Status 19:28Z (builds 58-63): 58 and 59 all out, 60 all but its Arabic TikTok ("potential spam" 14:00Z), 61 Arabic
  Instagram + TikTok out, 61-63 rest scheduled for the afternoon, sm02 Arabic out. Requeued 55's Arabic TikTok to
  04:30Z Nov 25 (the evening run's plan). Still in error: 37, 56, 60 (Arabic TikTok; one requeue a day fits the
  10-post queue: next free 2-hour gaps 01:30Z / 04:30Z Nov 26, then Nov 27). yt_desk check: nothing overdue.
- YouTube: desk.yml says verified: true (owner, Nov 22 11:00 PT), so all three builds carry `hold: [en.youtube,
  ar.youtube]` + `studio: 1` and nothing goes to YouTube through Buffer.
- Voices: the owner's call of 11:35 PT came in while this run was writing (another session changed voices.yml):
  every new Arabic voice is Saudi Mansour. 64 and 66 had been written in Egyptian: both were rewritten in Saudi
  dialect BEFORE any voice was made (no credits lost). Mansour, one take each: bigben 66.00 s (161 words, x1.11),
  shibam 68.86 s (160 words, hit the x1.12 cap), towerbridge 66.01 s (160 words); towerbridge line 4 "بس كل نص وزنه"
  was heard as "كلنا الصوزنا" by check_ar_voice (26%) and became "بس الواحد منهم يوزن أكثر من ألف طن" (one line remade,
  36 characters). Other lines: only the digit stat lines over 20%. Credits: about 2,600 characters for the three
  (ElevenLabs Pro: 19,234 of 613,234 used at 20:55Z, reset Dec 22). Easton: bigben 66.05 s (230 words), shibam 66.45 s
  (230), towerbridge 64.66 s (231). kit/tools/make_vo.py SAY now respells "shibam" -> "shee-bahm" for Easton; Whisper
  small writes it "She-Bomb", which is how "shi-BAAM" sounds in American English (the caption carries SHIBAM).
- Research (WebSearch titles only, no agents): parliament.uk "Great Clock facts" / "Great Clock adjustments",
  Britannica, Seiko museum "The escapement of Big Ben", scienceblog on the 1859 crack; Wikipedia / National Geographic /
  Atlas Obscura / UNESCO on Shibam (about 500 tower houses, 5-11 storeys, some over 30 m, mostly 16th century, re-mudded,
  lime tops); towerbridge.org.uk "How does Tower Bridge work?" and "The day a bus jumped over Tower Bridge" (Albert
  Gunter, Dec 1952), Wikipedia on the bascules (over 1,000 t each, counterweights, hydraulic accumulators, 42 m walkways,
  about 800 lifts a year, free).
- Scenes (all v2 look 2):
  - bigben.py (pend, tower, airy, escape, hands, bell, tag): elizabeth(c, t, lit, dusk, hour, minute) = the clock tower
    front view 960 units (dial at y -585, r 36), palace(), london_eye(); dial(c, x, y, r, hour, minute, lit, hand_kind
    blue|iron|copper, detail, min_ang) at any size (Roman numerals over r 60); pendulum(c, px, py, L, t, ang, pennies,
    heat, cold, stretch) = rod, penny shelf (fractional pennies drop in), bob; hand_drop(); escape_wheel() (double
    three-legged), gear(), observatory(), great_bell(crack, ring, hammer), bed_scene(rtl, spin). Hook: the giant dial
    lit from BEHIND (mirrored numerals) over the swinging pendulum while a hand drops a penny, then a cut on "famous"
    to the dial and out to the whole tower over the Palace at dusk.
  - shibam.py (wadi, flood, plan, wall, rain, inside, tag): CITY = three rows of tower houses from a fixed seed;
    tower_house(c, x, y, w, floors, t, built, lime, seed, dark, melt, lit, taper) (3 m floors, lime only on the top
    floor: more white blooms the frame out), mound(), city_wall(), cliffs() (screen parallax), flood_water(level, front),
    section() (a cut tower: crush / taper), ny_ghost() (dashed 1930s skyline). break2 is a TOP view of the mound with
    houses spilling off it. Lesson: towers that start below the city wall's height are hidden behind it, so the hook's
    first frame was empty until they started at half height, centre first.
  - towerbridge.py (river, map, pier, engine, walk, bus, tag): side view, 1 m = 10 units, road y 0, river 90; tower()
    (cut + stairs), pier(cut), leaf(side, ang, tail, cw) = a bascule turning about (+-300, 14) with rotate(side*ang),
    leaf_tip()/on_leaf(), walkways(people), chains(), front_water() (draw AFTER the piers so they stand in the water),
    ship_bow() (a tall ship bow-on, behind the bridge while scale < 1, in front after), bus() (a red double-decker),
    thames_map(), engine_room(on, fill, release) + leaf_inset(). The raised leaves stand just inside the towers' inner
    faces: draw them AFTER the towers or they vanish; the bus crossing on the road is clipped out where it passes
    through the towers. A pale stone bridge on the golden horizon washed out: the hook uses a dusk palette (DUSKP).
- Produce: one slug per run (64 and 66 at 20:17Z, 65 at 20:24Z), 20-22 minutes each. Final videos: bigben EN 69.2 s /
  AR 69.1 s, shibam EN 69.6 s / AR 72.0 s, towerbridge EN 67.8 s / AR 69.1 s; all -14 LUFS, peaks -2.0 to -2.2 dBFS,
  covers in and inside the grid crop. Whisper small on the English mixes: number formats, "checked twice" -> "check
  twice", "cracked today" -> "crack today", Shibam -> "She-Bomb", Tower Bridge's "heavy end" -> "heavy and" (caption
  carries it). CI base.en also wrote "heat and cold" -> "he and Cole", "roars" -> "wars", "lives" -> "lets": Whisper
  small hears those right on the mix.
- Pages: retired ep45 and ep57 (only failed Buffer YouTube posts left) and ep58, ep59 (all sent): media/ 711 -> 547 MB
  before today's six videos (about 650 MB after). Next to retire: 61-63 once all their posts are out, 60 and 37 after
  their Arabic TikTok requeues, 42, 48-50, 54-56 after theirs.
- Posts: pushed 64 + 66 after "pages build and deployment" for 1d2d79b succeeded, 65 after the one for eee6a87.
  Lineup: four ideas appended (73 the Lighthouse of Alexandria, 74 Maraya in AlUla, 75 Chand Baori, 76 a pressure cooker).

## Nov 22 2026 (show run, 13:17 PT): Survival Mode 3 "You vs Gravity" (sm03) for Mon Nov 23
- TODAY Sun Nov 22 PT, TOMORROW Mon Nov 23 PT. Hand-off done 14:08 PT (the whole run took under an hour; the four cuts
  render in about 18 minutes when the English and the Arabic chain run side by side on the 2 CPUs).
- Step 0: status 21:24Z: sm02's four TikTok + Instagram posts all sent (links in state/sm02.json), nothing to requeue.
  yt_desk check: nothing overdue (the `show` branch did not exist before this run: its hand-off is the first real push).
- Pick: pisa, machupicchu, operahouse, liberty (all Mansour). Gravity's four moves: it tips (Pisa), slides (Machu Picchu),
  is too heavy (Sydney's 15-tonne pieces), crumples (Liberty's skin as thin as two coins). Left out on purpose: 64-66 (they
  post as builds on the same day), hagiasophia (a religious building: the show rule), burjalarab (too close to sm02's Palm
  Jumeirah). Stock left in the Mansour group: barrier, greatwall, hagiasophia, burjalarab, fridge, suez, washer, bigben,
  shibam, towerbridge = two episodes (ideas: You vs the Sea = barrier, burjalarab, suez, towerbridge; You vs Time = bigben,
  shibam, greatwall + one more; a home-appliances world once 69 and 71 exist).
- The local clone is shallow (51 commits): fetch found machupicchu, operahouse, liberty in git history only because they
  were retired today. barrier, greatwall, burjalarab, fridge need `git fetch --deepen` first (README).
- First Saudi episode. Arabic closing lines in Saudi dialect: new kit survivalpromosa ("باقي قدامك ثلاثة زعماء." / "شوف
  المراحل الأربع كلها على قناتنا في يوتيوب، كيف تنبني." / "العالم الجاي قريب. اشترك، ولا الزعيم يفوز."), spec `ar:` block
  `promo: survivalpromosa`, `or_boss`, `next`. voices.yml untouched (its `ar` is Mansour already).
- New, tempo: the length window of make_vo_eleven.py slowed the show's 8-line Arabic script to x0.92 (sm02), while the
  builds around it play Mansour at x1.04 to x1.12. Now make_vo_eleven.py takes `--tempo` and scripts/make_voices.py
  (`show_tempo`) gives a show kit the mean tempo of its four builds (sm03: x1.12) and survivalpromo* kits x1.12. Builds
  are not touched by it.
- Voices: balance read first (19,234 of 613,234, 3%). Easton 42.76 s, 140 words: CI Whisper base.en and local Whisper
  small both differ only on homophones ("mud slides" -> "mudslides", "sails" -> "sales", "tonnes" -> "tons"); nothing
  reworded. Mansour: 8 lines, 611 characters, 49.98 s at x1.12, check_ar_voice 0-9% a line; closing lines 121 characters,
  2-5%. Whisper writes his qaf as g ("جدامك", "جريب"): the Saudi sound. 732 characters asked for in all; the account's
  counter read 19,588 afterwards.
- New in the layer: icons `rock`, `flat`, `down` (layout.ICON); spec keys `shot` / `still` now set for every level,
  because the default (the end of the hook) was two floors of the tower, a bare slope, a blueprint board. Liberty's
  camera pulls back earlier in the Arabic build, so its shot is per language (en 2.6, ar 1.85).
- Cuts (all -14.0 LUFS): English full 4:37.1 (true peak -2.3 dBFS, 86.8 MB, chapters 0:00 0:11 1:13 2:15 3:17 4:21),
  short 1:22.3 (-2.2, 39.5 MB); Arabic full 4:56.7 (-2.1, 88.6 MB, chapters 0:00 0:13 1:16 2:23 3:29 4:39), short 1:26.1
  (-2.0, 40.7 MB). Stills sheets and 140 frames pulled from the four finished files looked at (words, Arabic right to
  left, the right boss on each level); Whisper small on the finished mixes hears every new line in its place.
- Hand-off: media/sm03-en.mp4 + media/sm03-ar.mp4 and posts/sm03.yml on main with ALL six targets on hold (the Post
  workflow ran: state/sm03.json has no targets). kit/show/youtube/sm03.yml -> handoff.py pushed the two full cuts, the two
  thumbnails and sheet.json to the `show` branch (28c1b1f); every raw link answers 200 and `yt_desk.py plan` lists the
  four videos first. For Mon Nov 23 PT: Arabic full 09:00, English full 10:00, Arabic Short 10:30, English Short 12:15
  (YouTube, the main chat's 16:45 PT round); TikTok + Instagram Arabic 10:30 (18:30Z), English 12:15 (20:15Z) after
  `yt_desk.py release sm03`.
- For the build runs: media/sm01-survival-en.mp4 and media/sm02-*.mp4 may be retired (all their posts are sent, their
  YouTube uploads are in the ledger); media/sm03-* stays until its four posts are out.

## Nov 22 16:00 PT: desk round done early (check-in 15:40)
Verified: true worked: all 10 Studio uploads for Nov 23 went through with no daily-limit refusal (sm03 full+short and builds 64-66, both channels). Ledger updated, sm03 released, state/sm03.json has all four TikTok/Instagram targets scheduled (AR 18:30Z, EN 20:15Z). Episode 2 (sm02) is public everywhere. Studio showed "We are still checking your content" after Schedule: click "Got it" (the call 2 script now does it).

## Nov 22 2026 (evening run, 18:37 PT): 67 the Colosseum, 68 Taipei 101, 69 a dishwasher (for Mon Nov 23)
- TODAY Sun Nov 22 PT, TOMORROW Mon Nov 23 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT
  before the push). PST: Arabic Instagram 09:00 / 12:00 / 15:00 PT = 17:00Z / 20:00Z / 23:00Z Nov 23, Arabic TikTok
  08:30 / 12:30 / 15:00 PT (2 h either side of the show's Arabic TikTok at 10:30 PT); English 13:30 / 16:00 / 18:30 PT =
  21:30Z Nov 23, 00:00Z / 02:30Z Nov 24. YouTube: desk.yml verified: true, so all three hold YouTube with `studio: 1`.
- Status 02:49Z (Nov 22 PT, builds 58-63): six builds out. English Instagram + TikTok all twelve, Arabic Instagram all
  six, Arabic TikTok four (60 and 62 "potential spam"; 48's requeue refused again at 01:30Z Nov 23). YouTube: 59 and 61
  through Buffer, 58 and 60 in Studio, 62 and 63 none (as planned). yt_desk check: nothing overdue.
- Arabic TikTok in error: 37, 48, 56, 60, 62. The queue held 9 of 10 (49 at 04:30Z Nov 23, 64-66, sm03, 50 and 42 on
  Nov 24, 54 and 55 on Nov 25), so nothing was requeued at once: the check-in at 11:20Z Nov 23 (03:20 PT) dispatches
  post.yml for this run's waiting Arabic TikToks and requeues ONE error (60 -> 01:30Z Nov 26); the rest one a day
  (04:30Z Nov 26, then 01:30Z / 04:30Z Nov 27 ...). Old failed Buffer YouTube posts are left alone (verified channels:
  YouTube is Studio's job now).
- Metrics 02:54Z: 198,833 views (+14,176). English TikTok nearly stopped showing new posts since Nov 21 (52-59 median 6
  views; only the Eiffel Tower broke out, 944). English Instagram pushed only 2 of Nov 21's six. Arabic Instagram builds
  52-57 median 1,162. Entry in claude/build-it-performance.md.
- ElevenLabs Pro: 19,588 of 613,234 used before the voices (3%); three Mansour voices 882 + 879 + 860 characters.
- New tool: kit/tools/check_en_voice.py (Whisper small, line by line, the Nov 15 method; also takes a mix: `... <kit>
  mix.wav lead=0.5`). It caught "masts" -> "masks" (now "poles"), "want out" -> "went out" (now "try to leave") and "Abu
  Dhabi" -> "Abu Dhabi Dhabi" (line 10 of 69 now "a dome that rains light"). SAY now maps "101" -> "one-oh-one", so the
  script, the captions and the cover keep "TAIPEI 101" while Easton says it right.
- Anchor lesson: English keys match by START of word, so "SHADE" found "shaded" first; colosseum.py takes the second
  match for English (`self.w("tag", "SHADE", 0.95, nth=1)`). Check that no key is the start of an earlier word in its line.
- Scenes (all v2 look 2):
  - colosseum.py (section, ring, gates, ruin, tag): section() = the amphitheatre cut across its short axis (STEPS seat
    profile, crowd_on_steps, the outer wall with corridors, masts + sailcloth that slides out from them, wind that fills
    it, ropes down to stone posts, the hypogeum with shafts, cages, capstans and men, a lion on the lift); ring() = the
    whole ellipse from outside and above, 40 bays a side on three tiers + attic, half columns, cornices, the bowl and
    crowd, the awning (only the back panels, so the bowl stays visible), gate numerals, crowd jam / flow, holes, and
    `broken` for the ring today. Hook: sails pulled over the crowd, a lion rising through a trapdoor, then a whip to the
    ring at "congrats". Tag: a parking lot from above, one tree, a car circling (AR: "تدوّر موقف بظل").
  - taipei.py (city, room, ball, tag): tower() in elevation (1 m = 2 units) bending with `sway` (offset grows with height
    squared), eight flared sections, a cut window with the ball (drawn larger than life); bamboo(); seismo(); fireworks
    for the closer (and the cover); draw_ball_room() = the damper floors in screen space: ball on four cables, four
    pistons, visitors, storm windows, `frame` tilts the floors (in step = growing, against = dying). Tag: a car hits a
    speed bump and the cup in the inset empties (AR: a tea glass on a white thobe).
  - dishwasher.py (kitchen, sink, box, arms, enzyme, old, tag): machine() front view with xray / door: two racks, plates
    (mid-tone colours: light plates bloom into white discs in the finishing pass), two spray arms foreshortened with jets,
    the sump puddle, scraps pulled into the filter, pump, heater, pipe with dash_line flow; sink() with a litre counter;
    arm_top() + sprinkler(); chain() + enzyme(); old_machine() + lady() + maid() for 1886. Tag: mom at the sink, the open
    machine as her drying rack (AR "نشّافة!").
- Pages: retired ep61 and ep63 (all posts sent): media/ 723 -> 640 MB before the six new videos (about 760 MB after).
  Every other build still has an Arabic TikTok to requeue (37, 48, 56, 60, 62) or scheduled (42, 49, 50, 54, 55), and
  64-66 carry `studio:` with slots on Nov 23. media/sm* untouched (the build runs never retire the show's files).
- Produce (one slug per run, 17-26 minutes each): Colosseum EN 68.8 s / AR 70.2 s, Taipei EN 69.3 s / AR 73.0 s,
  dishwasher EN 67.9 s / AR 71.6 s; all -14 LUFS, peaks -2.0 to -2.4 dBFS, covers in and inside the grid crop.
  Whisper small on the mixes (`check_en_voice.py series/voice/<kit> mix.wav lead=0.5 pause=0.6`): number formats and
  homophones only ("sails" -> "sales"). Posts: 67 + 69 pushed after "pages build and deployment" for d4b10bf succeeded,
  68 after the one for e43b8f9. State 04:11Z: every Instagram + TikTok target scheduled on Mon Nov 23 PT except the
  Arabic TikToks of 68 and 69 (queue full): 68's added at 04:34Z by a post.yml dispatch after 49 left at 04:30Z (12:30 PT
  slot), 69's by the
  11:20Z check-in (send_later trig_014RdivAr2wbjiU92Wt1axfA, which also requeues 60's Arabic TikTok to 01:30Z Nov 26).
- Check-in Mon Nov 23 03:20 PT (11:20Z): status 11:22Z: 49's Arabic TikTok went out at 04:31Z (its requeue), 64-65
  Arabic all out; all 12 Instagram + TikTok targets of 67-69 scheduled on Mon Nov 23 PT after post.yml added 69's Arabic
  TikTok (15:00 PT); 60's Arabic TikTok requeued to 01:30Z Nov 26 (17:30 PT Wed Nov 25): queue 10 of 10 again. Still in
  error: 37, 48, 56, 62 (next free 2-hour gaps 04:30Z Nov 26, then 01:30Z / 04:30Z Nov 27).

## Nov 23 2026 (midday run, 11:23 PT): 70 the Louvre Abu Dhabi, 71 a vacuum cleaner, 72 the Petronas Twin Towers (for Tue Nov 24)
- TODAY Mon Nov 23 PT, TOMORROW Tue Nov 24 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT with
  `TZ=America/Los_Angeles date -d` before the push). PST: Arabic 00:00 / 03:00 / 06:00 PT = 08:00Z / 11:00Z / 14:00Z;
  English 06:00 / 08:30 / 11:00 PT = 14:00Z / 16:30Z / 19:00Z Nov 24. YouTube: desk.yml verified: true, so all three
  carry `hold: [en.youtube, ar.youtube]` + `studio: 1`.
- Status 19:28Z (builds 64-69 + sm03): 64 and 65 all out; 66 all but its Arabic TikTok ("potential spam" 14:00Z); 67
  Arabic Instagram out, Arabic TikTok refused (16:30Z), English 21:30Z; 68-69 scheduled for the afternoon; sm03 Arabic
  TikTok refused (18:30Z; the show run's job). Requeued 37's Arabic TikTok (fifth try) to 04:30Z Nov 26 (20:30 PT Wed).
  Still in error: Arabic TikTok 48, 56, 62, 66, 67 (+ sm03). Next free 2-hour gaps: 01:30Z / 04:30Z Nov 27, then Nov 28.
  Old failed Buffer YouTube posts (41-46, 49, 54, 57) left alone. yt_desk check: nothing overdue.
- ElevenLabs Pro: 20,859 of 613,234 used before the voices (3%). Mansour: louvre 879 characters + one remade line (L12
  "تحتها" was heard as "احتى" -> "تحت القبة"), vacuum 881, petronas 896, about 2,700 asked; the counter read 22,179 at 21:14Z.
- Voices: Easton louvre 64.29 s (226 words), vacuum 64.40 s (229), petronas 66.82 s (229; video 69.9 s, close to the
  70.5 s gate: keep Petronas-length scripts with four long numbers near 225 words). Mansour louvre 70.75 s, vacuum 71.41 s
  (x1.12 cap), petronas 69.00 s; check_ar_voice: only the digit stat lines flagged. Whisper small on the English voices:
  louvre L7 "rest it" -> "rested" (now "give it just four legs"), vacuum L9 "traps specks ... than a" (now "catches dust");
  English remade free. SAY now maps "nouvel" -> "noo-vel" (Whisper writes "Nouveau"); "Petronas" is written
  "Patronas"/"Patronus" (the right sound; the caption carries it).
- Research (WebSearch titles only, no agents): Louvre Abu Dhabi (louvreabudhabi.ae architecture, ArchDaily "engineering
  behind the dome", The National "final position for Louvre's 7000-tonne dome", "waterproofing work starts", "sea
  integration begins" / "museum on the sea" June 2016): 180 m, about 7,500 t, 7,850 stars in 8 layers (4 steel, 4
  aluminium), four hidden supports, the rain of light from palm-leaf roofs, 55 buildings like a medina, opened Nov 2017.
  Vacuum (Wikipedia / History.com / Smithsonian on Booth, Dyson's pages): Booth 1901, handkerchief on a dusty chair,
  'Puffing Billy' with hoses through windows; Dyson 5,127 prototypes, motors up to 125,000 rpm; HEPA 99.97% at 0.3 um.
  Petronas (Wikipedia, "Race to sky: How Japan, Korea built Malaysia's Twin Towers", FMT "5 fascinating facts", Otis):
  452 m, 88 floors, tallest 1998-2004, bridge on 41-42 at 170 m not bolted (slides), legs to floor 29, high-strength
  concrete (steel imports dear; twice the sway damping, twice the weight), site moved 60 m off cavernous limestone, 104
  piles up to 114 m, Hazama vs Samsung C&T / Kukdong.
- Scenes (all v2 look 2):
  - louvre.py (sea, plan, pit, beach): elevation 1 m = 4 units, sea level 0; dome lens d_top()/d_bot() (RX 360) with
    twinkling star holes, beams() = shafts + spots + falling specks (PLUS) through the holes, galleries() (BLD list,
    warm-lit at night), legs() x-ray, columns() forest, water() with the dome mirrored + sparkles; plan set =
    star_layers() (up to 8 lattices of eight-point stars on a sun disc), palm_top(), town_plan(); pit = a section with
    sheet piles, a pump, the yellow tub drawn with PathMeasure, the sea let back in; beach tag (umbrella from tent.py, dad
    = saudi_man in Arabic). Lessons: white galleries vanish on a pale noon sky (NOONP is deep blue now); Arabic labels need
    ASCII digits: Arabic-Indic digits come out reversed ("٤٥" was drawn "٥٤").
  - vacuum.py (room, can, carpet, bin, filter, street, tag): stick_vac() leaning ANG 28° (x-ray brush roll, crumbs up the
    wand, clear bin with a tornado and the dust level, motor fan, filter cap), rug(), room_bg(), broom() + dust_cloud(), a
    sealed can with air molecules + gauge(), fibres() + brush_roll(), a clogging bag vs a cyclone cone, the outlet +
    hair_mag(), Booth leaning onto the chair (person rotated 38°), booth_wagon() + horse(), robot_vac() + couch(). The stat
    camera zooms out (0.8) so the cards do not cover the vacuum.
  - petronas.py (city, ship, ground, bridge, race, tag): tower() in elevation (SECTIONS setbacks + pinnacle rings, sway
    grows with height squared, x-ray core + columns, the bridge slot), sky_bridge() (the deck keeps its length so its ends
    slide; legs to floor 29; bolts / bearings / snap), kl_city() with the KL Tower, ship() + price_tag(), a ground section
    at 2.2 px/m (limestone caves, the 60 m shift, 114 m piles), the race with crane() + flag() (jp / simplified kr), wifi().
    Lesson: lit silver towers blew out to white bars under the bloom: mid-grey SILVER, no add_glow on the towers.
- Produce: one slug per run (70 at 20:09Z, 71 at 20:23Z, 72 at 20:39Z): Louvre EN 67.4 s / AR 73.9 s, vacuum EN 67.5 /
  AR 74.5 s, Petronas EN 69.9 / AR 72.1 s; all -14 LUFS, peaks -1.9 to -2.8 dBFS, covers in and inside the grid crop.
  Whisper small on the mixes (`check_en_voice.py series/voice/<kit> mix.wav lead=0.5 pause=0.6`): number formats,
  a/the, Nouvel -> "Nouveau", Petronas -> "Patronas".
- Pages: retired ep49, ep64, ep65 (all posts sent; 64-65 in the Studio ledger): media/ 750 -> 651 MB before the six new
  videos (about 770 MB after). Next: 66-69 once their Arabic TikToks are out; 42, 50, 54, 55, 60, 37 after their requeues.
- Lineup: 80 Jeddah's giant sea fountain, 81 a zipper, 82 the Hong Kong-Zhuhai-Macau Bridge appended (checked by title).
- Arabic TikTok queue after 72: 10 of 10 (69, 50, 42, 54, 55, 60, 37, 70, 71, 72). Room comes back as 69 (23:00Z), 50
  (01:30Z), 42 (04:30Z) and 70 (08:00Z Nov 24) go out: the show's sm04 and the evening run's third Arabic TikTok may wait
  for a post.yml dispatch after one of those times.
- Status 21:22Z: 68's Arabic TikTok was refused too ("potential spam" at 20:30Z), 68's Arabic Instagram out at 20:03Z,
  66's English out at 19:05Z. Not requeued (the Arabic TikTok queue is 10 of 10). Arabic TikTok in error now: 48, 56,
  62, 66, 67, 68 (+ sm03). Free 2-hour gaps for them start at 01:30Z / 04:30Z Nov 27.

## Nov 23 2026, 13:55 PT: the hook rules (from build 73 on, both languages, both runs)
The owner brought a checklist ("I got this advice so let's check them out ... I don't want to stay stuck at 1,000 views,
so check if: specific clear hook, 3rd grade vocab, use names/numbers in hook, relatable topic, hook is NOT boring, cut
fluff, open loop"). The main chat checked builds 1-72 against it with state/metrics.json of Nov 23 02:54Z. Full study:
project doc claude/build-it-hook-checklist.md.
- What it found. Line 1 has drifted: builds 1-20 said it in 17 words and 4.2 s (Arabic 12 words, about 4 s), builds
  64-72 need 25 words and 6.6 s (Arabic 18 words, 6.8 s), two or three facts chained with commas, a 9th-grade sentence
  (builds 1-20: 5th grade). The first problem is now told by 10.6 s (was 8.4 s); the average TikTok viewer is gone by
  15 s in English and 11.6 s in Arabic. Same pace era (builds 1-39), short hook against long hook: English Instagram
  42% watched against 37% (29 s against 26 s) and 2,099 against 1,834 views; Arabic Instagram 32% against 29% and 286
  against 176 views; TikTok shows no difference. Small samples (15 to 24 posts a side), so this is a lean, not proof;
  the topic still decides more (turbine, wind tower, electric car and falaj were hits with long hooks). A number in the
  hook did not lift views by itself. The whole script's reading level (median grade 4.7) shows no link to watch time;
  the hook's does.
- THE RULES (write them into every new script; nothing already made is redone):
  1. Line 1: the series' frame stays ("If you ..., congrats, you just built X." / "لو ...، مبروك، كذا سويت لك ..."),
     but with ONE picture, no comma before "congrats" / "مبروك": at most 18 English words and 5.0 s spoken, at most 13
     Arabic words and 5.5 s. Words a nine-year-old uses. Models: "If you put a hotel on a boat, congrats, you just
     built a cruise ship." "If you build a train with a bird's beak for a nose, congrats, you just built a bullet train."
  2. The second fact you cut from line 1 (the number, the "then ...") opens line 2. The first problem must be fully
     told by 9.5 s in English and 10.0 s in Arabic.
  3. One name or one number in the hook is welcome when it fits in those words (the build's name is already on the
     cover frame); never both a number and a second clause.
  4. Open loop: line 2 tells the first danger AND raises one real question that only the reveal (line 11) answers; line
     11 answers it in its first sentence. A real fact, never an empty "wait for it". Example for Taipei 101: line 2
     "But typhoons hit this city every year. So why is it still standing?", line 11 "In twenty fifteen a typhoon
     swung the ball a full meter, and the tower stood calm."
  5. Plain words everywhere: aim for a reading grade of 4.5 or lower for the English script (the tool lists the long
     sentences and the 3-syllable words to swap; the build's own name and real part names may stay). Arabic: everyday
     Saudi words, one idea a sentence.
  6. Cut fluff: one fact a line, no stacked adjectives ("giant golden", "whole"), no line over 22 words.
  7. Relatable: the first number gets a comparison a child knows (cars, buses, a football field), and the topic rules
     of claude/build-it-performance.md stay (famous places with a story, everyday things).
- THE CHECK: from the kit folder, `python3 -I tools/check_hook.py <kit>` after writing the scripts, and again after
  the voice job (it then reads the spoken seconds). It must print no FAIL before you animate (the scene's word anchors
  depend on line 1). Two rewrite passes at most; if a FAIL remains, ship and say why in these notes. "aim for" lines
  are advice, not failures.
- THE TEST: the evening run's numbers study compares builds 73 and later with builds 64-72 at the same age (English
  and Arabic Instagram: average time watched / length, and views; TikTok after 3 days) and writes the result into
  claude/build-it-performance.md. Tell the owner the result in the evening message of Nov 28.
- Not changed: the 4-minute show's opening lines (already short), covers, closer, tag joke, line 10.

## Nov 23 2026, ~18:30 PT: Survival Mode 4 finished by the main chat
The show run of Nov 23 stopped at 13:36 PT on Claude's usage limit (ROUTINE_RUN_FAILURE_REASON_USAGE_LIMIT_REACHED), after its spec and voices were pushed. The main chat built the four cuts (EN full 4:40, short 1:23; AR full 4:54, short 1:28; all -14.0 LUFS, peaks -2.0 to -2.3 dBFS; stills sheets looked at), wrote posts/sm04.yml and kit/show/youtube/sm04.yml from sm03, ran handoff.py, uploaded the four videos in Studio for Tue Nov 24 (AR full 09:00, EN full 10:00, AR Short 10:30, EN Short 12:15 PT) and released the TikTok + Instagram posts. Builds 70-72 also uploaded (6 videos). sm03 Arabic TikTok failed at 10:30 PT Nov 23: requeued to 02:00Z Nov 25 (18:00 PT Nov 24). The afternoon round prompt now says to finish a failed show run the same way.

## Nov 23 2026 (evening run, 18:37 PT): 73 the Lighthouse of Alexandria, 74 Maraya, 75 Chand Baori (for Tue Nov 24)
- TODAY Mon Nov 23 PT, TOMORROW Tue Nov 24 PT (`TZ=America/Los_Angeles date` first; every at: turned back into PT
  before the push). PST: Arabic Instagram 09:00 / 12:00 / 15:00 PT = 17:00Z / 20:00Z / 23:00Z Nov 24, Arabic TikTok
  08:30 / 12:30 / 15:00 PT (2 h either side of the show's Arabic TikTok at 10:30 PT); English 13:30 / 16:00 / 18:30 PT =
  21:30Z Nov 24, 00:00Z / 02:30Z Nov 25. YouTube: desk.yml verified: true, so all three hold YouTube with `studio: 1`.
- Status 02:45Z (Nov 23 PT, builds 64-69): six builds out. English Instagram + TikTok all twelve, Arabic Instagram all
  six, Arabic TikTok only 64 and 65 (66-69 "potential spam"; 50's requeue refused again at 01:30Z Nov 24). YouTube: all
  six in Studio (ledger), sm03 too. yt_desk check: nothing overdue. Arabic TikTok in error: 48, 50, 56, 62, 66, 67, 68,
  69; the queue is 10 of 10 (37, 42, 54, 55, 60, 70-72, sm03, sm04), so nothing was requeued.
- Metrics 02:49Z: 215,479 views (+16,646). Pisa's Arabic TikTok 1,247 (the best Arabic TikTok since Nov 16); English
  TikTok near zero for a third day (58-64: 1-12 views); Arabic Instagram 58-63 median 1,505. Entry in
  claude/build-it-performance.md.
- First builds written to the hook rules (check_hook.py: all pass). English hooks 15-16 words, spoken 4.5-4.8 s, first
  problem by 8.5-9.2 s; Arabic hooks 12 words, 4.1-4.6 s, problem by 7.8-9.5 s. Lesson: check_hook's reading grade
  counts long names, so "the Lighthouse of Alexandria" left room for only one plain picture ("If you top a giant tower
  with fire"; "a fire on top of a skyscraper" failed at grade 7.8).
- Voices: ElevenLabs Pro 23,928 of 613,234 used before (4%), 30,241 after (other projects ran at the same time; ours
  about 2,500 characters: 810 + 821 + 822 + one remade closer line). Easton pharos 61.9 s (215 words), maraya 61.3 s
  (216), stepwell 61.0 s (213): short of 62 s but the videos are 64-65 s, inside the gate. Mansour 66.0 s each (tempo
  1.00-1.12). Whisper small on the English voices: "thirty-floor" -> "34" (now "a building with thirty floors"), "It
  guided ships" lost "It" (now "This tower guided ships"), "in mirrors" -> "and mirrors" (now "with mirrors"); English
  remade free. SAY now respells maraya -> "mah-rah-yah" (Whisper writes "Mariah" / "Mara Ya"), chand -> "chahnd", baori ->
  "bow-ree" (Whisper writes "Chanbo-ri"); the captions carry the names. check_ar_voice: only the digit lines over 10%
  except stepwell's closer, where the bare name "تشاند باوري" was heard "جنبا ور" (15%): the closer became "بير تشاند
  باوري" (one line remade, 11%), which also puts "بير" on the Arabic cover.
- Research (WebSearch titles only, no agents): Lighthouse of Alexandria (Wikipedia, World History, AramcoWorld on Ibn
  al-Shaykh, Archaeology magazine July 2025 "Submerged blocks lifted from seafloor": 22 blocks, Qaitbay citadel on its
  site); Maraya (Guinness 2020 "largest mirrored building", 9,740 m2, Giò Forma, Guardian Glass); Chand Baori
  (Wikipedia, Incredible India, India Water Portal: 3,500 steps, 13 levels, about 30 m, 5-6 °C cooler at the bottom,
  8th-9th century). Maraya's panel gaps and coating are said as general façade practice, not as Maraya specifics.
- Scenes (all v2 look 2):
  - pharos.py (harbor, far, ramp, street): tower() in elevation (1 m = 6 units, sea level 0): square tier, octagon tier
    with angled faces, cylinder, lantern with a bronze dish beside the flames (rays flame -> dish -> sea), a statue;
    `built` reveals it bottom-up, `dark` makes it a black shape, `fall` drops the tiers into the sea; galley() (an old
    ship with a striped square sail, tilt/sink/lamp), rocks_under() (x-ray reefs), water() with the beam's sparkles,
    seabed() with 22 blocks and one lifted on a crane cable; the ramp set is the tower cut open with a zigzag ramp and
    donkey_side() walking it (PathMeasure); tag: a delivery scooter circling identical houses while you wave a phone
    torch from a balcony. Light stone on a pale sky bloomed: day scenes use a deep blue DAYP.
  - maraya.py (valley, panel, home): landscape() = rounded sandstone outcrops (cliff_shape with quad bulges) on both
    sides of the hall, a far mesa, acacias; hall() is a box whose mirror shows the landscape flipped (saveLayer + clip,
    sky drawn in screen space), panel seams that fade as it "vanishes", a sheen; panel set: 2 x 3 panels that grow and
    shrink day/night and crack, then gaps, a sandstorm that dulls them and a coating that sends the sand back. Lesson:
    cliffs placed beyond the camera's width left a flat orange frame: put their inner edges just behind the hall.
  - stepwell.py (well, lobby): well() in section: back wall of zigzag double flights per floor (zig_stairs), side walls
    that go from straight (lean 0) to 13 stepped floors (lean 1), a green pool with a level, rain, caving chunks, one
    narrow stair for break4; `dug` 0 fills the frame with earth (otherwise the sky showed under the ground).
- Pages: media/ was 817 MB with no build fully sent. Retired ep48, ep50 and ep56 (their only unsent posts are Arabic
  TikToks in error that keep failing): 817 -> 699 MB before the six new videos (about 800 MB after). If a later run
  wants to requeue one of those three, restore its media from git history first (Buffer may fetch it again).
- Lineup: 83 a Thermos flask, 84 the Hoover Dam, 85 the Dubai Frame appended (checked by title: usbr.gov "one solid pour
  would take 125 years", Gulf News Dubai Frame sky walk at 150 m, Royal Institution / Britannica on Dewar's flask).
- Produce reports: pharos EN 65.0 s / AR 69.1 s, maraya EN 64.4 / AR 69.1, stepwell EN 64.1 / AR 69.1 (all -14 LUFS,
  covers true). Whisper small on the three English mixes: only numbers as digits and the names Maraya / Chand Baori
  (CI's smaller model wrote "with 34s" for pharos line 3; small hears "with 30 floors", so it was left).
- Posts: 73 + 74 pushed 04:13Z (after the Pages deploy of f783904 succeeded), 75 at 04:27Z (after 33b3a3c's deploy;
  Pages runs were cancelled by other projects' pushes for 15 minutes in between). State 04:16Z: 73 and 74 English
  Instagram + TikTok and Arabic Instagram scheduled at their Tue Nov 24 PT times; state 04:30Z: 75's the same, and
  73's Arabic TikTok got in at 16:30Z (42 had gone out at 04:30Z). The Arabic TikToks of 74 (20:30Z) and 75 (23:00Z)
  wait for queue room (10 of 10): check-in of this session at 11:20Z Nov 24 (send_later trig_01EoaDvsSa6p8qmJqLjJAEsA)
  dispatches post.yml once 70 (08:00Z) and 71 (11:00Z) have gone out. Errors 48, 50, 56, 62, 66-69 were not requeued
  (no room; free 2-hour gaps start 01:30Z / 04:30Z Nov 27). Watch: 54's requeue (01:30Z Nov 25) and sm03's (02:00Z
  Nov 25) are only 30 minutes apart, so one may be refused as spam; left alone (sm03 is the show's).
- Check-in 11:20Z Nov 24: nothing to dispatch. Other pushes' post.yml runs had already added the waiting Arabic
  TikToks (74 at 08:40Z, 75 at 11:08Z), so 73-75 are all scheduled: 08:30 / 12:30 / 15:00 PT Tue Nov 24 (queue 10 of 10).


## Nov 23 20:45 PT: NEW STYLE for every build: Seedance (owner approved)
- Owner after the Taipei 101 sample (Seedance footage only, cinema captions): "We can start making all our next
  videos like that? Change the plans to the new one." Recipe: series/SEEDANCE_STYLE.md (two 6-shot Seedance jobs per
  build, tools/seedance_cut.py, tools/seedance_publish.py writes media/ + review/ like produce.yml). This is the look
  the STYLE paragraph of the production prompts waits for: follow it from the Nov 24 runs on.
- Footage queue: higgsfield/queue.yml (76 cooker, 77 Golden Gate, 78 air fryer, 79 Kuwait Towers, 80 Jeddah
  fountain, 81 zipper queued). The hourly task "Higgsfield runner" makes them on the owner's Chrome.
- Free Seedance video ends Nov 28: bank footage until then. After that the same on-screen style runs on free
  unlimited pictures (GPT Image 2.6 / Nano Banana Pro / Seedream) with slow zoom; the cutter takes .png shots.
- Owner: the Easton voice is "annoying". Four ElevenLabs samples sent (Dan XA3P1cj7XJexe6Zq0ATX, Larry
  fIGaHjfrR8KmMy0vGEVJ, Liam VCgLBmBjldJmfphyB8sZ, Brian nPczCjzI2devNBz1zQrb); voices.yml en changes when he picks.
- Nov 23 21:59 PT: English voice is now J. Ballen (ElevenLabs 2LxhCRvenFtT95JOekmF, Southern storyteller with comic
  timing), owner's pick. voices.yml en switched. English costs about 1,000 ElevenLabs characters a build now, so the
  Build-It daily cap goes from 8,000 to 12,000 (6 builds x EN+AR ~ 11,400; the month still fits the 613k plan).
  Write the jokes for his timing.
- Nov 23 22:04 PT, owner on the English voice: "make his role kinda funny, like he is almost gonna laugh while
  talking, and add some humor words like he is talking to the viewers". English is J. Ballen on eleven_v4 with
  audio tags (voices.yml). HOW TO WRITE EVERY ENGLISH SCRIPT NOW (sample: series/sample_tpf_lines.txt, video
  sent 22:15 PT): start most lines with a tag ([amused], [playful], [chuckles], [laughs softly], [warmly], [proudly];
  [laughs] / [laughs harder] on the tag joke), talk to the viewer ("Y'all", "Now listen", "I'm serious", "oh boy",
  "Yes... a dishwasher"), keep the facts. Tags never reach the captions (make_vo_eleven strips them).
  LENGTH: he is slow and the laughs take time: 217 words = 93 s. Write about 160-170 words (14 lines) to land near
  70 s, and keep the hook line under 15 words. v4 has no speed setting; do not speed him up more than 1.1x.
- OVERRIDES for the two production prompts (midday 11:23 and evening 18:37), from Nov 24 on. Where a prompt says
  otherwise, these win:
  1. Look: Seedance builds (series/SEEDANCE_STYLE.md). Skip step 5 (v2 scene) and produce.yml; make the build with
     tools/seedance_publish.py, episodes.yml line `look: sd`. Take the LINEUP builds in order, but only ones whose
     two clips are `status: done` in higgsfield/queue.yml (ai_media.py get them); a slot with no ready footage gets
     the next ready build, and v2 only if none is ready. Never generate on Higgsfield in a scheduled run.
  2. English script: about 160-170 words (not 210-230), Ballen's funny delivery with [audio tags]; English voice up
     to about 74 s is fine (not 67); gates are seedance_publish's (EN 55-75 s, AR 55-85 s, -15..-13 LUFS).
  3. Each line must fit its shot: watch the clips (one frame per shot) before writing, and match line N to shot N
     (shot plan table in SEEDANCE_STYLE.md). Lines 12-13 use the still or the best A shot.
  4. ElevenLabs: Pro plan since Nov 22 (613,234 characters a month, resets Dec 22); the Build-It share is about
     12,000 characters a day. The "Creator, 23,000 left" line in the prompts is out of date.
- Nov 23 22:36 PT, owner: "I approve the new English voice with the sense of humor." Ballen + v4 tags is FINAL for
  English. He asked to try the same in Arabic: sample sent 22:55 PT (Mansour on eleven_v4 with the same tags, Saudi
  lines that talk to the viewer: series/sample_tpf_lines_ar_sa.txt; 156 words = 87 s, so Arabic needs ~125-135 words).
  Until he answers, Arabic builds stay on eleven_multilingual_v2 (voices.yml ar unchanged).
- Nov 23 23:01 PT, owner: "Love it we gonna use those voices and style for our next future videos." Arabic Mansour on
  eleven_v4 with funny tags is FINAL (voices.yml ar switched). Arabic scripts: talk to the viewer in Saudi, ~125-135
  words, voice <= ~80 s (gate 55-85 s); speed no more than 1.1x.
- Same message: owner asked about 16:9. Answer: Shorts/Reels/TikTok need 9:16, so SHORTS STAY 9:16 (Higgsfield stays
  9:16). 16:9 only for long YouTube videos (the 4-minute show). Never leave Higgsfield on 16:9 for a short build.
- Nov 23 23:53 PT, owner, STANDING TARGET: every day 6 shorts + 2 long videos, each in Arabic AND English, posted on all
  social media (shorts: YouTube Shorts, TikTok, Instagram; long videos: YouTube, 16:9 allowed for long). If Higgsfield
  refuses (busy slot: another chat runs scheduled jobs on the same account), schedule a retry (send_later 12 min) and keep
  retrying until the target is reached. A Cloudflare "Verify you are human" box is NOT a refusal to retry past: never click it,
  tell the owner. Higgsfield shorts stay 9:16.
- Nov 24 01:00 PT: build 78 (air fryer) is ALREADY MADE and checked, EN + AR: media/airfryer-b78-en.mp4 (73 s) and
  media/airfryer-b78-ar.mp4 (77 s), covers in review/airfryer-b78/cover_{en,ar}.jpg, spec kit/episodes/airfryer_sd.json.
  Owner saw both and said "everything looks great". Do NOT remake it: post it in the next free slots (standing approval:
  check, post, he removes what he dislikes). Builds 76 (cooker) and 77 (Golden Gate) are also ready as footage.
  Build 79 (Kuwait Towers): clip A fetched, B generating (kuwait-A/B in higgsfield/queue.yml).
- Build 79 Kuwait Towers made (VOICE_SPEED=1.08 on seedance_publish): media/kuwaittowers-b79-en.mp4 74 s, -ar.mp4 76 s, covers in review/kuwaittowers-b79/. Must be posted.
- Build 80 King Fahd's Fountain made (VOICE_SPEED=1.04): media/fountain-b80-en.mp4 72 s, -ar.mp4 69 s, covers review/fountain-b80/. Must be posted. Build 81 zipper: zipper-A fetched, zipper-B generating (02:18 PT).
- Build 81 zipper made (VOICE_SPEED=1.08): media/zipper-b81-en.mp4 73 s, -ar.mp4 70 s (AR audio re-normalised with ffmpeg loudnorm two-pass to -14.3 LUFS / -1.0 dBFS after the first cut measured -15.2). Must be posted. Tease shot in B4 looks like Golden Gate, not HZMB. hzmb-A generating since 02:31 PT.
- Build 82 HZM Bridge made (no speed-up needed): media/hzmb-b82-en.mp4 71 s (audio re-normalised, loudnorm two-pass), -ar.mp4 67 s. Must be posted. Tease = Thermos (build 83). thermos-A generating. Queue label "taipei = build 83" is wrong (taipei is LINEUP 68).
- Build 83 Thermos flask made (VOICE_SPEED=1.07, both passed gates): media/thermos-b83-en.mp4 71 s, -ar.mp4 67 s. Must be posted. Tease = Hoover Dam (build 84): hoover-A generating since ~03:38 PT, hoover-B todo. Minor: line 8 picture shows a steel flask falling (glass shot is B2 in the clip).
- Build 84 Hoover Dam: both clips fetched (hoover-A hf_113552, hoover-B hf_115235); episode next. Build 85 Dubai Frame: dubaiframe-A generating, B todo.
- Build 84 Hoover Dam made (VOICE_SPEED=1.06, both passed): media/hooverdam-b84-en.mp4 73 s, -ar.mp4 71 s. Must be posted. Tease = Dubai Frame (build 85): dubaiframe-A done, B generating. Note: hoover-B had no style line; look is fine.
- Build 85 Dubai Frame made (VOICE_SPEED=1.10, both passed): media/dubaiframe-b85-en.mp4 74 s, -ar.mp4 72 s. Must be posted. Tease = kettle (build 86): kettle-A done, kettle-B generating.
- Build 86 Electric kettle made (VOICE_SPEED=1.06, both passed): media/kettle-b86-en.mp4 73 s, -ar.mp4 71 s. Must be posted. Tease = hot air balloon (build 87): balloon-A generating since 05:50 PT, balloon-B todo.
- Build 87 Hot air balloon made (VOICE_SPEED=1.05, both passed): media/balloon-b87-en.mp4 72 s, -ar.mp4 69 s. Must be posted. Tease = Pont du Gard (build 88): pontdugard-A generating since 06:37 PT, B todo; noor-A/B (build 89) todo.
- Build 88 Pont du Gard made (VOICE_SPEED=1.11, both passed): media/pontdugard-b88-en.mp4 74 s, -ar.mp4 70 s. Must be posted. Tease = Noor Ouarzazate (build 89): noor-A generating since 07:13 PT, noor-B todo.
- Build 89 Noor Ouarzazate made (VOICE_SPEED=1.09, both passed): media/noor-b89-en.mp4 74 s, -ar.mp4 73 s. Must be posted. Tease = ballpoint pen (build 90): pen-A generating since 07:52 PT, pen-B todo; arch-A/B (build 91) todo.
- Build 90 ballpoint pen made (VOICE_SPEED=1.10 after 1.07 gave EN 76 s): media/pen-b90-en.mp4 74 s, -ar.mp4 73 s, post file posts/ep90-pen.yml. Tease = Gateway Arch (build 91): arch-A generating since 12:05 PT, arch-B todo. Builds 78-89 post files were missing; created Nov 24, queued on Buffer.

## Nov 24 2026 (midday run, 11:23 PT): 76 a pressure cooker, 77 the Golden Gate Bridge (Seedance; post Thu Nov 26)
- TODAY Tue Nov 24 PT, TOMORROW Wed Nov 25 PT, but TOMORROW was already full: the main chat posted builds 78-90 every
  2.5 h (EN 21:00 PT Nov 24 -> 03:00 PT Nov 26, AR 00:00 PT Nov 25 -> 06:00 PT Nov 26), about 9-10 builds per language
  on Nov 25 PT, and all four Buffer queues were 10 of 10 (25 targets waiting). So this run's builds take the next two
  slots of that 2.5 h grid after 90, on Thu Nov 26 PT: 76 EN 05:30 PT (13:30Z), AR Instagram 08:30 PT (16:30Z), AR
  TikTok 12:30 PT (20:30Z); 77 EN 08:00 PT (16:00Z), AR Instagram 12:00 PT (20:00Z), AR TikTok 15:30 PT (23:30Z) (Arabic
  TikToks 3 h apart and 2 h from the show's 10:30 PT; Arabic Instagram clear of the show's 10:30). FOR THE MAIN CHAT AND
  THE EVENING RUN: schedule 91 after 77 (EN from 18:30Z, AR from 21:30Z Nov 26), because 77's line 10 promises the
  Gateway Arch. Posting order 89 -> 90 -> 76 -> 77 -> 91: 90's own promise of the arch arrives two posts late.
- Only two builds: 90 (pen) was being made by the main chat (scripts 11:39 PT, posted 12:02 PT) and no other footage was
  done (arch-A/B, seatbelt-A/B todo at 11:45 PT). No v2 build: the v2 fallback is for days with empty slots, and the
  queues were overfull. 76-77 were the footage-ready LINEUP entries nobody had made.
- 78-90 were not in episodes.yml, so the LINEUP rule would have let a run pick them again: episodes.yml now lists them
  (look: sd, media slugs <kit>-bNN) and LINEUP 78-90 say "made by the main chat".
- FIXED, seedance_cut.py Arabic captions: two white words side by side merged into one libass run, and libass reversed
  them inside it, so in every 3-word chunk the words swapped places whenever the first or the last word was gold (the
  word order jumped as the highlight moved: "الألواح العادية الشمسية" in noor-b89-ar at 7.9 s). Now each word alternates
  two whites (&H00FFFFFF / &H00FEFEFE). EVERY Seedance Arabic video made before 12:30 PT Nov 24 (78-90) has the bug;
  they are already queued in Buffer, so a re-cut needs a new file name and an edit of the Buffer post (the main
  chat's call; the owner was told).
- New: a shot may carry "len" (seconds of footage to use); the cutter slows that shot to fill its line, so a long line
  no longer runs into the next Seedance shot. 76-77 use one detected shot per line (ffmpeg scdet threshold 4; cuts
  near 5/10/15/20/25 s, some shots have a second cut inside). 77's line 10 uses pen-B4 (the Gateway Arch at sunset):
  goldengate-B4 is an air fryer (78), already posted.
- post.py now fills free Buffer queue places in posting order (earliest fixed time first), not in file-name order:
  ep76/ep77 sorted before ep78-89 and would have jumped the queue ahead of posts due a day earlier.
- seedance_publish.py keeps the other language in report.json when one language is made again.
- Scripts (Ballen / Mansour v4 tags, 178-181 EN words, 133-138 AR words): cooker hook "this pot gets water hotter
  than boiling", the Andes kitchen, lid + rubber seal, rattling pot, weight that whistles, a bean skin plugs it, the
  melting backup plug, the lid lock pin, India counts whistles; Golden Gate hook "its famous orange started out as the
  undercoat", tides/waves/fog, the concrete tub pumped dry, a gray tower lost in fog, Morrow kept the orange (the Navy
  wanted bumblebee stripes), 27,572 wires a cable, the net and the Halfway to Hell Club (19 men), 200,000 walkers on
  opening day. Arabic tags: "وبتلبس المرقة", "امش عليه بشماغك الجديد... والهوا ياخذه ذكرى". Research: WebSearch titles
  only (Wikipedia pressure cooking / steam digester / high-altitude cooking, TTK Prestige and Wonderchef whistle guides,
  Presto manuals; NPR "accidental color", goldengate.org "a bathtub for the south tower", "cross section of a main
  cable", Wikipedia Half Way to Hell Club, History.com "6 things", May 27 1937 opening).
- check_hook.py: "Y'all," / "يا جماعة،" reads as a second picture (the old frame's comma test) in the Seedance style;
  timings after one rewrite pass: cooker EN hook 5.0 s, problem by 10.4 s; AR 4.7 / 10.2 s; Golden Gate EN 5.3 / 9.7 s,
  AR 5.4 / 10.1 s (better than 78-90, which tell the problem at about 12.7 s). Shipped.
- Whisper small on Ballen: "rubber ring" -> "rain" (now "rubber seal"), "Golden Gate" -> "Golden Day" (now "San
  Francisco's Golden Gate Bridge"), "in fog" -> "and fog" (reworded twice), "Hell Club" -> "Hill Club" (caption carries
  it). Mansour: "تسعطعش" heard "ساطع" (now "تسعة عشر"); "قدر الضغط" is heard "قدرة وغضب" but "اضغط" is heard right (left).
- Voices (tempo 1.12 both, no VOICE_SPEED): cooker EN 68.5 s / AR 67.7 s; Golden Gate EN 72.8 s / AR 71.2 s.
  ElevenLabs: about 5,100 characters with the remakes (EN 1,130 + 1,170, AR 920 + 974, remakes 335 + 243 + 239 + 119).
- Videos (seedance_publish, gates ok): ep76-cooker EN 69.9 s -14.7 LUFS / AR 69.1 s -14.9; ep77-goldengate EN 74.2 s
  -14.9 / AR 72.6 s -15.0 (EN close to the 75 s gate). Whisper small on both English mixes: number formats only.
- Pages: retired ep42, ep62, ep66-ep72 (sent, or only refused Arabic TikToks left; 66-72 in the Studio ledger):
  media/ 1.4 GB -> 1.06 GB, about 1.15 GB with 76-77. 78-90 alone are about 640 MB: retire them as their posts go out.
- Status 19:37Z: Nov 24 PT 70, 71 all out; 72 all but its Arabic TikTok (spam, 14:00Z); 73 Arabic Instagram out, its
  Arabic TikTok refused (16:30Z); sm04's Arabic TikTok refused (18:30Z). Arabic TikTok in error: 48, 50, 56, 62, 66-69,
  72, 73 (+ sm04). Not requeued: every queue is 10 of 10 with 25 new targets waiting, and a requeue takes a place
  from them. yt_desk check: nothing overdue.
- LINEUP: 96 a hand warmer, 97 the Museum of the Future, 98 Jewel Changi's Rain Vortex, 99 instant noodles appended.
- State (posting run 20:56Z, the first with the due-time order): the 8 Instagram + TikTok targets of 76-77 wait for
  queue room (every channel 10 of 10; 82-90 go first); the 4 YouTube targets hold for Studio. Post files pushed 20:53Z
  after the Pages deploy of 5165d15 succeeded. Check-in of this session at 12:50Z Nov 26 (trig_01GDbqqo7WNFquMfMEy6P1V4)
  dispatches post.yml if any still waits. The main chat was making 91 (arch, line 10 -> seatbelt) at 12:45 PT.
- Build 91 Gateway Arch made (VOICE_SPEED=1.13): media/arch-b91-en.mp4 74 s, -ar.mp4 72 s, post file posts/ep91-arch.yml. Tease = car seatbelt (build 92): seatbelt-A generating since ~12:45 PT, seatbelt-B todo; Huajiang (93) is teased by seatbelt-B.
- Build 92 seatbelt made (VOICE_SPEED=1.13): media/seatbelt-b92-en.mp4 72 s, -ar.mp4 72 s, post file posts/ep92-seatbelt.yml. Tease = Huajiang Grand Canyon Bridge (93): huajiang-A done, huajiang-B generating since 13:45 PT; then smoke alarm (94).

## Nov 24 2026 (evening run, 18:37 PT): 94 a smoke alarm, 95 the Falkirk Wheel (Seedance; post Fri Nov 27)
- TODAY Tue Nov 24 PT, TOMORROW Wed Nov 25 PT, but Wednesday was already full (the main chat's 78-87 English and
  78-87 Arabic, every 2.5 h) and Thursday held 88-90, 76, 77, 91, 92. So 94 and 95 post on Fri Nov 27 PT, right after
  the slot kept free for 93 (93's line 10 promises 94): 94 EN 06:00 PT (14:00Z), AR Instagram 00:00 PT (08:00Z), AR
  TikTok 03:30 PT (11:30Z); 95 EN 08:30 PT (16:30Z), AR Instagram 03:00 PT (11:00Z), AR TikTok 06:30 PT (14:30Z).
  Every at: turned back into PT before the push. YouTube: verified, so both hold it with `studio: 1`.
  NEXT FREE SLOTS AFTER 95 (for the runs of Nov 25; 96 goes first, 95's line 10 promises it): Fri Nov 27 English from
  11:00 PT, Arabic Instagram from 06:00 PT, Arabic TikTok from 12:30 PT (3 h after 95's 06:30 PT would be 09:30 PT, but
  that is within 2 h of the show's Arabic TikTok at 10:30 PT).
- 91 and 92 (main chat) were written at the same times as 76 and 77 (EN 13:30Z / 16:00Z Thu): moved after 77, as the
  midday run asked: 91 EN 10:30 PT, AR Instagram 14:30 PT, AR TikTok 18:30 PT; 92 EN 13:00 PT, AR Instagram 17:00 PT,
  AR TikTok 21:30 PT (Thu Nov 26). Nothing of them was on Buffer yet. 93's slot (kept free, LINEUP 93): EN 15:30 PT
  Thu, AR Instagram 19:30 PT Thu, AR TikTok 00:30 PT Fri.
- Builds picked: 93 (Huajiang) has scripts, voices and a spec from the main chat (14:04 PT) but no video: left to it.
  94 and 95 were the footage-ready LINEUP entries nobody had made (falkirk-B was fetched at 18:52 PT); 96 (hand warmer)
  had no footage (handwarmer-A not started at 19:26 PT), so two builds, no v2 (queues overfull, slots full for days).
  episodes.yml now lists the main chat's 91-92; LINEUP 91-92 say "made by the main chat".
- Status 02:48Z: Nov 24 PT six builds out (70-75): EN Instagram + TikTok all twelve, AR Instagram all six, AR TikTok
  70, 71, 75 (72-74 and sm04 refused). Arabic TikTok in error: 48, 50, 54, 56, 62, 66-69, 72-74, sm03, sm04; not
  requeued (every queue 10 of 10 with 25 new targets waiting). yt_desk check: nothing overdue.
- Metrics 02:56Z: 220,177 views (+4,698; Arabic Instagram +1,034 against +5,805 the day before). Arabic Instagram now
  stalls every other reel like English (64-69 median 175 views against 1,507 for 58-63). Entry in
  claude/build-it-performance.md; the owner is told ~6 a day per language looks like what the numbers support.
- Pages: retired ep54 (only a refused AR TikTok left) and ep73-75 (sent; Studio done): media/ 1.3 -> 1.15 GB before
  94-95 (+92 MB). 78-92 are about 750 MB: retire them as their posts go out (each keeps its media until its Studio slot).
- Research (WebSearch titles only, no agents): smoke alarm (NRC and EPA on americium ionization detectors; Kidde and
  First Alert "why smoke alarms chirp in the middle of the night"; Brown University 2004 / ScienceDaily "smell is not
  a wake-up call"; UL / NIST modern vs legacy furnishings: flashover in about 3:40 against about 29:30; First Alert and
  Illinois' 10-year sealed battery law; UW 2008 / CPSC on photoelectric alarms and cooking); Falkirk Wheel (ICE, ASME,
  Hackaday Feb 2026, Guinness "largest rotating boatlift", Wikipedia: 24 m, 1.5 kWh per half turn = about eight kettles,
  about 15,000 hand-tightened bolts, three 8 m gears, the 11 locks dismantled in 1933, the tunnel under the Antonine Wall
  and two locks up 11 m to the Union Canal, opened 2002). Higgsfield runner's facts in higgsfield/ideas.md were checked
  against these titles.
- Scripts: Ballen v4 tags, 189 and 186 English words; Mansour v4, 146 and 147 Arabic words. Hook pass twice (check_hook):
  94 EN hook 4.5 s, problem by 9.0 s; AR 5.2 / 9.9 s; 95 EN 4.1 / 8.8 s; AR 5.4 / 10.1 s (0.1 s over, shipped). The
  remaining "one picture" FAILs are the known "Y'all," / "يا جماعة،" comma false positive of the Seedance style.
- Whisper small on Ballen: "hide a speck" -> "high the speck" (now "have a speck ... inside"), "the house is coldest
  then" -> "cold as then" (now "cools down at night"), "seesaw" -> "sea salt" (now "like kids on a seesaw"), "Scotland
  built" -> "got" (left; the caption carries it). "Y'all" -> "Yo" and "So" -> "No/When" stay (whole series).
  check_ar_voice: no weak lines (max 20%, the digit lines and "اسكتلندا").
- Voices (tempo 1.12, no VOICE_SPEED): 94 EN 71.4 s / AR 75.3 s; 95 EN 69.4 s / AR 73.8 s. ElevenLabs about 5,000
  characters with the remakes (four EN passes on short lines).
- NEW in tools/seedance_cut.py (both for every later build):
  1. Loudness: the mix is raised to -14 LUFS by gain + limiter (alimiter 0.79), measured again until within 0.3 LU.
     Mansour's v4 takes peak about 20 dB over their loudness, so the old single loudnorm pass (and a two-pass loudnorm,
     tried) left 94-ar at -15.2 / -15.1 LUFS, under the gate (the main chat had the same on 82-ar). Now -14.1 to -14.2.
  2. A shot may carry a per-language override: {"line": 4, "src": A, "at": 15.5, "len": 4.9, "ar": {"src": ..., "at":
     0, "len": 4.95}}. 94's line 4 shows bacon frying in English; the Arabic cut uses a crop of the same shot without
     the pan (alarm, smoke, battery dropping out): out/aishots/buildit-smokealarm-sdA-kitchentop.mp4, made with
     `ffmpeg -ss 15.46 -t 4.96 -i buildit-smokealarm-sdA.mp4 -vf "crop=428:760:146:0,scale=720:1280:flags=lanczos,setsar=1"
     -c:v libx264 -crf 14 -an` (not in ai-media; remake it the same way). Watch the footage for pork, alcohol and
     similar before an Arabic cut.
  3. 94's line 10 uses falkirk-A shot 1 (smokealarm-B4 came out as canal locks, not the wheel); 95's reveal uses
     falkirk-A shot 1 again (falkirk-B5 came out as a round pool of boats, not the wheel).
- Videos (seedance_publish, gates ok, covers true): ep94-smokealarm EN 72.8 s -14.2 LUFS / AR 76.7 s -14.1; ep95-falkirk
  EN 70.8 s -14.2 / AR 75.2 s -14.2. QA sheets looked at (right shot under every line, Arabic words in reading order);
  Whisper small on both English mixes: number formats and the words above.
- LINEUP: 100 the Jeddah Tower (Build #100), 101 a fire sprinkler, 102 Abu Dhabi's Al Bahar Towers, 103 bubble wrap,
  104 Tokyo's G-Cans flood tunnel, 105 the Brooklyn Bridge appended (checked by search titles).
- Posts pushed 03:45Z after the Pages deploy of 606b4aa (after the videos' d6e1aa4) succeeded. All 8 Instagram +
  TikTok targets of 94-95 wait for queue places (every channel 10 of 10; 88-92, 76-77 and 93 come first in due-time
  order); later post.yml runs add them. Check-ins of this session: 15:10Z Nov 25 (trig_01Qc6n2WEvBG6xJgWjKDL78E,
  dispatches post.yml once if targets wait and places have freed) and 05:00Z Nov 27 (trig_0181nf4XBeMQf4pkL6iqGME5,
  makes sure 94-95 are on Buffer before their slots).
- Watch (not changed): Arabic TikTok on Wed evening PT is crowded: 60 (requeue) and 85 both at 01:30Z Nov 26, then 86
  04:00Z, 37 (requeue) 04:30Z, 87 06:30Z. 85-87 are not on Buffer yet, so a run may give 85 its own tiktok: time.
- The 4-minute show: its run of Nov 24 (13:17 PT) stopped on Claude's usage limit and no fallback made sm05, so Wed
  Nov 25 has no show episode (no long videos, no show short). The owner was told.

## Nov 25 2026 (midday run, 11:23 PT): 93 the Huajiang bridge (Seedance), 96 a hand warmer (v2) (post Thu Nov 26 / Fri Nov 27)
- TODAY Wed Nov 25 PT, TOMORROW Thu Nov 26 PT. Thursday was full (88-90, 76, 77, 91, 92) except the slot kept for 93,
  so 93 takes it (EN 15:30 PT Thu = 23:30Z, AR Instagram 19:30 PT Thu = 03:30Z Nov 27, AR TikTok 00:30 PT Fri = 08:30Z:
  3 h from 92 and from 94), and 96 takes Friday's third morning slot after 94-95 (EN 11:00 PT = 19:00Z, AR Instagram
  06:00 PT = 14:00Z, AR TikTok 12:30 PT = 20:30Z Nov 27). Every at: turned back into PT before the push. YouTube held,
  `studio: 1`. Only two builds: 97 (museum) is the next Seedance build and its footage was todo (see the picks below).
- Status 19:30Z: the main chat's 78-82 all out except the Arabic TikToks of 80 (13:00Z) and 82 (18:00Z), "potential
  spam"; 83 English out; 84-87 scheduled. 88-92, 76-77, 94-95 were waiting for Buffer places and post.yml had not run
  since 03:45Z (the 15:10Z check-in did not dispatch it): this run's pushes let it add them; every channel is 10 of 10
  again (20:26Z). yt_desk check: nothing overdue (its plan lists 78 and 79 English as already due, not uploaded).
- Requeues. The Arabic TikTok grid runs every 2.5-3 h through Friday; the only 2-hour gaps left were 16:00Z Nov 26 and
  16:30Z Nov 27 (both 2 h clear of the show's 18:30Z). 85's Arabic TikTok (not on Buffer yet, same minute as 60's
  requeue at 01:30Z) got its own `tiktok:` time, 16:00Z Nov 26 (08:00 PT Thu, 19:00 Riyadh); 80's (Jeddah's fountain)
  was requeued to 16:30Z Nov 27 (08:30 PT Fri, 19:30 Riyadh). Still in error, no gap and no queue place before Saturday:
  48, 50, 54, 56, 62, 66-69, 72-74, 82 (+ sm03, sm04). 37 (04:30Z Nov 26) sits 30 minutes after 86 (04:00Z): left, it
  was scheduled ahead.
- Picks. 93 had the main chat's footage, scripts, voices and spec since Nov 24 14:04 PT but no video: its English voice
  was 79.8 s (over the 75 s Seedance gate) and the hooks failed the rules (problem told at 13.9 s EN / 12.9 s AR). 96 had
  no footage at 11:40 PT, so it was made in the v2 look (SEEDANCE_STYLE.md fallback) and handwarmer-A/B were marked
  skipped; in fact the runner on the owner's computer had made handwarmer-A at 11:12 PT (its note came at 12:00 PT): it
  stays a spare in ai-media. 97 stays for Seedance: museum-A/B are next in the queue, then rainvortex-A/B (98).
- 93 fixes (one Seedance shot per line, with `len`; both fire lines on the burning-cable shot B1; reveal on A1, stat on
  A6): English 225 -> 187 words. Hook "Y'all, China hung a road over a canyon called... the Earth's crack." + line 2
  "Cars used to crawl down and back up: two hours! Now? Guess.", answered by line 11 "About two minutes." Unverified
  figures dropped: 96 trucks / 3,000 t -> "almost a hundred loaded trucks"; "1,100 degrees for a whole hour" -> "made to
  take eleven hundred degrees". Arabic lines 1, 2, 7, 9, 11, 12, 13 remade (closer "جسر هواجيانغ الكانيون الكبير" ->
  "جسر هواجيانغ"). Voices: EN 72.4 s (hook 4.8 s, problem by 9.6 s: 0.1 s over after two passes, shipped), AR 70.8 s
  (4.6 / 9.9 s). Whisper small: "old road" -> "whole road" and "in a gust" -> "Auguste" were reworded; on the mix only
  number formats, "Huajian" and sail/sale. Videos: EN 73.8 s / AR 72.2 s, -14.2 LUFS, peaks -1.6 / -1.7 dBFS.
- 96 (kit/episodes/handwarmer.py, v2): pouch(c, t, fill, cryst, heat, press, flash, melt, cold) = the clear pouch with
  its disc (world 600 x 380, disc at (-100, -50)); the crystal front is a circle from the disc clipped to the pouch,
  `melt` shrinks a rounded core (the boil); mitten() in two passes (behind / front) with `bare` cold hands; fingertip()
  clicks the disc; lens() = molecules wandering or snapping into a hex grid with sparks of heat; dominoes();
  chips_bag(); pocket_fire() (jeans pocket with a campfire, crossed out); packet() = a throwaway warmer whose wrapper
  tears, air streams in and an x-ray window shows iron grains rusting with salt, charcoal and vermiculite;
  pot_scene(), slope_scene() (a light pouch on white snow vanished: it sits in a dark glass card), bench_scene().
- Ballen v4 on a v2 build: v2's gate is 61-70.5 s and the video is the voice + 3.1 s, so keep the English to about 165
  spoken words (171 words = 68.0 s of voice at tempo 1.12 failed; 168 words = 66.5 s -> a 69.6 s video). Mansour v4
  131 words = 68.7 s -> 71.8 s. Videos: EN 69.6 s / AR 71.8 s, -14.0 LUFS, peaks -2.2 / -2.1 dBFS; Whisper small on the
  mix: disc/disk, "kind" -> "con", number formats (CI's base.en heard "heated seats" as "he did seats"; small hears it).
- Research (WebSearch titles only): Huajiang (China Daily "World's tallest bridge gets 1,100 C fireproof armor", People's
  Daily "Nearly 40,000 steel wires", Free Press Journal "around 100 heavy trucks", Tribune / Outlook "2 hours to 2
  minutes", VnExpress "across 'Earth's crack'", inkl "I can touch the clouds"); hand warmer (Frostburg "How do dry
  chemical heatpacks work", SFU heat pack demo, Science Focus, Wikipedia on sodium acetate as the salt and vinegar chip
  seasoning, HowStuffWorks disposable warmers, HotHands "up to 10 hours").
- Credits: ElevenLabs Pro 153,251 of 613,234 used at 19:40Z, 155,162 at 21:00Z (25% on day 3 of the period: the
  other projects use about 40,000 a day).
- Pages: retired ep55 (all sent), zipper-b81 (all sent, both Studio uploads done) and hzmb-b82 (only a refused Arabic
  TikTok left, Studio done): media/ 1.3 -> 1.2 GB with 93 and 96. Next: 83 after its Arabic posts (20:30Z Nov 25); 78
  and 79 once their English Studio uploads are done (still due in the desk plan); 37 and 60 after their requeued
  Arabic TikToks; 80 after Fri 16:30Z; 84-87 as they go out.
- LINEUP: 106 the Riyadh Metro, 107 a detachable chairlift, 108 an ice resurfacer appended (12 entries ahead of 96).

## Nov 25 2026 (show run, 13:17 PT): Survival Mode 5 "You vs the Sun" (sm05) for Thu Nov 26
- TODAY Wed Nov 25 PT, TOMORROW Thu Nov 26 PT. Hand-off done 14:17 PT (the run took an hour; no episode went out today,
  because the Nov 24 run died on the usage limit).
- Step 0: status 21:25Z: sm04's English TikTok + Instagram and Arabic Instagram are sent; its Arabic TikTok was blocked
  by TikTok ("potential spam", 18:30Z Nov 24), and sm03's was blocked again on its requeue (02:00Z Nov 25). sm04 was
  NOT requeued: the Arabic TikTok queue is 10 of 10 with nine targets waiting (76, 77, 91-96, then sm05), the grid has
  no 2-hour gap before Fri 20:30Z, and a requeue made before sm05 is released would take the place sm05's own Arabic
  TikTok needs at the 16:45 PT round (LINEUP: leave room for the show's posts). First free slot: Sat Nov 28 16:30Z
  (19:30 Riyadh, 2 h before the show's 18:30Z). Whoever has a free queue place after sm05 is on Buffer:
  `tools.yml cmd=requeue args="ar tiktok sm04=2026-11-28T16:30:00Z"`. yt_desk check: nothing overdue.
- Pick: colosseum, stepwell, louvre, maraya (all Mansour, all v2). The sun is the enemy in each script: the crowd bakes
  (Colosseum's roof of sails), it hardly rains (Chand Baori's 3,500 steps), a plaza like a frying pan (the Louvre Abu
  Dhabi's dome), a box baked like an oven (Maraya's mirrors). Left out: hagiasophia (show rule) and every build that
  posts tomorrow (88-93, 76, 77; they are Seedance builds anyway, see the last point).
- VOICES CHANGED since sm04. voices.yml `en` is J. Ballen (eleven_v4), and make_voices.py gives a show kit whatever
  voices.yml says, so the show's 8 English lines are Ballen now, one audio tag at the start of each line, at x1.10
  (`show_tempo` applies to English too now that it is an ElevenLabs voice: the mean Arabic tempo of the four builds).
  The four v2 builds inside still play Easton, so the English cut has two voices until the show can use Ballen builds.
  New kit `survivalpromob`: the three English closing lines by Ballen (spec `en: promo: survivalpromob`, x1.12).
  Arabic: voice.yml was dispatched with `model=eleven_multilingual_v2`, so Mansour's 8 lines match the v2 builds and
  `survivalpromosa` (voices.yml `ar` is eleven_v4 now; the input only changes the Arabic). kit/show/README.md says all this.
- Checks with Whisper small (downloaded again from the sherpa-onnx GitHub release, 639 MB in seconds). English take 1
  was heard as "a fine pan" (frying), "the sun makes" (bakes) and "you'd be a Roman summer" (you beat): lines 6-8
  reworded ("one big frying pan", "is baking", "you just beat"). Take 2 was heard as "the salty desert" (Saudi): line 7
  now says "Saudi Arabia" (the level card too). Take 3: only number formats differ. Ballen's closing lines 0 of 25.
  Arabic 0-5% a line, no weak lines. On the four finished files Whisper hears every new line in its place.
- ElevenLabs: about 2,300 characters (English 1,480 with the retakes, closing lines 176, Arabic 634). The account read
  155,162 before and 168,683 after (27% of 613,234; most of that hour's use was other projects).
- New in the layer: icon `umbrella` (layout.ICON, "No shade"). stock.py reads the main chat's slugs (airfryer-b78
  crashed it) and lists v2 builds only. Arabic level card: a boss name that ends in a deep tail (the ي of "شمس أبوظبي")
  runs into a long sub line under it, so keep that sub short ("ساحة على البحر · صارت فرن").
- Shallow clone: `git config remote.origin.promisor true; git config remote.origin.partialclonefilter blob:none;
  git fetch --filter=blob:none --deepen=400 origin main` reached every retired build in under a minute, and `fetch`
  then pulled only the eight videos (colosseum and louvre were retired in 0bc48b0, maraya and stepwell in 8d6fd17).
- Cuts (all -14.0 LUFS): English full 4:45.6 (true peak -2.1 dBFS, 85.7 MB at crf 24, chapters 0:00 0:13 1:18 2:19 3:23
  4:24), short 1:28.1 (-1.9, 39.0 MB); Arabic full 4:55.3 (-2.1, 87.3 MB at crf 24, chapters 0:00 0:13 1:17 2:22 3:30
  4:36), short 1:26.7 (-2.0, 39.0 MB). Stills sheets and 144 frames pulled from the four finished files looked at
  (words, Arabic right to left, the right boss on each level). Render: Arabic chain 13:44-14:02, English 13:55-14:13.
- Hand-off: media/sm05-en.mp4 + media/sm05-ar.mp4 and posts/sm05.yml on main with ALL six targets on hold (the Post
  workflow ran: state/sm05.json has no targets). kit/show/youtube/sm05.yml -> handoff.py pushed the two full cuts, the
  two thumbnails and sheet.json to the `show` branch; every raw link answers 200 and `yt_desk.py plan` lists the four
  videos first on each channel. For Thu Nov 26 PT: Arabic full 09:00, English full 10:00, Arabic Short 10:30, English
  Short 12:15 (YouTube, the main chat's 16:45 PT round); TikTok + Instagram Arabic 10:30 (18:30Z), English 12:15
  (20:15Z) after `yt_desk.py release sm05`.
- THE SHOW RUNS OUT OF BUILDS. build_show.py cuts a build with its scene file kit/episodes/<kit>.py (chapter_cuts:
  tl.pause_start, the reveal and tag chunks, ep.spans; prep: ep.draw_world for the cold-open shots, the card backdrops
  and the thumbnail). Seedance builds (look: sd, all from 76 on except 96) have none. Left in the Mansour group: barrier,
  burjalarab, fridge, suez, washer, taipei, dishwasher, vacuum, petronas, pharos, handwarmer (v4 voices) + hagiasophia
  (excluded) = about three episodes (ideas: the sea = barrier, burjalarab, suez, pharos; the house = fridge, washer,
  dishwasher, vacuum; then taipei, petronas, handwarmer + one). For the adapter: an sd build has the same 14 lines
  (2-9 the four breaks and fixes, 10 follow, 11 reveal, 12 stat, 13 closer, 14 tag), series/voice/<kit>.json gives
  every line's start and end, kit/episodes/<kit>_sd.json gives each line's shot; what is missing is the build's own
  time offset (tools/seedance_cut.py) and clean pictures (frames of the source clips instead of draw_world). The owner
  was told in the run's message.

## Nov 25 2026 (evening run, 18:37 PT): 97 the Museum of the Future, 98 the Rain Vortex, 99 instant noodles (v2; post Fri Nov 27)
- TODAY Wed Nov 25 PT, TOMORROW Thu Nov 26 PT. Thursday already carries 8 builds (88-90, 76, 77, 91-93), so 97-99 take
  Friday's evening slots right after 94-96 (96's line 10 promises 97): 97 EN 13:30 PT (21:30Z), AR Instagram 09:00 PT
  (17:00Z), AR TikTok 15:30 PT (23:30Z); 98 EN 16:00 PT (00:00Z Nov 28), AR Instagram 12:00 PT (20:00Z), AR TikTok 18:30
  PT (02:30Z Nov 28); 99 EN 18:30 PT (02:30Z Nov 28), AR Instagram 15:00 PT (23:00Z), AR TikTok 21:30 PT (05:30Z Nov 28).
  Arabic TikToks 3 h apart, the first 3 h after 96's (12:30 PT) and 5 h after the show's (10:30 PT). Every at: turned
  back into PT before the push. YouTube: verified, so all three hold it with `studio: 1`.
  NEXT FREE SLOTS AFTER 99 (for the runs of Nov 26; 100 goes first, 99's line 10 promises "Build #100, the Jeddah
  Tower"): Sat Nov 28 English from 06:00 PT, Arabic Instagram from 00:00 PT, Arabic TikTok from 00:30 PT (3 h after
  99's 21:30 PT; keep 2 h from the show's 10:30 PT).
- Why v2: museum-A/B and rainvortex-A/B were still todo (no Chrome on the runner since 11:51 PT; its 18:02 PT note:
  nothing generating), so 97-99 were made in the v2 look (SEEDANCE_STYLE.md fallback) and the four jobs are marked
  skipped in higgsfield/queue.yml ("next pair: build 100"). Seedance's free unlimited mode ends Nov 28.
- Status 02:51Z: Nov 25 PT English 80-86 out (87, 88 at 19:30 / 22:00 PT), Arabic Instagram 78-85 (86, 87 tonight),
  Arabic TikTok 78, 79, 81, 84 out; 82 and 83 refused, 60's requeue refused again (01:30Z); 80's requeue waits for Fri.
  Nothing requeued (no 2-hour gap in the Arabic TikTok grid through Friday, and queue places go to new posts first).
  yt_desk check: nothing overdue. Metrics 02:57Z: 227,490 views (+7,313); entry in claude/build-it-performance.md.
- Pages: retired ep60 (only a refused Arabic TikTok left), thermos-b83 (the same) and hooverdam-b84 (all sent); all
  three in the Studio ledger: media/ 1.3 -> 1.1 GB before 97-99. Keep 78 and 79 (their English Studio uploads are
  still listed as due). Next: 85 after its Arabic TikTok (16:00Z Nov 26), 86-88 as they go out, 37 after 04:30Z Nov 26.
- Voices (ElevenLabs Pro 169,520 of 613,234 before, about 6,500 characters with the remakes): Ballen v4 museum 66.28 s
  (first take 67.86 s: a 71 s video, over the v2 gate; hook and line 2 shortened), rainvortex 66.00 s (first 67.56 s;
  hook and line 4 shortened), noodles 66.00 s; Mansour v4 museum 66.88 s, rainvortex 66.09 s, noodles 66.00 s (x1.07).
  Hooks after the remakes: EN 4.4-4.8 s, problem by 7.9-8.8 s; AR 4.4-4.9 s, problem by 8.3-9.3 s (only the known
  "Y'all," / "يا جماعة،" comma FAILs). Whisper small on Ballen: "glass wall" -> "blast wall" (now "a low wall made of
  glass"), "pumps send" -> "pumps in" (now "pumps carry"), "rushes" -> "rashes" (now "soaks right back in").
  check_ar_voice: museum line 11 reads 49-51% because Whisper stops after the "!" of "برّاه هو اللي شايله!"; the
  second half on its own is heard right ("الفين واربعمية عارضة حديد متشابك مثل السلة"; the first take was heard
  "1200" and was rewritten "ألفين وأربع مية"), so it ships: check a long line in halves before remaking it. noodles L2
  "الطازجة" -> the Saudi "الطازة"; L13 remade as "ومبروك... كذا سويت لك" (Whisper heard "كيف أساعد لك" before).
- The cover parser (bik/cover.py _AR) does not take "..." after مبروك: noodles.py overrides draw_cover to read it as a
  comma ("مبروك، كذا سويت لك" + "النودلز"). Keep closers in the plain frame when you can.
- Scenes (v2 look 2):
  - museum.py (ring, grow, street, panel, glass, mom): the torus as the band between two ellipses (rp(u, s): u around
    the ring, s from the void's edge 0 to the outer edge 1), a 36 x 2 diagrid drawn as polylines in band space, the
    calligraphy windows as abstract strokes from a seed (no real words: no loops, they read as zeros), a hill drawn
    after the ring to hide its foot, x-ray floors, a blueprint with jittering trial nets settling into one, a truck
    whose curved beam jams under a sign gantry, a saddle mould that wrinkles a flat sheet, a robot arm, a water jet
    tracing a letter with PathMeasure; tag: mom with a spray bottle in front of the ring and a window cleaner's cradle.
    Lesson: the first layout put the ring's lower half in the caption band; camera y 190-210 at zoom 1.1 keeps it
    above y 1240.
  - rainvortex.py (inside, roof, section, sink): the dome seen from inside (ribs and rings converging on the oculus,
    a funnel of falling water with streaks, a clear drum, terraced forest, a sky train, a light-show palette at night),
    the doughnut roof from above with rain running to the hole, a section (arch with the oculus off centre, floors
    stepping down, pit, pool, tanks, pump and pipe loop, air streamlines with dash_paint, a low glass wall); camera
    (OX, 135, 0.85) keeps the floor and pit above the captions, the reveal pulls out to 0.74 to show the tanks.
  - noodles.py (macro, fresh, dry, pot, shed, kitchen, cup, tag): a noodle brick of wavy lines, a strand blown up with
    pores, steam out (frying) and water in (soaking), a plate with growing mould and a day calendar, a drying rack, a
    slow pot with a clock, a backyard shed with a wok, the cup in x-ray with the block at the bottom (cracks) or wedged
    mid-cup (water swirling under it), a bouncing van; the tag differs by language (EN a 3-minute timer and someone
    crunching; AR end of the month, three cups). Lesson: light gold and white bloom to flat shapes: mid-tone gold for the
    strand, a warm cream cup.
- Produce (one slug per run, about 16 minutes of rendering each, 03:33-03:50Z): museum EN 69.4 s / AR 70.0 s, rainvortex
  EN 69.1 / AR 69.2 s, noodles EN 69.1 / AR 69.1 s; all -14.0 LUFS, peaks -1.9 to -2.2 dBFS, covers true (the noodles
  Arabic cover reads "مبروك، كذا سويت لك" + "النودلز"). QA sheets and covers looked at in both languages. Whisper small
  on the three English mixes: number formats, "Y'all" -> "Yo", "And congrats" -> "Hey, congrats" only (CI's base.en
  heard "glass" as "blast" and "a pot and a stove" as "a pot in a soul"; small hears both right). Anchors all found,
  sweeps and save checks clean in both languages.
- Posts: posts/ep97-museum.yml, ep98-rainvortex.yml, ep99-noodles.yml pushed after the Pages deploy of 13e6a9a (the
  last produce commit) succeeded. All 12 Instagram + TikTok targets wait for Buffer places (every channel 10 of 10
  with 92-96 first in due-time order); later post.yml runs add them. Check-in of this session at 12:30Z Nov 27 (04:30
  PT Fri, trig_013c6esiLCurkqCNWftgX4jQ) dispatches post.yml if any of 94-99 still waits and requeues failures.
- Check-in 12:37Z Nov 27 (04:37 PT Fri): every Instagram + TikTok target of 94-99 is on Buffer at its Fri Nov 27 PT
  time (94's Arabic Instagram + TikTok and 95's Arabic Instagram already out); nothing failed, nothing dispatched.

## Nov 26 2026 (midday run, 11:23 PT): 100 the Jeddah Tower, 101 a fire sprinkler, 102 Al Bahar Towers (v2; post Sat Nov 28)
- TODAY Thu Nov 26 PT (Thanksgiving), TOMORROW Fri Nov 27 PT, but Friday already carries six builds (94-99), so 100-102
  take Saturday's first three slots, as the evening run of Nov 25 set out: EN 06:00 / 08:30 / 11:00 PT = 14:00Z /
  16:30Z / 19:00Z Nov 28; AR Instagram 00:00 / 03:00 / 06:00 PT = 08:00Z / 11:00Z / 14:00Z; AR TikTok 00:30 / 03:30 /
  06:30 PT = 08:30Z / 11:30Z / 14:30Z (3 h after 99's 21:30 PT Fri). Every at: turned back into PT with
  `TZ=America/Los_Angeles date -d` before the push. YouTube: verified, so all three hold it with `studio: 1`.
  NEXT FREE SLOTS (the evening run of Nov 26, builds 103-105; 102's line 10 promises bubble wrap): Sat Nov 28 English
  13:30 / 16:00 / 18:30 PT, Arabic Instagram 09:00 / 12:00 / 15:00 PT, Arabic TikTok from 12:30 PT (2 h after the show's
  10:30 PT). 08:30 PT Sat (16:30Z) is left free in the Arabic TikTok grid for the sm04 requeue the show run planned.
- Status 19:30Z: Thursday's English 89, 90, 76, 77, 91 out (92 13:00, 93 15:30 PT scheduled); Arabic Instagram 88-90,
  76, 77 out (91, 92, 93 tonight); Arabic TikTok 88, 89 out, 90 refused (14:00Z), 85's requeue refused (16:00Z), 76
  refused (20:30Z), 77, 91, 92 scheduled tonight. Not requeued: the Arabic TikTok queue is 10 of 10 again and the grid
  has no 2-hour gap before Saturday. In error now: 48, 50, 54, 56, 60, 62, 66-69, 72-74, 76, 82, 83, 85, 90 (+ sm03, sm04).
- yt_desk check: OVERDUE sm05 (all four: AR full 09:00, EN full 10:00, AR Short 10:30, EN Short 12:15 PT Thu): the main
  chat's round of Nov 25 16:45 PT did not upload them, so sm05's six TikTok + Instagram targets are still on hold (no
  show today). `yt_desk.py plan` also lists Thursday's builds 88-93, 76, 77 as due and not uploaded (the last ledger
  entries are from 01:07Z Nov 25). Told the owner at the top of the run's message; not repaired here.
- post.yml had not run since 04:02Z: a dispatch at 19:37Z added the waiting targets of 92-97 and 98 (English +
  Arabic Instagram). FIXED: ep99's English Instagram + TikTok were refused by post.py ("6 hashtags (limit 5)"): its
  `next:` "Build #100, the Jeddah Tower" made the cta line carry a hashtag. Now "Build 100, ..." (both scheduled at
  02:30Z Nov 28). Never put a "#" in `next:` or `text:` (100's caption says "Our 100th build"). 99's Arabic TikTok
  waits for a queue place (later post.yml runs; the 12:30Z Nov 27 check-in of the evening run of Nov 25).
- BUFFER API ALLOWANCE (state/last-run.md, the "30d" r=): Arabic 356 at 01:59Z -> 174 at 21:25Z, English 443 -> 253:
  about 170 a day each, and the 30-day window resets only in about 13.4 days (about Dec 10). Every post.yml run cost
  about 15 per account (post.py 2-4, then status.py about 11: it lists every post, 25 a page); a tools.yml status run
  and the status.yml cron (about twice a day) about 13 each. At that pace the Arabic account runs out around Fri Nov 27
  and then nothing new reaches Buffer until the reset. FIXED IN PART: post.yml now skips status.py on push runs
  (dispatches, tools.yml status and the cron still look), so a push costs 2-4. Six builds a day still need about 25 a
  day for posting alone, more than 174 lasts: the owner was told. Dispatch post.yml or tools.yml only when something
  waits, and skip the metrics run while the allowance is this low.
- Why v2: jeddahtower-A was made at 09:12 PT, but jeddahtower-B and sprinkler-A/B, albahar-A/B were todo (the
  on-computer runner made no job at 10:08, 11:08 or 12:08 PT), so no build had both clips; all three are v2 and the five
  jobs are marked skipped in higgsfield/queue.yml (jeddahtower-A stays a spare). The runner then queued bubblewrap-A/B and
  gcans-A/B for 103-104.
- Pages: retired ep37 (its Arabic TikTok requeue went out), dubaiframe-b85 (only a refused Arabic TikTok), kettle-b86
  and balloon-b87 (all out); all Studio uploads of 85-87 are in the ledger: media/ 1.2 GB -> about 1.0 GB, about 1.1 GB
  with 100-102. Keep 78, 79, 88-93 and 76-77 until their Studio uploads are done (all listed due).
- Voices: ElevenLabs Pro 172,707 of 613,234 before (28%, day 5 of the period), 176,152 at the end (29%). Ballen
  v4 + Mansour v4. First takes: jeddahtower EN 66.0 s / AR 66.0 s; sprinkler EN 70.3 s (x1.12 cap: over the v2 gate)
  / AR 70.7 s; albahar EN 68.3 s / AR 68.8 s. Two English passes: sprinkler lines 1, 2, 4, 11, 14 shortened (the
  [chuckles] in the hook cost 0.6 s: hook 5.4 -> 4.9 s); albahar lines 2, 5, 10, 14 shortened, then line 2 again (0.1 s
  over the 9.5 s mark); jeddahtower line 8 "steel lift ropes" heard "still lift ropes", then "metal lift ropes" heard
  "metal if ropes" -> "metal ropes", line 14 "your glasses still fog up" heard "your glass is still fog of" -> "stepping
  out of the car still fogs up your glasses". Final: EN 66.0 / 66.3 / 66.0 s; hooks EN 4.3 / 4.9 / 4.6 s, problem by
  9.1 / 8.8 / 9.4 s; AR hooks 4.1 / 4.9 / 4.3 s, problem by 8.5 / 8.4 / 10.0 s (only the "Y'all," / "يا جماعة،" comma
  FAILs). check_ar_voice: no weak line except jeddahtower line 3 (42%: "ميتين وسبعين" and "مية وخمسة" written as digits).
- Research (WebSearch titles plus higgsfield/ideas.md, no agents): Jeddah Tower (Newsweek Oct 30 "484 meters", the
  121st floor, Newsweek "El Niño challenge before major milestone" = 500 m not reached yet, Thornton Tomasetti 270 piles
  up to 105 m under a 5 m raft, ENR on the shell limestone and the taper against vortex shedding, KONE's 630+ m
  UltraRope ride); fire sprinkler (FPA "only the heads in the area of the fire operate", NFPA Journal 2022: one head in
  77% of fires where they operated, failures mostly a system shut off; NFSA bulb colours; Parmelee 1874); Al Bahar (AHR
  2,098 units, DesignCurial 1,049 a tower with a motor in each, JFDE roof light/wind/rain sensors and the mid-fold in a
  storm, "about half" the solar gain).
- Scenes (v2 look 2):
  - jeddahtower.py (sky, ground, wind, plan, lift, tag): tower_hw(f) = a three-wing taper whose wings end at 66% and 79%
    of the height; jtower(built, plan, lit) = the solid part (mid-grey concrete: light grey bloomed white) and the rest as
    a dashed glowing outline drawn upward; crane(); ruler() to 1,000 M; outline_building() petronas / taipei / burj for
    the height race; ground_cut(sink, piles, raft) with shells in soft limestone; box_tower() + vortex() + wind_streaks();
    plan_view(wings) + pencil() + tripod(); lift_shaft(heavy, belt, rise) + scale_card(); car_door(fog). The hook opens
    close on the cranes (zoom 2.3) and pulls out to the whole kilometre: a thin tower alone was a weak first frame.
  - sprinkler.py (office, factory, bulb, bakery, valve, tag): proj() = a one-point perspective ceiling with about a
    hundred heads (scale 3.2/Z); head(bulb, fill, burst, old, melt) = a pendent sprinkler (frame, glass bulb with its
    bubble, toothed deflector; old=True: an 1870s brass rose with a soft-metal plug); spray() = an umbrella of falling
    streaks; tongue() = a flame of three mid-tone teardrops (v2.flame's white additive core bloomed into a white blob on
    the dark sets); bakery(chart) with the five bulb colours; valve_room(shut, chain, wrench, alarm, drip) with an
    upstairs inset; ring_gauge() for the 77%; cake() / mabkhara() for the tag (EN 90 candles, AR dad's incense in a hotel).
  - albahar.py (towers, city, office, lattice, unit, storm, tag): unit(o, fx) = an umbrella shade of six triangles whose
    angular width opens with o (o=0: thin spikes), fx squeezes it round the cylinder; shaded_tower(sun) opens the units
    that face the sun (sun = azimuth); the hook starts close on the sunny side (zoom 2.3) so the wave of opening shades
    reads, then pulls out to both towers; mid-tone cream fabric (white bloomed); glass_tower(tint, glare); office_dark();
    old_house() + lattice_window() + dappled(); actuator_unit() + screen_sun(); sandstorm() + an anemometer inset;
    sunshade(opened) for the tag (a twisted bundle that springs into two discs).
- Produce (one slug per run, 17-24 minutes each; 101 at 20:20Z, 100 at 20:29Z, 102 at 20:37Z): Jeddah Tower EN 69.1 s /
  AR 69.1 s, fire sprinkler EN 69.4 s / AR 73.8 s, Al Bahar EN 69.1 s / AR 71.9 s; all -14.0 LUFS, peaks -2.1 / -2.2
  dBFS, covers true (the cover pictures: the finished tower at night; the sprinkler head big; the two towers at dusk).
  QA sheets and covers looked at in both languages; Whisper small on the three English mixes: number formats, "Jedda",
  "Alba Haar", "Y'all" -> "Yo" only. Anchors all found, sweeps and save checks clean in both languages.
- Posts: 100 + 101 pushed 21:08Z after the Pages deploy of 8017043 (after both produce commits) succeeded; 102 pushed
  21:22Z after the deploy of 619a493 (after 10269ad, the Al Bahar produce commit) succeeded. State 21:25Z: all six
  English Instagram + TikTok targets of 100-102 scheduled (14:00Z / 16:30Z / 19:00Z Nov 28) and 100's Arabic Instagram
  (08:00Z); 100's Arabic TikTok, 101's and 102's Arabic Instagram + TikTok (and 99's Arabic TikTok) wait for queue places
  (every Arabic channel 10 of 10 with Thursday's and Friday's posts): later post.yml runs add them in due-time order; a
  check-in of this session at 06:30Z Nov 28 (22:30 PT Fri, trig_01B8mDajFB4ywxA6hPqkaNvx) dispatches post.yml once if
  any still waits.
- LINEUP: 109 the Eastgate Centre (Harare), 110 the Bahrain World Trade Center, 111 a pin tumbler lock appended (nine
  entries ahead of 102: 103-111).

## Nov 26 2026 (show run, 13:17 PT): Survival Mode 6 "You vs the Sea" (sm06) for Fri Nov 27
- TODAY Thu Nov 26 PT, TOMORROW Fri Nov 27 PT. Hand-off done 14:17 PT (the run took an hour).
- Step 0: status 21:30Z (13-14 Buffer requests per account: the "30d" line then read Arabic 161, English 239; no second
  status run and no `limits`). sm05 is NOT OUT on TikTok and Instagram: posts/sm05.yml still holds all six targets and
  state/sm05.json has none. `yt_desk.py check` prints all four of its YouTube videos as OVERDUE (the ledger's last entry
  is 01:07Z Nov 25). But the main chat's own round ("Build-It YouTube desk: afternoon round" in list_triggers, next
  16:45 PT today) says in its prompt that a commit "YouTube desk: 17 uploads scheduled for Nov 26" from the Nov 25
  round may be unpushed: so the uploads may exist on YouTube while the repo cannot show them. Told the owner at the top
  of the message; nothing repaired. For whoever picks sm05 up:
  (1) handoff.py force-pushes the `show` branch, so sm05's full cuts, thumbnails and sheet were kept first on the branch
  `show-sm05` (the same commit, 450f1e6; the links inside its sheet still say /show/).
  (2) sm05's `at:` times have passed, and post.py gives a released target with a past time "now + 2 minutes": release
  it only when its shorts should go out, or give it new times first. A release also takes four queue places.
- sm04's Arabic TikTok (in error since Nov 24) was not requeued: all four Buffer queues are 10 of 10 with the Arabic
  TikToks of 99-102 waiting for a place, requeue.py lists every sent post before it moves one (about a dozen of the 161
  requests left), and TikTok has refused every Arabic show short so far (sm03 twice, sm04). The slot the midday run kept
  for it (Sat Nov 28 16:30Z) is free for a build.
- Pick: burjalarab, suez, pharos, barrier (all Mansour, all v2): land where there is none, a shortcut between two seas, a
  light for ships at night, a wall against the storm. "No land. No shortcut. No light." names levels 1 to 3 and the
  storm is the final boss. Bosses: the waves / the detour (لفّة أفريقيا) / the dark / the North Sea; joke row "TIMES YOU
  GOT SEASICK 0" ("كم مرة دوّخك البحر؟"); line 8 ends "with sand, steam, fire and steel". Left out: 96-99 (they post as
  builds on Friday), 100-102 (Saturday), hagiasophia (show rule). Stock after sm06 (stock.py): fridge, washer, taipei,
  dishwasher, vacuum, petronas, handwarmer, museum, rainvortex, noodles, jeddahtower, sprinkler, albahar = 13 builds,
  three episodes (ideas: the house = fridge, washer, dishwasher, vacuum; towers against the wind = taipei, petronas,
  jeddahtower, albahar; then handwarmer, noodles, sprinkler, rainvortex, museum).
- Voices in one pass, nothing recorded twice. ElevenLabs read 176,152 before; Ballen (eleven_v4, x1.09) 907 characters,
  57.33 s; Mansour (eleven_multilingual_v2 through the `model` input, x1.09) 619 characters, 51.58 s; the account read
  187,886 afterwards (31%; the other 10,000 of that half hour were other projects). Whisper small: English only number
  formats and "beat the sea" heard "beat the C"; Arabic 0-3% a line, no weak lines. On the four finished files every new
  line is heard in its place (worst line 4% / 7% / 5% / 11%, under the effects).
- New in the layer: icons `shortcut` (a straight arrow over a dotted long way round) and `lighthouse` (layout.ICON).
- Two lessons, both in the README now. (1) `shot`: the Burj Al Arab's hook ends on bare sea and Suez's on a map (shots
  1.0 / 4.4 / 3.3 for the hotel, the ship in its canal, the whole lighthouse). The barrier's hook is a view from above,
  two thin arms on a river, which cannot be read in half a second; the storm pushing the sea over the dike (EN 11.7,
  AR 10.7) reads at once and fits the stamp "STORM SURGE" / "البحر جاي". (2) Arabic card 1: the ج of "الموج" ran into
  the sub "ما فيه أرض · كله بحر"; the sub is now "كله بحر" and the stamp "ما فيه أرض". Both were seen on full-size
  frames before the long render (a ten-line script: `Show(work, out, plan).frame(g, sequential=False)` for the four
  cards and the four flashes) and cost one restart each, two to three minutes.
- The session's clone: `main` and `origin/main` sat at a Nov 23 commit with HEAD detached at today's tip, so a plain
  `git fetch origin main` asked for three days of media and hung. `git update-ref refs/remotes/origin/main HEAD` and
  `git checkout -B main HEAD` first; then the fetch is instant, and the blobless deepen (`--deepen=800`) reached the
  barrier's videos (retired in 13a5e57).
- Cuts (all -14.0 LUFS): English full 4:44.9 (true peak -2.2 dBFS, 91.4 MB at crf 22, chapters 0:00 0:13 1:16 2:21 3:20
  4:24), short 1:26.6 (-2.0, 40.1 MB); Arabic full 4:50.1 (-2.2, 83.1 MB at crf 24, chapters 0:00 0:12 1:18 2:24 3:25
  4:31), short 1:27.7 (-2.3, 41.6 MB). Stills sheets and 160 frames pulled from the four finished files looked at
  (words, Arabic right to left, the right boss on each level). Render: both chains side by side, 13:50 to 14:14.
- Hand-off: media/sm06-en.mp4 + media/sm06-ar.mp4 and posts/sm06.yml on main with ALL six targets on hold.
  kit/show/youtube/sm06.yml -> handoff.py pushed the two full cuts, the two thumbnails and sheet.json to the `show`
  branch (b1baad3); every raw link answers 200 and `yt_desk.py plan` lists the four videos first on each channel (then
  builds 94-99). For Fri Nov 27 PT: Arabic full 09:00, English full 10:00, Arabic Short 10:30, English Short 12:15
  (YouTube, the main chat's 16:45 PT round); TikTok + Instagram Arabic 10:30 (18:30Z), English 12:15 (20:15Z) after
  `yt_desk.py release sm06`.

## Nov 26 2026 (evening run, 18:37 PT): 103 bubble wrap, 104 Tokyo's G-Cans flood tunnel, 105 the Brooklyn Bridge (v2; post Sat Nov 28)
- TODAY Thu Nov 26 PT, TOMORROW Fri Nov 27 PT, but Friday already carries six builds (94-99) and Saturday's first three
  slots hold 100-102, so 103-105 take Saturday's evening slots, as the midday run set out: EN 13:30 / 16:00 / 18:30 PT =
  21:30Z Nov 28 / 00:00Z / 02:30Z Nov 29; AR Instagram 09:00 / 12:00 / 15:00 PT = 17:00Z / 20:00Z / 23:00Z Nov 28; AR
  TikTok 12:30 / 15:30 / 18:30 PT = 20:30Z / 23:30Z Nov 28 / 02:30Z Nov 29 (2 h after the show's 10:30 PT, 3 h apart).
  Every at: turned back into PT with `TZ=America/Los_Angeles date -d` before the push. YouTube: verified, so all three
  hold it with `studio: 1`.
  NEXT FREE SLOTS (the runs of Nov 27, builds 106-111; 105's line 10 promises the Riyadh Metro): Sun Nov 29 PT, the usual
  grid (midday run EN 06:00 / 08:30 / 11:00, AR 00:00 / 03:00 / 06:00, AR TikTok 00:30 / 03:30 / 06:30 PT, 3 h after
  105's 18:30 PT Sat; evening run EN 13:30 / 16:00 / 18:30, AR 09:00 / 12:00 / 15:00, AR TikTok from 12:30 PT).
- Status 02:55Z (Nov 26 PT, Thanksgiving, builds 88-93 + 76-77): English Instagram + TikTok 89, 90, 76, 77, 91, 92, 93
  out at their slots (88 went Wed 22:00 PT); Arabic Instagram 88-90, 76, 77, 91, 92 out, 93 at 19:30 PT; Arabic TikTok
  88 and 89 out, 90, 76, 77, 91 and 85's requeue refused ("potential spam"), 92 at 21:30 PT. Nothing requeued: the Arabic
  TikTok grid has no 2-hour gap before Saturday evening, the queue goes to 99-105 first, and every requeue lists all
  sent posts first (about a dozen of the Arabic account's ~133 API requests left).
- yt_desk check: "nothing overdue", but only because the `show` branch's sheet.json now holds sm06 (due Fri): the check
  reads only the newest show. sm05's four Studio uploads (due Thu) are still not in youtube/ledger.json and posts/sm05.yml
  still holds all six targets. The ledger's newest entries are the Nov 25 round (80-88 EN, 78-87 AR).
- Metrics: not run (Buffer's 30-day allowance: Arabic 146 / English 223 at 22:20Z before this run's status run, reset
  about Dec 10). Entry in claude/build-it-performance.md without new numbers; run metrics once on Nov 28 for the two tests.
- Pages: nothing retired. Every build in media/ (1.2 GB) still has a Studio upload due (78-79 EN, 88 AR, 89-99, 76-77),
  a post ahead (80's AR TikTok requeue at 16:30Z Nov 27, 92-102) or is the show's (sm*). The 700 MB rule cannot hold
  while the Studio backlog lasts. media/ is 1.3 GB with 103-105 and the Pages upload is now 1.53 GB: the deploy step
  warns "exceeds the allowed size of 1 GB. Deployment might fail". It still deploys, but retire builds the moment their
  Studio uploads are done.
- Pages wait: every "pages build and deployment" run from 03:21Z to 04:38Z was cancelled by the other projects' pushes
  (darija voice, Yallah, higgsfield: every 1-5 minutes), and a run needs about 6 minutes (checkout 3.7 min, upload 50 s,
  deploy 50 s). Run 1667 (09a3a1e, after the produce commit b605066) shows "cancelled", but its deploy step logged
  "Reported success!" at 04:38:17Z: the push that cancelled it came a second after the deployment went live. The post
  files went up after that (post.py also checks each file on Pages with its exact size before it uses the link). Read
  the deploy job's log, not only the run's conclusion.
- Why v2: bubblewrap-A was done (13:30 PT) but bubblewrap-B, gcans-A/B and brooklyn-A/B were todo at 19:40 PT (the
  on-computer runner idle since 13:24 PT): all five marked skipped in higgsfield/queue.yml (bubblewrap-A stays a spare).
- Voices: ElevenLabs Pro 187,886 of 613,234 used before (31%, day 5), 191,687 after the remakes (+3,801, other
  projects included). Ballen v4 + Mansour v4. First takes: bubblewrap EN
  66.0 s (x1.076) / AR 66.0 s; gcans EN 68.77 s (x1.12 cap, over the v2 gate) / AR 69.73 s; brooklyn EN 67.81 s (cap) /
  AR 66.0 s. Remakes (changed lines only): gcans hook "for floodwater" -> "for floods" and line 2 "the towns north of" ->
  "towns near" (hook 5.5 -> 4.8 s, problem by 10.2 -> 9.3 s), lines 3, 7, 9 shortened, AR hook and line 2 shortened (problem
  by 10.3 -> 9.6 s); brooklyn lines 3 and 9 shortened. Final: bubblewrap 66.0 / 66.0 s, gcans 66.03 / 69.05 s, brooklyn
  66.33 / 66.0 s; hooks EN 3.9 / 4.8 / 4.9 s, problem by 8.1 / 9.3 / 9.3 s; AR 4.8 / 4.8 / 4.4 s, by 9.1 / 9.6 / 8.7 s (only
  the known "Y'all," / "يا جماعة،" comma FAILs).
- Whisper small on Ballen: gcans "five wells" -> "five whales" (line 4 now "But they fill up in no time"), brooklyn
  "Its designer died" -> "Its desire died" (now "Its engineer died"); both remade and heard right. Otherwise "Y'all" ->
  "Yo", number formats, "Edo" -> "Ido", "computer" -> "computers". check_ar_voice: no weak lines (max 30%, brooklyn's
  digit line 9; bubblewrap lines 3 and 5 about 20%: "فحبسوا", "فسووا").
- Research (WebSearch titles only, no agents): bubble wrap (Smithsonian "the accidental invention of bubble wrap",
  Mental Floss, Wikipedia: Fielding and Chavannes 1957, two shower curtains, wallpaper and greenhouse flops, Sealed Air
  1960, IBM's 1401; iBubble / flat-shipped film inflated on site); G-Cans (MLIT Edogawa office, Scientific American,
  Tokyo Updates, Wikipedia: 6.3 km tunnel about 50 m down, five shafts about 70 m, the 177 x 78 x 18 m tank with 59
  pillars of about 500 t, four aircraft-type gas-turbine pumps, about 200 m3/s, "a 25 m pool in about a second");
  Brooklyn Bridge (History.com, Wikipedia, Linda Hall, ASCE: John Roebling died 1869 before work began, caissons and the
  bends, Washington bedridden with a telescope, Haigh's bad wire and 150 extra wires a cable, 5,434 wires a cable, Emily
  first across May 24 1883 with a rooster, Barnum's 21 elephants May 1884).
- Scenes (v2 look 2):
  - bubblewrap.py (wall, box, factory, truck, computer, sheet, tag): bubble(c, x, y, r, popped, squash) and sheet() = a
    hex grid of clear domes on a film, culled to the clip bounds (the zoomed hook drew ~440 bubbles: 1.4 s a frame);
    wall_room() = a 1957 living room papered with bubbles; card_box() a box with its front cut away; vase(broken);
    air_pillow(squash, popped) with molecules; drum() with cups and vacuum arrows; truck(cargo air|flat, coins);
    computer() = three 1959 cabinets with lights and tape reels, wrapped and crated; roll(unroll, big) for the closer;
    tag EN a giant box with one phone charger, AR mom's sofa still in its plastic ("من خمس سنين!").
  - gcans.py (hall, town, section, pool, tag): hall() = one-point perspective (HZ 880, F 700) of pillars at Z 14-140 m with
    ceiling light beams and tiny people; town() a typhoon; the section (surface y 470, tunnel y 900): shaft(), tunnel(surge),
    tank(level, calm), pump_house(on, lift) with four turbine fans, edo_river(); pool() + stopwatch() for the reveal; tag EN a
    sink clogged by one noodle, AR a street flooded after ten minutes of rain. Lesson: a light kitchen and a white car
    bloomed to white; keep tag sets mid-tone.
  - brooklyn.py (bridge, office, river, bends, cable, emily, tag): bridge() side view (deck y 820, towers x 270 / 810 with
    pointed arches, cable_y() catenary spans, stays and suspenders, lamps at night); elephant() walking, 21 of them in the
    hook (the stat's elephants use t - s("stat"), or they walk off screen); desk() 1869 with the drawing; caisson_section()
    (sink, water_in, air, dig, stones); blood_inset() bubbles; window_room() telescope; cable_cut(bad, snap, extra) =
    hex-packed wires and +150 green ones; lady() an 1880s dress, rooster(), carriage(); plastic_chair(broke) for the tag.
- LINEUP: 112 the Sydney Harbour Bridge, 113 Abu Dhabi's Formula Rossa, 114 an aluminum soda can appended (nine entries
  ahead of 105: 106-114).
- State (posting run 04:44Z Nov 27): 103's EN Instagram + TikTok (21:30Z Nov 28) and AR Instagram (17:00Z) scheduled;
  103's AR TikTok and all eight Instagram + TikTok targets of 104-105 wait for Buffer places (every channel 10 of 10 with
  94-99 and 100-103). The same run scheduled 99's and 100's AR TikToks and the AR Instagram of 101-102 (101's and 102's AR
  TikToks still wait). The runs of Nov 27 add them with their pushes as Friday's posts go out; the midday run's check-in
  at 06:30Z Nov 28 (trig_01B8mDajFB4ywxA6hPqkaNvx) and this run's at 15:00Z Nov 28 (trig_01Juzuz8MiV4WvyYVXvx3QgF)
  dispatch post.yml once if any still waits. Buffer's 30-day allowance after the run: English 205, Arabic 126 requests.

## Nov 27 2026 (midday run, 11:23 PT): 106 the Riyadh Metro, 107 a high-speed chairlift, 108 an ice resurfacer (v2; post Sun Nov 29 PT)
- TODAY Fri Nov 27 PT, TOMORROW Sat Nov 28 PT, but Saturday already carries six builds (100-105), so 106-108 take
  Sunday's first three slots, as the evening run of Nov 26 set out: EN 06:00 / 08:30 / 11:00 PT = 14:00Z / 16:30Z /
  19:00Z Nov 29; AR Instagram 00:00 / 03:00 / 06:00 PT = 08:00Z / 11:00Z / 14:00Z; AR TikTok 00:30 / 03:30 / 06:30 PT =
  08:30Z / 11:30Z / 14:30Z (6 h after 105's 18:30 PT Sat). Every at: turned back into PT with
  `TZ=America/Los_Angeles date -d` before the push. YouTube: verified, so all three hold it with `studio: 1`.
  NEXT FREE SLOTS (the evening run of Nov 27, builds 109-111; 108's line 10 promises the Eastgate Centre, "an office
  that breathes like a termite mound"): Sun Nov 29 PT English 13:30 / 16:00 / 18:30, Arabic Instagram 09:00 / 12:00 /
  15:00, Arabic TikTok from 12:30 PT, 3 h apart.
- Status at the start (tools.yml status, about 19:30Z): Friday's English 94, 95, 96 out at 06:00 / 08:30 / 11:00 PT (97
  13:30, 98 16:00, 99 18:30 PT scheduled); Arabic Instagram 94-97 out (98 12:00, 99 15:00 PT); Arabic TikTok 94 out, 95
  refused (06:30 PT), 80's requeue refused (08:30 PT), 96 12:30, 97 15:30, 98 18:30, 99 21:30 PT scheduled. Nothing
  requeued: every requeue lists all sent posts first and the Arabic account has almost no API requests left (below).
- yt_desk check: OVERDUE sm06, all four (AR full 09:00, EN full 10:00, AR Short 10:30, EN Short 12:15 PT Fri): the main
  chat did not upload them, so posts/sm06.yml still holds its six TikTok + Instagram targets. The ledger's newest
  entries are still the Nov 25 round. Told the owner at the top of the run's message; not repaired here.
- BUFFER API ALLOWANCE ("30d" r= in state/last-run.md): after the status run Arabic 87 / English 163; after the
  retirement push (19:51Z) 78 / 157; after this run's post-file push (21:10Z) Arabic 72 / English 153; resets in about
  12.4 days (about Dec 10). A production run costs about 13 (status) + 4-9 (push) per account and the status.yml cron
  about 13 twice a day: the Arabic account runs out around Sat Nov 28, after which no new Arabic post reaches Buffer until
  the reset. The owner was told (his call: Buffer's API upgrade, fewer status runs, or a pause). This run made no
  requeue, one push for all three post files and no check-in.
- Pages: retired ep76, airfryer-b78, kuwaittowers-b79, fountain-b80, pontdugard-b88, noor-b89, pen-b90 (41ce37e):
  TikTok + Instagram all out or only a refused Arabic TikTok left, and their Studio dates more than a day past (the
  desk offers only videos that go public tomorrow, so it no longer lists them; the files are in git history at
  41ce37e^ if the main chat still wants them). media/ 1.3 -> 0.97 GB, 1.1 GB with 106-108.
- Why v2: riyadhmetro-A/B and chairlift-A/B were todo at 12:20 PT (no build had both clips; nothing was queued for 108):
  the four jobs are marked skipped in higgsfield/queue.yml; next pair eastgate-A/B (109), and the runner queued
  bahrainwtc-A/B (110) at 13:00 PT.
- Voices: Ballen v4 + Mansour v4, about 6,600 ElevenLabs characters with the remakes (only changed lines cost). Voice
  runs 204-206 (first takes 19:46Z), 207-209 (rewordings 20:00Z), 210 (107 line 8, 20:09Z). Riyadh EN first take 67.7 s
  at the x1.12 cap (the video would be 70.8 s, over the 70.5 s v2 gate): five lines shortened. Whisper small on Ballen:
  Riyadh "groundwater" heard "brown water" (line 4 now "they hit water! Lots of it!") and "Riyadh Metro" heard "Rehab
  Metro" (reworded and remade); chairlift hook and line 2 too slow for the 5 s / 10 s marks (hook now "these chairs let
  go of their cable... on purpose"), "warm" heard "worn" and "steel" heard "still" (line 8 now "that cable gets longer
  in the heat, and loose cable slips"); resurfacer line 9 "hot water" heard "out water" ("spreads water... hot water!").
  Arabic: resurfacer line 9 "ففوطة" -> "وورا، فوطة". Final voices: Riyadh EN 66.7 s (x1.12) / AR 66.0 s, chairlift 66.0
  / 66.3 s (x1.12), resurfacer 66.0 / 66.0 s; hooks EN 4.4 / 4.1 / 4.4 s with the problem told by 9.0 / 8.8 / 9.4 s, AR
  4.2 / 4.2 / 4.3 s by 9.0 / 9.0 / 9.0 s. check_ar_voice: only Riyadh's digit line 12 weak (38%: "دقيقة 2.5").
  check_en_voice on the final resurfacer voice: number formats and "'cause" only.
- Anchors after the rewordings: Riyadh ("break2", "LOTS") with KEYS ("break2", "LOTS") -> "جوفية"; chairlift
  ("break4", "CABLE") -> "كيبل". Both languages "anchors: all found".
- Research (WebSearch, no agents): Riyadh Metro 176 km, six lines, 85 stations, the longest driverless metro network,
  TBMs and viaducts, groundwater pumped out and watertight tunnel lining, a control centre, platform screen doors,
  over 180 trains; detachable chairlifts: the grip opens in the station, tires slow the chair to a walk and speed it
  back up, springs close the grip and a weak grip stops the lift, a concrete counterweight keeps the cable tight as it
  grows in the heat, about 1,000 ft (300 m) a minute and 1,800 people an hour, the first chairlift by James Curran of
  the Union Pacific (Sun Valley, 1936) from his banana-loading hooks; ice resurfacer: blade, auger, wash jets, vacuum,
  a towel spreading hot water that melts the top and bonds, Frank Zamboni 1949 in Paramount, California, about 15
  minutes against about 90 by hand.
- Scenes (v2 look 2):
  - riyadhmetro.py (city, traffic, section, net, platform, map, tag): a night skyline with a Kingdom-Centre-like and a
    Faisaliah-like tower, the viaduct and a driverless train with a kid at the front window (the hook zooms 3.0 -> 1.0
    off the kid); a traffic jam with a 50 °C thermometer; the section with a TBM (tunnel +-90 px), a groundwater layer,
    pumps and lining rings, a train on the viaduct (train_x lerp 1125 -> 1700); six coloured lines and a crossed-out
    driver's cap on a dark disc, then a control room zoomed in; glass platform walls and doors; a 176 counter (Arabic:
    "176" + "كيلو" through arabic.text_ar) and a medal; tag: the uncle from behind in a red-checked shemagh steering an
    imaginary wheel.
  - chairlift.py (closer, station, slope, grip, terminal, port, tag): lift_line() between CAB0 (110, 1090) and CAB1
    (790, 560), the top station at CAB1 (the hook at a station placed further right showed black past the world's
    edge); closer_scene() a big foreground chair (scale 1.55) on a raised cable, also the cover; the station with the
    chair at scale 2.2, a bike for the speed, a skier knocked flat, tires and a speedo; grip_closeup() springs, a tester
    and STOP; terminal() heat sag and the counterweight pit; port() bananas to chairs; tags EN a glove dropped halfway
    up, AR the wedding buffet line (thobes toned to #C9D1DC / #B3BCC9 so they do not bloom white). floor_dark(c,
    y=1250) and mid-tone snow (#C3D0E2 / #9AACC6 / #71839F).
  - resurfacer.py (rink, grooves, cutaway, lens, reveal, tag): mid-tone ice (#9DB7D3 / #7F9DC0 / #6382A8, gloss
    #4F86C2); a top-down rink with a wet strip behind machine_top(); machine_side() cut away (blade, augers, jets,
    vacuum, towel) zoomed 1.45 -> 1.0 before break3, on a dark floor; a magnifier at (250, 590) r 160 for the bond;
    tags EN an arena cheering a mop vs the kitchen (dark floor), AR mom: "لا تشرب بارد وأنت حرّان!".
  - Lessons: build a skia Path first and then call addCircle on it (do not use the return of Path().addCircle(...));
    there is no sfx.rumble or sfx.screech (rumble comes from v2set); light snow, ice and machine colours bloom to
    white under the captions: mid-tones and a dark floor below y 1250.
- Produce (one slug per run: 106 at 20:41Z, 107 at 20:51Z, 108 at 21:00Z): Riyadh EN 69.8 s / AR 69.1 s, chairlift EN
  69.1 s / AR 69.43 s, resurfacer EN 69.1 s / AR 69.1 s; all -14.0 LUFS, peaks -1.9 to -2.2 dBFS, covers true (the
  driverless train on the viaduct at night, a four-seat chair on the cable over the slope, the rink from above with the
  machine and its glossy strip). QA sheets and covers looked at in both languages. Whisper on the mixes (report.json):
  number formats, "Y'all" -> "Yo", dropped "So"/"And", Riyadh "a train" -> "are trained", resurfacer line 2 "with hot
  water" -> "without water" (the voice alone is heard right; the caption carries it), "grooves" -> "droves", "packed
  arena" -> "pacterena".
- Posts: one commit (067865a) pushed at 21:07Z after the Pages deploy of c8ff1cf (after all three produce commits)
  logged "Reported success!" at 21:06:15Z. State 21:10Z: 106 all four scheduled (EN 14:00Z, AR Instagram 08:00Z, AR
  TikTok 08:30Z Nov 29); 107's and 108's AR Instagram scheduled (11:00Z / 14:00Z); 107's and 108's EN Instagram +
  TikTok and AR TikTok wait for Buffer places (every channel 10 of 10 with Friday's 97-99 and Saturday's 100-105). The
  evening run's push adds them first (due-time order) once two of Friday's posts are out on each channel (English 97-98
  by 16:00 PT, Arabic TikTok 97-98 by 18:30 PT); the runs of Nov 28 add any still waiting before the first slot, 107's
  AR TikTok at 03:30 PT Sun. The check-ins of Nov 26 (trig_01B8mDajFB4ywxA6hPqkaNvx 06:30Z, trig_01Juzuz8MiV4WvyYVXvx3QgF
  15:00Z Nov 28) only look at 99-105. If the Arabic allowance runs out first, the Arabic TikToks of 107-108 cannot be
  added: tell the owner, do not dispatch again.
- LINEUP: 106-108 taken; 115 a tower crane, 116 the Akashi Kaikyo Bridge, 117 float glass appended (nine entries ahead
  of 108: 109-117).
