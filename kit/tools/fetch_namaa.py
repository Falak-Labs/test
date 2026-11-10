"""Download the free Saudi Arabic voice model (NAMAA Saudi TTS, MIT license), shrink it to half size,
and pack it in parts small enough to attach in the chat. Standard library only:
    python3 fetch_namaa.py
Then attach every file named namaa_saudi.zip.001, .002, ... (about 6 files of 300 MB: a 450 MB part was
too big to attach in the chat, 328 MB went through).
"""
import json
import os
import struct
import time
import urllib.request
import zipfile

OUT = "namaa-saudi"
FILES = [
    ("NAMAA-Space/NAMAA-Saudi-TTS", "t3_mtl23ls_v2.safetensors"),
    ("NAMAA-Space/NAMAA-Saudi-TTS", "s3gen.safetensors"),
    ("NAMAA-Space/NAMAA-Saudi-TTS", "ve.safetensors"),
    ("NAMAA-Space/NAMAA-Saudi-TTS", "conds.pt"),
    ("NAMAA-Space/NAMAA-Saudi-TTS", "mtl_tokenizer.json"),
    ("NAMAA-Space/NAMAA-Saudi-TTS", "tokenizer.json"),
    ("NAMAA-Space/NAMAA-Saudi-TTS", "README.md"),
    ("ResembleAI/chatterbox", "grapheme_mtl_merged_expanded_v1.json"),
]
SHRINK = {"t3_mtl23ls_v2.safetensors", "s3gen.safetensors"}   # float32 -> bfloat16 (half the size)
PART = 300 * 1024 * 1024


def fetch(url, dest, tries=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "namaa-fetch/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                total = int(r.headers.get("Content-Length") or 0)
                done = 0
                with open(dest + ".part", "wb") as fh:
                    while True:
                        chunk = r.read(1 << 20)
                        if not chunk:
                            break
                        fh.write(chunk)
                        done += len(chunk)
                        if total > 5 << 20:
                            print(f"\r   {done / 1e6:8.1f} / {total / 1e6:.1f} MB", end="", flush=True)
                if total and done != total:
                    raise IOError(f"short read {done}/{total}")
            os.replace(dest + ".part", dest)
            if total > 5 << 20:
                print()
            return
        except Exception as e:
            print("\n   retry", i + 1, "->", e)
            time.sleep(3 * (i + 1))
    raise SystemExit("Gave up on " + url)


def to_bf16(src, dst):
    """Rewrite a safetensors file with every F32 tensor as BF16 (keep the top 16 bits of each float)."""
    with open(src, "rb") as fh:
        n = struct.unpack("<Q", fh.read(8))[0]
        header = json.loads(fh.read(n))
        data = fh.read()
    out_header, chunks, off = {}, [], 0
    for name, info in header.items():
        if name == "__metadata__":
            out_header[name] = info
            continue
        a, b = info["data_offsets"]
        raw = memoryview(data)[a:b]
        if info["dtype"] == "F32":
            raw = raw.cast("H")[1::2].tobytes()   # little-endian: second uint16 of each float32 is its top half
            dtype = "BF16"
        else:
            raw = raw.tobytes()
            dtype = info["dtype"]
        out_header[name] = {"dtype": dtype, "shape": info["shape"], "data_offsets": [off, off + len(raw)]}
        chunks.append(raw)
        off += len(raw)
    hb = json.dumps(out_header, separators=(",", ":")).encode()
    hb += b" " * (-len(hb) % 8)
    with open(dst, "wb") as fh:
        fh.write(struct.pack("<Q", len(hb)))
        fh.write(hb)
        for ch in chunks:
            fh.write(ch)


os.makedirs(OUT, exist_ok=True)
for repo, f in FILES:
    final = os.path.join(OUT, f.replace(".safetensors", ".bf16.safetensors") if f in SHRINK else f)
    if os.path.exists(final):
        continue
    dl = os.path.join(OUT, f)
    print("downloading", f)
    fetch(f"https://huggingface.co/{repo}/resolve/main/{f}", dl)
    if f in SHRINK:
        print("   halving", f)
        to_bf16(dl, final)
        os.remove(dl)

print("packing ...")
with zipfile.ZipFile("namaa_saudi.zip", "w", zipfile.ZIP_STORED) as z:
    for name in sorted(os.listdir(OUT)):
        z.write(os.path.join(OUT, name))
size = os.path.getsize("namaa_saudi.zip")
with open("namaa_saudi.zip", "rb") as fh:
    i = 0
    while True:
        chunk = fh.read(PART)
        if not chunk:
            break
        i += 1
        with open(f"namaa_saudi.zip.{i:03d}", "wb") as out:
            out.write(chunk)
os.remove("namaa_saudi.zip")
print(f"done: {i} parts (namaa_saudi.zip.001 ... .{i:03d}), {size / 1e6:.0f} MB in total. Attach all of them.")
