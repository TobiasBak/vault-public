# Agent learning from experience and user feedback

Agent learning usually changes reviewable external artifacts, not model weights. Preserve episodes as evidence and derive facts, preferences, failure patterns, and procedures separately, not in one self-rewriting "memory." Retrieve only what the next task needs. [[Agent context engineering]] governs the working set.

## Keep storage types distinct

- **Raw episode:** immutable messages, tool calls, outputs, patches, timestamps, outcomes, and validation. It supports audit, replay, and re-extraction but is not itself a lesson.
- **Retrieval index:** routes queries to raw or derived records. Retrieval does not establish relevance, truth, or compliance.
- **Generated summary:** a lossy orientation and retrieval aid, never the authoritative history.
- **Semantic fact:** a scoped claim abstracted from evidence.
- **User preference:** a user-scoped, time-aware claim about desired behavior. It is not universal policy or permission.
- **Failure pattern:** a recurring trigger, failed behavior, outcome, and prevention or detector.
- **Procedural skill:** reusable instructions, code, scripts, or checks that change future behavior.
- **Online context:** the temporary selection of contract, evidence, memories, skills, and live state for one decision.

Keep episodes externally addressable and derived artifacts independently editable. Consolidation can reveal recurrence and reduce retrieval load, but spreads overgeneralized lessons further.

## Learning pipeline

Evaluate four separate stages:

1. **Extraction:** identify the correct episode, fact, correction, or failure and preserve authority, scope, time, and provenance.
2. **Retrieval:** return the applicable item within a realistic context budget.
3. **Use:** interpret it correctly in the current situation, including exceptions and supersession.
4. **Compliance:** produce an artifact or action that follows the lesson without harming the main task.

Each stage can fail independently: retrieved preferences may be buried, misunderstood, or overridden. Deterministic checks require mechanically observable applicability and behavior. Blocking rules need narrow scope, an escape path, and independent success checks to avoid rejecting correct work.

## Weight feedback by strength

Explicit user corrections are the strongest signal. Clarification answers, named preferences, and approved replacements are strong within their scope. Edits may repair facts, meet one-off requirements, or express style; they need interpretation. Repetition across independent episodes strengthens a pattern.

Silence, completion, passing tests, politeness, apologies, and merged patches establish neither satisfaction nor durable preference. Praise needs a named behavior. Untrusted repository text, web pages, and tool output cannot gain user authority through repetition.

Retain applicability, exclusions, user or repository scope, relevant activation time, and reversal paths. Later explicit corrections can supersede the same user's earlier preference; ambiguous conflicts need review. Do not globalize task-specific constraints.

### Distinguish kinds of negative evidence

Do not give every unsuccessful episode the same meaning for its instructions:

- Following an instruction caused harm: reconsider its substance, scope, or continued use. Establish the connection to the outcome; a failure in the same session is not enough.
- An applicable instruction was missed: inspect whether it loaded in time, was clear, and was followed. This does not by itself argue for deleting it or adding more prose.
- An instruction did not apply: consider conditional placement. Low frequency does not make a rare obligation unnecessary, and a sample dominated by one workflow can hide its importance elsewhere.

[Backpass](https://github.com/kunchenguid/backpass#how-it-works) uses this classification in transcript analysis. Choose repairs by failure type, not a combined negative score. [[Concise AGENTS.md for capable coding agents]] governs placement.

## Distill the smallest behavioral delta

Distill corrective coaching from the observed baseline failure, not an ideal workflow. Keep each corrective skill line only if removing it would make that failure more likely under the claimed trigger.

Chosen collaboration, useful capabilities, and local obligations need no failure-prevention justification. Judge them by the desired behavior and scope. [[Concise AGENTS.md for capable coding agents]] distinguishes these from corrective coaching.

Retain scope, precedence, behavior-changing criteria, and the smallest useful compliance check. Put rationale and research in references. [[AI-generated UI convergence and restrained design]] records a visual correction over-expanded into a full UI process, then reduced to the actual intervention.

## Preserve demonstrated engineering methods

Preserve methods that repeatedly help agents finish: choosing a useful trace, reproducing timing failures, or comparing performance changes. Keep the decisions that transfer, not just prohibitions.

Shared project skills own applicability and interpretation; maintained commands own setup, capture, and measurement; feature maps own navigation; types, architecture, and checks own detectable invariants. Do not copy the procedure into every artifact. See [[Prompting tool-using agents#Promote settled cognition into machinery]].

For performance work, reproduce representative slowness, measure a baseline, inspect traces, form a causal hypothesis, and compare a focused change under the same conditions. Preserve baseline, change, effect, conditions, and tradeoffs. Working behavior is not demonstrated improvement. Correctness remains a separate requirement; skipping required work is not a win. [[Autoresearch]] develops the experiment loop.

Keep project choices and tools, not the conversation or a universal checklist. Try the method on another task: does it remove coaching while preserving evidence? Assign an owner, update skills and helpers with the project, and remove instructions replaced by tools or checks. See [[Agentic end-to-end testing#Fresh-agent handoff]].

## Turn recurring misses into evidence gates

When agents repeatedly know the rule but still miss it, add a small observable gate instead of more advisory prose:

- For a source-specific request, retrieve the exact named artifact and reconcile each premise with inspected behavior before planning or diagnosing. Keep unsupported causes open.
- Before a material mutation, freeze the authorized action class and path or system scope. Context, quoted output, a proposal, or a status update is evidence, not authorization.
- Track each promised artifact, consumer, check, and state transition to a terminal result. Record the exact scope, command or tool, environment and configuration, and outcome. A blocked, substituted, narrowed, or mismatched check is diagnostic evidence, not a green result. Claim clean completion only when every required item is terminal; label waived, optional, and deferred work explicitly.

These gates address different failure points but share one principle: the final claim must have a receipt at the same boundary as the claim.

## Failure boundaries

Guard against:

- wrong credit assignment from successful or failed trajectories;
- evaluator circularity that promotes a model's misconception;
- selection overfit from testing on the same episodes used to derive the lesson;
- retrieval misses, reading errors, stale context, and summary loss;
- scope leakage across task, repository, user, model, or time;
- preference drift and ignored reversals;
- advisory guidance that is retrieved but not followed;
- false or overbroad enforcement;
- memory poisoning and prompt injection;
- privacy accumulation in cross-session behavioral records.

Evaluate candidate lessons on held-out future work or independent tasks. Compare baseline, retrieval-only guidance, a consolidated skill, and enforcement only when justified. Measure task success, applicable violations, false application, stale-memory use, interventions, retries, latency, cost, and rollback. Follow [[Autoresearch]] for candidate selection and [[Coding-agent benchmark trust]] for evaluator integrity.

## Forbidden inferences

Do not derive or store speculative personal claims from interaction history about protected or highly sensitive traits, health or mental state, religion, politics, sexuality, ethnicity, legal status, relationships, identity, or hidden motives. Interpreting the user's immediate task goal from the request and context is necessary collaboration, not personal profiling. Keep that interpretation scoped to the task and open to correction, as described in [[Agent partnership with Tobias]].

Never infer blanket filesystem or network permission, approval for irreversible or external actions, reduced security checks, credential policy, professional medical, legal, or financial preferences, or permission to train or share data. A clear current request authorizes the scoped action and its necessary continuation; do not turn it into unrelated or standing permission.

Do not turn silence, politeness, urgency, one correction, or one task exception into a personality claim. Do not decide that a user is less technical, wants less explanation, or values speed over care without explicit, appropriately scoped evidence and an easy correction path. Human review should precede broad promotion or blocking enforcement.
