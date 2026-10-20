# T3 Code operations

Keep T3 service restarts out of live work, and create secrets and webhook schedules in their owning thread. [Delegation](../agents/subagent-delegation.md#t3-code-feedback) owns agent coordination and completion semantics.

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

## Service restarts

A service restart interrupts running runs and kills their in-flight tool calls, such as VM lanes and builds. On 2026-10-13, one restart killed 11 runs representing 2.7 hours of agent time. Since nightly `0.1.1-nightly.20261020.3411`, T3 starts a new run for each interrupted thread within seconds of startup (2026-10-20: three leads resumed 5 s after the restart), so the cost is the lost in-flight work, not the lead.

Changing a provider instance's settings entry while the server runs closes that instance and its sessions without that continuation: the instance registry rebuilds changed entries live, and continuations are written only at shutdown (source, nightly 3411). Change a busy instance's config by stopping `t3code.service`, editing `~/.t3/userdata/settings.json`, and starting it again.

Run `python3 .agents/skills/chief-of-staff/scripts/cos.py restart-check` from the vault root and restart only on exit 0. Otherwise hold the restart and tell Tobias what it would kill. [Dotfiles](../projects.md#dotfiles) owns service operations.
