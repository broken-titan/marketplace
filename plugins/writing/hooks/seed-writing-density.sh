#!/bin/sh
# Cursor only. UserPromptSubmit is stripped on Cursor, so the density card
# is a project .mdc. No off sentinel => the rule is present; an off sentinel
# removes it. Claude and Grok inject via UserPromptSubmit and no-op here.
if [ -z "${CURSOR_PLUGIN_ROOT:-}" ]; then
  exit 0
fi
root=$(git rev-parse --show-toplevel 2>/dev/null) || root="."
if [ -f .writing-density-off ] || [ -f "$root/.writing-density-off" ]; then
  rm -f .cursor/rules/writing-density.mdc
  rm -f "$root/.cursor/rules/writing-density.mdc"
  exit 0
fi
mkdir -p .cursor/rules
cp "${CURSOR_PLUGIN_ROOT}/templates/writing-density.mdc" .cursor/rules/writing-density.mdc
