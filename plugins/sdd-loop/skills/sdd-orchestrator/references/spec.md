# Stage Playbook: Spec

Goal – produce a functional spec that makes the ticket implementable without further requirements discussion. The spec is the contract that later stages build and test against.

## Process
1. Read the ticket, its parent, siblings, comments, and any linked material.
2. Draft the spec locally using this template.
   - **Problem** – what is broken or missing, and for whom.
   - **Goals** – what done looks like, in user-observable terms.
   - **Non-goals** – what this explicitly does not cover.
   - **Functional requirements** – reuse the stable IDs assigned at intake (`FR-1`, `FR-2`, ...; `NFR-*` for non-functional). Do not mint a parallel ID scheme. IDs are permanent, so never renumber on revision. A new requirement takes the next free number; a dropped one leaves a gap marked "removed".
   - **Acceptance criteria** – at least one per requirement, each with a stable ID under its requirement (`AC-1.1` and `AC-1.2` belong to FR-1) and mechanically testable. Choose the syntax per requirement – Given/When/Then for user-facing flows, EARS for system behavior, events, and error handling ("When <trigger>, the <system> shall <response>"; "While <state>, ..."; "If <error>, ..."). Mixing syntaxes within a spec is fine; untestable criteria are not. These IDs are the traceability keys – the design's test plan, the task plan, test names, and the verify matrix all cite them.
   - **Edge cases and error behavior**.
   - **Open questions** – anything the user or stakeholders must decide, each with your recommended answer.
3. Flag any requirement that cannot be made testable as an open question rather than papering over it.

## Clarify Loop
Work every open question before the spec is final. Re-run this section via `sdd-clarify` / `/sdd clarify` without rewriting the spec body.

1. **Self-resolution pass first.** For each open question, actively hunt for the answer in what already exists – the ticket tree and linked pages, the codebase, the constitution and product/structure steering docs, `.sdd/notes.md`, published sibling specs. A question with a discoverable factual answer – current behavior, existing constraints, what the code or schema allows – that the evidence supports confidently is resolved. Record it in a **Clarifications** section of the spec, marked self-resolved, with the evidence cited.

   Questions of intent, priority, or stakeholder preference are never self-resolved; evidence cannot answer "should we". E.g. "what does this endpoint return today on a missing record" is self-resolvable from the code, while "should a missing record 404 or return an empty list" is a decision. Re-run the pass when an answer surfaces new questions.
2. **Classify what survives.** Material means the answer would change requirements, acceptance criteria, or scope. Minor means wording, or a default that could ship either way.
3. **Escalate by mode.**
   - Interactive – ask the user the material questions, highest impact first, each with your recommended answer. Fold answers into Clarifications and repeat until nothing material is open, or the user explicitly defers it.
   - Batch – mark the work product and its pending-actions entry `MATERIAL QUESTIONS OPEN`. Minor questions ride along in the draft as deferred-with-recommendation.
   - Autonomous – material questions surviving self-resolution park the ticket as ATTENTION. Ambiguity stops the line; never guess. Minor questions are recorded as deferred-with-recommendation and the pipeline advances.

## Output (Local)
Write `.sdd/work/<ticket-key>/spec.md`. Present it with the open questions highlighted first.

## Candidate External Actions (for the Review Gate)
- Publish the spec per the orchestrator's Spec Storage setting (`ticket-comment`, `confluence`, or `in-repo`). Update `.sdd/work/<ticket-key>/trace.md` so each intake ID has a spec row.
- Add a comment listing the open questions and tagging the reporter, if the user wants stakeholder input.

## Quality Checks Before the Review Gate
- Every requirement and acceptance criterion carries its stable FR-*/NFR-*/AC-* ID, and no revision renumbered an existing one.
- Every acceptance criterion is testable by a machine, or by an unambiguous manual check.
- The non-goals section is non-empty. A spec without exclusions is usually underscoped.
- The spec answers "how do we know it works" for every goal.
- The Clarify Loop ran, so every open question is self-resolved with evidence, answered by the user, deferred as minor with a recommendation, or escalated per the active mode. No material question is silently open.
