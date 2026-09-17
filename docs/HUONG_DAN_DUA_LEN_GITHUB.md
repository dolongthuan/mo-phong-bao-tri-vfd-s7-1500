# Hướng dẫn đưa dự án lên GitHub

## Trước khi thực hiện

1. Đọc `docs/XIN_Y_KIEN_GIANG_VIEN.md` và nhận phản hồi của thầy.
2. Kiểm tra `.env` không có trong thư mục dự án.
3. Nếu token từng được gửi cho người khác, thu hồi token cũ và tạo token mới.

## Tạo repository

Tạo một repository trống trên GitHub. Không chọn tạo sẵn README hoặc `.gitignore` vì gói dự án đã có hai file này.

## Khởi tạo và đẩy mã nguồn

```powershell
git init
git add .
git commit -m "Khởi tạo dự án mô phỏng cảnh báo VFD"
git branch -M main
git remote add origin <DIA_CHI_REPOSITORY>
git push -u origin main
```

## Cách commit các lần tiếp theo

```powershell
git add <cac-file-da-sua>
git commit -m "Hoàn thành feature mô phỏng quá dòng F1"
git push
```

Chỉ commit khi một phần công việc có ý nghĩa đã hoàn thành. Không commit `.env`, `venv`, cache Python hoặc log chạy có thông tin riêng tư.

