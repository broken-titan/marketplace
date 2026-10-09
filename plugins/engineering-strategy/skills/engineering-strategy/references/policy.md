# Guiding policies

Policy interprets diagnosis into **explicit tradeoffs**.

A sentence with no tradeoff is a slogan. Leave it out.

## Set policy

1. Confirm the diagnosis covers the load-bearing themes.
2. Add policies until every diagnosis is addressed. Map each policy to one or more diagnosis ids (`D1`, `D2`, …).
3. Merge policies that overlap.
4. Back-test against recent decisions in this repo (ADRs, specs, review outcomes). A policy that cannot explain those decisions is incomplete or the diagnosis is.
5. Mine conflict again — especially from people who will live under the tradeoff.

If conviction is still low, return to refine (`references/refine.md`) instead of decorating the page.

## Altitude

Staffing ratios, technology choice, operating constraints, how decisions get made. A sprint plan, a Gantt chart, or a ticket breakdown is the wrong altitude.

## Kinds (use when they fit)

Common types — invent the instance from *this* repo’s evidence:

- **Approval** — who decides a recurring choice, and how to escalate
- **Allocation** — how scarce time or headcount splits
- **Direction** — an unambiguous must (consistency over local judgment)
- **Guidance** — how to frame a class of tradeoffs

## Each policy block

- **Statement** — the rule, specific enough that two readers apply it the same way
- **Tradeoff** — what is accepted as cost
- **Diagnoses** — `D-n` ids
- **Coherent action** — links to specs, architecture decisions, or living design docs that already (or will) carry the work

## How many

As many as the diagnosis requires. Boring and inevitable is a good sign.
