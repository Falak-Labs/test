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
- YouTube (owner decided Nov 19 21:13 PT, option 1): Buffer sends only 2 YouTube posts a day per channel and counts failed
  ones, so of each PT day's 6 builds only the 2 strongest get YouTube (English and Arabic of the same builds); the other
  4 posts files carry `hold: [en.youtube, ar.youtube]`. Strongest = famous mega-structures and everyday things, the
  kinds that do best on Instagram and TikTok (claude/build-it-performance.md). Never put a third YouTube post on a PT day,
  and never requeue a failed YouTube post onto a day that already has two (cmd=limits). YouTube is the lowest priority.
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
52. the Palm Jumeirah, an island shaped like a palm tree (Dubai) (promised by 51)
53. idea: a refrigerator
54. idea: the Eiffel Tower
55. idea: the Suez Canal
56. idea: an escalator
57. idea: the Sydney Opera House shells
58. idea: a giant Ferris wheel (Ain Dubai / the London Eye)
59. idea: the Statue of Liberty (a copper skin on an iron frame)
60. idea: a microwave oven
61. idea: the Leaning Tower of Pisa (why it leans and still stands)
62. idea: a Bedouin goat-hair tent (bait al-sha'ar) that keeps out rain and sun
63. idea: a washing machine
