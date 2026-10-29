# Repository diagnosis and design

Judge structure by what a contributor must discover, coordinate and remember to make a correct change. Remove unnecessary obligations; do not optimize for a tidy tree or a low smell count. The [foundations](design-principles.md) set the goal; this procedure finds the structure that serves it.

## Pick the change before judging the structure

Turn "this repo is slop" into a concrete question: add a real capability, change a business rule, replace an integration, or explain a reported failure. Draw representative changes from current requirements, actual consumers and relevant history. Include a consequential failure path when the task involves effects. Do not invent future extensibility to justify a framework.

For an existing repository, trace from the public operation through its runtime wiring to policy, state writes, external effects and the result callers observe. Search by the domain's names, then follow callers, implementations and constructors. An interface declaration is not proof that production uses it. Check other writers and entry points, including workers and migrations when they touch the same facts. Read relevant history for repeated fixes and reversals; co-changing files are a clue, not proof of bad coupling.

For a new repository, sketch the first caller's successful operation and meaningful failure before choosing modules. Identify which facts must be authoritative and who commits effects. Build that vertical workflow and its behavioral proof before extracting reusable infrastructure.

Keep the working trace in task notes or the report, not a parallel architecture inventory committed to the repo. Follow the requested scope: diagnosis, a proposed shape, and implementation are different deliverables.

## Find the mechanism, not just the smell

A useful finding identifies the locations, the decision or invariant they share, and the realistic change that becomes unsafe or unnecessarily scattered. Separate what source proves, what runtime evidence shows, and what remains a prediction. If a failing check or operation is the evidence, use [failure diagnosis](runtime-outcomes.md#explain-a-failure) before attributing it to architecture.

"This class is too large" supplies no repair criterion. "Adding a retryable failure requires updating three independent classifications, and a missed site silently disables retries" identifies the decision to consolidate and the behavior to protect. A class split that leaves those classifications independent does not fix it.

Several smells can come from one cause. Duplicated validation, undocumented call ordering and scattered edits may all result from a missing owner. Report and repair that cause once rather than scoring three independent defects. Prioritize broken contracts, consequential failure and recurring friction over awkward but stable code. Recommend leaving sound structure alone.

Use these lenses to form questions, not automatic rejection rules:

| Lens | Look for | Do not confuse it with |
|---|---|---|
| Decision ownership | Independent copies of one rule, competing writers, or callers coordinating private stages to preserve an invariant | Similar code with different reasons to change. One authority need not mean one class, file or process. |
| Decomposition | A feature's knowledge spread across technical layers or load/validate/save stages, so one decision requires repeated interpretation | Shared infrastructure with a genuine common contract. Feature-first folders can conceal the same scattering. |
| Contract leakage | Callers depend on storage layouts, vendor flags, ordering secrets or adapter details that the interface claims to hide | Explicit capabilities that genuinely differ. Do not force unlike integrations into a lying common interface. |
| State modeling | Boolean and optional-field combinations permit contradictions; every caller must remember which combinations work | Drafts, partial outcomes and uncertainty that the product actually has. Model them honestly rather than declaring them impossible. |
| Module depth | A large interface hides little, or many small files force repeated jumps to understand one operation | A substantial cohesive implementation behind a narrow contract. A "god file" is a responsibility problem, not a line threshold. |
| Dependency boundaries | A dependency crosses authority, state ownership, runtime or isolation constraints; an import rule has no discoverable reason | A chosen layer diagram. Keep useful boundaries, revise mistaken ones, and avoid layers that only forward calls. |
| Indirection | Delete a wrapper mentally: does policy or hidden knowledge return to callers, or only the callee's name? | A thin facade enforcing access or maintaining a public contract that existing consumers need. Hypothetical future substitution earns nothing. |
| Change propagation | A rule change needs hand-synchronized edits to several authorities, or an omitted site silently changes behavior | Necessary updates to a public schema, implementation, consumers and independent behavioral checks. Generated projections are not competing authorities. |

Do not turn file length, folder names, identical syntax or the number of changed files into correctness gates. Mechanical enforcement needs a specific invariant, not a proxy for good design.

## Types, validation and changing facts

Place each guarantee where it can actually be established:

- **Input meaning:** parse untrusted representations into domain values at their entry boundary. Internal code can rely on the properties that construction really guarantees, without repeated shape checks or fallback defaults.
- **Domain decisions:** keep business rules with their authoritative model. A structurally valid request may still be forbidden by the current lifecycle; that is a meaningful decision, not failed input decoding.
- **Current shared facts:** permissions, stock, uniqueness and revision identity can change after parsing. Enforce the relevant precondition where the state transition commits, with the owning transaction or conditional write. A value typed as approved does not prove its approval remains current.

Choose types that simplify real consumers. Do not build a type-state framework merely to encode every possible sequence. Keep invalid final combinations out of final types while giving legitimate intermediate and uncertain states their own representation.

Errors can originate anywhere an operation can fail. Handle them where the code can recover, translate the contract or clean up; a directory named boundary does not establish that responsibility. Changing an error model also changes consumers: inspect user-visible messages, serialized tags, retry classifications and non-exhaustive matches, not only constructors. More variants and cleaner chains are not improvements if behavior silently changes.

## Choose a coherent shape

For a material design decision, compare structurally different options before coding. Include leaving the structure alone or making a local repair when either meets the requirement; also consider merging responsibilities or deleting a needless feature or layer. Do not compare several patches that all preserve the same mistaken owner.

Write the proposed caller interaction, including a meaningful failure, and ask:

- Which component decides each invariant, and which one owns each state transition and external effect?
- What must a caller know beyond the interface? Does the module remove that knowledge or just move it to another file?
- Which details can change privately, and which changes legitimately require consumer coordination?
- Where do input decoding, current-state enforcement, outcome inspection and supported repair belong?
- What required behavior, compatibility, performance or deployment property does this option buy or risk?

Prefer the least complicated complete system satisfying the actual constraints. Reject both a small patch that adds another authority and a grand redesign that merely rearranges files. A larger cohesive module can beat tiny wrappers; a targeted extraction can beat retaining several independent responsibilities together. The driver decides, not a mandatory paradigm.

Record the chosen shape, its material tradeoff and the evidence that would make it worth revisiting. Use the existing task or decision owner; do not create an ADR tree or new documentation system for the exercise.

## Repair the whole affected path

When implementation is in scope, move the decision to its owner and update every affected producer, consumer and behavioral check. Remove the displaced route and misleading examples instead of leaving two supported ways to perform the operation. Keep migration machinery only for demonstrated consumer or durable-data obligations, with one owner for the translation.

Protect observable contracts while changing internals: error meaning, retry safety, lifecycle transitions, durable representations and required version coexistence all count. An accidental implementation detail need not survive just because an internal test asserts it; establish the independent requirement before changing either side.

Make the corrected path obvious to copy. Where the invariant is mechanically decidable, integrate a focused guard with its supported alternative using [enforcement](enforcement.md). A new naming convention or reminder is not a repair for split authority. Neither a guard nor a new abstraction substitutes for exercising the behavior.

## Proof

For diagnosis, show the traced scenario and enough source or runtime evidence to support the mechanism. Name uncertain consequences as hypotheses, with the next discriminating observation. Keep the report focused on consequential findings and a chosen next action; an empty findings list is valid when the structure holds up.

For a redesign, revisit the same change against the proposed interface. Show which independent decisions, hidden preconditions or synchronization points disappear and which necessary ones remain. This is a design argument, not a measured productivity gain.

For an implemented repair, exercise the affected [production contract](behavioral-boundaries.md), including the failure that motivated the work when applicable. Inspect all consumers of moved or split concepts, confirm the old authority is gone, and use [outcome and recovery proof](runtime-outcomes.md#proof) when effects change. Report what was preserved, what was deliberately changed and what remains unverified. Passing static checks alone does not establish a better design.
