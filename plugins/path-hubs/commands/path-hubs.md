---
description: Show Path hubs grouped by git repo path (Chats, Code, Unlinked).
---

Run `sh "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/path-hubs.sh" view` from the project root. Show the command output to the user. If it printed an `html:` path, tell them they can open that file. Do not invent hubs the command did not print.
