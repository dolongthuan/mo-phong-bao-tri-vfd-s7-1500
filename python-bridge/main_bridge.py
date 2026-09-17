"""Script chinh: doc DB_VFD_Fault tren S7-1500, khi Current_A/Temperature_C thuc
su vuot nguong (CURRENT_THRESHOLD_A/TEMPERATURE_THRESHOLD_C) thi tra cuu manual +
gui canh bao qua Telegram (text + anh) va goi dien Twilio (neu co cau hinh), roi
lap lai rung + thong bao + doc canh bao tren dien thoai qua Termux:API moi
TERMUX_REPEAT_INTERVAL_SEC cho toi khi Reset hoac tat he thong (Current_A/
Temperature_C tut xuong duoi nguong).

Chay: python python-bridge/main_bridge.py
Dung: Ctrl+C
"""
from __future__ import annotations

import logging
import time

from camera_capture import capture_photo
from config import load_config
from event_log import append_event
from fault_lookup import get_fault_info
from notifier_call import place_call
from notifier_telegram import send_photo, send_text
from notifier_termux import notify as notify_termux
from plc_client import FaultState, PlcClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

RECONNECT_DELAY_SEC = 5


def build_message(state: FaultState) -> str:
    info = get_fault_info(state.fault_code)

    if info is None:
        return f"⚠️ *CẢNH BÁO VFD: Lỗi không xác định (FaultCode={state.fault_code})*"

    if state.fault_code == 1:
        gia_tri = f"Dòng điện: {state.current_a:.1f} A"
    elif state.fault_code == 2:
        gia_tri = f"Nhiệt độ: {state.temperature_c:.1f} độ C"
    else:
        gia_tri = f"Dòng điện: {state.current_a:.1f} A - Nhiệt độ: {state.temperature_c:.1f} độ C"

    khuyen_nghi = ", ".join(info.khuyen_nghi_ngan)
    verified_note = "" if info.manual_verified else " (chưa xác nhận)"
    return (
        f"⚠️ *CẢNH BÁO: {info.ten_vi} — {gia_tri}*\n"
        f"Khuyến nghị: {khuyen_nghi}\n"
        f"Tham khảo: {info.manual_document} - {info.manual_page_hint}{verified_note}"
    )


def build_voice_text(message: str) -> str:
    return message.replace("*", "").replace("⚠️", "").replace("—", "-").replace("✅", "")


def build_reset_message() -> str:
    return "✅ *Hệ thống đã Reset.* Trạng thái biến tần bình thường."


def send_termux_alert(state: FaultState, cfg) -> bool | None:
    info = get_fault_info(state.fault_code)
    voice_text = build_voice_text(build_message(state))
    return notify_termux(
        cfg.termux_host,
        cfg.termux_port,
        cfg.termux_user,
        cfg.termux_password,
        title=f"⚠ Cảnh báo VFD: {info.ten_vi if info else 'Lỗi không xác định'}",
        content=voice_text,
        vibrate_ms=cfg.termux_vibrate_ms,
    )


def handle_threshold_exceeded(state: FaultState, cfg) -> None:
    logger.info("Vuot nguong: FaultCode=%s, Current_A=%.1f, Temperature_C=%.1f", state.fault_code, state.current_a, state.temperature_c)
    info = get_fault_info(state.fault_code)
    message = build_message(state)
    voice_text = build_voice_text(message)

    text_ok = send_text(cfg.telegram_bot_token, cfg.telegram_chat_id, message)

    photo_bytes = capture_photo(cfg.camera_index)
    photo_ok = False
    if photo_bytes is not None:
        photo_ok = send_photo(cfg.telegram_bot_token, cfg.telegram_chat_id, photo_bytes, caption="Ảnh chụp hiện trường lúc cảnh báo")

    call_ok = place_call(
        cfg.twilio_account_sid,
        cfg.twilio_auth_token,
        cfg.twilio_from_number,
        cfg.twilio_to_number,
        voice_text,
    )
    termux_ok = send_termux_alert(state, cfg)

    append_event(
        fault_event_id=state.fault_event_id,
        fault_code=state.fault_code,
        ten_vi=info.ten_vi if info else "không xác định",
        current_a=state.current_a,
        temperature_c=state.temperature_c,
        telegram_text_sent=text_ok,
        telegram_photo_sent=photo_ok,
        phone_call_sent=call_ok,
        termux_notified=termux_ok,
        manual_verified=info.manual_verified if info else False,
    )


def run() -> None:
    cfg = load_config()
    client = PlcClient(cfg.plc_ip, cfg.plc_rack, cfg.plc_slot)
    poll_interval_sec = cfg.poll_interval_ms / 1000
    current_alerted = False
    temperature_alerted = False
    last_termux_repeat = 0.0

    logger.info("Bat dau python-bridge - PLC %s (rack=%s, slot=%s), DB%s", cfg.plc_ip, cfg.plc_rack, cfg.plc_slot, cfg.db_number)

    while True:
        try:
            if not client.is_connected():
                logger.info("Dang ket noi PLC...")
                client.connect()
                logger.info("Da ket noi PLC.")

            state = client.read_fault_state(cfg.db_number)
            was_alerted = current_alerted or temperature_alerted

            current_over = state.current_a > cfg.current_threshold_a
            if current_over and not current_alerted:
                handle_threshold_exceeded(state, cfg)
                last_termux_repeat = time.monotonic()
            current_alerted = current_over

            temperature_over = state.temperature_c > cfg.temperature_threshold_c
            if temperature_over and not temperature_alerted:
                handle_threshold_exceeded(state, cfg)
                last_termux_repeat = time.monotonic()
            temperature_alerted = temperature_over

            is_alerted = current_alerted or temperature_alerted
            if is_alerted and (time.monotonic() - last_termux_repeat) >= cfg.termux_repeat_interval_sec:
                logger.info("Lap lai canh bao Termux (van con vuot nguong): Current_A=%.1f, Temperature_C=%.1f", state.current_a, state.temperature_c)
                send_termux_alert(state, cfg)
                last_termux_repeat = time.monotonic()

            if was_alerted and not is_alerted:
                logger.info("Da het canh bao (Reset/tat he thong) - gui thong bao Telegram, ngung lap lai canh bao dien thoai")
                send_text(cfg.telegram_bot_token, cfg.telegram_chat_id, build_reset_message())

            time.sleep(poll_interval_sec)

        except KeyboardInterrupt:
            logger.info("Dung theo yeu cau (Ctrl+C).")
            break
        except Exception:
            logger.exception("Loi giao tiep PLC - thu ket noi lai sau %s giay", RECONNECT_DELAY_SEC)
            client.disconnect()
            time.sleep(RECONNECT_DELAY_SEC)

    client.disconnect()


if __name__ == "__main__":
    run()
