---
description: Show Path hubs grouped by git repo path (Chats, Code, Unlinked).
---

Run `sh "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/path-hubs.sh" view` from the project root. Print only that output. Never invent hubs, chats, or files. If it printed an `html:` path, tell them they can open that file.
