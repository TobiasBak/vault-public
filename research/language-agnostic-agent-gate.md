# One blocking gate for agent-written code in any language

Status: design draft, nothing built yet (2026-11-05).

recheck-after: 2027-02-05

## Abstract

Existing linters stop at one language, and agents erode codebases in ways that are not tied to any language: they add code beside old code, cross boundaries, swallow errors and loosen their own gates. This paper designs a single Linux binary that checks those problems across the popular languages from one set of rules, configured per repository, with every finding blocking. It claims that most of the erosion agents cause is visible without a type checker, in a shared model of definitions, imports, references and diffs. The tool is also the apparatus for the gate hypotheses in the [codebase erosion paper](agent-codebase-erosion.md).

## Thesis

A language-agnostic, always-blocking gate built on syntax trees can catch most of the erosion agents cause, with false positives rare enough that repositories keep every default rule on.

The thesis is refuted if concept rules miss or misfire materially more often than the per-language tools they replace, if unresolvable dynamic code swamps real repositories, or if repositories disable large parts of the default suite to stay usable.

## Capabilities

Each capability exists because agents reliably produce the failure it blocks. The default suite covers all of them.

### Accretion

Agents add code and rarely delete it. This is the core of the tool.

- Unused exports, files and dependencies.
- A new path landing beside the old one without removing it.
- Names like `*_v2`, `new_*`, `legacy_*`, `utils2` and `helpers/`.
- Structural clones: the same logic pasted with renamed variables.
- A new symbol whose name or signature duplicates an existing one.
- The same literal rule defined twice: a magic number, URL or status string repeated across modules.

### Boundaries and ownership

- Imports crossing declared layers.
- Import cycles between modules.
- Reaching into another module's internals instead of its public entry point.
- Test-only hooks in production code.

### Defensive slop

- Swallowed errors: `except: pass`, `catch {}`, `.ok()`, `let _ =`, an ignored `err`.
- Catch-all handlers that log and continue.
- Fallback defaults on decoded data: `?? default`, `.get(k, {})`, `unwrap_or_default()`.

### Unfinished and leftover code

- Stubs: `todo!()`, `unimplemented!()`, `raise NotImplementedError`, a function whose body only passes.
- Debug output: `print`, `console.log`, `dbg!`.
- Disabled code: `if False:`, `if (0)`, dead branches behind constant conditions.

### Tests that lie

- Mocks of the repository's own modules.
- Sleeps and real timers.
- Snapshot and golden-file assertions.
- Tests reading private state.
- Skipped tests: `.skip`, `xfail`, `#[ignore]`.

### Dependencies

- A new third-party dependency not listed in the repository config. Adding it to the list is a gate-config change, so a human sees it.
- A dependency imported directly that the manifest only has transitively.

### Gate integrity

These check the diff against the base revision, never the candidate's own config.

- Edits to lint, formatter, CI or gate config.
- A new `disable`, a loosened threshold or a changed suite version.
- Per-file ignores and allowlists in other tools' config.

### History

- Changed or deleted migrations the base already contains.
- Ratchets: a continuous metric such as clone share or concentrated complexity may not get worse than its committed value.
- Changed paths no check or job claims.

### Hygiene

- Comments, where the repository bans them.
- Stray READMEs, docs directories and nested agent instruction files.
- Hand edits to generated files.
- Committed binaries and oversized fixtures.

## Design

### Shape

One static Linux binary. `check` runs the gate and exits nonzero on any finding. `test` runs every rule's examples. `report` prints metrics and never fails. Formatters and type-aware linters such as `ruff format`, `rustfmt` and Clippy run as declared steps, so a repository still has one entrypoint, but the tool does not reimplement them.

### Shared model

Language adapters built into the tool parse with tree-sitter and map each language into one model: files and modules, definitions and exports, imports and references, calls, error handlers, tests, comments and literals. Adapters also carry language meaning for shared concepts, such as what an ignored error or a sleep call looks like in that language. Adding a language means writing one adapter; no rule changes.

The first adapters cover Python, TypeScript and JavaScript, Rust and Go.

### Rules

Three kinds, available to the default suite and to repositories alike:

- **Violation rules** report a problem. Most are written against the shared model and carry no language. A rule that targets one language's quirk names the language and uses a raw syntax pattern.
- **Fact rules** add references or entry points to the model, so a repository's own dynamic patterns, such as a handler registry looked up by string, become visible to graph rules. The default suite ships fact rules for common frameworks.
- **Config** declares layers, entry points, dependency lists and ratchet values.

Every rule file carries its own examples: code it must flag and code it must pass, one snippet per supported language for concept rules, and expected references for fact rules. `test` fails on any mismatch, which proves a new rule catches the mistake it was written for and catches an adapter that maps a concept wrongly.

Every message names the rule, the location and the approved path. Output is plain text for agents and humans, and JSON for tools.

### Blocking

- The rule format has no severity field. A finding always fails `check`.
- No inline or per-file suppression exists.
- Code the adapter cannot resolve, such as `getattr` with a computed name, is itself a finding. The approved paths are an explicit registry, a fact rule or a declared entry point.
- A repository can disable a rule only as a whole, with a required reason, and adding that `disable` is a gate-integrity finding.

### Repository config

One file in the repository root. It pins the default suite version, so upgrading the tool never changes what blocks until the repository moves to the new suite and fixes everything it finds in the same change. It then adds the repository's rule directory, overrides default rules by id, disables rules with reasons and sets parameters. Shared rule packs are importable but optional.

### Candidate

`check` runs on the exact candidate: the staged tree in a commit hook, or the outgoing commits against their base in a push or landing path. Diff rules compare against that base. Parsing is parallel and incremental over changed files plus whatever the graph says they affect.

## Hypotheses

1. **Concept rules match per-language tools.** Unused-export, dead-file and boundary results agree with knip, vulture and import-linter on real repositories, except where code is dynamic. Refuted if disagreement outside dynamic code is common.
2. **Unresolved code is rare.** On typical Python and TypeScript repositories, unresolved findings number few enough to fix with fact rules or entry points in one sitting. Refuted if they swamp the real findings.
3. **The default suite stays quiet on good code.** On well-maintained open-source repositories, nearly every finding is judged real. Refuted if a rule's false positives would push a repository to disable it.
4. **Agents write correct rules in one pass.** Given a real mistake and its fix, an agent writes a rule whose examples pass and which rejects the original failure. Refuted if most attempts need human repair.
5. **It is fast enough to run on every commit.** Checking a typical change in a medium repository takes well under a second warm. Refuted by measurement under the [benchmark checklist](../skills/benchmark-checklist/SKILL.md).
6. **Blocking without silencing is livable.** Agents fix findings rather than editing gate config. The test belongs to hypothesis 6 of the [erosion paper](agent-codebase-erosion.md).

## Method

Build the shared model, the accretion and boundary rules, and the diff rules first. They are the part no existing tool covers across languages, and the erosion paper needs them.

1. Compare graph rules against knip, vulture and import-linter on a handful of public repositories per language, and inspect every disagreement.
2. Run the default suite on well-maintained public repositories and judge each finding real or false.
3. Replay recorded agent mistakes from review history: an agent writes the rule, and the rule must reject the historical change and pass the fix.
4. Time `check` on real changes, warm and cold, on an isolated machine.

Follow the [fast-loop funnel](../agents/autoresearch.md#fast-loops-first-tobias-2026-10-12): scout each measurement on one or two repositories and widen only where the signal is clear.

## Results

None yet.

## Open questions

- **Name.** The tool needs one.
- **Rule syntax.** Extend ast-grep's pattern language, use raw tree-sitter queries, or define a small concept language over the shared model. The concept rules decide this.
- **Clone detection across languages.** Normalized syntax trees find renamed copies within a language; whether the model can find the same logic written in two languages is unknown and probably not worth it.
- **Where ratchet values live.** In the repository config, where lowering a value passes and raising one is a gate-integrity finding, or computed from the base revision on every run.

## References

- [ast-grep](https://ast-grep.github.io): fast tree-sitter pattern linter whose rules are short YAML files with separately tested valid and invalid examples. The closest existing base for the violation rules.
- [tree-sitter code navigation](https://tree-sitter.github.io/tree-sitter/4-code-navigation.html): per-grammar `tags.scm` queries that mark definitions and references, the mechanism behind GitHub's code navigation. A ready start on the shared model.
- [knip](https://knip.dev): finds unused files, exports and dependencies in JavaScript and TypeScript, with entry points declared per framework. The model for fact rules and entry-point config.
