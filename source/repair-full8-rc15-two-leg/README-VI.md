# Yêu cầu hiện hành: knockout hai lượt

Thay thế lựa chọn một lượt ở rc14 cho mùa mới. League phase36đội/8lượt; play-off/R16/QF/SF hai lượt; chung kết một trận. Không luật bàn sân khách.189trận toàn giải, đội vô địch đá15hoặc17trận. Save đang chơi giữ định dạng đã lưu.

Bridge.prepare đóng băng carry_home/carry_away trong pending native session, đảo chiều bàn lượt đi cho đúng sân lượt về. Bridge.start xác nhận kế hoạch không bị thay đổi. Tổng bàn là dữ liệu riêng, không ghi thêm vào bàn lượt về hoặc thống kê cầu thủ. Match plan có quyết định khi hết90/120phút, bao gồm thắng riêng lượt về nhưng hòa tổng, hòa riêng lượt về nhưng thắng tổng, và tổng hòa dù bàn sân khách khác nhau.

Đây là hợp đồng dữ liệu và logic quyết định cho bộ nối engine, chưa phải bộ nối engine hoạt động. Không bật exTime/pk một cách mù quáng cho lượt về: native chỉ xét tỷ số riêng lượt có thể đá sai. Cấu hình event một lượt v25 ở rc14 vẫn chỉ áp dụng cho mùa một lượt. Provider tổng tỷ số vẫn vắng; gate chưa được bỏ. Chưa có gói FULL bàn giao, chưa thử điện thoại.
