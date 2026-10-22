# Agent-era development hardware

For cloud-served coding agents, buy local build capacity, not an AI accelerator. Size each box for simultaneous gates, persistent watchers and VMs; chat-thread count is not a hardware specification. Extra machines help only when teams or gate execution actually move to them.

## Measure before shopping

- Separate model latency, gate execution and admission waiting. Preserve workload, compiler version, cache state, concurrency, process boundary and errors beside every measurement.
- Cargo's [timings report](https://doc.rust-lang.org/cargo/reference/timings.html) distinguishes units waiting for CPU slots from units blocked by dependencies. Its active-unit graph excludes parallelism inside rustc.
- Measure whole gate process trees or cgroups, not one rustc or parent shell. Include VM reservations and other gates. Summed process RSS can double-count shared pages.
- Use available memory, pressure and active paging, not low Linux free memory or historical swap occupancy alone. Reclaimable cache isn't unavailable RAM; repair guards that count it as such while retaining every ancestor's genuine nonreclaimable budget. Worktrees mostly cost disk until their tools run.
- Passive samples can reveal contention, but cannot establish clean-build time, sustained cooling limits or an upgrade speedup.

## What to buy

**CPU:** strong per-core performance shortens dependency critical paths; physical cores support independent crates, gates and mutation workers. Cargo [defaults to logical-CPU-count jobs](https://doc.rust-lang.org/cargo/commands/cargo-build.html), so independent invocations can oversubscribe a host. Coordinate host-wide admission. SMT threads, Intel P/E cores and old server cores are not interchangeable capacity units. Ryzen AI Max is AMD; Intel's desktop line is Core Ultra. Neither an AI label nor an NPU/GPU score establishes compilation throughput. Compare complete-box cost within a capacity tier, using the same compilation harness where available. Keep synthetic multicore scores secondary; different engine versions, power settings or test cohorts cannot be joined into one ranking.

**RAM:** usable capacity must cover host reserve, non-gate agents/watchers, VMs and concurrent gate reservations without double-counting. There is no universal GB-per-agent figure. Inspect every ancestor's [cgroup limits](https://docs.kernel.org/admin-guide/cgroup-v2.html): a larger child budget cannot defeat its parent. RAM does not automatically change fixed limits, job slots or CPU capacity. Soldered RAM needs enough capacity at purchase; it has no DIMM upgrade path. Verify memory available to the CPU after any GPU reservation, not just the advertised total. A high-memory mini can ship with an inference-oriented split that leaves little RAM for builds, as the [GTR9 Pro review](https://www.servethehome.com/beelink-gtr9-pro-review-amd-ryzen-ai-max-395-system-with-128gb-and-dual-10gbe/3/) illustrates.

**ECC:** require CPU, board, firmware, DIMMs and Linux reporting to support correction. DDR5 on-die ECC is not system-level ECC. Registered server DIMMs are not desktop UDIMMs. Check actual memory channels and population; [Lenovo's P620 specification](https://psref.lenovo.com/syspool/Sys/PDF/ThinkStation/ThinkStation_P620/ThinkStation_P620_Spec.pdf) illustrates the difference. Do not sacrifice useful capacity or serial speed for an unverified ECC label.

**NVMe:** keep active source, targets and caches local. Budget duplicated worktree outputs and VM disks. Measure I/O pressure before paying for a faster PCIe generation. Backup storage is not a shared live Cargo target or T3 database.

**Cooling:** judge sustained compilation, not gaming benchmarks or boost clocks. Verify airflow, fan noise and wall power at the actual sustained setting. A temperature snapshot does not establish throttling; CPU TDP and PSU rating are not electricity consumption.

**GPU:** cloud coding models do not justify an inference GPU. Buy one only for explicit local-model, CUDA or graphics work. Preserve whatever display/GPU path real Linux and GUI verification requires. A bundled GPU is not a reason to reject an otherwise cheaper CPU/RAM system; compare the whole box without awarding an inference premium.

## Box and fleet choices

- Default to a modern single-socket box: good serial speed, local caches and straightforward ownership. Check exact board, firmware and validated memory configuration, not CPU capacity alone.
- Used Threadripper, EPYC and enterprise workstations deserve consideration when RAM, verified ECC or independent work exceed desktop limits. Compare complete systems including populated channels, storage, graphics, cooling and PSU. Rack servers need a suitable heat/noise location.
- Mini PCs must prove sustained cooling, memory capacity and expansion. Do not pair a barebone price with an unavailable high-memory SKU.
- Several boxes isolate teams and failures, but duplicate base RAM, storage and cache warming. A big box pools capacity but increases the shared failure domain. Choose from measured per-box admission and successful gates/hour, not summed core counts.
- Keep NAS and backup service separate from expendable build state. Remote workers need source access, not private model credentials.
- Remote rental can absorb bursts. Include transfer/setup latency, cache persistence, confidential-source handling and idle billing. No local hardware purchase is required to evaluate that option. Google AI plans already include some Colab compute; see [Colab in Google AI plans](colab-in-google-ai-plans.md).

## Make extra machines execute work

Move work through Git, never by copying live worktrees or T3 state (Tobias, 2026-10-11). Commit and push all source state, using WIP branches for dirty work; put handoffs in the owning repos and the restart plan in CoS state. Start fresh threads on the destination. Copy only data Git cannot hold, as cold backups.

Keep a whole team's agents, worktrees, gates and caches on its chosen host when the harness supports separate environments. T3's [remote-access documentation](https://github.com/pingdotgg/t3code/blob/05e4f888a0d8591c790d036140080092cf024d30/docs/user/remote-access.md) describes this ownership and new-thread balancing, not gate reservations. Confirm installed capabilities before relying on upstream features.

Whole-gate offload needs a frozen complete input and a receipt binding its digest, environment, executed checks, exit status and artifacts. Live source synchronization plus an SSH exit code is insufficient. Durable job IDs, cancellation and idempotent submission prevent duplicate work after disconnects. Admission belongs to the executing host; verdict caches must distinguish qualified environments.

Shared compiler storage and distributed compilation are not distributed testing. [sccache's Rust restrictions](https://github.com/mozilla/sccache/blob/main/docs/Rust.md) include disabled incremental compilation and uncached linker-invoking crates. Benchmark the actual eligible invocation mix.

Choose the OS for the verdict it proves. Matching Rust versions does not make NixOS equivalent to Omarchy's native libraries and desktop. [Xvfb](https://www.x.org/releases/current/doc/man/man1/Xvfb.1.xhtml) is X11, not a Hyprland/Wayland test. Declarative provisioning and runtime qualification are separate requirements.

Wired 2.5GbE has a raw ceiling of 312.5 MB/s; 10GbE has 1,250 MB/s, before overhead. Faster NICs cannot defeat slower switches, disks or relay paths. Transfer source deltas and receipts, not entire hot targets on every gate.

## What makes a deal good

Use [hardware-deal-check](../skills/hardware-deal-check/SKILL.md) to find and assess offers delivered in Denmark; it owns Tobias's price ceilings, landed-cost and electricity arithmetic, evidence requirements and purchase-safety limits. [Shopping preferences](../tobias/shopping.md) owns general suitability.

Cheap enterprise hardware can lose on idle energy and noise. Separate new, refurbished and private-used baselines: a low purchase price alone proves neither a suitable machine nor a market discount.

Reject Macs for development. Consider a Mac as a CI box only when a project needs macOS verdicts. Apple Silicon's ARM VMs do not supply the required x86 Omarchy/Wayland and Windows environments.

See [the feedback-loop skill](../skills/theodore-kaczynski-nullifier/SKILL.md) for cache/watcher ownership and [the Windows VM note](../software/omarchy-windows-vm.md) for VM memory and lifecycle constraints.
