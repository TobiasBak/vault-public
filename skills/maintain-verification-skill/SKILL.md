---
name: maintain-verification-skill
description: Check an existing project verification skill and case-derived feature map against source and live behavior, then fix proven drift. Use when verification instructions are stale, incomplete, or failing, or user-facing changes need to be reflected in the feature map.
---

# Maintain a verification skill

Keep the project's verification skill, case records and generated feature map honest. Cover every mapped behavior and entry point, both from source and in the running app; one convenient passing path is not coverage.

## Scope

Find the verification skill, authoritative case records and product CLI's `map [area]`; ask if ownership is ambiguous. If the workflow is missing, use `$create-verification-skill`. The map is generated from case records, never maintained as a README or feature-file tree. Edit only the skill, case navigation metadata and owned verification helpers or map generator; never product code or expected results to hide a regression. Use one writer and one live driver. For broad maps, delegate read-only source inspection by behavior.

## Check against source

Reconcile missing, duplicate and dead behavior-and-entry-point pairs in the case records, then regenerate the map; never edit generated output. For each behavior, locate its implementation and covering case, inspect every entry point, and derive a short live recipe from the case input and expected effects. Check recent user-facing changes for unmapped features, each backed by a concrete source path. Judge results against the intended product contract, not today's implementation. Combine steps within one scenario when every behavior and entry point stays visibly covered; separate cases keep independent mutable starting state.

## Live pass

Follow the skill's launch model: drive long-lived servers and UIs serially, and give short-lived CLIs fresh isolated sessions.
- Run doctor before the first drive and after any failure or surprise. A healthy process with a wedged UI needs a reset or relaunch.
- Capture each action, its result, and its side effects. Keep proof outside scratch and confirm it survives cleanup.
- Clean up failed attempts. Stop only what this run owns.
- When a prerequisite blocks a feature, record the route attempted and what was missing. A different passing path doesn't cover it.

## Triage

- **Map drift:** correct the authoritative case metadata or map generator against the contract and observed behavior, then regenerate. Correct task instructions in the skill, not a parallel feature file.
- **Harness gap** (working behavior the helper can't drive): repair owned helpers and report others.
- **Product regression:** keep the expected result, trace the failing boundary, and report the evidence-backed cause or the exact diagnostic blocker. First rule out a wrong check or environment. Never redefine expected behavior to hide a bug.

Rerun every correction against the app.

## Verification and handoff

Regenerate the map, exercise every mapped behavior and entry point through its covering case, rerun affected cases after corrections, then tear down. Report one of:
- **Clean:** full coverage, no corrections.
- **Changed:** one coherent reviewable change set, with any product failures named.
- **Blocked:** the blocker and what was checked.

List covered features, blocked paths, drift, regressions, and artifact locations. Raw run notes stay in scratch.
