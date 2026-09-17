"""Ghi log su kien loi vao data-logs/fault_events.csv."""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

_DATA_LOGS_DIR = Path(__file__).parent.parent / "data-logs"
_CSV_PATH = _DATA_LOGS_DIR / "fault_events.csv"

_CSV_HEADER = [
    "timestamp",
    "fault_event_id",
    "fault_code",
    "ten_vi",
    "current_a",
    "temperature_c",
    "telegram_text_sent",
    "telegram_photo_sent",
    "phone_call_sent",
    "termux_notified",
    "manual_verified",
]


def append_event(
    fault_event_id: int,
    fault_code: int,
    ten_vi: str,
    current_a: float,
    temperature_c: float,
    telegram_text_sent: bool,
    telegram_photo_sent: bool,
    phone_call_sent: bool | None,
    termux_notified: bool | None,
    manual_verified: bool,
) -> None:
    _DATA_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    is_new_file = not _CSV_PATH.exists()
    with open(_CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(_CSV_HEADER)
        writer.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                fault_event_id,
                fault_code,
                ten_vi,
                current_a,
                temperature_c,
                telegram_text_sent,
                telegram_photo_sent,
                phone_call_sent,
                termux_notified,
                manual_verified,
            ]
        )
