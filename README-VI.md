# 73 V16 UI7.13 FULL · một gói · không có Part 3

Chỉ dành cho APK 73 V16 (311010108), không dùng cho efootxi.

Tải một ZIP duy nhất. Mở ZIP, vào thư mục `testingdummy-<commit>/`, chép **assets/** và **classes5.dex** vào gốc APK 73 V16 trong MT Manager, chọn thay thế, sau đó ký một lần. Không chép nguyên thư mục bọc hoặc ZIP vào APK. Không cần áp bất kỳ Part/UI cũ nào.

Nên dùng APK 73 V16 gốc làm nền khi đóng gói; cài cập nhật bằng cùng khóa ký đang dùng để giữ save. Không cần gỡ game hay xóa dữ liệu. Sao lưu save trước khi thay APK. Nếu APK cũ có pc9308, không còn tham chiếu hoặc tải file đó trong bản này.

## Đã sửa

- Lỗi C_NAJM_0009 trong log UI7.12: `myleague-live-teams.json` là snapshot đội hình được ghi khi chạy nhưng bị pin SHA như mã tĩnh. Loại snapshot và diagnostics khỏi danh sách kiểm tra/copy/repair tĩnh. Giữ kiểm tra SHA của mã và tài nguyên tĩnh.
- Đã tái hiện đúng lỗi cũ, kiểm thử đăng nhập gateway khi không có snapshot và sau ba lần snapshot thay đổi đều NOERR, đồng thời mã tĩnh bị sửa vẫn bị từ chối.
- Bỏ Part 3: bỏ pc9308 và năm redirect NCA1–NCA5 cùng các mặc định đổi tên/ngoại hình của năm thẻ đó. Không xóa thẻ trong save, không xóa tùy chỉnh riêng đã lưu trong save.
- Gộp toàn bộ Part 1, Part 2, Part 4 tích lũy trước đây vào một gói: các face cũ khác, sáu face mới, UI/editor, kits/Y08/Y17, sleeves, accessories/màu, Transfer và các sửa trước.
- Transfer chỉ cho UEFA Champion League (122), World Nation League (128), Y08 (473), Y17 (518), chặn cả API ngoài bốn giải. Giảm thu thập đội nền xuống các đội thuộc bốn giải. Các giải khác vẫn tồn tại trong game.
- Cập nhật nhãn UI/diagnostics lên UI7.13; chỉ gắn bridge nhập ảnh một lần.

## Face mới vẫn giữ (Part 4 trước đây)

88042803047215 Ronaldo 2018; 105634720685845 Ronaldo Nazário; 105565464400480 Zidane; 105625593957752 Henry; 89138288266704 Ronaldo Mullet V8; 176104 Yan Diomande.

## Kiểm chứng

Có báo cáo gateway/native/package trong validation/. Đã kiểm tra mọi hàng manifest với gói này hoặc APK nền. Chưa chạy trực tiếp trên điện thoại Android/GPU; kiểm thử gateway trên máy build không thay thế kiểm thử trận đấu trên máy bạn. Các giới hạn tính năng của UI7.12 vẫn giữ: copy animation chỉ tám trường native đã xác minh; preview ảnh là khung crop, không phải giả lập đầy đủ giao diện thẻ trong game.
