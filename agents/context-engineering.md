# Context engineering

Context engineering controls what the model sees at each inference. The **working set** is a small, lossy view for the next decision. The **system of record** (repo files, task records, raw tool output, checkpoints, traces) is what that view is rebuilt from. Judge by correctness and recoverability, not token count: one missing governing constraint costs more than several extra files.

## Choosing context

- Retrieve what changes the outcome, a decision, authority, or the evidence of success. Topical similarity isn't enough. Performance work needs the operation, baseline, conditions, and target; architecture work needs owners, contracts, and why earlier choices were made.
- Stored knowledge needs a retrieval route that fires before the decision. When improving an agent setup, inspect active instructions and triggers, not just reference notes.
- Advertised context size is not usable size. Retrieval, multi-hop reasoning, and aggregation degrade before the window fills, and cached tokens still occupy attention.
- Even a short irrelevant rule can constrain judgment. Optimize for useful information, not minimum tokens or maximum procedure.

## State tiers

| Tier | Contents | Handling |
|---|---|---|
| Always-active contract | Objective, hard constraints, authorization, acceptance gates | Keep explicit; never trust a summary for these |
| Working set | Current step, nearby code, recent failures, selected evidence | Replace as work moves |
| Durable project state | Base revision, changes, decisions, validation results, risks | Versioned records |
| Evidence archive | Full logs, sources, traces, diffs | Stable references, narrow reads |
| Scratch | Tentative hypotheses, superseded plans | Let expire |

## Continuation

Summary compaction is lossy. It drops details, confuses attempted with completed work, revives stale decisions, and can duplicate effects around unfinished tool calls; repeated summaries compound the drift. Codex's experimental notes plus searchable history avoid that (see [coding models](coding-models.md#astra-specifics)). Native continuation never replaces repository state.

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

A skill's description is always in context as a trigger. A loose match loads unnecessary procedure and displaces a simpler response. Judge each skill by what it adds over the model and host, how precise its trigger is, and what a false activation costs. Explicit-only invocation suits deliberately chosen modes. Knowledge that needn't activate itself belongs in retrievable notes.

Hosts expose only each skill's `name`, `description`, and path until it is selected, so the front-loaded `description` is the whole discovery surface. Codex's optional `agents/openai.yaml` adds display name, starter prompt, and `policy.allow_implicit_invocation`; Pi and Claude Code ignore it and use `disable-model-invocation` in `SKILL.md` instead, so explicit-only skills need both. Naming the skill explicitly (`$name`) gives deterministic selection.

## Text as images

Rendering text as images can cut metered tokens, but the compression is lossy, model-specific, and unverified locally. Upload and vision latency, lost cache reuse, retries, and OCR-like errors (punctuation, indentation, page breaks, small fonts) can erase the saving. Never put instructions, tool protocols, code, paths, IDs, or numbers in pixels, and keep the exact text retrievable. Use it only if representative trials show equal correctness at lower cost per successful task.
