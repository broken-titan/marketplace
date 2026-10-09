---
name: frontend-aesthetics
description: >-
  Use when you build or restyle a user interface. Choose a concrete
  visual direction and ship production-looking screens instead of a
  generic assistant layout.
---

# Frontend Aesthetics

Load this when markup, styles, or components that a person will see are in scope. It is not an architecture pack and it is not an always-on stance.

Before the first styled surface, name the direction in one sentence: who the screen is for, what feeling it should carry, and one visual constraint you will keep (type family, palette, density, or motion). Then keep that constraint through the change.

## Direction

Pick a look that belongs to this product. Do not start from a centered hero, a three-card row, and a pale gray page with a single accent.

Choose type the way a designer would for this audience. Pair one display face with one readable body face, or commit to a single family with a real weight range. Do not reach for the same sans the last generated dashboard used.

Build a short palette: one surface, one ink, one accent, and one quiet line. Repeat those four. Do not sprinkle extra hues to make the page feel finished.

Set a spacing rhythm and a type scale, then stick to them. Uneven padding and one-off font sizes read as unfinished even when the colors are fine.

## Production

Ship the states a real user hits. Empty, loading, error, overflow, and a dense happy path belong in the first pass, not as a later polish ticket.

Hierarchy should be obvious at a glance: one primary action, secondary actions that recede, and body copy that does not compete with the title.

If the product already has tokens, components, or a CSS file, extend that system. Do not drop in a second button style because a fresh file felt easier.

Motion, if any, should be short and tied to a change the user caused. Do not animate every card on load.

## Stop

A screen fails this skill when a stranger could swap the logo and believe it was any other generated app. If that is true, change type, palette, or density before you add more components.
