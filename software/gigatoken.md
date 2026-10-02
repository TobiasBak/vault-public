# Gigatoken

[Gigatoken](https://github.com/marcelroed/gigatoken) (MIT, Rust with Python bindings, announced 2026-07-21) runs existing Hugging Face and `tiktoken` tokenizer definitions much faster. It suits bulk dataset preprocessing; it's not a new tokenizer.

**Why it's fast:**
- SIMD state machines replace pretokenization regexes
- a cache reuses encodings of repeated pre-tokens
- parallel workers barely interact
- the native API reads and splits files in Rust, so large Python objects never cross the boundary

**Claims:** the author reports roughly 500–1000× Hugging Face Tokenizers and about 100× `tiktoken` for many BPE tokenizers, with GPT-2 at 6–9 GB/s on consumer CPUs and 24.5 GB/s on a 144-core EPYC. Gains are largest with the native API on large repetitive corpora and much smaller in compatibility mode, on small inputs, and for SentencePiece. It doesn't help when inference dominates.

**Limits (initial release):** beta, Python ≥ 3.10, no WordPiece, weakly optimized SentencePiece, barely tested on Windows (use WSL). Unusual tokenizers may mismatch, so validate first.

```python
import gigatoken as gt
tok = gt.Tokenizer("Qwen/Qwen3-8B")
tokens = tok.encode_files(gt.TextFileSource(["data.txt"], separator=b"<|endoftext|>"))
```

Install with `uv add gigatoken`. Run `uv run gigatoken bench --validate` on representative data to check throughput and output agreement.
