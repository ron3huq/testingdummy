# FULL8 RC23 · sửa tiếp Ronaldo2027 trên nền RC22

Gói FULL tích lũy để áp lên APK v19.1 bằng MT Manager. Giữ Event UCL/World Cup của RC22; không thay giao diện, luật giải, My League hay dữ liệu cầu thủ. Giữ nguyên sửa tay/LOD mà người dùng đã xác nhận ổn.

## Ronaldo2027 · ID89138556572074

- Tăng tiếp xúc cục bộ hai mép môi khi nghỉ, thêm tối đa 0,9 mm so với RC22. Giữ số đỉnh/tam giác, UV, toàn bộ trọng số và cấu hình LOD/xương. Không khóa hàm, không sửa chiều dài tay, không xê dịch răng/lưỡi/cổ/tóc. Tangent/normal được xoay theo bề mặt môi mới.
- Khoang miệng, lớp lót, nướu và lưỡi có albedo gần đen, giảm phản xạ/occlusion riêng; răng được giữ sáng màu ngà, tách khỏi phần mô tối. Đây là xử lý texture/SRO của riêng mặt này, không thay đèn sân hoặc shader toàn game.
- Cân lại màu nền da đầu/cổ theo sáu palette thân gốc, giảm mảng màu má/trán lệch nhau, giữ chi tiết da/râu và màu môi. Đọc lại texture ETC2 sau nén để đo màu từng vùng.
- Sửa tham chiếu material: ba biến thể `ep00v0313`, `ep01v0291`, `lg00v0000` trong RC22 vẫn gọi material mặt RG28 cũ. RC23 chuyển tất cả biến thể sang material mặt R9C đúng palette. Material tóc giữ nguyên.
- Tài nguyên mới `R9C1..R9C6`, container `pc9408..9431`, revision 19023; không ghi đè tài nguyên R9B đang có. Tên mới giúp tránh dùng lại cache tài nguyên cũ khi khởi động lại.

## Cách áp FULL bằng MT Manager

1. Sao lưu APK và save đang dùng. Không cần gỡ game hoặc xóa data.
2. Mở bản sao APK v19.1 của bạn, chép đè toàn bộ `assets/` và `classes5.dex` từ ZIP FULL vào gốc APK; giữ các assets khác của APK nền.
3. Lưu, ký bằng đúng khóa đang dùng rồi cập nhật đè.
4. Đóng hẳn game và mở lại. Khi đổi palette da, cũng đóng và mở lại để đầu/thân nạp cùng cấu hình.
5. Kiểm tra Ronaldo2027 lúc đứng yên, há miệng/ăn mừng, ánh sáng sân và khoảng cách camera. Không trộn thư viện/manifest riêng từ các gói cũ vào FULL này.

Nếu đã áp RC22, vẫn dùng trọn FULL RC23 theo các bước trên. Trong artifact ZIP, `assets/` và `classes5.dex` nằm ngay ở gốc, không cần tải thêm gói vá nhỏ.

## Mức xác nhận

Kiểm tra host đọc lại đủ 24 asset: giữ cấu trúc/UV/trọng số/bone map/LOD của RC22, kiểm tra tên và phụ thuộc material, màu da sau nén, mô miệng tối/răng sáng. Kiểm tra mô phỏng góc nhìn khi nghỉ/hé hàm và khi há lớn; thực thi selector ARM64 bằng trình giả lập; kiểm tra chuỗi checksum/LOGIN và từng tệp FULL.

**Chưa chạy bản này trên điện thoại/engine Android.** Những pose thử không tái hiện toàn bộ clip ăn mừng và ánh sáng game, nên chưa khẳng định hết hở ở mọi animation hoặc màu da trùng tuyệt đối dưới mọi đèn. Các báo cáo RC22 cũ giữ để truy nguồn; báo cáo RC23 trong `validation/` là kiểm tra của lần sửa mặt này.

Thống kê Event AI/đối thủ vẫn chưa đầy đủ như giới hạn RC22. Không chứa APK, engine, save cá nhân hoặc Blend.
