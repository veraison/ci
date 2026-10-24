# Shared CI for Veraison repositories

Reusable workflows and tool configurations for the Veraison Go and Rust projects.

## Workflows

| Workflow | Purpose |
|---|---|
| [`go-test.yml`](.github/workflows/go-test.yml) | Go build & test |
| [`go-cover.yml`](.github/workflows/go-cover.yml) | Go minimum test coverage |
| [`go-lint.yml`](.github/workflows/go-lint.yml) | Go `make lint` |
| [`rust.yml`](.github/workflows/rust.yml) | Rust lint, test and cargo-deny |
| [`openapi.yml`](.github/workflows/openapi.yml) | OpenAPI validation |

Example (see each workflow's `inputs` for options):

```yaml
name: ci

on:
  push:
    branches: ["**"]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.event_name }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: ${{ github.ref_name != github.event.repository.default_branch }}

jobs:
  test:
    uses: veraison/ci/.github/workflows/go-test.yml@main
  cover:
    uses: veraison/ci/.github/workflows/go-cover.yml@main
    with:
      min-coverage: '80.0'
```

## Configurations

[`configs/`](configs) holds the shared configurations, synced into each project
by [`scripts/sync-config.py`](scripts/sync-config.py) and the
[`sync-configs`](.github/workflows/sync-configs.yml) workflow.

Go projects `include mk/lint.mk`, so `make lint` runs the same golangci-lint
locally and in CI.
