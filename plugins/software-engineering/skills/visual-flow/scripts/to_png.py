"""Rasterise a visual-flow SVG, for somewhere that will not take SVG.

    python to_png.py diagram.svg [out.png] [--scale 2] [--dark]

Uses headless Edge or Chrome, and nothing else will do: the diagram's
stylesheet leans on CSS custom properties, `color-mix()`, `mix-blend-mode` and
a blur filter, and the standalone rasterisers (cairosvg, rsvg-convert) drop or
mangle all four. A browser engine is the only thing that draws it as drawn.

The PNG is a still. The travelling pulses, the walkthrough and the file links
only exist in the SVG, so keep the SVG wherever the reader can follow it.
"""

import pathlib
import re
import shutil
import subprocess
import sys
import time
import tempfile

BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
NAMES = ["chromium", "chromium-browser", "google-chrome", "chrome", "msedge"]


def find_browser():
    for name in NAMES:
        found = shutil.which(name)
        if found:
            return found
    for path in BROWSERS:
        if pathlib.Path(path).exists():
            return path
    sys.exit("no Chrome or Edge found; one of them does the rasterising")


def to_png(svg_path, out_path, scale=2, dark=False):
    svg_path = pathlib.Path(svg_path).resolve()
    text = svg_path.read_text(encoding="utf-8")
    box = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', text)
    if not box:
        sys.exit(f"{svg_path.name} has no viewBox to size the render from")
    width, height = (round(float(box.group(1))), round(float(box.group(2))))

    out = pathlib.Path(out_path).resolve()
    if out.exists():
        out.unlink()

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        source = svg_path
        if dark:
            # The stylesheet already honours :root[data-theme="dark"], and when
            # the SVG is the document its root is the svg element.
            source = pathlib.Path(tmp) / svg_path.name
            source.write_text(text.replace("<svg class=\"flow\"",
                                           "<svg class=\"flow\" data-theme=\"dark\"", 1),
                              encoding="utf-8")
        cmd = [
            find_browser(), "--headless=new", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", f"--force-device-scale-factor={scale}",
            f"--window-size={width},{height}",
            # Its own profile: pointed at the default one, a browser already
            # running hands the job to that instance and exits having drawn
            # nothing.
            f"--user-data-dir={pathlib.Path(tmp) / 'profile'}",
            f"--screenshot={out}",
            source.as_uri(),
        ]
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        # msedge.exe hands the work to a child and returns at once, so the
        # command finishing says nothing about the file existing yet. Wait for
        # it to appear and stop growing.
        size, settled, deadline = -1, 0, time.monotonic() + 120
        while time.monotonic() < deadline:
            now = out.stat().st_size if out.exists() else -1
            settled = settled + 1 if now == size and now > 0 else 0
            if settled >= 3:
                break
            size = now
            time.sleep(0.3)

    if not out.exists() or out.stat().st_size == 0:
        detail = (done.stderr or done.stdout or "").strip()[-500:]
        sys.exit(f"the browser drew nothing for {svg_path.name}. "
                 f"rc={done.returncode} {detail}")
    print(f"{out} {width * scale}x{height * scale} "
          f"({out.stat().st_size // 1024}KB){' dark' if dark else ''}")


if __name__ == "__main__":
    args = sys.argv[1:]
    scale, dark = 2, False
    if "--dark" in args:
        args.remove("--dark")
        dark = True
    if "--scale" in args:
        i = args.index("--scale")
        scale = float(args[i + 1])
        del args[i:i + 2]
    if not 1 <= len(args) <= 2:
        sys.exit(__doc__)
    src = pathlib.Path(args[0])
    to_png(src, args[1] if len(args) == 2 else src.with_suffix(".png"), scale, dark)
