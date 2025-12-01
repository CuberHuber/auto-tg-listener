<!--
SPDX-FileCopyrightText: Copyright (C) 2025 Roman
Lupashko (CuberHuber)
SPDX-License-Identifier: MIT
-->

# Contributing to Totpify

Help wanted! We'd love your contributions to Totpify. Please review the following guidelines before contributing. Also, feel free to propose changes to these guidelines by updating this file and submitting a pull request.

If you are new here, start with Quick Start and then read the sections on
Style, Testing, and CI.

- [Quick start](#quick-start)
- [Tooling overview (CI and quality gates)](#tooling-overview-ci-and-quality-gates)
- [Git workflow and commit rules](#git-workflow-and-commit-rules)
- [PDD puzzles (0pdd) and task tracking](#pdd-puzzles-0pdd-and-task-tracking)
- [macOS specifics and local services](#macos-specifics-and-local-services)
- [References](#references)

## Quick start

Prereqs:

- Python 3.13+
- uv package manager: `brew install uv`

Install deps and create a virtual env:

```shell
uv sync
```

Create `.env` from template and run locally:

```shell
make start-locally
```

Run the listener as a LaunchAgent (macOS):

```shell
make autostart
make logs
```

Run quality checks:

```shell
make lint
```

Run tests:

```shell
make test
```

## Tooling overview (CI and quality gates)

CI is powered by GitHub Actions. See `.github/workflows/`.
The workflow runs on pushes and PRs to `main` and executes:

1. uv setup and dependency install: `uv sync`
2. License check via reuse (pre-commit)
3. Json Schema linters (pre-commit) with dependabot, github-workflows, github-actions, readthedocs, codecov, github-issue-config, jsonschema, citiation-file-format
4. Action lint (pre-commit)
5. Pre-commit hooks with a lot of checks (pre-commit)
6. Dotenv lint (pre-commit)
7. Ruff check (pre-commit)
8. Secrets detected (pre-commit)
9. Mypy strict type checking (pre-commit)
10. Flake8 with wemake-styleguide (pre-commit)
11. Markdown lint (pre-commit)

## Git workflow and commit rules

Branching strategy follows Git-Flow:

- `main`: production-ready code.
- `dev`: integration branch for features.
- Feature branches: `feature/<issue-number>-short-desc`.
- Merge features into `dev` via Pull Request.

Commit messages must follow Conventional Commits:

- Format: `type(scope): description`
- Types: feat, fix, refactor, test, docs, chore, experiment
- Example: `feat(otp): add support for 8-digit codes`
- Keep subject <= 50 chars; explain rationale in the body (~72 chars per line).
- Reference related issues in the body, e.g., `Refs #123`.

## PDD puzzles (0pdd) and task tracking

We use PDD (Puzzle Driven Development) with 0pdd. See `.0pdd.yml`.
Place in-code puzzles with the `@todo` tag, for example:

```text
##
# @todo #11:120m/DEV refactor function to use typed pattern parameter
##
```

0pdd will collect puzzles and open/update GitHub issues. Keep titles short and
descriptions actionable. For background on PDD, see yegor256's repos below.

## macOS specifics and local services

- Environment variables are loaded via `python-dotenv` inside
  `create_client_and_filter()` to avoid import-time side effects.
- The listener integrates with Apple Shortcuts via the `shortcuts` CLI. Ensure
  a Shortcut exists to receive text, and set `DC_SHORTCUT_NAME` if needed.
- A LaunchAgent template is provided in `template/service.plist.template` and
  automated via `make autostart`. Logs stream to `run/app.log` and
  `run/error.log`.

Required runtime variables (see `.env` template and README):

- `DC_TELEGRAM_API_ID`, `DC_TELEGRAM_API_HASH`, `DC_TELEGRAM_PHONE`
- `DC_CHAT_ID`, `DC_DATA_DIR` (default `run`), `DC_SHORTCUT_NAME` (optional)

## References

[//]: # (@todo #1:60m/DEV add sources link for each actions and pre-commit)
<!-- markdownlint-disable MD034 -->
- yegor256 open-source repos ([style](https://github.com/yegor256/elegantobjects) and [PDD](https://github.com/yegor256/0pdd) inspiration):
- Ruff: https://docs.astral.sh/ruff/
- wemake-python-styleguide: https://wemake-python-styleguide.rtfd.io/
- Mypy: https://mypy-lang.org/
- Pytest: https://docs.pytest.org/
- Codespell: https://github.com/codespell-project/codespell
- dotenv-linter: https://github.com/wemake-services/dotenv-linter
<!-- markdownlint-enable MD034 -->
Thank you for contributing!

### License

By contributing your code, you agree to license your contribution under the terms of the [MIT License](LICENSE).

All files are released with the MIT license.
