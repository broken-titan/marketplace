---
name: sdd-orchestrator
description: >-
  Use when a gated ticket needs stage inference and the matching playbook
  (intake through merge). Deploy is out of this loop. Routes to intake,
  spec, design, dev, verify, docs, bug, or lite.
---

# SDD Orchestrator

Spec-driven development pipeline, running intake -> spec -> design -> dev -> verify. Merge is the last stage this loop owns. Deploy is CI / out of loop. Code is never written until a spec with testable acceptance criteria exists. Every stage produces its work locally first; external writes happen only through the Review Gate.

Host overlays: `references/hosts.md`. Tracker adapters: `references/trackers.md`. Notify overlays: `references/notify.md`. Context-only exclusions: `references/context.md`.

## Safety Rules (Non-Negotiable)
- Only work on tickets carrying the gate label AND assigned to the user. The gate label is `ai-allowed` unless the repo's `## SDD Scope` section overrides it with a `label:` entry. Never add, remove, or modify the gate label yourself. The only exceptions are the two narrow Autonomous Mode carve-outs in `references/autonomous.md` – intake propagation to newly created children, and consuming `sdd-approved-*` approval labels.
- Other tickets are read-only context. You may fetch and read them when following an information trail (linked issues, parents, duplicates), but never work on them, propose actions for them, or enqueue them.
- No external writes without explicit per-item approval at the Review Gate. That covers tracker comments, edits, transitions, and issue creation; Confluence publishing; `git push`; and PRs. The sole exception is Autonomous Mode, where the user's explicitly declared gate policy (recorded in `.sdd/autonomy.json`) authorizes stage actions per `references/autonomous.md`.
- Reads are always allowed.
- All code work happens in isolated git worktrees, never on main or shared branches.
- On ambiguity or missing access, stop and report rather than guessing.
- Fail safe. When it is unclear which stage, gate, or rule applies, take the stricter option – the earlier stage, the tighter gate, asking over acting.

## Step 0: Resolve Scope
Determine which tracker, site, and project(s) this run covers, in priority order.

1. **Arguments** – `site=<hostname-or-name>` and/or `project=<KEY>[,<KEY>...]` passed to the sdd entry.
2. **Repo default** – an `## SDD Scope` section in `docs/sdd-scope.md` (if that file exists), else the repo's agent-instruction files (`AGENTS.md`, `CLAUDE.md`, or similar). Fields include `tracker:` (default `jira`), `spec-storage:` (default `ticket-comment`), `site:`, `projects:`, and an optional `label:` to override the gate label.
3. **Interactive fallback** – if neither exists and more than one site or project is reachable, list the connected sites and their visible projects and ask the user to choose before searching.

A ticket key argument implies its own scope. Never search outside the resolved scope, and state the active scope in the first status line of every run. Do not assume Jira tool names exist unless a connector is connected. Load `references/trackers.md` for Linear / GitHub Issues only when `tracker:` names them.

## Step 0.5: Preflight (Project Readiness)
Goal – confirm the project context the playbooks depend on actually exists before any stage work in a repo. Two items are required.

1. **Constitution** – a `constitution:` path under `## SDD Scope`, or a `docs/sdd-constitution.md` / `CONSTITUTION.md` at the repo root. It holds the project's non-negotiable principles (see sdd-init); specs, designs, and code must comply with it.
2. **Verification commands** – the `## Verification` section, required for the dev, verify, and docs stages.

Commands recorded as `none` are a deliberate declaration, not MISSING – the docs-only repo case. They still carry a consequence. With no test command there is no green baseline and no verified merge, so batch and autonomous runs park dev and verify tickets as ATTENTION rather than proceed unverified. Docs tickets still flow. State this consequence in the preflight line whenever `test: none` is recorded.

Everything else is optional context and never blocks – product and structure context docs (`product:`/`structure:` paths under `## SDD Scope`, or discoverable equivalents such as docs/product*.md, docs/structure*.md, ARCHITECTURE.md) and coding guidelines (`guidelines:` paths, CONTRIBUTING.md, style guides under docs/). Load whichever exist. Product grounds intake and spec judgments, structure grounds design and dev layout, and guidelines govern how code is written. Their absence needs no override.

Report the following in the preflight line of your first status output.

- The two required items as present (with path) or MISSING.
- The context docs as INFO – found with path, or absent.
- Whether CI is configured (workflow/pipeline files, e.g. `.github/workflows/`), also as INFO, and therefore which merge regime an autonomous run would use – CI-green, or the loop's own full verification. Deploy stays in CI; this loop's last stage is merge.

On missing items, behavior depends on the mode.

- **Interactive** – warn once with what is missing, why it matters for the stages ahead, and the remedy (sdd-init). Ask whether to proceed anyway, and record "preflight overridden by user" in the work product if they do.
- **Batch and autonomous** – refuse to start unless the invocation includes `preflight=override`. With the override, proceed and stamp a `PREFLIGHT WARNING` line listing the missing items into every work product and run summary of that run. Never override silently.

**Green baseline.** Before any stage work, run the recorded verification commands once against the base branch and record the commit hash and result in the run's first status output. This applies to batch and autonomous runs inside the repo checkout; offer it interactively before a dev, verify, or docs stage. With `test: none` recorded there is nothing to run – skip the baseline and apply the `none` consequences above instead.

A red baseline means failures during dev are unattributable, so each mode responds differently.

- Autonomous runs park the whole run as ATTENTION with the failure evidence, and stop.
- Batch runs skip dev/verify/docs tickets (logging "red baseline" in `.sdd/skipped.md`) but may still process intake, spec, and design.
- Interactive runs warn and let the user decide, recording the caveat.

`preflight=override` does NOT override a red baseline. The override covers missing documents; the baseline is a measurement of the repo as it stands.

Missing preflight items never alter which tickets are selected, only whether stage work starts.

## Step 1: Select
- If the user supplied a ticket key, fetch it and verify BOTH the gate label and that the ticket is assigned to the user. If either fails, report which one and stop.
- Otherwise search within scope using the active tracker adapter (`references/trackers.md`). Jira default: `project in (<KEYS>) AND assignee = currentUser() AND labels = "<gate-label>" AND statusCategory != Done ORDER BY priority DESC, updated DESC`. Omit the project clause only when the scope is an entire site.
- List results compactly (key, summary, type, status, priority) and ask the user which to process. On zero results, report and stop.

## Step 2: Infer Stage
If the invocation pinned a stage with `stage=<intake|spec|design|dev|verify|docs|bug>` (aliases: `specify`→spec, `plan`→design, `implement`→dev), use it, record "stage pinned by user" in the work product, and skip inference.

Otherwise fetch the full ticket – description, comments, links, attachments list, linked pages – then score it against this rubric and pick the single best fit.

- **Intake** – a long unstructured description or pasted notes, multiple features or concerns mixed together, no acceptance criteria, no linked spec. Often an Epic or an oversized Story. The ticket is really several tickets.
- **Spec** – a single scoped feature or change, but no spec document and no testable acceptance criteria. The intent is clear; the contract is not.
- **Design** – a spec or solid acceptance criteria exist (linked page or structured description), but no agreed technical approach – no architecture notes, interface definitions, or test plan.
- **Dev** – spec and design are present and sufficient, acceptance criteria are testable, and nothing material is unresolved in the comments.
- **Verify** – an implementation already exists (linked branch, PR, or referenced commits) and the ask is validation, test coverage, or acceptance checking.
- **Docs** – the deliverable is documentation only. Playbook: `references/docs.md`.
- **Bug** – current / expected / unchanged plus named regression tests. Playbook: `references/bug.md`. Pin with `stage=bug`.

**Lite fast-track.** When the best-fit stage is Spec or Design and the ticket is small, low-risk, and well-understood – one contained slice, clear intent, none of the risk exclusions in `references/lite.md` – propose Lite instead, meaning a single combined mini spec+design followed straight by dev, with one stop at the Review Gate. In interactive mode the user's approval of the Lite proposal replaces the per-stage approvals. In batch and autonomous modes, fast-track only on high-confidence eligibility, logging the evidence; anything lower runs the normal stages.

Present to the user the proposed stage (or Lite), the top 2 to 3 pieces of evidence from the ticket, a confidence level (high/medium/low), and what the stage playbook will produce. If confidence is low, say so and offer the runner-up stage. **Wait for the user to approve the stage before any stage work.**

## Step 3: Run the Stage Playbook
Before starting any playbook, read `.sdd/notes.md` if it exists. It holds durable project memory – gotchas, conventions, decisions – from earlier tickets. After finishing a playbook, append any newly learned durable facts to it, dated and attributed to the ticket key. Record only what future tickets benefit from, never per-ticket status.

Also load what Step 0.5 found. The constitution binds every stage; a spec, design, or change that would violate it must surface the conflict as an open question or ATTENTION item, never silently comply and never silently violate. Of the optional context docs, product context grounds intake and spec judgments, structure context grounds design and dev layout choices, and guidelines bind how code and docs are written.

**Corrections flow backward, then forward.** When any stage discovers a requirements problem – a wrong, missing, or ambiguous requirement, as opposed to a code bug – the fix goes to the spec first and flows forward through design and dev. Never patch code into disagreement with its spec. In-flight, that means returning the ticket to the stage that owns the error; spec updates are external actions and follow the active mode's approval rules. Post-delivery, that is Evolve Mode.

Read the matching file in this skill's `references/` directory and follow it exactly.

- Intake: `references/intake.md`
- Spec: `references/spec.md`
- Design: `references/design.md`
- Dev: `references/dev.md`
- Verify: `references/verify.md` (definition of done lives only there)
- Lite: `references/lite.md` (the approved fast-track only)
- Docs: `references/docs.md`
- Bug: `references/bug.md`

Standalone invocable surfaces (also `/sdd` aliases) point at playbook sections; they do not split this plugin.

- Clarify: `references/spec.md` § Clarify Loop — skill `sdd-clarify`
- Analyze: `references/analyze.md` — skill `sdd-analyze`
- Constitution: `references/constitution.md` — skill `sdd-constitution`
- Converge: `references/converge.md` — skill `sdd-converge`
- Status: `references/status.md` — skill `sdd-status`

Every stage work product is a draft. Write them under `.sdd/work/<ticket-key>/` (`intake.md`, `spec.md`, `design.md`, `tasks.md`, `verify.md`, `lite.md`, `trace.md`), never loose in the repo unless `spec-storage: in-repo` says otherwise for the published spec. All playbook output stays local until Step 4.

**Stable IDs.** FR/AC IDs are assigned at intake (or the first stage that can number them) and reused in spec and verify. Never renumber. Write a bidirectional trace artifact `.sdd/work/<ticket-key>/trace.md` before any merge action: intake ID → spec ID → verify evidence. Merge is blocked if that file is missing or an AC has no row.

## Step 4: Review Gate (Mandatory Stop)
Present three things.

1. A summary of the local work, with diffs, file listings, or the drafted document as appropriate.
2. Verification results where relevant, covering tests, lint, and type checks.
3. A numbered list of proposed external actions, each naming its target and its content. E.g. "Create 4 child stories under PROJ-120 as drafted", "Publish spec per spec-storage and add a remote link to PROJ-123", "Add a comment to PROJ-123 summarizing open questions".

Then say: "No external actions have been taken. Reply with the numbers to approve, or 'none' to stop here." Execute only approved items, one at a time, confirming each result.

On execution, a host guardrail hook (when the host can fence — `references/hosts.md`) blocks external write tools and `git push` unless `.sdd/.approve-external` exists. For each approved item, create that file, execute the single approved call, and delete the file immediately, before reporting the result. Never create the sentinel without a specific user-approved item, and never leave it in place between items. On a policy-only host, still follow this ritual; the fence is not mechanical.

`git push` to `main` / `master` / `trunk`, and `git push --force` / `-f` / `--force-with-lease`, stay blocked even in autonomous mode unless the sentinel is present.

## Step 5: Next
Ask whether to continue this ticket into the next stage, pick another eligible ticket, or stop. Re-run Step 2 when continuing, since the ticket's content has changed.

## Batch Mode
Activated when the user passes `batch` to the sdd entry. The goal is to keep working through the eligible ticket queue without waiting on the user, while performing ZERO external writes. A host-specific loop driver is an overlay in `references/hosts.md`, not a universal switch.

Six behaviors change from interactive mode.

- **Explicit scope required.** Batch mode never runs unscoped. If Step 0 resolves no scope from arguments or the repo default, stop immediately and report that batch mode needs `site=`/`project=` arguments or an `## SDD Scope` section. Do not fall back to asking-and-guessing, and do not search all sites.
- **Queue instead of pick.** Run the Step 1 search within the resolved scope, then process every result not already listed in `.sdd/processed.md`, highest priority first.
- **Stage approval becomes stage logging.** At Step 2, proceed automatically when confidence is high or medium and record the inference and evidence in the work product. When confidence is low, skip the ticket, log it in `.sdd/skipped.md` with the reason, and move on. Never guess on low confidence.
- **The Review Gate is deferred to Review Mode.** At Step 4, do not stop. Append each proposed external action to `.sdd/PENDING-ACTIONS.md` as an entry with a monotonically increasing ID that is never reused, status OPEN, the ticket key, the action, and the exact content or a reference to the output file. External writes never happen in batch mode; prior approval does not enable them, and all approvals are collected in Review Mode.
- **Repo-dependent stages.** The dev, verify, docs, and lite playbooks require the scoped repo's checkout. If the current working directory is not inside that repo, skip those tickets and log them in `.sdd/skipped.md` with reason "requires repo checkout". Intake, spec, and design run anywhere with tracker access.
- **State tracking.** After finishing a ticket's local work, append its key, inferred stage, the ticket's `updated` timestamp, and output file paths to `.sdd/processed.md`, so later passes never redo work. Re-process a ticket only when its current `updated` timestamp is newer than the one recorded. When re-processing, mark that ticket's earlier OPEN entries in `PENDING-ACTIONS.md` as SUPERSEDED before appending new ones.
- **Exit.** When the queue is empty (no unprocessed gate-labeled tickets), report "queue drained" with a summary of processed, skipped, and pending-action counts.

## Autonomous Mode
Activated by `auto` on the sdd entry. Hands-off pipeline execution, where external actions run without per-item approval, pausing only at the checkpoints the user explicitly declared with a mandatory `gates=` argument (from `{intake, spec, design, dev, verify, merge}`, or `gates=none`).

Gates are non-blocking. A gated ticket parks in `.sdd/GATES.md`, gets mirrored to a tracker comment, and the loop keeps working the queue. Approval comes via review mode or an `sdd-approved-<checkpoint>` label. Failures get bounded retries, then park for attention. Read `references/autonomous.md` and follow it exactly; refuse to start if its Startup requirements are not met.

## Review Mode
Activated by `review` on the sdd entry. This is the consolidated Review Gate for work done in batch mode, plus the resolution surface for autonomous-mode gates.

1. Load `.sdd/PENDING-ACTIONS.md` and `.sdd/GATES.md`. If neither has OPEN (or ATTENTION) entries, report that and stop.
2. Present OPEN entries grouped by ticket, each with its ID, the action or parked checkpoint, and where to read the full content or evidence. Present ATTENTION entries with their failure evidence.
3. Ask which IDs to approve. Execute approved entries one at a time, confirming each result, and mark them DONE (pending actions) or PASSED (gates) with a result note. Mark declined entries REJECTED. For ATTENTION entries, record the user's guidance on the entry so the next autonomous run can act on it, or mark it REJECTED.
4. Never execute an entry marked DONE, PASSED, REJECTED, or SUPERSEDED. Never batch-execute without per-ID approval.
5. Use the same sentinel mechanics as the interactive Review Gate – create `.sdd/.approve-external` per approved entry, execute the single call, delete the sentinel immediately.
6. Housekeeping at session end. Offer to archive resolved entries (DONE, PASSED, REJECTED, SUPERSEDED) out of `PENDING-ACTIONS.md` and `GATES.md` into `.sdd/archive/`, so the live ledgers stay short. After executing a merge, offer to remove that ticket's local worktree and branch, since the remote history is the record.

## Direct Intake Mode (Document or Inline Requirements)
Activated by `intake <file.md>`, or by `intake` with requirements text provided inline in the invocation message. The user-supplied document replaces the tracker ticket as the requirements source; the user handing it over is the authorization to process it, so no gate label applies to the source itself.

Six things differ from ticket-based intake.

- **Scope is still required.** Issue creation needs a target project. Resolve per Step 0; if no project can be resolved, draft the tree anyway and mark the external actions as blocked on scope.
- **Skip Steps 1-2.** The stage is intake by definition. Read the file (or the inline text) as the dump.
- **Parent.** `parent=<KEY>` attaches the drafted tree under that existing ticket. Verify it exists and is in scope; it does NOT need the gate label, since creating children under it is a Review Gate action like any other. Without `parent=`, the draft proposes a new Epic as the tree root.
- **Run `references/intake.md`** with the document as the source. Write the output to `.sdd/work/<slug-of-filename-or-topic>/intake.md` and record the source (path, or "inline, <date>") in its header for traceability.
- **The Review Gate is unchanged.** Every issue creation, link, and comment is a proposed external action requiring approval. Created tickets never carry the gate label; the user applies it to the ones they want the loop to work, same as ticket-based intake.
- **Not available in batch or autonomous mode.** Those modes discover work from the tracker queue only. A direct intake is always an explicit, attended invocation.

## Evolve Mode (Spec Drift)
Activated by `evolve <ticket-key>`. Runs the verify playbook's Drift Check section only. Compare the ticket's spec against the actual code behavior, produce a drift report listing where reality and spec diverge, and propose spec updates – or code fixes, if the spec is right and the code drifted – as external actions through the Review Gate.

## Spec Storage
`spec-storage:` under `## SDD Scope` chooses where the published spec lives.

| Value | Where stakeholders read it | Committed? |
|-------|----------------------------|------------|
| `ticket-comment` (default) | Comment (or attachment) on the ticket | No. Local copies under `.sdd/work/` stay drafts. |
| `confluence` | Configured Confluence space + remote link on the ticket | No. Needs `confluence-space:` and a connected Confluence connector. |
| `in-repo` | Markdown at `spec-path:` (default `docs/sdd/<ticket-key>.md`) | Yes, when the profile says in-repo. |

"Never committed" is the default until the profile says `in-repo`. All publishing is an external action and goes through the Review Gate. If a Confluence connector is not connected, do not pretend it is; fall back to ticket-comment and say so.

## State Directory
`.sdd/` lives at the repo root when running inside a git repository, otherwise in the current working directory. It holds the following.

- `processed.md`, `skipped.md`, `PENDING-ACTIONS.md`.
- `GATES.md` – the autonomous-mode gate and attention ledger.
- `AUDIT.md` – an append-only log of every autonomous external action.
- `notes.md` – project memory.
- `work/<ticket-key>/` – stage work products, including `trace.md`.
- `evidence/` – machine-captured verification and action evidence.
- `archive/` – resolved ledger entries moved out by Review Mode.
- Transiently, `.approve-external` (the guardrail sentinel, which must never persist between approved calls) and `autonomy.json` (the autonomous-run policy file, deleted at run end and never left behind).

It is local state and should be gitignored (offered by sdd-init), except published in-repo specs which live outside `.sdd/`.

## Gotchas

- `/loop` and PreToolUse are host overlays (`references/hosts.md`), not the contract.
- `auto` without an explicit `gates=` must refuse; there is no default gate set.
- A missing constitution is WARN interactively and a refuse in batch/auto unless `preflight=override`.
- `preflight=override` does not override a red baseline.
- Linear / GitHub Issues stay off until `tracker:` names them.
- Flattening `sdd-clarify` / `sdd-analyze` / `sdd-constitution` / `sdd-converge` / `sdd-status` into this file loses invocable surfaces.

## Quality bar

- [ ] Gate label + assignee both verified before stage work
- [ ] External writes only through the Review Gate (or the declared autonomous policy)
- [ ] Stage playbook file followed; FR/AC IDs never renumbered
- [ ] Trace file present before any merge action
- [ ] Instruction-file pattern used for scope, not a single-vendor target
