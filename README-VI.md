# V19.1 FULL-1 — Private Football

Gói tích hợp dành riêng cho **73efootball-V19.1.apk** tại release `releasee`. APK gốc có SHA-256 `9c0b249557eeab1543ce143af4d08269b6e9a5a965472242815dba5712c76469`. V20.2 chỉ là nguồn đối chiếu và nguồn thẻ Ronaldo 2017. Không áp gói này vào V16 hoặc V20.2.

## Cài bằng MT Manager

1. Sao lưu save bằng chức năng Export Save hiện có.
2. Mở APK **V19.1**. Trong ZIP này, mở thư mục bọc ngoài nếu tải từ GitHub.
3. Chép **assets/** và **classes5.dex** vào gốc APK, thay thế các file trùng. Ký APK một lần bằng **cùng khóa bạn đang dùng** và cài cập nhật. Giữ bộ tài nguyên game hiện có; không gỡ game hoặc xóa dữ liệu.
4. Không áp chồng Part/UI V16 cũ. `README-VI.md`, `validation/`, `extras/` và các báo cáo không chép vào APK.

Lần đầu cần để game cập nhật tài nguyên mới. Các chỉnh sửa native thực hiện trước Enter Game; lưu rồi đóng/mở lại ứng dụng theo hướng dẫn của từng mục.

## Nội dung

- Giữ giao diện WebView V19.1, sắp lại thành năm tab. Abilities ở tab khả năng; preferred foot/weak foot/injury resistance ở tab vị trí; innate skills ở tab kỹ năng; ngoại hình, model, copy model, equipment, màu phụ kiện, motion, skin, celebration và card art ở Appearance & Motion. Giữ mục boots của V19.1. Dùng các hộp chỉnh native cho các công cụ chuyên sâu.
- Launcher chỉ có lựa chọn tiếng Anh, bỏ lựa chọn ngôn ngữ và liên hệ tác giả; khóa zoom launcher. Giữ zoom cần thiết để căn ảnh trong trình crop. Có nút Diagnostics. UI asset lấy từ APK mới, tránh trộn cache giao diện cũ.
- Catalogue có giỏ chọn, tiếp tục chọn thẻ trước khi Add selected to storage. Giữ save manager và các chức năng V19.1.
- Chuyển toàn bộ payload V16/UI7.19 tích lũy, trừ Part3 đã hủy. Giữ các face/kits, ảnh, editor, level100, kỹ năng, nhiều thẻ cùng cầu thủ và cấu hình trước đó. Gộp trên dữ liệu V19.1; không thay nguyên protected runtime V19.1 bằng bản V16.
- Transfer chỉ gồm UEFA Champion League122, World Nation League128, Y08473 và Y17518. Giữ chọn formation, swap, đội hình, số áo, vai trò và kits. Dùng roster có capture native hoặc cấu hình đội cổ điển đã có; nếu chưa có snapshot thì giao diện yêu cầu vào game một lần, không tự đoán đội hình. Bản này dùng roster/order cùng thứ tự và bỏ lớp trả con trỏ GamePlan clone chưa đủ tin cậy.
- 41 file công thức kits được ghép lên CPK V19.1; các file V19.1 không liên quan được giữ nguyên byte.
- Hook ngoại hình V19.1 được giữ và nối tại đúng một entry đã xác minh. Hook lạ hoặc khác prologue bị từ chối. Không cài hai hook ghi đè nhau tại entry đó.
- Live Update công bố manifest của bộ tích hợp trước bước kiểm tra tương thích V19.1; giữ kiểm tra SHA, kích thước và giới hạn đường dẫn. Version tăng khi nội dung đổi và ổn định khi đăng nhập lại không đổi; cache không được chọn làm nguồn nội dung thay APK/SQL của bản cố định này. Đã thử đổi ảnh rồi đăng nhập lại với codec version native.
- Mini và Large dùng hai crop độc lập. Giữ pipeline mip/alpha đã sửa, và gửi cập nhật ảnh về editor sau khi lưu. Ưu tiên ảnh local trước ảnh CDN, giữ tải ảnh theo hàng đợi giới hạn. Tách nền vẫn theo worker của trình ảnh, không chạy khi chỉ tra cứu cầu thủ.

## Ba thẻ gốc

| ID thẻ | Face mod gốc | Xử lý |
|---|---|---|
|89136418985332|56334|Đưa nguyên thẻ Ronaldo2017 từ V20.2 vào catalogue V19.1: payload147 parameters, skills, metadata, boosters, design donor89133724764840 và ảnh9500031; không tự cấp một bản owned. Chọn trong catalogue để thêm vào storage.|
|89136418985320|56331|Giữ face gốc mod của V19.1.|
|89136418985303|56323|Bỏ override face NV17 cũ để dùng đúng face gốc mod; không lấy đầu4522.|

Payload thẻ332 được đối chiếu bằng dictionary đầy đủ với nguồn, không chỉ sao chép OVR. Tài nguyên face/ảnh mới giữ nguyên byte nguồn.

## Wukong

Chuyển các fur card còn gắn material mặt sang material dùng atlas râu và tăng mật độ. Áp dụng cả bốn biến thể mesh. Giữ vị trí đỉnh, chiều dài/khung ngoài và skin weights; giữ skeleton/bind data166 xương. Container đã được đọc lại và bốn mesh được xuất bằng UEViewer độc lập, so sánh skeleton với nguồn. Không tiếp tục sửa Joker hoặc các đầu khác. `extras/` có Blender và ảnh góc nhìn Wukong để tham khảo; shader Blender là bản xem trước.

## Kiểm chứng và giới hạn

`validation/` có báo cáo boot V19.1 thật trên máy build, tám nhóm API editor, thẻ332 đúng nguyên payload, integrity/manifest, đăng nhập lại sau import ảnh, crop trong Chromium, launcher/nút bridge/giỏ, liên kết DEX, ARM64 Transfer qua các consumer native, và kiểm tra mesh độc lập.

**Chưa chạy trực tiếp trên Android/GPU.** Các kiểm tra trên không bảo đảm tuyệt đối không crash hoặc không lag trên mọi điện thoại. Cần xác nhận trong trận/replay, đặc biệt phần hiển thị đội hình sau Transfer và phụ kiện. Các giới hạn V16 cũ vẫn giữ: SOUND cho từng thẻ chưa triển khai; copy motion chỉ gồm các trường đã kiểm chứng, không khẳng định chuyển được mọi signature animation khóa theo danh tính. Mức chỉ số127 là giới hạn lưu, không phải cam kết hiệu quả gameplay vượt mọi cap.
