# Black-box tests

A test is an input at the published interface and a specified output. Nothing else is a test. Few cases, each covering as much as it can.

## The box

- **The box is the repository's published interface:** CLI, HTTP API, file-in/file-out contract, or a library's public API. Nothing narrower. Declaring an internal module a "product" to test it is forbidden.
- **Input:** the request plus the environment's starting state: files, fake external services, clock, seeds.
- **Output:** the response plus effects observed in the environment: files written, messages in a fake mailbox, rows in a fake external system.
- Fakes replace external systems only. Never the repository's own code.

## Allowed case kinds

1. **Example:** input and expected output.
2. **Relation:** a stated relation between outputs of related inputs. Rotation preserves volume; importing twice is idempotent.
3. **Robustness:** generated input; no crash, no hang, within budget.
4. **Differential:** output matches an oracle system on the same input.

## Fat cases

- A case is a scenario, not an assertion. It covers every behavior one input can reach.
- Extend an existing case before adding one. A new case needs an input no existing case can absorb: a conflicting starting state, a different case kind, or a budget overrun.
- Each behavior and entry-point pair is covered by exactly one case.
- Every published entry point to a behavior is covered. Coverage through another entry point doesn't count.
- A write is proven by reading it back through the interface or the environment, never by the write's own response.
- The first divergence localizes failures. Small cases buy nothing.

## Forbidden

- Unit tests, tests of internal modules, private access, assertions on call sequences or internal data.
- Expected values produced by running the code under test.
- Assertions on diagnostic stage dumps.
- Splitting a scenario into cases that share a starting state.
- Mass-blessing.

## Case layout

```
corpus/<area>/<scenario>/
  input...      request and starting environment
  expected...   canonical output and effects
  case.toml     covers, oracle, tolerance, budget, tags
```

- `covers` lists the behavior and entry-point pairs the case protects. The map and the coverage check read it.
- The oracle is the spec section, the oracle system and version, or the hand derivation.

## Expected output

- From an independent source only: the system being replaced, a reference tool, a spec, or a recorded hand derivation.
- One canonicalizer owns normalization: sorted keys, scrubbed IDs and timestamps, declared float tolerance. Cases never normalize.
- Format changes go through one mechanical rewrite script over every expected file. Any diff the script doesn't explain is a behavior change.

## Runner

- Calls the real entrypoint in-process: same arguments, same `main`. A subprocess only when the process is the contract.
- One build, one warm environment, the whole selection.
- Parallel and hermetic: per-case temp dir, port, and fake state.
- Clock and randomness injected. No real sleeps. Seeds printed on failure.
- Runs the cases affected by the diff; the full corpus once on the final head.
- Reports every case over budget.
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

1. Mutation-test the old suite, then the corpus alone.
2. Every mutant only the old suite kills extends a case, or its code is deleted as dead.
3. Delete the old suite.
4. Turn on the ban.
