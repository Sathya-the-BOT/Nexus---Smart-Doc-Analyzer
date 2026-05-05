import streamlit as st
import pypdf
import numpy as np
import os
import re
import ast
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS // DOC-AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Terminal CLI CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=swap');

:root {
  --bg:        #0a0a0a;
  --surface:   #0d0d0d;
  --surface2:  #111111;
  --green:     #33ff00;
  --green-dim: #1a3f1a;
  --amber:     #ffb000;
  --red:       #ff3333;
  --muted:     #2a6b2a;
  --border:    #1f521f;
  --glow:      0 0 6px rgba(51,255,0,0.45);
  --glow-sm:   0 0 3px rgba(51,255,0,0.3);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
  font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
  background: var(--bg) !important;
  color: var(--green);
}
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: var(--bg) !important; }

/* CRT scanlines */
.stApp::before {
  content: '';
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px
  );
  pointer-events: none;
  z-index: 9999;
}

/* ── SIDEBAR COLLAPSE FIX ── */
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] * {
  display: flex !important;
  visibility: visible !important;
  opacity: 1 !important;
}
[data-testid="collapsedControl"] {
  background: var(--bg) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="collapsedControl"] svg { color: var(--green) !important; }
section[data-testid="stSidebarCollapsedControl"] {
  display: flex !important;
  visibility: visible !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] * {
  color: var(--green) !important;
  font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stSidebar"] .stFileUploader label { display: none !important; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  background: var(--bg) !important;
  border: 1px dashed var(--border) !important;
  border-radius: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--green) !important;
  background: rgba(51,255,0,0.03) !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] p {
  color: var(--muted) !important; font-size: 11px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
  background: var(--bg) !important;
  border: 1px solid var(--border) !important;
  color: var(--green) !important;
  border-radius: 0 !important; font-size: 11px !important;
}
[data-testid="stSidebar"] .stRadio label { font-size: 11px !important; }
[data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] { display: none !important; }
[data-testid="stSidebar"] .stTextInput input {
  background: var(--bg) !important;
  border: 0 !important;
  border-bottom: 1px solid var(--border) !important;
  border-radius: 0 !important;
  color: var(--green) !important;
  font-size: 11px !important;
  font-family: 'JetBrains Mono', monospace !important;
  text-shadow: var(--glow-sm);
}
[data-testid="stSidebar"] .stTextInput input:focus {
  border-bottom-color: var(--green) !important;
  box-shadow: none !important;
}
[data-testid="stSidebar"] .stTextInput label { display: none !important; }
[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--muted) !important;
  border-radius: 0 !important;
  width: 100% !important;
  font-size: 10px !important;
  padding: 6px 10px !important;
  font-family: 'JetBrains Mono', monospace !important;
  letter-spacing: 1px;
  transition: all 0.1s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: var(--red) !important;
  border-color: var(--red) !important;
  color: var(--bg) !important;
}

/* Alerts */
.stSuccess {
  background: rgba(51,255,0,0.05) !important;
  border: 1px solid var(--green) !important;
  border-radius: 0 !important;
}
.stError {
  background: rgba(255,51,51,0.07) !important;
  border: 1px solid var(--red) !important;
  border-radius: 0 !important;
}
[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 !important;
}
[data-testid="stExpander"] summary {
  color: var(--muted) !important;
  font-size: 11px !important;
  font-family: 'JetBrains Mono', monospace !important;
}

/* Main buttons */
.stButton > button {
  background: var(--bg) !important;
  border: 1px solid var(--border) !important;
  color: var(--muted) !important;
  border-radius: 0 !important;
  padding: 10px 14px !important;
  font-size: 11px !important;
  font-family: 'JetBrains Mono', monospace !important;
  text-align: left !important;
  width: 100% !important;
  height: auto !important;
  white-space: normal !important;
  line-height: 1.5 !important;
  transition: all 0.1s !important;
}
.stButton > button:hover {
  background: var(--green) !important;
  border-color: var(--green) !important;
  color: var(--bg) !important;
}

/* Chat input */
[data-testid="stChatInput"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--green) !important;
  box-shadow: var(--glow-sm) !important;
}
[data-testid="stChatInput"] textarea {
  background: var(--surface) !important;
  border: none !important;
  color: var(--green) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 13px !important;
  text-shadow: var(--glow-sm);
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }
[data-testid="stChatInput"] button {
  background: var(--green) !important; border-radius: 0 !important;
}
[data-testid="stChatInput"] button svg { color: var(--bg) !important; }

/* Download btn */
.stDownloadButton > button {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--muted) !important;
  border-radius: 0 !important;
  font-size: 10px !important;
  font-family: 'JetBrains Mono', monospace !important;
  letter-spacing: 1px;
}
.stDownloadButton > button:hover {
  border-color: var(--amber) !important;
  color: var(--amber) !important;
}

.stSpinner > div { border-top-color: var(--green) !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); }
::-webkit-scrollbar-thumb:hover { background: var(--green); }

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
@keyframes rise {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
.cursor-block {
  display: inline-block;
  width: 8px; height: 14px;
  background: var(--green);
  vertical-align: middle;
  animation: blink 1s step-end infinite;
}
</style>
""", unsafe_allow_html=True)


# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')


# ── PDF ───────────────────────────────────────────────────────────────────────
def extract_pdf(file, doc_name):
    file.seek(0)
    reader = pypdf.PdfReader(file)
    chunks, full_text = [], ""
    SIZE, OVL = 280, 55
    for pi, page in enumerate(reader.pages):
        pt = page.extract_text() or ""
        full_text += pt + "\n"
        words = pt.split()
        s = 0
        while s < len(words):
            ct = " ".join(words[s:s+SIZE])
            if ct.strip():
                chunks.append({"text": ct, "page": pi+1, "doc": doc_name})
            s += SIZE - OVL
    meta = {"pages": len(reader.pages), "words": len(full_text.split()),
            "chunks": len(chunks), "full_text": full_text[:5000]}
    return chunks, meta


def embed_chunks(chunks):
    return load_embedder().encode([c["text"] for c in chunks],
                                   show_progress_bar=False, batch_size=32)


def semantic_search(query, all_chunks, all_embs, k=5, doc_filter=None):
    from sklearn.metrics.pairwise import cosine_similarity
    if all_embs is None or not all_chunks:
        return []
    q_emb = load_embedder().encode([query])
    idxs = ([i for i,c in enumerate(all_chunks) if c["doc"] in doc_filter]
            if doc_filter else list(range(len(all_chunks))))
    if not idxs:
        return []
    scores = cosine_similarity(q_emb, all_embs[idxs])[0]
    top = np.argsort(scores)[::-1][:k]
    return [{"text": all_chunks[idxs[i]]["text"],
             "page": all_chunks[idxs[i]]["page"],
             "doc":  all_chunks[idxs[i]]["doc"],
             "score": float(scores[i])} for i in top]


# ── LLMs ─────────────────────────────────────────────────────────────────────
def _msgs(system, user_msg, history):
    m = [{"role": "system", "content": system}]
    for h in history[-4:]:
        m += [{"role":"user","content":h["q"]},{"role":"assistant","content":h["a"]}]
    m.append({"role":"user","content":user_msg})
    return m


def call_groq(api_key, system, user_msg, history):
    try:
        from groq import Groq
        r = Groq(api_key=api_key).chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=_msgs(system, user_msg, history),
            max_tokens=1024, temperature=0.3)
        return r.choices[0].message.content.strip()
    except Exception as e:
        err = str(e)
        if "429" in err: return "[ERR] RATE_LIMIT — wait and retry."
        if "401" in err: return "[ERR] INVALID_GROQ_KEY — check sidebar."
        return f"[ERR] {err}"


def call_gemini(api_key, system, user_msg, history):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        # ── FIXED: gemini-2.0-flash ───────────────────────────────────────────
        mdl = genai.GenerativeModel(model_name="gemini-2.0-flash",
                                     system_instruction=system)
        hist = []
        for h in history[-4:]:
            hist += [{"role":"user","parts":[h["q"]]},
                     {"role":"model","parts":[h["a"]]}]
        return mdl.start_chat(history=hist).send_message(user_msg).text
    except Exception as e:
        err = str(e)
        if "API_KEY" in err or "invalid" in err.lower():
            return "[ERR] INVALID_GEMINI_KEY — check sidebar."
        return f"[ERR] {err}"


def call_llm(provider, keys, system, user_msg, history):
    return (call_groq(keys.get("groq",""), system, user_msg, history)
            if provider == "Groq"
            else call_gemini(keys.get("gemini",""), system, user_msg, history))


def get_answer(provider, keys, results, question, history):
    ctx = "\n\n---\n\n".join(
        f"[FILE:{r['doc']}|PAGE:{r['page']}|SCORE:{int(r['score']*100)}%]\n{r['text']}"
        for r in results)
    system = ("You are NEXUS, a precise document analysis AI.\n"
              "RULES: Answer ONLY from context. If not found say 'NOT_FOUND'.\n"
              "Cite page: 'Ref: Page X of <file>'. Use markdown formatting.")
    return call_llm(provider, keys, system,
                    f"CONTEXT:\n{ctx}\n\nQUERY: {question}", history)


def get_summary(provider, keys, full_text):
    system = "You are a document analysis system. Be structured and concise."
    return call_llm(provider, keys, system,
                    f"Summarize with: **TOPIC**, **KEY_POINTS**(4 bullets), "
                    f"**DATA_FACTS**(3 bullets), **CONCLUSION**\n\n{full_text[:4500]}", [])


def get_suggestions(provider, keys, full_text):
    system = 'Output ONLY a Python list of 4 strings. No markdown. No preamble.'
    raw = call_llm(provider, keys, system,
                   f'4 insightful questions. Format: ["Q1?","Q2?","Q3?","Q4?"]\n\n{full_text[:2500]}', [])
    try:
        m = re.search(r'\[.*?\]', raw, re.DOTALL)
        if m:
            qs = ast.literal_eval(m.group())
            if isinstance(qs, list) and len(qs) >= 4:
                return qs[:4]
    except Exception:
        pass
    return ["What is the main topic?", "What are the key findings?",
            "What data is presented?", "What are the recommendations?"]


def build_export(history, doc_names):
    lines = ["NEXUS // CHAT EXPORT", "="*50,
             f"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
             f"SOURCES:   {', '.join(doc_names)}", "="*50, ""]
    for i, t in enumerate(history, 1):
        lines += [f"[Q{i}] {t['q']}", f"[A{i}] {t['a']}"]
        if t.get("citations"):
            lines.append("[REF] " + " | ".join(
                f"p.{c['page']} '{c['doc']}' {int(c['score']*100)}%"
                for c in t["citations"]))
        lines.append("")
    return "\n".join(lines)


# ── State ─────────────────────────────────────────────────────────────────────
for k, v in {"history":[],"all_chunks":[],"all_embeddings":None,
             "docs":{},"summaries":{},"suggestions":[],"prefill":"","provider":"Groq"}.items():
    if k not in st.session_state:
        st.session_state[k] = v

for k, env in [("groq_key","GROQ_API_KEY"),("gemini_key","GEMINI_API_KEY")]:
    if k not in st.session_state:
        st.session_state[k] = os.environ.get(env, "")

def get_keys():
    return {"groq": st.session_state.groq_key, "gemini": st.session_state.gemini_key}

def key_ok():
    k = get_keys()
    return bool(k["groq"] if st.session_state.provider == "Groq" else k["gemini"])


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown("""
    <div style="padding:16px 14px 12px;border-bottom:1px solid var(--border);">
      <pre style="color:var(--green);font-size:8.5px;line-height:1.25;
                  text-shadow:var(--glow);margin:0;overflow:hidden;">
 _  _ _____  ____  _  _  ___
( \\( | ___ \\( _  )( \\/ )/ __)
 )  ( | ____/  )(   )  ( \\__ \\
(_)\\_)|_____)__)(  (_/\\_)(___/</pre>
      <div style="font-size:9px;color:var(--muted);letter-spacing:2px;margin-top:6px;">
        DOC-ANALYSIS-SYSTEM v2.0
      </div>
    </div>""", unsafe_allow_html=True)

    # provider
    st.markdown('<div style="padding:12px 14px 0;"><div style="font-size:9px;'
                'color:var(--muted);letter-spacing:2px;margin-bottom:8px;">'
                '// SELECT_PROVIDER</div></div>', unsafe_allow_html=True)
    provider = st.radio("prov", ["Groq","Gemini"], horizontal=True,
                        index=0 if st.session_state.provider=="Groq" else 1,
                        label_visibility="collapsed")
    st.session_state.provider = provider

    # api key
    st.markdown(f'<div style="padding:10px 14px 0;"><div style="font-size:9px;'
                f'color:var(--muted);letter-spacing:2px;margin-bottom:6px;">'
                f'// API_KEY [{provider.upper()}]</div>'
                f'<div style="font-size:10px;color:var(--muted);">'
                f'{"$ export GROQ=" if provider=="Groq" else "$ export GEMINI="}'
                f'</div></div>', unsafe_allow_html=True)
    if provider == "Groq":
        k = st.text_input("gk", value=st.session_state.groq_key,
                          placeholder="gsk_...", type="password",
                          label_visibility="collapsed")
        st.session_state.groq_key = k
    else:
        k = st.text_input("mk", value=st.session_state.gemini_key,
                          placeholder="AIza...", type="password",
                          label_visibility="collapsed")
        st.session_state.gemini_key = k

    # upload
    st.markdown('<div style="height:1px;background:var(--border);margin:12px 0;"></div>'
                '<div style="padding:0 14px;"><div style="font-size:9px;color:var(--muted);'
                'letter-spacing:2px;margin-bottom:8px;">// LOAD_DOCUMENT --type=pdf'
                '</div></div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("pdf", type="pdf", label_visibility="collapsed")

    if uploaded:
        if not key_ok():
            st.error("[ERR] API_KEY_MISSING")
        elif uploaded.name not in st.session_state.docs:
            with st.spinner("INDEXING DOCUMENT..."):
                new_chunks, meta = extract_pdf(uploaded, uploaded.name)
                new_embs = embed_chunks(new_chunks)
                st.session_state.all_chunks.extend(new_chunks)
                st.session_state.all_embeddings = (
                    new_embs if st.session_state.all_embeddings is None
                    else np.vstack([st.session_state.all_embeddings, new_embs]))
                st.session_state.docs[uploaded.name] = meta
                st.session_state.summaries[uploaded.name] = get_summary(
                    provider, get_keys(), meta["full_text"])
                st.session_state.suggestions = get_suggestions(
                    provider, get_keys(), meta["full_text"])
                st.session_state.history = []
            st.success(f"[OK] {meta['pages']}pp / {meta['chunks']} chunks indexed")

    # loaded docs
    if st.session_state.docs:
        st.markdown('<div style="height:1px;background:var(--border);margin:12px 0;"></div>'
                    '<div style="padding:0 14px;"><div style="font-size:9px;color:var(--muted);'
                    'letter-spacing:2px;margin-bottom:8px;">// LOADED_FILES</div></div>',
                    unsafe_allow_html=True)
        for doc_name, meta in st.session_state.docs.items():
            short = doc_name[:22]+".." if len(doc_name)>24 else doc_name
            w = f"{round(meta['words']/1000,1)}k" if meta['words']>=1000 else str(meta['words'])
            bf = min(int(meta['chunks']/8), 18)
            bar = "█"*bf + "░"*(18-bf)
            st.markdown(f"""
            <div style="margin:0 14px 7px;padding:8px 10px;
                        border:1px solid var(--border);background:var(--surface2);">
              <div style="font-size:10px;color:var(--green);text-shadow:var(--glow-sm);
                          overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                &gt; {short}
              </div>
              <div style="font-size:9px;color:var(--muted);margin-top:3px;">
                {meta['pages']}pp · {w}w · {meta['chunks']}c
              </div>
              <div style="font-size:8px;color:var(--muted);margin-top:3px;letter-spacing:-1px;">
                [{bar}]
              </div>
            </div>""", unsafe_allow_html=True)

        tp = sum(m["pages"] for m in st.session_state.docs.values())
        tw = sum(m["words"] for m in st.session_state.docs.values())
        tc = sum(m["chunks"] for m in st.session_state.docs.values())
        st.markdown(f"""
        <div style="margin:0 14px 10px;padding:7px 10px;
                    border:1px solid var(--green-dim);background:rgba(51,255,0,0.02);">
          <div style="font-size:9px;color:var(--muted);">
            TOTAL :: {len(st.session_state.docs)} docs · {tp}pp · {round(tw/1000,1)}k words
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div style="padding:0 14px 14px;">', unsafe_allow_html=True)
        if st.button("[ PURGE ALL DOCUMENTS ]", use_container_width=True):
            for ks in ["history","all_chunks","suggestions"]:
                st.session_state[ks] = []
            st.session_state.all_embeddings = None
            st.session_state.docs = {}
            st.session_state.summaries = {}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:10px 14px;border-top:1px solid var(--border);margin-top:8px;">
      <div style="font-size:8px;color:var(--muted);line-height:1.9;letter-spacing:0.3px;">
        GROQ   :: llama-3.1-8b-instant<br>
        GEMINI :: gemini-2.0-flash [FIXED]<br>
        EMBED  :: all-MiniLM-L6-v2<br>
        SEARCH :: cosine-similarity top-5
      </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div style="max-width:800px;margin:0 auto;padding:36px 24px 140px;">',
            unsafe_allow_html=True)

if not st.session_state.docs:
    st.markdown("""
    <div style="padding:20px 0 48px;">
      <div style="font-size:9px;color:var(--muted);letter-spacing:3px;margin-bottom:24px;">
        user@nexus:~$ ./nexus --init --mode=rag --version=2.0
      </div>
      <pre style="color:var(--green);font-size:clamp(14px,3.5vw,34px);
                  line-height:1.1;text-shadow:var(--glow);margin-bottom:8px;
                  font-family:'JetBrains Mono',monospace;overflow:hidden;">
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝</pre>
      <div style="font-size:11px;color:var(--amber);letter-spacing:2px;margin-bottom:28px;">
        // DOCUMENT INTELLIGENCE SYSTEM // SEMANTIC RAG // v2.0
      </div>
      <div style="font-size:12px;color:var(--muted);line-height:2.2;max-width:460px;margin-bottom:36px;">
        <span style="color:var(--green);text-shadow:var(--glow-sm);">[OK]</span> semantic vector search — not keyword matching<br>
        <span style="color:var(--green);text-shadow:var(--glow-sm);">[OK]</span> page-level citations + relevance scores<br>
        <span style="color:var(--green);text-shadow:var(--glow-sm);">[OK]</span> multi-PDF cross-document queries<br>
        <span style="color:var(--green);text-shadow:var(--glow-sm);">[OK]</span> dual LLM :: groq [llama] + gemini [2.0-flash]<br>
        <span style="color:var(--green);text-shadow:var(--glow-sm);">[OK]</span> auto-summary on document load
      </div>
      <div style="color:var(--border);font-size:11px;margin-bottom:24px;letter-spacing:1px;">
        ================================================
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1px;
                  border:1px solid var(--border);max-width:480px;">
        <div style="padding:14px 12px;border-right:1px solid var(--border);">
          <div style="font-size:9px;color:var(--muted);letter-spacing:1px;">// STEP_01</div>
          <div style="font-size:11px;color:var(--green);margin-top:6px;text-shadow:var(--glow-sm);">
            UPLOAD.PDF
          </div>
          <div style="font-size:9px;color:var(--muted);margin-top:4px;">sidebar &gt; load_doc</div>
        </div>
        <div style="padding:14px 12px;border-right:1px solid var(--border);">
          <div style="font-size:9px;color:var(--muted);letter-spacing:1px;">// STEP_02</div>
          <div style="font-size:11px;color:var(--green);margin-top:6px;text-shadow:var(--glow-sm);">
            INDEX.VEC
          </div>
          <div style="font-size:9px;color:var(--muted);margin-top:4px;">embeddings built</div>
        </div>
        <div style="padding:14px 12px;">
          <div style="font-size:9px;color:var(--muted);letter-spacing:1px;">// STEP_03</div>
          <div style="font-size:11px;color:var(--green);margin-top:6px;text-shadow:var(--glow-sm);">
            QUERY.ASK
          </div>
          <div style="font-size:9px;color:var(--muted);margin-top:4px;">cited answers</div>
        </div>
      </div>
      <div style="margin-top:28px;font-size:12px;color:var(--muted);">
        user@nexus:~$ <span class="cursor-block"></span>
      </div>
    </div>""", unsafe_allow_html=True)

else:
    # summaries
    for doc_name, summary in st.session_state.summaries.items():
        short = doc_name[:34]+".." if len(doc_name)>36 else doc_name
        with st.expander(f"// AUTO_SUMMARY :: {short}", expanded=False):
            st.markdown(f"""
            <div style="padding:14px 16px;border:1px solid var(--border);
                        border-left:3px solid var(--green);background:var(--surface2);">
              <div style="font-size:9px;color:var(--muted);letter-spacing:2px;margin-bottom:10px;">
                [PROC] SUMMARY :: {doc_name}
              </div>
              <div style="font-size:12px;color:var(--green);line-height:1.9;
                          text-shadow:var(--glow-sm);">{summary}</div>
            </div>""", unsafe_allow_html=True)

    # suggestions
    if not st.session_state.history and st.session_state.suggestions:
        st.markdown("""
        <div style="font-size:9px;color:var(--muted);letter-spacing:2px;
                    margin-bottom:12px;display:flex;align-items:center;gap:10px;">
          // SUGGESTED_QUERIES
          <span style="flex:1;height:1px;background:var(--border);display:inline-block;"></span>
        </div>""", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, q in enumerate(st.session_state.suggestions):
            with cols[i % 2]:
                if st.button(f"> {q}", key=f"sq_{i}"):
                    st.session_state.prefill = q
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # chat
    if st.session_state.history:
        for turn in st.session_state.history:
            # user
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:8px;
                        animation:rise 0.2s ease;">
              <div style="max-width:74%;padding:12px 16px;
                          background:rgba(51,255,0,0.05);
                          border:1px solid var(--green);
                          font-size:13px;color:var(--green);
                          line-height:1.65;text-shadow:var(--glow-sm);">
                <div style="font-size:9px;color:var(--muted);letter-spacing:1px;margin-bottom:5px;">
                  user@nexus:~$
                </div>
                {turn['q']}
              </div>
            </div>""", unsafe_allow_html=True)

            # ai
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:6px;
                        animation:rise 0.2s ease;">
              <div style="max-width:86%;padding:14px 18px;
                          background:var(--surface);
                          border:1px solid var(--border);
                          border-left:2px solid var(--green);
                          font-size:13px;color:var(--green);
                          line-height:1.85;text-shadow:var(--glow-sm);">
                <div style="font-size:9px;color:var(--muted);letter-spacing:1px;margin-bottom:6px;">
                  nexus@system [OK] ::
                </div>
                {turn['a']}
              </div>
            </div>""", unsafe_allow_html=True)

            # citations
            if turn.get("citations"):
                cite_html = ""
                for c in turn["citations"]:
                    bf = int(c["score"] * 10)
                    bar = "█"*bf + "░"*(10-bf)
                    ds = c["doc"][:16]+".." if len(c["doc"])>18 else c["doc"]
                    cite_html += f"""
                    <div style="padding:4px 10px;border:1px solid var(--border);
                                font-size:9px;color:var(--muted);
                                font-family:'JetBrains Mono',monospace;
                                display:flex;align-items:center;gap:8px;
                                background:var(--surface2);">
                      <span style="color:var(--amber);">REF</span>
                      <span style="color:var(--green);text-shadow:var(--glow-sm);">
                        p.{c['page']}
                      </span>
                      <span>{ds}</span>
                      <span style="color:var(--muted);">[{bar}]{int(c['score']*100)}%</span>
                    </div>"""
                st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:4px;'
                            f'margin-bottom:24px;">{cite_html}</div>',
                            unsafe_allow_html=True)

        exp = build_export(st.session_state.history,
                           list(st.session_state.docs.keys()))
        st.download_button(
            "[ EXPORT_CHAT --format=txt ]", data=exp,
            file_name=f"nexus_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain")

st.markdown('</div>', unsafe_allow_html=True)

# input
if st.session_state.docs:
    n = len(st.session_state.docs)
    ph = (f"query across {n} docs // press Enter..."
          if n > 1 else "user@nexus:~$ query document...")
    question = st.chat_input(ph)
    if st.session_state.prefill and not question:
        question = st.session_state.prefill
        st.session_state.prefill = ""
    if question:
        if not key_ok():
            st.error("[ERR] API_KEY_MISSING — add key in sidebar")
        else:
            with st.spinner("RETRIEVING... REASONING..."):
                results = semantic_search(question, st.session_state.all_chunks,
                                          st.session_state.all_embeddings, k=5)
                answer = get_answer(st.session_state.provider, get_keys(),
                                    results, question, st.session_state.history)
            st.session_state.history.append(
                {"q": question, "a": answer, "citations": results})
            st.rerun()
else:
    st.chat_input("// upload PDF to initialize...", disabled=True)