r"""
Phase 1, Step 4: score the classifier against the whole eval set.

Runs every email in data/eval_set.csv through classify_email(), compares the
model's label with the correct one, and prints:
  - overall accuracy, plus easy vs tricky
  - accuracy per label (of the emails that ARE Spam, how many did it call Spam?)
  - every miss, with the model's reason
  - how many replies failed the format checks

It also saves one row per email to results/, so any run can be looked at later.

Run from the project folder:
    .venv\Scripts\python.exe src\evaluate.py
"""

import csv
import time
from collections import Counter
from datetime import datetime

from classify import LABELS, MODEL, PROMPT_VERSION, ROOT, classify_email, load_prompt


def pct(part, whole):
    return f"{part}/{whole} ({100 * part / whole:.0f}%)" if whole else "n/a"


def main():
    prompt = load_prompt(PROMPT_VERSION)
    with open(ROOT / "data" / "eval_set.csv", encoding="utf-8", newline="") as f:
        emails = list(csv.DictReader(f))

    print(f"Model: {MODEL} | Prompt: {PROMPT_VERSION} | Emails: {len(emails)}\n")

    results = []
    start = time.time()
    for e in emails:
        r = classify_email(e["sender"], e["subject"], e["body"], prompt)
        correct = r["label"] == e["label"]
        results.append({**e, "predicted": r["label"], "correct": correct,
                        "model_reason": r["reason"], "error": r["error"], "raw": r["raw"]})
        print("." if correct else "x", end="", flush=True)  # progress: . right, x wrong
    total_time = time.time() - start
    print(f"  done in {total_time:.0f}s\n")

    # Overall, and split by difficulty
    right = sum(r["correct"] for r in results)
    print(f"Accuracy:  {pct(right, len(results))}")
    for level in ["easy", "tricky"]:
        group = [r for r in results if r["difficulty"] == level]
        print(f"  {level:7}  {pct(sum(r['correct'] for r in group), len(group))}")

    # Per label: of the emails whose correct label is X, how many got X?
    print("\nPer label (correct label -> how many the model got right):")
    for label in LABELS:
        group = [r for r in results if r["label"] == label]
        print(f"  {label:20} {pct(sum(r['correct'] for r in group), len(group))}")

    # Format failures, counted by type
    errors = Counter(r["error"] for r in results if r["error"])
    print(f"\nFormat failures: {sum(errors.values())}")
    for err, n in errors.items():
        print(f"  {n} x {err}")

    # Every miss, so we can see what kind of mistakes it makes
    misses = [r for r in results if not r["correct"]]
    print(f"\nMisses ({len(misses)}):")
    for r in misses:
        print(f"  #{r['id']:>2} [{r['difficulty']}] {r['subject']}")
        print(f"       expected {r['label']}, got {r['predicted']}. Model said: {r['model_reason']}")

    # Save every row so this run can be inspected later
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out_file = out_dir / f"{stamp}_{MODEL}_{PROMPT_VERSION}.csv"
    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved: {out_file.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
