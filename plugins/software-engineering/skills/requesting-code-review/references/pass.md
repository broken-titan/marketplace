# Pass

Read the diff as if you will own the on-call for it.

## Look for

- **Correctness** – wrong branch, missing case, race, off-by-one, silent swallow
- **Missing tests** – a behavior change with no test that would fail without it
- **API contracts** – exported signatures, error cases, compatibility
- **Needless complexity** – extra types, extra layers, unused generality

## Finding

```
path/to/file.ext:LINE  severity  one-sentence claim
```

Severity:

| Level | Meaning |
|---|---|
| `blocker` | Wrong or unsafe if merged |
| `should` | Missing test, contract gap, or complexity that will cost the next edit |
| `nit` | Optional. Do not let comments about formatting or naming outnumber findings about correctness, tests, or contracts |

## Empty pass

If the read found nothing, say you read the whole diff and found nothing on correctness, tests, contracts, or extra complexity. If you would write a one-word approve, write findings or an explicit empty pass after a full read.
