# 73 V16 — UI5

[Tải bản cập nhật MT Manager UI5, 77,5 MB](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui5/V25-73-UI5-Fixes-MT.zip)

Áp lên APK 73 V16 đã có V25/UI4. Giữ face, My League, đội hình, tên cầu thủ, giao diện tiếng Anh và tự Enter sau 10 giây không chạm. Không chứa save cá nhân.

## Cài đặt

1. Xuất save dự phòng, giữ APK đang chạy tốt.
2. Trong MT Manager, mở APK đang dùng và ZIP này. Chép `classes5.dex`, gộp toàn bộ thư mục `assets` vào gốc APK; thêm tệp mới và đè tệp trùng.
3. Ký bằng **đúng khóa đã dùng cho APK đang cài**, rồi cài đè. **Không gỡ game, không xóa dữ liệu hay gỡ resource app.** Nếu báo xung đột chữ ký, chọn lại đúng khóa.
4. Đóng hẳn game rồi mở lại. Các gói sửa được nhập từ APK trên máy; không cần tải lại resource APK lớn.

Lịch/kết quả mùa đang chơi được giữ. Mùa Swiss cũ có 12 đội cần bắt đầu mùa Y08 mới để nhận lịch 10 đội; không xóa save toàn game.

## Thay đổi

- **Kits:** giữ nguyên kits Real Madrid và Barcelona Y17 theo xác nhận của bạn. Sửa chọn áo toàn bộ 10 đội Y08 bằng lịch đấu và phía người chơi, thay vì mã đội tạm thời trong phản hồi. MU Y08 dùng Telstar352; Real Y08 dùng AZ242; tám đội còn lại dùng kits CLB tương ứng. Giữ nguyên 40 tài nguyên chữ/số áo từ UI4.
- **Tay áo:** dựng lại từ mẫu tay ngắn native, giữ toàn bộ da tay, UV, vertex colors và bảng bone. Phần vải kéo dài được ôm theo mẫu tay dài. Không truyền mã model giả cho bộ nạp, không ép mesh chi tiết vào đường nạp LOD thấp. Chỉ bốn thẻ Ronaldo `88044950524330`, `89135066911146`, `89136418985303`, `89136418985302` trên hai kits Sparta351/Telstar352, slot0/1. Mẫu không hỗ trợ giữ hành vi native.
- **Băng cổ tay:** chính sách riêng cho bốn thẻ trên: băng trắng **cổ tay trái của cầu thủ**, tắt bên phải. Áp cả trước khi editor khởi tạo; thay cờ sleeve lúc dựng ngoại hình để phụ kiện không bị đường áo dài che mất. Suarez và cầu thủ khác giữ nguyên.
- **HLV:** đã port mô hình từ gói Zidane/Sir Alex vào đúng tài nguyên manager3D native của Martínez/Gattuso, gồm hai LOD, skeleton và bảng bone của manager gốc. UI4 chỉ có ảnh thẻ; UI5 bổ sung mesh trong trận. Ảnh thẻ được căn theo mẫu128×128, giữ tỉ lệ.
- **Chỉ số:** đăng ký đầy đủ ID thẻ sở hữu để bỏ qua hạ chỉ số đối thủ trong Y08/Y17, cả đường native và START. Giữ progression/boosters và dữ liệu save; không sửa trực tiếp save người dùng.
- **Skill:** bổ sung tên tiếng Anh khi bộ lấy nhãn native trả rỗng; hai thẻ Ronaldo custom dùng phạm vi trang skill riêng. Không thay cờ skill chỉ để làm hiện chữ. Giữ sửa Chop Turn → Long-reach Tackle đã có.
- **Giao diện:** bỏ hoàn toàn mục Height / skills và Body / motion khỏi DEX/khởi tạo editor. Hộp sửa cầu thủ giới hạn theo màn hình, dành chỗ cho nút dưới. Card Designer có bố cục hẹp/ngang, ô nhập co giãn, nút44px và cache phiên bản mới; giữ gộp yêu cầu vẽ và không vẽ liên tục khi đứng yên.
- **Logo:** sáu bộ logo riêng cho Y08, Y17, UEFA, Asia-Pacific, World Nations, AFC; đúng các cỡ native64/128/256 với lề trong suốt. Không thay tài nguyên logo quốc gia chung.

## Kiểm tra

Báo cáo trong `validation/`: chạy ARM64 với accessor engine gốc, bảo vệ thẻ sở hữu và khôi phục chỉ số qua đổi giải; START cho10 đội Y08 × hai phía; kiểm tra25 prologue bắt buộc và25 prologue khai báo trực tiếp; giải nén bằng zlib engine thật; kiểm tra1.443.317 đỉnh ở356 model × hai LOD; xuất đọc lại mẫu manager/body, thử skinning CPU khuỷu0–120°;40 glyph giữ nguyên;18 logo đúng cỡ. Card Designer tải/lưu/chuyển tab ở320×640,430×900,760×360, không tràn ngang hoặc repaint liên tục khi đứng yên. Manifest đối chiếu APK nền và overlay; face container pc9298 cùng17 ánh xạ giữ nguyên.

**Chưa thử trực tiếp trên điện thoại Android/GPU của bạn.** Kiểm tra thành phần không chứng minh hết lỗi animation, xuyên bề mặt hoặc hiệu năng thực tế. Cần xác nhận trong trận: tay áo khi chạy/ăn mừng, băng tay trái, đầu HLV, nhãn skill và kits Y08 ở cả hai phía. Đây không phải cam kết100% hình ảnh/hiệu năng.
