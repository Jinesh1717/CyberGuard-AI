import re, json
from pathlib import Path
from .config import CHUNK_SIZE, PROCESSED_DIR

def chunk_text(doc, size=CHUNK_SIZE):
    words = re.findall(r"\S+", doc["text"])
    out=[]
    for i in range(0, len(words), max(1, int(size*.88))):
        text=" ".join(words[i:i+size]).strip()
        if len(text.split()) >= 20:
            out.append({**{k:doc.get(k,"") for k in ("doc_id","title","publisher","url","page_or_section")}, "chunk_id": f"{doc['doc_id']}-{len(out):04d}", "text":text})
    return out

def build_chunks(documents):
    seen=set(); result=[]
    for d in documents:
        for c in chunk_text(d):
            key=re.sub(r"\W+", " ", c["text"].lower()).strip()
            if key not in seen: seen.add(key); result.append(c)
    return result

def save_chunks(chunks, path=PROCESSED_DIR/"chunks.jsonl"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(c) for c in chunks), encoding="utf-8")
