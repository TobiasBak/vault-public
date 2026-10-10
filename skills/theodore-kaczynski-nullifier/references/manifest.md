# Manifest

Ordered by measured cost. Each: the smell that reveals it, then the fix.

## 1. Ask the whole question in one call

Smell: chains of `rg`, `tail`, `git log`, each its own turn.

- CLI commands match the questions agents ask: "is this head mergeable", "why did this case fail", "what changed since the last green verdict".
- One call returns verdict, failing cases, first divergence, and repro command.
- Every probe sequence that repeats across sessions is a missing command.
- Independent reads go in one call.
- `<cli> map [area]` answers "where is this behavior" from case records. Never a hand-written map.

## 2. Wait on exit, never on a clock

Smell: `sleep 540; tail log`.

- `<cli> wait <job>` blocks until the job exits and returns its verdict. A job that dies at 35s answers at 35s.

## 3. Cache verdicts

Smell: rerunning a suite already passed on the same tree.

- Key: build inputs the case exercises (sources, lockfile, toolchain, flags), case files, harness version, fake-environment version. Inputs, not output bytes.
- The harness is the CLI entrypoint plus everything the case runner imports, derived from the imports, never listed by hand. The cache key, the watcher, and the `Behavior-Change:` guard read the same set.
- Value: verdict, actual-output hash, duration, producer.
- Content-addressed, outside every worktree and build directory, shared by all agents. Nothing a cleanup can delete.
- Nondeterminism is a bug in the case or the system.
- A new head whose diff touches none of a job's inputs reuses its verdict.

## 4. Have the answer before the question

Smell: every edit followed by build, test, read.

- One watcher per worktree. On change: debounce, build, run affected cases, store the verdict for the tree hash.
- `<cli> status` returns the verdict for the current tree hash, blocks while a run is in progress, never returns another tree's verdict.
- Starts on the first feedback command (`status`, `test`, `build`); read-only commands such as `doctor` never start it. Exits with the worktree or when idle. Low priority; takes a slot (§11).
- Agents never call the build tool directly.

## 5. Never pay for a cold start twice

Smell: the same build, boot, or setup repeated across worktrees, lanes, or runs.

- Snapshot and resume, a warm pool, or a shared content-keyed cache.
- New worktrees start from an existing build cache.
- One long-lived environment per resource, not one per run.

## 6. Caches explain their misses

Smell: "rebuilt again, no idea why."

- Store the input identity next to the key. On a miss, print field-level differences against the nearest key.
- Compare contexts without building before retrying an expensive build.
- Execution-only state stays out of the key.

## 7. One input set drives scope and key

Smell: a docs change triggers the full matrix.

- Each job declares its inputs once. Selection and cache key both derive from it.
- A path no job claims is an error.

## 8. Narrowest check first, full corpus once

Smell: full CI after every edit.

- In the loop: static checks and affected cases. Full corpus once, on the final head, through the verdict cache. The CLI picks the scope.

## 9. Budgets are visible

Smell: a step quietly tripled.

- Every tier has a budget next to its definition. Overruns print `budget 60s, took 158s`.
- Defaults: static checks ≤2s, affected cases ≤10s, full local corpus ≤60s, platform runs asynchronous.

## 10. Failures only

Smell: passing output in context.

- Passing cases print nothing. A failure prints case, first divergence, minimal diff, artifact paths, repro command. Logs go to artifacts.

## 11. One heavy job per resource

Smell: concurrent builds or guest runs slowing each other.

- A slot per heavy resource (CPU, guest machine, accelerator), taken by the CLI. The watcher takes one too.

## 12. Secondary platforms gate promotion, not the loop

Smell: a secondary-platform run on every PR.

- Merge on primary-platform evidence. Secondary platforms qualify release promotion.
- Build on the primary, ship artifacts to the secondary. Never build on the secondary.
- Platform-specific code sits behind one thin seam.

## 13. Bounded review loops

Smell: review rounds outlast implementation.

- A readiness bar and a round limit. Merge authority goes with the bar.
