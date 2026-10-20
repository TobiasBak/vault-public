# Black-box tests

A test is an input at the published interface and a specified output. Nothing else is a test. A **case** is one scenario directory with input, expected output, and `case.toml`; the **corpus** is all cases. Few cases, each covering as much as it can.

## The box

- The box is the published interface: CLI, HTTP API, file-in/file-out contract, or a library's public API. Nothing narrower; calling an internal module a "product" to test it is forbidden. A GUI is a thin shell over an API: the API is the box, and the GUI gets cases only for its own contract.
- **Input:** the request plus starting state: files, fake external services, clock, seeds.
- **Output:** the response plus effects seen in the environment: files written, messages in a fake mailbox, rows in a fake external system.
- Fakes replace external systems only, never the repo's own code. An external command is faked by a stub first on `PATH` that records its arguments and stdin; the record is the effect.
- Hard-to-reach paths go through the environment only: a fake service returning 500, a full disk, a kill at a crash point, a scripted clock.

## Allowed case kinds

1. **Example:** input and expected output.
2. **Relation:** a stated relation between outputs of related inputs (rotation keeps volume; a second import changes nothing).
3. **Robustness:** generated input; no crash, no hang, within budget.
4. **Differential:** output matches a reference system on the same input.

## Large scenario cases

- A case is a whole scenario, not one assertion, as large as its budget allows.
- When the interface takes a list of subjects, send one request per payload, operation, and set of call-level arguments: quote three SKUs in one `quote` call, not three calls. Different call-level arguments and separate rejection scenarios are separate requests.
- Extend a case before adding one. A new case needs an input no case can absorb: a conflicting starting state, a different kind, or a budget overrun.
- Each behavior-and-entry-point pair is covered by exactly one case, and every published entry point to a behavior is covered. Coverage through another entry point doesn't count.
- Prove a write by reading it back through the interface or environment, never by the write's own response.
- If a scenario can't fit its budget, split off groups of behavior that run on their own; each case does its own startup, setup, readback, and teardown. Keep every original request and assertion exactly once and record where each went (a projection map). Extra setup may add requests, never replace assertions. Cases may share authored input files, never mutable starting state.
- Don't start a product-performance project to keep a giant case whole. Verify the projection map, independent lifecycles, and complete fresh output counts. A giant case that didn't finish is no throughput baseline.

## Forbidden

- Unit tests, tests of internal modules, private access, assertions on call order or internal data.
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
  "pricing.volume-discount@invoice",
  "pricing.half-even-rounding@quote",
  "pricing.unknown-sku-refused@quote",
]
budget_ms = 300
budget_basis = "warm in-process run 40 ms; 300 ms caps affected-case feedback"
tolerance = { rel = 1e-12 }
oracle = """
Price list 4.2: 10% off at qty >= 100. 120 x 2.50 = 300.00, less 10% = 270.00.
Price list 4.5: half-even to cents. 0.125 -> 0.12.
Price list 2.1: an unknown SKU is refused with UNKNOWN_SKU.
"""
```

```json
[
  {"total": 270.0, "lines": [{"sku": "A1", "qty": 120, "net": 270.0}]},
  {"total": 270.0, "invoice": {"status": "issued", "total": 270.0}},
  {"total": 0.12},
  {"raised": {"code": "UNKNOWN_SKU", "entity": "Z9"}}
]
```

## Evidence and authority

| Evidence | Establishes | Does not establish |
|---|---|---|
| Static check acceptance | The candidate satisfies the implemented structural and metadata rules | Correct behavior, meaningful coverage, or an authoritative oracle |
| Behavioral execution and readback | The observed response and effects for the checked inputs, environment, and scope | General correctness, real-service delivery from a fake, or the authority of expected values |
| Judgment against the contract | The named source governs this behavior and the expected values follow from it | That the implementation actually produces those values without execution |

Read the source and check each changed expectation against it. Record the relevant section, version, or derivation in the oracle; its presence and a `Behavior-Change:` trailer establish traceability, not truth. A file's location does not establish independence. A reference implementation that preserves a known bug is not authority for behavior the governing contract rejects. If authority is missing or conflicting, resolve the contract before accepting outputs.

## Expected output

- **Independent source only:** the system being replaced, a reference tool, a spec, or a recorded hand derivation. The corpus is committed data; no script generates expected values. `accept` records output the agent checked against the named source.
- **Readable inputs.** Committed inputs are authored or exported and small enough to read. Generated input (deep nesting, long chains, noise, fine grids, fuzz) is never committed: the request names a builder, a small committed base, and parameters, and the runner builds it. The cache key covers builder source, base, and parameters, so a hit builds nothing. Builders are a fixed set owned by the runner and never compute expected values.
- **One canonicalizer** does all normalization: sorted keys, scrubbed random IDs and timestamps. Cases never normalize. IDs the interface hands back are output, never scrubbed: an echoed ID matches the request; an assigned one points to the object the input links it to. The canonical form covers every returned value (errors, NaN, infinities, signed zero, bytes); fix gaps there, never in a case.
- **Bare values, exact match.** A returned key the expected object lacks is a mismatch. The case tolerance applies to every number; a per-value tolerance is normalization and moves to the canonicalizer.
- **Matchers** mark exceptions, never the default, from a fixed set owned by the canonicalizer: tolerance override, range, one-of, any, pattern, unordered, enclosure (the true value lies within a bound the same output reports), and the canonical forms. One-of is for outputs the spec leaves open, never to hide nondeterminism. No other arithmetic, references, paths, or quantifiers; an expected file that computes is test code.
- **Relations.** A consistency property between outputs (parts sum to the total) is a named runner relation the case declares; where an independent value exists, write the value. A value the spec leaves to the implementation (an adaptive partition, a sampling start) is never copied from output; assert the property it must meet through a relation calling the public interface (samples lie within the reported deflection).
- Adding a matcher or relation is a design change, never a fix for one case.
- Agents read expected files on every failure, so size is cost: one line per request.
- Format changes go through one mechanical rewrite over all expected files. Any diff it doesn't explain is a behavior change.

## Runner

- Calls the real `main` in-process with the same arguments; a subprocess only when process behavior is the contract.
- One build and one warm environment for the whole selection. Each case gets its own temp dir, port, and fake state so cases run in parallel; parallelize when the selection overruns its budget.
- Clock and randomness injected; no real sleeps; seeds printed on failure.
- Runs affected cases by default when the writer invokes verification; the [landing check stays static](enforcement.md#checks). If the full corpus fits the affected-case budget, always run it all and build no selection.
- Reports every case over budget. A hung case is killed at its budget and fails, naming its request.
- Writes the verdict cache and feeds the watcher.

## Failure output

A failing case prints only: case path and behavior, the **first mismatch**, a small diff around it, the `.actual` path, and one command rerunning only this case. Passing cases print nothing. The `.actual` file is written before the comparison and survives the run, including failures, timeouts, and teardown.

To localize without unit tests: `--emit=<stage>` dumps intermediate stages for diagnosis (never asserted on), and the reducer shrinks a failing input to a minimal one that extends a case.

## Lifecycle

- Every bug fix extends a case with the minimized input, or adds one when none can absorb it.
- A case covering nothing another case doesn't is merged or deleted.
- An internal rewrite changes no case. A case that breaks without a behavior change depends on internals; fix the case.
- When mutation testing is adopted, run it on a schedule. Each surviving mutant extends a case until killed, or marks dead code to delete. Line coverage is not measured.

## Migrating an existing suite

- Start only for a chosen outcome with explicit permission to delete the old suite.
- First identify the authoritative public contract and agreed replacements or cutovers, and confirm the proof and its source of truth still matter after them. If the old suite's backend is being replaced, shelve the migration and keep the suite; a result on one backend doesn't carry over.
- Read the old suite as a list of behaviors. Never port tests one to one; old names, grouping, and fixtures leave no trace. A pilot showing the migration infeasible or worthless can stop it, never authorize deletion without replacement proof.

1. Freeze the old suite and fixture builders. No edits except deletion.
2. Write large cases in the [finished shape](#case-layout) for those behaviors.
3. Mutation-test the corpus, then run the old suite only on mutants the corpus missed. Sample at least a thousand mutants to estimate the old-suite-only kill rate; a hundred decides nothing.
   - Both suites first pass on the unmutated tree through the exact proof harness. A harness failing its baseline counts every mutant as killed.
   - Pilot fifty mutants. An old-only rate above a few percent is a harness bug until shown otherwise.
   - Estimate wall time from the pilot. Over an hour, change the method (cheaper build, mutants compiled once, fewer old-suite runs); never wait it out.
4. Each mutant only the old suite kills extends a case, or its code is deleted as dead.
5. Delete the old suite, its fixtures, and every script that produced them.
6. Turn on the unit-test ban.
