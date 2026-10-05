# Projects

Routes to repositories. Each repository owns its implementation detail; read its `AGENTS.md` before acting. A nearby copy, generated file, nested checkout, or evaluation patch is not authoritative; follow the owning repository.

## SWE Benchmarking

Custom evaluator for realistic application-development tasks that compares Pi and Codex configurations. It is not a SWE-bench runner.

- `/home/tobias/code/swe-benchmarking`, <https://github.com/TobiasBak/swe-benchmarking>, branch `main`
- Start with `setup/README.md`; `setup/AGENTS.md` owns isolation and comparison rules.
- Owns cases, isolation, hidden checks, judgment, and result provenance. It resists tampering but is not a sandbox: tested agents keep host capabilities, so untrusted models need a container or VM.

## Skills Autoresearch

The improvement loop for Agent Skills described in [autoresearch](agents/autoresearch.md).

- `/home/tobias/code/skills-autoresearch`, <https://github.com/TobiasBak/skills-autoresearch>, branch `main`
- Start with `README.md`, then `program.md` for research policy. Verify the docs against current controller behavior before expensive runs.
- Owns candidate policy, immutable evidence, and promotion. It treats SWE Benchmarking as a pinned, read-only evaluator outside the candidate surface.

## Dotfiles

Machine and dev-environment config for Windows, NixOS WSL, NixOS servers, and Arch.

- `/home/tobias/code/dotfiles`, <https://github.com/TobiasBak/dotfiles>, branch `main`
- Start with root `AGENTS.md`; for NixOS hosts and remote rebuilds, `nixos/README.md`.
- Get explicit approval before running installers or rebuild entrypoints. A file under the checkout is active only if its home or host target is a verified symlink or junction.
- Owns the installed T3 Code service (`AGENTS.md`, section "Installed T3 Code service"), the active Codex config, and the global `AGENTS.md`.
- Windows test VM lab ownership belongs here: `oip-windows-vm`, the single shared VM limit, and workload isolation are host policy. Keep its persisted home `~/.local/share/oip-windows-vm`. Product repositories own guest qualification; frozen misc snapshots are not maintained tooling. Activated on PC by Tobias on 2026-10-04; PATH resolves `/run/current-system/sw/bin/oip-windows-vm`. Use the maintained command, not the archive. A stopped clone still belongs to its current task: wait for explicit slot release before lifecycle actions. The lifecycle lock serializes mutations; it does not grant ownership.
- Agent skills live in this vault under `skills/` (see [AGENTS.md](AGENTS.md#skills)); `scripts/bootstrap-developer-tools.sh` links them. Some agent files are generated; check guidance before editing.
- Taildrop on the `pc` device: `taildrop-receiver.service` drains incoming files to `~/Phone/Inbox`, with numbered suffixes on collisions. A manual `tailscale file get` therefore shows `0/0 files`. Configured in `nixos/home/tobias/desktop.nix`.

## T3 Code

Tobias's daily interactive coding-agent environment: Claude Opus 5.5 orchestrates and delegates to GPT-6.1 Sol in Pi (see [coding models](agents/coding-models.md#current-choice)). [Orchestrator V2](https://github.com/pingdotgg/t3code/releases/tag/v0.0.46-nightly.20261003.2610) added Pi support in the nightly released 2026-10-03.

- `/home/tobias/code/t3code`, <https://github.com/pingdotgg/t3code>
- Source work follows the checkout's `AGENTS.md`; the installed service and updates follow dotfiles. Restarting the service can kill running agent sessions.
- Direction (confirmed 2026-07-30): provider-native agents are engines. T3 owns the collaborative workspace around them (shared task state, policy, evidence, provider integration), not a generic agent loop. See [AI-era durability](software/ai-era-durability.md).
- Live provider registration: `~/.t3/userdata/settings.json`.

## StepKit

Deterministic manufacturing-fact extraction from STEP models, plus an owned Rust geometry engine meant to replace its OpenCascade dependency.

- `/home/tobias/code/stepkit`, <https://github.com/TobiasBak/stepkit>, branch `main`: Python extraction library and CLI on OCCT. Owns the output contract, recognition, unfolding, and the private corpus under `data/step-files/` (never commit it elsewhere).
- `/home/tobias/code/stepkit-geometry`, <https://github.com/TobiasBak/stepkit-geometry> (private), branch `main`: Rust/PyO3 engine. Not yet wired into StepKit. `docs/implementation-status.md` is the status of record; private evidence and receipts live in ignored `.local/`, which has no backup.
- Trim policy (decided 2026-10-05): replace the narrow proof-carrying face profiles with one general tolerance-based trim reconstruction (project 3D boundary curves into UV within the file's declared uncertainty, adaptive integration with error estimates), deleting profiles where the general path agrees. Parity bar: whole-payload area and volume within 1e-6 relative of OCCT or of the fixture's independent answer. Speed gate: native at least 10x faster than OCCT on the common-success corpus cohort. No interior fold/injectivity proofs on spline supports (OCCT does none); refuse only on problems hit during integration.
- Topology decisions in the general trim path use the declared uncertainty, not exact arithmetic: contact between two edge uses within that uncertainty of their shared authored vertex is a joint, not a recross. Agents drifted into certified rational proofs of 1e-32 crossings; that is the retired proof-carrying approach.
- On the engine's analytic fixtures, OCCT re-import is the side that disagrees with the dimension-derived answers; treat OCCT as a comparison, not truth.

## System Canvas

Browser workspace for discussing software systems with a coding agent on a shared Excalidraw canvas.

- `/home/tobias/code/system-canvas`, <https://github.com/TobiasBak/system-canvas>, branch `main`
- Start with `README.md`, then `PROJECT.md` for the product model and `docs/sessions-and-storage.md` for persistence.

## Poly Executor

Polymarket research system.

- `/home/tobias/code/poly-executor` owns capture, replay, policy, risk, and execution.
- `/home/tobias/code/poly-llm` owns offline model work: model bundles and evaluation requests. It may read manifest-selected finalized cycles from the active capture SQLite; all other exchange goes through immutable manifests. It must never import executor source or connect to a running executor.
- Both use branch `main`. For cross-repo contract changes, read both repos' guidance and owning definitions.
- Data root `~/data` lives on `/mnt/data-2tb/poly-data`, as does the legacy `~/poly-executor-snapshots`.
- The v3 database was deleted 2026-07-31 after verified migration. Archive branches hold code only, so reproducing v3 exactly needs a separately retained snapshot.
- Capture, paper, shadow, dev, and tests never submit real orders, touch wallets, or use trading credentials. Production trading only runs on an explicit request to run the production engine.
