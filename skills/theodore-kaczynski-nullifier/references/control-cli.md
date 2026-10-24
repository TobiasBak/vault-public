# Product verification CLI

One entrypoint owns recurring product verification: checks, builds, cases, evidence, and diagnostics. Agents use it for operations it covers. Reuse shared tooling for workspace lifecycle, warm build-state forks, host admission, and landing; never wrap those commands just to put them behind this CLI.

## One entrypoint

Once the CLI covers a verification operation, delete scripts, task-runner targets, aliases, and wrappers duplicating it. The gate keeps an exact allowlist of runnable files and targets, including interpreted scripts: the CLI's code, published product entrypoints, and required integration hooks. Shared-tool configuration is not a competing entrypoint. The configured landing check calls `<cli> check` directly; do not add a repo-local merge command.

## Commands

A command earns its place by answering a real repeated question. Adopt only what the outcome needs; no placeholders. Names may change; the table is each command's contract once adopted. `AGENTS.md` lists the names; `--help` is the documentation.

| Command | Does |
|---|---|
| `status` | Current tree's verdict, from matching evidence or a workspace-local watcher. Blocks while a run for these inputs is in progress. |
| `wait <job>` | Blocks until the job's verdict exists, then returns it. |
| `why <case>` | The [failure output](black-box-tests.md#failure-output) plus the `emit` command for the failing request. |
| `map [area]` | Behaviors, entry points, and covering cases, generated from case records. |
| `check` | Format, lint, types, enforcement rules. Never runs cases. |
| `test [<case>...]` | Writer-invoked affected cases by default; `--full` for qualification when the active delivery policy requires it. |
| `accept <case> --source "<truth>"` | Records inspected output and its oracle after [contract judgment](black-box-tests.md#evidence-and-authority); never establishes truth by recording it. The commit still needs `Behavior-Change:`. |
| `reduce <case>` | Shrinks a failing input to a minimal failing case. |
| `emit <stage> <input>` | Diagnostic stage dump. |
| `env up\|reset\|down` | Fakes, services, platform VMs. Only where cases need managed external state. |
| `doctor` | Read-only check that this is the intended build with the edit loop's prerequisites. Missing optional capabilities are reported, never blocking; commands needing them block themselves. |
| `mutants` | Mutation run; surviving mutants listed as tasks. |
| `explain-miss <job>` | Field-by-field difference between this cache key and the nearest cached one. |
| `trace [verdict]` | What slowed verification and what changed ([tracing](tracing.md)). |

## Output

- First line of every command, `--json` included: `pass`, `fail`, or `blocked`, with tree hash and duration. `--json` returns the same result.
- Exit 0 pass, 1 fail, 2 blocked or incomplete. Blocked is never a pass; a skipped step was not verified.
- Nothing about passing steps: only the first line, the run receipt, and the answer. Logs go to artifacts.
- Every run prints its run ID and artifact directory; evidence survives cleanup.
- Overruns print `budget 60s, took 158s`.

## Runs

- Each run has an ID and its own disposable state (temp dirs, ports, fake data, VMs). Cleanup touches only what the run owns, never by process name.
- Watchers, compiler servers, and other source-reading services run in the workspace's mount namespace. gah presents different workspaces at the same path; a host-side daemon sees main there. Key live services by workspace identity, never canonical path alone. [Evidence keys](manifest.md#3-cache-verdicts) identify inputs, not workspaces.
- Heavy work runs directly under [shared resources](#shared-resources), never a repo-local scheduler.
- `env up` returns when `doctor` passes, not after a fixed delay. Anything over a few minutes runs in the background and returns a job ID for `wait`.
- Verify what "dry-run" and "test" modes actually write or contact.
- Feedback builds use a fast incremental profile; the cache key includes it. Whole-program optimization and single-unit codegen (e.g. `lto = "fat"`, `codegen-units = 1`) are for shipping and performance measurement only; in the edit loop they make a one-line change a full rebuild.
- Compilation units follow the module dependency graph. If an edit costs the same rebuild wherever it lands, the unit is a monolith: split it along the graph, keeping cycles together. Lowering optimization is no fix when the corpus is compute-bound; it moves the cost into the run.

## Shared resources

There is no host admission: the kernel shares CPU and memory, and repository entrypoints run commands directly. Never add a repo-local scheduler, pool or memory-headroom wait.

A resource only one user may hold at a time, such as a VM device, is locked by its owning tool. Foreground work waits for that owner; opportunistic watchers skip when it is busy and report no new evidence. Long-lived services and independent triggers run in their own systemd user unit (`systemd-run --user`), so they outlive the caller's session scope; take any exclusive lock inside that unit.

Missing required exclusive access is blocked, never a pass. Wait for process exit or file events, never fixed sleeps or poll loops.

## Mutation technique

Only for an authorized mutation-testing effort:
- Compile mutants once behind runtime switches and test them in one pass per case. The case runs unmutated; at each mutation site it reaches, every live mutant there is evaluated. One whose value equals the original stays in the parent; one that differs forks a child that runs to a verdict. A mutant no case reaches survives without a run. Reach only prunes runs, never counts as coverage.
- Forking needs a single-threaded process at the fork point and a kill timeout scaled from the unmutated case time. Where a process can't fork, flip one switch at a time and run only the cases reaching it. Rebuild only mutants a switch can't express, in one warm checkout per job, and report their count. Default scope: files changed against main.
- A mutant that fails to build is unviable: counted and reported, never a kill. An infrastructure failure blocks the run, never kills a mutant.

## Proof

Prove a changed contract through the real public entrypoint against [independently justified expectations](black-box-tests.md#evidence-and-authority): normal success, the targeted failure, relevant blocked prerequisites, and affected cache or cleanup behavior. Process changes also prove their deadlines and cleanup of what they own. Reuse valid evidence for unchanged parts, and don't run unrelated proofs just because this skill lists them.

A throwaway proof starts with a known-good pass in the same environment; a blocked baseline can't establish a failure. The task brief carries the environment setup and trust setup, scoped to the throwaway directory; tool-specific commands stay in the project or host setup.

Change authored input or environment state and call real interfaces. Never reach into private code or add permanent test-only switches for a probe. Never modify shared git refs, host configuration, or credentials to make a proof pass. Report a missing prerequisite as blocked, never as a rule rejection.
