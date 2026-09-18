---
name: sdd-analyze
description: >-
  Use when a ticket needs a read-only cross-artifact gate across spec,
  design, tasks, and code. Leaves tracker tickets untouched.
argument-hint: "<ticket-key>"
disable-model-invocation: true
---

Run the **analyze** gate. Read-only toward the tracker.

Playbook: `sdd-orchestrator/references/analyze.md`. Orchestrator Safety Rules bind. No Review Gate writes.

1. Parse $ARGUMENTS for a ticket key. Resolve scope per Step 0. Eligibility: gate label + assignee.
2. Follow `references/analyze.md` exactly. Local output is `.sdd/work/<ticket-key>/analyze.md`.
3. Stop after the verdict. Do not create issues, comments, or pending-actions for ticket writes.

Also reachable as the `sdd` entry with `analyze`.

## Easy mistakes

- A FAIL that opens tracker tickets is no longer read-only.
- Analyze does not replace verify; it does not merge.
