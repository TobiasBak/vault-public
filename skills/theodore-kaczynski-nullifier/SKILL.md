---
name: theodore-kaczynski-nullifier
description: Shape a repository for agent-only development so feedback is faster than agent thinking. Use when setting up or restructuring a repo, when agent loops feel slow, when builds, tests, CI, or platform runs dominate sessions, to find verification/CI/test bottlenecks or trace slow gates, whenever writing, reviewing, or migrating tests, and whenever writing AGENTS.md. Defines black-box-only testing, agent context, cached verdicts, always-on watchers, one-call answers, and no blind waits.
---

# Theodore Kaczynski Nullifier

Technology was never the problem. Waiting on it is.

## The law

**Agent thinking is the only acceptable bottleneck.** A tool call slower than a model turn needs a reason. A turn spent on a question the repo could have answered in the previous call is waste.

**No human reads this repository.** Repository-hygiene checks enforce these contracts when adopted for the selected outcome:
- **Zero comments.** No explanatory comments, doc comments, TODOs, banners, or commented-out code. A line-1 interpreter directive is not a comment.
- **Prose only in** root `AGENTS.md`, [skills](references/agent-context.md#skills), the CLI's `--help`, case records, and [approved published contracts](references/agent-context.md#what-stays-out). Every other prose file fails.
- **No README.**
- Name things for `rg`.

**Only black-box tests, as few as possible.** Input in at the published interface, specified output out. Extend a case before adding one. Static checks, types, linters, and formatters carry everything else. Keep an existing suite intact until an authorized [migration](references/black-box-tests.md#migrating-an-existing-suite) proves its replacement.

## The loop

1. **Measure.** Agents can't see their own time. Read the harness's session logs: model time is request to response, tool time is call to result. Split it into model, tool by class (build, test, platform, git, wait), and waiting on children or the user.
2. **Select one outcome.** Name the consumer workflow, who uses it, observed frequency, process boundary, current cost, and removable cause. Fix the largest measured recurring cost at its owner: the CLI, cache, harness, or host tooling. Never with an instruction agents must remember. Correctness, security, and data-loss defects justify scoped fixes without a speed claim.
3. **Check value.** Use existing evidence. A baseline and causal hypothesis can justify one or two matched screens. A migration, watcher, new enforcement system, or standalone proof program proceeds only when the screen demonstrates value. Otherwise park it; a failed screen does not justify another research program to rescue the candidate.
4. **Measure again** on the selected workflow after the change.
- Use `<cli> trace [verdict]` to locate verification bottlenecks and critical-path deltas under the [tracing contract](references/tracing.md).

## Adopt capabilities for the outcome

Read every reference in full. They define the contracts of capabilities adopted for the selected outcome, not an implementation backlog. Do not weaken an adopted check to make it green. Unrelated whole-repository conformance is separate work. In a new repository, establish the real first workflow and its correctness boundaries; add operational machinery when that workflow needs it.

The references:
- [manifest.md](references/manifest.md)
- [black-box-tests.md](references/black-box-tests.md)
- [control-cli.md](references/control-cli.md)
- [tracing.md](references/tracing.md)
- [enforcement.md](references/enforcement.md)
- [agent-context.md](references/agent-context.md)

Choose what removes the selected cost or repairs the broken contract:
- One control CLI whose adopted commands answer real recurring questions in one call, failures only.
- A small black-box corpus of fat scenarios within their budgets, and static checks.
- A verdict cache keyed on build inputs and case, shared across worktrees and agents.
- An always-on watcher, so the verdict for the current tree exists before anyone asks.
- `wait`, never `sleep`.
- A visible time budget on every adopted tier.
- Each adopted rule a gate check with an approved path.
- A root `AGENTS.md` in the [fixed shape](references/agent-context.md#root-agentsmd).
- Nothing duplicates the CLI; skills add only task-specific instructions.

## Verification

Prove the delivered outcome, not every capability in this skill:
- For an optimization, a before-and-after ledger for the targeted cost on the selected workflow.
- For changed contracts, success, targeted failure, applicable blocked prerequisites, and affected cache or cleanup behavior through the real public entrypoint. Use the [disposable proof procedure](references/control-cli.md#proof); reuse valid evidence for unchanged surfaces.
- For tracing, a real gate run emits a trace that loads as valid Chrome Trace JSON; one injected delay in a single step appears as the top critical-path delta in `<cli> trace`.
- For adopted or changed enforcement, the gate rejects the forbidden pattern and accepts the approved path through its real entrypoints.
- For cache changes, repeated unchanged-tree verdict reuse without building and rejection of stale evidence.
- For edit-loop changes, a one-line source edit reaching its verdict, rebuild included, faster than a model turn. Cache hits prove nothing about the edit loop.
- For navigation or diagnostic changes, a fresh agent given a real bug report locates, reproduces, and proves the fix. Count its turns before and after.
- For authorized suite deletion, the [replacement proof](references/black-box-tests.md#migrating-an-existing-suite). A failed pilot can stop migration, never authorize deletion without proof.
