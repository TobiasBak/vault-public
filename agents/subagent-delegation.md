# Subagent delegation

An agent does its own work: reading, research, exploration, design, implementation, tests and verification. Tobias's own outcome (2026-10-25): he gets more done, more accurately, with one agent than with an orchestrator in most cases; the rule began as 2026-10-24 (agents spawning far too many subagents). Compaction summarizes work already done; a brief is written before the work, so it cannot contain what the parent hasn't discovered yet. [Dotfiles](../projects.md#dotfiles) owns the global rule; this note covers how to divide work where dividing is allowed. Follow [compute routing](compute-routing.md) for model roles and effort.

recheck-after: 2027-01-24

## Who divides

Tobias, 2026-10-25: agents do their own work by preference, but any top-level agent whose large task divides into independent packages may delegate them to a strong model, and each delegate does all of its package itself. He never wants explorer-style agents; review subagents are fine. No subagent runs on Opus: there is no quota for it.

- **Top-level agents with a large, divisible task:** packages that are independent and testable on their own. Coordinators such as the [chief of staff](../.agents/skills/chief-of-staff/SKILL.md) work this way by design.
- **Broken or important work stays with the agent Tobias talks to** (Tobias, 2026-10-24): it does the work itself, coordinator or not. An agent working directly with Tobias is judged on responsiveness as well as model quality (Tobias, 2026-10-25): its latency is part of its fitness, so choose a conversational agent for the pace of the conversation, not only the score. Delegation is what buys capability without spending that responsiveness, not a way to reuse the same model everywhere.
- **Delegates:** never delegate further.
- **Never:** explorer, research, search or mapping agents. A broad search, many files, a long task or a big context is not a reason to delegate. Host prompts and skills that suggest them (Claude Code's `Agent`/Explore, vendored `grilling`, `deep-research`) lose to this rule.
- **Always allowed:** review subagents, each with a stated scope and blocking bar, reporting findings without delegating further. Protected surfaces a repository declares require one, and open-ended review/fix loops stay out ([code review](code-review.md#reviewers)).

## When a specialist earns its own context

Anthropic's Applied AI team (2026-10-22, several deployments): one model in one context window running an open-ended tool loop, procedure in skills and hard limits in tools, beat both one-prompt and orchestrator-subagent designs on quality, usually cheaper and faster. It keeps a subagent for three cases only: the loop measurably degrades on the task, work needs parallel fresh contexts that can be discarded, or tool choice and instructions conflict. Routers, planners, intent classifiers and per-team domain agents fold in, because shared context beats lossy summaries and each hop re-sends degraded detail. It names the usual failure as over-engineering: designs stacking an intent classifier, a fixed reasoning pipeline, segment buckets and an orchestrator where a clear system prompt, 4-5 thin data tools and firm output guardrails covered most cases. Divide by context, never by problem type or team. The model that writes the plan should carry it out, so it can change the plan mid-turn; a planner agent can't. Its failure list (subagent sprawl, frankenprompt, per-team evals, one customer at ~2x the runtime) is [Conway's law](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop) in an agent tree, and rigid multi-agent structure blocked migrations to better models.

Scope: advice for one product agent serving many users, from unnamed anecdotes; the rule above stays stricter. **Capability evidence expires with the model generation; mechanism doesn't** (Tobias, 2026-10-25: current models make most prior model knowledge obsolete).

- **Expired, kept as history:** the 2025 result where multi-agent beat single-agent Opus 4 by 90.2%. Its lesson survives as economics: the win cost ~15x chat tokens against 4x, and token usage explained most of the variance, so any architecture claim needs an equal-budget comparison ([benchmark trust](benchmark-trust.md)). "Coding has fewer parallelizable subtasks" was true of that generation, not a claim about this one.
- **Mechanism, still binding:** a handoff is a summary, so it loses detail whatever writes it; a second loop costs another call and another wait; actions carry implicit decisions, so parallel writers on differing assumptions produce inconsistent work. Capability reduces how often a second window is needed; it cannot make a summary lossless.
- **The deciding variable:** separable breadth (independent paths compressed back, as in search) versus interdependent work making shared decisions. Capability moves the boundary toward one loop.
- **Cognition's rule** (2025-06), share context and full traces and never run parallel multi-agents, argues from decisions, not model ability, so it still holds.

Bloat is a cost curve, not an IQ curve ([context engineering](context-engineering.md)), so a large window alone doesn't justify splitting: a subagent pays its own tokens and nested loop. A fresh context per task is also not a subagent — a new top-level session keeps one task in one window at no handoff cost. A review subagent is the deliberate exception, refused the author's narrative on purpose ([code review](code-review.md)).

**Folding a specialist:** build a task-completion eval first (ten golden examples is enough), then fold the most-used specialist, turning its prompt into a skill and its API calls into tools, and merge specialists that chain, share data or are called together. A kept specialist is a tool the main loop calls with a shared response schema, not a handoff. Read which tasks flipped, not the total ([benchmark trust](benchmark-trust.md)).

## How to split

Each delegate does the same job as a primary agent: it owns one whole outcome end to end, does everything itself and never delegates further. Never hand out research, exploration or mapping slices, and never split one chosen design across agents.

- Split by dependencies, ownership and independently testable behavior, not by file count. Keep tightly coupled files with one owner.
- Broad migrations: serial validated milestones, never fan-out writers.
- A unit is too small when setup dominates and too large when it needs the parent's full context recreated.

## Context lifespan

Follow-up outcomes get a fresh delegate; never add phases by steering or auto-resuming a finished one.

**30-minute notice** (Tobias, 2026-10-24): git-at-home's `t3/delegate-notice.patch` tells the parent once when a `delegate_task` child has run 30 minutes, and tells it to find why from the child's activity rather than restart a healthy task. CoS teams are top-level threads and get no notice; the census covers them.

When a delegate stops unfinished, its [continuation checkpoint](context-engineering.md#continuation) is unfinished work with an explicit next action, not a delivery claim. Preserve live job ownership and confirm the old writer has stopped before replacing it.

## Handoff

State the goal and deliverable, the minimum context with exact evidence locations, decisions already approved, permissions and side-effect limits, success criteria, output shape, and when to stop or escalate. Let the child choose its own procedure. Pass reduced inputs, not the parent transcript, and get back a compact result or an artifact reference.

- Word race and robustness reviews neutrally: describe the contract and ask whether it holds. On 2026-10-04 OpenAI's cyber filter killed a Pi Sol review briefed to "try to break the invariant", "hide the worker" and run "fork-heavy load"; reworded as contract checks it ran clean. Salvage partial artifacts from the child's output directory before re-delegating.
- Use gah for isolated candidate work; it gives each child its own workspace. Never create extra Git worktrees, clones or private tool trees. Dotfiles and vault remain plain checkouts with explicit writer ownership. Run `uv` from the assigned workspace root; copying a candidate's venv or entrypoints preserves absolute shebangs and can write back into the wrong checkout.
- Removing an old Git worktree deletes its gitignored files too, such as `.local/` receipts and evidence archives; retain needed evidence first.

## Authority and shared state

- The orchestrator owns requirements, decomposition, open decisions, integration, and acceptance. Children escalate any unapproved product, architecture, or scope choice.
- Never grant a child standing authority to extend a vocabulary, schema, or format "as needed". Sol uses it on every obstacle: a 2026-10-09 corpus conversion told to "add the minimal matcher without stopping" grew 19 matchers and turned expected-output files into an assertion language. Give the closed set, and make an extension a stop.
- Scope every stop condition to the item that hit it: park that item, finish the rest, report parked items at the end. Sol reads a bare "STOP and report" as halting the whole round; on 2026-10-09 a rewrite with 9,348 inventory items stopped on the first one and changed nothing. Stop the round only past a stated parked-item threshold.
- One writer per shared state. Gah owns workspace isolation and child integration. In plain shared checkouts, parallel writers must own disjoint files, including lockfiles, generated code and migrations.
- Inspect diffs and artifacts, not just reports.
- Check repository visibility through the host API before applying public-publication rules. A GitHub URL or authenticated `ls-remote` doesn't establish visibility; private pushes need no public-push exception (Tobias, 2026-10-11).
- Before declaring delegated work stalled, check file mtimes recursively (`git status` paths, not directory mtimes) and live `pi` processes (`pgrep -x pi`); a Pi parent's own subagents run in-process and never appear as T3 children. On 2026-10-04 a triage misread two live writers as stalled, and its "resume" spawned colliding writers.
- To stop a stray writer, kill its PID from `pgrep`. `pkill -f <pattern>` also matches and kills the shell running it (exit 144), so the rest of the command never runs.
- State landing authority in the task. In repos Tobias owns, agents land their own changes under the [delivery policy](../tobias/preferences.md#delivery-and-releases), using `gah merge` in gah workspaces. Agents land staging promotions autonomously. Production merge, deploy, publish and rollback require Tobias's explicit instruction for that action.
- Never `git commit` in a gah workspace. gah ignores commits made there and tracks the working tree against its recorded base; `gah merge --message` makes the landing commit. A forward, including the one inside `gah merge`, moves `HEAD` to the new base and leaves the change uncommitted, with new files untracked. On 2026-10-29 agents that had committed misread this: `format-patch` captured main's commit, a stash drop discarded the work, and `git diff` missed untracked files. Agents launched outside gah's shims never see its workspace explanation, so brief them on this. Read the change with `git add -N . && git diff`.
- Give a Codex delegate one package per brief. Twice on 2026-10-29 a Codex child given several packages landed one increment and reported done; one package each finished.
- A Pi child reads steering only between tool calls, so a long blocking command ignores it until it exits; to cancel now, `t3_thread_interrupt` or kill the process, then steer. On 2026-10-04 a "skip the Windows run" steer sent a minute into a 60-minute qualification run changed nothing.
- Wait only on correctness-critical results. Schedule on events rather than in barrier batches, and cancel optional work once the evidence suffices.
- Workers verify their own boundary; the orchestrator runs integration validation once. Report blocked shared tooling instead of having every worker investigate it.
- Review handoffs follow [code review](code-review.md). Keep the reviewer independent of the author's narrative. Don't impose a fixed scout, planner, implementer, reviewer pipeline.

## Compute routing

Model roles, targets and effort live in [compute routing](compute-routing.md), including the T3 inheritance trap and the routing hook. Judge delegation by correctness, latency, cost per success including retries, duplication, and recovery from failed children.

## T3 Code feedback

- Before restarting or updating T3, follow the [restart check](../software/t3-code-operations.md#service-restarts). [T3 operations](../software/t3-code-operations.md) also covers thread discovery, workspaces, secrets and webhooks.
- Orchestrator V2 separates deliberate progress messages from automatic completion delivery. Children feed findings to an active parent with `t3_thread_send` (`mode: "steer"`; `auto` only for an idle recipient), and the parent updates contracts the same way. These exchanges are model-chosen, not a fixed pipeline ([V2 MCP contract](https://github.com/pingdotgg/t3code/blob/8ed276c246b6/docs/orchestration-v2/orchestrator-mcp-server.md#t3_thread_send)).
- A parent's plain-text reply to a child's relayed progress message reaches nobody. Coordinate running children with `t3_thread_send` (`mode: "steer"`) to their `childThreadId`; on 2026-10-07 an overnight run lost several replies this way.
- Agent messages occupy the conversation's `user` role but retain `createdBy: "agent"` and `senderThreadId`. A user-role steering entry alone is not evidence that Tobias gave the instruction.
- Completion notifications are server-generated, distinct from progress messages, and tell the parent to read the result with `task_status`, which acknowledges delivery. V2 can wake an idle parent when children finish, so foreground completion doesn't mean delegated work is done. See the [V2 release notes](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610).
- `task_cancel` interrupts only the direct child. Grandchildren it delegated keep running and can sit on approval prompts; interrupt them by thread with `t3_thread_interrupt` (seen 2026-10-04, nightly `0.0.46-nightly.20261004.2644`).
- Tobias's agents always run full-access. Put limits like read-only in the task text; an approval mode chosen as a guard stalls the child. For Claude parents the dotfiles hook rewrites every `delegate_task` call to `runtimeMode: "full-access"` (verified: requested `approval-required`, child ran `full-access`).
