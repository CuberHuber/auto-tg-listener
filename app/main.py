"""
Main module.

SPDX-FileCopyrightText: Copyright (C) 2025 Roman Lupashko (CuberHuber)
SPDX-License-Identifier: MIT
"""

from app.project import AbstractHealthy
from app.telegram import AbstractTelegramChannel
from app.patterns import AbstractPattern, Otp


class App:
    """App entry class."""

    _components: AbstractHealthy
    _channel: AbstractTelegramChannel
    _pattern: AbstractPattern

    def __init__(
        self,
        channel: AbstractTelegramChannel,
        pattern: AbstractPattern,
        components: AbstractHealthy
    ) -> None:
        """Primary constructor."""
        self._channel = channel
        self._pattern = pattern
        self._components = components

    def healthcheck(self) -> None:
        """Project health checking."""
        self._components.check()

    async def run(self) -> None:
        """Run the app."""
        await self._channel.start()
        async for event in self._channel.events():
            ##
            # @todo #2:120m/DEV Implement shortcut call for OTP codes.
            ##
            Otp(event.message, self._pattern)
        await self._channel.stop()

    async def _setup(self) -> None:
        await self._channel.start()
