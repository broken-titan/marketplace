# Environmental overlay (TNI / NELAP)

Load when `environmental` or `tni_nelap` is on. Identifier kinds:
station, matrix, field-sample. Not patient.

## TNI / NELAP

The NELAC Institute (TNI) publishes the Environmental Laboratory
standard used by NELAP accreditation bodies. Accreditation is granted
for **matrix–method–analyte** combinations (fields of accreditation),
recorded in TNI LAMS. Primary vs secondary (reciprocal) ABs are
defined by the TNI standard.

TNI Volume 1 (management and technical requirements for laboratories
performing environmental analysis) supplements a quality-system module
aligned with ISO/IEC 17025. When `iso_17025` is also on, load the 17025
files as well.

Design consequences:

- Scope is **per field of accreditation**. Reports that claim
  accreditation must flag methods/analytes outside the FOA. This is
  the opposite of AAVLD's whole-lab posture.
- Demonstration of capability (DOC) records: TNI technical modules
  require DOC records **as long as the method is in use and for a
  stated period after last use**. A 2026 draft microbiology module
  (EL-V1M5) states five years past last use — **draft, not the
  citable in-force floor** until the lab's AB cites that edition.
  Store the floor from the profile / AB.
- Method, revision, matrix, and analyte codes are first-class
  (TNI LAMS codes exist for interchange).

Unverified: a single TNI clause number that is "the" retention rule
for all modules. Retention stays a class + floor.

## EPA SEDD

When `epa_sedd` is on. TNI / NELAP does **not** substitute.

[SEDD Specification v5.2 (March 2019)](https://www.epa.gov/sites/default/files/2019-05/documents/sedd_spec_v5-2-march_2019_508.pdf)
is a **named payload**: staged XML deliverable + data-element
dictionary. Software must emit (and, if received, validate) SEDD
at the stage the engagement names. Confirm whether a later SEDD
edition has replaced 5.2 before coding a schema freeze.

LIMSpec 20.3. Silence does not enable `epa_sedd`.

## Sources

- [TNI LAMS](https://lams.nelac-institute.org/)
- TNI Environmental Laboratory standard (current edition from
  nelac-institute.org — paywalled / membership; confirm edition
  before citing a module letter)
- [EPA SEDD v5.2 (March 2019)](https://www.epa.gov/sites/default/files/2019-05/documents/sedd_spec_v5-2-march_2019_508.pdf)
