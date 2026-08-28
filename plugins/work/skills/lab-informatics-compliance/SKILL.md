---
name: lab-informatics-compliance
description: Compliance guardrails for building laboratory software — LIMS, LIS, ELN, LES, SDMS, CDS. Covers electronic records, audit trails, electronic signatures, document/report generation, retention, and data integrity. Use when designing, implementing, or reviewing any feature that creates, modifies, stores, signs, exports, or reports laboratory data. Maps rules to 21 CFR Part 11, ISO/IEC 17025:2017, ISO 15189:2022, ALCOA++, EU GMP Annex 11, and PIC/S PI 041-1.
---

# Building laboratory software compliantly

Engineering guardrails for features that touch laboratory records: results, samples,
certificates of analysis, generated reports, signatures, and the events around them.

**MUST** = a regulatory requirement (clause cited). **SHOULD** = a strong expectation
an auditor will probe, or best practice that used to be a requirement. Every rule
carries its source so design decisions are defensible in an audit. A cited clause makes
a design *defensible*; it rarely makes a specific field *required* — read
"Required vs. defensive" below before turning any rule here into a column.

Verified against primary sources July 2026. See "Currency" at the end for what to
re-check and one widely circulated falsehood to resist.

## Where this sits

Three layers, from general to specific — know which one a requirement comes from,
because they have different scopes and different triggers:

1. **Regulated-computerised-system frameworks** — not lab-specific. 21 CFR Part 11,
   EU GMP Annex 11, ALCOA++/data-integrity guidance, GAMP 5. These govern any system
   holding records a regulator requires.
2. **Laboratory informatics** — this skill's level. The ASTM E1578 umbrella for lab
   software. Two tiers within it: **top-level systems** (LIMS, LIS, ELN) that manage
   workflow and own the data of record, and **specialized support systems**
   (LES, CDS, SDMS) that execute procedures or capture instrument data and feed
   upward. LIMS is sample/batch-centric; LIS is patient/specimen-centric — a
   distinction that has blurred since the early 2010s and that vendor naming no
   longer tracks reliably. What matters for compliance is whether the primary object
   is a **sample** (→ ISO/IEC 17025) or a **human patient** (→ ISO 15189 + CLIA).
   Lab systems also integrate with adjacent enterprise systems (ERP, MES, ECM),
   which E1578 explicitly brings into scope.
3. **Sector regimes** — what actually binds a given deployment (veterinary, food,
   clinical, pharma). See `references/domain-regimes.md`, and
   `references/poultry-veterinary.md` for poultry/veterinary work, where the binding
   accreditation standard is often AAVLD AC1 rather than ISO 17025 and the clause
   numbering used below therefore changes.

Rules 1–5 and 8–12 below are layer-1 material applied to lab software; rules 6–7 are
lab-specific.

## Governing frameworks — and when each actually applies

Do not assert that a framework binds a product without checking its trigger. Several
of these are commonly over-claimed.

| Framework | Applies when | Status |
|---|---|---|
| 21 CFR Part 11 | A record is required by an **FDA predicate rule** (§11.1(b)) — *broader than GxP*: food, device, drug, biologics, tobacco rules all count. Not triggered merely by being a lab. | In force; substantively unchanged since 1997 except the Mar 2023 §11.100(c) amendment |
| ISO/IEC 17025:2017 | Testing/calibration lab seeking accreditation, or a customer/regulator requiring it. Basis for AAVLD, A2LA, ANAB programs. | Edition 3, confirmed 2023, current |
| ISO 15189:2022 | **Medical** laboratories (human specimens). Report content is clause **7.4**, not 17025's 7.8. | Edition 4; replaced 15189:2012 + ISO 22870:2016; ILAC transition closed Dec 2025 |
| CLIA — 42 CFR part 493 | US testing of **human specimens** for diagnosis/treatment. Mandatory federal regulation, **not** an accreditation standard — sits alongside ISO 15189, not instead of it. | In force (a CMS/CDC RFI opened July 2026; nothing changed yet) |
| ALCOA+ / ALCOA++ | Universal data-integrity lens applied by inspectors across GxP. | WHO TRS 1033 Annex 4 and PIC/S PI 041-1 use ALCOA+ (9); EMA (2023) formalized ALCOA++ (10, adding Traceable) |
| EU GMP Annex 11 | Computerised systems in **GMP-regulated activities for medicinal products** — *narrower than GxP*. | **Binding text is still the January 2011 revision.** Draft revision published 7 Jul 2025, consultation closed 7 Oct 2025, final expected late 2026, application ~2027 |
| PIC/S PI 041-1 | GMP/GDP data management and integrity inspections. | In force since 1 Jul 2021 — the citable authority for risk-based audit-trail review **today** |
| GAMP 5 (2nd ed., 2022) | Validation lifecycle for GxP computerised systems. Custom-built software is Category 5 (fullest rigor). | Current; no 3rd edition |
| ASTM E1578 | Laboratory informatics terminology, lifecycle, functional requirements. | E1578-18, reaffirmed 2026 |

**Adopting a framework as a design standard is legitimate even when it does not
legally bind you** — Part 11's controls are a sound engineering baseline for any lab
record. Just say which posture you are in ("adopted as design standard" vs "legally
required"), because claiming unearned legal applicability is itself an audit finding.

## Required vs. defensive — read this before designing a schema

Every rule below carries a clause citation. **A citation means "this design satisfies
that clause," not "that clause mandates this field."** Conflating the two produces a
schema full of columns nobody can trace to a requirement and no caller ever fills.

Before adding any field, argument, or table, answer three questions:

1. **What does the clause literally require?** Usually far less than the practice built
   on it. ISO 17025 §7.5.1 requires "the identity of personnel responsible" — *one*
   identity, not an attribute set. §11.10(f)(g)(h) require authority and device
   *controls to exist*, not evidence of them stored in the record. §11.10(k)(2)
   requires change control over systems documentation — version control satisfies it;
   it does not ask each record to fingerprint its own templates.
2. **Is it derivable from something already stored?** A recorded build identifier
   resolves, through version control, every template, constant and pinned dependency in
   that build. Anything reachable that way is a duplicate, and duplicates drift.
3. **Is there a caller that will fill it?** A nullable column for a workflow that does
   not exist is not future-proofing — it is a permanently blank field implying a control
   the system does not have. Add it when the workflow arrives; the migration is cheap.

Under-building is a finding. Over-building is a different finding: it dilutes the
fields that *are* load-bearing and invites an auditor to ask what a blank column was
supposed to mean. Where a rule below reads as a mandate, check it against the clause
text before treating it as one.

## 1. Electronic records

- Every regulated record MUST be complete, self-contained, and reproducible: store
  the exact validated input data, not references that can drift
  (Part 11 §11.10(b); ISO 17025 §7.5.1).
- ISO 17025 §7.5.1 requires technical records to contain results, report, and
  "sufficient information to facilitate, **if possible**, identification of factors
  affecting the measurement result and its associated measurement uncertainty and
  enable the repetition of the laboratory activity under conditions as close as
  possible to the original." Note both limbs — the *factors-affecting* limb is what
  justifies snapshotting instrument, method, environmental, and configuration
  context, not merely inputs and outputs.
- §7.5.1 also requires the date **and the identity of personnel responsible for each
  activity and for checking data and results** — a *separate checker identity*
  distinct from the actor. If a workflow has a reviewer, the record needs a field for
  them.
- Define **one canonical record shape** (a single serializer/schema) and feed every
  sink from it — database row, embedded artifact copy, event payload. A field exists
  in the canonical shape or it does not exist. This prevents silent divergence.
- **Dual-home the record**: the database row and the generated artifact each carry
  the full record, so losing either leaves a complete reconstruction path. Accepted
  asymmetries only: the artifact cannot embed a hash of its own final bytes
  (recompute it from the surviving file), and the DB insert timestamp is
  corroborating evidence, not primary data. ISO 17025 §7.8.1.2 independently requires
  issued reports to be retained as technical records.
- **Hash across trust boundaries, not within them.** §11.10(a) requires the ability to
  discern altered records, and a hash delivers that only when it sits somewhere the
  tamperer cannot reach. A hash of the record stored in the same row as the record is
  defeated by anyone able to write that row — and where the table is immutable at
  database level (rule 2) nobody can, so the hash is redundant twice over. The hash that
  earns its place covers the **artifact stored outside the database**, beyond the
  trigger's reach: that is the independent witness that a blob was not swapped. The
  database record is witnessed instead by its copy embedded in the artifact
  (dual-homing, above) — which is also what the parity test in rule 10 compares.
- **No foreign keys on compliance records.** A record must describe the world *at the
  moment of the event*; an FK dereferences to current state, which is exactly wrong.
  Snapshot the needed fields (actor identity, config values) as plain columns. Part 11
  requires the trail to *identify* the operator, not to link relationally; §11.70
  linking is about signature-to-record binding, not database referential integrity.
- **No `misc`/catch-all JSON columns** on compliance records. Every field is named,
  typed, and traceable to a clause. Document-specific content lives in the (already
  complete) input-data JSON. Add a named column only when a concrete non-universal
  compliance field appears.

## 2. Audit trails

- Record **creation** events, not just changes and deletions. Part 11 §11.10(e)
  already lists "create, modify, or delete"; the draft Annex 11 revision makes
  creation coverage explicit and requires trails to be "always enabled and locked"
  with no ability to deactivate, delete, or silently modify. *(Draft — do not cite as
  in-force; §11.10(e) and ISO 17025 §7.5.2 already carry the requirement.)*
- **ISO 17025 §7.5.2 is the most on-point clause and is often missed**: amendments to
  technical records MUST be trackable to previous versions or original observations;
  **both** original and amended data MUST be retained, including the date of
  alteration, an indication of the altered aspects, and the personnel responsible.
  This is an ISO-side mandate for the same immutable trail Part 11 requires — cite
  both so the design rests on two frameworks.
- Audit records MUST be immutable, enforced at the **database level** (e.g. a
  trigger raising on UPDATE/DELETE), not only in application code. Python guards and
  read-only admin are UX; the DB guarantee is what an auditor accepts.
- There MUST be no off switch, and no code path may create the regulated artifact
  without creating the audit record — put the audit write in the same transaction as
  the operation.
- Trail retention MUST be at least as long as the records it covers (§11.10(e)).
- The trail MUST be human-reviewable and copyable for inspection (§11.10(b), (e)):
  read-only admin with search/filter by actor, date, and document identifier, plus an
  export path.
- **Periodic audit-trail review** is expected, with frequency scaled to system
  criticality — cite **PIC/S PI 041-1 (in force)** for this, not the draft Annex 11.
  Specific cadences ("monthly for high-risk") circulating in vendor articles are
  interpretation, not regulation; set yours by documented risk assessment.

## 3. Timestamps

- The compliance timestamp is when the operator **requested** the action
  (`requested_at`), captured server-side at request entry — **never** accepted from
  the client payload (ALCOA "Contemporaneous"; ISO 17025 §7.5.1 "recorded at the time
  they are made").
- Also record the DB insert time (`recorded_at`, system-generated). The delta is
  tamper evidence, and the system stamp is one the operator cannot influence.
- Store UTC. Clock trustworthiness (NTP) is an infrastructure requirement — flag it
  in deployment docs; the trail is only as credible as the clock.

## 4. Identity and attribution

- Every regulated action MUST have a non-null acting user. Anonymous generation must
  be impossible by construction (§11.10(d) access limiting, §11.10(g) authority
  checks).
- Snapshot the actor at event time via `AUTH_USER_MODEL`-agnostic duck-typing, never
  importing a concrete user model. **The floor is one identity that resolves to a person
  without consulting current state** (ISO 17025 §7.5.1, "the identity of personnel
  responsible") — not an attribute set. Pick it for uniqueness and for being non-blank
  on the actual user model: a login identity beats a display name, which on many models
  is optional and non-unique. A stable id alongside it is defensible — the id survives a
  changed login, the login survives a deleted user row — but check each further
  attribute against the three questions above rather than copying a list. Add the
  separate checker/reviewer identity **only where a review step exists**; otherwise it
  is a permanently blank column implying a control the workflow does not have.
- §11.10(f) sequencing, (g) authority checks and (h) device checks require **the
  controls to exist**. None of them requires storing evidence of the check in the
  record. Record such evidence only where the platform already produces it for free and
  it answers a question you will ask: a request id correlating the row to an existing
  structured-log trace usually qualifies; token ids, source IPs and user agents usually
  duplicate what that same request log already holds. Note that a correlation key's
  value decays with log retention — once the logs age out it points at nothing.
- Authorization itself (who MAY act) belongs to the platform's access-control layer;
  compliance modules trust the caller and record the evidence.

## 5. Electronic signatures

- A signature manifestation MUST carry the printed name of the signer, the date and
  time executed, and the **meaning** of the signature (§11.50(a)(1)–(3)).
- `meaning` is a constrained choice — the regulation's own examples are **review,
  approval, responsibility, authorship**. Never free text, never user-typed at
  signing time: it is a constant declared by the calling workflow per document type.
- All three items MUST appear in the human-readable output, not only in the database
  (§11.50(b)), and are subject to the same controls as the record itself.
- Signature/record linking (§11.70): embed the signature fields in the same immutable
  row, bound by the record's hashes, so they cannot be excised, copied, or
  transferred. The clause is technology-neutral; relational links are neither
  required nor sufficient.
- **Gate first**: does Part 11 even apply to this record (is there a predicate rule)?
  Answer it explicitly before building signature machinery.
- Out of scope for application modules — belongs to the identity/auth platform:
  identity verification (§11.100(b)), certification to FDA / Letter of Non-Repudiation
  (§11.100(c)), two-component signature execution (§11.200), ID-code/password/token
  controls (§11.300). State this boundary in design docs so a manifestation recorder
  is not mistaken for a signature executor.

## 6. Report and CoA content

For **testing/calibration labs**, ISO/IEC 17025:2017 clause 7.8. For **medical labs**,
the governing clause is ISO 15189:2022 **7.4** and every number below shifts.

Clause 7.8.2.1 lists **16 items (a)–(p)**, prefaced "each report shall include at
least the following information, **unless the laboratory has valid reasons for not
doing so**" — required by default, omissible only on documented grounds, with several
items carrying their own internal qualifiers. Do not design against a shortened list;
the full enumeration and its data-model consequences are in
`references/iso-17025-reporting.md`.

The items most often missed, and their schema impact:

- **(n) additions to, deviations, or exclusions from the method** — needs a place in
  the record per result or per assay group.
- **(p) clear identification of results from external providers** — needs a
  subcontracted-result flag.
- **(l) a statement that results relate only to the items tested, calibrated or
  sampled** — a *required content item*, not a disclaimer nicety. Drive the
  tested/calibrated/sampled wording from the report type rather than hardcoding.
- **(c) location of performance**, **(g) condition of the item**, **(a) a title**.

Two frequently-mis-stated points:

- **End-of-report marker is a MUST** (7.8.2.1(d): unique identification that all
  components are recognized as part of a complete report, and clear identification of
  the end). **"Page X of Y" is a SHOULD** — it was a 2005 requirement (5.10.2(c)) that
  was *not* carried into the 2017 edition; NIST's crosswalk marks it "still a best
  practice." It is one good way to satisfy the first half of (d), not a mandate.
  **Check the accreditation standard before relying on this**: AAVLD's requirements
  (SOP 1137 v1; legacy name "AC1") clause 5.10.2.3 *does* require unique identification
  "at the beginning and on each page" of the report, so for an AAVLD-accredited veterinary
  lab per-page identification is required after all — see
  `references/poultry-veterinary.md`.
- **Measurement uncertainty is conditional for test reports** (7.8.3.1(c) — when
  relevant to validity or application of results, when the customer requires it, or
  when MU affects conformity to a specification limit) but **unconditional for
  calibration certificates** (7.8.4.1(a)).

**Statements of conformity are their own clause (7.8.6), not a report-content
detail.** A pass/fail or in-tolerance field on a CoA *is* a statement of conformity,
and once made, 7.8.6.1–2 require the record to carry **three named fields**: which
results the statement covers, which specification/standard is met or not met, and the
decision rule applied (documented with its risk considerations — see ILAC-G8:09/2019).
One boolean is not enough.

## 7. Document generation and regeneration

- Pipeline per generation: validate input → render → hash input and output → store
  the artifact → write the immutable audit event (same transaction) → dispatch
  notification events. Rendering stays a pure function; compliance is the
  orchestrating layer above it.
- **Record `app_version` (git SHA / deploy tag) on every generation.** Where templates
  and stylesheets live in the repository and ship inside the deployed build, this single
  field already resolves — through version control — the exact bytes of every template,
  stylesheet, font and constant that shaped the output, plus the pinned renderer
  version. §11.10(k)(2) asks for change control over systems documentation and ISO 17025
  §7.11.2 for changes to be authorized, documented and validated before implementation:
  both are **process** requirements met by version control and review. Neither asks a
  record to fingerprint its own templates. Confirm the identifier is injected at build
  time — one hand-maintained in an env file cannot distinguish two builds.
- **A content hash of the render inputs earns its place only when the build identifier
  stops resolving them** — templates held in the database, mounted from a volume, or
  operator-editable at runtime. If you get there, hash the declared input set *per
  document type*. Two traps: hashing whole directories cross-contaminates, so an
  unrelated document type's stylesheet edit changes this document's version and two
  byte-identical renders record different versions — which defeats the only question the
  field exists to answer; and a hand-bumped version *constant* drifts. A **declared file
  list whose contents are hashed** avoids both, with a test asserting no file under the
  render roots is unlisted.
- **Regeneration and supersession — gate this before building it.** Ask first whether
  re-issue under the *same* document number is a workflow at all. If every generation
  allocates a fresh unique number, §7.8.8.3 never engages — nothing claims to replace
  anything — and the issue-suffix and "replaces" machinery below is dead weight. The
  clause governs *replacement*, not *repetition*. Where re-issue genuinely is a
  workflow, the rest of this bullet applies; where it is not, one nullable
  caller-supplied "replaces" string added later covers it without an allocator change.
- **Where re-issue is a workflow, get it right — it is commonly botched.**
  Even when every generation is a genuinely new report over different data (not an
  amendment), ISO 17025 §7.8.8.3 requires that a complete new report be **uniquely
  identified** and **contain a reference to the original it replaces**. A boilerplate
  line naming no specific antecedent satisfies neither that clause nor 7.8.2.1(d)'s
  unique-identification requirement if two materially different documents share one
  number.
  **Minimum viable design that preserves an append-only trail** (no supersession
  schema, no mutable links): give every generation its own unique report identifier
  (base number + monotonic issue suffix), and render the immediately-preceding
  identifier for that base number as an explicit "replaces" reference. Two derived
  template values. Also note §7.8.8.1 covers **re-issue**, not only amendment, and
  §7.8.8.2 requires true amendments to take the form of a further document carrying
  an "Amendment to Report, serial number…" statement.
- **Allocate the document identifier in its own short transaction, before rendering,
  and never hold a lock across the render.** The identifier has to appear inside the
  artifact, so allocation precedes rendering — and a naive `max(n)+1` read followed by a
  render and an insert leaves a window in which two generations claim one number.
  Serializing on a per-series counter row closes it: increment the counter with a
  database-side expression and read the value back **inside the same transaction**. The
  UPDATE holds the row lock until commit, so a concurrent caller blocks and then reads
  the committed value. Two statements, microseconds, no lock spanning the render, and no
  dependence on a `SELECT … FOR UPDATE` API (which some backends — Django's SQLite among
  them — do not implement). Keep the unique constraint as defence in depth rather than
  as the mechanism, and prefer failing a collision loudly over retrying a render.
- Numbering is **accountable rather than gapless**: a generation that fails after
  allocating burns a number. Writing the failed attempt as its own event row explains
  every gap, which is what ISO 17025 §7.11.3(e) (record system failures and the actions
  taken) wants regardless. Have the verification job flag an allocated number with no
  corresponding row at all — that is the signature of a process killed mid-flight.
- Prefer **PDF/A** for the archived rendition (§11.10(c)) and embed the canonical
  record JSON as an attachment — one artifact satisfying "human readable **and**
  electronic form" (§11.10(b)), verifiable even if it outlives the database. PDF/A-3
  (ISO 19005-3) is the only variant permitting arbitrary embedded files; **A-1 forbids
  attachments entirely and A-2 allows only embedded PDF/A**. Prefer conformance level
  **u** (`pdf/a-3u`) over `b` — it mandates Unicode text mapping, which is what makes
  the archived text reliably extractable later.
- Renderers do not guarantee conformance. **Validate output with an external
  validator (veraPDF) in CI or the verification command** — treat "we passed a
  variant string" as an intention, not a result. Do not also store the variant in the
  database: a PDF/A file declares its own conformance level in its XMP metadata, and the
  validator reads that claim from the file rather than from you.

## 8. Storage and retention

- Store artifacts via the framework's storage abstraction (e.g. Django `STORAGES`
  aliases), not custom plumbing. Secrets from env/key vault, never from DB config rows.
- **ISO 17025 §8.4.2 (Option A) is the clause for this section** and is easy to miss:
  it requires controls for identification, storage, protection, **back-up, archive**,
  retrieval, retention time, and **disposal** of records, retained "for a period
  consistent with the laboratory's contractual obligations," readily available, with
  access consistent with confidentiality commitments. Two consequences: back-up and
  archive are *in scope of the accreditation requirement*, not purely infrastructure
  concerns to be waved off; and retention is a **per-engagement value**, not a
  platform constant — make it explicit, enforceable config. Per-engagement is the floor
  of the idea, not the ceiling: some regimes anchor retention to a **method lifecycle**
  (AAVLD 5.4.3.2 — as long as the assay is in diagnostic use, plus seven years after it is
  retired), to a **rolling last-entry date**, or to an **in-use lifecycle with no fixed
  term** (9 CFR 439.20(b)(3) carries the last two in one subparagraph), none of which a
  `created_at + TTL` policy can express. Model retention per record family with
  its own anchor, and record the applicable regulatory **floor** alongside the
  configured value so config cannot be set below it.
- Apply **WORM/immutability policies** on the cloud container (time-based retention
  and/or legal hold) so stored artifacts match the DB trigger's guarantee at the
  infrastructure level. Verify the interaction with your upload path: WORM permits
  creating new blobs but blocks overwriting existing names unless versioning plus
  version-level immutability is configured. A time-based policy must be **locked** to
  count as compliance-grade.
- Never hard-delete within retention. Compliance records get no soft-delete either.
  "Permanent" is a defensible policy but it is a *choice about the retention period*,
  not an escape from having a defined one (§8.4.2 requires disposal controls).
- Record the storage backend and URI on each event so retrieval is mechanical
  (§11.10(c) ready retrieval).
- Where storage is managed by an external provider, ISO 17025 §7.11.4 makes the
  laboratory responsible for ensuring that provider complies with applicable
  requirements — cloud storage does not outsource the obligation.

## 9. Data integrity — the ALCOA++ lens

Ten attributes. FDA's 2018 CGMP Q&A still uses base ALCOA; WHO TRS 1033 Annex 4 and
PIC/S PI 041-1 use ALCOA+ (9); EMA's 2023 computerised-systems guideline formalized
**ALCOA++**, adding *Traceable*. A 2026 design should satisfy all ten.

| Attribute | Design test |
|---|---|
| Attributable | Non-null actor snapshot on every event |
| Legible | Human-readable output; readable admin |
| Contemporaneous | Server-side `requested_at` at request entry |
| Original | Immutable event + stored artifact + hashes |
| Accurate | Validated input; hash verification |
| Complete | Canonical record; parity test between copies |
| Consistent | Dual timestamps; monotonic trail |
| Enduring | PDF/A + WORM + retention config |
| Available | Read-only admin, export, verify command |
| **Traceable** | Every value linked to its origin and change history via the audit trail — the ISO 17025 §7.5.2 requirement, expressed as a data-integrity attribute |

## 10. Verification tooling

- Ship a verification command that re-hashes stored artifacts against recorded
  hashes, checks DB↔artifact record parity, validates archival-format conformance,
  and reports events past retention — **without deleting anything**. Scheduled runs
  are the evidence for the periodic-review expectation (PIC/S PI 041-1).
- Write a **parity test**: serialize the DB record, extract the embedded record from
  the artifact, assert identity (minus the accepted asymmetries in rule 1). Drift
  between record homes should be a test failure, not an audit finding.
- ISO 17025 §7.11.6 independently requires that calculations and data transfers be
  checked "in an appropriate and systematic manner" — cite it for this tooling.

## 11. Event distribution

- Emit an in-process signal after the audit record commits (`transaction.on_commit`);
  receivers are the connectors (message bus or webhook receivers registered from
  config). Ship the signal even with no receiver attached — it is a few lines, and
  adding it later means reopening the generation path. Do **not** ship a default
  logging receiver where the platform's request middleware already logs the operation:
  a duplicate line adds nothing, and the database row is the record either way.
- Distribution is best-effort and MUST NOT block or roll back the compliance write:
  the database row is the record; connectors are notification.

## 12. Portability and isolation

- Build compliance modules as if they will be installed on another platform: no
  imports from sibling apps; hard requirements minimal and documented in the module's
  README; optional integrations (cloud SDKs, structured logging) lazily imported with
  clear errors and graceful fallbacks.
- If the module uses a package, the module's docs declare it — never assume the host
  platform ships it.
- Platform-specific context (request ids, token claims) enters through optional
  caller-supplied parameters, not by importing the host's middleware internals.

## What code cannot cover

State these in design docs and PRs so the module is not mistaken for the whole
compliance story:

- **Validation documentation** — GAMP 5 (2nd ed., 2022) risk-based specification and
  verification (traditionally called IQ/OQ/PQ, though GAMP itself no longer prescribes
  that terminology). Custom-built lab software is **GAMP Category 5**, the highest
  rigor tier. ISO 17025 §7.11.2 requires validation *before introduction*, and
  re-validation after changes. Risk-categorize the system before planning validation.
- Written SOPs holding individuals accountable for actions under their signatures
  (§11.10(j)); training and competence records (§11.10(i)).
- FDA certification / Letter of Non-Repudiation Agreement for e-signatures
  (§11.100(c)).
- Systems-documentation distribution and access controls (§11.10(k)(1)). The
  revision-control half (k)(2) is addressed by version control plus the recorded build
  identifier (rule 7) — a process control, not a per-record field.
- Open-system controls (§11.30) if records ever traverse a system whose access is not
  controlled by those responsible for the content — adds encryption and digital
  signature expectations beyond §11.10.
- NTP/clock synchronization; database backups; disaster recovery (note §8.4.2 makes
  back-up and archive an accreditation-scope requirement even when implemented at
  infrastructure level).
- Identity proofing, password policy, MFA — the authentication platform's domain.
- Accreditation and certification programs themselves (AAVLD, A2LA, ANAB, ISO 27001).

## Design-review gate

Before merging any lab-informatics feature, answer all twelve:

1. Which framework actually applies here, and is it "legally required" or "adopted as
   design standard"? (Do not over-claim.)
2. Is every regulated action attributable to a non-null actor snapshot — plus a
   checker identity if, and only if, the workflow has a reviewer?
3. Is the audit record immutable at the DB level and written in the same transaction
   as the action?
4. Is the compliance timestamp server-side request time, with insert time as
   corroboration?
5. Are all copies of the record fed from one canonical shape, with a parity test?
6. Does every recorded hash cross a trust boundary — does it protect something the
   immutability mechanism cannot reach? Delete the ones that do not.
7. Is the build identifier recorded, injected at build time, and does it actually
   resolve the render inputs? If templates can change without a deploy, what covers
   that gap?
8. If this issues reports: is each one uniquely identified; is the identifier allocated
   race-free without holding a lock across the render; and — only where re-issue is a
   real workflow — does a replacement reference the specific document it replaces?
9. Can the record be retrieved, re-rendered, and verified years later without this
   codebase's current state?
10. Is everything code cannot cover explicitly flagged as organizational?
11. **Proportionality.** Can every field, argument and table name the clause it serves?
    Strike any that is derivable from something already stored, or that no existing
    caller will ever fill. Cut before merging — a blank column is a question you will be
    asked to answer.
12. Are failures recorded as events rather than raised into the void
    (ISO 17025 §7.11.3(e))?

## Currency — re-verify before relying on these

- **EU Annex 11 revision**: still draft as of July 2026. Binding text remains the
  January 2011 revision. Check EudraLex Volume 4 for the final before citing the
  expanded audit-trail requirements as in force. Draft **Annex 22** (AI in GMP) is on
  the same track — relevant if AI-assisted features are added; it permits only static,
  locked models in critical applications.
- **ISO/IEC 17025:2017 is current.** Multiple SEO- and AI-generated pages claim an
  "ISO/IEC 17025:2025 published 27 September 2025" with a 2028 transition. This is
  false: ISO's catalogue shows the 2017 edition confirmed in 2023 (stage 90.93) with
  no successor, and no accreditation body has issued a transition communiqué. The 2024
  climate-action amendments applied only to Annex SL management-system standards, not
  to CASCO standards like 17025. Next systematic review is due around 2028.
- **ILAC ceased operations 31 December 2025**; its functions passed to the Global
  Accreditation Cooperation on 1 January 2026. Cite ILAC guidance documents by number
  (e.g. ILAC-G8:09/2019), not by issuing-body currency.
- **CLIA**: a CMS/CDC Request for Information published 16 July 2026 (comments due
  14 September 2026) may lead to future rulemaking. Nothing in 42 CFR 493 has changed.

## Related resources

- **LIMSpec** (limswiki.org, CC BY-SA) — the open, standards-cited *requirements*
  specification for laboratory informatics: 36 subsections of "the system shall…"
  statements, each citing sources, covering the full sample lifecycle plus data
  integrity, configuration management, validation, cybersecurity, and privacy. It is
  complementary, not overlapping: LIMSpec says **what** the system must do; this skill
  says **how to build it so the requirement is actually met**. Cross-reference LIMSpec
  numbers in traceability matrices.
- **ASTM E1578** — the standard guide for laboratory informatics (terminology,
  lifecycle, functional requirements checklist). Paywalled; its content is largely
  reachable through LIMSpec's citations.
- **ISPE GAMP 5 (2nd ed.)** and the GAMP guides on lab systems and on records/data
  integrity — paywalled, organizational/validation-lifecycle focused, complementary to
  the "What code cannot cover" checklist.
- Reference files in this skill: `references/iso-lab-agnostic.md` (the 19 ISO
  requirements that hold whatever kind of lab it is, plus the five places lab type
  changes the answer; start here when the binding standard is not settled yet),
  `references/iso-17025-reporting.md` (the full
  7.8 clause map and its schema consequences), `references/domain-regimes.md` (which
  sector regimes bind which deployments), `references/poultry-veterinary.md` (poultry
  and veterinary work — who each obligation binds, the AAVLD AC1 ↔ ISO 17025 clause
  crosswalk, NPIP reporting as a workflow trigger, retention floors, and how to
  represent Salmonella and coccidia results).
