# Agent context

Keep root `AGENTS.md` small and verify the host loads it when needed; skills load only when relevant.

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

Before a line stays, name its reader, the moment they read it, and what breaks if it is deleted. A line whose reader never has this file open — a skill rule needed while editing a skill, a directory map needed while filing a note, a charter line a skill already owns — belongs at that moment's owner, and this file keeps a pointer or nothing. Adopting or rewriting the file is an audit of every line, not a reformat: a line that restates another file's rule is a second authority, not a reminder.

Keep orientation, task entrypoints, ownership and authority limits only where a fresh agent needs them. One possible structure is Purpose, Values, Loop, Areas and Boundaries; omit what does not help the repository. Values can name what they beat when that resolves a real tradeoff. This is an example, not a required heading order, ranking or line limit. Update consumers and checks when moving a real obligation.

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
- Each skill is self-contained: instructional file links stay inside its own directory, not vault notes or sibling skills. Name shared-tool and host dependencies; their active help and session instructions remain authoritative.
- Within a skill, give each instruction one home and link to it instead of repeating it. Do not copy CLI `--help`, shared delivery policies, or instructions already supplied by the target repository's root `AGENTS.md`.
- Every concrete path and command a skill names exists. The agent-context check validates mechanically resolvable references; relevance, duplication, and whether a procedure still earns its place require judgment on a representative task.
- The description says when the skill applies.
- When the CLI does a skill's whole procedure in one call, delete the skill or cut it to what remains.

## Pruning

- Chosen policies and real authority limits need no failure experiment. Other instructional lines stay only when they supply information a fresh agent needs on a representative task.
- When a check takes over a rule, delete the rule's line in the same change, except the common-path reminder allowed above.
- When a line keeps being violated, fix the owning structure or enforce the mechanically decidable pattern. Do not claim a syntax check enforces a semantic judgment.
