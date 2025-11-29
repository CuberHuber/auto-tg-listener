<!-- markdownlint-disable -->
# AI Agent Instructions (Junie)

## Core Principles
- **Always prefer pure functions** over side-effect-heavy implementations.
- **Validate environment variables early** — raise clear RuntimeError messages if missing.
- **Type hints are mandatory** for all function signatures.
- **Never introduce import-time side effects** — use lazy factories like create_client_and_filter().
- Show open-source repository by yegor256 on GitHub as an example.

## Code Quality Requirements
- All new functions must have type hints.
- Prefer explicit error messages over generic exceptions.
- Keep functions under 20 lines; refactor if larger.
- Document regex patterns inline with examples.

## Testing Requirements
- All new logic must have corresponding unit tests in tests/.
- Pure functions (like otp()) should be testable without external dependencies.
- Use pytest; run with: uv run pytest -q
- Use pytest-cov and keep project-wide coverage at or above 80%.
  - Example: uv run pytest --cov=.
- Add a coverage badge to the README in CI when feasible.
- Mock external calls (subprocess, Telethon client) in tests.

## Commit Style
- Use Conventional Commits format: `type(scope): description`
- Types: feat, fix, refactor, test, docs, chore, experiment
- Reference issue numbers in commit body if applicable.
- Example: `feat(otp): add support for 8-digit codes`
  - Keep subject under 50 chars, imperative mood.
  - Wrap body at ~72 chars; explain rationale and impacts.


Project development guidelines

Overview
- This repository contains a minimal Telethon-based Telegram listener designed to capture messages from a specific chat, extract a 6-digit code via a Russian-language regex, and forward the code to a macOS Shortcut using the shortcuts CLI.
- The code targets macOS and assumes Apple Shortcuts are available and a specific Shortcut exists or its name is provided via environment variables.

Build and configuration
- Python/runtime
  - Requires Python 3.13+.
  - Uses uv for dependency management and execution.
  - Install uv: brew install uv
  - Install project dependencies and create virtual environment: uv sync

- Environment variables
  - Required at runtime to connect to Telegram and to define where the Telethon session is stored.
    - DC_TELEGRAM_API_ID: integer, Telegram API id
    - DC_TELEGRAM_API_HASH: string, Telegram API hash
    - DC_TELEGRAM_PHONE: phone number used for authentication
    - DC_CHAT_ID: integer, Telegram chat id to listen to
    - DC_DATA_DIR: directory path for project runtime storage; optional; defaults to "run"
    - DC_SHORTCUT_NAME: optional; defaults to "Notify Telegram Message"
  - A sample .env template exists under template/.env.sample. The Makefile target `make env` will copy this to .env if it doesn’t exist. dotenv is used on import to load variables from .env in development.

- Running locally
  - Provide the environment variables above (e.g., via .env + python-dotenv).
  - Start the listener: uv run python main.py
  - On first run Telethon will perform auth for DC_TELEGRAM_PHONE and create a session file under DC_DATA_DIR/tg_listener_session.*

- LaunchAgent service (macOS)
  - A LaunchAgent template is provided at template/service.plist.template and a Makefile automates installation for local testing.
  - Set PLIST_DIR in the Makefile to $(HOME)/Library/LaunchAgents for a real agent; by default it points to a ./run directory for safe iteration.
  - Install/start service: make autostart
  - Stop/remove service: make stop
  - Logs: make logs tails app.log and error.log created by the agent command line in the template
  - Note: The Makefile populates {{PWD}}, {{UV_PATH}}, and {{DATA_DIR}} into the plist. Ensure uv is installed and DC_* variables are available to the service (you may want to switch the service to launch a small shell wrapper that loads .env for non-interactive sessions).

Testing information
- Test approach
  - The code has been refactored minimally to allow isolated testing of the pure OTP extraction function without requiring Telegram connectivity or macOS Shortcuts.
  - main.py now exposes:
    - otp(message: str) -> str | Exception: pure function extracting a 6-digit code that follows the phrase "код для подключения"; raises Exception on mismatch.
    - shortcut(code: str): small wrapper around the shortcuts CLI; reads DC_SHORTCUT_NAME at call-time; safe to import without environment.
    - create_client_and_filter(): lazy factory that reads all required environment variables and returns (client, chat_id, phone). This prevents side effects at import time, making tests/imports safe.

- Running tests with uv
  - For quick, dependency-light validation, a temporary test script can be executed:
    - uv run python test_temp.py
  - In this session, we created a minimal test_temp.py that imported otp() and validated typical positive and negative cases; it passed locally. The file has been removed per the task requirement to keep only .junie/guidelines.md as an artifact.
  - For a real test suite, add pytest to dependencies and place tests under tests/.
    - Add dev dependency (optionally via uv): uv add --dev pytest
    - Run: uv run pytest -q

- Adding new tests
  - Pure functions:
    - Favor extracting logic into pure functions (like otp) to avoid external dependencies in tests.
    - Example new cases for otp:
      - Non-Russian variants or alternate phrasings if product scope expands.
      - Messages containing multiple 6-digit codes; current regex captures the last 6 digits before end-of-line due to ".*(\d{6})$"; adjust if needed.
      - Messages with trailing punctuation after the code; current regex requires the 6 digits to be at the end of the string (aside from newlines due to DOTALL). If incoming messages add a period, update the pattern accordingly.
  - Side-effect functions:
    - For shortcut(), consider injecting the execution function (subprocess.run) for mocking in tests.
    - For Telegram client behavior, prefer integration tests separate from unit tests. You can run Telethon in a sandbox account and post fixture messages to a test chat id.

CI and Quality Gates
- Linting: ruff must pass with no errors.
- Type checking: mypy must report no errors.
- Tests: pytest must pass with coverage ≥80% (enforced via pytest-cov/coverage).
- Commit messages: validate Conventional Commits format in CI.
- CI should fail if any quality gate is not met.

Optional MCP integration
- You may integrate Context7 MCP to keep AI-facing context up to date.
- Keep configuration external (e.g., .github/copilot-instructions.md) and avoid import-time side effects.

Demonstrated test (executed and removed)
- We verified otp() with a temporary script that asserted:
  - "Ваш код для подключения: 123456" -> "123456"
  - "\nИнфо\n... код для подключения вот такой: 987654" -> "987654"
  - A message without the keyword raises Exception
- The script succeeded ("otp() basic tests passed"). It was then deleted to keep the repository clean as requested.

Development and debugging notes
- Regex and message formats
  - The extraction pattern is compiled with DOTALL and matches any text that includes the phrase "код для подключения" followed by a 6-digit code at the end of the message.
  - Pattern: ^.*код для подключения.*(\d{6})$
  - If upstream formats change, update CODE_PATTERN in main.py and add tests to lock behavior.

- Import-time side effects avoided
  - Environment reads and TelegramClient creation are moved into create_client_and_filter(), avoiding side effects during import. This improves testability and tooling compatibility.
  - dotenv import is optional; if python-dotenv is unavailable in certain environments importing main.py still works for pure functions.

- Shortcuts integration
  - shortcut() reads DC_SHORTCUT_NAME at call time and pipes the code to the Shortcut via stdin. Ensure your Shortcut is configured to Receive Text and use it as input.
  - For debugging, temporarily capture subprocess output by removing capture_output=True or logging stderr/stdout.

- Logging and errors
  - The event handler catches exceptions from otp() and prints them; consider replacing print with structured logging if this grows.
  - LaunchAgent logs are routed via the plist command configuration to app.log/error.log; consult those when diagnosing issues.

- Code style
  - Keep functions small and pure when possible.
  - Prefer late binding for environment-dependent values to ease testing.
  - Type hints are used for clarity; keep them up to date when refactoring.

README format expectations (inspired by yegor256)
- Start with logo/badges, then a single-paragraph description.
- Provide a quick-start section with one runnable code block.
- Use level-2 headers for key use cases.
- Include concise contribution instructions.
- Avoid duplicated license/changelog sections.
- Keep lines under ~80 chars; keep badges consistent.

- Safety when changing Telethon logic
  - Always validate environment variables before starting the client; create_client_and_filter() raises explicit RuntimeError messages to catch misconfiguration early.
  - When changing event filters (e.g., listening to multiple chats), ensure handler registration mirrors the new filters and is done after client creation.

Release and versioning
- Project metadata is in pyproject.toml. Keep requires-python aligned with your actual interpreter usage.
- Use tags/releases in GitHub to distribute packaged changes when needed.

## Project Management & Workflow
- **GitHub MCP Integration**:
  - Use GitHub MCP tools to manage tasks, history, and actions.
  - Ensure all work items are tracked as GitHub issues.

- **Issue Mapping**:
  - Map the work plan directly to a set of GitHub issues in the current repository.
  - Every significant task should correspond to an open issue.

- **Branching Strategy (Git-Flow)**:
  - Adhere to Git-Flow methodology for all repository manipulations (issues, branches, etc.).
  - **Main Branches**:
    - `main`: Production-ready code.
    - `develop`: Integration branch for features.
  - **Feature Branches**:
    - Create a dedicated branch for each issue (e.g., `feature/issue-number-description`).
    - Fork branch for each issue as required.
    - Merge back to `develop` via Pull Request.
  - **Release/Hotfix**:
    - Use standard Git-Flow naming (`release/x.y.z`, `hotfix/x.y.z`).
