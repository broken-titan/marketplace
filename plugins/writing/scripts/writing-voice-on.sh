#!/bin/sh
: > .writing-voice
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
template="$here/../templates/writing-voice.mdc"
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ] && [ -f "${CURSOR_PLUGIN_ROOT}/templates/writing-voice.mdc" ]; then
  template="${CURSOR_PLUGIN_ROOT}/templates/writing-voice.mdc"
fi
if [ -f "$template" ]; then
  mkdir -p .cursor/rules
  cp "$template" .cursor/rules/writing-voice.mdc
fi
echo "Writing voice is on for this project."
