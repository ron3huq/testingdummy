# Ronaldo 2027 — RC7 BASE · FACE DETAIL · WIP19019 — CHƯA ĐƯỢC BÀN GIAO

Nền FULL8 RC7 trên APK73/v19.1. Đây là payload assets/ và classes5.dex, không phải APK đã ký. Giữ DEX, Single Player, Transfer và accessories RC7; không áp điều khiển RC8. Không xóa data/save.

ID89138556572074 giữ đầu và tóc MessipradeepV2. Chỉ khép đường tiếp xúc môi bên trong, giữ độ dày viền môi; chỉnh lại thể tích mí rất nhỏ và thêm nếp dưới mắt/đuôi mắt theo ảnh tham khảo. Các nếp là texture chi tiết nhẹ, không cắt mesh hoặc thêm bone. Răng/lưỡi giữ màu gốc trong bóng tối; họng rất tối, không bôi đen toàn bộ phần oral.

Giữ vị trí, UV và trọng số cổ/thân RC7; bỏ bước ép cổ vào donor thấp vốn tạo các dải gồ. Màu đầu/cổ được cân về cùng palette native thân; lựa chọn1–6 áp dụng cả đầu lẫn thân khi khởi động. Giữ topology thực được vẽ và số đỉnh HQ; bỏ vùng chỉ số đệm không thuộc section, rig166bone, bind pose và tóc. Trọng số răng dưới/lưỡi được khôi phục từ chính bản nguồn calibrated RG27 để đi cùng da mặt, thay bản rigid-jaw riêng của RC7. LOD0 đủ166bone, LOD1 native compact153bone.

Chấm đen cằm trong ảnh trước là lỗi dựng bóng với tam giác đệm, không phải nốt ruồi được thêm vào texture. Asset mới chỉ chứa chỉ số tam giác của hai section được khai báo; kiểm tra chỉ số nằm trong số đỉnh ở cả hai LOD. Preview bỏ thêm tam giác suy biến có diện tích bằng0, có normal/SRO từ asset. Không xóa/bôi texture cằm.

Kiểm tra host phải đọc lại chính asset đã đóng gói: môi nghỉ không lộ phần oral, chớp mắt đóng hết ở pose thử, há hàm5/12/20/30độ thấy răng/lưỡi, các bản sao mép da giữ trùng nhau. Không gọi host pose là đã kiểm thử Android. Cần kiểm tra trực tiếp SIUU/chuyển LOD/ánh sáng trên điện thoại trước khi kết luận hết lỗi tay dài/crash hoặc mọi animation đều đúng.

UCL CHƯA TÍCH HỢP VÀO TRẬN THẬT. Source lõi UCL36đội có trong source/repair-full8-rc9-ucl/runtime; không có UI/native match adapter, thống kê cầu thủ, WorldCup adapter hay bộ lọc EventAI2mục trong ứng viên này. Không dùng nhánh v25 tự mô phỏng hiệp phụ/penalty cho trận người chơi khi thiếu kết quả thật. Không gọi ứng viên face là bản FULL hoàn thành UCL.

Không có save, DB, log cá nhân, APK/video/RAR nghiên cứu, engine hoặc protected bundle v25 trong gói. app.imy là thành phần gốc của APK, được giữ lại.

## Chặn bàn giao sau kiểm tra cận cảnh

Bản render từ pc9385 cho thấy các dải tam giác niêm mạc kéo qua khe miệng khi há hàm20độ. Kiểm tra mép da trùng nhau không phát hiện được lỗi này. Phân tích bổ sung thấy13tam giác nội miệng có cạnh kéo dài hơn3lần ở20độ (lớn nhất4,742lần),26tam giác ở30độ (lớn nhất6,571lần). Đây là chẩn đoán, không phải ngưỡng bảo đảm mọi animation. Chưa sửa bằng cách xóa mặt, bôi đen hoặc thay topology để che lỗi. Cần xử lý liên kết/biến dạng niêm mạc và kiểm tra lại với chuyển động môi/hàm thực của rig.

Không gọi bản này là hoàn thiện, không tải gói Android cho người dùng cài. finalize_face_candidate.py bị chặn bởi quality-gate.json cho tới khi có bằng chứng sửa lỗi miệng. Báo cáo motion cũ chỉ xác nhận hữu hạn/mép da/độ che mắt và độ nhìn thấy oral, không chứng minh không có xuyên hoặc kéo mesh.
