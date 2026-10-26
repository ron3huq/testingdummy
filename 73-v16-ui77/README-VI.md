# UI7.7 Earth — 73 V16 Part 2 Main

Áp toàn bộ ZIP vào gốc APK đang có UI7.6 và Part 1 Faces, ký cùng khóa rồi cài đè. Không gỡ game, không xóa dữ liệu. Nếu dùng APK gốc, áp cả Part 1 Faces UI7 và Part 2 UI7.7 trước khi ký; resource V9 vẫn là tài nguyên nền riêng.

## Player Model: bằng chứng và giới hạn

Đã thực thi đường cấu hình model → hook dựng model phát hành → hàm tính tỉ lệ xương gốc73 tại0x68d2b4c trên ARM64 giả lập. Với Arm Length, xương sk_upperarm_l có scale1.0 ở mức trung tính,1.05 ở mức lớn nhất và0.95 ở mức nhỏ nhất. Vì biên độ nhỏ, thay vài nấc có thể khó nhận ra bằng mắt.

Điều này chứng minh đường dữ liệu có thể thay đổi phép tính xương của game, chưa chứng minh render đúng trên điện thoại. Không có điện thoại kết nối để kiểm thử. Runtime Diagnostics nay có final_float_applies, last_card_id và mẫu bit float cánh tay trước/sau; có thể dùng log sau khi thực sự mở cảnh3D để kiểm tra đường dựng trên thiết bị.

## Chiều cao/cân nặng

- Cân nặng:40–250kg, đã đọc lại đúng250 bằng getter native gốc.
- Chiều cao:140–255cm là miền dữ liệu hiện hỗ trợ. **Chưa hỗ trợ350cm/3m5.** Trường gốc chỉ8bit: ghi350 bằng setter gốc sẽ đọc lại94. UI và API từ chối giá trị vượt255, không âm thầm cắt bit.
- Các kích thước cực đoan có thể bị giới hạn ở bước render/animation; kiểm tra readback dữ liệu không đồng nghĩa xác nhận mọi hành vi vật lý.

## Physics

Appearance & Motion → Physics · Verified Inputs chỉnh Height, Weight, Jump40–99 và mở Player Model để chỉnh tỉ lệ tay/chân/thân. Đây là các đầu vào thật đã xác minh của game.

**Chưa có bộ sửa độc lập năm số EFHub trong ảnh** (Leg Coverage Radius, Arm Coverage Radius, Jumping Height, Torso Collision, Leg Length Based Height). Các số đó là giá trị dẫn xuất/ước tính, không phải năm trường native đã xác minh. Không tạo thanh kéo giả hoặc gắn công thức EFHub chưa kiểm chứng vào dữ liệu game.

## Skill gốc

Skills → Edit Innate Skills. Dấu chọn và nhãn Current thể hiện skill đang có; chọn/bỏ rồi Save. Năm ô Additional Skills giữ riêng. Reopen player details sau khi lưu để làm mới màn hình cũ.

Lưu vào owned card và overlay native theo đúng ID thẻ64-bit. Chỉ thay74 cờ skill thuộc layout147 đã có; giữ progression, booster và các trường khác. Nhãn của các slot native chưa được đặt tên hoàn chỉnh không khẳng định có một động tác riêng đã kiểm chứng.

Giữ nguyên kits, giỏ catalogue, quyền dùng nhiều Ronaldo, ngoại lệ tay ngắn và các bản sửa trước. Phần tìm kiếm catalogue giữ nguyên mã, không thêm quét dữ liệu vào thao tác tìm; các mục mới chỉ tải khi người dùng mở. Projection trong trận không truy vấn SQL. Chưa có benchmark độ trễ trên điện thoại.

## Bảng ăn mừng có sáu thẻ/tên

[celebration-six-cards.csv](celebration-six-cards.csv):318 cặp parameter/giá trị,1544 dòng thẻ nguồn. Ưu tiên tên nguồn khác nhau và ID variation dài; nếu cần, bổ sung các phiên bản thẻ khác của cùng người. Có97 giá trị không đủ6 thẻ nguồn; không bịa hoặc lặp ID để đủ số lượng.

Quét toàn bộ46623 bản ghi bằng bộ nhập native gốc82aa124 rồi đọc bằng getter82a84d4. Tên lấy từ trường tiếng Anh ở offset332 của record nguồn. Đây là giá trị p59/p60, không tự suy ra rằng nó bằng số tên clip animation; chưa có xác nhận động tác trên sân.

## Kiểm tra

Kèm báo cáo: model-to-bone consumer, skill flags/height/weight/Jump qua native accessor, lưu và khôi phục dữ liệu, rollback khi giả lập lỗi ghi file, bảo toàn Additional Skills khi chiếu My League, projection không SQL, hash/manifest/DEX và đăng nhập gateway73.

Các bài kiểm tra ARM64 dùng bản ghi mô phỏng và stub ở ranh giới engine/Android được ghi trong báo cáo. UI, render và vật lý trên thiết bị chưa được thử trực tiếp; không cam kết100% hoạt động hoặc không lag trên mọi máy.
