# dmr-openapi-skeleton (Codex Skill)

This repository contains a Codex skill that generates a Django project skeleton using `django-modern-rest` from an OpenAPI specification (`3.1+`).

## What this skill does

- Reads an OpenAPI file and builds a transport-layer skeleton.
- Generates DTOs/serializers, controllers or blueprints, routers, `urls.py`, and OpenAPI docs wiring.
- Adds minimal smoke tests for routes and schema.
- Does not implement business logic by default (only placeholders and TODO points).

## Important statement about `generated_example`

Inside `generated_example`, there is **not a single line of code written by a human**.  
The entire example was generated automatically by Codex from the OpenAPI specification at `generated_example/openapi.yaml` (Thanks Swaager for example file).

Used prompt:


> $dmr-openapi-skeleton Read openapi.yaml and create a new runnable Django project in this folder. Bootstrap the environment with uv, generate pyproject.toml, settings, manage.py, DTOs, controllers, routers,
  docs wiring, and minimal smoke tests. Use PydanticSerializer, include msgspec and openapi extras, and do not implement business logic.



## Structure

- `skills/dmr-openapi-skeleton/SKILL.md` - main skill instructions.
- `skills/dmr-openapi-skeleton/references/*` - OpenAPI to DMR mapping guidance.
- `generated_example/openapi.yaml` - input specification.
- `generated_example/server/*` - generated Django + DMR project.
- `generated_example/tests/*` - generated integration smoke tests.

## Quick start (example)

```bash
cd generated_example
uv sync
uv run python manage.py runserver
```

Docs endpoints after startup:

- `/docs/openapi.json/`
- `/docs/redoc/`
- `/docs/swagger/`
- `/docs/scalar/`

## How to use this skill in Codex

Provide Codex with an OpenAPI file (or a spec URL/text) and ask it to generate a Django + `django-modern-rest` project skeleton.  
The skill follows the rules in `skills/dmr-openapi-skeleton/SKILL.md` and keeps the generated API contract as close as possible to the source spec.
