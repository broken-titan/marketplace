---
name: effort-reminder
description: >-
  At session start or the first user ask, check whether the current effort
  level matches the task. Soft reminder only — never change the control.
---
# Effort reminder

## When
Run once at session start, or on the first substantive user ask of a new thread.
Do not repeat every turn. Do not auto-change effort.

## Categories
- **Low** — sketching, brainstorming, or an easy change; quick in-loop responses.
- **Medium** — building and regular day-to-day work.
- **High** — fixing something big / chasing edge cases; verification matters.
- **Max** — hard handoff, security vulns, end-to-end; operate fully autonomously.

## Steps
1. **Read current effort** if the harness exposes it (session settings, `/effort`
   state, env/config the agent can query). If unavailable, leave `current` unknown.
2. **Classify** the user’s ask into Low / Medium / High / Max using the categories above.
3. **Remind only on mismatch** (or when `current` is unknown and the ask is clearly
   High or Max). One short line, then continue the real work. Examples:
   - "This looks High (edge-case chase) — bump effort if you’re still on Low/Medium."
   - "This looks Low (quick sketch) — drop effort if you’re on High/Max to save spend."
4. **Never** toggle, set, or request a UI change beyond that one-line note.

## Out of scope
Auto-switching effort, per-turn nagging, product-specific framing.
