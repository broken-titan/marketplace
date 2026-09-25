# Pass

Do these in order. Do not skip to a patch.

## 1. Reproduce

Get the failure on this tree. Prefer a test. If a test cannot be written yet, a command that fails the same way is enough; then write the test before the fix.

Record the command and the failure.

## 2. Locate

Narrow where the wrong value or branch is. Read, add a probe, or bisect. Stop when you can say which function or contract is wrong.

## 3. Hypothesize

State one cause: this input, this branch, this stored value. The next change must be the experiment that would falsify it.

## 4. Change

Write a failing test that shows the bug if you do not already have one. Watch it fail for this bug. Then the smallest production change. No nearby cleanup in the same edit.

Re-run the reproduction. The original failure must be gone. The new test must pass.
