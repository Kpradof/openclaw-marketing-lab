# Architecture

OpenClaw Marketing Lab is a small pipeline for turning public GitHub repositories into reusable AI marketing assets.

```text
GitHub Search
  ↓
Repository candidates
  ↓
Ranking and filtering
  ↓
Capability extraction
  ↓
Schema validation
  ↓
Skill / workflow / prompt-pack generation
  ↓
Manifest
  ↓
Human-reviewed pull request
```

## Core components

| Component | Path | Purpose |
|---|---|---|
| Discovery config | `config/keywords.json` | Search terms, filters, and limits. |
| Miner | `scripts/github_repo_miner.py` | Searches GitHub and stores raw candidate repos. |
| Analyzer | `scripts/repo_analyzer.py` | Scores candidate repos. |
| Top candidates | `scripts/top_candidates.py` | Selects repositories for extraction. |
| Asset generator | `scripts/generate_assets.py` | Converts capabilities into skills, workflows, prompt packs, and manifest entries. |
| Validator | `scripts/validate_all.py` | Validates generated JSON and manifest integrity. |
| Weekly automation | `.github/workflows/weekly-ingestion.yml` | Runs the pipeline and opens a PR. |

## Design principle

The system separates generation from acceptance.

Automation can discover and draft assets, but generated changes enter the repo through pull requests so humans can review the output before it becomes part of the capability library.
