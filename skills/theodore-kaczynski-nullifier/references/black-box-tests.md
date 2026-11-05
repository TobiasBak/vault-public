# Black-box tests

A behavioral test supplies input through a published production contract and asserts the values that contract owns against expectations written from an independent authority. Choose its [proof boundary](behavioral-boundaries.md) before choosing a driver. Tests live in the language's ordinary test setup with thin helpers; no repository-specific case format, corpus layout or record files.

## The box

- The box is the production contract: CLI, HTTP API, MCP server, file-in/file-out contract, or a library or model API with real consumers. An arbitrary internal module is not a product boundary, and a GUI is never a test boundary ([no GUI tests](behavioral-boundaries.md#no-gui-tests)). Backend behavior stays at its API; client rules use their production model.
- **Input:** the request plus starting state: files, operated dependencies' state, fake external services, clock, seeds.
- **Output:** the response plus effects seen in the environment: files written, rows in the product's database, messages in a fake mailbox, rows in a fake external system.
- **Run what the product operates.** A dependency the product deploys and runs, such as its database, queue, cache or object store, runs for real at the production version, started once in the warm environment. Each test gets its own database, schema, bucket or key prefix. A fake of it tests only the fake.
- **Fake what it doesn't.** Fakes replace only systems the product doesn't operate, never the repo's own code or an operated dependency. A fake answers from recorded real exchanges or the provider's published contract, never from a minimal shape the product happens to accept, and cites that source and version like any expectation. Where the provider has a sandbox, send it the requests tests send the fake, on a schedule, and compare the answers; a difference is fake drift until shown otherwise and is fixed in the fake. An external command is faked by a stub first on `PATH` that records its arguments and stdin; the record is the effect.
- Hard-to-reach paths go through the environment only: a fake service returning 500, a full disk, a kill at a crash point, a scripted clock.
- Driving the app interactively, including through a browser MCP, is exploration: it reproduces bugs, and what it finds extends a model or API test. It never produces a verdict.

## What proves what

Each obligation has one kind of proof. Choose by what the behavior is:

| Behavior | Proof |
|---|---|
| A domain rule with an authority: a statute, spec section, price list, protocol | An [example](#examples): authored input and the owned values the authority dictates |
| An invariant over stored or returned state | [The product enforces it](#invariants-belong-to-the-product); its self-audit reports what slips through |
| An engine with a large input space: parser, interpreter, solver, compiler, query planner | [Generated checks](#engines) against a reference or properties |
| Each published entry point | One [smoke run](#smoke-runs) |
| A schema or data migration | The [migration guards itself](#migrations) on the data it upgrades |
| A non-deterministic component, such as a model call | A [benchmark](#benchmarks), reported and never gated |

## Examples

- **Expected values come from the authority, never from output.** Write each one from the source before running: the spec, the reference system, or a short hand derivation. Never run the code and paste its result in; no snapshot, golden file or accept command records output as truth. A value you can't state without running the code has no authority yet: resolve the contract first. A reference implementation that preserves a known bug is not authority for behavior the governing contract rejects.
- **One line of authority per example:** the source and, only when the value isn't read straight off it, the derivation, such as `Price list 4.2: 10% off at qty >= 100, so 120 x 2.50 x 0.9`. The example helper takes it as a required argument and prints it on failure. No narrative, restated steps or history; a decision's reason goes in an ADR when it clears the bar. A changed rule changes its examples' values and citations in the same commit.
- **Assert only the values the example owns:** the total the rule computes, the refusal code, the row the write created. Never compare a whole response, file or document. A value another contract owns, such as a whole-bundle identity, is asserted only at its owner, so changing that owner touches only its tests.
- **Exact match.** A tolerance or rounding rule belongs to the value's type or its authority, stated once, never per example.
- **Inputs discriminate:** the plausible wrong implementation must produce a different value ([evidence](tests.md#evidence)).
- Prove a write by reading it back through the interface or environment, never by the write's own response.
- Domain behavior is proved once, at the cheapest entry point that runs its owning code. Parameterize over inputs that share setup; never copy a test to vary one input. A test's starting state is as small as the behavior allows.
- Committed inputs are authored and small enough to read. Generated input (deep nesting, long chains, fine grids) is built by the test from a small committed base and parameters, never committed, and the builder never computes expected values.

## Invariants belong to the product

- An invariant over state, such as balanced ledgers, every record having an owner, or no two confirmed values overlapping, lives where the product enforces it: a type that can't represent the violation, a database constraint or trigger, a refusal at the boundary that accepts the write. Don't restate it as a test of every operation that could break it.
- What can't be enforced at write time goes into a self-audit the product ships, such as `<product> check`, which reads stored state and reports each violation with its location and reason. It runs on real data, so it catches what authored inputs never reach.
- Prove each audit rule and constraint once: a planted violation in a throwaway store is reported or refused, and a clean store passes.

## Engines

- Generate inputs and compare against a reference implementation, or assert properties: round-trip (`parse(print(x)) == x`), idempotence, an algebraic law, agreement between two strategies the engine offers. Use the language's property-testing library.
- The reference is independent: another implementation, a formal model, or a slow obvious version. The same code run twice proves nothing.
- Draw inputs from real workloads too, such as the product's own definitions and recorded requests, so generation reaches the shapes users write.
- Robustness: generated malformed input never crashes or hangs within its deadline. Refusals consumers rely on are a small table of input and expected error.
- Generation may find new failures, but it never carries a required detection. A generated failure is reduced and pinned as an authored input that fails under every seed.

## Smoke runs

- One per published entry point: the real binary or server through a short representative session, then a clean self-audit and a handful of owned values. It covers what that surface owns: argument and schema decoding, exit codes, output shape, help and its own refusals. Where entry points share one dispatcher, a small sample runs the same operations through each and compares outputs. An entry point with its own implementation of a behavior is not covered through another.
- A cross-cutting stage, such as one more platform or pipeline phase, gets its own run; never add it to every test.

## Migrations

- No fixtures of old data. A store written by an earlier version is legacy the day the next migration lands, and a test per schema version only grows.
- A migration runs in one transaction with the self-audit before commit, so a bad migration refuses on the store it meets, real data included, and leaves it untouched.
- A landed migration is never edited; a fix is a new migration. A static check rejects the edit.
- While writing a migration, run it once on a copy of a store the current release wrote; that is development evidence, not a kept test.

## Benchmarks

- A non-deterministic component is measured, not gated: a truth set of authored inputs and correct outputs, written from authority like examples, scored per item over several runs with recall, precision or task success, retries, time and cost.
- Keep the baseline beside each change's result. A drop shows in the report, never as a red gate.
- The deterministic code around the component is tested with fakes answering from recorded real responses.

## Forbidden

- GUI tests of any kind, and product hooks that exist only for them ([no GUI tests](behavioral-boundaries.md#no-gui-tests)).
- Tests coupled to private helpers, internal fields or incidental call order. A production model's public output is a contract, not a diagnostic dump. The order of effects in the environment, such as a charge recorded before a shipment, is also output.
- Expected values whose only source is the code under test: snapshots, golden files and accept flows.
- Whole-output comparisons and assertions on diagnostic dumps.
- Tests restating an invariant the product enforces.
- Tests that share mutable starting state.
- A gate on a non-deterministic component.

## Prove the checker

The self-audit, comparators and property assertions decide verdicts, so a blind spot passes everything it hides.

- Show each comparison fails on a deliberate fault before relying on it: a planted violation for the audit, a wrong output for a differential, a wrong value for an example helper. A fault injected after normalization proves nothing about what normalization discards.
- An allowed exception (unsupported, skipped, unproven) is accepted only when its eligibility is established independently of the side claiming it. Counting exceptions is not enforcement.
- A crash, missing prerequisite or harness error is blocked, never a pass or a product failure.

## Runner

- The language's test runner, with thin glue. Call the real entry point in-process; a subprocess only when process behavior is the contract, as in smoke runs. A server under test starts once per identity or session a test needs.
- One build and one warm environment for the whole selection. Each test gets its own temp dir, port and fake state so tests run in parallel.
- Clock and randomness injected; no real sleeps; seeds printed on failure.
- Affected tests run by default when the writer invokes verification; the landing check stays static under the [enforcement rules](enforcement.md). If the full suite fits the affected-test budget, run it all and build no selection.
- Any single test runs by name. Iterate on the failing test alone and run the full selection once on final source.
- **Budgets and deadlines are separate.** A tier's budget is a feedback target: overruns print `budget 3s, took 3.09s` and never change the verdict. A hang deadline with wide headroom, such as ten times the budget, kills the test and fails it by name. Shared-host load must never fail a correct test.

## Failure output

A failing test prints only its name, its authority line, the owned value's expected and actual, the inputs that produced them, and one command rerunning only it. Passing tests print nothing. The run's artifacts keep that output through failures, timeouts and teardown.

For diagnosis, a product diagnostic flag exposes intermediate results without making them assertions. The reducer minimizes a failing generated input into its pinned regression.

## Lifecycle

- A bug fix gets regression proof at its owning contract: extend the example, audit rule, property or smoke run that owns the behavior, adding a test only for distinct behavior or starting state. Run it on the pre-fix build first: it fails with the reported symptom, and that failure output is kept as evidence. A check that passes before the fix doesn't reproduce the bug.
- **Cover the class, not the witness.** Before fixing, list the sibling inputs the same defect reaches, such as other entry points, chain depths, orderings, aliases and identities, and extend the test with them. A fix that makes only the reported reproduction pass leaves the next review to find its sibling.
- Review existing tests for keep, rewrite, merge or delete with [tests.md](tests.md).
- An internal rewrite changes no test. A test that breaks without a behavior change depends on internals; fix the test.
- Line coverage is not measured.

## Migrating an existing suite

This procedure replaces a whole suite. GUI suites are deleted outright under the [no-GUI rule](behavioral-boundaries.md#no-gui-tests).

- Start only for a chosen outcome with explicit permission to delete the old suite.
- First identify the authoritative public contract and agreed replacements or cutovers, and confirm the proof and its source of truth still matter after them. If the old suite's backend is being replaced, shelve the migration and keep the suite; a result on one backend doesn't carry over.
- Read the old suite as a list of behaviors. Never port tests one to one; old names, grouping, and fixtures leave no trace. An old assertion that contradicts the current spec is a design difference to record, not a behavior to port. A recorded expectation with no authority is not ported: find its authority or let it go.

1. List every behavior the old suite asserts and its fate: a replacement proof in the [shape it needs](#what-proves-what), the existing check that already owns it, or dropped with the reason (no authority, owned elsewhere, contradicts the spec).
2. Implement the replacement proofs and run them.
3. Delete the old suite, its fixtures, and every script that produced them. No check asserts the deletion.
4. Enforce the approved behavioral test boundaries.
