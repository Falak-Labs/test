# Build-It lineup (shared by the two daily runs)

Two runs a day make three builds each (Nov 17 2026, the owner: "Let's start posting 6 videos a day"):
- **Build-It midday production** (11:23 PT) makes TOMORROW's first three builds.
- **Build-It daily production** (18:37 PT) makes TOMORROW's last three builds.

Rules:
- STYLE (owner, Nov 23 20:32 PT): every new build is a Seedance build, see series/SEEDANCE_STYLE.md. Take the
  lowest-numbered builds whose footage is done in higgsfield/queue.yml; v2 cartoon only when none is ready.
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
- Arabic voice (owner, Nov 22 11:35 PT: "only ElevenLabs for Arabic, not the Egyptian one"; the A/B test of Nov 17 is
  over): for EVERY build from 64 on, write the Arabic script in Saudi dialect (frames: "لو ...، مبروك، كذا سويت لك ..." / "بس قبل لا ...، تابعني،
  لأن الجاي بنبني ..." / "ومبروك، كذا سويت لك ... بيدك"; see kit/series/sample_gulf_a_lines_ar_sa.txt); voices.yml
  `ar` is Mansour already, so add nothing to `ar_alt.kits`. No Egyptian voice or script for anything new. Run
  tools/check_ar_voice.py as usual.
  Saudi script style: real everyday Najdi/Hejazi-leaning white dialect, never Egyptian or formal Arabic words (use
  "وش، ليش، كذا، الحين، مرة، يبي، ما عاد، طيب"; not "إيه، ده، دلوقتي"). Short spoken sentences, no stiff written forms,
  numbers as spoken words, the same 13 lines and fact checks as the English. Write each line to be read aloud by one
  calm Saudi narrator at about 2.2 words a second; keep qaf natural. Check with tools/check_ar_voice.py and fix any
  line over 10% before producing.
- YouTube (owner, Nov 21 16:10 PT: "let's keep buffer then for IG and TK"; rule rewritten Nov 21 21:45 PT after two
  findings). (1) A scheduled run has NO browser, so a run never uploads to YouTube Studio: the main chat does it twice
  a day, about 16:45 and 21:30 PT (YOUTUBE_STUDIO_UPLOAD.md, "The desk"). (2) YouTube limits uploads: about 10 per
  rolling 24 hours for all the owner's unverified channels together, until HE does YouTube's one-time verification
  (he was told on Nov 21). `youtube/desk.yml` says `verified: false` until that is done. While it is false, each run
  ranks its three builds by how strong the topic is (famous places and everyday things first, see
  claude/build-it-performance.md) and posts them like this:
  - Build #1: YouTube through Buffer in both languages, as before Nov 21. Buffer's free plan sends 2 YouTube posts
    per channel in any rolling 24 hours and counts failed ones, so ONE build per run: give it a per-platform
    `at: {default: ..., youtube: ...}` that `tools.yml cmd=limits` and the state files show to be free (the notes of
    the runs of Nov 21 show the arithmetic). Never a third post in a window.
  - Build #2: `hold: [en.youtube, ar.youtube]` plus the top-level line `studio: 1` in its posts file. The main chat
    uploads it in Studio, scheduled at the build's own slot, when the day's limit has room: 6 Studio uploads a day,
    of which the show takes 4, so the midday run's #2 normally fits and the evening run's #2 only on a day the show
    did not come.
  - Build #3: the same hold plus `studio: 2`. It is uploaded only when room is left after that; otherwise it stays
    off YouTube. Do not promise the owner a YouTube upload for a held build: say it waits for room.
  When `youtube/desk.yml` says `verified: true`: all three builds get the hold and `studio: 1`, and no YouTube post
  goes through Buffer any more.
  Step 0 of every run: `python3 scripts/yt_desk.py check`. OVERDUE lines mean the main chat's upload did not happen:
  put them at the top of your message to the owner and do not try to repair it yourself.
  Never type a password or a code, and never click "Verify" on a YouTube page.
- Captions (owner, Nov 19 21:18 PT): config.yml cta now ends English Instagram + TikTok and Arabic Instagram captions with
  "Follow us on YouTube ... @congratsengineer / @kef.tenbeni". It is added by post.py; do not write it into `text:`.
  Arabic TikTok is left out on purpose (spam refusals). Money plan and platform rules: project doc
  claude/build-it-money-plan.md (read it before changing pace or platforms).
- The 4-minute show, daily in both languages (owner, Nov 21: "we can keep the tk and ig short and YouTube 4 mins", then
  14:08 PT: "daily 4 mins videos for yt 'ar & en' plus the min short", "the one you post on ig and tk post it on yt
  shorts too"). It has its own daily task ("Build-It 4-minute show") and its own guide, kit/show/README.md; the two
  build runs do not make it. What the build runs must know: its files are posts/sm*.yml + media/sm*-en.mp4 /
  media/sm*-ar.mp4 (the 1-2 minute cuts for TikTok + Instagram). Leave them alone: retire a media/sm* file only when
  its TikTok and Instagram posts are all sent, and never take ANY target of a posts/sm*.yml off hold: its full
  video and its Short go up in YouTube Studio through the main chat (so the show uses none of Buffer's two YouTube
  posts per 24 hours), and its TikTok and Instagram targets start on hold too, until the main chat has uploaded the
  full video and releases them (`scripts/yt_desk.py release`). Once released, its TikTok and Instagram posts count
  toward Buffer's 10 queued posts per channel, so leave room for two of them in each Arabic and English queue.
- Hook rules (owner's checklist, Nov 23 2026; study in claude/build-it-hook-checklist.md, rules in NIGHT_NOTES "Nov 23
  2026, 13:55 PT"): line 1 keeps the frame but shows ONE picture in at most 18 English words / 13 Arabic words (no comma
  before "congrats" / "مبروك"), the cut fact opens line 2, the first problem is told by 9.5 s (Arabic 10.0 s), line 2
  raises a question only the reveal (line 11) answers, plain words, one fact a line. From the kit folder run
  `python3 -I tools/check_hook.py <kit>` after writing the scripts and again after the voices: no FAIL before you animate.
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
61. idea: the Leaning Tower of Pisa (why it leans and still stands) (taken: evening run of 2026-11-21)
62. idea: a Bedouin goat-hair tent (bait al-sha'ar) that keeps out rain and sun (taken: evening run of 2026-11-21)
63. idea: a washing machine (taken: evening run of 2026-11-21)
64. idea: Big Ben's clock (old pennies on the pendulum keep it on time) (taken: midday run of 2026-11-22)
65. idea: Shibam in Yemen, the mud-brick skyscraper city (taken: midday run of 2026-11-22)
66. idea: London's Tower Bridge that lifts its road (taken: midday run of 2026-11-22)
67. idea: the Colosseum (its giant sun awning and the trapdoor lifts under the arena) (taken: evening run of 2026-11-22)
68. idea: Taipei 101's giant swinging damper ball (taken: evening run of 2026-11-22)
69. idea: a dishwasher (taken: evening run of 2026-11-22)
70. idea: the Louvre Abu Dhabi's dome, a "rain of light" over a museum on the sea (taken: midday run of 2026-11-23)
71. idea: a vacuum cleaner (taken: midday run of 2026-11-23)
72. idea: the Petronas Twin Towers and the sky bridge that slides as they sway (Kuala Lumpur) (taken: midday run of 2026-11-23)
73. idea: the Lighthouse of Alexandria, the Pharos (a fire seen far out at sea; its stones now lie in the harbour and in Qaitbay's fort) (taken: evening run of 2026-11-23)
74. idea: Maraya in AlUla, the world's largest mirrored building (it disappears into the Saudi desert) (taken: evening run of 2026-11-23)
75. idea: India's Chand Baori stepwell (about 3,500 steps down to cool water) (taken: evening run of 2026-11-23)
76. idea: a pressure cooker (taken: midday run of 2026-11-24)
77. idea: the Golden Gate Bridge (its "International Orange" was only the primer, and it was built into the fog and the tides) (taken: midday run of 2026-11-24)
78. idea: an air fryer (a small oven that "fries" with a whirlwind of hot air)
79. idea: the Kuwait Towers, water towers on the Gulf with a revolving deck on top
80. idea: Jeddah's giant sea fountain (King Fahd's Fountain, the tallest fountain in the world: sea water shot higher than most skyscrapers)
81. idea: a zipper (two rows of teeth that a small wedge locks and unlocks; Gideon Sundback, 1913)
82. idea: the Hong Kong-Zhuhai-Macau Bridge (55 km over the sea, diving into an undersea tunnel between two man-made islands)
83. idea: a Thermos flask (tea or Arabic coffee still hot hours later: two walls with a vacuum between them, silvered glass; James Dewar, 1892)
84. idea: the Hoover Dam (poured in one piece its concrete would have taken about 125 years to cool, so it was cast in blocks with cold-water pipes inside)
85. idea: the Dubai Frame (a 150 m picture frame between old and new Dubai, with a glass-floor bridge across the top)
86. idea: an electric kettle that switches itself off (steam runs down a little tube to a two-metal disc that snaps when the water boils and trips the switch: the click) (added by the Higgsfield runner so the Dubai Frame's Seedance clip B can tease it)
87. idea: a hot air balloon (a flame heats the air inside a huge fabric bag, hot air is lighter than cold air, so the whole basket floats up) (added by the Higgsfield runner so the kettle clip B can tease it)
88. idea: the Pont du Gard, the Roman aqueduct bridge in southern France (three tiers of stone arches about 49 m high, laid largely without mortar, carrying spring water across a valley in a channel that drops only 2.5 cm over the bridge; limescale up to 50 cm thick slowly choked it) (added by the Higgsfield runner so the hot air balloon's Seedance clip B can tease it)
89. idea: Noor Ouarzazate in Morocco, the solar plant that keeps making power after dark (about seven thousand mirrors aim sunlight at a 247 m tower that heats molten salt past 500 C; the hot salt waits in giant tanks and runs the turbines about seven hours after sunset) (added by the Higgsfield runner so the Pont du Gard's Seedance clip B can tease it)
90. idea: a ballpoint pen (a tiny steel ball turns in a socket and rolls out thick ink; John Loud's rolling-ball pen of 1888 was "too rough for paper", László Bíró's British patent of 1938 used a thicker ink that dried fast "like newspaper ink"; a tiny hole in the barrel equalizes the air pressure so it won't leak) (added by the Higgsfield runner so the Noor Ouarzazate Seedance clip B can tease it)
91. idea: the Gateway Arch in St. Louis (a 630 ft stainless steel arch built as two separate legs that had to meet in the sky: creeper cranes pulled themselves up the curved legs, a truss braced the legs against each other at 530 ft, and on the last day, Oct 28 1965, a jacking frame pressed the legs apart while firefighters ran cold water on the sun-warmed south leg so the last section would fit) (added by the Higgsfield runner so the ballpoint pen's Seedance clip B can tease it)
92. idea: a car seatbelt that locks only when you need it (a spring winds the belt onto a spool; in a sudden stop a weighted pendulum swings and its pawl catches a toothed ratchet gear on the spool, and a fast tug spins a centrifugal clutch that locks it the same way; Nils Bohlin's three-point belt for Volvo, 1959, which Volvo made free for all car makers) (added by the Higgsfield runner for the Gateway Arch's Seedance clip B to tease; its pair is queued: seatbelt-A/B)
93. idea: the Huajiang Grand Canyon Bridge in Guizhou, China, the world's highest bridge (a suspension bridge whose deck hangs 625 m above the bottom of the gorge on a 1,420 m main span; built from January 2022, opened 28 Sep 2025; a crossing that took about two hours now takes about two minutes per China Daily, 70 minutes to just over one per Wikipedia: check; a glass walkway under the deck, a lift beside a tower and a cafe on top of it) (added by the Higgsfield runner so the seatbelt's Seedance clip B can tease it)
94. idea: a smoke alarm (in an ionization alarm a speck of americium charges the air between two metal plates and smoke carries the charge away so the current drops; a photoelectric one sees smoke scatter a light beam onto its sensor; then the cooking false alarms, and the low-battery chirp that comes at night because a dying battery's resistance rises as the house cools) (added by the Higgsfield runner for the Huajiang bridge's Seedance clip B to tease; its pair is not queued yet)
95. idea: the Falkirk Wheel in Scotland, a giant rotating boat lift (two water-filled gondolas balance each other because a floating boat displaces its own weight of water, so ten hydraulic motors lift boats 24 m between two canals on about 1.5 kWh per half-turn, roughly what boiling eight kettles takes; it replaced a flight of 11 locks that took nearly a day; built in Derbyshire and bolted, not welded; three 8 m ring gears keep the gondolas level as the arms turn; opened 24 May 2002; facts and the figures to check are in higgsfield/ideas.md, Nov 24 10:05) (added by the Higgsfield runner for the smoke alarm's Seedance clip B to tease; its pair is not queued yet)
