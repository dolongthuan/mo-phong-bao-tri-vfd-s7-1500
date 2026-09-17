"""Test rieng ket noi Termux:API (khong can PLC) - chay de xac nhan
TERMUX_HOST/TERMUX_USER/TERMUX_PASSWORD dung va dien thoai da cai sshd +
termux-api truoc khi dung toi main_bridge.py.

Chay: python test-harness/test_termux_notify.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python-bridge"))

from config import load_config
from notifier_termux import notify as notify_termux


def main() -> None:
    cfg = load_config()

    print("Dang goi rung + thong bao qua Termux:API...")
    result = notify_termux(
        cfg.termux_host,
        cfg.termux_port,
        cfg.termux_user,
        cfg.termux_password,
        title="[TEST] Cảnh báo VFD",
        content="Đây là thông báo thử từ test-harness/test_termux_notify.py - nếu điện thoại rung và hiện thông báo, cấu hình Termux đã đúng.",
        vibrate_ms=cfg.termux_vibrate_ms,
    )
    if result is None:
        print("  Ket qua: BO QUA (chua cau hinh TERMUX_USER/TERMUX_PASSWORD trong .env)")
    else:
        print("  Ket qua:", "OK" if result else "THAT BAI")


if __name__ == "__main__":
    main()
