# eFootball73 V16 · UI7.9 FULL

Bản áp tích lũy, phát hành ngày **27/10/2026 (Việt Nam)**. Dành cho **eFootball73 V16**, không dùng cho efootxi. Bản full gồm hai phần dưới đây; APK73 và Resource73 gốc vẫn là thành phần riêng.

- **[Part1 Faces — tải tại đây](../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip)** (giữ nguyên gói đã kiểm tra).
- **[Part2 Main UI7.9 FULL — tải tại đây](V25-73-UI7.9-FULL-Part2-Main-MT.zip)** (tích lũy thay đổi Main từ các bản trước và face/tài nguyên mới).
- [Ảnh xem trước Hulk/Spider-Man](previews/hero-cards-preview.png) · [Ba ảnh Ronaldo](previews/ronaldo-layout-preview.png) · [SHA256](SHA256SUMS.txt).

## Cách áp

1. Sao lưu save bằng Save Manager nếu đang có save cần giữ.
2. Dùng MT Manager, chép **nội dung cả Part1 và Part2 vào cùng một APK73 V16**; chọn thay thế các tệp trùng tên. Không chép nguyên tệp ZIP vào APK. Không chồng tiếp Main UI7.6/7.7/7.8 sau Main7.9.
3. Ký APK bằng **đúng khóa đang dùng**, rồi cài đè. Không cần gỡ game hay xóa dữ liệu. Nếu bắt đầu từ APK73 sạch, vẫn cần bộ Resource73 gốc.
4. Mở ứng dụng, kiểm tra tiêu đề **UI7.9 Earth**. Chỉnh trong Player Editor **trước khi bấm Enter Game**. Sau khi lưu màu/model/appearance, đóng hẳn rồi mở lại app để game nạp cấu hình mới. Khi tải tài nguyên chưa xong, dùng Check & Repair Resources.

Nếu máy đã có đúng Part1 Faces trước đây thì chỉ cần cập nhật Part2 Main. Hai phần có đường dẫn không chồng nhau; các face mới được đưa vào container riêng trong Main, không thay gói face cũ.

## Những phần mới

- **Hulk:106754901843130**, **Spider-Man:105647605587130**. Chỉ thay đúng hai full cardID; hai thẻ vốn là Lukaku, các thẻ Lukaku khác được giữ. Mô hình, UV và vật liệu từ hai gói Android trial người dùng gửi; chuyển sang tên tài nguyên riêng NHUL/NSPD để tránh va chạm với face cũ. Không dùng thư viện native của bản efootxi trial cho bản73.
- Theo yêu cầu mới **tự tạo ảnh**, ảnh thẻ/miniface của hai nhân vật được dựng từ chính mô hình3D nói trên rồi ghép nền Avengers được thiết kế riêng. Không dùng hai ảnh hiển thị trong chat làm ảnh nguồn và không nhận là ảnh cắt nguyên từ chúng. [Nguồn dựng ảnh](hero-art-provenance.json), [kích thước/căn khung](hero-card-layouts.json). Đây là ảnh minh họa offline, không phải ảnh chụp Android.
- Hulk mặc định có màu thân người **#4e5b37, RGB78,91,55**. **Appearance & Motion → Skin · RGB Colour** có sáu palette gốc với mẫu màu đo từ texture game, sáu mẫu custom, ô HEX và ba thanh RGB0–255. Mẫu palette chỉ minh họa albedo; ánh sáng trong trận có thể làm màu nhìn khác.
- Custom RGB tạo texture Skin/Body/Lowbody riêng, giữ alpha gốc, không đổi độ trong suốt hay body mesh. Không ép RGB về palette gần nhất. Tối đa64 màu custom khác nhau, dùng chung được cho tối đa1024 hồ sơ thẻ tính cả Hulk mặc định. Chọn Original để bỏ ép màu. **Texture khuôn mặt riêng giữ màu của face**, vì thế chọn RGB không đồng nghĩa tô lại mọi khuôn mặt. Hulk đã có mặt xanh trong tài nguyên nguồn.
- **Edit Level** cho phép đặt giới hạn và level tới **100 cho mọi loại thẻ**, bao gồm Trending/Highlight. Nút chọn nhanh giới hạn50/100. Không tự nâng toàn bộ cầu thủ lên100 khi cài; người dùng tự chỉnh từng thẻ. Không tự cấp điểm ngoài progression; thử nghiệm level100 cho198 điểm, giữ nguyên Additional Skills.
- Ba thẻ **89138556572074,88044950524330,89135066911146** dùng ba ảnh trong IMAGE.RAR, giữ tỉ lệ, ảnh lớn184×256 chứa trọn tư thế, miniface128×128 căn riêng phần đầu. Dùng style nền game của Maldini **88045755960770**; giữ ảnh cầu thủ, không đưa ảnh Maldini vào.
-11 ảnh mod cũ (Xuân Sơn, Đình Bắc, Speed, Ronaldo2013, Özil, Hoàng Hên, Ronaldo2008, Tài Lộc, Quang Vinh, Ronaldo Jr, Hoàng Đức) đổi sang style nền **89137214427270**. Giữ nguyên các khối màu ETC2 của ảnh cầu thủ, chỉ xử lý alpha nền; không dựng lại khuôn mặt.

## Giữ các sửa đổi trước

Kits Y08/Y17 và cờ licensing Real Y08; đội hình/phân cấp My League; không áp trần chỉ số AI cho đội người chơi; phục hồi HLV gốc; face alias Ronaldo2027/2017; áo ngắn riêng89138556572074 và áo dài các thẻ Ronaldo đã yêu cầu; giỏ Player Catalogue; cho nhiều thẻ cùng cầu thủ trong đội; tìm kiếm không dấu; Player Model;64 tên skill và chỉnh innate hiện có; Additional Skills; chọn Main/Memorial celebration; Earth UI; sửa nạp tài nguyên, private CPK và đăng nhập. Các file triển khai các phần này được so sánh với UI7.8 để tránh thay đổi ngoài phạm vi.

**Physics vẫn được bỏ. Chiều cao140–220cm, cân nặng40–130kg**, giữ giới hạn đã phục hồi ở UI7.8. [Danh sách ID ăn mừng có tìm kiếm](celebration-ids.html) · [CSV](celebration-ids.csv): giữ318 nhóm,1.544 dòng, tối đa6 thẻ mỗi nhóm khi dữ liệu có đủ; không tự gán542/571/595 thành ID tham số khi chưa có bằng chứng.

## Kiểm tra và phạm vi xác minh

- [Package](package-validation.json): ZIP/CRC, đầy đủ manifest cho APK sạch, SHA của runtime/tài nguyên, DEX giữ267 lớp gốc,357 lớp sau bổ sung, không có save cá nhân, Part1/Part2 không trùng đường dẫn.
- [Native](native-features-validation.json): chạy thư viện ARM64 và một số hàm gốc73 qua Unicorn; phạm vi đúng hai thẻ hero, các thẻ Lukaku khác không đổi; body RGB không chuyển hướng head/body mesh, alpha giữ nguyên; style nền và ảnh đích độc lập. Ranh giới renderer/allocator được mô phỏng khi cần.
- [RGB](rgb-validation.json): đọc lại toàn bộ mip trong ba nhóm texture, lưu/đọc SQL, rollback khi ghi lỗi, URL tài nguyên ổn định và kiểm tra cache. Ba template BGRA cũng được đọc/export độc lập bằng UEViewer.
- [Level100](level-validation.json): dùng progression gốc để lưu/đọc lại level100,198 điểm, từ chối101, giữ Additional Skills.
- [Login](login-validation.json): gateway73 thực khởi tạo, CMD_LOGIN mã hóa trả NOERR, khôi phục CPK gốc không ghi đè CPK mod riêng; các bước chỉ dành cho Android được mô phỏng trên host.
- [Face dependencies](hero-dependencies.json): đủ12 phụ thuộc ngoài của22 package hero, không trùng ID package gốc; tám biến thể mesh được export độc lập. Không thay skeleton/cấu trúc nguồn để làm ảnh thẻ.

**Chưa kiểm thử trực tiếp trên điện thoại/renderer Android**, nên không cam kết tuyệt đối về màu dưới mọi ánh sáng, material trên mọi thiết bị hay độ trễ thực tế. Tìm kiếm/index cũ được giữ; UI tải lựa chọn theo yêu cầu, tạo texture ở luồng nền, không truy vấn SQL hoặc xử lý ảnh mỗi khung hình. Hai hook mới vẫn nằm trong trang RX4KB đang dùng:42×96=4032 byte, không thay allocator đã sửa lỗi loading.
