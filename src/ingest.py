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
    if not docs:
        docs = [
            {"doc_id":"fixture_phishing","title":"Cybersecurity Awareness Fixture: Phishing","publisher":"CISA/NIST fixture","url":"https://www.cisa.gov/secure-our-world/recognize-and-report-phishing","page_or_section":"Fixture guidance","text":"Phishing messages often create urgency, request sensitive information, or use suspicious links and unexpected attachments. Verify the sender through a trusted channel instead of clicking a suspicious link. Report suspected phishing through your organization’s process or the relevant service provider. If you clicked a suspicious link, disconnect if needed, notify your organization, change affected credentials, and report the incident."},
            {"doc_id":"fixture_passwords","title":"Cybersecurity Awareness Fixture: Passwords","publisher":"CISA/NIST fixture","url":"https://www.cisa.gov/secure-our-world/use-strong-passwords","page_or_section":"Fixture guidance","text":"Use long, unique passwords or passphrases for every account. A password manager can generate and store unique credentials. Reusing a password is risky because one compromised account can expose other accounts. Never share passwords or enter them into an untrusted page."},
            {"doc_id":"fixture_mfa","title":"Cybersecurity Awareness Fixture: Multifactor Authentication","publisher":"CISA/NIST fixture","url":"https://www.cisa.gov/secure-our-world/require-multifactor-authentication","page_or_section":"Fixture guidance","text":"Multifactor authentication adds protection by requiring two or more different types of evidence, such as something you know, have, or are. Enable MFA wherever it is available, especially for email, financial, and administrator accounts. Prefer phishing-resistant methods when available."},
            {"doc_id":"fixture_updates","title":"Cybersecurity Awareness Fixture: Software Updates","publisher":"CISA/NIST fixture","url":"https://www.cisa.gov/secure-our-world/keep-your-software-up-to-date","page_or_section":"Fixture guidance","text":"Install software and operating system updates promptly, preferably with automatic updates enabled. Updates often fix security weaknesses that attackers could exploit. Download updates from official sources and restart when required."}
        ]
        logging.warning("Using offline fallback corpus because no public sources could be downloaded.")
    return docs

if __name__ == "__main__":
    docs=download_docs(); (PROCESSED_DIR/"documents.jsonl").parent.mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR/"documents.jsonl").write_text("\n".join(json.dumps(x) for x in docs), encoding="utf-8")
    save_chunks(build_chunks(docs)); print(f"Indexed source documents: {len(docs)}")
