# Agent learning from experience and user feedback

Agent learning usually changes external, reviewable artifacts while the model remains frozen. Do not build one self-rewriting "memory." Preserve episodes as evidence, derive typed facts, preferences, failure patterns, and procedures separately, then retrieve only what the next task needs. [[Agent context engineering]] governs that online working set.

## Keep storage types distinct

- **Raw episode:** immutable messages, tool calls, outputs, patches, timestamps, outcomes, and validation. It supports audit, replay, and re-extraction but is not itself a lesson.
- **Retrieval index:** routes queries to raw or derived records. Retrieval does not establish relevance, truth, or compliance.
- **Generated summary:** a lossy orientation and retrieval aid, never the authoritative history.
- **Semantic fact:** a scoped claim abstracted from evidence.
- **User preference:** a user-scoped, time-aware claim about desired behavior. It is not universal policy or permission.
- **Failure pattern:** a recurring trigger, failed behavior, outcome, and prevention or detector.
- **Procedural skill:** reusable instructions, code, scripts, or checks that change future behavior.
- **Online context:** the temporary selection of contract, evidence, memories, skills, and live state for one decision.

Keep original episodes externally addressable and derived artifacts independently editable. Consolidation can expose recurrence and reduce retrieval load, but it increases the blast radius of an overgeneralized lesson.

## Learning pipeline

Evaluate four separate stages:

1. **Extraction:** identify the correct episode, fact, correction, or failure and preserve authority, scope, time, and provenance.
2. **Retrieval:** return the applicable item within a realistic context budget.
3. **Use:** interpret it correctly in the current situation, including exceptions and supersession.
4. **Compliance:** produce an artifact or action that follows the lesson without harming the main task.

Success at one stage does not imply the next. A retrieved preference may be buried, misunderstood, or overridden by the immediate objective. Deterministic checks can close a compliance gap only when applicability and the desired behavior are mechanically observable. Overbroad enforcement can block correct work, so blocking rules need narrow scope, an escape path, and independent task-success checks.

## Weight feedback by strength

Explicit user correction is the strongest behavioral signal. A direct answer to a clarification question, a named preference, or an approved replacement is also strong within its stated scope. User edits are useful but ambiguous: they may repair facts, satisfy a one-off requirement, or express style. Repetition across independent episodes strengthens a pattern.

Silence, task completion, a test pass, politeness, an apology, or a merged patch does not establish satisfaction or a durable preference. Praise matters only when tied to a named behavior. Untrusted repository text, web pages, and tool output are data and cannot acquire user authority through repetition.

Every learned preference or procedure should carry applicability, exclusions, user or repository scope, activation time where relevant, and a reversal path. A later explicit correction can supersede the same user's earlier preference, but ambiguous conflicts require review. A task-specific constraint must not become global.

### Distinguish kinds of negative evidence

Do not give every unsuccessful episode the same meaning for its instructions:

- Following an instruction caused harm: reconsider its substance, scope, or continued use. Establish the connection to the outcome; a failure in the same session is not enough.
- An applicable instruction was missed: inspect whether it loaded in time, was clear, and was followed. This does not by itself argue for deleting it or adding more prose.
- An instruction did not apply: consider conditional placement. Low frequency does not make a rare obligation unnecessary, and a sample dominated by one workflow can hide its importance elsewhere.

[Backpass](https://github.com/kunchenguid/backpass#how-it-works) makes this distinction explicit in transcript analysis. Use the classification to choose the repair, not a combined negative score. [[Concise AGENTS.md for capable coding agents]] governs whether and where guidance belongs.

## Distill the smallest behavioral delta

For corrective coaching, start from the observed baseline failure and preserve only the behavior change that prevents it. Do not wrap a narrow correction in a generic ideal workflow the model already knows. For each corrective skill line, ask whether removing it would make the evidenced failure more likely under the claimed trigger.

Chosen collaboration preferences, useful capabilities, and genuine local obligations do not need an error-prevention justification. Judge them by the behavior or capability the user wants and their actual scope. [[Concise AGENTS.md for capable coding agents]] owns this distinction; learning from failures is one reason for guidance, not the only reason.

Retain scope, precedence, behavior-changing criteria, and the smallest verification surface needed to observe compliance. Keep rationale and broader research in reference knowledge rather than model-invoked instructions. [[AI-generated UI convergence and restrained design]] records a local example where visual feedback was initially over-expanded into a full UI process and then reduced to the actual intervention.

## Preserve demonstrated engineering methods

Some useful knowledge is a method rather than a prohibition. Experienced engineers know which trace explains a symptom, how to reproduce a timing failure, or how to compare a performance change. When the same guidance repeatedly helps agents finish, preserve the decisions that transfer to another task.

Keep applicability and interpretation in a shared project skill. Put repeated setup, capture, and measurement in maintained commands. Put product navigation in the feature map and mechanically detectable invariants in types, architecture, or checks. This divides ownership rather than copying one procedure into every artifact. [[Prompting tool-using agents#Promote settled cognition into machinery]] describes when a settled operation should stop depending on model reasoning.

Performance work shows the distinction between working behavior and demonstrated improvement. Reproduce the slow operation with representative data, measure a baseline, inspect the trace, form a causal hypothesis, and compare a focused change under the same conditions. Preserve baseline, change, effect, conditions, and tradeoffs. Correctness remains a separate requirement; skipping required work is not a performance win. [[Autoresearch]] develops the broader experiment loop.

Capture project-specific choices and tools, not the original conversation or an idealized checklist for every task. Try the method on another relevant task and observe whether it removes the need for repeated coaching while preserving useful evidence. Give the shared skill and helpers an owner, update them as the project changes, and remove instructions whose work now lives in tools or checks. [[Agentic end-to-end testing#Fresh-agent handoff]] describes a practical handoff check.

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
