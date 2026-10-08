#!/bin/sh
input=$(cat)
have_jq=""
if command -v jq >/dev/null 2>&1; then
  have_jq=1
  cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // .command // empty' 2>/dev/null)
else
  cmd=$input
fi
if [ -z "$cmd" ]; then
  exit 0
fi

cursor=""
if [ -n "$have_jq" ]; then
  printf '%s' "$input" | jq -e '.command != null and .tool_input.command == null' >/dev/null 2>&1 && cursor=1
fi

deny() {
  msg=$1
  if [ -n "$cursor" ]; then
    printf '{"permission":"deny","agent_message":"%s"}\n' "$msg"
  fi
  echo "$msg" >&2
  exit 2
}

allow() {
  if [ -n "$cursor" ]; then
    printf '%s\n' '{"permission":"allow"}'
  fi
  exit 0
}

if ! printf '%s' "$cmd" | grep -Eq '(^|[[:space:];|&])git[[:space:]]+(commit|push)([[:space:]]|$)|(^|[[:space:];|&])git[[:space:]].*[[:space:]](commit|push)([[:space:]]|$)'; then
  allow
fi

root=$(git rev-parse --show-toplevel 2>/dev/null) || root="."
if [ -f "$root/.lean-gate-off" ] || [ -f .lean-gate-off ]; then
  allow
fi

gitdir=$(git rev-parse --git-dir 2>/dev/null) || gitdir=".git"
if [ -f "$gitdir/lean-gate.ok" ]; then
  rm -f "$gitdir/lean-gate.ok"
  allow
fi

deny "lean-gate: apply the lean-gate skill to the staged or to-be-pushed diff, write lean-gate.ok in the git dir, then retry this command."
