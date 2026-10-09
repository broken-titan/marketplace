#!/bin/sh
rm -f .writing-density-off
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
template="$here/../templates/writing-density.mdc"
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ] && [ -f "${CURSOR_PLUGIN_ROOT}/templates/writing-density.mdc" ]; then
  template="${CURSOR_PLUGIN_ROOT}/templates/writing-density.mdc"
fi
if [ -f "$template" ]; then
  mkdir -p .cursor/rules
  cp "$template" .cursor/rules/writing-density.mdc
fi
echo "Writing density is on for this project."
