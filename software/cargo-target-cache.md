# Cargo target cache safety

Preserve compatible Cargo contexts, but verify their source identity. A narrow preparation command cannot establish that other cached variants are obsolete, and inherited artifacts do not by themselves prove freshness for another source tree.

recheck-after: 2026-11-04

## Preserve contexts across preparation

Crates with the same name can have different dependency versions, feature sets and target kinds. Check-only outputs and linked builds also serve different consumers. Neither unread fingerprints nor a recent-access window establishes that a context is disposable.

Let Cargo resolve compilation freshness and repository tools define cleanup. Workspace orchestration should retain inherited build contexts rather than infer their usefulness from one warmup. Retiring a workspace remains a separate lifecycle operation; preserving contexts does not mean keeping all derived state forever.

### Measured preservation result

On 2026-10-28, GAH's automatic pruner deleted useful GUI contexts after an app/test warmup. Removing that pruner avoided repeated Cargo work without changing compiler optimization or application behavior.

Five alternating pairs used frozen Orderready source, Rust 1.99.0 and a busy shared Ryzen 7 7800X3D. Both sides began with warm preparation and GUI contexts. One GAH session cgroup measured repository preparation, optional original pruning, then the GUI build. Fetching, snapshot creation and publication were outside this boundary.

| Metric | Pruning median (range) | Preservation median (range) |
| --- | ---: | ---: |
| CPU seconds | 145.47 (142.03 to 155.78) | 1.25 (1.24 to 1.33) |
| Elapsed seconds | 28.91 (25.12 to 42.56) | 1.28 (1.20 to 1.44) |
| GUI Cargo units reprocessed | 74 (74 to 74) | 0 (0 to 0) |

Every confirmed run succeeded and produced the same executable hash. This was about 99.1% less CPU work for the measured warm-cache transition, not a cold-build or whole-workstation speedup. Cargo unit counts include compiler-cache restores; they do not count LLVM executions.

Preservation retained about 711 MiB of apparent cache files. That is not exclusive btrfs space. A real offline Cargo regression exercised multiple dependency versions, features and check/build contexts, then ran the resulting programs. The landed change is `27d11777b1bd58772524ae333d8fc776f30f474f`. Its project-owned evidence note, `spikes/cargo-cache-preservation-2026-10-28.md`, records the reproduction, full distributions and excluded hash-mismatch scout. Raw evidence stays with that project.

## Make changed source visible to Cargo

Preserving artifacts is not permission to reuse another tree's binary. A shared `CARGO_TARGET_DIR` across worktrees or snapshots can return stale products when changed content has older mtimes than the previous build. Cargo's path-member fingerprints did not distinguish the filesystem paths in the observations below.

The sharing owner needs content-hash tracking. Hold the invalidation/build lock while advancing mtimes for changed source files, and update the recorded hashes only after success.

Observed on 2026-10-14:

- A verdict used another worktree's artifacts. That tree's palette mutation failed three cases; the apparent build took 0.08 seconds.
- A separate baseline/candidate comparison was invalid: both binaries had one hash, the candidate was reported `Fresh`, and DWARF `comp_dir` identified the baseline tree. Preserved snapshot timestamps, archive extraction and older checkouts can create this freshness hazard.

## Match cache controls to the claim

Use separate empty target directories when isolating cold builds. To measure warm reuse, establish equivalent warm contexts before applying the treatment instead; clearing them would change the workload.

For a source-change experiment, prove that the intended code reached the product. For a cache-policy experiment, hold source and compiler flags fixed and check the expected product identity. A different hash is not an automatic correctness failure, but an unexplained mismatch cannot pass an identical-product guard. A zero-compilation consumer can be the intended result; a cached test verdict is not evidence that a behavioral test executed.

Use the [benchmark checklist](../skills/benchmark-checklist/SKILL.md) for confirmation. Related: [verification latency](../agents/verification-latency.md) and [background-work coalescing](background-work-coalescing.md).
