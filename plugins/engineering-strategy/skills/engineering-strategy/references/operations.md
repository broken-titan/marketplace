# Operations

Mechanisms that inspect whether policies are followed.

A policy with no operation is unused paper. Draft policy and operations as separate sections; they may sit next to each other in the published doc.

## What to specify per policy

1. **Inspect** — how you can tell the policy is in use (metric, review, sample of decisions). The inspect **cannot fail silently**: a missed look is visible (empty dashboard, overdue cadence, missing exception log).
2. **Exception** — who may grant a **written** exception, and where that record lives. Unwritten exceptions do not exist.
3. **Cadence** — how often someone looks, what they open, and who notices if they skip.

If you cannot name those three, the operation is not done.

## Mechanism kinds (pick; do not stack all)

- **Nudges** — context at decision time (a check in review, a bot on the path people already use). Often the lightest way to keep a policy alive.
- **Inspection** — a dashboard, a sample of decisions, or a scripted pull. Pair with cadence so it cannot rot unread.
- **Approval or advice** — a named forum for the ambiguous case. Say how to get on it.
- **Written exceptions** — findable, dated, owned. Calibrate later requests against prior ones.
- **Automation** — only when the path people use is already clear; a bad form is not a policy.
- **Explicit deferral** — a reopen date when you cannot operate a slice yet.
- **Meetings** — last resort. Easy to start, expensive to keep. Prefer canceling one over adding one.

Prefer mechanisms this organization already runs. A new ritual needs a reason.

## Evaluate before committing

For each mechanism, check:

- Leading *and* lagging signal, or say which is missing
- Adoption cost (incremental vs big-bang)
- Burden on the people following the policy
- Burden on the people running the mechanism
- How much it depends on one person’s authority
- Whether the culture will run it or fight it

Drop a mechanism that fails these and still claim the policy is “in force.”

## Output

For `strategy-operations`, write `docs/<slug>-strategy-operations.md` keyed by policy id (`P1`, …). The full skill copies or links that table into the living strategy doc (reader section: Operations).
