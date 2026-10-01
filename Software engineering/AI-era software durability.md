# AI-era software durability

Market and labour evidence checked 2026-07-30; provider integration checked 2026-09-26. Products and capabilities change faster than the distinctions below.

AI makes code production and software operation cheaper. Reliable state, execution, accountability, and domain knowledge remain valuable.

The labour evidence supports task reorganization more than wholesale replacement. The ILO's June 2026 review found limited large-scale displacement, uneven productivity gains, and weaker opportunities for younger workers ([ILO review](https://www.ilo.org/publications/impact-genai-jobs-productivity-and-work-organization-review-empirical)). US software-development postings rebounded but remained 27.5% below pre-pandemic levels in June 2026; senior and AI-related roles drove most of the recovery ([Indeed Hiring Lab](https://www.hiringlab.org/2026/07/08/ai-and-job-postings-from-destruction-to-creation/)).

Expect **fewer people needed for a fixed amount of routine output**, not necessarily fewer jobs overall. Lower cost can create demand. Workers who direct and verify agents gain leverage, while routine digital work and the junior-development pathway face more pressure.

## What software is exposed

The vulnerable product is a replaceable interaction layer:

- a thin interface over commodity data or model capability;
- generic generation, search, summarization, or agent-loop wrappers;
- shallow CRUD and workflow products whose useful behavior can be recovered from visible screens, exports, or ordinary APIs;
- per-seat tools whose revenue depends on many humans manually navigating the product;
- products with no authoritative state, difficult integration, proprietary outcome loop, network, distribution advantage, or accountability boundary.

The 2026 software selloff reflects investor expectations, not proof of enterprise replacement. The S&P North American Technology Software Index fell more than 20% through 6 February, yet analysts found little evidence of companies replacing major SaaS vendors with generated software. Slower mature-SaaS growth, per-seat exposure, and stock-based compensation mattered alongside AI fears ([S&P Global](https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/2/software-sell-off-may-be-overdone-yet-exposes-deeper-concerns-97965687)).

## What remains durable

Software remains valuable when it owns something the model cannot regenerate from a prompt:

- **Authoritative state and transactions:** ledgers, orders, identity, entitlements, durable history, and reconciliation.
- **Operational guarantees:** permissions, validation, idempotency, audit, security, rollback, and regulatory or professional signoff.
- **Difficult connectivity:** maintained integrations, external contracts, deployment environments, and physical or organizational boundaries.
- **Proprietary evidence and feedback:** real inputs, accepted outcomes, evaluator history, and the ability to improve from deployment without confusing user edits with universal truth. See [[Outcome-based learning for adaptive systems]].
- **Embedded domain process:** exception handling, approvals, institutional rules, and workflows that co-evolved with the organization.
- **Networks and collaboration:** products whose value comes from other participants, shared history, distribution, or a marketplace rather than the interface alone.
- **Agent tools:** compilers, tests, schemas, APIs, sandboxes, observability, CI, and other machinery that gives agents trustworthy feedback and constrained action.

A system of record is not automatically durable. AI makes its common data model and happy paths cheaper to rebuild. Exceptions, integrations, authority, and accountability supply the harder-to-replace value. The interface may shrink while agents increasingly operate the product through APIs.

## Likely architecture as intelligence becomes cheap

Use code for settled behavior and agents for semantic judgment. Code remains cheaper and more deterministic per execution. Agent reasoning fits ambiguity, frequent change, and cases that would otherwise accumulate brittle branches.

```text
unstructured input
        |
agent interpretation
        |
typed intent or plan
        |
deterministic validation and execution
        |
authoritative result
        |
outcome capture and comparison
        |
candidate improvements to examples, knowledge, configuration, or code
```

The agent should normally produce a typed plan rather than improvise low-level external writes. Deterministic machinery owns schemas, permissions, validation, idempotency, transactions, retries, audit, and execution. Agents own interpretation, uncertain choices, exceptions, investigation, and proposals for improvement. This keeps reasoning flexible without making production behavior opaque or unauditable.

A likely application therefore consists of:

- domain APIs and CLI tools that expose reliable capabilities;
- typed schemas for intent, plans, results, and errors;
- hard policies and validators for operational invariants;
- Markdown knowledge, examples, and structured configuration for behavior that remains contextual;
- traces, accepted outcomes, and evaluations that reveal whether the system is improving;
- a thin runtime that triggers agents, supplies context, records evidence, and enforces authority;
- a smaller interface focused on review, exceptions, approval, and observability rather than manually walking every workflow.

Keep isolated corrections as examples, recurring local patterns as scoped knowledge or configuration, and transferable patterns as shared guidance. Put stable, mechanically detectable behavior in code, and exclude forbidden states through schemas, permissions, or validation. Not every lesson belongs in code, but agents should not rediscover settled rules on every run. See [[Outcome-based learning for adaptive systems]] and [[Prompting tool-using agents#Promote settled cognition into machinery]].

As model cost falls, products can afford interpretation, critique, replay, and improvement for each case. Their differentiation shifts away from code volume and handcrafted workflow screens toward domain capabilities, difficult integrations, proprietary outcome history, evaluation quality, and safe authority over real systems.

## Provider gravity in coding-agent harnesses

Model providers can evolve models, tools, and the agent loop together, giving them a structural advantage in the generic coding harness. OpenAI's Agents API supplies a managed Codex harness with session state, tools, context management, and continuation. Anthropic's Agent SDK exposes Claude Code's tools, loop, and context management inside an application. Integrators can inherit those systems instead of recreating them. Provider integration guidance checked 2026-09-26. [OpenAI Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview), [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)

This makes an independent harness that competes mainly through its prompt, generic tool loop, compaction, or task decomposition fragile:

- the provider can train directly against its own loop and see failure modes unavailable to outsiders;
- the provider can update model and harness together;
- model improvements invalidate scaffolding assumptions;
- provider SDKs let other products inherit the native loop without reproducing it;
- a universal cross-model loop can become a lowest-common-denominator interface when models were optimized for different tools and interaction protocols.

Harness engineering does not disappear. Anthropic has shown that domain-specific harness work can improve results beyond the baseline, while warning that every added component encodes an assumption that can quickly become stale as the model improves ([harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)). The defensible strategy is to keep the model-facing loop thin, measured, and replaceable.

## Architecture consequence

Standardize **above** provider-native harnesses rather than replacing them:

```text
shared workspace, product workflow, policy, evaluation, and durable state
                               |
             provider-native Codex / Claude / other agent
                               |
       repository, sandbox, tools, tests, CI, and external systems
```

An independent coding product can remain valuable by owning:

- the human collaboration and multi-session workspace;
- repository and organization-specific context;
- local and cloud execution, credentials, permissions, and policy;
- review, evaluation, replay, deployment gates, and outcome history;
- issue, CI, production, and business-system integration;
- provider selection and migration where this produces real leverage.

Multi-provider support alone is easy to copy and may sacrifice native capability. Integrate native harnesses behind a stable product-level task and evidence model. Tobias confirmed this direction for [[Projects#T3 Code|T3 Code]] on 2026-07-30: own the collaborative workspace and controls around provider-native agents rather than recreate a generic coding loop.

The general product test is: **if the provider model and harness became dramatically better and cheaper tomorrow, would this product become more valuable or disappear?** Durable tools gain leverage from better intelligence because they own state, action, feedback, or accountability. Thin wrappers lose their reason to exist.
