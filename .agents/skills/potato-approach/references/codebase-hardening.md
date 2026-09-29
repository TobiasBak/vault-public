# Codebase hardening

Make routine work straightforward for less capable agents and busy people with little context. Correct work should not require the strongest model, repeated engineering advice, or constant supervision.

## Enforce first, repair end to end

Once the rule and its intended scope are settled, enable enforcement before cleaning up existing violations. The codebase-first knowledge hierarchy does not mean repairing everything before adding the gate.

1. Implement the check over the full agreed scope, including existing violations. Confirm that it accepts the supported pattern and rejects the forbidden one.
2. Wire the executable check into pre-commit and CI as a failing requirement, not an advisory report. Verify both entrypoints run it and propagate failure. Run it and use its failures as the repair inventory.
3. Repair the owning design and follow the effects through affected callers, tests, fixtures, and runtime behavior. Rerun the gate as work proceeds. Do not defer type-checking coverage until after the code has been repaired.
4. Continue until the enforced rule passes across its scope and the affected behavior works. Passing the gate by removing required behavior is not a repair.

Do not introduce a migration baseline, per-file suppression, warning-only mode, or narrower coverage to make known in-scope violations appear acceptable. Fix an incorrect check against the actual contract; do not weaken a correct rule to accommodate the current code.

If work must stop before all repairs are complete, leave enforcement enabled and the remaining failures visible. Record the command, unresolved failures, and where repair should resume. A later pass can finish the work; the current state is unfinished hardening, not a green or completed migration. During an active hardening task, a failing gate starts the repair work rather than ending the task.

## Put engineering knowledge into the design

Start with a real correction or recurring mistake. Identify the decision the engineer supplied, the behavior it protects, and the owner of the relevant state and effects. Do not encode an accidental feature of one failed patch as a universal rule.

Prefer changing types, data structures, APIs, and ownership boundaries so the mistake cannot be expressed through the supported interface. Existing code is the example future agents will follow. A written rule cannot compensate for a design that makes the forbidden shortcut easier than the correct implementation.

Give recurring work one conventional location, a small supported API, and a current example worth copying. Read [Approved implementation paths](approved-paths.md) when designing that alternative. Use the project's existing modules and tools before inventing a framework.

## Static checks are executable enforcement

A static check is a program that analyzes source, types, configuration, or dependencies and returns a nonzero exit status when the rule is violated. It runs without an agent interpreting the rule. Instructions in `AGENTS.md`, `SKILL.md`, another Markdown file, or a review prompt are guidance, not static checks. A CI job needs an actual checker behind it; naming the job after a rule does not implement that rule.

Use existing compilers, type checkers, linters, and dependency-analysis tools before writing a custom checker. Implement the rule in executable tooling or tool-consumed configuration. A repeated correction should become a repository-wide constraint when the invariant applies repository-wide. Failures must name the broken rule, affected location, and supported repair.

Keep one repository-owned rule implementation and configuration. Run it through both the installed pre-commit hook and CI; do not duplicate the rule in separate local and CI scripts. Integrate hook installation into the repository's normal setup so a checked-in hook configuration is not mistaken for an active hook. CI must run the check independently because local hooks can be skipped. Both paths must cover the rule's intended scope and propagate failure rather than swallowing it or reporting only a warning.

Demonstrate rejection of a known violation and acceptance of the supported pattern through the real check and its hook/CI entrypoints. Keep the invocation and result as evidence. If CI has not run, say so; local success and workflow configuration alone do not establish a passing CI run. Do not claim the check blocks merging unless the repository's merge policy requires its result. Markdown may explain or link to this machinery, but documentation alone never completes a static-check task.

For example, an engineer's knowledge that host-only work must stay out of the renderer belongs in separate modules and a checked import boundary. It should not depend on every agent remembering a performance warning. The [search example](approved-paths.md#worked-example-search-in-a-desktop-app) shows the supported path alongside the restriction.

## Keep guidance for what still needs judgment

For rules that need context-sensitive judgment, give [focused review agents](review-agents.md) responsibility for checking the actual change against explicit repository rules. This is the third level, rules and Bugbot, not merely another reminder to the implementation agent. A project can require the review before accepting a change, though a reviewer can still miss a violation.

Skills preserve useful methods such as choosing a trace or interpreting a performance comparison. They guide how work happens; review agents judge the resulting change. Human-enforced style guides are the weakest backstop because a person must notice every violation.

When extracting an experienced engineer's knowledge, choose its owner deliberately. Put invariants in structure or checks, context-dependent review criteria in reviewer instructions, repeatable mechanics in commands, and investigation choices in [engineering workflows](engineering-workflows.md). Keep rationale and external constraints in their owning documentation. Do not maintain prose copies of rules already expressed by the code or tool.

## Check the result

Exercise the supported user behavior and confirm that the known invalid operation or dependency is rejected. Static constraints do not prove runtime correctness or performance; use the existing verification tools for those claims.

If old examples still teach the forbidden approach, follow [Codebase cleanup](codebase-cleanup.md) within the task's scope. Inspect an API that keeps attracting misuse before adding another instruction. The next ordinary change should need less coaching.
