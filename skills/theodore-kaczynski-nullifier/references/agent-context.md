# Agent context

Every agent reads root `AGENTS.md` on every task. Skills load only when relevant. Keep always-on context small.

## Owners

| Knowledge | Owner |
|---|---|
| Purpose, values, orientation, loop, boundaries | Root `AGENTS.md` |
| Commands and flags | The CLI's `--help` |
| Task-specific procedures the CLI doesn't perform | Skills |
| Behaviors and entry points | `<cli> map`, from case records |
| Settled choices | A check, or one Boundaries line when no program can decide it |
| Invariants | Checks, whose failures name the fix |
| Ownership and structure | Directory and symbol names |
| Plans, status, progress, handoffs | The task tracker and PRs. Never the tree. |
| Decisions, rationale, ADRs | Issues and PRs. Never the tree. |

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

- <Commands for adopted behavior lookup, current-tree verdict, and failure diagnosis capabilities. Omit capabilities not adopted.>
- Never sleep.
- <Command for waiting on job exit or verdict, only if background jobs are adopted.>
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
- Docs directories. Contracts become checks and black-box cases through [contract migration](#contract-migration).

## Contract migration

- Before migrating a contract, apply the [contract and proof lifetime check](black-box-tests.md#migrating-an-existing-suite).
- Relocating a decision or contract does not revoke it. Preserve its authority and consumer route before removing its old prose home.
- Before deleting a contract doc, confirm no consumer outside the repo reads it.
- A consumed contract is the published interface: keep only the minimal machine-checked form that consumer needs, and record its exact approved path in the gate.

## Instruction surfaces

Root `AGENTS.md` owns always-on instructions; [skills](#skills) own progressive disclosure. Delete prompt files (including `.codex/` and `.pi/` prompts), command docs, and nested `AGENTS.md` files. First move their content to its [owner](#owners); an `AGENTS.md` line must pass [pruning](#pruning).

Hosts that require another instruction filename get only a symlink to the root `AGENTS.md`. Move an existing host file's content to its owner before replacing it. No README.

## Skills

- Repo-local skills are allowed.
- No duplication of CLI `--help`, `AGENTS.md` lines, or another skill. Link to the owner.
- Every named path and command exists. The agent-context check covers skills too.
- The description says when the skill applies.
- When the CLI performs a skill's procedure in one call, delete the skill or cut it to what remains.

## Pruning

- A line stays only if a fresh agent fails a representative task without it.
- When a check takes over a rule, delete the rule's line in the same change.
- When a line keeps getting violated, replace it with a check.
