# AI lead developer workflow strategy

This strategy concerns how developers work and how a team adopts AI in development. It does not concern adding AI to products.

## Working direction

Shorten the time from a developer's change to trustworthy feedback. Judge improvements by confirmed defects found, missed defects, false alarms, developer investigation time, and ongoing cost and maintenance, rather than generated code or test counts.

The durable investment is representative cases, clear expected behavior, easy environment startup, isolated test data, reliable resets, and inspectable results. These help developers and remain useful when models change.

## Automated testing opportunity

[[Agentic end-to-end testing]] is the stronger initial opportunity. An agent can exercise a running application, explore unexpected paths, inspect logs and APIs, and return reproducible failures. Stable discoveries should become deterministic regression tests where possible. Exact checks still own persistence, permissions, calculations, and external effects.

[[Jev and decision models]] could support repeated judgments within that process:

- Group related failures to reduce duplicate investigation.
- Classify likely environment problems, application defects, and inconclusive results.
- Check whether recorded evidence supports an agent's conclusion.
- Check meaning where exact assertions are awkward, such as whether an error message explains the observed failure.

These are untested candidates, not adopted capabilities. Jev does not replace the agent that operates the application or investigates a failure. A success message is not evidence of persistence; a checker needs authoritative state, not merely the testing agent's account of success. Model judgments should not initially approve PRs, gate releases, or decide which tests to skip.

## Proposed first experiment

Test one troublesome workflow with an agent alongside the existing process. Compare actionable findings and developer effort against the baseline. Evaluate semantic checks on known successes and real failures without letting them decide releases. Add Jev only if repeated judgments create a meaningful cost or delay and it performs well against alternatives.

No pilot has been selected or run. The next useful context is where the team loses time today: implementation, review, or verification.
