# Prompting tool-using agents

Prompts for capable tool-using agents should define a task contract and leave implementation choices to the model. Describe the destination rather than prescribing every intermediate step.

## Task contract

A task may need some of the following information when the request, active instructions, or repository do not already supply it. These are prompts for finding consequential gaps, not required fields to restate in every request:

- **Outcome:** the user-visible result.
- **Success criteria:** what must be true before completion.
- **Constraints:** permissions, safety, evidence, business rules, and side-effect limits.
- **Tools:** relevant capabilities and prerequisite lookups.
- **Output:** required content, structure, evidence, and validation.
- **Stop rules:** when to retry, use a fallback, ask, abstain, escalate, or finish.

Treat completion criteria as two independent choices: observability and demanded coverage. Make them checkable enough to distinguish done from not done; require exhaustive accounting only when omissions materially affect correctness, safety, or the stated outcome.

Reserve absolute terms for real invariants. Give criteria for judgment calls. An implementation request alone does not necessarily resolve a non-trivial product or architecture choice. If the prescribed approach conflicts with established boundaries or creates structural friction, surface that conflict and recommend the simplest coherent direction. Once a decision is explicitly resolved, execute it without reopening it unless new evidence makes it unsound.

## Tools provide capability, not cognition

Give agents capabilities reasoning alone cannot supply: access to external evidence, execution, deterministic validation, durable state, and enforced permissions or guardrails. Do not use tools to babysit a capable model with rigid plans, fixed workflows, or prescribed step-by-step cognition.

Procedural coaching ages as models and hosts improve. Retain it for a concrete unmet need, not merely because it once prevented a mistake. Chosen collaboration and genuine local obligations have different reasons to be explicit. Neither requires a prescribed reasoning process. [[Concise AGENTS.md for capable coding agents]] owns this distinction for durable instructions; [[Subagent delegation]] applies it to worker boundaries.

## Promote settled cognition into machinery

Spend model reasoning on uncertainty, exploration, semantic judgment, and exceptions. Repeatedly asking an agent to rediscover an already understood behavior repays input, latency, variance, and verification costs on every run. A prompt that usually produces the same known procedure is not yet automation. First decide whether that procedure is still needed; removing unnecessary coaching does not create an automation requirement.

When applicability and the desired outcome become mechanically observable, promote the behavior into the narrowest deterministic surface that can own it: ordinary code or an API for stable transformations, a tool or generator for reusable operations, a schema for structural constraints, and tests, lint, hooks, permissions, or CI for enforceable invariants. The agent can remain at the boundary to interpret ambiguous cases, investigate failures, propose new rules, and handle explicit exceptions. Deterministic machinery should return evidence and actionable errors rather than hide its decision.

Do not automate merely because one model produced the same answer twice. First establish a recurring meaningful pattern, a reliable detection signal, the acceptable false-positive and false-negative costs, and an escape path where legitimate exceptions exist. Compare task success and maintenance burden, not token reduction alone. After promotion, remove duplicated prompts and prose unless agents still need a concise pointer to the enforced contract.

## Autonomy and sequencing

State autonomy and approval boundaries once. Phrase user-controllable side effects as conditions such as “invoke only when the user allows it.” Treat a clear current request for the scoped action as that authorization and proceed without asking again. Ask only when the action was not clearly included, the target or scope is materially ambiguous, or a higher-priority non-overridable constraint applies. Do not turn a default-off action into an absolute prohibition when the user is allowed to activate it.

Parallelize independent reads or checks. Keep work serial when one result determines the next action or when tasks share mutable state. Resolve required retrieval before acting. An empty, partial, or suspiciously narrow result is not evidence that nothing exists; try a small number of meaningful fallback routes before concluding absence. See [[Subagent delegation]] when independent outcomes or context isolation may justify delegation.

Concurrency does not require another agent. A host can allow tool execution or a user question to remain pending while the same agent does independent work. Required answers and dependent results still block the actions that need them. Mid-turn steering changes the remaining task; it does not undo completed actions or automatically cancel running tools. [[Working with GPT-6 Astra]] records the current API and Codex distinctions.

## Make long-running tools cheap to supervise

Long-running tools should return concise progress, actionable failures, and a final result that identifies the inputs and checks performed. Retain full logs for diagnosis instead of streaming every successful check into model context. Bound failure excerpts and show where omitted output can be retrieved.

Keep one native process handle. Do independent work while the process runs; when its result is needed, use longer native waits that still allow progress updates and steering. Avoid combining process polls with repeated log reads or separate sleep calls. This improves the existing tool workflow without requiring a new monitoring service.

Judge efficiency by cost per successful task, not raw tool-call count. A batched call can contain many operations, and a poll may return useful evidence. Include retries, delegated work, cached input, and output in cost comparisons. Less console output alone does not establish lower total task cost.

## Evidence and verification

Define which claims need support and what evidence is sufficient. Distinguish retrieved facts from inference and surface source conflicts. Missing evidence does not establish a factual negative.

Useful verification depends on the artifact and risk: focused tests, type or lint checks, builds, smoke tests, real-use execution, or rendered visual inspection. Verification does not imply creating a new test suite. This knowledge does not require a verification paragraph in every prompt. Add explicit criteria where the task has a particular acceptance requirement or the active host leaves a consequential gap.

Reuse passing validation evidence when its source, environment, and validation inputs remain unchanged and it meets the required acceptance contract. Repeat checks when a change or new failure invalidates that evidence, not merely because another workflow section asks for validation. Keep focused development checks distinct from any required final full run.

## Simplify prompts first

When improving a prompt, compare it with the active model, host instructions, tools, and task. Remove repetition and unnecessary procedure without inventing a replacement. Use representative work when the effect of a change is uncertain and consequential, not as a prerequisite for deleting an obvious duplicate. Add only what communicates a chosen outcome, preference, local obligation, or concrete unmet need.

[[Concise AGENTS.md for capable coding agents]] governs durable instruction admission; this note governs the temporary task contract.
