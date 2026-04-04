import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

from step_handlers import ACTION_REGISTRY, default_handler


BASE_DIR = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = BASE_DIR / "workflows"
SKILLS_DIR = BASE_DIR / "skills"
RUNS_DIR = BASE_DIR / "generated" / "runs"


class OrchestratorError(Exception):
    pass


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise OrchestratorError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_workflow_path(workflow_name: str) -> Path:
    candidates = [
        WORKFLOWS_DIR / f"{workflow_name}.json",
        WORKFLOWS_DIR / f"{workflow_name}_workflow.json",
    ]
    for path in candidates:
        if path.exists():
            return path

    raise OrchestratorError(
        f"Workflow not found for name '{workflow_name}'. Checked: {[str(p) for p in candidates]}"
    )


def resolve_skill_path(skill_name: str) -> Path:
    candidates = [
        SKILLS_DIR / f"{skill_name}.json",
        SKILLS_DIR / f"{skill_name}_skill.json",
    ]
    for path in candidates:
        if path.exists():
            return path

    raise OrchestratorError(
        f"Skill not found for name '{skill_name}'. Checked: {[str(p) for p in candidates]}"
    )


def load_workflow(workflow_name: str) -> Dict[str, Any]:
    path = resolve_workflow_path(workflow_name)
    workflow = load_json(path)

    if not isinstance(workflow, dict):
        raise OrchestratorError(f"Workflow file must contain a JSON object: {path}")

    return workflow


def load_skill(skill_name: str) -> Dict[str, Any]:
    path = resolve_skill_path(skill_name)
    skill = load_json(path)

    if not isinstance(skill, dict):
        raise OrchestratorError(f"Skill file must contain a JSON object: {path}")

    return skill


def log(message: str) -> None:
    print(f"[orchestrator] {message}")


def save_run_result(context: Dict[str, Any]) -> Path:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    workflow_name = context.get("workflow_name", "workflow")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_path = RUNS_DIR / f"{workflow_name}_{timestamp}.json"

    with open(run_path, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False)

    return run_path


def execute_step(step: str, context: Dict[str, Any], skill: Dict[str, Any]) -> None:
    if not isinstance(step, str) or not step.strip():
        raise OrchestratorError(f"Invalid workflow step: {step!r}")

    log(f"Executing step: {step}")
    action = ACTION_REGISTRY.get(step)

    if action is None:
        default_handler(step, context, skill)
    else:
        action(context, skill)

    context["last_step"] = step
    context.setdefault("executed_steps", []).append(step)


def infer_skill_name(workflow_name: str, workflow: Dict[str, Any]) -> str:
    explicit_skill = workflow.get("skill_name")
    if isinstance(explicit_skill, str) and explicit_skill.strip():
        return explicit_skill

    name = workflow.get("name", workflow_name)
    if isinstance(name, str):
        return name.replace("_workflow", "")

    return workflow_name.replace("_workflow", "")


def run_workflow(
    workflow_name: str,
    initial_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    workflow = load_workflow(workflow_name)
    skill_name = infer_skill_name(workflow_name, workflow)
    skill = load_skill(skill_name)

    steps = workflow.get("steps", [])
    if not isinstance(steps, list):
        raise OrchestratorError("Workflow 'steps' must be a list")

    context: Dict[str, Any] = dict(initial_context or {})
    context["workflow_name"] = workflow.get("name", workflow_name)
    context["skill_name"] = skill.get("name", skill_name)

    log(f"Loaded workflow: {context['workflow_name']}")
    log(f"Loaded skill: {context['skill_name']}")
    log(f"Total steps: {len(steps)}")

    for step in steps:
        execute_step(step, context, skill)

    run_path = save_run_result(context)
    log(f"Saved run -> {run_path}")
    log("Workflow completed successfully.")

    return context


if __name__ == "__main__":
    try:
        result_context = run_workflow("marketingskills")
        print("\nFinal context:")
        print(json.dumps(result_context, indent=2, ensure_ascii=False))
    except OrchestratorError as e:
        log(f"ERROR: {e}")