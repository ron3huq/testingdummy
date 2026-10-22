# v18 — Đồng bộ đội hình từ game vào web editor

Bản này sửa dữ liệu nền của editor. Không thêm ghép tóc, mặt hoặc chỉnh hình thể.

## Vì sao v17 không khớp

Web v17 không đọc điện thoại. Một số đội dùng roster tĩnh và sơ đồ suy ra; số áo được tự điền khi thiếu. Các đội cổ điển dùng cấu hình mod biên dịch, cũng không phải ảnh chụp đội hiện tại trên máy bạn. Vì vậy không thể coi các danh sách đó là đội hình đang có trong game.

v18 bỏ các đội hình suy đoán khỏi màn hình chỉnh đội. Chỉ mở đội đã nhập từ file đọc trong game, hoặc dự án biên tập do bạn chủ động nhập lại. Đội chưa đọc có thông báo rõ, không tự đặt người/số áo/vai trò thay thế.

## Lần đầu: lấy dữ liệu đang có trên điện thoại

1. Tải **efootxi-v18-lineup-readback-update.zip**. Buộc dừng game và sao lưu work/tools cùng myleague_editor.json hiện tại.
2. Chép **10 file** trong install/work/tools/ của ZIP cập nhật vào files/embedded-gateway/work/tools/. ZIP này **không chứa myleague_editor.json**, nên giữ nguyên dự án đang dùng. Runtime đọc được dự án v17 hiện tại.
3. Mở game → My League → mở đội hình/đối thủ muốn chỉnh. Dữ liệu được ghi thụ động khi game tra cứu record đội hoặc mở cache đội vào trận; không gọi hàm engine từ trình xuất Python. Chưa mở đội thì file có thể chưa có đội đó. Có thể cần mở màn hình trước trận để game đọc cache đội.
4. Chờ khoảng2 giây. Dùng MT Manager chép file **files/embedded-gateway/work/tools/myleague-live-teams.json** ra Download. Nếu chưa có, kiểm tra myleague-snapshot-error.txt và select-team-status.json, version phải là native-hotfix-v18.
5. Tải app **MyLeagueStudio-v18-offline.zip**, giải nén, mở MyLeagueEditor.html bằng Chrome/Edge.
6. Tab **Đội hình & chuyển nhượng → Nhập file myleague-live-teams.json**, chọn file vừa chép. App hiện số đội đã đọc; đội thiếu không được dựng từ mẫu. Không cần gửi file lên mạng.
7. Chọn đúng giải/CLB. Tên cầu thủ/ID, số áo, đội trưởng và người đá phạt được nối theo danh tính cầu thủ, không lấy số thứ tự cũ làm danh tính. Dữ liệu nhập chưa tự trở thành ghi đè; chỉ Lưu khi thật sự chỉnh.

## Chỉnh và xuất lại

- Có **bốn biến thể sơ đồ**, lấy riêng từ native. Dropdown dùng tên trung tính Khối1/2, sơ đồ1/2 vì chưa gán nhãn tấn công/phòng ngự cho mọi chế độ UI. Chỉnh biến thể nào thì giữ các biến thể khác.
- Kéo tọa độ hoặc đổi vị trí; sơ đồ mẫu chỉ áp dụng khi bạn bấm nút. Mũi tên đổi cầu thủ giữa các ô, giữ hình học của ô.
- Vai trò tham chiếu Card ID. Giá trị native255 được hiển thị **Chưa gán**; không ép một người đá phạt vào chỗ trống. Vai trò trỏ người dự bị được giữ như dữ liệu đã đọc.
- Dự bị không có ô chiến thuật trên sân; app hiển thị dự bị và vị trí chính nguồn nếu có. Không tự biến tất cả dự bị thành GK.
- Số áo đọc nguyên bản. Nếu snapshot có số0/trùng, app hiển thị đúng dữ liệu đó nhưng yêu cầu sửa về số hợp lệ trước khi lưu; không tự chọn số mới. Ưu tiên snapshot NATIVE_MATCH_CACHE nếu cần kiểm tra số mà game dùng ở trước trận.
- Bấm Lưu đội hình → Xuất & nhập → Xuất ZIP. ZIP do app xuất chứa **đủ11 file**; buộc dừng và chép đủ11 file vào cùng thư mục tools để áp dụng dự án vừa chỉnh.
- Khi đổi đội hình trong game về sau, chép và nhập lại file snapshot mới. Đây là bản đọc tại thời điểm được game tra cứu, không phải kết nối trực tiếp liên tục giữa web và điện thoại.

## Phạm vi và kiểm tra

Hỗ trợ76 CLB/đội tuyển thuộc5 giải tùy chỉnh hiện tại; chỉ ghi đội đã quan sát được. File có teams và errors: đội dùng kiểu player key khác native base, số lượng/formation không hợp lệ bị từ chối thay vì đoán.

Đây là roster CLB/native dùng cho đối thủ My League. Đội DreamTeam sở hữu, số áo riêng và gameplan lưu của tài khoản là đường dữ liệu khác; không coi snapshot CLB là bản sao của DreamTeam.

Các dự án v16/v17 nhập lại được và mang nhãn dự án đã lưu, không mang nhãn dữ liệu trực tiếp. Nếu muốn bắt đầu từ đội mới nhất trong game, bỏ ghi đè của đội đó trong app để dùng snapshot đã nhập.

Đã kiểm tra Chromium và native ARM64 với dữ liệu thử cố ý đảo thứ tự roster, khác cả bốn sơ đồ, số áo riêng, người đá phạt255 và đội trưởng dự bị. Đã đọc lại kết quả qua bộ tiêu thụ sơ đồ ARM64 gốc. Chưa có file snapshot từ điện thoại bạn để đối chiếu, nên chưa khẳng định mọi đội trên máy bạn đã khớp. Hai ZIP app và cập nhật được kiểm tra hash/CRC sau khi đưa lên GitHub.
