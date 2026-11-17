# Week 2 Day 4: a multi-PDF RAG app with sources

`rag_app.py` is a Streamlit app. Upload several PDFs, and it splits them into chunks, embeds them with OpenAI `text-embedding-3-small` and stores them in one FAISS index held in `st.session_state`. Each question retrieves the 4 closest chunks across all files, and gpt-4o-mini (temperature 0) answers from those chunks only. Every chunk carries its real file name and page number, so the answer cites them and a Sources line lists every chunk retrieved.

```
pip install streamlit langchain langchain-openai langchain-community langchain-text-splitters pypdf faiss-cpu
export OPENAI_API_KEY="..."
streamlit run rag_app.py
```

## Test documents

`sample-pdfs/` holds three short PDFs for a fictional dental clinic, written for this test: a patient policy (3 pages), a front desk handbook (3 pages) and a patient FAQ (4 pages). One fact is planted to disagree: the policy and the FAQ say a refund takes 7 working days, and the handbook says 14.

Indexed: 10 chunks from 3 files (3, 3 and 4). Each section sits on its own page, so with a chunk size of 1,000 characters each page is one chunk.

## What the runs showed (18 Nov 2026)

| Question | Answer | Correct? |
|---|---|---|
| How long does a refund on a prepaid treatment plan take? | The documents disagree: patient-faq.pdf page 4 says 7 working days, staff-handbook.pdf page 2 says 14 | Yes, both pages right. It did not mention that clinic-policy.pdf page 2 also says 7, though that chunk was retrieved |
| Can I see a dentist on a Sunday? (first run) | "Not found in the uploaded documents." | No. patient-faq.pdf page 1 and staff-handbook.pdf page 3 were both retrieved and say the clinic is closed on Sundays, with an on-call number from 10 am to 1 pm |
| Same question, after the prompt fix | Closed on Sundays and national holidays (patient-faq.pdf page 1); for emergencies call the on-call number 10 am to 1 pm (staff-handbook.pdf page 3) | Yes |

The first Sunday answer failed on the prompt, not on retrieval. The rule "if the excerpts do not contain the answer, say Not found" made the model refuse a question the documents answer only indirectly. The rule now says to give an indirect answer and state what the excerpts say, and to reply "Not found" only when no excerpt bears on the question. The refund question was asked again after the change and still reported the disagreement.

## On the brief's two questions

**Disagreement.** The prompt tells the model not to pick a side when two documents differ, and to state what each one says with its file and page. The refund question shows that working.

**Five pages for one answer.** The Sources line lists all 4 retrieved chunks, while the answer itself cites only the 2 it used. Most of the time a long Sources line reflects the retrieval setting (top 4), not the chunk size. Here, with one section per page, each chunk is one topic, which is what the chunk size should give.

## Screenshots

| File | What it shows |
|---|---|
| `output/indexed-three-pdfs.png` | Three PDFs uploaded, 10 chunks, per-file counts |
| `output/answer-refund-disagreement.png` | The refund answer with both sources and the Sources line |
| `output/answer-not-found-before-fix.png` | The Sunday question failing before the prompt change |
| `output/answer-sunday-after-fix.png` | The Sunday question answered with pages |
| `output/rag-walkthrough.gif` | The four screens in order |
