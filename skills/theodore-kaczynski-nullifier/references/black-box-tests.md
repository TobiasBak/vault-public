# Black-box tests

A behavioral test supplies input through a published production contract and checks its specified output. Choose its [proof boundary](behavioral-boundaries.md) before choosing a driver. A **corpus case** is one scenario directory with input, expected output, and `case.toml`; the **corpus** is those scenarios. Public model and library contracts may instead use ordinary test targets.

## The box

- The box is the production contract: CLI, HTTP API, MCP server, file-in/file-out contract, or a library or model API with real consumers. An arbitrary internal module is not a product boundary, and a GUI is never a test boundary ([no GUI tests](behavioral-boundaries.md#no-gui-tests)). Backend behavior stays at its API; client rules use their production model.
- **Input:** the request plus starting state: files, operated dependencies' state, fake external services, clock, seeds.
- **Output:** the response plus effects seen in the environment: files written, rows in the product's database, messages in a fake mailbox, rows in a fake external system.
- **Run what the product operates.** A dependency the product deploys and runs, such as its database, queue, cache or object store, runs for real at the production version, started once in the warm environment. Each case gets its own database, schema, bucket or key prefix. A fake of it tests only the fake.
- **Fake what it doesn't.** Fakes replace only systems the product doesn't operate, never the repo's own code or an operated dependency. A fake answers from recorded real exchanges or the provider's published contract, never from a minimal shape the product happens to accept, and the `Behavior-Change:` trailer on a fake change names that source and version. Where the provider has a sandbox, send it the requests cases send the fake, on a schedule, and compare the answers; a difference is fake drift until shown otherwise and is fixed in the fake. An external command is faked by a stub first on `PATH` that records its arguments and stdin; the record is the effect.
- Hard-to-reach paths go through the environment only: a fake service returning 500, a full disk, a kill at a crash point, a scripted clock.
- Driving the app interactively, including through a browser MCP, is exploration: it reproduces bugs, and what it finds extends a model or API case. It never produces a verdict.

## Allowed case kinds

1. **Example:** input and expected output.
2. **Relation:** a stated relation between outputs of related inputs (rotation keeps volume; a second import changes nothing; parsing printed output returns the input). Inputs may be authored or [generated](#expected-output). A relation over generated inputs is a property test; its failing input goes through the reducer into the authored case it extends.
3. **Robustness:** generated input; no crash, no hang, within its deadline.
4. **Differential:** output matches a reference system on the same input.

Generation may find new failures, but it never carries a detection the gate requires. A required detection, such as a named mutant, is pinned as an authored request that detects it under every seed.

## Large scenario cases

- A case is a whole scenario, not one assertion, as large as its budget allows. Its starting state is as small as the behavior allows, not a copy of production size.
- When the interface takes a list of subjects, send one request per payload, operation, and set of call-level arguments: quote three SKUs in one `quote` call, not three calls. Different call-level arguments and separate rejection scenarios are separate requests.
- Extend a case before adding one. A new case needs an input no case can absorb: a conflicting starting state, a different kind, or a budget overrun. Never copy a scenario to vary one input; add the varied request to the case that already has the setup. Merging keeps the distinctions [tests.md](tests.md#classify) names.
- **Domain behavior is proved once,** at the cheapest entry point that runs its owning code. Each other published entry point gets one case for its own mechanism: argument and schema decoding, exit codes, output shape, help, and refusals specific to that surface. Where entry points share one dispatcher, a small equivalence sample runs the same operations through each and compares outputs. An entry point with its own implementation of a behavior is not covered through another.
- **A cross-cutting stage is proved in its own case.** Adding one more pipeline phase, platform or lane to every scenario multiplies suite time without new detection. Scenarios that pass through it supply its inputs; one case asserts its outcomes.
- Prove a write by reading it back through the interface or environment, never by the write's own response.
- If a scenario can't fit its budget, split off groups of behavior that run on their own; each case does its own startup, setup, readback, and teardown. Keep every original request and assertion exactly once and record where each went (a projection map). Extra setup may add requests, never replace assertions. Cases may share authored input files, never mutable starting state.
- Don't start a product-performance project to keep a giant case whole. Verify the projection map, independent lifecycles, and complete fresh output counts. A giant case that didn't finish is no throughput baseline.

## Forbidden

- Tests that drive a GUI, browser or accessibility tree, screenshot comparisons, and product hooks that exist only so tests can drive or observe a UI.
- Tests coupled to private helpers, internal fields or incidental call order. A production model's public output is a contract, not a diagnostic dump. The order of effects in the environment, such as a charge recorded before a shipment, is also output.
- Expected values whose only source is the code under test.
- Assertions on diagnostic stage dumps.
- Cases that share mutable starting state.
- Accepting many changed outputs at once without checking each.

## Case layout

```
corpus/<area>/<scenario>/
  input...      request and starting environment
  expected...   canonical output and effects
  case.toml     covers, oracle, tolerance, budget
```

- `covers` lists `<area>.<outcome>@<entry>` pairs. The outcome is what the user sees, never a test, function, or fixture.
- `oracle` identifies the independent authority for the expected values: the derivation itself, a spec section, or a reference system and version. Include enough provenance to find and judge the source. A published contract in this repo is valid when its authority is independent of the code under test; an implementation path or behavior copied into prose is not. Its prose is also where a case explains why the behavior is so.
- **The oracle never restates expected values.** It names the rule, inputs and arithmetic; the expected file holds the result, so the two cannot drift apart. History belongs in commit trailers, never in the oracle or a case description.
- Fields: `kind`, `covers`, `oracle`, `tolerance`, `budget_ms`, `budget_basis`, and `relations` for relation cases. No others.

```
corpus/pricing/discounts-and-rounding/
  payloads/order.xml
  requests.json
  expected.json
  case.toml
```

```toml
kind = "example"
covers = [
  "pricing.volume-discount@quote",
  "pricing.half-even-rounding@quote",
  "pricing.unknown-sku-refused@quote",
  "invoice.issue-from-quote@invoice",
]
budget_ms = 300
budget_basis = "warm in-process run 40 ms; 300 ms caps affected-case feedback"
tolerance = { rel = 1e-12 }
oracle = """
Price list 4.2: 10% off at qty >= 100, so 120 x 2.50 less 10%.
Price list 4.5: half-even to cents, applied to 0.125.
Price list 2.1: an unknown SKU is refused with UNKNOWN_SKU.
Invoicing spec 3.1: an invoice carries its quote's total unchanged.
"""
```

```json
[
  {"total": 270.0, "lines": [{"sku": "A1", "qty": 120, "net": 270.0}]},
  {"total": 0.12},
  {"raised": {"code": "UNKNOWN_SKU", "entity": "Z9"}},
  {"invoice": {"status": "issued", "total": 270.0}}
]
```

## Authority for expectations

Read the source and check each changed expectation against it. Record the relevant section, version, or derivation in the oracle; its presence and a `Behavior-Change:` trailer establish traceability, not truth. A file's location does not establish independence. A reference implementation that preserves a known bug is not authority for behavior the governing contract rejects. If authority is missing or conflicting, resolve the contract before accepting outputs. A passing case whose accepted output contradicts its authority is a wrong oracle, and its pass blesses the defect.

## Expected output

- **Independent source only:** the system being replaced, a reference tool, a spec, or a recorded hand derivation. The corpus is committed data; no script generates expected values. `accept` records output the agent checked against the named source.
- **Readable inputs.** Committed inputs are authored or exported and small enough to read. Generated input (deep nesting, long chains, noise, fine grids, fuzz) is never committed: the request names a builder, a small committed base, and parameters, and the runner builds it. The cache key covers builder source, base, and parameters, so a hit builds nothing. Builders are a fixed set owned by the runner and never compute expected values.
- **One canonicalizer** does all normalization: sorted keys, scrubbed random IDs and timestamps. Cases never normalize. IDs the interface hands back are output, never scrubbed: an echoed ID matches the request; an assigned one points to the object the input links it to. The canonical form covers every returned value (errors, NaN, infinities, signed zero, bytes, type tags, record fields, call arguments, references); fix gaps there, never in a case.
- **Record what the case covers.** A request selects, at the interface, the output its `covers` own, such as a query naming its results or a projection named in the request. A value another contract owns, such as a whole-bundle identity or a full derivation, is asserted only in its owner's case; repeating it elsewhere makes every change to that owner re-accept unrelated cases.
- **Bare values, exact match.** Within what a request records, a returned key the expected object lacks is a mismatch. The case tolerance applies to every number; a per-value tolerance is normalization and moves to the canonicalizer.
- **Matchers** mark exceptions, never the default, from a fixed set owned by the canonicalizer: tolerance override, range, one-of, any, pattern, unordered, enclosure (the true value lies within a bound the same output reports), and the canonical forms. One-of is for outputs the spec leaves open, never to hide nondeterminism. No other arithmetic, references, paths, or quantifiers; an expected file that computes is test code.
- **Relations.** A consistency property between outputs (parts sum to the total) is a named runner relation the case declares; where an independent value exists, write the value. A value the spec leaves to the implementation (an adaptive partition, a sampling start) is never copied from output; assert the property it must meet through a relation calling the public interface (samples lie within the reported deflection).
- Adding a matcher or relation is a design change, never a fix for one case.
- Agents read expected files on every failure, so size is cost: one line per request.
- Format changes go through one mechanical rewrite over all expected files. Any diff it doesn't explain is a behavior change.

## Prove the checker

The canonicalizer, comparator, runner and `accept` decide every verdict, so a blind spot in them passes every case it hides.

- Inject a fault into each component of the raw output, such as a type tag, record field, call argument, ID or reference, before normalization, and show the comparison fails. A fault injected after normalization proves nothing about what normalization discards.
- An allowed exception (unsupported, skipped, unproven) is accepted only when its eligibility is established independently of the side claiming it. Counting exceptions is not enforcement.
- The runner classifies each outcome. A product response that violates its expectation or response contract fails at its step. A crash, missing prerequisite or harness error is blocked. `accept` records only a completed mismatch, never a failed assertion or a blocked run.
- A static gate rejects the plausible bypass, such as an ordinary refactor or another syntax reaching the forbidden effect, not only the planted spelling.

## Runner

- Calls the real `main` in-process with the same arguments; a subprocess only when process behavior is the contract. A server under test starts once per identity or session the case needs, not once per request.
- One build and one warm environment for the whole selection. Each case gets its own temp dir, port, and fake state so cases run in parallel; parallelize when the selection overruns its budget.
- Clock and randomness injected; no real sleeps; seeds printed on failure.
- Runs affected cases by default when the writer invokes verification; the landing check stays static under the [enforcement rules](enforcement.md). If the full corpus fits the affected-case budget, always run it all and build no selection.
- Selects any single case. Iterate on the failing case alone and run the full selection once on final source; if the runner can't select one case, fix that first.
- **Budgets and deadlines are separate.** `budget_ms` is a feedback target: every overrun is reported as `budget 3s, took 3.09s` and never changes the verdict. The runner derives a hang deadline with wide headroom, such as ten times the budget; a case that reaches it is killed and fails, naming its request. Shared-host load must never fail a correct case.
- Writes the verdict cache when one is [adopted](manifest.md#cache-verdicts-only-when-measured).

## Failure output

A failing case prints only: case path and behavior, the **first mismatch**, a small diff around it, the `.actual` path, and one command rerunning only this case. Passing cases print nothing. The `.actual` file is written before the comparison and survives the run, including failures, timeouts, and teardown.

For diagnosis, `--emit=<stage>` exposes intermediate results without making them assertions. The reducer minimizes the failing input for its owning contract regression.

## Lifecycle

- A bug fix gets regression proof at its owning public contract. Extend an existing corpus scenario or model/library test, adding one only for distinct behavior or starting state. Run it on the pre-fix build first: it fails with the reported symptom, and that failure output is kept as evidence. A check that passes before the fix doesn't reproduce the bug.
- **Cover the class, not the witness.** Before fixing, list the sibling inputs the same defect reaches, such as other entry points, chain depths, orderings, aliases and identities, and extend the case with them. A fix that makes only the reported reproduction pass leaves the next review to find its sibling.
- Review existing cases and tests for keep, rewrite, merge or delete with [tests.md](tests.md).
- An internal rewrite changes no case. A case that breaks without a behavior change depends on internals; fix the case.
- When mutation testing is adopted, run it on a schedule. A surviving mutant needs a regression at the approved boundary, or evidence that its code is dead and should go. Line coverage is not measured.

## Migrating an existing suite

This procedure replaces a whole suite. GUI suites are deleted outright under the [no-GUI rule](behavioral-boundaries.md#no-gui-tests).

- Start only for a chosen outcome with explicit permission to delete the old suite.
- First identify the authoritative public contract and agreed replacements or cutovers, and confirm the proof and its source of truth still matter after them. If the old suite's backend is being replaced, shelve the migration and keep the suite; a result on one backend doesn't carry over.
- Read the old suite as a list of behaviors. Never port tests one to one; old names, grouping, and fixtures leave no trace. An old assertion that contradicts the current spec is a design difference to record, not a behavior to port. A pilot showing the migration infeasible or worthless can stop it, never authorize deletion without replacement proof.

1. Freeze the old suite and fixture builders. No edits except deletion.
2. Implement replacement proofs at the [appropriate boundaries](behavioral-boundaries.md). Corpus scenarios use the [finished shape](#case-layout).
3. Mutation-test the replacement proofs, then run the old suite only on mutants they missed. Sample at least a thousand mutants to estimate the old-suite-only kill rate; a hundred decides nothing.
   - Both suites first pass on the unmutated tree through the exact proof harness. A harness failing its baseline counts every mutant as killed.
   - Pilot fifty mutants. An old-only rate above a few percent is a harness bug until shown otherwise.
   - Estimate wall time from the pilot. Over an hour, change the method (cheaper build, mutants compiled once, fewer old-suite runs); never wait it out.
4. Extend the relevant replacement proof for each old-suite-only kill, or delete code established to be dead.
5. Delete the old suite, its fixtures, and every script that produced them.
6. Enforce the approved behavioral test boundaries.
