---
name: maintain-verification-skill
description: Check an existing project verification skill and feature map against source and live behavior, then fix proven drift. Use when verification instructions are stale, incomplete, or failing, or user-facing changes need to be reflected in the feature map.
---

# Maintain a verification skill

Keep the project's verification skill and feature map honest. Cover every mapped feature, both from source and in the running app; one convenient passing path is not coverage.

## Scope

Find the skill with launch, drive, and feature-map instructions, and ask if it's ambiguous. If none exists, use `$create-verification-skill`. Edit only that skill, its map, and helpers it owns; never product code. Use one writer and one live driver. For broad maps, delegate read-only source inspection by feature.

## Check against source

Reconcile missing, duplicate, and dead entries without producing a file inventory. For each feature, locate its implementation and entry points, spot likely drift, and write a short live recipe. Check recent user-facing changes for unmapped features, each backed by a concrete source path. Judge results against the intended product contract, not today's implementation. Recipes that share state can be combined as long as every feature and distinct entry point stays visibly covered.

## Live pass

Follow the skill's launch model: drive long-lived servers and UIs serially, and give short-lived CLIs fresh isolated sessions.
- Run doctor before the first drive and after any failure or surprise. A healthy process with a wedged UI needs a reset or relaunch.
- Capture each action, its result, and its side effects. Keep proof outside scratch and confirm it survives cleanup.
- Clean up failed attempts. Stop only what this run owns.
- When a prerequisite blocks a feature, record the route attempted and what was missing. A different passing path doesn't cover it.

## Triage

- **Map drift** (wrong instructions): correct against source and observed behavior.
- **Harness gap** (working behavior the helper can't drive): repair owned helpers and report others.
- **Product regression:** keep the expected result, capture evidence, and report it. Never redefine expected behavior to hide a bug.

Rerun every correction against the app.

## Verification and handoff

Exercise every mapped feature, rerun the affected ones after corrections, then tear down. Report one of:
- **Clean:** full coverage, no corrections.
- **Changed:** one coherent reviewable change set, with any product failures named.
- **Blocked:** the blocker and what was checked.

List covered features, blocked paths, drift, regressions, and artifact locations. Raw run notes stay in scratch.
