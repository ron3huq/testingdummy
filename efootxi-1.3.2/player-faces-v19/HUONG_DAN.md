# V19 — gói thử sửa mặt đen, dữ liệu CLB trên thẻ và kit Sparta

**Chưa xác nhận hết mặt đen trên điện thoại.** Người dùng đã xác nhận v18 vẫn thất bại; không coi log HOOK_ACTIVE/material confirmed là bằng chứng hình ảnh đã đúng. V19 xử lý một trường hợp vẽ chồng mà các bản trước bỏ sót, đồng thời ghi tên mesh phụ thực tế để kiểm chứng. Bốn khuôn mặt riêng vẫn được giữ; không thay chúng bằng đầu 2006.

## Cài một gói duy nhất

1. Tải `Faces-v19-13-cards-Sparta-kits.zip`, giải nén.
2. Buộc dừng game.
3. Dùng MT Manager gộp/chép đè cả `work/` và `livedata/` vào `files/embedded-gateway/` của game. Không xóa dữ liệu ứng dụng hoặc save.
4. Mở lại game. Trong `work/tools/noodle-hair-status.json`, phiên bản phải là `player-faces-v19-common-head-card-clubs`. Gateway giữ đúng 2441 byte; manifest/checksum đã cập nhật.

## Nội dung

- Chỉ bốn đầu lỗi: Ronaldo2017 **88044950524330**, Ronaldo2027 **106734785925546**, Ronaldo Jr **105765448873424**, Hoang Duc **105643042189511**. Engine có đường gắn đầu mới vào component chính và giữ mesh mặt gốc trong attachment phụ. Bộ kiểm tra cũ chỉ xử lý hai component dùng cùng mesh nên bỏ sót trường hợp khác mesh. V19 tắt main pass, depth pass và cast shadow của attachment mặt gốc được nhận diện chính xác, giữ mesh đầu mới; khôi phục cờ khi actor được dùng lại hoặc tắt tính năng. Đây là giả thuyết sửa cần kiểm chứng trên máy, chưa phải nguyên nhân được chứng minh.
- Sửa trực tiếp bản sao dữ liệu **giao diện thẻ**, thay vì chỉ sửa CLB ở bản ghi cầu thủ: sáu thẻ Xuan Son, Dinh Bac, Hoang Duc, Hoang Hen, Cao Pendant, Tai Loc bỏ các trường CLB/giải đấu và giữ Việt Nam. Speed đổi trường CLB hiển thị sang **Al Nassr**; quốc tịch vẫn Bồ Đào Nha. Chưa xác nhận hình ảnh UI trên máy.
- Kit **chỉ Sparta Rotterdam, Team ID351**: sân nhà dùng ảnh áo trắng `u0109p1_home.ftex`; ô áo thứ hai dùng ảnh xanh ngọc `u0109p1_third.ftex`. Tệp thứ hai thực chất là áo third2017–18, được dùng cho ô thứ hai theo hai bộ bạn gửi; không tự tạo áo away đen. Hai atlas BC7 FTEX5120 được giải mã và nén thành ETC2RGB1024 theo template native của Sparta. Các mip nhỏ FTEX bị hỏng được bỏ; giữ bố cục mip native (mỗi texture một level1024). DDS đính kèm vượt giới hạn tải32MiB, không được đọc; hai FTEX đã chứa đủ hai ảnh sử dụng.
- Toàn bộ299 chunk asset v18 được giữ nguyên, gồm mặt/tóc/LOD/rig/material và ảnh thẻ. Chỉ thêm hai texture kit mang tên Sparta. Không đổi bộ xương, Face ID, số áo, font áo hoặc kích thước chữ. Tên trên áo tiếp tục chữ hoa đầy đủ theo lựa chọn đã xác nhận: XUAN SON, DINH BAC…

## Kiểm tra sau cài

Xem riêng bốn thẻ lỗi trong trận và cutscene/replay, xem thẻ Việt Nam/Speed và hai áo Sparta. Nếu mặt vẫn đen, gửi `noodle-hair-status.json` của v19 sau khi đã xem một thẻ lỗi; các trường mới có ích là `last_common_head_mesh`, `common_head_candidates`, `common_head_render_disabled`, `common_head_other_mesh`, `card_ui_affiliation_changes`, `icon_ui_affiliation_changes`. Không cần chép toàn bộ thư mục game.

752 kiểm tra native ARM64,14 đường cài hook, manifest/idempotence/checksum và giải mã độc lập hai texture đã chạy. Engine allocator/virtual/UI-source boundaries được mô hình hóa; không chạy Android renderer/GPU ở đây. Chưa xác nhận ảnh kit qua shader/UV thực tế, UI CLB hay bốn mặt trên điện thoại. `device_verified=false` là chủ ý chính xác.
