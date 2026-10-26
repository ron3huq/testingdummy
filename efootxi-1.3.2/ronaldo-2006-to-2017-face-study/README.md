# Ronaldo 2006 → nghiên cứu cấu trúc mặt 2017 (bản Blender)

Theo yêu cầu đã xác nhận: chỉ .blend để kiểm tra trước. KHÔNG cài đè game, KHÔNG thay Spider-Man.

Mở Ronaldo_2006_to_2017_FACE_EDIT.blend bằng Blender 4.3.2. Texture đã đóng gói; không cần addon. Chọn face_high_2_fox_skin_mat → View / Frame Selected để xem mặt. Z / Material Preview để xem màu.

## Điều khiển so sánh
Trong Outliner, chọn 00_EDIT_CONTROLS. Vào Object Properties → Custom Properties:
- Face2017_strength: 0 = cấu trúc gốc 2006; 1 = bản chỉnh đang xem; tối đa 1.5.
- Neck_shortening_mm: 0 = cổ gốc; mặc định 6 mm; tối đa 10 mm.
Các mesh, kể cả tóc, cùng nhận độ rút cổ để không tách đường nối. Kiểu tóc không được thay đổi; tóc chỉ dịch cùng đầu. Save As trước khi tự chỉnh.

Hai shape key riêng: Ronaldo_2017_FACE_STRUCTURE và NECK_SHORTER_6mm. Slider trên từng mesh được điều khiển bằng 00_EDIT_CONTROLS, nên chỉnh thông số tại bộ điều khiển.

## Phạm vi đã chỉnh
Giảm độ đầy phần dưới má, làm rõ gò má và hàm, đưa cằm nhẹ ra trước và tăng nhẹ khối vùng cung mày. Đây là các thay đổi nhỏ ở cấp mm trên mesh gốc; không thay topology, UV hoặc skin weights. Cổ rút 6 mm theo biến dạng liên tục, không cắt bỏ mesh.

Đã sửa chế độ hiển thị smooth shading và alpha của texture tóc trong cảnh nguồn để tránh hình ảnh mặt chia tam giác/tóc thành các tấm đục. Không vẽ lại texture hoặc dựng kiểu tóc 2017.

## Giới hạn cần biết
Bản này là nghiên cứu hình dáng dựa trên các ảnh người dùng gửi, CHƯA được xác nhận giống Ronaldo 2017 chính xác. Ảnh có phối cảnh, biểu cảm và ánh sáng khác nhau; 6 mm là lựa chọn chỉnh nhẹ, không phải số đo suy ra chắc chắn từ ảnh.

Texture da và tóc vẫn của nguồn 2006. Các phần mắt/common assets không đầy đủ trong gói nguồn vẫn chưa được dựng lại; ảnh xem có thể thấy mắt tối. Điều này chưa được che giấu bằng ảnh tạo mới hay thay texture khác. Không tuyên bố là mặt 2017 hoàn thiện.

Hai video YouTube VXLd0h9XGzM và 5WH7s-IPIeM đều trả HTTP403 trong môi trường xử lý; chưa xem được nội dung, chưa áp dụng một workflow được trích từ video đó.

Chỉ kiểm tra Blender: mở lại file, đối chiếu 10 mesh với nguồn, giữ nguyên Basis/topology/UV/weights và kiểm tra controller. Chưa retarget/cook bản này cho Android, chưa thử trên điện thoại. File .blend không phải gói dán đè mobile.

Nguồn: CRISTIANO RONALDO 2006.zip do người dùng cung cấp. Tác giả gốc chưa xác minh. before-after.jpg dùng cùng camera/ánh sáng và cùng khung cắt để so hình dáng; các PNG riêng có khung hình đầy đủ.
