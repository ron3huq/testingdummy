# Đối chiếu FULL-7

## Nhịp trận trên Samsung A56

Hiện tượng người dùng mô tả là tốc độ cảm nhận khi chạy, giữ bóng và nhận thao tác; không phải số phút hay đồng hồ trận. Chưa có đo đạc trực tiếp trên A56 để xác định nguyên nhân. Độ sáng OLED thấp có thể giảm điện năng/nhiệt và giúp giữ hiệu năng lâu hơn; nhiệt độ, kết nối, tải nền và phong độ cũng có thể thay đổi theo phiên chơi. Các khả năng này chưa chứng minh rằng giờ 2–5 tự tăng tốc độ cầu thủ.

Màn hình 120 Hz hoặc mục tiêu FPS 120 không chứng minh game đang render đủ 120 khung hình/giây. Để so sánh, cần giữ cùng đội, phong độ, thể lực, sân, đối thủ, độ khó và chế độ; ghi FPS thực, thời gian khung hình, nhiệt và độ trễ thao tác khi đổi riêng độ sáng. FULL-7 giữ tốc độ vật lý và đồng hồ trận gốc.

## Các lớp phong độ

Phong độ dùng trong trận có năm mức: Terrible, Bad, Normal, Good, Excellent. Live Update A–E và thuộc tính Form chỉ là đầu vào xác suất. Trong bảng native, Live Update A vẫn có thể cho Normal/Good; sau đó engine còn giới hạn số Excellent ở bước áp đội hình. Vì vậy FULL-7 ép tại bước ghi phong độ cuối cùng, gồm cả đường nạp lại bản ghi, thay vì chỉ đổi nhãn A.

Form có ba giá trị nội bộ, không có giá trị “Excellent” để ghi vào trường đó. Thể lực và chấn thương là dữ liệu riêng. Phong độ đội CPU trong mô phỏng lịch giải lại là trọng số dựa trên chuỗi kết quả, không phải mũi tên phong độ trong trận. FULL-7 không ghi nhầm các trường này thành giá trị Excellent.

## Bandage mobile

Gói nguồn `MEGA_BANDAGE_PACK_FWC_2026_FL26_V7_AIO.rar` có SHA256 `7636a10f7c6b3f74c7595847d9aa473e85478715ac962c78f5f8cce1d7e82399`. Texture PC dùng UV khác mobile. Bản chuyển đổi chọn ba mẫu vải, dựng lại vùng cổ tay bằng UV thân native, giữ sáu màu da và phần texture bên ngoài vùng băng. Chọn độc lập hai tay tạo 15 tổ hợp khác rỗng, trên hai atlas Skin/Body: 180 texture riêng. Atlas Lowbody chứa chân nên được giữ nguyên.

Đường detail đổi khóa cấu hình trước hàm băm cache; đường common dùng đường tài nguyên riêng và vật liệu động thuộc từng actor. Vòng phạm vi bandage tách khỏi cut-long/RGB, có xử lý luồng, lồng callback và hết dung lượng. Khi không có cấu hình hoặc không có phạm vi hoạt động, đường tải bỏ qua khóa bandage. Kiểm tra native và trình đọc tài nguyên không thay thế thử nghiệm thiết bị.

## Điều khiển một cầu thủ và AI

Đã đối chiếu hai tệp PES 2021 trong release: APK SHA256 `b41d78f13db7bdefe200918fa2676a1242a9d2e40183517a4802a0dca18301f8`, ZIP SHA256 `8a6c66116f83855aba8c2f9d0b747e32032002a486b5e9972eda2a95daf060a1`. Bản cũ khóa cursor ở chế độ một cầu thủ nhưng không tự đáp ứng đầy đủ việc bật/tắt AI của bản hiện tại; không chép nguyên thư viện cũ vào game mới.

Module mới dùng hàm chuyển trạng thái native hiện tại để tạo quyền nhận thao tác, khóa đúng full ID còn trên sân và giữ ý định AI cho nút bấm, lưu thiết lập và lưu tạm. Pause/replay, cầu thủ rời sân, thay đội hình và vòng tạo/hủy trận được đối chiếu riêng. Lỗi bản lưu tạm cũ bật AI lại sau lựa chọn mới đã được tái hiện và sửa; 24 trường hợp xen kẽ đã qua kiểm tra độc lập.

Kiểm thử chạy module ARM64 đã biên dịch cùng các hàm engine gốc trong fixture. Vòng Update đầy đủ và đối tượng trận được khởi tạo bằng fixture; chưa chạy gameplay thực tế trên A56. Xem báo cáo trong `validation/` để phân biệt giới hạn từng kiểm tra.

## Face

Ronaldo 2027 dùng lại source mới gửi; chỉ chỉnh vùng mắt và đóng gói lại các section hiển thị. Hai Spider được căn kích thước đầu/cổ nhưng giữ điểm nối thân, skeleton và UV. Các kiểm tra đã đối chiếu container ghép cuối, 20 biến thể/40 mô tả LOD. Chưa có bằng chứng trên điện thoại xác nhận lỗi tay kéo dài hoặc sẹo cổ đã hết; không suy ra điều đó chỉ từ việc skeleton/LOD hợp lệ.
