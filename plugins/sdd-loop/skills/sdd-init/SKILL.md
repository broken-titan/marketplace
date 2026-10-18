---
name: sdd-init
description: >-
  Use when enabling spec-driven development in the current repo. Writes SDD
  Scope and Verification to agent-instruction files (AGENTS.md, CLAUDE.md,
  or similar) or docs/sdd-scope.md, then runs the health check.
argument-hint: "[site=<name>] [project=<KEY>,<KEY>]"
disable-model-invocation: true
---

Enable the loop in this repository. Procedure: `references/init.md`. Host overlays: `sdd-orchestrator/references/hosts.md`. Trackers: `sdd-orchestrator/references/trackers.md`.

Write local files only, except one explicitly approved bootstrap of a missing tracker project.

## Interface

| Field | Shape |
|-------|--------|
| Scope home | `docs/sdd-scope.md` first when present; else agent-instruction files (`AGENTS.md`, `CLAUDE.md`, or similar) |
| Tracker | `jira` default; Linear / GitHub Issues only when named |
| Gate label | `ai-allowed` unless the user sets `label:` |
| Output | `## SDD Scope` + `## Verification`; constitution in-repo, never in `.sdd/` |

## Easy mistakes

- Mentioning a bundled MCP on a host that never shipped one reads as a to-do.
- Enabling Linear or GitHub Issues from silence is wrong; they are overlays.
- A guessed project key without confirmation is not scope.
- Writing the constitution into `.sdd/` loses it and skips the preflight home.
- `/loop` is a host overlay, not a universal switch.

## Quality bar

- [ ] Instruction-file pattern used, not a single-vendor target
- [ ] Scope confirmed, not guessed
- [ ] Verification commands recorded or marked `none`
- [ ] `.sdd/` gitignored
- [ ] Doctor checks ran in place
