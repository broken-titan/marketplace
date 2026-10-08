# Meters

| Badge | Meaning | Payload |
|---|---|---|
| S | Session limit | `rate_limits.five_hour.used_percentage` |
| W | Weekly all models | `rate_limits.seven_day.used_percentage` |
| F | Weekly Fable | A Fable / model-scoped weekly window when present |

`remaining = clamp(100 - used, 0, 100)`. Color the fill from remaining: green at 50 or above, amber from 20 up to 49, red below 20.

`rate_limits` is absent for non-subscribers and before the first API response. Each window may be missing on its own. Skip that battery.

Weekly Fable is not in the documented status-line schema (`five_hour`, `seven_day` only). Read it when stdin (or `USAGE_BATTERIES_HOME/fable-used`) carries a Fable or `model_scoped` / `weekly_scoped` window. Do not call the OAuth usage API or read credentials. If Fable is on but no window exists, drop F and shrink the cluster.

Claude Code plugins cannot declare the primary `statusLine` in the manifest. Plugin `settings.json` accepts `subagentStatusLine` only. The hook writes a stable wrapper at `~/.claude/usage-batteries/statusline.sh` because `${CLAUDE_PLUGIN_ROOT}` is not expanded for `statusLine.command`.
