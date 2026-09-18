---
name: sdd
description: >-
  Use when running the spec-driven ticket loop: help, a ticket key, intake,
  batch, auto, review, evolve, stop, or the aliases specify / plan /
  implement / bug. Entry for interactive, batch, and autonomous modes.
argument-hint: "[help | ticket-key | intake <file.md> | batch | auto gates=<list|none> | review | evolve <ticket-key> | stop | clarify | analyze | constitution | converge | status | specify | plan | implement | bug] [site=<name>] [project=<KEY>,<KEY>] [parent=<KEY>] [stage=<stage>] [notify=jira,slack,push] [preflight=override]"
disable-model-invocation: true
---

Use the sdd-orchestrator skill. Parse $ARGUMENTS, then resolve scope per the orchestrator's Step 0.

Host command names live in `sdd-orchestrator/references/hosts.md`. Do not treat `/loop` or PreToolUse as universal.

`sdd` stays the entry point. The skills `sdd-clarify`, `sdd-analyze`, `sdd-constitution`, `sdd-converge`, and `sdd-status` are also directly invocable.

Match the modes below in order.

- **"help"** — usage reference only. Eligibility, command forms, aliases (`clarify` / `analyze` / `constitution` / `converge` / `status`; `specify`≈`stage=spec`, `plan`≈`stage=design`, `implement`≈`stage=dev`, `bug`≈`stage=bug`), gate names, kill switches. Point at this plugin's docs and `https://github.com/broken-titan/marketplace`. Keep it to a screenful.
- **"auto"** — Autonomous Mode (`references/autonomous.md`). Requires `gates=`, resolved scope, and a passing preflight (or `preflight=override`). No default gate set. `notify=slack` / `notify=push` are overlays (`references/notify.md`).
- **"stop"** — finish the current atomic action, write the run summary, delete `.sdd/autonomy.json`.
- **"review"** — OPEN entries from `.sdd/PENDING-ACTIONS.md` and `.sdd/GATES.md`; execute only approved IDs.
- **"evolve"** with a ticket key — verify playbook in drift-only mode.
- **"clarify"** / **"analyze"** / **"constitution"** / **"converge"** / **"status"** — the matching invocable skill.
- **"specify"** / **"plan"** / **"implement"** / **"bug"** — `stage=spec` / `design` / `dev` / `bug`.
- **"intake"** with a file or inline requirements — Direct Intake. `parent=<KEY>` optional.
- **Ticket key** — interactive mode. `stage=` pins the stage.
- **"batch"** — Batch Mode. Scoped queue, zero external writes. A host-specific loop driver is an overlay in `references/hosts.md`.
- **Otherwise** — interactive pick.

Follow the orchestrator exactly, including Review Gate rules. Interactive and review: no external action without per-item approval. Autonomous: the declared gate policy is the approval boundary.

## Easy mistakes

- `/loop` and PreToolUse are host overlays, not the contract.
- `auto` without `gates=` must refuse.
- Flattening the five invocable skills into this file loses those surfaces.
