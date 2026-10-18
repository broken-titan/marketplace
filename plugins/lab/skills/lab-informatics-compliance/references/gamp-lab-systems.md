# GAMP GPG — GxP Compliant Laboratory Computerized Systems

Load when any GxP flag is on (`part_11`, `annex_11`, `glp`, `gclp`,
`qmsr`, `pharma_qc`) or when `gamp_lab` is adopted as design
standard. **Distinct from GAMP 5** (lifecycle / Category 5 in
`domain-gxp.md`). This guide is laboratory-specific: instrument
complexity, raw-data definition, interfacing.

[ISPE store](https://ispe.org/publications/guidance-documents/gamp-good-practice-guide-gxp-compliant-laboratory-computerized-systems)
— 2nd edition, **2012**. Paywalled. Do not invent clause numbers.

## What this overlay is for

- Classify laboratory computerized systems (CDS, SDMS, LIMS, ELN,
  standalone instruments) by complexity and GxP impact.
- Define **raw data** for the system class (file + processing
  parameters, not a printout) — aligns with `base-objects.md` O6.
- Treat instrument interfaces as qualified connections (O5).
- USP ⟨1058⟩ Groups A/B/C sit beside this file (`usp-1058.md`);
  do not collapse AIQ into GAMP 5 IQ/OQ/PQ labels.

## What this overlay is not

- Not a substitute for GAMP 5 validation lifecycle. That package
  for the LIMS/LIS/ELN itself is the `lab-system-csv` skill.
- Not a statute. Posture is **adopted as design standard** unless
  a predicate already requires the same control.
- Written SOPs and the validation package remain organizational
  (base skill “What code cannot cover”).
