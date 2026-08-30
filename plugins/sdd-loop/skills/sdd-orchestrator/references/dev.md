# Stage Playbook: Dev

Goal – implement the ticket against its spec, tests first. This playbook refuses to run without a spec.

## Entry Criteria (Check First, Hard Gate)
- A spec exists – a linked page, a repo file, or structured acceptance criteria on the ticket – with no material open questions in its Clarifications.
- Acceptance criteria are testable.
- A task plan exists (`tasks.md` from the Design stage). When spec and design arrived from outside the loop without one, derive it first per the design playbook's task-plan step – dependency-ordered, file-path-pinned, ID-cited – before writing any code.
- No materially unresolved design questions in the comments.
- Spec and design agree. Run a quick cross-artifact pass. Every acceptance criterion is covered by the design's test plan, and neither document contradicts the other or the constitution. Disagreement fails entry; return the ticket to the stage that owns the error rather than coding around it.

If any check fails, stop, report which criterion failed, and recommend returning to the Spec or Design stage. Do not write code against an unspecified ticket.

## Process
1. Create an isolated git worktree on a branch named `<ticket-key>-<short-description>`.
2. Work the task plan in dependency order, one task at a time. Per task, write its tests first, derived directly from the acceptance criteria and named (or comment-mapped) to their AC IDs; implement until they pass without breaking existing ones; then check the task off in `tasks.md` before moving on, so an interrupted run resumes at the first unchecked task.
3. Run the project's full verification – test suite, linting, and type checks. Use the commands recorded in `## Verification` (`docs/sdd-scope.md`, else `AGENTS.md`, else `CLAUDE.md`). If that section is absent, detect the commands from the repo and state the assumption in your summary.
4. Capture the verification evidence to `.sdd/evidence/<ticket-key>-dev-<ISO timestamp>.md`, recording the commands run, exit codes, raw output tails, the commit hash, and diff stats. Copy the tool output through verbatim, so the approver reads what the commands printed.
5. Keep the change minimal. Anything out of scope becomes a note for a follow-up ticket. Never write the extra code.
6. Independent review. Spawn a fresh-context subagent to review the final diff against the spec, with no access to your reasoning, prompted to find problems through three lenses.
   - **Correctness** – does the code do what the acceptance criteria say.
   - **Security** – injection, secrets, authz, unsafe input handling.
   - **Spec compliance** – requirements missed, non-goals violated, untested edges.

   Address its confirmed findings, then spawn one more fresh-context reviewer over the amended diff to verify the fixes and catch what they introduced. Cap the loop at two review rounds. Only correctness, security, and spec-compliance findings are mandatory fixes; style and speculative-robustness findings are optional notes. A reviewer told to find gaps always finds some, and chasing every one over-engineers the change. List disputed or accepted-risk findings in the summary rather than silently dropping them.

## Output (Local)
- The worktree with committed changes (local commits only).
- The updated `tasks.md`, with every task checked off.
- The evidence file in `.sdd/evidence/`.
- A summary covering what changed, diff stats, the AC-ID-to-test mapping, verification results, and any follow-up items discovered.

## Candidate External Actions (for the Review Gate)
- Push the branch to the remote.
- Create a pull request referencing the ticket. Its body carries the task checklist with completion state and the AC-ID-to-test mapping, so the reviewer sees the plan and its coverage where they review.
- Add a comment on the ticket with the summary and branch name.
- Transition the ticket (e.g. to In Review).

None of these run without explicit per-item approval.

## Quality Checks Before the Review Gate
- Every acceptance criterion has at least one passing test citing its AC ID.
- Every task in `tasks.md` is checked off, or explicitly moved to a follow-up note.
- Full suite, lint, and type checks pass in the worktree, with the evidence file written.
- No unrelated files changed.
- Independent review completed, and every finding is fixed, disputed with reasons, or explicitly accepted in the summary.
