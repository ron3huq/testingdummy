# FULL8 RC22 · nền RC7 · Event UCL/World Cup v25 · Ronaldo2027

Đây là FULL tích lũy từ đúng `FULL8-RC7-complete-APK73.zip` trên APK v19.1 đã ký. Không cần áp RC21. Bỏ hoàn toàn đường UCL launcher/My League và hook tổng tỷ số của RC21. Bản này là **ứng viên để thử Android**, chưa được xác nhận trên điện thoại; không bảo đảm mọi animation/ánh sáng đã hoàn hảo.

## Áp bằng MT Manager

1. Sao lưu APK đang dùng và save theo cách bạn vẫn dùng. Không gỡ ứng dụng/xóa data.
2. Mở bản sao APK v19.1 trong MT Manager. Chép đè toàn bộ `assets/` và `classes5.dex` từ ZIP FULL vào gốc APK; giữ những assets khác của APK nền.
3. Lưu, ký bằng đúng khóa đang dùng và cập nhật đè. Mở lại ứng dụng từ đầu để nạp DEX, native và các gói mặt mới. Không trộn `classes5.dex` của RC21 vào gói này.
4. Vào **Event Mode / Event AI** để mở UCL hoặc World Cup. Bảng/lịch/nhánh đấu dùng `CupTournamentPanel`, nền và crest của chính v25. Không vào My League để chơi UCL.
5. Trong bảng Event có nút **Stats / Thống kê** để xem Vua phá lưới, Vua kiến tạo và MOTM.

## UCL và World Cup

Giữ thể thức đúng donor v25: 32 đội, 8 bảng × 4, 3 trận bảng; top 2 vào vòng 16 đội; knockout **một lượt**, có hiệp phụ/penalty theo cấu hình donor. Không còn mô hình 36 đội/8 vòng/hai lượt của RC21.

Giữ ID event v25: UCL 1120006/1120007, World Cup 1120010/1120011. Chuyển 14 module cup/roster/simulation, 37 helper giao diện/cài đặt, 35 lớp giao diện Java và các tài nguyên nền/crest của v25. Thêm một listener cùng nút thống kê vào lớp CupTournamentPanel đã chuyển. Toàn bộ 588 lớp DEX cũ của RC7 giữ nguyên, gồm launcher, Single Player và Transfer.

Engine `libUE4.so`, dt250/dt251 và dữ liệu tham chiếu v19.1/v25 đã đối chiếu trùng. Không chép engine hoặc thay toàn bộ app.imy v25. Module cup được cô lập để giữ các hàm My League/đối thủ toàn cục của RC7. V25 còn đoạn tương thích để trả lại mùa My League của bản cũ; luồng Event hiện tại đã kiểm tra không kích hoạt nhánh mượn mùa đó. Không tạo mùa UCL trong My League.

Thống kê giải gắn riêng theo cup_id, nối vòng bảng với knockout, chống cộng trùng khi gửi lại kết quả. Ghi bàn/kiến tạo lấy từ danh sách cầu thủ trong gói kết quả; MOTM chỉ ghi từ cờ `is_man_of_the_match` của engine. **Chưa có dữ liệu cầu thủ đầy đủ cho trận AI hoặc toàn bộ đối thủ**; bảng có thông báo giới hạn này, không tự bịa người ghi bàn/MOTM. Chưa nhận file Word hệ thống để đối chiếu các quy tắc và bố cục bổ sung trong tài liệu đó.

## Ronaldo2027 · ID89138556572074

Giữ nguồn mặt/tóc đang có của RC7, skeleton tham chiếu 166 bone, bind pose, topology HQ và phần cổ/thân. Sửa tiếp đường tiếp xúc môi; thêm đệm cục bộ 0,6 mm theo trọng số vùng môi để tư thế nghỉ/hé hàm rất nhẹ không lộ răng. Tổng thay đổi vị trí mặt tối đa khoảng 1,76 mm, không scale đầu hay cơ thể. Răng/lưỡi vẫn hiện khi há miệng; không bôi đen răng để thay cho việc khép môi. Niêm mạc lấy đúng vùng UV khoang miệng thay vì atlas má.

Bản gần giữ trọng số rig mặt để biểu cảm. Bản xa dùng cùng bề mặt/UV đã sửa, tránh phép chiếu low mesh chung làm méo atlas miệng. Chỉ ở LOD xa, ảnh hưởng các bone biểu cảm mặt được gộp về head theo rig xa; ảnh hưởng cổ/vai/thân giữ đúng bone toàn cục. LOD xa có đủ 153 active/required bone. Thu gọn **GPU bone map** về đúng bone thực sự dùng (19 ở bản gần, 6 ở bản xa), đổi chỉ số cục bộ tương ứng nhưng giữ trọng số toàn cục; không sửa chiều dài tay hay rest pose để che lỗi.

Có sáu atlas màu đầu đồng bộ với sáu palette native của thân; mặc định palette 2. Khi thay palette, đóng và mở lại game để mặt/thân được dựng lại cùng cấu hình, tránh so sánh với model đang cache từ trước.

## Đã kiểm tra / chưa kiểm tra

- Hai giải hoàn chỉnh trên host: tổng 14 chuỗi prepare/start/finish qua code v25, dữ liệu MessagePack v19.1, đội hình/HLV fixture; chung kết luân lưu; gửi lại kết quả không cộng trùng. My League thường giữ nguyên.
- Đọc lại 24 asset mặt đã đóng gói (4 biến thể × 6 palette): stream, chỉ số tam giác, UV, bone map/weights, bind pose và global skin weights.
- Tia nhìn ở 15 góc × 4 biến thể: không mẫu răng/lưỡi lộ qua môi ở tư thế nghỉ và jaw thử 1°/2°; mở hàm lớn vẫn thấy răng. Kiểm tra độc lập màu texture. Không có tam giác da bị lật do phần đệm môi.
- Kiểm tra ARM64 selector sáu palette, giữ hành vi bảy ID đối chứng khác; startup/LOGIN checksum và checksum toàn gói vẫn được kiểm tra.
- **Chưa chạy Android/ART, giao diện Java thật, chuyển LOD trong engine, SIUU hay ánh sáng trên máy**. Mô phỏng host không bảo đảm sửa hết lỗi ở mọi animation. Cần phản hồi điện thoại để xác nhận trọn luồng.

Không chứa APK, engine, save/DB cá nhân, Blend hay video. Bản đầy đủ nghĩa là đầy đủ payload tích lũy để áp lên nền v19.1, không có nghĩa đã được xác nhận hoàn hảo trên điện thoại.
