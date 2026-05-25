# Generated assets

The pipeline creates four kinds of reusable artifacts.

## Capability analysis

Path:

```text
research/openclaw_outputs/<repo>_analysis.json
```

This is the structured interpretation of a source repository.

## Skill

Path:

```text
skills/<repo>_skill.json
```

A skill describes the reusable capability: triggers, inputs, outputs, use cases, patterns, and prompt templates.

## Workflow

Path:

```text
workflows/<repo>_workflow.json
```

A workflow describes the execution steps associated with a skill.

## Prompt pack

Path:

```text
prompts/generated/<repo>_prompts.json
```

A prompt pack collects reusable prompts derived from the capability.

## Manifest

Path:

```text
generated/manifest.json
```

The manifest is the index of generated assets and is useful for downstream tools or catalogs.
