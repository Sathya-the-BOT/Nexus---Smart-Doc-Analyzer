# ⚡ Nexus AI — Smart Document Analyzer

A production-grade RAG (Retrieval-Augmented Generation) system for intelligent PDF Q&A with real semantic search, page-level citations, and multi-document support.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Real Semantic Search** | Uses `sentence-transformers` + cosine similarity — not keyword matching |
| **Multi-PDF Support** | Upload and query across multiple documents simultaneously |
| **Page Citations** | Every answer shows exact source page + relevance score |
| **Auto Summary** | Document is summarized automatically on upload |
| **Dual API** | Switch between Groq (Llama 3.1) and Google Gemini with one click |
| **Conversation Memory** | Follow-up questions retain context from previous turns |
| **Export Chat** | Download your full Q&A session as a text file |

---

## 🛠 Setup (Local)

### 1. Clone & install
```bash
git clone <your-repo>
cd nexus-ai
pip install -r requirements.txt
```

### 2. Get API keys (both free)
- **Groq**: https://console.groq.com → Create API key
- **Gemini**: https://aistudio.google.com → Get API key

### 3. Run
```bash
streamlit run app.py
```

Enter your API key(s) in the sidebar when the app opens.

---

## ☁️ Deploy to Streamlit Community Cloud (Recommended)

1. Push your code to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub → Select `app.py`
4. Add secrets in **Settings → Secrets**:
```toml
GROQ_API_KEY = "gsk_..."
GEMINI_API_KEY = "AIza..."
```
5. Click **Deploy** — done in ~2 minutes ✅

---

## 🏗 Architecture

```
PDF Upload
    │
    ▼
Page-by-Page Text Extraction (pypdf)
    │
    ▼
Semantic Chunking (280 words, 55 overlap)
    │
    ▼
Embedding Generation (all-MiniLM-L6-v2)
    │
    ▼
In-memory Vector Store (numpy arrays)
    │
  Query
    │
    ▼
Semantic Search (cosine similarity, top-5)
    │
    ▼
Context + Citations → LLM (Groq / Gemini)
    │
    ▼
Answer with Page Citations + Relevance Scores
```

---

## 📁 Project Structure

```
nexus-ai/
├── app.py              # Main application
├── requirements.txt    # Dependencies
└── README.md           # This file
```

---

## 🔑 Key Technical Concepts Demonstrated

- **RAG Pipeline** — Full retrieval-augmented generation from scratch
- **Semantic Embeddings** — Sentence transformers for meaning-based search
- **Vector Similarity** — Cosine similarity for chunk retrieval
- **LLM Integration** — Multi-provider API abstraction
- **Context Window Management** — Conversation history with truncation
- **PDF Processing** — Page-level text extraction and chunking

---

## 🏷 Tech Stack

`Python` `Streamlit` `sentence-transformers` `scikit-learn` `pypdf` `Groq API` `Google Gemini API` `NumPy`
