# UCL knockout một lượt theo yêu cầu mới

Người dùng đã bỏ yêu cầu lượt về: vòng loại trực tiếp đá một trận, hòa sau90phút thì hiệp phụ; còn hòa thì luân lưu. Giữ36đội,8lượt league phase, Como thay Ajax và Dortmund/Betis thay Genk/Villarreal.

Mùa mới tạo qua Store/Controller mang knockout_legs=1 và ruleset ucl-lp-single-match-knockout-v1. Có144trận league phase,8play-off,8R16,4QF,2SF,1chung kết:167trận. Đường vô địch12hoặc13trận tùy vé vào thẳng. Đội hạt giống chủ nhà ở các vòng được xếp hạt giống; chung kết trung lập trong mô hình CPU. Mùa cũ không có trường knockout_legs vẫn đọc là2, tránh đổi luật giữa mùa. API pure new có tham số2 cho test/hỗ trợ save cũ; luồng tạo mùa người dùng mặc định1.

Kiểm tra toàn mùa8bộ lịch cho cả hai đường vô địch, không cóleg2, từ chối hòa knockout chưa có penalty, nhận bàn hiệp phụ từ native period fields, tách luân lưu khỏi bàn thắng. Projection lịch sử native sửa kết quả hòa trên sân thànhWIN/LOSE theo penalty; tỷ số bàn giữ nguyên.

CHƯA PHẢI FULL: bộ nhận kết quả không đồng nghĩa game đã tự bật hiệp phụ. Static parser v19.1 tại0x7578bc8 đọc exTime/pk YES/NO. Hai đường gọi tìm thấy nằm trong event metadata (0x75bf130) và room_match_settings.match_env (0x75a8fb0), không phải bằng chứng rằng thêmmatch_envởrootCMD_START_GAME được engine dùng. Vì vậy không chèn một khóa bị bỏ qua rồi coi tính năng đã chạy. Cần nối đúng luồng event/match setup trên nềnRC7. Gate kích hoạt hiện còn giữ cho đến khi có provider thật; không thay bằnglambda giả trong bản giao.

Face19019, roster Dortmund và stage launcher giữ nguyên hướng tích hợp FULL tích lũy. Thống kê xuyên giải, WorldCup/lọc EventAI, final manifest và kiểm tra game vẫn chưa hoàn tất. Không kiểm thử trên điện thoại, không cógóiFULLcàiđặt từ bước này.

Đã viết ucl_lp_event_rules.configure theo đường metadata event của v25: LP exTime/pk=NO; knockout một lượt exTime/pk=YES, giữ CPU level. Đã chạy hàm _knockout_event trích từ cup_entry.pyc v25 với dịch vụ biên tối thiểu và so sánh match_env đúng với adapter mới.42tổ hợp stage/level qua; không sửa template nguồn. Đây là kiểm tra cấu hình/host, chưa nối provider vào event entry/routing RC7. Chưa bỏ gate hoặc giả lambda để coi như game đã bật hiệp phụ.
