import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "research" / "repos.json"
OUTPUT_PATH = ROOT / "research" / "repo_candidates.json"


def classify_repo(repo):
    text = (
        (repo.get("name") or "") + " " +
        (repo.get("description") or "") + " " +
        " ".join(repo.get("topics", []))
    ).lower()

    asset_types = []

    if any(w in text for w in ["prompt", "prompts"]):
        asset_types.append("prompts")

    if any(w in text for w in ["workflow", "automation", "pipeline"]):
        asset_types.append("workflows")

    if any(w in text for w in ["agent", "agents"]):
        asset_types.append("agents")

    if any(w in text for w in ["plugin", "integration"]):
        asset_types.append("plugins")

    if not asset_types:
        asset_types.append("unknown")

    score = 0

    stars = repo.get("stargazers_count", 0) or 0
    if stars >= 500:
        score += 3
    elif stars >= 100:
        score += 2
    elif stars >= 50:
        score += 1

    if repo.get("description"):
        score += 1

    if repo.get("topics"):
        score += 1

    if "unknown" not in asset_types:
        score += 2

    return {
        "full_name": repo.get("full_name"),
        "html_url": repo.get("html_url"),
        "description": repo.get("description"),
        "stargazers_count": stars,
        "asset_types": asset_types,
        "score": score
    }


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        repos = json.load(f)

    analyzed = [classify_repo(repo) for repo in repos]
    analyzed.sort(key=lambda x: x["score"], reverse=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(analyzed, f, indent=2)

    print(f"Saved {len(analyzed)} repos to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()