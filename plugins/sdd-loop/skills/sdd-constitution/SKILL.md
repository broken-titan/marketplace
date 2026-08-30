---
name: sdd-constitution
description: >-
  Use when amending the project constitution after init. Leaves tracker
  scope and verification commands as they are.
argument-hint: "[path]"
disable-model-invocation: true
---

Amend the project constitution only.

Playbook: `sdd-orchestrator/references/constitution.md`. First draft during enablement remains `sdd-init`.

1. Do not run tracker lookup, verification discovery, or sdd-doctor.
2. Follow `references/constitution.md`. Preview the diff; write on confirmation.
3. If $ARGUMENTS names a path, use it when it is already the recorded constitution or the user is relocating that file.

Also reachable as the `sdd` entry with `constitution`.

## Gotchas

- Re-running init to change a principle also rewrites scope and verification.
- The constitution lives in the repo, never in `.sdd/`.
