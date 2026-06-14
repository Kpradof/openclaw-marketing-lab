# Pipeline

## 1. Discover repositories

`github_repo_miner.py` loads `config/keywords.json`, searches GitHub, and writes repository metadata to:

```text
research/repos.json
```

## 2. Analyze and rank candidates

`repo_analyzer.py` and `top_candidates.py` score and select repositories worth converting into reusable capabilities.

Outputs:

```text
research/repo_candidates.json
research/top_candidates.json
```

## 3. Extract capabilities

For selected repositories, the extraction step produces structured capability JSON under:

```text
research/openclaw_outputs/
```

Capabilities include:

- inputs
- outputs
- reusable patterns
- workflow steps
- use cases
- prompt templates
- source metadata

## 4. Generate reusable assets

`generate_assets.py` converts capability JSON into:

```text
skills/
workflows/
prompts/generated/
generated/manifest.json
```

## 5. Validate

`validate_all.py` checks that generated assets parse correctly, match schemas, and that every manifest path exists.

## 6. Review

Weekly automation opens a pull request. Generated changes should be reviewed before merge.
