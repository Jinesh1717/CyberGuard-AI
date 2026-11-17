# GEN-07 Cybersecurity Awareness Assistant (CyberGuard AI)

A reproducible, grounded RAG demo for cybersecurity awareness questions. It uses public CISA/NIST guidance, FAISS retrieval, and either a local llama.cpp model or a citation-preserving extractive fallback.

## Architecture

```text
CISA/NIST manifest -> download/extract -> section-aware chunks -> embeddings/FAISS
                                                           -> retrieve -> evidence gate
                                                           -> llama.cpp or extractive answer -> citations
```

All generated claims must be supported by retrieved passages. Low-confidence, out-of-scope, harmful, and unsupported questions abstain. This project does not scan systems, detect live threats, or provide legal/incident-response advice.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m src.ingest
python -m src.embed_index
streamlit run app/streamlit_app.py
```

For a fully offline smoke test, the test suite uses a tiny fixture corpus. To use generation, place a compatible Gemma 3 4B instruct GGUF (Q4_K_M) in `models/` and set `CYBER_LLM_BACKEND=llama_cpp`; without it the app uses `extractive` mode.

## Sources

The manifest contains only public CISA and NIST sources. Each downloaded document records URL and retrieval date. Network availability can affect which documents are indexed; run `python -m src.ingest` to see the exact result.

## Commands

`make ingest`, `make index`, `make test`, `make eval`, `make security`, `make app`.

## Limitations

Small English-only knowledge base; guidance changes over time; local models can still make mistakes; extraction mode is not LLM generation; no live threat detection, vulnerability scanning, or professional advice.
