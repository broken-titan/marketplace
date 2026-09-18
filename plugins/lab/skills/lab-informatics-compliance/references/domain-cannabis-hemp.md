# Cannabis and hemp overlay

Load when `cannabis_hemp` is on. Identifier kinds: lot, batch, license.
There is **no single-state schema**. Do not hardcode one state's
label, COA layout, or METRC/BioTrack field names.

## Federal hemp (7 CFR part 990)

USDA Domestic Hemp Production Program: [7 CFR part 990](https://www.ecfr.gov/current/title-7/part-990).
Laboratories used for official THC testing sit under USDA/state plan
rules (approved methods, DEA registration where required, reporting
of total THC). Sampling often sits on the producer or a sampling
agent, not the lab — model sampling responsibility as a switch (see
iso-lab-agnostic R8).

Exact current 990 laboratory-approval and reporting paragraphs change
with AMS rules. Confirm eCFR before coding a deadline. Store method
and plan version as config.

## Cannabis (state)

Adult-use and medical cannabis testing is **state law**. Common
software obligations that recur (still not a universal statute):

- Chain of custody and unique package/lot identity.
- Panel completeness (potency, residual solvents, heavy metals,
  micro, mycotoxins, pesticides) as **config per license type**.
- Fail-action / fail-lot workflow is a regulated state process — do
  not invent a national fail rule.
- Seed-to-sale system integration is a connector; the lab record
  remains the canonical result.

When the lab is also 17025-accredited, load the 17025 files. When
official hemp testing under 990 is in scope, say so in the profile
separately from state cannabis.

Part 11, CLIA, and 15189 stay off unless their own triggers are met
(they usually are not for plant-material compliance testing).
