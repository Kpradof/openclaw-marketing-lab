# openclaw-marketing-lab

This project turns GitHub repositories into reusable AI capabilities for marketing systems.

Instead of treating repositories as code that only needs to be read manually, the goal here is to treat them as capabilities that can be extracted, structured, validated, and reused.

The system takes relevant repositories, analyzes them, and converts them into assets like skills, workflows, prompt packs, and a manifest that ties everything together.

## Why I built this

A lot of useful open-source work already exists, but most of it is difficult to reuse directly inside AI systems.

You can learn from a repository, but you usually cannot plug it into a larger workflow without first interpreting its structure, purpose, and patterns.

I built this project to explore a different model:

`repository -> structured capability -> reusable building block`

The goal is to make repositories easier to turn into components for agentic marketing systems.

## What it does

Right now the project can:

- discover and score relevant GitHub repositories
- select top candidates for deeper analysis
- use an LLM to extract structured capability data
- validate those outputs with JSON schemas
- generate reusable skills
- generate workflows from those skills
- generate prompt packs from the extracted capability
- build a manifest of generated assets
- run workflows through a simple orchestrator
- open pull requests automatically through GitHub Actions for review

## Core idea

This system transforms:

`repo -> metadata`

into:

`repo -> capability -> skill -> workflow -> prompt pack`

That makes a repository more useful as a system component instead of just a reference.

## Architecture

The flow looks like this:

```text
GitHub repositories
  -> ingestion and scoring
  -> top_candidates.json
  -> LLM capability extraction
  -> validated structured JSON
  -> skills / workflows / prompt packs
  -> manifest.json
  -> orchestrator
  -> pull request for human review
Project structure
textCopyCopied!
.github/workflows/     automation
research/              candidate data and generated analyses
schemas/               JSON schemas for validation
scripts/               ingestion, generation, validation, orchestration
skills/                generated reusable skills
workflows/             generated workflows
prompts/generated/     generated prompt packs
generated/             manifest and runtime outputs
Outputs
For each selected repository, the system can generate:

research/openclaw_outputs/
Structured capability analysis extracted from repository metadata

skills/
Reusable skill definitions with inputs, outputs, patterns, steps, use cases, and prompt templates

workflows/
Step-based workflow definitions derived from generated skills

prompts/generated/
Prompt packs generated from skill prompt templates

generated/manifest.json
An index of generated assets and their paths

Running locally
Install dependencies:

bashCopyCopied!
pip install openai jsonschema
Set your API key:

bashCopyCopied!
OPENAI_API_KEY=your_key_here
Optionally limit how many repositories are processed during testing:

bashCopyCopied!
REPO_LIMIT=1
Run generation:

bashCopyCopied!
python scripts/generate_assets.py
Run orchestration:

bashCopyCopied!
python scripts/orchestrator.py
Automation
The project currently uses GitHub Actions for scheduled and event-driven automation.

At the moment:

weekly ingestion runs on a scheduled GitHub Actions workflow
asset generation runs through a dedicated workflow and opens pull requests automatically
human review happens through the PR process before anything is merged
OpenClaw was used as a development and iteration layer while building the system, but Git-facing automation is intentionally handled through GitHub Actions instead of giving OpenClaw direct repository access.

That separation keeps the system easier to review and safer to operate.

GitHub workflows
The repository currently uses two automation paths:

weekly-ingestion
Runs repository discovery, scoring, and candidate selection on a schedule

generate-assets-pr
Runs capability extraction and asset generation, then opens a pull request with the generated outputs

The generation workflow expects this repository secret:

OPENAI_API_KEY

Current state
The current version already supports:

repository ingestion
candidate filtering
LLM-based capability extraction
schema validation
skill generation
workflow generation
prompt pack generation
manifest generation
orchestration
pull request automation
What I still want to improve:

richer workflow execution
stronger step handlers
better prompt-to-use-case mapping
scaling the pipeline across more repositories
cleaner composition of reusable AI marketing systems
What I like about this project
The most interesting part for me is the shift in perspective.

A repository is not just a codebase to inspect manually.

It can become a reusable capability that plugs into a larger AI system.

That idea is what this project is really testing.
