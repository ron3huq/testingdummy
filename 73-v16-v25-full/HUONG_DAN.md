# Bổ sung My League + kits cho 73 V16 đã có face V25

**Điều kiện:** dùng APK 73 V16 đã áp V25 và đã được bạn xác nhận face hoạt động tốt. Gói này là cập nhật nhỏ, không phải gói cài lên APK V16 gốc chưa có V25.

## Cài bằng MT Manager, không cần root/USB

1. Xuất save và giữ một bản sao APK face đang hoạt động để dự phòng.
2. Giải nén ZIP này. Mở **APK đang có face V25** bằng MT Manager → Xem/View. Thêm/gộp thư mục `assets/` vào gốc APK, đồng ý ghi đè file trùng; giữ các file khác.
3. Ký bằng **đúng khóa/chứng thư MT đã dùng cho game và APK resource hiện tại**. Cài đè APK mới. Nếu Android báo xung đột chữ ký, **dừng, đừng gỡ game**; cần chọn đúng khóa đã dùng.

Resource V9+ đang chạy giữ nguyên. Cài đè cùng khóa sẽ giữ dữ liệu ứng dụng. Bộ nạp chỉ cập nhật file mod; nó không ghi đè file save SQLite đang có.

## Phần đã khôi phục từ bộ thay đổi cũ được lưu

- Sáu giải: Uefa Champion League, AFC Nation League, World Nation League, Eredivisie, Asia-Pacific League, Y17 Champion League.
- Danh sách đội và phân nhóm; 18 roster native tùy chỉnh; 176 hồ sơ huyền thoại; các chỉnh chỉ số/kỹ năng, áo tay dài, đội trưởng, số áo và vị trí đã cấu hình trong bộ cũ.
- Lịch thi đấu, mô phỏng theo sức mạnh/phong độ/phân nhóm, cầu thủ ghi bàn/kiến tạo theo roster, sân nhà và thời tiết. Bộ gốc 73 xử lý lưu save và kết quả trận thật; không tính lại lịch sử kết quả đã lưu.
- Kits: Sparta Rotterdam → Real Madrid 2017; Telstar → Manchester United 2007; AZ → Real Madrid 2011; Heerenveen → Barcelona 2017, mỗi đội hai bộ. Bổ sung ánh xạ native đúng bốn đội; không ép một font hay kích thước tên/số áo chung.
- Giữ nguyên toàn bộ texture, đầu, miniface, background, đổi tên/quốc tịch/CLB và logic face V25 đang hoạt động. Không sửa `libnoodle_hair.so`, `noodle_hair.py` hoặc container `pc9298`.

Các giải/đội mới nên kiểm tra bằng **mùa My League mới**. Mùa đã lưu có danh sách đội khác vẫn giữ lịch cũ. Các tùy chỉnh riêng chỉ tồn tại trên máy cũ đã bị gỡ, chưa từng có trong file đã gửi/lưu, không thể suy ra từ gói này.

## Kiểm tra nếu có lỗi

- `files/embedded-gateway/work/tools/myleague-73-status.json`: mong đợi `INSTALLED`, version `v25-73-full1`.
- `select-team-status.json`: mong đợi `HOOK_ACTIVE`.
- `noodle-hair-status.json`: face giữ version `player-faces-v25-73-v16-port-test`.

Các đường trên thuộc dữ liệu nội bộ `com.efootball.revival.local`; dùng công cụ tài liệu của game nếu có. Không mặc định truy cập được bằng Android/data.

## Phạm vi kiểm tra

Đã kiểm tra module/API My League 73 thật trên SQLite thử, 23 prologue hook, nhánh trampoline có điều kiện, 18 roster/176 profile và quy tắc native trong Unicorn, cấu trúc 8 kits/32 font/16 thumbnail, toàn bộ checksum gói. Backing DB lookup của engine được mô hình hóa trong bài kiểm tra native vì bản 73 có bản vá mở rộng record riêng; không coi đó là thử DB live.

**My League/kits của bản bổ sung chưa được thử trên GPU điện thoại.** Face trước đó do bạn xác nhận hoạt động tốt; dữ liệu face được giữ byte nguyên vẹn. Không hứa không còn lỗi khi chưa có kết quả thử thiết bị.
