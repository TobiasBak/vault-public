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

## Bounded workload proof

Contain descendants in the kernel, and derive nested ownership from their actual cgroup rather than inherited environment. A detached child with `env: {}` can survive both process-group cleanup and owner-token discovery. Use group/tree discovery only as an explicitly weaker fallback; failed discovery must never prevent signalling the known group.

- Verify recursive `cgroup.events` population, not root `cgroup.procs`. A delegated root can have no direct processes while child groups remain live.
- Record the actual nested cgroup before launching a driver. A dead CLI PID is not enough to reclaim its lock; retain exclusion until the subtree is empty, including after cleanup errors.
- Read `memory.events.local` for the owning limit. Hierarchical events include independently enforced child OOMs and can falsely fail a successful enclosing test suite.
- Make cleanup verification part of the pass decision at both the execution and gate-result boundaries. Fail unverified cleanup locally. The only sound exception is an ephemeral CI runner VM, recorded and logged as the containment; execution failures still fail. The regression tests exercise the real gate consumer, not just the policy helper.

Host budgets and launcher policy remain owned by dotfiles' `nixos/hosts/pc/workloads.md`.

## Git fixtures inside hooks

Clear Git's repository-local environment before running a gate that creates temporary Git fixtures. Use `git rev-parse --local-env-vars` to identify the variables, including `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`. Changing a child command's working directory does not override them. Without this, a pre-commit test wrote fixture commits onto the real branch and replaced its index. Verify the real commit/push entrypoints, not just standalone test commands.

## Where agent verification time goes

Measure from session logs, receipts and PR timelines before tuning test runtime. In order-integration on 2026-10-02 to 04, the biggest losses weren't test execution:

- PRs sat ready overnight (10.2h) because owners lacked merge authority.
- A dead hosted workflow burned 19 × 30-minute Windows jobs.
- Native builds were discarded after every run, worktree and head move: 2.3h of compiling.
- Windows VM housekeeping (leftover guest state, a full disk, manual session setup) took 54 of a 98-minute qualification.
- The content-keyed native cache hashed the whole tracked tree, so any commit, even docs-only, changed every app's key and "cross-run reuse" never hit across commits. The CI scope selector likewise sent unclassified paths (skill YAML, docs images, root tests) to the full native matrix: 10 of 14 PRs. Key and scope must come from one per-app input set. The opposite failure, a key weaker than the source, let receipts test stale output; see [receipt binding](learning-from-feedback.md#evidence-gates-for-recurring-misses).
- Unbounded review/fix loops dominated the longest PRs; see [code review](code-review.md#reviewers).

A second ledger (2026-10-07 to 09, two long Opus-orchestrates-Sol runs, Claude and Pi session logs) found the model was already the bottleneck. Hours are summed across parallel children, so they measure cost, not wall clock:

| Run | Model | Tools | Turns | Avg turn |
|---|---:|---:|---:|---:|
| Service port to Rust, 363 children | 78.8h | 20.6h | 16,343 | 17s |
| Geometry engine, 122 children | 22.3h | 13.4h | 4,316 | 19s |

- Prompt cache hit 96%, so latency per turn is the model, not waste. At ~17s per turn, 30 tiny probes cost as much as a full test run. Turn count is the first lever: one command per question, batched reads, compact output.
- Medium effort was not faster than high per turn in the port (18.9s vs 17.2s).
- The parents waited blind: the port's parent spent 6.9h in `sleep 590` polling loops; the engine's slept 9 minutes on a gate that died at 35s. Wait on exit or notification, never on a timer.
- The one >10-minute test run was a Windows lane: 318s fresh-clone boot, 89s bundle upload, 244s nextest (188s of tests). Cold starts, not tests.
- The engine's gate (885 runs, avg 44s, worst 16 min) rebuilt a release per worktree and lost its caches to a reference key tied to the harness script hash and a deleted `target/`.

Measure with entry timestamps: in Pi, model time is the assistant entry's `timestamp` minus `message.timestamp` (request start), and tool time is the `toolResult` entry minus its calling assistant entry. In Claude Code logs, pair `tool_use` with `tool_result` by id.

Early review rounds mostly found real bugs. Fixes: delegate merge authority with a readiness bar, disable dead CI, keep build outputs in a content-keyed cross-run cache, carry receipts forward to a new head when its diff touches none of a job's inputs (order-integration `packages_ci.py --carry-forward`), run the full suite once on the final head, and give every platform run a clean, self-provisioning environment.

## Explain cache misses before rebuilding

Store the canonical input identity alongside its cache key and print field-level differences on a mismatch. Compare preparation and real build contexts without compiling before retrying an expensive build. Exclude execution-only state at the key owner rather than making one caller imitate another.

In one Windows build, preparation and CI selected identical Windows tools and sources but uv injected `UV_INTERNAL__PYTHONHOME` only in the project-venv context. The fix excluded the entire `UV_INTERNAL__` private launcher namespace while retaining the remaining build-setting allowlist. The fixed contexts matched compile-free; new fresh-clone, same-head and docs-only proofs then reused verified distributions with zero compilation and preserved producer provenance. Qualification can prove exact keyed bytes on a fresh OS without recompiling them; the owning release gate decides whether that is sufficient.

## Pruning tests

Keep tests that catch broken contracts or meaningful regressions across internal rewrites. Judge each assertion, not the test's category: a UI assertion may protect accessibility, a provider fixture may protect a protocol, and a registration test may be a discovery contract. Delete tests with no independent requirement, tests that mirror structure, and checks duplicated by cheaper equivalents. Coverage and count are not goals. The `review-test-quality` skill does this review.

## Refactor equivalence

Before a behaviour-preserving refactor merges, compare the base and the branch under the same test set. Record each durable output through pytest plugins (saved plans, HTTP exchanges, persisted session writes), then diff the outputs per test node and call index. Translate only the deliberate renames, removals and additions, and list each one; anything left over is unexplained. Add normalised accessibility snapshots and pixel diffs of the main screens.

Normalisation pitfalls, from order-integration M9:

- Under xdist, pytest temp paths gain `popen-gwN/`. Strip it, or compare runs that used the same worker mode.
- Random IDs inside strings (`execution-<hex8>`, upload hash directories, UUIDs) need stable placeholders. Map UUIDs in order of appearance.
- Evidence ZIP byte counts change with path lengths. Compare the unpacked, normalised JSON, not the size.
- Renamed test nodes must be mapped, or their records look like additions and removals.

### CSS migration proof

Retain the original production bundle before edits. If initial capture missed a state, serve that bundle against the same disposable fixture state, capture it, then restore the candidate; don't mock the page into looking equivalent.

CSS Modules migrations need checks beyond screenshots: runtime class queries can stop matching, custom tables can lose shared alignment rules, and removing an ancestor changes specificity in dirty/focused states. Audit styles-object references too: permissive module typings can accept nonexistent exports.

Sort computed-style property names before hashing; stylesheet edits can reorder custom-property enumeration without changing values. Reuse the same disposable fixture state and freeze clock/motion: regenerated IDs and dates can change text geometry. Normalizing the app origin does not repair that; renewing fixtures requires a fresh base capture.

Explain tiny pixel differences with evidence, not a blanket threshold. Repeat the unchanged baseline to test rasterization noise; inspect computed styles and geometry at the differing element. Wait for actual drawing content, not merely a default-sized canvas. A lazy render can otherwise look like a large CSS regression.

Finish shared frontend builds before registering and driving a fixture that fingerprints their assets. A valid readiness record becomes stale when another launcher rebuilds those assets. Compare recorded and current hashes before blaming a missing fingerprint or an ignored archive path; then build and launch serially with a fresh doctor-qualified record, never patch the registry to pass.

Identical protobuf map bytes can decode into different iteration orders in separate SDK processes. Trace transport and selection semantics before treating reordered lists as a refactor regression. For an equivalent visual state, filter and explicitly select the same named item through real UI controls; retain the original differing pair rather than adding product sorting for screenshots.

## Team adoption

For a team adopting AI in development, shorten the time from a change to trustworthy feedback. Measure confirmed defects found, defects missed, false alarms, investigation time, and maintenance cost, not generated code or test counts. The durable investments are representative cases, clear expectations, easy startup, isolated data, and inspectable results. A sensible first pilot runs an agent alongside the existing process on one troublesome workflow and compares findings and effort. Cheap judgment models like [Jev](jev.md) could later cluster failures or classify environment-vs-app issues, but they should never gate releases.
