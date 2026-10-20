# Omarchy agent operations

Use Omarchy's package and privilege paths, not raw Arch package tools or root-equivalent groups. Read the installed `omarchy` skill, including Privilege Escalation, before system changes. [Dotfiles](../projects.md#dotfiles) owns machine configuration.

## Packages and privilege

- System packages go through `omarchy pkg add`, never raw `pacman` or `yay`. Agents have no terminal for sudo: run `pkexec /usr/share/omarchy/bin/omarchy-pkg-add <pkgs>` in the background so Tobias can approve the desktop polkit dialog. Do not hand him a command to paste.
- AUR-only packages require Tobias's terminal: ask him to run `omarchy pkg aur add <pkgs>`, since `makepkg` refuses root.
- Root-equivalent groups such as `docker` are not an installation path for system files. The [Windows VM](omarchy-windows-vm.md) has its own narrowly scoped lifecycle helper.

## Unprivileged safety checks

Observed on Tobias's PC, 2026-10-11: agents had no passwordless sudo, and `lsof` and `fuser` were absent. Brief checks that work as uid `tobias`: scan readable `/proc` links.

Some daemons owned by Tobias were non-dumpable and unreadable even to him: `systemd --user`, `sd-pam`, `ssh-agent`, `gnome-keyring`, and speech-dispatcher's `sd_*` modules. Treat these as expected access restrictions, not automatic proof that a deletion target is unused. Establish the target's ownership and activity through other evidence; unrelated unreadable processes still need a disposition.
