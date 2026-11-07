# FULL8 RC24 · ba mặt Ronaldo và Event v25

FULL tích lũy nền FULL8 RC7 → RC22 → RC23, áp lên APK v19.1 bằng MT Manager. Không chứa APK, engine, save cá nhân hoặc Blend. Bản ứng viên chưa thử trên điện thoại.

## Mặt và ID

- `106783356083208`: Ronaldo 2007 từ ZIP người dùng xác nhận.
- `88043608522885`: Ronaldo JUVE 2020 từ ZIP người dùng xác nhận.
- `89138556572074`: tiếp tục sửa Ronaldo2027 đang có.

Hai mặt PC đã chuyển thành asset Android, giữ bề mặt/tóc của nguồn, retarget rig mặt vào skeleton thân native. Mỗi mặt có sáu palette da và bốn biến thể. Giữ bộ xương/bind pose thân native, bone map LOD gần/xa 19/6; vùng cổ có trọng số nhất quán giữa LOD. Không sửa chiều dài tay.

Ronaldo2027 giữ mọi đỉnh bề mặt, UV và tangent RC23; chỉ giảm đáp ứng cục bộ các bone hàm/môi/khóe miệng, thêm lớp niêm mạc tối phía sau mép tiếp xúc. Vẫn có chuyển động hàm/môi, mắt và lông mày. Khoang miệng, răng và lưỡi đều tối theo yêu cầu mới nhất; sửa phản xạ da đầu/cổ, cân palette đầu/thân. Không đổi đèn toàn sân. Tài nguyên mới R9D/R7A/R0A trong pc9432..9503, revision19024, tránh dùng lại cache tên cũ.

## UCL và World Cup

Giữ hai giải ở Event Mode, giao diện/nhóm/lịch/bracket v25, knockout một trận. Không có runtime RC21/two-leg, không biến thành giải My League. Mặc định mới LEGEND; giữ lựa chọn thủ công sau đó.

Thêm Ghi bàn, Kiến tạo, MOTM và Edit vào panel giải, tái sử dụng font/card/pill/crest của panel gốc. Trận chơi lấy sự kiện từ báo cáo engine, tách penalty quyết định thắng thua; chống cộng đôi theo game ID. Trận AI được mô phỏng vẫn dùng kết quả gốc của v25; các sự kiện cầu thủ được sinh cùng lúc mô phỏng và lưu trong trận, có nhãn AI simulation. MOTM chỉ lấy cờ engine, không bịa MOTM AI. Trận cũ chỉ có tỉ số không thể phục hồi chính xác tên người ghi bàn/kiến tạo; giao diện báo thiếu dữ liệu. Bắt đầu giải mới để có thống kê đầy đủ từ đầu.

Edit dùng đúng Transfer Edit hiện có, phạm vi đội UEFA122 và quốc gia128, cùng dữ liệu lưu và menu sửa đội/cầu thủ. Bổ sung dữ liệu đội hình công bố của v25 cho các đội/cầu thủ còn thiếu trong catalog cũ. Đội hình, số áo, đội trưởng, người đá phạt, thông số/skill được áp vào packet Event và native context tương ứng. Đây là chỉnh sửa đội dùng chung cùng phạm vi Transfer, không tạo bản sao mùa My League. Giữ cơ chế an toàn của editor: **lưu chỉnh sửa trước Enter Game; nếu engine đã nạp, đóng hẳn và mở lại app rồi sửa**. Không hỗ trợ đổi trực tiếp giữa trận.

## Cách áp bằng MT Manager

1. Sao lưu APK/save. Mở bản sao APK v19.1 đang dùng.
2. Chép đè toàn bộ `assets/` và `classes5.dex` từ gốc ZIP FULL vào gốc APK, giữ assets khác của APK nền.
3. Lưu và ký bằng đúng khóa đang dùng, cập nhật đè. Không cần xóa data.
4. Đóng hẳn game và mở lại. Đổi palette da cũng cần khởi động lại để đầu/thân cùng nạp cấu hình.
5. Kiểm tra cả ba ID lúc nghỉ, nói/ăn mừng, camera gần/xa, cổ/da dưới đèn sân; chơi thử Event, bảng ghi bàn/kiến tạo và chỉnh đội trước Enter Game.

Dùng trọn FULL này, không trộn thư viện/manifest riêng từ gói cũ. Artifact GitHub là một ZIP FULL phẳng, có assets và classes5.dex ngay ở gốc.

## Mức kiểm chứng

Host đã đọc lại mesh/texture cooked, kiểm tra bone map/bind pose/LOD, ray thử miệng nghỉ và pose tổng hợp, thực thi selector ARM64 bằng giả lập, kiểm tra vòng đời hai giải và chỉnh sửa đội bằng fixture, biên dịch Java/DEX và chuỗi checksum/LOGIN. Báo cáo RC24 nằm trong validation; các báo cáo RC22/23 chỉ là lịch sử.

**Chưa chạy engine Android hoặc thử trên điện thoại.** Không khẳng định môi hết xuyên trong mọi clip thực tế, tay/LOD không lỗi trên mọi máy, hoặc màu da trùng tuyệt đối dưới mọi ánh sáng. UI Android mới đã biên dịch/kiểm tra cấu trúc nhưng chưa thao tác trên thiết bị. Cần kiểm tra thực tế các điểm trên trước khi coi là bản hoàn thiện.
