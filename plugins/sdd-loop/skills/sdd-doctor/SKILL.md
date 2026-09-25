---
name: sdd-doctor
description: >-
  Use when checking whether the spec-driven loop is ready in this repo.
  Read-only health check; changes nothing.
disable-model-invocation: true
---

Read-only health check. Host overlay: `sdd-orchestrator/references/hosts.md`.

## Checks

1. **Connector.** PASS if at least one authenticated tracker connector can list sites. FAIL only when no tracker tools work. Mention a bundled MCP only when that host shipped one and nothing else works. Never nag about a missing `.mcp.json` on a host that was never shipped one.
2. **Identity.** The account assignee-current-user scopes to.
3. **Gate query.** Label from `## SDD Scope` `label:`, else `ai-allowed`. Zero eligible tickets is PASS. An error is FAIL.
4. **Repo config.** Find `## SDD Scope` and `## Verification` in `docs/sdd-scope.md`, then agent-instruction files (`AGENTS.md`, `CLAUDE.md`, or similar). Missing sections: interactive works, batch refuses; remedy is sdd-init. Run the orchestrator's preflight read-only. Do not run verification commands.
5. **Tooling.** `git` + worktrees; POSIX shell. Fence vs policy-only per `hosts.md`. Probe `echo sdd-guard-probe git push` only when this host can fence and `.sdd/` exists.
6. **Spec storage (optional).** Confluence access only when configured. Absent config is INFO.
7. **Autonomy state.** Stale `autonomy.json` is WARN. Leftover `.approve-external` is FAIL.

## Report

Each check PASS, WARN, FAIL, or POLICY-ONLY plus a one-line remedy. Verdict: ready for interactive use, ready for batch, policy-only on this host, or the specific blockers. Take no corrective action.

## Easy mistakes

- A missing constitution is WARN (interactive) / refuse-without-override (batch/auto), not a silent pass.
- Policy-only hosts are not FAIL for a missing mechanical fence.
- Doctor must not run the green baseline; the orchestrator does that at run start.

## Quality bar

- [ ] Read-only
- [ ] Instruction-file pattern, not one vendor file
- [ ] Bundled MCP mentioned only on the host that shipped it
- [ ] Compact verdict with remedies
