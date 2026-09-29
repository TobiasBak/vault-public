# Subagent delegation

Delegation is an execution option, not a guarantee of quality. Use it when a bounded subtask can produce independently useful progress and parallelism, context isolation, a specialized viewpoint, or independent verification outweighs startup and coordination cost. Keep small, obvious, tightly coupled work with the orchestrator. Specialize a worker's responsibility and context, not its step-by-step reasoning; the value is a focused evidence set or review lens rather than compensation for supposedly narrow domain intelligence.

## Route by task shape

Prompt length and keywords are weak difficulty signals. Assess:

- localization uncertainty and dependency breadth;
- reasoning depth and unresolved tradeoffs;
- mutation scope, blast radius, and reversibility;
- strength and cost of verification;
- parallel separability;
- context volume that exploration would consume.

Known local work with focused validation is usually direct. A bounded subsystem change may justify one implementation handoff. Cross-cutting or high-risk work benefits from parallel read-only mapping, a synthesized direction, one writer, and fresh validation. Broad migrations should proceed through serial validated milestones rather than uncontrolled writer fan-out.

## Cut coherent outcomes

Keep the decision spine with the orchestrator. Turn broad work into a dependency graph of unknowns, decisions, artifacts, and validations. Cut at ownership boundaries, evidence sources, independently testable behavior, or review concerns, not arbitrary file counts. Group tightly coupled files behind one interface into a cohesive worker boundary; do not optimize worker count or delegation coverage.

Classify units as investigation, decision support, mutation, or validation. Mark prerequisites and true joins. Launch only ready units, parallelize independent leaves, and synthesize before dependent work. Prefer vertical implementation slices that yield testable behavior. Horizontal fan-out fits read-only mapping, source gathering, extraction, or the same mechanical operation across isolated partitions.

A useful handoff states:

- goal and coherent deliverable;
- minimum sufficient context and exact evidence locations;
- approved product and architecture decisions;
- inputs, exclusions, permissions, and side-effect boundaries;
- success criteria and validation;
- compact output shape;
- stop and escalation conditions.

The child should choose the local procedure. The unit is too small when setup and context reconstruction dominate or siblings repeatedly touch the same state. It is too large when it mixes unrelated decisions, lacks a focused acceptance gate, or requires recreating the parent's full context.

## Preserve authority and shared state

The orchestrator owns requirements, decomposition, routing, unresolved decisions, synthesis, integration, and final acceptance. A child that discovers an unapproved product, architecture, or scope choice must escalate rather than decide silently.

Use one writer per shared state. Parallelize independent reading, testing, and review more readily than writes. Multiple writers are safe only when their state is isolated and an explicit merge and validation stage exists. Review actual artifacts or diffs, not merely child reports.

A dependency join should wait only for results required by correctness. Classify optional work as useful or speculative, consume it if timely, and cancel it when sufficient evidence exists. Barrier batches inherit the latency of the slowest child; event-driven scheduling can launch newly unblocked work as results, failures, questions, and timeouts arrive. Bound concurrency and stop when the evidence threshold is met.

## Context and return channel

Delegation isolates context only when the child receives a fresh or deliberately reduced context and returns a concise result. Passing the parent's bloated transcript, forcing reconstruction of the same state, or returning a full trace defeats the purpose. Scope repository inspection to the surfaces needed for the decision or implementation; reading the whole codebase is not a substitute for localization and can dominate cost. For large outputs, let the child write to authorized isolated storage and return an identity, revision, evidence summary, and uncertainty. [[Agent context engineering]] owns the broader working-set and checkpoint policy.

## Validation, stop, and escalation

Every mutation handoff owns focused verification for its boundary. After joining workers, the orchestrator reviews their diffs and runs shared and integration validation once. Workers report blocked shared tooling rather than duplicating environment investigation; use host-enforced timeouts when a validation command may stall. Escalate on conflicting localization, a widening change surface, repeated tool or test failure, weak validation, security or data-integrity risk, or a newly discovered conflict with an approved decision. Stop bounded exploration when its evidence standard is met, its budget is exhausted, or progress requires an orchestrator decision.

Independent review is most valuable when failure would be consequential, validation is weak, or the reviewer can inspect the artifact with fresh context. Give the reviewer requirements and governing invariants, base and candidate identities, the actual diff, context routes, review concerns, and validation evidence. Do not preload the author's exploration trace or conclusions. The reviewer should start at changed symbols, search outward for callers, alternate terminology, adapters, tests, and external boundaries, then cite exact artifact evidence. See [[Search-driven code discoverability]].

For pull requests, default to one general reviewer, then trigger specialists from the diff when a changed surface warrants a distinct lens such as security, data integrity, concurrency, or public contracts. Give each specialist a narrow responsibility and tools to retrieve more evidence beyond the diff. Do not always run a large fixed panel: irrelevant reviewers add context, latency, cost, and duplicate findings without creating independent value. More generally, do not impose a fixed scout, planner, implementer, and reviewer pipeline on ordinary work.

## Execution contract versus compute route

Permissions, tools, side-effect limits, and output shape form a stable execution contract. Model and reasoning effort are a separate routing choice based on difficulty, risk, latency, and available verification. Use the least expensive profile that reliably clears the quality gate, but account for retries and failed trajectories. Cheap-first escalation can save cost while increasing latency; parallel hedging is appropriate only when duplicates can be cancelled and cannot conflict.

Tobias's current interactive Codex preference lives in [[Working with GPT-6 Astra]]: native tooling without custom workers or an added delegation policy. [[Choosing and steering coding models]] covers current model and effort choices. Evaluate delegation against direct execution using end-state correctness, evidence, latency, context acquisition, cost per success, duplication, retries, and recovery from blocked or failed children.
