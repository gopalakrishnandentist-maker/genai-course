# Week 2 Day 3: tracing a LangChain app with LangSmith

`traced_app.py` sends three prompts to gpt-4o-mini through LangChain's `ChatOpenAI` and prints each answer. The file has no tracing code. Tracing is switched on by environment variables only:

```
export OPENAI_API_KEY="..."
export LANGSMITH_API_KEY="..."
export LANGSMITH_TRACING="true"
export LANGSMITH_PROJECT="social-eagle-w2d3"
```

Because tracing needs no code, it can be off without any error. `check_tracing.py` runs first and prints whether tracing is enabled, which project the runs will land in, and whether LangSmith accepts the key, so I am not searching the dashboard for runs that were never sent.

## The runs (18 Nov 2026, project social-eagle-w2d3)

| Prompt | Input tokens | Output tokens | Total | Latency | Cost (USD) |
|---|---|---|---|---|---|
| 1. In one sentence, what is LangChain? | 16 | 31 | 47 | 1.61 s | 0.000021 |
| 2. Classify a support message, one word | 35 | 1 | 36 | 1.01 s | 0.000006 |
| **3. 250-word explainer on logging prompts** | 41 | 260 | **301** | **3.94 s** | **0.000162** |

Prompt 3 is the expensive one: 301 of the 384 tokens in the three runs (78%), 86% of the cost, and 3.9 times the latency of prompt 2. It is expensive for a good reason. It asked for a 250-word answer, and output tokens cost more and take longer than input tokens. It came back at 217 words. The input side of all three prompts is almost the same size (16 to 41 tokens), so the length of the answer drives the cost.

Prompt 2 shows the other end: one output token ("Billing") in about a second.

The project also holds one failed run from an earlier attempt, when the OpenAI account had no API credit (error 429). LangSmith recorded that call as well: the prompt sent, the error and 4.2 s spent waiting. A failure is traced the same way as a success, which is the point of tracing.

## Screenshots

| File | What it shows |
|---|---|
| `output/terminal-run.png` | The pre-flight check and the three answers in the terminal |
| `output/langsmith-project-overview.png` | The project: 3 succeeded, 1 failed, gpt-4o-mini |
| `output/langsmith-project-runs.png` | The runs with latency, tokens and cost |
| `output/langsmith-run-opened.png` | Prompt 3 opened: the exact prompt sent, the response, 3.94 s, 301 tokens |
| `output/langsmith-run-token-breakdown.png` | Prompt 3 token split: 41 input, 260 output |
| `output/langsmith-walkthrough.gif` | All of the above in order |

## Run it

```
python -m venv venv && source venv/bin/activate
pip install langchain langchain-openai langsmith
# set the four variables above
python check_tracing.py
python traced_app.py
```
