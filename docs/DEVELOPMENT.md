# Development workflow

## Branches and releases

`develop` is the default branch and holds the latest accepted work. Branch from it and open pull requests against it. `main` holds the latest release: cut a release by merging `develop` into `main` and tagging `vX.Y.Z` on `main`. Patch branches (`vX.Y`) are created only when an older release needs a fix. Full rules: `git-commit-workflow.mdc` in any rules directory.

## Before changing files

1. Check `git status --short` and the current branch. Preserve work you did not create.
2. Read the files you will touch and the rule that owns them.
3. If you add or remove files, plan their `asset-manifest.json` entries first.

## Checks by change

| Change | Required checks |
|---|---|
| Device template or faceplate | validate, tests, preview, release; inspect `dist/preview.html` for every changed face |
| Connector artwork | Same as above; check every template that uses the connector |
| Upstream import | validate; confirm `provenance.json` commit and checksums; no edits to imported bytes |
| Validator, schema, or tooling | validate, tests, plus a new regression test that fails without the change |
| Licensing or policy | validate, release; confirm license texts and notices are in the archive |
| Docs or agent rules | validate (they are manifest entries); mirror equality check below |

Commands are listed in `AGENTS.md`. `PASS` means the licensing, checksum, SVG-safety, and geometry checks passed. It does not mean the layout matches real hardware or that the platform renders it.

## Adding or removing a file

1. Add or remove the file.
2. Add or remove its entry in `asset-manifest.json` by hand, with the correct `license`, `origin`, `source`, `revision`, `copyright`, `modifications`, and `notices`.
3. Run `python tooling/refresh_hashes.py` and review the manifest diff. It refuses to run while the manifest and the file tree disagree.
4. Run the checks for the change type.

## Agent rule mirrors

Rules are kept as identical copies for each agent surface. From the repository root:

```bash
cmp AGENTS.md CLAUDE.md && cmp AGENTS.md GEMINI.md
diff -qr .claude/rules .codex/rules
diff -qr .claude/rules .cursor/rules
diff -qr .claude/rules .gemini/rules
git diff --check
```

## Adaptation record

Reviewed on 2026-10-29 against the Kaleidoscope platform repository (branch `develop`): `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, the 20 rules mirrored under `.claude/rules/`, `.codex/rules/`, `.cursor/rules/`, and `.gemini/rules/`, the skill library, `.github/`, and the activity-logging hook documentation. `NightSquawk/kaleidoscope-snmp-profiles`, which made the same adaptation on 2026-09-13, was used as the precedent for a public data repository. Platform documents are reference material; the rules committed here govern this repository.

| Platform guidance | Adaptation here |
|---|---|
| Core instructions and subagent rule briefing | Focused edits, read before writing, brief delegated agents; library/platform boundaries replace service, RLS, and CSS constraints |
| Git branching and commit workflow | Kept `develop` as the integration branch and `main` as the release branch, Conventional Commits, explicit-path staging, and message files. Release branches are created on demand only. Version-scope tags, migration isolation, and hunk-level commit plans omitted: there is no migration history or parallel release line yet |
| Stash ban and pre-stash build gate | Kept in full; the gate runs the validator and tests because there is no build |
| Changelog generation | No dashboard changelog. `CHANGELOG.md` starts at the first tagged release, written from git log on `main`, consumer-visible changes only |
| Data-interface definition of done | Became the template data contract: stable port IDs, explicit units, evidence for `verified`, and coordinated schema/validator/docs changes |
| Audit logging, form/RUM privacy | Became the public-data rule: no customer data, credentials, real layouts, or telemetry, plus per-file provenance |
| Context7 auto-use | Optional; primary documentation preferred, no MCP configuration copied |
| Validation and QA skill | Verification vocabulary (validated / previewed / verified) and per-change evidence table |
| Docs and writing skill | One owning document per fact; PR description contents |
| Activity logging and session hooks | Not copied. They are internal to the platform's maintainers; hooks, local paths, and any work-tracking metadata stay outside this public repository |
| Gemini mirror | Added: `GEMINI.md` and `.gemini/rules/` alongside Claude, Codex, and Cursor |
| Dependabot | Kept for GitHub Actions only; the tooling has no package dependencies |
| Routes, services, workers, migrations, permissions, auth/session, feature flags, sockets, shadcn, frontend pages | Omitted: this repository has no application, database, UI, or runtime |
| Platform skills, discovery notes, MCP configs, hook scripts | Consulted; not copied, because their paths, services, and environments belong to the platform |

Update this record when importing further platform processes, and check that commands and paths still fit this repository before carrying them over.
