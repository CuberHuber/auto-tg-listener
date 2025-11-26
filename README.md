<div align="center">

[![Lint Python](https://github.com/CuberHuber/auto-tg-listener/actions/workflows/lint-python.yml/badge.svg)](https://github.com/CuberHuber/auto-tg-listener/actions/workflows/lint-python.yml)
[![Lint Markdown](https://github.com/CuberHuber/auto-tg-listener/actions/workflows/lint-markdown.yml/badge.svg)](https://github.com/CuberHuber/auto-tg-listener/actions/workflows/lint-markdown.yml)
[![Lint Makefile](https://github.com/CuberHuber/auto-tg-listener/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/CuberHuber/auto-tg-listener/actions/workflows/pre-commit.yml)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Issues - daytona](https://img.shields.io/github/issues/CuberHuber/auto-tg-listener)](https://github.com/CuberHuber/auto-tg-listener/issues)
![GitHub Release](https://img.shields.io/github/v/release/CuberHuber/auto-tg-listener)

<!-- Tech stack badges -->
[![Telethon](https://img.shields.io/badge/Telethon-1.x-6A5ACD)](https://github.com/LonamiWebs/Telethon)
[![uv](https://img.shields.io/badge/uv-managed-000000)](https://github.com/astral-sh/uv)
[![dotenv](https://img.shields.io/badge/python--dotenv-optional_at_import-success)](https://github.com/theskumar/python-dotenv)
[![Shortcuts](https://img.shields.io/badge/Apple-Shortcuts-blueviolet)](https://support.apple.com/guide/shortcuts/welcome/mac)

</div>

&nbsp;

<div align="center">
  <h1>Totpify</h1>

  <!-- One-liner description -->
  <b>🤖 Automated Telegram message listener with regex filtering and macOS Shortcuts integration</b>

  <!-- Quick links -->
  [Overview](#overview) • [Features](#features) • [Quick Start](#quick-start) • [Setup](#setup) • [Environment](#environment) • [LaunchAgent](#macos-launchagent) • [Tests](#tests)
</div>

---

## Overview

This is a minimal Telethon-based Telegram listener that watches a specific
chat for messages containing a Russian phrase with a 6‑digit code (OTP) and
forwards the extracted code to a macOS Shortcut via the shortcuts CLI.

- Extracts a 6‑digit OTP that follows the target phrase
- Forwards the code to a configurable Apple Shortcut via stdin
- Runs in the foreground or as a macOS LaunchAgent for background use

---

## Setup

### From source with uv (Recommended for Development)

> [uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver. It's the recommended way to set up the project for development.

#### Step 1: Install uv

```bash
brew install uv
```

#### Step 2: Clone the Repository

```bash
git clone https://github.com/CuberHuber/auto-tg-listener.git
cd auto-tg-listener
```

#### Step 3: Create Virtual Environment and install deps

```bash
uv sync
```

#### Step 4: Prepare environment file and runtime dir

```bash
make env   # copies template/.env.sample -> .env if not present and creates run/ directory
```

---

## Features

- Seamless integration with Apple Shortcuts
- 2FA Code Extraction
- Powerful regex pattern matching for precise message filtering
- MacOS LaunchAgent for background operation

---

## Quick Start

### 1. Get Telegram API Credentials

1. Visit <https://my.telegram.org/> (mobile device recommended)
2. Sign in and go to **API development tools**
3. Create a new application

    ```text
    App title: Demo Message Listener
    Short name: demomsglistener
    URL: [leave empty]
    Platform: Desktop
    Description: [leave empty]
    ```

4. Save your `api_id` and `api_hash`

### 2. Get Telegram Chat ID

1. Find the bot in Telegram: `@RawDataBot`.
2. Start the bot and follow the prompts.
3. The bot will return your `chat_id`.

### 3. Configure environment

1. Go to the project repository: `cd auto-tg-listener`
2. Fill in the `.env` file

```dotenv
DC_TELEGRAM_API_ID=[api_id]
DC_TELEGRAM_API_HASH=[api_hash]
DC_TELEGRAM_PHONE=[your_phone]

DC_CHAT_ID=[chat_id]
DC_SHORTCUT_NAME="Notify Telegram Message"

DC_DATA_DIR=run
```

### 4. Create a Shortcut

1. Launch the `Shortcuts` app.

#### Step 1: Create new shortcut

1. In `Shortcuts`, click the `+` button in the top toolbar.
2. A blank shortcut editor opens named "**Untitled Shortcut**".

#### Step 2: Change the name of the shortcut

1. Click on "**Untitled Shortcut**" or "**Shortcut Name**" at the top.
2. Enter the name: `Notify Telegram Message`.
3. Press _Enter_.

#### Step 3: Shortcut Receive settings

1. In the right pane, click the ⓘ (Details) icon.
2. Enable "**Use as Quick Action**" (to run from other apps).
3. In "**Receives**", choose "**Text**" from the dropdown.
4. In the editor, set **Shortcut Input** to `Text`.
5. Add the actions `Copy to Clipboard` and `Show Notification` (optional).

#### Step 4: Fill in the logic

<img width="611" height="244" alt="Screenshot 2025-10-06 at 11 39 43" src="https://github.com/user-attachments/assets/41932864-aad1-4a1d-88a0-4f4490b81f84" />

### 5. Run locally

```bash
make start-locally
```

> [!WARNING]
> You should see the listener start and print the chat id it listens to.

---

## Environment

Required variables (read at runtime by create_client_and_filter):

- DC_TELEGRAM_API_ID: integer — Telegram API id
- DC_TELEGRAM_API_HASH: string — Telegram API hash
- DC_TELEGRAM_PHONE: string — Phone number used for authentication
- DC_DATA_DIR: path — Directory for Telethon session storage; must be writable
- DC_CHAT_ID: integer — Telegram chat id to listen to

Optional variables:

- DC_SHORTCUT_NAME: string — Apple Shortcut name to run; default: "Notify Telegram Message"

> [!NOTE]
> python-dotenv is imported defensively; importing main.py without a .env
> present won’t crash. At runtime, ensure variables are actually set (via
> .env or the environment).

---

## macOS LaunchAgent

Run the listener as a background agent using launchd with the provided
template and Makefile.

### 1. Prerequisites

- uv is installed and available in PATH
- .env is configured (see [Setup](#step-4-prepare-environment-file-and-runtime-dir) and [Environment](#3-configure-environment))
- The Apple Shortcut is set to Receive: Text

### 2. Choose a destination for the plist

- Default: the Makefile uses ./run for safe iteration
- For a real agent: set PLIST_DIR to $(HOME)/Library/LaunchAgents in the Makefile

### 3. Install and start the agent

```bash
make autostart
```

### 4. View logs

```bash
make logs
```

This tails app.log and error.log written by the agent command.

### 5. Stop or remove the agent

```bash
make stop
```

> [!WARNING]
> LaunchAgents inherit a minimal PATH. If the shortcuts CLI or uv is not
> found, adjust PATH in template/service.plist.template or use absolute
> paths.

<!-- Separator for blockquotes -->

> [!NOTE]
> If the agent doesn't see your environment variables, use a small wrapper
> script that loads .env before invoking uv, or export variables at the user
> level.

---

## Troubleshooting

- Telethon login prompts or session issues: delete files under DC_DATA_DIR and run again to re-authenticate.
- shortcuts: command not found — Ensure Shortcuts CLI is available on macOS 12+ (preinstalled) and accessible in PATH for launchd. Adjust PATH in the plist if needed.
- No code extracted — Verify the incoming message ends with the 6 digits after the phrase and update CODE_PATTERN if upstream format has changed.

---

## Tests

Run the test suite to verify logic.

```bash
make test
```

---

## Contributing

We welcome small, focused contributions.

- Follow Conventional Commits, e.g. `feat(otp): add 8-digit support`.
- Keep functions pure and under 20 lines; add type hints to all functions.
- Avoid import-time side effects; prefer lazy factories (e.g.,
  create_client_and_filter()).
- Tests: place unit tests under tests/ and mock external calls
  (subprocess, Telethon). Maintain ≥80% project-wide coverage.
  Run: `uv run pytest --cov=.`
- Lint/type-check locally before pushing: ruff and mypy should pass.
- See .junie/guidelines.md for full details and quality gates.

## License

MIT — see LICENSE.
