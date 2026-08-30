# Doctor pass

Work file by file. Do not invent findings.

## 1. Over-constraint and conflicts

Find pairs that cannot both be true (e.g. “leave docs as appropriate” vs “never add comments”). Keep the rule the **product** needs. Drop the other or narrow it to the surface it actually governs.

Absolute always/never stays only for safety, compliance, destructive ops, or a named product opinion.

## 2. Progressive disclosure

If SKILL.md is a procedure, split: keep the map and the trigger; move steps to `references/<step>.md`. Point at those files once.

## 3. Trigger

Rewrite `description` per `skill-builder/references/trigger.md`.

## 4. The obvious

Delete explanations of git, markdown, or “read the file before editing” unless this product breaks that default.

## 5. Repeats

One home per instruction. SKILL.md xor a reference.

## 6. Galleries → contracts

Replace long example lists with inputs / enums / outputs. Keep one example only when the contract is still ambiguous.

## 7. Gotchas

Add a **Gotchas** section (or grow it) from failures already visible in the skill, its tests, or the repo. Do not invent lore.

## 8. Pack shape

A plugin with several skills stays several skills. Do not merge them into one markdown file. Do not add a bibliography.
