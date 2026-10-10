---
name: theodore-kaczynski-nullifier
description: Shape a repository for agent-only development so feedback is faster than agent thinking. Use when setting up or restructuring a repo, when agent loops feel slow, when builds, tests, CI, or platform runs dominate sessions, whenever writing, reviewing, or migrating tests, and whenever writing AGENTS.md. Defines black-box-only testing, agent context, cached verdicts, always-on watchers, one-call answers, and no blind waits.
---

# Theodore Kaczynski Nullifier

Technology was never the problem. Waiting on it is.

## The law

**Agent thinking is the only acceptable bottleneck.** A tool call slower than a model turn needs a reason. A turn spent on a question the repo could have answered in the previous call is waste.

**No human reads this repository.** The gate enforces:
- **Zero comments.** No explanatory comments, doc comments, TODOs, banners, or commented-out code. A line-1 interpreter directive is not a comment.
- **Prose only in** `AGENTS.md`, the CLI's `--help`, and case records. Every other prose file fails.
- **No README.**
- Name things for `rg`.

**Only black-box tests, as few as possible.** Input in at the published interface, specified output out. Extend a case before adding one. Static checks, types, linters, and formatters carry everything else.

## The loop

1. **Measure.** Agents can't see their own time. Read the harness's session logs: model time is request to response, tool time is call to result. Split it into model, tool by class (build, test, platform, git, wait), and waiting on children or the user.
2. **Fix the biggest cost** at its owner: the CLI, cache, harness, or host tooling. Never with an instruction agents must remember.
3. **Measure again.**

## A shaped repo has

Read every reference in full and bring the repo to every rule:
- [manifest.md](references/manifest.md)
- [black-box-tests.md](references/black-box-tests.md)
- [control-cli.md](references/control-cli.md)
- [enforcement.md](references/enforcement.md)
- [agent-context.md](references/agent-context.md)

The result:
- One control CLI whose commands answer whole questions in one call, failures only.
- A small black-box corpus of fat scenarios, and static checks. Nothing else.
- A verdict cache keyed on build inputs and case, shared across worktrees and agents.
- An always-on watcher, so the verdict for the current tree exists before anyone asks.
- `wait`, never `sleep`.
- A visible time budget on every tier.
- Every rule a gate check with an approved path.
- A root `AGENTS.md` in the [fixed shape](references/agent-context.md#root-agentsmd), and nothing else that instructs.

## Verification

- A before-and-after ledger for the targeted cost on a representative task.
- The gate rejecting a unit test, a comment, and an unexplained expected-output change through the real entrypoints.
- A repeated `status` on an unchanged tree returning from cache without building.
- A one-line source edit reaching its verdict, rebuild included, faster than a model turn. Cache hits prove nothing about the edit loop.
- A fresh agent given a real bug report locates, reproduces, and proves the fix. Count its turns before and after.
