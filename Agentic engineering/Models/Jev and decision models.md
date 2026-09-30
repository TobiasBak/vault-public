# Jev and decision models

Checked 2026-09-20 against TypeSafe's documentation and launch material. Jev is a text-based decision model, not a general forecasting engine or a replacement for a coding agent.

## What changes

Software sends a shared state and explicit questions. Jev returns bounded answers instead of generating prose. Independent questions run together against the same state; one answer does not become another question's context. Dependent decisions still need code and another call. This makes classification, candidate selection, and semantic checks its natural jobs. [Introduction](https://docs.typesafe.ai/introduction)

| Type | Returned value | Example |
| --- | --- | --- |
| Choice | One supplied option, probabilities over all options, and confidence | Which of these customer records matches the request? |
| Score | A probability-weighted position on an ordered rubric, its distribution, and confidence | How clearly does the source support this interpretation? |
| Noul | Probability that a yes/no proposition is true | Does the email explicitly request cancellation? |

Choice supports up to 255 options. Include an insufficient-evidence or no-match option when appropriate. Extra questions share state processing but still add input tokens. Score is a rubric judgment, not arbitrary numeric regression. [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score), [Noul](https://docs.typesafe.ai/primitives/noul)

TypeSafe calls this family System One and its training method Reinforcement Learning for Calibrated Decisions, or RLCD. The aim is useful probabilities rather than preferred prose. Calibration means that, across comparable predictions assigned 80%, the event occurs roughly 80% of the time. It does not certify an individual answer. The public primer describes a post-training path from pretrained language models; the practical distinction is the decision interface and training objective, not proof that language-model foundations have been replaced. [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer)

## What the claims establish

TypeSafe launched Jev on 2026-09-15 and claims a new architecture and parallel sampler. Its headline 193.6× speed and 444.6× cost gains come from its own workflow evaluations, which it describes as the high end of expected gains. Staff built the workflows; averaged Astra and Fable outputs supply reference answers. The comparison wrapper asks other models for probability-bearing structured answers, which adds work. These are useful demonstrations, not a measured improvement for Tobias's workloads.

The launch's zero-hallucination figure is a schema guarantee, explicitly not an empirical count of correct answers. Jev can choose a valid option for the wrong reason. Structured-output LLMs also constrain answer shapes; the interesting claim is cheaper, faster, better-calibrated judgments. [Launch and benchmark caveats](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

Choice and Score confidence summarize the shape of their probability distribution. Confidence is neither a second model checking the answer nor automatically the probability of correctness. Noul has no separate confidence field. Thresholds need labeled examples from the actual workload. Good overall calibration can still hide poor behavior for one Customer, language, or document type. [Confidence](https://docs.typesafe.ai/confidence)

Calibration alone does not establish useful discrimination. A model that always predicts a population's base rate can be calibrated while distinguishing no individual cases. The relevant engineering result is fewer consequential mistakes or more safely automated cases at the same error rate.

## Current operating limits

The documented version is `jev-1.13.0`. Direct pricing is $0.042 per million input tokens with free outputs. A hypothetical request billed for 10,000 input tokens costs $0.00042, or $420 for a million such requests, excluding surrounding processing. Context limits are 64k tokens overall and 32k for state plus the longest question. Input is text only. English is the strongest language. Customer-specific fine-tuning is not offered; customization uses supplied context and question definitions. Pin versions when comparing behavior or tuning thresholds. [Models and pricing](https://docs.typesafe.ai/models)

Vercel also exposes Jev through AI Gateway's experimental evaluation API. Its availability is separate from TypeSafe's direct-access waitlist. [Gateway release](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway)

Jev 1.13 struggles with exact arithmetic, counting, date comparisons, multi-step indirection, and irrelevant context. It cannot inspect drawings directly. Adversarial text can steer its answers. Separately asked questions need not obey logical identities; probabilities for a proposition and its negation can fail to sum to one. Parallel evaluation does not imply statistically independent errors. Keep arithmetic, authorization, and invariants in code. [Documented limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

## Application fit

These are fit judgments, not local benchmark results.

Document-processing workflows have a stronger fit than numeric market prediction. Their text-heavy work includes interpreting requests and checking extracted fields against source material. Jev can select or judge supplied candidates, but open-ended extraction, drawing interpretation, and exception investigation still need other tools or models. TypeSafe demonstrates a small-model extraction cascade where Jev checks individual fields and suspicious results escalate to a reasoning model. That supports evaluating a verifier role, not replacing extraction wholesale. [Extraction cascade](https://docs.typesafe.ai/cookbooks/sde_cascade)

[[Outcome-based learning for adaptive systems]] supplies something Jev cannot create: scoped human-accepted outcomes. Those can reveal whether its judgments predict actual corrections. Feedback does not automatically retrain Jev. It can improve supplied examples, question definitions, routing thresholds, or a separate trained model. The existing distinction between accepted outcomes and universal truth still applies.

TypeSafe's feature-discovery example combines an LLM proposing questions, Jev turning text into numeric features, and CatBoost learning from labels. This is a concrete connection to [[Autoresearch]] and [[Outcome-based learning for adaptive systems]]. The task-specific predictor and Jev remain separate models. [Feature-discovery cookbook](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery)

For [[Projects#Poly Executor|Poly Executor and poly-llm]], returning probabilities does not establish an advantage over models trained on market sequences. Jev's documented strengths concern language judgments; the current offline models consume numeric market history.

For coding-agent work, bounded relevance checks and routing are plausible supporting roles. Jev cannot replace repository investigation, code generation, or behavioral tests. A cheap model judgment must not become the ground truth used to promote changes.

[[AI lead developer workflow strategy]] records Tobias's developer-focused role and the untested candidates for using Jev in automated testing. Agent-led exploration is the proposed starting point; Jev is a possible supporting tool, not the strategy.

The broader implication agrees with [[AI-era software durability]]: falling judgment cost increases the value of reliable integrations, domain rules, accepted-outcome history, and measured execution. It does not justify replacing settled deterministic behavior with model calls.
