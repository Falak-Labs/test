# Higgsfield for every project: the free (unlimited) models, how to use them, and the plan

The owner (Ahmad), Nov 23 2026 19:30 PT: "I want you to use all of it, take advantage of everything and be smart."
His Higgsfield Plus plan (annual) has UNLIMITED generations on these models, but ONLY on the website higgsfield.ai in
his Chrome. Through the Higgsfield MCP connector the same models cost credits, and only 29 credits are left.

| Model (website)            | Kind  | Unlimited until            | Use it for |
|----------------------------|-------|----------------------------|------------|
| Seedance 2.5 (720p or 480p) | video | **Nov 28 2026** (14-day)   | cinematic shots: hooks, reveals, B-roll, intros |
| GPT Image 2.6 / 2.6 Flare  | image | Jan 13 2027 (60-day, 2K)   | keyframes, thumbnails, covers, scene art, text in pictures |
| GPT Image 2.5              | image | Jan 13 2027                | same |
| Nano Banana Pro            | image | Jan 13 2027 (2K)           | photoreal stills, edits of a picture, consistent characters |
| Seedream 5.0 Pro           | image | Jan 13 2027 (2K)           | stylized art, posters, backgrounds |
| Nano Banana, Kling O1 Image, Seedream 4.5, Seedream 5.0 Lite | image | while subscribed | everyday pictures after Jan 13 |

Not unlimited: Kling 3.0 / 4.0, Veo, Seedance at 1080p or 4K, sound, music. Those cost credits: do not use them.

## The rules (every chat)
1. **Never spend credits.** Only press Generate when the button says **Generate Unlimited**. Do not use the Higgsfield
   MCP generate tools for these models (they bill credits). If a button shows a number, stop and fix the settings.
2. **Video settings that make Seedance free:** higgsfield.ai/ai/video, model Seedance 2.5, Quality **720p** (or 480p),
   Bitrate **Standard**, sound **Off** (the speaker toggle under the prompt), Aspect Ratio as you need (9:16 for Shorts,
   TikTok, Reels; 16:9 for long YouTube), Duration 5s (4-30 s allowed; longer clips take longer), then scroll the left
   panel to **Unlimited mode** and switch it ON. The button must read "Generate Unlimited".
3. **One video at a time for the whole account.** The site runs one unlimited video job at a time and all the owner's
   chats share it. Before you press Generate, open History on the video page: if any card says "Generating", wait
   (check every minute) and do not press Generate twice. A 720p 5 s clip takes a few minutes. Pictures are faster.
4. **Your own Chrome tab.** Work in a tab you opened (Claude in Chrome tools), never in the owner's tabs or another
   chat's tab, and close it when you are done. Never type passwords or codes; if the site asks to sign in, tell the owner.
5. **Get the file out:** when a clip is done, read its link from the page (the <video> element of the finished card;
   pictures: the <img> of the result) and run the workflow **Fetch media** (.github/workflows/fetch-media.yml):
   `gh api -X POST repos/Falak-Labs/test/actions/workflows/fetch-media.yml/dispatches -f ref=main -f 'inputs[items]=<name>.mp4=<link> <name2>.png=<link2>'`
   or simply `python3 scripts/ai_media.py fetch <name>.mp4=<link> <name2>.png=<link2>` (it starts the workflow, waits and
   confirms). The runner downloads them (this workspace cannot reach Higgsfield's file host) and keeps them as assets
   of the release **ai-media** (not in git history). Get one back: `python3 scripts/ai_media.py get <name>.mp4 <folder>`;
   see what is there: `python3 scripts/ai_media.py list [filter]`. (`gh release download` does not work in these
   sessions: it needs GraphQL.) Finished clips live at https://d8j0ntlcm91z4.cloudfront.net/user_.../hf_<date>_<job>.mp4.
   Name files `<project>-<topic>-<shot>.mp4`, e.g. `buildit-taipei-hook.mp4`, `scary-ep07-door.mp4`, `yallah-kitchen-bg.png`.
6. **Log every generation** in higgsfield/ledger.md (one line: date PT, project, model, file name, the prompt in a few
   words, used where). Read it first: reuse a shot another project already made before you make a new one.
7. **Stay in your lane:** each project's AI shots follow that project's own style rules and topics. Nothing sexual,
   no real people's faces in made-up scenes, no copyrighted characters or logos.

## The plan to get the most out of it
**Nov 23-28: Seedance video days (the free video ends Nov 28).** Video is the scarce part, so every chat makes its
stock of clips now, best ideas first, and keeps them in ai-media for the weeks after:
- Build-It (Congrats Engineer / Kef Tenbeni): a hook shot and a reveal shot for each build in kit/series/LINEUP.md
  ahead of production, plus intro/level shots for the 4-minute show; 9:16, cinematic 3D look.
- The Dark Told Me (scary stories): atmosphere shots (doors, corridors, lights, shadows, weather) usable in many stories.
- Yallah Say: short scene shots of the lesson situations (kitchen, market, taxi, cafe).
- Any other active project the owner names.
A rough share of the one video slot: Build-It and scary stories first (they post daily), then the others.
About 12-20 clips an hour fit through the one slot; keep it busy day and night while the window lasts.

**Nov 23 - Jan 13: picture days (GPT Image 2.6, Nano Banana Pro, Seedream 5.0 Pro, 2K).** Pictures are fast:
thumbnails for every long YouTube video, covers, scene art and backgrounds that our engines animate (slow zoom,
parallax, light), keyframes for later video, character sheets for recurring characters.

**After Jan 13:** Nano Banana, Kling O1 Image, Seedream 4.5 and 5.0 Lite stay unlimited while he is subscribed.

**First, a sample:** each chat makes ONE sample with these shots in its own project and shows it to the owner before
switching its production over.
