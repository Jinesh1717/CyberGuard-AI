import json, numpy as np
from .config import INDEX_DIR, TOP_K
from .guardrails import clean_passages
def retrieve(query, top_k=TOP_K):
    if (INDEX_DIR/"offline.json").exists():
        import re
        q=set(re.findall(r"\w+", query.lower()))
        meta=json.loads((INDEX_DIR/"metadata.json").read_text(encoding="utf-8"))
        scored=[]
        for p in meta:
            words=set(re.findall(r"\w+", p["text"].lower()))
            score=len(q & words) / max(1, len(q))
            scored.append({**p, "score": score})
        return clean_passages(sorted(scored, key=lambda x:x["score"], reverse=True)[:top_k])
    import faiss
    from sentence_transformers import SentenceTransformer
    idx=faiss.read_index(str(INDEX_DIR/"index.faiss")); meta=json.loads((INDEX_DIR/"metadata.json").read_text(encoding="utf-8")); model=SentenceTransformer("all-MiniLM-L6-v2")
    scores, ids=idx.search(np.asarray(model.encode([query], normalize_embeddings=True), dtype="float32"), top_k)
    return clean_passages([{**meta[i],"score":float(scores[0][n])} for n,i in enumerate(ids[0]) if i >= 0])
