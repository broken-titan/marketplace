# Workflow

1. Identify the functions this change touches (the ones you will edit, plus callees you will split out of them).
2. Measure each. Use `references/measure.md`.
3. Rank by CC descending.
4. **Report hotspots with numbers before any edit.** Name the function, the CC, and the band (or the project ceiling).
5. Refactor the worst first. One function at a time. Load `references/tactics.md` and apply the first tactic that fits.
6. Re-measure that function (and any extracted functions) before moving to the next hotspot.
7. Repeat until every touched function is in band, or you have asked about an exported signature you cannot change.

## Report

End with all three:

### Before / after

| Function | CC before | CC after |
|---|---|---|
| `name` | n | n |

Include extracted functions as new rows (CC before is `-` or blank).

### Extracted names

A list of the functions you introduced, each named for what it does.

### Verification

How behavior was checked:

- Tests that ran before and after, and the result.
- Or: no tests exist; you said so; you suggested adding some; the change stayed minimal.
