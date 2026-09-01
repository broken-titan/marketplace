# Stage Playbook: Lite (Fast-Track for Small, Low-Risk Tickets)

Goal – carry a small, well-understood ticket from intent to implemented code with one combined artifact and one stop, instead of the full spec -> design -> dev sequence. The contract discipline is unchanged; testable acceptance criteria still come before code.

## Eligibility (Check First, Hard Gate)
All of these must hold.

- The change is one contained deliverable slice – clear intent, a handful of files, no cross-cutting refactor.
- Requirements are unambiguous enough that the Clarify Loop would surface nothing material.
- **No risk exclusion applies** – no security or auth surface, no data migration or schema change, no public API change, and nothing the constitution marks as sensitive.

A ticket that trips any exclusion leaves the fast track. Stop, say why, and route it through the full Spec and Design stages instead. That applies mid-flight too, when the work turns out bigger than it looked.

## Process
1. Draft one combined document, `.sdd/work/<ticket-key>/lite.md`, with these sections.
   - **Problem**.
   - **Functional requirements**, with stable FR-* IDs.
   - **Acceptance criteria**, with AC-x.y IDs, each mechanically testable per the spec playbook's syntax rules.
   - **Approach**, a paragraph or two.
   - **Affected files**, from actual repo exploration.
   - **Test plan**, with every AC ID mapped.
2. Run the spec playbook's Clarify Loop on it. Any material question that survives self-resolution disqualifies the fast track – route to the full Spec stage.
3. Derive a short task plan (`tasks.md`, per the design playbook's task-plan step). Typically a handful of tasks, file-path-pinned and ID-cited.
4. Run the dev playbook against the combined document as both spec and design – tests first, task-by-task with check-offs, full verification, evidence capture, and the independent review, all unchanged.

Mode flow.

- **Interactive** – the user's approval of the Lite proposal (orchestrator Step 2) covers the whole run. Work straight through to the Review Gate with no per-stage stops.
- **Batch and autonomous** – proceed only on high-confidence eligibility, logging the evidence; anything lower runs the normal stages. In autonomous runs, a declared `spec` or `design` gate parks a Lite ticket once, after the combined document is drafted. The `dev`, `verify`, and `merge` gates behave as usual.

## Output (Local)
`.sdd/work/<ticket-key>/lite.md`, `tasks.md`, and the dev playbook's outputs – the worktree, the evidence file, and the summary.

## Candidate External Actions (for the Review Gate)
- Publish the combined document per the orchestrator's Spec Storage Convention.
- The dev playbook's actions – push the branch, create the PR (task checklist and AC-ID-to-test mapping in the body), the summary comment, the transition.

## Quality Checks Before the Review Gate
- Every eligibility condition still holds now that the diff exists. Scope creep disqualifies retroactively, so route the ticket back through the full stages rather than shipping an oversized fast-track.
- Every dev-playbook quality check passes unchanged.
