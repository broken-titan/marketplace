---
name: tolkien-prose
description: >-
  Use when rewriting a journal, session log, or recap in high-fantasy walking
  prose, or when original-fiction / NPC-voice overlays are on.
---

A cadence coach for high-fantasy narrative English, with a local rewrite contract for journals and recaps.

**Mode switch.** Recap is the default when the source is a journal, session log, or recap rewrite. Original-fiction and NPC-voice overlays load only when the profile or the user says invention is allowed. Do not pick one mode and delete the other.

Inspect first. If the consuming repo has `docs/tolkien-prose-profile.md`, read it and honor it. Do not write a sample tenant into this plugin.

| File | When |
|---|---|
| `references/recap.md` | Recap / journal rewrite |
| `references/original.md` | Original-fiction or NPC-voice overlays |
| `references/questions.md` | Intake when mode / POV / tone is unknown |
| `references/technique.md` | Public cadence notes (not legendarium text) |
| `references/examples.md` | Tally vs walking pairs; mouth-card template |

## Mode

| Mode | When | Invention |
|------|------|-----------|
| **Recap** | Rewriting a journal, session log, or recap. Default for that job. | None. Fidelity contract. |
| **Original** | New fiction, or the profile/user says compose. | Allowed inside the profile. |
| **NPC-voice** | Spoken lines for named characters when the profile/mode says so. | Mouth-cards only; no plot add-ons unless original mode is also on. |

If the user did not name a mode and the source is notes of what already happened, use recap.

## Register

High-fantasy English is mostly plain. The antique feeling comes from grammar, cadence, and the sense that the world is older than the page. See `references/technique.md`. Do not paste or closely paraphrase still-protected letters, appendices, or narrative from a legendarium.

- Archaic English is terse in word choice, not in sentence length. Do not confuse economy of diction with three-word sentences.
- Archaism lives in word order and idiom, not costume vocabulary.
- Clauses often stand side by side, joined by "and."
- Landscape is seen from a standing place. Time has depth.
- People speak, but the tale is not a play. Most of a page should be walking narration.
- No two speakers share a mouth. If voices are not given, ask before writing much talk.

## Walking prose

When the source is notes, a game log, or a list of discoveries, do not promote every bullet to its own sentence. Fold related facts. Give a sentence its own line only when the thing in it turns the scene. Skip matter that does not act. Do not march "Then they went. Then they found."

Wrong (tally) and right (walking): `references/examples.md`.

## Three-pass

1. If recurring speakers lack cards and you cannot infer them, ask. Read notes as scenes.
2. Write walking narration first. Recap: no invented speech. Original / NPC: speech only where the overlay allows.
3. Cut contrast formulas, forecasts (unless the profile asked for a hook), prompt-questions, and talk that restates the narrator.
4. Read aloud. If more than about a third of a scene is quotation, cut lines (play-script cap).

## Forbidden (all modes)

- Contrast formulas ("It is not X. It is Y.", "not merely", "this is no ordinary").
- Unmotivated should and looking ahead unless the profile asked for a forecast.
- Play-script: a scene that is almost nothing but dialogue.
- Costume words and dummy-thee-ing the whole company.
- Telegram chronicle: one short sentence per bullet.

## Intake

When starting a consuming repo, or when mode / POV / tone is unknown, run `references/questions.md`. Write `docs/tolkien-prose-profile.md` only after the user confirms.

Context-only (do not load on recap unless asked): invented-language sheets, alliterative metre as a verse system, fairy-story theory essays, compressed annal style as a separate register.

## Gotchas

- Flattening recap and original into one mode invents speech in a journal rewrite.
- A profile written into this plugin is a sample tenant and vanishes on upgrade.
- Letter-and-appendix close paraphrase is not this skill's method.
- A page that could be replaced by the original bullet list is still a tally.

## Quality bar

- [ ] Mode named; recap default for journals
- [ ] Profile honored when present; written in the consuming repo
- [ ] Walking prose, not a tally
- [ ] No invented speech in recap
- [ ] Mouth-cards asked when NPC-voice needs them
