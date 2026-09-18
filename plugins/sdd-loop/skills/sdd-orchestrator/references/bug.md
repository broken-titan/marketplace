# Stage Playbook: Bug

Goal – pin a defect so a later spec/dev/verify cycle can close it. Optional stage, same plugin. Pin with `stage=bug` or `/sdd bug`.

## Entry

A ticket (or inline report) names something broken. If the ask is a new feature, use intake / spec instead.

## Capture

Write `.sdd/work/<ticket-key>/bug.md` with three blocks, all required:

1. **Current** — what happens now, with evidence (command, screenshot path, log line, commit).
2. **Expected** — what the spec or user says should happen. Cite an AC ID when one exists; otherwise draft a candidate AC and mark it new.
3. **Unchanged** — neighbor behavior that must stay the same (regression fence).

Then list **regression tests** to add: each maps to Expected or Unchanged, named so verify can cite it.

Stable IDs: reuse an existing AC when the bug is a miss on that criterion. A truly new contract gets the next free FR/AC number; never renumber.

## Next

Route to **spec** when Expected needs a contract change, else to **dev** when the spec already forbids Current. Verify must run the new regression tests before merge.

## Quality

- Current and Expected disagree on a factual outcome, not a taste note.
- Unchanged is non-empty.
- At least one regression test is named.
