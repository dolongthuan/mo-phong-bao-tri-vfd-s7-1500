"""Test rieng ket noi Telegram (khong can PLC) - chay de xac nhan BOT_TOKEN/CHAT_ID dung
truoc khi dung toi main_bridge.py.

Chay: python test-harness/test_telegram_notify.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python-bridge"))

from config import load_config
from notifier_call import place_call
from notifier_telegram import send_text, send_voice_alert

TEST_MESSAGE = "[TEST] Đây là tin nhắn thử từ test-harness/test_telegram_notify.py - nếu bạn nhận được, cấu hình Telegram đã đúng."


def main() -> None:
    cfg = load_config()

    print("Dang gui tin nhan text...")
    print("  Ket qua:", "OK" if send_text(cfg.telegram_bot_token, cfg.telegram_chat_id, TEST_MESSAGE) else "THAT BAI")

    print("Dang gui voice alert...")
    print("  Ket qua:", "OK" if send_voice_alert(cfg.telegram_bot_token, cfg.telegram_chat_id, TEST_MESSAGE) else "THAT BAI (co the chua cai gTTS hoac khong co internet)")

    print("Dang thu goi dien Twilio (neu co cau hinh)...")
    call_result = place_call(
        cfg.twilio_account_sid,
        cfg.twilio_auth_token,
        cfg.twilio_from_number,
        cfg.twilio_to_number,
        TEST_MESSAGE,
    )
    if call_result is None:
        print("  Ket qua: BO QUA (chua cau hinh TWILIO_* trong .env)")
    else:
        print("  Ket qua:", "OK" if call_result else "THAT BAI")


if __name__ == "__main__":
    main()
