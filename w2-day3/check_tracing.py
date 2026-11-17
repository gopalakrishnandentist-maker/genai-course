"""Run before traced_app.py to confirm tracing is on and the LangSmith key works.

Kept out of traced_app.py on purpose: the app itself has no tracing code.
"""
import os

from langsmith import Client, utils

print("Tracing enabled:", utils.tracing_is_enabled())
print("Project:", os.environ.get("LANGSMITH_PROJECT", "default (not set)"))
print("OpenAI key set:", bool(os.environ.get("OPENAI_API_KEY")))
print("LangSmith key set:", bool(os.environ.get("LANGSMITH_API_KEY")))

try:
    next(iter(Client().list_projects(limit=1)), None)
    print("LangSmith key accepted: yes")
except Exception as error:
    print("LangSmith key accepted: no,", type(error).__name__)
