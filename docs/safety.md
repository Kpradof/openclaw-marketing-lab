# Safety and review model

This repo uses generated outputs, so the project intentionally keeps a human in the loop.

## Guardrails

- Generated assets are committed through pull requests, not silently merged.
- Schemas constrain the shape of generated JSON.
- Validation checks parseability, schema conformance, and manifest path integrity.
- Secrets should live in local environment variables or GitHub Actions secrets, never in committed files.
- Generated skills are suggestions and starting points, not authority.

## Review checklist for generated PRs

Before merging weekly generated updates, check:

- Do new repos fit the marketing/GTM capability thesis?
- Are generated descriptions accurate and non-hallucinated?
- Are generated prompt templates useful and safe?
- Did validation pass?
- Are there unexpected file changes outside generated asset paths?

## Credential handling

Use `.env.example` as a template. Do not commit `.env`, tokens, API keys, customer data, or private repository context.
