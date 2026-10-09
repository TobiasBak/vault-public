# Agent context

Every line in the tree's context files is read by every agent on every task. Context is the most expensive prose in the repo.

## Owners

| Knowledge | Owner |
|---|---|
| Purpose, values, orientation, loop, boundaries | Root `AGENTS.md` |
| Commands and flags | The CLI's `--help` |
| Behaviors and entry points | `<cli> map`, from case records |
| Settled choices | A check, or one Boundaries line when no program can decide it |
| Invariants | Checks, whose failures name the fix |
| Ownership and structure | Directory and symbol names |
| Plans, status, progress, handoffs | The task tracker and PRs. Never the tree. |

One owner per fact. Every other place links or says nothing.

## Root AGENTS.md

Exactly these sections, in this order:

```
# <product>

<One line: what it does and its published interface.>

## Purpose

<Who consumes it, what it must achieve, what it never does.>

## Values

1. <value>: beats <what it overrides when they conflict>.

## Loop

- `<cli> map` to find a behavior; `<cli> status` for the verdict on the current tree; `<cli> why <case>` for a failure.
- Never sleep. `<cli> wait <job>`.
- Batch independent reads into one call.
- Tests are black-box cases in `<corpus>/`. No unit tests. Extend an existing case before adding one. Expected-output changes need a `Behavior-Change:` trailer naming the source of truth.

## Areas

- `<dir>/`: <what it owns>.

## Boundaries

- <authority boundary, external contract, or hazard an agent can't discover in time>.

```

- At most 80 lines.
- Values decide tradeoffs no rule anticipated. Ranked, at most five, each naming what it beats. A value that never wins a tradeoff is a slogan; delete it.
- A value a program can check also becomes a check. The line stays for the cases the check can't decide.
- Areas use the corpus area names.
- Boundaries hold only what an agent can't learn from code, `--help`, or a check failure before it does damage.

## What stays out

- Rationale, history, generic engineering advice, and descriptions of what the code does.
- Command documentation. `--help` owns it.
- Any rule a check enforces, unless agents hit it on the common path. Then one line, no explanation.
- Plans, status, and progress. A stale plan in the tree misleads every later agent.

## Host instruction files

The root `AGENTS.md` is the only instruction file. Hosts that require another filename get a symlink to it. No README.

## Pruning

- A line stays only if a fresh agent fails a representative task without it.
- When a check takes over a rule, delete the rule's line in the same change.
- When a line keeps getting violated, replace it with a check.
