#!/usr/bin/env python3
"""Render and configure Claude Code usage-battery meters."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

METERS = ("session", "weekly", "fable")
LABELS = {"session": "S", "weekly": "W", "fable": "F"}
CELLS = 6
GREEN_REMAINING = 50
AMBER_REMAINING = 20

GREEN = "\033[38;5;114m"
AMBER = "\033[38;5;214m"
RED = "\033[38;5;167m"
CREAM = "\033[38;5;223m"
CHARCOAL = "\033[38;5;240m"
DIM = "\033[38;5;236m"
RESET = "\033[0m"

HTML_GREEN = "#4ADE80"
HTML_AMBER = "#FBBF24"
HTML_RED = "#EF4444"
HTML_CREAM = "#E8DCC8"
HTML_OUTLINE = "#6B6560"
HTML_LOW_OUTLINE = "#C45C4A"


def home_dir() -> Path:
    raw = os.environ.get("USAGE_BATTERIES_HOME")
    if raw:
        return Path(raw)
    return Path.home() / ".claude" / "usage-batteries"


def claude_settings_path() -> Path:
    raw = os.environ.get("CLAUDE_CONFIG_HOME")
    if raw:
        return Path(raw) / "settings.json"
    return Path.home() / ".claude" / "settings.json"


def wrapper_path() -> Path:
    return home_dir() / "statusline.sh"


def clamp_percent(value: float) -> int:
    return max(0, min(100, int(round(value))))


def remaining_from_used(used: float) -> int:
    return clamp_percent(100 - used)


def color_for(remaining: int) -> str:
    if remaining >= GREEN_REMAINING:
        return GREEN
    if remaining >= AMBER_REMAINING:
        return AMBER
    return RED


def html_color_for(remaining: int) -> str:
    if remaining >= GREEN_REMAINING:
        return HTML_GREEN
    if remaining >= AMBER_REMAINING:
        return HTML_AMBER
    return HTML_RED


def parse_used(value: object) -> float | None:
    if value is None or value is False:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if not text or text.lower() in {"null", "none", "empty"}:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


def used_from_window(window: object) -> float | None:
    if window is None:
        return None
    if isinstance(window, (int, float, str)):
        return parse_used(window)
    if not isinstance(window, dict):
        return None
    for key in ("used_percentage", "used", "utilization", "percent"):
        used = parse_used(window.get(key))
        if used is not None:
            return used
    remaining = parse_used(window.get("remaining_percentage") or window.get("remaining"))
    if remaining is not None:
        return 100 - remaining
    return None


def looks_like_fable(value: object) -> bool:
    if isinstance(value, str):
        return "fable" in value.lower()
    if isinstance(value, dict):
        parts = [
            value.get("display_name"),
            value.get("name"),
            value.get("id"),
            value.get("model"),
            value.get("kind"),
        ]
        scope = value.get("scope")
        if isinstance(scope, dict):
            model = scope.get("model")
            if isinstance(model, dict):
                parts.extend([model.get("display_name"), model.get("id"), model.get("name")])
            else:
                parts.append(model)
            parts.append(scope.get("display_name"))
        return any(looks_like_fable(part) for part in parts if part is not None)
    return False


def fable_from_mapping(mapping: dict) -> float | None:
    for key, value in mapping.items():
        if looks_like_fable(key) or looks_like_fable(value):
            used = used_from_window(value)
            if used is not None:
                return used
        if isinstance(value, dict):
            nested = fable_from_mapping(value)
            if nested is not None:
                return nested
        if isinstance(value, list):
            nested = fable_from_list(value)
            if nested is not None:
                return nested
    return None


def fable_from_list(items: list) -> float | None:
    for item in items:
        if looks_like_fable(item):
            used = used_from_window(item)
            if used is not None:
                return used
        if isinstance(item, dict):
            nested = fable_from_mapping(item)
            if nested is not None:
                return nested
    return None


def fable_from_cache() -> float | None:
    path = home_dir() / "fable-used"
    if not path.is_file():
        return None
    try:
        return parse_used(path.read_text(encoding="utf-8").splitlines()[0])
    except (OSError, IndexError):
        return None


def extract_used(payload: dict) -> dict[str, float]:
    limits = payload.get("rate_limits")
    if not isinstance(limits, dict):
        limits = {}
    found: dict[str, float] = {}
    session = used_from_window(limits.get("five_hour") or limits.get("session"))
    weekly = used_from_window(limits.get("seven_day") or limits.get("weekly"))
    if session is not None:
        found["session"] = session
    if weekly is not None:
        found["weekly"] = weekly
    fable = None
    for key in ("fable", "seven_day_fable", "weekly_fable"):
        fable = used_from_window(limits.get(key))
        if fable is not None:
            break
    if fable is None:
        fable = fable_from_mapping(limits)
    if fable is None:
        extra = payload.get("usage") or payload.get("limits")
        if isinstance(extra, dict):
            fable = fable_from_mapping(extra)
        elif isinstance(extra, list):
            fable = fable_from_list(extra)
    if fable is None:
        fable = fable_from_cache()
    if fable is not None:
        found["fable"] = fable
    return found


def meter_enabled(name: str) -> bool:
    if name == "labels":
        return not (home_dir() / "labels-off").is_file()
    return not (home_dir() / f"{name}-off").is_file()


def set_meter(name: str, enabled: bool) -> None:
    path = home_dir() / ("labels-off" if name == "labels" else f"{name}-off")
    path.parent.mkdir(parents=True, exist_ok=True)
    if enabled:
        if path.exists():
            path.unlink()
        return
    path.write_text("", encoding="utf-8")


def visible_meters(used: dict[str, float]) -> list[tuple[str, int]]:
    visible = []
    for name in METERS:
        if name not in used or not meter_enabled(name):
            continue
        visible.append((name, remaining_from_used(used[name])))
    return visible


def draw_battery(remaining: int) -> str:
    filled = int(round(remaining / 100 * CELLS))
    filled = max(0, min(CELLS, filled))
    color = color_for(remaining)
    outline = RED if remaining < AMBER_REMAINING else CHARCOAL
    fill = color + ("█" * filled)
    empty = DIM + ("░" * (CELLS - filled))
    return f"{outline}[{RESET}{fill}{empty}{RESET}{outline}]▏{RESET}"


def draw_meter(name: str, remaining: int, labels: bool) -> str:
    cell = draw_battery(remaining)
    if not labels:
        return cell
    return f"{CREAM}{LABELS[name]}{RESET} {cell}"


def render_line(payload: dict) -> str:
    meters = visible_meters(extract_used(payload))
    if not meters:
        return ""
    labels = meter_enabled("labels")
    return "  ".join(draw_meter(name, remaining, labels) for name, remaining in meters)


def strip_ansi(text: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(text):
        if text[i] == "\033" and i + 1 < len(text) and text[i + 1] == "[":
            i += 2
            while i < len(text) and text[i] != "m":
                i += 1
            i += 1
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def load_json_stdin() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def cmd_render() -> int:
    sys.stdout.write(render_line(load_json_stdin()))
    if sys.stdout.isatty():
        sys.stdout.write("\n")
    return 0


def cmd_set(name: str, enabled: bool) -> int:
    if name not in METERS and name != "labels":
        print(f"unknown meter: {name}", file=sys.stderr)
        return 2
    set_meter(name, enabled)
    state = "on" if enabled else "off"
    if name == "labels":
        print(f"Usage battery labels are {state}.")
        return 0
    print(f"Usage battery {name} is {state}.")
    return 0


def load_settings(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def owned_status_line(command: object) -> bool:
    if not isinstance(command, str):
        return False
    marker = str(wrapper_path())
    return marker in command or "usage-batteries" in command


def write_wrapper(plugin_scripts: Path) -> None:
    dest = wrapper_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    renderer = plugin_scripts / "usage_batteries.py"
    dest.write_text(
        "#!/bin/sh\n"
        f'exec python3 "{renderer}" render\n',
        encoding="utf-8",
    )
    dest.chmod(0o755)


def write_settings(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def cmd_install(force: bool = False, remove: bool = False) -> int:
    settings_path = claude_settings_path()
    data = load_settings(settings_path)
    current = data.get("statusLine")
    command = current.get("command") if isinstance(current, dict) else None
    if remove:
        if current is None or owned_status_line(command):
            data.pop("statusLine", None)
            write_settings(settings_path, data)
            wrapper = wrapper_path()
            if wrapper.exists():
                wrapper.unlink()
            print("Usage batteries status line removed.")
            return 0
        print("A different status line is configured; left it in place.", file=sys.stderr)
        return 2
    plugin_scripts = Path(__file__).resolve().parent
    write_wrapper(plugin_scripts)
    wrapper = wrapper_path()
    block = {
        "type": "command",
        "command": str(wrapper),
        "padding": 0,
    }
    if current is None or owned_status_line(command) or force:
        data["statusLine"] = block
        write_settings(settings_path, data)
        print("Usage batteries status line is on.")
        return 0
    print("A different status line is configured; left it in place.")
    return 0


def html_battery(remaining: int) -> str:
    width = max(0, min(100, remaining))
    fill = html_color_for(remaining)
    outline = HTML_LOW_OUTLINE if remaining < AMBER_REMAINING else HTML_OUTLINE
    return (
        f'<span class="cell-wrap">'
        f'<span class="cell" style="border-color:{outline}">'
        f'<span class="fill" style="width:{width}%;background:{fill}"></span>'
        f"</span>"
        f'<span class="nub" style="background:{outline}"></span>'
        f"</span>"
    )


def html_cluster(used: dict[str, float], labels: bool | None = None) -> str:
    if labels is None:
        labels = meter_enabled("labels")
    parts = []
    for name, remaining in visible_meters(used):
        badge = f'<span class="letter">{LABELS[name]}</span>' if labels else ""
        parts.append(f'<span class="meter">{badge}{html_battery(remaining)}</span>')
    return f'<div class="cluster">{"".join(parts)}</div>'


def preview_html() -> str:
    samples = [
        ({"session": 20, "weekly": 55, "fable": 92}, "3 meters"),
        ({"session": 20, "weekly": 55}, "2 meters"),
        ({"session": 20}, "1 meter"),
    ]
    rows = []
    for used, title in samples:
        rows.append(
            f'<div class="row"><span class="caption">{title}</span>'
            f"{html_cluster(used, labels=True)}</div>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>B1 Bare cells</title>
  <style>
    html, body {{
      margin: 0;
      background: #0b0b0b;
      color: {HTML_CREAM};
      font: 14px/1.4 ui-sans-serif, system-ui, sans-serif;
    }}
    main {{ max-width: 980px; margin: 36px auto; padding: 0 28px 48px; }}
    h1 {{ font-weight: 500; font-size: 18px; color: {HTML_CREAM}; }}
    h1::before {{ content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #E07A5F; margin-right: 10px; vertical-align: 1px; }}
    .modes {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
    .card {{
      background: #141414;
      border-radius: 22px;
      min-height: 168px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
    }}
    .ghost {{ height: 8px; background: #2a2a2a; border-radius: 8px; width: 62%; margin-bottom: 8px; }}
    .ghost.short {{ width: 38%; }}
    .input {{
      background: #1c1c1c;
      border-radius: 14px;
      height: 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 14px;
      color: #8a8680;
    }}
    .send {{
      width: 22px; height: 22px; border-radius: 50%;
      background: #E07A5F; color: #1a1714; font-size: 11px;
      display: grid; place-items: center;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 12px;
      color: #8a8680;
      font-size: 12px;
    }}
    .cluster {{ display: flex; gap: 10px; align-items: center; }}
    .meter {{ display: flex; align-items: center; gap: 5px; }}
    .letter {{ color: {HTML_CREAM}; font-size: 11px; width: 10px; text-align: center; }}
    .cell-wrap {{ display: inline-flex; align-items: center; }}
    .cell {{
      width: 28px;
      height: 11px;
      border: 1.5px solid {HTML_OUTLINE};
      border-radius: 3px;
      display: inline-block;
      overflow: hidden;
      background: transparent;
    }}
    .nub {{
      width: 2.5px;
      height: 6px;
      margin-left: 1px;
      border-radius: 0 2px 2px 0;
    }}
    .fill {{
      display: block;
      height: 100%;
      border-radius: 1px 0 0 1px;
    }}
    .stack {{ margin-top: 32px; display: flex; flex-direction: column; gap: 10px; }}
    .stack .cluster {{ transform: scale(2); transform-origin: right center; }}
    .row {{
      background: #141414;
      border-radius: 16px;
      padding: 16px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      min-height: 44px;
    }}
    .caption {{ color: #8a8680; font-size: 12px; margin-bottom: 8px; }}
  </style>
</head>
<body>
  <main>
    <h1>B1 Bare cells</h1>
    <div class="modes">
      <section>
        <div class="caption">Code mode</div>
        <div class="card">
          <div class="ghost"></div>
          <div class="ghost short"></div>
          <div class="input"><span>&gt; |</span><span class="send">↑</span></div>
          <div class="footer"><span>Code</span>{html_cluster({"session": 20, "weekly": 55, "fable": 92}, True)}</div>
        </div>
      </section>
      <section>
        <div class="caption">Chat mode</div>
        <div class="card">
          <div class="ghost"></div>
          <div class="ghost short"></div>
          <div class="input"><span>Reply to Claude</span><span class="send">↑</span></div>
          <div class="footer"><span>Chat</span>{html_cluster({"session": 20, "weekly": 55, "fable": 92}, True)}</div>
        </div>
      </section>
    </div>
    <div class="caption" style="margin-top:28px">Adaptive cluster, shown at 2x</div>
    <div class="stack">{"".join(rows)}</div>
  </main>
</body>
</html>
"""


def cmd_preview(kind: str) -> int:
    payload = {
        "rate_limits": {
            "five_hour": {"used_percentage": 20},
            "seven_day": {"used_percentage": 55},
            "fable": {"used_percentage": 92},
        }
    }
    if kind == "html":
        sys.stdout.write(preview_html())
        return 0
    sys.stdout.write(render_line(payload))
    sys.stdout.write("\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] == "render":
        return cmd_render()
    command = args[0]
    if command in {f"{name}-on" for name in METERS} | {"labels-on"}:
        return cmd_set(command[:-3], True)
    if command in {f"{name}-off" for name in METERS} | {"labels-off"}:
        return cmd_set(command[:-4], False)
    if command == "install":
        return cmd_install(force="--force" in args, remove="--remove" in args)
    if command == "preview":
        return cmd_preview("html" if "html" in args else "ansi")
    print(
        "usage: usage_batteries.py [render|session-on|session-off|weekly-on|"
        "weekly-off|fable-on|fable-off|labels-on|labels-off|install|preview]",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
