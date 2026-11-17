"""Ask the model for 5 healthy breakfast ideas and print only the text.

Run:       python breakfast.py
See the raw message object once:  python breakfast.py --raw
Needs OPENAI_API_KEY in the environment.
"""
import sys

from langchain_openai import ChatOpenAI

PROMPT = (
    "List exactly 5 healthy breakfast ideas for a South Indian home kitchen.\n"
    "Healthy here means: at least 10 g protein per serving, whole grains or millets "
    "instead of refined flour, and no deep frying.\n"
    "Format: a numbered list, 1 to 5, one line each, dish name then the main protein "
    "in brackets. No introduction and no closing line."
)

llm = ChatOpenAI(model="gpt-4o-mini")

reply = llm.invoke(PROMPT)

if "--raw" in sys.argv:
    print(repr(reply))
else:
    print(reply.content)
