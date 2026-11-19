"""Retrieval and answering for the document Q&A app. No Streamlit here, so it can be tested on its own."""

from dataclasses import dataclass, field
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from prompts import ANSWER_PROMPT, REWRITE_PROMPT

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
MIN_SIMILARITY = 0.2  # excerpts below this are not relevant enough to show or send


@dataclass
class Index:
    store: FAISS
    per_file: dict = field(default_factory=dict)  # file name -> (pages, chunks)

    @property
    def total_chunks(self):
        return sum(chunks for _, chunks in self.per_file.values())


def load_pdf(path, display_name=None):
    """Load a PDF into page documents labelled with the file name and a 1-based page number."""
    pages = PyPDFLoader(str(path)).load()
    for page in pages:
        page.metadata["source"] = display_name or Path(path).name
        page.metadata["page_number"] = page.metadata.get("page", 0) + 1
    return pages


def split(pages):
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return [c for c in splitter.split_documents(pages) if c.page_content.strip()]


def build_index(named_pages, embeddings):
    """named_pages: list of (file name, page documents). Returns an Index, or None if no text."""
    chunks, per_file = [], {}
    for name, pages in named_pages:
        file_chunks = split(pages)
        chunks.extend(file_chunks)
        per_file[name] = (len(pages), len(file_chunks))
    if not chunks:
        return None
    return Index(FAISS.from_documents(chunks, embeddings, normalize_L2=True), per_file)


def label(doc):
    return f"{doc.metadata['source']}, page {doc.metadata['page_number']}"


def retrieve(index, question, k, min_similarity=MIN_SIMILARITY):
    """Top k chunks with their cosine similarity to the question (1 is identical).

    Vectors are L2-normalised, so FAISS returns the squared distance d2 and
    cosine similarity is 1 - d2 / 2.
    """
    hits = index.store.similarity_search_with_score(question, k=k)
    scored = [(doc, round(1 - float(d2) / 2, 2)) for doc, d2 in hits]
    return [(doc, s) for doc, s in scored if s >= min_similarity]


def format_context(docs):
    return "\n\n".join(f"[{i}] {label(d)}\n{d.page_content}" for i, d in enumerate(docs, start=1))


def format_history(turns, limit=6):
    """Last few chat turns as plain text for the rewrite step."""
    return "\n".join(f"{t['role']}: {t['content']}" for t in turns[-limit:])


def standalone_question(llm, question, turns):
    """Prompt chaining step 1: make a follow-up question searchable on its own."""
    if not turns:
        return question
    chain = REWRITE_PROMPT | llm | StrOutputParser()
    return chain.invoke({"history": format_history(turns), "question": question}).strip() or question


def answer_stream(llm, question, docs):
    """Prompt chaining step 2: stream the cited answer token by token."""
    chain = ANSWER_PROMPT | llm | StrOutputParser()
    return chain.stream({"context": format_context(docs), "question": question})


def as_documents(texts):
    """Helper for tests and demos: [(source, page, text)] -> Documents."""
    return [Document(page_content=t, metadata={"source": s, "page_number": p}) for s, p, t in texts]
