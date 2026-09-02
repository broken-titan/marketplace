# Tracker adapters

`tracker:` under `## SDD Scope` is a data field. It names the adapter.
It is not the type system.

**Default adapter: Jira.** If `tracker:` is omitted, use Jira. The loop
is the same on every adapter: gate label, assignee, comments, discovered
transitions.

## Jira (default)

- Search: `assignee = currentUser() AND labels = "<gate-label>" AND statusCategory != Done` plus the resolved project clause.
- Writes: comments, edits, transitions, issue create, links. Confluence
  publish is a separate `spec-storage:` choice.
- Identity: the connector's current-user call.
- Tools: only if a Jira/Atlassian connector is connected. Do not assume
  MCP tool names exist on every host.

## Overlay: Linear

Load only when `tracker: linear`.

Same loop: gate label (or Linear label), assignee, comments, discovered
state transitions. Map Jira words in the playbooks to Linear issue,
project, and comment. Do not invent Jira fields on Linear issues.

## Overlay: GitHub Issues

Load only when `tracker: github-issues`.

Same loop: gate label, assignee, comments, discovered state
(open / closed). Project boards and milestones are not this overlay
unless the ticket already uses them. `gh` is the CLI already in the
push guard; issue writes still go through the Review Gate / sentinel.

Silence does not enable Linear or GitHub Issues. Direct intake
(`intake <file.md>` or inline requirements) already exists and does
not require a tracker for the source document.
