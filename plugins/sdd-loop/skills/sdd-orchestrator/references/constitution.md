# Amend the constitution

Goal – change `docs/sdd-constitution.md` (or the path in `constitution:`) **after** init, without re-running tracker setup, verification discovery, or doctor.

Invocable as `sdd-constitution` or `/sdd constitution`. Init Step 4 still drafts the first file. This playbook is the later amendment.

## Scope

Touch only the constitution file and, if the path changes, the `constitution:` line under `## SDD Scope`. Leave `site:`, `projects:`, `tracker:`, `spec-storage:`, and `## Verification` alone.

Refuse to bootstrap a missing tracker project. If there is no constitution yet, offer to draft one here (same 3–5 principles bar as init) or point at `sdd-init` when scope and verification are also missing.

## Process

1. Read the current constitution and `## SDD Scope`.
2. Ask what must now always hold, or what the project must now never do. Keep the file to a short principle list.
3. Preview the exact diff. Wait for confirmation.
4. Write the file. If `constitution:` was `none`, set it to the new path in `docs/sdd-scope.md` (when that file exists) and in `AGENTS.md` / `CLAUDE.md` — those lines only.
5. Record a one-line dated note in `.sdd/notes.md` that the constitution changed, so later tickets see it.

## Quality

- Principles stay few (about 3–5). A new rule that is really a ticket goes to intake, not here.
- Specs, designs, and code already in flight that would violate the new text become ATTENTION / open questions on those tickets; do not silently rewrite them in this pass.
