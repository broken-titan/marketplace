---
name: RSCOP Analysis
description: >-
  Use when producing a non-functional requirements analysis (Reliability,
  Security, Cost, Operations, Performance) from a SOW, discovery notes, or
  client intake. Every row gets a measurable target and an evidence basis
  (Explicit / Implied / Default / Open).
---
**Hard rule:** Never mention a prior client, person, repository, product, or industry from any earlier engagement. This skill is project-agnostic. Substitute `{Client}`, `{End customer}`, `{Upstream system}`, `{Source repo}`, and `{Technical contact}` only inside the OUTPUT document you produce for the current run — fill those tokens from THIS project's sources, or leave the brace tokens in place when the source is silent. Do not invent names.

This file is a **recipe**, not a filled project document. Copy the starter catalog into a new analysis, classify every row from the current sources, then add project-specific rows. Do not ship this skill's wording as the deliverable.

The finished RSCOP file is an input to a Solutions Architecture Document (SAD). After this skill completes, the SAD skill (or an equivalent SAD authoring pass) consumes `rscop-<project-slug>.md` as the NFR spine for Solution Management, Security Architecture, Infrastructure Architecture, and related SAD sections.

---

## 1. When to run and required inputs

Run this skill when the user asks for a non-functional requirements analysis, an RSCOP pass, NFR lock-in before a SAD, or a discovery-call write-up of Reliability / Security / Cost / Operations / Performance.

**Required inputs (gather all that exist; do not invent the rest):**

| Input | What you extract | If missing |
|-------|------------------|------------|
| Scope of Work / contract draft | Stated commitments, out-of-scope items, delivery window, warranty, ownership | Mark affected rows **Open** |
| Discovery notes / intake call | Auth approach, roles, write vs read-only, UI baseline, named contacts, regulatory comments | Mark affected rows **Open** |
| Existing-stack notes | `{Source repo}`, `{Upstream system}`, packaging, CI, observability, cloud account, inherited SLOs | Mark affected rows **Open** |
| Defaults in this skill | Measurable baseline targets | Apply as **Default** and flag so `{Client}` can override |

If an input is missing, **mark the row Open**. Do not invent client facts, user counts, regulatory positions, deployment targets, or named people. Silence is not a "no" — it is an Open or a flagged Default.

**Assumed engagement class for Defaults:** small-to-medium web / SaaS application. Scale latency, availability, and capacity targets up when the source describes a larger or 24/7 system.

---

## 2. Evidence categories

Keep these exact names. Use them as **divider rows** in every table (`| **Explicit** | | | |`, and so on).

| Category | Meaning | Lock status |
|----------|---------|-------------|
| **Explicit** | Stated by the client in a source | Locked |
| **Implied** | Inferred from the source; not said in so many words | Needs explicit confirmation |
| **Default** | Baseline applied because the source was silent | Must be flagged so the client can override |
| **Open** | Needs an answer; cannot be safely defaulted | Blocks a safe commitment |

Classification rules:

1. If the source states a target or choice → **Explicit**. Use the client's number, not the catalog default.
2. If the source only hints (existing stack implies maintainability; a "later" comment implies a seam) → **Implied**. Write the inference and the confirmation needed.
3. If the source is silent and the starter catalog has a safe baseline → **Default**. Keep the catalog target. Flag it.
4. If the source is silent and a wrong guess would bind `{Client}` or transfer risk → **Open**. Do not fill a target with a guess.
5. Never promote Default → Explicit without a cited source sentence.

---

## 3. Two perspectives and table format

Every dimension has **Client** and **Engineering** tables. Same columns, every time:

```
| # | Requirement | What it means | Target |
|---|-------------|---------------|--------|
| **Explicit** | | | |
| X-C1 | … | … | … |
| **Implied** | | | |
| **Default (baseline applied — flag to client)** | | | |
| **Open (needs answer)** | | | |
```

Omit an empty evidence group (no blank divider). Group by evidence, not by ID. IDs stay stable once assigned.

Write targets as measurable statements (`At least 99.5%`, `At most 5 minutes`, `0 (zero)`, `100%`). Avoid "should" and "reasonable".

---

## 4. ID scheme

| Dimension | Client | Engineering |
|-----------|--------|-------------|
| Reliability | `R-C#` | `R-E#` |
| Security | `S-C#` | `S-E#` |
| Cost | `C-C#` | `C-E#` |
| Operations | `O-C#` | `O-E#` |
| Performance | `P-C#` | `P-E#` |
| Trade-offs | `T#` | — |

Starter-catalog rows keep the IDs below. Append project-specific rows with the next unused integer in that prefix. Do not renumber after regrouping.

---

## 5. Generic starter row catalog

Include every row below in every run. Classify each from the current sources (usually they stay **Default**). If the client stated a different target, promote that row to **Explicit** and replace the target. Phrase the output so it applies to this web / SaaS engagement — do not copy industry-specific wording from memory.

Placeholders `{Client}`, `{End customer}`, `{Upstream system}` appear only in the output document, and only where that entity is known or still unknown.

### Reliability — Client (`R-C#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| R-C1 | Availability during business hours | Portion of business-hours time the system is reachable and functional | At least 99.5% | Default |
| R-C2 | Behavior on upstream outage | What users see when `{Upstream system}` or authentication is down | 100% of affected pages show a read-only status banner with cached data; 0 blank pages or unhandled errors | Default |
| R-C3 | Cache freshness for user-facing reads | How stale displayed data may become before refresh | At most 5 minutes since last refresh | Default |
| R-C4 | Data loss in failure scenarios | Loss of state owned by this application in a failure | 0 (zero) for application-owned state via transactions | Default |
| R-C5 | Outage attribution visibility | Whether users can tell when a problem is upstream versus in this application | 100% of upstream-failure events display a status banner identifying the source | Default |

### Reliability — Engineering (`R-E#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| R-E1 | Recovery Point Objective (transactional data) | Maximum acceptable loss of application-owned state after a failure | At most 1 hour | Default |
| R-E2 | Recovery Point Objective (sourced / read-only data) | Maximum acceptable lag against `{Upstream system}` after failure | At most 24 hours | Default |
| R-E3 | Recovery Time Objective (full system) | How quickly the system is restored after total failure | At most 4 hours | Default |
| R-E4 | Recovery Time Objective (read paths) | How quickly read-only access is restored | At most 1 hour | Default |
| R-E5 | Mean Time To Detection | Time from problem starting to alert firing | At most 5 minutes | Default |
| R-E6 | Mean Time To Resolution | Time from alert to mitigation | At most 30 minutes | Default |
| R-E7 | Database backup retention (local) | How long backup copies are kept on the primary infrastructure | 30 days | Default |
| R-E8 | Database backup off-site copy | How often a copy is stored in a separate location | 1 per week | Default |
| R-E9 | Upstream call timeout | How long to wait for `{Upstream system}` before giving up | At most 5 seconds | Default |
| R-E10 | Circuit breaker activation threshold | Failures before this application stops calling an upstream service | 5 consecutive failures | Default |
| R-E11 | Health-check frequency | How often the system checks itself | Every 30 seconds | Default |
| R-E12 | Automated restart trigger | When the system restarts itself | After 2 consecutive failed health checks | Default |

### Security — Client (`S-C#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| S-C1 | Transport encryption required | The encryption protocol for data sent between user and server | Transport Layer Security version 1.3 required; 1.2 minimum | Default |
| S-C2 | HTTP Strict Transport Security max-age | How long browsers should remember to require encryption | At least 31,536,000 seconds (1 year) | Default |
| S-C3 | Database encryption at rest | Whether stored data is encrypted on disk | AES-256 with vendor-managed key | Default |
| S-C4 | Session idle timeout | How long a user can be inactive before being logged out | 30 minutes | Default |
| S-C5 | Session absolute timeout | Maximum session length regardless of activity | 8 hours | Default |
| S-C6 | Multi-Factor Authentication for privileged users | Portion of admin accounts requiring a second factor | 100% required | Default |
| S-C7 | Multi-Factor Authentication for standard users | Whether a second factor is available to non-admin users | Available as optional | Default |
| S-C8 | Password minimum length | Shortest password allowed | 12 characters | Default |
| S-C9 | Password breach-corpus check | Whether passwords are checked against known-compromised lists | Enabled (e.g., Have I Been Pwned blocklist) | Default |
| S-C10 | Sensitive data in application logs | User or personal information that appears in log files | 0 occurrences (enforced via log middleware) | Default |

### Security — Engineering (`S-E#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| S-E1 | Authorization enforcement layer | Where in the code roles are checked | Data-access layer (not view layer) | Default |
| S-E2 | Secrets storage | Portion of passwords, keys, tokens stored in a vault rather than in source code | 100% in a vault service; 0 in source or environment files in source | Default |
| S-E3 | Secret rotation cadence | How often credentials are replaced | Every 90 days | Default |
| S-E4 | Cross-tenant data leakage test | Automated check that one tenant cannot see another's data | 100% pass rate required to deploy | Default |
| S-E5 | Audit log coverage | Portion of reads (and any admin writes) recorded for audit | 100% of reads and admin actions; retained 1 year baseline | Default |
| S-E6 | OWASP Top 10 coverage | Mitigations implemented against the top 10 industry-recognized web vulnerabilities | 100% of categories addressed and verified by security scanning | Default |
| S-E7 | Security scans in continuous integration | Static and dynamic application security scans run during build | Both run on every build | Default |
| S-E8 | Dependency vulnerability scan cadence | How often third-party libraries are checked | Every pull request and 1 scheduled scan per week | Default |
| S-E9 | Critical vulnerabilities in production dependencies | Known severe security issues in third-party code | 0 (build blocked if any detected) | Default |
| S-E10 | Role matrix storage | Where the role-to-permission mappings live | Data-driven (configuration or database), not hardcoded | Default |

### Cost — Client (`C-C#`)

*This section captures operational and effort cost only — not commercial pricing.*

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| C-C1 | New-tenant onboarding effort | Engineering work to add another tenant later | At most 5 engineer-days | Default |
| C-C2 | Steady-state infrastructure cost | Annual operating cost as a fraction of build cost | At most 5% of build cost per year | Default |
| C-C3 | Post-handoff bug-fix warranty | Period after delivery during which fixes are included | 30 calendar days | Default |
| C-C4 | Production infrastructure ownership | Who owns the cloud account running production | `{Client}` | Default |
| C-C5 | Dependency selection preference | Open source versus paid services | Open source preferred; paid only with documented justification | Default |
| C-C6 | Cloud portability | Whether storage and compute can move to a different cloud later | Cloud-portable where cost-neutral | Default |

### Cost — Engineering (`C-E#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| C-E1 | New engineer onboarding time | Time from joining to first meaningful pull request using handoff documentation | At most 5 days | Default |
| C-E2 | Maintenance burden after handoff | Share of one engineer's time required to keep the system running | At most 10% of one engineer | Default |
| C-E3 | Handoff deliverable contents | What is included in the handoff package | At minimum: architecture document, deploy runbook, incident runbook, onboarding guide | Default |

### Operations — Client (`O-C#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| O-C1 | End-customer issue-reporting channel | A defined way for end users to report problems once they have access | 1 channel with a defined response timeline | Default |
| O-C2 | Release notes on behavior changes | Whether users are told when something changes | Provided for every release with user-visible changes | Default |
| O-C3 | Post-handoff deployment autonomy | Whether the inheriting team can deploy without contractor involvement | 100% (no contractor required for routine deploys) | Default |
| O-C4 | New-tenant onboarding (operational procedure) | Engineering effort to add another tenant as a documented process | At most 5 engineer-days | Default |
| O-C5 | Soft-launch milestone | Distinguish code-complete from `{End customer}` going live | 2 separate milestones: code complete (build phase ends) and customer-live (access granted when `{Client}` authorizes) | Default |

### Operations — Engineering (`O-E#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| O-E1 | Number of environments | Separate deployment targets | 3 (development, staging, production) | Default |
| O-E2 | Continuous-integration build time | Time from pushing code to seeing pass/fail | At most 5 minutes | Default |
| O-E3 | Staging deployment time after merge | Time from merging code to staging availability | At most 10 minutes | Default |
| O-E4 | Production deployment time | Time from approved trigger to production deployment | At most 10 minutes | Default |
| O-E5 | Unit test coverage on application code | Portion of code exercised by unit tests | At least 80% of lines | Default |
| O-E6 | Integration test coverage on critical paths | Portion of critical user flows exercised by integration tests | At least 60% | Default |
| O-E7 | Log format | Whether logs are machine-parseable | Structured JSON | Default |
| O-E8 | Log retention (searchable) | How long logs are kept searchable | 30 days | Default |
| O-E9 | Log retention (archived) | How long logs are kept in cold archive | 1 year | Default |
| O-E10 | Error tracker coverage | Portion of unhandled exceptions captured for review | 100% (sensitive data scrubbed before capture) | Default |
| O-E11 | Metrics dashboard on production service | Visibility into latency, traffic, errors, saturation | 1 dashboard covering all four signals | Default |
| O-E12 | Mean Time To Detection | Time from problem starting to alert firing | At most 5 minutes | Default |
| O-E13 | Mean Time To Resolution | Time from alert to mitigation | At most 30 minutes | Default |
| O-E14 | Alerts with corresponding runbooks | Portion of alerts that have a written response procedure | 100% (orphan alerts block deploys) | Default |
| O-E15 | Database migration posture | Whether schema changes require downtime | Zero-downtime, backwards-compatible | Default |
| O-E16 | Feature flag system | Ability to turn features on/off without redeploying | In use for user-facing toggles | Default |
| O-E17 | Upstream integration structure | How `{Upstream system}` is accessed in code | 1 declared interface module, with a mock layer for tests | Default |
| O-E18 | Asynchronous operation threshold | When an operation moves from synchronous to background | Any operation exceeding 5 seconds | Default |

### Performance — Client (`P-C#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| P-C1 | Page load time (95th percentile) | Time for 95% of page loads to be interactive | At most 2 seconds | Default |
| P-C2 | Page load time (99th percentile) | Time for 99% of page loads to be interactive | At most 5 seconds | Default |
| P-C3 | Interactive filtered query time (95th percentile) | Time for 95% of filter operations on lists up to 1000 rows | At most 1 second | Default |
| P-C4 | Asynchronous operation threshold | When an operation moves to background with notification | Operations exceeding 5 seconds | Default |
| P-C5 | Maximum rows per page | Largest result set returned in a single response | 100 rows | Default |
| P-C6 | Accessibility conformance | Standards for usability by people with disabilities | Web Content Accessibility Guidelines 2.1 Level AA | Default |
| P-C7 | Desktop responsive breakpoint | Minimum width at which the interface must work as a desktop layout | 1024 pixels | Default |
| P-C8 | Tablet responsive breakpoint | Minimum width for tablet-class display | 768 pixels | Default |
| P-C9 | Mobile responsive breakpoint | Minimum width for mobile-class display | 375 pixels | Default |
| P-C10 | Browser support | Which browsers and versions are tested and supported | Last 2 major versions of Chrome, Firefox, Safari, Edge | Default |
| P-C11 | Internationalization at launch | Languages supported at first release | English only; code structured to support more later | Default |

### Performance — Engineering (`P-E#`)

| # | Requirement | What it means | Target | Typical evidence |
|---|-------------|---------------|--------|------------------|
| P-E1 | Application read response time (95th percentile) | Time for 95% of read requests to respond | At most 500 milliseconds | Default |
| P-E2 | Application read response time (99th percentile) | Time for 99% of read requests | At most 1 second | Default |
| P-E3 | Database query response time (95th percentile) | Time for 95% of database queries | At most 200 milliseconds | Default |
| P-E4 | Full-table scans on user-facing paths | Database queries that scan every row to serve a request | 0 (zero) | Default |
| P-E5 | User-facing queries served from a database index | Portion of user-facing queries that use an index | 100% | Default |
| P-E6 | Provisioned throughput capacity | How much above expected peak the system is designed for | 5 times expected peak concurrent users | Default |
| P-E7 | Linear scaling without architecture rework | Up to what multiple of peak load the system scales without redesign | 5 times peak | Default |
| P-E8 | Spare capacity headroom at handoff | Headroom above current production load when the project ships | At least 2 times current load | Default |
| P-E9 | Latency verification before handoff | How performance targets are proven | Load test against measurable targets, not dev-time observation | Default |

---

## 6. How to add project-specific rows

After the starter catalog is in place, read THIS project's sources and **append** rows. Never bake a named company, person, repo, or product into this skill; put current-run names only in the output, via the placeholder tokens.

### 6.1 Standard Open questions (include unless the source already answered them)

These cannot be safely defaulted. Add them as **Open** with target `To be answered by {Client}` (or `{End customer}` / `{Technical contact}` when that party owns the answer). If a source answers one, promote it to Explicit or Implied and write the real target.

**Reliability**

| Suggested # | Requirement | Why it cannot be defaulted |
|-------------|-----------------|----------------------------|
| R-C6 | Contractual uptime commitment | A written SLA is a commercial fact |
| R-C7 | Data freshness expectation | How current displayed data must be versus `{Upstream system}` |
| R-E13 | Inherited reliability targets | Whether existing systems have SLOs this work must honor |
| R-E14 | Post-handoff incident response owner | Who is paged after delivery |

**Security**

| Suggested # | Requirement | Why it cannot be defaulted |
|-------------|-----------------|----------------------------|
| S-C11 | Regulatory regime applicability | HIPAA / GDPR / SOC 2 / PCI / FedRAMP / none is a client representation |
| S-C12 | Existing data-handling agreements | DPA / BAA / customer contracts that bind the build |
| S-C13 | End-customer identity-provider federation | Whether `{End customer}` will expect their own login / SSO later |
| S-C14 | Audit log retention period | Default is 1 year; longer if a regime applies — ask |
| S-E11 | Audit log destination | Application database only versus a central store |
| S-E12 | Role matrix source | Inherit an existing taxonomy versus define one |
| S-E13 | Pre-launch security review owner | Who signs off before `{End customer}` goes live |

**Cost**

| Suggested # | Requirement | Why it cannot be defaulted |
|-------------|-----------------|----------------------------|
| C-C7 | Target delivery date | External dates are contractual |
| C-C8 | Monthly infrastructure budget | Operating-cost ceiling |
| C-C9 | Paid dependency scope | Who pays for error tracking, APM, and similar |
| C-E4 | Approved tool or vendor list | Restrictions on what software can be used |

**Operations**

| Suggested # | Requirement | Why it cannot be defaulted |
|-------------|-----------------|----------------------------|
| O-C6 | User Acceptance Testing requirement | Whether `{End customer}` must sign off before go-live |
| O-C7 | Bug-filing channel | Where defects are tracked |
| O-C8 | Release cadence | How often the system is updated |
| O-C9 | Named handoff recipient | Who on the inheriting team owns the system after delivery |
| O-E19 | Additional environments | UAT or per-tenant preview beyond the 3-env default |
| O-E20 | Existing continuous-integration pattern | Conform to an existing pipeline versus choose |
| O-E21 | Existing observability stack | Plug into current tooling versus stand up new |
| O-E22 | Endpoint / laptop security posture | Device management, network, install permissions |
| O-E23 | AI coding tool permissions | Whether assistants and copilots are allowed |
| O-E24 | Local container and package install permissions | Whether the delivery team can install runtime tooling |
| O-E25 | Code review and approval workflow | Review, release manager, or direct commits |
| O-E26 | Deployment target | Cloud, region, and runtime for the packaged application |

**Performance**

| Suggested # | Requirement | Why it cannot be defaulted |
|-------------|-----------------|----------------------------|
| P-C12 | Total end-customer user count | How many people will use the system once live |
| P-C13 | Peak concurrent users | How many users at once during the busiest period |
| P-C14 | Domain display requirements | Which entities and attributes the UI must show (from `{Upstream system}` / `{Technical contact}`) |
| P-C15 | Export capability | CSV / Excel / PDF or none |
| P-C16 | Reporting and dashboards | Summary views or charts in scope |
| P-C17 | Mobile and tablet usage | Whether staff use non-desktop devices |
| P-E10 | Upstream corpus size and growth rate | How much data is stored and how fast it grows |
| P-E11 | Schema stability during build | Whether the data model will change while we build |
| P-E12 | Existing query patterns to reuse | Optimized patterns in `{Upstream system}` worth mirroring |

### 6.2 Explicit / Implied rows that appear only when the source speaks

Add a new row (next unused ID) when the current SOW or notes state or clearly imply any of the following. Leave them out when the source is silent — do not invent.

| Topic | Typical perspective | Evidence | What to capture |
|-------|---------------------|----------|-----------------|
| User-initiated writes versus read-only | R-C | Explicit if stated | 0 writes this engagement, or the allowed mutations; future-state writes called out of scope |
| Authentication approach | S-C / S-E | Explicit if stated | Built-in framework auth, SSO, or existing IdP; note a swap-point if future SSO is likely |
| Role structure and tenant scoping | S-C | Explicit if stated | Minimum roles (e.g. end-customer read-only vs `{Client}` staff); 0 cross-tenant access; 100% role-filtered reads |
| Multi-tenant architectural readiness | S-C | Explicit or Implied | Seams now (tenant column, scoped queries, tenant context) versus single-tenant only |
| Authorization layer (if they called it out) | S-E | Explicit | Promote S-E1 if they named the layer |
| Data-source / codebase reuse | C-E / O-E | Explicit if stated | Required reuse of `{Upstream system}` and `{Source repo}` versus greenfield |
| Inheriting-team stack fluency | C-E | Implied if an existing app in the same stack is cited | Confirm a named maintainer on the inheriting team |
| UI technology baseline | P-C | Explicit if stated | Admin UI / design system / custom UI; future-state custom UI out of scope if said |
| Deployment packaging | O-E | Explicit if stated | Containerized, VM, serverless, etc. |
| Code repository location | O-E | Explicit if stated | `{Source repo}` and branch-versus-new-repo |
| Technical contact during build | O-C / O-E | Explicit if named | `{Technical contact}` provides data model, access, and architectural context |
| Post-handoff ownership | O-C | Implied if "we will run it" is said | Inheriting team; still Open until a person is named |
| Handoff / deploy documentation commitments | O-C | Explicit if the SOW lists them | Install, configure, deploy, roll back, monitor; architecture + runbooks + onboarding |
| Regulatory position | S-C | Implied if `{Client}` said "no regime" | Record the representation; contract should formalize it — do not invent "no regime" |
| Soft-launch / pre-contract access | O-C | Explicit or Implied | Who may use the system during the build versus after `{End customer}` is authorized |

For each added row: one requirement name, one "what it means" clause, one measurable target, one evidence category, one ID.

---

## 7. Trade-offs

Table columns (exact):

```
| # | Trade-off | Dimensions affected | Magnitude | Decision owner |
|---|-----------|---------------------|-----------|----------------|
```

`Decision owner` is one of: **Decided** (cite the source), **Default applied** (`{Client}` can override), or **Open** (name who must answer).

### Common trade-off catalog

Include each row that applies to this engagement. Rewrite the decision from THIS project's sources. Do not carry forward a prior engagement's "Decided".

| # | Trade-off | Dimensions affected | Typical magnitude | How to decide |
|---|-----------|---------------------|-------------------|---------------|
| T1 | Multi-tenant architectural seams now versus refactor later | Security, Cost | About 1 day of upfront work; saves a full refactor when tenant 2 arrives | Default toward seams unless `{Client}` forbids it |
| T2 | Admin / framework UI baseline versus custom user interface | Performance (client), Cost | Custom UI adds weeks of design and front-end work | Explicit if the source named a baseline; otherwise Open |
| T3 | Authentication now with a swap-point for future SSO / external IdP | Security, Cost | About 1 day of upfront work for the seam; avoids a future rewrite | Default toward a provider-shaped interface |
| T4 | Read-only this engagement versus write / admin-side mutations | Reliability, Security, Cost | Writes expand threat model and test surface | Explicit if the source scoped writes; otherwise Open |
| T5 | Availability target — business hours versus 24/7 | Reliability, Cost | Significant infrastructure cost shift if 24/7 | Default 99.5% business hours; `{Client}` can override |
| T6 | Audit log destination — application database only versus shipped to a central store | Security, Operations | 2–3 days of build effort if shipped | Open until `{Client}` names a destination |
| T7 | Capacity planning — small initial user base versus larger future | Performance, Cost | Defaults to 5× peak; small initial count means low absolute capacity | Default applied until P-C12 / P-C13 are answered |
| T8 | Regulatory posture — confirmed regime versus "none stated" | Security, Cost | A named regime can add 20–40% compliance overhead | Open (or Implied only if `{Client}` stated a position); never invent "no regime" |

Add further `T#` rows for this project only (e.g. reuse-versus-rewrite, single-region DR). Keep names generic in this skill.

---

## 8. Closing sections

### Decision

Write a short prose close (not a table):

1. What is **locked** (Explicit rows that change architecture or scope).
2. What remains **Open**, clustered (operations policy, `{End customer}` specifics, data-model contents, deployment target — whatever is true for this run).
3. Whether the analysis is ready to feed a Solutions Architecture Document, and which SAD sections can be authored now versus which are blocked.

Do not claim completeness when Open rows still bind risk.

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

---

## 9. Output

Write a markdown document named `rscop-<project-slug>.md` (slug from the current project or `{Client}` short name; lowercase, hyphenated).

### Output skeleton

```markdown
# RSCOP Analysis: <short title for this engagement>

**Generated:** <date and trigger, e.g. post-discovery-call>
**Source:** <SOW and/or notes actually used — no prior-client filenames>
**Framework:** RSCOP (Reliability, Security, Cost, Operations, Performance)

This document captures the non-functional requirements for the project. Every row has a measurable target.

**Project context:** <3–6 sentences from THIS run's sources only. Use {Client}, {End customer}, {Upstream system}, {Source repo}, {Technical contact} where names are known or still unknown.>

**How to read each table:** rows are grouped by evidence basis into four categories shown as divider rows.

- **Explicit** — stated by the client; locked.
- **Implied** — inferred from the source; needs explicit confirmation.
- **Default** — baseline applied because the source was silent; must be flagged to the client so they can override.
- **Open** — needs an answer; cannot be safely defaulted.

---

## Project: <same short title>

### Reliability
**Client perspective**
<R-C table>

**Engineering perspective**
<R-E table>

### Security
**Client perspective** / **Engineering perspective**

### Cost
*This section captures operational and effort cost requirements only.*
**Client perspective** / **Engineering perspective**

### Operations
**Client perspective** / **Engineering perspective**

### Performance
**Client perspective** / **Engineering perspective**

### Trade-offs
<T# table>

### Decision
<prose>

### Document-Readiness Summary
<count table + Status line>
```

### SAD handoff

State in Decision (and, if useful, a one-line footer) that this file feeds the SAD skill / Solutions Architecture Document. Typical mapping:

| SAD area | RSCOP source |
|----------|----------------|
| Security Architecture | S-* |
| Infrastructure Architecture / recoverability | R-*, C-* |
| Solution Management (run) | O-*, R-E5, R-E6 |
| Solution Implementation (build) | O-E*, C-E* |
| Data / Application performance | P-* |
| Appendix — trade-off analyses | T* |

Do not author the SAD in this pass unless the user asked for both.

---

## 10. Procedure (run in order)

1. Confirm inputs. List what you have (SOW, notes, stack). List what you lack.
2. Draft **Project context** from this run only. Use the five tokens; never a prior-client name.
3. Copy the **starter catalog** into the five dimensions. Classify each row. Override targets only when Explicit.
4. Append **standard Open** rows that the sources did not answer.
5. Append **project-specific Explicit / Implied** rows the sources actually support (§6.2).
6. Fill the **trade-offs** table from the common catalog plus any this-run extras.
7. Write **Decision** and **Document-Readiness Summary** with real counts.
8. Save as `rscop-<project-slug>.md`.
9. Sweep the output: no prior-client names, no invented facts, every row has a measurable target or a named Open owner.

If the user asks only for a subset (e.g. Security), still apply evidence rules and IDs for that dimension; note that the other dimensions are not in this file.
