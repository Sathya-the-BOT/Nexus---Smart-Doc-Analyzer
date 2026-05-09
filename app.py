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
  --correct: #33ff00;
  --wrong: #ff3333;
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

[data-testid="stSidebar"] .stFileUploader label { display: none !important; }

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  border: none !important; background: transparent !important;
  padding: 0 !important; min-height: auto !important; display: block !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] { display: none !important; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] p { display: none !important; }

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
  width: 100% !important; background: #050505 !important; color: var(--fg) !important;
  border: 1px solid var(--border) !important; padding: 0.9rem 1rem !important;
  font-size: 13px !important; font-weight: 700 !important; text-transform: uppercase !important;
  letter-spacing: 0.08em !important; cursor: pointer !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button:hover {
  background: var(--fg) !important; color: black !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  background: var(--panel) !important; border: 1px dashed var(--border-2) !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] p {
  color: #94cc94 !important; font-size: 11px !important;
}

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
[data-testid="stSidebar"] .stTextInput textarea {
  background: #050505 !important; color: var(--fg) !important;
  border: 1px solid var(--border) !important; border-radius: 0 !important; box-shadow: none !important;
}

[data-testid="stSidebar"] .stTextInput input::placeholder,
[data-testid="stSidebar"] .stTextInput textarea::placeholder { color: #6b996b !important; }

[data-testid="stSidebar"] .stButton > button {
  background: transparent !important; color: var(--fg) !important;
  border: 1px solid var(--border) !important; border-radius: 0 !important;
  font-size: 11px !important; padding: 0.65rem 0.85rem !important; width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
  background: var(--fg) !important; color: #000 !important;
}

/* ── Mode tab active state ── */
.mode-active .stButton > button {
  background: var(--fg) !important;
  color: #000 !important;
  border: 1px solid var(--fg) !important;
  font-weight: 800 !important;
}

section[data-testid="stSidebar"] > div:first-child { padding-top: 0.25rem; }

.main-wrap {
  max-width: 1040px; margin: 0 auto; padding: 1.5rem 1.25rem 8rem;
}

.boot-box, .panel, .card, .summary-box, .chat-box {
  background: var(--panel); border: 1px solid var(--border);
}

.boot-box { padding: 1rem 1rem 1.1rem; margin-bottom: 1.1rem; }

.ascii { color: var(--fg); white-space: pre-wrap; line-height: 1.1; font-size: 12px; }

.hero { margin: 0.75rem 0 1.5rem; }
.hero-eyebrow {
  color: var(--amber); font-size: 11px; letter-spacing: 0.2em;
  text-transform: uppercase; margin-bottom: 0.75rem;
}
.hero-title {
  color: var(--fg); font-size: clamp(2rem, 5vw, 4rem); line-height: 1.0;
  font-weight: 800; text-transform: uppercase;
  text-shadow: 0 0 5px rgba(51,255,0,0.35); margin-bottom: 0.8rem;
}
.hero-sub {
  color: #98c898; max-width: 48rem; line-height: 1.8; margin-bottom: 1.25rem; font-size: 14px;
}

.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }
@media (max-width: 820px) { .grid-3 { grid-template-columns: 1fr; } }

.step-card { padding: 0.95rem; }
.step-top { color: var(--amber); font-size: 11px; margin-bottom: 0.65rem; }
.step-title { color: var(--fg); font-weight: 700; margin-bottom: 0.25rem; text-transform: uppercase; }
.step-desc { color: #93c493; font-size: 12px; line-height: 1.65; }

.section-label {
  color: var(--amber); font-size: 11px; letter-spacing: 0.18em;
  text-transform: uppercase; margin: 1.1rem 0 0.55rem;
}

.summary-box { padding: 1rem; margin-bottom: 0.75rem; }
.summary-title {
  color: var(--amber); font-size: 11px; letter-spacing: 0.16em;
  margin-bottom: 0.65rem; text-transform: uppercase;
}
.summary-content { color: #9cd09c; line-height: 1.75; font-size: 13px; }

.doc-card {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.8rem 0.85rem; margin-bottom: 0.55rem;
  background: var(--panel-2); border: 1px solid var(--border);
}
.doc-icon, .av {
  width: 2rem; height: 2rem; display: inline-flex; align-items: center;
  justify-content: center; border: 1px solid var(--border); color: var(--fg); flex: 0 0 auto;
}
.doc-icon { background: #071107; }
.doc-info { min-width: 0; flex: 1; }
.doc-name { color: var(--fg); font-size: 12px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.doc-meta { color: #86b586; font-size: 10px; margin-top: 0.2rem; }
.badge { color: var(--amber); border: 1px solid var(--border); padding: 0.2rem 0.4rem; font-size: 9px; }

.stats {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin-top: 0.75rem;
}
.stat { border: 1px solid var(--border); background: var(--panel); padding: 0.8rem 0.45rem; text-align: center; }
.stat-val { color: var(--fg); font-size: 1.15rem; font-weight: 800; line-height: 1; }
.stat-key { color: #82aa82; text-transform: uppercase; font-size: 9px; margin-top: 0.35rem; letter-spacing: 0.12em; }

.chat-wrap { margin-top: 1rem; }

.msg-user, .msg-ai {
  display: grid; grid-template-columns: 1fr auto; gap: 0.65rem; margin-bottom: 0.5rem; align-items: end;
}
.msg-ai { grid-template-columns: auto 1fr; align-items: start; }

.bubble-user, .bubble-ai {
  padding: 0.95rem 1rem; border: 1px solid var(--border); background: var(--panel);
  line-height: 1.75; font-size: 13px; white-space: normal; word-break: break-word;
}
.bubble-user { background: #0d2b0d; color: var(--fg); }
.bubble-ai { color: #b8deb8; }
.user-tag { color: var(--amber); font-size: 10px; letter-spacing: 0.14em; align-self: center; white-space: nowrap; }
.ai-tag { color: var(--fg); font-size: 10px; letter-spacing: 0.14em; align-self: center; white-space: nowrap; }

/* ── Quiz styles ── */
.quiz-header {
  border: 1px solid var(--border); background: var(--panel);
  padding: 0.9rem 1rem; margin-bottom: 1rem;
}
.quiz-header-top {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 0.5rem;
}
.quiz-title { color: var(--amber); font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; }
.quiz-counter { color: var(--fg); font-size: 11px; }
.quiz-bar-bg { height: 3px; background: var(--muted); width: 100%; }
.quiz-bar-fill { height: 3px; background: var(--fg); transition: width 0.3s; }

.quiz-question {
  border: 1px solid var(--border); background: var(--panel);
  padding: 1.25rem 1.1rem; margin-bottom: 1rem;
}
.quiz-q-label {
  color: var(--amber); font-size: 10px; letter-spacing: 0.18em;
  text-transform: uppercase; margin-bottom: 0.65rem;
}
.quiz-q-text { color: var(--fg); font-size: 15px; line-height: 1.7; font-weight: 700; }

.quiz-opt {
  display: block; width: 100%; text-align: left; padding: 0.75rem 1rem;
  margin-bottom: 0.5rem; background: var(--panel-2); border: 1px solid var(--border-2);
  color: #b8deb8; font-size: 13px; font-family: 'JetBrains Mono', monospace;
  cursor: pointer; transition: all 0.12s; line-height: 1.5;
}
.quiz-opt:hover { border-color: var(--fg); color: var(--fg); }
.quiz-opt.correct { border-color: var(--correct); color: var(--correct); background: rgba(51,255,0,0.06); }
.quiz-opt.wrong   { border-color: var(--wrong);   color: var(--wrong);   background: rgba(255,51,51,0.06); }
.quiz-opt.neutral { opacity: 0.45; }

.quiz-explanation {
  border: 1px solid var(--border-2); background: var(--panel-2);
  padding: 0.85rem 1rem; margin-top: 0.75rem; font-size: 12px; color: #9cd09c; line-height: 1.7;
}
.quiz-result-correct { color: var(--correct); font-weight: 700; font-size: 12px; letter-spacing: 0.1em; }
.quiz-result-wrong   { color: var(--wrong);   font-weight: 700; font-size: 12px; letter-spacing: 0.1em; }

.score-box {
  border: 1px solid var(--border); background: var(--panel);
  padding: 2.5rem 1.5rem; text-align: center; margin-bottom: 1.25rem;
}
.score-big {
  color: var(--fg); font-size: clamp(3rem, 10vw, 5.5rem);
  font-weight: 800; line-height: 1; margin: 0.5rem 0;
  text-shadow: 0 0 20px rgba(51,255,0,0.4);
}
.score-sub { color: #9cd09c; font-size: 13px; margin-top: 0.5rem; }
.score-grade { color: var(--amber); font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; }

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: #050505 !important; color: var(--fg) !important;
  border: 1px solid var(--border) !important; border-radius: 0 !important; box-shadow: none !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder { color: #7b9f7b !important; }

[data-testid="stForm"] { border: 1px solid var(--border); background: var(--panel); padding: 0.9rem; }

[data-testid="stFormSubmitButton"] button,
[data-testid="stDownloadButton"] button {
  background: transparent !important; color: var(--fg) !important;
  border: 1px solid var(--border) !important; border-radius: 0 !important;
}
[data-testid="stFormSubmitButton"] button:hover,
[data-testid="stDownloadButton"] button:hover {
  background: var(--fg) !important; color: #000 !important;
}

[data-testid="stExpander"] {
  background: var(--panel) !important; border: 1px solid var(--border) !important;
}
[data-testid="stExpander"] summary { color: var(--fg) !important; font-size: 12px !important; }

[data-testid="stNumberInput"] input {
  background: #050505 !important; color: var(--fg) !important;
  border: 1px solid var(--border) !important; border-radius: 0 !important;
  font-family: 'JetBrains Mono', monospace !important;
}

.stSpinner > div { border-top-color: var(--fg) !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); }

[data-testid="collapsedControl"] button {
  color: transparent !important; font-size: 0 !important;
  background: var(--bg) !important; border: none !important; position: relative !important;
}
[data-testid="collapsedControl"] button::after {
  content: '›'; font-size: 22px !important; color: #33ff00 !important;
  font-family: 'JetBrains Mono', monospace !important; display: block !important;
}
[data-testid="collapsedControl"] button:hover::after { color: #ffb000 !important; }
[data-testid="stSidebar"] button[data-testid="baseButton-header"] {
  color: transparent !important; font-size: 0 !important;
  background: transparent !important; border: none !important; position: relative !important;
}
[data-testid="stSidebar"] button[data-testid="baseButton-header"]::after {
  content: '‹'; font-size: 22px !important; color: #33ff00 !important;
  font-family: 'JetBrains Mono', monospace !important; display: block !important;
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
    q_words = set(re.findall(r"\b\w+\b", query.lower())) - _STOP
    if not q_words:
        return 0.0
    t_words = set(re.findall(r"\b\w+\b", text.lower()))
    return len(q_words & t_words) / len(q_words)


def hybrid_search(query, all_chunks, all_embeddings, k=5, doc_filter=None,
                  alpha=0.70, min_score=0.10):
    from sklearn.metrics.pairwise import cosine_similarity
    if all_embeddings is None or len(all_chunks) == 0:
        return []
    model   = load_embedder()
    q_emb   = model.encode([query])
    indices = (
        [i for i, c in enumerate(all_chunks) if c["doc"] in doc_filter]
        if doc_filter else list(range(len(all_chunks)))
    )
    if not indices:
        return []
    filtered_embs = all_embeddings[indices]
    sem_scores    = cosine_similarity(q_emb, filtered_embs)[0]
    kw_scores     = np.array([_keyword_score(query, all_chunks[i]["text"]) for i in indices])
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
        results.append({
            "text":      all_chunks[global_idx]["text"],
            "page":      all_chunks[global_idx]["page"],
            "doc":       all_chunks[global_idx]["doc"],
            "score":     score,
            "sem_score": float(sem_scores[local_idx]),
        })
    return results


# ── LLM helpers ───────────────────────────────────────────────────────────────
def _build_messages(system, user_msg, history):
    msgs = [{"role": "system", "content": system}]
    for turn in history[-4:]:
        msgs.append({"role": "user",      "content": sanitize_llm_text(turn["q"])})
        msgs.append({"role": "assistant", "content": sanitize_llm_text(turn["a"])})
    msgs.append({"role": "user", "content": user_msg})
    return msgs


def _context_from_results(results) -> str:
    if not results:
        return "NO_CONTEXT_FOUND"
    return "\n\n---\n\n".join(
        f"[Source: {r['doc']} | Page {r['page']} | Relevance: {int(r['score']*100)}%]\n{r['text']}"
        for r in results
    )


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


def _qa_user_msg(context, question) -> str:
    return (
        f"RETRIEVED CONTEXT:\n{context}\n\n"
        f"QUESTION:\n{question}\n\n"
        "Instructions:\n"
        "- Answer briefly and cite sources from the context.\n"
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


def call_groq(system, user_msg, history) -> str:
    try:
        resp = _groq_client().chat.completions.create(
            model=st.session_state.model_choice,
            messages=_build_messages(system, user_msg, history),
            max_tokens=1024, temperature=0.3,
        )
        return sanitize_llm_text(resp.choices[0].message.content.strip())
    except Exception as e:
        return _handle_groq_error(str(e))


def call_groq_stream(system, user_msg, history):
    try:
        stream = _groq_client().chat.completions.create(
            model=st.session_state.model_choice,
            messages=_build_messages(system, user_msg, history),
            max_tokens=1024, temperature=0.3, stream=True,
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


def get_summary(full_text) -> str:
    system   = "You are a document analyst. Be structured, concise, and factual."
    user_msg = (
        "Provide a structured document summary with these sections:\n"
        "Main Topic:\nKey Points:\nImportant Data/Facts:\nConclusion:\n\n"
        f"Document:\n{full_text[:4500]}"
    )
    return call_groq(system, user_msg, [])


def get_suggestions(docs_dict) -> list:
    combined = "".join(m["full_text"][:1200] + "\n\n" for m in docs_dict.values())
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


def generate_quiz(doc_texts: str, n: int = 6) -> list:
    """
    Generate n multiple-choice questions from the document text.
    Returns a list of dicts: {q, options: [4 strings], answer: int 0-3, explanation}
    """
    system = (
        "Generate multiple-choice quiz questions from this document. "
        "Output ONLY a valid Python list of dicts with these exact keys: "
        "q (question string), options (list of exactly 4 strings), "
        "answer (int 0-3 = index of correct option), explanation (1-2 sentence string). "
        "Example: [{\"q\": \"What is X?\", \"options\": [\"A\",\"B\",\"C\",\"D\"], "
        "\"answer\": 2, \"explanation\": \"Because...\"}, ...]. "
        "No markdown, no preamble. Questions must be answerable from the document only."
    )
    user_msg = (
        f"Generate exactly {n} quiz questions from this document:\n\n{doc_texts[:5000]}"
    )
    raw = call_groq(system, user_msg, [])
    try:
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            items = ast.literal_eval(match.group())
            if isinstance(items, list):
                valid = [
                    item for item in items
                    if (item.get("q")
                        and isinstance(item.get("options"), list)
                        and len(item["options"]) == 4
                        and isinstance(item.get("answer"), int)
                        and 0 <= item["answer"] <= 3)
                ]
                if valid:
                    return valid
    except Exception:
        pass
    # Fallback
    return [{
        "q": "What is the primary subject of this document?",
        "options": ["Could not generate", "Please try again", "Re-upload document", "Check API key"],
        "answer": 0,
        "explanation": "Quiz generation failed — please try again.",
    }]


def build_export(history, doc_names) -> str:
    lines = [
        "NEXUS AI — CHAT EXPORT", "=" * 60,
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Documents: {', '.join(doc_names) if doc_names else 'None'}",
        "=" * 60, "",
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
    # App
    "mode":          "chat",   # "chat" | "quiz"
    "history":       [],
    "all_chunks":    [],
    "all_embeddings": None,
    "docs":          {},
    "summaries":     {},
    "suggestions":   [],
    "prefill":       "",
    "doc_filter":    None,
    "groq_key":      os.environ.get("GROQ_API_KEY", ""),
    "model_choice":  "llama-3.1-8b-instant",
    "top_k":         5,
    # Quiz
    "quiz_items":     [],
    "quiz_index":     0,
    "quiz_score":     0,
    "quiz_done":      False,
    "quiz_generated": False,
    "quiz_answered":  False,
    "quiz_chosen":    -1,
    "quiz_n":         6,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


def active_key_ok() -> bool:
    return bool(st.session_state.groq_key)


def reset_app():
    for k in ["history","all_chunks","all_embeddings","docs","summaries",
              "suggestions","prefill","doc_filter",
              "quiz_items","quiz_index","quiz_score","quiz_done",
              "quiz_generated","quiz_answered","quiz_chosen"]:
        st.session_state[k] = _DEFAULTS[k]
    st.rerun()


def clear_chat_only():
    st.session_state.history = []
    st.session_state.prefill  = ""
    st.rerun()


def reset_quiz():
    for k in ["quiz_items","quiz_index","quiz_score","quiz_done",
              "quiz_generated","quiz_answered","quiz_chosen"]:
        st.session_state[k] = _DEFAULTS[k]


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

    # ── Mode tabs ──────────────────────────────────────────────────────────────
    st.markdown("### > MODE")
    mode_cols = st.columns(2)
    for col, (key, label) in zip(mode_cols, [("chat", "[ CHAT ]"), ("quiz", "[ QUIZ ]")]):
        with col:
            active = st.session_state.mode == key
            st.markdown(f'<div class="{"mode-active" if active else ""}">', unsafe_allow_html=True)
            if st.button(label, key=f"mode_{key}", use_container_width=True):
                if st.session_state.mode != key:
                    st.session_state.mode = key
                    if key == "quiz":
                        reset_quiz()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── API key ────────────────────────────────────────────────────────────────
    st.markdown("### > API KEY")
    groq_value = st.text_input(
        "groq_key", value=st.session_state.groq_key,
        placeholder="gsk_...", type="password", label_visibility="collapsed",
    )
    st.session_state.groq_key = groq_value

    # ── Model selector ─────────────────────────────────────────────────────────
    st.markdown("### > MODEL")
    model_labels = list(GROQ_MODELS.values())
    model_keys   = list(GROQ_MODELS.keys())
    cur_idx = model_keys.index(st.session_state.model_choice) if st.session_state.model_choice in model_keys else 0
    chosen_label = st.selectbox("model_select", model_labels, index=cur_idx, label_visibility="collapsed")
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
                        new_embs if st.session_state.all_embeddings is None
                        else np.vstack([st.session_state.all_embeddings, new_embs])
                    )
                    st.session_state.docs[uploaded.name]      = meta
                    st.session_state.summaries[uploaded.name] = get_summary(meta["full_text"])
                    new_docs_loaded = True

            if new_docs_loaded:
                st.session_state.suggestions = get_suggestions(st.session_state.docs)
                st.session_state.history     = []
                st.session_state.prefill     = ""
                reset_quiz()
                st.success("Documents indexed.")

    if st.session_state.docs:
        # ── Focus selector ─────────────────────────────────────────────────────
        st.markdown("### > DOCUMENTS")
        doc_names     = list(st.session_state.docs.keys())
        focus_options = ["All documents"] + doc_names
        cur_focus = (
            st.session_state.doc_filter[0]
            if st.session_state.doc_filter and st.session_state.doc_filter[0] in doc_names
            else "All documents"
        )
        chosen_focus = st.selectbox(
            "focus", focus_options,
            index=focus_options.index(cur_focus),
            label_visibility="collapsed",
        )
        st.session_state.doc_filter = None if chosen_focus == "All documents" else [chosen_focus]

        # ── Top-K slider (chat only) ───────────────────────────────────────────
        if st.session_state.mode == "chat":
            st.markdown("### > RETRIEVAL DEPTH")
            st.session_state.top_k = st.slider(
                "top_k", min_value=3, max_value=10,
                value=st.session_state.top_k, step=1,
                label_visibility="collapsed",
            )
            st.markdown(
                f'<div style="color:#7ea57e;font-size:10px;margin-top:-0.4rem;">'
                f'Retrieving top {st.session_state.top_k} chunks per query</div>',
                unsafe_allow_html=True,
            )

        # ── Doc cards ──────────────────────────────────────────────────────────
        for doc_name, meta in st.session_state.docs.items():
            short_name    = doc_name if len(doc_name) <= 24 else doc_name[:21] + "..."
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
              <div class="stat"><div class="stat-val">{len(st.session_state.docs)}</div><div class="stat-key">docs</div></div>
              <div class="stat"><div class="stat-val">{total_pages}</div><div class="stat-key">pages</div></div>
              <div class="stat"><div class="stat-val">
                {round(total_words/1000,1) if total_words >= 1000 else total_words}
              </div><div class="stat-key">words</div></div>
            </div>
            <div style="margin-top:0.45rem; color:#7ea57e; font-size:10px;">
              {total_chunks} total chunks indexed
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
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

mode    = st.session_state.mode
has_doc = bool(st.session_state.docs)

# ── Landing (no docs) ─────────────────────────────────────────────────────────
if not has_doc:
    st.markdown(
        """
        <div class="boot-box">
          <div class="ascii">NEXUS - AI Document Assistant</div>
        </div>
        <div class="hero">
          <div class="hero-eyebrow">Semantic PDF Intelligence</div>
          <div class="hero-title">Talk to any PDF<br>Instantly.</div>
          <div class="hero-sub">
            Upload documents and explore them with hybrid semantic search,
            AI-powered answers, and a built-in quiz mode to test your knowledge.
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
              <div class="step-top">03 // LEARN</div>
              <div class="step-title">Chat or Quiz</div>
              <div class="step-desc">Get streamed answers or test yourself with MCQ quizzes.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════
# CHAT MODE
# ══════════════════════════════════════════════════════════════════
elif mode == "chat":
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

    if not st.session_state.history and st.session_state.suggestions:
        st.markdown('<div class="section-label">> SUGGESTED QUERIES</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, q in enumerate(st.session_state.suggestions):
            with cols[i % 2]:
                if st.button(q, key=f"suggest_{i}", use_container_width=True):
                    st.session_state.prefill = q
                    st.rerun()

    if st.session_state.history:
        st.markdown('<div class="section-label">> CONVERSATION LOG</div>', unsafe_allow_html=True)
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for turn in st.session_state.history:
            st.markdown(
                f'<div class="msg-user">'
                f'<div class="bubble-user">{safe(turn["q"])}</div>'
                f'<div class="user-tag">YOU</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(f"**NEXUS:**\n\n{render_answer(turn['a'])}")
            if turn.get("citations"):
                with st.expander(f"▸ {len(turn['citations'])} SOURCE(S) RETRIEVED", expanded=False):
                    for c in turn["citations"]:
                        score_pct = int(c["score"] * 100)
                        short_doc = c["doc"] if len(c["doc"]) <= 22 else c["doc"][:19] + "..."
                        snippet   = c["text"][:160].replace("\n", " ").strip() + "…"
                        st.markdown(
                            f"`{short_doc}` &nbsp;·&nbsp; `p.{c['page']}` &nbsp;·&nbsp; "
                            f"`{score_pct}% relevance`\n\n> {snippet}\n\n---"
                        )
        st.markdown('</div>', unsafe_allow_html=True)

    export_text = build_export(st.session_state.history, list(st.session_state.docs.keys()))
    st.download_button(
        "[ EXPORT CHAT ]", data=export_text,
        file_name=f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain", use_container_width=False,
    )

    st.markdown("### > QUERY")
    with st.form("query_form", clear_on_submit=True):
        prompt = st.text_input(
            "cmd", value=st.session_state.prefill,
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
            with st.spinner("Retrieving context..."):
                results = hybrid_search(
                    question, st.session_state.all_chunks,
                    st.session_state.all_embeddings,
                    k=st.session_state.top_k,
                    doc_filter=st.session_state.doc_filter,
                )
            st.markdown(
                f'<div class="msg-user">'
                f'<div class="bubble-user">{safe(question)}</div>'
                f'<div class="user-tag">YOU</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown("**NEXUS:**")
            raw_answer = st.write_stream(
                get_answer_stream(results, question, st.session_state.history)
            )
            answer = sanitize_llm_text(raw_answer)
            st.session_state.history.append({"q": question, "a": answer, "citations": results})
            st.session_state.prefill = ""
            st.rerun()

# ══════════════════════════════════════════════════════════════════
# QUIZ MODE
# ══════════════════════════════════════════════════════════════════
elif mode == "quiz":
    st.markdown(
        '<div class="boot-box"><div class="ascii">NEXUS :: QUIZ MODE</div></div>',
        unsafe_allow_html=True,
    )

    if not active_key_ok():
        st.error("Add your Groq API key in the sidebar to use Quiz mode.")

    # ── Setup screen ──────────────────────────────────────────────────────────
    elif not st.session_state.quiz_generated:
        st.markdown(
            f"""
            <div class="summary-box" style="margin-bottom:1.1rem;">
              <div class="summary-title">HOW IT WORKS</div>
              <div class="summary-content">
                Nexus will generate multiple-choice questions directly from your
                loaded document(s). Pick a number of questions, hit generate, and
                test your knowledge. Each question shows the correct answer and
                an explanation after you respond.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("### > NUMBER OF QUESTIONS")
        quiz_n = st.number_input(
            "n_questions", min_value=3, max_value=20,
            value=st.session_state.quiz_n, step=1,
            label_visibility="collapsed",
        )
        st.session_state.quiz_n = int(quiz_n)

        # Which doc to quiz on
        doc_names = list(st.session_state.docs.keys())
        if len(doc_names) > 1:
            st.markdown("### > QUIZ ON")
            quiz_doc_focus = st.selectbox(
                "quiz_doc",
                ["All documents"] + doc_names,
                label_visibility="collapsed",
            )
        else:
            quiz_doc_focus = doc_names[0] if doc_names else "All documents"

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("[ GENERATE QUIZ ]", use_container_width=False):
            if not doc_names:
                st.warning("Upload a document first.")
            else:
                # Build text from selected scope
                if quiz_doc_focus == "All documents":
                    combined_text = "\n\n".join(
                        m["full_text"] for m in st.session_state.docs.values()
                    )
                else:
                    combined_text = st.session_state.docs[quiz_doc_focus]["full_text"]

                with st.spinner(f"Generating {st.session_state.quiz_n} questions..."):
                    items = generate_quiz(combined_text, n=st.session_state.quiz_n)

                st.session_state.quiz_items    = items
                st.session_state.quiz_index    = 0
                st.session_state.quiz_score    = 0
                st.session_state.quiz_done     = False
                st.session_state.quiz_generated = True
                st.session_state.quiz_answered  = False
                st.session_state.quiz_chosen    = -1
                st.rerun()

    # ── Results screen ────────────────────────────────────────────────────────
    elif st.session_state.quiz_done:
        total = len(st.session_state.quiz_items)
        score = st.session_state.quiz_score
        pct   = int(100 * score / total) if total else 0
        grade = (
            "EXCELLENT" if pct >= 80 else
            "GOOD JOB"  if pct >= 60 else
            "KEEP STUDYING"
        )
        st.markdown(
            f"""
            <div class="score-box">
              <div class="score-grade">{grade}</div>
              <div class="score-big">{pct}%</div>
              <div class="score-sub">{score} / {total} correct</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("[ RETRY ]", use_container_width=True):
                st.session_state.quiz_index    = 0
                st.session_state.quiz_score    = 0
                st.session_state.quiz_done     = False
                st.session_state.quiz_answered = False
                st.session_state.quiz_chosen   = -1
                st.rerun()
        with c2:
            if st.button("[ NEW QUIZ ]", use_container_width=True):
                reset_quiz()
                st.rerun()
        with c3:
            if st.button("[ BACK TO CHAT ]", use_container_width=True):
                reset_quiz()
                st.session_state.mode = "chat"
                st.rerun()

    # ── Active question ───────────────────────────────────────────────────────
    else:
        items   = st.session_state.quiz_items
        total   = len(items)
        idx     = st.session_state.quiz_index
        item    = items[idx]
        pct_bar = int(100 * idx / total)

        # Progress header
        st.markdown(
            f"""
            <div class="quiz-header">
              <div class="quiz-header-top">
                <span class="quiz-title">> QUIZ MODE</span>
                <span class="quiz-counter">Q {idx+1} / {total} &nbsp;·&nbsp;
                  Score: {st.session_state.quiz_score}</span>
              </div>
              <div class="quiz-bar-bg">
                <div class="quiz-bar-fill" style="width:{pct_bar}%"></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Question
        st.markdown(
            f"""
            <div class="quiz-question">
              <div class="quiz-q-label">QUESTION {idx+1}</div>
              <div class="quiz-q-text">{safe(item['q'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        answered    = st.session_state.quiz_answered
        chosen      = st.session_state.quiz_chosen
        correct_idx = item["answer"]

        if not answered:
            # Show clickable option buttons
            for oi, opt in enumerate(item["options"]):
                label = f"  {chr(65+oi)}.  {opt}"
                if st.button(label, key=f"qopt_{idx}_{oi}", use_container_width=True):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_chosen   = oi
                    if oi == correct_idx:
                        st.session_state.quiz_score += 1
                    st.rerun()
        else:
            # Show colour-coded results
            for oi, opt in enumerate(item["options"]):
                if oi == correct_idx:
                    cls, marker = "correct", "  ✓  CORRECT"
                elif oi == chosen:
                    cls, marker = "wrong", "  ✗  YOUR ANSWER"
                else:
                    cls, marker = "neutral", ""
                st.markdown(
                    f'<div class="quiz-opt {cls}">'
                    f'{chr(65+oi)}.  {safe(opt)}'
                    f'<span style="float:right;font-size:10px;letter-spacing:0.1em;">{marker}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # Result + explanation
            result_cls  = "quiz-result-correct" if chosen == correct_idx else "quiz-result-wrong"
            result_text = "CORRECT!" if chosen == correct_idx else (
                f"INCORRECT — correct answer: {item['options'][correct_idx]}"
            )
            explanation = safe(item.get("explanation", ""))
            st.markdown(
                f"""
                <div class="quiz-explanation">
                  <span class="{result_cls}">{result_text}</span>
                  {"<br><br>" + explanation if explanation else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            next_label = "[ FINISH QUIZ ]" if idx + 1 >= total else "[ NEXT QUESTION ]"
            if st.button(next_label, use_container_width=False):
                if idx + 1 >= total:
                    st.session_state.quiz_done = True
                else:
                    st.session_state.quiz_index    += 1
                    st.session_state.quiz_answered  = False
                    st.session_state.quiz_chosen    = -1
                st.rerun()

            # Exit mid-quiz
            if st.button("[ ABANDON QUIZ ]", use_container_width=False):
                reset_quiz()
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