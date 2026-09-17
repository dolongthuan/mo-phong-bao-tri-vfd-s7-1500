"""Ket noi va doc/ghi DB_VFD_Fault tren CPU S7-1500 (that hoac PLCSIM Advanced) qua python-snap7.

QUAN TRONG: DB_VFD_Fault phai duoc tao voi "Optimized block access" = OFF (Standard -
compatible), neu khong offset doc duoc se sai gia tri ma khong bao loi gi ca.
"""
from __future__ import annotations

from dataclasses import dataclass

import snap7
from snap7.util import get_bool, get_int, get_real, set_bool

# Offset du kien theo thu tu khai bao trong scl/DB_VFD_Fault.scl.
# PHAI doi chieu lai voi view "Extended" that trong TIA Portal sau khi Generate
# blocks from source - neu lech, sua truc tiep cac hang so ben duoi.
OFFSET_SIM_BUTTON = (0, 0)   # byte 0, bit 0 - nut loi dong (Overcurrent)
OFFSET_FAULT_ACTIVE = (0, 1)  # byte 0, bit 1
OFFSET_RESET_FAULT = (0, 2)   # byte 0, bit 2
OFFSET_SIM_BUTTON_OVERTEMPERATURE = (0, 3)  # byte 0, bit 3 - nut loi nhiet (Overtemperature)
OFFSET_FAULT_CODE = 2          # byte 2 (Int)
OFFSET_FAULT_EVENT_ID = 4      # byte 4 (Int)
OFFSET_SYSTEM_ON = (6, 0)      # byte 6, bit 0 - nut ON/OFF he thong
OFFSET_CURRENT_A = 8           # byte 8 (Real) - dong dien mo phong
OFFSET_TEMPERATURE_C = 12      # byte 12 (Real) - nhiet do mo phong
READ_SIZE = 16                 # tong so byte can doc (0..15)

# Ten nut mo phong (dung cho test-harness/inject_test_fault.py) -> offset ghi tuong ung
SIM_BUTTON_OFFSETS = {
    "overcurrent": OFFSET_SIM_BUTTON,
    "overtemperature": OFFSET_SIM_BUTTON_OVERTEMPERATURE,
}


@dataclass(frozen=True)
class FaultState:
    sim_button: bool
    fault_active: bool
    reset_fault: bool
    sim_button_overtemperature: bool
    fault_code: int
    fault_event_id: int
    system_on: bool
    current_a: float
    temperature_c: float


class PlcClient:
    def __init__(self, ip: str, rack: int, slot: int):
        self._ip = ip
        self._rack = rack
        self._slot = slot
        self._client = snap7.client.Client()

    def connect(self) -> None:
        self._client.connect(self._ip, self._rack, self._slot)

    def is_connected(self) -> bool:
        try:
            return bool(self._client.get_connected())
        except Exception:
            return False

    def disconnect(self) -> None:
        if self.is_connected():
            self._client.disconnect()

    def read_fault_state(self, db_number: int) -> FaultState:
        data = self._client.db_read(db_number, 0, READ_SIZE)
        return FaultState(
            sim_button=get_bool(data, *OFFSET_SIM_BUTTON),
            fault_active=get_bool(data, *OFFSET_FAULT_ACTIVE),
            reset_fault=get_bool(data, *OFFSET_RESET_FAULT),
            sim_button_overtemperature=get_bool(data, *OFFSET_SIM_BUTTON_OVERTEMPERATURE),
            fault_code=get_int(data, OFFSET_FAULT_CODE),
            fault_event_id=get_int(data, OFFSET_FAULT_EVENT_ID),
            system_on=get_bool(data, *OFFSET_SYSTEM_ON),
            current_a=get_real(data, OFFSET_CURRENT_A),
            temperature_c=get_real(data, OFFSET_TEMPERATURE_C),
        )

    def write_reset_fault(self, db_number: int, value: bool) -> None:
        self._write_bit(db_number, OFFSET_RESET_FAULT, value)

    def write_sim_button(self, db_number: int, value: bool, fault_name: str = "overcurrent") -> None:
        self._write_bit(db_number, SIM_BUTTON_OFFSETS[fault_name], value)

    def write_system_on(self, db_number: int, value: bool) -> None:
        self._write_bit(db_number, OFFSET_SYSTEM_ON, value)

    def _write_bit(self, db_number: int, offset: tuple[int, int], value: bool) -> None:
        byte_index, bit_index = offset
        data = self._client.db_read(db_number, byte_index, 1)
        set_bool(data, 0, bit_index, value)
        self._client.db_write(db_number, byte_index, data)
