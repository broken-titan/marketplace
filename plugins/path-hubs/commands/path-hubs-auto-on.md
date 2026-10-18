---
description: Turn Path hubs auto-link on. New repos join a hub from cwd or git remote.
---

Run `sh "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/path-hubs.sh" auto-on` from the project root only when the user asked to turn auto-link on. Leave auto-link alone otherwise. Then tell the user auto-link is on.
