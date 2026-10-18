# Notify overlays

`notify=` is optional. `jira` (or the active `tracker:` adapter's
comment surface) is always on as the approval surface.

## Labeled overlays (do not pretend extras exist)

- `notify=slack` — a DM or channel message via connected Slack tools,
  if any. This plugin ships no Slack extra. If no Slack tools are
  connected, log the skip to `AUDIT.md` and continue.
- `notify=push` — a desktop push where the client supports it. This
  plugin ships no push extra. If the client cannot send one, log the
  skip and continue.

Unknown channels fail the invocation. Delivery failure never blocks the
run beyond one attempt per event.
