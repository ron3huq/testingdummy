# Tay áo v12 và giới hạn kiểm chứng

## Tại sao thay v11

Thiết bị người dùng xác nhận v11 đã cài hook nhưng bộ đếm áp dụng bằng 0. V11 chỉ sửa bản sao packed52 khi đầu bản ghi trung gian chứa đúng full64 ID. Dữ liệu trạng thái cũ chưa đếm tổng số lần gọi, nên **chưa chứng minh được nguyên nhân là hàm không được gọi hay ID trung gian khác**.

V12 thêm:

- `0x68ceb44(outConfig, spec)`: đọc full64 ID trực tiếp từ `spec+8`, gọi bộ dựng gốc rồi đặt `outConfig+0x50=1` cho đúng thẻ 89138556572074.
- `0x68db150(entity, mode, config)`: sửa cùng trường ngay trước chuyển cấu hình qua virtual method. ID entity ở +0x28, được hai caller của game dùng để điền spec+8. Hàm gốc gồm năm lệnh dispatch; hook giữ nguyên dispatch đó, không chạy trampoline chứa lệnh CBZ tương đối đã di chuyển.
- Đếm số lần gọi, số lần khớp ID, chế độ cũ, ID cuối và tình trạng cài từng hook. Giữ đường serialize v11 như một đường bổ sung.

Native converter `0x68d1fbc` xác nhận packed mode2 là tay dài cưỡng bức, đầu ra config+0x50 bằng1, độc lập mùa. Không nhầm trường +0x4c (thuộc tùy chọn áo khác) với tay áo.

## Đã kiểm tra

`validate_appearance.py` chạy mã ARM64 gốc với 107 ca serializer, 6 ca mode/mùa, 16 ca toàn hàm dựng (DB và cache), 13 ca dispatch (gồm null entity). Có ca mô hình hóa DB trả bản ghi khóa4522 cho yêu cầu full64 thẻ Ronaldo: đường v11 bỏ qua, v12 vẫn sửa đúng đầu ra. Đây là **kịch bản kiểm thử**, chưa phải nguyên nhân đã xác nhận trên điện thoại.

So sánh trước/sau toàn cấu hình: chỉ trường tay áo thay đổi; ID khác và cùng lowbits khác full64 không bị sửa. Kiểm tra chuyển tiếp entity/mode/config, vùng đệm lân cận, giữ nguồn bảng. DB/context/resource lookup, libc và bước giày phụ được mô hình hóa; không mô phỏng renderer mesh/texture Android. Cần kiểm tra hình ảnh trong trận trên thiết bị.

## Tóc

Chưa ghép tóc Pato88038776539586 vào Ronaldo88044950524330. Không thay mặt hay mesh đầu. Các kết quả nghiên cứu asset/redirect v11 được giữ trong `research/`, không dùng để tuyên bố đã có tóc mới.
