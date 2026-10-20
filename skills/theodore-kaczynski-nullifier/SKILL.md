---
name: theodore-kaczynski-nullifier
description: Set up repositories for agents using shared infrastructure. Use when designing product verification or agent context, cutting a measured build, test, gate or platform-run wait, tracing slow feedback, or writing AGENTS.md.
---

# Theodore Kaczynski Nullifier

Technology was never the problem. Waiting on it is.

**Agent thinking is the only acceptable bottleneck.** A tool call slower than a model turn needs a reason. A turn spent on a question the repo could have answered in the previous call is waste.

## Ownership

Use the shared platform for workspaces, warm state, scheduling, and landing. Build only the product-specific feedback it cannot provide.

- **gah:** workspace isolation, forwarding, conflicts, child integration, warm build-state forks, and landing through the repository check. Its help and session instructions own the procedure.
- **heavy-lease:** host admission. Repository entrypoints [request resources](references/control-cli.md#host-admission), never implement another scheduler.
- **The repository:** published contract, verification inputs, cases, static checks, incremental builds, and diagnostics, exposed through a [product verification CLI](references/control-cli.md).

Warm state and a clean merge are not behavioral proof. Reuse evidence only when its [inputs still match](references/manifest.md#3-cache-verdicts); reconsider reasoning when its dependencies change.

## Repository rules

**No human reads this repository.** Adopted checks enforce:
- **Zero comments:** no explanatory or doc comments, TODOs, banners, or commented-out code. A line-1 `#!` is not a comment.
- **Prose only in** root `AGENTS.md`, [skills](references/agent-context.md#skills), CLI `--help`, case records, and [published contract files](references/agent-context.md#what-stays-out) at exact gate-listed paths. No README.
- Name things so `rg` finds them.

**Only black-box tests, as few as possible.** Input in at the published interface, specified output out. Extend a case before adding one. Static checks, types, linters, and formatters cover the rest. Keep an existing suite until an authorized [migration](references/black-box-tests.md#migrating-an-existing-suite) proves its replacement.

## Where the why goes

Comments stay banned. A reason names and code can't show goes:
1. Into something that runs: a check whose failure states the reason and approved path, or a case's `oracle` explaining the behavior.
2. For a one-off decision no program can check, a `Why:` trailer in the final landed commit, found with `git log -S'<code>'` or `git blame`.

The [landing integration](references/enforcement.md#landing-metadata) must preserve applicable trailers through squashes and parent landings. Child commits alone are not their durable home. Other rationale belongs in issues or PRs.

## The loop

Aim at a shorter edit-to-main loop on a named product workflow. This runs beside product work, never as its precondition.

1. **Measure** from harness session logs. Separate model, build, test, platform, admission, forwarding, conflict, landing, child, and user time. Include shared-tool waits.
2. **Pick one outcome:** workflow, users, frequency, current cost, and cause to remove. Fix the largest measured recurring cost at its owner, never with an instruction agents must remember. Correctness, security, and data-loss bugs justify scoped fixes without a speed claim.
3. **Check value:** a baseline and named cause justify one or two before-and-after trials under the same conditions. Migrations, watchers, new enforcement systems, and standalone proof efforts need a trial showing value. Otherwise shelve them.
4. **Measure again.** Stop at the measured target or when a one-line edit reaches its verdict, rebuild included, faster than a model turn. Further work needs a new measured cost.

## What to read

Adopt only what removes the chosen cost or repairs a broken contract. References define adopted capabilities, not a to-do list:

| Job | Read |
|---|---|
| Choosing the slow pattern to fix | [manifest.md](references/manifest.md) |
| Writing, changing, or migrating tests | [black-box-tests.md](references/black-box-tests.md) |
| Product verification commands, output, runs, proofs | [control-cli.md](references/control-cli.md) |
| Tracing slow feedback | [tracing.md](references/tracing.md) |
| Check targets, landing metadata, enforcement rollout | [enforcement.md](references/enforcement.md) |
| `AGENTS.md`, skills, moving docs out of the tree | [agent-context.md](references/agent-context.md) |

Never weaken an adopted check to pass. Whole-repo conformance is separate work. In a new repo, build the first real workflow and its correctness checks; add machinery only when it needs it.

## Verification

Prove what you delivered, not every capability here:
- **Speedup:** before-and-after numbers for the targeted cost on the chosen workflow, including process boundary and conditions.
- **Changed contract:** the [proof procedure](references/control-cli.md#proof).
- **Tracing:** a real run writes valid Chrome Trace JSON; an injected step delay appears as the top critical-path change in `<cli> trace`.
- **Enforcement:** the [landing-entrypoint proof](references/enforcement.md#proof), including candidate and metadata.
- **Cache or watcher:** matching inputs reuse evidence; changed inputs reject it after forwarding or child integration. A watcher observes its own workspace.
- **Edit loop:** a one-line edit reaches its verdict, rebuild included, faster than a model turn. Cache hits prove nothing here.
- **Navigation or diagnostics:** a fresh agent given a real bug report finds, reproduces, and proves the fix; count turns before and after.
- **Suite deletion:** the [replacement proof](references/black-box-tests.md#migrating-an-existing-suite). A failed pilot can stop a migration, never authorize deletion.
