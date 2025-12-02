# SPDX-FileCopyrightText: Copyright (C) 2025 Roman Lupashko (CuberHuber)
# SPDX-License-Identifier: MIT
"""Patterns module"""

import re
from abc import ABC
from functools import lru_cache
from typing import override, AnyStr

from multipledispatch import dispatch


class AbstractPattern(ABC):
    """Abstract Pattern class."""

    _expression: str
    _mode: int

    def matched(self, source: str) -> str | ValueError:
        """Check if the source matches the pattern."""
        _matched = self._pattern().search(source)
        if _matched:
            return str(_matched.group(1))
        raise ValueError(f"Message does not match pattern: {self._expression}")

    @lru_cache
    def _pattern(self):  # type: ignore[no-untyped-def]
        return re.compile(self._expression, self._mode)


class OtpPattern(AbstractPattern):
    """An OTP code in a message regex pattern."""

    @dispatch(str, int)  # type: ignore[no-redef,unused-ignore]
    def __init__(self, expression: str, mode: int) -> None:
        """Primary constructor."""
        self._expression = expression
        self._mode = mode

    @dispatch()  # type: ignore[no-redef]
    def __init__(self) -> None:
        """Secondary constructor."""
        self.__init__(r"^.*код для подключения.*(\d{6})$", re.DOTALL)


class Otp:
    """An OTP code in the message."""

    _message: str
    _pattern: AbstractPattern

    def __init__(self, message: str, pattern: AbstractPattern) -> None:
        """Primary constructor."""
        self._message = message
        self._pattern = pattern

    @override
    def __str__(self) -> str | ValueError:  # type: ignore[override]
        return self._code()

    def __int__(self) -> int | ValueError:
        return int(self._code())  # type: ignore[arg-type]

    @lru_cache
    def _code(self) -> str | ValueError:
        """Matched OTP code in the message."""
        return self._pattern.matched(self._message)
