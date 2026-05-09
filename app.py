import os
import re
import ast
import html
from datetime import datetime

import numpy as np
import streamlit as st
import pypdf


# =============================================================================
# Page config
# =============================================================================
st.set_page_config(
    page_title="Nexus AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# Constants
# =============================================================================
GROQ_MODELS = {
    "llama-3.1-8b-instant":    "Llama 3.1 8B  · Fast",
    "llama-3.3-70b-versatile": "Llama 3.3 70B · Smart",
}

# =============================================================================
# Terminal-style UI
# =============================================================================
st.markdown(
  """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

:root {
  --bg: #0a0a0a;
  --fg: #33ff00;
  --amber: #ffb000;
  --muted: #1f521f;
  --border: #1f521f;
  --border-2: #2d6b2d;
  --danger: #ff3333;
  --panel: #050505;
  --panel-2: #090909;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  border-radius: 0 !important;
}

html, body, [class*="css"] {
  font-family: 'JetBrains Mono', monospace !important;
  background: var(--bg) !important;
  color: var(--fg) !important;
}

#MainMenu, footer { visibility: hidden; }
header { visibility: visible; }

.stApp {
  background: var(--bg) !important;
  color: var(--fg) !important;
}

.stApp::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9998;
  background: repeating-linear-gradient(
    to bottom,
    rgba(51,255,0,0.035) 0px,
    rgba(51,255,0,0.035) 1px,
    transparent 2px,
    transparent 4px
  );
  opacity: 0.28;
}

.stApp::after {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9997;
  background: radial-gradient(
    circle at center,
    rgba(51,255,0,0.05) 0%,
    rgba(0,0,0,0) 65%
  );
}

[data-testid="stSidebar"] {
  background: #080808 !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] *,
button, input, textarea, select {
  font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stSidebar"] .stFileUploader {
  padding-top: 0.25rem;
}

[data-testid="stSidebar"] .stFileUploader label {
  display: none !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  min-height: auto !important;
  display: block !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] {
  display: none !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] p {
  display: none !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
  width: 100% !important;
  background: #050505 !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
  padding: 0.9rem 1rem !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  cursor: pointer !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button:hover {
  background: var(--fg) !important;
  color: black !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  background: var(--panel) !important;
  border: 1px dashed var(--border-2) !important;
  border-radius: 0 !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] p {
  color: #94cc94 !important;
  font-size: 11px !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
  background: transparent !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.55rem 0.8rem !important;
}

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
[data-testid="stSidebar"] .stTextInput textarea {
  background: #050505 !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}

[data-testid="stSidebar"] .stTextInput input::placeholder,
[data-testid="stSidebar"] .stTextInput textarea::placeholder {
  color: #6b996b !important;
}

[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 !important;
  font-size: 11px !important;
  padding: 0.65rem 0.85rem !important;
  width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
  background: var(--fg) !important;
  color: #000 !important;
}

section[data-testid="stSidebar"] > div:first-child {
  padding-top: 0.25rem;
}

/* Slider styling */
[data-testid="stSidebar"] .stSlider [data-testid="stSlider"] > div > div > div {
  background: var(--fg) !important;
}

.main-wrap {
  max-width: 1040px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 8rem;
}

.boot-box,
.panel,
.card,
.summary-box,
.chat-box {
  background: var(--panel);
  border: 1px solid var(--border);
}

.boot-box {
  padding: 1rem 1rem 1.1rem;
  margin-bottom: 1.1rem;
}

.ascii {
  color: var(--fg);
  white-space: pre-wrap;
  line-height: 1.1;
  font-size: 12px;
}

.hero {
  margin: 0.75rem 0 1.5rem;
}

.hero-eyebrow {
  color: var(--amber);
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.hero-title {
  color: var(--fg);
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.0;
  font-weight: 800;
  text-transform: uppercase;
  text-shadow: 0 0 5px rgba(51,255,0,0.35);
  margin-bottom: 0.8rem;
}

.hero-sub {
  color: #98c898;
  max-width: 48rem;
  line-height: 1.8;
  margin-bottom: 1.25rem;
  font-size: 14px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

@media (max-width: 820px) {
  .grid-3 { grid-template-columns: 1fr; }
}

.step-card { padding: 0.95rem; }
.step-top { color: var(--amber); font-size: 11px; margin-bottom: 0.65rem; }
.step-title { color: var(--fg); font-weight: 700; margin-bottom: 0.25rem; text-transform: uppercase; }
.step-desc { color: #93c493; font-size: 12px; line-height: 1.65; }

.section-label {
  color: var(--amber);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin: 1.1rem 0 0.55rem;
}

.summary-box { padding: 1rem; margin-bottom: 0.75rem; }
.summary-title { color: var(--amber); font-size: 11px; letter-spacing: 0.16em; margin-bottom: 0.65rem; text-transform: uppercase; }
.summary-content { color: #9cd09c; line-height: 1.75; font-size: 13px; }

.doc-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.8rem 0.85rem;
  margin-bottom: 0.55rem;
  background: var(--panel-2);
  border: 1px solid var(--border);
}

.doc-icon,
.av {
  width: 2rem;
  height: 2rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border);
  color: var(--fg);
  flex: 0 0 auto;
}

.doc-icon { background: #071107; }

.doc-info { min-width: 0; flex: 1; }
.doc-name { color: var(--fg); font-size: 12px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.doc-meta { color: #86b586; font-size: 10px; margin-top: 0.2rem; }

.badge { color: var(--amber); border: 1px solid var(--border); padding: 0.2rem 0.4rem; font-size: 9px; }

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.stat { border: 1px solid var(--border); background: var(--panel); padding: 0.8rem 0.45rem; text-align: center; }
.stat-val { color: var(--fg); font-size: 1.15rem; font-weight: 800; line-height: 1; }
.stat-key { color: #82aa82; text-transform: uppercase; font-size: 9px; margin-top: 0.35rem; letter-spacing: 0.12em; }

.suggestion-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.6rem;
}

@media (max-width: 700px) {
  .suggestion-grid { grid-template-columns: 1fr; }
}

.suggestion-btn {
  text-align: left !important;
  padding: 0.85rem 0.9rem !important;
  color: #b2dfb2 !important;
  border: 1px solid var(--border) !important;
  background: var(--panel) !important;
}

.suggestion-btn:hover {
  background: var(--fg) !important;
  color: #000 !important;
}

.chat-wrap { margin-top: 1rem; }

.msg-user,
.msg-ai {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.65rem;
  margin-bottom: 0.5rem;
  align-items: end;
}

.msg-ai {
  grid-template-columns: auto 1fr;
  align-items: start;
}

.bubble-user,
.bubble-ai {
  padding: 0.95rem 1rem;
  border: 1px solid var(--border);
  background: var(--panel);
  line-height: 1.75;
  font-size: 13px;
  white-space: normal;
  word-break: break-word;
}

.bubble-user { background: #0d2b0d; color: var(--fg); }
.bubble-ai { color: #b8deb8; }

.user-tag { color: var(--amber); font-size: 10px; letter-spacing: 0.14em; align-self: center; white-space: nowrap; }
.ai-tag { color: var(--fg); font-size: 10px; letter-spacing: 0.14em; align-self: center; white-space: nowrap; }

.cite-card {
  background: var(--panel);
  border: 1px solid var(--border);
  padding: 0.3rem 0.55rem;
  font-size: 10px;
  display: inline-flex;
  gap: 0.45rem;
  align-items: center;
}

.cite-page { color: var(--fg); }
.cite-score { color: var(--amber); }

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: #050505 !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
  color: #7b9f7b !important;
}

[data-testid="stForm"] {
  border: 1px solid var(--border);
  background: var(--panel);
  padding: 0.9rem;
}

[data-testid="stFormSubmitButton"] button,
[data-testid="stDownloadButton"] button {
  background: transparent !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 !important;
}

[data-testid="stFormSubmitButton"] button:hover,
[data-testid="stDownloadButton"] button:hover {
  background: var(--fg) !important;
  color: #000 !important;
}

[data-testid="stExpander"] {
  background: var(--panel) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 !important;
}

[data-testid="stExpander"] summary {
  color: var(--fg) !important;
  font-size: 12px !important;
}

.stSpinner > div { border-top-color: var(--fg) !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); }

[data-testid="collapsedControl"] button {
  color: transparent !important;
  font-size: 0 !important;
  background: var(--bg) !important;
  border: none !important;
  position: relative !important;
}
[data-testid="collapsedControl"] button::after {
  content: '›';
  font-size: 22px !important;
  color: #33ff00 !important;
  font-family: 'JetBrains Mono', monospace !important;
  display: block !important;
}
[data-testid="collapsedControl"] button:hover::after { color: #ffb000 !important; }

[data-testid="stSidebar"] button[data-testid="baseButton-header"] {
  color: transparent !important;
  font-size: 0 !important;
  background: transparent !important;
  border: none !important;
  position: relative !important;
}
[data-testid="stSidebar"] button[data-testid="baseButton-header"]::after {
  content: '‹';
  font-size: 22px !important;
  color: #33ff00 !important;
  font-family: 'JetBrains Mono', monospace !important;
  display: block !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# Helpers
# =============================================================================
@st.cache_resource(show_spinner=False)
def load_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def safe(text: str) -> str:
    return html.escape("" if text is None else str(text))


def sanitize_llm_text(text: str) -> str:
    """Strip accidental HTML / fenced-code artifacts from model output."""
    text = "" if text is None else str(text)
    text = text.replace("```", "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def render_answer(text: str) -> str:
    return sanitize_llm_text(text)


# ── PDF ingestion ──────────────────────────────────────────────────────────────
def extract_pdf(file_obj, doc_name: str):
    file_obj.seek(0)
    reader = pypdf.PdfReader(file_obj)
    chunks, full_text = [], ""
    chunk_size, overlap = 260, 60

    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"
        words = page_text.split()
        start = 0
        while start < len(words):
            chunk_text = " ".join(words[start : start + chunk_size]).strip()
            if chunk_text:
                chunks.append({"text": chunk_text, "page": page_idx + 1, "doc": doc_name})
            start += max(1, chunk_size - overlap)

    meta = {
        "pages":     len(reader.pages),
        "words":     len(re.findall(r"\b[\w'-]+\b", re.sub(r"\s+", " ", full_text).strip())),
        "chunks":    len(chunks),
        "full_text": full_text[:5000],
    }
    return chunks, meta


def embed_chunks(chunks):
    model = load_embedder()
    texts = [c["text"] for c in chunks]
    if not texts:
        return np.empty((0, 384))
    return model.encode(texts, show_progress_bar=False, batch_size=32)


# ── Retrieval ──────────────────────────────────────────────────────────────────
_STOP = {
    "the","a","an","is","are","was","were","in","on","at","to","of","and","or",
    "for","with","that","this","it","be","has","have","had","do","does","did",
    "but","if","by","from","as","not","what","how","when","where","who","which",
}

def _keyword_score(query: str, text: str) -> float:
    """Fraction of (non-stop) query words that appear in the chunk."""
    q_words = set(re.findall(r"\b\w+\b", query.lower())) - _STOP
    if not q_words:
        return 0.0
    t_words = set(re.findall(r"\b\w+\b", text.lower()))
    return len(q_words & t_words) / len(q_words)


def hybrid_search(
    query: str,
    all_chunks,
    all_embeddings,
    k: int = 5,
    doc_filter=None,
    alpha: float = 0.70,
    min_score: float = 0.10,
):
    """
    Combined semantic + keyword retrieval.
    alpha controls the semantic weight (1-alpha goes to keyword overlap).
    Chunks scoring below min_score are dropped so the LLM isn't fed junk.
    """
    from sklearn.metrics.pairwise import cosine_similarity

    if all_embeddings is None or len(all_chunks) == 0:
        return []

    model   = load_embedder()
    q_emb   = model.encode([query])
    indices = (
        [i for i, c in enumerate(all_chunks) if c["doc"] in doc_filter]
        if doc_filter
        else list(range(len(all_chunks)))
    )
    if not indices:
        return []

    filtered_embs = all_embeddings[indices]
    sem_scores    = cosine_similarity(q_emb, filtered_embs)[0]
    kw_scores     = np.array([_keyword_score(query, all_chunks[i]["text"]) for i in indices])

    # Normalise keyword scores to [0, 1]
    if kw_scores.max() > 0:
        kw_scores = kw_scores / kw_scores.max()

    combined  = alpha * sem_scores + (1 - alpha) * kw_scores
    top_local = np.argsort(combined)[::-1][:k]

    results = []
    for local_idx in top_local:
        score = float(combined[local_idx])
        if score < min_score:
            continue
        global_idx = indices[local_idx]
        results.append(
            {
                "text":      all_chunks[global_idx]["text"],
                "page":      all_chunks[global_idx]["page"],
                "doc":       all_chunks[global_idx]["doc"],
                "score":     score,
                "sem_score": float(sem_scores[local_idx]),
            }
        )
    return results


# ── LLM helpers ───────────────────────────────────────────────────────────────
def _build_messages(system: str, user_msg: str, history):
    msgs = [{"role": "system", "content": system}]
    for turn in history[-4:]:
        msgs.append({"role": "user",      "content": sanitize_llm_text(turn["q"])})
        msgs.append({"role": "assistant", "content": sanitize_llm_text(turn["a"])})
    msgs.append({"role": "user", "content": user_msg})
    return msgs


def _context_from_results(results) -> str:
    if not results:
        return "NO_CONTEXT_FOUND"
    parts = [
        f"[Source: {r['doc']} | Page {r['page']} | Relevance: {int(r['score']*100)}%]\n{r['text']}"
        for r in results
    ]
    return "\n\n---\n\n".join(parts)


def _qa_system() -> str:
    return (
        "You are Nexus, a precise document assistant.\n"
        "Rules:\n"
        "- Use ONLY the provided CONTEXT to answer. Do NOT use external knowledge.\n"
        "- If the answer can be found verbatim or inferred from the context, give a short, "
        "factual answer (1–3 sentences).\n"
        "- If you infer, state it briefly as an inference.\n"
        "- If the answer cannot be found or reasonably inferred, respond: "
        "'Answer not found in context.'\n"
        "- Do not output HTML, tags, or code blocks.\n"
        "- Be concise and prioritise directly referencing context passages when relevant."
    )


def _qa_user_msg(context: str, question: str) -> str:
    return (
        f"RETRIEVED CONTEXT:\n{context}\n\n"
        f"QUESTION:\n{question}\n\n"
        "Instructions:\n"
        "- Answer briefly and cite sources from the context.\n"
        "- Separate multiple supporting passages with semicolons.\n"
        "- If nothing in the context answers the question, say exactly: "
        "'Answer not found in context.'"
    )


def _groq_client():
    from groq import Groq
    return Groq(api_key=st.session_state.groq_key)


def _handle_groq_error(err: str) -> str:
    if "429" in err:
        return "⚠️ Rate limit reached. Please wait a moment and try again."
    if "401" in err or "invalid" in err.lower():
        return "⚠️ Invalid Groq API key. Please check the key in the sidebar."
    return f"⚠️ Groq error: {err}"


def call_groq(system: str, user_msg: str, history) -> str:
    """Non-streaming call — used for summaries, suggestions, and fallback."""
    try:
        resp = _groq_client().chat.completions.create(
            model=st.session_state.model_choice,
            messages=_build_messages(system, user_msg, history),
            max_tokens=1024,
            temperature=0.3,
        )
        return sanitize_llm_text(resp.choices[0].message.content.strip())
    except Exception as e:
        return _handle_groq_error(str(e))


def call_groq_stream(system: str, user_msg: str, history):
    """Generator that yields raw token strings for st.write_stream."""
    try:
        stream = _groq_client().chat.completions.create(
            model=st.session_state.model_choice,
            messages=_build_messages(system, user_msg, history),
            max_tokens=1024,
            temperature=0.3,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except Exception as e:
        yield _handle_groq_error(str(e))


# ── QA wrappers ────────────────────────────────────────────────────────────────
def get_answer_stream(results, question, history):
    ctx = _context_from_results(results)
    yield from call_groq_stream(_qa_system(), _qa_user_msg(ctx, question), history)


def get_answer(results, question, history) -> str:
    ctx = _context_from_results(results)
    return call_groq(_qa_system(), _qa_user_msg(ctx, question), history)


def get_summary(full_text: str) -> str:
    system   = "You are a document analyst. Be structured, concise, and factual."
    user_msg = (
        "Provide a structured document summary with these sections:\n"
        "Main Topic:\nKey Points:\nImportant Data/Facts:\nConclusion:\n\n"
        f"Document:\n{full_text[:4500]}"
    )
    return call_groq(system, user_msg, [])


def get_suggestions(docs_dict: dict) -> list:
    """
    Generate 4 suggested questions sampling from ALL loaded documents,
    not just the most recently uploaded one.
    """
    combined = ""
    for meta in docs_dict.values():
        combined += meta["full_text"][:1200] + "\n\n"

    system   = "Output ONLY a Python list of 4 strings. No markdown, no explanation."
    user_msg = (
        "Generate 4 insightful questions for this document collection.\n"
        'Format exactly like: ["Q1?","Q2?","Q3?","Q4?"]\n\n'
        f"{combined[:3200]}"
    )
    raw = call_groq(system, user_msg, [])

    try:
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            qs = ast.literal_eval(match.group())
            if isinstance(qs, list) and len(qs) >= 4:
                return [str(q) for q in qs[:4]]
    except Exception:
        pass

    return [
        "What is the main topic of this document?",
        "What are the key findings or conclusions?",
        "What data or evidence is presented?",
        "What are the recommendations or next steps?",
    ]


def build_export(history, doc_names) -> str:
    lines = [
        "NEXUS AI — CHAT EXPORT",
        "=" * 60,
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Documents: {', '.join(doc_names) if doc_names else 'None'}",
        "=" * 60,
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


# =============================================================================
# Session state
# =============================================================================
_DEFAULTS = {
    "history":      [],
    "all_chunks":   [],
    "all_embeddings": None,
    "docs":         {},
    "summaries":    {},
    "suggestions":  [],
    "prefill":      "",
    "doc_filter":   None,
    "groq_key":     os.environ.get("GROQ_API_KEY", ""),
    "model_choice": "llama-3.1-8b-instant",   # NEW
    "top_k":        5,                         # NEW
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


def active_key_ok() -> bool:
    return bool(st.session_state.groq_key)


def reset_app():
    for k in ["history","all_chunks","all_embeddings","docs","summaries",
              "suggestions","prefill","doc_filter"]:
        st.session_state[k] = _DEFAULTS[k]
    st.rerun()


def clear_chat_only():           # NEW — wipe history without losing indexed docs
    st.session_state.history = []
    st.session_state.prefill  = ""
    st.rerun()


# =============================================================================
# Sidebar
# =============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 1rem 0.9rem 0.8rem; border-bottom: 1px solid var(--border);
                    margin-bottom: 0.9rem;">
          <div style="color: var(--fg); font-weight: 800; font-size: 16px;
                      letter-spacing: 0.08em;">NEXUS AI</div>
          <div style="color: var(--amber); font-size: 10px; letter-spacing: 0.18em;
                      margin-top: 0.35rem;">TERMINAL PDF RAG</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── API key ────────────────────────────────────────────────────────────────
    st.markdown("### > API KEY")
    groq_value = st.text_input(
        "groq_key",
        value=st.session_state.groq_key,
        placeholder="gsk_...",
        type="password",
        label_visibility="collapsed",
    )
    st.session_state.groq_key = groq_value

    # ── Model selector (NEW) ───────────────────────────────────────────────────
    st.markdown("### > MODEL")
    model_labels = list(GROQ_MODELS.values())
    model_keys   = list(GROQ_MODELS.keys())
    current_idx  = model_keys.index(st.session_state.model_choice) if st.session_state.model_choice in model_keys else 0
    chosen_label = st.selectbox(
        "model_select",
        model_labels,
        index=current_idx,
        label_visibility="collapsed",
    )
    st.session_state.model_choice = model_keys[model_labels.index(chosen_label)]

    # ── Document upload ────────────────────────────────────────────────────────
    st.markdown("### > LOAD DOCUMENTS")
    uploaded_files = st.file_uploader("ADD PDF(S)", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        if not active_key_ok():
            st.error("Add your Groq API key first.")
        else:
            new_docs_loaded = False
            for uploaded in uploaded_files:
                if uploaded.name in st.session_state.docs:
                    continue

                with st.spinner(f"Indexing {uploaded.name}..."):
                    new_chunks, meta = extract_pdf(uploaded, uploaded.name)
                    new_embs         = embed_chunks(new_chunks)

                    st.session_state.all_chunks.extend(new_chunks)
                    st.session_state.all_embeddings = (
                        new_embs
                        if st.session_state.all_embeddings is None
                        else np.vstack([st.session_state.all_embeddings, new_embs])
                    )
                    st.session_state.docs[uploaded.name]      = meta
                    st.session_state.summaries[uploaded.name] = get_summary(meta["full_text"])
                    new_docs_loaded = True

            if new_docs_loaded:
                # Regenerate suggestions from ALL docs (fix for single-doc bug)
                st.session_state.suggestions = get_suggestions(st.session_state.docs)
                st.session_state.history     = []
                st.session_state.prefill     = ""
                st.success("Documents indexed.")

    if st.session_state.docs:
        # ── Focus selector ─────────────────────────────────────────────────────
        st.markdown("### > DOCUMENTS")
        doc_names     = list(st.session_state.docs.keys())
        focus_options = ["All documents"] + doc_names
        current_focus = (
            st.session_state.doc_filter[0]
            if st.session_state.doc_filter and st.session_state.doc_filter[0] in doc_names
            else "All documents"
        )
        chosen_focus = st.selectbox(
            "focus",
            focus_options,
            index=focus_options.index(current_focus),
            label_visibility="collapsed",
        )
        st.session_state.doc_filter = None if chosen_focus == "All documents" else [chosen_focus]

        # ── Top-K slider (NEW) ─────────────────────────────────────────────────
        st.markdown("### > RETRIEVAL DEPTH")
        st.session_state.top_k = st.slider(
            "top_k",
            min_value=3,
            max_value=10,
            value=st.session_state.top_k,
            step=1,
            label_visibility="collapsed",
            help="Number of chunks retrieved per query",
        )
        st.markdown(
            f'<div style="color:#7ea57e;font-size:10px;margin-top:-0.4rem;">'
            f'Retrieving top {st.session_state.top_k} chunks per query</div>',
            unsafe_allow_html=True,
        )

        # ── Doc cards ──────────────────────────────────────────────────────────
        for doc_name, meta in st.session_state.docs.items():
            short_name   = doc_name if len(doc_name) <= 24 else doc_name[:21] + "..."
            words_display = (
                f"{meta['words']:,}" if meta["words"] < 10_000
                else f"{round(meta['words']/1000, 1)}k"
            )
            st.markdown(
                f"""
                <div class="doc-card">
                  <div class="doc-icon">PDF</div>
                  <div class="doc-info">
                    <div class="doc-name">{safe(short_name)}</div>
                    <div class="doc-meta">
                      {meta['pages']} pages · {words_display} words · {meta['chunks']} chunks
                    </div>
                  </div>
                  <div class="badge">{meta['pages']}p</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        total_pages  = sum(m["pages"]  for m in st.session_state.docs.values())
        total_words  = sum(m["words"]  for m in st.session_state.docs.values())
        total_chunks = sum(m["chunks"] for m in st.session_state.docs.values())

        st.markdown(
            f"""
            <div class="stats">
              <div class="stat">
                <div class="stat-val">{len(st.session_state.docs)}</div>
                <div class="stat-key">docs</div>
              </div>
              <div class="stat">
                <div class="stat-val">{total_pages}</div>
                <div class="stat-key">pages</div>
              </div>
              <div class="stat">
                <div class="stat-val">
                  {round(total_words/1000,1) if total_words >= 1000 else total_words}
                </div>
                <div class="stat-key">words</div>
              </div>
            </div>
            <div style="margin-top:0.45rem; color:#7ea57e; font-size:10px;">
              {total_chunks} total chunks indexed
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        # NEW: two action buttons
        if st.session_state.history:
            if st.button("[ CLEAR CHAT ONLY ]", use_container_width=True):
                clear_chat_only()
        if st.button("[ CLEAR ALL DOCUMENTS ]", use_container_width=True):
            reset_app()

    st.markdown("---")


# =============================================================================
# Main area
# =============================================================================
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

if not st.session_state.docs:
    # ── Landing page ───────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="boot-box">
          <div class="ascii">NEXUS - AI Document Assistant</div>
        </div>
        <div class="hero">
          <div class="hero-eyebrow">Semantic PDF Intelligence</div>
          <div class="hero-title">Talk to any PDF<br>Instantly.</div>
          <div class="hero-sub">
            Upload documents and explore them with hybrid semantic search and
            AI-powered answers. Open the sidebar from the top-left control to
            load files or update the API key.
          </div>
          <div class="grid-3">
            <div class="card step-card">
              <div class="step-top">01 // LOAD</div>
              <div class="step-title">Upload PDFs</div>
              <div class="step-desc">Drop documents in the sidebar and index them automatically.</div>
            </div>
            <div class="card step-card">
              <div class="step-top">02 // INDEX</div>
              <div class="step-title">Build vectors</div>
              <div class="step-desc">Chunks are embedded with all-MiniLM-L6-v2 for hybrid retrieval.</div>
            </div>
            <div class="card step-card">
              <div class="step-top">03 // QUERY</div>
              <div class="step-title">Ask questions</div>
              <div class="step-desc">Streamed answers grounded in retrieved pages and citations.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    # ── Auto-summaries ─────────────────────────────────────────────────────────
    for doc_name, summary in st.session_state.summaries.items():
        short = doc_name if len(doc_name) <= 36 else doc_name[:33] + "..."
        with st.expander(f"> AUTO SUMMARY :: {short}", expanded=False):
            st.markdown(
                f"""
                <div class="summary-box">
                  <div class="summary-title">DOCUMENT SUMMARY</div>
                  <div class="summary-content">{render_answer(summary)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Suggested queries ──────────────────────────────────────────────────────
    if not st.session_state.history and st.session_state.suggestions:
        st.markdown('<div class="section-label">> SUGGESTED QUERIES</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, q in enumerate(st.session_state.suggestions):
            with cols[i % 2]:
                if st.button(q, key=f"suggest_{i}", use_container_width=True):
                    st.session_state.prefill = q
                    st.rerun()

    # ── Conversation log ───────────────────────────────────────────────────────
    if st.session_state.history:
        st.markdown('<div class="section-label">> CONVERSATION LOG</div>', unsafe_allow_html=True)
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

        for turn in st.session_state.history:
            # User bubble
            st.markdown(
                f"""
                <div class="msg-user">
                  <div class="bubble-user">{safe(turn['q'])}</div>
                  <div class="user-tag">YOU</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # AI answer — rendered as markdown, no raw HTML injection
            st.markdown(f"**NEXUS:**\n\n{render_answer(turn['a'])}")

            # Citation snippets (NEW — expandable with chunk preview)
            if turn.get("citations"):
                with st.expander(
                    f"▸ {len(turn['citations'])} SOURCE(S) RETRIEVED", expanded=False
                ):
                    for c in turn["citations"]:
                        score_pct = int(c["score"] * 100)
                        short_doc = c["doc"] if len(c["doc"]) <= 22 else c["doc"][:19] + "..."
                        snippet   = c["text"][:160].replace("\n", " ").strip() + "…"
                        st.markdown(
                            f"`{short_doc}` &nbsp;·&nbsp; `p.{c['page']}` &nbsp;·&nbsp; "
                            f"`{score_pct}% relevance`\n\n> {snippet}\n\n---"
                        )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Export ─────────────────────────────────────────────────────────────────
    export_text = build_export(
        st.session_state.history, list(st.session_state.docs.keys())
    )
    st.download_button(
        "[ EXPORT CHAT ]",
        data=export_text,
        file_name=f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=False,
    )

    # ── Query form ─────────────────────────────────────────────────────────────
    st.markdown("### > QUERY")
    with st.form("query_form", clear_on_submit=True):
        prompt = st.text_input(
            "cmd",
            value=st.session_state.prefill,
            placeholder="type a question about the loaded PDFs",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("[ EXECUTE ]", use_container_width=True)

    if submitted:
        question = prompt.strip()
        if not question:
            st.warning("Type a question first.")
        elif not active_key_ok():
            st.error("Add your Groq API key in the sidebar.")
        else:
            # Step 1 — retrieval
            with st.spinner("Retrieving context..."):
                results = hybrid_search(
                    question,
                    st.session_state.all_chunks,
                    st.session_state.all_embeddings,
                    k=st.session_state.top_k,
                    doc_filter=st.session_state.doc_filter,
                )

            # Step 2 — streaming answer
            st.markdown(
                f'<div class="msg-user">'
                f'<div class="bubble-user">{safe(question)}</div>'
                f'<div class="user-tag">YOU</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown("**NEXUS:**")

            # st.write_stream collects all yielded tokens and returns the full string
            raw_answer = st.write_stream(
                get_answer_stream(results, question, st.session_state.history)
            )
            answer = sanitize_llm_text(raw_answer)

            # Persist to history
            st.session_state.history.append(
                {"q": question, "a": answer, "citations": results}
            )
            st.session_state.prefill = ""
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# Sidebar collapse button fix (JS)
# =============================================================================
import streamlit.components.v1 as components

components.html(
    """
<script>
function fixCollapseBtn() {
  const doc = window.parent.document;

  doc.querySelectorAll('[data-testid="collapsedControl"] button').forEach(btn => {
    btn.innerHTML = '';
    btn.style.cssText += 'background:transparent!important;border:none!important;'
      + 'cursor:pointer!important;width:36px!important;height:36px!important;'
      + 'display:flex!important;align-items:center!important;justify-content:center!important;';
    const arrow = doc.createElement('span');
    arrow.textContent = '\u203a';
    arrow.style.cssText = 'color:#33ff00;font-size:24px;font-family:"JetBrains Mono",monospace;'
      + 'line-height:1;text-shadow:0 0 6px rgba(51,255,0,0.5);pointer-events:none;';
    btn.appendChild(arrow);
  });

  doc.querySelectorAll(
    '[data-testid="stSidebar"] button[data-testid="baseButton-header"]'
  ).forEach(btn => {
    btn.innerHTML = '';
    const arrow = doc.createElement('span');
    arrow.textContent = '\u2039';
    arrow.style.cssText = 'color:#33ff00;font-size:24px;font-family:"JetBrains Mono",monospace;'
      + 'pointer-events:none;';
    btn.appendChild(arrow);
  });
}

fixCollapseBtn();
[300, 800, 1500].forEach(t => setTimeout(fixCollapseBtn, t));
new MutationObserver(fixCollapseBtn).observe(
  window.parent.document.body, { childList: true, subtree: true }
);
</script>
""",
    height=0,
)