---
description: Wire usage batteries into the Claude Code status line.
---

Run `sh "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/usage-batteries-install.sh"` from the project. Do not overwrite an existing statusLine unless the user asked for `--force`. Fill is 100 minus used, clamped 0–100. Then tell the user whether the status line is on or was left in place.
