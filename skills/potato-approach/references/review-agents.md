# Focused review agents

For settled rules that need intent and context to check, make checking them a reviewer's explicit job. Rules tell the implementer what's expected; the reviewer verifies the change follows them. Keep mechanically decidable rules in static checks.

- **Define the job:** the concern, where it applies, and what counts as a violation, using the project's real examples. Examples: domain knowledge duplicated across owners, effects hidden behind a misleading API, a workaround kept instead of repaired.
- **Inputs:** intent, the candidate diff, the rules, and access to implementation, callers, and checks. Follow behavior beyond the changed lines; the author's explanation is not proof. The candidate stays read-only.
- Select reviewers by the concerns the change exposes. Reuse existing review tools; no permanent personas or orchestration systems.
- **Findings:** the violated rule, location, evidence, and consequence. Separate confirmed violations from open questions, and report incomplete coverage rather than passing it.
- **Acceptance:** define where the review runs and how findings block it. A report nobody must act on is advice. A required review enforces process, not perfect judgment.
- Once a finding becomes mechanically recognizable, promote it to a check, or better, to an API that removes the possibility.
