# Shared tool configurations

| File | Tool | In each project |
|---|---|---|
| [`.golangci.yml`](.golangci.yml) | golangci-lint | `.golangci.yml`, merged with `.golangci.project.yml` |
| [`deny.toml`](deny.toml) | cargo-deny | `deny.toml`, merged with `deny.project.toml` |
| [`mk/lint.mk`](mk/lint.mk) | `make lint` | `mk/lint.mk` |

Do not edit the copies in the projects, run
[`scripts/sync-config.py`](../scripts/sync-config.py) instead.
