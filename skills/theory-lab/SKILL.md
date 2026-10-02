---
name: theory-lab
description: Develop mechanistic, cross-domain theories and convert promising ones into discriminating experiment proposals. Invoke manually for anomaly explanation, theory development, paradigm search, or high-leverage Autoresearch directions beyond incremental optimization.
disable-model-invocation: true
---

# Theory Lab

Expand the hypothesis space through research, cross-domain synthesis, first principles, and experiment history. Optimize for explanatory leverage and information gain, not the smallest safe fix. A paradigm candidate must change the causal decomposition, controllable variable, representation, objective, scale, or unit of operation; unfamiliar vocabulary alone doesn't count. Propose experiments here; run them only when separately asked.

## Frame the inquiry

Pin down the phenomenon or anomaly, what would count as a breakthrough, existing observations and results, hard constraints (physical, safety, resources), the current explanation or champion, the evaluator and intervention surface, and the budget. Ask only for gaps that would change the investigation; otherwise state your assumptions. Separate real constraints from inherited conventions.

## Working set

In Tobias's vault (`vault-public`), search before assuming knowledge is absent, especially `agents/context-engineering.md` and `agents/autoresearch.md`. Map first, read narrowly, load whole artifacts only when needed, and keep stable references. Hold a compact reconstruction block: the contract, evidence references, observations and anomalies, live and rejected mechanisms, open questions, and the next action. Refresh it at boundaries and before handoff. Don't record speculative conclusions as established knowledge.

Interleave research and generation freely. Research early when facts are missing. Generate before searching exact formulations when the dominant literature would anchor you, and research afterwards for novelty and counter-evidence. Subagents with deliberately different, reduced evidence packets help with independent mechanism search, adjacent fields, or adversarial review. Keep synthesis and selection with yourself.

## Reconstruct the mechanism

Build the strongest current causal account. Separate:
- observation from explanation
- necessary constraints from design choices
- correlation from intervention
- static from conditional regimes
- the resource saved from where its cost actually moved

Identify bottlenecks, feedback loops, scaling, selection effects, hidden state, and unexplained anomalies. Say what would prove the account wrong.

## Generate candidates

Work at three levels: **local** (a parameter or component), **mechanism** (what controls the outcome), and **paradigm** (representation, decomposition, objective, topology, timescale, unit). Produce a few mechanistically distinct candidates, and keep one that challenges the dominant framing. Useful moves:

- split a concept into independent axes
- invert, remove, or condition an assumption
- change the unit, granularity, timescale, or boundary
- separate value from topology, storage, routing, or control
- make a static mechanism adaptive, or the reverse
- borrow mechanisms from structurally similar fields
- explain the anomaly rather than optimizing around it
- relocate computation or risk, accounting for the receiving side
- ask what overhead could reverse the theoretical gain

An analogy counts as evidence only after explicit mapping: entities, state, dynamics, constraints, feedback, scale, intervention, the bridge premise, and where the mapping fails. Search adjacent fields by causal structure, not by the target field's terms. Known parts can still compose into a new mechanism.

## Theory cards

For each serious candidate:
- **Claim:** the explanation and the intervention.
- **Causal chain:** how the intervention produces the outcome.
- **Departure:** which current assumption changes.
- **Basis:** observations, research, analogies, derivation.
- **Bridge assumptions:** what must hold for a transferred mechanism to apply.
- **Rivals.**
- **Divergent predictions:** what this theory expects that its rivals don't.
- **Falsifier:** the strongest feasible result that would kill it.
- **Failure signature:** what a failed implementation looks like and what it would still teach.
- **Scope and substrate:** where it should and shouldn't generalize.
- **Novelty:** known, adapted, new combination, or apparently new, with the nearest prior work.
- **Cheapest discriminating test.**

Develop the idea before attacking feasibility, then attack hard. Never certify novelty from a limited search. Compare candidates on separate axes: explanatory leverage, prediction specificity, fit with evidence, impact if true, test cost and reversibility, fragility, and safety and Goodhart risk. Prefer an experiment that discriminates over choosing between indistinguishable stories.

## Hand off to Autoresearch

With a bounded surface and trustworthy evaluator, turn theories into an experiment portfolio following `agents/autoresearch.md`. Per experiment, state:
- mechanism and rivals, intervention and control
- controlled variables, correctness gates, and confounds
- predictions under each rival
- information gain, cost, and reversibility
- success, falsification, near-miss, inconclusive, and invalid signatures
- rollback and limits
- reopening condition and successors

Keep evaluator changes separate from candidate changes. Use plateaus and repeated failure signatures to revise the model rather than generating nearby variants.

## Verification

When a theory could shape executable artifacts, map its mechanism to observable predictions at that surface, with rivals or ablations that discriminate between them. An aggregate improvement alone doesn't verify the explanation. Report exactly what ran and which predictions remain untested.

## Return

1. Inquiry contract.
2. Evidence map with conflicts and gaps.
3. Causal account and unexplained anomalies.
4. The strongest few theory cards.
5. Comparison and novelty findings.
6. Ordered experiments with a recommended first test.
7. Reconstruction block.

Mark what was retrieved, derived, and speculated. Cite only where authority or novelty matters. Stop at the requested depth, when candidates are indistinguishable, when the evaluator is unsuitable, when the budget runs out, or when a user decision is needed. If no testable theory survives, name the bottleneck and the evidence needed; don't manufacture a breakthrough.
