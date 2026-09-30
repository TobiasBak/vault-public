# Agent context engineering

Context engineering controls what a model sees at each inference: selection, order, presentation, retention, and removal. [[Prompting tool-using agents]] defines the task contract; context engineering keeps it, relevant evidence, tools, and execution state usable throughout the task.

The **working set** is a small, metered, lossy view for the next decision. The **system of record** holds repository files, task records, raw tool artifacts, checkpoints, and traces from which that view can be rebuilt.

## Decide what context matters

Retrieve information that changes the outcome, a decision, authority, or evidence of success; topical similarity is not enough. The [[Prompting tool-using agents#Task contract|task contract]] identifies what the agent must understand, decide, do, and demonstrate. Preserve the meaning and scope of accepted decisions, rationale, preferences, domain distinctions, constraints, current state, and unresolved questions.

The goal directs retrieval; retrieved knowledge can clarify its meaning. Performance work needs the user operation, baseline, measurement conditions, and required improvement. Architecture work needs owners, contracts, and reasons earlier choices were accepted or rejected. Resolve what evidence establishes and bring material gaps or conflicts to the user without requiring a formal specification.

Stored knowledge needs an owner, scope, and retrieval route that reaches the agent before the relevant decision. When improving an agent setup, inspect active instructions and retrieval routes, not just reference notes. [[Concise AGENTS.md for capable coding agents#Placement and authority]] covers placement in instructions, conditional guidance, references, or executable protection.

## State tiers

Treat state according to how it must survive:

- **Always-active contract:** objective, hard constraints, authorization, acceptance gates, and governing repository rules. Keep these explicit rather than trusting a generated summary.
- **Current working set:** the immediate step, nearby code, recent failures, selected evidence, and callable tools. Replace material as the locus of work moves.
- **Durable project state:** base revision, changed artifacts, decisions, progress, validation results, known failures, and unresolved risks. Store this in versioned or otherwise stable records.
- **Evidence archive:** full logs, source documents, traces, diffs, and test output. Keep stable references and retrieve narrow ranges when needed.
- **Ephemeral scratch:** tentative hypotheses and superseded plans. Let these expire unless they changed a decision or exposed a reusable failure.

External artifacts need stable identities and timely retrieval. Keep short orientation alongside authoritative originals for quick recovery and exact inspection.

## Usable capacity

Advertised context capacity is not reliable usable capacity. Retrieval, multi-hop reasoning, and aggregation can degrade before the nominal window fills. Tool definitions, outputs, images, examples, and repeated instructions consume attention and tokens. Caching may reduce cost or latency, but cached material still occupies context.

Relevant constraints and evidence can improve work; irrelevant, repeated, or competing rules consume attention and can conflict. Even a short instruction can constrain judgment unnecessarily when the model or host already supplies the behavior. Optimize useful information and intended collaboration, not minimum tokens or maximum procedure. [[Concise AGENTS.md for capable coding agents]] owns instruction admission.

For explicit context maintenance, use validated milestones, subsystem switches, handoffs, or changes that invalidate restart instructions. Native host management can own window transitions without a second mandatory checkpoint process.

## Conditional context and activation

A skill combines conditional context with an activation policy. Its model-visible description is an always-active retrieval cue, not a passive catalog entry. A weak match can load unnecessary procedure into the working set and displace a simpler response.

Automatic exposure lets agents discover specialized capabilities or chosen behavior. Judge what the skill adds beyond the model and host, trigger precision, and mistaken-activation cost. Broad triggers may increase recall while reducing precision. Use representative work for meaningful activation uncertainty; not every skill or removal needs a formal failure study. Chosen style and corrective coaching have different purposes.

Explicit invocation suits deliberately selected modes: it removes default exposure but makes the human discover and select the skill. Its body still costs context when invoked. Knowledge that need not activate itself belongs in retrievable references; omit procedure that adds no value over default behavior.

## Context continuation and checkpoints

Summary compaction is lossy continuation, not durable truth. It can lose later-important details, confuse attempted and completed work, revive stale decisions, or duplicate effects around unfinished tool calls. Repeated summaries amplify drift.

Codex's experimental notes-and-searchable-history system retains notes across windows and searchable earlier messages and outputs. [[Working with GPT-6 Astra]] records availability and inspected local configuration. Native continuation can replace duplicate manual context maintenance, not authoritative repository state.

For hosts that rely on summary compaction, or a handoff that must survive independently of the originating session, a restart-ready checkpoint can retain:

- the objective, non-goals, invariants, permissions, and acceptance gates;
- the base revision and current worktree or artifact identity;
- completed milestones with validation evidence;
- unfinished or deliberately incomplete state;
- consequential decisions, rationale, still-relevant rejected alternatives, and who authorized them;
- exact failures with pointers to raw output;
- remaining work in dependency order, including one concrete next action;
- unresolved questions, safety boundaries, and escalation conditions.

Keep only needed handoff fields in a small snapshot with retrievable evidence, not a diary. Checkpoints and native notes do not establish current repository state. Use idempotency or deduplication where retries or context transitions can repeat mutations.

## Retrieval and tool results

Start with orientation, then focused search and narrow source ranges; load complete artifacts only when needed. Summaries, symbols, paths, timestamps, and extracted facts should lead to originals, not replace them. Inline universally required material and disclose branch-specific detail conditionally. Pointers need an applicability cue and retrieval action. If agents repeatedly miss required material, sharpen the pointer before inlining the reference.

Return stable identifiers, source location and revision, truncation status, enough context to interpret a hit, and expansion routes. Supply selected matches, relevant fields, actionable errors, and raw-output references for the next decision, not complete repositories, logs, or API responses.

Use host filtering or [[Programmatic tool calling]] for deterministic joins, ranking, and aggregation that need not enter model context. Retain final-verification evidence. Optimize task success and invariant retention, not token reduction: one omitted governing constraint can cost more than several extra files.

## Repository retrieval surface

Context assembly begins before the harness runs. Repository names, types, tests, and domain language determine what lexical searches can retrieve. [[Search-driven code discoverability]] owns the naming practices and compact query maps that let an agent reach authoritative code without loading a prose copy of the implementation.

Limit failures should name the resource or budget, configured limit, actual or requested value, and known location or corrective route in domain terms. Silent clamping, truncation, or blank failures remove the evidence an agent needs to recover.

## Context isolation

A subagent isolates context through a bounded contract, reduced inputs, private exploration, and a compact result or durable artifact reference. Full parent transcripts or child traces add cost. [[Subagent delegation]] covers task shape, handoffs, and authority.

Keep the active contract concise, durable state authoritative, and lossy views linked to originals so a fresh session can recover. Judge correctness and recovery, not window utilization.
