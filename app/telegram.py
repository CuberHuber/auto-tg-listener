# SPDX-FileCopyrightText: Copyright (C) 2025 Roman Lupashko (CuberHuber)
# SPDX-License-Identifier: MIT
"""Telegram clients and Channels module"""

import os
from abc import ABC
from functools import lru_cache

from pathlib import Path
from typing import Any
from collections.abc import AsyncGenerator

from aiochannel import Channel as AioChannel, ChannelClosed

from multipledispatch import dispatch
from telethon import TelegramClient, events as tgEvents


class AbstractTelegram(ABC):
    """Abstract Telegram client wrapper."""

    _id: int
    _hash: str
    _session: Path
    _phone: str

    @lru_cache
    def client(self) -> TelegramClient:
        """Telegram client of telethon."""
        return TelegramClient(str(self._session), self._id, self._hash)


class Telegram(AbstractTelegram):
    """Telegram client wrapper."""

    @dispatch(Path)
    def __init__(self, root: Path) -> None:
        """Secondary constractor."""
        self.__init__(
            root / os.getenv("DC_DATA_DIR") / "tg_listener",
            int(os.getenv("DC_TELEGRAM_API_ID")),
            os.getenv("DC_TELEGRAM_API_HASH"),
        )

    @dispatch(Path, int, str)  # type: ignore[no-redef]
    def __init__(self, session: Path, _id: int, _hash: str) -> None:
        """Primary constructor."""
        self._session = session
        self._id = _id
        self._hash = _hash


class AbstractTelegramChannel(ABC):
    """Abstract Telegram channel listener."""

    _chat: int
    _phone: str
    _telegram: TelegramClient
    _channel: AioChannel[tgEvents.NewMessage.Event]

    async def start(self) -> None:
        """Setup telegram listener and launch it."""
        self._setup()
        await self._telegram.start(self._phone)

    async def stop(self) -> None:
        """To stop the telegram client listener and close the channel."""
        await self._telegram.run_until_disconnected()
        self._channel.close()

    async def events(self) -> AsyncGenerator[tgEvents.NewMessage.Event, Any]:
        """Async telegram message event generator."""
        while True:
            try:
                yield await self._channel.get()
            except ChannelClosed:
                break

    def _setup(self) -> None:
        self._telegram.add_event_handler(
            self._on, tgEvents.NewMessage(chats=self._chat)
        )

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore[no-untyped-def]
        self._channel.close()

    async def _on(self, event: tgEvents.NewMessage.Event) -> None:
        await self._channel.put(event)


class TelegramChannel(AbstractTelegramChannel):
    """Telegram channel listener wrapper."""

    @dispatch(TelegramClient)
    def __init__(self, telegram: TelegramClient) -> None:
        """Secondary constructor."""
        self.__init__(
            telegram,
            str(os.getenv("DC_TELEGRAM_PHONE")),
            int(os.getenv("DC_CHAT_ID")),
        )

    @dispatch(TelegramClient, str, int)  # type: ignore[no-redef]
    def __init__(self, telegram: TelegramClient, phone: str, chat: int) -> None:
        """Secondary constructor."""
        limit: int = 100
        self.__init__(telegram, phone, chat, AioChannel(limit))

    @dispatch(TelegramClient, str, int, AioChannel)  # type: ignore[no-redef]
    def __init__(
        self,
        telegram: TelegramClient,
        phone: str,
        chat: int,
        channel: AioChannel[tgEvents.NewMessage.Event],
    ) -> None:
        """Primary constructor."""
        self._telegram = telegram
        self._phone = phone
        self._chat = chat
        self._channel = channel
