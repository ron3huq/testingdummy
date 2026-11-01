# V19.1 FULL-6 · Transfer, Spider, face và LOD

Gói tích lũy dành cho APK73 eFootball V19.1 gốc SHA256 `9c0b249557eeab1543ce143af4d08269b6e9a5a965472242815dba5712c76469`. Chép toàn bộ `assets/` và `classes5.dex` vào APK V19.1, thay tệp trùng, ký bằng khóa đang dùng rồi cài cập nhật. Không cần áp lần lượt các FULL trước. Export Save trước khi cập nhật; giữ dữ liệu ứng dụng. Đóng game, chỉnh và lưu trước Enter Game; sau đó mở lại ứng dụng để nạp cấu hình native.

## Sửa trong FULL-6

- **Transfer toàn ảnh thủ môn:** đã tái hiện bằng bộ tra cứu ARM64 gốc ở chế độ cache2. Bản cũ ghi khóa cache của mọi thành viên thành0, khiến cả đội đọc cầu thủ số0. Bản này giữ nguyên khóa cache và fullID của từng người, chỉ đổi thứ tự đội hình. Kiểm tra đội trưởng và cả6 vai trò đá phạt qua chính bộ tra cứu cache, qua3 pool vật lý và lặp lại nhiều lần. Mã cache có phần cờ ở32bit trên cũng được giữ nguyên. Nếu một cầu thủ chưa được tạo trong cache, bản vá từ chối sửa cache đó thay vì trỏ nhầm về thủ môn; thay cầu thủ trước Enter Game để game tạo lại cache.
- **Transfer báo “no native kit in that slot”:** lưu vị trí/đội hình không còn tự coi các slot kit/GK có sẵn trong snapshot là một lần thay áo. Đổi kit rõ ràng vẫn được xác minh, kit không tồn tại vẫn bị từ chối và không lưu dở dang. Đội trưởng, người đá phạt và số áo gắn vớiID cầu thủ.
- **Spider-Man V1 →106782819217056; Miles →88035555413452:** hai ZIP mới gửi có nội dung giống hai ZIP đã nhập. Lỗi nằm trong bộ lọc runtime: thiếu cho phép hai thẻ có face gốc khác4522. Đã sửa và chạy160 trường hợp đường nạp mesh/texture,4 biến thể, dạng đường dẫn có/không dấu nháy vàNUL; thẻ ngoài phạm vi giữ nguyên.
- **Ronaldo2027 →89138556572074:** dùng geometry mặt/cổ,UV, trọng số xương hiệu dụng và bind gốc4522; bỏ lớp mắt/miệng/face phủ cũ. Giữ tóc2027 và các byte texture tóc; đặt cả khối tóc cao hơn1.05cm để khớp đỉnh đầu4522. Không lấy face từ hai bảnVol9 đã hủy.
- **Joker →106781476920663:** dùng JokerV3 đã gửi, tăng đầu10%, căn lại mốc hàm với model native và kéo chuyển tiếp cổ liên tục; giữ điểm gắn thân và xương thân/tay. Kiểm tra các đường nối trùng nhau sau khi fit.
- **LOD/tay kéo dài:** Ronaldo2027, Joker, Raiden và hai Spider dùng danh sách RequiredBones giống4522/SK_Base_Face của game:166 ởLOD0,153 ởLOD1. Loại bỏ13 mục mặt được chèn trước các xương vai/tay ởLOD thấp, đổi các trọng số mặt không có ởLOD đó sang đầu. Không đổi thứ tự xương thân.20 biến thể mesh/material đã qua trình đọc độc lập, kèm40 kiểm tra danh sáchLOD. Giữ LOD0 đãcooked-out của nguồn khi có, tránh nhân đôi buffer mesh không dùng. Cần đối chiếu hình thể trong trận trên điện thoại để xác nhận kết quả cuối.

## Những phần tích lũy được giữ

- Sửa chân thuận, tần suất và độ chính xác chân không thuận bằng đúng trường native; giữ các chỉnh riêng khi sao chép donor.
- Bảo vệ đội chính và dự bị người dùng khỏi quy tắc giảmOVR của NPC ở7 giải MyLeague. Những chỉ số do người dùng chủ động chỉnh vẫn áp dụng.
- Trong Transfer, chọn thành viên để mở **Abilities · Celebrations · Accessories**: chỉ số, ID ăn mừng,10 loại phụ kiện native/tay áo áp theo fullID và giải được chọn, kể cả cầu thủNPC không có serial sở hữu. Lưu bản nháp đội trước khi chỉnh thành viên.
- Y17/Y08: gắn bàn thắng/kiến tạo CPU theo từng sự kiện và trọng số đội; loạiGK và tự kiến tạo. Top20 là tối đa20 cầu thủ thực sự có số liệu. Không viết lại trận cũ hoặc bịa kiến tạo để lấp bảng.
- Giữ Wukong tóc dày/nâu olive theo ảnh; MulletA dùng tóc56322; Ronaldo2017/Noodle/Honda có miệng tối hơn; Raiden giữ materialPBR kim loại. BảnVol9 vẫn hủy.
- Giữ Accessories theo nhóm, reset màuOriginal, chỉnh từng tab không xóa tab khác; giữ chỉ mục tìm kiếm, gộp yêu cầu nhanh, giới hạn tải ảnh và dọn observer của giao diện.
- Giữ sửa đăng nhập FULL5.2: resource_revision là số19003,39 targetID dùng chung một hằng; readiness native vẫn bắt buộc. CPK loading tại cả3 đường giữ SHA256 `6fa4b9050f0a125e9ee295a7260ca3f1b5f718cdca6d5af94e2cc697d215fc4a`.

## Chưa hoàn tất và giới hạn kiểm chứng

**Bandagepack PC chưa chuyển xong sang phụ kiện mobile. Chế độ điều khiển riêng một cầu thủ khiAI bật chưa triển khai.** Gói này giữ các phụ kiện native và camera hiện có; không có hai tính năng mới đó để bật. Bandage cần UV cơ thể tương ứng và material riêng theo cầu thủ; điều khiển cần trace quyền nhận input thực trong trận và kiểm tra vòng bật/tắtAI, thay người, pause/replay. Xem `RESEARCH-VI.md`.

Nghiên cứu nhịp trận/phong độ dựa trên mô tả A56: chưa xác định nguyên nhân việc sáng thấp/2–5giờ mượt hơn. Không đồng nhất tốc độ di chuyển với đồng hồ trận, không tự thay tốc độ vật lý. Màn hình120Hz/mục tiêuFPS120 chưa phải phép đoFPS render hoặc độ trễ thao tác.

Các bản kiểm tra kèm trong `validation/` phân biệt hàmARM64/engine thật, gateway thử và phần cần máy thật. Đã kiểm tra CMD_LOGIN gốc, toàn bộ chuỗi manifest tài nguyên và đăng nhập lại bằng cacheversion.bin. Chưa chạy bảnFULL6 trênA56; chưa thể cam kết100% không crash/không lag/không xung đột. Gói không có save,DB thử hay diagnostics cá nhân. Ảnh dựng chỉ phục vụ đối chiếu hình học, không thay thế ảnh trong game.
