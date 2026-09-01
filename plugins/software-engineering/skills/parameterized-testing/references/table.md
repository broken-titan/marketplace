# Table

Parameterize when every case is the **same behavior** with different inputs or expected values.

Do **not** parameterize when:

- Setup differs (different fixtures, different collaborators, different I/O).
- Control flow in the test differs (`if` on the row, skip some asserts, call a different helper).

If setup or control flow differs, split them into two tests.

## How to build it

1. Name the behavior once (the test name).
2. Add a table. Each row has a **name** that says what the case is (empty input, upper bound, the bug from ticket N).
3. Add the failing row first. Run it. Watch that row fail for the missing case. Then the smallest production change.
4. Add further rows only after that row is green, still one behavior.

## Idiom

Match the repo:

- Python: existing `parametrize` (or the project’s table helper)
- Go: table-driven tests
- JS / TS: `test.each` / `it.each` if already in use
- .NET: `Theory` / `InlineData` if already in use
- Other: the same idea in whatever the suite already ships

Do not introduce a second parameterization style in one package.
