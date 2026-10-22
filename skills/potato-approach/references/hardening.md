# Hardening

Correct routine work shouldn't need the strongest model, repeated advice, or supervision.

## Enforce first, repair end to end

Tobias's rollout policy for a settled rule:

1. Implement the check over the full agreed scope, existing violations included. Confirm it accepts the supported pattern and rejects the forbidden one.
2. Wire it into the repository's real landing gate as a failing requirement and verify that the entrypoint propagates failure. Its failures are the repair inventory.
3. Repair the owning design and follow the effects through callers, tests, fixtures, and runtime behavior. Don't defer type coverage.
4. Continue until the gate passes and the behavior works. Passing by deleting required behavior is not a repair.

No migration baselines, per-file suppressions, warning-only modes, or narrowed scope. Fix a wrong check against the real contract; never weaken a correct one to fit the code. If you must stop, leave the gate enabled and failing and record the command, the remaining failures, and where to resume.

The failing gate lives in the repair workspace. Land the gate and its full repair together; a red gate on a shared default branch blocks every other agent's commits, and a baseline merged to get green breaks the policy.

## Put the decision in the design

Start from a real correction. Identify what the engineer decided, what it protects, and who owns that state. Don't turn an accident of one bad patch into a universal rule. Change types, data structures, APIs, or boundaries so the mistake can't be expressed. A written rule can't compensate for a design where the shortcut is easier.

**Every restriction needs an approved path.** A lint rule can reject an import, but it can't supply the missing API. For a recurring change, make these obvious in code: where it lives, which API performs it and owns its behavior, how valid states and failures are represented, allowed dependencies, the example to copy, and the check that proves the result. Put shared validation and effects behind the owning API, not in every caller. Use existing modules before inventing a framework.

*Example:* agents keep reading the file index inside UI components, which blocks the renderer. Provide `features/search/` with a shared contract (request, result, and failure types), a host service that owns index access, and a UI that calls the typed client. Add an import-graph check whose error points to the client. Copying the nearby example now preserves the boundary. Measure responsiveness separately.

## Static checks are executable

A static check is a program that exits nonzero on violation, with no agent interpreting it. AGENTS.md, skills, and review prompts are not checks, and a CI job named after a rule doesn't implement it.

- Use existing compilers, type checkers, linters, and dependency tools before writing custom checkers.
- Keep one rule implementation called by the real landing path, such as gah's configured check or Git hooks. Use CI only where the repository's policy already requires it.
- Failures name the rule, the location, and the supported fix.
- Demonstrate both rejection and acceptance through the real entrypoints, and state which ran. Don't claim a check blocks landing unless landing policy requires it.

## Prevent and recover

Prevent known mistake classes through the owning API and checks, but also make unforeseen failures visible, contained, and repairable:

- Represent incomplete and failed operations explicitly. Bound effects so one failed operation cannot silently corrupt unrelated work.
- Provide recovery at the effect boundary. Make retries safe or expose the state needed to decide whether to retry; a Git revert cannot undo an external write, deletion, or sent message.
- Preserve evidence needed for diagnosis and repair instead of hiding partial failure behind a success response or fallback.

## Preserve the reason for constraints

Keep the protected outcome and reason discoverable in the check's failure, behavioral oracle, or owning decision record. Reconsider the constraint when evidence shows its reason no longer holds; retire or replace obsolete mechanisms through an explicit policy decision. A failing check or inconvenient implementation is not evidence that a correct rule is obsolete. Keep an adopted rule enforced until that decision changes it.

## Cleanup

Bad examples spread. Find the owner before touching a workaround, and don't extend it because it's nearby. Move callers to the supported path and delete the alternatives within scope, leaving no second implementation to copy. Under enforce-first, the gate drives the migration.

**Comments:** recommend a repo-wide no-code-comments rule enforced by lint or CI. Comments make workarounds look approved. Remove the compromise itself, express the design through names, types, and checks, and preserve the reason in a check failure or case oracle. A one-off decision belongs in a `Why:` trailer in the landed commit; other rationale belongs in issues or PRs, not a docs tree. Change adopted rules deliberately, not through local exceptions.

Finish by verifying the affected behavior and that the check rejects the known bad pattern. Ask whether the next ordinary change can be made without inventing an exception.
