---
name: usage-batteries
description: >-
  Use when the user asks about Claude usage meters, status-line
  batteries, session or weekly limits, Weekly Fable, or how to
  toggle those meters and labels.
---

# Usage batteries

Horizontal phone batteries in Claude Code's status line. Fill is remaining (`100` minus used). One cell per meter that is on and has data.

## Files

| File | When |
|---|---|
| `references/meters.md` | Remaining math, colors, which window maps to S/W/F, missing Fable data |
| `references/toggles.md` | On/off commands, sentinel files, install/uninstall |
| Plugin extra `scripts/statusline.sh` | Status-line renderer. Reads JSON on stdin. |

## Hard rules

1. Report remaining as `100` minus `used_percentage`, clamped to 0–100; do not show used as the fill.
2. Draw batteries horizontally with the nub on the right and fill left to right; never use a vertical or upright battery.
3. Show only meters that are toggled on and have a usage window in the payload or cache.
4. Persist each meter and the label toggle with the plugin's on/off scripts; do not hand-edit a second settings scheme.
5. If Claude Code has no Chat/Code chrome API, keep using `statusLine` and say that is the supported surface.

## Easy mistakes

- Treating `used_percentage` as the battery fill.
- Drawing `🔋` or any upright cell.
- Inventing a Fable percent when the payload has no Fable window.
- Overwriting a `statusLine` the user already set, unless they asked to force install.

## Quality standards

- [ ] Remaining equals `100` minus used
- [ ] Cluster matches the meters that are on and present
- [ ] Labels are S/W/F when labels are on, and omitted when labels are off
- [ ] Toggles go through the plugin scripts
