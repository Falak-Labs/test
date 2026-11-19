"""List ElevenLabs shared-library English voices that could play a little boy in the lesson videos (key from
ELEVENLABS_API_KEY; never printed or written). Writes <out_dir>/kids.json. Listing costs no credits.
usage: python -I darija/tools/find_kid_voices.py <out_dir>"""
import json, os, re, sys, time
import requests

API = "https://api.elevenlabs.io/v1"
key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
if not key:
    sys.exit("ELEVENLABS_API_KEY is not set")
H = {"xi-api-key": key}
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
KEEP = ("voice_id", "public_owner_id", "name", "gender", "age", "accent", "locale", "language", "descriptive", "category", "use_case",
        "description", "usage_character_count_1y", "cloned_by_count", "free_users_allowed")


def get(path, **params):
    for t in range(4):
        r = requests.get(API + path, headers=H, params=params, timeout=60)
        if r.status_code in (429, 500, 502, 503):
            time.sleep(3 * (t + 1)); continue
        if r.status_code in (401, 403):
            raise RuntimeError(f"{path}: refused ({r.status_code})")
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"{path}: gave up")


res = {"voices": [], "notes": [], "slots": None}
seen = {}
for q in ({"search": "little boy"}, {"search": "kid boy"}, {"search": "child boy"}, {"search": "young boy"}, {"search": "cute boy"}, {"search": "boy child voice"},
          {"search": "kid"}, {"search": "child"}, {"search": "toddler"}, {"search": "schoolboy"}, {"search": "Dylan"}, {"search": "boy", "use_cases": "characters_animation"},
          {"search": "boy", "descriptives": "cute"}, {"search": "child", "gender": "male"}, {"search": "kid", "gender": "male"}):
    for page in range(2):
        try:
            d = get("/shared-voices", page_size=100, page=page, language="en", sort="usage_character_count_1y", **q)
        except Exception as e:  # noqa
            res["notes"].append(f"{q}: " + str(e)[:150].replace(key, "***")); break
        for v in d.get("voices", []):
            if v["voice_id"] not in seen:
                seen[v["voice_id"]] = {k: v.get(k) for k in KEEP}
                seen[v["voice_id"]]["q"] = q.get("search")
        if not d.get("has_more"):
            break
rx = re.compile(r"\b(boy|kid|kiddo|child|children|childlike|childish|toddler|little|schoolboy|year[- ]old|pre-?teen|young son)\b", re.I)
for v in seen.values():
    if rx.search((v.get("name") or "") + " " + (v.get("description") or "")) and (v.get("gender") or "") != "female":
        res["voices"].append(v)
res["voices"].sort(key=lambda v: -(v.get("usage_character_count_1y") or 0))
res["checked"] = len(seen)
try:
    s = get("/user/subscription")
    res["slots"] = {"used": s.get("voice_slots_used"), "limit": s.get("voice_limit")}
except Exception as e:  # noqa
    res["notes"].append("slots: " + str(e)[:120].replace(key, "***"))
json.dump(res, open(os.path.join(out, "kids.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("checked", res["checked"], "kept", len(res["voices"]), "notes", len(res["notes"]))
