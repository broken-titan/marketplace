# Broken Titan plugin marketplace

Agent plugin marketplace for Claude Code, Codex, Cursor, and Grok from [Broken Titan](https://brokentitan.com).

Homepage: https://brokentitan.com

## Install

### Claude Code

```
/plugin marketplace add broken-titan/marketplace
/plugin install software-engineering@plugins
```

### Codex (CLI and ChatGPT desktop)

```
codex plugin marketplace add broken-titan/marketplace
codex plugin add software-engineering@plugins
```

Or open `/plugins` in Codex and install from the Broken Titan tab.

### Cursor

Teams and Enterprise: Dashboard → Plugins & MCPs → Add Marketplace → Import from Repo, paste `https://github.com/broken-titan/marketplace`.

Solo: copy a plugin folder from the repo into `~/.cursor/plugins/local/<name>`.

### Grok Build

```
grok plugin marketplace add broken-titan/marketplace
grok plugin install software-engineering --trust
```

Swap software-engineering for any plugin below. Pin a release with a tag, e.g. `--ref v3.0.1` in Codex.

## Plugins

- `business` — Write founder planning documents that stay on evidence.
- `engineering-strategy` — Write a living engineering strategy in the repo you are working in.
- `frontend-aesthetics` — Give a screen a specific look, not a generic layout.
- `lab` — Laboratory informatics for a LIMS, LIS, or ELN.
- `path-hubs` — Group Chat and Code sessions under one hub per git repo path.
- `sdd-loop` — Take a tracker ticket from intake through merge on a written spec.
- `skill-authoring` — Create a skill pack, or restructure one that already exists.
- `software-engineering` — Write and change source code.
- `solution-architecture` — Requirements and architecture for the current engagement.
- `usage-batteries` — Show always-visible Claude usage meters in the status line as horizontal phone batteries.
- `writing` — Draft in the user's voice, write errors they will see, and write setup checklists.

## License

MIT. See [LICENSE](LICENSE).

## Author

[Broken Titan](https://brokentitan.com) · [GitHub](https://github.com/broken-titan)
