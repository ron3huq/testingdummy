# 73 V16 — UI6

[Tải bản cập nhật MT Manager UI6, 42,2 MB](https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/73-v16-ui6/V25-73-UI6-Persistent-NativeSleeves-Y08-MT.zip)

Áp lên APK **73 V16 đã có V25/UI5**, giữ face/kits gốc đã áp trước đó. Gói này chứa `classes5.dex` và thư mục `assets`; không chứa save cá nhân.

## Cài bằng MT Manager

1. Xuất save dự phòng, giữ APK đang hoạt động.
2. Mở APK đang dùng và ZIP này. **Ghi đè `classes5.dex`, gộp toàn bộ thư mục `assets`**, thêm file mới và đè file trùng. Không chỉ chép riêng Python.
3. Ký bằng **đúng khóa MT đang dùng**, cài đè. **Không gỡ game, không xóa dữ liệu, không gỡ resource app.**
4. Đóng hẳn game và mở lại. File sửa được lấy từ APK/local gateway; không cần tải lại resource APK lớn.

Lần đầu cần xác minh tài nguyên; những lần sau dùng cache đã xác minh theo phiên bản, kích thước và thời gian sửa file. Save và cấu hình editor đang có được giữ.

## Sửa cơ chế mod đôi lúc không được nạp

Kiểm tra mã tìm thấy các đường khởi tạo có thể gây thiếu mod: lỗi cài hook làm dừng thử lại; mã giải gửi quá sớm bị bỏ qua; chờ thư viện quá thời hạn khi ở editor lâu; marker phiên bản giống nhau khiến gateway bỏ qua kiểm tra file. Đây là các lỗi có thể gây tình trạng bạn báo, chưa có log điện thoại để quy kết từng lần xảy ra.

UI6 kiểm tra/phục hồi43 file bất biến từ APK trước khi chạy Python, nhận biết hook của chính nó khi thử lại, giữ mã giải chờ thư viện, không hết thời hạn khi ở editor, và đợi các phần mod bắt buộc sẵn sàng trước LOGIN/chuẩn bị trận. Nếu khởi tạo không đủ thì ghi lỗi và chặn trả về bản gốc im lặng. Không ghi đè save hoặc cấu hình editor của người chơi. Những tài nguyên nền có cùng kích thước được giữ trên lần nâng cấp; các phần sửa quan trọng vẫn được kiểm tra hash riêng.

## Áo tay dài, HLV và face

- Bỏ nạp model áo xắn. Bốn thẻ `88044950524330`, `89135066911146`, `89136418985303`, `89136418985302` được đặt **tay dài native trên mọi kits**, không giới hạn Sparta/Telstar. Người khác giữ các chính sách trước đó. Giữ cấu hình băng trắng cổ tay trái đã có; mức độ nhìn thấy phụ thuộc tay áo native.
- Gỡ phần thay HLV Zidane/Sir Alex; phục hồi byte gốc của8 tài nguyên manager3D và hai ảnh thẻ. Bảng Coach và đường lấy coach không còn được sửa bởi bản vá. R. Martínez/Gattuso dùng dữ liệu gốc73; không xóa các thẻ HLV sở hữu hoặc cầu thủ Zidane.
- **Face Ronaldo2027:** `106734785925546` → `89138556572074`, dùng lại profileNX27.
- **Face Ronaldo2017:** `88044950524330` → `89136418985303`, dùng lại profileNV17.
- Hai thay đổi face là ánh xạ đúng thẻ sang tài nguyên khuôn mặt/tóc đã có; container face/kits đang hoạt động giữ nguyên byte, không tạo thêm texture face.

## Kits Y08

Thêm cấu hình áo theo đúng đường dẫn các đội Swiss/Y08, cùng170 tài nguyên texture/font/thumbnail sao chép từ CLB nguồn. MU/Real lấy hình áo lịch sử từ **gói chúng ta đã làm**, không lấy texture Telstar/AZ nguyên bản. Hai đội dùng MU2008/Telstar và Realbwin/AZ. Tám đội còn lại lấy áo CLB tương ứng trong73, gồm cả cấu hình màu/họa tiết của những đội dùng áo dựng chung. Không tự thiết kế áo mới.

CPK giữ nguyên101 file và ID file gốc, thêm33 cấu hình áo Y08 và8 cấu hình chữ/số áo.12 bố cục glyph được xử lý sẵn trong tài nguyên để bỏ hook giải nén toàn game. Menu Y08 chỉ liệt kê các slot có cấu hình thật, tránh thêm áo thứ ba không tồn tại. Mã đội để chọn đội hình vẫn là mã Y08, không đổi sang đội hình hiện đại của CLB nguồn.

**Giữ nguyên texture kits Real Madrid/Barcelona Y17 đã được bạn xác nhận.** Bố cục chữ/số sau giải mã của hai đội vẫn tương đương UI5; các font glyph giữ nguyên byte.

## Tra cứu ăn mừng và skill

**Chưa xác minh được0542,0571,0595 thuộc cầu thủ nào trong bộ73 này, nên chưa áp hai thay đổi ăn mừng có điều kiện.** Đã kiểm tra47 danh mục CPK trong APK, danh mục IoStore resource và các tên ăn mừng tìm được trong engine. Mã animation không mặc nhiên là giá trị preset: nativeparameter59 là GoalPerformance9bit(0–511), còn60 là MemorialCelebration7bit(0–127). Không gán trực tiếp các số lớn vào hai trường này. Điều này không chứng minh animation đó không nằm trong một khối dữ liệu khác. Xem [báo cáo ăn mừng](validation/celebrations-report.json).

Theo cấu hình exact-card đang áp, cả `89136418985303` và `89136418985302` có10 skill sẵn sau sửa ChopTurn → Long-reachTackle:

Scissors Feint; Heading; Knuckle Shot; Acrobatic Finishing; First-time Shot; Captaincy; Fighting Spirit; Penalty Specialist; Long-range Shooting; Long-reach Tackle.

Không tính5 ô AdditionalSkills. Xem [báo cáo skill](validation/skills-report.json).

## Hiệu năng và kiểm tra

Bỏ container áo xắn khoảng42MB khỏi danh sách nạp; bỏ model HLV bổ sung; bỏ hook theo dõi mọi lượt inflate; giảm một lượt tính OVR lặp cho NPC cổ điển; chia sẻ cache hash engine; giảm theo dõi nền từ1giây xuống10giây. Giữ cache editor, preview tĩnh và gộp yêu cầu vẽ của UI5. Đây là các giảm tải xác định từ mã, **chưa phải số đo FPS/RAM/GPU trên điện thoại**. Không giảm chất lượng face. Xem [kiểm tra hiệu năng](validation/performance-audit.json).

Các báo cáo trong `validation/` gồm: thực thi ARM64/accessor engine,23 kiểm tra API MyLeague với10 đội/cả hai phía, thử tay dài qua nhiều kits/slot/giải, đối chiếu hai face với nguồn qua đường nạp native mô phỏng, phục hồi nguyên bảng Coach, đọc lại142 file CPK và ID, kiểm tra170 tài nguyên áo, chạy helper phục hồi bằng JVM, kiểm tra DEX274 lớp và đối chiếu7379 mục manifest với APK nền/overlay.

**Chưa chạy trên Android/GPU điện thoại của bạn.** Cần kiểm tra trong trận: áo tay dài, face hai thẻ nhận, kits Y08 ở cả hai phía, hai HLV gốc và vài lần mở lại game. Không cam kết100% hiển thị hoặc hiệu năng trước kiểm tra đó.
