#!/bin/sh
root=$(git rev-parse --show-toplevel 2>/dev/null) || root="."
: > "$root/.lean-gate-off"
echo "Lean gate is off for this project."
