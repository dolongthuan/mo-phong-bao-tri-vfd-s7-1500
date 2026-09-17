# Nhật ký phiên bản gửi giảng viên xem trước

## Trạng thái hiện tại

| Hạng mục | Trạng thái | Ghi chú |
|---|---|---|
| Mô phỏng PLC S7-1500 | Hoàn thành mức chức năng | Hai lỗi F1 và F4 |
| Python Bridge | Đã viết | Cần kiểm thử lại với DB Number hiện tại |
| Telegram | Đã có mã nguồn và bằng chứng thử nghiệm | Token không có trong gói gửi thầy |
| Termux API | Đã thử nghiệm | TTS có thể treo, đã có timeout |
| Twilio | Tùy chọn | Chưa cấu hình trong gói công khai |
| Báo cáo Đồ án 1 | Đã có bản hiện tại | Cần giảng viên xác nhận phạm vi và tên đề tài |
| GitHub | Đã chuẩn bị cấu trúc sạch | Chờ tạo repo và gửi link |

## Việc cần thực hiện sau khi giảng viên phản hồi

1. Chốt tên đề tài và phạm vi hai lỗi F1/F4.
2. Chốt sơ đồ kiến trúc và danh sách feature.
3. Kiểm tra DB Number và offset trong TIA Portal.
4. Chạy lại TC01 đến TC06, lưu minh chứng theo từng TestCaseID.
5. Đồng bộ số liệu cuối cùng vào báo cáo.
6. Đưa repo lên GitHub và tiếp tục commit theo từng feature.

Các ghi chép thử nghiệm cũ có chứa cấu hình cá nhân không được đưa vào gói gửi giảng viên. Khi cần truy vết, nhóm sử dụng bản lưu nội bộ.
