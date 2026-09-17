---
title: Worksheet thiet ke DB_VFD_Fault
type: docs-thiet-ke
project: mo-phong-bao-tri-vfd-s7-1500
---

# Worksheet thiet ke DB_VFD_Fault

## Bang bien (dung de doi chieu voi view "Extended" that trong TIA Portal)

| Ten bien | Kieu | Offset du kien | Y nghia | Ai ghi | Ai doc |
|---|---|---|---|---|---|
| SimButton_OverCurrent | Bool | 0.0 | Nut nhan mo phong loi dong (ep TRUE qua Watch Table hoac test-harness/inject_test_fault.py) | Nguoi van hanh / test-harness | FB_SimulateVFDFault |
| FaultActive | Bool | 0.1 | TRUE = dang co loi (latch) | FB_SimulateVFDFault | python-bridge |
| ResetFault | Bool | 0.2 | Ghi TRUE de xoa loi, FB tu dua ve FALSE | Watch Table / python-bridge | FB_SimulateVFDFault |
| SimButton_Overtemperature | Bool | 0.3 | Nut nhan mo phong loi nhiet (ep TRUE qua Watch Table hoac test-harness/inject_test_fault.py) | Nguoi van hanh / test-harness | FB_SimulateVFDFault |
| CurrentFaultLatched | Bool | 0.4 | Noi bo FB: TRUE khi loi dang active la loi dong - dieu khien Current_A | FB_SimulateVFDFault | FB_SimulateVFDFault |
| TemperatureFaultLatched | Bool | 0.5 | Noi bo FB: TRUE khi loi dang active la loi nhiet - dieu khien Temperature_C | FB_SimulateVFDFault | FB_SimulateVFDFault |
| FaultCode | Int | 2 | 0 = khong loi, 1..2 = xem bang ma loi ben duoi | FB_SimulateVFDFault | python-bridge |
| FaultEventID | Int | 4 | Tang dan moi lan co loi MOI (bat ky loai nao) - chi de tham khao/ghi log, python-bridge KHONG con dung bien nay de quyet dinh gui canh bao (xem CURRENT_THRESHOLD_A/TEMPERATURE_THRESHOLD_C) | FB_SimulateVFDFault | python-bridge (chi ghi log) |
| SystemOn | Bool | 6.0 | Nut ON/OFF he thong - TRUE = dang chay | Nguoi van hanh / test-harness/toggle_system_on.py | FB_SimulateVFDFault |
| Current_A | Real | 8 | Dong dien mo phong (A) - 0.0 khi tat, 8.0 binh thuong, TANG LIEN TUC KHONG GIOI HAN khi loi dong dang active (0.5/buoc moi 500ms) cho toi khi ResetFault | FB_SimulateVFDFault | python-bridge |
| Temperature_C | Real | 12 | Nhiet do mo phong (do C) - 0.0 khi tat, 50.0 binh thuong, TANG LIEN TUC KHONG GIOI HAN khi loi nhiet dang active (1.5/buoc moi 500ms) cho toi khi ResetFault | FB_SimulateVFDFault | python-bridge |

**Luu y offset:** cac gia tri Offset o tren la du kien theo quy tac dong goi bien
S7 tieu chuan (Bool don gian dan vao chung 1 byte, Int can chan byte). Sau khi
"Generate blocks from source" trong TIA Portal, BAT BUOC mo DB_VFD_Fault > view
"Extended" de xac nhan lai offset that. Neu lech, sua cac hang so
`OFFSET_*` trong `python-bridge/plc_client.py`.

**DB phai la Non-optimized ("Standard - compatible"):** tick tat "Optimized block
access" trong Properties > Attributes cua DB, neu khong python-snap7 doc offset se
sai gia tri ma khong bao loi.

## Ma loi (FaultCode) va tra cuu manual

Chi con 2 nut loi doc lap: **loi dong** (day Current_A len) va **loi nhiet**
(day Temperature_C len) - da bo 4 nut con lai (qua ap, thieu ap, qua tai I2t,
nhiet do chip cao) theo yeu cau don gian hoa. Bang tra cuu chi tiet nam o
`python-bridge/data/fault_codes_v20.json`. Da doi chieu voi ban PDF that
"SINAMICS V20 Inverter - Getting Started" (A5E03728127, 07/2012), Chuong 6
"Fault and warning codes", trang 59 - ca 2 ma loi ben duoi da danh dau
`verified: true`:

| FaultCode | Ma tren manual | Ten | Ghi chu |
|---|---|---|---|
| 0 | - | Khong loi | Trang thai binh thuong |
| 1 | F1 | Qua dong (Overcurrent) - loi dong | Trang 59 |
| 2 | F4 | Qua nhiet thiet bi (Overtemperature) - loi nhiet | Trang 59 |

## Kien truc luong du lieu

```
[Nut nhan / Watch Table]
        |
        v
SimButton_OverCurrent hoac SimButton_Overtemperature (Bool, DB_VFD_Fault)
        |
        v  (R_TRIG rieng cho tung nut trong FB_SimulateVFDFault, chay trong OB1 -
        v   CHI co tac dung neu SystemOn = TRUE, bo qua neu may dang tat)
FaultActive=TRUE, FaultCode=1 hoac 2, CurrentFaultLatched/TemperatureFaultLatched=TRUE
        |
        v  Current_A hoac Temperature_C TANG LIEN TUC KHONG GIOI HAN (0.5A/1.5 do C
        v  moi 500ms) cho toi khi ResetFault - xem scl/FB_SimulateVFDFault.scl
        |
        v  (python-snap7 poll moi POLL_INTERVAL_MS, so sanh voi CURRENT_THRESHOLD_A/
        v   TEMPERATURE_THRESHOLD_C moi vong poll - KHONG dua vao FaultEventID nua)
python-bridge/main_bridge.py: Current_A/Temperature_C > nguong lan dau (chua bao)?
        |
        v  (chi bao 1 lan khi vua vuot nguong, khong bao lap lai khi van dang vuot -
        v   bao lai neu tut xuong duoi nguong roi vuot len lan nua)
        +--> fault_lookup.py (tra cuu fault_codes_v20.json)
        +--> notifier_telegram.py (Telegram Bot API: sendMessage + sendAudio TTS)
        +--> notifier_call.py (Twilio Voice, optional - goi dien khi vua vuot nguong)
        +--> event_log.py (ghi data-logs/fault_events.csv, kem Current_A/Temperature_C)
```

Current_A/Temperature_C duoc FB_SimulateVFDFault tinh lai moi chu ky quet dua
tren SystemOn + CurrentFaultLatched/TemperatureFaultLatched hien tai (2 bit noi
bo, duoc set/clear boi R_TRIG cua tung nut loi va boi ResetFault) - xem bang
nguong o dau file scl/FB_SimulateVFDFault.scl.

## Doc them

- `PROJECT_CONTEXT.md` - toan bo cau hinh du an
- `README.md` - huong dan cai dat + chay
