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
| One verification entrypoint | A tracked runnable file (interpreter-run scripts included) or task-runner target outside the CLI's exact allowlist; a shell alias or wrapper duplicating a CLI command | The [single entrypoint](control-cli.md#one-entrypoint) |
| Budgets | A full corpus over budget | Make it faster, or raise the budget with its basis |

The **gate** is the landing path invoking `<cli> check`, the single implementation of the repository's static checks. It never selects or runs cases. The [delivery policy](../../../tobias/preferences.md#delivery-and-releases) owns writer-chosen tests, review, landing authority, and promotion qualification. Do not implement a second delivery system here.

## Check targets

Check the exact candidate being landed, not whichever tree is easiest to inspect:

- **gah:** check the forwarded workspace, including integrated child changes. There is no staged snapshot; workspace `HEAD` alone is not the candidate. If the candidate changes before landing, rerun its checks.
- **Ordinary Git:** pre-commit runs checks needing no build on the staged snapshot. Pre-push runs the full static check on the outgoing candidate and the trailer guard on outgoing commits only. A rebase reruns pre-push. Hooks adapt these snapshots to the same check implementation.
- Required candidate inputs that an entrypoint cannot supply are blocked prerequisites, never a pass or a rule rejection.

A guard never re-judges commits already on the remote under newer rules. Hosted CI only where the repo already has it; never add it as part of this.

## Landing metadata

Trailer rules apply to the diff and message that will reach the target history:

- `Behavior-Change:` names the source of truth for changed expectations or harness behavior. Child validation does not replace validation of the combined candidate.
- A squash or parent landing must carry applicable `Behavior-Change:` and `Why:` trailers into the proposed final message. Child commits alone do not preserve rationale in main's history. This is a landing-integration contract, not a reminder for agents to copy text.
- The trailer guard receives the candidate diff and proposed message before landing. It must not inspect an old `HEAD` message or assume child messages become the final one. Missing metadata integration blocks an adopted guard; invoking a check command alone does not establish this integration. Fix the gap at the owning landing tool, not with a repo-local merge wrapper.

`Why:` remains optional rationale; no check requires or validates its content.

## Approved paths

Ship every ban with its approved path in the same change. The failure names rule, location, and path, and states the reason in one clause when the rule name doesn't make it plain. That makes the check the first home for a [non-obvious reason](../SKILL.md#where-the-why-goes):

```
no-unit-tests: src/parser/lexer.rs:212 defines a test module.
Extend the corpus/parser/ case that covers this behavior, or add one with input, expected, case.toml.

no-cloud-run-iam-conditions: infra/run.tf:41 adds a condition to roles/run.invoker.
Cloud Run ignores resource.name conditions. Grant the role on the service without one.
```

## Rollout

1. Choose the checks the outcome needs. A new enforcement system goes ahead only after the [value check](../SKILL.md#the-loop), or as a scoped correctness, security, or data-loss fix. Unrelated conformance is separate work.
2. Each adopted check covers the whole repo, existing violations included. Its failures call for repairs under that check, not adopting every other rule.
3. Repair until the gate passes and behavior holds. Deleting required behavior is not a repair. Deleting a suite needs explicit permission and the [migration proof](black-box-tests.md#migrating-an-existing-suite).
4. Deliver gate and repairs together to the repo's designated merge owner.

No baselines, suppressions, warning-only modes, or narrowed scope for an adopted check. Fix a wrong check against the contract; never weaken a correct one. If you stop early, leave the gate failing in the repair workspace with the command, remaining failures, and resume point in the task tracker.

## Proof

Each check rejects the forbidden pattern and accepts the approved one through the real landing entrypoint. Prove it checks the candidate rather than an old base or unrelated staged tree. A metadata guard also proves final-message validation after squash or parent integration, and blocks when required metadata is unavailable.
