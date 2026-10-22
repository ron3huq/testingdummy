# My League Studio v17

Giải nén ZIP app, mở MyLeagueEditor.html bằng Chrome/Edge mới. App chạy offline sau khi tải, không phải APK cài đặt. Không cần root.

## Tạo pack

1. Mở tab **Pack cầu thủ → Tạo pack mới**.
2. Đặt tên; tìm tên hoặc đúng Card ID và thêm người. Chỉ hiển thị thẻ có đủ bản ghi registry.
3. **Lưu pack**, rồi vào **Xuất & nhập → Xuất ZIP để chép vào game**.
4. Buộc dừng game. Sao lưu bộ work/tools và file save local trước khi cài pack.
5. Giải nén ZIP mới; chép **đủ10 file** trong install/work/tools/ vào files/embedded-gateway/work/tools/ bằng MT Manager. Không chép cả folder install vào đây.
6. Mở game, vào danh sách tuyển cầu thủ đặc biệt. Pack không tự cấp người; rút bằng cơ chế sẵn có. Muốn đưa cầu thủ vào CLB My League, dùng tab đội hình riêng.

Giá gateway hiện tại100 coin/lượt,900 coin/10 lượt. Bản offline có policy coin99999 thì vẫn giữ policy đó. Pack ít hơn10 người còn lại không đủ cho một lượt10; dùng lượt1 hoặc reset.

Pool đã cài giữ danh sách để bảo toàn lịch sử rút. Muốn thay người sau đó: **Nhân bản với ID mới**, chỉnh bản mới; **Ẩn pack** cũ nếu muốn. Đổi tên pack vẫn được. Ẩn không xóa các thẻ đã sở hữu.

Có thể tải riêng pack JSON, nhập lại hoặc nhập ZIRU_PACKS_CONFIG.json / backup state.packs của app tham khảo. ID pack được cấp lại để tránh đè pack khác. Tất cả Card ID phải tồn tại trong registry của bản Android này; không nhập toàn bộ DB/response của người khác. Không nhập APK trực tiếp vào tab pack.

## Skill và preset động tác

64 skill được đối chiếu lại tên/mã. Defensive Fortress chưa xác minh được mã riêng, nên chưa có nút gán; Fortress vẫn có. Các mã nội bộ không còn được hiển thị làm skill.

Dáng chạy/rê bóng có5 ô preset riêng. Ô trống không ghi đè. Đây là mã nội bộ, chưa có preview; số lớn hơn không có nghĩa là đẹp hơn hay mạnh hơn. Kiểm tra từng thay đổi trong trận. Chiều cao/cân nặng và tay dài/ngắn vẫn hỗ trợ. Tóc/mặt/cơ bắp và tên hiển thị trong game chưa có bộ chỉnh đã xác minh.

Dự án v16 nhập được bằng **Nhập dự án JSON**. App báo chuyển đổi: Attack Trigger sửa về131, các cờ skill chưa xác minh chuyển về0 để loại bỏ ghi đè sai trước đây. Giữ bản JSON cũ và kiểm tra lại danh sách trước khi xuất. Các preset mới không thêm nếu bạn để trống.

## Kiểm tra trạng thái

Trong files/embedded-gateway/work/tools/:

- select-team-status.json: version native-hotfix-v17, editor_error:null, editor_status.ready:1.
- Sau khi mở danh sách tuyển: myleague-packs-status.json phải có state:READY, error:null, packs đúng số cấu hình. ERROR kèm Card ID hoặc agentID xung đột sẽ không cài dở dang pool.

Gửi nội dung lỗi nếu chưa thấy pack; không thay dt200. Toàn bộ app/runtime mới chưa kiểm tra trực tiếp trên Android. Đã kiểm tra giao diện Chromium, native ARM64 bằng Unicorn và gateway thật trên bản sao save. Chi tiết bằng chứng/giới hạn ở NGHIEN_CUU.md và validation/.

Thời tiết, sân, đội hình và buffs hiện có được giữ; phần mới chỉ áp dụng các trường bạn sửa. Mặc định dự án không thêm pack/ghi đè cầu thủ/đội. Runtime ZIP riêng cũng dùng dự án trống.
