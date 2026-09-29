# Autoresearch

Autoresearch is an indefinitely continuing autonomous ML-research loop at project level. The project mission may continue as long as useful legal moves remain. Its work is decomposed into bounded, immutable experiments and evidence epochs so that continuation is controlled rather than an unbounded mutable run. A project contract defines the change surface, trustworthy evaluator, resource limits, and consequential boundaries; the agent forms hypotheses, runs trials, records evidence, keeps or rejects candidates, rolls back safely, and chooses the next bounded unit.

```text
project mission -> campaign -> representation family -> evidence epoch -> trial
                  bounded       bounded              bounded           immutable
```

The point is not autonomous activity by itself. It is repeated, comparable, evidence-backed improvement with a durable basis for the next pivot.

## Required structure

A complete loop has:

1. a project research policy defining the mission, scope, objective, constraints, and hypothesis choice;
2. bounded campaigns, representation families, evidence epochs, and trials within that mission;
3. an intervention surface that is immutable for each trial and epoch;
4. a protected evaluator outside candidate control;
5. controlled inputs, environment, budget, and comparison conditions;
6. evidence linking candidate identity, baseline, outputs, metrics, failures, cost, and duration;
7. a selection policy for rejection, follow-up, confirmation, and promotion;
8. safe rollback to the current champion;
9. continuation from prior results rather than repeated one-shot guessing;
10. explicit gates for activating successors, reopening closed families, and crossing any consequential boundary reserved to a human by the project contract.

Hard correctness, safety, and integrity gates should precede optimization. Keep important tradeoffs visible instead of hiding score, cost, latency, complexity, and reliability in one scalar unless that scalar has a defensible meaning.

## Fit boundary

Autoresearch fits when trials are cheap enough to repeat, candidate changes are isolated and reversible, feedback is automatic and difficult to game, noise can be measured, and gains can be checked on held-out or broader conditions. It is weak when feedback is subjective, delayed, sparse, unsafe to obtain, or easy to Goodhart.

Useful targets include code performance, agent skills and prompts, context or retrieval policy, orchestration, compiler or database configuration, and test generation. Correctness tests remain hard gates when optimizing performance. Human judgment is required for the objective, surprising winners, or evaluator changes only when the project contract reserves those consequential boundaries; it is not a universal gate on ordinary transitions. The agent may continue through authorized trials, confirmations, pivots, and successor activation.

## Scout, screen, confirm

Tobias's implemented local loop uses a three-stage funnel:

- **Scout:** one development case with a fresh champion/candidate pair gives a cheap `promising`, `not-promising`, or `inconclusive` signal. It cannot promote.
- **Screen:** fresh paired runs across a broader set filter candidates under the real evaluator and integrity checks. Screening still cannot establish promotion.
- **Confirm:** a larger fresh replicated matrix is the only promotion evidence. Score, duration, cost, failure rate, and validity retain separate gates.

Fresh champion evidence avoids comparison across changed conditions. Replication limits promotion from one lucky trajectory. Held-out confirmation reduces selection overfit. Infrastructure or protocol invalidity is evidence about the experiment rather than candidate quality and must not be scored as a win or loss. A candidate execution that fails validation remains unscored for quality, but it still contributes to failure-rate gates and may justify rejection.

[[Projects#SWE Benchmarking|SWE Benchmarking]] supplies the controlled repository-task evaluator. [[Projects#Skills Autoresearch|Skills Autoresearch]] owns the candidate-generation, paired scheduling, evidence, selection, and continuation loop for Agent Skills. Keep the benchmark protected from the artifact being optimized.

## Evidence and executable portfolio

Immutable run artifacts are the scientific record: exact candidate and champion identities, environment, outputs, validation, metrics, hashes, and decision provenance. Never rewrite them to match later interpretation.

A separate executable portfolio is the control plane for the next action. It records each hypothesis's mechanism and rivals, expected information gain, cost, novelty, predicted outcomes and failure signatures, reopening condition, and successor proposals. Record positive, negative, near-miss, inconclusive, and invalid attempts. Persist immutable evidence, the current Pareto frontier, closed-family signatures, pivot rationale, successor candidates, activation gates, and reopening conditions. The portfolio may be revised as strategy changes, but it points to immutable evidence rather than replacing it.

Use repeated signatures to change search direction: confirm and ablate a positive mechanism; allow only bounded follow-up to a near miss; calibrate repeated invalidity; switch mechanism after repeated non-improvement; and require an explicit rationale when overriding the normal escalation rule.

## Exhaustion and frontier lifecycle

The project mission may continue indefinitely, while each campaign, representation family, and evidence epoch has a bounded scope, budget, and evidence plan. Exhaustion of a family or epoch is a pivot signal, not fleet termination. It should trigger architecture search, construction of a prerequisite, tool, kernel, or evaluator, a broadened hypothesis class within the mission, or activation of a safe successor epoch. A successor requires its recorded activation gates; a closed family can reopen only under its recorded reopening conditions.

An accepted frontier advance is a validated Pareto or model-quality gain, or a validated advance in search capability such as a better legal evaluator, kernel, tool, or prerequisite that expands reliable progress. Documentation, audits, and mere Git changes are not frontier advances unless they produce such validated capability or model evidence. Keep score, cost, latency, complexity, reliability, and search capability visible rather than hiding them in one scalar.

`exhausted` is a fleet status only when no useful legal project-level move remains or permanent external impossibility prevents continuation. It never means that a global optimum has been established. Record the status rationale and preserve the current frontier, closed-family signatures, successor candidates, activation gates, pivot rationale, and reopening conditions. Human involvement is needed only at consequential boundaries reserved by the project contract, not as a universal transition gate.

Protect evaluator material, isolate side effects, prohibit credentials and production writes, refresh baselines after protocol changes, and prefer a simpler candidate when gains are otherwise equivalent. A benchmark becomes an autoresearch engine only when candidate generation, evidence, selection, rollback, memory, and continuation all operate as one controlled loop.
