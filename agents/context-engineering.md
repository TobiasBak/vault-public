# Context engineering

Context engineering controls what the model sees at each inference. The **working set** is a small, lossy view for the next decision. The **system of record** (repo files, task records, raw tool output, checkpoints, traces) is what that view is rebuilt from. Judge by correctness and recoverability, not token count: one missing governing constraint costs more than several extra files.

## Choosing context

- Retrieve what changes the outcome, a decision, authority, or the evidence of success. Topical similarity isn't enough. Performance work needs the operation, baseline, conditions, and target; architecture work needs owners, contracts, and why earlier choices were made.
- Stored knowledge needs a retrieval route that fires before the decision. When improving an agent setup, inspect active instructions and triggers, not just reference notes.
- Advertised context size is not usable size, and the failure is task-shaped rather than general. Retrieval from a noisy pile, aggregation across many items and multi-hop reconciliation degrade before the window fills; direct work on a handful of files does not. That claim comes from long-context benchmarks on older models — re-check it against the current generation rather than inheriting it. Cached tokens still spend budget either way.
- **Context bloat is mainly an economics problem now** (Tobias, 2026-10-25): with good compaction, reading a marginal file or ingesting raw, uncleaned tool output costs tokens and wall time, not correctness. Quality is governed by whether the deciding constraint is present, not by volume, which is why the measurement below shows doubled model time with no quality loss. Two quality failure modes remain live and are not volume problems: an irrelevant rule that constrains judgment, and the task shapes above where cross-item comparison genuinely degrades.
- Even a short irrelevant rule can constrain judgment. Optimize for useful information, not minimum tokens or maximum procedure.
- Long-lived sessions get slower past ~300k context. 2026-10-20, Pi Sol 6.1 high, orderready, the same three routine tasks (two small implementations, one code-reading investigation) run by a fresh session per task, a lead at 200–310k and a lead at 380–480k:

  | Variant | Model time | Wall time | Cache read | Requests | s/request |
  |---|---|---|---|---|---|
  | Fresh per task | 550 s | 831 s | 4.0M | 87 | 6 |
  | Lead, 200–310k | 613 s | 880 s | 8.7M | 35 | 18 |
  | Lead, 380–480k | 1,126 s | 1,300 s | 14.6M | 40 | 28 |

  Leads batch work into fewer requests, so around 200k the cost is a wash; around 400k model time doubles while cache reads roughly quadruple. Quality did not drop: the long-lived lead's diffs were the smallest and were the ones landed — the evidence for reading this as a cost curve, not an intelligence curve. An earlier review-plus-test round (one run each) matched this: 141 s of model time fresh, 427 s at about 360k. Limits: one run per variant per task, the same host and time window, and task order differed between the leads and the fresh sessions.
- Tobias prioritizes prefix caching (2026-10-11). Confirm context changes using actual prefix-cache usage and whole-task cost per successful result, separating warm-up from steady long runs. Neither a 97% cache hit rate nor fewer visible tokens alone proves a win; count cache churn, compaction and output too.

## State tiers

| Tier | Contents | Handling |
|---|---|---|
| Always-active contract | Objective, hard constraints, authorization, acceptance gates | Keep explicit; never trust a summary for these |
| Working set | Current step, nearby code, recent failures, selected evidence | Replace as work moves |
| Durable project state | Base revision, changes, decisions, validation results, risks | Versioned records |
| Evidence archive | Full logs, sources, traces, diffs | Stable references, narrow reads |
| Scratch | Tentative hypotheses, superseded plans | Let expire |

## Continuation

Don't tune Pi compaction; use stock (Tobias, 2026-10-14). Earlier native compaction at 70k cost $0.98 vs $0.70 at 90k, one run each, neither halving peak context; a structured summary (goal / decisions / failed attempts / working set) at 50k used 73 vs 49 requests and cost $1.38 vs $0.82 for stock; epoch pruning cost 79% more over 6 stock vs 6 treatment runs ([issues #2](https://github.com/TobiasBak/pi-workspace-view/issues/2), [#4](https://github.com/TobiasBak/pi-workspace-view/issues/4), [#8](https://github.com/TobiasBak/pi-workspace-view/issues/8); [results PR #15](https://github.com/TobiasBak/pi-workspace-view/pull/15)). Summary compaction is lossy. It drops details, confuses attempted with completed work, revives stale decisions, and can duplicate effects around unfinished tool calls; repeated summaries compound the drift. Codex's experimental notes plus searchable history avoid that (see [Codex operations](codex-operations.md)). Native continuation never replaces repository state. During parallel work, reproduce a reported failure against current file bytes and verify the imported module's path. A delayed report or loaded module can describe code that another agent already replaced.

When a handoff must survive independently, a checkpoint holds:

- objective, non-goals, invariants, permissions, acceptance gates
- base revision and worktree identity
- completed milestones with evidence
- consequential decisions and who made them
- exact failures, with pointers to raw output
- remaining work in order, with one concrete next action
- open questions and escalation conditions

Keep it a snapshot, not a diary. Checkpoint at validated milestones, subsystem switches, and handoffs. Make retried mutations idempotent.

## Retrieval and tool output

- Orient first, then search narrowly and read narrow ranges. Load whole artifacts only when needed. Summaries should point to originals, not replace them.
- Tool results should return stable IDs, source location and revision, truncation status, and how to expand. Return selected matches and actionable errors rather than whole logs or API responses.
- Use host filtering or [programmatic tool calling](orchestration.md#programmatic-tool-calling) for joins, ranking, and aggregation that need no model judgment.
- Limit failures must name the budget, its limit, the actual value, and the fix. Silent truncation removes the evidence an agent needs to recover.
- Conditional detail needs an applicability cue and a retrieval action. If agents keep missing material, sharpen the pointer before inlining it.

## Skills as conditional context

A discoverable skill's description is always in context as a trigger. A loose match loads unnecessary procedure and displaces a simpler response. Judge each skill by what it adds over the model and host, how precise its trigger is, and what a false activation costs. Tobias wants every global skill model-invoked so agents find relevant workflows without him remembering skill names. Keep triggers precise rather than hiding skills behind explicit invocation. Knowledge that needn't activate itself belongs in retrievable notes.

Hosts expose only each skill's `name`, `description`, and path until it is selected, so the front-loaded `description` is the whole discovery surface. Codex's optional `agents/openai.yaml` adds display name, starter prompt, and `policy.allow_implicit_invocation`; Pi and Claude Code ignore it and use `disable-model-invocation` in `SKILL.md` instead, so explicit-only skills need both. Naming the skill explicitly (`$name`) gives deterministic selection.

## Text as images

Rendering text as images can cut metered tokens, but the compression is lossy, model-specific, and unverified locally. Upload and vision latency, lost cache reuse, retries, and OCR-like errors (punctuation, indentation, page breaks, small fonts) can erase the saving. Never put instructions, tool protocols, code, paths, IDs, or numbers in pixels, and keep the exact text retrievable. Use it only if representative trials show equal correctness at lower cost per successful task.
