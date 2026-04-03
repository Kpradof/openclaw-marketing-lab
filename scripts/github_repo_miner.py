import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "keywords.json"
OUTPUT_PATH = ROOT / "research" / "repos.json"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_search_query(keyword, min_stars, languages, updated_after):
    parts = [keyword, f"stars:>={min_stars}", f"pushed:>={updated_after}"]

    if languages:
        language_query = " ".join([f'language:"{lang}"' for lang in languages])
        parts.append(language_query)

    return " ".join(parts)


def github_request(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "openclaw-marketing-lab"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def search_repositories(keyword, min_stars, languages, updated_after, max_repos):
    query = build_search_query(keyword, min_stars, languages, updated_after)
    encoded_query = urllib.parse.quote(query)

    url = (
        f"https://api.github.com/search/repositories"
        f"?q={encoded_query}"
        f"&sort=stars"
        f"&order=desc"
        f"&per_page={max_repos}"
    )

    data = github_request(url)

    repos = []
    for item in data.get("items", []):
        repos.append({
            "keyword": keyword,
            "name": item.get("name"),
            "full_name": item.get("full_name"),
            "html_url": item.get("html_url"),
            "description": item.get("description"),
            "stargazers_count": item.get("stargazers_count"),
            "language": item.get("language"),
            "updated_at": item.get("updated_at"),
            "topics": item.get("topics", [])
        })

    return repos


def main():
    config = load_config()

    keywords = config.get("keywords", [])
    filters = config.get("filters", {})
    limits = config.get("limits", {})

    min_stars = filters.get("min_stars", 50)
    languages = filters.get("language", [])
    updated_after = filters.get("updated_after", "2023-01-01")
    max_repos = limits.get("max_repos_per_keyword", 5)

    all_results = []

    for keyword in keywords:
        print(f"Searching GitHub for: {keyword}")
        try:
            repos = search_repositories(
                keyword=keyword,
                min_stars=min_stars,
                languages=languages,
                updated_after=updated_after,
                max_repos=max_repos
            )
            all_results.extend(repos)
            time.sleep(1)
        except Exception as e:
            print(f"Error while searching '{keyword}': {e}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(all_results)} repos to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()