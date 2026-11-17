import json, numpy as np
from .config import INDEX_DIR, PROCESSED_DIR
try:
 import faiss
 from sentence_transformers import SentenceTransformer
except ImportError: faiss=None

def build():
    chunks=[json.loads(x) for x in (PROCESSED_DIR/"chunks.jsonl").read_text(encoding="utf-8").splitlines()]
    INDEX_DIR.mkdir(exist_ok=True)
    if faiss is None:
        (INDEX_DIR/"metadata.json").write_text(json.dumps(chunks), encoding="utf-8")
        (INDEX_DIR/"offline.json").write_text("true", encoding="utf-8")
        return
    model=SentenceTransformer("all-MiniLM-L6-v2"); vec=model.encode([c["text"] for c in chunks], normalize_embeddings=True)
    index=faiss.IndexFlatIP(vec.shape[1]); index.add(np.asarray(vec, dtype="float32")); INDEX_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_DIR/"index.faiss")); (INDEX_DIR/"metadata.json").write_text(json.dumps(chunks), encoding="utf-8")
if __name__ == "__main__": build()
