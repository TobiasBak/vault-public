---
name: disk-cleanup
description: Free disk space on Tobias's Omarchy workstation without disrupting concurrent agents. Use when disk space is low, a disk-full error appears, or Tobias asks to clean up, free space, or find what is eating the disk. Covers gah ownership, stale compiler output, scratch and tool caches.
---

# Disk cleanup

Preserve current work before reclaiming space. Agents run concurrently, and old modification times do not prove that a path is unused. Prefer verified-unused compiler output to deleting whole workspaces or scratch trees.

## Measure selectively

- `/` and `/home` share a compressed btrfs volume. Record `df -B1 /` and `df -h /` before and after each cleanup class. Concurrent jobs can change the totals.
- `du` does not predict physical recovery: compression and shared extents matter. `btrfs filesystem du -s <dir>` separates shared from exclusive extents, but still does not account for compression.
- Never walk all of `~` with `du`. Size selected directories in parallel with per-directory timeouts. Stop once there is enough evidence to choose a useful target.

## Establish ownership and activity

1. Inspect registered T3 projects and current threads across projects, not just the calling project. Protect work belonging to paused or waiting threads too. Use the current owning checkout's instructions; `~/code/<repo>` may be an obsolete pre-gah copy.
2. **Gah owns its workspace lifecycle.** Check the installed `gah --help`, `gah gc --help` and `gah gc --dry-run`. Never manually remove its mains, workspaces, pins, seeds, archives or retired subvolumes, including their build directories. An existing `gah-gc.timer` may already handle collection.
3. A gc dry run is an inventory, not permission to collect everything it lists. Clean workspaces can qualify after a short idle period; dirty-workspace age is not a universal grace period. Use owner-approved, explicitly selected lifecycle operations if workspace removal is necessary. Leave pinned qualification state alone.
4. Check candidate paths against running processes immediately before deletion: working directories, executables, open files, memory mappings, command/environment path references and mount namespaces. A process can use a path without having its cwd there. Do not print environment contents or credentials. If an inspection gap leaves ownership unclear, skip the candidate.
5. Check descendant modification and change times, not just the top-level directory or Git index. Age is only a candidate filter. Rescue folders, active tool stores and retained evidence require their owner's policy even when old.

Do not infer abandonment from a missing `.git`, a clean Git status, no process cwd, or a thread's completed turn. Do not use a blanket worktree reaper or idle-directory sweep while other threads are active.

## Reclaim in this order

### Unused compiler output in legacy worktrees

Keep the worktree, source, unpushed commits and diagnostic state. For a confirmed-unused pre-gah checkout:

- Select only standard Cargo compiler directories: a profile's `deps/`, `incremental/`, `build/` and `.fingerprint/`, including target-triple profiles when present.
- Verify the selected paths are real directories without symlinked ancestors, contain no tracked files, and have no recent descendant writes or process references. A conservative candidate cutoff is 72 hours; it does not replace ownership checks.
- Never delete an entire `target/` by name. Older tooling stores logs, receipts, parity results and other non-Cargo state alongside compiler output there.
- Record Git status before removal and verify it is unchanged afterward. Remove only the exact reviewed directories, without following symlinks or crossing filesystems. Measure the `df` delta.

### Agent scratch and application caches

Inspect `~/.cache/agent-tmp` selectively. Preserve source changes, unpushed work, rescue copies and evidence. Delete a whole entry only when its purpose and owner establish that it is disposable and unused.

Content-keyed application binaries and controls may rebuild on a miss. Confirm that behavior in the current owning source and recheck exact entries for process use before deletion. Recent reads can matter even when writes are old.

There is no global "keep two" parity-cache rule, "keep three" nightly rule, or 48-hour run-evidence expiry. Parity observations, nightly bundles, logs and receipts need the owning repository's retention policy. Missing eviction belongs in that repository, not an increasingly aggressive workstation sweep.

### Package caches

Inspect the installed command's help and active consumers first:

- **Docker:** prefer targeted old build-cache cleanup, such as `docker buildx prune --filter 'until=48h'`, after checking for builders. Keep its confirmation. Never use blanket `docker system prune -af`; unused images can still be required VM or tool images. Leave volumes alone.
- **uv:** `uv cache prune` is the supported conservative cleanup. Avoid forcing removal or treating a recently written cache as abandoned.
- **pnpm:** skip `pnpm store prune` when a running tool executes from the store or its ownership is unclear. The store can contain live installations, not just disposable downloads.
- **mise:** preview `mise cache prune --dry-run`; apply only suitable cache candidates. `mise prune` removes installed tool versions and is not cache cleanup.

## Leave alone

- All current gah workspaces and qualification pins unless their owner explicitly selects lifecycle cleanup.
- Steam games, `~/.windows/data.img`, `~/.local/state/win-vm/` and live T3 databases such as `~/.t3/userdata/statev2.sqlite`. Sparse VM image size is not allocated disk usage.
- Repository-protected references, run evidence, fixture stores and toolchain caches. In Orderready, preserve `evidence/`, `gpui-rewrite/`, `gpui-study/`, `accesskit-dispatch/`, its protected GPUI reference worktree, and caches such as `sccache`, `mamba`, `xwin` and `occt`.
- The pacman cache and journal. Do not seek root access for these small targets during ordinary agent cleanup.

## Report

Report free space before and after, each cleanup class's measured delta, and anything deliberately kept. Distinguish deletion recovery from concurrent disk activity. Name any archive refs actually created; compiler-only cleanup needs none. Keep cleanup reports and runtime inventories out of the public vault.

## Verification

Confirm the exact selected paths were removed, source status is unchanged in preserved worktrees, and protected state remains present. Report `df -h /` rather than promising recovery from `du`. A successful cleanup does not require collecting every old workspace or making gah's dry run empty.
