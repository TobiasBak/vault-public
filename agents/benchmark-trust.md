# Coding-agent benchmark trust

A score is evidence about a specific task set, revision, harness, access policy, model config, budget, and grader. It is not context-free coding ability.

## Distinct failures

Don't lump these together as "poisoning":

- **Training contamination:** tasks or gold patches were in the training data.
- **Runtime leakage:** answers recoverable from Git history, network, packages, tests, or images.
- **Evaluator gaming:** exploiting grader weaknesses.
- **Invalid grading:** tests that are wrong, underspecified, flaky, or too weak.
- **Selection saturation:** public over-optimization erodes predictive value.

## Current calls (2026-07-14)

- **SWE-Bench Pro:** discount public results. Images contained answer-bearing future history ([report](https://github.com/scaleapi/SWE-bench_Pro-os/issues/93)), and an audit found substantial grader problems ([audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)). A sealed, regraded revision would deserve a fresh look.
- **Datacurve DeepSWE v1.1** ([repo](https://github.com/datacurve-ai/deep-swe)): weight it above SWE-Bench Pro. Tasks are purpose-authored, fixes are unmerged upstream, clones are shallow, and verifiers are reviewed. Count a result as held out only if the model snapshot predates release and the runtime hides verifiers.

## Evidence ranking

1. Private or freshly authored hidden tasks.
2. Repo-specific held-out tasks with behavioral checks, isolated worktrees, sealed network and history, and reviewed graders. SWE Benchmarking is the local version.
3. External original tasks with purpose-built verifiers and audited environments.
4. Public historical benchmarks, after leakage and grading review.
5. Leaderboards and vendor summaries, for discovery only.

Record benchmark and task revision, model snapshot, effort, scaffold, budget, tools, network policy, Git-history state, image, verifier revision, pass rate, cost, latency, and exclusions. Prefer paired runs and cost per successful task. Inspect both passing and failing trajectories for answer retrieval and grader loopholes. Rebaseline after any model, harness, image, access, or evaluator change.

## Harness measurement traps

- Gate phases by stable run identity, not launcher PID. `uv run` can spawn a Python child whose PID names the readiness marker. A controller tested only with direct Python invocation can silently stall under the real command.
- Record agent latency separately from coordination, validation, and judging. Hold post-run validators and judges until measured agents finish; report coordinator stalls as batch delay rather than model slowness. Afterward, run independent grades concurrently unless an observed host or account constraint requires a cap.
- Separate streaming liveness from artifact retention. Valid updates omitted from logs must still refresh inactivity detection.
- Count native compaction usage and inspect nested programmatic tool events. Assistant-message accounting alone misses compaction cost and can hide nested agent invocations.
