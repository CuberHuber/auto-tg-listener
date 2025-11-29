# SPDX-FileCopyrightText: Copyright (C) 2025 Roman Lupashko (CuberHuber)
# SPDX-License-Identifier: MIT

"""Tests for automated Telegram message listener."""

import os
import subprocess
from unittest.mock import Mock, patch

import pytest

from main import get_env, otp, process_message_text, shortcut


class TestGetEnv:
    """Tests for get_env function."""

    def test_get_env_returns_value_when_exists(self):  # type: ignore[no-untyped-def]
        """Should return environment variable value when it exists."""
        with patch.dict(os.environ, {"TEST_KEY": "test_value"}):
            assert get_env("TEST_KEY") == "test_value"

    def test_get_env_returns_default_when_not_exists(self):  # type: ignore[no-untyped-def]
        """Should return default value when variable doesn't exist."""
        assert get_env("NONEXISTENT_KEY", "default") == "default"

    def test_get_env_raises_runtime_error_when_missing_and_no_default(self):  # type: ignore[no-untyped-def]
        """Should raise RuntimeError when variable missing and no default."""
        with pytest.raises(RuntimeError, match="Missing required environment variable"):
            get_env("NONEXISTENT_KEY")


class TestOtp:
    """Tests for OTP extraction function."""

    def test_otp_extracts_six_digit_code_from_valid_message(self):  # type: ignore[no-untyped-def]
        """Should extract 6-digit code from valid message."""
        message = "Ваш код для подключения: 123456"
        assert otp(message) == "123456"

    def test_otp_extracts_code_with_multiline_text(self):  # type: ignore[no-untyped-def]
        """Should extract code from multiline message."""
        message = "Ваш код для подключения к сервису A:\n 987654"
        assert otp(message) == "987654"

    def test_otp_raises_value_error_when_pattern_not_matched(self):  # type: ignore[no-untyped-def]
        """Should raise ValueError when message doesn't match pattern."""
        with pytest.raises(ValueError, match="Message does not match pattern"):
            otp("Random message without code")

    ##
    # @todo #1:30m/DEV Add test for edge cases with multiple codes in message.
    #  Need to verify behavior when message contains multiple 6-digit sequences.
    #  Should extract first or last occurrence?
    ##

    ##
    # @todo #1:45m/DEV Add test for code pattern variations.
    #  Test messages with different wording: "код подтверждения",
    #  "код авторизации", etc. Current regex might be too strict.
    ##


class TestShortcut:
    """Tests for macOS Shortcuts integration."""

    @patch("main.shutil.which")
    @patch("main.subprocess.run")
    def test_shortcut_executes_with_default_name(self, mock_run, mock_which):  # type: ignore[no-untyped-def]
        """Should execute shortcut with default name when not provided."""
        mock_which.return_value = "/usr/bin/shortcuts"
        with patch.dict(os.environ, {"DC_SHORTCUT_NAME": "TestShortcut"}):
            shortcut("123456")
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert args == ["/usr/bin/shortcuts", "run", "TestShortcut"]

    @patch("main.shutil.which")
    @patch("main.subprocess.run")
    def test_shortcut_passes_code_as_input(self, mock_run, mock_which):  # type: ignore[no-untyped-def]
        """Should pass OTP code as stdin to shortcut."""
        mock_which.return_value = "/usr/bin/shortcuts"
        shortcut("654321", "CustomShortcut")
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs["input"] == b"654321"

    @patch("main.shutil.which")
    @patch("main.logger")
    def test_shortcut_logs_error_when_executable_not_found(
        self, mock_logger, mock_which
    ):  # type: ignore[no-untyped-def]
        """Should log error when shortcuts executable not found."""
        mock_which.return_value = None
        shortcut("123456")
        mock_logger.error.assert_called_once_with("Shortcuts executable not found")

    @patch("main.shutil.which")
    @patch("main.subprocess.run")
    @patch("main.logger")
    def test_shortcut_handles_subprocess_timeout(
        self, mock_logger, mock_run, mock_which
    ):  # type: ignore[no-untyped-def]
        """Should handle and log timeout exception."""
        mock_which.return_value = "/usr/bin/shortcuts"
        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 5)
        shortcut("123456")
        mock_logger.exception.assert_called()

    ##
    # @todo #2:60m/DEV Add integration test for actual shortcut execution.
    #  Create mock shortcut on macOS and verify end-to-end flow.
    #  Consider using pytest-subprocess for better mocking.
    ##

    ##
    # @todo #2:45m/QA Add test for shortcut execution retry logic.
    #  Currently no retry mechanism. Should we retry on failure?
    #  Define retry policy (attempts, backoff strategy).
    ##


class TestProcessMessageText:
    """Tests for message processing pipeline."""

    @patch("main.shortcut")
    def test_process_message_extracts_and_triggers_shortcut(self, mock_shortcut):  # type: ignore[no-untyped-def]
        """Should extract OTP and trigger shortcut for valid message."""
        message = "Ваш код для подключения 111222"
        process_message_text(message)
        mock_shortcut.assert_called_once_with("111222")

    @patch("main.shortcut")
    def test_process_message_ignores_invalid_messages(self, mock_shortcut):  # type: ignore[no-untyped-def]
        """Should not trigger shortcut for invalid messages."""
        process_message_text("Random text without code")
        mock_shortcut.assert_not_called()

    ##
    # @todo #3:90m/DEV Add test for concurrent message processing.
    #  Verify thread-safety when multiple messages arrive simultaneously.
    #  Use asyncio testing patterns and check for race conditions.
    ##


class TestNewMessageHandler:
    """Tests for async message handler."""

    ##
    # @todo #4:120m/DEV Implement async handler tests.
    #  Create mock Telethon Event objects and verify handler behavior.
    #  Test error handling, logging, and edge cases (None message, etc.).
    ##

    ##
    # @todo #4:60m/DEV Add test for message filtering logic.
    #  Verify that only messages from specified chat_id are processed.
    #  Mock Telethon events with different chat IDs.
    ##


class TestCreateClientAndFilter:
    """Tests for Telegram client initialization."""

    ##
    # @todo #5:90m/DEV Add test for client creation with valid credentials.
    #  Mock TelegramClient and verify proper initialization.
    #  Test event handler registration.
    ##

    ##
    # @todo #5:60m/DEV Add test for missing environment variables handling.
    #  Verify RuntimeError raised with clear message when env vars missing.
    #  Test each required variable (API_ID, API_HASH, CHAT_ID, PHONE).
    ##


class TestMain:
    """Tests for main entry point."""

    ##
    # @todo #6:120m/DEV Implement end-to-end main() test.
    #  Mock entire Telegram client lifecycle (start, run_until_disconnected).
    #  Verify logging configuration and graceful shutdown on KeyboardInterrupt.
    ##

    ##
    # @todo #6:45m/QA Add test for signal handling (SIGTERM, SIGINT).
    #  Ensure proper cleanup when process receives termination signals.
    #  Test session file cleanup and connection closure.
    ##
