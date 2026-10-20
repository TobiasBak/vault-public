# Runtime outcomes and recovery

Establish the product's actual state at the boundary that owns each effect. Verification traces explain the feedback pipeline; they do not establish what the product did to files, services, or users.

## Find the answer before adding machinery

Take the changed operation and identify its public interface, intended outcome, affected resources, and effect owners. Use existing readback, status, logs, and diagnostics to answer:

| Question | Evidence needed |
|---|---|
| What state exists now? | Authoritative readback from the owner, with resource identity and observation time |
| What happened to this operation? | Correlated request or operation identity, attempted effects, acknowledgements, and remaining work |
| Which effects succeeded, failed, or are uncertain? | Per-effect state; a timeout or lost acknowledgement is not proof of no effect |
| What can safely be retried or repaired? | The owner's supported operation and its duplicate-prevention, preconditions, or compensation contract |

If an answer is missing on the real task, fix that gap at its owner. Do not create a universal state model, status service, or recovery CLI just to satisfy this reference.

## Make outcomes inspectable

- Distinguish an accepted request, completed local work, and confirmed external effects. A success response or clean process exit alone proves none of the later stages.
- Correlate structured events with the operation and affected resources so an agent can find causal evidence without reconstructing it from unrelated logs. Preserve useful failure evidence beyond disposable worker state.
- Name the authority and freshness of a diagnostic view. A stale projection, local intention, or fake service receipt is not the external system's current state.
- Represent incomplete and uncertain effects explicitly. If an external owner cannot confirm an outcome, retain that uncertainty instead of reporting success or retrying blindly.
- Keep diagnostics safe for the intended reader; never expose credentials or private payloads merely to make a failure easier to inspect.

## Explain a failure

Explain a failure before fixing, retrying, or handing it off.

1. Read the first failing step and its raw evidence: the compared values, logs, exit status, and environment. If the evidence is missing, that gap is the first defect: fix capture at its owner before spending another scarce run.
2. List the candidate causes: product, check or oracle, environment, missing evidence. Pick the cheapest observation that separates them, such as a host reproduction, a comparison on equivalent workloads, a bisection, or reading the installed code. State what each candidate predicts before running it.
3. Fix the established cause at its owner. If the check was wrong, show the reproduction that proves it and keep the behavior it was meant to guard.
4. If a limit blocks the deciding observation, keep diagnosing everything else. Hand off the evidence inspected, the remaining explanations, the next probe, and the exact missing authority or capability. "Remaining: diagnose" is not a result.

Harnesses persist expected and actual values before asserting, export every assertion input with the run's evidence, and keep output when a run fails or times out. Before a new or changed harness drives an expensive or gated run, run its comparison logic on the cheapest host against a known pass and a deliberate failure, including zero, one, and many values where collections are compared.

## Repair at the effect boundary

1. Read the current state and reconcile it with the intended outcome. Bound the affected operation and resources before changing anything.
2. Use the owning interface's supported retry, resume, reconcile, or compensation operation. Apply the required authority and preconditions; missing permission or unavailable state is blocked recovery.
3. Prevent duplicate effects at the boundary where they occur. A local retry flag cannot establish that a remote write did not happen. Do not promise exactly-once effects without a contract that supports them.
4. Read back the resulting state, including any remaining partial effects. A compensation is a new effect with its own possible failure, not an erasure of history.

A source revert changes future execution, not existing external state. Direct storage edits or improvised cleanup are not a supported repair unless the owner explicitly defines them as such. When no safe repair exists, contain further effects and report the affected identities, known state, uncertainty, and authority needed to proceed.

## Proof

For the changed path, run the real public interface in an isolated environment and verify its effects by authoritative readback. Check expectations against the [independent contract](black-box-tests.md#evidence-and-authority); evidence from a fake external service establishes only the exercised fake-environment behavior.

When recovery changes, use a relevant environment failure, such as a service accepting a write but losing its acknowledgement. Establish the resulting partial or uncertain state, exercise supported repair, and read back that the required outcome holds without duplicate effects or false success. Use the [case boundaries](black-box-tests.md#the-box), not private hooks or permanent probe switches.

Report what completed, what remains unknown or blocked, and the supported next action. Run only the failure needed to establish the changed recovery contract, not a speculative failure matrix.
