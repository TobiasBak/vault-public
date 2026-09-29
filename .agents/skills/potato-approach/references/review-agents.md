# Focused review agents

Some engineering rules require understanding intent and context. When the codebase and static checks cannot reliably enforce a settled rule, make checking it an explicit review-agent responsibility. This implements the third level of the approach, rules and Bugbot.

Repository rules tell the implementation agent what the project expects. A focused reviewer checks whether the resulting change actually follows them. A skill explaining how to implement a feature does not replace that check.

## Give the reviewer a specific job

Start with an adopted project rule or a recurring correction. Define the concern, where it applies, and what constitutes a violation. Examples include duplicating domain knowledge across owners, hiding effects behind a misleading API, or preserving a workaround instead of repairing its owning design. Use the project's actual examples and contracts, not general taste.

Keep mechanically decidable rules in static checks. An import restriction does not need a review agent if the dependency graph can enforce it.

Give the reviewer the change's intent, the candidate revision or diff, the relevant rules, and access to the affected implementation, callers, and checks. It should follow the behavior beyond changed lines where needed, rather than accepting the author's explanation as proof. Keep review read-only against the candidate.

Select reviewers by the concerns exposed by the task. Reuse existing review tools and agents. A focused assignment does not require a permanent agent persona, a new orchestration system, or every available reviewer on every change.

## Make findings affect acceptance

A finding should identify the violated rule, affected location, supporting evidence, and consequence. Separate confirmed violations from unresolved questions. Report missing context or incomplete coverage instead of treating an unfinished review as a pass.

When adopting the review rule, define where it runs and how findings affect acceptance. If the repository requires that review, unresolved violations must be fixed or explicitly resolved by the responsible authority before the change passes. A report nobody must act on is advice, not enforcement. Follow the target repository's existing acceptance policy; creating a review reference alone does not install a gate.

A required review enforces the process, not perfect judgment. Review agents can miss violations, so do not treat their approval as a structural guarantee or a replacement for runtime verification.

## Move recurring findings into stronger protection

If a finding becomes mechanically recognizable, promote it to a compiler, lint, dependency, or CI check. If a better API or data structure removes the possibility entirely, prefer that. Keep review attention on decisions that still need context instead of repeatedly paying an agent to rediscover an enforceable rule.
