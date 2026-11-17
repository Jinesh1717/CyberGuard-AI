import time, re
from .config import ABSTAIN_PHRASE, MODEL_DIR, BACKEND
from .guardrails import validate_query, classify, should_abstain
from .retrieve import retrieve
from .llm import ExtractiveBackend, LlamaCppBackend
def parse_citations(text, count): return sorted({int(x) for x in re.findall(r"\[(\d+)\]", text) if 1 <= int(x) <= count})
def ask(question, top_k=5):
    start=time.perf_counter(); q=validate_query(question); refusal=classify(q)
    if refusal: return {"answer":refusal,"citations":[],"retrieved":[],"abstained":True,"backend":BACKEND,"latency":0}
    results=retrieve(q, top_k)
    if should_abstain(results): return {"answer":ABSTAIN_PHRASE+" Try asking about phishing, passwords, MFA, updates, or reporting.","citations":[],"retrieved":results,"abstained":True,"backend":BACKEND,"latency":time.perf_counter()-start}
    backend=ExtractiveBackend()
    model=next(MODEL_DIR.glob("*.gguf"), None)
    if BACKEND=="llama_cpp" and model:
        try: backend=LlamaCppBackend(str(model))
        except Exception: pass
    text=backend.answer(q, results); citations=parse_citations(text,len(results))
    return {"answer":text,"citations":[results[i-1] for i in citations],"retrieved":results,"abstained":text.startswith(ABSTAIN_PHRASE),"backend":backend.name,"latency":time.perf_counter()-start}
