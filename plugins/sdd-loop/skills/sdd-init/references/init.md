# Init procedure

SKILL.md holds the trigger, write targets, and quality bar. Follow these steps in order.

## Bias

Anything with an obvious safe default is applied silently and listed in the final report with how to change it. Never ask the user to confirm a recommended default. Ask only the questions that need their judgment — scope confirmation, which commands to record, the product interview — and bundle related questions together.

This command writes only local repo files, with a single exception: creating a missing tracker project, and only with the user's explicit approval of that exact action (Step 2).

Host command names and hook wiring: `sdd-orchestrator/references/hosts.md`. Tracker adapters: `trackers.md` in this skill (or the orchestrator copy).

## Step 1: Inspect

- Confirm you are inside a git repository. If not, report and stop.
- Look for an existing `## SDD Scope` in `docs/sdd-scope.md` and in the repo's agent-instruction files (`AGENTS.md`, `CLAUDE.md`, or the same pattern). If one is found, show the current values and ask whether to update or leave them.

## Step 2: Resolve Scope

First, determine which tracker is in play. Default adapter is Jira (`tracker: jira`). Linear and GitHub Issues are overlays (`sdd-orchestrator/references/trackers.md`); do not enable them from silence.

For Jira: any connected server exposing Jira tools counts. If a working connector reaches the sites you need, use it and say nothing about a bundled MCP the current host was never shipped. Any mention of an unauthenticated server the user does not have reads as a to-do. A bundled host extra comes up in exactly one case: the user is on that host and no tracker tools work at all. Then direct them to authenticate it (or to enable their client's connector) and pause until reads succeed. On a host with no bundled MCP extra, do not nag about that file.

Then work through the following.

- If $ARGUMENTS provides site= and/or project=, use those.
- Otherwise, list the accessible sites/projects (read-only). Compare the repo name and remote URL against project names and keys, and propose the best match, clearly marked as a guess.
- Ask the user to confirm the site and project key(s). Do not proceed on a guess alone.
- Verify each confirmed project key actually exists (read-only lookup). For a key that does not exist, offer two paths and let the user pick.
  1. **Manual** — print exactly what to create in the tracker UI (name, key, recommended project type/template) and pause until they have done it.
  2. **Bootstrap**, only when a connected server exposes a project-creation tool. State the exact project to be created, get the user's explicit approval of that specific action, then execute it once using the sentinel mechanics — create `.sdd/` and `.sdd/.approve-external`, make the single call, delete the sentinel immediately. This is the only external write init may ever perform. On a permission error, report it plainly and fall back to the manual path. If no connected server has a project-creation tool, offer only the manual path. Never improvise one through raw API calls.
- A site that is missing entirely is out of scope. Report it and stop.
- Optionally ask for a Confluence space key for publishing specs and designs (Enter to skip). Only offer this when a connected site has Confluence write scopes.
- Ask spec storage if it is not obvious: `ticket-comment` (default; not committed), `confluence` (needs a space), or `in-repo` (markdown under the path they name). "Never committed" is the default until they say in-repo.
- Use the default gate label `ai-allowed` without asking. A team that uses a different label can volunteer it here, or edit the `label:` line later. Say so in the final report.

## Step 3: Detect Verification Commands

Inspect the repo to propose test, lint, and typecheck commands. Look at package.json scripts (npm/pnpm/yarn), Makefile targets, pyproject.toml/tox/pytest config, go.mod (`go test ./...`), *.sln or *.csproj (`dotnet test`), build.gradle, and Cargo.toml, with CI workflow files under .github/workflows as a cross-check.

Present the proposed commands. Offer to run each one once to prove it works before recording it. Record only what the user confirms, and mark anything unavailable as `none` rather than inventing a command.

## Step 4: Constitution and Optional Context Docs

The preflight requires exactly one document, the constitution. Everything else here is optional context that the stages use when it exists.

- **Constitution** (required by preflight) — the project's non-negotiable principles. Search `docs/sdd-constitution.md`, `CONSTITUTION.md`, or a principles section the user points to. If none exists, offer to draft a starter `docs/sdd-constitution.md` from a short interview (3-5 principles max) plus what the repo itself reveals. Commit the constitution to the repo. Never write it into `.sdd/`. If the user declines, record `constitution: none`. Later amendments use `sdd-constitution`.

- **Optional context docs** (never blocking; detect and record, but do not push the user to create them): product context (`docs/product*.md` or README purpose), structure (`ARCHITECTURE.md` or `docs/structure*.md`), coding guidelines (`CONTRIBUTING.md`, style guides under docs/).

List what was found and let the user confirm, trim, or add paths. Absence is fine.

## Step 5: Preview and Write

Show the exact sections to be added or updated.

```markdown
## SDD Scope
tracker: jira
spec-storage: ticket-comment
site: <confirmed site>
projects: <confirmed keys>
confluence-space: <space key, omit line if skipped>
label: <gate label, omit line to use the default ai-allowed>
constitution: <path, or none if explicitly declined>
product: <path, omit line if none found>
structure: <path, omit line if none found>
guidelines: <comma-separated paths, omit line if none found>

## Verification
test: <command or none>
lint: <command or none>
typecheck: <command or none>
```

`tracker:` defaults to `jira`. `spec-storage:` is `ticket-comment` (default), `confluence`, or `in-repo`. For `in-repo`, add `spec-path: docs/sdd/` (or the path they chose).

On the user's confirmation, write the sections to the repo's agent-instruction files (`AGENTS.md`, `CLAUDE.md`, or the same pattern — create a file that is missing; never overwrite unrelated existing content). If they asked for a dedicated file, also write `docs/sdd-scope.md` with the same sections — playbooks read that file first when it exists.

## Step 6: Housekeeping

Add `.sdd/` to .gitignore without asking. Create .gitignore if the repo has none, and skip silently if a pattern already covers it. If `spec-storage: in-repo`, do **not** gitignore the spec path.

## Step 7: Health Check (Automatic)

Run the sdd-doctor skill's checks now, in place. Do not tell the user to run it separately. Report its compact readiness summary, and if anything is WARN or FAIL, list the remedies before declaring init done.

Then finish by reporting the verdict, and that the sdd entry, batch, and `auto gates=<...>` now run in this repo with the pinned scope. Remind the user that only tickets assigned to them and carrying the gate label will ever be picked up, and that autonomous mode additionally requires an explicit `gates=` declaration on every invocation. Print a host-appropriate example from `sdd-orchestrator/references/hosts.md` rather than persisting any gate choice. Do not tell every host to run `/loop`.
