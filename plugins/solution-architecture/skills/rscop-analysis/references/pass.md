# RSCOP pass

Run in order. SKILL.md holds the hard rule and the interface.

## Inputs

Gather all that exist; do not invent the rest.

| Input | What you extract | If missing |
|-------|------------------|------------|
| Scope of Work / contract draft | Stated commitments, out-of-scope items, delivery window, warranty, ownership | Mark affected rows **Open** |
| Discovery notes / intake call | Auth approach, roles, write vs read-only, UI baseline, named contacts, regulatory comments | Mark affected rows **Open** |
| Existing-stack notes | `{Source repo}`, `{Upstream system}`, packaging, CI, observability, cloud account, inherited SLOs | Mark affected rows **Open** |
| Defaults in `catalog.md` | Measurable baseline targets | Apply as **Default** and flag so `{Client}` can override |

If an input is missing, **mark the row Open**. Do not invent client facts, user counts, regulatory positions, deployment targets, or named people. Silence is not a "no" — it is an Open or a flagged Default. Silence does not enable ECS/Fargate, DAST-every-build, HIBP, or a regime.

**Assumed engagement class for Defaults:** small-to-medium web / SaaS application, and only after the envelope is A. Scale latency, availability, and capacity targets up when the source describes a larger or 24/7 system.

## Evidence categories

Keep these exact names. Use them as **divider rows** in every table (`| **Explicit** | | | |`, and so on).

| Category | Meaning | Lock status |
|----------|---------|-------------|
| **Explicit** | Stated by the client in a source | Locked |
| **Implied** | Inferred from the source; not said in so many words | Needs explicit confirmation |
| **Default** | Baseline applied because the source was silent | Must be flagged so the client can override |
| **Open** | Needs an answer; cannot be safely defaulted | Blocks a safe commitment |

1. If the source states a target or choice → **Explicit**. Use the client's number, not the catalog default.
2. If the source only hints → **Implied**. Write the inference and the confirmation needed.
3. If the source is silent and the starter catalog has a safe baseline → **Default**. Keep the catalog target. Flag it.
4. If the source is silent and a wrong guess would bind `{Client}` or transfer risk → **Open**.
5. Never promote Default → Explicit without a cited source sentence.

## Table format

Every dimension has **Client** and **Engineering** tables. Same columns:

```
| # | Requirement | What it means | Target |
|---|-------------|---------------|--------|
| **Explicit** | | | |
| X-C1 | … | … | … |
| **Implied** | | | |
| **Default (baseline applied — flag to client)** | | | |
| **Open (needs answer)** | | | |
```

Omit an empty evidence group. Group by evidence, not by ID. IDs stay stable once assigned.

Write targets as measurable statements (`At least 99.5%`, `At most 5 minutes`, `0 (zero)`, `100%`). Avoid "should" and "reasonable".

## ID scheme

| Dimension | Client | Engineering |
|-----------|--------|-------------|
| Reliability | `R-C#` | `R-E#` |
| Security | `S-C#` | `S-E#` |
| Cost | `C-C#` | `C-E#` |
| Operations | `O-C#` | `O-E#` |
| Performance | `P-C#` | `P-E#` |
| Trade-offs | `T#` | — |

Starter-catalog rows keep the IDs in `catalog.md`. Append project-specific rows with the next unused integer in that prefix. Do not renumber after regrouping.

## Catalog, Opens, and trade-offs

Copy every starter row from `catalog.md`. Classify each from the current sources (usually they stay **Default**). If the client stated a different target, promote that row to **Explicit** and replace the target.

Skip envelope-gated rows when the envelope is not web/SaaS.

After the starter catalog is in place, append **standard Open** rows the sources did not answer, then **project-specific Explicit / Implied** rows the sources actually support. Never bake a named company, person, repo, or product into this skill.

## Closing sections

### Decision

Write a short prose close (not a table):

1. What is **locked** (Explicit rows that change architecture or scope).
2. What remains **Open**, clustered.
3. Whether the analysis is ready to feed a Solutions Architecture Document, and which SAD sections can be authored now versus which are blocked.

Do not claim completeness when Open rows still bind risk. If O-E26 (deployment target) is Open, leave it Open or ask. Do not assume AWS ECS/Fargate.

### Document-Readiness Summary

```
| Status | Count | Examples |
|--------|-------|----------|
| Explicit (locked) | N | 2–4 current-run IDs |
| Default (baseline applied — flag to client) | N | 2–4 starter IDs |
| Implied (confirm before commitment) | N | 2–4 current-run IDs |
| Open (block requirements completion) | N | 2–4 current-run IDs |
```

Count every data row (not divider rows). **Status** line: one sentence on readiness to feed the SAD.

## Output skeleton

Write `docs/rscop-<project-slug>.md` (slug from the current project or `{Client}` short name; lowercase, hyphenated).

Skeleton: title, generated date, source, Framework RSCOP, project context (3–6 sentences, tokens only), how-to-read the four evidence categories, then Client/Engineering tables per dimension, trade-offs, Decision, Document-Readiness Summary.

### SAD handoff

| SAD area | RSCOP source |
|----------|----------------|
| Security Architecture | S-* |
| Infrastructure Architecture / recoverability | R-*, C-* |
| Solution Management (run) | O-*, R-E5, R-E6 |
| Solution Implementation (build) | O-E*, C-E* |
| Data / Application performance | P-* |
| Appendix — trade-off analyses | T* |

Do not author the SAD in this pass unless the user asked for both.

## Procedure

1. Confirm inputs. List what you have (SOW, notes, stack). List what you lack.
2. Ask the envelope question (`envelope.md`).
3. Draft **Project context** from this run only. Use the five tokens; never a prior-client name.
4. Copy the **starter catalog**. Classify each row. Override targets only when Explicit. Skip envelope-gated rows when not web/SaaS.
5. Append **standard Open** rows that the sources did not answer.
6. Append **project-specific Explicit / Implied** rows the sources actually support.
7. Fill the **trade-offs** table from the common catalog plus any this-run extras.
8. Write **Decision** and **Document-Readiness Summary** with real counts.
9. Save as `docs/rscop-<project-slug>.md`.
10. Sweep the output: no prior-client names, no invented facts, every row has a measurable target or a named Open owner. No overlay enabled from silence.

If the user asks only for a subset (e.g. Security), still apply evidence rules and IDs for that dimension; note that the other dimensions are not in this file.
