# Agent context engineering

Context engineering is the harness policy for selecting, ordering, shaping, preserving, and retiring what a model sees at each inference step. [[Prompting tool-using agents]] defines the task contract; context engineering keeps that contract, the relevant evidence, tools, and execution state legible over a long trajectory.

The central distinction is between the **working set** and the **system of record**. Active context is a small, metered, lossy view assembled for the next decision. Repository files, task records, raw tool artifacts, checkpoints, and traces are durable state from which that view can be rebuilt.

## Decide what context matters

Information matters when it changes the intended outcome, a decision, an authority boundary, or the evidence needed to judge success. Topical similarity alone is not enough. Use the [[Prompting tool-using agents#Task contract|task contract]] to identify what the agent needs to understand, decide, do, and demonstrate. Relevant context includes accepted decisions and their rationale, applicable preferences, domain distinctions, constraints, current state, and unresolved questions. Retrieve enough to preserve their meaning and scope.

The goal directs retrieval, and retrieved knowledge can refine the understanding of the goal. A performance task needs the affected user operation, its baseline and measurement conditions, and the required improvement. An architectural choice needs the relevant owners, contracts, and reasons earlier choices were accepted or rejected. Resolve what existing evidence establishes; bring material gaps or conflicting requirements to the user. A task description need not become a formal specification to make these distinctions clear.

Storing a principle does not ensure it influences work. Important knowledge needs an owner, an appropriate scope, and a route into context before the decision it governs. When improving an agent setup, inspect the active instructions and retrieval routes as well as the reference notes. [[Concise AGENTS.md for capable coding agents#Placement and authority]] explains how to translate context knowledge into instructions, conditional guidance, references, or executable protection.

## State tiers

Treat state according to how it must survive:

- **Always-active contract:** objective, hard constraints, authorization, acceptance gates, and governing repository rules. Keep these explicit rather than trusting a generated summary.
- **Current working set:** the immediate step, nearby code, recent failures, selected evidence, and callable tools. Replace material as the locus of work moves.
- **Durable project state:** base revision, changed artifacts, decisions, progress, validation results, known failures, and unresolved risks. Store this in versioned or otherwise stable records.
- **Evidence archive:** full logs, source documents, traces, diffs, and test output. Keep stable references and retrieve narrow ranges when needed.
- **Ephemeral scratch:** tentative hypotheses and superseded plans. Let these expire unless they changed a decision or exposed a reusable failure.

External storage is useful only when artifacts have stable identities and are retrieved at the decision that needs them. Keep a concise orientation alongside authoritative originals: the summary speeds recovery, while the original supports exact inspection.

## Usable capacity

Advertised context capacity is not reliable usable capacity. At the current capability frontier, context remains scarce in attention, latency, and cost: retrieval, multi-hop reasoning, and aggregation can degrade well before the request exceeds the nominal window. Tool definitions, outputs, images, examples, and repeated instructions also consume attention and tokens. Prompt caching may reduce cost or latency, but it does not make the cached material disappear from context.

Additional context is not inherently harmful. Relevant constraints and evidence can improve work; irrelevant, redundant, or competing rules consume the same working set and can pull behavior in conflicting directions. Context design also determines how much judgment the agent can exercise. Even a short, clear instruction can steer work unnecessarily when the model or host already supplies the behavior. Optimize for useful information and intended collaboration, not minimum tokens or maximum procedural coverage. [[Concise AGENTS.md for capable coding agents]] owns this instruction-admission distinction.

In workflows that manage context explicitly, useful maintenance points include validated milestones, subsystem switches, handoffs, and changes that make restart instructions unsafe. A host with native context management can own window transitions; these boundaries do not imply a second mandatory agent-maintained checkpoint process.

## Conditional context and activation

A skill is a conditional context bundle plus an activation policy. A model-visible skill description is not a passive catalog entry: it is an always-active retrieval cue that competes for attention and can load a procedural body when the task only weakly matches. Once activated, that body joins the working set and can displace a simpler capable-model response.

Automatic exposure is useful when the agent should discover a specialized capability or chosen behavior without an explicit invocation. Its value depends on what it adds beyond the model and host, how well the trigger distinguishes relevant tasks, and the cost of mistaken activation. Broad triggers can raise recall while reducing precision. Use representative work to resolve meaningful uncertainty about activation; a formal failure study is not a prerequisite for every skill or removal. A skill encoding a chosen style has a different purpose from one correcting an old model weakness.

Explicit invocation removes default model exposure but makes the human responsible for discovery and selection; it does not make the skill body free once invoked. It suits deliberately selected modes. Put reusable knowledge in ordinary retrievable reference when it does not need to activate itself, and omit procedural context that adds no behavioral value over the model's default.

## Context continuation and checkpoints

Summary-based compaction is a lossy continuation mechanism, not durable truth. It can omit details whose importance appears later, blur attempted and completed work, revive stale decisions, or cause duplicate side effects around unfinished tool calls. Repeated summaries amplify drift.

Codex's experimental notes-and-searchable-history system offers another implementation. Notes survive across windows, and earlier messages and tool outputs remain searchable when a note omitted something. [[Working with GPT-6 Astra]] records availability and the inspected local configuration. Native continuation does not replace authoritative repository state, but it can remove the need to duplicate the host's context maintenance in manual task files.

For hosts that rely on summary compaction, or a handoff that must survive independently of the originating session, a restart-ready checkpoint can retain:

- the objective, non-goals, invariants, permissions, and acceptance gates;
- the base revision and current worktree or artifact identity;
- completed milestones with validation evidence;
- unfinished or deliberately incomplete state;
- consequential decisions, rationale, still-relevant rejected alternatives, and who authorized them;
- exact failures with pointers to raw output;
- remaining work in dependency order, including one concrete next action;
- unresolved questions, safety boundaries, and escalation conditions.

Use only the fields the handoff needs. Prefer a small structured snapshot plus retrievable evidence over a narrative diary. Neither a checkpoint nor native notes establish the current repository state. Where retries or context transitions can cross a mutation boundary, idempotency or deduplication prevents repeated effects.

## Retrieval and tool results

Use progressive disclosure: map or index first, focused search hits next, narrow source ranges after that, and complete artifacts only when necessary. Summaries, symbols, paths, timestamps, and extracted facts should add retrieval routes, not replace originals. Inline material required on every path and disclose branch-specific material. A pointer should encode a discriminating applicability condition and retrieval action, not merely name a target; if required material is repeatedly missed, sharpen the pointer before moving the full reference inline.

A useful result includes stable identifiers, source location and revision, truncation status, enough neighboring context to interpret the hit, and a route to more detail. Shape results around the next decision: selected matches, relevant fields, actionable errors, and references to raw output. Avoid dumping repositories, complete logs, or every API field into active context.

Use host-side filtering or [[Programmatic tool calling]] for deterministic joins, ranking, and aggregation when bulky intermediates need not reach the model. Keep evidence required for final verification. Retrieval should optimize downstream success and invariant retention, not token reduction alone: omitting one governing constraint can be worse than several extra files.

## Repository retrieval surface

Context assembly begins before the harness runs. Filenames, symbols, types, tests, error terms, comments, and domain documents determine which lexical searches reach useful evidence and how much irrelevant material enters the working set. Distinctive names, one spelling per concept, precise signatures, concept-named modules, behavior-named tests, and short rationale on owning definitions create stable retrieval handles. Generic aliases, `Any`-shaped boundaries, grab-bag files, and duplicated terminology force more search and inference.

Diagnostics are part of this retrieval surface. A breached limit should name the resource or budget in its owning domain terms, the configured limit, the actual or requested value, and the location or corrective route when known. Silent clamping, truncation, or blank failure removes the evidence and retrieval handles an agent needs to recover.

Repository context should act as a compact query map: define preferred terms, ownership boundaries, hazards, and routes to narrower authorities. Those terms should continue into code and tests so retrieval still works after the context document leaves the active window. It should not preload a prose copy of implementation. [[Search-driven code discoverability]] holds the design and reviewer guidance.

## Context isolation

A subagent isolates context only when it receives a bounded contract and reduced context, performs noisy exploration privately, and returns a compact result or durable artifact reference. Passing the full parent transcript or full child trace merely adds cost. See [[Subagent delegation]] for task shape, handoff, and authority rules.

Context remains reconstructable when the always-active contract is concise, durable state is authoritative, lossy views point back to originals, and every handoff can survive a fresh session. Judge the policy by completed-work correctness and recovery, not window utilization.
