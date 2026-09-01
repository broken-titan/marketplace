# Setup and memory

If the skill needs user-specific config (site, profile, voice, tenant):

1. Ask once.
2. Write it into the **consuming repo** (`docs/…`, or the repo’s agent-instruction file pattern: `AGENTS.md` / `CLAUDE.md` / similar).
3. Leave the marketplace skill directory empty of tenants.

Repeated-workflow state (queues, ledgers, last-run logs) lives in the consuming repo (e.g. `.sdd/`) or a stable plugin-data path the host keeps across upgrades. Do not store it next to SKILL.md in the pack — those files vanish or reset when the skill updates.
