---
name: disk-cleanup
description: Free disk space on Tobias's Omarchy workstation, where agent scratch, worktrees and tool caches fill the btrfs root. Use when disk space is low, a disk-full error appears, or Tobias asks to clean up, free space, or find what is eating the disk.
---

# Disk cleanup

Agents fill this disk, not Tobias. The big consumers are scratch they never delete, git worktrees they never remove, and content-keyed caches with no eviction. Free space in that order, deleting as you go; measure only enough to choose the next target.

## Measuring on this machine

- `/` and `/home` share one btrfs volume mounted with `compress=zstd:3`; free space is `df -h /`. `/home` has no snapper snapshots, so deletes free space immediately.
- `du` lies here: it reports uncompressed bytes and counts reflinked copies twice. A full `du ~` once reported 6.6 TB on a 1.9 TB disk and took longer than 10 minutes. Judge each deletion by the `df` delta.
- Compressible JSON shrinks about 20 times on disk. Deleting 700 GB of apparent parity JSON freed 35 GB. Uncompressible build output and binaries free close to their `du` size.
- `btrfs filesystem du -s <dir>` works without root and splits exclusive from shared bytes, still uncompressed. `compsize` needs root.
- Never walk all of `~` in one `du`. Size candidate directories in parallel with per-directory timeouts: `ls -d <dirs> | xargs -P 32 -I{} timeout 300 du -xs --block-size=1G {}`.

## What to delete, biggest first

Activity is file modification time. Skip anything written recently: other agents run concurrently and use these paths.

1. **Dead git worktrees.** Run `scripts/reap-worktrees.sh` and review it, then rerun it with `--apply`. A worktree counts as dead after 24 hours with no git-index change and no process inside it. It is archived to `refs/archive/worktrees/<name>` first; restore it with `git worktree add <path> refs/archive/worktrees/<name>`. The script skips locked worktrees and checkouts that tooling manages (`sg/gate/baselines`, `orderready/rmut-build`). Repositories had piled up 205 worktrees, which freed about 470 GB.
2. **`~/.cache/agent-tmp`**, every agent's `TMPDIR`: `scripts/sweep-idle.sh --keep '^claude-' ~/.cache/agent-tmp 720`, then `--apply`. Before deleting a directory with dirty files on a named branch, check whether it holds unpushed work.
3. **Leftovers in `~/.t3/worktrees/<project>/`:** directories without `.git` are remains of removed worktrees, so delete them. In worktrees idle at least 12 hours, delete `target/`.
4. **Content-keyed caches with no eviction**, which rebuild on a miss:
   - `~/code/stepkit-geometry/.local/sg/parity/issue-54/agreement-v1/cache/`: about 19 GB apparent per entry. Keep the 2 newest.
   - `~/.cache/stepkit-studio/{binaries,control,runs,gate-controls,hook-dispatchers}/`: delete entries idle for more than 48 hours.
5. **Nightly output:**
   - `~/.local/share/stepkit-studio/nightly/windows/`: keep the 3 newest runs.
6. **Package caches:** `docker system prune -af`, `uv cache prune`, `pnpm store prune`, `mise prune -y`.

## Leave alone

- Steam games, `~/.windows/data.img` and `~/.local/state/win-vm/` (sparse VM images that use far less than their size), and `~/.t3/userdata/statev2.sqlite` (live T3 state).
- Run evidence, such as `~/.local/share/orderready/evidence/`: it is what failures are diagnosed from, and Orderready forbids deleting it. Ask the owning repo for retention instead.
- `~/.local/share/orderready/cache/sccache` (self-limiting) and its toolchain caches (`mamba`, `xwin`, `occt`).
- The pacman cache and journal: small here, and they need root.

## Report

Report the free space before and after, what each class freed, what was kept and why, and the archive refs created. A cache that only grows is a bug in its owning repository. Name the missing eviction there rather than relying on repeated sweeps.

## Verification

`df -h /` shows the freed space, `reap-worktrees.sh` without `--apply` lists no `DEAD` worktree, and every reaped worktree that had local work has its `refs/archive/worktrees/<name>`.
