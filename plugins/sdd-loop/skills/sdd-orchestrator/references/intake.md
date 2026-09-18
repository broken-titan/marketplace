# Stage Playbook: Intake (Requirements Dump -> Ticket Tree)

Goal – turn a raw requirements dump into a structured, reviewable ticket tree. Nothing is created in Jira during this playbook.

The dump is either a tracker ticket (ticket-based intake) or a user-supplied document – a .md/.txt file path or inline text passed to intake (Direct Intake Mode). The process is identical; where the source differs, both forms are noted below. IDs assigned here are reused in spec and verify. Never renumber them later.

## Process
1. Read the full dump. For a ticket source that means the description, comments, attachments the user provides, and linked pages. For a document source it means the file or inline text, plus any documents it references that the user can provide.
2. Extract every distinct requirement. Separate features, constraints, assumptions, and open questions. Assign a stable ID to each requirement at intake (`FR-1`, `FR-2`, …; `NFR-*` for non-functional) and at least one acceptance-criterion ID under it (`AC-1.1`). These IDs are the traceability keys. A new requirement takes the next free number; a dropped one leaves a gap marked "removed".
3. Group requirements into a proposed ticket tree.
   - Parent at the top is the source ticket itself (or an Epic). For a document source, use the `parent=` ticket if given, else propose a new Epic.
   - One Story per independently deliverable slice of user value.
   - Tasks only for necessary technical enablers.
4. For each proposed ticket, draft a summary (imperative, under 80 chars), a description (context plus the requirements it covers), draft acceptance criteria (Given/When/Then where possible), dependencies on sibling tickets (as blocks / is-blocked-by relationships), and suggested labels. Never include the gate label (`ai-allowed`, or the repo's configured override) in suggested labels; the user applies that gate themselves.
5. Keep the tree Plans-ready, with real hierarchy (Epic -> Story -> Task, using the project's correct issue types) and dependencies as issue links, with no planning fields the dump did not supply. Never invent target dates, sprints, versions, estimates, or team assignments. Roadmapping is the user's job; the tree just has to slot into it cleanly.
6. List everything that could NOT be turned into a ticket – ambiguities, contradictions, open questions – each phrased as a question the user can answer or forward.

## Output (Local)
Write `.sdd/work/<ticket-key>/intake.md`, containing the ticket tree, the requirement-to-ticket traceability list (every FR/NFR/AC ID), and the open questions section. Also start `.sdd/work/<ticket-key>/trace.md` with those IDs (intake column filled; spec and verify columns empty). Present it to the user.

For a document source, write to `.sdd/work/<slug>/intake.md` instead, and record the source path (or "inline, <date>") in the header.

## Candidate External Actions (for the Review Gate)
- Create the drafted issues in the active tracker, linked to the parent, and create the drafted dependency links between siblings in the same batch, so the tree lands complete in one pass. For a document source with no `parent=`, create the proposed Epic first.
  - Note for the user that created tickets do NOT carry the gate label, so the orchestrator will not pick them up until a human applies it. That is intentional. Label only the ones you want processed.
- Add a comment on the source ticket (ticket-based intake only) summarizing the breakdown and open questions.
- Link related existing tickets if duplicates were found during search.

## Quality Checks Before the Review Gate
- Every requirement in the dump maps to exactly one ticket or one open question.
- No proposed ticket is bigger than roughly one deliverable slice.
- The tracker was searched first for existing tickets covering the same ground, and anything already covered is proposed as a link to that ticket.
- Plans-ready, meaning the hierarchy uses the project's real issue types, every drafted dependency is an issue link in the creation batch, and no planning field (dates, sprints, versions, estimates, teams) appears that the dump did not explicitly supply.
