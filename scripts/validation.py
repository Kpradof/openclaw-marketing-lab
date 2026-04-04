import json
import jsonschema
from jsonschema import validate
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "schemas" / "capability.schema.json", "r", encoding="utf-8") as f:
    capability_schema = json.load(f)

with open(BASE_DIR / "schemas" / "workflow.schema.json", "r", encoding="utf-8") as f:
    workflow_schema = json.load(f)

with open(BASE_DIR / "schemas" / "prompt-pack.schema.json", "r", encoding="utf-8") as f:
    prompt_pack_schema = json.load(f)


def validate_capability(capability_json):
    try:
        validate(instance=capability_json, schema=capability_schema)
        print("Capability JSON is valid.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation error: {e.message}")
        return False


def validate_workflow(workflow_json):
    try:
        validate(instance=workflow_json, schema=workflow_schema)
        print("Workflow JSON is valid.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Workflow validation error: {e.message}")
        return False


def validate_prompt_pack(prompt_pack_json):
    try:
        validate(instance=prompt_pack_json, schema=prompt_pack_schema)
        print("Prompt pack JSON is valid.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Prompt pack validation error: {e.message}")
        return False
