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

**Related rows:** S-E4, C-C1; Trade-off T1.

### ADR-002 — Test data source

**When it applies:** always. The build needs realistic data.

**Options:**

- **A. Use existing `{Upstream system}` data via `{Source repo}` / client infrastructure** — highest realism; depends on `{Technical contact}` granting access in week 1; watch data-egress and laptop-policy constraints.
- **B. Synthesize test data** — when existing data cannot leave its environment, or no corpus exists.
- **C. Hybrid** — scrubbed subset + synthesized edge cases. Use when A is available but incomplete (missing tenants, missing failure states).

**Pattern rationale:** prefer A when the scope is a view onto existing data and the contractor works on the client's side of the trust boundary. Prefer B/C when egress is forbidden or the model is net-new.

**Consequences:** Section 5 environment requires the chosen source; week-1 schedule depends on access or synthesis time.

**Related rows:** test-data access; add a project-specific row if the source states one. Do not invent a catalog ID.

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

**Related rows:** P-C1 class when envelope is web/SaaS; skip Django-admin default when it is not.

### ADR-004 — Audit log destination

**When it applies:** audit coverage/retention are in the RSCOP (they almost always are). Destination is frequently Open.

**Options:**

- **A. Application database only** — simplest; queryable in-app; sufficient when no central SIEM exists; risk: not searchable with other client streams.
- **B. Application database plus shipped to a central system** — higher integration cost; align with the existing observability/SIEM stack (O-E21 class).
- **C. Direct write to central system only** — loses local queryability for app admins.

**Pattern rationale:** do not pick B/C until `{Client}` names the destination system. Default the *coverage and retention*; leave destination **Proposed** until S-E12 class is answered.

**Consequences:** A keeps 4f and Section 6 self-contained. B/C couple to the observability and possibly deploy-target answers.

**Related rows:** S-E11, S-C14, O-E21; Trade-off T6.

### ADR-005 — Auth approach with swap point for future SSO

**When it applies:** always. SSO may be out of scope now and still arrive later.

**Options:**

- **A. Framework built-in auth, called directly throughout the app** — cheapest; locks a refactor when SSO is added.
- **B. Framework built-in auth behind a provider-shaped interface** — small upfront cost (~1 day); views, admin, and role bindings call only the interface. Future SSO/IdP swaps the implementation.
- **C. Build SSO / external IdP now** — only if an integration target is identified and in scope.

**Pattern rationale:** the seam is cheap relative to a retrofit. The end-customer's eventual IdP is often unknown; the seam protects any reasonable future answer. Future IdP preference **informs** the interface shape; it does not block building the seam.

**Consequences:** 4b has a provider module; views do not import the concrete auth library; 4f documents "swappable"; a future SSO engagement is scoped to the provider module.

**Related rows:** S-C13, T3.

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

**Related rows:** S-E1, S-E4; Trade-off T1.

---

