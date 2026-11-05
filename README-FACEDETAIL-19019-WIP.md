# Ronaldo 2027 — RC7 BASE · FACE DETAIL · WIP19019 — CHƯA ĐƯỢC BÀN GIAO

Nền FULL8 RC7 trên APK73/v19.1. Đây là payload assets/ và classes5.dex, không phải APK đã ký. Giữ DEX, Single Player, Transfer và accessories RC7; không áp điều khiển RC8. Không xóa data/save.

ID89138556572074 giữ đầu và tóc MessipradeepV2. Chỉ khép đường tiếp xúc môi bên trong, giữ độ dày viền môi; chỉnh lại thể tích mí rất nhỏ và thêm nếp dưới mắt/đuôi mắt theo ảnh tham khảo. Các nếp là texture chi tiết nhẹ, không cắt mesh hoặc thêm bone. Răng/lưỡi giữ màu gốc trong bóng tối; họng rất tối, không bôi đen toàn bộ phần oral.

Giữ vị trí, UV và trọng số cổ/thân RC7; bỏ bước ép cổ vào donor thấp vốn tạo các dải gồ. Màu đầu/cổ được cân về cùng palette native thân; lựa chọn1–6 áp dụng cả đầu lẫn thân khi khởi động. Giữ topology thực được vẽ và số đỉnh HQ; bỏ vùng chỉ số đệm không thuộc section, rig166bone, bind pose và tóc. Trọng số răng dưới/lưỡi được khôi phục từ chính bản nguồn calibrated RG27 để đi cùng da mặt, thay bản rigid-jaw riêng của RC7. LOD0 đủ166bone, LOD1 native compact153bone.

Chấm đen cằm trong ảnh trước là lỗi dựng bóng với tam giác đệm, không phải nốt ruồi được thêm vào texture. Asset mới chỉ chứa chỉ số tam giác của hai section được khai báo; kiểm tra chỉ số nằm trong số đỉnh ở cả hai LOD. Preview bỏ thêm tam giác suy biến có diện tích bằng0, có normal/SRO từ asset. Không xóa/bôi texture cằm.

Kiểm tra host phải đọc lại chính asset đã đóng gói: môi nghỉ không lộ phần oral, chớp mắt đóng hết ở pose thử, há hàm5/12/20/30độ thấy răng/lưỡi, các bản sao mép da giữ trùng nhau. Không gọi host pose là đã kiểm thử Android. Cần kiểm tra trực tiếp SIUU/chuyển LOD/ánh sáng trên điện thoại trước khi kết luận hết lỗi tay dài/crash hoặc mọi animation đều đúng.

UCL CHƯA TÍCH HỢP VÀO TRẬN THẬT. Source lõi UCL36đội có trong source/repair-full8-rc9-ucl/runtime; không có UI/native match adapter, thống kê cầu thủ, WorldCup adapter hay bộ lọc EventAI2mục trong ứng viên này. Không dùng nhánh v25 tự mô phỏng hiệp phụ/penalty cho trận người chơi khi thiếu kết quả thật. Không gọi ứng viên face là bản FULL hoàn thành UCL.

Không có save, DB, log cá nhân, APK/video/RAR nghiên cứu, engine hoặc protected bundle v25 trong gói. app.imy là thành phần gốc của APK, được giữ lại.

## Kiểm tra cận cảnh và chặn bàn giao FULL

Phát hiện hai island niêm mạc5/10 (146đỉnh) lấy UV từ atlas má. Chỉnh riêng UV0 của chúng sang vùng khoang miệng hiện có (0.9375,0.8125), không đổi vị trí, tam giác, trọng số hay UV ngoài môi/má. Ảnh jaw20 mới dựng lại từ pc9385 sau đóng gói cho thấy vùng niêm mạc tối; răng và lưỡi dùng UV riêng được giữ. Các thử nghiệm kéo niêm mạc ra sau hoặc tô tối theo atlas má gây lỗi ở má và đã bị loại bỏ, không áp vào asset.

Số đo kéo giãn niêm mạc là chẩn đoán, không phải ngưỡng chứng minh mọi animation. Báo cáo motion chỉ xác nhận hữu hạn, mép da trùng, độ che mắt và độ nhìn thấy oral; không chứng minh không có mọi xuyên mesh. Chưa kiểm thử trực tiếp điện thoại.

quality-gate.json vẫn chặn bàn giao FULL: UCL chưa nối native/UI/hiệp phụ tổng tỷ số. Không gửi gói face riêng như bàn giao cuối và không gọi bản WIP này là FULL hoàn thiện.
