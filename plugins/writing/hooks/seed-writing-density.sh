#!/bin/sh
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(git rev-parse --show-toplevel 2>/dev/null) || root="."
if [ -f .writing-density-off ] || [ -f "$root/.writing-density-off" ]; then
  rm -f .cursor/rules/writing-density.mdc
  rm -f "$root/.cursor/rules/writing-density.mdc"
  exit 0
fi
if [ -z "${CURSOR_PLUGIN_ROOT:-}" ]; then
  exit 0
fi
template="${CURSOR_PLUGIN_ROOT}/templates/writing-density.mdc"
if [ ! -f "$template" ]; then
  template="$here/../templates/writing-density.mdc"
fi
if [ ! -f "$template" ]; then
  exit 0
fi
mkdir -p .cursor/rules
cp "$template" .cursor/rules/writing-density.mdc
