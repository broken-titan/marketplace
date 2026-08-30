#!/bin/sh
# Unit tests for the sdd-loop guardrail hooks.
# Usage: sh hooks/test-hooks.sh   (from the plugin root, or anywhere)
# Exit 0 = all pass; nonzero = at least one failure (each printed).
#
# The hooks parse their input with jq when it is present and fall back to grep
# when it is not, so both branches need covering. Pass 1 runs the suite against
# whatever jq state the host happens to have. Pass 2 runs it again with jq
# masked out behind a shim PATH, which needs symlinks; on hosts without them
# it is skipped, and CI covers both.
set -u

HOOKS_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PUSH="$HOOKS_DIR/guard-git-push.sh"
WRITES="$HOOKS_DIR/guard-external-writes.sh"

WORK=$(mktemp -d)
trap 'cd / && rm -rf "$WORK"' EXIT
cd "$WORK" || exit 1

fails=0
total=0

payload() {
  printf '{"tool_name":"Bash","tool_input":{"command":"%s"}}' "$1"
}

# check_push <name> <expected-exit> <command-string>
check_push() {
  total=$((total + 1))
  payload "$3" | sh "$PUSH" >/dev/null 2>&1
  got=$?
  if [ "$got" -ne "$2" ]; then
    echo "FAIL: $1 (expected exit $2, got $got)"
    fails=$((fails + 1))
  fi
}

# check_writes <name> <expected-exit>
check_writes() {
  total=$((total + 1))
  printf '{}' | sh "$WRITES" >/dev/null 2>&1
  got=$?
  if [ "$got" -ne "$2" ]; then
    echo "FAIL: $1 (expected exit $2, got $got)"
    fails=$((fails + 1))
  fi
}

run_suite() {
  # --- no .sdd directory: hooks are inert ---
  rm -rf .sdd
  check_push "no .sdd: git push allowed" 0 "git push origin main"
  check_writes "no .sdd: jira write allowed" 0

  # --- bare .sdd (no sentinel, no policy): fail closed ---
  mkdir -p .sdd
  check_writes "bare .sdd: jira write blocked" 2
  check_push "bare .sdd: git push blocked" 2 "git push origin main"
  check_push "bare .sdd: gh pr create blocked" 2 "gh pr create --fill"
  check_push "bare .sdd: gh pr merge blocked" 2 "gh pr merge 1 --squash"
  check_push "bare .sdd: glab mr merge blocked" 2 "glab mr merge 1"
  check_push "bare .sdd: gh api blocked" 2 "gh api repos/o/r/pulls"
  check_push "bare .sdd: unrelated command allowed" 0 "ls -la"
  check_push "bare .sdd: liveness probe blocked" 2 "echo sdd-guard-probe git push"

  # --- per-item approval sentinel: the single approved call passes ---
  : > .sdd/.approve-external
  check_writes "sentinel: jira write allowed" 0
  check_push "sentinel: git push allowed" 0 "git push origin main"
  check_push "sentinel: force push allowed" 0 "git push --force origin feat-branch"
  check_push "sentinel: gh pr merge allowed" 0 "gh pr merge 1 --squash"
  check_push "sentinel: gh api allowed" 0 "gh api repos/o/r/pulls -f state=closed"
  rm -f .sdd/.approve-external

  # --- armed autonomous run with merge gated ---
  cat > .sdd/autonomy.json <<'EOF'
{"mode":"auto","gates":["merge"],"notify":["jira"],"scope":"project=TST","started":"2026-01-01T00:00:00Z","heartbeat":"2026-01-01T00:00:00Z"}
EOF
  check_writes "auto: jira write allowed" 0
  check_push "auto: git push allowed" 0 "git push -u origin feat-branch"
  check_push "auto: gh pr create allowed" 0 "gh pr create --fill"
  check_push "auto: push to main blocked" 2 "git push origin main"
  check_push "auto: push to master blocked" 2 "git push -u origin master"
  check_push "auto: force push blocked" 2 "git push --force origin feat-branch"
  check_push "auto: force-with-lease blocked" 2 "git push --force-with-lease origin feat-branch"
  check_push "auto, merge gated: merge blocked" 2 "gh pr merge 1 --squash"
  check_push "auto: gh api still blocked" 2 "gh api graphql -f query=q"

  # --- armed autonomous run with merge ungated ---
  cat > .sdd/autonomy.json <<'EOF'
{"mode":"auto","gates":["intake"],"notify":["jira"],"scope":"project=TST","started":"2026-01-01T00:00:00Z","heartbeat":"2026-01-01T00:00:00Z"}
EOF
  check_push "auto, merge ungated: merge allowed" 0 "gh pr merge 1 --squash"

  # --- policy file that is not an armed auto run: fail closed ---
  printf '{"mode":"batch","gates":[]}' > .sdd/autonomy.json
  check_writes "non-auto policy: jira write blocked" 2
  check_push "non-auto policy: push blocked" 2 "git push"

  # --- malformed policy file: fail closed ---
  printf 'not json at all' > .sdd/autonomy.json
  check_writes "malformed policy: jira write blocked" 2
  check_push "malformed policy: push blocked" 2 "git push"
  rm -f .sdd/autonomy.json
}

if command -v jq >/dev/null 2>&1; then
  echo "== pass 1: jq available =="
else
  echo "== pass 1: grep fallback (no jq on host) =="
fi
run_suite

# Second pass with jq masked out, where a shim PATH can be built.
if command -v jq >/dev/null 2>&1; then
  SHIM="$WORK/shim"
  mkdir -p "$SHIM"
  ok=1
  for t in sh cat grep rm mkdir; do
    p=$(command -v "$t" 2>/dev/null)
    case "$p" in
      /*) ln -s "$p" "$SHIM/$t" 2>/dev/null || ok=0 ;;
      *) ok=0 ;;
    esac
    [ "$ok" -eq 1 ] || break
  done
  if [ "$ok" -eq 1 ]; then
    echo "== pass 2: grep fallback (jq shimmed out) =="
    OLDPATH=$PATH
    PATH="$SHIM"
    run_suite
    PATH=$OLDPATH
  else
    echo "== pass 2 skipped: cannot build shim PATH on this host =="
  fi
fi

echo "$((total - fails))/$total passed"
[ "$fails" -eq 0 ] || exit 1
