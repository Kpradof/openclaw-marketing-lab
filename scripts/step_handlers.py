from typing import Dict, Any
from llm_analysis import client


def log(message: str):
    print(f"[step] {message}")


# --------------------------------------
# CORE HANDLERS
# --------------------------------------

def analyze_repository_metadata(context: Dict[str, Any], skill: Dict[str, Any]):
    log("Analyzing repository metadata")

    context["repository_analysis"] = {
        "skill_name": skill.get("name"),
        "description": skill.get("description", ""),
        "metadata": skill.get("metadata", {}),
    }


def extract_reusable_patterns(context: Dict[str, Any], skill: Dict[str, Any]):
    log("Extracting reusable patterns")

    patterns = skill.get("patterns", [])

    context["reusable_patterns"] = patterns or [
        "placeholder_pattern_1",
        "placeholder_pattern_2",
    ]


def map_patterns_to_marketing_use_cases(context: Dict[str, Any], skill: Dict[str, Any]):
    log("Mapping patterns to marketing use cases")

    patterns = context.get("reusable_patterns", [])
    use_cases = skill.get("use_cases", [])

    context["mapped_use_cases"] = {
        "patterns": patterns,
        "use_cases": use_cases,
    }


# --------------------------------------
# LLM-POWERED HANDLER
# --------------------------------------

def generate_llm_insights(context: Dict[str, Any], skill: Dict[str, Any]):
    log("Generating LLM insights")

    patterns = context.get("reusable_patterns", [])
    use_cases = context.get("mapped_use_cases", {}).get("use_cases", [])

    prompt = f"""
You are an AI marketing strategist.

Given these reusable patterns:
{patterns}

And these use cases:
{use_cases}

Generate:
- 3 actionable AI agent recommendations
- each with a clear action and expected outcome

Return clean text without formatting or markdown.
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        context["llm_insights"] = response.output_text

    except Exception as e:
        log(f"LLM step failed: {e}")
        context["llm_insights"] = "LLM generation failed"


# --------------------------------------
# DEFAULT HANDLER
# --------------------------------------

def default_handler(step: str, context: Dict[str, Any], skill: Dict[str, Any]):
    log(f"No handler for step '{step}'")

    context.setdefault("unhandled_steps", []).append(step)


# --------------------------------------
# ACTION REGISTRY
# --------------------------------------

ACTION_REGISTRY = {
    "analyze_repository_metadata": analyze_repository_metadata,
    "extract_reusable_patterns": extract_reusable_patterns,
    "map_patterns_to_marketing_use_cases": map_patterns_to_marketing_use_cases,
    "generate_llm_insights": generate_llm_insights,
}