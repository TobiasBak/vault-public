# Renderless behavioral verification

Use the [production-model proof boundary](../skills/review-test-quality/references/behavioral-boundaries.md)
for rule-only changes. That reference owns the enforcement and migration rules;
this case records the measured gain and its limits.

recheck-after: 2027-01-29

## What changed the decision

A local native Rust UI study on 2026-10-28/29 found two separate costs. Rust
compilation dominated the host CPU sample even when no GUI app was running.
Within a native workbench case, software rendering was expensive. Calling the
whole application "headless" would not remove its GUI compilation graph.

Selection coordination and pane arithmetic moved from the renderer into the
production model. Tests composed that model with the real drawing model and
checked contract values and generated action sequences. The renderer retained
native entities, event translation and execution of effects. The model test
build had 147 artifacts and no GPUI artifacts.

Static checks protected the pure dependency closure, including model test/build
edges, indirect workspace dependencies and platform-specific edges. Fault
probes rejected wrong resize steps, missing row-selection effects, lost pane
preferences and a model clock read. This made the cheap path an enforced
boundary rather than an instruction agents had to remember.

Repeated GUI state assertions were transferred only after the unchanged native
scenario passed against the extracted models. The case record named replacement
checks and retained native proofs; remaining expected output was not regenerated
from the candidate. Native key routing, focus, accessibility, popout lifetime,
empty-state presentation and document content stayed covered.

The property tests also exposed a harness interaction: a generated regression
seed written into the source tree changed the verifier's input fingerprint.
Disabling that source-directory persistence preserved shrinking and failure
evidence while letting the deliberate fault produce a normal failing verdict.

## Measured effect and limits

The comparison was the verification choice for a selection/pane-only edit:
the complete production model suite instead of the native workbench journey.
It was not a comparison of equivalent full-GUI coverage.

Five alternating batches per side each forced two fresh executions after
warmup. All 20 executions passed. Values below are batch medians, with the
full batch range.

| Warm verification path | CPU seconds | Seconds to returned verdict |
| --- | ---: | ---: |
| Native workbench journey, twice | 93.3; range 91.6 to 100.9 | 49.8; range 33.5 to 66.8 |
| Complete model suite, twice | 8.7; range 8.4 to 11.4 | 9.3; range 8.8 to 14.1 |

CPU covered the containing gah cgroup and child case cgroups. Persistent
compiler daemons outside that scope were excluded. Elapsed time included the
normal build-freshness checks and harness through the returned verdict. Other
compiler work was active on the 16-logical-CPU host.

After integration, one additional alternating pair on the final implementation
passed: 104.0 versus 12.6 CPU seconds, and 91.3 versus 15.8 elapsed seconds,
again for two executions per side. That pair confirms the large effect under
load; it is not a second five-batch estimate.

The original comparison saved about 91% of CPU for this rule-only proof choice;
the final pair saved about 88%. Shortening the native scenario itself showed
no convincing CPU saving. These results establish neither faster cold builds
nor faster complete qualification. The model path's remaining CPU was mostly
Cargo and verifier metadata, hashing, parsing and allocation.

Source: locally retained
`~/.local/state/orderready-renderless-verification/2026-10-28/measurement-audit.json`,
its referenced run receipts and the separate CPU profiles. Raw artifacts stay
outside the vault; product commands and requirements stay in their repository.

See [testing with agents](testing-with-agents.md) for the wider verification loop
and [verification latency](verification-latency.md) for whole-edit measurements.
