# Instructions and prompts

Describe the destination, not the steps. Capable models plan well; instructions should add only what the model, host, tools, and task don't already supply.

## What earns a place in AGENTS.md

- **Chosen collaboration:** how Tobias wants to work, his taste and priorities. Needs no failure justification.
- **Local facts:** authority boundaries, external contracts, and hazards the agent can't discover in time.
- **Corrective coaching:** a current, observed gap. Failures of older models or imaginable mistakes don't count.

There's no mandatory inventory of commit rules, test reminders, or engineering maxims. Delete unneeded coaching outright; don't replace it with hooks, reviewers, or checklists. Keep chosen character and consequential distinctions, and cut their repeated explanation. Revisit when the model, host, or work changes.

| Knowledge | Home |
|---|---|
| Task goal, scope, success criteria | The request and working state |
| Behavior across repos | Global instructions |
| Repo rules, authority boundaries, retrieval triggers | Repo or nested `AGENTS.md` |
| Rationale, domain knowledge, findings | Code, vault notes |
| Reusable method that needs judgment | Narrowly triggered skill |
| Mechanical invariant or repeatable operation | Types, checks, tools |

- **Global instructions stand alone (Tobias, 2026-10-10).** They never mention the vault: Tobias starts agents in the vault repo when its knowledge matters, so a preference every agent needs belongs inline. They guide by model and effort ("Haiku 5.5 at `high`"), not by naming tools or call payloads.
- **Retrieval must be triggered.** "Search before creating a note" does not cause retrieval before giving advice. Say when to retrieve.
- **Skills can load too late.** Moving rules into a skill risks them loading after they're needed. Check the earliest action that needs the rule, including resumed tasks and replies to user answers. Firstmate's [extraction](https://github.com/kunchenguid/firstmate/pull/5872) regressed this way and restored rules inline.
- **Reading isn't using.** File reads and wording checks don't show that an agent uses knowledge. Run a representative fresh-session task. Example (2026-10-02): cutting the global instruction file from 1,079 to ~430 words (vault pointers replacing copied preferences; the pointers were removed 2026-10-10) kept 6/6 vault-specific answers correct in fresh Claude Code and Codex sessions, at equal or lower cost. Harness gotcha: `claude -p` and `codex exec` read stdin, so in a shell loop they swallow the rest of the task file, expected answers included. Redirect `< /dev/null`.
- **Phrase authorization as a condition** ("invoke the live workflow only when Tobias asks"). A clear request satisfies it, with no reconfirmation. Reserve "never" for constraints Tobias genuinely can't override.

## Task contract

Supply these only where the request and repository leave a consequential gap:

- **Outcome:** the user-visible result.
- **Success criteria:** what must be true before you're done.
- **Constraints:** permissions, safety, business rules, side-effect limits.
- **Tools:** relevant capabilities and lookups that must come first.
- **Output:** required content, evidence, validation.
- **Stop rules:** when to retry, fall back, ask, escalate, or finish.

Reserve absolutes for invariants and give criteria for judgment calls. If a requested mechanism conflicts with boundaries, explain the conflict and recommend the coherent direction.

## Execution

- Parallelize independent reads and checks; serialize dependent work and shared mutations. Keep working while a tool or question is pending, but block dependent actions on it.
- Empty or suspiciously narrow results don't prove absence. Try a few meaningful alternative searches.
- Long-running tools should return short progress, actionable failures, and a final result naming inputs and checks. Keep logs out of context and link them. Hold one process handle and use native waits, never duplicate polling.
- Under a systemd service, use `setsid --wait` when wrapping a command. A service process can already lead its process group: plain `setsid` forks and returns success before the child finishes, then systemd can kill the child. Require actual validation output as well as the supervisor's exit code; an empty log and implausibly short run are not a pass.
- Missing evidence is not a negative. Separate fact from inference and surface conflicting sources.
- Choose verification by artifact and risk: focused tests, types, build, smoke test, real use, rendered inspection. Reuse passing evidence while inputs are unchanged, and rerun after invalidating changes.
- Judge cost per successful task, counting retries and delegated work, not tool-call counts.

## Promote settled reasoning into machinery

Tools supply evidence, execution, validation, state, and permissions, not scripted reasoning. Spend model reasoning on uncertainty and exceptions. When a recurring pattern becomes mechanically detectable, give it to the narrowest deterministic owner: code for transformations, generators for operations, schemas for structure, and tests, lint, hooks, or CI for invariants. That requires real recurrence, reliable detection, acceptable error costs, and an escape hatch for legitimate exceptions. Then delete the prompt text it replaced.
