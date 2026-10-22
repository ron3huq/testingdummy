# My League Studio và runtime v16

App web tự chứa chạy trên Chrome/Edge ở Android hoặc máy tính. Không cần root, cài Python hay compiler để xuất gói chỉnh sửa. Dành cho bộ efootxi Android1.3.2 và libUE4.so đã được các bản hotfix trước xác minh; không tự tương thích các APK/engine khác.

## Tải và mở app

Giải nén MyLeagueStudio-v16-offline.zip, mở **MyLeagueEditor.html** bằng Chrome/Edge mới. Nếu MT Manager hiện mã HTML như văn bản, chọn mở bằng trình duyệt. Toàn bộ thư viện và runtime nằm trong một file HTML; không tải thư viện mạng hay gửi dự án lên server.

Đã kiểm tra giao diện Chromium qua HTTP cục bộ, viewport máy tính và390px, các thao tác chỉnh/xuất/nhập. Chính sách Chromium của môi trường kiểm thử chặn file:// nên chưa kiểm tra cách mở file HTML trực tiếp trên Android; file app không có tài nguyên mạng phụ thuộc. Nếu trình duyệt không hỗ trợ DecompressionStream, dùng Chrome/Edge hiện tại như thông báo trong app.

## Cầu thủ

Tìm tên hoặc dán **đúng Card ID**, chọn phạm vi tất cả My League hoặc một giải cụ thể. Mỗi bản thẻ lưu riêng. Thư viện gồm46.610 bản ghi ID/tên, với snapshot chỉ số khi có nguồn; không phải dữ liệu live đọc từ máy bạn.

- Chỉ số thành phần40–99. Ô không đổi không được ghi đè. Overall do game tính theo chỉ số, vị trí và các boost; app không giả mạo một số OVR độc lập.
- Thêm skill bằng ô chọn, xóa bằng nút **Xóa** cạnh skill (có thể buộc tắt cả skill do buff cũ thêm vào). Các skill khác giữ nguyên. Ánh xạ74 cờ kỹ năng đã đối chiếu native.
- Ngoại hình: chiều cao140–220cm, cân nặng40–130kg; tay dài, tay ngắn, theo dữ liệu gốc hoặc không ghi đè. Chưa chỉnh mesh mặt/tóc, hình khối cơ bắp hay tay xắn.

Bấm **Lưu cầu thủ**. Các ô hiển thị sẵn là snapshot nguồn, có thể khác buff hiện tại trong game. Thay đổi bạn nhập được áp dụng sau hệ thống buff/balance có sẵn. Phần này có thể áp dụng cho NPC hoặc thẻ của bạn bằng đúng ID trong My League; không thay thẻ, level hay kho sở hữu trong save.

## CLB/đội tuyển và chuyển nhượng

Chọn giải và đội trong76 đội thuộc năm giải tùy chỉnh. Phần này chỉnh **roster/đội hình CLB native, bao gồm đối thủ My League**, không thay đội Dream Team hoặc kho cầu thủ của bạn.

11 dòng đầu là đá chính; sau là dự bị. Có mẫu4-3-3,4-2-3-1,4-4-2,3-4-3 và kéo tự do trên sân. Chọn vị trí từng ô; mũi tên đổi cầu thủ giữa các ô. Thay cầu thủ bằng tìm tên/ID; thêm/xóa dự bị để có11–40 cầu thủ. Chỉ dùng ID có bản ghi trong game. Các cầu thủ hoàn toàn mới chưa có trong phiên bản này không được tự tạo chỉ bằng nhập một ID.

Đội trưởng và sáu vai trò phạt: xa, gần, người đá thứ hai, góc trái, góc phải, penalty. Phải thuộc đội chính. Số áo1–99 không được trùng trong đội. Bấm **Lưu đội hình**. Thay cầu thủ ở một đội không tự gỡ ở đội cũ; mở đội cũ và thay tương ứng nếu cần. App không xử lý hợp đồng/chuyển nhượng thẻ sở hữu trong save.

Với đội chưa có sơ đồ native đã xác minh trong nguồn, app ghi rõ đây là gợi ý biên tập. Không ghi mẫu vào game chỉ vì bạn mở đội; chỉ xuất sau khi bạn thực sự sửa/lưu. Các trường thông thạo vị trí gốc của cầu thủ được giữ nguyên.

## Thời tiết mới

Ngày8 nằm trong hai khoảng người dùng nêu; v16 ưu tiên mùa đông:

- Ngày1–7: mùa hè, có thể quang/mưa và sáng/tối.
- Ngày8–14: mùa đông, vẫn có thể quang/mưa và sáng/tối.
- Ngày15 trở đi: linh động mùa hè/đông.

Mặc định35% mưa,50% ban đêm,45% mùa đông sau khoảng cố định. Có thể đổi các ngày/tỷ lệ trong app. Cùng một trận giữ điều kiện ổn định khi mở lại; không đổi kết quả hoặc lịch thi đấu. Không bật tuyết. Chưa bật sương mù: enum nguồn xác minh có fine/rain/snow/random/none, chưa có fog hoặc đường điều khiển tương ứng đáng tin cậy. Thử nghiệm tay xắn Gullit đã bị tắt cả trong cấu hình và native.

## Xuất để dùng MT Manager

1. Trong app, mở **Xuất & nhập → Xuất ZIP để chép vào game**. Không cần cài bản runtime mặc định trước; mỗi file ZIP xuất đã có toàn bộ runtime v16.
2. **Buộc dừng game**. Sao lưu bộ file hiện có trong `files/embedded-gateway/work/tools/`.
3. Giải nén ZIP vừa xuất. Chép toàn bộ **9 file trong `install/work/tools/`** đè vào thư mục trên; không tạo nhầm `tools/tools`.
4. Mở lại game, vào đúng My League và một trận mới để nạp nhân vật/đội hình.

9 file: gateway_runtime.py, select_team_runtime.py, libselect_team.so, myleague_realism.py, myleague_worlds.py, myleague_balance.py, myleague_custom.json, **myleague_editor_runtime.py**, **myleague_editor.json**. Không thay dt200, CPK, APK hoặc SQLite/save.

Nếu chỉ muốn thời tiết mới và tắt thử Gullit trước, dùng efootxi-1.3.2-native-hotfix-v16-editor-weather.zip. Gói này để trống sửa cầu thủ/đội hình. App cũng bắt đầu với cấu hình trống đó; không kèm các giá trị thử nghiệm trong quá trình kiểm tra.

## Lưu và nhập dự án

App lưu các sửa đổi đã bấm Lưu trong trình duyệt. **Tải dự án JSON** để sao lưu/chuyển máy. Nhập lại file myleague_editor.json để sửa tiếp. Không nhập myleague_custom.json cũ, vì đó là cấu hình nền đã ghim với thư viện native.

Mỗi dự án tối đa1.024 cấu hình cầu thủ và128 cấu hình đội. Nếu trình duyệt không cho localStorage, app báo và bạn vẫn có thể tải JSON/ZIP. Muốn phục hồi, buộc dừng rồi chép đủ bộ file sao lưu. Muốn bỏ riêng sửa editor, xuất lại dự án trống hoặc cài ZIP runtime mặc định v16.

## Kiểm tra sau khi cài

Mở files/embedded-gateway/work/tools/select-team-status.json sau khi vào My League:

- version: native-hotfix-v16.
- editor_error:null và editor_status.ready:1 nghĩa là dự án đã được nạp.
- editor_status.player_applies/team_applies tăng khi đường game đọc đối tượng có chỉnh.
- editor_team_results: mã1 là đã ghi đội;0 là chưa đọc trong phạm vi hiện tại;13 là một cầu thủ không giải được trong database native;31 là vượt dung lượng snapshot cache. Không ghi dở đội khi preflight thiếu người.
- editor_status.last_error_id là ID lỗi gần nhất; failures là bộ đếm tích lũy, không tự xóa sau một lần thành công.

Các native_team_results cũ thuộc hệ thống mặc định; với đội bạn cấu hình trong editor, xem editor_team_results. Mã14 của roster mặc định trước đây không bị bỏ kiểm tra đại trà; roster editor tường minh được kiểm tra toàn bộ các ID mới trước khi thay.

myleague-environment-status.json chứa mùa, weather, time_zone và fixture đã chọn. Bộ đếm chỉ xác nhận thực thi, không chứng nhận ảnh trên điện thoại đã đúng.

## Kiểm chứng và giới hạn

Đã chạy thao tác trên Chromium: sửa chỉ số/cơ thể/skill, chặn số áo trùng, đổi người, kéo vị trí, đội trưởng/phạt đền, xuất ZIP, lưu trình duyệt và nhập lại JSON. ZIP thực tế từ app được kiểm tra CRC, đủ9 file và khớp runtime.

Đã nạp chính JSON do app xuất qua API C trong Unicorn và đọc lại bằng hàm ARM64 gốc: chỉ số, skill, chiều cao/cân nặng và biên giới hạn; tay dài/ngắn; bốn biến thể đội hình, số áo, đội trưởng/sáu người đá phạt; truy vấn lặp không cộng dồn; rời phạm vi khôi phục các field/cached team. Thiếu một ID khiến toàn bộ phần ghi đội bị chặn. Kiểm tra gateway loại bỏ skill học thêm và giữ nguồn đầu vào, native/cached/entry-crash/appearance/regression/weather đều qua.

Một số boundary DB/resource/libc được mô hình hóa; chưa kiểm tra trực tiếp runtime editor mới, chiều cao/cân nặng hoặc kết quả thời tiết/hình ảnh trên điện thoại. V14 tay dài là phần đã được người dùng xác nhận trước đó. Mã mô phỏng kết quả v10 giữ nguyên byte; lịch và kết quả đã lưu không bị viết lại. Tài nguyên mesh/mặt/tóc hoặc cầu thủ không tồn tại trong engine nằm ngoài khả năng gói editor này.
