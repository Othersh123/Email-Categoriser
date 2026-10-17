r"""
Phase 0, Step 4: call a local model from Python.

Shows two things:
1. Ollama speaks the same API format as OpenAI, so the standard `openai`
   library works if we point it at localhost instead of OpenAI's servers.
2. The model is stateless. It remembers nothing between calls. Any
   "memory" is just us resending the earlier conversation each time.

Run from the project folder:
    .venv\Scripts\python.exe src\hello_ollama.py
"""

from openai import OpenAI

# Point the OpenAI client at Ollama on this laptop. Nothing leaves the machine.
# Ollama ignores the API key, but the library requires one, so any text works.
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Our variant with a 2048-token context, so it fits 100% on the 4 GB GPU.
# See modelfiles/llama3.2-3b-2k.Modelfile.
MODEL = "llama3.2-3b-2k"


def ask(messages):
    """Send a list of messages, print the reply and token counts, return the reply."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,  # always pick the most likely next token, so runs repeat
    )
    reply = response.choices[0].message.content
    usage = response.usage  # how many tokens went in and came out
    print(f"  Model: {reply}")
    print(f"  (tokens in: {usage.prompt_tokens}, tokens out: {usage.completion_tokens})\n")
    return reply


# Call 1: tell the model a fact.
first = [{"role": "user", "content": "My name is Priya. Reply in one short sentence."}]
print("Call 1: telling the model my name")
first_reply = ask(first)

# Call 2: a brand new request with no history. The model has never "met" us.
print("Call 2: new request, no history sent")
ask([{"role": "user", "content": "What is my name?"}])

# Call 3: resend the whole conversation so far, plus the new question.
# This is all "chat memory" is: the app replays the transcript every time.
print("Call 3: same question, but we resend the earlier messages")
ask(first + [
    {"role": "assistant", "content": first_reply},
    {"role": "user", "content": "What is my name?"},
])
