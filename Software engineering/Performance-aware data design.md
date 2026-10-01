# Performance-aware data design

An idiomatic, correct data model can dominate a hot path's cost. Rich objects and general containers make ownership clear and features easy to add and test. They suit scripts, bindings, and cold API glue, but allocation, copying, lookup, formatting, indirection, and memory layout can cost more than the computation in a frequently executed kernel.

Data representation is part of performance architecture. Ask what data the workload moves, how often, and how the kernel accesses it, not whether a type is modern or idiomatic.

## Failure pattern

An agent builds a convenient record containing everything any consumer needs, using owned containers and readable strings. Correctness tests pass. Features and usage grow without revisiting the layout. When the path becomes hot, profiling reveals that moving and accessing data costs more than the math, and the record must be redesigned.

Common C++ examples are:

```cpp
std::vector<T> out;
std::unordered_map<Key, Value> map;
std::string name;
std::optional<Metadata> metadata;
std::function<void(...)> callback;
std::ostringstream message;
```

None is inherently unsuitable for a hot path. Cost depends on ownership, scale, allocation, access order, reuse, and the fields the kernel touches.

| Convenient representation | Possible hot-path cost | Representation to investigate when measured |
| --- | --- | --- |
| A dynamic vector owned by every record | Many heap allocations, growth, copying, and pointer chasing | One flat or pooled buffer, offsets into shared storage, preallocation, or reuse |
| `unordered_map` | Hashing, indirection, poor locality, and allocator traffic | Dense indexing, sorted contiguous data, a specialized table, or moving lookup outside the kernel |
| `string` in every record | Allocation, variable-width data, comparison, parsing, and formatting | Stable IDs, enums, string interning, spans, or boundary-only names |
| `optional<Metadata>` inside the hot record | Wider records and cold fields loaded or copied with hot fields | A side table or explicit hot and cold records |
| `function` callbacks | Indirect dispatch, opaque ownership, and possible allocation | Explicit staged dispatch, function pointers, variants, or callbacks outside the inner path |
| `ostringstream` | General formatting machinery and repeated allocation | Preallocated formatting or producing diagnostics outside the kernel |

`vector` is often an excellent hot-path container because it is contiguous. Thousands of separately owned vectors or rich elements carrying cold state are the common problem, not `vector` itself. Processing whole records can favor an array of structures; scanning a few fields across many records can favor a structure of arrays.

Memory topology includes object relationships and traversal order: pointer graphs, nested ownership, hashes, and linked structures. Cheap math can still be slow when reaching its operands requires scattered reads and unpredictable control flow.

## Design and measurement method

1. **State the workload.** Record representative frequency, cardinality, payload distribution, target hardware, and the latency, throughput, or memory behavior that matters. A consequential threshold needs a measured receipt rather than a guessed limit.
2. **Measure the whole path.** Benchmark representative end-to-end work, then attribute time and allocation to domain computation, data movement, lookup, formatting, synchronization, and boundary conversion. A microbenchmark of the arithmetic alone answers a different question.
3. **Find the hot state.** Identify which fields are touched together and which metadata is cold, diagnostic, or consumer-specific. Do not let one record become the union of every consumer's needs by default.
4. **Compare representations.** Investigate batching, reuse, compact handles, flat storage, hot/cold separation, staged transformation, specialized indexing, or another layout that matches the measured access pattern.
5. **Price the complexity.** Specialized representations can reduce readability, complicate ownership, duplicate state, or make rare operations slower. Keep the rich boundary model when it remains useful and translate into a kernel representation only when the measured gain earns that cost.
6. **Validate both contracts.** Preserve correctness against an independent expected result and remeasure the representative workload. A fast wrong result and a correct cost model that was never measured are both failures.
7. **Record the change trigger.** Revisit the representation when frequency, cardinality, consumers, payload shape, hardware, or the dominant operation changes materially. Describe the decision as [[Software architecture#Design from drivers and tradeoffs|driver → decision → structure → consequence → change trigger]].

Correctness tests cannot establish that the cost model still fits. When performance is a real contract, retain a representative benchmark, profile, or measured tripwire alongside the behavioral tests. Do not turn implementation-specific timing noise into a hard gate without establishing a stable environment and a useful failure signal.

## Working with coding agents

Give the agent the workload before it chooses or extends the representation: known hot paths, the performance owner, representative inputs and scale, target hardware, and a route to benchmarks or profiles. Without that context, optimizing for local clarity and correctness is reasonable.

Review changes against the measured access pattern. New fields may be cold or consumer-specific rather than belong in every hot record. Feature growth can invalidate the original layout. Accept a specialized representation only after measuring the gain and its complexity cost.

Do not promote this into a global ban on rich objects or standard containers. Cold paths should usually optimize for clarity, correctness, and changeability. Hot-path redesign should follow representative evidence, not performance folklore or an agent's preference for low-level cleverness.

## Related examples

- [[Gigatoken]] gains much of its throughput from specialized state machines, cache reuse, and avoiding large cross-language object movement rather than changing the tokenization contract.
- [[Tobias's developer preferences]] favors direct domain models and simple data flow while leaving room for data-oriented design when measurements justify it.
