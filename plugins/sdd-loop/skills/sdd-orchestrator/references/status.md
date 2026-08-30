# Status (one screen)

Goal – one compact screen. No stage work, no Review Gate executions.

Invocable as `sdd-status` or `/sdd status`.

## Resolve

Scope per orchestrator Step 0. Preflight **read-only** per Step 0.5 (do not run the green baseline unless the user asks). Search the eligible queue per Step 1 (gate label + assignee, not-done).

## Screen

Print, in this order, and stop.

1. **Scope** — tracker, site, projects, gate label.
2. **Preflight** — constitution and verification as present (path) or MISSING; context docs as INFO; CI as INFO; `test: none` consequence when recorded.
3. **Eligible queue** — key, summary, type, priority. Zero is a valid screen.
4. **Inferred stage** — for each queued ticket, the Step 2 rubric in one word (`intake` / `spec` / `design` / `dev` / `verify` / `docs` / `bug` / `lite` candidate), plus high/medium/low. Do not wait for stage approval; this is display only.
5. **Ledgers** — counts and first lines of OPEN / ATTENTION in `.sdd/GATES.md` and OPEN in `.sdd/PENDING-ACTIONS.md`. "none" when a file is missing.
6. **Autonomy** — leftover `autonomy.json` or `.approve-external` if present (age of heartbeat).

Offer `sdd-doctor` for the full health check. Do not mutate ledgers, tickets, or git.
