---
name: theodore-kaczynski-nullifier
description: Diagnose and shape agent-maintained repositories so fresh agents can understand, change, verify and recover them. Use for structural repo reviews and redesigns, tangled ownership or coupling, recurring mistakes and review feedback worth enforcing, failing checks, writing, reviewing, pruning or migrating tests, unclear runtime outcomes, partial failure, product verification, agent context or measured feedback bottlenecks.
---

# Theodore Kaczynski Nullifier

Tobias's repositories are changed by agents and reviewed by no human, so the repository itself has to carry everything a fresh agent needs. A fresh agent should be able to find the owning code, change it, prove the change works through the product's own interface, and recover when reality disagrees, without asking anyone. The code is the documentation; prose keeps only what the running system can't express. The [foundations](references/design-principles.md) explain why, independent of any tool.

## The loop

Start from a real product task and the outcome its users need, not from a tooling checklist. To diagnose a repository, pick representative changes and follow the paths they actually take. For a new repository, build its first useful workflow instead of a directory template.

1. **Understand.** Find the published interface, the authoritative contract, the owning code and the boundaries where effects happen. Establish the intended behavior from a source other than the implementation, and list the compatibility obligations that consumers or persisted data impose. When the domain's terms are vague, contested or disagree with the code, settle them with the `domain-modeling` skill before choosing structure; it owns `GLOSSARY.md` and `docs/adr/`. Done when you can name the owner and the contract for the task.
2. **Diagnose and choose.** Trace the decisions, callers and state writers behind the task. For structural work, use [repository diagnosis and design](references/repo-design.md) to separate symptoms from causes and compare coherent shapes. Treat a smell as a lead to investigate. Choose by the obligations a design removes from contributors and callers, not by file count or architectural fashion.
3. **Change.** Repair the owning structure and the bad examples agents would copy, not just the symptom. Where a known mistake can be rejected mechanically, make it impossible or make a check reject it. Keep the [chosen policies](#repository-rules). Add machinery only for a demonstrated task gap, a measured recurring cost or a broken contract.
4. **Establish outcomes.** Run the changed path through its published interface and read back its effects. Keep [static acceptance, observed behavior and contract judgment](references/runtime-outcomes.md#evidence-and-authority) separate. State the inputs, environment and scope, and anything blocked or unknown. [Explain any failure](references/runtime-outcomes.md#explain-a-failure) before you fix, retry or hand it off.
5. **Recover when needed.** Before retrying, inspect which effects completed, which didn't and which are uncertain, at the component that owns them. Use the supported repair and verify the resulting state. Reverting source does not undo external effects. Follow the [runtime outcome procedure](references/runtime-outcomes.md).

When the repository can't answer a question the task needs, fix that gap at its owner. That is not a reason to build every capability this skill describes. Whole-repo conformance is separate work; for a whole-codebase untangling pass, use the `untangle-codebase` skill.

## Ownership

Use the shared platform for workspaces, warm state and landing, and build only the product-specific feedback it can't provide.

- **gah** owns workspace isolation, forwarding, conflicts, child integration, warm build-state forks, and landing through the repository's check. Its help text and session instructions own the procedure.
- **The kernel** shares CPU, and each heavy job gets a memory cap. There is no host admission: entrypoints run commands directly and [lock only exclusive resources](references/control-cli.md#shared-resources) through the tool that owns them, never through another scheduler.
- **The repository** owns its published contract, product state and recovery boundaries, verification inputs, tests, static checks, incremental builds and diagnostics. Recurring verification goes through a [product verification CLI](references/control-cli.md). Product operations stay at the interface that owns them.

The shared tools' help and the active session instructions own delivery and authority policy. Name these dependencies; don't copy their playbooks. A warm cache and a clean merge prove nothing about behavior. Reuse evidence only while its [inputs still match](references/manifest.md#cache-verdicts-only-when-measured).

## Repository rules

These are Tobias's chosen policies for repositories that agents maintain without human source review or repair. Changing one needs his explicit agreement; an optimization argument is not enough. Together they keep understanding in the running system instead of in commentary that drifts, and keep tests tied to what users see instead of to how the code is built.

- **Zero comments.** Source carries no explanatory or doc comments, TODOs, banners or commented-out code. A line-1 `#!` is not a comment. A reason goes where [the why goes](#where-the-why-goes).
- **Prose lives only in** root `AGENTS.md`, [skills](references/agent-context.md#skills), CLI `--help`, a test's one-line authority, the [domain glossary and ADRs](references/agent-context.md#owners), and [published contract files](references/agent-context.md#what-stays-out) at exact paths the gate lists. There is no README.
- **Tests are black-box contracts.** They exercise the appropriate production boundary, which includes a model's public API, and never private internals. [Tests](references/tests.md) owns writing, judging, pruning and migrating them, including replacing an existing suite.
- **No GUI tests.** UI rules live in a production model that tests prove through its API; [the rule](references/behavioral-boundaries.md#no-gui-tests) owns what counts as a GUI test.
- **Searchable names.** Name things so `rg` finds them.
- **Decode once, then trust types.** Untrusted data becomes types that exclude invalid states at the boundary that owns it, and inward code relies on what a type, schema or constructor guarantees without checking it again. This does not make [changing facts timeless](references/repo-design.md#types-validation-and-changing-facts). Handle an error only to recover, to translate it at a boundary or to clean up; never swallow it, default it away, or log it and continue. Keep single-use logic inline unless it owns a boundary or names a domain rule. Where a linter can reject redundant checks or discarded errors, turn that lint on.

Test helpers, context templates, command names and execution techniques are mechanisms, not these policies. Their reference contracts govern until an agreed replacement keeps the required behavior, safety, rationale and consumers. Fix a check that contradicts its contract; never weaken a correct check to make it pass.

## Where the why goes

Comments stay banned. When names and code can't show a reason, put it in the first place that fits:

1. **Something that runs:** a check whose failure states the reason and the approved path, a product refusal or self-audit message, or the authority line an example prints when it fails.
2. **A published contract file:** one line, for a contract Tobias decided that no single test owns, such as a version or compatibility rule.
3. **An ADR in `docs/adr/`:** for a decision no program can check that clears the `domain-modeling` skill's ADR bar. That skill owns writing ADRs and treating them as dated evidence, not rules.

The reason for one change goes in a `Why:` trailer in the commit that lands it; Tobias's repositories land on main without PRs. An unresolved decision goes in an issue.

## Faster feedback

**Agent thinking is the only acceptable bottleneck.** A tool call slower than a model turn needs a reason, and a turn spent finding an answer the repository could have supplied is waste. Optimize the whole loop from edit to main, including navigation and coordination, without weakening evidence or recovery.

Run the [measured optimization loop](references/manifest.md#optimization-loop) beside product work; it is never a precondition for it. Stop at the chosen target. More machinery needs a new demonstrated gap or measured cost.

**Small beats complete.** Verification machinery is product code with its own bugs. Use the language's build tool and test runner with thin glue. Adopt a cache, watcher, trace or custom runner only after a trial shows it pays, and remove one that doesn't. Bound memory per job instead of adding host-wide locks or queues anywhere, delegate briefs included ([why](references/manifest.md#bound-memory-not-concurrency)), and report any wait that stops making progress.

## What to read

The references describe adopted capabilities, not a to-do list. Read the one that matches the job:

| Job | Read |
|---|---|
| Understanding the foundations or changing this skill | [design-principles.md](references/design-principles.md) |
| Diagnosing source structure, choosing boundaries, planning a refactor, or shaping a new repo | [repo-design.md](references/repo-design.md) |
| Establishing runtime state, partial effects, or safe recovery; what evidence establishes | [runtime-outcomes.md](references/runtime-outcomes.md) |
| Writing, reviewing, pruning, or migrating tests; proof boundaries; real dependencies and fakes; budgets | [tests.md](references/tests.md) |
| Product verification commands, output, runs, proofs | [control-cli.md](references/control-cli.md) |
| Choosing and measuring a feedback cost to remove; locks, memory, caches | [manifest.md](references/manifest.md) |
| Mechanical checks, turning mistakes and their history into checks, candidate and metadata integration | [enforcement.md](references/enforcement.md) |
| `AGENTS.md`, skills, moving docs out of the tree | [agent-context.md](references/agent-context.md) |

## Verification

Prove what you delivered, not every capability here. Match the proof to the work:

- **Structural diagnosis or redesign:** the [design proof](references/repo-design.md#proof), with the representative change, the contracts kept and what remains uncertain. A request for diagnosis only ends with supported findings, not edits nobody asked for.
- **Changed contract:** the [proof procedure](references/control-cli.md#proof), with expectations checked against their independent authority.
- **Bug fix, test change or suite deletion:** the matching [test verification](references/tests.md#verification).
- **Runtime understanding or recovery:** the [outcome proof](references/runtime-outcomes.md#proof), including the relevant partial failure when recovery changes.
- **Agent-repo setup, navigation or skill behavior:** run the changed guidance on a representative task yourself. The searches and commands it names reach the owning code, the change and its outcome check work, and the supported recovery runs when needed. Don't stage a fresh agent; real sessions after landing are the remaining test. Claim a navigation improvement only from turn counts in real sessions before and after.
- **Failure diagnosability:** an injected failure leaves the compared values, inputs and environment in retained evidence, enough to name its cause without a rerun.
- **Speedup:** before-and-after numbers for the targeted cost on the chosen workflow, with the process boundary and conditions.
- **Enforcement:** the [landing-entrypoint proof](references/enforcement.md#proof), including candidate and metadata. It proves the implemented check, not semantic correctness beyond it.
- **Cache:** matching inputs reuse evidence; changed inputs reject it after forwarding or child integration; logged hits show the saving the trial claimed.
- **Edit-loop speed:** a one-line edit reaches its verdict, rebuild included, faster than a model turn. Cache hits prove nothing here.
