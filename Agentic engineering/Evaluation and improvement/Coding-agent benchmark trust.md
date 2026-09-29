# Coding-agent benchmark trust

A coding-agent result is evidence about a specific task set, revision, harness, access policy, model configuration, budget, and grader. It is not a context-free measure of coding ability. Define a result with enough scope to reproduce its opportunity to succeed or retrieve an answer. A patch can be technically plausible while the score is invalid because the task, runtime, or grader measured something else.

## Distinct trust failures

- **Training contamination:** tasks, gold patches, or close derivatives may have entered model training.
- **Runtime leakage:** the evaluated agent can recover answers from Git history, network access, package artifacts, tests, images, or other visible state.
- **Evaluator gaming:** the agent or harness exploits grader weaknesses without solving the intended engineering problem.
- **Invalid grading:** tests are strict in the wrong way, underspecified, misleading, flaky, or too weak to measure the task.
- **Selection saturation:** repeated public optimization against one benchmark makes its score less predictive even without direct memorization.

Do not collapse these into "poisoning." Record the demonstrated channel, benchmark version, split, harness conditions, and whether remediation was verified.

## Dated benchmark decisions

**SWE-Bench Pro, decision checked 2026-07-14:** discount public results as clean capability evidence when the harness exposes documented future Git history or upstream solutions, or when graders have not been revalidated. Public images were shown to contain answer-bearing history, and a later audit found substantial grader-quality problems. These are separate runtime-leakage and construct-validity failures. A sealed, regraded future revision may deserve different treatment, so the decision is scoped rather than permanent. Consequential references: [runtime leakage report](https://github.com/scaleapi/SWE-bench_Pro-os/issues/93) and [grader audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/).

**Datacurve DeepSWE v1.1, decision checked 2026-07-14:** give it more weight than affected SWE-Bench Pro results. Its tasks were purpose-authored, fixes were not merged upstream, base clones were shallow, and behavioral verifiers received authoring and review effort. This is stronger design, not proof of zero contamination or perfect grading. Treat a result as genuinely held out only when the model snapshot predates release and the runtime hides verifier and reference artifacts. See the [official repository](https://github.com/datacurve-ai/deep-swe).

## Evidence hierarchy

For consequential choices, prefer:

1. private or freshly authored tasks unavailable during model training and hidden from the agent;
2. repository-specific held-out tasks with behavioral checks, isolated worktrees, sealed network and history access, and independent grader review;
3. external original tasks with purpose-built verifiers, disclosed harnesses, and audited agent-visible environments;
4. public historical benchmarks after contamination, leakage, grading, and saturation review;
5. aggregate leaderboards or vendor summaries only as discovery signals.

[[Projects#SWE Benchmarking|SWE Benchmarking]] is the local controlled substrate, and [[Autoresearch]] governs repeated candidate selection.

Retain benchmark and task revision, model snapshot, reasoning effort, scaffold, token or turn budget, tools, network policy, Git-history state, execution image, verifier revision, pass rate, cost, latency, and exclusions. Prefer paired runs on identical tasks and cost per successful task. Inspect failed and passed trajectories for answer retrieval, grader loopholes, and unintended restrictions. Rebaseline after any model, harness, image, access, or evaluator change instead of comparing across protocol drift. A score earns trust from valid task construction, sealed runtime opportunity, behaviorally meaningful grading, and fresh confirmation, not from benchmark popularity.
