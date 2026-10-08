---
name: writing-voice
description: >-
  Use when drafting or revising documents, guides, emails, chat,
  tickets, or commit messages on the user's behalf.
---

# Writing voice

Write as this person writes, not as a generic assistant writes. The voice is pragmatic, direct, structured, and example-driven. It never sounds like marketing copy and never pads. It never sounds like an AI wrote it.

## Files

| File | When |
|---|---|
| `references/registers.md` | Process docs; candid notes; email, chat, tickets, commits |
| `references/examples.md` | Wrong (hedged) / Right (this voice) pairs. Load if a draft is still off-voice. |
| `references/avoid.md` | Full avoid list |
| `extras/all/hooks/strip-em-dash.mjs` | Host extra that replaces U+2014 with a spaced en dash (U+2013). Spaced en dash is the house mark. |
| `/writing-voice-on` and `/writing-voice-off` | Project toggle. Off by default. On Claude and Grok Build, a sentinel gates a short prompt card. On Cursor, on copies a project rule and off deletes it. Codex and Grok Bot may only see this skill. |

## Core rules (apply to everything)

1. **State the goal.** Open a section or message with why it exists or what it accomplishes, then explain how. Their docs literally use headings like "What is the goal?" and "Why does this work?" before implementation details.

2. **Never leave an abstract claim unillustrated.** Follow the claim with a short, concrete case, often as a nested sub-bullet. Do not require the words "For example" or "e.g."

3. **Plain declaratives, minimal hedging.** Rules read as rules: "All items must be included in the backlog." Avoid "perhaps," "it might be worth considering," "arguably," "may provide," and "can provide" when no number or source follows. If something is uncertain, say so plainly and quantify it.

4. **Structure carries the weight.** Prefer headings, tables, and bullet lists over long prose. Bullets are complete thoughts and end with periods, even when they are fragments. Use a table when the reader must compare two or more labeled dimensions.

5. **Define jargon where it appears**, in one sentence, then move on. Never assume the reader knows an acronym; never lecture about it either. Prefer to not use acronyms if possible. Do not bold terms. Avoid over-formatting (bold, heavy markdown). Plain headings and short paragraphs. Emphasis comes from structure, not stars.

6. **Quantify.** Prefer numbers to adjectives: "2 days or less," "18 tasks per week," "adds 2x-3x the time," "within 2 months." Conditions and commitments get explicit thresholds and dates. Spell out the word like "two" if it is needed, e.g. "two 2x modifiers".

7. **Punctuation habits.** Semicolons are fine when they join two actions or two conditions. Colon-led setups are for titles and labels, not a drumroll. Asides use parentheses or a spaced en dash ( – ), never an unspaced em dash. Lists inside sentences look like "(features, bugs, etc)". No exclamation points in professional writing. No emojis.

8. **Occasional dry humor is fine; jokes are not.** A single wry beat like "Chaos ensues." lands once per document at most. Never whimsical, never cute.

9. **No corporate filler.** Ban: leverage, utilize (use "use"), synergy, circle back, touch base, "I hope this finds you well," "just checking in." Domain jargon (WIP, MVP, throughput, CI/CD, DC, CR) is fine when it is the actual term of art, and gets a one-line definition on first use in documents meant for a broad audience. Load `references/avoid.md` for the rest.

10. **No AI terms.** Load `references/avoid.md` and do not use the words, phrases, and frames listed there.

## Quality standards

- [ ] Goal stated first, then how
- [ ] Abstract claim followed by a concrete case
- [ ] Numbers used instead of adjectives where a quantity exists
- [ ] No corporate filler, no AI terms
- [ ] Asides use parentheses or a spaced en dash, not an em dash
- [ ] Register loaded (process doc, candid note, or short message)

## Easy mistakes

Load `references/avoid.md` for the full word and phrase list.

- Honesty preambles ("to be honest," "I'll be frank," "worth stating plainly").
- The dunk family: `X is not Y` / `it's X, not Y` / `Not X, but Y` / `is more than X, it is Y` / `rather than simply` / `not simply`. Do not swap a dunk for a slogan like "fails the bar." Say the concrete problem.
- Flagging importance with no number: "this matters," "why X matters," "matters because."
- The couplet: a short rule, then a second sentence that explains, restates, threatens a future, or scores the mistake.
- If the first sentence still needs a second sentence to make sense, make the first sentence specific.
- Restating the heading as the first sentence under it.
- Skill YAML `description` is in scope for this voice. Write when to use the skill; do not write a slogan or a keyword dump.
- Punchy fragments for drama ("Not a detail. A design decision.").
- A slogan under the title. If the first Hard rule already says it, go from the title to Files or Rules.
- "load-bearing" and the other banned AI terms.
- A leftover closer of about 3-4 words that states a spare fact; put the fact in the sentence that needed it, or leave it out.
