# Codebase cleanup

Agents extend accepted code, including its mistakes. Remove bad examples, keep one supported implementation path, and prevent recurrence. Cleanup changes what the next agent learns from the repository.

## Remove the misleading precedent

Find the owner of the behavior before changing the workaround. Do not extend it because it is nearby or makes the smallest diff. Fix the design where the problem belongs, using [Approved implementation paths](approved-paths.md) when the supported alternative is missing.

Move affected callers to that path and remove obsolete alternatives within the task's scope. Do not leave a second implementation for agents to copy. Keep the canonical example current.

For hardening work, follow [Enforce first, repair end to end](codebase-hardening.md#enforce-first-repair-end-to-end) before migrating callers. Enforce against existing violations as well as new ones. If repairs span passes, leave the remaining failures visible in the enabled gate instead of exempting old code.

## Comments and repository rules

Recommend a repository-wide no-code-comments rule, enforced by lint or CI, when choosing repository rules. This is the local skill's adopted recommendation, not permission to override an existing project policy. Do not leave an adopted rule to each agent's judgment about which comments are useful.

Comments can make a workaround look approved and teach the next agent to copy it. Remove the underlying compromise instead of merely deleting its explanation. Make the design clear through names, structure, types, and checks. Preserve necessary rationale and external contracts in their owning documentation.

Change adopted rules deliberately, not through local exceptions that agents will copy.

## Finish with a usable example

Verify the behavior affected by the cleanup and any new check against the known bad pattern. Review the result as the next agent's starting point: can it make the next ordinary change without inventing an exception?

Recommend broader cleanup when the evidence warrants it, but do not expand the task into an unrelated repository-wide sweep.
