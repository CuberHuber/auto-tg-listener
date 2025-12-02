# SPDX-FileCopyrightText: Copyright (C) 2025 Roman Lupashko (CuberHuber)
# SPDX-License-Identifier: MIT
"""Project checkers module"""

import os
from pathlib import Path

from dotenv import load_dotenv
from multipledispatch import dispatch


class AbstractEnvironment:
    """Abstract environment checker."""

    _root: Path
    _variables: list[str]

    def health(self) -> None:
        """Checking all env variables."""
        load_dotenv(self._root / ".env")
        for name in self._variables:
            self._checked_variable(name)

    def _checked_variable(self, name: str) -> None:
        if os.getenv(name) is None:
            raise OSError(f"Missing required environment variable: {name}")


class Environment(AbstractEnvironment):
    """Local environment checker."""

    @dispatch(Path)
    def __init__(self, root: Path) -> None:
        """Secondary constructor."""
        self.__init__(
            root,
            [
                "DC_TELEGRAM_API_ID",
                "DC_TELEGRAM_API_HASH",
                "DC_TELEGRAM_PHONE",
                "DC_CHAT_ID",
                "DC_SHORTCUT_NAME",
                "DC_DATA_DIR",
            ],
        )

    @dispatch(Path, list)  # type: ignore[no-redef]
    def __init__(self, root: Path, variables: list[str]) -> None:
        """Primary constructor."""
        self._root = root
        self._variables = variables


class Project:
    """Project health checker."""

    _environment: AbstractEnvironment

    def __init__(self, environment: AbstractEnvironment) -> None:
        """Primary constructor."""
        self._environment = environment

    def health(self) -> None:
        """Health checking of the project."""
        self._environment.health()
