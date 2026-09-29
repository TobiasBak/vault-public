---
name: potato-approach
description: Design, implement, refactor, or review agent-maintained code so the easiest change is the correct one. Use for recurring mistakes, PR feedback, later regressions, enforced rules, shared engineering workflows, or project verification tools and feature maps. Not for ordinary prose or vault-note editing.
---

# Potato approach

Build a codebase agents can understand, change correctly, and operate to investigate and verify their work. Clear ownership, supported implementation paths, and working verification tools are essential parts of that environment.

Agents copy the code they read. The codebase is their primary working documentation and memory: its types, APIs, boundaries, and accepted examples teach the next change.

## Understand the system and equip the agent

Before choosing a change, trace the relevant product behavior through its owning code, callers, state, effects, and constraints. Find how to run and observe it. Use source inspection and runtime exploration together; neither a file inventory nor a passing static check establishes how the product behaves. Keep exploration scoped to the requested outcome.

Make that understanding recoverable from the project. Code structure conveys implementation ownership and boundaries; [feature maps](references/feature-map.md) explain what the product does, how users reach its behavior, and what should happen. Use and maintain existing maps, and fill relevant gaps when agents would otherwise have to guess. Confirm runnable instructions against the application.

Verification requires working capabilities, not an instruction to "test your changes." Ensure agents can establish starting state, exercise the relevant behavior, inspect its results and effects, and collect diagnostics or measurements needed for the task. Reuse existing tools; build or repair missing operations through [verification CLIs](references/verification-cli.md). Support investigation as well as known test scenarios. Preserve methods that need judgment in [engineering workflows](references/engineering-workflows.md).

When preparing a codebase for agent work, address product understanding and verification tools alongside implementation paths and enforcement, without waiting for repeated failures. Exercise the tools on the relevant workflow and keep them and affected feature maps current as the product changes. Static checks protect settled rules; runtime verification establishes whether the changed behavior works. Neither replaces the other.

## Choose where knowledge belongs

When an engineer supplies a correction or a settled design decision, prefer this order:

1. Codebase structure and examples.
2. Executable static checks run by pre-commit and CI, not Markdown instructions.
3. Repository rules checked by focused review agents, as with Bugbot.
4. Skills for methods that need judgment.
5. Human-enforced style guides.

Encode knowledge in the strongest suitable place. Do not default to another instruction or skill when a better API or check can prevent the mistake. Keep rationale and external contracts in prose where code cannot express them.

This is an order of preference for preserving knowledge, not a five-step checklist for every task.

For active codebase hardening, enforce the settled rule first, let existing violations fail, then repair them end to end. Do not hide failures with baselines, suppressions, or deferred coverage. If work stops before repair is complete, leave the gate enabled and visibly failing. [Codebase hardening](references/codebase-hardening.md#enforce-first-repair-end-to-end) owns the rollout procedure.

## Choose the work

Start with the requested outcome or observed failure. Read only the references needed for that work.

| Need | Direction and reference |
|---|---|
| PR review comments or bugs from earlier PRs may reveal missing protection | [Learn from PR feedback and later bugs](references/pr-feedback-review.md) |
| Repeated mistakes or too many implementation choices require supervision | [Codebase hardening](references/codebase-hardening.md) |
| Important engineering rules require judgment beyond static checks | [Focused review agents](references/review-agents.md) |
| Existing workarounds or competing patterns teach the wrong approach | [Codebase cleanup](references/codebase-cleanup.md) |
| Establish or improve agents' ability to explore and verify product behavior | [Feature maps](references/feature-map.md) for workflow knowledge; [verification CLIs](references/verification-cli.md) for working control and inspection tools |
| Agents repeatedly need help choosing an investigation or implementation method | [Engineering workflows](references/engineering-workflows.md) |

Combine directions when the problem needs them. Cleanup removes bad examples; hardening prevents recurrence. A feature-map task does not automatically authorize either.

Recommend broader rules when warranted; keep changes within the authorized task and the target repository's policy. For the video, timestamped topics, and related sources, read [References](references.md) when checking the approach's background, not on every use.
