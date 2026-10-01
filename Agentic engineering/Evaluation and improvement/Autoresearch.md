# Autoresearch

Autoresearch uses an agent to form hypotheses, run bounded experiments, compare results, and keep or reject changes against a trustworthy evaluator. A project contract defines the objective, change surface, resources, and authority. The aim is repeated, comparable improvement, not autonomous activity for its own sake.

## Core loop

A useful loop needs:

1. a defined objective, scope, and constraints;
2. isolated candidate changes, fixed for each trial;
3. a protected evaluator outside candidate control;
4. controlled inputs, environment, budget, and comparison conditions;
5. evidence linking candidate and baseline identities to outputs, metrics, failures, cost, and duration;
6. rules for rejection, follow-up, confirmation, promotion, and rollback;
7. memory of prior results to guide the next experiment;
8. clear stop rules and consequential boundaries reserved to a human.

Hard correctness, safety, and integrity gates should precede optimization. Keep important tradeoffs visible instead of hiding score, cost, latency, complexity, and reliability in one scalar unless that scalar has a defensible meaning.

## Fit boundary

Autoresearch fits when trials are cheap enough to repeat, candidate changes are isolated and reversible, feedback is automatic and difficult to game, noise can be measured, and gains can be checked on held-out or broader conditions. It is weak when feedback is subjective, delayed, sparse, unsafe to obtain, or easy to Goodhart.

Useful targets include code performance, agent skills and prompts, context or retrieval policy, orchestration, compiler or database configuration, and test generation. Correctness remains a hard gate when optimizing performance. The project contract determines which objectives, surprising winners, or evaluator changes need human judgment. Ordinary authorized trials and pivots need no extra approval.

## Local campaign structure

Tobias's local research system uses campaigns, representation families, evidence epochs, and immutable trials. A campaign completes a research direction through its required evidence stages; a family groups related representations; an epoch fixes comparison conditions. These are local control choices, not requirements for every autoresearch loop.

[[Projects#Skills Autoresearch|Skills Autoresearch]] owns the active research policy in `program.md`, candidate generation, scheduling, evidence, selection, and continuation. [[Projects#SWE Benchmarking|SWE Benchmarking]] supplies its protected repository-task evaluator. Read current policy before running campaigns; this note preserves the transferable design, not every controller rule.

## Scout, screen, confirm

Tobias's implemented local loop uses a three-stage funnel:

- **Scout:** one development case with a fresh champion/candidate pair gives a cheap `promising`, `not-promising`, or `inconclusive` signal. It cannot promote.
- **Screen:** fresh paired runs across a broader set filter candidates under the real evaluator and integrity checks. Screening still cannot establish promotion.
- **Confirm:** a larger fresh replicated matrix is the only promotion evidence. Score, duration, cost, failure rate, and validity retain separate gates.

In this system, `promote` means local adoption eligibility, not automatic installation. Installation needs a separate human-directed adoption commit and comparison on the intended model and effort settings. Broader claims need held-out transfer evidence from cases that did not shape the candidate.

Fresh champion evidence avoids comparison across changed conditions. Replication limits promotion from one lucky trajectory. Held-out confirmation reduces selection overfit. Infrastructure or protocol invalidity is evidence about the experiment rather than candidate quality and must not be scored as a win or loss. A candidate execution that fails validation remains unscored for quality, but it still contributes to failure-rate gates and may justify rejection.

## Evidence and executable portfolio

Immutable run artifacts preserve exact candidate and champion identities, environment, outputs, validation, metrics, hashes, and decision provenance. Never rewrite them to match later interpretation. Tracked research notes preserve conclusions and rationale with routes to those artifacts.

The local executable portfolio is a restartable hypothesis and result ledger, not a worker-assignment system or promotion evidence. It records mechanisms, rivals, expected information gain, cost, novelty, predicted outcomes, failure signatures, reopening conditions, and successors. Its ranking advises campaign selection; it does not grant execution authority. Record positive, negative, near-miss, inconclusive, and invalid attempts, and revise strategy without replacing the immutable evidence.

Use repeated signatures to change search direction: confirm and ablate a positive mechanism; allow only bounded follow-up to a near miss; calibrate repeated invalidity; switch mechanism after repeated non-improvement; and require an explicit rationale when overriding the normal escalation rule.

## Exhaustion and frontier lifecycle

The local project mission can continue while useful authorized work remains. Campaigns and experiments still have bounded scope, resources, and scientific stop rules. Exhausting a family or epoch can justify a new mechanism, architecture, prerequisite, tool, evaluator, or safe successor epoch. It does not prove that the project has no useful work left. Respect successor gates and recorded reopening conditions rather than retrying a closed family without new grounds.

An accepted frontier advance is a validated quality or Pareto gain, or a validated improvement in search capability such as a better permitted evaluator, kernel, tool, or prerequisite. Documentation, audits, and Git changes alone are not research gains. Keep score, cost, latency, complexity, reliability, and search capability visible.

In current local policy, `exhausted` can terminate a campaign whose declared protocol or search space is exhausted. It is not a claim of global optimality or an instruction to stop the whole research fleet. Record the outcome, rationale, frontier, closed-family signatures, and useful successors so the next campaign starts from evidence rather than repeating the same search. Repository policy owns exact terminal statuses and continuation rules.

Protect evaluator material, isolate research side effects from credentials and production writes, refresh baselines after protocol changes, and prefer the simpler candidate when gains are otherwise equivalent. A benchmark becomes an autoresearch engine when candidate generation, evaluation, selection, rollback, memory, and continuation work together.
