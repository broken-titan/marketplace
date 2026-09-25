# Base rules (load with this skill)

## Frameworks are triggers

| Framework | Turns on when | Stays off when |
|---|---|---|
| 21 CFR Part 11 | An FDA predicate rule requires the record, and the record is electronic (§11.1(b)). Food, device, drug, biologics, and tobacco predicates all count. | "We are a lab." LAAF-only records under 21 CFR part 1 subpart R are carved out by §11.1(p) unless another predicate also applies. |
| EU GMP Annex 11 | Computerised systems in GMP-regulated activities for medicinal products (human or veterinary). | Non-GMP testing. Food, environmental, or forensic work by itself. |
| ISO/IEC 17025:2017 | Seeking 17025 accreditation, or a customer/regulator requiring accredited 17025 results. | Doing testing generally. Edition 3, confirmed 2023. There is no 2025 edition. |
| ISO 15189:2022 | Medical laboratory accreditation (human specimens). Report content is clause **7.4**, not 17025's 7.8. | Animal, food, environmental, or forensic testing. Does **not** replace CLIA. |
| CLIA — 42 CFR part 493 | US testing of human specimens for diagnosis, prevention, treatment, or health assessment of an individual. | Forensic-only testing; research that does not report patient-specific care results; SAMHSA-certified workplace drug testing under 42 CFR 493.3(b). |
| HIPAA (45 CFR parts 160/164) | Covered entity or business associate handling PHI. Six-year clock at 164.530(j) is **compliance documentation**, not lab-report retention. | "We store results." Clinical-record retention is state law / payer / overlay, not HIPAA's six years. |
| ALCOA++ | Design lens. Use it to test a schema. It is not a statute. | Citing it as if it were a regulation. |
| PIC/S PI 041-1 | GMP/GDP data-integrity inspections (in force 1 Jul 2021). | Non-GMP labs, unless adopted as design standard. |
| GAMP 5 (2nd ed., 2022) | Validation lifecycle for GxP computerised systems. Custom software is Category 5. | Non-GxP labs, unless adopted as design standard. |
| ASTM E1578-18R26 | Functional-requirements catalog LIMSpec is built on (reapproved 2026). Paywalled; [ASTM store](https://store.astm.org/e1578-18r26.html). Use `limspec-map.md` for checklist content. | Treating it as a binding regulation. |
| GAMP GPG laboratory computerized systems (2nd ed., 2012) | Instrument complexity, raw-data definition, interfacing. Distinct from GAMP 5. [ISPE](https://ispe.org/publications/guidance-documents/gamp-good-practice-guide-gxp-compliant-laboratory-computerized-systems). | Substituting it for GAMP 5 or a statute. |

**Adopted as design standard** is a legitimate posture. Say so. Claiming
unearned legal applicability is itself a finding.

US device QC is **QMSR**: 21 CFR 820 incorporating ISO 13485:2016, in force
2 February 2026. Do not cite the retired QSR subsystem list as current law.

## Required vs. defensive

Before adding a field, argument, or table:

1. **What does the clause literally require?** Usually less than the practice
   built on it. "Identity of personnel responsible" is one identity, not an
   attribute set. Authority and device *controls* must exist; their evidence
   does not have to live in the record.
2. **Is it derivable from something already stored?** A recorded build
   identifier resolves, through version control, every template and pinned
   dependency in that build. Duplicates drift.
3. **Is there a caller that will fill it?** A nullable column for a workflow
   that does not exist is a permanently blank field implying a control the
   system does not have.

Under-building is a finding. Over-building is a different finding.

## 1. Electronic records

- Every regulated record MUST be complete, self-contained, and reproducible:
  store the exact validated input data, not references that can drift.
- Technical records MUST contain results, the issued report, and — if
  possible — enough to identify factors affecting the result and its
  measurement uncertainty, and to repeat the activity under conditions close
  to the original. The factors-affecting limb is why instrument, method,
  environment, and configuration are snapshotted.
- Record the date and the identity of personnel responsible for each
  activity. Add a **separate checker identity only where a review step
  exists**. A blank reviewer column implies a control the workflow does not
  have.
- Define **one canonical record shape** (a single serializer/schema). Every
  sink — database row, embedded artifact copy, event payload — is fed from
  it. A field exists in the canonical shape or it does not exist.
- **Dual-home the record**: the database row and the generated artifact each
  carry the full record. Accepted asymmetries only: the artifact cannot embed
  a hash of its own final bytes; the DB insert timestamp is corroboration,
  not primary data. Issued reports are themselves technical records — retain
  them.
- **Hash across trust boundaries, not within them.** A hash stored in the
  same row as the record is defeated by anyone who can write that row. Where
  the table is immutable at database level (rule 2) the in-row hash is
  redundant twice. The hash that earns its place covers the **artifact
  stored outside the database**. The database record is witnessed by its
  copy embedded in the artifact — which is what the parity test in rule 10
  compares.
- **No foreign keys on compliance records.** Snapshot actor identity and
  config as plain columns. Signature-to-record linking is about binding, not
  relational integrity.
- **No catch-all JSON columns** on compliance records. Every field is named,
  typed, and traceable to an obligation. Document-specific content lives in
  the (already complete) input-data JSON.

## 2. Audit trails

- Record **creation**, not only changes and deletions.
- Amendments MUST be trackable to previous versions or original
  observations. Retain both original and amended data, with the date of
  alteration, what changed, and who changed it. This is the ISO-side
  immutable trail; Part 11 §11.10(e) is the same idea when Part 11 is on.
- Enforce immutability at the **database level** (trigger raising on
  UPDATE/DELETE). Application guards are UX.
- No off switch. The audit write lives in the same transaction as the
  operation.
- Trail retention MUST be at least as long as the records it covers.
- The trail MUST be human-reviewable and copyable: read-only admin with
  search by actor, date, and document identifier, plus an export path.
- **Periodic audit-trail review** is expected, frequency scaled by risk.
  When GMP/GDP is on, cite PIC/S PI 041-1 (in force). Cadences in vendor
  articles are interpretation.

## 3. Timestamps

- The compliance timestamp is when the operator **requested** the action
  (`requested_at`), captured **server-side** at request entry — never from
  the client payload.
- Also record DB insert time (`recorded_at`). The delta is tamper evidence.
- Store UTC. Clock trustworthiness (NTP) is infrastructure; flag it in
  deployment docs.

## 4. Identity and attribution

- Every regulated action MUST have a non-null acting user. Anonymous
  generation must be impossible by construction.
- Snapshot the actor at event time via user-model-agnostic duck-typing.
  The floor is **one identity that resolves to a person without consulting
  current state**. A login identity beats a display name. A stable id
  alongside it is defensible. Do not copy an attribute list.
- Sequencing, authority, and device checks require **the controls to
  exist**. They do not require storing evidence of the check in the record
  unless a caller already produces it and you will ask that question (a
  request id into structured logs often qualifies; token ids and IPs
  usually duplicate the request log).
- Authorization (who MAY act) belongs to the access-control layer.

## 5. Electronic signatures

- **Gate first.** Does an e-signature rule apply to this record? If Part 11
  is off, do not build §11.50 machinery "just in case."
- When a signature manifestation is required, it MUST carry printed name,
  date/time executed, and **meaning**. Meaning is a constrained choice
  (review, approval, responsibility, authorship) declared by the workflow —
  never free text at signing time.
- All three items MUST appear in the human-readable output, not only in
  the database, and take the same controls as the record.
- Bind signature fields into the same immutable row / hashes so they cannot
  be excised, copied, or transferred by ordinary means (§11.70 when Part 11
  is on). Relational links are neither required nor sufficient.
- Out of scope for application modules (identity platform): identity
  verification, FDA certification / Letter of Non-Repudiation, two-component
  execution, password/token controls. State the boundary in design docs.

## 6. Report content

Do not apply a report-content clause set from the base. Load the overlay
that owns the report:

- ISO 17025 testing/calibration → `references/iso-17025-reporting.md`
- ISO 15189 medical → `references/iso-15189-clinical.md`
- AAVLD veterinary → `references/domain-veterinary.md` (clause 5.10)

Agnostic obligations that still hold once *any* report overlay is on:

- Unique identification of the issued document, plus a clear end-of-report
  marker.
- Results relate only to the items actually examined.
- Deviations from the method, and results from external providers, have
  named fields — these are the two most often missing from schemas.
- Customer-supplied data is marked as such.
- A pass/fail or in-tolerance field **is** a statement of conformity: once
  present, record scope, specification, and decision rule. One boolean is
  not enough.
- An interpretation is not another result column. It needs its own block,
  its own authorized person, and a stored basis.
- Per-page identification, measurement-uncertainty triggers, and "valid
  reasons" omission hatches are **overlay-specific**. Do not assume
  17025's answers.

## 7. Document generation and regeneration

- Pipeline: validate input → render → hash input and output → store the
  artifact → write the immutable audit event (same transaction) → dispatch
  notifications. Rendering stays a pure function.
- **Record `app_version` (git SHA / deploy tag) on every generation**,
  injected at build time. Where templates ship in the build, this resolves
  the exact bytes that shaped the output. Change-control obligations are
  **process** requirements met by version control and review — they do not
  ask each record to fingerprint its own templates.
- Hash render inputs only when the build identifier stops resolving them
  (templates in the database, on a volume, or operator-editable). Hash a
  **declared file list per document type**, with a test that no file under
  the render roots is unlisted. Do not hash whole directories. Do not
  hand-bump a version constant.
- **Gate re-issue before building it.** If every generation allocates a
  fresh unique number, replacement clauses never engage. Where re-issue is
  a real workflow: unique identifier (base + monotonic issue suffix) and an
  explicit "replaces" reference to the immediately preceding identifier.
  Allocate the identifier in its own short transaction **before** rendering;
  increment a per-series counter with a database-side expression and commit
  before the render. Never hold a lock across the render. Prefer failing a
  collision loudly over retrying a render.
- Numbering is **accountable rather than gapless**. A failed generation
  after allocate burns a number; write the failed attempt as an event.
  Verification flags an allocated number with no row — a killed process.
- Prefer **PDF/A-3u** for the archived rendition and embed the canonical
  record JSON. A-3 is the variant that permits arbitrary embedded files;
  **u** mandates Unicode text mapping. Validate with an external validator
  (veraPDF) in CI or the verification command. Do not store the variant in
  the database — the file declares it in XMP.

## 8. Storage and retention

- Store artifacts via the framework's storage abstraction. Secrets from
  env/key vault, never from DB config rows.
- Retention is a **configurable class + floor**, never a hardcoded year in
  this skill. Model per record family with its own **anchor** (creation
  date, method lifecycle, rolling last-entry, in-use with no fixed term).
  `created_at + TTL` cannot express the last three. Store the applicable
  **floor** beside the configured value so config cannot go below it.
  Overlay files name floors that actually bind. HIPAA's six years
  (45 CFR 164.530(j)) is documentation, not lab-report retention.
- Back-up, archive, retrieval, and **disposal** are in scope of record
  control, not purely infrastructure. A defined disposal control is
  required even when the chosen policy is indefinite retention.
- Apply **WORM / immutability** on the object store (time-based retention
  and/or legal hold). Lock a time-based policy. Version + version-level
  immutability if names may be overwritten.
- Never hard-delete within retention. Compliance records get no soft-delete.
- Record storage backend and URI on each event so retrieval is mechanical.
- An external provider does not absorb the laboratory's obligation.

## 9. Data integrity — ALCOA++ as a design lens

Ten attributes. FDA CGMP Q&A still uses base ALCOA; WHO TRS 1033 Annex 4
and PIC/S PI 041-1 use ALCOA+ (9); EMA (2023) formalized ALCOA++ (10,
adding Traceable). Use all ten as design tests. They are not a statute.

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
| Traceable | Every value linked to origin and change history via the trail |

## 10. Verification tooling

- Ship a verification command that re-hashes stored artifacts, checks
  DB↔artifact parity, validates archival-format conformance, and reports
  events past retention — **without deleting anything**. Scheduled runs
  are evidence of periodic review.
- Write a **parity test**: serialize the DB record, extract the embedded
  record from the artifact, assert identity (minus accepted asymmetries).
- Calculations and data transfers are checked systematically — cite the
  active overlay's information-system clause for this tooling.

## 11. Event distribution

- Emit an in-process signal after the audit record commits. Receivers are
  connectors registered from config. Ship the signal even with no receiver.
  Do not add a default logging receiver that duplicates request middleware.
- Distribution is best-effort and MUST NOT block or roll back the
  compliance write.

## 12. Portability and isolation

- No imports from sibling apps. Hard requirements documented. Optional
  integrations lazily imported with clear errors.
- If the module uses a package, the module's docs declare it.
- Platform-specific context enters through optional caller-supplied
  parameters.

## First-class objects (any lab)

Named rules **O1–O20** live in `references/base-objects.md`. They are
software, not footnotes. Summary: equipment lock-out; reagent/lot gates;
versioned method; metrological traceability; named interfaces; original
dynamic instrument data; OOS/OOT incident; QC/PT as types; §11.10(f)–(h)
as schema when Part 11 is on; `open_system` / §11.30; §11.70 linking;
unique write identity; competency **gate** (HR files stay organizational);
failure + downtime mode; versioned config; append-only CoC; cybersecurity
independent of privacy flags; backup = verified true copy; physical-sample
vs record retention; refuse privacy-erase inside a regulated keep.

## What code cannot cover

True organizational items only:

- Validation **documentation** (GAMP 5 Category 5 when GxP is on). The
  validate-including-interfaces **gate** is software (O5, O15).
- Written SOPs that hold people accountable for actions under their
  signatures; HR competency **files**. The write-path competency **gate**
  is software (O13).
- FDA certification / Letter of Non-Repudiation when Part 11 signatures
  are legally required.
- Accreditation visits and the certification program itself.
- Identity proofing, password policy, MFA (identity platform).
- NTP as infrastructure (flag it in deployment docs).

§11.30 open-system encryption/digital-signature measures are software
when `open_system` is on — see O10. Backup as a verified true copy is
software (O18); crash dumps do not qualify.

## Design-review gate

Answer all of these against the **profile** (or explicit flags), not
against a guessed lab type:

1. Which overlays are on, and is each "legally required" or "adopted as
   design standard"?
2. Is every regulated action attributable to a non-null actor snapshot —
   plus a checker identity if and only if the workflow has a reviewer?
3. Is the audit record immutable at the DB level and written in the same
   transaction as the action?
4. Is the compliance timestamp server-side request time, with insert time
   as corroboration?
5. Are all copies fed from one canonical shape, with a parity test?
6. Does every recorded hash cross a trust boundary?
7. Is the build identifier recorded, injected at build time, and does it
   resolve the render inputs?
8. If this issues reports: unique identification; race-free allocation
   without locking across the render; replacement references the specific
   document it replaces — only where re-issue is a real workflow. Report
   *content* checked against the loaded overlay, not this base file.
9. Can the record be retrieved, re-rendered, and verified years later
   without this codebase's current state?
10. Is everything code cannot cover flagged as organizational?
11. **Proportionality.** Can every field name the obligation it serves?
    Strike anything derivable or unfilled.
12. Are failures recorded as events rather than raised into the void?
13. Does each named object in `base-objects.md` (O1–O20) exist in
    the design, not as an SOP footnote?

## Currency

- **ISO/IEC 17025:2017 is current.** Claims of a 2025 edition are false.
  ISO catalogue: 2017 confirmed 2023 (stage 90.93), no successor. Next
  systematic review around 2028.
- **QMSR** (21 CFR 820 + ISO 13485:2016) in force 2 February 2026.
- **FBI QAS** for forensic DNA testing and databasing: text effective
  1 July 2025, not retroactive.
- **EU Annex 11**: binding text remains January 2011. Draft revision
  (consultation closed 7 Oct 2025) is not in force. Draft Annex 22 (AI)
  is on the same track.
- **ILAC** ceased 31 December 2025; functions passed to the Global
  Accreditation Cooperation on 1 January 2026. Cite ILAC documents by
  number (e.g. ILAC-G8:09/2019).
- **CLIA**: CMS/CDC RFI 16 July 2026 does not change 42 CFR 493.

