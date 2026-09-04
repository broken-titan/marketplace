# Select applicable checks

Read the staged diff, the branch diff against the merge base, or the paths the user named. Then mark each software-engineering skill as applicable or not. Do not invent a skill that is not in this plugin.

## Always, when there is a reviewable change

| Skill | Run when |
|---|---|
| `looks-good` own checks | Any reviewable diff |
| `requesting-code-review` | Source, test, or contract files changed |
| `comment-police` | Source files added or edited |
| `code-simplify` | Production or test code added or grown |
| `verification-before-completion` | The user is asking if the work is done, tests pass, or a review is ready |
| `lean-gate` | A ship-ready, staged, or to-be-pushed diff is in scope |

## Conditional

| Skill | Run when | Skip when |
|---|---|---|
| `test-driven-development` | The diff implements a feature or bugfix | Docs-only, generated-only, or no behavior change |
| `parameterized-testing` | Tests gain many cases, a boundary matrix, or copy-pasted test functions | No test cases added or split |
| `systematic-debugging` | The change is a bugfix, or a test is failing | No bug or failure is in scope |
| `exhaustive-match` | The diff adds or changes a switch, match, or closed key map | No closed-set branch or map |
| `complexity-refactor` | Touched functions are large, nested, or highly branching | Touched functions stay small and flat |
| `receiving-code-review` | Review comments have arrived on this change | No inbound comments |
| `change-architecture-diagram` | The user asked for blast-radius or data-flow diagrams | Diagrams were not requested |

## Exclusions

Apply a user exclusion to the matching own check or specialist only. Examples: "without docs" disables the docs own-check; "without lean-gate" disables the Lean Gate readiness check and does not touch the hook or toggle.

An unknown or malformed exclusion is a warning, not a disable.
