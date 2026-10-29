# Choose the behavioral proof boundary

Exercise a contract through the least expensive production interface that can
prove it. A black-box test does not have to launch the whole application.

## Match the proof to the obligation

| Obligation | Proof boundary |
| --- | --- |
| Invalid states, dependency direction, forbidden effects | Types, schemas and executable static checks |
| Selection, navigation, validation, reconciliation, stale-result policy, pane arithmetic | The public API of the production model that owns the rule |
| Persistence, transactions, protocols and effectful recovery | The owning API or adapter with its real operated dependencies |
| Key delivery, focus, clipboard, accessibility, window lifetime and binding model output to controls | The real app with its native or browser driver |
| Appearance, text geometry and rendered content | The relevant renderer; screenshots when the contract is visual |

A model proof cannot establish a native binding, and a dependency check cannot
establish correct model behavior. State both obligations when a change crosses
their boundary. Repository policy still owns landing and promotion requirements.

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
  compiles a renderer, accessibility driver or service runtime.
- Expose narrow build and behavioral jobs through the existing repository
  entrypoint. A windowless mode of the full application may still pay the full
  GUI compilation cost. Do not build a second runner just to avoid a window.
- Keep generated counterexamples outside fingerprinted source inputs. A
  property test writing a regression seed into its source directory can turn
  an ordinary failure into an input-change block. Retain shrinking and replay
  evidence in run artifacts; promote useful counterexamples deliberately.

The [enforcement rules](enforcement.md#checks) own gate integration. Reject a
known forbidden edge or effect and accept the supported model target through
the real check entrypoint before relying on the guard.

## Transfer assertions without transferring away the native proof

For a targeted reduction of GUI assertions:

1. Identify each assertion's independent contract, replacement model check and
   retained native mechanism. Keep this proof-ownership map in the case record,
   not a parallel feature catalogue.
2. Run the existing native scenario against the refactored implementation before
   pruning it. Unexplained behavior differences block the transfer.
3. Show the model replacement rejecting the corresponding contract fault.
   Compilation errors, missing prerequisites and infrastructure blocks are not
   evidence that the assertion catches the bug.
4. Remove only the now-redundant permutations. Keep proof of distinct native
   mechanisms and affected bindings, with the original independent expectations.
   Record any necessary setup changes explicitly; never bless candidate output
   as the new oracle.
5. Run the retained native scenario and the replacement checks. Apply the
   repository's oracle-change metadata and review requirements.

This is an assertion transfer, not permission to delete an entire suite. A
whole-suite replacement follows the separate [migration proof](black-box-tests.md#migrating-an-existing-suite).

## Measure the claimed saving

Attribute CPU to processes before blaming GUI tests. Compiler work, test-driver
work and software rasterization are different costs. Compare the normal warm
rule-only path through its returned verdict, including build and harness work;
record CPU as well as elapsed time and identify excluded processes.

Force real executions when comparing lanes, check their outputs, alternate
under shared-host load and retain the spread. A model-only versus native
comparison measures a different proof boundary, not equivalent full-app
qualification. Shortening a native journey, avoiding a native launch and
reducing cold compilation are separate claims.
