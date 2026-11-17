# Week 2 Day 5: five breakfast ideas from LangChain

`breakfast.py` asks gpt-4o-mini, through LangChain's `ChatOpenAI`, for five healthy breakfast ideas and prints only the text of the reply. The key comes from the `OPENAI_API_KEY` environment variable.

The prompt says what "healthy" means instead of leaving it to the model: at least 10 g protein per serving, whole grains or millets instead of refined flour, no deep frying, for a South Indian home kitchen. It also pins the format: a numbered list, one line each, the dish then its main protein in brackets, no introduction and no closing line.

```
pip install langchain langchain-openai
export OPENAI_API_KEY="..."
python breakfast.py          # the five ideas
python breakfast.py --raw    # the whole message object, once
```

## What invoke() returns

`llm.invoke(prompt)` returns an `AIMessage`, not a string. The `--raw` run prints all of it: the list sits in `content`, next to `response_metadata` (model `gpt-4o-mini-2024-07-18`, finish reason `stop`, 81 input and 82 output tokens) and `usage_metadata`. Printing `reply.content` gives only the list. The full object is in `output/raw-output.txt`.

## Two runs (18 Nov 2026)

| Run 1 | Run 2 |
|---|---|
| Oats Upma (Moong Dal) | Ragi dosa with sprouted green gram (green gram) |
| Quinoa Idli (Greek Yogurt) | Quinoa upma with peanuts and mixed vegetables (peanuts) |
| Millet Pongal (Split Peas) | Oats idli with curd and chopped nuts (yogurt) |
| Rava Dosa with Millet Flour (Chickpeas) | Millet pongal with moong dal and cashews (moong dal) |
| Poha with Sprouted Moong (Peanuts) | Whole grain vegetable paratha with paneer filling (paneer) |

The two runs did not match. Millet pongal is the only dish in both. Oats and quinoa come back in both, as different dishes. The format held exactly both times.

The definition of healthy held less well. Run 1 includes rava dosa, and rava is refined semolina, which the prompt ruled out. Neither run can show the 10 g protein rule was met, since the reply names a protein but gives no amount.

## Getting the same five every time

The default temperature lets the model pick different dishes on each run. Setting `temperature=0` makes the choice close to deterministic, though OpenAI does not guarantee identical output. A fixed list belongs in code or data, not in a model call. For the healthy rules, asking for the protein grams on each line would make the 10 g rule checkable.

## Files

| File | What it is |
|---|---|
| `breakfast.py` | The script |
| `output/terminal-runs.png` | The end of the `--raw` run and both normal runs in the terminal |
| `output/run1.txt`, `output/run2.txt` | The two lists as printed |
| `output/raw-output.txt` | The full `AIMessage` |
