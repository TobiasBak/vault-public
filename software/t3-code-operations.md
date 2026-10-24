# T3 Code operations

Keep T3 service restarts out of live work, update T3 only by hand with the gah patch reapplied, and create secrets and webhook schedules in their owning thread. [Delegation](../agents/subagent-delegation.md#t3-code-feedback) owns agent coordination and completion semantics.

## Threads and workspaces

- `t3_thread_list` with `projectId` reads other projects' threads, including subagents (verified 2026-10-11, nightly `0.0.46-nightly.20261010.2922`).
- `t3_thread_send` works across projects. Use `mode: "steer"` for a running team; `auto` may queue instead. Use `auto` to start an idle thread. A queued report can wake an idle recipient; "no reply needed" still spends a turn (observed 2026-10-11/13).
- `t3_thread_launch` prepares and binds the requested workspace before the team starts. Do not follow it with `t3_worktree_handoff`; that moves the calling thread. On 2026-10-17, a handoff terminated a run and its continuation remained queued for 20 minutes.
- T3 auto-settles on PR merge or after `sidebarAutoSettleAfterDays` (default 3) of inactivity. gah threads sit on `main` with no branch, worktree or PR, so only the inactivity timer applies; settle them explicitly. The MCP preferences tool can't set the timer (2026-10-20).

## Secrets, webhooks and Connect

Observed 2026-10-13, nightly `0.0.46-nightly.20261013.3042`:

- `request_secret` cards appear only in the requesting thread; Pi's call timed out. A saved `secretRef` is single-use and usable only in the thread that saved it. Both `schedule_task` and `update_scheduled_task` rejected cross-thread references.
- For the Sol-owned webhook workaround, the lead created the schedule disabled, then attached `signature.secret` from a private file at call time, never echoed. Never put the secret in a brief, chat, tracked file or report.
- A schedule's `webhookUrl` needs T3 Connect. On Tobias's headless `t3code.service`, there was no app toggle: run `t3 connect link` under a pty (`script -qfc`), accept the relay-client install with `y`, have Tobias open the printed URL on this PC, then restart safely. Verify with `t3 connect status` that the environment link is provisioned.

## Updating T3

T3 never updates automatically; Tobias turned the 05:00 timer off on 2026-10-21. Updates run only when he asks. The installed service binary is a local build with git-at-home's `t3/` patches: the gah launch handoff and the 30-minute delegate notice. An official update replaces it, and then every `delegate_task` child in a gah repo is refused at its first turn. On 2026-10-21 the 05:00 update did this, and review delegations hung for hours before the gah-pi proxy learned to exit with Pi.

1. Run the restart check below. Then start the update through dotfiles' `t3code-update.service`. Note the new `activeVersion` in `~/.t3/runtime/service-state.json`.
2. Clone upstream `pingdotgg/t3code` at tag `v<version>` under `~/.cache/agent-tmp/`. Apply git-at-home's `t3/` patches (`gah-launch.patch`, `delegate-notice.patch`; its `t3/README.md` owns the order and tests). If one fails, port it and land the new patch with `gah merge`. Either way, run the focused tests: `vp test run` on `gahLaunchContext.test.ts` and the Pi adapter test (107 tests at 3438).
3. Stamp `<version>` into the `version` field of `apps/{server,desktop,web}` and `packages/{contracts,provider-core}` `package.json`. Then run `pnpm install --frozen-lockfile`.
4. Build directly with `node apps/server/scripts/cli.ts build-exe`, using a minimal environment: `PATH`, `HOME`, and the three public keys in `~/.local/state/t3-gah/build-inputs.json` (relay URL, Clerk publishable key, CLI OAuth client ID; never copy them into tracked files). Also set `T3CODE_TELEMETRY_CHANNEL=dev`, `T3CODE_TELEMETRY_ENABLED=false`, `T3CODE_OTEL_SDK_DISABLED=true`, and empty `T3CODE_RELAY_CLIENT_OTLP_TRACES_{URL,DATASET,TOKEN}`. The result is `apps/server/dist-exe/t3`.
5. Put the built `t3` beside reflink copies of the installed version's `client/`, `node_modules/` and `resource-monitor/`. The binary fails with `Cannot find module` without them. Compare `--version`, `--help`, `connect --help` and `connect status --json` with the installed binary in a fresh `HOME` and `T3CODE_HOME`; outputs must match byte for byte.
6. Swap the binary at `~/.t3/runtime/versions/<version>/t3` with the service stopped. Run stop, swap and start as one script in its own user unit, so the restart cannot kill the installer: `env -u GAH_WORKSPACE -u GAH_ROOT systemd-run --user --slice=app.slice --collect -- <script>`, without `--wait`, logging to a file you check after T3 resumes your thread. Confirm the running exe's checksum once the service answers, not the instant `systemctl start` returns: on 2026-10-24 `/proc/<MainPID>/exe` was unreadable right after start and read fine moments later.
7. Verify from a gah workspace: delegate a trivial Pi child and check that `gah status` reports it as a subagent of the leader.

## Service restarts

A service restart interrupts running runs and kills their in-flight tool calls, such as VM lanes and builds. On 2026-10-13, one restart killed 11 runs representing 2.7 hours of agent time. Since nightly `0.1.1-nightly.20261020.3411`, T3 starts a new run for each interrupted thread within seconds of startup (2026-10-20: three leads resumed 5 s after the restart), so the cost is the lost in-flight work, not the lead.

Changing a provider instance's settings entry while the server runs closes that instance and its sessions without that continuation: the instance registry rebuilds changed entries live, and continuations are written only at shutdown (source, nightly 3411). Change a busy instance's config by stopping `t3code.service`, editing `~/.t3/userdata/settings.json`, and starting it again.

Moving a running thread to another instance with `t3_thread_configure` fails its active run instead of resuming it (2026-10-20, Pi to Pi); restart the thread with a message. Idle threads switch cleanly. The new instance starts a new provider session, so under gah the thread lands in a fresh workspace and must be pointed back at its old one.

Run `python3 .agents/skills/chief-of-staff/scripts/cos.py restart-check --self <your thread ID>` from the vault root and restart only on exit 0. Without `--self`, the check counts the calling thread and never passes outside CoS. Otherwise hold the restart and tell Tobias what it would kill. [Dotfiles](../projects.md#dotfiles) owns service operations.
