---
name: plugin-semver
description: >-
  Use when you change a published plugin or the marketplace catalog
  and need to pick a plugin or catalog version bump.
---

# Plugin semver

Bump the plugin you changed from the surface you added or broke, not from how large the diff looks.

A catalog bump is not a plugin bump. A new plugin starts at 1.0.0.

## Plugin

1. MAJOR when you remove or rename a published skill or hook, or change the plugin install name.
2. MINOR when you add a command, hook, on/off toggle, skill, or a first-party schema or renderer under a published skill.
3. PATCH when you only change copy, docs, or a bugfix with no new surface.

## Catalog

1. MAJOR when you remove a published plugin, change a slug, drop a published skill, or break host catalog layout.
2. MINOR when you add a published plugin, skill, command, hook, toggle, or a first-party schema or renderer under a published skill.
3. PATCH when you only fix listing text or the compiler and add no published surface.

`./build --check` rejects an authored PATCH when inference is MINOR, for the catalog and for each changed plugin.
