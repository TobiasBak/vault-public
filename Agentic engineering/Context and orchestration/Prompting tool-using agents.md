# Prompting tool-using agents

Define the task contract and leave implementation choices to the model. Describe the destination, not every step.

## Task contract

Supply these only where the request, active instructions, or repository leave consequential gaps:

- **Outcome:** the user-visible result.
- **Success criteria:** what must be true before completion.
- **Constraints:** permissions, safety, evidence, business rules, and side-effect limits.
- **Tools:** relevant capabilities and prerequisite lookups.
- **Output:** required content, structure, evidence, and validation.
- **Stop rules:** when to retry, use a fallback, ask, abstain, escalate, or finish.

Choose observability and required coverage separately. Make completion checkable; require exhaustive accounting only when omissions materially affect correctness, safety, or the requested outcome.

Reserve absolutes for invariants and give criteria for judgment calls. An implementation request may leave material product or architecture choices unresolved. If the requested mechanism conflicts with boundaries or creates structural friction, explain the conflict and recommend the simplest coherent direction. Execute resolved choices; reopen them only on new conflicting evidence.

## Tools provide capability, not cognition

Tools should supply external evidence, execution, deterministic validation, durable state, and enforced permissions, not rigid plans or prescribed reasoning.

Keep procedural coaching for a current unmet need, not an old mistake. Chosen collaboration and local obligations have separate reasons to be explicit without prescribing reasoning. [[Concise AGENTS.md for capable coding agents]] owns durable instruction admission; [[Subagent delegation]] applies it to workers.

## Promote settled cognition into machinery

Spend reasoning on uncertainty, exploration, semantic judgment, and exceptions. Repeatedly rediscovering a known procedure adds input, latency, variance, and verification costs; it is not automation. First check whether the procedure is still needed. Removing unnecessary coaching requires no replacement.

When applicability and outcomes become mechanically observable, use the narrowest deterministic owner: code or APIs for transformations, tools or generators for operations, schemas for structure, and tests, lint, hooks, permissions, or CI for invariants. Agents still interpret ambiguity, investigate failures, propose rules, and handle explicit exceptions. Machinery should return evidence and actionable errors.

Two identical answers do not justify automation. Establish a recurring meaningful pattern, reliable detection, acceptable false-positive and false-negative costs, and an escape path for legitimate exceptions. Compare task success and maintenance burden, not just tokens. Remove duplicated prompts after promotion, retaining only needed pointers to the enforced contract.

## Autonomy and sequencing

State autonomy and approval boundaries once. A condition such as "invoke only when the user allows it" is satisfied by a clear current request for that action. Do not ask again or turn default-off behavior into an absolute prohibition. Ask when the action is not included, target or scope is materially ambiguous, or a higher-priority non-overridable constraint applies.

Parallelize independent reads and checks; serialize dependent work or shared mutations. Retrieve required knowledge before acting. Empty, partial, or suspiciously narrow results do not establish absence; try a few meaningful alternatives. [[Subagent delegation]] covers independent outcomes and context isolation.

One agent can do independent work while a tool or user question remains pending. Required answers and results still block dependent actions. Mid-turn steering changes remaining work; it neither undoes completed actions nor automatically cancels tools. [[Working with GPT-6 Astra]] records API and Codex distinctions.

## Make long-running tools cheap to supervise

Long-running tools should return short progress, actionable failures, and a final result identifying inputs and checks. Keep full logs outside model context; bound failure excerpts and link omitted output.

Keep one native process handle and do independent work while it runs. When the result is needed, use longer native waits that permit updates and steering. Avoid duplicate polling, log reads, or sleeps; no new monitoring service is needed.

Judge cost per successful task, not tool-call count or console volume. Batches contain multiple operations and polls can return evidence. Count retries, delegated work, cached input, and output.

## Evidence and verification

Define sufficient evidence for claims, separate facts from inference, and surface source conflicts. Missing evidence is not a factual negative.

Choose verification by artifact and risk: focused tests, type or lint checks, builds, smoke tests, real use, or rendered inspection. This requires neither a new suite nor a verification paragraph in every prompt. State criteria for particular acceptance requirements or consequential gaps in host guidance.

Reuse passing evidence when source, environment, inputs, and acceptance requirements still match. Rerun checks after invalidating changes or failures, not repeated workflow instructions. Keep focused development checks separate from required final full runs.

## Simplify prompts first

Compare prompts with the active model, host, tools, and task. Cut repetition and unnecessary procedure without replacements. Use representative work for uncertain, consequential changes, not obvious duplicates. Add chosen outcomes, preferences, local obligations, or concrete unmet needs.

[[Concise AGENTS.md for capable coding agents]] governs durable instruction admission; this note governs the temporary task contract.
