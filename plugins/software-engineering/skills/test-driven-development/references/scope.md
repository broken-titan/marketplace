# Scope

| Situation | Rule |
|---|---|
| Feature or bugfix in production code | Failing test first |
| Spike / exploration | Throw the spike away. Start the cycle on a clean tree |
| Generated file | Out of scope |
| Config, flags, and other data the repo already treats as configuration | Out of scope |
| Test written after the production change | Delete the production change and write the failing test first if that test passed on the first run |

If a spike landed in the branch, delete it and start with a failing test.
