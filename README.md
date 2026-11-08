# Tải FULL8 RC25 cho APK v19.1

**[TẢI GÓI FULL8 RC25](https://github.com/ron3huq/testingdummy/actions/runs/42439862743/artifacts/13601456391)**

GitHub Actions đã dựng thành công và kiểm tra đủ **1.983 tệp**. Đăng nhập GitHub để tải artifact; hạn lưu30ngày. Đây là ZIP FULL tích lũy, có `assets/` và `classes5.dex` ở gốc, không cần tải delta trong `_ci`.

Mở **UCL Event Edit**, **World Cup Event Edit**, **Match Settings** trên giao diện ngoài trước Enter Game. Nút Transfer cũ giữ nguyên. Giữ pool v25 và tên/logo Ajax hiện tại. Chưa thử trên điện thoại.

Các tệp được kiểm tra bằng `payload-inventory.json`. Checksum ZIP GitHub có thể khác ZIP cục bộ vì cách đóng ZIP; nội dung payload đã được so khớp từng tệp.

# FULL8 RC25 · Event Edit riêng, hệ thống UCL v5 và setting v18-fixed

FULL tích lũy để áp lên APK v19.1 bằng MT Manager. Nền RC24/RC7, không chứa APK, engine, save cá nhân hoặc Blend. Chưa chạy bản này trên điện thoại.

## Event Edit tách khỏi My League

Giao diện ngoài có ba lối vào mới: **UCL Event Edit**, **World Cup Event Edit**, **Match Settings**. Nút Transfer cũ và các mục UEFA/World/Y08/Y17 của nó vẫn giữ nguyên.

Hai Event Edit dùng đúng giao diện Transfer đang có, tái sử dụng cùng mã xử lý, nhưng có instance, catalog, project và khóa lưu riêng. UCL Event dùng native context901, World Cup Event902; My League vẫn122/128. Không lấy đội/cầu thủ đã sửa của My League làm đội hình Event. Không chuyển mùa, bảng xếp hạng hoặc lịch của My League sang Event. Chỉnh ở một bên không ghi đè bên kia; hai Event cũng tách nhau.

Chức năng gồm đội hình, đổi/chuyển cầu thủ, số áo, sơ đồ, đội trưởng/người đá phạt, chỉ số, chân/vị trí, skill, celebration, gear và kit như editor gốc. Sửa validation áo thứ ba trong instance Event để không nhầm một CLB thật với ID đội ảo retro. Cơ chế editor gốc vẫn yêu cầu **sửa trước Enter Game; đóng hẳn/mở lại ứng dụng nếu engine đã nạp**. Thay đổi có hiệu lực ở lần nạp game sau, không sửa trực tiếp đội hình giữa trận.

Các chỉnh sửa RC24 đã lỡ lưu trong mục Transfer cũ không bị tự xóa/chuyển vì không thể biết chúng thuộc My League hay Event theo ý người dùng. Event Edit bắt đầu từ đội hình v25 và lưu riêng từ RC25.

## Hệ thống xác suất UCL theo DOCX v5

Theo lựa chọn cuối: **giữ nguyên pool v25 hiện có**, không thay Ajax bằng Como và không thêm đội. Bảy đội chưa có trong file được người dùng chốt tạm Nhóm4: Newcastle, Real Sociedad, Frankfurt, Ajax, Beşiktaş, Lazio, Fiorentina.

Áp bảng thắng/hòa/thua đúng từng chênh lệch nhóm và sân nhà/khách cho trận **AI UCL Event**; MU ở Nhóm5, giảm4 điểm phần trăm xác suất thắng khi thua hai trận liên tiếp ở vòng bảng. Mùa UCL mới bốc bốn pot, MU ở Pot4, vẫn đúng32đội được v25 chọn và ba trận bảng. Knockout vẫn **một trận**. Các trận người dùng đá và báo cáo engine giữ nguyên, không ép kết quả. World Cup và My League giữ thuật toán mô phỏng cũ vì tài liệu chỉ quy định UCL.

Các ví dụ tỉ số thắng đậm trong DOCX được dùng làm phân bố tỉ số có điều kiện sau bước thắng/hòa/thua. Các trọng số chi tiết còn thiếu, chia các tỉ số khác, hiệp phụ/luân lưu AI là lựa chọn triển khai có ghi trong metadata, không phải thông số chính xác được tài liệu cung cấp. Dùng tỷ trọng ghi bàn: Kane36%, Mbappé34%, Haaland38%, Dembélé20%, Lewandowski22%; Raphinha/Yamal14%, Kvaratskhelia20% trong khoảng file nêu; Bruno12%, Mbeumo14%, chỉ khi cầu thủ có trong XI của đội đó. Không tạo cầu thủ hay buff chỉ số để ép ghi bàn.

Các bảng phần trăm qua vòng/vô địch/Giày Vàng và tổng bàn/mùa trong tài liệu là mốc tham khảo, không được khóa cứng. Kết quả phải phát sinh từ các trận, bốc thăm và thể thức một lượt/ba trận bảng của Event v25. Thống kê AI được ghi rõ là mô phỏng; trận thật lấy scorer/assist/MOTM từ engine, không tính bàn luân lưu vào ghi bàn. Lịch sử đã chơi không bị mô phỏng lại hoặc bịa tên người ghi bàn. Nên bắt đầu giải mới để có bốc pot và thống kê đầy đủ từ đầu.

## Sửa đường nạp Ronaldo 2007/JUVE

RC24 có asset nhưng thiếu hai lớp cho phép hai ID mới trong native loader; gate đường dẫn cũng còn chặn profile mới của Ronaldo2027. RC25 sửa gate đầu cho hai ID mới và gate đường dẫn cho cả ba ID. Kiểm tra ARM64 đã tái hiện lỗi RC24 và kiểm tra hàm nạp đường dẫn thật chuyển sang asset mới với loader giả lập.

- `106783356083208` → Ronaldo2007, R7A1..6.
- `88043608522885` → Ronaldo JUVE2020, R0A1..6.
- `89138556572074` → Ronaldo2027 đang sửa, R9D1..6.

Không tự tạo thẻ mới trong tài khoản. Giữ nguyên toàn bộ mesh, texture, bind pose, cấu hình LOD và sửa miệng/da của RC24; lần này sửa bộ lọc nạp cả ba profile. Không sửa chiều dài tay. Tên/logo Ajax giữ nguyên theo yêu cầu cuối cùng.

## Match Settings từ v18-fixed

Đã đối chiếu: v18-fixed và v19.1 có engine cùng SHA256. Đưa ra giao diện ngoài đủ7setting gốc: Zoom, Height, Angle, Game Speed(-2..+2), PC Mode, Time(stock/siang=ngày/malam=đêm), Snow.

Lựa chọn được lưu riêng trong save gateway. Khi chưa Enter Game, giao diện báo **đã lưu/chờ engine**, không báo áp dụng giả. Sau khi engine/hook nạp và kiểm tra đúng phiên bản, worker áp lựa chọn, đọc lại byte native để xác nhận. Time/Snow nên chọn trước khi bắt đầu trận. Không thêm nút No Circle riêng vì bản donor không có một mục tách biệt như vậy trong bảng setting.

Mỗi địa chỉ chỉ chấp nhận byte gốc hoặc preset đã biết. Nếu đang có patch khác tại cùng địa chỉ, setting đó bị chặn và hiển thị xung đột, không ghi đè hook lạ. Khôi phục lựa chọn stock/OFF ở từng mục để trả về preset gốc. Không dùng lại tên package hoặc địa chỉ của bản engine khác.

## Áp gói FULL bằng MT Manager

1. Sao lưu APK và save. Mở bản sao APK v19.1 đang dùng.
2. Chép đè toàn bộ `assets/` và `classes5.dex` từ gốc ZIP FULL vào gốc APK. Giữ assets khác của APK nền, không trộn manifest/thư viện cũ vào gói này.
3. Lưu, ký bằng đúng khóa đang dùng và cập nhật đè; không cần xóa data.
4. Đóng hẳn và mở lại. Mở hai Event Edit hoặc Match Settings ở giao diện ngoài trước Enter Game.
5. Kiểm tra đúng ba card ID, miệng nghỉ/ăn mừng, camera gần/xa, màu da, LOD tay; chơi thử UCL/WC, chỉnh đội riêng và các setting.

Artifact GitHub là một ZIP FULL có assets/classes5.dex ngay ở gốc; không cần tải các delta trong `_ci`.

## Mức kiểm chứng

Kiểm tra host: save/project/catalog My League không bị Event sửa; lưu và cold-start Event; đổi cầu thủ/đội hình/áo/trách nhiệm/chỉ số/gear; native registration/kit theo scope riêng; cùng card có bốn scope native khác nhau và khôi phục khi đổi mode. Hai giải chạy đủ14chu kỳ trận bằng fixture. Mô phỏng300.000trận kiểm chứng bảng xác suất, giữ pool và bốn pot. Thực thi ARM64 gate mặt/đường dẫn và writer setting với bộ nhớ mẫu; đủ191lựa chọn đọc/ghi/đọc lại. UI ngoài đã thử nút trong Chromium với bridge Android giả lập, Java/DEX đã biên dịch và roundtrip.

**Chưa chạy engine Android/điện thoại.** Kiểm tra byte/đường dẫn không thay thế kiểm chứng tốc độ trận, camera, PC Mode, thời tiết, nạp asset thực tế, cử động môi, màu da và LOD trên máy. Các báo cáo RC24 trở về trước là lịch sử, không phải xác nhận RC25 trên thiết bị. Đây là ứng viên cần thử thực tế, chưa cam kết mọi setting hoặc mọi animation đều hoàn hảo.
