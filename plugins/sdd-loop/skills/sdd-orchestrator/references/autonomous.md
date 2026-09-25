# Mode Playbook: Autonomous

Goal – hands-off spec-driven development. The loop carries eligible tickets through the full pipeline (intake -> spec -> design -> dev -> verify -> merge) and executes external actions itself, pausing only at the checkpoints the user explicitly declared as gates. Gates are non-blocking, so a gated ticket parks while the loop keeps working the queue.

Everything in the orchestrator's Safety Rules still applies, except where this playbook states an explicit carve-out. Eligibility – the gate label plus assignment to the user – is unchanged, and is re-verified before every stage and before every batch of external actions.

## Startup (Hard Requirements)

Refuse to start unless ALL of the following are explicit in this invocation.

1. **Gates.** A `gates=` argument listing checkpoints from `{intake, spec, design, dev, verify, merge}`, or the literal `gates=none` for full autonomy. No default exists. Never assume, never reuse a previous run's gates, never infer from repo config. On a missing or malformed `gates=`, report the required syntax and stop.
2. **Scope.** Resolved from arguments or the repo `## SDD Scope` section, same rule as batch mode. Never run unscoped.
3. **Notify** (optional). `notify=` with a subset of `{jira, slack, push}`. The active tracker comment surface is always on as the approval surface. `slack` and `push` are labeled overlays in `references/notify.md`; this plugin ships no extras for them. An unknown channel fails the invocation.
4. **Preflight.** The orchestrator's Step 0.5 must pass – constitution and verification commands present – or the invocation must include `preflight=override`. Without the override, report what is missing and the remedy (sdd-init), and refuse to start. With the override, stamp a `PREFLIGHT WARNING` into the run summary and every work product. The Step 0.5 green baseline must also pass; a red baseline parks the run and is NOT overridable.
5. **Guardrail liveness self-test** (never overridable on a host that can fence). With `.sdd/` present, before writing `.sdd/autonomy.json`, and with no `.approve-external` sentinel, attempt a harmless probe command that matches the push guard's pattern but does nothing – e.g. `echo sdd-guard-probe git push`. On Claude or Cursor extras, the hook must block it with the sdd-loop guardrail message (or Cursor `{ "permission": "deny" }`).

   If the probe executes instead on a fencing host, the guards are not live. Refuse to start autonomous mode outright and point to sdd-doctor. Do not probe the write guard with a real write tool.

   If this host cannot fence, do not pretend the probe failed a missing PreToolUse. Refuse autonomous mode unless the user explicitly accepts **policy-only** in this invocation (record it in the run summary). Policy-only still requires `gates=`.

Then arm the run.

If `.sdd/autonomy.json` already exists, read its `heartbeat` before touching it.

- **Fresh** (within ~60 minutes – a single dev stage can legitimately run long between refreshes) means another autonomous run is likely active in this repo. Refuse to start, since deleting the file would kill that run's guard policy out from under it. Tell the user to stop the other run (`stop` on the sdd entry where it is running), or to delete the file themselves if they know it is dead.
- **Stale** marks a leftover from a crashed run. Delete it and proceed.

Either way, never inherit its contents. Then write `.sdd/autonomy.json`.

```json
{
  "mode": "auto",
  "gates": ["merge"],
  "notify": ["jira", "slack"],
  "scope": "site=<site> project=<KEYS>",
  "started": "<ISO timestamp>",
  "heartbeat": "<ISO timestamp>"
}
```

Refresh `heartbeat` to the current time at the top of every queue iteration and at every stage start and completion, leaving every other field untouched. sdd-doctor uses a stale heartbeat to tell a crashed run's leftover policy file from a live one.

The guardrail hooks read this file. External writes pass while it exists, and its `gates` list is honored as a hard ceiling, so merge stays mechanically blocked while gated. Deleting this file is the user's emergency stop. Treat its absence mid-run as STOP, and cease all external actions immediately, write the run summary, and end.

State the full active policy – scope, gates, notify channels – in the first status line.

On every exit (queue drained, `stop` on the sdd entry, fatal error), delete `.sdd/autonomy.json` and write a run summary covering tickets advanced, actions executed, gates parked, and attention items. Never leave the policy file behind.

## Checkpoint Semantics

A gate on checkpoint X means completing X's local work product, then PARKing. Do not execute X's external actions, and do not advance the ticket past X, until the gate is approved. The approver always reviews finished evidence – the drafted tree, the spec, the diff, the verdict – never intentions.

| Checkpoint | Parks after | Withheld until approval |
|---|---|---|
| `intake` | ticket tree drafted locally | creating child issues (with label + assignee propagation), breakdown comment |
| `spec` | spec drafted locally | publishing spec, remote link, comments |
| `design` | design drafted locally | publishing design, comments |
| `dev` | implementation + local verification + independent review done | push branch, create PR, summary comment, transition |
| `verify` | traceability matrix + suite run + drift report done | pushing added tests, posting verdict, spec corrections, transition |
| `merge` | PR open, CI green, no changes requested | merging the PR |

Ungated checkpoints auto-execute their external actions and the pipeline advances immediately. The pipeline ends at merge. Deploy is CI / out of loop. A Lite fast-track ticket treats a declared `spec` or `design` gate as parking once, after its combined document is drafted. Merge still requires `.sdd/work/<ticket-key>/trace.md`. `git push` to main/master/trunk and `--force` stay blocked without the sentinel even when merge is ungated.

## Queue Processing

Each iteration, in order.

1. **Resume pass.** Check every OPEN entry in `.sdd/GATES.md` for an approval (see Gate Approval). Once approved, execute the withheld actions, mark PASSED, and continue that ticket's pipeline. Also re-evaluate tickets parked on external waits, such as pending CI.
2. **Queue pass.** Run the batch-mode eligibility search. For each unparked, unprocessed ticket, highest priority first.
   - **Claim it first.** Atomically transition it to In Progress, discovering the project's real transition names (see Transitions). The claim makes ownership visible on the board and stops a second run – or a human – from double-working the item. A failed or unavailable claim transition means the ticket is contested or workflow-blocked, so skip it with an AUDIT entry and move on.
   - Then infer the stage under batch rules, where high or medium confidence proceeds and is logged; low confidence parks as ATTENTION rather than being skipped.
   - Advance stage by stage through the pipeline until a gate parks it, a failure parks it, or it completes (merged, or docs delivered).
3. **Re-verify** the gate label and assignee before each stage and before each batch of external actions. A ticket that lost either is dropped immediately with an AUDIT entry. This is a kill-switch layer, so honor it fast.

Unlike batch mode, external actions are NOT deferred to `PENDING-ACTIONS.md`. Ungated actions execute directly and are logged to `AUDIT.md`. The per-item sentinel is not used for autonomous execution, since the policy file authorizes it. (Review mode keeps its sentinel mechanics.)

## Gate Parking and the GATES.md Ledger

`.sdd/GATES.md` is the source of truth for parked work. Each entry carries a monotonically increasing ID that is never reused, the ticket key, the checkpoint, a status (`OPEN`, `PASSED`, `REJECTED`, `ATTENTION`, `SUPERSEDED`), the created timestamp, the evidence (local file paths, branch, PR URL), and – once resolved – who resolved it and how.

When parking at a gate, do all three.

1. Append the OPEN entry with its evidence.
2. Mirror to the active tracker. Comment on the ticket stating what is parked, where the evidence lives (PR link, published draft, or attached summary), and the exact approval instruction: "Add the label `sdd-approved-<checkpoint>` to this ticket to approve, or resolve via review mode."
3. Notify on the run's configured channels (see Notifications).

## Gate Approval

Two surfaces, one ledger.

- **Review mode** presents OPEN gate entries, alongside batch pending-actions and ATTENTION items, with their evidence. The user approves or rejects by ID. On approval, mark PASSED, and the withheld actions execute in-session under the per-item sentinel, or on the next autonomous iteration. On rejection, mark REJECTED, comment the rejection on the ticket, and stop advancing that ticket until its content changes.
- **Approval label.** During the resume pass, a parked ticket carrying `sdd-approved-<checkpoint>` for its parked checkpoint is approved. Before acting, read the issue changelog to identify who added the label, and record that identity in the GATES.md entry and in AUDIT.md. Then consume the label – remove it from the ticket – so a stale label can never approve a future re-park. A label for a checkpoint that is not currently parked is removed and logged as ignored.

Never treat any other artifact as approval. Comments, other labels, and transitions made by anyone else carry no approval weight.

## Failure Path: Bounded Retry, Then Park

- **Deterministic failures** (failing tests, lint or typecheck failures, red CI on the loop's own PR) get up to 2 fresh-context retry attempts within the run. Each retry re-reads the spec and the failure evidence without the prior attempt's reasoning. Still failing after that, park as ATTENTION with the failure evidence attached.
- **Park immediately, no retry**, where retrying adds no information. That covers low-confidence stage inference, material spec questions that survive the Clarify Loop's self-resolution pass, merge conflicts, a required tracker transition that does not exist or is blocked by workflow rules, missing access, and any ambiguity the Safety Rules say to stop on.
- ATTENTION entries use the same ledger, tracker mirror, and notifications as gates. They are resolved in review mode, where the user supplies guidance (recorded on the entry, after which the ticket re-enters the queue) or rejects.

Nothing is ever silently dropped. Every ticket the loop touched ends the run as completed, parked, or dropped-with-audit-entry.

## Merge Preconditions

When `merge` is ungated, or its gate is approved, merge only when ALL of these hold.

- All required CI checks on the PR are green. Treat CI that is still pending as a wait. Leave the ticket in the resume pass and re-check next iteration.
- No reviewer has requested changes. The FIRST changes-requested review on a loop-authored PR triggers one review-response pass, a fresh-context dev pass scoped to the review comments, which re-reads the spec and every comment, addresses or answers each one, pushes the update, and re-requests review. Log it to AUDIT.md. Changes requested again after that pass parks the ticket as ATTENTION – a human is engaged, so never merge past them. Either way, merging still requires the review to be re-approved or dismissed by the reviewer; never merge over an unresolved request.
- In repos with no CI configured, the loop's own verify stage (full suite, lint, typecheck per `## Verification`) must have passed in the worktree. Unverified code is never merged.

After a merge completes, remove the ticket's local worktree and local branch. The remote history is the record, and worktrees must never accumulate across runs.

## Transitions

Keep the board truthful, and transition tickets to match actual state. In Progress at claim (the start of the ticket's pipeline work), In Review at PR creation, Done at merge.

Discover each project's real transition names via the workflow; never hardcode them. A needed transition that is missing or blocked parks the ticket as ATTENTION. `Done` only ever happens at merge, never on the loop's own judgment that the code works.

## Non-Intrusive Operation (Comment Hygiene)

The tracker is a shared surface, so every write the team can see must earn its place. Aim for one comment per ticket per checkpoint event, and zero otherwise.

- **One SDD comment per ticket per checkpoint event.** Park, approval-request, rejection, and completion each justify a comment. Progress, retries, and internal stage transitions never do. Retry outcomes go to AUDIT.md only – and to the ticket only if the ticket ends up parked.
- **Update, don't stack.** When a ticket re-parks at the same checkpoint (after a rejection round-trip, say), update the run's existing mirror comment where the connector supports comment updates. Otherwise keep the new comment minimal and reference the old one.
- **No worklogs, no watchers, no field edits** beyond the transitions and labels this playbook explicitly defines.
- **Status transitions are the progress signal.** The board tells the team where things stand; comments are reserved for things a human must read or act on.
- **Run summaries stay local** (`.sdd/` and the session), never posted to the tracker. Slack and push get one summary message per run only when those overlays are connected (`references/notify.md`).

## Notifications

For every parked gate, ATTENTION item, and run summary, notify on the configured channels.

- tracker comment (always on): the mirror comment itself.
- `slack` / `push`: labeled overlays; see `references/notify.md`. Do not pretend extras exist.

Notifications are best-effort. A delivery failure is logged to AUDIT.md and never blocks, fails, or retries the run beyond one attempt per event.

## Audit Trail

`.sdd/AUDIT.md` is append-only. Log every external write the run executes (timestamp, ticket, action, target, result), every gate transition (parked; approved, with approver identity and surface; rejected), every retry, every dropped ticket, and every notification failure. Write the entry immediately after the action completes, before moving on.

Entries recording a stage completion or a merge link the machine-captured evidence file in `.sdd/evidence/` – raw command output, exit codes, and commit hashes, written verbatim by the dev and verify playbooks. Review mode shows the approver those files, so what they judge is the command output itself.

## Kill Switches (Honor All Three)

1. **Policy file deleted.** `.sdd/autonomy.json` gone mid-run. The hooks already fail closed, and the orchestrator must also stop all external actions, write the summary, and end.
2. **Gate label removed** from a ticket. That ticket is dropped at the next eligibility re-check, which happens before every stage and every action batch.
3. **`stop` on the sdd entry** – finish the current atomic action only, write the run summary, delete the policy file, end.

## Label Carve-Outs (Autonomous Mode Only)

Two narrow exceptions to "never touch labels yourself", both logged to AUDIT.md.

- **Intake propagation.** Child tickets created by an executed intake checkpoint inherit the gate label and the user as assignee, so the pipeline flows end to end. The `intake` gate is the control point for this self-expansion; the user accepted ungated propagation by explicitly declaring their gate set at startup.
- **Approval-label consumption.** Removing `sdd-approved-<checkpoint>` labels after recording them, as described in Gate Approval.

The gate label itself (`ai-allowed`, or the override) is still never added to pre-existing tickets and never removed from anything.
