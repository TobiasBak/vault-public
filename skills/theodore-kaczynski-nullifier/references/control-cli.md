# Control CLI

One entrypoint owns building, checking, testing, waiting, and inspecting. Agents never call the compiler, test runner, platform tooling, or package manager directly. Cache, watcher, slots, budgets, and scope selection live here.

## Commands

Names may change; the set may not.

| Command | Does |
|---|---|
| `status` | Verdict for the current tree, from cache or watcher. Blocks while a run for this tree is in progress. |
| `wait <job>` | Blocks until the job's verdict exists, then returns it. |
| `why <case>` | First divergence, minimal diff, `.actual` path, stage-dump command, repro command. |
| `map [area]` | Behaviors, entry points, and covering cases, generated from case records. |
| `check` | Format, lint, types, enforcement rules. |
| `test [<case>...]` | Affected cases by default; `--full` for the final head. |
| `accept <case> --source "<truth>"` | Writes expected output and its oracle. The commit still needs `Behavior-Change:`. |
| `reduce <case>` | Shrinks a failing input to a minimal failing case. |
| `emit <stage> <input>` | Diagnostic stage dump. |
| `env up\|reset\|down` | Fakes, services, platform guests. |
| `doctor` | Read-only check that this is the intended build with its prerequisites. |
| `mutants` | Mutation run; surviving mutants as tasks. |
| `explain-miss <job>` | Field-level difference between this key and the nearest cached one. |

AGENTS.md lists the names. `--help` is the documentation.

## Output

- First line: `pass`, `fail`, or `blocked`, with tree hash and duration.
- Exit 0 pass, 1 fail, 2 blocked or incomplete. Blocked is never a pass; a skipped step is never verified.
- Silent on success. Logs go to artifacts.
- Every run prints its run ID and artifact directory. Evidence survives cleanup.
- Overruns print `budget 60s, took 158s`.
- `--json` returns the same result.

## Runs

- Each run has an ID and disposable state: temp dirs, ports, fake data, guests. Cleanup touches only what the run owns, never by process name.
- Heavy work takes a slot per resource (CPU, guest machine, accelerator) first. The watcher competes for the same slots.
- `env up` returns when `doctor` passes, not after a delay.
- Anything longer than a few minutes runs in the background and returns a job ID for `wait`.
- Verify what "dry-run" and "test" modes actually write or contact.
- Feedback builds use their own fast incremental profile. Whole-program optimization and single-unit codegen are for shipping and performance measurement only; in the edit loop they turn a one-line change into a full rebuild. The cache key includes the profile.
- Compilation units follow the module dependency graph. When an edit costs the same rebuild wherever it lands, the unit is a monolith: split it along the graph, keeping cycles whole. Lowering optimization is not the fix when the corpus is compute-bound; it moves the cost into the run.
- Mutants are compiled once, every one behind a runtime switch, and tested in a single pass per case. The case runs unmutated. At each mutation site it reaches, every live mutant there is evaluated; a mutant whose value equals the original stays live in the parent, and one whose value differs forks a child that runs to the verdict. A mutant no case reaches survives without a run. Reach prunes runs and is never reported as coverage.
- Forks need a single-threaded process at the fork point and a kill timeout scaled from the unmutated case time. Where a process cannot fork, flip one switch at a time and run only the cases that reach it. Rebuild only mutants a switch cannot express, in one warm checkout per job, and report their count. Default scope is files changed against main.

## Proof

Run every command once against the real repo: pass, forced failure, blocked prerequisite, cache hit, cleanup.

Every one of those states is reachable through the CLI's flags or the environment. A proof that needs scratch code reaching into the CLI's internals means a switch is missing; add the switch, not the probe.
