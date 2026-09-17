"""Ep 1 nut SimButton_* = TRUE roi FALSE (mo phong nhan nut) de test main_bridge.py
ma khong can vao TIA Portal Watch Table.

Chay (mac dinh loi dong - Overcurrent, day Current_A len 8.5A):
  python test-harness/inject_test_fault.py

Chay loi nhiet (Overtemperature, day Temperature_C len 95 do C):
  python test-harness/inject_test_fault.py overtemperature
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python-bridge"))

from config import load_config
from plc_client import PlcClient, SIM_BUTTON_OFFSETS

_TEN_HIEN_THI = {
    "overcurrent": "SimButton_OverCurrent (loi dong - Overcurrent)",
    "overtemperature": "SimButton_Overtemperature (loi nhiet - Overtemperature)",
}


def main() -> None:
    fault_name = sys.argv[1] if len(sys.argv) > 1 else "overcurrent"
    if fault_name not in SIM_BUTTON_OFFSETS:
        print(f"Loai loi khong hop le: {fault_name}")
        print(f"Cac loai hop le: {', '.join(SIM_BUTTON_OFFSETS.keys())}")
        return

    cfg = load_config()
    client = PlcClient(cfg.plc_ip, cfg.plc_rack, cfg.plc_slot)
    client.connect()

    print(f"Dang ep {_TEN_HIEN_THI[fault_name]} = TRUE (mo phong nhan nut)...")
    client.write_sim_button(cfg.db_number, True, fault_name)
    time.sleep(0.3)
    client.write_sim_button(cfg.db_number, False, fault_name)
    print("Da tha nut ve FALSE. Kiem tra FaultActive/FaultCode/FaultEventID bang smoke_test_connection.py.")

    client.disconnect()


if __name__ == "__main__":
    main()
