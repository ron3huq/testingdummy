# V25 for 73 V16 — Full Editor / UI1

[Tải gói cập nhật MT Manager](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-editor-ui/V25-73-Full-Editor-UI1-MT.zip)

Dùng với **APK 73 đang chạy được face V25**. Đây là gói cập nhật APK, không phải file save và không phải resource APK. Không dùng cho efootxi 1.3.2/1.4.0.

## Cài trên điện thoại

1. Giữ bản sao APK đang chạy và file `.efsave` đã xuất.
2. Trong MT Manager, mở APK đang chạy bằng chế độ xem ZIP. Mở gói cập nhật ở cửa sổ còn lại.
3. Chép **`classes5.dex`** và **gộp thư mục `assets`** từ gói vào gốc APK. Chọn ghi đè các tệp trùng; giữ các tệp assets khác của APK.
4. Ký APK bằng **đúng khóa MT đã dùng cho bản đang cài**, rồi cài đè. **Không gỡ game.** Giữ nguyên ứng dụng resource đang dùng. Nếu Android báo xung đột chữ ký, dừng và chọn lại đúng khóa.
5. Đóng hẳn rồi mở lại ứng dụng. Chạm vào màn hình nếu muốn ở lại launcher để dùng editor; sau 10 giây không tương tác ở launcher, ứng dụng sẽ gọi chức năng Enter Game gốc.

Không cần tải lại resource. Gói không chứa save của bạn và không thay cơ sở dữ liệu câu lạc bộ bằng save mẫu.

## Những gì có trong gói

- Giữ bộ face/card art V25 đang chạy và toàn bộ gói My League trước đó: sáu giải, đội hình, cầu thủ cổ điển, các quy tắc chỉ số, kỹ năng, kết quả và môi trường thi đấu.
- Hai thẻ `89136418985303`, `89136418985302`: tay áo dài; nạp lại cờ kỹ năng bẩm sinh đúng dữ liệu của hai thẻ trong save được cung cấp. Không đổi face sang một cầu thủ khác.
- Bốn đội mặc kits mới: 351 / 352 / 242 / 245. Giữ texture riêng và dùng cấu hình hiển thị của Real Madrid / Manchester United / Barcelona để xử lý phần tên áo và số quần. Việc hiển thị trên GPU điện thoại vẫn cần kiểm tra trong trận.
- Launcher xanh đậm/teal, nút Enter Game cao gấp đôi; launcher, Save Manager, Player Editor và Card Designer dùng tiếng Anh. Thêm 2.100 mục dịch cho nhãn và thông báo, giữ giá trị dữ liệu và callback gốc.
- Tự vào game sau 10 giây không tương tác. Chạm sẽ đặt lại thời gian; không tự vào khi đang giữ tay, mở hộp thoại/editor, xử lý tài nguyên, chưa xác nhận thông báo gốc, hoặc ứng dụng ở nền. Không có hiệu ứng chuyển động hay tác vụ đồ họa nền mới.
- Editor hiển thị/tìm theo tên đã đổi, gồm Nguyen Xuan Son và các thẻ đổi tên trong bộ V25.
- Mở một cầu thủ trong Player Editor → **Body & motion**: chiều cao 140–220 cm, cân nặng 40–130 kg, chân thuận, preset ăn mừng tương thích, tay áo; băng cổ tay trái/phải, băng cổ chân và găng cầu thủ thường. Phụ kiện có Keep original / Off / On, giữ màu gốc. Không có găng thủ môn.

Lưu Body & motion **trước khi Enter Game**. Thiết lập áp dụng theo ID thẻ, dùng chung cho các bản sao của ID đó; được lưu trong metadata của save và dựng lại khi khởi động. Không viết đè tiến trình tập luyện, kỹ năng bổ sung, đội hình hoặc dữ liệu gốc của cầu thủ.

## Giới hạn kiểm chứng

Đây là **bản cập nhật đã kiểm tra ở mức mã/API/ARM64, chưa chạy trên điện thoại của bạn**. Không thể khẳng định mọi phần hiển thị/animation hoạt động 100% chỉ bằng kiểm tra phía máy tính.

- Ăn mừng: bộ truy cập native của bản 73 chỉ lưu 7 bit ở ô tương ứng. Ví dụ ghi 212 sẽ đọc lại thành 84. Gói chặn giá trị vượt 127; danh sách dùng các preset tương thích có trong dữ liệu, không gán tên động tác chưa xác nhận. Cần xem animation trong trận.
- Ngoại hình trong biểu mẫu này gồm chiều cao/cân nặng, tay áo và bốn loại phụ kiện trên. Chưa có trình sửa toàn bộ khuôn mặt, cơ thể, giày hay mọi loại phụ kiện. Các mục thử nghiệm có sẵn của editor gốc không được coi là đã sửa hoặc bảo đảm hoạt động.
- Phần tên áo/số quần đã đổi cấu hình native và kiểm tra đường nạp; cần kiểm tra cả sân nhà/sân khách trên điện thoại để xác nhận kết quả render.

## Kết quả kiểm tra

- DEX đúng phiên bản 037 như bản gốc; checksum/signature hợp lệ, giữ các lớp gốc, thêm helper và không trùng phương thức.
- API My League bản 73: 19 kiểm tra qua khi cài lớp editor mới; giữ cấu trúc login/warehouse và không sửa dữ liệu nguồn.
- Bộ truy cập ARM64 nguyên bản: kỹ năng của cả hai ID đầy đủ 64 bit, chân thuận, chiều cao/cân nặng ở các biên cho phép, ăn mừng trong miền hợp lệ; giá trị sai bị chặn.
- Hook tạo ngoại hình: cả hai ID mới nhận tay áo dài và cấu hình phụ kiện; ID khác được giữ nguyên. Vector phụ kiện dựng bằng hàm native gốc, giữ màu và các phần tử khác, bỏ qua vector sai cấu trúc.
- Bốn kits: cấu hình trực tiếp và bản cache nhận đúng cấu hình đội hiển thị; giữ các byte lân cận và đường nạp texture riêng. Giữ các kiểm tra đội hình/cầu thủ cổ điển của bản trước.
- Editor: đọc/lưu/khôi phục thiết lập, từ chối giá trị sai, hoàn tác khi ghi lỗi; cơ sở dữ liệu cầu thủ và save nguồn được giữ nguyên.
- Bản dịch web: kiểm tra nhãn, thông báo động, placeholder và hộp thoại; giữ nguyên giá trị nhập và mã script.

Chi tiết trong `validation/`; danh sách file và SHA-256 trong `inventory.json`, `SHA256SUMS.txt`.

## Mã nguồn

`source/` chứa runtime Python/C, helper Java, bản vá Smali so với `classes5.dex` gốc và bảng dịch. Biên dịch native dùng Zig 0.13, aarch64-linux-musl; DEX dùng API 24 / định dạng 037. File game gốc và save người dùng không nằm trong mã nguồn phát hành.
