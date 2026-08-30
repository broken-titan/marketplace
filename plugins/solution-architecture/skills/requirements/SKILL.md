---
name: requirements
description: >-
  Use when starting a feature or when a living spec needs updating from new
  feedback. Draft a numbered FR-*/NFR-* spec; a human signs off.
---

Produces the **living spec**: the durable, human-signed artifact later work flows from. Feature-level. RSCOP and the SAD are engagement-level. They are not two sources of truth. Paths: sibling `rscop-analysis/references/artifacts.md`.

Each requirement has: **ID**, **statement**, **source**, **verification method**. Stable IDs are never reused. A dropped requirement leaves a gap marked "removed". ISO/IEC/IEEE 29148 well-formedness is paywalled; do not invent clause letters.

## Interface

| Output | Path |
|--------|------|
| Living spec | `docs/<feature>-requirements.md` (or the repo's existing convention) |
| Open questions | `docs/<feature>-open-questions.md` |
| IDs | `FR-*` / `NFR-*`; NFR numbers align with the RSCOP catalog when engagement-level |

Ask the envelope first. If not web/SaaS, do not load page-load p95, WCAG, or session-timeout rows. Catalog numbers: TLS 1.3 required / 1.2 minimum; WCAG 2.1 AA on web/SaaS; RPO transactional ≤ 1h, sourced ≤ 24h.

## Process

1. **Intent** — who, what problem, business need. Pull from the conversation or a connected tracker page. Confirm the repo. Record unknowns in the open-questions log. Do not invent answers.
2. **Write** — outline in `references/outline.md`. Observable behavior, not implementation. No file paths or code snippets in the spec.
3. **Checkpoint** — present the spec and **stop**. Human signs off. Non-technical reviewers read scope through NFRs.

When later work learns something, **update the spec first**. Bump affected `FR-*` by adding a new ID or marking the old one removed.

## Gotchas

- A vague "fast" with no number is untestable.
- Filling a gap instead of logging it poisons later work.
- Reusing an ID after a drop hides a removal.
- This skill does not author a SOW or a SAD, and does not create tickets.

## Quality bar

- [ ] Envelope asked
- [ ] Every FR/NFR has ID, statement, source, verification method
- [ ] Open questions file exists for unknowns
- [ ] Stopped at human sign-off
- [ ] No implementation paths in the spec
