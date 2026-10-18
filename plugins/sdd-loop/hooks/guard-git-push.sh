#!/bin/sh
# Only enforce inside an active sdd-loop workspace (marked by a .sdd/ dir).
# Claude PreToolUse (exit 2) and Cursor beforeShellExecution (JSON permission).
if [ ! -d ".sdd" ]; then
  exit 0
fi
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

kind=""
case "$cmd" in
  *"gh pr merge"* | *"glab mr merge"*) kind="merge" ;;
esac
if [ -z "$kind" ]; then
  case "$cmd" in
    *"git push"* | *"gh pr create"* | *"gh pr edit"* | *"glab mr create"*) kind="push" ;;
  esac
fi
if [ -z "$kind" ]; then
  case "$cmd" in
    *"gh api"* | *"glab api"*) kind="api" ;;
  esac
fi
if [ -z "$kind" ]; then
  exit 0
fi

protected=""
force=""
case "$cmd" in
  *"git push"*)
    case "$cmd" in
      *" --force"* | *" --force-with-lease"* | *" -f "* | *" -f" | *"git push -f "*) force=1 ;;
    esac
    if printf '%s' "$cmd" | grep -Eq '(^|[[:space:]])origin[[:space:]]+(main|master|trunk)([[:space:]"'\'':]|$)|HEAD:(main|master|trunk)([[:space:]"'\'']|$)|:refs/heads/(main|master|trunk)([[:space:]"'\'']|$)'; then
      protected=1
    fi
    ;;
esac

if [ -f ".sdd/.approve-external" ]; then
  allow
fi

autonomous=""
merge_gated=""
if [ -f ".sdd/autonomy.json" ]; then
  if [ -n "$have_jq" ]; then
    mode=$(jq -r '.mode // empty' ".sdd/autonomy.json" 2>/dev/null)
    [ "$mode" = "auto" ] && autonomous=1
    jq -e '.gates | index("merge")' ".sdd/autonomy.json" >/dev/null 2>&1 && merge_gated=1
  else
    grep -q '"mode"[[:space:]]*:[[:space:]]*"auto"' ".sdd/autonomy.json" 2>/dev/null && autonomous=1
    grep -q '"merge"' ".sdd/autonomy.json" 2>/dev/null && merge_gated=1
  fi
fi

if [ -n "$force" ]; then
  deny "sdd-loop guardrail: blocked a force push. --force / --force-with-lease / -f need the per-item sentinel, even in an autonomous run."
fi
if [ -n "$protected" ]; then
  deny "sdd-loop guardrail: blocked a push to main, master, or trunk. Default-branch pushes need the per-item sentinel, even in an autonomous run."
fi

case "$kind" in
  push)
    if [ -n "$autonomous" ]; then
      allow
    fi
    deny "sdd-loop guardrail: blocked a remote push or PR write. This needs per-item approval through the Review Gate, or an armed autonomous run started with an explicit 'auto gates=...' invocation, which writes the .sdd/autonomy.json policy file this hook reads."
    ;;
  merge)
    if [ -n "$autonomous" ] && [ -z "$merge_gated" ]; then
      allow
    fi
    if [ -n "$autonomous" ]; then
      deny "sdd-loop guardrail: blocked a merge. 'merge' is a gated checkpoint in this autonomous run, so no merge happens until a human approves it. Park the ticket in .sdd/GATES.md and wait for the gate: the merge then runs under the per-item sentinel, or on the next iteration once the gate is marked PASSED."
    else
      deny "sdd-loop guardrail: blocked a merge. Merging needs per-item approval through the Review Gate, or an autonomous run whose declared gates do not include 'merge'."
    fi
    ;;
  api)
    deny "sdd-loop guardrail: blocked a raw gh/glab api call. Arbitrary remote API writes always need per-item approval through the Review Gate, even inside an autonomous run, because they can reach past every other guard here. For autonomous push and PR actions, use the specific gh/glab subcommands instead. Origin and Bitbucket have no shipped CLI matchers; use git plus the host PR UI or a connected MCP."
    ;;
esac
exit 0
