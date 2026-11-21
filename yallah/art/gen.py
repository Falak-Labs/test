#!/usr/bin/env python3
"""Free pictures for the Yallah Say lessons, made on a GitHub Actions runner. No paid service and no key.

  gen.py <job.json> <group> <out_dir>

Routes (per item, "route"):
  local         an open model (Apache 2.0 weights) run on the runner's own CPU with stable-diffusion.cpp
  horde         AI Horde, the volunteer GPU network, with its anonymous key
  pollinations  Pollinations' keyless Classic API (small, with their logo: here only to measure it)

An item: {"group","name","prompt","w","h","seed", "steps"?, "ref": [names of earlier items or repo paths]?}
Everything it learns (files chosen, seconds per picture, errors) goes to <out_dir>/log_<group>.txt and
summary_<group>.json, so a run can be judged without the Actions log.
"""
import json, os, re, shutil, subprocess, sys, time, urllib.error, urllib.parse, urllib.request, zipfile
from pathlib import Path

HF = "https://huggingface.co"
UA = "yallah-art-lab/0.1 (github.com/Falak-Labs/test)"
QUANTS = ["Q4_K_M", "Q4_K_S", "Q4_K", "Q4_0", "Q5_K_M", "Q5_K_S", "Q5_0", "Q6_K", "Q8_0"]

def gguf(repo, quants=QUANTS, bad=r"(?i)base"):
    return (repo, [rf"(?i)[-_.]{q}\.gguf$" for q in quants], bad)

MODELS = {
    # FLUX.2 [klein] 4B: Apache 2.0, 4 steps, makes pictures and edits them from reference pictures
    "klein4b": {
        "diffusion": [gguf("leejet/FLUX.2-klein-4B-GGUF"), gguf("unsloth/FLUX.2-klein-4B-GGUF")],
        "llm": [gguf("unsloth/Qwen3-4B-GGUF", bad=r"(?i)instruct|mmproj")],
        "vae": [("Comfy-Org/flux2-klein-4B", [r"split_files/vae/.*\.safetensors$"], None),
                ("Comfy-Org/flux2-dev", [r"split_files/vae/.*\.safetensors$"], None),
                ("black-forest-labs/FLUX.2-klein-4B", [r"^vae/.*\.safetensors$"], None),
                ("black-forest-labs/FLUX.2-dev", [r"(?i)^(flux2[-_]?)?(ae|vae)\.safetensors$"], None),
                ("black-forest-labs/FLUX.2-small-decoder", [r"\.safetensors$"], None)],
        "args": ["--cfg-scale", "1.0", "--sampling-method", "euler"], "steps": 4,
    },
    # Z-Image-Turbo: Apache 2.0, 8 steps, text to picture only
    "zimage": {
        "diffusion": [gguf("leejet/Z-Image-Turbo-GGUF")],
        "llm": [gguf("unsloth/Qwen3-4B-Instruct-2507-GGUF", bad=r"(?i)mmproj"), gguf("unsloth/Qwen3-4B-GGUF", bad=r"(?i)mmproj")],
        "vae": [("Comfy-Org/z_image_turbo", [r"split_files/vae/.*\.safetensors$"], None),
                ("black-forest-labs/FLUX.1-schnell", [r"^ae\.safetensors$"], None)],
        "args": ["--cfg-scale", "1.0"], "steps": 8,
    },
}

LOG = None
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    if LOG:
        with open(LOG, "a") as f:
            f.write(s + "\n")

def http(url, headers=None, data=None, timeout=60, method=None):
    h = {"User-Agent": UA}
    h.update(headers or {})
    req = urllib.request.Request(url, headers=h, data=data, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), dict(r.headers)

def sh(cmd, **kw):
    return subprocess.run(cmd, text=True, capture_output=True, **kw)

# ---------------------------------------------------------------- local route
def hf_pick(cands, what, dest):
    """First candidate file that exists and can be downloaded without an account."""
    for repo, pats, bad in cands:
        try:
            _, body, _ = http(f"{HF}/api/models/{repo}/tree/main?recursive=true&limit=1000")
            files = [f for f in json.loads(body) if f.get("type") == "file"]
        except Exception as e:
            log(f"  {what}: {repo}: cannot list ({e})")
            continue
        names = [f["path"] for f in files]
        log(f"  {what}: {repo}: {len(names)} files: " + ", ".join(n for n in names if n.endswith(('.gguf', '.safetensors', '.sft')))[:900])
        for pat in pats:
            hit = [f for f in files if re.search(pat, f["path"]) and not (bad and re.search(bad, f["path"]))]
            if not hit:
                continue
            f = sorted(hit, key=lambda x: x["path"])[0]
            url = f"{HF}/{repo}/resolve/main/{urllib.parse.quote(f['path'])}"
            # ask for the first byte only: tells a public file (200/206) from one that needs an account (401/403)
            code = sh(["curl", "-sL", "-r", "0-0", "-o", "/dev/null", "-w", "%{http_code}", "-A", UA, url]).stdout.strip()
            if code not in ("200", "206"):
                log(f"  {what}: {repo}/{f['path']}: HTTP {code} (needs an account?), trying the next")
                break
            out = dest / (what + Path(f["path"]).suffix)
            t = time.time()
            r = sh(["curl", "-sL", "--fail", "--retry", "3", "-A", UA, "-o", str(out), url])
            size = out.stat().st_size if out.exists() else 0
            want = (f.get("lfs") or {}).get("size") or 0
            if r.returncode != 0 or size < 1e6 or (want and size != want):
                log(f"  {what}: download failed ({r.returncode}, {size} of {want} bytes)")
                break
            log(f"  {what}: {repo}/{f['path']}  {size/1e9:.2f} GB in {time.time()-t:.0f} s")
            return str(out), f"{repo}/{f['path']}"
    raise SystemExit(f"no usable file for {what}")

def get_sdcpp(dest):
    tok = os.environ.get("GH_TOKEN", "")
    hdr = {"Accept": "application/vnd.github+json"}
    if tok:
        hdr["Authorization"] = "Bearer " + tok
    _, body, _ = http("https://api.github.com/repos/leejet/stable-diffusion.cpp/releases/latest", hdr)
    rel = json.loads(body)
    names = [a["name"] for a in rel["assets"]]
    log("sd.cpp release", rel["tag_name"], "assets:", ", ".join(names))
    cpu = [a for a in rel["assets"] if re.search(r"(?i)linux", a["name"]) and re.search(r"(?i)x86_64|x64|amd64", a["name"])
           and not re.search(r"(?i)vulkan|cuda|rocm|sycl|opencl|musa|hip|metal|arm|aarch", a["name"])]
    if not cpu:
        raise SystemExit("no Linux x86_64 CPU build in the release")
    # the runners are AVX2 machines (no AVX-512 on the AMD ones): take the AVX2 build, else the plain one
    plain = [x for x in cpu if not re.search(r"(?i)avx512|noavx", x["name"])] or cpu
    a = ([x for x in plain if re.search(r"(?i)avx2", x["name"])] or sorted(plain, key=lambda x: len(x["name"])))[0]
    z = dest / a["name"]
    r = sh(["curl", "-sL", "--fail", "--retry", "3", "-o", str(z), a["browser_download_url"]])
    if r.returncode != 0:
        raise SystemExit("sd.cpp download failed")
    with zipfile.ZipFile(z) as zf:
        zf.extractall(dest / "sdcpp")
    exe = None
    for p in sorted((dest / "sdcpp").rglob("*")):
        if p.is_file() and p.name in ("sd-cli", "sd"):
            exe = p
            break
    if not exe:
        raise SystemExit("no sd-cli in " + a["name"] + ": " + ", ".join(str(p) for p in (dest / "sdcpp").rglob("*"))[:600])
    exe.chmod(0o755)
    env = dict(os.environ, LD_LIBRARY_PATH=str(exe.parent) + ":" + os.environ.get("LD_LIBRARY_PATH", ""))
    log("sd.cpp:", a["name"], "->", exe)
    return str(exe), env, rel["tag_name"]

def run_local(items, job, out, summary):
    work = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "art"
    work.mkdir(parents=True, exist_ok=True)
    cpu = sh(["bash", "-c", "lscpu | grep -m1 'Model name' | sed 's/.*: *//'"]).stdout.strip()
    ncpu = os.cpu_count() or 4
    mem = sh(["bash", "-c", "free -g | awk 'NR==2{print $2}'"]).stdout.strip()
    log(f"runner: {cpu}, {ncpu} threads, {mem} GB RAM")
    exe, env, tag = get_sdcpp(work)
    (out / "sdcpp_help.txt").write_text(sh([exe, "--help"], env=env).stdout[:20000])
    loaded = {}
    for it in items:
        mname = it.get("model") or job.get("model") or "klein4b"
        m = MODELS[mname]
        if mname not in loaded:
            log(f"model {mname}:")
            t = time.time()
            loaded[mname] = {k: hf_pick(m[k], f"{mname}_{k}", work) for k in ("diffusion", "llm", "vae")}
            log(f"  weights ready in {time.time()-t:.0f} s")
        files = loaded[mname]
        png = out / (it["name"] + ".png")
        cmd = [exe, "--diffusion-model", files["diffusion"][0], "--llm", files["llm"][0], "--vae", files["vae"][0],
               "-p", it["prompt"], "-W", str(it.get("w", 768)), "-H", str(it.get("h", 768)),
               "--steps", str(it.get("steps", m["steps"])), "-s", str(it.get("seed", 42)),
               "-t", str(ncpu), "-o", str(png), "-v"] + m["args"] + it.get("args", [])
        for ref in it.get("ref", []):
            p = out / (ref + ".png")
            cmd += ["-r", str(p if p.exists() else Path(ref))]
        t = time.time()
        r = sh(cmd, env=env)
        sec = time.time() - t
        text = (r.stdout or "") + (r.stderr or "")
        (out / f"{it['name']}.sdlog.txt").write_text(text[-30000:])
        keep = [l.strip() for l in text.splitlines() if re.search(r"(?i)taking|completed|loading .* took|s/it|it/s|total params|error|fail", l)]
        rec = {"name": it["name"], "route": "local", "model": mname, "w": it.get("w", 768), "h": it.get("h", 768),
               "steps": it.get("steps", m["steps"]), "refs": len(it.get("ref", [])), "seconds": round(sec, 1),
               "ok": r.returncode == 0 and png.exists(), "files": {k: v[1] for k, v in files.items()},
               "cpu": cpu, "threads": ncpu, "sdcpp": tag}
        log(f"{it['name']}: {'ok' if rec['ok'] else 'FAILED ' + str(r.returncode)} in {sec:.0f} s  ({rec['w']}x{rec['h']}, {rec['steps']} steps, {rec['refs']} refs)")
        for l in keep[-14:]:
            log("    " + l[-220:])
        if not rec["ok"]:
            log("    tail: " + " | ".join(text.splitlines()[-8:])[-900:])
        summary.append(rec)

# ---------------------------------------------------------------- AI Horde route
def run_horde(items, out, summary):
    base = "https://aihorde.net/api/v2"
    hdr = {"apikey": "0000000000", "Client-Agent": "yallah-art-lab:0.1:github.com/Falak-Labs/test", "Content-Type": "application/json"}
    try:
        _, body, _ = http(base + "/status/models?type=image", hdr)
        models = sorted(json.loads(body), key=lambda m: -m.get("count", 0))
        log("horde models (workers, queued, eta s): " + "; ".join(f"{m['name']} ({m.get('count')}, {m.get('queued')}, {m.get('eta')})" for m in models[:25]))
    except Exception as e:
        log("horde: cannot list models:", e)
        models = []
    names = {m["name"]: m for m in models if m.get("count", 0) > 0}
    for it in items:
        want = it.get("horde_models") or ["Flux.1-Schnell fp8 (Compact)", "AlbedoBase XL (SDXL)", "Juggernaut XL", "SDXL 1.0", "DreamShaper XL"]
        model = next((w for w in want if w in names), None) or (models[0]["name"] if models else "stable_diffusion")
        flux = "flux" in model.lower()
        params = {"width": it.get("w", 1024), "height": it.get("h", 1024), "n": 1,
                  "steps": 4 if flux else 25, "cfg_scale": 1 if flux else 6.5,
                  "sampler_name": "k_euler" if flux else "k_euler_a", "karras": not flux}
        if "seed" in it:
            params["seed"] = str(it["seed"])
        req = {"prompt": it["prompt"], "params": params, "models": [model], "nsfw": False, "censor_nsfw": True,
               "r2": True, "shared": False, "slow_workers": True, "trusted_workers": False}
        rec = {"name": it["name"], "route": "horde", "model": model, "w": params["width"], "h": params["height"], "ok": False}
        t = time.time()
        try:
            _, body, _ = http(base + "/generate/async", hdr, json.dumps(req).encode(), method="POST")
            jid = json.loads(body)["id"]
            log(f"{it['name']}: horde job {jid} on {model}")
            last = ""
            while time.time() - t < it.get("wait", 1500):
                time.sleep(12)
                _, body, _ = http(f"{base}/generate/check/{jid}", hdr)
                c = json.loads(body)
                s = f"queue {c.get('queue_position')} wait {c.get('wait_time')} s processing {c.get('processing')}"
                if s != last and (time.time() - t) % 60 < 13:
                    log("    " + s)
                last = s
                if c.get("done") or c.get("faulted") or not c.get("is_possible", True):
                    break
            _, body, _ = http(f"{base}/generate/status/{jid}", hdr)
            st = json.loads(body)
            gens = st.get("generations") or []
            if gens:
                img = gens[0]["img"]
                raw = out / (it["name"] + ".webp")
                if img.startswith("http"):
                    _, data, _ = http(img, timeout=120)
                    raw.write_bytes(data)
                else:
                    import base64
                    raw.write_bytes(base64.b64decode(img))
                rec.update(ok=True, worker=gens[0].get("worker_name"), kudos=st.get("kudos"), censored=gens[0].get("censored"))
            else:
                rec["note"] = json.dumps({k: st.get(k) for k in ("done", "faulted", "is_possible", "queue_position", "wait_time")})
        except urllib.error.HTTPError as e:
            rec["note"] = f"HTTP {e.code}: {e.read()[:300].decode('utf-8', 'replace')}"
        except Exception as e:
            rec["note"] = repr(e)[:300]
        rec["seconds"] = round(time.time() - t, 1)
        log(f"{it['name']}: horde {'ok' if rec['ok'] else 'FAILED'} in {rec['seconds']:.0f} s {rec.get('note', '')}")
        summary.append(rec)

# ---------------------------------------------------------------- Pollinations keyless route
def run_pollinations(items, out, summary):
    for it in items:
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(it["prompt"]) + f"?width={it.get('w', 768)}&height={it.get('h', 768)}&seed={it.get('seed', 42)}"
        rec = {"name": it["name"], "route": "pollinations", "ok": False}
        t = time.time()
        try:
            code, data, hd = http(url, timeout=180)
            (out / (it["name"] + ".jpg")).write_bytes(data)
            rec.update(ok=code == 200 and len(data) > 5000, bytes=len(data), type=hd.get("Content-Type"))
        except urllib.error.HTTPError as e:
            rec["note"] = f"HTTP {e.code}, Retry-After {e.headers.get('Retry-After')}: {e.read()[:200].decode('utf-8', 'replace')}"
        except Exception as e:
            rec["note"] = repr(e)[:300]
        rec["seconds"] = round(time.time() - t, 1)
        log(f"{it['name']}: pollinations {'ok' if rec['ok'] else 'FAILED'} in {rec['seconds']:.0f} s {rec.get('note', '')}")
        summary.append(rec)

def main():
    global LOG
    job = json.loads(Path(sys.argv[1]).read_text())
    group, out = sys.argv[2], Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    LOG = out / f"log_{group}.txt"
    items = [i for i in job["items"] if i.get("group", "a") == group]
    summary = []
    by = {}
    for i in items:
        by.setdefault(i.get("route", "local"), []).append(i)
    try:
        if "pollinations" in by:
            run_pollinations(by["pollinations"], out, summary)
        if "horde" in by:
            run_horde(by["horde"], out, summary)
        if "local" in by:
            run_local(by["local"], job, out, summary)
    finally:
        (out / f"summary_{group}.json").write_text(json.dumps(summary, indent=1))
        # a small JPEG beside every picture, for quick looks
        try:
            from PIL import Image
            for p in list(out.glob("*.png")) + list(out.glob("*.webp")):
                Image.open(p).convert("RGB").save(p.with_suffix(".jpg"), quality=90)
        except Exception as e:
            log("jpeg copies skipped:", e)
    bad = [s["name"] for s in summary if not s.get("ok")]
    log("done:", len(summary) - len(bad), "ok,", len(bad), "failed", bad)

if __name__ == "__main__":
    main()
