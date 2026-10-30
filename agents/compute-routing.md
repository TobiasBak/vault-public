# Compute routing

Model roles, targets and effort for delegated work. Tobias's explicit current request overrides these defaults under [instruction precedence](instructions-and-prompts.md); the mechanics of dividing work live in [subagent delegation](subagent-delegation.md).

recheck-after: 2027-01-24

Keep the execution contract (permissions, tools, limits, output) separate from model routing; [subagent delegation](subagent-delegation.md) owns how to judge the result.

T3 Code's `delegate_task` inherits the parent's provider unless the call selects `target.providerInstanceId` or `target.driverKind`. Keeping the provider and model unchanged also preserves model options. This describes host behavior, not permission to inherit Opus for delegated work. Explicitly select the worker provider and model under Tobias's policy below. Explain unexpected routing from the recorded call's target and the parent's provider at call time, not just the current thread config or a model-name prefix.

Tobias's default model routing, revised 2026-10-17:

- **Team leads:** non-UI leads use GPT-6.1 Sol at reasoning `high`; UI leads use Claude Opus 5.5 at effort `high`. The chief of staff remains Opus. Its [lead brief](../.agents/skills/chief-of-staff/scripts/brief.md) owns team-specific delegation, authority gates and reporting; its [skill](../.agents/skills/chief-of-staff/SKILL.md) owns quota admission. Never switch running leads mid-task. Opus is never a child, designer or researcher.
- **GPT-6.1 Sol, reasoning `high`:** every subagent, delegate and reviewer, UI included, and non-UI leads. Never delegate to Opus (Tobias, 2026-10-25: no quota for Opus subagents; the dotfiles routing hook denies Opus targets). Select the model explicitly; never inherit the leader's provider or model. Run Sol through Codex, `{"providerInstanceId":"codex","model":"gpt-6.1-sol","options":{"reasoningEffort":"high"}}`: Tobias has more Codex quota than Pi's Subscription Sharing limit ([Pi operations](pi-operations.md)), and moved delegates there after Pi children hit that limit (2026-10-29). Pi's target is `{"providerInstanceId":"pi","model":"openai/gpt-6.1-sol","options":{"thinking":"high"}}`. Keep `high` over `medium` (Tobias, 2026-10-20): on one fresh run of a routine review plus a test change, `medium` cut model time 141→96 s but missed a valid review note that `high` caught. T3's `pi`, `claudeAgent` and `codex` instances run through `gah-pi`, `gah-claude` and `gah-codex` (Codex since 2026-10-30), so under git-at-home those targets give each child its own workspace on the leader's line. UI agents load `frontend-design` and judge the UI critically from real app-window screenshots, never host-desktop captures. Give children full access; put limits like "read-only" in the task. Only project-declared protected surfaces require a review subagent; trust artifacts, not done reports.
- **Claude Haiku 5.5:** retired (Tobias, 2026-10-12). The dotfiles routing hook denies Haiku targets.


Routing can need enforcement: Claude parents in T3 followed the host's native-tool preference over prose and selected `Agent`. The hook denies it and tells the agent to do the work itself. [Dotfiles](../projects.md#dotfiles) owns the shared global instructions and Claude routing hook; keep enforcement aligned with this policy.

See also: [coding models](coding-models.md) for capability, price and effort evidence; the [team note](../.agents/skills/chief-of-staff/SKILL.md) for team leadership.