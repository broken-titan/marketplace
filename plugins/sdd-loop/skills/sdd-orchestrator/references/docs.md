# Stage Playbook: Docs

Goal – change documentation only. Same worktree, evidence, and Review
Gate rules as other repo-dependent stages. Deploy is not this stage.

## Entry

The ticket states which documents change and what they must convey. If
that is unclear, recommend the Spec stage for a lightweight outline
instead of guessing.

## Process

1. Isolated worktree, same branch naming as the dev playbook.
2. Edit only documentation files named in the ticket or the outline.
3. Verification is a docs build or link check where the
   `## Verification` section records one, plus a read-through against
   the ticket. If no docs command is recorded, the read-through is the
   suite; say so in the evidence file.
4. Capture evidence to `.sdd/evidence/<ticket-key>-docs-<ISO timestamp>.md`.
5. Independent review is one fresh-context pass against the ticket
   (correctness of the claims, not code security). Cap at one extra
   pass if that reviewer finds factual errors.

## Output

Worktree, evidence file, summary. Update `.sdd/work/<ticket-key>/trace.md`
if this ticket has FR/AC IDs (docs-only tickets may have none).

## Candidate External Actions

Push the branch, open a PR, comment on the ticket, transition if the
user wants. No production deploy.

## Quality Checks

- Only documentation paths changed.
- The ticket's "what they must convey" list is covered or listed as
  follow-up.
- Evidence file written.
