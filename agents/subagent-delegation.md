# Subagent delegation

Delegate bounded, independently useful outcomes when parallelism, context isolation, independent verification, or a cheaper worker model outweighs startup and coordination cost. Keep small, obvious, tightly coupled work with the orchestrator. In Tobias's Opus-orchestrates-Sol setup the cheaper worker tilts the choice toward delegating, but it's still a judgment call (see [compute routing](#compute-routing)). Specialize by responsibility and context, not by reasoning step. Tobias's interactive Codex setup uses native tooling with no added delegation policy.

## When and how to split

Route by task shape, not prompt length. The relevant dimensions are localization uncertainty, dependency breadth, unresolved tradeoffs, blast radius, verification strength, parallel separability, and how much context exploration would burn.

- Known local work with focused validation: do it directly.
- A bounded subsystem change: one handoff may pay off.
- Cross-cutting or high-risk work: read-only mapping in parallel, then synthesis, one writer, and fresh validation.
- Broad migrations: serial validated milestones, never fan-out writers.

Split by dependencies, ownership, and independently testable behavior, not by file count. Keep tightly coupled files with one worker. Use vertical slices for implementation and horizontal fan-out for read-only mapping, gathering, and mechanical work on isolated partitions. A unit is too small when setup dominates and too large when it needs the parent's full context recreated.

## Handoff

State the goal and deliverable, the minimum context with exact evidence locations, decisions already approved, permissions and side-effect limits, success criteria, output shape, and when to stop or escalate. Let the child choose its own procedure. Pass reduced inputs, not the parent transcript, and get back a compact result or an artifact reference.

- Word race and robustness reviews neutrally: describe the contract and ask whether it holds. On 2026-10-04 OpenAI's cyber filter killed a Pi Sol review mid-run ("flagged for possible cybersecurity risk"). The brief said "try to break the invariant", "hide the worker" and "fork-heavy load". The same review reworded as contract checks ran clean. Salvage partial artifacts from the child's output directory before re-delegating.
- Children that run tests or probes on a candidate get a disposable `git worktree add` and run `uv` from its root. Copying the candidate's venv or entrypoints keeps absolute shebangs, so imports and artifacts land back in the candidate checkout.
- `git worktree remove` deletes gitignored files too, including `.local/` receipts and evidence archives. Copy evidence you need out of a disposable worktree, or have the child write it to a retained path, before removing the worktree.

## Authority and shared state

- The orchestrator owns requirements, decomposition, open decisions, integration, and acceptance. Children escalate any unapproved product, architecture, or scope choice.
- One writer per shared state. Multiple writers need isolated state plus an explicit merge and validation.
- Inspect diffs and artifacts, not just reports.
- Before declaring delegated work stalled, check file mtimes recursively (`git status` paths, not directory mtimes) and live `pi` processes (`pgrep -x pi`). A Pi parent's own subagents run in-process and never appear as T3 children. On 2026-10-04 a triage pass misread two live writers as stalled from T3 thread status and top-level directory mtimes, and its "resume" spawned colliding writers.
- To stop a stray writer, find its PID with `pgrep` and kill that PID. `pkill -f <pattern>` also matches the shell running the command, because the pattern is on its command line. The shell dies (exit 144), and the rest of the command, such as follow-up edits, never runs.
- State merge authority in the task. Without it, owner threads open PRs and then wait indefinitely for a go-ahead. Give them a readiness bar (reviews clean, CI green on the head, required platform run) and let them merge.
- A Pi child reads steering messages only between tool calls; one long blocking command (a VM run, a full CI driver) ignores them until it exits. To cancel such work now, interrupt the thread (`t3_thread_interrupt`) or kill the process, then steer. On 2026-10-04 a "skip the Windows run" steer arrived one minute after a 60-minute qualification command started, and the run finished anyway.
- Wait only on correctness-critical results. Schedule on events rather than in barrier batches, and cancel optional work once the evidence suffices.
- Workers verify their own boundary; the orchestrator runs integration validation once. Report blocked shared tooling instead of having every worker investigate it.
- Review handoffs follow [code review](code-review.md). Keep the reviewer independent of the author's narrative. Don't impose a fixed scout, planner, implementer, reviewer pipeline.

## Compute routing

Keep the execution contract (permissions, tools, limits, output) separate from the model and effort choice. Use the cheapest profile that reliably passes the quality gate, counting retries. Escalating cheap-first saves cost but adds latency. Judge delegation against direct execution on correctness, latency, cost per success, duplication, and recovery from failed children.

T3 Code's `delegate_task` inherits the parent's provider unless the call selects `target.providerInstanceId` or `target.driverKind`. Keeping the provider and model unchanged also preserves model options. The parent model chooses whether to override; Pi can request Codex children running the same LLM. Explain unexpected routing from the recorded call's target and the parent's provider at call time, not just the current thread config or a model-name prefix.

Tobias's split:

- The Claude Opus parent orchestrates and *prefers* to hand off sizable bounded work: broad reading, implementation slices, test runs, audits. He doesn't want forced delegation. Simple exploration, small edits, and context-heavy judgment stay with the parent, because handoffs and summaries lose context. The parent keeps requirements, decisions, integration, and final review. The cost rationale: a long session's cost is mostly the parent carrying its growing context.
- Subagents run in Pi on GPT-6.1 Sol (`pi` / `openai-codex/gpt-6.1-sol`), from Claude and Pi parents alike. Thinking is `medium` for clear or mechanical work and `high` for ambiguous debugging, design-sensitive changes, and reviews; pass `options: {"thinking": ...}` in the target. Verified 2026-10-04: a child sent `high` switched from Pi's `medium` default.
- Switch away from Pi Sol only on Tobias's request or when Pi lacks a required model or capability, and explain the reason. Codex parents keep their native subagents, which inherit Sol. The shared global instructions in dotfiles own this rule.
- A prose-only rule wasn't enough: Claude parents in T3 kept using the native `Agent` tool, because T3's injected guidance prefers native tools for same-provider work. Dotfiles' Claude `PreToolUse` hook (`configs/claude/route-subagents.sh`) now denies `Agent` whenever `T3CODE_HOME` is set and returns the `delegate_task` target. Outside T3 there's no `delegate_task`, so `Agent` stays allowed. Verified 2026-10-04 on Claude Code 2.1.289: a fresh session was blocked, and a Pi Sol child completed.

## T3 Code feedback

- In Orchestrator V2, separate deliberate progress messages from automatic completion delivery. Children can call `t3_thread_send` with `mode: "steer"` to feed findings into an active parent; `auto` also steers when the parent is ready. The parent can use the same tool to update child contracts. These exchanges are model-chosen, not a fixed T3 worker pipeline. See the [V2 MCP contract](https://github.com/pingdotgg/t3code/blob/8ed276c246b6/docs/orchestration-v2/orchestrator-mcp-server.md#t3_thread_send).
- Agent messages occupy the conversation's `user` role but retain `createdBy: "agent"` and `senderThreadId`. A user-role steering entry alone is not evidence that Tobias gave the instruction.
- Completion notifications are server-generated and distinct from progress messages. They tell the parent to retrieve the final result with `task_status`; reading the terminal result acknowledges delivery. V2 can wake an idle parent when children finish, so foreground completion does not imply the delegated work is done. See the [V2 release notes](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).
- `task_cancel` interrupts only the direct child. Grandchildren it delegated keep running and can sit on approval prompts; interrupt them by thread with `t3_thread_interrupt` (seen 2026-10-04, nightly `0.0.46-nightly.20261004.2644`).
- Tobias's agents always run full-access; nothing should wait on his approval. Of 596 T3 threads by 2026-10-04, 593 were full-access (T3's default); the 3 others had approval mode chosen explicitly, once by an Opus parent treating it as a read-only guard, which stalled its Pi child. Put limits like read-only in the task text. The global rule says so, and for Claude parents the dotfiles hook rewrites every `delegate_task` call to `runtimeMode: "full-access"` (verified: requested `approval-required`, child ran `full-access`).
