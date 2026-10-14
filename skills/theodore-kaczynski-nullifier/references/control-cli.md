# Control CLI

One entrypoint owns the recurring operations this repository actually needs. Agents never call the compiler, test runner, platform tooling, or package manager directly for operations the CLI owns. Adopted cache, watcher, slots, budgets, and scope selection live here.

## One entrypoint

Delete every script, Makefile or justfile target, `package.json` script, shell alias, and wrapper that duplicates a control-CLI command once the CLI covers it. Calling the CLI through a wrapper still duplicates its entrypoint.

The gate keeps an exact allowlist of runnable paths (interpreter-invoked scripts included) and task-runner targets: CLI implementation, published product entrypoints, and required tool integrations such as hooks calling `<cli> check`. No convenience wrappers.

## Commands

A command earns its place by answering a real repeated question, not by completing this table. Adopt only commands needed by the selected outcome; no future placeholders. Names may change. The table defines each command's contract when adopted. `env` exists only where cases need managed external state.

| Command | Does |
|---|---|
| `status` | Verdict for the current tree, from cache or watcher. Blocks while a run for this tree is in progress. |
| `wait <job>` | Blocks until the job's verdict exists, then returns it. |
| `why <case>` | First divergence, minimal diff, `.actual` path, the `emit` command for the failing request, repro command. |
| `map [area]` | Behaviors, entry points, and covering cases, generated from case records. |
| `check` | Format, lint, types, enforcement rules. Never runs cases. |
| `test [<case>...]` | Conservatively selected affected cases by default; `--full` for nightly promotion, or nightly on main without staging. See the [gate policy](enforcement.md#checks). |
| `accept <case> --source "<truth>"` | Writes expected output and its oracle. The commit still needs `Behavior-Change:`. |
| `reduce <case>` | Shrinks a failing input to a minimal failing case. |
| `emit <stage> <input>` | Diagnostic stage dump. |
| `env up\|reset\|down` | Fakes, services, platform guests. |
| `doctor` | Read-only check that this is the intended build with the prerequisites of the edit loop. Optional capabilities are reported, never blocking; the commands that need them block themselves. |
| `mutants` | Mutation run; surviving mutants as tasks. |
| `explain-miss <job>` | Field-level difference between this key and the nearest cached one. |

AGENTS.md lists the names. `--help` is the documentation.

## Output

- First line of every command, `--json` included: `pass`, `fail`, or `blocked`, with tree hash and duration.
- Exit 0 pass, 1 fail, 2 blocked or incomplete. Blocked is never a pass; a skipped step is never verified.
- No passing-step chatter: the first line, the run receipt, and the answer the command exists to give. Logs go to artifacts.
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

## Mutation technique

For an authorized mutation-testing owner, not a requirement for every shaping outcome:
- Compile mutants once behind runtime switches and test them in a single pass per case. The case runs unmutated. At each mutation site it reaches, every live mutant there is evaluated; a mutant whose value equals the original stays live in the parent, and one whose value differs forks a child that runs to the verdict. A mutant no case reaches survives without a run. Reach prunes runs and is never reported as coverage.
- Forks need a single-threaded process at the fork point and a kill timeout scaled from the unmutated case time. Where a process cannot fork, flip one switch at a time and run only the cases that reach it. Rebuild only mutants a switch cannot express, in one warm checkout per job, and report their count. Default scope is files changed against main.
- A mutant that fails to build is unviable: counted and reported, never a kill. An infrastructure failure blocks the run; it never kills a mutant.

## Proof

Prove the changed contract through the real public entrypoint: normal success, the targeted failure, applicable blocked prerequisites, and affected cache or cleanup behavior. Process changes prove their deadlines and owned cleanup. Reuse valid evidence for unchanged surfaces. Edit-to-verdict measurements apply to edit-loop changes; fresh-agent comparisons apply to navigation or diagnostic changes. Do not run unrelated proof campaigns solely because this skill lists them.

A disposable public-interface proof starts with a known-good positive in the same environment. A blocked baseline cannot establish a negative verdict. The brief carries the environment recipe and prerequisite trust setup, scoped to the disposable directory. Keep tool-specific commands in the project or host recipe.

Change authored input or environment state and call real interfaces. Never reach into private implementation or add permanent test-only switches to enable a probe. Do not modify shared refs, host configuration, or credentials to make a proof pass. Report prerequisite refusals as blocked, never as rule rejections.
