---
name: writing-for-agents
description: Write and edit text that agents act on, such as skills, AGENTS.md and CLAUDE.md files, prompts and delegate briefs. Use when creating, rewriting or reviewing any of them, or when an agent keeps misreading one.
---

# Writing for agents

An agent treats every sentence it loads as an instruction, so each sentence should change what the agent does. Two kinds of text do that: information the agent lacks, and structure that tells it what to do first and when it is done. Explanations of things the model already knows change nothing and dilute the rest.

## Keep what the agent lacks

The agent knows its trade. It does not know the goal, Tobias's choices, or what this environment hides.

- **State the goal and the reason for each rule, in a clause.** A reason lets the agent handle cases the rule never names. "Never use ellipses" is weaker than "the output is read aloud by a text-to-speech engine, so never use ellipses."
- **Name the objective wherever the cheap path competes with it.** Agents take the smallest change that passes. A refactor skill that says structure is what makes agent output good keeps renames and dead-code deletion from passing as the job. A section like this can read like a pitch. Keep it if it names an objective the agent would otherwise trade away.
- **Keep chosen policy, local facts and gotchas** the code, config and `--help` don't reveal.
- **Cut** definitions of known concepts, restated config or `--help`, and virtues the agent already practices.
- **Settle "the model already does this" by running it.** A run with and without the sentence decides. Argument doesn't.

## Say what to do

- **Give the positive target.** "Write flowing prose paragraphs" steers better than "don't use markdown". A ban activates the thing it names. Keep a hard ban when the ban is the policy, and pair it with what to do instead: the zero-comment rule comes with where the reason goes.
- **Use normal strength.** "Use X when Y" is enough. CRITICAL and MUST make current models overtrigger. Reserve absolutes for real invariants.
- **Name the actor, the action and the artifact.** Abstract nouns give the agent nothing to do.
  - Abstract: "Ensure robust verification coverage across change surfaces."
  - Concrete: "Before landing, run the test that exercises the function you changed, and add one if none fails when you break it."
- **Write vividly.** Tobias wants memorable wording that invites judgment over lists of abstract caveats. When adapting a strong source, keep its exact words wherever they still hold.
- **Use one term per concept, and prefer words the model already knows.** "Tracer bullet" and "red test" each carry a whole practice in two words. A coined term costs a definition. Reuse the domain's word and the code's name, so the same word links the prompt, the docs and the code.

## Show the hard move

Give one worked example for the step agents get wrong, with real-looking paths and values. Examples steer more reliably than descriptions. Choose the example that shows judgment, such as six scattered problems resolving into one fix, over the trivial case the agent would get right anyway.

## Shape the document

- **Steps run in order, and each ends on a criterion the agent can check.** Demand sets thoroughness: "every caller accounted for" drives more legwork than "list the callers". A vague end, like "understanding reached", invites stopping early.
- **Match freedom to fragility.** Give an exact command for a fragile operation and criteria for a judgment call.
- **Inline what every run needs; move what only some cases need behind a pointer.** Word the pointer as the condition for reading it, and keep references one level deep from `SKILL.md`. Keep a concept's rule, reason and caveats together.
- **The description is the only always-loaded part.** It says what the skill does and when to use it, with one trigger per distinct case, leading with the words a request would use. Tobias's global skills are model-invoked, so the trigger must be precise.
- **Give each instruction one home** and name the owner instead of restating it. A skill stays self-contained: its instructional links stay inside its own directory, and it names other skills and tools it depends on.
- **Follow the `unslop` skill for sentence style.** This skill decides what the text says; `unslop` decides how each sentence reads.

## Check it

1. Read it as the agent at the moment it loads. For each sentence, ask what the agent would do differently without it. Delete whole sentences that change nothing; trimming words from them doesn't help.
2. Run the changed guidance on a representative task and read the transcript. Did the agent reach the text, follow it and finish? Missed text needs a sharper pointer or a better position before it needs more words.
3. After landing, real sessions are the test. Revise from what agents actually did, not from how the text reads.

Sources: Anthropic's [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), Matt Pocock's [writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents), and Lauren Tan's [skill authoring playbook](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md), all read 2026-11-05.
