#!/bin/sh
root=$(git rev-parse --show-toplevel 2>/dev/null) || root="."
rm -f "$root/.lean-gate-off"
rm -f .lean-gate-off
echo "Lean gate is on for this project."
