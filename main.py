"""Automated Telegram message listener.

With regex filtering and macOS Shortcuts integration.
"""

import asyncio
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient, events

# Pre-compile regex pattern
CODE_PATTERN = re.compile(r"^.*код для подключения.*(\d{6})$", re.DOTALL)

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging to stdout."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )


def get_env(key: str, default: str | None = None) -> str:
    """Get environment variable or raise error."""
    env_value = os.getenv(key, default)
    if env_value is None:
        err_msg = f"Missing required environment variable: {key}"
        raise RuntimeError(err_msg)
    return env_value


def otp(message: str) -> str:
    """Extract OTP code from message."""
    match = CODE_PATTERN.search(message)
    if match:
        return match.group(1)
    err_msg = "Message does not match pattern"
    raise ValueError(err_msg)


def shortcut(code: str, shortcut_name: str | None = None) -> None:
    """Trigger macOS shortcut with the code."""
    if shortcut_name is None:
        shortcut_name = get_env("DC_SHORTCUT_NAME", "Notify Telegram Message")

    shortcuts_path = shutil.which("shortcuts")
    if not shortcuts_path:
        logger.error("Shortcuts executable not found")
        return

    try:
        subprocess.run(  # noqa: S603
            [shortcuts_path, "run", shortcut_name],
            input=code.encode("utf-8"),
            capture_output=True,
            timeout=5,
            check=True,
        )
    except subprocess.CalledProcessError:
        logger.exception("Shortcut execution failed")
    except subprocess.TimeoutExpired:
        logger.exception("Shortcut timed out:")


def process_message_text(text: str) -> None:
    """Extract OTP and trigger shortcut."""
    try:
        code = otp(text)
    except ValueError:
        return
    shortcut(code)


async def new_message_handler(event: events.NewMessage.Event) -> None:
    """Handle new messages."""
    try:
        if event.message and event.message.raw_text:
            process_message_text(event.message.raw_text)
    except Exception:
        logger.exception("Error handling message")


def create_client_and_filter() -> tuple[TelegramClient, int, str, str]:
    """Create client and register handlers."""
    load_dotenv()
    api_id = int(get_env("DC_TELEGRAM_API_ID"))
    api_hash = get_env("DC_TELEGRAM_API_HASH")
    phone = get_env("DC_TELEGRAM_PHONE")
    chat_id = int(get_env("DC_CHAT_ID"))
    data_dir = get_env("DC_DATA_DIR", "run")
    shortcut_name = get_env("DC_SHORTCUT_NAME", "Notify Telegram Message")

    client = TelegramClient(
        str(Path(data_dir) / "tg_listener_session"),
        api_id,
        api_hash,
    )

    client.add_event_handler(
        new_message_handler,
        events.NewMessage(chats=chat_id),
    )

    return client, chat_id, shortcut_name, phone


async def main() -> None:
    """Main application entry point."""
    setup_logging()
    client, chat_id, _, phone = create_client_and_filter()
    await client.start(phone=phone)

    logger.info(
        "listening to: %s. Фильтр: сообщения с кодом подключения",  # noqa: RUF001
        chat_id,
    )

    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
