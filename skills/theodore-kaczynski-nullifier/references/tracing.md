# Verification tracing

Every feedback command writes one trace per verdict, beside the verdict and keyed by its ID: `check`, `test`, `gate`, watcher jobs, and promotion runs. Preserve trace identity on [cached verdict reuse](manifest.md#3-cache-verdicts); never present cached producer work as a new execution.

## Spans

- Trace phases, steps, and cases; include build units where the build tool exposes them.
- Every span carries its ID, parent, monotonic start and end, wall duration, CPU user and system time, scheduler run delay (`schedstat` on Linux), exit status, cache hit or miss, and PID. Mark unavailable or inapplicable values explicitly, never as measured zero.
- Waits are spans: [slot admission](manifest.md#11-one-heavy-job-per-resource), lock admission, build locks, queueing, and waiting on background watchers. Record the holder's PID and command when known.
- Emit an explicit gap span for wall time no activity or wait span covers. A containing phase alone does not explain its uninstrumented time.
- Record dependency edges across parallel work and waits so the critical path follows what delayed the verdict, not merely the longest span.

## Host context

- Record load, slot owners, and foreign and own background jobs at trace start and end.
- Track overlap with those background jobs during the run, including jobs that start and finish between snapshots. Mark an overlapping measurement contaminated in the trace itself.

## Format

- Write Chrome Trace Event JSON that Perfetto or `chrome://tracing` opens directly as a waterfall. Never build a custom viewer.
- Use monotonic timestamps on a common timeline; retain parentage, dependencies, metrics, host context, and contamination in the trace.

## Agent query

`<cli> trace [verdict]` answers where the time goes and what changed in one call. Default to the latest verdict. Its answer is compact JSON through the [CLI output contract](control-cli.md#output), containing:

- Total wall time.
- The critical path as ordered spans with self time. Self time excludes the union of child intervals; never double-count nested or parallel spans.
- The wait-vs-work split, with gaps explicit rather than counted as work.
- Top self-time spans.
- Parallelism as total CPU user plus system time divided by wall time, without counting child CPU twice.
- Cache hit rate, with hit and miss counts.
- The contamination flag.
- A delta against main's latest trace for the same command, per critical-path span. Match stable phase, step, case, or build-unit identities; identify added, removed, and unmatched spans, and a missing baseline explicitly.

Reading the raw trace is never required to identify the bottleneck.

## Baseline and enforcement

Promotion runs retain baseline traces. A critical-path regression beyond the [repository's budget](manifest.md#9-budgets-are-visible) opens or updates an issue from the [promotion PR](enforcement.md#checks). Do not add a second enforcement path.
