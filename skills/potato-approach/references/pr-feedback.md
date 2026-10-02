# Learn from PR feedback and later bugs

Turn review comments and escaped bugs into hardening. For each, explain what allowed the mistake, where it was caught or why it escaped, and which durable change prevents the class. A list of past fixes is not the output.

## Inspect

- Stay in the requested repos, PRs, or window, and state what you couldn't inspect. Use existing repo and issue tools.
- Read each comment with its diff, surrounding code, follow-ups, and resolution, from humans and bots alike. A comment is a claim to verify, and a resolved thread may not have fixed anything. Separate confirmed corrections from disputed advice and changed requirements.
- For later bugs, link the reproduction to the introducing change and the fix, checking contracts at those revisions. Don't blame the last PR touching the file, and mark uncertain attribution as uncertain. A requirement added later is not a defect in earlier work.
- Several comments plus a bug may be one failure. Don't count them as separate recurrences.

## Find the gap

Group by mechanism, not symptom. Ask which invariant or ownership boundary was violated, what made the mistake easy, whether protection was missing, incomplete, bypassable, or wrong, and whether another agent could still make the mistake elsewhere. Choose the response by the priority order in [SKILL.md](../SKILL.md). Some gaps need behavioral regression tests or [verification tooling](verification.md) rather than a static rule. Repeated fixes to divergent adapter code, for example, call for one owned typed interface, not a list of banned spellings.

## Report

One entry per opportunity:

- **Evidence:** comments, issue, introducing PR, fix.
- **Failure and gap:** what went wrong and what protection was missing.
- **Proposed hardening:** owner, scope, supported alternative, and level.
- **Proof:** how it would reject the historical failure but allow valid behavior.
- **Disposition:** missing, incomplete, already protected, or uncertain.

Prioritize by consequence, recurrence, and number of callers affected, not comment volume. Check that the current code doesn't already have the protection. Implementing an accepted rule follows [enforce first](hardening.md#enforce-first-repair-end-to-end). Verify each guard against the historical failure or a faithful reproduction.
