# 73 V16 — UI2 Fast Catalogue + Ronaldo cuffs

[Tải gói cập nhật MT Manager](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui2/V25-73-UI2-Fast-Catalogue-Ronaldo-Cuffs-MT.zip)

Dùng cho **APK 73 đã chạy được face V25**. Gói giữ face/card art, My League và các kits hiện tại; thay bản UI1 bằng bản sửa này. Không dùng cho efootxi 1.3.2/1.4.0.

## Cài

1. Giữ bản sao APK đang chạy và save đã xuất.
2. Mở APK bằng MT Manager. Chép **`classes5.dex`** và **gộp toàn bộ `assets`** từ ZIP vào gốc APK: thêm tệp mới, ghi đè tệp trùng và giữ các assets khác của APK.
3. Ký bằng **đúng khóa MT đang dùng**, rồi cài đè. **Không gỡ game; giữ nguyên ứng dụng resource.** Nếu báo xung đột chữ ký, chọn lại đúng khóa thay vì gỡ ứng dụng.
4. Đóng hẳn và mở lại app. Không cần tải lại gói resource lớn. Bộ mesh mới được nạp từ tài nguyên cục bộ của bản cập nhật khi vào game lần đầu.

Gói lớn hơn UI1 vì có mesh tay áo riêng và toàn bộ tài nguyên Card Designer để thay đồng bộ, gồm các ảnh có sẵn trong APK gốc. Không có save hoặc cơ sở dữ liệu cá nhân trong gói.

## Các thay đổi

- **Bỏ Body & motion hoàn toàn khỏi giao diện và đường đọc dữ liệu.** Loại các lớp/nút/callback thêm ở UI1; không còn đọc metadata body cho từng cầu thủ. Khi khởi động, dọn các ô body do tính năng này ghi vào cấu hình native; giữ đội hình, thời tiết và các thiết lập khác. Không xóa hoặc thay cơ sở dữ liệu save.
- **Sửa nguyên nhân catalogue chậm:** UI1 sao chép bảng 46.465 tên trong mỗi lần tra tên; catalogue có 14.394 thẻ nên công việc bị lặp rất nhiều. UI2 dùng lại một bảng đã đổi tên. Cùng bản sao save, trên máy kiểm tra: **15,47 giây → 0,316 giây**, khoảng 49 lần nhanh hơn. Đây không phải số đo trên điện thoại.
- **Reading local save:** bỏ lớp body projection và truy vấn thừa theo từng cầu thủ; dùng lại kết quả đọc khi save không đổi. Cache tự hủy khi sửa cầu thủ, đổi/khôi phục save hoặc có ghi dữ liệu từ kết nối khác. Gateway gốc vẫn xử lý việc mở lại hoặc phục hồi save. Chuỗi đã là tiếng Anh đi thẳng qua, không chạy qua hàng loạt biểu thức dịch tiếng Trung.
- **Hai thẻ `89136418985303`, `89136418985302`:** thay Chop Turn bằng Long-reach Tackle trong cờ kỹ năng native và dữ liệu gửi vào game/editor. Giữ các kỹ năng khác, kỹ năng bổ sung và tiến trình tập luyện.
- **Card Designer:** thay đồng bộ HTML/CSS/JavaScript và thư viện assets bằng cùng một phiên bản. Dời bước dịch DOM sau khi trang khởi tạo, giữ bridge Android và các thao tác gốc. Nếu vẫn có lỗi khởi tạo, màn hình báo tệp/lỗi cụ thể thay cho dòng Reload chung chung.
- Giữ launcher tiếng Anh, nút Enter lớn và cơ chế tự Enter sau 10 giây không tương tác của bản trước.

## Tay áo và băng cổ tay: giới hạn chính xác

Chỉ bốn ID sau nhận tay áo xắn và băng cổ tay theo yêu cầu:

| Thẻ | ID |
| --- | --- |
| Ronaldo 2017 | `88044950524330` |
| Ronaldo 2006 | `89135066911146` |
| Ronaldo custom | `89136418985303` |
| Ronaldo custom | `89136418985302` |

**Tay áo:** mép vải tới khoảng giữa cẳng tay, có phần gập ở cổ tay áo; chỉ dùng với kits **Real Madrid 2017 trên Sparta (351)** và **Manchester United 2007/08 trên Telstar (352)**, ở hai slot áo đang thay. Mỗi mesh dùng tên riêng trong container `pc9299`; không ghi đè mesh chung. Da cánh tay, UV, skeleton và bind pose của mesh nền được giữ lại; chỉnh trọng số và normal/tangent ở phần tay áo để theo chuyển động cánh tay. Cầu thủ khác mặc hai kits này vẫn dùng áo tay dài bình thường. Bốn thẻ mặc kits khác giữ đường nạp mesh gốc.

**Băng cổ tay:** băng trắng ở **tay trái**, tắt băng tay phải cho đúng bốn ID trên, theo mẫu băng quấn bạn chỉ định ở thẻ Suárez `88033139394625`. Giữ các phụ kiện khác; không thay thẻ Suárez hay các cầu thủ khác. Băng cổ tay áp dụng cho bốn thẻ ở các kits khác nữa.

## Kiểm tra và giới hạn

- DEX 037 hợp lệ; giữ các lớp gốc, bỏ toàn bộ lớp/callback Body & motion. Các nút và thao tác gốc vẫn dùng API gốc.
- API đọc/editor: alias được dùng lại; cache phản ứng với sửa dữ liệu, ghi từ kết nối khác và mở lại save. Save nguồn và các hàng cầu thủ được giữ nguyên.
- My League: giữ 19 kiểm tra API của sáu giải, kết quả, đội hình và dữ liệu serialize gốc.
- ARM64: kiểm tra kỹ năng, policy cổ tay, cả hai hook body mobile; thử đầy đủ ID/kit/slot và trường hợp gần giống ID. Chỉ bốn ID trên với hai kits/slot cho phép được chuyển sang mesh riêng; các tham số của trường hợp khác được giữ nguyên.
- 25 điểm hook khớp engine 73 gốc; không trùng 15 hook của bộ face đang chạy.
- Mesh: 356 biến thể riêng, mỗi biến thể giữ hai LOD. Đọc/xuất lại bằng UE Viewer các mẫu 2015b07, 2015e07, 2015b02, 2123e07; so sánh phần da, chỉ mục, UV, skeleton và bind matrices. Biến thể nguồn không được chuẩn bị sẽ giữ đường nạp native.
- Card Designer: Chromium giả lập màn hình điện thoại, cả có/không có bridge Android giả lập; mở, tải/lưu dự án và chuyển tab đều qua, không thiếu asset hay lỗi JavaScript.

**Chưa chạy bản này trực tiếp trên điện thoại/GPU của bạn.** Hình dáng mép áo, băng cổ tay và chuyển động thực tế vẫn cần xem trong trận. Các phép thử mã/reader không thay cho kiểm tra render trên điện thoại; không khẳng định hoạt động 100% trên mọi máy.

Face native library, runtime và container `pc9298` được giữ byte-identical với bản đã hoạt động. Không có yêu cầu root hoặc USB.

Mã nguồn trong `source/`, kết quả trong `validation/`; `inventory.json` và `SHA256SUMS.txt` dùng kiểm tra gói tải về.
