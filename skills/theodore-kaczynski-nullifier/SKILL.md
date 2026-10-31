---
name: theodore-kaczynski-nullifier
description: Diagnose and shape agent-maintained repositories so fresh agents can understand, change, verify and recover them. Use for structural repo reviews and redesigns, tangled ownership or coupling, failing checks, unclear runtime outcomes, partial failure, product verification, agent context or measured feedback bottlenecks.
---

# Theodore Kaczynski Nullifier

Build for fresh-agent autonomy: understanding the system, changing it correctly, establishing what actually happened, and recovering when reality disagrees. The codebase is its living documentation; prose keeps only what the executable system cannot adequately express. These are the [foundations](references/design-principles.md), not consequences of a particular tool.

## The loop

Start with a real product task and the outcome its users need, not a tooling checklist. For repository diagnosis, choose representative changes and follow their actual paths. For a new repository, design around its first useful workflow rather than a directory template.

1. **Understand:** find the published interface, authoritative contract, owning code, and boundaries where effects happen. Establish intended behavior independently of the implementation; identify compatibility obligations from consumers or persisted data.
2. **Diagnose and choose:** trace the decisions, callers and state writers behind the task. For structural work, use [repository diagnosis and design](references/repo-design.md) to separate symptoms from causes and compare coherent shapes. A smell is a lead, not a verdict; choose by the obligations removed from contributors and callers, not file counts or architectural fashion.
3. **Change:** repair the owning structure and bad examples, not just the symptom. Make known mistakes impossible or mechanically rejected where enforceable. Preserve the [chosen policies](#repository-rules); add machinery only for a demonstrated task gap, measured recurring cost, or broken contract.
4. **Establish outcomes:** execute the changed path through its published interface and read back its effects. Separate [static acceptance, observed behavior, and contract judgment](references/runtime-outcomes.md#evidence-and-authority). State the inputs, environment, scope, and anything blocked or unknown. [Explain any failure](references/runtime-outcomes.md#explain-a-failure) before fixing, retrying, or handing it off.
5. **Recover when needed:** inspect completed, incomplete, and uncertain effects at their owner before retrying. Use supported repair and verify the resulting state; a source revert does not undo external effects. Follow the [runtime outcome procedure](references/runtime-outcomes.md).

A missing answer is a task gap to fix at its owner, not a reason to build every capability here. Whole-repo conformance is separate work.

## Ownership

Use the shared platform for workspaces, warm state and landing. Build only the product-specific feedback it cannot provide.

- **gah:** workspace isolation, forwarding, conflicts, child integration, warm build-state forks, and landing through the repository check. Its help and session instructions own the procedure.
- **The kernel:** CPU and memory sharing. There is no host admission; entrypoints run commands directly and [lock only exclusive resources](references/control-cli.md#shared-resources) through their owning tool, never another scheduler.
- **The repository:** published contract, product state and recovery boundaries, verification inputs, cases, static checks, incremental builds, and diagnostics. Recurring verification goes through a [product verification CLI](references/control-cli.md); product operations stay at their owning interface.

Shared-tool help and active session instructions own delivery and authority policies. Self-contained guidance identifies these dependencies without copying their playbooks. Warm state and a clean merge are not behavioral proof; reuse evidence only when its [inputs still match](references/manifest.md#3-cache-verdicts).

## Repository rules

These are Tobias's chosen policies for agent-maintained repositories without human source review or repair. Changing them needs his explicit agreement, not an optimization argument. They keep understanding tied to the executable system rather than parallel commentary, and tests tied to user-visible behavior rather than implementation structure.

- **Zero comments:** no explanatory or doc comments, TODOs, banners, or commented-out code. A line-1 `#!` is not a comment.
- **Prose only in** root `AGENTS.md`, [skills](references/agent-context.md#skills), CLI `--help`, case records, and [published contract files](references/agent-context.md#what-stays-out) at exact gate-listed paths. No README.
- **Black-box contracts, not private internals:** tests exercise the appropriate production boundary, including a model's public API. `$review-test-quality` owns writing, judging, pruning and migrating tests, including the replacement proof an existing suite needs before deletion.
- **Searchable names:** name things so `rg` finds them.
- **Decode once, then trust types:** untrusted data becomes types that exclude invalid states at the boundary that owns it; inward code never re-checks what a type, schema or constructor guarantees. This does not make [changing facts timeless](references/repo-design.md#types-validation-and-changing-facts). Errors are handled only to recover, translate at a boundary or clean up, never swallowed, defaulted away or logged and continued. Single-use logic stays inline unless it owns a boundary or names a domain rule. Where a linter can reject redundant checks or discarded errors, enable it.

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
| Diagnosing source structure, choosing boundaries, planning a refactor, or shaping a new repo | [repo-design.md](references/repo-design.md) |
| Establishing runtime state, partial effects, or safe recovery; what evidence establishes | [runtime-outcomes.md](references/runtime-outcomes.md) |
| Writing, reviewing, pruning, or migrating tests; proof boundaries; real dependencies and fakes; GUI cases | `$review-test-quality` |
| Product verification commands, output, runs, proofs | [control-cli.md](references/control-cli.md) |
| Choosing and measuring a feedback cost to remove | [manifest.md](references/manifest.md) |
| Tracing slow feedback | [tracing.md](references/tracing.md) |
| Mechanical checks, candidate and metadata integration | [enforcement.md](references/enforcement.md) |
| `AGENTS.md`, skills, moving docs out of the tree | [agent-context.md](references/agent-context.md) |

## Verification

Prove what you delivered, not every capability here:
- **Structural diagnosis or redesign:** the [design proof](references/repo-design.md#proof), including the representative change, preserved contracts and remaining uncertainty. A diagnosis-only request ends with supported findings, not unsolicited edits.
- **Changed contract:** the [proof procedure](references/control-cli.md#proof), with expectations checked against their independent authority.
- **Bug fix, test change, or suite deletion:** the matching `$review-test-quality` verification.
- **Runtime understanding or recovery:** the [outcome proof](references/runtime-outcomes.md#proof), including relevant partial failure when recovery changes.
- **Agent-repo setup, navigation, or skill behavior:** run the changed guidance on a representative task yourself: the searches and commands it names reach the owning code, the change and its outcome check work, and supported recovery runs when needed. Don't stage a fresh agent; real sessions after landing are the remaining test. Claim a navigation improvement only from turn counts in real sessions before and after.
- **Failure diagnosability:** an injected failure leaves the compared values, inputs and environment in retained evidence, enough to name its cause without a rerun.
- **Speedup:** before-and-after numbers for the targeted cost on the chosen workflow, including process boundary and conditions.
- **Tracing:** a real run writes valid Chrome Trace JSON; an injected step delay appears as the top critical-path change in `<cli> trace`.
- **Enforcement:** the [landing-entrypoint proof](references/enforcement.md#proof), including candidate and metadata. It proves the implemented check, not semantic correctness beyond it.
- **Cache or watcher:** matching inputs reuse evidence; changed inputs reject it after forwarding or child integration. A watcher observes its own workspace.
- **Edit-loop speed:** a one-line edit reaches its verdict, rebuild included, faster than a model turn. Cache hits prove nothing here.
