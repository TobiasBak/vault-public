# AI in the product

Scope: model calls inside products: LLM features, agents built into the product, classification, embeddings. Agent authority and prompt injection are [S10](access.md#s10-agents-in-the-product); provider isolation is [P9](dependencies.md#p9-services-behind-one-module).

Principles:
- Prompts, models and tools are code and ship through releases.
- Evals gate AI changes the way black-box cases gate code.
- Model output is untrusted input.

## Changing AI features

### M1 Prompts and models are code

Prompts, model IDs, parameters and tool definitions live in git and ship with the release ([R1](release.md#r1-everything-goes-through-git), [R2](release.md#r2-one-version-known-running-state)). A prompt or model change goes through staged rollout and per-version comparison. Nobody edits prompts in a provider dashboard.

Reason: a prompt change breaks a feature as easily as a code change.

Enforcement: model calls take prompts and model IDs only from typed definitions in the repo; provider dashboards hold no production prompts.

### M2 Evals gate changes

Each AI feature has an eval set of representative inputs with graded expected outcomes. It runs in CI on every prompt, model or tool change; a score below the last release blocks the merge. Deterministic graders first, model-graded rubrics only where needed. Incidents add eval cases ([O15](observability.md#o15-incidents-close-with-a-check)) with personal values removed.

Reason: without evals, nobody knows whether a change made the feature better or worse.

Enforcement: the eval run is a CI gate on changes to AI definitions.

### M3 Pinned models

Model IDs are exact snapshots, never aliases like `-latest`. Provider deprecations are tracked, and moving to a new model is an M2-gated change. When the provider is down, the feature switches to a fallback model that passes the same evals, or turns off with a clear error.

Reason: an alias lets the provider change the product without a release.

Enforcement: a static check rejects alias model IDs; a black-box case with the provider down gets the fallback or the clear error.

## Running AI features

### M4 Structured output

Model output that drives code is decoded into strict typed structs through schema-constrained output. Invalid output is a typed error, retried once, then handled. Code never parses prose.

Reason: tolerate versions, never ambiguity; a model's answer is untrusted input.

Enforcement: model calls that feed code return typed results; a black-box case with malformed recorded output gets the typed error.

### M5 Cost and latency budgets

Each AI feature has a per-request cost and latency budget, and each company a spending limit. Every model call records tokens, cost and latency in its [wide event](observability.md#o1-wide-events). Exceeding a budget alerts; exceeding a company's limit stops its AI calls with a clear error.

Reason: one customer's loop becomes the bill.

Enforcement: the provider module checks the company's limit before each call and emits the fields; budgets are alert definitions in git ([O4](observability.md#o4-telemetry-is-a-contract)).

### M6 Customer data and providers

Providers are used only under a data processing agreement, with no training on our data and zero data retention where offered, processing in the EU where available. Personal data is sent only when the feature needs it. A public sub-processor list names which provider processes what.

Reason: EU enterprise customers require it, and GDPR applies to everything sent.

Enforcement: P9's module is the only path to a provider; the sub-processor list is generated from configured providers.

### M7 Labeling

Users are told when content or a reply is AI-generated. Customer-affecting actions still need confirmation under S10.

Reason: EU AI Act transparency duties apply from August 2026, and users judge AI output differently.

Enforcement: AI-generated content carries a typed origin that the UI renders as a label.

### M8 Stored inputs and outputs

Model inputs and outputs are stored with personal values redacted, kept about 30 days, separate from telemetry, and readable only through [support access](access.md#s11-support-access).

Reason: debugging an AI feature needs what the model saw and said; redaction and short retention keep it safe and erasure simple.

Enforcement: the provider module redacts before storing; the store's retention is config in git.

### M9 Recorded responses in tests

Black-box cases replace model calls with recorded responses. Only evals call real models.

Reason: tests stay deterministic and free; evals measure the model.

Enforcement: the test configuration has no provider credentials.
