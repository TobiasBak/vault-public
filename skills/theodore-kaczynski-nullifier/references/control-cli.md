# Product verification CLI

One entrypoint owns recurring product verification: checks, builds, cases, evidence, and diagnostics. Agents use it for operations it covers. Reuse shared tooling for workspace lifecycle, warm build-state forks and landing; never wrap those commands just to put them behind this CLI.

## One entrypoint

Once the CLI covers a verification operation, delete scripts, task-runner targets, aliases, and wrappers duplicating it. The gate keeps an exact allowlist of runnable files and targets, including interpreted scripts: the CLI's code, published product entrypoints, and required integration hooks. Shared-tool configuration is not a competing entrypoint. The configured landing check calls `<cli> check` directly; do not add a repo-local merge command.

## Commands

These are the whole set. A command earns its place by answering a question agents repeat; add none speculatively. Names may change; the table is each command's contract once adopted. `AGENTS.md` lists the names; `--help` is the documentation.

| Command | Does |
|---|---|
| `check` | Format, lint, types, enforcement rules. Never runs cases. |
| `test [<case>...]` | Affected cases by default, any single case by name, `--full` when delivery policy requires it. |
| `status` | The current tree's verdict from matching evidence, or none. |
| `why <case>` | The [failure output](black-box-tests.md#failure-output) for the failing request. |
| `accept <case> --source "<truth>"` | Records inspected output and its oracle after [contract judgment](runtime-outcomes.md#evidence-and-authority); never establishes truth by recording it. The commit still needs `Behavior-Change:`. |
| `map [area]` | Behaviors, entry points, and covering cases, generated from case records. |

## Output

- First line of every command, `--json` included: `pass`, `fail`, or `blocked`, with tree hash and duration. `--json` returns the same result.
- Exit 0 pass, 1 fail, 2 blocked or incomplete. Blocked is never a pass; a skipped step was not verified.
- Nothing about passing steps: only the first line, the run receipt, and the answer. Logs go to artifacts.
- Every run prints its run ID and artifact directory; evidence survives cleanup.
- Overruns print `budget 60s, took 158s`.

## Runs

- Each run has an ID and its own disposable state (temp dirs, ports, fake data, VMs). Cleanup touches only what the run owns, never by process name.
- Source-reading services, such as compiler servers, run in the workspace's mount namespace: gah presents different workspaces at the same path, and a host-side daemon sees main there.
- Anything over a few minutes runs in the background and is waited on by process exit.
- Verify what "dry-run" and "test" modes actually write or contact.
- Feedback builds use a fast incremental profile. Whole-program optimization and single-unit codegen (e.g. `lto = "fat"`, `codegen-units = 1`) are for shipping and performance measurement only; in the edit loop they make a one-line change a full rebuild.
- Compilation units follow the module dependency graph. If an edit costs the same rebuild wherever it lands, the unit is a monolith: split it along the graph, keeping cycles together.

## Shared resources

There is no host admission: the kernel shares CPU, repository entrypoints run commands directly, and nothing queues behind a host-wide lock. Never add a repo-local scheduler, pool, memory-headroom wait or host lock, including in a delegate brief.

- Bound memory per job instead: each heavy job runs in its own memory-capped scope ([bound memory](manifest.md#bound-memory-not-concurrency)).
- A resource only one user may hold at a time, such as a VM device, is locked by its owning tool, which reports the holder. Long-lived services run in their own systemd user unit (`systemd-run --user`) and take any exclusive lock inside it.
- Missing required exclusive access is blocked, never a pass. A wait without progress for more than a few minutes is reported as a blocker naming the holder, never a silent `flock -w`.

## Proof

Prove a changed contract through the real public entrypoint against [independently justified expectations](runtime-outcomes.md#evidence-and-authority): normal success, the targeted failure, relevant blocked prerequisites, and affected cache or cleanup behavior. Process changes also prove their deadlines and cleanup of what they own. Reuse valid evidence for unchanged parts, and don't run unrelated proofs just because this skill lists them.

A throwaway proof starts with a known-good pass in the same environment; a blocked baseline can't establish a failure. The task brief carries the environment setup and trust setup, scoped to the throwaway directory; tool-specific commands stay in the project or host setup.

Change authored input or environment state and call real interfaces. Never reach into private code or add permanent test-only switches for a probe. Never modify shared git refs, host configuration, or credentials to make a proof pass. Report a missing prerequisite as blocked, never as a rule rejection.
