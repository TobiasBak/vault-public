# Gigatoken

[Gigatoken](https://github.com/marcelroed/gigatoken) is an MIT-licensed Rust implementation of existing language-model tokenizers, with Python bindings. Marcel Rød publicly announced it on 21 July 2026. It is not a new tokenization algorithm, vocabulary, or token format: it executes established Hugging Face and `tiktoken` tokenizer definitions much faster, especially for bulk dataset preprocessing.

## Why it is fast

- Specialized SIMD state machines replace the general-purpose regular expressions commonly used for pretokenization.
- A cache hierarchy reuses the encoded tokens for repeated pre-token strings such as words.
- Parallel workers interact minimally, while the native API lets Rust read and split files directly instead of moving large Python objects across the language boundary.
- It has optimized paths for many common BPE families on modern x86 and ARM CPUs.

Gigatoken can wrap Hugging Face Tokenizers and `tiktoken` for easier adoption. Its own file-oriented API is faster because it avoids compatibility and Python overhead:

```python
import gigatoken as gt

tokenizer = gt.Tokenizer("Qwen/Qwen3-8B")
source = gt.TextFileSource(["data.txt"], separator=b"<|endoftext|>")
tokens = tokenizer.encode_files(source)
```

## Interpreting the performance claims

The author reports roughly 500-1000x higher throughput than Hugging Face Tokenizers and around 100x higher throughput than `tiktoken` for many BPE tokenizers. Reported GPT-2 throughput ranges from about 6-9 GB/s on high-end consumer CPUs to 24.5 GB/s on a dual-socket 144-core EPYC system. The benchmark validates sampled output against the comparison implementation.

These are impressive but author-supplied bulk-throughput results, not a universal latency comparison. Speedups vary greatly by tokenizer family and hardware. They are largest when using the native API over large, repetitive corpora; compatibility mode and small interactive inputs retain more overhead. SentencePiece tokenizers currently see much smaller gains. Gigatoken accelerates tokenization and dataset preparation, not model inference itself, so it will have little effect when GPU inference or a remote model API dominates latency.

## Current limitations

As of the initial public release:

- The package is marked beta and requires Python 3.10 or newer.
- WordPiece is unsupported.
- SentencePiece support is substantially less optimized than BPE support.
- Windows has received little testing; WSL is recommended.
- Exact compatibility has a performance cost, and unusual tokenizer definitions may expose mismatches that should be validated before processing a full corpus.

Add it to a uv project with `uv add gigatoken`. Run `gigatoken bench` through `uv run` with `--validate` to check throughput and output agreement for a chosen Hugging Face tokenizer and representative local data.

## Sources

- [Repository and benchmark methodology](https://github.com/marcelroed/gigatoken)
- [PyPI package](https://pypi.org/project/gigatoken/)
- [Initial announcement, 21 July 2026](https://x.com/marcelroed/status/2079642154960564352)
