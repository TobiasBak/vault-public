# Engineering workflows

Some expert knowledge belongs in a method rather than a prohibition. A team may repeatedly need help choosing a useful trace, reproducing a timing failure, or comparing a performance change. Preserve the part that makes those investigations work.

Do not turn every engineering correction into a skill. First ask whether the knowledge can change the codebase or become a static check, following [Codebase hardening](codebase-hardening.md). Skills preserve investigation and implementation methods; [review agents](review-agents.md) check resulting changes against rules that still need judgment.

## Capture a demonstrated method

Start from work that produced a useful result. Identify what the person supplied that the agent could not recover from the project: a prerequisite, a tool choice, a diagnostic distinction, or a way to judge success.

Keep the reusable parts in the right place:

| Knowledge | Owner |
|---|---|
| Settled domain constraints, state ownership, and allowed dependencies | Types, APIs, architecture, and static checks |
| Engineering rules whose application needs context | Repository rules and focused review agents |
| When a method applies and how to interpret evidence | Project skill |
| Repeatable setup, capture, transformation, or measurement | Maintained command or helper |
| Product navigation and workflow meaning | Feature map |

Reuse existing skills and tools before adding another. Leave out the chronology of the original conversation and generic engineering advice. The next agent needs the decisions that transfer, not a transcript or a mandatory script for every task.

## Example: performance investigation

Adapt this to a real symptom and the project's profiling tools:

1. Reproduce the slow user operation with representative data. Name the measurement and the conditions that affect it.
2. Capture a baseline and the trace needed to explain it. For noisy measurements, use enough repeated observations to distinguish the proposed gain from normal variation.
3. Identify the expensive work from the trace. Form a specific hypothesis about its cause before changing code.
4. Make a focused change and exercise the same operation under comparable conditions.
5. Check correctness as well as the performance difference. Keep the baseline, change, effect, conditions, and tradeoffs together. Reject or investigate apparent wins caused by missing work or changed inputs.

Automate capture and comparison when those mechanics recur. Keep interpretation and hypothesis choice with the agent. For example, a CPU trace and a heap snapshot answer different questions; collecting both by default is not a substitute for understanding the symptom.

The skill should point to the project's actual tools and useful signals. It should not prescribe arbitrary performance limits, repetitions, or budgets without a basis.

## Improve it through use

Try the skill on another relevant task. Observe whether it removes the repeated need for coaching and still produces inspectable evidence. If it fails, correct the missing decision or tool behavior rather than appending a generic checklist.

Give the shared skill and its helpers an owner. Update them when the workflow changes, and remove instructions that duplicate behavior now handled by a command or enforced check.

Use the [fresh-agent handoff check](verification-cli.md#check-the-fresh-agent-handoff) to assess whether another agent can recover the method without the original conversation.
