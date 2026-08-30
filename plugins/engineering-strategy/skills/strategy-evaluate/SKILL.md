---
name: strategy-evaluate
description: >-
  Use when an existing engineering strategy file needs a read: iterate
  speed, cost of the next test (especially across teams), and whether the
  current iteration addresses the diagnosis. Writes
  docs/<slug>-strategy-evaluate.md. Leaves the strategy file as-is.
---

Evaluate an **existing** strategy file. Do not invent a new strategy.

Playbook: sibling `engineering-strategy/references/evaluate.md`.

## Process

1. Load `docs/engineering-strategy.md` or `docs/<slug>-engineering-strategy.md`. If none exists, stop.
2. Answer the three questions in `references/evaluate.md`.
3. Verdict: hold / iterate / end / replace. Strategies age; ending or replacing one is allowed.
4. Write `docs/<slug>-strategy-evaluate.md`. Point at which section to reopen; do not rewrite the living doc here.

## Gotchas

- Rewriting the living doc in the evaluate file mixes verdict with draft.
- Hold/iterate without naming next-test cost skips the third question.
- Ending or replacing a strategy is allowed; treating every file as permanent is not.

## Quality bar

- [ ] The three questions are answered from the file
- [ ] Next-test cost is named (or marked missing)
- [ ] Verdict is explicit
- [ ] No new strategy body in this output
