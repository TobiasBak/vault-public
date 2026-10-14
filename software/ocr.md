# OCR engines

## Indra OCR

Consider Datalab's **Indra OCR** for high-volume CPU document intake from clean printed scans or PDFs when line boxes, layout blocks and reading order matter. Benchmark it on representative documents before adopting it. Avoid it for handwriting, degraded scans or complex tables, and clear the model license before commercial use.

Primary sources checked **2026-10-14**: [launch post, 2026-10-13](https://www.datalab.to/blog/indra-ocr), [code repository](https://github.com/datalab-to/indra), [model card and weights](https://huggingface.co/datalab-to/indra-ocr).

- The main recognizer, `rec.onnx`, has about 1M parameters, not the entire layout pipeline. The default model bundle is about 18 MB. Outputs include Markdown, text and JSON with line and layout-block bounding boxes, block labels and reading order.
- Runs fully locally on CPU through ONNX Runtime, without PyTorch or a hosted API. Download weights once, then use `--model-dir` or `INDRA_OCR_MODEL_DIR` for offline operation. Default `auto` mode reads usable PDF text layers and OCRs missing content; `--mode ocr` forces recognition.
- Published OCR coverage: Latin, about 50 languages; Cyrillic; Greek; Devanagari; Bengali; simplified and traditional Chinese. The model card names English, French, German, Spanish, Italian, Portuguese, Dutch, Polish, Russian, Ukrainian, Greek, Hindi, Bengali and Chinese. Other scripts work only through digital PDF text layers, not scanned-image OCR. No vertical text.

### License verdict, checked 2026-10-14

Code is [Apache-2.0](https://github.com/datalab-to/indra/blob/661fb47ac332dce07f1ebc0d7b37ffe2361bd85b/LICENSE); weights use [AI Pubs Open RAIL-M, modified](https://huggingface.co/datalab-to/indra-ocr/blob/5993a956d7ea1d43c0d40d409962bb0b033ac1e8/LICENSE). **Commercial use is conditional, not unrestricted:**

- Attachment A bars use if you, your employer or affiliated entity exceeded **US$20M gross revenue in the prior year** or **US$20M total equity/debt funding from any source**. Personal use and research are exceptions to those two limits. The text says "more than", not "at least".
- Separately, it bars use for any purpose if that entity offers any product or service competing with any product or service of Datalab or its affiliates. This is broader than the README's shorthand about competing with its API; no personal/research exception is stated for this clause.
- Sections 4–8 impose downstream use restrictions, license/notice retention, attribution including for outputs, and share-alike explicitly covering outputs and their derivatives as well as model derivatives. Being below both financial thresholds is not enough on its own. Obtain a separate Datalab commercial license if these terms do not fit.

### Vendor benchmark, published 2026-10-13

These are **Datalab-run results on its own [OmniParseBench](https://www.datalab.to/blog/why-we-built-omniparsebench)**, not independent measurements:

- **Throughput:** same 300 pages on one x86 AMD EPYC machine, no GPU, 32 cores, one single-threaded worker process per core, OCR mode, otherwise default settings: Indra **49.4 pages/s**, PaddleOCR PP-OCRv6 small via RapidOCR **4.28**, Tesseract 5 **2.92**, PP-StructureV3 **≤0.18**. Indra is the mean of three runs; competitors ran once. PP-StructureV3 used a time-capped subset, so its figure is an upper bound. Model loading and one warm-up page per worker are excluded; including loading, a 300-page Indra job achieved **37.7 pages/s**.
- **`--math`:** about **30 pages/s** on 32 cores, from a separate container on the same CPU type and pages: **29.2** versus **44.9** without math there, not a paired comparison with 49.4.
- **Text score:** on all 2,937 pages, 4 x86 vCPUs per engine, one page at a time, default settings: Indra auto mode **41.3**, PP-OCRv6 small **35.8**, Tesseract 5 with Latin model **19.3**. Indra's OCR-only score is **33.5**; the 41.3 result includes PDF text-layer extraction and is not a scanned-only accuracy claim.

Unverified locally: runtime behavior, language quality and benchmark reproducibility. The primary sources substantiate the published claims, not performance on a particular intake workload.
