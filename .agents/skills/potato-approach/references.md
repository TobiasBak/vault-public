# Potato approach references

## Original video

[Watch Lauren Tan's full video on X](https://x.com/poteto/status/2102050467505430555/video/1), posted by [@poteto](https://x.com/poteto) on 2026-09-21. Roughly 38 minutes, originally prepared for Cursor Compile London.

The topic index below uses approximate positions from the video's captions and slides. It preserves the source topics; the linked local guides adapt selected ideas for our work.

## Topics in the video

| Position | Topic |
|---|---|
| 00:00 to 06:45 | Trust before parallelism. Reduce the human bottleneck by improving the agent's environment. |
| 06:45 to 09:00 | Runtime verification, performance evidence, and the distinction from formal methods such as Lean and TLA+. |
| 09:00 to 10:15 | Control Glass. A maintained control CLI replaces scripts reinvented each session. |
| 10:15 to 12:30 | Feature maps connect vague reports to product behavior, navigation, and verification. Maintain them with the product. |
| 12:30 to 14:45 | Shared engineering skills and pstack preserve expert methods beyond checking functional correctness. |
| 14:45 to 18:45 | Prefer codebase structure, then static analysis, rules/Bugbot, skills, and finally human-enforced style guides. |
| 18:45 to 20:30 | Dune makes the easiest implementation correct for low-context contributors. |
| 20:30 to 26:30 | Bad examples spread. Remove debt, keep one supported path, prevent recurrence. Dune bans comments to stop workaround propagation. |
| 26:30 to 30:30 | Dune's feature ownership, process separation, and import checks encode architectural knowledge. |
| 32:30 to 35:30 | An outer automation loop connects reports and telemetry to agents that reproduce and fix issues. |
| 35:30 to 38:02 | Use recurring corrections to choose which part of the environment to improve. |

## Related source material

- [pstack](https://github.com/cursor/plugins/tree/main/pstack), Lauren's public engineering skills and workflows.
- [Create a verification skill](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md), including a project-specific control interface and feature map.
- [Maintain a verification skill](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md), including source inspection and live checks of mapped features.
- [Lean](https://lean-lang.org/) and [TLA+](https://lamport.azurewebsites.net/tla/tla.html), the formal-method examples mentioned in the talk. They are not prerequisites for ordinary runtime verification.

The pstack links follow its current version, not a frozen copy of what existed when the talk was recorded. Use them as source material, not instructions to import its models, tools, or execution permissions into another project.

## Local topic guides

| Need | Reference |
|---|---|
| Extract hardening opportunities from PR comments and bugs traced to earlier changes | [Learn from PR feedback and later bugs](references/pr-feedback-review.md) |
| Encode engineering knowledge in structure and checks before relying on guidance | [Codebase hardening](references/codebase-hardening.md) |
| Check context-dependent engineering rules against an actual change | [Focused review agents](references/review-agents.md) |
| Remove bad examples and competing patterns without letting them return | [Codebase cleanup](references/codebase-cleanup.md) |
| Design a supported implementation path with clear ownership and enforced boundaries | [Approved implementation paths](references/approved-paths.md) |
| Make setup, application control, and evidence collection repeatable | [Verification CLIs](references/verification-cli.md) |
| Help agents find and exercise user-facing behavior | [Feature maps](references/feature-map.md) |
| Preserve useful investigation and implementation methods | [Engineering workflows](references/engineering-workflows.md) |

The [SKILL.md](SKILL.md) keeps the five-level priority order and routes to the relevant topic guides. The hierarchy chooses where knowledge belongs; the routes choose what work a task needs. Outer-loop automation and formal methods are retained here as source topics, not implemented local workflows.

## Distinctions for the local skill

- A **feature map** explains what the product does and how to reach and verify it. It complements a control CLI; it is not a source-file inventory.
- The [fresh-agent handoff check](references/verification-cli.md#check-the-fresh-agent-handoff) is our operational test of reduced coaching, not a procedure quoted from the talk.
- The [focused-review guide](references/review-agents.md) makes the rules/Bugbot level operational for our projects. Its reviewer assignments and acceptance guidance are local adaptations, not a prescribed process from the talk.
- [Learning from PR feedback and later bugs](references/pr-feedback-review.md) is our retrospective workflow for finding hardening opportunities. It extends the correction-to-enforcement principle rather than reproducing a procedure from the talk.
- [Enforce first, repair end to end](references/codebase-hardening.md#enforce-first-repair-end-to-end) is Tobias's explicit hardening policy. Unfinished repairs leave the gate failing; migration baselines and suppressions must not hide them. This rollout policy is a local decision, not a claim about the talk's prescribed sequence.
- The local recommendation for a repository-wide no-comments rule reflects [[Tobias's developer preferences]]. The talk supplies Dune's example; adopting a rule in another repository remains a project decision.

Related vault knowledge: [[Agentic engineering#Constrained codebases for low-context contributors]], [[Agentic end-to-end testing]], and [[Irreducible codebase documentation]].
