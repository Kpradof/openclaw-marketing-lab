import os
import json
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEBUG_LLM = os.getenv("DEBUG_LLM") == "1"


ANALYSIS_PROMPT_TEMPLATE = """
You are an expert software analysis assistant.

Analyze the following GitHub repository metadata carefully and extract a detailed, structured capability description as a JSON object.

Repository metadata:
- Name: {name}
- Description: {description}
- Topics: {topics}
- Language: {language}
- Stars: {stars}
- URL: {url}

Your JSON must strictly include these fields:
- name: concise skill or capability name (string)
- description: brief and precise summary of the repo's main purpose and functions (string)
- inputs: list of input parameters or data expected by the capability (each with name, type, description)
- outputs: list of outputs generated or returned by the capability (each with name, type, description)
- patterns: list of reusable patterns, techniques, or processes identified in the repo that can be reused
- steps: ordered list of key processing or usage steps describing the workflow inside the repo capability
- use_cases: common practical scenarios or applications for this capability
- prompt_templates: list of prompt template objects (each with name, template string including placeholders) useful for interacting with or invoking the capability
- metadata: object with language, stars count, repo_url

Rules:
- Return only one valid JSON object.
- Do not wrap the JSON in markdown fences.
- Do not include commentary before or after the JSON.
- If some sections are unknown, use empty lists but still include the keys.
- Ensure metadata includes language, stars, and repo_url.

Example JSON output:

{{
  "name": "example_skill",
  "description": "A capability that does X, Y, and Z.",
  "inputs": [
    {{"name": "input1", "type": "string", "description": "Input text to be analyzed."}}
  ],
  "outputs": [
    {{"name": "output1", "type": "string", "description": "Generated summary."}}
  ],
  "patterns": [
    "pattern1",
    "pattern2"
  ],
  "steps": [
    "Step 1 description",
    "Step 2 description"
  ],
  "use_cases": [
    "Use case 1",
    "Use case 2"
  ],
  "prompt_templates": [
    {{"name": "summary_prompt", "template": "Summarize this text: {{input1}}"}}
  ],
  "metadata": {{
    "language": "Python",
    "stars": 123,
    "repo_url": "https://github.com/example/repo"
  }}
}}
"""


def clean_json_response(text: str) -> str:
    text = (text or "").strip()

    if not text:
        raise ValueError("LLM returned empty response")

    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


def generate_analysis_with_llm(repo):
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        name=repo.get("name", ""),
        description=repo.get("description", ""),
        topics=", ".join(repo.get("topics", [])),
        language=repo.get("language", "unknown"),
        stars=repo.get("stargazers_count", 0),
        url=repo.get("html_url", "")
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    text = response.output_text
    cleaned_text = clean_json_response(text)

    if DEBUG_LLM:
        print("\n[DEBUG] Raw LLM response:")
        print(repr(text))

    try:
        parsed = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        if DEBUG_LLM:
            print("\n[DEBUG] Failed to parse cleaned LLM response as JSON")
            print("[DEBUG] Cleaned response:")
            print(cleaned_text)
        raise ValueError(f"LLM returned invalid JSON: {e}") from e

    if not isinstance(parsed, dict):
        raise ValueError("LLM response was valid JSON but not a JSON object")

    return parsed