# Host overlays

Generic playbooks in this plugin do not assume a single agent host.
Read this file for host-specific command names and hook wiring.

## What is universal

- Gate label + assignee eligibility
- `gates=` mandatory, no default
- Sentinels (`.sdd/.approve-external`) and `.sdd/autonomy.json`
- Lite exclusions, green baseline, kill switches, Clarify Loop
- FR/AC IDs never renumber
- Independent review cap (two rounds)
- Merge rules; deploy is CI / out of this loop

## Claude Code (`extras/claude`)

Shipped: PreToolUse hooks (`Bash` + MCP write matchers) that run
`guard-git-push.sh` and `guard-external-writes.sh`, and an optional
bundled Atlassian MCP entry (`.mcp.json`).

Claude-only strings, if the user is on this host:

- Slash commands such as `/sdd`, `/sdd-init`, `/sdd-doctor`, `/sdd review`, `/sdd clarify`, `/sdd status`
- `/loop` as a batch driver (not a universal host feature)
- PreToolUse as the hook event name
- `${CLAUDE_PLUGIN_ROOT}` in hook commands

If no Atlassian tools work, mention the bundled MCP (or the client's
connector) as a Claude-host remedy. Do not mention `.mcp.json` on a host
that was never shipped that file.

## Cursor (`extras/cursor`)

Shipped: the same two guard scripts, invoked as `beforeShellExecution`
(shell / git / `gh` / `glab`) and `beforeMCPExecution` (tracker writes).
`preToolUse` matcher `Shell` is an additional path some Cursor versions
use; the push script accepts both payload shapes.

Cursor-only strings, if the user is on this host:

- Skills invoked by name (`sdd`, `sdd-init`, `sdd-doctor`, `sdd-clarify`, `sdd-analyze`, `sdd-constitution`, `sdd-converge`, `sdd-status`), not `/loop`
- Hook events `beforeShellExecution` / `beforeMCPExecution`
- Deny via JSON `{ "permission": "deny" }` as well as exit 2

Do not tell Cursor users to run `/loop` or to configure PreToolUse.
Do not nag about a missing `.mcp.json`. If hooks are not loaded in this
session, doctor reports **policy-only** (the playbooks still bind; the
fence is not mechanical).

## Hosts that cannot fence

If the host has no hook schema that can block shell or MCP, doctor
reports **policy-only**. Do not invent a hook file. Do not invent a
missing marketplace MCP config.

## Git forges (overlay notes, not fake CLIs)

Shipped matchers: `git`, `gh`, `glab`.

- **Origin** (Cursor-hosted git): same `git push` rules; no extra CLI.
- **Bitbucket**: use `git` plus the host's PR UI or a connected MCP.
  Do not invent a `bb` / `bitbucket` CLI in the guard scripts.

## Instruction files

Playbooks read `## SDD Scope` / `## Verification` from, in order:

1. `docs/sdd-scope.md` if that file exists
2. `AGENTS.md`
3. `CLAUDE.md`

Init writes the same sections to `AGENTS.md` and `CLAUDE.md` (create
either if missing). It may also write `docs/sdd-scope.md` when the user
wants a dedicated file. Never treat `CLAUDE.md` as the only kernel.
