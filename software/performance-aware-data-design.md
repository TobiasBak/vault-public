# Performance-aware data design

An idiomatic, correct data model can dominate a hot path's cost. Rich records and general containers suit cold code, but in a frequently executed kernel the cost of allocation, copying, lookup, formatting, and indirection can exceed the computation itself. Data representation is part of performance architecture.

**Typical failure:** an agent builds one convenient record holding everything any consumer needs. Tests pass, features accrete, and later profiling shows data movement costs more than the math.

| Convenient | Hot-path cost | Investigate when measured |
|---|---|---|
| Vector owned by every record | Allocations, copies, pointer chasing | Flat or pooled buffer, offsets, reuse |
| `unordered_map` | Hashing, poor locality, allocator traffic | Dense indices, sorted arrays, lookup outside the kernel |
| `string` per record | Allocation, compare, parse, format | IDs, enums, interning, boundary-only names |
| `optional<Metadata>` in hot record | Wide records dragging cold fields | Side table, hot/cold split |
| `std::function` callbacks | Indirect dispatch, allocation | Staged dispatch, variants, function pointers |
| `ostringstream` | Formatting machinery, allocation | Preallocated or out-of-kernel diagnostics |

`vector` itself is often ideal because it's contiguous; thousands of separately owned vectors are the problem. Use an array of structs for whole-record processing and a struct of arrays for scanning a few fields. Pointer graphs and nested ownership make cheap math slow.

## Method

1. **Workload:** frequency, cardinality, payload distribution, hardware, and the latency, throughput, or memory target. Thresholds need a measured basis.
2. **Measure the whole path** and attribute time and allocation to compute, data movement, lookup, formatting, sync, and conversion. A microbenchmark of the arithmetic answers a different question.
3. **Find hot state:** which fields are touched together and which are cold or consumer-specific.
4. **Compare representations:** batching, reuse, handles, flat storage, hot/cold split, staged transforms.
5. **Price the complexity.** Keep the rich model at the boundary and translate to a kernel representation only when the gain earns it.
6. **Validate correctness** against an independent expectation and remeasure.
7. **Record the trigger** for revisiting: changes in frequency, cardinality, consumers, payload, or hardware.

Vet every reported number with the [benchmark checklist](../skills/benchmark-checklist/SKILL.md). Keep a representative benchmark or measured tripwire next to the behavioral tests when performance is a contract, but don't make noisy timings hard gates.

**With agents:** give them hot paths, scale, hardware, and benchmark routes before they design data structures. Without that, optimizing for clarity is correct. Never ban rich objects globally; redesign hot paths from evidence, not folklore. [Gigatoken](gigatoken.md) is an example.
