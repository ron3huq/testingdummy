# Ronaldo v5 — gói thử hai thẻ, bổ sung mắt và trong miệng

Dành cho efootxi Android 1.3.2 ARM64, không root, chép bằng MT Manager.

| Card ID | Đầu được dùng |
|---|---|
| 88044950524330 | Mặt/tóc mì tôm của v4a, giữ nguyên hình học; bổ sung mắt, răng và mặt trong miệng |
| 89135066911146 | Mặt/tóc Ronaldo 2006 từ ZIP người dùng cung cấp, thay đầu cũ riêng thẻ này |

Không đổi Face ID gốc hoặc hệ thống nhận diện cầu thủ. Các thẻ khác đi qua luồng gốc.

## Cài gói đầy đủ

1. Buộc dừng game.
2. Giải nén `Ronaldo-v5-hai-the-mat-mieng-2006.zip`.
3. Gộp **cả `work/` và `livedata/`** vào **`files/embedded-gateway/`**. Ghi đè đủ tám tệp; không dán hai thư mục này bên trong `work/tools/`.
4. Mở game và nhận Latest Data nếu có yêu cầu. Kiểm tra lần lượt đúng hai thẻ ở bảng trên.

Không xóa save hay dữ liệu ứng dụng. Không phải sửa APK, thay dt200 hoặc chạy lệnh trên điện thoại. Không cài chồng lại runtime v4/v4a sau khi chép v5. Container vẫn mang tên pc9298; manifest/hash mới giúp nhận gói mới và không cộng revision lặp lại.

## Cần kiểm tra trên điện thoại

- Đúng thẻ 88044950524330 vẫn có mặt và tóc mì tôm như v4a; thẻ 89135066911146 có mặt/tóc 2006.
- Nhìn gần: có tròng mắt, chớp mắt, hướng nhìn; miệng mở có răng và mặt trong miệng, không xuyên môi.
- Chạy cả trong trận, replay bàn thắng/bỏ lỡ và ăn mừng. Chú ý tay/giày kéo dài, vì lỗi này chưa được xác nhận hết trên v4a.
- Thử một thẻ Ronaldo khác để đối chiếu phạm vi. Không suy kết quả từ việc hai thẻ có cùng Face ID.

Log: `files/embedded-gateway/work/tools/noodle-hair-status.json`.
Version mới: `ronaldo-dual-v5-native-internals`. Kiểm tra `state`, `error`, `payload_verified`, `last_target_id`, `last_asset_path`, `mesh_path_redirects` và `nonnull_callbacks`. Face profile vẫn là mã 4522... là đúng. Nếu có lỗi, gửi log này cùng ảnh của đúng thẻ; không cần chép toàn bộ thư mục game.

## Quay lại

Cài lại **gói đầy đủ v4a** theo cùng cách gộp work/ và livedata/ để khôi phục trạng thái trước v5. Gói v4a đã xác nhận có mặt/tóc cử động nhưng vẫn thiếu mắt/miệng. Liên kết:
https://github.com/ron3huq/testingdummy/raw/refs/heads/chat-downloads/efootxi-1.3.2/ronaldo-pc-mesh-v4a/Ronaldo-PC-mesh-v4a-88044950524330.zip

`Tat-ban-thu-v5.zip` chỉ tắt thay đầu cho **cả hai thẻ**, trả về đầu gốc của game; không phục hồi riêng đầu mì tôm v4a. Không xóa dữ liệu ứng dụng.

## Đã làm và giới hạn

Đã thực sự đọc và giải nén v4a, nguồn v4/v4a, hai ZIP 2006, nguồn FMDL NEUBE cũ và Android gốc từ bản phát hành công khai. Bản dựng giữ nguyên 166 xương/bind matrices Android, hình học mặt và tóc mì tôm, cùng texture tóc v4a. Các block ETC2 của diffuse mặt v4a được giữ trong vùng atlas tương ứng; atlas còn có texture native cho mắt/răng/miệng. Normal/SRO dùng metadata native phù hợp, không dùng sRGB của diffuse để giả normal map.

Đã đưa trở lại 135 đỉnh native: 88 đỉnh vùng mắt và 47 đỉnh răng/mặt trong miệng; gán mắt theo xương skf_eye_l/r, răng dưới theo jaw, phần trên theo head. Vị trí mắt được khớp với lỗ mắt PC; không nắn lại da mặt/tóc mì tôm. Bản 2006 dùng 2.369 đỉnh da/cổ/da đầu và 2.097 đỉnh tóc từ nguồn 2006; không mang tóc mì tôm sang thẻ này. Mesh head-shell 2006 có toàn bộ đỉnh trùng nhau bị loại, không đưa hình học suy biến vào gói.

`oral.fmdl` PC được đọc: 325 đỉnh/530 tam giác, nhưng texture chung `oral_bsm.tga` và các map đi kèm không có trong nguồn PC. Bản này dùng răng/khoang miệng native đã có texture tương ứng. Không tuyên bố có rig hay chuyển động lưỡi độc lập, hoặc đủ mọi biểu cảm PC.

Đã kiểm tra tám mesh, trọng số, bone maps <=75, đủ active/required bones, skinning mắt/hàm, imports và checksum container. Đã chạy native ARM64 qua Unicorn và kiểm tra năm detour Python, gateway 2441 byte, manifest/idempotence và đóng gói. Engine được mô hình hóa tại biên khi chạy Unicorn; bộ đọc UE4 và ảnh CPU không phải renderer Android.

**Đây là bản thử chưa được người dùng xác nhận trên điện thoại. Chưa xác nhận hết lỗi replay/cutscene, chất lượng ánh sáng, mí mắt hay giao cắt môi. Không thể bảo đảm “không lỗi” chỉ từ kiểm tra trên máy dựng.**
