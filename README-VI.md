# FULL-7 · bản ứng viên sửa lần 1 — CHƯA HOÀN TẤT

Nền duy nhất: commit 74a1cd8100c8ecd022af9f16ef1f9f98cffcfc96, APK73 V19.1. Không chuyển efootxi/FULL-6. Đây là payload tích lũy để kiểm tra thay đổi; KHÔNG phải bản đã sửa xong bốn lỗi trên điện thoại.

Thay đổi thực tế:
- Launcher WebView có nút Single Player · AI, gọi privateTool(single-player) rồi SinglePlayerSettings.open. DEX đã được dựng lại, không chỉ thêm HTML.
- Khôi phục hồ sơ đội Transfer từ DB vào myleague_editor.json khi khởi tạo, trước khi cấu hình native. Trước đây load() chỉ đọc profiles; sửa/khôi phục tài nguyên có thể làm runtime dùng lại đội gốc.
- Parser phân biệt stock key và cached key: với mode 2 giữ cache index ở word đầu và full ID ở word sau; lưu cặp key để kiểm tra. Không đổi index thành ID. Kiểm tra chỉ số hợp lệ, trùng ID/index và danh tính đội. Trước đây kind!=0 làm loại các snapshot cached hợp lệ.
- Bandage đọc cùng cấu hình player đã mở rộng như installer, bao gồm các override Transfer theo giải.
- resource_revision 19005; refresh inventory, manifest và checksum, giữ kiểm tra toàn vẹn.

Kiểm tra đã chạy: lưu DB/khôi phục sau khi thay file cấu hình, dữ liệu captain/taker theo full ID truyền tới installer, nút launcher gửi đúng request, DEX assembly/disassembly, accessor ARM64 gốc đọc hai word trên record tổng hợp với cache index khác thứ tự đội hình. Đây là kiểm tra máy chủ/giả lập, không phải xác nhận điện thoại.

Chưa giải quyết/xác nhận:
- Chưa chứng minh ánh xạ pool của cache thực trên máy, lỗi toàn GK, vai trò, thay người và việc đội hình áp dụng trong trận đã hết. Native libselect_team.so giữ nguyên FULL-7.
- Ronaldo 2027 chưa sửa rig/LOD/bind pose, cổ/tay hoặc hoạt ảnh mắt/miệng. Tài nguyên face giữ nguyên FULL-7, không đánh đồng với ZIP nguồn bị thiếu.
- Chưa chứng minh accessories/bandage trái/phải áp dụng trong trận hoặc không lan cache.
- Đã sửa đường mở Single Player; chưa sửa hay xác nhận thuật toán AI trong trận. Giữ đúng libsingle_player.so SHA256 2e1ef1970c5c48544992d7cfaa8c08e3e1c0e53a696eeb568aacf0f677c0a459, không dùng bản thử 60e8a5.

Không thêm Ronaldo Vol 9; giữ Spider V1 106782819217056, Miles 88035555413452, Ronaldo 2027 89138556572074. Không đưa DB/save cá nhân, log riêng hoặc ZIP nghiên cứu vào payload. Các báo cáo full7-* cũ là lịch sử của nền, không phải bằng chứng cho bản này.

Đóng gói: chép assets/ và classes5.dex vào APK73 V19.1 nền đúng, ký bằng khóa đang dùng. Gói này dành cho kiểm tra tiếp; không có xác nhận chơi trên điện thoại.
