# Enforcement

Every adopted rule is a program that exits nonzero, or a CLI behavior that makes the violation impossible. `AGENTS.md` lines, skills, and review prompts are not checks. The table is each check's contract once adopted, not a to-do list.

## Checks

| Rule | Fails on | Approved path |
|---|---|---|
| Black-box tests only | Test code outside corpus and harness: inline test modules, per-module test files, test-only visibility hooks | A case in the corpus |
| Expected output is truth | A changed or deleted expected file without a `Behavior-Change:` trailer | `<cli> accept <case> --source "<truth>"` plus the trailer |
| Harness is behavior | Harness, canonicalizer, tolerance, or fake changes without the trailer; the guarded files are the cache key's harness set | The trailer |
| One case per behavior | A behavior-and-entry-point pair in two cases' `covers`; a published entry point no case covers | Extend the covering case |
| Case shape | A `covers` entry not `<area>.<outcome>@<entry>` or naming a test; an oracle naming a repo path; a field outside the [finished shape](black-box-tests.md#case-layout) | The finished shape |
| Every case has an oracle | A case record without one | The spec, reference system, or hand derivation |
| Bare expected values | A matcher outside the fixed set; a matcher repeating the case tolerance or default normalization | A bare value, or a named relation |
| Compact cases | An expected file not one line per request; two non-rejection requests with the same payload, operation, and call-level arguments where the interface takes a list | `<cli> accept`; merge the requests |
| One input set | A changed path no job claims | The owning job's inputs, or the explicit ignore list |
| Committed inputs are readable | A corpus input far larger and more compressible than the repo's real inputs; the failure prints both and the limit | A builder call |
| Zero comments | Any comment in a tracked file; a tracked format with no comment scanner not declared comment-free. Generated files exempt by exact name | Names, types, a check's failure message, a case's oracle, a `Why:` trailer |
| Prose only where allowed | Prose outside root `AGENTS.md`, skills, `--help`, case records, and exact published-contract paths; docs directories outside those paths; any README, input directories included; a published contract failing its machine check | The [owners and contract migration](agent-context.md#what-stays-out) |
| Agent context shape | Root `AGENTS.md` over 80 lines, off its sections, or with unranked or more than five values; any other `AGENTS.md`; prompt files (including `.codex/`, `.pi/`) or command docs; a path or command in `AGENTS.md` or a skill that doesn't exist; a host instruction file that isn't a symlink to root `AGENTS.md` | The [shape and instruction migration](agent-context.md) |
| Skill shape | No description of when it applies; repeating `--help`, `AGENTS.md`, or another skill; a whole procedure that is one CLI call | The [skill rules](agent-context.md#skills) |
| One control entrypoint | A tracked runnable file (interpreter-run scripts included) or task-runner target outside the CLI's exact allowlist; a shell alias or wrapper duplicating a CLI command | The [single entrypoint](control-cli.md#one-entrypoint) |
| Budgets | A full corpus over budget | Make it faster, or raise the budget with its basis |

All static checks have one implementation, `<cli> check`, called by the landing path. Git hooks provide pre-commit and pre-push entrypoints; gah invokes the repository check through `gah merge`:
- **pre-commit:** every check needing no build, on the staged snapshot, never the working tree.
- **pre-push:** the full static check and trailer guard on the pushed commits only. The writer chooses and runs relevant behavioral tests before landing; the hook does not select or run cases. A rebase reruns pre-push.
- **Landing:** push straight to main after the checks. In a gah workspace, `gah merge` runs the repository's check and pushes main; never commit, branch or push main with Git there. Only repository-declared protected surfaces need one independent review, parallel with pre-push and clear of blocking findings before landing. Validate fixes without another independent round.
- **Promotion PR:** the full corpus and secondary platforms; any failure blocks promotion. Main may be red on suites only promotion runs. The [delivery policy](../../../tobias/preferences.md#delivery-and-releases) owns staging batches, landing-agent responsibility and Tobias-only production promotion.

A guard never re-judges commits already on the remote under newer rules. Hosted CI only where the repo already has it; never add it as part of this.

## Approved paths

Ship every ban with its approved path in the same change. The failure names rule, location, and path, and states the reason in one clause when the rule name doesn't make it plain. That makes the check the first home for a [non-obvious reason](../SKILL.md#where-the-why-goes):

```
no-unit-tests: src/parser/lexer.rs:212 defines a test module.
Extend the corpus/parser/ case that covers this behavior, or add one with input, expected, case.toml.

no-cloud-run-iam-conditions: infra/run.tf:41 adds a condition to roles/run.invoker.
Cloud Run ignores resource.name conditions. Grant the role on the service without one.
```

A `Why:` commit trailer for one-off decisions is a convention; no check requires or validates it.

## Rollout

1. Choose the checks the outcome needs. A new enforcement system goes ahead only after the [value check](../SKILL.md#the-loop), or as a scoped correctness, security, or data-loss fix. Unrelated conformance is separate work.
2. Each adopted check covers the whole repo, existing violations included. Its failures call for repairs under that check, not adopting every other rule.
3. Repair until the gate passes and behavior holds. Deleting required behavior is not a repair. Deleting a suite needs explicit permission and the [migration proof](black-box-tests.md#migrating-an-existing-suite).
4. Deliver gate and repairs together to the repo's designated merge owner.

No baselines, suppressions, warning-only modes, or narrowed scope for an adopted check. Fix a wrong check against the contract; never weaken a correct one. If you stop early, leave the gate failing on the repair branch with the command, remaining failures, and resume point recorded.

## Proof

Each check rejects the forbidden pattern and accepts the approved one through the real gate entrypoints.
