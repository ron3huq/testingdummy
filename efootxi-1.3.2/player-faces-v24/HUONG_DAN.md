# V24 — ba nguồn 2017 độc lập và nguồn 2027 vừa gửi

Cài một gói đầy đủ: **Faces-v24-three-2017-and-new-2027.zip**.

1. Buộc dừng game trong Cài đặt Android.
2. Giải nén; dùng MT Manager gộp **cả `work/` và `livedata/`** vào `files/embedded-gateway/`, chép đè tệp trùng tên.
3. Mở game. `work/tools/noodle-hair-status.json` phải ghi `player-faces-v24-three-2017-new-sources`, `HOOK_ACTIVE`, `error: null`.

Không cài lại v23/v22 sau gói này. Không xóa save/dữ liệu ứng dụng. Gói không sửa libUE4 và không ghi đè cấu hình My League cá nhân.

## Gán nguồn mới

| Thẻ | ID | Nguồn mới | Profile trong log |
|---|---|---|---|
| Ronaldo 2017 | 88044950524330 | RP Facemaker, nhánh No Real Eyes | NX01 |
| Ronaldo Jr | 105765448873424 | Prince Shieka V6 | NXJR |
| Nicolás González | 105807861630781 | Nodle Hair PES 2021 From FIFA | NXNC |
| Ronaldo 2027 | 106734785925546 | ronaldo2027.rar, Kodigo | NX27 |

Ba thẻ 2017 dùng **ba bộ mesh, material và texture riêng**, không còn cùng trỏ một đầu. Giữ tên/áo/chỉ số đang có của từng thẻ; theo yêu cầu, Jr và Nicolás nhận ngoại hình từ các nguồn Ronaldo đã gửi. Mắt và trong miệng dùng thành phần native, nên chọn nhánh RP No Real Eyes để không ghép thêm mắt PC chồng lên mắt native.

RP và Prince là `.model` PES 2017; FIFA là FMDL PES 2021; nguồn 2027 mới cũng là `.model` PES 2017. Đã giải nén các lớp RAR/CPK/CRILAYLA/WESYS, đọc model bằng bộ đọc đúng định dạng. Các tệp ghi chú trong archive không được thực thi hoặc dùng làm chỉ thị cho tác nhân.

**Lưới mặt và tóc FIFA trùng từng byte với nguồn 2017 đã dùng trước đó.** Vì vậy RP được gán cho thẻ chính, Prince cho Jr, FIFA cho Nicolás. V24 vẫn thay đổi cách chuyển đổi FIFA chứ không tuyên bố đây là hình học hoàn toàn mới.

## Khác biệt kỹ thuật đã xác định

Trong v23, bộ chuyển đổi đã đọc X của normal map FIFA từ kênh đỏ cố định 255. Nguồn thực tế lưu X ở **alpha**, Y ở **green**; đọc sai làm Z tái tạo gần 0 thay vì một normal hướng ra bề mặt. V24 giải mã đúng A/G và dựng lại Z. Normal map đã mã hóa lại được đọc độc lập để đối chiếu với giá trị nguồn. Đây là lỗi chuyển đổi đã chứng minh được, **chưa chứng minh là nguyên nhân duy nhất của mọi trường hợp đen/tàng hình trước đây**.

Gói Prince khai báo `hair_2`, RP khai báo `hair_style`; v24 dùng đúng hai mẫu này và texture tương ứng, không chọn nhầm `hair_high` đi kèm. Nguồn 2027 dùng `hair_high` có trong archive. Giữ đầy đủ các lớp da mặt, gáy/đầu `head_phong`, scalp và các nhóm tóc thực; atlas tóc chứa cả texture nền tóc và texture phần sợi, với UV từng nhóm được chuyển sang đúng ô. Không bỏ một phần đầu chỉ vì tên material khác FMDL. Các placeholder HairTube bị ép gần phẳng và head ba đỉnh được bỏ khỏi phần render native; không ép chúng thành đĩa da/tóc đục. Phần tóc sợi thật vẫn giữ mask alpha. Đây là chuyển đổi asset, không sao chép nguyên shader pha trộn PC. Riêng `hair_2` của Prince chứa head placeholder ba đỉnh; phần scalp 341 đỉnh được lấy từ `head_phong` của `hair_high` có sẵn trong cùng gói để khép khoảng trống dưới tóc, vẫn giữ tóc sợi `hair_2`.

Bộ đọc `.model` và FMDL có quy ước thứ tự tam giác khác nhau. V24 xử lý riêng chiều mặt của mỗi định dạng; kiểm tra CPU có culling và kiểm tra chiều sâu vùng giữa mặt để bắt trường hợp mặt hướng vào trong, không chỉ đếm số đỉnh.

PES 2017 dùng chỉ số xương **cục bộ theo BoneGroup của mesh**. Chúng được đổi sang tên xương trước khi ánh xạ sang Android, không dùng trực tiếp làm chỉ số skeleton native. Giữ skeleton/inverse bind 166 xương, RequiredBones LOD0/LOD1 166/153, tối đa 4 trọng số/đỉnh, tổng byte 255 và palette dưới 75. Giữ mắt/miệng native. Chuyển về các điều khiển mắt/hàm/mí Android, không cam kết toàn bộ rig biểu cảm PC.

## Phạm vi giữ nguyên

Tất cả asset còn được giữ từ v23 đều nguyên byte: các mặt khác, Özil V2, Hoang Duc, kit, font, ảnh lớn/nền và miniface đã căn ở v23. Chỉ bỏ các skin asset NW01/NW27/NWJR đã bị thay thế, rồi thêm bốn namespace mới. Hoang Duc không có nguồn thay mới trong yêu cầu lần này; không tuyên bố đã sửa lỗi của đầu đó trong gói này.

Native chỉ đổi bốn ánh xạ profile so với v23. Không thêm probe/truy vấn engine/cờ render, không bật lại probe v22. Giữ sửa ABI Đội hình 23 đối số, tên/UI/áo, quốc tịch/CLB, kit, vị trí/chỉ số và áo dài tay trước đó.

## Kiểm tra và giới hạn

Đã kiểm tra nguyên số lượng/vị trí đỉnh/tam giác từ nguồn, đủ các nhóm tóc, native skeleton, trọng số, normal map A/G, package/import và mười biến thể đầu. Đã đọc lại mesh/texture độc lập bằng UEViewer; native có 578 kiểm tra nền, kiểm tra bốn namespace không lẫn thẻ và không thêm engine query. ZIP có CRC/SHA và kiểm tra fallback khi payload hỏng.

`CPU-static-review.png` là ảnh raster mesh/texture tĩnh ở ba góc nhìn có culling mặt lưng. Nó giúp kiểm tra mặt/tóc thực sự còn trong asset; **không phải ảnh game Android và không chứng minh shader/animation/GPU trên máy đã đúng**.

**Chưa xác nhận hết đen/tàng hình trên điện thoại.** Sau cài, xem lần lượt bốn ID trong bảng. Nếu còn lỗi, báo rõ ID nào đen hoặc tàng hình và gửi log v24 mới; không cần gửi lại nguồn. Nếu văng, buộc dừng và tạm đặt `work/tools/noodle_hair.json` thành `{"enabled":false}` để tắt redirect mặt, không xóa dữ liệu game.
