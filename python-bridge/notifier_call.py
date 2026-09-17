"""Goi dien thoai that (PSTN) qua Twilio Voice API - optional, chi chay khi day du config.

Neu khong dien TWILIO_* trong .env, ham place_call() se bo qua va tra ve None
(khong lam crash chuong trinh chinh) - du an van hoat dong qua Telegram.
"""
from __future__ import annotations

import logging
from xml.sax.saxutils import escape

logger = logging.getLogger(__name__)


def place_call(
    account_sid: str,
    auth_token: str,
    from_number: str,
    to_number: str,
    message: str,
) -> bool | None:
    if not all([account_sid, auth_token, from_number, to_number]):
        logger.info("Chua cau hinh Twilio (TWILIO_*) - bo qua goi dien thoai that, chi dung Telegram.")
        return None

    try:
        from twilio.rest import Client
    except ImportError:
        logger.warning("Chua cai twilio (pip install twilio) - bo qua goi dien thoai.")
        return None

    try:
        client = Client(account_sid, auth_token)
        twiml = f'<Response><Say language="vi-VN">{escape(message)}</Say></Response>'
        client.calls.create(twiml=twiml, to=to_number, from_=from_number)
        return True
    except Exception:
        logger.exception("Goi dien qua Twilio that bai")
        return False
