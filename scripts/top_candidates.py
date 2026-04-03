import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "research" / "repo_candidates.json"
OUTPUT_PATH = ROOT / "research" / "top_candidates.json"


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        repos = json.load(f)

    seen = set()
    filtered = []

    for repo in repos:
        full_name = repo.get("full_name")
        score = repo.get("score", 0)

        if not full_name or full_name in seen:
            continue

        if score >= 4:
            filtered.append(repo)
            seen.add(full_name)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(filtered)} top candidates to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()