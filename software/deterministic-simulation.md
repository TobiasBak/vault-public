# Deterministic simulation

recheck-after: 2027-05-03

Make a simulation a pure function of its seed and input log, and one property pays several times: exact replay of bug reports, server-side verification of client results, headless bots for tuning, and recorded-input regression tests. Keep rendering, audio and wall-clock time outside that function.

## Evidence: tibo.dog

Lauren Tan's agent-built browser game ([post](https://x.com/poteto/status/2117043478140276847), 2026-11-01) uses a fully deterministic simulation:

- The server replays every submitted high-score run from its inputs and rejects runs that don't reproduce the score.
- Headless bots play each difficulty to tune it against target survival rates. That is an [autoresearch](../agents/autoresearch.md) loop with a design objective. Bots measure bot survival; check the tuned values against human play.
- Three.js only draws. The simulation, post-processing and audio are custom, which keeps the determinism boundary in owned code.

The shipped bundle follows the JavaScript rules below (inspected 2026-11-03). The `sim` chunk uses only `max`, `min`, `floor`, `round`, `abs`, `sqrt`, `sign` and `imul` from `Math`, hashes integers for randomness and stores state in typed arrays. `sin`, `cos`, `hypot`, `atan2` and `performance.now` appear only in the rendering chunk.

## JavaScript rules

Client and server may run different engines, so the simulation avoids everything [ECMA-262](https://tc39.es/ecma262/#sec-math) leaves to the implementation:

- No `Math.random`, `Date.now` or `performance.now`. Seed an integer PRNG and step on a fixed tick.
- Only exactly specified arithmetic: `+ - * /`, `Math.sqrt`, rounding, `min`, `max`, `abs`, `sign`, `imul`. The spec defines `sqrt` as the correctly rounded result but calls `sin`, `cos`, `pow`, `hypot`, `exp`, `log` and the other transcendental functions "implementation-approximated", so V8 and JavaScriptCore may disagree in the last bit and a replay diverges. Use lookup tables or own implementations built from exact operations.

Enforce both with a lint rule scoped to simulation files by path ([Theodore's path-role checks](../skills/theodore-kaczynski-nullifier/references/enforcement.md#scope-by-path-role)), not with prose.
