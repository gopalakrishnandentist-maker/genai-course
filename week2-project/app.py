"""Ask Your Documents, Week 2 project: a chat app that answers questions from your PDFs with citations.

Run it with:
    streamlit run app.py

Needs OPENAI_API_KEY in the environment or in a .env file next to this one.
"""

import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import rag

HERE = Path(__file__).parent
SAMPLES = HERE / "sample-pdfs"
MODELS = ["gpt-4o-mini", "gpt-4o"]

load_dotenv(HERE / ".env")
st.set_page_config(page_title="Ask Your Documents", page_icon="📄", layout="wide")


@st.cache_resource(show_spinner=False)
def embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")


def index_files(named_paths):
    """named_paths: list of (display name, path)."""
    named_pages = [(name, rag.load_pdf(path, name)) for name, path in named_paths]
    return rag.build_index(named_pages, embeddings())


def index_uploads(uploads):
    named_paths, tmp_paths = [], []
    for up in uploads:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(up.getvalue())
            named_paths.append((up.name, tmp.name))
            tmp_paths.append(tmp.name)
    try:
        return index_files(named_paths)
    finally:
        for p in tmp_paths:
            os.remove(p)


def set_index(index, fingerprint):
    st.session_state.index = index
    st.session_state.fingerprint = fingerprint
    st.session_state.messages = []


def show_sources(sources):
    if not sources:
        st.caption("No excerpt was close enough to the question to use.")
        return
    with st.expander(f"Sources ({len(sources)} excerpts)"):
        for i, (src, page, score, text) in enumerate(sources, start=1):
            st.markdown(f"**[{i}] {src}, page {page}** · similarity {score:.2f}")
            st.caption(text[:600] + ("..." if len(text) > 600 else ""))


st.session_state.setdefault("messages", [])
st.session_state.setdefault("index", None)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("1. Your documents")
    uploads = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    use_samples = st.button(
        "Or try the sample clinic PDFs", width="stretch", disabled=not SAMPLES.exists()
    )

    st.header("2. Settings")
    model = st.selectbox("Model", MODELS, help="gpt-4o-mini is faster and cheaper.")
    top_k = st.slider("Excerpts per answer", 2, 8, 4, help="How many chunks are retrieved.")
    if st.button("New conversation", width="stretch"):
        st.session_state.messages = []

if not os.environ.get("OPENAI_API_KEY"):
    st.title("Ask Your Documents")
    st.error("OPENAI_API_KEY is not set. Add it to a .env file next to app.py, then restart.")
    st.stop()

try:
    if uploads:
        fp = tuple(sorted((u.name, u.size) for u in uploads))
        if st.session_state.get("fingerprint") != fp:
            with st.spinner("Reading, splitting and embedding your PDFs..."):
                set_index(index_uploads(uploads), fp)
    elif use_samples:
        with st.spinner("Loading the sample PDFs..."):
            paths = sorted(SAMPLES.glob("*.pdf"))
            set_index(index_files([(p.name, p) for p in paths]), "samples")
except Exception as exc:  # network, bad key, unreadable PDF
    st.error(f"Could not index the documents: {exc}")
    st.stop()

index = st.session_state.index

# ---------- Main ----------
st.title("Ask Your Documents")
st.caption("Answers come only from your PDFs, with every claim cited to a file and page.")

if index is None:
    if uploads:
        st.warning("No text could be read from these PDFs. Scanned pages need OCR first.")
    else:
        st.info("Upload one or more PDFs in the sidebar, or load the sample PDFs to try it.")
    st.stop()

with st.sidebar:
    st.success(f"{index.total_chunks} chunks from {len(index.per_file)} files")
    for name, (pages, chunks) in index.per_file.items():
        st.caption(f"{name}: {pages} pages, {chunks} chunks")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("searched_for"):
            st.caption(f"Searched for: {msg['searched_for']}")
        if msg.get("sources"):
            show_sources(msg["sources"])

question = st.chat_input("Ask a question about your documents")

if not st.session_state.messages and not question:
    st.markdown("**Try asking:** How long does a refund take? · Can I see a dentist on a Sunday?")
if question:
    history = st.session_state.messages[:]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            llm = ChatOpenAI(model=model, temperature=0)
            search_q = rag.standalone_question(llm, question, history)
            hits = rag.retrieve(index, search_q, top_k)
            docs = [d for d, _ in hits]
            reply = st.write_stream(rag.answer_stream(llm, question if not history else search_q, docs))
        except Exception as exc:
            st.error(f"The model call failed: {exc}")
            st.session_state.messages.pop()
            st.stop()
        searched_for = search_q if search_q != question else None
        if searched_for:
            st.caption(f"Searched for: {searched_for}")
        sources = [
            (d.metadata["source"], d.metadata["page_number"], s, d.page_content) for d, s in hits
        ]
        show_sources(sources)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "sources": sources, "searched_for": searched_for}
    )
