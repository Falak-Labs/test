#!/usr/bin/env python3
"""Builds the show can still use, grouped by their Arabic narrator (an episode needs four from ONE group).
    python3 show/stock.py
A build is out once a spec in show/specs/ lists it. Look-1 builds (Episodes 1-5) do not fit the game layer, and neither
do the Seedance builds (look: sd) until build_show.py learns to cut them (it reads kit/episodes/<kit>.py)."""
import glob
import os
import re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
eps = yaml.safe_load(open(os.path.join(ROOT, "episodes.yml"), encoding="utf-8"))["episodes"]
alt = set(yaml.safe_load(open(os.path.join(ROOT, "voices.yml"), encoding="utf-8"))["ar_alt"]["kits"])
used = {}
for p in sorted(glob.glob(os.path.join(HERE, "specs", "*.yml"))):
    for lv in yaml.safe_load(open(p, encoding="utf-8"))["levels"]:
        used[lv["kit"]] = os.path.basename(p)[:-4]
groups = {}
for e in eps:
    kit = e["kit"]
    m = re.search(r"^ep(\d+)-|-b(\d+)$", e["slug"])           # ep67-colosseum, or airfryer-b78 (the main chat's builds)
    if not m or e.get("look") != 2 or kit in used:            # look 1 and the Seedance builds (look: sd) have no
        continue                                              # kit/episodes/<kit>.py scene for build_show.py to cut
    n = int(m.group(1) or m.group(2))
    if not os.path.exists(os.path.join(ROOT, "kit/series/voice", kit + "_ar_sa.json")):
        continue                                          # its Arabic is not made yet
    g = ("Saudi, Mansour (ElevenLabs ar_alt)" if kit in alt or n >= 64 else "Egyptian (ElevenLabs ar)" if n >= 24 else
         "builds 21-23 (their own ElevenLabs voices: check before mixing)" if n >= 21 else
         "Saudi, NAMAA (builds 6-20; give the show's own lines to Mansour)")
    groups.setdefault(g, []).append(f"{n} {kit}")
print(f"used: {', '.join(f'{k} ({v})' for k, v in used.items())}\n")
for g, kits in groups.items():
    print(f"{g}: {len(kits)} builds = {len(kits) // 4} episodes\n  " + ", ".join(kits))
