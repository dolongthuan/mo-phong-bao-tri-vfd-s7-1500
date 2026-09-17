"""Test ket noi PLC co ban - chay TRUOC main_bridge.py de xac nhan doc DB OK.

Chay: python test-harness/smoke_test_connection.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python-bridge"))

from config import load_config
from plc_client import PlcClient


def main() -> None:
    cfg = load_config()
    print(f"Ket noi toi PLC {cfg.plc_ip} (rack={cfg.plc_rack}, slot={cfg.plc_slot})...")

    client = PlcClient(cfg.plc_ip, cfg.plc_rack, cfg.plc_slot)
    client.connect()

    if not client.is_connected():
        print("KET NOI THAT BAI - kiem tra lai IP/rack/slot, PUT/GET, PLCSIM Advanced instance.")
        return

    print("Ket noi OK. Dang doc DB_VFD_Fault...")
    state = client.read_fault_state(cfg.db_number)
    print(f"  SimButton_OverCurrent     = {state.sim_button}")
    print(f"  FaultActive               = {state.fault_active}")
    print(f"  ResetFault                = {state.reset_fault}")
    print(f"  SimButton_Overtemperature = {state.sim_button_overtemperature}")
    print(f"  FaultCode                 = {state.fault_code}")
    print(f"  FaultEventID              = {state.fault_event_id}")
    print(f"  SystemOn                  = {state.system_on}")
    print(f"  Current_A                 = {state.current_a:.1f} A")
    print(f"  Temperature_C             = {state.temperature_c:.1f} do C")

    client.disconnect()
    print("Da ngat ket noi. Smoke test hoan tat.")


if __name__ == "__main__":
    main()
