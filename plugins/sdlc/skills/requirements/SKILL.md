---
name: requirements
description: SDLC phase 1. Turn intent into a living spec - a crisp, numbered FR-*/NFR-* requirements doc that is the source of truth. The agent drafts; a human signs off the spec. Use to start a feature, or when the spec needs updating from new feedback. Ticket decomposition is the separate `tickets` skill, run after Design.
---

# Requirements - intent → living spec

Phase 1 of the `sdlc` loop. Produces the **living spec**: the durable, human-signed artifact that
every later phase flows from and writes back to. Code, design, and tests are downstream of this
document - keep it current, not a one-time handoff.

> **The spec encodes the *why*.** Code crisply states *what* it does; the spec states *why* it's
> like this and *what success looks like*. That's the artifact worth reviewing and keeping fresh -
> for humans and for the agent re-reading it on the next pass.

## Artifacts

No config file. Write the spec to `docs/<feature>-requirements.md` (and
`docs/<feature>-open-questions.md`) - match the repo's existing convention if one is present.
Tickets/Jira are the downstream `tickets` skill's concern, not here.

## Pipeline (agent drafts, human ratifies)

### 1. Establish intent
Before writing anything, get to *who the user is, what problem, what the business needs*.
- **Pull from where requirements live** - a Confluence page (`getConfluencePage` /
  `searchConfluenceUsingCql`), a Jira epic (`getJiraIssue` + children), a provided PRD/doc, or the
  conversation. Distill into a compact brief; keep a link back to the source for traceability.
- **Explore the repo to verify assertions** - confirm what already exists before specifying new
  work; reuse the domain's ubiquitous language (the glossary the steering lane maintains).
- **Interview relentlessly.** Walk each branch of the design tree, resolving dependent decisions
  one at a time, until you reach shared understanding. Don't guess to fill gaps - **record unknowns
  in the open-questions log** (`<feature>-open-questions.md`) rather than inventing an answer.
- **Pin measurable NFR goals** (latency, availability, error budgets, a11y) before writing the
  spec - a vague "fast" becomes an untestable requirement. State each as a number in §7.

### 2. Write the living spec
Write intent down as a crisp spec - *as formal as it needs to be, no more*. Use numbered
`FR-*`/`NFR-*` so each requirement is referenceable from tickets and reviews. Follow the structure
of the canonical example, [lab-ops-requirements.md](docs/lab-ops-requirements.md):

```
# <Feature> - Requirements
> What this is · companion docs · Date (absolute) · Owner · Based on (sources)
1. Overview & purpose
2. Goals
3. Stakeholders & reviewers
4. Scope  (in scope / out of scope & deferred - be explicit about what's intentionally absent)
5. Assumptions & constraints
6. Functional requirements        # numbered FR-*, grouped (shared behaviors first, then per area)
7. Non-functional requirements    # NFR-* - measurable (≤2s, WCAG 2.2 AA, TLS 1.3 …)
8. Phasing - what's available at launch
9. Related documents              # design doc, interface specs, open-questions
```
Rules: convert relative dates to absolute; **no file paths or code snippets** (they go stale);
state requirements as observable behavior, not implementation. Optionally fold user stories
(`As an <actor>, I want <feature>, so that <benefit>`) into Overview/Goals to ground the FR-*.

### 3. CHECKPOINT - human signs off the spec
Present the spec for review and **stop**. Non-technical reviewers read §4–§7. Sign-off here is the
gate into the **Design** phase. Ticket decomposition does not happen here - it runs after Design,
via the `tickets` skill, so slices can cut through the *designed* interfaces.

## Living-spec discipline (backflow)
When a later phase learns something - a design constraint, a failing property, customer feedback -
**update the spec first**, bump affected `FR-*`, then re-derive tickets/design. Keep the spec, the
open-questions log, and ticket acceptance criteria in sync. A stale spec poisons every downstream
phase.

## Traceability
Keep a link back from each `FR-*` to its source requirement (Confluence/Jira/doc URL) so the chain
**source → FR-\* → ticket → PR → deploy** stays navigable. The `FR-*` numbers are the anchor the
`tickets` skill and reviews reference.

## What it never does
Proceed past the spec checkpoint unprompted, derive or create tickets (that's the `tickets` skill),
state requirements as implementation/file paths, or fill unknowns with guesses instead of
open-questions.
