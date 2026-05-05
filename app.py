import streamlit as st
import pypdf
import numpy as np
import os
import re
import ast
import json
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
  --bg:        #07080f;
  --surface:   #0d0f1a;
  --surface2:  #131625;
  --surface3:  #1a1d30;
  --border:    #1e2235;
  --border2:   #252840;
  --text:      #dde1f0;
  --muted:     #5a6080;
  --faint:     #1e2235;
  --accent:    #00c9a7;
  --accent2:   #00e8c3;
  --accent-dim:#003d32;
  --gold:      #f5a623;
  --red:       #ff6b6b;
  --blue:      #4f9eff;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: var(--bg) !important;
  color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: var(--bg) !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
  width: 290px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stFileUploader label { display: none !important; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  background: var(--surface2) !important;
  border: 1.5px dashed var(--border2) !important;
  border-radius: 12px !important;
  padding: 14px !important;
  transition: all 0.2s;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--accent) !important;
  background: rgba(0,201,167,0.04) !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] p {
  color: var(--muted) !important; font-size: 11px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
  background: var(--surface3) !important;
  border: 1px solid var(--border2) !important;
  color: var(--accent) !important;
  border-radius: 8px !important;
  font-size: 11px !important;
}
[data-testid="stSidebar"] .stRadio label { font-size: 12px !important; }
[data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] { display: none !important; }
[data-testid="stSidebar"] .stTextInput input {
  background: var(--surface2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  font-size: 12px !important;
  font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(0,201,167,0.15) !important;
}
[data-testid="stSidebar"] .stTextInput label { display: none !important; }
[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--muted) !important;
  border-radius: 8px !important;
  width: 100% !important;
  font-size: 11px !important;
  padding: 5px 10px !important;
  transition: all 0.15s !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  border-color: var(--red) !important;
  color: var(--red) !important;
}

/* ── Sidebar blocks ── */
.sb-logo {
  padding: 18px 16px 14px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sb-brand {
  display: flex; align-items: center; gap: 9px;
}
.sb-icon {
  width: 30px; height: 30px;
  background: linear-gradient(135deg, var(--accent), #007a66);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
}
.sb-name {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 15px;
  color: var(--text) !important;
  letter-spacing: -0.5px;
}
.sb-tag {
  font-size: 9px;
  font-family: 'JetBrains Mono', monospace;
  color: var(--accent) !important;
  background: rgba(0,201,167,0.1);
  border: 1px solid rgba(0,201,167,0.2);
  border-radius: 4px;
  padding: 2px 6px;
  letter-spacing: 0.5px;
}
.sb-sec {
  padding: 14px 14px 0;
}
.sb-sec-label {
  font-size: 9px !important;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--muted) !important;
  font-weight: 700;
  margin-bottom: 8px;
  display: block;
}
.sb-divider { height: 1px; background: var(--border); margin: 14px 0 0; }

/* ── Provider toggle ── */
.provider-bar {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 4px;
}
.provider-btn {
  padding: 7px 10px;
  border-radius: 7px;
  font-size: 11px;
  font-weight: 600;
  text-align: center;
  cursor: pointer;
  transition: all 0.15s;
  color: var(--muted) !important;
}
.provider-btn.active {
  background: var(--accent-dim);
  color: var(--accent) !important;
  border: 1px solid rgba(0,201,167,0.3);
}

/* ── Doc cards ── */
.doc-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 11px;
  padding: 10px 12px;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
}
.doc-card.active { border-color: rgba(0,201,167,0.4); background: rgba(0,201,167,0.04); }
.doc-card-icon {
  width: 30px; height: 30px;
  background: rgba(0,201,167,0.1);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; flex-shrink: 0;
}
.doc-card-info { flex: 1; min-width: 0; }
.doc-card-name {
  font-size: 11px; font-weight: 600;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  color: var(--text) !important;
}
.doc-card-meta { font-size: 9px; color: var(--muted) !important; margin-top: 2px; }
.doc-badge {
  font-size: 8px; font-family: 'JetBrains Mono', monospace;
  background: rgba(0,201,167,0.1);
  color: var(--accent) !important;
  padding: 2px 5px; border-radius: 3px;
  border: 1px solid rgba(0,201,167,0.2);
}

/* ── Stats row ── */
.stats-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5px; margin-top: 8px; }
.stat-box {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 9px;
  padding: 8px 6px;
  text-align: center;
}
.stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px; font-weight: 700;
  color: var(--accent) !important; line-height: 1;
}
.stat-key { font-size: 8px; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3px; }

/* ── Main ── */
.main-wrap { max-width: 760px; margin: 0 auto; padding: 44px 24px 140px; }

/* ── Hero ── */
.hero { padding: 20px 0 52px; }
.hero-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--accent) !important;
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 24px;
}
.hero-eyebrow::before {
  content: '';
  width: 24px; height: 1px;
  background: var(--accent);
  display: inline-block;
}
.hero-title {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 56px; font-weight: 800;
  line-height: 1.0; letter-spacing: -3px;
  color: var(--text); margin-bottom: 20px;
}
.hero-title .dim { color: var(--muted); font-weight: 300; }
.hero-title .hl {
  background: linear-gradient(90deg, var(--accent2), var(--blue));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 15px; color: var(--muted); line-height: 1.8;
  max-width: 400px; font-weight: 400; margin-bottom: 40px;
}
.step-cards { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; max-width: 460px; }
.step-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px; padding: 16px 14px;
  transition: border-color 0.2s;
}
.step-card:hover { border-color: var(--border2); }
.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; color: var(--accent) !important;
  letter-spacing: 1px; margin-bottom: 10px;
}
.step-title { font-size: 13px; font-weight: 700; color: var(--text); margin-bottom: 4px; }
.step-desc { font-size: 11px; color: var(--muted); line-height: 1.5; }

/* ── Summary box ── */
.summary-box {
  background: var(--surface);
  border: 1px solid rgba(0,201,167,0.2);
  border-radius: 14px;
  padding: 18px 20px;
  margin-bottom: 28px;
  position: relative;
}
.summary-box::before {
  content: '';
  position: absolute; left: 0; top: 16px; bottom: 16px;
  width: 3px; background: var(--accent); border-radius: 0 2px 2px 0;
}
.summary-title {
  font-size: 10px; font-family: 'JetBrains Mono', monospace;
  color: var(--accent) !important; letter-spacing: 1.5px;
  text-transform: uppercase; margin-bottom: 10px;
  display: flex; align-items: center; gap: 7px;
}
.summary-content { font-size: 13px; color: var(--text); line-height: 1.7; }

/* ── Suggestions ── */
.sugg-header {
  font-size: 10px; font-family: 'JetBrains Mono', monospace;
  color: var(--muted); letter-spacing: 1.5px; text-transform: uppercase;
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 12px;
}
.sugg-header::after { content: ''; flex: 1; height: 1px; background: var(--border); }

.stButton > button {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  color: var(--muted) !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
  font-size: 12px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  text-align: left !important;
  width: 100% !important;
  line-height: 1.5 !important;
  height: auto !important;
  white-space: normal !important;
  transition: all 0.15s !important;
}
.stButton > button:hover {
  background: var(--surface2) !important;
  border-color: var(--accent) !important;
  color: var(--text) !important;
  transform: translateY(-1px) !important;
}

/* ── Chat ── */
.chat-wrap { display: flex; flex-direction: column; gap: 0; }
@keyframes rise {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.msg-row-user {
  display: flex; justify-content: flex-end; gap: 10px; align-items: flex-end;
  animation: rise 0.22s ease; margin-bottom: 8px;
}
.msg-row-ai {
  display: flex; justify-content: flex-start; gap: 10px; align-items: flex-start;
  animation: rise 0.22s ease; margin-bottom: 6px;
}
.bubble-user {
  background: linear-gradient(135deg, #007a66, var(--accent));
  color: #fff;
  padding: 12px 18px;
  border-radius: 18px 18px 4px 18px;
  font-size: 14px; line-height: 1.65; max-width: 70%;
  font-weight: 500;
}
.bubble-ai {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 16px 20px;
  border-radius: 4px 18px 18px 18px;
  font-size: 14px; line-height: 1.8; max-width: 82%;
}
.av {
  width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; flex-shrink: 0;
}
.av-ai  { background: var(--surface2); border: 1px solid var(--border2); }
.av-usr {
  background: linear-gradient(135deg, #007a66, var(--accent));
  color: white; font-size: 11px; font-weight: 700;
}

/* ── Citation cards ── */
.citations-row {
  display: flex; flex-wrap: wrap; gap: 6px;
  margin-left: 40px; margin-bottom: 24px;
  animation: rise 0.3s ease;
}
.cite-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 5px 10px;
  font-size: 10px;
  font-family: 'JetBrains Mono', monospace;
  color: var(--muted) !important;
  display: flex; align-items: center; gap: 5px;
}
.cite-card .cite-page {
  color: var(--accent) !important;
  font-weight: 700;
}
.cite-card .cite-doc {
  color: var(--muted) !important;
  max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.cite-score {
  background: rgba(0,201,167,0.1);
  color: var(--accent) !important;
  padding: 1px 5px; border-radius: 3px; font-size: 9px;
}

/* ── Export button ── */
.export-btn {
  font-size: 10px; font-family: 'JetBrains Mono', monospace;
  color: var(--muted) !important; cursor: pointer;
  text-decoration: underline; text-underline-offset: 3px;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
  background: var(--surface) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 14px !important;
  box-shadow: 0 0 0 1px var(--border) !important;
}
[data-testid="stChatInput"] textarea {
  background: var(--surface) !important;
  border: none !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 14px !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }
[data-testid="stChatInput"] button {
  background: var(--accent) !important;
  border-radius: 10px !important;
}

/* ── Misc ── */
.stSpinner > div { border-top-color: var(--accent) !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }
[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
[data-testid="stExpander"] summary { color: var(--muted) !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ── Model loading (cached) ────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')


# ── PDF helpers ───────────────────────────────────────────────────────────────
def extract_pdf(file, doc_name: str):
    file.seek(0)
    reader = pypdf.PdfReader(file)
    chunks = []
    full_text = ""
    CHUNK_SIZE, OVERLAP = 280, 55

    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"
        words = page_text.split()
        start = 0
        while start < len(words):
            chunk_text = " ".join(words[start: start + CHUNK_SIZE])
            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "page": page_idx + 1,
                    "doc": doc_name,
                })
            start += CHUNK_SIZE - OVERLAP

    meta = {
        "pages": len(reader.pages),
        "words": len(full_text.split()),
        "chunks": len(chunks),
        "full_text": full_text[:5000],
    }
    return chunks, meta


# ── Embeddings ────────────────────────────────────────────────────────────────
def embed_chunks(chunks):
    model = load_embedder()
    texts = [c["text"] for c in chunks]
    return model.encode(texts, show_progress_bar=False, batch_size=32)


def semantic_search(query: str, all_chunks, all_embeddings, k=5, doc_filter=None):
    from sklearn.metrics.pairwise import cosine_similarity
    if all_embeddings is None or len(all_chunks) == 0:
        return []
    model = load_embedder()
    q_emb = model.encode([query])

    if doc_filter:
        indices = [i for i, c in enumerate(all_chunks) if c["doc"] in doc_filter]
    else:
        indices = list(range(len(all_chunks)))

    if not indices:
        return []

    filtered_embs = all_embeddings[indices]
    scores = cosine_similarity(q_emb, filtered_embs)[0]
    top_local = np.argsort(scores)[::-1][:k]

    results = []
    for local_idx in top_local:
        global_idx = indices[local_idx]
        results.append({
            "text": all_chunks[global_idx]["text"],
            "page": all_chunks[global_idx]["page"],
            "doc": all_chunks[global_idx]["doc"],
            "score": float(scores[local_idx]),
        })
    return results


# ── LLM helpers ───────────────────────────────────────────────────────────────
def _build_messages(system, user_msg, history):
    msgs = [{"role": "system", "content": system}]
    for h in history[-4:]:
        msgs.append({"role": "user",      "content": h["q"]})
        msgs.append({"role": "assistant", "content": h["a"]})
    msgs.append({"role": "user", "content": user_msg})
    return msgs


def call_groq(api_key: str, system: str, user_msg: str, history):
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=_build_messages(system, user_msg, history),
            max_tokens=1024, temperature=0.3,
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        err = str(e)
        if "429" in err: return "⚠️ Rate limit — wait a moment and retry."
        if "401" in err: return "⚠️ Invalid Groq API key. Check sidebar."
        return f"⚠️ Groq error: {err}"


def call_gemini(api_key: str, system: str, user_msg: str, history):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system,
        )
        hist = []
        for h in history[-4:]:
            hist.append({"role": "user",  "parts": [h["q"]]})
            hist.append({"role": "model", "parts": [h["a"]]})
        chat = model.start_chat(history=hist)
        return chat.send_message(user_msg).text
    except Exception as e:
        err = str(e)
        if "API_KEY" in err or "invalid" in err.lower():
            return "⚠️ Invalid Gemini API key. Check sidebar."
        return f"⚠️ Gemini error: {err}"


def call_llm(provider, keys, system, user_msg, history):
    if provider == "Groq":
        return call_groq(keys.get("groq", ""), system, user_msg, history)
    return call_gemini(keys.get("gemini", ""), system, user_msg, history)


# ── Core RAG answer ───────────────────────────────────────────────────────────
def get_answer(provider, keys, results, question, history):
    context_parts = []
    for r in results:
        score_pct = int(r["score"] * 100)
        context_parts.append(
            f"[Source: {r['doc']} | Page {r['page']} | Relevance: {score_pct}%]\n{r['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    system = (
        "You are Nexus, a precise AI document assistant.\n"
        "Rules:\n"
        "- Answer ONLY from the provided context. Never fabricate information.\n"
        "- If the answer is not in the context, say: 'This information is not available in the uploaded documents.'\n"
        "- Always cite the source page when referencing specific facts (e.g. 'According to Page 4...').\n"
        "- Use markdown formatting: **bold** for key terms, bullet lists for multi-point answers.\n"
        "- Be concise but complete."
    )
    user_msg = f"RETRIEVED CONTEXT:\n{context}\n\nQUESTION: {question}"
    return call_llm(provider, keys, system, user_msg, history)


# ── Auto summary ──────────────────────────────────────────────────────────────
def get_summary(provider, keys, full_text):
    system = "You are a document analyst. Be structured and concise."
    user_msg = (
        "Provide a structured document summary:\n\n"
        "**Main Topic:** (1 sentence)\n"
        "**Key Points:** (4 bullet points)\n"
        "**Important Data/Facts:** (3 bullet points)\n"
        "**Conclusion:** (1-2 sentences)\n\n"
        f"Document:\n{full_text[:4500]}"
    )
    return call_llm(provider, keys, system, user_msg, [])


# ── Suggested questions ───────────────────────────────────────────────────────
def get_suggestions(provider, keys, full_text):
    system = 'Output ONLY a Python list of 4 strings. No markdown, no explanation, no preamble.'
    user_msg = f'4 insightful questions for this document. Format exactly: ["Q1?","Q2?","Q3?","Q4?"]\n\n{full_text[:2500]}'
    raw = call_llm(provider, keys, system, user_msg, [])
    try:
        match = re.search(r'\[.*?\]', raw, re.DOTALL)
        if match:
            qs = ast.literal_eval(match.group())
            if isinstance(qs, list) and len(qs) >= 4:
                return qs[:4]
    except Exception:
        pass
    return [
        "What is the main topic of this document?",
        "What are the key findings or conclusions?",
        "What data or evidence is presented?",
        "What are the recommendations or next steps?",
    ]


# ── Chat export ───────────────────────────────────────────────────────────────
def build_export(history, doc_names):
    lines = [
        "NEXUS AI — CHAT EXPORT",
        "=" * 50,
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Documents: {', '.join(doc_names)}",
        "=" * 50,
        "",
    ]
    for i, turn in enumerate(history, 1):
        lines.append(f"Q{i}: {turn['q']}")
        lines.append(f"A{i}: {turn['a']}")
        if turn.get("citations"):
            cites = ", ".join(
                f"p.{c['page']} in '{c['doc']}' ({int(c['score']*100)}%)"
                for c in turn["citations"]
            )
            lines.append(f"Sources: {cites}")
        lines.append("")
    return "\n".join(lines)


# ── Session state ─────────────────────────────────────────────────────────────
_defaults = {
    "history":       [],
    "all_chunks":    [],
    "all_embeddings": None,
    "docs":          {},       # doc_name -> meta
    "summaries":     {},       # doc_name -> summary text
    "suggestions":   [],
    "prefill":       "",
    "provider":      "Groq",
    "doc_filter":    None,     # None = all docs
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── API keys (env or session) ─────────────────────────────────────────────────
_env_groq   = os.environ.get("GROQ_API_KEY", "")
_env_gemini = os.environ.get("GEMINI_API_KEY", "")

if "groq_key"   not in st.session_state: st.session_state.groq_key   = _env_groq
if "gemini_key" not in st.session_state: st.session_state.gemini_key = _env_gemini


def keys():
    return {"groq": st.session_state.groq_key, "gemini": st.session_state.gemini_key}


def active_key_ok():
    p = st.session_state.provider
    k = keys()
    return bool(k["groq"] if p == "Groq" else k["gemini"])


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Logo ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="sb-logo">
      <div class="sb-brand">
        <div class="sb-icon">⚡</div>
        <span class="sb-name">Nexus</span>
      </div>
      <span class="sb-tag">v2.0</span>
    </div>""", unsafe_allow_html=True)

    # ── Provider ──────────────────────────────────────────────────────────────
    st.markdown('<div class="sb-sec"><span class="sb-sec-label">AI Provider</span>', unsafe_allow_html=True)
    provider = st.radio(
        "provider", ["Groq", "Gemini"],
        horizontal=True,
        index=0 if st.session_state.provider == "Groq" else 1,
        label_visibility="collapsed",
    )
    st.session_state.provider = provider
    st.markdown('</div>', unsafe_allow_html=True)

    # ── API Keys ──────────────────────────────────────────────────────────────
    st.markdown('<div class="sb-sec"><span class="sb-sec-label">API Key</span>', unsafe_allow_html=True)
    if provider == "Groq":
        k = st.text_input("groq_key", value=st.session_state.groq_key,
                          placeholder="gsk_...", type="password",
                          label_visibility="collapsed")
        st.session_state.groq_key = k
    else:
        k = st.text_input("gemini_key", value=st.session_state.gemini_key,
                          placeholder="AIza...", type="password",
                          label_visibility="collapsed")
        st.session_state.gemini_key = k
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Upload ────────────────────────────────────────────────────────────────
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sec"><span class="sb-sec-label">Upload PDF</span>', unsafe_allow_html=True)

    uploaded = st.file_uploader("pdf", type="pdf", label_visibility="collapsed")

    if uploaded:
        if not active_key_ok():
            st.error("Add your API key above first.")
        elif uploaded.name not in st.session_state.docs:
            with st.spinner("Indexing…"):
                new_chunks, meta = extract_pdf(uploaded, uploaded.name)
                new_embs = embed_chunks(new_chunks)

                st.session_state.all_chunks.extend(new_chunks)
                if st.session_state.all_embeddings is None:
                    st.session_state.all_embeddings = new_embs
                else:
                    st.session_state.all_embeddings = np.vstack(
                        [st.session_state.all_embeddings, new_embs]
                    )
                st.session_state.docs[uploaded.name] = meta

                # auto summary
                summary = get_summary(provider, keys(), meta["full_text"])
                st.session_state.summaries[uploaded.name] = summary

                # suggestions (from latest doc)
                st.session_state.suggestions = get_suggestions(
                    provider, keys(), meta["full_text"]
                )
                st.session_state.history = []

            st.success(f"✓ Indexed {meta['pages']} pages")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Active documents ──────────────────────────────────────────────────────
    if st.session_state.docs:
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-sec"><span class="sb-sec-label">Documents</span>', unsafe_allow_html=True)

        for doc_name, meta in list(st.session_state.docs.items()):
            words_display = (
                f"{meta['words']:,}" if meta["words"] < 10000
                else f"{round(meta['words']/1000,1)}k"
            )
            short_name = doc_name if len(doc_name) <= 22 else doc_name[:19] + "…"
            st.markdown(f"""
            <div class="doc-card">
              <div class="doc-card-icon">📄</div>
              <div class="doc-card-info">
                <div class="doc-card-name">{short_name}</div>
                <div class="doc-card-meta">{meta['pages']} pages · {words_display} words</div>
              </div>
              <span class="doc-badge">{meta['chunks']}c</span>
            </div>""", unsafe_allow_html=True)

        total_pages = sum(m["pages"] for m in st.session_state.docs.values())
        total_words = sum(m["words"] for m in st.session_state.docs.values())
        total_chunks = sum(m["chunks"] for m in st.session_state.docs.values())
        tw = f"{round(total_words/1000,1)}k" if total_words >= 1000 else str(total_words)
        st.markdown(f"""
        <div class="stats-row">
          <div class="stat-box"><div class="stat-val">{len(st.session_state.docs)}</div><div class="stat-key">docs</div></div>
          <div class="stat-box"><div class="stat-val">{total_pages}</div><div class="stat-key">pages</div></div>
          <div class="stat-box"><div class="stat-val">{tw}</div><div class="stat-key">words</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("🗑  Clear all documents", use_container_width=True):
            for k_s in ["history", "all_chunks", "suggestions", "summaries"]:
                st.session_state[k_s] = [] if k_s != "summaries" else {}
            st.session_state.all_embeddings = None
            st.session_state.docs = {}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Model info footer ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 10px 14px; border-top: 1px solid var(--border); margin-top: 16px;">
      <div style="font-size:9px; color: var(--muted); font-family:'JetBrains Mono',monospace; line-height:1.6;">
        Groq · Llama 3.1 8B Instant<br>
        Gemini · 1.5 Flash<br>
        Embeddings · all-MiniLM-L6-v2
      </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# ── No documents loaded → hero ─────────────────────────────────────────────
if not st.session_state.docs:
    st.markdown("""
    <div class="hero">
      <div class="hero-eyebrow">Semantic Document Intelligence</div>
      <div class="hero-title">
        Talk to <span class="hl">any PDF.</span><br>
        <span class="dim">Instantly.</span>
      </div>
      <div class="hero-sub">
        Upload documents and get precise, cited answers powered by
        real semantic search — not keyword guessing.
      </div>
      <div class="step-cards">
        <div class="step-card">
          <div class="step-num">01 /</div>
          <div class="step-title">Upload</div>
          <div class="step-desc">Drop one or multiple PDFs</div>
        </div>
        <div class="step-card">
          <div class="step-num">02 /</div>
          <div class="step-title">Index</div>
          <div class="step-desc">Semantic vectors built instantly</div>
        </div>
        <div class="step-card">
          <div class="step-num">03 /</div>
          <div class="step-title">Ask</div>
          <div class="step-desc">Get answers with page citations</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

else:
    # ── Auto summary (collapsible) ─────────────────────────────────────────
    for doc_name, summary in st.session_state.summaries.items():
        short = doc_name if len(doc_name) <= 30 else doc_name[:27] + "…"
        with st.expander(f"📋  Auto-summary — {short}", expanded=False):
            st.markdown(f"""
            <div class="summary-box">
              <div class="summary-title">⚡ Document Summary</div>
              <div class="summary-content">{summary}</div>
            </div>""", unsafe_allow_html=True)

    # ── Suggested questions ────────────────────────────────────────────────
    if not st.session_state.history and st.session_state.suggestions:
        st.markdown('<div class="sugg-header">Suggested questions</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, q in enumerate(st.session_state.suggestions):
            with cols[i % 2]:
                if st.button(q, key=f"sq_{i}"):
                    st.session_state.prefill = q
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Chat history ───────────────────────────────────────────────────────
    if st.session_state.history:
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for turn in st.session_state.history:
            # User bubble
            st.markdown(f"""
            <div class="msg-row-user">
              <div class="bubble-user">{turn['q']}</div>
              <div class="av av-usr">YOU</div>
            </div>""", unsafe_allow_html=True)

            # AI bubble
            st.markdown(f"""
            <div class="msg-row-ai">
              <div class="av av-ai">⚡</div>
              <div class="bubble-ai">{turn['a']}</div>
            </div>""", unsafe_allow_html=True)

            # Citation cards
            if turn.get("citations"):
                cite_html = ""
                for c in turn["citations"]:
                    score_pct = int(c["score"] * 100)
                    doc_short = c["doc"][:18] + "…" if len(c["doc"]) > 20 else c["doc"]
                    cite_html += f"""
                    <div class="cite-card">
                      <span>📄</span>
                      <span class="cite-doc">{doc_short}</span>
                      <span class="cite-page">p.{c['page']}</span>
                      <span class="cite-score">{score_pct}%</span>
                    </div>"""
                st.markdown(f'<div class="citations-row">{cite_html}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Export link
        export_text = build_export(st.session_state.history, list(st.session_state.docs.keys()))
        st.download_button(
            "↓ Export chat",
            data=export_text,
            file_name=f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )

st.markdown('</div>', unsafe_allow_html=True)

# ── Chat input ─────────────────────────────────────────────────────────────
if st.session_state.docs:
    placeholder = (
        f"Ask across {len(st.session_state.docs)} document(s)…"
        if len(st.session_state.docs) > 1
        else "Ask anything about your document…"
    )
    question = st.chat_input(placeholder)

    # Handle suggestion prefill
    if st.session_state.prefill and not question:
        question = st.session_state.prefill
        st.session_state.prefill = ""

    if question:
        if not active_key_ok():
            st.error("Please add your API key in the sidebar.")
        else:
            with st.spinner("Searching & reasoning…"):
                results = semantic_search(
                    question,
                    st.session_state.all_chunks,
                    st.session_state.all_embeddings,
                    k=5,
                    doc_filter=st.session_state.doc_filter,
                )
                answer = get_answer(
                    st.session_state.provider, keys(),
                    results, question, st.session_state.history,
                )
            st.session_state.history.append({
                "q": question,
                "a": answer,
                "citations": results,
            })
            st.rerun()
else:
    st.chat_input("Upload a PDF to begin…", disabled=True)
