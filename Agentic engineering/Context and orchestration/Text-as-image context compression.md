# Text-as-image context compression

> [!warning] Cautionary hypothesis
> Rendering text as images may reduce metered input tokens, but it is unverified locally and is not a safe general context policy.

Visual text is lossy, model-specific [[Agent context engineering|context compression]]. A favorable image-token count does not establish lower cost per successful task. Legibility limits, image upload and vision latency, rendering work, reduced prompt-cache reuse, retries, and exact-source recovery can erase the apparent saving.

Keep instructions, role boundaries, tool protocols, code, commands, paths, identifiers, numbers, and machine-readable data as text. Moving control information into pixels can weaken instruction hierarchy or break tool semantics. Image rendering also does not neutralize prompt injection.

Eligible material, if any, is long read-only reference text whose task can tolerate visual decoding. Preserve the unchanged original outside active context under a stable path, range, or artifact identity. The model must be able to retrieve exact text whenever punctuation, ordering, quotation, or transcription matters. Visual summaries and pages should augment retrieval, never become the only copy.

Likely failures include OCR-like substitutions, lost indentation and punctuation, errors across page boundaries, poor performance on small fonts or unfamiliar scripts, and weaker debugging because images are harder to search, diff, quote, redact, and inspect. Deterministic rendering and caching may reduce repeated work but do not remove these risks.

Treat density and benefit as specific to the model, task, and provider accounting. Prefer ordinary text, retrieval, and textual compaction unless repeated representative trials show equal correctness and lower total latency and cost per successful task. A single dense screenshot or token estimate is not sufficient evidence.
