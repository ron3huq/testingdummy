# Hệ thống xác suất theo tài liệu người dùng

Đây là mã đang phát triển trên FULL8 RC7 v19.1, chưa phải gói FULL cài đặt.

Đã chốt trực tiếp với người dùng: giữ Como thay Ajax; thay Genk/Villarreal bằng Dortmund/Real Betis. Bàn hiệp phụ được tính cho vua phá lưới, bàn luân lưu không tính. Nhóm sức mạnh trong tài liệu độc lập với bốn pot bốc thăm.

`../repair-full8-rc9-ucl/runtime/ucl_lp_probability.py` mô phỏng riêng trận CPU. Trận người dùng tự đá giữ kết quả native; không ép theo tỷ lệ. Chính sách được chụp vào mùa mới để không tự đổi luật giữa mùa; mùa cũ không có cpu_policy giữ thuật toán cũ.

Các bảng điểm số có tổng trọng số120 và113 được chuẩn hóa khi rút thăm. Mục5-1 xuất hiện hai lần trong bảng cách biệt lớn được cộng trọng số. Cú sốc3% nằm trong xác suất đội yếu thắng, không cộng thêm vào tổng xác suất thắng. Điều chỉnh phong độ xử lý chủ nhà trước, đội khách sau; derby cộng5điểm phần trăm hòa rồi chia lại phần thắng. Chung kết trung lập dùng trung bình hai cột nhà/khách. PSG/Barcelona có ưu tiên tỷ số nhiều bàn sau khi đã chọn kết quả thắng/hòa/thua.

Những chi tiết tài liệu chưa chỉ rõ được ghi minh bạch trong JSON: chia đều hai tỷ số sốc; hiệp phụ CPU phân thắng bại bằng một bàn; tỷ lệ sút thành công75% là giả định để tạo tỷ số luân lưu đối xứng. Không dùng các giả định này để thay kết quả người chơi. Các tùy chọn mục8 tắt. Không ép tái tạo số liệu40.000mùa minh họa trong tài liệu.

Đã kiểm tra8bộ lịch, đầy đủ144trận league phase/189trận toàn giải, hai đường vô địch15/17trận, tổng tỷ số lượt về và10.000loạt luân lưu hợp lệ. Test cũng xác nhận kết quả99-0 của người chơi không bị thuật toán xác suất sửa lại. Đây là kiểm tra host, chưa phải kiểm tra Android.

Dortmund có22ID cầu thủ hiện đại đối chiếu catalog tên/vị trí của game; JSON ghi rõ native_application_ready=false. Chưa coi danh sách ứng viên là đội đã có roster native hoạt động. Không dùng đội cổ điển thay thế. Còn phải hoàn thiện áp roster theo ngữ cảnh UCL, provider tổng tỷ số cho engine, nối thống kê cầu thủ/kiến tạo/MOTM, WorldCup/lọc EventAI và gộp cùng face19019 thành FULL. Không cung cấp stage hoặc patch riêng như bản hoàn thiện.
