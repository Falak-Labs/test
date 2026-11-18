"""List ElevenLabs voices that could play a Palestinian / Levantine Arabic teacher (reads the key from ELEVENLABS_API_KEY;
never printed or written). Writes darija/voice/_find/voices.json: the account's own voices and the shared library's Arabic
voices whose accent, locale or description mentions Palestinian, Levantine, Jordanian, Lebanese or Syrian.
Listing costs no credits.   usage: python -I darija/tools/find_voices.py <out_dir>"""
import json, os, re, sys, time
import requests

API = "https://api.elevenlabs.io/v1"
key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
if not key:
    sys.exit("ELEVENLABS_API_KEY is not set")
H = {"xi-api-key": key}
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
rx = re.compile(r"palestin|levant|jordan|lebanes|syria|shami|فلسطين|شامي|ar-ps|ar-jo|ar-lb|ar-sy|ar_ps|ar_jo|ar_lb", re.I)


def get(path, **params):
    for t in range(4):
        r = requests.get(API + path, headers=H, params=params, timeout=60)
        if r.status_code in (429, 500, 502, 503):
            time.sleep(3 * (t + 1)); continue
        if r.status_code in (401, 403):
            sys.exit(f"{path}: refused ({r.status_code}) {r.text[:200].replace(key, '***')}")
        r.raise_for_status()
        return r.json()
    sys.exit(f"{path}: gave up")


res = {"own": [], "shared": [], "notes": []}
try:
    for v in get("/voices", show_legacy="true").get("voices", []):
        res["own"].append({k: v.get(k) for k in ("voice_id", "name", "category", "labels", "description", "preview_url")})
except Exception as e:  # noqa
    res["notes"].append("own voices: " + str(e)[:200].replace(key, "***"))
seen = set()
for gender in ("female", "male", None):
    for page in range(6):
        try:
            p = dict(page_size=100, page=page, language="ar", sort="usage_character_count_1y")
            if gender:
                p["gender"] = gender
            d = get("/shared-voices", **p)
        except Exception as e:  # noqa
            res["notes"].append(f"shared {gender} p{page}: " + str(e)[:200].replace(key, "***")); break
        for v in d.get("voices", []):
            if v["voice_id"] in seen:
                continue
            seen.add(v["voice_id"])
            blob = json.dumps(v, ensure_ascii=False)
            if rx.search(blob):
                res["shared"].append({k: v.get(k) for k in ("voice_id", "public_owner_id", "name", "gender", "age", "accent", "locale", "language", "descriptive", "category", "use_case",
                                                            "description", "preview_url", "usage_character_count_1y", "cloned_by_count", "free_users_allowed")})
        if not d.get("has_more"):
            break
res["checked"] = len(seen)
json.dump(res, open(os.path.join(out, "voices.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("own voices", len(res["own"]), "| shared arabic checked", len(seen), "| levantine matches", len(res["shared"]), "|", res["notes"])
