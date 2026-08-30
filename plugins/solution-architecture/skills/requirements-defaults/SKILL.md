---
name: requirements-defaults
description: >-
  Use during a discovery call or before SAD/RSCOP work to walk NFR
  categories as HIT / MISS / DEFAULT / ASK. Writes
  docs/<slug>-nfr-discovery.md.
---

Walk non-functional requirements. Envelope first: web/SaaS vs data pipeline vs API vs other (`rscop-analysis/references/envelope.md`). Non-web skips page-load p95, WCAG, session timeouts, and admin-UI defaults.

Catalog numbers: TLS 1.3 required / 1.2 minimum; WCAG 2.1 AA (web/SaaS); RPO transactional ≤ 1 hour, sourced/read-only ≤ 24 hours; RTO ≤ 4 hours. Full category lists: `references/walk.md`. RSCOP rows: `rscop-analysis/references/catalog.md`.

SOW is an input. Next file after this matrix is `docs/rscop-<slug>.md`, then `docs/sad-<slug>.md`.

## Interface

| Tag | Meaning |
|-----|---------|
| **HIT** | Stated. Quote or paraphrase; locked. |
| **MISS** | Silent in scope. |
| **DEFAULT** | Target if they stay silent (`references/walk.md`). |
| **ASK** | Question that turns a MISS into a HIT or an override. |

Every category gets all four. Walk HIT → MISS → DEFAULT → ASK.

Output: `docs/<slug>-nfr-discovery.md`.

## Gotchas

- A MISS left unflagged becomes a silent DEFAULT — the author owns that risk.
- Feature talk is not a reason to skip a category.
- Overlays (Well-Architected, NIST families, C4, HIBP, DAST-every-build) stay off until flagged.

## Quality bar

- [ ] Envelope asked first
- [ ] All eight categories in `references/walk.md` filled
- [ ] Numbers match the RSCOP catalog
- [ ] File path is `docs/<slug>-nfr-discovery.md`
