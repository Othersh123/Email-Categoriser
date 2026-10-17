r"""
Phase 1, Step 3: classify one email with a local model.

classify_email() sends the prompt plus one email to the model and turns the
reply into a Python dict. Small models don't always follow the format, so
the reply is checked before we trust it.

Run from the project folder to try it on a few emails from the eval set:
    .venv\Scripts\python.exe src\classify.py
"""

import csv
import json
import time
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent  # the project folder
MODEL = "llama3.2-3b-2k"
PROMPT_VERSION = "v1"
LABELS = ["Spam", "Statements", "Important", "Podcasts and blogs", "Promotions", "Other"]

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def load_prompt(version):
    """Read a prompt from prompts/<version>.txt, so prompts are versioned files, not code."""
    return (ROOT / "prompts" / f"{version}.txt").read_text(encoding="utf-8")


def classify_email(sender, subject, body, prompt):
    """Ask the model for a label. Returns a dict with label, reason, raw reply and an error if any."""
    email_text = f"From: {sender}\nSubject: {subject}\n\n{body}"

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        # JSON mode: Ollama constrains the model so it can only produce valid JSON.
        # It guarantees the syntax, not that the right keys or label come back.
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},  # the instructions
            {"role": "user", "content": email_text},  # the email to sort
        ],
    )
    raw = response.choices[0].message.content

    # Check the reply in stages. Each failure gets its own error so we can count them later.
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"label": None, "reason": None, "raw": raw, "error": "not valid JSON"}

    label = data.get("label")
    if label not in LABELS:
        return {"label": label, "reason": data.get("reason"), "raw": raw,
                "error": f"unknown label: {label!r}"}

    return {"label": label, "reason": data.get("reason"), "raw": raw, "error": None}


if __name__ == "__main__":
    prompt = load_prompt(PROMPT_VERSION)
    with open(ROOT / "data" / "eval_set.csv", encoding="utf-8", newline="") as f:
        emails = {row["id"]: row for row in csv.DictReader(f)}

    # One easy email and two tricky ones.
    for email_id in ["1", "9", "26"]:
        e = emails[email_id]
        start = time.time()
        result = classify_email(e["sender"], e["subject"], e["body"], prompt)
        seconds = time.time() - start

        print(f"#{email_id}  {e['subject']}")
        print(f"  expected: {e['label']}")
        print(f"  model:    {result['label']}  ({seconds:.1f}s)")
        print(f"  reason:   {result['reason']}")
        if result["error"]:
            print(f"  ERROR:    {result['error']}  raw reply: {result['raw']}")
        print()
