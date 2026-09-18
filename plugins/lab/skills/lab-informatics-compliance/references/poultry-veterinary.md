# NPIP / poultry official-assay overlay

Load **only** when the profile (or the user) has `npip` on — official
National Poultry Improvement Plan assays or an NPIP-authorized
laboratory. This is not the default veterinary file and not the default
food file. General veterinary / AAVLD / NAHLN work uses
`domain-veterinary.md`. General food / LAAF / FSIS ALP uses
`domain-food.md`.

`domain-regimes.md` routes. `iso-17025-reporting.md` holds the 17025
clause map when 17025 is also on. This file is poultry-specific schema,
workflow, and reporting.

Clause text is paraphrased unless quoted.

## Who each obligation binds

The most common error in this material is attributing an obligation to the laboratory that
actually sits on the establishment, the producer, or the state. A design that internalizes
someone else's duty builds fields nobody needs; one that externalizes its own misses a
deadline.

| Regime | Binds | The lab's actual position |
|---|---|---|
| NPIP 9 CFR 147.52 | The **authorized laboratory** | Directly — but only if authorized *and* running official Plan assays |
| NPIP 9 CFR 145.14 | Whoever collects and tests official samples | Directly — this is the clause requiring an authorized lab |
| NPIP 9 CFR 145.23(b)(2)(i) and parallels | **Any** person performing poultry disease diagnostic services | Directly, and more broadly than 147.52 — no authorization needed to be caught by it |
| FSIS 9 CFR 417.5 | The **official establishment** | Never directly. Reaches the lab contractually, as supporting documentation under 417.5(a) |
| FSIS ALP 9 CFR 439.20 | The **accredited laboratory** | Directly, if ALP-accredited — the retention rule governing the lab's own LIMS |
| FDA 21 CFR 118.10 | The **shell egg producer** | Never directly. The lab's CoA feeds the producer's record |
| FSMA LAAF 21 CFR 1.1152 | The **LAAF-accredited laboratory** | Directly, within LAAF scope |
| ISO/IEC 17025 or AAVLD | The lab, via its accreditation contract | Directly, if accredited or seeking it |

**Router:** if the lab is neither NPIP-authorized nor in LAAF scope, the next three sections
are inapplicable detail — skip to *Retention floors* and *The poultry domain model*, which
apply regardless.

Two consequences worth designing to:

- **417.5(b) requires each entry to be "signed or initialed by the establishment employee
  making the entry."** A lab analyst is not an establishment employee, so a CoA is not a
  417.5(b) monitoring record. Cite subsections, not the bare section: **417.5(b)** is the
  ALCOA-like entry rule, **417.5(c)** the pre-shipment review, **417.5(d)** the
  electronic-records provision, **417.5(e)** retention.
- **417.5(c)** is worth borrowing even though it binds the establishment: "Where practicable,
  this review shall be conducted, dated, and signed by an individual who did not produce the
  record(s), **preferably** by someone trained in accordance with § 417.7 of this part, or the
  responsible establishment official." Note "where practicable" and "preferably" — the review
  is mandatory but reviewer independence is qualified, so build the reviewer-≠-author
  constraint with a **recorded override** rather than as an unconditional rule. This is the
  domain-native twin of ISO 17025 clause 7.5.1's separate checker identity; citing both lets a
  design rest on two frameworks.

## Which accreditation applies — and why the clause numbers change

**AAVLD numbers its clauses on the legacy ISO/IEC 17025:2005 scheme (4.x/5.x)** while this
skill cites 17025:2017's 7.x/8.x. For a US veterinary or poultry lab AAVLD is frequently the
standard actually in force, and its auditors work from the older numbering, so **carry both
citations** in any traceability matrix or PR justification.

A note on the document's identity, because it is easy to cite something that no longer
exists. What aavld.org serves under Qualtrax document control is **"AAVLD Requirements for an
Accredited Veterinary Medical Diagnostic Laboratory," SOP 1137 Version 1, approved 7 February
2023**. Its internal Revision Summary ends at Version 2021-01, and the clause text is
identical to that edition, so the numbering below is current. The legacy document number
**"AC1"** and the version string "V 2021.01" persist in secondary literature (including the
FDA/Vet-LIRN white paper) — treat them as aliases for the same standard, and check the
Qualtrax version before citing a clause.

| AAVLD (SOP 1137 v1, 2021-01 content) | ISO/IEC 17025:2017 | Subject |
|---|---|---|
| 5.10 (items 5.10.2.1–) | 7.8 | Report content |
| 5.10.2.3 | 7.8.2.1(d) | Report identification — **AAVLD is stricter** |
| 4.10 | 8.4 | Control of records |
| 4.4 (incl. 4.4.2) | 7.1 / 7.8.2.1(p) | Request review; subcontracting |
| 5.4.3 (incl. 5.4.3.2) | 7.2.2 / 8.4 | Method validation and its records |

Three AAVLD-specific requirements that change the design:

- **Per-page identification is required (5.10.2.3)**, not merely good practice: "unique
  identification (see 5.8.2.) at the beginning and on each page of the test report to ensure
  that the page is recognized as a part of the test report and a clear identification of the
  end of the report." This **qualifies this skill's most-emphasized mis-stated point.** Under
  ISO 17025:2017, 7.8.2.1(d) has no "each page" language — the end-of-report marker is the
  MUST and "Page X of Y" only a SHOULD. Under AAVLD, repeating the **unique report
  identifier** in a running header or footer on every page is required. Both sit under the
  same "unless the laboratory has valid reasons for not doing so" preamble.
- **Retention is keyed to the method lifecycle, not the record (5.4.3.2)** — see *Retention
  floors* below for the clause text and the formula.
- **The receiving laboratory must be named to the client (4.4.2)** for subcontracted or
  referred work; advisement may occur pre- or post-submission, and the test report is one of
  the named channels. So the subcontracted-result *flag* that satisfies ISO 7.8.2.1(p) must be
  an **external-provider identity field**, not a boolean.

**Scope posture changes whether you flag non-accredited assays.** AAVLD accredits "the entire
laboratory (all laboratory tests and activities), which is a departure from accrediting bodies
that award accreditation on a test by test or technology basis" — per the FDA/Vet-LIRN white
paper and AAVLD's program page rather than the standard itself. WOAH Terrestrial Manual 2024
chapter 1.1.5 states that where an accredited laboratory also offers non-accredited tests,
"these must be clearly indicated as such on any reports that claim or reference
accreditation." So a per-assay `in_accreditation_scope` flag is needed under a scoped posture
(A2LA, ANAB) and is inert under an AAVLD-only posture — make it **config-driven**. Concretely:
Salmonella culture is often inside a scope while a coccidia OPG count is not, so a report
referencing accreditation while listing both must mark the unscoped one.

AAVLD accreditation is **not** ISO/IEC 17025 accreditation. AAVLD is not listed as an ILAC-MRA
signatory: the FDA/Vet-LIRN white paper's comparison attributes MRAs (ILAC, APLAC, IAAC, IAF)
to bodies like A2LA and SCC while listing AAVLD's recognition as coming from the US Chief
Veterinary Officer, USDA-NAHLN and FDA Vet-LIRN. That is corroboration by omission rather than
an affirmative statement — verify against ILAC's signatory register before relying on it. On
that basis, do not put an ILAC-MRA mark on an AAVLD-accredited report.

## NPIP — what authorization actually obliges

The mandate is in **145.14**: "Samples for official tests shall be collected by an Authorized
Agent, Authorized Testing Agent, or State Inspector and tested by an authorized laboratory,
except that the stained antigen, rapid whole-blood test for pullorum-typhoid may be conducted
by an Authorized Testing Agent or State Inspector." 147.52 supplies the criteria for *being*
authorized — so the trigger is the lab's **status**, not the subject matter of the assay.

- **Collector identity is a distinct actor** with an authorization role — Authorized Agent /
  Authorized Testing Agent / State Inspector — captured at collection and separate from the
  technician who ran the assay. The generic "actor snapshot + checker identity" model has no
  slot for an off-site, differently-authorized collector, and no ISO 7.8.2.1 item forces one.
- **145.14(a)(1)** permits official blood tests conducted "in accordance with part 147 ... or
  according to literature provided by the producer", so a method-identification field must be
  able to hold a producer or kit-insert reference, not only an internal method code.

**Reporting is a workflow trigger, and the trigger moved.** 147.52(f)(2) was revised by APHIS
final rule 90 FR 46741 (30 Sept 2025, RIN 0579-AE74, instruction 33), **effective 30 October
2025**:

> All *Salmonella* Pullorum and Mycoplasma Plan disease **infected flocks as confirmed by
> testing in accordance with § 145.14** must be reported to the Official State Agency within
> 48 hours.

The superseded text read "*Salmonella* pullorum and Mycoplasma Plan disease **reactors** must
be reported ... within 48 hours." **Anything built against a pre-2025 CFR edition — or a
summary of one — has the wrong trigger.** The reportable object is now the **flock**, and the
confirming act is testing under 145.14, which is the lab's own testing. So:

- the record needs a **flock identifier that groups results**, not only sample identity;
- it needs a `confirmed_at` (the 145.14 confirmation) distinct from `result_reported_at` and
  from `report_issued_at`, plus `reported_to_osa_at`;
- firing notification on the first positive result **over-reports**; keying it to CoA issuance
  **under-reports**.

**There is no single clock — model a per-disease deadline table.** At least five distinct CFR
reporting regimes apply to poultry diagnostic work, with different triggers, recipients and
terms:

| Provision | Deadline | Trigger |
|---|---|---|
| 147.52(f)(2) | 48 hours | Confirmed infected flock, *S.* Pullorum / *Mycoplasma* |
| 145.23(b)(2)(i) and parallels | 48 hours | Source of any specimen yielding *S.* Pullorum or *S.* Gallinarum — binds **any** person performing poultry diagnostic services |
| 145.34 / 145.44 | 48 hours | Source of *Mycoplasma*-positive specimens |
| 146.24(a)(1)(iii) / 146.44(a)(1)(iii) | **24 hours** | Source of avian-influenza-positive specimens |
| 145.14(a)(9) | 10 days | All pullorum-typhoid tests |

**147.52(f)(1)** is a different mechanism again: a memorandum of understanding "or other
means" establishes testing and reporting criteria with the Official State Agency, "including
criteria that provide for reporting H5 and H7 low pathogenic avian influenza directly to the
Service." So some recipients and deadlines are **per-engagement configuration**, not constants.
A single hardcoded 48-hour clock will be wrong.

**Qualification and proficiency evidence must be audit-retrievable, and the audits are
scheduled:**

- **147.52(a)** — "The authorized laboratory must use the next available check test for each
  assay that it performs." Per assay, not per lab.
- **147.52(b)** — procedures "must be run **or overseen by** a laboratory technician who every
  4 years has attended, and satisfactorily completed, Service-approved laboratory workshops
  for Plan-specific diseases." The qualification attaches to whoever runs *or* oversees, so the
  record needs `overseen_by` alongside `performed_by`, and the 4-year lookup resolves against
  the overseer. A schema with a single "performed by" cannot evidence 147.52(b) when a trainee
  ran the plate under supervision — the normal case.
- **147.52(c)** — official Plan assays "must be performed and reported as described in the
  NPIP Program Standards or in accordance with other procedures approved by the
  Administrator." This is what makes the Program Standards binding for official assays. Note
  the register mismatch: **Standard B is written as a *recommended* procedure**, largely in
  "should" — its matrix-specific handling instructions are recommendations — but a few
  sentences use "shall", and 147.52(c) requires official assays to follow what the Standards
  describe. Do not promote Standard B's "should" text to MUST, and do not dismiss it either.
  Treat the **Standards version as a config value**, never a hardcoded constant.
- **147.52(d)** — the Official State Agency "will conduct a site visit and recordkeeping audit
  **at least once every 2 years**" — a floor, not a fixed cadence. **147.52(e)** — Service
  (NPIP staff) review **every 3 years**. **147.52(g)** additionally provides for verification
  sampling. These are the concrete, scheduled, adversarial events a retrievability design must
  survive: support retrieval **by analyst + date + assay**, which fails if the analyst is an
  unvalidated string.

## LAAF — where the ISO escape hatches close

If 21 CFR part 1 subpart R applies (a narrow trigger: import-alert removal, admission of an
imported article, response to an identified or suspected food-safety problem, or a directed
food laboratory order), it **incorporates ISO/IEC 17025:2017(E) into federal law by
reference** (§1.1101) and hardens it. Two assumptions this skill relies on elsewhere stop
holding:

- **§1.1152(d)(1)**: a full analytical report "must include ... All information described by
  ISO/IEC 17025:2017(E) sections 7.8.2.1(a) through (p) and 7.8.3.1(a) through (d)." The
  7.8.2.1 preamble's "unless the laboratory has valid reasons for not doing so" **does not
  survive** "must include all information described by (a) through (p)", and because MU is
  7.8.3.1(c) — inside the mandated (a)–(d) range — **measurement uncertainty stops being
  conditional**. The serializer needs a mode in which all 16 items plus MU are non-nullable and
  validation **fails closed**.
- **§1.1154(c)**: significant amendments must be trackable to previous and original versions,
  both retained, with "the date of amendment, the personnel responsible for the amendment, and
  a **conspicuous indication on the original document** stating that the document has been
  altered and that a more recent version of the document exists."

  **That forward indication breaks a pure append-only artifact model.** This skill's
  regeneration guidance prescribes only a *backward* reference — each new issue names the
  identifier it replaces — and rules out mutable links. An immutable stored PDF cannot receive
  a forward notice after the fact. Compliant options: keep a `superseded_by` pointer in the DB
  and stamp the notice at **retrieval/serving** time; or re-issue the original with the notice
  applied and retain both. Decide explicitly; do not assume backward-only satisfies LAAF.

**§1.1152 also demands finer-grained attribution than one report signatory**: "Name and
signature of the analyst who conducted **each analytical step**, including any applicable
validation and verification steps, and the date each step was performed" (§1.1152(d)(3));
retention of "all original compilations of raw data ... including discarded, unused, or
re-worked data, with the justification for discarding or re-working such data ... all
identified with unique sample identification, date, and time" (§1.1152(d)(8)); and
identification of any software used. So: attribution is **per step**, there are **three
distinct signature roles** (per-step analyst, the 7.8.2.1(o) report authorizer, and the
management certifier), and excluded or re-worked data must be **retained with a justification
field** — a design that simply omits them fails.

Note the interaction with Part 11: **LAAF records are carved out of 21 CFR Part 11 by
§11.1(p)**, so LAAF hardens ISO while removing the Part 11 overlay.

## Retention floors — four anchoring schemes, not one

Retention is not one number, and "per-engagement config" is necessary but insufficient. Record
the applicable **floor** alongside the configured value and refuse a shorter setting — but only
for floors that actually bind the lab.

| Source | Binds the lab? | Floor | Anchor |
|---|---|---|---|
| **FSIS ALP 9 CFR 439.20(b)** | **Yes**, if ALP-accredited | **3 years** | Per record family: QC and sample receipt/analysis/disposition "for the most recent three years that samples have been analyzed" ((b)(1)–(2)); prepared standards "three years after the last recorded entry" — **rolling**; and certificates of analysis for **purchased** standards "for at least the period of time that the materials are in use" — an **in-use** anchor with no fixed term |
| **AAVLD 5.4.3.2** | **Yes**, if AAVLD-accredited | assay in use **+ 7 years** after retirement | **Method lifecycle** |
| **LAAF 21 CFR 1.1154(a)** | **Yes**, in LAAF scope | **5 years** | Record creation |
| **FSIS 9 CFR 417.5(e)** | **No** — establishment | 1 yr (slaughter, refrigerated); 2 yr (frozen, preserved, shelf-stable) | Product category; offsite after 6 months if retrievable **within 24 hours** |
| **FDA 21 CFR 118.10(c)** | **No** — producer | 1 yr after the flock is permanently out of production | Flock lifecycle; offsite per (d) if retrievable within 24 hours — **except the written SE prevention plan, which must remain onsite** |

AAVLD 5.4.3.2 in full, because the enumeration matters: "Validation data, including all
original observations, calculations, equipment monitoring and calibration records, **archived
procedures used to formulate performance characteristics**, and a statement on validity of the
method, detailing its fitness for the intended use shall be retained by the laboratory for at
least as long as the assay is used for diagnostic purposes and for at least seven years after
the assay has been retired from use." The archived-procedures item is the one a method registry
design usually misses: **the versioned procedure text is itself on the method-lifecycle clock**,
not just the numeric data. Derive expiry as `max(assay in use, retirement + 7 years)`.

Two design points:

- **The bottom two rows are the wrong numbers for a lab system** — they bind the establishment
  and the producer. Implementing them on a lab LIMS enforces a flock-lifecycle anchor on
  records that never had one. They are here because a customer will cite them at you.
- **Rolling, lifecycle and in-use anchors cannot be expressed as `created_at + TTL`.**
  Retention must be modelled per record family with its own anchor, and a past-retention report
  must join through the method registry, the flock lifecycle, or a reagent/standard lot record.
  The in-use anchor has no fixed term at all — it is unevaluable without a lot lifecycle.
- **The 24-hour retrieval window is a storage-tier requirement**, not a retention period —
  beware archive-tier rehydration latency. And 118.10(d)'s provision that "electronic records
  are considered to be onsite if they are accessible from an onsite location" is what makes
  cloud-stored records acceptable: record it as an explicit design justification.

## The poultry domain model

**Do not hardcode a company/complex/farm/house/flock enum.** No source authorizes one and
integrators differ. What regulation *does* define:

- **9 CFR 145.1 "Flock"** — "All poultry of one kind of mating (breed and variety or
  combination of stocks) and of one classification on one farm", and in the disease-control
  sense "All of the poultry on one farm", with groups segregated at least 21 days optionally
  treated as separate flocks at the Official State Agency's discretion.
- **9 CFR 146.1** — "Commercial meat-type flock": "All of the meat-type chickens, spent fowl,
  meat-type turkeys, commercial upland game birds, or commercial waterfowl on one farm."

So the **minimum semantically-defined identity is farm + flock**, because that is the unit
regulation defines. **House must still be carried** — sampling intensity and results are
per-house — even though "house" is undefined in regulation. Model the hierarchy as typed,
ordered levels with a parent link, and **render the full typed path** on the report so each
name is disambiguated by its ancestry. A bare name is not an identification, and if the sample
or flock identifier is not unique *in the database*, the printed identity is ambiguous
regardless of what the template does (ISO clause 7.4.2 — see `iso-17025-reporting.md`).

Three generic clauses carry unusual weight in poultry work. The clause text is in
`iso-17025-reporting.md`; what matters here is that each is the **default case, not an edge
case**:

- **7.8.2.2 (customer-supplied data)** — flock ID, house, bird age, collection date and often
  the collection itself come from the grower or integrator, so essentially the whole
  traceability chain is customer-supplied. That makes the provenance marker, the conditional
  disclaimer, and the "results apply to the sample as received" statement routine rather than
  exceptional.
- **7.8.3.2 → 7.8.5 (sampling reporting)** — whether laboratory field staff or the grower
  collects decides whether six extra per-sample fields become required content. In poultry the
  answer varies by engagement, so it must be a modelled switch rather than a deployment
  assumption.
- **7.4.3 (deviations on receipt)** — poultry samples travel warm and arrive late; boot swabs,
  drag swabs, litter, dust, environmental sponges, carcass rinse, ceca, water and feed all have
  distinct integrity concerns. The per-result "which results may be affected" disclaimer is
  therefore the normal path, and a report-level condition string will not express it.

## Representing results

### Salmonella

**Detection, enumeration, and serotyping are three methods producing three result shapes, and
confirmation is staged.** NPIP Standard B walks suspect colonies through TSI/LIA slants, then
serological and biochemical screening, with a delayed secondary enrichment path when initial
selective enrichment is negative. The ISO family splits the same way (ISO 6579-1 detection,
with enumeration and serotyping in separate parts). Consequences:

- A single `method` field per assay group **cannot identify the method for each stage.** Attach
  method identity to the result **stage** (detection / confirmation / serogrouping / serotyping).
- Add an explicit `result_status` enum distinguishing **presumptive from confirmed**, plus the
  confirmation basis. A presumptive detection and a confirmed serovar are not interchangeable
  strings in one results list.

**Serogroup and serovar are results, not commentary.** NPIP Standard B: "All salmonellae
recovered shall be serogrouped or serotyped", and for pullorum-typhoid reactor culture
"Serogroup all isolates identified as salmonellae and serotype all serogroup D1 isolates."
Clause **7.8.3.1(e)** carries requirements imposed by "specific methods, authorities, customers
or groups of customers" onto the report. So serogroup and serovar must be **first-class typed
fields, each with its own method identity** — inside a generic list of free-text strings a
serotype is indistinguishable from a comment and cannot be validated or queried.

**Nomenclature follows a versioned scheme with formatting rules** (Grimont & Weill, *Antigenic
Formulae of the Salmonella Serovars*, 9th ed. 2007, WHO Collaborating Centre):

- Names were retained **only for subspecies *enterica* serovars**; serovars of other subspecies
  and of *S. bongori* "are designated only by their antigenic formula" — so a name field alone
  cannot represent them.
- Serovar names "**must no longer be italicized. The first letter is a capital letter**" (MUST).
- Acceptable forms are *S. enterica* subsp. *enterica* serovar Typhimurium, *S. enterica*
  serovar Typhimurium, or *Salmonella* ser. Typhimurium. Designations such as "S. Typhimurium"
  "should be limited to laboratory notebooks" (SHOULD). **A CoA is not a laboratory notebook.**
- A serotype model needs subspecies, an antigenic-formula field, and the **scheme edition** the
  name was validated against.

**Pullorum needs a biovar dimension.** "Pullorum is considered as one among the biovars of
serovar Gallinarum (identical 1,9,12:-:- formula)." Serotyping alone cannot distinguish them —
the antigenic formulae are identical — yet Pullorum carries the 147.52(f) reporting duty. So
the 48-hour workflow must trigger off **biovar plus the biochemical evidence that established
it**, never a substring match on a serovar name, and a single categorical-result field cannot
express this.

**O-groups exist in two notations and the poultry standard uses the older one.** The reference
scheme moves from letters to O-factors ("It is advisable to abandon designation-by-letter"),
mapping D1→9 and B→4, while NPIP Standard B still instructs labs to "serotype all serogroup D1
isolates." Store **both** designations with their mapping and render whichever the requesting
authority uses — otherwise "D1" and "O:9" are two values for one finding.

### Coccidia OPG

Where OPG comes from an automated image-based assay, the value may be **quantized rather than
continuous** and carry a hard lower reportable limit. For the PIPER assay specifically, the
published relation is `total OPG = 425 × total oocyst count`, giving a theoretical lower limit
of **425 OPG** (contrast a hemocytometer, where one counted oocyst represents 20,000 OPG, and
McMaster, reported to detect as few as 50 OPG). Consequences:

- A decimal field advertising four decimal places is **false precision** on a value that can
  only be an integer multiple of the conversion factor.
- A zero count must render as a **censored result** ("<425 OPG"), not "0".
- Store the **count as the primary datum**, derive OPG, and carry the conversion factor —
  clause 7.11.6 ("calculations and data transfers shall be checked in an appropriate and
  systematic manner") applies to the derivation.

**Size classes are an in-house measurand definition.** Where small/medium/large bins are
reported, they come from a vendor method with numeric boundaries (PIPER: small = major axis
<27 µm and minor <18 µm; medium = major <27 µm, minor >18 µm; large = major >27 µm), reported as
discriminating *E. acervulina*, *E. tenella*, and *E. maxima* respectively but explicitly not
able to discriminate all nine *Eimeria* species. "Small OPG" as a bare column label is
uninterpretable: print the bin definitions or reference the versioned in-house method, make the
method field required for this assay, and **do not let size classes imply species**.

### Species calls and comments are interpretations, not results

If a report names an *Eimeria* species — including by translating size classes into a species
call — comments on Salmonella prevalence, or says "consistent with", that crosses from result
into **opinion and interpretation**, and ISO clause 7.8.7 applies (clause text in
`iso-17025-reporting.md`; mandatory within LAAF scope via §1.1152(a)(4)).

The poultry-specific trap: size-class columns sit in the results table and look like results,
so a species inference feels like one more column. It is not. It needs a distinct
interpretation block with its own authorized interpreter — separate from the report authorizer
— and a stored reference to the documented basis. A verbal species call to a grower is itself a
record.

## Commonly over-claimed, commonly missed

**Over-claimed:**

- That ISO/IEC 17025 binds because the lab issues certificates of analysis. It is voluntary,
  binding through an accreditation contract or a customer/regulator requirement. Unaccredited
  labs lawfully issue CoAs.
- That NPIP applies because the assay is Salmonella on poultry. 147.52 applies to **authorized
  laboratories** performing **official Plan assays** — though note 145.23(b)(2)(i) reaches
  *any* person performing poultry diagnostic services, so "we are not NPIP-authorized" is not a
  complete answer on reporting duties.
- That FSIS **recommends** ISO/IEC 17025 for ALP participation — it does not; see
  `domain-regimes.md` for the exact framing, and note the acceptance route is conditioned on the
  lab being **in good standing** with an ILAC-recognized accrediting body.
- That the FSIS Salmonella performance standards impose laboratory requirements. They are
  establishment-facing categorization tools.
- That AAVLD accreditation is open to any veterinary lab. Its own requirements restrict
  eligibility — the Committee does not review commercial laboratories.

**Missed:**

- ISO clauses **7.8.2.2** (customer-supplied data), **7.8.5**/**7.8.3.2** (sampling reporting),
  **7.8.7** (opinions), **7.3.3** (sampling records), **7.4.2/7.4.3/7.4.4** (identification,
  deviations on receipt, storage conditions) — all in `iso-17025-reporting.md`, all routine in
  poultry work.
- The **24-hour** avian-influenza reporting clock (146.24(a)(1)(iii)/146.44(a)(1)(iii)), which
  is half the 48 hours most designs assume.
- That applicability is **per assay**. In a mixed Salmonella/coccidia platform, every candidate
  regime attaches to Salmonella; coccidia OPG has essentially no US regulatory hook outside an
  FDA animal-drug study. Resolve and record the regime set per assay group.

## Currency — re-verify before relying on these

- **9 CFR 147.52(f)(2)** (the 2025 revision described above): verified current at 2026-07-01 via
  the eCFR versioner API, and the section's credit line confirms no later amendment.
  **145.14's introductory text was revised by the same rule** (instruction 15); the quoted
  mandate survives unchanged.
- **Retrieval note:** ecfr.gov and federalregister.gov HTML redirect-block from some sandboxes.
  The versioner API works and is authoritative:
  `ecfr.gov/api/versioner/v1/full/<date>/title-9.xml?part=147&section=147.52`. govinfo GPO PDFs
  work but are **annual editions** — a year or more stale by construction, and the source of the
  superseded "reactors" text. Prefer the API for anything a deadline depends on.
- **AAVLD's requirements** are under Qualtrax document control and the identity has moved: SOP
  1137 Version 1 (approved 7 Feb 2023) carries 2021-01 clause content. Re-check the Qualtrax
  version, not the legacy "AC1 / V 2021.01" string, before citing a clause number.
- **NPIP Program Standards** are revised on a rolling basis; the Standard B content cited here
  was read from the December 2019 edition. Confirm the current edition and treat the version as
  configuration.
- **FSIS "Salmonella Framework for Raw Poultry Products"** (proposed 7 Aug 2024) was
  **withdrawn 25 April 2025**. Do not design to its serotype/level-based adulteration criteria.
  FSIS has since only sought input, via notices at 90 FR 55297 (2 Dec 2025) and 90 FR 57949
  (15 Dec 2025), "Exploring Practical Strategies To Reduce Salmonella in Poultry Products". No
  successor rule is in force; the 2016 performance standards (81 FR 7285) remain operative.
- **Salmonella nomenclature**: Grimont & Weill 9th ed. (2007) remains the WHO Collaborating
  Centre reference; new serovars are published in periodic supplements. Store the scheme edition
  with the result.
- **Claims deliberately omitted for lack of a verified source.** An earlier draft asserted an
  APHIS approved-laboratory regime at 9 CFR 71.22, state-law laboratory licensure and direct
  State-Veterinarian reporting duties, and a proposed NLRAD rule at 9 CFR part 57. Each rested
  on a single unrefuted source, and one of them was demonstrably reading a superseded CFR
  edition. They may well be real — **verify before adding them back**, and do not cite them from
  this file's history.
