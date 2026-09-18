# Tactics

Walk the code you just made green, or the overbuilt region the user named. Preserve behavior. Do not chase a complexity score. The hard rules stay in SKILL.md.

## 1. Delete

Remove unused functions, unused branches, unused parameters, and dead feature flags in the touched region.

## 2. Flatten

Collapse needless wrappers and pass-through modules. If a file or type exists only to forward a call, remove the hop.

## 3. Inline

One caller: put the body at the call site. Keep a name at the call site if it still helps. Stop; do not redesign the module.

## 4. Prefer what already exists

Try, in order: language-native, framework already in the repo, library APIs already on the dependency list. Custom code is last. A few extra lines of a native or existing call still win. Do not add a package to dodge a short function.

## 5. Extract

Only when the rule is ours (the stdlib does not already make it clear) or a second caller exists now. Otherwise call the native thing by its real name.
