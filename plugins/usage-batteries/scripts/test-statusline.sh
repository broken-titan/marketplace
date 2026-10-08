#!/bin/sh
# Unit tests for usage-batteries render and toggles.
set -u

SCRIPTS=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PY="$SCRIPTS/usage_batteries.py"
RENDER="python3 $PY render"

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
export USAGE_BATTERIES_HOME="$WORK/home"
export CLAUDE_CONFIG_HOME="$WORK/claude"
mkdir -p "$USAGE_BATTERIES_HOME" "$CLAUDE_CONFIG_HOME"

fails=0
total=0

payload() {
  python3 -c 'import json,sys; print(json.dumps(json.loads(sys.argv[1])))' "$1"
}

plain() {
  python3 -c 'import sys; from usage_batteries import strip_ansi; print(strip_ansi(sys.stdin.read()), end="")' 
}

check() {
  total=$((total + 1))
  name=$1
  shift
  if "$@"; then
    return 0
  fi
  echo "FAIL: $name"
  fails=$((fails + 1))
}

cd "$SCRIPTS" || exit 1

THREE='{"rate_limits":{"five_hour":{"used_percentage":20},"seven_day":{"used_percentage":55},"fable":{"used_percentage":92}}}'
SCOPED='{"rate_limits":{"five_hour":{"used_percentage":10},"seven_day":{"used_percentage":40},"model_scoped":[{"scope":{"model":{"display_name":"Fable"}},"used_percentage":70}]}}'
NONE='{"model":{"display_name":"Opus"}}'

out=$(payload "$THREE" | $RENDER)
text=$(printf '%s' "$out" | plain)

check "remaining 20 used -> 80 fill cells" \
  python3 -c "import sys; sys.exit(0 if sys.argv[1].count('█')==5+3+0 else 1)" "$text"
# 80% of 6 = 4.8 -> 5; 45% of 6 = 2.7 -> 3; 8% of 6 = 0.48 -> 0

check "has S W F labels" \
  python3 -c "import sys; t=sys.argv[1]; sys.exit(0 if t.count('S') and t.count('W') and t.count('F') else 1)" "$text"

check "no vertical battery emoji" \
  python3 -c "import sys; sys.exit(0 if '🔋' not in sys.argv[1] else 1)" "$text"

check "nub is on the right of each cell" \
  python3 -c "import sys,re; t=sys.argv[1]; sys.exit(0 if t.count(']▏')==3 else 1)" "$text"

check "green for plenty remaining" \
  python3 -c "import sys; sys.exit(0 if '\033[38;5;114m' in sys.argv[1] else 1)" "$out"

check "amber for mid remaining" \
  python3 -c "import sys; sys.exit(0 if '\033[38;5;214m' in sys.argv[1] else 1)" "$out"

check "red for low remaining" \
  python3 -c "import sys; sys.exit(0 if '\033[38;5;167m' in sys.argv[1] else 1)" "$out"

python3 "$PY" fable-off >/dev/null
two=$(payload "$THREE" | $RENDER | plain)
check "fable off shrinks to S W" \
  python3 -c "import sys; t=sys.argv[1]; sys.exit(0 if t.count('S') and t.count('W') and 'F' not in t and t.count(']▏')==2 else 1)" "$two"

python3 "$PY" weekly-off >/dev/null
one=$(payload "$THREE" | $RENDER | plain)
check "weekly off shrinks to S" \
  python3 -c "import sys; t=sys.argv[1]; sys.exit(0 if t.strip().startswith('S') and 'W' not in t and t.count(']▏')==1 else 1)" "$one"

python3 "$PY" session-off >/dev/null
empty=$(payload "$THREE" | $RENDER | plain)
check "all meters off prints nothing" \
  python3 -c "import sys; sys.exit(0 if sys.argv[1]=='' else 1)" "$empty"

python3 "$PY" session-on >/dev/null
python3 "$PY" weekly-on >/dev/null
python3 "$PY" fable-on >/dev/null
python3 "$PY" labels-off >/dev/null
nolabels=$(payload "$THREE" | $RENDER | plain)
check "labels off keeps three cells and drops letters" \
  python3 -c "import sys; t=sys.argv[1]; sys.exit(0 if t.count(']▏')==3 and 'S' not in t and 'W' not in t and 'F' not in t else 1)" "$nolabels"

python3 "$PY" labels-on >/dev/null
check "toggles persist across a new process" \
  python3 -c "import os,sys; sys.path.insert(0,'.'); from usage_batteries import meter_enabled; sys.exit(0 if meter_enabled('session') and meter_enabled('labels') else 1)"

missing=$(payload "$NONE" | $RENDER | plain)
check "missing rate_limits omits the cluster" \
  python3 -c "import sys; sys.exit(0 if sys.argv[1]=='' else 1)" "$missing"

scoped=$(payload "$SCOPED" | $RENDER | plain)
check "model_scoped Fable window is read" \
  python3 -c "import sys; t=sys.argv[1]; sys.exit(0 if t.count('F') and t.count(']▏')==3 else 1)" "$scoped"

check "remaining helper is 100 minus used" \
  python3 -c "from usage_batteries import remaining_from_used; assert remaining_from_used(0)==100; assert remaining_from_used(100)==0; assert remaining_from_used(37)==63; assert remaining_from_used(-5)==100; assert remaining_from_used(140)==0"

python3 "$PY" install >/dev/null
check "install writes settings and wrapper" \
  python3 -c "import json,os,sys; from pathlib import Path; home=Path(os.environ['USAGE_BATTERIES_HOME']); p=Path(os.environ['CLAUDE_CONFIG_HOME'])/'settings.json'; d=json.loads(p.read_text()); cmd=d['statusLine']['command']; sys.exit(0 if cmd==str(home/'statusline.sh') and 'usage_batteries.py' in Path(cmd).read_text() else 1)"

printf '%s\n' '{"statusLine":{"type":"command","command":"~/mine.sh"}}' > "$CLAUDE_CONFIG_HOME/settings.json"
python3 "$PY" install >/dev/null
check "install leaves a foreign status line" \
  python3 -c "import json,os,sys; from pathlib import Path; d=json.loads((Path(os.environ['CLAUDE_CONFIG_HOME'])/'settings.json').read_text()); sys.exit(0 if d['statusLine']['command']=='~/mine.sh' else 1)"

python3 "$PY" install --force >/dev/null
check "install --force replaces a foreign status line" \
  python3 -c "import json,os,sys; from pathlib import Path; home=Path(os.environ['USAGE_BATTERIES_HOME']); d=json.loads((Path(os.environ['CLAUDE_CONFIG_HOME'])/'settings.json').read_text()); sys.exit(0 if d['statusLine']['command']==str(home/'statusline.sh') else 1)"

html=$(python3 "$PY" preview html)
check "html preview is horizontal cells with nubs" \
  python3 -c "import sys; t=sys.argv[1]; sys.exit(0 if t.count('cell-wrap')>=7 and '🔋' not in t else 1)" "$html"

if [ "$fails" -ne 0 ]; then
  echo "$fails failed of $total"
  exit 1
fi
echo "ok: $total tests"
