---
name: architecture-decision-records
description: >-
  Use when a decision needs a durable ADR: status, supersedes, options, and
  consequences. Refuse until the reasoning holds. The SAD links ADRs; this
  skill writes them.
---

Author a **standalone ADR** for one decision. The Solutions Architecture Document **links** ADRs; it does not replace this skill.

Catalog patterns the SAD may still apply (ADR-001–007) live in the sibling `solutions-architecture-document/references/adrs.md`. This skill writes the record for *this* engagement's evidence.

Public ancestry (short-form ADR, MADR, Y-statement): `references/ancestry.md`. Templates: `references/templates.md`. Do not paste a book into the ADR.

SOW and envelope stay where they are. This skill writes decisions only.

## Refuse until reasoning holds

Do **not** write the file until every item below is true. Interview first. A request to "just write an ADR" or "pick option A" is incomplete.

1. **Context** names the force that makes the decision necessary now (constraint, RSCOP row, or explicit user fact).
2. **At least two options** exist, each with a real trade-off. A single option with a dummy alternative fails.
3. **The chosen option** is supported by *this* engagement's evidence, not habit or a prior project.
4. **Consequences** include both what becomes easier and what is accepted as cost (ops, test, SAD sections).
5. **Status** is one of Proposed, Accepted, Deprecated, Superseded, Rejected.
6. **Supersedes** is an existing ADR id, or `none`.

If any item is missing, ask. Stay refused.

## Path and numbering

Prefer the repo's existing ADR directory (`docs/adr/`, `docs/adrs/`, `adr/`). If none exists, write `docs/adr/NNNN-short-title.md` (zero-padded, next free number). Do not invent a second tree beside an existing one.

Title the file from the decision, not from a catalog pattern number. When the decision applies a SAD catalog pattern, cite that pattern id in **Related**.

## Choose a template

- **MADR-shaped** (default) — status, date, deciders, context, decision, options, consequences, related. Use `references/templates.md` § MADR.
- **Y-statement** — one paragraph for a small, local choice that still needs a record. Use `references/templates.md` § Y-statement. Promote to MADR when options or consequences grow.

Match field names in the template. Status is *this* engagement's status.

## After the file exists

- Point the SAD appendix at the file (path + one-line status). Do not recopy the ADR body into the SAD.
- If this ADR supersedes another, set the old file to **Superseded** and name the successor.
- Cite catalog IDs only when they exist in the current RSCOP (`O-E26`, `P-E1` as read latency). Leave a row **Open** when the evidence is Open.

## Easy mistakes

- A single option with a dummy alternative is not a decision.
- Inheriting Accepted from a prior project writes the wrong engagement's status.
- Recopying the ADR body into the SAD duplicates the record.

## Quality bar

- [ ] Reasoning checklist above holds
- [ ] File path matches the repo's ADR convention
- [ ] Status and supersedes are explicit
- [ ] Options are real; the selected option is marked
- [ ] Consequences name SAD / ops / test obligations
- [ ] No proper nouns from another engagement
- [ ] Ancestry is a link in `references/ancestry.md`, not a pasted chapter
