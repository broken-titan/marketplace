# FDA OOS investigations (21 CFR 211.192)

Load when `pharma_qc` or medicinal-product GMP activity is on,
or when `fda_oos` is adopted. Phase model is **guidance**, not a
statute; 211.192 is the predicate.

https://www.fda.gov/media/158416/download
https://www.ecfr.gov/current/title-21/section-211.192

## Phase I — laboratory investigation

Hypothesis-driven checks of the original failing aliquot /
preparation / instrument / calculation. The **original failing
value remains**. Do not delete-and-replace. Software: OOS
incident object (`base-objects.md` O7); block release.

## Phase II — full-scale

Extends outside the laboratory hypothesis (production, sampling,
other batches) when Phase I does not assign cause. Software:
same incident, additional linked records; still no silent
overwrite.

## What is not software

The written investigation SOP, QA approval of the protocol, and
the decision to retest / resample are organizational. The system
must **forbid** discarding the first result and must keep the
incident attached to the batch / sample.
