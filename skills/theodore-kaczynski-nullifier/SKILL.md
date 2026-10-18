---
name: theodore-kaczynski-nullifier
description: Set up a repository so agents, not humans, develop in it. Use when setting up or restructuring a repo for agents, when the chosen work is cutting a measured wait (build, test, CI, gate or platform run), when tracing slow gates, or when writing AGENTS.md.
---

# Theodore Kaczynski Nullifier

Technology was never the problem. Waiting on it is.

## Terms

- **Published interface:** what outside users call: CLI, HTTP API, file-in/file-out contract, or a library's public API.
- **Case:** one black-box test directory (input, expected output, `case.toml`). The **corpus** is all cases.
- **Verdict:** pass, fail, or blocked for one tree. The **gate** is the git hooks running `<cli> check`.
- **Approved path:** the allowed way to do what a check forbids. Every failure names it.
- **Promotion PR:** the main→staging PR (main→production without staging). It runs the full corpus and secondary platforms.

## The law

**Agent thinking is the only acceptable bottleneck.** A tool call slower than a model turn needs a reason. A turn spent on a question the repo could have answered in the previous call is waste.

**No human reads this repository.** Adopted checks enforce:
- **Zero comments:** no explanatory or doc comments, TODOs, banners, or commented-out code. A line-1 `#!` is not a comment.
- **Prose only in** root `AGENTS.md`, [skills](references/agent-context.md#skills), CLI `--help`, case records, and [published contract files](references/agent-context.md#what-stays-out) at exact gate-listed paths.
- **No README.**
- Name things so `rg` finds them.

**Only black-box tests, as few as possible.** Input in at the published interface, specified output out. Extend a case before adding one. Static checks, types, linters, and formatters cover the rest. Keep an existing suite until an authorized [migration](references/black-box-tests.md#migrating-an-existing-suite) proves its replacement.

## Where the why goes

Comments stay banned, no exceptions. A reason names and code can't show goes:
1. **First, into something that runs:** a gate check whose failure states the reason and approved path (`Cloud Run ignores resource.name conditions; grant roles/run.invoker on the service without one.`), or a case's `oracle` prose explaining the behavior.
2. **Second, for a one-off decision no program can check:** a `Why:` commit trailer (`Why: pin serde_yaml 0.9.33; 0.9.34 breaks anchors.`), found with `git log -S'<code>'` or `git blame`.

Anything else belongs in the issue or PR, never the tree.

## The loop

Aim at shorter PR lead time on a named product workflow, not faster tools for their own sake. This runs beside product work, never as its precondition.

1. **Measure** from the harness's session logs; agents can't see their own time. Split time into model (request to response), tool by kind (build, test, platform, git, wait), and waiting on child agents or the user.
2. **Pick one outcome:** the product workflow that gains and who uses it, how often it runs, the step where the time goes (e.g. pre-push), its current cost, and the cause you can remove. Fix the largest measured recurring cost where it originates (CLI, cache, harness, host tooling), never with an instruction agents must remember. Correctness, security, and data-loss bugs justify scoped fixes with no speed claim.
3. **Check value** with existing evidence. A baseline plus a named cause justifies one or two small before-and-after trials under the same conditions. A migration, watcher, new enforcement system, or standalone proof effort goes ahead only if a trial shows value; otherwise shelve it, with no new research to rescue it.
4. **Measure again** on the same workflow. Stop when a one-line edit reaches its verdict faster than a model turn, or the measured target is met. More loop work needs a new measured cost.

## What to read

Adopt only what removes the chosen cost or repairs a broken contract. References define each capability's contract once adopted; they are not a to-do list. Read only the ones the outcome needs:

| Job | Read |
|---|---|
| Choosing the slow pattern to fix (one-call answers, waits, cache, watcher, budgets, scope, review) | [manifest.md](references/manifest.md) |
| Writing, changing, or migrating tests | [black-box-tests.md](references/black-box-tests.md) |
| Adding CLI commands, output, runs, mutation testing, proofs | [control-cli.md](references/control-cli.md) |
| Tracing slow gates | [tracing.md](references/tracing.md) |
| Adopting, fixing, or rolling out checks | [enforcement.md](references/enforcement.md) |
| `AGENTS.md`, skills, moving docs out of the tree | [agent-context.md](references/agent-context.md) |

Never weaken an adopted check to pass. Whole-repo conformance is separate work. In a new repo, build the first real workflow and its correctness checks; add machinery when it needs it. Typical pieces: one control CLI answering recurring questions in one call, failures only; a small corpus of large scenario cases plus static checks; a verdict cache shared across worktrees and agents; a watcher; `wait`, never `sleep`; a visible budget per tier; every rule a gate check with an approved path; a root `AGENTS.md` in the [fixed shape](references/agent-context.md#root-agentsmd); nothing duplicating the CLI.

## Verification

Prove what you delivered, not every capability here:
- **Speedup:** before-and-after numbers for the targeted cost on the chosen workflow.
- **Changed contract:** the [proof procedure](references/control-cli.md#proof).
- **Tracing:** a real gate run writes valid Chrome Trace JSON, and one injected delay in one step is the top critical-path change in `<cli> trace`.
- **Enforcement:** the gate rejects the forbidden pattern and accepts the approved path through its real entrypoints.
- **Cache:** an unchanged tree reuses its verdict without building; stale evidence is rejected.
- **Edit loop:** a one-line edit reaches its verdict, rebuild included, faster than a model turn. Cache hits prove nothing here.
- **Navigation or diagnostics:** a fresh agent given a real bug report finds, reproduces, and proves the fix; count its turns before and after.
- **Suite deletion:** the [replacement proof](references/black-box-tests.md#migrating-an-existing-suite). A failed pilot can stop a migration, never authorize deletion.
