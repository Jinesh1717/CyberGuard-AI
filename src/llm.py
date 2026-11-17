from .config import ABSTAIN_PHRASE
class ExtractiveBackend:
    name="extractive"
    def answer(self, question, passages):
        sentences=[]
        for p in passages[:3]:
            s=p["text"].split(". ")[0].strip()
            if s: sentences.append(f"{s}. [{passages.index(p)+1}]")
        return " ".join(sentences) if sentences else ABSTAIN_PHRASE
class LlamaCppBackend(ExtractiveBackend):
    name="llama_cpp"
    def __init__(self, model_path):
        from llama_cpp import Llama
        self.llm=Llama(model_path=model_path, n_ctx=4096, verbose=False)
    def answer(self, question, passages):
        context="\n".join(f"[{i+1}] {p['text']}" for i,p in enumerate(passages))
        prompt=f"Answer only from the passages. Cite every claim with [n]. If unsupported, say {ABSTAIN_PHRASE}.\nPassages:\n{context}\nQuestion: {question}"
        return self.llm(prompt, max_tokens=300, temperature=.1)["choices"][0]["text"].strip()
