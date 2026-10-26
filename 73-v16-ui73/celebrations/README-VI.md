# Kết quả tra ID ăn mừng của bản73

Đã tìm thấy **121 nhãn** dạng `dml_goal_celebrate_XXXX` trong engine. Danh sách đầy đủ ở [animation-labels.txt](animation-labels.txt), kèm vị trí chuỗi trong file engine ở [animation-labels.csv](animation-labels.csv). Đây là các nhãn có tham chiếu thật; chưa chứng minh đây là toàn bộ animation, vì có thể còn tên được tạo động hoặc clip bên trong kho nhị phân khác.

## Các giá trị đang có trên thẻ

Đối chiếu các bản ghi147 tham số có sẵn từ save đã cung cấp và registry1679 thẻ, cùng bảng tên của73:

| p59 Goal Performance | Thẻ nguồn | ID thẻ |
|---|---|---|
| 16 | Bukayo Saka | 106759733768760 |
| 22 | Riccardo Calafiori | 106759733774894 |
| 90 | William Saliba | 106763491864289 |
| 94 | Lionel Messi | 89136409091415 |
| 212 | Cristiano Ronaldo | 106734785925546 |
| 219 | Viktor Gyökeres | 106745238253510 |

Đây là **giá trị đang lưu trong dữ liệu của thẻ nguồn**, chưa xem và xác nhận động tác trên sân. Không đặt tên kiểu Siu, ngủ, v.v. khi chưa có bằng chứng hình động. Dữ liệu không đủ để suy ra thẻ nguồn nào sở hữu mọi nhãn animation trong danh sách121 mã. Các thẻ có giá trị0 cũng không có nghĩa là không ăn mừng; có thể còn cách chọn mặc định của engine.

## Ba mã0542,0571,0595

Chưa tìm thấy nhãn `dml_goal_celebrate_0542`, `...0571`, `...0595` trong các nguồn đã quét; chưa xác minh được0542 thuộc cầu thủ Nhật hay0595 thuộc Kvaratskhelia.

Đã kiểm tra bằng accessor ARM64 thật của73 trên bản ghi giả lập: p59 Goal Performance chỉ lưu9 bit (0–511), p60 Memorial Celebration7 bit (0–127). Gán trực tiếp các số lớn này **không giữ nguyên ID**:

| Giá trị đưa vào | Đọc lại từ p59 | Đọc lại từ p60 |
|---|---|---|
| 542 | 30 | 30 |
| 571 | 59 | 59 |
| 595 | 83 | 83 |

Vì vậy không gán trực tiếp542/571/595 cho các thẻ Ronaldo/Kvaratskhelia. Một mã clip ngoài hệ thống tham số cần có ánh xạ đúng trước khi sử dụng. Kết quả này không chứng minh mọi clip mang các số đó đều vắng mặt trong mọi kho dữ liệu khác.

## Phạm vi kiểm tra

- Chuỗi ASCII và UTF16 trong libUE4.so của73.
- Payload thực của131 mục trong dt230 (bao gồm bảng anime, kho mtar và skeleton),1139 mục dt250,220 mục dt251; giải bọc CRILAYLA và lớp zlib PES nếu có, rồi tìm nhãn animation.
- Dùng lại kết quả rà47 bảng mục lục CPK của APK và bảng thư mục IoStore resource từ lần kiểm tra trước; không tính các đoạn0542/0571/0595 bên trong hash hoặc ID face là ID ăn mừng.
- Đối chiếu JSON thẻ có sẵn; không dùng lại phép chép trực tiếp row Player.bin vào record runtime, vì phép chép đó sai bố cục.
- Chạy setter/getter ARM64 gốc để kiểm tra giới hạn lưu và giá trị đọc lại. Chưa kiểm tra hình động trên điện thoại.

UI7.3 chỉ sửa bộ cấp phát hook và giữ các thay đổi trước; lần tra cứu này **không tự đổi ăn mừng của thẻ nào**.
