---
name: sdd-clarify
description: >-
  Use when a ticket already has a spec and needs the Clarify Loop re-run
  without rewriting the spec body.
argument-hint: "<ticket-key>"
disable-model-invocation: true
---

Run the **Clarify Loop** only. The spec body stays; Clarifications and open questions move.

Playbook: `sdd-orchestrator/references/spec.md` § Clarify Loop. Orchestrator Safety Rules and Review Gate still bind.

1. Parse $ARGUMENTS for a ticket key. Resolve scope per Step 0. Eligibility: gate label + assignee.
2. Read `.sdd/work/<ticket-key>/spec.md` or the published spec. If none exists, recommend the spec stage instead of inventing a spec here.
3. Follow the Clarify Loop: self-resolution first, classify material vs minor, escalate by mode.
4. Write updates into **Clarifications** and the open-questions list. Edit an AC in place only when a clarification changes its wording; keep its ID.
5. Present the delta. Publishing is a Review Gate external action.

Also reachable as the `sdd` entry with `clarify`.

## Easy mistakes

- Inventing a spec here skips the spec stage.
- Rebuilding Problem / Goals / FR sections on a clarify pass loses stable IDs.
