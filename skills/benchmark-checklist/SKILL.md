---
name: benchmark-checklist
description: Vet a performance measurement before reporting or acting on it, covering limiter, tuning, physical limits, errors, repeatability, relevance, and whether the work happened. Use when you run a benchmark, compare implementations or configs, or report a speedup or regression you measured.
---

# Benchmark checklist

Answer each question with evidence from a run, not a guess about the code. For a quick ballpark the user asked for, one run is enough: still check questions 4 and 7 and say it is one run. A choice between options is never a ballpark.

## Before running

- Write the claim you expect to ship ("export is 30% faster at p50 on the 60k-row dataset"). The questions test that sentence.
- Read the measurement script: what it times, counts, and ignores.
- Check `uptime` and `nproc`. If the machine is busy and you can't stop the load, interleave the sides so both see the same noise, and say so.

## The questions

1. **Why not double?** Name the limiter. Profile in a run you don't report, since profilers slow the work. Use per-process CPU (`top`, `pidstat`), a runtime profiler (`py-spy`, `perf`, `node --cpu-prof`), I/O wait, and syscall counts (`strace -c`), then map the hot spot to source. Watch the load generator: if it saturates first, you measured it. If a change didn't move the number, the limiter explains why.
2. **Was it tuned?** Run every side the way production does: release builds, production flags and env, batching, pools, cache warmth, versions, and data. A limiter that is a setting (commit per row, debug build, missing index) means that side is untuned. Tune and remeasure before picking a winner. Narrowing the claim to "as shipped today" doesn't fix this when the user is choosing what to adopt.
3. **Did it break limits?** Do the arithmetic against disk and network bandwidth and core count. Removing a piece that takes 10% of the run can make it at most about 11% faster. A result past a limit measured a cache, a no-op, or a bug.
4. **Did it error?** Count failures and non-success responses, and check outputs are correct, not just present. Rejections are often fast; timeouts and retries are slow. If the script doesn't count errors, add the count.
5. **Does it reproduce?** At least 5 runs per side, alternating A, B, A, B so warmup, caches, and drift don't favor one side. Report median and range. A gap smaller than run-to-run variation is no measurable difference; for close calls use a rank-sum test or the harness's statistics.
6. **Does it matter?** Next to any micro result, measure the end-to-end path a user waits on at realistic size and concurrency, and report the micro result as a share of it.
7. **Did it happen?** Confirm the work ran inside the timed region: the request arrived, rows were written, bytes were read, the result was used. Unconsumed generators, unawaited promises, results the optimizer discards, and timeouts all produce numbers for work that never happened.

## Report

- Lead with the verdict: faster, slower, no measurable difference, or inconclusive.
- Give the number with unit, run count, range, and limiter: "p50 41 ms → 33 ms, median of 7 runs per side, range 32–35 ms after, bound by JSON parsing on one core."
- Call it inconclusive when you claim a difference but can't name the limiter, a side ran untuned, or you couldn't check questions 4 and 7. Name the gap.
- Keep run logs and limiter evidence in a linked artifact, not the PR body.

## Verification

Before shipping a performance change, rerun the reported comparison from a clean build of the exact commit and confirm the claim sentence, error count, and work count hold.
