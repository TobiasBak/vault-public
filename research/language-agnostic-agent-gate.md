# One blocking gate for agent-written code in any language

Status: v1 built; all five build steps and the two-layer suite landed (2026-11-05).

recheck-after: 2027-02-05

## Abstract

Existing linters stop at one language, and agents erode codebases in ways that are not tied to any language: they add code beside old code, cross boundaries, swallow errors, pile defensive checks onto guaranteed types and loosen their own gates. This paper designs a single Linux binary that checks those problems from one set of rules, starting with Rust, Python and TypeScript, configured per repository, with every finding blocking. It claims that most of the erosion agents cause is visible without a type checker, in a language-neutral model of definitions, imports, references and calls. The tool is also the apparatus for the gate hypotheses in the [codebase erosion paper](agent-codebase-erosion.md).

## Thesis

A language-agnostic, always-blocking gate built on syntax trees can catch most of the erosion agents cause, with false positives rare enough that repositories keep every suite rule on.

The thesis is refuted if concept rules miss or misfire materially more often than the per-language tools they replace, if unresolved sites swamp real repositories, or if repositories disable large parts of the suite to stay usable.

## Capabilities

Each capability exists because agents reliably produce the failure it blocks. Capabilities are anti-patterns, and anti-patterns do not depend on language: the suite's generic rules are one rule per anti-pattern, which riprap applies to whichever languages the candidate contains. Problems that exist in only one language live in that language's group, which extends the generic rules and applies whenever the candidate contains the language. Only decidable checks become rules. A heuristic, such as a new path landing beside an old one or a new symbol resembling an existing one, appears in `report` until it is narrowed into something decidable.

### Accretion

Agents add code and rarely delete it. This is the core of the tool.

- Unused exports, files and dependencies.
- Names like `*_v2`, `new_*`, `legacy_*`, `utils2` and `helpers/` on files and directories. On definitions only `_v2` and `utils2` hold: every `legacy_*` and `new_*` definition in Tobias's repositories was a real name, compatibility handling or a creation verb.
- Exact clones: production functions whose syntax trees match once names are numbered by first use and literals reduced to their kind, at 50 or more body tokens. Tests and trait-impl members are excluded.
- Repeated literals: a module-level constant defined in two files of one language, either a distinctive string of eight or more characters or a same-named number above 10 that is neither round nor a power of two.

### Boundaries and ownership

- Imports between layers along an edge the config does not declare.
- Import cycles between modules.
- Reaching into another module's internals instead of its public entry point.
- Test-only hooks in production code.

### Defensive slop

- Swallowed errors: a catch-all `except: pass`, an empty `catch {}`.
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
- Debugger calls: `breakpoint()`, `pdb`, `debugger`, `dbg!`.
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

- JavaScript files: TypeScript only. A repository whose runtime mandates JS disables the rule; a single served script becomes an out-of-scope path.
- READMEs anywhere, docs directories except a root `docs/adr/`, and nested agent instruction files.
- Committed binaries, decided by executable signature: ELF, Mach-O, PE, ar, WebAssembly, Python bytecode. Images and other assets never match.
- Oversized fixtures: at least 128 KiB and compressing at least 64-fold. Real inputs in Tobias's repositories compress under 40-fold.

### Ratchets

- A metric above the value committed in the config. The finding sits on that value's line in `riprap.toml` and lists the metric's top contributors, because a ratchet promises something about the whole codebase and any single contributor may be untouched old code.

The metrics `report` prints:

- **Clone share:** the percentage of production lines in functions that copy an earlier function.
- **Concentrated complexity:** the percentage of complexity mass, cyclomatic complexity times the square root of lines, held by functions above complexity 10.
- **Handler density:** production error handlers per thousand production lines.

## Design

### Shape

One static Linux binary, `riprap`, named for the rock armour that stops shoreline erosion. `check` judges a candidate and exits nonzero on any finding. `test` runs every rule's examples. `report` prints metrics and never fails. Formatters and type-aware linters stay separate tools; the repository's landing command runs them beside riprap.

Exit codes: `0` passes, `1` has findings, `2` means riprap could not run, for example on an invalid config, a rule that fails to decode, or a file it cannot parse. Each finding is one line naming the rule, `path:line:col`, the message and the approved path; `--json` gives the same for tools.

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

- **Violation rules** produce findings. The suite has two layers. A generic rule names an anti-pattern that exists in more than one language; its id, message and approved path carry no language, and its language-specific shapes are conditions inside it, one per language, each an ast-grep condition or a model concept. Adding a language adds conditions, and one disable turns the anti-pattern off everywhere. A language group, one per language, holds language rules for problems only that language has, such as mutable default arguments in Python, `as any` in TypeScript or `#[allow]` in Rust. A group adds rules on top of the generic ones and never changes them. A repository's own rules may be either kind. One crate owns the ast-grep dependency and speaks riprap's own types, so replacing ast-grep later touches only that crate.
- **Coverage** is explicit for generic rules. For each anti-pattern and language, the rule either covers it, declares it not applicable with a reason, such as `except` in Rust, or leaves it unbuilt, and `riprap test` prints the matrix, so a gap is a visible cell rather than a missing file.
- **Fact rules** add references or entry points to the model, so a repository's own dynamic patterns, such as a handler registry looked up by string, become visible to rules that read the graph. The suite ships fact rules for the frameworks in use, starting with pytest fixtures.
- **Config** declares layers and the edges between them, boundaries, entry points, out-of-scope paths, parameters and ratchet values.

Every rule file carries its own examples: code it must flag and code it must pass, one snippet per supported language for concept rules, and expected references for fact rules. `test` fails on any mismatch, which proves a new rule catches the mistake it was written for and catches an adapter that maps a concept wrongly.

A rule joins the suite only after a run across Tobias's repositories in which every finding is a real problem. One false positive means narrowing the rule first. Real findings are not a blocker; each repository fixes them when it upgrades riprap.

### Blocking

- The rule format has no severity field. A finding always fails `check`.
- No inline or per-file way to silence a finding exists.
- A file riprap cannot parse means riprap could not run: exit 2, naming each file and position, never a skipped file, so broken or unsupported syntax cannot hide code from the rules. riprap cannot tell a grammar gap from truly broken syntax, and the compiler catches the latter anyway. Vendored code that hits a gap becomes an out-of-scope path.
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

Build step 1, 2026-11-05: a release build checked orderready's whole tree, 2,389 Rust files and about 640k lines, in 0.346 s wall on one warm run without a cache, on a shared Ryzen 7 7800X3D with 16 threads under load average 2.4. One run, so no variance figure. tree-sitter-rust 0.24.2 failed on four valid files under `third_party/`, among them `dyn 'static + FnOnce()`, which led to parse failures exiting 2 instead of being findings.

Build step 2, 2026-11-05: 31 language rules joined the comment rule. Each had zero false positives in an acceptance run across Tobias's 12 repositories, judged by the building agent under his standards. Getting there took narrowing: `except: pass` counts only catch-all handlers, `.get(k, {})` only chained with a literal key, `unwrap_or_default()` only after a JSON accessor. Plain `print` and `console.log` were dropped because every hit was a script's real output. The same orderready check took a median of 387 ms over 10 warm runs (376 to 427 ms) on 16 threads, against 320 ms for the comment rule alone, so one shared walk for all language rules costs about 65 ms. Parsing each file once matters more: in the `patterns` measurements a second parse cost about three times the whole matching walk, and walking once per rule cost about 330 ms per rule.

Build step 4, 2026-11-05: seven path rules over every file, with examples written as small file trees. All had zero false positives across the 12 repositories; the counts are mostly READMEs, 187 of them. orderready stayed at 403 ms. omarchy, which carries 190 MB of media, went from 43 to 153 ms because the binary check reads each file's first bytes in sequence.

Build step 3, 2026-11-05: the model and graph, with cross-file resolution for Cargo workspaces, uv projects and TypeScript paths, workspaces and barrels. Usage in Rust and Python is matched by name, which gives up some recall to avoid false positives. Decorators and macros count as machinery, treated as used until a fact rule resolves them; pytest fixtures, autouse fixtures, hooks and Nautilus extensions ship as fact rules. Across the acceptance run every finding was judged real: 129 mocks of the repository's own modules, 60 test-only hooks, 44 unused definitions, 19 unused and 11 transitive dependencies, 7 unresolved sites, 4 internals accesses, 2 unused files and 1 test nothing starts. Rust import cycles were dropped because module cycles are legal Rust. Layer and boundary rules were proved on fixtures only, because no repository declares layers yet.

Hypothesis 1, first evidence: on six Python repositories vulture reported 694 items. riprap flagged 17 of them and nothing vulture missed. Of the rest, 343 are outside riprap's scope, such as attributes and locals, 317 are framework or test code that riprap correctly keeps, and 17 were cases where riprap was right on inspection, such as names used only from strings. One was a real miss: a dead helper in a unittest subclass, which riprap keeps because it treats every method of a class with an external base as a possible override.

The orderready check grew to a median of 685 to 776 ms against 406 to 414 ms for the step 4 binary, over three interleaved rounds of 11 warm runs under load average 1.8 to 5.7 from other agents. An instrumented run split the time into about 360 ms parsing and inspecting files, 95 ms building the graph and 45 ms in concept rules. It is under the one-second target, so no cache was added.

Build step 5, 2026-11-05: exact clones, repeated literals, `report`, ratchets and a speed pass. Both new rules had zero false positives across the 12 repositories after narrowing. Clones stopped flagging enum-to-string tables, `get` and `get_mut` twins, trait delegations and tests. Literals had to drop raw occurrences, which numbered in the thousands, coincidental numbers with different names, round numbers and comparisons across languages. orderready's real findings were mostly one colour and type-scale palette copied into about five UI modules. Metric values across the repositories ranged from 0 to 4.75 for clone share, 29 to 86 for concentrated complexity and 1.3 to 17 for handler density. riprap commits its own values as its first ratchets.

The orderready check settled at a median of 635 ms, with 6.6 s of CPU, under load average 6 to 9. Parallel file reads, query compilation and rule execution won back about 140 ms, and the new features cost about 74 ms. The check is now bound by tree-sitter parsing, which takes about 40 percent of the CPU, the model query and ast-grep, so the next large gain needs a cache or less parsing. omarchy measured 693 ms before the speed pass and 217 ms after; step 3's mention building over its 66 MB of text was serial, which made step 4's 153 ms figure stale.

Two-layer suite, 2026-11-05: per-language twins such as `swallowed-error-python` merged into generic rules, with findings identical apart from ids on all 12 repositories. The coverage matrix has 90 cells: 80 covered, 7 not applicable for Rust with reasons, such as import cycles and redundant type checks, and 3 not built, which are Rust swallowed errors and private state in tests for Rust and TypeScript. New cells and rules all passed acceptance: a handler that only returns a default in all three languages, Rust log-and-continue limited to logging then `continue`, Rust rethrow-only limited to tail matches that `?` can always replace, and language-group rules for Python mutable defaults, TypeScript `any`, Rust `.unwrap()` in production code and `#[allow]`. Production-only rules exempt poisoned locks, panicked threads and literal parsing; `.unwrap()` hits on orderready dropped from 487 to 0 once test modules were recognized. Clones, literals and metrics now count production code only. A complexity-density metric, total cyclomatic complexity per thousand production lines, joined the report, ranging from 120 in orderready to 509 in pi-workspace-view. riprap declared its own layers and boundaries: zero layer-edge findings, and removing one declared edge produced seven, which proves the rule on real code. The orderready check measured 507 ms against 492 ms before.

## Open questions

- **Clone detection across languages.** Normalized syntax trees find renamed copies within a language; whether the model can find the same logic written in two languages is unknown and probably not worth it.
- **Rust swallowed errors.** `let _ =` and a statement-level `.ok();` were dropped from step 2: of 57 hits in Tobias's repositories, 23 sat in `Drop` impls and most of the rest were sends to a hung-up receiver or best-effort cleanup. Telling those from real swallowing needs types.
- **Private state in tests for Rust and TypeScript.** Python's `_name` convention is visible in syntax; Rust's non-`pub` items and TypeScript's `private` members need type information to tell from public access.
- **Recall in classes with external bases.** riprap treats every method of such a class as a possible override, so a dead helper in a unittest subclass passes. A per-framework list of hook names would close it.
- **TypeScript coverage.** Only two of Tobias's repositories carry real TypeScript, so the acceptance evidence there is thin.
- **Other standards.** Which external style guides to absorb into the suite after v1, each rule passing the same acceptance run.

## References

- [ast-grep](https://ast-grep.github.io): fast tree-sitter pattern linter whose rules are short YAML files with separately tested valid and invalid examples. The base for language rules.
- [tree-sitter code navigation](https://tree-sitter.github.io/tree-sitter/4-code-navigation.html): per-grammar `tags.scm` queries that mark definitions and references, the mechanism behind GitHub's code navigation. A ready start on the model.
- [knip](https://knip.dev): finds unused files, exports and dependencies in JavaScript and TypeScript, with entry points declared per framework. The model for fact rules and entry-point config.
