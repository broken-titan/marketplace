---
name: path-hubs
description: >-
  Use when you need Chat and Code sessions grouped by git repo path,
  or to link, unlink, or toggle Path hubs auto-link.
---

# Path hubs

Commands: `references/commands.md`. Matching and state: `references/state.md`. Host limits: `references/limits.md`.

## Rules

1. Run `path-hubs.sh view` (or `/path-hubs`) and print that output; do not invent hubs, chats, or files.
2. Treat Chat and Code as the same hub tree; do not keep a second grouping for Code mode.
3. Put cowork sessions under Chats when the source or cwd is distinguishable as cowork.
4. When auto-match fails, use `/path-hubs-link` and `/path-hubs-unlink`; persist through the scripts.
5. Leave auto-link unchanged unless the user asked to toggle it.

## Easy mistakes

- Drawing a sidebar Claude cannot host; the command view and optional status line are the surfaces.
- Re-linking a manually unlinked item on discover.
- Mixing Chat and Code into one flat list under a hub.

## Quality standards

- [ ] View shows hubs with Chats and Code, plus Unlinked
- [ ] Auto-link state matches `~/.claude/path-hubs/state.json` (or `PATH_HUBS_HOME`)
- [ ] Manual link and unlink survive a later discover pass
