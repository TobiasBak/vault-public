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

T3 Code's `delegate_task` inherits the parent's provider unless the call selects `target.providerInstanceId` or `target.driverKind`. Keeping the provider and model unchanged also preserves model options. The parent model chooses whether to override; Pi can request Codex children running the same LLM. Explain unexpected routing from the recorded call's target and the parent's provider at call time, not just the current thread config or a model-name prefix.

Tobias wants Pi parents to use Pi children by default. Switch harness only on his request or when Pi lacks a required model or capability, and explain the reason. The shared global instructions in dotfiles own this preference; Codex parents keep their native delegation behavior.

## T3 Code feedback

- In Orchestrator V2, separate deliberate progress messages from automatic completion delivery. Children can call `t3_thread_send` with `mode: "steer"` to feed findings into an active parent; `auto` also steers when the parent is ready. The parent can use the same tool to update child contracts. These exchanges are model-chosen, not a fixed T3 worker pipeline. See the [V2 MCP contract](https://github.com/pingdotgg/t3code/blob/8ed276c246b6/docs/orchestration-v2/orchestrator-mcp-server.md#t3_thread_send).
- Agent messages occupy the conversation's `user` role but retain `createdBy: "agent"` and `senderThreadId`. A user-role steering entry alone is not evidence that Tobias gave the instruction.
- Completion notifications are server-generated and distinct from progress messages. They tell the parent to retrieve the final result with `task_status`; reading the terminal result acknowledges delivery. V2 can wake an idle parent when children finish, so foreground completion does not imply the delegated work is done. See the [V2 release notes](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).
