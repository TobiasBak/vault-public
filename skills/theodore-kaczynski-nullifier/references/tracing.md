# Verification tracing

Every feedback command (`check`, `test`, gate, watcher jobs, promotion runs) writes one trace per verdict, stored beside the verdict under its ID. When a [cached verdict is reused](manifest.md#3-cache-verdicts), keep the original trace's identity; never present cached work as a new run.

## Spans

- Trace phases, steps, and cases, plus build units where the build tool exposes them.
- Every span records its ID, parent, monotonic start and end, wall time, CPU user and system time, scheduler run delay (`schedstat` on Linux), exit status, cache hit or miss, and PID. Mark missing or not-applicable values as such, never as a measured zero.
- Waits are spans too: [slot](manifest.md#11-one-heavy-job-per-resource) and lock acquisition, build locks, queueing, and waiting on background watchers. Record the holder's PID and command when known.
- Add an explicit gap span for wall time no activity or wait span covers. A parent phase alone doesn't explain its untraced time.
- Record dependency edges across parallel work and waits, so the critical path follows what actually delayed the verdict, not just the longest span.

## Host context

- At trace start and end, record load, slot holders, and background jobs (ours and others).
- Track overlap with background jobs during the run, including ones that start and finish between those snapshots. Mark an overlapped measurement as contaminated in the trace itself.

## Format

- Write Chrome Trace Event JSON that Perfetto or `chrome://tracing` opens directly as a waterfall. Never build a custom viewer.
- Use monotonic timestamps on one shared timeline; keep parentage, dependencies, metrics, host context, and contamination in the trace.

## Agent query

`<cli> trace [verdict]` answers where the time went and what changed, in one call, defaulting to the latest verdict. It returns compact JSON under the [CLI output contract](control-cli.md#output) with:

- Total wall time.
- The critical path as ordered spans with self time. Self time excludes the union of child intervals; never double-count nested or parallel spans.
- Wait versus work, with gaps shown separately, not counted as work.
- Top spans by self time.
- Parallelism: total CPU user plus system time divided by wall time, without counting child CPU twice.
- Cache hit rate, with hit and miss counts.
- The contamination flag.
- A per-span comparison of the critical path against main's latest trace for the same command. Match spans by stable phase, step, case, or build-unit identity; list added, removed, and unmatched spans, and say explicitly when there is no baseline.

Finding the bottleneck must never require reading the raw trace.

## Baseline and enforcement

Promotion runs keep baseline traces. A critical-path slowdown beyond the [repo's budget](manifest.md#9-budgets-are-visible) opens or updates an issue from the [promotion PR](enforcement.md#checks). Don't add a second enforcement path.
