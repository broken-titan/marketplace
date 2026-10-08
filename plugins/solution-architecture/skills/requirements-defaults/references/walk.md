# NFR category walk

## The two-tier model

**Functional requirements:** what the system *does*. Features, user flows, business processes.

**Non-functional requirements:** how the system *behaves*. Performance, security, reliability, and the rest. NFRs slip when teams focus only on features — call them out explicitly every time.

The matrix below is NFRs. Functional requirements get captured separately.

---

## Requirement Categories

Each category has: client-side concern, engineering-side concern, common discovery questions, and a sensible default for a small-to-medium web/SaaS application. Defaults assume a typical web app at <10K users; scale the targets up when the engagement is larger.

### 1. Performance & Scale

RSCOP: P (performance, scalability, capacity)

**Client-side concern:** "Will the app feel fast to my users? Will it survive a busy day?"

**Engineering-side concern:** "What are the latency targets I'm designing against, and at what scale do they have to hold?"

**Discovery questions:**
- Total users? Peak concurrent users?
- Typical operation: how many rows / how much data per query?
- Acceptable page load time and query latency?
- Expected growth — 2x in a year? 10x?
- Bursty load patterns (end-of-month reports, etc.)?
- Exports / batch operations — sync or async tolerable?

**Sensible defaults (if client silent):**
- Page load p95 ≤ 2s
- Interactive query p95 ≤ 1s for ≤ 1000 rows
- Throughput: design for 5× expected peak concurrency
- All list views paginated server-side; no unbounded result sets
- Operations > 5s become async with notification
- Database queries indexed against actual query patterns; no full-table scans on user-facing paths

### 2. Reliability & Continuity

RSCOP: R (reliability, availability, recoverability)

**Client-side concern:** "Will it be there when I need it? What happens if something breaks?"

**Engineering-side concern:** "What's my uptime budget, what failure modes are tolerable, and how fast must I recover?"

**Discovery questions:**
- Uptime target — 99.5% / 99.9% / 99.99%? Business hours or 24/7?
- Behavior under upstream/dependency outage — fail open, fail closed, graceful degradation?
- RPO (data loss tolerance) and RTO (recovery time tolerance)?
- Backup retention period?
- DR posture — single-region OK, or multi-region required?
- Incident response — who's on call, what's the response SLA?

**Sensible defaults:**
- 99.5% availability during business hours (one nine higher than internal tools usually need)
- RPO transactional ≤ 1h; sourced/read-only ≤ 24h via backups; RTO ≤ 4h
- Graceful degradation: read-only mode + status banner when dependencies are down
- Circuit breakers + timeouts on all upstream calls
- Health-check endpoint + automated restart on failure
- Zero data loss on acknowledged writes (transaction guarantees)

### 3. Security & Compliance

RSCOP: S (security and compliance)

**Client-side concern:** "Is my data safe? Are we compliant? Will an audit pass?"

**Engineering-side concern:** "What's the threat model, where are the trust boundaries, and what controls are required vs. nice-to-have?"

**Discovery questions:**
- Regulatory regime — HIPAA, GDPR, SOC 2, PCI, FedRAMP, FDA, industry-specific?
- Data classification — PII, PHI, financial, public?
- Auth — existing IdP / SSO? Protocol (OIDC/SAML)? MFA required?
- Authorization model — role-based, attribute-based, row-level?
- Audit logging — what events, retention period, queryable by whom?
- Encryption requirements — at rest, in transit, field-level?
- Required security review / pen test before launch?
- Existing DPA / BAA / customer contracts that bind us?

**Sensible defaults:**
- TLS 1.3 required; 1.2 minimum; HSTS enabled
- All secrets in a vault (AWS Secrets Manager, Vault, or equivalent), never in source or env files in source
- OWASP Top 10 mitigated; dependency scanning in CI
- Authorization enforced at the data-access layer (not only at the UI/controller layer); cross-tenant leakage test in CI
- Audit log of all writes + sensitive reads, retained 1 year (extend if compliance regime demands)
- Session timeout 30 min idle; re-auth for sensitive actions
- Database encrypted at rest (vendor default usually OK)
- No PII in application logs

### 4. Operability & Maintainability

RSCOP: O (operability and maintainability)

**Client-side concern:** "Can my team keep this running after handoff without calling you every week?"

**Engineering-side concern:** "Can I deploy safely, observe production, and respond to incidents without heroics?"

**Discovery questions:**
- Required environments — dev, staging, prod, UAT?
- CI/CD existing pattern, or do we choose?
- Observability stack — logging, metrics, tracing, errors? (Datadog, Sentry, CloudWatch, ELK)
- Alert routing — who gets paged, what channel?
- Release cadence — continuous deploy, weekly, scheduled?
- Feature flag system in use?
- Test data — provided, scrubbed prod, or synthesized?
- Code repo location and branching model?
- Handoff scope — what docs, what training, what knowledge transfer?

**Sensible defaults:**
- Three environments: dev (local), staging, prod
- CI on every push: lint + tests + dependency scan
- CD: staging on merge to main, prod via tagged release or approved button
- Structured logging (JSON), error tracking (Sentry-class), metrics on golden signals (latency, traffic, errors, saturation)
- Alert on prod errors > baseline + latency > SLO + dependency failures
- README + architecture-at-a-glance + deploy runbook + incident runbook
- Every alert has a runbook entry before it's wired up
- Onboarding doc: new engineer productive in ≤ 5 days

### 5. Usability & Accessibility

RSCOP: usually client P, or a separate UX track

**Client-side concern:** "Will my users be able to use this? Will it work for everyone we need to serve?"

**Engineering-side concern:** "What's the design source of truth, and what accessibility floor must we hold?"

**Discovery questions:**
- Existing design system / style guide? Designer assigned to this engagement?
- Target devices — desktop, tablet, mobile? Field use vs. office?
- Browser support matrix — modern evergreen, or legacy stragglers?
- Accessibility requirements — WCAG 2.1 AA (typical), AAA (rare), Section 508 (government)?
- Internationalization — English-only, or multi-locale?
- Existing user research / personas we can reference?

**Sensible defaults:**
- Component library: Tailwind + a headless library (Radix, Headless UI) or Bootstrap defaults if no design system
- Responsive: works ≥ 1024px desktop and ≥ 375px mobile; tablet incidental
- Browsers: last 2 versions of Chrome, Firefox, Safari, Edge
- Accessibility: WCAG 2.1 AA — keyboard nav, alt text, sufficient contrast, labeled forms (web/SaaS only; skip if envelope is not A)
- English-only unless explicitly scoped
- Error messages and empty states explicitly designed (not framework defaults)

### 6. Interoperability & Integration

RSCOP: integration / interoperability — SAD Integration Architecture

**Client-side concern:** "Does it play nicely with the systems I already have?"

**Engineering-side concern:** "What contracts am I binding to, what's the change posture of upstream systems, and what's my failure isolation?"

**Discovery questions:**
- Upstream systems we read from? Existing API contracts? Versioning policy?
- Downstream systems we write to? Synchronous or via event/queue?
- Data freshness expectation — live, eventual, batched?
- Existing integration patterns at the client we should mirror?
- Webhook / event-emission needs for downstream consumers?

**Sensible defaults:**
- All integrations through declared interface modules (one place to change when upstream changes)
- Async (queue/event) for any operation that doesn't need synchronous response
- Retry with exponential backoff + dead-letter queue for failed upstream calls
- Schema validation at integration boundaries (typed clients, serializers, or equivalent)
- Mock/stub layer for upstream services to enable testing without dependencies

### 7. Extensibility & Portability

RSCOP: weakly under Cost ("minimal rework"); extensibility and portability

**Client-side concern:** "Can we evolve this when our needs change? Can we move it if we have to?"

**Engineering-side concern:** "What change vectors are likely, and where do the seams need to be?"

**Discovery questions:**
- Anticipated future features / customers / regions / tenants?
- Cloud-portability requirement, or specific vendor lock-in acceptable?
- Open-source vs. proprietary component preferences?
- Plug-in / extension model needed for third parties?

**Sensible defaults:**
- Multi-tenant: design seams (tenant column on every row, tenant-scoped queries, tenant context at the request boundary) even if shipping single-tenant
- Cloud-agnostic where cheap (postgres, redis, S3-compatible storage); vendor-specific where it pays off (managed services)
- Twelve-factor app: config via env vars, stateless processes, externalized stores
- Major business rules in named, testable functions — not buried in controllers, views, or templates

### 8. Cost & Constraints

RSCOP: C — a constraint layer in practice, not a quality characteristic.

**Client-side concern:** "What does this cost to build, run, and own?"

**Engineering-side concern:** "What's my budget envelope, and what trade-offs is the client willing to accept to stay inside it?"

**Discovery questions:**
- Build budget envelope?
- Target delivery date? Any hard external dates (demo, contract)?
- Infra budget envelope (monthly run cost)?
- Existing infra they want to use vs. greenfield?
- Paid dependencies (Sentry, Datadog, etc.) — in our scope or theirs?
- Post-launch maintenance — on us, on them, or shared?
- Vendor preferences / restrictions?

**Sensible defaults:**
- Infra: cheapest tier that meets reliability/perf targets; provision for 5× peak; auto-scale where it pays off
- Hosting: client's existing cloud account; we don't run prod for them
- Dependencies: prefer mature open source; paid services only when buy clearly beats build
- Maintenance: defined warranty period (e.g., 30 days post-handoff for bug fixes); anything beyond is a new engagement

---

## Mapping to the SAD

The Solutions Architecture Document has this structure. Each section maps to categories above:

| SAD Section | Sources from |
|---|---|
| Solution Overview | Functional requirements + Cost & Constraints |
| Business Context | Functional requirements + stakeholder map |
| Conceptual Solution Overview | High-level architecture diagram (synthesized) |
| Information Architecture | Usability & Accessibility |
| Application Architecture | All NFRs + tech stack decisions |
| Data Architecture | Performance & Scale + Security & Compliance |
| Integration Architecture | Interoperability & Integration |
| Infrastructure Architecture | Reliability & Continuity + Cost |
| Security Architecture | Security & Compliance |
| Solution Implementation | Operability & Maintainability (build side) |
| Solution Management | Operability & Maintainability (run side) + Reliability |
| Appendix | Trade-off analyses, POC outcomes |

A discovery walk of the 8 categories above gives you the spine of a SAD. The progression is:

1. **Discovery call** → fill `docs/<slug>-nfr-discovery.md` (HIT/MISS/DEFAULT/ASK)
2. **RSCOP analysis** → turn the matrix into measurable rows in `docs/rscop-<slug>.md`
3. **SOW** (input, if it exists) → lock the matrix into commitments; this skill does not write the SOW
4. **Build phase week 1** → analysis becomes the SAD's "Business Context" and NFR sections (`docs/sad-<slug>.md`)
5. **Build phase ongoing** → SAD fills in Application / Data / Integration / Infrastructure / Security architecture sections
6. **Handoff** → SAD is the durable engagement artifact; living specs remain feature-level

Overlays (Well-Architected, NIST 800-53 families, C4/ArchiMate, HIBP, DAST-every-build, extra dialects) stay off until flagged. See `rscop-analysis/references/overlays.md`.

Context-only (not required): TOGAF ADM full cycle, IT4IT R2D, CAF vs WAF, arc42/4+1, INCOSE GTWR, ISO 25010 as why eight categories compress to five letters, Nygard ADR ancestry, Twelve-factor essay. See `rscop-analysis/references/context.md`.

## Two principles

1. **NFRs slip when teams focus on features.** Most clients arrive with a feature list and zero NFRs. Bring the NFR conversation in deliberately. Silence on an NFR is not "no requirement" — it is absorbed risk.

2. **Both perspectives are real.** The matrix forces business and engineering into the same artifact. Do not accept "the engineers will figure it out" as a close on a business question, or "the business doesn't care about that" as a close on a technical one.
