# UCL native-input session lifecycle

Tiếp tục nềnRC7 với knockout hai lượt. Chưa phát hànhFULL hoặc bật prototype.

Đã sửa Bridge.start: kiểm tra frozen match_plan và điều kiện provider trước cả đường trả cached start_packet; gọi lại provider khi khôi phục gói đã lưu để nạp lại trạng thái nativeRAM. Không dựng lại lineup hoặc đổi gameID trên retry. Provider có on_finish(game) tùy chọn để dọn cấu hình đúng phiên sau ghi nhận kết quả; lệnh kết quả đã có receipt vẫn dùng receipt cũ, không ghi thêm thống kê.

Đã sửa Controller: khi UCLđược chọn, yêu cầu đối thủ không cómatch_category đi vàoUCL, giống điều kiện của gateway gốc hỗ trợ category trống. Yêu cầu explicitEXHIBITION vẫn passthrough nếu không có trậnUCLpending. Nếu có trậnpending, chặn chuẩn bị chế độ khác và chặnCMD_START_GAMEgameIDkhác để tránh cấu hình native củaUCL rơi vào trận khác.

Test thực thi code Python prepare/start/finish/info/schedule/enter của APK73 đã qua: gọi lại provider trên cachedstart, sửa carry trong pending bị từ chối trước khi gọi provider, cleanup đúnggameID, cachelineupkhôngđổi, receipt/rollback/mùa thường không đổi. Các dịch vụ dữ liệu và provider trong test là boundaryfixture, không phải bằng chứng nativehook cài trong game. TestController thêm categorytrống và pendingmodeguards.

Truy vết native tiếp tục tại các vùng72eb...,72ea...,6cac...,6cdf...; configbuilder6a6479c đã được khảo sát nhưng chưa chứng minh đường còi hết giờ90/120phút. Không kết luận các hàm đọc thống kê theo hiệp là bộ điều khiển thời gian. NativeRuleInputprototype rc16 vẫn không được nối vào activationgate cho đến khi có bằng chứng end-of-match và binding/lifecycle đủ.
