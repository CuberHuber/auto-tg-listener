<div align="center">

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Issues - daytona](https://img.shields.io/github/issues/CuberHuber/auto-tg-listener)](https://github.com/CuberHuber/auto-tg-listener/issues)
![GitHub Release](https://img.shields.io/github/v/release/CuberHuber/auto-tg-listener)

</div>

&nbsp;

<div align="center">
  <h1>Auto Telegram Listener</h1>
  
  <!-- One-liner description -->
  <b>🤖 Automated Telegram message listener with regex filtering and macOS Shortcuts integration</b>

  <!-- Quick links -->
  [Features](#features) • [Installation](#installation) • [Quick Start](#quick-start)
</div>

---

## Installation

### From source with uv (Recommended for Development)

> [uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver. It's the recommended way to set up the project for development.

#### Step 1: Install uv
```bash
brew install uv
```

#### Step 2: Clone the Repository

```bash
git clone https://github.com/CuberHuber/auto-tg-listener.git
cd auto-tg-listener
```

#### Step 3: Create Virtual Environment
```bash
uv sync
```

---

## Features
- Seamless integration with Apple Shortcuts
- 2FA Code Extraction
- Powerful regex pattern matching for precise message filtering

---

## Quick Start

### 1. Get Telegram API Credentials

1. Зайти на сайт https://my.telegram.org/ через мобильное устройство (_рекомендуется_)
2. Залогинится и перейти по **API development tools**
3. Создать новое приложение
```
App title: Demo Message Listener
Short name: demomsglistener
URL: [оставить пустым]
Platform: Desktop
Description: [оставить пустым]
```
4. Сохранить `api_id` и `api_hash`

### 2. Get Telegram Chat ID

1. Найти бота в Telegram `@RawDataBot`.
2. Выбрать в боте личные сообщения или бота
3. Бот вернет `chat_id`

### 3. Configure

1. Перейти в репозиторий проекта `cd auto-tg-listener`
2. Скопировать шаблон .env файла `cp .env.sample .env`
3. Заполнить `.env` файл
```dotenv
DC_TELEGRAM_API_ID=[api_id]
DC_TELEGRAM_API_HASH=[api_hash]
DC_TELEGRAM_PHONE=[your phone]

DC_CHAT_ID=[chat_id]
DC_SHORTCUT_NAME="Notify Telegram Message"
```

### 4. Create a Shortcut

1. Запустить приложение `Shortcuts`.

#### Step 1: Create new shortcut
1. В приложении `Shortcuts` нажмите кнопку `+` в верхней панели инструментов 
2. Откроется пустой редактор shortcut с названием "**Untitled Shortcut**"

#### Step 2: Change the name of the shortcut
1. Кликните на "**Untitled Shortcut**" или "**Shortcut Name**" вверху окна
2. Введите имя: `Notify Telegram Message`
3. Нажмите _Enter_

#### Step 3: Shortcut Reveive setting
1. В правой панели найдите иконку ⓘ (Details) и кликните на неё 
2. Включите переключатель "**Use as Quick Action**" (для запуска из других приложений)
3. В разделе "**Receives**" выберите "**Text**" из выпадающего списка 
4. Перейти в блок Receive и выбрать `Text` как **Shortcut imput**
5. Добавить Action `Copy to Clipboard` и `Show notification` (по желанию)

#### Step 4: Fill in the logic
<img width="611" height="244" alt="Screenshot 2025-10-06 at 11 39 43" src="https://github.com/user-attachments/assets/41932864-aad1-4a1d-88a0-4f4490b81f84" />


### 4. Run
```bash
uv run python3 main.py
```


