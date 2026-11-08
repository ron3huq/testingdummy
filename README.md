# FULL8 RC26 · Khôi phục Transfer Edit My League

Sửa hồi quy RC25: việc tách Event Edit đã gỡ lớp dữ liệu nền chỉ đọc của Transfer cũ. Vì vậy Barcelona và các đội UEFA/World Nation lại báo cần snapshot native và không mở editor.

RC26 khôi phục lớp fallback RC24 trước bước kiểm tra/nạp profile đã lưu. Đội hình/record đã lưu hoặc đã quan sát trong My League được ưu tiên; dữ liệu đội hình công bố chỉ dùng khi thiếu bản ghi. Dữ liệu nền bất biến có thể dùng cùng nguồn, nhưng **chỉnh sửa My League122/128 và Event901/902 vẫn có project, khóa lưu và phạm vi native riêng**. Không tự chuyển, xóa hay gộp chỉnh sửa đã lưu.

Kiểm tra đã tái hiện lỗi Barcelona ở RC25, mở lại72đội có dữ liệu nền khi không có snapshot, lưu/đọc lại đội hình/số áo/đội trưởng/người đá phạt và chỉ số/chân/skill; kiểm tra cold start và chỉnh Event không đổi My League. Những đội ngoài bộ dữ liệu nền vẫn dùng snapshot native như cơ chế trước đây, không bịa đội hình mới.

Đây là FULL tích lũy RC25, chỉ sửa tuyến dữ liệu của Transfer cũ và checksum liên quan. Giữ nguyên native libraries, classes5.dex, mặt Ronaldo, Match Settings, UI và mô phỏng UCL; giữ Ajax theo lựa chọn cuối. Không chứa APK, engine hoặc save cá nhân.

## Áp bằng MT Manager

1. Sao lưu APK/save. Chép đè toàn bộ `assets/` và `classes5.dex` từ gốc ZIP FULL vào bản sao APK v19.1 đang dùng.
2. Lưu, ký bằng khóa cũ và cập nhật đè. **Không xóa data, không gỡ game.**
3. Đóng hẳn game rồi mở lại. Mở Transfer cũ ở giao diện ngoài trước Enter Game, chọn UEFA Champion League hoặc World Nation League.

Giữ quy tắc editor cũ: sửa trước Enter Game; đóng/mở lại app nếu engine đã nạp. Báo cáo RC26 trong validation là kiểm tra trên host/fixture, chưa xác nhận lại trên điện thoại. Báo cáo RC25 và các bản trước là lịch sử.
