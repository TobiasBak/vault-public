# Codebase erosion under continuous agent work

Prompts make agent code cleaner at the start but do not stop it degrading change by change. Whether mechanical gates change the rate of decay is untested. This note is the research brief for finding out, written before any run so the predictions can't move afterwards.

recheck-after: 2027-02-05

## Problem statement

Almost every coding benchmark scores one task in isolation. Real work is one feature after another on the same codebase, and each agent sees only its own task, so the smallest plausible patch wins every time: a parallel path, a duplicated rule, a branch bolted onto a big function. That is [patch accretion](agent-native-codebases.md#patch-accretion-is-the-main-failure). Each patch is locally fine; the sum makes every later change slower and more error-prone.

## Evidence so far

[SlopCodeBench](https://arxiv.org/abs/2603.24755) ([code](https://github.com/SprocketLab/slop-code-bench)) makes agents extend their own solution across checkpoints as requirements change. Version 2, read 2026-11-05: 36 problems, 196 checkpoints, 15 agents.

- No agent solves a problem end to end; the best passes 14.8% of checkpoints.
- Erosion rises in 77% of trajectories and verbosity in 75.5%. Agent code is 2.3x more verbose and 2.0x more eroded than 473 open-source Python repositories, which also degrade less often over their histories.
- An anti-slop prompt cut initial erosion by about 34 to 58% and verbosity by 27 to 36%, model-dependent, at about 12% more cost per checkpoint and a 2.4-point lower strict solve rate. A plan-first prompt helped less. Neither changed the slope: quality still fell about 1.3 points per checkpoint.
- The paper tested only prompts. No gates, refactor passes or review agents.

Metric definitions matter because they decide what can be gated:

- **Erosion:** the share of complexity mass, cyclomatic complexity times the square root of source lines, held by callables whose complexity exceeds 10.
- **Verbosity:** lines flagged by 137 ast-grep rules or found in structural clones, divided by total lines.

Both are computable by a check, so both could be gates today.

[CodeThread](https://arxiv.org/abs/2606.21804) measures the downstream effect directly: a later agent resolves up to 13.1% fewer follow-up tasks when building on an earlier agent's code instead of a human's. [SWE-CI](https://arxiv.org/abs/2603.03823) runs agents through sequences derived from real repository histories.

## Research question

Which mechanical locks flatten the per-checkpoint quality slope, not just the starting level, without trading away correctness?

## Hypotheses

Each states its prediction and what would refute it.

1. **Gates lower the level.** Any hard gate on a SlopCodeBench metric lowers initial erosion and verbosity at least as much as the anti-slop prompt. Refuted if gated runs start no cleaner than prompted ones.
2. **Deletion gates flatten the slope.** Gates on unused exports, files and dependencies (knip, cargo-machete) and on clones (jscpd) force the old path out when a new one lands, so they attack accretion itself. Predicted: a visibly flatter slope than baseline. Refuted if the slope matches the prompt arms.
3. **Complexity caps get gamed.** A per-function complexity cap improves the erosion number by splitting functions into helpers that still carry the same branching and coupling. Predicted: erosion drops but total complexity, clone count and follow-up pass rate don't improve. Refuted if transcripts show real consolidation rather than reshuffling.
4. **Boundary locks attack the cause.** Erosion is a proxy for blurred ownership. Import boundaries (dependency-cruiser, import-linter, workspace dependency rules) should help most on problems whose later checkpoints cross modules. Refuted if they show no effect there.
5. **Static gates can't see semantic duplication.** Two differently shaped implementations of one rule, or a feature in the wrong owner, pass every lint. A periodic consolidation pass, proved behavior-preserving by [refactor equivalence](testing-with-agents.md), flattens what gates leave. Refuted if gated-only runs already match it.
6. **An editable gate decays.** An agent that can change lint config or add suppressions loosens the gate under pressure. The [zero-comment rule](../skills/theodore-kaczynski-nullifier/references/enforcement.md) already blocks comment-form suppressions such as `eslint-disable`, `noqa`, `type: ignore` and `@ts-expect-error`; Rust's `#[allow]`, per-file overrides and config edits remain. Predicted: denying agent writes to gate config in harness permissions removes those bypasses. Check transcripts for attempts.

## Method

Follow the [fast-loop funnel](autoresearch.md#fast-loops-first-tobias-2026-10-12):

1. Precheck from published SlopCodeBench trajectories that the chosen problems actually erode in the baseline arm, and that later checkpoints cross modules for hypothesis 4.
2. Scout two or three problems, one model, one or two runs per arm: plain, anti-slop prompt, and each gate. A gate arm must pass its gate before the checkpoint counts, with the agent allowed to iterate.
3. Read transcripts for how the agent satisfied the gate: real consolidation, reshuffling or bypass attempts. Report quality slope, strict pass rate and cost as separate numbers.
4. Replicate only an arm whose slope visibly differs.

Runs are real compute. Run them on an isolated or cloud machine, not the shared workstation.

## Open decision: ratchets

The [rollout rules](../skills/theodore-kaczynski-nullifier/references/enforcement.md#rollout) forbid baselines. That fits rule violations, which can reach zero. Continuous measures such as duplication share or total complexity have no zero state; they need a fixed threshold or a ratchet that may only improve. A ratchet is not a grandfathered violation list, but the current wording reads as banning it. Settle this with the scout results for hypotheses 2 and 3.
