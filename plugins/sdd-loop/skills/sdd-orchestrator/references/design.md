# Stage Playbook: Design

Goal – settle the technical approach so the dev stage is mechanical.

Entry requires an existing spec or equivalent acceptance criteria. If none exist, stop and recommend the Spec stage instead. A spec whose Clarifications still show material open questions also fails entry. Send it back through the Spec stage's Clarify Loop rather than designing on ambiguity.

## Process
1. Read the spec and the relevant code. Explore the repository enough to ground every claim in real files.
2. Draft the design locally using this template.
   - **Approach** – the chosen solution in a few paragraphs.
   - **Alternatives considered** – at least one, with the reason it lost.
   - **Interfaces** – function signatures, API shapes, or schemas that change, in code blocks.
   - **Data changes** – migrations, new fields, storage implications.
   - **Test plan** – which acceptance criteria, cited by AC ID, map to unit, integration, or manual tests.
   - **Risks and rollout** – what could break, feature flags, reversibility.
   - **Affected files** – concrete paths discovered during exploration.
3. Add text-based diagrams (Mermaid or ASCII) where structure matters.
4. Decompose the approach into a task plan, written to `tasks.md` beside the design. Tasks are dependency-ordered, each small enough to implement and verify independently, each pinned to exact file paths and citing the FR/AC IDs it advances. Mark a task `[P]` when it is parallelizable – different files, no dependency on another task. The dev stage executes this plan and checks tasks off in place, so a crashed or resumed run can pick up mid-ticket.

## Output (Local)
Write `.sdd/work/<ticket-key>/design.md` and `.sdd/work/<ticket-key>/tasks.md`, and present them.

## Candidate External Actions (for the Review Gate)
- Publish the design, task plan included, per the orchestrator's Spec Storage Convention.
- Add a comment summarizing the chosen approach and any decisions needed.

## Quality Checks Before the Review Gate
- Every acceptance criterion in the spec appears in the test plan, cited by its AC ID.
- Every task in the plan pins real file paths and cites the requirement IDs it advances, and every AC ID is covered by at least one task.
- Interfaces are concrete enough to code against without further decisions.
- Every path in the affected-files list was opened during repository exploration.
- Consistency pass across artifacts. No design decision contradicts the spec or the constitution, no requirement is silently dropped, and nothing is designed that the spec does not ask for. A contradiction is fixed or surfaced as an open question, never left implicit. If the spec is the side that is wrong, send it back to the Spec stage as a backward correction; never work around it in the design.
