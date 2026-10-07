# Tactics

Apply in this order. Stop at the first move that drops the function into the target band without changing behavior.

## 1. Guard clauses

Invert the happy path. Return, raise, or continue at the top when a precondition fails. Flatten the rest.

Reach for this when the body is nested under a chain of "still ok?" checks.

## 2. Extract function

Pull a block into a function whose name says what happens. Drop names that narrate the steps. The caller should read as a short sequence of intentions.

Reach for this when a branch or loop body needs its own sentence, or when a comment is explaining a section.

## 3. Lookup table / map

Replace an if-else chain or a switch that only maps a value to a result with a table, dict, map, or enum lookup.

Reach for this when each arm does the same kind of work (return a value, pick a handler, pick a message).

## 4. Named predicates

Give a boolean condition a name. Keep the `if` / `while`; make the test read as a claim.

Reach for this when the condition is a compound `&&` / `||` or a comparison that needs a domain word.

## 5. Polymorphism / strategy

Replace a switch-on-type (or switch-on-kind) with types or strategies that each own the branch.

Use this **only** when the same switch-on-type appears in two or more places. One switch stays a switch or a table.

## 6. Flatten loops

Extract the loop body. Prefer `continue` (or an early return from the extracted function) over an `if` nested inside the loop.

Reach for this when the loop has a deep "this element is interesting" nest.
