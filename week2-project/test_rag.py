"""Offline tests: fake embeddings and a fake chat model, so no API key or credits are needed."""

from langchain_community.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models.fake_chat_models import FakeListChatModel

import rag
from prompts import ANSWER_SYSTEM

PAGES = rag.as_documents(
    [
        ("policy.pdf", 2, "Refunds on prepaid plans take 7 working days."),
        ("handbook.pdf", 2, "Refunds on prepaid plans take 14 working days."),
        ("faq.pdf", 1, "The clinic is closed on Sundays."),
    ]
)


def make_index():
    named = [(d.metadata["source"], [d]) for d in PAGES]
    return rag.build_index(named, DeterministicFakeEmbedding(size=32))


def test_index_counts_every_file():
    index = make_index()
    assert index.total_chunks == 3
    assert set(index.per_file) == {"policy.pdf", "handbook.pdf", "faq.pdf"}


def test_empty_input_gives_no_index():
    assert rag.build_index([("blank.pdf", rag.as_documents([("blank.pdf", 1, "   ")]))], DeterministicFakeEmbedding(size=8)) is None


def test_exact_text_is_top_hit():
    hits = rag.retrieve(make_index(), "The clinic is closed on Sundays.", k=2)
    assert hits[0][0].metadata["source"] == "faq.pdf"


def test_context_is_numbered_with_file_and_page():
    ctx = rag.format_context(PAGES[:2])
    assert ctx.startswith("[1] policy.pdf, page 2")
    assert "[2] handbook.pdf, page 2" in ctx


def test_first_question_is_not_rewritten():
    llm = FakeListChatModel(responses=["should not be used"])
    assert rag.standalone_question(llm, "How long is a refund?", []) == "How long is a refund?"


def test_follow_up_is_rewritten():
    llm = FakeListChatModel(responses=["How long does a refund take for children?"])
    turns = [{"role": "user", "content": "How long does a refund take?"}, {"role": "assistant", "content": "7 days [1]."}]
    assert rag.standalone_question(llm, "and for children?", turns) == "How long does a refund take for children?"


def test_answer_streams():
    llm = FakeListChatModel(responses=["Closed on Sundays [1]."])
    assert "".join(rag.answer_stream(llm, "Open Sunday?", PAGES[2:])) == "Closed on Sundays [1]."


def test_prompt_has_all_rtcfr_sections():
    for heading in ["# Role", "# Task", "# Context", "# Few-shot examples", "# Response format"]:
        assert heading in ANSWER_SYSTEM


def test_similarity_is_cosine():
    hits = rag.retrieve(make_index(), "The clinic is closed on Sundays.", k=3, min_similarity=-1)
    scores = [s for _, s in hits]
    assert scores[0] == 1.0
    assert all(-1 <= s <= 1 for s in scores) and scores == sorted(scores, reverse=True)


def test_weak_matches_are_dropped():
    hits = rag.retrieve(make_index(), "The clinic is closed on Sundays.", k=3, min_similarity=0.99)
    assert [d.metadata["source"] for d, _ in hits] == ["faq.pdf"]
