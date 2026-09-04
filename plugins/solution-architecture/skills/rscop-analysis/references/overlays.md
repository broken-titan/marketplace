# Overlays (off until flagged)

Silence does not enable any row here. Load a section only when the user
or an Explicit RSCOP row flags it.

## Cloud Well-Architected (named)

AWS, Azure, or GCP Well-Architected, including sustainability and privacy
as named pillars. Pick the vendor the engagement named. Do not dump all
three. Do not treat "we will host in a cloud" as a flag.

## NIST SP 800-53 (architecture-relevant families)

Load only the families named below, as an overlay, not a control dump:

- PT (PII processing)
- SR (supply chain)
- CM (configuration)
- IR (as process, not a playbook rewrite)
- CP (contingency)
- SC (system and communications)
- SI (system and information integrity)
- IA (identification and authentication)

Do not import the rest of 800-53.

## Notation

C4 or ArchiMate. Off until the user asks for that notation. Standalone Context / Container / Deployment diagrams are the `c4-diagrams` skill (modes design / prose / review / update).

## Data-platform extras

dbt Mesh, ODCS, OpenLineage (beyond the Astro Asset URI copy-from-UI
rule), extra warehouse dialects beyond `azure_sql` / `postgres`, and
medallion (bronze/silver/gold) rename. Medallion rename only if flagged;
default folders stay dbt Labs names.

## Password breach-corpus (HIBP)

S-C9-class check against a known-compromised list. Not a Default. Off
until flagged.

## DAST every build

Dynamic application security testing on every CI build. SAST-on-build
may stay a Default; DAST-every-build does not.

## Regulated SAD extras

When **S-C11 is Explicit** (a named regime), load the SAD extras that
regime requires (retention depth, field-level encryption, pen-test
cadence). "No regime stated" does not enable them.

## Runtime / deploy products

ECS, Fargate, Cloud Run, Kubernetes, and similar. Off until O-E26 is
Explicit or the user names a target. Do not enable a runtime from silence.
