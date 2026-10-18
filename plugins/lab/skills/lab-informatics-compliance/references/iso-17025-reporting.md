# ISO/IEC 17025:2017 clause 7.8 — report content, and what it means for your schema

Load this when designing or reviewing a report, model ,action, template, serializer, or any other part of the application that creates, updates, or deletes data.

Clause text is paraphrased; consult the standard itself for normative wording.

## 7.8.2.1 — the (a)–(p) list

Prefaced: "Each report shall include at least the following information, **unless the
laboratory has valid reasons for not doing so**, thereby minimizing any possibility of
misunderstanding or misuse." So: required by default, omissible only on documented
valid grounds. Several items carry additional internal qualifiers, noted below.

| Item | Requirement | Schema consequence |
|---|---|---|
| (a) | A title (e.g. "Test Report", "Calibration Certificate", "Report of Sampling") | Report-type constant, not a hardcoded string — it also drives (l)'s wording |
| (b) | Name and address of the laboratory | Config singleton, snapshotted into the record |
| (c) | Location of performance, including when performed at a customer facility, away from permanent facilities, or in temporary/mobile facilities | Per-activity field; often missed entirely |
| (d) | Unique identification that all components are recognized as part of a complete report, **and clear identification of the end** | End-of-report marker is mandatory; unique report identifier must be genuinely unique per issued document |
| (e) | **Name and contact information** of the customer | More than a client name — contact block |
| (f) | Identification of the method used | Per assay group |
| (g) | Description, unambiguous identification, and **when necessary the condition** of the item | Sample condition field |
| (h) | Date of receipt of item(s) and date of sampling, **where critical to the validity and application of the results** | Two distinct dates, both conditional |
| (i) | Date(s) of performance of the laboratory activity | Distinct from (h) and (j) |
| (j) | Date of issue of the report | Unconditional |
| (k) | Reference to the sampling plan and sampling method, **where relevant** | Conditional |
| (l) | A statement that the results relate only to the items **tested, calibrated or sampled** | Required content item, not an optional disclaimer; wording varies by report type |
| (m) | The results with, **where appropriate**, the units of measurement | |
| (n) | Additions to, deviations from, or exclusions from the method | Per-result or per-assay-group field — commonly absent from data models |
| (o) | Identification of the person(s) authorizing the report | Signatory block |
| (p) | Clear identification when results are from **external providers** | Subcontracted-result flag — commonly absent from data models |

**Non-normative note under 7.8.2.1**: the familiar "shall not be reproduced except in
full without approval of the laboratory" line is a NOTE, i.e. guidance, not a
requirement. Do not represent it as mandatory.

### Pagination

"Page X of Y" was an explicit requirement in the **2005** edition (5.10.2(c)) and was
**not** carried into 2017. NIST's crosswalk annotates it "still a best practice."
Treat it as a SHOULD and as one reasonable way to satisfy the first half of (d) — not
as a regulatory MUST. The end-of-report marker in (d) *is* a MUST. Per-page
identification required by other families (AAVLD, 15189) lives in those overlays,
not here.

## 7.8.3.1(c) — measurement uncertainty on test reports

Conditional. MU is reported in the same unit as the measurand (or as a term relative
to it, e.g. percent) when **any** of these is true:

- it is relevant to the validity or application of the test results,
- a customer's instruction requires it, or
- the MU affects conformity to a specification limit.

Design against those three triggers, not a vague "where applicable."

## 7.8.4.1(a) — measurement uncertainty on calibration certificates

**Unconditional.** If the platform ever issues something characterized as a
calibration certificate, MU stops being an optional per-assay decision and becomes
hard required content.

## 7.8.6 — statements of conformity (decision rules)

A distinct sub-clause with its own trigger, not a report-content detail.

- **7.8.6.1**: when a statement of conformity to a specification or standard is
  provided, the laboratory shall **document the decision rule employed**, taking
  account of the level of risk (false accept, false reject, statistical assumptions),
  **and shall apply it**. Where the decision rule is prescribed by the customer,
  regulations, or normative documents, further risk consideration is not necessary.
- **7.8.6.2**: the report shall clearly identify
  (a) to which results the statement of conformity applies,
  (b) which specifications, standards, or parts thereof are met or not met, and
  (c) the decision rule applied, unless inherent in the requested specification.

**Schema consequence** — this is the one most often reduced to a boolean: a pass/fail
or in-tolerance/out-of-tolerance field **is** a statement of conformity. Once you have
one, the record needs *three* named fields: scope of the statement, specification
reference, and decision-rule identity. Companion guidance: ILAC-G8:09/2019 (cite by
document number; ILAC's functions passed to the Global Accreditation Cooperation on
1 January 2026).

## 7.8.8 — amendments and re-issue

Three sub-clauses; all three matter for regeneration design.

- **7.8.8.1**: when an issued report needs to be **changed, amended, or re-issued**,
  any change of information shall be clearly identified and, where appropriate, the
  reason for the change included in the report. Note the trigger includes plain
  re-issue.
- **7.8.8.2**: amendments after issue shall be made **only in the form of a further
  document** (or data transfer) including the statement "Amendment to Report, serial
  number… [or as otherwise identified]" or equivalent wording, and shall meet all the
  requirements of the standard.
- **7.8.8.3**: when it is necessary to issue a **complete new report**, it shall be
  **uniquely identified** and shall **contain a reference to the original that it
  replaces**.

### The regeneration trap

A system that regenerates a report on demand — new data, new filters, same document
number each time — appears to escape 7.8.8 on the theory that each output is a new
report rather than an amendment. That defence only holds if each generation is
**uniquely identified**, which reusing one number gives up; and 7.8.8.3 additionally
requires a reference to the **specific** original replaced, which generic boilerplate
("supersedes any earlier document bearing this number") cannot provide, since it
cannot be resolved to an antecedent from the artifact alone.

**Minimum viable fix, preserving an append-only immutable trail** (no supersession
schema, no mutable links, no foreign keys): give each generation a unique report
identifier — base number plus a monotonic issue suffix — and render the immediately
preceding identifier for that base number as an explicit "replaces" reference. Both
are values derived at render time from the existing event trail.

## 7.5 — technical records

- **7.5.1** requires technical records for each activity to contain the results, the
  report, and sufficient information to facilitate, *if possible*, identification of
  **factors affecting the measurement result and its associated measurement
  uncertainty**, and to enable **repetition of the activity under conditions as close
  as possible to the original**. Both limbs; both qualified. The factors-affecting
  limb is the one that justifies capturing instrument, method, environment, and
  configuration context.
  It also requires the **date and identity of personnel responsible for each activity
  and for checking data and results** (a separate checker identity), and that original
  observations, data, and calculations be **recorded at the time they are made** and be
  identifiable with the specific task.
- **7.5.2** — the single most on-point clause for audit-trail design, and the one most
  often uncited: amendments to technical records shall be **trackable to previous
  versions or to original observations**, and **both original and amended data and
  files shall be retained**, including the **date of alteration**, an **indication of
  the altered aspects**, and the **personnel responsible**.
- **7.8.1.2**: all issued reports shall be retained as technical records.

## 7.8.2.2 — whose information is it

Often missed, and it drives a schema field rather than a sentence. The laboratory is
responsible for all information in the report **except information provided by the
customer**; "Data provided by a customer shall be clearly identified"; "a disclaimer shall
be put on the report when the information is supplied by the customer and can affect the
validity of results"; and where the laboratory was **not responsible for the sampling
stage**, "it shall state in the report that the results apply to the sample as received."

Schema consequence: a **provenance marker per field group** (lab-determined vs
customer-supplied) that the template actually renders, a **conditional disclaimer block**
that fires when customer-supplied data can affect validity, and an "as received" statement
driven by a sampling-responsibility flag rather than buried in free-text disclaimer config.

## 7.8.3.2 and 7.8.5 — when the lab did the sampling

**7.8.3.2** routes a test report into **7.8.5** whenever the laboratory is responsible for
the sampling activity. 7.8.5 then requires, in addition to 7.8.2 and where necessary for
interpretation: (a) the date of sampling; (b) unique identification of the item or material
sampled; (c) the location of sampling, "including any diagrams, sketches or photographs";
(d) a reference to the sampling plan and sampling method; (e) details of environmental
conditions during sampling that affect interpretation; (f) information required to evaluate
measurement uncertainty for subsequent testing.

Schema consequence: **"who collected the sample" is a schema-level switch, not a note.**
When the lab or its agents collect, six additional per-sample fields become required
content — including a location representation able to carry a diagram or photo. Model
sampling responsibility explicitly and make the sampling block conditionally required on it.

Distinct from report content, **7.3.3** enumerates the sampling **records** to retain where
relevant: (a) the sampling method reference; (b) date and time of sampling; (c) data to
identify and describe the sample; (d) the personnel performing sampling; (e) the equipment
used; (f) environmental or transport conditions; (g) diagrams or equivalent to identify the
sampling location; (h) deviations, additions or exclusions from the sampling method and plan.

## 7.4.2, 7.4.3, 7.4.4 — identification, deviations, and storage conditions

- **7.4.2**: a system for the unambiguous identification of items, which "shall ensure that
  items will not be confused physically or when referred to in records or other documents",
  and which shall, **if appropriate**, accommodate sub-division of an item or groups of
  items and their transfer. Consequence: if the sample identifier is not unique *in the
  database*, the printed identity is ambiguous and the model's own constraints prove it —
  check for a uniqueness constraint before claiming 7.8.2.1(g) is satisfied.
- **7.4.3**: deviations from specified conditions shall be recorded **on receipt**. Where
  there is doubt about an item's suitability, or it does not conform to the description
  provided, the laboratory shall consult the customer for further instructions before
  proceeding and **record the results of that consultation**; and where the customer
  requires the item tested anyway while acknowledging the deviation, the laboratory "shall
  include a disclaimer in the report indicating **which results may be affected** by the
  deviation."
  Consequence: **the condition disclaimer is per-result, not per-report.** A single
  report-level condition string cannot express "which results may be affected" — the schema
  needs a row-level affected-by-deviation marker with a deviation description, plus a
  separate record of the consultation and its outcome.
- **7.4.4**: where items must be stored or conditioned under specified environmental
  conditions, those conditions shall be **maintained, monitored and recorded**.

## 7.8.7 — opinions and interpretations

A separate clause from results, and the boundary is easy to cross by accident: any
"consistent with", any species call inferred from a measurement, any prevalence comment.

- **7.8.7.1**: only personnel **authorized for the expression of opinions and
  interpretations** may release the statement, and the laboratory shall **document the basis
  upon which it was made**. Its NOTE distinguishes opinions and interpretations from
  statements of inspection and product certification.
- **7.8.7.2**: they shall be based on the results obtained from the tested item and
  **clearly identified as such**.
- **7.8.7.3**: where communicated directly by dialogue with the customer, **a record of the
  dialogue shall be retained**.

Schema consequence: an interpretation is **not another result column**. It needs a distinct
block, rendered as an interpretation, with its **own authorizing person** — separate from the
7.8.2.1(o) report authorizer and constrained to an authorized set — and a stored reference to
the documented basis. A verbal interpretation is itself a record: a dialogue log.

## 7.11 — control of data and information management

**LIMS/equipment overlay:** `iso-17025-systems.md` (also **6.4**).
This reporting file keeps 7.11 so a serializer review still sees the
information-system cites. 7.11 **ends at 7.11.6**:

- **7.11.1**: access to the data and information needed for laboratory activities.
- **7.11.2**: the laboratory information management system(s) used for collection,
  processing, recording, reporting, storage, or retrieval of data shall be **validated
  for functionality before introduction**, including interfaces. Changes — including
  software configuration changes and modifications to COTS software — shall be
  **authorized, documented, and validated before implementation**. COTS software in
  general use within its designed application range may be considered sufficiently
  validated.
- **7.11.3(a)–(e)**: the system shall be protected from unauthorized access, safeguarded
  against tampering and loss, operated in a compliant environment, maintained to ensure
  data integrity, and shall **record system failures and the immediate and corrective
  actions taken**. That last limb is the one most often missed — a render that raises, an
  upload that fails, or a hash mismatch found by a verification job is a recordable system
  failure, not just a log line.
- **7.11.4**: where the system is managed or maintained **off-site or by an external
  provider**, the laboratory shall ensure the provider complies with all applicable
  requirements — cloud hosting does not transfer the obligation. **Cite 7.11.4 for this,
  not 7.11.3.**
- **7.11.5**: instructions, manuals and reference data relevant to the work shall be made
  available to personnel.
- **7.11.6**: calculations and data transfers shall be **checked in an appropriate and
  systematic manner** — the ISO-side citation for parity tests and verification tooling.

## 8.4 — control of records (Option A)

- **8.4.1**: establish and retain legible records demonstrating fulfilment of the
  standard's requirements.
- **8.4.2**: implement controls for **identification, storage, protection, back-up,
  archive, retrieval, retention time, and disposal**. Records shall be retained for a
  period **consistent with the laboratory's contractual obligations**; access shall be
  consistent with confidentiality commitments; records shall be readily available.

Consequences: retention is a per-family class with a stored floor and its own
anchor, not a platform constant. Method-lifecycle, rolling last-entry, and in-use
anchors cannot be expressed as `created_at + TTL` — those floors live in the
domain overlay that owns them. Back-up and archive fall inside the accreditation
requirement. A defined disposal control is required even if the chosen policy is
indefinite retention. Laboratories electing management-system Option B satisfy
this through an ISO 9001-conformant system instead.
