# V20 — 14 thẻ mặt và 4 đội nhận kit

Đây là **bản dựng chưa được xác minh trên điện thoại**. Đã chạy kiểm tra mã ARM64, kiểm tra asset và mở lại bằng UEViewer. Những kiểm tra đó **không chứng minh renderer Android đã hết mặt đen**. Không coi `HOOK_ACTIVE` hoặc `head_material_confirmed` là bằng chứng hình ảnh đã đúng.

## Chép gói

1. Buộc dừng efootxi Android 1.3.2.
2. Giải nén `Faces-v20-14-cards-4-teams.zip`.
3. Gộp và chép đè **cả `work/` và `livedata/`** vào `files/embedded-gateway/` bằng MT Manager. Hai thư mục phải nằm trực tiếp trong `embedded-gateway`, không nằm trong một thư mục phiên bản khác.
4. Mở lại game. Không xóa save hoặc dữ liệu ứng dụng. Gói cần hotfix v18 mà bạn đã xác nhận có.

Chỉ có **một gói cài**. ZIP source là mã và tài liệu nghiên cứu, không chép source vào game.

## Mặt và lỗi đen

Bốn thẻ lỗi được dựng lại thành các asset mới:

| Thẻ | ID đầy đủ | Profile riêng mới |
|---|---|---|
| Ronaldo 2017 | 88044950524330 | NW01 |
| Ronaldo 2027 | 106734785925546 | NW27 |
| Ronaldo Jr | 105765448873424 | NWJR |
| Nguyen Hoang Duc | 105643042189511 | NWHD |
| Mesut Ozil, thay Guler | 106778792700170 | NWOZ |

Nguồn 2017/2027 vừa gửi có model `face_high.fmdl` trùng SHA-256 với nguồn trước. Bản này thực sự dùng các tệp mới đó, nhưng thay đổi quan trọng nằm ở bước chuyển đổi:

- Dùng topology phần da, UV, tangent và **từng byte skin weight của từng LOD** từ ND06 mà người dùng đã xác nhận hoạt động trên bốn thẻ lỗi khi đối chiếu.
- Chuyển hình dáng mặt từ từng nguồn tương ứng qua ánh xạ tam giác trong UV; giữ cổ dưới đã làm mượt và đóng các đường nối trùng vị trí. Đây là bước chuyển topology, hình dáng có thể khác nhẹ nguồn PC tại các vùng có mật độ lưới khác nhau.
- Giữ geometry tóc riêng từ nguồn từng cầu thủ, không dùng tóc 2006 chung cho cả bốn thẻ.
- Dùng texture mặt của nguồn tương ứng, giữ normal/SRO và cách đóng gói của ND06. Mắt và phần trong miệng dùng 135 đỉnh Android, rig mắt/hàm native; chỉnh vị trí mắt và khoang miệng theo nguồn.
- Giữ skeleton 166 xương, khối inverse bind native, RequiredBones LOD0=166 và LOD1=153, giới hạn palette mobile và tổng weight byte=255. Không hứa có đủ mọi biểu cảm PC.
- Những đầu đã được duyệt, bao gồm 2006/2013/2008 và các cầu thủ Việt Nam khác, giữ nguyên asset mặt/tóc. Có 187 chunk đầu/tóc cũ được đối chiếu byte.

Log v19 cho biết mesh phụ thực tế là `SK_002d01`. Đã xuất và kiểm tra: đó là mesh cơ thể, không phải một đầu dự phòng để ẩn. Không mở rộng lệnh ẩn sang mesh này.

**Nguyên nhân GPU chính xác của lỗi đen vẫn chưa được chứng minh.** V20 là thay đổi cấu trúc asset có kiểm soát, không phải lời xác nhận lỗi đã hết trên thiết bị.

## Áo đấu

| Đội trong game | Team ID | Home | Away/p2 |
|---|---:|---|---|
| Sparta Rotterdam | 351 | Real Madrid 2017 trắng | Real Madrid 2017 xanh, nguồn third đã dùng ở v19 |
| Telstar | 352 | Manchester United 2007 đỏ | Manchester United 2007 xanh |
| AZ | 242 | Real Madrid 2011 trắng | Real Madrid 2011 đen/vàng |
| sc Heerenveen | 245 | Barcelona 2017 xanh/đỏ | Barcelona 2017 xanh ngọc |

Đổi đúng tám texture áo và 16 ảnh xem trước menu, gồm ảnh áo đơn và ảnh toàn bộ kit. Không thay áo thủ môn hay áo của các đội khác. Ảnh menu được chiếu từ atlas PES sang bố cục UI riêng; không kéo nguyên atlas vào ảnh menu.

Font chữ và số, kích thước, cách bố trí và đường dẫn tài nguyên gốc được giữ nguyên. Chỉ đổi màu RGB của atlas chữ/số để đọc được trên áo mới. **Các block alpha EAC gốc được giữ từng byte ở mọi mip**, tránh làm mất nét chữ/số khi nén lại. Với áo trắng dùng chữ tối; áo tối dùng màu sáng phù hợp. Vẫn cần kiểm tra tên và số thực tế trên điện thoại.

Trên áo vẫn dùng tên viết hoa đầy đủ đã được đồng ý: `XUAN SON`, `DINH BAC`, `HOANG DUC`, `HOANG HEN`, `QUANG VINH`, `TAI LOC`, `ISHOWSPEED`, `RONALDO JR`; Özil dùng `OZIL`. Tên giao diện dùng cách viết thông thường. Özil đổi tên thành `Mesut Ozil` và quốc tịch Đức; giữ CLB/giải của thẻ Güler gốc. Mã quốc tịch Đức 210 đã đối chiếu bằng getter native và bảng Country, không dùng mã hình cờ 23 để ghi vào record.

## Vị trí và chỉ số

- Ronaldo 2017: vị trí chính LWF; chỉ LWF thông thạo đầy đủ.
- Ronaldo 2006 và 2008: vị trí chính RWF; chỉ RMF và RWF thông thạo đầy đủ.
- Chỉ bốn thẻ 2017/2006/2008/2027 được đặt 17 chỉ số tấn công, kỹ thuật và thể chất trong khoảng **92–96**: nhận thức tấn công, rê bóng, kiểm soát bóng, giữ bóng chặt, dứt điểm, hai loại chuyền, đánh đầu, sút phạt, độ xoáy, tốc độ, sức mạnh cơ thể, thăng bằng, lực sút, tăng tốc, bật nhảy, thể lực.
- Giữ nguyên chỉ số phòng ngự, quyết liệt, gắn kết phòng ngự và thủ môn; không đặt tuổi, chiều cao, cân nặng, chân yếu hay kỹ năng vào khoảng 92–96.
- Dùng lớp editor v18 để áp dụng sau bước cân bằng rating, đồng thời phản ánh các tham số vào API project. Hiển thị cuối cùng trong những màn hình/hiệu ứng tăng cường khác vẫn cần đối chiếu trên máy.

Đã đối chiếu toàn bộ corpus cầu thủ để xác nhận thứ tự tham số thông thạo: `CF,SS,LWF,RWF,AMF,DMF,CMF,LMF,RMF,CB,LB,RB,GK`. Thứ tự này khác enum vị trí chính. Mức 2 là thông thạo đầy đủ, mức 0 là không thông thạo. Báo cáo: `position-parameter-evidence.json`.

Giữ chính sách tay dài cho 2017/2006/2013/2008 và Messi đã yêu cầu; 2027 vẫn tay ngắn.

## Ảnh thẻ

Thay sáu cặp ảnh: Ronaldo 2017, 2006, 2008, 2013, Özil và Tài Lộc. Ảnh lớn **184×256**, miniface **128×128**; hai bố cục riêng, giữ tỷ lệ khuôn mặt. Giữ lần hoán đổi ảnh 2006/2008 mà người dùng đã yêu cầu trước đó. Không vẽ sẵn rating, tên, quốc kỳ, CLB hay khung vào ảnh chân dung — game vẫn dựng các lớp UI đó.

Ảnh Tài Lộc gốc tìm thấy trong `pc9261`, không phải `pc1000/pc1001`. Đã dùng đúng package native để thay ảnh. Ảnh Özil và Tài Lộc được dựng từ model mặt người dùng cung cấp; các ảnh Ronaldo dựa trên ảnh người dùng gửi.

**Nền hiện là mẫu tự thiết kế theo phong cách Big Time, không phải tệp nền gốc mới nhất 2026/2027 đã được xác minh.** Các texture nền tách riêng trong dữ liệu kiểm tra phần lớn là placeholder 1×1; chưa có nguồn để xác nhận mẫu mới nhất. Xem `Card-layout-preview.png` trước khi cài.

## Quốc tịch/CLB và log

Giữ sáu thẻ Việt Nam ở quốc tịch Việt Nam, không hiện CLB/giải trong các bản sao dữ liệu UI được xử lý; Speed là Bồ Đào Nha/Al Nassr. Bổ sung bộ chuyển đổi UI `0x3883248` với đủ 10 đối số, vì bộ `0x38809bc` ở v19 không được gọi theo log điện thoại. Chưa có xác nhận hình ảnh UI mới trên máy.

Log: `files/embedded-gateway/work/tools/noodle-hair-status.json`.

Bản đúng phải ghi `player-faces-v20-source-topology-kits`. Đối với bốn đầu sửa, trường mới `last_redirected_asset_path` phải chứa `SK_NW01/NW27/NWJR/NWHD`; Özil là `SK_NWOZ`. `last_face_id` và `last_face_profile` vẫn ghi Face ID/profile **gốc**, không phải profile private. `last_asset_path` cũng là đường dẫn đầu vào gốc; dùng trường mới để xem đường dẫn sau chuyển. Các counter mới gồm `extended_card_builder_calls`, `extended_card_last_id`, `position_card_changes`, `position_last_card`.

Hãy đối chiếu riêng bốn thẻ lỗi ở gameplay, cận cảnh, replay và cutscene; đồng thời kiểm tra tên/số áo và menu chọn kit. Nếu còn lỗi, ảnh/video kèm log v20 và đúng Card ID sẽ phân biệt được asset mới đã được tải hay chưa. Không cần chép cả thư mục game.

`device_verified` giữ `false`: công cụ hiện tại không kết nối renderer Android để tự kiểm tra hình ảnh. `gateway_runtime.py` vẫn đúng 2441 byte, cơ chế manifest/checksum/idempotence giữ nguyên, revision tăng 38 khi đổi payload.
