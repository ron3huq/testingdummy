> Người dùng báo v3 kéo tay/giày trong cutscene. Có [bản thử v4](../ronaldo-pc-mesh-v4/HUONG_DAN.md) và gói tắt đầu thử; chưa xác nhận v4 trên thiết bị.

# Ronaldo PC face v3 — chuyển thử mặt từ 4522.cpk và giữ mã facial profile gốc

Chỉ **Card ID 88044950524330**. `4522` là nhóm tài nguyên đầu Ronaldo, không phải Card ID. Các bản v1/v1b dùng mặt Android gốc; v2 chỉ sculpt nhẹ mặt gốc và chuyển màu tóc. V3 mới chuyển bề mặt/màu da mặt từ nguồn PC.

## File người dùng cung cấp

Đã đọc `4522.cpk`: 14 tệp, gồm face.fpk nén CRILAYLA, face.fpkd 48 byte và 12 FTEX. Giải nén FPK ra face_high.fmdl, hair_high.fmdl, oral.fmdl, face_diff.bin. Cả bốn nội dung này và 12 texture **trùng byte/hash với nguồn PC người dùng đã gửi trước đó**. Đây là cùng nguồn mặt/tóc PC; các bản trước chưa áp mặt PC, không có nghĩa mặt PC đã được dùng từ đầu.

## Cài bằng MT Manager

1. Buộc dừng efootxi. Giữ bản sao gói đang dùng, không xóa dữ liệu hoặc gỡ ứng dụng.
2. Giải nén `Ronaldo-PC-face-v3-88044950524330.zip`.
3. Gộp **cả `work/` và `livedata/`** vào **`files/embedded-gateway/`**, cho phép ghi đè. Cần chép đủ tám tệp, gồm cả `libnoodle_hair.so` mới. Không dán CPK PC vào APK mobile.
4. Mở game; nếu hỏi tải dữ liệu mới thì tải. Vào sân bằng đúng Card ID 88044950524330, xem cận cảnh khi ăn mừng/replay.
5. Đọc `files/embedded-gateway/work/tools/noodle-hair-status.json`: version **`ronaldo-pc-face-v3`**, state HOOK_ACTIVE, error null. Sau khi đầu được tải, cần xem `redirects`, `nonnull_callbacks`, `face_id_preserves`, `last_face_profile`, `target_texture_callbacks`, `texture_nonnull_callbacks` và `texture_null_callbacks`.

`last_face_profile` đọc lại FString mã mặt từ actor tại offset đã đối chiếu với setter native. Với thẻ đã thấy trong log, giá trị mong đợi là `4522ep00v0313`, **không phải ND01ep00v0313**. `face_id_preserves` tăng xác nhận lời gọi setter được chuyển về mã gốc. Texture callback nonnull xác nhận có texture trả về; cần hình ảnh trong game để xác nhận phần nhìn thấy đúng.

## Mặt PC được chuyển thế nào

Nguồn PC và Android khác topology/rig. V3 chuyển bề mặt da mặt PC lên **743 đỉnh, 1222 tam giác mặt native**, có giới hạn dịch chuyển 8 mm và vùng bảo vệ quanh tâm mắt theo bind pose Android. Giữ số/ID đỉnh mặt, thứ tự tam giác, UV mặt, skin weights, skeleton và inverse bind matrices. Không đoán tên xương môi hoặc gán toàn bộ mặt vào xương đầu.

Texture da PC được chuyển sang layout UV Android và nén **ETC2 RGB 1024×1024**. Bốn texture riêng mang tên `T_ND01..._Face_D` được thêm vào container để lời gọi tải texture của engine có tài nguyên thật. Native callback của engine vẫn thực hiện gán texture và cleanup. Tóc giữ atlas màu/alpha v2 và hình học đã thử trước đó.

Đây là **bản chuyển thích nghi bề mặt và màu da PC**, không phải chép nguyên toàn bộ mesh/FOX shader/bộ rig PC. Không chuyển riêng bộ clip biểu cảm PC, shader normal/specular PC hoặc toàn bộ oral/eyelash mesh PC. Các phần điều khiển/nhãn cầu/răng có sẵn của mobile vẫn dùng hệ thống của game. Hình ảnh và chuyển động mắt–miệng v3 chưa được xác nhận trên điện thoại.

## Hướng sửa mặt đơ

Hook cũ đổi Face ID 4522... thành ND01... ở đầu hàm tải. Disassembly cho thấy hàm gốc dùng giá trị này để **lưu vào actor ở +0x448**, đồng thời tạo đường dẫn mesh **và texture Face_D**. Bản trước chỉ cung cấp mesh riêng; việc giữ cả mã actor thành tên mới là một điểm không tương thích cần loại bỏ.

V3 giữ việc tải mesh/texture riêng theo đúng thẻ, nhưng thêm hook ở setter native để actor nhận lại mã 4522... gốc. Hook chỉ đổi đối số FString của setter cho đúng thẻ; để setter gốc quản lý bộ nhớ. Thêm observer texture callback, luôn gọi callback gốc với đối số nguyên vẹn. Không đổi cơ chế cập nhật facial animation hoặc tạo chuyển động giả.

**Đây là một điểm sai đã tìm được trong luồng nhận diện và tải tài nguyên; chưa đủ bằng chứng kết luận nó là nguyên nhân duy nhất của mặt đơ.** Giữ skeleton và mã profile là điều kiện cần, không phải bằng chứng mắt/miệng đã hoạt động. Nếu vẫn đơ, cần log mới và video cận cảnh khi ăn mừng/replay, so với đầu gốc trong cùng điều kiện, để kiểm tra tiếp facial driver/LOD. Không thể xác nhận biểu cảm chỉ bằng ảnh đứng hoặc log HOOK_ACTIVE.

## Kiểm tra đã làm

- Giải nén CPK/CRILAYLA/FPK, đối chiếu hash bốn mô hình/dữ liệu và 12 texture với nguồn trước.
- UEViewer đọc lại 4 mesh, 4 texture mặt và texture tóc từ container mới; 11 package, mip/bulk/header round-trip.
- Giữ native UV mặt, skin weights, joint indices, màu vertex, topology và bind pose; kiểm tra mặt chuyển có giới hạn, hình học/skin tóc không đổi.
- Thực thi ARM64 bằng Unicorn: 14 kiểm tra gồm phạm vi full Card ID, bốn biến thể đầu, fallback, setter giữ mã numeric chỉ đúng thẻ, callback texture delegate và đọc lại profile actor. Thân các hàm engine được mô hình hóa tại biên; **không phải chạy renderer/facial animation của Android**.
- Chạy đầy đủ bốn nhánh Python installer và worker tới HOOK_ACTIVE với biên ctypes/native mô hình hóa; so prologue/SHA libUE4.so thật. Kiểm tra manifest/hash/idempotence và whitelist ZIP. Gateway giữ 2441 byte, không sửa DEX.

Không sửa dt200, dt870, save, đội hình hoặc thẻ khác. Native module v3 khác v1b/v2 vì có thêm hook bảo toàn nhận diện và observer. Cần buộc dừng game khi cập nhật hoặc quay lại bản cũ.

## Quay lại / tắt

[Quay lại v1b đã được người dùng xác nhận tải đầu](../ronaldo-noodle-v2-color-face/Quay-lai-Ronaldo-v1b.zip): buộc dừng, chép gộp work/ và livedata/ như lúc cài. Nếu chỉ tắt thử đầu, dùng `Tat-dau-thu-Ronaldo.zip` và buộc dừng/mở lại. Không xóa save.

Nguồn mặt/tóc PC do người dùng cung cấp, tóc NEUBE. V3 chưa được thử trên điện thoại.
