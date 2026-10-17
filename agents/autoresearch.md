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

## Fast loops first (Tobias, 2026-10-12)

This covers every experiment and every hill-climbing loop: prompts, skills, context, performance, config. Feedback speed beats rigor until an idea has shown a signal. The goal is a stream of ideas and large effects, not 5–10% gains: try many different mechanisms as cheap scouts, keep the ones that look good, and run a replicated 12-run confirm only on those.

- **Precheck the trigger without a model.** Before building anything, confirm from recorded runs or logs that the mechanism will fire on the chosen case. A checkpoint trial once ran on a case whose history never reached the trigger, so it couldn't produce a result.
- **Scout with 1–2 runs per arm.** Reuse recorded baselines when the case, model and effort match. Use the existing harness as-is. Add no isolation hardening and no review rounds. Inspect the transcripts, not just the totals.
- **Read scouts honestly.** One or two runs show whether the mechanism fired, what broke, and large effects. They can't resolve cost differences smaller than run-to-run noise, which was about ±15% on one case. Kill on mechanism failure or a clearly worse result; don't promote on a small gain.
- **Hill climbing:** each step is a scout. Keep or revert on 1–2 runs, take many cheap steps, and replicate only the candidate you'd adopt.
- **Pay for rigor only at confirm.** Use replicated arms, a hardened harness and independent review only when a scout shows an effect large enough to matter. Real-session measurement after a reversible settings change often confirms more cheaply than a benchmark.
- The slow part is harness building and review rounds, not runs. The 12-run comparison finished quickly; the checkpoint trial's six hardening reviews did not.

Subscription-backed benchmarks have no artificial dollar cap (Tobias, 2026-10-11). Label API-equivalent costs as estimates, not spend; still bound runs and respect quota. This grants no paid-API spending authority.

Correctness, safety, and integrity are hard gates applied before optimization. Keep score, cost, latency, complexity, and reliability as separate numbers unless a combined scalar means something. When gains are equal, prefer the simpler candidate. Refresh baselines after any protocol change.

**Fits** when trials are cheap and repeatable, changes are isolated and reversible, feedback is automatic and hard to game, noise is measurable, and gains can be checked on held-out cases. Good targets include performance, skills and prompts, retrieval policy, orchestration, and compiler or DB config. **Weak** when feedback is subjective, delayed, sparse, unsafe, or easy to Goodhart.

## Tobias's implementation

Skills Autoresearch owns the live policy (`program.md`), and SWE Benchmarking is its protected evaluator. Read current policy before running anything. The transferable design:

- **Structure:** campaigns (a research direction), families (related representations), epochs (fixed comparison conditions), and immutable trials.
- **Funnel:** *scout* (one case, fresh champion/candidate pair, yields promising, not-promising, or inconclusive, and can't promote), then *screen* (paired runs on a broader set, can't promote), then *confirm* (a larger fresh replicated matrix and the only promotion evidence, with separate gates for score, duration, cost, failure rate, and validity).
- "Promote" means eligible for adoption. Installing still needs a human-directed commit and a comparison at the intended model and effort. Broader claims need held-out transfer.
- **Invalid runs:** infrastructure or protocol invalidity is evidence about the experiment, not a win or loss. A candidate that fails validation is unscored for quality but still counts toward failure-rate gates.
- **Evidence:** run artifacts are immutable. The executable portfolio is a restartable hypothesis ledger covering mechanisms, rivals, expected information gain, predictions, failure signatures, and reopening conditions. It advises; it doesn't authorize.
- **Steering:** confirm and ablate positive mechanisms, give near misses only bounded follow-up, calibrate repeated invalidity, and switch mechanism after repeated non-improvement.
- **Exhaustion:** exhausting a family or epoch justifies a new mechanism, tool, evaluator, or successor epoch. It doesn't mean the project is done. Don't reopen a closed family without new grounds.
- A frontier advance is a validated quality or Pareto gain, or better search capability. Docs, audits, and Git churn are not research gains.
