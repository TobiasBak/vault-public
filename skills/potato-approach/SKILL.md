---
name: potato-approach
description: Design, implement, refactor, or review agent-maintained code so the easiest change is the correct one. Use for recurring mistakes, PR feedback, later regressions, enforced rules, shared engineering workflows, or project verification tools and feature maps. Not for prose or vault-note editing.
---

# Potato approach

Agents copy the code they read and take the easiest local path. Make that path correct, and give agents the tools to see whether their change works. Source: Lauren Tan's [talk](https://x.com/poteto/status/2102050467505430555/video/1) (2026-09-21) and her [pstack](https://github.com/cursor/plugins/tree/main/pstack) skills, adapted.

## Understand and equip

- Trace the behavior through its owning code, callers, state, and effects, and find how to run and observe it. Use both source and runtime; neither alone shows how the product behaves.
- Make that understanding recoverable. Code structure carries ownership; a feature map carries what the product does and how to reach it.
- Verification needs working capabilities, not "test your changes": set up state, exercise behavior, inspect results, collect diagnostics. Static checks protect settled rules; runtime verification shows the change works. You need both.

## Where knowledge goes

For a correction or settled decision, use the strongest place that fits:

1. Codebase structure and examples, so the mistake can't be expressed.
2. Executable static checks in pre-commit and CI. Markdown is never a check.
3. Repository rules enforced by focused review agents.
4. Skills, for methods that need judgment.
5. Human-enforced style guides.

This order decides where knowledge lives, not what to do on every task. When a correction repeats a rule that is already written down, the prose failed: fix the mistake and move the rule up a level in the same change.

## Pick the work

| Situation | Reference |
|---|---|
| Repeated mistakes, too many choices, rules to enforce, bad examples or workarounds to remove, comments | [hardening.md](references/hardening.md) |
| Rules that need judgment to check | [review-agents.md](references/review-agents.md) |
| Mining PR comments, fix and revert commits, and escaped bugs for missing protection | [mistake-history.md](references/mistake-history.md) |
| Choosing a design or screening a proposed shape | [design.md](references/design.md) |
| Agents can't find, run, or verify product behavior | [verification.md](references/verification.md) |
| Agents repeatedly need help choosing an investigation method | [engineering-workflows.md](references/engineering-workflows.md) |

Combine them as needed: cleanup removes bad examples, and hardening prevents their return.

## Verification

Show the new check rejecting the known bad pattern and accepting the supported one through its real pre-commit and CI entrypoints, and exercise the affected user behavior through the project's verification tooling. A passing static check proves the rule, not the behavior.
