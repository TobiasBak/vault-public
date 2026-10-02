# AI-era software durability

AI makes producing and operating code cheap. Value shifts to what a model can't regenerate from a prompt: authoritative state, execution, accountability, domain process, and feedback. Product test: **if the provider's model and harness became dramatically better and cheaper tomorrow, would this product gain value or disappear?**

## Labour and market (checked 2026-07-30)

Expect fewer people per unit of routine output, not necessarily fewer jobs. The ILO's June 2026 [review](https://www.ilo.org/publications/impact-genai-jobs-productivity-and-work-organization-review-empirical) found limited displacement, uneven productivity gains, and weaker prospects for young workers. US software postings were 27.5% below pre-pandemic levels in June 2026, with the recovery led by senior and AI roles ([Indeed](https://www.hiringlab.org/2026/07/08/ai-and-job-postings-from-destruction-to-creation/)). The early-2026 SaaS selloff (more than 20%) reflected expectations, not observed replacement of major vendors ([S&P](https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/2/software-sell-off-may-be-overdone-yet-exposes-deeper-concerns-97965687)).

## Exposed vs durable

**Exposed:** thin interfaces over commodity data or models, and generic generation or agent-loop wrappers. Also shallow CRUD whose behavior is recoverable from screens and exports, per-seat tools that depend on humans clicking, and anything without owned state, hard integrations, an outcome loop, network effects, or an accountability boundary.

**Durable:**
- authoritative state and transactions (ledgers, identity, entitlements, history)
- operational guarantees (permissions, validation, idempotency, audit, rollback, sign-off)
- hard connectivity (maintained integrations, external contracts, physical or organizational boundaries)
- proprietary inputs and accepted outcomes (see [outcome-based learning](../agents/learning-from-feedback.md#outcome-based-learning))
- embedded domain process (exceptions, approvals, institutional rules)
- networks and shared history
- agent tooling (compilers, tests, schemas, sandboxes, CI)

A system of record isn't automatically safe: its data model and happy paths become cheap to rebuild. Exceptions, integrations, and accountability are the hard part. Interfaces shrink as agents operate products through APIs.

## Architecture as intelligence gets cheap

Use code for settled behavior and agents for semantic judgment:

```text
unstructured input → agent interpretation → typed plan → deterministic validation and execution
→ authoritative result → outcome capture → candidate improvements (examples, knowledge, config, code)
```

Agents produce typed plans; they don't improvise external writes. Deterministic machinery owns schemas, permissions, validation, idempotency, transactions, audit, and execution. A typical app becomes domain APIs and CLIs, typed schemas, hard validators, Markdown knowledge and examples, traces and evals, a thin agent runtime, and a small UI for review, exceptions, and approval. Isolated corrections become examples, recurring local patterns become scoped config, and stable detectable rules become code.

## Provider gravity in coding harnesses

Providers co-train models with their own agent loops: OpenAI's [Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview) gives a managed Codex harness, and the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) exposes Claude Code's loop. An independent harness competing on prompts, generic tool loops, compaction, or decomposition is fragile, because providers see failures outsiders can't and ship model and harness together. Universal cross-model loops drift toward the lowest common denominator. Domain-specific harness work still pays, but each component encodes an assumption that model progress can invalidate ([Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)). Keep the model-facing loop thin, measured, and replaceable.

Standardize **above** native harnesses:

```text
shared workspace, workflow, policy, evaluation, durable state
             provider-native Codex / Claude / other
       repo, sandbox, tools, tests, CI, external systems
```

Independent coding products earn their place through:
- the collaborative multi-session workspace
- org-specific context
- execution, credentials, and policy
- review, evaluation, replay, and outcome history
- integrations with issues, CI, and production systems
- provider choice where it creates real leverage

Multi-provider support alone is easy to copy. This is T3 Code's direction (see [projects](../projects.md#t3-code)).
