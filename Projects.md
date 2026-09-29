# Projects

This is a routing map. Repositories own changing implementation detail. Read the named authoritative file before acting and follow local agent guidance.

## SWE Benchmarking

A custom software-engineering evaluator for realistic application-development tasks. It compares Pi and Codex configurations; it is not a public SWE-bench runner.

- Local: `/home/tobias/code/swe-benchmarking`
- Remote: <https://github.com/TobiasBak/swe-benchmarking>
- Default branch: `main`
- Start with `setup/README.md`; `setup/AGENTS.md` owns benchmark isolation and comparison rules.

The benchmark owns cases, agent and validation isolation, hidden checks, judgment, and result provenance. It is tamper-resistant, not a hostile-code sandbox: tested agents retain host-level capabilities, so untrusted models require a container or VM. This repository is the evaluation substrate used by [[Autoresearch]] and Skills Autoresearch.

## Skills Autoresearch

The controlled improvement loop for Agent Skills described in [[Autoresearch]].

- Local: `/home/tobias/code/skills-autoresearch`
- Branch: `main`
- Remote: <https://github.com/TobiasBak/skills-autoresearch>
- Start with `README.md`, then `program.md` for active research policy. Verify repository documentation against current controller behavior before expensive runs.

Skills Autoresearch owns candidate policy, immutable evidence, and promotion decisions. SWE Benchmarking remains its pinned, read-only evaluator rather than part of the candidate change surface.

## Dotfiles

Tobias's machine and development-environment configuration across Windows, NixOS WSL, NixOS servers, and Arch Linux.

- Local: `/home/tobias/code/dotfiles`
- Remote: <https://github.com/TobiasBak/dotfiles>
- Default branch: `main`
- Start with root `AGENTS.md`. For NixOS hosts and remote rebuild safety, use `nixos/README.md` and nested guidance.

Do not run installers or rebuild entrypoints without explicit approval. Files under the checkout are active only when the expected home or host target is a verified symlink or junction; repository content alone does not prove machine state.

Personal Pi and Codex skills are owned by the sibling `/home/tobias/code/skills` repository, not dotfiles. Some agent files are generated from their source project and must not be edited directly; check repository guidance before changing them.

[[Tailscale]] records the Taildrop receiver setup for the `pc` device.

## T3 Code

Tobias's preferred interactive environment for day-to-day coding-agent work. Use it with Codex until T3 Code supports Pi, then reconsider Pi as the provider.

Tobias confirmed 2026-07-30 that T3 Code should treat provider-native agents and harnesses as engines. Its durable product layer is the collaborative workspace and control surface around them: shared task state, interaction, policy, evidence, and provider integration. Do not build a unified generic agent loop merely to compete with model providers that train and tune models against their own harnesses. See [[AI-era software durability]].

- Local: `/home/tobias/code/t3code`
- Remote: <https://github.com/pingdotgg/t3code>
- Start with the checkout's `AGENTS.md` for source work. For the installed service and update procedure, follow `/home/tobias/code/dotfiles/AGENTS.md`, under `Installed T3 Code service`.

[[Choosing and steering coding models]] routes the daily model choice and current model guidance. [[DeepSeek V4.1 Flash in Codex]] records the separate Codex/OpenCode Go test option, its configuration route, and verified compatibility; it is not the daily default.

Service updates or restarts can terminate hosted coding-agent sessions. [[Projects#Dotfiles|Dotfiles]] owns the installed runtime's operational guidance; the T3 repository owns source development and verification.

## System Canvas

A browser workspace for discussing software systems with a coding agent on a shared Excalidraw canvas.

- Local: `/home/tobias/code/system-canvas`
- Remote: <https://github.com/TobiasBak/system-canvas>
- Default branch: `main`
- Start with `README.md`, then `PROJECT.md` for the product model and `docs/sessions-and-storage.md` for persistence semantics.

## Poly Executor

A Polymarket research system split between execution and offline model work.

- Executor: `/home/tobias/code/poly-executor`
- Offline model work: `/home/tobias/code/poly-llm`
- Stable persistent data root: `~/data`, backed by `/mnt/data-2tb/poly-data`; capture and training subtrees also resolve onto `data-2tb`
- Default branch: `main` in both repositories
- Start with the relevant `AGENTS.md`; when changing a cross-repository contract or its producer or consumer, read both repositories' guidance and owning definitions.

`poly-executor` owns capture, replay, policy, risk, and execution. `poly-llm` owns offline model work and exchanges only immutable artifacts with the executor. The deployed capture uses v4. The original v3 database was deleted on 2026-07-31 after full migration and historical parity verification; pinned archive branches retain code only, so exact v3 reproduction needs an independently retained snapshot. Persistent capture, training, paper, and research snapshot data live on `data-2tb`; the legacy `~/poly-executor-snapshots` path resolves there. Live execution is prohibited for agents; the repository guidance owns the exact capture and development allowances.

## Poly Trader

[[Poly Trader]] records the retrospective and durable lessons from Tobias's experimental Polymarket Bitcoin five-minute trader.

- Repository: `/home/tobias/code/poly-trader`
- Recovered SQLite evidence: no longer present on this machine; see [[Poly Trader]]
- Default branch: `main`
- Start with `AGENTS.md`; never enable real buys without explicit approval.

The repositories own implementation and raw evidence. The knowledge note owns the project-level interpretation and future direction.

## Cross-repository ownership

SWE Benchmarking owns task construction, evaluator policy, and benchmark evidence about pinned target-repository revisions. Skills Autoresearch owns experiments and promotion decisions while consuming that benchmark as a protected dependency. Dotfiles owns machine and agent-host configuration; the sibling skills repository owns model-invoked skill source; T3 Code owns Tobias's preferred interactive coding-agent workspace and its provider integration. Poly Executor owns capture, replay, policy, risk, and execution; its offline `poly-llm` sibling owns model-bundle and evaluation-request production.

A copied artifact, generated projection, nested checkout, or evaluation patch does not become authoritative merely because it is nearby. Follow the owning repository, verify the pinned revision or activation path, and preserve the safety boundary when work crosses repositories.
