# Commands

| Command | Script |
|---------|--------|
| `/path-hubs` | `scripts/path-hubs.sh view` |
| `/path-hubs-auto-on` | `scripts/path-hubs.sh auto-on` |
| `/path-hubs-auto-off` | `scripts/path-hubs.sh auto-off` |
| `/path-hubs-link` | `scripts/path-hubs.sh link $ARGUMENTS` |
| `/path-hubs-unlink` | `scripts/path-hubs.sh unlink $ARGUMENTS` |

`view` prints the text tree and writes `view.html` under the state directory.

Link arguments: `--id`, `--hub`, `--kind chat|code|cowork`, `--title`, `--path`, `--cwd`, `--session-id`. A bare path or hub id is `--hub`.

Unlink arguments: `--id` or a bare item id.
