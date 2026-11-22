# Build-It lineup (shared by the two daily runs)

Two runs a day make three builds each (Nov 17 2026, the owner: "Let's start posting 6 videos a day"):
- **Build-It midday production** (11:23 PT) makes TOMORROW's first three builds.
- **Build-It daily production** (18:37 PT) makes TOMORROW's last three builds.

Rules:
- Each run takes the three lowest-numbered entries below that are not in episodes.yml yet and not taken, in this order.
  As soon as you pick them, add "(taken: midday|evening run of <TODAY in PT>)" to their lines and push this file, so
  the other run skips them. A mark older than a day whose build is still not in episodes.yml is free again.
- Line 10 of build N promises build N+1 as listed here (the other run may be the one that makes it), so the order
  below is the posting order. Never reorder or renumber entries that are already promised by a made build.
- Keep at least nine entries ahead of the ones you take: when fewer remain, research new ideas and append them before
  you write your scripts, and commit this file with your scripts. Favor what the numbers say works
  (claude/build-it-performance.md): famous mega-structures and places with a real story, and everyday things people
  use. Mix countries and cultures (the Arab world, Asia, Africa, Europe, the Americas). Avoid religious rituals,
  politics, anything that mocks a culture, gadgets-in-a-lab openers and far-away space pictures.
- Arabic voice A/B test (owner picked the Gulf voice Mansour, Nov 17 22:15 PT): for every ODD-numbered build from 41
  on, write the Arabic script in Saudi dialect (frames: "لو ...، مبروك، كذا سويت لك ..." / "بس قبل لا ...، تابعني،
  لأن الجاي بنبني ..." / "ومبروك، كذا سويت لك ... بيدك"; see kit/series/sample_gulf_a_lines_ar_sa.txt) and add the
  kit name to `ar_alt.kits` in voices.yml; even builds stay Egyptian. Run tools/check_ar_voice.py as usual.
  Saudi script style: real everyday Najdi/Hejazi-leaning white dialect, never Egyptian or formal Arabic words (use
  "وش، ليش، كذا، الحين، مرة، يبي، ما عاد، طيب"; not "إيه، ده، دلوقتي"). Short spoken sentences, no stiff written forms,
  numbers as spoken words, the same 13 lines and fact checks as the English. Write each line to be read aloud by one
  calm Saudi narrator at about 2.2 words a second; keep qaf natural. Check with tools/check_ar_voice.py and fix any
  line over 10% before producing.
- YouTube (owner, Nov 21 16:10 PT, once uploads through YouTube Studio worked: "let's keep buffer then for IG and TK"):
  Buffer posts ONLY Instagram and TikTok. EVERY build goes to YouTube Shorts in both languages through YouTube Studio in
  the owner's Chrome, scheduled there for the build's own slot, so every posts file carries
  `hold: [en.youtube, ar.youtube]`. How: YOUTUBE_STUDIO_UPLOAD.md at the repo root, section "Builds". After the produce
  runs, when the videos are on main and the posts files are written: `python3 scripts/yt_meta.py <slug> <slug> <slug>
  > sheet.json`, push the sheet to the `uploads` branch, then per language switch Studio to the channel and run the
  guide's two calls per video. Each answer must say "Your video will be set to public on <TOMORROW> at <the slot>".
  Switch Studio back to the channel you found, close your tab, empty the `uploads` branch. YouTube itself allowed
  about 10 uploads per channel per 24 hours on Nov 10-12; six builds plus the show's two is 8.
  FALLBACK, for that run only: if the browser cannot be reached (no Claude in Chrome tools in your session, no browser
  connected, a refused call, a sign-in or verification page), post YouTube through Buffer the old way: the 2 strongest
  builds of the PT day per channel (Buffer's free plan sends 2 YouTube posts per channel in any rolling 24 hours and
  counts failed ones: check with cmd=limits, never a third), `hold` on the rest, and say in your message that Studio
  was out of reach. Never type a password or a code.
- Captions (owner, Nov 19 21:18 PT): config.yml cta now ends English Instagram + TikTok and Arabic Instagram captions with
  "Follow us on YouTube ... @congratsengineer / @kef.tenbeni". It is added by post.py; do not write it into `text:`.
  Arabic TikTok is left out on purpose (spam refusals). Money plan and platform rules: project doc
  claude/build-it-money-plan.md (read it before changing pace or platforms).
- The 4-minute show, daily in both languages (owner, Nov 21: "we can keep the tk and ig short and YouTube 4 mins", then
  14:08 PT: "daily 4 mins videos for yt 'ar & en' plus the min short", "the one you post on ig and tk post it on yt
  shorts too"). It has its own daily task ("Build-It 4-minute show") and its own guide, kit/show/README.md; the two
  build runs do not make it. What the build runs must know: its files are posts/sm*.yml + media/sm*-en.mp4 /
  media/sm*-ar.mp4 (the 1-2 minute cuts for TikTok + Instagram). Leave them alone: retire a media/sm* file only when
  its TikTok and Instagram posts are all sent, and never take a YouTube target of a posts/sm*.yml off hold (its full
  video and its Short go up in YouTube Studio, not through Buffer, so the show uses none of Buffer's two YouTube posts
  per 24 hours). Its TikTok and Instagram posts do count toward Buffer's 10 queued posts per channel.
- Entries marked "idea" are proposals: check them with a web search before writing; replace one only if it is not
  promised yet and the facts do not hold up.

## Upcoming
40. the Panama Canal locks (promised by 39) (taken: midday run of 2026-11-18)
41. the Dutch storm surge barrier, Maeslantkering (taken: midday run of 2026-11-18)
42. Venice built on wooden piles (taken: midday run of 2026-11-18)
43. the Great Wall of China (taken: evening run of 2026-11-18)
44. an Omani falaj water channel (taken: evening run of 2026-11-18)
45. Machu Picchu's terraces (taken: evening run of 2026-11-18)
46. the Aswan High Dam (taken: midday run of 2026-11-19)
47. an igloo (taken: midday run of 2026-11-19)
48. a Moroccan riad with its courtyard (taken: midday run of 2026-11-19)
49. the Hagia Sophia dome (taken: evening run of 2026-11-19)
50. a Korean ondol heated floor (taken: evening run of 2026-11-19)
51. the Burj Al Arab on its island (taken: evening run of 2026-11-19)
52. the Palm Jumeirah, an island shaped like a palm tree (Dubai) (promised by 51) (taken: midday run of 2026-11-20)
53. idea: a refrigerator (taken: midday run of 2026-11-20)
54. idea: the Eiffel Tower (taken: midday run of 2026-11-20)
55. idea: the Suez Canal (taken: evening run of 2026-11-20)
56. idea: an escalator (taken: evening run of 2026-11-20)
57. idea: the Sydney Opera House shells (taken: evening run of 2026-11-20)
58. idea: a giant Ferris wheel (Ain Dubai / the London Eye) (taken: midday run of 2026-11-21)
59. idea: the Statue of Liberty (a copper skin on an iron frame) (taken: midday run of 2026-11-21)
60. idea: a microwave oven (taken: midday run of 2026-11-21)
61. idea: the Leaning Tower of Pisa (why it leans and still stands)
62. idea: a Bedouin goat-hair tent (bait al-sha'ar) that keeps out rain and sun
63. idea: a washing machine
64. idea: Big Ben's clock (old pennies on the pendulum keep it on time)
65. idea: Shibam in Yemen, the mud-brick skyscraper city
66. idea: London's Tower Bridge that lifts its road
67. idea: the Colosseum (its giant sun awning and the trapdoor lifts under the arena)
68. idea: Taipei 101's giant swinging damper ball
69. idea: a dishwasher
70. idea: the Louvre Abu Dhabi's dome, a "rain of light" over a museum on the sea
71. idea: a vacuum cleaner
72. idea: the Petronas Twin Towers and the sky bridge that slides as they sway (Kuala Lumpur)
