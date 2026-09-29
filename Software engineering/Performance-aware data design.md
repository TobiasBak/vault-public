# Performance-aware data design

An idiomatic, locally correct data model can become the dominant cost of a hot path. Coding agents naturally reach for rich objects and general-purpose containers because they make ownership clear, features easy to add, and correctness easy to test. Those qualities fit tests, scripts, bindings, and cold API glue. In a frequently executed kernel, however, allocation, copying, lookup, formatting, indirection, and memory layout can cost more than the domain computation itself.

This makes data representation part of the performance architecture. The important question is not whether a type is modern or idiomatic, but what data the workload moves, how often it moves it, and how the consuming kernel accesses it.

## Failure pattern

An agent-shaped failure pattern to watch for develops like this:

1. Implement a feature with rich objects because that is locally easy.
2. Put everything needed by any consumer into one record.
3. Use general containers because they simplify ownership.
4. Use strings because they are readable and stable at boundaries.
5. Add correctness tests and establish that the feature works.
6. Extend the feature repeatedly without revisiting the representation.
7. Discover that the formerly small path now runs thousands of times.
8. Profile it and find that allocation, copying, lookup, formatting, indirection, and topology dominate rather than the actual math.
9. Spend several iterations undoing the original data model.

The characteristic C++ shape is convenient and reasonable in isolation:

```cpp
std::vector<T> out;
std::unordered_map<Key, Value> map;
std::string name;
std::optional<Metadata> metadata;
std::function<void(...)> callback;
std::ostringstream message;
```

None of these types is inherently unsuitable for performance-sensitive code. Their cost depends on ownership shape, record count, allocation pattern, access order, reuse, and which fields the kernel actually touches.

| Convenient representation | Possible hot-path cost | Representation to investigate when measured |
| --- | --- | --- |
| A dynamic vector owned by every record | Many heap allocations, growth, copying, and pointer chasing | One flat or pooled buffer, offsets into shared storage, preallocation, or reuse |
| `unordered_map` | Hashing, indirection, poor locality, and allocator traffic | Dense indexing, sorted contiguous data, a specialized table, or moving lookup outside the kernel |
| `string` in every record | Allocation, variable-width data, comparison, parsing, and formatting | Stable IDs, enums, string interning, spans, or boundary-only names |
| `optional<Metadata>` inside the hot record | Wider records and cold fields loaded or copied with hot fields | A side table or explicit hot and cold records |
| `function` callbacks | Indirect dispatch, opaque ownership, and possible allocation | Explicit staged dispatch, function pointers, variants, or callbacks outside the inner path |
| `ostringstream` | General formatting machinery and repeated allocation | Preallocated formatting or producing diagnostics outside the kernel |

`vector` is often an excellent hot-path container because it is contiguous. The problematic shape is commonly thousands of separately owned dynamic vectors or rich elements containing cold state, not `vector` itself. Likewise, array-of-structures and structure-of-arrays are workload choices: processing whole records can favor the former, while scanning a few fields across many records can favor the latter.

“Topology shape” includes the relationships and traversal pattern between objects: pointer graphs, nested ownership, hashes, linked structures, and the order in which memory is visited. A mathematically cheap operation can still be slow when reaching its operands requires scattered reads and unpredictable control flow.

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

An agent that is not given the workload will reasonably optimize for local clarity and correctness. For performance-sensitive work, make the operating model available before it chooses or extends the data representation:

- identify known hot paths and the owner of their performance contract;
- provide representative inputs, scale, hardware, and benchmark or profiling commands;
- require inspection of allocation, copying, lookup, formatting, indirection, and access patterns rather than timing only the core algorithm;
- ask whether new fields are hot, cold, diagnostic, or consumer-specific before adding them to a shared record;
- require a measured comparison before accepting a more specialized representation;
- remeasure after feature growth instead of assuming a once-small path remains cold.

Useful review questions are:

- Has one record become the union of everything any consumer might need?
- Does the inner path allocate, hash, copy, format, parse, or traverse strings?
- Are cold metadata and diagnostics carried through every operation?
- Is the benchmark measuring domain computation or mostly representation overhead?
- Does the access pattern match the container and layout?
- Has usage changed enough to invalidate the original design decision?

Do not promote this into a global ban on rich objects or standard containers. Cold paths should usually optimize for clarity, correctness, and changeability. Hot-path redesign should follow representative evidence, not performance folklore or an agent's preference for low-level cleverness.

## Related examples

- [[Gigatoken]] gains much of its throughput from specialized state machines, cache reuse, and avoiding large cross-language object movement rather than changing the tokenization contract.
- [[Tobias's developer preferences]] favors direct domain models and simple data flow while leaving room for data-oriented design when measurements justify it.
