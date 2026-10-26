# Uncensored and abliterated model hosting

Checked 2026-10-26 against each provider's `/v1/models` and HF file listings; names and prices are volatile.

recheck-after: 2026-11-26

## The shape of the market

- **The checked generic hosts did not list an uncensored DeepSeek V4.1 variant on 2026-10-26.** OpenRouter, Chutes, Novita, DeepInfra, Atlas Cloud, inference.net, OrcaRouter and Parasail listed the base Flash model; Featherless hosted only the base V4.1 despite its large community catalog.
- **The uncensored builds found derive from the smaller model.** They use V4.1 Flash (763B MoE); no uncensored V4 Pro (1.6T) was found. Treat the listed "V4.1 uncensored" endpoints as Flash-class when reasoning about cost and capability.
- **The finetunes drop vision.** Abliterated V4.1 endpoints are `text->text` at 1M context with 64k output and tool calling intact; the base model accepts images.
- **Matching prices do not prove a shared upstream.** NanoGPT and Venice both charge $0.33/$1.32 per Mtok with $0.00825 cache reads for V4.1 Flash Uncensored, which is the base model's $0.30/$1.20 plus 10%. Verify model provenance separately before treating the endpoints as independent or identical.
- **Abliteration vendors exist as their own product.** Abliteration AI (api.abliteration.ai, $20/month including $20 usage credit) serves `abliterated-model-large-flash`, derived from V4.1 Flash 1017, at roughly four times the NanoGPT and Venice prices.
- **Hugging Face hosts the weights, not an endpoint.** No V4.1 uncensored repo carries an `inferenceProviderMapping`; HF Inference Providers cannot serve them. Dedicated Inference Endpoints (per-hour, any public repo) or a rented GPU are the only HF routes.
- **Chub AI cannot be evaluated from Denmark:** its model API answers 403 "not available in your country".

## Where it runs, 2026-10-26

| Route | Model | Price per Mtok in / cached / out |
| --- | --- | --- |
| NanoGPT | `deepseek/deepseek-v4.1-flash-uncensored` (+`:thinking`) | 0.33 / 0.00825 / 1.32 |
| Venice | `deepseek-v4-1-flash-uncensored` | 0.33 / 0.00825 / 1.32 |
| Abliteration AI | `abliterated-model-large-flash` | 1.25 / 0.125 / 2.50 (plus $20/month) |

Abliteration AI includes a policy gateway, per-project keys and audit logging. Compare these features and verify model provenance before paying the premium.

## Self-host sizing

Weights for V4.1 Flash are 763B; the uncensored FP8 build `dealignai/DeepSeek-V4.1-Flash-UNCENSORED-FP8` is 510 GB, and community GGUFs run ~250 GB (IQ1_M), ~340 GB (Q2_K) and ~224 GB (OrcaRouter's "Mix-128G", gated). Vast.ai quoted 4×H200 (562 GB VRAM, $17.37/hr) and 8×H200 (1123 GB, $34.74/hr) on 2026-10-26. Weights alone fit in those capacities, but runtime and context need additional headroom. Compare measured throughput, utilization and quality with hosted pricing before choosing self-hosting.

## Checking this class of question

Fetch `/v1/models` from each candidate and grep; catalog pages and search results lag by weeks and hide geo-blocks. Hugging Face's `search` endpoint answers which variants exist and how large they are, and `?expand[]=inferenceProviderMapping` answers whether anyone serves them.

See also: [OpenRouter routing and pricing](openrouter.md), [coding models](../agents/coding-models.md).
