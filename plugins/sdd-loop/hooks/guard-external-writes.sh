#!/bin/sh
# Only enforce inside an active sdd-loop workspace (marked by a .sdd/ dir).
# Claude PreToolUse (exit 2) and Cursor beforeMCPExecution (JSON permission).
if [ ! -d ".sdd" ]; then
  exit 0
fi
input=$(cat)
cursor=""
tool_name=""
if command -v jq >/dev/null 2>&1; then
  printf '%s' "$input" | jq -e '.tool_name != null or .hook_event_name != null' >/dev/null 2>&1 && cursor=1
  printf '%s' "$input" | jq -e '.tool_input.command != null' >/dev/null 2>&1 && cursor=""
  tool_name=$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null)
else
  tool_name=$(printf '%s' "$input" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
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

write_tool() {
  name=$1
  name=${name#MCP:}
  name=${name# }
  case "$name" in
    mcp__*__*) name=${name##*__} ;;
  esac
  case "$name" in
    *:*) name=${name##*:} ;;
  esac
  case "$name" in
    createJiraIssue|editJiraIssue|transitionJiraIssue|addCommentToJiraIssue|addWorklogToJiraIssue|createIssueLink|createConfluencePage|updateConfluencePage|createConfluenceFooterComment|createConfluenceInlineComment|createCompassComponent|createCompassComponentRelationship|createCompassCustomFieldDefinition)
      return 0
      ;;
  esac
  printf '%s' "$name" | grep -Eq '^jira_(create|update|delete|add|set|transition|bulk|move|complete|start)_.*' && return 0
  printf '%s' "$name" | grep -Eq '^confluence_(create|update|delete|upload|add|remove|set)_.*' && return 0
  return 1
}

if [ -n "$tool_name" ] && ! write_tool "$tool_name"; then
  allow
fi

if [ -f ".sdd/.approve-external" ]; then
  if [ -n "$cursor" ]; then
    printf '%s\n' '{"permission":"allow"}'
  fi
  exit 0
fi
if [ -f ".sdd/autonomy.json" ]; then
  if command -v jq >/dev/null 2>&1; then
    mode=$(jq -r '.mode // empty' ".sdd/autonomy.json" 2>/dev/null)
    if [ "$mode" = "auto" ]; then
      if [ -n "$cursor" ]; then
        printf '%s\n' '{"permission":"allow"}'
      fi
      exit 0
    fi
  elif grep -q '"mode"[[:space:]]*:[[:space:]]*"auto"' ".sdd/autonomy.json" 2>/dev/null; then
    if [ -n "$cursor" ]; then
      printf '%s\n' '{"permission":"allow"}'
    fi
    exit 0
  fi
fi
deny "sdd-loop guardrail: blocked a tracker or wiki write. Writes need one of two authorizations. To approve this single action, go through the interactive Review Gate or review mode, which wraps the call in the transient .sdd/.approve-external sentinel. To run unattended, start an autonomous run with an explicit 'auto gates=...' invocation, which writes the .sdd/autonomy.json policy file this hook reads."
