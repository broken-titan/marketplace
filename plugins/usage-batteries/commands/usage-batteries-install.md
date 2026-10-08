---
description: Wire usage batteries into the Claude Code status line.
---

Run `sh "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/usage-batteries-install.sh"` from the project. If the user asked to replace an existing status line, add `--force`. Then tell the user whether the status line is on or was left in place.
