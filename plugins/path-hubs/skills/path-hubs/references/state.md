# State

Default file: `~/.claude/path-hubs/state.json`. Override the directory with `PATH_HUBS_HOME`. Session scan root is `$HOME`, or `PATH_HUBS_SCAN_ROOT` in tests.

```json
{
  "version": 1,
  "autoLink": true,
  "hubs": {},
  "items": {}
}
```

Hub id prefers the git remote (`org/repo`), then the last two path parts. Items store `kind` (`chat`, `code`, `cowork`), `hubId`, `manual`, and `unlinked`.

Match order: a manual unlink stays unlinked; a manual hub id wins; otherwise cwd git root, then remote, then path prefix. When auto-link is on, a new git root becomes a hub.

Discover reads `~/.claude/projects/<encoded-cwd>/*.jsonl` as chats (cowork when the source says so) and file paths in those transcripts as Code items. Cursor `~/.cursor/projects/*/agent-transcripts/*.jsonl` counts as Code.
