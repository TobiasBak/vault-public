# Jev (TypeSafe decision model)

Checked 2026-09-20. Jev is a text-only decision model: software sends a shared state plus explicit questions and gets back bounded, probability-bearing answers instead of prose. It is suited to classification, candidate selection, and semantic checks. It doesn't replace a coding agent or general forecasting. ([docs](https://docs.typesafe.ai/introduction))

- **Primitives:**
  - **Choice:** one of up to 255 options, with probabilities and confidence. Include a no-match option.
  - **Score:** a position on an ordered rubric, not numeric regression.
  - **Noul:** the probability a yes/no proposition is true.
- **Execution:** independent questions run in parallel against the same state; dependent decisions need code and another call.
- **Version and price:** `jev-1.13.0`, $0.042 per million input tokens, outputs free. 64k context, of which 32k covers state plus the longest question. English is strongest. No fine-tuning. Also available via Vercel AI Gateway. Pin the version when tuning thresholds.
- **Weak at:** arithmetic, counting, dates, multi-step indirection, irrelevant context, drawings, and adversarial text. A proposition's probability and its negation's needn't sum to 1. ([limits](https://docs.typesafe.ai/model-jaggedness/jev-1.13)) Keep arithmetic, authorization, and invariants in code.
- **Calibration is not correctness:** 80% predictions come true about 80% of the time overall. A model that always predicts the base rate is calibrated and useless. Confidence describes the shape of the distribution, not a verification. Set thresholds from labeled examples of your own workload.
- **Launch claims:** 193.6× speed and 444.6× cost come from TypeSafe's own workflows, the self-described high end, against Astra and Fable reference answers. "Zero hallucination" is a schema guarantee, not an accuracy figure.

## Fit

- **Strong:** document workflows such as interpreting requests and checking extracted fields against the source. TypeSafe's [cascade](https://docs.typesafe.ai/cookbooks/sde_cascade) has Jev verify each field and escalate suspicious ones to a reasoning model.
- **Feature discovery:** TypeSafe's [example](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery) has an LLM propose questions, Jev convert text to features, and CatBoost learn from them. That links to [autoresearch](autoresearch.md) and [outcome-based learning](learning-from-feedback.md#outcome-based-learning), whose accepted outcomes can test whether Jev's judgments predict real corrections.
- **Weak:** Poly Executor's numeric market models. Returning probabilities isn't an edge over sequence models.
- **Coding agents:** plausible for relevance checks and routing. Never use it as ground truth for promoting changes.
