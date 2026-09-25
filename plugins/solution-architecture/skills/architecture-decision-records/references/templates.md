# ADR templates

Copy the chosen shape into the file. Fill every field. Leave no placeholder braces in the published record.

## MADR-shaped

```markdown
# NNNN. {Title}

- Status: Proposed | Accepted | Deprecated | Superseded | Rejected
- Date: YYYY-MM-DD
- Deciders: {who must live with this}
- Supersedes: {NNNN or none}

## Context

Why this decision exists now. Cite the constraint, RSCOP row, or named fact.

## Decision drivers

- {force}
- {force}

## Options

### {Option A}

{one-paragraph trade-off}

### {Option B}

{one-paragraph trade-off}

## Decision

{The choice, one short paragraph. Mark the selected option by name.}

## Consequences

### Good

- {what becomes easier}

### Accepted

- {cost, ops, test, or SAD-section obligation}

## Confirmation

How we will know the decision is in force (test, review, SAD view).

## Related

- SAD: `docs/sad-<slug>.md` (link only)
- RSCOP rows: {IDs or none}
- Other ADRs: {ids this informs, depends on, or supersedes}
```

## Y-statement

Use when the choice is local and the options fit one paragraph. If a second paragraph of options appears, switch to MADR.

```markdown
# NNNN. {Title}

- Status: Proposed | Accepted | Deprecated | Superseded | Rejected
- Date: YYYY-MM-DD
- Deciders: {who}
- Supersedes: {NNNN or none}

In the context of {context}, facing {force}, we decided for {option} to achieve {quality}, accepting {downside}.

## Related

- SAD: `docs/sad-<slug>.md`
- RSCOP rows: {IDs or none}
```
