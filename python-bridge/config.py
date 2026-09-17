"""Nap cau hinh tu file .env (xem .env.example o thu muc goc du an)."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    plc_ip: str
    plc_rack: int
    plc_slot: int
    db_number: int
    poll_interval_ms: int

    current_threshold_a: float
    temperature_threshold_c: float

    camera_index: int

    telegram_bot_token: str
    telegram_chat_id: str

    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_number: str
    twilio_to_number: str

    termux_host: str
    termux_port: int
    termux_user: str
    termux_password: str
    termux_vibrate_ms: int
    termux_repeat_interval_sec: float


def load_config() -> Config:
    return Config(
        plc_ip=os.getenv("PLC_IP", "192.168.0.10"),
        plc_rack=int(os.getenv("PLC_RACK", "0")),
        plc_slot=int(os.getenv("PLC_SLOT", "1")),
        db_number=int(os.getenv("DB_NUMBER", "1")),
        poll_interval_ms=int(os.getenv("POLL_INTERVAL_MS", "500")),
        current_threshold_a=float(os.getenv("CURRENT_THRESHOLD_A", "15.0")),
        temperature_threshold_c=float(os.getenv("TEMPERATURE_THRESHOLD_C", "90.0")),
        camera_index=int(os.getenv("CAMERA_INDEX", "0")),
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID", ""),
        twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN", ""),
        twilio_from_number=os.getenv("TWILIO_FROM_NUMBER", ""),
        twilio_to_number=os.getenv("TWILIO_TO_NUMBER", ""),
        termux_host=os.getenv("TERMUX_HOST", "localhost"),
        termux_port=int(os.getenv("TERMUX_PORT", "8022")),
        termux_user=os.getenv("TERMUX_USER", ""),
        termux_password=os.getenv("TERMUX_PASSWORD", ""),
        termux_vibrate_ms=int(os.getenv("TERMUX_VIBRATE_MS", "1000")),
        termux_repeat_interval_sec=float(os.getenv("TERMUX_REPEAT_INTERVAL_SEC", "300")),
    )
