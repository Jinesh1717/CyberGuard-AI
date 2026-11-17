from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR, PROCESSED_DIR, INDEX_DIR, MODEL_DIR = (ROOT / x for x in ("data/raw", "data/processed", "index", "models"))
MANIFEST = ROOT / "data/sources.yaml"
CHUNK_SIZE = int(os.getenv("CYBER_CHUNK_SIZE", "280"))
TOP_K = int(os.getenv("CYBER_TOP_K", "5"))
SIMILARITY_THRESHOLD = float(os.getenv("CYBER_SIMILARITY_THRESHOLD", "0.15"))
MIN_PASSAGES = 1
ABSTAIN_PHRASE = "I couldn't find enough in the trusted sources to answer that confidently."
BACKEND = os.getenv("CYBER_LLM_BACKEND", "extractive")
