# Concise AGENTS.md for capable coding agents

AGENTS.md should add useful information beyond the active model, host instructions, tools, and task. Good advice does not automatically belong there. The goal is to express the intended collaboration and necessary local context while leaving the agent room to exercise judgment.

## What an instruction adds

Different kinds of guidance have different reasons to exist:

- **Chosen collaboration and priorities:** the relationship, taste, and tradeoffs the user wants. These do not need an error-prevention justification, but even a genuine preference may not be worth steering every session.
- **Local facts and obligations:** information the agent cannot otherwise recover before it matters, including actual authority boundaries, external contracts, and hidden operational conditions.
- **Corrective coaching:** instructions meant to compensate for an unmet capability or recurring behavior. An old failure or imaginable mistake does not establish a current need when the model or host has changed.

Compare with the active instructions and tools before retaining or adding a rule. Direct duplication is inspectable; expected model behavior still involves judgment. Neither every deletion nor every preference needs a benchmark. Evidence matters where uncertainty could change the decision, especially when a real obligation relies on the instruction.

There is no mandatory inventory of commit rules, generated-file warnings, testing reminders, or engineering maxims. Such topics can carry a real local requirement, but their category alone does not justify inclusion. Tobias's current direction is to specify the partner and priorities he wants rather than preserve a catalog of precautions against earlier models.

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

Code, manifests, named scripts, task runners, and CI already expose much of a repository's implementation and ordinary commands. A prose command map or architecture inventory needs a purpose beyond collecting discoverable facts. Follow the repository's chosen documentation conventions; a filename alone does not establish what knowledge belongs there. [[Irreducible codebase documentation]] and [[Search-driven code discoverability]] cover ownership and retrieval.

Keeping useful knowledge does not require making it instruction. Retrievable notes may preserve richer explanation and historical findings without requiring the agent to enact them as a workflow.

When creating or revising `AGENTS.md`, use [[Agent context engineering#Decide what context matters]] to identify the behavior and information needed for real tasks. Compare those needs with what the model, host, active instructions, tools, and retrieval routes already supply. A principle being recorded somewhere does not establish that the agent will encounter or apply it in time. Distinguish missing knowledge, a missing retrieval trigger, unclear instructions, and failure to follow a clear instruction; they call for different repairs.

Translate the finding into the smallest complete instruction at its owning scope. State the purpose, when it applies, the required behavior, and a route to supporting knowledge where needed. Preserve enough meaning to guide judgment. Provider examples and research are inputs to this decision, not text to paste wholesale into every repository.

For example, "search before creating a note" does not tell an agent to retrieve knowledge before giving advice. If informed advice is the repository's chosen behavior, its instructions need that earlier trigger. Likewise, the concrete goal and success criteria belong to the current task; standing instructions can require the agent to recover them from the request and relevant knowledge without imposing the same plan or verification checklist on every task.

Check the resulting behavior where it was uncertain: can an agent entering through the normal instructions find the relevant knowledge and use it without extra coaching? Reading files or passing a wording check does not establish that the knowledge affected the result. Use a representative fresh-session task when the uncertainty concerns startup or handoff, and keep conclusions scoped to what was exercised.

Moving instructions verbatim into a skill does not preserve their availability before a decision. Check the earliest action that needs the moved guidance, including entry through a resumed task or a user's answer rather than only the skill's main workflow. In [Firstmate's September 2026 extraction](https://github.com/kunchenguid/firstmate/pull/5872), the reported live regression check found load-timing gaps. The follow-up widened the validation-supervision trigger to cover user answers and restored several rules inline. The reusable lesson is to verify timely activation, not merely that the original text survives elsewhere.

An audit can challenge existing policy, but policy remains active until an authorized change replaces it. State genuine authorization conditions so a clear user request can satisfy them. A hazard establishes a factual concern, not permission to invent a prohibition or approval gate.

## Remove without replacing

Unnecessary coaching can simply disappear. It does not need a new reviewer, hook, checklist, or narrower copy elsewhere. Preserving an idea in ordinary knowledge is also optional when it adds nothing reusable.

Moving responsibility for a real contract is a different decision. Permissions, tools, tests, or targeted review may enforce that contract more reliably than prose. Validate such a replacement according to the consequences of failure. This is not a prerequisite for deleting generic advice that the host already supplies or the user no longer wants.

A targeted review can own a concern that only matters for particular changes. That does not make a separate reviewer or review service necessary for ordinary work. [[Context-sensitive code review]] describes how relevant evidence can support either native review or a deliberately orchestrated review system.

## Keep the intended meaning

Shorter is not automatically better. Preserve wording that expresses the user's chosen character or a consequential distinction; remove explanation that merely repeats it. Vivid wording can be useful, but memorability does not establish a reason to keep an instruction.

Revisit guidance when the user, model, host, or work changes. Ask what the instruction adds now, not just what past mistake inspired it. Use ordinary work or a focused comparison where the answer is uncertain, without turning maintenance into a required audit ceremony. [[Agent context engineering]] covers active context; [[Prompting tool-using agents]] covers the current task.
