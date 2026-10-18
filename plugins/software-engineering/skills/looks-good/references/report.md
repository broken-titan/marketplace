# Report

Print three buckets, then one verdict. A skill name appears in exactly one bucket.

```
run:
- <skill or own-check>: one-line result, with file:line if it found something

skipped as not applicable:
- <skill>: one-line reason from the change surface

disabled by user option:
- <skill or own-check>: the option text that disabled it
```

If a per-run option was unknown or malformed, print a warning before the buckets, then run the default applicable set.

## Own checks

| Check | Fail when |
|---|---|
| Diff hygiene | Unrelated hunks, generated noise, or a leftover debug edit |
| Naming/consistency | New names fight the names already in the touched files |
| Docs | User-facing or in-repo docs the change needs are missing or stale |
| User-facing polish | Visible copy, errors, or UI text is wrong or unfinished |
| Dead artifacts | Added files, exports, or config the change never uses |
| Reviewability | The diff cannot be reviewed without extra local context the report does not supply |

## Verdict

Pick exactly one:

| Verdict | When |
|---|---|
| `pass` | Applicable checks finished, and none need a change or a human |
| `fix before review` | A cited finding must be fixed in the tree before this is ready |
| `needs human review` | A cited finding needs a person (product call, secret, destructive, or unclear request) |

Cite `path/to/file.ext:LINE` on every finding that drives `fix before review` or `needs human review`.
