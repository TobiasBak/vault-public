# Cargo target cache safety

- For A/B comparisons, build each variant in its own empty `CARGO_TARGET_DIR`. Before trusting results, verify the intended change reached the binaries: different SHA hashes, DWARF `comp_dir`, or a Cargo log showing `Compiling` for the changed crate.
- Shared target caches need content-hash tracking. Under a lock covering invalidation and the build, bump the mtime of files whose content changed since the last build into that target and update the hash record after a successful build.

A shared `CARGO_TARGET_DIR` across worktrees or source snapshots can silently link another tree's artifacts.
Cargo fingerprints workspace (path) members without their filesystem paths and judges source freshness by mtime.
If tree B has the same package names and source mtimes older than tree A's last build, Cargo can report `Fresh` and give B A's binary. Preserved snapshot mtimes, `cp -p`, archive extraction, or an older checkout can trigger this.
- Observed on 2026-10-14: a verdict was cached for the wrong tree; another worktree's palette mutation failed three cases, and a 0.08 s "build" produced a stale app.
- A second observation that day invalidated a baseline/candidate comparison: both binaries had the same SHA, the candidate log said `Fresh`, and DWARF `comp_dir` pointed at the baseline tree.
