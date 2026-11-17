import json, logging, requests, yaml
from bs4 import BeautifulSoup
from .config import MANIFEST, PROCESSED_DIR
from .chunk import build_chunks, save_chunks
logging.basicConfig(level=logging.INFO)

def download_docs():
    docs=[]
    for s in yaml.safe_load(MANIFEST.read_text(encoding="utf-8")):
        try:
            html=requests.get(s["url"], timeout=20, headers={"User-Agent":"CyberGuard-AI research client"}).text
            soup=BeautifulSoup(html, "html.parser")
            for x in soup(["script","style","nav","footer"]): x.decompose()
            text="\n".join(x.strip() for x in soup.get_text("\n").splitlines() if x.strip())
            docs.append({"doc_id":s["id"],"title":s["title"],"publisher":s["publisher"],"url":s["url"],"page_or_section":"HTML page","text":text})
            logging.info("Downloaded %s (%d words)", s["id"], len(text.split()))
        except Exception as e: logging.warning("Skipped %s: %s. Download it manually into data/raw.", s["id"], e)
    return docs

if __name__ == "__main__":
    docs=download_docs(); (PROCESSED_DIR/"documents.jsonl").parent.mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR/"documents.jsonl").write_text("\n".join(json.dumps(x) for x in docs), encoding="utf-8")
    save_chunks(build_chunks(docs)); print(f"Indexed source documents: {len(docs)}")
