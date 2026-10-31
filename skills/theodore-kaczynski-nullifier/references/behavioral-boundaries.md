# Choose the behavioral proof boundary

Exercise a contract through the least expensive production interface that can
prove it. A black-box test does not have to launch the whole application.

## Match the proof to the obligation

| Obligation | Proof boundary |
| --- | --- |
| Invalid states, dependency direction, forbidden effects | Types, schemas and executable static checks |
| Selection, navigation, validation, reconciliation, stale-result policy, pane arithmetic, what a view shows | The public API of the production model that owns the rule |
| Persistence, transactions, protocols and effectful recovery | The owning API or adapter with its real operated dependencies |

A dependency check cannot establish correct model behavior, and a model check
cannot establish persistence. State both obligations when a change crosses
their boundary. Repository policy still owns landing and promotion requirements.

## No GUI tests

Tobias's policy (2026-10-31): no test drives a GUI, browser or accessibility
tree, and none compares screenshots. The product carries no hooks that exist
only so tests can drive or observe its UI.

- A rule a GUI test would protect moves into the
  [production model](#make-the-model-the-production-owner) and is proved there.
- Key delivery, focus, clipboard, accessibility, window lifetime and rendering
  have no automated proof. Keep the renderer a thin translation of model output
  and input intents, and report these as unverified when a change touches them.
- An agent may open the app to reproduce a reported bug or judge a design. What
  it finds becomes a model or API case, never a GUI case.

## Make the model the production owner

Move a coherent rule and its state out of rendering code. The renderer calls
that model, supplies measured geometry and service results, translates real
input into intents, and performs returned effects. There is one implementation,
not a simplified application written for tests.

A genuine model boundary has production callers, private state and a public
contract of inputs, projections and effect intents. Ordinary library test
targets may exercise that contract directly, including generated sequences.
Making every helper public or adding test-only setters does not create such a
boundary. Assert independently justified results, not internal calls or data
layout. Effect ordering is an assertion only where the consumer contract needs
that order.

## Keep the cheap path cheap

- Supply I/O results, time and randomness as inputs. Enforce production purity
  with source checks and dependency rules, rather than prose alone.
- Check model test/build dependencies as well as normal dependencies, including
  optional and target-specific workspace edges. Traverse reached dependencies'
  normal/build edges; their own development dependencies are not built unless
  their tests are also selected. Approve pure workspace libraries explicitly
  and give each reached owner a closed external dependency list.
- Inspect features and the resolved build graph when establishing or changing
  that boundary. A runtime-free source file is not enough if its test target
  compiles a renderer or service runtime.
- Expose narrow build and behavioral jobs through the existing repository
  entrypoint. A windowless mode of the full application still pays the full
  GUI compilation cost.
- Keep generated counterexamples outside fingerprinted source inputs. A
  property test writing a regression seed into its source directory can turn
  an ordinary failure into an input-change block. Retain shrinking and replay
  evidence in run artifacts; promote useful counterexamples deliberately.

[Enforcement](enforcement.md) owns gate integration. Reject a known forbidden
edge or effect and accept the supported model target through the real check
entrypoint before relying on the guard.
