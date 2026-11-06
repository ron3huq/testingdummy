# Tỷ số trận và tổng hai lượt bên cạnh

Theo ảnh tham khảo, lượt về cần hiển thị tỷ số đang đá và tổng hai lượt ở ô bên cạnh. Ô phụ cập nhật theo bàn vừa ghi: lượt đi 1–0, lượt về 0–0 thì hiển thị 0–0 (1–0); lượt về thành 2–1 thì hiển thị 2–1 (3–1). Bàn luân lưu không cộng vào hai tỷ số bàn thắng này.

Đã tìm thấy đường ghi dữ liệu native tại 0x6ba04ac..0x6ba05bc. Hàm bao ngoài bắt đầu tại 0x6ba02a4; x19 là vùng output, x20 = x19 + 0x61bc theo lệnh 0x6ba02e8. Đoạn kiểm tra ghi tỷ số riêng trận tại output + 0x61dc/0x61e0, cờ tổng tại +0x61ec và tổng hai lượt tại +0x61f0/0x61f4.

Nguồn tổng là RuleInput với cờ +0x12a và carry +0x12c/+0x12e, đọc qua 0x72ead9c/0x72eada4. Vòng ghi tỷ số hiện tại lấy thống kê kind5 riêng; vòng sau cộng carry để ghi tổng. Khi aggregate tắt, đoạn native hạ cờ tổng, không xóa các ô dữ liệu tổng cũ.

`test_native_score_publisher.py ENGINE` chạy đoạn ARM64 thật, getter và vòng lặp native; chỉ giả lập nguồn bàn hiện tại. Các register ngữ cảnh hiển thị hợp lệ được cấp sẵn tại đầu đoạn kiểm tra. Có 25 tổ hợp qua. Ví dụ theo ảnh: match[0,0], aggregate[1,0], flag1. Khi lượt về thành 2–1: match[2,1], aggregate[3,1], flag1. Tắt aggregate hạ flag0.

Giới hạn: chưa chạy toàn bộ hàm bao ngoài hoặc chứng minh output thuộc instance HUD đang render. Chưa có kiểm tra pixel, bố cục hoặc ảnh trong game để xác nhận ô tổng đã hiện. Các offset chỉ mô tả vùng dữ liệu đã kiểm tra, chưa đủ kết luận theme UCL hoặc HUD đã tích hợp. Không tạo ảnh mô phỏng rồi mô tả là gameplay.

Prototype RuleInput rc16 vẫn chưa được cài vào gói FULL; nhánh hết giờ, hiệp phụ và penalty còn cần xác minh. Đây là bằng chứng native bổ sung, chưa phải bản FULL bàn giao, chưa kiểm thử trên điện thoại.
