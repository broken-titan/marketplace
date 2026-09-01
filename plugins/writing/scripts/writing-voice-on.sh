#!/bin/sh
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ]; then
  mkdir -p .cursor/rules
  cp "${CURSOR_PLUGIN_ROOT}/templates/writing-voice.mdc" .cursor/rules/writing-voice.mdc
  echo "Writing voice is on for this Cursor project."
  exit 0
fi
: > .writing-voice
echo "Writing voice is on for this project."
