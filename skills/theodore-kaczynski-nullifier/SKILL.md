---
name: theodore-kaczynski-nullifier
description: Build self-explanatory, hardened repositories that agents can understand, change safely, verify and recover. Use when designing agent-repo structure, product verification or agent context, diagnosing unclear runtime outcomes or partial failure, cutting measured feedback waits, or writing AGENTS.md.
---

# Theodore Kaczynski Nullifier

Build for fresh-agent autonomy: understanding the system, changing it correctly, establishing what actually happened, and recovering when reality disagrees. The codebase is its living documentation; prose keeps only what the executable system cannot adequately express. These are the [foundations](references/design-principles.md), not consequences of a particular tool.

## The loop

Start with a real product task and the outcome its users need, not a tooling checklist.

1. **Understand:** find the published interface, authoritative contract, owning code, and boundaries where effects happen. Establish intended behavior independently of the implementation; identify compatibility obligations from consumers or persisted data.
2. **Change:** repair the owning structure and bad examples, not just the symptom. Make known mistakes impossible or mechanically rejected where enforceable. Preserve the [chosen policies](#repository-rules); add machinery only for a demonstrated task gap, measured recurring cost, or broken contract.
3. **Establish outcomes:** execute the changed path through its published interface and read back its effects. Separate [static acceptance, observed behavior, and contract judgment](references/black-box-tests.md#evidence-and-authority). State the inputs, environment, scope, and anything blocked or unknown.
4. **Recover when needed:** inspect completed, incomplete, and uncertain effects at their owner before retrying. Use supported repair and verify the resulting state; a source revert does not undo external effects. Follow the [runtime outcome procedure](references/runtime-outcomes.md).

A missing answer is a task gap to fix at its owner, not a reason to build every capability here. In a new repo, build the first real workflow and its correctness checks. Whole-repo conformance is separate work.

## Ownership

Use the shared platform for workspaces, warm state, scheduling, and landing. Build only the product-specific feedback it cannot provide.

- **gah:** workspace isolation, forwarding, conflicts, child integration, warm build-state forks, and landing through the repository check. Its help and session instructions own the procedure.
- **heavy-lease:** host admission. Repository entrypoints [integrate admission](references/control-cli.md#host-admission), never implement another scheduler.
- **The repository:** published contract, product state and recovery boundaries, verification inputs, cases, static checks, incremental builds, and diagnostics. Recurring verification goes through a [product verification CLI](references/control-cli.md); product operations stay at their owning interface.

Shared-tool help and active session instructions own delivery and authority policies. Self-contained guidance identifies these dependencies without copying their playbooks. Warm state and a clean merge are not behavioral proof; reuse evidence only when its [inputs still match](references/manifest.md#3-cache-verdicts).

## Repository rules

These are Tobias's chosen policies for agent-maintained repositories without human source review or repair. Changing them needs his explicit agreement, not an optimization argument. They keep understanding tied to the executable system rather than parallel commentary, and tests tied to user-visible behavior rather than implementation structure.

- **Zero comments:** no explanatory or doc comments, TODOs, banners, or commented-out code. A line-1 `#!` is not a comment.
- **Prose only in** root `AGENTS.md`, [skills](references/agent-context.md#skills), CLI `--help`, case records, and [published contract files](references/agent-context.md#what-stays-out) at exact gate-listed paths. No README.
- **Only black-box tests, as few as possible:** input at the published interface, specified output out. Extend a case before adding one. Static checks, types, linters, and formatters cover the rest. Keep an existing suite until an authorized [migration](references/black-box-tests.md#migrating-an-existing-suite) proves its replacement.
- **Searchable names:** name things so `rg` finds them.

Case layouts, context templates, command names, and execution techniques are mechanisms, not these policies. Their reference contracts govern until an agreed replacement preserves the required behavior, safety, rationale, and consumers. Fix a wrong check against that contract; never weaken a correct check merely to pass.

## Where the why goes

Comments stay banned. A reason names and code can't show goes:
1. Into something that runs: a check whose failure states the reason and approved path, or a case's `oracle` explaining the behavior.
2. For a one-off decision no program can check, a `Why:` trailer in the final landed commit, found with `git log -S'<code>'` or `git blame`.

The [landing integration](references/enforcement.md#landing-metadata) must preserve applicable trailers through squashes and parent landings. Child commits alone are not their durable home. Other rationale belongs in issues or PRs.

## Faster feedback

**Agent thinking is the only acceptable bottleneck.** A tool call slower than a model turn needs a reason; a turn spent on an answer the repo could have supplied is waste. Optimize the complete edit-to-main loop, including navigation and coordination, without weakening evidence or recovery.

Use the [measured optimization loop](references/manifest.md#optimization-loop) beside product work, never as its precondition. Stop at the chosen target; further machinery needs a new demonstrated gap or measured cost.

## What to read

References define adopted capabilities, not a to-do list:

| Job | Read |
|---|---|
| Understanding the foundations or changing this skill | [design-principles.md](references/design-principles.md) |
| Establishing runtime state, partial effects, or safe recovery | [runtime-outcomes.md](references/runtime-outcomes.md) |
| Writing, changing, or migrating tests; judging evidence | [black-box-tests.md](references/black-box-tests.md) |
| Product verification commands, output, runs, proofs | [control-cli.md](references/control-cli.md) |
| Choosing and measuring a feedback cost to remove | [manifest.md](references/manifest.md) |
| Tracing slow feedback | [tracing.md](references/tracing.md) |
| Mechanical checks, candidate and metadata integration | [enforcement.md](references/enforcement.md) |
| `AGENTS.md`, skills, moving docs out of the tree | [agent-context.md](references/agent-context.md) |

## Verification

Prove what you delivered, not every capability here:
- **Changed contract:** the [proof procedure](references/control-cli.md#proof), with expectations checked against their independent authority.
- **Runtime understanding or recovery:** the [outcome proof](references/runtime-outcomes.md#proof), including relevant partial failure when recovery changes.
- **Agent-repo setup, navigation, or skill behavior:** a fresh agent uses the changed guidance on a representative task, finds the owning code, makes the change, establishes the actual outcome, and uses supported recovery when needed, without hidden context or human repair. Count turns before and after when claiming a navigation improvement.
- **Speedup:** before-and-after numbers for the targeted cost on the chosen workflow, including process boundary and conditions.
- **Tracing:** a real run writes valid Chrome Trace JSON; an injected step delay appears as the top critical-path change in `<cli> trace`.
- **Enforcement:** the [landing-entrypoint proof](references/enforcement.md#proof), including candidate and metadata. It proves the implemented check, not semantic correctness beyond it.
- **Cache or watcher:** matching inputs reuse evidence; changed inputs reject it after forwarding or child integration. A watcher observes its own workspace.
- **Edit-loop speed:** a one-line edit reaches its verdict, rebuild included, faster than a model turn. Cache hits prove nothing here.
- **Suite deletion:** the [replacement proof](references/black-box-tests.md#migrating-an-existing-suite). A failed pilot can stop a migration, never authorize deletion.
