---
description: Turn Path hubs auto-link off. Existing links stay until unlinked.
---

Run `sh "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/path-hubs.sh" auto-off` from the project root only when the user asked to turn auto-link off. Leave auto-link alone otherwise. Then tell the user auto-link is off.
