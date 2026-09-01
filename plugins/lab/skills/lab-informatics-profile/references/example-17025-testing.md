# Example profile shape — generic 17025 testing laboratory

**Not this user's lab.** Output shape only. Not a food, veterinary,
clinical, or poultry lab unless those flags are on.

## Enabled overlays

| Flag | Posture | Trigger |
|---|---|---|
| `iso_17025` | legally required | Seeking / holding 17025 (or customer requires accredited results) |

Off: CLIA, 15189, Part 11, Annex 11, LAAF, ALP, AAVLD, NPIP, HIPAA,
WADA, SEDD, CJIS, HCT/P.

Domain flags depend on Q1 (e.g. `calibration` only, or `food_feed`
without ALP/LAAF). This example assumes **no sector program**.

## Identifier model

- Primary: item / sample
- Extra: none unless a domain flag adds lot, exhibit, etc.

## Report-content overlay

`references/iso-17025-reporting.md`

## Signature posture

Part 11 off. Report authorizer is 17025 7.8.2.1(o), not a Part 11
signature unless that flag is later enabled.

## Retention classes

| Class | Anchor | Floor |
|---|---|---|
| Technical records / issued reports | contractual / configured per family | none recorded — 17025 8.4.2 is contractual, not a year |

## Load from lab-informatics-compliance

- `references/domain-regimes.md`
- `references/base-objects.md`
- `references/limspec-map.md`
- `references/iso-lab-agnostic.md`
- `references/iso-17025-reporting.md`
- `references/iso-17025-systems.md`

## AGENTS.md block (shape)

```markdown
## Lab informatics
Profile: docs/lab-informatics-profile.md
Overlays: iso_17025
Load from lab-informatics-compliance: domain-regimes.md, base-objects.md, limspec-map.md, iso-lab-agnostic.md, iso-17025-reporting.md, iso-17025-systems.md
Do not enable additional compliance frameworks from silence.
```
