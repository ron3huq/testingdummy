# Phân tích tay áo v13

## Dữ liệu thiết bị

V11: áp dụng0. V12 sau khi đã vào sân vẫn tay ngắn: serialize24, builder24, builder_matches0, entity0. ID cuối114758 là Marc Cardona trong bảng Android, không phải bằng chứng rằng game đổi ID Ronaldo thành114758. Chưa có danh sách toàn bộ24 ID nên chưa xác định chính xác khâu nhận diện nào bị mất ID thẻ.

## Đường mới

`0x3a0b28c(owner, kit)` được wrapper phản chiếu UE `0x3cc8aa0` gọi. Nó đọc actor từ owner+0x4d8. Actor chứa native character config tại+0x10a0; full64 config ID tại+0x10 được đọc ở actor+0x10b0; trường tay áo+0x50 tương ứng actor+0x10f0.

Hook mới đọc ID ngay tại actor và đặt trường tay áo thành1 trước khi gọi nguyên hàm nạp áo gốc. Ở `0x3a0b538`, game đọc trường này vàoW24; tại `0x3a0b560..588` nó chọn cặp resource áo dài (+0x198/+0x19c) thay cho áo ngắn (+0x190/+0x194); tại `0x3a0b5e0` chuyển sleeveType2 sangW3 trước virtual LoadUniShirt `0x3a0b5f8`. Vì vậy bản này bao phủ bước sử dụng áo ngay cả khi không đi qua hook entity của v12.

Chỉ nhận89138556572074,4522,16781738. Cả ba có tên chính xác Cristiano Ronaldo trong Player.bin, SHA256 d6777010a0ac8723e0a95ac17a239efbb973140ad58c6bb8881cc9943d8207b8. Không suy ra ID từ lowbits cho cầu thủ tùy ý. Hai alias dùng chung có thể ảnh hưởng các thẻ Ronaldo khác được game dựng bằng cùng alias; không thể cam kết riêng một thẻ sau khi native renderer đã làm mất phân biệt ID.

Giữ các hook v12, bổ sung hai ring buffer64 lượt gọi để log danh sách ID builder và shirt. Tất cả hook mới tùy chọn: lỗi cài được ghi riêng và không làm dừng gateway My League.

## Kiểm tra

- 107 ca serializer và6 ca chế độ/mùa cũ.
- 16 ca toàn bộ native builder,13 ca dispatch cũ.
- **67 ca bước nạp áo UE**: 11 ID,2 chế độ đầu vào,3 loại kit, cộng trường hợp chưa có actor. Chạy mã gốc từ entry đến đúng lệnh gọi LoadUniShirt, kiểm tra cả W1/W2 chọn resource và W3 tay áo.
- Kit resource lookup/availability và một virtual update được mô hình hóa. Resource100/101 và200/201 là sentinel để phân biệt nhánh ngắn/dài, **không phải mã áo đấu thực tế**.
- Chỉ actor+0x10f0 khác baseline ở ID khớp; toàn vùng actor còn lại giống baseline. ID không khớp, full64 khác dù cùng lowbits và null actor được kiểm tra. Ring buffer quay vòng/biên được kiểm tra.
- Python loader/diagnostics kiểm tra prologue cả4 điểm ngoại hình với ELF gốc và tình huống lỗi cài một hook.

Không mô phỏng mesh/texture/shader trên Android. Chưa thể xác nhận ảnh tay dài thành công trên thiết bị; nếu mã áp dụng nhưng ảnh vẫn sai, cần xem tiếp tài nguyên áo thực tế. Chưa ghép tóc, chưa sửa mặt.
