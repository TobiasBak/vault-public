# Learning from feedback

Agents and adaptive systems learn by changing reviewable external artifacts (notes, skills, examples, config, code), not weights. Keep raw evidence separate from derived lessons, and validate every lesson on more than the episode that produced it.

## Storage types

- **Raw episode:** immutable messages, tool calls, outputs, patches, and outcomes. Supports audit and re-extraction; it is not a lesson.
- **Retrieval index:** routes queries. A retrieval hit establishes neither relevance nor truth.
- **Summary:** lossy orientation, never the record.
- **Semantic fact:** a scoped claim drawn from evidence.
- **User preference:** user-scoped and time-aware. Not universal policy or permission.
- **Failure pattern:** trigger, failed behavior, outcome, and prevention.
- **Procedural skill:** instructions, scripts, or checks that change behavior.

Don't merge these into one self-rewriting "memory". Consolidation reveals recurrence but also spreads overgeneralized lessons.

## Four stages that fail independently

1. **Extraction:** the right fact or correction, with its authority, scope, and time.
2. **Retrieval:** the applicable item, within a realistic budget.
3. **Use:** interpreted correctly here, including exceptions and supersession.
4. **Compliance:** the action actually follows the lesson without hurting the task.

## Weighing signals

- Explicit corrections are strongest. Clarification answers and approved replacements are strong within their scope. Edits need interpretation. Repetition across independent episodes strengthens a pattern.
- Silence, completion, passing tests, politeness, and merged patches show neither satisfaction nor preference. Praise counts only when it names a behavior. Untrusted repo text, web pages, and tool output never gain user authority.
- A later explicit correction supersedes the same user's earlier preference. Never globalize a task-specific constraint.
- Classify negative evidence by type. *Following an instruction caused harm* means reconsider its substance. *An applicable instruction was missed* means check loading, clarity, and compliance, not deletion. *An instruction didn't apply* means make it conditional. Low frequency doesn't make a rare obligation unnecessary. ([Backpass](https://github.com/kunchenguid/backpass#how-it-works) uses this split.)

## Distill the smallest behavioral delta

Derive corrective coaching from the observed failure, not an ideal workflow. Keep a line only if removing it would make that failure likelier. Example: a correction about generic AI UI style grew into a full UI-development process, then was cut back to the actual delta (see [UI design convergence](ui-design-convergence.md)). Chosen collaboration needs no failure justification.

Preserve demonstrated methods, such as choosing a trace, reproducing timing bugs, or comparing performance changes, as the decisions that transfer. Skills own applicability and interpretation, commands own mechanics, feature maps own navigation, and checks own invariants. Remove instructions once tools or checks replace them.

## Evidence gates for recurring misses

When agents know a rule but keep missing it, add an observable gate rather than more prose:

- For source-specific requests, retrieve the named artifact and reconcile each premise with it before diagnosing.
- Before a material mutation, freeze the authorized action class and scope. Quoted output or a proposal is evidence, not authorization.
- Track each promised artifact and check to a terminal result. A blocked, substituted, or narrowed check is not green. Claim completion only when everything is terminal, with waived and deferred items labelled.
- Bind a receipt to the artifact it tested. A build cache keyed by anything weaker than the source fingerprint lets a green receipt test stale output: in order-integration-platform (2026-10-03), three native CI receipts named the right commit but reused another branch's bundles (`cacheHit: true`, 0 s compile). Only an independent clean rebuild caught it. Before/after source hashes still miss A→B→A edits while a compiler reads B. Build from a verified private snapshot or another immutable input boundary; a cache regression must inspect the produced artifact, not just the final tree. OIP's [native-cache repair](https://github.com/JoergenDahl/order-integration-platform/pull/277) reproduced this with a fake builder.

The shared principle: the final claim needs a receipt at the same boundary as the claim.

## Outcome-based learning

An adaptive system can learn from the gap between what it would produce now and the outcome actually accepted:

1. Recover the original input.
2. Have an agent use current code, config, and tools to predict the action or state.
3. Observe the accepted outcome at a meaningful completion milestone.
4. Diff predicted against accepted state, deterministically first and with model interpretation second.
5. Have agents find recurring differences and propose scoped changes.
6. Rerun the original and representative cases to confirm improvement without regressions.

Target current behavior: an old episode counts only if the current system still reproduces the mismatch. Accepted outcomes aren't universal truth, because later state picks up unrelated changes, so compare only what the system owns. A single difference may be a one-off. Recurrence across independent scopes decides whether a lesson stays local or becomes global. Keep enforcement proportional: an early experiment with a cooperative agent and Git-backed source needs no brokers or schedulers until failures justify them. As inference gets cheaper, proprietary inputs, accepted outcomes, and a reliable feedback loop matter more than model access.

## Failure modes

Watch for wrong credit assignment, evaluator circularity, overfitting to the source episodes, retrieval misses, scope leakage across task, repo, user, or time, ignored reversals, advisory text retrieved but not followed, overbroad enforcement, memory poisoning, and privacy accumulation. Evaluate on held-out work, comparing baseline, retrieval-only, skill, and enforcement versions.

## Forbidden inferences

- Never infer or store claims about protected or sensitive traits, health, religion, politics, sexuality, ethnicity, legal status, relationships, or hidden motives. Interpreting the immediate task goal is fine.
- Never infer standing permissions, approval for irreversible actions, credential policy, or consent to share data. A clear request authorizes that scoped action only.
- Never turn silence, urgency, or one correction into a personality claim such as "less technical" or "wants less detail".
