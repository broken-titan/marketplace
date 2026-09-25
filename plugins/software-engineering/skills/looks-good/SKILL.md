---
name: looks-good
description: >-
  Use when asked for a general software review, a looks-good pass, or
  whether a change is ready. Invoke this instead of composing several
  review skills by hand.
---

# Looks good

Nothing runs until this skill is invoked. It is not a hook and has no on/off toggle.

Invoke `looks-good` for a general software review. Do not hand-pick a stack of review skills unless the user named those skills.

## Files

| File | When |
|---|---|
| `references/select.md` | Detect the change surface and choose applicable skills |
| `references/report.md` | Buckets, verdicts, and how to cite evidence |

## Hard rules

- Detect the change surface, then run every applicable software-engineering check by default.
- Skip a skill that does not match the surface, and list it as `skipped as not applicable`.
- Honor per-run or per-user exclusions only ("run looks-good without docs"); do not read or write `.looks-good.yml` or any other looks-good repo config.
- If a per-run option is unknown or malformed, warn and run the default applicable set; do not silently disable checks.
- Report `run`, `skipped as not applicable`, and `disabled by user option` as separate buckets.
- Return exactly one verdict: `pass`, `fix before review`, or `needs human review`.
- Cite file and line evidence for every finding that affects the verdict.
- Own these checks: diff hygiene, naming/consistency, docs, user-facing polish, dead artifacts, and reviewability.
- Load an applicable specialist skill and follow it; do not paste that skill's full body into this report.
- Include Lean Gate readiness from `lean-gate` when a ship-ready diff is in scope; do not run the commit/push hook, write `lean-gate.ok`, or change the lean-gate toggle.
- Treat `sdd-loop` as a future optional final step after implementation verification; do not invoke it from this skill.

## Quality standards

- [ ] Change surface named (paths, kind of diff)
- [ ] Every software-engineering skill is in exactly one report bucket
- [ ] Unknown or malformed options warned, default applicable set still run
- [ ] Own checks covered: hygiene, naming, docs, polish, dead artifacts, reviewability
- [ ] Lean Gate readiness reported when applicable, hook not executed
- [ ] One verdict with file:line citations

## Easy mistakes

- If you started several review skills without an invocation of `looks-good`, stop and run this skill instead.
- If you skipped a check because a config file was missing, run the default applicable set.
- If you ran the lean-gate hook or wrote `lean-gate.ok` from this skill, revert that and report readiness only.
- If the verdict is a recap of the diff, replace it with `pass`, `fix before review`, or `needs human review`.
