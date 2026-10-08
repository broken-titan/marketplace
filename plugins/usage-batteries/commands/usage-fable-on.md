---
description: Show the weekly Fable usage battery.
---

Run `sh "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/usage-fable-on.sh"`. Toggles go through the scripts. Do not invent a Fable percent. Fill is 100 minus used, clamped, only when a Fable window exists. Then tell the user the weekly Fable meter is on.
