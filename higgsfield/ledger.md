# Higgsfield generations (every chat appends one line per file; newest at the bottom)
# date PT | project | model | file in release ai-media | prompt in a few words | used where
2026-11-23 19:50 | buildit | Seedance 2.5 720p 9:16 5s (unlimited) | buildit-taipei-hook.mp4 | golden sphere swinging inside a skyscraper top floor, typhoon night | Taipei 101 sample (kit/episodes/taipei3.py), hook
2026-11-18 | buildit | Kling 3.0 9:16 5s (credits) | buildit-pyramid-hook-kling.mp4 | Great Pyramid gleaming white, drone rise | Nov 17 look sample, unused
2026-11-23 19:55 | buildit | Seedance 2.5 720p 9:16 5s (unlimited) | buildit-taipei-storm.mp4 | Taipei 101 in a typhoon from street level, crane up | Taipei 101 sample, break1
2026-11-23 20:10 | buildit | Seedance 2.5 720p 9:16 15s 3 shots (unlimited) | buildit-taipei-reveal.mp4 | 0-5 giant gold sphere swinging, 5-10 pistons, 10-15 tower at dawn | Taipei 101 sample, reveal + stat
2026-11-23 20:00 | buildit | Seedance 2.5 720p 9:16 15s 3 shots (unlimited) | buildit-goldengate-3shots.mp4 | 0-5 towers out of fog, 5-10 1930s workers on catwalk, 10-15 main cable close-up | stock for build 77 Golden Gate
2026-11-23 19:56 | scary | Seedance 2.5 720p 9:16 30s, 6 shots (unlimited) | scary-baron-palace-6shots.mp4 | Baron's Palace Cairo night: tower window glow, locked gate, watchman, smoke, tower fire, fire fades | Baron's Palace sample Short (EN+AR); shots reusable: palace exterior, gate, watchman, smoke crowd
- Nov 23 20:05 PT · Seedance 2.5 unlimited 30 s 9:16 720p · Taipei full-Seedance clip A (6 shots) → ai-media/buildit-taipei-sdA.mp4 · great, all 6 shots usable
- Nov 23 20:09 PT · Nano Banana Pro unlimited 9:16 1K · Taipei storm cover → ai-media/buildit-taipei-cover-nbp.png · good cover, tower not exact
- Nov 23 20:13 PT · GPT Image 2.6 Sunburst unlimited 9:16 · Taipei 101 blue hour → kit/out/aishots/buildit-taipei-bluehour-gpt.png · accurate tower
- Nov 23 20:19 PT · Seedance 2.5 unlimited 30 s · Taipei clip B (6 shots: tuned, swinging, pistons, dishwasher, deck, coffee)
- Note: image models with UNLIMITED badge (Nano Banana Pro/Nano Banana, GPT Image 2.6 Sunburst/Flare, GPT Image 2.5, Seedream 5.0 lite/Pro/4.5, FLUX.2 Pro, Kling O1, Auto) run in parallel with the Seedance video job. Unlimited needs batch 1/4 (4 images turns Unlimited off and costs credits). Only Seedance 2.5 is unlimited for video.
2026-11-23 20:11 | scary | GPT Image 2.6 Sunburst 16:9 2K (unlimited) | scary-baron-thumb-en.png | Baron's Palace thumbnail with text LOCKED SINCE 1950s / WHO LIT THE FIRE? | long video 1 thumbnail (EN)
2026-11-23 20:13 | scary | GPT Image 2.6 Sunburst 16:9 2K (unlimited) | scary-baron-thumb-bg.png | same palace, no text, left side clear | long video 1 thumbnail (AR, Arabic text added in code)
2026-11-23 20:32 | scary | Nano Banana Pro 9:16 2K (unlimited) | scary-roushdy-street.png | busy Alexandria street at night, dark unfinished 11-storey block | Roushdy Short, context
2026-11-23 20:32 | scary | Nano Banana Pro 9:16 2K (unlimited) | scary-roushdy-stairs-flashlights.png | three silhouettes climbing a concrete stairwell with flashlights | Roushdy Short, 2012 climbers
2026-11-23 20:33 | scary | Nano Banana Pro 9:16 2K (unlimited) | scary-roushdy-owner-desk.png | 1960s desk, bank papers, brass keys, oil lamp | Roushdy Short, owner theory (reusable: any 'old papers' beat)
2026-11-23 20:33 | scary | Nano Banana Pro 9:16 2K (unlimited) | scary-roushdy-top-window.png | low angle up a dark concrete block, one top window lit | Roushdy Short, doubter + closing
2026-11-23 20:36 | scary | GPT Image 2.6 Sunburst 16:9 2K (unlimited) | scary-roushdy-thumb-en.png | EMPTY FOR 60 YEARS / WHO TURNS ON THE LIGHT? | Roushdy long video thumbnail (EN)
2026-11-23 20:31 | scary | Seedance 2.5 720p 9:16 30s, 6 shots (unlimited) | scary-roushdy-6shots.mp4 | unfinished concrete block Alexandria night: flickering window, bricked entrance, flashlight stairwell, empty apartment with shape, passersby, top window light on/off | Roushdy Short (EN+AR); reusable for any abandoned-building story
- Nov 23 20:59 PT · Seedance 2.5 unlimited 30 s 9:16 · Build-It 76 pressure cooker job A (queue cooker-A) → buildit-cooker-sdA.mp4
- Nov 23 21:19 PT · Seedance 2.5 unlimited 30 s 9:16 · Build-It 76 pressure cooker job B (queue cooker-B) → buildit-cooker-sdB.mp4
- Nov 23 21:41 PT · Seedance 2.5 unlimited 30 s 9:16 · Build-It 77 Golden Gate job A (queue goldengate-A) → buildit-goldengate-sdA.mp4
- Note Nov 23 21:55 PT (hourly runner): this task runs in the cloud, without the owner's Chrome, so its runs cannot press Generate or make stills. They can still read History with no Chrome and no credits: Higgsfield MCP show_generations (type video, only_completed false) gives each job's status, full prompt and results.rawUrl (the clip link for ai_media.py fetch). goldengate-A was fetched that way. The main chat's own slot check keeps starting jobs meanwhile.
