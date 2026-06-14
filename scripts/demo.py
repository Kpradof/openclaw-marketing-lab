import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXAMPLE_DIR = BASE_DIR / "examples" / "alwrity"
OUTPUT_DIR = BASE_DIR / "examples" / "demo-output"

FILES = {
    "capability.json": BASE_DIR / "research" / "openclaw_outputs" / "alwrity_analysis.json",
    "skill.json": BASE_DIR / "skills" / "alwrity_skill.json",
    "workflow.json": BASE_DIR / "workflows" / "alwrity_workflow.json",
    "prompt-pack.json": BASE_DIR / "prompts" / "generated" / "alwrity_prompts.json",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for output_name, source in FILES.items():
        if not source.exists():
            print(f"Missing source file: {source}")
            return 1
        shutil.copyfile(source, OUTPUT_DIR / output_name)

    skill = load_json(FILES["skill.json"])
    workflow = load_json(FILES["workflow.json"])
    prompt_pack = load_json(FILES["prompt-pack.json"])

    summary = {
        "source_repo": skill.get("source", {}).get("repo_url"),
        "skill": skill.get("name"),
        "description": skill.get("description"),
        "workflow_steps": workflow.get("steps", []),
        "prompt_count": len(prompt_pack.get("prompts", [])),
        "outputs": sorted(p.name for p in OUTPUT_DIR.glob("*.json")),
    }

    with (OUTPUT_DIR / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("Demo generated:")
    print(f"- {OUTPUT_DIR.relative_to(BASE_DIR)}")
    print(f"- skill: {summary['skill']}")
    print(f"- workflow steps: {len(summary['workflow_steps'])}")
    print(f"- prompts: {summary['prompt_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
