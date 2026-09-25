# Public ancestry (cite; do not paste)

These are the public sources this skill's templates follow. Link them. Do not copy chapters, tables, or long quotations into an ADR or into this plugin.

## Documenting architecture decisions (Nygard)

Michael Nygard, 15 November 2011. The short-form ADR: title, status, context, decision, consequences.

https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions

Status vocabulary in that note (proposed / accepted / deprecated / superseded) is the core this skill keeps. **Rejected** is added so a considered-and-declined option can close.

## MADR

Markdown Any Decision Records. Field set this skill uses: status, date, deciders, context, decision drivers, considered options, decision outcome, consequences (good and bad), confirmation, more information.

https://adr.github.io/madr/

Use the current public template as a *shape*. Do not vendor a release tarball into the repo.

## Y-statement

One-sentence decision form used in architecture practice:

In the context of \<context\>, facing \<force\>, we decided for \<option\> to achieve \<quality\>, accepting \<downside\>.

Public write-ups: the MADR project’s Y-statement notes and architecture-decision records discussions that quote that shape. Keep the generated Y-statement to one paragraph.

## What to leave out

Paywalled handbooks, TOGAF ADM, and arc42 section templates stay out of this skill. Catalog ADR *patterns* for an engagement SAD remain in the sibling SAD `references/adrs.md`.
