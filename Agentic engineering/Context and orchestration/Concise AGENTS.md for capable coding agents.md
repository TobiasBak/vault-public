# Concise AGENTS.md for capable coding agents

AGENTS.md should add what the active model, host, tools, and task do not supply. Express chosen collaboration and necessary local context while leaving room for judgment. Good advice alone does not earn a place.

## What an instruction adds

Different kinds of guidance have different reasons to exist:

- **Chosen collaboration and priorities:** desired relationship, taste, and tradeoffs. These need no failure-prevention justification, but not every preference warrants steering every session.
- **Local facts and obligations:** authority boundaries, external contracts, and hidden operating conditions the agent cannot recover before they matter.
- **Corrective coaching:** compensation for current capability gaps or recurring behavior. Old failures or imaginable mistakes do not establish need after the model or host changes.

Compare rules with active instructions and tools. Duplication is inspectable; expected behavior needs judgment. Not every deletion or preference needs a benchmark. Seek evidence where uncertainty could change the decision, especially for real obligations.

There is no mandatory inventory of commit rules, generated-file warnings, testing reminders, or engineering maxims. Their category alone does not justify inclusion. Tobias wants his chosen partner and priorities, not a catalog of precautions against earlier models.

## Placement and authority

Place knowledge according to its scope, when the agent needs it, and whether it requires guidance or executable enforcement:

| Information | Owning place |
|---|---|
| Current goal, accepted scope, success criteria, and task-specific decisions | Current request and working state; preserve these through continuation and handoffs |
| Chosen behavior or obligations across repositories | Global instructions, within the user's approved scope |
| Standing repository behavior, local authority boundaries, and required retrieval triggers | Repository or nested `AGENTS.md`, with a short route to conditional detail |
| Domain knowledge, rationale, project orientation, and detailed findings | Authoritative code or retrievable subject and project notes, with recognizable names and links |
| A reusable method that needs judgment on particular tasks | A narrowly triggered skill linked to its tools and references |
| Mechanically enforceable invariants or repeatable operations | Types, APIs, checks, or maintained tools; instructions may point to them |

Code, manifests, scripts, task runners, and CI expose implementation and ordinary commands. Prose command maps and architecture inventories need a purpose beyond collecting discoverable facts. Follow repository documentation conventions; filenames alone do not assign ownership. See [[Irreducible codebase documentation]] and [[Search-driven code discoverability]].

Retrievable notes can keep explanation and historical findings without making them mandatory workflows.

Use [[Agent context engineering#Decide what context matters]] to find what real tasks need beyond the model, host, instructions, tools, and retrieval routes. Recording a principle does not ensure timely use. Missing knowledge, missing triggers, unclear instructions, and noncompliance need different repairs.

Write the smallest complete instruction at its owning scope: purpose, applicability, required behavior, and needed references. Preserve meaning for judgment. Provider examples and research inform this choice; do not paste them wholesale.

"Search before creating a note" does not trigger retrieval before advice. If informed advice is required, say when to retrieve. Standing instructions can require recovery of goals and success criteria from the request and knowledge without imposing one plan or verification checklist on every task.

Where behavior is uncertain, check whether normal instructions let an agent find and use knowledge without coaching. File reads and wording checks do not establish use. For startup or handoff uncertainty, exercise a representative fresh-session task and keep conclusions scoped to it.

Moving text into a skill does not guarantee timely activation. Check the earliest action that needs it, including resumed tasks and user answers. [Firstmate's September 2026 extraction](https://github.com/kunchenguid/firstmate/pull/5872) reported live load-timing regressions; the follow-up widened validation-supervision triggers to cover user answers and restored rules inline. Text surviving elsewhere is not enough.

Policy stays active until an authorized change replaces it, even during an audit. Let clear user requests satisfy genuine authorization conditions. A hazard does not authorize inventing prohibitions or approval gates.

## Remove without replacing

Delete unnecessary coaching without adding reviewers, hooks, checklists, or narrower copies. Do not retain ideas that add no reusable knowledge.

Moving a real contract into permissions, tools, tests, or review needs validation proportional to failure consequences. Removing generic advice already supplied by the host or no longer wanted does not.

Targeted review can own change-specific concerns without requiring a separate reviewer or service for ordinary work. [[Context-sensitive code review]] covers native and orchestrated review.

## Keep the intended meaning

Preserve chosen character and consequential distinctions; cut their repeated explanation. Shortness is not the goal, and memorability alone does not justify an instruction.

Revisit guidance when the user, model, host, or work changes. Judge what it adds now. Use ordinary work or focused comparisons for uncertainty, not mandatory audit ceremony. [[Agent context engineering]] covers active context; [[Prompting tool-using agents]] covers the task.
