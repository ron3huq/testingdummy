# Roster Dortmund qua API native RC7

Dùng `ucl_lp_roster.py` để thêm một hàng đội hình vào JSON editor trong stage. API ARM64 `editor_add_team/slot/plan/taker/commit` và hook nạp đội đã có sẵn trong RC7; không sửa hoặc thay thư viện libselect_team.so.

22cầu thủ hiện đại từ catalog tên/vị trí của game; Guirassy, Adeyemi, Brandt thuộc đội hình này. Không gán đội cổ điển. Đội hình4-2-3-1 với11đá chính,11dự bị, số áo khác nhau,4biến thể sơ đồ và vai trò đá phạt/captain nằm trong roster.

Phạm vi122 là UEFA: **Dortmund trong My League UEFA thường cũng nhận roster này**. Không gọi scope0 hoặc chế độ ghi toàn cục. Lựa chọn này dùng API scope đã có, tránh tự tạo mã competition chưa được engine hỗ trợ. Test xác nhận rời scope khôi phục đội nền và giải125 không nhận roster mới.

`test_roster_native.py LIBSELECT_TEAM ENGINE` chạy chính mã ARM64 RC7 bằng Unicorn, đồng thời chạy ba hàm engine thật ghi vị trí/role. Các dịch vụ tra cầu thủ/parameter/DB ở biên được giả lập có kiểm soát. Kiểm tra22ID/số áo/thứ tự xuất phát, khôi phục sau khi rời UEFA, thiếu cầu thủ bị từ chối trước khi ghi bất kỳ phần roster nào, và thử lại thành công. Khóa bằng SHA256 đúng RC7/engine.

Đã nối bước này vào `repair-full8-rc11-ucl-entry/build_entry.py`; stage nhận JSON editor mới qua luồng khởi động editor RC7 sẵn có. Không áp vào payload RC7 đang quảng bá, chưa thử trên điện thoại và chưa phải bản FULL giao người dùng. Provider tổng tỷ số native vẫn chưa xong.

Kiểm tra bổ sung cho thấy ensure_team126 khi đã đăng ký hàng editor sẽ truyền lỗi preflight ra ngoài; khi cầu thủ giả lập bị thiếu, ready không trả1. Khi khôi phục cầu thủ, ensure_team trả1. Không cần thêm monkey patch cho API này.
