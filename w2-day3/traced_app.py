from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

prompts = [
    "In one sentence, what is LangChain?",
    "Classify this support message as billing, technical or other. Answer with one word. "
    "Message: 'My invoice shows the wrong GST number.'",
    "Write a 250-word explainer for a hospital administrator on why an AI app should log "
    "every prompt and response it sends. Give three concrete problems the log helps catch.",
]

for number, prompt in enumerate(prompts, start=1):
    print(f"--- Prompt {number} ---")
    print(prompt)
    print()
    print(llm.invoke(prompt).content)
    print()
