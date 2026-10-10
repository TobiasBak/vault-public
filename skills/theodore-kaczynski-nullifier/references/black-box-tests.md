# Black-box tests

A test is an input at the published interface and a specified output. Nothing else is a test. Few cases, each covering as much as it can.

## The box

- **The box is the repository's published interface:** CLI, HTTP API, file-in/file-out contract, or a library's public API. Nothing narrower. Declaring an internal module a "product" to test it is forbidden.
- **Input:** the request plus the environment's starting state: files, fake external services, clock, seeds.
- **Output:** the response plus effects observed in the environment: files written, messages in a fake mailbox, rows in a fake external system.
- Fakes replace external systems only. Never the repository's own code.
- An external command is faked by a stub first on `PATH` that records its arguments and stdin. The record is the effect.

## Allowed case kinds

1. **Example:** input and expected output.
2. **Relation:** a stated relation between outputs of related inputs. Rotation preserves volume; importing twice is idempotent.
3. **Robustness:** built input; no crash, no hang, within budget.
4. **Differential:** output matches an oracle system on the same input.

## Fat cases

- A case is a scenario, not an assertion. It covers every behavior one input can reach.
- One request per payload, operation, and call-level arguments when the interface takes a list of subjects. Repeating a call per subject is the one-assert-per-test habit at request level. Different call-level arguments and separate rejection scenarios are separate requests.
- Extend an existing case before adding one. A new case needs an input no existing case can absorb: a conflicting starting state, a different case kind, or a budget overrun.
- Each behavior and entry-point pair is covered by exactly one case.
- Every published entry point to a behavior is covered. Coverage through another entry point doesn't count.
- A write is proven by reading it back through the interface or the environment, never by the write's own response.
- The first divergence localizes failures. Small cases buy nothing.

## Forbidden

- Unit tests, tests of internal modules, private access, assertions on call sequences or internal data.
- Expected values whose only source is the code under test.
- Assertions on diagnostic stage dumps.
- Splitting a scenario into cases that share a starting state.
- Mass-blessing.

## Case layout

```
corpus/<area>/<scenario>/
  input...      request and starting environment
  expected...   canonical output and effects
  case.toml     covers, oracle, tolerance, budget
```

- `covers` lists `<area>.<outcome>@<entry>` pairs. The outcome names what the user observes, never a test, function, or fixture.
- The oracle is the derivation itself, a spec section, or an oracle system and version. Never a path in this repository.
- Fields: `kind`, `covers`, `oracle`, `tolerance`, `budget_ms`, `budget_basis`, and `relations` for relation cases. No others.

A finished case:

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

## Expected output

- From an independent source only: the system being replaced, a reference tool, a spec, or a recorded hand derivation.
- The corpus is committed data. No script generates expected values; `accept` records output the agent has checked against the named source.
- Committed inputs are authored or exported and small enough to read. Built input (deep nesting, long chains, repeated noise, refined grids, fuzz) is never committed: the request names a builder, a small committed base, and parameters; the runner builds it. The cache key covers the builder's source, the base, and the parameters, so a cache hit builds nothing. Builders are a closed set owned by the runner and never compute expected values.
- One canonicalizer owns normalization: sorted keys, scrubbed nondeterministic IDs and timestamps. Cases never normalize. Identifiers the interface hands back to callers are output, never scrubbed. Their source is the input and the output's own structure: an echoed identifier matches the request or input, and an assigned one resolves to the object the input relates it to.
- The canonical form covers every value the interface returns: errors, non-finite and signed-zero floats, bytes. A gap is fixed in the canonicalizer, never worked around in a case.
- Expected files hold bare values. Objects match closed: a returned key the expected object omits is a divergence. The case tolerance applies to every number. A matcher marks an exception only, never the default.
- Matchers are a small closed set owned by the canonicalizer: tolerance override, range, one-of, any, pattern, unordered, enclosure (the true value lies within a bound the same output reports), and the canonical forms. One-of is for outputs the spec leaves open, never for hiding a nondeterministic one. No other arithmetic, references, paths, or quantifiers. An expected file that computes is test code.
- A consistency property between outputs (parts sum to the total, a reversed input gives the same answer) is a named relation in the runner, declared by the case. Where an independent value exists, write the value instead.
- Adding a matcher or relation is a design change, never a fix for one case.
- Where the spec leaves a value to the implementation (an adaptive partition, a sampling start), never copy it from output. Assert the contract it must meet through a relation that calls the public interface: samples lie within the reported deflection; reported parameters evaluate to the reported point.
- Agents read expected files on every failure. Their size is cost. The canonical writer emits one line per request.
- Tolerance lives on the case. A tolerance computed per value is normalization; hoist it.
- Format changes go through one mechanical rewrite script over every expected file. Any diff the script doesn't explain is a behavior change.

## Runner

- Calls the real entrypoint in-process: same arguments, same `main`. A subprocess only when the process is the contract.
- One build, one warm environment, the whole selection.
- Hermetic: per-case temp dir, port, and fake state, so cases can run in parallel. Parallelize when the selection overruns its budget.
- Clock and randomness injected. No real sleeps. Seeds printed on failure.
- Runs the cases affected by the diff; the full corpus once on the final head. When the full corpus fits the affected-case budget, every run is full; don't build dependency selection.
- Reports every case over budget. A hung case is killed at its budget and reported as that case's failure, with the request it was in.
- Writes to the verdict cache and serves the watcher.

## Failure output

A failing case prints only:
- case path and behavior
- the **first divergence**
- a minimal diff around it
- the `.actual` file path
- one command that reruns only this case

Passing cases print nothing.

## Localizing without unit tests

- **Stage dumps:** `--emit=<stage>` writes intermediate stages for diagnosis. Never asserted on.
- **Reducer:** shrinks a failing input to a minimal failing one, which extends a case.

## Hard-to-reach paths

Through the environment only: a fake service returning 500, a full disk, a kill at a crash point, a scripted clock.

A GUI is a thin shell over an API. The API is the box; the GUI gets only cases for its own contract.

## Coverage

Mutation testing on a schedule. Each surviving mutant extends a case until it dies, or is dead code to delete. Line coverage is not measured.

## Lifecycle

- Every bug fix extends a case with the minimized input, or adds one when none can absorb it.
- A case that covers nothing another case doesn't is merged or deleted.
- An internal rewrite changes no case. A case that breaks without a behavior change leaked internals; fix the case.

## Migrating an existing suite

Read the old suite as a list of behaviors. Never port tests one to one: names, grouping, and fixtures of the old suite leave no trace in the corpus.

1. Freeze the old suite and its fixture builders. No edits except deletion.
2. Write fat cases in the [finished shape](#case-layout) for the behaviors.
3. Mutation-test the corpus, then run the old suite only on mutants the corpus missed. Sample enough to estimate the old-only rate, at least a thousand mutants; a hundred decides nothing.
   - First, both suites pass on the unmutated tree through the exact harness the proof uses. A harness that fails its baseline classifies every mutant as killed.
   - Pilot fifty mutants. An old-only rate above a few percent is a harness bug until shown otherwise.
   - Project the wall time from the pilot. Over an hour, change the method: cheaper build, compiled-once mutants, fewer old-suite runs. Never wait it out.
4. Every mutant only the old suite kills extends a case, or its code is deleted as dead.
5. Delete the old suite, its fixtures, and every script that produced them.
6. Turn on the ban.
