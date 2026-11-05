# T3 Code operations

When Tobias asks for a T3 update, that authorizes the service restart, including interruption of active runs. Prepare the gah-patched runtime first, then update without asking again; T3 resumes interrupted threads automatically. Create secrets and webhook schedules in their owning thread. [Delegation](../agents/subagent-delegation.md#t3-code-feedback) owns agent coordination and completion semantics.

recheck-after: 2026-11-30

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

1. Resolve the newest nightly before changing the running service. An update request is restart approval, not a request to wait for every other agent to finish. Do not ask Tobias to approve the same restart again.
2. Clone upstream `pingdotgg/t3code` at tag `v<version>` under `~/.cache/agent-tmp/`. Apply git-at-home's `t3/` patches; its `t3/README.md` owns their order and checks. If either fails, port it and land the regenerated patches with `gah merge`.
3. Stamp `<version>` into the `version` field of `apps/{server,desktop,web}` and `packages/{contracts,provider-core}` `package.json`; at 3824 `provider-core` has no `version` field, so skip it there. Then run `pnpm install --frozen-lockfile`.
4. Build directly with `node apps/server/scripts/cli.ts build-exe`, using a minimal environment: `PATH` (with the checkout's `node_modules/.bin` first, since the build spawns `vp`), `HOME`, and the three public keys in `~/.local/state/t3-gah/build-inputs.json` (relay URL, Clerk publishable key, CLI OAuth client ID; never copy them into tracked files). Also set `T3CODE_TELEMETRY_CHANNEL=dev`, `T3CODE_TELEMETRY_ENABLED=false`, `T3CODE_OTEL_SDK_DISABLED=true`, and empty `T3CODE_RELAY_CLIENT_OTLP_TRACES_{URL,DATASET,TOKEN}`. The result is `apps/server/dist-exe/t3`.
5. Verify the new nightly's official archive against its published SHA-256, then assemble the patched runtime from that complete archive tree, replacing only `t3`. Do not reuse an older release's sibling assets. Compare `--version`, `--help`, `connect --help` and `connect status --json` between the official and patched builds in separate fresh homes; require identical output and exit status.
6. Publish that complete runtime under `~/.t3/runtime/versions/<version>/`, with its `.install-complete` sentinel containing the version, before starting dotfiles' `t3code-update.service`. The [official installer](https://github.com/pingdotgg/t3code/blob/v0.1.6-nightly.20261030.3940/apps/server/src/cloud/pinnedRuntime.ts) reuses it after checking the executable's version, so the service never starts an unpatched build. Run this handoff in an independent user unit: `env -u GAH_WORKSPACE -u GAH_ROOT systemd-run --user --slice=app.slice --collect -- <script>`, without `--wait`, with a retained log. After T3 resumes the thread, verify `activeVersion` in `~/.t3/runtime/service-state.json` and the running executable's checksum. Do not add a second manual restart.
7. Verify from a gah workspace: delegate a trivial Pi child and check that `gah status` reports it as a subagent of the leader. Also delegate a trivial Codex child and check that every `codex app-server` process carries its own `GAH_WORKSPACE`. Upstream T3 runs all Codex threads in one shared app-server; the gah patch splits it per thread. On 2026-10-30, a build without that split ran every Codex thread under the first thread's workspace.

## Service restarts

A service restart interrupts running runs and kills their in-flight tool calls, such as VM lanes and builds. On 2026-10-13, one restart killed 11 runs representing 2.7 hours of agent time. Since nightly `0.1.1-nightly.20261020.3411`, T3 starts a new run for each interrupted thread within seconds of startup (2026-10-20: three leads resumed 5 s after the restart), so the cost is the lost in-flight work, not the lead.

Changing a provider instance's settings entry while the server runs closes that instance and its sessions without that continuation: the instance registry rebuilds changed entries live, and continuations are written only at shutdown (source, nightly 3411). Change a busy instance's config by stopping `t3code.service`, editing `~/.t3/userdata/settings.json`, and starting it again.

Moving a running thread to another instance with `t3_thread_configure` fails its active run instead of resuming it (2026-10-20, Pi to Pi); restart the thread with a message. Idle threads switch cleanly. The new instance starts a new provider session, so under gah the thread lands in a fresh workspace and must be pointed back at its old one.

For maintenance that Tobias has not requested, list running threads across projects (`t3_thread_list` with `allProjects` and status `running`) and hold the restart while any thread other than yours is running. For an explicitly requested update or restart, that list is advisory, not a gate. Tobias confirmed this on 2026-10-30: proceed and rely on T3's automatic continuation instead of asking again. [Dotfiles](../projects.md#dotfiles) owns service operations.
