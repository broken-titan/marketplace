# Evaluate an existing strategy

Read a living strategy file. Do **not** invent a replacement strategy here. Ending or replacing one is allowed; say so and stop, or hand the user to `engineering-strategy` / `strategy-explore` for the next pass.

## Load

`docs/engineering-strategy.md` or `docs/<slug>-engineering-strategy.md`. If none exists, stop.

## Three questions

Answer each with evidence from that file (and the repo it links). Missing evidence is an answer.

1. **Iterate speed** — How quickly can this strategy be changed once reality moves? Look for a review cadence, a written exception path, and whether policies are specific enough to edit without a rewrite.
2. **Cost of the next test** — How expensive is the next trial, especially across teams? A cheap test on one module is cheap. Org-wide pressure with no trial is expensive. Name the next test or say it is missing.
3. **Fit to diagnosis** — Does the current iteration actually address the stated diagnoses? A policy that does not map to a `D-n`, or a diagnosis the policies never touch, is a miss.

## Age

Strategies age. A file that still fits last year’s diagnosis and last year’s landscape can be **ended** or **replaced**. Record that verdict. Do not keep a stale file In force out of habit.

## Output

`docs/<slug>-strategy-evaluate.md`:

- File evaluated (path, status, date)
- Answers to the three questions
- Verdict: hold / iterate / end / replace
- If iterate or replace: which section (policy, operations, refine, diagnosis, explore) to reopen — not a new strategy written here
