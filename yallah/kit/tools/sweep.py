"""sweep.py <page_dir>: call renderFrame for every frame (no screenshots) and report any exception; also time it."""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(args=["--disable-dev-shm-usage"]); page = b.new_page(viewport={"width": 1080, "height": 1920})
    logs = []
    page.on("console", lambda m: logs.append(f"[{m.type}] {m.text}")); page.on("pageerror", lambda e: logs.append(f"[pageerror] {e}"))
    page.goto((Path(sys.argv[1]) / "index.html").resolve().as_uri())
    page.evaluate("async () => { await document.fonts.ready; await window.RENDER_READY; }")
    t0 = time.monotonic()
    res = page.evaluate("""() => { const n = Math.round(window.RENDER_DURATION * 30), bad = []; let nan = 0;
      for (let i = 0; i < n; i++) { try { window.renderFrame(i / 30); } catch (e) { if (bad.length < 12) bad.push(i + ': ' + e.message); } }
      document.querySelectorAll('[transform]').forEach(e => { if (/NaN|undefined|Infinity/.test(e.getAttribute('transform'))) nan++; });
      return { n, bad, nan, ready: window.READY_OK }; }""")
    print(res, f"{time.monotonic() - t0:.1f}s"); print("\n".join(logs[:20]))
    b.close()
