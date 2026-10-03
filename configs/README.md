# Shared tool configurations

| File | Tool | Generated in each project as |
|---|---|---|
| [`.golangci.yml`](.golangci.yml) | golangci-lint (`lint` job of `go.yml`) | `.golangci.yml` (+ `.golangci.project.yml`) |
| [`deny.toml`](deny.toml) | cargo-deny (`deny` job of `rust.yml`) | `deny.toml` (+ `deny.project.toml`) |

Do not copy these files by hand: [`scripts/sync-config.py`](../scripts/sync-config.py)
generates each project's file from the common one and the project's optional
`*.project.*` additions, and the `sync-configs` workflow opens pull requests
when a file here changes. See the [main README](../README.md) for details.
