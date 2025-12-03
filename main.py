# SPDX-FileCopyrightText: Copyright (C) 2025 Roman Lupashko (CuberHuber)
# SPDX-License-Identifier: MIT

##
# @todo #11:120m/DEV entrance Elegant Object design
##

"""Automated Telegram message listener.

With regex filtering and macOS Shortcuts integration.
"""

import asyncio
import logging
import sys
from pathlib import Path

from app.main import App
from app.patterns import OtpPattern
from app.project import Environment, Project
from app.telegram import Telegram, TelegramChannel

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    root = Path(__file__).parent

    app = App(
        TelegramChannel(Telegram(root).client()),
        OtpPattern(),
        Project(
            [
                Environment(root),
            ]
        ),
    )
    try:
        app.healthcheck()
        asyncio.run(app.run())
    except KeyboardInterrupt:
        sys.exit(0)
