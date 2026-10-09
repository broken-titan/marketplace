---
name: sdd-converge
description: >-
  Use after verify when acceptance criteria are still uncovered and the
  ticket needs another dev pass until Converged.
argument-hint: "<ticket-key>"
disable-model-invocation: true
---

Run **converge** on a ticket that already has a verify pass.

Playbook: `sdd-orchestrator/references/converge.md`. Spec-side drift is evolve mode. Orchestrator Safety Rules, worktrees, and Review Gate still bind.

1. Parse $ARGUMENTS for a ticket key. Resolve scope per Step 0. Eligibility: gate label + assignee.
2. Follow `references/converge.md` until **Converged** or the remaining gaps are spec problems (then stop and point at clarify or evolve).
3. External push/PR/comment stay on the Review Gate.

Also reachable as the `sdd` entry with `converge`.

## Easy mistakes

- Converge appends tasks; it does not rewrite the spec. Spec drift is evolve.
- Running converge before a verify pass has no uncovered-AC evidence.
