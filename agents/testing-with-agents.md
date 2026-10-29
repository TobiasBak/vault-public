# Testing with agents

Agents investigate ambiguous behavior through the running app, APIs, logs, state and source. Deterministic tests repeat stable invariants cheaply. Neither tool use nor generated tests prove coverage.

## Landing

Follow the [delivery policy](../tobias/preferences.md#delivery-and-releases): static-only pre-push, writer-chosen tests, then straight to main (`gah merge` in gah workspaces). Full suites and secondary platforms qualify promotions. [Independent review](code-review.md) is only for repository-declared protected surfaces.

## Loop

1. Give the agent a realistic running environment, representative data, tools, and a clear authority boundary.
2. Define the workflow and observable success criteria, not every click.
3. Let it explore, keep artifacts, and investigate anomalies through the narrowest relevant surface.
4. Require a concrete reproduction with evidence: screenshots, traces, requests, logs, or resulting state.
5. Fix the responsible invariant (when authorized) and rerun both the minimized repro and the original scenario.
6. Promote stable discoveries into the cheapest durable protection: a deterministic test, schema, validator, lint rule, monitor, or clearer error.

Check authoritative state, not success messages. Derive expectations independently. Unclear expectations, unreliable resets and inaccessible state produce false alarms.

## Verification tooling

[Verification latency](verification-latency.md) owns the end-to-end speed target and shared-compute research directions.

[Renderless verification](renderless-verification.md) records the model/native
proof split and points to its enforced boundary and migration rules.

Keep a control CLI for launch, reset, interaction, inspection and cleanup. Its feature map is generated from case records linking behaviors and entry points to observable results, never a handwritten map or README. Commands stay in executable owners; the project's verification skill keeps only task steps the CLI cannot perform. Use `create-verification-skill` and `maintain-verification-skill`. Blocked or incomplete runs never pass.

**Handoff check:** in real sessions, can agents reproduce, fix and verify a representative report with normal tools and no coaching? Read those sessions; don't stage fresh agents for it (Tobias, 2026-10-24). Friction identifies the owner:

- couldn't find the feature: feature map or naming
- couldn't set up or inspect: tools
- couldn't establish what happened: observable state and causal diagnostics
- couldn't recover from a relevant partial failure: explicit state and supported recovery
- needed repeated diagnostic coaching: skill
- made an architectural mistake: API or enforced boundary
- claimed unsupported success: checks

Confirm each fix in later real sessions.

## Bounded workload proof

Contain descendants in the kernel, and derive nested ownership from their actual cgroup rather than inherited environment. A detached child with `env: {}` can survive both process-group cleanup and owner-token discovery. Use group/tree discovery only as an explicitly weaker fallback; failed discovery must never prevent signalling the known group.

- Verify recursive `cgroup.events` population, not root `cgroup.procs`. A delegated root can have no direct processes while child groups remain live.
- Record the actual nested cgroup before launching a driver. A dead CLI PID is not enough to reclaim its lock; retain exclusion until the subtree is empty, including after cleanup errors.
- Read `memory.events.local` for the owning limit. Hierarchical events include independently enforced child OOMs and can falsely fail a successful enclosing test suite.
- Make cleanup verification part of the pass decision at both the execution and gate-result boundaries. Fail unverified cleanup locally. The only sound exception is an ephemeral CI runner VM, recorded and logged as the containment; execution failures still fail. The regression tests exercise the real gate consumer, not just the policy helper.

## Jobs that must survive an agent turn

- Run heavy jobs directly through repository entrypoints; there is no host admission ([shared resources](../skills/theodore-kaczynski-nullifier/references/control-cli.md#shared-resources)).
- Start daemons and independent triggers in their own user unit, `systemd-run --user --slice=app.slice --collect -- <command>`, so they outlive the caller's gah session scope; take any exclusive lock inside it.
- Verify the resulting service's cgroup and ancestor memory limits rather than copying old percentages. Follow it with `systemctl --user status <unit>` and `journalctl --user -u <unit>`.
- `setsid`, `nohup`, `&` and a systemd scope do not establish independence from T3 session cleanup. Wait for process exit or file events, never fixed sleeps or poll loops.

## Expected crashes on Omarchy

- For mutation testing, fuzzing and abort tests, set `LimitCORE=1` on the transient systemd unit to cover descendants, or set `RLIMIT_CORE` to 1 before exec.
- Omarchy's `omarchy-crash-watch` shows a "Process crashed" toast for every systemd-coredump journal entry with the coredump `MESSAGE_ID` (`fc2e22bc…`), sending Tobias investigating expected crashes. Verified with a probe binary on his PC, 2026-10-11.
- `RLIMIT_CORE=0` (`ulimit -c 0`, `LimitCORE=0`) still journals "terminated abnormally without generating a coredump" under that ID. With a pipe `core_pattern`, 1 makes the kernel skip the helper entirely, so there is no entry or toast. This is the [documented kernel special case](https://man7.org/linux/man-pages/man5/core.5.html).

## Tool-manager test doubles

- Never shadow a tool manager on `PATH` with a delegating wrapper. A fake `mise` left first on `PATH` while the real `mise install` runs can trigger auto-reshimming that repoints every global shim in `~/.local/share/mise/shims` at the fake, breaking `cargo` and `rustc` across projects.
- Inject test inputs another way, or make `HOME`, `XDG_*`, `MISE_DATA_DIR`, `MISE_CACHE_DIR`, `MISE_STATE_DIR` and `CARGO_HOME` all private. Fingerprint host-global tool directories, including mise shims and their link targets, before and after such experiments.
- Private directories alone don't protect the host. An empty private `CARGO_HOME` makes mise activate a nonexistent `bin`, so `cargo` falls through to a stale host shim. A diagnostic probe that left mise auto-install enabled reinstalled host Rust and raced a rustup self-update. Run such fixtures under bubblewrap and disable mise auto-install before the first mise command. A read-only bind of `/` is not isolation: host Unix sockets stay connectable and `--unshare-net` doesn't cover them, so a child that inherits `DBUS_SESSION_BUS_ADDRESS` can ask the user's systemd to start an unsandboxed process. Bind only the directories the fixture needs, give it its own `/run`, `/tmp` and `$HOME`, clear the environment to an allowlist, and unshare every namespace. Prove isolation with probes that must fail inside and succeed outside: writes to the cargo, rustup and mise homes, a connection to the host session bus, and reads of host `$HOME`. Seen in OrderReady's slow suite, 2026-10-29.
- mise's default activation keeps inherited `PATH` additions ahead of pinned tools, so a stale shim earlier on `PATH` wins. Setting `MISE_ACTIVATE_AGGRESSIVE=true` puts pinned tools first.
- Recover with `PATH=/usr/bin:/bin /usr/bin/mise reshim`, then relink leftover orphan shims to `/usr/bin/mise`.

## Git fixtures inside hooks

- Tools and tests that spawn Git for fixture repositories, worktrees or clones must remove every variable listed by `git rev-parse --local-env-vars` from the child environment, including children that launch Git indirectly.
- Hooks export `GIT_DIR` and other repository-local variables; changing the working directory does not override them, so a hook-run gate can modify the real repository instead of its fixtures. One such pre-push gate committed and pushed deletion of the codebase.
- Prove isolation with a black-box check that runs the real tool with `GIT_DIR` set to a disposable outer repository and verifies that repository's HEAD, index, configuration and worktree registrations stay unchanged. Verify the real commit/push entrypoints too.

## Where agent verification time goes

Measure from session logs, receipts and PR timelines before tuning test runtime. A 2026-10-02 to 04 history review found the biggest losses outside test execution:

- PRs sat ready overnight (10.2h) because owners lacked merge authority.
- A dead hosted workflow burned 19 × 30-minute Windows jobs.
- Native builds were discarded after every run, worktree and head move: 2.3h of compiling.
- Windows VM housekeeping (leftover guest state, a full disk, manual session setup) took 54 of a 98-minute qualification.
- Whole-tree cache keys invalidated every app on docs changes. Unclassified paths sent 10 of 14 PRs to the full matrix. Derive keys and scope from one per-app input set; weaker keys admit stale output. See [receipt binding](learning-from-feedback.md#evidence-gates-for-recurring-misses).
- Unbounded review/fix loops dominated the longest PRs; see [code review](code-review.md#reviewers).

A second ledger (2026-10-07 to 09, two long Opus-orchestrates-Sol runs, Claude and Pi session logs) found the model was already the bottleneck. Hours are summed across parallel children, so they measure cost, not wall clock:

| Run | Model | Tools | Turns | Avg turn |
|---|---:|---:|---:|---:|
| Service port to Rust, 363 children | 78.8h | 20.6h | 16,343 | 17s |
| Geometry engine, 122 children | 22.3h | 13.4h | 4,316 | 19s |

- Prompt cache hit 96%, so latency per turn is the model, not waste. At ~17s per turn, 30 tiny probes cost as much as a full test run. Turn count is the first lever: one command per question, batched reads, compact output.
- Medium effort was not faster than high per turn in the port (18.9s vs 17.2s).
- The parents waited blind: the port's parent spent 6.9h in `sleep 590` polling loops; the engine's slept 9 minutes on a gate that died at 35s. Wait on exit or notification, never on a timer.
- The one >10-minute test run was a Windows lane: 318s fresh-clone boot, 89s bundle upload, 244s nextest (188s of tests). Cold starts, not tests.
- The engine's gate (885 runs, avg 44s, worst 16 min) rebuilt a release per worktree and lost its caches to a reference key tied to the harness script hash and a deleted `target/`.

Measure with entry timestamps: in Pi, model time is the assistant entry's `timestamp` minus `message.timestamp` (request start), and tool time is the `toolResult` entry minus its calling assistant entry. In Claude Code logs, pair `tool_use` with `tool_result` by id.

The durable fixes were direct integration authority, removal of dead CI, content-keyed cross-run build reuse and self-provisioning platform environments. Current suite and review policy is in [Landing](#landing).

## Explain cache misses before rebuilding

Store the canonical input identity alongside its cache key and print field-level differences on a mismatch. Compare preparation and real build contexts without compiling before retrying an expensive build. Exclude execution-only state at the key owner rather than making one caller imitate another.

Windows preparation and CI once differed only because uv injected `UV_INTERNAL__PYTHONHOME` in the project venv. Excluding the private `UV_INTERNAL__` namespace, while retaining the build-setting allowlist, made fresh-clone, same-head and docs-only proofs reuse verified distributions without compilation. The release contract decides whether exact keyed bytes suffice.

## Pruning tests

Keep tests that catch broken contracts or meaningful regressions across internal rewrites. Judge each assertion, not the test's category: a UI assertion may protect accessibility, a provider fixture may protect a protocol, and a registration test may be a discovery contract. Delete tests with no independent requirement, tests that mirror structure, and checks duplicated by cheaper equivalents. Coverage and count are not goals. The `review-test-quality` skill does this review.

## Refactor equivalence

Compare base and candidate under the same tests. Record durable plans, HTTP exchanges and session writes; diff per test node and call index. List deliberate renames, removals and additions. Anything else is unexplained. Include normalized accessibility snapshots and screen diffs.

Normalisation pitfalls:

- Under xdist, pytest temp paths gain `popen-gwN/`. Strip it, or compare runs that used the same worker mode.
- Random IDs inside strings (`execution-<hex8>`, upload hash directories, UUIDs) need stable placeholders. Map UUIDs in order of appearance.
- Evidence ZIP byte counts change with path lengths. Compare the unpacked, normalised JSON, not the size.
- Renamed test nodes must be mapped, or their records look like additions and removals.

### CSS migration proof

Retain the original production bundle before edits. If initial capture missed a state, serve that bundle against the same disposable fixture state, capture it, then restore the candidate; don't mock the page into looking equivalent.

CSS Modules migrations need checks beyond screenshots: runtime class queries can stop matching, custom tables can lose shared alignment rules, and removing an ancestor changes specificity in dirty/focused states. Audit styles-object references too: permissive module typings can accept nonexistent exports.

Sort computed-style property names before hashing; stylesheet edits can reorder custom-property enumeration without changing values. Reuse the same disposable fixture state and freeze clock/motion: regenerated IDs and dates can change text geometry. Normalizing the app origin does not repair that; renewing fixtures requires a fresh base capture.

Explain tiny pixel differences with evidence, not a blanket threshold. Repeat the unchanged baseline to test rasterization noise; inspect computed styles and geometry at the differing element. Wait for actual drawing content, not merely a default-sized canvas. A lazy render can otherwise look like a large CSS regression.

Finish shared frontend builds before registering and driving a fixture that fingerprints their assets. A valid readiness record becomes stale when another launcher rebuilds those assets. Compare recorded and current hashes before blaming a missing fingerprint or an ignored archive path; then build and launch serially with a fresh doctor-qualified record, never patch the registry to pass.

Identical protobuf maps can decode in different orders across SDK processes. Trace selection semantics before declaring a regression. Select the same named item through real controls and retain the original differing pair; never add product sorting for screenshots.

## Team adoption

Measure confirmed and missed defects, false alarms, investigation and maintenance, not generated code or test counts. Start with one troublesome workflow alongside the existing process. Invest in representative cases, clear expectations, easy startup, isolation and inspectable results. Cheap models like [Jev](jev.md) may classify failures, never gate releases.
