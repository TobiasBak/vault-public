# Testing with agents

Tool-using agents can operate a running app, explore off the scripted path, notice semantically wrong results, and trace symptoms through APIs, logs, database state, and source. Deterministic tests repeat known paths cheaply. Use agents for ambiguity and investigation, and deterministic checks for stable invariants. Agent flexibility doesn't automatically mean better coverage or lower cost.

## Loop

1. Give the agent a realistic running environment, representative data, tools, and a clear authority boundary.
2. Define the workflow and observable success criteria, not every click.
3. Let it explore, keep artifacts, and investigate anomalies through the narrowest relevant surface.
4. Require a concrete reproduction with evidence: screenshots, traces, requests, logs, or resulting state.
5. Fix the responsible invariant (when authorized) and rerun both the minimized repro and the original scenario.
6. Promote stable discoveries into the cheapest durable protection: a deterministic test, schema, validator, lint rule, monitor, or clearer error.

An agent's claim of success is weak evidence. Checkers need authoritative state; a success message doesn't prove persistence. Derive expected behavior independently, or the agent validates its own misconception. Unclear expectations, unreliable resets, or inaccessible state produce false alarms.

## Verification tooling

Agents need two things: a **maintained control CLI** (launch, reset, act, inspect, collect traces, clean up while keeping evidence) and a **feature map** (what the product does, how users reach each feature, and what result shows it worked). Lauren Tan's Control Glass is the example. Keep both with the project's verification skill. Report blocked or incomplete runs explicitly; they are never passes. Build them with the `create-verification-skill` skill and keep them current with `maintain-verification-skill`.

**Fresh-agent handoff check:** give a new agent a representative report, the repo, and normal tools, with no prior investigation. Can it find the feature, reproduce, fix, and prove the fix without coaching? Where it struggles shows what to repair:

- couldn't find the feature: feature map or naming
- couldn't set up or inspect: tools
- needed repeated diagnostic coaching: skill
- made an architectural mistake: API or enforced boundary
- claimed unsupported success: checks

## Pruning tests

Keep tests that catch broken contracts or meaningful regressions across internal rewrites. Judge each assertion, not the test's category: a UI assertion may protect accessibility, a provider fixture may protect a protocol, and a registration test may be a discovery contract. Delete tests with no independent requirement, tests that mirror structure, and checks duplicated by cheaper equivalents. Coverage and count are not goals. The `review-test-quality` skill does this review.

## Refactor equivalence

Before a behaviour-preserving refactor merges, compare the base and the branch under the same test set. Record each durable output through pytest plugins (saved plans, HTTP exchanges, persisted session writes), then diff the outputs per test node and call index. Translate only the deliberate renames, removals and additions, and list each one; anything left over is unexplained. Add normalised accessibility snapshots and pixel diffs of the main screens.

Normalisation pitfalls, from order-integration M9:

- Under xdist, pytest temp paths gain `popen-gwN/`. Strip it, or compare runs that used the same worker mode.
- Random IDs inside strings (`execution-<hex8>`, upload hash directories, UUIDs) need stable placeholders. Map UUIDs in order of appearance.
- Evidence ZIP byte counts change with path lengths. Compare the unpacked, normalised JSON, not the size.
- Renamed test nodes must be mapped, or their records look like additions and removals.

## Team adoption

For a team adopting AI in development, shorten the time from a change to trustworthy feedback. Measure confirmed defects found, defects missed, false alarms, investigation time, and maintenance cost, not generated code or test counts. The durable investments are representative cases, clear expectations, easy startup, isolated data, and inspectable results. A sensible first pilot runs an agent alongside the existing process on one troublesome workflow and compares findings and effort. Cheap judgment models like [Jev](jev.md) could later cluster failures or classify environment-vs-app issues, but they should never gate releases.
