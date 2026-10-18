---
name: verification-before-completion
description: >-
  Use when you are about to say done, that tests pass, or that a pull
  request is ready.
---

# Verification before completion

## Files

| File | When |
|---|---|
| `references/paste.md` | What to run and what to paste |

## Hard rules

- Before you say tests pass, run them on this tree and paste the command and the output.
- Do not report lint as clean unless you ran it on this tree.
- Do not claim green from memory, from a previous turn, or from "the type checker would catch it."
- This skill only covers proving the change on your machine.

## Quality standards

- [ ] Write down the command you ran
- [ ] Paste the output from this run
- [ ] Claim matches that output (pass, fail, or skipped)

## Easy mistakes

- If you did not run the tests on this tree, run them and paste the command and the output.
- If you edited after the last run, run the command again on this tree.
- If you did not run lint on this tree, run it.
- If you are writing a ticket or opening a PR, stop; this skill only covers proving the change on your machine.
