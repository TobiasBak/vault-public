# Manifest

Common slow patterns, ordered by measured cost: the symptom, then the fix.

## 1. Ask the whole question in one call

Symptom: chains of `rg`, `tail`, `git log`, each its own turn.

- Commands match the questions agents ask: "can this head merge", "why did this case fail", "what changed since the last green verdict". One call returns verdict, failing cases, first mismatch, and rerun command.
- A probe sequence that repeats across sessions is a missing command. Independent reads go in one call.
- `<cli> map [area]` answers "where is this behavior" from case records, never a hand-written map.

## 2. Wait on exit, never on a clock

Symptom: `sleep 540; tail log`. Fix: `<cli> wait <job>` returns the verdict when the job exits; a job that dies at 35s answers at 35s.

## 3. Cache verdicts

Symptom: rerunning a suite that already passed on the same tree.

- Key: the build inputs the case uses (sources, lockfile, toolchain, flags), case files, harness version, fake-environment version. Inputs, not output bytes.
- The harness is the CLI entrypoint plus everything the case runner imports, derived from the imports, never listed by hand. Cache key, watcher, and `Behavior-Change:` guard read this same set.
- Value: verdict, actual-output hash, duration, producer.
- Stored by content hash outside every worktree and build directory, shared by all agents, beyond any cleanup.
- Nondeterminism is a bug in the case or the system.
- A new head whose diff touches none of a job's inputs reuses its verdict.

## 4. Have the answer before the question

Symptom: every edit followed by build, test, read.

- One watcher per worktree. On change: wait for edits to settle, build, run affected cases, store the verdict for the tree hash.
- `<cli> status` returns the current tree's verdict, blocks while a run is in progress, never returns another tree's.
- The watcher starts on the first feedback command (`status`, `test`, `build`), never on read-only ones like `doctor`; exits with the worktree or when idle; runs under host admission (§11), skipping when busy.
- Agents never call the build tool directly.

## 5. Never pay for a cold start twice

Symptom: the same build, boot, or setup repeated across worktrees, parallel jobs, or runs. Fix: snapshot and resume, a warm pool, or a shared content-keyed cache. New worktrees start from an existing build cache. One long-lived environment per resource, not per run.

## 6. Caches explain their misses

Symptom: "rebuilt again, no idea why." Fix: store the input details beside the key and on a miss print field-by-field differences against the nearest key. Compare inputs without building before retrying an expensive build. State that only affects execution stays out of the key.

## 7. One input set drives selection and cache key

Symptom: a docs change triggers the full matrix. Fix: each job declares its inputs once; test selection and cache key both come from it. A path no job claims is an error.

## 8. Selected tests for main, full corpus on promotion

Symptom: full CI after every edit. Fix: the [gate policy](enforcement.md#checks).

## 9. Budgets are visible

Symptom: a step quietly got three times slower.

- Every tier has a budget next to its definition, and overruns print `budget 60s, took 158s`.
- Defaults: static checks ≤2s, affected cases ≤10s, full local corpus ≤60s, platform runs in the background.

## 10. Failures only

Symptom: passing output filling context. Fix: the [failure output](black-box-tests.md#failure-output) and [CLI output](control-cli.md#output) contracts.

## 11. Host-wide heavy-work admission

Symptom: concurrent builds or VM runs slowing each other. Fix: integrate the CLI with [heavy-lease](control-cli.md#host-admission), including exclusive VM lanes and watcher busy skips. Never add a competing repo-local scheduler.

## 12. Secondary platforms gate promotion, not the loop

Symptom: a secondary-platform run (e.g. the Windows VM) on every PR.

- Merge on primary-platform evidence; secondary platforms qualify the promotion.
- Build on the primary and ship artifacts to the secondary. Never build on the secondary.
- Platform-specific code sits behind one thin layer.

## 13. Review only protected surfaces

Symptom: routine changes wait on review, or fixes restart independent review rounds.

Follow the [landing gate](enforcement.md#checks) and [review policy](../../../agents/code-review.md): one independent review only for repository-declared protected surfaces. Set the blocking bar before review; validate blocking fixes without another independent round. Non-blocking findings become follow-ups. Landing authority stays with the repo's designated owner.
