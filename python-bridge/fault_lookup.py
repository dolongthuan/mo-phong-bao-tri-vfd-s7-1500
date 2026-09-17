"""Tra cuu thong tin loi bien tan tu bang JSON tu soan (khong doi chieu voi manual that).

CANH BAO: manual_reference.page_hint trong fault_codes_v20.json la chua xac nhan.
Truoc khi dung so lieu nay cho bao cao/do an chinh thuc, phai doi chieu lai voi
ban PDF "SINAMICS V20 Operating Instructions" that va cap nhat "verified": true.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

_DATA_PATH = Path(__file__).parent / "data" / "fault_codes_v20.json"


@dataclass(frozen=True)
class FaultInfo:
    fault_code: int
    code_tham_khao: str
    ten_vi: str
    ten_en: str
    mo_ta: str
    nguyen_nhan_thuong_gap: list[str]
    khuyen_nghi_xu_ly: list[str]
    khuyen_nghi_ngan: list[str]
    manual_document: str
    manual_section_hint: str
    manual_page_hint: str
    manual_verified: bool


def _load_table() -> dict:
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_fault_info(fault_code: int) -> Optional[FaultInfo]:
    table = _load_table()
    entry = table.get(str(fault_code))
    if entry is None:
        return None
    ref = entry["manual_reference"]
    return FaultInfo(
        fault_code=fault_code,
        code_tham_khao=entry["code_tham_khao"],
        ten_vi=entry["ten_vi"],
        ten_en=entry["ten_en"],
        mo_ta=entry["mo_ta"],
        nguyen_nhan_thuong_gap=entry["nguyen_nhan_thuong_gap"],
        khuyen_nghi_xu_ly=entry["khuyen_nghi_xu_ly"],
        khuyen_nghi_ngan=entry["khuyen_nghi_ngan"],
        manual_document=ref["document"],
        manual_section_hint=ref["section_hint"],
        manual_page_hint=ref["page_hint"],
        manual_verified=ref["verified"],
    )
