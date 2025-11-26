"""
Automated Telegram message listener with regex filtering and macOS Shortcuts integration.
"""
import asyncio
import os
import re
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient, events

# Load environment variables
load_dotenv()


def get_env(key: str, default: str | None = None) -> str:
    """Get environment variable or raise error."""
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


# Configuration
TELEGRAM_API_ID = int(get_env("DC_TELEGRAM_API_ID"))
TELEGRAM_API_HASH = get_env("DC_TELEGRAM_API_HASH")
TELEGRAM_PHONE = get_env("DC_TELEGRAM_PHONE")
DATA_DIR = get_env("DC_DATA_DIR", "run")
CHAT_ID = int(get_env("DC_CHAT_ID"))
SHORTCUT_NAME = get_env("DC_SHORTCUT_NAME", "Notify Telegram Message")

# Pre-compile regex pattern
CODE_PATTERN = re.compile(r"^.*код для подключения.*(\d{6})$", re.DOTALL)

client = TelegramClient(
    str(Path(DATA_DIR) / 'tg_listener_session'),
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH
)


@client.on(events.NewMessage(chats=CHAT_ID))  # type: ignore[misc]
async def handler(event: events.NewMessage.Event) -> None:
    """Handle new messages."""
    try:
        if event.message and event.message.raw_text:
            try:
                code = otp(event.message.raw_text)
                shortcut(code)
            except ValueError:
                # Message does not match pattern, ignore
                pass
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Error handling message: {exc}")


def otp(message: str) -> str:
    """Extract OTP code from message."""
    match = CODE_PATTERN.search(message)
    if match:
        return match.group(1)
    raise ValueError('Message does not match pattern')


def shortcut(code: str) -> None:
    """Trigger macOS shortcut with the code."""
    try:
        subprocess.run(
            ['shortcuts', 'run', SHORTCUT_NAME],
            input=code.encode('utf-8'),
            capture_output=True,
            timeout=5,
            check=True
        )
    except subprocess.CalledProcessError as exc:
        print(f"Shortcut execution failed: {exc}")
    except subprocess.TimeoutExpired as exc:
        print(f"Shortcut timed out: {exc}")


async def main() -> None:
    """Main application entry point."""
    await client.start(phone=TELEGRAM_PHONE)

    print(f"Listening to: {CHAT_ID}")
    print("Фильтр: сообщения с кодом подключения")

    await client.run_until_disconnected()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
