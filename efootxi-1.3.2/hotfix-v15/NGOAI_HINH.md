# Kết quả tay áo v15

## Tay dài đã có cơ sở thiết bị

Người dùng xác nhận v14 hoạt động. V15 tái sử dụng cùng serializer52-byte và builder0x68ceb44, thay điều kiện nhận diện bằng bảng ID đúng tên có giới hạn competition518/122. Giữ hai thẻ Ronaldo cũ không thay phạm vi. Không thêm điểm hook.

Danh tính trích từ Player.bin, SHA256 d6777010a0ac8723e0a95ac17a239efbb973140ad58c6bb8881cc9943d8207b8. 28 bản ghi Cristiano Ronaldo +51 Lionel Messi ở518; 26 K.Kvaratskhelia +31 Ousmane Dembélé +33 Jude Bellingham +44 Kylian Mbappé +36 Erling Haaland ở122. Khớp chính xác tên (Kvaratskhelia dùng tên viết tắt đúng nguồn), không dùng phép cắt lowbits cho người tùy ý. Khi rời phạm vi giải, các bản ghi mới dùng lại chế độ áo gốc; riêng hai thẻ v14 vẫn giữ yêu cầu đã hoạt động.

## Tay dài xắn ngang cẳng tay: chưa xác minh được

Ảnh người dùng mô tả tay dài kéo/xắn lên một phần cẳng tay, có nếp vải dồn ở tay. Chưa tìm được cờ rolled-sleeve, mẫu mesh hoặc Blueprint xử lý tương ứng trong nguồn được cung cấp. Đã rà tên asset và chuỗi native; danh sách sleeve-assets.json ghi lại kết quả tìm kiếm, không phải bằng chứng không tồn tại trong mọi gói game.

Packed sleeve có2 bit. Trong hai bảng nguồn, các giá trị thực tế chỉ0/1/2; **không có bản ghi nào dùng3**. Native converter0x68d1fbc xử lý mode3 thành config+0x50=2. Đã kiểm tra mã ARM64: giá trị2 được truyền đến tham số W3 của LoadUniShirt. Trong nhánh chọn resource đã nghiên cứu, giá trị2 đi nhánh resource áo ngắn; giá trị1 mới đi nhánh áo dài. Vì vậy **không thể kết luận2 là tay xắn hay tay3/4**.

Bản thử riêng bật mode3/config2 cho đúng ID88045755960810 (Ruud Gullit). Đây là thăm dò một giá trị native, không phải tạo mesh tay xắn hay ghép mẫu Ronaldo trong ảnh. Chỉ bản ZIP thử bật cờ; bản tay dài thông thường đểfalse. Không dùng mode3 cho bất kỳ cầu thủ khác. Có thể kết quả không khác áo ngắn, không giống ảnh, hoặc không được renderer hỗ trợ; khi đó quay lại ZIP thường. Muốn tạo đúng nếp gấp trong ảnh nếu game không hỗ trợ sẵn sẽ cần tài nguyên áo/mesh phù hợp, chưa có đường chỉnh đã được xác minh.

## Kiểm tra

- 1.024 ca chạy toàn builder ARM64 ở các context0/518/122/566: tên đúng giải mới nhận tay dài, ngoài phạm vi giữ giá trị gốc; kiểm tra các cầu thủ tên gần giống và toàn249 ID đã chọn.
-32 ca bật/tắt thử nghiệm, nhiều context và ID khác: chỉ Gullit88045755960810 nhận config2 khi bật.
- Converter mode3 chạy cả hai mùa và đường chuẩn bị LoadUniShirt thật; xác nhận W3=2, không coi đó là chứng minh hình ảnh tay xắn.
- Giữ các kiểm tra serializer107 ca, builder16 ca, dispatch13 ca, shirt selection67 ca và phát lại22 ID thiết bị trước đó.
- Python loader kiểm tra đọc cờfalse/true, chuyển cho native trước cài hook và xuất trạng thái. Native/cache/crash-entry/gateway regression được chạy lại.

Các boundary DB/context/resource lookup, libc và một số thiết lập phụ được mô hình hóa trong Unicorn. Không mô phỏng renderer/mesh/texture Android. V14 là phiên bản được người dùng xác nhận tay dài; nhóm cầu thủ mới và giá trị thử v15 chưa được kiểm tra hình ảnh trên điện thoại.
