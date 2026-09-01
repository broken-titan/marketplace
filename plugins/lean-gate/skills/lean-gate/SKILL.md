---
name: lean-gate
description: >-
  Use immediately before git commit or git push. Review the staged
  or to-be-pushed diff and keep only the smallest change that meets
  the request in front of you. Do not keep this loaded for ordinary
  editing.
---

# Lean Gate

Load this only when you are about to commit or push. It is not an always-on stance.

Walk the staged diff before `git commit`. Walk the commits and file diff that would leave this clone before `git push`. Then answer each item in order.

1. Does every hunk meet a request that was actually made? Drop work that only might be useful later.
2. Is this the smallest change that still meets that request? Prefer deleting or shrinking code over adding a new layer.
3. Did you introduce an abstraction, helper, or seam that has no second caller now? Remove it and keep the direct code.

If the diff fails any item, change the tree first. Do not commit or push the extra work.

When the hook blocks the command, finish this checklist, write `lean-gate.ok` in the repository git dir (`git rev-parse --git-dir`), and retry the same command. Do not write that file to skip the review.
