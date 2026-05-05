
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

[data-testid="stSidebar"] .stFileUploader {
  padding-top: 0.25rem;
}

[data-testid="stSidebar"] .stFileUploader label {
  display: none !important;
}

/* Remove big upload container styling */
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  min-height: auto !important;
  display: block !important;
}

/* Remove helper text */
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] {
  display: none !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] p {
  display: none !important;
}

/* Clean actual button */
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

/* Hover */
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
  .grid-3 {
    grid-template-columns: 1fr;
  }
}

.step-card {
  padding: 0.95rem;
}

.step-top {
  color: var(--amber);
  font-size: 11px;
  margin-bottom: 0.65rem;
}

.step-title {
  color: var(--fg);
  font-weight: 700;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
}

.step-desc {
  color: #93c493;
  font-size: 12px;
  line-height: 1.65;
}

.section-label {
  color: var(--amber);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin: 1.1rem 0 0.55rem;
}

.summary-box {
  padding: 1rem;
  margin-bottom: 0.75rem;
}

.summary-title {
  color: var(--amber);
  font-size: 11px;
  letter-spacing: 0.16em;
  margin-bottom: 0.65rem;
  text-transform: uppercase;
}

.summary-content {
  color: #9cd09c;
  line-height: 1.75;
  font-size: 13px;
}

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

.doc-icon {
  background: #071107;
}

.doc-info {
  min-width: 0;
  flex: 1;
}

.doc-name {
  color: var(--fg);
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-meta {
  color: #86b586;
  font-size: 10px;
  margin-top: 0.2rem;
}

.badge {
  color: var(--amber);
  border: 1px solid var(--border);
  padding: 0.2rem 0.4rem;
  font-size: 9px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.stat {
  border: 1px solid var(--border);
  background: var(--panel);
  padding: 0.8rem 0.45rem;
  text-align: center;
}

.stat-val {
  color: var(--fg);
  font-size: 1.15rem;
  font-weight: 800;
  line-height: 1;
}

.stat-key {
  color: #82aa82;
  text-transform: uppercase;
  font-size: 9px;
  margin-top: 0.35rem;
  letter-spacing: 0.12em;
}

.suggestion-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.6rem;
}

@media (max-width: 700px) {
  .suggestion-grid {
    grid-template-columns: 1fr;
  }
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

.chat-wrap {
  margin-top: 1rem;
}

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

.bubble-user {
  background: #0d2b0d;
  color: var(--fg);
}

.bubble-ai {
  color: #b8deb8;
}

.user-tag {
  color: var(--amber);
  font-size: 10px;
  letter-spacing: 0.14em;
  align-self: center;
  white-space: nowrap;
}

.ai-tag {
  color: var(--fg);
  font-size: 10px;
  letter-spacing: 0.14em;
  align-self: center;
  white-space: nowrap;
}

.citations-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.45rem 0 1rem 2.55rem;
}

.cite-card {
  background: var(--panel);
  border: 1px solid var(--border);
  padding: 0.3rem 0.55rem;
  font-size: 10px;
  display: inline-flex;
  gap: 0.45rem;
  align-items: center;
}

.cite-page {
  color: var(--fg);
}

.cite-score {
  color: var(--amber);
}

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

.stSpinner > div {
  border-top-color: var(--fg) !important;
}

::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  background: var(--bg);
}

::-webkit-scrollbar-thumb {
  background: var(--border);
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
    """
    Remove accidental HTML/code-block output from the model so the UI stays clean.
    """
    text = "" if text is None else str(text)
    text = text.replace("```", "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def render_answer(text: str) -> str:
    """
    Render as markdown, not HTML, so model output cannot inject raw tags.
    """
    return sanitize_llm_text(text)


def extract_pdf(file_obj, doc_name: str):
    file_obj.seek(0)
    reader = pypdf.PdfReader(file_obj)

    chunks = []
    full_text = ""
    chunk_size = 260
    overlap = 60

    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"
        words = page_text.split()

        start = 0
        while start < len(words):
            chunk_text = " ".join(words[start:start + chunk_size]).strip()
            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "page": page_idx + 1,
                        "doc": doc_name,
                    }
                )
            start += max(1, chunk_size - overlap)

    meta = {
        "pages": len(reader.pages),
        "words": len(re.findall(r"\b[\w'-]+\b", re.sub(r"\s+", " ", full_text).strip())),
        "chunks": len(chunks),
        "full_text": full_text[:5000],
    }
    return chunks, meta


def embed_chunks(chunks):
    model = load_embedder()
    texts = [c["text"] for c in chunks]
    if not texts:
        return np.empty((0, 384))
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
        results.append(
            {
                "text": all_chunks[global_idx]["text"],
                "page": all_chunks[global_idx]["page"],
                "doc": all_chunks[global_idx]["doc"],
                "score": float(scores[local_idx]),
            }
        )
    return results


def _build_messages(system, user_msg, history):
    messages = [{"role": "system", "content": system}]
    for turn in history[-4:]:
        messages.append({"role": "user", "content": sanitize_llm_text(turn["q"])})
        messages.append({"role": "assistant", "content": sanitize_llm_text(turn["a"])})
    messages.append({"role": "user", "content": user_msg})
    return messages


def call_groq(api_key: str, system: str, user_msg: str, history):
    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=_build_messages(system, user_msg, history),
            max_tokens=1024,
            temperature=0.3,
        )
        return sanitize_llm_text(response.choices[0].message.content.strip())
    except Exception as e:
        err = str(e)
        if "429" in err:
            return "⚠️ Rate limit reached. Please wait a moment and try again."
        if "401" in err or "invalid" in err.lower():
            return "⚠️ Invalid Groq API key. Please check the key in the sidebar."
        return f"⚠️ Groq error: {err}"


def call_llm(system: str, user_msg: str, history):
    return call_groq(st.session_state.groq_key, system, user_msg, history)


def get_answer(results, question, history):
    context_parts = []
    for r in results:
        score_pct = int(r["score"] * 100)
        context_parts.append(
            f"[Source: {r['doc']} | Page {r['page']} | Relevance: {score_pct}%]\n{r['text']}"
        )

    context = "\n\n---\n\n".join(context_parts) if context_parts else "NO_CONTEXT_FOUND"

    system = (
      "You are Nexus, a precise document assistant.\n"
      "Rules:\n"
      "- Use ONLY the provided CONTEXT to answer. Do NOT use external knowledge.\n"
      "- If the answer can be found verbatim or inferred from the context, give a short, factual answer (1-3 sentences).\n"
      "- If you infer, state it briefly as an inference.\n"
      "- If the answer cannot be found or reasonably inferred, respond: 'Answer not found in context.'\n"
      "- Do not output HTML, tags, or code blocks. Do not include step-by-step chains of thought.\n"
      "- Be concise and prioritize directly quoting or referencing context passages when relevant."
    )

    user_msg = (
      f"RETRIEVED CONTEXT:\n{context}\n\n"
      f"QUESTION:\n{question}\n\n"
      "Instructions:\n"
      "- Answer briefly and cite sources from the context using the required source markers.\n"
      "- If multiple context passages support the answer, list them separated by semicolons.\n"
      "- If nothing in the context answers the question, say exactly: 'Answer not found in context.'"
    )
    return call_llm(system, user_msg, history)


def get_summary(full_text):
    system = "You are a document analyst. Be structured, concise, and factual."
    user_msg = (
        "Provide a structured document summary with these sections:\n"
        "Main Topic:\n"
        "Key Points:\n"
        "Important Data/Facts:\n"
        "Conclusion:\n\n"
        f"Document:\n{full_text[:4500]}"
    )
    return call_llm(system, user_msg, [])


def get_suggestions(full_text):
    system = "Output ONLY a Python list of 4 strings. No markdown, no explanation."
    user_msg = (
        'Generate 4 insightful questions for this document.\n'
        'Format exactly like: ["Q1?","Q2?","Q3?","Q4?"]\n\n'
        f"{full_text[:2500]}"
    )
    raw = call_llm(system, user_msg, [])

    try:
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
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


def build_export(history, doc_names):
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
defaults = {
    "history": [],
    "all_chunks": [],
    "all_embeddings": None,
    "docs": {},           # doc_name -> meta
    "summaries": {},      # doc_name -> summary
    "suggestions": [],
    "prefill": "",
    "doc_filter": None,   # None or [doc_name, ...]
    "groq_key": os.environ.get("GROQ_API_KEY", ""),
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def active_key_ok():
    return bool(st.session_state.groq_key)


def reset_app():
    st.session_state.history = []
    st.session_state.all_chunks = []
    st.session_state.all_embeddings = None
    st.session_state.docs = {}
    st.session_state.summaries = {}
    st.session_state.suggestions = []
    st.session_state.prefill = ""
    st.session_state.doc_filter = None
    st.rerun()


# =============================================================================
# Sidebar
# =============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 1rem 0.9rem 0.8rem; border-bottom: 1px solid var(--border); margin-bottom: 0.9rem;">
          <div style="color: var(--fg); font-weight: 800; font-size: 16px; letter-spacing: 0.08em;">
            NEXUS AI
          </div>
          <div style="color: var(--amber); font-size: 10px; letter-spacing: 0.18em; margin-top: 0.35rem;">
            TERMINAL PDF RAG
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### > API KEY")
    groq_value = st.text_input(
        "groq_key",
        value=st.session_state.groq_key,
        placeholder="gsk_...",
        type="password",
        label_visibility="collapsed",
    )
    st.session_state.groq_key = groq_value

    st.markdown("### > LOAD DOCUMENTS")
    uploaded_files = st.file_uploader(
        "ADD PDF(S)",
        type="pdf",
        accept_multiple_files=True,
    )

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
                    new_embs = embed_chunks(new_chunks)

                    st.session_state.all_chunks.extend(new_chunks)
                    if st.session_state.all_embeddings is None:
                        st.session_state.all_embeddings = new_embs
                    else:
                        st.session_state.all_embeddings = np.vstack(
                            [st.session_state.all_embeddings, new_embs]
                        )

                    st.session_state.docs[uploaded.name] = meta
                    st.session_state.summaries[uploaded.name] = get_summary(meta["full_text"])
                    st.session_state.suggestions = get_suggestions(meta["full_text"])
                    new_docs_loaded = True

            if new_docs_loaded:
                st.session_state.history = []
                st.session_state.prefill = ""
                st.success("Documents indexed.")

    if st.session_state.docs:
        st.markdown("### > DOCUMENTS")
        doc_names = list(st.session_state.docs.keys())
        focus_options = ["All documents"] + doc_names
        current_focus = "All documents"
        if st.session_state.doc_filter:
            current_focus = st.session_state.doc_filter[0] if st.session_state.doc_filter[0] in doc_names else "All documents"

        chosen_focus = st.selectbox(
            "focus",
            focus_options,
            index=focus_options.index(current_focus),
            label_visibility="collapsed",
        )
        st.session_state.doc_filter = None if chosen_focus == "All documents" else [chosen_focus]

        for doc_name, meta in st.session_state.docs.items():
            short_name = doc_name if len(doc_name) <= 24 else doc_name[:21] + "..."
            words_display = f"{meta['words']:,}" if meta["words"] < 10000 else f"{round(meta['words']/1000, 1)}k"

            st.markdown(
                f"""
                <div class="doc-card">
                  <div class="doc-icon">PDF</div>
                  <div class="doc-info">
                    <div class="doc-name">{safe(short_name)}</div>
                    <div class="doc-meta">{meta['pages']} pages · {words_display} words · {meta['chunks']} chunks</div>
                  </div>
                  <div class="badge">{meta['pages']}p</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        total_pages = sum(m["pages"] for m in st.session_state.docs.values())
        total_words = sum(m["words"] for m in st.session_state.docs.values())
        total_chunks = sum(m["chunks"] for m in st.session_state.docs.values())

        st.markdown(
            f"""
            <div class="stats">
              <div class="stat"><div class="stat-val">{len(st.session_state.docs)}</div><div class="stat-key">docs</div></div>
              <div class="stat"><div class="stat-val">{total_pages}</div><div class="stat-key">pages</div></div>
              <div class="stat"><div class="stat-val">{round(total_words/1000,1) if total_words >= 1000 else total_words}</div><div class="stat-key">words</div></div>
            </div>
            <div style="margin-top:0.45rem; color:#7ea57e; font-size:10px;">{total_chunks} total chunks indexed</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        if st.button("[ CLEAR ALL DOCUMENTS ]", use_container_width=True):
            reset_app()

    st.markdown("---")
    


# =============================================================================
# Main area
# =============================================================================
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

if not st.session_state.docs:
    st.markdown(
        """
        <div class="boot-box">
          <div class="ascii">NEXUS - AI Document Assistant</div>
        </div>
        <div class="hero">
          <div class="hero-eyebrow">Semantic PDF Intelligence</div>
          <div class="hero-title">Talk to any PDF <br>Instantly.</div>
          <div class="hero-sub">
            Upload documents and explore them with semantic search and AI-powered answers.
            Open the sidebar from the top-left control to load files or update the API key.
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
              <div class="step-desc">Chunks are embedded with all-MiniLM-L6-v2 for retrieval.</div>
            </div>
            <div class="card step-card">
              <div class="step-top">03 // QUERY</div>
              <div class="step-title">Ask questions</div>
              <div class="step-desc">Answers are grounded in retrieved pages and citations.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
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
                f"""
                <div class="msg-user">
                  <div class="bubble-user">{safe(turn['q'])}</div>
                  <div class="user-tag">YOU</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Use markdown rendering only — no HTML injection path.
            st.markdown(
                f"**NEXUS:**\n\n{render_answer(turn['a'])}",
            )

            if turn.get("citations"):
                st.markdown("**SOURCES**")
                for c in turn["citations"]:
                    score_pct = int(c["score"] * 100)
                    short_doc = c["doc"] if len(c["doc"]) <= 18 else c["doc"][:15] + "..."
                    st.markdown(
                        f"- `FILE:{short_doc}`  ·  `P.{c['page']}`  ·  `{score_pct}%`"
                    )

        st.markdown('</div>', unsafe_allow_html=True)

    export_text = build_export(st.session_state.history, list(st.session_state.docs.keys()))
    st.download_button(
        "[ EXPORT CHAT ]",
        data=export_text,
        file_name=f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=False,
    )

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
            with st.spinner("Searching documents and generating answer..."):
                results = semantic_search(
                    question,
                    st.session_state.all_chunks,
                    st.session_state.all_embeddings,
                    k=5,
                    doc_filter=st.session_state.doc_filter,
                )
                answer = get_answer(results, question, st.session_state.history)

            st.session_state.history.append(
                {
                    "q": question,
                    "a": answer,
                    "citations": results,
                }
            )
            st.session_state.prefill = ""
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
