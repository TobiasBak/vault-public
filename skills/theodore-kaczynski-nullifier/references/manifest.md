# Manifest

Use this branch of the [autonomy loop](../SKILL.md#the-loop) when a real workflow has a measured feedback cost. Fix its owner without weakening correctness or recovery. The patterns below are not a priority ranking.

## Optimization loop

1. **Measure** from harness session logs. Separate model, navigation, build, test, platform, forwarding, conflict, landing, child, and user time. Include shared-tool waits.
2. **Pick one outcome:** workflow, users, frequency, current cost, and cause to remove. Fix the largest measured recurring cost at its owner, never with an instruction agents must remember.
3. **Check value:** a baseline and named cause justify one or two before-and-after trials under the same conditions. Speed-motivated migrations, watchers, enforcement systems, and standalone proof efforts need a trial showing value. Otherwise shelve them. A demonstrated autonomy gap or correctness, security, or data-loss bug can justify a scoped fix without a speed claim.
4. **Measure again.** Stop at the measured target or when a one-line edit reaches its verdict, rebuild included, faster than a model turn. Further optimization needs a new measured cost.

This work runs beside product work, never as its precondition.

## 1. Ask the whole question in one call

Symptom: chains of `rg`, `tail`, `git log`, each its own turn.

- Product commands answer product questions: "why did this case fail", "what changed since the last green verdict". One call returns verdict, failing cases, first mismatch, and rerun command. Workspace and landing questions go to gah, not a second implementation.
- A probe sequence that repeats across sessions is a missing command. Independent reads go in one call.
- `<cli> map [area]` answers "where is this behavior" from case records, never a hand-written map.

## 2. Wait on exit, never on a clock

Symptom: `sleep 540; tail log`. Fix: `<cli> wait <job>` returns the verdict when the job exits; a job that dies at 35s answers at 35s.

## 3. Cache verdicts

Symptom: rerunning a suite that already passed on the same tree.

- Key: the build inputs the case uses (sources, lockfile, toolchain, flags), case files, harness version, operated-dependency and fake-environment versions, and qualified execution environment. Inputs, not output bytes, current directory, or workspace ID.
- The harness is the CLI entrypoint plus everything the case runner imports, derived from the imports, never listed by hand. Cache key, watcher, and `Behavior-Change:` guard read this same set.
- Value: verdict, actual-output hash, duration, producer.
- Stored by content hash outside disposable workspaces and build directories, shared by agents, beyond workspace cleanup.
- Nondeterminism is a bug in the case or the system.
- After forwarding or integrating child work, compare the resulting inputs before reusing evidence. A new head whose diff touches none of a job's inputs reuses its verdict. Warm artifacts and a successful landing check are not case verdicts.

## 4. Have the answer before the question

Symptom: every edit followed by build, test, read.

- One watcher per workspace, identified by workspace identity and running in its [mount namespace](control-cli.md#runs). On change: wait for edits to settle, build, run affected cases, store the verdict for the tree hash.
- `<cli> status` returns the current tree's verdict, blocks while a run is in progress, never returns another tree's.
- The watcher starts on the first feedback command (`status`, `test`, `build`), never on read-only ones like `doctor`; exits with the workspace or when idle; skips and reports no new evidence when an exclusive resource it needs is held ([shared resources](control-cli.md#shared-resources)).
- Agents never call the build tool directly.

## 5. Never pay for a cold start twice

Symptom: the same build, boot, or setup repeated across workspaces, parallel jobs, or runs.

- Use gah's warm build-state forks; do not build a second workspace provisioner, main warmer, or artifact copier. The repository supplies its build command and incremental configuration.
- Diagnose remaining cold starts at their owner. Use existing snapshot/resume or shared caches for external environments when the measured workflow needs them.
- Share expensive immutable preparation, not mutable case state. Each case still owns its state.

## 6. Caches explain their misses

Symptom: "rebuilt again, no idea why." Fix: store the input details beside the key and on a miss print field-by-field differences against the nearest key. Compare inputs without building before retrying an expensive build. State that only affects execution stays out of the key.

## 7. One input set drives selection and cache key

Symptom: a docs change triggers the full matrix. Fix: each job declares its inputs once; test selection and cache key both come from it. A path no job claims is an error.

## 8. Keep qualification out of the edit loop

Symptom: full qualification after every edit. Select relevant cases for feedback; keep the [landing check static](enforcement.md#checks). Shared-tool and session policy own where full qualification runs, not a second policy in the repository CLI.

## 9. Budgets are visible

Symptom: a step quietly got three times slower.

- Every tier has a budget next to its definition, and overruns print `budget 60s, took 158s`.
- Defaults: static checks ≤2s, affected cases ≤10s, full local corpus ≤60s, platform runs in the background.

## 10. Failures only

Symptom: passing output filling context. Fix: the [failure output](black-box-tests.md#failure-output) and [CLI output](control-cli.md#output) contracts.

## 11. Host-wide heavy work

Symptom: concurrent builds or VM runs slowing each other. Fix: let the kernel share CPU and memory and lock only exclusive resources through their owner ([shared resources](control-cli.md#shared-resources)). Never add a repo-local scheduler.

## 12. Avoid repeated platform setup

Symptom: secondary-platform startup or compilation dominates feedback. Use the qualification boundary set by the active delivery policy. Reuse prepared environments and build compatible artifacts once where the platform contract permits it; do not prohibit a platform-native build needed for valid evidence.

Keep platform-specific code behind its owning boundary. Never substitute primary-platform success for a required secondary-platform result.

## 13. Coordination has an owner

Symptom: routine changes wait on invented approvals, or fixes restart unnecessary review rounds. Check the active delivery and review policy, measure the actual wait, and repair the owning integration. Do not add another review or approval system to the repository CLI.
