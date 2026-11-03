# Đối chiếu Single Player PES2021

Nguồn nghiên cứu: PES.2021LordzGaming.apk từ releasee. Đọc OnePlayerRouter trong DEX và code ARM64 liblordzoneplayer.so; libpesoneplayr.so được xem phần selector/hook. Không đóng gói APK/thư viện cũ vào payload.

OnePlayerRouter có requestToken/requestKind/requestRows/choose. JNI choose tại0x5924 kiểm tra token, trạng thái picker, phạm vi chỉ số rồi lưu chỉ số chọn tại state+0xc. Đường native tại0x6c64 lấy key từ hàng đã chọn, tra vị trí live qua hàm engine PES2021+0x6812eec; chỉ chấp nhận0..21 và đúng side. Nhánh0x7084 lưu key và chuẩn hóa order về0..10 bằng cách trừ11 khi cần. Danh sách/chọn người gắn với trận và đội đang điều khiển, không coi catalogue40k là đội hình.

APK73 cần accessor của chính engine73 và key full64+serial; địa chỉ PES không được bê nguyên sang73. Bridge lookup73 giữ tra ID sang serial live. Bản73 RC2 đã bỏ gate AI ở tick0x112d4 nhưng bỏ sót gate AI tại control-entry0x120e8, nên AI tắt vẫn không ghi controller. RC3 bỏ thêm gate này; giữ kiểm tra pause/replay/player ownership và restore của module đã xác minh. Chỉ hai lệnh gate khác bản2e1ef197 gốc.

Bài test RC2 dừng ở ranh giới control-entry nên không phát hiện gate thứ hai. Bài test RC3 chạy toàn bộ enter/fixed/restore, dùng accessor/setter ARM64 engine73 gốc trên cấu trúc tổng hợp, thử11 thay đổi con trỏ native và xác nhận khóa lại cùng người, rồi khôi phục dữ liệu cũ. Đây vẫn không phải kiểm chứng điện thoại.
