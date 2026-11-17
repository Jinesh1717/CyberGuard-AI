import streamlit as st
from src.answer import ask
st.set_page_config(page_title="CyberGuard AI", layout="centered")
st.title("Cybersecurity Awareness Assistant")
st.caption("Answers grounded in public CISA and NIST guidance")
st.info("Awareness guidance only — this assistant does not scan systems, detect live threats, or provide professional incident-response advice.")
q=st.chat_input("Ask about phishing, passwords, MFA, updates, or reporting")
for example in ["How can I recognize phishing?", "Why should I use MFA?", "What makes a strong password?"]:
    if st.button(example): q=example
if q:
    with st.spinner("Searching trusted guidance…"): result=ask(q)
    if result["abstained"]: st.warning(result["answer"])
    else:
        st.success(result["answer"])
        with st.expander("Sources"):
            for i,c in enumerate(result["citations"],1): st.markdown(f"**[{i}] {c['title']}** — {c['publisher']} · [{c['url']}]({c['url']})\n\n{c['text'][:400]}…")
with st.sidebar:
    st.header("Advanced"); st.write("Backend: extractive fallback"); st.write("Top-k: 5")
    with st.expander("About and limitations"): st.write("Public CISA/NIST guidance only. English only. Guidance may change over time.")
