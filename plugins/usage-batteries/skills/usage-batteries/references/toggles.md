# Toggles

Sentinels live in `USAGE_BATTERIES_HOME` (default `~/.claude/usage-batteries`). A `*-off` file means that meter or the labels are off. No file means on.

| Ask | Run from the plugin root |
|---|---|
| Session on/off | `sh "${CLAUDE_PLUGIN_ROOT}/scripts/usage-session-on.sh"` or `usage-session-off.sh` |
| Weekly on/off | `usage-weekly-on.sh` / `usage-weekly-off.sh` |
| Fable on/off | `usage-fable-on.sh` / `usage-fable-off.sh` |
| Labels on/off | `usage-labels-on.sh` / `usage-labels-off.sh` |
| Wire the status line | `usage-batteries-install.sh` |
| Remove this status line | `usage-batteries-install.sh --remove` |

After a toggle, tell the user which meters will show. Do not start unrelated work.

Install writes `statusLine` in `~/.claude/settings.json` only when that key is missing or already points at this plugin's wrapper. Pass `--force` only when the user asked to replace a foreign status line.
