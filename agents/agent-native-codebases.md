# Agent-native codebases

An agent-native codebase stays understandable, changeable, and verifiable across fresh agent contexts. Every context starts from the repository and leaves its handoff there, so intent, ownership, invariants, unfinished work, and evidence must be recoverable without private human memory. Capability belongs to the whole system: model, prompt, context, state, tools, orchestration, permissions, evaluator, and feedback loop. Improving one layer alone can just move the failure somewhere else.

The [design principles](../skills/theodore-kaczynski-nullifier/references/design-principles.md) set the goal: a fresh agent understands the system, changes it correctly, establishes actual outcomes, and recovers when reality disagrees. They require independent authority for correctness, inspectable runtime behavior, recoverable failure, and constraints whose reasons remain discoverable.

The [agentic engineering loop](agentic-engineering-loop.md) connects this repository design to choosing and carrying out useful work.

## Patch accretion is the main failure

A narrow task rewards the smallest plausible change even when it adds a parallel path, duplicates a rule, blurs ownership, or tests only the symptom. Each such patch enlarges the next change's context, and slower verification pushes later agents toward even narrower patches. Cheap patches make later agent work progressively more expensive.

Before implementing, reconstruct the behavior end to end: owner, invariants, callers, effects, verification path. Compare the smallest patch, a local refactor, and the simplest coherent redesign. A quick patch is sound when it is local, reversible, boundary-preserving, and independently verifiable. Duplicated knowledge, scattered changes, hidden effects, a false abstraction, or a missing test seam call for repair at the owning boundary. Concrete friction justifies focused redesign; it does not justify unrelated cleanup or speculative abstraction.

Settle goals, contracts, invariants, and acceptance up front. Discover the details against the real system and deliver in reversible increments. Disposable experiments need no production structure.

## Make the easiest change the correct one

Agents copy the code they read. Types, APIs, boundaries, and accepted examples teach more than instructions do, and bad examples spread just as fast as good ones. Lock down routine choices so weak models and low-context humans can make correct changes:

- Keep feature code together, give state and effects one owner, enforce dependency boundaries, and use types that exclude invalid states.
- Keep one conventional path per recurring change. Remove bad examples and block their return.
- Pair every restriction with a usable alternative: an obvious location, a supported API, and an example worth copying. Checks reject the wrong way; interfaces make the right way easy. When agents keep fighting a boundary, fix the supported path before adding instructions.
- Comments that justify a workaround make it look approved. Fix the design instead (see [documentation and naming](documentation-and-naming.md)).

The [potato-approach skill](../skills/potato-approach/SKILL.md) owns the order in which a correction goes into codebase structure, static checks, judgment rules, skills, or human-enforced style guides; prose sits at the bottom of it. Two exemplars: the vault's link and staleness checks run as a commit hook rather than as a remembered step, and the dotfiles routing hook denies model targets that prose had already ruled out ([routing](compute-routing.md)). A rule that keeps needing reminders is a missing mechanism.

**Enforce first, repair end to end** (Tobias's rollout policy). Enable a settled rule over its full scope immediately and let existing violations fail; the failing gate is the work inventory. No baselines, suppressions, warning-only modes, or deferred type coverage. If work stops, leave the gate enabled and failing and record what remains. Unfinished repair is an acceptable handoff; false green is not.

Someone has to own this upkeep. Lauren Tan calls it gardening. Her Dune framework keeps features together, checks imports between Electron main and renderer, and bans comments. Combine constraints, skills, and [runtime verification](testing-with-agents.md) before scaling parallelism. Once agents can reproduce and verify, reports and alerts can become coding tasks automatically.

Source: Lauren Tan, [September 2026 talk on trusting coding agents](https://x.com/poteto/status/2102050467505430555/video/1). The operational method lives in the [potato-approach skill](../skills/potato-approach/SKILL.md).

## Decode once, then trust types

Agents write defensively. A narrow task can't see the guarantee upstream, so a null check, a `catch` or a fallback default looks free. Each one adds a path nobody tests, hides the bug it was meant to catch, and teaches the next agent the type can't be trusted. It's patch accretion at line scale.

- Decode untrusted data once, at the boundary that owns it, into types that exclude invalid states. Inward code never re-checks what a type, schema or constructor guarantees.
- Handle an error only to recover, translate it at a boundary or clean up. Swallowing, defaulting away (`.ok()`, `unwrap_or_default()`, `catch {}`) or logging and continuing turns a failure into a wrong answer.
- Inline single-use logic unless the helper owns a boundary or names a domain rule. A row of named predicates, each one business rule, reads better than one inlined boolean; a name that restates its body doesn't earn the jump.

Enforce it where a lint can: TypeScript `strict` with `@typescript-eslint/no-unnecessary-condition` rejects checks a type rules out, and Clippy's `map_err_ignore` and `let_underscore_must_use` reject discarded errors. Prose covers the rest. Origin: rules attributed to a large coding agent's `AGENTS.md` that circulated on X on 2026-10-28; the version here tightens their helper exception and replaces "avoid try/catch" with when to handle an error.
