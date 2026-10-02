# Subagent delegation

Delegate bounded, independently useful outcomes when parallelism, context isolation, or independent verification outweighs startup and coordination cost. Keep small, obvious, tightly coupled work with the orchestrator. Specialize by responsibility and context, not by reasoning step. Tobias's interactive Codex setup uses native tooling with no added delegation policy.

## When and how to split

Route by task shape, not prompt length. The relevant dimensions are localization uncertainty, dependency breadth, unresolved tradeoffs, blast radius, verification strength, parallel separability, and how much context exploration would burn.

- Known local work with focused validation: do it directly.
- A bounded subsystem change: one handoff may pay off.
- Cross-cutting or high-risk work: read-only mapping in parallel, then synthesis, one writer, and fresh validation.
- Broad migrations: serial validated milestones, never fan-out writers.

Split by dependencies, ownership, and independently testable behavior, not by file count. Keep tightly coupled files with one worker. Use vertical slices for implementation and horizontal fan-out for read-only mapping, gathering, and mechanical work on isolated partitions. A unit is too small when setup dominates and too large when it needs the parent's full context recreated.

## Handoff

State the goal and deliverable, the minimum context with exact evidence locations, decisions already approved, permissions and side-effect limits, success criteria, output shape, and when to stop or escalate. Let the child choose its own procedure. Pass reduced inputs, not the parent transcript, and get back a compact result or an artifact reference.

## Authority and shared state

- The orchestrator owns requirements, decomposition, open decisions, integration, and acceptance. Children escalate any unapproved product, architecture, or scope choice.
- One writer per shared state. Multiple writers need isolated state plus an explicit merge and validation.
- Inspect diffs and artifacts, not just reports.
- Wait only on correctness-critical results. Schedule on events rather than in barrier batches, and cancel optional work once the evidence suffices.
- Workers verify their own boundary; the orchestrator runs integration validation once. Report blocked shared tooling instead of having every worker investigate it.
- Review handoffs follow [code review](code-review.md). Keep the reviewer independent of the author's narrative. Don't impose a fixed scout, planner, implementer, reviewer pipeline.

## Compute routing

Keep the execution contract (permissions, tools, limits, output) separate from the model and effort choice. Use the cheapest profile that reliably passes the quality gate, counting retries. Escalating cheap-first saves cost but adds latency. Judge delegation against direct execution on correctness, latency, cost per success, duplication, and recovery from failed children.
