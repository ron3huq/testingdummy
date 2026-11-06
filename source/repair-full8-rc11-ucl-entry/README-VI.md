# UCL launcher entry — bản làm việc, chưa phải FULL bàn giao

Nền vẫn là FULL8 RC7 trên APK73/v19.1. Giai đoạn này thêm nút launcher, operation `ucl → ui73_ucl` trong LauncherWeb, và lệnh cài router trong bản sao bridge_73. `build_entry.py` tạo stage độc lập; không sửa DEX, payload inventory hoặc runtime đang quảng bá của RC7. Không chép stage riêng này vào điện thoại: đây chưa phải FULL có manifest được hoàn tất.

Danh sách 36 đội giữ Como1907 ID4219 thay Ajax116. Theo lựa chọn mới của người dùng khi đọc tài liệu xác suất, Dortmund126 thay Genk1195 và Real Betis194 thay Villarreal267. Betis có28slot trong dữ liệu nền. Dortmund có danh sách22cầu thủ hiện đại được đối chiếu tên và vị trí bằng catalog game, đã có bộ áp qua API editor native RC7 trong stage mới; kiểm tra ARM64 host xác nhận22ID/số áo/sơ đồ và khôi phục khi rời scope. Scope122 cũng cập nhật Dortmund trong My League UEFA thường. Chưa kiểm thử điện thoại; xem source rc13. Không dùng Celtic131/Rangers132 vì RC7 đang gán các ID đó cho đội Y17. Không ID nào của pool trùng classic_teams hoặc hai giải Y08/Y17. Đây là pool tùy chọn, không phải danh sách dự UCL chính thức.

Có8bộ lịch hợp lệ; mỗi bộ8lượt ×18trận, mỗi đội8đối thủ khác nhau,4nhà/4khách,1nhà/1khách với mỗi pot; không gặp cùng liên đoàn và tối đa2đối thủ của một liên đoàn khác. Thuật toán host tách đồ thị8bậc thành5perfect-matching và3màu cuối, thay cho bài màu1152biến lớn. Android nhận lịch JSON đã kiểm tra, không chạy SciPy.

Kiểm tra đã chạy:
- Dựng và giải ngược DEX:588lớp, chỉ LauncherWeb thay đổi; lớp SinglePlayer/Transfer giống RC7. DEX stageSHA044d1c0a22b25657cda71cb457a7bedd8f8e38e4e0521580863a978453132b7f.
- Chromium chạy các script launcher thật với Android host giả lập và Controller SQLite thật: chọn Como, tạo mùa, bảng36dòng,8lượt đủ18trận, kích hoạt/đọc lại/rời mùa; save My League thường giữ nguyên. Đây không phải kiểm thử Android/engine.
- Các test lõi mùa, kết quả native, ledger, routing và pool đều qua. host-*.json ghi phạm vi cụ thể.

Lệnh kiểm tra tại workspace đã có RC7 và công cụ Java:
```
python source/repair-full8-rc11-ucl-entry/build_entry.py ROOT FRESH_STAGE
python source/repair-full8-rc11-ucl-entry/test_ui.py ROOT FRESH_STAGE
```
Test UI cần Playwright, Chromium và loopback; không tải resource ngoài. Ảnh host nằm ở stage, không được mô tả là ảnh trong game.

Chưa hoàn tất: điều khiển engine hiệp phụ theo tổng tỷ số; nối đầy đủ attribution cầu thủ/native/CPU; WorldCup và lọc EventAI; kiểm chứng luồng vào MyLeague từ menu native, rồi gộp face19019 + entry + manifest thành FULL mới. Provider tổng tỷ số vẫn vắng; kích hoạt UCL bị chặn. Không phát hành một mùa chỉ đá được league phase rồi kẹt lượt về. Không cần người dùng biếtADB để tiếp tục viết các phần này.
