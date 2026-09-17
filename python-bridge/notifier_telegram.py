"""Gui canh bao qua Telegram Bot API: tin nhan text + voice note (text-to-speech).

Telegram Bot API khong the tu goi dien thoai that toi mot so dien thoai - phan
"cuoc goi" that (PSTN) nam o notifier_call.py (qua Twilio, optional).
"""
from __future__ import annotations

import logging
import os
import tempfile

import requests

logger = logging.getLogger(__name__)

_API_URL = "https://api.telegram.org/bot{token}/{method}"
_TIMEOUT_TEXT = 10
_TIMEOUT_AUDIO = 30


def send_text(bot_token: str, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
    if not bot_token or not chat_id:
        logger.warning("Chua cau hinh TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID - bo qua gui tin nhan.")
        return False
    try:
        resp = requests.post(
            _API_URL.format(token=bot_token, method="sendMessage"),
            data={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            timeout=_TIMEOUT_TEXT,
        )
        resp.raise_for_status()
        return True
    except requests.RequestException:
        logger.exception("Gui tin nhan Telegram that bai")
        return False


def send_photo(bot_token: str, chat_id: str, photo_bytes: bytes, caption: str = "") -> bool:
    if not bot_token or not chat_id:
        logger.warning("Chua cau hinh TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID - bo qua gui anh.")
        return False
    try:
        resp = requests.post(
            _API_URL.format(token=bot_token, method="sendPhoto"),
            data={"chat_id": chat_id, "caption": caption},
            files={"photo": ("canh-bao-loi.jpg", photo_bytes, "image/jpeg")},
            timeout=_TIMEOUT_AUDIO,
        )
        resp.raise_for_status()
        return True
    except requests.RequestException:
        logger.exception("Gui anh Telegram that bai")
        return False


def send_voice_alert(bot_token: str, chat_id: str, text: str) -> bool:
    if not bot_token or not chat_id:
        logger.warning("Chua cau hinh TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID - bo qua voice alert.")
        return False
    try:
        from gtts import gTTS
    except ImportError:
        logger.warning("Chua cai gTTS (pip install gTTS) - bo qua voice alert.")
        return False

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            mp3_path = os.path.join(tmp_dir, "canh-bao-loi.mp3")
            gTTS(text=text, lang="vi").save(mp3_path)
            with open(mp3_path, "rb") as audio_file:
                resp = requests.post(
                    _API_URL.format(token=bot_token, method="sendAudio"),
                    data={
                        "chat_id": chat_id,
                        "title": "Canh bao loi VFD",
                        "performer": "PLC S7-1500 - python-bridge",
                    },
                    files={"audio": ("canh-bao-loi.mp3", audio_file, "audio/mpeg")},
                    timeout=_TIMEOUT_AUDIO,
                )
            resp.raise_for_status()
        return True
    except Exception:
        logger.exception("Gui voice alert Telegram that bai (co the do khong co internet cho gTTS)")
        return False
