# Đối chiếu hiệp phụ/penalty của v25 và cấu hình theo từng lượt

Hàm _knockout_event của cup_entry.pyc v25 đặt exTime=YES, pk=YES cho knockout một lượt. Khi state.two_legs là true và phase thuộc R16/QF/SF, hàm lại đặt cả hai về NO. Điều này không phủ nhận chế độ knockout một lượt đã có hiệp phụ/penalty; nó cho thấy không thể chép nguyên cấu hình hai lượt của bản đó để có đầy đủ tính năng yêu cầu.

Đã cập nhật ucl_lp_event_rules.configure: league phase và lượt đi đặt NO/NO; chung kết một trận đặt YES/YES; lượt về chỉ xuất YES/YES khi bên gọi xác nhận đã có bộ nối native xét tổng tỷ số. Nếu chưa có xác nhận, hàm từ chối cấu hình lượt về. Không dùng nhãn sẵn sàng giả hoặc tạo kết quả penalty để thay trận chưa đá.

Test có 42 tổ hợp thể thức một lượt và 28 tổ hợp vòng/độ khó cho hai lượt. Đã chạy hàm _knockout_event thật trích từ v25 và xác nhận nhánh hai lượt tắt hiệp phụ/penalty. Test template nguồn không bị sửa. Chỉ code hàm được chọn chạy với dữ liệu kiểm tra; không chạy khởi tạo toàn bộ module v25 và không chép protected bundle vào repo.

Chưa nối chính sách này vào event entry/routing RC7; chưa chứng minh nhánh hết giờ dùng RuleInput tổng hai lượt; native prototype chưa được cài vào bản giao. Đây chưa phải gói FULL hoàn thiện và chưa thử trên điện thoại. native_aggregate_ready là điều kiện cần ở lớp cấu hình, không phải bằng chứng engine đã hoạt động.
