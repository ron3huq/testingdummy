# UI7.5 Earth — Y08 kits và Player Model

Part 2 Main đầy đủ cho APK 73 V16. Part 1 Faces dùng lại bản UI7. Đây không phải APK cài trực tiếp và không dành cho efootxi 1.4.1.

## Sửa kits Y08

Bản trước chép khối palette nhưng bỏ sót bit2 tại Team+0x3fd mà mã game dùng để quyết định đường đọc mẫu áo. UI7.5 đồng bộ cờ này cho 10 đội thay thế, sửa cả lookup trực tiếp và các Team đã lưu đệm. Danh sách uniform gửi cho client nay giữ ID đội Y08 đúng với roster/cache; resolver native và các recipe hiện có chuyển sang nguồn áo tương ứng.

| Đội Y08 | ID đội | Nguồn kits |
|---|---:|---|
| Manchester United | 1706 | Telstar 352 — bộ retro MU đang có |
| Real Madrid | 4937 | AZ 242 — bộ retro Real đang có |
| Arsenal | 1957 | Arsenal 108 |
| Barcelona | 1956 | Barcelona 121 |
| AC Milan | 4962 | AC Milan 120 |
| Juventus | 4964 | Juventus 102 |
| Inter Milan | 4938 | Inter Milan 103 |
| Liverpool | 1950 | Liverpool 119 |
| Chelsea | 1228 | Chelsea 101 |
| Bayern | 1955 | Bayern 127 |

Các gói texture/CPK được giữ nguyên từ UI7.4 đã vào game được. Y17 giữ nguyên nhánh gửi uniform và tài nguyên áo đã được người dùng xác nhận. Bộ sửa roster, OVR đội người chơi, face, skill và áo tay dài mặc định được giữ lại.

## Player Model

Player Editor → Appearance & Motion → Player Model · Body Proportions.

Có 11 mục tương ứng ảnh yêu cầu: Arm Length, Shoulder Width, Neck Length, Chest Measurement, Neck Size, Shoulder Height, Leg Length, Thigh Size, Waist Size, Arm Size, Calf Size.

Mặc định mỗi mục là Original, không ghi đè số gốc. Bật ô của mục cần đổi rồi kéo thanh0–14; 7 là mức trung tính của decoder native. Restore Original bỏ các ô chọn; nhấn Save để lưu. Sửa trước khi Enter Game; nếu đã vào game, đóng hẳn và mở lại trước khi chỉnh.

Cài đặt lưu theo đúng ID thẻ64-bit trong meta của save cục bộ; áp ở bản sao appearance khi game dựng cầu thủ, không sửa record mặt/tóc gốc. Không quét catalogue, không thêm truy vấn SQL khi render cầu thủ; phần tìm kiếm giữ nguyên mã. Chiều cao/cân nặng vẫn ở nút riêng.

## Cài đè từ UI7.4 đang chạy

1. Giữ APK đang có cả Part 1 Faces và UI7.4. Sao lưu save nếu cần.
2. Trong MT Manager, chép đè toàn bộ nội dung ZIP UI7.5 vào gốc APK đó, rồi ký bằng cùng khóa hiện tại và cài đè.
3. Không gỡ game, không xóa dữ liệu hoặc tài nguyên. Đóng hẳn rồi mở lại, xác nhận UI7.5 Earth.

Nếu bắt đầu từ APK 73 V16 gốc, áp đủ Part 1 Faces UI7 và Part 2 UI7.5 trước khi ký. Không cần áp nối tiếp các Part 2 cũ. Resource V9 vẫn là tài nguyên nền riêng.

## Kiểm tra và giới hạn

- 180 tổ hợp đối thủ/phía người chơi trong Y08: ID đội và uniform đồng bộ; giữ slot hợp lệ; nhánh Y17 không đổi.
- Thực thi thư viện ARM64 phát hành bằng Unicorn với accessors game73: cả10 đội, cờ mẫu áo hai trạng thái, lookup mới và cache cũ; kiểm tra lại roster/formation/OVR/skill/phụ kiện/sleeve trước đó.
- Decoder cơ thể thật của73: 11 trường ×15 giá trị; các bit mặt/tóc/đầu/áo và dữ liệu còn lại giữ nguyên; scope đúng thẻ64-bit kể cả appearance nguồn có ID khác.
- Lưu/đọc lại/khôi phục model, kiểm tra giới hạn và chặn sửa sau khi engine đã nạp; không thay dữ liệu chỉ số cầu thủ.
- Đăng nhập gateway73, URL/hash, manifest7383 mục,47 payload quan trọng, DEX giữ267 lớp gốc; cả hai Part không trùng đường dẫn.

Đây là kiểm tra trên máy với dữ liệu mô phỏng ở ranh giới Android; chưa kiểm thử trực tiếp trên điện thoại. Không có căn cứ cam kết mọi lỗi xung đột đều đã được loại bỏ trên thiết bị. Nếu kits vẫn sai, Runtime Diagnostics có thêm y08-kits-status.json để xác định chính xác hai đội và uniform đã gửi.

Mã nguồn và báo cáo kiểm tra kèm theo. Các script có đường dẫn workspace của phiên xây dựng; không kèm save hoặc dữ liệu người chơi.
