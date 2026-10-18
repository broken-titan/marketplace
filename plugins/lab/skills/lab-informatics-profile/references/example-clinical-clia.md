# Example profile shape — generic US clinical + CLIA, optional 15189

**Not this user's lab.** Output shape only.

## Enabled overlays

| Flag | Posture | Trigger |
|---|---|---|
| `human_care` | — | Results issued for individual care |
| `clia` | legally required | Q3 A + US authority |
| `iso_15189` | design standard | Sought in addition to CLIA |
| `hipaa` | legally required | PHI as covered entity |

Off: Part 11, Annex 11, 17025, LAAF, ALP, NPIP, forensic, blood,
WADA, SEDD, CJIS, HCT/P, IVDR in-house, open_system, autoverification.

## Identifier model

- Primary: patient + specimen
- Extra: accession (if AP is later added, update the profile)

## Report-content overlay

`references/iso-15189-clinical.md` (clause 7.4 + CLIA section).
Do not apply 17025 7.8.

## Signature posture

Part 11 off. No LAAF carve-out. Authorized-release identity is a 15189
/ CLIA review field, not a §11.50 manifestation unless Part 11 is later
turned on.

## Retention classes

| Class | Anchor | Floor |
|---|---|---|
| Patient-care results | report issue / last amendment | none recorded — configurable; state / payer |
| HIPAA documentation | last effective date | 6 years (45 CFR 164.530(j)) — **documentation only** |

## Load from lab-informatics-compliance

- `references/domain-regimes.md`
- `references/base-objects.md`
- `references/limspec-map.md`
- `references/iso-15189-clinical.md`
- `references/domain-clinical.md`

## AGENTS.md block (shape)

```markdown
## Lab informatics
Profile: docs/lab-informatics-profile.md
Overlays: human_care, clia, iso_15189, hipaa
Load from lab-informatics-compliance: domain-regimes.md, base-objects.md, limspec-map.md, iso-15189-clinical.md, domain-clinical.md
Do not enable additional compliance frameworks from silence.
```
