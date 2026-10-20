# Agent context

Every agent reads root `AGENTS.md` on every task; skills load only when relevant. Keep the always-loaded part small.

## Owners

Each fact has one home; everywhere else links to it or says nothing.

| Knowledge | Home |
|---|---|
| Purpose, values, orientation, loop, boundaries | Root `AGENTS.md` |
| Commands and flags | The owning tool's `--help` |
| Workspace, scheduling, and landing procedure | Shared-tool help and session instructions, not repository prose |
| Task steps the CLI doesn't perform | Skills |
| Behaviors and entry points | `<cli> map`, built from case records |
| Settled choices | A check, or one Boundaries line when no program can decide it |
| Invariants and their reasons | Checks, whose failures state the reason and fix |
| Why a one-off decision was made | A `Why:` commit trailer ([why](../SKILL.md#where-the-why-goes)) |
| Ownership and structure | Directory and symbol names |
| Plans, status, progress, handoffs | The task tracker and PRs, never the tree |
| Decisions, rationale, ADRs | Issues and PRs, never the tree |

## Root AGENTS.md

Exactly these sections, in this order:

```
# <product>

<One line: what it does and its published interface.>

## Purpose

<Who uses it, what it must achieve, what it never does.>

## Values

1. <value>: beats <what it overrides when they conflict>.

## Loop

- <Commands for the adopted capabilities: behavior lookup, current-tree verdict, failure diagnosis. Omit any not adopted.>
- <Product job wait command, only if background jobs are adopted.>
- Tests are black-box cases in `<corpus>/`. No unit tests. Extend an existing case before adding one. Expected-output changes need a `Behavior-Change:` trailer naming the source of truth.
- No comments. A reason goes in a check's failure message, a case's oracle, or a `Why:` commit trailer.

## Areas

- `<dir>/`: <what it owns>.

## Boundaries

- <authority limit, external contract, or hazard an agent can't discover before it does damage>.

```

- At most 80 lines.
- Values settle tradeoffs no rule foresaw: ranked, at most five, each naming what it beats (`1. Correct output: beats speed.`). A value that never wins a tradeoff is a slogan; delete it. A value a program can check also becomes a check; the line stays for cases the check can't decide.
- Areas use the corpus area names.
- Boundaries hold only what an agent can't learn from code, `--help`, or a check failure before it does damage (`Never deploy to production; only Tobias does.`).

## What stays out

- Rationale, history, generic advice, and descriptions of what the code does.
- Command docs; `--help` owns them. Shared-platform procedures and global agent habits stay out too.
- Any rule a check enforces, unless agents hit it on the common path. Then one line, no explanation.
- Plans, status, and progress. A stale plan in the tree misleads every later agent.
- Docs directories. Their contracts become checks and cases through [contract migration](#contract-migration). The one exception is a published contract file: one an outside consumer reads (an OpenAPI spec, a schema), kept at an exact path the gate lists.

## Contract migration

- First apply the [check that the contract and its proof will still matter](black-box-tests.md#migrating-an-existing-suite).
- Moving a decision or contract does not cancel it. Keep its authority, and the way its consumers reach it, before deleting its old prose.
- Before deleting a contract doc, confirm nothing outside the repo reads it.
- A contract an outside consumer reads is part of the published interface: keep only the smallest machine-checked form that consumer needs, and list its exact path in the gate.

## Instruction surfaces

Root `AGENTS.md` holds always-on instructions; [skills](#skills) hold instructions loaded on demand. Delete prompt files (including `.codex/` and `.pi/` prompts), command docs, and nested `AGENTS.md` files, after moving their content to its [home](#owners). A line moved into `AGENTS.md` must pass [pruning](#pruning).

A host that requires another instruction filename gets only a symlink to root `AGENTS.md`. Move an existing host file's content to its home before replacing it. No README.

## Skills

- Repo-local skills are allowed.
- Never repeat CLI `--help`, `AGENTS.md` lines, or another skill. Link to the home instead.
- Every path and command a skill names exists. The agent-context check covers skills.
- The description says when the skill applies.
- When the CLI does a skill's whole procedure in one call, delete the skill or cut it to what remains.

## Pruning

- A line stays only if a fresh agent fails a representative task without it.
- When a check takes over a rule, delete the rule's line in the same change.
- When a line keeps being violated, replace it with a check.
