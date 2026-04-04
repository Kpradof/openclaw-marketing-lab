import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOP_CANDIDATES_PATH = os.path.join(BASE_DIR, "research", "top_candidates.json")
OUTPUT_ANALYSIS_DIR = os.path.join(BASE_DIR, "research", "openclaw_outputs")
SKILLS_DIR = os.path.join(BASE_DIR, "skills")
WORKFLOWS_DIR = os.path.join(BASE_DIR, "workflows")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts", "generated")
MANIFEST_PATH = os.path.join(BASE_DIR, "generated", "manifest.json")

STOPWORDS = {
    "a", "an", "and", "the", "of", "in", "on", "for", "to", "with", "is", "are",
    "this", "that", "be", "as", "by", "at", "from", "or", "it", "you", "your",
    "we", "us", "our", "but", "if", "not", "can", "will", "would"
}


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


def clean_triggers(topics, description):
    words = set()

    if topics:
        for t in topics:
            for w in re.split(r"\W+", t.lower()):
                if w and w not in STOPWORDS:
                    words.add(w)

    if description:
        for w in re.split(r"\W+", description.lower()):
            if w and w not in STOPWORDS:
                words.add(w)

    return list(words) if words else []


def normalize_io_items(items):
    normalized = []
    for item in items or []:
        if not isinstance(item, dict):
            continue

        normalized.append({
            "name": item.get("name", ""),
            "type": item.get("type", "string"),
            "description": item.get("description", "")
        })

    return normalized


def normalize_prompt_templates(templates):
    normalized = []
    for tpl in templates or []:
        if not isinstance(tpl, dict):
            continue

        normalized.append({
            "name": tpl.get("name", ""),
            "template": tpl.get("template", "")
        })

    return normalized


def normalize_string_list(items):
    if not isinstance(items, list):
        return []

    cleaned = []
    for item in items:
        if isinstance(item, str) and item.strip():
            cleaned.append(item.strip())

    return cleaned


def generate_skill(repo):
    repo_name = get_repo_name(repo)
    repo_name_safe = sanitize_name(repo_name)
    topics = get_topics(repo)
    description = repo.get("description", "")
    language = repo.get("language", "unknown")
    stars = repo.get("stargazers_count", 0)
    url = repo.get("html_url")

    triggers = clean_triggers(topics, description)
    if not triggers:
        triggers = [repo_name_safe]

    return {
        "name": repo_name_safe,
        "type": "repository_derived_skill",
        "description": description.strip(),
        "triggers": triggers,
        "inputs": [
            {
                "name": "repository_context",
                "type": "string",
                "description": "Repository context or summary to analyze"
            },
            {
                "name": "user_goal",
                "type": "string",
                "description": "User goal for extracting reusable patterns"
            }
        ],
        "outputs": [
            {
                "name": "reusable_patterns",
                "type": "array",
                "description": "Reusable patterns identified from the repository"
            },
            {
                "name": "suggested_actions",
                "type": "array",
                "description": "Suggested follow-up actions based on the analysis"
            }
        ],
        "steps": [
            "analyze_repository_metadata",
            "extract_reusable_patterns",
            "map_patterns_to_marketing_use_cases"
        ],
        "use_cases": [
            "marketing automation",
            "workflow design",
            "prompt generation"
        ],
        "patterns": [],
        "prompt_templates": [],
        "metadata": {
            "language": language,
            "stars": stars,
            "repo_url": url
        },
        "source": {
            "repo_name": repo_name,
            "repo_url": url
        }
    }


def generate_skill_from_capability(capability, repo_name=None):
    metadata = capability.get("metadata", {}) or {}
    repo_url = metadata.get("repo_url", "")
    base_name = sanitize_name(repo_name or capability.get("name", "repo"))

    description = capability.get("description", "")
    triggers = clean_triggers([], description)
    if repo_name:
        triggers = list(set(triggers + [sanitize_name(repo_name)]))
    if not triggers:
        triggers = [base_name]

    return {
        "name": base_name,
        "type": "repository_derived_skill",
        "description": description,
        "triggers": triggers,
        "inputs": normalize_io_items(capability.get("inputs", [])),
        "outputs": normalize_io_items(capability.get("outputs", [])),
        "steps": normalize_string_list(capability.get("steps", [])),
        "use_cases": normalize_string_list(capability.get("use_cases", [])),
        "patterns": normalize_string_list(capability.get("patterns", [])),
        "prompt_templates": normalize_prompt_templates(
            capability.get("prompt_templates", [])
        ),
        "metadata": {
            "language": metadata.get("language", "unknown"),
            "stars": metadata.get("stars", 0),
            "repo_url": repo_url
        },
        "source": {
            "repo_name": repo_name or capability.get("name", ""),
            "repo_url": repo_url
        }
    }


def generate_workflow(repo):
    repo_name = get_repo_name(repo)
    repo_name_safe = sanitize_name(repo_name)

    return {
        "name": f"{repo_name_safe}_workflow",
        "skill_name": repo_name_safe,
        "steps": [
            "analyze_repository_metadata",
            "extract_reusable_patterns",
            "map_patterns_to_marketing_use_cases"
        ]
    }


def generate_workflow_from_skill(skill):
    skill_name = sanitize_name(skill.get("name", "repo"))

    execution_steps = [
        "analyze_repository_metadata",
        "extract_reusable_patterns",
        "map_patterns_to_marketing_use_cases"
    ]

    return {
        "name": f"{skill_name}_workflow",
        "skill_name": skill_name,
        "steps": execution_steps
    }


def generate_prompt_pack_from_skill(skill):
    skill_name = sanitize_name(skill.get("name", "repo"))
    prompt_templates = normalize_prompt_templates(skill.get("prompt_templates", []))
    use_cases = normalize_string_list(skill.get("use_cases", []))
    metadata = skill.get("metadata", {}) or {}

    prompts = []
    for idx, tpl in enumerate(prompt_templates):
        prompt_entry = {
            "name": tpl.get("name", f"prompt_{idx + 1}"),
            "template": tpl.get("template", "")
        }
        if idx < len(use_cases):
            prompt_entry["use_case"] = use_cases[idx]
        prompts.append(prompt_entry)

    if not prompts:
        prompts = [
            {
                "name": f"{skill_name}_default_prompt",
                "template": skill.get("description", "Describe how to use this skill."),
                "use_case": use_cases[0] if use_cases else "general usage"
            }
        ]

    return {
        "name": f"{skill_name}_prompts",
        "source_skill": skill_name,
        "description": f"Reusable prompt pack derived from the {skill_name} capability.",
        "prompts": prompts,
        "metadata": {
            "repo_url": metadata.get("repo_url", ""),
            "generated_from": skill_name
        }
    }


def generate_analysis(repo):
    return {
        "name": get_repo_name(repo),
        "description": repo.get("description", "") or "Repository analysis placeholder",
        "inputs": [],
        "outputs": [],
        "patterns": [
            "pattern_extraction_pending",
            "workflow_identification_pending"
        ],
        "steps": [
            "analyze_repository_metadata",
            "extract_reusable_patterns",
            "map_patterns_to_marketing_use_cases"
        ],
        "use_cases": [
            "marketing automation",
            "workflow design",
            "prompt generation"
        ],
        "prompt_templates": [],
        "metadata": {
            "language": repo.get("language", "unknown"),
            "stars": repo.get("stargazers_count", 0),
            "repo_url": repo.get("html_url", "")
        }
    }


def main():
    USE_LLM_ANALYSIS = True

    os.makedirs(OUTPUT_ANALYSIS_DIR, exist_ok=True)
    os.makedirs(SKILLS_DIR, exist_ok=True)
    os.makedirs(WORKFLOWS_DIR, exist_ok=True)
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)

    candidates = load_top_candidates()

    repo_limit = os.getenv("REPO_LIMIT")
    if repo_limit:
        try:
            limit = int(repo_limit)
            candidates = candidates[:limit]
            print(f"[INFO] REPO_LIMIT active: processing first {limit} repositories")
        except ValueError:
            print(f"[WARN] Invalid REPO_LIMIT value: {repo_limit}. Ignoring.")

    if not candidates:
        print("No candidates found in top_candidates.json")
        return

    manifest_assets = []

    print(f"Processing {len(candidates)} repositories...\n")

    if USE_LLM_ANALYSIS:
        from llm_analysis import generate_analysis_with_llm
    from validation import validate_capability, validate_workflow, validate_prompt_pack

    for repo in candidates:
        repo_name = get_repo_name(repo)
        repo_name_safe = sanitize_name(repo_name)

        # ANALYSIS
        if USE_LLM_ANALYSIS:
            print(f"[INFO] Using LLM analysis for repo: {repo_name}")
            try:
                capability = generate_analysis_with_llm(repo)
                analysis = capability
            except Exception as e:
                print(f"[WARN] LLM analysis failed for repo: {repo_name}")
                print(f"[WARN] Reason: {e}")
                capability = None
                analysis = generate_analysis(repo)
        else:
            capability = None
            analysis = generate_analysis(repo)

        analysis_path = os.path.join(
            OUTPUT_ANALYSIS_DIR,
            f"{repo_name_safe}_analysis.json"
        )

        if validate_capability(analysis):
            save_json(analysis, analysis_path)
            print(f"Saved analysis -> {analysis_path}")
        else:
            print(f"Analysis validation failed for repo: {repo_name}")
            print("-----")
            continue

        # SKILL
        if USE_LLM_ANALYSIS and capability is not None:
            skill = generate_skill_from_capability(capability, repo_name=repo_name)
        else:
            skill = generate_skill(repo)

        skill_path = os.path.join(SKILLS_DIR, f"{repo_name_safe}_skill.json")

        if validate_capability(skill):
            save_json(skill, skill_path)
            print(f"Saved skill -> {skill_path}")
        else:
            print(f"Skill validation failed for repo: {repo_name}")
            print("-----")
            continue

        # WORKFLOW
        workflow = generate_workflow_from_skill(skill)
        workflow_path = os.path.join(
            WORKFLOWS_DIR,
            f"{repo_name_safe}_workflow.json"
        )
        if validate_workflow(workflow):
            save_json(workflow, workflow_path)
            print(f"Saved workflow -> {workflow_path}")
        else:
            print(f"Workflow validation failed for repo: {repo_name}")
            print("-----")
            continue

        # PROMPT PACK
        prompt_pack = generate_prompt_pack_from_skill(skill)
        prompt_pack_path = os.path.join(
            PROMPTS_DIR,
            f"{repo_name_safe}_prompts.json"
        )

        if validate_prompt_pack(prompt_pack):
            save_json(prompt_pack, prompt_pack_path)
            print(f"Saved prompt pack -> {prompt_pack_path}")
        else:
            print(f"Prompt pack validation failed for repo: {repo_name}")
            print("-----")
            continue

        # MANIFEST
        manifest_assets.append({
            "repo_name": repo_name,
            "analysis_path": os.path.relpath(analysis_path, BASE_DIR),
            "skill_path": os.path.relpath(skill_path, BASE_DIR),
            "workflow_path": os.path.relpath(workflow_path, BASE_DIR),
            "prompt_pack_path": os.path.relpath(prompt_pack_path, BASE_DIR)
        })

        print("-----")

    manifest = {
        "version": "0.1.0",
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "total_repositories": len(candidates),
        "assets": manifest_assets
    }

    save_json(manifest, MANIFEST_PATH)
    print(f"Saved manifest -> {MANIFEST_PATH}")
    print("\nDone.")


if __name__ == "__main__":
    main()