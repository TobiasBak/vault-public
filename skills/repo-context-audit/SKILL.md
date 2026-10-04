---
name: repo-context-audit
description: Audit repository instructions, documentation ownership, and retrieval for context that adds value beyond the active model and host.
---

# Repository context audit

Find which repository context adds information and which just constrains competent work. Keep knowledge retrievable without turning it all into instructions.

## Instructions

Compare each instruction with what the active model, host, tools, and task already supply. Being correct, prudent, or once useful doesn't mean an instruction adds value now. Sort them into three kinds:

- **Chosen collaboration:** how the user wants to work. Needs no error-prevention justification, but not every preference belongs in every session.
- **Local facts:** real authority boundaries and contracts the agent would otherwise miss. A possible hazard doesn't create a prohibition.
- **Corrective coaching:** keep only for a concrete current gap, not an imaginable mistake or an old model's habit.

No topic, such as commit rules, generated files, or testing, is a mandatory category. Deleting unneeded coaching needs no replacement hook, reviewer, or benchmark. Moving a real obligation elsewhere does need verification proportional to its consequences.

## Knowledge and retrieval

Look for competing authorities, implementation copied into prose, and useful rationale that is hard to find. Code owns behavior; docs keep intent, rationale, contracts, and terms. Follow the repo's existing doc conventions. To test retrieval, run searches drawn from real tasks, errors, and domain terms, and check whether they reach the owner. Fix the route that fails. One narrow search proves nothing missing, and this audit isn't a code refactor.

## Recommendations

Give each material finding a location, why it matters, and the treatment. For governing instructions, show the exact diff and say whether it retires coaching or changes policy. Deletion can be the whole improvement; moving, adding docs, or adding enforcement each needs its own reason. When the context already serves the work, recommend no change.

## Verification

After edits, rerun the representative searches and check links whose destinations moved. If code behavior changed, verify through the public interface or real use. Report changes and remaining uncertainty.
