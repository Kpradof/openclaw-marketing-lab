import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOP_CANDIDATES_PATH = os.path.join(BASE_DIR, "research", "top_candidates.json")
OUTPUT_ANALYSIS_DIR = os.path.join(BASE_DIR, "research", "openclaw_outputs")
SKILLS_DIR = os.path.join(BASE_DIR, "skills")
WORKFLOWS_DIR = os.path.join(BASE_DIR, "workflows")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts", "generated")
MANIFEST_PATH = os.path.join(BASE_DIR, "generated", "manifest.json")


def load_top_candidates():
    with open(TOP_CANDIDATES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("candidates") or data.get("repos") or []

    return []


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def sanitize_name(name):
    return (
        str(name).lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
    )


def get_topics(repo):
    return repo.get("topics") or repo.get("keywords") or []


def get_repo_name(repo):
    if repo.get("name"):
        return repo["name"]

    if repo.get("full_name"):
        return repo["full_name"].split("/")[-1]

    return "repo"


# -----------------------------
# Analysis
# -----------------------------

def generate_analysis(repo):
    return {
        "repo_name": get_repo_name(repo),
        "full_name": repo.get("full_name"),
        "url": repo.get("html_url"),
        "description": repo.get("description", ""),
        "topics": get_topics(repo),
        "language": repo.get("language"),
        "stars": repo.get("stargazers_count", 0),
        "score": repo.get("score", 0),
        "patterns": [
            "pattern_extraction_pending",
            "workflow_identification_pending"
        ],
        "generated_from": "generate_assets.py MVP"
    }


# -----------------------------
# Asset decision logic
# -----------------------------

def decide_asset_type(repo):
    text_blob = (
        f"{get_repo_name(repo)} {repo.get('description', '')}"
    ).lower()

    if any(k in text_blob for k in ["workflow", "pipeline", "automation"]):
        return "workflow"

    if any(k in text_blob for k in ["prompt", "llm"]):
        return "prompt"

    return "skill"


# -----------------------------
# Generators
# -----------------------------

def generate_skill(repo):
    return {
        "name": f"{get_repo_name(repo)}_skill",
        "description": repo.get("description", ""),
        "topics": get_topics(repo),
        "actions": [
            "extract_patterns",
            "apply_logic"
        ]
    }


def generate_workflow(repo):
    return {
        "name": f"{get_repo_name(repo)}_workflow",
        "steps": [
            "input_data",
            "process_data",
            "generate_output"
        ],
        "source_repo": repo.get("html_url")
    }


def generate_prompt(repo):
    return {
        "name": f"{get_repo_name(repo)}_prompt",
        "description": repo.get("description", ""),
        "topics": get_topics(repo),
        "template": "Analyze this repository and extract reusable marketing automation patterns."
    }


# -----------------------------
# Main
# -----------------------------

def main():
    os.makedirs(OUTPUT_ANALYSIS_DIR, exist_ok=True)
    os.makedirs(SKILLS_DIR, exist_ok=True)
    os.makedirs(WORKFLOWS_DIR, exist_ok=True)
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)

    candidates = load_top_candidates()

    if not candidates:
        print("No candidates found in top_candidates.json")
        return

    manifest_assets = []

    print(f"Processing {len(candidates)} repositories...\n")

    for repo in candidates:
        repo_name = get_repo_name(repo)
        repo_name_safe = sanitize_name(repo_name)

        analysis = generate_analysis(repo)
        analysis_path = os.path.join(
            OUTPUT_ANALYSIS_DIR,
            f"{repo_name_safe}_analysis.json"
        )
        save_json(analysis, analysis_path)
        print(f"Saved analysis -> {analysis_path}")

        asset_type = decide_asset_type(repo)

        if asset_type == "workflow":
            workflow = generate_workflow(repo)
            path = os.path.join(WORKFLOWS_DIR, f"{repo_name_safe}_workflow.json")
            save_json(workflow, path)
            print(f"Saved workflow -> {path}")

        elif asset_type == "prompt":
            prompt = generate_prompt(repo)
            path = os.path.join(PROMPTS_DIR, f"{repo_name_safe}_prompt.json")
            save_json(prompt, path)
            print(f"Saved prompt -> {path}")

        else:
            skill = generate_skill(repo)
            path = os.path.join(SKILLS_DIR, f"{repo_name_safe}_skill.json")
            save_json(skill, path)
            print(f"Saved skill -> {path}")

            manifest_assets.append({
                "repo_name": repo_name,
                "asset_type": asset_type,
                "analysis_path": os.path.relpath(analysis_path, BASE_DIR),
                "asset_path": os.path.relpath(path, BASE_DIR)
            })

        print("-----")

    manifest = {
        "total_repositories": len(candidates),
        "assets": manifest_assets
    }

    save_json(manifest, MANIFEST_PATH)
    print(f"Saved manifest -> {MANIFEST_PATH}")
    print("\nDone.")


if __name__ == "__main__":
    main()