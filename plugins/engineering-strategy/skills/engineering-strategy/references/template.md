# Living strategy — file shape

Write in five-step order (explore → diagnose → refine → policy → operations). **Publish in reader order** so someone looking for what to do hits policy first. Keep diagnosis and exploration in this same file.

```markdown
# Engineering strategy{optional: : <slug>}

- Status: Draft | In force
- Updated: YYYY-MM-DD
- Owner: {role or name}
- Sign-off: {human, date — omit until signed}
- Refine: test | map | model | both | skipped (short internal loop — <reason>)

## Guiding policies

### P1. {name}

- Tradeoff: {what we accept}
- Diagnoses: D1, …
- Statement: {the rule}
- Actions: {links to specs, architecture decisions, living design docs}

### P2. …

## Operations

| Policy | Inspect | Exception | Cadence |
|--------|---------|-----------|---------|
| P1 | | | |

## Refinement

{link to docs/<slug>-strategy-refine.md, or "skipped: short internal loop — <reason>"}

Cheap test: {path or one-line result | none — stay Draft}

## Diagnosis

### D1. {short name}

{theory}

Perspectives: …

Data: {link | missing}

### D2. …

## Exploration

{constraints, alternatives, implicit strategy, with repo paths}

## Links

- Specs: …
- Architecture decisions: …
- Living design docs: …
- Sibling artifacts: explore / diagnosis / refine / operations / evaluate paths when they exist
```

No opening vision. Useful and short.

**In force** only after a named human signs off **and** a cheap test exists (or refine was skipped as a short internal loop). Otherwise stay **Draft**.
