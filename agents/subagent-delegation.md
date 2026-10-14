# Subagent delegation

Delegate bounded, independently useful outcomes when parallelism, context isolation, independent verification, or a cheaper worker model outweighs startup and coordination cost. Keep coordination and context-heavy judgment with the orchestrator, and tightly coupled execution with one worker. Specialize by responsibility and context, not by reasoning step. Follow [compute routing](#compute-routing) for model roles and effort.

## When and how to split

Route by task shape, not prompt length. The relevant dimensions are localization uncertainty, dependency breadth, unresolved tradeoffs, blast radius, verification strength, parallel separability, and how much context exploration would burn.

- Known local work with focused validation: one executor, no further splitting.
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
- State merge authority in the task. Default in repos Tobias owns: threads merge their own PRs at the [global instructions' readiness bar](https://github.com/TobiasBak/dotfiles/blob/main/agents/AGENTS.md#how-to-orchestrate); green nightlies automatically promote main to staging without asking Tobias. Only Tobias promotes production; agents never push, promote or deploy it (Tobias, 2026-10-14).
- A Pi child reads steering messages only between tool calls; one long blocking command (a VM run, a full CI driver) ignores them until it exits. To cancel such work now, interrupt the thread (`t3_thread_interrupt`) or kill the process, then steer. On 2026-10-04 a "skip the Windows run" steer arrived one minute after a 60-minute qualification command started, and the run finished anyway.
- Wait only on correctness-critical results. Schedule on events rather than in barrier batches, and cancel optional work once the evidence suffices.
- Workers verify their own boundary; the orchestrator runs integration validation once. Report blocked shared tooling instead of having every worker investigate it.
- Review handoffs follow [code review](code-review.md). Keep the reviewer independent of the author's narrative. Don't impose a fixed scout, planner, implementer, reviewer pipeline.

## Compute routing

Keep the execution contract (permissions, tools, limits, output) separate from model routing. Within the approved roles below, judge delegation by correctness, latency, cost per success including retries, duplication, and recovery from failed children.

T3 Code's `delegate_task` inherits the parent's provider unless the call selects `target.providerInstanceId` or `target.driverKind`. Keeping the provider and model unchanged also preserves model options. This describes host behavior, not permission to inherit Opus for delegated work. Explicitly select the worker provider and model under Tobias's policy below. Explain unexpected routing from the recorded call's target and the parent's provider at call time, not just the current thread config or a model-name prefix.

Tobias's model-routing decision, 2026-10-11, revised 2026-10-14:

- **Team leads:** before launching, run `python3 /home/tb/code/vault-public/.agents/skills/chief-of-staff/scripts/cos.py quota`. If every window is below 60%, the lead may be Claude Opus 5.5 at effort `high`; otherwise use Pi GPT-6.1 Sol at thinking `high`, including when quota is unknown. Mainly UI teams keep Opus leads. Never switch running leads mid-task. The lead owns design, decisions, coordination, integration, and acceptance. Sol leads work behind chief-of-staff gates: post the plan (design, files in scope, check, worker slices) to the chief of staff and wait for its go only for a scope extension beyond the issue, a protected-surface change (existing tests or their expectations, budgets, manifests, oracles, published or frozen contracts), or a choice that belongs to Tobias. Otherwise proceed directly and record the plan in the issue. Hand over the merge-ready PR for the chief of staff to merge. At most 3 concurrent children and 2 review rounds. Stop and report when a child weakens or deletes an existing test, or drops a check of a real requirement (a worker fixing its own new, invalid assertion is fine; report it), edits outside scope, repeats a failure without progress (the same command or check fails for the same cause after a retry or rework; converging mechanical fixes such as lint, format or type errors don't count), or makes a claim no artifact backs. Outside UI work, Opus is limited to quota-approved team leads and Tobias's chief of staff; never use Opus children, design or research agents.
- **Pi GPT-6.1 Sol, thinking `high`:** default for non-UI delegated work: execution, implementation, research, exploration, test runs, audits, and review. Explicitly target `{"providerInstanceId":"pi","model":"openai-codex/gpt-6.1-sol","options":{"thinking":"high"}}`; never inherit the leader's provider or model, and never use Codex CLI for Sol. OpenAI models cannot do UI (Tobias, 2026-10-13): UI design, implementation and review target `{"providerInstanceId":"claudeAgent","model":"claude-opus-5-5","options":{"effort":"high"}}`. UI agents load `frontend-design` and judge the UI critically from real app-window screenshots, never host-desktop captures. Give children full access; put limits like "read-only" in the task. A separate child independently reviews every diff under this routing; trust artifacts, not done reports. Report `subagents: tasks=<n> accepted=<n> reworked=<n> rejected=<n> throttled=<n>`.
- **OpenCode Space Bunny:** stop using it entirely. See the [trial finding](coding-models.md#current-choice). Never use paid OpenCode models.
- **Claude Haiku 5.5:** retired (Tobias, 2026-10-12). Research and exploration go to Sol; the dotfiles routing hook denies Haiku and Space Bunny targets.

Plan-gate decision (Tobias, 2026-10-13): all gates that day were approved, the conditions mostly restated existing rules, and the waits cost 30 minutes to 2.5 hours.

Brief workers with a concrete design, not a menu of architectural choices. Children may split execution further; design questions go back to the top-level lead.

Routing can need enforcement: Claude parents in T3 followed the host's native-tool preference over prose and selected `Agent`. [Dotfiles](../projects.md#dotfiles) owns the shared global instructions and Claude routing hook; keep enforcement aligned with this policy.

## T3 Code feedback

- Restarting or updating the T3 service can terminate running agents. Finish or stop hosted work before a restart; [dotfiles](../projects.md#dotfiles) owns service operations.
- In Orchestrator V2, separate deliberate progress messages from automatic completion delivery. Children can call `t3_thread_send` with `mode: "steer"` to feed findings into an active parent; `auto` also steers when the parent is ready. The parent can use the same tool to update child contracts. These exchanges are model-chosen, not a fixed T3 worker pipeline. See the [V2 MCP contract](https://github.com/pingdotgg/t3code/blob/8ed276c246b6/docs/orchestration-v2/orchestrator-mcp-server.md#t3_thread_send).
- A parent's plain-text reply to a child's relayed progress message reaches nobody: the child never sees it. Coordinate running children with `t3_thread_send` (`mode: "steer"`) to their `childThreadId`. On 2026-10-07 an overnight run lost several coordination replies this way before switching to steer.
- Parallel PRs from many children, where force-push is banned: have one integration child stack them in a fixed order. It merges each parent branch into the next with a merge commit, gates every layer, and retargets with `gh pr edit --base`. Give it a written conflict brief with per-file "keep both intents" notes. CSS dead-rule deletions proven against `main` must be re-proven against the integrated stack, because the stacked TSX can revive a class.
- Agent messages occupy the conversation's `user` role but retain `createdBy: "agent"` and `senderThreadId`. A user-role steering entry alone is not evidence that Tobias gave the instruction.
- Completion notifications are server-generated and distinct from progress messages. They tell the parent to retrieve the final result with `task_status`; reading the terminal result acknowledges delivery. V2 can wake an idle parent when children finish, so foreground completion does not imply the delegated work is done. See the [V2 release notes](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).
- `task_cancel` interrupts only the direct child. Grandchildren it delegated keep running and can sit on approval prompts; interrupt them by thread with `t3_thread_interrupt` (seen 2026-10-04, nightly `0.0.46-nightly.20261004.2644`).
- Tobias's agents always run full-access; nothing should wait on his approval. Of 596 T3 threads by 2026-10-04, 593 were full-access (T3's default); the 3 others had approval mode chosen explicitly, once by an Opus parent treating it as a read-only guard, which stalled its Pi child. Put limits like read-only in the task text. The global rule says so, and for Claude parents the dotfiles hook rewrites every `delegate_task` call to `runtimeMode: "full-access"` (verified: requested `approval-required`, child ran `full-access`).
