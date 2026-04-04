# openclaw-personal-marketing-lab

An agentic system that turns GitHub repositories into reusable AI capabilities for marketing automation.

## Why this project exists

Open-source repositories often contain valuable implementation patterns, workflows, and domain knowledge, but they are difficult to reuse directly as building blocks for AI systems.

This project explores a different approach:

**a repository is not just code — it is a capability that can be extracted, structured, validated, and reused.**

The goal of `openclaw-marketing-lab` is to transform relevant GitHub repositories into reusable assets such as:

- structured capabilities
- skills
- workflows
- prompt packs
- manifest indexes

These assets can then be orchestrated into larger automated marketing systems.

---

## What the system does

The pipeline currently supports:

1. **Repository ingestion**
   - finds relevant GitHub repositories using keyword-based discovery
   - analyzes and scores them
   - filters top candidates

2. **Capability extraction**
   - uses an LLM to analyze repository metadata
   - extracts structured JSON capabilities

3. **Validation**
   - validates generated outputs with JSON schemas

4. **Asset generation**
   - converts capabilities into:
     - skills
     - workflows
     - prompt packs
     - manifest entries

5. **Orchestration**
   - runs workflows against generated skills
   - stores execution runs for inspection

6. **Automation**
   - uses GitHub Actions to generate assets and open pull requests for human review

---

## Core idea

This project transforms:

`repo -> metadata`

into:

`repo -> structured capability -> reusable system building block`

---

## High-level architecture

```text
GitHub repositories
    ↓
ingestion + scoring
    ↓
top_candidates.json
    ↓
LLM capability extraction
    ↓
validated structured capability JSON
    ↓
skills / workflows / prompt packs
    ↓
manifest.json
    ↓
orchestrator execution
    ↓
GitHub PR for human review
