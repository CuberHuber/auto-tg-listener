from pathlib import Path

from telethon import TelegramClient, events
import subprocess
import asyncio
import re
from dotenv import load_dotenv
import os

load_dotenv()


TELEGRAM_API_ID = int(os.getenv("DC_TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("DC_TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("DC_TELEGRAM_PHONE")
DATA_DIR = os.getenv("DC_DATA_DIR")

chat_id = os.getenv("DC_CHAT_ID")
SHORTCUT_NAME = os.getenv("DC_SHORTCUT_NAME", "Notify Telegram Message")

# Pre-compile regex pattern
CODE_PATTERN = re.compile(r"^.*код для подключения.*(\d{6})$", re.MULTILINE | re.DOTALL)

client = TelegramClient(Path(DATA_DIR) / 'tg_listener_session', int(TELEGRAM_API_ID), TELEGRAM_API_HASH)


@client.on(events.NewMessage(chats=chat_id))
async def handler(event):
    try:
        if event.message.text is not None and (code := otp(event.message.text)):
            shortcut(code)
    except Exception as e:
        print(e)


def otp(message: str) -> str | Exception:
    match = CODE_PATTERN.search(message)
    if match:
        code = match.group(1)
        return code
    else:
        raise Exception('Message does not match pattern')

def shortcut(code: str):
    subprocess.run(
        ['shortcuts', 'run', SHORTCUT_NAME],
        input=code.encode('utf-8'),
        capture_output=True,
        timeout=5
    )


async def main():
    await client.start(TELEGRAM_PHONE)  # type: ignore

    print(f"Listening to: {chat_id}")
    print(f"Фильтр: сообщения с кодом подключения")

    await client.run_until_disconnected()  # type: ignore


if __name__ == '__main__':
    asyncio.run(main())
