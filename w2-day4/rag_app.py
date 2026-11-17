"""Multi-PDF RAG app with sources.

Run with:  streamlit run rag_app.py
Needs OPENAI_API_KEY in the environment.
"""
import os
import tempfile

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4

PROMPT = ChatPromptTemplate.from_template(
    """Answer the question using only the excerpts below. Each excerpt is labelled
with its file and page.

Rules:
- If the excerpts answer the question indirectly (for example, a service is not
  offered but an alternative is), give that answer and say what the excerpts state.
- Only if no excerpt bears on the question, say "Not found in the uploaded documents."
- If two documents say different things, do not pick one. Say they disagree and
  state what each one says, naming the file and page.
- Keep the answer short.

Excerpts:
{context}

Question: {question}
"""
)


def make_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")


def make_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


def load_pdf(uploaded_file):
    """Load one uploaded PDF into page documents, labelled with its real file name."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(uploaded_file.getvalue())
        path = tmp.name
    try:
        pages = PyPDFLoader(path).load()
    finally:
        os.remove(path)
    for page in pages:
        page.metadata["source"] = uploaded_file.name
        page.metadata["page_number"] = page.metadata.get("page", 0) + 1
    return pages


def build_store(files):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks, per_file = [], {}
    for uploaded_file in files:
        pages = load_pdf(uploaded_file)
        file_chunks = splitter.split_documents(pages)
        chunks.extend(file_chunks)
        per_file[uploaded_file.name] = (len(pages), len(file_chunks))
    if not chunks:
        return None, per_file, 0
    return FAISS.from_documents(chunks, make_embeddings()), per_file, len(chunks)


def label(doc):
    return f"{doc.metadata['source']} - page {doc.metadata['page_number']}"


def answer(question, store):
    docs = store.as_retriever(search_kwargs={"k": TOP_K}).invoke(question)
    context = "\n\n".join(f"[{label(d)}]\n{d.page_content}" for d in docs)
    reply = (PROMPT | make_llm()).invoke({"context": context, "question": question})
    return reply.content, docs


def unique_sources(docs):
    seen = []
    for doc in docs:
        if label(doc) not in seen:
            seen.append(label(doc))
    return seen


st.title("Ask across your PDFs")

if not os.environ.get("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY is not set. Export it in the terminal, then restart the app.")
    st.stop()

files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if files:
    fingerprint = tuple(sorted((f.name, f.size) for f in files))
    if st.session_state.get("fingerprint") != fingerprint:
        with st.spinner("Reading, chunking and embedding..."):
            store, per_file, total = build_store(files)
        st.session_state.store = store
        st.session_state.per_file = per_file
        st.session_state.total = total
        st.session_state.fingerprint = fingerprint

    if st.session_state.store is None:
        st.warning("No text could be read from these PDFs. Scanned pages need OCR first.")
        st.stop()

    st.success(
        f"Indexed {st.session_state.total} chunks from {len(st.session_state.per_file)} files."
    )
    with st.expander("Per file"):
        for name, (pages, count) in st.session_state.per_file.items():
            st.write(f"{name}: {pages} pages, {count} chunks")

    question = st.text_input("Ask a question")
    if question:
        with st.spinner("Searching..."):
            text, docs = answer(question, st.session_state.store)
        st.write(text)
        st.caption("Sources: " + " | ".join(unique_sources(docs)))
else:
    st.info("Upload one or more PDFs to begin.")
