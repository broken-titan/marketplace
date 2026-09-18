# Exploration

First step. Do not open with a vision. Consider alternatives before attaching to one approach.

## Goal

Search the problem and solution space. Update priors. Implicit strategy already lives in how this repo decides things; industry / state of the art keeps those priors from going stale.

## This repo first (implicit strategy)

1. Living specs, roadmaps, and open-questions files under `docs/` (and any path the repo already uses).
2. Architecture decision records (status, options, consequences).
3. Living design docs and any in-force strategy file.
4. Org pressure the user or notes state: hiring freeze, deadline, compliance clock, platform load.
5. What is already treated as “how we do things” in review checklists or constitution-like files.

List paths. A claim with no path is an interview question, not a fact.

## Then outward (state of the art)

How similar teams recently approached the same *kind* of problem — internal first, then public writing. Record sources as generic kinds (paper, talk, adjacent team), not imported proper nouns.

Save judgment for diagnosis. If nobody’s mind moved, keep gathering.

## Alternatives

Write at least two plausible approaches on the page before anyone commits. Attaching to the first idea you like is the failure mode this step exists to prevent.

## Stop

When constraints, implicit rules, state-of-the-art notes, and at least one alternative are listed. Then diagnose.

## Output

For `strategy-explore`, write `docs/<slug>-strategy-explore.md`. In the living doc, this becomes the last reader section (same content, not a second file that replaces it).
