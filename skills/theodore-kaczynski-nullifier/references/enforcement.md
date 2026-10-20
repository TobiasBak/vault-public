# Enforcement

Mechanically decidable rules become programs that exit nonzero, or CLI behavior that makes the violation impossible. `AGENTS.md` lines, skills, and review prompts are not checks. The table is each check's contract once adopted, not a to-do list.

Check acceptance establishes only the implemented mechanical property. Independent authority, meaningful behavior coverage, and the correctness of a derivation still require [contract judgment and execution](black-box-tests.md#evidence-and-authority). Keep those obligations explicit rather than claiming a metadata guard proves them.

## Checks

| Rule | Fails on | Approved path |
|---|---|---|
| Black-box tests only | Test code outside corpus and harness: inline test modules, per-module test files, test-only visibility hooks | A case in the corpus |
| Expected-output metadata | A changed or deleted expected file without a `Behavior-Change:` trailer | `<cli> accept <case> --source "<truth>"` plus the trailer |
| Harness-change metadata | Harness, canonicalizer, tolerance, or fake changes without the trailer; the guarded files are the cache key's harness set | The trailer |
| Declared coverage | A behavior-and-entry-point pair in two cases' `covers`; a declared published entry point no case covers | Extend the covering case |
| Case shape | A `covers` entry not `<area>.<outcome>@<entry>`; a field outside the [finished shape](black-box-tests.md#case-layout) | The finished shape |
| Every case has an oracle | A case record without one | The spec, reference system, or hand derivation |
| Bare expected values | A matcher outside the fixed set; a matcher repeating the case tolerance or default normalization | A bare value, or a named relation |
| Compact cases | An expected file not one line per request; two non-rejection requests with the same payload, operation, and call-level arguments where the interface takes a list | `<cli> accept`; merge the requests |
| One input set | A changed path no job claims | The owning job's inputs, or the explicit ignore list |
| Committed inputs are readable | A corpus input far larger and more compressible than the repo's real inputs; the failure prints both and the limit | A builder call |
| Zero comments | Any comment in a tracked file; a tracked format with no comment scanner not declared comment-free. Generated files exempt by exact name | Names, types, a check's failure message, a case's oracle, a `Why:` trailer |
| Prose only where allowed | Prose outside root `AGENTS.md`, skills, `--help`, case records, and exact published-contract paths; docs directories outside those paths; any README, input directories included; a published contract failing its machine check | The [owners and contract migration](agent-context.md#what-stays-out) |
| Agent context shape | Root `AGENTS.md` over 80 lines, off its sections, or with unranked or more than five values; any other `AGENTS.md`; prompt files (including `.codex/`, `.pi/`) or command docs; an unresolved concrete path or command reference in `AGENTS.md` or a skill; a host instruction file that isn't a symlink to root `AGENTS.md` | The [shape and instruction migration](agent-context.md) |
| Skill shape | A missing description; an instructional file link escaping its skill directory; an unresolved concrete path or command reference | The [skill rules](agent-context.md#skills); judge relevance and duplication on a real task |
| One verification entrypoint | A tracked runnable file (interpreter-run scripts included) or task-runner target outside the CLI's exact allowlist; a shell alias or wrapper duplicating a CLI command | The [single entrypoint](control-cli.md#one-entrypoint) |
| Budget declarations | A case without a budget or its basis | Declare both; the [runner](black-box-tests.md#runner) enforces runtime overruns |

The **gate** is the landing path invoking `<cli> check`, the single implementation of the repository's static checks. It never selects or runs cases. Do not implement a second delivery system in the repository CLI.

## Landing integration

Shared-tool help and active session instructions own delivery policy: landing procedure, review requirements, promotion qualification, and production authority. Discover the applicable policy before delivery; do not infer permission from this skill or copy the platform's playbook into repository prose.

The repository supplies static checks, behavioral jobs and their inputs, evidence, and required candidate metadata to that owner. Its integration must establish the candidate and metadata contracts below. Missing required integration is blocked, not permission to add a local landing wrapper or bypass a policy.

## Check targets

Check the exact candidate being landed, not whichever tree is easiest to inspect:

- **gah:** check the forwarded workspace, including integrated child changes. There is no staged snapshot; workspace `HEAD` alone is not the candidate. If the candidate changes before landing, rerun its checks.
- **Ordinary Git:** hooks adapt the actual staged or outgoing candidate supplied by the landing path to the same check implementation. Trailer guards inspect outgoing commits only. Changed candidate inputs invalidate their previous checks.
- Required candidate inputs that an entrypoint cannot supply are blocked prerequisites, never a pass or a rule rejection.

A guard never re-judges commits already on the remote under newer rules. Integration supplies evidence to the existing delivery system rather than adding another CI or qualification path.

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

1. Choose the checks the real task gap or broken contract needs. A speed-motivated enforcement system first passes the [value check](manifest.md#optimization-loop). Unrelated conformance is separate work.
2. Each adopted check covers the whole repo, existing violations included. Its failures call for repairs under that check, not adopting every other rule.
3. Repair until the gate passes and behavior holds. Deleting required behavior is not a repair. Deleting a suite needs explicit permission and the [migration proof](black-box-tests.md#migrating-an-existing-suite).
4. Deliver gate and repairs together to the repo's designated merge owner.

No baselines, suppressions, warning-only modes, or narrowed scope for an adopted check. Fix a wrong check against the contract; never weaken a correct one. If you stop early, leave the gate failing in the repair workspace with the command, remaining failures, and resume point in the task tracker.

## Proof

Each check rejects its mechanically specified forbidden pattern and accepts the approved one through the real landing entrypoint. Prove it checks the candidate rather than an old base or unrelated staged tree. A metadata guard also proves final-message validation after squash or parent integration, and blocks when required metadata is unavailable. Report semantic obligations separately; accepting an oracle or trailer is not proof that its claim is correct.
