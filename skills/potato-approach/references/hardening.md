# Hardening

Correct routine work shouldn't need the strongest model, repeated advice, or supervision.

## Enforce first, repair end to end

Tobias's rollout policy for a settled rule:

1. Implement the check over the full agreed scope, existing violations included. Confirm it accepts the supported pattern and rejects the forbidden one.
2. Wire it into pre-commit and CI as a failing requirement and verify that both propagate failure. Its failures are the repair inventory.
3. Repair the owning design and follow the effects through callers, tests, fixtures, and runtime behavior. Don't defer type coverage.
4. Continue until the gate passes and the behavior works. Passing by deleting required behavior is not a repair.

No migration baselines, per-file suppressions, warning-only modes, or narrowed scope. Fix a wrong check against the real contract; never weaken a correct one to fit the code. If you must stop, leave the gate enabled and failing and record the command, the remaining failures, and where to resume.

## Put the decision in the design

Start from a real correction. Identify what the engineer decided, what it protects, and who owns that state. Don't turn an accident of one bad patch into a universal rule. Change types, data structures, APIs, or boundaries so the mistake can't be expressed. A written rule can't compensate for a design where the shortcut is easier.

**Every restriction needs an approved path.** A lint rule can reject an import, but it can't supply the missing API. For a recurring change, make these obvious in code: where it lives, which API performs it and owns its behavior, how valid states and failures are represented, allowed dependencies, the example to copy, and the check that proves the result. Put shared validation and effects behind the owning API, not in every caller. Use existing modules before inventing a framework.

*Example:* agents keep reading the file index inside UI components, which blocks the renderer. Provide `features/search/` with a shared contract (request, result, and failure types), a host service that owns index access, and a UI that calls the typed client. Add an import-graph check whose error points to the client. Copying the nearby example now preserves the boundary. Measure responsiveness separately.

## Static checks are executable

A static check is a program that exits nonzero on violation, with no agent interpreting it. AGENTS.md, skills, and review prompts are not checks, and a CI job named after a rule doesn't implement it.

- Use existing compilers, type checkers, linters, and dependency tools before writing custom checkers.
- Keep one rule implementation, run by both the installed pre-commit hook (installed during normal setup) and CI (because hooks can be skipped).
- Failures name the rule, the location, and the supported fix.
- Demonstrate both rejection and acceptance through the real entrypoints. If CI hasn't run, say so. Don't claim a check blocks merges unless merge policy requires it.

## Cleanup

Bad examples spread. Find the owner before touching a workaround, and don't extend it because it's nearby. Move callers to the supported path and delete the alternatives within scope, leaving no second implementation to copy. Under enforce-first, the gate drives the migration.

**Comments:** recommend a repo-wide no-code-comments rule enforced by lint or CI. Comments make workarounds look approved. Remove the compromise itself, express the design through names, types, and checks, and keep the rationale in owning docs. Change adopted rules deliberately, not through local exceptions.

Finish by verifying the affected behavior and that the check rejects the known bad pattern. Ask whether the next ordinary change can be made without inventing an exception.
