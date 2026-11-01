---
name: maintain-verification-skill
description: Check an existing project verification skill and test-derived feature map against source and live behavior, then fix proven drift. Use when verification instructions are stale, incomplete, or failing, or user-facing changes need to be reflected in the feature map.
---

# Maintain a verification skill

Keep the project's verification skill and test-derived feature map honest. Cover every mapped behavior and entry point, both from source and through the running product's published non-GUI interfaces; one convenient passing path is not coverage. Tobias allows no GUI tests, and `$theodore-kaczynski-nullifier` owns the test rules: a GUI test, GUI driver or screenshot comparison found here is drift to remove, with any rule it protected moved to a model or API test.

## Scope

Find the verification skill and the test runner's list of test names, which is the feature map; ask if ownership is ambiguous. If the workflow is missing, use `$create-verification-skill`. The map is never maintained as a README or feature-file tree. Edit only the skill, test names and owned verification helpers; never product code or expected results to hide a regression. Use one writer and one live driver.

## Check against source

Reconcile missing, duplicate and dead behaviors in the test list. For each behavior, locate its implementation and the test that proves it, check that each other entry point has its smoke run, and derive a short live recipe from the test's input and owned values. Check recent user-facing changes for untested features, each backed by a concrete source path. Judge results against the intended product contract, not today's implementation. A test copied to vary one input folds into a parameterized test that already has its setup.

## Live pass

Follow the skill's launch model: drive long-lived servers serially, and give short-lived CLIs fresh isolated sessions.
- Run doctor before the first drive and after any failure or surprise. A healthy process that stops answering needs a reset or relaunch.
- Capture each action, its result, and its side effects. Keep proof outside scratch and confirm it survives cleanup.
- Clean up failed attempts. Stop only what this run owns.
- When a prerequisite blocks a feature, record the route attempted and what was missing. A different passing path doesn't cover it.

## Triage

- **Map drift:** rename or add tests against the contract and observed behavior. Correct task instructions in the skill, not a parallel feature file.
- **Harness gap** (working behavior the helper can't drive): repair owned helpers and report others.
- **Product regression:** keep the expected result, trace the failing boundary, and report the evidence-backed cause or the exact diagnostic blocker. First rule out a wrong check or environment. Never redefine expected behavior to hide a bug.

Rerun every correction against the app.

## Verification and handoff

List the tests, exercise every mapped behavior and entry point through the published interface, rerun affected tests after corrections, then tear down. Report one of:
- **Clean:** full coverage, no corrections.
- **Changed:** one coherent reviewable change set, with any product failures named.
- **Blocked:** the blocker and what was checked.

List covered features, blocked paths, drift, regressions, and artifact locations. Raw run notes stay in scratch.
