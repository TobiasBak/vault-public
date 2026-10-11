# Subagent delegation

Delegate bounded, independently useful outcomes when parallelism, context isolation, independent verification, or a cheaper worker model outweighs startup and coordination cost. Keep small, obvious, tightly coupled work with the orchestrator. In Tobias's Opus-orchestrates-Sol setup the cheaper worker tilts the choice toward delegating, but it's still a judgment call (see [compute routing](#compute-routing)). Specialize by responsibility and context, not by reasoning step. Tobias's interactive Codex setup uses native tooling; model roles follow the same routing policy.

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
- Never grant a child standing authority to extend a vocabulary, schema, or format "as needed". Sol uses it on every obstacle: a 2026-10-09 corpus conversion told to "add the minimal matcher without stopping" grew 19 matchers, including arithmetic and JSON-pointer references, and turned expected-output files into an assertion language. Give the closed set, and make an extension a stop.
- Scope every stop condition to the item that hit it: park that item, finish the rest, report parked items at the end. Sol reads a bare "STOP and report" as halting the whole round; on 2026-10-09 a rewrite with 9,348 inventory items stopped on the first one and changed nothing. Stop the round only past a stated parked-item threshold.
- One writer per shared state. Parallel editors share one checkout on disjoint files; give a slice its own worktree when slices must touch the same files (lockfiles, generated code, migrations count) or its work may be thrown away. Isolated writers need an explicit merge and validation.
- Inspect diffs and artifacts, not just reports.
- Before declaring delegated work stalled, check file mtimes recursively (`git status` paths, not directory mtimes) and live `pi` processes (`pgrep -x pi`). A Pi parent's own subagents run in-process and never appear as T3 children. On 2026-10-04 a triage pass misread two live writers as stalled from T3 thread status and top-level directory mtimes, and its "resume" spawned colliding writers.
- To stop a stray writer, find its PID with `pgrep` and kill that PID. `pkill -f <pattern>` also matches the shell running the command, because the pattern is on its command line. The shell dies (exit 144), and the rest of the command, such as follow-up edits, never runs.
- State merge authority in the task. Default in repos Tobias owns: threads merge their own PRs at the [global instructions' readiness bar](https://github.com/TobiasBak/dotfiles/blob/main/configs/agents/AGENTS.md#how-to-orchestrate); staging or production promotion still needs Tobias (Tobias, 2026-10-11).
- A Pi child reads steering messages only between tool calls; one long blocking command (a VM run, a full CI driver) ignores them until it exits. To cancel such work now, interrupt the thread (`t3_thread_interrupt`) or kill the process, then steer. On 2026-10-04 a "skip the Windows run" steer arrived one minute after a 60-minute qualification command started, and the run finished anyway.
- Wait only on correctness-critical results. Schedule on events rather than in barrier batches, and cancel optional work once the evidence suffices.
- Workers verify their own boundary; the orchestrator runs integration validation once. Report blocked shared tooling instead of having every worker investigate it.
- Review handoffs follow [code review](code-review.md). Keep the reviewer independent of the author's narrative. Don't impose a fixed scout, planner, implementer, reviewer pipeline.

## Compute routing

Keep the execution contract (permissions, tools, limits, output) separate from the model and effort choice. Use the cheapest profile that reliably passes the quality gate, counting retries. Escalating cheap-first saves cost but adds latency. Judge delegation against direct execution on correctness, latency, cost per success, duplication, and recovery from failed children.

T3 Code's `delegate_task` inherits the parent's provider unless the call selects `target.providerInstanceId` or `target.driverKind`. Keeping the provider and model unchanged also preserves model options. This describes host behavior, not permission to inherit Opus for delegated work. Explicitly select the worker provider and model under Tobias's policy below. Explain unexpected routing from the recorded call's target and the parent's provider at call time, not just the current thread config or a model-name prefix.

Tobias's explicit model-role clarification is the source of this preference:

- Opus 5.5 leads and designs top-level teams only. Never delegate to an Opus subagent, including for design or research. The top-level Claude lead owns requirements, architecture, decisions, integration, and acceptance. Sol top-level leads are temporary Claude-quota recovery, not the permanent default.
- The lead prefers handing off sizable bounded reading, implementation slices, test runs, and audits, but keeps simple exploration, small edits, and context-heavy judgment. Brief workers with a concrete design, not a menu of architectural choices. Children may split execution further; design questions go back to the top-level lead.
- GPT-6.1 Sol owns delegated execution, implementation, and code review, including hard reviews. From Claude and Pi parents alike, explicitly target `{"providerInstanceId":"pi","model":"openai-codex/gpt-6.1-sol","options":{"thinking":"medium"}}`; use `high` for ambiguous debugging, intricate or design-sensitive implementation, and reviews. Never rely on inheritance from Opus. Native Codex subagents remain usable when explicitly configured for Sol.
- Haiku 5.5 at `high` remains the exception for narrowly bounded, checkable non-coding research: call-site/dependency censuses, bounded doc/log audits, log triage, and doc questions. It never leads teams, designs, implements code, or reviews code. See [Haiku 5.5 specifics](coding-models.md#haiku-55-specifics). Other worker models require Tobias's request or a missing Sol capability, with the reason stated; this does not permit Opus children. The shared global instructions in dotfiles own enforcement.
- A prose-only rule wasn't enough: Claude parents in T3 kept using the native `Agent` tool, because T3's injected guidance prefers native tools for same-provider work. Dotfiles' Claude `PreToolUse` hook (`configs/claude/route-subagents.sh`) now denies `Agent` whenever `T3CODE_HOME` is set and returns the `delegate_task` target. Outside T3 there's no `delegate_task`, so `Agent` stays allowed by that hook; the model-role policy still applies. Verified 2026-10-04 on Claude Code 2.1.289: a fresh session was blocked, and a Pi Sol child completed.

## T3 Code feedback

- Restarting or updating the T3 service can terminate running agents. Finish or stop hosted work before a restart; [dotfiles](../projects.md#dotfiles) owns service operations.
- In Orchestrator V2, separate deliberate progress messages from automatic completion delivery. Children can call `t3_thread_send` with `mode: "steer"` to feed findings into an active parent; `auto` also steers when the parent is ready. The parent can use the same tool to update child contracts. These exchanges are model-chosen, not a fixed T3 worker pipeline. See the [V2 MCP contract](https://github.com/pingdotgg/t3code/blob/8ed276c246b6/docs/orchestration-v2/orchestrator-mcp-server.md#t3_thread_send).
- A parent's plain-text reply to a child's relayed progress message reaches nobody: the child never sees it. Coordinate running children with `t3_thread_send` (`mode: "steer"`) to their `childThreadId`. On 2026-10-07 an overnight run lost several coordination replies this way before switching to steer.
- Parallel PRs from many children, where force-push is banned: have one integration child stack them in a fixed order. It merges each parent branch into the next with a merge commit, gates every layer, and retargets with `gh pr edit --base`. Give it a written conflict brief with per-file "keep both intents" notes. CSS dead-rule deletions proven against `main` must be re-proven against the integrated stack, because the stacked TSX can revive a class.
- Agent messages occupy the conversation's `user` role but retain `createdBy: "agent"` and `senderThreadId`. A user-role steering entry alone is not evidence that Tobias gave the instruction.
- Completion notifications are server-generated and distinct from progress messages. They tell the parent to retrieve the final result with `task_status`; reading the terminal result acknowledges delivery. V2 can wake an idle parent when children finish, so foreground completion does not imply the delegated work is done. See the [V2 release notes](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).
- `task_cancel` interrupts only the direct child. Grandchildren it delegated keep running and can sit on approval prompts; interrupt them by thread with `t3_thread_interrupt` (seen 2026-10-04, nightly `0.0.46-nightly.20261004.2644`).
- Tobias's agents always run full-access; nothing should wait on his approval. Of 596 T3 threads by 2026-10-04, 593 were full-access (T3's default); the 3 others had approval mode chosen explicitly, once by an Opus parent treating it as a read-only guard, which stalled its Pi child. Put limits like read-only in the task text. The global rule says so, and for Claude parents the dotfiles hook rewrites every `delegate_task` call to `runtimeMode: "full-access"` (verified: requested `approval-required`, child ran `full-access`).
