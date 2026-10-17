# Learnings: Running Small LLMs Locally

I'm a Product Manager learning how LLMs actually work by building an email categorizer on a small local model. This is my running log of what I tried, what broke, and what it taught me about building AI products.

**Setup:** GTX 1050 Ti (4GB VRAM), 8GB RAM, Ollama, small 1B to 4B models.

---

<!-- New entries go below, newest at the bottom -->

## 2026-10-17: Phase 0, getting a model running on my GPU

**What I tried:**
Updated my NVIDIA driver, installed Ollama on D: (C: only had 13 GB free), downloaded llama3.2:3b, and called it from Python using the openai library pointed at localhost.

**What happened:**
- My driver was from 2019 (419). Ollama needs 531+. Without updating, it would have silently run on the CPU.
- Ollama ignored the model folder I set as an environment variable. The desktop app has its own setting that overrides it. Found it by reading the server log.
- llama3.2:3b is a 2.0 GB download but needed 2.9 GB of GPU memory, because the context window reserves memory up front. My usable budget was 2.8 GB, so 18% ran on the CPU.
- Cutting the context from 4096 to 2048 tokens: 2.3 GB, 100% GPU, 23.1 to 27.9 tokens/sec. Same answer word for word.
- The OpenAI-compatible endpoint drops the context setting with no error. Had to bake it into a model variant with a Modelfile.
- Loading takes 70 to 80 seconds because D: is a spinning hard drive.
- Statelessness test: told it my name, asked in a new call, it had no idea. Resent the history and it knew. That call cost 63 tokens instead of 30.

**What this means for building products:**
- "Runs on device" depends on driver, runtime, disk, RAM and VRAM. A failure in any of them shows up as "it's slow," not as an error. That's a support ticket.
- Context window is a memory cost paid up front, not a free feature. Pick it based on the longest input you actually need.
- Chat memory is the app resending the transcript. Every turn costs more than the last.
