# Refine — test, map, model

Pick the technique that fits. Situational awareness before org-wide pressure.

## When to run vs skip

**Run** when the next step would apply a policy across teams, or the landscape is still moving (build-vs-buy, evolution, a new capability class).

**Skip** only for a short internal loop — one team, one habit, one sprint. Write the reason. Mapping or a trial adds nothing there.

## Modes

| Mode | Produce |
|------|---------|
| **test** | A cheap narrow trial and what it resolved |
| **map** | Wardley map + implications |
| **model** | Systems sketch (stocks, flows, feedback) + implications |
| **both** | More than one technique, then one implications list |
| **skip** | One sentence why this is a short internal loop |

Infer from the ask. If unclear, ask once. Combine techniques when one leaves a load-bearing uncertainty open.

An **untested strategy** is org-wide pressure with no trial. Name that finding; do not set the living doc In force until a cheap test exists or skip is justified.

Stop testing when the load-bearing uncertainty is resolved. More trials after that are stalling.

## Strategy testing (test)

A cheap, **narrow** trial before the organization feels the policy.

- Scope: one component, one module, or one integration — not the fleet.
- Time: short enough that a miss is recoverable.
- Question: the single uncertainty the diagnosis still hangs on (will this interface hold, will this allocation starve the other work, will the exception path get used).
- Result: what changed in diagnosis or policy, or “uncertainty remains; next trial is …”

Write the trial plan and the outcome in the refine artifact. A plan with no outcome is still Draft.

## Wardley mapping (map)

Zoom-out ecosystem. Components: **users**, **needs**, **capabilities**. A box on a user is a need; a box on a need is a capability. Capabilities never attach directly to a user.

- **X-axis** (evolution): genesis → custom → product → commodity
- **Y-axis**: visibility to the user (high = seen; low = invisible dependency)

Start small (one user is enough). Draw value chains, then place them. Study the current map. Optionally a second map for a predicted evolution. Implications must name what diagnosis or policy would have to change.

Syntax: Mermaid (`flowchart` / `graph`) or a labeled table. PlantUML only when the repo already uses it. Stay generic.

## Systems modeling (model)

Stocks (work in progress, unreviewed changes, open incidents), flows (arrive / finish), feedback (the policy that speeds or starves a flow).

Sketch the loop. Name the stock you would measure. State what happens if a policy pushes one flow without a balancing loop. Implications feed diagnosis or policy.

## Output

`docs/<slug>-strategy-refine.md`: mode, skip-reason or the test/map/model, implications for diagnosis and policy ids. The full skill links this file (reader section: Refine).
