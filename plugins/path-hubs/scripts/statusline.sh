#!/bin/sh
if [ -n "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}" ]; then
  exec python3 "${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}}/scripts/path_hubs.py" statusline
fi
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$here/path_hubs.py" statusline
