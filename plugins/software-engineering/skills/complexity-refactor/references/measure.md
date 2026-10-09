# Measure

Cyclomatic complexity (CC) for a function is **decision points + 1**.

Count each:

- `if`
- `else if`
- `case` / `when` arm
- loop (`for`, `while`, `do`, `for-each`)
- `catch` / `except` / `rescue`
- ternary (`? :`, `if`/`else` expressions)
- `&&` / `||` (and `and` / `or`) inside a condition

Do not count `else` by itself. A bare `else` is the leftover path. Leave it out of the count.

A function with no decisions is CC 1.

## Tools first

Prefer a real tool over a hand count. Use the first that exists for the language and is already in the repo or easy to run:

| Language | Command |
|---|---|
| Python | `radon cc -s -a` |
| JS / TS | eslint `complexity` (project config or a one-off rule) |
| Go | `gocyclo` |
| Mixed / other | `lizard` |

If none of those run, count per function by the formula above and show the count next to the name. Say that the count is manual.

## Project thresholds win

If the repo already sets a complexity ceiling (eslint `complexity`, radon, sonar, lizard, a Makefile target, a CI gate), **that number wins**. Report against it. Do not invent a stricter house limit.

## Defaults when none exist

| CC | Action |
|---|---|
| 1-5 | Leave alone |
| 6-10 | Watch. Refactor only if already touching the function |
| 11-15 | Refactor now |
| 15+ | Must split |

Apply the band to the function you measured. File-level totals do not set the band.
