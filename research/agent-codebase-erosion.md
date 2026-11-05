# Do agent-maintained codebases inevitably degrade?

Status: pre-registered, no runs yet (2026-11-05).

recheck-after: 2027-02-05

## Abstract

Agents build codebases one task at a time, and every task rewards the smallest change that passes. This paper claims that agent use therefore degrades a codebase continuously, whatever the environment around the agent. It tests that claim by putting the strongest mechanical locks we can build around agents working through a chain of changes. If any lock flattens the decline, degradation is an environment problem with an engineering fix. If none does, the claim stands, and agent work needs a different shape than one feature at a time.

## Thesis

Agent use continuously degrades a codebase, whatever the environment.

Each agent sees only its own task, so the smallest plausible patch wins every time: a parallel path, a duplicated rule, a branch bolted onto a big function. That is [patch accretion](../agents/agent-native-codebases.md#patch-accretion-is-the-main-failure). Each patch is locally fine. Together they make every later change slower and more error-prone, and a benchmark that scores one task at a time can't see the cost.

The thesis is refuted if any intervention clearly flattens the per-change quality slope without lowering correctness. Telling the agent to write clean code is not enough: in [SlopCodeBench](https://arxiv.org/abs/2603.24755) it made code start cleaner and left the slope unchanged.

## Hypotheses

Each one tries to refute the thesis and names the result that would refute the hypothesis itself.

1. **Gates lower the level.** Any hard gate on erosion or verbosity lowers starting values at least as much as an anti-slop prompt. Refuted if gated runs start no cleaner than prompted ones.
2. **Deletion gates flatten the slope.** Gates on unused exports, files and dependencies (knip, cargo-machete) and on clones (jscpd) force the old path out when a new one lands, so they attack accretion itself. Predicted: a visibly flatter slope than baseline. Refuted if the slope matches the prompt arm.
3. **Complexity caps get gamed.** A per-function complexity cap improves the erosion number by splitting functions into helpers that still carry the same branching and coupling. Predicted: erosion drops but total complexity, clone count and later pass rate don't improve. Refuted if transcripts show real consolidation rather than reshuffling.
4. **Boundary locks attack the cause.** Erosion is a proxy for blurred ownership. Import boundaries (dependency-cruiser, import-linter, workspace dependency rules) should help most where later changes cross modules. Refuted if they show no effect there.
5. **Static gates can't see semantic duplication.** Two differently shaped implementations of one rule, or a feature in the wrong owner, pass every lint. A periodic consolidation pass, proved behavior-preserving by [refactor equivalence](../agents/testing-with-agents.md), flattens what gates leave. Refuted if gated-only runs already match it.
6. **An editable gate decays.** An agent that can change lint config or add suppressions loosens the gate under pressure. The [zero-comment rule](../skills/theodore-kaczynski-nullifier/references/enforcement.md) already blocks comment-form suppressions such as `eslint-disable`, `noqa`, `type: ignore` and `@ts-expect-error`; Rust's `#[allow]`, per-file overrides and config edits remain. Predicted: denying agent writes to gate config in harness permissions removes those bypasses. Check transcripts for attempts.

## Method

The testbed is [SlopCodeBench](https://github.com/SprocketLab/slop-code-bench), where an agent extends its own solution across checkpoints as requirements change. Its two quality metrics can be computed by a check, so they can serve as gates:

- **Erosion:** the share of complexity mass, cyclomatic complexity times the square root of source lines, held by callables whose complexity exceeds 10.
- **Verbosity:** lines flagged by 137 ast-grep rules or found in structural clones, divided by total lines.

Follow the [fast-loop funnel](../agents/autoresearch.md#fast-loops-first-tobias-2026-10-12):

1. Precheck from published trajectories that the chosen problems erode in the baseline arm, and that later checkpoints cross modules for hypothesis 4.
2. Scout two or three problems, one model, one or two runs per arm: plain, anti-slop prompt, and each gate. A gate arm must pass its gate before the checkpoint counts, with the agent allowed to iterate.
3. Read transcripts for how the agent satisfied the gate: real consolidation, reshuffling or bypass attempts. Report quality slope, strict pass rate and cost as separate numbers.
4. Replicate only an arm whose slope visibly differs.

Gaming threatens validity: a gate scored by the metric it enforces can look like a win while the code gets no better. Judge each gated arm also on metrics it does not enforce, and on whether later checkpoints get easier to pass.

Runs are real compute. Run them on an isolated or cloud machine, not the shared workstation. Harness code and run artifacts live in their own repository.

## Results

None yet.

## Open questions

- **Ratchets.** The [rollout rules](../skills/theodore-kaczynski-nullifier/references/enforcement.md#rollout) forbid baselines. That fits rule violations, which can reach zero. Continuous measures such as duplication share or total complexity have no zero state; they need a fixed threshold or a ratchet that may only improve. A ratchet is not a grandfathered violation list, but the current wording reads as banning it. Settle this with the scout results for hypotheses 2 and 3.

## References

- [SlopCodeBench paper](https://arxiv.org/abs/2603.24755): agents extend their own solutions across 196 checkpoints in 36 problems as requirements change. Quality prompts lowered starting erosion and verbosity but not their rise per checkpoint; version 2, read 2026-11-05.
- [SlopCodeBench code](https://github.com/SprocketLab/slop-code-bench): the harness, problems and metric implementations this paper's runs build on.
- [Radon](https://radon.readthedocs.io): Python cyclomatic complexity tool. Its bounds supply the erosion metric's threshold of 10.
- [ast-grep](https://ast-grep.github.io): structural code search and lint by syntax-tree pattern. It supplies the verbosity metric's flagged lines.
- [knip](https://knip.dev): finds unused files, exports and dependencies in JavaScript and TypeScript projects. Deletion gate for hypothesis 2.
- [cargo-machete](https://github.com/bnjbvr/cargo-machete): finds unused Cargo dependencies. Deletion gate for Rust.
- [jscpd](https://github.com/kucherenko/jscpd): copy-paste detector across many languages. Clone gate for hypothesis 2.
- [dependency-cruiser](https://github.com/sverweij/dependency-cruiser): validates JavaScript and TypeScript imports against declared rules. Boundary lock for hypothesis 4.
- [import-linter](https://github.com/seddonym/import-linter): enforces import contracts between Python modules. Boundary lock for hypothesis 4, and the fit for SlopCodeBench's Python problems.
