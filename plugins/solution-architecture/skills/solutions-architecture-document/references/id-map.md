# ID map (from the RSCOP catalog)

Cite IDs only as they appear in `rscop-analysis/references/catalog.md`.
Do not invent `O-E29`. When authoring the SAD Open Questions table or
ADR **Related** rows, copy from this map.

| Catalog ID | Catalog meaning | SAD use |
|------------|-----------------|---------|
| O-E26 | Deployment target | 4e Infrastructure; working assumption only if the user chose one |
| P-E1 | Application read response time p95 | Latency, not the data model |
| P-E9 | Latency verification before handoff | Load-test / customer-live clock |
| P-E11 | Schema stability during build | Data-model walkthrough blocker (with P-C14) |
| P-C12 | Total end-customer user count | Scaling |
| P-C13 | Peak concurrent users | Scaling |
| P-C14 | Domain display requirements | 4a attributes; data-model walkthrough |
| P-C17 | Mobile and tablet usage | 4a breakpoints |
| O-C5 | Soft-launch milestone | Code-complete vs customer-live |
| O-E20 | Existing CI pattern | 4b / 5 tool choices |
| O-E21 | Existing observability stack | 4b / 6 tool choices |
| S-E11 | Audit log destination | 4f, ADR-004 |
| S-E12 | Role matrix source | 4f |
| S-E13 | Pre-launch security review owner | 4f |
| S-C11 | Regulatory regime | Regulated SAD extras only when Explicit |
| S-C13 | End-customer IdP federation | Informs ADR-005; does not block the seam |
| C-C7 | Target delivery date | 1 Constraints |
| T1 | Multi-tenant seams now vs later | ADR-001, ADR-007 |
| T6 | Audit destination | ADR-004 |

## Open Questions table (use these IDs)

| Requirement ID | Question | Blocks SAD section |
|---|---|---|
| P-E11, P-C14 | Data-model walkthrough and schema stability | 4c Data Architecture — fully blocked until `{Technical contact}` delivers |
| O-E26 | Deployment target (cloud, region, runtime) | 4e Infrastructure — leave Open or ask; do not assume ECS/Fargate |
| P-C14 | Which entities/attributes the UI must show | 4a Information Architecture — partially blocked |
| P-C12, P-C13, P-C17 | User count, peak concurrency, device mix | 4e scaling; 4a breakpoint priority |
| O-E20, O-E21 | Existing CI pattern and observability stack | 4b, 5, 6 tool choices |
| O-E22, O-E23, O-E24 | Device / AI-tool / install permissions | Build velocity; does **not** block architecture authoring |
| S-E11 | Audit log destination | 4f, ADR-004 |
| S-E12 | Role matrix source | 4f |
| S-C13 | End-customer future identity-provider preference | Informs ADR-005; does not block the seam |
| C-C7 | Target delivery date | 1 Constraints — pending contract if gated |

Prefer filling this table from the current `docs/rscop-<slug>.md` rows
that are still Open, using the catalog IDs above. Do not hardcode a
stale ID from memory.
