# Omarchy Windows VM

Agents may use Tobias's Omarchy Windows VM for staging checks (Tobias, 2026-10-11). Its RAM counts against host admission. Use `win-vm`, not Omarchy's RDP-coupled launcher; stop only the VM instance your work owns.

[Dotfiles](../projects.md#dotfiles) owns installation, guest bootstrap, baseline configuration and the lifecycle helper. Start with its `AGENTS.md` and `agents/windows-vm/README.md`, then the installed command's `--help`. Do not recreate setup recipes or baseline identities here. System changes follow [Omarchy's privilege rules](omarchy-agent-operations.md#packages-and-privilege), never Docker-based installation of host files.

recheck-after: 2027-01-24

## Driving it: `win-vm`

The live command follows `~/.dotfiles/agents/windows-vm/win-vm`. It reaches the guest over SSH and runs GUI work inside the configured user's desktop session.

```bash
win-vm up                                    # start if needed; wait for SSH and the desktop
win-vm put ./app.exe 'C:/Users/tb/AppData/Local/myapp/app.exe'
win-vm gui 'C:\Users\tb\AppData\Local\myapp\app.exe'
win-vm gui --timeout 3600 --wait 'C:\...\runner.exe' --flag
win-vm uia inspect -a <pid> --depth 8 --json > state.uia.json
win-vm screenshot --app <pid> state.png
win-vm exec 'Get-Process myapp'
win-vm get 'C:/Users/tb/AppData/Local/myapp/log.txt' ./log.txt
win-vm down                                   # stop only an instance started by win-vm
```

- `exec` has no desktop. Anything visual goes through `gui`, `uia` and `screenshot`, which run in the interactive session.
- `gui --wait` waits for process exit and returns its exit code. NTSTATUS codes outside 0–255 map to shell exit 255; the JSON retains the exact code. Its timeout bounds execution and kills the owned process tree on expiry.
- `gui` without `--wait` intentionally leaves the app running. The caller owns its later cleanup.
- `uia` passes arguments to `winapp ui`. For selectors and state capture, see [Windows GUI automation](windows-gui-automation.md).
- `status` reports container state, SSH reachability, the desktop session, lifecycle ownership, persistent/ephemeral mode, lease holder and pinned baseline.
- `up` leaves an already-running VM unowned. Plain `down` checks the recorded container start identity. Never use `down --force` unless you know the VM is free; a shared harness's ownership marker is not proof that another agent has finished.
- `up` restores a disconnected session to the console, but never takes over an active RDP session. Omarchy's ordinary VM launcher opens RDP and stops the VM when its window closes, so it is unsuitable for agent-owned jobs.
- The guest has no GPU and uses WARP software rendering. Visual correctness is meaningful; smoothness and memory are not representative of a physical Windows machine.

## Disposable runs

Use a disposable baseline clone for work that must not persist, such as installs, users, hosts-file edits, trusted CAs or SYSTEM tasks. `win-vm up` and `win-vm run --ephemeral` own host admission, including the exclusive `win-vm` resource and guest-memory check. Call them directly, without an outer host lease; choose `--class gate` for qualification, `interactive` for ordinary work or `efficiency` for background research.

```bash
win-vm run --class gate --ephemeral -- ./lane.sh
```

- The clone starts from the pinned, stopped baseline. Persistent storage and the host shared folder are not mounted into it; guest writes are discarded at teardown.
- `run` refuses if the persistent VM is already running. It never stops someone else's session to make room.
- The run holds `win-vm`'s lifecycle lease throughout execution. Child commands inherit `WIN_VM_LEASE` and target that clone; they cannot start, stop or nest runs, or fall through to the persistent VM if the clone disappears.
- A guardian tears down after process exit or signals. Cleanup failures remain failures, with recovery instructions. Do not boot or reuse a stale clone.
- Re-pin the baseline only deliberately after checking the guest is stopped and free. Read its current identity from `win-vm status`, not a vault receipt.

## Credentials and files

Credentials live in `~/.keys/windows-vm.env`; the dedicated SSH key and host-key file are `~/.keys/windows-vm-agent` and `~/.keys/windows-vm-known_hosts`. Never copy their contents into evidence, commands, briefs or tracked files.

Use `win-vm put` and `get` for agent transfers. The host's `~/Windows` Samba share can show stale listings because host-side writes do not break Windows directory leases. Closing the share to refresh it drops open handles; coordinate first.

For Tobias's manual use, RDP drive redirection exposes a host folder under This PC. Use `sdl-freerdp3` and pass credentials on stdin, never in argv. noVNC has no clipboard. Installation and re-bootstrap procedures belong to dotfiles.

## Screenshots and cleanup

Capture the app with `win-vm screenshot --app <pid>`. Whole-guest screenshots are allowed; host-desktop screenshots require Tobias's explicit approval. Stop owned apps and release the VM when done, without stopping another user's or agent's session.
