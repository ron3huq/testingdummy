# UI7.6 Earth — 73 V16 Part 2 Main

Áp ZIP này vào gốc APK đang có UI7.5 và Part 1 Faces, ký cùng khóa rồi cài đè. Không gỡ game hoặc xóa dữ liệu. Nếu bắt đầu từ APK 73 V16 gốc, cần cả Part 1 Faces UI7 và Part 2 UI7.6; resource V9 vẫn là tài nguyên nền riêng.

## Thay đổi

- Real Madrid Y08 (4937): giữ nguồn áo bwin/AZ242 đã có, bật đúng cờ đọc recipe realUni. Cờ của Real gốc109 không thể dùng làm nguồn vì đây là CLB không có license trong bảng gốc. Chỉ sửa trường hợp4937; các đội Y08 khác và kits Y17 giữ nguyên.
- Player Model: hiển thị các số gốc từ bảng PlayerAppearance hiện có, theo ID chính xác hoặc base ID của thẻ; ghi rõ khi không tìm thấy. Giá trị15 trong bảng nghĩa là mặc định native, hiển thị7. Các giá trị đã tùy chỉnh vẫn hiển thị riêng. Thêm áp dụng lại11 trường float sau builder để tránh nhánh model base đưa chúng về trung tính. Không sửa bit mặt/tóc/đầu hoặc các chỉ số khác.
- Chỉ thẻ89138556572074 chuyển sang tay ngắn. Bốn Ronaldo đã yêu cầu tay dài vẫn giữ nguyên.
- Catalogue: nhấn thẻ đưa vào Cart, giữ nguyên tìm kiếm và màn hình catalogue. Mở Cart để xem, chạm tên để bỏ lựa chọn, rồi Add to Storage để gọi tính năng thêm thẻ gốc lần lượt. Nếu một lần thêm thất bại, các mục chưa thêm được giữ trong giỏ; không thêm lại những mục đã thành công. Giỏ chỉ thuộc lần mở catalogue hiện tại, không lưu qua đóng ứng dụng.
- Nhiều Ronaldo: mã gốc e186_cr_stats.validate_cristiano cấm hai thẻ cùng người4522 và gây lỗi khi lưu squad. UI7.6 bỏ giới hạn theo người, vẫn kiểm tra duplicate instance và giữ nguyên kiểm tra ownership/serial trong player_identity. Không đổi ID cầu thủ, không giả phản hồi thành công khi save thất bại.

## Bảng ăn mừng

[celebration-card-map.csv](celebration-card-map.csv) có286 giá trị Goal Performance và32 giá trị Memorial Celebration, với một ID thẻ nguồn cho mỗi giá trị đã tìm thấy ở parameter59 (Goal Performance) và60 (Memorial Celebration). Quét toàn bộ46.623 bản ghi Player bằng bộ chuyển đổi ARM64 gốc82aa124 rồi đọc bằng accessor gốc82a84d4. Ưu tiên ID thẻ variation dài khi có.

Đây là giá trị trong dữ liệu cầu thủ, không tự khẳng định số đó bằng tên clip animation hay mô tả một động tác cụ thể. p59 lưu9 bit, p60 lưu7 bit; không gán trực tiếp542/571/595 vì chúng vượt miền lưu tương ứng. Những clip chưa xác minh được chủ sở hữu không được gán tên đoán.

## Kiểm tra và giới hạn

Kèm kiểm tra ARM64 cho cờ áo Real, sửa riêng tay ngắn, giá trị body sau builder; kiểm tra actual protected identity validator tái hiện lỗi stock và chấp nhận hai thẻ Ronaldo đã sở hữu trong khi từ chối duplicate/unowned; kiểm tra manifest/hash/DEX và đăng nhập gateway73.

Chưa chạy trực tiếp trên điện thoại. Giỏ hàng đã biên dịch và nối vào dialog catalogue trước khi show, nhưng chưa có kiểm thử UI Android trên thiết bị. Tác động model và render áo vẫn cần xác nhận trong game; không cam kết100% mọi thiết bị.
