# SCIP indexers: cost and what they execute

recheck-after: 2027-02-06

`rust-analyzer scip` builds and runs project code unless `cargo.buildScripts.overrideCommand` replaces the build step; the `enable = false` switches do not stop it. Indexing costs seconds and gigabytes, so a SCIP index belongs in an audit, not in a per-commit gate. The [gate paper](../research/language-agnostic-agent-gate.md#results) records what an index would add to riprap.

## What each indexer executes

- **rust-analyzer 0.3.3105, `rust-analyzer scip`.** It runs `cargo metadata`, which downloads crate sources but runs nothing. It then runs `cargo check`, which compiles and runs every build script, the project's included, and builds the proc macros it later loads. `--config-path` with `cargo.buildScripts.enable: false` and `procMacro.enable: false` still ran ripgrep's `build.rs`, pcre2-sys's C build, and the serde and thiserror derives. Only `{"cargo": {"buildScripts": {"overrideCommand": ["true"]}}}` stopped it; then no `target/` appears. It sets `RUSTUP_AUTO_INSTALL=0`, so a repository's `rust-toolchain.toml` cannot install a toolchain, and it needs a cargo on `PATH` (`mise exec rust@<version> rust-analyzer@latest -- …`).
- **Cost of the safe mode.** Without proc macros, items under attribute macros lose their bodies: a Leptos `#[component]` function had no occurrences, so its calls looked unused. Tobias's repositories lost 2 of 256 attributed items in the orderready subset.
- **scip-typescript 0.6.1.** It uses the TypeScript compiler API and runs no project code. Run it through `pnpm dlx` without installing the repository's dependencies, so their types stay unresolved.
- **scip-python 0.6.8.** It is pyright-based. It calls the Python interpreter to find `sys.path`, and pip to list packages unless `--environment` names a file. Run it with `--environment` pointing at a file containing `[]`, and put a `python`/`python3` shim on `PATH` that execs `python3 -I`. Otherwise the interpreter starts in the repository root, and a planted `json.py` would run.
- **External signatures.** rust-analyzer emits signatures only for workspace symbols. A call into std or a dependency resolves to an exact symbol, such as `lib/fs/remove_file().` or Result's `unwrap_or`, with no return type.

## Cost

Measured 2026-11-06 on a 16-thread Ryzen 7 7800X3D under `nice`, `systemd-run --user --scope -p MemoryMax=8G`, one indexer at a time, one run each. Rust used the safe mode above. Peak memory is the scope's `memory.peak`.

| Repository | Language, lines | Wall | Peak | Index |
|---|---|---|---|---|
| claude-mail | Rust, 2k | 2.9 s | 1.4 GB | 0.35 MB |
| ripgrep | Rust, 55k | 4.3 s | 1.0 GB | 8.6 MB |
| kasse | Rust, 26k | 6.0 s | 1.2 GB | 5.3 MB |
| orderready subset, 40 of 77 crates | Rust, 201k plus vendored dependencies | 25 s | 4.0 GB | 42 MB |
| orderready | Rust, 646k | killed at 8 GB after 76 s | — | — |
| agent-of-empires | Rust, 622k | killed at 8 GB after 157 s | — | — |
| zod | TypeScript, 103k | 7.9 s | 1.1 GB | 17 MB |
| umami | TypeScript, 161k | 7.4 s | 0.75 GB | 23 MB |
| rich | Python, 52k | 16 s | 0.82 GB | 4.5 MB |
| httpx | Python, 18k | 4.8 s | 0.55 GB | 2.8 MB |

With build scripts and proc macros on, claude-mail took 22 s and 2.65 GB, and orderready hit the 8 GB cap after 240 s. Lowering the LRU capacity, using one thread or passing `--exclude-vendored-libraries` did not save orderready. rust-analyzer has no incremental SCIP mode, so every run pays the full cost.

Reading an index is cheap: the Rust `scip` 0.6 crate decoded the 42 MB orderready-subset index and mapped 413k occurrences by position in about 130 ms, at 201 MB peak.
