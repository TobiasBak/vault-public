# Enforcement

Every rule adopted for the selected outcome is a program that exits nonzero, or a CLI behavior that makes the violation impossible. The table defines adopted checks, not an implementation backlog. AGENTS.md lines, skills, and review prompts are not checks.

## Checks

| Rule | Fails on | Approved path |
|---|---|---|
| Black-box tests only | Test code outside corpus and harness: inline test modules, per-module test files, test-only visibility hooks | A case directory in the corpus |
| Expected output is truth | A modified or deleted expected file without a `Behavior-Change:` trailer | `<cli> accept <case> --source "<truth>"` plus the trailer |
| Harness is behavior | Changes to harness, canonicalizer, tolerances, or fakes without the trailer; the guarded set is the cache key's harness set | The trailer |
| One case per behavior | A behavior and entry-point pair in two cases' `covers`; a published entry point no case covers | Extend the covering case |
| Case shape | A `covers` entry off `<area>.<outcome>@<entry>` or naming a test; an oracle naming a path in this repository; a field outside the [finished shape](black-box-tests.md#case-layout) | The finished shape |
| Every case has an oracle | A case record without one | The spec, oracle system, or hand derivation |
| Bare expected values | A matcher outside the closed set; a matcher that restates the case tolerance or default normalization | A bare value, or a named relation |
| Compact cases | An expected file not in the canonical writer's one-line-per-request form; two non-rejection requests with the same payload, operation, and call-level arguments where the interface takes a list of subjects | `<cli> accept`; merge the requests |
| One input set | A changed path no job claims | The owning job's inputs, or the explicit ignore set |
| Committed inputs are readable | A corpus input far larger and more compressible than the repository's real inputs; the failure prints both and the limit | A builder call |
| Zero comments | Any comment in a tracked file; a tracked format with no comment scanner that isn't declared commentless. Generator-owned files are exempt by exact name | Names, types, checks |
| Prose only where allowed | Prose outside root `AGENTS.md`, skills, CLI `--help`, case records, and exact approved published-contract paths; docs directories outside those paths; any README, input directories included; an approved contract failing its machine check | The [owners and contract migration](agent-context.md#what-stays-out) |
| Agent context shape | Root `AGENTS.md` over 80 lines, off its sections, or with unranked values or more than five; any other `AGENTS.md`; prompt files (including `.codex/` and `.pi/` prompts) or command docs; a path or command named by `AGENTS.md` or a skill that doesn't exist; a host instruction file that isn't a symlink to root `AGENTS.md` | The [shape and instruction migration](agent-context.md) |
| Skill shape | A missing applicability description; duplicated CLI `--help`, `AGENTS.md` instructions, or another skill; a skill whose entire procedure is one CLI invocation | The [skill rules](agent-context.md#skills) |
| One control entrypoint | A tracked runnable path, interpreter-invoked scripts included, or task-runner target outside the CLI's exact allowlist; a configured shell alias or wrapper duplicating a CLI command | The [single entrypoint](control-cli.md#one-entrypoint) |
| Budgets | A full corpus over budget | Make it faster, or raise the budget with its basis |

One implementation per check: the control CLI's `check`. The gate is the commit hooks calling it: pre-commit runs every check that needs no build against the staged snapshot, never the working tree; pre-push runs the full static check plus touched corpus cases on the pushed head, from cache when green, with no new failures versus main, and the trailer guard over the pushed commits only. Touched-case selection is conservative, but a change it can't map to cases (shared code, harness, dependencies, budgets) runs that code's own tests plus one smoke case per lane, never the full corpus. Report failures already on main without blocking the push. The full corpus and secondary platforms run on the promotion PR under the [product testing and promotion rule](../../../tobias/preferences.md#testing-and-debugging). A guard never re-judges commits already on the remote under rules they predate. Hosted CI only where the repository already has one. Never add hosted CI as part of this.

## Approved paths

Ship every ban with its approved path in the same change. The failure names rule, location, and path:

```
no-unit-tests: src/parser/lexer.rs:212 defines a test module.
Extend the corpus/parser/ case that covers this behavior, or add one with input, expected, case.toml.
```

## Rollout

1. Select checks required by the chosen consumer outcome. A new enforcement system proceeds only after the [value check](../SKILL.md#the-loop), or as a scoped correctness, security, or data-loss fix. Unrelated conformance is separate work.
2. Each adopted check covers the whole repo, existing violations included. Its failures identify repairs for that check, not a mandate to adopt every other rule.
3. Repair until the gate passes and behavior holds. Deleting required behavior is not a repair. Suite deletion requires explicit authority and the [migration proof](black-box-tests.md#migrating-an-existing-suite).
4. Deliver gate and repair together to the repository's designated merge owner.

No baselines, suppressions, warning modes, or narrowed scope for an adopted check. Fix a wrong check against the contract; never weaken a correct one. Stopping early leaves the gate failing on the repair branch with the command, remaining failures, and resume point recorded.

## Proof

Each check rejects the forbidden pattern and accepts the approved one through the real gate entrypoints.
