---
name: Solutions Architecture Document
description: >-
  Use when authoring a Solutions Architecture Document from an RSCOP analysis
  and discovery notes. Follows the handbook SAD structure (overview, business
  context, conceptual, six architecture views, implementation, management,
  ADRs).
---
Author a **Solutions Architecture Document (SAD)** for the current engagement. This skill is a recipe and outline, not a filled project document. Produce a client-specific SAD from inputs; do not copy facts, names, or decisions from any prior engagement.

Grounded in the *Solutions Architect Handbook* (Ch. 1, 2, 16) and aligned with RSCOP (Reliability, Security, Cost, Operations, Performance).

## Hard rules

- **Never invent client facts.** Every concrete claim must come from the RSCOP file, SOW, discovery notes, or a named working assumption. If a fact is missing, mark the section **blocked** or **Open** and list the blocking requirement IDs.
- **Never mention a prior client.** Do not name, allude to, or reuse proper nouns from other engagements. Placeholders (`{Client}`, `{End customer}`, `{Upstream system}`, `{Source repo}`, `{Technical contact}`) appear only in the generated SAD, never as leftover names from an example.
- **Defaults are load-bearing.** Every RSCOP row with evidence basis *Default* is an assumption the client can override. Summarize the material ones; do not silently promote a Default to a locked decision.
- **Open stays Open.** Do not fill an Open RSCOP row with a guess. Either leave the SAD subsection blocked, or (only where this skill explicitly allows) state a *working assumption* and label it as such.
- **Cross-link, do not duplicate.** The RSCOP file remains the NFR source of truth. The SAD cites row IDs (`R-C3`, `S-E4`, …) and summarizes; it does not recopy every NFR table.

## When to run

Run this skill when the engagement needs a durable architecture artifact for delivery, handoff, or contract review.

**Required inputs (in order of priority):**

1. **RSCOP markdown** — `rscop-<project-slug>.md` (or equivalent). Complete enough that Explicit / Implied / Default / Open rows are populated. If this file does not exist, **stop and produce it first** using the RSCOP Analysis skill. Do not author a SAD from a feature list alone.
2. **Scope of Work / SOW** — in-scope / out-of-scope, reuse constraints, packaging, timeline.
3. **Discovery notes** — stakeholder map, technical-contact answers, existing-system walkthroughs.
4. Optional: existing architecture notes, data-model excerpts, vendor/tool inventory, contract language on regulatory regime.

**Do not run** if the only input is a feature list with no RSCOP pass. Produce the RSCOP first.

## Output

Write a single markdown file:

```
sad-<project-slug>.md
```

Cross-link the RSCOP file from the header and from every section that cites NFR rows.

Use these placeholders in the generated document only (substitute real names from *this* engagement's inputs):

| Placeholder | Meaning |
|-------------|---------|
| `{Client}` | Contracting organization that owns the engagement and (usually) production |
| `{End customer}` | Organization that will use the system once live; may be the client, or a customer of the client |
| `{Upstream system}` | Existing system this solution reads from or writes through; may be several |
| `{Source repo}` | Codebase this work branches from or lives in |
| `{Technical contact}` | Named person who provides data model, repo access, and architectural context during the build |
| `{Inheriting team}` | Post-handoff operational owner (may still be unnamed) |

Slug the filename from the current project name, not from a placeholder.

---

## Document header

Start the SAD with:

```markdown
# Solutions Architecture Document: {Solution name} ({Client})

**Version:** v0.x | **Last updated:** YYYY-MM-DD | **Status:** Draft | Post-discovery | Ready for review | …

**Audiences:** Business ({Client} leadership, {End customer} stakeholders if/when in-scope) · Engineering (delivery team, {Inheriting team})

**Requirements analysis input:** [rscop-<project-slug>.md](rscop-<project-slug>.md) — summarize remaining Open count and the clusters they fall in (end-customer specifics, client tooling policy, data-model contents, deployment target, …).

**How to read this document:** name the sections that are reliable *now* versus the sections that are blocked. Typical split: Overview, Business Context, Conceptual Overview, and most of Section 4 are reliable; Data Architecture and Infrastructure Architecture often remain partially blocked on a data-model walkthrough and a deployment-target answer.
```

Status language must match evidence: "substantially populated, N specifics pending" is honest; "complete" is not if Open rows still block a view.

---

## Authoring method

1. Read the RSCOP cover-to-cover. Inventory Explicit, Implied, Default, and Open rows. Note trade-off IDs (`T1`…).
2. Draft the header and Section 1 from SOW + Explicit rows. List Distinct milestones (see below).
3. Draft Sections 2–3 from capabilities, processes, and the actor/system diagram.
4. Draft each Section 4 view as **What is known** + **Open questions blocking section completion**. Never leave a blocked view looking finished.
5. Draft Sections 5–6 from Operations / Reliability defaults, aligning tool choices to existing client patterns when known.
6. Author ADRs for every Key Architecture Decision. Use the catalog below as *decision patterns* — pick the option this engagement's evidence supports; do not inherit a prior project's Accepted status.
7. Close with the Open Questions table. Every blocked subsection must appear as a row.

Cite RSCOP row IDs inline (`S-C5`, `O-E29`). When a Default is used as a design input, say so.

---

## Distinct milestones: code-complete vs. customer-live

Treat **code complete** and **customer live** as distinct milestones whenever the end customer is gated by a contract, procurement, UAT sign-off, or any similar external event.

| Milestone | Meaning | What ties to it |
|-----------|---------|-----------------|
| *Code complete* | Build phase ends; in-scope features delivered; {Client} staff can exercise the system | Delivery of code, docs, handoff package |
| *Customer live* | {End customer} gains access | **30-day warranty** and **load-test verification** (P-E10 class) start here, *not* at code-complete |

If the end customer *is* the client and no external gate exists, say so and collapse the two milestones — do not invent a soft-launch.

Record the split under Section 1 Scope and under Operations (`O-C9` class). Warranty language in Cost and Section 6 must use the customer-live clock.

---

## Working assumptions (allowed exception to "don't invent")

When a design-blocking row is Open but the team must keep moving, state a **working assumption**, label it, and keep the design portable.

**Deployment target Open (`O-E29` class):** assume a common simple Docker target such as **AWS ECS/Fargate** (or the client's nearest equivalent: Cloud Run, plain Docker hosts, Kubernetes). Reasoning: mid-size teams often want container deploy without Kubernetes operational overhead.

**Keep the container twelve-factor / generic:**

- Configuration via environment variables
- Stateless process, non-root user
- `HEALTHCHECK` directive, configurable port
- Image built once and promoted across environments

Only the **deploy pipeline** (task definitions, env injection, ingress) is target-specific. If the client later confirms Kubernetes, Cloud Run, or bare hosts, reuse the container and swap the pipeline.

Author Section 4e against the working assumption and revise on confirmation. Do the same pattern for CI platform and observability stack when those rows are Open: prefer "align with {Client}'s existing pattern" over introducing a new vendor.

---

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
| Multi-tenancy | … | S-C5 / ADR-001 / ADR-007 |
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
- Spare capacity headroom and designed throughput (P-E7 / P-E9 class)

**If O-E29 (or equivalent) is Open:** apply the working-assumption rule above. Author topology, networking/DNS, and scaling against that assumption; label it; revise on confirmation.

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

Every Key Architecture Decision is an ADR. Use this format **exactly** (field order and names):

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

### Open Questions Blocking This Document

Close the SAD with this table. The complete unanswered list lives in the RSCOP; this table is the **architecture-material subset**.

| Requirement ID | Question | Blocks SAD section |
|---|---|---|
| {P-E1, …} | Data-model walkthrough and schema stability | 4c Data Architecture — fully blocked until `{Technical contact}` delivers |
| {O-E29} | Deployment target (cloud, region, runtime) | 4e Infrastructure — working assumption in force until confirmed |
| {display-attribute rows} | Which entities/attributes the UI must show | 4a Information Architecture — partially blocked |
| {P-C13, P-C14, mobile} | User count, peak concurrency, device mix | 4e scaling; 4a breakpoint priority |
| {O-E23, O-E24} | Existing CI pattern and observability stack | 4b, 5, 6 tool choices |
| {laptop-policy rows} | Corporate-laptop / tooling policy | Build velocity; does **not** block architecture authoring |
| {S-E12} | Audit log destination | 4f, ADR-004 |
| {S-E13} | Role matrix source | 4f |
| {future IdP row} | End-customer future identity-provider preference | Informs ADR-005; does not block the seam |
| {C-C7} | Target delivery date | 1 Constraints — pending contract if gated |

Call out the single highest-priority discovery item (usually the data-model walkthrough) and which blocker can wait until staging is needed (usually deploy target).

---

## ADR catalog (decision patterns)

Use these seven as a checklist. Each is a **pattern with options**, not an accepted decision. Select (or reject) per this engagement's evidence. Add ADRs for decisions that are not in this list.

Recommended default, where noted, is a starting point for silent/typical web apps — still flag it to the client.

### ADR-001 — Multi-tenant architectural readiness

**When it applies:** more than one organization will ever see the system, or the SOW says "onboard additional customers with minimal rework," even if only one tenant is commercially active at launch.

**Options:**

- **A. Full multi-tenant at launch** — every operational procedure (billing, onboarding UI, per-tenant config) is built now. Right when tenant 2 is real and near.
- **B. Single-tenant with multi-tenant seams** — tenant column (or equivalent), scoped querysets, tenant-context middleware. System runs single-tenant in practice; adding tenant 2 is a documented operational procedure. Typical cost: about a day of upfront work.
- **C. Pure single-tenant; refactor when needed** — cheapest now; most expensive when tenant 2 arrives. Only honest if the client explicitly accepts a rewrite.

**Pattern rationale:** "minimal rework" (C-C1 class, often defaulted to ≤ 5 engineer-days) is implausible without seams. Seams convert second-customer onboarding into configuration.

**Consequences if B selected:** 4c models carry a tenant association; 4f runs a cross-tenant leakage test even with one active tenant; 4b includes tenant-context middleware from day one.

**Related rows:** S-C5, S-E4, C-C1; Trade-off T1 class.

### ADR-002 — Test data source

**When it applies:** always. The build needs realistic data.

**Options:**

- **A. Use existing `{Upstream system}` data via `{Source repo}` / client infrastructure** — highest realism; depends on `{Technical contact}` granting access in week 1; watch data-egress and laptop-policy constraints.
- **B. Synthesize test data** — when existing data cannot leave its environment, or no corpus exists.
- **C. Hybrid** — scrubbed subset + synthesized edge cases. Use when A is available but incomplete (missing tenants, missing failure states).

**Pattern rationale:** prefer A when the scope is a view onto existing data and the contractor works on the client's side of the trust boundary. Prefer B/C when egress is forbidden or the model is net-new.

**Consequences:** Section 5 environment requires the chosen source; week-1 schedule depends on access or synthesis time.

**Related rows:** O-E3 class; test-data trade-off if one exists.

### ADR-003 — UI technology baseline

**When it applies:** always. "Usability over polish" still needs a baseline.

**Options:**

- **A. Framework admin / scaffold baseline** (e.g. Django admin, Rails ActiveAdmin, equivalent). Fast; fits read-only or internal-tool scope; light theming allowed; custom UI is a later engagement.
- **B. Custom server-rendered templates + a component library** (e.g. Tailwind + headless components). Needs design effort; only if a designer or design system is in scope.
- **C. Progressive enhancement on the server stack** (HTMX-class). Escalation path for a few interactive pages without a second artifact. Allowed mid-engagement per page; rarely the whole baseline.
- **D. Decoupled SPA** (React/Vue + API). Consider when the client already has a design system and SPA, or the UX cannot be met by A/B/C. Tax: two pipelines, CORS/auth, two test stacks. Do not choose it to "match a sibling app" unless that unification is in *this* SOW.
- **E. Existing client design system.** Select if one is identified and staffed. If none exists, say so; do not invent one.

**Pattern rationale:** timeline, write-posture, staffing model, and whether the end customer has already seen a UI. Solo or short engagements favor A. Revisit D as a future engagement if surfaces must unify later.

**Consequences:** 4a hierarchy follows the chosen convention; 4b either has or does not have a front-end build step; 4f must still enforce tenant/row access under the chosen UI's permission model.

**Related rows:** P-C1 class; export/reporting rows if they force more than a list/detail UI.

### ADR-004 — Audit log destination

**When it applies:** audit coverage/retention are in the RSCOP (they almost always are). Destination is frequently Open.

**Options:**

- **A. Application database only** — simplest; queryable in-app; sufficient when no central SIEM exists; risk: not searchable with other client streams.
- **B. Application database plus shipped to a central system** — higher integration cost; align with the existing observability/SIEM stack (O-E24 class).
- **C. Direct write to central system only** — loses local queryability for app admins.

**Pattern rationale:** do not pick B/C until `{Client}` names the destination system. Default the *coverage and retention*; leave destination **Proposed** until S-E12 class is answered.

**Consequences:** A keeps 4f and Section 6 self-contained. B/C couple to the observability and possibly deploy-target answers.

**Related rows:** S-E12, S-C19, O-E24; Trade-off T7 class.

### ADR-005 — Auth approach with swap point for future SSO

**When it applies:** always. SSO may be out of scope now and still arrive later.

**Options:**

- **A. Framework built-in auth, called directly throughout the app** — cheapest; locks a refactor when SSO is added.
- **B. Framework built-in auth behind a provider-shaped interface** — small upfront cost (~1 day); views, admin, and role bindings call only the interface. Future SSO/IdP swaps the implementation.
- **C. Build SSO / external IdP now** — only if an integration target is identified and in scope.

**Pattern rationale:** the seam is cheap relative to a retrofit. The end-customer's eventual IdP is often unknown; the seam protects any reasonable future answer. Future IdP preference **informs** the interface shape; it does not block building the seam.

**Consequences:** 4b has a provider module; views do not import the concrete auth library; 4f documents "swappable"; a future SSO engagement is scoped to the provider module.

**Related rows:** S-C1, future-IdP row, S-E11 class.

### ADR-006 — Build versus buy

**When it applies:** always, even when the SOW already assumes a custom build. Document the choice so it is not an unexamined assumption.

**Options (adapt names to the domain; do not import another client's vendors):**

- **A. Custom build on the client's existing stack / `{Source repo}`** — no new vendor; integrates with `{Upstream system}`; single-stack maintenance for `{Inheriting team}`.
- **B. Commercial domain-portal module** — only if `{Upstream system}` is itself that commercial product and the module fits the read/write posture.
- **C. Open-source domain platform** — evaluate only if it *displays* someone else's data rather than insisting on *owning* the workflow. Watch for a second language/runtime beside the client's stack.
- **D. Low-code internal-tool builder** — fast UI on an existing schema; trade-offs: license, hosted dependency, weaker data-access-layer authorization, second technology for `{Inheriting team}`.
- **E. Enterprise customer-portal platform** — usually overkill for a narrow, single-purpose surface; procurement cost often exceeds a short engagement.

**Pattern rationale:** if the fundamental work is "expose `{Upstream system}` as a scoped view," off-the-shelf tools are optimized for a different problem (own the data, own the workflow, generic portal). Integration cost then exceeds writing the equivalent code. Revisit when a future end-customer has a fundamentally different model, UX, or regime. This ADR does not commit `{Client}` to custom for all future work.

**Consequences:** stack, licensing, and whether ADR-001/003/005 remain meaningful (a buy decision can force those ADRs to be rewritten).

**Related rows:** UI baseline, reuse-of-existing-services, inheriting-team skill fit.

### ADR-007 — Tenant isolation enforcement

**When it applies:** when ADR-001 commits to seams, or when any two organizations must never see each other's rows.

**Recommended default:** Postgres Row-Level Security **plus** application-level scoped querysets (defense in depth). State this as the recommended default; still walk the options.

**Options:**

- **A. Postgres RLS + scoped querysets (recommended default).** Database rejects cross-tenant reads; application layer makes intent visible and protects against misconfigured RLS. Both layers tested independently.
  - Every tenant-scoped table has a tenant key aligned with the client's existing org concept.
  - RLS policy: `tenant_id = current_setting('app.current_tenant_id')` (type as appropriate).
  - Middleware sets `app.current_tenant_id` via `SET LOCAL` from the authenticated principal.
  - A tenant-scoped manager (or equivalent) adds a current-tenant filter on every query.
  - Migrations run as a `BYPASSRLS` role; request-time queries run as a regular role.
- **B. RLS only** — loses code-as-documentation; queries become brittle if RLS is misconfigured.
- **C. Application-level queryset filtering only** — vulnerable to raw SQL, forgotten filters, privileged views. Insufficient when the leak cost is high.
- **D. Schema-per-tenant** — strong isolation; per-tenant migration overhead; reserved for tens-to-hundreds of tenants.
- **E. Database-per-tenant** — strongest isolation, highest ops cost; inappropriate for one or a handful of tenants.

**Pattern rationale:** enforce isolation at the lowest layer that can do it. Application-only enforcement leaves a window for a future bug after handoff. Schema/DB-per-tenant is usually over-engineering at launch.

**Preconditions if A selected:** this system **owns its own Postgres database**. Do not add RLS policies to `{Upstream system}`'s database. Pushing for a separate database is the cleaner separation regardless.

**Consequences if A selected:** dual DB roles in settings and migration commands; CI check that every `tenant_id` table has an RLS policy; two test suites (regular role asserts RLS denies; bypass role asserts the manager still filters); small pre-build learning time for RLS fluency.

**Related rows:** S-C4, S-C5, S-E1, S-E4; specifies the mechanism ADR-001 committed to.

---

## Defaults-template mapping (do not drift)

When a section feels empty, return to the category that feeds it. Do not invent a parallel outline.

| SAD section | Feeds from |
|---|---|
| 1 Solution Overview | Functional requirements + Cost & Constraints |
| 2 Business Context | Functional requirements + stakeholder map |
| 3 Conceptual Solution Overview | Synthesized actor/system diagram |
| 4a Information Architecture | Usability & Accessibility |
| 4b Application Architecture | All NFRs + tech-stack decisions |
| 4c Data Architecture | Performance & Scale + Security & Compliance |
| 4d Integration Architecture | Interoperability & Integration |
| 4e Infrastructure Architecture | Reliability & Continuity + Cost |
| 4f Security Architecture | Security & Compliance |
| 5 Solution Implementation | Operability & Maintainability (build) |
| 6 Solution Management | Operability & Maintainability (run) + Reliability |
| 7 Appendix | Trade-offs, POC outcomes, vendor comparisons, ADRs |

Silence on an NFR is not "no requirement." It is a Default the client can override, or an Open that blocks a view. The architect bridges both audiences: do not close a business question with "engineering will figure it out," and do not close a technical question with "the business does not care."

---

## Quality bar before handing the file over

- [ ] Filename is `sad-<project-slug>.md` and the header links the RSCOP
- [ ] No proper nouns from any other engagement
- [ ] Every concrete number or control cites a row ID or is labeled a working assumption
- [ ] Code-complete and customer-live are distinct if and only if an external gate exists
- [ ] Warranty and load-test verification follow customer-live when the split exists
- [ ] Each Section 4 view has a "blocked on" list or an explicit "nothing blocking"
- [ ] Seven catalog ADRs are present as patterns applied to *this* evidence (or explicitly N/A with reason)
- [ ] ADR field order matches the format above
- [ ] Open Questions table is the last section and covers every blocked view
- [ ] Container/app remains twelve-factor if the deploy target is still Open
