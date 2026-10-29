# Omarchy agent operations

Use Omarchy's package and privilege paths, not raw Arch package tools or root-equivalent groups. Read the installed `omarchy` skill, including Privilege Escalation, before system changes. [Dotfiles](../projects.md#dotfiles) owns machine configuration.

recheck-after: 2027-01-24

## Packages and privilege

- System packages go through `omarchy pkg add`, never raw `pacman` or `yay`. Agents have no terminal for sudo: run `pkexec /usr/share/omarchy/bin/omarchy-pkg-add <pkgs>` in the background so Tobias can approve the desktop polkit dialog. Do not hand him a command to paste.
- AUR-only packages require Tobias's terminal: ask him to run `omarchy pkg aur add <pkgs>`, since `makepkg` refuses root.
- Root-equivalent groups such as `docker` are not an installation path for system files. The [Windows VM](omarchy-windows-vm.md) has its own narrowly scoped lifecycle helper.

## Replace a user-owned CLI without stranding running agents

On Linux, unlinking an executing binary can leave its `/proc/<pid>/exe` pathname marked `(deleted)`. The process can continue running while a later attempt to launch that pathname fails.

Stage the qualified new binary beside the live executable, then use `mv --exchange --no-copy -T "$staged" "$live"`. The exchange puts the old inode at the staging pathname instead of unlinking it. Keep that path until its running consumers no longer need it; do not overwrite the backup during another update. Same-directory staging avoids a cross-filesystem move, and `--no-copy` prevents a copy fallback.

Verified on 2026-10-29 with GNU coreutils 9.12 during a GAH update: an existing process retained its old executable inode and resolved it through the backup pathname, while new launches used the qualified replacement. Check those process/path invariants as well as the installed hash. See Linux's [atomic exchange semantics](https://man7.org/linux/man-pages/man2/rename.2.html) and [GNU mv options](https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html).

## Unprivileged safety checks

Observed on Tobias's PC, 2026-10-11: agents had no passwordless sudo, and `lsof` and `fuser` were absent. Brief checks that work as uid `tobias`: scan readable `/proc` links.

Some daemons owned by Tobias were non-dumpable and unreadable even to him: `systemd --user`, `sd-pam`, `ssh-agent`, `gnome-keyring`, and speech-dispatcher's `sd_*` modules. Treat these as expected access restrictions, not automatic proof that a deletion target is unused. Establish the target's ownership and activity through other evidence; unrelated unreadable processes still need a disposition.
