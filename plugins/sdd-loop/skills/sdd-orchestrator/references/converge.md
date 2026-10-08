# Converge (after verify)

Goal – after a verify pass, close uncovered acceptance criteria by **appending tasks** and requiring another **dev** pass, repeating until the ticket is **Converged**.

Invocable as `sdd-converge` or `/sdd converge`. Complements **evolve** (`/sdd evolve`): evolve is spec-side drift; converge is task/dev-side coverage.

## Entry

A verify artifact exists (`.sdd/work/<ticket-key>/verify.md`) with a matrix keyed on AC IDs. If verify has not run, run or recommend the verify playbook first.

Eligibility and Review Gate rules are the orchestrator's.

## Process

1. Read `verify.md` and `trace.md`. Collect every AC marked UNCOVERED, or whose verify evidence is missing.
2. If that set is empty **and** the suite passed: mark the ticket **Converged** in `verify.md` (one line, dated) and stop.
3. Otherwise append tasks to `.sdd/work/<ticket-key>/tasks.md` — one task per uncovered AC (or a tight group that shares a file), file-path-pinned, citing that AC ID. Do not renumber existing tasks; add after the last.
4. Require a **dev** pass on the new tasks only (dev playbook: tests first, evidence, independent review cap already consumed stays consumed).
5. Re-run **verify** on the new evidence.
6. Repeat 1–5 until every AC has a verify row with evidence and the suite is green.

A requirements problem (wrong or missing AC) is **not** converge work. Send that to the spec (Clarify or evolve). Converge only covers ACs the spec already owns.

## Output

Updated `tasks.md`, the extra dev evidence, an updated `verify.md` / `trace.md`, and a verdict of **Converged** or **still uncovered** (list remaining AC IDs).

External push/PR/comment still go through the Review Gate.

## Quality

- No new tracker tickets for uncovered ACs; tasks stay on this ticket.
- FR/AC IDs are unchanged.
- Evolve is offered only when the spec is the side that drifted.
