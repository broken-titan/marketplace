#!/bin/sh
if [ -n "${GROK_PLUGIN_ROOT:-}" ]; then
  exec python3 "${GROK_PLUGIN_ROOT}/scripts/path_hubs.py" statusline
fi
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$here/path_hubs.py" statusline
