"""Ep SystemOn = TRUE/FALSE (mo phong nut ON/OFF he thong) de test main_bridge.py
ma khong can vao TIA Portal Watch Table.

Chay (bat he thong, Current_A/Temperature_C ve gia tri binh thuong 8A/50 do C):
  python test-harness/toggle_system_on.py on

Chay (tat he thong, Current_A/Temperature_C ve 0A/25 do C):
  python test-harness/toggle_system_on.py off
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python-bridge"))

from config import load_config
from plc_client import PlcClient


def main() -> None:
    trang_thai = sys.argv[1] if len(sys.argv) > 1 else "on"
    if trang_thai not in ("on", "off"):
        print("Tham so khong hop le - dung 'on' hoac 'off'.")
        return

    cfg = load_config()
    client = PlcClient(cfg.plc_ip, cfg.plc_rack, cfg.plc_slot)
    client.connect()

    gia_tri = trang_thai == "on"
    print(f"Dang ghi SystemOn = {gia_tri}...")
    client.write_system_on(cfg.db_number, gia_tri)
    print("Da ghi xong. Kiem tra Current_A/Temperature_C bang smoke_test_connection.py.")

    client.disconnect()


if __name__ == "__main__":
    main()
