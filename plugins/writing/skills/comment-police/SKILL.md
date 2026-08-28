---
name: comment-police
description: Polices code comments to prevent unnecessary additions during generation editing refactoring or review. Only permits essential comments for genuinely complex non-obvious logic and requires explicit user confirmation first as it signals potential over-complexity. Activate for any task involving source code in any language.
---

# Comment Police

## Overview

Enforces a strict "comments only when unavoidable" policy. Prioritizes self-documenting code via clear names, small focused functions, and simple structures. Comments are a last resort and a warning sign.

## Instructions

- Default to adding **no comments at all** when writing or modifying code. Code must stand on its own through intention-revealing names and obvious flow.

- Never insert comments that describe what the code literally does (e.g. no "# loop over items", no "# validate input", no redundant docstrings).

- Only contemplate a comment when the logic is truly intricate, involves subtle invariants, performance trade-offs, or domain rules that resist simplification and clear naming.

- The moment you feel "I need to explain what's going on here with a comment", treat it as a red flag: the code is probably too complicated.

- When that happens:
  1. Do not write the comment yet.
  2. First propose a cleaner, simpler refactoring or alternative implementation to the user.
  3. Ask explicitly: "This section is complex enough to warrant a comment. Should I refactor it to eliminate the need for explanation, or do you want a brief comment added after your approval?"
  4. Wait for clear user confirmation before adding any comment or keeping the complex version.

- For library or API code, use docstrings sparingly — only when the contract cannot be inferred from the function signature, parameter names, and type hints.

- Always favor refactoring toward simplicity over documenting complexity. If a comment feels necessary, a better design almost always exists.

- After any edit, re-scan for comment opportunities and challenge whether a structural improvement could remove them.

- If the user explicitly requests comments in straightforward code, add them but remind them of the maintainability cost.