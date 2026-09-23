# Telegram QR Bot

A fast, lightweight Telegram bot that generates and decodes QR codes in private chats and groups.

---

## File Structure

```text
.
├── .env.example
├── .gitignore
├── qrbot.py
├── requirements.txt
└── README.md
```

---


## Features

- **Private Chat**:
  - Send any plain text to generate a QR code.
  - Send a QR code image to decode and read the text.
- **Group Chats**:
  - Use `/qr <text>` to generate a QR code.
  - Send a QR code photo with the caption `/decode` to extract its text.

---

## System Prerequisites

1. **Python 3.10+** installed on your system.
2. **ZBar C-library** (required by `pyzbar` to decode images):
  - **Debian / Ubuntu:** 
    ```bash
    sudo apt update && sudo apt install -y libzbar0
    ```
  - **macOS (via Homebrew):** 
    ```bash
    brew install zbar
    ```
  - **Windows:** 
    Usually bundled automatically with the wheel. If you encounter a `DLL load failed` error, install the [Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-runtime).

---

## Setup & Running Guide

### 1. Linux & macOS

   ```bash
   git clone https://github.com/AnonHawk666/qrbot
   cd qrbot
   mv .env.example .env
   ````
   Open `.env` in any text editor and replace the placeholder with your actual bot token from [@BotFather](https://t.me/botfather):
   
   ```env
   BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
   ```

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 qrbot.py
   ```

---

### 2. Windows

   ```cmd
   cd C:\path\to\project
   ren .env.example .env
   ```
   Open `.env` in Notepad and insert your bot token from [@BotFather](https://t.me/botfather):
   ```cmd
   notepad .env
   ```
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python3 qrbot.py
   ```

---

## Stopping the Bot

- Press `CTRL + C` in the active terminal to stop the bot process.
- Run `deactivate` to exit the Python virtual environment.
