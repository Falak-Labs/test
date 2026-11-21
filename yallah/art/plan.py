#!/usr/bin/env python3
"""Print the job's groups as a GitHub Actions output: one parallel runner per group."""
import json, sys
job = json.load(open(sys.argv[1]))
groups = []
for it in job["items"]:
    g = it.get("group", "a")
    if g not in groups:
        groups.append(g)
print("groups=" + json.dumps(groups))
