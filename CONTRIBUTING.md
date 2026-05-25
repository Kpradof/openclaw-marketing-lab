# Contributing

Useful ways to contribute:

## Suggest a seed repository

Open an issue with:

- repository URL
- why it matters for marketing, GTM, RevOps, growth, or agentic workflows
- the capability you think it contains

## Improve discovery

Edit `config/keywords.json` to add better search terms, languages, or filters.

## Improve schemas

Schemas live in `schemas/`. Tightening schemas improves generated asset quality.

## Improve scoring

Scoring logic lives in `scripts/repo_analyzer.py` and `scripts/top_candidates.py`.

## Add examples

Curated examples live in `examples/`. Good examples should include:

- source repo summary
- extracted capability
- generated skill
- generated workflow
- generated prompt pack
- human-readable explanation

## Validate before opening a PR

```bash
python -m pip install -r requirements.txt
python scripts/validate_all.py
python scripts/demo.py
```
