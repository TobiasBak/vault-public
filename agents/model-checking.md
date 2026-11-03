# Model checking agent-built state machines

Model-check a component when several state machines run at once and timers, focus loss, asynchronous loads or lost contexts can fire in any order. Example tests cover the orders someone thought of; a model checker such as TLA+'s TLC explores every order and returns a counterexample trace for each broken rule. Agents make writing the spec cheap, so its cost no longer rules out formal methods for this class of bug.

## Evidence: tibo.dog

Lauren Tan built tibo.dog, a browser survivors-like, with agents (Grok bot and Cursor) in four days and about 1,150 PRs ([post](https://x.com/poteto/status/2117043478140276847), 2026-11-01). She kept one formal-verification skill per major system: story, cutscenes and game systems. Her published story-mode model runs five parts at once (story, lines, pause, level-up offer, knock-down) under 17 rules. TLC found 11 bugs, fixed in PRs #929 to #1191, among them:

- The 8-second level-up auto-pick fired while the player had looked away, and the run played on.
- After a reroll, the auto-pick pointed at a card from the old hand.
- The pause menu opened over a scripted line, and a laugh effect kept shaking the screen under the focus pause.
- A character got up behind the loading screen while WebGL was lost.

Each is an interleaving: a timer, a focus or WebGL event, or a load racing another machine. None needs unusual input, and none appears in a test that drives one machine at a time.

## Method

- Model each machine and each external event source (timers, focus, visibility, context loss, load completion, reset) as an independent actor. State the rules as invariants, such as "no auto-pick while away" or "no line on screen after reset".
- Keep one spec and one skill per system, so the agent changing that system reruns its checker. The skill says how to run TLC and read a counterexample.
- Turn each counterexample into a fix and a deterministic test that replays that event order against the real code. The model checks the design; only the test checks the code. [Deterministic simulation](../software/deterministic-simulation.md) makes such replays exact.
- The model is a second implementation and drifts. Change it in the same commit as the machine, or generate it from the code's transition table. Tan's post doesn't say how she kept them in sync.
- Render the model as a diagram with violating states marked. Tan's diagrams let a human review the design and every bug found without reading TLA+, the goal [system specs](../skills/system-specs/SKILL.md) serve for other boundaries.

Other verification routes: [testing with agents](testing-with-agents.md).
