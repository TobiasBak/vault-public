# One blocking gate for agent-written code in any language

Status: v1 design settled, nothing built yet (2026-11-05).

recheck-after: 2027-02-05

## Abstract

Existing linters stop at one language, and agents erode codebases in ways that are not tied to any language: they add code beside old code, cross boundaries, swallow errors, pile defensive checks onto guaranteed types and loosen their own gates. This paper designs a single Linux binary that checks those problems from one set of rules, starting with Rust, Python and TypeScript, configured per repository, with every finding blocking. It claims that most of the erosion agents cause is visible without a type checker, in a language-neutral model of definitions, imports, references and calls. The tool is also the apparatus for the gate hypotheses in the [codebase erosion paper](agent-codebase-erosion.md).

## Thesis

A language-agnostic, always-blocking gate built on syntax trees can catch most of the erosion agents cause, with false positives rare enough that repositories keep every suite rule on.

The thesis is refuted if concept rules miss or misfire materially more often than the per-language tools they replace, if unresolved sites swamp real repositories, or if repositories disable large parts of the suite to stay usable.

## Capabilities

Each capability exists because agents reliably produce the failure it blocks. Only decidable checks become rules. A heuristic, such as a new path landing beside an old one or a new symbol resembling an existing one, appears in `report` until it is narrowed into something decidable.

### Accretion

Agents add code and rarely delete it. This is the core of the tool.

- Unused exports, files and dependencies.
- Names like `*_v2`, `new_*`, `legacy_*`, `utils2` and `helpers/`.
- Exact structural clones above a size: the same logic pasted with renamed variables.
- The same literal defined twice: a magic number, URL or status string repeated across modules.

### Boundaries and ownership

- Imports between layers along an edge the config does not declare.
- Import cycles between modules.
- Reaching into another module's internals instead of its public entry point.
- Test-only hooks in production code.

### Defensive slop

- Swallowed errors: `except: pass`, `catch {}`, `.ok()`, `let _ =`.
- Catch-all handlers that log and continue.
- Fallback defaults on decoded data: `?? default`, `.get(k, {})`, `unwrap_or_default()`.

### Over-engineering

Agents cover edge cases the types already exclude, with fallback on fallback and checks repeated deep inside code that should trust its inputs.

- Type checks an annotation already guarantees: `isinstance(x, int)` when `x: int`, `typeof x === "string"` when `x: string`, `if x is None` when `x` is not optional.
- Error handling outside a boundary.
- Useless handlers: a catch that only rethrows, a `try` nested inside a handler, a handler that returns a default.
- Fallback chains of three or more: `a ?? b ?? c ?? d`, `x or y or z or {}`, `getattr(o, "k", None)` on a typed object.

Handler density per thousand lines is a metric in `report`, which a repository can ratchet.

### Unfinished and leftover code

- Stubs: `todo!()`, `unimplemented!()`, `raise NotImplementedError`, a function whose body only passes.
- Debug output: `print`, `console.log`, `dbg!`.
- Disabled code: `if False:`, `if (false)`, dead branches behind constant conditions.

### Tests that lie

- Mocks of the repository's own modules.
- Sleeps and real timers.
- Snapshot and golden-file assertions.
- Tests reading private state.
- Skipped tests: `.skip`, `xfail`, `#[ignore]`.

### Comments

A comment that explains a workaround or justifies the code usually marks a design heading the wrong way, and the next agent copies both. The message steers toward names and types, a check that carries the reason, or an ADR. Reasoning in [documentation and naming](../agents/documentation-and-naming.md).

- Line and block comments.
- Docstrings and doc comments.
- Suppression directives such as `noqa` and `@ts-expect-error`.
- Not a shebang, or one `SPDX-License-Identifier` line at the top of a file.

### Dependencies

- A dependency imported directly that the manifest only has transitively.

### Hygiene

- JavaScript files: TypeScript only, unless the file is an out-of-scope path.
- Stray READMEs, docs directories and nested agent instruction files.
- Committed binaries and oversized fixtures.

### Ratchets

- A metric, such as clone share or handler density, above the value committed in the config.

## Design

### Shape

One static Linux binary, `riprap`, named for the rock armour that stops shoreline erosion. `check` judges a candidate and exits nonzero on any finding. `test` runs every rule's examples. `report` prints metrics and never fails. Formatters and type-aware linters stay separate tools; the repository's landing command runs them beside riprap.

Exit codes: `0` passes, `1` has findings, `2` means riprap could not run, for example on an invalid config or a rule that fails to decode. Each finding is one line naming the rule, `path:line:col`, the message and the approved path; `--json` gives the same for tools.

### Implementation language

Rust, because the hard parts already exist as Rust libraries and the tool must ship as one fast binary.

- Tree-sitter's best-maintained bindings and the grammar crates compile straight into the binary, and `ast-grep-core` supplies matching for language rules.
- A native binary has no runtime to install. mise installs it from the repository with its cargo backend; prebuilt binaries wait until a second machine needs them.
- Parallel parsing without garbage-collection pauses fits the speed target, as Ruff, Biome, oxc and ast-grep show.
- Rule files and config decode once through serde into types with no invalid states. With no severity field in the type, a warning level cannot exist.
- Rust is among the first adapters, so the tool gates its own source early.

The cost is compile time in the agent's own edit loop. Split the workspace so a rule change never rebuilds the parser, and keep a warm [target cache](../software/cargo-target-cache.md).

Extending the tool never requires Rust. Rules and config are TOML, and adapters are mostly tree-sitter query files in the style of `tags.scm`, with Rust only where a language's name resolution needs real code.

### Model

Adapters built into the tool parse with tree-sitter and map each language into one model: files and modules, definitions and exports, imports and references, calls, error handlers, tests, comments and literals. Adapters also carry language meaning for shared concepts, such as what an ignored error or a sleep call looks like in that language. Adding a language means writing one adapter; no rule changes.

v1 has adapters for Rust, Python and TypeScript including TSX. Resolution understands Cargo workspaces, uv projects and workspaces, and TypeScript's `tsconfig` paths, pnpm workspaces and `package.json` exports, following re-exports through barrel files. Other layouts are unresolved until an adapter learns them.

riprap does not duplicate the compilers. rustc already flags dead private code and `tsc` flags unused locals, so riprap covers what they cannot see: exports unused across the workspace, unused files and dependencies, and in Python, which has no compiler, private dead code too.

### Rules

Three kinds, available to the suite and to repositories alike:

- **Violation rules** produce findings. Most are concept rules, written against the model with no language. A language rule targets one language's quirk and matches its syntax with an ast-grep pattern. One crate owns the ast-grep dependency and speaks riprap's own types, so replacing ast-grep later touches only that crate.
- **Fact rules** add references or entry points to the model, so a repository's own dynamic patterns, such as a handler registry looked up by string, become visible to rules that read the graph. The suite ships fact rules for the frameworks in use, starting with pytest fixtures.
- **Config** declares layers and the edges between them, boundaries, entry points, out-of-scope paths, parameters and ratchet values.

Every rule file carries its own examples: code it must flag and code it must pass, one snippet per supported language for concept rules, and expected references for fact rules. `test` fails on any mismatch, which proves a new rule catches the mistake it was written for and catches an adapter that maps a concept wrongly.

A rule joins the suite only after a run across Tobias's repositories in which every finding is a real problem. One false positive means narrowing the rule first. Real findings are not a blocker; each repository fixes them when it upgrades riprap.

### Blocking

- The rule format has no severity field. A finding always fails `check`.
- No inline or per-file way to silence a finding exists.
- A file that fails to parse is a finding, so broken or unsupported syntax cannot hide code from the rules.
- An unresolved site is a finding when the construct is avoidable: a computed `getattr` or `importlib` name, a non-literal `import()`, `eval`. The approved paths are an explicit registry, a fact rule or a declared entry point. Language machinery that cannot be avoided, such as Rust macros, Python decorators and barrel re-exports, resolves conservatively: whatever it names counts as used, which may miss dead code but never invents a finding.
- A repository can disable a rule only as a whole, with a required reason, which stays visible in every diff of the config. Catching a loosened config is the developer's job in review, not riprap's.

### Config

`riprap.toml` in the repository root records every difference from the suite: the repository's rule directory, overrides of suite rules by id, disables with reasons, parameters, layers, boundaries, entry points, out-of-scope paths and ratchets. Out-of-scope paths are exact, never globs, so the scope cannot quietly widen.

The binary ships only the current suite. A repository's pinned riprap version in `mise.toml` is its suite version, so upgrading means bumping the pin and fixing what the new rules find in the same change.

### Candidate

`check` judges the whole tree, always: the working tree, which is the candidate in a gah workspace, or the index with `--staged`. There is no diff mode. Old findings in untouched code are still findings, and graph rules cannot be judged from a diff anyway: deleting the last caller of an export leaves the unused export in a file the diff never touched.

### Speed

A whole-tree check of orderready, about 640k lines of Rust, must finish in under a second warm, with files in the page cache and no persistent cache. A cache that gives the same result as a full run is added only if a measured run misses that.

## Build order

1. The comment rule, so riprap gates its own source from the start.
2. Language rules through ast-grep: defensive slop, over-engineering, leftovers and tests that lie.
3. The model and graph: unused code, boundaries, cycles, internals access and error handling outside boundaries.
4. Banned names and hygiene.
5. Exact clones, metrics and ratchets.

## Hypotheses

1. **Concept rules match per-language tools.** Unused-export, dead-file and boundary results agree with knip, vulture and import-linter on real repositories, except where code is dynamic. Refuted if disagreement outside dynamic code is common.
2. **Unresolved sites are rare.** On typical Python and TypeScript repositories, they number few enough to fix with fact rules or entry points in one sitting. Refuted if they swamp the real findings.
3. **The suite stays quiet on good code.** On well-maintained repositories, nearly every finding is judged real. Refuted if a rule's false positives would push a repository to disable it.
4. **Agents write correct rules in one pass.** Given a real mistake and its fix, an agent writes a rule whose examples pass and which rejects the original failure. Refuted if most attempts need human repair.
5. **Whole-tree checks are fast enough for every commit.** The orderready target above holds. Refuted by measurement under the [benchmark checklist](../skills/benchmark-checklist/SKILL.md).
6. **Blocking without silencing is livable.** Agents fix findings rather than loosening the config. The test belongs to hypothesis 6 of the [erosion paper](agent-codebase-erosion.md).

## Method

1. Compare graph rules against knip, vulture and import-linter on a handful of public repositories per language, and inspect every disagreement.
2. Run the suite on Tobias's repositories and on well-maintained public ones, and judge each finding real or false.
3. Replay recorded agent mistakes from review history: an agent writes the rule, and the rule must reject the historical change and pass the fix.
4. Time `check` on orderready, warm and cold.

Follow the [fast-loop funnel](../agents/autoresearch.md#fast-loops-first-tobias-2026-10-12): scout each measurement on one or two repositories and widen only where the signal is clear.

## Results

None yet.

## Open questions

- **Clone detection across languages.** Normalized syntax trees find renamed copies within a language; whether the model can find the same logic written in two languages is unknown and probably not worth it.
- **Other standards.** Which external style guides to absorb into the suite after v1, each rule passing the same acceptance run.

## References

- [ast-grep](https://ast-grep.github.io): fast tree-sitter pattern linter whose rules are short YAML files with separately tested valid and invalid examples. The base for language rules.
- [tree-sitter code navigation](https://tree-sitter.github.io/tree-sitter/4-code-navigation.html): per-grammar `tags.scm` queries that mark definitions and references, the mechanism behind GitHub's code navigation. A ready start on the model.
- [knip](https://knip.dev): finds unused files, exports and dependencies in JavaScript and TypeScript, with entry points declared per framework. The model for fact rules and entry-point config.
