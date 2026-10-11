# Omarchy Windows VM

Agents may use Tobias's Omarchy Windows VM for staging checks (Tobias, 2026-10-11). Stop it afterwards; its RAM counts against build admission.

## Facts

- Installed with `omarchy windows vm install`. That command prompts in a terminal (RAM, cores, disk, user), so open it for Tobias with `omarchy-launch-floating-terminal-with-presentation "omarchy windows vm install"`.
- It is the dockur/windows image in the Docker container `omarchy-windows`. RDP listens on `127.0.0.1:3389` and the noVNC web viewer on `127.0.0.1:8006`, both localhost-only.
- Credentials: `~/.keys/windows-vm.env` (`WINDOWS_VM_USERNAME`, `WINDOWS_VM_PASSWORD`). Agent SSH key: `~/.keys/windows-vm-agent`, with its pinned host key in `~/.keys/windows-vm-known_hosts`. Never copy them anywhere else.
- No GPU. Windows renders with WARP, its software rasterizer, so look and correctness are real but smoothness and memory are not representative.
- `tb` is in the `docker` group (sudoless Docker, 2026-10-11).
- Don't use `omarchy-windows-vm launch` for agent work. It always opens RDP and stops the VM when that window closes.

## Driving it: `win-vm`

`win-vm` (dotfiles `agents/windows-vm/`, linked into `~/.local/bin`) starts the VM headless, reaches the guest over SSH as `tb` (an administrator), and runs GUI work inside tb's desktop session.

```bash
win-vm up                                    # start if needed; wait for SSH and tb's desktop; prints JSON
win-vm put ./app.exe 'C:/Users/tb/AppData/Local/myapp/app.exe'
win-vm gui 'C:\Users\tb\AppData\Local\myapp\app.exe'      # prints {"pid": N}
win-vm gui --timeout 3600 --wait 'C:\...\runner.exe' --flag  # blocks; exits with the process's code
win-vm uia inspect -a <pid> --depth 8 --json > state.uia.json
win-vm screenshot --app <pid> state.png       # omit --app for the whole guest desktop
win-vm exec 'Get-Process myapp'               # one PowerShell script over SSH
win-vm get 'C:/Users/tb/AppData/Local/myapp/log.txt' ./log.txt
win-vm down                                   # stops the VM only if this up started it
win-vm run --ephemeral -- ./lane.sh           # disposable baseline clone; exits with lane.sh's code
```

- **Ownership.** When `up` starts the VM, it records the container's start time in `~/.cache/win-vm/started-by-win-vm`. Plain `down` stops only that instance, so a VM someone else started (Tobias, another agent) stays up. `down --force` stops it unconditionally; use it only when you know the VM is free. Concurrent `up`s are serialized; if `up` finds the VM already running or can't prove it started it, it leaves the VM unowned.
- **One polkit dialog per host boot.** Omarchy's bind mounts for the VM disk vanish at reboot, and only its privileged helper recreates them. The first `up` after a reboot asks Tobias to approve one polkit dialog; later `up`s in the same boot need nothing.
- `up` and `down` take Omarchy's own VM lock (`/run/lock/omarchy-windows-vm`), so they can't race an Omarchy install, removal or launch.
- **`gui --wait`** blocks until the started process exits, prints `{"pid": N, "exit_code": M}` and exits with M. Codes outside 0–255 (NTSTATUS crashes) exit 255; the JSON keeps the exact code. Waiting polls the scheduled task over short SSH calls, so no SSH session is held. `--timeout` (default 120 s) bounds the wait: past it, `win-vm` kills the process tree and fails. Each `gui`, `uia` or `screenshot` call costs about 15–20 s of fixed overhead.
- `exec` runs in the SSH session, which has no desktop. Anything visual goes through `gui`, `uia` and `screenshot`, which run as one-shot scheduled tasks in tb's interactive session.
- tb logs on automatically at boot. If tb's session is disconnected (after an RDP client closes), `win-vm` moves it to the console with a SYSTEM `tscon`, so the desktop stays unlocked. An active RDP session is used as is and never taken over.
- `uia` passes its arguments to `winapp ui` (WinApp CLI 0.7.1) verbatim. For selectors and state capture, see [windows-gui-automation](windows-gui-automation.md). WinApp telemetry is opted out machine-wide.
- `status` prints JSON: container state, IP, SSH reachability, tb's session, `started_by_win_vm`, `mode` (`persistent` or `ephemeral`), the `lease` holder, the pinned `baseline` and `residue`.

## Disposable runs: `run --ephemeral`

For work whose guest state must not persist (installs, users, hosts-file edits, trusted CAs, SYSTEM tasks), such as Orderready's nightly Windows lanes.

- **Baseline.** `win-vm baseline` pins reflinked, read-only copies of the stopped guest's files from `~/.windows` into `~/.local/state/win-vm/baseline/`. Its `baseline.json` records `captured_at` and each file's sha256. The current baseline was captured 2026-10-11 from the post-bootstrap disk; `data.img` sha256 `84685c2a5f8e…`. Re-pin only deliberately: every later run starts from it.
- **Each run** reflink-copies the baseline into `~/.local/state/win-vm/ephemeral/` and boots it through a compose override that replaces both `/storage` and `/shared`. The persistent disk and `~/Windows` are never mounted, so the persistent disk stays byte-identical. At the end the container and the copy are deleted, discarding every guest write. Runs need no polkit dialog, even after a reboot. Boot to ready takes about 20–30 s.
- **Lease.** The run holds an exclusive lease for its whole duration. Every other `win-vm` command fails fast and names the holder (pid, command, start time); nothing queues. The host command and its children get `WIN_VM_LEASE`, so their `win-vm` calls reach the clone. They can't start, stop or nest runs, and they refuse to act if the clone is gone rather than touch the persistent VM.
- **Persistent VM running.** The run refuses with exit 1 and `win-vm: persistent VM is running; refusing ephemeral run (holder: …)`. It never stops a VM that may be someone else's session.
- **Exit and kills.** `run` exits with the host command's code (128+N if signal N killed it). A guardian in its own systemd scope (`win-vm-ephemeral-*.scope`) tears down when the run exits for any reason, including `kill -9` or the caller's cgroup being killed. A host command orphaned by such a kill keeps running; its `win-vm` calls are refused. If both die (host reboot), the next `win-vm` command cleans up the residue first.
- SSH goes to the container IP on port 22: dockur forwards every port except 5900, 8006, 139 and 445 to the guest. Nothing is exposed beyond the host-only Docker bridge.

## Guest setup

Done once on 2026-10-11; repeat only for a reinstalled guest. `win-vm bootstrap` stages pinned, hash-checked installers in `~/.cache/win-vm/bootstrap` and opens RDP with that folder redirected. Tobias double-clicks `\\tsclient\winvm\bootstrap.bat` and accepts UAC. The script is idempotent and logs to `C:\ProgramData\win-vm\bootstrap.log` and to the host stage folder. It:

- installs OpenSSH Server (public-key only, the agent key in `administrators_authorized_keys`, firewall open on TCP 22 only);
- installs the VC++ x64 runtime and WinApp CLI (`C:\Program Files\winapp`, on the machine PATH);
- keeps tb's autologon without a logon-count limit, and disables sleep, the lock on resume and the screen saver;
- hands tb's session to the console, which closes the RDP window.

Afterwards, stop the VM (`win-vm down`) and pin the result with `win-vm baseline`.

Lessons from the first run:

- Windows Installer refuses to install from an RDP session or a `\\tsclient` path (exit 1645). Copy installers locally and run them as SYSTEM from a one-shot scheduled task.
- The OpenSSH MSI's stock `Subsystem sftp sftp-server.exe` is relative, and the MSI doesn't put its folder on PATH, so `scp` and `sftp` close right after authentication. Use the quoted absolute path to `sftp-server.exe`.
- `query session` exits 1 even when it succeeds.

## Getting files in

- Use `win-vm put`.
- Host `~/Windows` is bind-mounted to the container's `/shared`, which Samba shares as `\\host.lan\Data` (the desktop's **Shared** folder). Files added on the host often don't show up. Samba's directory leases (`smb3 directory leases = Auto`) let Windows keep its cached listing, and host-side writes through the bind mount don't break the lease. `docker exec omarchy-windows smbcontrol smbd close-share Data` forces a fresh listing, but it drops open handles, so coordinate first. The per-daemon folders under Samba's core-dump path are empty, not crashes.
- For Tobias, RDP with drive redirection puts a host folder under This PC. Pass the password on stdin, never with `/p:`, because argv is visible to every process:

  ```bash
  (set -a; . ~/.keys/windows-vm.env; printf '%s\n' "$WINDOWS_VM_PASSWORD" |
    setsid sdl-freerdp3 /v:127.0.0.1:3389 /u:"$WINDOWS_VM_USERNAME" /cert:ignore \
      /clipboard /dynamic-resolution /drive:<name>,<host-dir> /from-stdin:force &)
  ```

- Use `sdl-freerdp3`, not `xfreerdp3`. From a T3 agent shell, `xfreerdp3` can't open X display `:0`.
- noVNC has no clipboard. Use RDP when Tobias needs to paste.

## Etiquette

Ask before full-desktop host screenshots (`grim`); they capture Tobias's private apps. Guest screenshots through `win-vm screenshot` are fine. Stop the VM when you're done.
