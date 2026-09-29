# Learn from PR feedback and later bugs

Use PR review comments and bugs traced to earlier PRs to find ways to harden the codebase. The result should explain what allowed a mistake, where it was caught or why it escaped, and which durable change would prevent or detect the same class of mistake. A list of past fixes is not enough.

## Inspect the evidence

Work within the requested repository, PRs, subsystem, or time window. State what was inspected and what was unavailable. Use existing repository and issue tools; this review does not need a new collection service or database.

Read review discussions alongside the relevant diff, surrounding code, follow-up revisions, and final resolution. Include both human and automated comments. A comment is a claim to investigate, not proof of a defect or authority to impose a new rule. A resolved thread does not establish that the underlying problem was fixed. Separate confirmed corrections from disputed advice, false positives, and changes in requirements.

Distinguish mistakes caught before merge from bugs found afterward. A useful review comment may show a working review process whose repeated effort belongs in stronger protection. A later bug also raises the question of why it escaped the existing process.

For a later bug, connect the issue or reproduction to the introducing change and the eventual fix, when known. Check the behavior and contracts at those revisions, not just today's code. Do not blame the last PR touching a file or assume a linked PR caused the bug. Mark uncertain attribution as uncertain and say what evidence is missing. A requirement introduced later is not a defect in a PR that correctly followed the earlier contract.

Preserve links to the useful comments, issues, PRs, and revisions. Several comments and a later bug may describe one underlying failure; do not count them as independent recurrences.

## Find the prevention gap

Group findings by the mechanism that allowed the mistake, not merely the symptom or file. For each group, ask:

- Which invariant, ownership boundary, or engineering decision did the change violate?
- What in the codebase made the mistake possible or easy to copy?
- Did protection not exist, have incomplete coverage, permit bypasses, encode the wrong expectation, or require judgment the reviewer never applied?
- What did the fix repair, and can another agent still make the same mistake elsewhere?

Use the skill's priority order to choose the response. Prefer types, APIs, ownership, and canonical examples that remove the mistake, then static checks for remaining detectable violations. Give context-dependent rules to [focused review agents](review-agents.md). Use [engineering workflows](engineering-workflows.md) for missing investigation methods, not as a replacement for enforceable rules.

Some gaps need behavioral regression checks or better [verification tools](verification-cli.md) and [feature maps](feature-map.md). Identify the missing scenario or observation. Do not force a runtime-only failure into a static rule, or stop at a regression test when a structural repair can prevent the whole class.

For example, repeated fixes to divergent adapter-unwrapping code suggest one typed interface owned by the runtime, not a growing list of forbidden spellings. Check other callers before proposing the scope of that rule.

## Return actionable hardening candidates

Produce a compact report with one entry per distinct opportunity. Each entry needs:

| Field | Useful content |
|---|---|
| Evidence | Source comments, issue, introducing PR when established, and corrective change |
| Failure and gap | The mistake, why it was possible, where it was caught, and what protection was missing |
| Proposed hardening | The owning code or rule, intended scope, supported alternative, and place in the priority order |
| Proof | How the proposed protection would reject or detect the historical failure while allowing legitimate behavior |
| Disposition | Missing protection, incomplete protection, already protected, or still uncertain; name any unresolved decision |

For a proposed static check, identify the executable tool or rule and its pre-commit and CI entrypoints. A Markdown instruction is not implemented protection. [Codebase hardening](codebase-hardening.md#static-checks-are-executable-enforcement) defines the implementation and verification requirements.

Prioritize consequence, observed recurrence, and the number of affected callers over comment volume. One consequential bug can justify protection; repeated minor opinions do not automatically justify a repository-wide ban. Check current code and gates before proposing work that has already been completed. Omit findings that yield no useful hardening opportunity rather than forcing every comment into a rule.

## Carry accepted rules into hardening

A review-only task returns candidates and recommendations. It does not modify product code, post comments, or close issues. When implementation is already authorized and the rule and scope are settled, follow [Enforce first, repair end to end](codebase-hardening.md#enforce-first-repair-end-to-end): enable the full gate, let violations fail, and repair the affected behavior without baselines or suppressions.

Verify a new guard against the historical failure or a faithful reproduction, as well as valid behavior. Keep the evidence with the resulting change so the next agent can tell which failure it prevents. A proposed rule is not an installed guard, and a successful bug fix alone does not establish that recurrence is prevented.
