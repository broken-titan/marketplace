# Envelope gate

First question, before loading web/SaaS rows:

**What is the system envelope?**

- A. Web / SaaS application (pages, sessions, browsers)
- B. Data pipeline / warehouse ELT
- C. API / service with no end-user UI this engagement
- D. Other (name it in one line)

Record the answer on the discovery matrix and the RSCOP cover.

## If not A (web / SaaS)

Do **not** load:

- P-C6 through P-C11 (WCAG, breakpoints, browser matrix, i18n-at-launch)
- P-C1 / P-C2 (page-load p95 / p99)
- S-C4 / S-C5 (session idle / absolute timeouts)
- SAD ADR-003 option A as a Django-admin / scaffold default
- UI technology baseline as if a page app were in scope

Use API or pipeline latency rows (P-E1 class) instead of page-load. Session
timeouts stay off unless the envelope later gains a browser session.

Silence does not pick A.
