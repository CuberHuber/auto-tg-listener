# Makefile for Auto Telegram Listener

# Variables
PROJECT_NAME := com.user.tglistener
RUNTIME_DIR := $(PWD)/run
# PLIST_DIR := $(HOME)/Library/LaunchAgents
PLIST_DIR := $(RUNTIME_DIR)
PLIST_FILE := $(PLIST_DIR)/$(PROJECT_NAME).plist
LOG_FILE := $(RUNTIME_DIR)/app.log
ERROR_LOG_FILE := $(RUNTIME_DIR)/error.log
TEMPLATE_FILE := $(PWD)/template/service.plist.template
TEMPLATE_ENV := $(PWD)/template/.env.sample
PYTHON_BIN := $(shell which uv)
USER_ID := $(shell id -u)

.PHONY: all help start-locally autostart lint stop env logs clean test

all: help

help: ## Show this help message
	@echo "Usage: make [command]\n\nCommands:\n  install    - Install uv, dependencies, and create .env\n  run        - Run the script manually\n  autostart  - Install as a background service\n  stop       - Stop service\n  logs       - Tail logs\n  clean      - Cleanup"

start-locally: env
	@if [ -z "$(PYTHON_BIN)" ]; then echo "❌ Error: uv not found. Run 'make install' first."; exit 1; fi
	@if [ ! -f "$(TEMPLATE_FILE)" ]; then echo "❌ Error: Template file '$(TEMPLATE_FILE)' not found."; exit 1; fi

	@echo "Launch locally..."
	@uv run python main.py

autostart: env ## Generate plist from template and load into launchd
	@if [ -z "$(PYTHON_BIN)" ]; then echo "❌ Error: uv not found. Run 'make install' first."; exit 1; fi
	@if [ ! -f "$(TEMPLATE_FILE)" ]; then echo "❌ Error: Template file '$(TEMPLATE_FILE)' not found."; exit 1; fi

	@echo "Generating LaunchAgent plist..."

	@perl -pe 's|{{PWD}}|$(PWD)|g; s|{{UV_PATH}}|$(PYTHON_BIN)|g; s|{{DATA_DIR}}|$(RUNTIME_DIR)|g' "$(TEMPLATE_FILE)" > "$(PLIST_FILE)"

	@echo "Loading service $(PROJECT_NAME)..."
	@# Выгружаем старый сервис, если он был (игнорируем ошибки)
	-launchctl bootout gui/$(USER_ID)/$(PROJECT_NAME) 2>/dev/null
	@# Загружаем новый
	launchctl bootstrap gui/$(USER_ID) "$(PLIST_FILE)"

	@echo "✅ Service installed and started! Logs are at $(PWD)/app.log"

lint: ## Run code quality tools
	@$(PYTHON_BIN) run pre-commit run --all-files

test: ## Run tests
	@$(PYTHON_BIN) run pytest -q

stop: ## Stop and remove the background service
	@echo "Stopping service..."
	-launchctl bootout gui/$(USER_ID)/$(PROJECT_NAME) 2>/dev/null
	@rm -f $(PLIST_FILE)
	@echo "✅ Service stopped and removed."

env:
	@if [ -f ".env" ]; then echo "⚠️  .env file exists."; else cp -n $(TEMPLATE_ENV) .env; echo "ℹ️  .env created."; fi
	@mkdir -p $(PLIST_DIR);

logs: ## Tail the application logs
	@tail -f $(RUNTIME_DIR)/app.log $(RUNTIME_DIR)/error.log

clean:
	@echo "Cleaning all env and temporary files..."
	@rm -rf $(RUNTIME_DIR)

	@echo "✅ Garbage removed."