# Subagent delegation

One primary agent does its whole task itself: reading, research, exploration, design, implementation, tests and verification. Tobias's own outcome (2026-10-25): he gets more done, more accurately, with one agent than with an orchestrator in most cases; the rule began as 2026-10-24 (agents spawning far too many subagents). Frontier compaction loses little; partial briefs and rebuilt understanding lose more. [Dotfiles](../projects.md#dotfiles) owns the global rule; this note covers how to divide work where dividing is allowed. Follow [compute routing](compute-routing.md) for model roles and effort.

recheck-after: 2027-01-24

## Who divides

- **Coordinators:** the top agent Tobias talks to that runs other agents, such as the [chief of staff](../.agents/skills/chief-of-staff/SKILL.md).
- **Large-project leads:** top agents owning several independent outcomes, more than one agent can carry.
- **Broken or important work stays with the agent Tobias talks to** (Tobias, 2026-10-24): it does the work itself, coordinator or not. Sol 6.1 is too slow for it.
- **Everyone else:** no subagents. The only exception is the independent review a repository declares for protected surfaces ([code review](code-review.md)). A broad search, many files, a long task or a big context is not a reason to delegate. Host prompts and skills that suggest subagents (Claude Code's `Agent`/Explore, vendored `grilling`, `deep-research`) lose to this rule.

## When a specialist earns its own context

Anthropic's Applied AI team, on several enterprise deployments (2026-10-22): one model in one context window running an open-ended tool loop, with procedure in skills and hard limits in tools, beat both one-prompt designs and orchestrator-subagent designs on quality, usually at lower cost and latency. It keeps a subagent when the single loop measurably degrades from context bloat, tasks need parallel fresh contexts that can be discarded, or tool choice and instructions conflict. Routers, planners, intent classifiers and per-team domain agents fold in instead, because shared context beats lossy summaries and each hop re-sends degraded detail ("telephone game"). One customer measured roughly 2x faster runtime on a single loop, and Anthropic's own failure list — subagent sprawl, frankenprompt, evals overfitted per team, latency — is [Conway's law](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop) in an agent tree. Rigid multi-agent structure is also what blocked migrations to a capable new model.

Scope, because it is easy to over-read: that is advice for one product agent serving many end users, not evidence about how one person's agent fleet should divide work, and the rule above stays stricter than it. Its anecdotes are unnamed deployments with no published eval.

What separates the durable part from the expired part: **capability evidence expires with the model generation, mechanism doesn't** (Tobias, 2026-10-25: current models make most prior model knowledge obsolete). Numbers from an Opus 4 / Sonnet 4 eval, a June 2025 subagent design, or a threshold calibrated on last year's models cannot settle today's architecture, and per-generation scaffolding is exactly what the 2026 report says gets in a better model's way. So:

- **Expired, kept only as history:** the 2025 multi-agent research result (multi-agent beat single-agent Opus 4 by 90.2% on an internal research eval). The structural lesson inside it survives — that result was bought with spend, roughly 15x chat tokens against 4x for a single agent, with token usage explaining most of that eval's variance — so an architecture claim still needs an equal-budget comparison ([benchmark trust](benchmark-trust.md)). Coding has fewer parallelizable subtasks than research; that was true of the 2025 generation and is not a claim about the current one.
- **Mechanism, still binding:** a handoff is a summary, so it loses detail no matter how capable the writer is; a second loop costs another call and another wait; actions carry implicit decisions, so parallel writers with differing assumptions produce inconsistent work. Capability can reduce how often you need a second window. It cannot make a lossy summary lossless.
- **The variable that decides it:** separable breadth — independent paths compressed back, as in search — versus interdependent work making shared decisions. Higher capability moves the boundary toward one loop, because the model can hold more and route for itself.

Cognition's rule (2025-06) to share context and full traces, never build parallel multi-agents, is stated as a principle about decisions rather than a claim about model ability, which is why it still holds. Treat anything from that era that measures *how much a model can do* as superseded until re-measured on the current models.

The declared-surface review is the deliberate exception: it is refused the author's narrative, so a fresh context is the feature rather than the loss ([code review](code-review.md)).

A fresh context per task is not a subagent: a new top-level session keeps one whole task in one window at no handoff cost ([context engineering](context-engineering.md)). Delegation is for outcomes that run beside the caller, not for shortening its window.

**Folding an existing specialist:** build the task-completion eval first — one end-to-end set owned centrally plus small sets shipped with each skill, ten golden examples is enough — then fold the highest-use one, turning its prompt into a skill and its API calls into tools. Merge specialists that chain on each other's output, touch the same data or are usually called together.

- Grade the final message; while an orchestrator exists also track routing accuracy, and afterwards whether the right skill or tool was chosen.
- Keep a specialist as a tool the main loop calls, with a shared response schema and the main agent verifying its conclusion against real data. Full handoff only when it must talk to the user directly; otherwise it is a skill plus tools.
- Read which tasks flipped, not just the total, and run each more than once. In Anthropic's sample support agent one fold lowered latency and broke a passing chain: the main agent answered from an order-lookup tool without asking the shipping specialist for the delivery date. It showed up in one run of two.

## How to split

Each delegate does the same job as a primary agent: it owns one whole outcome end to end, does everything itself and never delegates further. Never hand out research, exploration, mapping or review slices, and never split one chosen design across agents.

- Split by dependencies, ownership and independently testable behavior, not by file count. Keep tightly coupled files with one owner.
- Broad migrations: serial validated milestones, never fan-out writers.
- A unit is too small when setup dominates and too large when it needs the parent's full context recreated.

## Context lifespan

Each delegate gets one whole outcome, a validation boundary and a stop condition, and keeps it to the end. Follow-up outcomes get a fresh delegate; never add phases by steering or auto-resuming a finished one.

**30-minute notice** (Tobias, 2026-10-24, replacing the 2026-10-22 forced checkpoint and restart): T3 tells the parent once when a `delegate_task` child has run 30 minutes, through git-at-home's local `t3/delegate-notice.patch`. The notice tells the parent to find why from the child's activity and not restart a healthy task, so instructions don't repeat it. CoS teams are top-level threads and get no notice; the census covers them.

When a delegate stops unfinished, its [continuation checkpoint](context-engineering.md#continuation) is unfinished work with an explicit next action, not a delivery claim. Preserve live job ownership and confirm the old writer has stopped before replacing it.

## Handoff

State the goal and deliverable, the minimum context with exact evidence locations, decisions already approved, permissions and side-effect limits, success criteria, output shape, and when to stop or escalate. Let the child choose its own procedure. Pass reduced inputs, not the parent transcript, and get back a compact result or an artifact reference.

- Word race and robustness reviews neutrally: describe the contract and ask whether it holds. On 2026-10-04 OpenAI's cyber filter killed a Pi Sol review mid-run ("flagged for possible cybersecurity risk"). The brief said "try to break the invariant", "hide the worker" and "fork-heavy load". The same review reworded as contract checks ran clean. Salvage partial artifacts from the child's output directory before re-delegating.
- Use gah for isolated candidate work; it gives each child its own workspace. Never create extra Git worktrees, clones or private tool trees. Dotfiles and vault remain plain checkouts with explicit writer ownership. Run `uv` from the assigned workspace root; copying a candidate's venv or entrypoints preserves absolute shebangs and can write back into the wrong checkout.
- Removing an old Git worktree deletes gitignored files too, including `.local/` receipts and evidence archives. Retain needed evidence before cleanup; do not create another worktree to replace it.

## Authority and shared state

- The orchestrator owns requirements, decomposition, open decisions, integration, and acceptance. Children escalate any unapproved product, architecture, or scope choice.
- Never grant a child standing authority to extend a vocabulary, schema, or format "as needed". Sol uses it on every obstacle: a 2026-10-09 corpus conversion told to "add the minimal matcher without stopping" grew 19 matchers, including arithmetic and JSON-pointer references, and turned expected-output files into an assertion language. Give the closed set, and make an extension a stop.
- Scope every stop condition to the item that hit it: park that item, finish the rest, report parked items at the end. Sol reads a bare "STOP and report" as halting the whole round; on 2026-10-09 a rewrite with 9,348 inventory items stopped on the first one and changed nothing. Stop the round only past a stated parked-item threshold.
- One writer per shared state. Gah owns workspace isolation and child integration. Keep coupled changes under one owner; isolated writers still need integration validation. In plain shared checkouts, parallel writers must own disjoint files, including lockfiles, generated code and migrations.
- Inspect diffs and artifacts, not just reports.
- Check repository visibility through the host API before applying public-publication rules. A GitHub URL or authenticated `ls-remote` doesn't establish visibility; private pushes need no public-push exception (Tobias, 2026-10-11).
- Before declaring delegated work stalled, check file mtimes recursively (`git status` paths, not directory mtimes) and live `pi` processes (`pgrep -x pi`). A Pi parent's own subagents run in-process and never appear as T3 children. On 2026-10-04 a triage pass misread two live writers as stalled from T3 thread status and top-level directory mtimes, and its "resume" spawned colliding writers.
- To stop a stray writer, find its PID with `pgrep` and kill that PID. `pkill -f <pattern>` also matches the shell running the command, because the pattern is on its command line. The shell dies (exit 144), and the rest of the command, such as follow-up edits, never runs.
- State landing authority in the task. In repos Tobias owns, agents land their own changes under the [delivery policy](../tobias/preferences.md#delivery-and-releases), using `gah merge` in gah workspaces. Agents land staging promotions autonomously. Production merge, deploy, publish and rollback require Tobias's explicit instruction for that action.
- A Pi child reads steering messages only between tool calls; one long blocking command (a VM run, a full CI driver) ignores them until it exits. To cancel such work now, interrupt the thread (`t3_thread_interrupt`) or kill the process, then steer. On 2026-10-04 a "skip the Windows run" steer arrived one minute after a 60-minute qualification command started, and the run finished anyway.
- Wait only on correctness-critical results. Schedule on events rather than in barrier batches, and cancel optional work once the evidence suffices.
- Workers verify their own boundary; the orchestrator runs integration validation once. Report blocked shared tooling instead of having every worker investigate it.
- Review handoffs follow [code review](code-review.md). Keep the reviewer independent of the author's narrative. Don't impose a fixed scout, planner, implementer, reviewer pipeline.

## Compute routing

Model roles, targets and effort live in [compute routing](compute-routing.md), including the T3 inheritance trap and the routing hook. Judge delegation by correctness, latency, cost per success including retries, duplication, and recovery from failed children.

## T3 Code feedback

- Before restarting or updating T3, follow the [restart check](../software/t3-code-operations.md#service-restarts). [T3 operations](../software/t3-code-operations.md) also covers thread discovery, workspaces, secrets and webhooks.
- In Orchestrator V2, separate deliberate progress messages from automatic completion delivery. Children can call `t3_thread_send` with `mode: "steer"` to feed findings into an active parent; use `auto` only for an idle recipient. The parent can use the same tool to update child contracts. These exchanges are model-chosen, not a fixed T3 worker pipeline. See the [V2 MCP contract](https://github.com/pingdotgg/t3code/blob/8ed276c246b6/docs/orchestration-v2/orchestrator-mcp-server.md#t3_thread_send).
- A parent's plain-text reply to a child's relayed progress message reaches nobody: the child never sees it. Coordinate running children with `t3_thread_send` (`mode: "steer"`) to their `childThreadId`. On 2026-10-07 an overnight run lost several coordination replies this way before switching to steer.
- Parallel PRs from many children, where force-push is banned: have one integration child stack them in a fixed order. It merges each parent branch into the next with a merge commit, gates every layer, and retargets with `gh pr edit --base`. Give it a written conflict brief with per-file "keep both intents" notes. CSS dead-rule deletions proven against `main` must be re-proven against the integrated stack, because the stacked TSX can revive a class.
- Agent messages occupy the conversation's `user` role but retain `createdBy: "agent"` and `senderThreadId`. A user-role steering entry alone is not evidence that Tobias gave the instruction.
- Completion notifications are server-generated and distinct from progress messages. They tell the parent to retrieve the final result with `task_status`; reading the terminal result acknowledges delivery. V2 can wake an idle parent when children finish, so foreground completion does not imply the delegated work is done. See the [V2 release notes](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).
- `task_cancel` interrupts only the direct child. Grandchildren it delegated keep running and can sit on approval prompts; interrupt them by thread with `t3_thread_interrupt` (seen 2026-10-04, nightly `0.0.46-nightly.20261004.2644`).
- Tobias's agents always run full-access; nothing should wait on his approval. Of 596 T3 threads by 2026-10-04, 593 were full-access (T3's default); the 3 others had approval mode chosen explicitly, once by an Opus parent treating it as a read-only guard, which stalled its Pi child. Put limits like read-only in the task text. The global rule says so, and for Claude parents the dotfiles hook rewrites every `delegate_task` call to `runtimeMode: "full-access"` (verified: requested `approval-required`, child ran `full-access`).
