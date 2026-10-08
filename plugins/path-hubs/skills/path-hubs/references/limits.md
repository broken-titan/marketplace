# API limits

Claude Code does not give plugins a session-list sidebar or a way to replace Chat/Code chrome. `usage-batteries` in this family hit the same wall and used `statusLine`. Official plugin settings accept `agent` and `subagentStatusLine` only.

This plugin ships the 2a grouping on the surfaces that exist:

1. `/path-hubs` text tree plus a Claude-themed HTML view (`view.html`).
2. `SessionStart` auto-link of the current cwd when the toggle is on.
3. Optional user `statusLine` pointing at `scripts/statusline.sh`.

It cannot inject Path hubs into Claude's own left rail. Wire the status line in `~/.claude/settings.json` if you want the compact `2a · hub · chats · code` row:

```json
{
  "statusLine": {
    "type": "command",
    "command": "sh ${CLAUDE_PLUGIN_ROOT}/scripts/statusline.sh"
  }
}
```

`${CLAUDE_PLUGIN_ROOT}` is set while the plugin is enabled; a copied absolute path also works.
