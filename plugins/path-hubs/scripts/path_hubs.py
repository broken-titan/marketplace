#!/usr/bin/env python3
"""Group Chat and Code sessions under one hub per git repo path."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


STATE_VERSION = 1
REMOTE_RE = re.compile(
    r"(?:[:/])(?P<org>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?/?$"
)


def now_ts() -> float:
    return datetime.now(timezone.utc).timestamp()


def home_dir() -> Path:
    return Path(os.environ.get("HOME") or str(Path.home()))


def scan_root() -> Path:
    raw = os.environ.get("PATH_HUBS_SCAN_ROOT")
    return Path(raw) if raw else home_dir()


def state_dir() -> Path:
    raw = os.environ.get("PATH_HUBS_HOME")
    if raw:
        return Path(raw)
    return home_dir() / ".claude" / "path-hubs"


def state_path() -> Path:
    return state_dir() / "state.json"


def view_path() -> Path:
    return state_dir() / "view.html"


def empty_state() -> dict[str, Any]:
    return {"version": STATE_VERSION, "autoLink": True, "hubs": {}, "items": {}}


def load_state() -> dict[str, Any]:
    path = state_path()
    if not path.is_file():
        return empty_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return empty_state()
    if not isinstance(data, dict):
        return empty_state()
    data.setdefault("version", STATE_VERSION)
    data.setdefault("autoLink", True)
    data.setdefault("hubs", {})
    data.setdefault("items", {})
    if not isinstance(data["hubs"], dict):
        data["hubs"] = {}
    if not isinstance(data["items"], dict):
        data["items"] = {}
    return data


def save_state(state: dict[str, Any]) -> None:
    dest = state_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def run_git(cwd: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return (result.stdout or "").strip() or None


def expand_path(raw: str | None) -> str:
    if not raw:
        return ""
    return str(Path(os.path.expanduser(raw)).resolve()) if raw.startswith("~") else raw


def display_path(path: str) -> str:
    home = str(home_dir())
    if path == home:
        return "~"
    if path.startswith(home + "/"):
        return "~" + path[len(home) :]
    return path


def normalize_remote(remote: str | None) -> str:
    if not remote:
        return ""
    value = remote.strip()
    match = REMOTE_RE.search(value.rstrip("/"))
    if match:
        return f"{match.group('org')}/{match.group('repo')}"
    parsed = urlparse(value)
    if parsed.path:
        parts = [p for p in parsed.path.split("/") if p and p != "git"]
        if len(parts) >= 2:
            return f"{parts[-2]}/{parts[-1].removesuffix('.git')}"
    return value.removesuffix(".git")


def short_from_path(path: str) -> str:
    parts = [p for p in Path(path).parts if p not in ("/",)]
    if len(parts) >= 2:
        return f"{parts[-2]}/{parts[-1]}"
    return parts[-1] if parts else path


def session_cwd(rows: list[dict[str, Any]], fallback: str) -> str:
    for row in rows:
        for key in ("cwd", "workspace", "workspace_dir"):
            value = row.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        message = row.get("message")
        if isinstance(message, dict):
            value = message.get("cwd")
            if isinstance(value, str) and value.strip():
                return value.strip()
    return fallback


def git_identity(path: str) -> tuple[str, str, str]:
    if not path:
        return "", "", ""
    start = Path(path)
    if start.is_file():
        start = start.parent
    if not start.exists():
        return "", "", short_from_path(path)
    probe = start if start.is_dir() else start.parent
    if not probe.is_dir():
        return "", "", short_from_path(path)
    root = run_git(probe, "rev-parse", "--show-toplevel")
    if not root:
        return "", "", short_from_path(str(probe))
    remote = run_git(Path(root), "remote", "get-url", "origin") or ""
    short = normalize_remote(remote) or short_from_path(root)
    return root, remote, short


def hub_id_for(path: str, remote: str, short: str) -> str:
    return normalize_remote(remote) or short or short_from_path(path)


def ensure_hub(state: dict[str, Any], path: str, remote: str = "", short: str = "") -> dict[str, Any]:
    if not path and not remote:
        raise SystemExit("hub needs a path or remote")
    ident_path, ident_remote, ident_short = git_identity(path) if path else ("", remote, short)
    hub_path = ident_path or path
    hub_remote = ident_remote or remote
    hub_short = short or ident_short or hub_id_for(hub_path, hub_remote, "")
    hub_id = hub_id_for(hub_path, hub_remote, hub_short)
    for existing in state["hubs"].values():
        if existing.get("id") == hub_id:
            if hub_path and not existing.get("path"):
                existing["path"] = hub_path
            if hub_remote and not existing.get("remote"):
                existing["remote"] = hub_remote
            return existing
        if hub_path and existing.get("path") == hub_path:
            return existing
        if hub_remote and normalize_remote(existing.get("remote")) == normalize_remote(hub_remote):
            return existing
    hub = {
        "id": hub_id,
        "shortName": hub_short,
        "path": hub_path,
        "remote": hub_remote,
    }
    state["hubs"][hub_id] = hub
    return hub


def decode_claude_project(name: str) -> str:
    if name.startswith("-"):
        return "/" + name[1:].replace("-", "/")
    return name.replace("-", "/")


def relative_when(ts: float) -> str:
    if not ts:
        return ""
    delta = max(0, int(now_ts() - ts))
    if delta < 12 * 3600:
        return "Today"
    days = delta // 86400
    if days <= 1:
        return "Yesterday"
    if days < 14:
        return f"{days} days ago"
    if days < 60:
        weeks = max(1, days // 7)
        return f"{weeks} week ago" if weeks == 1 else f"{weeks} weeks ago"
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d")


def first_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload.strip()
    if isinstance(payload, dict):
        for key in ("text", "content", "message"):
            found = first_text(payload.get(key))
            if found:
                return found
        content = payload.get("content")
        if isinstance(content, list):
            for item in content:
                found = first_text(item)
                if found:
                    return found
    if isinstance(payload, list):
        for item in payload:
            found = first_text(item)
            if found:
                return found
    return ""


def session_title(lines: list[dict[str, Any]], fallback: str) -> str:
    for row in lines:
        role = str(row.get("role") or row.get("type") or "").lower()
        if role in {"user", "human"}:
            text = first_text(row.get("message") or row)
            if text:
                return re.sub(r"\s+", " ", text).strip()[:72]
    return fallback


def walk_file_paths(payload: Any, found: list[str]) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in {"file_path", "filePath", "path"} and isinstance(value, str):
                if "/" in value and not value.startswith("http"):
                    found.append(value)
            else:
                walk_file_paths(value, found)
    elif isinstance(payload, list):
        for item in payload:
            walk_file_paths(item, found)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return rows
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def is_cowork(cwd: str, source: str, title: str) -> bool:
    blob = f"{cwd} {source} {title}".lower()
    return "cowork" in blob


def language_of(path: str) -> str:
    ext = Path(path).suffix.lower()
    return {
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".py": "Python",
        ".go": "Go",
        ".rs": "Rust",
        ".md": "Markdown",
        ".json": "JSON",
        ".sh": "Shell",
    }.get(ext, ext.lstrip(".").upper() or "File")


def merge_item(state: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    existing = state["items"].get(item["id"])
    if not existing:
        state["items"][item["id"]] = item
        return item
    for key in ("title", "subtitle", "cwd", "path", "source", "sessionId", "mtime", "kind"):
        if item.get(key) and (not existing.get(key) or key in {"mtime", "subtitle", "title"}):
            existing[key] = item[key]
    return existing


def assign_hub(state: dict[str, Any], item: dict[str, Any]) -> None:
    if item.get("unlinked"):
        item["hubId"] = ""
        return
    if item.get("manual") and item.get("hubId") and item["hubId"] in state["hubs"]:
        return
    cwd = item.get("cwd") or item.get("path") or ""
    remote = item.get("remote") or ""
    root = ""
    short = ""
    if cwd:
        root, git_remote, short = git_identity(cwd)
        remote = remote or git_remote
        item["cwd"] = item.get("cwd") or cwd
        item["remote"] = remote
        if state.get("autoLink") and root:
            hub = ensure_hub(state, root, remote, short)
            item["hubId"] = hub["id"]
            return
    if remote:
        for hub in state["hubs"].values():
            if normalize_remote(hub.get("remote")) == normalize_remote(remote):
                item["hubId"] = hub["id"]
                return
    probe = root or cwd
    if probe:
        for hub in state["hubs"].values():
            hub_path = hub.get("path") or ""
            if hub_path and (probe == hub_path or probe.startswith(hub_path + "/")):
                item["hubId"] = hub["id"]
                return
    if not item.get("manual"):
        item["hubId"] = ""


def discover_claude(state: dict[str, Any]) -> None:
    root = scan_root() / ".claude" / "projects"
    if not root.is_dir():
        return
    for project in sorted(p for p in root.iterdir() if p.is_dir()):
        project_cwd = decode_claude_project(project.name)
        jsonl_files = list(project.glob("*.jsonl"))
        jsonl_files.extend(project.glob("*/*.jsonl"))
        for path in jsonl_files:
            if path.name.endswith(".lock"):
                continue
            rows = load_jsonl(path)
            sid = path.stem
            cwd = session_cwd(rows, project_cwd)
            title = session_title(rows, sid)
            kind = "cowork" if is_cowork(cwd, "claude", title) else "chat"
            mtime = path.stat().st_mtime
            item = {
                "id": f"chat:{sid}",
                "kind": kind,
                "title": title,
                "subtitle": relative_when(mtime),
                "sessionId": sid,
                "source": "claude",
                "cwd": cwd,
                "path": "",
                "hubId": "",
                "manual": False,
                "unlinked": False,
                "mtime": mtime,
            }
            stored = merge_item(state, item)
            if not stored.get("manual"):
                stored["unlinked"] = False
            assign_hub(state, stored)
            files: list[str] = []
            walk_file_paths(rows, files)
            seen: set[str] = set()
            for file_path in files:
                resolved = file_path
                if not resolved.startswith("/"):
                    resolved = str(Path(cwd) / file_path)
                if resolved in seen:
                    continue
                seen.add(resolved)
                code = {
                    "id": f"code:{resolved}",
                    "kind": "code",
                    "title": Path(resolved).name,
                    "subtitle": f"{language_of(resolved)} · {Path(resolved).as_posix()}",
                    "sessionId": sid,
                    "source": "claude",
                    "cwd": cwd,
                    "path": resolved,
                    "hubId": stored.get("hubId") or "",
                    "manual": False,
                    "unlinked": False,
                    "mtime": mtime,
                }
                code_stored = merge_item(state, code)
                if not code_stored.get("manual"):
                    assign_hub(state, code_stored)


def discover_cursor(state: dict[str, Any]) -> None:
    root = scan_root() / ".cursor" / "projects"
    if not root.is_dir():
        return
    candidates = list(root.glob("*/agent-transcripts/*.jsonl"))
    candidates.extend(root.glob("*/*.jsonl"))
    for path in candidates:
        if path.name.endswith(".lock"):
            continue
        rows = load_jsonl(path)
        sid = path.stem
        cwd = ""
        for row in rows:
            cwd = row.get("cwd") or row.get("workspace") or cwd
        if not cwd:
            parent = path.parent
            if parent.name == "agent-transcripts":
                cwd = decode_claude_project(parent.parent.name)
            else:
                cwd = decode_claude_project(parent.name)
        title = session_title(rows, sid)
        mtime = path.stat().st_mtime
        item = {
            "id": f"code:{sid}",
            "kind": "code",
            "title": title,
            "subtitle": f"Cursor · {relative_when(mtime)}",
            "sessionId": sid,
            "source": "cursor",
            "cwd": cwd,
            "path": "",
            "hubId": "",
            "manual": False,
            "unlinked": False,
            "mtime": mtime,
        }
        stored = merge_item(state, item)
        if not stored.get("manual"):
            stored["unlinked"] = False
        assign_hub(state, stored)


def discover(state: dict[str, Any]) -> dict[str, Any]:
    discover_claude(state)
    discover_cursor(state)
    return state


def grouped(state: dict[str, Any]) -> dict[str, Any]:
    hubs = []
    unlinked = []
    for hub in sorted(state["hubs"].values(), key=lambda h: h.get("shortName") or h["id"]):
        chats = []
        code = []
        for item in state["items"].values():
            if item.get("unlinked") or item.get("hubId") != hub["id"]:
                continue
            if item.get("kind") == "code":
                code.append(item)
            else:
                chats.append(item)
        chats.sort(key=lambda i: (-float(i.get("mtime") or 0), i.get("title") or ""))
        code.sort(key=lambda i: (-float(i.get("mtime") or 0), i.get("title") or ""))
        hubs.append({"hub": hub, "chats": chats, "code": code})
    for item in state["items"].values():
        if item.get("unlinked") or not item.get("hubId") or item.get("hubId") not in state["hubs"]:
            unlinked.append(item)
    unlinked.sort(key=lambda i: (-float(i.get("mtime") or 0), i.get("title") or ""))
    return {
        "autoLink": bool(state.get("autoLink")),
        "hubs": hubs,
        "unlinked": unlinked,
    }


def current_identity(cwd: str | None = None) -> tuple[str, str, str]:
    raw = cwd or os.environ.get("PATH_HUBS_CWD") or os.getcwd()
    return git_identity(raw)


def current_session_id() -> str:
    return os.environ.get("PATH_HUBS_SESSION_ID") or ""


def select_hub(tree: dict[str, Any], cwd: str | None = None) -> dict[str, Any] | None:
    if not tree["hubs"]:
        return None
    root, remote, _short = current_identity(cwd)
    for row in tree["hubs"]:
        hub = row["hub"]
        if root and hub.get("path") == root:
            return row
        if remote and normalize_remote(hub.get("remote")) == normalize_remote(remote):
            return row
    return tree["hubs"][0]


def link_item(
    state: dict[str, Any],
    *,
    item_id: str = "",
    hub_ref: str = "",
    kind: str = "",
    title: str = "",
    path: str = "",
    cwd: str = "",
    session_id: str = "",
) -> dict[str, Any]:
    cwd = expand_path(cwd) or current_identity()[0] or os.getcwd()
    session_id = session_id or current_session_id()
    path = expand_path(path)
    if hub_ref:
        if hub_ref in state["hubs"]:
            hub = state["hubs"][hub_ref]
        elif hub_ref.startswith("/") or hub_ref.startswith("~") or "/" in hub_ref:
            ref_path = expand_path(hub_ref) if hub_ref.startswith("~") or hub_ref.startswith("/") else hub_ref
            if Path(ref_path).exists() or ref_path.startswith("/"):
                root, remote, short = git_identity(ref_path)
                hub = ensure_hub(state, root or ref_path, remote, short)
            else:
                hub = ensure_hub(state, cwd, "", hub_ref)
        else:
            hub = ensure_hub(state, cwd, "", hub_ref)
    else:
        root, remote, short = git_identity(cwd)
        hub = ensure_hub(state, root or cwd, remote, short)
    if not item_id:
        if path:
            item_id = f"code:{path}"
        elif session_id:
            prefix = "code" if (kind or "chat") == "code" else "chat"
            item_id = f"{prefix}:{session_id}"
        else:
            item_id = f"chat:{hub['id']}:{int(now_ts())}"
    existing = state["items"].get(item_id, {})
    resolved_kind = kind or existing.get("kind") or ("code" if path or item_id.startswith("code:") else "chat")
    item = {
        "id": item_id,
        "kind": resolved_kind,
        "title": title or existing.get("title") or (Path(path).name if path else session_id or item_id),
        "subtitle": existing.get("subtitle") or relative_when(now_ts()),
        "sessionId": session_id or existing.get("sessionId") or "",
        "source": existing.get("source") or "manual",
        "cwd": cwd or existing.get("cwd") or "",
        "path": path or existing.get("path") or "",
        "remote": hub.get("remote") or "",
        "hubId": hub["id"],
        "manual": True,
        "unlinked": False,
        "mtime": existing.get("mtime") or now_ts(),
    }
    state["items"][item_id] = item
    return item


def unlink_item(state: dict[str, Any], item_id: str = "") -> dict[str, Any]:
    if not item_id:
        sid = current_session_id()
        if sid:
            for prefix in ("chat", "code"):
                candidate = f"{prefix}:{sid}"
                if candidate in state["items"]:
                    item_id = candidate
                    break
        if not item_id:
            cwd = current_identity()[0]
            for item in state["items"].values():
                if item.get("cwd") == cwd and not item.get("unlinked"):
                    item_id = item["id"]
                    break
    if not item_id or item_id not in state["items"]:
        raise SystemExit("nothing to unlink")
    item = state["items"][item_id]
    item["unlinked"] = True
    item["hubId"] = ""
    item["manual"] = True
    return item


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def render_text(state: dict[str, Any], cwd: str | None = None) -> str:
    tree = grouped(state)
    selected = select_hub(tree, cwd)
    auto = "on" if tree["autoLink"] else "off"
    lines = ["2a · Path hubs", f"Auto-link new repos: {auto}", ""]
    lines.append("PATH HUBS")
    if not tree["hubs"]:
        lines.append("  (none)")
    for row in tree["hubs"]:
        hub = row["hub"]
        mark = "●" if selected and selected["hub"]["id"] == hub["id"] else "○"
        lines.append(f"  {mark} {hub.get('shortName') or hub['id']}")
        if hub.get("path"):
            lines.append(f"    {display_path(hub['path'])}")
        lines.append(f"    Chats ({len(row['chats'])})")
        for item in row["chats"]:
            extra = " · cowork" if item.get("kind") == "cowork" else ""
            lines.append(f"      🔗 {item.get('title') or item['id']}{extra}")
        lines.append(f"    Code ({len(row['code'])})")
        for item in row["code"]:
            lines.append(f"      🔗 {item.get('title') or item['id']}")
    lines.append("")
    lines.append("UNLINKED")
    chats = [i for i in tree["unlinked"] if i.get("kind") != "code"]
    code = [i for i in tree["unlinked"] if i.get("kind") == "code"]
    if not tree["unlinked"]:
        lines.append("  (none)")
    else:
        for item in chats:
            lines.append(f"  {item.get('title') or item['id']}")
        for item in code:
            lines.append(f"  {item.get('title') or item['id']}")
    if selected:
        hub = selected["hub"]
        lines.extend(
            [
                "",
                f"Chat context · {hub.get('shortName')}",
                f"Code context · {hub.get('shortName')}",
                f"Same grouping in both modes · {len(selected['chats'])} chats · {len(selected['code'])} code",
            ]
        )
    return "\n".join(lines) + "\n"


ICON_FOLDER = (
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="#e07a5f" d="M3 6.75A2.75 2.75 0 0 1 5.75 4h4.1c.4 0 .78.16 1.06.44l1.15 1.15c.18.18.43.28.69.28H18.25A2.75 2.75 0 0 1 21 8.62v8.63A2.75 2.75 0 0 1 18.25 20H5.75A2.75 2.75 0 0 1 3 17.25V6.75Z"/></svg>'
)
ICON_CHAT = (
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="#e07a5f" d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8A2.5 2.5 0 0 1 17.5 16H9l-4 4v-4.2A2.5 2.5 0 0 1 4 13.5v-8Z"/></svg>'
)
ICON_CODE = (
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="#e07a5f" d="M8.3 7.3 3.6 12l4.7 4.7 1.4-1.4L6.4 12l3.3-3.3-1.4-1.4Zm7.4 0-1.4 1.4L17.6 12l-3.3 3.3 1.4 1.4 4.7-4.7-4.7-4.7Z"/></svg>'
)
ICON_CHAIN = (
    '<svg class="ico chain" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="#e07a5f" d="M10.6 13.4a4 4 0 0 1 0-5.6l2.1-2.1a4 4 0 0 1 5.6 5.6l-1.2 1.2-1.4-1.4 1.2-1.2a2 2 0 1 0-2.8-2.8l-2.1 2.1a2 2 0 0 0 0 2.8l.7.7-1.4 1.4-.7-.7Zm2.8-2.8a4 4 0 0 1 0 5.6l-2.1 2.1a4 4 0 1 1-5.6-5.6l1.2-1.2 1.4 1.4-1.2 1.2a2 2 0 1 0 2.8 2.8l2.1-2.1a2 2 0 0 0 0-2.8l-.7-.7 1.4-1.4.7.7Z"/></svg>'
)


def item_meta(item: dict[str, Any]) -> str:
    if item.get("kind") == "code":
        path = item.get("path") or ""
        rel = path
        cwd = item.get("cwd") or ""
        if cwd and path.startswith(cwd + "/"):
            rel = path[len(cwd) + 1 :]
        return f"{language_of(path)} · {rel or item.get('title')}"
    return item.get("subtitle") or ""


def render_html(state: dict[str, Any], cwd: str | None = None) -> str:
    tree = grouped(state)
    selected = select_hub(tree, cwd)
    auto = "on" if tree["autoLink"] else "off"
    selected_name = (selected["hub"].get("shortName") if selected else "—")
    selected_path = display_path(selected["hub"]["path"]) if selected and selected["hub"].get("path") else ""
    chat_count = len(selected["chats"]) if selected else 0
    code_count = len(selected["code"]) if selected else 0

    def items_html(items: list[dict[str, Any]], linked: bool) -> str:
        if not items:
            return '<div class="empty">None</div>'
        chunks = []
        for item in items:
            title = html.escape(str(item.get("title") or item["id"]))
            meta = html.escape(item_meta(item))
            icon = ICON_CODE if item.get("kind") == "code" else ICON_CHAT
            link = "linked" if linked else "unlinked"
            cowork = " cowork" if item.get("kind") == "cowork" else ""
            chunks.append(
                f'<div class="row {link}{cowork}">'
                f'{icon}'
                f'<span class="copy"><span class="title">{title}</span>'
                f'<span class="meta">{meta}</span></span>'
                f'{ICON_CHAIN}'
                f"</div>"
            )
        return "".join(chunks)

    hub_blocks = []
    for row in tree["hubs"]:
        hub = row["hub"]
        active = " active" if selected and selected["hub"]["id"] == hub["id"] else ""
        hub_blocks.append(
            f'<section class="hub{active}">'
            f'<div class="hub-head">{ICON_FOLDER}'
            f'<span class="hub-name">{html.escape(hub.get("shortName") or hub["id"])}</span></div>'
            f'<div class="hub-path">{html.escape(display_path(hub.get("path") or ""))}</div>'
            f'<div class="folder-line"><span>Chats</span><span class="count">{len(row["chats"])}</span></div>'
            f'{items_html(row["chats"], True)}'
            f'<div class="folder-line"><span>Code</span><span class="count">{len(row["code"])}</span></div>'
            f'{items_html(row["code"], True)}'
            f"</section>"
        )
    unlinked_chats = [i for i in tree["unlinked"] if i.get("kind") != "code"]
    unlinked_code = [i for i in tree["unlinked"] if i.get("kind") == "code"]
    chat_items = selected["chats"] if selected else []
    code_items = selected["code"] if selected else []
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2a · Path hubs</title>
<style>
:root {{
  --bg: #14110f;
  --panel: #1b1714;
  --sidebar: #181512;
  --ink: #f3ece3;
  --muted: #9c9288;
  --coral: #e07a5f;
  --green: #7dce82;
  --line: #2c2622;
  --field: #241f1b;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: var(--bg); color: var(--ink); font: 13px/1.45 ui-sans-serif, "Segoe UI", sans-serif; }}
.app {{ min-height: 100vh; display: grid; grid-template-rows: 52px 1fr 36px; }}
.top {{ display: flex; align-items: center; padding: 0 20px; border-bottom: 1px solid var(--line); letter-spacing: 0.02em; }}
.top h1 {{ font-size: 16px; font-weight: 560; margin: 0; }}
.body {{ display: grid; grid-template-columns: 280px 1fr 1fr; min-height: 0; }}
.side {{ background: var(--sidebar); border-right: 1px solid var(--line); padding: 16px 14px 20px; overflow: auto; }}
.kicker {{ color: var(--muted); font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; margin: 18px 0 8px; }}
.kicker:first-child {{ margin-top: 0; }}
.hub {{ padding: 10px 0 14px; }}
.hub-head {{ display: flex; gap: 8px; align-items: center; color: var(--coral); font-weight: 600; }}
.hub.active .hub-name {{ color: var(--ink); }}
.ico {{ width: 14px; height: 14px; flex: 0 0 14px; display: block; }}
.hub-path {{ color: var(--muted); font-size: 11px; padding: 2px 0 8px 22px; }}
.folder-line {{ display: flex; justify-content: space-between; color: var(--muted); padding: 6px 0 4px 8px; }}
.count {{ color: var(--ink); }}
.row {{ display: grid; grid-template-columns: 14px 1fr 14px; gap: 8px; align-items: start; padding: 6px 4px; }}
.row .title {{ display: block; }}
.row .meta {{ display: block; color: var(--muted); font-size: 11px; }}
.row.unlinked .chain {{ opacity: 0.35; }}
.empty {{ color: var(--muted); padding: 4px 8px 8px; }}
.toggle {{ display: flex; align-items: center; gap: 10px; margin-top: 22px; padding-top: 14px; border-top: 1px solid var(--line); }}
.switch {{ width: 36px; height: 20px; border-radius: 99px; background: #3a332e; position: relative; }}
.switch.on {{ background: var(--coral); }}
.switch::after {{ content: ""; width: 14px; height: 14px; border-radius: 50%; background: var(--ink); position: absolute; top: 3px; left: 3px; }}
.switch.on::after {{ left: 19px; }}
.col {{ padding: 20px 22px; overflow: auto; }}
.col + .col {{ border-left: 1px solid var(--line); }}
.col h2 {{ margin: 0 0 14px; font-size: 16px; font-weight: 560; }}
.card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; margin-bottom: 16px; }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--green); display: inline-block; margin-right: 8px; }}
.field {{ margin-top: 8px; background: var(--field); border-radius: 8px; padding: 8px 10px; }}
.field .sub {{ color: var(--muted); font-size: 11px; }}
.foot {{ display: flex; gap: 18px; align-items: center; padding: 0 16px; border-top: 1px solid var(--line); color: var(--muted); font-size: 11px; }}
.note {{ color: var(--muted); font-size: 11px; margin-top: 8px; }}
</style>
</head>
<body>
<div class="app">
  <header class="top"><h1>2a · Path hubs</h1></header>
  <div class="body">
    <aside class="side">
      <div class="kicker">Path hubs</div>
      {''.join(hub_blocks) if hub_blocks else '<div class="empty">No hubs yet</div>'}
      <div class="kicker">Unlinked</div>
      {items_html(unlinked_chats + unlinked_code, False)}
      <div class="toggle">
        <div class="switch {auto}"></div>
        <div>
          <div>Auto-link new repos</div>
          <div class="note">Link paths automatically · {auto}</div>
        </div>
      </div>
    </aside>
    <section class="col">
      <h2>Chat context</h2>
      <div class="card"><span class="dot"></span>Connected to hub<div class="field">{html.escape(str(selected_name))}<div class="sub">{html.escape(selected_path)}</div></div></div>
      <div class="kicker">Linked items</div>
      {items_html(chat_items, True)}
      <div class="kicker">Unlinked items</div>
      {items_html(unlinked_chats, False)}
    </section>
    <section class="col">
      <h2>Code context</h2>
      <div class="card"><span class="dot"></span>Connected to hub<div class="field">{html.escape(str(selected_name))}<div class="sub">{html.escape(selected_path)}</div></div></div>
      <div class="kicker">Linked items</div>
      {items_html(code_items, True)}
      <div class="kicker">Unlinked items</div>
      {items_html(unlinked_code, False)}
    </section>
  </div>
  <footer class="foot">
    <span>Chat context · {html.escape(str(selected_name))} · {chat_count} linked items</span>
    <span>Code context · {html.escape(str(selected_name))} · {code_count} linked items</span>
    <span>2a · Path hubs · auto-link {auto}</span>
  </footer>
</div>
</body>
</html>
"""


def write_html(state: dict[str, Any], dest: Path | None = None, cwd: str | None = None) -> Path:
    dest = dest or view_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(render_html(state, cwd), encoding="utf-8")
    return dest


def cmd_view(args: argparse.Namespace) -> int:
    state = load_state()
    discover(state)
    save_state(state)
    fmt = args.format
    if fmt in {"html", "both"}:
        dest = Path(args.out) if args.out else view_path()
        written = write_html(state, dest)
        print(f"html: {written}")
    if fmt in {"text", "both"}:
        sys.stdout.write(render_text(state))
    return 0


def cmd_auto(on: bool) -> int:
    state = load_state()
    state["autoLink"] = on
    save_state(state)
    print(f"Auto-link new repos is {'on' if on else 'off'}.")
    return 0


def cmd_link(args: argparse.Namespace) -> int:
    state = load_state()
    discover(state)
    item = link_item(
        state,
        item_id=args.id,
        hub_ref=args.hub or args.target,
        kind=args.kind,
        title=args.title,
        path=args.path,
        cwd=args.cwd,
        session_id=args.session_id,
    )
    save_state(state)
    print(f"Linked {item['id']} to {item['hubId']}.")
    return 0


def cmd_unlink(args: argparse.Namespace) -> int:
    state = load_state()
    item = unlink_item(state, args.id or args.target)
    save_state(state)
    print(f"Unlinked {item['id']}.")
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    state = load_state()
    discover(state)
    save_state(state)
    tree = grouped(state)
    selected = select_hub(tree)
    auto = "on" if tree["autoLink"] else "off"
    name = selected["hub"].get("shortName") if selected else "unlinked"
    chats = len(selected["chats"]) if selected else 0
    code = len(selected["code"]) if selected else 0
    print(f"2a · {name} · {chats} chats · {code} code · auto-link {auto} · unlinked {len(tree['unlinked'])}")
    return 0


def cmd_statusline(_args: argparse.Namespace) -> int:
    payload = read_stdin_json()
    cwd = payload.get("cwd") or payload.get("workspace_dir") or None
    if payload.get("session_id"):
        os.environ["PATH_HUBS_SESSION_ID"] = str(payload["session_id"])
    state = load_state()
    discover(state)
    if cwd and state.get("autoLink"):
        root, _remote, _short = git_identity(str(cwd))
        if root:
            link_item(state, cwd=str(cwd), session_id=str(payload.get("session_id") or ""))
            save_state(state)
    tree = grouped(state)
    selected = select_hub(tree, cwd)
    auto = "on" if tree["autoLink"] else "off"
    name = selected["hub"].get("shortName") if selected else "unlinked"
    chats = len(selected["chats"]) if selected else 0
    code = len(selected["code"]) if selected else 0
    print(f"2a · {name} · {chats} chats · {code} code · auto-link {auto}")
    return 0


def cmd_session_start(_args: argparse.Namespace) -> int:
    payload = read_stdin_json()
    cwd = str(payload.get("cwd") or payload.get("workspace_dir") or os.getcwd())
    sid = str(payload.get("session_id") or "")
    if sid:
        os.environ["PATH_HUBS_SESSION_ID"] = sid
    state = load_state()
    discover(state)
    root, _remote, short = git_identity(cwd)
    if state.get("autoLink") and root:
        item = link_item(
            state,
            session_id=sid,
            cwd=cwd,
            kind="cowork" if is_cowork(cwd, str(payload.get("source") or ""), "") else "chat",
            title=str(payload.get("session_name") or sid or "Current session"),
        )
        save_state(state)
        message = f"Path hubs: linked to {item['hubId']} (auto-link on)."
    else:
        save_state(state)
        message = "Path hubs: auto-link is off."
        if state.get("autoLink") and not root:
            message = "Path hubs: unlinked (auto-link on; no git repo)."
        for item in state["items"].values():
            if item.get("cwd") in {root, cwd} and item.get("hubId"):
                flag = "on" if state.get("autoLink") else "off"
                message = f"Path hubs: {item['hubId']} (auto-link {flag})."
                break
        else:
            if not state.get("autoLink"):
                message = f"Path hubs: {short or 'unlinked'} (auto-link off)."
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": message,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Path hubs")
    sub = parser.add_subparsers(dest="cmd", required=True)
    view = sub.add_parser("view")
    view.add_argument("--format", choices=("text", "html", "both"), default="both")
    view.add_argument("--out")
    view.set_defaults(func=cmd_view)
    on = sub.add_parser("auto-on")
    on.set_defaults(func=lambda _a: cmd_auto(True))
    off = sub.add_parser("auto-off")
    off.set_defaults(func=lambda _a: cmd_auto(False))
    link = sub.add_parser("link")
    link.add_argument("target", nargs="?", default="")
    link.add_argument("--id", default="")
    link.add_argument("--hub", default="")
    link.add_argument("--kind", default="")
    link.add_argument("--title", default="")
    link.add_argument("--path", default="")
    link.add_argument("--cwd", default="")
    link.add_argument("--session-id", default="")
    link.set_defaults(func=cmd_link)
    unlink = sub.add_parser("unlink")
    unlink.add_argument("target", nargs="?", default="")
    unlink.add_argument("--id", default="")
    unlink.set_defaults(func=cmd_unlink)
    status = sub.add_parser("status")
    status.set_defaults(func=cmd_status)
    statusline = sub.add_parser("statusline")
    statusline.set_defaults(func=cmd_statusline)
    start = sub.add_parser("session-start")
    start.set_defaults(func=cmd_session_start)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
