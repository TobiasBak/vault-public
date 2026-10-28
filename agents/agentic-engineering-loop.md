# Agentic engineering loop

Choose a valuable outcome, establish how to recognize success, and give an agent the means to reach it. Improve those conditions from the blockers encountered in real work. More subscriptions, tokens, or agents are not prerequisites for this loop.

## Choose work worth doing

Reconsider useful work previously rejected because it was tedious: exhaustive migrations, data cleanup, compatibility checks, or investigating a backlog of reproducible failures. Agents can change which of these tasks are worth attempting. Tedium is an opportunity signal, not value in itself. Start from who benefits and what becomes possible, not from a need to keep agents busy.

## Establish verification before scaling execution

Ask what observable result would distinguish success from a plausible-looking attempt. Establish a usable verification path early; discovering how to verify may itself be the first task. If judgment is subjective, name who judges and what evidence they need rather than inventing an automatic score.

[Testing with agents](testing-with-agents.md) owns verification methods. [Autoresearch](autoresearch.md) covers work that fits a repeatable experiment loop. Neither passing an easy proxy nor producing a large diff establishes the intended outcome.

## Equip the agent, then let it work

Supply missing inputs through the [task contract](instructions-and-prompts.md#task-contract). Prefer a usable environment and access to authoritative state over a longer procedural prompt. Let the agent discover implementation details within the agreed boundaries.

## Ask what is blocking progress

At a stall or handoff, ask: "What is the biggest blocker, what evidence shows it, and what would let you proceed?" A useful answer names the attempted action, observed result, and missing capability or decision. Treat the proposed cause as a hypothesis until checked.

Remove the demonstrated obstacle, resume the task, and check whether progress improves. This is an iterative loop, not a one-time onboarding exercise. Recurring friction belongs with its durable owner; the [handoff check](testing-with-agents.md#verification-tooling) routes these repairs. Don't turn every complaint into a global instruction or redesign the environment before trying real work.

The engineer still owns the outcome, boundaries, and judgment of the evidence. Blocker reports help steer the work; they do not transfer that responsibility to the agent.

Origin: a workflow image supplied by Tobias on 2026-10-28, adapted with his explicit exclusion of the multiple-Claude-subscriptions advice. Its author was not identified.
