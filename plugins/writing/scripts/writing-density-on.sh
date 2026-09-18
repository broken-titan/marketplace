#!/bin/sh
rm -f .writing-density-off
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ]; then
  mkdir -p .cursor/rules
  cp "${CURSOR_PLUGIN_ROOT}/templates/writing-density.mdc" .cursor/rules/writing-density.mdc
  echo "Writing density is on for this Cursor project."
  exit 0
fi
echo "Writing density is on for this project."
