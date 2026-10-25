# UI7 FULL — Earth Edition cho 73efootball V16

Tải **cả hai file**, áp vào cùng APK 73 V16. Đây là một bộ FULL chia làm hai ZIP có đường dẫn không trùng nhau; không cần áp V25/UI1–UI6 trước.

- [Part 1 — Faces, 88,3 MiB](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip)
- [Part 2 — Main, 15,0 MiB](https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/73-v16-ui7/V25-73-UI7-FULL-Part2-Main-MT.zip)

## Sửa trong UI7

- Bổ sung đầy đủ ba file `pc9298` và bộ nạp Python đã sửa. UI6 trước đó là bản tăng thêm, nên áp riêng lên APK gốc mới cài sẽ thiếu gói này. Bản FULL đã kiểm tra đủ toàn bộ thay đổi so với manifest APK gốc.
- Giao diện launcher màu xanh không gian, Trái Đất và sao tĩnh, nút Enter lớn. Không video, không tải ảnh mạng, không hiệu ứng chạy liên tục. Trái Đất dùng chung một bitmap 384×384 (~576 KiB); giữ các thao tác gốc và bộ đếm tự vào game sau 10 giây không chạm.
- Trong **Edit Player → Appearance & Motion → Height & Weight**, sửa chiều cao 140–220 cm và cân nặng 40–130 kg. Chỉ đọc khi bấm mở; lưu trên luồng nền, chỉ đổi hai thông số tương ứng. Cần sửa trước khi Enter Game; nếu đã vào game, đóng và mở lại ứng dụng trước khi sửa. Thay đổi ngoại hình áp theo đúng ID thẻ, kể cả các bản sao cùng ID.
- Tìm tên không cần dấu, ở cả danh sách cầu thủ đang sở hữu và Player Catalogue: `kaka` → `Kaká`, `muller` → `Müller`, `joao felix` → `João Félix`, `dang van lam` → `Đặng Văn Lâm`. Tên hiển thị giữ nguyên. Vẫn tìm được ID và nhiều từ kết hợp.
- Catalogue chuẩn hóa khóa tìm một lần trên luồng nền, dùng lại chỉ mục; hủy lượt tìm cũ khi gõ tiếp, chỉ hiện kết quả của lượt mới nhất. Không quét dữ liệu chiều cao/cân nặng khi tìm cầu thủ.

## Các phần cũ được tích hợp

Giữ toàn bộ trạng thái UI6: face V25 và hai phép sao chép face đúng ID; My League Y08/Y17 và các giải đã sửa; đội hình, phân cấp, số áo/vai trò; bộ kits, font số/tên và logo; ngoại lệ chỉ số cho thẻ của người chơi; skill hai thẻ Ronaldo custom; giao diện tiếng Anh và sửa Card Designer.

Bốn Ronaldo `88044950524330`, `89135066911146`, `89136418985303`, `89136418985302` dùng **áo dài tay gốc**, đã bỏ kiểu xắn tay. Giữ cấu hình băng cổ tay trái. Hai HLV Zidane/Sir Alex đã được gỡ và phục hồi dữ liệu HLV gốc như yêu cầu mới nhất. Không đưa trở lại Body & motion/Height–skills nặng của các bản cũ.

Hai face alias vẫn là `106734785925546` → `89138556572074` và `88044950524330` → `89136418985303`. Các ID ăn mừng 0542/0571/0595 chưa xác minh được ánh xạ trong engine73 nên không tự gán sai.

Các thư viện native, tài nguyên kits/face và logic My League giữ nguyên byte so với UI6; báo cáo cũ ở [73-v16-ui6/validation](../73-v16-ui6/validation). Phần mới có báo cáo riêng trong [validation](validation).

## Cách áp bằng MT Manager

1. Export save trong Save Manager trước khi cài APK đã sửa. Giữ APK gốc và file save đã xuất.
2. Dùng APK **73efootball V16** làm nền. Mở Part 1, chép thư mục `assets` vào **gốc APK**, hợp nhất và thay các file trùng đường dẫn.
3. Mở Part 2, chép `assets` và `classes5.dex` vào **gốc cùng APK**, thay file trùng. Phải áp xong **cả hai phần rồi mới ký APK**. Không chép nguyên file ZIP vào game.
4. Ký APK bằng key MT đã dùng cho bản đang cài, rồi cài đè nếu chữ ký khớp. Nếu Android báo xung đột chữ ký, hãy kiểm tra đã xuất save thành công trước khi tính đến gỡ bản đang cài; chữ ký APK gốc và chữ ký MT không thể cài đè nhau.
5. Giữ/cài resource APK V9. Nếu vừa cài game sạch, hoàn thành nhập tài nguyên V9 rồi vào game. Hai ZIP này chứa đầy đủ **bản mod**, không thay thế toàn bộ resource APK của game.
6. Trong launcher mới phải thấy dòng **UI7 Earth**. Không áp lại bản vá cũ lên UI7 vì có thể ghi đè mã mới.

Cơ chế trước khi khởi động kiểm tra và phục hồi 45 file mod bất biến từ chính APK, gồm gói pc9298. File lớn đã xác minh được dùng cache theo phiên bản/kích thước/mtime; không giải nén lại toàn bộ mỗi lần mở. Save và cấu hình chỉnh sửa của người chơi không bị cơ chế này ghi đè.

## Đã kiểm tra và giới hạn

Đã chạy kiểm tra đóng gói trên 7.380 dòng manifest so với APK gốc; đủ nguồn cho 45 file mod bất biến; thử cài sạch ở mức file, xóa pc9298, làm hỏng mã và phục hồi bằng Java helper thật; kiểm tra giao dịch SQLite/rollback, cache editor, lưu lại chiều cao/cân nặng, và đọc lại bằng accessor ARM64 gốc. Kiểm tra tìm kiếm Unicode, lọc/sắp xếp/hủy kết quả và fixture 50.000 thẻ trên máy chủ. DEX giữ đủ 267 lớp gốc, không đóng gói nhầm các lớp stub dùng khi biên dịch.

Chưa chạy trực tiếp trên điện thoại/GPU Android, nên không khẳng định FPS hay cam kết không lag trên mọi máy. Các kiểm tra giả lập ARM64 và kiểm tra JVM không thay cho thử trận đấu thực tế.

SHA-256 của hai ZIP nằm trong [SHA256SUMS.txt](SHA256SUMS.txt).
