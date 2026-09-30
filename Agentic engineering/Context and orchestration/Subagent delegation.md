# Subagent delegation

Delegate bounded, independently useful outcomes when parallelism, context isolation, focused evidence, or independent verification outweigh startup and coordination costs. Keep small, obvious, tightly coupled work with the orchestrator. Specialize responsibility and context, not reasoning steps. Delegation does not guarantee quality or compensate for supposedly narrow domain intelligence.

## Route by task shape

Prompt length and keywords are weak difficulty signals. Assess:

- localization uncertainty and dependency breadth;
- reasoning depth and unresolved tradeoffs;
- mutation scope, blast radius, and reversibility;
- strength and cost of verification;
- parallel separability;
- context volume that exploration would consume.

Known local work with focused validation is usually best handled directly. A bounded subsystem change may justify one handoff. Cross-cutting or high-risk work benefits from read-only mapping, synthesis, one writer, and fresh validation. Deliver broad migrations through serial validated milestones, not writer fan-out.

## Cut coherent outcomes

The orchestrator owns consequential decisions. Split work by dependencies, ownership, evidence, independently testable behavior, or review concerns, not file counts. Keep tightly coupled files behind one interface in one worker's scope. Worker count and delegation coverage are not goals.

Separate investigation, decision support, mutation, and validation; mark prerequisites and required joins. Launch ready independent work and synthesize before dependent work. Prefer testable vertical implementation slices. Horizontal fan-out fits read-only mapping, source gathering, extraction, or mechanical work on isolated partitions.

A useful handoff states:

- goal and coherent deliverable;
- minimum sufficient context and exact evidence locations;
- approved product and architecture decisions;
- inputs, exclusions, permissions, and side-effect boundaries;
- success criteria and validation;
- compact output shape;
- stop and escalation conditions.

Let children choose procedures. Units are too small when setup dominates or siblings repeatedly share state; too large when decisions are unrelated, acceptance is unfocused, or the parent's full context must be recreated.

## Preserve authority and shared state

The orchestrator owns requirements, decomposition, routing, unresolved decisions, synthesis, integration, and acceptance. Children must escalate unapproved product, architecture, or scope choices.

Use one writer per shared state. Parallelize independent reading, testing, and review. Multiple writers require isolated state and explicit merge and validation. Inspect artifacts or diffs, not just reports.

Wait only for correctness-critical results. Use timely optional work and cancel it once evidence is sufficient. Barrier batches wait for the slowest child; event-driven scheduling starts work as results, failures, questions, or timeouts unblock it. Bound concurrency and stop at the evidence threshold.

## Context and return channel

Context isolation requires fresh or reduced inputs and concise returns, not the parent's transcript, repeated state reconstruction, or full traces. Inspect only what the decision or implementation needs; whole-codebase reads do not replace localization. For large outputs, use authorized isolated storage and return identity, revision, evidence summary, and uncertainty. [[Agent context engineering]] owns working sets and checkpoints.

## Validation, stop, and escalation

Workers verify their mutation boundaries. The orchestrator reviews joined diffs and runs shared and integration validation once. Report blocked shared tooling instead of duplicating investigation; use host timeouts for potentially stalled checks. Escalate conflicting localization, widening scope, repeated failures, weak validation, security or integrity risks, or conflicts with approved choices. Stop at sufficient evidence, exhausted budget, or a required orchestrator decision.

For review handoffs, use [[Context-sensitive code review#Initial contract and map|the review contract]] and [[Context-sensitive code review#Reviewers and authority|the reviewer-selection and authority guidance]]. Keep review independent from the author's narrative. Do not impose a fixed scout, planner, implementer, and reviewer pipeline on ordinary work.

## Execution contract versus compute route

Keep permissions, tools, side-effect limits, and output shape separate from model and effort routing. Choose by difficulty, risk, latency, and verification. Use the cheapest profile that reliably passes the quality gate, counting retries and failures. Cheap-first escalation can save cost but increase latency; parallel hedging requires cancellable, nonconflicting duplicates.

[[Tobias's developer preferences]] owns the interactive Codex setup, including native tooling without custom workers or an added delegation policy. [[Choosing and steering coding models]] covers current model and effort choices. Evaluate delegation against direct execution using end-state correctness, evidence, latency, context acquisition, cost per success, duplication, retries, and recovery from blocked or failed children.
