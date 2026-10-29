# kaleidoscope-infrastructure-library

Public hardware definitions, original SVG faceplates, connector drawings, and port-level layouts for Kaleidoscope's infrastructure digital twins. The library is data plus a dependency-free Python validator and packager. Rendering, rack placement, live port state, and tenant inventory live in the separate Kaleidoscope platform repository.

## Start here

Read `README.md`, `CONTRIBUTING.md`, and `LICENSING.md` for purpose, submission rules, and licensing boundaries. Read `docs/DEVELOPMENT.md` for the branch model, checks by change type, and the record of which platform rules were adapted here.

## Layout

| Path | Responsibility |
|---|---|
| `catalog/kaleidoscope/CC0-1.0/devices/` | Kaleidoscope-authored device templates, one JSON file per device |
| `catalog/kaleidoscope/CC0-1.0/connectors.json` | Connector IDs mapped to connector artwork |
| `catalog/upstream/<source>/<license>/` | Byte-preserved upstream imports plus `provenance.json`; never edit |
| `artwork/kaleidoscope/CC0-1.0/` | Original faceplate and connector SVGs |
| `artwork/third-party/` | Third-party artwork with rights evidence (none yet) |
| `asset-manifest.json` | Per-file license, origin, provenance, and SHA-256; authoritative |
| `policy/licenses.json` | Licenses allowed to ship |
| `schemas/` | JSON Schema for device templates (descriptive; the validator is the enforced contract) |
| `tooling/` | `validate.py`, `refresh_hashes.py`, `preview.py`, `release.py` |
| `tests/` | Validator regression tests |
| `.github/workflows/` | CI validation and preview/release artifacts |

## Rules

Read these rule files before making changes. The same files live under `.claude/rules/`, `.codex/rules/`, `.cursor/rules/`, and `.gemini/rules/`; directory presence alone is not a substitute for reading them.

| Rule | File under each rules directory |
|---|---|
| Core behavior and repository boundaries | `core-instructions.mdc` |
| Branches, releases, and scoped commits | `git-commit-workflow.mdc` |
| Shared-worktree preservation | `stash-build-gate.mdc` |
| Templates, ports, connectors, and artwork | `template-data-contract.mdc` |
| Licensing, provenance, and the manifest | `licensing-and-provenance.mdc` |
| Validation and evidence | `validation-and-evidence.mdc` |
| Documentation, research, and change notes | `documentation-and-research.mdc` |

Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` identical, and all four rule directories identical in filenames and contents. Every one of these files is registered in `asset-manifest.json`, so refresh hashes after editing them. User instructions take precedence over these repository defaults.

## Commands

Python 3.11+ (CI uses 3.12), standard library only. Run from the repository root:

```bash
python tooling/validate.py                  # licensing, provenance, checksums, SVG safety, geometry
python -m unittest discover -s tests -v     # validator regression tests
python tooling/preview.py                   # writes dist/preview.html
python tooling/release.py                   # validates, then writes dist/kaleidoscope-infrastructure-library.zip
python tooling/refresh_hashes.py            # only after registering/removing files in the manifest by hand
```

## Essential constraints

- `develop` is the default and integration branch; pull requests target it. `main` holds the latest release and changes only by merging `develop`.
- Every file except `.git`, `dist`, `__pycache__`, and the manifest itself must be registered in `asset-manifest.json` with a correct license and hash, or validation fails.
- Upstream imports stay byte-for-byte. Kaleidoscope additions go in separate files.
- Layouts are `illustrative` unless verified against the device or manufacturer documentation with recorded evidence. Never invent dimensions or port order.
- Published port IDs are stable; changed hardware gets a new template ID.
- No manufacturer imagery without documented permission. No customer data, credentials, real rack layouts, or telemetry: this repository is public.
- Preserve unrelated work. Never stash for routine validation; stage and commit only explicit owned paths.
