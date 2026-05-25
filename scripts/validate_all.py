import json
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator

BASE_DIR = Path(__file__).resolve().parent.parent

SCHEMA_MAP = {
    "capability": BASE_DIR / "schemas" / "capability.schema.json",
    "workflow": BASE_DIR / "schemas" / "workflow.schema.json",
    "prompt_pack": BASE_DIR / "schemas" / "prompt-pack.schema.json",
}

TARGETS = {
    "capability": BASE_DIR / "research" / "openclaw_outputs",
    "workflow": BASE_DIR / "workflows",
    "prompt_pack": BASE_DIR / "prompts" / "generated",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def iter_json_files(directory: Path) -> Iterable[Path]:
    if not directory.exists():
        return []
    return sorted(p for p in directory.glob("*.json") if p.is_file())


def validate_file(path: Path, validator: Draft202012Validator) -> list[str]:
    errors: list[str] = []
    try:
        payload = load_json(path)
    except Exception as exc:
        return [f"{path}: invalid JSON: {exc}"]

    for error in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{path}: {location}: {error.message}")
    return errors


def validate_manifest_paths() -> list[str]:
    manifest_path = BASE_DIR / "generated" / "manifest.json"
    if not manifest_path.exists():
        return [f"Missing manifest: {manifest_path}"]

    errors: list[str] = []
    manifest = load_json(manifest_path)
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        return ["generated/manifest.json: assets must be a list"]

    path_keys = ["analysis_path", "skill_path", "workflow_path", "prompt_pack_path"]
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(f"generated/manifest.json: assets[{index}] must be an object")
            continue
        for key in path_keys:
            value = asset.get(key)
            if not value:
                errors.append(f"generated/manifest.json: assets[{index}].{key} is missing")
                continue
            target = BASE_DIR / value
            if not target.exists():
                errors.append(f"generated/manifest.json: assets[{index}].{key} points to missing path: {value}")
    return errors


def main() -> int:
    all_errors: list[str] = []

    for kind, schema_path in SCHEMA_MAP.items():
        schema = load_json(schema_path)
        validator = Draft202012Validator(schema)
        files = list(iter_json_files(TARGETS[kind]))
        print(f"Validating {kind}: {len(files)} files")
        for path in files:
            all_errors.extend(validate_file(path, validator))

    print("Validating manifest paths")
    all_errors.extend(validate_manifest_paths())

    if all_errors:
        print()
        print("Validation failed:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print("All generated assets are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
