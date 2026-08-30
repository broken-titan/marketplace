# Skill folder tree

```
<skill-dir>/
  SKILL.md                 # trigger, map, opinions, gotchas, quality bar
  references/              # procedures, catalogs, checklists — load per step
  assets/                  # optional templates to copy
  scripts/                 # optional composition helpers
```

A plugin skill pack is `plugins/<group>/skills/<skill>/` with that shape under each skill. Shared playbooks for one group live under one skill’s `references/` and are pointed at by siblings.

Tell the agent **what exists**. It opens a reference when that step starts.

SKILL.md stays a lightweight guide. If a section is longer than the map needs, it belongs in `references/`.
