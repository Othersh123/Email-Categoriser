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

## 2026-10-17: Phase 1, eval set and first classifier

**What I tried:**
Wrote down category definitions in categories.md, then 30 fake emails with correct labels (13 deliberately tricky). Built a prompt that asks for JSON and a script that scores every email.

**What happened:**
- 22/30 correct (73%). Easy emails 76%, tricky 69%.
- Zero format failures. JSON mode made the output valid every time.
- The model over-calls Spam. 4 of the 8 misses were legit emails marked Spam, including a real card statement. Of the 9 emails it called Spam, only 5 were.
- It never picked Other (0/3). LinkedIn became Podcasts and blogs.
- An order confirmation became Promotions and an electricity bill became Statements. Both were "easy" for me, not for the model.

**What surprised me:**
My first Spam definition used "senders I never signed up with." The model can't know that. It only sees the email. I had to rewrite the rule around deception instead.

**What this means for building products:**
- Every rule in an AI spec has to be answerable from what the model actually sees.
- 100% on a label can be fake. Spam caught every real spam email because it called lots of things spam. You need to look at both directions.
- Mistakes don't cost the same. A statement in Spam is a missed bill. A promo in Other is nothing. Decide which error to avoid before chasing accuracy.
- 30 emails is a baseline, not a verdict. One email moves the score by 3 points.
