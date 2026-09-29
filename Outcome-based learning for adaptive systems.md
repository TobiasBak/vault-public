# Outcome-based learning for adaptive systems

An adaptive system can learn from the difference between what its current implementation would produce for an input and the outcome ultimately accepted in the real system. This operational feedback is often stronger and cheaper than trying to capture every user's intent or rationale.

## Core loop

1. Retain or recover the original task input.
2. Let an agent use the current code, configuration, and tools to determine the system's current predicted action or state.
3. Observe the accepted real-world outcome at a meaningful completion milestone.
4. Compare predicted and accepted state, preferably with a deterministic structural diff before model interpretation.
5. Let agents identify recurring differences and propose or implement scoped changes.
6. Re-run the original and representative cases against the current system to verify improvement and detect regressions.

Learning targets current behavior, not the historical implementation that first produced the feedback. An old episode remains useful evidence only if the current system still reproduces its mismatch. An archived historical plan can improve auditability and exact reconstruction, but it is not required for the simpler current-system comparison.

## Evidence boundaries

An accepted outcome is not automatically universal ground truth. Observe it at a meaningful milestone because later state may contain unrelated changes. Compare only the parts of the outcome the system intends to own. A single difference may be a one-off correction or workaround; recurrence across applicable cases strengthens it, and recurrence across independent scopes determines whether a lesson should remain local or become global.

Agents may suggest changes or alter bounded behavior directly depending on consequence, evaluation quality, and rollback. In either case, separate observed differences from derived lessons and validate changes against more than the episode that inspired them. See [[Agent learning from experience and user feedback]].

Keep enforcement proportional to consequence. An early experiment with a cooperative agent, a disposable external test environment, and Git-backed source may reasonably rely on an explicit read-only mission and existing client safeguards. Do not add brokers, isolated filesystems, agent modes, schedulers, or durable feedback infrastructure until observed failures or scale justify them.

## Direction as inference becomes cheaper

Cheaper and faster models make repeated interpretation, replay, and improvement economical. Access to capable models becomes less differentiating, while proprietary inputs, accepted outcomes, and a reliable feedback loop become more valuable.

The application can increasingly become agent-driven orchestration over durable Markdown knowledge, typed schemas, and constrained tools. Deterministic machinery should continue to own stable operational guarantees such as permissions, external writes, validation, idempotency, and auditability. See [[Prompting tool-using agents]] and [[AI-era software durability]].
