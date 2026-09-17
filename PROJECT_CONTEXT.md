# Bối cảnh dự án

## Tên dự án

Mô phỏng giám sát và cảnh báo lỗi VFD bằng PLC S7-1500

## Mục tiêu của phiên bản hiện tại

Kiểm chứng chuỗi chức năng từ tạo dữ liệu trên PLC ảo, đọc dữ liệu bằng Python, phát hiện vượt ngưỡng, ghi sự kiện và gửi cảnh báo đến điện thoại.

## Phạm vi đã triển khai

- TIA Portal V20 và PLCSIM Advanced với CPU S7-1500 ảo.
- Hai lỗi độc lập: F1 quá dòng và F4 quá nhiệt.
- Dòng điện bình thường 8 A; nhiệt độ bình thường 50 °C.
- Ngưỡng thử nghiệm: 15 A và 90 °C.
- Python Bridge đọc DB 16 byte bằng `python-snap7`.
- Telegram gửi tin nhắn và ảnh webcam.
- Termux:API rung, hiển thị thông báo và đọc cảnh báo.
- Twilio là chức năng tùy chọn.
- CSV lưu sự kiện cảnh báo.

## Ngoài phạm vi hiện tại

- Chưa kết nối biến tần SINAMICS V20 và động cơ thật.
- Chưa đọc thanh ghi Modbus trực tiếp từ biến tần.
- Chưa tích hợp V-Box thật.
- Chưa có dữ liệu dài hạn hoặc mô hình dự báo tuổi thọ hữu ích còn lại.
- Chưa đánh giá độ chính xác dự báo, cảnh báo giả hoặc cảnh báo bỏ sót ngoài hiện trường.

## Giao diện dữ liệu PLC

| Offset | Biến | Kiểu | Ý nghĩa |
|---:|---|---|---|
| 0.0 | `SimButton_OverCurrent` | Bool | Kích hoạt lỗi F1 |
| 0.1 | `FaultActive` | Bool | Lỗi đang được chốt |
| 0.2 | `ResetFault` | Bool | Xóa lỗi |
| 0.3 | `SimButton_Overtemperature` | Bool | Kích hoạt lỗi F4 |
| 2 | `FaultCode` | Int | 0 không lỗi, 1 F1, 2 F4 |
| 4 | `FaultEventID` | Int | Số thứ tự sự kiện |
| 6.0 | `SystemOn` | Bool | Bật hoặc tắt hệ thống |
| 8 | `Current_A` | Real | Dòng điện mô phỏng |
| 12 | `Temperature_C` | Real | Nhiệt độ mô phỏng |

## Trạng thái

- [x] Mã SCL cho DB và FB mô phỏng.
- [x] Python Bridge và các kênh cảnh báo.
- [x] Test harness cho kết nối, bật hệ thống và tạo hai lỗi.
- [x] Báo cáo Đồ án 1 hiện có.
- [x] Gói dự án đã loại thông tin nhạy cảm để gửi giảng viên xem trước.
- [ ] Giảng viên xác nhận phạm vi và sơ đồ chức năng.
- [ ] Kiểm tra lại toàn bộ pipeline trên đúng DB Number của project TIA hiện tại.
- [ ] Ghi lại kết quả kiểm thử có RunID, TestCaseID và phiên bản phần mềm.

## Quy tắc cập nhật

- Code PLC đặt trong `scl/`.
- Code chạy chính đặt trong `python-bridge/`.
- Script kiểm tra đặt trong `test-harness/`.
- Tài liệu thiết kế đặt trong `docs-thiet-ke/` hoặc `docs/`.
- Không commit `.env`, log chạy thật, `venv` hoặc cache Python.
- Mỗi feature hoàn thành phải có một commit mô tả rõ nội dung thay đổi.

