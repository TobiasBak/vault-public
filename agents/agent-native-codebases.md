# Agent-native codebases

An agent-native codebase stays understandable, changeable, and verifiable across fresh agent contexts. Every context starts from the repository and leaves its handoff there, so intent, ownership, invariants, unfinished work, and evidence must be recoverable without private human memory. Capability belongs to the whole system: model, prompt, context, state, tools, orchestration, permissions, evaluator, and feedback loop. Improving one layer alone can just move the failure somewhere else.

## Patch accretion is the main failure

A narrow task rewards the smallest plausible change even when it adds a parallel path, duplicates a rule, blurs ownership, or tests only the symptom. Each such patch enlarges the next change's context, and slower verification pushes later agents toward even narrower patches. Cheap patches make later agent work progressively more expensive.

Before implementing, reconstruct the behavior end to end: owner, invariants, callers, effects, verification path. Compare the smallest patch, a local refactor, and the simplest coherent redesign. A quick patch is sound when it is local, reversible, boundary-preserving, and independently verifiable. Duplicated knowledge, scattered changes, hidden effects, a false abstraction, or a missing test seam call for repair at the owning boundary. Concrete friction justifies focused redesign; it does not justify unrelated cleanup or speculative abstraction. Bring material design choices to Tobias with a recommendation; the requested implementation is not a settled design.

Settle goals, contracts, invariants, and acceptance up front. Discover the details against the real system and deliver in reversible increments. Disposable experiments need no production structure.

## Make the easiest change the correct one

Agents copy the code they read. Types, APIs, boundaries, and accepted examples teach more than instructions do, and bad examples spread just as fast as good ones. Lock down routine choices so weak models and low-context humans can make correct changes:

- Keep feature code together, give state and effects one owner, enforce dependency boundaries, and use types that exclude invalid states.
- Keep one conventional path per recurring change. Remove bad examples and block their return.
- Pair every restriction with a usable alternative: an obvious location, a supported API, and an example worth copying. Checks reject the wrong way; interfaces make the right way easy. When agents keep fighting a boundary, fix the supported path before adding instructions.
- Comments that justify a workaround make it look approved. Fix the design instead (see [documentation and naming](documentation-and-naming.md)).

When correcting an agent, put the knowledge in the strongest place that fits, in this order:

1. **Codebase:** change the structure, API, or data model so the mistake can't be expressed.
2. **Static checks:** compiler, type, lint, or dependency checks that fail with a nonzero exit in pre-commit and CI. Markdown is never a static check.
3. **Rules plus focused review agents:** for rules that need judgment. A required review gates acceptance, but it is not a guarantee. See [code review](code-review.md).
4. **Skills:** reusable methods that need judgment, such as debugging, performance work, or verification.
5. **Human-enforced style guides:** the weakest form. Treat review findings as signals that structure or checks are missing.

**Enforce first, repair end to end** (Tobias's rollout policy). Enable a settled rule over its full scope immediately and let existing violations fail; the failing gate is the work inventory. No baselines, suppressions, warning-only modes, or deferred type coverage. If work stops, leave the gate enabled and failing and record what remains. Unfinished repair is an acceptable handoff; false green is not.

Someone has to own this upkeep. Lauren Tan calls it gardening. Her Dune framework keeps features together, checks imports between Electron main and renderer, and bans comments. Combine constraints, skills, and [runtime verification](testing-with-agents.md) before scaling parallelism. Once agents can reproduce and verify, reports and alerts can become coding tasks automatically.

Source: Lauren Tan, [September 2026 talk on trusting coding agents](https://x.com/poteto/status/2102050467505430555/video/1). The operational method lives in the [potato-approach skill](../.agents/skills/potato-approach/SKILL.md).
