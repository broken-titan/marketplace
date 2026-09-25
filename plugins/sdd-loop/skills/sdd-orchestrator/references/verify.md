# Stage Playbook: Verify

Goal – validate existing work against the ticket's spec and acceptance criteria, and close test gaps.

## Definition of done (this loop)

This is the only DoD for a ticket this loop owns. Merge is last. Deploy is CI / out of loop (labeled; do not treat deploy as a stage).

A ticket is done when all of the following hold:

- Every AC ID from intake (reused in the spec) appears exactly once in the traceability matrix.
- `.sdd/work/<ticket-key>/trace.md` is bidirectional: intake ID ↔ spec ID ↔ verify evidence (test name or UNCOVERED-then-added). Merge is blocked if this file is missing or an AC has no row.
- The recorded verification commands passed in the worktree, with an evidence file, or the ticket is docs-only per `references/docs.md`.
- Drift check completed (or "no drift found").
- Independent review cap from the dev playbook was already applied if this ticket went through dev; verify does not add a third review round.
- External publish/push/PR/merge still go through the Review Gate or the declared autonomous gates.

Deploy, release, and production rollout are not in this list.

## Process
1. Locate the implementation in a linked branch, PR, or commits referenced on the ticket. If none can be found, stop and ask the user where the work lives.
2. Retrieve the spec or acceptance criteria. If none exist, verification has no contract to check against, so report that and recommend the Spec stage.
3. Check out the work in an isolated worktree.
4. Build the traceability matrix, keyed on AC IDs. Each acceptance criterion, by its ID, maps to the test(s) covering it, or marked UNCOVERED. If the spec predates the ID convention, assign IDs as part of the drafted spec correction.
5. Run the full suite, lint, and type checks using the repo `## Verification` commands from `docs/sdd-scope.md`, else `AGENTS.md`, else `CLAUDE.md` (detect them and state your assumptions if the section is absent). Record the results, and capture the evidence to `.sdd/evidence/<ticket-key>-verify-<ISO timestamp>.md`, recording commands, exit codes, raw output tails, and the commit hash. Copy the tool output through verbatim, so the approver reads what the commands printed.
6. For each UNCOVERED criterion, write the missing test in the worktree.
7. Manually review the diff against the spec for behavior the tests cannot catch – error messages, edge-case handling, non-goals violated.
8. Drift Check. Compare the spec against what the code actually does today, in both directions.
   - **Spec-ahead drift** – requirements the code never implemented.
   - **Code-ahead drift** – behavior the code has that the spec never mentions.

   For each divergence, decide which side is right and draft the fix – a spec update when the reality is intentional, a code defect entry when the spec is the contract. In Evolve Mode (`/sdd evolve <ticket-key>`), run ONLY this step plus the report.

## Output (Local)
Write `.sdd/work/<ticket-key>/verify.md` containing the traceability matrix, suite results, new tests added, the drift report (or "no drift found"), and a verdict of passes spec, passes with gaps (listed), or fails (with the failing criteria). Fill the verify column of `.sdd/work/<ticket-key>/trace.md`. The evidence file in `.sdd/evidence/` backs the suite-results claims.

## Candidate External Actions (for the Review Gate)
- Push the branch with the added tests.
- Comment the verification report on the ticket or PR.
- Update the published spec with approved drift corrections.
- Transition the ticket if the user considers the verdict sufficient.

## Quality Checks Before the Review Gate
- Every acceptance criterion appears exactly once in the matrix, keyed by its AC ID.
- The verdict is justified only by evidence in the report, never by assumption.

Uncovered ACs after this pass: `sdd-converge` / `/sdd converge` appends tasks and requires another dev pass until Converged. Spec-side drift stays `evolve`.
