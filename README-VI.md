# V19.1 FULL-7

Gói tích lũy cho APK73 eFootball V19.1 gốc SHA256 `9c0b249557eeab1543ce143af4d08269b6e9a5a965472242815dba5712c76469`. Chép toàn bộ `assets/` và `classes5.dex` vào APK V19.1, thay tệp trùng, ký bằng khóa đang dùng rồi cài cập nhật. Giữ dữ liệu ứng dụng và export save trước khi cập nhật. Không cần cài lần lượt các FULL trước.

Chỉnh và lưu trước **Enter Game**, rồi mở lại ứng dụng. **Match Settings** mở hai mục: phong độ My League và điều khiển một cầu thủ.

## Phong độ Excellent

Trong **Match Settings → My League · Condition**, bật **Always Excellent**. Mặc định áp dụng cho cầu thủ sở hữu, gồm chính và dự bị; có thể chọn cả hai đội. Bản sửa ghi đúng phong độ cuối cùng sau bước giới hạn Excellent của engine. Live Update A–E, độ ổn định Form, thể lực và chấn thương giữ ý nghĩa riêng. Lựa chọn được lưu trong dữ liệu cấu hình ứng dụng và không mất khi khôi phục tài nguyên APK.

## Điều khiển một cầu thủ khi bật AI

Mở **Match Settings → Single Player · AI matches**, chọn cầu thủ theo tên hoặc full card ID và bật tính năng. Danh sách hỗ trợ cả thẻ sở hữu và cầu thủ trong catalogue; chỉ cầu thủ đang ở đội được điều khiển và có mặt trên sân mới được khóa.

- **AI tắt:** điều khiển thủ công gốc.
- **AI bật:** người dùng điều khiển cầu thủ đã chọn, đồng đội dùng AI.
- Cầu thủ được chọn ở ghế dự bị, rời sân hoặc chưa khả dụng: AI tiếp tục điều khiển; khóa được xét lại theo full ID khi đội hình thay đổi.
- Pause/replay và thay trận dùng đường khôi phục native; lựa chọn AI mới không bị bản lưu tạm cũ bật trở lại.

Mục này thay đổi quyền điều khiển và cursor; các thiết lập góc camera có sẵn tiếp tục dùng bình thường. Không có Python, SQL hay ghi tệp trong vòng cập nhật trận.

## Accessories và bandage

Trong **Player Editor → Accessories**, mở mục cổ tay trái/phải và chọn **Pack bandage**. Transfer cũng có lựa chọn tương tự trong Accessories của thành viên. Ba mẫu chuyển sang mobile: **trắng**, **đen bản rộng**, **vàng**; chọn riêng từng tay. Chọn **Use native wrist tape** để trở về băng native và màu đã lưu.

Bản chuyển đổi dùng UV và sáu màu da native, giữ nguyên mesh, xương, trọng số, alpha và vật liệu. Chỉ băng native ở tay được chọn mẫu mới được ẩn. Mẫu được phân biệt trước khóa cache để tránh lan sang cầu thủ khác. Đây là ba mẫu vải đã chuyển đổi từ gói nguồn; không phải nhập nguyên 326 texture PC hay toàn bộ hình xăm/da của gói đó.

## Face và các sửa tích lũy

- Spider V1 → **106782819217056**, Miles → **88035555413452**: tăng đầu 10%, làm đầy vùng cổ trước, giữ điểm nối thân, UV và texture.
- Ronaldo 2027 → **89138556572074**: áp lại đúng ZIP mới gửi, giữ hình mặt và tóc nguồn; làm mắt nâu và giảm tối quanh mí bằng vùng chỉnh giới hạn. Giữ nguyên phần texture ngoài vùng mắt. Sửa cách đóng gói khoảng trống giữa hai section của mesh nguồn.
- Giữ Joker V3, Wukong, Raiden và các face đã có. Hai bản Ronaldo Vol9 vẫn bị hủy.
- Giữ sửa Transfer toàn ảnh GK, vai trò theo ID cầu thủ, và lỗi lưu đội hình bị kiểm tra nhầm kit. Giữ chỉnh chỉ số, ID ăn mừng và Accessories theo full ID/giải.
- Giữ chân thuận/chân không thuận, bảo vệ chỉ số cầu thủ sở hữu trong bảy giải My League, bàn thắng/kiến tạo Y08/Y17 và các tối ưu giao diện trước đó.

## Kiểm chứng và giới hạn

Các báo cáo `validation/` phân biệt mã ARM64 gốc, mô phỏng native, gateway và kiểm tra tài nguyên. Đã kiểm tra phong độ cuối, lưu/nạp lại lựa chọn, bandage theo cầu thủ/cache, bật/tắt AI và các vòng pause/replay, cùng container face đã ghép. Không đưa APK PES nghiên cứu, RAR nguồn, save, DB thử hoặc diagnostics cá nhân vào gói.

Chưa chạy FULL-7 trực tiếp trên Samsung A56. Lỗi tay kéo dài và sẹo cổ cần xác nhận bằng hình trong trận; kiểm tra skeleton/LOD và ảnh dựng không đủ để khẳng định hai lỗi đó đã hết. Hiện tượng nhịp chơi mượt hơn lúc sáng thấp/2–5 giờ chưa được đo trên máy, nên không tự thay tốc độ vật lý hay thời gian trận.

CPK loading ở cả ba đường giữ SHA256 `6fa4b9050f0a125e9ee295a7260ca3f1b5f718cdca6d5af94e2cc697d215fc4a`. `resource_revision` vẫn là số nguyên; các kiểm tra readiness/checksum được giữ.
