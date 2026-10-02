# Autoresearch

An agent forms hypotheses, runs bounded experiments, and keeps or rejects changes against a trustworthy evaluator. A benchmark becomes an autoresearch engine when candidate generation, evaluation, selection, rollback, memory, and continuation work together.

## Requirements

1. Defined objective, change surface, resources, and authority.
2. Isolated candidate changes, fixed per trial.
3. A protected evaluator outside the candidate's control.
4. Controlled inputs, environment, and budget.
5. Evidence tying candidate and baseline identities to outputs, metrics, failures, cost, and duration.
6. Rules for rejection, follow-up, confirmation, promotion, and rollback.
7. Memory of prior results.
8. Stop rules.

Correctness, safety, and integrity are hard gates applied before optimization. Keep score, cost, latency, complexity, and reliability as separate numbers unless a combined scalar means something. When gains are equal, prefer the simpler candidate. Refresh baselines after any protocol change.

**Fits** when trials are cheap and repeatable, changes are isolated and reversible, feedback is automatic and hard to game, noise is measurable, and gains can be checked on held-out cases. Good targets include performance, skills and prompts, retrieval policy, orchestration, and compiler or DB config. **Weak** when feedback is subjective, delayed, sparse, unsafe, or easy to Goodhart.

## Tobias's implementation

[Skills Autoresearch](../projects.md#skills-autoresearch) owns the live policy (`program.md`), and [SWE Benchmarking](../projects.md#swe-benchmarking) is its protected evaluator. Read current policy before running anything. The transferable design:

- **Structure:** campaigns (a research direction), families (related representations), epochs (fixed comparison conditions), and immutable trials.
- **Funnel:** *scout* (one case, fresh champion/candidate pair, yields promising, not-promising, or inconclusive, and can't promote), then *screen* (paired runs on a broader set, can't promote), then *confirm* (a larger fresh replicated matrix and the only promotion evidence, with separate gates for score, duration, cost, failure rate, and validity).
- "Promote" means eligible for adoption. Installing still needs a human-directed commit and a comparison at the intended model and effort. Broader claims need held-out transfer.
- **Invalid runs:** infrastructure or protocol invalidity is evidence about the experiment, not a win or loss. A candidate that fails validation is unscored for quality but still counts toward failure-rate gates.
- **Evidence:** run artifacts are immutable. The executable portfolio is a restartable hypothesis ledger covering mechanisms, rivals, expected information gain, predictions, failure signatures, and reopening conditions. It advises; it doesn't authorize.
- **Steering:** confirm and ablate positive mechanisms, give near misses only bounded follow-up, calibrate repeated invalidity, and switch mechanism after repeated non-improvement.
- **Exhaustion:** exhausting a family or epoch justifies a new mechanism, tool, evaluator, or successor epoch. It doesn't mean the project is done. Don't reopen a closed family without new grounds.
- A frontier advance is a validated quality or Pareto gain, or better search capability. Docs, audits, and Git churn are not research gains.
