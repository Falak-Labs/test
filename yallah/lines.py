#!/usr/bin/env python3
"""Yallah Say: the voice scripts of one lesson, and what recording them will cost.

usage: python3 yallah/lines.py <lesson> [--write]

Splits the lesson's voice lines by where they are recorded (see kit/tools/gen2.py) into the scripts the workflow
"Darija lesson voice" records, one run per script:
  darija/lines/ma<lesson>.txt, pa<lesson>.txt   the lines of this lesson in each dialect
  darija/lines/kids<lesson>.txt                 the pupils' English lines both dialects share
  darija/lines/macommon.txt, pacommon.txt       the teacher's lines that never change (recorded once)
  darija/lines/kidscommon.txt                   "See you next time!" and "Bye!" (recorded once)
Without --write nothing is saved. Either way it prints, per script, how many characters are not recorded yet:
a line counts when its take is missing in darija/voice/ or was recorded from other words. One character is about
one ElevenLabs credit, so the last line is what the lesson will cost."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "kit", "tools"))
import gen2  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 1:
    sys.exit(__doc__)
NN, write = args[0], "--write" in sys.argv
EP = gen2.lesson(NN)
word = EP["word"]["full"]
g = {loc: gen2.groups(NN, loc) for loc in ("ma", "pa")}
assert g["ma"]["kids"] == g["pa"]["kids"], "the pupils' shared lines differ between the dialects"

scripts = []        # (script name, title line, rows)
for loc in ("ma", "pa"):
    scripts.append((f"{loc}{NN}", f"# Yallah Say, episode {NN} ({loc}): five phrases, quiz, hard word ({word}) in a sentence.", g[loc]["own"]))
if g["ma"]["kids"]:
    scripts.append((f"kids{NN}", f"# Yallah Say, episode {NN}: the pupils' English lines that both dialects share (hard word: {word}).", g["ma"]["kids"]))
if not EP.get("own_lines"):
    for loc in ("ma", "pa"):
        scripts.append((f"{loc}common", f"# Yallah Say ({loc}): the teacher's lines that never change. Recorded once, used by every lesson.", gen2.common(loc)))
    scripts.append(("kidscommon", "# Yallah Say: the pupils' goodbye. Recorded once, used by every lesson in both dialects.", gen2.KIDSCOMMON))

total = 0
for name, title, rows in scripts:
    todo = 0
    for sp, tid, text in rows:
        j = os.path.join(ROOT, "darija", "voice", name, tid + ".json")
        if not (os.path.exists(j) and os.path.exists(j[:-5] + ".mp3") and json.load(open(j, encoding="utf-8")).get("text") == text):
            todo += len(text)
    total += todo
    path = os.path.join(ROOT, "darija", "lines", name + ".txt")
    text = gen2.lines_text(title, rows)
    state = "same as saved" if os.path.exists(path) and open(path, encoding="utf-8").read() == text else ("saved" if write else "not saved")
    if write and state == "saved":
        open(path, "w", encoding="utf-8").write(text)
    print(f"{name:11s} {len(rows):3d} lines, {sum(len(r[2]) for r in rows):4d} characters, {todo:4d} to record   ({state})")
print(f"lesson {NN} ({word}): {total} characters to record")
