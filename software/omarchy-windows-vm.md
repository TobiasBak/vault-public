# Omarchy Windows VM

Agents may use Tobias's Omarchy Windows VM for staging checks (Tobias, 2026-10-11). Stop it afterwards; its RAM counts against build admission.

## Facts

- Installed with `omarchy windows vm install`. That command prompts in a terminal (RAM, cores, disk, user), so open it for Tobias with `omarchy-launch-floating-terminal-with-presentation "omarchy windows vm install"`.
- It is the dockur/windows image in the Docker container `omarchy-windows`. RDP listens on `127.0.0.1:3389` and the noVNC web viewer on `127.0.0.1:8006`, both localhost-only.
- Credentials: `~/.keys/windows-vm.env` (`WINDOWS_VM_USERNAME`, `WINDOWS_VM_PASSWORD`). Never copy them anywhere else.
- No GPU. Windows renders with WARP, its software rasterizer, so look and correctness are real but smoothness and memory are not representative.
- `tb` is not in the `docker` group, and every `docker` command needs `pkexec`, which means a polkit dialog for Tobias. Batch all container work into one script per prompt.

## Getting files in

- Host `~/Windows` is bind-mounted to the container's `/shared`. Samba shares that as `\\host.lan\Data`, which appears as the desktop's **Shared** folder.
- On 2026-10-11 the share listed empty in Windows, even though the container saw the files and Samba had written core dumps. It worked after a forced reconnect: `docker exec omarchy-windows smbcontrol smbd close-share Data`. The root cause is unconfirmed.
- More reliable: open RDP with drive redirection. The folder then appears under This PC.

  ```bash
  source ~/.keys/windows-vm.env
  setsid uwsm-app -- sdl-freerdp3 /u:"$WINDOWS_VM_USERNAME" /p:"$WINDOWS_VM_PASSWORD" \
    /v:127.0.0.1:3389 /cert:ignore /clipboard /drive:<name>,<host-dir> /dynamic-resolution &
  ```

- Use `sdl-freerdp3`, not `xfreerdp3`. From a T3 agent shell, `xfreerdp3` can't open X display `:0`.
- noVNC has no clipboard. Use RDP when Tobias needs to paste.
- Fallback: `python3 -m http.server --bind 172.18.0.1` (the Docker bridge). The VM's Edge can reach it, and it isn't exposed on the LAN.
- A launcher `.bat` that copies the app to `%LOCALAPPDATA%` and installs `vc_redist.x64.exe` when it's missing saves Tobias clicks. Rust MSVC builds need the VC++ runtime.

## Not yet set up

There is no scriptable agent channel such as OpenSSH or WinRM inside the guest. Until one exists, agents stage files and Tobias clicks.

## Etiquette

Ask before full-desktop screenshots (`grim`). They capture Tobias's private apps. Prefer the VM's own view.
