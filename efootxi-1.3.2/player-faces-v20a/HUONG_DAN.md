# v20a — bản vá lỗi mở Đội hình trên v20

Chỉ dành cho máy đã cài **Faces-v20-14-cards-4-teams.zip**.

1. Buộc dừng game trong Cài đặt Android. Không chỉ thoát về màn hình chính.
2. Giải nén **Faces-v20a-squad-crash-hotfix.zip**.
3. Dùng MT Manager gộp `work/` vào `files/embedded-gateway/work/`, chép đè cả ba tệp trong `work/tools/`.
4. Mở lại game rồi thử vào Đội hình. Log mới phải ghi `player-faces-v20a-squad-abi-fix`.

Không xóa dữ liệu ứng dụng, save, hoặc `livedata/`. Gói này giữ nguyên toàn bộ mặt, tóc, ảnh thẻ, kits, font, chỉ số và vị trí của v20. Không cần cài lại gói đầy đủ v20 sau bản vá.

Lỗi mã đã tìm được: hook UI tại `0x3883248` của v20 chỉ chuyển tiếp 10 đối số. Hàm native đọc 8 đối số trong thanh ghi và 15 đối số trên stack, tổng cộng 23. Đối số thứ 17 (đếm từ 1) là con trỏ bị đọc ở `0x3883628`; thiếu nó có thể gây văng trước khi bộ đếm `extended_card_builder_calls` tăng. v20a chuyển tiếp đủ 23 đối số, kể cả khi tính năng sửa mặt tắt.

v20a cũng sửa cách tìm vùng trống cho trampoline: xét toàn bộ khoảng trống giao với phạm vi lệnh B ±128 MiB, thay vì chỉ xét đầu khoảng trống. Tiếp tục dùng mmap không cố định; không ghi đè vùng nhớ đã cấp phát. Nếu vẫn không cấp phát được, hook báo lỗi kèm địa chỉ và số lần thử.

Đã tái hiện lỗi đọc bộ nhớ không hợp lệ của binary v20 và kiểm tra binary v20a bằng các lệnh ARM64 thật trong prologue, 15 lần đọc đối số stack, lần đọc con trỏ và epilogue của engine. Các phần còn lại của hàm dựng thẻ được bỏ qua trong kiểm tra này. Đã chạy lại 792 kiểm tra native với mô hình biên engine, 15 đường cài hook Python, kiểm tra hash/manifest và ZIP.

**Chưa kiểm chứng trực tiếp trên điện thoại.** Bản vá sửa lỗi ABI đã chứng minh được; chưa thể bảo đảm mọi nguyên nhân crash đã hết và chưa xác nhận bốn mặt hết đen. Nếu còn văng, gửi `work/tools/noodle-hair-status.json` của lần chạy mới; không cần gửi toàn bộ thư mục game.
