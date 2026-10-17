# Email Categoriser

A Gmail categoriser that runs on a small open-source LLM on my own laptop. No cloud AI, no email content leaving the machine. It suggests labels, never deletes anything, and is meant to get better when I correct it.

## Why I'm building this

I'm a Product Manager. I want to understand how LLMs actually behave (what they cost, where they break, what "running locally" really takes) so I can make better calls on AI features. The tool is the vehicle. What I learn along the way goes in [learnings.md](learnings.md).

## How it works

- **[Ollama](https://ollama.com)** runs the model locally and serves it on `localhost`.
- **Python** calls it with the standard `openai` library, pointed at Ollama instead of OpenAI.
- **Model:** `llama3.2:3b`, 4-bit quantized, with a 2048-token context so it fits fully on a 4 GB GPU.
- **Hardware:** a 2018 laptop with a GTX 1050 Ti (4 GB VRAM) and 8 GB RAM. The constraint is the point.

## Categories

Spam, Important, Credit card rewards, Brand offers, Podcast links, Blog posts.

## Roadmap

| Phase | What | Status |
|---|---|---|
| 0 | Run a model on the local GPU and call it from Python | ✅ Done |
| 1 | Synthetic eval set and a first classifier | Next |
| 2 | Run experiments: prompts, examples, models | |
| 3 | Read real Gmail (read-only) | |
| 4 | Store my corrections and apply labels | |
| 5 | RAG: use past corrections as examples | |
| 6 | Tool calling | |
| 7 | Expose it as an MCP server | |

## Privacy

- The eval set is hand-written fake emails.
- Real email data stays on my machine and is never committed.
- Gmail access is read-only until labelling is turned on. Nothing is ever deleted.

## Try it

Needs [Ollama](https://ollama.com/download) and Python 3.12.

```powershell
ollama pull llama3.2:3b
ollama create llama3.2-3b-2k -f modelfiles/llama3.2-3b-2k.Modelfile
python -m venv .venv
.venv\Scripts\python.exe -m pip install openai
.venv\Scripts\python.exe src\hello_ollama.py
```

Built with help from [Claude Code](https://claude.com/claude-code).
