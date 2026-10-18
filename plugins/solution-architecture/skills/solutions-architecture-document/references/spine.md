# Section spine

## Section spine

Keep this structure. Under each heading: authoring instructions, then the outline the generated SAD must contain.

### 1. Solution Overview

**Author from:** SOW functional scope + Cost & Constraints + Explicit RSCOP rows.

#### Purpose

One paragraph: what the system is, who it serves, what existing systems it sits on, and the business question it answers. No implementation detail.

#### Scope

**In scope** — bullet the delivered surface (application shape, read/write posture, auth approach this engagement, tenant seams, packaging, documentation/handoff).

**Out of scope (future-state)** — writes if this engagement is read-only; SSO if only a seam is in scope; native mobile; reporting/exports unless confirmed; onboarding additional end-customers at launch (architectural support ≠ commercial activation).

**Distinct milestones** — code-complete vs. customer-live when gated (see above).

#### Assumptions

Every Default row is a load-bearing assumption. Point at the RSCOP for the full list. Summarize the *most material* defaults **by RSCOP dimension**, citing row-ID ranges:

- **Reliability** — availability, RPO/RTO, upstream-outage behavior, backup retention
- **Security** — TLS, secrets, audit retention, MFA posture, encryption at rest, PII-in-logs = 0, cross-tenant leakage tests in CI
- **Cost** — new-customer onboarding effort cap, production account owner, OSS preference, warranty clock (customer-live)
- **Operations** — environment count, CI/deploy time budgets, coverage floors, structured logging, runbook-before-alert, zero-downtime migrations
- **Performance** — page/app/db latency p95, no full-table scans, server-side pagination, WCAG floor, browser matrix, i18n posture
- **Regulatory representation** — quote the client's stated regime (or "none stated") as Implied; require contract formalization; apply baseline engineering hygiene regardless

Do not invent numbers. Copy targets from the RSCOP Defaults.

#### Constraints

Reuse of `{Upstream system}` / `{Source repo}`, packaging (e.g. Docker), tenant isolation, read/write posture, auth-swap-point requirement, hosting account owner. Each constraint should be traceable to an Explicit or Implied row.

#### Dependencies

Named systems and people, not vibes:

- `{Upstream system}` — data source; who owns the model
- Further-upstream systems that feed it (not directly accessed, but they shape the model)
- `{Source repo}` — branch/reuse constraint
- `{Technical contact}` — data model, repo access, architectural context
- Domain reviewer (if any) — UI/workflow validation
- Contract or external gate — required before customer-live
- `{Inheriting team}` — post-handoff owner (name if known; else Open)

#### Key Architecture Decisions

List the ADRs that exist (or must exist) with one-line status. Detail lives in the Appendix.

Typical set: ADR-001 … ADR-007 from the catalog below. Add engagement-specific ADRs as needed; do not omit a catalog ADR just because the option chosen is "not applicable — document why."

---

### 2. Business Context

**Author from:** functional requirements + stakeholder map + RSCOP NFR summary. Handbook mapping: Business Context ← functional reqs + stakeholder map.

#### Business Capabilities

Who can do what, and when:

- `{End customer}` staff (once live): the jobs the system enables
- `{Client}` staff during build: exercise against real or production-like data before the end customer sees it
- `{Client}` as a business: the repeatable pattern or strategic question this engagement establishes

#### Key Business Processes

Numbered primary process. State clearly what this system **does not** participate in (intake, mutation, generation — if it is a view onto state owned elsewhere).

Flag process specifics that wait on a data-model walkthrough (entity states, attributes, lifecycle granularity).

#### Stakeholders

Table: **Role | Concerns**. Include at least:

| Role | Typical concerns |
|------|------------------|
| `{End customer}` staff (eventual end users) | Correct, timely, scoped data |
| `{End customer}` leadership (if they are a contract holder) | Visibility expectations before/after signing |
| `{Client}` leadership | Delivery, pattern, timeline |
| `{Client}` operations / domain team | No disruption to `{Upstream system}`; accurate reflection of recorded state |
| Domain reviewer (if any) | Workflow language and expectations |
| `{Technical contact}` | Data model, repo access, architectural fit; possible handoff candidate |
| Build team | Acceptance criteria, integration points, handoff materials |
| `{Inheriting team}` | Operate and evolve without the contractor |

Drop rows that do not exist on this engagement; do not invent personas.

#### Non-Functional Requirements

Point at the RSCOP. One-paragraph summary **by dimension**, noting which items are Explicit / Default / Open. Do not paste the full NFR tables.

#### Regulatory & Compliance

- State the client's representation (regime applies / does not / unknown).
- If "no regime," require the contract to formalize that representation and to locate future compliance responsibility on `{Client}`, not the contractor.
- Apply baseline hygiene regardless: audit of reads and admin actions, encryption in transit and at rest, secrets in vault, PII scrubbed from logs, dependency scanning, cross-tenant leakage test in CI (when multi-tenant seams exist).
- Note the adjustment points if a regime appears later: audit retention, encryption depth, pen-test cadence.

---

### 3. Conceptual Solution Overview

**Author from:** synthesized high-level architecture. This section should be readable by both audiences.

1. **Prose (3–6 sentences):** what the system is, what it reads/writes, what it owns vs. what `{Upstream system}` owns, where authorization is applied.
2. **Diagram** — ASCII or mermaid. Actors → this system → `{Upstream system}` → further-upstream systems. Annotate trust boundaries (HTTPS/TLS), read vs. write arrows, and which box is "this project."
3. **End-to-end flow** — one paragraph from real-world event through upstream write, user login, authn/authz, scoped presentation. Mention the customer-live gate if it exists.
4. **Component responsibilities** — one bullet per box on the diagram. This system: auth, request handling, role-aware filtering, audit writes, integration. `{Upstream system}`: canonical store / model owner. Further-upstream: records operations; not directly accessed.

Diagram template (replace labels from *this* engagement):

```
                    +-----------------------+
                    |  {End customer} staff |
                    |  (once live)          |
                    +----------+------------+
                               |
                    +----------v------------+
                    |  {Client} staff       |
                    |  (build-phase users)  |
                    +----------+------------+
                               | HTTPS (TLS 1.3)
                               v
                    +-------------------------+
                    |  This system            |
                    |  (from {Source repo},   |
                    |   packaged as agreed)   |
                    |  - presentation         |
                    |  - auth (swap point)    |
                    |  - role/tenant filter   |
                    |  - audit writes         |
                    +-----------+-------------+
                                | reads / writes as scoped
                                v
                    +-------------------------+
                    |  {Upstream system}      |
                    |  (canonical data)       |
                    +-----------^-------------+
                                | upstream writes
                    +-----------+-------------+
                    |  Further-upstream       |
                    |  (not directly accessed)|
                    +-------------------------+
```

---

### 4. Solution Architecture

Six views. Each view: **What is known** (cited) then **Open questions blocking section completion** (row IDs). A view with a fully blocked core (no data model, no deploy target) must say so in the first sentence.

#### 4a. Information Architecture

**Sources:** Usability & Accessibility + client-perspective Performance rows.

Cover:

- UI technology baseline (admin framework, custom templates, existing design system — from ADR-003)
- Primary user types and what each may see/do
- Navigation hierarchy (list / detail / related-object, or the equivalent)
- Accessibility floor (default WCAG 2.1 AA unless overridden)
- Responsive breakpoints (defaults 1024 / 768 / 375) and whether mobile is a first-class target or incidental

Block finalization of view lists and filter sets until the entity list exists (data-model walkthrough). Call out Open rows for display attributes, export/reporting, scan/barcode participation if relevant, mobile usage.

#### 4b. Application Architecture

**Sources:** all NFR dimensions + tech-stack decisions.

Cover:

- Component shape (one app vs. several; branch vs. greenfield; how it talks to `{Upstream system}`: in-process, shared DB, or API — mark Open if unknown)
- Authorization at the **data-access layer**, not the view layer
- Auth behind a provider-shaped interface (ADR-005) so views never import the concrete IdP
- Tenant context via middleware; views do not handle tenant logic directly

**Tech-stack table** (required):

| Layer | Choice | Source |
|-------|--------|--------|
| Language | … | Implied / Explicit |
| Framework | … | Explicit |
| User interface | … | ADR-003 |
| Authentication | … | ADR-005 |
| Authorization | … | S-E1 class |
| Multi-tenancy | … | T1 / ADR-001 / ADR-007 |
| Containerization | … | Explicit packaging row |
| Deployment target | … | Open or working assumption |
| Continuous integration | … | Align with {Client} pattern; Open if unknown |
| Observability | … | Align with {Client} stack; Open if unknown |
| Feature flags | … | Default if silent |

**Configuration:** secrets in vault; per-environment config via env vars; tenant catalog and role matrix data-driven.

Open questions typically: existing CI pattern, observability stack, corporate-laptop posture (velocity, not architecture), code-review workflow.

#### 4c. Data Architecture

**Sources:** Performance & Scale + Security & Compliance. Often the most blocked view.

Cover what is known without the full ERD:

- What this system **does not** own (canonical business data in `{Upstream system}`)
- Portal/app-owned state (sessions, role bindings if local, audit rows, preferences)
- Whether this system owns its own database (precondition of ADR-007 if RLS is selected)
- Partition key (`tenant_id` or the client's existing org concept)
- Migration role vs. request-time role (if RLS)
- Backup policy applies to **this system's** state; `{Upstream system}` backups stay with their owner

Leave ERD, schema, data-flow-beyond-conceptual, and storage strategy **blocked** until `{Technical contact}` delivers the model. Name that walkthrough as the highest-priority discovery item.

Open questions typically: ERD availability, schema stability during build, corpus size/growth, existing query patterns to mirror.

#### 4d. Integration Architecture

**Sources:** Interoperability & Integration.

**Integration map** (required table):

| Integration | Direction | Mechanism | Sync/Async | Notes |
|-------------|-----------|-----------|------------|-------|
| This system ↔ `{Upstream system}` | … | ORM / shared DB / API — Open until confirmed | Sync for user-facing reads; async if > 5s | Mechanism depends on how `{Source repo}` and `{Upstream system}` relate |
| This system ↔ `{End customer}` browsers | Inbound | HTTPS / TLS 1.3 | Sync | Default unless overridden |
| This system ↔ `{Client}` staff browsers | Inbound | HTTPS / TLS 1.3 | Sync | Default unless overridden |

Add rows for any other confirmed integration. Do not invent webhooks or buses.

**Failure isolation** (from Reliability engineering defaults unless overridden):

- Timeout on every upstream call (default 5s)
- Circuit breaker after N consecutive failures (default 5)
- Health-check interval + automated restart (default 30s / 2 failures)
- On `{Upstream system}` failure: cached last-known-good + status banner; no blank page

Open questions: exact integration mechanism; deployment target as it affects networking.

#### 4e. Infrastructure Architecture

**Sources:** Reliability & Continuity + Cost.

What is usually known early:

- Environment count (default: dev local, staging, production)
- Production account owner (default: `{Client}`)
- Packaging (Docker or as Explicit)
- Spare capacity headroom and designed throughput (P-E6 / P-E8 class)

**If O-E26 (or equivalent) is Open:** leave it Open or ask. Do not assume ECS/Fargate. Author topology only against a *user-labeled* working assumption; revise on confirmation.

**Local development:** compose file with the app + its datastore. Add Redis/queue only if the scope warrants background work or shared cache.

Open questions: deploy target confirmation, monthly infra budget, extra environments (UAT, per-customer preview), user count / peak concurrency.

#### 4f. Security Architecture

**Sources:** Security & Compliance. This view must be specific enough to implement.

**Authentication and authorization**

- Concrete mechanism this engagement (built-in, existing IdP, SSO) and the swap-point posture (ADR-005)
- Role-based (or ABAC) enforcement at the data-access layer
- Minimum roles (end-customer scoped vs. client-staff broader). MFA required for privileged, optional for standard, unless overridden

**Role / permission matrix**

- Storage: data-driven, not hardcoded
- Source: inherit existing taxonomy vs. define here — often Open

**Encryption**

- In transit: TLS 1.3 required, 1.2 minimum; HSTS max-age ≥ 31,536,000s unless overridden
- At rest: AES-256, vendor-managed key unless a regime demands more
- Field-level: not in baseline unless a regime requires it

**Secrets** — 100% in a vault; 0 in source; rotation cadence (default 90 days)

**Audit** — 100% of reads and admin actions; retention 1 year baseline (extend if regime); destination is often Open (ADR-004)

**Tenant boundary** (if ADR-001/007 apply)

- Primary enforcement mechanism (RLS recommended default — see ADR-007)
- Defense in depth at the application layer
- Tenant context: middleware sets app context **and** session variable
- Role separation: bypass role for migrations; regular role for request-time
- CI: cross-tenant leakage test at **both** layers; SQL check that every `tenant_id` table has a policy; 100% pass required to deploy

**App and dependency security** — OWASP Top 10 + SAST/DAST every build; dep scan every PR + weekly; critical vulns block deploy

**Compliance posture** — restate Section 2; do not weaken it

**Threat model summary** — at least: cross-tenant leakage, credential theft, session hijack, injection, dependency compromise, insider misuse of staff access. Each threat maps to a control row.

Open questions typically: future IdP preference (informs swap-point design, does not block it), role-matrix source, audit destination, pre-launch security-review owner.

---

### 5. Solution Implementation

**Sources:** Operability & Maintainability (build side).

**Development approach**

- Idiomatic structure for the chosen framework
- Branch/merge aligned with `{Client}` conventions (Open if unknown)
- Authz at data-access layer; auth only through the provider interface; tenant logic only in middleware
- `{Upstream system}` behind **one declared interface module** with a mock layer for tests

**Build and CI**

- Time budget (default ≤ 5 minutes push-to-result)
- Steps: lint, unit tests, dep vuln scan, SAST, DAST, cross-tenant leakage test
- Coverage floors (default ≥ 80% unit on app code; ≥ 60% integration on critical paths)
- CI platform: align with existing pattern; do not pick a new one while the row is Open

**Deployment**

- Staging and production time budgets (default ≤ 10 minutes each)
- Image built once, promoted
- Zero-downtime, backwards-compatible migrations
- Rollback procedure in the deploy runbook (handoff deliverable)

**Data migration**

- If this system does not own the canonical business data: no migration of that data
- App-owned state starts empty; initial `{Client}` user provisioning is a runbook step
- If a migration *is* in scope, describe source, transform, cutover, and rollback

**Decommissioning**

- Net-new: "Not applicable."
- Replacement: what is turned off, data retention, DNS/account teardown, owner of the work

---

### 6. Solution Management

**Sources:** Operability & Maintainability (run side) + Reliability.

**Operational management** — weekly dep scans; criticals block builds; non-criticals batched; platform-upgrade cadence aligns with `{Inheriting team}` (often Open)

**Monitoring and alerting**

- Structured JSON logs; searchable + archive retention (defaults 30 days / 1 year)
- Error tracker: 100% of unhandled exceptions, sensitive data scrubbed
- One metrics dashboard per production service: latency, traffic, errors, saturation
- Alert routing + on-call: align with `{Client}` existing setup
- 100% of alerts have a runbook entry before being wired

**Production support**

- Post-handoff owner: `{Inheriting team}` (name if known)
- Warranty: 30 calendar days **from customer-live**, not code-complete, unless the SOW says otherwise

**Incident management** — MTTD / MTTR defaults (5 min / 30 min) unless the client has an existing procedure to inherit. Severity and escalation: align, do not invent.

**Disaster recovery and business continuity**

- RPO / RTO for app-owned state and for read paths (cite RSCOP)
- Backup retention (local + off-site)
- Upstream-outage behavior (banner + cache freshness)

**Capacity management**

- Designed throughput and linear-scaling multiple (defaults 5× peak)
- Headroom at handoff (default ≥ 2× current)
- Scaling triggers wait on user-count / concurrency answers; if a single end-customer at launch, say initial concurrency is likely modest — do not invent a number

---

### 7. Appendix

#### Architecture Decision Records

Every Key Architecture Decision is an ADR. Prefer files authored by `architecture-decision-records` (`docs/adr/` or the repo's existing tree) and **link** them here. When an ADR must be inlined, use this format **exactly** (field order and names):

```markdown
#### ADR-00N: {Title}

**Status:** Proposed | Accepted | Superseded | Rejected
**Date:** YYYY-MM-DD
**Deciders:** {who must live with this}

**Context**
Why this decision exists now. Cite the constraint or RSCOP rows that force it.

**Decision**
The choice, in one short paragraph. If still Open, say who owes the answer and which row.

**Options Considered**
- **Option A: …** Trade-off in one sentence.
- **Option B: …** (Selected) — only mark Selected when this engagement's evidence supports it.
- **Option C: …**

**Rationale**
Why the selected option wins *on this engagement*. Cost of the seam vs. cost of the retrofit is a valid argument; "we always do it this way" is not.

**Consequences**
Bullet the SAD sections this decision changes, plus operational or test obligations.

**Related**
Requirements analysis rows: {IDs}; Trade-off {Tn}; other ADRs this informs or depends on.
```

Status is **this engagement's** status. Do not copy Accepted from a catalog example.

#### Trade-off summary

Point at the RSCOP trade-off table. List each `Tn` as Decided / Defaulted / Open and name the ADR that closed it when one exists.

#### Proof-of-concept outcomes and benchmarks

None is a valid answer. Recommend candidates that unblock a risk (e.g. filtered-query latency vs. P-E2 / P-C4) and schedule them after the data model is known. Do not fabricate results.

#### Vendor and tool comparisons

Only for Open operational choices (CI, observability, runtime). Prefer "align with `{Client}` existing pattern." Compare vendors only when the client has no pattern.

#### Glossary

Define engagement-specific systems, roles, and RSCOP terms (Default, Open, RPO, RTO, Tenant, soft-launch milestone). Do not define placeholder names as if they were real products.

---

