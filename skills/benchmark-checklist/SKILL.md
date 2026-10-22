---
name: benchmark-checklist
description: Vet a performance measurement before reporting or acting on it, covering limiter, tuning, physical limits, errors, repeatability, relevance, and whether the work happened. Use when you run a benchmark, compare implementations or configs, or report a speedup or regression you measured.
---

# Benchmark checklist

Match the evidence to the decision. For exploratory screening, use the existing harness and 1–2 runs per side; check correctness and that the work happened (questions 4 and 7), inspect the output, and label the result provisional. Do not harden the harness or replicate every idea before it shows a useful signal.

For adoption decisions and confirmed performance claims, answer every question with run evidence, not guesses about the code. A user-requested ballpark may use one run if questions 4 and 7 pass and the report says it is one run.

## Before running

- Write the hypothesis for a scout, or the claim you expect to ship ("export is 30% faster at p50 on the 60k-row dataset"). The questions test that sentence.
- Read the measurement script: what it times, counts, and ignores.
- Check `uptime` and `nproc`. If the machine is busy and you can't stop the load, interleave the sides so both see the same noise, and say so.

## The questions

1. **Why not double?** Name the limiter. Profile in a run you don't report, since profilers slow the work. Use per-process CPU (`top`, `pidstat`), a runtime profiler (`py-spy`, `perf`, `node --cpu-prof`), I/O wait, and syscall counts (`strace -c`), then map the hot spot to source. Watch the load generator: if it saturates first, you measured it. If a change didn't move the number, the limiter explains why.
2. **Was it tuned?** Run every side the way production does: release builds, production flags and env, batching, pools, cache warmth, versions, and data. A limiter that is a setting (commit per row, debug build, missing index) means that side is untuned. Tune and remeasure before picking a winner. Narrowing the claim to "as shipped today" doesn't fix this when the user is choosing what to adopt.
3. **Did it break limits?** Do the arithmetic against disk and network bandwidth and core count. Removing a piece that takes 10% of the run can make it at most about 11% faster. A result past a limit measured a cache, a no-op, or a bug.
4. **Did it error?** Count failures and non-success responses, and check outputs are correct, not just present. Rejections are often fast; timeouts and retries are slow. For scouts, count errors from existing output; instrument confirmed runs if needed.
5. **Does it reproduce?** For a confirmed comparison, at least 5 runs per side, alternating A, B, A, B so warmup, caches, and drift don't favor one side. Report median and range. A gap smaller than run-to-run variation is no measurable difference; for close calls use a rank-sum test or the harness's statistics.
6. **Does it matter?** Next to any micro result, measure the end-to-end path a user waits on at realistic size and concurrency, and report the micro result as a share of it.
7. **Did it happen?** Confirm the work ran inside the timed region: the request arrived, rows were written, bytes were read, the result was used. Unconsumed generators, unawaited promises, results the optimizer discards, and timeouts all produce numbers for work that never happened.

## Report

- Lead with the verdict: faster, slower, no measurable difference, or inconclusive. For scouts, use promising, not promising, or inconclusive; a provisional large effect justifies confirmation, not adoption.
- Give the workload, timed process boundary, units, run count, spread, and known limiter or evidence gap: "p50 41 ms → 33 ms, median of 7 runs per side, range 32–35 ms after, bound by JSON parsing on one core."
- A confirmed comparison is inconclusive if the limiter is unknown or a side ran untuned. A scout may leave the limiter unconfirmed, but any run with unchecked correctness or work count (questions 4 and 7) is inconclusive. Name the gap.
- Keep run logs and limiter evidence in a linked artifact, not the PR body.

## Verification

Before shipping a performance change, rerun the reported comparison from a clean build of the exact commit and confirm the claim sentence, error count, and work count hold.
