# openclaw-personal-marketing-lab

This project turns GitHub repositories into reusable AI capabilities for marketing systems.

Instead of treating repositories as code you read manually, the idea here is to treat them as capabilities that can be extracted, structured, validated, and reused.

The system takes relevant repositories, analyzes them, and converts them into reusable assets like skills, workflows, prompt packs, and a manifest that ties everything together.

## Why I built this

A lot of useful open-source work already exists, but most of it is hard to reuse directly inside AI systems.

You can learn from a repo, but you usually cannot plug it into a larger system without doing a lot of interpretation first.

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
