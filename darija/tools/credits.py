#!/usr/bin/env python3
"""How many ElevenLabs credits the account has left this month. Costs no credits.
The key is read from ELEVENLABS_API_KEY and never printed or written. Writes <out_dir>/credits.json with the plan
name, the monthly allowance, what is used, what is left and the day the count starts again. Nothing else from the
account is saved.   usage: python -I darija/tools/credits.py <out_dir>"""
import json
import os
import sys
import time

import requests

out = sys.argv[1]
key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
res = {"checked": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
if not key:
    res["error"] = "the ELEVENLABS_API_KEY secret is not set"
else:
    try:
        r = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": key}, timeout=30)
        if r.status_code != 200:
            res["error"] = f"ElevenLabs answered {r.status_code}"
        else:
            s = r.json()
            used, limit = s.get("character_count"), s.get("character_limit")
            res.update({"plan": s.get("tier"), "allowance": limit, "used": used,
                        "left": (limit - used) if isinstance(limit, int) and isinstance(used, int) else None})
            reset = s.get("next_character_count_reset_unix")
            if reset:
                res["starts_again"] = time.strftime("%Y-%m-%d", time.gmtime(reset))
    except requests.RequestException as e:
        res["error"] = type(e).__name__
os.makedirs(out, exist_ok=True)
json.dump(res, open(os.path.join(out, "credits.json"), "w", encoding="utf-8"), indent=1)
print(json.dumps(res))
