# OpenRouter routing and pricing

Checked 2026-10-24 on DeepSeek V4.1 Flash 1017 with direct API probes; the routing rules are general, the prices are volatile.

recheck-after: 2026-11-24

## Prices

- **Listed prices already include provider discounts.** `pricing.discount: 0.82` beside $0.054 means $0.30 list, 82% off, charged now. Promotions end without notice.
- **Effective input** on the provider page is (1 − hit rate) × input + hit rate × cache read, over all customers' traffic. Agent traffic runs 90–97% cache hits, so it is far below the input price. Rank providers on your own token mix (uncached input, cache read, output from Pi session usage), not on effective input or headline input.
- **Cache-read price varies 30× between providers** (Reka charges input price for cache reads; DeepInfra $0.003). With agent workloads, cache read and output decide the bill.
- **Each snapshot is a separate model ID** with separate provider prices and promotions (`deepseek-v4.1-flash` vs `deepseek-v4.1-flash-1017`).
- **Direct is not reliably cheaper.** Several providers list lower prices on OpenRouter than on their own sites (DigitalOcean, Cloudflare, inference.net, Relace); some match (Together, Baseten, DeepInfra, Fireworks standard). Fireworks Spot exists only on OpenRouter. OpenRouter adds a fee when buying credits; BYOK is fee-free up to $25,000/month on pay-as-you-go and BYOK endpoints are tried first.
- **Account guardrails filter `/api/v1/models/user`.** Allowing one model makes key-scoped catalogs (Pi's included) list only that model.

## Routing

- **`sort: "price"` ranks by input price only.** Four controlled pairs: output and cache-read prices were ignored every time. Exclude providers whose cache read is expensive or whose cache hit rate is poor with `ignore`, so input order matches real cost.
- **`preferred_min_throughput` / `preferred_max_latency` barely act without a sort.** With `sort`, providers below the floors (rolling 5-minute p50) move to the end. Floors + `sort: "price"` = cheapest provider that is fast enough.
- **Default routing** weighs cache-adjusted effective price, TTFT, errors, 429s and end-to-end speed ([provider docs](https://openrouter.ai/docs/guides/providers/traffic-routing); the routing guide's "inverse square of price" is stale) and keeps exploration traffic on weak endpoints. Measured: 20 sessions landed on 14 providers, median 97 tps against 279 tps for floors + price.
- **Sticky routing** pins a conversation to one provider after a cache hit, or from the first request when `session_id` / `x-session-id` is sent; expires after 10 minutes idle. **`provider.order` disables it.** Verified: five sessions each stayed on one provider with ~99% cached prompt tokens on later turns. The cache is shared across sessions on the same provider.
- **`zdr: true`** limits routing to zero-retention endpoints; per-endpoint `dataPolicy` (training, retainsPrompts) is in the provider page data. DeepSeek's own endpoint trains on prompts.
- **Quantization labels are self-reported.** DeepSeek V4/V4.1 ship MXFP4 experts with FP8 elsewhere; `fp8` endpoints serve the experts losslessly upcast, `mxfp4` matches the shipped expert format, plain `fp4` is ambiguous.
- **Speed stats need an API key.** `/api/v1/models/<id>/endpoints` returns `throughput_last_30m` and `latency_last_30m` at p50/p75/p90/p99 (no p95) only when authenticated; unauthenticated they are null. Throughput percentiles count from the fast end, so p90 is the slow tail. p90 throughput ran about half of p50 on nearly every endpoint, so p50 floors already exclude the bad tails; p90 adds noise on low-volume endpoints.
- **Routing cannot depend on thinking level.** Pi sends its thinking level as `reasoning.effort` on the same model ID; every DeepSeek V4.1 endpoint lists `reasoning_effort`, so `require_parameters` filters nothing, and speed stats have only one `text_generation` workload.

See also: [coding models](../agents/coding-models.md), [Pi operations](../agents/pi-operations.md), [uncensored model hosting](uncensored-model-hosting.md).
