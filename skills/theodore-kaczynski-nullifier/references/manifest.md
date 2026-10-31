# Feedback speed

The goal is many agents working at once, each getting a trustworthy verdict faster than a model turn, and none sitting in a queue. Remove measured waits; never build machinery for a wait nobody measured.

## Optimization loop

1. **Measure** from real session logs. Separate model, navigation, build, test, forwarding, landing and wait time, including waits on other agents.
2. **Pick one cost:** the largest recurring one, its cause and its owner. Fix it at the owner, never with an instruction agents must remember.
3. **Trial before adopting.** A baseline and a named cause justify one or two before-and-after trials under the same conditions. A speed-motivated tool, cache, watcher, migration or enforcement system that has no trial showing it pays is shelved, and one already built is removed. A correctness, security or data-loss bug can justify a scoped fix without a speed claim.
4. **Measure again** and stop at the target. More work needs a new measured cost.

Never let this work block product work.

## Keep verification small

Verification code is product code with its own bugs, reviews and runtime. Use the build tool and test runner the language ships, and keep the repository's verification CLI thin glue over them.

- When the verification machinery's own tests cost more than the product's tests, or a slow suite exercises the pipeline with fake services rather than the product, the machinery is too big. Shrink it before adding to it.
- A capability earns its place by a measured saving on a real workflow, not by matching a feature list. The [CLI commands](control-cli.md#commands) are the whole set; add none speculatively.

## Never wait silently

Most lost hours are waits nobody saw.

- Wait on process exit or a file event, never a clock. A job that dies at 35 s answers at 35 s.
- No host-wide locks or queues, in tools, scripts or delegate briefs. Lock only a resource one user can hold at a time, such as a VM device, through its [owning tool](control-cli.md#shared-resources).
- A wait with no progress for more than a few minutes is a blocker. The waiter reports what it waits on and who holds it, instead of blocking for an hour on `flock -w`.
- Iterate on the one failing case and run the full selection once on final source.

## Bound memory, not concurrency

The kernel shares CPU well; memory overcommit turns into swap thrash that slows every agent. Run each heavy job, such as a compile or a suite, in its own memory-capped scope (`systemd-run --user --scope -p MemoryMax=…`) so an out-of-memory kill fails that job, visibly, instead of thrashing the host or killing the agent that started it. A job that needs that much memory is a cost to fix at its owner: generated-code size, monolithic compilation units, needless whole-program optimization.

## Cache verdicts only when measured

Rerunning a check on unchanged inputs is waste, but a cache adds key bugs, freshness bugs and review surface. Adopt one only after measuring how often identical inputs recur.

- Key: the git tree hash of the job's declared paths, the toolchain lock and the harness version. Not output bytes, directories or workspace IDs.
- Store the verdict outside disposable workspaces, so every agent shares it.
- Log every hit and miss. A cache whose hit rate and saved time aren't measured is not kept.
- Warm build artifacts and a clean landing check are not verdicts.

## Never pay for a cold start twice

Use gah's warm build-state forks; do not build a second workspace provisioner, warmer or artifact copier. Share expensive immutable preparation, never mutable case state.

## Keep qualification out of the edit loop

Run the affected cases for feedback and keep the [landing check static](enforcement.md#checks). Delivery policy owns where full qualification runs.

## Budgets are visible

Every tier has a budget beside its definition, and overruns print `budget 60s, took 158s`. Defaults: static checks ≤2 s, affected cases ≤10 s, full local corpus ≤60 s. A budget reports; it never fails a correct run ([runner](black-box-tests.md#runner)).

## Failures only

Passing output costs context. Use the [test failure output](black-box-tests.md#failure-output) and [CLI output](control-cli.md#output) contracts.
