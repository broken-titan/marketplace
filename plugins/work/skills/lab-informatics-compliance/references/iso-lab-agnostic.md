# The ISO baseline, agnostic to lab type

Load this when you need the ISO requirements before you know which standard binds the
deployment. Testing and calibration labs are accredited to ISO/IEC 17025:2017. Medical
labs go to ISO 15189:2022. US veterinary labs often go to AAVLD instead. The obligations
below hold across all three. The clause numbers do not.

Use this file to design the data model. Use
[iso-17025-reporting.md](iso-17025-reporting.md) for the exact 17025 clause map, and
[domain-regimes.md](domain-regimes.md) to work out which standard actually binds.

## Why one view works for all three

ISO 15189:2022 is structurally aligned with ISO/IEC 17025:2017, and its Annex B carries
an explicit clause comparison against both 17025:2017 and ISO 9001:2015. AAVLD's
requirements (SOP 1137 v1, carrying 2021-01 content) are derived from and congruent with
17025:2017, but they are numbered on the legacy 2005 scheme. So the same obligation
appears in three places under three numbers.

Design against the obligation. Resolve the number when you know the standard.

| Obligation | ISO/IEC 17025:2017 | ISO 15189:2022 | AAVLD SOP 1137 |
|---|---|---|---|
| Report content | 7.8 | **7.4** | 5.10 |
| Report identification | 7.8.2.1(d) | resolve via Annex B | 5.10.2.3 (stricter) |
| Control of records | 8.4 | resolve via Annex B | 4.10 |

Only the 15189 report-content number is verified here. For anything else in 15189, read
Annex B rather than assuming the 17025 number carries over. Citing a 17025 clause number
at a medical lab auditor is a credibility problem even when the substance is right.

## Records

**R1. One identity per activity, and a separate checker only where a check happens.**
17025 §7.5.1 requires the date and the identity of personnel responsible for each
activity and for checking data and results. The floor is one identity that resolves to a
person without consulting current state. Add the checker field where a review step
exists. A blank reviewer column implies a control the workflow does not have.

**R2. Records are made at the time.** §7.5.1 requires original observations, data, and
calculations to be recorded when they are made. In software terms the compliance
timestamp is captured server-side at request entry. It is never accepted from a client
payload.

**R3. The record is complete enough to repeat the activity.** §7.5.1 has two limbs, both
qualified by "if possible". The record must facilitate identification of factors
affecting the result and its measurement uncertainty. It must also enable repetition
under conditions as close as possible to the original. The factors-affecting limb is what
justifies snapshotting instrument, method, environmental, and configuration context.

**R4. An amendment keeps the original.** §7.5.2 is the most on-point ISO clause for
audit-trail design and the one most often uncited. Amendments must be trackable to
previous versions or original observations. Both original and amended data must be
retained, with the date of alteration, an indication of what changed, and the personnel
responsible. This is an ISO-side mandate for the same immutable trail 21 CFR Part 11
§11.10(e) requires, so cite both.

## Items and sampling

**R5. Items are unambiguously identified.** §7.4.2 requires a system that ensures items
are not confused physically or when referred to in records. If the sample identifier is
not unique in the database, the printed identity is ambiguous no matter what the template
does. Check for a uniqueness constraint before claiming the report identifies the item.

**R6. Deviations are recorded on receipt, and the disclaimer is per result.** §7.4.3
requires deviations from specified conditions to be recorded on receipt. Where the
customer wants the item tested anyway, the report must indicate *which results may be
affected*. One report-level condition string cannot express that. The schema needs a
row-level affected-by-deviation marker, a deviation description, and a record of the
customer consultation and its outcome.

**R7. Storage and conditioning conditions are monitored and recorded.** §7.4.4 applies
whenever items must be held under specified environmental conditions.

**R8. Who collected the sample is a schema-level switch.** §7.8.3.2 routes a report into
§7.8.5 whenever the lab is responsible for sampling. Six further per-sample fields then
become required report content, including a sampling location able to carry a diagram or
photograph. §7.3.3 separately enumerates the sampling records to retain. Model sampling
responsibility explicitly. Do not bake it into a deployment assumption.

## Reports

**R9. Every report carries a fixed content set.** 17025 §7.8.2.1 lists 16 items (a) to
(p). ISO 15189 §7.4 covers the same ground for medical reports under different numbering.
Agnostic to lab type, a report needs: a title, the issuing lab's identity, the customer's
identity and contact details, unambiguous identification of the item, the method, the
results with units, the relevant dates, the location of performance, the person
authorizing release, a unique identifier plus a clear end-of-report marker, a statement
that results relate only to the items tested, any deviations from the method, and clear
identification of results from external providers. The last two are the ones most often
absent from data models.

**R10. Customer-supplied data is marked as such.** §7.8.2.2 makes the lab responsible for
all information in the report *except* what the customer supplied, requires
customer-supplied data to be clearly identified, and requires a disclaimer when that data
can affect validity. Where the lab did not do the sampling, the report must state that
results apply to the sample as received. That is a provenance marker per field group plus
a conditional disclaimer block, not a paragraph of static template text.

**R11. Measurement uncertainty has named triggers.** For test reports §7.8.3.1(c) makes
MU conditional on three things: relevance to validity or application of results, a
customer instruction, or an effect on conformity to a specification limit. Design against
those three, not a vague "where applicable". For calibration certificates §7.8.4.1(a)
makes MU unconditional.

**R12. A pass/fail field is a statement of conformity, and one boolean is not enough.**
§7.8.6 is its own clause with its own trigger. Once the report states conformity, the
record needs three named fields: which results the statement covers, which specification
or standard is met or not met, and the decision rule applied. The decision rule must be
documented with its risk considerations. Companion guidance is ILAC-G8:09/2019, cited by
document number.

**R13. An interpretation is not another result column.** §7.8.7 covers opinions and
interpretations. Only authorized personnel may release one, the basis must be documented,
the statement must be clearly identified as an interpretation, and a verbal
interpretation given to a customer is itself a record. Any "consistent with", any species
call inferred from a measurement, and any prevalence comment crosses this line. It needs
its own block, its own authorized interpreter distinct from the report authorizer, and a
stored reference to the documented basis.

**R14. A replacement report names the specific document it replaces.** §7.8.8.1 covers
change, amendment, and plain re-issue. §7.8.8.2 requires a true amendment to take the
form of a further document carrying an "Amendment to Report, serial number..." statement.
§7.8.8.3 requires a complete new report to be uniquely identified and to reference the
original it replaces. Boilerplate that names no antecedent satisfies neither. Gate this
before building it: if every generation allocates a fresh unique number, nothing claims
to replace anything and §7.8.8.3 never engages.

## The information system itself

**R15. Validate before introduction, and after every change.** §7.11.2 covers the
laboratory information management system used for collection, processing, recording,
reporting, storage, or retrieval, including interfaces. Changes, including configuration
changes and modifications to commercial software, must be authorized, documented, and
validated before implementation.

**R16. A system failure is a recordable event.** §7.11.3(e) requires system failures and
the immediate and corrective actions taken to be recorded. A render that raises, an
upload that fails, and a hash mismatch found by a verification job are all in scope. A log
line is not a record.

**R17. An external provider does not absorb the obligation.** §7.11.4 makes the lab
responsible for ensuring an off-site or external provider complies with all applicable
requirements. Cloud hosting does not transfer this. Cite 7.11.4 for it, not 7.11.3.

**R18. Calculations and data transfers are checked systematically.** §7.11.6 is the
ISO-side citation for parity tests, re-hashing, and verification tooling. Any derived
value falls under it, including a unit conversion applied to a raw count.

## Retention

**R19. Retention is a per-obligation value with its own anchor.** §8.4.2 requires
controls for identification, storage, protection, back-up, archive, retrieval, retention
time, and disposal. Records are retained for a period consistent with the lab's
contractual obligations, kept readily available, and access-controlled consistently with
confidentiality commitments.

Two consequences. Back-up and archive sit inside the accreditation requirement, so they
are not purely infrastructural. And retention cannot be a platform constant. Real anchors
include the record's creation date, a method lifecycle, a rolling last-entry date, and an
in-use lifecycle with no fixed term. A `created_at + TTL` policy cannot express the last
three. Model retention per record family with its own anchor, and store the regulatory
floor alongside the configured value so config cannot be set below it. Examples of each
anchor are in [poultry-veterinary.md](poultry-veterinary.md).

Having a *defined* disposal control is required even when the chosen policy is indefinite
retention. Labs on management-system Option B satisfy §8.4 through an ISO 9001-conformant
system instead.

## What is not agnostic

Five places where lab type changes the answer. Check each before shipping.

1. **Report-content clause numbers.** 17025 §7.8 versus 15189 §7.4. Every 7.8 citation in
   this skill shifts for a medical lab.
2. **Per-page identification.** Under 17025 §7.8.2.1(d) the end-of-report marker is
   required and "Page X of Y" is only good practice. It was a 2005 requirement (§5.10.2(c))
   that did not carry into 2017. AAVLD §5.10.2.3 does require the unique identifier at the
   beginning and on each page, so for an AAVLD-accredited lab it is a requirement.
3. **The "valid reasons" escape hatch.** 17025 §7.8.2.1 is prefaced "unless the
   laboratory has valid reasons for not doing so". Inside FSMA LAAF scope, 21 CFR
   §1.1152(d)(1) requires all of (a) through (p) plus §7.8.3.1(a) through (d), which
   removes both the escape hatch and MU's conditionality. The serializer needs a fail-closed
   mode.
4. **Measurement uncertainty.** Conditional on test reports, unconditional on calibration
   certificates, and unconditional inside LAAF scope.
5. **Scope posture.** Bodies like A2LA and ANAB accredit test by test, so a report
   referencing accreditation must flag assays outside scope. AAVLD accredits the whole
   laboratory, which makes that flag inert. Make it config-driven rather than hardcoded.

## Design-review questions that hold for any lab

1. Does every regulated action carry a non-null actor identity, plus a checker identity
   if and only if the workflow has a reviewer? (R1)
2. Is the compliance timestamp captured server-side at request entry? (R2)
3. Can the record be re-rendered and the activity repeated from what is stored? (R3)
4. Is the amendment trail append-only and immutable at the database level? (R4)
5. Does a uniqueness constraint back the printed item identity? (R5)
6. Is the deviation disclaimer per result rather than per report? (R6)
7. Is sampling responsibility a modelled switch that gates the §7.8.5 block? (R8)
8. Can the serializer name the clause each report field satisfies, and can it fail closed
   when a regime removes the omission grounds? (R9, and item 3 above)
9. Is customer-supplied data marked and rendered as such? (R10)
10. Does every conformity statement carry scope, specification, and decision rule? (R12)
11. Are interpretations a distinct block with their own authorized person? (R13)
12. Does a replacement report reference the specific document it replaces, where re-issue
    is a real workflow? (R14)
13. Are system failures written as events rather than logged and lost? (R16)
14. Does retention model an anchor per record family, with the regulatory floor stored
    alongside? (R19)

## Sources

- [ISO/IEC 17025:2017](https://www.iso.org/standard/66912.html), General requirements for
  the competence of testing and calibration laboratories. Edition 3, confirmed 2023. Clause
  text paraphrased throughout, verified against the skill's clause map in
  [iso-17025-reporting.md](iso-17025-reporting.md).
- [ISO 15189:2022](https://www.iso.org/standard/76677.html), Medical laboratories.
  Edition 4, replacing 15189:2012 and absorbing ISO 22870:2016. Annex B carries the
  comparison against 17025:2017. Report content is clause 7.4.
- AAVLD, "Requirements for an Accredited Veterinary Medical Diagnostic Laboratory",
  SOP 1137 Version 1 (approved 7 February 2023, carrying 2021-01 clause content). Under
  Qualtrax document control at aavld.org. The legacy document number "AC1" is an alias.
  Crosswalk and caveats in [poultry-veterinary.md](poultry-veterinary.md).
- ILAC-G8:09/2019, guidance on decision rules and statements of conformity. Cite by
  document number. ILAC ceased operations 31 December 2025 and its functions passed to the
  Global Accreditation Cooperation on 1 January 2026.
- FSMA LAAF rule, 21 CFR part 1 subpart R, §§1.1101 to 1.1201. Incorporates
  ISO/IEC 17025:2017(E) by reference. Trigger and hardening detail in
  [domain-regimes.md](domain-regimes.md) and [poultry-veterinary.md](poultry-veterinary.md).
- 21 CFR Part 11 §11.10(e), cited alongside 17025 §7.5.2 for the audit trail. See
  [SKILL.md](../SKILL.md) rules 1 and 2.

## Currency

ISO/IEC 17025:2017 is current. Pages claiming an "ISO/IEC 17025:2025" edition are false.
The 2017 edition was confirmed in 2023 with no successor, and the next systematic review
is due around 2028. Accreditation to ISO 15189:2012 stopped being recognized under the
ILAC Arrangement after 6 December 2025. Re-check AAVLD clause numbers against the current
Qualtrax version rather than the legacy "AC1 / V 2021.01" string.
