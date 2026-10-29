# 73 V16 UI7.15 · Gói tích lũy một ZIP · Không Part 3

Dùng cho 73 V16, versionCode 311010108. Không dùng cho efootxi.

Trong ZIP cục bộ này, **assets/** và **classes5.dex** nằm ngay ở gốc. Nếu tải qua GitHub sau này thì mở thư mục bọc `testingdummy-<commit>/` trước. Chép **assets/** và **classes5.dex** vào gốc APK 73 V16 trong MT Manager, chọn thay thế rồi ký một lần. Không chép thư mục bọc vào APK. Không cần áp thêm UI/Part cũ. Dùng cùng khóa ký để cài cập nhật và giữ save; không cần gỡ game hoặc xóa dữ liệu.

## Ánh xạ mới

- **89138288266704 → Ronaldo Mullet V12**. Theo câu yêu cầu “bỏ Ronaldo 2008, thay bằng Mullet V12”; ID 106654775417922 trong tên ZIP được coi là ID thử của gói xuất. Đã thông báo giả định này trong chat. Gói Ronaldo 2008 vừa gửi đã bị loại khỏi container mới. Giữ ảnh thẻ có sẵn của thẻ Mullet; không dùng ảnh Ronaldo 2008 mới.
- 106654775417922 → Ronaldo 2014 V18, giữ riêng, không bị Mullet ghi đè.
- 105756321970183 → Wukong V9, không dùng V7.
- 105797392639585 → Ghost V1.
- 105568954067359 → Raiden; 106781476920663 → Joker.
- 88042803047215 → Ronaldo 2017 UCL final; 105794439855675 → Robben.
- 105625593957752 → Henry mới thay gói trước; các face còn lại tích lũy từ UI7.14 được giữ.

Không nhập mã Python/SO từ các ZIP face thử người dùng gửi; chỉ nhập tài nguyên mesh/material/texture, đổi namespace riêng và dùng runtime của bản 73.

## Thay đổi

- Sửa lỗi HTTP404 khi game xin `pc9311_mobile_and.ucas` bằng tên phẳng trong khi ảnh custom nằm trong thư mục generation. Server chọn đúng generation, giữ kiểm tra đường dẫn, HEAD, byte ranges và ETag. Tự dựng lại tài nguyên ảnh từ crop đã lưu nếu state/file bị thiếu; giữ save.
- Transfer vẫn chỉ UEFA122, World Nation128, Y08473, Y17518. Thêm 17 bố trí lấy từ bảng TacticsFormation native, cập nhật đồng bộ bốn plan; thêm SWAP chọn A rồi B trên danh sách hoặc sân. Giữ số áo theo cầu thủ, vai trò/tọa độ theo ô, giữ đội trưởng/người đá phạt theo ID. Đội hình lấy từ capture native và cấu hình đã lưu; đội chưa có capture được báo rõ, không tạo danh sách đoán.
- Thêm nút Copy Model trong Player Model; giao diện đọc cả thông số được kế thừa từ model đã copy. Copy gồm các trường native đã xác minh; không tuyên bố chuyển được mọi animation độc quyền gắn với danh tính.
- Áo dài xắn dùng viền gốc của mẫu áo dài, giữ UV để nhận màu/trim từ kit. Toàn bộ 123 mẫu thân được dựng lại; áo dài nguyên bản vẫn có lựa chọn riêng. Giữ bind pose và 166 xương native ở cả hai LOD.
- Accessories xử lý danh sách native đảo thứ tự, thiếu mục hoặc rỗng; thêm mục được bật qua hàm append gốc, không bỏ qua toàn bộ vì không đúng thứ tự 18 mục. Giữ mục không chỉnh và găng thủ môn; thêm bộ đếm diagnostics để kiểm tra băng trái/phải trên thiết bị.
- Giảm bóng tóc **chỉ 89138556572074** bằng material/SRO riêng. Không đổi hình học, UV, skin weights, skeleton, albedo; sau đảo namespace, toàn bộ byte mesh khớp gốc. Thẻ 106734785925546 vẫn dùng tài nguyên NX27 cũ.
- Thay ảnh lớn/miniface cho 10 thẻ: R9, Henry, Zidane, Robben, Spider-Man, Wukong, Ronaldo2014, Ronaldo2017, Raiden, Joker. Dùng ảnh gốc được gửi, căn đầu/crop theo khung native 128×128 và184×256, resize đồng tỉ lệ, không vẽ lại mặt. Ảnh custom người dùng tự nhập có ưu tiên cao hơn ảnh mặc định đi kèm.
- Tên/tên áo/CLB/quốc tịch và số đo cầu thủ thật cập nhật theo yêu cầu. Bốn nhân vật Spider-Man/Wukong/Raiden/Joker chỉ giữ quốc tịch Mỹ/Trung Quốc/Đức/Mỹ, không gắn CLB; các tùy chỉnh riêng đã lưu vẫn ưu tiên hơn mặc định.
- Giữ sửa bootstrap UI7.14: hash mã khi nâng cấp cùng kích thước, repair trước Python trên cả hai nhánh mở lại/nâng cấp; snapshot đội hình và diagnostics không bị pin như file tĩnh. Giữ tất cả thay đổi tích lũy ngoài Part3; không tải/redirect pc9308.

## Phần chưa hoàn tất và giới hạn kiểm chứng

**SOUND đổi riêng một thẻ chưa được triển khai trong bản này.** Lớp CRI tìm được chưa có full card ID; đổi cue chung có thể đổi luôn các thẻ khác của cùng người, trái yêu cầu. Chuỗi `commentaryName` đã dò trong engine thuộc dữ liệu đội (kề shorthand/formation), không phải trường tiếng đọc cầu thủ. Không thêm nút giả hoặc sửa nhầm dữ liệu. Cần xác định tiếp đường player→commentary với tài nguyên bình luận thực tế của bản Android.

Các kiểm thử trong validation/ chạy trên máy build: gateway đăng nhập/codec, Java HTTP/upgrade, Java bố trí/SWAP và giả lập ARM64 với hàm engine gốc. Đã đọc lại 36 mesh đầu mới, cả hai LOD, xác minh xương/weights; 246 LOD thân áo giữ bind pose; tài nguyên ảnh/material đọc lại bằng UEViewer. **Chưa kiểm chứng render/GPU, tiếng bình luận, băng cổ tay hiển thị, replay/cutscene hoặc độ mượt trên điện thoại.** Không coi kiểm thử host là bảo đảm 100% trên thiết bị.

Sau cài cập nhật, đóng hẳn và mở lại ứng dụng trước khi thử. Những lần chỉnh appearance/Transfer yêu cầu mở lại vẫn phải làm trước Enter Game. Khi kiểm tra ảnh mặc định mới, nếu trước đó tự nhập ảnh cho cùng thẻ thì bỏ override ảnh tự nhập nếu muốn xem ảnh đi kèm.
