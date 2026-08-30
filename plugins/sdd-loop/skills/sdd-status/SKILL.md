---
name: sdd-status
description: >-
  Use when a one-screen read of queue, inferred stage, GATES/PENDING/
  ATTENTION, and preflight is enough. Read-only.
argument-hint: "[site=<name>] [project=<KEY>,<KEY>]"
disable-model-invocation: true
---

Print the **status** screen and stop.

Playbook: `sdd-orchestrator/references/status.md`. Doctor remains the full health check (`sdd-doctor`).

1. Parse $ARGUMENTS for `site=` / `project=`. Resolve scope per orchestrator Step 0.
2. Follow `references/status.md`. No stage playbook, no ledger writes, no Review Gate.

Also reachable as the `sdd` entry with `status`.

## Gotchas

- Status is not doctor: no connector probe, no hook fence test.
- Status must not start a stage or approve a gate.
