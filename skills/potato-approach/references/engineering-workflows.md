# Engineering workflows

Some expert knowledge is a method, not a prohibition: choosing a useful trace, reproducing a timing bug, comparing a performance change. Check [hardening](hardening.md) first; a skill shouldn't hold what a check or API could enforce.

## Capture a demonstrated method

Start from work that succeeded. Identify what the human supplied that the agent couldn't recover: a prerequisite, a tool choice, a diagnostic distinction, a success criterion. Put each piece with its owner:

| Knowledge | Owner |
|---|---|
| Domain constraints, ownership, allowed dependencies | Types, APIs, static checks |
| Rules needing context to apply | Review agents |
| When a method applies and how to read evidence | Project skill |
| Repeatable setup, capture, measurement | Maintained command |
| Navigation and workflow meaning | Feature map |

Reuse existing skills and tools. Leave out conversation chronology and generic advice.

## Example: performance investigation

1. Reproduce the slow operation with representative data, naming the measurement and conditions.
2. Capture a baseline and the trace that explains it, with enough repetitions to beat noise.
3. Form a specific causal hypothesis from the trace.
4. Make a focused change and remeasure under the same conditions.
5. Check correctness. Keep the baseline, change, effect, conditions, and tradeoffs together. Investigate wins that come from skipped work or changed inputs.

Automate capture and comparison; keep interpretation with the agent. A CPU trace and a heap snapshot answer different questions. Don't prescribe limits or repetition counts without a basis.

## Improve through use

Try the skill on another task. If it fails, fix the missing decision or tool rather than appending checklists. Give the skill an owner, and remove steps once a command or check handles them. Validate with the [fresh-agent handoff](verification.md#fresh-agent-handoff-check).
