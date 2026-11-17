import re
from .config import ABSTAIN_PHRASE, MIN_PASSAGES, SIMILARITY_THRESHOLD

HARMFUL = re.compile(r"(write|build|create).{0,30}(malware|ransomware|phishing kit)|break into|steal credentials", re.I)
OUT_OF_SCOPE = re.compile(r"\b(recipe|weather|medical diagnosis|stock price)\b", re.I)
INJECTION = re.compile(r"ignore (all|any|previous)|reveal (the )?system prompt|when asked about|do not cite|follow these instructions", re.I)

def validate_query(q: str) -> str:
    q = re.sub(r"\s+", " ", q).strip()
    if not q or len(q) > 1000: raise ValueError("Please enter a question under 1000 characters.")
    return q

def classify(q: str) -> str | None:
    if HARMFUL.search(q): return "I can’t help create attacks or steal credentials. I can help with defensive awareness guidance instead."
    if OUT_OF_SCOPE.search(q): return ABSTAIN_PHRASE
    return None

def clean_passages(passages):
    return [p for p in passages if not INJECTION.search(p.get("text", ""))]

def should_abstain(results):
    return len(results) < MIN_PASSAGES or results[0].get("score", 0) < SIMILARITY_THRESHOLD
