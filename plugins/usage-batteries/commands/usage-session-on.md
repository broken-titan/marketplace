---
description: Show the session usage battery.
---

Run `sh "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/usage-session-on.sh"`. Toggles go through the scripts. Fill is 100 minus used, clamped. Then tell the user the session meter is on.
