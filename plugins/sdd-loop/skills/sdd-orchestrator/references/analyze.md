# Cross-artifact analyze (read-only gate)

Goal – one read-only pass across spec, design, tasks, and code. This is a **gate**. It reports. It does not create tracker tickets, publish specs, or open PRs.

Invocable as `sdd-analyze` or `/sdd analyze`. Complements the consistency paragraphs in `design.md` and `dev.md`; run those in-stage as well. This file is the standalone pass.

## Entry

Resolve the ticket (argument key, or ask). Eligibility: gate label + assignee, same as the orchestrator. Reads are always allowed.

Need at least a spec (or Lite combined doc) and whatever else exists. Missing design, tasks, or code is a finding, not a crash.

## Pass (read-only)

Open, do not write:

- `.sdd/work/<ticket-key>/spec.md` (or `lite.md`)
- `design.md`, `tasks.md` when present
- `verify.md`, `trace.md` when present
- The constitution (`constitution:` path, else `docs/sdd-constitution.md` / `CONSTITUTION.md`)
- The implementation (linked branch, PR, or worktree) when it exists

Check, in order:

1. **IDs.** Every FR/AC from intake still exists; nothing was renumbered. `trace.md` rows match, or the gap is listed.
2. **Spec ↔ design.** Every AC is in the design test plan. The design asks for nothing the spec does not. Constitution conflicts are findings.
3. **Design ↔ tasks.** Every AC has a task. Every task cites IDs and real paths.
4. **Tasks ↔ code.** When code exists, each checked task matches the tree; unchecked tasks that already landed are findings.
5. **Code ↔ spec.** Behavior the spec forbids, or ACs with no test name, are findings. Do not run Evolve; only report.

## Output

Write `.sdd/work/<ticket-key>/analyze.md` locally: verdict **PASS** or **FAIL**, the finding list (artifact, id, what disagrees), and which stage owns each fix.

Do **not** append tracker tickets, pending-actions for issue creation, or comments. The user decides what to file.

## Gate

- **PASS** – no material disagreement. Later stages may proceed.
- **FAIL** – return to the stage that owns the first material finding (spec, design, or dev). Do not implement around it.

Batch / autonomous: a FAIL parks ATTENTION with this file as evidence. Interactive: present the list and wait.
